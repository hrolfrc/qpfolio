# QPFolio Roadmap — Version 0.1.0

## Vision
`qpfolio` provides a clean, open-source interface for solving **quadratic programming (QP)** portfolio optimization problems using **OR-Tools** (with the **OSQP** backend).  
It enables researchers and practitioners to model, solve, and visualize modern portfolio optimization problems such as **Markowitz Mean-Variance Optimization (MVO)**, **Most Diversified Portfolio (MDP)**, and **Distributionally Robust Optimization (DRO-lite)**.

---

## 0.1.0 Objectives
The **0.1.0 release** focuses on:
- A **stable QP formulation layer** for portfolio problems.
- **Solver independence** via an adapter interface.
- A complete **example pipeline** from simulated assets to efficient frontier visualization.
- **Mathematical clarity**, **numerical correctness**, and **reproducibility**.

---

## Milestones

### **Phase 1 — Core Infrastructure (Week 1–2)**
**Goal:** Establish minimal, functional project skeleton and CI setup.

- [ ] Initialize `qpfolio/` package with base layout:
```

qpfolio/
core/
data.py
models.py
solve.py
frontier.py
metrics.py
visualize.py
solvers/
base.py
mathopt_osqp.py
tests/

````
- [ ] Add `pyproject.toml` and minimal `README.md`.
- [ ] Configure pytest + coverage.
- [ ] Set up GitHub Actions (build, test, lint).
- [ ] Define versioning and changelog policy (semantic versioning).

**Deliverable:** Importable empty package with CI badge.

---

### **Phase 2 — Mathematical Core (Week 3–4)**
**Goal:** Implement and test QP problem formulations.

- [ ] Implement `ProblemSpec` and `Solution` dataclasses.
- [ ] Build a unified **QP intermediate representation (IR)**:
```python
Q, c, A_eq, b_eq, A_ineq, b_ineq, bounds
````

* [ ] Implement model builders:

  * [ ] `build_mvo_problem(mu, Sigma, R_target)`
  * [ ] `build_mdp_problem(sigma, Sigma)`
  * [ ] `build_dro_problem(mu, Sigma, gamma)`
* [ ] Add convexity and feasibility checks.
* [ ] Write basic unit tests using synthetic 2–3 asset cases.

**Deliverable:** All three problem formulations pass analytical correctness tests.

---

### **Phase 3 — Solver Layer (Week 5)**

**Goal:** Integrate OR-Tools + OSQP backend.

* [ ] Implement `Solver` abstract base class in `solvers/base.py`.
* [ ] Implement `MathOptOSQP` adapter:

  * Build model from IR.
  * Solve and extract primal weights, duals (if available).
* [ ] Implement fallback warning and clear error messages for solver unavailability.
* [ ] Add reproducible solver tests on synthetic data.

**Deliverable:** Solves MVO, MDP, and DRO-lite QPs with OR-Tools + OSQP.

---

### **Phase 4 — Efficient Frontier and Metrics (Week 6)**

**Goal:** Generate and visualize portfolio frontiers and risk metrics.

* [ ] Implement `compute_frontier()` using ε-constraint method.
* [ ] Implement `metrics.py`:

  * Expected return, variance, Sharpe, Sortino, diversification ratio.
* [ ] Implement `visualize.py`:

  * Frontier plot (risk-return curve).
  * Weight bar chart.
  * Risk contribution breakdown.
* [ ] Unit tests verifying monotonic variance and frontier smoothness.

**Deliverable:** Frontier visualization pipeline verified end-to-end.

---

### **Phase 5 — Simulation & Examples (Week 7)**

**Goal:** Provide reproducible examples and demos.

* [ ] Add stock simulation utilities in `data.py`:

  * Multivariate normal returns generator.
  * GBM path simulation.
* [ ] Example notebook: `examples/efficient_frontier.ipynb`

  * Simulate returns.
  * Estimate `mu` and `Sigma`.
  * Compute and plot efficient frontier.
  * Print top-3 portfolios by Sharpe ratio.
* [ ] Add CLI stub: `qpfolio solve --config examples/config.yaml` (optional).
* [ ] Add documentation examples to `README.md`.

**Deliverable:** End-to-end demonstration from data → optimization → visualization.

---

### **Phase 6 — Testing, Documentation, and Release (Week 8)**

**Goal:** Finalize testing, write documentation, and release to PyPI.

* [ ] Ensure ≥90% code coverage.
* [ ] Validate numeric stability (positive semidefinite Σ, feasible constraints).
* [ ] Finalize `README.md`, `ROADMAP.md`, and `CHANGELOG.md`.
* [ ] Add docstrings + inline mathematical references.
* [ ] Create PyPI distribution and verify install.
* [ ] Tag and release `v0.1.0`.

**Deliverable:** `qpfolio` published on PyPI with working examples.

---

## Future Versions

| Version    | Focus                                                    |
| ---------- | -------------------------------------------------------- |
| **0.2.0**  | Box, group, and sector constraints (still convex).       |
| **0.3.0**  | Tracking error and transaction cost extensions.          |
| **0.4.0**  | Risk parity (approximate QP) and ERC frontier.           |
| **0.5.0**  | MIQP extensions (cardinality constraints, integer lots). |
| **0.6.0+** | Multi-period, scenario-based, and Wasserstein DRO.       |

---

## Guiding Principles

* **Keep it convex:** All models must remain QP in v0.1.
* **Transparency over abstraction:** Mathematical definitions first, code second.
* **Solver modularity:** Swappable backend design from the start.
* **Reproducibility:** Deterministic seeds, clear examples, high test coverage.
* **Pedagogical clarity:** Each method demonstrable in ≤20 lines of Python.

---

## Expected Outcome

At the end of v0.1.0:

* Users can simulate assets, build covariance matrices, and compute efficient frontiers.
* Core optimization problems (MVO, MDP, DRO-lite) are solved with OR-Tools + OSQP.
* Results can be visualized and validated with built-in metrics and plots.
* Codebase is modular, testable, and ready for constraints and new methods in 0.2+.

---