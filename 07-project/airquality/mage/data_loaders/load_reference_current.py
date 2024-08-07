import sys
import psycopg
import pandas as pd

# TODO Add the project root to the Python path
sys.path.append("/home/src/mage")
from utils.dbconfig import load_magedb_config


if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data(*args, **kwargs):
    """
    Loads data from the PostgreSQL database.

    This function connects to a PostgreSQL database using connection parameters
    from environment variables and retrieves data from the 'original_data' and 
    'aq_predictions' tables. The retrieved data is loaded into pandas DataFrames.

    Returns:
        tuple: A tuple containing two pandas DataFrames:
            - reference_data: DataFrame containing the data from the 'raw_training_data' table.
            - current_data: DataFrame containing the data from the 'aq_predictions' table.
    """
    with psycopg.connect(**load_magedb_config()) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM public.raw_training_data")
            
            results = cur.fetchall()
            
            colnames = [desc.name for desc in cur.description]
            
            reference_data = pd.DataFrame(results, columns=colnames)

            cur.execute("SELECT * FROM public.aq_predictions")
            
            results = cur.fetchall()
            
            colnames = [desc.name for desc in cur.description]
            
            current_data = pd.DataFrame(results, columns=colnames)
    
    return reference_data, current_data


@test
def test_output(output, *args) -> None:
    assert output is not None, 'The output is undefined'
