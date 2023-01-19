# mlflow-server


### Run command
```shell
docker build . -t mlflow
```

```shell
docker run --env  BACKEND_STORE_URI="sqlite:///mlflow.db" --env  DEFAULT_ARTIFACT_ROOT="." -p 5000:5000 mlflow
```

```shell
 mlflow ui --backend-store-uri sqlite:///mlflow.db --default-artifact-root gs://aiteam-mlflow-storage-bucket/models -h 0.0.0.0 -p 8888
 ```
