# tests/test_cross_ref_client.py

import unittest
from unittest.mock import patch, MagicMock
import json
import tempfile
import pathlib
import requests

# Ensure the path is correct to import from your source directory
from bib_ami.cross_ref_client import CrossRefClient


class TestCrossRefClientLogging(unittest.TestCase):
    """
    Test suite for the structured JSONL logging in CrossRefClient.
    """

    def setUp(self):
        """Set up a temporary directory and a client instance for each test."""
        # Create a temporary directory to store the log file
        self.test_dir = tempfile.TemporaryDirectory()
        self.log_file_path = pathlib.Path(self.test_dir.name) / "test_results.jsonl"

        # We will patch the session creation, so these are placeholders
        self.client = CrossRefClient(
            email="test@example.com",
            results_log_file=str(self.log_file_path)
        )

        # Sample data for testing
        self.doi = "10.1234/example.doi"
        self.original_entry = {
            "title": "An Original Title",
            "author": "John Doe and Jane Smith"
        }

    def tearDown(self):
        """Clean up the temporary directory after each test."""
        self.test_dir.cleanup()

    @patch('bib_ami.cross_ref_client.requests.Session')
    def test_logging_on_success(self, mock_session_cls):
        """
        Verify that a successful API call writes a complete SUCCESS log.
        """
        # --- Arrange: Configure the mock session and its response ---
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "message": {
                "title": ["An Original Title"],  # Same title
                "author": [
                    {"given": "John", "family": "Doe"},
                    {"given": "Jane", "family": "Smith"},
                    {"given": "Sam", "family": "Jones"}  # One new author
                ]
            }
        }
        # Make raise_for_status do nothing for a successful response
        mock_response.raise_for_status.return_value = None

        # Configure the session instance's get method to return our mock response
        mock_session_instance = mock_session_cls.return_value
        mock_session_instance.get.return_value = mock_response

        # Re-initialize client to use the mocked session
        self.client.session = mock_session_instance

        # --- Act: Call the method under test ---
        result = self.client.get_metadata_by_doi(self.doi, self.original_entry)

        # --- Assert ---
        # 1. Assert the method returned the data
        self.assertIsNotNone(result)
        self.assertEqual(result['title'], ["An Original Title"])

        # 2. Assert the log file was created and contains one line
        self.assertTrue(self.log_file_path.exists())
        with open(self.log_file_path, 'r') as f:
            log_lines = f.readlines()
        self.assertEqual(len(log_lines), 1)

        # 3. Assert the log content is correct
        log_data = json.loads(log_lines[0])
        self.assertEqual(log_data['status'], 'SUCCESS')
        self.assertEqual(log_data['doi'], self.doi)
        self.assertEqual(log_data['diff']['title_diff'], 'No change')
        self.assertEqual(log_data['diff']['authors_diff']['added'], ["Sam Jones"])
        self.assertEqual(log_data['diff']['authors_diff']['removed'], [])

    @patch('bib_ami.cross_ref_client.requests.Session')
    def test_logging_on_failure(self, mock_session_cls):
        """
        Verify that a failed API call writes a complete FAILURE log.
        """
        # --- Arrange: Configure the mock to simulate an HTTP error ---
        error_message = "404 Client Error: Not Found"
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(error_message)

        mock_session_instance = mock_session_cls.return_value
        mock_session_instance.get.return_value = mock_response
        self.client.session = mock_session_instance

        # --- Act: Call the method under test ---
        result = self.client.get_metadata_by_doi(self.doi, self.original_entry)

        # --- Assert ---
        # 1. Assert the method returned None on failure
        self.assertIsNone(result)

        # 2. Assert the log file was created
        self.assertTrue(self.log_file_path.exists())
        with open(self.log_file_path, 'r') as f:
            log_lines = f.readlines()
        self.assertEqual(len(log_lines), 1)

        # 3. Assert the log content is correct
        log_data = json.loads(log_lines[0])
        self.assertEqual(log_data['status'], 'FAILURE')
        self.assertEqual(log_data['doi'], self.doi)
        self.assertIn('error_message', log_data)
        self.assertEqual(log_data['error_message'], error_message)


if __name__ == '__main__':
    unittest.main(verbosity=2)
