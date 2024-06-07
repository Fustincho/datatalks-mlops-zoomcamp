from pandas import DataFrame

from mage_ai.io.file import FileIO
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_file(*args, **kwargs) -> DataFrame:
    """
    This block downloads the parquet data file from the NYC website.
    The FileIO loader transforms the parquet into a pandas.DataFrame

    Dataset Source: https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page
    """
    filepath = 'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-03.parquet'

    return FileIO().load(filepath)


@test
def test_output(output, *args) -> None:
    """
    Here we verify that the data was loaded successfully. There are 3'403.766 records.
    """
    assert len(output) == 3_403_766
