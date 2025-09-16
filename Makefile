venv:
	@python -m virtualenv venv
	@source ./venv/bin/activate

dev:
	@python run.py --host=0.0.0.0 --port=8080 --reload

test:
	@pytest

client-dev:
	@cd web && yarn dev

clean:
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@rm -rf .pytest_cache .coverage
