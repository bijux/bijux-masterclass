# Module 55 Solutions — Routing, Validation, Errors, and Idempotency

## Prediction reasoning

Semantic fingerprints should be equal when validated commands are equal even if JSON representation differs. An in-progress idempotency record must exist before another request can interleave at an `await`. A matching validator returns 304 with no representation body. In-progress records should not be evicted to make room because a retry could then create another effect. A job created before response loss is committed; only client knowledge is incomplete.

## Repair reasoning

Typed routing separates path grammar from domain lookup. Parse the URL once, match exact segments, validate percent-decoded identifiers, and return an exhaustive route union.

Runtime validation should reject arrays, null, extra fields, unsupported operations, oversized payloads, and invalid operation-specific values. Only the validated result becomes `SubmitCommand`.

Request IDs trace attempts. Idempotency keys bind attempts to one semantic submission. Store both when useful, but never substitute one for the other.

Fingerprint the validated operation and payload in canonical order. For richer commands, use a deterministic canonical encoding rather than raw `JSON.stringify()` on arbitrary objects.

A full idempotency store can evict expired terminal records. If no eligible record exists, reject before creating a job.

Events belong to the state authority. If an HTTP adapter emits “job accepted” after sending a response, a dropped response can suppress an event for a committed job. Publish during the commit transition.

ETags are quoted opaque validators. Parse supported lists and wildcard behavior deliberately; the laboratory may implement a documented strict subset.

## Construction notes

Use private collections and return immutable views. A job view should not expose mutable internal state. Increment revision in the same transition that changes job state.

A stable problem type:

```ts
interface Problem {
  readonly type: string;
  readonly title: string;
  readonly status: number;
  readonly code: string;
  readonly detail: string;
  readonly requestId: string;
}
```

Bound every string produced from peer input. Internal error causes remain separate.

Two interleaved same-key tests should force a scheduling point after admission. The second call must observe the record, not create a second job. In a purely synchronous in-memory commit, the race is avoided by design; the test explains why future persistence cannot insert an unguarded await.

## Laboratory evidence

Strong router tests include:

- static versus parameter route precedence;
- percent-encoded invalid path;
- unsupported method with `Allow`;
- exact body shape;
- same-key replay;
- same-key conflict;
- store capacity;
- matching and stale ETags;
- HEAD metadata parity;
- no event on pre-commit rejection;
- event on committed submission even when rendering later fails.

## ServiceWire transfer

The HTTP adapter converts `SubmitResult` into 202 and a representation. Both HTTP/1.1 and HTTP/2 call the same application object. The domain object owns job IDs, revisions, idempotency records, and event append.

## Independent transfer

An order fingerprint includes customer/account identity under the authenticated context, line items, currency, addresses, and semantic options. It excludes whitespace and request ID. Commit occurs when the authoritative order record and idempotency record are established atomically. Durable exactly-once behavior across process restart requires persistent transactional storage or a serialized durable command log, reserved for Course 7.

## Defense summary

The application boundary turns a request attempt into a semantic command. Idempotency preserves operation identity across uncertain responses. Revisions preserve representation identity across state changes. Keeping these authorities separate is what makes retries and conditional reads correct.

## Ambiguous submission solution

The semantic commit occurs when the application authority inserts the idempotency binding and queued job under one synchronous transition. The 202 representation is constructed afterward; client observation occurs only when bytes reach the client. A lost response therefore does not imply non-commit.

A retry with the same key and canonical command fingerprint returns the existing job. A changed payload produces conflict because the key is already bound to different semantics. The bounded idempotency record is the reconciliation witness.

For a new `priority` field, include it in the fingerprint if it changes execution semantics. Excluding it would let the same key silently replay a job with a different requested priority. During rolling upgrade, old clients omit the field and receive the documented default; canonicalization must make that default explicit so old and new representations agree. Changing the default later is a compatibility change because it changes fingerprint semantics and job behavior.

## Problem-contract solution

Each problem uses a stable machine code and status; human detail is bounded and never carries stack traces, file paths, keys, or raw payloads. Malformed JSON is a permanent client representation error. Idempotency conflict is a semantic conflict requiring a different key or identical command. Overload is potentially retryable only when the server contract supplies policy such as a retry hint and the operation remains within its overall deadline. Clients branch on code and status, not prose.
