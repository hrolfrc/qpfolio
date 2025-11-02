# bib-ami: Future Development Plan

With the core architecture implemented and tested, the project is on a solid foundation. This document outlines the remaining features required to complete the current vision, as well as potential enhancements for future versions.

---

## Foundational Priority: Code Quality & Robustness

This is an ongoing priority that should be addressed alongside all new feature development to ensure the long-term health and stability of the project.

### Increase Test Coverage to >90%

* **Goal:** To move from the current coverage level to 85–95%, ensuring automated tests verify all critical application logic.
* **Strategy:**
    1.  **Target Untested Logic:** Use the Codecov report to identify modules and functions with low coverage.
    2.  **Write "Unhappy Path" Tests:** Add specific unit tests for error conditions, such as file I/O errors in the `Ingestor`, API failures in the `Validator`, and malformed entries in the `Reconciler`.
    3.  **Ensure Full Branch Coverage:** Add tests to verify that all `if/else` conditions in the `Triage` and `Reconciler` classes are executed.
    4.  **Maintain Coverage:** Configure CI (e.g., with Codecov's settings) to fail a pull request if it decreases the overall test coverage.

### Refactor Pipeline for Immutable Data Flow

* **Problem:** Currently, each component (`Validator`, `Refresher`, `Reconciler`) modifies the main `BibDatabase` object "in-place." This can lead to subtle side-effect bugs, where one component's changes unexpectedly break a later one (e.g., the title-refresh bug affecting the reconciler).
* **Solution:** Refactor the `BibTexManager` and all pipeline components to follow a more functional approach. Each step should take a database object as input and return a **new, transformed database object** as output. The manager would be responsible for chaining these steps together.
* **Benefits:** This architectural change provides:
    * **Data Lineage:** The state of the data can be inspected at every intermediate step, making debugging trivial.
    * **Resilience:** It eliminates the class of side-effect bugs we encountered.
    * **Clarity:** The inputs and outputs for each step become explicit and easier to reason about.

---

## Priority 1: High-Value Future Enhancements

These features would provide the most significant improvements in coverage and usability for a future `v1.0` release.

### 1. Implement Configurable Quality Gating (API-First Approach)
* **Goal:** To make the tool's filtering logic flexible and user-configurable, moving away from hard-coded rules.
* **Strategy:** We will follow an "API-First" development model to implement this feature.
    1.  **Build CLI Scaffold:** First, implement the new user-facing commands in `cli.py` with placeholder ("Not Implemented") logic. This includes the `bib-ami config` sub-command (with `set`, `get`, `list`) and the `--split-by-quality` output flag.
    2.  **Implement `config` Command Logic:** Build and test the full functionality for the `config` command to read from and write to the user's JSON configuration file.
    3.  **Implement Internal Quality Scoring:** Modify the `Validator` and `Refresher` to assign a "quality level" (e.g., Verified, Confirmed, Accepted) to each entry's audit trail.
    4.  **Connect Logic to CLI:** Finally, update the `Triage` and `Writer` components to use the quality scores and the rules from the configuration file to perform the final filtering and file writing.

### 2. Add DataCite API Support

* **Problem:** CrossRef primarily covers journal articles and conference papers. Datasets, software, and many technical reports are registered with DataCite.
* **Solution:** Create a `DataCiteClient` that mirrors the `CrossRefClient`. The `Validator` would first query CrossRef; if no match is found, it would then query DataCite as a fallback. This would dramatically increase the tool's coverage.

### 3. Add ISBN Validation for Books

* **Problem:** Books are a common entry type but often lack DOIs.
* **Solution:** For entries of type `@book`, use the `isbn` field to query an external source like the **Google Books API** or **Open Library API**. A successful match would allow the book to be validated and its metadata refreshed.

### 4. Implement API Caching

* **Problem:** Running the tool multiple times on the same library results in many redundant API calls, which is slow and unfriendly to the API providers.
* **Solution:** Implement a simple local file-based cache. Before making an API call, check if the query has been made recently. If so, use the cached result. This would provide a performance boost for iterative runs.

---

## Priority 2: Robustness and Quality-of-Life Improvements

These are smaller features that would make the tool more professional and easier to use.

* **Interactive "Gleaning" Mode:** For the `suspect.bib` file, an interactive mode could present each suspect entry to the user and ask them to `[k]eep`, `[d]iscard`, or `[s]earch again with new metadata?`.
* **Configurable Triage Rules:** Move the rules for what constitutes an "Accepted" entry (e.g., `@book`, `@techreport`) into a configuration file, allowing users to customize the triage logic.
* **Parallel API Requests:** The validation phase is the main bottleneck. Refactor the `Validator` to use Python's `concurrent.futures` to make multiple API requests in parallel, speeding up the process for large bibliographies.