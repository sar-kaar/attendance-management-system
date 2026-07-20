#!/bin/bash
cd /home/site/wwwroot
# Try to find and activate the virtualenv
for venv in antenv venv .venv env; do
    if [ -f "$venv/bin/activate" ]; then
        source "$venv/bin/activate"
        break
    fi
done
python manage.py migrate --noinput
python manage.py collectstatic --noinput
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --timeout 120
