# Database performance laboratory

The database lab uses the exact Course 2 schema and migrations through 008, then applies migration 009.

## Full proof

```bash
TEST_DATABASE_URL=postgresql://... make postgres-proof
```

The live route:

1. applies migrations in a disposable database;
2. loads a declared skewed fixture;
3. captures `EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)`;
4. runs the `WL-RUN-LIST` and `WL-RUN-SUBMIT` workloads;
5. applies migration 009 using non-transactional concurrent-index steps;
6. repeats plans and workloads;
7. runs owner-isolation and stable-pagination oracles;
8. records index sizes and write cost.

Packaged plan fixtures support parser and review exercises when PostgreSQL is unavailable. They are not a substitute for live plan execution.
