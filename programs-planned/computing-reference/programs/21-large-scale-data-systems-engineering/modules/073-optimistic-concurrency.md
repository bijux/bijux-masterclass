---
module_id: LSDS-073
program: Large-Scale Data Systems Engineering
level: 2
module_number: 73
title: Optimistic Concurrency
status: complete
last_verified: 2026-09-04
---

# Optimistic Concurrency

## One-Page Review

### Governing question

How can independent writers prepare lakehouse changes concurrently, detect only semantic interference at commit time, preserve a serial explanation of accepted states, retry without repeating expensive data work, and stop safely when an outcome or assumption is uncertain?

### Essential definitions

- **optimistic concurrency control (OCC)** executes without holding a table-wide write lock, then validates assumptions before atomic publication.
- A **base snapshot** is the committed state against which an operation read and planned.
- A **read set** identifies state whose observed values influenced the proposed change.
- A **write set** identifies files, rows, partitions, metadata, or references the operation proposes to add, remove, or alter.
- A **validation predicate** states what must remain true between base and commit.
- A **serialization point** is the atomic publication event that orders successful commits.
- A **conflict** is a concurrent change that falsifies a required assumption, not merely any movement of the table head.
- **rebase** reapplies a logical action to a newer head after validating intervening commits.
- **idempotency** makes repeating the same logical request produce no additional effect after its first success.
- An **unknown outcome** means publication may have succeeded but the writer did not receive conclusive acknowledgement.

### Central model, mechanism, or theorem

Transaction $T$ reads base $b$, records assumptions $V_T$, prepares immutable action $A_T$, observes current head $h$, and may commit only when $V_T(b,h)$ holds. Publication is conditional:

$$\operatorname{CAS}(head,h,new(T,h)).$$

If CAS loses, refresh and validate again. An append may require only that compatible schema/spec/protocol remain valid; a rewrite requires every replaced input still be live; a predicate overwrite/delete must ensure intervening files cannot satisfy its predicate; metadata changes commonly require stricter version equality. Successful CAS operations impose a total commit order, but correctness depends on sufficiently strong validation. Retry reuses prepared files when their semantics remain valid and uses transaction identity to resolve replay. Unknown publication is checked before any new attempt.

### Critical invariants

- Every attempt records transaction identity, base, operation, read/write scope, validation predicate, staged objects, and outcome.
- The authoritative head changes through one atomic conditional operation; unconditional last-writer-wins publication is forbidden.
- Validation is operation-specific and includes all state that influenced results, including schema, partition, protocol, and delete semantics.
- A successful commit has a serial position and preserves every earlier nonconflicting accepted action.
- Rebase reruns validation against every relevant intervening change; it never merely substitutes a newer version number.
- Prepared immutable data may be reused only when its schema, partitioning, content, and logical intent remain valid.
- One logical ingestion/batch identity commits at most once, including after timeout or process restart.
- Unknown outcomes are resolved by transaction/snapshot status before retry or cleanup.
- Conflict retries are bounded, jittered, cancellable, and classified separately from transport/service failures.
- Metrics connect conflict type, operation, overlap scope, retries, wasted work, latency, head movement, and terminal outcome without exposing sensitive predicates.

### Common failures

Common failures include treating CAS as the entire correctness proof; validating only the head version and retrying every operation; using partition-directory equality as row-level disjointness; omitting files read by a predicate from the validation scope; allowing schema/protocol changes beneath a prepared writer; blindly retrying a lost acknowledgement; generating a new transaction ID on retry; rebuilding expensive data for a metadata-only CAS loss; infinite immediate retries under contention; using timestamps as versions; deleting staged files while a prior attempt may have committed; and reporting all conditional failures as infrastructure incidents.

### Compact example

Writers A and B both read snapshot 40. A appends file `a`; B appends file `b`. A publishes 41. B's CAS from 40 fails, but its append assumptions still hold, so it rebases `b` onto 41 and publishes 42 containing both files. Writer C read file `x` at 40 to rewrite it. If snapshot 41 removed `x`, C's CAS loss is a semantic conflict: publishing C's old replacement would resurrect or double-transform state. C aborts or recomputes. A moved head is therefore a retry signal; validation decides whether it is a conflict.

### Connections

[LSDS-050](050-reprocessing-a-stream-without-double-applying-effects.md) supplies replay identity, [LSDS-055](055-work-stealing-and-speculation.md) supplies attempt selection, [LSDS-068](068-adaptive-query-execution.md) supplies epoch reasoning, [LSDS-071](071-table-snapshots-and-atomic-commit.md) defines publication, and [LSDS-072](072-manifest-and-metadata-trees.md) defines reusable immutable metadata.

## Governing Question

Serializing an entire table behind one long-held lock is understandable but wastes parallelism. Distributed writers may spend minutes scanning, joining, sorting, and producing immutable files before a short publication step. Holding a lock throughout that work creates lease expiry, convoying, head-of-line blocking, and failure-recovery problems. Letting everyone publish unconditionally loses updates.

OCC moves coordination to the boundary. Writers read a snapshot, prepare changes independently, and validate just before an atomic commit. This works well when conflicts are uncommon or logical operations commute. It performs badly when hot writers repeatedly invalidate one another or validation is too coarse. More importantly, OCC is safe only if its predicates represent the operation's true dependencies.

The governing question is how to define those dependencies, distinguish retryable head movement from semantic conflict, preserve expensive staged work, handle unknown results and idempotency, and operate the system under contention without trading data correctness for apparent throughput.

## Why This Matters

Lakehouse tables combine many writers: streaming ingestion, batch append, correction, merge, delete, compaction, clustering, index construction, schema evolution, snapshot maintenance, and replication. These operations overlap differently. Two blind appends may commute; two rewrites of the same file do not. A delete by predicate can conflict with a concurrent append even when they touch no identical old file, because the new file may contain rows the delete intended to cover.

Weak validation produces silent anomalies: lost updates, resurrected rows, missed deletes, duplicate batches, incompatible encodings, or broken delete applicability. Excessively strong validation produces avoidable aborts and wasted compute. The engineering objective is semantic precision, not the fewest conflicts at any cost.

OCC also crosses system boundaries. The catalog or log must offer a genuine conditional serialization primitive. Object writes, credentials, network timeouts, application checkpoints, and cleanup all participate. An error response can mean “condition false,” “definitely not attempted,” or “outcome unknown”; collapsing them is unsafe.

## Prerequisites and Retrieval

Review idempotent replay in [LSDS-050](050-reprocessing-a-stream-without-double-applying-effects.md), speculative attempts in [LSDS-055](055-work-stealing-and-speculation.md), adaptive epochs in [LSDS-068](068-adaptive-query-execution.md), atomic table commits in [LSDS-071](071-table-snapshots-and-atomic-commit.md), and immutable metadata graphs in [LSDS-072](072-manifest-and-metadata-trees.md).

You should understand CAS, conditional create/update, MVCC, serializability, snapshot isolation, write skew, read/write sets, immutable files, set algebra, predicates, stable identities, retries, exponential backoff, idempotency keys, leases, fencing, checksums, and distributed failure ambiguity.

For diagnosis retain the base and attempted head, intervening commits, operation predicate, normalized read/write scope, validation result, staged-object inventory, transaction ID, conditional-request identity, response/error classification, retry trace, and final published snapshot. Without these artifacts, “conflict” often becomes an unverifiable label.

## Learning Objectives

After this module, you should be able to:

1. Separate optimistic execution, semantic validation, and atomic publication.
2. Define read sets, write sets, and validation predicates for common table operations.
3. Distinguish a CAS race from an actual logical conflict.
4. Explain why file-level conflict detection may miss predicate and metadata anomalies.
5. Prove when append rebasing preserves both writers and when rewrite rebasing is unsafe.
6. Reuse prepared immutable objects without reusing stale assumptions.
7. Design idempotent retries and resolve unknown commit outcomes.
8. Choose bounded backoff, admission, serialization, or ownership for hot tables.
9. Instrument conflict type, overlap, retry cost, and wasted work.
10. Test adversarial schedules, timeouts, crashes, evolution, and maintenance races.

## Core Exposition

### Transaction model

Represent transaction $T$ as

$$T=(id,b,R_T,W_T,V_T,A_T),$$

where $id$ is stable logical identity, $b$ is base snapshot, $R_T$ is the semantic read set, $W_T$ is intended write scope, $V_T$ is a predicate over base/current/intervening state, and $A_T$ is the reusable logical action plus staged immutable objects. These elements need not be literal materialized sets; a predicate range, partition filter, schema ID, or referenced-file set can encode them.

The lifecycle is read, plan, stage, refresh, validate, publish, confirm. Staging may be distributed and speculative. Only selected attempt outputs enter $A_T$. Publication conditionally advances a catalog pointer or creates a unique next log version. Confirmation associates $id$ with the published result.

### CAS is necessary but insufficient

CAS prevents two writers from both replacing the same observed head. Suppose A publishes first; B fails its conditional operation. If B simply changes expected head and retries unchanged metadata, it can overwrite A. Safe rebase constructs a new candidate containing A's accepted changes and B's action, then applies $V_B$.

Even a perfect CAS does not reveal whether actions commute. That is a semantic property. Let state-transition functions be $f_A$ and $f_B$. For a shared base $S$, operations commute when

$$f_B(f_A(S))=f_A(f_B(S))$$

and both preconditions remain true. Blind append of distinct immutable files often commutes. Overwrite, merge, delete, schema update, and maintenance require stronger analysis.

### Operation-specific validation

**Append:** ensure table identity, compatible schema/spec/protocol, valid target branch, and no operation policy invalidates the append. Reuse staged data and add it to the latest compatible head. If append semantics promise uniqueness by business key, file-disjointness is not enough.

**Rewrite or compaction:** record exact input files. Commit only if all inputs remain live and no required delete/sequence semantics changed. Concurrent additions may be harmless if not meant for the rewrite; removal of any input is normally terminal for that prepared result.

**Overwrite/delete by predicate:** validate that files read or removed remain valid and that intervening additions cannot contain predicate-matching rows when the operation promises to affect the table as observed through commit. Partition summaries can reduce validation scope only when predicate projection is inclusive.

**Merge/upsert:** capture match predicate, source identity, candidate target files, uniqueness assumptions, and intervening files that could match. Row-level concurrency may reduce false conflicts but needs stable row identity and delete/update semantics.

**Metadata/protocol/schema/partition change:** validate field/spec IDs, compatibility, required features, and concurrent metadata changes. These changes often conflict table-wide because writers prepared encodings under the old contract.

**Snapshot expiration/cleanup:** validate reachability, retained references, unknown attempts, and maintenance ownership. Physical deletion is not safely rebased from a stale reachability scan.

### Intervening-change validation

If base $b$ remains an ancestor of head $h$, inspect commits on path $(b,h]$. Summaries can accelerate conflict checks, but must be conservative. Compare added/removed files, partitions, predicates, schema/spec/protocol changes, delete files, sequence ranges, and reference movement relevant to $V_T$.

If $b$ is no longer on the target branch—perhaps because of rollback or reference replacement—the history diverged. A normal forward rebase may not be meaningful. Fail with a distinct terminal classification unless the operation has an explicit divergent-history rule.

Validation itself races with publication. It cannot validate, pause, then unconditionally write. The candidate built on observed head $h$ must publish with CAS expecting exactly $h$. If another commit wins, repeat refresh and validation.

### Isolation and anomalies

Atomic snapshots give readers a consistent version. OCC validation determines writer isolation. Snapshot isolation that detects overlapping file writes can still permit write skew when two transactions read disjoint records and update disjoint files based on a shared invariant. If the application needs serializability—such as “at most one active leader”—the invariant must be represented in a common conflict key, constraint service, or serializable coordinator.

State the guarantee precisely: atomic snapshot publication, snapshot-isolated reads, operation-specific conflict detection, serializable table metadata, or serializable application invariants are different claims.

### Reuse, retry, and idempotency

Prepared content is usually immutable and expensive; metadata is cheaper. Structure retries so files are named by attempt and can be referenced from a rebased candidate without rewriting. Reuse requires unchanged logical rows, compatible schema/spec/encoding, selected attempt ownership, and durable integrity. Never reuse an overwrite output after its inputs or predicate meaning changed.

Keep one logical transaction ID across retries. Record it in table commit metadata or a coordinated ledger. Before executing or publishing a retry, search for that identity. A new process should recover the same ID from durable application state, not invent one.

### Unknown outcomes

After sending the conditional publish, the client may time out. The operation might have failed before reaching the service, lost the CAS, or succeeded while its response was lost. Mark it unknown. Resolve by refreshing the authoritative head/history and locating transaction ID, proposed snapshot, commit token, or exact metadata identity. If found, confirm success. If a later incompatible commit exists without the identity, apply protocol-specific reasoning; do not assume absence from one stale read proves failure.

Staged objects from an unknown attempt are not orphans. Cleanup waits until outcome resolution, retention, and reachability establish safety.

### Contention control

Under high contention, immediate retries synchronize writers and amplify waste. Use capped exponential backoff with jitter, retry/time budgets, cancellation, and observability. Limit concurrent committers independently from data-producing tasks. Prefer early conflict detection when reliable markers or ownership signals can stop doomed work.

When conflicts are structurally frequent, change architecture: partition ownership, per-key/partition serialization, microbatch aggregation, a commit queue, sharded tables, merge service, or pessimistic lease with fencing. Locks require durable ownership, timeout, renewal, and fencing; a stale lock holder must not publish after losing its lease.

### Observability and testing

Measure attempts per logical transaction, CAS losses, semantic conflicts by class, validation scan time/bytes/commits, backoff, end-to-end commit latency, staged and reused bytes, recomputed work, abandoned objects, unknown outcomes and resolution time, queue depth, and success after retry. Segment by operation, table, partition/range, engine/version, catalog, and writer class while hashing or redacting predicates.

Use deterministic schedule tests: pause writers after read, stage, validation, publish request, and lost response. Generate pairs and triples of append, overwrite, delete, merge, schema, compaction, rollback, and cleanup. Compare final states with a serial reference model. Inject stale reads, duplicated requests, CAS loss, timeout-after-success, process death, corrupt metadata, and branch divergence.

## Definitions and Notation

Let:

- $S_v$ be table state at committed version/snapshot $v$;
- $T=(id,b,R_T,W_T,V_T,A_T)$ be a logical transaction;
- $I(b,h)$ be commits intervening between base $b$ and head $h$;
- $F_v$ be live content files at version $v$;
- $A^+_T$ and $A^-_T$ be files added and removed by $T$;
- $p_T$ be a row or partition predicate influencing $T$;
- $f_T$ be the state-transition function for $T$;
- $k$ be attempt number and $K$ the configured attempt cap;
- $d_k=\min(d_{max},d_0 2^k)+J_k$ be capped backoff with jitter $J_k$;
- $C$ be semantic conflicts and $L$ CAS losses;
- $W$ be discarded work and $U$ reusable staged work.

A CAS loss means the expected head changed. A semantic conflict means $\neg V_T(b,h)$. Therefore $C\le L$ for attempts that reached CAS under a protocol that validates each refreshed head, though implementations may detect conflict before attempting CAS. Do not report CAS losses and conflicts interchangeably.

Conflict rate needs a denominator: conflicts per attempted commit, per logical transaction, or per operation cohort answer different questions. Retry amplification can be attempts/logical transactions. Work amplification should use compute time or bytes actually redone, not count metadata-only retries as full data recomputation.

## Mechanisms, Invariants, or Proof Structure

### No-lost-append argument

Let A and B add disjoint immutable sets $X$ and $Y$ to base $F$. A commits $F\cup X$. B loses CAS, refreshes, validates append compatibility, constructs $(F\cup X)\cup Y$, and conditionally publishes against A's head. The result contains both sets. Blindly republishing $F\cup Y$ would lose $X$.

### Rewrite safety argument

Transaction R replaces input set $Q\subseteq F_b$ with output $Z$. Its output represents exactly the logical content of $Q$. If head $h$ no longer contains every $q\in Q$, then removing $Q$ and adding $Z$ can reintroduce deleted content or duplicate rewritten content. The predicate $Q\subseteq F_h$ is therefore necessary, though additional checks may be required for new delete files, schema, or sequence semantics.

### Predicate-conflict argument

Delete D promises to remove rows matching $p$ from the commit-visible state. A concurrent append adds file $y$ that may contain $p$ rows. Even though $y\notin F_b$ and D never read its path, committing D without examining $y$ violates the promise. Validation must reject or include $y$ using an inclusive `may_match(y,p)` test.

### Idempotency argument

If every accepted commit records unique logical ID $id$ and publication rejects or recognizes a duplicate $id$, then repeated delivery of the same operation has at most one logical effect. Unique attempt filenames alone do not prove this: two attempts with different files can encode the same batch.

### Linearization audit

For each success, identify one atomic publication time and order commits accordingly. Replay their logical actions from the initial state and compare with every committed snapshot. Then check each transaction's promised read/isolation semantics. Publication order proves atomic state changes; it does not by itself prove serializable application behavior.

## Alternatives and Trade-Offs

**Pessimistic table locks** avoid late conflicts but serialize unrelated operations and require leases/fencing. **OCC** maximizes staging parallelism when conflicts are rare but may waste work under contention.

**Table-version validation** is simple and safe but aborts all head movement. **File-level validation** permits disjoint work but may miss predicate conflicts. **Row/key-range validation** is precise but needs indexes, stable identity, and more metadata.

**Late validation** avoids coordination during work but discovers conflicts after maximum cost. **Early detection** using markers, ownership, or intent records saves compute but adds shared state and can create false conflicts.

**Automatic rebase** improves availability for commuting actions. **Fail-fast** is safer for complex semantics and makes application intent explicit. Configure by operation, not one global retry switch.

**Client-side retry** is flexible but implementations can diverge. **Catalog/commit-service retry** centralizes policy and observability but increases service responsibility and may not understand operation semantics.

**Partition ownership** nearly eliminates writer conflict within a routing epoch but reduces flexibility and requires reassignment/fencing. **Central commit queueing** orders publication without preventing parallel file generation, at the cost of another availability and scaling component.

## Failure Modes and Misconceptions

1. **CAS equals OCC correctness.** CAS orders publications; validation supplies semantic safety.
2. **Every moved head conflicts.** Compatible appends may rebase safely.
3. **Every CAS loss is retryable.** Rewrites, predicates, evolution, or divergent history can invalidate prepared work.
4. **Disjoint old files mean disjoint operations.** Predicate operations can overlap new files or shared invariants.
5. **Partition equality proves row conflict.** It is often conservative and may create false conflicts.
6. **Different partitions never conflict.** Schema, protocol, uniqueness, or table-wide invariants can connect them.
7. **The write set is sufficient.** Reads that influenced output belong in validation.
8. **Rebase means changing the version.** It means reconstructing and validating the action on the new head.
9. **Retry gets a new ID.** That destroys duplicate recognition.
10. **Timeout means failure.** It may be success with a lost response.
11. **Missing from one read means not committed.** The status read may be stale or incomplete.
12. **Attempt filenames provide idempotency.** They prevent collision, not duplicate logical batches.
13. **All staged data is reusable.** Evolution or changed inputs can invalidate it.
14. **Infinite retries improve reliability.** They can create livelock, cost explosion, and starvation.
15. **No conflicts means correct validation.** Validation may be dangerously weak.
16. **Many conflicts mean broken storage.** The workload may genuinely contend or validation may be coarse.
17. **A lock needs no OCC.** Lease loss and stale holders require fencing/conditional publication.
18. **Snapshot isolation is serializability.** Write skew can preserve file disjointness while violating an application invariant.

## Worked Examples

### Example 1

A and B append distinct files from base 10. A publishes 11. B refreshes, confirms schema/spec compatibility, adds its file to 11, and publishes 12. Both survive; B reuses its data file and rewrites only metadata.

### Example 2

A compacts `{f1,f2}` into `g`. B deletes `f2` and commits first. A's condition `{f1,f2} subset of live(head)` fails. Adding `g` would resurrect rows from `f2`, so A must recompute or abort.

### Example 3

A deletes `country='SE'` from base files. B appends a new file whose country bound includes `SE`. No old file overlaps, but B's addition conflicts with A's commit-visible delete promise. Inclusive predicate validation catches it.

### Example 4

A prepares data using schema ID 7. B changes a required type/protocol and publishes schema ID 8. Even a pure append must check whether its files remain readable and conforming. Compatibility policy—not “append always retries”—decides.

### Example 5

A's CAS request times out after the catalog accepts it. On restart, A searches history for transaction ID `source-9:batch-44`, finds it in snapshot 81, and confirms success. Rewriting the batch with a new ID would duplicate it.

### Example 6

Ten writers collide and immediately retry. Their synchronized loops keep colliding. Capped exponential backoff with independent jitter spreads attempts, but persistent conflicts still justify partition ownership or a commit queue. Backoff treats symptoms; architecture addresses overlap.

### Example 7

Two transactions each observe that one of two doctors is on call, then independently turn a different doctor off. Their file writes are disjoint, yet the invariant “at least one on call” fails. A shared constraint key or serializable coordinator is required.

### Example 8

A metadata rewrite and an append start at snapshot 90. Append publishes 91. The rewrite validates its replacement covers the unchanged old manifests and retains the new append manifest, then publishes 92. Replacing the entire root computed at 90 would lose the append.

### Example 9

A lock holder's lease expires during a long write, and B acquires the lock. A later resumes. A fencing token in conditional publication rejects A's stale token; without fencing, pessimistic locking can still admit a stale writer.

### Example 10

The executable fixture classifies intervening changes for append, rewrite, and predicate delete.

<!-- bijux-verify: {"id":"optimistic-conflict-classification","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"append=safe_rebase\nrewrite=conflict_missing_input\npredicate_delete=conflict_matching_append\nlogical_transactions=3\n","stderr":""}} -->
```python
live_at_base = {"f1", "f2", "f3"}
live_at_head = {"f1", "f3", "new-se.parquet"}
rewrite_inputs = {"f1", "f2"}
new_file_bounds = {"new-se.parquet": {"country": ("SE", "SE")}}

append_result = "safe_rebase"
rewrite_result = (
    "safe_rebase" if rewrite_inputs <= live_at_head else "conflict_missing_input"
)
low, high = new_file_bounds["new-se.parquet"]["country"]
delete_result = (
    "conflict_matching_append" if low <= "SE" <= high else "safe_rebase"
)

print(f"append={append_result}")
print(f"rewrite={rewrite_result}")
print(f"predicate_delete={delete_result}")
print("logical_transactions=3")
```

## Cross-Program Connections

- **Database systems:** OCC, MVCC, serializability, predicate locking, write skew, and transaction logs provide the formal vocabulary.
- **Distributed systems:** CAS, consensus-backed metadata, idempotency, linearization, leases, fencing, retry, and unknown outcomes provide the failure model.
- **Data engineering:** appends, merges, CDC, compaction, clustering, schema evolution, and maintenance define distinct validation semantics.
- **Streaming systems:** source offsets, epochs, checkpoints, and transaction identities determine exactly-once effects.
- **Storage engineering:** immutable staging, conditional APIs, object identity, and cleanup determine whether retries can reuse work safely.
- **Platform engineering:** admission, queues, ownership, credentials, metrics, alerts, and runbooks manage hot tables and commit services.
- **Testing:** deterministic schedulers, model checking, property tests, fault injection, and history replay expose rare schedules.
- **Security and governance:** predicate redaction, audit trails, authorization changes, legal holds, and tenant boundaries affect validation and evidence.

## References

1. Apache Iceberg, [Reliability](https://iceberg.apache.org/docs/1.7.1/reliability/). Versioned. Documents concurrent writes, atomic metadata swap, retry reuse, and assumption validation.
2. Apache Iceberg, [Table Format Specification](https://iceberg.apache.org/spec/). Current. Defines commit conflict resolution, snapshots, sequence numbers, and requirements.
3. Apache Iceberg, [Concurrent Writes in iceberg-go](https://go.iceberg.apache.org/concurrent-writes.html). Current. Documents validators, retry, divergence, and commit outcomes.
4. Delta Lake, [Concurrency Control](https://docs.delta.io/concurrency-control/). Current. Documents OCC stages and conflict classes.
5. Delta Lake, [Transaction Log Protocol](https://github.com/delta-io/delta/blob/master/PROTOCOL.md). Current. Defines commits, transaction identifiers, protocol actions, and table state.
6. Delta Lake, [Delta Kernel](https://docs.delta.io/delta-kernel/). Current. Documents connector transactions and commit results.
7. Apache Hudi, [Concurrency Control](https://hudi.apache.org/docs/next/concurrency_control/). Current. Documents OCC, locks, nonblocking modes, and early detection.
8. Apache Hudi, [Timeline](https://hudi.apache.org/docs/next/timeline/). Current. Defines table actions and instant states.
9. Amazon DynamoDB, [Working with Items and Attributes](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/WorkingWithItems.html). Current. Documents conditional writes, condition failure, and retry behavior.
10. Amazon DynamoDB, [UpdateItem API](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_UpdateItem.html). Current. Defines conditional update expressions and results.
11. Google Cloud Storage, [Request Preconditions](https://cloud.google.com/storage/docs/request-preconditions). Current. Documents generation and metageneration preconditions for conditional object operations.
12. Azure Blob Storage, [Conditional Headers](https://learn.microsoft.com/en-us/rest/api/storageservices/specifying-conditional-headers-for-blob-service-operations). Current. Defines ETag and time-based conditional operations.
13. PostgreSQL, [Transaction Isolation](https://www.postgresql.org/docs/current/transaction-iso.html). Current. Explains isolation levels, serialization anomalies, and retry obligations.

## Exercises

### Exercise 1

Writers A and B append disjoint immutable files from the same base. State the validation and rebase steps that preserve both updates after A commits first.

### Exercise 2

A rewrite replaces `{p,q,r}`. At the new head, `{p,r}` remain live and `q` was deleted. Can the staged output be committed? Explain the anomaly it could create.

### Exercise 3

A delete promises to remove all rows with `day=2026-09-04`. An intervening file has day bounds `[2026-09-03, 2026-09-05]`. How should validation classify it, and why can bounds not prove that it definitely conflicts?

### Exercise 4

Design a retry record for an ingestion batch whose commit response may be lost. Identify the stable fields and recovery decision sequence.

### Exercise 5

A table observes 240 commit attempts for 200 logical transactions: 28 CAS losses, 10 semantic conflicts, and 6 full data recomputations. Compute attempt amplification and clearly scoped rates.

## Answers to the Exercises

### Answer 1

B refreshes to A's head, verifies table identity, branch, schema/spec/protocol compatibility, uniqueness or policy constraints, and any other append assumptions. It constructs a new candidate that references A's accepted state plus B's staged files, then CAS-publishes expecting A's exact head. If another writer wins, B repeats. It retains the same logical transaction ID and reuses files only while their semantics remain valid.

### Answer 2

No. The necessary input-live predicate `{p,q,r} subset of F_head` is false. The output was computed from `q`; adding it after `q` was deleted can resurrect its logical rows or double-apply a transformation. Abort or recompute from a new base, also accounting for delete and sequence semantics.

### Answer 3

The file must be treated as `may match`, so it conflicts with a delete that promises commit-visible coverage unless the operation incorporates it. Inclusive bounds admit false positives: the file's range spans the target day but may contain only the endpoints. Bounds can prove safe exclusion when disjoint; overlap does not prove actual matching rows.

### Answer 4

Persist source/batch identity, one logical transaction ID, base, operation and validation scope, staged object identities/checksums, proposed metadata/snapshot identity, publish request token, attempt history, and outcome state. On recovery, query authoritative table history/transaction records for the logical ID and proposed snapshot. If found, confirm success and advance source progress. If conclusively absent, refresh, revalidate, and retry with the same ID. If still ambiguous, remain unknown and do not republish or delete staged objects.

### Answer 5

Attempt amplification is $240/200=1.20$ attempts per logical transaction. CAS-loss rate per attempt is $28/240\approx11.67\%$. Semantic-conflict rate per attempt is $10/240\approx4.17\%$, or $10/200=5\%$ per logical transaction only if the ten conflicts belong to distinct transactions. Full-recomputation rate is $6/200=3\%$ per logical transaction under that scope. The counts do not state how many CAS losses later became conflicts, succeeded, or exhausted retries, nor the compute cost of each recomputation.
