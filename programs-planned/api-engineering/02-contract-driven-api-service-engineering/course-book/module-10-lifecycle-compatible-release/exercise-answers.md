# Reference Answers — Module 10: Lifecycle and Compatible Release

Read after attempting all twelve Lifecycle and Compatible Release exercises. Compare the owner, invariant, counterexample, and oracle rather than copying wording.

## 1. Differentiate liveness and readiness for the API.

Liveness says the process loop is functioning; readiness says the instance has valid configuration/schema and can serve requests. Temporary database failure may make it unready without proving the process is dead.

## 2. What should worker readiness check?

Valid configuration, reachable database, required migrations, and ability to participate in claims; it need not run a complete analysis.

## 3. Why should application replicas not all run migrations automatically?

It obscures ownership, creates startup races, and couples traffic admission to schema mutation. A controlled migration step is reviewable and ordered.

## 4. What is the safe rollback point in expand–backfill–enforce?

Application code can roll back while schema remains expanded and old-compatible. After destructive enforcement, rollback may no longer be safe without another migration.

## 5. Why can old and new code coexist after expansion?

The new field/structure is optional or has compatible defaults; old code can ignore it and new code tolerates its absence until backfill/contract.

## 6. What makes a container build reproducible enough for this course?

Pinned base/runtime/dependencies, deterministic source inputs, no startup installation, recorded versions, and manifest/checksum evidence. Bit-for-bit image reproducibility is not claimed unless measured.

## 7. How should a worker handle SIGTERM while processing?

Stop claiming; either finish a bounded guarded commit or cease/close so the lease expires and another worker recovers. Never fabricate completion.

## 8. Why is a long SSE connection relevant to drain?

The server must decide whether to close/reconnect streams within drain deadline and ensure no DB transaction or file handle leaks.

## 9. What should startup logs include and exclude?

Include release, schema target, role, non-secret configuration categories, and readiness result; exclude tokens, DSNs with passwords, webhook secrets, and payloads.

## 10. Why is breaking API 1.2.0 candidate rejected even if database migration succeeds?

The public contract change is breaking for consumers. Internal schema capability does not override API compatibility policy.

## 11. Trace compatible service and schema release in the primary implementation

The relevant entry points are `capstone/tracks/python-fastapi/src/analysis_service/config.py` and `capstone/tracks/typescript-fastify/src/config.ts`. The required invariant is that old and new service versions coexist during expand/backfill/enforce without weakening API 1.1 or API 1.2 behavior.

## 12. Compare compatible service and schema release across Python and TypeScript

Both tracks must preserve this invariant: old and new service versions coexist during expand/backfill/enforce without weakening API 1.1 or API 1.2 behavior. The intentional difference is that configuration loaders differ; release identity, migration order, health, and rollback limits are shared.
