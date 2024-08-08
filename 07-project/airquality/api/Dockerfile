FROM python:3.10.14-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -U pip && pip install --no-cache-dir -r requirements.txt

COPY main.py .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
