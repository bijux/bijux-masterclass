FROM python:3.13-slim
WORKDIR /app
COPY tracks/python-distributed/src /app/reference
COPY network-lab /app/network-lab
ENV PYTHONPATH=/app/reference:/app/network-lab
ENTRYPOINT ["python", "-m", "network_lab.service"]
