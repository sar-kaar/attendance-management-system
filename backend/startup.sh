#!/bin/bash
cd /home/site/wwwroot
python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py seed_data 2>/dev/null || true
gunicorn config.wsgi:application --bind 0.0.0.0:8000
