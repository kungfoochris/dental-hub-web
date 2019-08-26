#!/bin/bash
# entry.sh
# python3 manage.py migrate
python manage.py makemigrations
python manage.py migrate
gunicorn dental.wsgi:application --bind 0.0.0.0:6061
# python3 manage.py runserver 0.0.0.0:6061
 