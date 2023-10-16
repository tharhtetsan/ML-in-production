import json
import base64
import boto3
import os

PREDICTIONS_STREAM_NAME = os.getenv('PREDICTIONS_STREAM_NAME', 'ride_predictions')
kinesis_client = boto3.client('kinesis')


def prepare_features(ride):
    features = {}
    features['PU_DO'] = '%s_%s' % (ride['PULocationID'], ride['DOLocationID'])
    features['trip_distance'] = ride['trip_distance']
    return features


def predict(features):
    #pred = model.predict(features)
    return 10#float(pred[0])



def lambda_handler(event, context):
    
    
    prediction_events = []
    
    print(json.dumps(event))
    for record in event['Records']:
        # for endcoded stream data
        encoded_data = record['kinesis']['data']
        decoded_data = base64.b64decode(encoded_data).decode('utf-8')
        ride_event = json.loads(decoded_data)
        
        print(ride_event)
        ride_id = ride_event['ride_id']
        features = prepare_features(ride_event['ride'])
        prediction = predict(features)
        
        prediction_event = {
             'model': 'ride_duration_prediction_model',
            'version': '123',
            'prediction': {
                'ride_duration': prediction,
                'ride_id':ride_id
                }
            }
            
        result = kinesis_client.put_record(
                StreamName=PREDICTIONS_STREAM_NAME,
                Data=json.dumps(prediction_event),
                PartitionKey=str(ride_id)
            )
        prediction_events.append(prediction_event)
        print("PREDICTIONS_STREAM_NAME :",PREDICTIONS_STREAM_NAME)
        print(result)
        print(decoded_data)

    
    return prediction_events