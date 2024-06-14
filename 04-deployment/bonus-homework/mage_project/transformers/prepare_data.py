if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):

    year = int(kwargs['year'])
    month = int(kwargs['month'])

    categorical = ['PULocationID', 'DOLocationID']

    data['duration'] = data.tpep_dropoff_datetime - data.tpep_pickup_datetime
    data['duration'] = data.duration.dt.total_seconds() / 60

    data = data[(data.duration >= 1) & (data.duration <= 60)].copy()

    data[categorical] = data[categorical].fillna(-1).astype('int').astype('str')

    data['ride_id'] = f'{year:04d}/{month:02d}_' + data.index.astype('str')

    return data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
