FROM python:3.13-slim

WORKDIR /app

COPY engine.py .
COPY rules.json .

CMD ["python", "/app/engine.py", "daemon", "--rules", "/app/rules.json", "--events", "/data/security-events.jsonl", "--alerts", "/data/security-alerts.jsonl"]
