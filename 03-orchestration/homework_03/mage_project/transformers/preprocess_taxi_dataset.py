from pandas import DataFrame, to_datetime

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@transformer
def transform(data: DataFrame, *args, **kwargs) -> DataFrame:
    """
    Preprocess the dataset

    Args:
        data: Raw data

    Returns:
        data: Filtered DataFrame based on duration time
    """
    # Specify your transformation logic here

    data.tpep_dropoff_datetime = to_datetime(data.tpep_dropoff_datetime)
    data.tpep_pickup_datetime = to_datetime(data.tpep_pickup_datetime)

    data['duration'] = data.tpep_dropoff_datetime - data.tpep_pickup_datetime
    data.duration = data.duration.dt.total_seconds() / 60

    data = data[(data.duration >= 1) & (data.duration <= 60)]

    categorical = ['PULocationID', 'DOLocationID']
    data[categorical] = data[categorical].astype(str)

    return data


@test
def test_output(output, *args) -> None:
    """
    Here we verify that the data was filtered successfully. There should be 
    3'316.216 records remaining.
    """
    assert len(output) == 3_316_216
