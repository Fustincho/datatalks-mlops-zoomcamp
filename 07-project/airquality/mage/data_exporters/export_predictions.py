import os
import psycopg

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

create_table_query = """
    CREATE TABLE IF NOT EXISTS aq_predictions (
        datetime TIMESTAMP NOT NULL,
        sid_20466 FLOAT,
        sid_34841 FLOAT,
        sid_34845 FLOAT,
        sid_35394 FLOAT,
        sid_35577 FLOAT,
        sid_35606 FLOAT,
        sid_35843 FLOAT,
        sid_36047 FLOAT,
        sid_36064 FLOAT,
        sid_36066 FLOAT,
        sid_36092 FLOAT,
        predictions FLOAT,
        PRIMARY KEY (datetime)
    );
"""

@data_exporter
def export_data(data, *args, **kwargs):
    """
    Exports the data to a PostgreSQL database.

    This function connects to a PostgreSQL database using connection parameters
    from environment variables and inserts the data into the 'aq_predictions' table.
    If a row with the same 'datetime' already exists, 
    it does nothing (ON CONFLICT DO NOTHING).

    Parameters:
    data (pd.DataFrame): The input data to be exported. It should contain the columns:
                        'datetime', 'sid_20466', 'sid_34841', 'sid_34845', 'sid_35394', 
                        'sid_35577', 'sid_35606', 'sid_35843', 'sid_36047', 'sid_36064', 
                        'sid_36066', 'sid_36092', 'predictions'.
    """
    conn_params = {
        'host': os.environ['MAGEDB_HOST'],
        'port': os.environ['MAGEDB_PORT'],
        'dbname': os.environ['MAGEDB_NAME'],
        'user': os.environ['MAGEDB_USER'],
        'password': os.environ['MAGEDB_PASSWORD'],
    }

    with psycopg.connect(**conn_params) as conn:
            
        insert_query = """
        INSERT INTO aq_predictions (
            datetime, sid_20466, sid_34841, sid_34845, sid_35394, sid_35577, 
            sid_35606, sid_35843, sid_36047, sid_36064, sid_36066, sid_36092, predictions
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
        ON CONFLICT (datetime) DO NOTHING;
        """

        # Iterate over the dataframe and insert rows
        with conn.cursor() as cur:
            cur.execute(create_table_query)
            conn.commit()
            
            for row in data.itertuples(index=False, name=None):
                cur.execute(insert_query, row)
            conn.commit()

