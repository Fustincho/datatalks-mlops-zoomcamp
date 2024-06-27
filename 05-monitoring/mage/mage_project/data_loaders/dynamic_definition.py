from typing import Dict, List

@data_loader
def load_data(*args, **kwargs) -> List[List[Dict]]:
    """
    In your block, you'll need to return a specific data structure. 
    A dynamic block must return a list of 2 lists of dictionaries 
    (e.g. List[List[Dict]]).
    """
    basepath = 'https://d37ci6vzurychx.cloudfront.net/trip-data/'
    filepaths = [
        basepath + 'green_tripdata_2022-01.parquet',
        basepath + 'green_tripdata_2024-03.parquet'
    ]

    targets = [
        ("green_tripdata", "2022-01"),
        ("green_tripdata", "2022-02"),
        ("green_tripdata", "2022-03"),
        ("green_tripdata", "2022-04")
    ]

    datasets = []
    metadata = [] 
    for i , target in enumerate(targets):
        datasets.append(dict(id=i, type=target[0], date=target[1]))
        metadata.append(dict(block_uuid=f'{i}_{target[0]}_{target[1]}'))
    
    return [
        datasets,
        metadata,
    ]