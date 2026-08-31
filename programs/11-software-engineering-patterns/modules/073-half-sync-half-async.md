---
module_id: SEPAT-073
program: Software Engineering: Patterns
level: 2
module_number: 73
title: Half-Sync/Half-Async
status: complete
last_verified: 2026-08-29
---

# Half-Sync/Half-Async

## One-Page Review

### Governing question

How can a system combine efficient asynchronous event handling with comprehensible synchronous service code while making the queue between them a bounded, observable, cancellation-aware ownership and overload boundary?

### Essential definitions

- The **asynchronous service layer** owns event demultiplexing, connections or handles, framing, timers, admission, and bounded nonblocking callbacks.
- The **queueing layer** transfers immutable or exclusively owned work between concurrency models and defines capacity, ordering, fairness, deadlines, and rejection.
- The **synchronous service layer** contains worker threads or processes that execute sequential-looking, possibly blocking service logic.
- A **work item** is a self-contained request envelope with stable request identity, owner and generation, payload or payload lease, deadline, authority context, and result route.
- A **result item** is an immutable terminal or progress envelope returned to the async owner; it is not permission for a worker to mutate event-loop-owned state.
- **ownership transfer** establishes which layer may access mutable state or release resources at each handoff.
- **admission** decides whether work enters the bounded system; acceptance is not completion.
- **backpressure** slows, pauses, or rejects production before finite queues, workers, memory, or downstream capacity are exhausted.
- **queue wait** is the interval between accepted enqueue and worker start; it consumes the same end-to-end deadline as service.
- A **stale result** belongs to an earlier owner generation, expired authority, cancelled request, or already-terminal identity and therefore cannot mutate current state.

### Central model, mechanism, or theorem

For accepted request (r), the normal path is

$$
async\_admit \rightarrow Q_{work} \rightarrow sync\_execute
\rightarrow Q_{result} \rightarrow async\_deliver.
$$

The async layer creates envelope

$$
E_r=(request\_id,owner,generation,deadline,authority,payload),
$$

transfers it through bounded (Q_{work}), and is the only layer that later interprets the result against current connection and request state. With arrival rate λ, (k) workers, and mean service rate μ per worker, a necessary—not sufficient—stability condition is

$$
\lambda < k\mu.
$$

For a stable measured interval, Little's Law gives $L=\lambda W$, and response time decomposes as (T=W_q+S+W_r): work-queue wait, synchronous service, and result-delivery wait. A queue capacity (K) bounds queued payload memory approximately by (K b_{max}), but total memory also includes in-flight worker state, result backlog, connection state, and allocator/runtime overhead.

### Critical invariants

- The async owner never blocks on enqueue, worker completion, synchronous I/O, locks held by workers, or result handling.
- Both work and result queues have explicit finite capacity, ownership, admission policy, and saturation behavior.
- A work item contains stable identity, owner generation, monotonic deadline, authority snapshot/reference policy, immutable or exclusively owned payload, and one result route.
- Workers never retain or mutate raw sockets, event-loop objects, callbacks with unsafe lifetime, or connection-owned mutable state.
- Every accepted request reaches one logical terminal classification: delivered, rejected before acceptance, cancelled/expired, failed, or unresolved and reconciled.
- A result is applied only after request identity, owner generation, deadline policy, current authority, and terminal state are checked by the async owner.
- Queue wait is measured and deadline-checked before expensive work; expired jobs do not silently consume scarce service.
- Worker count, queue capacity, blocking concurrency, downstream pools, and tenant quotas form one capacity design.
- Ordering is explicit: FIFO dequeue does not guarantee result order, per-connection order, fairness, or effect order.
- Shutdown stops admission, chooses drain or cancel semantics, continues result reaping, and records work whose external effect is ambiguous.

### Common failures

Common failures include an unbounded default executor, blocking enqueue from the event-loop thread, passing a live connection or mutable request buffer to workers, allowing workers to write responses directly, treating cancellation of a future as cancellation of a blocking operation, accepting jobs whose deadlines expire in the queue, sizing threads without the downstream connection pool, one shared pool causing priority inversion, assuming FIFO completion, silently dropping rejected jobs, unbounded result accumulation, retrying ambiguous effects with new identity, shutting down the loop before results are reaped, and reporting low worker service time while excluding queue wait.

### Compact example

An event loop admits two immutable requests to a capacity-two queue and rejects a third with an explicit overload result. Worker `w1` completes request `r1` for connection generation 1. Before delivery, that connection closes and reopens as generation 2, so the loop classifies `r1` as stale. Worker `w2` completes `r2` for an unchanged connection and the loop delivers it. Neither worker ever owns a socket; the finite queue bounds retained jobs and makes rejection testable.

### Connections

[SEPAT-071](071-reactor.md) supplies a readiness-driven async layer; [SEPAT-072](072-proactor.md) supplies a completion-driven one; [SEPAT-074](../ROADMAP.md) explores Leader/Followers as another concurrency structure. Half-Sync/Half-Async also connects to [Operating Systems](../../22-operating-systems/ROADMAP.md), [Software Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md), [Security Engineering](../../25-security-engineering/ROADMAP.md), [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md), and [Platform Engineering](../../29-platform-engineering/ROADMAP.md).

## Governing Question

When an asynchronous I/O layer is efficient but business or legacy service logic is naturally synchronous, how should the system separate their concurrency models without hiding blocking, losing ownership, or converting overload into an ever-growing queue?

Half-Sync/Half-Async is an architectural pattern, not a promise that adding a pool makes any event-driven system safe. It integrates a lower asynchronous service layer with an upper synchronous service layer through an explicit queueing layer. Its quality depends on the semantics of both handoffs: what is copied or transferred, what is bounded, who may mutate what, how a deadline and cancellation cross the boundary, and how results rejoin the asynchronous owner.

## Why This Matters

Network gateways, database proxies, protocol servers, GUI applications, storage controllers, and integration services often have two incompatible needs. They need one or a few asynchronous threads to multiplex many handles efficiently, yet they also need sequential code that calls blocking libraries, uses thread-affine facilities, or expresses a complex transaction clearly. Rewriting every dependency as nonblocking may be impossible or economically unsound.

The pattern creates a deliberate impedance matcher. The async layer protects multiplexing efficiency; the sync layer protects straight-line reasoning; the queue controls their interaction. If that queue is implicit or unbounded, a burst becomes retained memory and extreme latency. If the loop blocks while submitting, one saturated worker pool freezes unrelated I/O. If a worker receives a socket, connection object, or borrowed buffer, ownership races return. Production use therefore requires a capacity and lifecycle contract, not merely an executor call.

## Prerequisites and Retrieval

You should understand threads, event loops, Reactor or Proactor, producer-consumer queues, mutual exclusion, memory visibility, deadlines, cancellation, partial I/O, backpressure, idempotency, and basic queueing. Retrieve these facts:

1. Readiness and completion handlers must stay bounded if one dispatch thread serves many handles.
2. A thread-safe queue provides synchronization for the envelope; it does not make arbitrary referenced objects safe to share.
3. A finite worker pool has finite throughput even when submission is asynchronous.
4. A blocking call may ignore or delay cancellation and may have an external effect before returning.
5. Connection/descriptor identity can be reused; a generation distinguishes old results from a current owner.
6. FIFO dequeue order does not imply FIFO completion across multiple workers.
7. A request deadline covers admission, queue wait, service, result queueing, and delivery—not service time alone.
8. A finite input queue without an explicit full policy merely moves the overload decision into an exception or accidental block.

## Learning Objectives

After completing this module, you should be able to:

- identify the asynchronous, queueing, and synchronous participants and assign their ownership;
- distinguish Half-Sync/Half-Async from a generic thread pool, Active Object, Reactor, Proactor, and Leader/Followers;
- design immutable work/result envelopes with identity, generation, deadline, authority, payload ownership, and terminal correlation;
- derive necessary capacity constraints from arrival rate, worker service rate, downstream limits, memory bounds, and deadlines;
- choose finite admission, backpressure, rejection, shedding, and fairness policies without blocking the async owner;
- preserve visibility and mutable-state isolation across queue handoffs;
- handle queue expiry, cancellation, late/stale results, reordered completions, worker failure, and ambiguous effects;
- size and isolate worker pools according to CPU, blocking ratios, dependencies, tenants, and service classes;
- design staged shutdown that stops admission, drains or cancels, reaps results, and reconciles unresolved work;
- verify correctness with deterministic models, saturation tests, race schedules, fault injection, observability, and domain review.

## Core Exposition

### Separate concurrency models by responsibility

The asynchronous layer owns the resources that demand multiplexing: listeners, connections, event registrations, completion handles, timers, protocol state, and output readiness. Its handlers parse only enough bounded input to identify a valid request, apply cheap admission and authorization gates, construct an owned work envelope, and return. It does not wait for workers or downstream services.

The synchronous layer owns service execution. A worker dequeues one envelope and may call a blocking database driver, legacy library, filesystem API, or sequential domain algorithm. It produces a result envelope and relinquishes request resources. It does not call non-thread-safe event-loop APIs or decide whether an old connection may receive the result.

The queueing layer is a first-class participant. It adapts push-style async arrival to pull-style synchronous workers, supplies a memory-visibility edge according to the chosen implementation, holds work during short bursts, and exposes the exact point at which the system must exert pressure or reject. A concurrent queue alone does not establish the whole protocol; envelope ownership and terminal bookkeeping do.

### Model the two handoffs

On admission, the async owner validates frame size and representation, captures stable request and tenant identity, establishes deadline, leases or copies bounded payload storage, records owner generation, and tries a nonblocking enqueue. Success transfers envelope ownership to the work pipeline. Failure retains ownership long enough to release resources and return the documented overload outcome.

A worker checks whether the job is already expired or cancelled before scarce downstream work. It executes under a bounded dependency budget, catches failures into a typed result, and attempts bounded publication. The result carries request ID, owner/generation, status, effect identity or reconciliation evidence, and safe response data—not a closure that assumes connection lifetime.

The async owner reaps results, looks up the current request, validates generation and terminal state, rechecks policy that can change during long service where required, and either schedules bounded output or classifies the result stale/late. This second validation is essential because correct worker execution does not prove that delivery remains authorized or meaningful.

### Make envelopes self-contained

A work envelope commonly contains:

| Field | Purpose | Failure prevented |
| --- | --- | --- |
| `request_id` | Deduplication and terminal correlation | Duplicate/misattributed result |
| `owner_id`, `generation` | Detect closed/reused connection or session | Stale mutation/data disclosure |
| `tenant`, `principal`, authority reference | Quota and authorization context | Cross-tenant work/confused deputy |
| `accepted_at`, `deadline` | Queue age and end-to-end expiry | Expensive work after usefulness |
| operation and version | Dispatch and schema compatibility | Ambiguous handler/version skew |
| payload or lease | Exclusive/immutable data ownership | Concurrent mutation/use-after-release |
| effect/idempotency identity | Reconcile retries and ambiguous effects | Duplicate external effect |
| trace/correlation | End-to-end observation | Invisible queue latency |

Avoid raw descriptors, pointers into a mutable parser buffer, live ORM sessions, implicit thread-local authority, and event-loop callbacks. If a payload is too large to copy, transfer an explicitly leased immutable segment whose release is tied to a terminal path. The queue implementation may create a happens-before edge, as Java `BlockingQueue` specifies, but that visibility does not grant safe concurrent mutation after enqueue.

### Treat queue capacity as a contract

There is no neutral queue choice. A direct handoff accepts only when a worker can take work, tightly coupling admission to instantaneous service. A bounded buffer absorbs a measured burst and gives a finite memory/latency budget. An unbounded queue accepts overload until memory, deadlines, or operational tolerance fail.

For capacity (K), worst-case queued payload storage is bounded by (K b_{max}) only when every payload actually obeys (b_{max}) and shared/referenced storage is accounted for. Add worker in-flight state, result queue, response buffers, allocator overhead, traces, and downstream clients. Queue capacity should follow a burst and deadline budget, not a convenient round number.

Suppose (k) workers each sustain mean service rate μ. The inequality λ < (kμ) is necessary for long-run stability under a compatible workload, but not sufficient for a service-level objective. Variability, correlated arrivals, priority, downstream stalls, lock contention, failure retries, and utilization near one inflate tail wait. Measure distributions and test saturation.

### Budget the entire latency path

Let (W_q) be work-queue wait, (S) synchronous service, and (W_r) result-queue/dispatch wait. Then

$$
T=W_q+S+W_r+T_{network/output}
$$

for the relevant end-to-end response. A worker that reports a 20 ms database call has not met a 100 ms objective if the request waited 300 ms before starting. Record `accepted_at` and monotonic deadline in the envelope. Reject work that lacks enough estimated slack when policy supports that decision, and always discard or reconcile already-expired work before consuming a scarce dependency.

Little's Law relates measured stable averages, $L=\lambda W$. It is useful for checking observations: 800 accepted jobs/s with mean 0.25 s in the pipeline implies about 200 jobs on average. It does not bound a percentile, guarantee stability, select queue capacity, or justify admission above dependency capacity.

### Define overload explicitly

When the work queue is full, options include pausing reads or request production, disabling readiness interest until a low watermark, returning a protocol-specific overload response, rejecting before consuming a large body, shedding a documented low-priority class, or applying per-tenant admission. Every option has correctness and fairness consequences.

Do not use a blocking `put` on an event-loop thread: a full queue then stalls all handles served by that loop. “Caller runs” is also dangerous when the caller is the async layer because it executes the blocking job on the loop. Silent discard loses an accepted request. Dropping the oldest may discard the job nearest completion of its queue wait and requires an explicit terminal response/reconciliation. Prefer a nonblocking bounded offer plus a deliberate protocol outcome.

Use global and partitioned limits. A global cap protects the process; per-tenant, connection, operation, and dependency caps prevent one source from monopolizing it. Weighted fair scheduling or separate pools can protect high-importance classes, but strict priority can starve ordinary work. Record rejection reason and avoid cardinality explosions in metrics.

### Size workers against real bottlenecks

For CPU-bound work, workers near available CPU may be appropriate after measurement. For blocking work, more threads can hide wait but consume stacks, scheduler time, memory, connections, and locks. A database pool of 16 cannot be made to serve 200 simultaneous calls by creating 200 workers; it produces another queue and may hold unrelated resources while waiting.

Model worker concurrency with every downstream constraint: connection pools, file descriptors, device queues, rate limits, remote quotas, memory, and serialization locks. Separate workloads that block on different dependencies or have incompatible latency/criticality; otherwise a slow bulk export can starve authentication or health work. This is Bulkhead reasoning applied inside the synchronous layer.

Dynamic resizing is control, not magic. Scale signals lag, new workers may intensify the bottleneck, and shrinking cannot instantly stop running blocking calls. Put hard safety limits under any adaptive policy and test oscillation, cold start, dependency degradation, and recovery.

### Preserve ordering deliberately

One FIFO work queue orders dequeue, not completion. With multiple workers, job 2 can finish before job 1. A priority queue changes even dequeue order, and result publication can be reordered again. If protocol or entity semantics require order, represent it explicitly.

Options include one active job per connection/entity, partitioned queues with stable affinity, sequence numbers plus a bounded reorder buffer, optimistic version checks, or a serial executor layered over the pool. Each has head-of-line, memory, and failure consequences. Never hold a result indefinitely waiting for a missing predecessor without a deadline and recovery policy.

### Make cancellation truthful

Cancellation has at least three locations. A queued job can sometimes be marked cancelled or physically reclaimed; a claimed but not started job can check a tombstone; a running blocking call may be interruptible, cooperatively cancellable, or impossible to stop. Cancelling the future observed by the event loop often cancels only interest in the result, not the underlying call.

Keep cancellation request separate from actual worker outcome. A database write may succeed after the client disconnects. The result is stale for delivery but vital for effect reconciliation. Use stable idempotency/effect identity, conditional writes, transaction status, or compensation rather than assuming that a dropped response implies no effect.

Deadline expiry follows the same discipline. Stop queued work early; request cancellation where supported; continue to reap running results; release leases exactly once; and classify late effects. Never terminate a thread asynchronously while it can hold locks or invariants unless the platform and code have a proven cleanup contract.

### Return results without violating ownership

Workers should publish data, not manipulate async resources. In many event-loop libraries, almost all loop objects are thread-confined; use the documented thread-safe wakeup/submission primitive or a bounded multi-producer result queue plus event notification. Coalesce wakeups if safe, but never let coalescing lose terminal identities.

Bound (Q_{result}) too. If result publication blocks indefinitely while shutdown waits for workers, or if results grow without limit because the loop is busy, the architecture can deadlock or exhaust memory in the reverse direction. Reserve result capacity with accepted work, use a one-result-per-request bound, or provide a spill/reaping mechanism with explicit ownership. The loop must drain results in bounded batches so it does not starve new I/O or timers.

### Contain worker failures

Translate expected domain, timeout, dependency, and cancellation failures into typed results. Catch unexpected exceptions at the worker boundary, attach safe diagnostics, preserve terminal accounting, and decide whether the worker remains trustworthy. Do not leak stack traces, credentials, SQL, payloads, or cross-tenant data in result envelopes.

A process crash defeats in-memory terminal bookkeeping. If accepted work has durable or high-stakes effects, define a durable acceptance boundary, idempotency identity, outbox/ledger, and restart reconciliation. Half-Sync/Half-Async itself gives no exactly-once guarantee across failures.

### Design shutdown as a protocol

Shutdown proceeds in ownership order:

1. mark the async admission boundary closing and stop accepting new jobs;
2. decide per class whether queued work drains, receives an explicit cancellation result, or moves to a durable continuation system;
3. signal workers and request cooperative cancellation of eligible running calls;
4. keep the async/result path alive while workers publish terminal outcomes;
5. deliver allowed responses, discard stale ones, release every lease, and reconcile external effects;
6. after a deadline, record unresolved identities and apply the documented forced policy;
7. only then destroy worker, queue, event-loop, and connection resources in their specified order.

Queue APIs may not provide an intrinsic close operation; sentinel records, closed flags plus conditions, or executor lifecycle methods need a race-free contract. Poison records must not be mistaken for user jobs, starve behind unlimited work, or terminate all consumers when only one sees one sentinel.

### Observe the boundary

Measure accepted/rejected by reason and class; work queue depth, bytes, oldest age, and deadline slack; dequeue and service duration; worker busy/idle and dependency wait; result queue depth/age; wakeup-to-delivery delay; cancellations by stage and actual outcome; late/stale/duplicate results; per-tenant fairness; memory/lease pools; downstream saturation; and shutdown residue.

Trace timestamps at admission, enqueue, claim, service start/end, result publish, result reap, and delivery. Avoid only measuring worker function duration. Alert on oldest age and deadline slack before capacity is fully consumed. Use bounded labels: request IDs belong in traces/logs, not metric dimensions.

### Verify the architecture

Use a deterministic state model to enumerate accept, reject, cancel, claim, complete, close/reopen, duplicate, and deliver orders. Stress the real queue implementation for visibility and race safety. Inject slow workers, stuck dependencies, result-loop stalls, worker exceptions, full queues, client disconnects, deadline expiry at every boundary, and shutdown while each lifecycle state is populated.

Verify memory with large maximum payloads and allocator overhead; fairness with adversarial tenants; ordering with deliberately inverted service times; and recovery with ambiguous external effects. Use model checking or schedule control for lifecycle invariants where risk justifies it. Performance tests must report workload, distribution, hardware/runtime, pool and queue configuration, warmup, saturation, and tail latency.

### A finite executable model

The following deterministic model demonstrates bounded admission, separated worker/result envelopes, and generation validation. It deliberately simulates scheduling; it does not claim to test OS threads, memory ordering, blocking I/O, or production queue performance.

<!-- bijux-verify: {"id":"sepat-073-boundary-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"admit=r1,r2 rejected=r3 queue=2\nworker=w1 job=r1 result=ok queue=1\nclose=conn-a generation=2\nworker=w2 job=r2 result=ok queue=0\ndeliver=r1:stale,r2:delivered results=2\nbounded=True rejected=1\n","stderr":""}} -->
```python
class Boundary:
    def __init__(self, capacity):
        self.capacity = capacity
        self.jobs = []
        self.results = []
        self.generations = {"conn-a": 1, "conn-b": 1}
        self.rejected = 0

    def admit(self, job):
        if len(self.jobs) >= self.capacity:
            self.rejected += 1
            return False
        self.jobs.append(dict(job))
        return True

    def work(self, worker):
        job = self.jobs.pop(0)
        result = {
            "request": job["request"],
            "connection": job["connection"],
            "generation": job["generation"],
            "outcome": "ok",
            "worker": worker,
        }
        self.results.append(result)
        return result

    def close(self, connection):
        self.generations[connection] += 1
        return self.generations[connection]

    def deliver(self, result):
        current = self.generations[result["connection"]]
        if result["generation"] != current:
            return "stale"
        return "delivered"


boundary = Boundary(capacity=2)
r1 = {"request": "r1", "connection": "conn-a", "generation": 1}
r2 = {"request": "r2", "connection": "conn-b", "generation": 1}
r3 = {"request": "r3", "connection": "conn-a", "generation": 1}

accepted = []
for item in (r1, r2, r3):
    if boundary.admit(item):
        accepted.append(item["request"])
print(f"admit={','.join(accepted)} rejected=r3 queue={len(boundary.jobs)}")

first = boundary.work("w1")
print(f"worker=w1 job={first['request']} result={first['outcome']} queue={len(boundary.jobs)}")
generation = boundary.close("conn-a")
print(f"close=conn-a generation={generation}")
second = boundary.work("w2")
print(f"worker=w2 job={second['request']} result={second['outcome']} queue={len(boundary.jobs)}")

first_delivery = boundary.deliver(first)
second_delivery = boundary.deliver(second)
print(f"deliver=r1:{first_delivery},r2:{second_delivery} results={len(boundary.results)}")
print(f"bounded={len(boundary.jobs) <= boundary.capacity} rejected={boundary.rejected}")
```

## Definitions and Notation

Let λ denote the effective accepted arrival rate; (k) the number of synchronous workers; μ the measured mean service rate of one worker for the specified workload; (K_w,K_r) the work/result queue capacities; (L) the average jobs in a stable measured subsystem; (W) their mean residence time; (W_q) work-queue wait; (S) worker service time; and (W_r) result wait.

Let request lifecycle be

$$
created\rightarrow accepted\rightarrow queued\rightarrow claimed\rightarrow
executing\rightarrow result\_queued\rightarrow terminal.
$$

Rejection occurs before `accepted`. Cancellation and expiry are requests/observations that may occur across states; they do not erase a running external effect. `owner_generation` changes whenever a reusable connection/session owner is retired. A terminal result is **current** only if its request cell is nonterminal, its owner/generation matches, and current deadline/authority policy permits application.

The capacity vector

$$
C=(K_w,k,K_r,C_{downstream},B_{payload},Q_{tenant})
$$

must be analyzed as one system. Enlarging one component cannot raise safe throughput past the binding bottleneck and can increase retained work.

## Mechanisms, Invariants, or Proof Structure

### Safety argument

Assume admission assigns a unique request identity, records the current owner generation, and transfers an immutable/exclusive envelope only after successful enqueue. Assume each worker consumes an envelope once, publishes at most one terminal result under that identity, and never accesses async-owned mutable state. Assume the async owner serializes terminal decisions and checks identity/generation before mutation. Then a result for a retired generation cannot mutate a current owner, and two result observations cannot create two logical terminal mutations. This is a local safety argument; queue/worker/process failure requires implementation and recovery evidence.

### Boundedness argument

If (Q_{work}) capacity is (K_w), at most (k) jobs execute, (Q_{result}) capacity is (K_r), every envelope obeys owned-byte limits, and admission does not create hidden unbounded side queues, then in-memory pipeline jobs are bounded by (K_w+k+K_r) plus explicitly bounded delivery state. This does not bound runtime stacks, allocator fragmentation, connection state, dependency queues, kernel buffers, or durable continuations; include them separately.

### Liveness conditions

Progress requires available workers, terminating or time-bounded service calls, a result path that can accept/reap, and an async loop that continues dispatch. A finite queue proves no liveness. Deadlock can arise if the event loop blocks on the work queue while workers block publishing results that only that loop can drain. Avoid circular waits through nonblocking async admission, reserved/bounded result capacity, and shutdown ordering.

### Queueing limits

For stable averages Little's Law checks $L=\lambda W$. The condition λ < (kμ) expresses offered work below idealized mean service capacity; it is neither a tail-latency proof nor universally sufficient. Service dependence, nonstationarity, burst correlation, priority, failures, and downstream queues require empirical and sometimes formal analysis. Mark model assumptions explicitly.

### Verification obligations

Automated checks can validate envelope schemas, capacity configuration, state transitions, duplicate/stale suppression, exact code output, and generated workload invariants. Independent recomputation checks queueing arithmetic. Concurrency tests exercise visibility and schedules but do not prove absence of races. Line-by-line proof review must challenge uniqueness, transfer, and progress assumptions. Performance and reliability remain empirical claims tied to a declared deployment and workload.

## Alternatives and Trade-Offs

| Design | Advantage | Cost or risk | Appropriate use |
| --- | --- | --- | --- |
| Half-Sync/Half-Async | Separates async multiplexing from synchronous service reasoning | Two handoffs, queue latency, cancellation/ownership complexity | Async front end with bounded blocking/legacy work |
| Pure Reactor | Few threads and explicit nonblocking state | All service paths must remain nonblocking | Supported nonblocking dependencies and high concurrency |
| Pure Proactor | Operation processor owns async progress | Backend/lifetime/cancellation semantics | Native completion-oriented I/O |
| Thread per connection/request | Straight-line ownership and debugging | Thread/resource scale and downstream pressure | Strictly bounded loads or measured lightweight threads |
| Generic executor offload | Simple local escape from blocking | Often hides queue capacity, owner, fairness, and result semantics | Small scoped work with explicitly configured bounds |
| Active Object | Method invocations become queued requests owned by an active object | Per-object scheduling and future semantics | Encapsulating an object's concurrency policy |
| Leader/Followers | Threads rotate event-source leadership without a separate handoff pool | More complex promotion/affinity; handler may occupy follower | Event services where handoff overhead dominates |
| Process workers | Fault/CPU/runtime isolation | Serialization, IPC, deployment and crash recovery | Unsafe libraries, CPU work, isolation boundaries |
| Durable broker/workflow | Survives process failure and supports long work | Higher latency and distributed delivery semantics | Durable asynchronous jobs rather than request-lifetime work |

Large queues absorb longer bursts but retain more stale work and increase tail wait. More workers may raise concurrency while exhausting dependencies. Separate queues improve isolation but can strand capacity. Work stealing improves utilization but complicates affinity, fairness, observability, and deterministic ordering.

## Failure Modes and Misconceptions

- **“A thread pool is Half-Sync/Half-Async.”** The pattern requires explicit concurrency layers and a semantic handoff, not incidental offload.
- **“The queue can be unbounded because memory is large.”** Sustained overload converts into unbounded latency and retained state before memory finally fails.
- **“Blocking enqueue is backpressure.”** On an event loop it can freeze unrelated handles and create a result-publication deadlock.
- **“Caller-runs automatically slows producers.”** If the caller is the async dispatcher, it violates the nonblocking invariant.
- **“Thread-safe queue means the payload is thread-safe.”** Only the handoff/container synchronization is established; referenced mutable objects still need ownership.
- **“A worker can write the socket when done.”** It violates loop affinity and can target a closed/reused connection.
- **“Cancelling the future stops the database call.”** The observed future and underlying blocking/effect lifecycle can diverge.
- **“FIFO preserves responses.”** Multiple workers reorder completion; response/effect order requires explicit serialization.
- **“Expired work may run because it was accepted.”** Queue wait consumes the deadline; useless work steals current capacity.
- **“More workers fix a slow dependency.”** They may intensify connection, rate-limit, lock, memory, or scheduler contention.
- **“Only the input queue needs a bound.”** Results and output can accumulate when the event loop or peer is slow.
- **“One pool maximizes utilization.”** A slow class or tenant can starve critical work and defeat latency isolation.
- **“Service time is response time.”** Queue and result dispatch waits are often dominant under pressure.
- **“A stale result is harmless.”** Without generation/authority checks it can disclose data or mutate a new session.
- **“Shutdown can stop the loop first.”** Workers then cannot publish/reap results and leases/effects become unresolved.
- **“Completion means exactly-once effect.”** Local terminal handling does not make an external write exactly once across crash/retry.

## Worked Examples

### Example 1

**Situation.** A Reactor parses a request and calls a legacy blocking database client.

**Reasoning.** The loop creates an owned envelope with request ID, connection generation, deadline, tenant, query operation, parameters, and idempotency identity. A bounded nonblocking enqueue transfers it to a synchronous worker. The worker returns data/status through a result envelope. Only the loop schedules socket output after validating current generation.

**Conclusion.** The pattern isolates the blocking client without transferring connection ownership.

### Example 2

**Situation.** Eight workers are busy and a capacity-32 work queue is full when another request arrives.

**Reasoning.** Blocking the loop or executing the request there violates the architecture. The admission policy rejects with a documented overload response, pauses production/readiness where useful, releases payload lease, increments a bounded rejection metric, and preserves unrelated connections.

**Conclusion.** Full-queue behavior is an API and safety decision, not an implementation accident.

### Example 3

**Situation.** An unbounded executor accepts 50,000 jobs during a downstream outage; dashboards show no rejected requests.

**Reasoning.** Acceptance hid overload. Jobs retain payloads and credentials, expire before service, and make recovery worse. Replace the hidden queue with finite capacity aligned to memory/deadline budgets, cap tenants and downstream concurrency, reject or durably redirect before acceptance, and measure oldest age.

**Conclusion.** Zero rejection can mean uncontrolled queueing rather than reliability.

### Example 4

**Situation.** A service creates 100 workers for a database pool containing 12 connections.

**Reasoning.** At most 12 calls can use the dependency; other workers wait while holding job state and possibly locks. Bound database jobs at or below a measured safe pool share, separate other work, ensure acquisition consumes the request deadline, and observe pool wait separately from query time.

**Conclusion.** Worker capacity must respect the downstream bottleneck.

### Example 5

**Situation.** A client disconnects, its future is cancelled, and the blocking worker later reports that a payment authorization succeeded.

**Reasoning.** Delivery is stale, but the external effect is real or ambiguous. Record effect identity and actual outcome, reconcile transaction state, suppress response to the retired generation, and ensure retry reuses the idempotency identity. Never infer rollback from future cancellation.

**Conclusion.** Cancellation of interest and cancellation of effect are different facts.

### Example 6

**Situation.** Two requests on one session enter FIFO order, but the second worker finishes first.

**Reasoning.** If operations commute, correlate responses independently. If session semantics require order, permit one in-flight job per session or use sequence/version checks and a bounded reorder policy. A FIFO work queue alone is insufficient.

**Conclusion.** Ordering belongs to the domain contract, not the pool assumption.

### Example 7

**Situation.** A strict-priority queue continuously receives premium jobs while standard jobs wait beyond their deadlines.

**Reasoning.** Strict priority permits starvation. Use reserved capacity, weighted fair scheduling, aging, per-class pools, or explicit lower-class rejection before acceptance. Verify adversarial sustained mixes rather than average fairness.

**Conclusion.** Priority without starvation policy is not controlled service differentiation.

### Example 8

**Situation.** Workers finish quickly, but the event loop spends seconds in a logging callback and the result queue grows.

**Reasoning.** The reverse handoff is saturated. Bound result capacity, keep loop callbacks small, process results in fair batches, move logging to a safe bounded path, and track result oldest age. Reserve publication capacity so workers and shutdown cannot deadlock.

**Conclusion.** Both directions of the architecture need service and capacity budgets.

### Example 9

**Situation.** Deployment stops accepting traffic and immediately destroys the event loop while six jobs execute.

**Reasoning.** Workers lose the only safe result route. Instead keep the result owner alive, classify queued jobs by drain/cancel policy, request cooperative cancellation, reap terminal results, release leases, record ambiguous effects at deadline, then dismantle resources in dependency order.

**Conclusion.** Shutdown is a cross-layer protocol, not a pool destructor call.

### Example 10

**Situation.** A clinical gateway offloads medication-order validation to blocking workers while a clinician logs out and another user reuses the workstation session.

**Reasoning.** Envelope identity includes order, patient, authenticated principal, session generation, policy version, deadline, and audit correlation. Worker output is advisory data, not delivery authority. The loop revalidates session generation and current authorization, never sends stale patient data, and records an already-committed external effect for reconciliation. Per-tenant/patient bounds prevent resource abuse; protected logs contain identifiers, not clinical payloads.

**Conclusion.** High-stakes handoff requires current-authority validation and effect audit in addition to concurrency safety.

## Cross-Program Connections

- [Operating Systems](../../22-operating-systems/ROADMAP.md): threads, scheduling, memory visibility, descriptors, blocking calls, and cancellation implement both layers.
- [Software Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md): schedule control, saturation tests, fault injection, model-based lifecycle tests, and performance methodology verify the boundary.
- [Security Engineering](../../25-security-engineering/ROADMAP.md): tenant quotas, authority freshness, stale-result suppression, payload retention, and log hygiene constrain work transfer.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md): deadlines, idempotency, ambiguous effects, retries, and reconciliation extend beyond the in-process queue.
- [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md): overload responses, cancellation, request identity, and response ordering turn capacity into an external contract.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md): worker/dependency pools, rollout draining, telemetry, resource limits, and incident response make the pattern operable.
- [SEPAT-071](071-reactor.md) and [SEPAT-072](072-proactor.md) supply possible async layers; [SEPAT-074](../ROADMAP.md) offers an alternative leadership structure.

## References

1. Schmidt, Douglas C., and Charles D. Cranor. “Half-Sync/Half-Async: An Architectural Pattern for Efficient and Well-structured Concurrent I/O.” *Pattern Languages of Program Design 2*, Addison-Wesley, 1996. <https://www.dre.vanderbilt.edu/~schmidt/PDF/PLoP-95.pdf>. Accessed 2026-08-29.
2. Schmidt, Douglas C., Michael Stal, Hans Rohnert, and Frank Buschmann. *Pattern-Oriented Software Architecture, Volume 2: Patterns for Concurrent and Networked Objects*. Wiley, 2000.
3. Oracle. “ThreadPoolExecutor,” Java SE 17 API. Queue strategies, saturation, rejection, lifecycle, and monitoring. <https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/concurrent/ThreadPoolExecutor.html>. Accessed 2026-08-29.
4. Oracle. “BlockingQueue,” Java SE 17 API. Capacity operations, shutdown note, and memory-consistency guarantee. <https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/concurrent/BlockingQueue.html>. Accessed 2026-08-29.
5. Python Software Foundation. “Event Loop: Executing code in thread or process pools,” Python 3.14 documentation. <https://docs.python.org/3/library/asyncio-eventloop.html#executing-code-in-thread-or-process-pools>. Accessed 2026-08-29.
6. Python Software Foundation. “Developing with asyncio: Concurrency and multithreading,” Python 3.14 documentation. <https://docs.python.org/3/library/asyncio-dev.html#concurrency-and-multithreading>. Accessed 2026-08-29.
7. Boost C++ Libraries. “thread_pool,” Boost.Asio current documentation. <https://www.boost.org/doc/libs/latest/doc/html/boost_asio/reference/thread_pool.html>. Accessed 2026-08-29.
8. The Open Group. “General Information: Threads,” POSIX.1-2024. Cancellation-point semantics. <https://pubs.opengroup.org/onlinepubs/9799919799/functions/V2_chap02.html>. Accessed 2026-08-29.
9. Little, John D. C. “A Proof for the Queuing Formula: L = λW.” *Operations Research* 9, no. 3 (1961): 383–387. <https://doi.org/10.1287/opre.9.3.383>.
10. Goetz, Brian, et al. *Java Concurrency in Practice*. Addison-Wesley, 2006. Task execution, cancellation, queues, and thread-pool sizing.
11. Harchol-Balter, Mor. *Performance Modeling and Design of Computer Systems*. Cambridge University Press, 2013.
12. Gregg, Brendan. *Systems Performance*, 2nd ed. Addison-Wesley, 2020. Queueing, saturation, latency, and workload evidence.
13. Nygard, Michael T. *Release It!*, 2nd ed. Pragmatic Bookshelf, 2018. Bulkheads, timeouts, stability, and production failure modes.

Worker defaults, executor queues, cancellation, event-loop thread-safety, memory ordering, and shutdown behavior vary by language/runtime/library version. Current official specifications were checked on 2026-08-29; verify the exact deployed implementation and configuration.

## Exercises

### Exercise 1

For an event-driven document service that calls a blocking parser and database, assign every resource and action to the async, queueing, or synchronous layer. Define both envelopes and five invariants that prevent cross-layer races.

### Exercise 2

A service accepts 600 jobs/s. It has 12 workers, each sustaining 55 jobs/s for this workload. Mean pipeline residence time is 0.20 s; maximum owned payload is 64 KiB; work-queue capacity is 80. Check the necessary mean stability inequality, compute average jobs using Little's Law, compute the maximum work-queue payload bound, and state why none proves the latency objective.

### Exercise 3

Design Half-Sync/Half-Async for a multi-tenant gateway with a Reactor front end, blocking identity provider, 200 ms deadline, per-tenant fairness, connection reuse, result reordering, and a downstream pool of 24. Specify admission, capacities, ownership, cancellation, delivery, shutdown, and telemetry.

### Exercise 4

Diagnose a service whose event loop uses blocking queue insertion, default unbounded executor, 200 workers over a 20-connection database pool, mutable shared request buffers, worker socket writes, future-only cancellation, and loop-first shutdown. Give a coherent remediation and verification strategy.

### Exercise 5

Design and review a Half-Sync/Half-Async emergency-control gateway that validates and records actuator commands through a blocking certified library. Address command/authority identity, effect semantics, finite capacity and priority, ordering, deadlines/cancellation, result validation, fail-safe response, shutdown/crash recovery, security, observability, testing, and external evidence.

## Answers to the Exercises

### Answer 1

The async layer owns sockets, parser state, frame limits, current connection generation, cheap authentication/admission, timers, output buffers/readiness, and terminal delivery. It copies or leases bounded document bytes and constructs a work envelope. The queueing layer owns finite work/result queues, nonblocking offer/wakeup, capacity/fairness, visibility guarantees, and lifecycle accounting. The sync layer owns parser/database calls and worker-local state; it emits typed result data only.

The work envelope contains request, connection/generation, tenant/principal and policy reference, deadline, operation/schema, immutable payload lease, idempotency/effect identity, and trace. The result contains those correlations, typed parser/database outcome, effect evidence, safe response data, and timings. Invariants include: the loop never blocks; only the loop touches connection state; payload is immutable/exclusive until terminal release; accepted identities receive one terminal classification; both queues and bytes are bounded; worker checks expiry before dependency use; and delivery validates generation/current authority. Tests deliberately close/reuse connections, mutate original parser buffers after copy, invert completion, saturate both queues, and inject database ambiguity.

### Answer 2

Idealized mean worker capacity is

$$
k\mu=12\times55=660\text{ jobs/s},
$$

so (600<660) satisfies the necessary inequality with only about nine percent nominal headroom. Little's Law gives

$$
L=\lambda W=600\times0.20=120
$$

average jobs across the measured pipeline. Maximum payload held only in the work queue is

$$
80\times64\text{ KiB}=5120\text{ KiB}=5\text{ MiB}.
$$

The total also includes up to 12 executing payloads, result/output envelopes, connection state, dependency queues, stacks, and overhead. Means do not bound bursts or percentiles; service rates can be dependent and nonstationary; near-capacity utilization amplifies tail wait; and the 120-job observation may expose hidden queues outside the declared capacity. Measure each stage and test the target arrival/service distributions and dependency failures.

### Answer 3

The Reactor validates bounded frames and current credentials cheaply, assigns request ID and connection generation, sets a monotonic 200 ms deadline, and applies global, per-tenant, per-connection, and identity-provider admission. It nonblockingly offers immutable envelopes to tenant-aware weighted-fair queues. Capacity follows memory and useful-wait budgets and cannot permit more than the safe share of 24 downstream connections; reserve critical capacity and reject/pause before accepting excess work.

Workers check tombstone/deadline before acquiring the identity connection; acquisition and call consume remaining time. They publish result envelopes with correlation and actual dependency outcome through a bounded result path. They never hold sockets. The Reactor validates request terminal cell, connection generation, current authorization policy where required, and remaining delivery relevance. Sequence-independent results may deliver individually; session-dependent ones use one active job or a bounded sequence buffer.

Cancellation marks queued work, requests supported dependency cancellation for running work, and still reaps actual outcomes. Shutdown stops admission, explicitly cancels or drains queued jobs, keeps result dispatch alive, reconciles ambiguous identity-provider effects, releases leases, then destroys resources. Measure admission/rejection, tenant fairness, work/result depth and oldest age, deadline slack at each stage, downstream wait/call time, worker utilization, stale/late/cancel outcomes, delivery delay, memory, and shutdown residue. Verify saturation, adversarial tenants, all deadline races, disconnect/reuse, dependency stall, reordered results, full reverse queue, worker crash/exception, and rolling shutdown.

### Answer 4

Blocking insertion can freeze every connection on the loop and deadlock with workers publishing results. An unbounded executor hides overload; 200 workers contend for 20 database connections; mutable buffers race; socket writes violate affinity; future cancellation does not establish call outcome; loop-first shutdown strands results/resources.

Create explicit finite work/result queues and nonblocking admission with protocol-visible rejection or read pausing. Bound database concurrency to a measured safe pool share and isolate unrelated workloads. Copy or transfer a leased immutable payload; workers return data envelopes; only the loop generation-checks and writes. Carry monotonic deadlines through queue and connection acquisition, mark cancellation by identity, use supported cooperative dependency cancellation, and reap late/ambiguous effects with stable idempotency identity. Stop admission first, cancel/drain by policy, keep results alive, release/reconcile, then stop workers and loop.

Verify a lifecycle model plus real concurrency stress, buffer sentinels, queue-full and reverse-full tests, connection reuse, inverted completion, cancellation at queued/claimed/running/result states, database outage/recovery, worker exception, memory bound, tenant fairness, dependency-pool saturation, and shutdown/crash recovery. Report full end-to-end tails and queue age rather than database service time alone.

### Answer 5

Assign immutable command ID, actuator and control-session generation, authenticated operator/system principal, current authority/safety-policy version, monotonic sequence, deadline, idempotency/effect identity, payload classification, and audit trace. The async layer performs authenticated framing, bounds, replay/sequence checks, and admission but the certified blocking library performs validation/execution in isolated synchronous workers. No worker owns transport or current session state.

Use finite global and per-controller queues, reserved emergency capacity, starvation-bounded scheduling, maximum payload/work duration, and worker concurrency no greater than certified library/device constraints. Define overload and fail-safe action with the safety case; never improvise silent discard. Preserve command order per actuator through one active command or verified sequence/version protocol. Expired queued commands do not execute. Cancellation of a running command is advisory unless the library/device proves interruption; every actual effect is reconciled under stable identity.

Workers return typed validation/effect evidence. The async owner revalidates generation, current authority, terminal cell, sequence and safe response policy. A stale response is not delivered, but an applied actuator effect remains audit/recovery truth. Acknowledgement must distinguish accepted, validated, commanded, and confirmed physical effect. Shutdown stops admission, enters the specified safe operating state, drains/cancels by command class, keeps results/audit active, records unresolved effects, and resumes only after sequence/effect reconciliation. Crash recovery uses a protected durable command/effect ledger.

Authenticate every producer; authorize least privilege by actuator/action; protect payloads, keys, logs and traces; rate-limit principals; and make audit records tamper-evident with controlled retention. Observe queue age/slack, fairness, sequence gaps, validation and device outcome, stale/cancel/late results, resource saturation, safe-state transitions and unresolved effects. Verification includes deterministic state/model checking, certified-library contract tests, hardware-in-the-loop, overload and priority tests, race/fault/power-loss injection, adversarial security tests, clock and network failure, rolling shutdown, restart reconciliation, and safe-state drills. Production claims require named control/safety, domain, certified-library, security, reliability/operations, human-factors, and regulatory reviewers plus traceable hazard analysis and acceptance evidence.
