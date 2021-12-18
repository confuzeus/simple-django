FROM node:lts-bullseye-slim AS node

ARG DOCKER_BROWSERSYNC_PORT=3000

WORKDIR /app

EXPOSE $DOCKER_BROWSERSYNC_PORT

ENV PATH ./node_modules/.bin/:$PATH

COPY docker/node-entrypoint.sh /usr/local/bin/entrypoint.sh

RUN chmod +x /usr/local/bin/entrypoint.sh

USER node

ENTRYPOINT ["entrypoint.sh"]

FROM python:3.10-slim-bullseye AS piptools

ARG DOCKER_UID=1000
ARG DOCKER_GID=1000

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update && apt-get install --no-install-recommends -y \
  build-essential \
  libpq-dev

WORKDIR /app/requirements

RUN addgroup --gid $DOCKER_GID python && \
    adduser --gid $DOCKER_GID --uid $DOCKER_UID --disabled-password \
     --gecos '' python

COPY docker/piptools-compile.sh /compile
RUN sed -i 's/\r$//g' /compile
RUN chmod +x /compile

USER python

RUN pip install --user pip-tools

ENV PATH /home/python/.local/bin:$PATH

FROM python:3.10-slim-bullseye AS djangobase

ARG DOCKER_UID=1000
ARG DOCKER_GID=1000

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update && apt-get install --no-install-recommends -y \
  build-essential \
  libpq-dev \
  gettext \
  graphicsmagick \
  libjpeg-dev \
  zlib1g-dev \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

RUN addgroup --gid $DOCKER_GID django && \
    adduser --gid $DOCKER_GID --uid $DOCKER_UID --disabled-password \
     --gecos '' django

COPY requirements /app/requirements

COPY docker/django-entrypoint.sh /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

WORKDIR /app

ENV PATH /home/django/.local/bin:$PATH

FROM djangobase AS djangodebug

COPY docker/django-debug-start.sh /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY docker/piptools-compile.sh /compile
RUN sed -i 's/\r$//g' /compile
RUN chmod +x /compile

USER django

RUN pip install --user pip-tools

RUN pip-sync requirements/base.txt requirements/dev.txt --pip-args "--user"

ENTRYPOINT ["/entrypoint"]

FROM djangobase AS djangoprod

COPY docker/django-prod-start.sh /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY . /app

RUN chown -R django:django /app

USER django

RUN pip install --user pip-tools

RUN pip-sync requirements/base.txt requirements/prod.txt --pip-args "--user"

ENTRYPOINT ["/entrypoint"]