FROM --platform=linux/amd64 python:3.11-slim

ENV MLFLOW_HOME /mlflow \
    AWS_DEFAULT_REGION us-east-1

WORKDIR $MLFLOW_HOME

COPY requirements.txt .
COPY entrypoint.sh .

RUN pip install -U pip && pip install -r requirements.txt && chmod +x entrypoint.sh

EXPOSE 5000

CMD ["./entrypoint.sh"]
