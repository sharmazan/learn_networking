FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY client.py /app/client.py

CMD ["python", "/app/client.py"]

