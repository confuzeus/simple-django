.PHONY: init install-dev-deps coverage reset fixtures fmt lfmt services \
	stop-services serve-django shell migrate

SHELL := /bin/bash

init: install-dev-deps
	npm install
	npm run build
	poetry run python manage.py collectstatic --no-input
	poetry run python manage.py test
	poetry run python manage.py migrate

install-dev-deps:
	poetry install --with dev

coverage:
	rm -rf htmlcov
	DJANGO_TEST=1 poetry run coverage run manage.py test
	poetry run coverage html
	firefox htmlcov/index.html

reset:
	poetry run python manage.py reset_db
	poetry run python manage.py migrate

fixtures:
	poetry run python manage.py init_site

fmt:
	@poetry run black --exclude __pycache__  config
	@poetry run black --exclude __pycache__ --exclude migrations simple_django
	@poetry run isort --skip migrations --skip __pycache__ simple_django
	@poetry run isort --skip __pycache__ config
	@poetry run djhtml -i templates/**/*.html
	@npx prettier --write staticSrc/js

lint:
	@poetry run flake8 config
	@poetry run flake8 simple_django

fmtl: fmt lint

services:
	docker-compose up -d

stop-services:
	docker-compose down

serve-django:
	poetry run python manage.py runserver_plus --keep-meta-shutdown

shell:
	poetry run python manage.py shell_plus

migrate:
	poetry run python manage.py migrate

