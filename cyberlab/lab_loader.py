"""Lab loader module for loading and managing cybersecurity labs."""

import os
import importlib
from pathlib import Path
from typing import Optional

# Configuration - can be overridden by environment variable
LAB_FOLDER: str = os.environ.get("CYBERLAB_LABS_DIR", "labs")


class LabError(Exception):
    """Base exception for lab-related errors."""
    pass


class LabNotFoundError(LabError):
    """Raised when a lab cannot be found."""
    pass


class LabLoadError(LabError):
    """Raised when a lab fails to load."""
    pass


class LabValidationError(LabError):
    """Raised when lab validation fails."""
    pass


def get_labs_directory() -> Path:
    """Get the labs directory path.
    
    Returns:
        Path: Path to the labs directory
        
    Raises:
        LabError: If the labs directory doesn't exist
    """
    labs_path = Path(LAB_FOLDER)
    if not labs_path.exists():
        raise LabError(f"Labs directory not found: {LAB_FOLDER}")
    if not labs_path.is_dir():
        raise LabError(f"Labs path is not a directory: {LAB_FOLDER}")
    return labs_path


def validate_lab_name(name: str) -> str:
    """Validate and sanitize lab name to prevent path traversal.
    
    Args:
        name: The lab name to validate
        
    Returns:
        str: The validated lab name
        
    Raises:
        LabValidationError: If the lab name is invalid
    """
    if not name:
        raise LabValidationError("Lab name cannot be empty")
    
    # Check for path traversal attempts
    if ".." in name or "/" in name or "\\" in name:
        raise LabValidationError("Invalid lab name: path traversal detected")
    
    # Check for other dangerous characters
    dangerous_chars = [";", "&", "|", "$", "`"]
    for char in dangerous_chars:
        if char in name:
            raise LabValidationError(f"Invalid lab name: contains forbidden character '{char}'")
    
    return name


def list_labs() -> list[str]:
    """List all available labs in the labs directory.
    
    Returns:
        list[str]: List of available lab names
        
    Raises:
        LabError: If the labs directory cannot be accessed
    """
    try:
        labs_path = get_labs_directory()
    except LabError:
        return []
    
    labs: list[str] = []
    for f in labs_path.iterdir():
        if f.is_file() and f.suffix == ".py" and not f.name.startswith("__"):
            labs.append(f.stem)
    
    return sorted(labs)


def get_lab_info(name: str) -> dict:
    """Get information about a specific lab.
    
    Args:
        name: The lab name
        
    Returns:
        dict: Lab information including name, description, and difficulty
        
    Raises:
        LabNotFoundError: If the lab doesn't exist
    """
    name = validate_lab_name(name)
    
    try:
        labs_path = get_labs_directory()
    except LabError as e:
        raise LabNotFoundError(str(e))
    
    lab_file = labs_path / f"{name}.py"
    if not lab_file.exists():
        raise LabNotFoundError(f"Lab '{name}' not found")
    
    # Try to import and get docstring
    module = importlib.import_module(f"labs.{name}")
    
    info: dict = {
        "name": name,
        "description": module.__doc__ or "No description available",
    }
    
    # Try to get additional metadata if available
    if hasattr(module, "DIFFICULTY"):
        info["difficulty"] = module.DIFFICULTY
    if hasattr(module, "OBJECTIVES"):
        info["objectives"] = module.OBJECTIVES
    
    return info


def run_lab(name: str, *args: str) -> bool:
    """Run a specific lab by name.
    
    Args:
        name: The lab name to run
        *args: Optional arguments to pass to the lab
        
    Returns:
        bool: True if the lab completed successfully, False otherwise
        
    Raises:
        LabNotFoundError: If the lab doesn't exist
        LabLoadError: If the lab fails to load or run
    """
    name = validate_lab_name(name)
    
    try:
        labs_path = get_labs_directory()
    except LabError as e:
        raise LabNotFoundError(str(e))
    
    lab_file = labs_path / f"{name}.py"
    if not lab_file.exists():
        raise LabNotFoundError(f"Lab '{name}' not found in {LAB_FOLDER}")
    
    try:
        module = importlib.import_module(f"labs.{name}")
        
        # Check if run function exists
        if not hasattr(module, "run"):
            raise LabLoadError(f"Lab '{name}' does not have a 'run' function")
        
        # Run the lab with optional arguments
        if args:
            return module.run(*args)  # type: ignore[no-any-return]
        return module.run()  # type: ignore[no-any-return]
        
    except ImportError as e:
        raise LabLoadError(f"Failed to import lab '{name}': {e}")
    except Exception as e:
        raise LabLoadError(f"Error running lab '{name}': {e}")
