About QPFolio
=============

**QPFolio** is an open-source Python library for quadratic programming–based portfolio optimization.
It is designed to provide a rigorous, extensible foundation for modeling, solving, and visualizing convex
portfolio allocation problems using efficient solvers such as OR-Tools and OSQP.

This page summarizes the project's governance model, maintainers, and licensing information.

----

Project Governance
------------------

QPFolio is currently maintained under a **single-maintainer model** to ensure architectural coherence and reproducibility
during early development (``v0.1.x``). The governance approach emphasizes transparency, documentation, and stability over speed.

Governance principles:

* **Clarity before complexity:** prefer simple, well-tested features over premature generalization.
* **Reproducibility:** every release must build, test, and document successfully.
* **Transparency:** key design decisions are recorded in the repository (see ``GOVERNANCE.md``).

As the project matures toward ``v1.0.0``, QPFolio intends to evolve into a
**core maintainer + contributor** model with formal review processes and documented governance procedures.

For details, refer to:

* :file:`../GOVERNANCE.md`
* :file:`../MAINTAINERS.md`

----

Maintainer
----------

The current project maintainer is:

**Rolf Carlson**
*Founder and Lead Developer*

Responsibilities include project architecture, optimization modeling, documentation, and release management.

For direct inquiries, please use the contact information listed in ``pyproject.toml`` or the GitHub repository profile:

* **Repository:** https://github.com/hrolfrc/qpfolio
* **Issues:** https://github.com/hrolfrc/qpfolio/issues

----

Licensing
---------

QPFolio is released under the **Apache License 2.0**, a permissive and business-friendly open-source license.

Key points:

* You may freely use, modify, and distribute the code.
* Attribution to the original author is required.
* The license includes a patent grant for contributors.
* The software is provided *“as is”*, without warranty of any kind.

Full license text: :file:`../LICENSE`

----

Acknowledgments
---------------

QPFolio builds upon several robust open-source ecosystems, including:

* **[OR-Tools](https://developers.google.com/optimization)** — optimization modeling framework by Google.
* **[OSQP](https://osqp.org)** — open-source quadratic programming solver.
* **NumPy**, **Pandas**, **Matplotlib**, and **SciPy** for numerical and visualization foundations.

The project acknowledges and thanks the developers of these tools for their contributions to the open-source community.

----

Citation
--------

If you use QPFolio in research or publications, please cite the software appropriately:

.. code-block:: bibtex

   @software{qpfolio,
     author = {Carlson, Rolf},
     title = {QPFolio: Quadratic Programming Portfolio Optimizer},
     year = {2025},
     url = {https://github.com/hrolfrc/qpfolio},
     note = {Version 0.1.0}
   }

----

Summary
-------

QPFolio aims to bridge modern convex optimization and practical portfolio management.
By combining mathematical rigor with clean software engineering,
it provides a reliable foundation for simulation, analysis, and real-world application
of quadratic programming in finance.

