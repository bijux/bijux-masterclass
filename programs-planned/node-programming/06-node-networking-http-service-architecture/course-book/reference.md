# Networking and Service Reference Desk

This reference compresses recurring distinctions. It is not a substitute for the module chapters.

## Layer map

| Layer | Owns | Does not automatically own |
|---|---|---|
| DNS resolution | name-to-address candidates | connection success, service identity |
| TCP | ordered reliable byte stream while connected | message boundaries, application commit |
| UDP | independent datagrams | delivery, order, uniqueness, peer authenticity |
| TLS | encrypted authenticated channel under configured trust and identity policy | application authorization |
| HTTP | request/response message semantics | domain validation, idempotency records, retry safety |
| SSE | ordered text events on one HTTP response | durable history, exactly-once delivery |
| HTTP/2 | multiplexed streams in one session | unlimited capacity, application fairness |
| ServiceWire domain | job identity, state, revision, idempotency, event publication | durable storage or distributed consensus |

## Address vocabulary

- **service URL**: logical application endpoint such as `https://example.test:8443`;
- **hostname**: name supplied to resolution and usually TLS identity verification;
- **address candidate**: one resolved address and family;
- **local address**: the address and port of this socket endpoint;
- **remote address**: the peer endpoint observed by this socket;
- **advertised address**: value the product tells clients to use; it may differ from the bound wildcard address;
- **SNI server name**: TLS name sent during handshake so a server can select credentials;
- **ALPN protocol**: application protocol selected during TLS negotiation.

Never replace a logical hostname with a resolved IP before TLS verification unless the product intentionally changes its identity policy.

## Time vocabulary

| Time concept | Meaning |
|---|---|
| connect timeout | maximum time to establish transport |
| header timeout | maximum time to receive or parse HTTP headers |
| body deadline | remaining budget for body transfer and validation |
| idle timeout | maximum period without qualifying activity |
| operation deadline | absolute latest time for the whole operation |
| retry delay | bounded wait before another allowed attempt |
| shutdown grace | one budget for accepted work to finish before abort |

Prefer one monotonic absolute deadline:

```ts
const deadline = performance.now() + budgetMs;
const remaining = () => Math.max(0, deadline - performance.now());
```

Each phase consumes from the same budget. Resetting a full timeout per phase violates an end-to-end promise.

## TCP state reminders

TCP is a byte stream. A read can return:

- part of one application frame;
- exactly one frame;
- several frames;
- zero bytes only according to API-specific semantics;
- EOF after all prior bytes;
- an error.

Half-close means one direction has ended while the other may remain usable. Product policy must say whether a peer that ends its request side may still receive a response.

`write()` acceptance means Node accepted data into its write path. It does not prove peer receipt or application commit.

## UDP checklist

A request/response protocol above UDP normally needs:

- version;
- message type;
- request or nonce identity;
- bounded payload;
- peer policy;
- deadline;
- retry schedule;
- response correlation;
- duplicate and stale-response policy;
- amplification consideration.

Discovery is not authorization. A valid discovery response only tells the client which endpoint answered the discovery contract.

## HTTP method vocabulary

- **safe**: intended not to request state change, such as GET or HEAD;
- **idempotent**: repeating the same intended request has the same intended effect, such as PUT under an appropriate application contract;
- **cacheable**: response may be reused under HTTP caching rules and response metadata;
- **conditionally applicable**: preconditions such as `If-None-Match` or `If-Match` control whether the operation proceeds.

A POST can become safely retryable under an application idempotency protocol. The method name alone is insufficient.

## Stable problem details

A useful application error response contains:

```json
{
  "type": "https://servicewire.invalid/problems/body-too-large",
  "title": "Request body exceeds the configured limit",
  "status": 413,
  "code": "BODY_TOO_LARGE",
  "detail": "The request body exceeded 65536 bytes.",
  "requestId": "..."
}
```

The `code` is a stable programmatic identifier. `detail` must be bounded and must not contain stack traces, secrets, raw authorization headers, or unbounded peer input.

## Idempotency record

At minimum, record:

```text
idempotency key
request fingerprint
state: in-progress | terminal
terminal response or result identity
retention time
```

Rules:

- unseen key: create in-progress record and become commit authority;
- same key, same fingerprint, in progress: attach or report accepted state;
- same key, same fingerprint, terminal: replay the terminal response;
- same key, different fingerprint: conflict;
- expired key: apply the documented retention policy.

The fingerprint must cover the semantic request, not incidental JSON whitespace or header ordering.

## Entity tags

An ETag identifies a selected representation version. ServiceWire uses a quoted revision-derived tag such as:

```text
"job-7-rev-3"
```

`If-None-Match` can turn an unchanged GET into `304 Not Modified`. A future state-changing operation may use `If-Match` to reject stale writers. ETags are not cryptographic authentication.

## HTTP client checklist

For every operation define:

- agent and socket-pool ownership;
- total deadline;
- connection and response-body limits;
- acceptable status and media type;
- redirect policy;
- retry eligibility;
- idempotency evidence;
- maximum attempts and delay budget;
- cancellation cleanup;
- body-consumption or discard rule;
- agent shutdown.

A response object is not complete product success until the required body has been bounded, consumed, validated, and released.

## TLS checklist

Separate these questions:

1. Was the channel encrypted?
2. Was the certificate chain trusted?
3. Did the certificate identify the requested hostname?
4. Which application protocol did ALPN select?
5. Is this authenticated identity authorized for the requested operation?

Never use `rejectUnauthorized: false` as a routine repair. Local fixtures should configure a dedicated teaching CA and the expected server name.

## HTTP/2 checklist

Track separately:

- session ownership;
- session-level error;
- stream ownership;
- stream reset;
- stream body bound;
- maximum concurrent streams;
- local and remote settings;
- flow-control windows;
- GOAWAY;
- graceful session close;
- forced destruction.

A stream can fail without invalidating every other stream. A session failure affects all streams it owns.

## SSE wire format

```text
id: 42
event: job-updated
data: {"jobId":"job-7","state":"succeeded"}

```

Rules:

- each event ends with a blank line;
- multi-line data requires one `data:` field per line;
- event IDs are opaque replay positions;
- comments such as `: heartbeat` can keep intermediaries and clients active;
- a bounded journal needs an explicit replay-gap response;
- slow subscribers need a queue bound and removal policy.

## Admission map

A service can have several distinct capacities:

```text
listening sockets
accepted connections
requests currently parsing
application commands waiting
active domain work
retained idempotency records
event-journal entries
SSE subscribers
per-subscriber queued bytes
HTTP/2 sessions
HTTP/2 streams
```

Do not use one `maxConnections` setting as if it bounded all of these.

## Shutdown phases

A defensible shutdown sequence is:

```text
1. quiesce
   stop new acceptance and report not-ready

2. drain
   allow accepted operations to finish under one grace deadline

3. abort
   cancel or destroy operations still active after grace

4. join
   observe every owned task, connection, session, and timer

5. report
   publish one authoritative terminal summary and exit status
```

Calling `server.close()` is one mechanism within this process, not the complete product lifecycle.
