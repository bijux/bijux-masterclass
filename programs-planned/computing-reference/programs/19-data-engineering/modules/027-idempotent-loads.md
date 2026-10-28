---
module_id: DE-027
program: Data Engineering
level: 1
module_number: 27
title: Idempotent Loads
status: complete
last_verified: 2026-09-02
---

# Idempotent Loads

## One-Page Review

### Governing question

How can a data load be retried, replayed, overlapped, or resumed after an ambiguous failure while producing the same governed target effect as one successful application of each intended input unit?

### Essential definitions

- **Idempotence** means that applying the same logical operation more than once has the same intended effect as applying it once: $L(L(S,u),u)=L(S,u)$.
- A **load unit** is the smallest independently retryable input with a stable identity, such as a file manifest, source partition and range, CDC transaction, micro-batch, or snapshot generation.
- An **idempotency key** names one logical load operation across physical attempts; its scope and payload fingerprint are part of the contract.
- An **effect identity** names the target mutation that must occur at most once, and is not necessarily the entity's business key.
- A **receipt** is durable target evidence that a specific load unit and payload fingerprint reached a declared terminal outcome.
- An **ambiguous commit** occurs when the client cannot tell whether a submitted transaction committed, often because acknowledgement was lost after the commit decision.
- A **conditional mutation** changes a target only if an identity, version, compare-and-set, or uniqueness predicate permits it.
- An **immutable generation** is a complete new dataset version written away from the trusted pointer and published with one atomic metadata change.
- A **replay window** is the period for which inputs, identities, schemas, code, and target history remain sufficient to reproduce or safely recognize prior effects.
- **convergence** means that permitted retries and reorderings lead to one intended state under explicitly stated preconditions; it is stronger than merely suppressing duplicate requests.

### Central model, mechanism, or theorem

Let $S$ be target state, $u=(k,h,p)$ a load unit with stable key $k$, canonical payload digest $h$, and effects $p$, and $L$ the load transition. Safe idempotence requires

$$
L(L(S,u),u)=L(S,u).
$$

A common implementation performs, in one serializable or otherwise sufficient target transaction:

1. claim or read receipt $(k,h)$;
2. reject the operation if $k$ exists with another digest;
3. apply deterministic conditional row/file effects;
4. record the successful receipt and output evidence; and
5. commit effects and receipt together.

If the transaction aborts, neither is trusted. If acknowledgement is lost after commit, retry observes the matching receipt and returns the recorded result. Atomicity closes the dangerous states “effect without receipt” and “receipt without effect.”

### Critical invariants

- The retry unit, identity namespace, source scope, payload canonicalization, transformation version, target, and terminal outcome are explicit.
- One idempotency key never silently denotes two different payloads; equal key plus unequal digest fails closed.
- Effects and their success receipt commit atomically, or an independently replayable authoritative layer and its checkpoint do.
- Source duplicates are resolved to deterministic target candidates before any one-target-row merge; target uniqueness is enforced physically where required.
- Mutable rows accept only the intended source version; a late older replay cannot regress state or resurrect a delete.
- Snapshot or partition replacement becomes visible only after the entire immutable generation validates.
- Attempts, retries, receipts, affected rows, rejects, target snapshot/commit, and code/schema versions remain auditable.
- Retry does not repeat ungoverned external effects such as notifications, exports, or irreversible API calls.
- Concurrency control covers simultaneous first attempts, not only sequential replay.
- Recovery retains input and identity evidence long enough to decide whether to replay, resume, reconcile, or rebuild.

### Common failures

Equating `MERGE` with idempotence; using a run timestamp or random UUID as the retry key; deduplicating by entity key and erasing legitimate versions; accepting one key with a changed payload; recording a receipt before mutations; committing data before a non-atomic checkpoint; appending on every retry; incrementing totals with a replayable statement; omitting deletes; allowing multiple source rows to match one target row; comparing nullable keys with ordinary equality; overwriting newer rows with older events; truncating the trusted table before replacement succeeds; treating a lost acknowledgement as a failed commit; sending email inside the database retry loop; trusting reported affected-row counts as reconciliation; or expiring receipts while source retries remain possible.

### Compact example

Batch `orders/eu/42` contains three entity versions and digest `d7`. Its first transaction writes two current rows, one tombstone, three effect identities, and a batch receipt, but the client loses the acknowledgement. A retry presents the same key and digest, reads the committed receipt, and changes nothing. A request reusing `orders/eu/42` with digest `e9` is rejected. A delayed version 6 for an entity already at version 8 is recorded as stale rather than regressing the row. The final state and audit evidence equal one successful application.

### Connections

[DE-022](022-watermarks-and-high-water-marks.md) constrains progress, [DE-023](023-file-arrival-and-manifest-processing.md) defines input publication, and [DE-026](026-database-change-data-capture.md) supplies replay-prone change identities and versions. The next module develops deduplication and record identity, while later modules cover merge semantics, orchestration retries, exactly-once effects, and replayable raw ingestion.

## Governing Question

What durable evidence lets an operator retry a load after timeout, worker death, process restart, overlap, or lost acknowledgement without guessing whether the previous attempt changed the target?

Retries are inevitable. Networks can fail after a server commits but before the client receives success. Workers can die after writing data but before advancing an orchestrator marker. A scheduled partition can overlap a manual backfill. A broker can redeliver a micro-batch. Operators can rerun a file after correcting infrastructure while the original attempt's terminal state remains unclear.

The unsafe response is to infer outcome from the client error. A timeout says that the caller stopped waiting; it does not say whether the target committed. Blind retry can duplicate additive effects. Blind skip can omit an uncommitted load. Manual inspection based on current row counts may not distinguish one correct application from two compensating errors.

An idempotent load makes replay an ordinary protocol. It defines one logical unit, preserves stable identity across attempts, makes the target effect deterministic, records the relationship between identity and payload, and couples effect to durable completion evidence. The design must cover concurrent first attempts, partial batches, late versions, deletes, schema changes, non-transactional stores, and effects beyond the primary table.

The word “idempotent” is sometimes applied too broadly. A command can be idempotent for current target rows but still duplicate audit events, billable exports, notifications, sequence allocation, or downstream messages. It can converge after sequential retries but race under concurrency. It can suppress a correction because its key is too coarse. The governing claim must therefore name the observable boundary and intended effect.

## Why This Matters

Without idempotence, reliability mechanisms create corruption. A retry policy converts transient failures into duplicate inserts, doubled balances, inflated counters, repeated snapshots, or repeated activation. Disabling retries avoids some duplicates but turns recoverable failures into missing data and sustained operational intervention.

Ambiguous commits are the central case. Consider a target transaction that commits and an acknowledgement packet that disappears. From the caller's perspective, this case is observationally similar to a transaction that never reached the server. Only target-side identity and receipt evidence can distinguish them safely. A process-local “already ran” set disappears precisely when recovery needs it.

Batch size does not remove the issue. A million-row file can fail after 700,000 autocommitted statements. Replaying all rows may double append-only facts; resuming at an approximate line can omit or repeat boundaries. A transactional bulk statement avoids partial visibility only if its input-to-target matching is deterministic and the receipt/checkpoint shares its commit.

Idempotence also enables planned operations. Historical backfills can overlap current ingestion if generations or source versions prevent regression. Deployments can retry after lock conflicts. Orchestrators can recover lost state by querying target receipts. Disaster recovery can reconstruct materializations from immutable raw units rather than preserve every transient worker state.

The property improves evidence, not only convenience. A receipt ledger connects input identity and digest to target commit, code version, schema version, counts, controls, and output snapshot. Reconciliation can then ask whether every expected unit has exactly one accepted meaning and whether every trusted effect belongs to an accepted unit.

Idempotence has costs. Receipts and event identities need retention, indexes, and lifecycle rules. Conditional writes can contend. Immutable replacement needs temporary capacity. Version checks can expose upstream order defects rather than hide them. These costs are usually less than the unbounded ambiguity of non-repeatable mutation, but they must be engineered rather than assumed.

## Prerequisites and Retrieval

Retrieve the producer and consumer contract; target owner; input unit and scope; source system/epoch; file manifest, object version, partition, offset range, CDC position, transaction, or batch identity; retry and redelivery behavior; maximum overlap; payload canonicalization; content digest; schema and transformation versions; row/event/business keys; source versions and ordering domain; insert/update/delete semantics; snapshot versus delta meaning; authoritative grain; target constraints and indexes; transaction boundaries; isolation level; atomic conditional-write support; merge/upsert syntax and product/version semantics; commit acknowledgements; statement and transaction retry behavior; affected-row semantics; staging tables; immutable generation/pointer facility; checkpoint/receipt store; external side effects; downstream publication; late and out-of-order policy; correction/retraction policy; null and key-change behavior; target partitions; concurrency; locks and deadlocks; timeout policy; input and receipt retention; rebuild path; reconciliation controls; observability; security classification; credentials; tenant boundaries; disaster recovery; and runbooks.

Distinguish logical retry from a new correction; attempt ID from stable idempotency key; event occurrence ID from entity/business key; input payload digest from target row digest; source version from ingestion time; duplicate delivery from duplicate source fact; replay from backfill; stale version from identical version; append-only event from current-state projection; “not matched” from an absent row under a sufficient isolation contract; statement atomicity from batch atomicity; target data commit from orchestrator success; client timeout from server rollback; upsert syntax from semantic determinism; affected-row count from exact effect set; uniqueness constraint from check-then-insert code; dataset generation from mutable table name; staging completion from trusted publication; process memory from durable receipt; and current-state equality from complete history.

Create a load contract before implementation:

| Concern | Required decision and evidence |
|---|---|
| Unit | Stable retry boundary, source scope, expected members, terminal states |
| Identity | Namespace, key derivation, collision policy, lifetime, tenant/environment scope |
| Payload | Canonical bytes/records, digest algorithm/version, schema and code identity |
| Effect | Append, replace, insert-if-absent, current-state merge, additive delta, or retraction |
| Order | Source version domain, tie/conflict policy, late-arrival behavior |
| Atomicity | Statements, target transaction, receipt coupling, publication pointer |
| Concurrency | Isolation, uniqueness/compare-and-set, retryable conflicts, ownership/lease role |
| Evidence | Receipt, row effects, counts, controls, target commit/snapshot, rejects |
| Recovery | Retry, resume, reconcile, rebootstrap, input/receipt retention horizons |
| Side effects | Outbox, downstream transaction, compensating or independently idempotent protocol |

Before choosing `MERGE`, reproduce the target engine's documented behavior for duplicate source matches, duplicate target rows, null keys, clause ordering, nondeterministic matches, concurrent writers, constraint violations, affected-row counts, transaction retries, and failed statements. Similar SQL syntax does not imply identical semantics.

## Learning Objectives

After completing this module, you should be able to:

1. define idempotence for a named load unit and observable target boundary;
2. distinguish stable idempotency keys, event identities, entity keys, versions, attempts, and receipts;
3. explain why timeouts and lost acknowledgements require target-side evidence;
4. design an atomic effect-plus-receipt transaction and handle concurrent first attempts;
5. select insert-if-absent, versioned upsert, ledger, immutable replacement, or commutative aggregation deliberately;
6. make source-to-target merge cardinality deterministic before target mutation;
7. prevent late replay from regressing rows, resurrecting deletes, or repeating additive effects;
8. extend idempotence across files, checkpoints, messages, and external side effects without overstating guarantees;
9. test crash points, duplicates, payload conflicts, partial batches, concurrency, schema changes, and receipt expiry; and
10. assemble operational and reconciliation evidence that supports a bounded idempotence claim.

## Core Exposition

### Define the effect boundary

Idempotence belongs to an operation under an equivalence relation, not to a tool name. For target state $S$ and logical load unit $u$, a load transition $L$ is idempotent when

$$
L(L(S,u),u)=L(S,u).
$$

The equality must say what observers can see. If the current table is identical but an audit row, notification, storage object, bill, or downstream event appears twice, the broader workflow is not idempotent. Conversely, separate attempt logs may legitimately record every retry while the requested business/data effect remains one; RFC 9110's definition of idempotent methods similarly distinguishes the intended request effect from incidental logging.

State the boundary in a sentence: “For one canonical manifest digest in tenant and target namespace, any number of accepted retries produces one published dataset generation and one set of materialized entity versions; attempts remain individually auditable.” This is testable. “The pipeline is exactly once” is not.

Idempotence does not mean that repeating arbitrary different inputs has no effect. A correction is a new logical unit. Nor does it mean commutativity: operations $u$ and $v$ can each be idempotent while order matters, so $L(L(S,u),v)$ may differ from $L(L(S,v),u)$.

### Choose the retry unit

The unit should match the boundary that can be identified, retained, validated, and committed. Common units include:

- an immutable file generation named by source, object version, and manifest digest;
- a source partition with half-open version range $(a,b]$;
- a CDC transaction or event occurrence;
- an orchestrator asset partition and declared code/schema version;
- a streaming query epoch or micro-batch under one checkpoint lineage; or
- a complete snapshot generation published through a metadata pointer.

Too large a unit increases retry work and transaction contention. Too small a unit multiplies receipt overhead and can lose required atomicity. A transfer transaction that changes two accounts cannot safely be split into independently published row units if consumers require the invariant to hold at all visible points.

Do not derive retry identity from an execution timestamp, random identifier generated on every attempt, worker hostname, or scheduler try number. Those identify physical attempts. The same logical input must recover the same key after every restart, including in another environment chosen for disaster recovery.

### Separate key, payload, event, and entity identity

Let a logical unit be

$$
u=(n,k,h,c,p),
$$

where $n$ is an identity namespace, $k$ the idempotency key, $h$ a canonical payload digest, $c$ the interpretation contract, and $p$ the proposed effects. The namespace includes target dataset, tenant/security domain, producer/source epoch, and perhaps transformation contract. It prevents `partition=2026-09-02` in two unrelated datasets from colliding.

The receipt key can be $(n,k)$. Once claimed successfully, it binds to digest $h$ and contract $c$. A retry with the same tuple returns prior outcome. The same key with a different digest or incompatible contract is not a retry; it is an identity conflict and must fail closed or enter explicit adjudication.

An entity key identifies the subject whose current state is projected. An event identity identifies one occurrence affecting it. Deduplicating all records by entity key would erase legitimate versions. Conversely, using only event identity does not decide which of two different events is newer. Store the dimensions separately.

### Canonicalize payloads honestly

A digest is useful only if its input bytes or logical record sequence are reproducible. Specify field order, row order, Unicode normalization, number and timestamp representation, null encoding, compression scope, line endings, ignored transport fields, schema identity, and digest algorithm/version.

Hashing raw compressed bytes proves equality of that object representation, not semantic equality after decompression and parsing. Hashing a sorted logical record set may intentionally ignore source order, but that is unsafe when order carries meaning. Choose the equivalence required by the load, record both object checksum and logical digest when helpful, and never silently change canonicalization under an existing key namespace.

A cryptographic digest makes accidental collision negligible under its threat model; it does not authenticate an untrusted producer by itself. Bind manifests to trusted identities/signatures or access controls where adversarial replacement matters.

### Use an atomic effect-plus-receipt transaction

For a transactional target, the basic protocol is:

1. begin a target transaction under an isolation/concurrency contract sufficient for the claimed invariants;
2. insert or lock receipt key $(n,k)$ with expected digest and `in_progress` or terminal semantics;
3. if a terminal receipt exists with the same digest/contract, return its recorded result without reapplying;
4. if the key exists with different meaning, reject;
5. stage/validate deterministic candidates and apply all required effects;
6. store row/event effect identities, counts, controls, output snapshot/commit identity, and a successful receipt; and
7. commit once.

The success receipt and effects must share the transaction. If data commits first and the receipt later, a crash between them causes replay ambiguity. If receipt commits first, retry skips missing effects. An `in_progress` receipt in another transaction can also become a permanent false block after worker death unless it is only a lease and final success remains coupled to effects.

When a client times out during commit, it does not issue compensating writes based on guesswork. It reconnects and queries the receipt by stable key. Matching success means return recorded outcome. Absence means retry the whole transaction. A nonterminal/uncertain record requires the documented target recovery protocol.

### Enforce concurrency at the target

Sequential replay tests do not cover two workers attempting a new unit simultaneously. Both can check “receipt absent” and both apply effects before either inserts a marker. Use a unique constraint, atomic conditional put, compare-and-set, transactional lock, or serializable conflict—not a process-local precheck—as the arbiter.

The receipt table commonly has a unique key on namespace plus idempotency key. `INSERT ... ON CONFLICT` can claim it atomically in PostgreSQL, but exact behavior remains statement-, index-, and isolation-specific. PostgreSQL documents `ON CONFLICT DO UPDATE` as deterministic and rejects a command that would affect one existing row more than once; it also documents that applications at stronger isolation levels must be prepared to retry serialization failures.

Transaction retry must replay deterministic logic from stable inputs. Random defaults, current time, sequence allocation, mutable lookups, or external calls inside the retry can create a new meaning. Materialize nondeterministic decisions into the unit contract before the retry loop when they matter.

### Make insert-if-absent loads exact

For immutable facts with stable event identity, enforce a unique target constraint on the event/effect identity. An attempted duplicate with the same canonical payload is a no-op; an unequal payload under the identity is a conflict. Do not implement `SELECT` then `INSERT` without a concurrency mechanism.

An insert-only sink can preserve every legitimate source occurrence while suppressing redelivery. It does not automatically protect aggregates computed with `amount = amount + incoming.amount`; the aggregate write can repeat even if the fact insert is later found duplicate. Insert the fact/receipt and update dependent state in one transaction, derive aggregates from the fact table, or use an effect ledger keyed by event identity.

Physical uniqueness must match semantic uniqueness. A nullable unique key may permit multiple nulls depending on the target. Composite keys need canonical null/empty semantics. Target collation can equate strings the producer treats as distinct. Validate type conversion before using the converted value as the arbiter.

### Design deterministic current-state upserts

A current-state table usually needs entity key $K(e)$ and source version $V(e)$. A conditional mutation accepts event $e$ only when no row exists or

$$
V(e)>V_{stored}
$$

inside the same comparable version domain. Equal version and equal payload is replay. Equal version and unequal payload is conflict. Older version is a stale no-op with evidence, not an update.

The source version must represent causal/order semantics appropriate to the entity: database log position in a valid stream epoch, source revision, sequence, or version tuple. Ingestion time is not a safe replacement because retries and network delay change it. Wall-clock event time requires an explicit tie and clock policy.

Store tombstones or deletion versions long enough to prevent an older replay from resurrecting a deleted entity. Removing both row and version metadata makes “absent” indistinguishable from “never seen.” Retention and privacy requirements can be satisfied with minimal non-sensitive deletion identity/version evidence when policy permits, or by rebuilding from an authoritative bounded generation.

### Normalize source cardinality before merge

An upsert statement does not decide which of several candidates for one target key is authoritative. Before mutation, enforce or compute one candidate per target key using declared ordering and conflict rules. Preserve rejected/losing records and counts for audit.

For candidate multiset $B$ and target key function $K$, require

$$
\forall q:\left|\{e\in winner(B):K(e)=q\}\right|\le 1.
$$

“Take any row” is nondeterministic. “Take maximum version” still needs a rule for equal maximum versions with unequal payloads. A stable tiebreaker can make execution deterministic but must not invent source truth; conflicting identities often deserve quarantine.

Vendor `MERGE` behavior varies. BigQuery documents that an update/merge target row must match at most one source row in the relevant case. Snowflake documents deterministic and nondeterministic duplicate-join cases. PostgreSQL documents a cardinality violation when one `ON CONFLICT DO UPDATE` statement would affect one existing row more than once. Treat these errors as useful contract enforcement, not reasons to add arbitrary aggregation.

### Understand null and changing keys

SQL equality with two null operands yields unknown, not true. A nullable merge key can therefore fail to match an existing logically-null key and insert another row. Prefer non-null durable identity; otherwise use an explicit null-safe comparison supported by the engine and a uniqueness design with matching semantics.

Business keys can change. If the source represents a rename from old key to new key, a plain upsert on the new key leaves the old row behind. Carry stable entity identity plus operation semantics, or model the change as an atomic delete-old/insert-new transaction. Never infer deletion merely because a record is absent from one delta batch.

Key normalization changes—case folding, whitespace trimming, type conversion, Unicode handling—can collapse formerly distinct identities. Version and migrate the key contract, preflight collisions, and do not reuse old receipt namespaces under new canonicalization.

### Treat snapshot replacement as publication

For a complete snapshot or partition, writing immutable generation $g$ and atomically switching a trusted pointer is often clearer than millions of row upserts. Retries write or validate the same content-addressed objects. The pointer changes only after every planned partition, schema, count, digest, and control passes.

Let $M_g$ be the complete manifest for generation $g$. Publication is a conditional transition

$$
P:M_{old}\rightarrow M_g
$$

only if the expected current pointer still equals $M_{old}$ and $M_g$ is valid. A repeated transition to the already-published $M_g$ is a no-op. A competing newer generation causes a compare-and-set conflict rather than regression.

Do not truncate or overwrite the trusted target before replacement succeeds. Rename/swap operations, metadata commits, and object-store pointers have engine-specific atomicity and reader-consistency semantics. Verify them rather than infer them from one API call.

### Bound partial-batch behavior

If the target supports a batch transaction of acceptable size, atomic effect-plus-receipt gives a clean boundary. For very large units, use deterministic subunits with their own receipts plus a parent manifest that becomes trusted only when all expected children validate. A child can retry independently; the parent cannot publish partially.

Resuming from “last row number” is unsafe unless row enumeration is immutable, exact, and durably coupled to effects. Prefer stable child identities such as file digest and row-group, source key range, or offset interval. Every planned empty subunit must also produce evidence so absence is not mistaken for incomplete work.

Do not expose staging tables as trusted data. A failed attempt may leave fragments for diagnosis or garbage collection, but readers resolve only a complete generation/receipt. Cleanup is separate from correctness and must not race active attempts.

### Handle additive and non-idempotent transformations

Assignments such as `balance = source.balance` can be idempotent for a stable source version. Relative updates such as `balance = balance + delta` are not: replay adds again. Convert additive effects into an event/effect ledger with unique identity, then compute totals from accepted ledger rows or update totals atomically only when the ledger insertion is new.

Similarly, `count = count + 1`, sequence advancement, “append current time,” and list concatenation repeat effects. Some operations can be modeled as an idempotent set union keyed by immutable element identity. Others can use algebraic state with deduplicated operation IDs. The implementation must preserve the actual business semantics, not rewrite every operation as “last write wins.”

Commutative, associative aggregation can tolerate reordering, but duplicate inputs still matter unless the operation is also idempotent. Maximum is naturally idempotent for the same comparable value; sum is not. State the algebra and identity domain instead of relying on intuition.

### Couple checkpoints to durable effects

For a source position or micro-batch checkpoint $C$, advancing $C$ says earlier required effects are recoverable. The safe relation is

$$
C\preceq D,
$$

where $D$ is the greatest source position represented by the required durable effects or an authoritative replayable raw layer. If the checkpoint advances first, crash can cause loss. If effects commit first and checkpoint lags, replay occurs; idempotence makes that safe.

Apache Spark documents that `foreachBatch` provides at-least-once write guarantees by default and exposes `batchId` for deduplicating output. That batch ID is useful only within its documented query/checkpoint lineage and target namespace, with target-side receipts. Deleting checkpoints, changing query identity, splitting targets, or calling an external sink without coupled evidence can change the guarantee.

If one batch writes multiple independent sinks, a single framework checkpoint does not make their commits atomic. Land once in an authoritative transactional/raw sink and derive others idempotently, use an actual cross-sink transaction where available, or maintain per-sink receipts and withhold overarching success until reconciliation.

### Keep external effects out of blind retry loops

Database writes, message publication, file creation, notifications, API calls, and billing systems rarely share one transaction. Calling them between target mutation and receipt commit creates a dual-write gap.

The transactional outbox pattern records an intended external message in the same target transaction as the data effect. A relay publishes it with stable message identity; consumers deduplicate or otherwise make their own effects idempotent. This does not make the network deliver once, but it couples durable intent to the data commit and supports replay.

For an external API, use its documented idempotency key if the key lifetime, payload-conflict behavior, response replay, and scope meet the workflow. Otherwise introduce a governed mediator/ledger or a reconciliation/compensation protocol. Never assume HTTP `PUT` or `DELETE` makes a multi-system workflow idempotent merely because the method's intended server effect is defined as idempotent.

### Version schemas and transformation meaning

The same input bytes can produce different effects after code, lookup, timezone, schema, or policy changes. Decide whether replay means reproduce the original result or intentionally recompute under a new contract. Include the relevant transformation/schema/reference-data version in receipt evidence and, where semantics differ, in the logical unit namespace.

A bug fix is not necessarily a retry. It may be a correction generation with a new identity linked to the superseded result. Reusing the old key and overwriting its digest destroys audit meaning; silently returning the old receipt prevents correction. Model supersession explicitly.

Schema migration and target constraint changes can invalidate old upserts. Preserve raw inputs and interpretation metadata for rebuild. Test old-unit replay against supported code versions, or declare a finite replay horizon and a documented rebootstrap path.

### Retain receipts for the real retry horizon

Receipt lifetime must cover maximum source redelivery, orchestrator retry, backfill overlap, disaster recovery, and delayed external callback periods. If receipts expire while the original effects remain, a late duplicate can be accepted as new.

Let $T_r$ be receipt retention and $T_d$ the maximum duplicate/retry horizon under all producers and recovery paths. A basic safety requirement is

$$
T_r\ge T_d,
$$

unless another durable uniqueness/version mechanism survives longer. This inequality is only as reliable as the horizon inventory; unbounded manual replay demands durable generation/event identity or an explicit namespace rollover/rebuild protocol.

Archive receipts with sufficient lineage if the hot store must remain small. Compaction can retain key, payload digest, outcome, source range, target commit/snapshot, and policy dates without every verbose attempt log. Privacy classification applies to receipts and digests too.

### Observe decisions, not just executions

For each logical unit record key/namespace, payload and contract digests, source boundaries, first/last attempt, attempt count, outcome, rows proposed/accepted/stale/conflicting/rejected/deleted, target commit/snapshot, checkpoints, code/schema version, controls, latency, and owner. Record physical attempt IDs separately.

Metrics should distinguish successful first applications, matching replays, payload conflicts, concurrent claim conflicts, serialization/deadlock retries, stale versions, partial staging cleanup, ambiguous commit lookups, and receipt-retention headroom. A falling row-write count can mean healthy replay suppression or missing inputs; expected-unit reconciliation disambiguates it.

Trace input manifest to receipt to row/event effect identities and published datasets. Logs alone are not durable proof if they can be sampled, rotated, or emitted before transaction commit.

### Reconcile both coverage and exclusivity

Idempotence proves repeated same-unit application does not change intended effect. It does not prove that every expected unit arrived, that input content was correct, or that no unauthorized unit affected the target.

Use two directions:

1. **coverage:** every expected input unit has one terminal accepted or explicitly resolved receipt and its promised effects/controls;
2. **exclusivity:** every trusted target generation/effect traces to an accepted governed unit.

Compare key sets, versions, tombstones, counts, control totals, digests, and source/target positions at compatible cuts. Equal totals can hide one duplicate and one omission. Current-state equality cannot prove intermediate history if event preservation is required.

### Test the failure matrix

Inject crashes before receipt claim, after claim, during staging, after some conditional writes, before commit, during commit acknowledgement, after target commit but before source checkpoint, and after checkpoint. Restart with the same unit and verify one intended effect plus accurate attempt evidence.

Race two first attempts; retry serialization and deadlock failures; send the same key with changed content; send the same event twice in one batch and across batches; send two versions of one entity in reverse order; send equal version with conflicting content; delete then replay an older update; change a business key; supply null keys; generate multiple source rows per target; and cross a schema/code version boundary.

For immutable generations, omit one child, duplicate a child, corrupt a checksum, lose pointer acknowledgement, publish competing generations, and run cleanup during an active attempt. For external effects, lose acknowledgements on both sides of the outbox/relay boundary.

Successful finite tests provide evidence for those cases and versions. They do not prove every target isolation behavior, driver retry, storage consistency, or failure timing. Combine tests with documented contracts, constraints, transaction logs, reconciliation, and production monitoring.

## Definitions and Notation

Let:

- $S$ be observable target state inside the declared idempotence boundary;
- $u$ be one logical load unit and $a$ one physical attempt;
- $n$ be identity namespace and $k$ the stable idempotency key;
- $h$ be canonical input payload digest and $c$ interpretation-contract digest;
- $I(e)$ be source event/effect occurrence identity;
- $K(e)$ be entity/business identity affected by event $e$;
- $V(e)$ be source version in a declared comparable domain;
- $R(n,k)$ be the durable receipt for a logical unit;
- $E$ be accepted effect identities;
- $P$ be the trusted dataset-generation pointer;
- $C$ be a committed source/orchestrator checkpoint;
- $D$ be the greatest source position durably recoverable by required effects/raw data;
- $T_d$ be maximum duplicate/retry horizon; and
- $T_r$ be receipt/identity retention horizon.

The idempotence equation is

$$
L(L(S,u),u)=L(S,u).
$$

For any number $m\ge1$ of identical accepted replays,

$$
L^m(S,u)=L(S,u).
$$

This says nothing about a different unit $v$, even if $K(u)=K(v)$. For a versioned current-state projection, accept a candidate only when its version is newer, treat equal-version/equal-digest as replay, and treat equal-version/unequal-digest as conflict:

$$
decide(e)=
\begin{cases}
insert, & K(e)\notin S,\\
update, & V(e)>V_S(K(e)),\\
replay, & V(e)=V_S(K(e))\land h(e)=h_S(K(e)),\\
conflict, & V(e)=V_S(K(e))\land h(e)\ne h_S(K(e)),\\
stale, & V(e)<V_S(K(e)).
\end{cases}
$$

Version comparison is undefined across incompatible source/topology epochs unless the contract provides an ordering. Do not force incomparable values into this function.

For one batch candidate set $B$, deterministic target cardinality requires at most one winner for each target key:

$$
\forall q:\left|\{e\in winner(B):K(e)=q\}\right|\le1.
$$

The receipt uniqueness invariant is

$$
R(n,k)=(h,c,o)\implies retry(n,k,h',c')
\begin{cases}
returns\ o, & (h',c')=(h,c),\\
fails, & (h',c')\ne(h,c).
\end{cases}
$$

Checkpoint and retention safety require $C\preceq D$ and $T_r\ge T_d$ under their stated domains. These are necessary operational conditions, not sufficient proof of correct input or transformation.

## Mechanisms, Invariants, or Proof Structure

**Conditional atomic-receipt theorem.** Suppose one target transaction (1) uniquely binds $(n,k)$ to $(h,c)$, (2) deterministically applies every required effect for $u$, (3) records effect identities and terminal receipt, and (4) atomically commits or aborts them together. Suppose concurrent transactions are serialized or conflicting claims cause safe retry. Then every accepted attempt with the same $(n,k,h,c)$ yields the same committed intended target effect as one attempt; a different payload/contract under the key is rejected.

**Proof sketch.** For the first committed attempt, atomicity makes effects and receipt visible together. Any attempt that aborts changes neither trusted effects nor receipt. Any later or concurrent accepted retry observes or conflicts on the unique receipt key. Once it observes the matching terminal receipt, it returns recorded outcome without applying effects; a different digest/contract fails. Therefore the number of physical attempts does not change the intended effect. The theorem does not cover effects outside the transaction, incorrect canonicalization, expired receipts, or operations omitted from $p$.

**Stable-unit invariant.** Logical retry preserves namespace, key, payload meaning, schema/code interpretation, source boundaries, and target. A correction or recomputation with different meaning receives a new linked identity.

**Key-binding invariant.** One $(n,k)$ binds permanently for its retention horizon to one $(h,c)$. Same-key/different-meaning input is conflict, never silent replay.

**Atomic evidence invariant.** Trusted effects and the terminal receipt share one atomic boundary, or effects land in an authoritative replayable layer whose receipt/checkpoint shares that boundary.

**Cardinality invariant.** Candidate normalization produces at most one authoritative mutation per target key per statement/transaction, with explicit equal-version conflicts and loser evidence.

**Occurrence-versus-entity invariant.** $I(e)$ suppresses repeat delivery of one occurrence; $K(e)$ groups legitimate versions of the same entity. Neither substitutes for the other.

**Version monotonicity invariant.** Target state/tombstone for $K(e)$ never moves backward in a comparable $V$ domain. Equal version with unequal content blocks; an older event produces no current-state mutation.

**Publication invariant.** A snapshot/partition generation becomes trusted only as a complete validated manifest through an atomic conditional pointer/metadata commit. Staging fragments remain untrusted.

**Checkpoint invariant.** $C\preceq D$. Replay caused by $C\prec D$ is tolerated; $C\succ D$ may lose unrepresented effects.

**Retention invariant.** Receipt/event/tombstone evidence outlives every permitted duplicate and recovery route, or a superseding immutable generation and namespace transition closes the old replay domain.

**Side-effect invariant.** Each effect outside the primary transaction has its own stable identity and receipt/outbox/reconciliation contract. Primary-table idempotence is not advertised as workflow idempotence.

**Reconciliation boundary.** Receipt uniqueness establishes one accepted meaning per observed key. Expected-unit coverage and source correctness require independent manifests, ranges, controls, and compatible-cut comparisons.

<!-- bijux-verify: {"id":"atomic-idempotent-load","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"accepted=3\nreplayed=3\nstale=1\ndeleted=True\natomic_failure=True\nambiguous_retry_safe=True\npayload_conflict=True\ncurrent=a:12@3,c:30@1\nreceipts=2\n","stderr":""}} -->
```python
from hashlib import sha256

class Warehouse:
    def __init__(self):
        self.rows = {"a": (1, 10), "b": (1, 20)}
        self.tombstones = {}
        self.events = {}
        self.receipts = {}

    def load(self, key, records, fail_before_commit=False):
        canonical = repr(tuple(records)).encode()
        digest = sha256(canonical).hexdigest()
        if key in self.receipts:
            if self.receipts[key]["digest"] != digest:
                raise ValueError("idempotency key reused with different payload")
            return dict(self.receipts[key]["result"]), True

        rows = dict(self.rows)
        tombstones = dict(self.tombstones)
        events = dict(self.events)
        accepted = stale = 0

        for event_id, entity, version, operation, value in records:
            payload = (entity, version, operation, value)
            if event_id in events:
                if events[event_id] != payload:
                    raise ValueError("event identity conflict")
                continue

            current_version = max(
                rows.get(entity, (-1, None))[0],
                tombstones.get(entity, -1),
            )
            if version <= current_version:
                stale += 1
                events[event_id] = payload
                continue

            if operation == "delete":
                rows.pop(entity, None)
                tombstones[entity] = version
            else:
                rows[entity] = (version, value)
                tombstones.pop(entity, None)
            events[event_id] = payload
            accepted += 1

        result = {"accepted": accepted, "stale": stale}
        if fail_before_commit:
            raise RuntimeError("modeled crash before atomic commit")

        self.rows, self.tombstones, self.events = rows, tombstones, events
        self.receipts[key] = {"digest": digest, "result": dict(result)}
        return result, False

warehouse = Warehouse()
batch = (
    ("e-1", "a", 3, "upsert", 12),
    ("e-2", "b", 2, "delete", None),
    ("e-3", "c", 1, "upsert", 30),
    ("e-4", "a", 2, "upsert", 11),
)

before = (dict(warehouse.rows), dict(warehouse.receipts))
try:
    warehouse.load("orders/eu/42", batch, fail_before_commit=True)
except RuntimeError:
    pass
atomic_failure = before == (warehouse.rows, warehouse.receipts)

first, was_replay = warehouse.load("orders/eu/42", batch)
after_first = (
    dict(warehouse.rows),
    dict(warehouse.tombstones),
    dict(warehouse.events),
)
second, was_replay = warehouse.load("orders/eu/42", batch)
ambiguous_retry_safe = after_first == (warehouse.rows, warehouse.tombstones, warehouse.events)

payload_conflict = False
try:
    warehouse.load("orders/eu/42", batch[:-1])
except ValueError:
    payload_conflict = True

warehouse.load("orders/eu/43", (("e-5", "a", 1, "upsert", 9),))
current = ",".join(
    f"{key}:{value}@{version}"
    for key, (version, value) in sorted(warehouse.rows.items())
)
print(f"accepted={first['accepted']}")
print(f"replayed={second['accepted']}")
print(f"stale={first['stale']}")
print(f"deleted={'b' not in warehouse.rows and warehouse.tombstones['b'] == 2}")
print(f"atomic_failure={atomic_failure}")
print(f"ambiguous_retry_safe={was_replay and ambiguous_retry_safe}")
print(f"payload_conflict={payload_conflict}")
print(f"current={current}")
print(f"receipts={len(warehouse.receipts)}")
```

This executable fixture models copy-on-write atomic commit in one process. It shows a crash before commit leaving no effects, matching batch replay returning its receipt, different payload under the same key failing, a tombstone blocking resurrection, and an older version becoming stale. It does not model a database isolation level, simultaneous processes, hash adversaries, durable storage, or external side effects.

## Alternatives and Trade-Offs

**Atomic receipt ledger versus target-only uniqueness.** A receipt ledger provides unit-level outcome, payload binding, counts, and ambiguous-commit lookup. Target unique event IDs can be simpler and finer grained, but may not prove whole-batch completeness. Many systems use both.

**Row upsert versus immutable generation replacement.** Upserts minimize rewritten data and suit current-state deltas. Immutable generations provide clean dataset atomicity and reproducibility but require temporary space and metadata publication. Choose by unit, reader contract, and target capability.

**Event ledger versus direct additive update.** A unique event ledger makes deltas replay-safe and auditable, then derives aggregates. Direct conditional counters can reduce storage/latency but require atomic operation-ID tracking and complicate rebuild.

**Source version ordering versus last-write-wins time.** Source versions prevent ingestion-delay regression when their domain is valid. Wall-clock last-write-wins is portable-looking but depends on clock/tie semantics and may discard corrections. Preserve conflicts where order is not authoritative.

**One receipt per batch versus one per row/event.** Batch receipts reduce metadata and establish whole-unit completion. Fine-grained receipts enable partial restart and cross-batch redelivery handling. Hierarchical parent/child receipts can combine them at greater complexity.

**Database transaction versus staged publication.** A database transaction gives strong atomicity within size/resource limits. Staged immutable outputs plus atomic pointer work across large/object datasets but move correctness into manifest completeness and conditional publication.

**Strict payload conflict versus overwrite.** Failing same-key/different-payload protects audit meaning. Overwrite seems operationally convenient but turns identity into mutable state. Corrections should use explicit superseding identities.

**Pessimistic lock versus optimistic uniqueness/compare-and-set.** Locks can simplify one-writer reasoning but reduce concurrency and need timeout/dead-owner handling. Optimistic conflicts scale under low contention but require deterministic retry and clear conflict classification.

**Retain receipts indefinitely versus bounded retention.** Indefinite identity evidence maximizes replay safety but costs storage and may conflict with privacy. Bounded retention requires a proven duplicate horizon plus namespace rollover, tombstone/uniqueness survival, or rebuild-only policy.

**Framework delivery feature versus sink protocol.** Framework checkpoints and transactional integrations can reduce work within supported topology. Sink-side identity remains valuable across resets, manual backfills, migrations, and external effects. Claims should stop at verified boundaries.

**No-op stale event versus quarantine.** Ignoring older versions protects current state and can be expected under reordering. High or unexplained stale volume can indicate corrupted ordering, wrong epochs, or bad source versions; preserve metrics/evidence and quarantine conflicts rather than hide them.

## Failure Modes and Misconceptions

**“The statement is `MERGE`, so the load is idempotent.”** Merge syntax does not define stable input identity, source cardinality, order, deletes, concurrency, receipt coupling, or external effects. A clause that adds a delta can repeat; multiple source matches can error or behave nondeterministically.

**“The scheduler run ID is an idempotency key.”** Retry attempts often receive new run IDs, while manual reruns may reuse parameters with changed code. Derive a stable logical key and record attempt IDs separately.

**“A random UUID prevents duplicates.”** A new UUID per attempt guarantees that retries look distinct. Producer-assigned stable event IDs help only if the producer persists/replays them with the same occurrence.

**“Primary key means event identity.”** A primary key for the current entity collapses versions. Event identity suppresses delivery repeats; entity key chooses the current-state subject. Both may be required.

**“Check then insert is safe.”** Two workers can both see absence. Use target-enforced uniqueness or atomic condition under sufficient concurrency control.

**“Same key means same request.”** Keys can be accidentally reused after producer bugs, partition rewrites, tenant collisions, or changed canonicalization. Bind key to content and contract digests and reject mismatch.

**“Success marker first prevents duplicate work.”** It can permanently certify effects that never committed. Terminal receipt and effects must share an atomic boundary.

**“Data first, marker second is harmless.”** A crash between commits leads the retry to repeat effects. This is safe only when every effect independently suppresses replay and whole-unit completeness can still be proven.

**“A timeout means rollback.”** The server may have committed before acknowledgement was lost. Query by stable receipt/transaction evidence rather than infer from client outcome.

**“Upsert protects against late data.”** An unconditional update overwrites new state with old state. Compare source versions and retain delete versions/tombstones.

**“Maximum version always finds truth.”** Versions may be incomparable across topology epochs; equal versions can carry conflicts; an erroneous high version can poison state. Validate domain and retain adjudication evidence.

**“One source row always matches one target row.”** Dirty target uniqueness, nullable keys, and duplicated source candidates break cardinality. Preflight and enforce it.

**“Affected row count proves the load.”** Engines differ in reporting inserted, updated, matched-but-unchanged, or deleted rows. Counts do not prove exact identities or payloads.

**“Truncate and reload is naturally idempotent.”** Repeating a completed reload may converge, but a failure after truncate exposes missing/partial data. Build and validate away from the trusted pointer, then publish atomically.

**“Append-only files are safe because paths are unique.”** Attempt-specific paths can duplicate logical data. Content-addressed child identities plus a single manifest publication define trusted membership.

**“Exactly-once streaming removes sink design.”** The guarantee is bounded to named engines, sources, sinks, checkpoints, transactions, and failure modes. Custom callbacks and multi-sink workflows often remain replay-prone.

**“Deduplication can happen eventually.”** Consumers may observe duplicate effects before cleanup, and additive downstream work can become irreversible. Suppress at the governed effect boundary or explicitly accept provisional semantics.

**“Delete needs no receipt because the row is gone.”** Absence forgets the deletion version and permits older replay to resurrect state. Preserve minimal governed tombstone/version evidence.

**“Retrying serialization failures is always safe.”** The transaction body must derive the same logical effects from stable inputs. External calls, random values, sequences, or current lookups can change meaning.

**“Receipts can be dropped after a successful day.”** Source redelivery, manual replay, and disaster recovery may occur later. Align retention with every recovery path, not the normal schedule.

**“Current state equality proves exactly one load.”** Two applications may overwrite to the same values while duplicating events, audit, cost, or downstream actions. Audit effect identities and coverage at the required boundary.

## Worked Examples

### Example 1

A daily file has manifest key `billing/us/2026-09-01`, object version `v18`, logical digest `h1`, schema `s4`, and 2,400 expected rows. The loader writes a receipt keyed by dataset, region, date, and object version, binding it to `h1/s4`. Row effects and the receipt commit in one warehouse transaction. The client loses acknowledgement; retry reads the successful receipt and returns its recorded 2,400 accepted rows without scanning the target for guesses. A replacement object under the same object version but digest `h2` fails as an identity conflict.

### Example 2

Two workers concurrently load new event `payment-event-77`. Both attempt an insert into an event ledger with a unique constraint on producer epoch plus event ID. One transaction inserts the ledger row, updates the derived account projection, records its unit receipt, and commits. The other conflicts, reloads the accepted digest, and returns replay success only if content matches. A prior application-level `SELECT` could improve messaging but is not the correctness arbiter.

### Example 3

A batch contains account `a` at versions 8, 9, and 9. The two version-9 payloads differ. Selecting `MAX(version)` does not yield one meaning. The normalizer groups by entity, identifies the unequal tie, quarantines the entity's candidates, and prevents the batch receipt from claiming full success unless the contract permits partial acceptance with explicit child outcomes. Choosing the lexicographically larger payload would be deterministic execution but fabricated business precedence.

### Example 4

The target stores customer `c` at version 14. Delivery brings version 12, then delete version 15, then a replay of version 14. Version 12 is stale. Version 15 removes the current row and stores tombstone `(c,15)`. Version 14 remains stale against the tombstone and cannot resurrect the customer. Privacy policy permits retention of the pseudonymous identity/version but not the deleted payload.

### Example 5

A full product partition consists of 16 planned hash buckets. Each bucket is written under generation `g52` with its stable bucket ID, row count, checksum, and schema digest. Bucket 7 fails and retries to the same content address. The manifest cannot validate until all 16 receipts, including zero-row buckets, exist. A conditional pointer swap publishes `g52`; loss of acknowledgement is resolved by reading the pointer. Cleanup never deletes generations referenced by readers or active attempts.

### Example 6

A replayable order delta says `quantity += 3`. Running the SQL twice adds six. Instead, the load inserts `(order-9, adjustment-event-4, +3)` into a unique adjustment ledger and derives quantity from accepted adjustments, or conditionally applies the counter update only in the transaction where that event identity was newly inserted. A repeated event returns the original receipt and contributes zero additional delta.

### Example 7

A Spark `foreachBatch` callback receives batch ID 118. The sink receipt namespace includes the stable query/checkpoint identity and target, not just integer 118. It writes batch effects and receipt in one database transaction. A retry of 118 is a no-op. If operators delete the checkpoint and start a new query lineage, they do not assume its batch 118 is the old unit; raw event identities or a new namespace govern overlap.

### Example 8

A load writes a warehouse table and sends a completion message. Sending before commit can announce absent data; sending after commit can be lost or duplicated. The warehouse transaction writes data, receipt, and outbox record with stable message identity. A relay retries publication. The consumer records the message identity with its own effect. The design claims replay-safe effects across these bounded protocols, not one distributed transaction.

### Example 9

A team changes currency conversion from daily closing rates to transaction-time rates. Replaying yesterday's file with new code is not the same logical operation, even though the input bytes match. They create a correction generation whose identity includes transformation contract `fx-transaction-time-1`, links it to the superseded receipt, validates control totals, and atomically republishes the partition. The original receipt remains immutable audit evidence.

### Example 10

Receipt retention is 30 days, but a disaster-recovery exercise restores raw files from 90 days ago and replays them into a target whose event unique indexes survived only 45 days. The architecture cannot claim safe replay over 90 days. It must extend compact receipt/event identity retention, rebuild a fresh empty generation in a new namespace, or prohibit in-place replay beyond the proven horizon and document the rebootstrap procedure.

## Cross-Program Connections

**Database Engineering.** Unique constraints, transaction atomicity, isolation, locking, write conflicts, MVCC, conditional updates, and recovery determine whether effect-plus-receipt protocols actually serialize concurrent attempts.

**Distributed Systems.** Ambiguous outcomes, retry protocols, stable request identity, duplicate delivery, consensus-backed conditional writes, leases, fencing, and the limits of cross-system atomicity explain why idempotence is foundational.

**API and Service Engineering.** HTTP method semantics and API idempotency keys offer a parallel at request boundaries. Data workflows must still validate key scope, payload binding, lifetime, response replay, and downstream effects.

**Software Engineering Patterns.** Command identity, repositories, unit of work, outbox, immutable value objects, and explicit state machines help separate logical operations from attempts and couple evidence to effects.

**Programming Languages.** Equality, hashing, serialization, numeric/time representations, side effects, and pure/deterministic functions shape canonical payloads and repeatable transformations.

**Security Engineering.** Tenant-scoped identities, authenticated manifests, collision/abuse resistance, replay authorization, least privilege, sensitive receipts, and audit integrity prevent idempotence controls from becoming cross-tenant or replay attack surfaces.

**Systems Engineering.** Hazard analysis treats double application, omission, regression, partial publication, and false completion as system-level failure modes spanning source, transport, sink, orchestrator, and operators.

**Data Architecture and Governance.** Ownership, lineage, retention, correction, supersession, and authoritative dataset boundaries determine which repeated effects are equivalent and how evidence must persist.

## References

1. IETF, [RFC 9110: HTTP Semantics, Section 9.2.2—Idempotent Methods](https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2.2). Defines idempotence in terms of the intended server effect of multiple identical requests and distinguishes incidental per-request effects.
2. PostgreSQL Global Development Group, [PostgreSQL: INSERT](https://www.postgresql.org/docs/current/sql-insert.html). Documents `ON CONFLICT`, arbiter constraints, and the deterministic/cardinality behavior of `ON CONFLICT DO UPDATE`.
3. PostgreSQL Global Development Group, [PostgreSQL: Transaction Isolation](https://www.postgresql.org/docs/current/transaction-iso.html). Documents isolation phenomena, concurrent DML behavior, and the need to retry serialization failures at stronger levels.
4. Apache Spark, [Structured Streaming Programming Guide: Using foreach and foreachBatch](https://spark.apache.org/docs/latest/streaming/apis-on-dataframes-and-datasets.html#using-foreach-and-foreachbatch). Documents default at-least-once `foreachBatch` writes and use of `batchId` for output deduplication.
5. Google Cloud, [BigQuery GoogleSQL DML Syntax: MERGE Statement](https://cloud.google.com/bigquery/docs/reference/standard-sql/dml-syntax#merge_statement). Documents merge matching, multiple-source-row errors for updated targets, null comparison concerns, and atomic replace using a constant-false predicate.
6. Snowflake, [MERGE](https://docs.snowflake.com/en/sql-reference/sql/merge). Documents clause behavior and deterministic versus nondeterministic duplicate source-to-target joins.
7. Delta Lake, [Table Deletes, Updates, and Merges](https://docs.delta.io/latest/delta-update.html). Documents merge-based deduplication, within-source deduplication needs, and the requirement for idempotent merge logic under replayable `foreachBatch` execution.
8. Martin Kleppmann, [Designing Data-Intensive Applications, Second Edition](https://dataintensive.net/). Provides background on retries, idempotence, event identity, transactions, distributed-system faults, stream processing, and derived-data reliability; consult the cited edition for full context.

## Exercises

### Exercise 1

A loader uses scheduler attempt UUID as its receipt key. Attempt A inserts 10,000 rows and commits, but loses acknowledgement. Attempt B gets a new UUID and replays the same manifest. Explain why the scheme is not idempotent. Propose a stable unit identity, payload-binding rule, transaction boundary, and ambiguous-commit recovery query. State what remains outside the claim.

### Exercise 2

The target holds `x=(version 5,value 40)` and tombstone `y=(version 7)`. A batch delivers, in order: event `a` for `x` version 6 value 44; `b` for `x` version 4 value 30; `c` for `y` version 6 value 9; duplicate `a`; and `d` for `z` version 1 value 8. Under event-identity deduplication and strict version monotonicity, compute accepted effects, stale occurrences, replay occurrences, and final state.

### Exercise 3

A source batch contains target key `p` at versions 10/value A, 12/value B, and 12/value C; target key `q` at versions 3/value D and 4/value E; and target key `r` once. Design a deterministic normalization rule that does not fabricate precedence. Which keys can proceed, which must conflict, and what evidence belongs in the parent receipt?

### Exercise 4

A pipeline writes a database table, an object-store export, and a notification service. No distributed transaction spans them. Design a replay-safe architecture using an authoritative commit, outbox or publication manifest, stable identities, per-sink receipts, and reconciliation. Identify precisely what “success” means and where duplicate delivery can still occur.

### Exercise 5

The maximum broker redelivery is 14 days, scheduled retry is 7 days, manual in-place replay is allowed for 60 days, and disaster recovery can restore 180-day raw inputs. Hot receipts last 30 days and compact receipt keys/digests last 90 days; target event uniqueness lasts 45 days. Evaluate safe replay horizons for normal retry, manual replay, and disaster recovery. Give two durable remedies without assuming that increasing one arbitrary timeout proves safety.

## Answers to the Exercises

### Answer 1

The UUID identifies a physical attempt, so A and B look like different logical operations. If the target is append-oriented, B can add another 10,000 effects; even if row upserts converge, attempt-level audit or downstream effects may duplicate. Define the unit from immutable source meaning, for example `(dataset, tenant, manifest_id, source_object_version)` and bind it to canonical manifest/data digest, schema digest, and transformation contract. In one sufficient target transaction, apply all governed row/event effects and insert the terminal receipt with counts and target commit identity. On timeout, query that receipt by stable key: matching success returns the recorded result; absence retries; changed digest conflicts. The claim excludes object exports, messages, notifications, or other sinks unless they have coupled outbox/receipt protocols, and it does not prove that the source manifest itself is correct or complete.

### Answer 2

Event `a` is accepted: `x` moves from version 5/value 40 to version 6/value 44. Event `b` is a distinct occurrence but stale because version 4 is below stored version 6. Event `c` is stale against tombstone `y` version 7, so it cannot resurrect `y`. The repeated `a` is one replay occurrence, not a second update. Event `d` is accepted and inserts `z=(1,8)`. Thus there are two accepted effects (`a`, `d`), two stale new occurrences (`b`, `c`), one duplicate delivery/replay, and final current rows `x=(6,44)`, `z=(1,8)` with tombstone `y=(7)`. The event ledger may record stale occurrence identities so their later redelivery is classified consistently.

### Answer 3

Group candidates by target key, then by comparable source version. Select the unique greatest version only when all candidates at that greatest version have the same canonical payload/operation; exact repeated occurrence IDs are removed first, while different occurrence IDs with identical payload remain governed according to the source contract. Key `q` proceeds with version 4/value E and key `r` proceeds with its sole candidate. Key `p` conflicts because the greatest version 12 has unequal values B and C; lexicographic or arrival-order choice would invent precedence. The parent evidence records expected/proposed counts, per-key winners, the rejected lower versions, the `p` conflict identities/digests, code/schema/version-domain identifiers, and whether policy makes the whole parent fail atomically or publishes only explicitly complete child units. A full-success receipt cannot conceal the unresolved key.

### Answer 4

Choose the database transaction as authoritative: it commits table effects, the load receipt, and outbox records for an export request and notification intent, each with stable IDs derived from the logical load. An export worker writes immutable content-addressed objects, validates them, and conditionally publishes one manifest; its receipt binds message ID to object/manifest digests. A notification relay calls a service with a stable idempotency key if supported and records the observed terminal response; its consumer also deduplicates when possible. The load is globally “complete” only when the database receipt and required sink receipts reconcile to the expected outbox set. The database commit can be exactly atomic within its contract; delivery to workers may repeat, object writes may be retried, and notification requests may be duplicated on the network. The bounded claim is one published export and one intended notification effect under each sink's verified identity/retention semantics, not one physical delivery.

### Answer 5

Normal automated retry/redelivery is covered because both hot receipts (30 days) and longer-lived uniqueness exceed the maximum 14-day broker and 7-day schedule horizons. Manual in-place replay at 60 days is not safely covered by hot receipts or 45-day target uniqueness, but compact receipt keys/digests last 90 days and can cover it only if they remain authoritative, queryable before effects, preserve the full namespace/payload binding, and are coupled to surviving effects. In-place disaster-recovery replay at 180 days is not covered: all listed identity evidence expires by 90 days. Remedies include retaining compact authoritative receipt/event/tombstone identity for at least the full 180-day recovery horizon with tested restore procedures, or rebuilding a new empty immutable target generation in a new namespace from the restored raw corpus and publishing it after complete validation rather than replaying into surviving state. The team must also align schema/code/input retention and source-unit manifests; extending a receipt TTL alone does not make old inputs interpretable or complete.
