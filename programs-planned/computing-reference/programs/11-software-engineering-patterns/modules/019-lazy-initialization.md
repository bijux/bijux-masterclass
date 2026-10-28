---
module_id: SEPAT-019
program: Software Engineering: Patterns
level: 1
module_number: 19
title: Lazy Initialization
status: complete
last_verified: 2026-08-28
---

# Lazy Initialization

## One-Page Review

### Governing question

When should construction be deferred until demand, and how must concurrency, publication, recursion, failure, cancellation, invalidation, latency, and lifecycle be specified so the first caller does not become an accidental startup system?

### Essential definitions

- **Lazy Initialization** defers creation or computation until a value is first demanded.
- **eager initialization** performs the work at a planned construction or startup boundary.
- A **lazy cell** records uninitialized, initializing, ready, and failure state around a factory.
- **memoization** caches a function result by arguments; one-value laziness is a special, narrower case.
- **safe publication** ensures observers see all effects of completed initialization according to the language memory model.
- **single-flight** coalesces concurrent demand so one attempt runs while other callers await its result.
- **failure caching** retains an initialization error; **retry policy** permits a later bounded attempt.
- **reentrant initialization** occurs when a factory directly or indirectly demands its own lazy value.
- **invalidation** retires a ready value and establishes which generation future callers may observe.
- **warming** deliberately triggers lazy paths before traffic or ahead of predicted demand.

### Central model, mechanism, or theorem

Represent a lazy cell as a state machine:

$$
U \rightarrow I \rightarrow R(v),\qquad I\rightarrow F(e)\;\text{or}\;U.
$$

Only one initializer may own state $I$. A value is published only after complete successful construction, with $complete(v)\;hb\;read(v)$ for every observer. Failure policy chooses cached terminal $F(e)$, reset to $U$, or bounded retry with time/backoff conditions. For use probability $p$, initialization cost $C_i$, and per-access lazy overhead $C_a$, a crude expected-work comparison is eager $C_i$ versus lazy $pC_i+nC_a$; it excludes tail latency, contention, retained memory, failure timing, and operational risk, so measurement and service objectives govern the decision.

### Critical invariants

- No caller observes a partially constructed value or publication without the required memory ordering.
- At most one active attempt exists per key when single-flight semantics are claimed.
- Recursion is detected or deliberately supported without returning partial state or deadlocking silently.
- Failure caching/retry, backoff, deadlines, cancellation, and error identity are explicit.
- A canceled waiter does not necessarily cancel shared initialization; ownership policy decides.
- Readiness matches required eager/lazy dependencies and does not claim a path ready before required validation.
- Invalidation creates coherent generations; old values remain valid for existing holders or are fenced.
- Shutdown owns initialized resources, handles never-initialized cells, and rejects initialization after drain begins.

### Common failures

Common failures include unsafe check-then-create, double-checked locking without correct atomic rules, publishing the reference before construction finishes, hidden blocking I/O on an ordinary getter, first-request latency spikes, thundering-herd retry after failure, caching transient errors forever, retrying permanent errors forever, deadlock from recursive initialization, cancellation of one waiter aborting work needed by others, stale values after configuration change, leaked lazy resources omitted from shutdown, and lazy-loading domain data after its session/transaction has closed.

### Compact example

A finite lazy cell holds a catalog factory. Construction count remains zero until first access; two accesses receive one identical immutable value. A second cell uses explicit retry-on-failure: the first attempt raises, state returns to uninitialized, and the second succeeds. The example is sequential and proves no thread-safety or latency property.

### Connections

[SEPAT-016](016-singleton-and-its-hidden-global-state.md) separates lazy one-time construction from global access, [SEPAT-017](017-object-pool.md) compares warming and on-demand resource creation, and [SEPAT-018](018-dependency-injection-as-a-creation-pattern.md) uses providers at explicit graph boundaries. Lazy state also connects to [Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md), [Database Engineering](../../18-database-engineering/ROADMAP.md), and [Software Delivery and Reliability Engineering](../../14-software-engineering-software-delivery-and-reliability-engineering/ROADMAP.md).

## Governing Question

Does deferral remove enough unused work or move enough cost to the right boundary to justify a new concurrent state machine and a demand-time failure mode?

“Create it only if needed” sounds local. In production it changes when configuration is validated, when credentials are read, which request pays setup latency, how failures affect readiness, how many threads race, and whether shutdown knows the resource exists. Lazy Initialization is therefore lifecycle policy, not a boolean optimization.

## Why This Matters

Large applications may have optional formats, plugins, models, caches, indexes, or remote clients that many processes never use. Eagerly building all of them wastes startup time and memory. Laziness can be a major improvement when use probability is low or initialization depends on a context unavailable at startup.

But deferral transfers work and risk. If a TLS client, schema compiler, or model takes seconds to initialize, the first user sees it. If thousands of callers arrive together, broken coordination can perform the work thousands of times or block an entire execution pool. Correctness requires a precise state machine; operational quality requires deciding where latency and failure belong.

## Prerequisites and Retrieval

You should understand construction, providers, threads/tasks, locks and atomics, memory visibility, futures/promises, caching, deadlines, and resource lifecycle. Retrieve these facts:

1. Reference equality does not imply that a value was safely published.
2. Exactly-once attempt, at-most-one concurrent attempt, and eventually-successful value are different guarantees.
3. Failure can be permanent, transient, caller-specific, or cancellation-specific.
4. A getter that performs I/O is an effectful operation even if its syntax looks like a field read.
5. Cache invalidation and lazy initialization become the same generation problem once values can change.
6. Startup speed is not useful if required functionality fails only after traffic admission.

## Learning Objectives

After completing this module, you should be able to:

- justify eager, lazy, warm, or hybrid initialization from use and service evidence;
- specify the lazy-cell state machine and publication guarantees;
- distinguish once, single-flight, memoization, caching, and deferred provider semantics;
- design failure, retry, recursion, timeout, and cancellation behavior;
- prevent first-use latency and dependency-outage herds;
- implement coherent invalidation and configuration generations;
- integrate lazy resources with readiness, observability, and shutdown;
- evaluate language/runtime primitives instead of hand-rolling unsafe coordination.

## Core Exposition

### Decide what is being deferred

Deferral can target allocation, parsing, network connection, authentication, index construction, file mapping, plugin loading, or a whole object graph. State the operation and its effects. A cheap wrapper whose first method opens a socket is not truly initialized at wrapper construction.

Also state the key. Is there one value per process, tenant, request, locale, model version, or configuration generation? A “single lazy value” often becomes an unbounded keyed cache accidentally.

### Choose the demand boundary

The first demand should be an explicit effectful boundary when initialization can block or fail. Prefer `load`, `acquire`, or an asynchronous result over a property getter that surprises callers with seconds of I/O.

Propagate deadline, cancellation, trace context, and classified failure. Do not let library default timeouts exceed the request budget.

### State machine

Begin in `uninitialized`. One caller atomically becomes initializer and changes the state to `initializing`. Concurrent callers either wait, share a future, receive “in progress,” or use a stale value according to policy.

Success publishes a complete value then transitions to `ready`. Failure transitions to cached `failed` or back to `uninitialized` under retry policy. Shutdown transitions the owner to `draining/closed`; later demand must not create a resource that nobody will close.

### Safe publication

The value reference must not become visible before all constructor writes and required side effects complete. Use documented language primitives: class initialization, one-time cells, `call_once`, atomics with correct ordering, or a synchronized future.

Do not improvise double-checked locking from intuition. Correctness varies by language and version and includes both atomic reference access and ordering of object-field writes.

### Single-flight and waiting

One active initializer per key avoids duplicate expensive work. Waiters share completion but retain their own deadlines. A waiter timing out should detach without corrupting the shared attempt.

Who owns cancellation? If the first caller's cancellation aborts shared work, later callers may fail spuriously. Common policies let initialization continue while any interested waiter remains, or give the cell/root an independent lifecycle context. State it explicitly.

### Failure policy

Cache permanent errors such as invalid static configuration until configuration generation changes. Retry transient dependency failures with bounded backoff and jitter. Do not use a single undifferentiated exception for both.

An exactly-once primitive may poison after panic/exception, retry, or expose a permanent erroneous state. Read its specification. If business needs differ, wrap the primitive with an explicit, tested policy rather than assuming behavior.

### Recursive initialization

Factory A may demand lazy B, whose factory demands A. A non-reentrant lock deadlocks; a runtime may return partially initialized state or signal recursion; a future may await itself.

Detect cycles during graph validation where possible. At runtime track initializer ownership and fail with a causal path. Redesign by extracting common data, separating phases, or passing a callback that is used only after both values are ready.

### Latency and warming

Measure initialization latency distribution, not just its mean. If the path is required for common traffic, eager initialization or pre-readiness warming makes failure and latency predictable. If rarely used, lazy demand with a distinct service objective may be better.

Warm in a bounded, observable way. Starting every replica simultaneously can create a cache/database/model-download stampede. Coordinate rollout, cap concurrency, add jitter, and respect downstream budgets.

### Readiness semantics

Required dependencies must be validated before readiness even if their implementation uses lazy internal allocation. Optional features can report “not initialized,” “warming,” “ready,” or “failed” separately.

Never mark the whole service healthy because the process starts while every essential lazy path remains untested. Synthetic probes can exercise representative paths, but their successful past execution does not guarantee future availability.

### Invalidation and generations

If a value never changes, a one-time cell is enough. Configuration reload introduces generations. Build generation $g+1$ independently, validate it, atomically route new callers to it, allow holders of $g$ to finish, then close it.

Clearing a shared pointer in place can race active users and trigger duplicate initialization. Use immutable generation handles and ownership counts or an explicit drain protocol.

### Lazy domain loading

ORM lazy loading defers data access behind navigation/property access. It can produce N+1 queries, demand I/O after the session closes, or make serialization trigger database calls. Query plans and transaction boundaries become invisible.

Prefer explicit fetch plans at application boundaries when latency, consistency, or transaction scope matters. Lazy proxies are useful only when their I/O and ownership semantics remain visible and measured.

### Resource lifecycle

A lazy value may own files, sockets, pools, threads, or memory mappings. The composition root registers the cell as an owner. On shutdown, it closes the value if ready, handles initialization in progress according to deadline, and does nothing for never-created values.

Avoid finalizers as the primary plan. Make closure idempotent and prohibit post-close initialization.

### Observability

Record state, attempts, successes, failures by bounded class, recursion detection, active/waiting callers, initialization duration, first-use latency, cache/generation age, invalidations, stale holders, warm-up outcome, and shutdown result.

Trace which request triggered demand without attaching unbounded caller identities to metrics. Alert on repeated retries, long initialization, synchronized fleet attempts, or essential paths never warmed before traffic.

## Definitions and Notation

Let state $S_t\in\{U,I,R(v),F(e),D,C\}$ mean uninitialized, initializing, ready, failed, draining, or closed. Let attempt $a_g$ belong to configuration generation $g$. `owner(a)` is the one initializer; $W_a$ is its waiter set.

For safe publication:

$$
complete(a_g,v)\;hb\;observe_c(R_g(v))\quad\text{for every successful caller }c.
$$

For one active attempt per key $k$:

$$
|\{a: active(a)\land key(a)=k\}|\le 1.
$$

Let $p$ be probability of use, $C_i$ initialization cost, $C_a$ lazy access overhead, and $n$ access count. The estimate $pC_i+nC_a$ is only a screening model; real decisions require latency distributions, concurrency, memory, failure, and operational evidence.

## Mechanisms, Invariants, or Proof Structure

### Safety argument

Assume state changes are atomic under a documented synchronization protocol. Only a successful owner stores $v$, and it performs the release/publication transition after complete construction. Readers acquire/await the ready transition before reading. Then no reader can observe $v$ through the cell before construction happens-before its read. This proof sketch does not cover objects that leak themselves from their constructors.

### Failure transition

On failure, the owner records a classified error before waking waiters. Cached policy transitions to $F(e)$; retry policy atomically returns to $U$ with attempt/backoff metadata. No waiter may both consume the failed attempt and silently become a new owner without reevaluating its deadline and policy.

### Generation transition

Publishing generation $g+1$ changes only the routing pointer for new acquisitions. Existing handles pin $g$. Therefore closure of $g$ occurs only after it is unpublished and its holder count reaches zero, preventing use-after-close under those assumptions.

### Executable sequential model

<!-- bijux-verify: {"id":"lazy-state-and-retry","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"deferred=True\nsame-instance=True\nbuilds=1\nretry-value=ready\nattempts=2\n","stderr":""}} -->
```python
class LazyCell:
    def __init__(self, factory, cache_failure=True):
        self.factory = factory
        self.cache_failure = cache_failure
        self.state = "uninitialized"
        self.value = None
        self.error = None

    def get(self):
        if self.state == "ready":
            return self.value
        if self.state == "failed":
            raise self.error
        if self.state == "initializing":
            raise RuntimeError("recursive initialization")
        self.state = "initializing"
        try:
            value = self.factory()
        except Exception as error:
            self.error = error
            self.state = "failed" if self.cache_failure else "uninitialized"
            raise
        self.value = value
        self.state = "ready"
        return value


builds = []

def build_catalog():
    builds.append("build")
    return ("patterns", "architecture")


catalog = LazyCell(build_catalog)
deferred = builds == []
first = catalog.get()
second = catalog.get()

attempts = []

def transient_factory():
    attempts.append("attempt")
    if len(attempts) == 1:
        raise RuntimeError("temporary")
    return "ready"


retrying = LazyCell(transient_factory, cache_failure=False)
try:
    retrying.get()
except RuntimeError:
    pass

print(f"deferred={deferred}")
print(f"same-instance={first is second}")
print(f"builds={len(builds)}")
print(f"retry-value={retrying.get()}")
print(f"attempts={len(attempts)}")
```

The run proves deferral, one successful stored identity, one build, and explicit retry after one classified toy failure in a sequential trace. It deliberately provides no synchronization, async cancellation, clock/backoff, invalidation, or resource closing.

## Alternatives and Trade-Offs

**Eager initialization** pays cost and exposes failure at startup. Prefer it for required, bounded, predictable resources whose readiness matters.

**Background warming** overlaps startup or predicted demand with construction. It needs ownership, capacity, cancellation, and readiness semantics.

**Per-call construction** avoids cached history and invalidation when construction is cheap and values are short-lived.

**Memoization/cache** stores results per input key and needs eviction, capacity, and key correctness. Do not disguise an unbounded cache as a lazy field.

**Object Pool** reuses multiple leased instances; a lazy cell commonly stores one value. Pool creation may itself be lazy.

**Proxy/virtual proxy** preserves an interface while deferring a target, but can hide I/O and failure. An explicit provider/future is clearer when effects matter.

**Generated/static data** moves computation to build time, reducing runtime failure at the cost of artifact size and regeneration discipline.

Choose based on probability of use, latency placement, resource cost, failure ownership, and lifecycle—not fashion.

## Failure Modes and Misconceptions

- **“Lazy means faster.”** It may only move cost to a more expensive latency path.
- **“A null check is sufficient.”** Concurrent publication and duplicate attempts require synchronization.
- **“Exactly once means eventual success.”** A single failed attempt may poison the value permanently.
- **“All failures should retry.”** Invalid configuration can create endless storms.
- **“The first caller owns cancellation.”** Shared demand needs independent ownership policy.
- **“A getter is harmless.”** Lazy getters can block, allocate, authenticate, or perform network I/O.
- **“A successful ping makes the lazy value ready forever.”** Health and credentials can change immediately.
- **“Clearing the field reloads safely.”** Active holders and competing rebuilds need generation control.
- **“Lazy ORM fields are just collections.”** Access can issue queries outside expected transaction/latency boundaries.
- **“Unused means no lifecycle.”** In-progress or initialized resources still require shutdown ownership.

## Worked Examples

### Example 1

A desktop editor defers a rarely used export codec. The explicit `load_export_codec` operation reports progress and errors; common editing startup avoids the cost. **Conclusion:** Low use probability and an explicit UX boundary support laziness.

### Example 2

An API lazily opens its mandatory database pool on the first request. The first request times out and readiness had reported healthy. The pool is moved to bounded startup before traffic. **Conclusion:** Required dependency failure belongs before readiness.

### Example 3

Twenty threads request a compiled schema. A one-time cell performs one compilation and safely publishes the immutable result; waiters retain individual deadlines. **Conclusion:** Single-flight and waiter policy are separate from caching.

### Example 4

Configuration factory A requests B, and B requests A. Runtime ownership tracking reports `A -> B -> A` rather than deadlocking. The graph is redesigned around shared parsed configuration. **Conclusion:** Recursive lazy creation often reveals a dependency cycle.

### Example 5

A plugin signature is invalid. The error is cached for configuration generation 7 and retried only when generation 8 arrives. **Conclusion:** Permanent failure should not become a tight retry loop.

### Example 6

A model server downloads weights lazily on each replica after a traffic spike. The fleet overwhelms artifact storage. Deployment now warms a bounded cohort with jitter before routing. **Conclusion:** Per-process safety does not prevent distributed initialization storms.

### Example 7

An ORM serializer walks a lazy relationship after the transaction closes, causing a runtime error; when kept open, it causes hundreds of queries. An explicit projection/fetch plan replaces it. **Conclusion:** Hidden lazy I/O obscures consistency and cost.

### Example 8

Credential rotation builds client generation 12 while generation 11 serves existing leases. New calls switch only after authentication succeeds; old leases drain before close. **Conclusion:** Invalidation is a versioned ownership transition.

### Example 9

A canceled waiter detaches from shared index construction. Other waiters remain, so the root-owned initialization continues. If the final waiter leaves, policy may cancel only if partial artifacts are safely cleaned. **Conclusion:** Cancellation requires an explicit owner and cleanup contract.

### Example 10

An autonomous-vehicle stack proposes lazy calibration loading after motion begins. The design is rejected: required calibration is authenticated, validated, bounded in time, and ready before actuation, with independent fail-safe enforcement. **Conclusion:** Startup optimization cannot move a safety prerequisite past its hazard boundary.

## Cross-Program Connections

- **Concurrent Programming:** locks, atomics, futures, happens-before, cancellation, and reentrancy determine safety.
- **Programming Languages:** class initialization and standard once/lazy primitives define failure and recursion semantics.
- **Database Engineering:** lazy relationships, transaction scope, connection acquisition, and query plans affect correctness and latency.
- **Distributed Systems:** replica fleets create stampedes, retries, stale generations, and dependency load.
- **Cloud and Platform Engineering:** startup, readiness, autoscaling, rollout cohorts, and configuration rotation interact with warming.
- **Performance Engineering:** use probability, cold latency, contention, retained memory, and tail distributions justify decisions.
- **Security Engineering:** deferred authentication, secret loading, signed plugins, and generation fencing control authority.
- **Testing and Quality:** deterministic state-machine, concurrency, failure, cancellation, and lifecycle tests provide different evidence.
- **Reliability Engineering:** thundering herds, backoff, circuit breaking, readiness, and shutdown govern failure behavior.
- **Systems Engineering:** safety prerequisites and real-time deadlines constrain permissible deferral.

## References

1. Martin Fowler, [“Lazy Load”](https://martinfowler.com/eaaCatalog/lazyLoad.html), in *Patterns of Enterprise Application Architecture*, accessed 2026-08-28. Describes lazy initialization, virtual proxy, value holder, and ghost approaches for deferred data loading.
2. Oracle, [*The Java Language Specification*, §12.4.2](https://docs.oracle.com/javase/specs/jls/se22/html/jls-12.html#jls-12.4.2), Java SE 22, accessed 2026-08-28. Specifies synchronized class initialization, recursion, completion, waiting, and erroneous-state behavior.
3. The Rust Project Developers, [`std::sync::LazyLock`](https://doc.rust-lang.org/std/sync/struct.LazyLock.html), accessed 2026-08-28. Documents thread-safe first-use initialization and its force, poison, and destructor considerations.
4. The Go Authors, [`sync.Once`, `OnceValue`, and `OnceValues`](https://pkg.go.dev/sync), accessed 2026-08-28. Documents once-only execution, memory-model synchronization, panic replay for value helpers, and return-value caching.
5. Bjarne Stroustrup and Herb Sutter, editors, [*C++ Core Guidelines*](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines), rules I.2, I.3, and I.22, accessed 2026-08-28. Discusses global initialization order, function-local static initialization, hidden state, races, and destruction concerns.
6. Mark Seemann and Steven van Deursen, *Dependency Injection Principles, Practices, and Patterns*, Manning, 2019, ISBN 978-1-61729-473-0. Provides explicit provider, scope, composition-root, and lifetime context.
7. Martin Kleppmann, *Designing Data-Intensive Applications*, O'Reilly, 2017, ISBN 978-1-4493-7332-0. Provides cache, replication, consistency, failure, and distributed coordination context for generation and stampede analysis.

## Exercises

### Exercise 1

Formalize the executable `LazyCell` state transitions and explain precisely what it proves and fails to prove. Add a cached-failure trace without conflating it with retry-on-failure.

### Exercise 2

Design a thread-safe async lazy cell with single-flight, waiter deadlines, cancellation, recursion detection, classified retry with backoff, and shutdown. State linearization points and ownership assumptions.

### Exercise 3

Given initialization cost 800 ms, access overhead 2 microseconds, 5% process use probability, and 400 accesses when used, compute the simple expected-work comparison, then explain why it cannot decide production placement.

### Exercise 4

Design a generation-safe reload for a lazily built tenant routing table under concurrent requests, configuration errors, bounded memory, and rollback.

### Exercise 5

An unfamiliar radiation-therapy controller proposes lazily loading treatment calibration on first beam command. Critique the proposal and specify evidence and named human review required for any deployment claim.

## Answers to the Exercises

### Answer 1

The first cell starts `U`. Construction count is zero. First `get` performs `U -> I -> R(tuple)` and stores the complete tuple. Second `get` observes `R` and returns the identical reference without another factory call. The retry cell performs `U -> I -> U` after its first exception because `cache_failure=False`, then `U -> I -> R("ready")`.

For cached failure, create a factory that always raises a specific exception and a default `LazyCell`. First access performs `U -> I -> F(e)`; second access raises the stored `e` without calling the factory again. Assert one attempt and, if the language permits meaningful identity comparison, the intended error identity policy. The sequential model proves no atomicity, memory ordering, concurrent single-flight, waiter behavior, timing, backoff, cancellation, invalidation, resource cleanup, or constructor non-leakage.

### Answer 2

Protect `(state, generation, attempt)` with an atomic state machine or mutex. The linearization point for ownership is the successful transition `U -> I(attempt_id, owner_context)`. The owner runs the async factory outside the lock. Success constructs fully, then under synchronization publishes `R(g,value)` and completes a shared future; the release/complete operation synchronizes with awaiting readers. Failure publishes a classified attempt result, then policy atomically chooses `F(g,error)` or `U(next_allowed_time,attempt_count)` before waking waiters.

Each waiter registers with its own deadline and atomically detaches on timeout. Detaching does not cancel the attempt while other waiters or the root own it. If policy cancels when interest reaches zero, the factory must accept cancellation and remove partial resources before state can return to `U`. Track initialization call-chain tokens; a demand for the same cell/attempt reports a recursion path. Backoff and jitter are cell-owned, bounded by error class and generation. Shutdown atomically changes to `D`, rejects new owners/waiters, cancels or awaits the current attempt to a deadline, closes a ready value exactly once, then publishes `C`. Test linearizability/model traces and stress/fault behavior.

### Answer 3

Eager simple cost is 800 ms per process. Lazy expected initialization cost is $0.05\times800=40$ ms. When used, 400 accesses cost $400\times2$ microseconds = 800 microseconds = 0.8 ms; averaged over all processes that overhead is 0.04 ms if accesses occur only in the 5% used case. Under that simplified interpretation, expected lazy work is about 40.04 ms versus 800 ms.

This does not place the cost. A used process's first caller still pays roughly 800 ms; concurrent callers contend; initialization can fail; access overhead distribution and memory differ; use may correlate with peak load; fleet replicas may stampede; readiness and service objectives may require prevalidation; and resource lifetime/shutdown may dominate. Measure use distribution, cold/warm tail latency, concurrency, downstream capacity, failure/retry behavior, startup budget, memory, and user-visible objectives. Hybrid bounded warming may be preferable.

### Answer 4

Key cells by `(tenant_id, config_generation)` under a global bounded cache. Parse and validate signed configuration before eligibility. A miss starts at most one build for that key; waiters share it with individual deadlines. A failed new generation is cached as a classified configuration error and does not displace the last known good generation.

After generation $g+1$ builds and passes route invariants, atomically update that tenant's routing handle for new requests. Each request pins its selected immutable generation until completion. Retire $g$, close it only when unpublished and holder count is zero, and enforce global/per-tenant memory and build-concurrency limits with eviction of safe retired/idle entries. Rollback republishes a still-valid prior generation through the same transition, never mutates a table under readers. Test concurrent first access, bad config, delayed build, timeout, cancellation, duplicate event, rollback, tenant deletion, memory pressure, and process restart.

### Answer 5

Calibration is a precondition for safe dose delivery, not an optional feature whose latency/failure belongs on the first beam command. Lazy loading can expose missing, stale, unauthenticated, wrong-patient/machine, wrong-unit, or partially parsed calibration after motion/beam preparation and can violate real-time bounds. The proposal is rejected unless “lazy” only means preloading within a controlled pre-treatment state before any hazardous action and readiness remains false until validation completes.

Bind calibration to patient, approved treatment plan, machine identity, hardware/software/configuration generation, units, validity interval, and signed provenance. Validate bounds, geometry, checksums/signatures, compatibility, and independent dose constraints. Publish an immutable generation only after complete verification; fence old generations; fail safe on ambiguity; and enforce independent hardware/firmware dose, position, interlock, and emergency-stop limits. No demand path may silently retry into beam enablement.

Evidence includes requirements and hazard traceability, dimensional and numerical recomputation against an independent implementation, formal/state analysis where tractable, worst-case timing, static analysis, independent code/proof review, cybersecurity/provenance assessment, simulator and hardware-in-the-loop tests, corrupted/stale/wrong-patient/partial-file/failure injection, calibration laboratory evidence, end-to-end treatment workflow and human-factors validation, and controlled release under applicable medical/radiation regulations. Named radiation oncologists, medical physicists, dosimetrists, radiation-therapy technologists, controls/real-time engineers, functional-safety engineers, cybersecurity, human-factors, quality, regulatory, operations, and independent verification authorities must approve. Repository validation proves no treatment safety or clinical suitability.
