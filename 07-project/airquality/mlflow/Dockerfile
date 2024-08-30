FROM python:3.11-slim

ENV MLFLOW_HOME=/mlflow
ENV AWS_DEFAULT_REGION=us-east-1

WORKDIR $MLFLOW_HOME

COPY requirements.txt .
COPY entrypoint.sh .

RUN pip install -U pip && pip install -r requirements.txt && chmod +x entrypoint.sh

EXPOSE 5000

ENTRYPOINT ["./entrypoint.sh"]
