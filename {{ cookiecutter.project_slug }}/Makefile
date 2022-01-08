.PHONY: init pipcompile coverage reset dev

init:
	export COMPOSE_PROFILES=debug
	docker-compose build piptools
	docker-compose run --rm piptools /compile
	docker-compose build
	docker-compose run --rm node npm run build
	docker-compose run --rm djangodebug python manage.py collectstatic --no-input
	DJANGO_TEST=1 docker-compose run --rm djangodebug python manage.py test
	docker-compose run --rm djangodebug python manage.py migrate

pipcompile:
	docker-compose --profile debug run --rm piptools /compile

coverage:
	rm -rf htmlcov
	DJANGO_TEST=1 docker-compose --profile debug run --rm djangodebug coverage run manage.py test
	docker-compose --profile debug run --rm djangodebug coverage html
	firefox htmlcov/index.html

reset:
	docker-compose --profile debug run --rm djangodebug python manage.py reset_db
	docker-compose --profile debug run --rm djangodebug python manage.py migrate
	docker-compose --profile debug run --rm djangodebug python manage.py init_site

dev:
	docker-compose --profile debug up
