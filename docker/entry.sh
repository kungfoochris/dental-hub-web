#!/bin/bash
# entry.sh
cd src
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver 0.0.0.0:3000
