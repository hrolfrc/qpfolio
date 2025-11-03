from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class GBMParams:
    """Per-asset GBM parameters."""
    mu: float          # annualized drift (e.g., 0.08)
    sigma: float       # annualized volatility (e.g., 0.20)
    s0: float = 100.0  # initial price


def _as_arrays(
    mus: np.ndarray | float,
    sigmas: np.ndarray | float,
    s0s: np.ndarray | float,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    mus = np.atleast_1d(np.asarray(mus, dtype=float))
    sigmas = np.atleast_1d(np.asarray(sigmas, dtype=float))
    s0s = np.atleast_1d(np.asarray(s0s, dtype=float))
    if not (mus.shape == sigmas.shape == s0s.shape):
        raise ValueError("mus, sigmas, and s0s must have the same shape.")
    return mus, sigmas, s0s


def simulate_gbm_paths(
    mus: np.ndarray | float,
    sigmas: np.ndarray | float,
    *,
    T: float = 1.0,
    steps_per_year: int = 252,
    s0: np.ndarray | float = 100.0,
    n_paths: int = 1,
    seed: Optional[int] = None,
) -> pd.Panel | dict[int, pd.DataFrame]:
    """
    Simulate (vector) GBM price paths for N assets over [0, T].

    S(t) = S(0) * exp((mu - 0.5*sigma^2) t + sigma W(t))

    Returns a dict: {path_index: DataFrame(time_index, assets)}.
    (pandas.Panel is deprecated; returning dict keeps dependencies light.)
    """
    rng = np.random.default_rng(seed)
    mus, sigmas, s0s = _as_arrays(mus, sigmas, s0)

    n_assets = mus.size
    n_steps = int(T * steps_per_year)
    dt = 1.0 / steps_per_year
    times = np.linspace(0.0, T, n_steps + 1)

    out: dict[int, pd.DataFrame] = {}
    for p in range(n_paths):
        # standard Brownian increments ~ N(0, dt)
        Z = rng.standard_normal(size=(n_steps, n_assets))
        dW = np.sqrt(dt) * Z
        W = np.vstack([np.zeros((1, n_assets)), np.cumsum(dW, axis=0)])

        drift = (mus - 0.5 * sigmas**2) * times[:, None]
        diff  = sigmas * W
        X = drift + diff
        S = s0s * np.exp(X)  # (n_steps+1, n_assets)

        df = pd.DataFrame(S, index=pd.Index(times, name="t"))
        out[p] = df
    return out


def simulate_prices_and_returns(
    mus: np.ndarray | float,
    sigmas: np.ndarray | float,
    *,
    T: float = 1.0,
    steps_per_year: int = 252,
    s0: np.ndarray | float = 100.0,
    seed: Optional[int] = None,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Convenience wrapper for a single path: returns (prices, log_returns).
    """
    paths = simulate_gbm_paths(
        mus, sigmas, T=T, steps_per_year=steps_per_year, s0=s0, n_paths=1, seed=seed
    )
    prices = paths[0]
    # log returns aligned to (1..end); prepend zeros to keep same length as prices
    log_ret = np.log(prices).diff().fillna(0.0)
    return prices, log_ret
