# Open Cyber Lab

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.0-orange)](pyproject.toml)

![Open Cyber Lab](Open_cyber_lab.png)

Open Cyber Lab is an open-source Python project for learning cybersecurity through interactive labs.

> **⚠️ Disclaimer**: This project is for educational purposes only. Always obtain proper authorization before testing or using cybersecurity techniques.

## Features

- 🔐 **SQL Injection Lab** - Learn about SQL injection vulnerabilities
- 🔑 **Password Cracking Lab** - Understand dictionary attacks and password security
- 🏗️ **Modular Architecture** - Easy to add new labs
- 🎯 **Interactive Learning** - Hands-on exercises with validation
- 📊 **Progress Tracking** - Clear objectives and feedback

## Installation

### Prerequisites

- Python 3.8 or higher

### Quick Install

```bash
# Clone the repository
git clone https://github.com/donaldozoubery/open-cyber-lab.git
cd open-cyber-lab

# Install dependencies
pip install -r requirements.txt
```

## Usage

### List Available Labs

```bash
python cyberlab.py list
```

Output:
```
=== Available Labs ===

  • password_cracking
  • sql_injection

Total: 2 lab(s)
```

### Run a Lab

```bash
python cyberlab.py run sql_injection
python cyberlab.py run password_cracking
python cyberlab.py run password_cracking medium  # with wordlist size
```

### Get Lab Information

```bash
python cyberlab.py info sql_injection
python cyberlab.py info password_cracking
```

### Show Version

```bash
python cyberlab.py --version
```

## Adding New Labs

1. Create a new Python file in the [`labs/`](labs/) directory
2. Implement a `run(*args)` function
3. Optionally add metadata:
   - `DIFFICULTY` - Lab difficulty level
   - `OBJECTIVES` - List of learning objectives

### Example Lab Template

```python
"""
My New Lab

Description of what this lab teaches.
"""

DIFFICULTY = "Intermediate"

OBJECTIVES = [
    "Learn objective 1",
    "Learn objective 2"
]

def run(*args):
    """Run the lab."""
    print("Hello from my new lab!")
    return True
```

## Project Structure

```
open-cyber-lab/
├── cyberlab/              # Main package
│   ├── __init__.py       # Package initialization
│   ├── cli.py            # Command-line interface
│   └── lab_loader.py    # Lab loading utilities
├── labs/                  # Cybersecurity labs
│   ├── sql_injection.py
│   └── password_cracking.py
├── pyproject.toml        # Project configuration
├── requirements.txt      # Dependencies
└── README.md            # This file
```

## Configuration

### Environment Variables

- `CYBERLAB_LABS_DIR` - Override the labs directory (default: `labs`)

```bash
export CYBERLAB_LABS_DIR=my_custom_labs
```

## Development

### Install Development Dependencies

```bash
pip install -e ".[dev]"
```

### Run Tests

```bash
pytest
```

### Code Formatting

```bash
black .
ruff check .
```

## Exit Codes

| Code | Description |
|------|-------------|
| 0   | Success |
| 1   | General error |
| 2   | Lab not found |
| 3   | Lab load error |
| 4   | Invalid argument |

## Contributing

Contributions are welcome! Please read our [contributing guidelines](CONTRIBUTING.md) first.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

- **Jaotiana Donaldo ZOUBERY**

## Acknowledgments

- Thanks to all contributors
- Inspired by OWASP educational materials

## Security

If you discover a security vulnerability, please report it responsibly.

## Contact
For questions or feedback, please open an issue on GitHub.

## ⭐ Star the repo if you like the project
---

<p align="center">
  Made with 🔒 for cybersecurity education
</p>
