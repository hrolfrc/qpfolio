import numpy as np
from qpfolio.core.metrics import risk_contributions


def test_trc_sum_equals_variance():
    w = np.array([0.4, 0.3, 0.3])
    Sigma = np.array([[0.04, 0.01, 0.00],
                      [0.01, 0.05, 0.02],
                      [0.00, 0.02, 0.06]])
    rc = risk_contributions(w, Sigma)
    var = float(w @ Sigma @ w)
    # sum of total risk contributions equals portfolio variance
    assert abs(rc["trc"].sum() - var) < 1e-10
