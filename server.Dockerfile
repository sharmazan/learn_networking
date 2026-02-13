FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY server.py /app/server.py

# Server listens on TCP port 9000
EXPOSE 9000

CMD ["python", "/app/server.py"]

