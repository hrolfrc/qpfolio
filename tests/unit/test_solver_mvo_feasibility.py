import numpy as np
from qpfolio.core.models import build_mvo_problem
from qpfolio.solvers.mathopt_osqp import MathOptOSQP


def test_mvo_feasible_long_only():
    mu = np.array([0.08, 0.10, 0.12])
    Sigma = np.array([[0.04, 0.01, 0.00],
                      [0.01, 0.05, 0.02],
                      [0.00, 0.02, 0.06]])
    r_target = 0.09
    prob = build_mvo_problem(mu, Sigma, r_target=r_target, long_only=True)
    sol = MathOptOSQP().solve(prob)

    w = sol.x
    assert np.isclose(w.sum(), 1.0, atol=1e-4)
    assert (w >= -1e-9).all()  # allow tiny numerical slack
    # noinspection PyCompatibility
    assert w @ mu >= r_target - 1e-4
