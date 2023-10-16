
import lambda_function

event = {

    "Records": [
      {
        "kinesis": {
          "kinesisSchemaVersion": "1.0",
          "partitionKey": "1",
          "sequenceNumber": "49645409528811360698132100277697042876752816908273713154",
          "data": "ewogICAgICAgICJyaWRlIjogewogICAgICAgICAgICAiUFVMb2NhdGlvbklEIjogMTMwLAogICAgICAgICAgICAiRE9Mb2NhdGlvbklEIjogMjA1LAogICAgICAgICAgICAidHJpcF9kaXN0YW5jZSI6IDMuNjYKICAgICAgICB9LCAKICAgICAgICAicmlkZV9pZCI6IDE1NgogICAgfQ==",
          "approximateArrivalTimestamp": 1697130294.845
        },
        "eventSource": "aws:kinesis",
        "eventVersion": "1.0",
        "eventID": "shardId-000000000000:49645409528811360698132100277697042876752816908273713154",
        "eventName": "aws:kinesis:record",
        "invokeIdentityArn": "arn:aws:iam::517074519053:role/lambda-kinesis-role",
        "awsRegion": "ap-southeast-2",
        "eventSourceARN": "arn:aws:kinesis:ap-southeast-2:517074519053:stream/ride_events"
      }
    ]
  }
result = lambda_function.lambda_handler(event, None)
print(result)