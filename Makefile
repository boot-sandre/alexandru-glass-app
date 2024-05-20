PYTHON_VERSION := 3.12
PYTHON_BLACK_VERSION := py312
PYTHON_GLOBAL_EXE := python$(PYTHON_VERSION)
VENV := .venv
PYTHON_VENV_EXE := $(VENV)/bin/python
PIP_VENV_EXE := $(VENV)/bin/pip
BLACK_VENV_EXE := $(VENV)/bin/black
FLAKE_VENV_EXE := $(VENV)/bin/flake8
ISORT_VENV_EXE := $(VENV)/bin/isort
PYTEST_VENV_EXE := $(VENV)/bin/pytest
DJANGO_SETTINGS := alexandru_optica_app.settings.development
DJANGO_SETTINGS_TEST := alexandru_optica_app.settings.testing
DJANGO_SERV_ADDR := localhost:8000
DB_DEV := db.sqlite3
NPM_EXE := npm


venv:
	$(PYTHON_GLOBAL_EXE) -m venv $(VENV)
.PHONY: venv

install: venv
	$(PIP_VENV_EXE) install -r requirements.txt
.PHONY: install

install_dev: venv
	$(PIP_VENV_EXE) install -r requirements-dev.txt -r requirements.txt
.PHONY: install_dev

static:
	mkdir -p static
.PHONY: static

install_front: static
	npm install
.PHONY: install_front

front_build:
	npm run dev
	$(PYTHON_VENV_EXE) manage.py collectstatic --settings=$(DJANGO_SETTINGS)  --noinput -c -l -v 2
.PHONY: front_build

clean_front:
	rm -rf node_modules/
	rm -rf static/
.PHONY: clean_front

freeze_requirements: venv
	$(PIP_VENV_EXE) freeze --all > requirements-freeze.txt
.PHONY: freeze_requirements

clean: clean_front
	rm -rf $(VENV)
	find . -type f -name '*.pyc' -delete
.PHONY: clean

clean_db:
	rm $(DB_DEV)

migrations:
	$(PYTHON_VENV_EXE) manage.py makemigrations --settings=$(DJANGO_SETTINGS)
.PHONY: makemigrations

migrate:
	$(PYTHON_VENV_EXE) manage.py migrate --settings=$(DJANGO_SETTINGS)
.PHONY: migrate

superuser:
	$(PYTHON_VENV_EXE) manage.py createsuperuser --settings=$(DJANGO_SETTINGS)
.PHONY: superuser

run:
	$(PYTHON_VENV_EXE) manage.py runserver --settings=$(DJANGO_SETTINGS) $(DJANGO_SERV_ADDR)
.PHONY: run

shell:
	$(PYTHON_VENV_EXE) manage.py shell --settings=$(DJANGO_SETTINGS)
.PHONY: shell

black_diff:
	$(BLACK_VENV_EXE) -t $(PYTHON_BLACK_VERSION) --diff .
.PHONY: black_diff

black_apply:
	$(BLACK_VENV_EXE) -t $(PYTHON_BLACK_VERSION) .
.PHONY: black_apply

flake:
	$(FLAKE_VENV_EXE) .
.PHONY: flake

isort:
	$(ISORT_VENV_EXE) .
.PHONY: isort

tests:
	$(PYTEST_VENV_EXE) -s -vv tests/
.PHONY: tests

tests_lf:
	$(PYTEST_VENV_EXE) -s -vv --lf tests/
.PHONY: tests_lf

tests_lf_pdb:
	$(PYTEST_VENV_EXE) -s -vv --lf --pdb tests/
.PHONY: tests_lf_pdb

qa: black_diff flake
.PHONY: qa

ci: qa tests
.PHONY: ci

ci_full: clean install install_dev install_front front_build qa tests
.PHONY: ci_full

