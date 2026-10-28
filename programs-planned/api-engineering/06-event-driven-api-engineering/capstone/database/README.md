# Event persistence schema

The canonical migration chain is `001` through `012`. Revisions `001`–`009` are inherited unchanged. Course 6 adds:

- `010`: transactional event outbox and consumer inbox;
- `011`: bounded replay checkpoints and dead-letter custody;
- `012`: event contract catalogue, consumer compatibility declarations, and release decisions.

Use a disposable PostgreSQL database for the laboratory:

```bash
TEST_DATABASE_URL=postgresql://course6:fixture-course6@localhost:54326/analysis_events \
  capstone/database/apply-migrations.sh
TEST_DATABASE_URL=... make postgres-proof
```

Migration 009 contains concurrent index creation and is therefore executed as its own `psql` invocation. Never wrap the complete chain in one transaction merely for convenience.
