import requests
from deepdiff import DeepDiff
import json

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
url = 'http://localhost:8080/2015-03-31/functions/function/invocations'

actual_response = requests.post(url, json=event).json()
print(actual_response)
expected_response = {'predictions': [
    {'model': 'ride_duration_prediction_model', 
     'version': 'Test123',
       'prediction': {
           'ride_duration': 10.0,
             'ride_id': 156}
             }
             ]
    }

diff = DeepDiff(actual_response,expected_response)
print(f'diff = ',diff)
assert 'type_changes' not in diff