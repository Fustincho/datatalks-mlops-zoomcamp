from mage_ai.io.file import FileIO
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_file(*args, **kwargs):
    year = int(kwargs['year'])
    month = int(kwargs['month'])
    basepath = 'https://d37ci6vzurychx.cloudfront.net/trip-data/'
    datapath = f'yellow_tripdata_{year:04d}-{month:02d}.parquet'

    return FileIO().load(basepath + datapath)


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
