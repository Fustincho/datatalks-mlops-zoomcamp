FROM python:3.10.13-slim

WORKDIR /app

COPY batch_processing.py .
COPY model.bin .
COPY Pipfile Pipfile.lock /app/

RUN pip install -U pip && pip install pipenv 
RUN pipenv install --deploy --ignore-pipfile

ENTRYPOINT ["pipenv", "run", "python", "batch_processing.py"]