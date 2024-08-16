FROM --platform=linux/amd64 python:3.11-slim

ENV MLFLOW_HOME /mlflow
ENV AWS_DEFAULT_REGION us-east-1

WORKDIR $MLFLOW_HOME

COPY requirements.txt .

RUN pip install -U pip && pip install -r requirements.txt

EXPOSE 5000

ARG DB_USERNAME
ARG DB_PASSWORD
ARG DB_ENDPOINT
ARG DB_NAME
ARG ARTIFACT_ROOT

ENV BACKEND_STORE_URI="postgresql://${DB_USERNAME}:${DB_PASSWORD}@${DB_ENDPOINT}/${DB_NAME}"

CMD ["mlflow", "server", \
    "--backend-store-uri", "$BACKEND_STORE_URI", \
    "--default-artifact-root", "$ARTIFACT_ROOT", \
    "--host", "0.0.0.0", \
    "--port", "5000"]
