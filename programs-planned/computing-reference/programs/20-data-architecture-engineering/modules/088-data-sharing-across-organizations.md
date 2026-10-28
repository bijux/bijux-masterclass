---
module_id: DARCH-088
program: Data Architecture Engineering
level: 2
module_number: 88
title: Data Sharing Across Organizations
status: complete
last_verified: 2026-09-03
---

# Data Sharing Across Organizations

## One-Page Review

### Governing question

How should independent organizations share data or permit joint computation while preserving each party's authority, semantics, purpose, privacy, security, sovereignty, service, evidence, remedy, economics, and ability to end the relationship?

### Essential definitions

- **Cross-organization data sharing** is a governed relationship in which one legal or administrative entity makes data, a data service, or a bounded computation available to another.
- A **provider** is the party authorized to offer a named data asset or computation; possession alone does not establish authority.
- A **recipient** is a party permitted to obtain data, query a service, or receive an approved result under a defined purpose and set of obligations.
- A **collaboration operator** runs an exchange, marketplace, clean room, transfer service, identity service, or other shared control plane without automatically becoming the owner of every participant's data.
- A **sharing package** binds a stable asset identity to contract, schema, semantics, classification, provenance, quality, time, policy, delivery, service, and lifecycle versions.
- A **sharing agreement** records parties, authority, assets, purposes, permissions, prohibitions, duties, onward-use rules, service, cost, liability, evidence, incident, remedy, change, termination, and dispute terms.
- A **machine policy** is an executable representation of some agreement or organizational rules; it neither creates legal authority nor guarantees enforcement by itself.
- **Purpose binding** associates a request and its resulting uses with a specific approved objective, population, decision, time, and recipient context.
- **Onward sharing** is any disclosure or access by an additional party, including affiliates, subcontractors, tools, model providers, and derived-product consumers.
- A **clean room** is a controlled collaboration environment that restricts data access, query forms, computation, or outputs; the label alone proves neither privacy nor security.
- **Move data to compute** copies or delivers data into a recipient-controlled environment. **Move compute to data** executes approved logic near provider-controlled data and returns bounded output.
- **Revocation** prevents specified future access. It does not retroactively erase exports, caches, screenshots, models, or other derivatives already outside the enforcement boundary.
- A **sharing receipt** records request, parties, purpose, authority, asset and policy versions, decision, delivery or computation, result, lineage, obligations, costs, and limitations.
- A **derived asset** is data, a model, statistic, feature, report, or decision materially produced from shared data and therefore potentially subject to provenance and use obligations.
- **Closure** ends authorization and technical access, reconciles copies and derivatives, revokes credentials and routes, settles duties and costs, preserves required evidence, and prevents recovery from reactivating the exchange.

### Central model, mechanism, or theorem

Represent a sharing relationship as:

`X = (U, P, A, C, I, D, G, O, R, L)`

where `U` is use and affected outcomes, `P` parties, roles, and authority, `A` asset identity and semantics, `C` contractual rights and duties, `I` identity, delegation, and trust, `D` delivery or controlled computation, `G` governance, policy, privacy, and security, `O` observation, provenance, cost, and outcomes, `R` resilience, incidents, remedy, and recovery, and `L` lifecycle and closure. Sharing is qualified only when every component has an accountable owner, enforceable boundary, evidence, and failure behavior appropriate to the use.

### Critical invariants

- Provider, recipient, operator, identity issuer, asset, distribution, agreement, policy, request, delivery, output, derivative, receipt, and incident have distinct stable identities.
- The provider proves authority to share the exact asset for the exact purpose; possession, catalog publication, or technical access is insufficient.
- Every recipient, actor, service, subcontractor, region, purpose, and onward-sharing path is known or explicitly denied.
- Agreement prose, catalog metadata, executable policy, delivery configuration, and observed enforcement are versioned and reconciled without treating any one as the whole truth.
- Minimum necessary fields, records, time range, precision, frequency, and duration are shared; minimization is evaluated against the use, not file size alone.
- Semantic, temporal, quality, provenance, and correction limits travel with each distribution and derivative.
- Identity is authenticated at each boundary, delegated authority remains attributable, and tokens are audience-, scope-, purpose-, and time-bounded.
- Copies, queries, clean rooms, APIs, events, files, and models receive controls suited to their different persistence, inference, retry, and revocation behavior.
- A successful transfer, query, or computation is distinct from authorized receipt, compliant use, correct interpretation, beneficial outcome, and fulfilled duties.
- Incidents, disputes, corrections, consent or authority changes, deletion, legal holds, and termination propagate through named contacts and tested mechanisms.
- Revocation claims state their boundary; existing copies and derivatives are reconciled rather than assumed to disappear.
- Closure removes every live and recoverable access path while preserving evidence required for accountability, dispute, audit, and remedy.

### Common failures

Common failures include treating a nondisclosure agreement as a data architecture; assuming a marketplace listing proves sharing authority; exporting an entire table for one aggregate; using a shared service account; trusting a recipient's network because it belongs to a partner; declaring tokenized data anonymous; allowing unrestricted repeated clean-room queries; omitting subcontractors and derived models; recording delivery but not use; confusing revocation with remote deletion; accepting schema compatibility as semantic agreement; failing to propagate corrections; and ending a contract while credentials, copies, subscriptions, caches, recovery snapshots, and renewal jobs remain active.

### Compact example

Ten invented sharing proposals are evaluated against six declared requirements. Four qualify; one each lacks provider authority, a complete agreement, bounded identity, an enforceable purpose policy, a safe delivery design, or end-to-end evidence and closure. Seven organizations, seven delivery patterns, four data classes, ten receipts, and ten decisions are counted. Executable evidence confirms only those declarations and counts. It proves no real authority, legality, consent, privacy, security, semantic fitness, enforcement, deletion, economics, or beneficial outcome.

### Connections

[DARCH-027](027-producer-and-consumer-contracts.md), [DARCH-034](034-api-led-data-access.md), [DARCH-057](057-shared-code-sets-and-controlled-vocabularies.md), [DARCH-064](064-lineage-architecture.md), [DARCH-074](074-consent-and-purpose-limitation.md), [DARCH-075](075-data-residency-and-sovereignty.md), [DARCH-078](078-masking-tokenization-and-clean-rooms.md), [DARCH-079](079-audit-and-provenance-architecture.md), [DARCH-084](084-federated-computational-governance.md), and [DARCH-087](087-federated-query-and-data-virtualization.md) establish contracts, access, semantics, provenance, policy, privacy, sovereignty, clean rooms, governance, and federation foundations. [DARCH-089](../ROADMAP.md) next develops interoperability without a universal model.

## Governing Question

Two organizations can exchange a file in minutes. Establishing who may disclose which version, for what purpose, to which identities and processors, under which semantics and jurisdictions, with which controls, evidence, correction, remedy, cost, and end condition is the architecture problem.

The governing question is not whether a transfer mechanism exists. It is whether every party can make and verify the claims needed to share responsibly while retaining independent authority. Durable designs make the relationship explicit, minimize the asset and duration, select a delivery or computation pattern from risk and outcome, enforce controls at every boundary, observe use without creating another surveillance hazard, and plan closure before access begins.

## Why This Matters

NIST's [Using Privacy Framework 1.1](https://www.nist.gov/privacy-framework/using-privacy-framework-11) material describes a data processing ecosystem of interconnected entities and discusses profiles, formal agreements, communication, verification, and reassessment across organizational roles. It supports treating privacy outcomes and third-party relationships as an operating system, not a one-time approval.

NIST [SP 800-207](https://csrc.nist.gov/pubs/sp/800/207/final) defines zero trust around users, assets, and resources rather than implicit trust based on network location or ownership. A partner network, private link, or collaboration membership therefore cannot replace per-request authentication, authorization, context, and resource protection.

NIST [SP 800-188](https://csrc.nist.gov/pubs/sp/800/188/final) covers de-identification techniques and governance, including disclosure risk, quasi-identifiers, synthetic data, and formal privacy approaches. It also cautions that simple masking tools may not perform adequate de-identification. Sharing architecture must state the threat model and residual linkage risk rather than relabel data anonymous.

The NIST [Cybersecurity Framework 2.0](https://www.nist.gov/cyberframework) organizes cybersecurity outcomes across Govern, Identify, Protect, Detect, Respond, and Recover and includes third-party and supply-chain considerations. Cross-organization sharing spans all six functions because it creates durable dependencies, credentials, data paths, detection responsibilities, incident contacts, and recovery behavior.

NIST [SP 800-61 Revision 3](https://csrc.nist.gov/pubs/sp/800/61/r3/final) integrates incident response into cybersecurity risk management. A sharing relationship needs joint preparation, detection, notification, containment, investigation, recovery, and lessons learned; forwarding an alert to a generic contract contact is not an incident design.

W3C [DCAT 3](https://www.w3.org/TR/vocab-dcat-3/) models catalogs, datasets, dataset series, distributions, data services, versions, relationships, access rights, licenses, and policies. It helps organizations exchange discoverable metadata while distinguishing the conceptual dataset from a file, API, or other accessible distribution.

The W3C [ODRL Information Model 2.2](https://www.w3.org/TR/odrl-model/) represents assets, parties, permissions, prohibitions, duties, constraints, remedies, consequences, agreement policies, and conflict strategies. It can carry interoperable usage-policy expressions, but the specification does not supply organizational authority or enforcement by itself.

The W3C [PROV Overview](https://www.w3.org/TR/prov-overview/) describes provenance through entities, activities, and agents so users can assess quality, reliability, and trustworthiness. Cross-organization evidence must preserve who produced, transformed, delivered, and received which version without assuming that a signed file proves its meaning or quality.

IETF [RFC 8693](https://www.rfc-editor.org/info/rfc8693/) defines OAuth token exchange and distinguishes delegation from impersonation, including subject and actor context. It provides a useful protocol mechanism for cross-boundary delegation, while authorization policy, token validation, revocation propagation, and recipient semantics remain deployment responsibilities.

IETF [RFC 9700](https://www.rfc-editor.org/info/rfc9700/) records current OAuth 2.0 security best practice, including sender-constrained tokens, exact redirect matching, and stronger client authentication guidance. Cross-organization API sharing should use contemporary protections and narrowly bound tokens rather than long-lived bearer secrets copied into partner systems.

Delta Lake's [Delta Sharing documentation](https://docs.delta.io/delta-sharing/) describes an open REST protocol for sharing table snapshots, older snapshots, changes, and streams across tools. The protocol demonstrates transport and version access; providers still need identity, authority, policy, semantic, service, evidence, and lifecycle architecture around it.

AWS [Clean Rooms documentation](https://docs.aws.amazon.com/clean-rooms/latest/userguide/what-is.html) describes collaboration memberships, configured data, analysis rules and templates, logs, output controls, differential privacy, and cryptographic options. Its explicit shared-responsibility and configuration model illustrates why a clean-room product is a control surface, not proof that a collaboration is safe.

Snowflake's [Secure Data Sharing documentation](https://docs.snowflake.com/en/user-guide/data-sharing-intro) distinguishes providers, consumers, shares, read-only imported databases, direct shares, listings, exchanges, and clean rooms. It also distinguishes same-platform metadata sharing from cross-region replication, which matters for copy, residency, cost, and revocation claims.

Google Cloud's [Introduction to BigQuery Sharing](https://cloud.google.com/bigquery/docs/analytics-hub-introduction) describes exchanges, listings, publishers, subscribers, linked datasets, roles, usage metrics, private and public sharing, and commercial offerings. The service model reinforces that discovery, subscription, access, billing, and actual use are separate events.

OpenLineage's [object model](https://openlineage.io/docs/spec/object-model/) represents datasets, jobs, runs, events, and extensible facets. Sharing receipts can connect provider transformations, distributions, recipient ingestion, and derivatives, but instrumentation coverage and disclosure-safe metadata still require deliberate design.

The Bitol [Open Data Contract Standard](https://bitol-io.github.io/open-data-contract-standard/latest/) provides machine-readable product, schema, quality, service, role, support, and infrastructure sections. Such contracts can improve technical coordination, but they supplement rather than replace negotiated rights, organizational accountability, and observed controls.

Together these sources support ecosystem risk management, resource-focused trust, de-identification governance, incident readiness, interoperable catalog and policy descriptions, attributable delegation, secure protocols, controlled collaboration, lineage, and machine-readable contracts. They do not determine applicable law, establish a party's authority, prove semantic fitness, prevent all inference or copying, guarantee downstream behavior, or demonstrate public benefit. Those claims require local legal, policy, technical, and affected-party evidence.

## Prerequisites and Retrieval

You should understand data products, contracts, schemas, semantics, time, classification, privacy, consent, purpose limitation, security, identity federation, authorization, APIs, events, files, query engines, clean rooms, cryptography, lineage, observability, service objectives, incident response, retention, deletion, legal hold, sovereignty, cost, recovery, and architecture decisions.

Retrieve provider, recipient, operator, processor, subcontractor, affected party, asset, distribution, service, agreement, permission, prohibition, duty, purpose, authority, license, classification, minimum necessary, onward sharing, delegation, impersonation, audience, scope, clean room, de-identification, linkage attack, output control, privacy budget, receipt, derivative, correction, incident, remedy, revocation, termination, and closure.

As a retrieval test, inspect a proposed exchange of customer transaction data with a fraud consortium. Ask who may disclose it; whose people are affected; which records and time range are necessary; which customer, transaction, fraud, and time meanings align; whether a copy, API, query, clean room, or aggregate is justified; which recipient identities, processors, regions, purposes, models, and outputs are allowed; how corrections, incidents, deletion, audit, cost, disputes, and closure work; and which claims cannot be enforced after data leaves provider control. A signed contract and encrypted channel answer only part of the problem.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish bilateral sharing, exchanges, marketplaces, data spaces, APIs, events, files, shared tables, federated queries, clean rooms, trusted research environments, and public release;
2. identify parties, roles, affected populations, authority, purposes, assets, distributions, derivatives, regions, processors, and onward-sharing paths;
3. design agreements and machine contracts for semantics, quality, rights, duties, service, cost, incident, remedy, change, renewal, and closure;
4. choose between data movement, remote query, approved computation, aggregation, de-identification, synthetic data, and no sharing;
5. bind identity, delegation, audience, scope, purpose, device or workload, policy, and evidence across organizational trust domains;
6. reason about minimization, inference, linkage, clean-room output, privacy budgets, copies, derivatives, deletion, and revocation limits;
7. build provenance, receipts, correction, monitoring, audit, incident, dispute, and outcome mechanisms without excessive disclosure;
8. operate compatibility, service objectives, quotas, billing, schema and policy change, renewal, recovery, and termination;
9. test organizational, contractual, semantic, privacy, security, delivery, evidence, and lifecycle failure boundaries; and
10. defend a sharing architecture from explicit outcomes, alternatives, risks, evidence, economics, and residual uncertainty.

## Core Exposition

**Begin with a legitimate outcome.** Name the decision, service, research question, public benefit, commercial product, or statutory function the relationship supports. Identify affected people and organizations as well as direct users. “The partner wants our data” is demand, not justification.

**Test necessity before mechanism.** Ask whether the outcome can be achieved with no sharing, a public source, a smaller aggregate, provider-run computation, a synthetic dataset, a short-lived query, or a coarser time range. Sharing less reduces semantic, privacy, security, operational, and closure burden.

**Model every party and role.** Record provider, recipient, exchange operator, identity issuer, cloud or infrastructure provider, subcontractor, analyst, result receiver, auditor, incident contact, payer, and affected population. One organization may hold several roles; similar role names do not imply identical obligations across jurisdictions.

**Prove authority for the exact act.** Authority to collect, store, analyze, publish metadata, disclose, license, sell, query, transform, or permit onward sharing can differ. Record the originating decision, applicable policy or agreement, scope, effective interval, approver, evidence, challenge path, and conditions. Architecture cannot manufacture missing authority.

**Separate possession from ownership and authority.** A processor, platform, reseller, or consortium member may possess bytes without having the right to disclose them. “It is in our bucket” is a location statement.

**Identify the asset independently of its distribution.** The conceptual customer-risk product, a versioned Parquet snapshot, a query endpoint, a stream topic, and a clean-room table are related but distinct. Stable identifiers let contracts and receipts name exactly what changed or moved.

**Publish a sharing package.** Bind owner, authority, consumers, purpose, schema, grain, keys, semantic mappings, valid and observation time, classifications, provenance, quality, completeness, corrections, distribution, policy, service, cost, support, change, retention, deletion, and closure. A raw table grant externalizes ambiguity.

**Treat semantics as a negotiated boundary.** Reconcile identifiers, units, code sets, nulls, precision, time zones, valid time, event meaning, populations, inclusion rules, and aggregation. Record accepted differences and losses. Compatible serialization is not shared meaning.

**Represent time explicitly.** A snapshot has production, valid, observation, extraction, publication, availability, receipt, and expiry times. Streams add event and processing time. Agreement periods and consent or authority intervals do not automatically align with data time.

**Classify fields, records, combinations, and outputs.** Sensitivity can emerge through joins, rarity, longitudinal history, small groups, location, free text, embeddings, or model parameters even when individual columns appear ordinary. Classification must follow transformations and derivatives.

**Write the agreement as an operating contract.** Name parties, authority, assets, purposes, permitted actions, prohibitions, duties, recipients, processors, regions, security, privacy, quality, service, cost, intellectual-property terms, attribution, audit, incident notification, correction, deletion, hold, remedy, dispute, change, renewal, termination, and survival. Obtain qualified legal advice where law or negotiated rights apply.

**Do not confuse agreement with enforcement.** Prose creates commitments and remedies; catalogs aid discovery; machine contracts express technical expectations; policies make decisions; enforcement points constrain behavior; evidence records what was observed. A durable design reconciles all five.

**Version rights and technical contracts independently.** A schema can remain stable while purpose, permitted recipients, residency, retention, pricing, or incident terms change. Conversely, a schema can change under the same agreement. Receipts bind the exact versions effective for each use.

**Resolve policy conflicts explicitly.** Provider, recipient, operator, jurisdiction, purpose, data-subject preference, and platform rules can conflict. Define precedence, denial behavior, escalation, exceptions, timeouts, and evidence. Silent “most permissive wins” is unsafe.

**Choose a topology from authority and risk.** Bilateral links simplify party count but multiply integrations. A hub, exchange, or marketplace centralizes discovery and some controls but creates operator concentration. A consortium distributes governance but requires conflict and exit mechanisms. Public release maximizes reach and makes revocation least plausible.

**Choose a delivery pattern from the outcome.** Options include managed file export, event subscription, API, shared table, replicated distribution, federated query, provider-run job, remote function, clean room, trusted research environment, aggregate publication, synthetic data, or no sharing. Compare persistence, expressiveness, freshness, isolation, inference, cost, portability, and closure.

**Understand copy semantics.** After a recipient obtains plaintext or a usable export, provider-side revocation usually affects future access, not existing copies. Contracts, recipient controls, attestations, watermarking, monitoring, and remedies may reduce risk but do not restore technical possession.

**Understand query semantics.** Query-in-place can reduce bulk copies but still exposes results, timing, errors, metadata, and repeated-query inference. Caches, temporary tables, client downloads, and downstream notebooks create new copies. Query controls require shape, rate, cardinality, and output reasoning.

**Understand clean-room semantics.** Specify members, data inputs, identity matching, approved templates, query roles, result receivers, thresholds, differential-privacy parameters, privacy-budget accounting, logs, exports, billing, and deletion. Test differencing, collusion, auxiliary data, malicious queries, repeated runs, model leakage, and operator compromise.

**Treat de-identification as a risk claim.** Name the attacker, auxiliary data, direct and quasi-identifiers, transformations, linkage tests, utility loss, release context, review, residual risk, and reassessment trigger. Tokenization and pseudonymization often preserve linkability and remain sensitive.

**Use synthetic data with provenance and limits.** Synthetic output can leak training records or reproduce bias, rare patterns, and invalid correlations. Record generator, training source, privacy method, evaluation, intended analyses, prohibited uses, uncertainty, and derivative obligations.

**Bind organizational identity.** Establish issuer trust, tenant and organization identity, user or workload identity, assurance level, lifecycle, group semantics, and emergency access. A partner email domain or account invitation is not durable authorization.

**Preserve subject and actor.** When a broker, service, analyst tool, or pipeline acts for another principal, retain both the requesting subject and current actor. Distinguish delegation from impersonation. Prevent a service token from erasing the human, workload, organization, and purpose chain.

**Constrain credentials.** Prefer asymmetric client authentication and sender-constrained, audience-, scope-, resource-, purpose-, and time-bounded tokens. Rotate keys, validate issuers and audiences, prevent confused-deputy use, propagate revocation where designed, and avoid shared long-lived bearer secrets.

**Authorize more than connection.** Evaluate organization, subject, actor, asset, field, row, action, purpose, region, time, device or workload posture, output, rate, and obligations. Re-evaluate long sessions and subscriptions as policy or identity changes.

**Place enforcement at every consequential boundary.** Cover discovery, subscription, token issuance, endpoint, source, query planner, row and column filters, computation, output, export, cache, derivative publication, retention, and deletion. Record which controls are preventive, detective, contractual, or merely advisory.

**Minimize delivery.** Limit fields, rows, population, history, precision, frequency, volume, and access duration. Provide provider-calculated aggregates when raw values are unnecessary. Avoid “future usefulness” as an unlimited purpose.

**Protect the transport and the object.** Authenticate endpoints, encrypt in transit, sign or hash immutable manifests, isolate keys, scan for malware and malicious content, verify size and schema, prevent replay and substitution, and define atomicity. TLS does not establish asset authority or semantic correctness.

**Protect recipient storage and compute.** Define approved regions, accounts, networks, services, devices, keys, administrators, backups, logs, exports, model training, notebooks, and subprocessors. Provider controls end at the boundary unless the recipient demonstrably implements corresponding safeguards.

**Control egress and derivatives.** Decide which aggregates, rows, files, models, features, reports, screenshots, and decisions may leave the collaboration. Apply output review where needed. Register material derivatives with provenance, policy, retention, owners, and recipients.

**Design quality and correction flows.** Publish quality dimensions, known limitations, acceptance checks, reconciliation, issue contacts, severity, correction identifiers, and replacement or withdrawal procedures. Recipients must distinguish an empty correction from a missing update.

**Propagate schema and semantic change.** Provide notice windows, compatibility rules, conformance tests, dual publication, migration evidence, consumer acknowledgment, and retirement dates. Contract renewal does not prove technical compatibility.

**Define service objectives across the journey.** Measure discovery, approval, provisioning, freshness, availability, latency, delivery completeness, correction time, revocation time, incident notification, support, and closure. Provider endpoint uptime alone is not recipient success.

**Assign capacity and cost.** Name who pays for storage, transfer, egress, query compute, privacy mechanisms, identity, logs, support, audits, incidents, and exit. Enforce quotas and budgets. Unexpected bills can terminate a socially valuable sharing relationship as surely as an outage.

**Create end-to-end receipts.** Record request, parties, subject and actor, purpose, authority, agreement, asset, distribution, schema, policy decision, source version, transformation, delivery or computation, result, obligations, lineage, cost, status, and limitations. Minimize sensitive literals and separate each party's evidence custody.

**Observe use without inventing omniscience.** Provider logs can prove issued access or source reads, not every downstream use. Recipient attestations and audits add evidence but have scope and sampling limits. State blind spots, log retention, clock assumptions, and tamper controls.

**Measure outcomes and harms separately.** Counts of listings, subscriptions, bytes, queries, and organizations show activity. Measure whether the intended decision or service improved, who benefited, who was excluded, what errors and incidents occurred, and whether a smaller sharing design would suffice.

**Prepare joint incident response.** Define event taxonomy, detection sources, severity mapping, twenty-four-hour contacts, secure evidence channels, notice decision rights, containment authority, preservation, regulator or affected-party coordination where applicable, public communication, recovery, and lessons learned.

**Design disputes and remedy.** Provide routes to challenge authority, quality, billing, interpretation, access denial, misuse, correction, or deletion. Preserve evidence, pause risky use, contain harm, correct outputs, notify affected parties when required, and track remedy rather than closing at ticket resolution.

**Treat deletion as a distributed workflow.** Inventory provider sources, delivered copies, backups, caches, notebooks, models, features, aggregates, logs, and downstream recipients. Define which must be erased, corrected, restricted, retained under hold, or cannot be reversed, with evidence and residual limitations.

**Treat revocation precisely.** Revoke tokens, memberships, shares, endpoints, subscriptions, keys, URLs, query templates, routes, and renewal jobs. Ask the recipient to reconcile existing copies and derivatives under the agreement. Do not claim cryptographic remote deletion when none exists.

**Recover cautiously.** Restore current agreements, identity trust, keys, policies, asset versions, corrections, tombstones, holds, incident state, recipient status, and termination records before reopening. A backup can resurrect access that governance intentionally removed.

**Plan closure before opening.** Define natural expiry, renewal evidence, export and derivative inventory, data return or deletion, key destruction, credential revocation, subscription drainage, cost settlement, dispute survival, evidence retention, operator exit, and recovery nonactivation.

**Prefer no sharing when assurance is inadequate.** Missing authority, incompatible purpose, uncontrolled onward use, unacceptable re-identification risk, unresolvable semantics, disproportionate harm, absent remedy, or unverifiable closure can make refusal the correct architecture decision.

## Definitions and Notation

Use:

`X = (U, P, A, C, I, D, G, O, R, L)`.

Represent a party as:

`p = (id, legal_or_administrative_identity, role, authority, contacts, processors, regions, assurance, lifecycle)`.

Represent a sharing package as:

`a = (id, owner, source, version, schema, semantics, time, classification, provenance, quality, distributions, correction, lifecycle)`.

Represent an agreement as:

`c = (id, parties, authority, assets, purposes, permissions, prohibitions, duties, recipients, regions, service, cost, incident, remedy, change, termination)`.

Represent an access decision as:

`d = (request, subject, actor, organization, purpose, asset, action, context, agreement, policy_versions, result, obligations, expiry, evidence)`.

Represent a sharing receipt as:

`r = (request, parties, purpose, authority, agreement, asset, distribution, policy, decision, delivery_or_compute, result, lineage, obligations, cost, status, limitations)`.

Let the minimum sharing set for use `u` be `M(u)`. A proposed distribution `A` is minimized only relative to declared dimensions—fields, records, population, time, precision, frequency, volume, and duration—and evidence that `A - M(u)` is empty or justified. A smaller byte count alone does not prove minimization.

Let `Reach(a)` contain every provider, recipient, operator, processor, copy, cache, model, report, decision, and derivative reachable from asset `a`. The set is evidence-bounded: missing lineage, unreported exports, or opaque subcontractors make it incomplete.

Define propagation coverage for an event class `e` as:

`C_e = confirmed_required_targets / known_required_targets`.

The ratio is undefined when the denominator is unknown and never proves that unknown targets do not exist.

Define query disclosure budget `B` as a mechanism-specific composition of approved outputs. For differential privacy, composition must follow the chosen formal accounting method; counting queries alone is not a privacy proof.

Define `Revoked(x, t)` to mean specified future access paths for identity, agreement, asset, or distribution `x` are denied after time `t`. It says nothing about copies or derivatives created before `t` unless those are separately reconciled.

Define `Closed(c)` to require no active or recoverable identity, credential, membership, listing, route, share, subscription, endpoint, file URL, query template, cache, copy, derivative permission, renewal, billing path, or recovery configuration can continue agreement `c`, while required evidence and unresolved duties remain controlled.

## Mechanisms, Invariants, or Proof Structure

Use the following assurance gates.

**Outcome gate.** Define purpose, decision, users, affected parties, benefit, necessity, alternatives, minimization, success, harm, and end condition.

**Party gate.** Verify provider, recipient, operator, issuer, processor, subcontractor, analyst, result receiver, payer, auditor, incident contact, and role lifecycle.

**Authority gate.** Bind collection, use, disclosure, transformation, licensing, onward-sharing, and termination authority to exact assets, parties, purposes, times, and evidence.

**Asset gate.** Verify stable identity, owner, source, schema, grain, keys, semantics, time, classification, provenance, quality, distributions, corrections, and lifecycle.

**Agreement gate.** Reconcile parties, assets, purpose, permissions, prohibitions, duties, recipients, regions, security, privacy, service, cost, audit, incident, remedy, change, dispute, and termination.

**Identity gate.** Authenticate issuer, organization, subject, actor, workload, delegation, assurance, audience, scope, resource, purpose, device, time, revocation, and emergency use.

**Pattern gate.** Compare no sharing, aggregate, synthetic, file, event, API, shared table, replication, federation, provider-run compute, clean room, and trusted environment.

**Privacy gate.** Test minimization, direct and quasi-identifiers, auxiliary data, linkage, query differencing, collusion, privacy budgets, outputs, models, retention, deletion, and residual risk.

**Security gate.** Enforce endpoint trust, least privilege, encryption, key separation, integrity, replay protection, isolation, malware controls, quotas, egress, detection, and evidence.

**Semantic gate.** Validate identifiers, populations, grain, nulls, units, codes, precision, time, inclusion, quality, transformations, loss, and recipient interpretation.

**Delivery gate.** Define atomicity, versions, manifests, checksums, retries, duplication, completeness, freshness, acknowledgement, temporary state, and failure behavior.

**Output gate.** Control rows, aggregates, thresholds, repeated queries, models, features, reports, exports, screenshots, and registered derivatives.

**Evidence gate.** Correlate request, authority, agreement, identity, policy, asset, version, transformation, delivery, result, use evidence, lineage, obligations, cost, and limitations.

**Operations gate.** Manage service objectives, capacity, quotas, billing, support, corrections, change, compatibility, attestations, audits, renewal, and outcomes.

**Incident gate.** Prepare detection, classification, secure contacts, notice, containment, evidence, investigation, coordination, recovery, communication, remedy, and learning.

**Recovery gate.** Restore current agreements, identities, policies, keys, asset state, corrections, tombstones, holds, incidents, recipients, and termination before access.

**Closure gate.** Drain use, revoke access, reconcile copies and derivatives, delete or retain correctly, destroy keys, stop costs and renewal, preserve evidence, and test nonactivation.

### Executable evidence: sharing-candidate evaluation

The following program classifies ten invented sharing proposals against six declared requirements.

<!-- bijux-verify: {"id":"sharing-candidate-evaluation","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"proposals=10\nqualified=4\nmissing_authority=1\nincomplete_agreement=1\nidentity_gap=1\npurpose_policy_gap=1\nunsafe_delivery=1\nmissing_evidence_and_closure=1\norganizations=7\ndelivery_patterns=7\ndata_classes=4\nsharing_receipts=10\ndecision_events=10\n","stderr":""}} -->
```python
proposals = [
    {"organization": "hospital-a", "pattern": "clean-room", "class": "restricted", "authority": True, "agreement": True, "identity": True, "purpose": True, "delivery": True, "evidence": True},
    {"organization": "university-b", "pattern": "trusted-environment", "class": "sensitive", "authority": True, "agreement": True, "identity": True, "purpose": True, "delivery": True, "evidence": True},
    {"organization": "supplier-c", "pattern": "api", "class": "internal", "authority": True, "agreement": True, "identity": True, "purpose": True, "delivery": True, "evidence": True},
    {"organization": "agency-d", "pattern": "aggregate", "class": "public", "authority": True, "agreement": True, "identity": True, "purpose": True, "delivery": True, "evidence": True},
    {"organization": "broker-e", "pattern": "file", "class": "restricted", "authority": False, "agreement": True, "identity": True, "purpose": True, "delivery": True, "evidence": True},
    {"organization": "university-b", "pattern": "file", "class": "sensitive", "authority": True, "agreement": False, "identity": True, "purpose": True, "delivery": True, "evidence": True},
    {"organization": "supplier-c", "pattern": "api", "class": "internal", "authority": True, "agreement": True, "identity": False, "purpose": True, "delivery": True, "evidence": True},
    {"organization": "affiliate-f", "pattern": "shared-table", "class": "restricted", "authority": True, "agreement": True, "identity": True, "purpose": False, "delivery": True, "evidence": True},
    {"organization": "partner-g", "pattern": "event", "class": "sensitive", "authority": True, "agreement": True, "identity": True, "purpose": True, "delivery": False, "evidence": True},
    {"organization": "hospital-a", "pattern": "clean-room", "class": "restricted", "authority": True, "agreement": True, "identity": True, "purpose": True, "delivery": True, "evidence": False},
]

def evaluate(proposal):
    if not proposal["authority"]:
        return "missing_authority"
    if not proposal["agreement"]:
        return "incomplete_agreement"
    if not proposal["identity"]:
        return "identity_gap"
    if not proposal["purpose"]:
        return "purpose_policy_gap"
    if not proposal["delivery"]:
        return "unsafe_delivery"
    if not proposal["evidence"]:
        return "missing_evidence_and_closure"
    return "qualified"

results = [evaluate(proposal) for proposal in proposals]
print(f"proposals={len(proposals)}")
for outcome in ["qualified", "missing_authority", "incomplete_agreement", "identity_gap", "purpose_policy_gap", "unsafe_delivery", "missing_evidence_and_closure"]:
    print(f"{outcome}={results.count(outcome)}")
print(f"organizations={len({proposal['organization'] for proposal in proposals})}")
print(f"delivery_patterns={len({proposal['pattern'] for proposal in proposals})}")
print(f"data_classes={len({proposal['class'] for proposal in proposals})}")
print(f"sharing_receipts={len(proposals)}")
print(f"decision_events={len(results)}")
```

The output reports ten proposals, four qualified and one of each declared failure, seven organizations, seven delivery patterns, four data classes, ten declared receipts, and ten decisions.

The evidence is deliberately narrow. Invented Booleans and strings do not establish sharing authority, agreement validity, identity assurance, purpose enforcement, delivery safety, evidence completeness, closure, legality, consent, semantics, privacy, security, quality, cost, or outcome. Production assurance requires qualified organizational and legal review, authority records, contract and policy tests, identity federation tests, adversarial privacy analysis, delivery and output controls, lineage, incident exercises, recipient evidence, closure drills, and affected-party outcomes.

## Alternatives and Trade-Offs

**Do not share.** Authority, privacy, security, and closure exposure stay lowest. The intended collaboration or benefit may be impossible, so document the rejected need and conditions for reconsideration.

**Public release.** Access is broad, reusable, and operationally simple after publication. Revocation is weak, context is lost, and classification, provenance, accessibility, versioning, and correction must support an unknown audience.

**Bilateral managed files.** The delivery is portable and easy to inspect. Every recipient creates copies, key exchange, retry, retention, deletion, schema-change, and reconciliation work.

**Event subscription.** Changes arrive with low latency and explicit event identities. Ordering, replay, duplicate handling, schema evolution, consent or authority changes, and indefinite derived state become difficult.

**Purpose-specific API.** The provider retains a policy and service boundary and can minimize each response. Runtime coupling, rate, latency, availability, client compatibility, and export control remain.

**Shared live table.** Recipients get fresh query access without managing scheduled files. Platform coupling, query inference, provider load, policy placement, and cross-region fulfillment need evidence.

**Replicated distribution.** Recipient performance and provider isolation improve. Copies, freshness, residency, egress, deletion, encryption, and revocation become material.

**Federated query.** Data can remain in source systems and be composed on demand. Semantic mapping, snapshot limits, distributed policy, source protection, partial failure, and runtime cost grow.

**Provider-run aggregate.** Only the necessary statistic crosses the boundary. The recipient loses flexibility, and small groups, repeated releases, biased definitions, and unverifiable calculations can still disclose or mislead.

**Synthetic data.** Broad experimentation may be possible with reduced direct exposure. Utility, rare-case fidelity, memorization, bias, provenance, and inappropriate production use require validation.

**Clean room.** Joint computation and output rules can narrow direct access. Identity matching, query differencing, collusion, auxiliary information, privacy budgets, operator trust, billing, and derivative control remain.

**Trusted research environment.** Strong administrative, technical, and output-review boundaries can support sensitive work. Onboarding, researcher friction, reproducibility, cost, exit, and institutional trust increase.

**Open protocol.** Provider and consumer tooling can interoperate without one proprietary engine. Protocol conformance covers only defined messages; identity, semantics, service, policy, governance, and operations still need profiles.

**Single-platform exchange.** Provisioning, policy integration, and billing can be convenient. Vendor, region, account, feature, pricing, and exit dependencies concentrate.

**Central exchange operator.** Discovery, identity, contracts, evidence, and common controls can scale. The operator becomes a trust, availability, metadata, competition, cost, and governance concentration point.

**Federated consortium.** Parties retain more autonomy and share governance. Decision rights, conflict, funding, conformance, enforcement, membership change, and dissolution become multi-party systems problems.

**Contractual control after export.** Existing tools and recipient freedom remain. Enforcement becomes mainly organizational and remedial once plaintext copies leave the provider boundary.

**Technical control near the provider.** Preventive policy, revocation, minimization, and evidence improve. The recipient accepts less flexibility and more runtime dependence on provider or operator systems.

## Failure Modes and Misconceptions

1. **“A signed agreement makes the sharing architecture complete.”** Identity, semantics, controls, evidence, incidents, and closure remain.
2. **“Possession proves authority to share.”** Custody and disclosure authority are different facts.
3. **“The data owner is obvious.”** Collection, intellectual-property, privacy, stewardship, platform, and decision rights can differ.
4. **“One party name identifies every role.”** Providers, recipients, processors, operators, payers, and result receivers need distinct identities.
5. **“Affiliates are the same organization.”** Legal, administrative, regional, and control boundaries may differ.
6. **“A partner can choose its own subcontractors.”** Onward processors can change risk, region, and accountability.
7. **“A catalog listing proves approval.”** Discoverability is not authority, subscription, or access.
8. **“Subscription proves intended use.”** Access activation does not establish downstream purpose or outcome.
9. **“The purpose can be broad for future value.”** Unbounded purpose defeats minimization and meaningful review.
10. **“More data is safer than missing a field.”** Excess data increases exposure, ambiguity, and closure cost.
11. **“An encrypted transfer is a safe sharing design.”** Authority, endpoint identity, content, semantics, recipient use, and deletion remain.
12. **“A private network makes the partner trusted.”** Network location does not establish request or resource authorization.
13. **“A service account is enough attribution.”** Human, workload, organization, delegation, and purpose disappear.
14. **“Token exchange propagates revocation automatically.”** Input and output token lifecycles require deployment-specific coordination.
15. **“A long-lived bearer token is operationally simpler.”** Theft, replay, overbreadth, rotation, and offboarding risks expand.
16. **“Read-only means low risk.”** Reading can disclose, infer, copy, train, overload, and cause downstream harm.
17. **“Compatible schemas mean shared semantics.”** Population, keys, units, codes, time, nulls, and inclusion rules can differ.
18. **“A snapshot date identifies the data.”** Source versions, valid time, extraction, correction, and publication also matter.
19. **“A checksum proves data quality.”** It proves byte integrity relative to a named input, not correctness or fitness.
20. **“No-copy sharing moves no data.”** Query results, caches, spill, metadata, and client exports still cross boundaries.
21. **“Provider-side revocation deletes recipient copies.”** Future denial cannot retroactively erase uncontrolled plaintext.
22. **“Expiring a link closes the exchange.”** Cached files, credentials, notebooks, models, subscriptions, and backups remain.
23. **“Tokenized data is anonymous.”** Stable tokens preserve linkability and may be reversible or joinable.
24. **“Removing names de-identifies the dataset.”** Quasi-identifiers and auxiliary data can re-identify people or establishments.
25. **“Synthetic data contains no sensitive information.”** Models can memorize or expose source patterns and rare cases.
26. **“A clean room guarantees privacy.”** Configuration, queries, outputs, collusion, auxiliary data, and operator trust determine risk.
27. **“Minimum group size stops inference.”** Repeated and overlapping queries can reveal individuals by differencing.
28. **“A privacy budget is just a query quota.”** Formal composition depends on mechanism, parameters, adjacency, and accounting.
29. **“Approved SQL cannot leak.”** Predicates, errors, timing, joins, functions, and outputs can create channels.
30. **“Output review is merely manual approval.”** Review needs criteria, evidence, independence, consistency, and adversarial tests.
31. **“The platform enforces the agreement.”** Platform controls cover only modeled rules and actual enforcement points.
32. **“Machine policy is the legal agreement.”** Executable rules are a scoped translation and can omit context or remedies.
33. **“Deny-by-default resolves every conflict.”** It contains access but still needs escalation, correction, and availability handling.
34. **“Provider logs prove recipient compliance.”** They observe provider boundaries, not every downstream use.
35. **“Recipient attestation proves deletion.”** It is evidence with issuer, scope, method, timing, and assurance limits.
36. **“Lineage ends at delivery.”** Recipient transformations, models, reports, and decisions remain material derivatives.
37. **“Every derivative inherits identical rules.”** Applicability depends on transformation, agreement, policy, and authority and must be decided explicitly.
38. **“Correction means send a replacement file.”** Recipients must identify affected versions, uses, derivatives, and decisions.
39. **“An empty update means no correction.”** Empty, missing, delayed, rejected, and not-applicable states differ.
40. **“Contract renewal confirms technical compatibility.”** Schemas, identities, APIs, policies, and regions require separate tests.
41. **“Endpoint uptime is the service objective.”** Approval, freshness, completeness, interpretation, correction, and revocation matter.
42. **“The recipient always pays.”** Storage, egress, compute, privacy, support, and incidents may fall on different parties.
43. **“Usage volume measures collaboration value.”** Bytes and queries show activity, not benefit, equity, correctness, or harm.
44. **“A security incident belongs to the breached party.”** Shared assets, evidence, notification, containment, and remedy cross boundaries.
45. **“The contract contact is an incident channel.”** Operational response needs tested, secure, continuously staffed contacts and authority.
46. **“Deletion overrides legal hold automatically.”** Conflicting obligations need explicit decisions, segregation, evidence, and later action.
47. **“Termination is immediate everywhere.”** In-flight work, replicas, caches, credentials, derivatives, billing, and backups have separate clocks.
48. **“Recovery can restore the last working configuration.”** It may resurrect revoked parties, old rights, stale data, or closed routes.
49. **“Leaving an exchange removes every dependency.”** Identity trust, shared keys, copies, contracts, costs, and incident duties may remain.
50. **“Stopping transfer means sharing is closed.”** Existing data and derivatives can continue to be used unless reconciled and governed.

## Worked Examples

### Example 1

A retailer proposes sending all customer transactions to a logistics partner for delivery forecasting. The architecture instead shares daily region-product aggregates, excludes rare groups, bounds history, and records the forecasting purpose. Raw customer identity is unnecessary for the decision.

### Example 2

A hospital and university use a trusted research environment. Named researchers receive short-lived access to a versioned cohort; direct identifiers remain separate; query, export, and output review are recorded; the agreement identifies corrections, publications, model derivatives, incident contacts, and study closure.

### Example 3

A supplier API exchanges a subject token for a sender-constrained, audience-specific token. The receipt preserves supplier workload, employee subject, acting service, organization, purpose, contract version, resource, decision, and expiry. The supplier's private network alone grants nothing.

### Example 4

Two advertisers use a clean room for overlap counts. Approved templates enforce minimum groups and a formally configured privacy mechanism with composition accounting. Adversarial tests cover repeated subsets, auxiliary lists, colluding analysts, error channels, and result exports; a product label does not substitute for these tests.

### Example 5

A manufacturer publishes machine telemetry through an open table-sharing protocol. The sharing package identifies device population, units, calibration, valid time, firmware, corrections, snapshot version, service, and license. Protocol compatibility does not resolve those meanings.

### Example 6

A data marketplace listing is visible to hundreds of organizations. Subscription initiates identity, authority, purpose, region, contract, and payment checks. Only then does a recipient receive a scoped distribution. Listing view, subscription, access, delivery, use, and outcome remain distinct events.

### Example 7

A fraud consortium discovers a bad merchant-code mapping. A signed correction names affected asset versions and time range. Each member returns a receipt for replacement, quarantines affected derivatives, identifies decisions made from the faulty mapping, and records remediation gaps rather than merely downloading the new file.

### Example 8

A recipient exports shared rows into a model-training pipeline. The agreement requires derivative registration, so the model binds training snapshot, purpose, evaluation, retention, permitted deployments, and deletion behavior. Revoking table access does not pretend the trained model vanished.

### Example 9

A cross-region sharing feature silently introduces replication. Architecture tests expose the new storage location, keys, egress charges, recovery copy, deletion path, and legal review requirement. A metadata-only share in one region did not imply no-copy behavior everywhere.

### Example 10

A consortium dissolves. Members drain subscriptions, revoke identity federation and credentials, disable listings and query templates, reconcile exports and derivatives, settle charges, preserve disputes and incident evidence, remove recovery configuration, and prove that restoring an old backup does not reactivate access.

## Cross-Program Connections

- [Data Engineering](../../19-data-engineering/ROADMAP.md) owns reliable production of distributions, change streams, quality evidence, correction flows, lineage emission, retention, and deletion execution.
- [Large-Scale Data Systems Engineering](../../21-large-scale-data-systems-engineering/ROADMAP.md) owns shared-table engines, replication, clean-room compute, isolation, quotas, scheduling, caching, scale, and storage behavior.
- [Database Engineering](../../18-database-engineering/ROADMAP.md) owns schemas, constraints, snapshots, query controls, statistics, transaction boundaries, views, and source protection.
- [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) owns purpose-specific interfaces, identity propagation, token handling, authorization, rate limits, idempotency, errors, streaming, compatibility, and service objectives.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md) owns self-service exchanges, tenant boundaries, identity integration, policy enforcement points, secrets, observability, billing, support, and recovery.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) owns threat modeling, zero trust, cryptography, least privilege, detection, egress, incident response, and security assurance.
- [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md) owns service boundaries, trust interfaces, adapters, contracts, compatibility, dependency direction, and evolution.
- [Network Engineering](../../24-network-engineering/ROADMAP.md) owns endpoint reachability, DNS, TLS, private connectivity, segmentation, bandwidth, cross-region paths, and transport diagnosis.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies reasoning about identity, partial failure, retries, ordering, snapshots, cancellation, evidence, and recovery across independent parties.
- [Systems Engineering](../../26-systems-engineering/ROADMAP.md) supplies stakeholder, assurance, hazard, interface, lifecycle, trade-space, incident, and emergent-risk reasoning.

## References

1. NIST, [Using Privacy Framework 1.1](https://www.nist.gov/privacy-framework/using-privacy-framework-11), privacy risk management across the data processing ecosystem.
2. NIST, [SP 800-207: Zero Trust Architecture](https://csrc.nist.gov/pubs/sp/800/207/final), resource-focused authentication, authorization, and trust principles.
3. NIST, [SP 800-188: De-Identifying Government Datasets](https://csrc.nist.gov/pubs/sp/800/188/final), de-identification techniques, governance, and disclosure risk.
4. NIST, [Cybersecurity Framework 2.0](https://www.nist.gov/cyberframework), Govern, Identify, Protect, Detect, Respond, and Recover outcomes.
5. NIST, [SP 800-61 Revision 3](https://csrc.nist.gov/pubs/sp/800/61/r3/final), incident response within cybersecurity risk management.
6. W3C, [Data Catalog Vocabulary 3](https://www.w3.org/TR/vocab-dcat-3/), catalogs, datasets, distributions, services, versions, rights, and policies.
7. W3C, [ODRL Information Model 2.2](https://www.w3.org/TR/odrl-model/), parties, assets, permissions, prohibitions, duties, constraints, and remedies.
8. W3C, [PROV Overview](https://www.w3.org/TR/prov-overview/), provenance entities, activities, agents, and supporting specifications.
9. IETF, [RFC 8693: OAuth 2.0 Token Exchange](https://www.rfc-editor.org/info/rfc8693/), token exchange, delegation, impersonation, subject, and actor.
10. IETF, [RFC 9700: Best Current Practice for OAuth 2.0 Security](https://www.rfc-editor.org/info/rfc9700/), current OAuth security threats and recommendations.
11. Delta Lake, [Delta Sharing](https://docs.delta.io/delta-sharing/), an open protocol for table snapshots, changes, and streaming access.
12. Amazon Web Services, [What Is AWS Clean Rooms?](https://docs.aws.amazon.com/clean-rooms/latest/userguide/what-is.html), collaboration membership, configured data, analysis, and output controls.
13. Snowflake, [About Secure Data Sharing](https://docs.snowflake.com/en/user-guide/data-sharing-intro), providers, consumers, shares, listings, exchanges, and clean rooms.
14. Google Cloud, [Introduction to BigQuery Sharing](https://cloud.google.com/bigquery/docs/analytics-hub-introduction), exchanges, listings, publishers, subscribers, linked datasets, and usage.
15. OpenLineage, [Object Model](https://openlineage.io/docs/spec/object-model/), datasets, jobs, runs, events, and facets for operational lineage.
16. Bitol, [Open Data Contract Standard](https://bitol-io.github.io/open-data-contract-standard/latest/), machine-readable schema, quality, service, role, support, and infrastructure contracts.

## Exercises

### Exercise 1

Design a bilateral sharing package for a provider and research institution using sensitive longitudinal data. Define outcome, affected parties, authority, asset identity, semantics, minimization, delivery pattern, agreement, identity, privacy, security, provenance, service, incident, remedy, derivatives, and closure.

### Exercise 2

Compare managed file, event subscription, API, shared table, federated query, provider-run aggregate, synthetic data, clean room, trusted research environment, and no sharing for one cross-organization use. Make persistence, freshness, inference, recipient flexibility, source protection, portability, cost, and revocation boundaries explicit.

### Exercise 3

Specify federated identity and authorization for a request that crosses an exchange operator and provider. Cover issuers, organization, subject, actor, delegation, audience, scope, resource, purpose, workload, token binding, expiry, revocation, policy decisions, evidence, and emergency access.

### Exercise 4

Threat-model a clean-room collaboration. Include identity resolution, malicious and colluding members, auxiliary data, repeated and overlapping queries, errors, timing, minimum groups, formal privacy accounting, outputs, models, logs, operator compromise, incidents, and deletion.

### Exercise 5

Plan termination of a five-party data consortium. Inventory identities, agreements, listings, shares, subscriptions, files, replicas, caches, models, reports, decisions, keys, logs, incidents, disputes, costs, backups, legal holds, attestations, and recovery paths.

## Answers to the Exercises

### Answer 1

Name the exact research outcome, population, users, affected people, benefit, harm, alternatives, and end date. Prove collection, use, and disclosure authority for a stable asset and named parties. Publish fields, grain, keys, meanings, valid and observation time, provenance, quality, corrections, and residual uncertainty. Minimize records, attributes, precision, history, frequency, and duration. Choose a provider-run computation or controlled environment if raw export is unnecessary. The agreement covers purpose, permissions, prohibitions, duties, processors, regions, publication, models, service, cost, incident, remedy, change, and termination. Federated identities and short-lived scoped credentials preserve subject and actor. Test linkage, output, transport, isolation, audit, correction, and deletion. Register derivatives and receipts. Closure drains work, revokes every access path, reconciles copies and models, applies holds, preserves evidence, and tests recovery nonactivation.

### Answer 2

Build a trade matrix against the use rather than choosing from product labels. Files maximize portability and recipient control but create durable copies. Events improve freshness but accumulate state and replay duties. APIs retain provider policy while adding runtime coupling. Shared tables simplify analytical access but expose query and platform dependencies. Federation avoids planned copies but creates distributed semantic and failure risk. Provider aggregates minimize disclosure but reduce flexibility. Synthetic data needs privacy and utility evaluation. Clean rooms constrain computation and outputs but retain inference and operator risk. Trusted environments add administrative and output control at higher friction and cost. No sharing wins when authority, purpose, safety, semantics, remedy, or closure cannot be made adequate. State exactly what revocation stops for each pattern and what persists afterward.

### Answer 3

Trust only configured issuers and bind each external organization to reviewed tenant identity and lifecycle. Authenticate the requesting subject and acting workload separately. Use explicit delegation rather than ambiguous impersonation. Exchange for a short-lived sender-constrained token whose audience, resource, scope, purpose, organization, subject, actor, and expiry match the provider endpoint. The operator cannot widen rights and the provider independently evaluates agreement, asset, action, fields, rows, region, posture, rate, and duties. Rotate credentials, prevent replay and confused-deputy use, propagate revocation through a designed mechanism, and preserve emergency-access policy. Correlate request, token identifiers or safe digests, issuer, delegation, policy versions, decision, enforcement, result, and limitations without logging raw secrets or sensitive data.

### Answer 4

Model provider, recipient, analyst, result receiver, payer, operator, identity matcher, cloud administrator, and colluding members. Test false and adversarial matches, rare cohorts, auxiliary lists, overlapping subsets, repeated queries, differencing, predicates, functions, errors, timing, aborted runs, cached results, exports, screenshots, and model leakage. Approved templates and minimum groups are only layers. If differential privacy is used, define adjacency, mechanism, parameters, composition, budget owner, exhaustion, and reset rather than substituting a query count. Restrict member roles and outputs, isolate keys and compute, minimize logs, and test operator compromise. Receipts bind inputs, versions, templates, policies, budget, execution, receiver, and export. Joint incident and deletion workflows cover inputs, temporary state, results, models, logs, and residual uncertainty.

### Answer 5

Freeze new memberships and changes, notify accountable and operational contacts, and establish a signed termination ledger. Drain in-flight requests and subscriptions. Revoke issuer trust, tokens, service accounts, memberships, listings, shares, endpoints, presigned URLs, encryption keys, and renewal automation. Each party inventories files, replicas, tables, event state, caches, notebooks, features, models, reports, decisions, subprocessors, and onward recipients. Apply deletion, return, restriction, correction, or legal hold per asset and derivative, recording scope and assurance of attestations. Settle billing, licenses, publications, open incidents, remedies, and disputes. Preserve minimum required evidence with controlled access and expiry. Remove dormant network, policy, and recovery configuration, restore a representative backup in isolation, and prove that terminated parties and routes do not reactivate.
