.PHONY: help install test lint format clean run docker-build docker-run docker-stop

help:
	@echo "Open Cyber Lab - Make Commands"
	@echo ""
	@echo "Available commands:"
	@echo "  make install      - Install dependencies"
	@echo "  make test        - Run tests"
	@echo "  make lint        - Run linters"
	@echo "  make format      - Format code"
	@echo "  make clean       - Clean temporary files"
	@echo "  make run         - Run the application"
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-run   - Run Docker container"
	@echo "  make docker-stop  - Stop Docker container"

install:
	pip install -e ".[dev]"

test:
	pytest -v --cov=cyberlab --cov=labs

test-coverage:
	pytest --cov=cyberlab --cov=labs --cov-report=html --cov-report=xml

lint:
	ruff check .
	black --check .

format:
	black .
	ruff check --fix .

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .ruff_cache htmlcov *.egg-info build dist

run:
	python cyberlab.py --help

docker-build:
	docker build -t open-cyber-lab .

docker-run:
	docker run -it --rm open-cyber-lab

docker-stop:
	docker stop $$(docker ps -q --filter ancestor=open-cyber-lab) 2>/dev/null || true

security:
	ruff check . --select=SEC

pre-commit:
	pre-commit install
	pre-commit run --all-files
