# Module 76: Backpressure, Admission Control, and Fair Work Distribution

**Course 8, day 6 · Module 76 of 80**

**76/80** · [Course overview](../index.md) · [Workbook](workbook.md) · [Solutions](solutions.md) · [JobWire guide](../capstone.md)

## The question

> When demand exceeds service capacity, where may work wait, which bound is authoritative, and how does overload become an explicit product outcome instead of memory growth, latency collapse, or starvation?

## Why this comes now

The first week created futures, owned tasks, bounded frames, connection lifecycles, and a typed protocol. Those pieces can still form an unbounded service. A connection limit does not bound requests per connection. A bounded broker queue does not bound accepted sockets. A semaphore around active work does not bound queued response bodies. Retries can multiply demand even when every individual client is bounded.

Async systems are particularly vulnerable because waiting does not consume one OS thread. That scalability advantage can conceal enormous numbers of suspended futures, retained buffers, channel messages, and timers. “Nothing is blocking” can coexist with memory exhaustion and minute-long tail latency.

This module treats backpressure as an end-to-end flow-control contract. The service calculates a resource envelope, admits work only when it can own the consequences, and returns a deliberate overload response when it cannot.

## What you will be able to do

- find every accumulation point in an async service;
- distinguish connection admission, queue capacity, active-work permits, response buffering, and retry budgets;
- choose between waiting, rejecting, shedding, degrading, and disconnecting under overload;
- acquire permits before irreversible commitment;
- use bounded `mpsc`, semaphores, and actor ownership without assuming they imply fairness;
- separate queue capacity from concurrency limit;
- prevent head-of-line blocking where one slow class occupies shared capacity;
- define per-connection and global in-flight limits;
- calculate a conservative memory/resource envelope;
- test saturation deterministically.

## Core model

### Backpressure is propagation of limited capacity

A producer creates demand. A consumer has finite service rate and finite storage. Backpressure is the mechanism by which the consumer’s limited capacity changes producer behavior.

Possible propagation forms:

```text
producer awaits capacity
producer receives BUSY / rate-limited response
producer drops low-priority work
connection admission pauses
upstream transport window eventually closes
request is rejected before body read or commit
```

The correct choice depends on the boundary. Waiting can preserve work but consume deadlines and connection resources. Rejecting preserves service health but shifts retry responsibility upstream. Dropping may be acceptable for telemetry but not financial transactions.

### Bound every accumulation point

Create a capacity ledger before choosing primitives:

| Accumulation point | Unit | Maximum | Owner | Saturation outcome |
|---|---|---:|---|---|
| accepted connections | sockets/tasks | 256 | listener | wait in backlog or reject |
| per-connection decoded requests | requests | 1 in V1 | connection task | stop reading until response |
| broker mailbox | owned requests | 128 | broker sender | wait within deadline or BUSY |
| active jobs | permits | 16 | broker | remain queued |
| result payload | bytes/job | 64 KiB | job | domain error if exceeded |
| idempotency records | entries | 10,000 | broker | deterministic expiry/eviction |
| HTTP request body | bytes | 4 KiB | HTTP handler | 413 response |
| client retries | attempts | 4 | client | terminal failure |

The envelope is not simply the sum of advertised limits; some resources overlap and each item has overhead. The point is to make growth dimensions finite and reviewable.

### Admission occurs before commitment

A service should acquire the capacity needed to own a request before acknowledging or committing to it. If a connection reads a 64 KiB frame, sends “accepted,” and only then waits for a job permit, the service has promised more than it can deliver and retained the request indefinitely.

Possible commit points:

- after acquiring a broker queue slot;
- after the broker records an idempotency entry;
- after acquiring active-work capacity;
- after durable storage, in a persistent system.

Name the application commit point separately from socket write or channel send. If admission times out before commit, a `BUSY` response is honest. If timeout occurs after commit, the client may need idempotent recovery.

### Bounded channel and semaphore solve different dimensions

A bounded `mpsc` channel limits queued messages. A semaphore limits concurrent holders. A common broker uses both:

```text
bounded mailbox: limits requests waiting for broker inspection
job semaphore: limits expensive operations executing concurrently
```

If the broker waits to acquire a job permit while processing its mailbox, it may stop answering status, cancellation, or duplicate requests. A stronger actor records the request, then spawns or queues work through a separate bounded scheduler so the state authority remains responsive.

Conversely, spawning one task per queued request that waits on the semaphore recreates an unbounded task queue. The scheduler must own a bounded waiting structure.

### Queueing changes latency before capacity is exhausted

At high utilization, queueing delay grows sharply. A service can remain below its hard capacity while violating latency objectives. Backpressure policy therefore uses both hard bounds and deadlines:

- maximum queue length prevents unbounded memory;
- request deadline prevents work from becoming useless while waiting;
- admission metrics reveal saturation;
- early rejection may protect useful work already admitted.

A queue is not free capacity. It is stored latency.

### Fairness is a policy, not a default guarantee

Tokio channels and semaphores have documented ordering behaviors, but application fairness includes more:

- one connection sending many requests;
- one tenant occupying every permit;
- large jobs delaying small jobs;
- slow response consumers retaining completed results;
- retry storms from one upstream.

Fairness strategies include:

- per-connection in-flight limits;
- per-tenant queues and quotas;
- round-robin scheduling;
- separate classes or pools;
- weighted admission;
- maximum job cost;
- deadline-aware dropping.

Every strategy trades throughput, complexity, predictability, and isolation. Course 8 requires a simple explicit policy, not a universal scheduler.

### Head-of-line blocking can cross layers

Head-of-line blocking occurs when one slow item prevents unrelated work from advancing. Examples:

- one connection processes requests sequentially and a long job blocks later pings;
- the broker awaits active capacity inside its receive loop;
- one shared output queue contains a large response before small responses;
- HTTP health checks query a blocked broker through the same saturated channel as jobs.

Sometimes sequential behavior is intentional. JobWire V1 uses one in-flight request per TCP connection, but concurrency across connections. Health reads an atomic/advisory snapshot rather than waiting behind the work queue. State the boundary.

### Slow consumers are resource owners

A client that stops reading can cause response bytes and tasks to remain live. Bound response size, apply write deadlines, and avoid retaining a broker permit while waiting for a slow socket. Commit results to broker-owned bounded state, release execution capacity, then let the connection retrieve or write the result under its own deadline.

This separation prevents network slowness from occupying compute capacity.

### Overload responses are protocol behavior

A structured overload response can include:

```text
BUSY request-id retry-after-ms
```

The retry hint is advisory and should not invite synchronized retries. Clients still need jitter and an overall deadline. The server should distinguish:

- connection admission rejection;
- broker queue saturation;
- tenant quota;
- service shutting down;
- request too large.

Do not map every overload to an internal error. Overload is expected product behavior at a finite boundary.

### End-to-end backpressure crosses network directions

If a server stops reading because its request budget is full, TCP receive windows eventually limit the sender. But bytes may already be buffered in the kernel, runtime, codec, and client. Relying only on transport flow control gives a large and platform-dependent envelope. Application-level bounds and explicit rejection provide earlier control.

On the response side, a server that keeps reading unlimited requests while the client is not reading responses can accumulate unbounded result state. Sequential V1 request/response naturally limits this to one per connection. Pipelined versions need an explicit maximum.

### Saturation tests need controlled gates

Do not test overload by launching many tasks and sleeping. Use:

- a semaphore or notification that holds workers at a known point;
- a bounded queue with a known capacity;
- channels acknowledging admission;
- paused time for admission deadlines;
- assertions on exact accepted, queued, rejected, and active counts.

The test should prove the transition at capacity, not hope the scheduler reaches it.

## Use the idea in a complete program

A bounded relay separates mailbox capacity from active work. This simplified version owns all waiting requests in one broker task and never spawns more active jobs than permits.

```rust
use std::{collections::VecDeque, future::Future, sync::Arc};
use tokio::{
    sync::{mpsc, oneshot, Semaphore},
    task::JoinSet,
};

pub struct Request<I, O, E> {
    pub input: I,
    pub reply: oneshot::Sender<Result<O, E>>,
}

pub async fn run_broker<I, O, E, F, Fut>(
    mut rx: mpsc::Receiver<Request<I, O, E>>,
    max_active: usize,
    work: F,
) where
    I: Send + 'static,
    O: Send + 'static,
    E: Send + 'static,
    F: Fn(I) -> Fut + Clone + Send + 'static,
    Fut: Future<Output = Result<O, E>> + Send + 'static,
{
    let permits = Arc::new(Semaphore::new(max_active));
    let mut waiting = VecDeque::new();
    let mut active = JoinSet::new();
    let mut input_closed = false;

    loop {
        while let Some(request) = waiting.pop_front() {
            let Ok(permit) = Arc::clone(&permits).try_acquire_owned() else {
                waiting.push_front(request);
                break;
            };
            let operation = work.clone();
            active.spawn(async move {
                let _permit = permit;
                let result = operation(request.input).await;
                let _ = request.reply.send(result);
            });
        }

        if input_closed && waiting.is_empty() && active.is_empty() {
            break;
        }

        tokio::select! {
            received = rx.recv(), if !input_closed => match received {
                Some(request) => waiting.push_back(request),
                None => input_closed = true,
            },
            joined = active.join_next(), if !active.is_empty() => {
                let _ = joined;
            }
        }
    }
}
```

This is not yet a full production broker. The waiting queue is bounded only by the input channel plus messages already received, so a production design gives it an explicit maximum or keeps requests in the bounded channel until a slot exists. Panic outcomes are ignored here and must be classified in a complete implementation. The example exposes the design question rather than hiding it.

## Practice sequence

1. Enumerate every accumulation point in JobWire.
2. Compare channel capacity and active-work permits.
3. Move admission before the application commit point.
4. Design a `BUSY` response and retry hint.
5. Prevent the broker state loop from waiting on long work.
6. Separate compute capacity from slow network writers.
7. Add per-connection fairness.
8. Test exact saturation with controlled gates.

## Ready to continue

Continue only when you can explain:

- why async waiting can still consume unbounded memory;
- what each queue and semaphore bounds;
- where admission becomes commitment;
- why a queue stores latency;
- how one slow consumer can retain resources;
- what fairness policy exists;
- how overload is observed by the peer.

## Primary Rust references

- Tokio bounded `mpsc`, `oneshot`, and `Semaphore` documentation;
- Tokio task and time contracts from Modules 72 and 77;
- protocol overload and retry fields defined by the product rather than inferred from runtime behavior.

## Continue

Complete the [workbook](workbook.md), use the [reasoned solutions](solutions.md) only after freezing your own answer, build [Bounded Relay Broker](../../labs/module-06-bounded-relay-broker/README.md), and add the sixth [JobWire increment](../capstone.md#increment-6-bound-demand-end-to-end). Then continue to [Module 77](../module-77-cancellation-safety-deadlines-and-graceful-shutdown/index.md).
