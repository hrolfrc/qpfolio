Visualization
=============

Efficient Frontier (Real)
-------------------------

.. image:: _static/artifacts/v0/frontier.png
   :alt: Efficient Frontier
   :align: center
   :width: 720px

.. image:: _static/artifacts/v2/dro_frontier.png
   :alt: DRO frontier (Σ + γI)
   :width: 70%
   :align: center

.. image:: _static/artifacts/v2/mdp_point.png
   :alt: MDP point (closed-form)
   :width: 50%
   :align: center

Efficient Frontier + Capital Market Line
----------------------------------------

.. image:: _static/artifacts/v0/frontier.png
   :alt: Efficient Frontier (CML drawn by code sample)
   :align: center
   :width: 720px

Weights Along the Frontier (Real)
---------------------------------

.. image:: _static/artifacts/v0/weights.png
   :alt: Weights Along the Frontier
   :align: center
   :width: 720px

Risk Contributions (Real)
-------------------------

.. image:: _static/artifacts/v0/risk_contrib.png
   :alt: Risk Contributions (mid frontier)
   :align: center
   :width: 720px

How to generate these artifacts
-------------------------------

We generate these files with a real qpfolio run (OSQP-backed) via:

.. code-block:: bash

   make docs-artifacts

See ``scripts/generate_docs_artifacts.py`` for the exact steps and parameters.
