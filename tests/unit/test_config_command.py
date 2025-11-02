# tests/unit/test_config_command.py

import unittest
import json
from unittest.mock import patch, mock_open
from pathlib import Path

from bib_ami.cli import CLIParser


class TestConfigCommand(unittest.TestCase):
    """
    Unit tests for the 'config' sub-command in the CLIParser.
    """

    @patch("pathlib.Path.home")
    @patch("pathlib.Path.exists")
    @patch("pathlib.Path.mkdir")
    @patch("builtins.open", new_callable=mock_open)
    def test_config_set_creates_new_file_and_directory(self, mock_file, mock_mkdir, mock_exists, mock_home):
        """
        Tests that `config set` correctly creates the config directory and a new
        config file if they don't exist.
        """
        # Arrange: Simulate that the config file does not exist
        mock_exists.return_value = False
        # Set a predictable home directory for the test
        mock_home.return_value = Path("/fake/home")

        mock_argv = ['__main__', 'config', 'set', 'email', 'test@example.com']

        # Act
        with patch('sys.argv', mock_argv):
            parser = CLIParser()
            args = parser.parse_args()
            parser.handle_config_command(args)

        # Assert
        config_dir = Path("/fake/home/.config/bib-ami")
        mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)
        mock_file.assert_called_once_with(config_dir / "config.json", "w")

        handle = mock_file()
        written_data = "".join(call.args[0] for call in handle.write.call_args_list)
        self.assertEqual(json.loads(written_data), {"email": "test@example.com"})

    @patch("pathlib.Path.home")
    @patch("pathlib.Path.exists")
    @patch("pathlib.Path.mkdir")
    @patch("builtins.open", new_callable=mock_open, read_data='{"email": "old@example.com"}')
    def test_config_set_updates_existing_file(self, mock_file, mock_mkdir, mock_exists, mock_home):
        """
        Tests that `config set` correctly reads an existing config file,
        updates it with a new value, and writes it back.
        """
        # Arrange: Simulate that the config file already exists
        mock_exists.return_value = True
        mock_home.return_value = Path("/fake/home")

        mock_argv = ['__main__', 'config', 'set', 'fuzzy_threshold', '90']

        # Act
        with patch('sys.argv', mock_argv):
            parser = CLIParser()
            args = parser.parse_args()
            parser.handle_config_command(args)

        # Assert
        # The directory should not be created if it exists
        mock_mkdir.assert_not_called()

        handle = mock_file()
        written_data = "".join(call.args[0] for call in handle.write.call_args_list)
        final_config = json.loads(written_data)

        # Check that both old and new values are present
        self.assertEqual(final_config["email"], "old@example.com")
        self.assertEqual(final_config["fuzzy_threshold"], "90")

    @patch("pathlib.Path.home")
    @patch("pathlib.Path.exists")
    @patch("pathlib.Path.mkdir")
    @patch("builtins.open", new_callable=mock_open)
    def test_config_set_handles_nested_keys(self, mock_file, mock_mkdir, mock_exists, mock_home):
        """
        Tests that `config set` can correctly create and set a nested key like
        'triage_rules.min_quality_for_final_bib'.
        """
        # Arrange
        mock_exists.return_value = False
        mock_home.return_value = Path("/fake/home")

        mock_argv = ['__main__', 'config', 'set', 'triage_rules.min_quality_for_final_bib', 'Verified']

        # Act
        with patch('sys.argv', mock_argv):
            parser = CLIParser()
            args = parser.parse_args()
            parser.handle_config_command(args)

        # Assert
        handle = mock_file()
        written_data = "".join(call.args[0] for call in handle.write.call_args_list)
        final_config = json.loads(written_data)

        # Check that the nested structure was created correctly
        self.assertIn("triage_rules", final_config)
        self.assertEqual(final_config["triage_rules"]["min_quality_for_final_bib"], "Verified")

    @patch("pathlib.Path.home", return_value=Path("/fake/home"))
    @patch("pathlib.Path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data='{"email": "test@example.com"}')
    @patch("builtins.print")
    def test_config_get_retrieves_value(self, mock_print, mock_file, mock_exists, mock_home):
        """Tests that `config get` correctly retrieves and prints an existing value."""
        mock_argv = ['__main__', 'config', 'get', 'email']
        with patch('sys.argv', mock_argv):
            parser = CLIParser()
            args = parser.parse_args()
            parser.handle_config_command(args)

        mock_print.assert_called_once_with("test@example.com")

    @patch("pathlib.Path.home", return_value=Path("/fake/home"))
    @patch("pathlib.Path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data='{"email": "test@example.com"}')
    @patch("builtins.print")
    def test_config_get_handles_missing_key(self, mock_print, mock_file, mock_exists, mock_home):
        """Tests that `config get` prints a message for a non-existent key."""
        mock_argv = ['__main__', 'config', 'get', 'nonexistent_key']
        with patch('sys.argv', mock_argv):
            parser = CLIParser()
            args = parser.parse_args()
            parser.handle_config_command(args)

        mock_print.assert_called_once_with("Key 'nonexistent_key' not found in configuration.")

    @patch("pathlib.Path.home", return_value=Path("/fake/home"))
    @patch("pathlib.Path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data='{"email": "test@example.com", "fuzzy_threshold": 90}')
    @patch("builtins.print")
    def test_config_list_prints_all_settings(self, mock_print, mock_file, mock_exists, mock_home):
        """Tests that `config list` prints the entire configuration as formatted JSON."""
        mock_argv = ['__main__', 'config', 'list']
        with patch('sys.argv', mock_argv):
            parser = CLIParser()
            args = parser.parse_args()
            parser.handle_config_command(args)

        # Assert that print was called and that its output is valid, complete JSON
        mock_print.assert_called_once()
        printed_output = mock_print.call_args[0][0]
        parsed_output = json.loads(printed_output)
        self.assertEqual(parsed_output, {"email": "test@example.com", "fuzzy_threshold": 90})

    @patch("pathlib.Path.home", return_value=Path("/fake/home"))
    @patch("pathlib.Path.exists", return_value=False)
    @patch("builtins.print")
    def test_config_list_handles_no_file(self, mock_print, mock_exists, mock_home):
        """Tests that `config list` prints a clean message if no config file exists."""
        mock_argv = ['__main__', 'config', 'list']
        with patch('sys.argv', mock_argv):
            parser = CLIParser()
            args = parser.parse_args()
            parser.handle_config_command(args)

        config_path = Path("/fake/home") / ".config" / "bib-ami" / "config.json"
        mock_print.assert_called_once_with(f"No configuration found at {config_path}")
