---
module_id: DE-056
program: Data Engineering
level: 2
module_number: 56
title: Exactly-Once Effects
status: complete
last_verified: 2026-09-03
---

# Exactly-Once Effects

## One-Page Review

### Governing question

How can a replayable streaming pipeline make each accepted logical occurrence change a named business boundary once despite duplicate delivery, uncertain responses, crashes, reassignment, concurrent attempts, and recovery—and what evidence proves the scope without claiming that handler code ran once?

### Essential definitions

- An **effect** is a durable state transition or externally observable outcome, such as a ledger posting, row version, output record, file generation, notification request, or published view.
- An **effect scope** names the occurrence identity, operation, target boundary, tenant/domain, interval, and failure model covered by the once-only claim.
- An **idempotency key** identifies one intended operation across retries. It is not merely a unique delivery-attempt ID.
- A **request fingerprint** canonically binds an idempotency key to the intended operation, target, and parameters so key reuse with different intent is rejected.
- **Mathematical idempotence** means applying an operation twice has the same result as applying it once: $f(f(s))=f(s)$. Many business operations, such as increment or send-email, are not naturally idempotent.
- A **deduplication receipt** durably records that a named effect identity was accepted, including its fingerprint, result, status, and relevant version.
- An **inbox** is a receiver-owned ledger of consumed occurrence IDs and outcomes, commonly stored atomically with local domain changes.
- An **outbox** stores a domain change and an event-to-publish in one source transaction; a relay may publish the outbox row more than once, so the event keeps a stable ID.
- A **linearization point** is the single authoritative instant at which an operation takes effect in the abstract contract, even if requests and responses span time.
- A **conditional mutation** changes state only when a version, token, absence condition, or other precondition holds.
- A **fencing token** is a monotonically ordered authority value that lets a target reject effects from stale owners.
- A **transactional consume-transform-produce boundary** atomically commits input progress with output records and managed state inside one supported transaction domain.
- A **prepare/commit protocol** reserves or stages effects before a later decision makes them visible; recovery must resolve every prepared transaction.
- **Exactly-once effect** means one accepted logical occurrence produces one named durable outcome under the declared scope, even though delivery and handler execution may repeat.
- **Reconciliation** independently compares authoritative obligations with receipts and visible results, then repairs or escalates discrepancies.

### Central model, mechanism, or theorem

For occurrence $x$, canonical request fingerprint $h(x)$, and effect boundary $B$, let $R_B[x]$ be a durable receipt and $E_B[x]$ the accepted effect. An atomic apply-once protocol enforces:

1. a unique key on `(tenant, operation, occurrence_id)`;
2. first use of the key atomically writes $E_B[x]$ and $R_B[x]$;
3. a retry with the same fingerprint returns the recorded outcome without reapplying the effect;
4. the same key with a different fingerprint is rejected; and
5. input progress advances only in the same transaction or after the receipt is authoritatively queryable.

The safety invariant is

$$
R_B[x]\iff E_B[x],\qquad \operatorname{count}(E_B[x])\le1.
$$

Liveness adds that every valid required $x$ eventually reaches one accepted outcome:

$$
\operatorname{count}(E_B[x])=1.
$$

The biconditional is achievable directly only when receipt and effect share an atomic boundary, or when a recoverable protocol makes intermediate states convergent. A receipt written before an unrelated effect can suppress unfinished work; an effect written before an unrelated receipt can repeat.

### Critical invariants

- The once-only claim names the exact effect boundary, occurrence namespace/generation, operation, tenant/target, validity rules, interval, and covered failures.
- Every retry of one intent reuses the same idempotency key; distinct intent gets a new key; the server compares canonical fingerprints.
- Receipt and local effect are committed atomically, or an explicit recoverable state machine resolves incomplete reservation, execution, and publication states.
- Database uniqueness is enforced by the authoritative store under concurrency, not by a read-then-write check in application memory.
- Duplicate paths return or reconstruct a semantically equivalent prior result without repeating non-idempotent work.
- Source progress never advances beyond an accepted effect/receipt boundary and stale consumer generations cannot commit effects or progress.
- Outbox row and source domain change share one transaction; relay retries preserve the same event ID; downstream consumers still handle duplicate publication.
- Transactional output is hidden until commit, aborted work is not treated as visible, and readers use the required committed-read mode.
- Prepared transactions, commit handles, epochs, timeouts, and recovery ownership are durable and operationally resolvable.
- Deduplication retention exceeds every producer retry, broker replay, restoration, backfill, regional recovery, and operator-delay horizon—or the guarantee is explicitly time-bounded.
- Keys are scoped to avoid tenant/operation collisions and protected against guessing, tampering, unbounded cardinality, and sensitive-data leakage.
- Multi-effect workflows identify which effects are atomic, compensatable, conditional, or reconciled; one receipt cannot make unrelated systems atomic.
- Deployments preserve key, fingerprint, receipt, result, and state compatibility across code/schema/config generations.
- Fault tests inject failure before and after the effect linearization point and prove one visible result over a complete finite input cut.

### Common failures

Common failures include generating a fresh idempotency key on every retry; using the broker offset as a global business identity; performing `SELECT` then `INSERT` without a unique constraint; recording “seen” before the effect in a different transaction; applying the effect before an unrelated receipt; reusing a key for changed parameters; evicting receipts before late retries; treating `PUT` or upsert as idempotent when values depend on current state; confusing idempotent Kafka production with an external database guarantee; assuming an outbox prevents duplicate relay; exposing prepared data before commit; letting two owners share a transactional ID or fencing token; calling compensation rollback; counting handler invocations instead of effects; and claiming exactly once without reconciliation.

### Compact example

A balance projection receives occurrences `e-100:+7`, `e-101:-2`, and `e-102:+5`, each more than once. In one database transaction it inserts `(account, event_id, payload_digest, result)` under a unique constraint, applies the balance change only for a new row, stores next source progress, and commits. Six same-intent deliveries yield balance 110 from 100, not the naive 120. A later `e-101:-9` conflicts with the recorded fingerprint and is quarantined rather than silently treated as the old retry. This proves only the modeled database boundary, not email, payment-network, or cross-region effects.

### Connections

[DE-044](044-retries-timeouts-and-idempotency.md) established retry and idempotency foundations. [DE-051](051-streams-logs-and-unbounded-data.md) defined logical occurrence identity; [DE-052](052-topics-partitions-and-offsets.md) supplied source coordinates; [DE-053](053-producer-keys-and-ordering.md) covered producer sessions and duplicates; [DE-054](054-consumer-groups.md) supplied ownership epochs; and [DE-055](055-delivery-semantics-in-streaming-pipelines.md) exposed replay/omission crash windows. DE-057 through DE-060 will add time, windows, state, and late/duplicate/out-of-order semantics without weakening the effect boundary.

## Governing Question

“Exactly once” is valuable only when it names what occurs once. Code execution is usually the wrong object: a worker may deserialize, validate, compute, and call a sink repeatedly during recovery. What matters is whether one logical occurrence creates one ledger posting, one current row transition, one output record in a committed transaction, or one accepted external request.

The core obstacle is the dual-write gap. After applying an effect, a process must record progress so replay does not repeat it. If the effect succeeds and progress fails, replay can duplicate. If progress succeeds first and the effect fails, recovery can omit. Moving the order changes the failure, not the atomicity. Exactly-once effects require one atomic boundary or a durable protocol that makes all partial states recoverably converge.

There is no universal boundary. A database transaction can atomically join an inbox receipt, account mutation, outbox row, and source checkpoint stored in that database. It cannot automatically join an email provider or payment network. A Kafka transaction can join Kafka input offsets and output-topic records under the configured protocol. It does not automatically include an arbitrary HTTP side effect. A stream processor may checkpoint managed state exactly once while a custom sink remains at least once.

The governing question is therefore constructive: what is the effect identity, where is its linearization point, what durable evidence surrounds it, how do concurrent and late attempts converge, how long is that memory retained, and how does reconciliation detect claims the online protocol missed?

## Why This Matters

Duplicate effects are not merely duplicate rows. Repeated retries can charge a card twice, allocate two machines, send contradictory notifications, decrement inventory twice, create multiple workflow instances, append repeated ledger entries, or expose transient states in an output topic. Omissions from premature deduplication are equally serious and often harder to notice.

At-least-once delivery is usually the safest transport baseline because it preserves work under crashes. That choice pushes duplicate tolerance into state and effect design. Exactly-once effects let transport retry aggressively while business outcomes converge, but only if identities survive every hop and the target participates.

Natural idempotence is rarer than it appears. `SET status='shipped'` looks idempotent, yet a second application can overwrite a later cancellation, emit another audit entry, or update `modified_at`. `PUT /resource/7` may replace one representation, but authorization, versioning, billing, hooks, and returned identifiers can differ. Idempotence is a property of a complete operation and observation, not an HTTP verb or SQL spelling.

Deduplication stores become correctness infrastructure. Their uniqueness, isolation, retention, migration, backup, regional consistency, and authorization determine whether the claim survives concurrent workers and old retries. A fast cache is not enough if eviction reopens the effect window.

Transactional protocols bring their own operational costs. Open or prepared transactions hold resources; commit uncertainty requires recovery; transactional IDs must be unique and stable; readers may need committed isolation; checkpoint duration delays visibility; coordinator outages stall work; and a protocol upgrade can invalidate assumptions. The stronger semantic is worthwhile only when these controls are owned and tested.

## Prerequisites and Retrieval

Retrieve the business effect: exact mutation or observation; target system/tenant/resource; authoritative source; occurrence and command identity; requested parameters; result/receipt; legal state transitions; concurrency rules; reversal/compensation; customer visibility; and financial, safety, privacy, or compliance impact.

Retrieve the source contract: topic/stream/subscription generation; partition/shard/message coordinate; event ID issuer and uniqueness domain; producer request/transaction/session identity; payload/schema version; ordering/version; retention; replay/backfill; redelivery; and known producer-duplicate paths.

Retrieve the consumer contract: group/application identity; ownership generation; checkpoint semantics; processing concurrency; framework/version; input state; output state; restart/rebalance; stale-owner behavior; and where source progress becomes durable relative to the effect.

Retrieve target semantics: transaction boundary; uniqueness and conditional-write support; isolation level; linearization/commit response; item/batch partial results; idempotency-key support; key/fingerprint/result retention; read-after-write consistency; timeout behavior; rollback; replication/failover; and administrative repair APIs.

Retrieve protocol state: inbox/receipt schema; unique constraints; status machine; lease/fencing token; attempt log; request fingerprint; stored response; source coordinate; output ID; checkpoint; outbox state; transactional/producer ID; prepare/commit handle; timeout; and recovery owner.

Retrieve failure paths: crash before/after receipt reservation, effect, checkpoint, prepare, commit request, commit response, publication, and acknowledgement; concurrent duplicates; stale consumer; network partition; target failover; uniqueness/index outage; transaction timeout; coordinator loss; partial batch; replay after retention; key collision; changed parameters; schema change; and operator repair.

Retrieve operational evidence: duplicate-key conflicts; fingerprint mismatches; receipt hit/miss/age; new versus replay outcome; effect count; prepared/in-doubt transactions; aborts/fencing; outbox backlog/attempts; checkpoint/effect frontier; oldest dedup record; retry horizon; reconciliation differences; compensation; and manual override audit.

Distinguish delivery attempt from logical occurrence; event ID from broker offset; idempotency key from random retry ID; natural idempotence from deduplication; dedup receipt from effect; reservation from completion; atomicity from ordering; transaction commit request from committed decision; rollback from compensation; source transaction from downstream transaction; outbox creation from outbox publication; exactly-once state from exactly-once external effect; producer idempotence from application resend; committed visibility from physical write; and online prevention from reconciliation.

Create an effect contract:

| Concern | Required decision and evidence |
|---|---|
| Scope | Operation, target/tenant, occurrence namespace, interval, failures, exclusions |
| Identity | Issuer, canonical form, generation, collision policy, child/multi-effect derivation |
| Fingerprint | Canonical parameters, target, schema/version, digest, mismatch response |
| Linearization | Exact authoritative point making effect and receipt valid |
| Atomicity | Shared transaction or recoverable protocol linking receipt, effect, progress |
| Concurrency | Unique/conditional enforcement, isolation, stale-owner fencing, result replay |
| Retention | Retry/replay/backfill/DR horizon, tombstones, archive, expiry behavior |
| Publication | Outbox/transactional sink, stable output ID, committed visibility, relay retries |
| Failure | Every crash/timeout/partial/prepare/commit/reassignment outcome and recovery owner |
| Evidence | Fault matrix, receipts, effect query, finite-cut reconciliation, alerts, drills |

Write a falsifiable claim: “For tenant `T`, operation `post-ledger-entry`, occurrence namespace `N`, and retained cut `[a,b)`, concurrent or sequential retries with the same key and canonical fingerprint converge on one committed ledger row and one receipt in database generation `D`; conflicting fingerprints fail; source progress advances in the same transaction; stale generations are rejected; and no exactly-once claim is made for downstream notifications emitted outside the outbox/inbox protocol.”

## Learning Objectives

After completing this module, you should be able to:

1. define an exactly-once effect by identity, target, boundary, interval, and failure model;
2. distinguish repeated execution from repeated durable outcomes;
3. design atomic inbox/receipt, effect, and checkpoint transactions;
4. use unique constraints, canonical fingerprints, conditional writes, and result replay safely under concurrency;
5. explain what outbox, transactional messaging, and two-phase commit do and do not guarantee;
6. map framework-managed state and transactional sinks to their actual product scope;
7. design idempotent external API calls, deterministic files, and recoverable multi-effect workflows;
8. size and govern deduplication retention across retry, replay, backfill, and disaster recovery;
9. fence stale owners and preserve semantics through migration and regional recovery; and
10. prove the claim with fault injection, durable receipts, and finite-cut reconciliation.

## Core Exposition

### Name one effect boundary

Begin with a concrete sentence: “one accepted `invoice-issued` occurrence creates one immutable invoice ledger entry in database cluster D.” This names an operation, identity class, outcome, and target. It does not yet include email, analytics, an output topic, or a user interface.

If several outcomes matter, list them separately. A transaction may cover the invoice row and an outbox row. A relay later delivers the event to a broker. A notification consumer later calls an email API. Each boundary needs its own effect identity and recovery proof; the overall workflow needs composition and reconciliation.

Avoid “the event is processed once.” Handler invocations, deserialization, pure calculation, and prepared writes may repeat safely. Exactly-once effects are about durable observations under a named equivalence relation.

### Establish stable intent identity

An idempotency key must be generated before the first uncertain attempt and reused for all retries of that intent. If the consumer generates a UUID inside each delivery attempt, every replay looks new and deduplication cannot work. Prefer a domain-issued occurrence/command ID; derive child IDs deterministically when one input produces several effects.

Scope the key. `(tenant, operation, occurrence_id)` is safer than an unqualified UUID when issuers or environments can collide. Include a namespace generation when IDs can be recycled. Do not place raw sensitive data in keys merely for convenience; opaque high-entropy identifiers reduce leakage and guessing.

Broker coordinates can be useful receiver-local keys when source generation, topic, partition, and offset are all included and immutable. They do not identify duplicates created at publish time and should not escape as universal business identity.

### Bind keys to canonical fingerprints

The same key with different parameters is not a retry; it is conflicting intent. Compute or store a canonical fingerprint over operation, tenant/target, resource, material arguments, semantic version, and any policy-relevant context. Define normalization, field presence, ordering, numeric representation, Unicode, and hashing.

On a duplicate key, compare fingerprints before returning the prior result. If they match, return a semantically equivalent response or durable receipt. If they differ, reject and alert. Silently returning the old result can make a caller believe changed parameters took effect.

Do not blindly hash secrets into an observable ledger. Protect payload references and digests, define collision policy, and retain enough canonical evidence to diagnose mismatches without expanding privacy exposure.

### Distinguish natural and enforced idempotence

An operation $f$ is idempotent when $f\circ f=f$ over the full observable state. Set insertion into a mathematical set and assigning the same immutable content to the same generation can be idempotent. Increment, append, transfer, allocate-next-ID, and send-notification generally are not.

Even a nominal set operation may have non-idempotent side effects: audit rows, hooks, timestamps, billing, counters, or external callbacks. Conditional version checks can make a state transition apply at most once, but the conflict response and associated effects are part of the contract.

Enforced idempotence wraps a non-idempotent operation with durable identity and atomic duplicate detection. The goal is not to pretend the operation commutes with itself; it is to make repeated requests converge on the recorded first outcome.

### Build an atomic inbox and effect transaction

For a database-owned effect, start one transaction. Attempt to insert an inbox/receipt row under an authoritative unique constraint. If it is new, validate the fingerprint, apply the domain mutation, store the result, optionally advance source progress and insert outbox records, then commit. If the row already exists, verify the fingerprint and return the committed result without mutation.

Do not implement this as `SELECT` followed by `INSERT` without a uniqueness constraint. Two concurrent transactions can both observe absence. Let the database serialize on the unique key; handle conflict using the product's documented transaction/isolation semantics. PostgreSQL, for example, documents `ON CONFLICT` as selecting an alternative action for a unique/exclusion conflict, but the application must still design the complete transaction and result behavior.

Receipt and mutation must share the commit. Writing the receipt first in one transaction creates a crash window that suppresses unfinished work. Writing the mutation first creates a window that repeats it. A separate cache cannot close a database transaction gap.

### Store a meaningful prior result

Duplicate callers need a semantic response. Store status, resource/effect ID, relevant output version, canonical fingerprint, completion time, source coordinate, and perhaps a protected response snapshot or deterministic reconstruction pointer. A bare boolean “seen” can leave the caller unable to distinguish success, rejection, or an abandoned reservation.

Decide whether deterministic failures are cached. Some APIs persist the first endpoint result, including errors after execution begins; validation failures before execution may remain retryable. Whatever rule is chosen must be explicit, bounded, and versioned.

If responses contain ephemeral links, secrets, or mutable projections, do not replay them verbatim indefinitely. Store durable outcome identity and reconstruct an authorized current representation while preserving semantic equivalence.

### Avoid abandoned reservations

A common design inserts `IN_PROGRESS` in one transaction, performs an external effect, then marks `DONE`. A crash after reservation can block forever; stealing too soon can duplicate an effect already accepted but not recorded. This is not exactly once by itself.

If work cannot share one transaction, define a recoverable state machine: owner token, lease, immutable fingerprint, attempt, external idempotency key, prepare/receipt handle, last verified state, expiry, and takeover rules. Recovery queries the target by stable identity before retrying. An `IN_PROGRESS` row is evidence of uncertainty, not success.

For targets with no idempotency or query API, the uncertainty may be irreducible. Choose compensation, human resolution, a different target boundary, or an honest at-least-once/at-most-once contract.

### Use conditional mutations and fencing

Conditional writes can linearize an effect: update account version 41 to 42 only if current version is 41; insert resource only if absent; accept writer epoch 18 only if not below the stored epoch. The condition must include the protected invariant, not merely delivery identity.

Fencing is essential when consumer ownership can overlap. A stale generation may carry a valid occurrence ID that has not yet been recorded. The target should reject a lower ownership/producer epoch where ordered authority matters. Deduplication stops the same effect ID twice; fencing stops an old owner from issuing a different still-unseen effect after authority moved.

Do not derive fencing from wall-clock timestamps unless the target's protocol explicitly provides comparable trusted epochs. Use coordinator-issued monotone tokens or version preconditions enforced at the write boundary.

### Couple source progress when one store can own both

If the effect and source position can live in one database, store both in the same transaction. The checkpoint denotes the next source position after the largest contiguous set of accepted effects. Recovery reads the database checkpoint and seeks the source accordingly.

Kafka's consumer documentation describes this pattern: store results and offsets atomically in the same system, disable automatic commits, and restore the consumer position from that store. The claim then covers the database transaction boundary under the application's assignment and fencing rules—not Kafka's separate group-offset store.

Multiple partitions require a vector of next positions or per-partition rows. Concurrency still cannot advance across holes. Assignment generation, topic generation, and leader epoch where applicable prevent a stale or recreated source from reusing coordinates incorrectly.

### Use an outbox to eliminate a source dual write

A service that changes its database and publishes an event faces another dual write. Insert an immutable outbox row in the same transaction as the domain change. A CDC connector or relay later publishes it. Because the transaction commits both or neither, the event obligation is durable with the source change.

The relay is normally at least once: it may publish and crash before marking progress. Preserve one outbox event ID across relay attempts. Consumers use that ID in their own inbox/effect boundary. The outbox makes reliable publication possible; it does not by itself make the broker contain one physical record or every downstream side effect occur once.

Debezium's documented outbox router expects an event ID field that can be propagated for duplicate removal and an aggregate ID useful as the message key. Preserve both identity roles and restrict the connector transformation to the intended outbox table shape.

### Use transactional consume-transform-produce within its domain

Messaging platforms can join consumed progress with output records. In Kafka, a transactional producer can send to multiple partitions atomically, send consumed offsets to the transaction, and rely on committed-read consumers. Kafka Streams' current exactly-once-v2 guarantee atomically coordinates input offsets, state-store updates, and Kafka output-topic writes within its documented environment.

Kafka producer idempotence prevents duplicates from supported client retries within its documented producer/session scope; application-level resend is not automatically deduplicated. A transactional ID extends recovery/fencing across producer sessions and must be uniquely assigned to the intended producer instance. Transactional topic durability and consumer `read_committed` configuration remain part of the proof.

Pulsar documents transactions that atomically cover writes and acknowledgements across topics for consume-process-produce. Preserve the Pulsar-specific transaction, subscription, client, broker, timeout, and committed-visibility requirements; do not translate the claim into arbitrary external effects.

### Understand prepare and commit

Two-phase-style sinks separate writing/preparing from final visibility. A writer creates durable committables associated with checkpoint $k$; after the framework declares $k$ complete, a committer makes them visible. Recovery must be able to commit an already-decided unit idempotently or abort one that never received a commit decision.

Flink's current Sink API documents `SupportsCommitter` for exactly-once semantics using a two-phase commit protocol, with a committing writer producing committables at checkpoint/end of input and a committer finalizing them. This is an interface and protocol obligation, not evidence that every custom sink is correct.

Inventory transaction identifiers, staged objects, checkpoint IDs, decision logs, commit retries, abort cleanup, timeout limits, maximum open transactions, and reader visibility. A lost commit response must not cause a new unrelated transaction that duplicates output.

### Publish files and tables by immutable generation

Object stores and table formats often lack a single rename/transaction spanning every object. Write data files to immutable names derived from job/output generation, partition, input cut, and content digest. Retry creates or verifies the same objects. Publish a manifest/snapshot pointer conditionally only after all referenced objects exist and validate.

Readers consume only committed manifests, not listing results or staging prefixes. Repeating manifest publication with the same generation is idempotent; a different content digest under the same identity is a conflict. Garbage collection waits until no committed/recoverable snapshot references staged files.

Exactly-once here means one logical table snapshot or file generation for the input cut, not one physical write request. Duplicate identical objects can be harmless storage waste, while two committed manifests for one generation are a semantic conflict.

### Call external APIs with server-owned idempotency

For an HTTP or RPC effect, the target must participate. Send a stable caller-scoped idempotency token and the same semantic parameters on retry. The server atomically records the token with all mutations and returns a semantically equivalent result for duplicates; changed parameters under the same token are rejected.

Stripe's current API documentation illustrates a concrete bounded contract: idempotency keys on `POST`, saved first results after endpoint execution begins, parameter comparison, and possible key pruning after at least 24 hours. That retention may be shorter than a stream backfill horizon, so the pipeline cannot blindly replay older inputs against the API.

AWS's Builders' Library similarly emphasizes caller-provided request identifiers, atomic recording with mutations, semantically equivalent retry responses, late arrivals, and parameter mismatch. Use a target's actual contract, not the general pattern, to decide the supported interval.

### Design retention from the latest possible retry

Deduplication memory must outlive the maximum late attempt, not just the normal retry loop. Include broker retention, checkpoint rollback, disaster restore, regional failover, delayed queue, manual replay, backfill, offline device delay, incident detection/approval, and clock uncertainty.

Let $T_r$ be automatic retry horizon, $T_b$ broker/source replay, $T_d$ disaster rollback age, $T_m$ authorized manual delay, and $\epsilon$ safety margin. A conservative receipt retention is

$$
T_{dedup}\ge\max(T_r,T_b,T_d,T_m)+\epsilon.
$$

If indefinite business uniqueness is required, bind the key to an immutable domain ledger rather than an expiring cache. If receipts expire, state the guarantee interval and route older replay through isolated reconciliation instead of the live effect path.

### Handle multi-effect workflows honestly

One input may update a database, publish an event, charge a payment method, and send a notification. Unless all targets share one transaction—which is uncommon—there is no single atomic exactly-once boundary. Give every step a deterministic child effect ID and durable workflow state.

Drive the workflow forward with retry-safe commands and target receipts. Some effects are reversible; others need compensation, such as refunding rather than erasing a charge. Compensation is a new auditable effect, not rollback of history. Define dependency ordering, terminal states, deadlines, escalation, and reconciliation.

Sometimes the best boundary changes the design: record an immutable payment intent once, let a specialized payment service execute it idempotently, and have downstream views consume its authoritative outcome. Narrow ownership is easier to prove than distributed exactly once across arbitrary services.

### Preserve semantics through change and disaster recovery

Schema and code changes can alter canonical fingerprints, key scopes, effect derivation, unique indexes, and replay behavior. Version them. During rollout, old and new workers must agree on existing identities and results or be isolated by generation. Never rebuild a dedup table from incomplete recent logs while accepting live traffic.

Back up receipts, inbox/outbox rows, transactional metadata, checkpoints, and effect state consistently. A disaster restore to yesterday followed by replay can repeat effects made after the backup if the external target did not roll back. Query/reconcile target receipts or retain an independent durable ledger across the recovery point.

Regional active-active operation requires an authority model. Eventually replicated dedup caches can accept the same key concurrently in two regions. Use a globally consistent home, partitioned ownership with fencing, target-native idempotency, or a conflict-safe effect design.

### Observe effect semantics

Instrument new-key wins, duplicate-key hits, fingerprint mismatches, returned prior results, conditional-write conflicts, stale-token rejection, receipt/effect transaction latency, aborts, commit uncertainty, prepared age, outbox backlog/publication attempts, inbox age, dedup retention headroom, and reconciliation differences.

Count logical occurrences and durable effect identities separately from attempts. A high dedup-hit rate can indicate healthy replay or an upstream retry storm. A zero duplicate-row count can coexist with omitted effects if receipts were written early. A commit-success metric can coexist with unobserved results if readers ignore committed visibility rules.

Dashboards should trace occurrence → attempts → receipt → effect/version → outbox/output → checkpoint → visible projection. Protect identifiers and payloads while keeping joinable opaque references for incident investigation.

### Test linearization and recovery

Inject failure before receipt insert, after insert but before mutation, after mutation before commit, during commit, after commit before response, before/after checkpoint, during outbox publication, after publish before relay progress, during prepare, after prepare before decision, during commit, after commit response loss, and during stale-owner overlap.

Run concurrent identical requests and same-key/different-payload requests. Restore an old checkpoint, replay beyond receipt retention, fail over regions, migrate schemas, rebuild indexes, time out transactions, and rotate credentials. Query the authoritative target rather than counting client returns.

For a finite input cut, prove every valid occurrence has exactly one accepted receipt/effect identity, every conflict has a governed outcome, source progress does not cross a missing effect, and published/visible generations match the contract. Preserve the attempt and effect ledger as evidence.

### Review the complete once-only argument

A defensible design connects fifteen claims: effect boundary is named; occurrence keys are stable/scoped; fingerprints bind intent; target uniqueness/conditions serialize concurrency; receipt and effect are atomic or recoverably staged; duplicate result semantics are defined; progress follows effects; ownership is fenced; outbox/transactional publication preserves identity; readers observe only committed data; retention covers all retries/replay/DR; multi-effect steps have child identities; migrations preserve compatibility; metrics expose uncertainty; and fault/reconciliation tests prove the finite cut.

Remove any link and the claim narrows. A unique key without atomic mutation can omit. A transaction without stable identity can apply two distinct retries. An outbox without downstream inbox can publish duplicates. A framework checkpoint cannot include an arbitrary side effect. A dedup cache cannot protect replay after eviction. Exactly-once effects are an end-to-end argument over a deliberately small boundary.

## Definitions and Notation

Let $x\in X$ be a logical occurrence in namespace $N$ and tenant/domain $T$. Let $k(x)$ be its idempotency key and $h(x)$ its canonical request fingerprint.

- $B$: named effect boundary.
- $E_B(x)$: set of durable effects at $B$ attributed to $x$.
- $R_B(x)$: durable receipt containing key, fingerprint, status, result, and version.
- $A(x)$: set of delivery or request attempts for $x$.
- $g$: current ownership or writer generation.
- $v$: target state version used by a conditional mutation.
- $O(x,i)$: deterministic child effect ID for child index/role $i$.
- $P$: durable next-source-position checkpoint.
- $Q$: governed conflict/quarantine outcomes.
- $T_{dedup}$: duration for which the target remembers completed keys.
- $T_{late}$: maximum supported age of any retry or replay.

The once-only safety property for accepted valid occurrences is

$$
\forall x:\quad |E_B(x)|\le1.
$$

The liveness/completeness property is

$$
\forall x\in X_{required}:\quad |E_B(x)|\ge1,
$$

so together they yield $|E_B(x)|=1$. Invalid or conflicting occurrences must be excluded by a declared predicate and mapped to $Q$; otherwise moving them aside weakens completeness.

Idempotence of a state transition $f_x$ is

$$
f_x(f_x(s))=f_x(s).
$$

For a non-idempotent transition $u_x$, an apply-once wrapper can be modeled as

$$
W(s,R,x)=
\begin{cases}
(u_x(s),R\cup\{k(x)\mapsto(h(x),result)\}), & k(x)\notin R,\\
(s,R), & R[k(x)].fingerprint=h(x),\\
\text{conflict}, & \text{otherwise}.
\end{cases}
$$

This wrapper is safe only when the state mutation and receipt update occur atomically or an equivalent protocol resolves partial states. The map expression alone is not an implementation proof.

For $m$ attempts and $n$ unique matching keys, naive non-idempotent application performs $m$ effects while apply-once performs $n$; duplicate attempts suppressed are $m-n$. Conflicting same-key/different-fingerprint attempts are not duplicates and should not enter either total silently.

If one occurrence produces child roles $I$, deterministic child identities satisfy

$$
O(x,i)=H(N\parallel k(x)\parallel i\parallel version),\qquad i\in I,
$$

where framing/canonicalization and collision policy are specified. The parent completes only under an explicit predicate over child receipts, such as all required children committed.

For retention,

$$
T_{dedup}\ge T_{late}+\epsilon,
$$

and $T_{late}$ must include automatic retries, source replay, checkpoint rollback, disaster restore, delayed delivery, backfill, and authorized manual action. A smaller retention makes the once-only claim interval-bounded.

## Mechanisms, Invariants, or Proof Structure

Use this review sequence:

1. **Name the effect.** Identify the exact durable target observation and finite required input cut.
2. **Choose identity.** Define issuer, namespace, scope, generation, and deterministic child IDs before any attempt.
3. **Bind intent.** Canonicalize and fingerprint material operation parameters and target.
4. **Find the linearization point.** Identify the authoritative transaction commit, conditional write, target receipt, or committed manifest.
5. **Join receipt and effect.** Use one transaction or specify every recoverable intermediate state and owner.
6. **Serialize concurrency.** Enforce uniqueness/conditions at the target; reject stale generations and payload conflicts.
7. **Return prior outcomes.** Preserve enough result evidence for semantic retry responses and diagnosis.
8. **Advance progress safely.** Commit next positions with the effect or only after authoritative receipt lookup.
9. **Publish reliably.** Preserve event IDs through outbox relay or supported transactional messaging; require committed visibility.
10. **Retain memory.** Cover the latest possible retry/replay/backfill/DR attempt and govern expiry.
11. **Compose workflows.** Give each non-atomic target a child effect state, retry, compensation, and reconciliation rule.
12. **Test and reconcile.** Inject failures at every boundary and compare authoritative obligations to durable effects.

The safety invariant is:

> For every accepted key/fingerprint in the declared namespace and interval, concurrent and repeated attempts can expose at most one effect at the named boundary, and no stale owner can create an alternate effect.

The liveness invariant is:

> Every valid required occurrence eventually has one committed effect/receipt or an explicitly allowed terminal outcome while identity, replay, retention, capacity, and target authority remain available.

Exactly-once safety without liveness can reserve keys forever and omit work. Liveness without safety can retry into duplicates. Both depend on availability and correctness of the target transaction/condition, identity issuer, durable receipt store, recovery process, and reconciliation authority.

This executable compares naive application with an atomic apply-once abstraction. It demonstrates key/fingerprint decisions over finite data; it does not implement transaction isolation, durable storage, distributed commit, fencing, or recovery.

<!-- bijux-verify: {"id":"apply-once-ledger","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"attempt_count=7\nunique_matching_effects=3\nduplicate_replays=3\nfingerprint_conflicts=1\nnaive_balance=120\napply_once_balance=110\nreceipts=(('acct-7:e-100', 7), ('acct-7:e-101', -2), ('acct-7:e-102', 5))\noutbox_ids=('balance:e-100', 'balance:e-101', 'balance:e-102')\nexactly_once_effect_count=True\n","stderr":""}} -->
```python
starting_balance = 100
attempts = (
    ("acct-7:e-100", 7),
    ("acct-7:e-101", -2),
    ("acct-7:e-100", 7),
    ("acct-7:e-102", 5),
    ("acct-7:e-101", -2),
    ("acct-7:e-102", 5),
    ("acct-7:e-101", -9),  # Same key, conflicting intent.
)

naive_balance = starting_balance + sum(
    amount for _, amount in attempts if amount != -9
)
apply_once_balance = starting_balance
receipts = {}
outbox_ids = []
duplicates = 0
conflicts = 0

for key, amount in attempts:
    if key in receipts:
        if receipts[key] == amount:
            duplicates += 1
        else:
            conflicts += 1
        continue
    # In a real design, receipt, mutation, and outbox insert share one commit.
    receipts[key] = amount
    apply_once_balance += amount
    event_id = key.split(":", 1)[1]
    outbox_ids.append(f"balance:{event_id}")

print(f"attempt_count={len(attempts)}")
print(f"unique_matching_effects={len(receipts)}")
print(f"duplicate_replays={duplicates}")
print(f"fingerprint_conflicts={conflicts}")
print(f"naive_balance={naive_balance}")
print(f"apply_once_balance={apply_once_balance}")
print(f"receipts={tuple(sorted(receipts.items()))}")
print(f"outbox_ids={tuple(outbox_ids)}")
print(f"exactly_once_effect_count={len(receipts) == len(set(receipts))}")
```

The model assumes the first matching request wins and the transaction never partially commits. Production evidence must establish those assumptions in the actual target.

## Alternatives and Trade-Offs

**Natural idempotence versus dedup ledger.** Natural idempotence avoids receipt lookup/storage but may not cover metadata, hooks, or concurrent versions. A ledger handles non-idempotent operations and returns prior results, at storage/retention/privacy cost.

**Database transaction versus external progress store.** One database transaction offers a clear atomic boundary for local effect, inbox, checkpoint, and outbox. External group offsets integrate with broker tooling but leave an effect/progress crash window unless another protocol coordinates them.

**Unique insert versus conditional version update.** Unique identity stops the same occurrence twice. Version conditions protect state-machine order and stale writers. Many systems need both because different occurrences can conflict with the same resource.

**Store full response versus reconstruct.** Full response replay is simple and semantically stable but may retain secrets or stale presentation. Storing durable result identity reduces exposure but needs deterministic authorized reconstruction.

**Outbox versus direct dual write.** Outbox atomically couples source data and publication obligation and supports CDC. It adds table/connector/backlog operations and does not eliminate duplicate relay or downstream inbox needs.

**Transactional messaging versus application inbox/outbox.** A platform transaction can efficiently cover supported topics, offsets, and state. Inbox/outbox crosses application/database boundaries more flexibly. Neither automatically covers unsupported external services.

**Two-phase commit versus idempotent sink.** Two-phase commit can make a checkpoint cut atomically visible but holds prepared resources and needs recovery. Idempotent sinks tolerate replay with simpler coordination when stable identity and deterministic results exist.

**Pessimistic lock versus optimistic condition.** Locks serialize directly but can reduce throughput and create deadlock/timeout pressure. Optimistic unique/version conditions scale well under low contention but require explicit conflict/retry behavior.

**Permanent ledger versus expiring cache.** Permanent domain receipts support indefinite uniqueness and audit but grow without bound. TTL stores control cost but time-bound the guarantee and require protected handling of older replay.

**Global deduplication versus partitioned ownership.** Global consistency prevents cross-region duplicates but adds latency/availability coupling. Partitioned home regions scale better if routing and fencing never overlap; failover is more complex.

**Synchronous effect versus durable intent workflow.** Direct calls offer low latency but expose caller timeouts. Persisting an intent/outbox makes progress recoverable and lets a specialized worker own the effect, at asynchronous latency and operational cost.

**Compensation versus strict atomicity.** Compensation enables multi-system workflows where one transaction is infeasible, but observers can see intermediate effects and compensation may not restore the original world. It is a different semantic, not exactly-once atomicity.

## Failure Modes and Misconceptions

**“Same payload means duplicate.”** Two legitimate occurrences can share a payload. Identity must express intent, not content equality alone.

**“A UUID per attempt enables idempotency.”** It makes every retry distinct. Generate before the first attempt and reuse it.

**“Broker offset is the event ID.”** It identifies one accepted record in one topic generation/partition; publisher duplicates have other offsets and external effects need durable business scope.

**“Check then insert is safe.”** Concurrent workers can both observe absence. Enforce uniqueness or a condition at the authoritative target.

**“Insert receipt, then call the API.”** A crash leaves a false completed marker or abandoned reservation that can suppress required work.

**“Call the API, then insert receipt.”** A crash after acceptance repeats the external effect unless the API itself deduplicates/query-resolves the stable key.

**“Upsert makes increments idempotent.”** Updating `balance = balance + amount` on conflict repeats the increment. The operation, not the SQL keyword, must converge.

**“PUT is always idempotent.”** Hooks, versions, authorization, generated fields, billing, and changed request bodies can create different observations.

**“Return already exists on retry.”** It may leave the caller unable to know whether its first request created the resource. Store and return semantic prior outcome.

**“One key can be reused after changing parameters.”** This conflates intents. Compare fingerprints and reject mismatch.

**“The dedup cache can expire after normal retries.”** Checkpoint restore, delayed delivery, backfill, and disaster recovery may arrive much later.

**“Producer idempotence covers application resends.”** Kafka's current producer documentation explicitly limits supported idempotence and warns that application-level resends are not automatically deduplicated.

**“Kafka transaction includes my HTTP call.”** It covers supported Kafka records/offsets and associated framework state, not arbitrary external effects.

**“Outbox publishes one physical message.”** Relay retry can duplicate publication. Stable event identity and downstream inbox remain necessary.

**“Prepared means committed.”** Prepared data may later abort. Readers and operators need committed decision/visibility.

**“Commit timeout means abort.”** The decision may have succeeded while the response was lost. Recover/query using the same transaction identity.

**“Exactly-once state means exactly-once email.”** Managed state and external notification are different boundaries.

**“Deduplication is enough for stale owners.”** An old owner can issue a different unseen effect. Enforce fencing/version authority too.

**“Compensation erases the first effect.”** It adds a new effect and may not reverse external observation, time, or legal consequences.

**“No duplicate alerts prove exactly once.”** Omitted effects, key collisions, early receipts, and unobserved targets require full reconciliation.

## Worked Examples

### Example 1

Two workers concurrently receive `ledger-entry/e-91`. Both attempt an inbox insert in the same database transaction as the ledger mutation. The unique constraint selects one winner; the loser reads the matching fingerprint/result. One ledger row and receipt commit. An application-level precheck alone would not prove this.

### Example 2

A replay sends key `create-report/r-8` with a different date range than the original. The stored fingerprint mismatches, so the target returns an intent-conflict error and quarantines evidence. Returning the old report would falsely claim the new range was created.

### Example 3

An order service commits `status=PAID` and outbox event `payment-recorded/e-44` together. The CDC relay publishes twice after losing its first acknowledgement. The shipping consumer's inbox deduplicates `e-44` with its local shipment transition. The outbox solved the source dual write; the inbox solved the downstream replay.

### Example 4

A Kafka application consumes order partition 2 offset 90 and emits invoice and audit records in one Kafka transaction with next input offset 91. Committed-read consumers see both outputs or neither. A separate email call inside the handler can still repeat and is moved behind an idempotent notification intent.

### Example 5

A Flink sink stages files for checkpoint 700 under immutable names, emits committables, and publishes one manifest only after checkpoint completion. Recovery retries the same commit identities. Readers ignore staging. The claim is one committed snapshot for the cut, not one object-store request.

### Example 6

A payment API retains idempotency keys for 24 hours, while the stream can replay seven days after disaster restore. Live automatic retries are protected; old replay is not. The system retains a permanent internal payment-intent ledger and routes old recovery through target receipt lookup/reconciliation.

### Example 7

Region A and B both consume during a partition while their dedup tables replicate eventually. Each inserts `allocate/x-2` and allocates a server. The fix assigns the tenant to one fenced home region or uses a globally consistent target. Eventual duplicate convergence cannot undo two external allocations.

### Example 8

A worker reserves `email/e-12`, sends the email, and crashes before `DONE`. Because the provider lacks idempotency and query-by-key, takeover cannot distinguish sent from unsent. The team narrows the claim to at-least-once email, records an uncertainty case, and redesigns around a provider-supported message identity.

### Example 9

Restoring yesterday's database backup removes receipts for effects that remain in an external payment network. Replaying the log would charge again. Disaster recovery first imports/query-reconciles payment receipts and fences live processing before replaying from the old checkpoint.

### Example 10

One order occurrence needs inventory reservation, payment, and notification. Each gets a deterministic child ID and durable workflow state. Inventory and payment use target-native idempotency; notification is best-effort with reconciliation. A refund compensates a later inventory failure. The workflow does not pretend all three systems committed atomically.

## Cross-Program Connections

Database systems contributes ACID transactions, unique constraints, isolation, conditional updates, MVCC, write-ahead logging, recovery, and serializable histories. The local inbox/effect/checkpoint pattern is a database transaction design.

Distributed systems contributes linearizability, consensus, fencing, epochs, leases, atomic commit, two-phase commit, partial failure, and uncertain outcomes. Exactly-once effects are distributed agreement about identity and visibility.

API and service engineering contributes caller-provided idempotency keys, canonical request semantics, conditional requests, receipts, retries, deadlines, status resources, and versioned error contracts.

Software architecture contributes transactional outbox, inbox, sagas, process managers, aggregate ownership, command/event separation, and compensation. These patterns deliberately choose atomic boundaries.

Formal methods contributes safety and liveness, refinement, state machines, invariants, linearization points, temporal logic, and adversarial schedules around commit uncertainty.

Security engineering contributes key authenticity, namespace isolation, replay protection, receipt integrity, authorization, least privilege, tamper evidence, and privacy-safe retention.

Cryptography contributes collision-resistant digests, canonical encoding, authenticated tokens, and key rotation. Hashing supports identity evidence but does not create atomicity.

Operating systems contributes crash consistency, durable flush, process identity, cancellation, buffered I/O, and recovery. A local return is not necessarily stable storage.

Site reliability engineering contributes fault injection, disaster recovery, reconciliation, prepared-transaction monitoring, retention headroom, change safety, capacity, and incident repair.

Platform engineering contributes transactional connector support, secret/identity distribution, regional routing, schema migrations, deployment fencing, managed state stores, and guarded replay tooling.

Accounting contributes immutable ledgers, balancing entries, reversals, audit trails, and reconciliation. Financial effects are better represented as durable facts than overwritten state.

Data governance contributes retention, erasure, lineage, tenant boundaries, legal hold, and evidence access. Deduplication memory is governed production data.

## References

1. Apache Kafka. [Producer Configuration, Apache Kafka 4.3](https://kafka.apache.org/43/generated/producer_config.html). Accessed 2026-09-03. Primary configuration reference for idempotence, acknowledgements, retries, in-flight ordering, transactional IDs, and transaction timeout.
2. Apache Kafka. [KafkaProducer API, Apache Kafka 4.3](https://kafka.apache.org/43/javadoc/org/apache/kafka/clients/producer/KafkaProducer.html). Accessed 2026-09-03. Primary API documentation for idempotent and transactional producer scope, application resend caveats, producer sessions, fencing, atomic multi-partition writes, and committed readers.
3. Apache Kafka. [Kafka Streams Core Concepts, Apache Kafka 4.3](https://kafka.apache.org/43/streams/core-concepts/). Accessed 2026-09-03. Primary documentation for exactly-once-v2 coordination of input offsets, state stores, and Kafka output topics.
4. Apache Kafka. [KafkaConsumer API, Apache Kafka 4.3](https://kafka.apache.org/43/javadoc/org/apache/kafka/clients/consumer/KafkaConsumer.html). Accessed 2026-09-03. Primary client documentation for atomically storing offsets with results in an external store and restoring source position.
5. Apache Flink. [Fault Tolerance](https://nightlies.apache.org/flink/flink-docs-stable/docs/learn-flink/fault_tolerance/). Accessed 2026-09-03. Primary documentation distinguishing replayed execution, exactly-once managed state, and end-to-end transactional/idempotent sink requirements.
6. Apache Flink. [Data Sinks](https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/internals/sinks/). Accessed 2026-09-03. Primary Sink API documentation for writer state, committables, committers, and two-phase-commit exactly-once semantics.
7. Apache Pulsar. [What Are Transactions?](https://pulsar.apache.org/docs/4.2.x/txn-what/). Accessed 2026-09-03. Primary documentation for atomic writes and acknowledgements across topics and transactional consume-process-produce scope.
8. Debezium. [Outbox Event Router](https://debezium.io/documentation/reference/stable/transformations/outbox-event-router.html). Accessed 2026-09-03. Primary documentation for outbox-table capture, stable event IDs, aggregate keys, routing, and duplicate-removal identity.
9. PostgreSQL Global Development Group. [PostgreSQL INSERT](https://www.postgresql.org/docs/current/sql-insert.html). Accessed 2026-09-03. Primary SQL documentation for unique-index conflicts and `ON CONFLICT` actions used in concurrency-safe receipt insertion.
10. Stripe. [Idempotent Requests](https://docs.stripe.com/api/idempotent_requests). Accessed 2026-09-03. Primary API documentation for retry keys, stored results, parameter comparison, execution boundary, and retention limits.
11. Amazon Web Services. [Making Retries Safe with Idempotent APIs](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/). Accessed 2026-09-03. Primary engineering guidance for caller request IDs, atomic token/effect storage, semantic retry responses, late requests, and conflicting intent.

## Exercises

### Exercise 1

A balance starts at 200. Attempts arrive as `(a,+10)`, `(b,-4)`, `(a,+10)`, `(c,+7)`, `(b,-4)`, `(c,+7)`, and `(b,-9)`. Under first-key-wins with fingerprint comparison, compute the naive matching-retry balance, apply-once balance, new effects, duplicate hits, and fingerprint conflicts. Explain what atomicity the arithmetic assumes.

### Exercise 2

Automatic retries last 20 minutes, broker replay reaches 72 hours, disaster restore can roll back 9 days, authorized backfill may occur after 30 days, and safety margin is 2 days. Compute minimum dedup retention. Assess a target API that prunes keys after 24 hours and propose a safe older-replay path.

### Exercise 3

For an inbox/effect/checkpoint transaction, place crashes at: before receipt insert, after receipt insert but before mutation, after mutation but before commit, during commit with response loss, and after commit before source acknowledgement. State recovery behavior when all three records share one database transaction, then contrast a receipt committed before an external effect.

### Exercise 4

Design exactly-once effects for a partitioned consumer updating account balances in PostgreSQL. Include event/key namespace, fingerprint, unique/index and receipt schema, balance/version condition, checkpoint vector, ownership fencing, transaction steps, duplicates/conflicts, outbox, retention, migration, metrics, and fault/reconciliation tests.

### Exercise 5

Audit a claim that a Kafka Streams exactly-once-v2 application also creates exactly one support ticket through an HTTP API. Separate the documented Kafka boundary from the ticket boundary and design a durable intent plus target-idempotency or reconciliation protocol. State the strongest honest claim if the ticket API has neither idempotency nor query-by-request-ID.

## Answers to the Exercises

### Answer 1

Ignoring the conflicting final `(b,-9)` as not a matching retry, naive application performs six arithmetic effects and produces $200+10-4+10+7-4+7=226$. Apply-once accepts keys `a:+10`, `b:-4`, and `c:+7`, producing $200+10-4+7=213$. There are three new effects, three same-key/same-fingerprint duplicate hits, and one same-key/different-fingerprint conflict. The arithmetic assumes duplicate classification, receipt insertion, balance mutation, and prior-result storage are one authoritative atomic/serializable decision. Without that, concurrent first attempts or a crash between receipt and mutation can violate the result.

### Answer 2

The latest supported attempt is the 30-day authorized backfill; adding a 2-day margin gives minimum $T_{dedup}=32$ days. The 9-day disaster restore dominates ordinary broker and automatic retry but not backfill. A target that prunes keys after 24 hours cannot protect direct 30-day replay. Retain a durable internal effect ledger for at least 32 days or permanently, isolate older replay, query the target by durable business/effect identity, compare obligations with receipts/results, and conditionally repair. Do not send old records directly through the live API under the expired key and claim exactly once.

### Answer 3

Before receipt insert, nothing commits and recovery retries. Receipt insert and mutation are uncommitted intermediate writes inside the same transaction, so crashes after either but before commit roll back both; recovery retries. During commit with response loss, the outcome is uncertain to the caller, but recovery reuses the same key and queries/retries the database transaction: if committed, the receipt/result is returned without mutation; if aborted, one new transaction applies all records. After commit before source acknowledgement, replay finds the receipt and returns the prior result, then safely advances progress. If a receipt is committed in one transaction before an external effect, a crash can leave “seen” with no effect; a retry may suppress the required work. An `IN_PROGRESS` state needs target-native idempotency/query and a recoverable owner/lease protocol, not blind skipping.

### Answer 4

Use a key such as `(tenant, account-balance-transition, event_namespace_generation, event_id)` issued before publication, plus a canonical fingerprint over account, signed amount, currency, business version, and schema. In PostgreSQL create an inbox table with a unique constraint on that key and fields for fingerprint, source topic generation/partition/offset, owner generation, committed account version, result, and timestamps. In one transaction insert the receipt or detect conflict, lock/conditionally update the account from expected version $v$ to $v+1$, record the result, advance that partition's next offset only through the contiguous accepted prefix, and insert an immutable outbox row with deterministic event ID. Reject fingerprint mismatch and stale ownership/version; matching duplicates return the stored result. Relay may publish repeatedly, so downstream uses the outbox ID. Retain inbox/checkpoints across maximum replay/backfill/DR, back them up consistently, and version fingerprint/schema migration. Monitor new/duplicate/conflict/stale counts, transaction retries, checkpoint/effect gaps, outbox age, and retention headroom. Test concurrent duplicates, changed payload, every crash point, commit-response loss, rebalance/stale owner, checkpoint restore, index migration, receipt expiry, and source-to-ledger reconciliation.

### Answer 5

Kafka Streams exactly-once-v2 covers its documented Kafka input offsets, state stores, and Kafka output-topic records when transactional IDs, broker durability, and committed-read consumers are correct. An HTTP ticket call is outside that transaction. Persist a deterministic `create-ticket/<source-occurrence>` intent as a Kafka transactional output or database outbox record, then let a specialized worker call the ticket API with the same target-supported idempotency key on every attempt. Store/query the target ticket ID and receipt, reject parameter mismatch, advance intent progress after the receipt, retain keys across replay, and reconcile intents with tickets. If the API supports query-by-request-ID but not atomic idempotency, recovery can resolve uncertain calls before retrying. If it supports neither idempotency nor query, exactly-once ticket creation is unprovable: the strongest honest claim is at-least-once attempts with possible duplicate tickets (or at-most-once with possible omission), plus detection, manual reconciliation, and a plan to change the boundary/provider.
