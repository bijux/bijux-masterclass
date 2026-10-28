# Reference Answers — Module 07: Streaming and Artifact Integrity

Read after attempting all twelve Streaming and Artifact Integrity exercises. Compare the owner, invariant, counterexample, and oracle rather than copying wording.

## 1. Why is Content-Length insufficient for enforcement?

It may be absent, wrong, or not represent decoded/multipart content as expected. The service must count actual consumed bytes.

## 2. Why must staging and final paths share a filesystem?

Atomic rename semantics generally apply within one filesystem; cross-device moves may fail or degrade to non-atomic copy.

## 3. What does content-addressed storage buy?

Deterministic identity, natural deduplication, immutable paths, and direct integrity expectation between digest and bytes.

## 4. Why publish before metadata in this course?

It prevents visible metadata from pointing to absent content. The remaining orphan window is detectable and recoverable.

## 5. What is the cost of verifying checksum on every download?

It rereads all bytes and adds latency/I/O. Immutable content-addressed paths and periodic/on-demand audit may provide a better balance; policy must be explicit.

## 6. How should interrupted staging be cleaned?

The active request removes its temporary file in `finally`; a periodic startup/audit task removes old unreferenced staging files after a safe age.

## 7. Why not hold a transaction while streaming run events?

Slow or disconnected clients would retain a connection and database snapshot. Read event batches using short queries and stream outside transactions.

## 8. How does SSE reconnect relate to event positions?

A stable event ID/position lets the client report the last received item; the server resumes after that persisted boundary where supported.

## 9. Can two logical artifacts share content bytes?

Yes. Content object identity may be shared while metadata retains separate run/name/owner relationships, subject to policy.

## 10. What should happen when bytes are tampered?

Integrity proof must fail; the service should not silently update the checksum to match unauthorized content.

## 11. Trace bounded content-addressed artifact publication in the primary implementation

The relevant entry points are `capstone/tracks/python-fastapi/src/analysis_service/artifacts.py` and `capstone/tracks/typescript-fastify/src/artifacts.ts`. The required invariant is that staging is bounded, publication is atomic and no-clobber, and the digest names exactly the published bytes.

## 12. Compare bounded content-addressed artifact publication across Python and TypeScript

Both tracks must preserve this invariant: staging is bounded, publication is atomic and no-clobber, and the digest names exactly the published bytes. The intentional difference is that stream APIs differ; the checksum, size, confinement, and idempotent-publish outcome do not.
