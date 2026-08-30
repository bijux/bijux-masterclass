---
module_id: DBE-049
program: Database Engineering
level: 1
module_number: 49
title: Serializable Snapshot Isolation
status: complete
last_verified: 2026-08-30
---

# Serializable Snapshot Isolation

## One-Page Review

### Governing question

How can a database preserve snapshot isolation's nonblocking reads while rejecting every committed history that could violate serializability?

### Essential definitions

A **serialization graph** has committed transactions as vertices and dependencies as directed edges. A `wr` edge orders a writer before a reader of its version; a `ww` edge orders successive writers; an **`rw` antidependency** orders a reader before a concurrent writer whose later version the reader did not see. Under snapshot isolation, `wr` and `ww` relationships follow snapshot/version order, so cycles require special adjacent `rw` edges. A **dangerous structure** is `T1 -rw-> T2 -rw-> T3` with the relevant concurrency and commit-order conditions. **Serializable snapshot isolation (SSI)** runs transactions on snapshots, tracks enough reads and writes to detect dangerous structures, and aborts selected transactions before unsafe histories can all commit. A **predicate read** includes qualifying existing rows and gaps/conditions through which a later write could have changed the result. A **safe snapshot** cannot place a read-only transaction in a serialization anomaly; a **deferrable** read-only transaction may wait for one.

### Central model, mechanism, or theorem

Dangerous-structure theorem: every serialization anomaly under snapshot isolation contains adjacent antidependencies `T1 -rw-> T2 -rw-> T3`, where T3 is the first transaction in that cycle to commit; T1 and T2 overlap, T2 and T3 overlap, and T1 may equal T3 in a two-transaction cycle. Therefore, preventing all commit-order-qualified dangerous structures is sufficient for serializability. The converse is false: such two-edge structure may exist without a closing path from T3 to T1, so conservative SSI can abort a history that was actually serializable.

### Critical invariants

- Read tracking covers rows, predicates, and plan-dependent access paths that a concurrent write could invalidate.
- Dependency direction is derived from version visibility, never guessed from statement or commit timestamps alone.
- Conflict metadata outlives a transaction when overlapping transactions can still complete a dangerous structure.
- A dangerous structure is resolved before all participating transactions become irrevocably committed.
- Victim selection never attempts to abort an already committed transaction and aims for safe retry.
- Coarsening or summarizing tracking may add false positives but must not introduce false negatives.
- Read-only optimization is used only after the snapshot is proven safe under its theorem.
- Every serialization failure discards the entire attempt and triggers bounded whole-transaction retry.

### Common failures

Failures include calling every MVCC serializable mode SSI; treating SI read sets as row IDs only; confusing nonblocking SIREAD metadata with blocking locks; reversing `rw` edges; requiring a full cycle before acting; assuming every dangerous structure is an anomaly; releasing conflict state at commit too early; losing predicate coverage on a new index/scan plan; treating lock promotion as a correctness failure rather than a precision loss; assuming read-only transactions cannot participate in anomalies; using deferrable on writers; retrying only the failed statement; trusting results from an aborted read; or interpreting a serialization-error rate without transaction-class and contention context.

### Compact example

Doctors A and B are initially on call. T1 reads B and later writes A off; T2 reads A and later writes B off. T1's read of old B gives `T1 -rw-> T2`; T2's read of old A gives `T2 -rw-> T1`. With T1 committing first, the theorem instance is `T1 -rw-> T2 -rw-> T1` where T3 equals T1. Plain SI admits disjoint writes; SSI must abort one attempt. By contrast, `A -rw-> B -rw-> C` with no path C-to-A is dangerous-looking but acyclic, illustrating a possible conservative abort.

### Connections

Retrieve [Snapshot Visibility](047-snapshot-visibility.md), [Isolation Levels](048-isolation-levels.md), and [Read and Write Anomalies](042-read-and-write-anomalies.md). Continue through the Database Engineering [roadmap](../ROADMAP.md) to DBE-050, Concurrency-Control Testing, and the Level II transaction/recovery material.

## Governing Question

What must an SSI implementation observe, retain, and reject so that a set of snapshot transactions has a serial explanation without turning every read into a blocking lock?

## Why This Matters

Snapshot isolation is attractive because readers use stable committed versions and normally do not block writers. It also prevents concurrent write-write collisions in the same logical item. Yet write skew shows that those properties do not imply serializability. Adding ad hoc locks to every application can repair known cases, but it shifts predicate coverage, lock ordering, and missed-writer risk into every team.

SSI uses a theorem about snapshot-isolation serialization graphs to centralize that protection. Instead of blocking every reader/writer conflict, the database records read-write antidependencies and aborts only when their pattern could close a serialization cycle. It can therefore retain much of SI's concurrency while providing a serializable contract to successfully committed transactions.

The mechanism changes operational behavior. Reads create nonblocking dependency metadata; transaction commit is not necessarily the end of that metadata's lifetime; sequential scans can require coarse predicate coverage; memory pressure can promote fine tracking into coarser tracking; and correct protection appears to applications as serialization failures. False-positive aborts are acceptable for safety, but excessive aborts can violate availability and latency objectives.

PostgreSQL has shipped production SSI since 9.1 and documents its current serializable level as repeatable-read snapshot behavior plus monitoring for serialization anomalies. Its `SIReadLock` entries are predicate-read markers, not locks that block writers. Current PostgreSQL documentation also exposes read-only safe-snapshot behavior, `SERIALIZABLE READ ONLY DEFERRABLE`, plan-sensitive predicate-lock granularity, and configuration controlling predicate-lock memory/promotion. Those concrete choices illuminate the general proof, but they are not a universal SSI API.

## Prerequisites and Retrieval

You should understand MVCC snapshots, transaction overlap, read-from/version order, directed graphs, cycle detection, predicates and index ranges, commit/abort, isolation levels, write skew, locks, deadlocks, and idempotent retry. Retrieve `wr`, `ww`, `rw` antidependency, serialization graph, snapshot isolation, first-committer-wins, phantom, predicate read, topological order, safe retry, false positive/negative, and read-only transaction.

DBE-048 established isolation as a set of admitted histories and reproduced a two-transaction SI anomaly. This module derives the structure an SSI engine must detect. DBE-050 will broaden the evidence from one graph to deterministic database schedules, model-based exploration, crash boundaries, and production telemetry.

## Learning Objectives

After this module, you can:

1. construct `wr`, `ww`, and `rw` edges from a multiversion history;
2. explain why SI serialization cycles require adjacent `rw` antidependencies;
3. state the commit-order-qualified dangerous-structure theorem and its assumptions;
4. distinguish a necessary dangerous structure from a complete cycle;
5. trace detection, commit checking, victim selection, and safe retry;
6. explain predicate-read tracking across tuples, pages, ranges, relations, and access plans;
7. reason about metadata retention, summarization, promotion, prepared transactions, and memory bounds;
8. derive the read-only safe-snapshot condition and deferrable trade-off;
9. design application retry, observability, and capacity controls for SSI; and
10. test both prevented anomalies and acceptable false-positive abort behavior.

## Core Exposition

**Start from a multiversion serialization graph.** Each committed transaction is a vertex. Edges express ordering forced by observed versions:

- `Ti -wr-> Tj` when Ti writes the version Tj reads, so Ti must precede Tj.
- `Ti -ww-> Tj` when Tj installs the next version after Ti's version, so Ti must precede Tj.
- `Ti -rw-> Tj` when Ti reads a version and concurrent Tj writes a later version that Ti did not see; Ti must precede Tj in any serial explanation.

The last edge is called an antidependency because it arises from a read that missed a concurrent write, not from data flowing from writer to reader. Its direction is reader to writer. Predicate reads count: if Ti reads all rows satisfying P and Tj inserts a new P-row invisible to Ti's snapshot, `Ti -rw-> Tj` exists even though no physical row read by Ti was overwritten.

A history is serializable exactly when its applicable serialization graph is acyclic. A topological order then supplies a serial order. But maintaining the complete graph and searching every path may be expensive. SSI relies on stronger structure specific to snapshot isolation.

**Why SI cycles need consecutive antidependencies.** Under SI, a `wr` dependency means the writer committed before the reader's snapshot, and `ww` order is constrained by installed versions/first-committer-wins. These forward visibility/version relationships cannot alone wrap around an SI cycle. The original results show every SI serialization cycle contains `T1 -rw-> T2 -rw-> T3`, with T3 the earliest committer in that cycle. Each antidependency connects concurrent transactions; T1 and T2 overlap, and T2 and T3 overlap. For a two-transaction cycle, T1 and T3 can be the same transaction.

This is a necessary-pattern theorem. If the engine ensures no qualifying dangerous structure survives commit, then no cycle survives, hence the committed history is serializable. It need not prove a closing path `T3 ...-> T1`. That omission makes detection practical but conservative: some acyclic graphs contain the two edges and may be aborted.

Commit ordering reduces false positives. If T1 or T2 committed before T3, then T3 was not first among the putative cycle, so that instance cannot satisfy the theorem. Implementations can retain enough transaction state to use this fact. Exact rules and victim choices are implementation-specific; the durable logic is that ordering filters must never discard a structure that could witness a cycle.

The executable model checks two finite graphs. It enumerates commit-qualified adjacent `rw` edges and separately tests acyclicity. The cyclic write-skew graph contains a real theorem witness. The chain graph contains the same local witness but has a topological order, demonstrating that dangerous is necessary rather than sufficient.

<!-- bijux-verify: {"id":"ssi-dangerous-structure","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"anomalous_edges=(('T1', 'T2'), ('T2', 'T1'))\nanomalous_dangerous=(('T1', 'T2', 'T1'),)\nanomalous_serializable=False\nacyclic_edges=(('A', 'B'), ('B', 'C'))\nacyclic_dangerous=(('A', 'B', 'C'),)\nacyclic_serializable=True\ndangerous_is_necessary_not_sufficient=True\nevidence=finite_ssi_graphs\n","stderr":""}} -->
```python
def dangerous_structures(vertices, rw_edges, commit_rank):
    structures = set()
    for first, middle in rw_edges:
        for candidate_middle, last in rw_edges:
            if middle != candidate_middle:
                continue
            if commit_rank[last] <= commit_rank[first] and commit_rank[last] < commit_rank[middle]:
                structures.add((first, middle, last))
    return tuple(sorted(structures))

def is_acyclic(vertices, edges):
    incoming = {vertex: 0 for vertex in vertices}
    outgoing = {vertex: set() for vertex in vertices}
    for left, right in edges:
        if right not in outgoing[left]:
            outgoing[left].add(right)
            incoming[right] += 1
    ready = sorted(vertex for vertex, degree in incoming.items() if degree == 0)
    visited = 0
    while ready:
        vertex = ready.pop(0)
        visited += 1
        for target in sorted(outgoing[vertex]):
            incoming[target] -= 1
            if incoming[target] == 0:
                ready.append(target)
                ready.sort()
    return visited == len(vertices)

anomalous_vertices = {"T1", "T2"}
anomalous_edges = {("T1", "T2"), ("T2", "T1")}
anomalous_commit = {"T1": 1, "T2": 2}
acyclic_vertices = {"A", "B", "C"}
acyclic_edges = {("A", "B"), ("B", "C")}
acyclic_commit = {"A": 2, "B": 3, "C": 1}

anomalous_dangerous = dangerous_structures(
    anomalous_vertices, anomalous_edges, anomalous_commit
)
acyclic_dangerous = dangerous_structures(acyclic_vertices, acyclic_edges, acyclic_commit)
anomalous_serializable = is_acyclic(anomalous_vertices, anomalous_edges)
acyclic_serializable = is_acyclic(acyclic_vertices, acyclic_edges)

print(f"anomalous_edges={tuple(sorted(anomalous_edges))}")
print(f"anomalous_dangerous={anomalous_dangerous}")
print(f"anomalous_serializable={anomalous_serializable}")
print(f"acyclic_edges={tuple(sorted(acyclic_edges))}")
print(f"acyclic_dangerous={acyclic_dangerous}")
print(f"acyclic_serializable={acyclic_serializable}")
print(f"dangerous_is_necessary_not_sufficient={bool(acyclic_dangerous) and acyclic_serializable}")
print("evidence=finite_ssi_graphs")
```

The code assumes all supplied edges are already valid `rw` antidependencies between overlapping SI transactions. It omits snapshots, versions, predicates, `wr`/`ww` edges, subtransactions, prepared state, abort races, summarized transactions, and a real SSI scheduler. It proves only the stated finite graph results.

**Detection starts with reads, not writes alone.** When Ti reads a tuple, range, or relation, the engine records that a later concurrent write affecting that read could create `Ti -rw-> Tj`. When Tj writes, it checks relevant read markers and records conflicts. This tracking must represent absence: “no reservation in this interval” has no returned tuple, yet an inserted overlapping reservation changes the predicate result.

PostgreSQL calls its nonblocking read markers predicate locks and displays them as `SIReadLock`. The name can mislead. They do not make a writer wait and do not participate in ordinary lock deadlocks; they preserve enough information to detect dependencies. Blocking tuple/table locks used by writes and explicit locking are separate mechanisms that can still wait or deadlock.

Access plans affect tracking granularity. An index range can often mark narrower key/page coverage; a sequential scan may require relation-level coverage. A correct new index access method must either provide accurate predicate-lock hooks or fall back to conservative coverage. Plan changes can therefore alter false-positive rates without changing the serializability guarantee.

**Bounded memory requires conservative coarsening.** Fine-grained read markers and transaction graph state cannot grow without limit. An implementation may combine tuple markers into page markers, page markers into relation markers, or summarize completed transactions. Coarsening makes more writes appear relevant, increasing false positives, but must never omit a real dependency. This is the same safety direction as a conservative static analysis: precision may fall; soundness must remain.

Current PostgreSQL exposes `max_pred_locks_per_transaction`, `max_pred_locks_per_relation`, and `max_pred_locks_per_page`. These parameters govern shared tracking capacity and promotion thresholds, not a fixed maximum count of rows a transaction may read. Raising them uses memory; leaving them too low for broad access can promote markers and increase serialization failures. Query/index design, transaction size, and capacity settings interact.

**Conflict metadata can outlive commit.** Suppose T3 commits while overlapping T2 remains active, and T2 overlaps T1. T3's application work is done, but its ordering/conflict facts may still be required to decide whether T1/T2 can complete a dangerous structure. Releasing all metadata at transaction commit would create a false negative. Implementations retain or summarize state until no active transaction can form a relevant path.

Prepared transactions, subtransactions/savepoints, parallel queries, replication, recovery, and transaction-ID lifecycle complicate ownership and retention. A subtransaction abort must remove its logical effects without erasing parent conflicts; a prepared transaction may remain in-doubt for a long time; recovery must not resurrect a history without necessary ordering state. The implementation proof must cover these paths, not just ordinary `BEGIN/COMMIT`.

**Abort policy protects safety and retry progress.** Once a dangerous structure and commit condition require action, abort any still-abortable participant whose removal breaks the threat. A production policy also seeks **safe retry**: immediately retrying the selected victim should not recreate the identical failure with the same already-committed participant. The PostgreSQL implementation paper explains why aborting the middle transaction T2 when possible achieves this for its structure: after T3 has committed, retried T2 no longer overlaps T3 and cannot recreate that same outgoing antidependency.

Safe retry is narrower than guaranteed success. A retry can meet new conflicting transactions, a constraint error, deadlock, timeout, cancellation, resource exhaustion, or a business rejection. Applications still need bounded attempts, deadlines, jitter appropriate to contention, stable operation identity, and explicit exhaustion behavior.

An abort must occur before all necessary participants become irrevocable. Commit-path checks and concurrency-safe state transitions must handle simultaneous commits. The engine cannot report success and later retract it. Conservative early abort may waste work; delayed resolution can reduce unnecessary aborts but increases state/race complexity.

**Read-only transactions need theorem-aware treatment.** “It writes nothing” does not mean it cannot complete a serialization cycle. A read-only transaction can be T1 in `T1 -rw-> T2 -rw-> T3`, with another dependency returning from T3 through the graph. The refined theorem says that if T1 is read-only, T3 must have committed before T1 acquired its snapshot.

This yields **safe snapshots**. Informally, a read-only snapshot is safe when no concurrent read/write transaction has or can develop an outgoing `rw` antidependency to a transaction committed before that snapshot. A read-only transaction on such a snapshot can execute without creating an SSI anomaly, regardless of what it reads.

PostgreSQL can discover safety for ordinary serializable read-only transactions and release tracking early. `SERIALIZABLE READ ONLY DEFERRABLE` requests a safe snapshot before executing; it may block before the first query and retry snapshot acquisition internally. Once safe, the report avoids serialization failure from SSI and read-tracking overhead. This is useful for long analytical reads that prefer startup delay to mid/late abort. It is not for writers, does not promise a bounded wait, and does not make the snapshot fresh at query completion.

**False positives are a liveness/capacity concern, not silent corruption.** A dangerous structure without a closing path can be aborted even though the history was serializable. Coarse predicate tracking can create additional apparent overlaps. The contract remains safe because valid histories are rejected, not invalid histories admitted. But repeated aborts consume CPU, connection time, logs, and downstream retry capacity.

Measure by transaction class: attempts, successful commits, serialization failures by SQLSTATE/vendor code, retry depth/exhaustion, elapsed work before abort, read/write set proxies, snapshot age, predicate-lock granularity, plan/index changes, active/prepared duration, pool occupancy, and tail latency. Do not log sensitive values or treat `SIReadLock` count as a universal risk score.

**Applications complete the contract.** Every invariant-bearing operation must execute as a participating serializable transaction. A read through a weaker replica/cache, a background writer at weaker isolation, or an external side effect outside the retry boundary can bypass the proof. Native constraints should remain in place; serialization can still surface constraint errors whose application handling must be correct.

On SQLSTATE `40001` or documented equivalent, discard all read results and tentative responses, roll back/release the connection safely, then rerun the entire transaction function from fresh reads. Keep an idempotency key stable across attempts. Use a transactional outbox or equivalent for messages; never email/charge before successful commit unless the external protocol itself provides a recoverable idempotent transaction.

**Verification needs positive and negative schedules.** Force the doctor write-skew schedule under plain SI/repeatable-read behavior and show both commits can produce the invalid state where supported. Repeat under SSI/serializable and require that not all unsafe attempts commit: one may abort, block into a different safe observation, or hit a constraint. Then run the aborted transaction through the real retry loop and require a valid committed result.

Also test an acyclic history with antidependencies. It may commit or conservatively abort; both can be correct under SSI, but retry exhaustion/latency gates still matter. Test empty predicates, index and sequential plans, plan changes, coarse tracking, long read-only transactions, deferrable startup wait, savepoint rollback, prepared state if used, cancellation, connection loss, and deployment configuration. A green two-session example is evidence for that schedule, never a proof of all histories.

## Definitions and Notation

- `Ti -wr-> Tj`: Tj reads a version written by Ti; serial order requires Ti before Tj.
- `Ti -ww-> Tj`: Tj writes the next version after Ti; serial order requires Ti before Tj.
- `Ti -rw-> Tj`: Ti reads a version/predicate and concurrent Tj writes a later result Ti did not see; Ti must precede Tj.
- **Serialization graph:** committed transactions and required-order dependency edges.
- **Serialization anomaly:** a committed history whose applicable serialization graph contains a cycle.
- **Dangerous structure:** adjacent `rw` antidependencies `T1 -rw-> T2 -rw-> T3` satisfying overlap and commit-order conditions.
- **False positive:** an aborting detected structure with no actual closing serialization-graph cycle.
- **False negative:** failure to detect an unsafe structure; unacceptable because a nonserializable history may commit.
- **Predicate read marker:** nonblocking metadata covering values or absences a concurrent write could change.
- **Promotion/coarsening:** replacing fine markers with broader ones to bound state, preserving safety while reducing precision.
- **Safe snapshot:** snapshot on which a read-only transaction cannot participate in an SSI anomaly under the proven condition.
- **Safe retry:** victim selection property preventing the identical already-known structure from aborting the immediate retry.

## Mechanisms, Invariants, or Proof Structure

The serializability proof is by contradiction. Assume a nonserializable committed SI history survives. Its serialization graph has a cycle. The SSI theorem says that cycle contains a commit-qualified dangerous structure. If the implementation soundly records every possible `rw` edge, retains the relevant overlap/order state, and prevents every such structure from all committing, that structure could not survive. Contradiction; therefore every surviving committed history is serializable.

Each premise matters. Predicate coverage establishes edge completeness. Atomic commit checking prevents simultaneous commits escaping. State retention covers transactions after commit while overlaps remain. Conservative promotion/summarization preserves edges. Victim resolution removes at least one vertex/effect before irrevocability. Recovery and prepared-state rules preserve the same invariants across exceptional paths.

The converse does not follow: two adjacent `rw` edges do not prove a path from T3 back to T1. The acyclic executable chain has a dangerous candidate and a valid topological order. This justifies conservative false positives but forbids describing every serialization failure as proof that the application would otherwise corrupt data.

For read-only T1, the incoming cycle edge cannot be `rw` or `ww` because T1 writes nothing; it must be a `wr` edge from some T0 whose version T1 sees. Thus T0 committed before T1's snapshot. Since T3 is first to commit in the cycle, T3 committed before T0 and therefore before T1's snapshot. This derivation supplies the read-only snapshot-order filter and safe-snapshot optimization.

## Alternatives and Trade-Offs

- **SSI versus plain SI:** SSI adds graph/read tracking and aborts to exclude write skew; plain SI has lower metadata cost but admits nonserial histories.
- **SSI versus strict two-phase locking:** SSI keeps ordinary reads nonblocking and resolves dangerous patterns by abort; S2PL blocks conflicts and deadlock-resolves, often with different contention behavior.
- **SSI versus full optimistic validation:** both may abort at validation; SSI exploits SI graph structure rather than necessarily comparing complete read/write sets.
- **Exact cycle detection versus dangerous structures:** exact paths could reduce false positives but require more graph state/work; local conservative detection bounds complexity.
- **Fine versus coarse predicates:** fine tracking improves concurrency but consumes memory; promotion bounds memory while increasing apparent conflicts.
- **Ordinary versus deferrable read-only:** ordinary starts promptly but may track/abort; deferrable may wait for a safe snapshot, then runs without SSI abort risk from that snapshot.
- **Serializable versus exact constraint/guard:** SSI covers dynamic dependencies broadly; constraints/guards can be simpler and cheaper for specific invariants and remain valuable defense.

## Failure Modes and Misconceptions

- “SSI detects write-write conflicts.” SI already handles overlapping same-item writers; SSI's distinctive evidence is `rw` antidependency structure.
- “A read lock blocked my writer.” PostgreSQL `SIReadLock` is nonblocking tracking; another lock or resource caused the wait.
- “Two `rw` edges prove corruption.” They are necessary evidence, not necessarily a closed cycle.
- “A full cycle must be stored.” SSI can safely act on the theorem's local dangerous structure.
- “Commit frees everything.” Overlapping active transactions may still need a committed transaction's conflict state.
- “Only returned rows matter.” Empty predicates and index gaps can be invalidated by inserts.
- “Promotion weakened serializability.” Correct promotion weakens precision, causing more false positives, not unsafe commits.
- “Read-only cannot abort.” It can participate in a cycle unless its snapshot is proven safe.
- “Deferrable makes reports current.” It trades possible startup wait for a safe historical snapshot, not completion-time freshness.
- “`40001` means retry `COMMIT`.” Reexecute the entire transaction from fresh reads.
- “Zero aborts proves SSI overhead is zero.” Tracking, memory, CPU, and retained metadata can cost resources without aborts.
- “High aborts mean the engine is wrong.” They can reflect real conflicts, conservative tracking, poor plans, long transactions, or undersized metadata; diagnose before changing isolation.

## Worked Examples

### Example 1

T1 reads old B then T2 writes B, so `T1 -rw-> T2`. The reader must precede the invisible writer in a serial explanation. Conclusion: `rw` direction is reader-to-writer, opposite the intuitive data-flow direction.

### Example 2

T1 reads predicate “no booking overlaps [10,11)” and gets empty; T2 inserts an overlapping row. No tuple read by T1 was overwritten, yet the result would change. Conclusion: predicate/gap coverage creates `T1 -rw-> T2`.

### Example 3

Doctor write skew yields `T1 -rw-> T2 -rw-> T1`; T1 commits first. Here theorem T3 equals T1, and the graph is a two-vertex cycle. Conclusion: dangerous structures do not require three distinct transactions.

### Example 4

Graph `A -rw-> B -rw-> C`, with C first to commit and no path C-to-A, is acyclic. SSI may abort conservatively. Conclusion: a dangerous structure is sufficient evidence for safe intervention, not proof of an actual anomaly.

### Example 5

A sequential scan of orders causes relation-level predicate coverage; concurrent inserts anywhere relevant generate more apparent conflicts than an indexed range scan. Conclusion: plan/index choice can change abort precision without changing the correctness contract.

### Example 6

Fine tuple markers exceed a threshold and promote to a page/relation marker. An unrelated write now appears conflicting and an acyclic transaction aborts. Conclusion: conservative coarsening bounds memory at the cost of false positives, never missing a real edge.

### Example 7

T3 commits, but T2 remains active and overlaps T1. Deleting T3's conflict record immediately would hide the required earliest-committer evidence. Conclusion: logical transaction completion and SSI metadata reclamation have different lifetimes.

### Example 8

A long read-only report starts amid heavy writers and later receives a serialization failure. Marking it serializable, read-only, deferrable makes it wait for a safe snapshot before its first query, then complete without SSI conflict tracking. Conclusion: use deferrable when startup latency is preferable to aborting expensive read work.

### Example 9

T2 is selected as victim in `T1 -rw-> T2 -rw-> T3` after T3 commits. On immediate retry, T2 no longer overlaps already-committed T3, so the same outgoing edge cannot recur. Conclusion: safe-retry victim selection improves progress but cannot exclude new conflicts.

### Example 10

An application catches `40001`, publishes a result computed by the aborted attempt, then retries only the final update. The database is serializable, but the service exposes nonexistent history. Conclusion: discard attempt results and retry the complete transaction with stable external identity/outbox discipline.

## Cross-Program Connections

- [Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) supplies dependency direction, happens-before, optimistic conflict detection, deadlock versus abort, and safe reclamation.
- [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) supplies directed graphs, incremental cycle evidence, interval/range structures, and bounded summaries.
- [Software Engineering Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) supplies deterministic barriers, model oracles, state-space exploration, and failure injection.
- [Data Engineering](../../19-data-engineering/ROADMAP.md) supplies long snapshots, analytical readers, CDC/outbox boundaries, and reconciliation.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies certification, replica visibility, distributed serializability, ambiguous commit, and idempotent retries.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md) supplies low-cardinality transaction-class metrics, trace correlation, SLOs, capacity controls, and privacy-aware diagnostics.

## References

1. Michael J. Cahill, Uwe Röhm, and Alan D. Fekete, [“Serializable Isolation for Snapshot Databases”](https://www.cs.cornell.edu/~sowell/dbpapers/serializable_isolation.pdf), *SIGMOD*, 2008; SSI algorithm, dangerous structures, and evaluation.
2. Dan R. K. Ports and Kevin Grittner, [“Serializable Snapshot Isolation in PostgreSQL”](https://www.vldb.org/pvldb/vol5/p1850_danrkports_vldb2012.pdf), *PVLDB* 5(12), 2012; production implementation, commit ordering, safe snapshots, memory, and integration.
3. Alan Fekete et al., [“Making Snapshot Isolation Serializable”](https://www.cse.iitb.ac.in/infolab/Data/Courses/CS632/2009/Papers/p492-fekete.pdf), *ACM TODS* 30(2), 2005; SI serialization-graph structure and application transformation.
4. Atul Adya, [*Weak Consistency: A Generalized Theory and Optimistic Implementations for Distributed Transactions*](https://publications.csail.mit.edu/lcs/pubs/pdf/MIT-LCS-TR-786.pdf), MIT PhD thesis, 1999; dependency-based histories and isolation models.
5. PostgreSQL Global Development Group, [Transaction Isolation](https://www.postgresql.org/docs/current/transaction-iso.html), PostgreSQL 18 current documentation, retrieved 2026-08-30; serializable behavior, retries, SIREAD locks, and deferrable reads.
6. PostgreSQL Global Development Group, [Lock Management](https://www.postgresql.org/docs/current/runtime-config-locks.html), PostgreSQL 18 current documentation, retrieved 2026-08-30; predicate-lock capacity and promotion settings.
7. PostgreSQL Global Development Group, [`pg_locks`](https://www.postgresql.org/docs/current/view-pg-locks.html), PostgreSQL 18 current documentation, retrieved 2026-08-30; observable lock-manager and predicate-marker state.
8. PostgreSQL Project Wiki, [SSI](https://wiki.postgresql.org/wiki/SSI), retrieved 2026-08-30; worked SI/SSI behaviors and application retry guidance.
9. PostgreSQL Global Development Group, [System Information Functions and Operators](https://www.postgresql.org/docs/current/functions-info.html), PostgreSQL 18 current documentation, retrieved 2026-08-30; `pg_safe_snapshot_blocking_pids` and safe-snapshot operational diagnosis.
10. Tianzheng Wang et al., [“Efficiently Making (Almost) Any Concurrency Control Mechanism Serializable”](https://arxiv.org/abs/1605.04292), 2016; serialization certification alternatives and read-tracking trade-offs.

## Exercises

### Exercise 1

Given a versioned schedule with four transactions, identify every `wr`, `ww`, and `rw` edge, state required overlap, find cycles, and list commit-qualified dangerous structures.

### Exercise 2

Prove the read-only snapshot-order condition: if read-only T1 participates in an SI anomaly through `T1 -rw-> T2 -rw-> T3`, why must T3 commit before T1's snapshot?

### Exercise 3

Diagnose a rise in PostgreSQL serialization failures after a query-plan change from an index range scan to a sequential scan. Separate correctness, predicate precision, capacity, and application retry evidence; propose safe mitigations.

### Exercise 4

Design a production SSI state model covering transaction begin/snapshot, tuple and predicate reads, writes, commit races, victim choice, post-commit retention, summarization, subtransaction abort, prepared transactions, and crash recovery. State one invariant per transition.

### Exercise 5

Design an SSI rollout for reservation allocation plus a long read-only report. Include forced histories, serial/invariant oracles, deferrable policy, retries/outbox, metrics, capacity gates, canary, rollback, and limitations.

## Answers to the Exercises

### Answer 1

Bind each read to a specific version and each successive write to version order. Add `writer -wr-> reader` for the version observed, `earlier writer -ww-> later writer` for replacement order, and `reader -rw-> concurrent later writer` when the reader saw the predecessor or predicate without that write. Do not infer `rw` merely because statements overlap: the write must affect the read result and remain invisible to that snapshot. Run cycle/topological analysis on the full graph. For every adjacent pair of `rw` edges `T1->T2` and `T2->T3`, require T1/T2 and T2/T3 overlap and test whether T3 is earliest in the candidate cycle/commit-order rule; allow T1=T3. Report insufficient evidence if versions, predicate domain, overlap, or commit outcome is missing.

### Answer 2

Because T1 is read-only, the cycle edge entering T1 cannot be `rw`—that would require T1 to write the missed later version—and cannot be `ww`. It must be `T0 -wr-> T1`, meaning T1 observed T0's version. Under SI, T0 therefore committed before T1 acquired its snapshot. The dangerous-structure theorem chooses T3 as the first transaction in the cycle to commit, so T3 committed before T0. By transitivity, T3 committed before T1's snapshot. Hence if no concurrent read/write transaction can have an outgoing `rw` edge to a transaction committed before the snapshot, read-only T1 cannot occupy the required anomaly structure; this is the safe-snapshot basis.

### Answer 3

First confirm engine/version, serializable setting on affected sessions, SQLSTATE `40001`, transaction classes, plans, indexes/statistics, predicate settings, and retry results. The sequential scan can require relation-level SIREAD coverage, so more writes appear to affect the read and more dangerous structures/false positives are detected. Serializability is not weakened; precision and liveness changed. Reproduce both plans with forced safe/unsafe schedules and serial/invariant oracles. Restore a sound selective index or statistics when query semantics/performance support it; shorten transactions; mark genuine readers read-only/deferrable where suitable; tune predicate-lock capacity only after measuring memory and promotion; bound/jitter whole retries and control concurrency. Never suppress `40001`, downgrade isolation, or add a misleading predicate solely to reduce the metric without an alternative invariant proof.

### Answer 4

Begin creates identity and declared mode; snapshot atomically records visibility/overlap. Read adds conservative tuple/range/relation markers covering every possible invalidating write. Write discovers relevant markers and records directed conflicts without blocking on SIREAD metadata. Commit atomically checks dangerous structures/order and makes either commit or abort irrevocable; victim is uncommitted and preferably safe-retry. Committed conflict state remains until no overlapping active/prepared transaction can need it. Promotion replaces fine markers with a superset; summarization retains every ordering fact needed to prevent false negatives. Savepoint abort removes logical effects but preserves parent-relevant conflicts. Prepare persists/retains outcome and graph obligations. Recovery reconstructs or conservatively represents prepared/active conflict state before admitting commits. Invariants: no real `rw` edge omitted, no unsafe structure all commits, no committed victim aborted, no needed state reclaimed, and every coarsening is a coverage superset.

### Answer 5

Inventory every allocator/report writer, isolation setting, replica/cache path, invariant, predicate/index, transaction duration, external effect, and operation identity. Force empty-predicate and doctor-style disjoint-write schedules under the current level; record reads, versions, errors, outcomes, and serial/invariant oracle. Enable SSI for every invariant participant and require unsafe schedules not all commit; run victims through bounded whole-transaction retries with a stable idempotency key and outbox insert in the same transaction. Make the long report `SERIALIZABLE READ ONLY DEFERRABLE` when startup wait is acceptable; measure safe-snapshot wait and freshness separately. Canary by tenant/transaction class with gates on invariant reconciliation, commit/abort/retry/exhaustion, wasted work, p95/p99, pools, CPU/memory, predicate promotion/granularity, snapshot age, WAL/replica/outbox lag, and report wait. Preserve prior routing/configuration for rollback, but downgrade only while exact constraints/guards provide an alternative proof. State that finite tests and telemetry cannot prove every history, engine defect absence, cross-system atomicity, or workload-independent capacity.
