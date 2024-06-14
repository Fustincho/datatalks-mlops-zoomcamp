import numpy as np
import pandas as pd

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):

    data, X_val, model = data
    
    y_pred = model.predict(X_val)

    mean_pred = np.mean(y_pred)
    std_pred = np.std(y_pred)

    print(f'Prediction metrics - Mean: {mean_pred}, Std: {std_pred}')
    
    df_result = pd.DataFrame({'ride_id': data['ride_id'], 'y_pred': y_pred})

    return df_result


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
