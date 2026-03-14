"""Progress tracking module for Open Cyber Lab.

This module handles user progress tracking, storing completed labs
and providing statistics about learning progress.
"""

import json
import os
from datetime import datetime
from typing import Optional

# Default progress file location
DEFAULT_PROGRESS_FILE = ".cyberlab_progress.json"


class ProgressTracker:
    """Track user progress through cybersecurity labs."""
    
    def __init__(self, progress_file: Optional[str] = None):
        """Initialize the progress tracker.
        
        Args:
            progress_file: Path to progress file (default: .cyberlab_progress.json)
        """
        self.progress_file = progress_file or DEFAULT_PROGRESS_FILE
        self.data: dict = self._load_data()
    
    def _load_data(self) -> dict:
        """Load progress data from file.
        
        Returns:
            dict: Progress data
        """
        if os.path.exists(self.progress_file):
            try:
                with open(self.progress_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return self._create_empty_data()
        return self._create_empty_data()
    
    def _create_empty_data(self) -> dict:
        """Create empty progress data structure.
        
        Returns:
            dict: Empty progress data
        """
        return {
            "version": "1.0.0",
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "completed_labs": {},
            "total_attempts": 0,
            "statistics": {
                "total_time_spent": 0,
                "favorite_lab": None
            }
        }
    
    def _save_data(self) -> None:
        """Save progress data to file."""
        self.data["last_updated"] = datetime.now().isoformat()
        
        try:
            with open(self.progress_file, 'w') as f:
                json.dump(self.data, f, indent=2)
        except IOError as e:
            print(f"Warning: Could not save progress: {e}")
    
    def complete_lab(self, lab_name: str, attempts: int = 1, time_spent: int = 0) -> bool:
        """Mark a lab as completed.
        
        Args:
            lab_name: Name of the completed lab
            attempts: Number of attempts to complete
            time_spent: Time spent in seconds
            
        Returns:
            bool: True if successful
        """
        self.data["completed_labs"][lab_name] = {
            "completed_at": datetime.now().isoformat(),
            "attempts": attempts,
            "time_spent": time_spent
        }
        self.data["total_attempts"] += attempts
        self.data["statistics"]["total_time_spent"] += time_spent
        
        self._save_data()
        return True
    
    def is_completed(self, lab_name: str) -> bool:
        """Check if a lab is completed.
        
        Args:
            lab_name: Name of the lab
            
        Returns:
            bool: True if completed
        """
        return lab_name in self.data["completed_labs"]
    
    def get_completed_labs(self) -> list[str]:
        """Get list of completed labs.
        
        Returns:
            list[str]: List of completed lab names
        """
        return list(self.data["completed_labs"].keys())
    
    def get_lab_progress(self, lab_name: str) -> Optional[dict]:
        """Get progress for a specific lab.
        
        Args:
            lab_name: Name of the lab
            
        Returns:
            Optional[dict]: Lab progress data or None
        """
        return self.data["completed_labs"].get(lab_name)
    
    def reset_progress(self) -> bool:
        """Reset all progress data.
        
        Returns:
            bool: True if successful
        """
        self.data = self._create_empty_data()
        self._save_data()
        return True
    
    def get_statistics(self) -> dict:
        """Get overall statistics.
        
        Returns:
            dict: Statistics data
        """
        completed = len(self.data["completed_labs"])
        
        return {
            "total_completed": completed,
            "total_attempts": self.data["total_attempts"],
            "total_time_spent": self.data["statistics"]["total_time_spent"],
            "completed_labs": self.get_completed_labs()
        }
    
    def export_progress(self, filename: str) -> bool:
        """Export progress to a file.
        
        Args:
            filename: Output filename
            
        Returns:
            bool: True if successful
        """
        try:
            with open(filename, 'w') as f:
                json.dump(self.data, f, indent=2)
            return True
        except IOError:
            return False
    
    def import_progress(self, filename: str) -> bool:
        """Import progress from a file.
        
        Args:
            filename: Input filename
            
        Returns:
            bool: True if successful
        """
        try:
            with open(filename, 'r') as f:
                self.data = json.load(f)
            self._save_data()
            return True
        except (IOError, json.JSONDecodeError):
            return False


# Global tracker instance
_tracker: Optional[ProgressTracker] = None


def get_tracker() -> ProgressTracker:
    """Get or create the global progress tracker.
    
    Returns:
        ProgressTracker: The tracker instance
    """
    global _tracker
    if _tracker is None:
        _tracker = ProgressTracker()
    return _tracker


def complete_lab(lab_name: str, attempts: int = 1, time_spent: int = 0) -> bool:
    """Convenience function to mark a lab as completed.
    
    Args:
        lab_name: Name of the completed lab
        attempts: Number of attempts
        time_spent: Time spent in seconds
        
    Returns:
        bool: True if successful
    """
    return get_tracker().complete_lab(lab_name, attempts, time_spent)


def is_completed(lab_name: str) -> bool:
    """Convenience function to check if a lab is completed.
    
    Args:
        lab_name: Name of the lab
        
    Returns:
        bool: True if completed
    """
    return get_tracker().is_completed(lab_name)


def get_statistics() -> dict:
    """Convenience function to get statistics.
    
    Returns:
        dict: Statistics data
    """
    return get_tracker().get_statistics()
