#!/usr/bin/env bash

# Force the execution to be in the same folder as the file
cd "$(dirname "$0")"

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

if [ -z "${LOCAL_IMAGE_NAME}" ]; then 
    LOCAL_TAG=$(date +"%Y-%m-%d-%H-%M")
    export LOCAL_IMAGE_NAME="nyc-taxi-duration-batch:${LOCAL_TAG}"
    echo -e "${BLUE}[INTEGRATION TEST]: LOCAL_IMAGE_NAME is not set. Building a new image with tag: ${LOCAL_IMAGE_NAME}${NC}"
    docker build -f Dockerfile.test -t ${LOCAL_IMAGE_NAME} ..
else
    echo -e "${BLUE}[INTEGRATION TEST]: LOCAL_IMAGE_NAME is set to ${LOCAL_IMAGE_NAME}. No need to build a new image.${NC}"
fi

echo -e "${BLUE}[INTEGRATION TEST]: Starting Docker containers with docker-compose up...${NC}"
docker compose up -d

echo -e "${BLUE}[INTEGRATION TEST]: Waiting for containers to initialize...${NC}"
sleep 5

echo -e "${BLUE}[INTEGRATION TEST]: Executing batch processing pipeline test that saves predictions locally...${NC}"
docker compose exec batch-processing pipenv run python test_local_file.py

ERROR_CODE=$?

if [ ${ERROR_CODE} != 0 ]; then
    echo -e "${RED}[INTEGRATION TEST]: Error occurred during the local file test. Fetching logs and shutting down containers.${NC}"
    docker compose logs
    docker compose down
    exit ${ERROR_CODE}
else
    echo -e "${GREEN}[INTEGRATION TEST]: Local file test passed successfully.${NC}"
fi

echo -e "${BLUE}[INTEGRATION TEST]: Executing batch processing pipeline test that saves predictions to S3...${NC}"

aws --endpoint-url=http://localhost:4566 s3 mb s3://taxi-nyc-duration
aws --endpoint-url=http://localhost:4566 s3 ls

docker compose exec batch-processing pipenv run python test_s3.py

ERROR_CODE=$?

if [ ${ERROR_CODE} != 0 ]; then
    echo -e "${RED}[INTEGRATION TEST]: Error occurred during the S3 test. Fetching logs and shutting down containers.${NC}"
    docker compose logs
    docker compose down
    exit ${ERROR_CODE}
else
    echo -e "${GREEN}[INTEGRATION TEST]: S3 test passed successfully.${NC}"
fi

echo -e "${BLUE}[INTEGRATION TEST]: Executing mock data pipeline test that saves predictions to S3...${NC}"

docker compose exec batch-processing pipenv run python test_mock_data.py

ERROR_CODE=$?

if [ ${ERROR_CODE} != 0 ]; then
    echo -e "${RED}[INTEGRATION TEST]: Error occurred during the S3 test. Fetching logs and shutting down containers.${NC}"
    docker compose logs
    docker compose down
    exit ${ERROR_CODE}
else
    echo -e "${GREEN}[INTEGRATION TEST]: S3 test passed successfully.${NC}"
fi

echo -e "${GREEN}[INTEGRATION TEST]: All tests passed successfully. Shutting down containers.${NC}"
docker-compose down
