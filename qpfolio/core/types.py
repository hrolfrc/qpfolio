# qpfolio/core/types.py
from dataclasses import dataclass
from typing import Optional, Sequence, Tuple, Mapping, Any
import numpy as np

Array = np.ndarray


@dataclass
class ProblemSpec:
    """
    Generic QP container with light validation.

    Objective:
        minimize 0.5 * x^T Q x + c^T x

    Linear constraints (two supported forms):

    (1) OSQP triplet (preferred):
        l <= A x <= u

    (2) Legacy equality/inequality + bounds (still supported):
        A_eq x = b_eq
        A_ineq x <= b_ineq
        bounds[i] = (lb_i, ub_i)

    Notes:
        - You may supply either (1) or (2). If both are supplied, the solver
          will prefer (1) and ignore (2).
        - Bounds are allowed with either form. When using the triplet, bounds
          are folded into (A,l,u) before calling OSQP.
    """
    # Objective
    Q: Array  # (n, n) PSD / symmetric
    c: Array  # (n,)

    # --- OSQP triplet (optional) ---
    A: Optional[Array] = None  # (m, n)
    l: Optional[Array] = None  # (m,)
    u: Optional[Array] = None  # (m,)

    # --- Variable bounds (optional) ---
    # Each entry is (lo, hi); use None for +/- inf.
    bounds: Optional[Sequence[Tuple[Optional[float], Optional[float]]]] = None  # len n

    # --- Legacy equality/inequality forms (optional) ---
    A_eq: Optional[Array] = None  # (k, n)
    b_eq: Optional[Array] = None  # (k,)
    A_ineq: Optional[Array] = None  # (p, n)
    b_ineq: Optional[Array] = None  # (p,)

    # (Kept for compatibility with any code that references these names)
    G: Optional[Array] = None  # alias for A_ineq (if ever used)
    h: Optional[Array] = None  # alias for b_ineq (if ever used)

    def __post_init__(self):
        # Validate Q, c
        if self.Q.ndim != 2 or self.Q.shape[0] != self.Q.shape[1]:
            raise ValueError("Q must be square (n x n).")
        n = self.Q.shape[0]
        if self.c.shape != (n,):
            raise ValueError("c must have shape (n,).")

        # Validate OSQP triplet if any is provided
        using_triplet = (self.A is not None) or (self.l is not None) or (self.u is not None)
        if using_triplet:
            if self.A is None or self.l is None or self.u is None:
                raise ValueError("If using OSQP triplet, A, l, and u must be provided together.")
            if self.A.ndim != 2 or self.A.shape[1] != n:
                raise ValueError("A must have shape (m, n).")
            m = self.A.shape[0]
            if self.l.shape != (m,) or self.u.shape != (m,):
                raise ValueError("l and u must have shape (m,).")
            if not np.all(self.l <= self.u):
                raise ValueError("Each row bound must satisfy l[i] <= u[i].")

        # Validate bounds if present
        if self.bounds is not None:
            if len(self.bounds) != n:
                raise ValueError("bounds must have length n.")
            for i, bh in enumerate(self.bounds):
                if bh is None:
                    # allow None entry meaning no bounds row at all
                    continue
                lo, hi = bh
                if (lo is not None) and (hi is not None) and (lo > hi):
                    raise ValueError(f"bounds[{i}] has lo > hi.")

        # Validate legacy equality
        if self.A_eq is not None:
            if self.A_eq.ndim != 2 or self.A_eq.shape[1] != n:
                raise ValueError("A_eq must have shape (k, n).")
            k = self.A_eq.shape[0]
            if self.b_eq is None or self.b_eq.shape != (k,):
                raise ValueError("b_eq must have shape (k,).")

        # Validate legacy inequality
        # Accept either (A_ineq, b_ineq) or (G, h) as aliases. Don't require both sets.
        A_ineq = self.A_ineq if self.A_ineq is not None else self.G
        b_ineq = self.b_ineq if self.b_ineq is not None else self.h
        if (A_ineq is not None) or (b_ineq is not None):
            if A_ineq is None or b_ineq is None:
                raise ValueError("If using inequality form, both A_ineq(G) and b_ineq(h) must be provided.")
            if A_ineq.ndim != 2 or A_ineq.shape[1] != n:
                raise ValueError("A_ineq/G must have shape (p, n).")
            p = A_ineq.shape[0]
            if b_ineq.shape != (p,):
                raise ValueError("b_ineq/h must have shape (p,).")


@dataclass
class Solution:
    """
    Standardized QP solution container.
    """
    x: Array  # optimal variable vector (n,)
    obj: float  # objective value at x (0.5 x^T Q x + c^T x)
    status: str  # e.g., "solved", "optimal", "infeasible", etc.
    info: Optional[Mapping[str, Any]] = None  # raw solver stats/timings/etc.

    # Backward-compat alias for older code/tests expecting .obj_value
    @property
    def obj_value(self) -> float:
        return self.obj


__all__ = [
    "Array",
    "ProblemSpec",
    "Solution",
]
