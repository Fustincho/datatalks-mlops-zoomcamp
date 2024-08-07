import pandas as pd
from datetime import datetime, timezone

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    """
    Transforms and pivots sensor data within a specified date range.

    This function takes raw sensor data, concatenates it into a single DataFrame,
    and then pivots the DataFrame so that each sensor's data becomes a column.

    Parameters:
    data (list): A list of lists containing DataFrames for each sensor.
    **kwargs: Pipeline variables specifying the start / end dates.

    Returns:
    pd.DataFrame: A pivoted DataFrame with datetime as the index and each sensor's
                  data as separate columns. Sensor cols are prefixed with 'sid_'.
    """
    start_date = datetime(
        int(kwargs['y_start']), int(kwargs['m_start']), int(kwargs['d_start']),
        tzinfo=timezone.utc
    )
    end_date = datetime(
        int(kwargs['y_end']), int(kwargs['m_end']), int(kwargs['d_end']),
        tzinfo=timezone.utc
    )

    dfs = []
    for sensor_df in data:
        # The reduce output block returns a list of lists of returns. 
        # (In this case, a lists of lists with the dataframe)
        dfs.append(sensor_df)
    concatenated_df = pd.concat(dfs, ignore_index=True)

    pivot_df = concatenated_df.pivot(index='datetime', columns='sensor_id', values='value').reset_index()
    pivot_df = pivot_df.rename_axis(None, axis=1)
    pivot_df.columns = [f'sid_{col}' if isinstance(col, int) else col for col in pivot_df.columns[:]]

    return pivot_df

@test
def test_output(output, *args) -> None:
    assert output is not None, 'The output is undefined'
