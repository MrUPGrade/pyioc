#!/usr/bin/env bash

if [ -z "${EXEC_USER_ID}" ]
then
    echo "EXEC_USER_ID variable must be passed"
    exit -1
fi

find . -iname *.pyc -delete

useradd -m -o -u $EXEC_USER_ID executor
sudo -E -u  executor "$@"

find . -iname *.pyc -delete
