### [Sending data](https://github.com/DataTalksClub/mlops-zoomcamp/tree/main/04-deployment/streaming#sending-data)

```shell
KINESIS_STREAM_INPUT=ride_events
aws kinesis put-record \
    --stream-name ${KINESIS_STREAM_INPUT}\
    --partition-key 1 \
--cli-binary-format raw-in-base64-out \
    --data "Hello, this is a test."




```

Record example

```json
{
    "ride": {
        "PULocationID": 130,
        "DOLocationID": 205,
        "trip_distance": 3.66
    }, 
    "ride_id": 123
}
```

Sending this record

```shell
aws kinesis put-record \
    --stream-name ${KINESIS_STREAM_INPUT} \
    --partition-key 1 \
--cli-binary-format raw-in-base64-out \
    --data '{
        "ride": {
            "PULocationID": 130,
            "DOLocationID": 205,
            "trip_distance": 3.66
        }, 
        "ride_id": 156
    }'
```

**pipenv install boto3 scikit-learn --python=3.9**

**docker build . -t stream-model-duration:v1**


References

https://docs.aws.amazon.com/lambda/latest/dg/with-kinesis-example.html

https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis.html

https://gallery.ecr.aws/lambda/python
