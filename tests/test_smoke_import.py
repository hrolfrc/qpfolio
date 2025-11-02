def test_import_and_version():
    import qpfolio
    assert hasattr(qpfolio, "__version__")


def test_frontier_mock_solver():
    import numpy as np
    from qpfolio.core.frontier import compute_frontier
    from qpfolio.solvers.mathopt_osqp import MathOptOSQP

    n = 3
    mu = np.array([0.08, 0.10, 0.12])
    Sigma = np.eye(n) * 0.04
    targets = [0.07, 0.09, 0.11]
    pts = compute_frontier(mu, Sigma, targets, solver=MathOptOSQP())
    assert len(pts) == len(targets)


def test_trc_sum():
    import numpy as np
    from qpfolio.core.metrics import risk_contributions
    w = np.array([0.5, 0.5]);
    Sigma = np.array([[0.04, 0.0], [0.0, 0.09]])
    rc = risk_contributions(w, Sigma)
    var = float(w @ Sigma @ w)
    assert abs(rc["trc"].sum() - var) < 1e-12
