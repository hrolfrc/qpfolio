Usage
=====

This section walks through the basic workflow for using **QPFolio** to simulate asset data,
build quadratic optimization problems, and visualize results.

----

Quick Start
-----------

Here’s a minimal example showing how to construct and solve an efficient frontier:

.. code-block:: python

   import numpy as np
   from qpfolio.core.data import simulate_mvn_returns
   from qpfolio.core.estimates import sample_mean_cov
   from qpfolio.core.frontier import compute_frontier
   from qpfolio.solvers.mathopt_osqp import MathOptOSQP
   from qpfolio.core.visualize import plot_frontier

   # Simulate 10 assets over 252 trading days
   R, mu, Sigma = simulate_mvn_returns(n_assets=10, n_periods=252)
   mu_est, Sigma_est = sample_mean_cov(R)

   # Define target returns and solver
   targets = np.linspace(0.05, 0.15, 10)
   solver = MathOptOSQP()

   # Compute efficient frontier
   results = compute_frontier(mu_est, Sigma_est, targets, solver)

   # Plot the frontier
   plot_frontier([(risk, ret) for risk, ret, _ in results])

This will display a risk-return curve showing the efficient frontier.

----

Interpreting Results
--------------------

Each portfolio point along the frontier provides:

* **Risk (σ):** Portfolio standard deviation (volatility).
* **Return (μ):** Expected portfolio return.
* **Weights (w):** Optimal asset weights that minimize variance for the given target return.

You can access these values directly from the ``results`` list:

.. code-block:: python

   for risk, ret, sol in results:
       print(f"Target: {ret:.3f}  Risk: {risk:.3f}  Status: {sol.status}")

----

Alternative Models
------------------

You can build and solve other problem types provided by QPFolio:

* **Mean-Variance Optimization (MVO):**

  .. code-block:: python

     from qpfolio.core.models import build_mvo_problem

     problem = build_mvo_problem(mu_est, Sigma_est, r_target=0.1)
     solution = solver.solve(problem)

* **Most Diversified Portfolio (MDP):**

  .. code-block:: python

     from qpfolio.core.models import build_mdp_problem

     sigmas = np.sqrt(np.diag(Sigma_est))
     problem = build_mdp_problem(sigmas, Sigma_est)
     solution = solver.solve(problem)

* **Distributionally Robust Optimization (DRO-lite):**

  .. code-block:: python

     from qpfolio.core.models import build_dro_lite_problem

     problem = build_dro_lite_problem(mu_est, Sigma_est, r_target=0.1, gamma=0.2)
     solution = solver.solve(problem)

----

Visualization Options
---------------------

QPFolio includes built-in visualization tools to help interpret portfolio results:

* **Efficient Frontier:**

  .. code-block:: python

     from qpfolio.core.visualize import plot_frontier
     plot_frontier([(risk, ret) for risk, ret, _ in results])

* **Risk Metrics:**

  .. code-block:: python

     from qpfolio.core.metrics import sharpe, diversification_ratio

     w = results[0][2].x
     print("Sharpe:", sharpe(w, mu_est, Sigma_est))
     print("Diversification Ratio:", diversification_ratio(w, np.sqrt(np.diag(Sigma_est)), Sigma_est))

----

Next Steps
----------

Explore the :doc:`api_reference` for detailed class and function documentation.
