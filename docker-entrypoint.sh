#!/bin/sh

if [ -z $COMMAND ]; then
    COMMAND="tail -f /dev/null"
fi

source ./env/bin/activate

echo "Run command $COMMAND"

sh -c "$COMMAND"
