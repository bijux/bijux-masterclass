# Python provider

A FastAPI implementation of the canonical contract. It is intentionally in-memory and deterministic.

```bash
uvicorn analysis_api.app:app --app-dir services/python-fastapi/src --port 8000
pytest services/python-fastapi/tests
```

Training credentials:

| Credential | Principal | Purpose |
|---|---|---|
| `Bearer learner-read` | `learner` | read scopes only |
| `Bearer learner-write` | `learner` | normal read/write scopes |
| `Bearer other-owner` | `other` | ownership-boundary tests |
| `Bearer admin` | `admin` | all scopes and internal diagnostics |
| `X-API-Key: demo-api-key` | `learner` | alternative API-key path |

The provider does not host OAuth. The OpenAPI security scheme describes the production-shaped contract; deterministic tokens make local proof reproducible.
