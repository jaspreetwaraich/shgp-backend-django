#!/bin/bash
set -x

# Make migrations
# python manage.py makemigrations webapp
python manage.py migrate
python manage.py createcachetable