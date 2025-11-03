from __future__ import annotations

import numpy as np
from typing import Tuple


def sample_mean_cov(
    x: np.ndarray,
    *,
    freq: int = 1,
    ddof: int = 1,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Estimate sample mean vector and covariance matrix for asset returns.

    Parameters
    ----------
    x : np.ndarray
        2D array of shape (T, N) containing return observations.
        Each row is a time step; each column is an asset.
    freq : int, default=1
        Frequency multiplier for annualization or scaling.
        For example:
          - `freq=252` for daily returns → annualized
          - `freq=12`  for monthly returns → annualized
          - `freq=1`   leaves values unscaled
    ddof : int, default=1
        Delta degrees of freedom for covariance (see numpy.cov).

    Returns
    -------
    mu : np.ndarray
        Mean vector (shape (N,)) — scaled by `freq` if specified.
    Sigma : np.ndarray
        Covariance matrix (shape (N, N)) — scaled by `freq` if specified.

    Notes
    -----
    - Annualization assumes independence of returns over periods.
    - Scaling both mean and covariance by `freq` is standard
      for small daily or monthly compounding intervals.

    Examples
    --------
    >>> import numpy as np
    >>> rng = np.random.default_rng(0)
    >>> x = rng.normal(0.001, 0.01, size=(252, 3))
    >>> mu, Sigma = sample_mean_cov(x, freq=252)
    >>> mu.shape, Sigma.shape
    ((3,), (3, 3))
    """
    if x.ndim != 2:
        raise ValueError(f"Expected 2D array, got shape {x.shape}")

    # Mean vector
    mu = np.mean(x, axis=0)
    # Sample covariance (rowvar=False → columns are variables)
    Sigma = np.cov(x, rowvar=False, ddof=ddof)

    # Scale (annualization)
    mu *= freq
    Sigma *= freq

    return mu, Sigma
