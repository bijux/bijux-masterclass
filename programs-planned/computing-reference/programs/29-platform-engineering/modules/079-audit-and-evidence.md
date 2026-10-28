---
module_id: PLAT-079
program: Platform Engineering
level: 2
module_number: 79
title: Audit and Evidence
status: complete
last_verified: 2026-09-02
---

# Audit and Evidence

## One-Page Review

### Governing question

How should a platform produce, protect, and retrieve evidence that lets an authorized reviewer determine what changed, who or what acted, which policy and inputs governed the action, what actually happened, and where the record is incomplete—without turning audit collection into an unbounded privacy, cost, or availability hazard?

### Essential definitions

- An **audit event** is a structured record of a security-, governance-, or operations-relevant action at a defined observation point.
- An **evidence claim** is a proposition supported by one or more records, configurations, artifacts, or observations; a record is not automatically proof of the claim inferred from it.
- **provenance** describes where a record came from, which producer and schema emitted it, and which transformations or transfers occurred before use.
- **coverage** is the set of actors, actions, resources, paths, stages, environments, and time intervals for which the evidence design intends to produce usable records.
- **completeness** is the supported degree to which required events within that coverage reached the evidence store; it must account for known exclusions and loss.
- **integrity** is resistance to undetected alteration, deletion, insertion, reordering, or substitution after an event is produced.
- **authenticity** is confidence that the claimed producer emitted a record; a valid signature does not establish truthfulness or completeness.
- **chain of custody** is the attributable history of collection, transfer, storage, access, export, and disposition of evidence.
- A **decision record** captures an enforcement result together with the policy revision, material input references, decision identifier, and reason needed for explanation or bounded replay.
- **event time** is when the source says an action occurred; **observed time** is when another component received or observed it.
- **correlation** links records about the same request, workflow, deployment, identity session, artifact, or resource without assuming that timestamps alone establish identity.
- **legal hold** suspends normal disposition for specifically governed evidence; it is not permission to retain all telemetry forever.

### Central model, mechanism, or theorem

For a claim $q$ evaluated at time $t$, let $R_q$ be its required record set and let each record $r$ carry producer, subject, action, event/observed time, policy/schema revision, sequence/correlation identifiers, and integrity metadata. Define

$$
Support(q,t)=Coverage(R_q)\land Delivery(R_q)\land Authenticity(R_q)
\land Integrity(R_q)\land Semantics(R_q)\land Custody(R_q,t).
$$

The conclusion is bounded by the weakest term. Hashing complete-looking files cannot repair a missing observation point; a complete stream from an untrusted producer cannot establish authenticity; authentic records with ambiguous schemas cannot support semantic replay. “No matching event” supports “no observed event in the declared coverage interval,” not “the action did not occur.”

### Critical invariants

- Every evidence objective names the claim, authoritative observation point, event classes, fields, retention, access, expected latency, and acceptable loss.
- Actor identity distinguishes human, workload, controller, delegated session, and infrastructure service; initiator and executor are preserved when both are known.
- Resource identity uses stable identifiers plus namespace/account/cluster and generation or version, not display name alone.
- Decision evidence binds result to exact policy revision, parameter/data revisions, enforcement point, input digest or safe projection, and decision identifier.
- Source event time and collector observed time remain separate; clock source, skew, and uncertainty are measured.
- Sequence, checkpoint, delivery acknowledgement, duplicate, late arrival, and loss signals make pipeline gaps visible.
- Raw evidence is written to access-controlled, retention-governed storage before lossy normalization; transformation lineage and schema versions remain reproducible.
- Integrity controls protect both records and manifests/checkpoints, with keys and trust roots separated from ordinary platform administration.
- Evidence access, search, export, redaction, hold, and deletion are themselves authorized and audited.
- Sensitive bodies, tokens, secrets, personal data, and tenant data are minimized or masked at the earliest trustworthy point consistent with the claim.
- Control effectiveness is assessed with tests and independent observations; configuration presence or log existence is never reported as proof that a control worked.
- Known blind spots, disabled intervals, unsupported sources, sampling, rate limiting, and collection failures are first-class evidence.

### Common failures

Logging only denials; recording the human but not a controller executor; using resource names without stable IDs; omitting old state; collecting request bodies containing secrets; redacting after broad access; trusting source timestamps as ordered truth; correlating by time alone; sampling security events; dropping events silently under backpressure; accepting collector health as delivery proof; normalizing away original fields; mutable index mistaken for immutable archive; hash without trusted anchor; signature mistaken for truthful producer; retention copied from a vendor default; legal hold applied to an entire lake; reviewers querying production directly; policy decision without revision or input; generated report without query and dataset digest; audit disabled during recovery; backup restore losing locks or retention; and claiming absence of activity from absence of records.

### Compact example

A production deletion passes through an authenticated platform API and Kubernetes API. The platform records request, initiating human, executing workload identity, tenant, correlation and decision IDs, resource UID/version, policy bundle digest, safe input digest, allow result, and reason. Kubernetes records request and response stages under a reviewed audit policy. Collectors assign observed time and per-source sequence, acknowledge durable raw writes, and publish gap counters. Hourly manifests hash ordered raw segments and are signed by a separately authorized key; immutable retention and access audit protect the archive. A case export includes query revision, time/coverage declaration, manifest roots, selected record hashes, redaction rules, reviewer identity, and known gaps. It supports a precise claim about the observed deletion, not a universal claim that no bypass occurred.

### Connections

Audit evidence makes the identity, isolation, policy, admission, and supply-chain decisions from PLAT-071–078 reviewable. It consumes observability foundations from PLAT-061–070 while imposing stronger completeness, custody, privacy, and integrity requirements than ordinary debugging telemetry. It also feeds platform SLOs, incident response, compliance assessment, cost governance, and the autonomy/guardrail negotiation in PLAT-080.

## Governing Question

How can a platform make important actions explainable and assessable months later when identities, policies, resources, schemas, topology, and vendor systems have changed since the action occurred?

The answer is not “retain more logs.” Evidence is designed backward from a claim. A platform must define the observation boundary, preserve the meaning and lineage of records, expose losses, and let a reviewer reproduce the reasoning under controlled access.

Audit is also a product interface. Developers need a timely answer to “why was this denied?” Security needs trustworthy detection and investigation. Risk teams need repeatable control assessment. Tenants need isolation and appropriate access. Operators need a system that degrades without taking the production control plane down.

## Why This Matters

Platform teams centralize high-impact operations: identity federation, cluster and account creation, secrets, deployments, artifact promotion, network policy, databases, and destructive workflows. A single platform action may fan out through controllers and cloud APIs. Without correlation and stable subject identity, the final infrastructure change becomes detached from the initiating request.

Evidence has several audiences with different questions. An operator reconstructs an outage. A security analyst scopes malicious credentials. An auditor evaluates whether a control operated during a period. A developer explains a policy decision. A privacy reviewer verifies disposition. One undifferentiated event stream usually satisfies none well.

Weak audit design creates false assurance. A dashboard can show zero violations because the agent stopped sending. An immutable bucket can preserve incomplete records perfectly. A signed event can faithfully report a compromised producer’s lie. A successful API response does not prove the intended resource converged.

Excessive collection is harmful too. Request bodies may contain credentials, personal data, proprietary source, or tenant payloads. Long retention and broad search multiply breach impact and cost. Evidence architecture must minimize data, partition access, document purpose, and delete when obligations end.

## Prerequisites and Retrieval

Retrieve threat modeling; authentication, authorization, workload identity, delegation, session and token semantics; distributed systems and controllers; clocks, NTP/PTP, ordering, UUIDs and sequence numbers; hashes, signatures, Merkle/hash chains, timestamps, trust roots, key rotation and revocation; structured logging and schemas; Kubernetes audit policy/stages/levels; cloud control-plane audit services; OpenTelemetry log records and trace context; policy decision logs; object storage retention/immutability; encryption and key management; queues, checkpoints, acknowledgements, backpressure and replay; data classification, privacy, legal hold and disposition; incident response and forensics; control objectives and assessment procedures; query versioning; backup/restore; and cost modeling.

Distinguish audit from application debug logging; event from evidence claim; source from collector; initiator from executor; identity name from immutable identity attributes; resource name from UID/version; request from decision from effect; event time from observed time; correlation from causation; ordering from clock proximity; integrity from authenticity from accuracy; completeness from availability; immutable storage from immutable index; retention from legal hold; redaction from deletion; control design from implementation from operating effectiveness; and “no observed event” from “no event occurred.”

## Learning Objectives

After completing this module, you should be able to:

1. translate audit and investigation questions into explicit evidence claims, observation points, coverage, fields, and assurance requirements;
2. design a canonical event envelope that preserves actor, subject, action, outcome, time, correlation, policy/schema revision, and provenance;
3. correlate platform, Kubernetes, cloud, policy, CI/CD, artifact, and runtime records without relying on timestamps alone;
4. quantify pipeline delivery, duplicates, late arrivals, gaps, clock uncertainty, and query reproducibility;
5. separate raw custody-preserving evidence from normalized indexes, derived detections, dashboards, and reports;
6. apply hashing, signed checkpoints, immutable retention, key separation, access audit, and restore verification with correct guarantee boundaries;
7. minimize sensitive data, partition tenant access, govern redaction, retention, hold, export, and deletion;
8. record policy and supply-chain decisions so reviewers can explain or replay them under pinned revisions and inputs;
9. test evidence controls through synthetic canaries, fault injection, independent reconciliation, case exercises, and restoration; and
10. operate audit collection as a reliable platform capability with SLOs, cost controls, safe degradation, and explicit blind spots.

## Core Exposition

### Begin with claims and audiences

Write the question before choosing a log source. “Who changed production network access?” requires the initiating principal, delegated executor, old and new resource state or a meaningful diff, decision, persistence result, downstream convergence, and applicable environment. A generic HTTP access log is insufficient.

For each claim, identify audience, purpose, authority, observation point, event classes, minimum fields, acceptable latency/loss, retention, privacy class, access roles, and validation method. A control assessor may need a statistically or fully defined period; an incident responder needs rapid search and raw export; a developer may need only a redacted decision explanation.

Separate preventive evidence, detective evidence, and assessment evidence. A policy decision shows what an enforcement point returned. A later inventory observation shows what existed. A test record shows whether a configured control rejected a known-bad request. Together they support stronger conclusions than any alone.

State the negative claim carefully. If every relevant request must traverse a protected API, audit policy covers the verbs/resources, collection loss is bounded, and the interval is intact, absence becomes meaningful within that boundary. If direct cloud, node, datastore, break-glass, or restore paths exist, include or disclose them.

### Define an evidence contract

An evidence contract is a versioned schema plus semantic obligations. It defines required fields, identifiers, cardinality, allowed values, producer authentication, privacy classification, delivery behavior, ordering/loss signals, retention class, and compatibility policy.

A useful canonical envelope includes event ID; schema and producer versions; producer identity and environment; event and observed timestamps; source sequence or checkpoint; initiating and executing identities; tenant/account/cluster; action and stage; subject type, stable ID, name and version; result/status/reason; request, trace, workflow and decision IDs; policy/data/artifact revisions; safe input/output references or digests; integrity/custody metadata; and classification.

Do not flatten away source meaning. Preserve the raw record and source schema. Normalize selected fields into an index while retaining mapping version and transformation digest. When a parser changes, rebuild the derived view from governed raw data rather than rewriting history invisibly.

Schema evolution is an assurance issue. Additive optional fields are easier than changing identity semantics. Consumers must reject or quarantine unsupported security-critical versions instead of silently defaulting missing fields to safe values.

### Preserve initiator, executor, and delegation

A human may request a deployment; a platform service authorizes it; a controller service account creates a Kubernetes workload; a cloud controller creates a load balancer. Each identity is true at a different edge. Recording only the final executor loses intent, while copying the original user into every event without authentication creates spoofable attribution.

Carry signed or otherwise authenticated delegation context where the architecture supports it. Record the direct caller independently. Link both with request/workflow identifiers and parent-child relationships. Preserve immutable issuer, subject, audience, session, credential/key identifier, and authentication method as policy permits; display names are secondary.

For shared controllers, record the parent object UID/generation and reconcile child operations back to the admitted parent. Do not claim the controller’s API credential proves which human initiated a queued action unless the workflow evidence establishes that link.

Break-glass use needs reason, approver or declared emergency authority, bounded credential/session, target scope, start/expiry, actions, and after-action review. Never log the credential value itself.

### Identify resources and state transitions

Names are often reusable. Use cloud resource IDs, Kubernetes UID plus namespace/cluster, database identifiers, artifact digests, repository immutable IDs, and policy bundle digests. Record resource generation/version when the question involves a particular state.

For changes, capture safe old/new state or a canonical diff when necessary. Bodies are expensive and sensitive, so prefer allowlisted fields, hashes, object-store references under stricter access, or domain events. A hash can prove equality to later supplied bytes but cannot reveal the change.

Distinguish accepted request, persisted state, controller reconciliation, and observed runtime effect. A successful create audit event can precede a failed controller. Evidence of each stage prevents “API success” from being reported as “service delivered.”

Deletion requires tombstone-quality identity because the resource may be unavailable later. Preserve UID, last version, owner/tenant, deletion actor, policy decision, protection/finalizer state, and disposition result where required.

### Record policy decisions reproducibly

A decision record should contain a unique decision ID, enforcement point, action/subject, result, stable reason/rule identifiers, policy engine/version, exact policy bundle revision or digest, parameter/data revisions, relevant trust/revocation snapshot, and input digest or minimized replay projection.

OPA decision logs illustrate bundle revision, path, input, result, requester, timestamp, decision ID, and optional trace context. Their masking feature is important because policy inputs and results can contain secrets or personal data. Rate limiting or dropping must be treated as a coverage loss, not an invisible optimization.

Full deterministic replay may be impossible when policy calls time, network, randomness, changing inventory, or external risk data. Either eliminate those dependencies from the enforcement path, snapshot their material results, or label replay as partial. Store engine and schema versions needed to interpret the policy.

Explanation differs from replay. A stable rule ID and safe reason may explain a denial without retaining the entire request. High-impact approvals and exceptions additionally need owner, approver, scope, justification, controls, issue reference, created/expiry time, and revocation evidence.

### Correlate across boundaries deliberately

Use independent identifiers for different scopes: request ID for one API exchange, trace ID for distributed execution, workflow/run ID for asynchronous orchestration, decision ID for a policy evaluation, resource UID for lifecycle, and artifact digest for bytes. Record parent links when one creates another.

W3C Trace Context standardizes HTTP propagation for distributed tracing, but trace headers originate in an untrusted transport unless the receiving boundary establishes trust. Regenerate or authenticate context at trust boundaries, constrain baggage, and never authorize solely from a trace ID.

Asynchronous queues must carry durable causation metadata across retries and fan-out. Each consumer records message/event ID, attempt, parent workflow, direct workload identity, and produced resource. Idempotency keys help distinguish retry from a new requested effect.

Correlation by approximate time is a fallback with uncertainty, not an exact link. Shared NAT addresses, recycled pod names, clock skew, high event rates, and batching make time-plus-name joins dangerous.

### Treat time and ordering as evidence fields

OpenTelemetry distinguishes source `Timestamp` from `ObservedTimestamp`. Retain both. Their difference helps detect clock error, buffering, and transport delay but does not by itself diagnose which component is wrong.

Synchronize clocks, monitor offset and source, and record uncertainty for sensitive workflows. A wall clock cannot totally order distributed events. Use per-source monotonic sequence, API resource version where semantically valid, queue offsets, workflow edges, and signed checkpoints.

Late events should be admitted with original event time and arrival time. Queries define whether they use event-time or ingest-time windows and how long results remain provisional. Periodic compliance reports should record a close/watermark rule and be regenerable when late data arrives.

Clock rollback, leap handling, suspended VMs, node replacement, and restore are test cases. Never overwrite a source timestamp during normalization.

### Engineer observable delivery and loss

The path is producer, local buffer/agent, transport, collector, queue, raw store, parser, index, query, and export. Each edge can lose, duplicate, reorder, delay, corrupt, or reject events. Define acknowledgement only after the intended durability boundary.

Use source sequence or offset, persistent checkpoints, idempotent event IDs, bounded retry, dead-letter/quarantine, and per-stage accepted/rejected/dropped counters. Record configuration changes and restarts for producers and collectors. Alert on silence only when expected event volume or synthetic canaries makes silence interpretable.

Sampling is suitable for some performance telemetry, not for sparse high-impact audit events. If sampling is unavoidable, record method/rate and prohibit unsampled conclusions. Rate limiting, size rejection, malformed payloads, disk pressure, queue exhaustion, and backend quota must expose loss counters and affected intervals.

Keep audit collection off the synchronous control path unless the risk explicitly requires durable audit before success. A synchronous remote backend can stop the platform during an outage. Local durable buffering, bounded fail behavior, and priority classes usually provide a safer trade-off.

### Separate raw evidence, indexes, and reports

Raw evidence is the closest retained representation to the source, with provenance and custody. A normalized index accelerates search. A detection is a derived claim. A report or case export selects and presents records. These are distinct layers.

Index deletion or corruption should be recoverable from raw segments. Raw retention may differ from searchable retention. Query results must record query text/version, parameters, execution time, dataset/partition manifest, parser/index version, row count, result digest, redaction, and reviewer.

Dashboards are navigation aids, not durable evidence unless exported with their data and transformation definition. Screenshots omit filters, late data, permissions, and source revisions.

Store important assessment packages as manifests referencing immutable records and control tests. Revalidation should detect missing source objects, changed query code, invalid signatures, or expired trust assumptions.

### Protect integrity and authenticity

Transport authentication and encryption protect collection edges. Storage policies restrict mutation and deletion. Hash each raw segment and create ordered manifests containing source, interval, sequence range, count, segment hashes, previous checkpoint, schema/collector revision, and known loss. Sign or timestamp checkpoints under separated authority.

A chained digest makes deletion or modification detectable only relative to a trusted checkpoint and available chain. If the attacker controls both record store and signing key, the guarantee collapses. Separate keys, roles, accounts/projects, and administrative paths; rotate and revoke with verifiable history.

AWS CloudTrail’s digest design is a useful concrete example: log-file hashes appear in signed digest files, and digest files reference previous signatures. The design can expose later modification or deletion within enabled, delivered intervals; it does not prove that every real-world action generated a CloudTrail record.

Periodically validate stored segments and checkpoints from an independent environment. Restore a sample archive and reproduce a case package. Integrity validation that is enabled but never executed is an untested control.

### Maintain chain of custody

Custody begins at production, not when an investigator downloads a file. Record producer/collector identity, receipt time, source partition/sequence, transformation, raw object ID/hash, storage policy, and every privileged access, export, redaction, hold, or disposition event.

Case exports should be read-only packages with manifest, source references/hashes, verifier instructions, query/reduction history, time/coverage statement, known gaps, reviewer/exporter identity, and access classification. Work on verified copies while preserving originals.

Avoid claiming evidentiary admissibility from a technical pattern alone; jurisdictions, contracts, organizational procedures, competence, and documentation matter. Platform engineering supplies traceability and integrity controls for authorized legal and compliance processes.

Audit the auditors. Search queries may reveal sensitive relationships even if raw values are masked. Use case-scoped, time-bound access, separation of duties for highly sensitive sources, export approval, watermarking where appropriate, and anomaly detection on evidence access.

### Minimize and partition sensitive data

Collect fields needed for declared purposes. Secrets, credentials, authorization headers, tokens, cookies, private keys, full environment variables, database payloads, and arbitrary request/response bodies are denied by default. Allowlisting is safer than chasing secret patterns after ingestion.

Redact at the earliest trustworthy producer or collector, before broad transport and storage. Preserve a redaction rule revision and record that redaction occurred. Hashing low-entropy personal data is often reversible by guessing and still creates a stable identifier; use keyed pseudonyms with governed rotation when correlation is necessary.

Partition by tenant, environment, data class, and purpose. Central collection does not imply universal search. Support tenant-visible records with platform-sensitive fields removed, while restricting security and custody metadata to appropriate roles.

Encryption at rest is necessary but does not replace authorization. Key access, decryption, query, export, and backup paths require controls. Test deletion across raw objects, indexes, caches, replicas, exports, and backups subject to documented retention and hold obligations.

### Govern retention, hold, and disposition

Retention follows purpose, risk, contractual/regulatory obligations, investigation horizon, source cost, and privacy. Define it by evidence class rather than copying one duration to every source. Searchable hot, compressed raw, case package, and aggregate retention may differ.

Legal hold identifies custodians/sources, scope, authority, start, review, release, and affected disposition jobs. It must be narrow and auditable. On release, ordinary retention resumes; held data does not automatically get a new lifetime.

Deletion is a workflow with evidence. Record due objects, applicable policy/hold, deletion execution, failures, retries, and verification. Crypto-erasure may help when encryption keys have isolated scope, but shared keys make selective deletion impossible.

Budget storage, ingestion, indexing, query, egress, replication, and restore. Control cardinality and body size at contracts, not through silent backend truncation. Cost alerts must never silently disable high-value audit classes.

### Assess controls instead of counting logs

NIST SP 800-53A structures assessment around examination, interview, and testing procedures. For a platform control, examine policy/configuration and records, interview accountable operators where required, and test behavior with authorized scenarios. Log presence is one evidence input.

For “production privileged pods are denied,” inspect policy revision and scope, test a known violating request at every relevant path, verify denial decision and Kubernetes audit records, query current inventory for prohibited state, test exceptions, and reconcile bypass-capable paths. This tests design, implementation, and operation.

Use synthetic audit canaries that perform safe, uniquely identified actions and verify end-to-end arrival, schema, correlation, integrity checkpoint, search, and deletion at expected times. Canaries validate their path, not every source; rotate cases across the coverage matrix.

Track evidence SLOs: required-source coverage, durable delivery rate, p99 availability latency, gap detection time, clock-offset bounds, parse/quarantine rate, query success/latency, integrity-validation success, access-review completion, disposition timeliness, and restore/replay success.

### Design degraded operation and recovery

Prioritize events by consequence. Identity, authorization, policy change, privilege, secret access, artifact promotion, production mutation, break-glass, audit configuration, and evidence access deserve durable priority over verbose debug records.

When transport or storage is unavailable, buffer locally within protected quotas, shed only declared lower-priority classes, expose affected interval, and recover in order without duplication. For actions requiring non-repudiable audit before execution, define fail-closed scope and a separately governed emergency path.

The evidence system must not recursively depend on itself for recovery authorization. Preserve offline runbooks, bounded recovery identity, alternate integrity verification, and ability to restore raw archives plus manifests, keys/trust metadata, schemas, parsers, queries, access policies, and holds.

Audit configuration is high-risk configuration. Changes to sources, policies, levels, filters, masks, sampling, routes, storage locks, retention, keys, or privileged access receive review, versioning, rollout evidence, and independent alerts.

### Build the capability incrementally

Inventory current claims, sources, blind spots, identities, schemas, stores, costs, access, retention, and obligations. Select a small high-impact journey such as production deployment or tenant provisioning and map end to end.

Establish canonical identifiers and evidence contracts before centralizing everything. Route to a durable raw tier and one reproducible index. Add gap telemetry, synthetic canaries, query manifests, access audit, and integrity checkpoints.

Migrate consumers from ad hoc dashboards to versioned queries and case packages. Remove duplicate sensitive streams only after parity is demonstrated. Enforce producer/schema requirements at onboarding and treat undocumented loss as a release blocker for high-impact controls.

Review evidence objectives periodically. A new controller, API version, direct cloud path, region, restore mechanism, policy engine, or tenant model changes coverage even if the logging backend stays healthy.

## Definitions and Notation

Let $S$ be the set of governed sources and $I=[t_0,t_1]$ an assessment interval. For source $s$:

- $E_s(I)$ is the events the evidence contract says should be emitted within $I$;
- $D_s(I)$ is the distinct events durably received, after deduplication;
- $g_s(I)$ is known loss from sequence gaps, rejection, drops, or disabled intervals;
- $u_s(I)$ is unresolved uncertainty where the expected event count is not directly observable;
- $\delta_s$ is the measured clock-offset bound for the relevant interval;
- $M_s$ is the ordered raw-segment manifest with hashes and checkpoint links;
- $P_s$ is producer, collector, schema, parser, and transformation provenance;
- $A_s$ is the authorization and custody history for evidence access and mutation.

For a record $r$:

$$
r=(id,producer,actor,executor,action,subject,state,result,t_e,t_o,seq,corr,rev,class).
$$

Here $t_e$ and $t_o$ are event and observed time, `seq` is source ordering/checkpoint data, `corr` is a typed set of correlation identifiers, `rev` contains policy/data/schema revisions, and `class` governs sensitivity and retention.

When an expected count is available, a delivery estimate is

$$
C_s(I)=\frac{|D_s(I)|}{|D_s(I)|+g_s(I)},
$$

but $C_s=1$ does not mean complete if $u_s>0$ or the source itself omitted actions. Report $(C_s,g_s,u_s)$ and coverage assumptions rather than a context-free percentage.

A query result is represented by

$$
Q=(query\_digest,parameters,dataset\_manifest,parser\_revision,
executed\_at,result\_digest,redaction,reviewer).
$$

This makes later reproduction testable even when a hot index has expired.

## Mechanisms, Invariants, or Proof Structure

### Evidence-production mechanism

1. Define a bounded claim, audience, purpose, interval, decision consequence, and assurance level.
2. Enumerate authoritative and corroborating observation points, including alternate, recovery, and bypass paths.
3. Specify versioned event contracts, stable actor/subject identifiers, safe state representation, and policy/schema revisions.
4. Authenticate producers and transports; assign observed time, event ID, sequence/checkpoint, and provenance at collection.
5. Buffer and acknowledge against a declared durability boundary; expose duplicates, rejection, late arrival, gap, and disabled intervals.
6. Write source-preserving raw segments under partitioned access and retention before lossy parsing or aggregation.
7. Hash segments, create ordered count/sequence manifests, and anchor signed checkpoints under separated authority.
8. Normalize through versioned transformations while retaining raw references and quarantining unsupported or malformed events.
9. Correlate through typed request, trace, workflow, decision, resource, and artifact identifiers; state uncertainty for inferred joins.
10. Produce detections, explanations, assessments, and exports with versioned query and dataset manifests.
11. Audit evidence access, masking, export, holds, and disposition; test restore and independent integrity verification.
12. Reconcile canaries and independent inventories, publish coverage/SLOs and blind spots, and revise contracts as platform paths change.

### Attribution invariant

Every reported actor is supported by the authentication boundary that observed it. Direct caller, initiating identity, delegated executor, controller, and approver remain distinct. A copied username or trace field never becomes authoritative merely by appearing in several logs.

### Subject invariant

Every material record identifies the governed subject with stable environment and version context. Reused names cannot merge histories, and a policy decision for one resource generation or artifact digest cannot transfer to another.

### Decision invariant

Every consequential allow, deny, warn, mutate, approve, promote, exempt, revoke, or break-glass result binds to the exact enforcement point and policy/data/trust revisions used. If replay inputs are omitted for privacy or practicality, the limitation is explicit.

### Delivery invariant

Every collection edge either durably acknowledges an event or exposes a bounded retry, rejection, drop, sequence gap, or uncertain interval. Downstream success metrics cannot erase upstream unknowns.

### Custody invariant

Raw record, manifest, transformation, query, access, export, hold, and deletion histories form a traceable chain. Any gap in custody narrows the claims that can be supported.

### Proof sketch: event absence cannot prove action absence without coverage

Suppose query $Q$ returns no record for action $a$ during interval $I$. Construct two worlds with the same stored dataset: in $W_0$, $a$ never occurs; in $W_1$, $a$ occurs through an unobserved bypass or while the producer is disabled. Because the query input is identical, $Q$ returns empty in both worlds. Therefore the empty result alone cannot distinguish non-occurrence from non-observation.

Add premises: every path capable of $a$ crosses source set $S$; each source contract emits the relevant class; source configuration is continuously evidenced; sequence/checkpoint reconciliation reports no gaps; clocks and query window include uncertainty; and raw/index/query transformations are verified. Under those bounded premises, absence supports “no observed action within governed coverage.” It still does not prove facts outside $S$, $I$, the defined action semantics, or the assumed producer correctness.

### Executable coverage audit

The following synthetic program classifies ten source intervals by their first unsupported assurance condition. It demonstrates explicit gaps and uncertainty; it does not validate a real collector, signature, clock, or storage system.

<!-- bijux-verify: {"id":"audit-evidence-coverage","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"supported=5\ndelivery_gap=1\nproducer_gap=1\nintegrity_gap=1\nsemantic_gap=1\ncustody_gap=1\n"}} -->
```python
from dataclasses import dataclass


@dataclass(frozen=True)
class SourceInterval:
    name: str
    expected: int
    received: int
    producer_attested: bool
    manifest_valid: bool
    schema_supported: bool
    custody_complete: bool


intervals = [
    SourceInterval("identity", 120, 120, True, True, True, True),
    SourceInterval("policy", 90, 90, True, True, True, True),
    SourceInterval("kubernetes", 410, 410, True, True, True, True),
    SourceInterval("cloud", 75, 75, True, True, True, True),
    SourceInterval("artifact", 30, 30, True, True, True, True),
    SourceInterval("delivery", 55, 54, True, True, True, True),
    SourceInterval("producer", 20, 20, False, True, True, True),
    SourceInterval("integrity", 40, 40, True, False, True, True),
    SourceInterval("semantic", 65, 65, True, True, False, True),
    SourceInterval("custody", 12, 12, True, True, True, False),
]

counts = {
    "supported": 0,
    "delivery_gap": 0,
    "producer_gap": 0,
    "integrity_gap": 0,
    "semantic_gap": 0,
    "custody_gap": 0,
}

for interval in intervals:
    if interval.received != interval.expected:
        counts["delivery_gap"] += 1
    elif not interval.producer_attested:
        counts["producer_gap"] += 1
    elif not interval.manifest_valid:
        counts["integrity_gap"] += 1
    elif not interval.schema_supported:
        counts["semantic_gap"] += 1
    elif not interval.custody_complete:
        counts["custody_gap"] += 1
    else:
        counts["supported"] += 1

for key, value in counts.items():
    print(f"{key}={value}")
```

### Verification strategy

Validate contracts with schema and semantic tests; inject unique canaries at each observation path; compare producer sequence/counts with durable raw manifests; simulate transport loss, duplicates, reordering, disk pressure, malformed/oversized records, clock skew, collector restart, queue exhaustion, index rebuild, key rotation, compromised administrator, disabled audit, legal hold, and region restore.

Independently verify segment hashes and signed checkpoints, then reproduce a historical query and case export from restored raw data. Confirm authorization boundaries for tenant, operator, security, assessor, privacy, and legal roles. Seed secrets and personal-data markers in authorized test inputs and prove prohibited values do not reach raw, index, export, or backup tiers.

For control evidence, combine examination, interview where applicable, and direct testing. A synthetic denial tests one policy path; inventory reconciliation checks prohibited state; audit and decision records explain the evaluation; bypass tests bound coverage. Record failures as evidence gaps rather than editing them out of the report.

## Alternatives and Trade-Offs

1. **Application events versus infrastructure audit:** domain events express business meaning; infrastructure audit independently observes API actions. Use both for important claims.
2. **Full bodies versus metadata:** bodies improve reconstruction but increase secret/privacy/cost risk. Prefer allowlisted fields, diffs, digests, and governed references.
3. **Centralized lake versus federated stores:** central search improves correlation; federation preserves residency and tenancy. A manifest/query layer can span governed partitions.
4. **Synchronous audit versus asynchronous delivery:** synchronous durability strengthens selected actions but adds availability coupling. Reserve it for explicitly high-consequence paths.
5. **Fail closed versus continue with gap:** fail closed protects non-repudiation but can stop recovery; continuing needs bounded emergency scope, gap evidence, and reconciliation.
6. **Every event versus sampling:** complete high-value classes support audit; sampled high-volume telemetry controls cost but cannot support complete counts.
7. **Source normalization versus raw preservation:** normalization speeds query; raw preservation retains semantics and reparsability. Maintain both with lineage.
8. **Hot searchable retention versus cold raw retention:** hot data lowers response time; cold storage lowers cost. Test retrieval and rebuild, not just storage existence.
9. **Object lock versus administrative flexibility:** immutability resists deletion but can preserve sensitive mistakes and increase cost. Partition and predefine retention.
10. **Hash chains versus signed checkpoints:** chains expose sequence discontinuity; signatures add an authenticated anchor. Neither covers omitted source events.
11. **Provider-native audit versus unified envelope:** native logs have authoritative fields; a unified envelope improves cross-platform query. Never discard the native representation.
12. **Trace propagation versus local correlation:** traces connect services; local request/resource IDs limit trust propagation. Treat external trace context as untrusted input.
13. **Deterministic replay versus minimized explanation:** replay needs more inputs and versions; explanation can retain less sensitive data. Classify decisions by consequence.
14. **Tenant self-service search versus brokered export:** direct search is timely but risks cross-tenant inference; brokered packages offer stronger review at higher latency.
15. **Long retention versus minimization:** longer windows aid investigations and obligations; they magnify exposure and cost. Govern by evidence purpose and class.
16. **Shared signing key versus separated integrity authority:** shared operations are simpler; separated keys prevent ordinary storage admins from silently rewriting anchors.
17. **Mutable dashboards versus versioned assessment packages:** dashboards aid live exploration; packages support repeatability and review.
18. **Vendor SIEM versus portable raw archive:** managed analytics accelerate adoption; portable governed raw data reduces lock-in and preserves future reparsing.

## Failure Modes and Misconceptions

- **“All logs are audit logs.”** Debug verbosity does not create stable identity, coverage, custody, or retention semantics.
- **“The event says a user, so attribution is proven.”** The field may be copied or spoofed; bind it to the authenticating observation point.
- **“Controller identity is enough.”** It identifies the executor, not necessarily the initiating human or parent workflow.
- **“A trace ID is authorization.”** Trace context is correlation input and may cross untrusted boundaries.
- **“Timestamps establish order.”** Distributed clocks skew; use causal links, sequence, and explicit uncertainty.
- **“Request success proves effect.”** Persistence and downstream convergence are separate observations.
- **“A resource name is permanent identity.”** Names can be reused across tenants, clusters, accounts, or time.
- **“Policy result is reproducible.”** Not without exact policy, parameters, data/trust snapshot, engine semantics, and material inputs.
- **“Log everything, redact later.”** Sensitive data has already crossed and entered systems before later masking.
- **“Hashing makes records trustworthy.”** Hashing detects change only relative to a trusted value; it does not prove origin or truth.
- **“A signature proves the event happened.”** It proves control of signing authority over bytes, subject to trust and key security.
- **“Immutable storage proves completeness.”** It preserves what arrived, including an incomplete set.
- **“No alert means no attack.”** Detection may be disabled, delayed, filtered, or missing coverage.
- **“Collector uptime proves delivery.”** Buffers, parsing, queues, quotas, and storage may still lose data.
- **“At-least-once means complete.”** It permits duplicates and still depends on bounded source/transport behavior.
- **“A normalized index is the original.”** Parsing and field mapping can be lossy or wrong.
- **“Screenshots are sufficient audit evidence.”** They omit source set, query, filters, revisions, and integrity.
- **“Sampling is fine if the rate is known.”** It cannot prove every privileged action was captured.
- **“More retention is always safer.”** It increases privacy, breach, legal, and cost exposure.
- **“Encryption solves access control.”** Authorized decryption, query, export, and key administration remain risks.
- **“Legal hold means keep the whole lake.”** Hold must be scoped, reviewed, released, and audited.
- **“Deletion from the index completes disposition.”** Raw, replicas, caches, exports, and backups may remain.
- **“Compliance is a dashboard.”** Control effectiveness requires defined assessment procedures and corroboration.
- **“Canary success proves all sources.”** It proves only the exercised path and interval.
- **“Cloud audit covers the workload.”** Provider control-plane events do not necessarily describe in-workload or node behavior.
- **“Kubernetes audit is enabled by default everywhere.”** Configuration and policy determine whether and what is recorded.
- **“RequestResponse is always the best Kubernetes level.”** Bodies may expose secrets and consume substantial resources.
- **“Audit backend outage should always stop the API.”** Failure behavior is a risk decision; universal synchronous coupling can destroy availability.
- **“Restoring objects restores evidence assurance.”** Keys, locks, manifests, schemas, access rules, holds, and query tooling must also be restored and verified.
- **“Unknown is equivalent to compliant.”** Missing or ambiguous evidence is a separate result, not a pass.

## Worked Examples

### Example 1

A team asks who granted production database administrator access. The evidence contract covers identity-provider authentication, privileged workflow approval, platform authorization/decision, cloud IAM mutation, and periodic entitlement inventory. It preserves human initiator, platform executor, role/resource immutable IDs, old/new bindings, request/workflow/decision IDs, policy bundle digest, ticket/approval reference, and expiry. The report states a two-minute collector outage as an affected interval rather than hiding it behind a successful final inventory.

### Example 2

A Kubernetes audit policy records metadata for read-heavy requests, request bodies for selected configuration writes, and metadata for secret resources so secret bodies are never captured. It covers create, update, patch, delete, impersonation, authorization review, admission warnings, and audit-policy changes. The platform load-tests API-server memory and audit backend behavior, monitors truncated/batched delivery, and deploys canaries for every protected verb/resource matrix.

### Example 3

A deployment denial record contains decision ID, workload and initiating identities, target cluster/namespace, policy bundle digest, parameter-set digest, artifact digest, stable failed rule IDs, safe field paths, result, event/observed time, and trace/workflow IDs. The raw pod body is not retained. Developers receive a tenant-scoped explanation; security can join to a separately protected Kubernetes event through decision/request IDs.

### Example 4

A controller creates three cloud resources after one platform request. The workflow records parent run ID and authenticated initiator. Each queue message has immutable message ID, attempt, parent, and intended resource key. The controller records direct workload identity and resulting cloud resource ID. Cloud audit independently observes each API call. The graph now distinguishes requested intent, authorization, retries, executor actions, and effects without pretending the cloud provider authenticated the human.

### Example 5

An attacker with storage-administrator access changes a raw segment and rebuilds a search index. Independent hourly signed manifests contain ordered segment hashes and previous checkpoint, stored in a separate security account. Verification detects the mismatch. If the attacker also controlled the signing workload during that hour, authenticity is uncertain; the design therefore uses isolated workload identity, threshold approval for key-policy changes, and external checkpoint replication.

### Example 6

During queue pressure, a collector retains identity, authorization, policy-change, secret-access, production mutation, promotion, and evidence-access classes while shedding sampled debug events. It records per-class rejected counts, sequence gaps, disk/buffer saturation, and interval. The incident report limits claims for the dropped class but can still substantiate high-priority paths. The degradation policy was tested before the outage.

### Example 7

A quarterly assessment of “unsigned images cannot enter production” examines admission and supply-chain policy/configuration, tests an unsigned digest in representative clusters and alternate paths, verifies denial and decision records, reconciles runtime image digests against signature evidence, reviews active exceptions, and exercises break-glass. The package records queries, manifests, policy revisions, test IDs, results, gaps, reviewer, and report digest. A configuration screenshot alone would not assess operation.

### Example 8

A privacy request requires disposition of tenant audit data after its governed period. The catalog identifies raw partitions, normalized indexes, caches, case exports, replicas, and backup schedules. A narrow legal hold excludes only specified records. Deletion jobs emit manifests of due/deleted/failed objects; verification queries confirm absence from active tiers and scheduled backup expiry. The deletion evidence contains object IDs and hashes, not the deleted sensitive bodies.

### Example 9

A region is restored from backup. Operators restore raw objects, signed manifests, trust metadata, schema registry, parser/query versions, tenant partitions, access policy, holds, and audit of evidence access. They validate checkpoint chains, replay a historical case, execute canaries, and compare counts with source checkpoints before declaring the region authoritative. Restoring only the SIEM index would preserve neither custody nor reproducibility.

### Example 10

A platform migrates from five vendor dashboards to a governed evidence plane. It inventories claims and sources, introduces canonical request/workflow/decision/resource IDs, preserves provider-native raw records, builds versioned normalization, and dual-runs old and new queries. Parity includes counts, known exclusions, latency, access, cost, and case reproduction. Only after discrepancy ownership and retention/hold migration are verified does it retire duplicate ingestion.

## Cross-Program Connections

1. **Identity and access management:** authoritative authentication, delegation, session, impersonation, and credential-use evidence determine attribution quality.
2. **Distributed systems:** causal graphs, retries, queues, partial failure, clocks, and convergence explain why a timestamp-sorted log is not a history.
3. **Security engineering:** threat models define producers, bypasses, tampering adversaries, key separation, detections, and incident evidence.
4. **Data engineering:** schemas, lineage, stream delivery, watermarks, late data, partitioning, indexes, and reproducible transformations underpin evidence quality.
5. **Cryptography:** hashes, signatures, timestamps, key rotation, and authenticated checkpoints support bounded integrity/authenticity claims.
6. **Privacy engineering:** minimization, purpose limitation, pseudonymization, access partitioning, retention, hold, and deletion constrain audit collection.
7. **Site reliability engineering:** evidence SLOs, backpressure, degradation priorities, canaries, disaster recovery, and capacity keep collection dependable.
8. **Software supply-chain security:** artifact digests, provenance, signing, promotion, revocation, and policy revisions become subjects in the evidence graph.
9. **Policy as code:** decision IDs, bundle revisions, parameters, masked inputs, explanations, exceptions, and replay connect enforcement to review.
10. **Risk and compliance:** control objectives, examination/testing, sampling boundaries, assessment periods, residual uncertainty, and case custody turn records into defensible conclusions.

## References

1. National Institute of Standards and Technology. [SP 800-92: Guide to Computer Security Log Management](https://csrc.nist.gov/pubs/sp/800/92/final). Retrieved 2026-09-02.
2. National Institute of Standards and Technology. [SP 800-92 Rev. 1 Initial Public Draft: Cybersecurity Log Management Planning Guide](https://csrc.nist.gov/pubs/sp/800/92/r1/ipd). Retrieved 2026-09-02.
3. National Institute of Standards and Technology. [SP 800-53 Rev. 5.1: Security and Privacy Controls for Information Systems and Organizations](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final). Retrieved 2026-09-02.
4. National Institute of Standards and Technology. [SP 800-53A Rev. 5: Assessing Security and Privacy Controls](https://csrc.nist.gov/pubs/sp/800/53/a/r5/final). Retrieved 2026-09-02.
5. National Institute of Standards and Technology. [SP 800-86: Guide to Integrating Forensic Techniques into Incident Response](https://csrc.nist.gov/pubs/sp/800/86/final). Retrieved 2026-09-02.
6. Kubernetes. [Auditing](https://kubernetes.io/docs/tasks/debug/debug-cluster/audit/). Retrieved 2026-09-02.
7. Kubernetes. [Logging Architecture](https://kubernetes.io/docs/concepts/cluster-administration/logging/). Retrieved 2026-09-02.
8. OpenTelemetry. [Logs Data Model](https://opentelemetry.io/docs/specs/otel/logs/data-model/). Retrieved 2026-09-02.
9. OpenTelemetry. [Logging Specification](https://opentelemetry.io/docs/specs/otel/logs/). Retrieved 2026-09-02.
10. World Wide Web Consortium. [Trace Context](https://www.w3.org/TR/trace-context/). Retrieved 2026-09-02.
11. Open Policy Agent. [Decision Logs](https://www.openpolicyagent.org/docs/management-decision-logs). Retrieved 2026-09-02.
12. Amazon Web Services. [Validating CloudTrail Log File Integrity](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-log-file-validation-intro.html). Retrieved 2026-09-02.
13. Internet Engineering Task Force. [RFC 5848: Signed Syslog Messages](https://www.rfc-editor.org/rfc/rfc5848). Retrieved 2026-09-02.
14. Internet Engineering Task Force. [RFC 5424: The Syslog Protocol](https://www.rfc-editor.org/rfc/rfc5424). Retrieved 2026-09-02.

## Exercises

### Exercise 1

Define an evidence contract for production privilege changes spanning identity provider, platform workflow, Kubernetes, and cloud IAM. Include claims, fields, coverage, loss, retention, access, and validation.

### Exercise 2

Design an integrity and custody scheme for multi-region raw audit segments whose storage administrators must not be able to rewrite history undetected.

### Exercise 3

Create an assessment procedure for the claim “only approved, digest-bound artifacts execute in production.” Distinguish design, implementation, and operating evidence.

### Exercise 4

Plan privacy-safe audit for a multi-tenant policy service whose inputs may contain secrets, personal data, and proprietary configuration while developers need denial explanations.

### Exercise 5

Plan migration from provider dashboards and 30-day mutable indexes to a reproducible evidence capability without interrupting investigations or violating existing holds.

## Answers to the Exercises

### Answer 1

State the bounded claims: who requested/approved/executed each grant, which subject/resource/role/version changed, which policy allowed it, whether the provider persisted it, and whether current inventory converged. Cover direct, delegated, controller, break-glass, restore, and alternate cloud paths. Name each authoritative observation point and disclose any path that cannot be observed.

Require immutable issuer/subject/session plus direct workload identity; tenant/account/cluster; stable role/resource IDs; old/new binding or safe diff; request/workflow/decision IDs; policy/parameter digest; approval and expiry; outcome; event/observed time; sequence/checkpoint; schema/producer revision; and classification. Never retain token values.

Use acknowledged raw delivery, per-source sequence/count reconciliation, gap and disabled-interval alerts, signed segment manifests, independent canaries, and entitlement inventory. Retain according to privilege/investigation and legal obligations, partition tenant and sensitive access, audit searches/exports, and validate quarterly through direct/alternate-path tests plus historical query reproduction.

### Answer 2

Authenticate producers and collectors with workload identities. Write ordered source/region segments to versioned object storage with restrictive retention controls. Manifest each interval with source identity, event and sequence range, count, known gaps, collector/schema revision, and segment hashes. Chain manifests to previous checkpoints and sign them using isolated keys unavailable to ordinary storage administrators.

Replicate checkpoints to a separately administered security account or external transparency/timestamp service. Separate storage, signing-key policy, retention, and evidence-review roles; threshold-approve key and lock-policy changes. Audit every privileged read, export, retention change, and deletion. Rotate keys while retaining verification metadata and explicit compromise cutoffs.

Continuously compare producer counts and sequences to manifests. Independently verify signatures, chain continuity, objects, and gap signals. Restore a region and reproduce a historical case. State limits: the scheme detects post-collection alteration/deletion relative to trusted anchors; it cannot prove omitted source actions or honest producer semantics.

### Answer 3

For design, examine requirements for exact image digest, authorized signer/issuer, provenance, SBOM/risk, current revocation, promotion, all image fields, admission, runtime reconciliation, exceptions, and bypass paths. Confirm policy maps these to explicit enforcement points and evidence contracts.

For implementation, inspect pinned policy and trust revisions, deployment/admission configuration, policy scope, collector contracts, decision records, registry/evidence binding, runtime inventory, exceptions, access, and recovery paths. Validate that records contain artifact digest, workload/cluster, decision ID, policy/data revisions, reason, time, sequence, and custody.

For operation, attempt approved and disallowed digests across representative clusters, init/ephemeral/injected containers, controller-generated workloads, outage and break-glass paths. Verify expected decisions and audit records, reconcile every running digest against current evidence, sample promotion history, review exceptions/revocations, and reproduce the period report from raw manifests. Report unknown sources and gaps separately from pass/fail.

### Answer 4

Define a minimal decision envelope: decision and trace IDs, authenticated tenant/workload, action, subject type/stable ID, result, stable rule/reason IDs, policy/parameter digests, event/observed time, and safe field paths. Do not ingest full input/output by default. Use schema allowlists; remove credentials/tokens; replace necessary identities with tenant-scoped keyed pseudonyms; record masking revision.

Generate developer explanations at decision time from safe rule metadata. Provide tenant-scoped access only to their decisions and strip platform/security attributes. Store a more restricted input digest or encrypted reference only for decisions whose consequence justifies replay, with case-bound access and short retention. Snapshot external data revisions without copying sensitive payloads where possible.

Test with seeded secret and personal-data markers across producer, queue, raw, index, export, cache, and backup. Audit queries and exports, alert on bulk access, define class-specific retention and deletion, and disclose when privacy minimization prevents full replay.

### Answer 5

Inventory claims, sources, current dashboards/queries, identity and resource semantics, raw availability, parser/index versions, costs, users, retention, exports, holds, blind spots, and active investigations. Freeze undocumented deletion and preserve held datasets without expanding holds.

Introduce canonical IDs and versioned evidence contracts at high-impact sources. Dual-write provider-native records to governed raw partitions and existing systems. Build normalization with raw references, gap telemetry, signed manifests, access partitions, and reproducible query packages. Backfill only where source authenticity, schema, and custody can be stated; label imported history accordingly.

Port queries one at a time and compare counts, sampled records, exclusions, late data, latency, access, and result digests over overlapping periods. Reproduce open cases and assessment reports, test restore, migrate retention/hold/disposition metadata, and train owners. Retire each old path only after its consumers, investigations, exports, and holds are mapped and parity exceptions resolved. Preserve a rollback/read-only window and never claim historic assurance that the legacy system did not provide.
