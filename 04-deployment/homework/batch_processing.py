#!/usr/bin/env python
# coding: utf-8

import logging
import os
import pickle

import boto3
import click
import numpy as np
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

with open('model.bin', 'rb') as f_in:
    dv, model = pickle.load(f_in)

categorical = ['PULocationID', 'DOLocationID']


def read_data(filename):
    df = pd.read_parquet(filename)

    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')

    return df


@click.command()
@click.option('--year', default=2023, prompt='Enter a year', help='Year of the data')
@click.option('--month', default=3, prompt='Enter a month (1-12)', help='Month of the data')
@click.option('--metrics', is_flag=True, help='Print metrics about the predictions')
@click.option('--bucket', help='Name of the S3 bucket to upload the results', required=False)
def main(year, month, metrics, bucket):

    logging.info(f'Starting data processing for {year}-{month:02d}')

    logging.info('Loading and processing data...')
    df = read_data(
        f'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year:04d}-{month:02d}.parquet')

    logging.info('Data loaded successfully. Proceeding with predictions.')

    logging.info('Transforming categorical variables...')
    dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(dicts)

    logging.info('Generating predictions using the model...')
    y_pred = model.predict(X_val)

    logging.info('Predictions generated successfully.')

    if metrics:
        logging.info('Calculating prediction metrics...')
        mean_pred = np.mean(y_pred)
        std_pred = np.std(y_pred)
        min_pred = np.min(y_pred)
        max_pred = np.max(y_pred)
        logging.info('Prediction metrics - Mean: %f, Std: %f, Min: %f, Max: %f',
                     mean_pred, std_pred, min_pred, max_pred)

    df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')

    logging.info('Preparing results for export...')
    df_result = pd.DataFrame({'ride_id': df['ride_id'], 'y_pred': y_pred})

    output_file = 'output.parquet'

    logging.info('Exporting results to %s...', output_file)

    df_result.to_parquet(
        output_file,
        engine='pyarrow',
        compression=None,
        index=False
    )

    logging.info('Data processing and export completed successfully.')

    if bucket:
        logging.info('Uploading results to S3 bucket: %s', bucket)
        s3_client = boto3.client('s3')
        # S3 object key with folder structure
        s3_key = f'{year}/{month:02d}/{output_file}'
        s3_client.upload_file(output_file, bucket, s3_key)
        logging.info('File uploaded successfully to S3 at %s.', s3_key)


if __name__ == '__main__':
    main()
