#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
python manage.py cargar_datos

# Crea el superusuario si están definidas las variables DJANGO_SUPERUSER_*.
# Si ya existe, el comando falla y el "|| true" evita que se corte el deploy.
python manage.py createsuperuser --noinput || true