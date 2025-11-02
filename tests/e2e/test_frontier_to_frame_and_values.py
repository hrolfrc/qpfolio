import numpy as np
from qpfolio.core.frontier import compute_frontier
from qpfolio.core.metrics import frontier_to_frame
from qpfolio.solvers.mathopt_osqp import MathOptOSQP


def test_frontier_to_frame_has_weights_and_metrics():
    mu = np.array([0.08, 0.10, 0.12])
    Sigma = np.array([[0.04, 0.01, 0.00],
                      [0.01, 0.05, 0.02],
                      [0.00, 0.02, 0.06]])
    targets = [0.07, 0.09, 0.11]
    pts = compute_frontier(mu, Sigma, targets, solver=MathOptOSQP())
    df = frontier_to_frame(pts, asset_labels=["A", "B", "C"])
    assert {"risk", "return", "obj", "status", "w_A", "w_B", "w_C"}.issubset(df.columns)
    assert len(df) == len(targets)
