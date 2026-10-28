---
module_id: LSDS-079
program: Large-Scale Data Systems Engineering
level: 2
module_number: 79
title: Catalog and Transaction Coordination
status: complete
last_verified: 2026-09-04
---

# Catalog and Transaction Coordination

## One-Page Review

### Governing question

How can a catalog resolve durable table identity, publish metadata changes with a real serialization point, coordinate changes across tables or branches, survive retries and failover, and expose precise guarantees without becoming a stale cache, unsafe lock service, or hidden source of split-brain state?

### Essential definitions

- A **catalog** maps durable object identities and names to current metadata plus governance and capability information.
- A **table identity** is a stable UUID or equivalent identity distinct from a mutable name and storage location.
- A **metadata pointer** identifies the current immutable table-metadata root.
- A **commit requirement** is a predicate that must hold at publication, such as expected UUID, reference head, schema ID, or property value.
- A **commit update** is a declared state transition applied only if every requirement succeeds.
- A **serialization point** is the atomic coordinator event that orders successful commits.
- A **multi-table transaction** makes requirements and updates for multiple tables visible atomically at one coordinator revision.
- A **branch-mediated transaction** stages commits on an isolated reference and atomically moves or merges a published reference.
- A **lease** is expiring permission; a **fencing token** is a monotonically ordered credential that lets protected resources reject stale holders.
- A **catalog cache** is a derived acceleration structure and never the authority for conditional publication.

### Central model, mechanism, or theorem

Let catalog state at revision $r$ be $C_r$, mapping object identity $i$ to name, UUID, reference heads, metadata pointer, lifecycle state, and policy. Transaction $T=(id,Q,U)$ contains stable request identity $id$, requirements $Q=\{q_1,\ldots,q_m\}$, and updates $U$. The coordinator may publish

$$C_{r+1}=U(C_r)\quad\text{iff}\quad\bigwedge_{q\in Q}q(C_r)=true.$$

Requirements and updates must be evaluated atomically at one serialization point. A client-side sequence of two valid single-table commits is not an atomic two-table transaction: observers can see the intermediate state and failure can leave half the intent published. Cross-table atomicity needs a shared coordinator primitive or an atomic branch/reference publication. Otherwise call the design a workflow and specify idempotency, intermediate visibility, compensation, and reconciliation.

### Critical invariants

- Names, UUIDs, storage locations, metadata pointers, and reference heads are distinct fields with explicit uniqueness and lifecycle rules.
- The authoritative catalog performs conditional publication; cached or object-listed state cannot authorize a commit.
- Every commit binds a stable transaction ID, actor, target identity, base revision/head, requirements, updates, and terminal or unknown outcome.
- All requirements are checked against the same catalog state that the updates atomically replace.
- A multi-table atomicity claim names one shared transaction domain and one serialization point.
- Rename, drop, undrop, replace, and register cannot silently substitute a different UUID beneath a stale name.
- Lease loss prevents future publication, and protected writers/resources reject stale fencing tokens.
- Cache invalidation preserves correctness even if freshness is delayed; commit paths refresh authoritative state.
- Unknown outcomes are resolved by request identity and authoritative history before retry or cleanup.
- Backups include catalog history/configuration and are restored consistently with reachable metadata and object storage.

### Common failures

Common failures include using object-store listing as the catalog; treating a table name as stable identity; updating a metadata pointer unconditionally; checking requirements before rather than within the atomic write; calling sequential table commits a transaction; using a lease without fencing; allowing caches to accept writes; retrying an unknown commit with a new ID; reusing a deleted name while stale clients still target its old UUID; implementing rename as visible create-plus-drop; vending credentials broader or longer-lived than the requested operation; declaring catalog failover healthy before quorum and storage dependencies agree; and restoring database rows without the metadata objects they reference.

### Compact example

Catalog revision 42 maps `orders` to pointer version 7 and `inventory` to version 11. A coordinated sale requires both expected versions and updates them to 8 and 12. The coordinator evaluates both predicates and installs both pointers at revision 43, or changes neither. If another writer first moves inventory to 12, the whole sale conflicts; publishing orders alone is forbidden. If the catalog only supports per-table CAS, the application must use a branch/reference transaction or explicitly operate a recoverable workflow rather than claim atomic visibility.

### Connections

[LSDS-050](050-reprocessing-a-stream-without-double-applying-effects.md) supplies request identity, [LSDS-071](071-table-snapshots-and-atomic-commit.md) supplies immutable roots, [LSDS-072](072-manifest-and-metadata-trees.md) supplies metadata graphs, [LSDS-073](073-optimistic-concurrency.md) supplies semantic validation, [LSDS-074](074-schema-evolution-at-scale.md) supplies stable IDs, and [LSDS-078](078-deletion-vectors-and-row-level-changes.md) supplies row-change coordination.

## Governing Question

An immutable metadata tree describes a table version, but readers and writers still need an authority that says which root is current. A catalog resolves an identifier, establishes object identity, publishes reference changes, controls namespace lifecycle, and often brokers credentials or policy. That small pointer-changing surface is the serialization boundary for enormous data systems.

Catalog is an overloaded word. A directory of metadata files, a metastore row, a REST service, a versioned branch store, and an in-process cache expose different atomicity and failure properties. A catalog protocol can make clients portable without making every backend's transaction domain identical. Engineers must identify the authoritative state transition beneath the interface.

The governing question is how to coordinate identity, requirements, updates, retries, locks, branches, caches, security, availability, and recovery so every successful publication has one explainable order and every broader guarantee states its exact boundary.

## Why This Matters

Every query begins with catalog resolution. Stale or inconsistent resolution can make two engines read different snapshots under the same table name. Every write ends with catalog publication. A weak conditional update can lose commits even when all data and metadata files are correct.

Cross-table pipelines create sharper expectations: publish facts and dimensions together, advance input and output checkpoints, swap a family of materialized views, or deploy compatible schema changes. If the platform exposes only single-table commits, orchestration cannot manufacture atomic visibility by sending requests quickly. It can provide retries, compensation, readiness markers, or branch publication, but those are different guarantees.

Catalogs are also security and availability chokepoints. They authenticate clients, authorize namespace/table actions, may vend scoped storage credentials, and reveal inventory. An outage can stop new queries or commits; a split brain can corrupt heads; a stale credential can bypass a lost lease. Operating this layer requires database-grade rigor and an explicit data-plane degradation policy.

## Prerequisites and Retrieval

Review replay identity in [LSDS-050](050-reprocessing-a-stream-without-double-applying-effects.md), snapshot commits in [LSDS-071](071-table-snapshots-and-atomic-commit.md), metadata trees in [LSDS-072](072-manifest-and-metadata-trees.md), OCC in [LSDS-073](073-optimistic-concurrency.md), schema identity in [LSDS-074](074-schema-evolution-at-scale.md), and row changes in [LSDS-078](078-deletion-vectors-and-row-level-changes.md).

You should understand namespaces, UUIDs, immutable objects, CAS, database transactions, serializability, snapshot isolation, consensus/quorum, revisions, branches, leases, fencing, idempotency, cache coherence, HTTP failure ambiguity, authentication, authorization, credential vending, audit logs, replication, backups, and disaster recovery.

For diagnosis retain catalog/warehouse identity, object UUID and name, base/current coordinator revision, reference name/head, old/new metadata locations, every requirement/update, request and trace IDs, actor/credential scope, conditional result, retry history, cache version/age, server leader/term, and referenced-object integrity.

## Learning Objectives

After this module, you should be able to:

1. Separate catalog authority, immutable metadata, object storage, and client cache roles.
2. Model names, UUIDs, locations, pointers, references, revisions, requirements, and updates.
3. Identify the exact serialization primitive behind a catalog commit.
4. Distinguish single-table CAS, multi-table atomicity, branch publication, and workflows.
5. Design safe create, register, rename, replace, drop, and undrop lifecycles.
6. Use leases only with validation and fencing where stale writers can damage state.
7. Resolve retryable conflicts and unknown outcomes with stable request identity.
8. Design safe cache, credential-vending, authorization, and audit behavior.
9. Operate catalog availability, migration, backup, restore, and reconciliation.
10. Test histories and failures against precisely labeled consistency guarantees.

## Core Exposition

### Authority and state split

The catalog owns current resolution; object storage owns immutable table metadata and data; engines own derived caches and staged artifacts. A common catalog record includes stable UUID, namespace/name, warehouse or explicit table location, current metadata root, reference heads, lifecycle state, properties, and policy bindings. Some services materialize more metadata server-side, but the authority boundary must remain explicit.

Object listing cannot safely infer the current root. Listings may be stale, contain abandoned attempts, retain historical roots, or expose attacker-planted names. A filename with the largest number is not an authority. Readers resolve through the catalog and then traverse checksummed metadata; recovery tools infer only under an explicit, audited repair procedure.

### Identity, naming, and lifecycle

Names are human-facing keys; UUIDs identify objects across rename. Locations identify bytes and may change through relocation. Reusing a dropped name too quickly can make a stale client act on a new table. Conditional operations therefore assert UUID as well as name/head when identity substitution matters.

Create reserves a unique name and UUID, chooses a noncolliding location, writes or asks the service to write initial metadata, and publishes once. Register attaches an existing valid metadata root without guessing ownership. Rename should be one atomic catalog operation in its transaction domain. Replace must declare whether identity, grants, lineage, location, and history survive. Drop changes catalog reachability; purge is a separate destructive storage lifecycle. Undrop needs retained authoritative identity and unexpired objects.

### Requirement-and-update commits

A change-based protocol sends requirements and updates rather than an entire stale record. Requirements may assert table UUID, reference snapshot, last-assigned field/spec/order ID, current schema, property, or object existence/nonexistence. Updates add a snapshot, set a reference, evolve schema/spec/order, set/remove properties, or change lifecycle state.

The server evaluates all requirements and updates inside one database/consensus transaction. On false requirement it changes nothing and returns a distinct conflict. On accepted request it assigns a coordinator revision and durable result. Validating on one connection and updating later on another is a time-of-check/time-of-use race.

### Single-table serialization

For one table, compare-and-set on the authoritative pointer or revision supplies a serialization point. A table-format library may first validate semantic assumptions, construct a candidate metadata root, then request conditional publication. If the head moved, it refreshes and applies the operation-specific rules from [LSDS-073](073-optimistic-concurrency.md).

The catalog must not turn a conditional request into last-writer-wins. It also must not acknowledge before the new state is durable enough for the advertised failure model. The metadata object should exist and pass integrity checks before its pointer becomes readable. If the catalog writes metadata on behalf of clients, ownership of naming, encryption, and cleanup moves server-side.

### Multi-table coordination

An atomic multi-table transaction evaluates every table's requirements and installs every update in one coordinator transaction. All targets must share the transaction domain. A REST endpoint accepting a list does not itself prove backend atomicity; the implementation's durable commit boundary does.

If tables live in separate catalogs, regions, or databases, use distributed transaction machinery with stated blocking/failure assumptions, redesign ownership, or expose a workflow. A workflow may write tables independently and publish a completion marker, maintain an intent/outbox, compensate earlier steps, or continuously reconcile. Readers must know whether to ignore incomplete epochs. These techniques provide useful convergence, not instantaneous all-or-nothing visibility.

### Versioned catalogs and branches

A versioned catalog can pin reads to one commit hash across many content keys. Writers stage a sequence on an isolated branch; an atomic merge, transplant, or reference reassignment exposes it. This can make a prepared cross-table state visible through one reference movement, provided all readers resolve that reference consistently and the service checks merge requirements.

Branch publication is not equivalent to rewriting each external table pointer after the fact. Specify conflict rules, ancestry, content-key uniqueness, merge behavior, and whether storage objects are durable before reference movement. Long-lived branches also affect retention and garbage collection.

### Locks, leases, and fencing

Some backends need mutual exclusion because their pointer store lacks adequate conditional semantics or mixed client generations use incompatible paths. A lock narrows concurrent access but does not validate table semantics. A lease can expire during a pause; the old holder may resume believing it still owns the lock.

Issue monotonically increasing fencing token $z$ on acquisition. Every protected catalog/storage mutation records and rejects tokens lower than the greatest accepted token. Heartbeats extend liveness, not safety. If the protected resource cannot enforce fencing, a lease alone cannot prevent a stale writer. Prefer short critical sections: stage immutable files outside the lock, then refresh, validate, and publish inside it.

### Retry and unknown outcomes

Give each logical commit a stable idempotency key scoped to actor and operation. Reuse it only for the same canonical request. The catalog durably maps it to request digest, status, and result for a documented window. Same key plus different payload is an error.

Classify condition failure, authorization denial, validation error, definitely-unattempted transport failure, throttling, and unknown outcome separately. After timeout at publication, query authoritative head/history or an operation-status endpoint by request ID. A stale cache miss is not proof of failure. Do not create a new ID or delete staged metadata until outcome is resolved.

### Caches and discovery

Catalog caches reduce resolution latency and service load. Cache entries bind catalog identity, object UUID, name, reference, metadata pointer/revision, policy epoch, and expiry. Negative caches need shorter, deliberate lifetimes because create/undrop can invalidate them. Rename invalidates old and new name keys.

Stale cached pointers may be acceptable for explicitly stale reads or pinned historical queries. They are not acceptable as the expected current value for an unrefreshed commit. Use revision-bearing responses, conditional revalidation, watch/invalidation where available, bounded TTL, jittered refresh, request coalescing, and load shedding. Prevent a catalog outage from becoming a synchronized refresh storm.

### Security and credential vending

Authorize catalog actions and storage access separately but coherently. Resolve identity before evaluating table policy; protect against name/UUID substitution. Credential vending or remote signing should bind principal, table UUID, operation, exact path/prefix, permissions, region, encryption context, and short expiry. A table rename should not broaden old credentials.

Audit authentication identity, impersonation/delegation chain, authorization decision/policy version, catalog/table/reference, requirements/updates, request ID, result, and credential scope without logging secrets or sensitive property values. Listings and error differences can leak object existence; namespace isolation and rate limits matter.

### Availability, migration, and recovery

Define behavior when catalog is unavailable. A pinned reader may continue from a validated immutable root for a bounded policy window; discovery, authorization refresh, and new commits usually stop. Never promote a writable fallback that lacks the authoritative revision history. Leader failover must preserve quorum/term rules and reject stale leaders.

Catalog migrations require dual-read comparison before cutover, one writer authority, frozen or replicated revisions, UUID/name/location preservation, credential-policy migration, and rollback criteria. Dual write without a coordinator can diverge. Backup includes database/consensus state, encryption/key configuration, policy, idempotency ledger, audit chain, and the metadata objects referenced at the recovery point. Restore verifies every pointer and tests new conditional commits before reopening writes.

### Observability and verification

Measure resolution latency/hit ratio/staleness, commit requirements and updates, conditional conflicts, server transaction latency, revisions, idempotent replays, unknown outcomes, lock waits/lease loss/fencing rejection, branch divergence/merge conflicts, credential issuance, authorization denials, leader changes, replication lag, cache storms, broken pointers, and recovery-point gaps. Segment by catalog, tenant, namespace, operation, engine/version, region, and outcome without exposing names unnecessarily.

Model-check small histories of creates, commits, rename, replace, drop, branch merge, cache reads, lease expiry, failover, and timeout. Record invocation/response intervals and verify successful writes admit the promised serial order. Inject response loss after durable commit, stale caches, duplicated IDs, leader pause, clock skew, partial migration, missing metadata, and storage denial.

## Definitions and Notation

Let:

- $C_r$ be authoritative catalog state at coordinator revision $r$;
- $i$ be stable object identity and $n$ a mutable namespace/name;
- $uuid(i)$ be table UUID and $loc(i)$ its storage location;
- $ptr_r(i)$ be current metadata pointer for object $i$ at revision $r$;
- $head_r(i,b)$ be reference $b$'s head for table/content key $i$;
- $T=(id,Q,U)$ be logical request identity, requirement set, and update set;
- $q_j(C_r)$ be requirement $j$ evaluated on one authoritative state;
- $D$ be one coordinator transaction domain;
- $z$ be a monotonically increasing fencing token;
- $a$ be cache age and $\delta$ allowed staleness for an explicitly stale read;
- $L_c$, $L_s$, and $L_e$ be catalog, storage, and end-to-end latencies;
- $RPO$ and $RTO$ be recovery-point and recovery-time objectives.

A successful catalog transaction satisfies $\bigwedge_j q_j(C_r)$ and makes $U(C_r)$ visible at one revision. For objects $i_1,i_2$ in distinct transaction domains $D_1\ne D_2$, ordinary local transactions do not imply an atomic joint revision. Cache hit rate is meaningless without cache age and correctness policy. Availability metrics need a denominator and operation class: cached reads, fresh resolution, and commits have different dependencies.

## Mechanisms, Invariants, or Proof Structure

### Conditional-publication proof

Assume the coordinator serially evaluates requirements and updates. Transaction T observes expected pointer $p$ and requires $ptr(i)=p$. Exactly one contender can replace $p$ first. Later contenders evaluate against the new state and fail or rebuild, so no accepted update silently overwrites an intervening pointer. This proves pointer serialization, not semantic validity of under-specified requirements.

### Multi-table atomicity proof

For tables A and B in domain D, transaction T checks $Q_A\land Q_B$ and installs $U_A,U_B$ in one durable coordinator commit. No catalog revision contains only one update, so readers pinned to a revision see before or after. If either requirement fails, neither update occurs. Sequential per-table CAS lacks this indivisible state transition and fails the proof.

### Fencing proof

New lock holder receives $z_2>z_1$. Every protected mutation is accepted only when token is at least the greatest accepted value. After a $z_2$ mutation, paused holder $z_1$ is rejected even if it never observed lease loss. Without resource-side comparison, token issuance alone has no protective effect.

### Branch-publication proof

Readers resolve published reference P to commit h. Work is staged under isolated reference W and validated against P. One conditional reference update changes P from h to h'. Readers resolving before see h; readers resolving after see h'. The proof requires one atomic reference movement, consistent resolution, durable referenced objects, and conflict validation.

### Adversarial verification

Test create/create name collision, stale UUID, missing/corrupt metadata, rename races, drop/recreate, replace identity, sequential half-commit, multi-table requirement failure, branch divergence, lease expiry during pause, stale fencing token, duplicate/different-payload idempotency key, timeout-after-commit, stale positive/negative caches, leader failover, migration split brain, and restore with absent objects. Require exact success/conflict/unknown classification and no silent pointer loss.

## Alternatives and Trade-Offs

**Metastore/database catalogs** reuse mature transactions and indexing but couple scale and availability to that service. **REST catalogs** give language portability, server-side policy, and credential vending but add network/protocol operations. **Filesystem catalogs** are simple where rename/locking is strong but are dangerous on stores without the assumed atomic primitives. **Versioned catalogs** provide cross-key history and branches but add merge, retention, and operational semantics.

**Single-table CAS** is compact and scalable but cannot promise atomic cross-table visibility. **Coordinator multi-table transactions** provide it within one domain at the cost of larger contention/failure scope. **Branch publication** isolates preparation and enables one exposure point but requires reference-aware readers. **Workflows** span arbitrary systems but expose intermediate states or depend on markers/compensation.

**Optimistic requirements** favor low contention and short coordinator work. **Locks** can reduce repeated conflicts but add queues, leases, fencing, and deadlock/liveness concerns. **Pessimistic ownership** suits structurally hot objects if partitioning is stable.

**Client-written metadata** reduces service data-plane work but complicates credentials and cleanup. **Server-written metadata** centralizes canonicalization and policy but increases service bandwidth, storage permissions, and availability burden.

**Long cache TTLs** reduce catalog load and improve availability for stale reads but delay discovery and policy changes. **Short TTLs/watches** improve freshness but amplify service dependencies and invalidation complexity.

## Failure Modes and Misconceptions

1. **Catalog is only discovery.** Its pointer update is often the write serialization point.
2. **Largest metadata filename is current.** Attempts and history invalidate that inference.
3. **Name is identity.** Rename, drop/recreate, and replace make it unsafe.
4. **Storage location is identity.** Relocation and multiple registrations separate them.
5. **CAS proves transaction correctness.** Requirements may omit semantic dependencies.
6. **Check then write is conditional.** Without one atomic boundary it races.
7. **Two successful commits are an atomic pair.** Intermediate visibility disproves it.
8. **One REST request means one transaction.** Backend durability defines atomicity.
9. **A completion marker rewinds readers.** It coordinates aware readers only.
10. **A lease prevents stale work.** Pause and expiry require fencing.
11. **A fencing number protects by itself.** The resource must compare it.
12. **Cache TTL guarantees freshness.** Age, invalidation, and clocks matter.
13. **Cached head can authorize commit.** Refresh authoritative conditions first.
14. **Retry means new request.** New identity can duplicate a successful unknown commit.
15. **Rename is copy then drop.** That exposes aliasing, absence, or split ownership.
16. **Drop means bytes erased.** Purge and retained-reference cleanup are separate.
17. **Dual write makes migration safe.** Independent writes can diverge.
18. **Database backup is sufficient.** Referenced metadata, keys, and policy must align.

## Worked Examples

### Example 1

Table name `sales.orders` resolves to UUID `u1` and pointer `p7`. A stale client expects `u0,p6`; asserting only name could mutate the wrong reincarnated table. Requirements on UUID and pointer reject it.

### Example 2

Writer A and B expect pointer `p7`. A publishes `p8`. B's conditional update fails, refreshes, validates its append, builds `p9` containing both actions, and retries against `p8`.

### Example 3

A workflow commits `orders` and then crashes before `inventory`. Readers observe half the sale. An idempotent reconciler can finish or compensate, but the interval proves the workflow was not atomic.

### Example 4

A coordinator transaction requires orders revision 7 and inventory revision 11. Inventory is already 12, so it applies neither update. The system reports a conflict, not partial success.

### Example 5

Three tables are staged on branch `run-42`. After validation, published reference `prod` moves atomically to the staged commit. Reference-aware readers see all three changes together.

### Example 6

Holder A pauses after lease expiry. Holder B acquires fencing token 18 and publishes. A resumes with token 17; the catalog rejects it even though A's local process still thinks it holds a lock.

### Example 7

A commit response times out after durable revision 91. Retrying request ID `r5` returns the recorded revision 91. Sending identical content as new ID `r6` could duplicate the logical action.

### Example 8

A negative cache says table `x` is absent for five minutes. Another client creates it. Create requests must check authority rather than trust the negative cache; reads either revalidate or expose their bounded-staleness contract.

### Example 9

During migration, old catalog remains sole writer while new catalog shadows reads and compares UUID, pointer, references, and policies. Cutover fences old writes before enabling new writes; simultaneous independent writers are never allowed.

### Example 10

The executable fixture models atomic requirements and updates for two table pointers.

<!-- bijux-verify: {"id":"catalog-transaction","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"first=committed\norders=8 inventory=12 revision=43\nsecond=conflict\nunchanged=yes\n","stderr":""}} -->
```python
catalog = {"orders": 7, "inventory": 11, "revision": 42}


def commit(expected, updates):
    before = dict(catalog)
    if any(catalog[name] != version for name, version in expected.items()):
        return "conflict", catalog == before
    for name, version in updates.items():
        catalog[name] = version
    catalog["revision"] += 1
    return "committed", catalog == before


result, _ = commit({"orders": 7, "inventory": 11}, {"orders": 8, "inventory": 12})
print(f"first={result}")
print(f"orders={catalog['orders']} inventory={catalog['inventory']} revision={catalog['revision']}")

result, unchanged = commit({"orders": 8, "inventory": 11}, {"orders": 9, "inventory": 12})
print(f"second={result}")
print(f"unchanged={'yes' if unchanged else 'no'}")
```

## Cross-Program Connections

- **Distributed systems:** consensus, linearizability, CAS, leases, fencing, idempotency, and failure detectors define publication safety.
- **Database systems:** catalog rows, serializable transactions, MVCC, unique constraints, and write-ahead logs implement authority.
- **API engineering:** conditional requests, canonical payloads, idempotency keys, status resources, pagination, and version negotiation shape the protocol.
- **Platform engineering:** tenant isolation, fleet capability, SLOs, rate limits, migrations, backups, and incident response operate the service.
- **Security engineering:** identity, policy evaluation, delegated credentials, signing, audit, and namespace privacy protect metadata and bytes.
- **Programming languages:** typed requirement/update unions and exhaustive error handling prevent ambiguous client behavior.
- **Formal methods:** histories, linearization points, invariants, state machines, and model checking test guarantees.
- **Data governance:** naming, ownership, lineage, retention, deletion, and policy versions depend on stable catalog identity.

## References

1. Apache Iceberg, [REST Catalog Specification](https://iceberg.apache.org/rest-catalog-spec/). Current. Defines the portable catalog protocol and change-based commits.
2. Apache Iceberg, [REST Catalog OpenAPI](https://github.com/apache/iceberg/blob/main/open-api/rest-catalog-open-api.yaml). Current. Defines commit requirements, updates, transactions, errors, capabilities, and idempotency fields.
3. Apache Iceberg, [Reliability](https://iceberg.apache.org/docs/latest/reliability/). Current. Documents atomic commits, optimistic concurrency, retries, and catalog responsibilities.
4. Apache Iceberg, [Table Format Specification](https://iceberg.apache.org/spec/). Current. Defines table identity, metadata roots, snapshots, references, and commit requirements.
5. Apache Iceberg, [Catalog Properties](https://iceberg.apache.org/docs/latest/catalog-properties/). Current. Documents catalog caching, authentication, locking, and backend configuration.
6. Apache Iceberg, [Transaction API](https://iceberg.apache.org/javadoc/latest/org/apache/iceberg/Transaction.html). Current. Defines grouping multiple table updates into one atomic table commit.
7. Project Nessie, [Transactions](https://projectnessie.org/guides/transactions/). Current. Describes cross-table transactions, branches, reference assignment, and isolation choices.
8. etcd, [API: Transactions](https://etcd.io/docs/v3.6/learning/api/). Version 3.6. Defines atomic comparison-guarded multi-key updates and revisions.
9. AWS, [DynamoDB Condition Expressions](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Expressions.ConditionExpressions.html). Current. Documents conditional mutation predicates.
10. AWS Glue, [REST APIs for Apache Iceberg](https://docs.aws.amazon.com/glue/latest/dg/iceberg-rest-apis.html). Current. Documents REST catalog authentication, endpoints, and authorization integration.
11. Apache ZooKeeper, [Recipes and Solutions](https://zookeeper.apache.org/doc/current/recipes.html). Current. Documents lock recipes and sequencing patterns.
12. Apache Hive, [Locking](https://cwiki.apache.org/confluence/display/Hive/Locking). Current. Documents metastore-backed locking behavior and compatibility concerns.
13. PostgreSQL, [Transaction Isolation](https://www.postgresql.org/docs/current/transaction-iso.html). Current. Defines isolation phenomena, serializable execution, and retry obligations.

## Exercises

### Exercise 1

Catalog revision 90 has table A at pointer 4 and B at pointer 8. Transaction T expects those values and proposes 5 and 9. Another writer first moves B to 9. State the atomic result and why sequential publication would differ.

### Exercise 2

Design requirements for renaming `finance.daily` to `finance.ledger` without allowing a stale client to rename a reincarnated table or overwrite an existing destination.

### Exercise 3

A worker holds a 30-second lease, pauses for 45 seconds, and resumes after a new worker publishes with token 61. Explain what the old worker with token 60 may safely do.

### Exercise 4

Design a non-atomic cross-catalog workflow that advances an input checkpoint and publishes an output table. Label intermediate visibility, retry, compensation, and reconciliation explicitly.

### Exercise 5

Specify a catalog disaster-recovery exercise, including consistency between catalog state, immutable metadata, security configuration, and post-restore conditional writes.

## Answers to the Exercises

### Answer 1

T's joint requirement is false because B is 9 rather than 8, so a genuine atomic coordinator changes neither table; A stays 4 and B stays 9. Sequential publication could advance A to 5 before discovering B's conflict, leaving a visible half-state. Repairing that later does not make the earlier interval atomic.

### Answer 2

Require source name exists, source UUID equals the caller's observed UUID, source lifecycle state is active, source catalog revision or version is expected, destination name is absent, and both names belong to the intended namespace/transaction domain. In one transaction remove the old name mapping and install the new mapping to the same UUID, pointer, location, references, and policy bindings; emit one durable revision and invalidate both cache keys.

### Answer 3

It must not publish or mutate protected state. Lease expiry ended its authority, and token 60 is stale after 61 was accepted. It may discard purely local computation or refresh authoritative state and start a new acquisition/replan under a new token. Resource-side fencing must reject any delayed token-60 request; checking only the worker's local lease flag is insufficient.

### Answer 4

Create a stable workflow ID and intent record containing input base/checkpoint, output base, deterministic staged objects, desired updates, and status. Commit the output idempotently, then conditionally advance the checkpoint, recording each result. Readers either accept documented intermediate output or filter by a completion epoch. On failure, retry the same IDs; if intent is cancelled, compensate only through a new conditional transaction. A reconciler compares intent, output history, and checkpoint and completes or flags divergence. State plainly that independent catalogs provide convergence, not atomic visibility.

### Answer 5

Choose recovery revision/time and stop or fence writers. Restore catalog database/consensus state, policy and identity configuration, encryption/key access, idempotency ledger, and audit anchors. Inventory every restored pointer/reference and verify the corresponding immutable metadata object, checksum, data/delete reachability, warehouse identity, and credential boundary. Compare revisions and references with backup evidence, run read-only queries, then issue a canary conditional commit and forced stale-CAS conflict. Measure achieved RPO/RTO, keep the former authority fenced, and reopen writes only after reconciliation has no unexplained missing or extra reachable objects.
