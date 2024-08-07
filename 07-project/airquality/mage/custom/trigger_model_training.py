import requests

if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@custom
def transform_custom(*args, **kwargs):
    """
    Trigger the model_training pipeline
    """

    url = "http://localhost:6789/api/pipeline_schedules/2/api_trigger"

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer 0e577da5d92047d6ace0048cd8a1810c"
    }

    data = {
        "pipeline_run": {
            "variables": {
                "experiment_name": kwargs['experiment_name']
            }
        }
    }

    response = requests.post(url, headers=headers, json=data)