import mlflow
import pickle

from typing import Tuple
from sklearn.linear_model import LinearRegression
from sklearn.metrics import root_mean_squared_error
from scipy.sparse._csr import csr_matrix
from sklearn.base import BaseEstimator
from pandas import Series

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data(data: Tuple[csr_matrix, Series, BaseEstimator], *args, **kwargs):
    """
    Exports data to some source.

    Args:
        X_train: training dataset
        y_train: labels (duration)
        dv: DictVectorizer

    Exports:
        Model and DictVectorizer to Mlflow
    """

    # Tracking URI is handled via Docker Compose
    # mlflow.set_tracking_uri('http://mlflow:5000')

    experiment_name = "Homework 3"
    mlflow.set_experiment(experiment_name)

    with mlflow.start_run():
        X_train, y_train, dv = data
        y_train = y_train.values

        lr = LinearRegression()

        lr.fit(X_train, y_train)

        y_pred = lr.predict(X_train)

        rmse = root_mean_squared_error(y_train, y_pred)

        mlflow.log_metric("train_rmse", rmse)

        print(f"The intercept value is: {lr.intercept_}")

        with open("homework_03/artifacts/dict_vectorizer.pkl", "wb") as f:
            pickle.dump(dv, f)

        mlflow.log_artifact("homework_03/artifacts/dict_vectorizer.pkl")
        mlflow.sklearn.log_model(lr, artifact_path='artifact')
