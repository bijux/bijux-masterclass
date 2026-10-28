# Worked answers — Unary RPCs, Metadata, Status, and Rich Errors

These are reference answers, not scripts to memorize. Compare the decision rule and evidence, then revise your answer.

## 1. Which fields belong in metadata for `CreateRun`, and which belong in the request message?

Authorization, trace, and bounded transport context belong in metadata. Parent, dataset, algorithm, expected revision, and request identity affect the application decision and belong in the message.

**Decisive evidence:** metadata policy review

## 2. Map an invalid algorithm, a missing run, and a stale revision to gRPC statuses.

Invalid algorithm is `INVALID_ARGUMENT`; a policy-concealed or absent run is `NOT_FOUND`; a stale optimistic concurrency token is `ABORTED` or the declared precondition status. The profile must choose consistently.

**Decisive evidence:** status vector

## 3. Why is `UNKNOWN` or `INTERNAL` an inadequate default for expected domain conflicts?

Expected conflicts are part of the public contract and require actionable, stable codes. Treating them as internal defects prevents correct client behavior and corrupts reliability metrics.

**Decisive evidence:** status coverage table

## 4. What makes an error detail safe for a client?

It uses public identifiers and stable reason codes, contains only information the caller is authorized to know, is bounded, and avoids stack, SQL, host, path, and secret data.

**Decisive evidence:** error-detail redaction test

## 5. Where should a database unique-constraint error be translated?

At the application/transport translation edge after the repository maps the database condition to a domain/application error. Handlers should not parse vendor error strings.

**Decisive evidence:** repository/application error mapping test

## 6. Why should a generic interceptor not decide run ownership by itself?

Ownership may require authoritative resource state and operation context. A generic interceptor lacks that context and can separate the check from the mutation.

**Decisive evidence:** authorization placement review

## 7. Describe the ambiguous outcome when `CreateRun` commits but the response is lost.

The client sees failure but the run exists. It must reuse the same bound request identifier or reconcile; generating a new identifier can duplicate the effect.

**Decisive evidence:** post-commit response-loss trace

## 8. Differentiate application `CancelRun` from transport cancellation.

`CancelRun` changes durable application state. Transport cancellation only signals that the caller has stopped waiting; it does not roll back committed work.

**Decisive evidence:** cancellation sequence

## 9. When should a client treat `UNAVAILABLE` as retryable?

Only when the method and request are safe to replay, the retry budget and deadline permit it, and the failure occurred in a class covered by the service policy.

**Decisive evidence:** retry-classification table

## 10. How should a hidden resource be represented to an authenticated but unauthorized caller?

Return the policy's concealed `NOT_FOUND` without revealing ownership or existence. Audit the denial internally with bounded data.

**Decisive evidence:** concealment vector

## 11. Why is a global gRPC-to-HTTP status map insufficient?

HTTP operations distinguish validation, ETag preconditions, conflicts, and concealment differently. The mapping needs operation and detail context.

**Decisive evidence:** HTTP conformance suite

## 12. Define the proof that Python and TypeScript expose equivalent unary behavior.

Run shared requests through each adapter and compare status code, stable detail code, authorized metadata, durable effect, and public HTTP translation—not exception class names.

**Decisive evidence:** cross-language unary report
