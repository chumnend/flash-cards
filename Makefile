.PHONY: init
init: 
	@pipenv install --three -r requirements.txt

.PHONY: start
start:
	@flask run

.PHONY: test
test:
	@python -m unittest discover
