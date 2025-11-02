from typing import TYPE_CHECKING, Iterable, Optional
import numpy as np
import matplotlib.pyplot as plt

if TYPE_CHECKING:  # avoid RTD import errors without adding pandas as a hard dep
    import pandas as pd


def plot_frontier(points: Iterable[tuple[float, float, object]], *, ax=None,
                  show_tangent: bool = False, rf: float = 0.0):
    """Plot (risk, return) frontier. Optionally draw CML (tangent) from rf."""
    if ax is None:
        _, ax = plt.subplots()

    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    ax.plot(xs, ys, marker="o", linewidth=1.5)
    ax.set_xlabel("Risk (stdev)")
    ax.set_ylabel("Expected Return")
    ax.set_title("Efficient Frontier")
    ax.grid(True)

    if show_tangent and xs:
        vols = np.asarray(xs, dtype=float)
        rets = np.asarray(ys, dtype=float)
        with np.errstate(divide="ignore", invalid="ignore"):
            sharpe = (rets - rf) / vols
        i = int(np.nanargmax(sharpe))
        ax.plot([0.0, vols[i]], [rf, rets[i]], linestyle="--")
    return ax


def plot_weights_along_frontier(weights: "pd.DataFrame", *, ax=None):
    """Stacked area chart of weights across frontier index."""
    if ax is None:
        _, ax = plt.subplots()

    # index along x, columns as assets
    x = range(len(weights))
    ax.stackplot(x, weights.values.T)
    ax.set_xlabel("Frontier Index")
    ax.set_ylabel("Weight")
    ax.set_title("Weights Along Frontier")
    ax.set_ylim(0.0, 1.0)
    ax.legend(list(weights.columns), loc="best")
    return ax


def plot_risk_contributions(w, Sigma, labels: Optional[list[str]] = None, *, ax=None):
    """Bar chart of total risk contributions as fraction of portfolio σ."""
    if ax is None:
        _, ax = plt.subplots()

    w = np.asarray(w, dtype=float)
    Sigma = np.asarray(Sigma, dtype=float)
    mrc = Sigma @ w                     # marginal risk contribution
    trc = w * mrc                       # total risk contribution
    vol = float(np.sqrt(w @ Sigma @ w))
    frac = trc / vol if vol > 0 else trc

    idx = np.arange(len(w))
    ax.bar(idx, frac)
    if labels:
        ax.set_xticks(idx, labels, rotation=45, ha="right")
    ax.set_ylabel("Risk Contribution (fraction of σ)")
    ax.set_title("Total Risk Contributions")
    ax.grid(True, axis="y", alpha=0.3)
    return ax


def plot_corr_heatmap(Sigma, labels: Optional[list[str]] = None, *, ax=None):
    """Correlation heatmap derived from covariance matrix Σ."""
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
