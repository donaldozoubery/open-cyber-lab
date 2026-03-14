"""Tests for progress module."""

import pytest
import sys
import json
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from cyberlab.progress import ProgressTracker


class TestProgressTracker:
    """Tests for ProgressTracker class."""

    def test_create_empty_data(self):
        """Test empty data creation."""
        with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as f:
            tracker = ProgressTracker(f.name)
            assert tracker.data["version"] == "1.0.0"
            assert tracker.data["completed_labs"] == {}
            Path(f.name).unlink()

    def test_complete_lab(self):
        """Test completing a lab."""
        with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as f:
            tracker = ProgressTracker(f.name)
            result = tracker.complete_lab("sql_injection", attempts=2, time_spent=60)
            assert result is True
            assert "sql_injection" in tracker.data["completed_labs"]
            Path(f.name).unlink()

    def test_is_completed(self):
        """Test checking if lab is completed."""
        with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as f:
            tracker = ProgressTracker(f.name)
            tracker.complete_lab("sql_injection")
            assert tracker.is_completed("sql_injection") is True
            assert tracker.is_completed("xss") is False
            Path(f.name).unlink()

    def test_get_completed_labs(self):
        """Test getting completed labs."""
        with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as f:
            tracker = ProgressTracker(f.name)
            tracker.complete_lab("sql_injection")
            tracker.complete_lab("xss")
            labs = tracker.get_completed_labs()
            assert len(labs) == 2
            Path(f.name).unlink()

    def test_reset_progress(self):
        """Test resetting progress."""
        with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as f:
            tracker = ProgressTracker(f.name)
            tracker.complete_lab("sql_injection")
            tracker.reset_progress()
            assert tracker.get_completed_labs() == []
            Path(f.name).unlink()

    def test_get_statistics(self):
        """Test getting statistics."""
        with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as f:
            tracker = ProgressTracker(f.name)
            tracker.complete_lab("sql_injection", attempts=3, time_spent=120)
            stats = tracker.get_statistics()
            assert stats["total_completed"] == 1
            assert stats["total_attempts"] == 3
            assert stats["total_time_spent"] == 120
            Path(f.name).unlink()


class TestConvenienceFunctions:
    """Tests for convenience functions."""

    @patch('cyberlab.progress._tracker', None)
    @patch('cyberlab.progress.ProgressTracker')
    def test_complete_lab_function(self, mock_tracker_class):
        """Test complete_lab convenience function."""
        from cyberlab.progress import complete_lab
        mock_instance = MagicMock()
        mock_tracker_class.return_value = mock_instance
        
        result = complete_lab("test_lab")
        
        assert result is True
        mock_instance.complete_lab.assert_called_once()

    @patch('cyberlab.progress._tracker', None)
    @patch('cyberlab.progress.ProgressTracker')
    def test_is_completed_function(self, mock_tracker_class):
        """Test is_completed convenience function."""
        from cyberlab.progress import is_completed
        mock_instance = MagicMock()
        mock_instance.is_completed.return_value = True
        mock_tracker_class.return_value = mock_instance
        
        result = is_completed("test_lab")
        
        assert result is True
        mock_instance.is_completed.assert_called_once()
