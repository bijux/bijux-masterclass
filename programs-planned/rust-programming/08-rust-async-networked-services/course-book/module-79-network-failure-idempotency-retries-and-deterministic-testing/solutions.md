# Reasoned Solutions — Module 79: Network Failure, Idempotency, Retries, and Deterministic Testing

[Return to the workbook](workbook.md) · [Return to the chapter](index.md) · [Open the JobWire guide](../capstone.md)

The governing correction is that retry is a semantic protocol, not a loop around I/O. The server must recognize one operation across attempts and preserve enough state to resolve ambiguity.

## Part 1 — Prediction solutions

1. No. The server may have committed and lost the response.
2. Each retry may become a new semantic operation and duplicate effects.
3. No. Reusing a key with changed meaning is a conflict and must be rejected.
4. The server can execute the same semantic request again after eviction, violating the advertised idempotency window.
5. A protocol defect or incompatible peer may be retried repeatedly, amplifying load and hiding a permanent failure.
6. Clients synchronize into retry waves that strike the service at the same times.
7. Machine load and scheduling can delay or accelerate tasks. Use paused time and explicit state gates.
8. No, not unless records are persisted or shared externally. In-memory scope ends with the process.

## Part 2 — Repair reasoning

Construct one canonical request and idempotency key before the loop. Classify failures by phase and policy. The server inserts an in-progress record at commit, stores terminal successes and terminal domain failures, rejects changed fingerprints, and bounds retention. The retry loop carries one deadline and injects deterministic jitter. Tests script exact outcomes and advance virtual time.

## Part 3 — Focused exercise guidance

The fingerprint excludes request IDs because those identify wire attempts, not semantic meaning. It includes every operation and payload field that changes the effect. In-progress duplicates should either attach bounded waiters or receive a stable in-progress response.

Malformed response is normally nonretryable because the peer violated the agreed protocol. Busy and selected transport failures may retry. Reset after write is retryable only with the same idempotency identity.

## Part 4 — Laboratory comparison

A strong client reports attempt history without losing the final causal error. A strong server proves one handler execution under disconnect-after-commit. The test asserts counts and record states, not only eventual success.

## Part 5 — Capstone comparison

JobWire’s process-local record is sufficient for the course’s single-process service and explicitly not restart-durable. Terminal domain errors are cached so repeated invalid semantic requests do not rerun. Eviction policy and client retry window must agree.

## Part 6 — Reconstruction and defense

A complete defense separates transport observation from application commit, request ID from semantic key, retryable from permanent failure, and wall-clock waiting from deterministic virtual time. It states the exact lifetime and scope of the idempotency guarantee.
