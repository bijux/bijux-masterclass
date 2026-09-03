---
module_id: DARCH-075
program: Data Architecture Engineering
level: 2
module_number: 75
title: Data Residency and Sovereignty
status: complete
last_verified: 2026-09-03
---

# Data Residency and Sovereignty

## One-Page Review

### Governing question

How should a data architecture discover, decide, enforce, and prove where data is stored, processed, accessed, transferred, administered, backed up, and recovered—and which authorities and operators can exercise power over it—without confusing a cloud region label with legal compliance or operational sovereignty?

### Essential definitions

- **Data location** is an evidenced fact about where a particular data representation or processing event exists at a specified time and granularity.
- **Data residency** is a requirement or commitment governing locations in which defined data and operations may occur.
- **Data localization** is an applicable rule requiring some or all data, processing, control, or copies to remain within a specified territory; its exact strength must be stated rather than inferred from the label.
- **Data sovereignty** concerns the legal, organizational, technical, and operational authorities that can control or compel access to data and services; physical location is only one dimension.
- A **jurisdiction profile** is a versioned interpretation of applicable authorities, territorial and extraterritorial reach, sector rules, transfer conditions, government-access risk, and review triggers for a defined activity.
- A **residency profile** converts approved requirements into explicit allowed and prohibited locations for asset classes, operations, actors, keys, replicas, recovery, and lifecycle states.
- A **location claim** states the country, territory, provider geography, region, zone, facility, logical boundary, source, time, and confidence for an asset or event.
- A **transfer** is a governed disclosure, movement, or making-available event across a defined legal or policy boundary; remote access can be a transfer even when stored bytes do not move.
- A **data boundary** is an engineered scope within which specified data, operations, identities, administration, and dependencies are intended to remain under stated controls.
- **Operational sovereignty** is the demonstrated ability to operate, secure, recover, update, investigate, and exit a service under approved personnel, organizations, dependencies, and decision rights.
- **Technical sovereignty** is the demonstrated ability to understand, control, replace, and migrate critical technical components and interfaces under defined conditions.
- A **transfer mechanism** is an approved legal or policy instrument for a particular flow; it is not evidence that every destination law, safeguard, purpose, or onward transfer is acceptable.
- A **transfer assessment** evaluates the actual flow, parties, destination, authority, data, purpose, safeguards, access risk, enforceability, and residual risk at a specified time.
- A **placement decision** resolves a residency profile against an asset, operation, actor, dependency, availability objective, and current provider capability.
- **Proof of residency** is corroborated evidence about actual placement and access over time, not merely a requested configuration or contract clause.
- **Closure** removes active data, replicas, exports, credentials, keys, support paths, transfer mechanisms, exceptions, and recovery routes while preserving the minimum evidence required to explain past decisions.

### Central model, mechanism, or theorem

Represent residency and sovereignty governance as:

`R = (A, J, D, P, T, X, C, E, O, L)`

where `A` is applicability and authority, `J` jurisdiction profiles, `D` governed data and representations, `P` placement and processing locations, `T` transfers and onward flows, `X` actors and access paths, `C` technical, contractual, and organizational controls, `E` evidence and uncertainty, `O` operations and resilience, and `L` lifecycle and closure. A placement is fit only when the applicable profile, real asset plane, operation, location, actors, provider entity, dependencies, key control, transfer basis, recovery path, and observed evidence all agree.

### Critical invariants

- Requirement, interpretation, asset, copy, operation, location, actor, legal entity, transfer, assessment, safeguard, exception, decision, and observation have stable separate identities.
- Country, territory, provider geography, region, availability zone, facility, network endpoint, tenant boundary, and legal jurisdiction are not interchangeable.
- Customer content, derived data, indexes, caches, logs, telemetry, metadata, support records, keys, models, backups, and deletion residue are inventoried separately.
- Storage, computation, transit, remote access, administration, support, monitoring, failover, recovery, export, and deletion are independently constrained.
- A provider region selection is a requested configuration; actual scope, exceptions, global services, personnel access, subprocessors, and recovery behavior require evidence.
- No workload may self-assert a less restrictive residency profile or choose an arbitrary destination.
- Transfer mechanisms and adequacy status are versioned, scoped, reviewable inputs rather than permanent properties of a country.
- Encryption changes exposure only under explicit key, identity, runtime, metadata, and compelled-access assumptions; it does not move data or erase jurisdiction.
- Availability design does not silently cross a prohibited boundary, and residency controls do not silently eliminate required resilience.
- Unknown, mixed, stale, conflicting, unsupported, and unverified placement state fail visibly for restricted processing.
- Runtime policy, network and identity controls, provider configuration, and downstream contracts enforce the same approved decision.
- Recovery and closure cannot reactivate prohibited copies, expired exceptions, obsolete mechanisms, or unauthorized access paths.

### Common failures

Common failures include treating residency, localization, and sovereignty as synonyms; assuming a region name proves a country; inventorying only primary databases; ignoring logs, metadata, keys, caches, models, and backups; treating remote support as non-transfer because bytes stay at rest; assuming encryption eliminates jurisdiction; allowing global control-plane services into a local boundary; enabling cross-region replication by default; letting failover override policy during an incident; recording country only at dataset level; accepting vendor marketing as proof; using contracts without technical enforcement; using technical controls without lawful authority; allowing workloads to self-label location; caching transfer assessments indefinitely; overlooking subprocessors and corporate entities; measuring configured resources rather than observed processing; and restoring a prohibited replica from backup.

### Compact example

Ten invented placements are evaluated against three declared profiles. Four local placements and one assessed transfer are permitted. One placement violates location, one violates personnel access, one has unknown location, one lacks required key control, and one transfer has a stale assessment. Four countries, three personnel jurisdictions, eight asset planes, and ten decision events are counted. Executable evidence confirms only those declarations. It proves no real geography, legal applicability, provider behavior, government-access protection, key exclusivity, transfer validity, operational autonomy, or beneficial outcome.

### Connections

[DARCH-064](064-lineage-architecture.md), [DARCH-069](069-metadata-apis-and-eventing.md), [DARCH-072](072-policy-as-code-for-data.md), [DARCH-073](073-classification-architecture.md), and [DARCH-074](074-consent-and-purpose-limitation.md) establish provenance, interfaces, executable policy, classification, purpose, and authority. [DARCH-076](../ROADMAP.md) next develops retention and legal hold.

## Governing Question

An application can store its primary database in Frankfurt while sending logs to a global service, copying backups to another country, allowing support from several jurisdictions, using keys controlled by a foreign parent, training a model elsewhere, and failing over across a prohibited boundary. “Hosted in Europe” cannot describe this system.

The governing question is how to turn legal, contractual, sector, customer, and organizational requirements into precise constraints across every representation and operation. A durable architecture connects applicability to real data flows, prevents invalid placements before provisioning, observes what actually happened, handles lawful transfer and compelled-access risk, and preserves service continuity without making claims stronger than its evidence.

## Why This Matters

The European Union's [General Data Protection Regulation](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32016R0679) makes international-transfer conditions apply to transfers and onward transfers of personal data covered by Chapter V. It provides several mechanisms and limited derogations rather than a universal rule that personal data must remain in one country. Architecture must therefore model applicability, parties, flow, destination, mechanism, safeguards, and review instead of encoding `EU-only` as a complete legal answer.

The European Data Protection Board's final [Recommendations 01/2020 on supplementary measures](https://www.edpb.europa.eu/documents/recommendation/recommendations-012020-on-measures-that-supplement-transfer-tools-to_en) describe a process for mapping transfers, identifying transfer tools, assessing destination law and practice, adopting supplementary measures, completing procedural steps, and reevaluating. The precise legal test belongs to qualified reviewers. Architecturally, inventories and controls must cover onward transfers and actual access, not only declared storage.

The European Commission's [standard contractual clauses for international transfers](https://commission.europa.eu/publications/standard-contractual-clauses-international-transfers_en) provide approved contractual modules for specified exporter-importer relationships. Clauses are scoped instruments, not a global location policy, and contract execution does not prove technical enforcement or eliminate assessment duties.

The Court of Justice of the European Union's [judgment in Case C-311/18](https://curia.europa.eu/juris/document/document.jsf?text=&docid=228677&pageIndex=0&doclang=EN) addressed transfers, standard clauses, destination-country public-authority access, effective protection, and supervisory powers. It demonstrates why a transfer mechanism cannot be evaluated apart from the legal and practical environment in which data becomes accessible.

The UK Information Commissioner's Office's current guidance on [completing a transfer risk assessment](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/international-transfers/completing-a-transfer-risk-assessment/) describes risks from third-party access in the destination and difficulty enforcing safeguards. It was updated in January 2026 to reflect UK terminology. UK analysis and EU analysis are not interchangeable; the architectural lesson is to attach every assessment to authority, method, version, destination, facts, and expiry.

The EU [Data Act](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32023R2854) includes provisions addressing conflicting international or third-country governmental access and transfer of certain non-personal data held in the Union by data-processing service providers. Residency architecture can therefore concern non-personal, industrial, public-sector, or commercially sensitive data as well as personal data.

The OECD [Declaration on Government Access to Personal Data Held by Private Sector Entities](https://legalinstruments.oecd.org/api/print?ids=693&lang=en) identifies common principles involving legal basis, legitimate aims, approvals, data handling, transparency, oversight, and redress. It also recognizes that authority can reach an entity or data outside the requesting state's territory. Physical storage location alone cannot prove immunity from compelled access.

NIST [SP 800-53 Release 5.2.0](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final) includes controls for external services, processing and storage location, organization-controlled keys, system use, information flow, contingency, supply chain, and privacy. Its location enhancement ties processing, data, and service placement to organization-defined requirements. A control catalog still requires system-specific selection, implementation, assessment, and evidence.

Kubernetes documents well-known [`topology.kubernetes.io/region` and `topology.kubernetes.io/zone` labels](https://kubernetes.io/docs/reference/labels-annotations-taints/#topologykubernetesioregion). These labels express provider-specific scheduling topology and failure domains; they do not establish country, jurisdiction, legal entity, support path, or residency compliance. Placement systems need a governed mapping from runtime topology to approved location claims.

AWS guidance on [hybrid architectures for personal-data processing requirements](https://docs.aws.amazon.com/whitepapers/latest/hybrid-architectures-to-address-personal-data-processing-requirements/actions-recommendations-and-best-practices.html) states provider-specific regional behavior and describes customer responsibility for chosen movement and architecture. Such statements are useful provider evidence but remain service-, feature-, account-, contract-, and time-specific.

Microsoft's [Sovereign Public Cloud controls and principles](https://learn.microsoft.com/en-us/azure/azure-sovereign-clouds/public/overview-controls-principles) distinguish regional services from global services and describe residency, key, confidential-computing, personnel, and operational controls. The documentation explicitly warns that service availability in a region does not alone establish all data-handling characteristics.

Google Cloud's [Assured Workloads data residency guidance](https://docs.cloud.google.com/assured-workloads/docs/data-residency) distinguishes customer data at rest, service data, resource-location policy, supported resources, and unrestrictable services. It shows why boundary assurance needs asset-plane and service coverage, not a folder name alone.

Together these sources support a layered architecture: authoritative interpretation, complete flow inventory, typed location and access claims, placement policy, provider capability, technical enforcement, contractual and organizational measures, observed evidence, continuous reassessment, resilient recovery, and honest limitations.

## Prerequisites and Retrieval

You should understand privacy and data protection, jurisdiction, cross-border transfer, contracts, government access, data classification, purpose limitation, lineage, cloud regions and zones, distributed storage, replication, encryption and key management, identity, networking, policy as code, observability, disaster recovery, incident response, vendor management, migration, and lifecycle governance.

Retrieve controller, processor, exporter, importer, subprocessor, legal entity, establishment, territory, country, jurisdiction, geography, region, zone, facility, residency, localization, sovereignty, data boundary, transfer, onward transfer, remote access, compelled access, adequacy, safeguard, assessment, encryption, pseudonymization, key custody, support path, control plane, data plane, management plane, telemetry, replica, backup, failover, recovery, exception, attestation, observation, drift, and closure.

As a retrieval test, inspect `region = eu-west`. Ask which provider and service define it; which countries and facilities it covers; whether the value is configuration, observation, or contract; which content, metadata, logs, keys, replicas, support records, and backups follow it; where computation, administration, and failover occur; which legal entities and personnel can access it; which rules apply to each data subject and purpose; whether remote access or onward flow is a transfer; and what evidence proves current placement. The label alone answers none of these questions.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish physical and logical location, residency, localization, sovereignty, jurisdiction, transfer, remote access, and operational control;
2. derive versioned residency profiles from applicable legal, contractual, sector, customer, security, resilience, and organizational requirements;
3. inventory customer content, derived data, metadata, telemetry, keys, models, caches, replicas, backups, support data, and deletion residue;
4. model countries, territories, provider geographies, regions, zones, facilities, entities, personnel, services, subprocessors, and confidence without semantic collapse;
5. evaluate transfers and onward access using scoped mechanisms, assessments, supplementary controls, exceptions, and review triggers;
6. compile placement policy into provisioning, scheduling, identity, network, storage, encryption, replication, egress, and recovery controls;
7. reconcile declared configuration, contracts, provider capabilities, runtime observations, and downstream attestations;
8. design availability, failover, incident, and recovery behavior that respects location constraints without hiding resilience loss;
9. operate metrics, evidence, exceptions, migration, correction, and closure across multi-cloud and hybrid estates; and
10. identify the limits of residency controls and evaluate broader legal, human-rights, security, competition, portability, and operational outcomes.

## Core Exposition

**Begin with applicability, not a map.** Identify the organization, establishments, people, data, sector, purpose, contracts, public obligations, destinations, and operations that cause rules to apply. Country of storage can be relevant without being the only connecting factor.

Record the authority, interpreter, scope, effective time, assumptions, conflicts, decision, and next review. Architecture consumes an authorized interpretation; it does not invent law from region names.

**Separate requirement from implementation.** A requirement such as “specified records and their disaster-recovery copies must remain in territory T” is different from a cloud configuration, scheduler constraint, firewall rule, contract term, or attestation.

Link requirements to implementations and observations so each can change without rewriting history.

**Define boundary semantics precisely.** State whether a rule concerns country, group of countries, customs territory, political subdivision, provider geography, named facilities, organization-controlled premises, or a logical tenant.

Define inclusion and exclusion. “Europe,” “EU,” “EEA,” and a vendor's European geography can denote different sets.

**Distinguish residency, localization, and sovereignty.** Residency constrains location. Localization may require a local copy, local processing, exclusive local retention, or local control depending on the authority. Sovereignty adds authority, compelled access, ownership, personnel, operations, technology, and exit.

Never claim sovereignty from residence alone. A local facility can be operated by a foreign entity, rely on a global control plane, or be irrecoverable without remote personnel.

**Model multiple jurisdictions.** An activity can implicate the data subject's location, controller and processor establishments, contracting entities, service-provider parent, operator location, storage site, processing site, destination, and sector authority.

Preserve conflicts and unknowns. A single `jurisdiction` column discards the relationships that make analysis possible.

**Inventory every asset plane.** Include primary content, attachments, derived tables, indexes, search vectors, feature stores, training and evaluation sets, model weights, prompts and outputs, caches, queues, change logs, audit logs, traces, metrics, crash dumps, support bundles, identity attributes, billing records, keys, secrets, replicas, snapshots, archives, and deletion journals.

Classify each plane by subject, sensitivity, purpose, owner, retention, location behavior, and applicable profile. “Operational metadata” is not automatically harmless or out of scope.

**Inventory every operation.** Storage at rest is only one operation. Model collection, ingestion, validation, transformation, query, inference, training, routing, transit, remote display, administration, support, troubleshooting, monitoring, export, disclosure, replication, failover, restore, deletion, destruction, and legal preservation.

An operation can create a regulated transfer or exposure without creating a durable destination copy.

**Represent location as evidence.** A useful claim states asset or event, operation, provider, service, account, resource, country, territory, geography, region, zone, facility if known, source, observation method, observed time, valid interval, confidence, and limitations.

Do not fabricate facility precision from a regional API. Unknown is a valid result and may block restricted use.

**Separate requested, declared, observed, and inferred location.** Infrastructure code requests a region. A provider API declares resource configuration. Network or service evidence observes behavior. A mapping infers country or jurisdiction.

Store each evidence type and reconcile disagreement. Repeating the configured value in a dashboard does not create independent assurance.

**Govern location vocabularies.** Give countries, territories, geographies, regions, zones, facilities, and logical boundaries stable identifiers with source and valid time. Map provider topology to territorial concepts explicitly.

Country codes do not encode contested status, sector interpretation, facility location, or legal applicability. Preserve the profile that interpreted them.

**Create residency profiles.** A profile states covered data classes and subjects, purposes, allowed and prohibited locations by operation, permitted actors and entities, remote-access rules, transfer mechanisms, key requirements, provider capabilities, retention, availability, failover, recovery, evidence, review, and exception policy.

Profiles are governed objects, not caller strings. A workload references an approved profile version through trusted metadata.

**Resolve at the smallest governable scope.** Dataset-level policy can be too coarse when rows concern different subjects or contracts. Row-level routing can be too complex and can leak through joins, indexes, and operations.

Choose a partition boundary that preserves enforcement, query semantics, deletion, resilience, and evidence. Split incompatible populations when safe mixed processing cannot be proved.

**Treat transfers as typed relationships.** Identify exporter, importer, controller and processor roles, data and subjects, purpose, operations, destination, onward recipients, mechanism, assessment, safeguards, effective interval, incidents, and termination.

A contract with one vendor does not authorize every service, affiliate, subprocessor, destination, or purpose.

**Assess actual access.** Support sessions, administrator consoles, replicated memory, diagnostic bundles, content-delivery systems, threat detection, telemetry, and managed-service operations can create relevant access paths.

Model who can make data intelligible, under which identity, from where, for what reason, with whose approval, through which system, and with what receipt.

**Evaluate government-access and conflict risk.** Tie analysis to destination law and practice, provider entities, data and encryption, key control, public-authority powers, safeguards, enforceability, transparency, oversight, redress, and current evidence.

Do not reduce this work to a country color. Different data, services, parties, protections, and time periods can produce different decisions.

**Use transfer mechanisms precisely.** Adequacy, standard clauses, binding rules, certifications, codes, agreements, or exceptions have distinct scopes and conditions under applicable regimes.

Record the exact instrument, module, parties, dates, attachments, assessment, supplementary measures, termination, and review. Expiry or legal change invalidates cached decisions.

**Apply supplementary controls as assumptions.** Encryption can reduce intelligibility when algorithms, endpoints, identities, key custody, runtime, metadata, backups, and compelled-access conditions support that conclusion. Pseudonymization depends on separation and reidentification capability.

Customer-managed keys are not necessarily customer-exclusive keys. A provider-mediated key service, accessible application runtime, or support role may still expose plaintext.

**Control placement before creation.** Admission policy should reject unapproved regions, services, replicas, global resources, network routes, identities, and key locations before data arrives.

Guard accounts, projects, subscriptions, clusters, namespaces, catalogs, pipelines, databases, object stores, queues, analytics, AI services, observability, and backup products. Defaults should be safe for the profile.

**Bind purpose and residency.** The same dataset may be allowed in one location for service delivery and prohibited there for research, model training, or disclosure. Carry purpose, basis, subject scope, and profile version into policy decisions.

Location is not a substitute for purpose limitation or authorization.

**Constrain compute and memory.** A local database queried by foreign compute can expose data outside the storage boundary. Bind processing jobs, serverless functions, notebooks, inference endpoints, temporary volumes, swap, and memory dumps to allowed topology.

Verify that schedulers and managed services actually support the required constraint; a preferred-affinity hint is not a hard boundary.

**Constrain identity and personnel.** Residency policy can require local, cleared, screened, or organization-controlled operators. Enforce approved workforce identities, device posture, just-in-time access, dual control, purpose, session recording, export limits, and revocation.

Personnel citizenship, residence, employer, access location, and legal authority are separate attributes. Use only authorized criteria and review human-rights and employment implications.

**Constrain networks and egress.** Deny unapproved public endpoints, cross-region service calls, replication links, observability exporters, package callbacks, webhook destinations, and support tunnels. Resolve DNS, proxies, content delivery, and service endpoints under the same model.

Network controls observe endpoints, not necessarily legal entities or data meaning. Combine them with identity, service, workload, and data context.

**Constrain keys and secrets.** State where key material, wrapping keys, HSM operations, backups, administrators, recovery shares, and audit data may exist. Separate customer-managed, customer-controlled, customer-held, and externally held keys.

Plan rotation, loss, emergency use, provider outage, migration, deletion, and legal demand. Exclusive keys can increase sovereignty while also increasing unrecoverable-loss risk.

**Inspect global and nonregional services.** Identity, DNS, billing, policy, support, threat intelligence, package registries, and control planes may be global even when a data service is regional.

Determine which data each service handles and whether exclusions are technically and contractually supported. A global service is not automatically forbidden, but its scope cannot be hidden.

**Govern subprocessors and supply chains.** Record provider legal entities, affiliates, subprocessors, facilities, support organizations, network carriers, software dependencies, and change-notification terms.

Evaluate new recipients and destinations before activation. Contract notice without an operational block can allow an invalid change to precede review.

**Design resilience within constraints.** Determine required failure independence, recovery point, recovery time, availability, integrity, and safety. Find compliant zones, regions, providers, or local facilities that satisfy them.

If no design satisfies both policy and resilience, expose the conflict to authorized decision makers. Do not silently choose availability or residency.

**Make failover policy aware.** Precompute allowed failover destinations and required controls. During an incident, verify current approval, profile, destination health, transfer mechanism, key path, and expiry before moving data.

Emergency exceptions require authority, bounded scope, time, evidence, notification, containment, and exit. “Break glass” is not unlimited geography.

**Make backups first-class.** Track snapshot creation, deduplication, media, vault, key, replica, immutability, operator, restore environment, expiry, and destruction. A backup can outlive the rule or recreate a prohibited placement.

Recovery rehearsals must verify current policy before restore, replay corrections and deletions, and close transient resources afterward.

**Control derived data and models.** Aggregates, embeddings, features, weights, checkpoints, evaluation samples, and synthetic outputs require evidence-based classification. Derivation does not automatically remove residency or sovereignty duties.

Record inputs, transformations, privacy tests, possible subjects, purpose, recipients, training and inference locations, deletion limitations, and reuse constraints.

**Provide a placement decision API.** Accept authenticated workload, asset, subject and contract scope, classification, purpose, operation, proposed service and location, actors, availability need, and time. Return decision, profile and rule versions, allowed alternatives, obligations, expiry, and protected explanation.

Make retries idempotent and policy changes observable. Do not leak sensitive classification or legal reasoning in broad error messages.

**Publish immutable events.** Emit requirement, profile, provider-capability, placement, transfer, access, drift, exception, failover, recovery, and closure events with effective and record time.

Consumers deduplicate, preserve causation, reject rollback, and reconcile gaps. An event is evidence of publication, not proof that every resource changed.

**Continuously reconcile reality.** Compare catalog and lineage, infrastructure declarations, provider inventory, configuration APIs, runtime telemetry, network flow, identity sessions, key logs, contracts, subprocessors, backups, and downstream attestations.

Open incidents for unknown, conflicting, stale, or prohibited state. Reconciliation coverage needs a denominator of expected assets and operations.

**Protect sovereignty evidence.** Location, government-access analysis, operator sessions, exceptions, and transfer records can expose security architecture, personal data, investigations, and commercial relationships.

Minimize, partition, encrypt, authorize, retain, and audit the evidence. Evidence protection must not make independent assessment impossible.

**Measure decisions and effects.** Track governed assets, located assets, independently corroborated claims, unsupported services, prevented provisions, prohibited observations, transfer assessments, upcoming expiries, subprocessor changes, access sessions, failovers, exceptions, recovery tests, and closure.

Separate configured compliance from observed compliance. Report unknown and excluded populations, not just success percentages.

**Correct history without rewriting it.** When a location mapping or legal interpretation was wrong, preserve the old claim and decision, issue corrected versions, contain affected processing, identify transfers and recipients, notify authorities and people where required, migrate or delete data, and verify remediation.

Changing a dashboard label does not repair past access or placement.

**Engineer portability and exit.** Sovereignty includes the ability to export usable data and metadata, reproduce controls, transfer keys where permitted, replace dependencies, validate completeness, revoke provider access, and delete residual copies.

Test exit before an emergency. Proprietary services, undocumented metadata, egress time, key coupling, and unavailable skills can turn formal portability into fiction.

**Close deliberately.** Stop new writes and transfers, drain workloads, export required records, expire identities and exceptions, destroy active and backup copies under policy, revoke keys and routes, terminate mechanisms and contracts, obtain provider evidence, and test that recovery cannot reactivate the boundary.

Retain only the minimum decision, transfer, incident, and destruction evidence required under separately authorized controls.

## Definitions and Notation

Let `a` denote an applicability decision, `j` a jurisdiction profile, `d` a governed data representation, `o` an operation, `l` a location claim, `x` an actor or access path, `t` a transfer relationship, `c` a control set, `e` evidence, and `q` a resilience requirement.

Define a residency profile as:

`P = (D, O, L+, L-, X+, X-, K, T, Q, E, V)`

where `D` is covered data, `O` governed operations, `L+` allowed locations, `L-` prohibited locations, `X+` approved actors, `X-` prohibited actors, `K` key and intelligibility conditions, `T` transfer rules, `Q` resilience and recovery constraints, `E` required evidence, and `V` authority, version, and validity.

A location claim is:

`L(d, o, τ) = (country, territory, geography, region, zone, facility, provider, service, source, confidence)`

at time `τ`. Components may be unknown. Absence of facility evidence must not be filled from region marketing.

A placement decision can be expressed as:

`permit(d, o, l, x, τ) = applicable(P, d, o, τ) ∧ location_ok(P, l, o) ∧ actor_ok(P, x, o) ∧ key_ok(P, d, o) ∧ transfer_ok(P, t, τ) ∧ resilience_ok(P, q) ∧ evidence_fresh(P, e, τ)`

This is an architectural predicate, not a legal theorem. Each function depends on authorized profiles and evidence.

A transfer record is:

`T = (exporter, importer, roles, data, subjects, purpose, operations, destination, onward, mechanism, assessment, safeguards, interval)`

Transfer validity is scoped to this tuple. Reusing one element does not authorize a different transfer.

A sovereignty capability vector is:

`S = (legal_control, data_control, identity_control, key_control, operator_control, technical_control, recovery_control, exit_control)`

The vector prevents a single maturity label from hiding a weak dimension. It is a review model, not a universal score.

Define observed placement coverage for a window as:

`coverage = corroborated_in_scope_assets / expected_in_scope_assets`

The denominator includes missing inventory. Assets excluded by approved scope are reported separately.

Define prohibited exposure rate as:

`exposure_rate = confirmed_prohibited_access_or_placement_events / observed_governed_operations`

Zero observed events does not prove zero exposure when observation coverage is incomplete.

## Mechanisms, Invariants, or Proof Structure

A residency control plane should implement the following assurance gates.

**Applicability gate.** Identify organizations, establishments, subjects, sectors, contracts, authorities, purposes, data, operations, territories, and review owners.

**Interpretation gate.** Create approved, versioned requirements with assumptions, conflicts, legal or policy basis, effective time, and expiry.

**Inventory gate.** Enumerate data planes, copies, transformations, models, metadata, logs, keys, identities, providers, subprocessors, routes, and recovery assets.

**Vocabulary gate.** Govern countries, territories, provider geographies, regions, zones, facilities, entities, services, operation types, and evidence sources.

**Profile gate.** Bind data and operations to allowed and prohibited locations, actors, access, key conditions, transfers, resilience, evidence, and exceptions.

**Assessment gate.** Evaluate actual exporters, importers, destination law and practice, mechanisms, safeguards, government access, onward flows, enforceability, residual risk, and review date.

**Capability gate.** Verify that each provider, service, feature, region, support model, control plane, backup, and key system can implement the profile.

**Provisioning gate.** Reject invalid accounts, projects, resources, regions, services, replicas, endpoints, identities, and keys before data use.

**Runtime gate.** Enforce operation, workload, purpose, identity, network, compute, storage, egress, support, and session constraints on real requests.

**Transfer gate.** Require current parties, mechanism, assessment, safeguards, destination, onward restrictions, approval, and evidence before disclosure or remote access.

**Resilience gate.** Prove availability, failure independence, failover, recovery, backup, key restoration, and emergency behavior stay within policy or surface an explicit conflict.

**Observation gate.** Collect provider inventory, runtime topology, network, identity, key, storage, replication, transfer, access, backup, and deletion evidence with source and time.

**Reconciliation gate.** Compare expected inventory and decisions with observed assets and events; quarantine unknown, stale, conflicting, and prohibited state.

**Change gate.** Reassess legal rules, mechanisms, adequacy, subprocessors, provider behavior, services, topology mappings, contracts, purposes, data, and threats before activation.

**Incident and correction gate.** Contain invalid placement or access, preserve facts, determine affected scope, notify, migrate or delete, remedy, update controls, and verify closure.

**Recovery and closure gate.** Restore current profiles and restrictions before processing; end resources, copies, access, routes, keys, mechanisms, exceptions, and reactivation paths.

### Executable evidence: residency-profile placement evaluation

This Python example classifies ten invented placement requests against three declared profiles. It tests only literal declarations and does not perform legal or geographic verification.

<!-- bijux-verify: {"id":"residency-profile-placement-evaluation","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"placements=10\nprofiles=3\npermitted_local=4\npermitted_transfer=1\nlocation_violation=1\naccess_violation=1\nunknown_location=1\nkey_control_violation=1\nblocked_transfer=1\ncountries=4\npersonnel_jurisdictions=3\nasset_planes=8\ndecision_events=10\n","stderr":""}} -->
```python
profiles = {
    "eu_restricted": {
        "local": {"de", "fr"},
        "personnel": {"de", "fr"},
        "organization_key": True,
        "transfer_mechanisms": set(),
    },
    "global_standard": {
        "local": {"de", "fr", "us"},
        "personnel": {"de", "fr", "us"},
        "organization_key": False,
        "transfer_mechanisms": {"scc"},
    },
    "public": {
        "local": {"us"},
        "personnel": {"us"},
        "organization_key": False,
        "transfer_mechanisms": set(),
    },
}

placements = [
    {"asset": "patient-db", "plane": "content", "profile": "eu_restricted", "operation": "storage", "location": "de", "personnel": "de", "organization_key": True, "mechanism": None, "assessment_current": False},
    {"asset": "patient-snapshot", "plane": "backup", "profile": "eu_restricted", "operation": "storage", "location": "fr", "personnel": "de", "organization_key": True, "mechanism": None, "assessment_current": False},
    {"asset": "patient-analysis", "plane": "derived", "profile": "eu_restricted", "operation": "processing", "location": "de", "personnel": "fr", "organization_key": True, "mechanism": None, "assessment_current": False},
    {"asset": "support-session", "plane": "support", "profile": "eu_restricted", "operation": "support", "location": "fr", "personnel": "us", "organization_key": True, "mechanism": None, "assessment_current": False},
    {"asset": "diagnostic-log", "plane": "telemetry", "profile": "eu_restricted", "operation": "storage", "location": "us", "personnel": "de", "organization_key": True, "mechanism": None, "assessment_current": False},
    {"asset": "query-cache", "plane": "cache", "profile": "eu_restricted", "operation": "storage", "location": None, "personnel": "de", "organization_key": True, "mechanism": None, "assessment_current": False},
    {"asset": "identity-index", "plane": "content", "profile": "eu_restricted", "operation": "storage", "location": "de", "personnel": "de", "organization_key": False, "mechanism": None, "assessment_current": False},
    {"asset": "partner-export", "plane": "export", "profile": "global_standard", "operation": "transfer", "location": "ca", "personnel": "us", "organization_key": False, "mechanism": "scc", "assessment_current": True},
    {"asset": "research-export", "plane": "export", "profile": "global_standard", "operation": "transfer", "location": "us", "personnel": "us", "organization_key": False, "mechanism": "scc", "assessment_current": False},
    {"asset": "public-catalog", "plane": "public", "profile": "public", "operation": "storage", "location": "us", "personnel": "us", "organization_key": False, "mechanism": None, "assessment_current": False},
]

def evaluate(placement):
    profile = profiles[placement["profile"]]
    if placement["location"] is None:
        return "unknown_location"
    if placement["operation"] == "transfer":
        if (
            placement["mechanism"] in profile["transfer_mechanisms"]
            and placement["assessment_current"]
        ):
            return "permitted_transfer"
        return "blocked_transfer"
    if placement["location"] not in profile["local"]:
        return "location_violation"
    if placement["personnel"] not in profile["personnel"]:
        return "access_violation"
    if profile["organization_key"] and not placement["organization_key"]:
        return "key_control_violation"
    return "permitted_local"

results = [evaluate(placement) for placement in placements]

print(f"placements={len(placements)}")
print(f"profiles={len(profiles)}")
print(f"permitted_local={results.count('permitted_local')}")
print(f"permitted_transfer={results.count('permitted_transfer')}")
print(f"location_violation={results.count('location_violation')}")
print(f"access_violation={results.count('access_violation')}")
print(f"unknown_location={results.count('unknown_location')}")
print(f"key_control_violation={results.count('key_control_violation')}")
print(f"blocked_transfer={results.count('blocked_transfer')}")
print(f"countries={len({p['location'] for p in placements if p['location']})}")
print(f"personnel_jurisdictions={len({p['personnel'] for p in placements})}")
print(f"asset_planes={len({p['plane'] for p in placements})}")
print(f"decision_events={len(results)}")
```

The expected output reports ten placements, three profiles, four local permits, one transfer permit, one location violation, one personnel-access violation, one unknown location, one key-control violation, one blocked transfer, four declared countries, three personnel jurisdictions, eight asset planes, and ten decision events on separate lines.

The evidence is deliberately narrow. Country strings do not establish facility, territory, jurisdiction, provider entity, service behavior, or actor location. The profiles are invented and are not legal rules. The evaluator treats one `scc` string and one Boolean as a current transfer assessment, does not inspect onward recipients, and does not enforce any result. It proves no applicable law, valid mechanism, effective safeguard, exclusive key control, provider conformance, government-access resistance, resilience, deletion, human-rights protection, or outcome. Production assurance requires authorized interpretation, complete inventory, provider-specific capability evidence, typed location observations, real transfer assessments, identity and network enforcement, independent testing, affected-party review, reconciliation, incident correction, recovery exercises, and exit tests.

## Alternatives and Trade-Offs

**Single-country deployment.** Location reasoning is simpler. Service choice, capacity, latency, availability, disaster recovery, and supplier diversity may weaken.

**Approved multi-country territory.** Resilience and service access improve. Territorial mappings, transfers, contracts, and differentiated rules become more complex.

**Public cloud regional services.** Mature controls and elastic operations are available. Global dependencies, provider entities, support access, and service exceptions require continuous review.

**Sovereign or national cloud.** Personnel, entity, support, and location controls may be stronger. Feature parity, interoperability, cost, capacity, and concentration risk can suffer.

**Customer premises.** Physical custody and local operation can increase. Supply chain, skills, patching, disaster recovery, and compelled access do not disappear.

**Hybrid processing.** Restricted data can remain local while elastic services handle bounded outputs. Interfaces, classification, synchronization, leakage, failure, and deletion become harder.

**Per-tenant regional stacks.** Isolation and explanation are clear. Fleet sprawl, uneven versions, utilization, and operations cost increase.

**Shared regional platform.** Governance and efficiency improve. Tenant-specific rules, mixed data, and common-service leakage require stronger partitioning.

**Row-level residency routing.** Fine-grained contractual or subject requirements can be represented. Joins, transactions, indexes, caches, analytics, and recovery become complex.

**Dataset-level routing.** Operations remain tractable. Mixed populations may be overrestricted or incorrectly combined.

**Hard admission controls.** Invalid resources are prevented before use. Unsupported services and emergency work can be blocked.

**Detective controls.** Adoption is flexible and drift is visible. Detection occurs after prohibited placement or access may have happened.

**Provider-managed keys.** Availability and service integration are strong. Provider or service access and compelled disclosure assumptions may be unacceptable.

**Customer-controlled keys.** Revocation and separation improve. Runtime plaintext, service integration, key operators, and provider-mediated operations can remain.

**Externally held keys.** Provider access can be reduced substantially. Latency, availability, disaster recovery, and irreversible loss risks increase.

**Local-only support.** Personnel boundaries are clearer. Expertise, hours, incident response, and service restoration may be constrained.

**Global support with approval.** Specialist recovery is available. Remote access, entity, device, jurisdiction, and evidence controls become critical.

**Same-territory replication.** Availability can improve without crossing the declared boundary. Correlated disaster risk and regional capacity may remain.

**Cross-boundary disaster recovery.** Catastrophic resilience improves. Transfer and localization rules, notification, safeguards, and failback require authorization.

**Global control plane.** Fleet consistency and vendor operation improve. Metadata, identity, policy, and support may leave the workload boundary.

**Isolated control plane.** Operational autonomy and boundary clarity improve. Patch distribution, feature delivery, monitoring, and recovery can lag.

**Contractual commitments.** Roles, remedies, subprocessors, and change obligations become explicit. Contracts cannot physically prevent a bad route or configuration.

**Technical enforcement.** Placement and access can be blocked at runtime. Code cannot decide disputed legal interpretation or bind an external sovereign.

**Central placement service.** Policy and evidence are consistent. Outage, latency, authority concentration, and cross-domain context become risks.

**Federated placement decisions.** Local requirements and operations remain close to domains. Vocabulary, equivalence, conflict, and assurance require protocols.

**Provider attestations.** Broad infrastructure evidence is economical. Scope, sampling, date, service coverage, and customer configuration limit inference.

**Direct observations.** Resource and access state is timely. Observation can be incomplete, provider-mediated, sensitive, and expensive.

**Portable baseline services.** Exit and multi-provider consistency improve. Advanced managed capabilities and performance may be sacrificed.

**Provider-specific services.** Capability and productivity improve. Reproduction, policy equivalence, migration, and technical sovereignty become harder.

## Failure Modes and Misconceptions

**“Residency, localization, and sovereignty are synonyms.”** They concern different location, authority, control, and operational properties.

**“A country flag proves compliance.”** A display icon is neither an authoritative rule nor observed placement evidence.

**“A provider region is a legal jurisdiction.”** Regions are provider constructs whose territorial and entity relationships require mapping.

**“Europe always means the EU.”** Geographic, political, contractual, and provider boundaries differ.

**“Data sovereignty means data never crosses a border.”** Sovereignty can involve authority, operators, keys, dependencies, recovery, and exit as well as location.

**“Local storage eliminates foreign authority.”** Authority may attach to entities, operators, control, or extraterritorial process.

**“All personal data must stay in its country of origin.”** Applicable regimes and sectors define varied transfer and localization rules.

**“Non-personal data has no sovereignty concern.”** Industrial, public, strategic, confidential, and regulated non-personal data can be governed.

**“A transfer requires copying bytes.”** Remote access or making data available can be governed even without durable copying.

**“Transit never matters.”** Routing, termination, caching, observation, and applicable rules determine relevance.

**“Encryption moves data outside scope.”** Encryption changes intelligibility assumptions, not physical location or every legal duty.

**“Customer-managed keys mean customer-exclusive keys.”** Service runtime or provider roles may still reach keys or plaintext.

**“Keys are metadata and can be global.”** Key location, operators, recovery, and access may be central requirements.

**“Pseudonymized data is anonymous everywhere.”** Reidentification capability and contextual law or policy remain relevant.

**“The primary database is the whole system.”** Logs, indexes, caches, replicas, models, support data, and backups can contain governed data.

**“Telemetry contains no customer data.”** Identifiers, payload fragments, queries, errors, and behavior can appear in telemetry.

**“Control-plane metadata is harmless.”** Names, policies, identities, topology, and activity can be sensitive or regulated.

**“A model has no residency after training.”** Weights, checkpoints, memorization, inputs, outputs, and operation locations require assessment.

**“Derived data automatically inherits no restrictions.”** Transformation can reduce, preserve, or create risks and obligations.

**“A local API endpoint proves local processing.”** Routing, backing services, support, and control planes may be elsewhere.

**“Region configuration proves actual location.”** Configuration is one evidence source and can drift or cover only part of a service.

**“Infrastructure code is independent evidence.”** It usually restates the requested state rather than observing provider behavior.

**“Every service in a region is regional.”** Global and nonregional services can handle data differently.

**“Availability zones are countries.”** Zones are failure domains within provider-defined regions.

**“Node labels are legal evidence.”** Mutable provider-specific labels require trustworthy mapping and corroboration.

**“Preferred scheduling is a residency boundary.”** A scheduler may place elsewhere when preference is not a hard constraint.

**“Network geolocation proves facility location.”** Endpoints, proxies, anycast, and provider networks weaken that inference.

**“Blocking internet egress blocks all transfers.”** Private links, managed integrations, support paths, replication, and provider operations remain.

**“Access control proves permitted jurisdiction.”** Identity permission does not prove actor location, entity, purpose, or transfer basis.

**“Personnel citizenship determines every sovereignty question.”** Residence, employer, access location, authority, and applicable rules are separate.

**“A standard contract authorizes every flow.”** Parties, modules, data, purpose, destination, onward transfer, and assessment scope matter.

**“Adequacy is permanent.”** Decisions, coverage, organizations, laws, and facts can change.

**“One transfer assessment covers a country forever.”** Services, data, parties, purposes, safeguards, law, and practices evolve.

**“A vendor contract is technical enforcement.”** Misconfiguration and unsupported features can contradict the commitment.

**“Technical location controls establish legal validity.”** Applicable authority and interpretation remain outside the policy engine.

**“Subprocessor notice is enough.”** Activation may need review, objection, migration, or blocking before access.

**“Corporate ownership and data location are identical.”** Entity control and physical placement are different sovereignty dimensions.

**“Local hosting guarantees operational autonomy.”** Remote dependencies, licenses, updates, keys, and expertise can stop local operation.

**“Open source guarantees technical sovereignty.”** Build systems, maintainers, dependencies, skills, and operational knowledge still matter.

**“Multi-cloud automatically reduces sovereignty risk.”** It can multiply entities, controls, transfers, gaps, and inconsistent evidence.

**“Single-region always satisfies localization.”** The region may cross a territory, use global services, or lack required operator controls.

**“Replication is only an availability setting.”** It creates copies, flows, keys, retention, and recovery paths.

**“Disaster recovery is exempt from location policy.”** Emergency processing needs applicable authority and bounded controls.

**“Failover should always maximize uptime.”** An unauthorized destination can create greater harm than controlled unavailability.

**“Backups follow the current resource policy.”** Old snapshots can retain prior topology, keys, subjects, and rules.

**“Deletion of the primary closes residency risk.”** Replicas, exports, models, logs, backups, and provider residue may remain.

**“Zero detected violations proves residency.”** Missing inventory and weak observation can hide exposure.

**“One hundred percent configured resources proves compliance.”** Configuration coverage is not processing, access, or outcome coverage.

**“Changing the region label corrects history.”** Past access, transfer, disclosure, and effects require investigation and remedy.

**“Restoring locally makes an old backup compliant.”** The backup can contain prohibited data, expired exceptions, and obsolete decisions.

## Worked Examples

### Example 1

A health service stores records and backups in two approved national regions. Its default tracing service is global and can capture query parameters. The admission controller blocks tracing until payload filtering and an approved regional sink are verified; database locality alone was insufficient.

### Example 2

A European controller uses a foreign analytics provider under a scoped transfer mechanism and current assessment. The record names parties, data, purpose, service, destination, subprocessors, encryption, key access, onward limits, expiry, and evidence. A new subprocessor remains blocked until review completes.

### Example 3

A bank's object store is regional, but support personnel can open decrypted objects through a global console. The profile requires local approved operators and dual approval. Identity policy, session proxy, device checks, recording, and content export controls enforce the personnel boundary.

### Example 4

A Kubernetes cluster spans three zones in one provider region. Topology labels guide scheduling, while a signed provider-region mapping supplies the territorial claim. Admission rejects pods whose volumes, secrets, telemetry sink, or node selector do not match the governed profile.

### Example 5

A retailer routes customer partitions by contract territory. Orders are processed locally, but aggregate demand planning is allowed in a wider region after a documented transformation and purpose review. Provenance records exactly which fields and tests support the derived-data decision.

### Example 6

A disaster destroys the primary region. The only healthy destination is prohibited for the affected records. The runbook enters a safe read-only mode, escalates the explicit availability conflict, and does not silently invoke cross-boundary failover under a generic emergency flag.

### Example 7

A research platform uses externally held keys for a restricted archive. Compute requests short-lived decryption authorization in an approved confidential environment. Evidence distinguishes key custody, runtime plaintext, operator access, workload identity, location, and output egress rather than claiming encryption alone proves sovereignty.

### Example 8

A global identity service stores tenant configuration outside the workload region. The architecture classifies each attribute, separates authentication necessities from optional profile data, documents the global dependency, restricts payload, and records the applicable decision instead of calling the whole system local.

### Example 9

A provider changes a managed database's backup behavior. Capability-monitoring emits an effective-dated change event; affected profiles become pending, new provisioning stops, existing instances are assessed, and compliant migration options are produced before the provider deadline.

### Example 10

During exit, an organization exports content, schemas, lineage, policy bindings, consent state, audit evidence, and key material into a verified replacement. It revokes identities and routes, obtains scoped deletion evidence for replicas and backups, and proves old recovery automation cannot recreate provider resources.

## Cross-Program Connections

**Privacy Engineering.** International transfers, purpose, minimization, government access, transparency, rights, vulnerable populations, and redress define human consequences beyond infrastructure placement.

**Security Engineering.** Identity, encryption, keys, confidential computing, network control, monitoring, supply chain, incident response, and recovery reduce exposure without deciding legal authority.

**Cloud and Platform Engineering.** Landing zones, accounts, projects, regions, admission, schedulers, service catalogs, policy, key systems, observability, and backup defaults implement boundaries at scale.

**Distributed Systems.** Replication, consistency, partitions, failover, clocks, routing, caches, queues, and recovery create location and availability trade-offs.

**Data Engineering.** Pipelines, lakehouses, warehouses, streams, lineage, copies, exports, transformations, and orchestration determine real data movement.

**API and Service Engineering.** Placement decisions, resource APIs, idempotency, versioning, protected explanations, events, and reconciliation expose residency controls safely.

**Machine Learning Engineering.** Training data, feature stores, accelerators, checkpoints, model weights, prompts, inference, telemetry, and deletion complicate asset and operation scope.

**Site Reliability Engineering.** Service objectives, regional failure, capacity, degraded modes, failover, restore, exercises, and incident authority make policy operational.

**Governance, Risk, and Compliance.** Applicable law, sector rules, contracts, transfer mechanisms, assessments, exceptions, government access, evidence, and remedy define authorized requirements.

**Procurement and Vendor Management.** Legal entities, subprocessors, locations, support, audit rights, change notification, portability, deletion, and exit must match technical reality.

**Enterprise Architecture.** Capability ownership, strategic autonomy, supplier concentration, interoperability, portfolio standards, and migration determine sustainable sovereignty.

**Ethics and Public Policy.** Human rights, democratic oversight, access powers, community sovereignty, indigenous data governance, competition, and equitable service access exceed country routing.

## References

1. European Union, [“Regulation (EU) 2016/679 (General Data Protection Regulation)”](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32016R0679), 2016. Retrieved 2026-09-03.
2. European Data Protection Board, [“Recommendations 01/2020 on Measures That Supplement Transfer Tools”](https://www.edpb.europa.eu/documents/recommendation/recommendations-012020-on-measures-that-supplement-transfer-tools-to_en), 2021. Retrieved 2026-09-03.
3. European Commission, [“Standard Contractual Clauses for International Transfers”](https://commission.europa.eu/publications/standard-contractual-clauses-international-transfers_en), 2021. Retrieved 2026-09-03.
4. Court of Justice of the European Union, [“Data Protection Commissioner v Facebook Ireland and Maximillian Schrems, Case C-311/18”](https://curia.europa.eu/juris/document/document.jsf?text=&docid=228677&pageIndex=0&doclang=EN), 2020. Retrieved 2026-09-03.
5. UK Information Commissioner's Office, [“Completing a Transfer Risk Assessment”](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/international-transfers/completing-a-transfer-risk-assessment/), 2026. Retrieved 2026-09-03.
6. European Union, [“Regulation (EU) 2023/2854 on Harmonised Rules on Fair Access to and Use of Data (Data Act)”](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32023R2854), 2023. Retrieved 2026-09-03.
7. Organisation for Economic Co-operation and Development, [“Declaration on Government Access to Personal Data Held by Private Sector Entities”](https://legalinstruments.oecd.org/api/print?ids=693&lang=en), 2022. Retrieved 2026-09-03.
8. National Institute of Standards and Technology, [“SP 800-53 Release 5.2.0: Security and Privacy Controls for Information Systems and Organizations”](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final), 2025. Retrieved 2026-09-03.
9. Kubernetes, [“Well-Known Labels, Annotations and Taints: Topology Region and Zone”](https://kubernetes.io/docs/reference/labels-annotations-taints/#topologykubernetesioregion), retrieved 2026-09-03.
10. Amazon Web Services, [“Hybrid Architectures to Address Personal Data Processing Requirements: Actions, Recommendations, and Best Practices”](https://docs.aws.amazon.com/whitepapers/latest/hybrid-architectures-to-address-personal-data-processing-requirements/actions-recommendations-and-best-practices.html), retrieved 2026-09-03.
11. Microsoft, [“Controls and Principles in Sovereign Public Cloud”](https://learn.microsoft.com/en-us/azure/azure-sovereign-clouds/public/overview-controls-principles), 2026. Retrieved 2026-09-03.
12. Google Cloud, [“Assured Workloads: Data Residency”](https://docs.cloud.google.com/assured-workloads/docs/data-residency), 2026. Retrieved 2026-09-03.

## Exercises

### Exercise 1

Design residency profiles for a multinational health platform covering clinical records, appointment data, billing, support tickets, audit logs, telemetry, analytics, research exports, models, keys, backups, and deletion journals. Specify applicable authority, operations, locations, actors, transfer rules, resilience, evidence, and exceptions.

### Exercise 2

Design a multi-cloud placement control plane. Define vocabularies, trusted workload identity, profile resolution, provider-capability registry, admission controls, placement API, network and key enforcement, event contracts, reconciliation, protected evidence, and failure behavior.

### Exercise 3

Create a transfer and remote-access architecture for a regional data controller using global support, fraud analysis, research partners, and subprocessors. Include parties, purposes, data, mechanisms, assessments, safeguards, sessions, onward flows, changes, incidents, and closure.

### Exercise 4

Design resilience for a workload whose records must remain within one territory but whose recovery objective cannot be met by one region. Compare zones, multiple domestic regions, local facilities, hybrid services, alternate providers, degraded modes, and bounded emergencies. State what evidence would justify the result.

### Exercise 5

Plan migration from spreadsheets, region tags, vendor contracts, and undocumented backups to authoritative residency governance. Include discovery, source preservation, semantic mapping, unknowns, canaries, dual evaluation, remediation, consumer adoption, recovery testing, and retirement criteria.

## Answers to the Exercises

### Answer 1

Create separate applicability and jurisdiction decisions for each organization, establishment, subject population, contract, sector, purpose, and operation. Define stable profiles for clinical care, billing, support, security, optional analytics, protocol-specific research, and lifecycle evidence. For every profile, state allowed and prohibited country, territory, provider geography, region, zone, facility, operator, legal entity, support path, key custody, transfer, backup, restore, and deletion behavior with authority, version, expiry, and reviewer.

Inventory clinical fields, attachments, appointments, invoices, identity attributes, support content, logs, traces, metrics, caches, search indexes, derived tables, feature stores, training and evaluation data, weights, exports, snapshots, archives, keys, deletion journals, and provider residue. Bind each representation to subjects, classification, purpose, basis, retention, lineage, owner, and evidence. Separate storage, processing, transit, remote display, administration, support, disclosure, replication, failover, recovery, and deletion.

Use admission and runtime controls for accounts, services, locations, schedulers, networks, identities, sessions, egress, keys, replicas, and exports. Require current assessments and mechanisms for each transfer and onward recipient. Make resilience conflicts explicit, preapprove compliant failover, rehearse restore under current rules, and prohibit silent emergency expansion. Reconcile expected inventory against provider, runtime, network, identity, key, backup, and recipient evidence. Metrics expose unknown and unsupported populations; incidents preserve history, contain use, migrate or delete, notify as required, and verify remedy.

### Answer 2

Define stable identities for countries, territories, provider geographies, regions, zones, facilities, services, capabilities, entities, actor attributes, operations, data classes, purposes, profiles, mechanisms, assessments, safeguards, observations, exceptions, and decisions. Provider mappings include source, service and feature coverage, effective interval, confidence, exclusions, global dependencies, support, backup, key, and recovery behavior. Workload identities come from trusted build and runtime systems rather than request parameters.

The placement API accepts authenticated workload, data and subject scope, purpose, operation, proposed provider service and topology, actor, key plan, network route, availability target, and time. It returns permit or deny, alternatives, profile and rule versions, obligations, evidence needs, expiry, and a protected explanation. Infrastructure admission prevents invalid accounts, projects, resources, replicas, endpoints, and keys. Runtime policy binds scheduler, storage, query, job, identity, network, decryption, export, and support decisions.

Publish immutable profile, capability, decision, provision, observation, access, transfer, exception, drift, failover, recovery, and closure events. Consumers deduplicate and reject rollback. Reconciliation compares catalogs, lineage, declarations, provider inventory, topology, flow logs, identity sessions, key logs, backups, contracts, and recipient attestations. Unknown or conflicting restricted state quarantines creation or processing. Encrypt and partition sensitive reasoning. Operate availability objectives for the decision service, signed offline-safe policy where justified, bounded caches, revocation, incident response, and recovery that loads current restrictions before workload data.

### Answer 3

Represent each exporter, importer, controller, processor, joint controller, subprocessor, support organization, research partner, and provider entity separately. A transfer relationship names data and subjects, purpose, operations, destination, onward parties, authority, exact mechanism and module, attachments, assessment method, destination facts, government-access analysis, safeguards, effective time, expiry, reviewer, notification, dispute, and termination. Global support is an access operation with personnel employer, access location, device, workload, session, approval, displayed fields, export ability, recording, and receipt.

Fraud analysis, service support, and each research protocol use separate purposes and necessity or basis decisions. Minimize views and exports, pseudonymize only with proven separation, hold keys under stated custody, gate decryption by workload and approved context, restrict networks, and prevent unmanaged downloads. Register subprocessors and onward recipients before access; a proposed change opens review and blocks activation where required. Periodic reassessment detects legal, practice, entity, service, purpose, data, safeguard, and subprocessor changes.

Events record request, approval, session start and end, transfer, receipt, exception, incident, and revocation. Reconciliation compares provider access logs, identity, network, export, recipient, and contract inventories. An incident contains access, preserves facts, identifies data and people, evaluates notification and remedy, rotates credentials and keys where needed, and verifies downstream deletion or restriction. Closure revokes identities, sessions, routes, exports, mechanisms, contracts, and recovery paths while retaining minimum authorized evidence.

### Answer 4

Start with explicit failure model, recovery point and time, maximum outage, integrity and safety constraints, capacity, key recovery, and the exact territorial rule. Test multiple independent availability zones first, but verify whether their power, network, control-plane, and disaster risks meet the objective. Evaluate two domestic regions if available; otherwise compare organization-controlled facilities, domestic alternate providers, hybrid replicas, offline immutable media, reduced-capability local service, and restoration from tested portable artifacts.

For every option, model customer content, metadata, logs, keys, operators, network, control plane, backups, licenses, software supply chain, and recovery dependencies. Prove the destination and support model are allowed and that replication, failover, restore, and failback use current profiles. Quantify correlated failure, capacity, latency, consistency, cost, operational skill, and exercise evidence. If no design meets both objectives, document the incompatibility and obtain an authorized requirement or risk decision rather than weakening either silently.

Precompute approved destinations and signed runbooks. Runtime failover verifies current profile, data scope, purpose, destination capability, mechanism, keys, authority, expiry, and evidence. A bounded emergency path states triggering conditions, approver, data and operations, destination, duration, safeguards, monitoring, notification, containment, and forced exit. Exercises inject regional loss, control-plane loss, key outage, stale policy, denied destination, incomplete backup, and rollback. Success requires service outcome plus proof that no prohibited copy, operator, route, or residual resource remained.

### Answer 5

Inventory every spreadsheet row, tag namespace, policy, contract, assessment, vendor, legal entity, account, resource, service, region, zone, data asset, operation, subject and contract population, support path, network route, key, replica, backup, failover job, export, subprocessor, exception, and observation source. Preserve immutable source snapshots with ownership and access controls. Define canonical vocabularies and typed records before mapping. A tag such as `EU` becomes a legacy assertion with source and limitations, not a proven country or valid profile.

Resolve contracts and assessments to exact parties, services, data, purposes, destinations, safeguards, dates, and termination. Discover resources through provider APIs, catalogs, lineage, runtime topology, flow logs, identity sessions, key records, backup vaults, and recovery configurations. Unknown region semantics, global-service behavior, subject scope, support access, subprocessor, or backup location remain unknown and block restricted new use. Prioritize potentially prohibited access and copies for containment and authorized review.

Canary profiles in selected domains, dual-evaluate old and new decisions, compare placements and failures, correct mappings, and test provisioning, runtime access, transfer, failover, restore, and deletion. Register every consumer and collect adoption evidence. Migrate or delete invalid resources, replay current exceptions and restrictions, and reconcile full denominators. Deprecate spreadsheet and free-form tag writes, revoke old policy permissions, remove unsafe defaults, and update incident and recovery procedures. Retirement proves no provisioner, job, support path, replica, backup, or restore process can treat ambiguous legacy state as residency authorization while historical evidence remains interpretable.
