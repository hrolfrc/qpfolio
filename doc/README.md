# QPFolio Documentation

This directory contains the **Sphinx** source files for the [QPFolio](https://github.com/hrolfrc/qpfolio) documentation,
which is automatically built and published on **[Read the Docs](https://qpfolio.readthedocs.io/en/latest/)**.

---

## 🧭 Overview

QPFolio’s documentation is designed to serve three purposes:

1. **User Guide:**  
   Explain how to install, configure, and use QPFolio for quadratic portfolio optimization.

2. **Developer Reference:**  
   Provide API documentation for core modules, solvers, and helper utilities.

3. **Project Transparency:**  
   Include governance, changelog, and contribution details consistent with the repository’s policies.

The documentation is written in **reStructuredText (.rst)** and built using **Sphinx** with the **Furo** theme.

---

## 🧰 Prerequisites

Before building the docs locally, ensure you have the development dependencies installed:

```bash
pip install -e ".[docs]"
