---
module_id: API-068
program: API & Service Engineering
level: 2
module_number: 68
title: Dead-Letter Handling
status: complete
last_verified: 2026-09-02
---

# Dead-Letter Handling

## One-Page Review

### Governing question

When normal delivery can no longer make safe progress, how should a system preserve the original message and evidence, classify ownership, bound harm, repair the cause, and redrive or terminate work without losing identity, order, or accountability?

### Essential definitions

- A **dead letter** is a message removed from its normal delivery path because a configured delivery, expiry, routing, capacity, or application condition was reached.
- A **dead-letter queue/topic/subqueue/exchange path (DLQ)** is a provider or application mechanism that stores or routes such messages; it is not itself remediation.
- A **poison message** repeatedly causes deterministic failure for a consumer or version.
- A **retryable failure** has a reasonable prospect of succeeding without changing message or system semantics; a **terminal failure** does not under current policy.
- A **quarantine** isolates suspect or unsafe input for controlled analysis; a **parking/hold queue** delays known recoverable work until a dependency or policy condition changes.
- A **failure envelope** preserves the original logical identity and immutable payload reference/fingerprint plus failure, attempt, source, consumer, and routing evidence.
- **Redrive** is an authorized operation that reintroduces dead-lettered work to a named processing path under explicit gates and rate limits.
- A **tombstone/disposition record** is durable evidence that a dead letter was resolved, superseded, expired, rejected, compensated, or intentionally discarded.

### Central model, mechanism, or theorem

For original logical message $m$, delivery attempts $a_i$, failure class $k$, and disposition $d$, the lifecycle is

$$
normal\rightarrow retry/hold\rightarrow dead\ letter\rightarrow triage\rightarrow repair\rightarrow redrive\mid terminal\ disposition.
$$

Every transition preserves $m$, fingerprint, source lineage, and audit. If dead-letter arrival rate is $\lambda_d$ and sustainable resolution/redrive rate is $\mu_d$, backlog grows at approximately $\max(0,\lambda_d-\mu_d)$. A DLQ without ownership, retention, capacity, alerting, and resolution SLO is delayed data loss.

### Critical invariants

Dead-lettering never rewrites one failed logical message into an unrelated new fact. Original ID, tenant, schema/type/version, ordering key/version, source destination/subscription, first/last failure times, attempt evidence, safe error taxonomy, and payload fingerprint remain traceable even if a provider wraps the message or assigns a new transport ID. Same message cannot loop silently between source, retry, and DLQ.

Classification separates transient dependency/capacity faults, invalid/schema/auth/policy faults, expired commands, domain rejections, consumer defects, and uncertain effects. Retry and redrive preserve idempotency/effect IDs and respect order, deadlines, current authorization, schema compatibility, dedup retention, and downstream capacity. Operators use least privilege, four-eyes/approval where risk requires it, immutable audit, canary/rate-limited redrive, reconciliation, and explicit terminal disposition.

### Common failures

Treating a DLQ as success; one shared queue with no source provenance; retrying malformed or unauthorized messages; sending transient outages directly to permanent quarantine; fixed attempt counts without time/backoff/failure class; assuming provider counts are exact; losing payload or application ID during wrapping/redrive; logging secrets in error strings; acknowledging source before durable dead-letter capture; dead-letter publishing failure; deleting after inspection; redriving everything at full speed; changing IDs to bypass deduplication; redrive loops; order overtaking; expired commands executed later; old consumer/schema bug repeated; insufficient retention; unbounded backlog; and no owner or terminal evidence.

### Compact example

A shipment command fails because consumer release 7 rejects a newly optional field incorrectly. After bounded retries, its failure envelope preserves command ID, order version, source offset, fingerprint, release, and validation code. Operators deploy release 8, canary-redrive ten oldest compatible commands at 2/s using the same IDs, verify idempotent shipment state and order continuity, then ramp. Expired commands receive terminal dispositions rather than shipment. **Conclusion:** the DLQ supported evidence and recovery; it did not decide correctness.

### Connections

[Delivery and Acknowledgment](066-delivery-and-acknowledgment.md) defines retry/ack boundaries; [Idempotent Consumers](067-idempotent-consumers.md) makes redrive safe. [Event Schema Design](062-event-schema-design.md) and [Ordering and Partition Keys](065-ordering-and-partition-keys.md) govern compatibility and holes. The next modules address event versioning and full replay/evolution design.

## Governing Question

Which failures should retry, pause, quarantine, dead-letter, expire, compensate, or terminate—and what durable evidence and controlled workflow guarantee that every removed message is either safely restored or explicitly accounted for?

## Why This Matters

Normal delivery cannot retry forever. One malformed record can monopolize a partition, a dependency outage can create an explosive retry loop, a stale command can become dangerous, and a consumer defect can reject an entire schema version. Dead-letter mechanisms let healthy traffic continue and preserve failed work for diagnosis. They also move correctness responsibility away from the normal consumer into an often neglected operational path.

Products use the same words for different mechanisms. Amazon SQS associates a source queue with another queue and supports redrive tasks. Google Pub/Sub configures a dead-letter topic on a subscription and documents best-effort/approximate maximum attempts. RabbitMQ republishes dead-lettered messages to an exchange for rejection, expiry, length, or delivery-limit reasons and documents routing/cycle/safety behavior. Azure Service Bus exposes a secondary subqueue with its own lifetime and settlement behavior. Apache Pulsar distinguishes retry-letter and dead-letter topics under specific client/subscription semantics.

These are transport facts, not business resolution. Moving a message can change enqueue time, provider message ID, routing headers, order relative to live traffic, or retention clock. The source-to-DLQ move may itself fail under some configurations. An application command may no longer be authorized or relevant when replayed. A repaired consumer may produce an external effect that the original attempt already completed.

Dead-letter design is therefore an incident, data-governance, and recovery system. It needs taxonomy, lineage, capacity, security, ownership, observability, remediation tooling, redrive controls, and closure evidence. “Messages are in the DLQ” is an unresolved production state.

## Prerequisites and Retrieval

Retrieve [Event Schema Design](062-event-schema-design.md), [Ordering and Partition Keys](065-ordering-and-partition-keys.md), [Delivery and Acknowledgment](066-delivery-and-acknowledgment.md), and [Idempotent Consumers](067-idempotent-consumers.md). Be able to identify message identity, attempts, acknowledgement boundary, deduplication horizon, subject version, deadline, and every local/external effect.

Retrieve the chosen provider's exact dead-letter triggers, attempt-count semantics, ack/nack/expiry interactions, forwarding/wrapping, routing headers, identity changes, retention clocks, encryption/IAM, delivery guarantees for the dead-letter move, ordering, redrive destination/rate/filtering, task cancellation, metrics, and regional behavior. Retrieve application schema registry, artifact/release provenance, replay authorization, and data-retention policy.

## Learning Objectives

After completing this module, you can:

1. distinguish retry, delayed retry, parking, quarantine, dead-letter, and terminal disposition;
2. classify failures by semantics, ownership, retryability, deadline, and uncertainty;
3. design a failure envelope that preserves identity, lineage, ordering, and safe diagnostics;
4. evaluate provider-specific dead-letter triggers, counts, forwarding, retention, and safety;
5. prevent source-to-DLQ loss and retry/dead-letter cycles;
6. operate DLQ capacity, age, retention, access, alerting, and resolution SLOs;
7. diagnose and repair consumer, producer, schema, dependency, and policy faults;
8. redrive with idempotency, ordering, canaries, rate control, gates, and rollback;
9. close messages with auditable success, rejection, expiry, supersession, or compensation; and
10. verify the full failure-to-resolution lifecycle under faults and adversarial input.

## Core Exposition

### Treat dead lettering as a lifecycle

Draw states from original publication to final closure. A message can be pending, delivered, retry scheduled, held for dependency, quarantined for unsafe input, dead-lettered after a policy boundary, under investigation, eligible for redrive, redriving, resolved successfully, terminally rejected/expired/superseded, or awaiting compensation/manual action.

Assign an owner and SLO to every nonterminal state. The broker team may own transport forwarding, but the producing/consuming domain owns meaning and disposition. Security owns suspected malicious content; data governance owns privacy/retention constraints; incident command may own mass-failure recovery. A RACI without an on-call route and executable runbook is not operational ownership.

Dead-letter receipt should create a durable case/index record keyed by consumer scope and original logical message ID. This record points to protected payload storage/provider coordinates, tracks investigation and dispositions, and survives provider retention or message movement. It must not become a second unaudited source of mutable truth.

Define closure: a message is not resolved merely because it left the DLQ. Closure requires verified successful processing/reconciliation or an authorized terminal disposition with reason, actor, evidence, and downstream obligations.

### Classify failures before choosing a path

Use stable machine-readable classes, not raw exception strings:

- transient infrastructure/dependency/capacity fault: delayed retry with jitter/circuit breaking;
- throttling/rate limit: provider-directed delay and bounded concurrency;
- malformed envelope or schema incompatibility: quarantine/dead letter for producer/consumer repair;
- authentication/integrity failure: security quarantine, no blind retry;
- authorization/policy failure: terminal or policy hold pending deliberate reauthorization;
- expired/stale command: terminal expiry/supersession, not late execution;
- domain rejection/conflict: terminal business outcome or workflow replan;
- deterministic consumer defect: isolate affected release/type and repair code;
- resource-specific dependency state: keyed hold until prerequisite event/state, with deadline;
- uncertain external effect: reconciliation state, not ordinary retry;
- unknown: short bounded diagnostic retries, then quarantine/escalation.

Separate who can fix it. Producer defects require contract correction and perhaps republish with a new legitimate fact/version; consumer defects require deployment; transient outages require recovery; bad reference data may need controlled repair; malicious messages require evidence preservation. Redriving before the owning condition changes only recreates failure and load.

Attempt count alone is a weak classifier. Three failures over milliseconds during an outage differ from three failures over days with changing dependencies. Include elapsed age, last-progress evidence, error class, deadline, dependency health, and cost/risk. Provider maximum attempts may be approximate or reset under documented conditions; maintain application evidence when exact business policy matters.

### Separate retry, hold, quarantine, and dead letter

Immediate/local retry handles brief races and transient calls within bounded processing deadline. Delayed retry handles recoverable faults with backoff without monopolizing workers. A parking/hold path represents known waiting conditions such as unavailable customer master data or paused tenant; it has a wake condition and deadline.

Quarantine isolates messages that are unsafe, suspect, incompatible, or require forensic access. Its consumers and tools should not execute business effects. A DLQ commonly represents exhaustion of a normal delivery policy, but provider mechanisms can also route expiry or capacity overflow; do not assume every member is poison.

Some domain rejections should produce a normal typed outcome event and acknowledgement, not a DLQ. “Insufficient funds” is a business result. Invalid signature, unknown schema, invariant violation, or repeated handler crash needs operational handling. Using a DLQ for ordinary negative business outcomes hides expected state and burdens operators.

Keep each path's allowed transitions, retention, alerting, access, and destination explicit. Avoid a single catch-all queue whose members require incompatible remediation or disclosure permissions.

### Preserve an immutable failure envelope

Carry or index:

1. original application message ID and immutable fingerprint;
2. tenant/security scope, message type, schema/spec version, subject/key/version, causation/correlation;
3. source broker, namespace/topic/queue/subscription/group, partition/offset or receipt coordinates;
4. original publish/occurred/deadline/expiry times and first/last delivery/failure times;
5. delivery attempts when trustworthy plus application attempt history summary;
6. consumer name/semantic version, artifact digest/release, configuration/feature flags, region;
7. normalized failure class/code, safe bounded diagnostics, dependency/provider request IDs;
8. current idempotency/inbox/effect state and uncertain-outcome marker;
9. dead-letter trigger/path/routing history and payload storage reference; and
10. disposition/redrive case ID, approvals, actor, timestamps, destination, and verification.

Preserve original bytes or an immutable governed representation when legal and useful. Provider wrapping or header mutation must not obscure original application envelope. If payload is too large/sensitive, use encrypted object reference plus digest and retention coupling; ensure the object does not expire before the case.

Do not copy stack traces, credentials, tokens, personal data, or whole payloads into broadly readable headers, metrics, or tickets. Normalize error codes at capture time; store restricted forensic detail separately. Bound every field to prevent a malicious message from amplifying storage.

### Understand provider triggers and semantics

Map exact mechanism per destination/subscription. SQS uses receive counts/redrive policy and requires compatible queue type; retention-clock behavior differs for standard and FIFO movement. Its managed redrive can reset transport identity/enqueue time and interleave with live messages. Preserve application ID/order version independently.

Google Pub/Sub forwards an undeliverable message by wrapping it and adding source-subscription attributes. Its configured maximum delivery attempts is documented as approximate/best effort and depends on correct IAM. Treat it as load-shaping, not an exact business counter.

RabbitMQ can dead-letter on reject without requeue, expiry, queue-length overflow, or quorum delivery limit. Routing can use original or configured keys, cycles are possible/detected under documented conditions, and dead-letter republishing safety depends on queue/configuration. Monitor the forwarding path itself.

Azure Service Bus provides a DLQ subqueue and supports application-level reason/description; its DLQ does not automatically clean up and messages require explicit settlement. Oversized exception descriptions can collide with message-size limits, reinforcing bounded error metadata.

Pulsar client/subscription types and versions govern retry/dead-letter features and topic naming. Retry-letter and dead-letter intents differ. Across all providers, pin current documentation and test the selected mode rather than build one generic abstraction from names.

### Make the move durable and observable

A source consumer that manually publishes to a DLQ then acknowledges source has a dual-write window. If it acknowledges first, failure can be lost; if it publishes first and ack is lost, duplicate dead letters can occur. Use provider atomic dead-lettering where specified, transactional broker support where applicable, or an application-owned durable failure record/outbox with idempotent case identity.

Provider-managed dead lettering may also fail due to destination absence, permissions, encryption keys, quota, routing, or unavailable quorum. Alert on forwarding errors and compare source terminal attempts with DLQ receipts/case records. “Configured” is not evidence that capture works.

Use stable case key `(consumer_scope, original_message_id, failure_epoch/class)` and fingerprint. Multiple dead-letter events for the same logical message may update attempt history rather than create unrelated cases. Do not suppress a genuinely different failure after a repair; version/epoch the occurrence while retaining lineage.

Test permissions before incidents, including service principals performing forwarding and human/automation roles performing peek, receive, redrive, delete/complete, decrypt, and destination send. Configuration-as-code should validate source/DLQ compatibility and retention.

### Protect ordering and dependencies

Removing a poison record lets later records overtake it. That may be desirable for independent keys and invalid for one subject state machine. Record the ordering key/subject version and decide whether to block only that key, buffer later versions, apply complete-state snapshots, or mark a deliberate gap.

A partition-wide retry can stall unrelated subjects; a retry topic can reorder. Keyed lanes and durable per-subject gap state preserve local order while other keys progress. Redrive must reintegrate the missing version before dependent later effects when transitions are noncommutative.

Do not assume FIFO DLQ/redrive restores original order; live messages, provider movement, retries, and new transport IDs can interleave. Domain versions and idempotent consumers remain authoritative. For a superseded complete-state event, terminal disposition may be safer than applying an old state.

Cross-message prerequisites require explicit correlation/workflow state. Dead lettering one command should not leave a saga waiting forever; publish or record a failure outcome/incident transition where the workflow contract needs it.

### Operate backlog, capacity, and retention

Measure incoming dead-letter rate $\lambda_d$, resolution/redrive throughput $\mu_d$, backlog count/bytes, oldest age, percentile age, failure class/type/consumer/tenant/release distribution, and re-dead-letter rate. If $\lambda_d>\mu_d$, backlog grows; even if average rates balance, burst headroom and investigator capacity matter.

Little's Law gives a planning relationship $L_d\approx\lambda_d W_d$ in stable flow, where $L_d$ is average unresolved cases and $W_d$ mean resolution time. It is not a promise under bursty incidents. Set alert/SLOs by risk: any payment-integrity quarantine may page immediately, while replaceable analytics might use batch triage.

Retention must cover detection, incident response, repair, validation, approval, controlled redrive, audit, and worst outage. Coordinate broker DLQ retention with external payload object, schema/artifact, logs/traces, encryption keys, dedup/effect ledgers, and source data. Provider clocks can differ between source and DLQ; verify exact mode.

Provision count and bytes for mass schema/release failure. Apply source admission/circuit breakers before DLQ becomes the emergency overflow. A DLQ is not an infinite buffer. When retention approaches, escalate and export to a governed archive/case store or take explicit terminal action—never silently expire high-value work.

### Diagnose and repair systematically

Cluster by normalized class, consumer release, schema/type, producer, tenant, source partition/key, first-failure time, dependency, and fingerprint signature. A sharp release-correlated onset suggests regression; one producer/schema suggests contract drift; all messages suggest dependency/configuration; one key suggests data invariant/hot entity; random timeouts suggest capacity/network.

Reproduce with protected payload fixtures in an isolated environment and the recorded artifact/config/schema. Avoid executing external effects; replace providers with outcome-aware test doubles. Determine whether any original attempt committed local or external state by querying inbox/effect ledger and authoritative systems.

Repair the cause before the message. Deploy compatible consumer, restore dependency, correct schema registry/policy, repair reference data, or provide a governed transformation. Never edit original evidence in place. If transformation changes semantic content, create a new signed/authorized message with new identity and explicit `supersedes` lineage; if it only restores representation without changing intent, record transformation version and preserve original identity according to contract.

Test the repair against representative cases, edge schemas, duplicates, order gaps, expired commands, uncertain effects, and current production traffic. Link change/release evidence to the redrive case.

### Redrive as a controlled production change

Eligibility gates should confirm:

- root cause has changed and repair is deployed/healthy;
- message identity/fingerprint/evidence is intact;
- schema and consumer version can interpret it;
- deadline/relevance/current authorization permit execution;
- idempotency/effect ledgers still cover the original horizon;
- prior uncertain effects are reconciled;
- subject ordering/gaps and downstream prerequisites are safe;
- destination capacity, quotas, budgets, and incident conditions allow load; and
- rollback/stop criteria, approver, and observer are assigned.

Redrive a canary selected by representative failure classes/ages/tenants without cherry-picking only easy messages. Start below downstream spare capacity, apply per-tenant/key bulkheads and jitter, then ramp based on success latency, new DLQ rate, effect invariants, and live SLOs. Provider redrive may not filter/transform; build a controlled application workflow when selection or transformation is required.

Preserve original application ID, effect ID, subject key/version, causation, occurred time, and first-failure evidence. Add a redrive attempt/case ID as metadata; do not replace logical identity with the provider's new message ID. Revalidate current policy and schema without silently changing the historical fact.

Pause automatically on repeated same-class failure, conflict, ordering gap, provider uncertainty, downstream saturation, security signal, or invariant drift. Redriven messages that fail again return to a bounded occurrence/case path, not an infinite source↔DLQ loop.

### Record terminal dispositions

Not every dead letter should be redriven. Valid terminal dispositions include processed and reconciled, duplicate already effected, expired, superseded, business rejected, unauthorized, malicious/corrupt, compensated, manually completed, source-corrected by a new fact, or irrecoverable under approved loss policy.

Each disposition records original/case ID, class, decision code, actor/service, approval, time, evidence, impact, compensation/new-message linkage, and retention policy. Deleting/completing provider message happens only after the durable disposition commits. High-risk bulk disposition requires query snapshot, counts/digests, dry run, two-person approval, and post-action reconciliation.

Do not call “discard” a solution. State accepted impact and notify affected workflow/customer/regulator when required. Metrics should distinguish resolved by processing from resolved by rejection/expiry/compensation.

### Secure the dead-letter plane

DLQs concentrate malformed input, personal data, credentials accidentally embedded by producers, and detailed error context. Apply encryption, least-privilege destination/source/redrive IAM, network controls, tenant isolation, audited break-glass access, key rotation, retention/deletion, and export controls.

Separate inspect from execute. Analysts may view safe metadata without payload; payload access is just-in-time and logged; only a redrive service can send to allowed destinations under policy. Prevent arbitrary destination selection, message editing, and bypass of schema/auth/deadline checks.

Treat messages as hostile data. Inspection UIs escape content, do not fetch attacker-controlled URLs, cap decompression/parsing, disable active rendering, and redact secrets. Failure strings are untrusted. Redrive authorization cannot be conveyed solely inside the message being redriven.

### Observe and verify end to end

Dashboards connect source attempts, retry/hold, dead-letter forwarding, case creation, oldest age, retention headroom, diagnosis, redrive, repeat failure, final effect, checkpoint, and disposition. Correlate by protected original ID/case while avoiding raw high-cardinality sensitive labels.

Synthetic probes regularly force a safe known failure and verify source removal, DLQ arrival, envelope fields, encryption/access, alert, case creation, test redrive/disposition, and audit. Fault injection covers missing destination, denied IAM/KMS, full quota, broker failover, wrapper change, retention expiry, duplicate forwarding, partial redrive cancellation, and region loss.

Property/integration tests assert logical ID/fingerprint/order version preservation, bounded attempts, no loops, idempotent redrive, same-ID conflict handling, deadline/auth revalidation, and one terminal disposition. Disaster tests restore source and DLQ/case/inbox/effect/outbox consistently and reconcile counts/digests—not provider metrics alone.

## Definitions and Notation

Let logical message $m$ have attempts $a_i$, immutable fingerprint $f(m)$, consumer scope $c$, subject version $v$, deadline $D$, and external effect IDs $e_k(m)$. Let failure class $k$ belong to retryable, hold, quarantine, terminal, or uncertain families. Let case $Q(c,m,r)$ identify a dead-letter occurrence/epoch $r$ while preserving $m$.

Let dead-letter arrival rate be $\lambda_d$, sustainable resolved-case rate $\mu_d$, unresolved backlog $L_d$, mean time to resolution $W_d$, average stored bytes $b_d$, and retention $T_d$. Stable flow requires $\lambda_d<\mu_d$ with burst/failure headroom; $L_d\approx\lambda_dW_d$ under Little's Law assumptions; retained bytes are first-order $\lambda_db_dT_d$ absent resolution/compaction details.

Disposition $d(m)$ is one of verified processed, duplicate, rejected, expired, superseded, compensated, malicious/corrupt, irrecoverable-approved, or another governed domain state. Provider deletion/settlement follows durable $d(m)$.

## Mechanisms, Invariants, or Proof Structure

1. Enumerate failure classes, semantic deadlines, effect uncertainty, and owning teams.
2. Map each class to bounded retry, hold, quarantine, DLQ, or normal terminal outcome.
3. Preserve original ID/fingerprint/payload reference, source, order, consumer release, attempts, and safe diagnostics.
4. Verify dead-letter movement durability, permissions, routing, retention, and provider-specific approximations.
5. Create one durable case/disposition state machine and protect it from duplicate forwarding.
6. Monitor rate, backlog, age, retention headroom, source-to-DLQ parity, and repeat failure.
7. Diagnose clusters, reproduce safely, reconcile prior effects, and repair root cause.
8. Gate canary/rate-limited redrive by compatibility, authorization, deadline, idempotency, order, and capacity.
9. Preserve logical/effect identity and stop loops or invariant drift automatically.
10. Settle/delete only after verified processing or durable authorized terminal disposition.

Proof sketch: if source removal is atomic with provider dead-letter capture—or an idempotent durable application case bridges the dual write—then each exhausted logical message has at least one recoverable case. Unique case identity/fingerprint collapses duplicate forwarding. If settlement follows a durable verified disposition, no case disappears without accounting. This proves accountable capture only within retention and failure assumptions; safe business recovery additionally requires compatible repair, idempotent effects, ordering/deadline/authorization checks, and redrive verification.

## Alternatives and Trade-Offs

**Long retry versus early DLQ.** Long retry absorbs transient faults but consumes capacity/delays following work. Early DLQ isolates quickly but can turn brief outages into operator load. Class/age/cost-based policy is stronger than one count.

**Provider DLQ versus application case store.** Provider mechanism integrates routing and delivery. Application case store gives normalized cross-provider state, exact ownership/disposition, and longer governance. Often use both with parity, not two unrelated truths.

**Shared versus per-source/class DLQ.** Shared simplifies infrastructure but mixes schemas, permissions, retention, and owners. Per-domain/source/class improves isolation at operational-resource cost. Preserve provenance either way.

**Retry topic versus parking store.** Retry topic preserves broker workflow and delayed delivery but can reorder and loop. Parking store exposes conditions/workflow state but requires scheduler and ownership.

**Edit-and-redrive versus immutable correction.** In-place edit is convenient but destroys evidence/identity meaning. Immutable original plus governed transformation/new superseding fact supports audit and reproducibility.

**Automatic versus approved redrive.** Automation shortens recovery for low-risk known faults. Approval/canary protects high-impact commands and mass changes. Encode tiers by effect/risk, not operator convenience.

**Block key versus let later versions pass.** Blocking preserves noncommutative order but raises key latency. Passing improves availability but needs complete-state semantics, gap tracking, or later reconciliation.

**Delete after resolution versus durable tombstone.** Delete minimizes storage; tombstone prevents ambiguity/repeated handling and supports audit. Keep compact disposition under governed retention even if payload is removed earlier.

## Failure Modes and Misconceptions

1. “It is in the DLQ, so it is handled.”
2. Attempt count is treated as exact across providers and all failure types.
3. Business rejection is dead-lettered instead of represented as normal outcome.
4. Transient outage floods permanent quarantine; malformed input retries forever.
5. Provider wrapper/new message ID replaces original application identity.
6. Source is acknowledged before durable dead-letter/case capture.
7. Dead-letter destination, IAM, KMS, routing, quota, or quorum failure is unmonitored.
8. Raw payload/exception secrets leak through headers, metrics, tickets, or UI.
9. One shared DLQ has no tenant/source/schema/owner provenance.
10. Poison removal silently violates per-key order or strands a workflow.
11. DLQ retention/object/key expires before detection and repair.
12. Operator viewing/receiving changes attempt/settlement state unexpectedly.
13. Root cause is not repaired before full-speed redrive.
14. Redrive uses new logical/effect IDs and repeats external effects.
15. Expired or unauthorized commands execute months later.
16. Redrive interleaves with live traffic and overloads the repaired dependency.
17. Failed redrive loops between retry/source/DLQ without occurrence bounds.
18. Messages are deleted after inspection without durable disposition/reconciliation.

## Worked Examples

### Example 1

A five-minute database outage produces transient dependency failures. Circuit breaker pauses consumption and delayed retry absorbs them; the system does not create 200,000 permanent cases merely because a low attempt threshold was crossed.

### Example 2

A producer emits schema version 9 while the consumer supports through 8. Messages quarantine by type/version/producer/release with original IDs. Compatibility is deployed and tested before canary redrive; the producer is corrected to prevent recurrence.

### Example 3

A command has deadline 10:30 and reaches DLQ at 10:45. It receives terminal `expired` disposition and workflow outcome; redrive does not execute a stale inventory reservation.

### Example 4

RabbitMQ routes a rejected message to a dead-letter exchange whose quorum is unavailable. Forwarding telemetry/case parity alarms; the team does not infer capture merely from the consumer's rejection call.

### Example 5

One order's version 42 fails validation while 43 arrives. The consumer records a gap and blocks only that order's transition lane. After repair, 42 redrives with its original version before 43 commits; other orders continue.

### Example 6

An SQS redrive gives moved messages new transport IDs and interleaves them with live traffic. The application envelope retains event ID/order version, so idempotent consumers and domain ordering remain correct without relying on queue message ID.

### Example 7

A payment call timed out before the command dead-lettered. Triage queries the effect ledger/provider using the original capture ID and finds success. The case closes as processed/reconciled; redrive would have risked a second charge.

### Example 8

A malicious compressed payload repeatedly exhausts parser memory. Size/decompression bounds classify it as security quarantine; analysts inspect inert protected bytes. It is never rendered or redriven into the normal parser.

### Example 9

A DLQ receives 80 messages/s while remediation sustains 50/s. Backlog grows 30/s, or 108,000/hour. Autoscaling consumers cannot fix deterministic poison; incident response stops the bad producer/release and increases safe resolution capacity.

### Example 10

After repair, operators canary 20 messages across the oldest age, three tenants, and two failure signatures at 1/s. They verify zero repeat failures, subject continuity, external-effect uniqueness, and live SLOs before staged ramp; every case records redrive and final disposition.

## Cross-Program Connections

[Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies partial failure, retries, leases, fencing, replication, and ambiguity. [Database Engineering](../../18-database-engineering/ROADMAP.md) supplies durable case state, uniqueness, transactions, retention, and recovery.

[Security Engineering](../../25-security-engineering/ROADMAP.md) contributes quarantine, forensic handling, tenant isolation, least privilege, hostile-content safety, and audit. [Software Engineering Patterns](../../11-software-engineering-patterns/ROADMAP.md) contributes circuit breaker, retry, outbox, saga, state machine, and compensating actions.

[Data Engineering](../../19-data-engineering/ROADMAP.md) uses bad-record quarantine, replay, backfill, data-quality routing, and reconciliation. [Platform Engineering](../../29-platform-engineering/ROADMAP.md) owns broker policies, IAM/KMS, dashboards, runbooks, redrive tooling, quotas, and disaster recovery. [Systems Engineering](../../26-systems-engineering/ROADMAP.md) contributes failure-mode analysis, hazard controls, lifecycle ownership, verification, and closure evidence.

## References

1. Amazon Web Services. “Using Dead-Letter Queues in Amazon SQS.” Retrieved 2026-09-02. <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-dead-letter-queues.html>
2. Amazon Web Services. “Learn How to Configure a Dead-Letter Queue Redrive in Amazon SQS.” Retrieved 2026-09-02. <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-configure-dead-letter-queue-redrive.html>
3. Amazon Web Services. “Setting Up Dead-Letter Queue Retention in Amazon SQS.” Retrieved 2026-09-02. <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/setting-up-dead-letter-queue-retention.html>
4. Google Cloud. “Dead-Letter Topics.” Retrieved 2026-09-02. <https://docs.cloud.google.com/pubsub/docs/dead-letter-topics>
5. RabbitMQ. “Dead Letter Exchanges.” Retrieved 2026-09-02. <https://www.rabbitmq.com/docs/next/dlx>
6. Microsoft. “Service Bus Dead-Letter Queues.” Retrieved 2026-09-02. <https://learn.microsoft.com/en-us/azure/service-bus-messaging/service-bus-dead-letter-queues>
7. Apache Software Foundation. “Apache Pulsar 3.3 Messaging.” Retrieved 2026-09-02. <https://pulsar.apache.org/docs/3.3.x/concepts-messaging/>

## Exercises

### Exercise 1

Classify these failures and choose retry, delayed retry, hold, quarantine, normal terminal outcome, DLQ, or reconciliation: database timeout, invalid signature, insufficient funds, unknown schema version, missing customer record expected within an hour, expired shipment command, consumer null dereference, and payment timeout after request send.

### Exercise 2

Design a provider-neutral dead-letter failure envelope and case state machine for a multi-tenant order service. Include identity, fingerprint, source/attempt/order, consumer release, error evidence, payload security, uncertain effects, ownership, redrive, disposition, and duplicate forwarding.

### Exercise 3

A DLQ receives 150 messages/s during an incident for 45 minutes, then 8 messages/s. The team can safely resolve/redrive 40 messages/s starting 15 minutes after incident onset. Ignoring normal backlog before onset, compute backlog at 15 minutes, at 45 minutes, and how long after minute 45 it takes to drain if no other limits apply.

### Exercise 4

Plan a redrive of 600,000 order-transition messages after a consumer schema defect. Include root-cause proof, representative canary, order gaps, idempotency/effects, deadlines/auth, rate/downstream capacity, live-traffic protection, stop/rollback criteria, metrics, audit, and terminal cases.

### Exercise 5

Design dead-letter handling for payments across two regions and two broker products. Include capture durability, normalized cases, provider identity/wrapping differences, effect uncertainty, failover/fencing, security, retention/restore, reconciliation, and tests without claiming exactly-once global recovery.

## Answers to the Exercises

### Answer 1

Database timeout is transient: bounded delayed retry with jitter/circuit breaker, escalating only if age/SLO or persistent evidence changes class. Invalid signature is security quarantine/terminal rejection; do not retry executable processing. Insufficient funds is a normal typed business rejection and acknowledgement, not operational DLQ.

Unknown schema version is compatibility quarantine/DLQ owned by producer/consumer teams, unless registry unavailability makes it a transient hold. Missing customer expected within one hour is keyed hold/delayed retry with prerequisite wakeup and deadline; after deadline it becomes terminal/workflow exception. Expired shipment command is terminal expired/superseded outcome.

Consumer null dereference is deterministic consumer defect: minimal bounded retries, then DLQ/quarantine by release and repair deployment. Payment timeout after send is uncertain external effect: persist/query/reconcile same effect ID; generic retry or DLQ redrive without reconciliation risks a duplicate. Every choice remains subject to actual provider/domain contract and current evidence.

### Answer 2

Use case key `(tenant, consumer-scope, original-message-id, occurrence-epoch)` with uniqueness and immutable message fingerprint. Store message type/schema, subject/order ID/version, causation/correlation, original occurred/publish/deadline, source provider/region/topic-or-queue/subscription/partition/offset or receipt coordinates, provider/application attempt summaries, first/last failure, consumer semantic version/artifact/config, normalized class/code, bounded redacted diagnostics, dependency request IDs, inbox/effect/outbox state, and provider dead-letter routing/wrapper history.

Payload stays in encrypted tenant-scoped provider storage or governed object store with digest, legal retention, and access audit. Safe metadata is separately searchable. The state machine is captured, triaged, assigned, investigating, repair-ready, redrive-approved, redriving, verified-resolved, or terminally disposed. In-progress actions have owner/epoch/deadline; transitions are audited.

Duplicate forwarding with same fingerprint appends bounded attempt/routing evidence to the same case; different fingerprint is conflict/security escalation. Redrive records case/attempt ID and preserves logical/effect IDs/order version. Terminal disposition records reason, actor/approval, evidence, compensation/superseding fact, and impact. Provider settlement/deletion occurs only after verified durable disposition. Views and actions are least-privilege, non-enumerating across tenants, and resistant to hostile payload rendering.

### Answer 3

For the first 15 minutes no resolution occurs. Backlog is $150\times15\times60=135{,}000$ messages. From minute 15 through 45, net growth is $150-40=110$ messages/s for 30 minutes, adding $110\times30\times60=198{,}000$. Backlog at minute 45 is therefore $333{,}000$.

After minute 45, arrival falls to 8/s while resolution stays 40/s, so net drain is 32/s. Drain time is $333{,}000/32=10{,}406.25$ seconds, about 173.44 minutes or 2 hours 53 minutes 26 seconds after minute 45. This ideal result excludes retries, repeat failures, ordering/key limits, downstream headroom, approvals, and live SLOs; an actual plan uses lower safe redrive capacity and monitors age/retention.

### Answer 4

First stop/roll back the defective release or incompatible producer path and prove the failure cluster is explained by schema version/release. Deploy a compatibility fix; test recorded fixtures, all affected versions, same-ID conflicts, duplicates, subject transitions, expired commands, and external-effect states. Reconcile whether any prior attempts committed before failure.

Build an immutable eligible set of 600,000 case IDs/digests grouped by tenant, subject key/version, age, failure signature, deadline, and effect state. Exclude expired/superseded/unauthorized/uncertain-effect cases into explicit dispositions or manual reconciliation. Ensure inbox/effect retention still covers original IDs. For transition streams, identify gaps and redrive per subject version; do not rely on provider FIFO or new transport IDs.

Canary a representative set across oldest/newest, schemas, tenants, regions/partitions, and signatures—perhaps tens, not only easy records—at a very low rate. Verify success/outbox/downstream state, no duplicate external effects, no repeat DLQ, ordering continuity, and live latency/error budgets. Then ramp in stages bounded below measured spare capacity, with per-tenant/key fairness and pause between stages. Reserve capacity for live traffic and coordinate databases, providers, registries, and quotas.

Automatic stops include repeat class above threshold, any same-ID fingerprint conflict, uncertain payment/shipment effect, subject gap, invariant drift, authorization failure, downstream saturation, live SLO breach, or forwarding/case parity loss. Rollback stops/cancels remaining redrive; already moved messages remain tracked/idempotent and are not erased. Audit query snapshot, approvals, artifact/config, rates, moved/succeeded/re-dead/terminal counts, actors, and disposition. Reconcile all 600,000 to exactly one governed final case state.

### Answer 5

Define one application logical payment command ID/fingerprint and stable provider effect ID independent of both brokers' message IDs, wrappers, offsets, and redrive IDs. Each consumer scope records inbox/effect state in an authoritative regional home under fencing epoch. Provider-managed DLQ is configured/tested, but an idempotent normalized case store records source provider/region/destination/subscription, coordinates, wrapper/routing history, consumer artifact, attempt/class, and protected payload reference. Source removal to case/DLQ is atomic where provider supports it or bridged by durable outbox/case parity.

Before any redrive, query payment ledger/provider by effect ID. Captured/declined results close/reconcile; uncertain remains blocked for manual/provider resolution; only proven absent eligible work retries the same effect ID. Redrive preserves command/effect/order identity and current authorization/deadline policy. It is canary/rate-limited against both broker and payment spare capacity.

One home region/epoch may execute a payment identity. Failover fences the old region and restores payment state, inbox, effect ledger, outbox, case/disposition, and encryption access to a known recovery point before consumption. Eventual case replication alone cannot prevent two charges; unavailable authority pauses execution. Broker mirrors may change offsets/IDs but not application identity.

Encrypt tenant payload/evidence, separate inspect/execute roles, require approved destination and high-risk redrive, escape hostile content, and audit decrypt/decision/action. Retention covers broker DLQs, object payloads, provider key/query horizon, dedup/effect ledger, charge reconciliation, backup restore, and incident response; restoration is parity-checked.

Test crash/partition at each capture and effect boundary, denied IAM/KMS, unavailable DLQ/quorum, duplicate/wrapped messages, provider timeout-after-success, stale region, restore mismatch, retention edge, live/redrive interleaving, and cancellation. Reconcile source facts, cases, inbox/effects, provider objects, outbox/events, and final accounting. The result is accountable, idempotent recovery within named scopes—not unqualified global exactly once.
