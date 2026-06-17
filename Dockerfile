FROM python:3.12-slim

WORKDIR /app

Run pip install flask

COPY beispiel-server.py .
COPY templates ./templates
COPY static ./static

EXPOSE 5000

CMD ["python", "beispiel-server.py"]

