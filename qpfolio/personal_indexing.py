# qpfolio/personal_indexing.py
from __future__ import annotations

from typing import Iterable, Optional, Sequence, Tuple

import numpy as np

from qpfolio.core.types import ProblemSpec, Solution
from qpfolio.solvers.mathopt_osqp import MathOptOSQP


Bounds = Sequence[Tuple[float, float]]


def _apply_exclusions_and_caps(
    n: int,
    max_weight: float,
    exclude: Optional[Iterable[int]] = None,
) -> Bounds:
    """
    Build per-asset bounds for long-only portfolios with optional exclusions and caps.
    Each asset gets (0, max_weight) unless excluded, in which case (0, 0).
    """
    cap = float(max_weight)
    bounds: list[Tuple[float, float]] = [(0.0, cap) for _ in range(n)]
    if exclude:
        for idx in exclude:
            if 0 <= idx < n:
                bounds[idx] = (0.0, 0.0)  # force weight to zero
    return tuple(bounds)


def _sum_to_one_constraint_A_l_u(n: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Equality constraint in (A, l, u) form:
        sum_i w_i = 1  <=>  A w between l and u with l = u = 1
    Returns (A, l, u) where A has shape (1, n) and l, u have shape (1,).
    """
    A = np.ones((1, n), dtype=float)
    l = np.array([1.0], dtype=float)
    u = np.array([1.0], dtype=float)
    return A, l, u


def personal_index_optimizer(
    Sigma: np.ndarray,
    w_bench: np.ndarray,
    *,
    max_weight: float = 0.05,
    exclude: Optional[Iterable[int]] = None,
    solver: Optional[MathOptOSQP] = None,
) -> Solution:
    """
    Tracking-error QP (long-only, per-asset cap, optional exclusions).

    Minimize 0.5 (w - w_bench)^T Σ (w - w_bench)
    subject to sum(w) = 1, 0 ≤ w_i ≤ max_weight, and optional exclusions.

    Expands (dropping constants) to a standard convex QP:
        min 0.5 * w^T Σ w  +  (-Σ w_bench)^T w
    """
    n = int(Sigma.shape[0])
    if Sigma.shape != (n, n):
        raise ValueError("Sigma must be square (n x n).")
    if w_bench.shape != (n,):
        raise ValueError("w_bench must have shape (n,).")

    Q = np.array(Sigma, dtype=float)
    c = -Q @ np.array(w_bench, dtype=float)

    A, l, u = _sum_to_one_constraint_A_l_u(n)
    bounds = _apply_exclusions_and_caps(n, max_weight, exclude)

    problem = ProblemSpec(Q=Q, c=c, A=A, l=l, u=u, bounds=bounds)
    use_solver = solver or MathOptOSQP()
    return use_solver.solve(problem)


def personal_index_optimizer_esg(
    Sigma: np.ndarray,
    w_bench: np.ndarray,
    *,
    exposure_matrix: Optional[np.ndarray] = None,   # rows = exposures, cols = assets
    exposure_targets: Optional[np.ndarray] = None,  # length = n_exposures
    exposure_penalty: float = 1.0,                  # λ for L2 exposure penalty
    max_weight: float = 0.05,
    exclude: Optional[Iterable[int]] = None,
    solver: Optional[MathOptOSQP] = None,
) -> Solution:
    """
    Personalized tracking with *quadratic exposure penalties* (keeps it QP).

    Objective:
        0.5 (w - w_bench)^T Σ (w - w_bench) + 0.5 * λ * ||E w - t||_2^2

    Expands to:
        0.5 * w^T (Σ + λ E^T E) w + [(-Σ w_bench) - λ E^T t]^T w   (constants omitted)

    Notes
    -----
    - L2 exposure penalties keep the problem a convex QP.
    - If `exposure_matrix` is provided without `exposure_targets`, targets default to E @ w_bench.
    """
    n = int(Sigma.shape[0])
    if Sigma.shape != (n, n):
        raise ValueError("Sigma must be square (n x n).")
    if w_bench.shape != (n,):
        raise ValueError("w_bench must have shape (n,).")

    Q = np.array(Sigma, dtype=float)
    c = -Q @ np.array(w_bench, dtype=float)

    if exposure_matrix is not None and exposure_penalty > 0.0:
        E = np.array(exposure_matrix, dtype=float)
        if E.shape[1] != n:
            raise ValueError("exposure_matrix must have shape (k, n).")
        if exposure_targets is None:
            t = E @ w_bench
        else:
            t = np.array(exposure_targets, dtype=float)
            if t.shape != (E.shape[0],):
                raise ValueError("exposure_targets must have shape (k,).")
        lam = float(exposure_penalty)
        Q = Q + lam * (E.T @ E)
        c = c - lam * (E.T @ t)

    A, l, u = _sum_to_one_constraint_A_l_u(n)
    bounds = _apply_exclusions_and_caps(n, max_weight, exclude)

    problem = ProblemSpec(Q=Q, c=c, A=A, l=l, u=u, bounds=bounds)
    use_solver = solver or MathOptOSQP()
    return use_solver.solve(problem)


def personal_index_optimizer_taxaware(
    Sigma: np.ndarray,
    w_bench: np.ndarray,
    *,
    w_prev: np.ndarray,
    tax_weights: Optional[np.ndarray] = None,  # nonnegative weights for turnover penalty
    turnover_penalty: float = 1.0,             # η for L2 turnover penalty
    max_weight: float = 0.05,
    exclude: Optional[Iterable[int]] = None,
    solver: Optional[MathOptOSQP] = None,
) -> Solution:
    """
    Tax/turnover-aware tracking using an **L2 turnover penalty** (QP-safe).

    Objective:
        0.5 (w - w_bench)^T Σ (w - w_bench) + 0.5 * η * ||D (w - w_prev)||_2^2

    with D = diag(tax_weights) (identity if None). Expands to:
        0.5 * w^T (Σ + η D^T D) w + [(-Σ w_bench) - η D^T D w_prev]^T w
    """
    n = int(Sigma.shape[0])
    if Sigma.shape != (n, n):
        raise ValueError("Sigma must be square (n x n).")
    if w_bench.shape != (n,):
        raise ValueError("w_bench must have shape (n,).")
    if w_prev.shape != (n,):
        raise ValueError("w_prev must have shape (n,).")

    Q = np.array(Sigma, dtype=float)
    c = -Q @ np.array(w_bench, dtype=float)

    if turnover_penalty > 0.0:
        eta = float(turnover_penalty)
        if tax_weights is None:
            d = np.ones(n, dtype=float)
        else:
            d = np.array(tax_weights, dtype=float)
            if d.shape != (n,):
                raise ValueError("tax_weights must have shape (n,).")
            if np.any(d < 0):
                raise ValueError("tax_weights must be nonnegative.")
        dd = np.square(d)  # diagonal entries of D^T D
        Q = Q + eta * np.diag(dd)
        c = c - eta * (dd * np.array(w_prev, dtype=float))

    A, lower, upper = _sum_to_one_constraint_A_l_u(n)
    bounds = _apply_exclusions_and_caps(n, max_weight, exclude)

    problem = ProblemSpec(Q=Q, c=c, A=A, l=lower, u=upper, bounds=bounds)
    use_solver = solver or MathOptOSQP()
    return use_solver.solve(problem)
