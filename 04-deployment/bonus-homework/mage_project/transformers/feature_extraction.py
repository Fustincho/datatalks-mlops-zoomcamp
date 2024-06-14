import numpy as np
import pickle

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@transformer
def transform(data, *args, **kwargs):
    
    with open('./mage_project/model.bin', 'rb') as f_in:
        dv, model = pickle.load(f_in)

    categorical = ['PULocationID', 'DOLocationID']

    dicts = data[categorical].to_dict(orient='records')
    X_val = dv.transform(dicts)

    return data, X_val, model


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
