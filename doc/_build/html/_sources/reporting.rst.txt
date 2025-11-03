Reporting
=========

Artifacts
---------
Save frontier results for audit/repro:

.. code-block:: python

   df = frontier_to_frame(points)
   save_frontier_csv(df, "reports/run1/frontier.csv")
   save_solution_json(points[0][2], "reports/run1/solution_0.json")

HTML Summary (optional)
-----------------------
.. code-block:: python

   # Save figures to reports/run1/*.png, then:
   render_report(df, {"frontier_png": "reports/run1/frontier.png",
                      "risk_png": "reports/run1/risk_contrib.png"},
                 out_html="reports/run1/index.html")
