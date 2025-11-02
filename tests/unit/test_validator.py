# tests/unit/test_validator.py

import unittest
from unittest.mock import MagicMock

from bib_ami.validator import Validator
from tests.fixtures.record_builder import RecordBuilder  # Assuming this is available


class TestValidatorUnit(unittest.TestCase):
    """
    Focused unit tests for the private _validate_entry method in the Validator.
    """

    def setUp(self):
        """Set up a mock client and a Validator instance for each test."""
        # Create a mock client that we can control for each test case
        self.mock_client = MagicMock()
        self.validator = Validator(client=self.mock_client)

    def test_validate_entry_for_book(self):
        """
        Rule 1: Books should be treated as pre-validated and should NOT call the client.
        The method should return the book's own DOI if present.
        """
        # Arrange: Create a book entry with a DOI
        book_with_doi = RecordBuilder("book1").as_book().with_doi("10.9999/book.doi").build()

        # Act
        result = self.validator._validate_entry(book_with_doi)

        # Assert
        self.assertEqual(result, "10.9999/book.doi")
        self.mock_client.get_doi_for_entry.assert_not_called()

    def test_validate_entry_for_book_without_doi(self):
        """
        Rule 1a: A book without a DOI should also not call the client and return None.
        """
        # Arrange
        book_without_doi = RecordBuilder("book2").as_book().build()

        # Act
        result = self.validator._validate_entry(book_without_doi)

        # Assert
        self.assertIsNone(result)
        self.mock_client.get_doi_for_entry.assert_not_called()

    def test_validate_entry_for_article_with_found_and_resolvable_doi(self):
        """
        Rule 2: A standard entry should call the client, which finds a DOI
        that successfully resolves.
        """
        article = RecordBuilder("article1").with_title("An Article").build()
        expected_doi = "10.1234/article.doi"
        self.mock_client.get_doi_for_entry.return_value = expected_doi

        # --- NEW: Configure the mock for the doi.org check ---
        mock_head_response = MagicMock()
        mock_head_response.status_code = 302  # Simulate a successful redirect
        self.mock_client.session.head.return_value = mock_head_response

        result = self.validator._validate_entry(article)

        self.assertEqual(result, expected_doi)
        self.mock_client.get_doi_for_entry.assert_called_once_with(article)
        self.mock_client.session.head.assert_called_once()

    def test_validate_entry_for_article_with_unresolvable_doi(self):
        """
        Rule 3: The client finds a DOI, but it does not resolve (e.g., 404).
        """
        article = RecordBuilder("article2").with_title("Another Article").build()
        self.mock_client.get_doi_for_entry.return_value = "10.5678/bad.doi"

        # --- NEW: Configure the mock for a FAILED doi.org check ---
        mock_head_response = MagicMock()
        mock_head_response.status_code = 404  # Simulate Not Found
        self.mock_client.session.head.return_value = mock_head_response

        result = self.validator._validate_entry(article)

        self.assertIsNone(result)
        self.mock_client.get_doi_for_entry.assert_called_once_with(article)
        self.mock_client.session.head.assert_called_once()


if __name__ == '__main__':
    unittest.main(verbosity=2)