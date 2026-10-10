#!/bin/sh
# Punto de entrada común: «web» levanta Gunicorn y «scheduler» levanta cron.
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
      --timeout 60 \
      --access-logfile - \
      --error-logfile -
    ;;
  scheduler)
    # cron no hereda el entorno del contenedor: se guarda para las tareas.
    python -c "import os, shlex; print('\n'.join(f'export {k}={shlex.quote(v)}' for k, v in os.environ.items() if k.startswith(('DJANGO', 'POSTGRES', 'SIREMA', 'TZ'))))" > /etc/sirema.env
    chmod 0600 /etc/sirema.env
    # Al volver de un corte de luz, recupera las fechas omitidas (CU-C4, curso 1.a).
    python manage.py generar_revisiones || true
    exec cron -f
    ;;
  *)
    exec "$@"
    ;;
esac
