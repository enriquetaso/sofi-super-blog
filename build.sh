#!/usr/bin/env bash
# exit on error
set -o errexit

poetry version
poetry --version
poetry update -v
poetry install -vvv

python manage.py collectstatic --no-input
python manage.py migrate
python manage.py createsuperuser --noinput --username $DJANGO_SUPERUSER_USERNAME --email $DJANGO_SUPERUSER_EMAIL --password $DJANGO_SUPERUSER_PASSWORD
