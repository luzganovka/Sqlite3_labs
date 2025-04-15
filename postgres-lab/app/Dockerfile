FROM python:3.11-slim

WORKDIR /app

COPY scripts/ ./scripts

RUN pip install --no-cache-dir psycopg2-binary

CMD ["python", "./scripts/fill_db.py"]