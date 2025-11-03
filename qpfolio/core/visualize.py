from __future__ import annotations

from typing import TYPE_CHECKING, Iterable, Optional, Sequence
import numpy as np
import matplotlib.pyplot as plt

if TYPE_CHECKING:  # avoid hard pandas dep at import time
    import pandas as pd


def plot_frontier(points: Iterable[tuple[float, float, object]], *, ax=None):
    """
    Plot (risk, return) efficient frontier.
    points: iterable of (risk, return, solution)
    Returns matplotlib Axes.
    """
    if ax is None:
        _, ax = plt.subplots()

    risks = [float(p[0]) for p in points]
    rets = [float(p[1]) for p in points]
    ax.plot(risks, rets, marker="o", linewidth=1.5)
    ax.set_xlabel("Risk (stdev)")
    ax.set_ylabel("Expected Return")
    ax.set_title("Efficient Frontier")
    ax.grid(True)
    return ax


def plot_frontier_with_cml(points: Iterable[tuple[float, float, object]], *, rf: float = 0.0, ax=None):
    """
    Plot frontier and Capital Market Line (tangent from risk-free rate).
    Returns matplotlib Axes.
    """
    if ax is None:
        _, ax = plt.subplots()

    risks = np.asarray([float(p[0]) for p in points], dtype=float)
    rets = np.asarray([float(p[1]) for p in points], dtype=float)
    ax.plot(risks, rets, marker="o", linewidth=1.5, label="Frontier")

    # CML: pick max Sharpe point
    with np.errstate(divide="ignore", invalid="ignore"):
        sharpe = (rets - rf) / risks
    i = int(np.nanargmax(sharpe))
    ax.plot([0.0, risks[i]], [rf, rets[i]], linestyle="--", label="CML")

    ax.set_xlabel("Risk (stdev)")
    ax.set_ylabel("Expected Return")
    ax.set_title("Efficient Frontier + Capital Market Line")
    ax.grid(True)
    ax.legend(loc="best")
    return ax


def plot_weights_along_frontier(weights: "pd.DataFrame", *, ax=None, labels: Optional[Sequence[str]] = None):
    """
    Stacked area chart of weights across frontier points.
    weights: DataFrame shape (k, n), index=frontier index, columns=assets (w_* or names)
    """
    if ax is None:
        _, ax = plt.subplots()

    x = range(len(weights))
    series = [weights[c].to_numpy() for c in weights.columns]
    ax.stackplot(x, series, labels=(labels if labels else list(weights.columns)))
    ax.set_xlabel("Frontier Index")
    ax.set_ylabel("Weight")
    ax.set_ylim(0.0, 1.0)
    ax.set_title("Weights Along Frontier")
    if labels or len(weights.columns) <= 12:
        ax.legend(loc="upper right", ncols=3)
    ax.grid(True, axis="y", alpha=0.2)
    return ax


def plot_risk_contributions(w, Sigma, labels: Optional[Sequence[str]] = None, *, ax=None):
    """
    Bar chart of total risk contributions as fraction of portfolio stdev.
    """
    if ax is None:
        _, ax = plt.subplots()

    w = np.asarray(w, dtype=float)
    Sigma = np.asarray(Sigma, dtype=float)

    mrc = Sigma @ w
    trc = w * mrc
    vol = float(np.sqrt(max(w @ Sigma @ w, 0.0)))
    frac = trc / vol if vol > 0 else trc

    idx = np.arange(len(w))
    ax.bar(idx, frac)
    if labels:
        ax.set_xticks(idx, labels, rotation=0)
    ax.set_ylabel("Risk Contribution (fraction of σ)")
    ax.set_title("Total Risk Contributions")
    ax.grid(True, axis="y", alpha=0.3)
    return ax


def plot_corr_heatmap(Sigma, labels: Optional[Sequence[str]] = None, *, ax=None):
    """
    Heatmap of correlation implied by covariance Σ.
    """
    if ax is None:
        _, ax = plt.subplots()

    Sigma = np.asarray(Sigma, dtype=float)
    d = np.sqrt(np.clip(np.diag(Sigma), 1e-12, None))
    Corr = Sigma / np.outer(d, d)

    im = ax.imshow(Corr, interpolation="nearest")
    ax.set_title("Correlation Heatmap")
    if labels:
        ax.set_xticks(range(len(labels)))
        ax.set_yticks(range(len(labels)))
        ax.set_xticklabels(labels, rotation=45, ha="right")
        ax.set_yticklabels(labels)
    plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    return ax
