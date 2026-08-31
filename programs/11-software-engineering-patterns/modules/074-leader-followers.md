---
module_id: SEPAT-074
program: Software Engineering: Patterns
level: 2
module_number: 74
title: Leader-Followers
status: complete
last_verified: 2026-08-29
---

# Leader-Followers

## One-Page Review

### Governing question

How can a fixed pool of threads take turns waiting on shared event sources and processing events directly, avoiding a separate handoff queue while preserving exactly one leader, safe promotion, single-owner handle processing, bounded concurrency, and recoverable shutdown?

### Essential definitions

- A **handle** identifies an event source such as a socket, completion source, queue, or timer; a **handle set** is the set demultiplexed together.
- The **leader** is the thread currently entitled to wait on/demultiplex the next event for one handle set.
- A **follower** waits on the pool synchronizer for promotion to leader; it does not concurrently demultiplex the same handle set.
- A **processing thread** is the former leader after it selected an event, promoted continuity, and dispatched the corresponding handler.
- **promotion** is the synchronized transfer of leader entitlement to one eligible follower.
- **rejoining** returns a processing thread to leader/follower selection after its handler finishes.
- An **unbound association** permits any pool thread to process any handle; a **bound association** preserves affinity between a handle and thread or follower.
- **handle deactivation** temporarily excludes a handle/event kind from demultiplexing while its current event is processed; reactivation returns it under explicit state and generation checks.
- A **leader gap** is an interval with no thread waiting on the handle set, usually because all pool threads are processing or promotion failed.
- A **thundering herd** occurs when one event wakes many waiters that contend even though little work is available.

### Central model, mechanism, or theorem

For pool thread (t), use roles

$$
follower \rightarrow leader \rightarrow processing \rightarrow
\begin{cases}leader,&\text{if no leader exists},\\follower,&\text{otherwise.}\end{cases}
$$

For each handle set (H), enforce leader cardinality

$$
0\le |Leader(H)|\le 1,
$$

and ordinarily maintain (|Leader(H)|=1) whenever the pool is running and at least one nonprocessing thread is available. On event (e), the leader atomically claims/deactivates the relevant handle as required, promotes exactly one follower, then becomes a processing thread. After bounded handling it reactivates or retires the handle and rejoins.

With (n) pool threads and (p(t)) processing at time (t), a leader can exist only if (p(t)<n). Long/blocking handlers can consume every thread, creating a leader gap in which the operating system or upstream source queues events. Removing the application handoff queue removes its allocation and context-switch cost; it does not remove finite capacity or overload.

### Critical invariants

- For each handle set, at most one live thread owns leader entitlement at a time.
- Promotion and leader-state mutation occur under one proven synchronization protocol; spurious wakeups always recheck a predicate.
- The old leader establishes successor responsibility before entering potentially long or blocking handler work, except under a documented no-follower path.
- A handle requiring serialized service is inactive/claimed while processed; two threads cannot concurrently read, frame, or mutate its connection state.
- Handle registration, deactivation, reactivation, close, and reuse are serialized and generation-checked.
- Every thread has one explicit role and cleanup path; exception, cancellation, and timeout cannot silently strand leader entitlement.
- Pool size, per-handler blocking, downstream concurrency, kernel/backlog capacity, and admission form one bounded system.
- Priority, affinity, and scheduling policy do not permit an ineligible or lower-priority successor to violate required service guarantees.
- Shutdown stops admission and event registration, wakes followers, retires leader ownership, drains/cancels processors, and destroys synchronization only after no thread references it.
- Metrics distinguish leader wait, promotion, handler service, leader gaps, pool occupancy, handle backlog, admission, and end-to-end latency.

### Common failures

Common failures include two leaders waiting on the same unsafe demultiplexer, no leader after an exception, promoting after rather than before a blocking handler, signaling without changing a predicate, treating a condition-variable wakeup as entitlement, concurrent reads from one byte stream, reactivating a closed/reused descriptor, assuming no explicit application queue means no queueing, exhausting all threads with slow handlers, unbounded accept/connection admission, follower starvation, priority inversion, affinity that leaves work idle, holding the pool lock during I/O, recursively reentering the demultiplexer, destroying a condition variable while followers wait, and reporting handler throughput while kernel/backlog delay grows.

### Compact example

Threads `t1`, `t2`, and `t3` share two handles. `t1` starts as leader. On event `a` for `h1`, it deactivates `h1`, promotes `t2`, and processes `a`. A duplicate `h1` event is blocked while active. On event `b` for `h2`, `t2` promotes `t3` and processes `b`. When `t1` finishes, it reactivates `h1` and rejoins as follower. `t3` can then select `h1`, promote `t1`, and process event `c`. Every transition preserves one leader and one processor per handle.

### Connections

[SEPAT-071](071-reactor.md) defines readiness demultiplexing; [SEPAT-073](073-half-sync-half-async.md) contrasts a separate async-to-sync queue; [SEPAT-075](../ROADMAP.md) studies general thread-pool policy. Leader/Followers also connects to [Operating Systems](../../22-operating-systems/ROADMAP.md), [Computer Architecture](../../23-computer-architecture/ROADMAP.md), [Network Engineering](../../24-network-engineering/ROADMAP.md), [Software Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md), and [Platform Engineering](../../29-platform-engineering/ROADMAP.md).

## Governing Question

When several threads must share event sources and also perform their handlers, how should they rotate the right to wait for events so the system avoids redundant wakeups and handoff overhead without creating two leaders, losing the only leader, or processing one handle concurrently?

Leader/Followers organizes a pool around roles, not a permanent dispatcher and workers. One leader waits on a handle set. Followers wait on a separate pool synchronizer. When the leader obtains an event, it arranges for one follower to become the next leader and then handles the event itself. On completion it rejoins. The elegance is that the thread that receives the event can keep its stack, cache context, and request data through processing. The difficulty is that leader election, handle ownership, and handler duration now determine whether event demultiplexing continues.

## Why This Matters

High-throughput servers can pay for every queue object, lock, buffer transfer, context switch, and cache miss between I/O dispatch and service execution. Leader/Followers can avoid a distinct application request queue and let a preallocated thread perform an event from detection through service. It has appeared in network frameworks, object request brokers, transaction servers, and other latency-sensitive concurrent systems.

The optimization changes the correctness problem. A traditional dispatcher is a stable owner; here ownership rotates. The same pool is both the event-wait resource and processing capacity. If all threads block in handlers, nobody waits for new events. If promotion is lost, the service silently stops. If two waiters both believe they are leader on an unsafe handle set, duplicate dispatch or concurrent stream reads can corrupt state. The pattern is suitable only with a precise role protocol and validated platform semantics.

## Prerequisites and Retrieval

You should understand Reactor, thread pools, mutexes, condition variables/semaphores, event demultiplexing, socket stream semantics, scheduling, memory visibility, cancellation, deadlines, resource admission, and shutdown. Retrieve these facts:

1. A condition-variable wait must be associated with a predicate and may wake spuriously.
2. Signaling a condition variable does not transfer a mutex or prove the signaled thread ran.
3. Some event APIs permit multiple waiters safely; others duplicate wakeups, serialize internally, or impose registration constraints.
4. Concurrent reads on one byte stream can split bytes unpredictably and corrupt framing even if each syscall is thread-safe.
5. File descriptor/handle values may be reused after close; numeric equality is not lifecycle identity.
6. A handler that blocks occupies both processing capacity and one potential future leader.
7. The kernel listen queue, socket buffers, device queue, or upstream system can hold events when no user-space leader waits.
8. Thread priority, affinity, and scheduling policies affect promotion latency and priority inversion.

## Learning Objectives

After completing this module, you should be able to:

- identify handle set, event source, handler, pool, synchronizer, leader, follower, and processing roles;
- trace initial join, leader wait, event claim, follower promotion, handler dispatch, handle reactivation, and rejoin;
- specify leader uniqueness and continuity, role partition, handle serialization, generation, and terminal cleanup invariants;
- implement promotion with monitor/condition/semaphore predicates that tolerate spurious wakeups and lost-race attempts;
- distinguish unbound, bound-handle/thread, multiple-handle-set, and priority-aware variants;
- compare Leader/Followers with Reactor, Half-Sync/Half-Async, Proactor, generic thread pool, and thread-per-connection;
- analyze pool exhaustion, leader gaps, backlog growth, head-of-line effects, affinity, and priority inversion;
- integrate admission, deadlines, cancellation, exceptions, close/reuse, security, and staged shutdown;
- design observability that exposes role transitions and hidden queueing outside application memory;
- verify the state machine using invariant models, controlled schedules, stress, platform tests, overload, and failure injection.

## Core Exposition

### Identify the participants

A handle set groups sources that one demultiplexing operation can wait upon. Event handlers map ready/completed sources to application service. The thread pool owns a finite set of threads and a synchronizer protecting leader identity, eligible followers, shutdown, and sometimes priorities or affinity. The OS/runtime demultiplexer supplies event waiting and selection.

Threads move among leader, follower, and processing roles. Only the leader invokes the shared demultiplexing operation for that handle set under the pattern's base protocol. Followers are not idle generic workers consuming a job queue; they wait specifically for leader entitlement. Processing threads run handlers and later join the role protocol again.

### Join without creating two leaders

At initialization or after processing, a thread enters the pool monitor. If the pool is stopping, it follows shutdown. If there is no leader and the thread is eligible, it records itself as leader while holding the state lock, releases the lock, and waits on the event source. Otherwise it waits as a follower in a predicate loop.

The predicate is stronger than “I woke.” It may include `leader is absent`, `this thread was selected`, compatible priority, handle-set assignment, generation, and `not stopping`. Condition waits release the associated mutex atomically and reacquire it before return; implementations must still loop because wakeups can be spurious or another thread can win before this one reacquires.

Leader identity is logical entitlement, not just a thread ID stored for diagnostics. Every path that leaves leader wait—event, timeout, error, cancellation, shutdown—must update the same protected state. Avoid copying a leader token outside the monitor in a way that lets an old generation resume after reconfiguration.

### Detect, claim, promote, then process

When the leader obtains an event, it identifies the handle and handler under the event API's rules. If that handle cannot be processed concurrently, mark the relevant event kind inactive or claimed before another leader can select it. Then choose/promote an eligible follower, establish the successor's leader state, and only afterward enter handler work.

This ordering preserves event-wait continuity. If processing begins first and blocks, no follower knows it should wait on the handle set. Promotion should not hold the pool lock across handler I/O. The successor may not actually run immediately, so promotion latency remains scheduler-dependent; record it.

If no follower is available because all other threads process events, there may temporarily be no leader. The current thread cannot both block in a handler and wait on the shared event set. The OS/upstream queues events until a thread completes and becomes leader, subject to finite capacity. Some implementations may restrict what work a last thread accepts or offload exceptional long work, but that is an explicit hybrid policy.

### Deactivate shared handles correctly

With level-triggered readiness, a handle may remain ready while its handler runs. A new leader can select it again, causing concurrent reads or state mutation. Temporarily deactivate the handle/event kind, maintain one-active-handler state, or use an event API feature whose one-shot/exclusive semantics are understood and rearmed correctly.

Reactivation occurs only after the handler restores a valid state. Associate registration with `(handle, generation)` rather than the numeric handle alone. If processing closes the connection, do not rearm it. If ownership transfers or a newer generation registers the same number, an old processor cannot reactivate or deregister the new resource.

Different event kinds may have different concurrency rules. A connection might serialize reads while allowing an independently queued write completion. Protocol state, not syscall thread safety, determines safe parallelism. Encode the claim granularity explicitly.

### Preserve role and handle invariants on failure

Wrap demultiplexer return, promotion, dispatch, and cleanup in structured state transitions. An exception before promotion must either keep/recover a leader or trigger controlled pool failure. An exception after promotion means the successor exists, but the old leader must still release the handle claim and rejoin/retire. A handler exception cannot leave a handle permanently inactive without an observable quarantine policy.

Avoid asynchronous thread termination while a thread owns the leader token, pool mutex, registration mutation, or protocol state. Prefer cooperative cancellation observed at defined safe points. If a thread truly dies, a supervisor needs enough synchronized state to detect missing leadership, retire its generation, repair/quarantine handles, and promote without allowing the old thread to resume.

### Select a promotion protocol

A simple unbound protocol signals one follower; whichever eligible thread wins becomes leader. This is compact but scheduling is nondeterministic. A designated protocol records the exact successor and then signals/broadcasts; this supports priority, affinity, and testing but requires safe removal of cancelled/dead candidates and defense against a designated thread that never runs.

Semaphore-based tokens can represent available leadership but must still bind token count to actual leader state. A count greater than one can create multiple leaders; a lost token can halt the pool. Condition-variable signaling must change protected state before signaling. Broadcast can recover complex predicates but may create a herd.

For real-time or priority-sensitive service, select a follower whose scheduling priority can service the highest-priority event, use priority-inheritance/protecting synchronization where available, and analyze inversion. Promotion of a low-priority thread does not guarantee prompt leadership even if a high-priority event waits.

### Choose bound or unbound association

In an unbound pool, any leader processes the event it detected. This keeps the receive-to-handler path on one thread and balances work naturally, but thread-local state cannot imply connection identity. Application context must be explicit or safely thread-specific.

A bound handle/thread association routes a handle to a particular follower/processor. It can preserve cache, stack, library, or protocol affinity, but the leader may need an additional dispatch/promotion step. A slow bound thread can leave its handle idle while others are free. Rebinding requires generation and state transfer.

Multiple event-source variants assign different leaders/leader groups to sources that one demultiplexer cannot combine. Pool size must exceed simultaneous leader requirements if every source needs continuous coverage. This begins to resemble partitioned Reactors or staged pipelines; name and analyze the actual architecture rather than forcing the base label.

### Understand where queueing moved

Leader/Followers often removes an application work queue between a dispatcher and worker. Events can still wait in the listen backlog, socket receive buffer, completion queue, device queue, runtime registration, scheduler run queue, connection state, or remote sender. Those stores are finite and may have weaker per-tenant visibility and rejection semantics.

When (n) threads all process, there is no leader. If average accepted work approaches service capacity, leader gaps and external queues grow. Unlike a bounded application queue with explicit offer failure, overload might appear as connection refusal, packet loss, peer timeout, kernel memory, or stale readiness. Admission before expensive processing remains mandatory.

Measure backlog and oldest event age where the platform exposes them. Bound accepted connections, per-connection frames, in-flight handlers, payload bytes, dependency work, output, and tenant shares. “No allocation per handoff” is a performance property, not a capacity plan.

### Bound handler duration and blocking

The pattern's original motivation permits synchronous event handling, and processing threads can block. But each blocked handler shrinks the set able to lead. Pool size must account for the distribution of handler service, downstream concurrency, scheduling, and the minimum event-wait coverage needed.

Do not grow the pool without bound to compensate. Threads consume stacks and scheduler/lock resources, and may overload a database or remote dependency. Separate rare long tasks into a bounded Half-Sync/Half-Async or workflow stage if measurements justify the hybrid. Then make the ownership and queue boundary explicit.

Enforce monotonic deadlines through event wait, handler, dependency acquisition, response, and shutdown. A follower promotion timeout can detect liveness risk but must not create a second leader while the first successor is merely delayed. Recovery requires a generation/fencing protocol, not a timer alone.

### Control ordering and reentrancy

Per-handle deactivation can serialize handler calls, but it does not automatically order multiple handles belonging to one entity or outgoing effects. Use entity ownership, sequence/version checks, strands, or conditional state. If one handler recursively calls the pool's event loop, role counts and lock assumptions can break; forbid or explicitly support nested demultiplexing.

Level-triggered sources must be drained only within a fairness budget; draining one busy handle completely can starve others. Edge-triggered/one-shot sources require draining/rearming according to precise platform semantics or events can be lost. The pattern does not erase Reactor obligations.

### Integrate security and authority

An attacker can occupy all processors with slow requests, create repeated readiness, force expensive authentication, exploit connection admission, or target the dependency that blocks handlers. Apply bounded parsing, authentication before costly work where possible, per-principal/tenant quotas, deadlines, rate limits, payload limits, and circuit/bulkhead policies.

Thread-local identity is dangerous when threads rotate among connections. Clear/request-scope security context, locale, tracing, credentials, transactions, and sensitive buffers on every transition. A handler's authorization snapshot may expire before effect; revalidate current authority at the appropriate commit boundary. Protect role and handle identifiers without logging secrets or payloads.

### Shut down without orphaning roles

Shutdown sets a protected stopping state and stops new external admission/registration. Wake all followers so their predicate observes stopping. Interrupt or wake the leader through the documented demultiplexer mechanism; do not destroy its handle set underneath it. The leader retires its entitlement once.

Processing threads finish, cooperatively cancel, or record unresolved effects under a deadline. They do not reactivate handles into a stopped generation. Join all pool threads before destroying mutexes, conditions, registrations, or handler state. POSIX, for example, makes destruction of a mutex still referenced by waiters undefined; lifecycle ordering is part of correctness.

A rolling replacement is similar: fence the old pool generation, stop its admission, drain active handles/results, transfer only explicit resumable state, and ensure an old processor cannot rearm a handle owned by the new generation.

### Observe the role protocol

Record current leader per handle-set generation, follower and processor counts, role-transition totals, time in each role, event-wait duration, event-to-promotion and promotion-to-successor-wait latency, no-leader duration, handle-active duration, deactivation/reactivation errors, duplicate/stale events, handler/service/dependency duration, kernel/listen/completion backlog, connection admission/rejection, thread priority/affinity, and shutdown residue.

Maintain the accounting invariant (leader+followers+processors+retired=n) for known threads, with leader in `{0,1}` per group. Metrics should not require taking the hot pool lock or create unbounded labels. Put connection/request identity in sampled traces, not metric cardinality.

### Verify platform and state behavior

First model role transitions and handle claims independently of threads. Exhaustively exercise event before/after promotion, spurious follower wake, follower cancellation, no-follower state, handler error, close/reuse, simultaneous readiness, shutdown in every role, and delayed successor scheduling. Assert leader cardinality and role partition after every transition.

Then test the actual demultiplexer because multi-waiter, one-shot, exclusive, readiness, cancellation, and close semantics are platform/version/configuration specific. Use controlled barriers to widen races; thread sanitizers where supported; stress and soak; process/thread fault injection; slow/blocked dependencies; overload; priority/affinity tests; descriptor reuse; and graceful/forced shutdown. Performance comparisons must report hardware, OS, runtime, handler mix, pool size, affinity, event API, load distribution, and tails.

### A finite executable model

This deterministic model checks one-leader role rotation and per-handle exclusion. It simulates a schedule and does not execute threads, locks, condition variables, sockets, priorities, memory ordering, or OS event demultiplexing.

<!-- bijux-verify: {"id":"sepat-074-role-rotation","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"initial leader=t1 followers=t2,t3\nevent=a old=t1 new=t2 processing=t1 active=h1\nduplicate=h1 blocked=True\nevent=b old=t2 new=t3 processing=t1,t2 active=h1,h2\nfinish=t1 rejoin=follower active=h2\nevent=c old=t3 new=t1 processing=t2,t3 active=h2,h1\nfinish=t2,t3 leader=t1 followers=t2,t3 active=none\ninvariants=one_leader=True role_partition=True\n","stderr":""}} -->
```python
class LeaderFollowers:
    def __init__(self, threads):
        self.order = list(threads)
        self.roles = {thread: "follower" for thread in threads}
        self.leader = threads[0]
        self.roles[self.leader] = "leader"
        self.active = []

    def followers(self):
        return [thread for thread in self.order if self.roles[thread] == "follower"]

    def processors(self):
        return [thread for thread in self.order if self.roles[thread] == "processing"]

    def try_event(self, thread, event, handle):
        if thread != self.leader or handle in self.active:
            return None
        candidates = self.followers()
        successor = candidates[0] if candidates else None
        self.roles[thread] = "processing"
        self.leader = successor
        if successor is not None:
            self.roles[successor] = "leader"
        self.active.append(handle)
        return event, successor

    def finish(self, thread, handle):
        self.active = [item for item in self.active if item != handle]
        if self.leader is None:
            self.leader = thread
            self.roles[thread] = "leader"
        else:
            self.roles[thread] = "follower"

    def one_leader(self):
        leaders = [thread for thread in self.order if self.roles[thread] == "leader"]
        return len(leaders) == 1 and leaders[0] == self.leader

    def role_partition(self):
        allowed = ("leader", "follower", "processing")
        return all(self.roles[thread] in allowed for thread in self.order)


pool = LeaderFollowers(["t1", "t2", "t3"])
print(f"initial leader={pool.leader} followers={','.join(pool.followers())}")

event, successor = pool.try_event("t1", "a", "h1")
print(f"event={event} old=t1 new={successor} processing={','.join(pool.processors())} active={','.join(pool.active)}")
blocked = pool.try_event("t2", "duplicate", "h1") is None
print(f"duplicate=h1 blocked={blocked}")

event, successor = pool.try_event("t2", "b", "h2")
print(f"event={event} old=t2 new={successor} processing={','.join(pool.processors())} active={','.join(pool.active)}")
pool.finish("t1", "h1")
print(f"finish=t1 rejoin=follower active={','.join(pool.active)}")

event, successor = pool.try_event("t3", "c", "h1")
print(f"event={event} old=t3 new={successor} processing={','.join(pool.processors())} active={','.join(pool.active)}")
pool.finish("t2", "h2")
pool.finish("t3", "h1")
active = ",".join(pool.active) if pool.active else "none"
print(f"finish=t2,t3 leader={pool.leader} followers={','.join(pool.followers())} active={active}")
print(f"invariants=one_leader={pool.one_leader()} role_partition={pool.role_partition()}")
```

## Definitions and Notation

Let (T) be a fixed thread set of size (n); (H_g) the handle set owned by pool generation (g); (L_g\subseteq T) current leaders; (F_g) followers; (P_g) processors; and (R_g) retired/stopping threads. The role partition is

$$
T=L_g\uplus F_g\uplus P_g\uplus R_g,
\qquad |L_g|\in\{0,1\}.
$$

For serialized handle (h), `active(h,g)` means exactly one processor in pool generation (g) owns its current handler claim. Registration identity is `(handle_value, handle_generation, pool_generation, event_kind)`.

Let (G(t)) be leader-gap indicator, equal to 1 when the pool runs but no leader waits; τₚ promotion latency; (S_h) handler service time; (B) externally queued/backlogged events; and (C_d) downstream concurrency. These are measured quantities, not universal constants.

## Mechanisms, Invariants, or Proof Structure

### Leader-uniqueness argument

Assume one monitor protects `leader`, pool generation, eligibility and role changes. A thread becomes leader only while holding that monitor after observing no current leader or an explicit designation to itself. It records the new state before release; all awakened followers loop on the predicate. By mutual exclusion, two transitions cannot both observe and install leadership for the same generation. This proves only the abstract protocol if the monitor implementation and every mutation path obey the assumptions.

### Continuity argument

If a leader detects an event, an eligible follower exists, promotion records exactly one successor before the old leader blocks/processes, and the scheduler eventually runs the successor, then handle-set waiting resumes. If any premise fails—no follower, lost state change, successor death/starvation, demultiplexer error—continuity is not guaranteed. A watchdog can detect a gap but needs fencing to repair it safely.

### Per-handle safety argument

Assume event selection atomically establishes `active(h,g)` before a successor can select the same serialized event kind; only its owning processor may mutate the handler state; and close/reactivation compares handle and pool generations. Then concurrent same-handle processing and stale reactivation are excluded in the modeled path. This does not prove OS close/read/write behavior or multi-process ownership.

### Capacity argument

At most (n) handlers execute, but if all (n) process, no leader remains. The application has bounded processor concurrency; external event storage is bounded only by separately verified listen/socket/device/completion/upstream capacities. The absence of an application work queue therefore cannot establish bounded end-to-end backlog.

### Review categories

Automated state exploration can check role cardinality, partition, allowed transitions and handle claims for a finite model. Schedule-controlled integration tests can reproduce races but not prove all schedules. Platform tests establish observed demultiplexer behavior only for declared versions/configurations. Performance, fairness, priority and cache claims are empirical. Proof review must examine monitor, promotion, failure, generation and liveness assumptions line by line.

## Alternatives and Trade-Offs

| Design | Advantage | Cost or limitation | Best fit |
| --- | --- | --- | --- |
| Leader/Followers | Direct event-to-handler path, reused threads/stacks, no separate work handoff | Complex rotating ownership; all processors can leave no leader | Bounded handlers over a shared event set |
| Single-thread Reactor | Simple event ownership and ordering | One handler thread; blocking stalls all | Fully nonblocking bounded handlers |
| Multi-Reactor/partitioned loops | Stable per-partition ownership and scale | Rebalancing, cross-loop coordination | Connection-affine event systems |
| Half-Sync/Half-Async | Explicit bounded async/sync boundary and isolation | Queue/data transfer/context switch | Blocking/long service behind responsive I/O |
| Proactor | Operation processor reports completions | Buffer/cancellation/backend semantics | Native async completion operations |
| Generic bounded thread pool | Familiar task submission and explicit queue | Extra handoff; not an event-wait protocol | Independent submitted tasks |
| Thread per connection | Straight-line affinity and lifecycle | Thread/scheduler/resource scale | Strictly bounded connections or validated lightweight threads |
| Bound handle/thread Leader/Followers | Cache/library/protocol affinity | Imbalance and rebinding complexity | Strong thread-affine resources |
| Multiple leader groups | Covers incompatible event sources | More threads, coordination and partition sizing | Sources that cannot share a demultiplexer |

The pattern can reduce allocation, synchronization, and context switches compared with a separate handoff, but those are workload- and implementation-dependent empirical claims. Rotating a leader itself can require scheduling/context switching. Optimize only after a correct baseline and representative measurements.

## Failure Modes and Misconceptions

- **“Leader means permanent dispatcher.”** Leadership rotates; the former leader normally processes the event.
- **“All pool threads wait on the I/O source.”** Followers wait on the pool protocol; one leader waits on a shared handle set in the base form.
- **“A signal makes the receiver leader.”** The protected predicate/designation grants entitlement, not wakeup alone.
- **“Condition waits wake only when signaled.”** Spurious wakeups are permitted; loop on state.
- **“Promote after processing.”** A long handler then creates an avoidable leader gap.
- **“Two waiters improve availability.”** On an incompatible demultiplexer they can duplicate dispatch or race on one handle.
- **“Thread-safe reads preserve protocol frames.”** Concurrent stream reads can divide bytes and corrupt parser ownership.
- **“No user queue means no backlog.”** Events wait in kernel, device, runtime, scheduler, peer, or connection buffers.
- **“Fixed threads imply bounded memory.”** Connections, payloads, output and external queues can remain unbounded.
- **“Blocked processors do not affect I/O.”** Every blocked processor reduces possible leaders/followers.
- **“Timeout permits a second leader.”** A delayed leader may still run; recovery requires generation fencing.
- **“Affinity always improves cache use.”** It can strand capacity and worsen tails under skew.
- **“Reactivation by descriptor number is safe.”** Close/reuse needs lifecycle generation.
- **“One leader guarantees per-entity ordering.”** Concurrent processors on related handles still need domain serialization.
- **“Handler exception only fails one request.”** It may strand a claim or role unless cleanup repairs state.
- **“Stop means destroy synchronization.”** Waiters/processors must exit and join before owned primitives are destroyed.

## Worked Examples

### Example 1

**Situation.** Three server threads initialize against one shared readiness set.

**Reasoning.** Under the pool monitor, the first eligible joiner records itself leader. The other two enter a predicate loop as followers. Only the leader calls the demultiplexer; role accounting is one leader, two followers, zero processors.

**Conclusion.** Initial join uses the same synchronized entitlement rule as later rejoin.

### Example 2

**Situation.** The leader selects a request and begins a 500 ms database call before promoting anyone.

**Reasoning.** No thread waits for new events during that interval even though followers exist. Promote/record one successor before the blocking call, or use a different architecture if handler setup cannot safely release event ownership first. Measure promotion-to-wait latency.

**Conclusion.** Promotion ordering is a liveness property.

### Example 3

**Situation.** A condition-variable broadcast wakes four followers and two proceed without rechecking leader state.

**Reasoning.** Both may call the shared demultiplexer as leaders. Protect leader identity with one mutex, assign/update while locked, and wait in a loop checking generation, designation and stopping. Broadcast is a wake mechanism, not election.

**Conclusion.** Mutual exclusion plus predicates, not notification count, enforces leader uniqueness.

### Example 4

**Situation.** A level-triggered socket remains readable while its first handler parses a frame; the new leader selects it again.

**Reasoning.** Concurrent reads can split the byte stream and mutate one parser. Deactivate/one-shot claim the read event before promotion makes reselection possible; process within fairness/byte limits; rearm only the current live generation after parser state is coherent.

**Conclusion.** Same-handle exclusion is separate from leader exclusion.

### Example 5

**Situation.** Every thread blocks waiting for a slow identity provider.

**Reasoning.** The pool has no follower to promote and therefore no leader. New arrivals accumulate externally and time out. Bound dependency concurrency, use deadlines/circuit breaking/admission, reserve event coverage where justified, or isolate long work behind a bounded Half-Sync/Half-Async stage.

**Conclusion.** Pool exhaustion converts processing delay into event-wait outage.

### Example 6

**Situation.** A connection closes during processing; the OS reuses its descriptor for a new tenant before the old handler rearms it.

**Reasoning.** Numeric descriptor checks pass incorrectly. Registration and handler claim carry connection and pool generation; close retires the old generation. Old cleanup can release its own resources but cannot rearm/deregister or deliver into the new owner.

**Conclusion.** Generation fencing prevents stale handle mutation and cross-tenant disclosure.

### Example 7

**Situation.** A bound handle/thread variant gives one thread all hot connections while two peers remain mostly idle.

**Reasoning.** Affinity improved locality but created imbalance. Measure per-thread queue/service/leader availability; rebalance only at safe state-transfer boundaries, use less rigid partitioning, or choose unbound processing where thread affinity is not a contract.

**Conclusion.** Affinity trades locality for scheduling flexibility.

### Example 8

**Situation.** A high-priority event arrives, but the promoted successor is a low-priority thread preempted by medium-priority work.

**Reasoning.** A logical leader exists but cannot run, so service stalls through priority inversion. Use priority-aware successor selection, suitable synchronization protocol, OS real-time analysis where applicable, and measured worst-case promotion—not ordinary priority labels alone.

**Conclusion.** Leader existence and timely leadership are different properties.

### Example 9

**Situation.** Shutdown broadcasts followers and destroys the condition variable while a processing thread is about to rejoin.

**Reasoning.** The late thread can reference destroyed synchronization. Set stopping under the monitor, fence the generation, wake leader/followers, prevent reactivation/rejoin into service, wait for processors and join all threads, then destroy pool resources.

**Conclusion.** Destruction follows proof of role quiescence.

### Example 10

**Situation.** An air-traffic telemetry gateway uses Leader/Followers to receive and validate signed position updates.

**Reasoning.** Each aircraft/session has generation, sequence, deadline, authenticated identity and bounded parser state. Read handling is serialized per stream; promotion happens before bounded validation; cryptographic/dependency work cannot consume every event thread without an analyzed reserve/hybrid boundary. Stale results never update a reused session; overload and gaps trigger defined operational responses. Safety claims require hardware/network fault tests and named domain review.

**Conclusion.** Efficient role rotation does not replace identity, capacity, security, recovery, or safety evidence.

## Cross-Program Connections

- [Operating Systems](../../22-operating-systems/ROADMAP.md): mutex/condition semantics, scheduling, cancellation, descriptors and event APIs implement the role protocol.
- [Computer Architecture](../../23-computer-architecture/ROADMAP.md): cache affinity, migration, false sharing and memory ordering influence measured costs.
- [Network Engineering](../../24-network-engineering/ROADMAP.md): accept backlogs, stream framing, readiness modes, flow control, close and descriptor reuse shape handle behavior.
- [Software Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md): controlled schedules, state models, race tools, overload, soak and fault injection verify invariants.
- [Security Engineering](../../25-security-engineering/ROADMAP.md): connection admission, slow-request exhaustion, per-principal quotas, context clearing and stale-generation checks constrain attacks.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md): CPU affinity, thread priority, rolling drain, backlog metrics, resource limits and incident recovery operationalize the pool.
- [SEPAT-071](071-reactor.md) defines the event participant; [SEPAT-073](073-half-sync-half-async.md) contrasts queued handoff; [SEPAT-075](../ROADMAP.md) generalizes worker-pool policies.

## References

1. Schmidt, Douglas C., Carlos O'Ryan, Michael Kircher, and Irfan Pyarali. “Leader/Followers: A Design Pattern for Efficient Multi-threaded I/O Demultiplexing and Dispatching.” *PLoP 2000*. <https://www.dre.vanderbilt.edu/~schmidt/PDF/lf.pdf>. Accessed 2026-08-29.
2. Schmidt, Douglas C., Michael Stal, Hans Rohnert, and Frank Buschmann. *Pattern-Oriented Software Architecture, Volume 2: Patterns for Concurrent and Networked Objects*. Wiley, 2000.
3. Schmidt, Douglas C. “Reactor: An Object Behavioral Pattern for Demultiplexing and Dispatching Handles for Synchronous Events.” <https://www.dre.vanderbilt.edu/~schmidt/PDF/reactor-siemens.pdf>. Accessed 2026-08-29.
4. The Open Group. “pthread_cond_clockwait, pthread_cond_timedwait, pthread_cond_wait,” POSIX.1-2024. Predicate, mutex, cancellation and wake semantics. <https://pubs.opengroup.org/onlinepubs/9799919799/functions/pthread_cond_clockwait.html>. Accessed 2026-08-29.
5. The Open Group. “pthread_mutex_destroy, pthread_mutex_init,” POSIX.1-2024. Synchronization lifecycle. <https://pubs.opengroup.org/onlinepubs/9799919799/functions/pthread_mutex_destroy.html>. Accessed 2026-08-29.
6. Kerrisk, Michael. “epoll(7).” Linux manual page. Readiness, edge/level triggering and multiple-waiter behavior. <https://man7.org/linux/man-pages/man7/epoll.7.html>. Accessed 2026-08-29.
7. Kerrisk, Michael. “select(2).” Linux manual page. Descriptor sets, readiness and limitations. <https://man7.org/linux/man-pages/man2/select.2.html>. Accessed 2026-08-29.
8. IETF. *RFC 9293: Transmission Control Protocol (TCP)*. August 2022. <https://www.rfc-editor.org/rfc/rfc9293>.
9. Stevens, W. Richard, Bill Fenner, and Andrew M. Rudoff. *UNIX Network Programming, Volume 1*, 3rd ed. Addison-Wesley, 2003.
10. Goetz, Brian, et al. *Java Concurrency in Practice*. Addison-Wesley, 2006. Condition queues, task execution, cancellation and liveness.
11. Herlihy, Maurice, and Nir Shavit. *The Art of Multiprocessor Programming*, revised 1st ed. Morgan Kaufmann, 2012. Synchronization and concurrent reasoning.
12. Gregg, Brendan. *Systems Performance*, 2nd ed. Addison-Wesley, 2020. Scheduling, queues, utilization, saturation and latency evidence.

Demultiplexer multi-wait behavior, exclusive/one-shot readiness, condition variables, thread cancellation, priority, affinity, descriptor close/reuse and shutdown vary by OS/runtime/library version. Current official specifications were checked on 2026-08-29; validate exact deployed behavior.

## Exercises

### Exercise 1

Draw the participants and state transitions for four unbound threads sharing one readiness set. Specify leader, role-partition, promotion, handle-claim, generation and cleanup invariants.

### Exercise 2

A pool has (n=6) threads. At one instant five handlers block and the leader selects an event. Explain the possible role transition, what happens if the handler also blocks, where later events wait, and what evidence is needed to choose a safer capacity/architecture. Do not infer an arrival-rate result from thread count alone.

### Exercise 3

Design a priority-aware Leader/Followers server for two handle sets that cannot share one demultiplexer. Include leader groups, pool sizing, follower promotion, same-handle exclusion, affinity, deadlines, admission, priority inversion, overload and observability.

### Exercise 4

Diagnose an implementation that broadcasts without a predicate, lets two leaders call `select`, processes before promotion, never deactivates readable streams, blocks on a database from every thread, rearms by descriptor number, and destroys its monitor before processors exit. Provide a correction and test plan.

### Exercise 5

Design a Leader/Followers command gateway for a safety-critical rail-control system. Address identity/generation, authenticated authority, ordering, event and handler bounds, promotion failure, priorities, effect semantics, shutdown/restart, security, observability, verification and required external review.

## Answers to the Exercises

### Answer 1

Participants are one handle set/demultiplexer, registered handles and concrete handlers, a four-thread pool, and a monitor/condition protecting role state. Initially one thread records leader and enters event wait; three followers wait on the pool predicate. On an event, the leader atomically claims/deactivates the serialized handle, records/designates one follower as successor, signals it, becomes processor, dispatches, cleans/reactivates the current generation, then under the monitor becomes leader if none exists or follower otherwise.

Invariants are: at most one leader for the handle-set generation; four threads partition exactly among leader/follower/processor/retired; every wake rechecks eligibility/designation/stopping; promotion state changes under the same mutex; a serialized `(handle,generation,event_kind)` has at most one processor; only the owning processor cleans its claim; old generations cannot rearm current handles; exception/cancellation/shutdown releases or quarantines claims and cannot silently lose leadership; and synchronization is destroyed only after all roles retire. A state model should assert these after every transition.

### Answer 2

With five processors and one leader, no follower exists. When the leader selects the event it can process it, leaving zero leaders and six processors, or apply a documented last-thread policy. If it blocks, nobody waits in user space until some earlier processor finishes and rejoins as leader. Later events can accumulate in listen/socket/device/completion/runtime/upstream queues, be refused/dropped, or time out according to finite platform/protocol capacity. The application has no spare event-wait coverage.

Thread count alone gives neither arrival rate nor service capacity. Measure distributions of event arrivals, handler and dependency service, blocking overlap/correlation, leader-gap frequency/duration, promotion scheduling, backlog and oldest age, admission/rejection, downstream pools, deadlines, CPU/memory and failure behavior. Test representative bursts and dependency stalls. Remedies may include stricter admission/deadlines, bounded dependency concurrency/circuit breaking, more threads within proven resource limits, reserving event coverage, partitioning workloads, or moving long work to a bounded Half-Sync/Half-Async/durable stage.

### Answer 3

Create one leader entitlement per handle-set generation, so continuous coverage needs at least two leader-capable threads before any processing capacity. Either partition followers/processors by source for strong isolation or maintain a shared eligible pool with explicit designation; analyze the latter's atomic cross-group role accounting. Size above required leaders plus measured concurrent bounded handlers, but below CPU, stack, descriptor and downstream limits.

Promotion records a designated eligible successor under the monitor before processing. Choose by event/service priority, affinity and aging while preventing starvation; use suitable OS priority/inheritance controls and measure promotion-to-run worst cases. Deactivate/one-shot claim serialized handles with handle/pool generations. Bound handler time/dependency acquisition and never let affinity rearm a stale handle. Per-source/tenant admission, backlog and payload limits define overload; if a group lacks a follower, events wait only within verified external limits or receive protocol fail-safe handling.

Observe leader per group, eligible followers, processors by priority/source, role/promotion latencies, gaps, handle-active age, backlog, deadline slack, affinity imbalance, inversion indicators, downstream saturation and rejection. Verify state-machine cardinality across both groups; spurious/broadcast wakeups; simultaneous events; designated follower delay/death; priority mixes/starvation; handle close/reuse; dependency stalls; saturation; shutdown in all roles; and exact platform multi-wait semantics.

### Answer 4

Broadcast without protected predicates permits multiple followers to infer leadership; two `select` callers may duplicate readiness and race. Processing before promotion creates gaps. Undeactivated readable streams can be processed concurrently and corrupt framing. Database blocking consumes every leader candidate. Numeric rearm can target a reused connection. Early monitor destruction lets late rejoin touch invalid synchronization.

Use one monitor-protected leader/generation/designation state and follower predicate loop; permit only the current leader to demultiplex. Claim/deactivate the selected stream before making it visible to the successor, designate/signal one follower before handler work, and rearm only live matching generations. Bound/deadline database concurrency, circuit-break failures, admit within capacity, and isolate long work behind an explicit bounded queue if needed. Shutdown sets stopping, fences registrations, wakes leader/followers, drains/cancels processors and joins them before destruction.

Build a finite role/claim model, then controlled real-thread schedules for spurious/broadcast wake, simultaneous join/promotion, event/error/timeout paths, no-follower state, handler exception, descriptor close/reuse and shutdown at each point. Run race/thread sanitizers, actual platform event tests, stream framing sentinels, database stall/recovery, backlog overload, priority/affinity, soak, forced thread/process failure and restart reconciliation. Assert leader cardinality, role partition, one handler per generation, no stale rearm, bounded resources and zero unaccounted shutdown work.

### Answer 5

Every command carries immutable command ID, train/track/controller/session and pool generations, authenticated principal/system identity, current authority/safety-policy version, monotonic sequence, deadline, effect/idempotency identity, classification and audit correlation. One serialized claim per control stream prevents concurrent parsing; entity sequence/version rules order effects across handles. The leader promotes a qualified successor before bounded validation/dispatch, and an old generation cannot rearm or acknowledge a current controller.

Reserve analyzed high-criticality leader/processor capacity without allowing ordinary starvation to become invisible; enforce authenticated admission, global/source/principal limits, maximum frame and handler work, dependency/device concurrency, deadlines and circuit/fail-safe behavior. A promotion watchdog observes gaps but creates a replacement only through fenced generation consensus within the process. If all safe processors are occupied, follow the hazard-approved overload/safe-state policy rather than silently queueing beyond verified kernel/backlog limits.

Distinguish received, authenticated, validated, issued, device-accepted and confirmed physical effect. Cancellation/connection loss cannot erase an issued command; reconcile via stable identity and protected durable command/effect ledger. Shutdown stops admission, enters defined safe operation, wakes and retires leader/followers, drains/cancels processors by command class, prevents old rearm, records unresolved effects, joins threads, and reconciles before restart.

Use mutual authentication, least privilege, replay/sequence defense, protected keys, payload and audit records, thread-context clearing, quotas and tamper evidence. Observe every role/gap/promotion, handle generation/active age, priority/inversion, command stage/deadline, backlog/rejection, effect outcome, safe-state transition and residue. Verification requires model checking of roles/order, platform concurrency tests, race/fault/overload and adversarial security testing, hardware-in-the-loop, scheduler/priority worst-case analysis, power/network/process failures, safe-state and recovery drills. Production claims require named rail-control/safety, signaling/domain, concurrency/platform, security, reliability/operations, human-factors and regulatory reviewers with traceable hazards and acceptance evidence.
