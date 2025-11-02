.. _getting_started:

Getting Started
===============

This guide is designed to get you up and running with **bib-ami** in under five minutes. It covers installation and a simple first run to demonstrate the tool's core functionality.

For a complete reference of all commands and options, please see the :doc:`usage_guide` guide.

Installation
------------

**bib-ami** is distributed via the Python Package Index (PyPI) and can be installed easily using ``pip``. Ensure you have Python 3.7 or higher installed.

.. code:: bash

   pip install bib-ami

This command will install ``bib-ami`` and all necessary dependencies.

A Quick Start Example
---------------------

The fastest way to see **bib-ami** in action is to run it on a directory of your existing ``.bib`` files. This single command will merge all found files, validate them against external APIs, and triage them based on their quality.

**Step 1: Prepare Your Input**

Place all the source ``.bib`` files you want to process into a single directory (e.g., ``my_papers/``).

**Step 2: Run the Command**

Run the following command from your terminal. You must provide your email address for responsible use of the CrossRef API’s "Polite Pool."

.. code:: bash

   bib-ami --input-dir my_papers/ --output-file final_library.bib --email "your.name@university.edu"

**Step 3: Review the Output**

After the process completes, ``bib-ami`` will have created two files:

* ``final_library.bib``
  This file contains the high-quality, "Verified" and "Accepted" entries that meet the default quality standards.

* ``final_library.suspect.bib``
  This file contains all entries that could not be verified and require manual review. The tool creates this file automatically using the name of your output file as a base.

A summary of the actions taken (e.g., duplicates removed, DOIs added) will also be printed to your console.

Next Step: Set Your Defaults
----------------------------

To avoid typing your email address every time, you can set it as a global default using the new ``config`` command. This is the recommended next step for any regular user.

.. code:: bash

   bib-ami config set email "your.name@university.edu"

This command saves your email in a user-level configuration file. Now you can run ``bib-ami`` without the ``--email`` flag. To learn more about configuration, see the :doc:`usage_guide` page.