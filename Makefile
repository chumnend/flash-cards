.PHONY: help install install-dev dev test clean migrate check fix

# Default target
help:
	@echo "Available commands:"
	@echo "  Development:"
	@echo "    install       - Install Python dependencies"
	@echo "    dev          - Run development server"
	@echo ""
	@echo "  Testing:"
	@echo "    test         - Run backend tests"
	@echo ""
	@echo "  Database:"
	@echo "    migrate       - Drop and recreate database"
	@echo ""
	@echo "  Code Quality:"
	@echo "    check         - Check code quality (formatting, linting, type checking)"
	@echo "    fix           - Format code and run all quality checks"
	@echo ""
	@echo "  Utilities:"
	@echo "    clean         - Clean cache and build files"

# Development
install:
	@echo "Installing Python dependencies..."
	@poetry install

dev:
	@echo "Starting development server..."
	@python run.py --reload

# Testing
test:
	@echo "Running backend tests..."
	@pytest -v

# Manage database
migrate:
	@echo "Dropping and recreating database..."
	@python ./migrations/scripts/dropdb.py && python ./migrations/scripts/createdb.py

# Code quality
check:
	@echo "Running code quality checks..."
	@echo "Checking code formatting with Black..."
	@poetry run black --check flashly/ tests/ migrations/
	@echo "Linting code with Flake8..."
	@poetry run flake8 flashly/ tests/ migrations/
	@echo "Type checking with MyPy..."
	@poetry run mypy flashly/
	@echo "All code quality checks passed!"

fix:
	@echo "Formatting code with Black..."
	@poetry run black flashly/ tests/ migrations/
	@echo "Running code quality checks..."
	@echo "Checking code formatting with Black..."
	@poetry run black --check flashly/ tests/ migrations/
	@echo "Linting code with Flake8..."
	@poetry run flake8 flashly/ tests/ migrations/
	@echo "Type checking with MyPy..."
	@poetry run mypy flashly/
	@echo "Code formatted and all checks passed!"

# Development setup
clean:
	@echo "Cleaning cache and build files..."
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@rm -rf .pytest_cache .coverage
