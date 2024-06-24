import datetime
import logging
import pickle
import time

import pandas as pd
import psycopg
from evidently import ColumnMapping
from evidently.metrics import (ColumnDriftMetric, ColumnQuantileMetric,
                               DatasetCorrelationsMetric, DatasetDriftMetric,
                               DatasetMissingValuesMetric)
from evidently.report import Report
from psycopg import Cursor

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s]: %(message)s")

create_table_statement = """
drop table if exists dummy_metrics;
create table dummy_metrics(
	timestamp timestamp,
	prediction_drift float,
	num_drifted_columns integer,
	share_missing_values float,
    quantile_fifty_value float
)
"""

# We will upload March 2024 data
begin = datetime.datetime(2024, 3, 1, 0, 0)

num_features = ['passenger_count',
                'trip_distance', 'fare_amount', 'total_amount']

cat_features = ['PULocationID', 'DOLocationID']

reference_data = pd.read_parquet('data/reference.parquet')
with open('models/lin_reg.bin', 'rb') as f_in:
    model = pickle.load(f_in)

raw_data = pd.read_parquet('data/green_tripdata_2024-03.parquet')


# Evidently Report Configuration
column_mapping = ColumnMapping(
    prediction='prediction',
    numerical_features=num_features,
    categorical_features=cat_features,
    target=None
)

report = Report(metrics=[
    ColumnDriftMetric(column_name='prediction'),
    DatasetDriftMetric(),
    DatasetMissingValuesMetric(),
    DatasetCorrelationsMetric(),
    ColumnQuantileMetric(column_name='fare_amount', quantile=0.5)
]
)

# pylint: disable=E1129


def prep_metrics_table():
    # Establish connection to the 'taxi_monitoring' database
    with psycopg.connect("host=localhost port=5432 dbname=taxi_monitoring user=postgres password=postgres_admin_pwd") as conn:
        conn.autocommit = True  # Enable autocommit
        cur = conn.cursor()
        cur.execute(create_table_statement)


def calculate_metrics_postgresql(curr: Cursor, i):
    # Data per days
    current_data = raw_data[(raw_data.lpep_pickup_datetime >= (begin + datetime.timedelta(i))) &
                            (raw_data.lpep_pickup_datetime < (begin + datetime.timedelta(i + 1)))]

    current_data['prediction'] = model.predict(
        current_data[num_features + cat_features].fillna(0))

    report.run(reference_data=reference_data, current_data=current_data,
               column_mapping=column_mapping)

    result = report.as_dict()

    prediction_drift = float(result['metrics'][0]['result']['drift_score'])
    num_drifted_columns = int(
        result['metrics'][1]['result']['number_of_drifted_columns'])
    share_missing_values = float(
        result['metrics'][2]['result']['current']['share_of_missing_values'])
    quantile_fifty_value = float(
        result['metrics'][4]['result']['current']['value'])

    curr.execute(
        "insert into dummy_metrics(timestamp, prediction_drift, num_drifted_columns, share_missing_values, quantile_fifty_value) values (%s, %s, %s, %s, %s)",
        (begin + datetime.timedelta(i), prediction_drift,
         num_drifted_columns, share_missing_values, quantile_fifty_value)
    )


SEND_TIMEOUT = 10


def main():
    prep_metrics_table()
    last_send = datetime.datetime.now() - datetime.timedelta(seconds=10)
    with psycopg.connect("host=localhost port=5432 dbname=taxi_monitoring user=postgres password=postgres_admin_pwd") as conn:
        conn.autocommit = True
        for i in range(0, 31):
            with conn.cursor() as curr:
                calculate_metrics_postgresql(curr, i)

                curr.execute("SELECT COUNT(*) FROM dummy_metrics")
                row_count = curr.fetchone()[0]
                logging.info(f"Row count after iteration {i}: {row_count}")

            new_send = datetime.datetime.now()
            seconds_elapsed = (new_send - last_send).total_seconds()
            if seconds_elapsed < SEND_TIMEOUT:
                time.sleep(SEND_TIMEOUT - seconds_elapsed)

            # Update last_send to the new send time after sleeping
            last_send = datetime.datetime.now()

            logging.info("data sent")


if __name__ == '__main__':
    main()
