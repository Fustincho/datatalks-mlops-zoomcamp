import os
import psycopg
import pandas as pd

if "data_loader" not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data(*args, **kwargs):
    """
    Loads data from a PostgreSQL database.

    This function connects to a PostgreSQL database using connection parameters
    from environment variables and retrieves all data from the 'raw_training_data' table.
    The retrieved data is then loaded into a pandas DataFrame.

    Returns:
    pd.DataFrame: A DataFrame containing the data retrieved from the 'raw_training_data' table.
    """

    conn_params = {
        "host": os.environ["MAGEDB_HOST"],
        "port": os.environ["MAGEDB_PORT"],
        "dbname": os.environ["MAGEDB_NAME"],
        "user": os.environ["MAGEDB_USER"],
        "password": os.environ["MAGEDB_PASSWORD"],
    }

    with psycopg.connect(**conn_params) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM public.raw_training_data")

            results = cur.fetchall()

            colnames = [desc.name for desc in cur.description]

            dataset = pd.DataFrame(results, columns=colnames)
    return dataset


@test
def test_output(output, *args) -> None:
    assert output is not None, "The output is undefined"
