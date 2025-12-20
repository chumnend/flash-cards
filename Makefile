# Pyramid backed
dev:
	@python run.py --host=0.0.0.0 --port=8080 --reload

test:
	@pytest

# Manage database
migrate:
	@python ./migrations/scripts/dropdb.py && python ./migrations/scripts/createdb.py

createdb:
	@python ./migrations/scripts/createdb.py

dropdb:
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

# React frontend
client-dev:
	@cd flashly-client && yarn dev

# Development setup
clean:
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@rm -rf .pytest_cache .coverage
