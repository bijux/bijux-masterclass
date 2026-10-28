# Python consumer

A small handwritten consumer used by the course before and after client generation. It demonstrates the HTTP workflow without hiding contract semantics behind generated convenience methods.

```bash
python -m analysis_client --base-url http://127.0.0.1:8000
pytest clients/python/tests
```

`make clients-generate` also creates a generator-owned package under `generated/`. The handwritten consumer remains stable so learner exercises can compare both styles.
