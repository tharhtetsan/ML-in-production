#!/usr/bin/env bash
set -e

mlflow server --host 0.0.0.0 --port 5000 --backend-store-uri ${BACKEND_STORE_URI} --default-artifact-root ${DEFAULT_ARTIFACT_ROOT} &

wait -n
