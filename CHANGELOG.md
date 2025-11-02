# QPFolio — Changelog

All notable changes to this project will be documented in this file.  
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),  
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]
### Added
- Initial repository skeleton (`qpfolio/` package structure).
- Continuous integration (pytest + coverage).
- Base documentation files (`README.md`, `ROADMAP.md`, `CHANGELOG.md`).
- Project configuration (`pyproject.toml`, build metadata).

### In Progress
- Implementation of `ProblemSpec` and `Solution` dataclasses.
- Construction of unified QP intermediate representation (`Q, c, A_eq, b_eq, A_ineq, b_ineq`).
- Basic unit tests for MVO/MDP problem generation.

---

## [0.1.0] — *Planned Release*
**Target:** First public PyPI release  
**Focus:** Functional prototype of QP portfolio optimization.

### Added
- **Core Formulations**
  - Markowitz Mean-Variance Optimization (MVO)
  - Most Diversified Portfolio (MDP)
  - Distributionally Robust Optimization (DRO-lite)

- **Solvers**
  - `MathOptOSQP` adapter using OR-Tools with OSQP backend.
  - Abstract solver interface for future CVXPY or Gurobi backends.

- **Mathematical Engine**
  - Quadratic Programming intermediate representation (QP-IR).
  - Convexity checks and error handling.

- **Frontier and Metrics**
  - Efficient frontier generation (ε-constraint method).
  - Risk/return metrics: expected return, variance, Sharpe ratio, diversification ratio.

- **Simulation Tools**
  - Synthetic data generators (multivariate normal, GBM).
  - Basic estimators for mean and covariance.

- **Visualization**
  - Efficient frontier plot.
  - Portfolio weights and risk contribution plots.

- **Documentation**
  - Getting Started guide with examples.
  - Example notebook: `examples/efficient_frontier.ipynb`.
  - Complete docstrings and math references for all classes.

- **Testing**
  - >90% unit test coverage on mathematical core.
  - Synthetic 2–3 asset test cases with analytical solutions.

- **Distribution**
  - Build and publish to PyPI as `qpfolio==0.1.0`.
  - Verified install from pip and functional examples.

---

## [0.2.0] — *Planned*
**Focus:** Extended constraints and flexibility.

### Planned Features
- Per-asset box bounds and group constraints.
- Sector and maximum exposure constraints.
- Tracking error minimization vs. benchmark portfolios.
- Enhanced visualization and frontier annotation.
- Extended test suite and user documentation.

---

## [0.3.0] — *Planned*
**Focus:** Transaction cost and risk-parity extensions.

### Planned Features
- Quadratic transaction cost penalties.
- Iterative risk parity and equal risk contribution methods.
- CLI interface (`qpfolio solve --config <file>`).
- Expanded example library.

---

## Versioning Policy
- Versions follow **Semantic Versioning**: `MAJOR.MINOR.PATCH`.
- Until `1.0.0`, minor version bumps may include breaking changes.
- Development pre-releases follow `0.x.y` or tags like `0.1.0a1`, `0.1.0rc1`.

---

## Release Procedure
1. Run full test suite (`pytest --maxfail=1 --disable-warnings -q`).
2. Update version number in `pyproject.toml` and `qpfolio/__init__.py`.
3. Update `CHANGELOG.md` and `ROADMAP.md` to reflect changes.
4. Build and verify package:  
   ```bash
   python -m build
   twine check dist/*
