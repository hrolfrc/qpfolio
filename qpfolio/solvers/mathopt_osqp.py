# qpfolio/solvers/mathopt_osqp.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Sequence, Tuple
import numpy as np

try:
    import osqp  # type: ignore
except Exception:  # pragma: no cover
    osqp = None

import scipy.sparse as sp

from qpfolio.core.types import ProblemSpec, Solution, Array


# ---------- Helpers ----------

def _osqp_info_to_dict(info_ns) -> dict:
    """
    Convert OSQP info (often a SimpleNamespace) to a plain dict, tolerating
    version differences in field names.
    """
    base = {}
    try:
        base.update(vars(info_ns))
    except Exception:
        pass

    # Normalize common residual fields if missing on this OSQP version
    if "pri_res" not in base:
        base["pri_res"] = getattr(info_ns, "pri_res", getattr(info_ns, "pri_res_norm", None))
    if "dua_res" not in base:
        base["dua_res"] = getattr(info_ns, "dua_res", getattr(info_ns, "dua_res_norm", None))

    # Common extras (populate if present, otherwise None)
    for k in ("iter", "status_val", "setup_time", "solve_time", "rho"):
        if k not in base:
            base[k] = getattr(info_ns, k, None)

    return base


def _bounds_to_triplet(n: int, bounds: Optional[Sequence[Tuple[Optional[float], Optional[float]]]]):
    """
    Convert variable bounds into an OSQP-style triplet (A_b, l_b, u_b),
    where A_b = I (n x n), l_b[i] <= x_i <= u_b[i].
    None maps to +/- inf appropriately.
    """
    if bounds is None:
        return None, None, None

    I = np.eye(n)
    l = np.empty(n, dtype=float)
    u = np.empty(n, dtype=float)

    for i, bh in enumerate(bounds):
        if bh is None:
            lo, hi = None, None
        else:
            lo, hi = bh
        l[i] = -np.inf if lo is None else float(lo)
        u[i] =  np.inf if hi is None else float(hi)

    return I, l, u


def _stack_osqp_system(
    *,
    Q: Array,
    c: Array,
    A_eq: Optional[Array],
    b_eq: Optional[Array],
    A_ineq: Optional[Array],
    b_ineq: Optional[Array],
    bounds: Optional[Sequence[Tuple[Optional[float], Optional[float]]]],
):
    """
    Build OSQP system P, q, A, l, u from legacy (A_eq, b_eq, A_ineq, b_ineq, bounds).

    Returns:
        P (n,n)  : quadratic matrix (symmetrized)
        q (n,)   : linear vector
        A (m,n)  : constraint matrix
        l (m,)   : lower bounds
        u (m,)   : upper bounds
    """
    n = Q.shape[0]
    blocks_A = []
    blocks_l = []
    blocks_u = []

    # Equality constraints: A_eq x = b_eq  -> b_eq <= A_eq x <= b_eq
    if A_eq is not None and b_eq is not None:
        blocks_A.append(A_eq)
        blocks_l.append(b_eq.astype(float, copy=False))
        blocks_u.append(b_eq.astype(float, copy=False))

    # Inequality constraints: A_ineq x <= b_ineq -> -inf <= A_ineq x <= b_ineq
    if A_ineq is not None and b_ineq is not None:
        blocks_A.append(A_ineq)
        blocks_l.append(-np.inf * np.ones_like(b_ineq, dtype=float))
        blocks_u.append(b_ineq.astype(float, copy=False))

    # Variable bounds -> I x between l and u
    A_b, l_b, u_b = _bounds_to_triplet(n, bounds)
    if A_b is not None:
        blocks_A.append(A_b)
        blocks_l.append(l_b)
        blocks_u.append(u_b)

    if not blocks_A:
        A = np.zeros((0, n), dtype=float)
        l = np.zeros((0,), dtype=float)
        u = np.zeros((0,), dtype=float)
    else:
        A = np.vstack(blocks_A)
        l = np.concatenate(blocks_l)
        u = np.concatenate(blocks_u)

    P = (Q + Q.T) / 2.0
    q = c.astype(float, copy=False)

    return P, q, A, l, u


def _merge_triplet_with_bounds(
    A: Array, l: Array, u: Array,
    bounds: Optional[Sequence[Tuple[Optional[float], Optional[float]]]]
):
    """
    Append variable-bounds rows to an existing (A, l, u) triplet.
    """
    if bounds is None:
        return A, l, u

    n = A.shape[1]
    A_b, l_b, u_b = _bounds_to_triplet(n, bounds)
    if A_b is None:
        return A, l, u

    A2 = np.vstack([A, A_b])
    l2 = np.concatenate([l, l_b])
    u2 = np.concatenate([u, u_b])
    return A2, l2, u2


def _clip_to_bounds(x: Array, bounds: Optional[Sequence[Tuple[Optional[float], Optional[float]]]]) -> Array:
    """
    Numerically enforce variable bounds post-solve to counter tiny solver residuals.
    Clips each x_i into [lo_i, hi_i] when bounds exist; leaves unconstrained coords unchanged.
    """
    if bounds is None:
        return x
    lo = []
    hi = []
    for bh in bounds:
        if bh is None:
            lo.append(-np.inf); hi.append(np.inf)
        else:
            lo.append(float(bh[0]) if bh[0] is not None else -np.inf)
            hi.append(float(bh[1]) if bh[1] is not None else  np.inf)
    lo = np.asarray(lo, dtype=float)
    hi = np.asarray(hi, dtype=float)
    return np.minimum(np.maximum(x, lo), hi)


# ---------- Solver wrapper ----------

@dataclass
class MathOptOSQP:
    """
    Thin OSQP wrapper that understands either:
      (a) OSQP triplet (A, l, u) [preferred], plus optional bounds
      (b) Legacy (A_eq, b_eq, A_ineq, b_ineq) plus bounds
    """
    verbose: bool = False
    eps_abs: float = 1e-7
    eps_rel: float = 1e-7
    max_iter: int = 100000
    polish: bool = True  # enable OSQP polishing by default for tighter feasibility

    def solve(self, problem: ProblemSpec) -> Solution:
        if osqp is None:
            raise RuntimeError(
                "osqp is not installed. Install with `pip install osqp` or include the 'solver' extra."
            )

        # Prefer the triplet if present
        if (problem.A is not None) and (problem.l is not None) and (problem.u is not None):
            P = (problem.Q + problem.Q.T) / 2.0
            q = problem.c.astype(float, copy=False)

            A, l, u = _merge_triplet_with_bounds(problem.A, problem.l, problem.u, problem.bounds)

            Psp = sp.csc_matrix(P)
            Asp = sp.csc_matrix(A)

            prob = osqp.OSQP()
            prob.setup(
                P=Psp,
                q=q,
                A=Asp,
                l=l,
                u=u,
                verbose=self.verbose,
                eps_abs=self.eps_abs,
                eps_rel=self.eps_rel,
                max_iter=self.max_iter,
                polish=self.polish,
            )
            res = prob.solve()

            x = res.x if res.x is not None else np.zeros_like(q)
            # Final small safety: clip to bounds to avoid 1e-7 overshoots.
            x = _clip_to_bounds(x, problem.bounds)

            obj = float(res.info.obj_val) if getattr(res.info, "obj_val", None) is not None else np.nan
            status = str(res.info.status).lower() if getattr(res.info, "status", None) is not None else "unknown"
            info = _osqp_info_to_dict(res.info)
            return Solution(x=x, obj=obj, status=status, info=info)

        # Fallback to legacy path
        A_ineq = problem.A_ineq if problem.A_ineq is not None else problem.G
        b_ineq = problem.b_ineq if problem.b_ineq is not None else problem.h

        P, q, A, l, u = _stack_osqp_system(
            Q=problem.Q,
            c=problem.c,
            A_eq=problem.A_eq,
            b_eq=problem.b_eq,
            A_ineq=A_ineq,
            b_ineq=b_ineq,
            bounds=problem.bounds,
        )

        Psp = sp.csc_matrix(P)
        Asp = sp.csc_matrix(A)

        prob = osqp.OSQP()
        prob.setup(
            P=Psp,
            q=q,
            A=Asp,
            l=l,
            u=u,
            verbose=self.verbose,
            eps_abs=self.eps_abs,
            eps_rel=self.eps_rel,
            max_iter=self.max_iter,
            polish=self.polish,
        )
        res = prob.solve()

        x = res.x if res.x is not None else np.zeros_like(q)
        x = _clip_to_bounds(x, problem.bounds)

        obj = float(res.info.obj_val) if getattr(res.info, "obj_val", None) is not None else np.nan
        status = str(res.info.status).lower() if getattr(res.info, "status", None) is not None else "unknown"
        info = _osqp_info_to_dict(res.info)
        return Solution(x=x, obj=obj, status=status, info=info)
