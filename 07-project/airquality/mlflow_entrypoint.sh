#!/bin/bash

LOCALSTACK_ENDPOINT="http://localstack:4566"
BUCKET_NAME="mlflow"

until (aws --endpoint-url=$LOCALSTACK_ENDPOINT s3 ls > /dev/null 2>&1); do
  echo "Waiting for LocalStack S3 service..."
  sleep 5
done

# Create S3 bucket (MLflow artifact store)
echo "Creating S3 bucket ${BUCKET_NAME} in LocalStack..."
aws --endpoint-url=$LOCALSTACK_ENDPOINT s3 mb s3://$BUCKET_NAME

echo "Starting MLflow server..."
mlflow server \
  --backend-store-uri postgresql://mlflow_user:mlflow_password@mlflowdb/mlflow_db \
  --default-artifact-root s3://$BUCKET_NAME \
  --host 0.0.0.0 \
  --port 5000
