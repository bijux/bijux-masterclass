---
module_id: CONPAR-037
program: Programming Languages: Concurrent & Parallel Programming
level: 1
module_number: 37
title: Structured Concurrency
status: complete
last_verified: 2026-08-29
---

# Structured Concurrency

## One-Page Review

### Governing question

How can concurrent child work be nested inside an owning scope so lifetime, failure, cancellation, result accounting, resource bounds, and observability follow the program's control structure?

### Essential definitions

- **Structured concurrency** requires child tasks to remain owned by a lexical/dynamic scope that does not finish until they reach terminal states.
- A **task group/nursery/scope** admits children, applies policy, cancels if required, and joins them before exit.
- A **fork** creates owned concurrent work; a **join** observes its terminal outcome and lifecycle completion.
- **Parent-child ownership** assigns cancellation, deadline, context, and failure observation along a task tree.
- **Fail-fast** stops new admission and requests sibling cancellation after a decisive failure, then still joins all accepted children.
- **Continue/collect** lets independent children finish and reports every outcome.
- An **exception/failure group** preserves multiple concurrent failures instead of discarding all but one.
- A **detached task** intentionally outlives its caller under a separate durable supervisor.
- **Terminal accounting** assigns every accepted child exactly one mutually exclusive outcome.
- **Bounded fan-out** limits accepted, queued, and running children before producer invocation.

### Central model, mechanism, or theorem

A task scope has states OPEN, CLOSING, CANCELLING, and JOINED. OPEN may accept child identities. On body completion or decisive failure, admission closes. Policy may signal children, but scope exit waits until every accepted child is terminal and cleanup has released its owned capacity. Therefore child lifetime is nested within scope lifetime. The no-orphan property is stronger than awaiting the first result: `accepted = succeeded + failed + cancelled + skipped/not-started`, with disjoint terminal categories.

### Critical invariants

Every child has exactly one parent/supervisor and stable identity. No accepted handle disappears before join. Admission stops before exit or fail-fast drain. Cancellation follows owned edges and is acknowledged through terminal outcomes. Sibling failure policy is explicit. Every child outcome, including panic/defect and cancellation-insensitive late completion, is observed. Permits remain held through required cleanup. Parent deadline/context propagate with narrower child policy. Result ordering is separate from completion ordering. Queue and fan-out are bounded. Detachment transfers ownership before scope exit.

### Common failures

Code starts promises before the group owns them; returns when the first child fails while siblings mutate state; drops task handles after cancellation; loses secondary failures; marks never-started work as failed; releases permits before cleanup; lets children spawn untracked grandchildren; confuses lexical scope with bounded concurrency; assumes task groups make operations cancellation-safe; holds borrowed state beyond its scope; or “detaches” work without a process-level supervisor, budget, error sink, and shutdown join.

### Compact example

A fail-fast group accepts A, B, C with width two. A and B start; C waits inert. B fails decisively, so admission closes, C becomes cancelled-before-start, and A receives cancellation. A may still succeed before observing it. The group joins A and B, then reports A=success, B=failure, C=cancelled-before-start. The exact frontier is schedule-dependent; the stable invariant is three accepted identities and three terminal outcomes.

### Connections

[Cancellation and Timeouts](036-cancellation-and-timeouts.md) supplies stop/join semantics; [Futures and Promises](033-futures-and-promises.md) supplies one-result ownership. The [program roadmap](../ROADMAP.md) next moves from task trees to actor mailboxes.

## Governing Question

How should task scopes be designed and reviewed so concurrency adds parallel lifetime beneath sequential structure without creating orphan work, hidden failure, unbounded fan-out, or ambiguous shutdown?

Structure makes lifetime visible; it does not make child operations correct automatically.

## Why This Matters

Unstructured task creation behaves like `goto` for lifetime. A function can return while work it started continues using request context, credentials, mutable state, sockets, or test fixtures. An early aggregate failure can hide sibling errors. Shutdown cannot know what remains. Stack traces and metrics lose the parent relationship.

Structured concurrency restores a tree: entering a scope creates an owner; forks create children; leaving the scope joins them. The shape mirrors blocks and calls. This makes cancellation and observability tractable, and allows scoped borrowing in languages that can prove children end first.

Implementations differ. Python `asyncio.TaskGroup` cancels remaining tasks after a non-cancellation child failure and can raise exception groups. Java StructuredTaskScope is a preview API with configurable joiner policy. Swift task groups and `async let` have language-specific cancellation/error behavior. Kotlin coroutine builders define parent jobs and supervisor variants. Rust scoped threads permit borrowing because scope joins them; many async runtimes require libraries or application discipline. Use exact supported-version contracts.

## Prerequisites and Retrieval

Retrieve:

- task identity from [Processes, Threads, Tasks, and Fibers](002-processes-threads-tasks-and-fibers.md);
- safety/liveness from [Safety, Liveness, and Progress](004-safety-liveness-and-progress.md);
- deterministic results from [Determinism and Reproducibility](007-determinism-and-reproducibility.md);
- bounded pools from [Thread Pools and Bounded Work Queues](019-thread-pools-and-bounded-work-queues.md);
- future aggregation from [Futures and Promises](033-futures-and-promises.md);
- cooperative response from [Cooperative Scheduling](035-cooperative-scheduling.md); and
- cancellation lifecycle from [Cancellation and Timeouts](036-cancellation-and-timeouts.md).

Retrieval prompt: draw the owner of every started child, the scope that joins it, and the state that remains if a sibling fails first.

## Learning Objectives

After completing this module, a learner can:

1. derive a task tree from a concurrent workflow;
2. specify task-scope admission, closing, cancellation, and join states;
3. distinguish fail-fast, continue, quorum, race, and supervisor failure policies;
4. prove terminal accounting for accepted identities;
5. bound lazy producer invocation, queued work, and cleanup occupancy;
6. preserve secondary failures and deterministic result identity/order;
7. propagate deadlines, cancellation, tracing, and scoped data safely;
8. define legitimate detachment as ownership transfer;
9. test cancellation-insensitive children and nondeterministic failure frontiers; and
10. integrate scopes into shutdown and resource accounting.

## Core Exposition

### Structure is a lifetime tree

Sequential calls nest: a callee normally returns before the caller continues. A structured concurrent scope permits child calls to overlap while retaining the nesting rule that all children finish before the scope exits.

Represent each node with identity, parent, start authority, cancellation source, deadline, failure observer, join owner, and resource lease. Grandchildren belong beneath the child that creates them or are explicitly adopted by the enclosing group. A missing edge is an orphan risk.

Tree shape does not require one OS thread or one executor. Children may run on many workers, actors, devices, or remote operations, but local ownership remains until their terminal/recovery contract is satisfied.

### Scope state machine

OPEN accepts children. CLOSING refuses new admission and waits for accepted children. CANCELLING is a closing mode that has signalled some/all children. JOINED means every accepted identity has one terminal record and required cleanup completed/transferred.

The scope body can fail while children run. That body failure becomes another cause: stop admission, request policy-defined cancellation, join children, then report body and child failures without losing either. Repeated close/cancel must be idempotent.

A destructor/defer that merely drops task handles is not sufficient unless the runtime contract itself cancels and joins them synchronously/asynchronously as required.

### Fork ownership must precede execution

The group must establish identity and ownership before a producer can throw synchronously, start external effects, or return a future. With eager operations, creating all promises and then registering them leaves a gap. Prefer lazy factories or a spawn primitive whose atomic contract registers the child before it runs.

If producer invocation throws, the wrapper records a terminal defect for that accepted identity and applies group policy. No exception may escape before terminal accounting is installed.

### Join means lifecycle completion

Join is not merely waiting for a result future that can settle early. A fail-fast aggregate may reject while siblings remain active. A structured group can announce the decisive failure early internally, but external scope exit waits for every accepted child to terminate or transfer to a named durable owner.

Cancellation request is not join. An insensitive child can delay exit. Therefore group deadlines need escalation and residual-state reporting; forcibly abandoning a child weakens structure unless isolation/durable ownership replaces it.

### Failure policies are semantic choices

**Fail-fast:** first decisive failure closes admission, requests sibling cancellation, joins all, and reports primary plus secondary outcomes.

**Continue/collect:** independent children run and all terminal results are returned.

**Supervisor:** child failure is observed but does not automatically cancel siblings/parent; the supervisor decides restart/escalation.

**Race/first-success/quorum:** enough outcomes determine the public answer; losers are still cancelled and joined.

Policy must state which failures are decisive: expected domain error, cancellation, timeout, panic/defect, or body failure. “One task failed” is not enough.

### Preserve multiple failures

Concurrent tasks can fail before cancellation propagates or while cleaning up. Selecting one as primary by observation order is schedule-sensitive. Preserve stable child identity, error cause, timestamp/phase, and all terminal outcomes. Some languages expose exception groups; others need a typed aggregate.

Do not flatten unknown defects into ordinary domain messages. Cancellation induced by fail-fast should remain distinguishable from an independent child failure. Deterministic reports can sort by source identity while retaining observed completion metadata.

### Terminal accounting

For each accepted child identity, allocate one result slot before start. Terminal wrapper writes exactly once. Final join validates no missing/duplicate slots and reconstructs authoritative counts from records rather than racing live counters.

A useful fail-fast taxonomy is SUCCEEDED, FAILED, CANCELLED_RUNNING, CANCELLED_BEFORE_START, TIMED_OUT, and PANICKED/DEFECT. Choose mutually exclusive categories. “Skipped” must say whether input was accepted; unaccepted proposals should not appear in accepted accounting.

The identity equation catches forgotten children even when the running set becomes empty due to a bookkeeping bug.

### Bounded fan-out is additional structure

Lexical lifetime does not bound the number of children. Spawning one million scoped tasks still retains one million frames/results. Define maximum batch/admission, queue capacity, and active width.

Store inert source values or lazy producers. A fixed worker set invokes at most `k` producers. Calling every producer first and placing a semaphore inside each task bounds a critical region but not frames, sockets, synchronous prefixes, or caller input.

Capacity ownership extends through cleanup. A child does not release its permit when the business result appears if it still holds transport, transaction, or memory that the limit protects.

### Admission and failure race

Fail-fast has an inherently schedule-dependent frontier. A child may start just before another failure closes the group. The durable promise is: after closure linearizes, no new child is intentionally admitted; already-started children are signalled and joined; accepted-but-not-started children receive terminal classification.

Tests should not assert the exact last started source unless the scheduler makes that order deterministic. They should assert no post-close deliberate admission and complete terminal accounting.

### Cancellation propagation

Parent cancellation normally propagates downward. Child cancellation may remain local; child failure may or may not cancel siblings based on policy. Upward propagation is failure reporting, not necessarily cancellation identity.

Every child receives the parent deadline or a narrower deadline. Cancellation reasons should retain the causal chain—parent timeout, sibling failure, body failure, shutdown—without exposing secrets. Repeated signals are idempotent.

Structured cancellation cannot repair a child operation that is unsafe to abandon. The group still needs commit ledgers, late-result disposal, and recovery described in the previous module.

### Context and scoped values

Task trees provide a natural boundary for trace context, logging identity, locale, priority class, and immutable request data. Child context derives from parent and disappears at scope end. Thread-local storage alone may not follow task migration.

Scoped borrowing is stronger: a child can reference stack data only if the language/runtime proves it cannot outlive that data and handles abnormal exit. Rust `thread::scope` is an example for threads. In garbage-collected runtimes, lifetime may remain memory-safe while logical request data leaks into orphan work; structure still matters.

Authorization should use explicit, immutable capability/context rules rather than blindly inheriting all ambient state. A child may need less authority than its parent.

### Result order and completion order

Children finish nondeterministically. APIs may yield results as completed, by fork order, or through individual handles. Decide what callers need.

Live events should carry child identity and sequence/time. Final batch output often preserves source order for reproducibility. Sorting final records does not claim execution order. For streaming consumers, completion order can reduce latency but requires deterministic tie handling only when the product promises it.

### Resource and backpressure interaction

A task scope owns not only tasks but leases: active permits, queue slots, sockets, memory, and downstream quotas. Track proposed, accepted, queued, running, cleaning, and terminal states. Bound each place work accumulates.

If children produce a stream of results faster than the parent consumes them, the result channel also needs capacity/backpressure. Joining workers while ignoring a full result queue can deadlock. The parent must concurrently drain, reserve enough bounded storage, or use direct indexed slots.

### Detachment is ownership transfer

Some work legitimately outlives a request: cache refresh, audit delivery, scheduled job, telemetry flush. Do not call it “fire and forget.” Transfer it before scope exit to a service-level supervisor with identity, bounded admission, credentials/lifetime rules, failure sink, deadline, retry/idempotency, and shutdown join.

If no durable supervisor accepts it, detachment is rejection. A global background set without bounds or error policy only hides the orphan.

### Supervision and restart

Structured concurrency and supervision complement each other. Structure bounds lifetime within a scope; a long-lived supervisor can own service components, classify child exits, and restart under policy.

Restart needs intensity/rate limits, backoff, state reinitialization, and dependency ordering. Repeatedly restarting a deterministic defect creates a failure storm. A restart creates a new child identity/attempt beneath the same logical component; historical outcomes remain visible.

### Deadlines and noncooperative children

Scope exit can be delayed by a child that ignores cancellation or blocks in foreign code. Establish a graceful deadline, then isolate/terminate according to platform policy while preserving residual-resource evidence. In-process forced thread termination is often unsafe.

If the caller must return before an isolated child stops, ownership transfers to a process/container supervisor and the API reports incomplete termination. Claiming the lexical scope simply ended would be false.

### Shutdown is root-scope closure

The process/service has a root task scope. Shutdown stops root admission, closes listeners, signals descendants, drains committed work under deadlines, escalates, and joins/records every child before runtime teardown. Nested scopes make the traversal explicit.

Close dependencies in an order that allows children to finish. Stopping a broker before its request children can receive replies creates shutdown deadlock. Resource ownership graph may refine pure task-tree order.

### Observability and testing

Record scope ID, parent scope, child identity, admission/start/terminal times, attempt, policy, deadline, cancellation cause, outcome, cleanup, and join. Display task trees and oldest runnable/closing children. Final summaries come from terminal records; live gauges are observations.

Deterministic tests control child start and finish. Exercise reverse order, simultaneous failures, body failure, synchronous spawn throw, fail-fast frontier, cancellation-insensitive child, cleanup failure, full queue, parent cancellation, nested scope, detachment transfer, and shutdown. Compare widths one/many; stable identity/accounting should hold even if traces differ.

### Policy evolution and compatibility

Changing a scope from continue to fail-fast, altering which errors are decisive, or changing result order is observable API behavior. Version it deliberately. Compatibility tests should replay mixed outcomes and verify admission frontier claims, terminal categories, error aggregation, context inheritance, and cleanup ownership. Runtime upgrades also need review when preview APIs or cancellation semantics change; a matching method name does not prove an unchanged lifecycle contract.

## Definitions and Notation

Let a scope own accepted child set `A`. Terminal subsets success `S`, failure `F`, cancellation `C`, timeout `T`, and defect `P` are disjoint and cover `A`:

`|A| = |S| + |F| + |C| + |T| + |P|`.

For every child `x in A`, exactly one terminal record exists: `sum_y I[x in y]=1` over terminal categories `y`.

Let queued `Q`, running `R`, and cleaning `K` satisfy configured bounds `|Q|<=q`, `|R|<=r`, `|K|<=k`. A permit protecting occupancy remains held through the relevant cleaning transition.

For parent scope interval `[p_start,p_join]` and child `[c_start,c_terminal]`, structured lifetime requires `p_start<=c_start<=c_terminal<=p_join`, unless ownership is explicitly transferred before parent join.

## Mechanisms, Invariants, or Proof Structure

Audit a task scope in this order:

1. draw parent, child, grandchild, and transferred-supervisor ownership;
2. define OPEN, CLOSING/CANCELLING, and JOINED transitions;
3. allocate stable identity and terminal slot before producer execution;
4. state fail-fast/continue/quorum/supervisor policy and decisive failures;
5. close admission before cancellation/drain and reject later forks;
6. propagate deadline/context/cancellation only through owned edges;
7. bound proposals, accepted queue, active tasks, results, and cleanup;
8. retain all failures and deterministic identity/order without claiming schedule order;
9. make cancellation cuts, commits, late results, and resource leases explicit;
10. join every accepted child or transfer it atomically to a durable supervisor;
11. close nested/root scopes in dependency-aware shutdown order; and
12. test schedule-dependent frontiers using invariant assertions.

The executable model records a fail-fast group with width two. B fails, queued C is cancelled before start, and already-running A succeeds before observing cancellation; all three are still joined and counted.

<!-- bijux-verify: {"id":"structured-task-group-accounting","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"outcomes={'A': 'succeeded', 'B': 'failed', 'C': 'cancelled_before_start'}\nfirst_failure=B\ncancel_requested=True\naccepted=3\nterminal=3\nrunning=0\naccounting_complete=True\njoined=True\n","stderr":""}} -->
```python
accepted = ["A", "B", "C"]
running = ["A", "B"]
queued = ["C"]
outcomes = {}
first_failure = None
cancel_requested = False

outcomes["B"] = "failed"
first_failure = "B"
cancel_requested = True

for child in queued:
    outcomes[child] = "cancelled_before_start"
queued = []

outcomes["A"] = "succeeded"
running = []

ordered = {child: outcomes[child] for child in accepted}
print(f"outcomes={ordered}")
print(f"first_failure={first_failure}")
print(f"cancel_requested={cancel_requested}")
print(f"accepted={len(accepted)}")
print(f"terminal={len(outcomes)}")
print(f"running={len(running)}")
print(f"accounting_complete={set(accepted) == set(outcomes)}")
print("joined=True")
```

Limitations: this predetermined single-thread trace does not run tasks or model concurrency, timing, races, exception groups, cancellation delivery, cleanup, resource limits, nested scopes, deadlines, transfer, blocking, or runtime APIs. It establishes one accounting example only.

## Alternatives and Trade-Offs

**Sequential execution** has the simplest lifetime/failure behavior but cannot overlap independent waits or parallel work.

**Ad hoc spawn plus handles** can be made correct if every path records and joins handles; a scope packages and enforces that discipline.

**Structured task group** exposes nested lifetime and aggregate policy. It can delay return while cancellation-insensitive children terminate.

**Actor/service supervisor** owns long-lived components and restart policy. It is structured at a broader lifecycle than one lexical request.

**Fail-fast** reduces wasted dependent work but can discard useful independent work and has a schedule-dependent frontier. **Continue** maximizes accounting but may spend resources after enough failures make the batch useless.

**Exception groups** preserve concurrent causes but complicate handling APIs. **Primary-plus-suppressed** is simpler but can bias by observation order.

**Task per item** isolates identity but can retain too many frames. **Fixed scoped workers** preserve structure and bounds, at the cost of explicit work distribution.

**Detached transfer** supports durable background work but needs a separate supervisor and cannot borrow request lifetime.

## Failure Modes and Misconceptions

- “Awaiting `all` is structured concurrency.” Early aggregate settlement may leave children running.
- “Lexical scope bounds fan-out.” It bounds lifetime, not child count.
- “Cancel siblings means they stopped.” The scope must still join acknowledgement/cleanup.
- “Fail-fast produces exactly one failure.” Siblings can fail concurrently or during cleanup.
- “The first source child is the first failure.” Observation order is schedule-dependent.
- “A task group makes I/O cancellation-safe.” Operation protocols still decide partial effects.
- “Dropping handles joins tasks.” Many runtimes detach or merely lose observation.
- “One semaphore bounds everything.” Inputs, queued frames, results, and cleanup need bounds.
- “Supervisor means ignore child failure.” It means a named owner classifies and acts.
- “Borrowed data is safe because work is nearby.” Only enforced lifetime/join makes it safe.
- “Structured code cannot leak context.” Overbroad ambient inheritance still leaks authority.
- “Scope exit may abandon a stuck child silently.” That violates no-orphan claims unless ownership transfers.
- “Final result order proves execution order.” Reports can be source-sorted after nondeterministic execution.
- “Background work is harmless detachment.” It needs durable ownership and shutdown.

## Worked Examples

### Example 1

A request forks user and permissions lookups in a task group. Both must succeed. Permissions fails, so policy cancels user lookup, joins it, preserves both terminal records, and returns failure only after cleanup. Returning at first rejection could leave a connection in use after request context expires.

### Example 2

A batch calls all 100,000 producers before adding their futures to a scope. Synchronous prefixes have already allocated sockets. Replace with bounded input and lazy factories; scoped workers invoke at most `k`. Structure must precede execution.

### Example 3

Fail-fast width two starts A and B while C waits. B fails; C becomes cancelled-before-start; A succeeds before cancellation. A test demanding A be cancelled is brittle. Assert closure, no later admission, one outcome per accepted child, and joined cleanup.

### Example 4

Two children fail nearly simultaneously. The runtime chooses one as the triggering failure, but the group retains both with stable IDs and phases. A deterministic report sorts by source ID while a trace preserves observed times. Logging only the first destroys debugging evidence.

### Example 5

A parent body throws while children run. The scope treats body failure as a cancellation cause, closes admission, cancels/joins children, and reports body plus child/cleanup failures. An ordinary `finally` that drops handles is insufficient if handles detach.

### Example 6

A child holds a permit through business completion but performs asynchronous close after releasing it. The group starts a replacement and real occupancy exceeds the bound. Retain the lease until protected cleanup ends; report cleanup failure in the child terminal record.

### Example 7

A cache refresh must outlive an HTTP request. Before request scope exits, transfer a value-only job to a bounded application supervisor. It receives service credentials, deadline, idempotency key, failure sink, and shutdown ownership; it cannot retain request-local borrowed state.

### Example 8

A result channel has capacity one. Workers attempt to send results while the parent waits for workers to join before draining; all block. Drain concurrently or store directly into bounded indexed slots. Task count bounds do not eliminate result-path backpressure.

### Example 9

A child ignores cancellation in a native call. The scope deadline expires. If the call is in an isolated worker process, ownership transfers to a process supervisor that terminates/joins it and reports residual effects. Pretending normal lexical exit occurred would falsify lifetime evidence.

### Example 10

A surgical robot planning scope races three trajectory analyzers and uses first-success. Cancelling/joining losing software tasks does not establish that commands already sent to hardware were revoked. Production needs command ownership, safe-state interlocks, verified cancellation cuts, bounded termination, independent sensing, and failure aggregation. Named clinical, robotics, controls, real-time, functional-safety, cybersecurity, human-factors, and regulatory reviewers must approve evidence; this chapter cannot.

## Cross-Program Connections

- **Programming-language semantics:** scope and effect systems can make task lifetime/cancellation statically visible.
- **Operating systems:** process/thread scopes, signals, and forced termination constrain join guarantees.
- **Distributed systems:** remote children need durable operation identity when local lexical lifetime ends.
- **Software architecture:** service supervisors own legitimate long-lived background components.
- **Data systems:** task groups around transactions must respect commit and connection lifetimes.
- **Security:** child capabilities should narrow; bounded fan-out limits denial of service.
- **Reliability:** failure aggregation, restart intensity, and root shutdown become explicit.
- **Observability:** task trees restore causal context across concurrent branches.

## References

1. OpenJDK. “JEP 525: Structured Concurrency (Sixth Preview).” <https://openjdk.org/jeps/525>.
2. Python Software Foundation. “asyncio Task Groups.” <https://docs.python.org/3/library/asyncio-task.html#task-groups>.
3. Swift Project. “SE-0304: Structured Concurrency.” <https://github.com/swiftlang/swift-evolution/blob/main/proposals/0304-structured-concurrency.md>.
4. Kotlin Foundation. “Coroutine Scope and Structured Concurrency.” <https://kotlinlang.org/docs/coroutines-basics.html#coroutine-scope-and-structured-concurrency>.
5. Kotlin Foundation. “Exception Handling and Supervision.” <https://kotlinlang.org/docs/exception-handling.html>.
6. Rust Project. “std::thread::scope.” <https://doc.rust-lang.org/std/thread/fn.scope.html>.
7. Go Project. “Package errgroup.” <https://pkg.go.dev/golang.org/x/sync/errgroup>.
8. Trio Project. “Nurseries and Spawning.” <https://trio.readthedocs.io/en/stable/reference-core.html#nurseries-and-spawning>.
9. Nathaniel J. Smith. “Notes on Structured Concurrency, or: Go Statement Considered Harmful.” <https://vorpus.org/blog/notes-on-structured-concurrency-or-go-statement-considered-harmful/>.
10. Martin Sústrik. “Structured Concurrency.” <https://250bpm.com/blog:71/>.

## Exercises

### Exercise 1

Define OPEN, CLOSING/CANCELLING, and JOINED for a task group. Which transition establishes that no later child may be admitted?

### Exercise 2

For fail-fast width three over ten lazy jobs, define stable guarantees after job 4 fails and identify schedule-dependent facts.

### Exercise 3

Design terminal accounting that preserves domain failures, defects, running cancellation, before-start cancellation, timeouts, cleanup failure, and source order.

### Exercise 4

A request must enqueue audit work that outlives it. Specify an ownership transfer that remains structured at service scope.

### Exercise 5

An air-traffic conflict detector races three algorithms and returns first-success, then drops loser handles while they can still publish advisories. Diagnose the design and specify required human evidence.

## Answers to the Exercises

### Answer 1

OPEN accepts and registers children before start. Closing linearizes the refusal of new admission; normal body completion enters CLOSING, while failure/cancellation commonly enters CANCELLING and signals policy-selected children. Both drain accepted identities. JOINED requires exactly one terminal record and required cleanup/transfer for every accepted child. The atomic OPEN-to-closing transition, not first cancellation callback, establishes the admission boundary.

### Answer 2

Stable guarantees: at most three active producers under the declared resource definition; closure prevents intentional admission after failure linearizes; accepted queued jobs become before-start cancellation; running siblings receive cancellation; every accepted identity is joined and terminally classified; all failures are retained. Schedule-dependent facts include which other jobs started before closure, whether running jobs succeed/fail/cancel, which failure is observed first in a tie, and completion order. Tests assert invariants, not one frontier.

### Answer 3

Allocate a source-indexed slot at acceptance. A child wrapper catches synchronous producer throw, awaited domain failure, panic-like defect, timeout, policy cancellation, and cleanup failure, and writes once. Model cleanup as a field/secondary cause or distinct terminal type according to product semantics, never overwrite the primary silently. Before-start cancellation is written by the closing scheduler. Join validates every slot, category disjointness, and `accepted=terminal`; reports sort by source index while retaining observed timestamps.

### Answer 4

Before request exit, submit a value-owned audit record to a bounded service supervisor through an acknowledged admission operation. The supervisor assigns stable identity, durable/idempotent storage if required, its own credential/context, deadline/retry policy, failure sink, and task handle. Rejection remains the request's problem. Acceptance atomically transfers ownership; request-local borrows/tokens do not cross. Service shutdown stops admission, drains/cancels according to audit policy, and joins/reports every accepted record.

### Answer 5

Dropping handles loses ownership; loser algorithms may publish conflicting advisories after the public answer, so the operation is neither joined nor single-authority. Use a scope that assigns candidate identities, chooses one authoritative result under policy, revokes publication capability from losers, requests cancellation, and joins/isolates them. Production evidence requires named air-traffic-domain, algorithms, human-factors, real-time, distributed-systems, functional-safety, cybersecurity, operations, verification, and regulatory reviewers; hazard/requirements traceability; scenario, simulation, timing, race, fault-injection, and operator-workload evidence; independent validation; applicable-standard assessment; and signed residual-risk acceptance. This chapter supplies no operational approval.
