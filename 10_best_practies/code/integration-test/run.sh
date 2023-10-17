#!/usr/bin/env bash

set e+

cd "$(dirname "$0")"


LOCAL_TAG=`date +"%Y-%m-%d-%H-%M"`
export LOCAL_IMAGE_NAME="stream-model-duration:${LOCAL_TAG}"

echo "LOCAL_IMAGE_NAME is not set, building a new image with tag ${LOCAL_IMAGE_NAME}"
docker build -t ${LOCAL_IMAGE_NAME} ..

docker-compose up -d

pipenv run python test-docker.py
ERROR_CODE=$?

if [ ${ERROR_CODE} != 0 ]; then
    docker-compose logs
fi 
    docker-compose down