---
module_id: DE-089
program: Data Engineering
level: 2
module_number: 89
title: Auditability and Provenance
status: complete
last_verified: 2026-09-03
---

# Auditability and Provenance

## One-Page Review

### Governing question

How can a data organization produce evidence that a specific actor or workload performed a specific action under a specific policy on exact input and output versions, while preserving causality, time, integrity, completeness limits, confidentiality, and chain of custody—and without treating an append-only table, hash, dashboard, or compliance label as proof of truth?

### Essential definitions

- **Auditability** is the engineered ability to reconstruct and evaluate consequential actions and control decisions from attributable, interpretable, protected, retrievable evidence.
- An **audit event** records a security-, governance-, or operation-relevant occurrence. It is evidence about an occurrence, not the occurrence itself.
- **Provenance** records the entities, activities, and agents involved in producing, influencing, or delivering data or another thing.
- An **entity** is a versioned thing with fixed aspects for the claim being made; an **activity** uses or generates entities over time; an **agent** bears some responsibility.
- **Lineage** is the dependency-oriented portion of provenance, commonly describing which inputs contributed to which outputs through which transformations.
- **Attribution** relates an entity to a responsible agent; **association** relates an activity to an agent; **delegation** records that one agent acted on behalf of another.
- A **decision receipt** records inputs, policy/version, subject and workload, decision, reason, time, and correlation needed to explain an authorization or governance decision.
- **Event time** is when an occurrence is asserted to have happened; **record time** is when the source recorded it; **ingest/observed time** is when another system received it.
- **Canonicalization** maps a logical record to one deterministic byte representation before hashing or signing.
- **Tamper evidence** makes certain after-the-fact changes detectable under stated assumptions. It does not prevent change or prove capture truth.
- A **hash chain** binds each canonical event to the prior digest. A **Merkle tree** supports compact inclusion and consistency proofs over a committed set or sequence.
- An **anchor** is an independently protected checkpoint, signature, timestamp, or publication used to detect rewriting beyond one administrative boundary.
- **Completeness** means required eligible events were captured and remain queryable; it requires a trustworthy denominator or reconciliation source.
- **Chain of custody** is the documented sequence of collection, handling, transfer, analysis, storage, and disposition for evidence.
- **Auditability debt** is the accumulated gap between claims that must be explainable and the evidence actually captured, protected, and testable.

### Central model, mechanism, or theorem

Represent an evidence event as

$$
e_i=\langle id,actor,effectiveSubject,workload,action,objects,policy,
t_e,t_r,t_o,outcome,reason,correlation,schema,previousDigest\rangle.
$$

Represent provenance as a directed labeled graph $G=(V,R)$ whose vertices include entities, activities, and agents, and whose relations include usage, generation, derivation, attribution, association, and delegation. Version identity is part of the claim: “table A influenced report B” is weaker than “snapshot A@42 was used by run R7, which generated report B@9.”

For canonical byte encoding $C(e_i)$ and collision-resistant hash $H$:

$$
h_i=H(h_{i-1}\parallel C(e_i)).
$$

Given a protected known checkpoint $h_k$, recomputation can detect covered byte modification, reordering, or interior deletion before that checkpoint under the hash and canonicalization assumptions. It cannot establish that the source told the truth, that every required event was emitted, that an omitted tail never existed, or that the attributed human actually controlled a credential.

Coverage may be reported as

$$
Coverage(W)=\frac{|ObservedRequired(W)|}{|EligibleRequired(W)|},
$$

only when an independent control surface can establish the denominator for window $W$. Otherwise report denominator status and gaps, not a reassuring percentage.

### Critical invariants

- Every consequential claim names exact resource, input, output, code, configuration, schema, policy, and identity versions or records why a version is unavailable.
- Human actor, authenticated principal, effective subject, service/workload identity, session, delegation, and credential are distinct fields.
- Allow, deny, failure, override, break-glass, administrative read, export, policy change, evidence access, and evidence deletion are all auditable where relevant.
- Event, record, and observed times remain distinct; clock source, precision, skew, and uncertainty are recorded or bounded.
- Correlation preserves causal context across request, job, query, transformation, authorization, output, and downstream delivery without claiming a total global order.
- Retries and duplicates preserve stable event/action identity; deduplication never silently removes genuinely repeated actions.
- Schemas and semantics are versioned. Parsers preserve unknown fields and original evidence while producing normalized views.
- Evidence is append-oriented, least-privilege, encrypted, minimized, access-logged, retained under policy, and isolated from the actor or system it may implicate.
- Hashes, signatures, chains, trees, timestamps, immutable storage, and anchors are described only for the properties and threat boundaries they actually supply.
- Integrity verification covers canonicalization, key identity/status, protected checkpoints, algorithm agility, gaps, and verifier independence.
- Capture completeness is reconciled against independent eligible-action counts, sequence/range continuity, source health, and downstream receipt—not inferred from collector success alone.
- Provenance relations preserve derivation meaning; mere co-occurrence or common job membership does not prove one entity influenced another.
- Redaction or de-identification preserves event identity, relationships, and verification evidence while minimizing sensitive values.
- Evidence lifecycle reconciles audit retention, legal holds, deletion duties, backup expiry, key retention, and investigation needs through authorized policy.
- Every investigation records query, export, transformation, analyst, tool/version, digest, time, handoff, and disposition so derived evidence has provenance too.
- Control objectives map to explicit evidence, expected population, owner, retrieval test, exception route, and expiry; “logs enabled” is not a control conclusion.
- Auditability is continuously tested with missing, duplicate, late, reordered, forged, redacted, schema-changed, clock-skewed, and compromised-producer cases.

### Common failures

Common failures include recording only the login identity while a service acts for a user; logging a mutable table name without snapshot/version; recording success but not deny or override; losing the policy version and reason; overwriting events in place; trusting producer timestamps as global order; deduplicating two real actions; silently dropping unknown schema fields; centralizing logs under the same administrator they may implicate; exposing secrets and query results in logs; hashing noncanonical JSON; storing a chain head beside the chain with identical privileges; assuming a signature proves truthful capture; reporting 100% coverage without a denominator; drawing derivation edges from temporal proximity; retaining audit evidence forever; and exporting investigation data without a chain of custody.

### Compact example

A scheduled workload uses service identity `transformer`, assumes a role for data steward `s17`, reads input snapshot `orders@184`, executes code digest `sha256:...` with configuration `cfg@12`, receives policy decision `allow` from `policy@31`, and generates `revenue@52`. A useful evidence bundle links the activity to both agents and their delegation, exact inputs and output, run/correlation IDs, event and observed times, decision reason, schema version, and prior digest. An independently protected checkpoint detects later record rewriting. It still cannot prove that the source emitted every read or that steward `s17` intended the action; coverage reconciliation and identity controls address those different claims.

### Connections

[DE-049](049-run-metadata-and-operational-state.md) supplies execution identity, [DE-066](066-time-travel-and-reproducible-reads.md) supplies reproducible data versions, [DE-076](076-data-contracts.md) supplies evidence obligations, [DE-078](078-data-incident-detection-and-triage.md) consumes evidence during incidents, [DE-079](079-root-cause-analysis-with-lineage.md) combines causality and lineage, [DE-081](081-technical-operational-and-business-metadata.md) governs descriptive context, [DE-082](082-dataset-and-column-lineage.md) covers dependency graphs, [DE-084](084-ownership-and-stewardship.md) assigns accountability, and [DE-085](085-classification-and-sensitive-data.md), [DE-086](086-access-control-for-analytical-data.md), [DE-087](087-masking-tokenization-and-de-identification.md), and [DE-088](088-retention-and-deletion.md) constrain evidence protection and lifecycle. [DE-090](../ROADMAP.md) next examines data product thinking.

## Governing Question

An organization often says “the logs show what happened.” That statement compresses several independent questions. Was the relevant event emitted? Did it identify the effective human and workload? Did it name immutable input and output versions? Was its timestamp trustworthy enough for the claimed order? Could an administrator alter it? Was its meaning preserved across schema changes? Can reviewers retrieve it within the promised interval? Does it expose more sensitive data than the control needs?

Auditability is therefore a capability, not a file type. It starts with claims and control objectives, derives an evidence contract, captures evidence at authoritative enforcement and execution points, protects and reconciles it, and repeatedly demonstrates retrieval and interpretation. A verbose log stream can be unauditable if it lacks identity, version, reason, coverage, or preservation. A smaller structured evidence set can be stronger if it is deliberately tied to decisions and effects.

Provenance answers a related but not identical question: what people, systems, activities, and prior entities influenced a result? It can support reproducibility, quality assessment, incident analysis, accountability, intellectual credit, and governance. Lineage provides dependency paths, but full provenance also includes responsibility, delegation, generation, usage, time, and provenance of the evidence itself.

The governing problem is to build scoped arguments. State the proposition—such as “only approved code and policy produced this published dataset”—then identify the population, evidence, integrity and completeness assumptions, queries, exceptions, and lifecycle. Do not upgrade a technical artifact into a legal conclusion. Qualified audit, legal, privacy, security, records, and domain authorities determine which controls and retention duties apply; engineering makes their claims falsifiable and retrievable.

## Why This Matters

Data products influence payments, access, safety, reporting, research, and machine decisions. When an output is challenged, teams must reconstruct more than code. They need the input versions, policy and configuration, actor and delegation, execution environment, time relationships, exceptions, and exact output. Without them, a successful rerun may use different data and still appear to validate the original result.

Audit evidence is also a security boundary. A privileged analyst can export a sensitive table; an administrator can change access policy; a service can assume another role; a failed authorization may reveal attack attempts. If evidence lives only on the implicated system under the same privileges, an attacker or operator can erase the history needed to investigate. Conversely, indiscriminate logging can become a concentrated store of credentials, personal data, query text, tokens, and business secrets.

Operationally, evidence reduces recovery time. A run record linked to lineage can bound affected outputs. A decision receipt can explain why an access request was allowed. Sequence gaps can reveal collector failure. Schema versions can distinguish a real behavioral change from a parser defect. These are engineered diagnostic properties, not paperwork added after delivery.

Auditability also disciplines claims. “Tamper-proof,” “immutable,” “complete,” and “nonrepudiable” are usually too broad. Storage may prevent ordinary overwrite while allowing privileged lifecycle deletion. A signature establishes possession of a key, not the truth of the signed assertion. A hash chain can expose interior mutation only relative to a checkpoint. Precise claims let reviewers reason about residual risk instead of relying on security adjectives.

## Prerequisites and Retrieval

Retrieve control objectives and obligations: relevant policies, contracts, regulatory interpretations, security and privacy controls, records schedules, litigation or preservation holds, incident needs, evidence consumers, assurance level, retrieval deadlines, and authorized exception owners.

Retrieve identity context: human actor, authenticated principal, effective subject, service account, workload identity, device/session, credential/key ID, authentication method, role assumption, delegation chain, tenant, environment, source network, break-glass state, and identity lifecycle events. Determine which system is authoritative for each field.

Retrieve object and execution identity: stable dataset/table/file/topic/model/report IDs; schema and contract versions; snapshot, commit, partition, object version, and row/batch identifiers; query/job/run/request/trace IDs; code artifact digest; dependency lock; container or runtime image; configuration and feature flags; policy bundle and rule versions; and output publication/version IDs.

Retrieve time semantics: event, source-record, receive/observed, processing, commit, and publication times; timezone; monotonic versus wall clock; synchronization source; precision; uncertainty; known clock offset; sequence numbers; and causal correlation. A timestamp without clock provenance is weaker than it appears.

Retrieve capture architecture: authoritative policy decision points, policy enforcement points, orchestrators, query engines, stores, gateways, catalogs, lineage emitters, identity providers, collectors, queues, dead-letter paths, normalization pipelines, evidence stores, indexes, archives, backup paths, anchors, verifiers, and consumer queries.

Retrieve threat and trust boundaries: producer compromise, privileged administrator, collector outage, network partition, replay, forged identity, stolen signing key, canonicalization mismatch, timestamp manipulation, sequence truncation, storage deletion, evidence exfiltration, cross-tenant disclosure, and collusion across roles.

Retrieve lifecycle and operations: classification, minimization/redaction, access policy, evidence-access audit, signing and encryption keys, key rotation/revocation, retention, holds, deletion, backup, restore, export, investigation workspaces, chain-of-custody forms, schema registry, parser versions, health metrics, gap alerts, sampling rules, and verification drills.

Separate the following pairs: auditability from observability; evidence from conclusion; entity from its mutable locator; event from record; actor from credential; authentication from intent; association from derivation; event time from observed time; total order from partial order; append-only from immutable; integrity from truth; inclusion from completeness; signature validity from signer authorization; retention from accessibility; redaction from evidence destruction; and a generated audit report from an independent external audit.

Build an evidence requirement table before choosing technology:

| Control claim | Eligible population | Required fields and relations | Independent reconciliation | Protection and lifecycle |
|---|---|---|---|---|
| Published output used approved inputs | publication events | output version, activity, input versions, code/config/policy | catalog publications versus provenance graph | signed checkpoint, governed retention |
| Sensitive export was authorized | export attempts | actor, effective subject, workload, object, decision/reason, outcome | gateway requests versus store reads | isolated access, minimized parameters |
| Administrators cannot silently rewrite history | protected event ranges | canonical records, sequence, digest, checkpoint/key | independent anchor and verifier | separation of duties, key rotation |
| Required actions are captured | all eligible actions | stable event/action IDs and outcome | enforcement-point counts versus received events | gap alert, retry/dead-letter, expiry |
| Investigation evidence remained controlled | evidence items and derivatives | collector, handler, transfer, digest, query/tool | custody inventory versus handoffs | case access, hold, disposition |

Write a falsifiable claim: “For all production publish actions in UTC day D, catalog C supplies the eligible denominator; enforcement point P emits schema S4 with actor/workload/delegation, exact input/output snapshots, code/config/policy versions, decision and reason; collector K acknowledges stable IDs; reconciliation R reports duplicates, late arrivals and gaps; canonical events are chained, signed in hourly Merkle checkpoints and anchored to independently administered store A; verifier V checks chain, key status, checkpoint consistency and retrieval; exceptions E remain named; records are minimized, access-logged, held or deleted under policy L.”

## Learning Objectives

After completing this module, you should be able to:

1. distinguish auditability, audit events, provenance, lineage, observability, evidence, and assurance conclusions;
2. model versioned entities, activities, agents, usage, generation, derivation, attribution, association, and delegation;
3. design an evidence schema that preserves actor, effective subject, workload, action, object versions, policy, outcome, reason, time, and correlation;
4. reason about event/record/observed time, uncertainty, causal partial order, retries, duplicates, late events, and schema evolution;
5. evaluate append-only storage, access isolation, digital signatures, hash chains, Merkle commitments, trusted timestamps, and independent anchors against explicit threats;
6. explain why cryptographic integrity does not prove truthful capture, identity intent, semantic correctness, or completeness;
7. define and test completeness using eligible populations, independent reconciliation, sequence continuity, source health, and downstream acknowledgments;
8. protect and minimize audit evidence while meeting retention, hold, deletion, backup, and investigation obligations;
9. build reproducibility and chain-of-custody workflows whose derived evidence has its own provenance; and
10. map control objectives to evidence contracts, operational checks, metrics, exceptions, and bounded conclusions.

## Core Exposition

### Begin with claims and evidence contracts

Start with the proposition a reviewer must evaluate. “Every privileged read is authorized” requires a population of privileged read attempts, authorization decisions, enforcement outcomes, identities, objects, policy versions, and reconciliation. “This report is reproducible” requires exact source snapshots, code and configuration, environment, random seeds where applicable, and output identity. The word “every” immediately creates a completeness requirement.

An evidence contract gives each event type a durable name, owner, purpose, eligible trigger, required and prohibited fields, schema version, identifiers, time semantics, ordering guarantees, delivery behavior, classification, retention, access policy, integrity controls, reconciliation source, latency objective, and change process. Treat it like a data contract with stronger adversarial assumptions.

Capture at authoritative decision and enforcement points. Application text such as “user exported data” is weak if the gateway made the authorization decision and the warehouse performed the read. Link request, decision, enforcement, execution, and delivery with stable identifiers. Preserve denies and failures because omission biases the record and hides attempted misuse.

### Model provenance as versioned responsibility and influence

The W3C PROV model provides domain-neutral primitives. Entities have fixed aspects within a description; activities occur over time and use or generate entities; agents bear responsibility. Relations distinguish an activity using an entity, an entity being generated by an activity, an output being derived from an input, an entity being attributed to an agent, an activity being associated with an agent, and an agent acting on behalf of another.

These distinctions prevent common inference errors. If a job reads two tables but only one influences an output branch, usage alone does not automatically prove derivation from both. If a scheduler launches a workload for an analyst, workload identity, analyst, scheduler, and delegation play different roles. If a table mutates, model snapshots or commits as distinct entities; a mutable URI is only a locator.

Provenance itself needs provenance. Record which collector observed a relation, which adapter normalized it, which schema and rule inferred it, and whether it was declared, statically analyzed, observed at runtime, or manually asserted. Confidence or evidence type should not be silently converted into a certain edge.

### Preserve identity, policy, and decision context

Record the authenticated principal and the effective subject separately. A workload may authenticate with a service certificate, assume a role, act for a user, and access a tenant's data. The credential identifies a mechanism, not necessarily the accountable human. Preserve session, delegation, authentication strength, workload deployment, and role/policy context needed to reconstruct the chain.

For governance and access decisions, emit a decision receipt. It names the request and relevant attributes, policy bundle/rule/version, decision, reason or matched rule, enforcement point, actor/workload/delegation, resource version, event and observed times, outcome, correlation, and override/break-glass state. Minimize sensitive attributes: record classifications, stable protected references, or approved digests when full values are unnecessary.

Policy change is itself consequential. Audit who proposed, reviewed, approved, deployed, rolled back, or bypassed a rule, with before/after versions and test evidence. Otherwise an access event can cite `policy@31` while nobody can explain how that policy came to exist.

### Treat distributed time as evidence with uncertainty

One wall-clock timestamp cannot reliably order a distributed system. Event time expresses the producer's assertion; record time may capture local persistence; observed time captures arrival at another system. Clock synchronization reduces error but does not create a perfect global clock. Store timezone/offset, precision, clock source, and known uncertainty when order matters.

Use causal identifiers and local sequence where available. If request A causes authorization B, job C, and publication D, explicit links establish the relevant order even if clocks overlap. A trace/span model can carry trace ID, span ID, parent ID, flags, and observed time; it helps correlation but does not prove that all causal relationships were instrumented.

Late and reordered events are normal. Define watermark and correction behavior for audit queries, keep original event and observed times, and mark when reports are provisional. Never rewrite the original timestamp simply to fit arrival order. Investigations should be able to distinguish the event history from the warehouse's later normalized view.

### Engineer delivery, duplicate, and schema semantics

Collectors fail, queues retry, partitions reorder, and producers restart. Give each logical emission a stable event ID and each underlying action/request a stable action ID. Two deliveries with one event ID are duplicates; two different events for repeated reads may be legitimate. Deduplication must be scoped by producer identity and ID domain, not by similar message text.

Avoid “exactly once” claims unless the complete transactional boundary is defined and demonstrated. At-least-once delivery plus idempotent ingestion, unique identity, explicit duplicate metrics, and reconciliation is often the honest design. An outbox can couple a domain change and pending evidence record in one database transaction, but publishing and downstream storage still require retry and deduplication.

Version schemas and semantics. Producers should not reuse a field with a new meaning. Collectors preserve raw canonical evidence or an integrity-verifiable original representation, retain unknown fields, quarantine invalid records, and emit normalized derivatives with transformation provenance. Parser upgrades should be replay-tested against historical versions.

### Protect evidence by threat boundary

Append-only usually means the normal API exposes additions but no updates; privileged operators, lifecycle services, storage administrators, or compromised credentials may still alter or remove data. Immutable or WORM controls are also bounded by configured retention, governance mode, provider semantics, keys, administrators, and physical system. State who is prevented from doing what, for how long.

Separate evidence production, administration, review, and destruction where consequence warrants. Forward records across an administrative boundary promptly; restrict producer permissions to append; use least-privilege reader roles; audit evidence access; require dual authorization for exceptional deletion; encrypt in transit and at rest; and monitor configuration or retention changes. Independent copies increase resilience but also privacy and lifecycle scope.

Cryptographic controls complement these boundaries. Canonicalize deterministic fields, bind sequence and context, sign with identified protected keys, publish or independently preserve checkpoints, rotate keys with verifiable continuity, record revocation and compromise intervals, and test verification from archived material. Algorithm and format agility matter over long retention.

### Interpret cryptographic evidence precisely

A digest binds bytes under collision-resistance assumptions. A digital signature supports the claim that a holder of a private key signed particular bytes; certificate/key status and authorization at the relevant time still matter. A trusted timestamp protocol can bind a digest to evidence from a time-stamping authority, but it does not validate the event's semantic content.

A hash chain makes each covered record depend on its predecessor. If an attacker can rewrite every record and the unprotected chain head, the chain adds little. Protect checkpoints outside the writer's control. A Merkle tree commits to a set or ordered log and permits compact inclusion proofs; consistency proofs can show append-only evolution under a specified construction. Inclusion proves membership in a committed structure, not that the structure contains all required real-world events.

Cryptography cannot repair upstream lies. A compromised producer can sign a fabricated event or omit an event. A stolen key weakens attribution. A bad canonicalizer can cause verifier disagreement. A chain with an unanchored tail can be truncated. Pair integrity with independent observation, enforcement, eligible-population reconciliation, protected identity, source health, and key incident procedures.

### Measure completeness rather than assuming it

Completeness needs a population. For a query gateway, eligible request IDs may come from an independently controlled admission counter or transaction journal. For data publication, the catalog may enumerate committed versions. For policy decisions, enforcement actions should reconcile with decision receipts. If the denominator depends on the same failing emitter as the numerator, coverage can misleadingly remain 100%.

Check source sequence gaps, expected partitions, heartbeats, producer versions, collector acknowledgments, queue lag, dead letters, invalid/quarantined records, duplicate IDs, late arrivals, parse loss, index lag, archive retrieval, and anchor cadence. Reconciliation should explain $eligible=observed+knownMissing+excluded$ for a defined scope and time, with each exclusion governed.

Sampling can test quality but cannot prove universal capture unless the statistical claim and selection design support it. A zero-error sample is not proof of zero missing events. Report known gaps, unknown denominator, stale sources, and late windows explicitly. Auditability improves when absence becomes a first-class state rather than disappearing from dashboards.

### Minimize and govern the evidence lifecycle

Logs and provenance can contain personal data, secrets, SQL literals, row values, tokens, paths, customer identifiers, or security topology. Collect only what the control requires. Prefer stable pseudonymous references, classification labels, parameter names, approved one-way or keyed references, and separately protected lookups over raw payloads. Never log credentials, private keys, bearer tokens, or sensitive result bodies merely for convenience.

Redaction must be deterministic enough to preserve event identity and correlation without creating linkability beyond purpose. Keep redaction policy/version and transformation provenance. If a sensitive value is accidentally captured, incident handling may require access restriction and governed remediation; silently editing a protected record can destroy integrity. A correction or redaction event plus preserved restricted original may be appropriate when policy permits.

Retention balances investigation, assurance, privacy, records, litigation, and cost. Apply [DE-088](088-retention-and-deletion.md): exact trigger, minimum/maximum, holds, backups, keys, deletion receipts, and restore behavior. Integrity keys or checkpoints may need a different lifecycle from event content. Deleting the verification key too early can make retained evidence unverifiable; retaining identity maps too long can defeat minimization.

### Support investigations and reproducibility

On collection, identify the source, collector, method, scope, time, operator, tool/version, and digest. Preserve original evidence read-only; perform parsing, filtering, joining, timezone conversion, and visualization as derived activities with their own inputs, outputs, code/configuration, and operators. Each export or handoff records sender, recipient, authority, purpose, time, digest, protection, and acknowledgment.

Chain of custody does not magically make evidence true. It supports an argument that the item presented is the item collected and explains subsequent handling. Investigators still assess source reliability, clock quality, completeness, alternative explanations, and authorization. Limit case access and record investigator queries because investigation stores often aggregate especially sensitive evidence.

For reproducibility, package or reference immutable input snapshots, environment and dependency locks, code and configuration digests, policy versions, seeds, feature definitions, run parameters, and output digests. Reproducibility can be limited by nondeterministic hardware, external services, deleted inputs, changing dependencies, or privacy constraints; record these boundaries instead of claiming exact replay.

### Turn control objectives into tested operations

For each control, define owner, population, evidence fields/relations, source, integrity boundary, completeness reconciliation, query, expected outcome, exception, retention, and test cadence. A control such as “privileged exports require approval” should be executable as a join among eligible export actions, decisions, approvals, results, and exceptions—not a screenshot that logging is enabled.

Exercise failure paths. Disable a producer, delay one partition, duplicate a batch, corrupt one record, reorder events, rotate or revoke a key, change a schema, skew a clock, compromise an emitter in a tabletop, redact a protected field, truncate an unanchored tail, restore an archive, and expire evidence. Confirm alerts, reconciliation, verification, retrieval, escalation, and bounded conclusions.

Useful measures include eligible and observed event counts; known missing and denominator-unknown scopes; capture and indexing latency; duplicate, late, invalid, quarantined, and dead-letter rates; sequence gaps; producer/collector health; unsigned or unverifiable events; checkpoint/anchor age; key status; schema/parser coverage; provenance edge coverage by evidence type; retrieval success and time; evidence-access anomalies; retention exceptions; and failed restore/verifier drills. A single “logging healthy” indicator hides too much.

## Definitions and Notation

Let $E$, $A$, and $R$ denote versioned entities, activities, and agents. Let $G=(V,L)$ be a directed labeled provenance graph with $V=E\cup A\cup R$. A relation $used(a,e)$ says activity $a$ used entity $e$; $generated(e,a)$ says $e$ was generated by $a$; $derived(e_2,e_1)$ says $e_2$ was influenced through transformation or construction from $e_1$. Association and delegation attach responsibility without being conflated with derivation.

Let $Q_W$ be the independently established set of required eligible occurrences in window $W$, $O_W$ the required occurrences with valid retrievable evidence, $M_W=Q_W\setminus O_W$ known missing occurrences, and $X_W$ governed exclusions. A reconciliation invariant is

$$
Q_W=O_W\mathbin{\dot\cup}M_W\mathbin{\dot\cup}X_W,
$$

where the dotted union requires disjoint classifications. When $Q_W$ is known, $coverage(W)=|O_W|/|Q_W\setminus X_W|$. When it is unknown, the ratio is undefined rather than zero or one.

For event $e_i$, deterministic canonicalization $C$ and hash $H$, define genesis $h_0$ from explicit domain/version context and

$$
h_i=H(domain\parallel schema_i\parallel h_{i-1}\parallel C(e_i)).
$$

An anchor $a_k=Protect(k,h_k,t_k,keyState_k)$ places checkpoint $h_k$ across a stated trust boundary. Verification $Verify(e_{1:k},a_k)$ recomputes encodings/digests and validates the protection evidence. Its conclusion is limited to the represented range and assumptions.

For timestamps, $t_e(e)$ is asserted event time, $t_r(e)$ local record time, and $t_o(e)$ collector-observed time. If known clock uncertainty is $\epsilon_e$, the occurrence interval is $[t_e-\epsilon_e,t_e+\epsilon_e]$. Nonoverlapping intervals can support order; overlapping intervals generally cannot. Explicit causal relation $x\rightarrow y$ supplies a partial order independent of a global wall clock.

## Mechanisms, Invariants, or Proof Structure

### Evidence lifecycle mechanism

1. State the control or reconstruction claim, scope, population, consumer, assurance need, and qualified authority.
2. Model exact entities, activities, agents, responsibility/delegation, decisions, effects, identifiers, versions, time semantics, and prohibited sensitive fields.
3. Define an evidence contract with schema/version, trigger, source, delivery, duplicate/late behavior, classification, integrity, reconciliation, retention, and change ownership.
4. Capture at authoritative decision and enforcement points; link request, decision, execution, input/output, and publication with stable correlation.
5. Deliver through observable retryable paths; preserve event and action identities; quarantine invalid/unknown versions; retain transformation provenance.
6. Canonicalize and protect events; establish sequence or Merkle checkpoints, signatures, timestamps, and independent anchors according to threat model.
7. Reconcile eligible populations, source sequences/health, acknowledgments, queues, gaps, duplicates, late events, parser outcomes, and retrieval indexes.
8. Store evidence with least privilege, separation of duties, encryption, access audit, retention/hold/deletion, backups, key lifecycle, and verifier availability.
9. Query and derive evidence reproducibly; preserve original items and record every normalization, investigation, export, handoff, and conclusion boundary.
10. Test capture failure, producer compromise, timing, schema, cryptographic, lifecycle, and recovery cases; measure debt and remediate named gaps.

### Integrity and completeness claims

**Conditional integrity claim.** Suppose $C$ is deterministic, $H$ remains collision resistant, the verifier has an authentic protected anchor $a_k$, the protection key and process were trustworthy for the claimed time, and every intended record $e_1,\ldots,e_k$ is supplied. Then modification, reordering, or deletion within the anchored prefix causes recomputation to disagree except with negligible hash-collision probability or compromise of an assumption.

**Proof sketch.** Each $h_i$ binds $C(e_i)$ and $h_{i-1}$. A changed record changes its digest and every successor. Reordering changes predecessor inputs. Interior deletion connects records through a predecessor digest different from the recorded one. The authentic anchor prevents replacing $h_k$ without defeating its protection. This argument says nothing about truthful original content or records omitted before commitment.

**Conditional completeness claim.** If independent source $Q_W$ exactly enumerates required eligible occurrences, exclusions $X_W$ are authorized and disjoint, and every observed record maps one-to-one to a member of $Q_W$, then $M_W=\varnothing$ establishes complete observed coverage for the defined window and contract.

**Proof sketch.** The disjoint reconciliation partitions the eligible population. If no eligible member is missing and exclusions are removed from the required denominator, each required occurrence has mapped evidence. The claim fails if the denominator shares the emitter's blind spot, mappings collapse repeated actions, or evidence is present but invalid/unretrievable.

### Executable hash-chain illustration

This deterministic example canonicalizes three constrained ASCII JSON fixtures, chains them, verifies the chain, then changes one protected event. Its tiny encoder is deliberately limited to the fixture's already validated string keys and values; production code must use a specified, tested canonicalization standard and general-purpose encoder. The example illustrates mutation detection only. It does not prove that events were true or complete, and production designs still need protected anchors, keys, trusted time/context, domain separation, lifecycle, and independent reconciliation.

<!-- bijux-verify: {"id":"audit-event-hash-chain","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"events=3\nchain_valid=true\ntampered_chain_valid=false\nhash_chain_proves_event_truth=false\n","stderr":""}} -->
```python
import hashlib


def canonical(record: dict[str, str]) -> bytes:
    fields = [f'"{key}":"{record[key]}"' for key in sorted(record)]
    return ("{" + ",".join(fields) + "}").encode()


def build_chain(events: list[dict[str, str]]) -> list[str]:
    previous = bytes(32)
    chain = []
    for event in events:
        digest = hashlib.sha256(previous + canonical(event)).digest()
        chain.append(digest.hex())
        previous = digest
    return chain


def verify(events: list[dict[str, str]], expected: list[str]) -> bool:
    return build_chain(events) == expected


events = [
    {"id": "e1", "action": "read", "object": "orders@184"},
    {"id": "e2", "action": "transform", "object": "run@7"},
    {"id": "e3", "action": "publish", "object": "revenue@52"},
]
chain = build_chain(events)
tampered = [dict(event) for event in events]
tampered[1]["action"] = "delete"

print(f"events={len(events)}")
print(f"chain_valid={verify(events, chain)}".lower())
print(f"tampered_chain_valid={verify(tampered, chain)}".lower())
print("hash_chain_proves_event_truth=false")
```

## Alternatives and Trade-Offs

1. **Central evidence service versus domain-owned capture.** Centralization standardizes protection and querying but can lose domain semantics and become a high-value bottleneck. Domain capture preserves context but needs enforceable contracts and independent collection.
2. **Application logging versus enforcement-point evidence.** Applications explain intent; gateways, policy engines, stores, and orchestrators observe decisions and effects. Link both for consequential flows rather than choosing one uncritically.
3. **Full payload versus minimized references.** Payloads simplify reconstruction but amplify privacy and secret exposure. Protected stable references and classified parameters usually support controls with lower risk.
4. **Human-readable text versus structured events.** Text helps local diagnosis; structured versioned schemas support stable joins and validation. A structured envelope can include a bounded human message without making it authoritative.
5. **One global schema versus typed event contracts.** A global envelope improves interoperability; one enormous schema encourages vague optional fields. Use a stable envelope plus owned typed payloads and semantic versions.
6. **Wall-clock sorting versus causal order.** Time sorting is convenient but unsafe under skew. Parent/correlation links and local sequences better express causality, while synchronized clocks bound cross-system analysis.
7. **At-least-once versus attempted exactly-once delivery.** At-least-once creates duplicates but makes loss and retry visible. Stronger transactional coupling can reduce ambiguity within a narrow boundary but should not become an end-to-end slogan.
8. **Hash chain versus Merkle tree.** A chain is simple and order-sensitive but gives linear verification. Merkle structures provide compact inclusion and consistency proofs at greater implementation and canonical-order complexity.
9. **Local checkpoint versus independent anchor.** Local checkpoints are fast but share compromise risk. Independent anchoring strengthens rewrite detection while adding latency, cost, availability, and lifecycle dependencies.
10. **Producer signatures versus collector signatures.** Producer signatures bind origin more directly but expand key management to every emitter. Collector signatures simplify custody after receipt but cannot independently prove producer origin.
11. **Immutable hot store versus tiered retention.** Long hot retention speeds investigation but raises exposure and cost. Tiered protected archives reduce cost but require tested retrieval, index, verifier, and key availability.
12. **Complete capture versus risk-based sampling.** Complete capture supports event-level reconstruction but can be expensive and sensitive. Sampling can test trends, not substantiate universal claims unless the assurance objective is explicitly statistical.
13. **Automatic lineage versus declared lineage.** Runtime and static extraction scale but can miss dynamic or semantic influence. Declared lineage carries intent but may drift. Preserve evidence type and reconcile multiple sources.
14. **Direct identifiers versus pseudonymous correlation.** Direct identity eases investigation but concentrates personal data. Scoped keyed references reduce exposure while requiring protected resolution and rotation strategy.
15. **Long audit retention versus minimization and deletion.** Long retention helps historical inquiries; it also increases breach and privacy exposure. Use claim-specific periods, holds, bounded archives, and documented deletion verification.

## Failure Modes and Misconceptions

1. **“Observability equals auditability.”** Diagnostic telemetry may be sampled, mutable, unauthenticated, short-lived, or missing policy and effective identity.
2. **“The event is the fact.”** It is an assertion produced by a system with failure and compromise modes.
3. **“More logs mean stronger evidence.”** Volume without stable semantics, attribution, versions, reconciliation, or retrieval can obscure gaps.
4. **“The username identifies the actor.”** Services, assumed roles, delegation, shared credentials, and compromised sessions require richer identity context.
5. **“Authentication proves intent.”** It supports credential use under stated controls, not human intent or freedom from compromise.
6. **“A table name identifies the data.”** Mutable names need snapshot, commit, object, or generation versions.
7. **“Job membership proves derivation.”** Usage and temporal proximity do not necessarily mean an input influenced an output.
8. **“All timestamps define one order.”** Distributed clocks skew; causal links and uncertainty matter.
9. **“Ingest time can replace event time.”** It describes observation and latency, not when the source occurrence happened.
10. **“Duplicate-looking events are safe to discard.”** Two genuine repeated actions can have identical fields; stable identity is required.
11. **“A successful collector means capture is complete.”** Producers, routes, schemas, partitions, and indexes can fail independently.
12. **“The event count is its own denominator.”** The same blind spot can reduce both apparent expectation and observation.
13. **“Append-only means immutable.”** Privileged deletion, retention changes, storage replacement, or account compromise may remain possible.
14. **“A hash prevents tampering.”** It detects byte changes only when a trusted expected digest exists.
15. **“A valid chain proves no omission.”** Pre-commit omissions and unanchored tail truncation can remain invisible.
16. **“A signature proves truth.”** It proves a key signed bytes under cryptographic assumptions; the signer or producer can be wrong or malicious.
17. **“A timestamp proves occurrence time.”** It may bind bytes to authority time, not validate the embedded event-time assertion.
18. **“Merkle inclusion proves completeness.”** It proves membership in a committed tree; population completeness needs independent reconciliation.
19. **“One signing key forever simplifies audit.”** It increases compromise blast radius and ignores algorithm, revocation, and retention lifecycles.
20. **“Normalization may replace originals.”** Parser or mapping bugs then rewrite the only evidence; derived views need their own provenance.
21. **“Unknown schema fields can be dropped.”** They may carry future or domain-specific evidence and their loss becomes silent.
22. **“Deny events are noise.”** They reveal policy behavior, failed access, probing, and attempted abuse.
23. **“Evidence administrators need unrestricted access.”** Separation, minimization, dual control, and access audit should constrain them too.
24. **“Logging sensitive payloads is necessary for investigations.”** Stable references and controlled source retrieval often provide sufficient evidence with less exposure.
25. **“Redaction leaves integrity unchanged.”** Byte changes require explicit derived records, policy provenance, and renewed commitments.
26. **“Audit data must be retained forever.”** It remains subject to purpose, policy, hold, security, privacy, backup, and deletion constraints.
27. **“A dashboard screenshot is durable evidence.”** It omits query, data version, transformation, filters, time, and reviewer provenance.
28. **“Chain of custody proves the source was correct.”** It documents handling, not source truth or completeness.
29. **“A reproducible output must be correct.”** Deterministic replay can reproduce a consistently wrong algorithm or biased input.
30. **“Passing one audit proves continuous control.”** Systems, schemas, keys, policies, populations, and threats change; evidence must be continuously tested.

## Worked Examples

### Example 1

**Situation.** An analyst uses single sign-on, an orchestration service, and an assumed warehouse role to export classified records.

**Reasoning.** The login, session, analyst, orchestrator workload, service credential, assumed role, tenant, export request, policy decision, exact snapshot, query digest, result object, and delivery outcome are linked. The record does not equate the service credential with the human or store raw result rows.

**Conclusion.** Attribution needs the delegation chain and enforcement effect, not one username field.

### Example 2

**Situation.** Two services timestamp events 90 milliseconds apart, but each clock has possible error of 150 milliseconds.

**Reasoning.** Their occurrence intervals overlap, so wall clocks cannot establish order. A request parent ID proves the first response caused the second request; observed times explain collection order without replacing source assertions.

**Conclusion.** Causal evidence can establish relevant order when synchronized clocks cannot.

### Example 3

**Situation.** A queue retries an export event after an acknowledgment timeout, and the same user performs a second identical export.

**Reasoning.** The retry shares event ID `ev-9`; the second action has event ID `ev-10` and a distinct action/request ID. Ingestion deduplicates only `ev-9` deliveries and retains both actions. Payload hashing alone would have collapsed legitimate behavior.

**Conclusion.** Event identity separates transport duplicates from repeated real actions.

### Example 4

**Situation.** A hash-chained audit file validates, but an attacker controlled the producer for an hour.

**Reasoning.** The chain supports no-after-commit modification within anchored ranges. The compromised producer could omit reads or emit false actors before hashing. Gateway counters, store access evidence, workload attestation, source health, and incident-key intervals are needed to bound the hour.

**Conclusion.** Integrity of assertions is not truth or completeness of occurrences.

### Example 5

**Situation.** The audit dashboard reports 100% receipt because all 9,700 emitted records arrived; an independent gateway journal lists 10,000 eligible requests.

**Reasoning.** Reconciliation finds 300 missing events. Partition and producer-version analysis localizes a failed emitter deployment. The dashboard's original denominator shared the emitter's blind spot and was invalid for the universal claim.

**Conclusion.** Completeness requires an independently established eligible population.

### Example 6

**Situation.** A lineage system observes that a job read customer and holiday tables before producing a score table.

**Reasoning.** Runtime usage edges are recorded for both. Branch-level code evidence shows only customer data influenced this output version; holiday data fed an unused diagnostic branch. The system records evidence type instead of inferring derivation from every read.

**Conclusion.** Usage is necessary context but is not automatically derivation.

### Example 7

**Situation.** A schema upgrade renames `principal` to `authenticated_principal` and adds `effective_subject`.

**Reasoning.** The producer emits schema version 4. The collector preserves version-3 originals, maps the old field only to authenticated principal, leaves effective subject unknown, and records normalization version. It does not manufacture equivalence between the old principal and a delegated user.

**Conclusion.** Honest unknowns preserve meaning better than convenient backfill.

### Example 8

**Situation.** An investigator exports 400 events, converts timezones, filters them, and produces a timeline.

**Reasoning.** Collection records source/range/tool and digests. The export, conversion, filter, and timeline are versioned activities linked to immutable inputs, code/configuration, analyst, authorization, and outputs. Each handoff is acknowledged and case access is logged.

**Conclusion.** Derived investigative evidence needs provenance and custody just like source evidence.

### Example 9

**Situation.** A delete request covers a person whose identity appears in seven-year audit records.

**Reasoning.** Qualified policy owners resolve the deletion request, audit purpose, applicable minimum/maximum, and any hold. Active operational data is handled separately; audit records are minimized or pseudonymized where allowed, tightly restricted, expired on schedule, and remain verifiable through content-independent checkpoints and governed key retention.

**Conclusion.** Auditability does not authorize indefinite identifiable retention or silent evidence rewriting.

### Example 10

**Situation.** A quarterly control requires evidence that every production dataset publication used approved code and policy.

**Reasoning.** Catalog commits define the population. Each commit joins to run, input snapshots, artifact digest, configuration, policy decision, reviewer/exception, output digest, and anchored receipt. Missing joins fail the control population; samples then assess semantic correctness without replacing full coverage reconciliation.

**Conclusion.** A control becomes auditable when its population, joins, evidence, exceptions, and conclusion bounds are executable.

## Cross-Program Connections

- [DE-049](049-run-metadata-and-operational-state.md) provides run IDs, attempts, checkpoints, outcomes, and operational state that anchor activity evidence.
- [DE-066](066-time-travel-and-reproducible-reads.md) supplies snapshot identity and versioned reads required for reproducibility claims.
- [DE-076](076-data-contracts.md) treats evidence schemas, delivery, semantic versions, and ownership as governed interfaces.
- [DE-078](078-data-incident-detection-and-triage.md) consumes attributable, protected, timely evidence and identifies missing telemetry as an incident constraint.
- [DE-079](079-root-cause-analysis-with-lineage.md) uses provenance and time-bounded causal evidence to narrow affected paths without confusing correlation with cause.
- [DE-081](081-technical-operational-and-business-metadata.md) governs identifiers, semantics, classifications, ownership, and versions used by evidence records.
- [DE-082](082-dataset-and-column-lineage.md) develops dependency graphs; this chapter adds agent responsibility, evidence type, integrity, custody, and completeness.
- [DE-084](084-ownership-and-stewardship.md) assigns accountable control, exception, evidence, and lifecycle owners.
- [DE-085](085-classification-and-sensitive-data.md), [DE-086](086-access-control-for-analytical-data.md), and [DE-087](087-masking-tokenization-and-de-identification.md) govern classification, least privilege, and minimization of audit stores.
- [DE-088](088-retention-and-deletion.md) governs evidence retention, holds, backup expiry, redaction/deletion workflows, receipts, and restore behavior.
- [API-034](../../28-api-and-service-engineering/modules/034-authorization-checks.md) connects authorization decision and enforcement evidence; [API-046](../../28-api-and-service-engineering/modules/046-object-level-authorization.md) develops exact-object authorization and TOCTOU reasoning.
- [DE-090](../ROADMAP.md) uses trustworthy history and decision evidence to support accountable data products and service expectations.

## References

- World Wide Web Consortium, *PROV-DM: The PROV Data Model*, W3C Recommendation, 2013. <https://www.w3.org/TR/prov-dm/>
- World Wide Web Consortium, *PROV-O: The PROV Ontology*, W3C Recommendation, 2013. <https://www.w3.org/TR/prov-o/>
- National Institute of Standards and Technology, *Guide to Computer Security Log Management*, SP 800-92, 2006. <https://csrc.nist.gov/pubs/sp/800/92/final>
- National Institute of Standards and Technology, *Security and Privacy Controls for Information Systems and Organizations*, SP 800-53 Rev. 5 Update 1, 2020. <https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final>
- OpenTelemetry Authors, “Logs Data Model,” current specification. <https://opentelemetry.io/docs/specs/otel/logs/data-model/>
- OpenLineage Authors, “Object Model,” current specification documentation. <https://openlineage.io/docs/spec/object-model/>
- Internet Engineering Task Force, *Certificate Transparency Version 2.0*, RFC 9162, 2021. <https://www.rfc-editor.org/rfc/rfc9162.html>
- Internet Engineering Task Force, *Internet X.509 Public Key Infrastructure Time-Stamp Protocol (TSP)*, RFC 3161, 2001. <https://www.rfc-editor.org/rfc/rfc3161.html>
- Amazon Web Services, “Validating CloudTrail Log File Integrity,” current CloudTrail documentation. <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-log-file-validation-intro.html>
- OWASP Foundation, “Logging Cheat Sheet,” current guidance. <https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html>
- Cybersecurity and Infrastructure Security Agency, “Best Practices for Event Logging and Threat Detection,” 2024. <https://www.cisa.gov/resources-tools/resources/best-practices-event-logging-and-threat-detection>
- SLSA Community, “Provenance,” SLSA specification 1.2, 2025. <https://slsa.dev/spec/v1.2/provenance>

## Exercises

### Exercise 1

Distinguish an event, evidence, auditability, provenance, lineage, observability, attribution, association, delegation, and chain of custody. For an analyst-triggered scheduled transformation, model the relevant entities, activity, agents, usage, generation, and delegation without inferring unsupported derivation.

### Exercise 2

An audit chain contains 1,000 canonical events and an independently signed checkpoint at event 900. Explain what verification can and cannot conclude if event 450 is modified, event 600 is deleted, events 700 and 701 are reordered, the last 40 events are truncated, the producer omitted a real action before capture, and the signing key was compromised after checkpoint creation.

### Exercise 3

A gateway journal contains 50,000 eligible request IDs. The evidence store has 49,850 unique mapped IDs, 120 known missing IDs, 30 authorized test exclusions, 200 duplicate deliveries, 75 late events within the reporting watermark, and 10 invalid records that are among the 120 missing mappings. Reconcile the population, compute governed coverage, and explain how duplicates, late events, and invalid records should be reported.

### Exercise 4

Design an evidence contract and operational architecture for sensitive analytical exports. Cover actor/effective subject/workload, object and policy versions, decision and outcome, event/observed time, delivery and duplicate semantics, canonicalization and anchoring, completeness reconciliation, redaction, access control, retention/holds/deletion, queries, metrics, and adversarial tests.

### Exercise 5

An investigation receives a database audit file, identity-provider records, a dashboard export, and an analyst notebook. The systems have different clocks, one parser changed midmonth, and the notebook contains customer identifiers. Design collection, normalization, analysis, handoff, reproducibility, minimization, and disposition procedures. State which conclusions would remain conditional.

## Answers to the Exercises

### Answer 1

An **event** is a structured assertion that an occurrence happened; **evidence** is information used to support or challenge a claim; **auditability** is the capability to reconstruct and evaluate the claim from protected retrievable evidence. **Provenance** describes entities, activities, agents, and influence/responsibility; **lineage** emphasizes dependency paths. **Observability** uses signals to understand runtime state but may be sampled, short-lived, or mutable. **Attribution** relates an entity to an agent, **association** an activity to an agent, and **delegation** one agent acting for another. **Chain of custody** documents evidence handling.

Model the exact input snapshots, code/configuration, policy, run record, and output snapshot as entities. The scheduled transformation is an activity that used the exact inputs and generated the output. The orchestration workload and analyst are agents; associate the workload with execution and record that it acted on behalf of the analyst only if authenticated scheduling evidence supports that relation. Attribute owned code or output according to actual responsibility. Record runtime usage for every read, but assert derivation only where code/runtime evidence supports influence. Preserve the source and confidence of each relation.

### Answer 2

Given deterministic canonicalization, collision resistance, an authentic checkpoint, and trustworthy key state, modifying event 450 changes its digest and all successors through 900; deleting 600 breaks the predecessor link; and swapping 700/701 changes order-sensitive inputs. Each should fail verification against the event-900 checkpoint.

The checkpoint says nothing directly about the unanchored suffix after 900. Truncating the last 40 events can go undetected unless a later protected checkpoint, expected range/sequence, independent receipt, or eligible-population reconciliation proves they should exist. A real action omitted before event construction never entered the chain and also requires independent completeness evidence. A compromise after checkpoint creation need not invalidate the earlier checkpoint if trustworthy timestamp/key-status evidence establishes it predates compromise, but incident review must bound the compromise interval and verify the anchor. None of the cases establishes whether the originally committed events were truthful or whether credential use represented human intent.

### Answer 3

The independent population is 50,000. The disjoint accounting is 49,850 mapped observed IDs, 120 known missing mappings, and 30 authorized exclusions, totaling 50,000. The required denominator after governed exclusions is $50{,}000-30=49{,}970$. Coverage is

$$
\frac{49{,}850}{49{,}970}\approx 0.9975986=99.76\%.
$$

The 200 duplicate deliveries do not increase unique coverage; report them as delivery/ingestion behavior and verify they map to existing event IDs. The 75 late events are included in the 49,850 only if they arrived before final reconciliation; report their latency and whether the earlier report was provisional. The ten invalid records are already members of the 120 missing mappings, so do not double-count them; expose `invalid=10` as a reason subset and retain/quarantine them for correction. Coverage is not 100%, and authorized exclusions need owner, reason, and expiry rather than silent removal.

### Answer 4

Define `sensitive_export` with stable event and request/action IDs; authenticated principal, effective subject, workload/deployment, session and delegation; tenant; stable dataset and exact snapshot; query/template digest and classified parameter references; policy bundle/rule, decision, reason, approval/exception, break-glass; attempted/denied/succeeded/failed outcome; result object/delivery reference; event, record and observed times with clock metadata; correlation/trace; producer and schema versions. Prohibit credentials, raw rows, tokens, and unrestricted query literals.

Capture request and decision at the gateway/policy engine, read effect at the store, and delivery at the export service. Use at-least-once delivery, stable IDs, acknowledgments, quarantine/dead-letter, late windows, and explicit deduplication. Canonicalize a versioned envelope, chain or Merkle-commit bounded ranges, sign checkpoints with protected rotated keys, and copy anchors to an independently administered store. Reconcile the gateway's eligible request journal to decisions, reads, results, and evidence; report missing joins and governed exclusions.

Classify the evidence, encrypt it, separate append/administration/review/destruction roles, log evidence access, and use scoped pseudonymous identity references with controlled resolution. Apply authorized retention triggers, minimum/maximum periods, holds, backup expiry, key lifecycle, and verified deletion. Provide control queries for unapproved success, unmatched store reads, break-glass, missing events, stale anchors, and late or invalid records. Measure coverage, gaps, latency, duplicates, dead letters, schema and key status, retrieval, unusual evidence access, and expiry. Test producer outage/compromise, replay, duplicates, clock skew, schema change, key rotation/compromise, anchor loss, unauthorized evidence access, redaction, restore, hold, and deletion.

### Answer 5

Collect each source into a restricted case store with source system, scope/range, acquisition method, collector/operator, original timezone/clock metadata, tool/version, acquisition time, byte count and digest. Preserve originals read-only. Record every transfer with sender, recipient, authority, purpose, digest, time, protection, and acknowledgment. Treat the dashboard export as a derived artifact: capture its query, filters, dashboard/version, source data version, generation time, and exporter where available; a screenshot alone is weak.

Normalize through versioned parsers while retaining raw inputs and unknown fields. Apply the correct parser on each side of the midmonth change and record mapping provenance. Keep event, record, and observed times; estimate clock offset/uncertainty from trustworthy shared events and use intervals plus causal IDs instead of forcing a total order. Execute joins, filters, timezone conversion, and timeline generation as reproducible activities with code/configuration, analyst, inputs, outputs, and digests.

Move the notebook into the controlled case boundary, restrict access, replace customer values in working derivatives with scoped protected references where analysis permits, and preserve any required original under explicit authority/hold. Pin its environment, dependencies, inputs, parameters, and outputs; disable uncontrolled network or export paths as appropriate. At closure, apply case, legal-hold, security, privacy, records, backup, and deletion policies to originals, derivatives, identity maps, keys, and exports; record disposition receipts.

Conclusions remain conditional on source truth and capture completeness, credential attribution, clock bounds, parser correctness, undocumented dashboard transformations, notebook reproducibility, and any missing eligible-population denominator. Chain of custody and matching digests support unchanged handling; they do not remove those epistemic limits.
