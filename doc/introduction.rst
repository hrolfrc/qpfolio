Introduction to Quadratic Portfolio Optimization
================================================

Why Quadratic?
--------------
Variance is quadratic in portfolio weights: :math:`\sigma_p^2 = w^\top \Sigma w`.
This makes problems like mean–variance optimization convex and efficiently solvable with QP solvers (e.g., OSQP).

Core Concepts (Glossary)
------------------------
**Return (Expected)** (:math:`\mu`):
  Average expected return per asset (annualized here).

**Covariance Matrix** (:math:`\Sigma`):
  Second-moment structure of returns. Diagonals are variances, off-diagonals encode co-movements.

**Volatility** (:math:`\sigma`):
  Standard deviation of returns. For asset :math:`i`, :math:`\sigma_i = \sqrt{\Sigma_{ii}}`.

**Correlation**:
  Normalized covariance in :math:`[-1, 1]`. High correlation reduces diversification benefits.

**Efficient Frontier**:
  The set of portfolios with minimum variance for a given expected return.

**Capital Market Line (CML)**:
  Line from the risk-free rate tangent to the efficient frontier. The tangency portfolio maximizes Sharpe ratio.

**Sharpe Ratio**:
  :math:`(\mu_p - R_f) / \sigma_p`. Return per unit of risk.

**Risk Contribution (RC)**:
  Asset :math:`i`'s contribution to total risk: :math:`\mathrm{RC}_i = \frac{w_i (\Sigma w)_i}{\sigma_p}`.

**Most Diversified Portfolio (MDP)**:
  Portfolio that maximizes the diversification ratio. Closed-form (ignoring long-only constraints): :math:`w \propto \Sigma^{-1}\sigma`.

**DRO (Distributionally Robust Optimization)**:
  Robustification technique that guards against estimation/model error. A simple convex surrogate is :math:`\Sigma' = \Sigma + \Gamma` with :math:`\Gamma \succeq 0`.

How to Read the Plots
---------------------
**Efficient Frontier**:
  Points on the curve are optimal risk–return trade-offs. The leftmost point is minimum-variance.

**CML + Tangency Point**:
  The CML dominates portfolios below it; the tangent is the max-Sharpe risky portfolio.

**Weights Along Frontier**:
  Stacked areas show how allocations evolve as target return (and risk) rises.

**Risk Contributions**:
  Bars reveal which assets dominate total portfolio risk. Balanced contributions indicate better diversification.

**Correlation Heatmap**:
  Visualizes dependencies. Lower correlations (cool colors) improve diversification.

Where to Next
-------------
- :doc:`methods`
- :doc:`data_generation`
- :doc:`visualization`
- :doc:`comparison`
- :doc:`example_portfolio_workflow`
