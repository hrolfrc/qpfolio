from typing import List, Tuple
import matplotlib.pyplot as plt


# def plot_frontier(points: List[Tuple[float, float]]):
#     """Plot (risk, return) pairs."""
#     xs = [p[0] for p in points]
#     ys = [p[1] for p in points]
#     plt.figure()
#     plt.plot(xs, ys, marker="o")
#     plt.xlabel("Risk (stdev)")
#     plt.ylabel("Expected Return")
#     plt.title("Efficient Frontier")
#     plt.grid(True)
#     return plt.gca()

# efficient frontier + optional tangent/CML
def plot_frontier(points, *, ax=None, show_tangent=False, rf=0.0):
    """
    Parameters
    ----------
    points : list[(risk, ret, Solution)]
    show_tangent : bool
        If True and rf provided, draw capital market line (CML).
    Returns
    -------
    matplotlib.axes.Axes
    """


# stacked area chart of weights along the frontier
def plot_weights_along_frontier(weights: "pd.DataFrame", *, ax=None):
    """
    weights: DataFrame indexed by target return or frontier index, columns=assets
    """


# risk contribution bar chart for a single portfolio
def plot_risk_contributions(w, Sigma, labels=None, *, ax=None):
    """
    Computes mrc = Σ w, trc_i = w_i * (Σ w)_i
    Plots total risk contributions normalized by portfolio stdev.
    """


# covariance/ correlation heatmap
def plot_corr_heatmap(Sigma, labels=None, *, ax=None):
    """
    Cor = D^{-1/2} Σ D^{-1/2}
    """
