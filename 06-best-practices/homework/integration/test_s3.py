import os
import subprocess

import pandas as pd

bucket = "taxi-nyc-duration"

# Run the batch processing script with the test data
subprocess.run(
    [
        "pipenv",
        "run",
        "python",
        "batch_processing.py",
        "--year",
        "2023",
        "--month",
        "3",
        "--metrics",
        "--bucket",
        bucket,
    ],
    check=True,
)

options = {"client_kwargs": {"endpoint_url": os.getenv("S3_ENDPOINT_URL")}}

# Load the output file generated by the script
output_file = "2023/03/taxi_type=yellow_year=2023_month=03.parquet"

df_result = pd.read_parquet(f"s3://{bucket}/{output_file}", storage_options=options)

# Verify the structure of the output
assert "ride_id" in df_result.columns, "'ride_id' column is missing from the output."
assert "y_pred" in df_result.columns, "'y_pred' column is missing from the output."
