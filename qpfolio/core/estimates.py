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
    ~~~~~~~~~~
    - **x** (ndarray, shape (T, N)): Return observations. Rows = time, columns = assets.
    - **freq** (int, default 1): Scaling factor (e.g., 252 for daily→annualized).
    - **ddof** (int, default 1): Degrees of freedom for covariance (passed to ``numpy.cov``).

    Returns
    ~~~~~~~
    - **mu** (ndarray, shape (N,)): Mean vector scaled by ``freq``.
    - **Sigma** (ndarray, shape (N, N)): Covariance matrix scaled by ``freq``.

    Notes
    ~~~~~
    Annualization assumes returns are independent across periods. Scaling both mean
    and covariance by ``freq`` is the standard convention for small compounding intervals.

    Examples
    --------
    .. code-block:: python

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
