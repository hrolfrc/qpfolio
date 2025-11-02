import numpy as np
from qpfolio.core.data import simulate_mvn_returns


def test_simulation_is_deterministic_with_seed():
    R1, mu1, S1 = simulate_mvn_returns(5, 200, seed=123)
    R2, mu2, S2 = simulate_mvn_returns(5, 200, seed=123)
    assert np.allclose(R1, R2)
    assert np.allclose(mu1, mu2)
    assert np.allclose(S1, S2)
