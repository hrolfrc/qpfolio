import unittest
import copy

# Assuming your source code is structured to allow this import
from bib_ami.metadata_refresher import MetadataRefresher


# noinspection PyTypeChecker
class TestMetadataRefresher(unittest.TestCase):
    """
    Focused unit tests for the _refresh_single_entry helper method
    in the MetadataRefresher.
    """

    def setUp(self):
        """Set up a refresher instance for each test."""
        # The client isn't used by the helper method, so we can pass None.
        self.refresher = MetadataRefresher(client=None)

    def test_refreshes_all_fields_when_changed(self):
        """
        Tests that all fields are correctly updated when the metadata
        from the API is new and different.
        """
        # Arrange
        original_entry = {
            "ID": "test_id",
            "ENTRYTYPE": "article",
            "title": "Old Title",
            "author": "Doe, John",
            "year": "2020",
        }
        api_metadata = {
            "title": ["A New, Better Title"],
            "author": [{"family": "Smith", "given": "Jane"}],
            "year": "2023",
            "journal": "Journal of New Results",
            "isbn": ["978-3-16-148410-0", "978-0-521-88073-5"]
        }

        # Act
        changed = self.refresher._refresh_single_entry(original_entry, api_metadata)

        # Assert
        self.assertTrue(changed)
        self.assertEqual(original_entry["title"], "A New, Better Title")
        self.assertEqual(original_entry["author"], "Smith, Jane")
        self.assertEqual(original_entry["year"], "2023")
        self.assertEqual(original_entry["journal"], "Journal of New Results")
        self.assertEqual(original_entry["isbn"], "978-3-16-148410-0")  # Should take the first ISBN

    def test_returns_false_when_no_changes_made(self):
        """
        Tests that the method correctly identifies when the fetched metadata
        matches the existing data, making no changes and returning False.
        """
        # Arrange
        original_entry = {
            "ID": "test_id",
            "ENTRYTYPE": "article",
            "title": "A Perfect Title",
            "author": "Smith, Jane",
            "year": "2023",
        }
        # A deep copy to compare against later
        entry_before_refresh = copy.deepcopy(original_entry)

        api_metadata = {
            "title": ["A Perfect Title"],
            "author": [{"family": "Smith", "given": "Jane"}],
            "year": "2023",
        }

        # Act
        changed = self.refresher._refresh_single_entry(original_entry, api_metadata)

        # Assert
        self.assertFalse(changed)
        self.assertEqual(original_entry, entry_before_refresh)  # Ensure no fields were touched

    def test_handles_empty_or_missing_metadata_gracefully(self):
        """
        Tests that no changes are made and no errors occur when the API
        returns an empty or minimal metadata object.
        """
        # Arrange
        original_entry = {"ID": "test_id", "title": "A Title"}
        entry_before_refresh = copy.deepcopy(original_entry)
        empty_metadata = {}

        # Act
        changed = self.refresher._refresh_single_entry(original_entry, empty_metadata)

        # Assert
        self.assertFalse(changed)
        self.assertEqual(original_entry, entry_before_refresh)

    def test_only_updates_changed_fields(self):
        """
        Tests that only the differing fields are updated, leaving
        matching fields untouched.
        """
        # Arrange
        original_entry = {
            "ID": "test_id",
            "title": "Old Title",
            "author": "Smith, Jane"
        }
        api_metadata = {
            "title": ["A New Title"],  # This title is different
            "author": [{"family": "Smith", "given": "Jane"}]  # This author is the same
        }

        # Act
        changed = self.refresher._refresh_single_entry(original_entry, api_metadata)

        # Assert
        self.assertTrue(changed)
        self.assertEqual(original_entry["title"], "A New Title")
        self.assertEqual(original_entry["author"], "Smith, Jane")  # Should be unchanged


if __name__ == '__main__':
    unittest.main(verbosity=2)
