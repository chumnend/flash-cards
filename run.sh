#!/bin/bash

cd src
python manage.py collectstatic
python manage.py migrate

gunicorn flashcards.wsgi
