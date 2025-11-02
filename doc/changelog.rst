Changelog
=========

All notable changes to **QPFolio** are documented here.
This summary corresponds to the ``CHANGELOG.md`` file in the project root and follows
`Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_ and Semantic Versioning (2.0.0).

----

Unreleased
-----------

**In progress**

* Core QP data structures (:class:`qpfolio.core.types.ProblemSpec` and :class:`qpfolio.core.types.Solution`)
* Basic mean-variance, MDP, and DRO-lite model builders
* OR-Tools + OSQP solver adapter (stub implementation)
* Frontier generation and plotting
* Unit tests and documentation scaffolding
* Continuous integration with CircleCI and documentation builds on Read the Docs

----

Version 0.1.0 (Planned)
------------------------

**Target:** First public PyPI release

**Features**

* **Optimization Models**
  * Markowitz Mean-Variance Optimization (MVO)
  * Most Diversified Portfolio (MDP)
  * Distributionally Robust Optimization (DRO-lite)

* **Solver Integration**
  * MathOpt + OSQP backend
  * Abstract solver interface for future extensions (e.g., CVXPY)

* **Frontier and Metrics**
  * Efficient frontier computation (ε-constraint method)
  * Sharpe ratio, diversification ratio, and risk contributions

* **Simulation Tools**
  * Synthetic data generation via multivariate normal and GBM
  * Sample mean and covariance estimators

* **Visualization**
  * Frontier and portfolio weight plots via Matplotlib

* **Documentation & Testing**
  * Sphinx documentation hosted on Read the Docs
  * CircleCI for CI/CD
  * ≥ 90% test coverage on core modules

----

Version 0.2.0 (Planned)
------------------------

* Box, group, and sector constraints (still convex)
* Tracking-error minimization vs. benchmark portfolios
* Enhanced visualization and reporting tools

----

Version 0.3.0 (Planned)
------------------------

* Transaction cost and risk-parity extensions
* Command-line interface (``qpfolio solve --config <file>``)
* Expanded example notebooks

----

Versioning Policy
-----------------

QPFolio follows **Semantic Versioning (SemVer 2.0.0)**:

* **MAJOR** – Breaking changes or redesigns
* **MINOR** – Backward-compatible feature additions
* **PATCH** – Bug fixes or refinements

Until version 1.0.0, minor version bumps may still include interface changes.

----

Release Procedure
-----------------

1. Run full test suite (``pytest --maxfail=1 --disable-warnings -q``)
2. Update version numbers in ``pyproject.toml`` and ``qpfolio/__init__.py``
3. Update ``CHANGELOG.md`` and ``ROADMAP.md``
4. Build the package:

   .. code-block:: bash

      python -m build
      twine check dist/*

5. Upload to TestPyPI, verify, then publish:

   .. code-block:: bash

      twine upload --repository testpypi dist/*

6. Tag the release in Git:

   .. code-block:: bash

      git tag -a v0.1.0 -m "Release 0.1.0"
      git push origin v0.1.0
