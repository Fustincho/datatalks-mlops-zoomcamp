import pandas as pd
from sklearn.model_selection import train_test_split, ParameterGrid
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import mlflow
import mlflow.xgboost
import xgboost as xgb

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    target = "duration_min"
    num_features = ["passenger_count", "trip_distance", "fare_amount", "total_amount"]
    cat_features = ["PULocationID", "DOLocationID"]

    train_df, val_df = train_test_split(data, test_size=0.2, random_state=1020)

    X_train = train_df[num_features + cat_features]
    y_train = train_df[target]
    X_val = val_df[num_features + cat_features]
    y_val = val_df[target]

    categorical_transformer = OneHotEncoder(handle_unknown='ignore')

    # Create the preprocessor
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', categorical_transformer, cat_features)
        ],
        remainder='passthrough'  # Keep the remaining columns as they are
    )

    param_grid = {
        'max_depth': [3, 4, 5, 6, 7, 8],
        'learning_rate': [0.01, 0.1, 0.2, 0.3, 0.4],
        'n_estimators': [50, 100, 150]
    }
    
    for params in ParameterGrid(param_grid):
            
        with mlflow.start_run():
            # Log the parameters
            mlflow.log_params(params)
            
            # Create a pipeline that includes the preprocessing and the model
            model = Pipeline(steps=[
                ('preprocessor', preprocessor),
                ('regressor', xgb.XGBRegressor(**params, random_state=42))
            ])
            
            # Train the model with the current hyperparameters
            model.fit(X_train, y_train)
            
            # Predict on the validation set
            y_pred = model.predict(X_val)
            
            # Calculate the mean squared error
            mse = mean_squared_error(y_val, y_pred)
            
            # Log the metrics
            mlflow.log_metric("mse", mse)
            
            # Log the model
            mlflow.sklearn.log_model(model, "model")
            
            print(f"Params: {params}, MSE: {mse}")

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
