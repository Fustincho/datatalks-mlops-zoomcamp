LOCAL_TAG:=$(shell date +"%Y-%m-%d-%H-%M")
LOCAL_IMAGE_NAME:=nyc-taxi-duration-batch:${LOCAL_TAG}

test:
	pipenv run pytest tests/

quality_checks:
	pipenv run isort .
	pipenv run black .
	pipenv run pylint --recursive=y .

build: quality_checks test
	docker build -t ${LOCAL_IMAGE_NAME} .

integration_test: quality_checks test
	docker build -t ${LOCAL_IMAGE_NAME} -f integration/Dockerfile.test .
	LOCAL_IMAGE_NAME=${LOCAL_IMAGE_NAME} bash integration/run.sh

setup:
	pipenv install --dev
