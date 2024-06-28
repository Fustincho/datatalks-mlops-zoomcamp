import os
import subprocess

import pandas as pd

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
    ],
    check=True,
)

# Load the output file generated by the script
output_file = "taxi_type=yellow_year=2023_month=03.parquet"
df_result = pd.read_parquet(output_file)

# Check if output file exists
assert os.path.exists(output_file), f"Output file {output_file} was not created."

# Verify the structure of the output
assert "ride_id" in df_result.columns, "'ride_id' column is missing from the output."
assert "y_pred" in df_result.columns, "'y_pred' column is missing from the output."
