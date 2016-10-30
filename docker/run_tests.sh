#!/usr/bin/env bash

set -ex

FILE_PATH="$(readlink -f ${BASH_SOURCE[0]})"
FILE_DIR="$(dirname ${FILE_PATH})"
SRC_DIR="$(dirname ${FILE_DIR})"

for PY_VER in 2.6 2.7 3.3 3.4 3.5
do
    docker run -it \
    -v ${SRC_DIR}:/code \
    -e PY_VER=${PY_VER} \
    -e EXEC_USER_ID=$(id -u) \
    mrupgrade/pyioc-test:latest \
    bin/run_tests.sh
done
