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


def risk_contributions(w, Sigma):
    mrc = Sigma @ w  # marginal risk contribution
    trc = w * mrc  # total risk contribution
    port_sigma = (w @ Sigma @ w) ** 0.5
    return {"mrc": mrc, "trc": trc, "trc_frac": trc / (port_sigma if port_sigma > 0 else 1.0)}


def tracking_error(w, w_ref, Sigma):
    d = w - w_ref
    return float((d @ Sigma @ d) ** 0.5)


def beta_to_benchmark(w, Sigma, w_mkt):
    cov = float(w @ Sigma @ w_mkt)
    var_mkt = float(w_mkt @ Sigma @ w_mkt)
    return cov / var_mkt if var_mkt > 0 else float("nan")


def information_ratio(w, w_ref, mu, Sigma):
    ar = float((w - w_ref) @ mu)
    te = tracking_error(w, w_ref, Sigma)
    return ar / te if te > 0 else float("nan")


def turnover(w_old, w_new):
    return float((abs(w_new - w_old)).sum())


def frontier_to_frame(points, asset_labels=None):
    import pandas as pd, numpy as np
    rows = []
    for i, (risk, ret, sol) in enumerate(points):
        row = {"idx": i, "risk": risk, "return": ret, "obj": sol.obj_value, "status": sol.status}
        if asset_labels is None:
            for j, xj in enumerate(sol.x):
                row[f"w_{j}"] = float(xj)
        else:
            for name, xj in zip(asset_labels, sol.x):
                row[f"w_{name}"] = float(xj)
        rows.append(row)
    return pd.DataFrame(rows).set_index("idx")
