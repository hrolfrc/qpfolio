````markdown
# qpfolio: Quadratic Programming Portfolio Optimizer

[![CircleCI](https://circleci.com/gh/hrolfrc/qpfolio.svg?style=shield)](https://circleci.com/gh/hrolfrc/qpfolio)
[![ReadTheDocs](https://readthedocs.org/projects/qpfolio/badge/?version=latest)](https://qpfolio.readthedocs.io/en/latest/)
[![Codecov](https://codecov.io/gh/hrolfrc/qpfolio/branch/master/graph/badge.svg)](https://codecov.io/gh/hrolfrc/qpfolio)

**QPFolio** is a Python library for solving **quadratic programming (QP)** portfolio optimization problems using **[OR-Tools](https://developers.google.com/optimization)** and the **[OSQP](https://osqp.org/)** solver backend.  
It provides a clean, extensible API for constructing, solving, and visualizing portfolios based on modern convex optimization techniques.

The library enables users to model and compare multiple optimization philosophies — such as **Markowitz Mean-Variance Optimization (MVO)**, **Most Diversified Portfolio (MDP)**, and **Distributionally Robust Optimization (DRO-lite)** — all solvable with standard QP methods.

---

## Key Features

- **Markowitz Mean-Variance Optimization (MVO):**  
  Find the efficient frontier by minimizing portfolio variance subject to a target return constraint.

- **Most Diversified Portfolio (MDP):**  
  Construct portfolios that maximize diversification ratio for improved stability and balanced risk exposure.

- **Distributionally Robust Optimization (DRO-lite):**  
  Account for uncertainty in return estimates by adding covariance-based robustness penalties — still fully solvable as a convex QP.

- **Efficient Frontier Computation:**  
  Generate the full risk-return trade-off curve and visualize it with one line of code.

- **Risk & Performance Metrics:**  
  Compute Sharpe ratios, diversification ratios, and risk contributions for all portfolios.

- **Solver Abstraction Layer:**  
  Use OR-Tools’ MathOpt interface (with OSQP backend) for robust and fast convex QP solving, or extend easily to CVXPY or Gurobi in future releases.

- **Built-In Visualization:**  
  Plot efficient frontiers, risk decomposition charts, and weight allocations directly via Matplotlib.

---

## Getting Started

### 1. Installation

Ensure you have Python 3.9+ installed.  
You can install **QPFolio** directly from PyPI:

```bash
pip install qpfolio
````
---

### 2. Quick Start

Here’s how to simulate sample asset data, optimize for a target return, and visualize the efficient frontier:

```python
import numpy as np
from qpfolio.core.data import simulate_mvn_returns
from qpfolio.core.estimates import sample_mean_cov
from qpfolio.core.frontier import compute_frontier
from qpfolio.solvers.mathopt_osqp import MathOptOSQP
from qpfolio.core.visualize import plot_frontier

# Simulate 10 assets and estimate mean/covariance
R, mu, Sigma = simulate_mvn_returns(n_assets=10, n_periods=252)
mu_est, Sigma_est = sample_mean_cov(R)

# Define target returns along the frontier
targets = np.linspace(0.05, 0.15, 10)

# Compute efficient frontier
solver = MathOptOSQP()
points = compute_frontier(mu_est, Sigma_est, targets, solver)

# Plot
plot_frontier([(risk, ret) for risk, ret, _ in points])
```

This produces a smooth efficient frontier and returns the corresponding optimal weights for each portfolio point.

---

## Configuration and Extensions

QPFolio’s modular design makes it easy to:

* Swap solver backends via the `Solver` interface.
* Add new optimization formulations (e.g., tracking error minimization, box constraints).
* Extend risk metrics or visualizations.
* Integrate simulated or historical data through standardized input structures.

For example, to include robustness to covariance uncertainty:

```python
from qpfolio.core.models import build_dro_lite_problem
problem = build_dro_lite_problem(mu_est, Sigma_est, r_target=0.1, gamma=0.2)
```

---

## Documentation

Full documentation (including mathematical formulations and developer guides) is available at:
📘 **[qpfolio.readthedocs.io](https://qpfolio.readthedocs.io/en/latest/)**

Topics include:

* Model formulations (MVO, MDP, DRO)
* QP structure and solver setup
* Frontier generation and metrics
* API reference and extension patterns

---

## Contributing

QPFolio is currently in **early development (v0.1.x)** and not yet open for external contributions.
You’re welcome to open issues for feedback, feature suggestions, or bug reports.
See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## License

Distributed under the **Apache License 2.0**.
See [LICENSE](LICENSE) for full terms.

---

**QPFolio** — a mathematical foundation for modern portfolio optimization.

