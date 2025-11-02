# tests/unit/test_cli.py

import unittest
from unittest.mock import patch
from pathlib import Path

from bib_ami.cli import CLIParser


class TestCLIParser(unittest.TestCase):
    """
    Unit tests for the command-line interface parser (CLIParser).
    """

    # --- FIXED: Added the 'run' command to the argument list ---
    @patch('sys.argv',
           ['__main__', 'run', '--input-dir', 'in', '--output-file', 'out/final.bib', '--email', 'test@example.com'])
    def test_get_settings_generates_default_suspect_file(self):
        """
        Test Case 1: Verify that a default suspect_file path is created
        when one is not provided.
        """
        parser = CLIParser()
        expected_suspect_path = Path("out/final.suspect.bib")

        # In the test, we need to get the settings for the 'run' command
        args = parser.parse_args()
        settings = parser.get_run_settings(args)

        self.assertIsNotNone(settings.suspect_file)
        self.assertEqual(settings.suspect_file, expected_suspect_path)

    # --- FIXED: Added the 'run' command to the argument list ---
    @patch('sys.argv',
           ['__main__', 'run', '--input-dir', 'in', '--output-file', 'out.bib', '--suspect-file', 'custom/explicit.bib',
            '--email', 'test@example.com'])
    def test_get_settings_respects_provided_suspect_file(self):
        """
        Test Case 2: Verify that a user-provided suspect_file path is
        used and not overwritten by the default logic.
        """
        parser = CLIParser()
        expected_suspect_path = Path("custom/explicit.bib")

        args = parser.parse_args()
        settings = parser.get_run_settings(args)

        self.assertEqual(settings.suspect_file, expected_suspect_path)

    # This test doesn't need 'run' because it's testing a top-level failure
    @patch('sys.argv', ['__main__', 'run', '--input-dir', 'in', '--output-file', 'out.bib'])
    def test_get_settings_errors_without_email(self):
        """
        Test Case 3: Verify that the parser correctly exits if the required
        --email argument is not provided.
        """
        parser = CLIParser()

        with self.assertRaises(SystemExit):
            args = parser.parse_args()
            # We call get_run_settings to trigger the validation
            parser.get_run_settings(args)

# Note: I have removed the `if __name__ == '__main__'` block as it's not needed
# when running tests with a test runner like pytest.