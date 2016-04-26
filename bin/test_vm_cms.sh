#!/usr/bin/env bash

# git clone https://github.com/ulkoart/wsba.git && cd wsba && git checkout feature/cms && bin/test_vm_cms.sh

virtualenv env
source env/bin/activate
pip install -r requirements.txt
bin/bower_install.sh
mkdir extra
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver