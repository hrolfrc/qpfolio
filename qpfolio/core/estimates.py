import numpy as np
from typing import Tuple


def sample_mean_cov(returns: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Compute sample mean and covariance from returns matrix (T, N)."""
    mu = returns.mean(axis=0) * 252.0
    Sigma = np.cov(returns, rowvar=False) * 252.0
    return mu, Sigma
