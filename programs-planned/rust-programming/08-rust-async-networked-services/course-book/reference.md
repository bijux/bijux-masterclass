# Async and Network Service Reference Desk

Use this page after attempting recall. It compresses the course’s recurring distinctions; it is not a substitute for the module chapters.

## Future and task terms

| Term | Operational meaning |
|---|---|
| future | an inert value representing a computation that may be advanced by polling |
| `Poll::Ready(T)` | the future has completed and produced its terminal value |
| `Poll::Pending` | the future cannot complete now and has arranged a wakeup when progress may be possible |
| waker | a capability that schedules the owning task for another poll; it is not the result itself |
| suspension point | an `.await` location at which state may be retained and control returned to the executor |
| task | a future scheduled by an executor, with its own lifecycle and terminal outcome |
| cancellation by drop | abandoning a future by destroying its state machine; cleanup follows owned fields’ destructors |
| cancellation safe | repeatedly abandoning and recreating an operation does not lose or duplicate protocol state beyond the documented contract |

## Tokio task choices

| Need | Mechanism | Main obligation |
|---|---|---|
| concurrent `Send + 'static` async work | `tokio::spawn` | retain or deliberately detach the `JoinHandle` |
| dynamically managed child set | `JoinSet` | drain every terminal result and define shutdown |
| non-`Send` local future | `LocalSet` / `spawn_local` | remain on the local runtime context |
| blocking or CPU-heavy function | `spawn_blocking` | bound admission; cancellation cannot preempt already running blocking work |
| shared cancellation | `CancellationToken` | define which task owns cancellation and which children inherit it |

## Stream and frame distinctions

```text
TCP bytes ≠ read calls ≠ frames ≠ protocol messages ≠ committed operations
```

A decoder must handle:

- zero or more complete frames in one buffer;
- a partial prefix or payload;
- clean EOF with no buffered partial frame;
- truncated EOF with leftover incomplete data;
- length overflow and configured maximums;
- canonical encoding independent of read chunking.

## Capacity ledger

List every place bytes or work may wait:

| Location | Unit | Bound | Overload behavior |
|---|---|---:|---|
| accepted connections | permits | configured | reject or delay before spawning |
| per-connection input | bytes | frame maximum plus small overhead | close with protocol error |
| broker queue | requests | channel capacity | wait within deadline or reject busy |
| active jobs | permits | worker limit | remain queued or reject according to policy |
| completed idempotency records | entries/bytes/time | retention policy | expire or evict deterministically |
| outbound response | bytes | response maximum | reject internal result before encoding |

A bounded queue does not make the service bounded if accepted sockets, spawned tasks, bodies, retries, or completion records remain unbounded.

## Cancellation ledger

For each await point record:

| Operation | State before await | State owned by future | External side effect possible? | Safe to abandon? | Repair if not |
|---|---|---|---|---|---|
| channel receive | no item removed yet | receiver borrow | no | usually | none |
| write full frame | prefix may be written | remaining slice | yes | protocol-dependent | single writer plus explicit close/retry rule |
| broker commit | candidate request | reply sender and idempotency key | yes | only with transaction protocol | actor-owned commit point |
| sleep/backoff | retry state | timer | no | yes | none |

Do not memorize cancellation-safety lists. Derive them from state ownership and side effects.

## Network failure classes

| Class | Examples | Retry default |
|---|---|---|
| local configuration | invalid address, unsupported version | no |
| admission | busy, rate limited | perhaps, with deadline and server guidance |
| transient transport | connect refused, reset before send | perhaps |
| ambiguous transport | disconnect after request write | only with idempotency semantics |
| protocol | malformed response, state violation | no; treat peer or implementation as faulty |
| domain rejection | invalid command, impossible operation | no |
| internal server | temporary dependency failure | policy-specific |
| deadline exhausted | overall budget consumed | no further attempts |

## HTTP boundary

Keep four layers separate:

1. listener and accepted transport;
2. HTTP connection driver;
3. request routing and body policy;
4. application service and domain state.

A health route should report exactly what it can prove. “Process event loop is responsive” is weaker than “broker accepts work,” which is weaker than “all dependencies are healthy.” Name the level.

## Idempotency record

An idempotency key is meaningful only with a scope and request fingerprint:

```text
(scope, key) → request fingerprint + terminal state/result
```

If the same key arrives with a different fingerprint, reject it. If the first request is in progress, either attach a waiter or return an explicit in-progress response. Retention must be bounded by time, count, or memory.

## Test controls

Prefer causal controls over real-time sleeps:

- paused Tokio time and explicit advancement;
- barriers, channels, and notifications to place operations at a known state;
- duplex streams or local loopback sockets;
- scripted partial reads and writes;
- deterministic retry jitter sources;
- assertions on terminal outcomes and resource counts;
- timeouts around the whole test only as a hang detector, not as the protocol oracle.

## Choosing the execution boundary

| Work | Keep in the current future | Spawn an async task | Use blocking isolation |
|---|---|---|---|
| short, naturally part of caller result | usually | only when lifecycle independence is required | no |
| concurrent I/O child with explicit parent ownership | perhaps with `join!` | yes, if the parent retains and joins it | no |
| dynamic set of async children | awkward | `JoinSet` or equivalent owner | no |
| filesystem or library call that may block an OS thread | no | not directly | `spawn_blocking` or a dedicated bounded pool |
| sustained CPU work | no on runtime workers | only through a bounded CPU facility | dedicated pool or later parallel design |

Spawning is not merely a performance choice. It changes ownership, lifetime, panic observation, cancellation, and shutdown accounting.

## Deadline taxonomy

| Deadline | Question answered | Common mistake |
|---|---|---|
| connect | how long may address resolution and connection establishment take? | treating it as the whole request budget |
| handshake | how long may negotiation remain incomplete? | allowing a connected peer to hold a permit forever |
| idle | how long may no protocol progress occur? | resetting it on irrelevant activity |
| operation | how long may one broker or dependency operation take? | assuming timeout rolled the operation back |
| write stall | how long may a response remain unable to progress? | holding application capacity while waiting on a slow peer |
| overall request | what end-to-end budget remains across stages and retries? | restarting the full budget at every stage |
| shutdown grace | how long may cooperative draining continue before abort? | applying a fresh grace period to every child sequentially |

Prefer one absolute deadline when several stages share one budget. Derive remaining duration at each stage instead of nesting independent full-duration timeouts.

## TCP and UDP decision boundary

| Property | TCP | UDP |
|---|---|---|
| application sees | ordered byte stream | individual datagrams |
| message boundaries | must be designed | preserved per datagram |
| reliability | retransmission and ordering while the connection survives | no delivery, order, or duplicate guarantee |
| backpressure signal | writes and buffers eventually stall | sends can succeed while later delivery is lost |
| peer lifecycle | connection state exists | no connection semantics in the transport |
| typical course use | framed request/response protocols | bounded telemetry or application-defined reliability |

Neither transport authenticates the peer. A socket address is routing information and an observation, not a durable identity claim.

## Protocol error scope

| Error | Recover on same connection? | Typical response |
|---|---|---|
| unknown command with intact frame and known state | often | structured error, remain synchronized |
| invalid argument inside a known command | often | request-scoped rejection |
| unsupported negotiated version | no | negotiation error, then close |
| command before required handshake | usually no | state error, then close |
| frame length above maximum | no | close; do not attempt allocation or resynchronization |
| invalid frame encoding / truncated EOF | no | close; framing synchronization is lost |
| duplicate request ID | policy-specific | reject or define multiplexing semantics explicitly |
| idempotency conflict | request-scoped | stable conflict error; do not execute |

Recovery is safe only when the parser knows exactly where the next message begins and the connection state remains defined.

## Graceful shutdown sequence

A complete service usually needs this order:

```text
publish shutting-down state
→ stop accepting new transports
→ stop application admission
→ reject buffered but uncommitted commands
→ signal connection and worker children
→ drain under one absolute grace deadline
→ abort leftovers
→ join every task
→ publish or return the final report
```

Changing the order changes semantics. Cancelling workers before closing admission can accept work that can never start. Dropping join handles before observation erases panic and cancellation evidence. Waiting without one deadline can make total shutdown time proportional to child count.

## Retry prerequisites

Retry is defensible only when all of these are known:

1. the failure class is eligible under policy;
2. the operation is idempotent by nature or protected by a server-recognized idempotency key;
3. equal keys are bound to equal request fingerprints;
4. the server defines in-progress and completed duplicate behavior;
5. retention is long enough for the retry window and explicitly bounded;
6. the client retains one overall deadline and attempt limit;
7. backoff cannot exceed the remaining budget;
8. terminal domain and protocol failures are not disguised as transient transport failures.

“At least once on the wire” can still mean “once semantically” only when the server owns that semantic identity.

## Audit questions for any async service

Before calling a service complete, answer:

- Which futures can be dropped at each `select!` branch, and what state do they own?
- Which tasks can outlive the function that created them?
- Which handle observes each panic?
- Where can bytes, connections, requests, waiters, results, retries, and metrics accumulate?
- Which operation is the semantic commit point?
- Which response can be lost after commit?
- Which errors preserve framing and connection state?
- Which health fields are authoritative and which are snapshots?
- Which outputs must remain deterministic across legal schedules?
- What remains true after shutdown grace expires?

An answer that names only an API is incomplete. Name the product invariant the API helps enforce.
