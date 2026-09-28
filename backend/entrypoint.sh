#!/bin/sh

chmod +x entrypoint.sh

python manage.py makemigrations
python manage.py migrate --no-input


echo "Running collectstatic for Django Admin and backend assets..."
python manage.py collectstatic --no-input

gunicorn config.wsgi:application --bind 0.0.0.0:8000 --reload