from evidently import ColumnMapping
from evidently.report import Report

from evidently.metrics import DatasetDriftMetric


if "custom" not in globals():
    from mage_ai.data_preparation.decorators import custom

x_sensors_colnames = [
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


@custom
def transform_custom(data, *args, **kwargs):
    """
    Generates a dataset drift metric report using Evidently and returns the result
    along with the complete current dataset.

    Parameters:
    data (tuple): A tuple containing two pandas DataFrames:
                  - reference_data: DataFrame containing the historical sensor data.
                  - current_data: DataFrame containing the current sensor data.

    Returns:
    tuple: A tuple containing:
           - pandas.DataFrame: The complete current data including 'datetime' and sensor columns.
           - float: The drift share indicating the proportion of drifted features.
    """
    reference_data, current_data = data

    complete_current_data = current_data.copy()

    reference_data = reference_data[x_sensors_colnames]
    current_data = current_data[x_sensors_colnames]

    column_mapping = ColumnMapping(
        target=None, numerical_features=x_sensors_colnames, categorical_features=None
    )

    report = Report(
        metrics=[
            DatasetDriftMetric()
        ]  # + [ColumnDriftMetric(column_name=sensor) for sensor in x_sensors_colnames],
    )

    report.run(
        reference_data=reference_data[-700:],
        current_data=current_data,
        column_mapping=column_mapping,
    )

    drift_share = report.as_dict()["metrics"][0]["result"]["drift_share"]

    return complete_current_data[
        ["datetime"] + x_sensors_colnames + ["sid_35606"]
    ], drift_share
