# Contributing to Open Cyber Lab

Thank you for your interest in contributing!

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/open-cyber-lab.git`
3. Add upstream: `git remote add upstream https://github.com/donaldozoubery/open-cyber-lab.git`
4. Create a branch from `dev`: `git checkout -b dev` then `git checkout -b feature/your-feature`

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

1. Make sure you're on `dev` branch: `git checkout dev`
2. Create your feature branch: `git checkout -b feature/your-feature`
3. Make your changes and commit
4. Push to your fork
5. Open a pull request to `dev` branch (NOT to `main`)
6. Ensure all CI checks pass
7. Wait for review
8. After merge to `dev`, the maintainer will merge to `main` for release

## Important Notes

- **Do NOT** merge directly to `main`
- All contributions go through `dev` branch
- Use **Squash merge** or **Rebase merge** when merging PRs

## Reporting Issues

- Use GitHub Issues
- Describe the problem clearly
- Include steps to reproduce

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
