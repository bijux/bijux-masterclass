# Final Review: Build and Defend an Async Service

The final review is independent transfer. Do not modify JobWire. Build a smaller **LeaseClock** service from the specification below, then defend it through the same ledgers used throughout Course 8.

## Product

LeaseClock accepts TCP clients using a length-delimited protocol. A client negotiates version 1, then may acquire, renew, inspect, or release a named lease. Each lease has an owner token and an expiry time. The service also exposes HTTP `/health` and `/stats` routes.

Required commands:

```text
HELLO 1
ACQUIRE <request-id> <idempotency-key> <name> <ttl-ms>
RENEW <request-id> <idempotency-key> <name> <owner-token> <ttl-ms>
GET <request-id> <name>
RELEASE <request-id> <idempotency-key> <name> <owner-token>
QUIT
```

## Required guarantees

- frame payloads are bounded before allocation;
- one connection cannot create an unbounded number of tasks;
- all state transitions are owned by one broker task or protected by an equally explicit protocol;
- acquire, renew, and release are idempotent within a documented retention window;
- a reused idempotency key with different request content is rejected;
- expiry uses one monotonic time source;
- clients receive stable request identifiers in responses;
- graceful shutdown stops admission, signals connections, drains a configured interval, aborts leftovers, and joins all tracked tasks;
- `/health` distinguishes runtime responsiveness from admission readiness;
- `/stats` reports advisory counts and labels them as such;
- output and tests do not depend on task completion order.

## Required artifacts

1. A future-state ledger for the timer or expiry task.
2. A task tree showing listener, connection tasks, broker, expiry work, HTTP service, and shutdown owner.
3. A frame grammar and maximum-size calculation.
4. A protocol state machine with error scope.
5. A full capacity ledger.
6. A cancellation ledger for every `select!` branch and timeout.
7. An idempotency and retry ledger.
8. A service dossier naming guarantees and non-guarantees.
9. Unit, integration, paused-time, chunking, retry, and shutdown tests.
10. A short operational guide that states every configured bound.

## Adversarial scenarios

Your implementation must be tested against:

- one-byte frame delivery;
- several frames delivered in one read;
- a length prefix above the maximum;
- clean EOF and truncated EOF;
- command before handshake;
- unsupported version;
- repeated identical idempotent request;
- key reuse with a changed payload;
- client disconnect after sending but before reading the response;
- queue saturation;
- deadline expiry while waiting for capacity;
- cancellation during connection handling;
- shutdown with idle, active, and blocked clients;
- a slow HTTP client;
- paused-time lease expiry;
- a broker task panic injected under test.

## Oral defense

Explain without opening the code:

1. What makes another poll of your expiry future useful?
2. Which task owns lease state and why?
3. Where is the application commit point?
4. What happens when a client times out after the commit but before the response?
5. Which limits bound memory as client count grows?
6. Which operations are cancellation safe?
7. What does health prove, and what does it not prove?
8. How does shutdown reach every task?
9. Why do your tests remain deterministic?
10. Which part would change first for a multi-process deployment?

A complete answer names both a mechanism and its product consequence. “Tokio handles it” or “the channel is bounded” is not sufficient.

## Build sequence

Implement LeaseClock in ten explicit increments. Preserve a passing state after each increment.

### 1. Freeze the domain before networking

Define validated lease names, owner tokens, TTL bounds, lease state, and terminal domain errors. Use an injected monotonic clock or Tokio time boundary so expiry can be tested with paused time. Decide whether an expired lease is removed eagerly by a timer, lazily on access, or through a hybrid policy. Record the cost and race implications of that choice.

### 2. Prove framing independently

Implement and test the codec without sockets. Every split point must decode to the same messages. Coalesced frames must remain separately recoverable. An oversized prefix must fail before reserve. An interrupted final frame must be distinguishable from clean EOF.

### 3. Define a total protocol machine

Separate byte framing, textual or binary syntax, argument validation, and state transition. Enumerate every connection-state/message pair. Assign each failure a scope: request, connection, or service. Do not use a wildcard transition to hide an unexamined case.

### 4. Create one state authority

Put lease mutation, expiry decisions, idempotency records, and capacity decisions behind one broker task or an equivalently explicit synchronization protocol. State precisely when `ACQUIRE`, `RENEW`, and `RELEASE` commit. A response write is not the commit point.

### 5. Add bounded connection ownership

The listener must acquire admission capacity before spawning connection work. Each accepted connection has one owner, one protocol state, one framed buffer, and one tracked terminal outcome. Idle and write deadlines must have distinct meanings.

### 6. Add HTTP without duplicating authority

The HTTP layer reads snapshots or asks a narrow operational service. It must not mutate leases or create a second source of truth. Bound request bodies even when the current routes expect none. Track and drain every HTTP connection task.

### 7. Add idempotency and retry semantics

Use separate request IDs and idempotency keys. Store a fingerprint and in-progress/completed state. Equal retries attach or replay. Changed content conflicts. Define record capacity and retention. Build a client test where the server commits and the connection disappears before the response is observed.

### 8. Add shutdown as a protocol

Publish not-ready state, stop listeners and broker admission, reject buffered uncommitted work, signal children, drain under one absolute deadline, abort leftovers, and join all handles. Lease expiry work and HTTP connections must appear in the same task tree.

### 9. Add causal adversarial tests

Use notifications, channels, paused time, scripted streams, and status snapshots to place the service in a known state. Do not infer that a queue is full or a timer is armed merely because a sleep elapsed.

### 10. Write the service dossier

State the wire version, bounds, commit points, retry policy, retention policy, health meaning, shutdown behavior, determinism promises, and non-guarantees. The dossier should allow a reviewer to predict behavior without reading implementation details.

## Acceptance matrix

| Area | Required evidence |
|---|---|
| future mechanics | no lost wake path; latest waker stored; terminal polling contract stated |
| task ownership | listener, connections, broker, expiry work, HTTP, and shutdown all have join owners |
| framing | arbitrary chunking invariance; checked arithmetic; bounded allocation; explicit EOF behavior |
| protocol | total state table; stable errors; version policy; canonical rendering |
| capacity | every accumulation point named with unit, bound, and overload result |
| cancellation | every selected or timed future classified; post-commit ambiguity documented |
| idempotency | equal replay, in-progress duplicate, changed fingerprint, retention, and capacity tested |
| retry | narrow retry classes; one semantic key; attempt bound; backoff cap; one overall deadline |
| HTTP | body bound, total routing, honest health, stable stats, tracked connection shutdown |
| lifecycle | admission closes first; cooperative drain; one grace deadline; abort; complete joins |
| determinism | stable output and assertions independent of legal completion order |
| documentation | guarantees and non-guarantees agree with code and tests |

A feature is not accepted merely because one end-to-end test succeeds. Each row needs direct evidence at the layer that owns the claim.

## Non-guarantees you must state

At minimum, decide and document whether LeaseClock does **not** guarantee:

- durable leases across process restart;
- exactly-once execution across process or network partition;
- authenticated owner identity;
- fairness among all clients under sustained overload;
- precise wall-clock expiry across system-clock changes;
- multi-process coordination;
- zero-copy framing;
- continued service after broker panic;
- unlimited idempotency retention;
- compatibility with unknown future protocol versions.

Honest exclusions strengthen the product. An unstated non-guarantee becomes an accidental promise.

## Self-review standard

Your final build is ready for defense only when you can perform these tasks without consulting JobWire:

1. draw the complete task tree and shutdown order;
2. trace one successful acquire and one ambiguous retry at ownership level;
3. calculate a conservative memory envelope from all configured capacities;
4. identify the exact line or transition that commits a lease mutation;
5. explain what each timeout cancels and what it cannot undo;
6. show that every accepted child task is joined;
7. show that every accepted semantic operation reaches one terminal idempotency state;
8. derive the HTTP health result from authoritative service state;
9. reproduce the protocol transition table from memory;
10. name the first architectural change required for durable or multi-process leases.

Where an explanation becomes vague, return to the corresponding ledger. Do not patch the defense with more framework terminology.
