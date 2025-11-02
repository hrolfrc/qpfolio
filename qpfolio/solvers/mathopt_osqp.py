from __future__ import annotations
from typing import Any, Optional, Sequence, Tuple
import numpy as np
import scipy.sparse as sp
import osqp

from qpfolio.core.types import ProblemSpec, Solution
from qpfolio.solvers.base import Solver


def _stack_osqp_system(
        Q: np.ndarray,
        c: Optional[np.ndarray],
        A_eq: Optional[np.ndarray],
        b_eq: Optional[np.ndarray],
        A_ineq: Optional[np.ndarray],
        b_ineq: Optional[np.ndarray],
        bounds: Optional[Sequence[Tuple[float, float]]],
):
    """
    Build OSQP matrices (P, q, A, l, u) for:
      min 1/2 x^T Q x + c^T x
      s.t. A_eq x = b_eq
           A_ineq x <= b_ineq
           bounds[i][0] <= x_i <= bounds[i][1]
    """
    n = Q.shape[0]
    P = 0.5 * (Q + Q.T)  # ensure symmetry
    # small ridge for numeric stability if not PSD within tolerance
    ev_min = np.linalg.eigvalsh(P).min()
    if ev_min < 1e-10:
        P = P + (1e-8 - min(ev_min, 0.0)) * np.eye(n)

    q = np.zeros(n) if c is None else c.astype(float)

    A_blocks = []
    l_blocks = []
    u_blocks = []

    # Equals: A_eq x = b_eq
    if A_eq is not None and b_eq is not None:
        A_blocks.append(A_eq)
        b_eq = b_eq.astype(float)
        l_blocks.append(b_eq)
        u_blocks.append(b_eq)

    # Inequalities: A_ineq x <= b_ineq  ->  -inf <= A_ineq x <= b_ineq
    if A_ineq is not None and b_ineq is not None:
        m_ineq = A_ineq.shape[0]
        A_blocks.append(A_ineq)
        l_blocks.append(np.full(m_ineq, -np.inf))
        u_blocks.append(b_ineq.astype(float))

    # Bounds: lo <= x <= hi
    if bounds is not None:
        lo = np.array([b[0] if b[0] is not None else -np.inf for b in bounds], dtype=float)
        hi = np.array([b[1] if b[1] is not None else np.inf for b in bounds], dtype=float)
        I = np.eye(n)
        # x >= lo  ->  lo <= I x <= +inf
        A_blocks.append(I)
        l_blocks.append(lo)
        u_blocks.append(np.full(n, np.inf))
        # x <= hi  ->  -inf <= I x <= hi
        A_blocks.append(I)
        l_blocks.append(np.full(n, -np.inf))
        u_blocks.append(hi)

    if A_blocks:
        A = np.vstack(A_blocks)
        l = np.concatenate(l_blocks)
        u = np.concatenate(u_blocks)
    else:
        # No constraints: add dummy zero rows to satisfy OSQP (needs A)
        A = np.zeros((1, n))
        l = np.array([-np.inf])
        u = np.array([np.inf])

    return sp.csc_matrix(P), q.astype(float), sp.csc_matrix(A), l, u


class MathOptOSQP(Solver):
    """
    OSQP-backed solver that satisfies the Solver interface.

    Note:
      - Uses the native OSQP Python API. You can later replace internals with
        OR-Tools MathOpt+OSQP while preserving this public class.
    """

    def __init__(self, **options: Any):
        # Sensible defaults; user can still override via options
        defaults = dict(
            eps_abs=1e-6,
            eps_rel=1e-6,
            max_iter=20000,
            polish=True,  # refine primal/dual
            adaptive_rho=True,
        )
        # noinspection PyCompatibility
        self.options = {**defaults, **(options or {})}

    def solve(self, problem: ProblemSpec) -> Solution:
        if osqp is None:
            raise RuntimeError("osqp is not installed. Install with `pip install osqp` or include the 'solver' extra.")

        P, q, A, l, u = _stack_osqp_system(
            Q=problem.Q,
            c=problem.c,
            A_eq=problem.A_eq,
            b_eq=problem.b_eq,
            A_ineq=problem.A_ineq,
            b_ineq=problem.b_ineq,
            bounds=problem.bounds,
        )

        prob = osqp.OSQP()
        prob.setup(P=P, q=q, A=A, l=l, u=u, **self.options)
        res = prob.solve()

        status = str(res.info.status)
        x = np.array(res.x, dtype=float) if res.x is not None else np.zeros(P.shape[0])
        obj = float(res.info.obj_val) if res.info.obj_val is not None else float("nan")

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
