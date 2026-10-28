# Module 55 — HTTP Application Boundaries: Routing, Validation, Errors, and Idempotency

**Progress: 55/100**

## The governing question

> How do you turn a valid HTTP message into one typed application command, commit it exactly under the product's rules, and return a stable representation that can be replayed or conditionally reused?

## Why this module comes now

Module 54 established the finite HTTP message boundary. The adapter can now produce method, path, headers, and a bounded parsed body. Those facts are still not a domain command.

This module builds the application protocol: route selection, path parameters, runtime validation, stable errors, idempotency records, representation revisions, and conditional reads. It is the point where the service decides what a request means.

The crucial distinction is:

```text
HTTP request accepted
        ≠
application command committed
```

A request can be syntactically valid yet rejected before semantic commit. Once a state-changing command commits, a lost response must not cause a retry to create a second effect.

## Observable outcomes

By the end of the module, you can:

- define a route table with unambiguous precedence;
- parse exact path parameters without treating arbitrary strings as identifiers;
- validate query, header, and body data from `unknown`;
- separate application commands from transport objects;
- design stable problem types and status mappings;
- implement idempotency-key syntax, fingerprints, in-progress state, replay, conflict, retention, and capacity;
- assign revisions to representations;
- generate entity tags and implement `If-None-Match`;
- distinguish request IDs, job IDs, event IDs, and idempotency keys;
- identify the component that owns semantic commit.

## The application boundary ledger

| Input or state | Example | Authority |
|---|---|---|
| request ID | `req-...` | diagnostics |
| idempotency key | random client token | semantic retry identity |
| path job ID | `job-000001` | route validator |
| submission body | operation and payload | runtime validator |
| request fingerprint | canonical semantic request | idempotency authority |
| job ID | server-assigned | job store |
| job revision | monotonic integer | job state transition |
| ETag | quoted representation tag | response renderer |
| event sequence | monotonic event position | event journal |
| problem code | `IDEMPOTENCY_CONFLICT` | public error contract |

These identifiers solve different problems. Reusing one string everywhere makes logs look simpler while corrupting semantics.

## Routing is ordered grammar

A router is not a list of string comparisons. It is a grammar over method and path.

For ServiceWire:

```text
GET|HEAD /v1/health
GET      /v1/stats
POST     /v1/jobs
GET|HEAD /v1/jobs/:jobId
GET      /v1/events
```

Static routes should normally win before parameter routes. Path decoding needs a policy for percent-encoding, empty segments, trailing slashes, repeated slashes, and query strings. Avoid broad regular expressions that accept strings the identifier validator later interprets differently.

The route result should be typed:

```ts
type Route =
  | { readonly kind: 'health'; readonly head: boolean }
  | { readonly kind: 'stats' }
  | { readonly kind: 'submit' }
  | { readonly kind: 'job'; readonly id: JobId; readonly head: boolean }
  | { readonly kind: 'events'; readonly after?: number };
```

An exhaustive switch then proves every route kind is handled.

## Runtime validation creates trusted commands

TypeScript types do not validate network values. Parse JSON to `unknown`, then validate exact shape:

```ts
interface SubmitCommand {
  readonly operation: 'uppercase' | 'word-count' | 'checksum' | 'sleep';
  readonly payload: string;
}
```

Decide:

- are extra properties rejected?
- are operation names case-sensitive?
- what is the maximum payload in characters and bytes?
- what syntax is accepted for `sleep`?
- can an empty payload be legal for every operation?
- which fields participate in idempotency fingerprinting?

Validation should return structured issues with bounded paths and messages. A cast is not validation.

## The semantic commit point

A submission progresses through:

```text
network bytes
  → HTTP message
  → validated SubmitCommand
  → idempotency admission
  → job creation
  → event append
  → response
```

The idempotency authority and job store must agree on one commit sequence. If the response fails after job creation, the operation is still committed. A retry with the same key must observe or replay the same semantic result.

A process-local design can perform these steps synchronously under one JavaScript authority without an external transaction. Course 7 will revisit this when records become durable or distributed.

## Idempotency keys

A key is client-generated semantic identity. Define strict syntax and length, for example 16–128 visible ASCII characters from a safe subset. Do not accept unbounded arbitrary header values.

A record:

```ts
type IdempotencyRecord =
  | {
      readonly kind: 'in-progress';
      readonly fingerprint: string;
      readonly jobId: JobId;
      readonly createdAtMs: number;
    }
  | {
      readonly kind: 'terminal';
      readonly fingerprint: string;
      readonly jobId: JobId;
      readonly response: SubmitResponse;
      readonly createdAtMs: number;
    };
```

The design may expose an accepted response immediately after job creation rather than wait for job completion. In that case the terminal idempotency response is the stable submission result, while the job itself continues through later states.

## Fingerprint semantic input, not incidental bytes

Two JSON bodies can encode the same command with different whitespace and property order. Fingerprinting raw body bytes would treat them as different. Validate first, then create a canonical semantic representation:

```ts
function fingerprint(command: SubmitCommand): string {
  return createHash('sha256')
    .update(command.operation)
    .update('\0')
    .update(command.payload)
    .digest('hex');
}
```

The hash here is a compact equality key, not authorization. A simple collision-resistant digest is appropriate, but the idempotency record must still compare under one application authority.

Same key with:

- same fingerprint: replay or return existing job;
- different fingerprint: 409 conflict;
- no record: create and commit;
- capacity exhausted: reject before commit;
- expired record: apply retention policy.

## In-progress duplicates

Several retries can arrive while the first request is committing. Even in a single Node.js process, `await` can allow interleaving. The idempotency record should be created before any suspension that could admit another request for the same key.

If job creation is synchronous and local, create both record and job in one non-suspending section. If later code requires asynchronous durable persistence, the authority must become transactional or serialized. Course 7 addresses that escalation.

## Capacity and eviction

Idempotency is retained state. Define:

- maximum records;
- retention time;
- eviction order;
- whether in-progress records can be evicted;
- behavior when capacity is full;
- whether job records and idempotency records expire together.

Never evict an in-progress record merely to admit a new request; that can duplicate the operation after a retry. A simple course design rejects new submissions when capacity is full and evicts only old terminal records under explicit policy.

## Stable errors

An application problem is a public type. Examples:

| Code | Status | Meaning |
|---|---:|---|
| `ROUTE_NOT_FOUND` | 404 | no supported route |
| `METHOD_NOT_ALLOWED` | 405 | path known, method unsupported |
| `INVALID_REQUEST` | 422 | runtime/domain validation failed |
| `IDEMPOTENCY_KEY_REQUIRED` | 400 | submission lacked key |
| `IDEMPOTENCY_CONFLICT` | 409 | same key, different request |
| `JOB_NOT_FOUND` | 404 | valid ID not present |
| `OVER_CAPACITY` | 503 | service cannot admit a new job |
| `NOT_READY` | 503 | service is quiescing or unavailable |

Stable codes are more durable than English messages. Clients should not parse `detail`.

## Revisions and entity tags

Every job state transition increments a revision:

```text
queued rev 1
running rev 2
succeeded rev 3
```

The selected representation receives an ETag such as:

```text
"job-job-000001-rev-3"
```

On GET:

- no `If-None-Match`: return 200 and representation;
- matching ETag: return 304 with no body;
- nonmatching ETag: return 200 with current representation.

Parse conditional headers according to the supported subset. Do not compare unquoted improvised values while calling them ETags.

ETags support representation revalidation. They are not job identity or authorization.

## Problem response versus event publication

A rejected request that never commits a job should not produce a job-state event. A committed job submission whose response later fails still produces job events. This distinction helps reconcile client ambiguity.

Event publication must occur within the domain authority that changes state. HTTP adapters observe the result; they do not invent state-change events independently.

## Worked case — lost submission response

1. Client sends POST with key K and command C.
2. Server validates C.
3. No record exists for K.
4. Server creates in-progress record and job J.
5. Server returns 202, but connection resets before client receives it.
6. Client retries K with the same C.
7. Server finds same fingerprint and returns J.
8. Client retries K with different command D.
9. Server returns conflict.

The service creates one job. The response loss changes client knowledge, not server commit.

## Route handlers should not own network objects

A clean application interface receives typed values:

```ts
interface ServiceWireApplication {
  submit(
    command: SubmitCommand,
    key: IdempotencyKey,
  ): SubmitResult;

  getJob(id: JobId): JobView | undefined;
  stats(): ServiceStats;
  health(): HealthView;
}
```

It does not receive `IncomingMessage` or `ServerResponse`. This keeps domain semantics reusable across HTTP/1.1 and HTTP/2.

## Common wrong models

### “POST cannot be retried”

Method semantics alone do not decide application retry. A correct idempotency protocol can make a semantic submission retryable.

### “A request ID is enough”

Request IDs identify attempts. They do not bind several attempts to one operation.

### “Hash the raw body”

That makes whitespace and property order part of semantic identity.

### “Evict any idempotency record when full”

Evicting in-progress identity can duplicate work.

### “ETag is a checksum”

It is an opaque representation validator under the server's policy. It need not be content hash.

## Decision procedure

For every state-changing route:

1. validate method, path, headers, body, and command;
2. identify semantic retry key;
3. canonicalize and fingerprint semantic input;
4. define idempotency record states;
5. define one commit authority;
6. define replay and conflict behavior;
7. bound and retain records;
8. assign domain identity and revision;
9. publish events from the domain transition;
10. return stable status, representation, and ETag.

## ServiceWire increment

Implement:

- typed router;
- strict job ID and idempotency-key validators;
- `SubmitCommand`;
- process-local job and idempotency stores;
- stable problems;
- revisions and ETags;
- GET/HEAD conditional behavior;
- bounded retained records.

## Case study — ambiguous commit and the idempotency authority

A client sends:

```http
POST /v1/jobs
Idempotency-Key: order-import-2026-08-10-001
```

The server validates the command, creates `job-000021`, commits the idempotency record, and sends a 202 response. The connection resets before the client receives headers. The client now knows only that the response was lost. It does not know whether the semantic commit occurred.

A retry with the same key and same semantic command should return the existing job. A retry with the same key and different command must return conflict. This requires one authority to bind:

```text
idempotency key
    ↔ command fingerprint
    ↔ job identity
    ↔ replayable submission representation
```

If the idempotency record is inserted after the job, a crash or asynchronous gap can create an unrepeatable commit. In ServiceWire the store is process-local and the commit is synchronous, so the insertion sequence can be made indivisible with respect to other JavaScript execution. A durable service would need a database transaction or equivalent serialization boundary.

### Fingerprint semantics

Hashing raw JSON bytes is insufficient when semantically equivalent requests can differ in whitespace or property order. ServiceWire fingerprints the validated command fields in a canonical order. The fingerprint is not an authentication primitive; it is a compact equality witness inside one trusted process.

A useful review question is: **which differences should create conflict?** For example, changing `payload` clearly changes the command. Adding an ignored transport header should not. Changing a future optional field might or might not, depending on its semantic effect. The fingerprint definition is part of API evolution.

### ETags solve a different problem

An idempotency key reconciles creation. An ETag identifies one representation revision. `If-None-Match` can avoid transferring an unchanged job representation. It does not make `POST` idempotent and does not protect a state transition unless used with an appropriate precondition contract.

Keep the two mechanisms separate:

| Mechanism | Authority | Question answered |
|---|---|---|
| idempotency key | client chooses key; server stores binding | “Did this semantic creation already commit?” |
| job ID | server | “Which resource is this?” |
| revision | job authority | “Which state transition version is this?” |
| ETag | representation function | “Does the client already have this representation?” |

### Domain errors versus transport errors

The domain should return typed failures such as `OVER_CAPACITY`, `IDEMPOTENCY_CONFLICT`, or `JOB_NOT_FOUND`. The HTTP adapter maps them to status and problem documents. The domain must not depend on Node request objects or mutate responses. This keeps the same application authority reusable from HTTP/1.1 and HTTP/2.

### Bounded retention

Process-local idempotency still needs limits. Once `maxIdempotencyRecords` is reached, the service must reject new keys or evict by a documented policy. Silent eviction can turn a later retry into duplicate work. ServiceWire chooses bounded retention and explicit overload rather than claiming durable exactly-once behavior.

The reader should be able to trace every submission through four moments: validation, semantic commit, response construction, and response observation. Only the first three occur under server authority. The fourth belongs to the network and client.

## Ready to continue

You are ready for the client module when you can explain how a client reconciles a lost response without creating a second job.

## Primary references

- [Node HTTP](https://nodejs.org/docs/latest-v24.x/api/http.html)
- [RFC 9110 — HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110)
- [RFC 9457 — Problem Details](https://www.rfc-editor.org/rfc/rfc9457)

## Continue

- [Workbook](workbook.md)
- [Reasoned solutions](solutions.md)
- [Laboratory brief](../../labs/module-55-typed-http-router/README.md)
- [ServiceWire engineering guide](../capstone.md)
