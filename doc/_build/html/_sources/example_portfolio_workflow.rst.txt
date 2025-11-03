End-to-End Example: Portfolio Workflow
======================================

1) Generate Synthetic Data
--------------------------
.. code-block:: python

   import numpy as np
   from qpfolio.simulation.gbm import simulate_prices_and_returns

   prices, log_ret = simulate_prices_and_returns(
       mus=[0.08, 0.10, 0.12, 0.09, 0.11],
       sigmas=[0.20, 0.25, 0.22, 0.18, 0.28],
       T=1.0, steps_per_year=252, seed=123
   )
   mu = np.asarray(log_ret.mean() * 252)
   Sigma = np.asarray(log_ret.cov() * 252)

2) Compute a Frontier (MVO)
---------------------------
.. code-block:: python

   import numpy as np
   from qpfolio.core.frontier import compute_frontier
   from qpfolio.solvers.mathopt_osqp import MathOptOSQP

   targets = np.linspace(mu.min()*0.8, mu.max()*1.05, 12)
   solver = MathOptOSQP()
   points = compute_frontier(mu, Sigma, targets, solver=solver)

3) Visualize
------------
.. code-block:: python

   import matplotlib.pyplot as plt
   from qpfolio.core.visualize import plot_frontier_with_cml

   ax = plot_frontier_with_cml(points, rf=0.02)
   plt.show()

4) Inspect Weights & Risk Contributions
---------------------------------------
.. code-block:: python

   import pandas as pd
   from qpfolio.core.metrics import frontier_to_frame, risk_contributions

   df = frontier_to_frame(points, asset_labels=[f"A{i}" for i in range(len(mu))])
   mid = len(df) // 2
   w_mid = df.filter(like="w_").iloc[mid].to_numpy()
   rc_mid = risk_contributions(w_mid, Sigma)

   print(df.head())
   print(rc_mid)

Notes
-----
- Replace GBM with MVN returns if preferred.
- Swap MVO for MDP or DRO by constructing the corresponding problem builder.
