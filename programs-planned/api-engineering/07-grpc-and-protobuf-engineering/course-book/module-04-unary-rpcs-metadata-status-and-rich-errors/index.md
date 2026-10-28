# Unary RPCs, Metadata, Status, and Rich Errors

**Module 04 of 10**

> **Governing question:** How should a unary RPC expose success and failure so that generated clients receive stable application meaning rather than transport accidents or leaked internals?

## Place in the program

The first three modules established a justified boundary, precise messages, and compatibility discipline. This module makes the simplest remote interaction honest. Unary RPC is not “call a function over the network.” It has metadata, one request message, one response message, a final status, and potentially structured error details. Those pieces must map cleanly to the application without turning transport conventions into business state.

## Learning outcomes

- implement thin unary server adapters around application use cases
- separate transport metadata from business request fields
- map application outcomes to stable gRPC status codes
- design safe structured error details without leaking internal state
- compose interceptors for authentication, authorization, tracing, and policy without hiding business logic
- translate internal gRPC outcomes back to the existing public HTTP Problem Details contract

## Capstone result

Implement `CreateRun`, `GetRun`, and `CancelRun` with shared status vectors, safe metadata policy, and equivalent Python and TypeScript client behavior.

## The unary call lifecycle

A unary call has one logical request and one logical response, but several observable phases: name resolution and channel readiness; client metadata construction; serialization; server interception; request parsing; application execution; response serialization; trailing metadata and final status. Failure can occur in each phase. A client may receive no application response even when the server committed state.

The server adapter should therefore be thin and explicit. It validates transport-level shape that generation cannot enforce, extracts trusted identity and deadline context, converts the message into an application command, invokes one use case, maps the result, and returns a generated response. It must not contain SQL, retry loops, or domain transitions. The use case remains testable without gRPC.

The client adapter is equally important. Application code should not catch arbitrary `grpc.RpcError` or JavaScript callback errors throughout the codebase. A transport adapter maps status and details into a small course-owned outcome vocabulary. The application decides whether to reconcile, retry, display a safe message, or fail.

## Metadata is not a second request body

gRPC metadata is appropriate for cross-cutting transport context: authorization credentials, trace propagation, request provenance, idempotency headers when the contract profile chooses metadata, and negotiated diagnostic preferences. It is not a place to hide resource identifiers, ownership fields, algorithms, or mutable business options simply because adding metadata avoids changing the proto.

Metadata keys and values need a policy. ASCII keys are normalized lowercase; binary keys use the `-bin` suffix. Bound total size and per-value length. Reject duplicate singleton credentials. Never trust caller-supplied tenant or role metadata without cryptographic identity binding. Do not log raw authorization values.

A field belongs in the request message when it affects the application decision, needs generated documentation and compatibility governance, or must be included in idempotency fingerprinting. The course keeps `request_id` in `CreateRunRequest`, making its semantics visible. The identity token remains metadata because it authenticates who invokes the request rather than defining the requested run.

## Status codes are a finite public vocabulary

gRPC status codes are not HTTP codes with different numbers. Use the smallest stable vocabulary that lets clients choose a correct action. `INVALID_ARGUMENT` means the request is invalid independent of current system state. `FAILED_PRECONDITION` means the system is not in a state that permits the operation. `ABORTED` usually signals a concurrency conflict that may succeed after re-reading. `NOT_FOUND` represents concealed or genuinely absent resources according to policy. `ALREADY_EXISTS` can represent an idempotency identifier bound to incompatible input. `PERMISSION_DENIED` means an authenticated principal lacks authority; `UNAUTHENTICATED` means identity could not be established.

`INTERNAL` is not a bucket for every exception. Unexpected faults are logged with an internal incident identity and returned as a sanitized status. Dependency unavailability may map to `UNAVAILABLE` only when the caller can safely treat the failure as transient. Deadline expiry uses `DEADLINE_EXCEEDED`; cancellation initiated by the caller uses `CANCELLED`. The status policy records retry classification separately because a code alone does not establish operation safety.

## Rich error details require restraint

The standard status model carries code, human-readable message, and optional typed details. Details can identify invalid fields, precondition violations, resource information, retry guidance, or a stable domain error code. They must not expose SQL, stack traces, filesystem paths, secrets, internal hostnames, or cross-tenant resource existence.

Design details for machines first. A field violation identifies the public field path and a stable reason. A precondition detail names the violated public rule. A retry detail describes the earliest sensible retry delay but does not override the caller's deadline or idempotency requirement. Human messages remain concise and non-authoritative.

The dependency-light course profile uses a governed error-detail envelope that can be represented in both tracks without extra packages. The full environment optionally uses `google.rpc.Status` and standard detail messages. The capability matrix states which path was exercised.

## Exception translation belongs at one edge

Framework exceptions, database errors, and domain errors must not cross the RPC boundary directly. Define an application error taxonomy: invalid input, missing resource under policy, version conflict, invalid transition, idempotency conflict, dependency unavailable, and unexpected defect. One mapper owns the conversion to status and details.

Ordering matters. Authentication and edge validation occur before application use. Authorization may need a loaded resource, so some decisions belong in the use case rather than a generic interceptor. Domain errors are mapped after the use case. Unexpected exceptions are captured last, assigned an incident identifier, and sanitized. Mapping the same error in several handlers causes status drift.

Tests enumerate every public application outcome and assert one status mapping. A “default INTERNAL” branch remains for defects but cannot substitute for a complete policy.

## Interceptors are policy plumbing, not hidden domain logic

Interceptors are useful for trace context, metric boundaries, authentication parsing, common metadata limits, deadline observation, and final error sanitation. They should not decide whether a principal owns a particular run unless the required resource context and policy are explicitly passed. Hiding resource authorization in a generic interceptor makes call behavior difficult to review and can create time-of-check/time-of-use gaps.

Document interceptor order. A typical server path establishes a request identity, validates edge metadata, authenticates, starts telemetry, invokes the handler and application policy, maps expected errors, sanitizes unexpected errors, and records final status. Cleanup must run when the handler raises or the client cancels.

Client interceptors can add authentication, tracing, and bounded telemetry. Automatic retries require a separate reviewed service configuration; they must not be smuggled into a generic interceptor that replays every method.

## CreateRun and ambiguous completion

`CreateRun` illustrates why unary success is not the whole story. The server may commit the run and idempotency record, then lose the response. The client receives `UNAVAILABLE` or a deadline failure. It cannot infer whether no run exists. The stable request identifier lets a retry replay the stored outcome, but only if the same semantic input is bound to the identifier.

If the identifier is reused with changed input, return `ALREADY_EXISTS` or the profile's explicit idempotency-conflict status and safe detail. If the caller cannot retry within its deadline, it can reconcile through a query keyed by the request identifier or user-visible resource. Do not return success before the authoritative transaction commits.

The unary conformance test injects failure before invocation, before commit, after commit, and during response delivery. Later modules add deadline and retry policy; this module establishes the outcome vocabulary.

## CancelRun and preconditions

Cancellation is an application command, not transport cancellation. `CancelRunRequest` carries the run name, expected ETag or revision token, and request identifier. A stale precondition maps to `ABORTED` or `FAILED_PRECONDITION` according to the policy's intended client action. A terminal run that cannot be canceled produces a stable precondition violation, not `INTERNAL`.

Transport cancellation means the caller no longer wants the RPC result. It does not guarantee that the cancellation command did not commit. The server observes context cancellation and avoids unnecessary work, but authoritative state is decided by the transaction. Clients reconcile ambiguous outcomes.

Keeping application cancellation distinct from transport cancellation prevents a common naming and correctness failure.

## Mapping back to the public HTTP API

The public OpenAPI surface remains authoritative for external clients. The HTTP adapter may call the internal RPC control plane, then map gRPC outcomes to the existing RFC 9457 Problem Details model. This mapping must preserve meaning without exposing gRPC implementation details.

For example, `INVALID_ARGUMENT` with field violations maps to the documented validation problem. `NOT_FOUND` follows the HTTP concealment policy. A stale ETag conflict maps to the documented `412` or `409` behavior, depending on the original operation contract. `UNAVAILABLE` may map to `503` with bounded retry guidance. The mapping is operation-specific; a global status-to-HTTP table is insufficient.

Conformance tests run the same public HTTP scenarios before and after the internal RPC migration. A transport refactor cannot silently change the public promise.

## Worked failure review: stale cancellation

A client reads a queued run at revision 4 and sends `CancelRun` with ETag `"run-4"`. Another actor advances the run to running revision 5 before cancellation commits. The server must not overwrite revision 5 merely because the request is authenticated and syntactically valid. The application transaction compares the expected version and raises a concurrency conflict.

The status policy chooses `ABORTED` because the client may re-read authoritative state and decide whether a new cancellation attempt is still appropriate. `FAILED_PRECONDITION` would also be plausible in another profile, but the course requires one stable mapping and documents the intended recovery. The trailing detail carries a stable reason such as `concurrency_conflict`; it does not reveal database row versions, SQL, or another principal’s action.

The handler does not catch a database vendor exception and inspect its message. The repository maps the failed compare-and-swap to an application error. The transport mapper owns the gRPC status. The public HTTP adapter then maps that outcome to the exact existing HTTP precondition/conflict behavior. Each layer has one vocabulary and one translation edge.

Consider metadata. The call includes one authorization value and trace context. The run name, ETag, and request identifier remain in `CancelRunRequest` because they define the application command and its idempotency fingerprint. Putting the ETag into metadata would hide a business precondition from schema review and generated clients. Putting a caller-supplied tenant in metadata would be worse: it could become an authorization bypass.

Now inject response loss after the cancellation transaction commits. The client receives `UNAVAILABLE`, not success. Transport status cannot prove that cancellation failed. A retry with the same request identity can replay the stored outcome, or the client can call `GetRun` and reconcile. An automatic fallback that invokes a local cancellation path with a new identity can duplicate or conflict with the committed effect.

The evidence for this case includes the request and metadata, application error, final status and safe detail, durable run revision/state, idempotency outcome, and public HTTP mapping. A unit test of the status mapper is necessary but not sufficient; the live network test proves trailing metadata and code over gRPC, while a durable integration test proves the transaction. The learner should be able to point to each proof and state what it does not establish.

## Implementation reading

Study `capstone/rpc-case/status-policy.yaml`, `capstone/shared/vectors/status.json`, Python `status.py` and `server.py`, and TypeScript `status.ts` and `inprocess.ts`. The network reference proves live unary behavior in Python; both tracks share semantic status vectors.

## Failure checklist

- Is business input hidden in metadata rather than the message?
- Does every expected application outcome have one reviewed status mapping?
- Can error details reveal internal or cross-tenant information?
- Are resource-level authorization decisions hidden in generic interceptors?
- Can a committed command be mistaken for a failed command after response loss?
- Does the HTTP gateway preserve the existing public Problem Details behavior?

## Transition

After preserving the checkpoint evidence, continue to **Deadlines, Cancellation, Retries, and Idempotent Calls**. Do not progress while the non-compensable gate remains unresolved.
