FROM --platform=linux/amd64 python:3.11-slim

ENV MLFLOW_HOME /mlflow \
    AWS_DEFAULT_REGION us-east-1 \
    BACKEND_STORE_URI="postgresql://${MLFLOWDB_USER}:${MLFLOWDB_PASSWORD}@${MLFLOWDB_ENDPOINT}/${MLFLOWDB_DBNAME}"

WORKDIR $MLFLOW_HOME

COPY requirements.txt .

RUN pip install -U pip && pip install -r requirements.txt

EXPOSE 5000

CMD ["sh", "-c", "mlflow server --backend-store-uri $BACKEND_STORE_URI --default-artifact-root $MLFLOW_ARTIFACT_ROOT --host 0.0.0.0 --port 5000"]
