---
module_id: CONPAR-067
program: Programming Languages: Concurrent & Parallel Programming
level: 2
module_number: 67
title: Immutable Snapshots and Multi-Version State
status: complete
last_verified: 2026-08-29
---

# Immutable Snapshots and Multi-Version State

## One-Page Review

### Governing question

How can readers observe a stable, internally consistent past state while writers publish new state concurrently, and what additional validation is required when a stable snapshot is not serializable?

### Essential definitions

- An **immutable snapshot** is a stable view whose reachable values do not change for the lifetime of that view.
- A **version** is an immutable state or item value associated with an identity and ordering coordinate.
- **structural sharing** reuses unchanged immutable nodes across versions while copying changed paths.
- **partial persistence** permits queries against every version but updates only the newest; **full persistence** also permits updates from old versions.
- An **atomic snapshot object** supports updates to components and a scan linearizable as one instantaneous read of all components.
- **MVCC** retains multiple item versions so a read selects the version visible to its snapshot.
- A **snapshot timestamp** or logical epoch defines the reader's visibility frontier; it is not necessarily wall time.
- **snapshot isolation** (SI) reads from one committed snapshot and normally prevents concurrent transactions with overlapping write sets from both committing.
- **write skew** occurs when transactions read a shared predicate, write disjoint items, and jointly violate an invariant while each is valid against its snapshot.
- **safe publication** makes a complete immutable root/version visible atomically with the required memory ordering.
- **reclamation** proves no reader can reach an old version before its storage is reused or freed.
- A **version horizon** is the oldest version that active readers, replicas, recovery, audit, or retention policy may still require.

### Central model, mechanism, or theorem

Let committed versions of item x be pairs `(v, value)` ordered by logical version v. A snapshot at read version r selects the greatest committed `v ≤ r`, plus the transaction's own writes. Writers build private immutable changes, validate the required conflict relation, then atomically publish a new root or commit record. Readers never observe partial construction. This yields stable nonblocking reads when visibility and lifetime are correct. It does not by itself yield serializability: SI's first-committer-wins rule for write/write conflicts misses cycles made only of read/write anti-dependencies, including write skew.

### Critical invariants

Published objects are transitively immutable. Each snapshot has one visibility rule across all items. Version identities never compare ambiguously after wraparound or reuse. Commit publication orders initialization before discovery. Aborted versions are invisible. A writer validates every dependency required by the stated isolation level, not only direct write collisions. Readers announce or pin lifetimes before reclamation can pass them. The version horizon includes active snapshots, replicas, backups, change streams, and recovery. Durable data, indexes, metadata, and external effects agree on the same commit boundary. Resource exhaustion from long readers is bounded and observable.

### Common failures

Implementations call a shallow copy immutable while referenced objects mutate; read each field at a different time; publish a root before children initialize; use wall time as a total commit order; compare wrapped counters naively; reclaim a version after scanning an incomplete reader registry; allow write skew under SI; forget phantoms and predicate reads; mutate shared nodes during path copying; retain every version forever; vacuum past a lagging replica; mix database snapshot state with live cache or service reads; or treat one stable view as automatically current, serializable, durable, or safe.

### Compact example

Doctors A and B are initially on call. Two SI transactions start at the same version. Each sees the other on call and writes only its own row to false. Their write sets are disjoint, so write/write validation lets both commit; the invariant “at least one doctor is on call” becomes false. Serializable validation must detect the predicate dependency, abort one, or lock/materialize the invariant.

### Connections

[Optimistic Concurrency and Validation](062-optimistic-concurrency-and-validation.md) supplies validation structure. [Hazard Pointers](055-hazard-pointers.md) and earlier reclamation modules protect retired versions. [Deterministic Parallel Execution](065-deterministic-parallel-execution.md) can build stable roots. The next module applies immutable values to parallel functional evaluation.

## Governing Question

What semantic, publication, conflict, and lifetime conditions let immutable and multi-version state decouple readers from writers without confusing a coherent old view with a serializable, durable, or current one?

A snapshot is not merely a copy. It is a contract about which version of every relevant object a reader may observe, how that view becomes stable, and how long its storage remains valid.

## Why This Matters

Concurrent read-heavy systems often suffer when readers and writers serialize on the same lock. Immutable roots and MVCC let readers traverse stable data while writers construct successors. The technique underlies functional data structures, configuration publication, routing tables, compiler structures, databases, filesystems, caches, analytics, and replicated state.

The advantages are substantial: readers can avoid write contention; consistent historical queries become possible; rollback and comparison are natural; and private construction simplifies reasoning. Costs move elsewhere. Updates allocate and retain versions, publication requires correct memory ordering, long readers delay reclamation, and transactions may need validation beyond write/write conflicts.

The most dangerous conceptual error is “repeatable means serializable.” A transaction can see a perfectly stable snapshot and still participate in a globally impossible outcome. Snapshot semantics, isolation semantics, lifecycle safety, durability, and freshness are separate claims.

## Prerequisites and Retrieval

Retrieve:

- component-wide concurrency reasoning from [Designing a Correct Multithreaded Component](020-designing-a-correct-multithreaded-component.md);
- reclamation from [Hazard Pointers](055-hazard-pointers.md);
- atomic root publication from [Visibility and Publication](024-visibility-and-publication.md);
- transaction validation from [Optimistic Concurrency and Validation](062-optimistic-concurrency-and-validation.md); and
- conflict graphs from [Conflict Detection and Contention](064-conflict-detection-and-contention.md).

Retrieval prompt: define a state with two related fields and construct an interleaving where reading each field atomically still produces a pair that never existed. Then state how one root pointer or version frontier prevents that torn view.

## Learning Objectives

After completing this module, a learner can:

1. distinguish immutable values, persistent structures, atomic snapshots, MVCC, and snapshot isolation;
2. implement path-copying and structural-sharing invariants;
3. define version visibility, read-your-writes, commit, and abort rules;
4. prove safe root publication under a named memory model;
5. identify write skew, phantoms, and serialization-graph cycles;
6. select write-conflict, predicate, serializable-snapshot, or explicit-lock validation;
7. design version pinning, horizon computation, reclamation, and backpressure;
8. coordinate durable logs, indexes, caches, replicas, and external effects;
9. test boundary cases including wraparound, crash, lag, cancellation, and resource exhaustion; and
10. scope high-stakes snapshot evidence and independent review.

## Core Exposition

### Five related but different ideas

An immutable value never changes after construction. A persistent data structure retains old logical versions after an update, often through immutable nodes and structural sharing. An atomic snapshot object offers a linearizable multi-component scan even though components are updated concurrently. MVCC stores multiple item versions and chooses visible versions by a concurrency-control rule. Snapshot isolation is one transaction-level rule commonly implemented with MVCC.

None implies all the others. A copied mutable graph is not deeply immutable. A persistent tree can be used by one thread without atomic publication. An atomic scan algorithm need not preserve arbitrary history. MVCC can implement read committed, SI, or serializable isolation. An SI transaction reads one coherent snapshot but can be nonserializable.

Name the abstraction and observation. “Snapshot” may mean a root pointer, collection value, database transaction view, filesystem checkpoint, VM memory image, or distributed cut. Their consistency, durability, lifetime, and failure rules differ.

### Persistent data structures

An ephemeral update destroys the prior logical version. A partially persistent structure permits reading all versions while updates derive from the newest. Full persistence permits updates from any version, producing a version tree. Confluent persistence can combine versions, producing a version DAG and harder identity/alias reasoning.

Path copying creates new nodes along every path from the modified leaf to the root and reuses unchanged subtrees. Updating one key in a balanced tree of n nodes uses O(log n) new nodes while old roots retain the old value. No shared node may be mutated. A shallow “copy” followed by modifying a shared child corrupts every version reaching it.

Structural sharing trades allocation and indirection for cheap snapshots. Branching factor, cache locality, reference counting, tracing GC, fragmentation, equality/hashing, and batch updates determine practical cost. Transients or uniquely owned builders can mutate private nodes before freezing, but uniqueness and freeze publication become trusted invariants.

Version roots need stable provenance: parent version, logical commit ID, schema/configuration, and content digest where required. Pointer equality can accelerate comparisons inside one lifetime; it is not a durable content identity and may be reused after reclamation.

### Atomic snapshot objects

Reading register A and then B separately does not guarantee `(A,B)` existed simultaneously. An atomic snapshot scan must be linearizable: there is a point between invocation and response at which the returned vector equals shared memory. A global immutable root makes this straightforward when all fields live below one root and the root load is atomic.

When independent writers own components, snapshot algorithms can repeatedly collect tagged values and use helping. In the classic single-writer construction, an updater associates a sequence number and a snapshot with its value. A scanner that sees two identical collects can return them; if it observes one process move enough times, it can use the snapshot that process recorded. The proof places the scan at a valid linearization point and establishes wait-freedom under assumptions.

Do not translate that sketch casually into production code. Bounded tags, multiwriter support, atomic register width, progress, and memory ordering are central. Seqlocks provide another pattern: a reader retries if a sequence changes or is odd. They can starve readers under continuous writes and do not preserve history unless values are separately versioned.

### MVCC visibility

Represent each committed version of item x with a creator/commit coordinate and, depending on design, a deletion/end coordinate. A transaction obtains read version r. A read of x returns its own latest write if present; otherwise it selects the newest committed version visible at r. Uncommitted, aborted, too-new, or logically deleted versions are excluded.

Visibility may use monotonically ordered transaction IDs, commit sequence numbers, hybrid clocks, or an explicit snapshot containing active transactions. Wall-clock timestamps alone are unsafe when clocks move, collide, or lack the required global order. Distributed timestamp allocation needs uncertainty and causality rules beyond this local model.

A database statement may take a new snapshot per statement (read committed), while a transaction-level snapshot remains stable across statements (SI/repeatable-read style). Current PostgreSQL documentation, for example, distinguishes these behaviors and separately provides serializable snapshot isolation. Product names are not portable specifications; test observed guarantees and read the exact version's documentation.

### Private writes and commit publication

Writers normally place new values in a private write set or create uncommitted version records. Before commit they validate conflicts and constraints. Commit assigns or confirms an order, makes all versions visible atomically with transaction metadata, persists required log/data ordering, then acknowledges according to durability policy. Abort leaves no visible partial version.

In memory, construct an immutable graph privately, then release-publish its root; readers acquire-load the root before traversal. The release/acquire edge makes prior initialization visible. If storage is language-managed and immutable, the runtime may provide publication rules, but the program still needs one atomic root transition. Mutating a child after publication reintroduces races and tears logical versions.

Multiple related roots require one indirection through a super-root or a commit descriptor that readers interpret consistently. Publishing data root, index root, and metadata counter independently can expose combinations that never committed.

### Snapshot isolation

Under a common SI formulation, transaction T reads from the committed snapshot at its start and sees its own writes. Concurrent transactions whose write sets overlap cannot both commit: first-committer-wins. Read-only transactions obtain stable views without blocking writers, and many lost-update patterns are prevented.

SI is not serializability. Consider an invariant `A_on_call OR B_on_call`. Transactions T_A and T_B share the same initial snapshot where both are true. T_A reads B and writes only A=false. T_B reads A and writes only B=false. Their write sets do not intersect, so both pass write/write validation. The final state violates the invariant and has no equivalent serial order: whichever ran second would have observed the first doctor off call.

This is write skew. It arises through a cycle of read/write anti-dependencies rather than direct write collision. Similar failures occur in quotas, uniqueness across predicates, account aggregates, appointment capacity, graph constraints, and “at least one active replica” rules.

### Executable write-skew model

The following sequential model simulates two concurrent transactions from version 0. SI validates only overlapping write keys, commits both disjoint writes, and violates the invariant. A conservative serializable validator tracks read sets and aborts B because A changed a key B read. This is evidence for the stated finite model, not a database, locking, durability, or complete SSI implementation.

<!-- bijux-verify: {"id":"snapshot-isolation-write-skew","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"start={'A': True, 'B': True}\nsi_commits=['A', 'B']\nsi_final={'A': False, 'B': False}\nsi_invariant=False\nserial_commits=['A']\nserial_final={'A': False, 'B': True}\nserial_invariant=True\n","stderr":""}} -->
```python
start = {"A": True, "B": True}
transactions = {
    "A": {"reads": {"B"}, "writes": {"A": False}},
    "B": {"reads": {"A"}, "writes": {"B": False}},
}

si_state = dict(start)
si_commits = []
committed_writes = set()
for name in ["A", "B"]:
    write_keys = set(transactions[name]["writes"])
    if not write_keys.intersection(committed_writes):
        si_state.update(transactions[name]["writes"])
        committed_writes.update(write_keys)
        si_commits.append(name)

serial_state = dict(start)
serial_commits = []
changed_keys = set()
for name in ["A", "B"]:
    read_keys = transactions[name]["reads"]
    if not read_keys.intersection(changed_keys):
        serial_state.update(transactions[name]["writes"])
        changed_keys.update(transactions[name]["writes"])
        serial_commits.append(name)

print(f"start={start}")
print(f"si_commits={si_commits}")
print(f"si_final={si_state}")
print(f"si_invariant={si_state['A'] or si_state['B']}")
print(f"serial_commits={serial_commits}")
print(f"serial_final={serial_state}")
print(f"serial_invariant={serial_state['A'] or serial_state['B']}")
```

The conservative validator may abort more executions than necessary; real serializable algorithms use precise dependency tracking or locks. The example proves neither that every SI system implements exactly this loop nor that tracking direct read keys handles predicate phantoms.

### Predicates, phantoms, and serializability

A query reads a predicate, not merely the rows returned. “Count active reservations where room=R and time overlaps interval I” depends on absent rows that a concurrent transaction may insert. Row read sets alone miss the phantom. Predicate locks, range/index locks, materialized conflict rows, or serializable dependency tracking must represent that dependency.

Serialization graphs model transactions as nodes and dependency edges. A committed history is serializable when its relevant graph is acyclic under the theory's assumptions. SI anomalies contain particular dependency cycles. Serializable Snapshot Isolation (SSI) monitors read/write dependencies and aborts transactions when a dangerous structure could complete a nonserializable cycle, retaining many nonblocking reads.

Applications can also lock the invariant: select/update one guardian row representing “on-call coverage,” use a serializable isolation level with retry, or restructure writes so conflicting invariant changes touch one key. Ad hoc post-commit checks are too late if both invalid effects became visible.

### Freshness, consistency, and opacity

A snapshot can be internally consistent but stale. Readers must declare whether any committed version is acceptable, whether they require at least version r, bounded staleness, read-your-writes, monotonic reads, or the latest linearizable root. Cache invalidation and replica lag belong to this contract.

Transaction opacity requires even aborted/live transactions to observe consistent states, important when inconsistent intermediate reads could cause exceptions or unsafe actions. Snapshot stability alone does not ensure opacity if uncommitted versions leak or reads mix sources.

Cross-system reads are especially risky. A database transaction snapshot combined with a live cache, filesystem, feature service, or HTTP response is not one snapshot. Capture and version external inputs, route them through a transactional boundary, or state the mixed-consistency semantics.

### Version identity and ordering

Version numbers need a total or sufficient partial order for visibility. A fixed-width counter eventually wraps. Naive unsigned comparison can treat ancient versions as new. Use a width whose wrap is impossible within all retained/reference lifetimes plus a proved modular comparison window, or coordinate a safe epoch reset. Never reuse `(object,version)` while a stale reference may exist.

The ABA problem is version identity loss: a location holds pointer/value A, changes, then again appears as A, misleading compare-and-swap or validation. Tags reduce risk only with a no-wrap proof. Immutable objects plus never-reused identity within the protection window, hazard pointers, epochs, or wider stamped references address different cases.

Commit order and visibility order must align with transaction rules. Allocating ID 20 before 19 commits does not necessarily make 20 visible first. A snapshot representation may need a frontier plus exceptions for active/aborted transactions rather than one scalar.

### Lifetime and reclamation

Old versions cannot be freed while a reader might reach them. Garbage-collected heaps provide memory safety for reachable objects, though retained roots still cause space leaks. Manual systems need reference counts, hazard pointers, epochs, read-copy-update grace periods, or another proved scheme.

A common epoch design lets readers announce entry/version before loading the root, traverse without per-node locks, then announce exit. Writers retire old roots and reclaim only after every reader that could have seen them has left. Ordering between announcement and root load is essential; scanning a reader registry before a late announcement can free live state.

Database vacuum computes a horizon from active transactions and other consumers. Replication slots, backups, logical decoding/change streams, time-travel queries, and audits can extend retention. Long or abandoned readers create version bloat, cache pressure, I/O amplification, and eventual outage. Monitor oldest snapshot age, retained bytes/versions, reclamation throughput, and blockers; enforce timeouts, quotas, cancellation, or snapshot export policy without violating consumers' contracts.

Reclamation is not durability retention. A log segment may be unneeded by memory readers but required for recovery or a replica. Conversely, a durable historical row may be logically invisible. Maintain distinct horizons and delete only after all obligations pass.

### Durability, recovery, and external effects

An in-memory root swap is atomic but not crash durable. A durable MVCC system orders write-ahead log, data/index pages, commit record, flush, and acknowledgment according to its recovery protocol. After crash, a transaction is wholly committed or aborted; indexes and visibility metadata must reconstruct the same state.

Copy-on-write filesystems and trees publish new roots after child blocks are durable enough for the claimed crash model. Torn sectors, reordered writes, checksums, superblock rotation, and storage caches matter. “Immutable block” does not guarantee it reached stable storage.

External side effects cannot be rolled back by hiding a version. Use transactional outbox/intents, stable commit IDs, idempotent dispatch, and reconciliation. A snapshot query that triggers an irreversible action needs freshness and commit-success requirements, not only internal consistency.

### Performance model

Readers may become one root load plus immutable traversal, avoiding lock coherence traffic. Writers pay path copying or version creation, validation, indexing, allocation, cache misses, publication, and reclamation. Snapshot isolation can reduce read/write blocking but increase aborts under write contention or serializable dependency checks.

Measure version-chain length, visibility-scan cost, copied nodes/bytes, root contention, commit validation time, abort cause/rate, reader latency, oldest snapshot age, retained bytes, vacuum/reclamation lag, replica horizon, cache locality, fragmentation, and recovery volume. Benchmark realistic long readers and failures; steady short transactions hide the dominant tail risk.

Batching updates can reduce copied paths and root swaps but increases publication latency and conflict surface. Compaction shortens chains at CPU/I/O cost. Adaptive policies must preserve visibility and retention contracts under overload.

### Evidence strategy

For persistent structures, test old roots after every new update, random branch-from-old operations where supported, aliasing, equality, iteration, exceptions, and concurrent publication. Compare each version with a simple copied reference model. Property-test that updates affect exactly declared keys and shared nodes remain immutable.

For MVCC, generate histories with reads, writes, predicates, commit/abort, retry, deletion, schema/index change, long snapshots, wrap boundaries, crash points, replica lag, and reclamation. Record version selection and construct serialization graphs. Use targeted write-skew and phantom tests. Verify recovery and index/table agreement.

For memory safety, delay readers at every announcement/load/dereference/exit boundary while writers publish and reclaim. Use sanitizers/model checking where applicable. Vary counter widths near wrap. Fault allocation and persistence. One clean stress run is neither a proof of lifetime safety nor serializability.

## Definitions and Notation

- `R_v`: immutable root published for logical version v.
- `V_x`: ordered committed versions of item x.
- `r(T)`: snapshot/read version of transaction T.
- `w(T)`: commit version of T if committed.
- `WS(T)`: write set of T.
- `RS(T)`: item and predicate read dependencies of T.
- `visible(x,T)`: greatest committed version of x allowed by T's snapshot, overridden by T's own write.
- `T_i →rw T_j`: T_i read a version or predicate later overwritten by T_j, a read/write anti-dependency.
- `H`: version/reclamation horizon.
- `retire(R_v)`: remove R_v from publication while retaining storage until safe.

Snapshot stability is `visible(x,T)` remaining fixed for all repeated reads unless T writes x. Serializability additionally requires a serial order consistent with the committed history; stability alone does not supply it.

## Mechanisms, Invariants, or Proof Structure

### Persistent-structure induction

Assume every node reachable from old root R is immutable. An update allocates new nodes along affected paths, points their unchanged edges to old immutable subtrees, initializes all fields, and never modifies a reachable old node. Induction from changed leaf to new root proves R still denotes the old value and R' denotes the functional update.

### Publication proof

Writer fully constructs transitively immutable R', then release-stores the shared root. Reader acquire-loads that root before dereferencing. The synchronizes-with edge makes construction happen-before traversal. Atomic root replacement prevents mixed roots; lifetime protection prevents reclamation during traversal.

### SI anomaly proof

T_A and T_B share snapshot `(A=true,B=true)`. Each makes a decision based on the item the other later writes, so there are anti-dependencies in both directions. Disjoint write sets let both pass SI write-conflict validation. The two-edge cycle prevents a serial order and final false/false violates the invariant.

### Reclamation proof

Define H so every active reader can reach only versions `v ≥ H` or explicitly pinned exceptions. Retire older unreachable roots, wait until every reader that could have loaded them before retirement has passed a grace condition, then reclaim. Prove announcement/load ordering, registry visibility, nesting, cancellation, thread death, and version nonreuse.

## Alternatives and Trade-Offs

| Approach | Main benefit | Principal limitation |
|---|---|---|
| Full copy per snapshot | simple isolation | O(n) time/space per update |
| Persistent path copying | cheap old versions | allocation, indirection, reclamation |
| Atomic immutable root | simple coherent reads | writer/root contention; whole-state organization |
| Seqlock/retry scan | low writer overhead | reader retry/starvation; no history |
| Reader-writer lock | direct mutable state | read/write blocking and lock lifecycle |
| MVCC read committed | nonblocking statement snapshots | successive statements can differ |
| Snapshot isolation | stable transaction view, write-conflict prevention | write skew and phantoms |
| Serializable snapshot isolation | serializable commits with many nonblocking reads | dependency tracking and aborts |
| Predicate/explicit locking | protects declared invariants | blocking, deadlocks, query/index coupling |

Choose by semantic need, not by the label “snapshot.” A stable old root is ideal for read-mostly configuration; a business invariant may require serializable validation; a tiny mutable structure may be simpler under one lock.

## Failure Modes and Misconceptions

- **“Immutable root means immutable graph.”** Every reachable shared object must be frozen.
- **“Atomic field reads make a snapshot.”** The combined values may never have coexisted.
- **“Persistent means durable.”** Data-structure persistence is historical access, not crash persistence.
- **“MVCC is an isolation level.”** It is a mechanism supporting several visibility/validation rules.
- **“Repeatable reads are serializable.”** Stable snapshots can admit write skew.
- **“Disjoint writes do not conflict.”** They may jointly violate a read predicate.
- **“Row read sets cover queries.”** Absent rows and ranges create phantoms.
- **“Timestamp means wall time.”** logical commit/visibility order needs explicit semantics.
- **“A large tag prevents ABA.”** It needs a no-wrap/no-reuse proof for the protection window.
- **“GC solves versions.”** It prevents freeing reachable objects but not retention bloat.
- **“No active transaction means vacuum is safe.”** Replicas, backups, streams, and audit may pin history.
- **“Root swap is durable commit.”** Crash ordering and recovery are separate.
- **“Snapshot plus live cache is one view.”** Cross-system reads require coordination or mixed semantics.
- **“Readers never block writers means free concurrency.”** version creation, validation, abort, and reclamation still cost.
- **“One stress test proves reclamation.”** rare announcement/free interleavings require proof and systematic tools.

## Worked Examples

### Example 1

**Persistent map.** Updating key 9 copies a logarithmic search path and shares all other immutable subtrees. Old and new roots return different values for 9 but equal values elsewhere. **Conclusion:** history is cheap only when shared nodes never mutate.

### Example 2

**Torn pair.** Reader loads balance before a transfer and ledger total after it, producing a pair no commit contained. One atomic super-root fixes the view. **Conclusion:** component atomicity is not snapshot atomicity.

### Example 3

**Statement snapshots.** Two read-committed queries in one transaction see versions 10 and 12; a transaction snapshot sees version 10 twice. **Conclusion:** snapshot acquisition time defines repeatability.

### Example 4

**Write skew.** Both on-call transactions commit disjoint writes and remove all coverage. **Conclusion:** SI write/write validation does not protect every invariant.

### Example 5

**Phantom.** Two transactions each see zero overlapping reservations and insert a different row for the same room/time. Range dependency or invariant lock is required. **Conclusion:** predicates include absent rows.

### Example 6

**Safe publication.** A writer initializes a routing tree then release-publishes one root; an acquire reader traverses immutable children. **Conclusion:** atomic discovery and memory ordering complement immutability.

### Example 7

**Long reader.** An analytics query pins version 400 while writers reach 900; vacuum cannot remove 401–899 dependencies and storage grows. **Conclusion:** retention is part of concurrency capacity.

### Example 8

**Wraparound.** A 16-bit version counter cycles while a device sleeps holding an old reference. Naive comparison accepts reused identity as new. **Conclusion:** counter width must exceed the whole reference lifetime or use safe epochs.

### Example 9

**Crash boundary.** New tree root reaches disk before one child block; recovery finds a published pointer to incomplete state. WAL or ordered copy-on-write commit is needed. **Conclusion:** memory atomicity does not imply crash atomicity.

### Example 10

**Clinical medication configuration.** A snapshot must bind drug library, patient parameters, unit conversions, device capabilities, alarm policy, signatures, effective time, rollback, and audit, while freshness and physical-device state remain separate. Named clinical-pharmacy, nursing, biomedical, human-factors, concurrency/database, real-time/embedded, cybersecurity/privacy, quality/regulatory, operations, and independent safety reviewers must approve requirements, publication, recovery, deployment, and residual risk; none is claimed here. **Conclusion:** coherent versioning is necessary but insufficient clinical assurance.

## Cross-Program Connections

- **Functional programming:** immutable values and persistent structures make versioned reasoning compositional.
- **Databases:** MVCC, SI, SSI, predicates, vacuum, and recovery operationalize multi-version state.
- **Distributed systems:** replicas, logical clocks, consistent cuts, and lag extend visibility across nodes.
- **Operating systems:** RCU and copy-on-write publish read-mostly state and defer reclamation.
- **Storage:** immutable blocks, WAL, root switching, and recovery define crash-consistent snapshots.
- **Security:** stale authorization/configuration and snapshot export can violate revocation or confidentiality.
- **Testing:** history generation and serialization graphs expose anomalies that final-state examples may miss.
- **Safety engineering:** provenance, freshness, rollback, and independent review bind snapshots to intended use.

## References

1. James R. Driscoll, Neil Sarnak, Daniel D. Sleator, and Robert E. Tarjan, “Making Data Structures Persistent,” *Journal of Computer and System Sciences* 38(1), 1989. <https://doi.org/10.1016/0022-0000(89)90034-2>
2. Yehuda Afek, Hagit Attiya, Danny Dolev, Eli Gafni, Michael Merritt, and Nir Shavit, “Atomic Snapshots of Shared Memory,” *Journal of the ACM* 40(4), 1993. <https://doi.org/10.1145/153724.153741>
3. Philip A. Bernstein and Nathan Goodman, “Multiversion Concurrency Control—Theory and Algorithms,” *ACM Transactions on Database Systems* 8(4), 1983. <https://doi.org/10.1145/319996.319998>
4. Hal Berenson et al., “A Critique of ANSI SQL Isolation Levels,” SIGMOD 1995. <https://doi.org/10.1145/223784.223785>
5. Alan Fekete, Dimitrios Liarokapis, Elizabeth O'Neil, Patrick O'Neil, and Dennis Shasha, “Making Snapshot Isolation Serializable,” *ACM Transactions on Database Systems* 30(2), 2005. <https://doi.org/10.1145/1071610.1071615>
6. Michael J. Cahill, Uwe Röhm, and Alan D. Fekete, “Serializable Isolation for Snapshot Databases,” SIGMOD 2008. <https://doi.org/10.1145/1376616.1376690>
7. Dan R. K. Ports and Kevin Grittner, “Serializable Snapshot Isolation in PostgreSQL,” VLDB 2012. <https://doi.org/10.14778/2367502.2367523>
8. PostgreSQL Global Development Group, *PostgreSQL 18: Introduction to MVCC*; retrieved 2026-08-29. <https://www.postgresql.org/docs/current/mvcc-intro.html>
9. PostgreSQL Global Development Group, *PostgreSQL 18: Transaction Isolation*; retrieved 2026-08-29. <https://www.postgresql.org/docs/current/transaction-iso.html>
10. Linux Kernel Contributors, *What Is RCU? -- “Read, Copy, Update”*; retrieved 2026-08-29. <https://docs.kernel.org/RCU/whatisRCU.html>

## Exercises

### Exercise 1

Prove path copying for one update to a persistent balanced search tree preserves the old root. Include aliasing, exceptions, publication, identity, and complexity.

### Exercise 2

Specify an MVCC visibility function for committed, active, aborted, deleted, and self-written versions. Contrast statement and transaction snapshots.

### Exercise 3

Construct and analyze a snapshot-isolation write-skew and a phantom anomaly. Give three sound prevention strategies and their trade-offs.

### Exercise 4

Design publication and reclamation for an in-memory versioned routing table with long readers, cancellation, counter wrap, and configuration rollback.

### Exercise 5

A clinical decision service reads a patient snapshot and versioned medical knowledge. Specify snapshot, serializability, freshness, durability, recovery, security, evidence, and required human review.

## Answers to the Exercises

### Answer 1

Assume old root R reaches only immutable nodes and a balanced search path has O(log n) nodes. Allocate replacements from the changed leaf upward; each new node copies unchanged fields/edges and points changed edge to the new child. Do not mutate any node reachable from R. If allocation or comparison fails, discard private nodes and publish nothing. By induction upward, each new subtree represents the functional update while each old subtree is unchanged; hence R retains the old map and R' represents the new map. Fully initialize R', then atomically release-publish it; readers acquire-load and pin its lifetime. Durable identity uses version/content metadata, not reused addresses. Work and new space are O(log n), subject to balancing rotations copying every affected path. Shared unchanged storage is counted once but remains retained while either root is live.

### Answer 2

Let T have snapshot description S, including visibility frontier and active/aborted exceptions. First return T's newest own write, including own tombstone. Otherwise choose the newest version of x whose creator committed before/within S, is not aborted or still active relative to S, and whose deletion/replacement is not visible to S. A tombstone yields absence. Never expose uncommitted other writes. Read committed obtains S per statement, so two statements can see intervening commits; a transaction snapshot fixes S for all statements and adds read-your-writes. Scalar commit IDs suffice only if assignment/publication form a valid frontier; gaps may require active-transaction metadata. Schema, index, and external-source visibility must follow compatible rules.

### Answer 3

Write skew: two on-call transactions read the other true and write distinct own rows false; their two read/write anti-dependencies form a cycle while SI sees no write/write collision. Phantom: two transactions query an empty reservation predicate and insert different qualifying rows; row read sets omit the absent rows. Prevent with serializable/SSI dependency detection and retry; predicate/range locks that block conflicting inserts; or materialize the invariant in a guardian/counter row both transactions lock or update. SSI retains concurrency but tracks dependencies and may abort; predicate locks couple behavior to access paths and can block/deadlock; guardian rows simplify correctness but create contention and require complete use by every writer. Direct business-constraint support may be best when available.

### Answer 4

Build a transitively immutable table with stable logical version and parent. Writers validate inputs, fully initialize a private root, then release-CAS/store it; readers enter a protection epoch before acquire-loading and exit on every success, error, or cancellation path. Retire replaced roots and reclaim after all pre-retirement readers pass a grace period and no rollback/audit pin remains. Monitor oldest pin and retained bytes; bound reader duration or spill/export snapshots under policy. Use a version width and modular window proved not to wrap within maximum pin/rollback lifetime, or coordinated epoch reset with no stale references. Rollback publishes a new version derived from an old root rather than mutating history. Persist configuration/signature before acknowledgement if crash recovery is claimed; test delayed readers at announcement/load/exit and wrap boundaries.

### Answer 5

Bind patient observations, units, provenance/effective time, consent, device context, knowledge/rule versions, interaction data, model/toolchain, configuration, and policy into one declared input snapshot. Specify whether decisions need serializable coordination with orders/allergies and use SSI, invariant locks, or transactional materialization rather than assuming SI. State maximum staleness and revocation/emergency refresh rules. Commit decision, explanation, knowledge IDs, and audit atomically or through durable idempotent intents; define WAL/backup/replica recovery, rollback, and reconciliation. Authenticate snapshots, authorize historical access, minimize/encrypt protected data, sign/version governed knowledge, and audit exports. Verify history/anomaly tests, reference cases, long-reader/vacuum pressure, crashes, lag, cancellation, version wrap, rollback, tampering, unavailable dependencies, and fail-safe behavior. Named clinical-specialty, pharmacy, nursing, informatics, statistics/model, database/concurrency, security/privacy, human-factors, quality/regulatory, operations, and independent safety reviewers must approve intended use, evidence, override, monitoring, and residual risk; coherent snapshots alone do not establish clinical validity or safety.
