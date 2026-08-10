FROM python:3.13-slim

WORKDIR /app

RUN pip install --no-cache-dir cryptography==45.0.6

COPY deploy.py .

CMD ["python", "/app/deploy.py"]
