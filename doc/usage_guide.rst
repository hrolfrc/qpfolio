Usage & Configuration
=====================

This section serves as a reference guide for users who want to customize
the behavior of ``bib-ami``. It provides a detailed description of all
available command-line arguments and explains how to use a configuration
file for persistent settings.

Command-Line Reference
----------------------

The ``bib-ami`` tool has two primary functions: running the bibliography
workflow and managing your default settings.

Running the Workflow
~~~~~~~~~~~~~~~~~~~~

This is the default command. It processes your ``.bib`` files according to
the options you provide.

.. code:: bash

   bib-ami --input-dir <path> --output-file <path> --email <address> [options]

**Workflow Arguments:**

``--input-dir <path>``
   |
   | **(Required)** Specifies the path to the directory containing the
     source ``.bib`` files that you want to process.

``--output-file <path>``
   |
   | **(Required)** Specifies the full path, including the filename, for
     the main bibliography output file. For example:
     ``output/final_library.bib``.

``--suspect-file <path>``
   |
   | (Optional) Specifies the path for the file containing suspect
     entries. If not provided, it defaults to a name based on the main
     output file (e.g., if output is ``final.bib``, this will be
     ``final.suspect.bib``).

``--split-by-quality``
   |
   | (Optional) A flag that alters the output behavior. Instead of
     creating just two files (final and suspect), it will create a
     separate ``.bib`` file for each quality level encountered (e.g.,
     ``final.verified.bib``, ``final.confirmed.bib``).

``--merge-only``
   |
   | (Optional) A flag that instructs the tool to only merge all source
     ``.bib`` files into the specified output file, without performing
     any validation or enrichment.

``--email <address>``
   |
   | Your email address, required for querying the CrossRef API under
     their "Polite Pool" policy. This argument overrides any email set
     in a configuration file.

Managing Configuration
~~~~~~~~~~~~~~~~~~~~~~

The ``config`` sub-command allows you to view and set your default
settings without having to manually edit the JSON configuration file.

.. code:: bash

   bib-ami config [action]

**Config Actions:**

``set <key> <value>``
   |
   | Sets a default value in your user-level configuration file.
   |
   | *Example:* ``bib-ami config set email "my.name@university.edu"``
   | *Example:* ``bib-ami config set triage_rules.min_quality_for_final_bib "Confirmed"``

``get <key>``
   |
   | Displays the current value of a specific setting.
   |
   | *Example:* ``bib-ami config get email``

``list``
   |
   | Displays all settings currently in your user-level configuration file.
   |
   | *Example:* ``bib-ami config list``


Configuration File
------------------

For settings you use frequently, you can create a configuration file.
``bib-ami`` will automatically look for and load settings from these files.

**File Locations and Precedence:**

The tool searches for ``bib_ami_config.json`` in the following order, with
settings from later locations overriding earlier ones:

1.  **User-Default Location:** In your user config directory (e.g.,
    ``~/.config/bib-ami/config.json`` on Linux). This is where the
    ``config set`` command writes to and is the best place for your
    personal defaults.
2.  **Project-Specific Location:** In the directory where you are running
    the ``bib-ami`` command. This is useful for project-specific overrides.
3.  **Command-Line Arguments:** An argument provided directly on the command
    line (e.g., ``--email``) will **always** have the final say,
    overriding all configuration files.

**Example ``bib_ami_config.json``:**

.. code:: json

   {
     "email": "your.name@university.edu",
     "fuzzy_threshold": 95,
     "triage_rules": {
       "min_quality_for_final_bib": "Verified"
     }
   }

**Available Quality Levels for Triage:**

* ``Verified`` (Highest)
* ``Confirmed``
* ``Accepted``
* ``Reconciled``
* ``Suspect`` (Lowest)