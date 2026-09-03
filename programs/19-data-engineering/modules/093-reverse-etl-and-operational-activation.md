---
module_id: DE-093
program: Data Engineering
level: 2
module_number: 93
title: Reverse ETL and Operational Activation
status: complete
last_verified: 2026-09-03
---

# Reverse ETL and Operational Activation

## One-Page Review

### Governing question

How can governed analytical state be translated into bounded, attributable, reversible operational effects in CRMs, support systems, advertising platforms, messaging tools, finance applications, product services, and partner APIs without treating warehouse rows as commands, overwriting destination-owned truth, violating consent, duplicating actions, or declaring success before destination state is reconciled?

### Essential definitions

- **Reverse ETL** synchronizes modeled data from a warehouse or analytical platform into operational destinations.
- **Operational activation** uses data-derived decisions, attributes, audiences, or signals to change an external system or workflow.
- A **sync model** defines the source population, grain, stable identity, fields, eligibility, and version sent to one activation.
- A **destination object** is the remote record, list membership, event, task, or resource affected by activation.
- A **match key** maps one source entity to the intended destination identity; it is part of correctness and authority, not only configuration.
- **Field ownership** states which system or role may authoritatively create, replace, merge, clear, or leave each destination field.
- A **sync mode** defines effects such as append, update, upsert, mirror, add-to-list, remove-from-list, or delete.
- **Desired state** describes what the destination should contain; an **event/command** requests one transition. Their retry and deletion semantics differ.
- A **change set** classifies source rows as create, update, remove/delete, or unchanged relative to a prior authoritative comparison.
- **Idempotency** means repeating the same logical operation produces no additional effect beyond the first successful application.
- A **destination receipt** records remote ID, operation identity, accepted/rejected status, error, version or timestamp, and verification evidence.
- **Partial success** occurs when a batch accepts some items and rejects, delays, or ambiguously handles others.
- A **suppression** prevents activation for a subject, purpose, channel, destination, or period because of consent, policy, safety, holdout, or operational state.
- **Activation freshness** is elapsed time from the authoritative source/decision boundary to the effective destination state.
- **Reconciliation** compares eligible desired state and destination-observed state under a common mapping and classifies missing, extra, stale, duplicate, conflicted, suppressed, and unknown items.
- A **kill switch** stops new effects at a bounded control point while preserving evidence and safe recovery.

### Central model, mechanism, or theorem

For source model state $S_v(t)$, eligibility and suppression policy $P_p(t)$, mapping $m_v$, and field projection $\pi_v$, desired destination state is

$$
D^*(t)=\{m_v(k)\mapsto\pi_v(r):r\in S_v(t),\ P_p(r,t)=eligible\}.
$$

The observed destination $D(t)$ may differ because of queueing, partial failure, remote edits, rate limits, or eventual consistency. Reconciliation partitions the comparison:

$$
Keys(D^*\cup D)=matched\mathbin{\dot\cup}missing\mathbin{\dot\cup}extra\mathbin{\dot\cup}stale\mathbin{\dot\cup}conflicted\mathbin{\dot\cup}unknown.
$$

A sync is complete for a boundary only when every in-scope item has a terminal, policy-valid outcome or explicit bounded exception. “API request accepted” is not necessarily “remote effect visible.” For command-like irreversible effects, source membership must not automatically replay the action; a stable command identity and state machine are required.

### Critical invariants

- Every activation has an owner, purpose, lawful/contractual policy basis where applicable, destination, object, source boundary, model/mapping version, consumers, and kill switch.
- Source grain and match key are unique, stable, tenant-scoped, normalized, and verified against destination identity before any mutation.
- Identity merges, splits, recycling, aliasing, email/phone normalization, and destination reassignment have explicit rules and evidence.
- Each destination field has one authoritative writer or a documented merge/conflict policy; warehouse syncs do not overwrite destination-owned edits silently.
- Desired-state syncs, membership syncs, append-only events, and one-time commands use distinct protocols.
- Creates, updates, clears, removals, deletes, unchanged rows, suppressions, and unknowns remain distinct.
- Consent, purpose, channel preference, residency, age/eligibility, legal hold, frequency cap, safety block, and holdout are evaluated at effect time, not only model-build time.
- Dry run reports exact target IDs, operation classes, changed fields, removals, volume/cost, policy blocks, and unusual deltas without exposing sensitive values.
- Batches are bounded, rate-aware, deadline-aware, idempotent, retryable per item, and resumable without replaying successful irreversible effects.
- Remote accepted, completed, visible, rejected, retriable, permanent, conflicted, and unknown outcomes are not collapsed into success/failure.
- Source, extracted, queued, attempted, accepted, effective, and reconciled positions/times remain observable.
- Destination schemas, enums, required fields, types, rate limits, quotas, authentication, versions, and error taxonomies are contract-tested and monitored.
- Backfills and resyncs use blast-radius approval, canaries, cohort expansion, rate budgets, suppression re-evaluation, and rollback/compensation boundaries.
- Deletes and audience removals propagate deliberately; absence from a current query is not interpreted as deletion unless mirror semantics prove the prior membership set.
- Reconciliation includes destination-observed state or trustworthy receipts and never relies only on source counts or request transport.
- Sensitive fields are minimized, transformed only under approved policy, protected in staging/logs/dead letters, and deleted across source, vendor, and backup lifecycles.
- Activation effectiveness is separated from sync reliability; delivery does not prove causal business lift.
- Every external side effect and policy decision is attributable without logging raw payloads or credentials unnecessarily.

### Common failures

Common failures include matching on mutable email without tenant scope; allowing two syncs to own the same CRM field; upserting a nonunique source grain; interpreting absent rows as destination deletion; retrying one-time coupon or message commands; considering HTTP 202 complete; losing per-item errors inside a successful batch; updating consent only in tomorrow's warehouse model; clearing a field when null meant “do not manage”; overwriting newer destination edits; blasting a full resync after state corruption; ignoring rate-limit reset and retry headers; storing sensitive payloads in dead letters; counting accepted audience rows as campaign impact; and turning off a sync without removing previously activated state.

### Compact example

A governed customer model produces one row per `(tenant, customer_id)` with CRM tier, support risk, and an advertising suppression flag. The sync maps through an immutable destination crosswalk, owns only namespaced CRM fields, evaluates current consent immediately before action, and diffs against its last confirmed desired-state generation. It canaries 100 changes, sends bounded idempotent batches, preserves per-item receipts, retries only ambiguous/retriable items, and reads back or consumes remote status to reconcile. A consent withdrawal removes audience membership urgently even if the general warehouse refresh is delayed. CRM agents' notes remain destination-owned.

### Connections

[DE-035](035-incremental-models.md) supplies changed-set logic, [DE-049](049-run-metadata-and-operational-state.md) supplies execution states, [DE-055](055-delivery-semantics-in-streaming-pipelines.md) and [DE-056](056-exactly-once-effects.md) distinguish delivery from effect, [DE-060](060-handling-late-duplicate-and-out-of-order-events.md) governs correction, [DE-073](073-reconciliation-tests.md) compares state, [DE-076](076-data-contracts.md) defines source/destination contracts, [DE-085](085-classification-and-sensitive-data.md) and [DE-086](086-access-control-for-analytical-data.md) constrain export, [DE-088](088-retention-and-deletion.md) governs removal, [DE-089](089-auditability-and-provenance.md) supplies receipts, and [DE-092](092-materialized-views-and-derived-tables.md) supplies derived desired state. [DE-094](../ROADMAP.md) next develops data APIs.

## Governing Question

Traditional ingestion moves operational data into analytical systems. Reverse ETL moves modeled analytical data back into operational tools. The direction change is consequential: a bad warehouse row may now alter a customer record, suppress or launch a campaign, create a support task, change a product entitlement, or send data to a third party.

Not every row is a command. A table saying that customer `c7` is in segment `gold` can define desired membership. An event saying “send coupon” represents a one-time effect. Re-querying the table should converge desired state, but replaying the command can send another coupon. Activation design must distinguish state synchronization from transition requests.

Destinations also contain independent truth. A salesperson edits an account owner, a support agent writes a note, or a destination workflow computes status. A warehouse-centric design can overwrite these changes because it assumes the analytical model owns the whole object. Field-level authority and conflict policy are prerequisites.

The governing problem spans policy and distributed systems: decide who may be activated and why, resolve identity, calculate exact desired effects, preview blast radius, respect remote contracts, handle partial/ambiguous outcomes, reconcile effective state, measure business impact independently, and remove effects when purpose or eligibility ends.

## Why This Matters

Activation closes the loop between analysis and action. It can put product-qualified leads in a CRM, risk indicators in support tools, approved audiences in advertising platforms, inventory forecasts in planning systems, or feature entitlements in product services. Done well, it removes manual exports and makes governed models operationally useful.

It also multiplies consequence. A duplicate metric in a dashboard is bad; the same defect sending duplicate messages or changing financial state is worse. Vendor APIs often have rate limits, asynchronous jobs, partial batch errors, eventually visible results, and schemas outside the team's control. Network uncertainty makes simple retries unsafe for non-idempotent actions.

Privacy and governance risk increase when customer attributes cross a boundary. Consent can change faster than a scheduled model. A hash of an identifier can remain personal or matchable data. A destination may retain uploaded audiences, logs, exports, backups, or derived profiles under its own semantics and contract.

Operational ownership therefore cannot end at “rows sent.” Teams need effect SLOs, destination reconciliation, on-call routes, kill switches, vendor incident playbooks, schema/rate monitoring, and decommission workflows. They also need experiments or causal analysis to learn whether activation helped; sync health and business effectiveness are different questions.

## Prerequisites and Retrieval

Retrieve business intent: decision/action, owner, target population, channel, purpose, permitted use, eligibility, suppressions, frequency caps, holdouts, success/harm measures, human review, start/end, rollback/compensation, and acceptable blast radius.

Retrieve source model: stable ID, grain/key, definition/schema/policy version, authoritative inputs, source boundary/watermark, insert/update/delete encoding, null meaning, late corrections, identity merges/splits, classification, quality, freshness, owner, and lineage.

Retrieve destination contract: object and field schema, external IDs, match/upsert/create/update/delete/list modes, ownership, required/read-only fields, null/clear semantics, batch limits, payload size, rate/quota windows, concurrency, idempotency, asynchronous status, partial results, error codes, retries, consistency/read-after-write, versioning, sandbox, and audit/export APIs.

Retrieve identity and policy: tenant, internal-to-destination crosswalk, identifier normalization, consent/purpose/channel state, residency, data processing agreement, age/region restrictions, deletion, retention, holds, encryption, credential scope, vendor subprocessors, and incident notification.

Retrieve runtime state: sync/model/mapping generations, prior confirmed desired set, source extraction position, operation IDs, batches, attempts, destination job IDs, per-item receipts, retries, dead letters, rate-limit state, accepted/effective times, reconciliation, alerts, kill switch, and manual overrides.

Retrieve lifecycle: initial load, canary, recurring changes, pause/resume, reset, full resync, backfill, destination schema migration, credential rotation, vendor outage, consent emergency, source rollback, destination handoff, decommission, removal, evidence retention, and provider exit.

Distinguish model row from command; desired state from event history; match key from mutable contact attribute; null-as-clear from null-as-unmanaged; source absence from explicit removal; update from upsert; accepted from effective; batch success from item success; retryable from ambiguous; policy eligibility from technical deliverability; audience delivery from impression or outcome; pause from rollback; and sync deletion from destination cleanup.

Create an activation contract:

| Concern | Required evidence and decision |
|---|---|
| Intent | Purpose, action/state, owner, population, suppressions, holdout and end |
| Identity | Source grain/key, destination match key, crosswalk, tenant and merge/split rules |
| Authority | Field writers, null/clear, conflict, remote edit and deletion semantics |
| Policy | Consent, purpose, channel, region, minimization, retention and vendor duties |
| Protocol | Desired state or command, operations, batch, idempotency, retry and ordering |
| Destination | Schema/version, limits, async/partial status, consistency and error taxonomy |
| Verification | Receipts, readback/status, common boundary, reconciliation and exceptions |
| Operations | Dry run, canary, kill switch, alert, backfill, recovery and decommission |

Write a falsifiable claim: “Activation A generation G maps one source row per `(tenant,customer_id)` at boundary B through crosswalk X7 into destination object O; owns only fields F; evaluates policy P19 and suppression S immediately before effect; computes create/update/remove/noop against confirmed state; sends bounded batch Q with stable operation IDs and rate/deadline budgets; records per-item accepted/effective outcomes; reconciles desired and observed state within 15 minutes; quarantines identity/schema conflicts; supports kill switch K and canary C; and removes all owned state under decommission D without altering destination-owned fields.”

## Learning Objectives

After completing this module, you should be able to:

1. distinguish reverse ETL, activation, desired-state synchronization, audience membership, append-only events, and one-time commands;
2. define source grain, tenant-safe match keys, identity crosswalks, merge/split/recycling behavior, and destination object identity;
3. assign field-level authority and specify upsert, update, clear, remove, delete, null, and conflict semantics;
4. bind consent, purpose, channel, residency, suppression, holdout, frequency, and deletion policy to effect time;
5. design bounded diff, dry-run, canary, approval, batching, rate limiting, idempotency, retry, partial-result, and dead-letter behavior;
6. track source-to-effective progress and distinguish queued, attempted, accepted, completed, visible, rejected, conflicted, and unknown states;
7. reconcile desired source state with remote state or trustworthy receipts at a common boundary;
8. operate resyncs, backfills, schema changes, vendor outages, credential rotations, emergency suppression, and decommission safely;
9. protect payloads, identifiers, credentials, staging, logs, dead letters, vendors, retention, deletion, and audit evidence; and
10. measure sync reliability separately from causal business effectiveness, harms, holdouts, and downstream outcomes.

## Core Exposition

### Start with an action and authority boundary

Name the operational decision and responsible owner. “Send customer data to CRM” is too broad. “Maintain the approved lifecycle tier in field `warehouse_lifecycle_tier` for active enterprise accounts” identifies a state, field, population, purpose, and boundary. State which humans or services consume it and what they may do.

Classify the destination effect. Attribute synchronization seeks convergence. List or audience membership adds/removes identities. Append-only events preserve occurrences. Commands trigger transitions. Records/tasks may need create-once then update. Each requires different idempotency and deletion behavior.

Establish field ownership. Namespace warehouse-managed fields where possible. For shared fields, define precedence, version, merge, manual override, conflict, and expiration. Never let a broad upsert replace an entire object when only three fields are authorized.

### Make identity resolution explicit

One source row must not ambiguously match several destination objects unless fan-out is intended and bounded. Validate uniqueness at source, crosswalk, and destination. Scope identifiers by tenant/account/environment. Case-folding, whitespace, phone country codes, email aliasing, Unicode, leading zeros, and recycled identifiers can change matches.

Prefer immutable internal and destination IDs in a protected crosswalk. If mutable email or phone bootstraps matching, record the resolved destination ID and govern rematch. An email reassigned to a different person must not inherit prior attributes. Identity merge and split needs a state machine: which destination survives, which fields move, which memberships are removed, and which receipts preserve history.

Hashing an email does not solve identity or policy. It changes representation while retaining matchability and collision/normalization concerns. Treat the crosswalk and hashed identifiers according to their sensitivity and purpose.

### Define source model and mapping semantics

Give the model a stable ID, grain, unique key, definition/schema version, authoritative boundary, quality/freshness contract, classification, lineage, and owner. A destination sync should depend on a governed product, not an analyst's mutable query or spreadsheet.

Map every source field to a destination field, transform, type, enum, size, null behavior, default, sensitivity, owner, and update condition. Distinguish null meaning unknown, intentionally clear, inapplicable, withheld by policy, or not managed. Silent type coercion and truncation corrupt operational state.

Validate destination-required fields and read-only/system fields. Version mappings independently from source schema. A source column rename can be compatible while an enum meaning change is breaking. Contract tests run against a sandbox or safe fixture before production.

### Compute a complete and safe change set

For desired-state sync, compare current eligible model state with prior confirmed desired state or remote state. Classify create, update with exact changed fields, remove/delete, no-op, suppressed, conflict, and unknown. Stable keys and canonical field comparison prevent noisy rewrites.

Absence is ambiguous. It may mean genuine ineligibility, source failure, late partition, changed filter, or partial extraction. Mirror/delete semantics require evidence that the source population is complete for the boundary. Apply minimum-volume and maximum-removal guards; stop on unexpected shrinkage or expansion.

For commands, construct an explicit command ledger with stable ID, subject/object, action, parameters, policy decision, requested time, state, expiry, attempts, and terminal outcome. Never regenerate command identity from current query membership. Replaying a model must not repeat an irreversible command.

### Evaluate policy immediately before effect

The model may have been computed hours earlier. Consent, channel preference, account status, sanctions, safety blocks, legal constraints, frequency caps, or holdout can change before the destination call. Place a policy enforcement check near dispatch using current authoritative state and record its version/reason.

Emergency suppression needs a faster path than ordinary warehouse refresh. A kill switch can stop all or scoped effects by tenant, destination, operation, purpose, or cohort. It should fail safe, propagate rapidly, be access-controlled, auditable, tested, and separate from destructive cleanup.

Minimize payloads and purposes. Send only fields required for the destination action. Binding one export approval to all future vendor uses is not acceptable. Confirm destination/region, retention, deletion, subprocessors, and use restrictions through qualified governance and contracts.

### Preview and control blast radius

Dry run before mutation. Report source boundary, model/mapping/policy versions, total and per-operation counts, exact stable targets in protected evidence, fields changed, clear/delete counts, suppressions, conflicts, unknowns, destination calls, estimated quota/time/cost, and comparison with recent baselines.

Require stronger approval for first runs, new destination objects, mapping/identity changes, deletes, unusually large cohorts, sensitive fields, full resyncs, or commands. Canaries should span tenants, operations, edge values, and identity cases, not merely the first rows.

Expand cohorts only after destination receipts and readback validate identity, fields, policy, and no unexpected workflows. A syntactically accepted record can still trigger downstream automation; sandbox and destination workflow coordination matter.

### Respect destination limits and asynchronous state

Model request, payload, batch, concurrency, daily, tenant, and endpoint limits. Rate limits may use fixed/sliding windows or dynamic quotas. Honor documented retry timing and status, distribute budgets across syncs, and prevent one backfill from starving urgent suppression.

Bulk APIs commonly accept jobs then process items asynchronously. Track remote job and item IDs. Parse per-item outcomes even when the HTTP request or job is successful. Some errors are permanent validation failures, some retriable throttles, and some ambiguous timeouts where the effect may have occurred.

Bound queues and deadlines. Cancel or expire obsolete changes before dispatch when a newer source version supersedes them. Coalesce desired-state updates safely by key/version, but do not coalesce distinct commands. Protect the destination from retry storms after recovery.

### Engineer idempotency and conflict behavior

Use stable operation identity derived from activation, target, source generation/version, operation semantics, and mapping version—not attempt number. If a destination accepts idempotency keys, understand retention and parameter-reuse behavior. Otherwise keep an internal effect ledger and use conditional updates or read-before-write where safe.

Upsert is not automatically idempotent: additive fields, append operations, triggers, and nonunique match keys can repeat effects. Prefer setting desired values with version guards. For one-time commands, a durable destination or internal command ID must return the prior outcome on retry.

Detect conflicts when destination state changed after the observed base version. Policies may make source win, destination win, merge fields, preserve manual override for a period, or quarantine for human review. Record both versions and never hide conflict as a successful overwrite.

### Track state from source to effective outcome

Represent per-item lifecycle such as `eligible`, `suppressed`, `planned`, `queued`, `attempted`, `accepted`, `processing`, `effective`, `rejected_permanent`, `retryable`, `conflicted`, `unknown`, `compensated`, or `removed`. Batch summaries aggregate items but do not replace them.

Keep source/model boundary, extraction time, queue time, attempt time, accepted time, destination completion/visibility time, and reconciliation time. Activation freshness ends at the effect consumers rely upon, not at warehouse query completion or API acceptance.

Receipts minimize payloads while preserving target reference, operation ID/type/version, destination request/job/item ID, mapping/policy, status, error class, attempt, timestamps, remote version, verification, and exception. Credentials and raw sensitive fields do not belong in logs or dead letters.

### Reconcile destination state

If the destination supports safe readback/export, compare owned fields and membership at a common boundary. If only receipts exist, establish which receipt status proves effect and sample or independently verify where possible. Some advertising destinations intentionally do not expose exact matched membership; state the evidence limitation.

Partition outcomes into matched, missing, extra, stale, conflict, suppressed-but-present, duplicate, rejected, and unknown. Counts alone cannot detect swapped identities or stale fields. Compare keys, normalized values, source/destination versions, operation receipts, and aggregate/business invariants.

Reconciliation must not overwrite newer valid destination state blindly. Repair uses current model and policy, stable operation identity, bounded selectors, canaries, and the same safeguards as normal activation. Persistent or high-consequence drift becomes an incident.

### Handle deletions, suppressions, and compensation

When a subject leaves an audience or revokes consent, remove the applicable destination state within the policy/SLO. Keep a protected suppression tombstone long enough to prevent older replay or full resync from re-adding it. Separate urgent removals from general low-priority updates.

Attribute clearing differs from object deletion; object deletion may affect destination-owned fields or workflows. Delete only when authority and contract permit. Otherwise clear owned fields, remove membership, revoke access, or send a destination-specific deletion request and verify its status.

Not every effect is reversible. A sent message, external notification, or consumed coupon cannot be unsent. Compensation may disable future use, issue a correction, revoke an entitlement, or notify operators, but it is not erasure of the original effect. Use human approval and tighter canaries for irreversible actions.

### Operate backfills, resyncs, and migrations

A full resync can issue millions of writes, retrigger workflows, exceed quota, overwrite manual edits, or re-add suppressed identities. Treat it as a migration: pin source/model/mapping/policy versions, dry-run differences, validate suppressions, select cohorts, reserve rate budget, canary, expand, reconcile, and keep a kill switch.

When sync state is lost, do not assume every source row needs an upsert. Reconstruct prior confirmed desired state from receipts/readback where possible. Generate deterministic operations and no-ops. For destination schema/API changes, run parallel mappings in sandbox, then limited production cohorts, and coordinate downstream automations.

Backfills should preserve the same current effect-time policy even when source facts are historical. Historical consent may matter for audit but does not authorize present activation. Reprocess commands only from an explicit authorized ledger and skip terminal IDs.

### Separate reliability from effectiveness

Reliability asks whether the intended eligible effects became correct destination state within SLO. Measures include source-to-effective lag, success by terminal status, retries, throttling, unknowns, conflicts, drift, suppressions, and incidents.

Effectiveness asks whether the activation changed a business outcome and at what harm/cost. Delivery or audience match is not conversion. Use randomized holdouts where ethical and practical, or qualified causal designs; predefine metrics, guardrails, attribution windows, interference, sample size, and stopping rules.

Do not exclude failed deliveries from treatment analysis in a way that biases conclusions. Report intent-to-treat and operational exposure as appropriate. Product, legal, privacy, risk, and domain roles govern experimentation and downstream decisions.

### Secure and retire the integration

Use least-privilege destination credentials scoped to exact objects/actions, separate environments/accounts, rotate secrets, restrict egress, validate endpoints, encrypt transport/staging, and audit configuration and effects. Treat vendor connectors and hosted sync state as part of the supply chain and data inventory.

When retiring, stop new effects, inventory destination-owned versus sync-owned state, remove or transfer owned attributes/memberships under policy, revoke credentials/webhooks, delete staging/dead letters/caches, expire vendor-held data/backups under contract, remove schedules and alerts, and notify owners/consumers. Pausing a job is not decommissioning.

Retain minimal receipts and decision provenance according to retention/hold obligations. Verify no alternate trigger or old version can restart the activation. Record residual irreversible effects and contractual exceptions honestly.

## Definitions and Notation

Let $K$ be stable source entities, $x_k^v$ source state at version $v$, $m(k)$ destination identity, $\pi(x)$ owned-field projection, and $P(k,t)$ effect-time policy. Desired state for eligible keys is $D^*$; observed state is $D$.

For target $k$, operation identity can be modeled as

$$
opid=H(activation\parallel generation\parallel k\parallel sourceVersion\parallel operation\parallel mappingVersion).
$$

It excludes attempt so retries share identity. Hashing supplies deterministic identity only if canonicalization and inputs are stable; it does not make a non-idempotent destination effect safe by itself.

For item $k$, activation lag is $L_k=t_{effective}(k)-t_{authoritative}(k)$ when both are known and comparable. Accepted-only items have right-censored or unknown effective lag, not zero. Let batch accounting satisfy

$$
eligible=effective+suppressed+permanentFailure+retryable+conflict+unknown
$$

at a named boundary, with disjoint outcomes. `effective` may require destination readback/status rather than request acceptance.

Define field authority $Owner(objectType,field,purpose)$ and conflict resolver $R(sourceVersion,destinationVersion,manualOverride,policy)$. A missing owner or ambiguous identity yields quarantine, not source-wins by default.

## Mechanisms, Invariants, or Proof Structure

### Activation lifecycle mechanism

1. State the action or desired state, purpose, accountable owner, eligible population, suppressions, holdout, harm/benefit measures, duration, and reversibility.
2. Define governed source grain/key/model/boundary and destination object/match identity; resolve tenant, normalization, merge, split, recycling, and collision cases.
3. Assign field-level authority and map types, enums, null/clear, defaults, versions, remote edits, delete, and conflict semantics.
4. Classify the protocol as desired state, membership, append event, or command; define idempotency, ordering, retry, expiry, and terminal outcomes accordingly.
5. Re-evaluate consent/purpose/channel/region/safety/holdout at dispatch; apply scoped kill switch and urgent suppression before other effects.
6. Compute complete change classes, dry-run exact targets/fields/removals, enforce blast-radius bounds and approval, and canary representative cases.
7. Dispatch bounded rate/deadline-aware batches with stable operation IDs; parse asynchronous per-item outcomes and retry only safe items.
8. Track source-to-effective lifecycle, preserve minimized receipts, read back/status-check, reconcile, quarantine conflict/unknown, and repair through guarded paths.
9. Test duplicates, timeout ambiguity, partial success, schema/rate change, identity collision, consent race, source shrink, resync, vendor outage, reconciliation drift, and credential compromise.
10. Measure reliability and causal effectiveness separately; deprecate and remove destination state, credentials, retained data, triggers, and evidence under governed lifecycle.

### Convergence and command-safety claims

**Conditional desired-state convergence claim.** If every eligible key has a unique stable destination identity, owned-field desired values are deterministic at boundary $b$, every planned change is eventually applied or explicitly terminal, operations are idempotent and version-guarded, effect-time policy remains valid, no unauthorized competing writer changes owned fields, and reconciliation repairs drift, then observed owned fields converge to $D^*(b)$.

**Proof sketch.** The diff maps each mismatch to a create, update, removal, or no-op. Eventual application resolves each planned mismatch; idempotency makes retries neutral; version guards prevent old operations from regressing state; field authority prevents unmodeled interference; reconciliation discovers residuals. Changing source/policy creates a new desired boundary, and identity ambiguity or a competing writer invalidates the claim.

**Conditional command at-most-once-effect claim.** If each logical command has a globally unique durable ID, the destination atomically records that ID with the effect or provides equivalent retained idempotency semantics, retries reuse it, and ID retention covers every replay interval, then repeated delivery produces at most one represented effect.

**Proof sketch.** The first accepted ID commits the effect and marker. Every later attempt finds the marker and returns the prior outcome without applying again. The claim fails if marker/effect are not atomic, IDs collide or change, retention expires before replay, or downstream workflows repeat independently.

### Executable desired-state sync illustration

This deterministic fixture computes create, update, delete, and no-op operations, applies stable operation IDs, retries the same plan, and compares the destination with desired state. It illustrates convergence for one owned object; it does not model remote partial failure, consent, competing writers, or irreversible commands.

<!-- bijux-verify: {"id":"idempotent-desired-state-sync","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"create=1\nupdate=1\ndelete=1\nnoop=1\napplied=3\nretry_new_effects=0\ndestination_matches_desired=true\n","stderr":""}} -->
```python
desired = {"a": 10, "b": 25, "d": 40}
destination = {"a": 10, "b": 20, "c": 30}


def plan(desired_state: dict[str, int], observed: dict[str, int]) -> list[tuple[str, str, int | None]]:
    operations = []
    for key in sorted(set(desired_state) | set(observed)):
        if key not in desired_state:
            operations.append(("delete", key, None))
        elif key not in observed:
            operations.append(("create", key, desired_state[key]))
        elif desired_state[key] != observed[key]:
            operations.append(("update", key, desired_state[key]))
        else:
            operations.append(("noop", key, desired_state[key]))
    return operations


operations = plan(desired, destination)
for kind in ("create", "update", "delete", "noop"):
    print(f"{kind}={sum(operation[0] == kind for operation in operations)}")

applied_ids = set()


def apply(ops: list[tuple[str, str, int | None]]) -> int:
    new_effects = 0
    for kind, key, value in ops:
        operation_id = f"sync-7:{kind}:{key}:{value}"
        if kind == "noop" or operation_id in applied_ids:
            continue
        applied_ids.add(operation_id)
        if kind == "delete":
            destination.pop(key, None)
        else:
            destination[key] = value
        new_effects += 1
    return new_effects


print(f"applied={apply(operations)}")
print(f"retry_new_effects={apply(operations)}")
print(f"destination_matches_desired={destination == desired}".lower())
```

## Alternatives and Trade-Offs

1. **Reverse ETL versus application-owned integration.** Reverse ETL reuses governed warehouse models and central operations; application integration stays near transactional intent and can offer stronger command semantics. Choose by authority and latency.
2. **Desired-state sync versus events/commands.** Desired state converges and coalesces; events preserve occurrences and commands trigger once. Conflating them produces duplicates or lost history.
3. **Update versus upsert.** Update refuses unknown targets and exposes identity gaps; upsert simplifies creation but can duplicate records or fill incomplete objects.
4. **Mirror/delete versus additive membership.** Mirror removes stale members but trusts complete source comparison; additive avoids unsafe removal but accumulates obsolete state.
5. **Mutable natural key versus crosswalk.** Email/phone is convenient but changes and recycles; durable crosswalks reduce mismatch while adding protected state and lifecycle.
6. **Source wins versus destination wins.** Source authority stabilizes managed fields; destination/manual authority preserves operational edits. Field-level policy avoids one global answer.
7. **Batch versus real-time activation.** Batch coalesces work and controls cost; real-time reduces lag but adds continuous policy, ordering, capacity, and outage concerns.
8. **Readback versus receipts.** Readback verifies visible state but costs quota and may expose data; receipts scale but can prove acceptance rather than effect. Combine proportionally.
9. **Large batches versus small batches.** Large batches improve throughput but increase retry ambiguity and blast radius; small batches improve isolation at request/limit overhead.
10. **Automatic retry versus human quarantine.** Retry heals transient failures; permanent, conflict, identity, policy, or high-impact ambiguous cases need review.
11. **Full resync versus incremental repair.** Full resync can recover unknown state but threatens quota, workflows, suppressions, and manual edits; targeted repair is safer when drift is localized.
12. **Compensation versus prevention.** Compensation helps reversible effects; messages, disclosures, and some financial actions cannot be undone, justifying approval and canaries.
13. **Vendor connector versus custom destination worker.** Connectors accelerate coverage; custom code can enforce unique domain semantics. Both need contract testing, evidence, security, and exit plans.
14. **Operational delivery metric versus experiment outcome.** Delivery diagnoses reliability; randomized/causal measurement estimates impact. Optimizing only one can hide failure in the other.

## Failure Modes and Misconceptions

1. **“A warehouse row is an action.”** It may represent state, a derived fact, or a command candidate; protocol must be explicit.
2. **“Reverse ETL reverses ETL exactly.”** The destination mutation creates side effects, ownership conflicts, remote limits, and policy consequences.
3. **“Email is a stable customer key.”** It changes, aliases, recycles, and can cross tenants.
4. **“Hashed identifiers are anonymous.”** They remain matchable and may be personal data in context.
5. **“One source row creates one destination row.”** Nonunique matches, fan-out, defaults, and workflows can violate that assumption.
6. **“Upsert prevents duplicates.”** Only a unique correct match key and destination semantics can.
7. **“Null means clear.”** It may mean unknown, withheld, inapplicable, or unmanaged.
8. **“Source owns every mapped field.”** Operational users and workflows may own some destination values.
9. **“Last writer wins resolves conflict.”** It hides authority and clock/order errors.
10. **“Missing source row means delete.”** Partial extraction or model failure can cause catastrophic removal.
11. **“Pause rolls back activation.”** Prior memberships, fields, tasks, or messages remain.
12. **“HTTP success means item success.”** Batch and asynchronous systems can reject individual records later.
13. **“Accepted means effective.”** Remote processing, matching, replication, moderation, or workflow execution may remain.
14. **“Timeout means failed.”** The effect may have committed; blind retry can duplicate it.
15. **“Idempotency key makes any action safe.”** Destination retention, parameter rules, atomicity, and downstream triggers define safety.
16. **“Retry the whole batch.”** It can replay successes unless item identity/effects are idempotent.
17. **“Rate limits are just delays.”** They affect freshness, fairness, expiry, suppression priority, and recovery load.
18. **“Consent in the model is current.”** Effect-time state can change after model computation.
19. **“Audience removal can wait for the next campaign.”** Policy may require urgent suppression and verified removal.
20. **“Full resync is a harmless repair.”** It can overwrite edits, re-trigger workflows, exceed quotas, and resurrect suppressions.
21. **“Counts prove sync equality.”** Swapped identities, stale fields, and extra/missing pairs can cancel numerically.
22. **“Dead letters are safe logs.”** They often contain sensitive payloads and need strict access/lifecycle.
23. **“Destination sandbox matches production.”** Quotas, workflows, schemas, data, and permissions can differ.
24. **“Successful sync proves business value.”** It establishes transport/effect evidence, not causal impact.
25. **“Matched audience size equals reached users.”** Matching, eligibility, auction, delivery, and observation are separate stages.
26. **“Manual export is safer because it is visible.”** It usually lacks repeatability, minimization, receipts, deletion, and access controls.
27. **“Connector ownership belongs to the vendor.”** Internal teams own purpose, data, configuration, monitoring, incidents, and exit.
28. **“Deleting the sync removes destination data.”** Decommission must explicitly remove or transfer owned state.

## Worked Examples

### Example 1

**Situation.** Two tenants share the same email address in separate destination accounts. **Reasoning.** Match uses `(destination_account, tenant, destination_contact_id)` from a protected crosswalk; global email matching is forbidden. **Conclusion.** Tenant scope is part of identity.

### Example 2

**Situation.** CRM agents update `account_owner` while the warehouse model also maps it. **Reasoning.** The sync stops owning that field, publishes a separate recommendation, or uses an explicit reviewed conflict workflow. **Conclusion.** Analytical convenience does not confer field authority.

### Example 3

**Situation.** Source population drops 70% after an upstream failure. **Reasoning.** Mirror deletion exceeds the shrinkage bound; the run stops and marks completeness unknown rather than removing destination members. **Conclusion.** Absence is actionable only under proven complete scope.

### Example 4

**Situation.** A bulk request accepts 1,000 rows but later reports 12 invalid enums and three unknown outcomes. **Reasoning.** The run records 985 effective/accepted-as-defined, quarantines permanent validation failures, resolves ambiguous items by status/readback, and never reports 100% success. **Conclusion.** Batch transport and item effects are separate.

### Example 5

**Situation.** A request times out after creating a support task. **Reasoning.** Retry reuses durable command ID stored atomically with the task; the API returns the prior task. If the destination lacks this semantic, status/readback precedes retry. **Conclusion.** Timeout requires outcome resolution, not optimism.

### Example 6

**Situation.** A user withdraws advertising consent minutes after the hourly model runs. **Reasoning.** A fast suppression path blocks queued adds and submits removal using current policy, with priority quota and a tombstone preventing stale replay. **Conclusion.** Effect-time policy cannot depend solely on batch freshness.

### Example 7

**Situation.** A new mapping converts an unknown tier to null, and destination null clears the field. **Reasoning.** Contract tests expose the mismatch; unknown becomes “unmanaged/quarantine,” while clear uses an explicit operation. **Conclusion.** Null semantics are part of the mutation protocol.

### Example 8

**Situation.** Sync state is lost and operators propose a full resync. **Reasoning.** Receipts and readback reconstruct confirmed state; dry run finds 200,000 no-ops, 300 changes, 20 conflicts, and five suppressions. Only bounded deltas proceed. **Conclusion.** Recovery should minimize new effects, not maximize writes.

### Example 9

**Situation.** Campaign conversion rises after activation. **Reasoning.** Seasonal demand and selection may explain it. A randomized holdout with guardrails estimates intent-to-treat effect while sync metrics explain delivery. **Conclusion.** Reliable activation is necessary but not proof of lift.

### Example 10

**Situation.** A connector is retired but destination attributes remain. **Reasoning.** Owners inventory fields/memberships, remove sync-owned values under policy, preserve destination-owned data, revoke credentials, delete staged/vendor copies, and verify no trigger restarts it. **Conclusion.** Decommission ends effects and retained state, not merely scheduling.

## Cross-Program Connections

- [DE-035](035-incremental-models.md) provides model diff, high-water, lookback, stable-key and merge foundations.
- [DE-049](049-run-metadata-and-operational-state.md) models run, attempt, checkpoints, partial outcomes and recovery.
- [DE-055](055-delivery-semantics-in-streaming-pipelines.md), [DE-056](056-exactly-once-effects.md), and [DE-060](060-handling-late-duplicate-and-out-of-order-events.md) distinguish transport, idempotent effects, order and correction.
- [DE-073](073-reconciliation-tests.md), [DE-074](074-freshness-and-timeliness.md), and [DE-076](076-data-contracts.md) supply common-boundary comparison, end-to-end lag and interface ownership.
- [DE-085](085-classification-and-sensitive-data.md), [DE-086](086-access-control-for-analytical-data.md), [DE-088](088-retention-and-deletion.md), and [DE-089](089-auditability-and-provenance.md) govern export, purpose, consent, lifecycle and receipts.
- [DE-092](092-materialized-views-and-derived-tables.md) supplies versioned desired state, incremental maintenance, atomic publication and rebuild correctness.
- [API-019](../../28-api-and-service-engineering/modules/019-bulk-and-batch-operations.md) provides per-item batch outcomes; [API-037](../../28-api-and-service-engineering/modules/037-idempotency-keys.md) provides request identity and replay semantics.
- [API-067](../../28-api-and-service-engineering/modules/067-idempotent-consumers.md) and [API-070](../../28-api-and-service-engineering/modules/070-designing-an-asynchronous-api-for-replay-and-evolution.md) connect duplicate delivery, async resources, replay and evolution.
- [PLAT-073](../../29-platform-engineering/modules/073-resource-quotas.md) and [PLAT-077](../../29-platform-engineering/modules/077-admission-control.md) connect shared rate budgets, admission and overload recovery.
- [DE-094](../ROADMAP.md) develops governed data-serving APIs as an alternative or complement to copying state into external systems.

## References

- Hightouch, “Syncs Overview,” current documentation. <https://hightouch.com/docs/syncs/overview>
- Census, “Syncs,” current documentation. <https://docs.getcensus.com/basics/syncs>
- Salesforce, “Bulk API 2.0,” current developer documentation. <https://developer.salesforce.com/docs/atlas.en-us.api_asynch.meta/api_asynch/bulk_api_2_0.htm>
- HubSpot, “API Usage Guidelines and Limits,” current developer documentation. <https://developers.hubspot.com/docs/api/usage-details>
- Stripe, “Idempotent Requests,” current API documentation. <https://docs.stripe.com/api/idempotent_requests>
- Google, “Get Started with Customer Match,” Google Ads API current documentation. <https://developers.google.com/google-ads/api/docs/remarketing/audience-segments/customer-match/get-started>
- Braze, “API Limits,” current documentation. <https://www.braze.com/docs/api/api_limits/>
- Internet Engineering Task Force, *The Idempotency-Key HTTP Header Field*, RFC 9335, 2023. <https://www.rfc-editor.org/rfc/rfc9335.html>
- National Institute of Standards and Technology, *Privacy Framework 1.0*, 2020. <https://www.nist.gov/privacy-framework/privacy-framework>
- OWASP Foundation, “Third Party Payment Gateway Integration,” current guidance on server-side verification and callback handling. <https://cheatsheetseries.owasp.org/cheatsheets/Third_Party_Payment_Gateway_Integration_Cheat_Sheet.html>

## Exercises

### Exercise 1

Distinguish desired-state synchronization, mirror membership, append event, and one-time command. For each, specify identity, retry, delete/removal, ordering, terminal outcome, and replay behavior.

### Exercise 2

A desired model has keys A=10, B=25, D=40; confirmed destination state has A=10, B=20, C=30. Derive the operation classes. The update for B times out, create D succeeds, and delete C is rate-limited. Design safe retry and final reconciliation.

### Exercise 3

Design a CRM activation contract when sales agents own account owner/notes, the warehouse owns risk tier, email can change, two tenants share contacts, destination upsert requires email, null clears fields, and bulk jobs return asynchronous per-item results.

### Exercise 4

An advertising activation runs hourly, but consent withdrawal must take effect in five minutes. Design source, fast suppression, queued-work cancellation, destination removal, tombstone, rate priority, reconciliation, privacy, evidence, and failure behavior. Explain what audience acceptance does not prove.

### Exercise 5

A company has 240 syncs, overlapping field writers, unknown owners, permanent credentials, no per-item receipts, frequent full resyncs, and vendor costs but no outcome experiments. Design a risk-prioritized recovery and define technical and business completion evidence.

## Answers to the Exercises

### Answer 1

**Desired-state synchronization** keys one current representation and retries the same target/version idempotently; removal clears owned state when eligibility ends; later versions supersede older ones; terminal means observed values match or a bounded exception exists; replay converges. **Mirror membership** similarly converges a complete set, but removal is safe only when prior/current membership populations are known complete.

An **append event** has immutable event ID and occurrence ordering/partition; retries reuse ID and consumers deduplicate while retaining each distinct occurrence; deletion is normally a separate governed tombstone/correction, not absence; terminal means durable accepted/processed according to contract; replay preserves the same events. A **one-time command** has durable command ID, state machine, expiry, authorization and atomic effect marker; retries return prior outcome; compensation is a separate command; ordering and duplicate suppression follow the domain; replay must never re-execute a terminal ID.

### Answer 2

The diff is `noop A`, `update B 20→25`, `delete C`, and `create D=40`. A no-op sends nothing. D's success is stored by stable operation ID and destination receipt, so batch retry excludes or safely replays it. C's rate-limited delete enters retryable state with documented reset/backoff and priority appropriate to its policy; it is not counted effective. B's timeout is ambiguous: query operation status or read back B using the same destination identity/version. If B is already 25, mark the original operation effective; otherwise retry the identical idempotent operation ID or conditional set, never a new additive action.

Reconcile desired versus observed owned values after retries: A=10, B=25, D=40 must match, C must be absent/cleared under the defined removal semantic, and no extras/conflicts/unknowns remain. Preserve attempted, accepted, visible, throttled, ambiguous, and verified times separately. Counts alone do not prove the keys or values.

### Answer 3

Define one source row per `(tenant, immutable_customer_id)` and a protected crosswalk to `(destination_account, contact_id)`. Email is a mutable attribute and bootstrap lookup only; after match, persist destination ID and detect email reassignment/collision. If destination upsert requires email, restrict it to controlled create after uniqueness checks; updates use contact ID. Shared people across tenants stay in separate destination-account/tenant scopes.

Warehouse owns only namespaced `risk_tier` and its version/effective time. Agent-owned account owner and notes are never mapped or replaced. Mapping treats source null for risk as unknown/unmanaged; explicit `clear_risk_tier` is a separate authorized operation. Validate enum/type/length and classify payload. Resolve conflicts if an agent edits the namespaced field through a documented source-wins/manual-override rule rather than blind last-writer-wins.

Bulk jobs use bounded canaries, stable per-contact operation IDs, source/mapping/policy versions, and rate budgets. Track job then per-item accepted/rejected/processing/effective state. Permanent validation/identity errors quarantine; throttles retry; timeouts resolve status/readback before identical retry. Reconcile owned field and remote version by contact ID. Credentials allow only required objects/fields and live in the correct environment; receipts omit notes/email values while preserving protected target references and evidence.

### Answer 4

Maintain ordinary audience desired state from a versioned model, but stream consent withdrawals from the authoritative consent service into a separate high-priority suppression ledger. Dispatch checks current consent immediately before sending. A withdrawal writes a durable subject/purpose/channel/destination tombstone, cancels queued adds, prevents late/replayed model generations from re-adding, and submits destination removal within a reserved rate budget.

Track withdrawal, queue cancellation, removal request, accepted/processed state, and any vendor-defined effective status. Reconcile suppressed subjects against available destination membership or trustworthy removal receipts; persistent unknowns escalate. Fail closed for new adds when consent state or suppression service is unavailable. Encrypt identifiers, minimize/hash only as destination policy permits, restrict ledger/receipts, and apply retention/deletion plus vendor contract obligations. Test outage, reordering, full resync, identifier change and quota exhaustion.

Audience acceptance proves at most that the destination accepted uploaded items under its API semantics. It does not prove identity match, audience inclusion, removal completion, ad eligibility, impression, reach, conversion, legal basis, or causal effect. Report each stage separately and use governed holdouts/causal methods for effectiveness.

### Answer 5

Inventory sync IDs, owners/purposes, source models/boundaries, destinations/objects, match keys, mapped fields and owners, policies/consent, modes, schedules, credentials, receipts/logs, suppressions, removals, costs, consumers and outcomes. Freeze new high-risk/full-resync changes without approval; keep necessary known-safe flows monitored. Kill or contain exposed sensitive, financial/entitlement, messaging, deletion/suppression, cross-tenant, ambiguous-identity and competing-writer risks first.

Assign accountable owners or deprecation paths. Build field-ownership matrices and remove overlaps through namespaced fields or explicit conflict rules. Replace permanent broad credentials with scoped rotated secrets. Add source grain/key and destination crosswalk tests, mapping contracts, effect-time policy, dry-run/removal bounds, canaries, per-item operation IDs/states, retry taxonomy, dead-letter protection, kill switches, and readback/receipt reconciliation. Replace routine full resyncs with changed-state repair; govern necessary resyncs as migrations.

Retire unused/duplicate syncs by removing destination-owned activation state and credentials, not just schedules. For remaining activations, separate delivery reliability from business value. Introduce ethical holdouts or other qualified causal designs with benefit/harm, cost and guardrails; do not preserve harmful or valueless syncs because they are technically healthy.

Technical completion measures include owner/purpose, unique identity, field-authority, policy, credential, dry-run/canary, idempotency, per-item receipt, terminal outcome, freshness, reconciliation, suppression/removal, schema/rate, incident and decommission coverage; conflicts, unknowns, drift, full-resync frequency, lag and exception age. Business evidence includes eligible population, assignment, delivery/exposure, outcome/guardrail definitions, experiment power/quality, incremental effect and total cost. Every active sync must have a reviewed contract and evidence—or a named time-bounded exception.
