# Data Retrieval and Handling
import os
# Utility Functions and Miscellaneous
import datetime
from scipy import stats
from functools import reduce
# Machine Learning
import xgboost as xgb
# Data Preprocessing
from sklearn.impute import KNNImputer
# Hyperparameter Optimization
import optuna
# Experiment Tracking and Model Management
import mlflow
import mlflow.pyfunc
from mlflow import MlflowClient
# Saving and Loading Models
import pickle

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

class ImputerAndXGBoost(mlflow.pyfunc.PythonModel):
    """
    A custom MLflow model that combines a KNN imputer and an XGBoost model.
    """
    def load_context(self, context):
        """
        Loads the KNN imputer and XGBoost model from artifacts.
        """
        with open(context.artifacts["imputer"], "rb") as f:
            self.imputer = pickle.load(f)
        self.xgboost_model = xgb.Booster()
        self.xgboost_model.load_model(context.artifacts["xgboost_model"])
        
    def predict(self, context, model_input):
        """
        Imputes missing values and makes predictions using the XGBoost model.
        Parameters:
        model_input (pandas.DataFrame): The input data for prediction.

        Returns:
        numpy.ndarray: The predictions from the XGBoost model.
        """
        imputed = self.imputer.transform(model_input)
        dmatrix = xgb.DMatrix(imputed)
        return self.xgboost_model.predict(dmatrix)


@data_exporter
def export_data(dataset, *args, **kwargs):
    """
    Trains a machine learning model, performs hyperparameter optimization,
    and logs the model in MLflow.

    Parameters:
    dataset (pandas.DataFrame): The input dataset used for training.
    *args: Additional arguments.
    **kwargs: Additional keyword arguments.

    Returns:
    None
    """
    X = dataset[
        [
            "sid_20466",
            "sid_34845",
            "sid_34841",
            "sid_35394",
            "sid_35577",
            "sid_35843",
            "sid_36047",
            "sid_36066",
            "sid_36064",
            "sid_36092",
        ]
    ]

    y = dataset["sid_35606"]

    imputer = KNNImputer(n_neighbors=5)
    X_imputed = imputer.fit_transform(X)

    imputer_path = "./mage/artifacts/imputer.pkl"
    with open(imputer_path, "wb") as f:
        pickle.dump(imputer, f)

    MLFLOW_HOST = os.environ("MLFLOW_HOST")
    mlflow.set_tracking_uri(f"http://{MLFLOW_HOST}:5000")

    experiment_name = kwargs['experiment_name']
    current_datetime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    mlflow.set_experiment(f'{experiment_name}_{current_datetime}')

    dtrain = xgb.DMatrix(X_imputed, label=y)

    def objective(trial):
        param = {
            "verbosity": 0,
            "booster": trial.suggest_categorical("booster", ["gbtree", "gblinear", "dart"]),
            "validate_parameters": True,
            "objective": "reg:squarederror",
            "tree_method": "auto",
            "lambda": trial.suggest_float("lambda", 1e-8, 1.0, log=True),
            "alpha": trial.suggest_float("alpha", 1e-8, 1.0, log=True),
            "subsample": trial.suggest_float("subsample", 0.2, 1.0),
            "colsample_bytree": trial.suggest_float("colsample_bytree", 0.2, 1.0),
            "max_depth": trial.suggest_int("max_depth", 3, 9, step=2),
            "n_estimators": trial.suggest_int("n_estimators", 100, 300),
        }

        if param["booster"] in ["gbtree", "dart"]:
            param["eta"] = trial.suggest_float("eta", 1e-8, 1.0, log=True)
            param["max_depth"] = trial.suggest_int("max_depth", 3, 9, step=2)
            param["min_child_weight"] = trial.suggest_int("min_child_weight", 2, 10)
            param["gamma"] = trial.suggest_float("gamma", 1e-8, 1.0, log=True)
            param["grow_policy"] = trial.suggest_categorical("grow_policy", ["depthwise", "lossguide"])

        if param["booster"] == "dart":
            param["sample_type"] = trial.suggest_categorical("sample_type", ["uniform", "weighted"])
            param["normalize_type"] = trial.suggest_categorical("normalize_type", ["tree", "forest"])
            param["rate_drop"] = trial.suggest_float("rate_drop", 1e-8, 1.0, log=True)
            param["skip_drop"] = trial.suggest_float("skip_drop", 1e-8, 1.0, log=True)
        
        with mlflow.start_run():
            mlflow.log_params(param)
            
            # Cross-validation
            cv_results = xgb.cv(
                dtrain=dtrain,
                params=param,
                nfold=5,  # Number of folds
                num_boost_round=200,  # Maximum number of boosting rounds
                early_stopping_rounds=10,  # Stop if no improvement after these rounds
                metrics='rmse',  # Metric to evaluate
                seed=1020
            )
            
            best_rmse = cv_results['test-rmse-mean'].min()
            best_rounds = cv_results['test-rmse-mean'].idxmin()
            
            mlflow.log_metric("best_rmse", best_rmse)
            mlflow.log_metric("best_rounds", best_rounds)

            # Train the model with the best number of rounds on the full training data
            final_model = xgb.train(param, dtrain, num_boost_round=best_rounds)

            xgboost_model_path = "./mage/artifacts/xgboost_model.json"
            final_model.save_model(xgboost_model_path)

            mlflow.pyfunc.log_model(
                artifact_path="model",
                python_model=ImputerAndXGBoost(),
                artifacts={
                    "imputer": imputer_path,
                    "xgboost_model": xgboost_model_path,
                }
            )

        return best_rmse

    optuna.logging.set_verbosity(optuna.logging.WARNING)

    # Create an Optuna study and optimize
    study = optuna.create_study(direction="minimize")
    study.optimize(objective, n_trials=2, timeout=600)

    client = MlflowClient()

    experiment = client.get_experiment_by_name(experiment_name)

    experiment_id = experiment.experiment_id

    runs = client.search_runs(experiment_ids=experiment_id, order_by=["metrics.rmse"], max_results=1)

    best_run = runs[0].to_dictionary()
    # Fetch the best hyperparameters
    best_hyperparameters = best_run['data']['params']

    model_name = "openaq-medellin-35606-xgboost-imputer"
    
    # List all registered models
    registered_models = [model.name for model in client.list_registered_models()]

    # Check if the model already exists
    if model_name not in registered_models:
        # Create the registered model
        client.create_registered_model(model_name)
        print(f"Registered model '{model_name}' created.")
    else:
        print(f"Registered model '{model_name}' already exists.")

    client.set_registered_model_tag(model_name, "task", "regression")

    s3_bucket_name = os.environ["S3_BUCKET_NAME"]

    result = client.create_model_version(
        name=model_name,
        # on log_model we set artifact_path="model"
        source=f"s3://{s3_bucket_name}/{best_run['info']['experiment_id']}/{best_run['info']['run_id']}/artifacts/model", 
        run_id=best_run['info']['run_id'],
    )

    client.set_registered_model_alias(model_name, "champion", result.version)
    client.set_model_version_tag(model_name, result.version, "validation_status", "approved")
