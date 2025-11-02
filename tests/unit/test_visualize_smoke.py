import numpy as np
from qpfolio.core.visualize import plot_frontier, plot_risk_contributions, plot_corr_heatmap
import matplotlib

matplotlib.use("Agg")  # headless


def test_plot_smoke():
    pts = [(0.05, 0.04, object()), (0.06, 0.055, object())]
    ax = plot_frontier(pts)
    assert ax is not None

    w = np.array([0.6, 0.4])
    Sigma = np.array([[0.04, 0.01], [0.01, 0.05]])
    ax = plot_risk_contributions(w, Sigma, labels=["A", "B"])
    assert ax is not None

    ax = plot_corr_heatmap(Sigma, labels=["A", "B"])
    assert ax is not None
