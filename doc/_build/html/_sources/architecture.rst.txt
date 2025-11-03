.. _architecture:

Architecture
============

Overview
--------

**QPfolio** follows a modular three-layer design that separates mathematical formulation, solver abstraction, and application logic.

The goal is to make portfolio optimization problems **composable**, **extensible**, and **transparent**.

Layered Design
--------------

.. image:: _static/qpfolio_architecture_layers.svg
   :align: center
   :alt: QPfolio three-layer architecture


**1. Core Optimization Engine**

- Classes: ``ProblemSpec``, ``MathOptOSQP``
- Responsibilities:
  - Express any quadratic optimization problem.
  - Interface consistently with different solvers (e.g., OSQP, CVXOPT, Gurobi).
  - Provide common data structures and diagnostics (objective, constraints, status).

**2. Portfolio Optimization Methods**

- Examples: Mean–Variance Optimization (MVO), Most Diversified Portfolio (MDP), Distributionally Robust Optimization (DRO).
- Responsibilities:
  - Define standard formulations using expected returns ``μ`` and covariance ``Σ``.
  - Convert theoretical problems into standardized QP form.
  - Support custom extensions (tracking error, factor tilts, robust risk).

**3. Applications**

- Examples: Personal Indexing, ESG-Tilted Portfolios, Tax-Aware Rebalancing.
- Responsibilities:
  - Combine portfolio optimization methods with domain-specific constraints.
  - Provide reproducible examples and workflows.
  - Integrate visualization and reporting layers.

Advantages of the Architecture
------------------------------

- **Composability:** Any convex optimization problem with quadratic structure can be represented.
- **Reusability:** Methods reuse the same solver interface; switching solvers requires no code changes.
- **Transparency:** Each layer exposes mathematical structure and solver diagnostics.
- **Extensibility:** New optimization variants (e.g., factor models, frontier generation) plug in without refactoring.

Relation to the Documentation
-----------------------------

- :ref:`methods` introduces the mathematical formulations that define portfolio optimization problems.
- :ref:`usage` demonstrates how to instantiate and solve those problems.
- :ref:`personal-indexing` and related pages show applied use cases built atop this architecture.
