#!/usr/bin/env bash

FILE_PATH="$(readlink -f ${BASH_SOURCE[0]})"
FILE_DIR="$( dirname ${FILE_PATH})"
SRC_DIR="$( dirname ${FILE_DIR})"

docker pull mrupgrade/docker-deadsnakes-bundle-dev
# --no-cache --force-rm
docker build -t mrupgrade/pyioc-test:latest -f ${SRC_DIR}/docker/pyioc_test/Dockerfile ${SRC_DIR}
