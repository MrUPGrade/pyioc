#!/usr/bin/env bash

set -e

FILE_PATH=$(readlink -f ${BASH_SOURCE[0]})
FILE_DIR=$(dirname ${FILE_PATH})
SRC_DIR=$(dirname ${FILE_DIR})

if [ -z "${PY_VER}" ]
then
    PY_VER=2.7
fi

python${PY_VER} -m pytest tests/
