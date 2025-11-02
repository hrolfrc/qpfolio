import numpy as np
from typing import Tuple


def simulate_mvn_returns(n_assets: int, n_periods: int, seed: int = 1) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Simulate multivariate normal returns and return (R, mu, Sigma)."""
    rng = np.random.default_rng(seed)
    mu = rng.normal(0.08, 0.05, size=n_assets)
    A = rng.normal(size=(n_assets, n_assets))
    Sigma = A @ A.T
    # scale covariance to reasonable annualized volatility
    Sigma = Sigma / np.max(np.linalg.eigvalsh(Sigma)) * 0.15 ** 2
    R = rng.multivariate_normal(mean=mu / 252.0, cov=Sigma / 252.0, size=n_periods)
    return R, mu, Sigma
