# Python reference track

FastAPI is confined to transport/authentication. Psycopg uses explicit SQL because locks, transaction predicates, and migration compatibility are course material. The API and worker are separate processes from one codebase.

```bash
python -m analysis_service.cli migrate --target 002
uvicorn analysis_service.app:app --reload
python -m analysis_service.worker
```
