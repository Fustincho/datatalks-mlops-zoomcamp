from scipy import stats
from functools import reduce

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@transformer
def transform(dataset, *args, **kwargs):
     """
    Transforms the dataset by removing rows with NaN values in the 'sid_35606' column
    and filtering out rows based on z-score thresholds.

    This function performs the following steps:
    1. Removes rows with NaN values in the 'sid_35606' column.
    2. Drops the 'datetime' column.
    3. Calculates z-scores for each column.
    4. Filters out rows where any column's z-score exceeds the threshold of 3.

    Parameters:
    dataset (pandas.DataFrame): The input dataset to be transformed.

    Returns:
    pd.DataFrame: The transformed dataset with outliers removed.
    """
    dataset = dataset[~dataset["sid_35606"].isna()]
    dataset.drop(columns="datetime", inplace=True)
    z_scores = dataset.apply(stats.zscore)
    threshold = 3

    masks = []
    for col in dataset.columns:
        masks.append(abs(z_scores[col]) > threshold)

    mask = reduce(lambda x, y: x | y, masks)

    dataset = dataset[~mask]

    return dataset


@test
def test_output(output, *args) -> None:
    assert output is not None, 'The output is undefined'
