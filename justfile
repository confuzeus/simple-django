@init:
  uv sync
  mkdir -p static/{js,css,images}
  pnpm install
  pnpm build
  python manage.py collectstatic --no-input
  python manage.py createcachetable
  python manage.py migrate

@reset:
  python manage.py reset_db
  python manage.py migrate

@fixtures:
  python manage.py init_site

@fmt:
  uv tool run ruff --format simple_django
  uv tool run djlint templates
  pnpm exec prettier --write staticSrc/js staticSrc/scss

@lint:
  uv tool run ruff check --fix simple_django
  pnpm js-lint

@fmtl: fmt lint

@server-django:
  python manage.py runserver_plus --keep-meta-shutdown

@shell:
  python manage.py shell_plus

@migrate:
  python manage.py migrate

@mailhog:
  podman run -p "127.0.0.1:1025:1025" -p "127.0.0.1:8025:8025" docker://mailhog/mailhog

@build-image:
  podman build --tag simple_django:latest .