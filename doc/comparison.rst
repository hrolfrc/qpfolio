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

.. image:: _static/artifacts/v2/comparison_frontiers.png
   :alt: MVO vs DRO frontiers and MDP point
   :width: 80%
   :align: center


.. image:: _static/artifacts/v2/comparison_frontiers.png
   :alt: MVO vs DRO frontiers with MDP point
   :width: 85%
   :align: center

.. image:: _static/artifacts/v2/dro_frontier.png
   :alt: DRO frontier (Σ + γ I)
   :width: 70%
   :align: center

.. image:: _static/artifacts/v2/mdp_point.png
   :alt: Most Diversified Portfolio (point)
   :width: 55%
   :align: center


Key Takeaways
-------------
- **MVO** achieves the best frontier under precise estimates but is brittle.
- **MDP** diversifies exposures—weights vary more smoothly with target return.
- **DRO** shifts the frontier downward but reduces sensitivity to estimation error.
