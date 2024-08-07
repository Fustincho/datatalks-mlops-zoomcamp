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
        "Authorization": "Bearer 61a8842835644709bcbfeefbf91c93c0"
    }

    data = {
        "pipeline_run": {
            "variables": {
                "experiment_name": kwargs['experiment_name']
            }
        }
    }

    response = requests.post(url, headers=headers, json=data)