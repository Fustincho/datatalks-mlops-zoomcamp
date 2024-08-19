
# How to Use the Air Quality Prediction Model Code

NOTE: make sure you are running these commands in the root folder of the project, that is: [here](https://github.com/Fustincho/datatalks-mlops-zoomcamp/tree/main/07-project/airquality).

For more information about MAGE pipelines go [here](./MAGE_PIPELINES.md)

## 0. Install the dependencies

You can install the necessary dependencies to test locally using Poetry by running:

```bash
poetry install
poetry install --with dev
```

Alternatively, you can create a virtual environment and install the dependencies listed in the `requirements.txt` file by running:

```bash
python -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`
pip install -r requirements.txt
```

## 1. Setting Up the Project Infrastructure

The project infrastructure is managed through Docker, and the services are defined in the `docker-compose.yaml` file. To get started:

- **Build and Start the Services**:
  Run the following command to build and start the services in detached mode:
  ```bash
  docker compose up --build -d
  ```

## 2. Running Data Extraction and ETL

- **Access MAGE AI**:
  Open your browser and navigate to `http://localhost:6789` to access the MAGE AI interface.
  
- **Execute the Data ETL Pipeline**:
  Within MAGE AI, run the `openaq_data_etl` pipeline. This pipeline fetches all necessary training data from OpenAQ and stores it in the PostgreSQL database (`magedb`).

## 3. Model Training

- **Automatic Model Training**:
  After the ETL pipeline completes, the `model_training` pipeline is triggered automatically. This pipeline trains the model using the data stored in `magedb`.
  
  **Note**: The default configuration runs two iterations of the XGBoost model. This can be adjusted in the pipeline configuration for more iterations or other modifications.

## 4. Building and Running the Inference API

- **Navigate to the Inference API Directory**:
  Change to the `inference_api/` directory:
  ```bash
  cd inference_api/
  ```

- **Build the Inference API Container**:
  Run the `build.sh` script to build the inference API container:
  ```bash
  ./build.sh
  ```
  This script will:
  - Fetch the registered MLflow model tagged as `@champion`.
  - Build an API using FastAPI to serve predictions through the `predict/` and `predict_batch/` endpoints.
  - Ensure the API container is connected to the same Docker network (`airquality_default`) as the rest of the infrastructure.

## 5. Simulating Production Calls

- **Perform Batch Predictions**:
  With the model API running, simulate production calls by fetching new data not used in training. For this, you now need to run once the `simulate_production_predictions` pipeline. Use the `predict_batch/` endpoint to make predictions.
  
- **Store Predictions and Actuals**:
  Save both the predicted values and the actual values in a database for monitoring purposes.

## 6. Monitoring and Automatic Retraining

- **Dataset Drift Detection**:
  The `monitoring` pipeline utilizes EvidentlyAI's library to detect dataset drift by comparing the newly predicted values against the training dataset.
  
- **Trigger Retraining**:
  If significant drift is detected, the pipeline automatically triggers retraining. The new data is incorporated into the training set, and the reference dataset used by EvidentlyAI is updated.

## 7. Development and Testing Tools

- **Package Management with Poetry**:
  Use Poetry for dependency management and local testing:
  - To create a virtual environment in the project directory, run:
    ```bash
    poetry config virtualenvs.in-project true
    ```
  - Install the project dependencies:
    ```bash
    poetry install --with dev
    ```

- **Using the Makefile**:
  A `Makefile` is provided to simplify common tasks:
  - **Linting and Formatting**:
    Use the `ruff` linter and formatter:
    ```bash
    make lint
    make format
    ```
  - **Running Tests**:
    - **MAGE AI Tests**: Tests are done block by block.
    - **Inference API Tests**: Run with `pytest`:
      ```bash
      make test
      ```

