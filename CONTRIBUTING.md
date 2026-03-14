# Contributing to Open Cyber Lab

Thank you for your interest in contributing!

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/open-cyber-lab.git`
3. Create a branch: `git checkout -b feature/your-feature`

## Development Setup

```bash
# Clone and setup
git clone https://github.com/donaldozoubery/open-cyber-lab.git
cd open-cyber-lab

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

## Adding New Labs

1. Create a new Python file in `labs/` directory
2. Implement a `run(*args)` function
3. Add metadata:
   - `DIFFICULTY` - "Beginner", "Intermediate", or "Advanced"
   - `OBJECTIVES` - List of learning objectives
4. Add docstring with description

### Lab Template

```python
"""
[Lab Name] Lab

Learn about [topic].

DISCLAIMER: This lab is for educational purposes only.
"""

DIFFICULTY = "Beginner"

OBJECTIVES = [
    "Objective 1",
    "Objective 2"
]

def run(*args):
    """Run the lab."""
    print("Hello from the lab!")
    return True
```

## Code Style

- Follow PEP 8
- Use type hints
- Run linters: `ruff check . && black .`
- Write tests for new features

## Pull Request Process

1. Update documentation if needed
2. Add tests for new features
3. Ensure all tests pass
4. Update CHANGELOG.md
5. Submit a pull request

## Reporting Issues

- Use GitHub Issues
- Describe the problem clearly
- Include steps to reproduce

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
