#!/bin/sh
set -e
cd /app

case "$1" in
  web)
    python manage.py migrate --noinput
    python manage.py collectstatic --noinput --verbosity 0
    python manage.py crear_administrador
    exec gunicorn config.wsgi:application \
      --bind 0.0.0.0:8000 \
      --workers "${GUNICORN_WORKERS:-3}" \
      --timeout "${GUNICORN_TIMEOUT:-900}" \
      --access-logfile - \
      --error-logfile -
    ;;
  scheduler)
    python -c "import os, shlex; print('\n'.join(f'export {k}={shlex.quote(v)}' for k, v in os.environ.items() if k.startswith(('DJANGO', 'POSTGRES', 'SIREMA', 'TZ'))))" > /etc/sirema.env
    chmod 0600 /etc/sirema.env
    python manage.py generar_revisiones || true
    exec cron -f
    ;;
  *)
    exec "$@"
    ;;
esac
