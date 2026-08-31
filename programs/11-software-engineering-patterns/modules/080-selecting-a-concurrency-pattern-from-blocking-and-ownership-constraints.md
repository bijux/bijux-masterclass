---
module_id: SEPAT-080
program: Software Engineering: Patterns
level: 2
module_number: 80
title: Selecting a Concurrency Pattern from Blocking and Ownership Constraints
status: complete
last_verified: 2026-08-29
---

# Selecting a Concurrency Pattern from Blocking and Ownership Constraints

## One-Page Review

### Governing question

Given concrete ownership, I/O, blocking, ordering, dependency, capacity, cancellation, effect, lifecycle, and evidence constraints, which concurrency pattern—or smallest explicit composition—fits without hiding overload or creating unsafe shared state?

### Essential definitions

- An **ownership domain** is the thread, loop, object, partition, process, or protocol exclusively entitled to mutate state/resources.
- A **blocking map** classifies every call as bounded CPU, potentially blocking, asynchronous initiation, readiness operation, completion handling, foreign callback, or unknown.
- An **event model** is readiness (handler attempts I/O), completion (operation result arrives), submitted task, state-guarded method request, or stream item/demand.
- A **capacity vector** lists all finite counts/bytes/concurrency: connections, outstanding operations, queue entries, threads, buffers, dependencies, results, tenants, retries, and deadlines.
- A **wait-for graph** records which execution/resource owner waits for which other owner; cycles and exhausted resources reveal deadlock/starvation.
- An **ordering domain** identifies the smallest key requiring serialized observation/effect: connection, entity, partition, stream, or none.
- A **linearization/effect contract** distinguishes local state decision, result completion, remote/durable effect, and acknowledgement.
- A **pattern composition seam** is an explicit ownership transfer with bounded queue/result/cancellation/shutdown semantics.
- A **selection claim** is conditional on workload, platform, dependency and evidence; a pattern name alone proves nothing.
- **review required** is the correct outcome when constraints are unknown/conflicting; inventing a catch-all architecture is not selection.

### Central model, mechanism, or theorem

Select from constraints in this order:

$$
ownership\rightarrow event/blocking\rightarrow ordering\rightarrow capacity/dependencies
\rightarrow cancellation/effects\rightarrow lifecycle\rightarrow evidence.
$$

First choose where mutable state lives. Then keep potentially blocking work out of an owner that must make multiplexed progress. Introduce a queue/worker boundary only when the blocking map requires it and bound both directions. For a pipeline with accepted rate λ and stage capacities μᵢ, sustainable throughput is limited by

$$
\mu_{pipeline}\le \min_i\mu_i,
$$

so adding concurrency before a slower dependency cannot make the system stable. Every candidate must satisfy safety invariants, absence/management of wait cycles, finite resource bounds and terminal shutdown/effect accounting before performance comparison.

### Critical invariants

- Every mutable resource has one explicit synchronization/ownership policy; no pattern seam leaves ambiguous mutation authority.
- No event loop, completion dispatcher, active-object scheduler, or sole leader blocks on unbounded/foreign work.
- Every queue, outstanding set, worker/dependency pool, payload/result buffer and tenant share is finite with a full policy.
- Event semantics match the backend: readiness is not completion; executor offload is not native asynchronous I/O.
- Required ordering is represented by affinity/serialization/sequence/version at the smallest correct domain.
- Futures/callbacks/results never execute unknown blocking work in an ownership-critical thread by accident.
- Cancellation/deadline state is separate from computation and external effect; late outcomes are reaped/reconciled.
- Cross-pattern wait/resource graph is acyclic or has a proven progress/timeout/recovery protocol.
- Shutdown follows ownership dependencies, stops admission first, drains/cancels/reaps, fences generations, and destroys last.
- The chosen design has falsifiable verification obligations and documents platform/workload assumptions and unsupported guarantees.

### Common failures

Common failures include choosing async because it sounds scalable, one thread per connection without connection bounds, Reactor handlers calling blocking databases, Proactor code reusing buffers before completion, a Thread Pool with unbounded queue, Active Object servant doing long I/O, Monitor Object callbacks under lock, Leader/Followers with every thread blocked, a Future mistaken for execution/backpressure, bounded queue inserted at every edge without end-to-end ownership, thread pool larger than dependency pool, cross-pool future cycles, global serialization for per-key ordering, cancellation assumed to undo effects, and benchmarking only the happy path before proving lifecycle safety.

### Compact example

A gateway owns 50,000 sockets on a readiness loop, parses small frames, calls a blocking legacy identity library backed by 32 connections, and returns per-connection ordered results. The fit is Reactor for socket ownership plus Half-Sync/Half-Async at one bounded seam: immutable generation-qualified requests enter a queue whose worker concurrency is at most the safe dependency share; results return to the loop for generation/order validation. A pure Reactor would block; 50,000 threads waste resources; a generic unbounded executor hides overload; a Proactor label does not change readiness or library semantics.

### Connections

[SEPAT-071](071-reactor.md) through [SEPAT-079](079-producer-consumer-with-bounded-buffers.md) provide the candidate vocabulary. The selection method also connects to [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md), [Software Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md), [Operating Systems](../../22-operating-systems/ROADMAP.md), [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md), and [Platform Engineering](../../29-platform-engineering/ROADMAP.md).

## Governing Question

When several concurrency patterns could make a design “work,” which constraints determine the smallest architecture that remains correct under overload, cancellation, failure and shutdown on the deployed platform?

Concurrency patterns are responsibility assignments. Reactor assigns readiness progression to handlers; Proactor assigns operation progress to an asynchronous processor; Monitor Object borrows caller threads under a lock; Active Object owns servant execution; Thread Pool schedules independent work; Half-Sync/Half-Async connects concurrency models; Leader/Followers rotates event leadership; Producer-Consumer buffers stages; Future/Promise communicates one result. Selection begins with the problem's actual ownership and blocking, not preferred syntax.

## Why This Matters

Wrong pattern selection often passes functional tests. It fails when a database slows, a queue fills, completion arrives after close, one tenant monopolizes workers, shutdown races effects, or a callback runs on a completion thread. Adding more patterns can deepen the failure by multiplying queues and hidden executors.

A disciplined selection method creates a reviewable constraint model and tests alternatives against it. It also reveals when no local concurrency pattern solves the real problem—for example durable work across process failure needs a persistent workflow/broker, and hard real-time safety needs scheduling/hardware evidence beyond object patterns.

## Prerequisites and Retrieval

You should be able to explain Reactor, Proactor, Half-Sync/Half-Async, Leader/Followers, Thread Pool, Active Object, Monitor Object, Future/Promise and bounded Producer-Consumer. Retrieve these distinctions:

1. Reactor reports readiness; Proactor reports operation completion.
2. Monitor Object executes on caller threads; Active Object schedules requests in another control domain.
3. Thread Pool bounds active workers only if queue/payload/dependency/results are also bounded.
4. Half-Sync/Half-Async explicitly crosses async and blocking layers through queues.
5. Leader/Followers avoids a separate handoff but loses a leader if all pool threads process/block.
6. Future/Promise represents a result and supplies no backpressure by itself.
7. Producer-Consumer work sharing is not broadcast and finite buffers force a full policy.
8. No in-memory pattern provides durable acceptance/exactly-once external effect across process failure.

## Learning Objectives

After completing this module, you should be able to:

- build ownership, blocking, event, ordering, capacity, wait-for, lifecycle and effect models before choosing;
- reject candidate patterns whose core assumptions conflict with known constraints;
- select a minimal primary pattern and introduce explicit compositions only at real ownership/blocking seams;
- distinguish API syntax (`async`, futures, executors) from backend concurrency architecture;
- size capacity against bottleneck/dependency and useful deadlines rather than upstream concurrency;
- design ordering, cancellation, stale-generation, result context and shutdown across seams;
- compare safety, liveness, performance, operability, portability and team complexity separately;
- write falsifiable design claims and a verification matrix for each candidate;
- revisit selection when platform/backend/workload evidence contradicts assumptions;
- identify when durability, isolation, real-time or regulatory requirements demand architecture beyond these patterns.

## Core Exposition

### Start with an ownership table

Inventory mutable resources: connection/handle, parser, session, domain entity, cache, buffer, database client, file/device, queue, result and metrics state. For each, name owner, allowed mutators, lifecycle generation, synchronization, transfer mechanism and release condition.

| Resource | Owner candidates | Questions |
| --- | --- | --- |
| Socket/handle | Reactor/Proactor loop, leader pool, bound thread | Who reads/writes/closes/rearms; can numeric handle be reused? |
| Domain aggregate | Monitor, Active Object, partition/actor | Synchronous or asynchronous calls; guards/order; external effects? |
| Work item/buffer | Queue then worker/operation | Copy/lease; bytes; terminal release; cancel race? |
| Dependency client | Worker pool/limiter | Thread-safe/affine; max concurrency; blocks/cancels? |
| Future/result | Completer then observers | Completion authority/context; late/stale delivery; retention? |

If two patterns both believe they own a socket or servant, the design is already wrong. Composition transfers immutable/exclusive envelopes, not live mutable owners.

### Build the blocking map

For every call in each execution context, classify worst-case behavior from official contract and deployed backend: bounded CPU, lock wait, blocking syscall/library, readiness nonblocking operation, native completion initiation, executor-backed pseudo-async, callback/continuation, or unknown. Treat unknown as potentially blocking until measured/documented.

Mark contexts that must never block: GUI/event loop, completion reaper, Active Object scheduler serving latency-critical state, Leader thread, real-time control thread. Any potentially blocking edge out of such a context requires redesign, bounded offload or a proven very short operation.

Do not infer from `await`: the awaited library may use a hidden thread pool, synchronous DNS, lock, or callback. Conversely, blocking syntax on lightweight threads may be operationally acceptable, but dependencies and state ownership remain finite.

### Identify the event model

If the OS says a handle is ready and application must attempt/advance I/O, Reactor fits. If application submits an operation and later receives its actual result, Proactor fits. A cross-platform facade may use either readiness or blocking workers underneath; qualify each backend.

If work is independent submitted functions, Thread Pool is likely. If calls target one sequential stateful object with async results/guards, Active Object. If caller threads synchronously enter short protected methods and wait on state predicates, Monitor Object. If a sequence of items crosses rate-mismatched stages, bounded Producer-Consumer.

Leader/Followers fits when multiple preallocated threads can rotate waiting on shared event sources and handle events directly, handlers are bounded enough to retain leadership capacity, and the platform supports the demultiplexing protocol. It is not a generic load balancer.

### Choose state ownership before execution capacity

Independent stateless tasks can share a pool. Stateful operations need an ordering owner. Putting entity mutations in a generic pool plus locks often reconstructs a Monitor; per-entity serialization/mailbox reconstructs Active Object/actor. Name the actual policy.

Use Monitor Object for short synchronous atomic operations where callers may block and state/conditions are local. Avoid foreign I/O/callbacks under lock. Use Active Object when callers should decouple, guards/queueing matter, and one control domain can own sequential servant state; split long external work into continuations.

Thread confinement/partitioned event loops can own many entities without one thread each. Pattern vocabulary can compose, but every object needs one active mutation token and finite mailbox.

### Decide whether a concurrency-model seam is needed

An async front end plus unavoidable blocking service is the core Half-Sync/Half-Async case. The async layer owns I/O; a finite work queue and sync workers own blocking service; a finite result path returns immutable results. Worker count respects dependency capacity. The loop validates current generation before delivery.

Do not offload every small function. Handoffs add queue wait, copies/leases, cancellation/reordering and shutdown complexity. Keep bounded CPU parsing on the owner if fairness budget permits; offload only measured/blocking/isolated work.

For long durable work, the seam may be an outbox/broker/workflow rather than in-memory Half-Sync. State the new distributed semantics.

### Model ordering domains

Ask what must be ordered: bytes on a connection, requests for one entity, operations for one account, records in one partition, or all work. Use the smallest domain. Reactor/Active Object/Monitor naturally serialize an owner; thread pools and MPMC queues do not preserve completion order.

Options include affinity/strand, one in-flight per key, partitioned queue, sequence/version conditional mutation, bounded reorder buffer or commutative operations. Global locks/one thread provide simple correctness at possible throughput cost; choose after identifying actual domain, not by default.

Ordering external effects may require idempotency and database/device conditional versions beyond local scheduling.

### Build the capacity vector

List:

$$
C=(connections,outstanding\ ops,queue\ count/bytes,workers,buffers,
dependencies,results,retries,tenants,timers).
$$

For each give hard bound, owner, full policy, metric and shutdown behavior. A finite upstream queue with an unbounded downstream executor is not bounded. A Proactor with unlimited submissions is not scalable. A Future graph can be an unbounded queue without visible queue depth.

Sustainable pipeline throughput cannot exceed its slowest stage/dependency. More workers before 32 database connections only create another wait. Use Little's Law for stable measured averages, but size from tail/burst/deadline and failure distributions.

### Build the wait-for graph

Nodes include locks, pool workers, event loops, leaders, queues, connection pools, futures, device operations and result executors. Draw directed waits. Look for:

- Monitor A waits on B while retaining A;
- pool parents wait on children queued to same saturated pool;
- event loop blocks enqueue while workers block publishing results to loop;
- Active Object method waits on its own future;
- pool A waits on B and B waits on A;
- shutdown waits for workers after destroying their result/dependency path.

Remove cycles through open calls, async composition, resource order, reserved/accommodating capacity, explicit queues or ownership redesign. Timeout detects a wait but does not prove safe effect cleanup.

### Specify cancellation and effects

For every stage list queued, running, completed, delivered and external-effect cancellation. A future/timeout can stop observation while work continues. A Proactor cancel can lose to completion. A blocking library may be uncancellable. A Monitor wait interruption returns under lock but prior mutation may exist.

Carry stable request/effect identity, deadline and owner generation through every seam. Late results are reaped; stale delivery is suppressed; actual effects are reconciled. Do not promise exactly once from a local terminal cell.

### Design shutdown from the ownership graph

Stop external admission first. Fence connection/object/pool generation. Close queues so blocked producers/consumers terminate. Decide drain versus abort. Request cancellation without releasing resources prematurely. Keep completion/result/event-loop paths alive while operations/workers finish. Reconcile ambiguous durable effects. Join threads/tasks, then destroy queues, locks, handles and dependencies in reverse ownership order.

Write shutdown states before implementation. A design that works only during steady state is incomplete.

### Compare candidates on separate axes

Use a decision record rather than one score:

| Axis | Questions |
| --- | --- |
| Safety | Ownership, invariant, memory visibility, buffer lifetime, ordering, stale generations |
| Liveness | Blocking, wait cycles, starvation, leader gaps, guard progress, cancellation |
| Capacity | Counts, bytes, downstream, tenants, results, failure-mode overload |
| Semantics | Readiness/completion, acceptance, delivery, external effect, durability |
| Operations | Metrics, debugging, drain, rollout, recovery, backend portability |
| Performance | Throughput/tails, context switches, cache, batching, CPU/memory/power |
| Human complexity | API clarity, team expertise, proof/test burden, failure diagnosis |

Reject safety/lifecycle mismatches before benchmarking. Performance results are deployment-specific and cannot repair semantic errors.

### Candidate fit matrix

| Constraint shape | Primary fit | Disqualifying signal |
| --- | --- | --- |
| Many readiness handles, nonblocking bounded handlers | Reactor | Handler calls blocking/long foreign work |
| Native submitted operations and result completions | Proactor | API actually reports readiness/uses hidden blocking without bound |
| Async I/O owner plus blocking sequential services | Half-Sync/Half-Async | Unbounded queues or worker access to owner state |
| Shared event set, direct bounded handler pool | Leader/Followers | All handlers can block/exhaust leader candidates |
| Independent bounded tasks | Thread Pool | Shared mutable ordering or same-pool wait cycles |
| Stateful async method interface with guards | Active Object | Long servant blocking/unbounded mailbox |
| Short synchronous protected state/conditions | Monitor Object | Foreign I/O/callbacks or cross-lock cycles under monitor |
| Rate-mismatched item stages | Bounded Producer-Consumer | Loss/fan-out/durability semantics left implicit |
| One eventual result | Future/Promise (supporting) | Treated as capacity/execution architecture |

Patterns can support one another: Monitor implements a buffer; Future returns Active Object results; Thread Pool powers Half-Sync. Supporting mechanisms do not change the primary ownership model.

### Avoid pattern accumulation

Adding Reactor + Proactor + Active Object + Thread Pool + queues everywhere can create duplicate scheduling, copies and unclear ownership. Each seam needs a force: backend event mismatch, blocking isolation, state ownership, rate mismatch, durability or fault isolation. If a seam has no specific force, remove it.

Collapse adjacent queues when they provide no separate admission/failure/ownership boundary. Do not collapse a necessary security, durability, dependency bulkhead or scheduling boundary merely to reduce diagrams.

### Prototype alternatives with representative failure

For plausible candidates implement thin vertical slices with real backend and dependency. Test normal load, burst, slow/stuck dependency, cancellation, connection close/reuse, full queues, result consumer stall, worker/handler exception, process shutdown/restart and tenant skew. Capture full end-to-end tails and resource curves.

Benchmark comparable semantics: same capacity, durability, ordering, error/cancel, payload and workload. A faster design that drops or reorders differently is not equivalent.

### Record selection and triggers

The architecture decision should include constraints, candidates rejected and why, chosen ownership/seams, capacity vector, wait graph, backend versions, verification evidence, known limitations and triggers to revisit. Examples: dependency becomes nonblocking; tail service exceeds budget; connection volume changes; platform completion support matures; durability requirement appears.

“Review required” is a valid selector output when a constraint combination is unsupported or unknown. It prevents silently defaulting to an unsafe catch-all.

### A finite executable selector

This deterministic ruleset illustrates constraint-driven primary selection for eight canonical shapes. It is pedagogical, not a universal architecture engine; real systems require the full analyses above and may need a small explicit composition.

<!-- bijux-verify: {"id":"sepat-080-constraint-selector","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"readiness_gateway=reactor\ncompletion_storage=proactor\nlegacy_async_gateway=half-sync-half-async\nshared_cache=monitor-object\nguarded_account=active-object\ncpu_batch=thread-pool\nshared_event_service=leader-followers\nstream_pipeline=bounded-producer-consumer\nchecks=ownership,blocking,event,ordering,capacity,effect,shutdown,evidence\n","stderr":""}} -->
```python
def select_pattern(spec):
    if spec.get("stream") and spec.get("rate_mismatch"):
        return "bounded-producer-consumer"
    if spec.get("shared_state") and spec.get("short_sync_methods"):
        return "monitor-object"
    if spec.get("isolated_state") and spec.get("async_methods"):
        return "active-object"
    if spec.get("async_front") and spec.get("blocking_service"):
        return "half-sync-half-async"
    if spec.get("event_model") == "readiness":
        if spec.get("rotating_shared_pool") and spec.get("bounded_handlers"):
            return "leader-followers"
        if spec.get("nonblocking_handlers"):
            return "reactor"
    if spec.get("event_model") == "completion":
        return "proactor"
    if spec.get("independent_tasks") and spec.get("bounded_execution"):
        return "thread-pool"
    return "review-required"


scenarios = (
    ("readiness_gateway", {"event_model": "readiness", "nonblocking_handlers": True}),
    ("completion_storage", {"event_model": "completion"}),
    ("legacy_async_gateway", {"async_front": True, "blocking_service": True}),
    ("shared_cache", {"shared_state": True, "short_sync_methods": True}),
    ("guarded_account", {"isolated_state": True, "async_methods": True}),
    ("cpu_batch", {"independent_tasks": True, "bounded_execution": True}),
    ("shared_event_service", {"event_model": "readiness", "rotating_shared_pool": True, "bounded_handlers": True}),
    ("stream_pipeline", {"stream": True, "rate_mismatch": True}),
)
for name, constraints in scenarios:
    print(f"{name}={select_pattern(constraints)}")
print("checks=ownership,blocking,event,ordering,capacity,effect,shutdown,evidence")
```

## Definitions and Notation

Let ownership graph (O=(R,D)) map mutable resources (R) to owner domains (D). Blocking map β assigns each call/context a worst-case blocking class. Wait graph (G_w=(V,E)) records resource/execution dependencies. Ordering equivalence ∼ partitions operations into domains requiring serialization.

Capacity vector (C=(c_1,\ldots,c_n)) records hard resource bounds and full policies. Stage service rates are μᵢ; accepted rate λ; end-to-end deadline (D_r); lifecycle generation (g); and stable request/effect identity (r,e).

A candidate (P) is admissible only if it maps every resource to one ownership policy, respects β, preserves required ∼, has finite C, handles cycles/effects/lifecycle and has testable evidence obligations.

## Mechanisms, Invariants, or Proof Structure

### Ownership-preservation argument

If each mutable resource has exactly one owner/synchronization protocol and every seam transfers immutable/exclusive envelopes with generation-qualified results, two domains cannot concurrently mutate the same resource in the abstract design. Implementation aliases, unsafe APIs and external systems remain proof obligations.

### Blocking-isolation argument

If all potentially unbounded calls are absent from multiplexing/ownership-critical contexts and occur only in finitely admitted workers/dependencies with result return, one slow call cannot directly block the owner loop/scheduler. It can still saturate queues/workers and cause overload; capacity/full policy handles that separate property.

### Capacity/stability argument

Finite C bounds declared resources if no hidden buffers/graphs exist. Throughput cannot exceed the bottleneck; when λ exceeds sustainable minimum service, some bound reaches its full policy. More upstream concurrency/queue capacity cannot prove stability.

### Liveness limits

An acyclic wait graph plus eventually terminating operations and fair-enough scheduling supports progress under stated premises. Timeouts/cancellation can bound waits but do not retroactively undo effects. External failure, priority and scheduler behavior require empirical/recovery evidence.

### Review discipline

Proof review checks mapping assumptions line by line. Automated models validate finite state/invariants. Integration tests validate exact backends/dependencies. Load/fault tests support performance/reliability claims. Named human review is required for domain/safety/regulatory correctness.

## Alternatives and Trade-Offs

| Selection strategy | Advantage | Failure mode | Better practice |
| --- | --- | --- | --- |
| Familiarity-first | Fast initial implementation | Forces every workload into one model | Constraint and ownership inventory |
| Benchmark-first | Optimizes measured path | Compares unequal/unsafe semantics | Reject safety mismatches, then benchmark |
| Library/API-first | Uses ecosystem defaults | Hidden queues/executors/backend | Inspect exact implementation/contracts |
| Thread-count heuristic | Simple number | Ignores dependencies/memory/tails | Capacity vector and measured workload |
| Pattern-per-component | Clear local labels | Too many queues/ownership seams | Minimal seams tied to forces |
| One global pattern | Uniformity | Bad fit for mixed blocking/state/I/O | Explicit small composition |
| Fully custom lock-free | Potential hot-path gains | Huge proof/maintenance burden | Proven library until evidence requires custom |
| Durable workflow everywhere | Strong persistence | Excess latency/operational complexity | Use only at durable/long-lived boundary |

Uniformity is valuable when constraints match. A standard bounded Thread Pool/queue can be better than a theoretically faster custom ring because correctness, tooling and team operations dominate. Conversely, a genuine completion backend may justify Proactor over emulated readiness/offload.

## Failure Modes and Misconceptions

- **“Async/await selects Proactor.”** Syntax does not identify readiness, completion or hidden workers.
- **“Nonblocking always scales best.”** CPU, memory, dependencies, buffers and complexity still bind.
- **“Blocking is always wrong.”** Bounded dedicated/lightweight-thread contexts can be simplest and safe.
- **“Thread pool solves concurrency.”** It schedules tasks; state ownership/order remain.
- **“Future solves backpressure.”** It represents one result and can multiply work invisibly.
- **“Monitor serializes external effects.”** Only protected local state is serialized.
- **“Active Object prevents all races.”** Leaked aliases, continuations and external work can race.
- **“Leader/Followers has no queue.”** Kernel/upstream backlog remains and all processors can remove leadership.
- **“Proactor cancellation frees buffers.”** Actual terminal completion/backend contract returns ownership.
- **“One bounded queue bounds the pipeline.”** Every hidden/downstream/upstream dimension must be finite.
- **“More workers fix latency.”** They can overload the dependency and worsen tails.
- **“FIFO queue gives ordered responses.”** Parallel completion/effects reorder.
- **“Timeout makes wait graph safe.”** Ambiguous effects/resources and recurrence remain.
- **“Pattern composition is modular automatically.”** Seams need ownership, capacity and lifecycle contracts.
- **“Lock-free is the advanced choice.”** Proof and operability can outweigh hot-path benefit.
- **“Passing tests selects the architecture.”** Representative overload/fault/backend evidence is required.

## Worked Examples

### Example 1

**Situation.** A server has many readiness sockets and all handlers only parse bounded frames/update connection state.

**Reasoning.** Reactor fits with one/partitioned owner loops, fairness budgets, bounded connection/output/in-flight state and no blocking handlers. Proactor adds no value if backend only reports readiness; a worker handoff adds ordering/copy cost without force.

**Conclusion.** Match event semantics and keep the smallest owner.

### Example 2

**Situation.** Native storage accepts asynchronous reads/writes with owned buffers and completion records.

**Reasoning.** Proactor fits if operation/buffer/cancel/outstanding/completion semantics are verified. Reactor would emulate readiness poorly; a blocking pool may be fallback for unsupported operations but must be separately bounded.

**Conclusion.** Completion ownership—not callback syntax—selects Proactor.

### Example 3

**Situation.** A Reactor gateway calls a blocking legacy database library.

**Reasoning.** Add one Half-Sync/Half-Async seam: finite immutable requests, workers no greater than safe DB share, finite results, generation/order checks on loop. Never block loop/caller-run or expose sockets to workers.

**Conclusion.** Mixed event/blocking models justify an explicit handoff.

### Example 4

**Situation.** A small in-memory resource pool needs synchronous acquire/release with condition waiting.

**Reasoning.** Monitor Object is direct: private state/invariant, condition loops, monotonic deadline, open call for slow validation and broadcast close. Active Object adds queue/future temporal semantics without need.

**Conclusion.** Short synchronous shared-state methods favor a monitor.

### Example 5

**Situation.** Concurrent clients submit guarded commands to one device state and need asynchronous results.

**Reasoning.** Active Object fits: exclusive proxy, finite activation queue, pure guards, sequential servant, futures on safe executor, external device work as generation-qualified continuation. Monitor would block callers and support less explicit scheduling.

**Conclusion.** Stateful async method scheduling favors Active Object.

### Example 6

**Situation.** Millions of independent bounded CPU transforms need parallel execution.

**Reasoning.** A finite Thread Pool/work-stealing design fits, but admission cannot enqueue millions blindly. Bound roots/bytes, match CPU/memory bandwidth, avoid blocking/nested waits, observe results and structure lifetime.

**Conclusion.** Independence selects task scheduling; finite input remains mandatory.

### Example 7

**Situation.** A transaction server wants direct shared-event handling with preallocated threads and bounded handlers.

**Reasoning.** Leader/Followers can reduce handoff/context cost if platform multi-wait/handle exclusion and promotion are correct. Size so handlers cannot consume every leader candidate; otherwise Half-Sync/Reactor separation is safer.

**Conclusion.** Leader rotation is a conditional optimization with liveness premises.

### Example 8

**Situation.** Telemetry ingestion, parsing and storage run at differing rates.

**Reasoning.** Bounded Producer-Consumer stages make rate mismatch/bytes/watermarks explicit. Preserve key order/identity, dependency limit, loss policy and close. Futures may report item outcomes but do not replace stage backpressure.

**Conclusion.** Repeated item flow selects bounded streaming queues/channels.

### Example 9

**Situation.** A local operation must survive process restart and take hours.

**Reasoning.** None of the in-memory patterns alone provides durable acceptance. Use a durable workflow/broker/operation resource with idempotency, leases, status and recovery; use local pools/loops inside workers as implementation details.

**Conclusion.** Reject the candidate set when durability changes the problem class.

### Example 10

**Situation.** A clinical command gateway has readiness network I/O, blocking certified validation, per-patient ordered state and durable device effects.

**Reasoning.** Likely composition: Reactor owns sockets; bounded Half-Sync workers call validation under certified capacity; per-patient Active Object/partition applies ordered current-authority state; durable effect ledger/device protocol reconciles. Each seam is finite/generation-qualified; simpler alternatives are evaluated. Named clinical/safety review owns policy.

**Conclusion.** High-stakes composition is justified only by distinct ownership/blocking/durability forces.

## Cross-Program Connections

- [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md): quality attributes, deployment/failure boundaries and ADRs frame selection.
- [Software Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md): models, controlled schedules, load/fault experiments and reproducibility validate choices.
- [Operating Systems](../../22-operating-systems/ROADMAP.md): I/O APIs, threads, memory models, scheduling and handles constrain available semantics.
- [Security Engineering](../../25-security-engineering/ROADMAP.md): authority, tenant isolation, resource exhaustion, stale state and protected evidence cross every seam.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md): deadlines, durability, idempotency, effects and recovery define limits of local patterns.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md): quotas, pools, autoscaling, rollout drain, telemetry and incident response operationalize selection.
- [SEPAT-071](071-reactor.md) through [SEPAT-079](079-producer-consumer-with-bounded-buffers.md) are the candidate pattern set synthesized here.

## References

1. Schmidt, Douglas C., Michael Stal, Hans Rohnert, and Frank Buschmann. *Pattern-Oriented Software Architecture, Volume 2*. Wiley, 2000.
2. Schmidt, Douglas C. “Reactor.” <https://www.dre.vanderbilt.edu/~schmidt/PDF/reactor-siemens.pdf>. Accessed 2026-08-29.
3. Schmidt, Douglas C., Carlos O'Ryan, Michael Kircher, and Irfan Pyarali. “Leader/Followers.” <https://www.dre.vanderbilt.edu/~schmidt/PDF/lf.pdf>. Accessed 2026-08-29.
4. Schmidt, Douglas C., and Charles D. Cranor. “Half-Sync/Half-Async.” <https://www.dre.vanderbilt.edu/~schmidt/PDF/PLoP-95.pdf>. Accessed 2026-08-29.
5. Lavender, R. Greg, and Douglas C. Schmidt. “Active Object.” <https://www.dre.vanderbilt.edu/~schmidt/PDF/Act-Obj.pdf>. Accessed 2026-08-29.
6. Schmidt, Douglas C. “Monitor Object.” <https://www.dre.vanderbilt.edu/~schmidt/PDF/monitor.pdf>. Accessed 2026-08-29.
7. Oracle. “ThreadPoolExecutor,” “BlockingQueue,” and “CompletableFuture,” Java SE 25 API. <https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/concurrent/ThreadPoolExecutor.html>. Accessed 2026-08-29.
8. Boost C++ Libraries. “The Proactor Design Pattern,” Boost.Asio. <https://www.boost.org/latest/doc/html/boost_asio/overview/core.html>. Accessed 2026-08-29.
9. Goetz, Brian, et al. *Java Concurrency in Practice*. Addison-Wesley, 2006.
10. Herlihy, Maurice, and Nir Shavit. *The Art of Multiprocessor Programming*, revised 1st ed. Morgan Kaufmann, 2012.
11. Harchol-Balter, Mor. *Performance Modeling and Design of Computer Systems*. Cambridge University Press, 2013.
12. Nygard, Michael T. *Release It!*, 2nd ed. Pragmatic Bookshelf, 2018.
13. Gregg, Brendan. *Systems Performance*, 2nd ed. Addison-Wesley, 2020.

Backend I/O, queue/executor defaults, cancellation, memory visibility, scheduler fairness, lightweight threads and shutdown vary by platform/runtime/library version. Current official sources were checked on 2026-08-29; qualify exact deployments.

## Exercises

### Exercise 1

Create the ownership, blocking, event, ordering, capacity, wait-for, cancellation/effect and shutdown models for an API gateway with readiness sockets, JWT validation, blocking database, per-account ordering and asynchronous client responses. Select/reject candidates with reasons.

### Exercise 2

A pipeline accepts 900 requests/s. Parse capacity is 1,400/s, 24 workers each sustain 45/s for the workload, and a database safely supports 700/s. Mean measured residence is 0.4 s. Compute worker nominal capacity, bottleneck upper bound and Little's-Law average resident requests. Explain the architectural consequence and limitations.

### Exercise 3

Compare Monitor Object, Active Object and generic Thread Pool for a stateful device controller with guarded commands, slow device I/O, synchronous status reads and 5,000 devices. Propose a minimal composition and its verification obligations.

### Exercise 4

Diagnose an architecture with Reactor handlers doing blocking calls, unlimited Proactor submissions, an unbounded common Thread Pool, futures waited by the same pool, workers writing sockets, per-entity operations unordered, three implicit queues and loop-first shutdown. Redesign and define tests.

### Exercise 5

Select and justify a concurrency architecture for a safety-critical emergency-control platform with many connections, blocking certified libraries, per-asset ordered state, durable effects, strict deadlines and fail-safe operation. Include rejected alternatives, capacity, lifecycle, security, evidence and named review.

## Answers to the Exercises

### Answer 1

Reactor/partitioned loops own listeners, sockets, parser, connection generation and output order. JWT verification is classified: local bounded crypto may remain under fairness budget or use bounded CPU pool; remote key refresh is async/separate. Database API is blocking, so a Half-Sync seam transfers immutable request/account/generation/deadline/authority/effect envelopes into a finite queue. Worker concurrency is at most a measured safe DB pool share; workers never touch sockets.

Per-account effects require one in-flight/partitioned queue, Active Object-style state owner, or conditional database version/idempotency—not global serialization. Results return through finite queue/thread-safe loop wake and are generation/current-authority checked. Futures represent responses but do not own capacity.

Reject pure Reactor because DB blocks; pure Proactor because readiness/DB are not completion operations; thread-per-connection absent strict connection/thread proof; unbounded generic executor; Monitor across network/DB; Leader/Followers if handlers block; per-account Active Object with dedicated thread due 5,000+ scaling unless shared scheduler. Capacity includes connections, frame bytes, JWT tasks, DB queue/workers/connections, per-account pending, results/output, tenants/retries/timers. Wait graph excludes loop-blocking queues and same-pool waits. Shutdown stops listeners, drains/cancels queues, reaps DB effects/results, closes sockets, joins then destroys.

### Answer 2

Worker nominal capacity is

$$
24\times45=1080\text{ requests/s}.
$$

Pipeline upper bound is the minimum of parse 1,400, worker 1,080 and database 700, so at most 700 requests/s under stated safe rates. Accepted 900/s exceeds the bottleneck: no finite queue is long-run stable. Little's Law for the *claimed stable measured boundary* gives

$$
L=900\times0.4=360.
$$

But the rates contradict a long-run stable pipeline unless 900 is transient, measurement boundary excludes rejected/backlogged work, or DB 700 is not binding during that sample.

Architecture must reduce admission below sustainable DB service, shed/queue durably under explicit semantics, increase DB safe capacity, cache/change work, or relax outcome—not add workers/buffer. Measurements need aligned boundaries, workloads, distributions and failure behavior. Means do not prove tails, ordering, correctness or durability.

### Answer 3

Monitor Object gives synchronous caller-thread state and conditions, but holding it across slow device I/O is unsafe and synchronous status can contend. Active Object naturally serializes guarded commands and returns futures, but one thread/queue per 5,000 devices wastes resources and one slow method blocks. Generic Thread Pool supplies shared capacity but does not preserve per-device state/order/guards.

Use a shared-scheduler Active Object/partition model: one private servant/mailbox/generation/active token per device, finite global/device/tenant count/bytes, and bounded executor time slices ensuring one request per device at once. Synchronous status returns an immutable safely published snapshot (or bounded monitor read) if freshness contract permits. A command records pending intent/effect under device owner, initiates slow I/O through dependency-bounded async/worker pool, then generation-qualified completion reenters the device mailbox. Futures deliver on separate bounded context.

Verify one-active-token model, pure guards/fair device selection, current snapshots, command order, stale completion, cancel/deadline/effect races, hot-device fairness, exact capacity, device pool stall, callback context, close/reuse, shared scheduler crash and restart reconciliation; run hardware/device fault, load/tail, race/memory and security tests.

### Answer 4

Blocking Reactor handlers freeze multiplexing; unlimited Proactor operations consume buffers/rings; unbounded pool/futures hide overload and same-pool wait deadlocks; workers violate socket affinity; unordered entity effects corrupt state; implicit queues prevent capacity accounting; loop-first shutdown strands results.

Keep Reactor handlers bounded. Verify which operations are true Proactor and cap outstanding counts/bytes/completion handling. Put blocking work behind one explicit finite Half-Sync boundary with worker count matching dependencies and asynchronous composition (no same-pool get). Transfer immutable generation-qualified envelopes; only loop writes sockets. Partition/serialize per entity or use conditional versions. Enumerate/merge queues unless each provides a real ownership/dependency/durability boundary; bound both directions and expose oldest age.

Shutdown stops admission, fences generations, closes/drains/cancels work, requests/reaps operations, keeps loop/result delivery alive, reconciles effects, closes sockets and joins executors before destruction. Tests cover blocking detection, full queues, same-pool graph, buffer lifetime, out-of-order/stale results, entity races, dependency/loop/result stall, cancellation, operation completion after close, memory bounds, overload, graceful/forced shutdown and process recovery.

### Answer 5

Use readiness Reactor or verified native Proactor per actual connection backend, partitioned for connection scale/CPU. Certified blocking libraries run behind finite Half-Sync queues/workers constrained by certified/dependency capacity. Per-asset ordered state uses shared-scheduler Active Objects/partitions with generation, guard and one-active ownership—not a thread each. Durable command/effect ledger/workflow sits at the irreversible boundary; local futures expose status but never substitute for durable truth.

Reject pure loop because certified calls block; thread-per-connection unless bounded/qualified; generic pool alone because state/order absent; Monitor across external calls; Leader/Followers where blocking exhausts leaders; in-memory queues/futures for durable acceptance; Proactor label where backend is readiness. Capacity covers connections/buffers/outstanding I/O, validation count/bytes/workers/dependency, per-asset mailboxes, durable backlog, results/output, priorities/tenants/retries/timers with hazard-approved full policies.

Carry authenticated command/asset/session/generation, authority/policy, sequence, deadline and effect identity. Cancellation stops safe future work but reconciles issued effects. Fail-safe mode handles uncertainty/overload. Shutdown transfers admission to safe fallback, drains/cancels by criticality, reaps/reconciles effects, fences old generations and resumes only after durable/physical-state reconciliation. Apply least privilege, mutual authentication, replay defense, encryption, protected audit and quotas.

Evidence includes formal ownership/state/order/wait models, exact backend/certified-library contracts, model checking, hardware-in-loop, worst-case timing, saturation/priority, network/device/library/power/process fault injection, stale/duplicate/late effects, security/adversarial, fail-safe and recovery drills. Production claims require named domain/safety, certified-library, controls/concurrency, communications, human-factors, security, reliability/operations and regulatory reviewers with traceable hazards and acceptance evidence.
