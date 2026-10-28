---
module_id: CONPAR-036
program: Programming Languages: Concurrent & Parallel Programming
level: 1
module_number: 36
title: Cancellation and Timeouts
status: complete
last_verified: 2026-08-29
---

# Cancellation and Timeouts

## One-Page Review

### Governing question

When an owner no longer wants an operation's result or its deadline expires, how can the system stop useful work, preserve committed effects, release resources, and report one truthful terminal outcome?

### Essential definitions

- **Cancellation request** communicates that an owner wants work to stop; it is not proof of termination.
- **Cancellation acknowledgement** confirms that a component observed the request and reached its declared cancellation boundary.
- A **timeout** is a local decision made when waiting exceeds a duration or deadline.
- A **deadline** is an absolute expiration instant for an end-to-end operation, preferably on a monotonic clock within one process.
- A **time budget** is the remaining interval before the deadline after reserving overhead/cleanup.
- A **cancellation point** is a boundary where an operation checks or receives cancellation.
- **Cancellation safety** means abandonment at a permitted point preserves specified local and protocol invariants.
- A **commit point** separates work that can be discarded/restarted from work whose outcome must be recovered or compensated.
- **Shielding/masking** temporarily defers cancellation so a critical cleanup or commit sequence can finish.
- A **late outcome** arrives after the public caller has timed out, cancelled, or otherwise stopped waiting.

### Central model, mechanism, or theorem

Separate the public-result state machine from underlying execution. Public state changes once from PENDING to SUCCEEDED, FAILED, CANCELLED, or TIMED_OUT. A timeout winner may request cancellation, but underlying work continues through CANCELLING to STOPPED, or it may complete and produce a late outcome. The owner is finished only after the public result is settled and every underlying resource/task is either joined, transferred to a named supervisor, or represented by durable recovery state.

### Critical invariants

One public terminal transition wins. Request, observation, acknowledgement, and cleanup are distinct timestamps. Cancellation propagates only along owned edges and does not corrupt unrelated work. Deadlines never reset at each stage; children receive no more than remaining budget. Expiration prevents starting work that cannot usefully finish. Commit-point outcomes are recovered rather than blindly retried. Late values/errors are observed and resources disposed. Cancellation reasons preserve cause without leaking secrets. Cleanup is idempotent, bounded, and joined. Clock semantics and boundary translation are explicit.

### Common failures

Code treats timeout as proof the server did nothing; creates a fresh timeout per stage; cancels a future but drops the task handle; assumes thread interruption is safe; swallows cancellation as ordinary success; catches cancellation and keeps running; retries a possibly committed operation without an idempotency key; leaves timers/listeners registered; shields an unbounded region; uses wall clock for elapsed budgets; lets cleanup exceed the original deadline invisibly; or reports “cancelled” while background mutations continue.

### Compact example

At logical time 10 a deadline settles the public result as TIMED_OUT and requests cancellation. The producer reports success at 11 before acknowledging cancellation at 12. Success cannot resettle the public result; it is a late outcome whose resource must be disposed or whose durable effect must be recovered. Acknowledgement at 12 proves only the producer reached its stop boundary. Joining cleanup completes ownership.

### Connections

[Cooperative Scheduling](035-cooperative-scheduling.md) supplies cancellation checkpoints; [Async/Await State Machines](034-async-await-state-machines.md) supplies suspension cuts. The [program roadmap](../ROADMAP.md) next scopes child lifetimes with structured concurrency.

## Governing Question

How should cancellation, timeout, deadline, commit, retry, cleanup, and late-completion protocols be designed so stopping interest never masquerades as stopping effects?

Cancellation is a lifecycle protocol, not an exception class.

## Why This Matters

Users navigate away, requests exceed latency objectives, services shut down, supervisors fail fast, and speculative races discard losers. Without cancellation, obsolete work consumes CPU, memory, connections, locks, quotas, and remote capacity. With poorly specified cancellation, systems corrupt partial state, duplicate committed effects, leak resources, or lie about safety.

APIs differ. WHATWG `AbortSignal` broadcasts a reason and APIs decide how to react. .NET cancellation tokens support cooperative observation and callbacks. Go contexts carry cancellation and deadlines through call trees. Java `Future.cancel` may attempt interruption, but interruption is cooperative and API-specific. Python task cancellation injects `CancelledError` at a suspension boundary. Dropping a Rust future abandons its local state, while Tokio timeout returns when its inner future is dropped. None is a universal rollback primitive.

The portable discipline separates desire, signal, observation, terminal classification, effect recovery, and join.

## Prerequisites and Retrieval

Retrieve:

- safety/liveness from [Safety, Liveness, and Progress](004-safety-liveness-and-progress.md);
- resource counting from [Semaphores and Resource Counting](014-semaphores-and-resource-counting.md);
- bounded pools from [Thread Pools and Bounded Work Queues](019-thread-pools-and-bounded-work-queues.md);
- future/task ownership from [Futures and Promises](033-futures-and-promises.md);
- suspension cuts from [Async/Await State Machines](034-async-await-state-machines.md); and
- cooperative checkpoints from [Cooperative Scheduling](035-cooperative-scheduling.md).

Retrieval prompt: when a deadline wins, list the underlying task, timer, remote effect, result resource, cancellation listener, and cleanup handle that still require an owner.

## Learning Objectives

After completing this module, a learner can:

1. distinguish cancellation request, observation, acknowledgement, terminal outcome, and join;
2. design one-shot arbitration among success, failure, cancellation, and timeout;
3. propagate absolute deadlines without resetting budgets;
4. build a cancellation ledger around each suspension/commit point;
5. classify operations as safe to abandon, recover, compensate, or finish;
6. handle late values, errors, timers, listeners, and resource release;
7. scope shielding and cleanup with separate bounded policy;
8. integrate cooperative checks, blocking work, and remote cancellation honestly;
9. test races with virtual time and placed barriers; and
10. avoid retrying ambiguous effects without identity and deduplication.

## Core Exposition

### Separate five lifecycle events

Cancellation has at least five moments:

1. an owner decides the result is no longer wanted;
2. a request/signal is published;
3. the worker observes it;
4. work reaches a terminal stop or competing outcome; and
5. the owner joins cleanup and classifies the result.

These moments can be separated by scheduler delay, blocking code, network loss, or non-cooperating libraries. Telemetry should not label request time as completion time. An API returning from `cancel()` may mean only that the request was recorded.

### Public outcome and underlying execution

The caller-facing future and the producer task are different state machines. A timeout wrapper can settle the former while the latter still runs. If the wrapper abandons all references, a late error becomes unobserved and a late value can leak a file, socket, permit, or transaction handle.

Designate a loser owner. It may await termination, attach disposal, transfer work to a supervisor, or record a durable operation ID for later recovery. “The caller stopped waiting” is never an ownership plan.

### Terminal arbitration

Success, failure, explicit cancellation, deadline, and shutdown can race. Use one atomic or event-loop-owned transition from PENDING. Only the winner publishes the public outcome and performs one-time public accounting. Losing paths still release their inputs and report late/duplicate evidence.

Precedence should come from linearization, not a fragile chain of `if cancelled` checks. Some products deliberately prefer a completed value if it was committed before the deadline even when delivered later; others classify by observation time. State the rule and retain both underlying and public timestamps.

### Cooperative cancellation points

CPU loops check a token at bounded intervals. Async tasks observe cancellation at waits or explicit checks. Blocking calls respond only if their API supports interruption/cancellation. Foreign code may ignore the signal entirely.

Maximum response includes remaining non-checking work, scheduler latency, downstream stop time, and cleanup. A 10 ms token polling interval cannot promise 10 ms termination if one indivisible call blocks for seconds.

At each point, state must be valid. Private candidate data can be discarded. Shared effects need a commit protocol, compensation, or durable recovery.

### Cancellation safety is operation-specific

Memory-safe destruction can release owned local fields while leaving semantic damage. Abandoning a channel receive before it removes an item may be safe; abandoning a frame write after a prefix is visible can corrupt the peer protocol. Cancelling fair lock acquisition can lose queue position without corrupting memory, changing fairness.

Create a ledger for each cancellation point: local state retained/dropped, locks/permits, external effects, peer expectation, late-result route, and restart rule. Do not label an entire library “cancellation safe” based on one method.

### Commit points and ambiguous outcomes

Before commit, cancellation should ensure the semantic effect did not occur. At commit, an authority durably records ownership/identity. After commit, cancellation stops waiting or further work but cannot pretend the effect vanished.

Remote timeout commonly yields UNKNOWN: request may not have arrived, may be executing, or may have committed while the response was lost. Use an idempotency key and status/replay protocol. Retrying under a new identity can duplicate payments, jobs, messages, or commands.

Compensation is a new effect that can fail; it is not rollback equivalence. Record its ownership and deadlines separately.

### Durations, deadlines, and clocks

A duration says “wait this long from now.” A deadline says “the whole operation expires then.” Giving connect, authenticate, query, and write each a fresh 500 ms timeout can consume two seconds. Compute one deadline at admission; before each stage derive `remaining=deadline-now`, subtract required cleanup/transport reserve, and refuse work when nonpositive.

Use monotonic time for in-process elapsed budgets so wall-clock adjustment cannot extend or shorten them. Absolute monotonic instants generally cannot be transmitted between machines because epochs/rates differ. Distributed protocols often send remaining timeout or a wall-time deadline and reconstruct a local deadline while accounting for elapsed transit and skew. gRPC converts deadlines across systems and warns that cancellation requires explicit propagation/handling.

Clock choice, precision, overflow, timer granularity, and suspend behavior belong in the contract. A deadline firing is itself scheduled and may occur late under overload.

### Budget allocation and reserves

Children cannot receive more than the parent's remaining budget. A stage can have a smaller cap: `child_deadline=min(parent_deadline, now+stage_cap)`. Reserve time for response serialization, cancellation propagation, and cleanup instead of spending the entire budget on primary work.

Static percentages are a starting policy, not truth. Queue delay, retry cost, and downstream latency consume budget. Observability should record remaining time at each stage. Starting a side effect with less time than its minimum safe completion/recovery interval is an admission defect.

### Timeout wrappers own two branches

A timeout races an operation and timer. If operation wins, cancel/retire the timer and publish its result. If timer wins, publish timeout once, request cancellation, keep observing the operation, dispose late resources, and join or transfer cleanup. If both are ready, use a documented tie/selection rule.

Timer handles and abort listeners are resources. Remove them when either branch wins. Reusing a signal that is already aborted should take an immediate, specified path. Never retain a callback after the operation's lifetime.

A wrapper that simply races promises without controlling the producer is a waiting timeout, not an execution timeout. Name it honestly.

### Cancellation propagation trees

Parents normally propagate cancellation to owned children; children do not automatically cancel siblings or parents unless supervision policy says so. Linking unrelated requests to one token creates failure coupling. Failing to link a child leaves orphan work.

Use derived tokens/contexts with parent deadline, child cap, stable operation identity, and causality. Remove registrations when the child terminates. Combine sources—user cancel, parent failure, deadline, shutdown—into one first cause plus a record of later causes; repeated requests must be idempotent.

Do not put secrets or unbounded exception graphs into broadcast reasons. Reasons cross trust, logging, and lifetime boundaries.

### Catching cancellation correctly

Cancellation is often represented as an exception/error, but semantics differ from ordinary failure. Catching a broad exception and returning success can swallow cancellation and make shutdown hang. Catch only to restore invariants, add context, or translate at an architectural boundary, then re-signal unless policy deliberately converts it.

Cleanup code must distinguish primary failure from cancellation and cleanup failure. Observability usually records cancellation separately from service errors; retries may treat user cancellation, deadline, overload, and infrastructure failure differently.

Some runtimes allow a task to suppress cancellation. That is a powerful policy choice and must not become an accidental `catch`.

### Shielding and masking

Short regions may need to finish despite cancellation: releasing a permit, publishing a commit record and its outcome pointer, restoring an invariant, or joining a critical child. Shielding defers delivery to that region; it does not grant infinite time.

Keep the shield minimal, use a cleanup deadline, make actions idempotent, and remember the pending cancellation afterward. Shielding remote business work just to obtain success defeats caller budget and overload controls. If a commit sequence cannot be safely interrupted, admission must ensure enough remaining budget before it begins.

### Blocking and interruption

Thread interruption is cooperative notification, not safe asynchronous termination. Code must define which waits respond, restore interrupt status when appropriate, and leave shared state consistent. Some calls are uninterruptible; native or device operations may continue.

For bounded blocking pools, cancellation can remove not-started work, signal running work, and ignore/dispose late output. The task handle remains owned until terminal. Killing arbitrary threads can strand locks and violate foreign/runtime invariants; use process isolation when forceful termination is required by an untrusted workload.

### Resource ownership and cleanup

For every operation, inventory timer, token registration, task/future, queue slot, semaphore permit, buffer, file/socket, transaction, remote ID, and trace span. Assign each exactly one release or transfer path for every terminal race.

Cleanup should be idempotent because timeout, shutdown, and producer completion may converge. Release one-time resources through guarded ownership, not repeated best-effort callbacks. A cleanup deadline that expires produces a residual-resource report and escalates to a documented forced policy; it does not make the resource disappear.

### Retry is not cancellation recovery by default

Retry consumes the same end-to-end deadline and resource budget. It begins a new attempt, so the owner must stop/observe the previous attempt or use durable idempotency. Backoff must not sleep past the deadline. Retry only classified transient outcomes; do not retry user cancellation.

Hedging starts multiple attempts intentionally. It needs unique attempt identities under one logical idempotency key, cancels losers, joins them, and accounts for amplified load. Under overload, hedging can worsen the tail it tries to reduce.

### Shutdown uses the same protocol

Shutdown stops admission, signals cancellation, permits bounded drain/cleanup, aborts/isolates remaining work under policy, and joins every task. A process signal is merely the first request. Closing the scheduler before waiters observe cancellation strands them.

Committed work may need to finish or become durably recoverable while uncommitted queued work is rejected. Response writes may be bounded separately. Record one shutdown cause, idempotently handle repeated signals, and report residual tasks/resources.

### Observability and deterministic tests

Record operation ID, parent ID, start/deadline, remaining budget at stage entry, cancel requester/reason, request/observation/acknowledgement/join timestamps, public winner, underlying outcome, commit state, cleanup duration, and late result. Avoid high-cardinality secret reasons.

Tests should place the operation with barriers: before start, waiting, just before commit, just after commit, during cleanup, and after terminal. Use a controllable monotonic clock/timer. Exercise both branches of every race, duplicate cancellation, already-cancelled input, zero/negative budget, timer cleanup, late success/error, blocking non-response, and shutdown. Wall-clock sleeps are weak race evidence.

## Definitions and Notation

Let request, observation, acknowledgement, and join times be `t_req <= t_obs <= t_ack <= t_join` when all occur. Missing acknowledgement is a valid outcome that must be reported, not invented.

For deadline `D` and monotonic time `t`, remaining budget is `R(t)=max(0,D-t)`. A child deadline `D_c` satisfies `D_c<=D`; with stage cap `s`, choose `D_c=min(D,t+s)`.

Public terminal indicators for operation `o` are success `S_o`, failure `F_o`, cancellation `C_o`, and timeout `T_o`. Exactly one public outcome requires `S_o+F_o+C_o+T_o=1`. Underlying execution has a separate terminal indicator and may become terminal later.

At cancellation cut `k`, let `E_k` be externally visible effects and `O_k` owned local resources. Cancelling can release `O_k` under its cleanup rules but does not imply inverse effect `E_k^{-1}` exists or succeeds.

## Mechanisms, Invariants, or Proof Structure

Audit cancellation and timeout in this order:

1. identify public result owner, worker owner, timer owner, and remote authority;
2. enumerate success, failure, cancellation, timeout, shutdown, and duplicate attempts;
3. linearize one public winner while preserving every losing resource/outcome;
4. distinguish request, observation, acknowledgement, terminal stop, and join;
5. define one monotonic end-to-end deadline and child caps/reserves;
6. build a ledger at every cancellation/commit cut;
7. define idempotency, status recovery, compensation, and late-result policy;
8. propagate cancellation only through owned relationships with bounded reasons;
9. constrain masking and blocking with explicit cleanup/termination bounds;
10. remove timers/listeners and release permits/handles exactly once;
11. stop admission, signal, drain, isolate/abort, and join at shutdown; and
12. place deterministic barriers on both sides of every race.

The executable trace makes timeout the public winner, then records late success, cancellation acknowledgement, and joined cleanup without a second public settlement.

<!-- bijux-verify: {"id":"timeout-cancellation-arbitration","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"public_outcome=timed_out\nwinner_time=10\ncancel_requested=True\ncancel_acknowledged=True\nlate_outcomes=['success@11']\npublic_transitions=1\nterminal_attempts=2\ncleanup=joined\n","stderr":""}} -->
```python
public = "pending"
winner_time = None
cancel_requested = False
cancel_acknowledged = False
late = []
public_transitions = 0
terminal_attempts = 0

events = [(10, "deadline"), (11, "success"), (12, "cancel_ack")]
for logical_time, event in events:
    if event == "deadline":
        terminal_attempts += 1
        if public == "pending":
            public = "timed_out"
            winner_time = logical_time
            cancel_requested = True
            public_transitions += 1
    elif event == "success":
        terminal_attempts += 1
        if public == "pending":
            public = "succeeded"
            winner_time = logical_time
            public_transitions += 1
        else:
            late.append(f"success@{logical_time}")
    elif event == "cancel_ack":
        cancel_acknowledged = True

print(f"public_outcome={public}")
print(f"winner_time={winner_time}")
print(f"cancel_requested={cancel_requested}")
print(f"cancel_acknowledged={cancel_acknowledged}")
print(f"late_outcomes={late}")
print(f"public_transitions={public_transitions}")
print(f"terminal_attempts={terminal_attempts}")
print("cleanup=joined")
```

Limitations: this logical-time single-thread model stipulates ordered events and successful cleanup. It does not implement clocks, threads, atomics, timer delay, cancellation delivery, resource disposal, failures, blocking, distributed effects, idempotency, deadline propagation, or forced termination.

## Alternatives and Trade-Offs

**No cancellation** simplifies local control flow but wastes obsolete resources and delays shutdown.

**Cooperative token/context** composes across owned calls and preserves cleanup, but latency depends on check points and API support.

**Future/task cancellation** may connect observation to execution more directly; semantics still vary for started work and interruption.

**Dropping an async future** promptly releases local state in ownership-oriented runtimes, but external effects and detached work need separate protocols.

**Process isolation/termination** can stop untrusted computation more forcefully. It is expensive and still requires durable external-effect recovery.

**Relative timeouts** are convenient for one isolated wait. **Absolute deadlines** preserve an end-to-end budget across queues and retries.

**Fail-fast cancellation** reduces wasted work. **Drain-to-completion** may be required after commit or for cheap cleanup. Structured owners can report early while still joining, if reporting and lifecycle are not conflated.

**Shielding** preserves a narrow invariant but worsens response latency and must have a bound. **Compensation** can address committed business effects but is another fallible operation.

## Failure Modes and Misconceptions

- “Cancel returned true, so execution stopped.” It may only change a handle state or request interruption.
- “Timeout means the effect did not happen.” Remote and buffered effects can commit late.
- “Cancellation is memory unsafety.” Memory safety and semantic cancellation safety are different.
- “A fresh timeout per stage preserves the caller budget.” It resets and multiplies it.
- “Wall-clock deadline is ideal inside one process.” Monotonic time is usually needed for elapsed budgets.
- “One monotonic instant can be sent to another host.” Monotonic epochs are generally local.
- “Catching all errors is robust.” It can swallow cancellation and block shutdown.
- “Dropping the promise stops its producer.” Observation and task ownership may be separate.
- “Shielding cleanup guarantees cleanup.” It can hang or fail without a separate policy.
- “Thread interruption safely preempts arbitrary code.” Cooperation and invariant restoration remain necessary.
- “Retry repairs timeout.” It can duplicate an ambiguous committed effect.
- “Timer expiration occurs exactly at deadline.” Scheduler load and clock resolution add delay.
- “Late success can be ignored.” It may contain a resource or durable operation identity.
- “Cancellation token performs cleanup.” It communicates intent; owners perform and join cleanup.

## Worked Examples

### Example 1

A pure search builds a private candidate list and checks cancellation every bounded chunk. On cancellation it discards the list and releases its permit. No external effect occurred, so restart is safe with the same input. The response bound still includes the longest chunk and scheduler latency.

### Example 2

A socket write times out after a prefix may have reached the peer. Closing local state prevents further writes but does not remove the prefix. The protocol needs framing that detects truncation and reconnect/recovery behavior; repeating blindly can duplicate or corrupt a message.

### Example 3

Connect, authenticate, query, and serialize each receive 500 ms, turning a nominal 500 ms request into two seconds. Establish `D` once, derive remaining time at each step, use smaller stage caps, and reserve response/cleanup time. Do not begin query if remaining time cannot cover its safe minimum.

### Example 4

A timeout races a file-open operation. The timer wins, but open later returns a descriptor. A loser observer closes the late descriptor and records cleanup. Without it, repeated timeout tests leak descriptors even though every public result is “timed out.”

### Example 5

A parent token cancels two owned children and one unrelated cache refresh because all share a global controller. Derive child tokens only along ownership edges. The cache refresh needs its own supervisor and shutdown policy; convenience is not authority.

### Example 6

A broad catch handles Python task cancellation as an ordinary exception and loops again. Shutdown never joins. Catch cancellation only around invariant restoration, then re-raise; classify it separately from service failure. Confirm exact exception hierarchy for supported Python versions.

### Example 7

A database request times out after the server commits but before reply. Retry uses the same idempotency key; a status query returns the existing committed result. A new key would create a second transaction. Client timeout is UNKNOWN, not “rolled back.”

### Example 8

Cleanup is shielded while closing a remote stream, but the peer never responds. Add a bounded cleanup deadline, then close transport locally and emit a residual-state report. An infinite shield converts cancellation into a new hang.

### Example 9

An uninterruptible codec occupies every blocking worker after callers cancel. Task handles remain owned; the queue stops admission; late outputs are discarded; shutdown reports workers past deadline and may isolate/terminate their process under policy. Token checks cannot interrupt foreign code.

### Example 10

A medication-order service times out after transmitting a dose command and automatically retries under a new identifier. The first command may have committed, so a duplicate dose is possible. Safety requires stable command identity, deduplication, authoritative status recovery, device acknowledgement and sensed-state checks, fail-safe workflow, and clinical reconciliation. Named pharmacy, clinical, device, distributed-systems, safety, cybersecurity, human-factors, and regulatory reviewers must approve evidence; this chapter cannot.

## Cross-Program Connections

- **Operating systems:** interruption, signals, timers, process isolation, and monotonic clocks constrain cancellation.
- **Distributed systems:** deadlines cross clock domains; timeout creates ambiguous remote outcomes.
- **Databases:** commit points, idempotency, and transaction recovery decide retry safety.
- **Security:** cancellation prevents resource exhaustion, while untrusted reasons and priorities need validation.
- **Reliability:** retry, hedging, shutdown, and residual-state reporting consume common budgets.
- **Software engineering:** tokens follow ownership and interface capability boundaries.
- **Observability:** causal timestamps distinguish slow propagation from slow cleanup.
- **Safety engineering:** local cancellation cannot substitute for independently verified physical safe state.

## References

1. WHATWG. “DOM Standard: AbortController and AbortSignal.” <https://dom.spec.whatwg.org/#interface-abortcontroller>.
2. Oracle. “Java Platform API: Future.cancel.” <https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/concurrent/Future.html#cancel(boolean)>.
3. Oracle. “Java Tutorials: Interrupts.” <https://docs.oracle.com/javase/tutorial/essential/concurrency/interrupt.html>.
4. Microsoft. “Cancellation in Managed Threads.” <https://learn.microsoft.com/en-us/dotnet/standard/threading/cancellation-in-managed-threads>.
5. Go Project. “Package context.” <https://pkg.go.dev/context>.
6. Python Software Foundation. “Coroutines and Tasks: Task Cancellation and Timeouts.” <https://docs.python.org/3/library/asyncio-task.html>.
7. Rust Project. “Asynchronous Programming in Rust: Cancellation.” <https://rust-lang.github.io/async-book/part-guide/more-async-await.html>.
8. Tokio Project. “tokio::time::timeout.” <https://docs.rs/tokio/latest/tokio/time/fn.timeout.html>.
9. gRPC Authors. “Deadlines.” <https://grpc.io/docs/guides/deadlines/>.
10. The Open Group. “clock_gettime.” <https://pubs.opengroup.org/onlinepubs/9799919799/functions/clock_gettime.html>.

## Exercises

### Exercise 1

Distinguish cancellation request, observation, acknowledgement, public terminal outcome, and join using one task timeline.

### Exercise 2

A four-stage operation assigns 300 ms independently to every stage. Replace this with one deadline, stage caps, and cleanup reserve. State clock assumptions.

### Exercise 3

Design a timeout wrapper that safely handles operation-first, timer-first, tie, late value, late error, timer disposal, and duplicate cancellation.

### Exercise 4

Create a cancellation/commit ledger for a remote payment request. Specify idempotency, status recovery, retry, compensation, and shutdown ownership.

### Exercise 5

An aircraft actuator client treats a local timeout as proof that a flap command was not applied and immediately sends an opposite command. Diagnose the hazard and define human evidence needed for production.

## Answers to the Exercises

### Answer 1

At `t_req`, the parent records intent and signals. At `t_obs`, the task next checks/receives it. At `t_ack`, the task reaches its defined cancelled terminal boundary after releasing or transferring resources. The public future may have settled CANCELLED or TIMED_OUT earlier at `t_pub`; that classification does not prove `t_ack`. At `t_join`, the owner observes terminal state and cleanup evidence. Some operations never acknowledge, so timeout/escalation must report that truth.

### Answer 2

At admission choose monotonic `D=now+300ms`, reserving, for example, an explicitly justified response/cleanup interval. For stage `i`, compute remaining `R=max(0,D-now)` and choose `D_i=min(D-reserve, now+cap_i)`; reject starting when no safe budget remains. Caps do not reset the parent. The monotonic clock is process-local; cross-host propagation sends a protocol-defined timeout/deadline and reconstructs local remaining budget while accounting for transport/skew. Percentages and minimums require measurement.

### Answer 3

Use one atomic/event-loop terminal arbiter. Operation-first publishes its value/error and unregisters the timer. Timer-first publishes timeout once, requests cancellation, and retains a terminal observer. A defined tie rule selects one winner. Late values are disposed or transferred; late errors are recorded. Repeated cancel is idempotent. Remove signal listeners and timer handles on every path, and join/transfer the producer before ownership ends. Tests place barriers on each ordering with virtual time.

### Answer 4

Before durable payment acceptance, cancellation releases local reservation and proves no charge under the authority's protocol. At commit, store idempotency key, request fingerprint, and status atomically. After commit or ambiguous transport loss, retry uses the same key and queries/attaches to status; it never invents a new payment. Compensation is a separately identified refund that can fail and needs its own owner/deadline. Shutdown rejects uncommitted queue entries, preserves recoverable committed records, cancels workers, observes late results, and joins cleanup.

### Answer 5

Local timeout proves only missing observation by a deadline; the actuator may have accepted, partially executed, completed, or rejected the first command. An opposite command can create unsafe motion without authoritative state. The protocol needs unique monotonic command identity, stale/duplicate rules, acknowledgement correlation, sensed-position verification, interlocks, bounded command/recovery behavior, and safe degradation. Production evidence requires named aerospace systems, flight-controls, actuator/hardware, real-time, functional-safety, cybersecurity, human-factors, verification, operations, and regulatory reviewers; hazard/requirements traceability; hardware-in-the-loop, timing, fault-injection, and environmental evidence; applicable-standard assessment; and signed residual-risk acceptance. This module grants no approval.
