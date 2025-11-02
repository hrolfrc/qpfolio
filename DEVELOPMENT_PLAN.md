# Development Plan: Configurable Quality Gating

This document outlines the specific, ordered tasks required to implement the "Configurable Quality Gating" feature as defined in the project's main `ROADMAP.md`.

## Phase 1: Build the CLI Scaffold

*Goal: Create the full user-facing command-line interface, with placeholder logic.*

- [ ] Refactor `cli.py` to use `argparse`'s `subparsers` to support a `config` command.
- [ ] Add the placeholder for the `config` command.
- [ ] Add the `set`, `get`, and `list` actions as placeholders for the `config` command.
- [ ] Add the new `--split-by-quality` flag to the main command's arguments.
- [ ] Write initial unit tests to confirm the parser recognizes the new commands and flags without error.

## Phase 2: Fully Implement the `config` Command

*Goal: Make the `config` command fully functional for reading and writing settings.*

- [ ] Create a new helper module to manage the location of the config file (e.g., finding `~/.config/bib-ami/config.json`).
- [ ] Implement the `bib-ami config set <key> <value>` logic to write to the JSON file.
- [ ] Implement the `bib-ami config get <key>` logic to read a specific value.
- [ ] Implement the `bib-ami config list` logic to print the entire config file.
- [ ] Write comprehensive unit tests for all `config` actions, mocking the file system to test file creation, reading, and writing.

## Phase 3: Implement Internal Quality Scoring

*Goal: Teach the application to assign a quality score to every reference.*

- [ ] In the `Validator`, update the `_validate_entry` method to return a specific quality score (e.g., `4`, `2`, `0`) instead of just a DOI or None.
- [ ] Update the `validate_all` method to attach this score to each entry's `audit_info` dictionary.
- [ ] Update the `Refresher` so it doesn't alter the quality score set by the `Validator`.
- [ ] Update the unit tests for `_validate_entry` to check for the correct returned score.

## Phase 4: Connect Logic to the CLI

*Goal: Make the application's filtering and writing steps respect the new scores and configuration.*

- [ ] Update the `CLIParser` to read the `triage_rules` from the config file and to translate quality names (e.g., "Verified") into numbers (e.g., 4).
- [ ] Refactor the `Triage` class to use the `min_quality_for_final_bib` setting and the entry's `quality_level` score to perform its filtering.
- [ ] Update the `Writer` class to implement the file-splitting logic for the `--split-by-quality` flag.
- [ ] Update the end-to-end tests to verify that the entire system works correctly with the new configuration options.