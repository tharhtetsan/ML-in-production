import os
import sys
sys.path.append(os.getcwd())

import model
import lambda_function
from pathlib import Path
 
def read_text(file):
    test_directory = Path(__file__).parent

    with open(test_directory / file, 'rt', encoding='utf-8') as f_in:
        return f_in.read().strip()
    


def test_base64_decode():
    base64_input = read_text('data.b64')

    actual_result = model.base64_decode(base64_input)
    expected_result = {
        "ride": {
            "PULocationID": 130,
            "DOLocationID": 205,
            "trip_distance": 3.66,
        },
        "ride_id": 256,
    }
    print(actual_result)
    assert actual_result == expected_result


def test_prepare_features():
    model_service = model.ModelService(None)
    ride = {
        "PULocationID": 130,
        "DOLocationID": 205,
        "trip_distance": 3.66,
    }

    actual_features = model_service.prepare_features(ride)

    expected_fetures = {
        "PU_DO": "130_205",
        "trip_distance": 3.66,
    }
    assert actual_features == expected_fetures


def test_predict():
    model_mock = ModelMock(10.0)
    model_service = model.ModelService(None)
    fetures = {
        "PU_DO": "130_205",
        "trip_distance": 3.66,
    }
    actual_result = model_mock.predict(fetures)[0]
    expected_result = 10.0
    assert actual_result == expected_result

def test_lambda_handler():
    model_mock = ModelMock(10.0)
    model_version = "Test123"
    model_service = model.ModelService(model_mock,model_version)
    stream_record = {
        "Records": [
            {
                "kinesis": {
                    "data": "ewogICAgICAgICJyaWRlIjogewogICAgICAgICAgICAiUFVMb2NhdGlvbklEIjogMTMwLAogICAgICAgICAgICAiRE9Mb2NhdGlvbklEIjogMjA1LAogICAgICAgICAgICAidHJpcF9kaXN0YW5jZSI6IDMuNjYKICAgICAgICB9LCAKICAgICAgICAicmlkZV9pZCI6IDI1NgogICAgfQ==",
                    "approximateArrivalTimestamp": 1654161514.132
                },
            }
        ]
    }
    actual_predictions = model_service.lambda_handler(stream_record)
    expected_predictions = { 'predictions' : [
                {
                'model': 'ride_duration_prediction_model',
                'version': model_version,
                'prediction': {'ride_duration': 10.0, 'ride_id': 256},
                }
             ]
    }
    assert actual_predictions == expected_predictions
    




class ModelMock:
    def __init__(self, value):
        self.value = value

    def predict(self, X):
        n = len(X)
        return [self.value] * n
    


if __name__ == "__main__":
    print(test_base64_decode())
    
    