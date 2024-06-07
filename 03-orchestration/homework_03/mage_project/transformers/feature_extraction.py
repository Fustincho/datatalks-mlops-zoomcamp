from typing import Tuple

from pandas import DataFrame, Series
from sklearn.feature_extraction import DictVectorizer
from scipy.sparse._csr import csr_matrix
from sklearn.base import BaseEstimator

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(
    data: DataFrame, *args, **kwargs
) -> Tuple[csr_matrix, Series, BaseEstimator]:
    """
    Extracts categorial features using a DictVectorizer.

    Args:
        data: Filtered DataFrame based on trip duration

    Returns:
        X_train: training dataset
        y_train: labels (duration)
        dv: DictVectorizer
    """
    categorical = ['PULocationID', 'DOLocationID']
    numerical = ['trip_distance']

    train_dicts = data[categorical + numerical].to_dict(orient='records')

    dv = DictVectorizer()

    X_train = dv.fit_transform(train_dicts)

    target = 'duration'
    y_train = data[target]

    return X_train, y_train, dv
    