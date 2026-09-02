---
module_id: PLAT-055
program: Platform Engineering
level: 2
module_number: 55
title: Idempotent Reconciliation
status: complete
last_verified: 2026-09-02
---

# Idempotent Reconciliation

## One-Page Review

### Governing question

How can a controller safely repeat reconciliation after duplicate events, conflicts, crashes, timeouts, leader changes, and late responses without duplicating or misapplying external effects?

### Essential definitions

- **idempotency** means repeating an operation one or more times has the same intended effect as performing it once.
- An **attempt** is one execution of a request; an **operation** is the stable logical intent that may span many attempts.
- An **idempotency key** identifies one logical operation within a declared tenant, API, resource, and retention scope.
- A **request fingerprint** is a canonical digest of the intent-bearing parameters bound to that key.
- A **deduplication record** stores the fingerprint, lifecycle state, result or external identity, and expiry for an operation key.
- An **ambiguous outcome** exists when the caller cannot determine whether an effect occurred, commonly after timeout or connection loss.
- **create-or-adopt** means create by stable identity, or adopt an existing object only after verifying owner and intended configuration.
- A **conditional write** applies only if a version, generation, state, or field precondition still holds.
- A **tombstone** preserves enough deletion or deduplication evidence after the primary object disappears to classify late attempts.
- **effect identity** answers “which real-world change?”; request transport identity and reconcile invocation identity do not answer it automatically.

### Central model, mechanism, or theorem

For state transformer $f$, effect idempotency requires $f(f(x))=f(x)$ for every state in scope. A controller realizes this property through a protocol, not a retry flag. Derive a stable key $k$ from durable resource identity and logical intent; derive canonical fingerprint $h$. Atomically reserve a record $D(k)=(h,q,r,t_e)$ with lifecycle $q$, result/effect identity $r$, and expiry $t_e$. An unseen key may start. The same key and same fingerprint resumes or replays the recorded result. The same key and a different fingerprint is rejected. An in-progress or unknown result is observed by stable external identity before any new mutation. Expiry ends the deduplication guarantee unless another durable identity or tombstone still prevents duplication.

### Critical invariants

- Operation keys are stable across attempts but distinct across logically different effects, resource UIDs, tenants, and relevant desired generations.
- One key is bound to one canonical fingerprint; key reuse with different intent fails closed.
- Reservation and service-side mutation are atomic when they share a store, or the external API supplies an equivalent idempotency/identity guarantee.
- A timeout means outcome unknown, never known failure; recovery observes before it creates or mutates again.
- Existing external state is adopted only after identity, ownership, tenant, and intent checks succeed.
- Absolute desired assignments are preferred over relative commands; concurrent updates use versions, tests, or field ownership.
- Successful response replay is semantically equivalent; it need not repeat incidental timestamps or transport bytes.
- Deduplication retention exceeds the documented retry and late-delivery horizon, including queues, restore, and disaster recovery.
- Delete convergence includes dependent effects, finalizers, tombstones, and name/UID reuse—not merely “not found.”
- Tests inject crashes at every reservation, call, response, observation, and checkpoint boundary and include concurrent and late duplicates.

### Common failures

Generating a random provider name on every reconcile; treating HTTP POST, PUT, or DELETE labels as end-to-end proof; using Kubernetes name without UID; caching by key without comparing payload; writing a dedup record after the effect; retrying timeout immediately; treating every conflict as previous success; adopting another tenant’s object; expressing “increment replicas” instead of “set replicas to target”; pruning keys before queued retries expire; recording only successes; confusing work-queue coalescing with effect deduplication; assuming leader election prevents old requests; deleting the primary record before cleanup evidence; and claiming exactly-once execution because duplicate effects were suppressed.

### Compact example

A database claim with UID `u7` requests provider plan digest `p3`. The operator derives `tenant/acme/database/u7/provision/p3`, persists that key and fingerprint before submission, and asks the provider to create resource `db-u7` with the same token and owner tags. The response is lost. On restart, the operator does not generate a new name or submit a blind second create. It looks up the operation and `db-u7`. If an object exists with the expected tenant, UID, and fingerprint, it adopts and records the provider ID. A mismatched object causes a collision condition and human-safe quarantine. Absence plus an expired provider search window permits a bounded retry with the same key. Conditions expose `Provisioning`, `OutcomeUnknown`, or `IdentityCollision`; none fabricates exactly-once execution.

### Connections

This module specializes desired-state convergence from [PLAT-052](052-desired-state-and-reconciliation.md), durable workflow checkpoints from [PLAT-054](054-operator-state-machines.md), Kubernetes workload identity from [PLAT-024](024-pods-workloads-and-controllers.md), and API concurrency from API & Service Engineering. PLAT-056 applies these effect rules to finalizers and deletion; PLAT-057 through PLAT-060 extend them to status, dependency graphs, recovery, and domain APIs.

## Governing Question

How can a platform controller repeatedly attempt work while ensuring that repetition converges on one authorized effect rather than accumulating duplicate infrastructure, payments, messages, grants, routes, or deletions?

Reconciliation is intentionally repetitive. A watch may deliver duplicate notifications, a worker may crash after an external call, an API server may reject a stale status update, or a network may lose the successful response. At-least-once scheduling is usually the practical availability choice. Yet many effects—provisioning a database, rotating a secret, incrementing capacity, publishing an event—are not naturally safe to repeat.

Idempotent reconciliation bridges that mismatch. It does not mean that the reconcile function runs once, that responses are byte-identical, or that every downstream system offers exactly-once execution. It means the entire protocol gives repeated attempts one stable logical identity, verifies that repeated payloads mean the same thing, and uses observation and conditional state changes so the intended externally visible effect occurs no more than once or converges to one equivalent result.

## Why This Matters

Controllers operate precisely where partial failure is ordinary. They span the Kubernetes API, cloud control planes, databases, message brokers, DNS, identity systems, and human approval. No general atomic transaction covers all of them. A crash can occur before a call, during it, after the provider commits, after the response, or after local status is written. The recovery code cannot infer which boundary was crossed merely from an error.

Duplicate effects have asymmetric costs. An extra read is often harmless; an extra database can cost money and expose data; a repeated “add member” can broaden authority; a repeated increment can exceed quota; a repeated notification can page people; a second deletion aimed at a reused name can destroy a successor object. A sound design classifies each effect rather than attaching one global retry policy.

Idempotency also improves operability. A stable operation identity joins logs, traces, provider activity, audit records, and status. Operators can answer whether an attempt is new, replayed, in progress, completed, inconsistent, or too old to classify. Without that evidence, “retry” becomes a high-risk guess during an incident.

The guarantee has boundaries. A 24-hour key cache cannot protect a request replayed after 25 hours. A provider token scoped only to an account cannot distinguish two tenants unless the controller binds tenant identity. A successful create followed by a failed event publish is not repaired merely because each individual call is idempotent. The chapter therefore treats idempotency as an explicit end-to-end protocol with scope, retention, composition, and retirement rules.

## Prerequisites and Retrieval

Retrieve functions and state transformations, equality and equivalence relations, hashing and canonical serialization, unique identifiers, desired-state control loops, at-least-once delivery, distributed-system partial failure, request/response protocols, HTTP method semantics, optimistic concurrency, compare-and-swap, database transactions, uniqueness constraints, write-ahead records, leases and fencing, work queues, Kubernetes object name/UID identity, `resourceVersion`, JSON Patch tests, Server-Side Apply field ownership, finalizers, tombstones, transactional outbox, message deduplication, timeouts, exponential backoff and jitter, observability, multi-tenancy, security replay, schema evolution, backup/restore, and disaster recovery.

You should distinguish mathematical idempotency from a service guarantee; invocation from logical operation; operation key from object name; fingerprint from secret authentication material; transport retry from business retry; successful replay from identical response bytes; concurrency exclusion from effect deduplication; timeout from rejection; absence now from never created; name from UID; create-or-adopt from create-or-ignore; deduplication retention from data retention; producer outbox from consumer deduplication; idempotent activities from an idempotent workflow; and at-most-one effect from exactly-once execution.

## Learning Objectives

After completing this module, you should be able to:

1. define mathematical, API-level, and end-to-end idempotency and state their scopes;
2. derive stable operation identities and canonical request fingerprints from resource intent;
3. implement atomic reservation, replay, resume, conflict, and expiry behavior for deduplication records;
4. recover from ambiguous external outcomes through observation and create-or-adopt protocols;
5. choose absolute desired assignments, conditional writes, and field ownership for repeated updates;
6. design repeat-safe create, update, delete, event, and multi-step reconciliation effects;
7. size, secure, migrate, restore, and retire idempotency evidence;
8. distinguish idempotent components from an idempotent composed workflow; and
9. verify guarantees with concurrent duplicate, crash-boundary, late-arrival, and key-expiry tests.

## Core Exposition

### Start with the logical operation

One reconcile invocation is not the unit that should be deduplicated. The same desired generation may be reconciled hundreds of times, while one invocation may need several distinct effects. Define a logical operation in domain terms: provision this resource incarnation with this immutable plan; assign this target policy revision; publish this transition fact; revoke this credential version.

The operation remains stable while attempts repeat. Its identity changes only when the domain says a new effect is authorized. Useful key components include tenant, resource kind, immutable resource UID, action, and an intent discriminator such as desired generation, target revision, or plan digest. A key shaped as `tenant/uid/action/generation` is interpretable, but the precise generation rule is domain-specific. A scale target can coalesce generations if only the latest absolute target matters; an invoice issue operation must not silently coalesce two billing periods.

Never key only by a reusable display name. Kubernetes names are unique within resource scope at one moment, while UIDs distinguish historical incarnations. If `database/orders` is deleted and recreated, its new UID must produce new operation identities. Likewise bind tenant and account so an idempotency record cannot cross an authorization boundary.

Avoid nondeterministic inputs. Current time, worker ID, random UUID generated during each attempt, map iteration order, and mutable defaults destroy stability. If randomness is needed for an external name, generate once and durably persist it before the call, or derive a collision-resistant name from immutable identity.

### Bind a key to canonical intent

A key alone prevents neither programmer error nor malicious replay. Compute a fingerprint over exactly the parameters that define the intended effect. Canonicalization must specify field order, absent versus null, normalized units, default expansion, number representation, Unicode handling where relevant, and which metadata is excluded.

Suppose attempt one uses key `k` for 20 GiB and attempt two reuses `k` for 200 GiB. Replaying the first success would violate current intent; executing the second would violate the one-operation meaning of the key. Reject the mismatch with a durable diagnostic. Stripe and AWS service guidance use this same principle: a client token identifies one request intent, and later incompatible parameters are an error rather than a new operation.

Do not put credentials or unrestricted personal data directly in keys or logs. The fingerprint may be a cryptographic digest, but a bare unsalted digest of a small sensitive domain can still leak by guessing. Store or encrypt the minimum evidence needed, authorize reads, and bind the digest to schema revision so canonicalization changes are explicit.

### Reserve before executing

Model a deduplication registry entry as

$$
D(k)=(h,q,r,t_c,t_e,v),
$$

where $k$ is operation key, $h$ fingerprint, $q$ lifecycle state, $r$ result or external identity, $t_c$ creation time, $t_e$ expiry, and $v$ record/schema version. Typical states are `Reserved`, `Submitted`, `Succeeded`, `FailedDefinitive`, `OutcomeUnknown`, and `Quarantined`.

On first sight, atomically insert `Reserved` under a unique constraint. If two workers race, one wins and the other reads the winner. For a repeated key, compare fingerprints before doing work. Completed compatible records replay a semantic result. Active records resume observation. Mismatched records reject. Expired or unreadable records do not justify a blind repeat.

If the mutation and registry share one transactional database, reserve and perform the local mutation in one transaction or enforce a uniqueness constraint on the domain effect. Writing the registry after a non-transactional effect leaves a fatal gap: the process can crash after the effect and before evidence, so a retry sees the key as new.

For an external provider, the controller cannot atomically commit its local record and provider state. Prefer a provider-supplied idempotency token with documented scope and retention. Also assign a stable external name or tags that allow observation. Persist the key, fingerprint, external lookup identity, and request intent before submission. The durable record is a recovery plan, not proof that the provider acted.

### Treat responses as evidence with different strength

A successful provider response is useful evidence, but the controller can lose it before checkpointing. A transport timeout is weaker: it says the client stopped waiting, not that the server rejected or rolled back the request. A definitive validation response can be safe to classify as no effect only if the provider contract says execution did not begin.

Separate response classes:

- **pre-execution rejection**: invalid or unauthorized request with a contract that no mutation began;
- **accepted/in progress**: stable provider operation ID exists and should be observed;
- **success**: effect is reported complete, then independently verify critical postconditions where appropriate;
- **definitive failure**: provider contract establishes the operation ended without the target effect;
- **ambiguous**: timeout, connection reset, process crash, inconsistent replicas, or response that lacks an identity needed for proof.

For ambiguity, observe by operation token, external name, provider tags, or a domain-specific query. Delay and retry observation with jitter because a committed effect may not yet be visible through an eventually consistent listing API. Only submit again when the provider contract, observation window, and retained identity make it safe—and reuse the same operation identity.

### Create or adopt; never create or assume

A stable external name can turn duplicate create into a conflict, but a conflict is not proof of success. The existing object might predate the controller, belong to another resource incarnation or tenant, or embody a different plan.

Create-or-adopt therefore verifies provider account/project, tenant, immutable owner UID, action or plan fingerprint, object type, critical immutable parameters, and any controller-specific signature or tag. If all match, record the provider ID and continue observation. If any fail, stop automatic mutation and expose an identity-collision condition. Do not “repair” a mismatched object until policy explicitly establishes ownership and consequences.

Provider-generated names weaken recovery unless another searchable correlation exists. Random names regenerated per attempt are especially unsafe. A deterministic name can still collide after truncation or normalization; include enough digest entropy, validate returned tags, and test provider naming rules.

### Prefer level-triggered assignments over edge-triggered commands

“Set replicas to 5” is naturally convergent: repeated evaluation of the current value produces 5. “Increase replicas by 1” applies an edge and can produce 6, 7, or more after duplicate attempts. Controllers should calculate an absolute target from desired state and observed state.

Idempotent assignment alone does not prevent lost updates. Two actors can read version 10, derive different replacements, and overwrite each other. Use compare-and-swap, Kubernetes `resourceVersion`, JSON Patch `test`, provider ETags, or scoped Server-Side Apply ownership. On conflict, reread and recompute; do not replay a stale full-object write.

Field ownership makes repeated application safer when actors own disjoint fields, but it is not universal operation deduplication. Forced ownership can steal fields, admission can default or mutate data, and downstream controllers can create effects. Assert only fields the controller truly owns and observe the resulting domain state.

For sets, use stable element identity and desired membership. “Ensure member UID `u` exists” can be idempotent; “append this entry” may duplicate it. For counters, sequence allocation, transfers, and quota consumption, use a domain operation ID or transactional ledger entry rather than pretending the relative command is an assignment.

### Separate queue deduplication from effect idempotency

Controller work queues may coalesce repeated reconcile requests for the same object key. This reduces redundant computation, but it offers no durable effect guarantee. A request can be dequeued, start an effect, crash before acknowledgement, and return later. Different object keys can target one shared external object. Old leaders or callbacks can arrive outside the queue.

Leader election similarly reduces simultaneous workers but does not revoke already-issued provider calls. Resource-version conflicts protect Kubernetes writes, not remote effects. Use queue coalescing and leadership for efficiency and authority, then retain operation identity, provider idempotency, and fencing or preconditions for correctness.

At-least-once attempts are compatible with at-most-one logical effect. They do not create exactly-once execution: code, network requests, reads, logs, and rejected duplicate attempts can execute many times. State the useful guarantee precisely—for example, “within tenant and 72-hour token retention, compatible attempts create no more than one provider database, and later reconciles converge on its verified ID.”

### Make delete a convergent protocol

HTTP semantics classify DELETE as idempotent by intended effect, so repeated deletion of the same target may leave it absent. A controller deletion often contains more: drain traffic, snapshot data, revoke access, delete children, update billing, publish audit, and remove a finalizer. Each obligation needs its own stable identity and completion evidence.

Use immutable external IDs and ownership checks for destructive calls. A request aimed only at a reusable name can delete a new incarnation after the old object disappears. Preserve UID-to-provider-ID binding or a tombstone long enough to classify late calls and callbacks.

`NotFound` can mean already deleted, wrong region/account, stale read, never created, or lost authorization that masks existence. Interpret it using the provider contract and earlier durable evidence. Remove a finalizer only when every required obligation is completed, explicitly abandoned under authorized orphan policy, or transferred to another durable owner. PLAT-056 develops this protocol in detail.

### Handle events with producer and consumer guarantees

A transactional outbox solves one dual-write boundary: commit the domain change and an event record in the same database transaction, then relay the outbox asynchronously. The relay can publish more than once, so messages carry a stable event ID and consumers deduplicate or make their own handlers idempotent.

Do not use the resource’s current generation as the identity of every event. Different facts in one generation need distinct IDs; a repeated representation of the same fact should retain its original ID. Consumers need retention at least as long as broker redelivery, replay, restore, and manual re-drive horizons.

Inbox records can atomically bind message ID to consumer-side mutation when they share a store. For external side effects, the consumer repeats the same operation protocol described here. Broker exactly-once features usually have a defined transactional and time scope; they do not automatically cover a cloud API call or email system.

### Compose effects explicitly

If $f$ and $g$ are each idempotent, their composition need not be idempotent. If they also commute, then

$$
(f\circ g)^2=f\circ g\circ f\circ g=f\circ f\circ g\circ g=f\circ g.
$$

Without commutation, repeating the sequence can change the result. Even commuting final state transformations may produce duplicate irreversible observations such as emails or audit charges. Multi-step workflows need stable identity per step, durable checkpoints, ordering rules, compensation or forward recovery, and an end-to-end invariant.

Consider “ensure database exists, then publish credentials.” Database create may be token-idempotent and secret apply may be field-idempotent, yet a crash between them can leave a database without published credentials. Idempotency limits duplication; it does not give atomic all-or-nothing completion. Reconciliation resumes incomplete obligations from durable evidence.

### Define retention as part of the contract

Deduplication records consume storage, indexes, and privacy budget. Pruning is necessary, but expiry changes correctness. After expiry, the service may treat the same key as new. Define the maximum client retry, broker delay, controller backoff, suspended-resource duration, disaster-recovery replay, and human re-drive horizon. The guarantee is the minimum retained evidence across every participating system.

Under stable arrival rate $\lambda$ unique operations per unit time and average retention $\tau$, Little’s Law gives an idealized mean live-record count

$$
L=\lambda\tau.
$$

This is capacity planning, not a correctness proof. Replication, secondary indexes, result payloads, tombstones, bursts, clock uncertainty, legal holds, and failed-record policy add cost. Partition or compact evidence only after proving late attempts remain harmless through permanent object identity, a domain ledger, or rejection after an operation horizon.

Restore complicates retention. Restoring a registry to yesterday while provider state remains current can resurrect keys as unseen. Backup and disaster-recovery design must reconcile provider inventory, advance epochs, fence stale writers, or conservatively quarantine ambiguity. Clock rollback must not extend or shorten retention accidentally; store absolute timestamps with documented clock assumptions and avoid using expiry as sole authorization.

### Secure the replay surface

An idempotency key is not authorization. Authenticate and authorize every repeated request against current policy, while preserving the historical result needed for safe classification. Bind key scope to tenant, principal or resource owner where appropriate, service, action, and environment.

Attackers can reuse visible keys, probe whether operations exist, or exhaust the registry with unique keys. Use unguessable or server-derived components where suitable, rate and quota controls, bounded payloads, constant-information errors across tenants, encryption, access control, and audit. Never return another tenant’s cached result because a key string collides.

Cancellation and policy change require care. Replaying an earlier success does not necessarily authorize exposing its sensitive result to a now-unauthorized caller. Separate effect classification from result disclosure. An operation can remain “already succeeded” while its credentials or detailed response are withheld or rotated.

### Version and retire the protocol

Key derivation, canonicalization, record schema, provider scope, and retention are persisted protocol decisions. Version them. During rolling upgrades, old and new controllers must derive compatible identities or be fenced by workflow revision. A silent key-form change can submit every in-flight operation again.

Migrate records additively where possible. Persist original key and fingerprint version; map old records before accepting new attempts; test downgrade and restored backups. If a provider shortens token retention or changes parameter-comparison rules, revise the declared guarantee and add local identity/observation before rollout.

Retiring a controller means more than stopping reconciles. Drain or transfer active operations, retain searchable mappings for the late-response horizon, fence old credentials and leaders, disposition finalizers, preserve required tombstones/audit, and document who classifies delayed callbacks. Removing the registry while attempts remain possible converts known duplicates into apparently new work.

### Verify crashes, concurrency, and time

Build a crash matrix around every boundary: before reservation; after reservation; before request bytes leave; after provider commit but before response; after response but before result checkpoint; after checkpoint but before status; and during deletion or compensation. Restart with the same and a different worker version.

Run concurrent identical attempts and same-key/different-fingerprint attempts. Delay responses beyond timeouts. Return conflicts, stale reads, `NotFound`, and duplicate callbacks. Delete and recreate the Kubernetes object with the same name and a new UID. Advance beyond local and provider retention. Restore an old deduplication backup against current provider state. Partition observation from mutation endpoints.

Assertions should inspect domain outcomes, not only HTTP codes or record counts: number of provider objects owned by UID, target configuration, absence of unauthorized adoption, number and identity of emitted events, finalizer obligations, and preserved ambiguity. Fault injection and model-based traces supplement real provider contract tests; they do not replace them.

## Definitions and Notation

Let $X$ be the relevant state space and $f:X\to X$ an intended state transformation. It is **idempotent** when $f^n(x)=f(x)$ for every $x\in X$ and integer $n\ge 1$. The equality can be a declared semantic equivalence $\sim$ rather than byte equality: $f(f(x))\sim f(x)$.

Let $R$ be immutable resource identity, including tenant and UID; $a$ an action; $i$ the intent revision or plan digest; and $K$ a key-derivation function. Then $k=K(R,a,i)$ identifies one logical operation. Let $C$ canonicalize intent-bearing request $p$ and $H$ be a collision-resistant digest; $h=H(C(p))$ is the fingerprint. Hash collision resistance lowers accidental or adversarial collision risk but does not correct an incomplete canonical field set.

Let $D(k)=(h,q,r,t_e,v)$ be a durable registry record. Define the decision function:

$$
\operatorname{decide}(k,h')=
\begin{cases}
\text{reserve and start}, & D(k)\text{ absent and safely classifiable};\\
\text{resume or replay}, & h'=h\text{ and }q\text{ active or completed};\\
\text{reject mismatch}, & h'\ne h;\\
\text{observe or quarantine}, & q\text{ unknown, expired, or inconsistent}.
\end{cases}
$$

An **attempt ID** identifies one execution for telemetry; it must not replace $k$. A **provider operation ID** is an external system’s correlation handle. An **object identity** names the effect target. One logical operation may use all three.

**At-most-once effect** means no more than one domain effect in the stated scope. **At-least-once attempt** means retry scheduling eventually executes one or more attempts under stated availability assumptions. **Exactly-once execution** would mean precisely one execution, which ordinary distributed retries cannot establish. A useful controller generally seeks at-least-once attempts plus idempotent or deduplicated effects and eventual observation.

The **retry horizon** $T_r$ is the latest legitimate repeated attempt; **evidence horizon** $T_e$ is how long deduplication/identity evidence remains trustworthy. Safe replay classification requires $T_e\ge T_r$ plus clock and delivery margin, unless a permanent domain invariant replaces the expiring record.

## Mechanisms, Invariants, or Proof Structure

### Protocol

1. Read the latest desired state, immutable UID, tenant, deletion state, and existing operation record.
2. Derive a versioned logical operation key from domain intent; never generate it afresh per attempt.
3. Canonicalize intent-bearing parameters and compute a fingerprint.
4. Atomically insert a reservation, or load the record that won the key race.
5. Reject key/fingerprint mismatch before any external effect.
6. For completed records, reauthorize disclosure and replay a semantic result or continue postconditions.
7. For active/unknown records, observe by stable operation/object identity before submission.
8. Submit only when the state and provider contract permit, reusing the same token and target identity.
9. Persist provider correlation and verified outcome with conditional writes; on conflict, reread.
10. Reconcile every downstream obligation—status, secret, event, cleanup—under its own stable identity.
11. Retain evidence through all retry/replay horizons, then retire it with documented late-arrival behavior.

### Core invariants

- **binding:** each accepted $k$ maps to exactly one canonical fingerprint version and intent;
- **scope:** tenant, environment, resource incarnation, action, and provider account cannot collide silently;
- **single reservation:** a unique constraint or equivalent chooses one first writer;
- **unknown preservation:** missing response never becomes “no effect” without contractual evidence;
- **adoption safety:** an existing object is accepted only if all authoritative ownership and intent predicates hold;
- **conditional advancement:** local state advances from the version and generation actually observed;
- **obligation completeness:** completing one effect cannot erase unfinished events, secrets, cleanup, or status obligations;
- **retention coverage:** evidence outlives every supported delayed attempt and restore scenario;
- **version compatibility:** every active worker understands or safely stops on stored key/fingerprint schema;
- **bounded disclosure:** cached results do not bypass current authorization or expose cross-tenant data.

### Proof sketch and its boundary

Assume: key derivation is deterministic and injective over authorized logical operations in scope; fingerprint canonicalization distinguishes different intents; the registry enforces one record per key; every effect path passes through the decision function; provider execution deduplicates the key or external identity permits safe create-or-adopt; evidence remains available for all attempts; and implementations satisfy ownership and conditional-write checks.

For the first compatible attempt, the unique reservation authorizes at most one new provider identity. Every later compatible attempt reaches the same record. If completed, it replays/continues without a new effect. If active or ambiguous, it observes the same provider identity; any resubmission uses the same provider token/identity. An incompatible attempt is rejected. Therefore attempts within the stated scope and evidence horizon converge on at most one accepted logical effect.

This is a proof sketch of the model, not proof of a deployment. It fails if a code path bypasses the registry, a provider ignores tokens, names collide without verified tags, evidence expires early, restore loses records, canonicalization omits a field, or a controller adopts mismatched state. Availability is separate: a system can preserve at-most-one effect by doing nothing forever.

### Executable design inventory

The following synthetic inventory checks ten protocol designs against ten required controls. It is a pedagogical classifier, not evidence about any real provider or controller.

<!-- bijux-verify: {"id":"idempotency-design-inventory","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"safe=2\nambiguous=6\nunsafe=2\n"}} -->
```python
required = {
    "stable_key", "fingerprint", "atomic_reservation", "provider_identity",
    "observe_unknown", "conditional_update", "ownership_check",
    "retention", "tenant_scope", "crash_tests",
}

designs = {
    "database": required,
    "dns": required,
    "random-name": required - {"stable_key", "provider_identity"},
    "late-expiry": required - {"retention"},
    "blind-adopt": required - {"ownership_check", "tenant_scope"},
    "post-write-record": required - {"atomic_reservation"},
    "timeout-retry": required - {"observe_unknown"},
    "etag-missing": required - {"conditional_update"},
    "weak-fingerprint": required - {"fingerprint"},
    "untested": required - {"crash_tests"},
}

counts = {"safe": 0, "ambiguous": 0, "unsafe": 0}
for controls in designs.values():
    missing = required - controls
    category = "safe" if not missing else ("ambiguous" if len(missing) == 1 else "unsafe")
    counts[category] += 1
for category in ("safe", "ambiguous", "unsafe"):
    print(f"{category}={counts[category]}")
```

The inventory deliberately labels a one-control omission “ambiguous,” not “almost safe.” The impact depends on which control is missing and the domain. Real verification must exercise provider semantics, concurrency, crash recovery, authorization, restore, and externally observed effects.

## Alternatives and Trade-Offs

### Natural assignment versus deduplication registry

Absolute assignment to a strongly identified object is simple and often durable. It works for `replicas=5`, desired labels, or replacing a policy document. It does not cover append, increment, one-time publication, resource creation with generated identity, or mixed effects. Use natural convergence where the domain supports it; add explicit operation records where it does not.

### Client-generated identity versus provider idempotency token

A deterministic external name remains discoverable after local record loss, but naming limits and user collision complicate it. A provider token can preserve native response replay and concurrent request handling, but its scope and retention may be shorter than controller recovery. Strong designs use both stable token and observable owner identity when practical.

### Local registry versus provider-only guarantee

A local registry gives controller-visible lifecycle, result, audit, and cross-provider coordination. It adds storage, transactions, schema migrations, cleanup, and disaster-recovery coupling. Provider-only keys reduce local state but can become opaque, expire unexpectedly, and fail to cover downstream effects. Select the minimum evidence that still supports recovery and incident explanation.

### Cached response versus recomputed response

Returning the exact original response is convenient when clients need created IDs. Recomputing from current state avoids retaining sensitive or stale payloads. The semantic contract should identify stable fields and permitted changes. Reauthorize either path; idempotency does not promise that an expired credential or current status remains identical.

### Generation key versus plan-digest key

Generation is cheap and available, but metadata-only or defaulting behavior can complicate what it means, and harmless edits may create unnecessary new operations. A plan digest represents effect intent more precisely but needs stable canonicalization and versioning. Often store both: UID/generation for traceability and a versioned plan digest for semantic binding.

### Fail closed versus automated repair after mismatch

Quarantine on identity or fingerprint mismatch protects other tenants and unknown resources but may block recovery. Automated mutation restores liveness faster but can seize or corrupt an object. Default to fail closed for ownership ambiguity; offer a privileged, audited adopt/replace procedure with explicit evidence and consequence.

### Permanent ledger versus expiring cache

A permanent domain ledger gives strong replay history but accumulates cost and sensitive data. An expiring cache bounds cost but bounds the guarantee. Compact old records into minimal tombstones, permanent domain uniqueness constraints, or cryptographic audit only when late actions can still be classified safely.

### Optimistic concurrency versus serialized worker

A single worker reduces ordinary races but becomes a bottleneck and cannot contain stale requests after failover. Optimistic concurrency scales and detects stale local writes, at the cost of retries and careful recomputation. Use serialization for efficiency where helpful; use versions, fencing, and idempotency for correctness.

### Transactional outbox versus direct publish

Direct publish is low latency and low storage but leaves a crash gap with the domain update. An outbox closes that local dual-write gap and supports replay, while requiring a relay, retention, and idempotent consumers. It does not make external consumer effects atomic.

### Provider lookup versus resubmission

Lookup avoids duplication under ambiguous outcomes but may be slow, costly, stale, or unavailable. Resubmission with a documented stable provider key can be safe and faster. Combine them based on provider guarantees: observe first when token retention or effect identity is uncertain; resubmit the same key when native deduplication is authoritative.

### One workflow key versus per-step keys

One key is easy to correlate but cannot distinguish repeated legitimate steps or safely resume partial work. Per-step keys isolate effects and retries but require durable workflow structure and end-to-end obligation tracking. Use a workflow ID plus stable activity keys derived from step meaning and attempt semantics.

### Delete record immediately versus tombstone

Immediate deletion minimizes storage and privacy exposure but makes late callbacks and name reuse dangerous. Tombstones retain classification evidence at operational and compliance cost. Store the minimum immutable identity, outcome, expiry, and audit needed for the late-arrival horizon.

## Failure Modes and Misconceptions

1. **“The reconcile function is idempotent because it can run twice.”** Repeatability is a claim to prove across every effect and crash boundary, not a function signature.
2. **“PUT or DELETE makes the workflow idempotent.”** RFC 9110 describes intended semantics of one HTTP resource method; surrounding notifications, billing, generated children, and reused names can still duplicate or misapply effects.
3. **“A UUID per attempt prevents duplicates.”** It guarantees different identities and therefore defeats deduplication. Generate once per logical operation and persist or derive it.
4. **“The object name is stable identity.”** Names can be reused. Bind Kubernetes UID and provider owner evidence.
5. **“A 409 conflict means our create succeeded earlier.”** It proves only that something conflicts. Retrieve and verify ownership and fingerprint.
6. **“Timeout means the provider failed.”** The provider may have committed and the response may be lost. Mark unknown and observe.
7. **“The provider token is enough forever.”** Tokens have scope, parameter rules, and retention. Controller retry and restore horizons may exceed them.
8. **“Same key means return the old result.”** First compare canonical intent and current disclosure authorization.
9. **“Write the dedup record after success.”** A crash between effect and record makes the duplicate appear new.
10. **“Leader election provides exactly once.”** A previous leader’s remote call can outlive its lease; callbacks and queues also duplicate.
11. **“Work-queue coalescing protects effects.”** It is an in-memory scheduling optimization, not durable cross-system deduplication.
12. **“Set and increment are equivalent after observation.”** A lost response to increment makes the next safe value unknowable without an operation ledger.
13. **“Server-Side Apply solves all concurrency.”** It manages field ownership and conflicts; it does not deduplicate provider calls or make forced ownership safe.
14. **“NotFound proves deletion completed.”** It may reflect scope, permission, replication, or identity error. Interpret it against recorded identity and provider semantics.
15. **“Two idempotent steps form an idempotent workflow.”** Composition also needs ordering/commutation, checkpoints, and complete obligations.
16. **“Cache expiry is only a cost setting.”** It is the end of a correctness guarantee unless another durable invariant remains.
17. **“Restoring the controller database restores truth.”** Provider state may be newer; stale evidence can authorize duplicate work.
18. **“Exactly-once effect means exactly-once execution.”** Attempts and requests can execute repeatedly even when one domain effect is preserved.
19. **“A hash proves requests are the same.”** Only the included canonical fields and collision assumptions support that conclusion.
20. **“Stopping the controller retires operations.”** Late callbacks, queued attempts, credentials, finalizers, and provider work remain until explicitly drained or transferred.

## Worked Examples

### Example 1

**Situation.** Tenant `north` has Kubernetes object name `orders`, UID `8f2`, generation 7, and immutable provider-plan digest `a91`. The controller may restart during provisioning. What should identify the logical effect?

**Reasoning.** The reconcile attempt ID is unsuitable because it changes. The name is unsuitable because it can be reused. A key such as `prod/north/database/8f2/provision/a91` binds environment, tenant, kind, UID, action, and immutable plan. Generation 7 remains recorded for traceability, but if generations 6 and 7 canonicalize to the same immutable plan, the digest deliberately coalesces them. The fingerprint covers provider account, region, engine, version, size, encryption identity, and plan schema revision.

**Conclusion.** Persist and reuse the derived operation key and versioned fingerprint; generate a separate attempt ID only for telemetry.

### Example 2

**Situation.** The first call under key `k9` requests a 20 GiB encrypted volume. A buggy retry under `k9` requests 200 GiB and a different key-management identity.

**Reasoning.** The registry contains fingerprint $h_{20}$. Canonicalizing the retry produces $h_{200}\ne h_{20}$. Replaying the old result would misrepresent the requested effect; executing the new request would let one key mean two effects. The decision function rejects before provider mutation and exposes a stable `IdempotencyKeyReuse` reason. The controller must derive a new authorized operation identity or correct the bug.

**Conclusion.** Same key plus different fingerprint is a conflict, never a cache hit or automatic new operation.

### Example 3

**Situation.** A provider commits creation of `db-8f2`, but the response is lost and the controller crashes with its local record at `Submitted` and no provider ID.

**Reasoning.** The next reconcile loads the same key and does not declare failure. It queries by stable external name and owner tags. The listing endpoint is eventually consistent, so it retries observation within the documented visibility window. It finds one object whose tenant, UID, plan fingerprint, and provider account all match, records its immutable provider ID through a conditional update, and verifies readiness. If none appears after the safe observation window, it may resubmit the same provider idempotency token according to the provider contract.

**Conclusion.** Outcome ambiguity is resolved by stable observation and same-key resubmission, not a fresh create.

### Example 4

**Situation.** Creating deterministic name `bucket-orders-8f2` returns a conflict. The existing bucket has tenant `south` and owner UID `44c`.

**Reasoning.** Name equality establishes collision, not ownership. Both tenant and UID contradict the expected object. Updating tags or deleting the bucket would cross an authorization boundary. The controller records collision evidence, sets `IdentityCollision=True`, stops automatic effects for this operation, and requires a privileged resolution that selects a different identity or proves transfer.

**Conclusion.** Create-or-adopt must fail closed on any authoritative ownership mismatch.

### Example 5

**Situation.** Desired replicas change from 4 to 5. The provider offers `increment(1)` and `setCapacity(5)`. A response can be lost.

**Reasoning.** If `increment(1)` commits and the response disappears, repeating it yields 6. A local “sent” flag cannot prove the provider result after a crash. Repeating `setCapacity(5)` leaves capacity 5, subject to provider identity and concurrency semantics. The controller reads the latest desired target and current provider version, then conditionally assigns 5. A conflict triggers reread and recomputation.

**Conclusion.** Express desired levels as absolute assignments; use operation ledgers for truly relative domain actions.

### Example 6

**Situation.** On integer state, let $f(x)=0$ and $g(x)=1$ if $x=0$, otherwise $g(x)=x$. Are $f$, $g$, and $f\circ g$ idempotent?

**Reasoning.** $f(f(x))=0=f(x)$, so $f$ is idempotent. For $g$, zero becomes one and any nonzero remains itself; applying $g$ again changes nothing, so $g$ is idempotent. But $(f\circ g)(x)=f(g(x))=0$. With this order the composition is idempotent. Reverse the order: $(g\circ f)(x)=g(0)=1$, also idempotent here, so this pair is not a counterexample. Choose instead set transformations on strings: $f$ removes every trailing `b`, while $g$ appends `b` only when absent. Each is idempotent. Applying $f\circ g$ always removes the newly ensured `b`, so it is idempotent; applying $g\circ f$ ensures one `b`, also idempotent. Again they converge. This failed search demonstrates that examples must be checked, not asserted. A valid counterexample on three states uses $f=(0\mapsto1,1\mapsto1,2\mapsto2)$ and $g=(0\mapsto0,1\mapsto2,2\mapsto2)$. Both are idempotent, but $h=f\circ g$ maps $0\mapsto1$, $1\mapsto2$, and $2\mapsto2$; hence $h(h(0))=2\ne1=h(0)$.

**Conclusion.** Individually idempotent transformations do not guarantee idempotent composition; order and interaction require proof or end-to-end testing.

### Example 7

**Situation.** A platform accepts 200,000 unique effect operations per second at peak-normalized steady rate and retains deduplication evidence for 24 hours. Estimate the mean live records under the simplified stable model.

**Reasoning.** With $\lambda=200{,}000$ records/second and $\tau=24\times60\times60=86{,}400$ seconds,

$$
L=\lambda\tau=200{,}000\times86{,}400=17{,}280{,}000{,}000.
$$

At even 200 bytes of primary record data, raw primary storage is about 3.456 TB before indexes, replication, allocator overhead, results, tombstones, and bursts. Partitioning and compact result representations matter, but shortening retention is a correctness decision tied to retry horizons.

**Conclusion.** High-rate idempotency requires explicit capacity architecture; retention cannot be tuned as a cache hit-rate preference alone.

### Example 8

**Situation.** Workers A and B receive the same object and derive identical $k,h$. Both attempt to provision.

**Reasoning.** A conditional insert under a unique key permits A to create `Reserved`; B receives a uniqueness conflict and loads A’s record. A submits provider token $k$. Before checkpointing the response, A loses leadership. B sees `Submitted`, queries the provider by $k$ or deterministic identity, and records the verified provider ID using record version 2. A later tries to write using version 1 and loses compare-and-swap. It discards its stale response and rereads. Both may execute code and provider request handling, but one logical provider object is accepted.

**Conclusion.** Atomic reservation, provider identity, observation, and conditional checkpointing contain concurrent and stale workers together.

### Example 9

**Situation.** Resource `cache/blue` UID `old` was deleted. A delayed delete request refers only to provider name `blue`. Meanwhile a new Kubernetes resource with UID `new` has adopted a new provider object with the same display name.

**Reasoning.** A name-only request cannot distinguish incarnations and could delete the successor. The original delete protocol should persist immutable provider object ID and owner UID in a tombstone and condition the provider delete on that identity or owner tag. If the provider cannot condition deletion, the controller must retrieve and verify before acting, and quarantine if identity is uncertain. The tombstone remains through the maximum queued/late-call horizon.

**Conclusion.** Repeat-safe deletion depends on immutable incarnation identity and retained evidence, not eventual absence of a reusable name.

### Example 10

**Situation.** The local operation database is restored to midnight, but cloud provider state is current at noon. A 09:00 database creation record is absent locally, and the object still exists remotely.

**Reasoning.** Treating the missing record as unseen would duplicate the database. Disaster recovery enters a fenced recovery epoch: old workers and credentials are disabled; the controller inventories provider objects by signed owner UID and plan tags; it reconstructs or quarantines records; only then can new creates proceed. Objects with ambiguous tags are not adopted automatically. The team verifies that provider token retention still covers restored operations and extends local tombstones where it does not.

**Conclusion.** Registry restore must reconcile against external truth before absence can authorize a new effect.

## Cross-Program Connections

1. **API & Service Engineering:** HTTP method idempotency, request IDs, conditional requests, long-running operations, error contracts, and replayed responses define the service boundary controllers consume.
2. **Distributed Systems:** partial failure, impossibility of inferring remote outcome from timeout, at-least-once delivery, consensus-backed uniqueness, and fencing explain why the protocol needs durable evidence.
3. **Database Systems:** unique constraints, compare-and-swap, transactional inbox/outbox, ledgers, isolation, and write-ahead records implement local atomic boundaries.
4. **Data Structures Engineering:** canonical maps, sets with stable keys, hashes, indexes, Bloom filters, and log compaction shape high-volume deduplication stores and their false-positive risks.
5. **Security Engineering:** tenant binding, authorization on replay, key guessing, registry exhaustion, sensitive cached results, audit, and credential fencing make idempotency a security boundary.
6. **Reliability Engineering:** timeouts, bounded exponential backoff with jitter, retry budgets, fault injection, ambiguous-outcome runbooks, and recovery objectives govern operation under failure.
7. **Software Testing:** property-based traces, concurrency schedules, crash-point injection, model checking, provider contract tests, and mutation testing challenge the at-most-one-effect invariant.
8. **Formal Methods:** state transformers, equivalence, invariant induction, composition, commutativity, and counterexamples clarify what is actually proved.
9. **Data Engineering:** event replay, checkpoint restoration, watermark and retention horizons, deduplicating consumers, and backfills reuse the same identity-versus-attempt distinction.
10. **Systems Engineering:** boundaries, assumptions, hazard analysis, independent protection layers, lifecycle evidence, and retirement prevent a local mechanism from being mistaken for a system guarantee.

## References

1. IETF. [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html). 2022. See safe and idempotent methods and retry implications.
2. IETF. [RFC 6902: JavaScript Object Notation (JSON) Patch](https://www.rfc-editor.org/rfc/rfc6902.html). 2013. Defines patch operations including test preconditions.
3. Amazon Web Services. [Making retries safe with idempotent APIs](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/). Retrieved 2026-09-02.
4. Amazon Web Services. [Timeouts, retries, and backoff with jitter](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/). Retrieved 2026-09-02.
5. Amazon Web Services Prescriptive Guidance. [Transactional outbox pattern](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html). Retrieved 2026-09-02.
6. Kubernetes. [Kubernetes API Concepts](https://kubernetes.io/docs/reference/using-api/api-concepts/). Retrieved 2026-09-02. Covers identity, concurrency, patch preconditions, and dry-run behavior.
7. Kubernetes. [Object Names and IDs](https://kubernetes.io/docs/concepts/overview/working-with-objects/names/). Retrieved 2026-09-02. Distinguishes names from lifetime-unique UIDs.
8. Kubernetes SIG Architecture. [API Conventions](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md). Retrieved 2026-09-02.
9. Kubernetes. [Server-Side Apply](https://kubernetes.io/docs/reference/using-api/server-side-apply/). Retrieved 2026-09-02. Documents field managers, ownership, and conflicts.
10. controller-runtime. [Package reconcile documentation](https://pkg.go.dev/sigs.k8s.io/controller-runtime/pkg/reconcile). Retrieved 2026-09-02. Documents reconcile requests, queue behavior, requeue, and errors.
11. Google. [AIP-155: Request identification](https://google.aip.dev/155). Retrieved 2026-09-02. Specifies request IDs for duplicate detection and idempotency.
12. Stripe. [Idempotent requests](https://docs.stripe.com/api/idempotent_requests). Retrieved 2026-09-02. Documents key retention, parameter comparison, and response replay behavior.
13. Pat Helland. [Life Beyond Distributed Transactions: An Apostate's Opinion](https://www.cidrdb.org/cidr2007/papers/cidr07p15.pdf). CIDR, 2007. Develops durable identity and workflow reasoning beyond distributed transactions.
14. Martin Kleppmann. *Designing Data-Intensive Applications*. O'Reilly Media, 2017. See distributed transactions, delivery semantics, idempotence, logs, and fault reasoning.

## Exercises

### Exercise 1

A controller log contains reconcile request `namespace/orders`, attempt UUID `a-77`, Kubernetes UID `u-9`, desired generation 12, plan digest `p-4`, provider operation `op-88`, and provider object `db-301`. State the role of each identifier and propose a logical provisioning key.

### Exercise 2

For key $k$, worker A inserts fingerprint $h_1$ and submits a request. Its response is lost. Worker B arrives with $k,h_1$. Worker C arrives with $k,h_2$. Describe the safe decision for B and C, including what evidence B needs before completion.

### Exercise 3

A controller writes `Succeeded` only after a provider create returns. Fault injection crashes the process immediately after provider commit. On restart it generates a new random provider name and creates again. Identify the violated invariants and design the smallest durable correction.

### Exercise 4

Provider A supports `setCapacity(target, etag)` but no idempotency token. Provider B supports `addCapacity(delta, token)` with 48-hour token retention. Design reconciliation for a desired capacity resource that may remain suspended for seven days. Compare safety and retention requirements.

### Exercise 5

A platform must send one legally required notice when a resource crosses a policy threshold. Events can replay after disaster recovery 90 days later; the email provider deduplicates tokens for only 24 hours. Design an end-to-end protocol, including domain identity, transaction boundary, consumer behavior, disclosure/security, and retirement.

## Answers to the Exercises

### Answer 1

`namespace/orders` is a queue/API lookup key and is reusable across incarnations. `a-77` identifies one execution attempt for telemetry. `u-9` is immutable Kubernetes resource-incarnation identity. Generation 12 identifies a revision of desired state but may or may not equal a distinct effect. `p-4` identifies canonical immutable provisioning intent. `op-88` is the provider’s asynchronous operation handle. `db-301` is the resulting provider object identity. A suitable key is `tenant-or-cluster-scope/u-9/provision/p-4`, with environment and provider account included where collision is possible. Store generation 12, `op-88`, and `db-301` as correlated evidence rather than substituting any one for the logical key.

### Answer 2

B loads the existing record because its key and fingerprint match. It must not assume failure or create under a fresh identity. It observes by the persisted provider token, operation handle, deterministic target, or verified owner tags. If it finds the effect, it checks tenant, UID, fingerprint, and relevant postconditions before conditionally recording completion. If the provider still reports in progress or visibility is uncertain, B retains an active/unknown state and retries observation with bounded jitter. Same-key resubmission is allowed only under the provider’s documented guarantee. C has $h_2\ne h_1$ and must be rejected before any effect with a stable mismatch reason. Neither the age of the request nor worker identity changes this binding.

### Answer 3

The design violates stable operation identity, reserve-before-effect, unknown-outcome preservation, and observable provider identity. Post-success recording leaves an effect-to-record crash gap; a new random name makes retry a distinct create. The smallest durable correction is to derive or persist one operation key and external lookup name before submission, atomically reserve that key locally, pass the same token if the provider supports it, and attach tenant/UID/fingerprint ownership metadata. After restart, load `Reserved`/`Submitted`, query the provider by stable identity, verify ownership and plan, and adopt or continue. If the provider cannot search, the controller needs a provider-supported idempotency token or must classify the API as unsafe for automatic retry and quarantine ambiguous outcomes.

### Answer 4

For Provider A, reconciliation reads current capacity and ETag, calculates the absolute desired target, and calls `setCapacity(target, etag)`. A lost response is followed by reread: target capacity means convergence; an ETag conflict means reread/recompute. The assignment is naturally idempotent, though side effects such as billing notifications must be evaluated separately.

For Provider B, `addCapacity` is relative, so the controller derives one stable operation token for each authorized delta and keeps a ledger of base/target/operation. Reusing the token within 48 hours prevents duplicate additions. A resource suspended seven days exceeds native retention: blind resubmission can add twice. The platform must either preserve an independently queryable provider operation/object ledger that proves whether the delta applied, refresh/complete before expiry under a documented protocol, translate desired capacity into a safe absolute API, or stop and require manual reconciliation after the ambiguity horizon. Local retention alone cannot extend the provider’s guarantee.

### Answer 5

Define the legal notice as a domain fact with immutable identity such as `tenant/resource-UID/policy-revision/threshold-crossing-sequence`, not an email attempt. In the transaction that records the qualifying threshold crossing, insert an outbox row under a unique event ID. A relay may publish it repeatedly. The notification consumer atomically inserts an inbox/notice ledger entry and tracks `Pending`, provider submission ID, `Sent`, or `OutcomeUnknown`.

Because provider token retention is 24 hours but replay is 90 days, provider deduplication alone is insufficient. The consumer retains its notice ledger and message identity beyond 90 days, uses a stable provider token and message fingerprint, and records a provider message ID or another queryable delivery identity before acknowledging completion. On ambiguous response it queries status; if the provider offers no durable lookup beyond 24 hours, automatic resubmission after that horizon risks a duplicate legally required notice and must follow an explicit policy—such as a permanent provider-side recipient/event header recognized by a controlled gateway, or human/legal review—rather than silently send.

Authorize event and ledger access by tenant, minimize notice content in keys, encrypt sensitive result data, and reauthorize any status disclosure. Retain a minimal immutable sent/tombstone record through the 90-day replay horizon plus recovery margin and any legal retention; retire provider credentials and relay routes only after queues, backups, and callbacks can no longer reintroduce the event. Verification includes concurrent relay duplicates, crash after send, delayed provider response, 91-day restore, cross-tenant key collision, and inspection that exactly one notice fact—not exactly one code execution—was accepted.
