.PHONY: init
init: 
	@pipenv install --three -r requirements.txt

.PHONY: start
start:
	gunicorn flashcards:app

.PHONY: dev 
dev: export FLASK_ENV=development
dev: 
	flask run

.PHONY: test
test:
	@python -m unittest discover
