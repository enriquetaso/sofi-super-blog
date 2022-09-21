#!/usr/bin/env bash
# exit on error
set -o errexit

poetry version
poetry --version
poetry update -v
poetry install -vvv

python manage.py collectstatic --no-input
python manage.py migrate

# Run the next line only once:
# python manage.py createsuperuser --noinput
