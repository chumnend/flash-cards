dev:
	@python run.py --host=0.0.0.0 --port=8080 --reload

test:
	@pytest

migrate:
	@python ./migrations/scripts/dropdb.py && python ./migrations/scripts/createdb.py

createdb:
	@python ./migrations/scripts/createdb.py

dropdb:
	@python ./migrations/scripts/dropdb.py

client-dev:
	@cd flashly-client && yarn dev

clean:
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@rm -rf .pytest_cache .coverage
