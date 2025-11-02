import numpy as np
from typing import Iterable, List, Tuple
from .models import build_mvo_problem
from .solve import solve_qp
from .types import Solution


def compute_frontier(mu: np.ndarray, Sigma: np.ndarray, r_targets: Iterable[float], solver) -> List[
    Tuple[float, float, Solution]]:
    """Return list of (risk, ret, solution) along frontier."""
    results = []
    for r in r_targets:
        problem = build_mvo_problem(mu, Sigma, r_target=r, long_only=True)
        sol = solve_qp(problem, solver)
        w = sol.x
        port_ret = float(w @ mu)
        port_var = float(w @ Sigma @ w)
        results.append((port_var ** 0.5, port_ret, sol))
    return results
