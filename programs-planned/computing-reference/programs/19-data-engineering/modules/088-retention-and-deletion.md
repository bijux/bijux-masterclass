---
module_id: DE-088
program: Data Engineering
level: 2
module_number: 88
title: Retention and Deletion
status: complete
last_verified: 2026-09-03
---

# Retention and Deletion

## One-Page Review

### Governing question

How can a data organization translate purpose, lifecycle, contract, law, legal hold, recovery, security, and subject-specific obligations into versioned object-level retention decisions and verifiable deletion across tables, snapshots, logs, caches, replicas, backups, exports, models, and third parties, without confusing a SQL delete, tombstone, expired catalog entry, encryption-key change, or inaccessible user interface with completed erasure?

### Essential definitions

- **Retention** is continued preservation of data for a stated scope, purpose, authority, and interval; it is not a default of keeping everything indefinitely.
- A **retention trigger** is the governed event from which an interval is calculated, such as record creation, account closure, contract end, case resolution, or last required use.
- A **retention rule** binds data class/scope and context to a trigger, minimum or maximum interval, authority, jurisdiction, purpose, precedence, and version.
- A **disposition** is the authorized action at a lifecycle boundary: delete, anonymize under an approved determination, archive, transfer, review, or retain under hold.
- A **legal or preservation hold** suspends otherwise eligible disposition for exact data and custodians under authorized scope; it does not justify retaining unrelated data.
- **Logical deletion** makes data unavailable to ordinary product paths, often with a tombstone or status; **physical deletion** removes recoverable representations from a storage layer.
- **Soft deletion** preserves the original record while marking it inactive; it supports recovery but is retention, not erasure.
- A **tombstone** is deletion state propagated to replicas, caches, streams, indexes, and restored copies so deleted data is not resurrected.
- **Crypto-erasure** renders encrypted data infeasible to recover by destroying required key material under a validated design and threat model.
- **Media sanitization** renders access to target data on media infeasible for a stated level of effort using an appropriate method and verification.
- A **deletion scope graph** relates the subject/data item to every governed copy, version, derivative, cache, index, log, backup, export, model, and processor obligation.
- A **deletion receipt** records target IDs/versions, policy and authority, action, executor, time, storage outcome, exceptions/holds, verification, and remaining bounded copies without retaining deleted contents.
- **Deletion latency** is elapsed time from authoritative eligibility or request to verified disposition at each required layer.
- **Resurrection** occurs when deleted data reappears through restore, replay, replication, reprocessing, re-ingestion, or stale cache.
- **Backup expiry** is scheduled loss of recoverability under the backup lifecycle; it is not necessarily immediate selective deletion.

### Central model, mechanism, or theorem

For data object/version $o$, policy revision $P$, and time $t$, resolve an authorized disposition window:

$$
Window_P(o)=\langle notBefore(o),notAfter(o),action(o),holds(o),unknowns(o)\rangle.
$$

Deletion is eligible only when the minimum-retention boundary has passed, a maximum-retention or valid request requires action, no applicable hold blocks it, dependencies are ready, and required policy evidence is complete:

$$
Eligible_P(o,t)=Required(o,t)\land t\ge notBefore(o)\land \neg ActiveHold(o,t)\land CompleteEvidence(o,t).
$$

Completion is universal over the required scope graph, not one database response:

$$
Complete(o)=\forall n\in RequiredScope(o),\ VerifiedDisposition(n)\lor DocumentedBoundedException(n).
$$

A deletion statement can establish one node's logical state while snapshots, noncurrent object versions, backups, caches, exports, or consumers remain recoverable.

### Critical invariants

- Policies identify stable data classes and exact scopes, authoritative sources, purpose, trigger semantics, minimum/maximum intervals, timezone, versions, effective dates, and disposition.
- Legal, regulatory, contractual, records, security, product, research, and subject-request rules remain attributable; engineers do not invent legal precedence.
- Unknown classification, owner, trigger, jurisdiction, contract, hold status, or lineage becomes a visible exception or quarantine—not automatic retention or deletion.
- Holds are authorized, least-scope, immutable/auditable, periodically reviewed, independently releasable, and propagated before destructive work.
- Desired retention, configured lifecycle, effective recoverability, observed access, and verified deletion remain distinct.
- Scope covers current rows/files plus historical snapshots, change streams, indexes, caches, replicas, logs, temporary/staging/dead-letter data, extracts, notebooks, shares, backups, models, token vaults, keys, and third parties.
- A subject or entity locator is protected and versioned; inability to find pseudonymized or duplicated records does not prove their absence.
- Deletion uses stable IDs and bounded selectors, dry-run/impact preview, authorization, separation where appropriate, concurrency protection, idempotency, rate limits, and fail-safe behavior.
- Table/file deletion semantics are understood: row tombstones, copy-on-write files, snapshot reachability, noncurrent versions, delete markers, garbage collection, and physical blocks differ.
- Recovery objectives and deletion obligations are co-designed; backup immutability has documented expiry, access restriction, restore controls, and tombstone replay.
- Restores, disaster recovery, replays, source re-ingestion, and rebuilds reapply current deletions and holds before serving data.
- Crypto-erasure requires complete key-to-data mapping, exclusive effective key control, protected backup-key deletion, no plaintext copies, algorithm/key assurance, and verification.
- Retention metadata and deletion receipts minimize subject data while remaining tamper-evident, access-controlled, retained, and sufficient to prove action.
- Aggregate or de-identified outputs are assessed for continuing subject linkage and valid de-identification evidence rather than deleted reflexively or exempted reflexively.
- Third-party and downstream duties have delivery, acknowledgment, execution, exception, verification, escalation, and contract-exit evidence.
- Metrics report eligible scope, processed/verified/failed/held/unknown nodes, age and latency by layer/class—not only deletion job success.
- Tests exercise holds, policy conflicts, partial failure, retry, late events, schema/lineage gaps, versioned storage, backup restore, compromised keys, third-party nonresponse, and resurrection.
- Destructive automation stops on scope expansion, policy ambiguity, unusual volume, lost hold feed, or verification mismatch.

### Common failures

Common failures include “retain forever” as the safest default; putting one duration on a table with several record triggers; using creation time where closure time is required; ignoring timezone and late corrections; deleting a current row while time travel retains old files; writing an object-store delete marker while noncurrent versions remain; expiring catalog metadata but not storage; removing raw data while caches, exports, features, logs, or token maps persist; treating a backup as exempt forever; restoring a deleted subject; deleting during an unpropagated hold; retaining an entire lake for one narrow hold; accepting a processor email as verification; destroying a key while plaintext and backup keys remain; keeping sensitive evidence inside deletion logs; and reporting job success when coverage or physical outcomes are unknown.

### Compact example

A customer's current warehouse row is deleted and the API returns success. The table format still references an earlier snapshot, object storage retains noncurrent files, a dashboard cache holds an extract, a nightly model feature copy exists, and backups remain recoverable for 30 days. A correct workflow writes a stable tombstone, removes active/queryable copies, expires eligible snapshots and object versions after safety checks, invalidates caches/features, notifies downstream processors, prevents re-ingestion, and records backup expiry plus restore-time tombstone replay. Completion truthfully distinguishes immediate logical restriction from later bounded loss of recoverability.

### Connections

[DE-049](049-run-metadata-and-operational-state.md) supplies execution evidence, [DE-066](066-time-travel-and-reproducible-reads.md) explains historical reachability, [DE-076](076-data-contracts.md) carries lifecycle duties, [DE-078](078-data-incident-detection-and-triage.md) handles deletion failures, [DE-082](082-dataset-and-column-lineage.md) builds scope, [DE-083](083-data-catalogs.md) exposes policy and requests, [DE-084](084-ownership-and-stewardship.md) assigns authority, [DE-085](085-classification-and-sensitive-data.md) supplies handling context, [DE-086](086-access-control-for-analytical-data.md) protects retained data, and [DE-087](087-masking-tokenization-and-de-identification.md) distinguishes anonymizing disposition from masking. [DE-089](../ROADMAP.md) next deepens auditability and provenance.

## Governing Question

Retention and deletion are often implemented as a timestamp column plus a nightly job. That model breaks as soon as records within one table have different triggers, jurisdictions, contracts, subjects, purposes, holds, or downstream copies. It also cannot say whether “deleted” means hidden from an application, absent from the latest table snapshot, unrecoverable by administrators, expired from backups, or sanitized from retired media.

The requirements can pull in both directions. A maximum period or valid erasure request may require deletion; a minimum records period or legal hold may forbid it; security and minimization may favor less data; incident response and recovery may require bounded evidence. Conflict resolution belongs to authorized policy owners and qualified counsel, records, privacy, security, and domain roles—not ad hoc pipeline logic.

Distributed analytical systems make completion a graph problem. Data moves through ingestion, bronze/silver/gold tables, change streams, indexes, caches, notebooks, exports, models, partners, snapshots, replicas, and backups. A command against one node provides no evidence about the rest. Conversely, deleting an underlying file too early can corrupt an in-flight table operation or violate a hold.

The governing requirement is a policy-to-proof lifecycle: determine exact scope and timing, preserve holds, execute safe idempotent disposition at each layer, propagate tombstones, prevent resurrection, verify outcomes, retain minimal evidence, and state bounded exceptions honestly.

## Why This Matters

Over-retention increases privacy, security, discovery, breach, and operational exposure. Old copies often have weaker ownership, classification, monitoring, and access controls than current products. They also cost money and make corrections or subject rights harder to honor.

Under-retention can destroy evidence, violate contracts or records duties, break reproducibility, impair incident investigation, and corrupt recovery. A retention engine therefore cannot be optimized only for deletion volume. It must protect authorized minimums and holds while meeting authorized maximums.

Deletion also affects data correctness. A subject tombstone that does not reach a late-arriving ingestion stream can resurrect data. Expiring a snapshot still referenced by a branch can damage readers. Deleting token mappings before dependent systems reconcile can strand correction and deletion. Lifecycle behavior is part of product semantics.

Trust depends on precise claims. “We delete within 30 days” should identify the triggering event, systems covered, immediate restrictions, backup window, exceptions, verification, and measurement. Honest bounded recoverability is stronger engineering than a blanket promise contradicted by storage design.

## Prerequisites and Retrieval

Retrieve policy sources: data inventory and classification, purposes, contracts, jurisdictions, applicable law interpreted by qualified roles, records schedules, consent or account state, product lifecycle, incident/security needs, research approvals, backup/recovery obligations, legal holds, and processor terms.

Retrieve data scope: stable subject/entity/product/dataset/field/generation IDs; identity/token mappings; tables/files/partitions/rows; snapshots/branches/tags; object versions/delete markers; streams/topics; replicas; indexes/search; caches; logs/traces; temporary/staging/dead-letter data; notebooks; reports/extracts; model features/checkpoints; shares; archives; backups; devices/media; and external processors.

Retrieve time semantics: creation/event/collection/closure/contract-end/case-resolution/last-use timestamps, source clocks/timezones, valid versus observation time, late/corrected events, interval start/end inclusivity, business calendars, policy effective dates, and clock quality.

Retrieve storage behavior: logical/physical delete, MVCC/history, time travel, copy-on-write/merge-on-read, compaction/vacuum/garbage collection, versioning, lifecycle rules, WORM/object lock, legal holds, replication lag, key hierarchy, crypto-erasure, media sanitization, backup chain and restore behavior.

Retrieve operations: policy evaluation, dry run, approval, authorization, selector, affected count/bytes, dependencies, tombstone, job/run, retry/idempotency, partial failure, quarantine, verification, receipts, metrics, alerts, incident escalation, rollback boundaries, processor messages, and attestations.

Retrieve risk and recovery: RPO/RTO, accidental deletion, ransomware, privileged misuse, compromised keys, disaster recovery, restore drills, immutable copies, maximum tolerable recoverability, deletion latency objectives, and evidence retention.

Distinguish minimum from maximum retention; trigger from ingestion time; policy from configured lifecycle; hold from ordinary retention; logical from physical deletion; soft delete from erasure; delete marker from version removal; snapshot expiration from orphan cleanup; unreferenced from safe-to-delete; access revocation from deletion; encryption from crypto-erasure; de-identification from masking; backup unavailability from expiry; request acknowledgment from completed disposition; and receipt metadata from retained content.

Create a lifecycle decision record:

| Concern | Required evidence and decision |
|---|---|
| Subject | Stable item/subject/product/generation IDs and locator version |
| Policy | Rule/version, authority, purpose, jurisdiction, contract and class |
| Time | Trigger source/value, interval, not-before/not-after and timezone |
| Holds | Hold IDs, exact scope, issuer, start/review/release and precedence |
| Scope | Current/history/replica/cache/log/export/model/backup/processor nodes |
| Action | Delete/anonymize/archive/review, method, authorization and dependencies |
| Execution | Job/run, selector, idempotency, counts, outcomes, failures and retry |
| Verification | Layer-specific observation, independent check and residual recovery |
| Evidence | Receipt/digest, policy, actors, timestamps, exceptions and minimization |
| Lifecycle | Restore protection, downstream acknowledgment, expiry and incident route |

Write a falsifiable claim: “Policy P12 applies to item class C7 at generation G42, using account-closure event E9 in UTC and a 365-day minimum/400-day maximum; hold feed H3 is current and blocks 17 exact item IDs; lineage scope L8 resolves 12 required systems, 10 delete immediately, immutable backup B5 expires within 28 days and replay gate T4 prevents resurrection, processor Q2 acknowledges 53 exact targets, execution R6 reconciles eligible/deleted/held/failed/unknown counts, independent verification V7 samples storage and restores, and minimal receipts prove bounded outcomes without retaining deleted values.”

## Learning Objectives

After completing this module, you should be able to:

1. distinguish retention, disposition, legal hold, logical/physical deletion, tombstones, crypto-erasure, media sanitization, and backup expiry;
2. model minimum/maximum periods, trigger events, time semantics, policy authority, conflicts, unknowns, and versioned decisions;
3. build a deletion scope graph across active data, histories, replicas, streams, caches, logs, exports, models, backups, keys, and processors;
4. design safe, authorized, idempotent, concurrency-aware deletion execution with dry runs, bounds, failure isolation, and receipts;
5. reason about MVCC, table snapshots, branches/tags, object versioning, delete markers, garbage collection, compaction, and orphan-file hazards;
6. reconcile retention and deletion with backup immutability, RPO/RTO, restore, tombstone replay, legal hold, and disaster recovery;
7. evaluate crypto-erasure and media sanitization claims against key/data/media scope and threat assumptions;
8. handle subject-level requests, pseudonyms, aggregates, de-identified outputs, models, and third parties without overclaiming;
9. measure policy/configuration/scope coverage, eligibility, latency, failures, holds, recoverability, resurrection, and verified outcomes; and
10. test lifecycle rules with simulated time, late/corrected events, holds, policy changes, partial outages, restores, and adversarial destructive inputs.

## Core Exposition

### Model rules as authoritative temporal policy

Give every rule a durable ID, owner/authority, version, effective interval, source citation, data class/scope, purpose/context, trigger, minimum and/or maximum duration, disposition, jurisdiction/contract qualifiers, exception behavior, and review cadence. Do not embed durations only in scheduler code or bucket configuration.

A minimum says “do not dispose before”; a maximum says “dispose no later than,” subject to valid exceptions such as a hold. Some policies require review rather than automatic deletion. Resolve all applicable rules into a decision with provenance. If qualified authorities have not resolved a conflict, quarantine and escalate the exact scope instead of choosing the longer or shorter interval silently.

Trigger semantics matter more than arithmetic. “Seven years after closure” needs an authoritative closure event, reopening behavior, corrections, timezone, and missing-event policy. Event time and ingestion time differ. A late closure event may make an item immediately overdue; a corrected event may change eligibility. Preserve the policy and trigger version used for each decision.

### Inventory scopes and ownership

Start with stable data and subject identifiers, then traverse lineage, catalogs, storage inventories, query/access history, orchestration, model registries, shares, backup catalogs, and processor registers. Label each node current, historical, derived, cached, logged, exported, backed up, held, unknown, or out of scope with reason.

Lineage is necessary but incomplete. Runtime copies, spreadsheets, notebooks, screenshots, manual exports, abandoned buckets, and vendor systems may not appear. Combine declared consumer contracts, storage scanning, access logs, cloud inventory, endpoint controls, interviews, and incident evidence. Missing coverage is a measured risk, not a zero count.

Subject-level deletion requires a governed locator that maps current and historical identifiers, pseudonyms, tokens, merges/splits, accounts, devices, and households according to policy. Protect this mapping because it is itself identifying. Version it so retries and audits can explain which objects were targeted.

### Separate eligibility from execution

The policy engine determines eligible, retained-not-due, held, unknown, conflicting, or requires-review. The executor applies a storage-specific action only to a signed/versioned decision set. This separation reduces the chance that a storage administrator invents policy or that a policy reviewer performs destructive work without controls.

Before execution, preview stable target IDs/versions, counts, bytes, systems, holds, dependencies, expected outcomes, and unusual deltas. Bound batches and blast radius; require stronger approval for exceptional scale or protected systems. Use exact selectors, concurrency/version guards, idempotency keys, and checkpoints. Never build destructive scope from an unresolved environment variable, broad wildcard, or mutable display name.

Deletion is often irreversible at a layer, so safety is not “rollback later.” Stop on lost hold feeds, changed policy revision, expanded scope, mismatched counts, unrecognized schema, permission drift, or verification failure. Partial progress should be replayable without deleting unrelated or newly retained data.

### Understand storage-layer truth

A relational `DELETE` may create a new MVCC version while old pages remain until vacuum or storage reuse. A lakehouse row delete can write delete files or replacement files while prior snapshots still reference original data. Snapshot expiration removes metadata reachability and makes unreferenced files eligible for cleanup; branch/tag references and concurrent readers can extend life.

Orphan cleanup is not interchangeable with snapshot expiration. An unreferenced file may belong to an in-flight writer or appear different because of path normalization. Use the table format's maintenance procedures, safe age bounds, ownership rules, dry runs, and concurrency design. Directly deleting guessed files can corrupt table state.

In versioned object storage, a simple delete may add a marker while noncurrent versions remain. Lifecycle must cover current markers, noncurrent versions, incomplete multipart uploads, replicas, and locks. WORM/object-lock retention and legal holds apply to specific versions under platform semantics. Verify effective configuration rather than inferring it from the current listing.

Indexes, search systems, materialized views, caches, CDN objects, BI extracts, and feature stores may rebuild from upstream or retain independent copies. Each needs a target action and verification. Disabling a catalog entry or revoking access reduces exposure but does not delete bytes.

### Propagate tombstones and prevent resurrection

Create an authoritative tombstone or suppression ledger keyed by stable subject/item identity and policy event. It must outlive the longest replay/restore/re-ingestion path needed to prevent resurrection while minimizing retained identifying data. A salted or keyed locator may help, but its matching, collision, rotation, and deletion implications need design.

Streams propagate deletion events with schema/version, effective time, source, reason class, target identity, and idempotency. Consumers acknowledge application and expose failures. Late upserts must compare against tombstone state. Rebuilt indexes and tables consult the ledger before becoming readable.

Restore procedures are a critical PEP. Restore into isolation, apply current holds, policies, tombstones, and security configuration, reconcile known deletions since the backup point, scan/verify, and only then promote. A successful restore that resurrects deleted data is a lifecycle failure even if recovery objectives were met.

### Co-design backups, immutability, and deletion

Backups defend against accidental destruction, corruption, ransomware, and disasters. Immutability can deliberately prevent early selective deletion. Document which backups contain the data, chain dependencies, retention/expiry, access, encryption, key custody, locations, restore authority, and maximum recoverability window.

When immediate selective removal is infeasible, restrict access, prevent ordinary restoration, expire the backup under its governed schedule, and ensure restore-time deletion replay. State this bounded exception in user, regulator, contract, and internal claims as applicable. Do not call the data physically deleted while recovery remains possible.

Test backup expiry and restore behavior. Catalog expiry does not prove media blocks or provider copies are gone; provider semantics and contracts define evidence. Retain enough minimal metadata to prove which backup generations expired and which tombstones must apply, without recreating deleted content.

### Evaluate crypto-erasure and media sanitization

Crypto-erasure can efficiently address encrypted datasets or media if the target data is encrypted only under key material that is completely destroyed, including wrapped copies, caches, escrow, replicas, snapshots, logs, and backups. Shared keys can make the deletion scope too broad; layered per-object or per-tenant keys improve granularity but increase lifecycle complexity.

Validate key generation, hierarchy, algorithm/mode, exclusive use, mapping, rotation, access, escrow, backup, hardware behavior, destruction method, and inability to recover. Destroying a catalog reference to a key is not destruction. Nor does key destruction affect plaintext exports, decrypted caches, tokens, or alternate keys.

Media sanitization addresses reuse or disposal of physical/logical media. Choose clear, purge, or destroy-like methods according to current authoritative guidance, media technology, sensitivity, threat, reuse, and verification. Cloud customers often cannot operate physical media; provider architecture, contracts, attestations, encryption, and tenant-key controls become part of evidence.

### Handle holds and exceptional retention

A hold record names authority, matter/purpose, exact custodians/data scope, start, preservation behavior, notification constraints, reviewer, periodic review, and release authority. Apply holds before lifecycle execution and prove propagation. Separate the power to issue/release a hold from ordinary deletion administration where risk warrants.

Overbroad holds create indefinite shadow archives; underbroad holds destroy required evidence. Use identifiers, date ranges, products, sources, and lineage to scope precisely, but retain unknown zones until resolved. When released, re-evaluate normal policy from its original trigger rather than starting a fresh retention period unless policy explicitly says so.

Emergency suspension of deletion during a control incident should be time-bounded, authorized, monitored, and narrowed as evidence improves. “Pause everything forever” is not a durable incident response.

### Treat derivatives and external processors explicitly

An aggregate may no longer support a subject-level deletion if it is genuinely nonidentifying and updating it would disclose membership; a pseudonymized row may remain locatable and in scope. Apply the contextual evidence from DE-087 and qualified policy interpretation. Do not exempt every derived table or rewrite every statistic automatically.

Models can memorize or encode contributions. Depending on obligation, risk, model type, and feasibility, response may include deleting training examples for future runs, retraining, unlearning with validated evidence, restricting output, retiring a model, or documenting why an aggregate model is outside scope. A registry tag alone is not remediation.

Processors and partners need stable request/target IDs, authenticated delivery, deadlines, acknowledgment, status, exception/hold reporting, completion evidence, escalation, audit rights, subprocessors, contract exit, and breach handling. An email saying “done” is weaker than reconciled target counts and agreed evidence, but invasive proof can itself expose data; design proportional verification.

### Prove outcomes without retaining what was deleted

For each node record the target's stable pseudonymous reference or batch digest, decision/policy version, authorized actors, execution ID/time/method, expected and observed counts, storage response, verification method/time, exception/hold, remaining recoverability, retry/escalation, and downstream acknowledgments. Keep content values out of receipts.

Verification is layer-specific: absence from current queries; snapshot/reference inspection; noncurrent-version inventory; cache/index negative lookup; key-state attestation; processor receipt; backup expiry; and restore drill. Use independent sampling or control where consequences justify it. “Command returned zero errors” verifies execution transport, not full disposition.

Measure inventory/policy/lineage coverage, eligible volume, on-time completion, latency distribution, held/unknown/conflicted/failed scope, retries, verification coverage, noncurrent bytes, backup residual windows, downstream acknowledgment, restore-resurrection tests, and incidents. Report denominators and age, not just successful runs.

## Definitions and Notation

Let $O$ be stable data objects or versions, $N(o)$ their required scope-graph nodes, $P_v$ policy revision $v$, $t_0(o)$ an authoritative trigger time, $d_{min}$ a minimum retention duration, $d_{max}$ a maximum duration, and $H(o,t)$ active holds.

Define boundaries $b_{min}=t_0+d_{min}$ and $b_{max}=t_0+d_{max}$ when applicable. A policy can require review instead of automatic action, and an unresolved trigger leaves boundaries unknown. For a deletion-requiring rule:

$$
Eligible(o,t)=Known(o,t)\land t\ge b_{min}(o)\land t\ge b_{max}(o)\land \neg H(o,t).
$$

In practice, different rules may contribute the binding minimum and maximum; an authorized resolver records both provenance and any conflict. Let node outcome

$$
V(n)\in\{deleted,anonymized,expired,held,notDue,failed,unknown,documentedException\}.
$$

Then complete deletion is not a Boolean database flag but a quantified claim over the declared graph:

$$
Complete(o)\iff \forall n\in N(o),\ V(n)\in\{deleted,anonymized,expired,documentedException\}.
$$

Whether `anonymized` satisfies disposition depends on an approved context-specific determination. Whether `documentedException` satisfies an external promise depends on the promise; it must never be silently counted as deleted. Coverage is $|N_{resolved}|/|N_{eligible}|$ only when the eligible denominator is known.

## Mechanisms, Invariants, or Proof Structure

### End-to-end lifecycle mechanism

1. Classify exact data scope and retrieve authoritative purposes, jurisdictions, contracts, records rules, triggers, owners, holds, and policy versions.
2. Resolve minimum/maximum/review rules into item-level decisions; quarantine missing, conflicting, stale, or unauthorized evidence.
3. Construct the scope graph from catalog, lineage, runtime, storage, backup, model, export, and processor evidence; quantify unknown coverage.
4. Preview stable targets, counts, bytes, dependencies, holds, policy revision, unusual deltas, blast-radius bounds, and required approvals.
5. Issue an immutable tombstone/disposition event before or atomically with active deletion so consumers, late writes, rebuilds, and restores cannot resurrect it.
6. Execute layer-specific idempotent actions with exact selectors, concurrency guards, rate limits, checkpoints, retries, failure isolation, and stop conditions.
7. Apply snapshot expiration, noncurrent-version lifecycle, garbage collection, crypto-erasure, backup expiry, or sanitization only under their own safety and evidence requirements.
8. Notify downstream processors and owners; reconcile acknowledgments, exceptions, failures, deadlines, and escalations.
9. Verify current absence, historical reachability, keys, caches/indexes, artifacts, backups, restores, and processor outcomes; retain minimized receipts.
10. Monitor policy/config drift, overdue scope, unknowns, holds, restore/re-ingestion, new lineage, incidents, and recurrence; re-evaluate on change.

### Safety and liveness claims

**Safety claim.** If execution targets only objects proven eligible under one current policy/hold snapshot and stable selectors, then no object covered by an active known hold or unexpired minimum is intentionally deleted by the modeled executor.

**Liveness claim.** If every required scope node is known, every eligible node has an eventually available authorized executor, failures are retried or escalated, and no hold/exception remains indefinitely, then every required node eventually reaches a terminal disposition outcome.

**Proof sketches.** For safety, eligibility contains the negation of active hold and passage of the minimum boundary; binding the signed decision set and version guards to the executor preserves those predicates at action time or forces re-evaluation. For liveness, each nonterminal eligible node advances on successful execution or remains in a retry/escalation queue; under eventual availability and finite holds/exceptions, it cannot remain nonterminal forever.

Real systems weaken the assumptions: stale hold feeds threaten safety; missing lineage and processors threaten liveness; immutable backups deliberately delay terminal expiry; public exports may be irrecoverable. The proof sketches justify design obligations, not a universal deletion guarantee.

### Executable eligibility illustration

This deterministic fixture separates deletion eligibility from not-due, held, dependency-blocked, and unknown-policy states. It is policy logic illustration, not legal interpretation or storage deletion.

<!-- bijux-verify: {"id":"retention-eligibility-states","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"delete=1\nretain_hold=1\nretain_not_due=1\nretain_dependency=1\nquarantine_unknown=1\nall_records_accounted_for=true\n","stderr":""}} -->
```python
records = [
    {"id": "a", "deadline": 100, "hold": False, "ready": True},
    {"id": "b", "deadline": 100, "hold": True, "ready": True},
    {"id": "c", "deadline": 130, "hold": False, "ready": True},
    {"id": "d", "deadline": None, "hold": False, "ready": True},
    {"id": "e", "deadline": 100, "hold": False, "ready": False},
]
now = 120


def decide(record: dict[str, object]) -> str:
    if record["deadline"] is None:
        return "quarantine_unknown"
    if bool(record["hold"]):
        return "retain_hold"
    if now < int(record["deadline"]):
        return "retain_not_due"
    if not bool(record["ready"]):
        return "retain_dependency"
    return "delete"


counts = {state: 0 for state in (
    "delete", "retain_hold", "retain_not_due", "retain_dependency", "quarantine_unknown"
)}
for record in records:
    counts[decide(record)] += 1
for state in counts:
    print(f"{state}={counts[state]}")
print(f"all_records_accounted_for={sum(counts.values()) == len(records)}".lower())
```

## Alternatives and Trade-Offs

1. **Central policy engine versus embedded rules.** Central evaluation improves consistency and evidence; embedded rules reduce dependency latency. Either needs version synchronization and one authoritative policy source.
2. **Record-level versus partition/table expiry.** Record granularity honors different triggers but can be expensive. Coarser expiry is efficient when policy and time truly align, not when it merely simplifies storage.
3. **Hard versus soft delete.** Hard deletion reduces recoverability; soft deletion enables recovery and audit but retains sensitive content. Use soft delete only for a defined bounded purpose and interval.
4. **Immediate versus batched execution.** Immediate action lowers latency; batching improves efficiency and reviewability. Batches need deadlines, exact membership, retries, and blast-radius controls.
5. **Tombstone versus destructive event only.** Tombstones prevent re-ingestion and restore resurrection; they retain minimal identity state. Scope their own retention and protection deliberately.
6. **Fine-grained backup deletion versus rolling expiry.** Selective deletion can be complex or impossible in immutable chains. Bounded expiry plus restore-time replay is often safer but must be disclosed honestly.
7. **WORM compliance versus administrative recoverability.** Strong immutability protects records and ransomware recovery but blocks early deletion. Separate data by lifecycle class before locking and govern holds precisely.
8. **Crypto-erasure versus overwrite/file deletion.** Crypto-erasure can be fast and media-independent but relies on complete key/data mapping and no plaintext copies. Physical deletion may be more direct yet storage abstractions obscure media behavior.
9. **Delete versus approved anonymizing disposition.** Anonymization may preserve aggregate utility; it requires contextual evidence and may not satisfy every rule or request. Masking alone is insufficient.
10. **Full downstream proof versus contractual attestation.** Direct technical proof is stronger but often unavailable across processors and can expose data. Use proportional reconciled evidence, audit rights, and escalation.
11. **Long versus short recovery windows.** Longer windows improve resilience; shorter windows reduce recoverability risk and cost. Match RPO/RTO and deletion promises with explicit bounds.
12. **Aggressive automation versus review gates.** Automation meets scale and deadlines; manual review protects novel/conflicted/high-impact cases. Risk-tier policy and stop conditions combine them.

## Failure Modes and Misconceptions

1. **“Keeping everything is safest.”** It increases exposure and can violate maximum-retention duties.
2. **“Shortest retention is always safest.”** Premature deletion can violate holds, records duties, recovery, and evidence needs.
3. **“One table gets one duration.”** Rows can have different subjects, purposes, triggers, jurisdictions, and holds.
4. **“Ingestion time is the trigger.”** Policy may depend on occurrence, closure, contract end, or last required use.
5. **“A missing trigger means retain forever.”** Unknowns require ownership and resolution, not invisible indefinite retention.
6. **“Choose the longest rule when policies conflict.”** That can violate a maximum; authorized roles must resolve precedence.
7. **“A hold covers the whole lake.”** Holds should preserve exact required scope and explicitly managed unknowns.
8. **“Releasing a hold starts retention over.”** Normal boundaries usually derive from original triggers unless policy says otherwise.
9. **“SQL DELETE removes the bytes.”** MVCC, logs, snapshots, replicas, and backups may retain recoverability.
10. **“Dropping a table deletes its files.”** Catalog and storage ownership/lifecycle semantics differ.
11. **“A delete marker is permanent deletion.”** Noncurrent object versions can remain readable to privileged paths.
12. **“Snapshot expiration immediately deletes all history.”** Other snapshots, branches, tags, or references can retain files.
13. **“Every unreferenced file is orphaned.”** In-flight writers and path mismatches make aggressive cleanup dangerous.
14. **“Vacuum is merely performance maintenance.”** It changes time-travel and physical-recovery boundaries.
15. **“Backups are outside deletion scope.”** They need bounded retention, access, restore replay, and truthful exception claims.
16. **“Immutable means exempt.”** Immutability is a chosen constraint whose expiry and policy fit must be designed.
17. **“Restore first, govern later.”** That creates a window where deleted or held data can be served incorrectly.
18. **“Tombstones can expire with active data.”** They must cover the longest path that could replay older data.
19. **“Key deletion proves crypto-erasure.”** Alternate keys, escrow, backups, plaintext, caches, or shared-key scope can defeat it.
20. **“Encryption is deletion.”** Available decryption authority means the data remains recoverable.
21. **“Catalog disappearance proves absence.”** Uncataloged, orphaned, exported, or abandoned storage may remain.
22. **“Revoking access deletes data.”** It reduces availability to a principal but preserves the content.
23. **“Pseudonymized records cannot be found.”** Protected token mappings and linkage can keep them attributable.
24. **“Aggregates always require row subtraction.”** Some valid nonidentifying statistics may not be subject-addressable; qualified policy decides.
25. **“Deleting training rows fixes a model.”** Memorization or influence may persist; retraining/unlearning claims need validation.
26. **“The processor acknowledged the email.”** Receipt of a request is not verified execution.
27. **“Zero job errors means complete.”** Scope, counts, outcomes, physical state, and exceptions still need reconciliation.
28. **“Receipts should retain deleted values for proof.”** That recreates the content; use identifiers/digests and minimized evidence.
29. **“A failed deletion can wait silently.”** Overdue failures need retry, escalation, containment, and incident criteria.
30. **“Deletion can be promised absolutely.”** Claims must name scope, layers, latency, recovery windows, exceptions, and evidence.

## Worked Examples

### Example 1

**Situation.** A seven-year rule starts at contract closure, but the lifecycle job uses row creation time.

**Reasoning.** Long-running contracts become eligible too early while recently closed old records may be miscomputed. The policy record must name authoritative closure, reopening and correction semantics. The engine recomputes from event time, quarantines missing closures, and compares changed eligibility before execution.

**Conclusion.** Correct duration applied to the wrong trigger is an incorrect and potentially destructive policy.

### Example 2

**Situation.** A valid subject request reaches an account with current rows, two pseudonyms, a merged former account, and a dashboard extract.

**Reasoning.** A protected versioned locator resolves the identity history and token domains; catalog/lineage/runtime evidence finds the extract. Each node is evaluated against holds and applicable rules. Active copies are deleted or validly anonymized, refreshes are disabled, tombstones prevent source replay, backup residuals are recorded, and minimized receipts reconcile targets.

**Conclusion.** Subject deletion is identity resolution plus scope and policy, not one primary-key statement.

### Example 3

**Situation.** An object-store delete call returns success on a versioned bucket.

**Reasoning.** The call created a current delete marker; earlier versions remain. Inventory shows three noncurrent versions and one replica. Lifecycle rules must permanently expire eligible noncurrent versions and replica copies after any locks/holds. Verification inspects version IDs rather than only ordinary listing.

**Conclusion.** API success established logical hiding, not loss of recoverability.

### Example 4

**Situation.** A lakehouse snapshot is expired, but a named audit tag references it.

**Reasoning.** Files remain reachable through the tag and must not be garbage-collected. If the tag is an authorized hold-like record, retention is correct; if stale, its owner reviews/removes it. Maintenance then expires snapshots and deletes only files unreferenced by all valid metadata after safe age/concurrency checks.

**Conclusion.** Reference reachability, not apparent age alone, determines safe physical cleanup.

### Example 5

**Situation.** Backups are immutable for 35 days while ordinary data promises a seven-day active deletion target.

**Reasoning.** The system deletes active/queryable copies within seven days, blocks ordinary restoration, preserves tombstones, and records that encrypted immutable backup generations remain recoverable until scheduled expiry. Restore drills reapply deletions before promotion. External wording distinguishes active deletion from the 35-day maximum backup recovery window.

**Conclusion.** Recovery and deletion can coexist when the residual window and controls are explicit and verified.

### Example 6

**Situation.** A legal hold feed stops updating shortly before a large automatic expiry run.

**Reasoning.** Hold freshness is a safety precondition. The executor stops before deletion, alerts the hold authority and operations, preserves already completed receipts, and does not replace unknown status with “no hold.” Once the authoritative feed recovers, it rebuilds and reauthorizes the target set.

**Conclusion.** Availability loss in preservation evidence must fail safe for destructive action.

### Example 7

**Situation.** A tenant-encrypted archive is to be crypto-erased by deleting its key.

**Reasoning.** Review maps every archive block exclusively to the tenant key, validates wrapped/escrow/backup key copies, confirms no plaintext cache/export, checks algorithm and provider destruction behavior, and records independent key-state evidence. A shared master key or retained wrapped copy would invalidate the claim.

**Conclusion.** Crypto-erasure is a property of complete key and plaintext scope, not a key-management API verb alone.

### Example 8

**Situation.** A daily ingestion replay contains an old customer event after their deletion completed.

**Reasoning.** The consumer checks the authoritative tombstone ledger before publishing; the event is quarantined and counted as a resurrection attempt. The team traces why the source retained it, applies the downstream request, and tests rebuilds from the oldest retained log and backup.

**Conclusion.** Deletion remains a continuing invariant while older sources can replay data.

### Example 9

**Situation.** A model was trained on a record now eligible for deletion.

**Reasoning.** Lineage confirms contribution; risk and policy owners determine whether the model remains subject-linked or within an approved aggregate use. They test memorization/influence and evaluate retraining, validated unlearning, restriction, or retirement. Removing the training row affects future training but does not alter the current model.

**Conclusion.** Model disposition requires evidence about the model, not only its training table.

### Example 10

**Situation.** A deletion run reports 9,998 successes and two permission failures out of 10,000 targets.

**Reasoning.** The batch is not complete. Receipts preserve exact failed IDs without values; access to those nodes is restricted, retry uses the same idempotent decision set, and persistent failure escalates by deadline and consequence. Independent verification samples successes and confirms both failures eventually reach terminal outcomes.

**Conclusion.** Aggregate success rate cannot erase known incomplete high-risk targets.

## Cross-Program Connections

- [DE-049](049-run-metadata-and-operational-state.md) provides state, retries, receipts, and incident-aware workflow evidence for lifecycle execution.
- [DE-066](066-time-travel-and-reproducible-reads.md) explains why current-row deletion does not remove historical snapshot reachability.
- [DE-078](078-data-incident-detection-and-triage.md) supplies containment and escalation when deletion fails, runs too broadly, loses a hold, or resurrects data.
- [DE-082](082-dataset-and-column-lineage.md) constructs the governed scope graph while this chapter adds storage inventories and processor evidence for gaps.
- [DE-085](085-classification-and-sensitive-data.md) and [DE-087](087-masking-tokenization-and-de-identification.md) determine whether a derivative remains sensitive or qualifies for an approved alternative disposition.
- [DE-086](086-access-control-for-analytical-data.md) protects retained, held, backup, receipt, key, vault, and tombstone data without substituting access revocation for deletion.
- Security Engineering owns media sanitization, cryptographic key assurance, and adversarial controls in greater depth; this chapter integrates them with analytical lifecycle semantics.
- [DE-089](../ROADMAP.md) develops auditability and provenance for retention decisions, transformations, execution, and verification.

## References

- National Institute of Standards and Technology, *Guidelines for Media Sanitization*, SP 800-88 Rev. 2, 2025. <https://csrc.nist.gov/pubs/sp/800/88/r2/final>
- National Institute of Standards and Technology, *NIST Privacy Framework 1.0*, 2020. <https://www.nist.gov/privacy-framework/privacy-framework>
- European Union, *Regulation (EU) 2016/679*, especially Articles 5 and 17, official text. <https://eur-lex.europa.eu/eli/reg/2016/679/oj>
- Apache Iceberg, “Maintenance,” snapshot expiration, metadata cleanup, and orphan-file guidance, current documentation. <https://iceberg.apache.org/docs/latest/maintenance/>
- Apache Iceberg, “Branching and Tagging,” snapshot-reference retention, current documentation. <https://iceberg.apache.org/docs/latest/branching/>
- Google Cloud, “Data Retention with Time Travel and Fail-Safe,” BigQuery current documentation. <https://cloud.google.com/bigquery/docs/time-travel>
- Amazon Web Services, “Retaining Multiple Versions of Objects with S3 Versioning,” current documentation. <https://docs.aws.amazon.com/AmazonS3/latest/userguide/Versioning.html>
- Amazon Web Services, “Managing the Lifecycle of Objects,” Amazon S3 current documentation. <https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html>
- Amazon Web Services, “Locking Objects with Object Lock,” Amazon S3 current documentation. <https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html>
- PostgreSQL Global Development Group, “Routine Vacuuming,” PostgreSQL 18 current documentation. <https://www.postgresql.org/docs/current/routine-vacuuming.html>
- Cloud Security Alliance, “Cloud Data Management Capabilities,” Cloud Controls Matrix v4.0.12. <https://cloudsecurityalliance.org/artifacts/cloud-controls-matrix-v4>
- UK Information Commissioner's Office, “Principle (e): Storage Limitation,” current UK GDPR guidance. <https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-protection-principles/a-guide-to-the-data-protection-principles/storage-limitation/>

## Exercises

### Exercise 1

Distinguish minimum retention, maximum retention, legal hold, logical delete, physical delete, soft delete, tombstone, backup expiry, crypto-erasure, and media sanitization. Give one evidence item needed for each disposition-related claim.

### Exercise 2

A record closed on day 40 has a 30-day minimum and 60-day maximum. At day 105, an active hold covers it. Its current row is hidden, one snapshot and two noncurrent object versions remain, and a backup expires at day 120. Compute its ordinary boundaries and explain its current lifecycle state and what may be claimed.

### Exercise 3

Design an idempotent deletion workflow for an Iceberg-like table with branches, snapshots, concurrent writers, orphan files, a cache, change stream, and daily backup. Include hold freshness, preview, stable targets, tombstones, snapshot/file maintenance, retries, verification, restore, and stop conditions.

### Exercise 4

Compare selective backup rewriting, rolling backup expiry with restore-time tombstone replay, and per-subject crypto-erasure for a system promising active deletion in seven days and maximum recoverability in 45 days. State security, reliability, cost, proof, and key-granularity trade-offs and choose a design.

### Exercise 5

A merger reveals 400 unowned datasets, inconsistent lifecycle rules, stale legal-hold tags, 80 processors, and unknown notebook/model copies. Design a staged retention-and-deletion control recovery that makes progress without either mass deletion or indefinite retention. Define evidence and completion measures.

## Answers to the Exercises

### Answer 1

**Minimum retention** forbids disposition before a boundary; evidence is authoritative trigger plus rule/version and calculated not-before time. **Maximum retention** requires disposition by a boundary; evidence adds calculated not-after and applicable exception state. A **legal hold** suspends ordinary disposition for exact scope; evidence is authorized hold ID, issuer, scope, effective/review state, and propagation receipt.

A **logical delete** prevents ordinary visibility; evidence is negative query behavior plus tombstone/current-state record. A **physical delete** removes a recoverable representation at one layer; evidence is layer-specific version/reference/block outcome and verification. A **soft delete** preserves content with inactive state; evidence must call it retained and name its bounded purpose/expiry. A **tombstone** prevents replay/resurrection; evidence is consumer/restore enforcement and coverage. **Backup expiry** ends recovery from named generations on schedule; evidence is catalog/provider outcome plus restore test where appropriate. **Crypto-erasure** destroys exclusive required key material; evidence covers all key copies, mapping, plaintext absence, destruction, and threat assumptions. **Media sanitization** renders target access infeasible for a level of effort; evidence records media, method, authority, verification, disposition, and current standard basis.

### Answer 2

The ordinary not-before boundary is day $40+30=70$ and the maximum boundary is day $40+60=100$. At day 105 the item would ordinarily be overdue for disposition, but the active applicable hold blocks destructive action. Hiding the current row is logical restriction, not completed deletion. The snapshot, two noncurrent object versions, and backup remain recoverable and must be preserved while the hold applies if they are in its scope.

The organization may claim the active product path is hidden and the item is retained under hold, with known recoverable nodes and backup schedule. It may not claim physical deletion or fulfilled erasure. When authorized hold release occurs, the engine re-evaluates against the original day-40 trigger; it should then act immediately because day 100 has passed, subject to any new rule. It propagates tombstones, expires/removes eligible historical versions under safe storage procedures, and lets the backup expire no earlier than policy permits while ensuring restore-time hold/deletion replay.

### Answer 3

Pin a current policy/hold snapshot and require hold-feed freshness. Resolve stable row/item IDs and exact table generation, then preview affected rows, snapshots, branch/tag references, files, cache keys, stream consumers, and backup generations. Compare counts/bytes with bounds and require authorization. Commit durable tombstones and row-level logical deletion atomically or in a sequenced outbox so consumers cannot miss the event. Concurrent writes use item versions or tombstone checks and cannot reintroduce targets.

Expire only snapshots no longer required by retention, holds, branches/tags, readers, or recovery policy. Use the table format's atomic maintenance API. Delete files only when no valid snapshot/reference needs them. Run orphan cleanup with a safe age greater than maximum writer duration, canonical path comparison, dry run, and separate verification; never infer orphan status from age alone. Invalidate caches and require stream consumer acknowledgments. Each node stores idempotent outcome keyed by decision-set and target version; partial failures retry without widening scope.

Verification queries current/history views, inspects references and storage inventory, tests cache absence and consumer state, and records the daily backup's bounded residual window. Restore occurs in isolation, replays all tombstones since the backup point, rebuilds caches under current policy, verifies targets absent or held, and only then promotes. Stop on stale/lost holds, policy/version change, scope/count expansion, active unknown branch, path mismatch, permissions change, writer-age uncertainty, or verification disagreement.

### Answer 4

Selective backup rewriting can remove targets earlier but rewrites chains, increases cost, complicates integrity, and may weaken immutability or recovery; proof must cover old media and rewritten chain correctness. Rolling expiry keeps immutable backups simple and reliable, but targets remain recoverable until their generation ages out; restore-time tombstone replay and strict backup access are essential. Per-subject crypto-erasure can make selected ciphertext infeasible to recover quickly, but requires fine-grained exclusive keys, complete key mapping and backup-key destruction; millions of subject keys and shared records complicate operation.

A practical design promises ordinary active/queryable deletion within seven days and explicitly bounded backup recoverability no later than 45 days. Use immutable rolling backups with lifecycle-attested expiry, separate access, tombstone ledger retained past the oldest backup, and isolated restore/replay tests. For especially sensitive isolated tenant archives, add per-tenant—not falsely per-subject—crypto-erasure if key scope matches policy. Avoid selective rewriting unless a rule truly requires faster backup removal and the backup architecture can preserve integrity. Evidence includes active-node receipts, backup-generation mapping/expiry, access logs, restore-negative tests, tombstone coverage, and any key-destruction attestation.

### Answer 5

First freeze unreviewed destructive automation and prohibit new indefinite/default rules without blocking ordinary governed operations. Inventory stable dataset IDs, owners, classifications, purposes, contracts/jurisdictions, triggers, configured lifecycle, storage/history/backups, consumers/processors, notebooks, models, shares, holds, and observed access. Separate verified high-risk facts from unknowns. Reconcile hold tags with the authoritative hold system; only authorized hold roles release or narrow them.

Assign accountable remediation owners and route orphan scopes through DE-084 escalation. Establish conservative time-bounded quarantine profiles: restrict access and new copies while policy is unknown, preserve possible held data, and prioritize by sensitivity, overdue evidence, exposure, business criticality, and recoverability. Qualified authorities resolve reusable policy classes and conflicts. Simulate eligibility and effective changes before applying them. Pilot low-risk, well-known datasets through preview, tombstone, execution, verification, and restore tests; expand in bounded cohorts with stop conditions.

Require each processor to reconcile exact products/targets, subprocessors, retention, holds, deletion capability, evidence, and contract exit. Scan runtime/storage/access evidence for undeclared notebooks and exports; register or contain them. Trace models to training data and assign disposition review rather than assuming row deletion changes models. Time-bound exceptions with compensating access, monitoring, owner, deadline, and escalation.

Measure inventory, owner, classification, policy, trigger, hold, lineage, processor, notebook/model, backup and verification coverage with denominators; resolved conflicts; known eligible/held/unknown volumes and age; overdue deletion; failed nodes; effective recoverability windows; processor acknowledgments; restore-resurrection tests; exception debt; and incidents. Completion means every active scope has authoritative policy/ownership, valid holds, bounded recoverability, tested execution/restore, and reconciled outcome—or an explicit approved exception. It is neither “nothing deleted” nor “all old data purged.”
