dev:
	@python run.py --host=0.0.0.0 --port=8080 --reload

test:
	@pytest

migrate:
	@python ./migrations/createdb.py

client-dev:
	@cd web && yarn dev

clean:
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@rm -rf .pytest_cache .coverage
