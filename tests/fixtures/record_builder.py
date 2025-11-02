import logging

# Configure basic logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


# ==============================================================================
# File: tests/fixtures/record_builder.py
# A factory for creating BibTeX record dictionaries for tests.
# ==============================================================================

class RecordBuilder:
    """A fluent builder for creating BibTeX entry dictionaries for tests."""

    def __init__(self, entry_id: str):
        self._record = {"ID": entry_id, "ENTRYTYPE": "article"}

    def with_title(self, title: str):
        self._record["title"] = title
        return self

    def with_author(self, author: str):
        self._record["author"] = author
        return self

    def with_note(self, note: str):
        self._record["note"] = note
        return self

    # --- NEW: The missing method ---
    def with_doi(self, doi: str):
        """Adds a DOI to the record."""
        self._record["doi"] = doi
        return self

    def as_book(self):
        self._record["ENTRYTYPE"] = "book"
        return self

    def build(self) -> dict:
        return self._record
