 #!/bin/sh
export BACKEND_STORE_URI="postgresql://${MLFLOWDB_USER}:${MLFLOWDB_PASSWORD}@${MLFLOWDB_ENDPOINT}/${MLFLOWDB_DBNAME}"

echo "Starting MLflow server..."
mlflow server --backend-store-uri $BACKEND_STORE_URI --default-artifact-root $MLFLOW_ARTIFACT_ROOT --host 0.0.0.0 --port 5000