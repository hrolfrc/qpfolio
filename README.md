# qpfolio: Quadratic Programming Portfolio Optimizer

[![CircleCI](https://circleci.com/gh/hrolfrc/qpfolio.svg?style=shield)](https://circleci.com/gh/hrolfrc/qpfolio)
[![ReadTheDocs](https://readthedocs.org/projects/qpfolio/badge/?version=latest)](https://qpfolio.readthedocs.io/en/latest/)
[![Codecov](https://codecov.io/gh/hrolfrc/qpfolio/branch/master/graph/badge.svg)](https://codecov.io/gh/hrolfrc/qpfolio)

**QPFolio** is a Python library for solving **quadratic programming (QP)** portfolio optimization problems using **[OR-Tools](https://developers.google.com/optimization)** and the **[OSQP](https://osqp.org/)** solver backend.  
It provides an extensible API for constructing, solving,
and visualizing portfolios based on modern convex optimization techniques.

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
