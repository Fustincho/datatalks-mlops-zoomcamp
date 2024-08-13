import os
import json
import requests
import pandas as pd

if "transformer" not in globals():
    from mage_ai.data_preparation.decorators import transformer
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    """
    Transforms the dataset by creating a payload for a batch prediction API,
    sending the data to the API, and appending the predictions to the dataset.

    Parameters:
    data (pandas.DataFrame): The input dataset containing sensor data.

    Returns:
    pd.DataFrame: The input dataset with an added 'predictions' column.
    """
    sensors = [20466, 34845, 34841, 35394, 35577, 35843, 36047, 36066, 36064, 36092]

    def create_sensor_dicts(data, sensors):
        sensor_keys = [f"sid_{sensor}" for sensor in sensors]
        dict_list = data[sensor_keys].to_dict(orient="records")
        return dict_list

    sensor_data = create_sensor_dicts(data, sensors)
    sensor_data = [
        {k: (None if pd.isna(v) else v) for k, v in d.items()} for d in sensor_data
    ]

    api_data_payload = {"batch": sensor_data}

    API_HOST = os.environ["API_HOST"]
    url = f"http://{API_HOST}:8000/predict_batch"
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    response = requests.post(url, headers=headers, data=json.dumps(api_data_payload))

    # Check response and append predictions to dataframe
    if response.status_code == 200:
        predictions = response.json().get("predictions", [])
        data["predictions"] = predictions
    else:
        data["predictions"] = None

    print(data.dtypes)
    return data


@test
def test_output(output, *args) -> None:
    assert output is not None, "The output is undefined"
