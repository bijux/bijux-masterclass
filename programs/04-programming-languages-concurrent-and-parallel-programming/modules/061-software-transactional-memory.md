---
module_id: CONPAR-061
program: Programming Languages: Concurrent & Parallel Programming
level: 2
module_number: 61
title: Software Transactional Memory
status: complete
last_verified: 2026-08-29
---

# Software Transactional Memory

## One-Page Review

### Governing question

How can a runtime make a group of shared-memory reads and writes appear atomic while preserving consistent speculative execution, composability, useful progress, and safe interaction with effects that cannot be rolled back?

### Essential definitions

- A **transaction** is a dynamic execution that tentatively reads and writes transactional locations, then commits all its writes atomically or aborts without publishing them.
- A **read set** and **write set** record the locations observed and tentatively changed by a transaction.
- A **conflict** exists when concurrent transactions access the same location and at least one access writes it.
- **Validation** checks that observations on which a transaction depends still justify its execution and prospective commit.
- **Opacity** requires every transaction, including live and aborted transactions, to observe a state consistent with some legal serial execution while respecting real-time order.
- **Version management** is eager when shared data is overwritten with undo information and lazy when writes remain private until commit.
- **Conflict detection** is eager when conflicts are noticed during access and lazy when they are discovered at validation or commit.
- **Strong atomicity** orders transactional and nontransactional accesses together; weak atomicity generally isolates only transactions from transactions.
- An **irrevocable effect** cannot safely be repeated or undone, such as sending a network request or releasing a physical actuator.
- A **contention manager** is policy for resolving conflicting transactions; it is not the safety mechanism itself.

### Central model, mechanism, or theorem

An optimistic STM starts a transaction, returns reads from a consistent snapshot, buffers writes, and validates dependencies. At commit it obtains exclusive publication rights for its write set, revalidates the read set, publishes all writes as one logical event, and releases metadata. A conflict or failed validation aborts the transaction and discards tentative state; retry re-executes from the beginning. Serializability is not enough for safe speculative execution: opacity also constrains live and doomed transactions, so they cannot act on a fractured state before abort is recognized.

### Critical invariants

Uncommitted writes are invisible outside their transaction. A committed transaction has one serialization point compatible with the abstract specification. Every returned transactional read belongs to a consistent legal snapshot. Validation covers every semantic dependency, not merely convenient fields. Metadata cannot be mistaken for application data. Locks or ownership records are acquired without exposing partial publication and released on every exit. Retried code is free of uncontrolled irrevocable effects. Transactional and nontransactional access follow the implementation's declared atomicity contract. Exceptions, cancellation, allocation, reclamation, nesting, shutdown, and fallback preserve all-or-nothing state.

### Common failures

Programs perform I/O inside retryable code; validate only at commit and allow doomed transactions to divide by zero or dereference invalid state; publish one buffered write before another; omit a read from the dependency set; deadlock while acquiring multiple write locks; assume `atomic` implies durability; mix plain and transactional accesses under weak atomicity; let long transactions cause repeated aborts; mistake obstruction-free retries for fairness; leak tentative allocations; use wall-clock or random values inconsistently across retries; or adopt hardware transactions without a correct fallback.

### Compact example

Transaction A reads balances `(5,5)` and tentatively transfers one unit. Transaction B commits `(3,7)` first. A's versions no longer match, so A must publish neither tentative value. On retry, A reads `(3,7)`, proposes `(2,8)`, validates, and commits both values together. The invariant `x + y = 10` holds at each committed state; observing `(2,7)` would reveal a broken publication protocol.

### Connections

[Linearizability Proofs](058-linearizability-proofs.md) supplies serialization reasoning, and [Contention Management in Nonblocking Algorithms](059-contention-management-in-nonblocking-algorithms.md) supplies retry policy. The next modules deepen optimistic validation, transactional retry, composition, conflict detection, and contention.

## Governing Question

What must an STM guarantee, record, validate, and prohibit so that a convenient `atomic` block is a defensible concurrency abstraction rather than a rollback illusion?

The answer separates four layers. The programming model describes transactional variables and composition. The correctness condition describes allowed histories. The implementation supplies versions, locks, logs, validation, and publication. Policy chooses victims, retry delays, and resource limits. Confusing these layers causes both false proofs and disappointing systems.

## Why This Matters

Locks protect invariants, but abstractions built from locks do not generally compose. A function that moves one item between two independently locked collections cannot simply call each collection's correct methods and thereby obtain one atomic move. Lock order, failure, blocking, and rollback escape through the interface. STM proposes a higher-level unit: compose reads and writes into a transaction and let the runtime coordinate conflicts.

The programmer can express a transfer or multi-field transition close to its invariant. Some systems retry it when relevant state changes rather than exposing condition-variable choreography. The runtime can change synchronization strategies without changing the abstract operation.

The abstraction is not magic. Transaction bodies may execute many times. A doomed transaction can run before validation. Metadata adds cost, and large access sets increase validation and contention. Progress depends on policy, allocation, scheduling, and fallback. Plain memory, I/O, exceptions, foreign code, destruction, and reclamation define the real safety boundary.

STM also differs from a database transaction. Both use atomicity and isolation ideas, but an ordinary STM transaction changes volatile process memory and usually promises neither durability across power loss nor distributed atomic commit. Treating `atomic` as ACID durability can lose externally important state.

## Prerequisites and Retrieval

Retrieve:

- happens-before and visibility from [Happens-Before Relations](023-happens-before-relations.md);
- read-modify-write and ordering from [Atomic Read-Modify-Write Operations](025-atomic-read-modify-write-operations.md);
- abstract histories from [Linearizability Proofs](058-linearizability-proofs.md);
- progress classifications from [Obstruction-Free, Lock-Free, and Wait-Free Progress](051-obstruction-free-lock-free-and-wait-free-progress.md); and
- conflict policy from [Contention Management in Nonblocking Algorithms](059-contention-management-in-nonblocking-algorithms.md).

Retrieval prompt: two operations each preserve `x + y = 10` when executed alone. List the interleavings that become observable if their two writes publish independently, then identify what a transaction must hide or validate.

## Learning Objectives

After completing this module, a learner can:

1. distinguish STM atomicity and isolation from durability and distributed commit;
2. define read sets, write sets, versions, ownership records, validation, commit, abort, and retry;
3. explain why opacity is stronger than serializability and relevant to speculative execution;
4. trace a lazy-versioned optimistic transaction through a TL2-style commit path;
5. compare eager and lazy versioning, conflict detection, and read visibility;
6. reason about transactional versus nontransactional access and strong versus weak atomicity;
7. classify retry-safe, deferred, compensatable, and prohibited effects;
8. identify progress, contention, nesting, privatization, reclamation, and lifecycle hazards;
9. design evidence for functional correctness and operational suitability; and
10. specify additional review for high-consequence transactional state transitions.

## Core Exposition

### Begin with a sequential transaction specification

Let shared transactional state be a mapping from locations to values. A transaction executes a program over a logical state, producing either `commit(result, updates)` or `abort`. Its sequential specification must define legal values, invariants, return results, exception behavior, and whether explicit retry is observable. If it commits, every update takes effect; if it aborts, none does.

This abstract contract permits locks, per-location versions, indirection, logs, multi-version storage, or hardware assistance. Clients must not infer progress from atomicity unless explicitly specified.

An STM location must not be confused with an ordinary variable. Reads and writes are intercepted so the runtime can track dependencies and delay or undo publication. A language may enforce that distinction through types; a library in an unsafe language may rely on discipline and therefore has a larger review surface.

### Histories and correctness

A committed transaction should appear at one logical instant between invocation and response, yielding a serial history compatible with the object specifications. Strict serializability respects real-time precedence: if A finishes before B begins, the serial order cannot put B before A. At a transaction interface, this resembles linearizability of each complete transaction as one operation.

But a doomed transaction executes before its abort. Suppose it reads `x = 0` from before one commit and `y = 0` from after another, although the invariant requires exactly one of them to be zero. It may compute `1 / (x + y)`, use an invalid index, or follow an impossible pointer before final validation rejects it. A history containing only committed transactions can still be serializable while the speculative execution was unsafe.

Opacity closes that gap. Informally, all transactions—committed, aborted, and live—must be embeddable in a legal sequential history that respects real-time ordering. Aborted transactions may have no effect, but their reads must still describe a consistent state. Implementations obtain opacity through mechanisms such as snapshot timestamps, incremental validation, sandboxing, or constrained language semantics. A commit-only check without protection against unsafe intermediate computation is insufficient in an unmanaged setting.

### Transactional metadata

A typical word-based STM maintains per location or stripe a value plus version, ownership state, or descriptor pointer. A transaction descriptor contains status and access sets. Coarse metadata creates false conflicts; fine metadata costs space and cache traffic.

The read set usually records location identity and observed version. The write set records the new value and often the old value or associated metadata. A read of a location already in the local write set returns the tentative value. Duplicate accesses must be normalized so validation and publication do not disagree.

Metadata is concurrent state. Define atomic widths, ordering, wraparound, lock bits, version comparison, and release on every abort path. A counter that wraps into an indistinguishable old version can validate stale observations, much like ABA.

### A lazy optimistic path

Consider a TL2-style family of designs. At begin, transaction T reads a global version clock `bt`. A transactional read first checks its own write buffer. Otherwise it reads the location and ownership/version metadata in an order that detects concurrent writers. It accepts the value only if the location is unlocked and its version is not newer than `bt`; implementations may reread metadata to ensure the value and version belong together. The location/version enters T's read set.

Writes enter a private buffer. At commit, a read-only transaction can often finish after suitable validation. A writer acquires ownership records for its write set in a canonical order or with a nonblocking protocol. It obtains a commit version, then validates read dependencies not safely covered by its own locks. If a dependency changed or is held incompatibly, T releases ownership and aborts. Otherwise it publishes every buffered value, stamps metadata with the commit version, and releases ownership using the required memory ordering.

The logical serialization point depends on the algorithm and proof—often the commit timestamp acquisition or a point during publication under exclusive metadata—not on whichever source line looks important. Readers must be unable to accept a partially published write set. The proof connects concrete metadata transitions to the abstract atomic transaction.

The following deterministic model shows version validation and all-or-nothing buffered publication. It is sequential teaching code: it does not implement concurrent STM, opacity under arbitrary interleavings, atomic machine publication, or a language memory model.

<!-- bijux-verify: {"id":"stm-version-validation","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"t1_first=aborted\nafter_conflict={'x': 3, 'y': 7}\nt1_retry=committed\nfinal={'x': 2, 'y': 8}\nsum=10\nversions={'x': 2, 'y': 2}\n","stderr":""}} -->
```python
store = {"x": {"value": 5, "version": 0}, "y": {"value": 5, "version": 0}}


def begin():
    return {"reads": {}, "writes": {}}


def read(transaction, key):
    if key in transaction["writes"]:
        return transaction["writes"][key]
    cell = store[key]
    transaction["reads"][key] = cell["version"]
    return cell["value"]


def write(transaction, key, value):
    transaction["writes"][key] = value


def commit(transaction):
    valid = all(store[key]["version"] == version for key, version in transaction["reads"].items())
    if not valid:
        return "aborted"
    for key, value in transaction["writes"].items():
        store[key]["value"] = value
        store[key]["version"] += 1
    return "committed"


def transfer_one():
    transaction = begin()
    x = read(transaction, "x")
    y = read(transaction, "y")
    write(transaction, "x", x - 1)
    write(transaction, "y", y + 1)
    return transaction


t1 = transfer_one()
t2 = begin()
write(t2, "x", 3)
write(t2, "y", 7)
commit(t2)
print(f"t1_first={commit(t1)}")
print(f"after_conflict={{'x': {store['x']['value']}, 'y': {store['y']['value']}}}")
t1_retry = transfer_one()
print(f"t1_retry={commit(t1_retry)}")
print(f"final={{'x': {store['x']['value']}, 'y': {store['y']['value']}}}")
print(f"sum={store['x']['value'] + store['y']['value']}")
print(f"versions={{'x': {store['x']['version']}, 'y': {store['y']['version']}}}")
```

The model applies buffered writes sequentially only because no actual concurrency exists during `commit`. A production implementation needs atomic metadata and a protocol that prevents other transactions from accepting the intermediate state.

### Design dimensions

**Lazy versioning** keeps tentative writes private and discards them cheaply on abort, but commit must publish a potentially large set. **Eager versioning** writes shared data early while preserving undo information; it can make commit cheaper but complicates abort, observation, and failures. A crash between eager writes and undo is not automatically recoverable.

**Eager conflict detection** reacts when conflicting accesses occur, potentially avoiding doomed work, but requires coordination on the access path and a victim decision. **Lazy detection** permits work to continue until validation/commit, which can reduce shared metadata traffic yet waste computation and produce late aborts.

**Invisible reads** avoid writing shared metadata and make read-mostly workloads attractive, but writers cannot directly identify readers and readers may repeatedly abort. **Visible reads** announce readers, enabling some conflict policies and privatization protocols at the cost of writes, cleanup, and bounded reader representation.

**Single-version** systems retain one committed value and must prevent readers from losing their snapshot. **Multi-version** systems let readers choose a version consistent with a timestamp, reducing read-write conflicts but requiring version retention, selection, and reclamation. Module 067 develops multi-version state.

### Effects and repeatability

Abort means the transaction body may execute again. Therefore a retryable transaction cannot directly send email, write a socket, append to an ordinary file, acquire an external lock, acknowledge a message, charge a card, emit a physical command, or mutate untracked memory. The effect may happen twice even though only one memory transaction commits, or it may happen despite abort.

Safe patterns include computing pure data inside the transaction and performing the effect afterward; recording an idempotent intent in transactional state for an owned dispatcher; or using an implementation-defined irrevocable mode that serializes and guarantees the transaction will not abort after the effect boundary. Each pattern has distinct crash semantics. An in-memory STM plus a post-commit effect still has a crash window, so exactly-once external behavior requires a protocol beyond volatile STM.

Reading time, randomness, thread identity, or a changing external source also affects repeatability. Capture such input under a declared policy outside the transaction or accept that retries may compute a different proposal. Logging inside a transaction should be buffered, tagged by attempt, or explicitly treated as speculative; otherwise operators see events for work that never committed.

### Explicit retry and composition

Some language-level STMs provide `retry`: the transaction abandons its attempt and waits until a location it read changes. This turns a predicate such as “queue nonempty” into a composable blocking operation. An alternative operator can try one transaction and, if it retries, try another while combining relevant wake dependencies.

This is stronger than automatically rerunning after conflict. Semantic retry is requested by program logic; conflict abort is imposed by concurrency control. Implementations must prevent missed wakeups, unbounded dependency retention, and unfair wake storms. Module 063 develops these semantics and their compositional laws.

### Exceptions, cancellation, and nesting

An exception normally aborts tentative writes before propagating, but language-specific rules decide which exceptions are catchable inside a transaction and whether a handler observes prior tentative state. Asynchronous cancellation must not strand ownership records or publish half a write set. Masking cancellation around internal commit does not authorize arbitrary long uninterruptible transactions.

Nested atomic blocks need a contract. **Flattening** treats inner work as part of one outer transaction: an inner “commit” is not externally visible, and an outer abort removes it. **Closed nesting** can abort inner work independently but exposes results only with the outer commit. **Open nesting** publishes inner effects early and needs semantic compensation and isolation arguments; it is not ordinary all-or-nothing nesting.

### Transactional and plain accesses

Strong atomicity makes transactional operations atomic relative to plain accesses. Weak atomicity isolates transactions only from other transactions; a plain read may observe tentative or intermediate representation unless the program follows additional rules. Even when an implementation offers strong atomicity, data races in the host language may remain undefined.

Every location needs an access discipline. Publishing a transactional object to plain code, privatizing it after a transaction, or reclaiming it while an old transaction can still refer to it requires synchronization beyond a superficial commit. A transaction that removes a node does not prove no live transaction holds a speculative pointer. GC can preserve memory safety but not necessarily semantic consistency or bounded retention.

### Progress and contention

Atomicity says which outcomes are legal, not whether anyone finishes. A global commit lock can implement correct STM while blocking. An obstruction-free implementation permits a transaction running alone to complete but can livelock under conflict. A lock-free system-wide claim still permits individual starvation. Allocation, validation, scheduler pauses, irrevocable mode, and fallback are part of the public progress path.

Contention management may abort younger transactions, favor older ones, use randomized or exponential backoff, prioritize short write sets, or serialize after repeated failure. No policy is universally best. It must preserve safety independently and should be evaluated for throughput, tail latency, starvation, wasted work, priority, and adversarial schedules.

### Operational boundaries

Measure aborts by cause, attempts per commit, read/write-set sizes, validation work, ownership wait, transaction duration, oldest age, fallback/irrevocable entries, retained versions, and allocation. Cardinality-safe telemetry should not expose sensitive values. Trace attempt identity separately from logical transaction identity.

Bound transaction size and duration where possible. Long transactions enlarge conflict windows and may pin versions or memory. Overload can create positive feedback: conflicts cause retries, retries consume CPU and lengthen transactions, and longer transactions conflict more. Admission, batching, partitioning, and fallback may be more effective than a clever victim heuristic.

Shutdown must prevent new transactions, resolve or abort active attempts, release metadata, drain deferred effects, and reclaim versions safely. Forking, signals, dynamic unloading, foreign callbacks, thread registration, and runtime suspension require explicit qualification. A process restart discards volatile transactional state unless a separate persistence design exists.

### Evidence for adoption

Start with the abstract state machine and invariants. Provide an opacity or stated weaker-condition argument, concrete-to-abstract mapping, serialization points, metadata invariants, memory-order/lifetime reasoning, progress scope, and effect discipline. Use bounded histories or model checking for small configurations, adversarial schedules, fault injection, race/undefined-behavior tools where applicable, and differential tests against a serialized reference.

Performance evidence needs a representative transaction mix, conflict topology, read/write-set distribution, duration, working set, skew, allocation, oversubscription, NUMA, failures, and shutdown. Compare competent locks, partitioning, immutable or message-passing designs, and mature STM implementations with identical semantics. A microbenchmark showing many tiny disjoint transactions proves little about an application dominated by I/O or irrevocable work.

## Definitions and Notation

- `T`: a transaction attempt; retries are distinct attempts of one logical operation.
- `R(T)`: locations and versions read by T.
- `W(T)`: locations and tentative values written by T.
- `bt(T)`: begin or snapshot timestamp.
- `ct(T)`: commit timestamp, when the design uses one.
- `ver(x)`: committed version metadata for location x.
- `conflict(T,U)`: `(W(T) ∩ (R(U) ∪ W(U))) ∪ (W(U) ∩ R(T))` is nonempty.
- `S`: a legal sequential history of transactions.
- `H`: an observed concurrent history, including live and aborted transactions.
- `≺rt`: real-time precedence in H.
- `I(s)`: application invariant over committed state s.

Serializability asks for an equivalent legal S for committed effects. Strict serializability additionally preserves `≺rt`. Opacity extends a consistent legal serialization requirement to committed, aborted, and live transactions after completing or aborting pending operations appropriately. Exact formal definitions vary in presentation; a proof must state its model rather than rely on the label alone.

## Mechanisms, Invariants, or Proof Structure

### Representation invariant

Each transactional location is either unlocked with a stable committed value/version or owned according to a valid transaction descriptor. A tentative write is reachable only through its owning transaction until commit publication. A terminal aborted descriptor cannot later publish, and a terminal committed descriptor denotes one complete logical write set. Metadata transitions use atomic operations and ordering sufficient for readers to pair values with versions.

### Read validity argument

For each accepted read of x, show the value corresponds to a committed version allowed by T's snapshot and that x did not change across the value/metadata observation. Then show later validation or incremental checks prevent T from continuing after the set of accepted reads ceases to fit one legal snapshot. This second obligation is where opacity exceeds “we will notice at commit.”

### Commit refinement argument

Before publication, T owns or otherwise excludes conflicting publication for every x in `W(T)`. Validation establishes that every semantic dependency in `R(T)` remains compatible. Assign a serialization point permitted by the algorithm. Show all external readers order either before the entire T or after the entire T, never between its writes. Finally show the abstract state transition preserves I or returns the specified failure.

### Abort argument

An abort changes no abstract transactional state. Lazy tentative values are discarded; eager values are restored or made unreachable before others can accept them. Every ownership record, waiter registration, allocation, version reference, and deferred effect is released or transferred exactly once. Cancellation and exceptions refine this same abort transition unless the contract specifies successful commit first.

### Progress argument

State the scheduler, allocator, metadata primitive, retry, contention-manager, and fallback assumptions. Prove only the corresponding blocking, obstruction-free, lock-free, or wait-free property. Safety must not depend on fairness policy. Empirical completion rates support operational decisions but do not prove universal liveness.

## Alternatives and Trade-Offs

| Design | Main advantage | Main cost or limitation |
|---|---|---|
| Coarse mutex | small proof surface; predictable effects | blocking and limited parallelism |
| Fine-grained locks | concurrency for disjoint state | lock ordering and noncomposable interfaces |
| Message passing/owner task | explicit effects, ordering, and backpressure | queue/owner latency; distributed composition |
| Immutable snapshots | cheap consistent reads | copy, publication, and retained-version cost |
| Optimistic STM | declarative multi-location atomicity | validation, retries, effect restrictions |
| Pessimistic STM | avoids repeated conflicting work | ownership traffic, deadlock/priority concerns |
| Multi-version STM | read snapshots with fewer read-write conflicts | version selection and reclamation |
| Hardware transactional memory | low instrumentation on successful small transactions | capacity/conflict/spurious aborts; mandatory fallback |
| Hybrid TM | fast hardware path plus software fallback | interaction proof and duplicated complexity |
| Database/durable log | persistence and recovery protocols | latency, I/O, schema and distributed boundaries |

Choose by invariant boundary and workload. STM is strongest when operations combine dynamic shared locations and remain short, in-memory, and retry-safe. Ownership or messaging is often clearer when effects dominate. A mutex is often superior when contention is modest and composition stays within one owned abstraction.

## Failure Modes and Misconceptions

- **“Atomic means durable.”** Ordinary STM state disappears on process or power failure.
- **“Serializability protects aborted code.”** Opacity or equivalent sandboxing is needed for consistent speculative reads.
- **“Validation at commit is always enough.”** Doomed unmanaged code can fail before commit.
- **“Abort undoes everything.”** The runtime cannot retract arbitrary I/O or untracked mutation.
- **“Retry is just a loop.”** Semantic retry needs dependency tracking and missed-wakeup prevention.
- **“Conflicts are data races.”** Conflicts are STM concurrency-control relations; host-language races are a separate safety issue.
- **“Disjoint writes cannot conflict.”** Shared reads, striped metadata, allocators, and global clocks can connect them.
- **“Read-only is free.”** Snapshot acquisition, read barriers, validation, and version retention remain.
- **“One global clock serializes execution.”** It orders commits but need not prevent disjoint transaction bodies from running concurrently.
- **“More retries imply incorrectness.”** They may be legal yet operationally unacceptable.
- **“Contention policy proves safety.”** Victim choice affects progress/performance; core validation must preserve safety regardless.
- **“Nested commit is permanent.”** Flattened and closed nesting remain contingent on the outer transaction.
- **“GC solves transactional lifetime.”** It can prevent reuse while leaving stale semantics and unbounded retention.
- **“Hardware transactions remove fallback.”** Capacity, conflicts, interrupts, and implementation causes can abort them.
- **“Plain reads automatically participate.”** That depends on strong atomicity and host-language rules.

## Worked Examples

### Example 1

**Atomic transfer.** State is `(a,b)=(40,60)` with invariant `a+b=100`. A transaction reads both, buffers `(30,70)`, validates, and publishes together. Any reader must order before it and see `(40,60)`, or after it and see `(30,70)`. **Conclusion:** atomic publication preserves a cross-location invariant that independent stores would expose transiently.

### Example 2

**Write-write conflict.** T and U both read `x=4`; T proposes 5 and U proposes 9. If T commits version 8, U's recorded version 7 fails validation. U aborts and may retry from 5. Last-writer-wins without validation would silently discard T. **Conclusion:** conflicting proposals require an order, not blind publication.

### Example 3

**Why opacity matters.** In every committed state, `denominator > 0`. T reads an old pointer to the object, then a new `denominator=0` from a replacement state that makes the old pointer invalid. Even if commit validation later aborts T, dereferencing or division can already fail. Incremental validation or a consistent snapshot prevents that fractured observation. **Conclusion:** aborted/live reads are part of memory safety reasoning.

### Example 4

**False conflict.** Locations x and y use one striped ownership record. T writes x while U writes y; their abstract write sets are disjoint, yet one must abort because the metadata aliases. Finer stripes reduce this false conflict but consume metadata/cache capacity. **Conclusion:** implementation granularity can reduce concurrency without changing semantic conflicts.

### Example 5

**Irrevocable email.** A transaction decrements inventory and sends an email, then loses validation. Inventory is unchanged but the customer received a message; retry can send another. Instead commit a transactional “email intent” with an idempotency key and let a dispatcher deliver it under a separately specified durable protocol. **Conclusion:** rollbackable memory does not make external effects rollbackable or durable.

### Example 6

**Explicit retry.** A transactional dequeue reads an empty queue and executes semantic `retry`. The runtime registers the queue location and suspends efficiently. An enqueue commits a changed queue version and makes the dequeue eligible to rerun. Polling every millisecond would add latency/load and would not compose across alternatives. **Conclusion:** dependency-aware retry is a programming-model feature, not merely conflict backoff.

### Example 7

**Weak atomicity leak.** Transaction T eagerly writes field x before y while keeping undo data. Plain code reads x without an STM barrier and sees the tentative value. Transactions may remain mutually isolated, yet the mixed program is wrong. Use strong atomicity or forbid mixed access with enforceable ownership/types. **Conclusion:** the boundary around transactional locations is part of the contract.

### Example 8

**Long reader pressure.** A multi-version read transaction scans for ten seconds while writers commit every millisecond. Avoiding reader aborts retains thousands of old versions; bounding versions may instead abort the reader. Partition the scan, use an explicit snapshot budget, or choose a database/snapshot architecture. **Conclusion:** fewer logical conflicts can become retention debt.

### Example 9

**Hardware fast path.** A small update usually commits in hardware but aborts for capacity on a larger input. Retrying forever is not progress. A fallback lock must coordinate so hardware transactions subscribe to or check it; otherwise hardware and fallback paths can overlap unsafely. **Conclusion:** fallback is part of the algorithm and proof, not an exception handler.

### Example 10

**Infusion-pump dose state.** A proposed transaction atomically consumes a prescription token, updates delivered dose, and schedules an actuator command. Volatile STM cannot itself make the physical command atomic or durable. The design needs a human-approved state machine separating committed intent, uniquely identified command dispatch, acknowledgement, recovery, duplicate suppression, bounds, alarm behavior, and manual override. Named clinical safety, embedded/runtime, formal-methods, hardware, cybersecurity, human-factors, quality/regulatory, and operations reviewers must examine assumptions and evidence; no external review is claimed here. **Conclusion:** high-consequence memory atomicity is only one component of an end-to-end safety protocol.

## Cross-Program Connections

- **Programming languages:** effects, exceptions, types, and operational semantics determine which transaction bodies are meaningful.
- **Databases:** serializability, multi-versioning, logging, and recovery are related, but durability and distribution require additional protocols.
- **Formal methods:** opacity, refinement, invariants, and liveness separate guarantees from implementation intuition.
- **Computer architecture:** cache coherence, atomic metadata, fences, HTM, and NUMA shape cost and correctness.
- **Operating systems:** scheduling, cancellation, signals, page faults, and resource exhaustion constrain progress.
- **Software engineering:** compositional APIs, effect boundaries, observability, fallback, and ownership determine maintainability.
- **Security:** adversarial conflicts, timing, untrusted transaction bodies, retention, and unsafe rollback paths expand attack surfaces.
- **Safety engineering:** transactional intent must connect to durable, physical, and human processes through reviewed state machines.

## References

1. Nir Shavit and Dan Touitou, “Software Transactional Memory,” PODC 1995, pp. 204–213. <https://doi.org/10.1145/224964.224987>
2. Maurice Herlihy, Victor Luchangco, Mark Moir, and William N. Scherer III, “Software Transactional Memory for Dynamic-Sized Data Structures,” PODC 2003. <https://doi.org/10.1145/872035.872048>
3. Rachid Guerraoui and Michal Kapalka, “On the Correctness of Transactional Memory,” PPoPP 2008. <https://doi.org/10.1145/1345206.1345233>
4. Dave Dice, Ori Shalev, and Nir Shavit, “Transactional Locking II,” DISC 2006. <https://doi.org/10.1007/11864219_14>
5. Tim Harris, Simon Marlow, Simon Peyton Jones, and Maurice Herlihy, “Composable Memory Transactions,” PPoPP 2005. <https://doi.org/10.1145/1065944.1065952>
6. Luke Dalessandro, Michael F. Spear, and Michael L. Scott, “NOrec: Streamlining STM by Abolishing Ownership Records,” PPoPP 2010. <https://doi.org/10.1145/1693453.1693464>
7. James R. Larus and Ravi Rajwar, *Transactional Memory*, Morgan & Claypool, 2007. <https://doi.org/10.2200/S00070ED1V01Y200611CAC002>
8. Maurice Herlihy and Nir Shavit, *The Art of Multiprocessor Programming*, revised first edition, 2012. <https://www.elsevier.com/books/the-art-of-multiprocessor-programming/herlihy/978-0-12-397337-5>
9. GHC Project, `Control.Concurrent.STM` library documentation, current package documentation; retrieved 2026-08-29. <https://hackage.haskell.org/package/stm/docs/Control-Concurrent-STM.html>
10. Intel, “Intel Transactional Synchronization Extensions,” architecture and optimization documentation, current edition; retrieved 2026-08-29. <https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html>

## Exercises

### Exercise 1

Define abort, conflict, validation, strict serializability, and opacity. Give one execution that a committed-only serializability check can miss but opacity rejects.

### Exercise 2

Trace two lazy-versioned transactions. T reads `x=2,y=8` and buffers `x=3,y=7`; U reads x and commits `x=5`. State which sets and versions T records, why its first attempt aborts, and what may be published.

### Exercise 3

A transaction writes a file, mutates an ordinary cache, updates two TVars, and logs success. Diagnose every effect under possible conflict retry and redesign the operation with an explicit failure model.

### Exercise 4

Compare a coarse mutex, fine-grained locks, optimistic STM, immutable snapshots, and one-owner message passing for a read-heavy configuration registry with rare multi-key updates and a deterministic unload requirement.

### Exercise 5

A railway controller wants STM to reserve a route across track segments and command signals. Specify the abstract state, correctness/progress conditions, effect boundary, recovery protocol, evidence, and mandatory human review needed before deployment.

## Answers to the Exercises

### Answer 1

Abort terminates an attempt without publishing transactional writes. A conflict is overlapping access to one location with at least one write. Validation checks that recorded dependencies still support the attempt. Strict serializability gives committed transactions a legal serial order respecting real-time precedence. Opacity extends consistent legal observations to live and aborted transactions. For example, invariant states are `(pointer=A,valid=A)` and `(pointer=B,valid=B)`. A doomed transaction reads old pointer A and new validity B, then dereferences A before commit validation. Removing the aborted transaction leaves a serializable committed history, but the transaction observed no legal state; opacity rejects it.

### Answer 2

Initially T records `R(T)={x:vx,y:vy}` and `W(T)={x:3,y:7}`; its tentative reads/writes are private. U records at least x's observed version, obtains publication rights, validates, commits `x=5`, and advances x's version. T's later validation finds `ver(x) != vx`; therefore it aborts and may publish neither x=3 nor y=7. On retry it must reread the new committed state and recompute rather than reuse its old proposal. A real implementation also prevents readers from accepting partial U/T publication and handles write ownership atomically.

### Answer 3

The file append and ordinary-cache mutation are untracked and survive abort; retry duplicates or compounds them. Direct success logging can describe an attempt that later aborts. TVar writes alone roll back. Redesign the transaction to compute data and atomically update TVars plus a uniquely keyed effect intent. After commit, an owned dispatcher applies cache/file effects idempotently and records status; logging distinguishes attempt, commit, dispatch, and acknowledgement. If file durability across crashes matters, volatile STM is insufficient: use a durable log/database protocol and define the crash windows, replay, duplicate suppression, and operator recovery.

### Answer 4

A coarse mutex has the smallest proof and deterministic unload if readers do not hold it across arbitrary work, but can serialize access. Fine locks increase concurrency while complicating multi-key order and unload. Optimistic STM expresses multi-key invariants well, but every access must participate, transactions must be short/retry-safe, and shutdown must resolve attempts. Immutable snapshots make reads simple and updates atomically publish a new registry; retained handles determine unload. One-owner messaging makes update/effect order explicit but adds request latency and queue lifecycle. For rare updates, immutable snapshots with bounded handles or a well-scoped lock are leading designs unless measurement or composition rejects them. Gate on exact snapshot/lifetime semantics, retained bytes, p99, update atomicity, close/admission, handle draining, destructor context, and owner failure.

### Answer 5

Specify segments, routes, incompatibility graph, signal aspects, train occupancy, command intents, acknowledgements, failures, and the invariant that no committed reservations authorize conflicting movements. Require strict real-time/opacity semantics for controller decisions plus an explicitly justified progress and deadline model. STM may atomically reserve memory state and enqueue a uniquely identified intent; it must not directly treat a retryable physical signal command as rolled back. A durable controller protocol validates field state, dispatches idempotently, confirms safe aspect, handles partial communication, restart, fail-safe timeout, manual control, and audit. Evidence includes formal state-machine/refinement and invariant review, bounded model/exhaustive small-topology tests, concurrency histories, weak-memory/runtime qualification, fault and hardware-in-loop tests, worst-case timing, overload, restart, upgrade, cybersecurity, and independent hazard analysis. Named signaling engineers, functional-safety assessors, formal-methods specialists, real-time/runtime and hardware engineers, cybersecurity, human-factors, operations/maintenance, quality/regulatory, and independent assurance reviewers must approve assumptions, evidence, fallback, and residual risk. No course exercise substitutes for those approvals.
