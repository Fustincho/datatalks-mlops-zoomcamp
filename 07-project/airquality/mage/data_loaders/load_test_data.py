import os
import requests
import pandas as pd

import time
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta

import urllib.parse

if "data_loader" not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data(*args, **kwargs):
    """
    Load data from the OpenAQ API for specified sensors and time range.

    Returns:
        pandas.DataFrame: A DataFrame containing the pivoted sensor data.
    """
    headers = {"accept": "application/json", "X-API-Key": os.environ["OPENAQ_API_KEY"]}

    x_sensors = [20466, 34845, 34841, 35394, 35577, 35843, 36047, 36066, 36064, 36092]

    y_sensor = [35606]

    sensor_ids = x_sensors + y_sensor

    start_date = datetime(2024, 7, 1, tzinfo=timezone.utc)
    end_date = datetime(2024, 7, 31, tzinfo=timezone.utc)

    def generate_url(sensor_id, start, end, limit=1000):
        base_url = f"https://api.openaq.org/v3/sensors/{sensor_id}/measurements"

        params = {
            "period_name": "hour",
            "date_from": start.isoformat(),
            "date_to": end.isoformat(),
            "limit": limit,
            "page": "1",
        }
        encoded_params = urllib.parse.urlencode(params)

        full_url = f"{base_url}?{encoded_params}"

        return full_url

    all_data = []

    def fetch_sensor_data(sensor_id):
        sensor_data = []

        date_range = pd.date_range(start_date, end_date, freq="MS")

        for current_date in date_range:
            month_end = current_date + relativedelta(months=1)

            while True:
                url = generate_url(sensor_id, current_date, month_end)
                response = requests.get(url, headers=headers)
                # print(url)

                if response.status_code == 429:
                    # print("Rate limit exceeded, sleeping for 30 seconds...")
                    time.sleep(30)
                    continue

                if response.status_code == 403:
                    # print("Error 403", sensor_id)
                    time.sleep(30)
                    continue

                if response.status_code == 408:
                    # print("Error 408", sensor_id)
                    time.sleep(30)
                    continue

                if response.status_code != 200:
                    print(f"Error: {response.status_code}")
                    print(url)
                    break

                data = response.json()
                if not data["results"]:
                    break

                for item in data["results"]:
                    value = item["value"]
                    utc_datetime = item["period"]["datetimeFrom"]["utc"]
                    sensor_data.append(
                        {
                            "sensor_id": sensor_id,
                            "datetime": utc_datetime,
                            "value": value,
                        }
                    )
                break

        return sensor_data

    # Iterate over all sensors and fetch data
    for sensor_id in sensor_ids:
        sensor_data = fetch_sensor_data(sensor_id)
        all_data.extend(sensor_data)

    df = pd.DataFrame(all_data)

    df.to_csv("inference_data.csv", index=False)

    pivot_df = df.pivot(
        index="datetime", columns="sensor_id", values="value"
    ).reset_index()
    pivot_df = pivot_df.rename_axis(None, axis=1)
    pivot_df.columns = [
        f"sid_{col}" if isinstance(col, int) else col for col in pivot_df.columns[:]
    ]

    return pivot_df


@test
def test_output(output, *args) -> None:
    assert output is not None, "The output is undefined"
