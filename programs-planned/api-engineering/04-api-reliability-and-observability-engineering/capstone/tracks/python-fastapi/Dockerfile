FROM python:3.14.7-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
RUN useradd --create-home --uid 10001 app
WORKDIR /app
COPY pyproject.toml ./
COPY src ./src
COPY migrations ./migrations
COPY fixtures ./fixtures
RUN pip install --no-cache-dir .
USER app
EXPOSE 8000
CMD ["uvicorn","analysis_service.app:app","--host","0.0.0.0","--port","8000"]
