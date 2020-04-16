#!/bin/sh


command=$@

if [ -z $command ]; then
    command="alembic upgrade head && gunicorn -c gunicorn.config.py wsgi:application"
fi

source ./env/bin/activate

echo "Run command $command"

sh -c "$command"
