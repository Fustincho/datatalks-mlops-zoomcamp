import os
import psycopg
from typing import Dict, List

if "data_loader" not in globals():
    from mage_ai.data_preparation.decorators import data_loader

def create_aq_database():
    conn_params = {
            "host": os.environ["MAGEDB_HOST"],
            "port": os.environ["MAGEDB_PORT"],
            "dbname": os.environ["MAGEDB_NAME"],
            "user": os.environ["MAGEDB_USER"],
            "password": os.environ["MAGEDB_PASSWORD"],
        }

    with psycopg.connect(**conn_params) as conn:
        conn.autocommit = True
        cur = conn.cursor()
        # Check if the database exists
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", ('aq_data',))
        exists = cur.fetchone()

        # If the database does not exist, create it
        if not exists:
            cur.execute('CREATE DATABASE aq_data')

@data_loader
def load_data(*args, **kwargs) -> List[List[Dict]]:
    """
    A dynamic block must return a list of 2 lists of dictionaries
    (e.g. List[List[Dict]]).
    This dynamic block organizes the sensors into an acceptable
    dynamic block output so that data is fetched in parallel by
    the dynamic childs.
    """

    create_aq_database()

    sensor_ids = [
        20466,
        34845,
        34841,
        35394,
        35577,
        35843,
        36047,
        36066,
        36064,
        36092,
        35606,
    ]

    datasets = []
    metadata = []

    for i, sensor_id in enumerate(sensor_ids):
        datasets.append(dict(id=i, sensor_id=sensor_id))
        metadata.append(dict(block_uuid=f"{i}_{sensor_id}"))

    return [
        datasets,
        metadata,
    ]
