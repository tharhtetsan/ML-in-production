### Env Create 
```bash
pip install pipenv
pipenv install

```


We only need pytest for dev env. And we don't need for prod.
```bash
pipenv install --dev pytest

```


Generate pipenv to requirements.txt
```bash
pipenv run pip freeze > requirements.txt
```


```bash
docker build -t stream-model-duration:v1 .

docker run -it --rm \
    -p 8080:8080 \
    -e PREDICTIONS_STREAM_NAME="ride_predictions" \
    -e RUN_ID="e1efc53e9bd149078b0c12aeaa6365df" \
    -e TEST_RUN="True" \
    -e AWS_DEFAULT_REGION="eu-west-1" \
    stream-model-duration:v1

```
