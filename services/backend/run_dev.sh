#!/bin/bash

# make sure migration are up to date
python backend-django/manage.py makemigrations music
python backend-django/manage.py migrate

# start server
python -Xfrozen_modules=off -m debugpy --listen 0.0.0.0:5678  backend-django/manage.py runserver 0.0.0.0:8001