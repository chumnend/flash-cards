.PHONY: help install install-dev install-client build dev prod test test-backend test-frontend clean migrate createdb dropdb format format-check lint type-check check fix

# Default target
help:
	@echo "Available commands:"
	@echo "  Development:"
	@echo "    install        - Install Python dependencies"
	@echo "    install-dev    - Install Python dev dependencies"
	@echo "    install-client - Install client dependencies"
	@echo "    dev           - Run development servers (React + Python)"
	@echo "    dev-backend   - Run backend development server only"
	@echo "    dev-client    - Run client development server only"
	@echo ""
	@echo "  Production:"
	@echo "    build         - Build client for production"
	@echo "    prod          - Build client and start production server"
	@echo ""
	@echo "  Testing:"
	@echo "    test          - Run all tests"
	@echo "    test-backend  - Run backend tests only"
	@echo "    test-frontend - Run frontend tests only"
	@echo ""
	@echo "  Database:"
	@echo "    migrate       - Drop and recreate database"
	@echo "    createdb      - Create database"
	@echo "    dropdb        - Drop database"
	@echo ""
	@echo "  Code Quality:"
	@echo "    format        - Format code with Black"
	@echo "    format-check  - Check code formatting"
	@echo "    lint          - Lint code with Flake8"
	@echo "    type-check    - Type check with MyPy"
	@echo "    check         - Run all quality checks"
	@echo "    fix           - Format and run all checks"
	@echo ""
	@echo "  Utilities:"
	@echo "    clean         - Clean cache and build files"

# Installation
install:
	@echo "Installing Python dependencies..."
	@poetry install

install-dev:
	@echo "Installing Python dev dependencies..."
	@poetry install --with dev

install-client:
	@echo "Installing client dependencies..."
	@cd flashly/client && npm install

# Development
dev: install-client
	@echo "Starting development servers..."
	@concurrently \
		--names "BACKEND,FRONTEND" \
		--prefix-colors "blue,green" \
		"python run.py --reload" \
		"cd flashly/client && npm run dev"

dev-backend:
	@echo "Starting backend development server..."
	@python run.py --reload

dev-client: install-client
	@echo "Starting client development server..."
	@cd flashly/client && npm run dev

# Production
build: install-client
	@echo "Building client for production..."
	@cd flashly/client && npm run build

prod: build
	@echo "Starting production server..."
	@python run.py

# Testing
test: test-backend test-frontend

test-backend:
	@echo "Running backend tests..."
	@pytest -v

test-frontend: install-client
	@echo "Running frontend tests..."
	@cd flashly/client && npm test

# Manage database
migrate:
	@echo "Dropping and recreating database..."
	@python ./migrations/scripts/dropdb.py && python ./migrations/scripts/createdb.py

createdb:
	@echo "Creating database..."
	@python ./migrations/scripts/createdb.py

dropdb:
	@echo "Dropping database..."
	@python ./migrations/scripts/dropdb.py

# Code formatting and linting
format:
	@echo "Formatting code with Black..."
	@poetry run black flashly/ tests/ migrations/

format-check:
	@echo "Checking code formatting with Black..."
	@poetry run black --check flashly/ tests/ migrations/

lint:
	@echo "Linting code with Flake8..."
	@poetry run flake8 flashly/ tests/ migrations/

type-check:
	@echo "Type checking with MyPy..."
	@poetry run mypy flashly/

check: format-check lint type-check
	@echo "All code quality checks passed!"

fix: format check
	@echo "Code formatted and all checks passed!"

# Development setup
clean:
	@echo "Cleaning cache and build files..."
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type d -name "node_modules" -exec rm -rf {} +
	@rm -rf .pytest_cache .coverage
	@rm -rf flashly/client/dist flashly/client/.vite
