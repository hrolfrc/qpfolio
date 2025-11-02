.. _bib-ami-testing-strategy:

For Developers: The Testing Strategy
====================================

Goal
----

The primary goal of this test plan is to verify that the ``bib-ami`` tool achieves its desired outcome: producing a **verified, configurable, auditable, and high-fidelity "golden" bibliography**. This plan ensures that every component and workflow is rigorously tested to meet the project’s core principles of data integrity and user-driven quality control.

Testing Philosophy: A Layered Approach
--------------------------------------

To ensure comprehensive coverage, we use a layered testing strategy. Each layer serves a distinct purpose, providing a safety net that catches different types of errors.

- **Unit Tests**: Fast, isolated tests to verify the internal logic of individual methods and small, focused "logic units."
- **Integration Tests**: Focused tests to verify that data objects and commands flow correctly between the distinct components as orchestrated by the ``BibTexManager``.
- **End-to-End (E2E) Tests**: Comprehensive tests that run the entire application via its command-line interface on realistic data to ensure the final output files are correct.

This layered approach allows for rapid feedback during development (from unit tests) while guaranteeing the robustness of the complete system (from E2E tests).

Test Environment and Helper Classes
-----------------------------------

A robust testing environment is crucial for efficiency. All test code resides in a dedicated ``tests/`` directory. This environment is supported by a set of specialized helper classes.

Helper Class Descriptions
~~~~~~~~~~~~~~~~~~~~~~~~~

**BibTexTestDirectory**
   :Location: ``tests/fixtures/directory_manager.py``
   :Purpose: To programmatically create and clean up temporary directory structures for our tests.

**Mock Clients (e.g., MockCrossRefClient)**
   :Location: ``tests/mocks/api_client.py``
   :Purpose: To simulate external API clients for fast, offline testing.
   :Responsibilities:
     - Implement the same public methods as the real client (e.g., ``get_doi_for_entry``).
     - **Crucially, must also simulate any underlying methods used by other components, such as the ``session.head()`` call for DOI resolution.**
     - Be configurable to return specific, predefined responses.

**RecordBuilder**
   :Location: ``tests/fixtures/record_builder.py``
   :Purpose: To act as a factory for creating structured test data (Python dictionaries representing BibTeX records).

Test Suite Breakdown
--------------------

Unit Tests
~~~~~~~~~~

:Goal: Verify the correctness of each "logic unit" in complete isolation. This is where we test our refactored helper methods.
:How it meets the desired outcome: Ensures the core algorithms for parsing, scoring, and configuration are correct by design, forming the foundation of a **trustworthy** system.

+-------------------------------------+---------------------------------------------------------------------------------------------------------------+
| **Unit to Test**                    | **Test Method Description**                                                                                   |
+=====================================+===============================================================================================================+
| ``CLIParser``                       | Using ``unittest.mock`` to simulate ``sys.argv``, test that the parser correctly handles the ``config``       |
|                                     | sub-command, the ``--split-by-quality`` flag, and the intelligent default for ``--suspect-file``.             |
+-------------------------------------+---------------------------------------------------------------------------------------------------------------+
| ``Validator._validate_entry``       | Test that the method correctly identifies books, calls the client for other types, and correctly invokes the  |
|                                     | DOI resolution check.                                                                                         |
+-------------------------------------+---------------------------------------------------------------------------------------------------------------+
| ``Refresher._refresh_single_entry`` | Test that the method correctly parses all fields (title, author, year, isbn) from a mock API response and     |
|                                     | only modifies the entry when data has changed.                                                                |
+-------------------------------------+---------------------------------------------------------------------------------------------------------------+

Integration Tests
~~~~~~~~~~~~~~~~~

:Goal: Verify that the "plumbing" between components inside the ``BibTexManager`` is solid and that data objects are passed and received correctly.
:How it meets the desired outcome: Guarantees the **auditability** of the workflow by confirming the integrity of the data as it flows through the pipeline.

+------------------------------------------+-------------------------------------------------------------------------------------------------------------+
| **Test Case**                            | **Actions**                                                                                                 |
+==========================================+=============================================================================================================+
| ``Validator`` → ``Refresher``            | Run the ``Validator`` on test data. Pass its output `BibDatabase` object directly to the ``Refresher`` and  |
|                                          | assert that the refresher correctly processes the ``verified_doi`` and ``audit_info`` fields.               |
+------------------------------------------+-------------------------------------------------------------------------------------------------------------+
| ``Refresher`` → ``Reconciler``           | Run the ``Validator`` and ``Refresher``. Pass the refreshed `BibDatabase` object to the ``Reconciler``      |
|                                          | and assert that it correctly uses the "original_title" from the audit trail for its fuzzy comparisons.      |
+------------------------------------------+-------------------------------------------------------------------------------------------------------------+
| ``Reconciler`` → ``Triage`` & ``Writer`` | Run the full pipeline up to reconciliation. Pass the reconciled `BibDatabase` to the ``Triage`` and         |
|                                          | ``Writer`` and assert that the final output files are created based on the quality scores and triage rules. |
+------------------------------------------+-------------------------------------------------------------------------------------------------------------+

End-to-End (E2E) Tests
~~~~~~~~~~~~~~~~~~~~~~

:Goal: Verify that the entire application works as a cohesive whole, invoked from the command line.
:How it meets the desired outcome: Demonstrates that all principles are upheld in a complete run, ensuring a **complete** and **auditable** final product that respects user configuration.

+----------------------------+-----------------------------------------------------------------------------------------------------------------+
| **Test Scenario**          | **Actions**                                                                                                     |
+============================+=================================================================================================================+
| Configuration Scenario     | Use the ``bib-ami config set`` command to define a custom quality threshold. Run the main workflow and          |
|                            | assert that the final output files correctly reflect the rule set in the configuration.                         |
+----------------------------+-----------------------------------------------------------------------------------------------------------------+
| Output Splitting Scenario  | Run the workflow with the ``--split-by-quality`` flag. Assert that separate output files (e.g.,                 |
|                            | ``final.verified.bib``, ``final.accepted.bib``) are created with the correct entries in each.                   |
+----------------------------+-----------------------------------------------------------------------------------------------------------------+