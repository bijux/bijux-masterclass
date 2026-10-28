# Module 56 — HTTP Clients: Agents, Pooling, Deadlines, Redirects, and Retry

**Progress: 56/100**

## The governing question

> How do you make one HTTP client operation own its pooled socket opportunity, request bytes, response body, redirects, retries, cancellation, and one total time promise without duplicating a committed effect?

## Why this module comes now

The server now has strict finite routes and a process-local idempotency protocol. A robust service still needs a supported client. Client code is often compressed into one `fetch()` or `request()` call, but production behavior includes connection pooling, queueing inside an agent, DNS and connection delay, response-body limits, redirects, retries, and cleanup.

The client is where ambiguous commit becomes unavoidable. A timeout only describes what the client observed. It does not prove that the server did nothing. This module uses the server's idempotency contract to make that ambiguity manageable.

## Observable outcomes

By the end of the module, you can:

- own an `http.Agent` or `https.Agent` and close it deliberately;
- distinguish agent queueing, socket connection, request write, response headers, body consumption, and application validation;
- apply one absolute deadline across every phase and retry;
- bound response bytes before retention;
- define body discard or destruction when a response is not consumed;
- implement redirect policy with origin, method, credentials, loops, and remaining budget;
- classify transport, protocol, status, representation, and validation failures;
- retry only when method semantics and application idempotency permit it;
- preserve the same idempotency key across attempts;
- expose attempt history without leaking secrets.

## The client-operation ledger

| Resource or fact | Owner |
|---|---|
| shared agent | client instance |
| agent socket slot | one request attempt |
| request object | attempt scope |
| request body | caller/client boundary |
| response stream | attempt scope |
| accumulated response bytes | bounded body reader |
| deadline timer | semantic operation |
| redirect history | semantic operation |
| retry policy | semantic operation |
| idempotency key | semantic operation |
| abort listeners | operation/attempt cleanup |
| terminal result | semantic operation |

The semantic operation can own several attempts. Each attempt owns exactly one request and at most one response.

## Agents are resource managers

Node's HTTP agents manage connection reuse and socket pools. An agent can retain idle sockets and queue requests when capacity is full. A caller-visible request can therefore wait before a new network connection begins.

Configure and document:

- keep-alive policy;
- maximum total sockets;
- maximum sockets per origin;
- maximum free sockets;
- scheduling policy if relevant;
- idle-socket behavior;
- client shutdown.

Using the global agent delegates these choices. A reusable library or service client often benefits from a private agent so ownership and tests are explicit.

Agent limits are not application admission limits. They bound connection resources, not semantic operations retained elsewhere.

## One operation, several attempts

Define:

```ts
interface AttemptRecord {
  readonly number: number;
  readonly startedAtMs: number;
  readonly target: string;
  readonly outcome:
    | 'response'
    | 'transport-error'
    | 'deadline'
    | 'cancelled';
  readonly status?: number;
  readonly code?: string;
}
```

Attempt records support diagnostics. They must not contain authorization values, full response bodies, or unbounded error text.

The operation decides when another attempt is legal. It owns:

- stable request semantics;
- stable idempotency key;
- one deadline;
- maximum attempts;
- backoff schedule;
- redirect history;
- final result.

## The phase model

A client attempt passes through:

```text
agent queue
    ↓
socket assignment / connection
    ↓
request headers and body write
    ↓
response headers
    ↓
bounded response body
    ↓
representation validation
    ↓
application result
```

Failure before request bytes leave the process is different from failure after a response begins, but Node APIs do not always expose a perfect commit boundary. The safest retry decision combines:

- method semantics;
- idempotency key;
- server contract;
- observed phase;
- remaining deadline;
- policy.

## Absolute deadlines

Use one deadline across:

- agent waiting;
- connection;
- TLS;
- request transmission;
- response headers;
- body;
- redirects;
- retry delays.

Each attempt receives `remainingMs()`. A client should refuse to begin a new retry when no meaningful budget remains.

A timeout wrapper around only the response promise misses agent and connection time. A fresh timeout inside each redirect or retry multiplies the product promise.

Cancellation and deadline are related but distinct. The caller may cancel early. The deadline is time policy. Both converge on cleanup: destroy the request, stop body retention, remove listeners, and settle once.

## Request bodies and replayability

A retry requires another copy of the request body. A `Buffer` or immutable string is replayable. A one-shot stream may not be.

Classify request bodies:

- **replayable**: bytes can be produced again identically;
- **non-replayable**: stream or side-effectful generator can be consumed once;
- **conditionally replayable**: can be regenerated from a stable source under a bound.

Do not retry a consumed non-replayable body merely because the method or idempotency key permits retry.

ServiceWire's JSON submissions use a bounded `Buffer`, so attempts can replay exact bytes.

## Response bodies are hostile inputs

A server or intermediary can return an unexpectedly large body, including for error statuses. Enforce `maxResponseBytes` while reading. The `Content-Length` header can support early rejection but does not replace observed counting.

When the client does not need a body, it still needs a policy:

- consume and discard within a bound so the socket may be reused;
- destroy the response/request, sacrificing reuse;
- stream to a bounded consumer.

Leaving a response unread can tie up a socket and prevent pool reuse.

## Status is not enough

A successful transport can return:

- redirect;
- overload;
- malformed JSON;
- unsupported media type;
- application problem;
- stale representation;
- success status with invalid schema.

The client boundary should classify:

```ts
type ClientFailure =
  | { readonly kind: 'transport'; readonly code?: string }
  | { readonly kind: 'deadline' }
  | { readonly kind: 'cancelled' }
  | { readonly kind: 'response-too-large'; readonly limit: number }
  | { readonly kind: 'redirect'; readonly code: string }
  | { readonly kind: 'http'; readonly status: number; readonly problem?: Problem }
  | { readonly kind: 'representation'; readonly code: string }
  | { readonly kind: 'validation'; readonly issues: readonly Issue[] };
```

Do not convert every non-2xx response into an unstructured thrown string.

## Redirect policy

Redirects create a new request target. Define:

- accepted status codes;
- maximum redirect count;
- loop detection;
- same-origin versus cross-origin;
- downgrade from HTTPS to HTTP;
- authorization/cookie forwarding;
- method and body behavior;
- response-body disposal;
- remaining deadline;
- idempotency key behavior.

For a service client, a conservative policy is often “no redirects” unless the service contract requires them. The laboratory implements a controlled subset to force the decisions.

## Retry policy

Retry is safe when the semantic operation is safe to repeat under the server contract. Inputs include:

- safe/idempotent HTTP method;
- application idempotency key;
- replayable body;
- transport failure phase;
- response status such as bounded overload;
- server retry hint;
- attempts remaining;
- deadline remaining.

Never retry indefinitely. Bound attempts and delay. Add jitter in real fleets to avoid synchronized retries; inject it in tests.

ServiceWire permits retrying job submission with the same key and exact semantic request. It does not permit changing the key after an ambiguous attempt.

## Ambiguous commit

Timeline:

```text
client sends complete POST
server creates job
server begins 202 response
connection resets
client sees transport error
```

The client cannot infer rollback. A retry with the same idempotency key reconciles. A retry with a new key can create another job.

This is why the client and server protocols must be designed together. Retry logic cannot be correct from transport errors alone.

## Connection reuse and stale sockets

A pooled idle socket can close before reuse. The client may observe errors when attempting a new request. Agent and request logic should classify and, where semantic policy permits, retry under the same operation.

Avoid building logic that assumes one semantic operation maps to one TCP connection. Keep-alive intentionally breaks that identity.

## Worked case — bounded GET with ETag

The client has cached job representation and ETag. It sends:

```http
GET /v1/jobs/job-000001
If-None-Match: "job-job-000001-rev-3"
```

Possible responses:

- 304: return cached validated representation;
- 200 with new ETag and valid body: replace cache;
- 404 problem: job absent under server retention policy;
- 503: apply retry policy only if deadline and attempt budget permit;
- invalid JSON or oversized body: fail representation contract, not retry blindly.

The cached object is trusted only if it was validated when stored and its ETag corresponds to the request target and authorization context.

## Client shutdown

A client instance owns its agents. `close()` should:

- reject new operations;
- cancel or allow active operations according to policy;
- wait for tracked operations if promised;
- destroy idle and active agent sockets as needed;
- settle once;
- become safe to close repeatedly.

A library that creates private agents but never exposes closure leaks handles in tests and long-lived processes.

## Common wrong models

### “Timeout means the server did nothing”

It means the client did not complete within its observation budget.

### “Retry is a network concern”

It is an application semantic decision supported by transport evidence.

### “The agent is just an optimization”

It owns sockets and queues and affects capacity, latency, and shutdown.

### “A 2xx response is valid”

The body still needs bounded consumption and runtime validation.

### “Redirect keeps the same request”

Origin, method, credentials, and identity may change.

## Decision procedure

For each client operation:

1. define semantic request and stable identity;
2. classify body replayability;
3. choose agent and pool policy;
4. create one deadline;
5. define response-byte limit;
6. define accepted statuses and media types;
7. validate body;
8. define redirect policy;
9. define retry policy;
10. record bounded attempts;
11. close every response/request path;
12. expose client shutdown.

## ServiceWire increment

Implement a supported client that can:

- submit with a caller-supplied idempotency key;
- get jobs with optional ETag;
- get stats;
- enforce one deadline;
- bound response bytes;
- parse stable problems;
- retry supported failures;
- close its agent.

## Deep reasoning — the client owns a distributed uncertainty budget

A supported HTTP client is a subsystem with its own resources and policies. It owns agents, sockets, response buffers, retry timers, redirect decisions, abort listeners, and terminal evidence. A convenience function that creates a fresh agent and timeout for every request hides these obligations rather than removing them.

### One deadline across attempts

Suppose the caller grants 800 ms:

```text
attempt 1 connect + response: 260 ms, transport reset
backoff: 40 ms
attempt 2: 300 ms, receives 503
backoff: 80 ms
attempt 3 has at most 120 ms remaining
```

The third attempt must use the remainder. A common bug gives each attempt 800 ms and adds backoff on top, turning a bounded operation into several seconds.

The client should record attempt evidence separately from the final error:

```ts
interface AttemptRecord {
  readonly number: number;
  readonly endpoint: string;
  readonly outcome: 'response' | 'transport-error' | 'deadline';
  readonly status?: number;
  readonly code?: string;
  readonly elapsedMs: number;
}
```

This list must itself be bounded by the maximum attempt count. It supports diagnostics without retaining bodies or secrets.

### Retry eligibility is semantic

A retry decision needs at least four inputs:

- method and operation semantics;
- whether the request body can be reproduced;
- whether an idempotency mechanism exists;
- remaining operation budget.

`GET /v1/jobs/:id` is naturally retryable under ordinary conditions. `POST /v1/jobs` is retryable only because the caller supplies a stable idempotency key and the body is retained as bounded bytes. A streaming upload that cannot be replayed has a different contract.

### Redirects are new authority decisions

A redirect can change origin, transport security, credentials, method, or body handling. Do not automatically follow it merely because Node exposed `Location`. The policy should define:

- allowed status codes;
- maximum redirects;
- same-origin or cross-origin behavior;
- whether HTTPS may downgrade to HTTP;
- which headers survive;
- whether method and body are preserved;
- how the same overall deadline applies.

ServiceWire’s teaching client does not need broad redirect support. The laboratory includes a narrow same-origin policy so the risks become explicit.

### Response bounds are enforced during receipt

Checking body size after `Buffer.concat()` is too late. The client should count chunks as they arrive and destroy the response once the bound is exceeded. The terminal error must remain `RESPONSE_TOO_LARGE`, not be overwritten by the transport error caused by destruction.

### Agent lifecycle

Keep-alive agents retain sockets after individual requests finish. This is desirable when reuse is part of the client design, but it means request completion does not imply resource completion. The client needs an idempotent `close()` that destroys both HTTP and HTTPS agents. Tests should verify that operations after close fail deterministically.

### Reconciliation after ambiguous submit

When a submit attempt resets after the server might have committed, retry with the same key. If the retry also fails and the operation deadline expires, the caller still has the key. A more advanced client can expose a reconciliation operation or let the caller query by key. Do not report “submission failed” as though non-commit were proven.

The mature client error model says what was observed: deadline exhausted, transport failed, HTTP problem received, response exceeded limit, protocol representation malformed, or client closed. It does not invent certainty the network cannot provide.

## Ready to continue

You are ready for TLS when you can explain why a client can know transport failed without knowing whether the semantic operation committed.

## Primary Node.js references

- [HTTP](https://nodejs.org/docs/latest-v24.x/api/http.html)
- [HTTPS](https://nodejs.org/docs/latest-v24.x/api/https.html)
- [AbortController](https://nodejs.org/docs/latest-v24.x/api/globals.html#class-abortcontroller)

## Continue

- [Workbook](workbook.md)
- [Reasoned solutions](solutions.md)
- [Laboratory brief](../../labs/module-56-deadline-aware-http-client/README.md)
- [ServiceWire engineering guide](../capstone.md)
