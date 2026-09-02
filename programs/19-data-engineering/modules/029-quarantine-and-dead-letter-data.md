---
module_id: DE-029
program: Data Engineering
level: 1
module_number: 29
title: Quarantine and Dead-Letter Data
status: complete
last_verified: 2026-09-02
---

# Quarantine and Dead-Letter Data

## One-Page Review

### Governing question

How can a data pipeline contain inputs it cannot safely process, preserve enough evidence to diagnose and replay them, keep trusted outputs complete under an explicit policy, and prevent retry storms, silent loss, ordering damage, or sensitive-data exposure?

### Essential definitions

- **Quarantine** is a governed data disposition for an input that cannot enter trusted output under the current contract but remains retained, classified, owned, and potentially remediable.
- A **dead-letter queue/topic/subqueue (DLQ)** is a transport-specific destination for messages the delivery or processing policy could not complete; it is a mechanism, not a universal semantic guarantee.
- A **poison record** deterministically fails the same stage under the same relevant code/configuration and should not consume unbounded retries.
- A **transient failure** may succeed without changing input meaning after a dependency, capacity, timeout, or concurrency condition recovers.
- A **systemic failure** affects a meaningful population or invalidates pipeline assumptions and usually requires pausing/rolling back rather than routing every record individually.
- An **error taxonomy** assigns stable machine-readable class, stage, retryability, scope, severity, and owner instead of relying on exception text.
- A **quarantine envelope** links immutable original evidence to source identity/position, payload digest, error taxonomy, code/schema/configuration, attempts, security class, and resolution history.
- **redrive/replay** submits a quarantined or dead-lettered logical unit through a declared corrected processing path while preserving original identity and lineage.
- A **terminal disposition** is the current governed state of one input unit: accepted, quarantined/held, or intentionally excluded; pending retry is nonterminal.
- **mass-balance reconciliation** proves that every expected input unit resolves to exactly one current disposition at a declared boundary.
- A **quarantine budget** is an explicit count/rate/age/semantic threshold beyond which partial continuation is no longer acceptable.

### Central model, mechanism, or theorem

For expected logical input units $U$ at one manifest/range boundary, let $A$, $Q$, $X$, and $P$ be current accepted, quarantined/held, intentionally excluded, and pending sets. Require a disjoint exhaustive partition

$$
U=A\uplus Q\uplus X\uplus P.
$$

A complete run has $P=\varnothing$ and satisfies its declared policy for $Q$; zero pending records does not imply zero quarantined records. For each unit, accepted effect and current quarantine disposition are mutually exclusive, while historical quarantine attempts remain immutable after successful redrive.

The processing protocol validates identity and payload, classifies failures, retries only bounded transient cases, atomically records either accepted effect or quarantine disposition, advances source progress only after that durable routing, and replays through a new linked attempt after root-cause remediation.

### Critical invariants

- Input unit/grain, identity, payload digest, source boundary, expected population, and completion policy are explicit.
- Every expected unit has exactly one current disposition; neither accepted-and-quarantined nor silently absent is allowed.
- Original bytes/record evidence remain immutable and addressable; error extracts never replace the source payload.
- Error codes and retryability are stable taxonomies; raw exception strings are diagnostic detail, not workflow control.
- Transient retries are bounded with backoff/jitter/deadlines; deterministic, systemic, security, and programmer failures follow distinct paths.
- Quarantine/DLQ publication and source acknowledgement/checkpoint obey a durability protocol; failure cannot acknowledge a unit whose accepted or contained evidence is absent.
- Batch/transaction/order invariants decide whether record-level continuation is permitted; quarantine is not a license to publish an invalid partial state.
- Replay preserves logical occurrence identity, uses versioned corrected code/configuration, and cannot duplicate an already accepted effect.
- Historical quarantine evidence, attempts, decisions, and resolutions remain auditable even when current disposition changes after redrive.
- Access, encryption, retention, deletion, and display sanitization reflect that error stores often contain the most sensitive or malformed payloads.
- Counts, rates, age, reasons, owners, replay outcomes, and unresolved backlog reconcile and alert before containment capacity is exhausted.

### Common failures

Catching every exception and continuing; retrying deterministic parse errors forever; routing infrastructure outages as millions of bad records; acknowledging the source before DLQ publication; writing only exception text without original identity; copying truncated payload fragments as evidence; treating broker delivery-attempt counts as exact across products; configuring a DLQ with no subscription/owner/retention alarm; dropping ordered messages and continuing blindly; publishing a batch that violates cross-record controls; redriving before deploying a fix; assigning new occurrence IDs on replay; deleting originals when replay begins; recursively dead-lettering the DLQ; logging secrets/PII in error detail; silently expiring unresolved records; or claiming success because the main output job completed.

### Compact example

Four logical units arrive in six deliveries. Unit `a` is accepted, `b` has a deterministic parse error and is quarantined, `c` suffers one transient failure then succeeds, `d` enters a policy hold, and a repeated delivery of `a` is a no-op. Current state is two accepted plus two quarantined, with no pending unit and exact mass balance. After parser remediation, `b` redrives under the same occurrence identity, becomes accepted once, and retains its original quarantine/history record; `d` remains held.

### Connections

[DE-022](022-watermarks-and-high-water-marks.md) governs acknowledgement progress, [DE-023](023-file-arrival-and-manifest-processing.md) defines expected populations and atomic publication, [DE-026](026-database-change-data-capture.md) supplies ordered occurrences, [DE-027](027-idempotent-loads.md) makes redrive replay-safe, and [DE-028](028-deduplication-and-record-identity.md) separates replay from identity conflict. The next module designs replayable raw ingestion.

## Governing Question

What evidence permits a pipeline to continue after one input fails, while proving that the input was neither lost nor admitted into trusted output, that retry policy matches the failure, and that later remediation cannot duplicate or reorder effects?

Data pipelines meet malformed encodings, schema drift, domain violations, expired credentials, rate limits, corrupt compression, missing reference data, target constraints, code defects, security attacks, and infrastructure outages. These conditions are not interchangeable. A parser error in one record might be isolated safely. A schema registry outage is not evidence that every record is bad. An invariant violation across a financial batch may make all record-level continuation unsafe.

Quarantine is an accountable state, not an exception-catching convenience. It retains the original evidence, explains why trust was withheld, assigns ownership and a deadline, and supports a controlled decision: correct and replay, exclude under policy, repair upstream, or permanently retain/delete under governance. A dead-letter facility may carry that state, but broker semantics alone do not define it.

Continuation changes the meaning of “success.” If 99,990 of 100,000 records land and ten are quarantined, the run may be operationally complete under a contract that permits bounded record loss from the trusted view and exposes the ten explicitly. It is not semantically equivalent to a complete source snapshot if totals, relationships, or transactions require all 100,000. The policy must predate the incident.

The governing question is therefore end to end: identity, error classification, transactional routing, progress acknowledgement, semantic completeness, secure evidence, operational ownership, and replay all need one coherent protocol.

## Why This Matters

Without bounded containment, one poison record can stall an entire stream or trigger infinite retry, cost, and alert noise. Without fail-closed batch semantics, catching that record can silently corrupt totals, referential integrity, or transaction state. Both extremes are common because the failure unit was never matched to the data invariant.

DLQs can become data graveyards. Messages accumulate without consumers, dashboards, retention analysis, or replay tooling. The primary pipeline looks green because difficult records left its path, while the unresolved backlog ages beyond source, schema, or legal retention. “Sent to DLQ” is not a terminal business outcome.

Acknowledgement ordering creates loss risk. If a consumer acknowledges a source message and then fails to write its quarantine envelope, neither trusted output nor contained evidence exists. If it writes containment and crashes before acknowledging, the source redelivers; stable identity and idempotent quarantine receipts make that safe.

Error stores concentrate risk. Malformed records can contain oversized values, injection strings, credentials mistakenly placed in fields, prohibited personal data, or payloads designed to exploit viewers and replay tools. Dumping raw bytes and stack traces into broadly readable logs expands the incident.

Replay can cause a second failure. A “fixed” parser can still produce a different entity identity, double an earlier partial effect, violate current schema, or overwhelm downstream systems. Safe redrive must bind to the original unit, record corrected processing versions, stage/validate output, and reconcile before closing the case.

Good containment also improves producers. Stable reason codes, counts, source positions, examples, and age reveal whether defects originate in one producer release, schema, tenant, partition, or code deployment. The feedback loop is impossible when errors are free-form logs detached from source identity.

## Prerequisites and Retrieval

Retrieve the dataset/product owner; source owners; input grain and logical identity; source system/epoch, topic/queue/subscription, partition/offset, file/object version, manifest, CDC transaction, or request identity; payload digest and immutable raw location; expected input population; transaction and ordering boundaries; schemas/contracts and compatibility policy; parsing/validation stages; cross-record controls; accepted/excluded/quarantine definitions; retryable error classes; infrastructure dependencies; provider DLQ semantics; delivery count meaning; acknowledgement/checkpoint behavior; atomic transaction/outbox capability; visibility/ack deadlines; backoff, jitter, maximum attempts, elapsed deadline, and circuit breaker; error taxonomy; envelope schema; reason/detail length; stack-trace policy; code/config/schema/reference-data versions; owner and service level; quarantine budgets; capacity and retention; encryption and access; tenant separation; classification and privacy; malware/content scanning; log sanitization; replay authorization; corrected transformation selection; idempotency receipts; ordering recovery; downstream restatement; reconciliation controls; audit; deletion/legal hold; disaster recovery; and incident/runbook procedures.

Distinguish malformed payload from unsupported schema; domain invalidity from missing reference data; deterministic failure from repeated observation; transient dependency from permanent business rejection; one-record defect from systemic code/configuration failure; poison record from slow/large valid record; quarantine from ordinary retry; DLQ transport from semantic disposition; current disposition from immutable attempt history; original bytes from rendered/error excerpt; error code from exception message; source delivery count from exact processing attempt count; failure timestamp from event time; acknowledgement from accepted effect; contained input from successfully completed dataset; replay from new business event; corrected processing from payload mutation; exclusion from deletion; resolved case from erased evidence; and operational success from semantic completeness.

Build a failure policy matrix before enabling continuation:

| Failure class | Typical evidence | Default action | Completion effect |
|---|---|---|---|
| Transient dependency/capacity | timeout, throttling, unavailable dependency, retryable conflict | bounded retry with backoff/jitter; circuit break on population | pending until success or reclassified |
| Deterministic record/content | reproducible parse/type/domain failure for one unit | quarantine with immutable raw pointer and stable reason | allowed only within declared record-level budget |
| Contract/schema incompatibility | unknown schema/version or incompatible required field | pause scope or quarantine governed units; coordinate producer | often blocks batch/source generation |
| Systemic code/config defect | sudden high common failure after deployment | stop/rollback/circuit; do not flood DLQ | blocks affected scope |
| Security/policy signal | malicious content, cross-tenant identity, prohibited data | isolate, restrict, notify incident/privacy owner | blocks or holds under policy |
| Cross-record invariant | totals, transaction, keys, relationships fail | quarantine/fail atomic batch or generation | blocks publication unless partial semantics explicit |
| Intentional exclusion | documented out-of-scope record with reason | record exclusion receipt | may count as terminal $X$ |

The matrix is versioned and tested. Operators may override only through an audited decision that records reason, scope, expiry, and owner.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish retry, quarantine, dead-letter routing, exclusion, security hold, and systemic stop;
2. define input units and prove mass balance across current dispositions;
3. design stable error taxonomies and evidence-rich, privacy-aware quarantine envelopes;
4. order accepted/quarantine durability and source acknowledgement safely;
5. select record-, transaction-, partition-, or batch-level containment from semantic invariants;
6. prevent retry storms with bounded attempts, elapsed deadlines, backoff, jitter, and circuit breaking;
7. handle poison records without silently violating stream order or checkpoint meaning;
8. redrive immutable originals idempotently under corrected versioned processing while retaining history;
9. operate capacity, retention, access, age, ownership, reconciliation, and producer feedback; and
10. test crash points, systemic faults, sensitive payloads, provider edge cases, and replay correctness.

## Core Exposition

### Define the input and containment boundary

Choose the smallest unit that can be classified without violating atomic meaning: one event occurrence, source record, file row, source transaction, file/partition, or complete snapshot generation. Do not default to row-level quarantine when the source commits multi-row transactions or the output contract requires cross-row completeness.

Bind the unit to namespaced identity and payload digest as [DE-028](028-deduplication-and-record-identity.md) describes. A failed delivery attempt is not a new unit. If the same identity arrives with different bytes, classify identity conflict rather than overwrite quarantine evidence.

Define the trust boundary. Raw landing may accept opaque bytes while standardized output requires parse/schema/domain validity. “Accepted to raw” and “accepted to curated” are separate dispositions at separate stages. The envelope names the failing stage and upstream accepted boundary.

### Separate quarantine from DLQ mechanics

Quarantine is a data/product control: it says the unit is outside a named trusted output under a current decision, retains evidence, and has ownership/resolution semantics. A DLQ is a queue/topic/subqueue behavior offered by a messaging or connector system. A DLQ can implement part of quarantine transport; quarantine can also be a database table, immutable object generation, or governed error dataset.

Provider behavior differs. Amazon SQS configures movement through `maxReceiveCount` and warns that a DLQ can break exact FIFO operation order. Google Cloud Pub/Sub documents that forwarding occurs after an approximately configured number of delivery attempts and may wrap the original message. Azure Service Bus documents a dead-letter subqueue without automatic cleanup and states that TTL is not observed inside it. Confluent Cloud sink connectors describe DLQ topics for serialization/deserialization errors while the connector continues.

Therefore retrieve actual provider/version/configuration, IAM, envelope transformation, attempt counting, retention, ordering, redrive, and observability. Never write a portable correctness proof from the label “DLQ.”

### Design a stable error taxonomy

Use a controlled code such as `PARSE.INVALID_UTF8`, `SCHEMA.UNKNOWN_ID`, `DOMAIN.NEGATIVE_AMOUNT`, `REFERENCE.MISSING_KEY`, `DEPENDENCY.TIMEOUT`, `TARGET.CONSTRAINT`, `SECURITY.TENANT_MISMATCH`, or `INVARIANT.BATCH_TOTAL`. Codes are versioned and documented with owner, retryability, scope, severity, and expected remediation.

Exception class/message/stack fingerprint can be diagnostic fields. They should not decide retry because wording changes across libraries, versions, locales, and nested causes. Map unknown exceptions conservatively to programmer/systemic failure, not automatically to record quarantine.

RFC 9457 defines machine-readable problem detail objects for HTTP APIs and extension members. A pipeline error envelope can borrow the principle of stable type/code plus occurrence-specific detail, while remaining its own data contract. Do not expose internal stacks or sensitive values merely because the structure supports extensions.

### Classify before retrying

Retry only when another attempt can plausibly change the outcome without changing logical input meaning. Network timeout, rate limit, lock conflict, or temporarily unavailable schema service may qualify. Invalid UTF-8 bytes will not heal through sleep. A missing reference row might be transient if its publication is known in progress, or deterministic if the source contract forbids it.

Classification depends on stage and dependency evidence, not only exception type. A database timeout after commit may be an ambiguous success requiring receipt lookup, not a fresh mutation. An HTTP 500 might repeat a deterministic request bug. A validation exception appearing in 80% of one producer release is systemic even if each record can be individually described.

Record classifier version and inputs. If later evidence changes retryability, reclassify through an audited event rather than mutate history.

### Bound retry by attempts and elapsed time

Use exponential or otherwise governed backoff, jitter to avoid synchronized retries, maximum attempts, maximum elapsed time, per-attempt timeout, and an overall deadline. Respect dependency-provided retry hints where trusted. Limit concurrency and isolate retry capacity from fresh traffic when appropriate.

Attempt count alone is not enough. Ten retries in one second differ from ten over a day. A worker crash before recording an attempt can make application counts differ from broker delivery counts. Provider counts may be approximate. Persist your own attempt evidence when exact operational history matters.

A simple exponential schedule may be

$$
d_i=\min(d_{max},d_0 2^{i-1})+J_i,
$$

where $J_i$ is bounded jitter. This is an example, not a universal optimal policy. Budget worst-case queue residence, downstream deadlines, and dependency recovery characteristics.

### Detect systemic failure before flooding containment

Quarantining every record during a schema registry outage, expired target credential, broken deployment, or missing reference snapshot misclassifies healthy input and can exhaust the DLQ. Aggregate failures by code, stage, producer/schema, deployment, partition, and time. Trip a circuit when count/rate/common fingerprint or invariant thresholds indicate systemic scope.

A circuit moves the affected source/partition/pipeline to pending/paused state, preserves source retention/lease safety, alerts an owner, and probes recovery deliberately. It does not acknowledge unread data as quarantined merely to keep dashboards green.

Use a quarantine budget such as maximum fraction, absolute count, age, high-severity count, or affected key domain. A single prohibited security record may block publication even if the numeric rate is tiny; 100 optional telemetry defects may be permitted. Semantic severity outranks one global percentage.

### Construct an evidence-rich quarantine envelope

Include:

- quarantine record ID and logical input identity/namespace;
- immutable raw object/reference, source coordinates, payload size, and digest;
- safe preview only when policy permits, never as the authoritative original;
- source producer, tenant, schema/event type/version, and event/valid/ingestion times;
- failing pipeline, stage, transform, deployment/code/configuration/reference-data versions;
- stable error code/version, retryability, scope, severity, safe detail, exception fingerprint;
- first/last seen, attempt IDs/counts/timing, broker metadata, and prior dispositions;
- batch/transaction/manifest and expected-population lineage;
- security classification, access policy, encryption key domain, retention/deletion/legal hold;
- owner, service level, incident/ticket, next action, and review deadline; and
- replay generation/attempt, corrected processing version, outcome, target receipt, and resolution.

Keep the envelope schema itself evolvable. Required identity/digest/error fields must remain decodable across upgrades. Large raw payloads usually belong in immutable governed storage referenced by digest/version, not embedded repeatedly in queue headers.

### Preserve the original without trusting it

Original bytes are evidence because parsing/normalization may be the defect. Store them before lossy conversion and bind them to a cryptographic digest plus source identity. Do not mutate the original “in place” during manual repair.

Evidence need not be broadly readable. Store raw in a restricted zone; expose minimized metadata and safe redacted samples to ordinary operators. Viewers must escape control characters and markup, bound sizes, avoid formula/terminal/log injection, and prevent automatic execution/deserialization.

If remediation changes data, create a corrected derivative with author, reason, rule/tool, timestamp, approval, and link to original. Decide whether producer correction or consumer repair is authoritative. Replaying silently hand-edited bytes under the old digest destroys lineage.

### Route accepted and contained effects atomically

For unit $u$, the processing transaction should produce either accepted effects plus receipt or quarantine disposition plus receipt under one current state, then acknowledge source progress. A common design writes immutable raw first, processes from raw, and transactionally updates output/disposition/checkpoint metadata. Another uses a database transaction/outbox to publish containment.

Let $D_A(u)$ and $D_Q(u)$ mean durable accepted and quarantine current disposition. Before acknowledgement require

$$
D_A(u)\oplus D_Q(u),
$$

where $\oplus$ denotes exactly one. Intentionally excluded units use their own durable $D_X$ state. Pending retry is not acknowledged past an unrecoverable source boundary unless authoritative raw permits replay.

If accepted output and broker DLQ cannot share a transaction, land source once in authoritative raw storage and derive both idempotently, or use an outbox/receipt protocol. Sending to DLQ followed by source acknowledgement still has a crash gap unless both outcomes are recoverable by identity.

### Reconcile all current dispositions

At boundary $b$, let $U_b$ be expected unique logical units and current dispositions $A_b,Q_b,X_b,P_b$. Require disjointness and exhaustion:

$$
U_b=A_b\uplus Q_b\uplus X_b\uplus P_b.
$$

For run completion, $P_b=\varnothing$. Policy may require $Q_b=\varnothing$, or permit bounded categories/counts with explicit degraded status. Exclusion $X_b$ must come from versioned scope/policy, not convenient error swallowing.

Reconcile identities, not only counts. Equal totals can hide a unit present in both accepted and quarantine plus another absent from both. Check exact key sets/digests, batch/transaction completeness, source ranges, and downstream effects.

Historical attempt/quarantine rows do not violate current disjointness after redrive. The logical unit's current disposition becomes accepted, while the original quarantine record has resolution `accepted_by_replay` and remains linked.

### Choose record, transaction, or batch quarantine

Record-level continuation is appropriate when records are semantically independent, accepted records remain valid alone, controls permit partial output, and consumers can interpret degraded completeness. Examples may include optional telemetry or independent enrichment fields.

Quarantine the whole transaction when atomic source changes must remain together. A CDC transaction that debits one account and credits another cannot publish only the parsable row. Preserve transaction envelope and every member, including those that parsed, so replay reconstructs the commit.

Quarantine or fail the file/partition/generation when manifest completeness, schema uniformity, control totals, unique keys, cross-row relationships, or snapshot equivalence fails. A thousand individually valid rows do not redeem a missing trailer or mismatched total.

Document whether a contained child blocks parent publication. Parent manifests enumerate current outcomes; they never omit failed children and still claim completeness.

### Protect ordering and causality

Skipping a poison event in an ordered stream allows later events to observe a state that never existed. For an entity, update version 8 may depend on version 7; quarantining 7 and applying 8 can be invalid even if 8 parses.

Options include parking the affected partition/key while other independent keys continue; retaining later events behind a per-key gap; quarantining the full transaction/range; applying an explicit compensating/snapshot reconstruction; or accepting out-of-order semantics only when the consumer contract supports version-aware independent events.

AWS explicitly warns against DLQ use with FIFO queues when moving a message would break exact order. Generalize the concern, not the product implementation: record the order domain, gap, blocked successors, source retention, and recovery plan.

Checkpoint cannot leap over an unrecoverable quarantined event if downstream replay needs the original stream order. Authoritative raw plus per-key/version logic can decouple broker progress, but raw then owns retention and ordering evidence.

### Handle schema and contract failures deliberately

Unknown schema ID may be transient during registry propagation, permanent after retention loss, or a security problem if the ID is unauthorized. Preserve original serialized bytes and writer metadata. Do not decode using “closest” schema and quarantine only fields that fail.

Compatible schema evolution can route through versioned readers. Incompatible required changes often block a producer/version scope rather than create endless per-record DLQ entries. Coordinate contract rollout and source retention so corrected consumers can replay.

Record whether failure occurred before or after identity extraction. If the payload cannot be parsed enough to derive occurrence ID, use transport coordinates and object digest as provisional identity; never generate a fresh random identity on every delivery.

### Treat programmer and invariant failures as stop signals

Null dereference, assertion failure, impossible state, corrupted lookup, or unexpected output constraint often indicates code/system defects. Catching `Exception` and labeling the current record bad can contaminate all following output.

Apache Beam's `with_exception_handling` can produce good and bad outputs and includes threshold controls. The operator must still choose exception classes, partial behavior, thresholds, windowing, and error handling consistent with semantics. A library feature cannot decide whether continuation is safe.

Fail the affected atomic unit, preserve input and execution evidence, roll back untrusted output, trip a circuit when scope is uncertain, and reproduce in a protected environment. Only reclassify as record-specific after evidence.

### Isolate security and policy events

Malformed input can be hostile. Excessive nesting, decompression bombs, huge fields, parser exploits, path/object injection, formula injection, cross-tenant identifiers, prohibited data, secrets, and malware need bounded parsing and security containment—not routine operator download/redrive.

Use separate access domains and reason codes for security/privacy holds. Scan where appropriate, restrict viewers/replay roles, require approvals, log access, and avoid reflecting raw content into alerts, tickets, dashboards, or command lines.

OWASP logging guidance lists access tokens, passwords, keys, connection strings, and sensitive personal data among values that usually should not be recorded directly and recommends removal/masking/sanitization/hashing/encryption as appropriate. A quarantine store may need raw evidence, but that evidence belongs in controlled storage; diagnostic logs and previews should be minimized.

NIST SP 800-92 frames log management as generation, transmission, storage, access, and disposal of log data. Apply comparable lifecycle discipline to error metadata while recognizing that raw quarantined payload is governed data, not merely a log.

### Make redrive a new linked processing attempt

Do not press “replay all” first. Identify root cause and affected population; deploy/version the correction; reproduce on representative quarantined inputs; assess changed semantics; plan rate/capacity/order; choose exact identities; and define success/reconciliation/rollback.

Redrive reads immutable originals or approved corrected derivatives and preserves logical occurrence identity. It creates a new processing attempt/replay generation linked to the quarantine record, code/schema/config/reference versions, author/approval, start/end positions, and target receipt.

[DE-027](027-idempotent-loads.md) supplies the effect-plus-receipt rule: if a unit partially or ambiguously succeeded before containment, replay must query stable target identity and avoid a second effect. New random event IDs defeat this protection.

Do not delete/move the original out of quarantine before confirmed target effect and current-disposition transition. Mark resolution, retain evidence per policy, and make replay itself retryable. If replay fails differently, append an attempt/error event; do not overwrite the first diagnosis.

### Redrive in governed cohorts

Select records by immutable manifest of quarantine IDs/digests, source range, reason code/version, producer/schema/deployment, and time—not a mutable dashboard query with no snapshot. Record selection query and result manifest.

Canary a small representative cohort, compare proposed accepted outputs and controls, then increase rate. Respect original key/partition ordering or explicitly rebuild current state from a complete range. Isolate redrive capacity from live ingestion to prevent recovery from causing a new outage.

After redrive reconcile selected count, accepted/currently quarantined/excluded/pending outcomes, target effect identities, source/batch controls, downstream restatements, and quarantine resolution records. Partial redrive success remains visible.

### Operate retention and capacity

Retention must cover diagnosis, remediation, schema/code availability, replay, audits, producer correction, disaster recovery, and legal/privacy obligations. Broker defaults may not. Azure Service Bus documents no automatic DLQ cleanup and no TTL observation inside the DLQ; indefinite accumulation is still not a safe retention policy.

Track records, bytes, oldest age, growth rate, available capacity, and projected exhaustion:

$$
t_{exhaust}=\frac{B_{free}}{r_{in}-r_{out}},\qquad r_{in}>r_{out}.
$$

This estimate assumes stable rates and usable capacity; burst, object overhead, quotas, and compaction can invalidate it. Alert well before exhaustion and apply the systemic circuit rather than drop new errors.

Retention expiry is a governed resolution only when policy authorizes it and evidence records deletion scope/reason. Never let unresolved data disappear silently due to queue or bucket lifecycle.

### Assign ownership and service levels

Every reason/source domain has an owner: producer team, pipeline team, schema/reference owner, security/privacy, or data steward. Routing rules should page/queue the right owner without exposing sensitive content.

Define time to detection, classification, owner acknowledgement, remediation, redrive, and downstream correction. Prioritize by semantic harm, age, volume, source retention, customer/legal deadline, and blocked successors—not only record count.

An empty DLQ can mean health, misconfiguration, missing permissions, or silent discard. Test the path with safe synthetic failures and verify source, containment, metrics, alerts, access, and replay end to end.

### Observe rates, age, and transitions

Measure input units, accepted, quarantined, excluded, pending, duplicate deliveries, transient attempts, systemic circuits, unknown error codes, reason/stage/producer/schema/deployment distribution, first/oldest age, bytes, replay selection/success/failure, recurrence after fix, and downstream restatement.

Use both counters and exact reconciliation. Provider attempt counters can be approximate; Pub/Sub documents best-effort forwarding around an approximately configured maximum. Operational charts should not imply exact policy enforcement when the provider does not promise it.

Alert on sudden rate change, first occurrence of severe class, unknown taxonomy, oldest-age breach, growth/capacity risk, owner SLA, repeated redrive failure, accepted-and-quarantined overlap, missing disposition, and unexpected zero volume.

### Test every crash and policy boundary

Inject crash before/after raw write, accepted effect, quarantine write, disposition receipt, checkpoint, source acknowledgement, replay effect, and resolution update. Verify duplicate delivery yields one current disposition/effect and retained attempt history.

Test exact retry thresholds, elapsed deadline, jitter bounds, provider count reset/approximation, circuit thresholds, empty/one/all-record failure, large error bursts, unknown exception, dependency outage, schema outage, code regression, and recovery.

Test ordered keys/transactions, predecessor quarantine with later successors, whole-file totals, referential dependencies, partial output visibility, backfill overlap, redrive selection snapshot, canary/full cohorts, replay rollback, and downstream restatement.

Test oversized/malformed/hostile payloads, decompression limits, unsafe characters, secret/PII previews, cross-tenant routing, permission denial, encryption/key rotation, retention expiry, legal hold, disaster restore, and audit access.

## Definitions and Notation

Let:

- $U_b$ be expected unique logical input units at boundary $b$;
- $u$ be one logical unit and $O(u)$ its stable occurrence identity;
- $h(u)$ be immutable original payload digest;
- $A_b$ be units currently accepted into the named trusted boundary;
- $Q_b$ be units currently quarantined or held;
- $X_b$ be units intentionally excluded by governed scope/policy;
- $P_b$ be units pending initial work or transient retry;
- $H(u)$ be immutable disposition/attempt history;
- $D(u)$ be current disposition;
- $e(u)$ be stable error taxonomy code and version;
- $a_i(u)$ be physical processing attempt $i$;
- $C$ be source checkpoint/acknowledgement progress;
- $R$ be the greatest source boundary recoverable from raw/accepted/quarantine evidence;
- $B_{free}$ be usable containment capacity; and
- $r_{in},r_{out}$ be quarantine arrival and resolution byte rates.

Mass balance at a snapshot requires

$$
U_b=A_b\uplus Q_b\uplus X_b\uplus P_b.
$$

Equivalently, for every $u\in U_b$, exactly one current disposition predicate is true:

$$
\mathbf{1}_{A_b}(u)+\mathbf{1}_{Q_b}(u)+\mathbf{1}_{X_b}(u)+\mathbf{1}_{P_b}(u)=1.
$$

Completion requires $P_b=\varnothing$ plus the declared constraints on $Q_b$ and $X_b$. A permitted nonempty $Q_b$ produces an explicitly degraded/partial semantic status, not an unqualified completeness claim.

Source progress requires

$$
C\preceq R,
$$

where recoverability includes identity, payload, schema, ordering, and replay evidence—not merely an error counter.

Current state and history differ. A redrive can transition

$$
D(u):quarantined\rightarrow accepted
$$

while $H(u)$ remains append-only and records original failure, remediation, replay attempts, and resolution.

## Mechanisms, Invariants, or Proof Structure

**Conditional disposition-conservation theorem.** Suppose $U_b$ is an exact expected identity set; every processing transition atomically commits one current disposition/receipt for $u$ (and any accepted effect), uniqueness prevents concurrent conflicting dispositions, source progress never exceeds recoverable evidence, and transitions preserve immutable history. Then each $u\in U_b$ is neither silently lost nor double-counted at current state, and accepted/quarantined/excluded/pending sets form a disjoint exhaustive partition. Completion claims can be evaluated from $P_b$ and declared $Q_b/X_b$ policy.

**Proof sketch.** Initially every expected unit is pending. A valid atomic transition removes it from one current set and inserts it into exactly one next set under a unique identity constraint; abort changes neither. Induction over transitions preserves membership count one. Accepted effects share their accepted disposition, and quarantine/exclusion receipts share their states. Replay transitions current quarantine to accepted once while appending history. Exact reconciliation against $U_b$ establishes exhaustion. The theorem does not prove that $U_b$, the classifier, policy, accepted transformation, or original source is correct.

**Identity invariant.** One namespaced $O(u)$ binds to one $h(u)$. Equal identity/equal digest is redelivery; equal identity/unequal digest is conflict.

**Raw-evidence invariant.** Immutable original bytes/record and source coordinates remain recoverable or an approved derivative explicitly preserves the transformation and lineage. Preview/detail is never the sole evidence.

**Taxonomy invariant.** Stable machine code/version controls workflow; exception text and stack fingerprint add bounded diagnostics. Unknown/systemic exceptions fail conservatively.

**Retry invariant.** Only classified transient failures retry, within attempts, elapsed deadline, backoff, jitter, concurrency, and dependency/circuit budgets.

**Atomic-routing invariant.** Accepted effect/current accepted receipt or current quarantine/exclusion receipt becomes durable before source acknowledgement; mutually exclusive current states share one transition protocol.

**Semantic-boundary invariant.** Record continuation is allowed only when transaction, order, batch totals, relationships, and consumer completeness remain valid under explicit degraded-output policy.

**Progress invariant.** $C\preceq R$. Acknowledged source history always resolves through authoritative raw, accepted effect, or containment evidence sufficient for replay.

**Replay invariant.** Redrive preserves logical occurrence identity, links corrected code/config/schema and selection manifest, produces at most one accepted effect, and appends rather than erases history.

**Security invariant.** Raw error payload, preview, envelope, logs, tickets, viewer, and replay path each enforce classification, tenant isolation, access, output encoding, size limits, retention, and audit.

**Capacity invariant.** Quarantine cannot silently exceed storage, queue, age, owner, or replay capacity; systemic controls activate before evidence loss.

**Reconciliation boundary.** Disposition conservation proves accounted routing for declared $U_b$. It does not prove source completeness, accepted correctness, policy legitimacy, or resolution quality.

<!-- bijux-verify: {"id":"quarantine-disposition-redrive","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"deliveries=6\nunique_units=4\naccepted_before_redrive=2\nquarantined_before_redrive=2\npending_before_redrive=0\nduplicate_deliveries=1\ntransient_retries=1\nmass_balance=True\nredrive_accepted=True\nquarantine_history_retained=True\nidempotent_redrive=True\nremaining_quarantine=1\n","stderr":""}} -->
```python
from hashlib import sha256

units = {
    "a": "10",
    "b": "bad",
    "c": "20",
    "d": "policy-hold",
}

class Router:
    def __init__(self):
        self.bindings = {}
        self.disposition = {key: "pending" for key in units}
        self.output = {}
        self.attempts = {key: 0 for key in units}
        self.history = {key: [] for key in units}
        self.quarantine = {}
        self.duplicate_deliveries = 0
        self.transient_retries = 0

    def route(self, key, fixed=False):
        payload = units[key]
        digest = sha256(payload.encode()).hexdigest()
        if key in self.bindings and self.bindings[key] != digest:
            raise ValueError("identity reused with different payload")
        self.bindings[key] = digest

        if self.disposition[key] == "accepted":
            self.duplicate_deliveries += 1
            self.history[key].append("accepted-replay")
            return

        self.attempts[key] += 1
        if key == "c" and self.attempts[key] == 1:
            self.transient_retries += 1
            self.history[key].append("dependency-timeout")
            return

        if payload == "bad" and not fixed:
            self.disposition[key] = "quarantined"
            self.quarantine.setdefault(key, {"original": payload, "resolved": False})
            self.history[key].append("parse-invalid-integer")
            return

        if payload == "policy-hold":
            self.disposition[key] = "quarantined"
            self.quarantine.setdefault(key, {"original": payload, "resolved": False})
            self.history[key].append("policy-hold")
            return

        value = 30 if key == "b" and fixed else int(payload)
        self.output[key] = value
        self.disposition[key] = "accepted"
        if key in self.quarantine:
            self.quarantine[key]["resolved"] = True
        self.history[key].append("accepted")

router = Router()
delivery_ids = ("a", "b", "c", "c", "d", "a")
for unit_id in delivery_ids:
    router.route(unit_id)

before = dict(router.disposition)
accepted_before = sum(value == "accepted" for value in before.values())
quarantined_before = sum(value == "quarantined" for value in before.values())
pending_before = sum(value == "pending" for value in before.values())
duplicates_before = router.duplicate_deliveries
mass_balance = accepted_before + quarantined_before + pending_before == len(units)

router.route("b", fixed=True)
after_redrive = dict(router.output)
attempts_after_redrive = router.attempts["b"]
router.route("b", fixed=True)
idempotent_redrive = (
    after_redrive == router.output
    and attempts_after_redrive == router.attempts["b"]
    and router.history["b"][-1] == "accepted-replay"
)
remaining = sum(value == "quarantined" for value in router.disposition.values())

print(f"deliveries={len(delivery_ids)}")
print(f"unique_units={len(router.disposition)}")
print(f"accepted_before_redrive={accepted_before}")
print(f"quarantined_before_redrive={quarantined_before}")
print(f"pending_before_redrive={pending_before}")
print(f"duplicate_deliveries={duplicates_before}")
print(f"transient_retries={router.transient_retries}")
print(f"mass_balance={mass_balance}")
print(f"redrive_accepted={router.disposition['b'] == 'accepted'}")
print(f"quarantine_history_retained={'b' in router.quarantine and router.quarantine['b']['resolved']}")
print(f"idempotent_redrive={idempotent_redrive}")
print(f"remaining_quarantine={remaining}")
```

The executable fixture models four known logical units, deterministic and policy quarantine, one transient retry, exact current-disposition accounting, an immutable original field, linked resolution, and replay-safe accepted output. It uses in-memory state and a hard-coded correction; it does not prove durable atomicity, concurrent uniqueness, broker acknowledgements, secure storage, ordering, classifier correctness, or production replay.

## Alternatives and Trade-Offs

**Stop on first error versus record-level continuation.** Stopping protects unknown atomic/invariant boundaries but reduces availability. Continuing isolates independent defects but can publish semantically incomplete data. Choose from grain and consumer contract, not tolerance convenience.

**Broker DLQ versus governed quarantine dataset.** Provider DLQs integrate delivery attempts and operations. A governed store provides richer envelopes, query/reconciliation, access, and long retention. Many systems land broker DLQ records promptly into governed quarantine while preserving broker metadata.

**Embed raw payload versus immutable pointer.** Embedding eases standalone debugging but duplicates sensitive/large data and header limits. Pointers reduce duplication but require durable object version/digest, access, and co-retention. Store enough safe metadata to diagnose missing objects.

**Retry count versus elapsed deadline.** Counts are simple but ignore attempt spacing and long outages. Deadlines bound latency; combining both plus backoff/jitter is usually clearer. Provider counters may still be approximate.

**Per-record DLQ versus circuit breaker.** Per-record routing handles sparse deterministic defects. Circuits prevent systemic outages from becoming massive quarantines, at the cost of pausing healthy subsets if scope detection is coarse.

**Preserve order by blocking versus skip and compensate.** Blocking keeps causal semantics but raises lag/source retention. Skipping improves throughput but requires independent/version-aware events or later reconstruction and explicit gaps. FIFO labels alone do not choose.

**Original-only replay versus approved correction.** Replaying originals proves code/config remediation. Some source defects need corrected derivatives; those require authorship, lineage, approval, changed digest, and producer/governance rules.

**Manual redrive versus automated policy.** Manual approval suits high-risk, rare, ambiguous cases but creates age/backlog. Automated replay of known transient/fixed classes scales if version/selection/idempotency gates are strong and rollback exists.

**Retain forever versus governed expiry.** Long retention improves diagnosis/rebuild but increases cost/privacy exposure. Expiry is acceptable only after resolution and policy evidence, or with a rebootstrap source; queue defaults are not governance.

**Detailed error payload versus minimized diagnostics.** Rich context accelerates diagnosis but broadens sensitive-data/injection risk. Keep raw restricted and expose safe typed metadata/previews by role.

**Same queue redrive versus new replay generation.** Direct movement is operationally easy but can erase selection/version evidence or loop. A replay generation with immutable manifest and receipts supports canarying, rate control, audit, and reconciliation.

## Failure Modes and Misconceptions

**“DLQ means the data is safe.”** It may have different retention, IAM, ordering, wrapping, attempt, cleanup, and durability behavior. Verify end-to-end evidence and ownership.

**“Quarantined means processed successfully.”** It means trust was withheld and evidence retained. Dataset completion depends on declared semantics/budget.

**“Every exception belongs in quarantine.”** Code bugs and systemic outages often require stop/rollback; security signals require controlled isolation; transient failures should retry.

**“Retry until it works.”** Deterministic inputs will not heal, and systemic retry storms can extend outages. Bound and classify retry.

**“Maximum delivery count is exact.”** Provider semantics differ; Pub/Sub documents approximate maximum attempts. Maintain claims within the provider contract.

**“One low error percentage is always acceptable.”** A single missing transfer half, deletion, tenant violation, or regulated record can invalidate output. Use semantic budgets.

**“Record quarantine preserves transactions.”** Splitting an atomic source transaction exposes impossible state. Contain/replay the required transaction unit.

**“Later events can always pass a poison record.”** Ordered/keyed state may depend on it. Park successors or use proven independent/version semantics.

**“Exception text is an error contract.”** Messages change and may contain sensitive values. Use stable taxonomy plus safe detail.

**“The stack trace contains enough evidence.”** It may omit original bytes, source identity, schema, code/config, and batch context. Use a structured envelope.

**“Copy the bad row from logs for replay.”** Logs can truncate, escape, redact, sample, or mutate content. Replay immutable source/raw evidence or approved derivative.

**“A random replay ID prevents duplicates.”** It makes the original look new. Preserve logical occurrence identity and target receipts.

**“Remove from DLQ before replay to avoid duplicates.”** Replay can fail after removal. Retain original and mark resolution only after reconciled effect.

**“Replay all after the fix.”** The cohort can include unrelated reasons, versions, tenants, or security holds. Select immutable governed manifests and canary.

**“Resolved means delete history.”** Historical failure/remediation evidence supports audit, recurrence analysis, and correction. Apply governed retention, not erasure by convenience.

**“Raw quarantine can be widely accessible because it is operational.”** It often contains the riskiest data. Restrict it more strongly than normal curated data where appropriate.

**“An empty DLQ proves health.”** Permissions, routing, metrics, or producers may be broken. Exercise the path synthetically and reconcile source identities.

**“TTL will clean every dead-letter store.”** Product behavior differs; Azure Service Bus does not observe TTL within its DLQ and has no automatic cleanup.

**“The main job's green status proves complete output.”** Accepted records can coexist with unowned quarantine, exclusions, or missing dispositions. Reconcile $U=A\uplus Q\uplus X\uplus P$.

**“Quarantine replaces producer accountability.”** Containment protects consumers, but reason/source evidence should drive upstream contract correction and prevention.

## Worked Examples

### Example 1

A file manifest declares 1,000 rows and a control total. One row has invalid UTF-8. The business contract requires the entire file total and ordered ledger. The pipeline stores the immutable file and parse evidence, quarantines the whole manifest generation, publishes no trusted rows, and asks the producer for correction. Record-level continuation would create a false complete ledger.

### Example 2

An optional telemetry stream has independent events and permits up to 0.01% `DOMAIN.OUT_OF_RANGE` quarantine with explicit degraded metadata. One malformed event receives a durable envelope and source acknowledgement only after raw/quarantine commit. Accepted events continue. The daily manifest lists accepted and quarantined identities; exceeding budget blocks publication and alerts the producer owner.

### Example 3

A schema registry outage causes 70% of records across schemas to raise `DEPENDENCY.SCHEMA_LOOKUP_TIMEOUT`. The circuit classifier pauses affected partitions and retries registry health with backoff. It does not create millions of `SCHEMA.UNKNOWN` quarantine records. Authoritative raw retention and source lag are monitored until consumers resume.

### Example 4

A Pub/Sub subscription configures a dead-letter topic. Operators assume exactly five attempts, but the product documents approximate best-effort forwarding. The pipeline records its own processing attempts and never uses provider count as exact business evidence. It consumes the dead-letter subscription into governed quarantine, preserving the wrapped original/source-subscription metadata and checking IAM/routing with synthetic tests.

### Example 5

An ordered account stream fails at version 12; versions 13 and 14 decode but depend on state 12. The consumer parks that account key and retains later events behind the gap while other independent keys proceed. After correcting version 12, it replays 12–14 in version order and reconciles the account snapshot before releasing the key.

### Example 6

A database target times out while accepting event `e9`. Treating timeout as failure and sending `e9` to quarantine could create accepted-and-quarantined overlap. The consumer queries the idempotent target receipt. If success exists, current disposition is accepted and the timeout remains attempt history. If absent, it retries the atomic transaction or contains the event before acknowledging source.

### Example 7

A malformed CSV field contains a spreadsheet formula and an access token. Raw bytes are stored encrypted in a restricted tenant zone. The envelope exposes digest, length, column, stable parse code, and a sanitized bounded preview; alerts and tickets exclude the token/formula. Only approved responders can retrieve raw, and the replay tool never launches a spreadsheet or shell.

### Example 8

After deploying parser version 4, operators select 20,000 `PARSE.QUOTING_V3` records by immutable quarantine-ID manifest. A 100-record canary validates schema, identities, totals, and target receipts. The redrive preserves occurrence IDs, rate-limits behind live traffic, records version 4 outcomes, and transitions successful current dispositions to accepted while retaining original version-3 failures.

### Example 9

An Azure Service Bus DLQ grows for months because normal queue TTL assumptions were applied to it. Monitoring of record/byte age catches the mismatch before quota pressure. The team adds an owned drain into governed quarantine, explicit lifecycle resolution, safe replay manifests, and alarms. It does not enable blind deletion of unresolved messages.

### Example 10

A new deployment starts throwing an unrecognized null dereference for 2% of records. Instead of classifying those records as bad, unknown-exception policy trips a circuit on the deployment/source scope, rolls back, and preserves the affected raw range. Reprocessing under the prior version succeeds; the incident links the code defect to attempts without blaming producer data.

## Cross-Program Connections

**Distributed Systems.** At-least-once delivery, ambiguous commits, acknowledgements, leases, backoff, jitter, circuit breakers, ordering, and dual writes determine safe containment and replay.

**API and Service Engineering.** Stable problem types, retryability, idempotency keys, rate-limit hints, request receipts, and error redaction parallel pipeline error contracts.

**Platform Engineering.** Queue/topic provisioning, IAM, encryption, quotas, dashboards, alert routing, runbooks, and self-service replay tooling make quarantine operable rather than a graveyard.

**Reliability Engineering.** Error budgets, backlog age, retry storms, circuit behavior, capacity exhaustion, incident severity, and recovery objectives connect data quality to service health.

**Security Engineering.** Hostile parsing, injection, secrets/PII, tenant isolation, malware, access logs, retention, key management, and replay authorization shape containment architecture.

**Database Engineering.** Transactions, unique constraints, outbox tables, savepoints, isolation, and receipts implement atomic accepted/quarantine current state.

**Data Architecture and Governance.** Ownership, contract policy, degraded completeness, lineage, stewardship, retention, exclusion, legal hold, and producer correction define semantic resolution.

**Systems Engineering.** Failure classification, hazard containment, state transitions, conservation, feedback, capacity, and degraded-mode criteria prevent local error handling from causing systemic risk.

## References

1. Amazon Web Services, [Using Dead-Letter Queues in Amazon SQS](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-dead-letter-queues.html). Documents redrive policies, `maxReceiveCount`, retention considerations, access policies, and FIFO ordering cautions.
2. Google Cloud, [Dead-Letter Topics](https://cloud.google.com/pubsub/docs/dead-letter-topics). Documents Pub/Sub forwarding/wrapping, required roles, and approximate best-effort maximum delivery attempts.
3. Microsoft, [Overview of Service Bus Dead-Letter Queues](https://learn.microsoft.com/en-us/azure/service-bus-messaging/service-bus-dead-letter-queues). Documents DLQ addressing, reasons, delivery counts, TTL behavior, explicit completion, and lack of automatic cleanup.
4. Confluent, [View Connector Dead Letter Queue Errors in Confluent Cloud](https://docs.confluent.io/cloud/current/connectors/dead-letter-queue.html). Documents sink-connector DLQ topics, continued processing for serialization/deserialization errors, headers, and operational inspection.
5. IETF, [RFC 9457: Problem Details for HTTP APIs](https://www.rfc-editor.org/rfc/rfc9457.html). Defines machine-readable problem types, standard members, extension members, and security considerations for HTTP error details.
6. Apache Beam, [Python SDK Core Transforms: `with_exception_handling`](https://beam.apache.org/releases/pydoc/current/apache_beam.transforms.core.html#apache_beam.transforms.core.Map.with_exception_handling). Documents good/dead-letter outputs and configurable exception, threshold, timeout, callback, and error-handler behavior.
7. OWASP Foundation, [Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html). Provides guidance on event attributes, sanitization, sensitive values, injection, access, monitoring, and retention for diagnostic records.
8. National Institute of Standards and Technology, [SP 800-92: Guide to Computer Security Log Management](https://csrc.nist.gov/pubs/sp/800/92/final). Provides lifecycle guidance for generating, transmitting, storing, accessing, analyzing, and disposing of security log data.

## Exercises

### Exercise 1

A 500-record file contains two malformed optional telemetry rows, but its manifest also declares a total that must equal the sum of all records for billing. Design the correct containment unit, current dispositions, trusted publication decision, envelope evidence, and producer feedback. Explain why “498 accepted, 2 quarantined” is or is not a complete bill.

### Exercise 2

Classify each failure and choose retry/quarantine/circuit/security behavior: (a) one invalid UTF-8 record; (b) schema service timeout across 90% of records; (c) target commit acknowledgement timeout; (d) unknown null dereference after a deployment; (e) cross-tenant identifier with an embedded access token. State what evidence would change each classification.

### Exercise 3

At boundary $b$, the expected manifest has 10,000 unique IDs. Accepted has 9,940 IDs, quarantine 45, exclusion 10, and pending 10. Five IDs occur in both accepted and quarantine; five expected IDs occur in none of the four sets. Determine why count totals alone mislead, compute the number of distinct accounted IDs if all other sets are disjoint, and state the conditions for completion.

### Exercise 4

A containment store has 900 GB usable free capacity. Quarantine arrives at 75 GB/hour and is resolved at 15 GB/hour. Estimate time to exhaustion under constant rates. Design alert/circuit thresholds and explain why the calculation is not a guarantee. Then address what changes if the error is a systemic schema outage rather than record defects.

### Exercise 5

Design a redrive for 50,000 quarantined records spanning three error codes, two schema versions, and an ordered source. Include immutable selection, canarying, corrected version identity, rate/order controls, idempotence, current-state transitions, retained history, reconciliation, rollback, security approval, and producer/downstream communication.

## Answers to the Exercises

### Answer 1

The billing total makes the file/generation the semantic atomic unit even if telemetry rows appear individually optional. Preserve the immutable file/object version, manifest, checksum, row positions, parse failure bytes or restricted raw pointers, schema/parser versions, total, source identity, and reason codes. Current disposition for the generation is quarantined/failed, with no trusted billing publication; row-level diagnostic child states may show 498 parsable and two invalid but cannot promote the parent. Notify the producer with safe evidence and request a corrected new object/version linked to the original. “498 accepted, 2 quarantined” is not a complete bill because the declared total cannot be validated and the accepted subset may understate amount; publishing it as complete violates the contract. A separate explicitly provisional non-billing diagnostic output could exist if consumers and policy support it.

### Answer 2

(a) Invalid UTF-8 is a deterministic record-content quarantine if records are independent; if it prevents whole-file controls or transaction parsing, contain the parent unit. Evidence that upstream bytes changed or a parser bug exists changes the path. (b) Ninety-percent schema-service timeout is a transient systemic dependency failure: trip a circuit/pause, preserve raw/source retention, and probe recovery rather than flood quarantine. Evidence that schema IDs are permanently unknown for one producer could reclassify that cohort. (c) Commit acknowledgement timeout is ambiguous outcome: query target receipt/transaction evidence; matching success means accepted, absence permits idempotent retry, unresolved state blocks acknowledgement. (d) Unknown null dereference after deployment is a programmer/systemic stop/rollback until reproduction proves narrow record specificity. (e) Cross-tenant ID plus token is security/privacy containment with restricted raw, sanitized alerts, incident ownership, and no ordinary automated redrive. Verified safe tenant mapping and credential revocation may enable governed remediation but do not erase the incident.

### Answer 3

The naive counts sum to $9,940+45+10+10=10,005$, yet five IDs overlap accepted and quarantine. If all other sets are disjoint, their union contains $10,005-5=10,000$ distinct IDs. The statement that five expected IDs occur in none means five of those 10,000 distinct disposition IDs must be unexpected/outside the manifest (or another premise is inconsistent); exact set comparison reveals this while totals do not. Completion requires every and only expected ID to be in exactly one current set, no overlap, $P_b=\varnothing$, governed exclusions, and quarantine satisfying the declared semantic budget. Here overlap, missing expected IDs, unexpected IDs, and ten pending units all block completion regardless of total equality.

### Answer 4

Net growth is $75-15=60$ GB/hour, so the constant-rate estimate is $900/60=15$ hours. Alerts should fire on first severe/new reason, acceleration, oldest-age/service-level breach, and staged capacity projections—for example operational investigation well above 12 hours remaining, automatic source-scope circuit at a tested safer reserve, and incident escalation before storage/queue quotas threaten evidence. Exact numbers depend on recovery time, burst tolerance, reserved capacity, and business criticality. The estimate ignores burstiness, compression/object overhead, quota partitions, resolution slowdown, retries, and rate measurement error, so it is not a guarantee. If a schema outage causes the rate, circuit/pause the affected source immediately and preserve authoritative raw/source retention; do not spend 15 hours converting healthy records into individual quarantines.

### Answer 5

First group and diagnose by stable error code/version, schema, producer, source range, order domain, and security class; do not mix unresolved security holds or unrelated defects. After deploying versioned corrections, snapshot an immutable manifest of the exact quarantine IDs, payload digests, original pointers, predecessor/successor dependencies, and intended corrected processor/schema/reference versions. Obtain required data/security/producer approvals. Run representative canaries for each cohort and boundary case, comparing proposed identities, schemas, counts, controls, target receipts, and downstream effects. Preserve original logical occurrence IDs; use idempotent effect receipts and treat ambiguous prior effects explicitly. For ordered keys/partitions, replay from required predecessor through successors in source order or rebuild a complete state range. Rate-limit behind live traffic and monitor dependencies/capacity. Each attempt appends history; success atomically changes current disposition to accepted while marking the original quarantine resolved, never deleting it at replay start. Reconcile all 50,000 selection IDs into accepted, still quarantined, excluded, or pending; validate no duplicate target effects, exact ranges/order, batch controls, and downstream restatements. Roll back unpublished generations or use compensating/rebuild procedures for published effects. Communicate residual cases, recurrence, corrected producer contract, and downstream version/publish status before closing.
