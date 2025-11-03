.. _personal-indexing:

Personal Indexing (Tracking Error, ESG, and Tax-Aware)
======================================================

Overview
--------

This section demonstrates three common use cases:

1. Basic tracking-error minimization with long-only and per-asset caps.
2. ESG-style tilting via linear exposure penalties.
3. Tax/turnover-aware optimization via L2 penalty toward a previous portfolio.

Requirements
------------

* ``numpy``
* ``osqp`` (QP solver)
* ``scipy``

Basic Tracking Error
--------------------

We construct a small PSD covariance, a uniform benchmark, and solve:

.. doctest::

   >>> import numpy as np
   >>> from qpfolio.personal_indexing import personal_index_optimizer
   >>> np.random.seed(1)
   >>> n = 5
   >>> R = np.random.randn(n, n)
   >>> Sigma = 0.08 * np.eye(n) + 0.01 * (R + R.T) / 2.0
   >>> w_bench = np.ones(n) / n
   >>> sol = personal_index_optimizer(Sigma, w_bench, max_weight=0.5)
   >>> sol.status in ("solved", "optimal")
   True
   >>> abs(sol.x.sum() - 1.0) < 5e-6
   True
   >>> (sol.x >= -1e-12).all()
   True
   >>> (sol.x <= 0.5 + 1e-12).all()
   True

ESG Penalty Example
-------------------

We tag asset 0 with an exposure row and penalize deviations from a near-zero target.

.. doctest::

   >>> from qpfolio.personal_indexing import personal_index_optimizer_esg
   >>> np.random.seed(2)
   >>> n = 8
   >>> R = np.random.randn(n, n)
   >>> Sigma = 0.08 * np.eye(n) + 0.01 * (R + R.T) / 2.0
   >>> w_bench = np.ones(n) / n
   >>> base = personal_index_optimizer(Sigma, w_bench, max_weight=0.5)
   >>> exposures = np.zeros((1, n)); exposures[0, 0] = 1.0
   >>> targets = np.zeros(1); penalties = np.array([10.0])
   >>> esg = personal_index_optimizer_esg(Sigma, w_bench, exposures, targets, penalties, max_weight=0.5)
   >>> # Asset 0 weight should drop relative to baseline:
   >>> esg.x[0] <= base.x[0] + 1e-9
   True

Tax/Turnover-Aware Example
--------------------------

We penalize distance from the previous portfolio ``w_prev`` to reduce turnover.

.. doctest::

   >>> from qpfolio.personal_indexing import personal_index_optimizer_taxaware
   >>> np.random.seed(3)
   >>> n = 7
   >>> R = np.random.randn(n, n)
   >>> Sigma = 0.08 * np.eye(n) + 0.01 * (R + R.T) / 2.0
   >>> w_bench = np.ones(n) / n
   >>> w_prev = np.zeros(n); w_prev[2] = 1.0
   >>> tax_weights = np.linspace(1.0, 2.0, n)
   >>> base = personal_index_optimizer(Sigma, w_bench, max_weight=0.7)
   >>> tax = personal_index_optimizer_taxaware(Sigma, w_bench, w_prev=w_prev, tax_weights=tax_weights, turnover_penalty=10.0, max_weight=0.7)
   >>> # Tax-aware should be closer to w_prev than baseline is:
   >>> import numpy as np
   >>> np.linalg.norm(tax.x - w_prev) <= np.linalg.norm(base.x - w_prev) + 1e-9
   True

Run the Example Scripts
-----------------------

You can also run the example scripts directly:

.. code-block:: bash

   python examples/personal_indexing_basic.py
   python examples/personal_indexing_esg.py
   python examples/personal_indexing_taxaware.py
