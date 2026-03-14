"""
Open Cyber Lab - Cybersecurity Learning Platform

An open-source project for learning cybersecurity through interactive labs.
"""

__version__ = "1.0.0"
__author__ = "Jaotiana Donaldo ZOUBERY"
__license__ = "MIT"

from cyberlab.lab_loader import list_labs, run_lab

__all__ = ["list_labs", "run_lab", "__version__"]
