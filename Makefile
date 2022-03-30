.PHONY: init \ pipcompile pipsync coverage reset fixtures fmt lfmt services \
	stop-services serve-django serve-worker shell migrate

SHELL := /bin/bash

init: pipcompile pipsync
	npm install
	npm run build
	python manage.py collectstatic --no-input
	python manage.py test
	python manage.py migrate

pipcompile:
	pip-compile --upgrade --generate-hashes --output-file requirements/base.txt requirements/base.in
	pip-compile --upgrade --generate-hashes --output-file requirements/dev.txt requirements/dev.in
	pip-compile --upgrade --generate-hashes --output-file requirements/prod.txt requirements/prod.in

pipsync:
	pip-sync requirements/base.txt requirements/dev.txt

coverage:
	rm -rf htmlcov
	DJANGO_TEST=1 coverage run manage.py test
	coverage html
	firefox htmlcov/index.html

reset:
	python manage.py reset_db
	python manage.py migrate

fixtures:
	python manage.py init_site

fmt:
	black .
	isort .

lint:
	flake8

lfmt: fmt lint

services:
	docker-compose up -d

stop-services:
	docker-compose down

serve-django:
	python manage.py runserver_plus

serve-worker:
	python manage.py qcluster

shell:
	python manage.py shell_plus

migrate:
	python manage.py migrate

