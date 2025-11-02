API Reference
=============

This section provides an overview of the main public modules and classes in **QPFolio**.

The API is organized into three layers:

1. **Core Modules** — Problem generation, metrics, and visualization.
2. **Solvers** — Abstractions and adapters for different backends.
3. **Data Utilities** — Simulation and estimation helpers.

----

Core Modules
------------

.. automodule:: qpfolio.core.data
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: qpfolio.core.estimates
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: qpfolio.core.models
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: qpfolio.core.frontier
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: qpfolio.core.metrics
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: qpfolio.core.visualize
   :members:
   :undoc-members:
   :show-inheritance:

----

Solver Interfaces
-----------------

.. automodule:: qpfolio.solvers.base
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: qpfolio.solvers.mathopt_osqp
   :members:
   :undoc-members:
   :show-inheritance:

----

Data Types
----------

.. automodule:: qpfolio.core.types
   :members:
   :undoc-members:
   :show-inheritance:

----

Developer Notes
---------------

* All modules use **type hints** and are **mypy**-compatible.
* Each optimization model returns a :class:`qpfolio.core.types.ProblemSpec` object.
* Solver adapters return a :class:`qpfolio.core.types.Solution` object with fields:
  ``x`` (weights), ``obj_value`` (objective value), ``status``, and ``info``.
