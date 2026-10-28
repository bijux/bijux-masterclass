FROM python:3.13-slim
WORKDIR /app
COPY pyproject.toml ./
RUN pip install --no-cache-dir fastapi==0.128.2 pydantic==2.13.4 python-multipart==0.0.32 uvicorn==0.48.0
COPY src ./src
ENV PYTHONPATH=/app/src
EXPOSE 8000
CMD ["python", "-m", "uvicorn", "analysis_api.app:app", "--host", "0.0.0.0", "--port", "8000"]
