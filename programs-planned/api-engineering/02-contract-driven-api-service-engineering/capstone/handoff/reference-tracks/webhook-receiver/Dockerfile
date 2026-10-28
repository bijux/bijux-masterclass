FROM python:3.14.6-slim
WORKDIR /app
RUN useradd --system --uid 10001 --create-home receiver
COPY receiver.py ./receiver.py
RUN mkdir -p /data && chown -R receiver:receiver /app /data
USER receiver
ENV RECEIVER_DATABASE=/data/receiver.sqlite3
EXPOSE 8080
CMD ["python", "receiver.py"]
