---
module_id: SEPAT-082
program: Software Engineering: Patterns
level: 2
module_number: 82
title: Timeout and Deadline
status: complete
last_verified: 2026-08-29
---

# Timeout and Deadline

## One-Page Review

### Governing question

How can one caller-owned time budget govern queueing, nested calls, retries, parallel work, cleanup, response and ambiguous external effects without resetting at each layer?

### Essential definitions

- A **timeout** bounds one wait or activity duration from a local start.
- A **deadline** is the latest time by which an operation or outcome is still useful under a declared clock/protocol.
- An **absolute operation deadline** is established once at admission and inherited by all descendant work.
- **Remaining budget** is max(0, T − now) for deadline T on the relevant clock.
- A **child deadline** is no later than its parent and may be earlier due to dependency limits or reserved time.
- An **attempt timeout** bounds one attempt inside the remaining operation budget.
- A **queue budget** bounds time before execution; expiration in a queue should prevent stale work from starting.
- A **cleanup/response reserve** protects time for reconciliation, resource release, serialization and delivery.
- **Cancellation** signals that work is no longer wanted or authorized; it is cooperative unless a runtime contract proves stronger behavior.
- A **late outcome** completes after the observer stopped waiting and still requires ownership/effect handling.

### Central model, mechanism, or theorem

For parent deadline Tₚ, local time t, child maximum duration m and parent reserve g, derive

\[
T_c=\min(T_p-g,\;t+m),\qquad T_c\le T_p.
\]

Admit work of minimum useful duration w only if

\[
t+w+g\le T_p.
\]

All queueing, backoff, attempts and dependent calls consume the same finite interval. Independent relative timeouts instead accumulate: three sequential five-second waits can consume about fifteen seconds, while three operations under one five-second absolute deadline cannot legitimately extend the caller's authority beyond five seconds.

### Critical invariants

- Establish a bounded absolute deadline at the ingress/ownership boundary; untrusted callers cannot demand infinite retention.
- Every child deadline is at most its parent and every retry uses the original deadline.
- Compute local elapsed/remaining time with a monotonic clock; use wall-clock/protocol timestamps only with explicit skew/conversion rules.
- Count queue, connection acquisition, DNS/TLS, request, response body, backoff, callback, serialization and cleanup time according to the declared boundary.
- Do not start work that cannot finish meaningfully within remaining budget and reserve.
- Propagate cancellation to descendants, observe it in long work, release timers/resources, and reap late completions.
- A local timeout does not prove remote cancellation, rollback, non-execution or absence of durable effect.
- Parallel children share the same temporal boundary; concurrency does not create new time or capacity.
- Longer deadlines are not free: they retain memory, sockets, workers, locks, queue entries and authority.
- Telemetry distinguishes deadline source, queue time, attempt time, cancellation reason, late outcome and effect reconciliation.

### Common failures

Common failures include no deadline by default, resetting a five-second timeout at every hop, timing only socket read while DNS/connect/TLS/queue remain unbounded, using wall clock for elapsed duration, trusting arbitrary client deadlines, truncating sub-millisecond budgets to zero/infinity, starting expensive work with no response reserve, treating `Future.get(timeout)` as task cancellation, swallowing interruption/cancellation, orphaning child tasks, returning timeout while continuing an unbounded mutation, retrying after deadline, applying one global constant to unlike operations, benchmarking only healthy latency, and calling a timeout an SLO or correctness proof.

### Compact example

An API admits a request with absolute deadline 5,000 ms on its local monotonic timeline. Parsing ends at 400 ms. A database child has a 2,200 ms maximum and the parent reserves 300 ms, so its deadline is min(4,700, 2,600) = 2,600 ms. If it returns at 2,700 ms, it is already late even though 2,300 ms remain for a fallback/response. No descendant may create a new five-second budget. A mutation that committed before its response timed out is reconciled rather than declared rolled back.

### Connections

[SEPAT-081](081-retry-with-bounded-backoff.md) places retry delay and attempts inside one deadline. This module prepares the time boundaries required by forthcoming Circuit Breaker, Bulkhead, Rate Limiter, Load-Shedding, Saga, Transactional Outbox and Idempotent Consumer modules.

## Governing Question

What temporal contract lets a distributed operation stop useless work and bound resource retention while preserving correct ownership of cancellation, late results and uncertain effects?

A timeout is local mechanism. A deadline is end-to-end intent. Cancellation is a signal. None proves that a remote effect did not happen. Production design keeps these meanings separate and composes them through one request-scoped lifetime.

## Why This Matters

Without deadlines, slow or failed dependencies can retain finite resources until a service collapses. With poorly composed timeouts, each layer may wait its full local allowance after upstream interest has ended. With aggressive timeouts, healthy tail requests fail, retry traffic rises and useful work is abandoned. The design problem is therefore not “add a timeout”; it is select, propagate, enforce, observe and test a bounded temporal contract against workload and effect semantics.

Deadlines also express authority. After a caller disconnects or a command expires, continuing computation may waste capacity or violate a freshness/safety decision. Yet irrevocable work already issued may require completion or reconciliation. The right response depends on the state machine, not the timer alone.

## Prerequisites and Retrieval

Learners should retrieve:

- monotonic versus civil/wall time, duration, resolution, overflow and skew;
- request lifecycle, asynchronous completion and cooperative cancellation;
- queueing, utilization, tail latency and Little's Law;
- partial failure, ambiguous result and idempotency;
- connection pools, thread pools and backpressure;
- tracing/metrics and fault injection;
- [bounded retry](081-retry-with-bounded-backoff.md) and [concurrency ownership](080-selecting-a-concurrency-pattern-from-blocking-and-ownership-constraints.md).

Before continuing, explain why stopping a wait is different from stopping a computation and why stopping a computation is different from undoing an external effect.

## Learning Objectives

After this module, learners can:

1. distinguish timeout, deadline, cancellation, expiry, attempt bound and effect outcome;
2. derive child deadlines without extending parent authority;
3. allocate queue, dependency, retry, cleanup and response reserves;
4. choose correct local clocks and cross-process propagation representations;
5. design cooperative cancellation trees and ownership of late completions;
6. prevent stale queued work and unbounded connection/body/shutdown waits;
7. select deadlines from user value, SLOs, latency distributions and failure costs;
8. verify temporal boundaries with virtual clocks, controlled stalls and real integration evidence;
9. reason about security, overload and safety consequences of time policy.

## Core Exposition

### Distinguish the contracts

A relative timeout answers: “from this local start, how long may this operation or wait continue?” An absolute deadline answers: “after what instant is this logical result no longer wanted?” A cancellation signal answers: “the owner asks descendants to stop.” Expiry is the observation that a deadline passed. None alone states whether an effect occurred.

Different timeouts have different scopes: pool acquisition, DNS lookup, TCP connection, TLS handshake, request write, first byte, idle gap, entire response body, transaction statement, lock wait, queue wait, future wait, graceful drain. A “2 s HTTP timeout” is incomplete unless the library version and covered phases are named. Some APIs leave phases unbounded; some reset idle timers when bytes arrive, allowing a trickle to retain a connection indefinitely.

The operation deadline encloses all relevant phases:

\[
L_{end-to-end}=L_{queue}+L_{acquire}+L_{connect}+L_{service}+L_{response}+L_{cleanup}.
\]

The sum is a boundary model, not a claim that phases are independent or strictly sequential. Parallel work takes the maximum critical-path duration while consuming aggregate resources.

### Establish deadline at ingress

Translate a trusted operation profile or bounded caller request into an absolute local deadline once. Enforce minimum/maximum policy: rejecting absurdly short requests may be clearer than starting guaranteed failure; cap excessive deadlines to protect resources. Authenticate any deadline that carries command authority across trust boundaries.

For interactive work, user value and public SLO help set the maximum, but the two are not identical. An SLO describes an aggregate service objective; a deadline governs one operation. A deadline should include network and response delivery reserve and should be validated against latency distributions under realistic load/failure, not chosen just above a current p99.9 without accounting for sampling, deployments or cold paths.

For durable work, the request deadline may govern admission/acknowledgement while the accepted workflow has a separately stated maximum age or due time. Do not silently detach work from the caller: return an acceptance contract and durable status identity.

### Derive children

If a parent deadline is Tₚ and current time t, a child cannot exceed Tₚ. It may be shortened by a dependency maximum and reserved parent work:

\[
T_c=\min(T_p-g, t+m).
\]

Reserve g is not arbitrary padding. It owns required cleanup, fallback decision, result mapping, serialization, network return and uncertain-effect recording. Separate hard safety reserve from optional quality work.

Sequential children consume remaining time. Parallel children may share a parent deadline, but limit concurrency and decide whether all results, a quorum, first acceptable result or one primary outcome is required. Cancel losing/redundant work where safe, and still reap its completions.

Never derive a child from a fresh default when a parent exists. A child may be earlier but not later. Long-lived infrastructure background work needs its own explicit lifecycle instead of inheriting an expired request or discarding request authority accidentally.

### Clock and propagation

Use a monotonic clock for local elapsed duration/deadline arithmetic because civil time can jump due to synchronization, administrator changes or leap handling. Preserve sufficient resolution, saturate arithmetic safely and test near-zero/overflow boundaries.

Cross-process protocols vary. An absolute civil timestamp is interoperable but exposed to clock skew. A relative remaining duration avoids directly comparing remote clocks but loses transit time unless the protocol/runtime subtracts elapsed time. gRPC documentation describes converting a propagated deadline to a timeout with elapsed time deducted to mitigate skew; exact language behavior varies and must be verified. Do not invent a timestamp header without specifying clock, units, skew, authentication, transit behavior and hop processing.

At a receiving service, clamp propagated time to local policy. Record original source and effective deadline without trusting client-supplied diagnostics as authority.

### Cancellation tree

Cancellation should flow from an operation owner to descendant calls/tasks, not from arbitrary child to unrelated parent. A derived child can be cancelled earlier. Long loops check at bounded intervals; blocking APIs need a real cancellation/interrupt/deadline mechanism; queues drop expired items before expensive work; callbacks and results need an owner even after cancellation.

Cancellation is cooperative unless the runtime specifies otherwise. Java `Future.cancel(true)` attempts interruption when applicable; it does not guarantee arbitrary code or remote I/O stops. A timed `Future.get` only stops waiting unless the caller explicitly cancels and the task observes it. Go contexts carry cancellation/deadline signals; functions must propagate and observe them. gRPC server applications remain responsible for stopping spawned activity after call cancellation.

Resource cleanup must run exactly once under races between success, error, timeout and cancellation. Close/release ownership should be idempotent. Do not hold locks while waiting for cancellation completion. Bound cleanup while preserving a durable reconciliation path for work that cannot be safely abandoned.

### Late and ambiguous outcomes

A client can time out at the same instant a server commits. The client knows only that it did not observe success in time. State possibilities include not started, executing, committed with response lost, failed with response lost, or still running. For a mutation, classify as ambiguous unless the protocol supplies stronger evidence.

Use durable idempotency/effect identity, conditional updates, status queries, outbox/workflow records or reconciliation. A late successful completion must not mutate destroyed request state or be silently dropped if it establishes durable truth. Generation/fencing prevents a completion from an old request/connection instance affecting a new owner.

Cancellation after dispatch means “stop if still safely stoppable,” not rollback. Compensation is a new domain action with its own failure semantics.

### Queueing and overload

Deadline-aware queueing rejects/expires stale items before service. Store deadline and enqueue time; order by business policy, not automatically earliest deadline, unless schedulability and fairness are analyzed. Head-of-line blocking can cause many operations to expire together. Queue-time histograms and oldest-age reveal overload earlier than handler latency alone.

Long deadlines increase average resident work. By Little's Law, L = λW at a stable boundary: increasing mean residence W at fixed λ increases resident requests and associated memory/connections. Timeouts limit residence but do not create capacity; overload requires concurrency bounds, admission, rate limiting and shedding.

Timeouts can worsen overload: a request times out, retries, while original work continues. Align cancellation, retry owner, dependency isolation and effect handling. Do not use timeouts as the only bulkhead.

### Selection and calibration

Start from consequence of lateness and abandonment, then measure realistic latency by operation/dependency/region/workload. Include queueing, cold start, connection establishment, TLS/DNS, payload size, failure and deployment. Select a deadline that respects user/business/safety value and resource risk. Define dependency maximum and reserves explicitly. Revisit on material topology or workload change.

False-positive timeouts waste completed work and may duplicate load. False-negative long waits retain resources and deliver stale results. Tail-percentile heuristics are inputs, not proofs. Model correlation: downstream latency is not independent across attempts/requests during an incident.

### Executable budget model

The following deterministic model uses integer milliseconds on a fictional monotonic timeline. It derives children and tests the exact admission boundary. It does not sleep or claim runtime enforcement.

<!-- bijux-verify: {"id":"sepat-082-deadline-budget","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"root_deadline_ms=5000\nafter_parse_remaining_ms=4600\ndatabase_child_deadline_ms=2600\nafter_database_remaining_ms=2300\nexact_boundary_admitted=true\none_ms_late_admitted=false\nthree_reset_timeouts_ms=15000\none_absolute_budget_ms=5000\n","stderr":""}} -->
```python
def remaining(deadline_ms, now_ms):
    return max(0, deadline_ms - now_ms)


def child_deadline(parent_ms, now_ms, maximum_ms, reserve_ms):
    return min(parent_ms - reserve_ms, now_ms + maximum_ms)


def can_admit(parent_ms, now_ms, useful_ms, reserve_ms):
    return now_ms + useful_ms + reserve_ms <= parent_ms


root = 5000
database = child_deadline(root, 400, 2200, 300)

print("root_deadline_ms=" + str(root))
print("after_parse_remaining_ms=" + str(remaining(root, 400)))
print("database_child_deadline_ms=" + str(database))
print("after_database_remaining_ms=" + str(remaining(root, 2700)))
print("exact_boundary_admitted=" + str(can_admit(root, 4200, 500, 300)).lower())
print("one_ms_late_admitted=" + str(can_admit(root, 4201, 500, 300)).lower())
print("three_reset_timeouts_ms=" + str(3 * 5000))
print("one_absolute_budget_ms=" + str(root))
```

This proves arithmetic for fixed inputs only. It omits timer resolution, scheduling, wall/monotonic conversion, I/O, queueing, cancellation, interruption, cross-host skew, process pause, resource cleanup and external effects.

### Observability and verification

Trace logical deadline source/effective value and child derivation without high-cardinality raw timestamps as metric labels. Record queue/acquire/connect/service/response/cleanup durations, remaining budget at admission/dispatch/completion, cancellation initiator/reason, deadline-exceeded location, work avoided, late outcome and reconciliation. Separate caller cancellation, local policy deadline, dependency timeout, server pushback and shutdown.

Use virtual/injectable monotonic clocks for deterministic boundaries, but test actual runtime timers and transport behavior separately. Cover:

- exact equality, one tick before/after, zero/negative, precision truncation and overflow;
- parent earlier than child maximum; reserve exceeding remainder;
- sequential and parallel children; retry/backoff consumption;
- queue expiry before dispatch and deadline during service/response;
- cancellation before start, during waits/CPU/I/O/effect and after success race;
- APIs that ignore interruption/cancellation; late callbacks after owner destruction;
- response loss after commit and durable reconciliation;
- clock jumps/skew/transit conversion and process suspension;
- overload, cold start, connection/DNS/TLS stalls and shutdown drain;
- telemetry conservation: every accepted operation reaches terminal or durable uncertain state.

Tests against mocks cannot prove real driver cancellation, server effect status, timer precision, network ambiguity or production tail capacity. Fault experiments must use isolated systems under explicit ownership.

## Definitions and Notation

Let Tₚ and T꜀ be parent/child deadlines, t monotonic local time, B(t)=max(0,T−t) remaining budget, m child maximum duration, g cleanup/response reserve, w minimum useful work, q queue time, a attempt time and L end-to-end residence. A timeout Δ created at t₀ produces local deadline t₀+Δ; repeatedly creating Δ at nested starts is deadline reset.

Let X mean cancellation requested, O terminal observed outcome and E durable effect state. X does not logically imply ¬E. `DEADLINE_EXCEEDED` is an observer/runtime status under a protocol, not proof of remote non-execution.

## Mechanisms, Invariants, or Proof Structure

**Non-extension.** Because T꜀ = min(Tₚ−g,t+m), T꜀ ≤ Tₚ when g ≥ 0. Inductively, every descendant derived this way is no later than the root deadline. Clock-domain conversion must preserve this order within declared uncertainty.

**Admission safety.** If work is admitted only when t+w+g ≤ T and completes within w under model assumptions, reserve g remains before T. The premise is empirical/contractual; actual scheduling and failures may violate w, so cancellation/reconciliation remain necessary.

**Bounded policy lifetime.** A finite root T bounds policy-authorized inline descendants only if every queue, wait, call and spawned task observes the deadline/cancellation and cleanup is bounded or transferred durably. Uncooperative operations are counterexamples.

**Cancellation-tree containment.** Parent cancellation reaches all registered descendants; a child cannot cancel unrelated ancestors/siblings through the ownership interface. Race-safe cleanup/reaping is required for terminal ownership.

**Effect uncertainty.** Timeout/cancellation changes observer interest and perhaps execution scheduling, but without an atomic effect protocol there exists an execution where commit precedes lost response. Therefore ¬observed-success does not imply ¬effect.

**No universal optimum.** Deadline selection depends on user value, workload distribution, topology, capacity and failure costs. A measured percentile does not prove safety, availability or optimality outside its experiment.

## Alternatives and Trade-Offs

| Alternative | Prefer when | Limitation |
|---|---|---|
| one absolute deadline | interactive/directed work has one usefulness boundary | needs propagation and reserves |
| local phase timeout | bounding a specific acquisition/read/idle phase | can leave other phases unbounded or reset end-to-end time |
| child shorter than parent | dependency has a stricter maximum or fallback needs time | too short creates false failures/retry load |
| caller cancellation only | work loses value when caller leaves | disconnect may be transient; durable accepted work needs separate lifetime |
| durable workflow deadline/maximum age | work legitimately outlives request | changes acceptance/status contract and operational burden |
| server-enforced limit | protects service from excessive caller deadlines | cannot know all caller value and does not stop client wait alone |
| adaptive policy by operation/profile | stable classes have different costs/distributions | complexity, feedback safety and policy versioning |
| no deadline | only for explicitly lifecycle-owned background services | shutdown/resource/failure bounds still mandatory; rarely valid for request work |

## Failure Modes and Misconceptions

- **Timeout and deadline are synonyms.** A duration can create a deadline, but scope and reset behavior differ.
- **A timeout cancels work.** Many APIs only stop the wait.
- **Cancellation rolls back.** External effects may already be issued or committed.
- **A child gets the full configured maximum.** It gets at most parent remainder minus reserve.
- **Parallel work has independent budgets.** It shares time and consumes capacity concurrently.
- **Wall time is fine for elapsed duration.** Clock adjustments can extend or shorten waits.
- **Monotonic time can be sent across hosts.** Its epoch is generally local; use protocol conversion.
- **One client deadline is always authoritative.** Clamp untrusted/excessive values and authenticate command authority.
- **The handler timeout covers the body.** Library-specific phases must be verified.
- **Expired queue items can run because work was accepted.** Stale work consumes capacity and may violate semantics.
- **Longer deadline improves reliability.** It may raise residence/overload and worsen tails.
- **Short deadline protects capacity.** Not if abandoned work continues or retries multiply it.
- **Deadline exceeded means server failed.** The observer may have imposed too little time or lost a successful response.
- **Virtual-clock tests prove timing.** They prove policy logic, not runtime timers/transports.
- **One percentile chooses the deadline.** Workload, false-timeout cost, cold/failure paths and user value matter.

## Worked Examples

### Example 1

An edge establishes T=2 s. Authentication consumes 180 ms and parsing 20 ms. A child profile allows 1.5 s, while 250 ms is reserved for mapping/response. The child deadline is min(1.75 s, 1.7 s)=1.7 s from ingress—not 1.5 s from whenever a nested library happens to start after further delay.

### Example 2

Three sequential services each configure five seconds locally. Under reset semantics, failure can take about fifteen seconds plus overhead. Propagating one deadline causes later services to receive only remainder; a service rejects before starting if its minimum useful time plus reserve no longer fits.

### Example 3

An HTTP client sets a read-idle timeout but no pool-acquisition or total-body deadline. Saturated connections wait indefinitely, and a peer sends one byte before every idle expiry. The fix names and bounds queue/acquire/connect/TLS/headers/body/total phases under one operation deadline and size/rate limits.

### Example 4

A queued image transformation expires before a worker receives it. The worker checks the stored deadline/generation before allocation and returns expired without processing. Queue metrics record avoided work. If the job was durably accepted under a separate workflow contract, request disconnect does not delete it; its maximum age governs instead.

### Example 5

Two replicas are queried in parallel for the first acceptable read. Both inherit the parent deadline and separate concurrency admission. When one succeeds, the loser is cancelled, but its completion is reaped and resources closed. A late result cannot write into a recycled request object.

### Example 6

A Java caller times out on `future.get(100, MILLISECONDS)`. The task continues because timed get only bounded waiting. The owner invokes supported cancellation, the task checks interruption, the underlying driver receives its deadline, and late completion is handled. Tests include a deliberately uninterruptible dependency to verify isolation and shutdown.

### Example 7

A payment call reaches its deadline just after the ledger commits. Returning “failed, no charge” is false. The API returns/records an uncertain outcome keyed by durable command identity; replay/query yields the committed result. Cancellation suppresses further safe work but does not create a compensating refund implicitly.

### Example 8

A fleet uses civil timestamps from callers whose clocks differ by seconds. Some requests arrive expired and others overrun. The protocol uses its documented deadline propagation/conversion, clamps local effective duration, records skew diagnostics and uses local monotonic time for enforcement. Security policy prevents clients from extending signed command validity.

### Example 9

At 800 requests/s with stable mean residence 0.25 s, Little's Law estimates 200 resident requests at the defined boundary. Raising mean residence to 2 s without changing arrivals yields 1,600 residents, before considering retries or instability. Longer deadlines require capacity/admission evidence, not only a configuration change.

### Example 10

An infusion-control command has a clinical validity interval, communications deadline and device actuation deadline. Expiry triggers a hazard-defined fail-safe state, not generic retry. Authenticated sequence/fencing rejects stale commands; device acknowledgement loss triggers reconciliation. Worst-case timing, clock failure, power/network faults and human response require named clinical, controls, hardware, security and operations review.

## Cross-Program Connections

- [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md): end-to-end policy ownership and dependency budgets.
- [Software Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md): virtual time, race boundaries, fault injection and decisive temporal oracles.
- [Operating Systems](../../22-operating-systems/ROADMAP.md): clocks, timers, scheduling, interruption and resource retention.
- [Network Engineering](../../24-network-engineering/ROADMAP.md): DNS/connect/TLS/read phases, transport ambiguity and cross-host timing.
- [Security Engineering](../../25-security-engineering/ROADMAP.md): authenticated validity, replay/stale command defense and resource-exhaustion limits.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md): partial failure, cancellation propagation, late results and effect reconciliation.

## References

1. gRPC Authors. “Deadlines.” gRPC Documentation. <https://grpc.io/docs/guides/deadlines/>
2. gRPC Authors. “Cancellation.” gRPC Documentation. <https://grpc.io/docs/guides/cancellation/>
3. Go Authors. “Package context.” Go Standard Library Documentation. <https://pkg.go.dev/context>
4. Ajmani, Sameer. “Go Concurrency Patterns: Context.” Go Blog, 2014. <https://go.dev/blog/context>
5. Oracle. “Future.” Java SE 25 API Specification. <https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/concurrent/Future.html>
6. IEEE and The Open Group. “Clock and Timer Functions.” POSIX.1-2024, Base Definitions/System Interfaces. <https://pubs.opengroup.org/onlinepubs/9799919799/functions/clock_gettime.html>
7. Brooker, Marc. “Timeouts, Retries, and Backoff with Jitter.” Amazon Builders' Library, 2019. <https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/>
8. Nygard, Michael T. *Release It!*, 2nd ed. Pragmatic Bookshelf, 2018.
9. Kleppmann, Martin. *Designing Data-Intensive Applications*. O'Reilly, 2017.
10. Harchol-Balter, Mor. *Performance Modeling and Design of Computer Systems*. Cambridge University Press, 2013.
11. Jain, Raj. *The Art of Computer Systems Performance Analysis*. Wiley, 1991.
12. Gregg, Brendan. *Systems Performance*, 2nd ed. Addison-Wesley, 2020.
13. OpenTelemetry Authors. “Semantic Conventions for RPC.” <https://opentelemetry.io/docs/specs/semconv/rpc/>

Runtime defaults, covered timeout phases, clock resolution, propagation, cancellation and driver behavior vary by version/platform. Current official sources were checked on 2026-08-29; verify the exact deployed stack.

## Exercises

### Exercise 1

Model a 3,000 ms API operation that calls authentication, database and object storage, then serializes a response. Define deadline source, child derivation, queue/attempt limits, reserves, cancellation and late-effect handling.

### Exercise 2

At t=350 ms under parent deadline 2,000 ms, reserve is 250 ms. Child maximum durations are 900 ms and 1,600 ms. Compute each child deadline if considered separately. At t=1,300 ms, determine whether work needing 500 ms plus the reserve may start. Explain equality.

### Exercise 3

A stable boundary receives 600 requests/s. Mean residence increases from 0.2 s to 1.5 s after deadline expansion. Compute average resident requests before/after and discuss why the calculation does not prove adequate capacity or causality.

### Exercise 4

Diagnose a service with relative five-second timeouts at four layers, wall-clock elapsed arithmetic, unbounded pool acquisition, timed future waits without cancellation, ignored queue expiry, retries with fresh time, and mutations reported rolled back at timeout. Redesign and specify tests.

### Exercise 5

Design temporal policy for a safety-critical remote control system with clock uncertainty, intermittent network, strict actuation validity and irreversible effects. Include security, fail-safe/reconciliation, evidence and named review.

## Answers to the Exercises

### Answer 1

Establish T=3,000 ms at trusted ingress on a monotonic local timeline after clamping caller policy. Carry the operation context explicitly. Authentication might receive min(T−response/cleanup reserve, now+auth maximum). Database and object storage get separately measured maxima, dependency concurrency limits and deadlines no later than parent; sequential work consumes remainder, while parallel work shares T and bounded capacity. Queue items carry T and expire before dispatch.

Reserve time for fallback/effect reconciliation, result mapping, serialization and network response. Each retry delay/attempt remains inside T and one retry owner. Cancellation propagates to cancellable descendants; long CPU work checks it; driver operations use real deadlines. Stop new work when minimum useful duration plus reserve does not fit. Reap callbacks and close resources exactly once.

Reads may discard generation-stale results after cleanup; mutations use durable effect identity/status. Timeout after dispatch is ambiguous until query/replay/reconciliation proves state. Telemetry records source/effective deadline, phase times, remaining budgets, cancellation, late result and terminal/durable-uncertain outcome.

### Answer 2

Parent-minus-reserve is 2,000−250=1,750 ms. At t=350, the 900 ms child yields min(1,750,1,250)=1,250 ms. The 1,600 ms child yields min(1,750,1,950)=1,750 ms. Both are absolute instants on the stated timeline.

At t=1,300, admission requires 1,300+500+250≤2,000. The sum is 2,050, so it must not start. Equality would be admitted by the model because it preserves exactly the declared reserve at the deadline, although real systems usually include uncertainty/scheduling margin and must define timer-resolution semantics.

### Answer 3

Little's Law gives L=λW. Initially L=600×0.2=120 average resident requests. After expansion, L=600×1.5=900. This is 7.5 times the residency at the defined stable boundary.

The calculation assumes aligned long-run averages and stability. It does not give distribution/tails, memory per request, concurrency at individual dependencies, hidden queues, retries, abandonment, correlation or causality. The expanded deadline may cause residence, may merely reveal an already slower dependency, or may change acceptance/retry behavior. Capacity requires measured resource and overload evidence.

### Answer 4

Four reset timeouts can consume roughly twenty seconds plus uncovered phases. Wall-clock jumps corrupt elapsed budgets. Unbounded acquisition bypasses the timeout. Timed future wait leaves tasks running. Expired queued work wastes capacity. Fresh retry budgets extend caller authority and amplify load. Timeout cannot prove mutation rollback.

Create one bounded ingress deadline on monotonic time; explicitly cover queue/acquire/DNS/connect/TLS/write/read/body and cleanup. Derive every child ≤ parent−reserve and clamp client input. Pass cancellation context; use driver/runtime cancellation and isolate uncooperative work. Expire queues before service. Reap late futures/results. Put bounded retry under the original deadline. Use durable identity/reconciliation for mutations and report uncertainty honestly.

Test exact time boundaries, clock jumps/precision/overflow, each stalled phase, queue expiry, sequential/parallel propagation, cancel before/during/after execution, uninterruptible task, late callback after owner close, commit/response-loss ambiguity, retries, overload/residency, cold starts and graceful/forced shutdown. Validate actual libraries/drivers and telemetry accounting, not only virtual-time mocks.

### Answer 5

Define authenticated command issue time, validity interval, device generation/fence, sequence, effect identity, maximum communication delay and actuation deadline under an explicit clock synchronization/uncertainty model. Clamp remote claims locally and reject/fail safe when uncertainty consumes the safe window. Use monotonic time locally; protocol time conversion includes skew/transit bounds and protected time sources.

Cancellation/expiry prevents future safe steps but does not undo issued actuation. Durable controller/device state distinguishes reserved, sent, acknowledged, observed, failed and uncertain. Lost acknowledgement triggers state reconciliation; repeat only when hazard analysis and device idempotency/fencing prove safety. Stale generations/sequences and replayed commands are rejected. Capacity reserves critical control without allowing priority abuse; overload enters a hazard-defined fail-safe mode.

Evidence includes formal timed state/effect model, worst-case execution/communication/clock-error analysis, model checking where feasible, hardware-in-loop deadline/race/duplicate/lost-ack tests, time-source failure, process/device/power/network fault injection, overload, security/replay tests, protected audit and recovery drills. Approval requires named domain/clinical or industrial safety, controls, hardware, communications/timing, distributed systems, security, reliability/operations, human-factors and regulatory reviewers with traceable hazards and acceptance criteria.
