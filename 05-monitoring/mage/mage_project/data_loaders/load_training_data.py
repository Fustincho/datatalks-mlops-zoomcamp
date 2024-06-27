import psycopg
import pandas as pd

from os import path

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_postgres(*args, **kwargs):
    
    conn_params = {
        'host': 'mage_db',
        'port': '5432',
        'dbname': 'taxi_monitoring',
        'user': 'postgres',
        'password': 'postgres_admin_pwd',
    }

    # Connect to the database
    with psycopg.connect(**conn_params) as conn:
        # Define your SQL query
        query = "SELECT * FROM training_data"

        # Execute the query and load data into a DataFrame
        df = pd.read_sql(query, conn)

    return df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
