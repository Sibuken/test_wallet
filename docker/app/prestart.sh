#! /usr/bin/env sh

python /app/manage.py collectstatic --noinput
python /app/manage.py compilemessages
python /app/manage.py migrate
