import numpy as np


def expected_return(w: np.ndarray, mu: np.ndarray) -> float:
    return float(w @ mu)


def variance(w: np.ndarray, Sigma: np.ndarray) -> float:
    return float(w @ Sigma @ w)


def sharpe(w: np.ndarray, mu: np.ndarray, Sigma: np.ndarray, rf: float = 0.0) -> float:
    ret = expected_return(w, mu) - rf
    vol = variance(w, Sigma) ** 0.5
    return ret / vol if vol > 0 else float("nan")


def diversification_ratio(w: np.ndarray, sigmas: np.ndarray, Sigma: np.ndarray) -> float:
    num = float(w @ sigmas)
    den = (w @ Sigma @ w) ** 0.5
    return num / den if den > 0 else float("nan")
