FROM python:3.13.5-slim
WORKDIR /app
COPY server.py /app/server.py
USER 65532:65532
EXPOSE 8090
ENTRYPOINT ["python", "/app/server.py"]
