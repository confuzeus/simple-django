#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

python manage.py collectstatic --noinput
gunicorn config.asgi --bind 0.0.0.0:$DOCKER_DJANGO_PORT --chdir=/app -k uvicorn.workers.UvicornWorker