PYTHON_VERSION := 3.11
PYTHON_GLOBAL_EXE := python$(PYTHON_VERSION)
VENV := .venv
PYTHON_VENV_EXE := $(VENV)/bin/python
PIP_VENV_EXE := $(VENV)/bin/pip
DJANGO_SETTINGS := alexandru_optica_app.settings
DJANGO_SERV_ADDR := localhost:8000



venv:
	$(PYTHON_GLOBAL_EXE) -m venv $(VENV)
.PHONY: venv

install:
	$(PIP_VENV_EXE) install -r requirements.txt
.PHONY: install

clean:
	rm -rf $(VENV)
	find . -type f -name '*.pyc' -delete
.PHONY: clean

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
