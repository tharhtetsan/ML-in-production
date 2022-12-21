# mlflow-server


### Run command
```shell
docker build . -t mlflow
```

```shell
docker run --env  BACKEND_STORE_URI="sqlite:///mlflow.db" --env  DEFAULT_ARTIFACT_ROOT="." -p 5000:5000 mlflow
```

