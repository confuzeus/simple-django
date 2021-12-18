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
	python manage.py init_site
	python manage.py init_membership
	python manage.py createsuperuser

runserver:
	python manage.py runserver_plus

runserverhttps:
	python manage.py runserver_plus --cert-file ./ssl/server.crt --key-file ./ssl/server.key

dev:
	npm run dev

devhttps:
	BROWSERSYNC_HTTPS=true npm run dev
