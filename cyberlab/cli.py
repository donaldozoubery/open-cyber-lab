"""Command-line interface for Open Cyber Lab."""

import sys
import argparse

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False
    # Fallback colors (empty strings)
    class _Fore:
        CYAN = GREEN = RED = YELLOW = MAGENTA = ""
    class _Style:
        BRIGHT = DIM = RESET_ALL = ""
    Fore = _Fore()
    Style = _Style()

from cyberlab import __version__
from cyberlab.lab_loader import (
    list_labs,
    run_lab,
    get_lab_info,
    LabError,
    LabNotFoundError,
    LabLoadError,
    LabValidationError,
)
from cyberlab.progress import ProgressTracker


# Exit codes
EXIT_SUCCESS: int = 0
EXIT_GENERAL_ERROR: int = 1
EXIT_LAB_NOT_FOUND: int = 2
EXIT_LAB_LOAD_ERROR: int = 3
EXIT_INVALID_ARGUMENT: int = 4


def print_error(message: str) -> None:
    """Print an error message to stderr."""
    if COLORAMA_AVAILABLE:
        print(f"{Fore.RED}Error:{Style.RESET_ALL} {message}", file=sys.stderr)
    else:
        print(f"Error: {message}", file=sys.stderr)


def print_success(message: str) -> None:
    """Print a success message."""
    if COLORAMA_AVAILABLE:
        print(f"{Fore.GREEN}Success:{Style.RESET_ALL} {message}")
    else:
        print(f"Success: {message}")


def print_info(message: str) -> None:
    """Print an info message."""
    if COLORAMA_AVAILABLE:
        print(f"{Fore.CYAN}Info:{Style.RESET_ALL} {message}")
    else:
        print(f"Info: {message}")


def print_header(message: str) -> None:
    """Print a header message."""
    if COLORAMA_AVAILABLE:
        print(f"{Fore.MAGENTA}{Style.BRIGHT}{message}{Style.RESET_ALL}")
    else:
        print(f"=== {message} ===")


class Args:
    """Simple args container for type hints."""
    command: str
    lab_name: str
    args: list[str]


def cmd_list(args: Args) -> int:
    """List all available labs.
    
    Args:
        args: Parsed command-line arguments
        
    Returns:
        int: Exit code
    """
    try:
        labs = list_labs()
        
        if not labs:
            print_info("No labs found. Add new labs to the 'labs' directory.")
            return EXIT_SUCCESS
        
        print_header("Available Labs")
        print()
        
        for lab in labs:
            print(f"  {Fore.CYAN}•{Style.RESET_ALL} {lab}")
        
        print()
        print_info(f"Total: {len(labs)} lab(s)")
        
        return EXIT_SUCCESS
        
    except LabError as e:
        print_error(str(e))
        return EXIT_GENERAL_ERROR


def cmd_run(args: Args) -> int:
    """Run a specific lab.
    
    Args:
        args: Parsed command-line arguments
        
    Returns:
        int: Exit code
    """
    lab_name = args.lab_name
    
    try:
        print_header(f"Running Lab: {lab_name}")
        print()
        
        # Pass additional arguments to the lab
        lab_args = args.args if hasattr(args, 'args') else []
        run_lab(lab_name, *lab_args)
        
        print()
        print_success("Lab completed!")
        
        # Track progress
        tracker = ProgressTracker()
        if not tracker.is_completed(lab_name):
            tracker.complete_lab(lab_name)
            print_info(f"Progress saved: '{lab_name}' marked as completed!")
        
        return EXIT_SUCCESS
        
    except LabNotFoundError as e:
        print_error(str(e))
        print_info("Run 'python cyberlab.py list' to see available labs.")
        return EXIT_LAB_NOT_FOUND
        
    except LabLoadError as e:
        print_error(str(e))
        return EXIT_LAB_LOAD_ERROR
        
    except LabValidationError as e:
        print_error(str(e))
        return EXIT_INVALID_ARGUMENT
        
    except KeyboardInterrupt:
        print()
        print_info("Lab interrupted by user.")
        return EXIT_GENERAL_ERROR
        
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        return EXIT_GENERAL_ERROR


def cmd_info(args: Args) -> int:
    """Show information about a specific lab.
    
    Args:
        args: Parsed command-line arguments
        
    Returns:
        int: Exit code
    """
    lab_name = args.lab_name
    
    try:
        info = get_lab_info(lab_name)
        
        print_header(f"Lab: {info['name']}")
        print()
        print(info['description'])
        
        if 'difficulty' in info:
            print()
            print(f"Difficulty: {info['difficulty']}")
        
        if 'objectives' in info:
            print()
            print("Objectives:")
            for obj in info['objectives']:
                print(f"  {Fore.CYAN}•{Style.RESET_ALL} {obj}")
        
        # Show completion status
        tracker = ProgressTracker()
        if tracker.is_completed(lab_name):
            print()
            print(f"{Fore.GREEN}✓ Completed{Style.RESET_ALL}")
        
        return EXIT_SUCCESS
        
    except LabNotFoundError as e:
        print_error(str(e))
        return EXIT_LAB_NOT_FOUND
        
    except Exception as e:
        print_error(str(e))
        return EXIT_GENERAL_ERROR


def cmd_progress(args: Args) -> int:
    """Show user progress.
    
    Args:
        args: Parsed command-line arguments
        
    Returns:
        int: Exit code
    """
    try:
        tracker = ProgressTracker()
        stats = tracker.get_statistics()
        completed = tracker.get_completed_labs()
        all_labs = list_labs()
        
        print_header("Your Progress")
        print()
        
        # Progress bar
        total = len(all_labs)
        done = len(completed)
        percentage = int((done / total) * 100) if total > 0 else 0
        
        bar_length = 30
        filled = int((done / total) * bar_length) if total > 0 else 0
        bar = f"{Fore.GREEN}{'█' * filled}{Fore.RED}{'░' * (bar_length - filled)}{Style.RESET_ALL}"
        
        print(f"Progress: [{bar}] {percentage}%")
        print()
        
        print(f"Completed: {done}/{total} labs")
        print(f"Total attempts: {stats['total_attempts']}")
        
        if stats['total_time_spent'] > 0:
            minutes = stats['total_time_spent'] // 60
            print(f"Time spent: {minutes} minutes")
        
        if completed:
            print()
            print("Completed labs:")
            for lab in completed:
                print(f"  {Fore.GREEN}✓{Style.RESET_ALL} {lab}")
        
        # Show remaining labs
        remaining = [lab for lab in all_labs if lab not in completed]
        if remaining:
            print()
            print("Remaining labs:")
            for lab in remaining:
                print(f"  {Fore.CYAN}○{Style.RESET_ALL} {lab}")
        
        return EXIT_SUCCESS
        
    except Exception as e:
        print_error(str(e))
        return EXIT_GENERAL_ERROR


def cmd_reset(args: Args) -> int:
    """Reset user progress.
    
    Args:
        args: Parsed command-line arguments
        
    Returns:
        int: Exit code
    """
    try:
        tracker = ProgressTracker()
        
        print_warning = input("Are you sure you want to reset all progress? (yes/no): ")
        
        if print_warning.lower() == "yes":
            tracker.reset_progress()
            print_success("Progress reset successfully!")
        else:
            print_info("Reset cancelled.")
        
        return EXIT_SUCCESS
        
    except Exception as e:
        print_error(str(e))
        return EXIT_GENERAL_ERROR


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser."""
    parser = argparse.ArgumentParser(
        prog="cyberlab",
        description="Open Cyber Lab - Learn cybersecurity through interactive labs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  cyberlab list                  List all available labs
  cyberlab run sql_injection     Run the SQL injection lab
  cyberlab info sql_injection    Show info about the SQL injection lab
  cyberlab progress              Show your progress
  cyberlab reset                 Reset all progress
  cyberlab --version             Show version information

For more information, visit: https://github.com/jaotiana/open-cyber-lab
"""
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # List command
    subparsers.add_parser(
        "list",
        help="List all available labs",
        description="Display a list of all available cybersecurity labs."
    )
    
    # Run command
    run_parser = subparsers.add_parser(
        "run",
        help="Run a specific lab",
        description="Execute a cybersecurity lab by name."
    )
    run_parser.add_argument(
        "lab_name",
        help="Name of the lab to run"
    )
    run_parser.add_argument(
        "args",
        nargs="*",
        help="Optional arguments to pass to the lab"
    )
    
    # Info command
    info_parser = subparsers.add_parser(
        "info",
        help="Show information about a lab",
        description="Display detailed information about a specific lab."
    )
    info_parser.add_argument(
        "lab_name",
        help="Name of the lab to show info about"
    )
    
    # Progress command
    subparsers.add_parser(
        "progress",
        help="Show your progress",
        description="Display your learning progress and statistics."
    )
    
    # Reset command
    subparsers.add_parser(
        "reset",
        help="Reset your progress",
        description="Reset all progress data."
    )
    
    return parser


def main() -> int:
    """Main entry point for the CLI.
    
    Returns:
        int: Exit code
    """
    parser = create_parser()
    args = parser.parse_args()
    
    # Handle no command
    if args.command is None:
        parser.print_help()
        return EXIT_SUCCESS
    
    # Route to appropriate command handler
    if args.command == "list":
        return cmd_list(args)
    elif args.command == "run":
        return cmd_run(args)
    elif args.command == "info":
        return cmd_info(args)
    elif args.command == "progress":
        return cmd_progress(args)
    elif args.command == "reset":
        return cmd_reset(args)
    else:
        print_error(f"Unknown command: {args.command}")
        return EXIT_GENERAL_ERROR


if __name__ == "__main__":
    sys.exit(main())
