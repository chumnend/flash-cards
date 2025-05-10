VENV_DIR = venv
PYTHON = python3
PIP = $(VENV_DIR)/bin/pip
PYTEST = $(VENV_DIR)/bin/pytest
PSERVE = $(VENV_DIR)/bin/pserve

all: install

venv:
	$(PYTHON) -m virtualenv $(VENV_DIR)

upgrade-tools: venv
	$(PIP) install --upgrade pip setuptools

install: upgrade-tools
	$(PIP) install -e ".[testing]"

test:
	$(PYTEST)

run:
	$(PSERVE) development.ini --reload

clean:
	rm -rf $(VENV_DIR)
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

