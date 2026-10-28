# Worked Answers — Module 07: Streaming and Artifact Integrity

Use these solutions to audit your reasoning for **Streaming and Artifact Integrity**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. Why is Content-Length insufficient for enforcement?

It may be absent, wrong, or not represent decoded/multipart content as expected. The service must count actual consumed bytes.

The chapter’s decisive distinction is this: Read multipart content in fixed chunks, track cumulative size, and abort when the configured maximum is exceeded. Declared Content-Length may permit early rejection but cannot replace measured enforcement because it can be absent or false.

**Evidence.** Test the use case without the framework, then through the transport and durable adapter, including one restart or failure path.

## 2. Why must staging and final paths share a filesystem?

Atomic rename semantics generally apply within one filesystem; cross-device moves may fail or degrade to non-atomic copy.

In the cumulative capstone, the rule becomes concrete: The final path derives from the SHA-256 digest, typically with prefix directories. Identical content converges to one immutable object. Publication uses an atomic filesystem rename within one filesystem; cross-filesystem moves do not provide the same guarantee.

**Evidence.** Interrupt a bounded transfer, inspect staging cleanup, then verify atomic publication, checksum, memory bound, and owner-authorized retrieval.

## 3. What does content-addressed storage buy?

Deterministic identity, natural deduplication, immutable paths, and direct integrity expectation between digest and bytes.

A useful way to reason about the boundary is: Artifact metadata stores checksum, byte size, media type, owner, run, and path identity. Retrieval verifies enough metadata/path consistency to detect tampering. Full checksum-on-every-download is a policy trade-off; the course includes an explicit audit command and verification path.

**Evidence.** Test the use case without the framework, then through the transport and durable adapter, including one restart or failure path.

## 4. Why publish before metadata in this course?

It prevents visible metadata from pointing to absent content. The remaining orphan window is detectable and recoverable.

The implementation consequence is: Filesystem and PostgreSQL cannot commit atomically in this design. Publishing first avoids metadata pointing to missing content, but a crash before metadata commit can leave an orphan. The course records, audits, and safely removes orphans after a retention window.

**Evidence.** Test the use case without the framework, then through the transport and durable adapter, including one restart or failure path.

## 5. What is the cost of verifying checksum on every download?

It rereads all bytes and adds latency/I/O. Immutable content-addressed paths and periodic/on-demand audit may provide a better balance; policy must be explicit.

The important nuance is: The Streaming and Artifact Integrity increment must preserve the frozen API and every earlier durability invariant while delivering this result: Implement streamed upload, content-addressed publication, checksums, SSE/NDJSON progress, and authorized download The comparison track must expose the same public outcomes even when internal libraries and control flow differ.

## 6. How should interrupted staging be cleaned?

The active request removes its temporary file in `finally`; a periodic startup/audit task removes old unreferenced staging files after a safe age.

Under concurrency or failure, the distinction becomes: Incomplete bytes live under a staging directory that no download route serves. A unique temporary name prevents collisions. Failure or disconnect removes the staged file. Publication occurs only after validation and checksum finalization.

**Evidence.** Test the use case without the framework, then through the transport and durable adapter, including one restart or failure path.

## 7. Why not hold a transaction while streaming run events?

Slow or disconnected clients would retain a connection and database snapshot. Read event batches using short queries and stream outside transactions.

The design remains honest only if: SSE uses text event framing and blank-line termination; NDJSON uses one complete JSON value per line. Both carry stable event IDs/positions so consumers can detect order and reconnect. Neither changes the durable event source.

**Evidence.** Force competing requests against one database transaction boundary and inspect public responses, uniqueness/version rows, and rollback state after restart.

## 8. How does SSE reconnect relate to event positions?

A stable event ID/position lets the client report the last received item; the server resumes after that persisted boundary where supported.

The consumer-facing consequence is: SSE uses text event framing and blank-line termination; NDJSON uses one complete JSON value per line. Both carry stable event IDs/positions so consumers can detect order and reconnect. Neither changes the durable event source.

**Evidence.** Test the use case without the framework, then through the transport and durable adapter, including one restart or failure path.

## 9. Can two logical artifacts share content bytes?

Yes. Content object identity may be shared while metadata retains separate run/name/owner relationships, subject to policy.

The operational consequence is: Claim Required evidence ---: --- --- 1 upload memory bounded Write the narrow command and machine-readable oracle. 2 size limit enforced by measured bytes Write the narrow command and machine-readable oracle. 3 interrupted upload unpublished Write the narrow command and machine-readable oracle. 4 atomic final rename Write the narrow command and machine-readable oracle. 5 checksum matches bytes Write the narrow command and machine-readable oracle.

## 10. What should happen when bytes are tampered?

Integrity proof must fail; the service should not silently update the checksum to match unauthorized content.

The strongest engineering interpretation is: For Streaming and Artifact Integrity , record the inherited API behavior, the new durable rule, one rejected alternative, the first counterexample, and the exact application, adapter, migration, or proof artifact that owns the choice.

**Counterexample.** The service passes in one process but loses the invariant after restart, concurrency, or a partial dependency failure.

**Evidence.** Test the use case without the framework, then through the transport and durable adapter, including one restart or failure path.

## 11. Trace bounded content-addressed artifact publication in the primary implementation

The relevant entry points are `capstone/tracks/python-fastapi/src/analysis_service/artifacts.py` and `capstone/tracks/typescript-fastify/src/artifacts.ts`. The required invariant is that staging is bounded, publication is atomic and no-clobber, and the digest names exactly the published bytes.

The defect-oriented view is: The excerpt for Streaming and Artifact Integrity isolates one mechanism from the full service. Before copying it, locate the decision or transaction boundary, state the assumption it makes, trace cleanup on failure, and name the regression that would expose moving the guard elsewhere.

## 12. Compare bounded content-addressed artifact publication across Python and TypeScript

Both tracks must preserve this invariant: staging is bounded, publication is atomic and no-clobber, and the digest names exactly the published bytes. The intentional difference is that stream APIs differ; the checksum, size, confinement, and idempotent-publish outcome do not.

Across the Python and TypeScript tracks, the invariant is: The Streaming and Artifact Integrity increment must preserve the frozen API and every earlier durability invariant while delivering this result: Implement streamed upload, content-addressed publication, checksums, SSE/NDJSON progress, and authorized download The comparison track must expose the same public outcomes even when internal libraries and control flow differ.
