# Worked Answers — Module 04: Unary RPCs, Metadata, Status, and Rich Errors

Use these solutions to audit your reasoning for **Unary RPCs, Metadata, Status, and Rich Errors**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. Which fields belong in metadata for `CreateRun`, and which belong in the request message?

Authorization, trace, and bounded transport context belong in metadata. Parent, dataset, algorithm, expected revision, and request identity affect the application decision and belong in the message.

**Decisive evidence:** metadata policy review

The chapter’s decisive distinction is this: A field belongs in the request message when it affects the application decision, needs generated documentation and compatibility governance, or must be included in idempotency fingerprinting. The course keeps request id in CreateRunRequest, making its semantics visible. The identity token remains metadata because it authenticates who invokes the request rather than defining the requested run.

## 2. Map an invalid algorithm, a missing run, and a stale revision to gRPC statuses.

Invalid algorithm is `INVALID_ARGUMENT`; a policy-concealed or absent run is `NOT_FOUND`; a stale optimistic concurrency token is `ABORTED` or the declared precondition status. The profile must choose consistently.

**Decisive evidence:** status vector

In the cumulative capstone, the rule becomes concrete: Cancellation is an application command, not transport cancellation. CancelRunRequest carries the run name, expected ETag or revision token, and request identifier. A stale precondition maps to ABORTED or FAILED PRECONDITION according to the policy's intended client action. A terminal run that cannot be canceled produces a stable precondition violation, not INTERNAL.

## 3. Why is `UNKNOWN` or `INTERNAL` an inadequate default for expected domain conflicts?

Expected conflicts are part of the public contract and require actionable, stable codes. Treating them as internal defects prevents correct client behavior and corrupts reliability metrics.

**Decisive evidence:** status coverage table

A useful way to reason about the boundary is: INTERNAL is not a bucket for every exception. Unexpected faults are logged with an internal incident identity and returned as a sanitized status. Dependency unavailability may map to UNAVAILABLE only when the caller can safely treat the failure as transient. Deadline expiry uses DEADLINE EXCEEDED; cancellation initiated by the caller uses CANCELLED. The status policy records retry classification separately because a code alone does not establish operation safety.

## 4. What makes an error detail safe for a client?

It uses public identifiers and stable reason codes, contains only information the caller is authorized to know, is bounded, and avoids stack, SQL, host, path, and secret data.

**Decisive evidence:** error-detail redaction test

The implementation consequence is: The standard status model carries code, human-readable message, and optional typed details. Details can identify invalid fields, precondition violations, resource information, retry guidance, or a stable domain error code. They must not expose SQL, stack traces, filesystem paths, secrets, internal hostnames, or cross-tenant resource existence.

## 5. Where should a database unique-constraint error be translated?

At the application/transport translation edge after the repository maps the database condition to a domain/application error. Handlers should not parse vendor error strings.

**Decisive evidence:** repository/application error mapping test

The important nuance is: The handler does not catch a database vendor exception and inspect its message. The repository maps the failed compare-and-swap to an application error. The transport mapper owns the gRPC status. The public HTTP adapter then maps that outcome to the exact existing HTTP precondition/conflict behavior. Each layer has one vocabulary and one translation edge.

## 6. Why should a generic interceptor not decide run ownership by itself?

Ownership may require authoritative resource state and operation context. A generic interceptor lacks that context and can separate the check from the mutation.

**Decisive evidence:** authorization placement review

Under concurrency or failure, the distinction becomes: Interceptors are useful for trace context, metric boundaries, authentication parsing, common metadata limits, deadline observation, and final error sanitation. They should not decide whether a principal owns a particular run unless the required resource context and policy are explicitly passed. Hiding resource authorization in a generic interceptor makes call behavior difficult to review and can create time-of-check/time-of-use gaps.

## 7. Describe the ambiguous outcome when `CreateRun` commits but the response is lost.

The client sees failure but the run exists. It must reuse the same bound request identifier or reconcile; generating a new identifier can duplicate the effect.

**Decisive evidence:** post-commit response-loss trace

The design remains honest only if: CreateRun illustrates why unary success is not the whole story. The server may commit the run and idempotency record, then lose the response. The client receives UNAVAILABLE or a deadline failure. It cannot infer whether no run exists. The stable request identifier lets a retry replay the stored outcome, but only if the same semantic input is bound to the identifier.

## 8. Differentiate application `CancelRun` from transport cancellation.

`CancelRun` changes durable application state. Transport cancellation only signals that the caller has stopped waiting; it does not roll back committed work.

**Decisive evidence:** cancellation sequence

The consumer-facing consequence is: Transport cancellation means the caller no longer wants the RPC result. It does not guarantee that the cancellation command did not commit. The server observes context cancellation and avoids unnecessary work, but authoritative state is decided by the transaction. Clients reconcile ambiguous outcomes.

## 9. When should a client treat `UNAVAILABLE` as retryable?

Only when the method and request are safe to replay, the retry budget and deadline permit it, and the failure occurred in a class covered by the service policy.

**Decisive evidence:** retry-classification table

The operational consequence is: Now inject response loss after the cancellation transaction commits. The client receives UNAVAILABLE, not success. Transport status cannot prove that cancellation failed. A retry with the same request identity can replay the stored outcome, or the client can call GetRun and reconcile. An automatic fallback that invokes a local cancellation path with a new identity can duplicate or conflict with the committed effect.

## 10. How should a hidden resource be represented to an authenticated but unauthorized caller?

Return the policy's concealed `NOT_FOUND` without revealing ownership or existence. Audit the denial internally with bounded data.

**Decisive evidence:** concealment vector

The strongest engineering interpretation is: Document interceptor order. A typical server path establishes a request identity, validates edge metadata, authenticates, starts telemetry, invokes the handler and application policy, maps expected errors, sanitizes unexpected errors, and records final status. Cleanup must run when the handler raises or the client cancels.

## 11. Why is a global gRPC-to-HTTP status map insufficient?

HTTP operations distinguish validation, ETag preconditions, conflicts, and concealment differently. The mapping needs operation and detail context.

**Decisive evidence:** HTTP conformance suite

The defect-oriented view is: For example, INVALID ARGUMENT with field violations maps to the documented validation problem. NOT FOUND follows the HTTP concealment policy. A stale ETag conflict maps to the documented 412 or 409 behavior, depending on the original operation contract. UNAVAILABLE may map to 503 with bounded retry guidance. The mapping is operation-specific; a global status-to-HTTP table is insufficient.

## 12. Define the proof that Python and TypeScript expose equivalent unary behavior.

Run shared requests through each adapter and compare status code, stable detail code, authorized metadata, durable effect, and public HTTP translation—not exception class names.

**Decisive evidence:** cross-language unary report

Across the Python and TypeScript tracks, the invariant is: The evidence for this case includes the request and metadata, application error, final status and safe detail, durable run revision/state, idempotency outcome, and public HTTP mapping. A unit test of the status mapper is necessary but not sufficient; the live network test proves trailing metadata and code over gRPC, while a durable integration test proves the transaction.
