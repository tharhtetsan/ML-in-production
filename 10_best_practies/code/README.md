
## Unit Testing
### Env Create

```bash
pip install pipenv
pipenv install

```

We only need pytest for dev env. And we don't need for prod.

```bash
pipenv install --dev pytest
pipenv install --dev deepdiff
pipenv install

```

Generate pipenv to requirements.txt

```bash
pipenv run pip freeze > requirements.txt
```

```bash
docker build -t stream-model-duration:test .

docker run -it --rm \
    -p 8080:8080 \
    -e PREDICTIONS_STREAM_NAME="ride_predictions" \
    -e RUN_ID="e1efc53e9bd149078b0c12aeaa6365df" \
    -e TEST_RUN="True" \
    -e AWS_DEFAULT_REGION="eu-west-1" \
    stream-model-duration:test
```



## Integration testing
Mounting the model folder:

```bash
docker run -it --rm \
    -p 8080:8080 \
    -e PREDICTIONS_STREAM_NAME="ride_predictions" \
    -e RUN_ID="Test123" \
    -e MODEL_LOCATION="/app/model" \
    -e TEST_RUN="True" \
    -e AWS_DEFAULT_REGION="eu-west-1" \
    -v $(pwd)/model:/app/model \
    stream-model-duration:test
```

Integration test

```bash
chmod +x integration-test/run.sh 

sleep 1

sh integration-test/run.sh 

pipenv run python test-docker.py

```

## Testing Cloudservices with Localstack

####  Localstack commands
check stream list from my AWS
```bash
aws kinesis list-streams
```
check stream list from localstack  AWS
```bash
aws --endpoint-url=http://localhost:4566 \
    kinesis create-stream \
    --stream-name ride_predictions \
    --shard-count 1

aws --endpoint-url=http://localhost:4566 kinesis list-streams
```


Test all 
```bash
pipenv run pytest tests/
sudo sh integration-test/run.sh 
```


## Code quality: linting and formatting
```bash
pipenv install --dev pylint
pipenv run pylint .
```




### Reference
https://linuxize.com/post/bash-shebang/

https://github.com/localstack/localstack

https://github.com/pylint-dev/pylint
