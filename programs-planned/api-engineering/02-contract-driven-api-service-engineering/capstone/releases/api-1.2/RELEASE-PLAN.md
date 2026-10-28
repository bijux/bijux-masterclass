# API 1.2.0 / service 1.1 release plan

This release has four independent identifiers:

| Axis | Before | After |
|---|---:|---:|
| OpenAPI specification | 3.1.2 | 3.1.2 |
| Public API | 1.1.0 | 1.2.0 |
| Executable service | 1.0 | 1.1 |
| Database migration | 002 | 005 |

`resultSummary` is an optional, nullable response field during coexistence. The
new artifact-content operation is additive. Neither change permits old service
1.0 processes to stop working against the expanded schema.

## Ordered release

1. Prove service 1.0 against API 1.1.0 and migration 002.
2. Apply migration 003. It adds nullable storage; service 1.0 remains valid.
3. Deploy service 1.1 readers and writers implementing API 1.2.0.
4. Run service 1.0 and service 1.1 against the expanded schema.
5. Demonstrate application rollback to service 1.0 while migration 003 remains.
6. Remove service 1.0 writers.
7. Apply migration 004 and prove the backfill.
8. Apply migration 005 only after no old writer can omit the new value.
9. Prove API 1.1.0 compatibility and API 1.2.0 behavior.

The static compatibility report classifies `resultSummary` as review-required,
not as universally harmless: strict clients that reject unknown response
properties need an explicit migration decision.
