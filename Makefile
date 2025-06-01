install:
	@pip install -e ".[testing]"
	@cd web && yarn install

dev:
	@pserve development.ini --reload

client-dev:
	@cd web && yarn dev

test:
	@pytest

clean:
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@rm -rf .pytest_cache .coverage
