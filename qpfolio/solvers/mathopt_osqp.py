from __future__ import annotations

from typing import Any, Optional, Sequence, Tuple

import numpy as np
import osqp
import scipy.sparse as sp

from qpfolio.core.types import ProblemSpec, Solution
from qpfolio.solvers.base import Solver


# noinspection PyCompatibility
def _stack_osqp_system(
        Q: np.ndarray,
        c: Optional[np.ndarray],
        A_eq: Optional[np.ndarray],
        b_eq: Optional[np.ndarray],
        A_ineq: Optional[np.ndarray],
        b_ineq: Optional[np.ndarray],
        bounds: Optional[Sequence[Tuple[float, float]]],
) -> tuple[sp.csc_matrix, np.ndarray, sp.csc_matrix, np.ndarray, np.ndarray]:
    """
    Build OSQP matrices (P, q, A, lower, upper) for the problem:

        minimize   (1/2) x^T Q x + c^T x
        subject to A_eq x = b_eq
                   A_ineq x <= b_ineq
                   bounds[i][0] <= x_i <= bounds[i][1]

    Returns
    -------
    P : csc_matrix
    q : ndarray
    A : csc_matrix
    lower : ndarray
    upper : ndarray
    """
    n = Q.shape[0]

    # Symmetrize Q and add a tiny ridge if necessary for numerical stability
    P = 0.5 * (Q + Q.T)
    ev_min = np.linalg.eigvalsh(P).min()
    if ev_min < 1e-10:
        P = P + (1e-8 - min(ev_min, 0.0)) * np.eye(n)

    q = np.zeros(n, dtype=float) if c is None else c.astype(float, copy=False)

    A_blocks: list[np.ndarray] = []
    lower_blocks: list[np.ndarray] = []
    upper_blocks: list[np.ndarray] = []

    # Equality constraints: A_eq x = b_eq  -> lower == upper == b_eq
    if A_eq is not None and b_eq is not None:
        A_blocks.append(A_eq)
        b_eqf = b_eq.astype(float, copy=False)
        lower_blocks.append(b_eqf)
        upper_blocks.append(b_eqf)

    # Inequality constraints: A_ineq x <= b_ineq  ->  -inf <= A_ineq x <= b_ineq
    if A_ineq is not None and b_ineq is not None:
        m_ineq = A_ineq.shape[0]
        A_blocks.append(A_ineq)
        lower_blocks.append(np.full(m_ineq, -np.inf, dtype=float))
        upper_blocks.append(b_ineq.astype(float, copy=False))

    # Variable bounds: lo <= x <= hi
    if bounds is not None:
        lo_vec = np.array([b[0] if b[0] is not None else -np.inf for b in bounds], dtype=float)
        hi_vec = np.array([b[1] if b[1] is not None else np.inf for b in bounds], dtype=float)
        eye_n = np.eye(n, dtype=float)

        # x >= lo     ->  lo <= I x <= +inf
        A_blocks.append(eye_n)
        lower_blocks.append(lo_vec)
        upper_blocks.append(np.full(n, np.inf, dtype=float))

        # x <= hi     ->  -inf <= I x <= hi
        A_blocks.append(eye_n)
        lower_blocks.append(np.full(n, -np.inf, dtype=float))
        upper_blocks.append(hi_vec)

    if A_blocks:
        A = np.vstack(A_blocks)
        lower = np.concatenate(lower_blocks)
        upper = np.concatenate(upper_blocks)
    else:
        # OSQP requires an A matrix; use a single dummy row with unbounded range
        A = np.zeros((1, n), dtype=float)
        lower = np.array([-np.inf], dtype=float)
        upper = np.array([np.inf], dtype=float)

    return sp.csc_matrix(P), q, sp.csc_matrix(A), lower, upper


class MathOptOSQP(Solver):
    """
    OSQP-backed solver implementing the generic Solver interface.

    Notes
    -----
    - Uses the native OSQP Python API internally.
      You can later swap internals to OR-Tools MathOpt+OSQP without changing this class.
    - Default tolerances are tightened for small portfolio problems; callers can override
      via keyword options (e.g., MathOptOSQP(eps_abs=1e-5, eps_rel=1e-5)).
    """

    # noinspection PyCompatibility
    def __init__(self, **options: Any):
        defaults = dict(
            eps_abs=1e-6,
            eps_rel=1e-6,
            max_iter=20000,
            polish=True,
            adaptive_rho=True,
        )
        self.options = {**defaults, **(options or {})}

    # noinspection PyCompatibility
    def solve(self, problem: ProblemSpec) -> Solution:
        if osqp is None:
            raise RuntimeError(
                "osqp is not installed. Install with `pip install osqp` or include the 'solver' extra."
            )

        P, q, A, lower, upper = _stack_osqp_system(
            Q=problem.Q,
            c=problem.c,
            A_eq=problem.A_eq,
            b_eq=problem.b_eq,
            A_ineq=problem.A_ineq,
            b_ineq=problem.b_ineq,
            bounds=problem.bounds,
        )

        prob = osqp.OSQP()
        # Last-argument-wins: user-provided options override defaults
        prob.setup(P=P, q=q, A=A, l=lower, u=upper, **self.options)
        res = prob.solve()

        status = str(getattr(res.info, "status", "unknown"))
        x = np.array(res.x, dtype=float) if getattr(res, "x", None) is not None else np.zeros(P.shape[0])
        obj = float(getattr(res.info, "obj_val", np.nan))

        # Optional: (very small) post-solve snap for equalities already near-feasible.
        # This avoids pretty-print jitter like sum(w)=0.9999998 in downstream artifacts.
        if (
                problem.A_eq is not None
                and problem.b_eq is not None
                and res.x is not None
        ):
            Ax = problem.A_eq @ x
            err = problem.b_eq - Ax
            # Only attempt correction if already very close (keeps inequality feasibility safe in practice)
            if np.linalg.norm(err, ord=np.inf) <= 1e-3:
                M = problem.A_eq @ problem.A_eq.T
                try:
                    corr = problem.A_eq.T @ np.linalg.solve(M, err)
                    x = x + corr
                except np.linalg.LinAlgError:
                    pass  # keep original x if M is ill-conditioned

        return Solution(
            x=x,
            obj_value=obj,
            status=status,
            info={
                "iter": getattr(res.info, "iter", None),
                "status_val": getattr(res.info, "status_val", None),
                "run_time": getattr(res.info, "run_time", None),
                "pri_res": getattr(res.info, "pri_res", None),
                "dua_res": getattr(res.info, "dua_res", None),
            },
        )
