---
module_id: LSDS-050
program: Large-Scale Data Systems Engineering
level: 1
module_number: 50
title: Reprocessing a Stream Without Double-Applying Effects
status: complete
last_verified: 2026-09-04
---

# Reprocessing a Stream Without Double-Applying Effects

## One-Page Review

### Governing question

How can a streaming system replay historical input to rebuild correct results without charging, notifying, provisioning, publishing, or otherwise changing the outside world more than once for the same logical operation?

### Essential definitions

- A **logical effect** is the business-visible change intended once, such as charging an order or establishing one current projection value.
- A **physical attempt** is one execution of code that may request that effect; replay and retry can create several attempts.
- An **idempotency key** identifies one logical effect across every attempt that may produce it.
- A **payload fingerprint** is a deterministic digest of the canonical operation parameters associated with a key.
- A **deduplication ledger** durably records a key, fingerprint, status, outcome, and relevant epoch so repeat attempts can return the prior result.
- An **ambiguous outcome** occurs when a caller cannot tell whether a destination committed an effect, commonly after a timeout or lost response.
- A **fencing token** is a monotonically ordered generation that lets a destination reject writes from an obsolete worker.
- A **transactional outbox** stores domain state and an effect intent in one local transaction; a relay may deliver the intent repeatedly.
- An **inbox** records consumed effect identities atomically with a consumer's local change.
- A **compensating effect** is a new business action that counteracts an earlier effect; it is not time travel or database rollback.
- A **shadow replay** recomputes in an isolated namespace with external effects disabled, then compares results before controlled cutover.

### Central model, mechanism, or theorem

Let $k$ be a stable logical-effect key, $h$ a canonical payload fingerprint, and $D[k]=(h,o,s,e)$ the destination's durable record of fingerprint, outcome, status, and fencing epoch. The destination must perform one atomic decision:

1. if $k$ is absent, validate authority and epoch, apply or durably schedule the effect, and store its outcome;
2. if $k$ exists with the same $h$, return the recorded outcome without applying the effect again; and
3. if $k$ exists with a different $h$, reject or quarantine the conflict.

Exactly-once logical effect requires a stable key, deterministic payload, durable retention covering every possible replay, atomicity between the deduplication decision and effect, stale-writer fencing, and recoverable outcomes. Exactly-once operator state alone does not provide these properties for an external destination.

### Critical invariants

- Logical-effect identity is stable across retry, restart, rescale, replay, correction, and software deployment.
- Attempt IDs are never substituted for effect IDs; a new attempt does not authorize a new business action.
- The same key denotes the same canonical intent; a same-key/different-payload request is a conflict, not a retry.
- The destination atomically records acceptance and the effect, or exposes a native idempotency/transaction protocol with equivalent scope.
- A successful repeat returns the original durable outcome rather than manufacturing a second outcome.
- Deduplication retention exceeds the maximum retry, outage, source retention, backfill, correction, and disaster-recovery horizon plus margin.
- Restored or concurrent workers cannot commit with an epoch older than the destination's accepted fencing token.
- Checkpoint completion commits only the sink work prepared for that checkpoint; recovery resolves prepared transactions deterministically.
- Reprocessing defaults to an isolated materialization and disabled/sandboxed side effects; production cutover is explicit and auditable.
- Reconciliation accounts for every intended effect as applied once, safely pending, rejected, compensated, or requiring intervention.

### Common failures

Common failures include using partition offset as permanent business identity; creating a fresh idempotency key on every retry; recording deduplication after a remote call; treating `ON CONFLICT DO NOTHING` as proof that the payload matched; expiring keys before a long replay; overwriting with wall-clock last-write-wins; assuming checkpoints cover arbitrary APIs; replaying notifications or charges through the live channel; retrying a timed-out non-idempotent request blindly; letting a restored worker commit after its replacement; deleting old materialization before comparison; treating compensation as rollback; and reporting exactly-once without naming the source, state, sink, visibility, identity, retention, and failure scope.

### Compact example

A replay issues four physical requests: charge order 7 for 100, the identical request again, charge order 8 for 250, and then reuse order 7's key for 120. An atomic ledger applies two logical effects totaling 350, returns order 7's original receipt for the retry, and rejects the conflicting 120 request. Counting function calls would say four; the business ledger correctly says two.

### Connections

[LSDS-042](042-partitioned-consumption.md) supplies source positions and ownership. [LSDS-047](047-checkpoint-barriers.md) and [LSDS-048](048-state-snapshots-and-recovery.md) explain replay after checkpoints. [LSDS-049](049-backpressure-across-operators.md) bounds replay pressure. This module supplies the effect boundary needed before later modules address broader streaming operations.

## Governing Question

Recovery deliberately repeats computation. A worker can process a record, call a payment API, and fail before its checkpoint completes. On restore, the input position and managed state return to the checkpoint, so the worker executes the record again. The state machine may still be exactly once, while the customer is charged twice.

The same danger appears without failure. Teams replay retained input after fixing a bug, recompute a projection with new code, backfill a newly added field, or rebuild after corrupt state. Reprocessing may execute millions of old logical operations. Some outputs are replaceable data; others are irreversible interactions with people, money, inventory, credentials, or legal workflows.

The governing question is therefore about an end-to-end protocol, not a runtime switch. Which effects are being protected? What stable identity survives every replay? Where is the atomic decision? How long is its evidence retained? How are conflicting requests, ambiguous responses, stale writers, corrections, and cutover handled? A useful answer names the exact boundary within which “once” holds and gives a recovery story for every crash window.

## Why This Matters

Replay is a foundational advantage of logs and deterministic dataflows. It permits correction, audit, disaster recovery, migration, and reproducible views. Yet replay is safe only when recomputation is separated from external action. Otherwise the mechanism intended to repair state becomes a mass-duplication mechanism.

Effects have different algebra. Setting projection row `customer-7` to version 12 can be an idempotent replacement. Appending a distinct audit fact is safe if consumers deduplicate its stable identity. Incrementing a counter, sending a welcome email, issuing a credential, decrementing inventory, and charging a card are not naturally safe under repetition. Calling all of them “sink writes” erases the important distinction.

Operational ambiguity is unavoidable. A timeout proves the caller did not receive a response; it does not prove the destination did not act. A process can die after the remote commit and before recording the receipt. Two workers can overlap during failover. A checkpoint can succeed while an unrelated API call is still in flight. Good design makes these uncertainties explicit rather than betting on rare timing.

Safety also includes correction. A wrong historical amount should usually produce a versioned replacement, retraction, or adjustment, not reuse a key with different semantics and not erase the audit trail. Some effects cannot be reversed; others require a refund, cancellation, or notice governed as a new operation. Reprocessing policy is therefore a business and security policy as much as a storage protocol.

## Prerequisites and Retrieval

Review partitioned consumption in [LSDS-042](042-partitioned-consumption.md), stateful operators in [LSDS-043](043-stateful-operators.md), checkpoint barriers in [LSDS-047](047-checkpoint-barriers.md), state snapshots and recovery in [LSDS-048](048-state-snapshots-and-recovery.md), and backpressure in [LSDS-049](049-backpressure-across-operators.md).

You should understand replayable logs, offsets, checkpoints, transactions, unique constraints, conditional writes, canonical serialization, cryptographic hashes, retry/timeouts, two-phase commit, change-data capture, versioned datasets, authorization, and reconciliation.

## Learning Objectives

After this module, you should be able to:

1. distinguish physical processing, result commitment, and logical external effects;
2. define stable input, computation, effect, attempt, and checkpoint identities;
3. design an atomic idempotency ledger with payload-conflict detection and durable outcomes;
4. compute a defensible deduplication-retention horizon from replay and recovery obligations;
5. connect checkpoint epochs to transactional sinks and fence obsolete writers;
6. use transactional outbox/inbox, conditional upsert, immutable objects, or destination-native idempotency appropriately;
7. handle ambiguous remote outcomes without blind duplicate execution;
8. isolate shadow replay, compare materializations, reconcile effects, and perform controlled cutover;
9. model corrections and compensation as explicit new facts or effects; and
10. validate effect safety with crash-point, concurrency, expiry, conflict, replay, and reconciliation tests.

## Core Exposition

### Define the logical effect

Start with a business sentence: “capture at most one payment for order 7 at approved amount 100,” or “publish exactly one current balance for account 9 at calculation version 4.” The protected unit is not a source record or function invocation. One input can cause several effects, and several inputs can contribute to one effect.

State whether the contract is creation, replacement, transition, append, notification, or command. Define its uniqueness domain: tenant, account, order, effect type, and semantic version. Also define whether “once” means one accepted request, one durable state transition, one externally visible result, or one human-visible action.

### Separate identities

Use distinct names for distinct purposes. An input event ID identifies a fact. A source position locates a delivery in a particular log generation and partition. A computation version identifies code/schema/rules. An effect key identifies a business action. An attempt ID identifies one physical execution. A checkpoint/transaction epoch identifies one coordinated commit generation.

A useful effect key can be a tuple such as `(tenant, order, "capture", authorization_version)`. It remains stable when the record moves partitions or the job restarts. A random UUID generated inside the retry loop is an attempt ID and defeats deduplication. An offset can be useful transport provenance but changes after republishing and may collide across topics or generations.

### Canonicalize intent deterministically

Bind the key to a canonical fingerprint of the intended operation. Canonicalization fixes field names, types, ordering, encodings, currency units, normalization, default values, and semantic version. Hash the canonical bytes, not an unstable map rendering.

The fingerprint prevents a dangerous ambiguity: the same key arriving with amount 100 and later amount 120. Silently returning the first result hides corruption; silently applying the second violates once-only semantics. Treat this as a conflict requiring a new authorized correction key or investigation.

Nondeterministic values such as current time, random IDs, environment defaults, and mutable reference data must be captured as input or derived once and stored. A replay should reconstruct the same intent or explicitly declare a new computation/effect version.

### Make the decision atomic at the effect boundary

The core operation is compare-and-record at the destination that owns the effect. If the effect and ledger are in one transactional database, a unique key plus transaction can atomically insert the ledger and mutate domain state. If the destination exposes native idempotency, it must durably bind key to request and outcome for the required horizon.

“Check then act” in two independent operations is unsafe: two workers can both see absence and both act. “Act then record” is unsafe if the process dies in between. “Record then act” is unsafe if acting fails permanently unless the record represents a durable intent that a relay can finish. Atomicity may mean direct transaction, destination-native protocol, transactional intent, or a coordinated distributed transaction whose participants all support it.

### Persist the original outcome

Deduplication is more than dropping repeats. Store status, canonical fingerprint, destination identifier, receipt/result, timestamps, authorization context reference, and epoch. A retry with the same key and fingerprint should receive the recorded outcome, even when the first caller never saw it.

Represent in-progress and unknown states carefully. A permanent “in progress” after a crashed owner needs lease/epoch recovery. An unknown remote outcome should trigger lookup or reconciliation by key, not immediate re-execution. Responses may contain secrets or personal data, so retain only what recovery/audit requires and protect it accordingly.

### Size the deduplication horizon

Let $H_r$ be maximum source replay age, $H_b$ maximum backfill age, $H_o$ maximum outage/recovery age, $H_c$ correction workflow age, and $H_n$ network/client retry age. A conservative retention condition is

$$H_D \ge \max(H_r,H_b,H_o,H_c,H_n)+M$$

for operational margin $M$. Use the largest authorized route by which the same logical effect can return, not the usual retry delay. If regulation or storage policy requires earlier deletion, preserve a non-sensitive durable tombstone or choose a different effect protocol.

Expiry changes semantics. Once a key is forgotten, the destination can accept the same logical action again. Tombstone compaction, backup restoration, regional failover, tenant migration, and clock error all belong in the retention analysis.

### Fence obsolete writers

During restart or rescale, an old worker may resume after a new owner has taken over. Give ownership a monotonic epoch or fencing token. The destination accepts a write only when its token is not older than the recorded generation under the protocol's comparison rule.

Leases without fencing are insufficient: a paused process may wake after its lease expires and still possess credentials. Sequence numbers must be scoped to the resource and stored durably at the enforcement point. Split-brain tests should prove that an older generation cannot prepare, commit, overwrite, or extend work.

### Coordinate transactional sinks with checkpoints

A checkpoint-aware sink commonly writes into a transaction per checkpoint epoch. At the barrier it flushes and prepares committable metadata. Only after global checkpoint completion does the coordinator commit that epoch. Failure aborts or leaves prepared transactions for deterministic recovery.

This is a form of two-phase coordination. It requires unique transaction identity, durable prepared state, idempotent commit/abort, timeout sizing longer than checkpoint plus recovery, and fencing of prior job instances. Downstream readers may need committed-only isolation. Visibility is delayed until commit.

Do not generalize the guarantee beyond participating resources. A runtime checkpoint can make managed state exactly once while an HTTP call in user code runs twice. A Kafka transaction coordinates supported topic writes and consumer offsets; it does not automatically enlist a payment API or arbitrary database.

### Use transactional outbox and inbox

When local state and message publication cannot be atomically written to separate systems, store the domain change and an outbox row in one database transaction. The row contains a stable event/effect ID, aggregate identity, order/version, type, canonical payload, and authorization provenance. A relay or change-data-capture connector publishes committed rows.

The relay is normally at least once: it may publish and fail before marking success. Therefore the event ID remains stable, and the destination uses an inbox or native idempotency to atomically record receipt with its local state change. The outbox closes the lost-message dual-write window; it does not by itself prevent downstream duplicates.

Order must be defined per aggregate or key. Global timestamp order is usually neither reliable nor necessary. Monitor unpublished age, relay attempts, duplicate delivery, poison rows, schema compatibility, retention, and downstream acknowledgement.

### Use conditional upserts for replaceable state

For a projection, a stable primary key and version can make repeats converge. Insert version 12 if absent; update only when incoming version is greater than the stored version; treat equal version/same fingerprint as a replay and equal version/different fingerprint as conflict. Return the stored version/outcome.

`ON CONFLICT DO NOTHING` merely suppresses an insertion error unless the application verifies what conflicted. Blind last-write-wins using worker wall clocks allows a late replay to overwrite a newer result. Prefer source sequence, logical revision, or computation epoch with explicit ordering semantics.

Commutative operations can also help: set union or max under a valid domain order tolerates duplicates differently from increment. Prove the algebra and correction behavior rather than labeling an update “idempotent” because it usually converges.

### Write immutable files and objects safely

Object stores and file sinks can write attempt output to unique staging names, then publish an immutable manifest for the successful checkpoint/materialization. Readers consume only objects named by the committed manifest. Orphan attempt files can be garbage-collected after their recovery horizon.

Never let multiple attempts overwrite a shared final object without conditional generation checks. Include partition, logical interval, schema/calculation version, content digest, and checkpoint/materialization ID in metadata. A manifest swap can provide a small atomic publication point even when the data set contains many objects.

### Treat append logs as another boundary

Appending the same event twice creates two physical records even if their payloads match. A broker's idempotent producer may suppress retry duplicates within its defined producer/session sequence protocol. Transactions can coordinate multiple topic writes and offsets within the broker's supported scope.

Long-term replay safety still needs stable business IDs because a new producer, republished input, retention restore, or separate pipeline may legitimately append again. Downstream consumers should define whether they deduplicate by event ID, aggregate version, effect key, or materialized state. Compaction by key is not a universal substitute: duplicates may be observed before compaction, and history/audit requirements differ.

### Resolve ambiguous API outcomes

Assume a request can commit remotely while its response is lost. Send a destination-recognized idempotency key and identical canonical parameters on retry. Persist the returned response. If an operation times out, query status by that key or destination object ID before deciding to retry, compensate, or escalate.

HTTP method idempotence describes the intended server effect of repeated identical requests; it does not make arbitrary application actions safe. A nominally idempotent request can still create per-request logs, and a `POST` can be safely retryable only through an application protocol such as a durable key.

Key scope and retention are part of an external API's contract. If a provider forgets keys after 24 hours but your disaster replay reaches 30 days, the provider's native window is insufficient. Keep local effect evidence, prevent live replay, reconcile, or negotiate another protocol.

### Treat compensation as a new effect

A refund does not erase a charge; a cancellation does not make the booking never have existed. Compensation has its own stable identity, authorization, payload, retry, outcome, and audit trail. It may fail or become impossible after a point of no return.

Record enough information during forward execution to choose and execute compensation. Account for concurrent changes: restoring an old value may overwrite legitimate later work. Domain policy decides whether to compensate, continue forward, choose an alternative, or request human judgment.

### Isolate replay from production effects

The safest default is a shadow replay. Read a declared source range and snapshot/reference-data version; write a new materialization namespace; route external-effect requests to a disabled, sandbox, or capture-only adapter; and record what would have happened. Do not share live consumer groups, output tables, object prefixes, idempotency namespaces, or credentials accidentally.

Make effect capability explicit rather than relying on a forgotten boolean deep in code. Separate credentials and network policy can prevent shadow jobs from reaching production destinations. Bind a run manifest to code, configuration, source offsets, schemas, reference snapshots, owner, approval, and expected output/effect counts.

### Compare, reconcile, and cut over

Compare shadow and current materializations by keyed counts, digests, invariants, business totals, distribution shifts, sampled rows, and known corrections. Classify differences as intended code changes, late/corrected input, nondeterminism, source drift, or defects.

Reconcile effect intents separately. For each key, identify existing destination outcome, proposed identical repeat, legitimate new version, conflict, missing effect, compensation, and unknown. High-impact effects require explicit authorization rather than automatic emission from a historical replay.

Cut over with an atomic pointer, view, alias, manifest, or version selection where possible. Quiesce or dual-process a precisely bounded tail, record the handoff watermark/offset, and retain rollback material. Rollback changes which materialization is read; it cannot undo already emitted real-world effects.

### Handle corrections explicitly

Correct a replaceable projection with a higher logical version or publish a new materialization. Correct an append-only fact with a retraction and replacement linked to the original. Correct money with an authorized adjustment, refund, or supplemental charge. Never mutate a key's payload merely to force a different outcome.

Notifications deserve their own policy. A replay may rebuild delivery history without resending messages. If a correction must notify a person, create a new communication effect with template/content version, audience, purpose, approval, and suppression rules.

### Secure the replay path

An idempotency key is not authorization. Authenticate the caller and authorize tenant, effect type, amount, environment, replay range, and cutover. Scope keys by tenant/account so one principal cannot collide with another's action. Bind fingerprint and authorization context to the ledger.

Treat guessed/replayed keys, payload conflicts, mass replay, and old privileged events as security signals. Rotate credentials without destroying the ability to verify historical authority. Minimize personal data in ledgers and logs; apply encryption, access control, deletion policy, and auditable exceptions.

Use separate production-effect credentials only for a tightly controlled reconciliation emitter. A general backfill worker usually needs read access and isolated write access, not the ability to charge customers or send messages.

### Observe logical and physical work

Measure physical attempts, unique effect keys, first applications, same-payload replays, payload conflicts, rejected stale epochs, in-progress age, ambiguous outcomes, query resolutions, compensation status, and manual interventions. A falling duplicate rate can be bad if dedup records expired unnoticed.

For transactional sinks observe prepared/committed/aborted transaction counts and age, checkpoint-to-visibility latency, transaction timeouts, fencing failures, and recovery resolution. For outbox/inbox observe oldest unpublished/unused age, relay lag, delivery attempts, inbox duplicate hits, poison messages, and retention.

Every replay needs scope telemetry: source range, code/materialization version, isolated destination, expected/actual records, would-be effects, conflicts, differences, approvals, cutover point, and reconciliation closure. Counts should satisfy a conservation relation such as

$$N_{attempt}=N_{first}+N_{replay}+N_{conflict}+N_{rejected}+N_{pending}$$

under mutually exclusive terminal definitions for the measured interval.

### Validate crash windows and lifecycle

Test crashes before acceptance, after ledger insert, after effect but before response, after prepare, during commit, after commit before checkpoint acknowledgement, during restore, and during concurrent takeover. Inject duplicate and reordered delivery, long pause beyond leases, ledger unavailability, destination timeout, and partial batch success.

Test same key/same payload, same key/different payload, accidental key collision, stale epoch, clock skew, dedup expiry, restored old backup, cross-region failover, tenant collision, schema change, correction, and unauthorized replay. Run a replay older than normal operations in an isolated environment.

Finally reconcile the destination, not merely pipeline logs. Logs show attempts and can be duplicated or lost. Evidence is the durable keyed outcome plus destination business state and an audit explaining every exception.

## Definitions and Notation

Let $x$ denote an input fact, $i(x)$ its stable event identity, $v$ a computation/materialization version, $k=g(x,v,p)$ a logical-effect key under business policy $p$, and $a$ a physical attempt identity. Let $h=H(C(q))$ be a fingerprint of canonicalized effect payload $q$, where $C$ is deterministic canonicalization and $H$ is a collision-resistant hash used with appropriate domain separation.

Let $e$ be the ownership/checkpoint epoch, and let the destination ledger entry be $D[k]=(h,o,s,e)$ with outcome $o$ and state $s$ such as prepared, committed, compensated, rejected, or unknown. Let $H_D$ be deduplication retention and $H_R$ the maximum authorized recurrence horizon of the same logical key.

The key safety condition is $H_D\ge H_R$ plus operational margin. A logical once-only effect means all accepted attempts for the same $(k,h)$ converge to one committed business outcome. It does not mean user code runs once, one network packet is sent, or one log line exists.

An operation is **naturally idempotent** only under specified state and comparison semantics. A protocol is **deduplicating** when it recognizes stable keys. A sink is **transactional with the runtime** only when prepare/commit/recovery participate in the runtime's checkpoint protocol. These properties are related but not interchangeable.

## Mechanisms, Invariants, or Proof Structure

Use this review sequence:

1. Enumerate every effect and classify it as replaceable state, append, command, notification, allocation, or irreversible action.
2. Define the logical uniqueness domain and distinguish event, position, computation, effect, attempt, transaction, and destination IDs.
3. Define canonical payload bytes and same-key/different-payload conflict behavior.
4. Locate the atomic boundary joining first-use detection with effect or durable intent.
5. Prove repeat attempts return the same stored outcome and cannot manufacture a second destination object.
6. Establish retention from the maximum replay/outage/backfill/correction horizon and test expiry/restore.
7. Prove stale workers are fenced and concurrent attempts serialize at the destination.
8. For checkpoint sinks, trace prepare, global completion, commit, abort, timeout, visibility, and recovery.
9. For dual writes, trace transactional outbox, at-least-once relay, downstream inbox/native idempotency, ordering, and poison handling.
10. Define shadow isolation, difference classification, effect reconciliation, approval, cutover, rollback, and evidence.
11. Model correction and compensation as new versioned facts/effects with independent failure handling.
12. Test every crash boundary and reconcile durable destination state against intended logical effects.

Proof sketch: suppose all attempts for effect key $k$ reach a linearizable atomic operation at the destination. Exactly one attempt can observe $k$ absent and transition it to a committed or durably finishable intent bound to $h$. Every concurrent or later attempt observes the entry. Same-$h$ attempts return $o$; different-$h$ attempts reject. Durable retention prevents later replay from recreating absence, and fencing prevents an obsolete owner from bypassing the accepted epoch. Therefore multiple physical executions yield at most one committed logical effect for $(k,h)$.

The proof fails if checking and effect are separate, if the destination cannot recognize $k$, if a key changes across replay, if a key expires, if conflicting payloads are accepted, if an old writer can overwrite, or if an effect escapes to an unenlisted system. At-least-once input plus exactly-once managed state is not sufficient.

## Alternatives and Trade-Offs

- **Destination-native idempotency** handles ambiguous retries close to the effect and can return the original result, but key scope, retention, payload comparison, and provider availability constrain it.
- **Checkpoint-coordinated transactions** give strong end-to-end visibility for participating sinks, but add latency, prepared state, timeouts, coordinator load, and operational recovery complexity.
- **Transactional outbox plus inbox** avoids cross-system dual-write loss with common databases and brokers, but remains eventually consistent and requires duplicate handling, ordering, relay operations, and retention.
- **Versioned conditional upsert** is simple and efficient for replaceable projections, but does not naturally model increments, notifications, or irreversible actions.
- **Immutable objects plus committed manifest** make retries cheap and preserve auditability, but consume storage and require orphan cleanup and reader indirection.
- **Commutative/monotone state** tolerates some duplication and reordering, but only where the domain operation has the proven algebra and corrections remain expressible.
- **Distributed two-phase commit** can coordinate multiple capable resources, but blocking, participant availability, timeout/recovery, and limited ecosystem support often make narrower boundaries preferable.
- **Shadow replay and versioned cutover** minimize production risk and support comparison, but require duplicate storage/compute and a plan for the live tail.
- **Compensation** addresses effects that already happened, but is a fallible domain workflow and may not restore the original state.
- **At-least-once plus reconciliation** can be appropriate when duplicates are tolerable or repairable, but the accepted exposure, detection delay, and repair authority must be explicit.

## Failure Modes and Misconceptions

- “The framework is exactly once, so the API call is exactly once.” Managed state and external effects have different commit boundaries.
- “The function ran once.” Runtimes can retry, speculate, or execute concurrently even when committed results are deduplicated.
- “The event ID is always the effect ID.” One event may create many effects; one effect may aggregate many events.
- “An offset is a permanent ID.” Repartitioning, republishing, new topics, restores, and source replacement change its namespace.
- “A random key makes retries safe.” Only reuse of the same stable logical key makes attempts correlate.
- “Check then insert is sufficient.” Concurrent workers race unless the decision is atomic.
- “Insert conflict means identical intent.” The existing payload and outcome must be verified.
- “Twenty-four-hour key retention covers us.” It fails a replay or outage older than twenty-four hours.
- “A timeout means nothing happened.” The destination may have committed and lost the response.
- “Retrying with a new amount under the old key is a correction.” It is a semantic conflict; create a versioned correction effect.
- “Last writer wins.” A delayed replay can overwrite newer truth, especially with unsynchronized wall clocks.
- “Outbox gives exactly once everywhere.” It prevents local state/message loss; relays and consumers still handle duplicates.
- “Broker idempotence covers historical replay.” Producer-session retry suppression is not permanent business deduplication.
- “Compensation rolls back history.” It creates another visible and fallible business event.
- “Disabling an effects flag is isolation.” Credentials, routes, shared namespaces, and escape paths must enforce isolation.
- “Logs prove correctness.” Logs describe attempts; reconciliation must examine durable keyed outcomes and destination state.
- “Deduplication means drop repeats.” Clients often need the original receipt/status, and conflicts must be surfaced.
- “Exactly once is universal.” Always state identity, effect, source, state, sink, visibility, retention, and failure scope.

## Worked Examples

### Example 1

A job reads event `order-7-approved` from one partition and calls a card API. It crashes after the provider captures 100 but before checkpoint completion. The restored job rereads the event. With key `(merchant, order-7, capture, auth-v1)` and fingerprint of currency/amount/account, the provider returns the stored receipt. A fresh UUID would double-charge.

### Example 2

A projection receives customer revision 12 twice. A conditional transaction inserts or updates key `customer-9` only when incoming revision exceeds stored revision. Equal revision with equal fingerprint returns current state; equal revision with different fingerprint raises corruption. Revision 11 arriving late cannot overwrite revision 12.

### Example 3

The normal retry horizon is one day, but source retention is 14 days, disaster restore can use a 30-day backup, and correction runs can reach 90 days. With seven days of margin, the deduplication evidence must cover at least $\max(1,14,30,90)+7=97$ days. A provider's 24-hour native window cannot carry this contract alone.

### Example 4

A checkpoint sink prepares transactions `job-A/epoch-81` and `job-A/epoch-82`. Global checkpoint 81 completes, so the coordinator commits 81 idempotently. The job fails while 82 is prepared. Recovery consults completed-checkpoint metadata, aborts or leaves 82 invisible according to the protocol, and fences the old job generation.

### Example 5

An order service changes status and must publish `OrderApproved`. Writing the database then publishing loses the message on a crash; publishing then committing can announce a rolled-back order. One local transaction writes both order revision and outbox row. The relay may publish twice, so the inventory consumer atomically records the event ID in its inbox with reservation state.

### Example 6

A file sink writes attempt objects under an isolated prefix and produces a manifest listing content digests for checkpoint 55. Readers switch only to the committed manifest. A failed attempt's files are unreachable and later garbage-collected after the recovery horizon; they never become visible by filename convention alone.

### Example 7

A request to provision a credential times out. Blind retry could allocate twice. The client queries the provider by idempotency key; if committed, it stores the original credential reference; if definitively absent, it retries the identical request; if unknown persists, it quarantines for controlled reconciliation rather than changing keys.

### Example 8

A corrected fare cannot reuse `ticket-3/charge-v1` with a new amount. The system records a separate adjustment or refund key linked to the original charge. Both actions remain auditable, and retry of either action uses its own stable payload-bound key.

### Example 9

A 60-day replay writes `balance-calculation-v7-shadow`, while network policy blocks payment and notification endpoints. Comparison finds 30 intended projection differences, two nondeterministic mismatches, and zero authorized new charges. Engineers fix nondeterminism, rerun, reconcile by key, then atomically change the serving alias. No old notification is resent.

### Example 10

This executable fixture separates four attempts from two first applications. It models same-payload replay and payload conflict; it does not model durable storage, atomic transactions, concurrency, fencing, authorization, hashing, expiry, remote ambiguity, or compensation.

<!-- bijux-verify: {"id":"logical-effect-ledger","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"applied=('charge:order-7', 'charge:order-8')\nreplayed=('charge:order-7',)\nconflicts=('charge:order-7',)\ntotal=350\nreceipts=('receipt-1', 'receipt-2')\n","stderr":""}} -->
```python
requests = (
    ("charge:order-7", "amount=100", 100),
    ("charge:order-7", "amount=100", 100),
    ("charge:order-8", "amount=250", 250),
    ("charge:order-7", "amount=120", 120),
)

ledger = {}
applied = []
replayed = []
conflicts = []

for key, fingerprint, amount in requests:
    previous = ledger.get(key)
    if previous is None:
        receipt = "receipt-" + str(len(applied) + 1)
        ledger[key] = (fingerprint, amount, receipt)
        applied.append(key)
    elif previous[0] == fingerprint and previous[1] == amount:
        replayed.append(key)
    else:
        conflicts.append(key)

total = sum(entry[1] for entry in ledger.values())
receipts = tuple(entry[2] for entry in ledger.values())

print("applied=" + repr(tuple(applied)))
print("replayed=" + repr(tuple(replayed)))
print("conflicts=" + repr(tuple(conflicts)))
print("total=" + str(total))
print("receipts=" + repr(receipts))
```

The expected output reports applied keys `('charge:order-7', 'charge:order-8')`, replayed key `('charge:order-7',)`, conflicting key `('charge:order-7',)`, total `350`, and receipts `('receipt-1', 'receipt-2')`.

## Cross-Program Connections

- **Distributed systems:** idempotency, linearizable compare-and-record, consensus-backed transactions, leases, fencing, and ambiguous failure define the safety boundary.
- **Database engineering:** unique constraints, transactions, MVCC, conditional updates, outbox tables, CDC, and versioned corrections implement durable effect protocols.
- **API and service engineering:** request idempotency, status lookup, payload conflict, receipts, compensation, authentication, and rate limits shape remote effect contracts.
- **Platform engineering:** separate identities/credentials/namespaces, checkpoint coordinators, replay tooling, policy gates, audit trails, and cutover mechanisms make safe reprocessing operable.
- **Security engineering:** effect keys do not replace authorization; tenant scoping, anti-replay policy, least privilege, evidence retention, and privacy controls remain mandatory.
- **Reliability engineering:** crash injection, recovery time, unknown-outcome queues, reconciliation, alerts, and runbooks turn protocol assumptions into tested behavior.
- **Data architecture:** immutable facts, retractions, materialization versions, lineage, source snapshots, and semantic revisions determine what replay means.
- **Formal methods:** safety can be stated as at most one committed outcome per payload-bound key, while liveness asks whether a valid pending effect eventually resolves.

## References

1. Apache Kafka. [Kafka Design: Message Delivery Semantics and Transactions.](https://kafka.apache.org/42/design/design/) Current official explanation of idempotent production, transactions, offsets, committed reads, external-system limits, and delivery scopes.
2. Apache Kafka. [Producer Configurations.](https://kafka.apache.org/42/configuration/producer-configs/) Current official `enable.idempotence`, `transactional.id`, ordering, retry, delivery-timeout, and transaction configuration contract.
3. Apache Flink. [Fault Tolerance.](https://nightlies.apache.org/flink/flink-docs-stable/docs/learn-flink/fault_tolerance/) Current distinction between repeated execution, exactly-once managed state, and end-to-end transactional or idempotent sinks.
4. Apache Flink. [Data Sinks.](https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/sinks/) Current sink writer, committable, committer, writer-state, and two-phase-commit interfaces.
5. Apache Flink. [Kafka DataStream Connector.](https://nightlies.apache.org/flink/flink-docs-stable/docs/connectors/datastream/kafka/) Current delivery modes, checkpoint coordination, committed visibility, transaction identity, and timeout considerations.
6. Google Cloud. [Exactly-once in Dataflow.](https://cloud.google.com/dataflow/docs/concepts/exactly-once) Current explanation of at-least-once execution, exactly-once committed pipeline results, deduplication, nondeterminism, and external side-effect limits.
7. Akidau et al. [MillWheel: Fault-Tolerant Stream Processing at Internet Scale.](https://research.google/pubs/millwheel-fault-tolerant-stream-processing-at-internet-scale/) Primary paper on persistent state, record identity, deduplication, low watermarks, and fault-tolerant stream processing.
8. Internet Engineering Task Force. [RFC 9110: HTTP Semantics, Section 9.2.2.](https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2.2) Standard definition and retry implications of HTTP idempotent methods.
9. Stripe. [Idempotent Requests.](https://docs.stripe.com/api/idempotent_requests) Current destination-native key, stored-response, parameter comparison, conflict, and pruning behavior for API requests.
10. PostgreSQL Global Development Group. [INSERT.](https://www.postgresql.org/docs/current/sql-insert.html) Current unique-conflict, conditional update, privilege, and returned-outcome behavior for atomic upsert designs.
11. Debezium. [Outbox Event Router.](https://debezium.io/documentation/reference/stable/transformations/outbox-event-router.html) Current official outbox event structure, routing, identifiers, aggregate keys, schema, and CDC relay configuration.
12. Amazon Web Services. [Transactional Outbox Pattern.](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html) Current dual-write analysis, local transaction, relay/CDC, duplicate-consumer, and ordering considerations.
13. Garcia-Molina and Salem. [Sagas.](https://www.cs.princeton.edu/techreports/1987/070.pdf) Primary paper defining long-lived transactions as component transactions with compensating transactions.

## Exercises

### Exercise 1

A payment replay can revisit 180-day-old input. Normal retries last 2 days, outage recovery 21 days, corrections 365 days, and policy requires 30 days of margin. Compute the minimum ledger horizon and explain what happens if a provider retains keys for only 24 hours.

### Exercise 2

Design identities for a shipment event that updates a customer projection, reserves inventory, and sends a first-shipment notification. Distinguish event, source position, computation version, effect keys, attempt IDs, and checkpoint epoch.

### Exercise 3

Enumerate the crash windows in a naive “call remote API, then insert dedup row” design. Replace it using destination-native idempotency or transactional intent and explain how ambiguous responses resolve.

### Exercise 4

A shadow replay reports 1,000,000 attempts, 990,000 first applications, 8,000 same-payload replays, 500 conflicts, and 1,000 pending outcomes. Does the conservation relation close? What should happen before cutover?

### Exercise 5

Design an end-to-end reprocessing review for a checkpointed stream that writes a database projection, publishes broker events, sends emails, and can issue refunds. Include atomicity, retention, fencing, isolation, correction, security, observability, testing, reconciliation, and cutover.

## Answers to the Exercises

### Answer 1

The recurrence horizon is $\max(180,2,21,365)=365$ days. Adding 30 days gives at least 395 days of durable deduplication evidence. A 24-hour provider window cannot safely receive the historical replay directly: after pruning it may treat an old key as new. Suppress live effects, maintain a longer-lived local ledger/tombstone, query and reconcile destination state, or use a newly authorized correction protocol.

### Answer 2

The shipment fact gets a globally scoped event ID and transport provenance such as topic/partition/offset. The projection names its calculation/schema version. Inventory might use `(tenant, order, line, reserve, fulfillment_version)`; notification might use `(tenant, order, first-shipment-notice, audience, template_version)`. Each process invocation gets a fresh attempt ID, while all retries preserve the relevant effect key and canonical fingerprint. The runtime assigns a checkpoint/transaction epoch for coordinated sink commit. None of event ID, offset, attempt, or epoch is automatically interchangeable with either business-effect key.

### Answer 3

Crashes can occur before the call, while it executes, after remote commit before response, after response before the row, and during row commit. Concurrent workers also race on absence. Prefer a destination that atomically binds the stable key and fingerprint to the effect/outcome; a repeat queries or resubmits the same key and receives the recorded result. Otherwise atomically store a durable effect intent locally, relay it at least once, and require a destination inbox/idempotency boundary. A timeout enters unknown state and is queried/reconciled by key; it is not retried with a new key.

### Answer 4

The classified count is $990{,}000+8{,}000+500+1{,}000=999{,}500$, leaving 500 attempts unexplained. Cutover must stop until definitions are confirmed, missing attempts are classified, conflicts are resolved or explicitly rejected, pending outcomes reach a safe terminal state, and keyed destination reconciliation matches the authorized effect set. Aggregate equality alone would still require invariant and sampled/keyed checks.

### Answer 5

Give each projection revision, published event, email, and refund a stable payload-bound effect key; preserve separate event/attempt/epoch IDs. Use a conditional versioned transaction for the projection, a transactional outbox for broker publication with inbox/dedup downstream, suppression/capture-only routing for historical emails, and independently authorized idempotent refund commands. Size ledger/inbox/outbox retention for the longest replay/correction horizon, fence job generations, and trace prepare/commit/recovery for checkpoint-participating sinks. Run shadow replay in separate tables/topics/object prefixes with credentials unable to contact production email/refund endpoints. Compare keyed projections and would-be effects, express corrections as higher versions/retractions/adjustments, and require tenant-scoped authorization and audited approval. Observe attempts, first/replay/conflict/unknown outcomes, prepared transactions, outbox/inbox lag, stale-epoch rejection, suppression, and reconciliation. Inject every crash boundary, duplicate/concurrent delivery, expiry, backup restore, failover, schema change, unauthorized replay, and compensation failure. Resolve differences and unknowns before an atomic materialization cutover; emit only explicitly approved new corrective effects and retain rollback plus reconciliation evidence.
