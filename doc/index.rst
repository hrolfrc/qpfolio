.. qpfolio documentation master file
   Created by Sphinx for Read the Docs.

qpfolio: Quadratic Programming Portfolio Optimizer
==================================================

.. image:: https://circleci.com/gh/hrolfrc/qpfolio.svg?style=shield
   :target: https://circleci.com/gh/hrolfrc/qpfolio
   :alt: CircleCI Build Status

.. image:: https://readthedocs.org/projects/qpfolio/badge/?version=latest
   :target: https://qpfolio.readthedocs.io/en/latest/
   :alt: ReadTheDocs

.. image:: https://codecov.io/gh/hrolfrc/qpfolio/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/hrolfrc/qpfolio
   :alt: Codecov Coverage

**QPFolio** is a Python library for solving **quadratic programming (QP)** portfolio optimization problems using
`OR-Tools <https://developers.google.com/optimization>`_ and the
`OSQP solver <https://osqp.org/>`_. It provides a clean, extensible API for constructing, solving,
and visualizing portfolios based on modern convex optimization techniques.

The library enables users to model and compare multiple optimization philosophies—such as
**Markowitz Mean-Variance Optimization (MVO)**, **Most Diversified Portfolio (MDP)**,
and **Distributionally Robust Optimization (DRO-lite)**—all solvable with standard QP methods.

----

Key Features
------------

* **Markowitz Mean-Variance Optimization (MVO):**
  Minimize portfolio variance subject to a target return constraint and full investment.

* **Most Diversified Portfolio (MDP):**
  Construct portfolios that maximize diversification ratio for improved stability and balanced risk exposure.

* **Distributionally Robust Optimization (DRO-lite):**
  Introduce robustness to uncertainty in return estimates through covariance inflation—remaining fully convex.

* **Efficient Frontier Computation:**
  Generate the complete risk-return trade-off curve and visualize it easily.

* **Risk & Performance Metrics:**
  Compute Sharpe ratios, diversification ratios, and risk contributions.

* **Solver Abstraction Layer:**
  Built on top of OR-Tools MathOpt with OSQP backend; extendable to CVXPY, Gurobi, or other solvers.

* **Visualization Tools:**
  Plot efficient frontiers, allocation breakdowns, and risk contributions via Matplotlib.

----

Getting Started
---------------

Installation
~~~~~~~~~~~~

Ensure you have Python 3.9 or later installed.

Install QPFolio from PyPI:

.. code-block:: bash

   pip install qpfolio

For development or documentation builds:

.. code-block:: bash

   pip install -e ".[dev,docs]"

Quick Start
~~~~~~~~~~~

Simulate assets, compute the efficient frontier, and visualize results:

.. code-block:: python

   import numpy as np
   from qpfolio.core.data import simulate_mvn_returns
   from qpfolio.core.estimates import sample_mean_cov
   from qpfolio.core.frontier import compute_frontier
   from qpfolio.solvers.mathopt_osqp import MathOptOSQP
   from qpfolio.core.visualize import plot_frontier

   R, mu, Sigma = simulate_mvn_returns(n_assets=10, n_periods=252)
   mu_est, Sigma_est = sample_mean_cov(R)

   targets = np.linspace(0.05, 0.15, 10)
   solver = MathOptOSQP()
   points = compute_frontier(mu_est, Sigma_est, targets, solver)
   plot_frontier([(risk, ret) for risk, ret, _ in points])

This produces the efficient frontier and returns optimal portfolio weights for each target return.

----

Configuration and Extensions
----------------------------

QPFolio is designed for flexibility:

* Swap solvers easily using the :class:`qpfolio.solvers.base.Solver` interface.
* Add new optimization models (e.g., tracking error or box constraints).
* Extend metrics, visualization tools, or simulation utilities.

Example: introducing moment-based robustness:

.. code-block:: python

   from qpfolio.core.models import build_dro_lite_problem
   problem = build_dro_lite_problem(mu_est, Sigma_est, r_target=0.1, gamma=0.2)

----

Documentation
-------------

Full documentation is available at:

📘 **`https://qpfolio.readthedocs.io/en/latest/ <https://qpfolio.readthedocs.io/en/latest/>`_**

Contents include:

* Mathematical formulations (MVO, MDP, DRO)
* Solver setup and interfaces
* Frontier generation and metrics
* API reference and extensibility guides

----

Project Information
-------------------

* **Repository:** https://github.com/hrolfrc/qpfolio
* **Issues:** https://github.com/hrolfrc/qpfolio/issues
* **License:** Apache License 2.0
* **Author:** Rolf Carlson

----

.. toctree::
   :maxdepth: 2
   :caption: Contents

   installation
   introduction
   philosophy_and_goals
   architecture
   methods
   usage
   applications/personal_and_direct_indexing
   personal_indexing
   visualization
   reporting
   api_reference
   api_personal_indexing
   contributing
   changelog
   about


