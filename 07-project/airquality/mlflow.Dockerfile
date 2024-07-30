FROM --platform=linux/amd64 python:3.11-slim

ENV MLFLOW_HOME /mlflow
# https://mlflow.org/docs/latest/python_api/mlflow.environment_variables.html
ENV MLFLOW_S3_ENDPOINT_URL http://localstack:4566
ENV AWS_DEFAULT_REGION us-east-1

WORKDIR $MLFLOW_HOME

# Install MLflow and psycopg2 (for the backend store)
RUN pip install -U pip && pip install mlflow==2.12.1 psycopg2-binary boto3

# Install AWS CLI (https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    && curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip \
    && ./aws/install \
    && rm -rf awscliv2.zip aws

COPY mlflow_entrypoint.sh .

RUN chmod +x mlflow_entrypoint.sh

EXPOSE 5000

ENTRYPOINT [ "./mlflow_entrypoint.sh" ]
