# System and OS operations
import os
import time

# Date and Time operations
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta

# Data manipulation and HTTP requests
import pandas as pd
import requests
import urllib.parse

if "data_loader" not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test


def generate_url(sensor_id, start, end, limit=1000):
    """
    Generates the complete request URL for fetching sensor data from the OpenAQ API.

    Parameters:
    sensor_id (str): The ID of the sensor for which data is to be fetched.
    start (datetime): The start datetime for the data retrieval period.
    end (datetime): The end datetime for the data retrieval period.
    limit (int): The maximum number of results to retrieve. Default is 1000.

    Returns:
    str: The complete URL for the API request.
    """
    base_url = f"https://api.openaq.org/v3/sensors/{sensor_id}/measurements"

    params = {
        "period_name": "hour",
        "datetime_from": start.isoformat(),
        "datetime_to": end.isoformat(),
        "limit": limit,
        "page": "1",
    }
    encoded_params = urllib.parse.urlencode(params)

    full_url = f"{base_url}?{encoded_params}"

    return full_url


def fetch_sensor_data(sensor_id, start_date, end_date, headers):
    """
    Fetches sensor data from the OpenAQ API for a given sensor within a specified date range.

    This function calls the OpenAQ API to retrieve sensor data for the sensor with the given
    sensor_id. It requests data iteratively, one month at a time, handling rate limits and
    other potential errors appropriately.

    Parameters:
    sensor_id (str): The ID of the sensor for which data is to be fetched.
    start_date (datetime): The start date for the data retrieval in 'YYYY-MM-DD' format.
    end_date (datetime): The end date for the data retrieval in 'YYYY-MM-DD' format.
    headers (dict): The headers to include in the API request.

    Returns:
    pandas.DataFrame: A DataFrame containing the sensor data, with columns for sensor_id,
                      datetime, and value.

    The function handles the following API response codes:
    - 429: Rate limit exceeded; waits for 30 seconds before retrying.
    - 403: Forbidden; waits for 30 seconds before retrying.
    - 408: Request timeout; waits for 30 seconds before retrying.
    - Other non-200 responses: Prints an error message and skips to the next iteration.
    """
    sensor_data = []

    date_range = pd.date_range(start_date, end_date, freq="MS")

    for current_date in date_range:
        month_end = current_date + relativedelta(months=1)

        while True:
            url = generate_url(sensor_id, current_date, month_end)
            response = requests.get(url, headers=headers)
            # print(url)

            if response.status_code == 429:
                print("Rate limit exceeded, sleeping for 30 seconds...")
                time.sleep(30)
                continue

            if response.status_code == 403:
                print("Error 403", sensor_id)
                time.sleep(30)
                continue

            if response.status_code == 408:
                print("Error 408", sensor_id)
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
                    {"sensor_id": sensor_id, "datetime": utc_datetime, "value": value}
                )
            break

    return pd.DataFrame(sensor_data)


@data_loader
def load_data_from_api(data, *args, **kwargs):
    """
    Load data from one OpenAQ sensor within a specified date range.

    This function uses the fetch_sensor_data function to retrieve data for a given sensor
    from the OpenAQ API. The date range is set from January 1, 2022, to June 30, 2024.

    Parameters:
    data (dict): A dictionary (dynamic child block) containing the sensor_id of the sensor.
    **kwargs: Pipeline variables specifying the start / end dates.

    Returns:
    pd.DataFrame: A DataFrame containing the sensor data retrieved from the OpenAQ API.
    """

    start_date = datetime(
        int(kwargs["y_start"]),
        int(kwargs["m_start"]),
        int(kwargs["d_start"]),
        tzinfo=timezone.utc,
    )
    end_date = datetime(
        int(kwargs["y_end"]),
        int(kwargs["m_end"]),
        int(kwargs["d_end"]),
        tzinfo=timezone.utc,
    )

    headers = {"accept": "application/json", "X-API-Key": os.environ["OPENAQ_API_KEY"]}

    return fetch_sensor_data(data["sensor_id"], start_date, end_date, headers)


@test
def test_output(output, *args) -> None:
    assert output is not None, "The output is undefined"
