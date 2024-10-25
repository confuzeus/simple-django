### BUILD Stage

FROM python:3.12-bookworm AS build

RUN <<EOT
apt-get update -qy
apt-get install -qyy \
    -o APT::Install-Recommends=false \
    -o APT::Install-Suggests=false \
    build-essential \
    ca-certificates \
    python3-setuptools \
    python3-dev
EOT

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin

ENV UV_COMPILE_BYTECODE=1 \
    UV_PROJECT_ENVIRONMENT=/app/venv

COPY pyproject.toml /requirements/
COPY uv.lock /requirements/

RUN --mount=type=cache,target=/root/.cache <<EOT
cd /requirements
uv sync \
    --locked \
    --no-dev \
    --no-editable \
    --no-install-project \
    --extra prod
EOT

### Final stage

FROM python:3.12-slim-bookworm

RUN <<_EOF
apt-get update -qy
apt-get install -qyy \
    -o APT::Install-Recommends=false \
    -o APT::Install-Suggests=false \
    ca-certificates \
    sqlite3
apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false
rm -rf /var/lib/apt/lists/*
_EOF

COPY --from=build /app/venv/ /app/venv/
COPY . /app

RUN chmod +x /app/gunicorn-docker-cmd

WORKDIR /app

EXPOSE 8000

RUN <<_EOF
groupadd -g 700 -r simple_django
useradd -g 700 -u 700 -r simple_django
_EOF

USER simple_django

CMD ["echo", "Specify a default command."]

