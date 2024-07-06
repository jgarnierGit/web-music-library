#!/bin/bash

set -m

# make sure migration are up to date
python backend-django/manage.py makemigrations music
python backend-django/manage.py migrate

redis-server 2>&1 &

# start server
python -Xfrozen_modules=off -m debugpy --listen 0.0.0.0:5678 backend-django/manage.py runserver 0.0.0.0:8000 2>&1 &

# # start Celery worker
python -Xfrozen_modules=off -m debugpy --listen 0.0.0.0:6900 -m celery -A appbackend worker --loglevel=INFO 2>&1 &

fg %2