#!/usr/bin/env bash

git checkout feature/cms
virtualenv env
source env/bin/activate
pip install -r requirements.txt
bin/bower_install.sh
mkdir extra
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver