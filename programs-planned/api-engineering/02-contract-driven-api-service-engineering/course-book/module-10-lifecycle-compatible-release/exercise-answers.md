# Worked Answers — Module 10: Lifecycle and Compatible Release

Use these solutions to audit your reasoning for **Lifecycle and Compatible Release**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. Differentiate liveness and readiness for the API.

Liveness says the process loop is functioning; readiness says the instance has valid configuration/schema and can serve requests. Temporary database failure may make it unready without proving the process is dead.

The chapter’s decisive distinction is this: Liveness reports that the process is functioning and should not be restarted merely because a dependency is temporarily unavailable. Readiness reports whether the instance should receive its role’s work. The API may be unready when migrations are missing; a worker may be unready when it cannot reach PostgreSQL.

## 2. What should worker readiness check?

Valid configuration, reachable database, required migrations, and ability to participate in claims; it need not run a complete analysis.

In the cumulative capstone, the rule becomes concrete: Required settings, types, ranges, secret sources, paths, and environment-specific restrictions are validated at startup. Defaults are safe for local course use but not silently reused for production-designated environments. Configuration appears in evidence without exposing secret values.

**Evidence.** Kill a worker after claim or partial work, expire the lease, start a replacement, and prove one final effect plus rejection of the stale generation.

## 3. Why should application replicas not all run migrations automatically?

It obscures ownership, creates startup races, and couples traffic admission to schema mutation. A controlled migration step is reviewable and ordered.

A useful way to reason about the boundary is: During rolling release, old and new application versions may access the same expanded schema. New code must write data old code tolerates; old code must not erase new fields. The course runs service 1.0 and service 1.1 sequentially/concurrently against migration phases.

## 4. What is the safe rollback point in expand–backfill–enforce?

Application code can roll back while schema remains expanded and old-compatible. After destructive enforcement, rollback may no longer be safe without another migration.

The implementation consequence is: Application rollback is possible while schema remains in its backward-compatible expanded form. Destructive enforcement is delayed because database rollback may be impossible or expensive. Release notes state the last safe rollback point.

**Evidence.** Test the use case without the framework, then through the transport and durable adapter, including one restart or failure path.

## 5. Why can old and new code coexist after expansion?

The new field/structure is optional or has compatible defaults; old code can ignore it and new code tolerates its absence until backfill/contract.

The important nuance is: During rolling release, old and new application versions may access the same expanded schema. New code must write data old code tolerates; old code must not erase new fields. The course runs service 1.0 and service 1.1 sequentially/concurrently against migration phases.

## 6. What makes a container build reproducible enough for this course?

Pinned base/runtime/dependencies, deterministic source inputs, no startup installation, recorded versions, and manifest/checksum evidence. Bit-for-bit image reproducibility is not claimed unless measured.

Under concurrency or failure, the distinction becomes: The container/image is built from pinned dependencies and source, runs as non-root, writes only declared volumes, and does not install packages at startup. The same artifact is promoted between release steps; configuration changes outside it.

**Evidence.** Test the use case without the framework, then through the transport and durable adapter, including one restart or failure path.

## 7. How should a worker handle SIGTERM while processing?

Stop claiming; either finish a bounded guarded commit or cease/close so the lease expires and another worker recovers. Never fabricate completion.

The design remains honest only if: Shutdown first stops admission, then waits a bounded period for active requests or work, closes resources, and exits. Timeout behavior is explicit. Streams and uploads receive cancellation and cleanup; workers stop claiming before handling current authority.

**Evidence.** Kill a worker after claim or partial work, expire the lease, start a replacement, and prove one final effect plus rejection of the stale generation.

## 8. Why is a long SSE connection relevant to drain?

The server must decide whether to close/reconnect streams within drain deadline and ensure no DB transaction or file handle leaks.

The consumer-facing consequence is: The excerpt for Lifecycle and Compatible Release isolates one mechanism from the full service. Before copying it, locate the decision or transaction boundary, state the assumption it makes, trace cleanup on failure, and name the regression that would expose moving the guard elsewhere.

**Evidence.** Test the use case without the framework, then through the transport and durable adapter, including one restart or failure path.

## 9. What should startup logs include and exclude?

Include release, schema target, role, non-secret configuration categories, and readiness result; exclude tokens, DSNs with passwords, webhook secrets, and payloads.

The operational consequence is: The Lifecycle and Compatible Release increment must preserve the frozen API and every earlier durability invariant while delivering this result: Build lifecycle controls, compatible expand/backfill/enforce migrations, rollback evidence, and release proof The comparison track must expose the same public outcomes even when internal libraries and control flow differ.

## 10. Why is breaking API 1.2.0 candidate rejected even if database migration succeeds?

The public contract change is breaking for consumers. Internal schema capability does not override API compatibility policy.

The strongest engineering interpretation is: For Lifecycle and Compatible Release , record the inherited API behavior, the new durable rule, one rejected alternative, the first counterexample, and the exact application, adapter, migration, or proof artifact that owns the choice.

**Evidence.** Run empty-database migrations and an old/new coexistence sequence with expansion, rollback, backfill, enforcement, and public conformance.

## 11. Trace compatible service and schema release in the primary implementation

The relevant entry points are `capstone/tracks/python-fastapi/src/analysis_service/config.py` and `capstone/tracks/typescript-fastify/src/config.ts`. The required invariant is that old and new service versions coexist during expand/backfill/enforce without weakening API 1.1 or API 1.2 behavior.

The defect-oriented view is: The ten module results now satisfy this course promise: A PostgreSQL-backed service with transactions, durable jobs, bounded artifacts, reliable webhooks, and a compatible API 1.2 release. The next course is API Security Engineering ; it consumes the outgoing handoff rather than reinterpreting completed work.

## 12. Compare compatible service and schema release across Python and TypeScript

Both tracks must preserve this invariant: old and new service versions coexist during expand/backfill/enforce without weakening API 1.1 or API 1.2 behavior. The intentional difference is that configuration loaders differ; release identity, migration order, health, and rollback limits are shared.

Across the Python and TypeScript tracks, the invariant is: Claim Required evidence ---: --- --- 1 startup config matrix Write the narrow command and machine-readable oracle. 2 role-specific health semantics Write the narrow command and machine-readable oracle. 3 graceful API drain Write the narrow command and machine-readable oracle. 4 worker recovery on shutdown Write the narrow command and machine-readable oracle. 5 non-root reproducible build Write the narrow command and machine-readable oracle.
