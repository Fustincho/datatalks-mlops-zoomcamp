import psycopg

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

create_table_statement = """
DROP TABLE if exists training_data;
CREATE TABLE training_data (
    "VendorID" INT,
    lpep_pickup_datetime TIMESTAMP,
    lpep_dropoff_datetime TIMESTAMP,
    store_and_fwd_flag VARCHAR(10),
    "RatecodeID" FLOAT,
    "PULocationID" INT,
    "DOLocationID" INT,
    passenger_count FLOAT,
    trip_distance FLOAT,
    fare_amount FLOAT,
    extra FLOAT,
    mta_tax FLOAT,
    tip_amount FLOAT,
    tolls_amount FLOAT,
    ehail_fee FLOAT,
    improvement_surcharge FLOAT,
    total_amount FLOAT,
    payment_type FLOAT,
    trip_type FLOAT,
    congestion_surcharge FLOAT,
    duration_min FLOAT
);
"""

@data_exporter
def export_data(data, *args, **kwargs):
    """
    Exports data to some source.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Output (optional):
        Optionally return any object and it'll be logged and
        displayed when inspecting the block run.
    """
    # Specify your data exporting logic here
    conn_params = {
        'host': 'mage_db',
        'port': '5432',
        'dbname': 'taxi_monitoring',
        'user': 'postgres',
        'password': 'postgres_admin_pwd',
    }

    # Connect to the database
    with psycopg.connect(**conn_params) as conn:
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(create_table_statement)
        # In PostgreSQL, identifiers (such as table names and column names) are case-insensitive by default.
        # They are converted to lower case unless quoted. To preserve the case (e.g., PULocationID),
        # you need to use double quotes when defining or referencing the column.

        for i, row in data.iterrows():
            sql = """
            INSERT INTO training_data (
                "VendorID", lpep_pickup_datetime, lpep_dropoff_datetime, store_and_fwd_flag, "RatecodeID", "PULocationID",
                "DOLocationID", passenger_count, trip_distance, fare_amount, extra, mta_tax, tip_amount,
                tolls_amount, ehail_fee, improvement_surcharge, total_amount, payment_type, trip_type, congestion_surcharge,
                duration_min
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
            """
            cur.execute(sql, (
                row['VendorID'], row['lpep_pickup_datetime'], row['lpep_dropoff_datetime'], row['store_and_fwd_flag'], 
                row['RatecodeID'], row['PULocationID'], row['DOLocationID'], row['passenger_count'], row['trip_distance'], 
                row['fare_amount'], row['extra'], row['mta_tax'], row['tip_amount'], row['tolls_amount'], 
                row['ehail_fee'], row['improvement_surcharge'], row['total_amount'], row['payment_type'], 
                row['trip_type'], row['congestion_surcharge'], row['duration_min']
            ))
        
        cur.execute(f"SELECT COUNT(*) FROM training_data")
        row_count = cur.fetchone()[0]
        print(f"Number of rows: {row_count}")

