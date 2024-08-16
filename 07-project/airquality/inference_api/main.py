import os
from typing import List

import mlflow
import mlflow.pyfunc
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

mlflow.set_tracking_uri(os.environ["MLFLOW_TRACKING_URI"])

MODEL_NAME = "openaq-medellin-35606-xgboost-imputer"
MODEL_VERSION_ALIAS = "champion"

model_uri = f"models:/{MODEL_NAME}@{MODEL_VERSION_ALIAS}"
model = mlflow.pyfunc.load_model(model_uri)

app = FastAPI()


# Define the request model
class DataInput(BaseModel):
    sid_20466: float | None
    sid_34845: float | None
    sid_34841: float | None
    sid_35394: float | None
    sid_35577: float | None
    sid_35843: float | None
    sid_36047: float | None
    sid_36066: float | None
    sid_36064: float | None
    sid_36092: float | None


# Define the batch request model
class BatchDataInput(BaseModel):
    batch: List[DataInput]


@app.post("/predict")
def predict(data: DataInput):
    input_data = pd.DataFrame([data.model_dump()])
    predictions = model.predict(input_data)
    return {"prediction": predictions.tolist()}


@app.post("/predict_batch")
def predict_batch(data: BatchDataInput):
    input_data = pd.DataFrame([item.model_dump() for item in data.batch])
    predictions = model.predict(input_data)
    return {"predictions": predictions.tolist()}
