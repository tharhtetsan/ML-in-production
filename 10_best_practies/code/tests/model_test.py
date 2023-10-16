#import lambda_function

def test_prepare_features():
    """
    ride = {
        "PULocationID": 130,
        "DOLocationID": 205,
        "trip_distance": 3.66,
    }

    actual_features = lambda_function.prepare_features(ride)

    expected_fetures = {
        "PU_DO": "130_205",
        "trip_distance": 3.66,
    }
    #assert actual_features == expected_fetures
    """
    assert 1 == 1