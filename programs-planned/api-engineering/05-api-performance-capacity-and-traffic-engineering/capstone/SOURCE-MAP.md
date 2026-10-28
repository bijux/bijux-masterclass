# Course-book to executable-source map

| Module | Python reference | TypeScript reference | Shared evidence |
|---:|---|---|---|
| 1 | `models.py`, `identity.py`, `workload.py` | `models.ts`, `identity.ts`, `workload.ts` | `performance-case/`, `shared/vectors/identity.json` |
| 2 | `statistics.py`, benchmark harness | `statistics.ts` | `shared/vectors/statistics.json`, benchmark profiles |
| 3 | `http_efficiency.py`, `streaming.py` | `http-efficiency.ts` | `shared/vectors/http.json`, local server |
| 4 | `query_plans.py`, `db_budget.py` | `query-plans.ts` | SQL, migration 009, plan fixtures |
| 5 | `runtime.py`, `profiling.py` | `runtime.ts` | runtime vectors and profiler recipes |
| 6 | `queueing.py`, `admission.py` | `queueing.ts`, `admission.ts` | concurrency budget and queue vectors |
| 7 | `cache.py`, `singleflight.py` | `cache.ts`, `singleflight.ts` | cache catalogue and cache vectors |
| 8 | `traffic.py`, `shedding.py` | `traffic.ts`, `shedding.ts` | traffic policy and traffic vectors |
| 9 | `capacity.py`, `cost.py` | `capacity.ts`, `cost.ts` | capacity scenarios and sensitivity model |
| 10 | `regression.py`, `release.py` | `regression.ts`, `release.ts` | release fixtures and planted defects |
