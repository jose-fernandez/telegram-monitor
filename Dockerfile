FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV MONITOR_DATA_DIR=/app/data

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY main_cli.py .

RUN mkdir -p /app/data

CMD ["python", "main_cli.py"]
