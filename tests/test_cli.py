"""Tests for CLI module."""

import pytest
import sys
from io import StringIO
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from cyberlab.cli import (
    main,
    cmd_list,
    cmd_run,
    cmd_info,
    print_error,
    print_success,
    print_info,
    print_header,
    EXIT_SUCCESS,
    EXIT_GENERAL_ERROR,
    EXIT_LAB_NOT_FOUND,
    EXIT_LAB_LOAD_ERROR,
    EXIT_INVALID_ARGUMENT,
)


class TestExitCodes:
    """Tests for exit codes."""

    def test_exit_codes_defined(self):
        """Test that all exit codes are defined."""
        assert EXIT_SUCCESS == 0
        assert EXIT_GENERAL_ERROR == 1
        assert EXIT_LAB_NOT_FOUND == 2
        assert EXIT_LAB_LOAD_ERROR == 3
        assert EXIT_INVALID_ARGUMENT == 4


class TestCmdList:
    """Tests for cmd_list function."""

    @patch('cyberlab.cli.list_labs')
    def test_cmd_list_success(self, mock_list_labs):
        """Test successful list command."""
        mock_list_labs.return_value = ["sql_injection", "password_cracking"]
        
        result = cmd_list(MagicMock())
        
        assert result == EXIT_SUCCESS

    @patch('cyberlab.cli.list_labs')
    def test_cmd_list_empty(self, mock_list_labs):
        """Test list command with no labs."""
        mock_list_labs.return_value = []
        
        result = cmd_list(MagicMock())
        
        assert result == EXIT_SUCCESS

    @patch('cyberlab.cli.list_labs')
    def test_cmd_list_error(self, mock_list_labs):
        """Test list command with error."""
        mock_list_labs.side_effect = Exception("Test error")
        
        result = cmd_list(MagicMock())
        
        assert result == EXIT_GENERAL_ERROR


class TestCmdRun:
    """Tests for cmd_run function."""

    @patch('cyberlab.cli.run_lab')
    def test_cmd_run_success(self, mock_run_lab):
        """Test successful run command."""
        mock_run_lab.return_value = True
        
        args = MagicMock()
        args.lab_name = "sql_injection"
        args.args = []
        
        result = cmd_run(args)
        
        assert result == EXIT_SUCCESS
        mock_run_lab.assert_called_once_with("sql_injection")

    @patch('cyberlab.cli.run_lab')
    def test_cmd_run_with_args(self, mock_run_lab):
        """Test run command with arguments."""
        mock_run_lab.return_value = True
        
        args = MagicMock()
        args.lab_name = "password_cracking"
        args.args = ["medium"]
        
        result = cmd_run(args)
        
        assert result == EXIT_SUCCESS
        mock_run_lab.assert_called_once_with("password_cracking", "medium")

    @patch('cyberlab.cli.run_lab')
    def test_cmd_run_lab_not_found(self, mock_run_lab):
        """Test run command with non-existent lab."""
        from cyberlab.lab_loader import LabNotFoundError
        mock_run_lab.side_effect = LabNotFoundError("Lab not found")
        
        args = MagicMock()
        args.lab_name = "nonexistent"
        
        result = cmd_run(args)
        
        assert result == EXIT_LAB_NOT_FOUND

    @patch('cyberlab.cli.run_lab')
    def test_cmd_run_lab_load_error(self, mock_run_lab):
        """Test run command with lab load error."""
        from cyberlab.lab_loader import LabLoadError
        mock_run_lab.side_effect = LabLoadError("Load error")
        
        args = MagicMock()
        args.lab_name = "broken_lab"
        
        result = cmd_run(args)
        
        assert result == EXIT_LAB_LOAD_ERROR


class TestCmdInfo:
    """Tests for cmd_info function."""

    @patch('cyberlab.cli.get_lab_info')
    def test_cmd_info_success(self, mock_get_info):
        """Test successful info command."""
        mock_get_info.return_value = {
            "name": "sql_injection",
            "description": "Test description",
            "difficulty": "Beginner"
        }
        
        args = MagicMock()
        args.lab_name = "sql_injection"
        
        result = cmd_info(args)
        
        assert result == EXIT_SUCCESS

    @patch('cyberlab.cli.get_lab_info')
    def test_cmd_info_not_found(self, mock_get_info):
        """Test info command with non-existent lab."""
        from cyberlab.lab_loader import LabNotFoundError
        mock_get_info.side_effect = LabNotFoundError("Lab not found")
        
        args = MagicMock()
        args.lab_name = "nonexistent"
        
        result = cmd_info(args)
        
        assert result == EXIT_LAB_NOT_FOUND


class TestPrintFunctions:
    """Tests for print functions."""

    def test_print_error(self):
        """Test print_error function."""
        # Should not raise an exception
        print_error("Test error message")

    def test_print_success(self):
        """Test print_success function."""
        # Should not raise an exception
        print_success("Test success message")

    def test_print_info(self):
        """Test print_info function."""
        # Should not raise an exception
        print_info("Test info message")

    def test_print_header(self):
        """Test print_header function."""
        # Should not raise an exception
        print_header("Test header")


class TestMain:
    """Tests for main function."""

    @patch('sys.argv', ['cyberlab', 'list'])
    @patch('cyberlab.cli.cmd_list')
    def test_main_list_command(self, mock_cmd_list):
        """Test main with list command."""
        mock_cmd_list.return_value = EXIT_SUCCESS
        
        result = main()
        
        assert result == EXIT_SUCCESS
        mock_cmd_list.assert_called_once()

    @patch('sys.argv', ['cyberlab', 'run', 'sql_injection'])
    @patch('cyberlab.cli.cmd_run')
    def test_main_run_command(self, mock_cmd_run):
        """Test main with run command."""
        mock_cmd_run.return_value = EXIT_SUCCESS
        
        result = main()
        
        assert result == EXIT_SUCCESS
        mock_cmd_run.assert_called_once()

    @patch('sys.argv', ['cyberlab', 'info', 'sql_injection'])
    @patch('cyberlab.cli.cmd_info')
    def test_main_info_command(self, mock_cmd_info):
        """Test main with info command."""
        mock_cmd_info.return_value = EXIT_SUCCESS
        
        result = main()
        
        assert result == EXIT_SUCCESS
        mock_cmd_info.assert_called_once()

    @patch('sys.argv', ['cyberlab'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_no_command(self, mock_stdout):
        """Test main with no command."""
        result = main()
        
        assert result == EXIT_SUCCESS

    @patch('sys.argv', ['cyberlab', 'unknown'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_unknown_command(self, mock_stdout):
        """Test main with unknown command."""
        result = main()
        
        assert result == EXIT_GENERAL_ERROR
