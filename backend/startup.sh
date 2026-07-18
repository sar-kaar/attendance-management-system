#!/bin/bash
cd /home/site/wwwroot
source antenv/bin/activate
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --timeout 120
