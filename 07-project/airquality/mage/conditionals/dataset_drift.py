if "condition" not in globals():
    from mage_ai.data_preparation.decorators import condition


@condition
def evaluate_condition(data, *args, **kwargs) -> bool:
    """
    Evaluates the dataset drift from the update_training_data and determines whether
    it exceeds a specified threshold.

    Parameters:
    data (tuple): A tuple containing the dataset and the dataset drift share.
                  - data[0]: The complete current data.
                  - data[1]: The drift share indicating the proportion of drifted features.

    Returns:
    bool: True if the drift share is greater than or equal to 0.5, otherwise False.
    """
    if data[1] >= 0.5:
        return True
    else:
        return False
