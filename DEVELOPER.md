## 📄 `DEVELOPER.md`

````markdown
# Developer Quickstart

Welcome to the **QPFolio** developer guide.  
This document provides the essential steps for setting up your environment, running tests, building docs, and preparing a release.

---

## 🧱 1. Environment Setup

Clone the repository and install dependencies in editable mode:

```bash
git clone https://github.com/hrolfrc/qpfolio.git
cd qpfolio
pip install -e ".[dev,docs]"
````

This installs:

* Core dependencies (`numpy`, `ortools`, `osqp`, etc.)
* Development tools (`pytest`, `ruff`, `mypy`)
* Documentation tools (`sphinx`, `furo`)

---

## 🧪 2. Running Tests

Use **pytest** to run the full test suite:

```bash
pytest -v
```

Run with coverage reporting:

```bash
pytest --cov=qpfolio --cov-report=term-missing
```

To lint and type-check before committing:

```bash
ruff check .
mypy qpfolio
```

---

## 📖 3. Building the Documentation

Build the HTML docs locally with Sphinx:

```bash
cd docs
make html
```

Open the generated site in your browser:

```
docs/_build/html/index.html
```

Documentation is also built automatically on **Read the Docs**:

🔗 [https://qpfolio.readthedocs.io/en/latest/](https://qpfolio.readthedocs.io/en/latest/)

---

## 🧰 4. CircleCI Integration

Continuous Integration (CI) is configured in `.circleci/config.yml`.
Each commit triggers:

* Dependency installation
* Linting (Ruff, MyPy)
* Unit testing (Pytest + Coverage)
* Package build verification

You can replicate the same checks locally by running:

```bash
python -m build
pytest -v
```

---

## 🚀 5. Preparing a Release

Follow these steps for version bumps and PyPI publication:

1. Update version strings in:

   * `qpfolio/__init__.py`
   * `pyproject.toml`

2. Update `CHANGELOG.md` and verify documentation.

3. Build and validate the package:

   ```bash
   python -m build
   twine check dist/*
   ```

4. Test upload to **TestPyPI**:

   ```bash
   twine upload --repository testpypi dist/*
   ```

5. Verify installation from TestPyPI:

   ```bash
   pip install --index-url https://test.pypi.org/simple qpfolio
   ```

6. Once confirmed, publish to **PyPI**:

   ```bash
   twine upload dist/*
   ```

7. Tag and push the release:

   ```bash
   git tag -a v0.1.0 -m "Release 0.1.0"
   git push origin v0.1.0
   ```

---

## 🧩 6. Repository Layout

```
qpfolio/
├── core/                # Core modeling, solving, and metrics
├── solvers/             # Solver abstractions and OR-Tools/OSQP adapters
├── tests/               # Unit tests
├── docs/                # Sphinx documentation
├── .circleci/           # CI configuration
├── ROADMAP.md           # Development plan
├── CHANGELOG.md         # Version history
├── CONTRIBUTING.md      # Contribution guidelines
└── DEVELOPER.md         # This file
```

---

## 🧭 7. Key Links

* **Repository:** [github.com/hrolfrc/qpfolio](https://github.com/hrolfrc/qpfolio)
* **Documentation:** [qpfolio.readthedocs.io](https://qpfolio.readthedocs.io/en/latest/)
* **License:** Apache 2.0 (`LICENSE`)
* **Maintainer:** Rolf Carlson

---

## 💡 Developer Philosophy

> *Readable code. Reliable math. Reproducible results.*

Every contribution should uphold these three principles.

```