PYTEST = python3 -m pytest

PYLINT = python3 -m pylint --jobs=4
PYCODESTYLE = python3 -m pycodestyle
ISORT = python3 -m isort --check-only

PYTHON_FILES = main.py # $(shell fd '.*\.py$$')

lint:
	$(PYLINT) $(PYTHON_FILES)
	$(PYCODESTYLE) $(PYTHON_FILES)
	$(ISORT) $(PYTHON_FILES)

all: lint
