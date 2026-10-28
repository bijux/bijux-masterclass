---
module_id: API-003
program: API & Service Engineering
level: 1
module_number: 3
title: Status Codes and Error Meaning
status: complete
last_verified: 2026-08-31
---

# Status Codes and Error Meaning

## One-Page Review

### Governing question

How should an HTTP response communicate what happened to this request so that a client, intermediary, operator, and human can take the right next action?

### Essential definitions

- A **status code** is a three-digit protocol outcome classification, not an application exception name.
- A **status class** groups outcomes: `1xx` informational, `2xx` successful, `3xx` redirection, `4xx` client-request problems, and `5xx` server-side failure to fulfill an apparently valid request.
- A **response status** reports the result of one request under a specified method, target, authority, and time. It does not by itself prove a downstream business outcome.
- A **problem detail** is a representation that adds machine-readable and human-readable detail; it supplements rather than replaces status semantics.
- A **retry decision** needs both status meaning and request-specific evidence: method semantics, deadline, idempotency, credentials, resource state, and an explicit server hint when present.

### Central model, mechanism, or theorem

Model a response as $R=(s,h,b,e)$: status $s$, fields $h$, optional content $b$, and occurrence evidence $e$. A client action is a function $A(R,Q,C)$ of the response, original request $Q$, and client context $C$, not of $s$ alone. A coherent response satisfies $Meaning(s)land Meaning(h)land Meaning(b)$ for the same occurrence; no field or body may silently contradict the status.

### Critical invariants

Choose the most specific registered status whose normative meaning is true. Keep authorization, validation, conflict, precondition, rate, and availability cases distinct when the distinction changes recovery. Preserve required fields such as `Location`, `Allow`, `WWW-Authenticate`, or `Retry-After` where their status semantics require or make them useful. Do not expose sensitive existence or policy information through more specific errors. A response body explains; it never rewrites the protocol result.

### Common failures

Returning `200` with an error flag; calling every client-visible failure `400`; treating `401` as authorization denial; using `404` where a known resource has a state conflict; using `500` for malformed input; promising exactly-once completion from `202`; returning a framework stack trace; retrying every `5xx`; and treating a reason phrase or localized message as a stable machine contract.

### Compact example

`POST /payments` with syntactically valid JSON can still fail authorization (`403`), validation (`422`), uniqueness or workflow conflict (`409`), a failed required precondition (`412`), or transient capacity (`503`, perhaps with `Retry-After`). All have different remediation. Returning `400` for all five forces clients to guess.

### Connections

Module 002 supplies method safety and idempotency. Module 004 explains response fields, Module 006 preconditions, Module 008 retry semantics, Module 021 contracts, Module 035 error translation, and Modules 041–050 API security. Distributed systems supplies uncertainty after timeouts; security engineering supplies disclosure and authorization rules.

## Governing Question

What does this response allow a recipient to conclude about the request, and what is the safest useful next action?

Status codes are intentionally compact control data. They let generic software distinguish an accepted request from a malformed request, an authentication challenge, a redirect, a conflict, or a server failure without parsing a product-specific body. That interoperability is lost when an API always returns a success code and places the real outcome in JSON.

## Why This Matters

An API response is consumed by more than the application screen: generated clients, browsers, retry middleware, gateways, caches, alerting, audit tools, and operators all use status semantics. A misleading status causes concrete harm: a monitoring system may count business rejections as availability failures, a client may retry a permanent validation error, or a gateway may cache or redirect an exchange under false assumptions.

HTTP Semantics, RFC 9110, defines the classes and registered code meanings independently of wire version. The IANA registry is the current authority for assigned codes. It is not a menu to decorate outcomes after implementation; it is part of the externally observable contract. RFC 9457 defines Problem Details as a standard representation for additional error information, explicitly retaining HTTP status as the protocol signal.

## Prerequisites and Retrieval

Retrieve request/response messages, resource identity, representations, JSON syntax, HTTP methods, authentication versus authorization, and the difference between a client-observed response and an authoritative domain event. Recall from Module 002 that safe and idempotent are method properties, not a promise that a particular attempt has no effect or that its response will arrive.

## Learning Objectives

By the end of this module, you should be able to:

1. classify any HTTP response by its status class without overstating what that class proves;
2. choose among common successful, redirect, client-error, and server-error statuses from request facts;
3. distinguish malformed syntax, failed semantic validation, missing authentication, denied authorization, absent-or-hidden resources, conflicts, and failed preconditions;
4. design a Problem Details representation that agrees with its HTTP status;
5. specify client recovery without using status code alone as a retry rule;
6. identify required or recovery-relevant response fields; and
7. review error responses for security disclosure, observability, and contract stability.

## Core Exposition

### Status is control data, not a verdict on reality

The status line reports how the origin or intermediary handled the received request. A `201 Created` says the request resulted in one or more new resources and should normally identify the primary one with `Location`; it does not prove a package arrived or a payment settled outside the service. A `202 Accepted` says processing has been accepted but is not complete. A `204 No Content` says there is no response content, not that no state changed. State the authority and completion boundary in the contract.

The five classes guide generic behavior. Informational responses occur before the final response. A `2xx` response means the request was successfully received, understood, and accepted according to the selected code's semantics. A `3xx` response asks for further action, commonly another request to a location. A `4xx` response says the request cannot currently be fulfilled as received; it is not moral blame and may be resolvable after credentials, representation, target, or state changes. A `5xx` response says the server failed to fulfill an apparently valid request. Neither class tells a client whether blindly repeating an unsafe operation is safe.

### Choose from facts, not from route conventions

First identify the method, target resource, representation, authenticated principal, authorization result, validation result, state predicate, and server condition. Then select the narrowest status whose definition holds. `400 Bad Request` is appropriate when the request cannot be processed because it is malformed or invalid at the HTTP request level. `415 Unsupported Media Type` isolates an unacceptable request content type; `406 Not Acceptable` concerns available response representations under negotiation. `422 Unprocessable Content` is useful when syntax and media type are understood but the content's instructions cannot be processed semantically.

Authentication and authorization require care. `401 Unauthorized` historically has a misleading reason phrase: it means authentication is required or supplied credentials are unacceptable, and a response includes a `WWW-Authenticate` challenge. `403 Forbidden` means the server understood the request but refuses to fulfill it. A service may deliberately use `404 Not Found` for an unauthorized target when revealing its existence would be harmful. That is a security policy, not evidence that the resource literally does not exist.

Conflicts and preconditions are different. `409 Conflict` describes a conflict with the target resource's current state that a user may resolve, such as a duplicate human-facing name or invalid workflow transition. `412 Precondition Failed` says one or more request preconditions evaluated false, commonly a validator supplied through `If-Match`. `428 Precondition Required` says the origin requires a conditional request to prevent a lost update. These distinctions give a client different recovery paths: refresh and merge for a failed validator, supply a validator for a missing one, or alter a domain decision for a conflict.

### Success, redirects, and asynchronous completion

Use `200 OK` only when its general successful semantics fit and a response representation is supplied. Use `201 Created` when creation occurred; include `Location` whenever feasible. Use `202 Accepted` for queued or otherwise unfinished processing, and return an operation resource or another documented mechanism to inspect progress. Use `204 No Content` only when the response intentionally has no content; a client must not parse a body from it. Do not use a `2xx` code merely because the server produced a JSON envelope.

Redirection is not a generic success wrapper. `301`, `302`, `307`, and `308` have different permanence and method-rewrite implications. A public API must specify whether a client may follow a redirect automatically, whether credentials may be forwarded, and whether the original method and content must be preserved. A `303 See Other` deliberately directs the client to retrieve a different resource after a request; it can be useful after a command when the result resource has separate retrieval semantics.

### Error representations and stable problem types

Problem Details uses the media type `application/problem+json` (or its XML counterpart). A problem object can include a type URI, title, status, detail, instance, and extension members. The `status` member is advisory for the body; the actual response status is authoritative protocol control data. Keep `type` stable enough to identify a problem category, but do not make localized prose, framework exception names, database constraint names, or stack traces a client dependency.

For a field-level validation response, state which input locations and rules failed without leaking hidden policy or values. Give an occurrence identifier through `instance` or a documented correlation field so a user can report a failure and operators can find evidence. The identifier is not permission to retrieve another tenant's log record. Errors must be no more revealing than the authorization model allows.

### Retry, observability, and uncertainty

A retry rule needs a request identity and a deadline. `503 Service Unavailable` can include `Retry-After`, but that does not make an unsafe POST replay-safe. `429 Too Many Requests` indicates rate limiting and may also include `Retry-After`; clients should back off rather than synchronize into a new burst. A timeout or a dropped response is not an HTTP status at all. For a non-idempotent operation, the server may already have applied the request. Prefer an idempotency key, operation resource, or status lookup before retrying.

Record status, problem type, method, route template, dependency classification, and latency, while protecting targets, credentials, and sensitive request content. Metrics should separate expected `4xx` categories from unexpected `5xx` and should not equate a high `4xx` rate with healthy behavior or a low one with correct authorization. Sample representative error bodies and validate that their status, fields, and machine codes agree.

<!-- bijux-verify: {"id":"classify-outcomes","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"422 client-repair\n409 state-resolution\n412 refresh-validator\n429 backoff\n503 retry-if-contract-allows\n","stderr":""}} -->
```python
actions = {
    422: "client-repair",
    409: "state-resolution",
    412: "refresh-validator",
    429: "backoff",
    503: "retry-if-contract-allows",
}

for status in (422, 409, 412, 429, 503):
    print(f"{status} {actions[status]}")
```

This executable table checks only the chapter's illustrative recovery mapping. It does not prove that a real request is idempotent, authorized, complete, or safe to retry.

## Definitions and Notation

Let $Q=(m,u,h_q,b_q)$ be a request with method $m$, target $u$, fields $h_q$, and optional content $b_q$. Let $R=(s,h_r,b_r,e)$ be the resulting response occurrence. Let $P(Q)$ be the set of predicates observed while processing: syntax, media type, authentication, authorization, semantic validity, preconditions, resource state, and service availability.

The selection function $Select(P)$ must choose a registered status $s$ whose normative conditions hold and whose specificity does not falsely reveal protected facts. **Outcome semantics** is the documented relation between $Q$, $P$, and $R$. **Recovery semantics** is the set of safe client actions after that outcome. A **stable machine code** is a documented domain token or Problem Details type, not a replacement status code. **Occurrence evidence** ties a response to logs or an operation record without claiming that the evidence is universally complete.

## Mechanisms, Invariants, or Proof Structure

Apply this decision procedure:

1. Parse the request framing, target, fields, and declared media type.
2. Authenticate before exposing sensitive target details; apply the documented concealment policy.
3. Authorize the principal for the target and requested action.
4. Validate representation syntax, media type, and domain semantics separately.
5. Evaluate explicit HTTP preconditions before performing protected mutation.
6. Evaluate domain state and concurrency rules; distinguish conflict from failed precondition.
7. Determine whether the requested effect completed, was accepted for later work, redirected, or could not be fulfilled because of service failure.
8. Attach only response fields and representation detail consistent with that result.
9. Define client recovery, observability, and rate behavior from the full response and request contract.

The **coherence invariant** is that status, fields, body, logs, and metrics describe one outcome category. The **least-disclosure invariant** is that increased status specificity must not expose an otherwise protected fact. The **recovery invariant** forbids automatic replay unless the method, operation identity, deadline, and known application state permit it. Test all branches at the boundary, including a response lost after the effect committed.

## Alternatives and Trade-Offs

**One generic error envelope versus Problem Details.** A private envelope may be reasonable inside a bounded product, but it duplicates status classification and often becomes inconsistent. Problem Details gives a standardized base while leaving domain extensions possible. In either style, status remains primary protocol control data.

**`400` versus `422`.** A single `400` reduces a public taxonomy but obscures whether a client should repair framing or a meaningful, well-formed instruction. Use `422` only with a documented semantic boundary; do not create elaborate distinctions clients cannot act on.

**`403` versus concealment with `404`.** `403` helps an authenticated user understand a permission problem. Concealed `404` reduces enumeration and discovery. Choose per resource class and threat model, then make observations, support workflows, and documentation consistent with that choice.

**Synchronous success versus `202`.** A synchronous terminal response gives simple client reasoning. `202` contains queueing and long work but introduces operation tracking, expiry, cancellation, duplicate handling, and an explicit definition of accepted versus completed.

## Failure Modes and Misconceptions

Returning a success status with `{ "ok": false }` breaks generic HTTP consumers. Returning raw exceptions couples clients to implementation. Mapping every domain rejection to `500` misclassifies ordinary client recovery as an outage. Returning `401` after a valid identity but insufficient permission confuses challenge handling. Treating `404` as proof of nonexistence can violate a concealment policy. A `409` without a conflict explanation strands users. A `202` without a status resource makes completion unknowable. A retry recommendation without an idempotency boundary can duplicate a charge or command.

## Worked Examples

### Example 1

A client sends malformed JSON to `POST /orders`; parsing cannot produce the documented representation. Return `400 Bad Request` with a problem type for malformed JSON and a safe location description. The conclusion is that the client must repair framing before any domain validation exists.

### Example 2

The JSON is valid but `quantity` is `-3`, violating the order contract. Return `422 Unprocessable Content` and identify `quantity` and its lower-bound rule. This is not `400` merely because it is an error: the server understood both format and intended instruction, then rejected its semantics.

### Example 3

An unauthenticated request reaches `GET /invoices/inv-9`. The service requires a bearer credential and returns `401` with the appropriate `WWW-Authenticate` challenge. The conclusion is authentication recovery, not evidence that the invoice exists or that the caller would be authorized after authentication.

### Example 4

An authenticated employee requests another tenant's invoice. The threat model says resource existence is confidential. Return the same documented `404` used for absent invoices, log the authorization decision internally, and avoid a body distinction. The conclusion is deliberate concealment, not an assertion that the invoice is absent.

### Example 5

Two users choose the same unique, human-facing project slug. The second valid create cannot satisfy the current namespace rule. Return `409 Conflict` with a stable problem type and, if disclosure permits, suggested alternatives. The client can choose another slug; a retry without change will reproduce the conflict.

### Example 6

A client sends `PUT /profile/me` with `If-Match: "v7"`, but the current validator is `"v8"`. Return `412 Precondition Failed`; the client fetches the current representation, merges deliberately, and submits a new conditional update. Calling this `409` would hide the failed HTTP condition and make automated merge logic less precise.

### Example 7

`POST /exports` queues a ten-minute report. The service creates operation `op-44`, returns `202 Accepted`, and documents `GET /operations/op-44` for status. The conclusion is only that the work was accepted; `201` would falsely imply the finished export resource already exists.

### Example 8

A gateway rejects a request because the account exceeded its quota. Return `429 Too Many Requests` and, when the policy can state it honestly, `Retry-After: 60`. A client adds jitter and respects its own deadline. The conclusion is controlled backoff, not permission to replay an expired or non-idempotent command forever.

### Example 9

The origin cannot reach a required dependency and cannot fulfill an otherwise valid retrieval. Return `503 Service Unavailable`; include `Retry-After` only if the estimate is credible. A GET may be retried within budget, while a POST requires its idempotency and operation-status contract. The same status leads to different actions because requests differ.

### Example 10

An endpoint returns `200 OK` with `{"status": 422, "error": "invalid quantity"}`. A generic client records success, skips error handling, and a cache or monitor sees a false success. Correct the response to `422` and use a Problem Details body. The conclusion is that body fields cannot repair a contradictory status.

## Cross-Program Connections

[HTTP method semantics](002-http-methods-and-their-semantics.md) determines whether retry is meaningful. The later Conditional Requests module develops `412` and `428`. Security engineering owns authorization policy and data disclosure; API engineering owns how that policy is communicated at this boundary. Distributed systems explains ambiguous completion after lost responses. Software testing owns boundary matrices and fault injection; later API modules apply those methods to contract tests and production telemetry.

## References

- Fielding, R., Nottingham, M., and Reschke, J. *HTTP Semantics*, RFC 9110, IETF Standards Track, June 2022, Sections 15–16. Retrieved 2026-08-31. https://www.rfc-editor.org/rfc/rfc9110.html
- Nottingham, M., Wilde, E., and Dalal, S. *Problem Details for HTTP APIs*, RFC 9457, IETF Standards Track, July 2023. Retrieved 2026-08-31. https://www.rfc-editor.org/rfc/rfc9457.html
- Internet Assigned Numbers Authority. *Hypertext Transfer Protocol (HTTP) Status Code Registry*. Retrieved 2026-08-31. https://www.iana.org/assignments/http-status-codes/http-status-codes.xhtml

## Exercises

### Exercise 1

State the difference between `401`, `403`, and a concealment-oriented `404`, including one required or useful response-field consequence.

### Exercise 2

For a conditional update with an obsolete `If-Match` validator, derive why `412` communicates more than a generic conflict and state the client recovery sequence.

### Exercise 3

Design a Problem Details response for a valid JSON request whose `startDate` is after `endDate`. Specify status, media type, stable type, safe detail, and one extension member.

### Exercise 4

An API returns `202` for a payment submission. Compare two designs: a response that only says "accepted" and one that returns an operation resource. Identify the evidence each design provides and the risks it leaves.

### Exercise 5

Review this policy: “Retry every `5xx` response three times.” Replace it with a bounded rule that accounts for method semantics, idempotency evidence, deadlines, and server hints.

## Answers to the Exercises

### Answer 1

`401` means authentication is required or unacceptable and uses `WWW-Authenticate` to state a challenge. `403` means the service understood the request but refuses it, commonly after identifying the caller. A concealment-oriented `404` intentionally gives the same externally visible outcome for absent and inaccessible targets; it must be a documented security policy and must not leak the difference through body shape, timing where controllable, or support tooling.

### Answer 2

`If-Match` makes success conditional on a specific selected representation state. When that predicate is false, `412` names the failed HTTP precondition rather than merely saying that the target is in conflict. The client should retrieve the current representation and validator, reconcile its intended change with the current state under domain rules, then submit a new conditional request. It should not overwrite the newer state blindly.

### Answer 3

Return `422 Unprocessable Content` with `Content-Type: application/problem+json`, a stable type such as `https://api.example.test/problems/invalid-date-range`, and a safe detail such as “startDate must not be after endDate.” An extension member may be `invalidParams` containing the two field names and rule identifiers. Do not return raw parser internals, unrelated object data, or a status member that disagrees with the HTTP status.

### Answer 4

The bare `202` proves only acceptance at the documented boundary; the client cannot distinguish queued, running, failed, completed, or expired work without another mechanism. An operation resource supplies a stable target for observed state, progress, terminal result, cancellation policy, and correlation. It still does not prove an external payment settled unless the operation state explicitly represents and is authoritative for that claim. The operation design adds retention, authorization, polling, and duplicate-submission responsibilities.

### Answer 5

Retry only when the remaining deadline permits it, the request is safe or has documented idempotency/operation identity, the failure is classified as transient, and no response or operation lookup already proves a terminal effect. Honor a credible `Retry-After`, use bounded exponential backoff with jitter, preserve relevant conditions and credentials, and stop on permanent client errors. For an uncertain non-idempotent POST, query the idempotency or operation record before replaying; a `5xx` class alone is insufficient evidence.
