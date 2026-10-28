# Reasoned Solutions — Module 79: Network Failure, Idempotency, Retries, and Deterministic Testing

[Workbook](workbook.md) · [Chapter](index.md) · [Laboratory](../../labs/module-09-idempotent-retry-client/README.md) · [JobWire guide](../capstone.md)

Use these notes only after preserving your prediction and repair for **Module 79: Network Failure, Idempotency, Retries, and Deterministic Testing**. Compare the reasoning against this question: *When a network operation fails without revealing whether the remote side committed it, how do idempotency, retry budgets, failure classification, and deterministic tests preserve one semantic outcome?* Do not compare line count first. A different implementation is valid when it preserves the same public contract and can defend its ownership, failure, ordering, capacity, safety, compatibility, and evidence consequences.

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

## Deep reasoning and transfer

### Decisive model

> When a network operation fails without revealing whether the remote side committed it, how do idempotency, retry budgets, failure classification, and deterministic tests preserve one semantic outcome?

Build a **retry and commit matrix**. Mark the owner or authority, valid and invalid states, first decisive phase or event, state after failure, and visible consequence. The model is too weak when it records only the API call and not the relationship that makes the call legal or useful.

### Outcome checks

1. **Classify failures by phase, scope, retryability, and commit ambiguity.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
2. **Distinguish idempotent operation semantics from retrying an HTTP or TCP request.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
3. **Design idempotency keys with scope, fingerprint, in-progress state, terminal result, and retention.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
4. **Reject key reuse with different request content.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
5. **Attach duplicate callers to one in-progress operation or return a defined status.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.

### Repair discipline

The weak repair for this module is any change that makes the current example pass by deleting the first outcome: **Classify failures by phase, scope, retryability, and commit ambiguity.** A principled repair preserves that requirement, narrows the unsupported assumption, and makes the deciding fact observable in the retry and commit matrix.

### Reference implementation comparison

For [Idempotent Retry Client](../../labs/module-09-idempotent-retry-client/README.md), compare contract, state transitions, adversarial cases, cleanup, and public behavior before syntax. Identify the earliest operation that could violate the contract and the type, check, protocol, or review procedure that prevents it. Then state when a simpler design would be preferable.

### Capstone transfer

In JobWire, Module 79 is complete only when the new behavior fits the existing authority map. Trace the changed fact from input through validation, state transition, effect, output, and tests. Two components deciding the same fact indicate a second source of truth rather than successful integration.

### Oral defense

Answer these without notes:

1. In **Network Failure, Idempotency, Retries, and Deterministic Testing**, which relationship decides this question: “When a network operation fails without revealing whether the remote side committed it, how do idempotency, retry budgets, failure classification, and deterministic tests preserve one semantic outcome?”
2. What is the smallest causal negative case?
3. Which repair preserves the requirement?
4. Which tempting repair deletes it?
5. What can the chosen evidence falsify, and what remains unproved?
6. How would the design change in a product unrelated to JobWire?
