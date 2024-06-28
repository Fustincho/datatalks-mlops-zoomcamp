
# Homework 6: Best Practices

This homework builds upon the results from Homework 4. This time, we will focus on creating unit tests and integration tests for our batch processing script. Additionally, we will create a Makefile to orchestrate various actions such as linting and formatting.

## Table of Contents

- [Homework 6: Best Practices](#homework-6-best-practices)
  - [Table of Contents](#table-of-contents)
  - [Getting Started](#getting-started)
  - [Tests](#tests)
    - [Unit Tests](#unit-tests)
    - [Integration Tests](#integration-tests)
  - [Changes to batch\_processing.py](#changes-to-batch_processingpy)
  - [Homework Solution](#homework-solution)

## Getting Started

To set up your local environment, run the following command:

```sh
make setup
```

## Tests

### Unit Tests

The file `test/test_batch.py` contains unit tests for the data preparation process.

### Integration Tests

The `integration/` directory contains all the files required to run integration tests. Here are the key components:

- **[run.sh](/integration/run.sh)**: This script launches the integration test. You can also run it executing `make integration_test`.
- **test_*.py**: These files contain the test cases and are executed within `run.sh`.
- **[Dockerfile.test](/integration/Dockerfile.test)**: This Dockerfile is used to build a specific image for the integration test.
- **[docker-compose.yml](/integration/docker-compose.yml)**: This file orchestrates the test image with a Localstack service, simulating the upload of the batch processing file to S3.

## Changes to batch_processing.py

- **New flag**: Added a new flag in `click`, `--test`, which allows the batch processing pipeline to run on mock data specified in the homework instead of downloading taxi data.
- **`create_s3_client` function**: Created a new function to handle cases where we need an S3 client connected to Localstack instead of the AWS cloud.

## Homework Solution

1. **Create the "main" block**: To invoke the main function, use the following if statement:

    ```python
    if __name__ == "__main__":
        main()
    ```

2. **Create Folder and Files**: To use `pytest`, create a folder named `tests` with the following files:
    - `test_batch.py`: This file contains the tests.
    - `__init__.py`: This file is necessary to allow importing of `batch_processing.py`.

3. **Mock Data Rows**: With the given data, the expected dataframe should have 2 rows. The script filters rides longer than 60 minutes or shorter than a minute. Based on the provided mock data, the remaining rows are 2.

    ```python
    data = [
        (None, None, dt(1, 1), dt(1, 10)),    # 9m
        (1, 1, dt(1, 2), dt(1, 10)),          # 8m
        (1, None, dt(1, 2, 0), dt(1, 2, 59)), # 59s
        (3, 4, dt(1, 2, 0), dt(2, 2, 1)),     # 1h1s 
    ]
    ```

4. **AWS CLI S3 Commands for Localstack**: Use the `--endpoint-url` option to adjust AWS CLI S3 commands for Localstack.

    Examples:

    ```sh
    aws --endpoint-url=http://localhost:4566 s3api list-buckets           # List buckets
    aws --endpoint-url=http://localhost:4566 s3 ls                        # List buckets
    aws --endpoint-url=http://localhost:4566 s3 mb s3://taxi-nyc-duration # Create a bucket
    ```

5. **Integration Test with Mock Data**: Create a test using the mock data from question 3. The size of the output file is 1868 bytes.

6. **Sum of Predicted Durations**: Create an integration test using the mock data from question 3. The sum of predicted durations for the test dataframe is 36.27725045203073.

    **Both answers (for question 5 and 6) are output to the console when running the integration test:**

    ```sh
    make integration_test
    ...
    Homework Q5: File size in S3: 1868 bytes
    Homework Q6: Sum of predictions: 36.27725045203073
    ...
    ```
