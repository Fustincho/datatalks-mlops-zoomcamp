import pandas as pd

from helpers import dt
from batch_processing import prepare_data


def test_prepare_data():
    """
    This test covers all the data preparation processes:
    - The creation of the duration column
    - The filtering of data depending on the duration value
    - The NA imputation to -1
    - The conversion of categorical variables to strings
    """
    # Preparing mock data
    columns = [
        "PULocationID",
        "DOLocationID",
        "tpep_pickup_datetime",
        "tpep_dropoff_datetime",
    ]

    data = [
        (None, None, dt(1, 1), dt(1, 10)),
        (1, 1, dt(1, 2), dt(1, 10)),
        (1, None, dt(1, 2, 0), dt(1, 2, 59)),
        (3, 4, dt(1, 2, 0), dt(2, 2, 1)),
    ]

    expected_data = [
        ("-1", "-1", dt(1, 1), dt(1, 10), 9.0),
        ("1", "1", dt(1, 2), dt(1, 10), 8.0),
    ]

    df = pd.DataFrame(data, columns=columns)
    expected_df = pd.DataFrame(expected_data, columns=columns + ["duration"])

    expected_df = expected_df.astype(
        {"PULocationID": "object", "DOLocationID": "object"}
    )

    print(expected_df.describe())
    df = prepare_data(df, categorical=["PULocationID", "DOLocationID"])
    print(df)

    pd.testing.assert_frame_equal(df, expected_df)
