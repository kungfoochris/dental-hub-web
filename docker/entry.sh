#!/bin/bash
# entry.sh
python3 manage.py migrate
python3 manage.py makemigrations
python3 manage.py migrate
gunicorn dental.wsgi:application --bind 0.0.0.0:3000
# python3 manage.py runserver 0.0.0.0:3000
