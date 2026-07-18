#!/bin/bash
cd /home/site/wwwroot
pip install -r requirements.txt
python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py seed_data || true
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --timeout 120
