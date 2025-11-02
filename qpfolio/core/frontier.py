from typing import Iterable, List, Tuple

import numpy as np

from .models import build_mvo_problem
from .types import Solution


# noinspection PyCompatibility
def compute_frontier(mu: np.ndarray, Sigma: np.ndarray, targets: Iterable[float], solver) -> List[Tuple[float, float, Solution]]:
    """Return list of (risk, ret, solution) along frontier."""
    points = []
    for R in targets:
        prob = build_mvo_problem(mu, Sigma, r_target=R, long_only=True)
        sol = solver.solve(prob)
        status = (sol.status or "").lower()
        if not status.startswith("solved"):
            continue  # skip infeasible or non-optimal points
        risk = float(np.sqrt(sol.x @ Sigma @ sol.x))
        ret = float(sol.x @ mu)
        points.append((risk, ret, sol))
    # ensure increasing risk order (tiny jitter possible)
    points.sort(key=lambda t: t[0])
    return points
