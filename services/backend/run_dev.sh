#!/bin/bash

# make sure migration are up to date
python backend-django/manage.py migrate
# start server
python backend-django/manage.py runserver 0.0.0.0:8000