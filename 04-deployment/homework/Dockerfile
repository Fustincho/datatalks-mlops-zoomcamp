FROM agrigorev/zoomcamp-model:mlops-2024-3.10.13-slim

WORKDIR /app

COPY taxi_batch_processing.py /app

COPY Pipfile Pipfile.lock /app/

RUN pip install pipenv && pipenv install --deploy --ignore-pipfile

ENTRYPOINT ["pipenv", "run", "python", "taxi_batch_processing.py"]