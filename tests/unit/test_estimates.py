import numpy as np
from qpfolio.core.estimates import sample_mean_cov


def test_sample_mean_cov_shapes_and_scaling():
    rng = np.random.default_rng(0)
    x = rng.normal(0.001, 0.01, size=(252, 4))
    mu, Sigma = sample_mean_cov(x, freq=252)
    assert mu.shape == (4,)
    assert Sigma.shape == (4, 4)
    assert np.allclose(np.diag(Sigma) > 0, True)
