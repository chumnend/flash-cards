install:
	@pip install -e ".[testing]"

dev:
	@pserve development.ini --reload

client:
	@cd web && yarn install && yarn run dev

test:
	@pytest

clean:
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@rm -rf .pytest_cache .coverage
