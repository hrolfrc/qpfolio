from typing import List, Tuple
import matplotlib.pyplot as plt


def plot_frontier(points: List[Tuple[float, float]]):
    """Plot (risk, return) pairs."""
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    plt.figure()
    plt.plot(xs, ys, marker="o")
    plt.xlabel("Risk (stdev)")
    plt.ylabel("Expected Return")
    plt.title("Efficient Frontier")
    plt.grid(True)
    return plt.gca()
