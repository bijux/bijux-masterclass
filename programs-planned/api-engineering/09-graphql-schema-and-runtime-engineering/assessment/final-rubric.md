# Final assessment rubric

The final assessment is scored out of 100, but critical properties are
non-compensable. A polished schema cannot compensate for cross-tenant data
exposure, unbounded demand, a broken mutation contract, or dishonest partial
failure.

| Area | Points | Required evidence |
|---|---:|---|
| Schema and semantic modeling | 15 | Deliberate nullability, stable identifiers, interfaces/unions, input semantics, and ownership annotations |
| Resolver and composition architecture | 15 | Owner-only source calls, request-scoped batching, no direct database joins, bounded fan-out |
| Pagination and query semantics | 10 | Signed population-bound high-water cursors, stable continuation, filter and tenant binding |
| Mutation correctness | 10 | Source-owned idempotency, expected-version handling, domain result unions, replay and conflict evidence |
| Authorization and exposure | 15 | Field and tenant policy, no call after denial, schema exposure review, resource concealment |
| Demand and cache safety | 10 | Persisted-operation identity, complete budget report, principal-aware caching, rejection before execution |
| Errors and partial data | 10 | Exact paths, truthful nulls, correct bubbling, source identity, no false empty success |
| Subscriptions and resume | 5 | Duplicate suppression, gap detection, bounded buffering, explicit transport boundary |
| Evolution and release | 5 | Directional classification, active-client validation, field ownership, budget and old-client gates |
| Engineering defense | 5 | Clear reasoning, reproducible evidence, residual risks, honest scope claims |

## Non-compensable failures

The submission does not pass if any of the following occurs:

- a resolver reads or writes a private source-service database;
- tenant or field authorization is bypassed;
- denied work still invokes the protected source service;
- an existing cursor can be replayed for another tenant, field, or filter;
- a mutation loses idempotency or expected-version behavior;
- a downstream failure is represented as valid empty data;
- an untrusted arbitrary operation bypasses admission or demand policy;
- a subscription silently skips a sequence;
- a breaking release is accepted;
- a claim is presented as production-proven without the required environment.

A passing score is 85/100 after all non-compensable gates pass. Scores of 95 or
above require not only correct behavior but also clear explanation of trade-offs,
limits, and why rejected alternatives are unsafe.
