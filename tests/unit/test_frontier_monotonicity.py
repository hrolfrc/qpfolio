import numpy as np
from qpfolio.core.frontier import compute_frontier
from qpfolio.solvers.mathopt_osqp import MathOptOSQP


def test_frontier_risk_non_decreasing():
    mu = np.array([0.08, 0.10, 0.12, 0.13])
    Sigma = np.array([[0.04, 0.01, 0.01, 0.00],
                      [0.01, 0.05, 0.02, 0.01],
                      [0.01, 0.02, 0.06, 0.02],
                      [0.00, 0.01, 0.02, 0.07]])
    targets = np.linspace(0.06, 0.14, 9)
    pts = compute_frontier(mu, Sigma, targets, solver=MathOptOSQP())
    risks = [r for (r, _, _) in pts]
    assert all(risks[i] <= risks[i + 1] + 1e-6 for i in range(len(risks) - 1))
