Method Comparison
=================

Setup
-----
- Synthetic 5-asset universe (MVN or GBM-derived log returns).
- Annualized estimates :math:`(\hat{\mu}, \hat{\Sigma})`.
- Long-only, fully invested.

What We Compare
---------------
- Efficient frontiers (risk vs return).
- Weights along the frontier.
- Risk contributions at representative points.
- (Optional) Robustness sweep: vary :math:`\Gamma` in DRO.

Example Figures
---------------
.. image:: _static/artifacts/v1/mvo_frontier.png
   :alt: MVO Frontier
   :width: 75%

.. image:: _static/artifacts/v1/mdp_frontier.png
   :alt: MDP Frontier
   :width: 75%

.. image:: _static/artifacts/v1/dro_frontier.png
   :alt: DRO Frontier
   :width: 75%

Key Takeaways
-------------
- **MVO** achieves the best frontier under precise estimates but is brittle.
- **MDP** diversifies exposures—weights vary more smoothly with target return.
- **DRO** shifts the frontier downward but reduces sensitivity to estimation error.
