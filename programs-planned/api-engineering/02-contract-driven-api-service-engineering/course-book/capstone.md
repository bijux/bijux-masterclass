# Capstone — Contract-Driven API Service Engineering

## One continuing platform

The capstone is the Analysis Runs Platform. Principals create projects, register datasets, submit analysis runs, observe progress, retrieve verified artifacts, and receive or consume completion facts. Course 2 does not replace the platform; it adds the responsibility **make the promise durable**.

## Starting state

The immutable Course 1 API 1.1 handoff and its provider-neutral proof corpus.

## Course increments

| Module | Platform increment |
|---:|---|
| 1 | Create transport, application, and adapter boundaries for the fixed operation ledger. |
| 2 | Implement project, dataset, run, cancellation, and artifact rules as testable domain behavior. |
| 3 | Persist principals, projects, datasets, runs, artifacts, and ownership with constraints and deterministic migrations. |
| 4 | Implement persistent request fingerprints, replayed outcomes, version columns, ETags, and transaction rollback. |
| 5 | Implement owner-bound, filter-bound, high-water keyset traversal and evidence-backed query plans. |
| 6 | Add durable jobs, leases, heartbeats, fencing, cancellation, duplicate-safe effects, and abandoned-work recovery. |
| 7 | Implement streamed upload, content-addressed publication, checksums, SSE/NDJSON progress, and authorized download. |
| 8 | Add a transactional outbox, signed deliveries, retry state, deduplication, and destination constraints. |
| 9 | Assemble pure, integration, concurrent, process-kill, conformance, and planted-defect proofs. |
| 10 | Build lifecycle controls, compatible expand/backfill/enforce migrations, rollback evidence, and release proof. |


## Language tracks

Choose one primary implementation track. Use the second as an idiomatic comparison and shared-vector parity reference.

Shared fixtures, vectors, operation maps, releases, and black-box scenarios define parity. Identical class names or directory shape do not.

## Capstone reading order

1. read the module chapter and identify the owning mechanism;
2. inspect the narrow source path named by the chapter;
3. inspect the corresponding test or vector;
4. run the focused proof;
5. perform the lab modification in a working branch;
6. return to the chapter and explain how the implementation realizes the model.

## Handoff discipline

The predecessor material is read-only evidence. The current course may add a compatible public interface, migration, or profile only when its release rules permit it. It must not rewrite earlier history to simplify the present implementation.

**Outgoing handoff:** A durable API 1.2 service handoff with migrations 001–005, idempotency, optimistic concurrency, stable pagination, worker recovery, artifact integrity, and transactional webhook delivery.

## Final capstone question

Can you trace one accepted case and one rejected, failed, overloaded, or duplicated case from the public boundary to the authoritative outcome, then name the proof and limitation at every layer this course owns?
