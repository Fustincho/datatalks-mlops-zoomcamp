if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data(data, *args, **kwargs):

    year = int(kwargs['year'])
    month = int(kwargs['month'])

    output_file = f'mage_project/{year:04d}-{month:02d}-preds.parquet'

    data.to_parquet(
        output_file,
        engine='pyarrow',
        compression=None,
        index=False
    )
