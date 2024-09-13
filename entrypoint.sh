#!/bin/bash

set -e

python manage.py migrate --no-input
python manage.py collectstatic --no-input

gunicorn application.config.wsgi:application --bind 0.0.0.0:8080 --reload