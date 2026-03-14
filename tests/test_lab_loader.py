"""Tests for lab_loader module."""

import pytest
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from cyberlab.lab_loader import (
    validate_lab_name,
    list_labs,
    get_lab_info,
    run_lab,
    LabError,
    LabNotFoundError,
    LabLoadError,
    LabValidationError,
)


class TestValidateLabName:
    """Tests for validate_lab_name function."""

    def test_valid_lab_name(self):
        """Test valid lab names pass validation."""
        assert validate_lab_name("sql_injection") == "sql_injection"
        assert validate_lab_name("password_cracking") == "password_cracking"
        assert validate_lab_name("test123") == "test123"

    def test_empty_name_raises_error(self):
        """Test empty name raises validation error."""
        with pytest.raises(LabValidationError, match="cannot be empty"):
            validate_lab_name("")

    def test_path_traversal_raises_error(self):
        """Test path traversal attempts raise error."""
        with pytest.raises(LabValidationError, match="path traversal"):
            validate_lab_name("../etc/passwd")
        
        with pytest.raises(LabValidationError, match="path traversal"):
            validate_lab_name("../../../root")
        
        with pytest.raises(LabValidationError, match="path traversal"):
            validate_lab_name("labs/../labs/sql_injection")

    def test_forward_slash_raises_error(self):
        """Test forward slash raises error."""
        with pytest.raises(LabValidationError, match="path traversal"):
            validate_lab_name("labs/sql_injection")

    def test_backslash_raises_error(self):
        """Test backslash raises error."""
        with pytest.raises(LabValidationError, match="path traversal"):
            validate_lab_name("labs\\sql_injection")

    def test_dangerous_characters_raise_error(self):
        """Test dangerous characters raise error."""
        with pytest.raises(LabValidationError):
            validate_lab_name("test;rm -rf")
        
        with pytest.raises(LabValidationError):
            validate_lab_name("test&whoami")
        
        with pytest.raises(LabValidationError):
            validate_lab_name("test|cat /etc/passwd")


class TestListLabs:
    """Tests for list_labs function."""

    def test_list_labs_returns_list(self):
        """Test that list_labs returns a list."""
        labs = list_labs()
        assert isinstance(labs, list)

    def test_list_labs_contains_expected(self):
        """Test that expected labs are present."""
        labs = list_labs()
        assert "sql_injection" in labs
        assert "password_cracking" in labs

    def test_list_labs_sorted(self):
        """Test that labs are sorted alphabetically."""
        labs = list_labs()
        assert labs == sorted(labs)

    def test_list_labs_excludes_dunder(self):
        """Test that __init__ and __pycache__ are excluded."""
        labs = list_labs()
        assert "__init__" not in labs
        assert "__pycache__" not in labs


class TestGetLabInfo:
    """Tests for get_lab_info function."""

    def test_get_lab_info_returns_dict(self):
        """Test that get_lab_info returns a dictionary."""
        info = get_lab_info("sql_injection")
        assert isinstance(info, dict)

    def test_get_lab_info_contains_name(self):
        """Test that info contains the lab name."""
        info = get_lab_info("sql_injection")
        assert info["name"] == "sql_injection"

    def test_get_lab_info_contains_description(self):
        """Test that info contains a description."""
        info = get_lab_info("sql_injection")
        assert "description" in info

    def test_get_lab_info_not_found(self):
        """Test that non-existent lab raises error."""
        with pytest.raises(LabNotFoundError):
            get_lab_info("nonexistent_lab")

    def test_get_lab_info_invalid_name(self):
        """Test that invalid name raises error."""
        with pytest.raises(LabValidationError):
            get_lab_info("../etc/passwd")


class TestRunLab:
    """Tests for run_lab function."""

    def test_run_lab_sql_injection(self):
        """Test running sql_injection lab."""
        # Should not raise an exception
        result = run_lab("sql_injection")
        assert result is not None

    def test_run_lab_password_cracking(self):
        """Test running password_cracking lab."""
        # Should not raise an exception
        result = run_lab("password_cracking")
        assert result is not None

    def test_run_lab_not_found(self):
        """Test running non-existent lab raises error."""
        with pytest.raises(LabNotFoundError):
            run_lab("nonexistent_lab")

    def test_run_lab_invalid_name(self):
        """Test running with invalid name raises error."""
        with pytest.raises(LabValidationError):
            run_lab("../etc/passwd")

    def test_run_lab_with_args(self):
        """Test running lab with arguments."""
        # password_cracking accepts wordlist size
        result = run_lab("password_cracking", "small")
        assert result is not None


class TestLabError:
    """Tests for custom exception classes."""

    def test_lab_error_base(self):
        """Test LabError can be raised and caught."""
        with pytest.raises(LabError):
            raise LabError("test error")

    def test_lab_not_found_error(self):
        """Test LabNotFoundError inheritance."""
        with pytest.raises(LabError):
            raise LabNotFoundError("not found")

    def test_lab_load_error(self):
        """Test LabLoadError inheritance."""
        with pytest.raises(LabError):
            raise LabLoadError("load error")

    def test_lab_validation_error(self):
        """Test LabValidationError inheritance."""
        with pytest.raises(LabError):
            raise LabValidationError("validation error")
