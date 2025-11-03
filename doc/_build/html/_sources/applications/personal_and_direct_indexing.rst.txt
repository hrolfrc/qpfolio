Personal Indexing and Direct Indexing
=====================================

Overview
--------
**Personal indexing** and **direct indexing** represent the convergence of
quantitative finance and personalized wealth management.
They allow investors—particularly those working through
**Registered Investment Advisors (RIAs)**—to obtain index-like exposure while
expressing individual preferences, values, and tax considerations.

qpfolio provides the quantitative foundation for these strategies through
**convex quadratic optimization (QP)**.  By modeling personalization and
constraints mathematically, qpfolio allows users to design and test
customized portfolios with clarity and reproducibility.

Definitions
-----------
**RIA (Registered Investment Advisor)**
    A fiduciary professional or firm that provides investment advice and is
    registered with the SEC or state regulators.  RIAs typically construct
    portfolios tailored to individual clients’ goals, risk tolerance, and
    constraints.

**SMA (Separately Managed Account)**
    A portfolio of individual securities managed for a single investor.  Unlike
    a mutual fund or ETF, the investor owns each position directly, enabling
    customization and tax management.

**ESG (Environmental, Social, and Governance)**
    A framework for evaluating companies based on sustainability and ethical
    criteria.  ESG-based investing might, for example, underweight companies
    with high carbon emissions or overweight firms with strong governance
    practices.

**QP (Quadratic Program)**
    An optimization problem where the objective function is quadratic and the
    constraints are linear.  qpfolio solves these efficiently using
    `MathOptOSQP`.

Two Complementary Perspectives
------------------------------

Personal Indexing (qpfolio framing)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Personal indexing treats the investor’s portfolio as a **mathematical
optimization problem**:

    Construct a portfolio that tracks a reference benchmark or risk structure,
    while satisfying investor-specific constraints.

This framing emphasizes the analytical and quantitative layer: the RIA defines
objectives (e.g., tracking error, volatility, sector exposures, turnover),
and qpfolio solves for the optimal portfolio weights :math:`w^*`.

Advantages:

- Solver-based precision rather than heuristic filtering.
- Full transparency and auditability.
- Continuous control over deviation from benchmarks.
- Quantifiable trade-offs between return, risk, and personalization.

Direct Indexing (industry framing)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Direct indexing, as defined by **S&P Global** and **BlackRock**, refers to
replicating an index (such as the S&P 500®) **through direct ownership of the
underlying securities**—typically inside an SMA.

It combines the passive efficiency of index investing with:

- **Customization**: adjust sector or factor exposures.
- **Tax efficiency**: harvest losses to offset gains.
- **Transparency**: clients see and own their individual holdings.

Whereas personal indexing is model-centric, direct indexing is
**operations-centric**, involving brokerage infrastructure and tax engines.
Nonetheless, both are rooted in the same **mathematical foundation**—minimizing
tracking error subject to investor constraints.

Similarities and Differences
----------------------------

+---------------------------+--------------------------------------------+-----------------------------------------------+
| Aspect                    | **Personal Indexing** (qpfolio)            | **Direct Indexing** (Industry)                |
+===========================+============================================+===============================================+
| **Objective**             | Optimize a benchmark-tracking portfolio    | Replicate an index with tax and customization |
|                           | under quantitative constraints.            | features in an SMA.                           |
+---------------------------+--------------------------------------------+-----------------------------------------------+
| **Implementation**        | Mathematical model (QP solver).            | Brokerage platform with overlay software.     |
+---------------------------+--------------------------------------------+-----------------------------------------------+
| **Control Variables**     | Weights :math:`w`                          | Trades and realized gains/losses.             |
+---------------------------+--------------------------------------------+-----------------------------------------------+
| **Customization**         | Arbitrary constraints (ESG, sector caps,   | Platform-defined tilts and exclusions.        |
|                           | turnover, factor exposure).                |                                               |
+---------------------------+--------------------------------------------+-----------------------------------------------+
| **Primary Benefit**       | Quantitative flexibility and transparency. | Tax efficiency and operational integration.   |
+---------------------------+--------------------------------------------+-----------------------------------------------+
| **Primary Limitation**    | Requires modeling and estimation.          | Limited control over optimization layer.      |
+---------------------------+--------------------------------------------+-----------------------------------------------+

Canonical Optimization Problems
-------------------------------

1. Tracking Error Minimization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Minimize the variance of deviations from a benchmark portfolio
:math:`w_b`:

.. math::

    \min_w \frac{1}{2}(w - w_b)^\top \Sigma (w - w_b)
    \quad \text{s.t.} \quad
    w^\top \mathbf{1} = 1,\;
    0 \le w_i \le w_{\max}

where :math:`\Sigma` is the covariance matrix of returns.

**Use Case:**
Track the S&P 500 with 100 securities and a 5 % cap per asset.

2. Personalized Tracking (ESG or Sector Tilts)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. math::

    \begin{aligned}
    \min_w \quad & \frac{1}{2}(w - w_b)^\top \Sigma (w - w_b) \\
    \text{s.t.} \quad &
    w^\top \mathbf{1} = 1, \\
    & w^\top e_{\text{energy}} \le 0.05, \;
      w^\top e_{\text{tech}} \ge 0.20, \\
    & w \ge 0.
    \end{aligned}

**Use Case:**
Underweight fossil fuels, overweight technology, maintain overall index-like
risk.

3. Tax-Aware Direct Indexing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Include turnover or tax penalties:

.. math::

    \min_w \frac{1}{2}(w - w_b)^\top \Sigma (w - w_b)
    + \lambda \sum_i \tau_i |w_i - w_i^{\text{prev}}|

where:

- :math:`\tau_i` = estimated tax cost for asset *i*
- :math:`w_i^{\text{prev}}` = previous holdings
- :math:`\lambda` = trade-off parameter between tax cost and tracking error.

**Use Case:**
Rebalance while deferring gains; harvest losses opportunistically.

How qpfolio Supports These Problems
-----------------------------------

+--------------------------------------+------------------------------------------+
| **Component**                        | **Role**                                 |
+======================================+==========================================+
| ``simulate_mvn_returns()``           | Generate synthetic or scenario data.     |
+--------------------------------------+------------------------------------------+
| ``sample_mean_cov()``                | Estimate mean returns and covariances.   |
+--------------------------------------+------------------------------------------+
| ``ProblemSpec``                      | Define the QP (Q, c, A, b, bounds).      |
+--------------------------------------+------------------------------------------+
| ``MathOptOSQP``                      | Solve the optimization efficiently.      |
+--------------------------------------+------------------------------------------+
| ``frontier_to_frame()``              | Export results for visualization.        |
+--------------------------------------+------------------------------------------+
| ``plot_risk_contributions()``        | Decompose portfolio risk exposure.       |
+--------------------------------------+------------------------------------------+
| ``plot_corr_heatmap()``              | Visualize diversification and structure. |
+--------------------------------------+------------------------------------------+

Example Scenarios
-----------------

**A. Index Tracking with Fewer Stocks**

.. code-block:: python

    from qpfolio.personal_indexing import personal_index_optimizer
    from qpfolio.core.data import simulate_mvn_returns
    from qpfolio.core.estimates import sample_mean_cov
    import numpy as np

    R = simulate_mvn_returns(n_assets=100, n_obs=250)
    mu, Sigma = sample_mean_cov(R)
    w_bench = np.ones(100) / 100

    selected = np.random.choice(range(100), size=25, replace=False)
    Sigma_sub = Sigma[np.ix_(selected, selected)]
    w_bench_sub = w_bench[selected]

    sol = personal_index_optimizer(Sigma_sub, w_bench_sub, max_weight=0.05)

**B. ESG Tilted Portfolio**

.. code-block:: python

    excluded = [1, 5, 7, 9, 13]
    sol = personal_index_optimizer(Sigma, w_bench, exclude=excluded)

**C. Tax-Aware Rebalancing**

.. code-block:: python

    from qpfolio.personal_indexing import personal_index_optimizer_taxaware
    sol = personal_index_optimizer_taxaware(Sigma, w_bench,
                                            w_prev=w_prev, tax_rates=τ)

Discussion and Outlook
----------------------

Personal indexing provides a **research-grade, model-driven** way to construct
customized portfolios.
Direct indexing implements these principles operationally within SMAs for
real-world deployment.

qpfolio bridges these worlds by giving RIAs and quantitative researchers a
common platform to:

- Prototype personalized index strategies.
- Quantify the cost of constraints (tracking-error budget).
- Visualize diversification and tax effects.
- Ensure numerical transparency and reproducibility.

Future extensions include:
- Multi-period optimization with dynamic rebalancing.
- Factor attribution and risk decomposition.
- Integration with transaction-cost and liquidity models.
