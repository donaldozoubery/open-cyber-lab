"""Tests for lab modules."""

import pytest
import sys
from pathlib import Path
from io import StringIO
from unittest.mock import patch

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestSqlInjectionLab:
    """Tests for SQL Injection lab."""

    def test_sql_injection_run_exists(self):
        """Test that sql_injection lab has a run function."""
        from labs import sql_injection
        assert hasattr(sql_injection, "run")
        assert callable(sql_injection.run)

    def test_sql_injection_metadata(self):
        """Test that sql_injection has metadata."""
        from labs import sql_injection
        assert hasattr(sql_injection, "DIFFICULTY")
        assert hasattr(sql_injection, "OBJECTIVES")
        assert sql_injection.DIFFICULTY == "Beginner"
        assert isinstance(sql_injection.OBJECTIVES, list)
        assert len(sql_injection.OBJECTIVES) > 0

    def test_check_sql_injection(self):
        """Test SQL injection detection function."""
        from labs.sql_injection import check_sql_injection
        
        # Should detect SQL injection patterns
        assert check_sql_injection("admin' OR '1'='1") is True
        assert check_sql_injection("admin' OR '1'='1' --") is True
        assert check_sql_injection("' OR '1'='1' /*") is True
        assert check_sql_injection("admin' --") is True
        assert check_sql_injection("'; DROP TABLE users; --") is True
        
        # Should not flag normal input
        assert check_sql_injection("admin") is False
        assert check_sql_injection("john_doe") is False
        assert check_sql_injection("test123") is False

    def test_validate_solution_sql_injection_success(self):
        """Test solution validation with SQL injection."""
        from labs.sql_injection import validate_solution
        
        result = validate_solution("admin' OR '1'='1", "")
        
        assert result["success"] is True
        assert "SQL Injection detected" in result["message"]

    def test_validate_solution_valid_credentials(self):
        """Test solution validation with valid credentials."""
        from labs.sql_injection import validate_solution
        
        result = validate_solution("admin", "admin123")
        
        assert result["success"] is False

    def test_validate_solution_wrong_credentials(self):
        """Test solution validation with wrong credentials."""
        from labs.sql_injection import validate_solution
        
        result = validate_solution("admin", "wrong_password")
        
        assert result["success"] is False


class TestPasswordCrackingLab:
    """Tests for Password Cracking lab."""

    def test_password_cracking_run_exists(self):
        """Test that password_cracking lab has a run function."""
        from labs import password_cracking
        assert hasattr(password_cracking, "run")
        assert callable(password_cracking.run)

    def test_password_cracking_metadata(self):
        """Test that password_cracking has metadata."""
        from labs import password_cracking
        assert hasattr(password_cracking, "DIFFICULTY")
        assert hasattr(password_cracking, "OBJECTIVES")
        assert password_cracking.DIFFICULTY == "Beginner"
        assert isinstance(password_cracking.OBJECTIVES, list)
        assert len(password_cracking.OBJECTIVES) > 0

    def test_hash_password(self):
        """Test password hashing function."""
        from labs.password_cracking import hash_password
        
        # Same password should always produce same hash
        hash1 = hash_password("test123")
        hash2 = hash_password("test123")
        assert hash1 == hash2
        assert len(hash1) == 64  # SHA-256 produces 64 hex characters

    def test_generate_wordlist_sizes(self):
        """Test wordlist generation."""
        from labs.password_cracking import generate_wordlist
        
        small = generate_wordlist("small")
        medium = generate_wordlist("medium")
        large = generate_wordlist("large")
        
        assert len(small) == 10
        assert len(medium) == 20
        assert len(large) > len(medium)

    def test_crack_password_success(self):
        """Test password cracking with correct guess."""
        from labs.password_cracking import crack_password, hash_password
        
        password = "secret123"
        target_hash = hash_password(password)
        wordlist = ["admin", "password", "secret123", "test"]
        
        success, found, attempts = crack_password(target_hash, wordlist)
        
        assert success is True
        assert found == "secret123"
        assert attempts == 3

    def test_crack_password_failure(self):
        """Test password cracking with wrong wordlist."""
        from labs.password_cracking import crack_password, hash_password
        
        password = "very_secure_password_12345"
        target_hash = hash_password(password)
        wordlist = ["admin", "password", "secret123", "test"]
        
        success, found, attempts = crack_password(target_hash, wordlist)
        
        assert success is False
        assert found is None
        assert attempts == 4

    def test_validate_solution_success(self):
        """Test solution validation when cracked."""
        from labs.password_cracking import validate_solution
        
        result = validate_solution(True)
        
        assert result["success"] is True
        assert "successfully" in result["message"].lower()

    def test_validate_solution_failure(self):
        """Test solution validation when not cracked."""
        from labs.password_cracking import validate_solution
        
        result = validate_solution(False)
        
        assert result["success"] is False


class TestLabIntegration:
    """Integration tests for labs."""

    def test_all_labs_have_run_function(self):
        """Test that all labs have a run function."""
        import labs
        import pkgutil
        
        for _, module_name, _ in pkgutil.iter_modules(labs.__path__):
            module = __import__(f"labs.{module_name}", fromlist=["run"])
            assert hasattr(module, "run"), f"{module_name} missing run function"

    def test_all_labs_have_metadata(self):
        """Test that all labs have metadata."""
        import labs
        import pkgutil
        
        for _, module_name, _ in pkgutil.iter_modules(labs.__path__):
            module = __import__(f"labs.{module_name}", fromlist=["DIFFICULTY", "OBJECTIVES"])
            assert hasattr(module, "DIFFICULTY"), f"{module_name} missing DIFFICULTY"
            assert hasattr(module, "OBJECTIVES"), f"{module_name} missing OBJECTIVES"
