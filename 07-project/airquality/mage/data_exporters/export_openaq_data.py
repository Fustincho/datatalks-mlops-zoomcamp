import os
import psycopg
import pandas as pd
from pandas import DataFrame

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

create_table_statement = """
DROP TABLE if exists raw_training_data;
CREATE TABLE raw_training_data (
    datetime TIMESTAMPTZ,
    sid_20466 FLOAT,
    sid_34845 FLOAT,
    sid_34841 FLOAT,
    sid_35394 FLOAT,
    sid_35577 FLOAT,
    sid_35843 FLOAT,
    sid_36047 FLOAT,
    sid_36066 FLOAT,
    sid_36064 FLOAT,
    sid_36092 FLOAT,
    sid_35606 FLOAT
);
"""

@data_exporter
def export_data_to_postgres(df: DataFrame, **kwargs) -> None:
    """
    Exports a DataFrame to a PostgreSQL database.

    This function converts the 'datetime' column to datetime format and ensures that 
    all other columns are of type float. It then connects to a PostgreSQL database 
    using connection parameters from environment variables and inserts the data 
    into the 'raw_training_data' table.

    Parameters:
    df (pandas.DataFrame): The DataFrame to be exported. It is expected to have a 
                           'datetime' column and several sensor columns prefixed with 'sid_'.
    **kwargs: Additional keyword arguments (not used).

    The function assumes the following environment variables are set for database connection:
    - MAGEDB_HOST: The hostname of the PostgreSQL server.
    - MAGEDB_PORT: The port number of the PostgreSQL server.
    - MAGEDB_NAME: The name of the PostgreSQL database.
    - MAGEDB_USER: The username for the PostgreSQL database.
    - MAGEDB_PASSWORD: The password for the PostgreSQL database.

    The function creates the 'raw_training_data' table if it does not exist and 
    inserts data into this table row by row. It prints the number of rows inserted 
    at the end of the process.
    """

    df['datetime'] = pd.to_datetime(df['datetime'])
    for col in df.columns[1:]:
        df[col] = df[col].astype(float)

    conn_params = {
        'host': os.environ['MAGEDB_HOST'],
        'port': os.environ['MAGEDB_PORT'],
        'dbname': os.environ['MAGEDB_NAME'],
        'user': os.environ['MAGEDB_USER'],
        'password': os.environ['MAGEDB_PASSWORD'],
    }

    # Connect to the database
    with psycopg.connect(**conn_params) as conn:
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(create_table_statement)

        # Insert data into the table row by row
        insert_query = """
        INSERT INTO raw_training_data (datetime, sid_20466, sid_34845, sid_34841, sid_35394, sid_35577, sid_35843, sid_36047, sid_36066, sid_36064, sid_36092, sid_35606) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        for i, row in df.iterrows():
            cur.execute(insert_query, (
                row['datetime'], row['sid_20466'], row['sid_34845'], row['sid_34841'], row['sid_35394'], row['sid_35577'],
                row['sid_35843'], row['sid_36047'], row['sid_36066'], row['sid_36064'], row['sid_36092'], row['sid_35606']
            ))
        
        cur.execute(f"SELECT COUNT(*) FROM raw_training_data")
        row_count = cur.fetchone()[0]
        print(f"Number of rows: {row_count}")