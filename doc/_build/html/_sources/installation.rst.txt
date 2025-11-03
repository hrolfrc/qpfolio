Installation
============

This page explains how to install **QPFolio** for both regular users and developers.

----

Basic Installation
------------------

Ensure you have **Python 3.9 or later** and `pip` installed.
You can install QPFolio directly from PyPI:

.. code-block:: bash

   pip install qpfolio

Once installed, verify the installation:

.. code-block:: bash

   python -m pip show qpfolio

You should see version information similar to:

.. code-block:: text

   Name: qpfolio
   Version: 0.1.5
   Summary: Quadratic programming portfolio optimization library using OR-Tools and OSQP.

----

Development Installation
------------------------

If you plan to modify QPFolio or build the documentation, clone the repository:

.. code-block:: bash

   git clone https://github.com/hrolfrc/qpfolio.git
   cd qpfolio

Install with development and documentation extras:

.. code-block:: bash

   pip install -e ".[dev,docs]"

This will install testing tools (``pytest``, ``ruff``, ``mypy``) and Sphinx dependencies for local docs builds.

----

Testing the Installation
------------------------

After installation, run the test suite to confirm everything works:

.. code-block:: bash

   pytest -v

You should see all tests pass, including the ``test_frontier_mock_solver`` smoke test.

----

Building the Documentation
--------------------------

To build the documentation locally using Sphinx:

.. code-block:: bash

   cd docs
   make html

The generated site will appear under ``_build/html``.
Open ``_build/html/index.html`` in your browser to preview it.

----

Next Steps
----------

Proceed to the :doc:`usage` section to learn how to simulate assets, solve portfolios, and visualize the efficient frontier.
