Visualization
=============

Efficient Frontier
------------------
.. code-block:: python

   points = compute_frontier(mu_est, Sigma_est, targets, solver)
   ax = plot_frontier([(r, m) for r,m,_ in points], show_tangent=True, rf=0.02)

Weights Along the Frontier
--------------------------
.. code-block:: python

   df = frontier_to_frame(points, asset_labels=[f"A{i}" for i in range(len(mu_est))])
   W = df[[c for c in df.columns if c.startswith("w_")]]
   plot_weights_along_frontier(W)
