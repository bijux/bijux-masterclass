---
module_id: DARCH-071
program: Data Architecture Engineering
level: 2
module_number: 71
title: Federated Data Governance
status: complete
last_verified: 2026-09-03
---

# Federated Data Governance

## One-Page Review

### Governing question

How should an organization distribute authority for data decisions across domains, platforms, risk functions, and shared governing bodies while preserving enterprise obligations, cross-domain interoperability, visible accountability, and a workable path for conflict, correction, recovery, and exit?

### Essential definitions

- **Data governance** is the system by which decision rights, obligations, evidence, resources, and accountability for data are established, exercised, observed, challenged, and changed.
- **Federation** distributes bounded governance authority among autonomous participants that accept a shared constitutional minimum and explicit coordination protocols.
- A **domain** is a durable responsibility boundary with subject expertise, operational control, data-producing or consuming capabilities, named authority, and measurable outcomes; it is not merely an organizational chart box.
- A **governance constitution** defines mandatory principles, nondelegable obligations, reserved decisions, delegated powers, evidence requirements, conflict rules, amendment, and exit.
- A **decision right** specifies who may decide what, for which data and purpose, under which constraints, with which consultation, evidence, effective time, and appeal.
- An **accountable owner** answers for outcomes and unresolved risk; a **steward** performs or coordinates day-to-day governance; a **custodian** implements technical controls. Titles do not prove authority or capacity.
- A **minimum control baseline** is the smallest shared set of identity, metadata, protection, quality, interoperability, audit, lifecycle, and assurance requirements that every participating domain must satisfy.
- A **domain policy** specializes the baseline for local risks and uses without weakening nondelegable obligations.
- A **federated data product** exposes governed data, metadata, interfaces, policies, evidence, service objectives, support, change, and lifecycle commitments across a domain boundary.
- A **control plane** carries policy, identity, metadata, evidence, decisions, and coordination; a **data plane** carries governed data processing and exchange. The distinction is logical, not necessarily a separate technology stack.
- **Conformance** means declared controls meet specified requirements; **effectiveness** asks whether they actually reduce the intended risk and support legitimate outcomes.
- An **exception** is time-bounded, attributable acceptance of a stated deviation with scope, rationale, compensating controls, risk owner, review date, and closure conditions.
- A **federation conflict** is a disagreement between valid authorities, policies, definitions, priorities, or evidence that cannot be resolved by local rules alone.
- **Subsidiarity** assigns a decision to the lowest competent authority whose scope contains its consequences while escalating decisions with wider externalities.
- **Closure** ends authority, access, publication, automation, exceptions, dependencies, and recovery paths while preserving required evidence and historical interpretation.

### Central model, mechanism, or theorem

Represent a federation as:

`F = (C, D, R, P, B, E, O, X, L)`

where `C` is the shared constitution, `D` participating domains, `R` decision rights and roles, `P` policies and profiles, `B` shared baselines and boundary contracts, `E` evidence and assurance, `O` operations and outcome feedback, `X` exceptions and conflict resolution, and `L` lifecycle and exit. A federation is governable only if each consequential decision resolves to one accountable authority, applicable constraints compose without silent weakening, evidence can be traced to control and outcome, and unresolved cross-domain externalities have a legitimate escalation path.

### Critical invariants

- Every governed asset, product, policy, decision, exception, issue, and control has stable identity, scope, authority, version, and effective time.
- Accountability is singular for a decision outcome even when work, consultation, and implementation are shared.
- Domains may strengthen shared requirements but cannot silently weaken law, rights, safety, security, privacy, records, or enterprise risk obligations.
- Reserved enterprise decisions and delegated domain decisions are explicit; absence of a rule is not delegation.
- Producers remain accountable for published contract and evidence; consumers remain accountable for authorized and fit use.
- A shared catalog aggregates authoritative assertions without becoming the unquestioned authority for every assertion.
- Policy conflict, missing evidence, stale attestation, unknown ownership, and unsupported purpose fail visibly for consequential use.
- Exceptions expire, are observable, and cannot become permanent policy through repeated renewal without explicit amendment.
- Metrics publish denominators and distinguish activity, conformance, control effectiveness, product fitness, consumer adoption, risk, and outcome.
- Federation changes preserve historical decisions, policy versions, evidence, and affected-party remedy.
- Recovery restores authority and policy state before automated data actions resume.
- Exit closes active dependencies and exports portable identities, contracts, evidence, histories, and tombstones without inventing semantic equivalence.

### Common failures

Common failures include renaming committees as federation; treating decentralization as absence of shared rules; copying a RACI chart without defining decisions; assigning ownership to unavailable executives; making stewards accountable without authority or budget; centralizing every approval; delegating nondelegable obligations; allowing local policy to weaken the baseline; counting catalog entries as governed products; treating certification as permanent fitness; confusing provenance with truth; hiding policy conflicts behind precedence order; accepting undocumented exceptions; measuring meetings and tickets instead of outcomes; requiring consumers to infer source authority; propagating controls through lineage without transformation rules; building one universal maturity score; and retiring a domain while its products, permissions, exceptions, events, and restore procedures remain active.

### Compact example

Three invented domains receive six decision delegations. Four decisions are locally decidable, one requires shared approval, and one is reserved centrally. Five products are assessed against four baseline controls: three conform, one has an active exception, and one is blocked. Two cross-domain conflicts enter resolution; one is closed and one remains open. Executable evidence confirms only those declarations and counts. It proves no legal compliance, role legitimacy, control effectiveness, product fitness, policy enforcement, or beneficial outcome.

### Connections

[DARCH-027](027-producer-and-consumer-contracts.md), [DARCH-057](057-shared-code-sets-and-controlled-vocabularies.md), [DARCH-061](061-metadata-architecture.md), [DARCH-064](064-lineage-architecture.md), [DARCH-068](068-data-catalog-architecture.md), [DARCH-069](069-metadata-apis-and-eventing.md), and [DARCH-070](070-connecting-technical-metadata-to-business-meaning.md) establish contracts, shared vocabularies, metadata, provenance, catalog, interface, and semantic foundations. [DARCH-072](../ROADMAP.md) next develops privacy architecture and privacy-enhancing patterns.

## Governing Question

Data decisions occur where systems are designed, transactions are captured, products are operated, regulations are interpreted, risks are accepted, and consumers act. A small enterprise council cannot possess all of that context or approve every change. Yet allowing each team to define identity, access, retention, quality, meaning, evidence, and sharing independently creates incompatible controls and unowned externalities.

The governing question is therefore not whether governance should be centralized or decentralized. It is which decisions belong at which boundary, which obligations cannot be delegated, how authorities coordinate, what evidence crosses boundaries, and how the system corrects itself when local choices harm shared outcomes. Federation is an engineered allocation of authority, not a cultural aspiration or tooling brand.

## Why This Matters

The U.S. Federal Data Strategy [Data Governance Playbook](https://resources.data.gov/assets/documents/fds-data-governance-playbook.pdf) describes governance as setting and enforcing priorities for managing and using data as a strategic asset. It calls for an authorized governance body that establishes policies, procedures, roles, reporting, monitoring, and investment priorities. The playbook supports a coordinating center, but it does not imply that one body should perform every operational decision.

The Federal Data Strategy [Practices](https://strategy.data.gov/practices/) require sufficient authorities, roles, organizational structures, policies, and resources, along with protection of confidentiality, privacy, and integrity. That formulation matters because a role name without authority or resources is not an operating model. Federation must connect stated accountability to capacity and enforcement.

NIST's [Privacy Framework](https://www.nist.gov/privacy-framework/privacy-framework) treats governance as part of enterprise risk management and connects executives, business and process managers, and implementation personnel. Its profiles support communication across a data-processing ecosystem. A federated data architecture can use the same pattern: a common vocabulary of outcomes, current and target profiles, local implementation choices, and traceable evidence.

The UK Government's [Data Ownership Model](https://www.gov.uk/government/publications/data-ownership-in-government/data-ownership-model) distinguishes accountable data owners, operational data stewards, and technical custodians. It also addresses shared datasets across organizations through primary and local owners. These are useful role patterns, but local authority, law, employment design, and capability must determine their implementation.

The EU [Interoperable Europe Act](https://interoperable-europe.ec.europa.eu/Interoperable-Europe-Act-Regulation) establishes a governance structure for public-sector interoperability and provides for a European Interoperability Framework spanning legal, organizational, semantic, and technical layers. Its scope is specific and legal advice is required for applicability. Architecturally, it demonstrates that independent participants can coordinate through a shared board, common frameworks, assessments, reusable solutions, and specialized profiles without erasing national or sector authority.

NIST's [Cybersecurity Framework 2.0](https://www.nist.gov/cyberframework) adds Govern as a core function and connects organizational context, risk strategy, roles, policy, oversight, and supply-chain risk. Although it addresses cybersecurity risk rather than supplying a complete data-governance model, its separation of governance outcomes from implementation techniques is useful for federations whose domains use different technologies.

W3C [DCAT 3](https://www.w3.org/TR/vocab-dcat-3/) provides interoperable descriptions for catalogs, datasets, distributions, data services, versions, relationships, rights, and policies. It supports aggregation across decentralized catalogs. A shared catalog can therefore coordinate discovery while preserving publisher identity and multiple distributions; conformance to DCAT does not settle organizational authority or product fitness.

W3C [ODRL 2.2](https://www.w3.org/TR/odrl-model/) models permissions, prohibitions, duties, constraints, parties, assets, and policy relationships. It can carry machine-readable usage policy across boundaries, but its own model does not enforce a policy or decide whether the policy is lawful, legitimate, compatible, or effective.

W3C [PROV-O](https://www.w3.org/TR/prov-o/) represents entities, activities, agents, derivation, attribution, association, delegation, and qualified relations. Federation needs that provenance to distinguish a domain assertion, a platform transformation, a risk approval, and an independent assessment. Provenance establishes traceable origin; it does not make the assertion true.

W3C [Data Quality Vocabulary](https://www.w3.org/TR/vocab-dqv/) distinguishes quality dimensions, metrics, measurements, policies, annotations, and feedback. Its consumer-purpose orientation supports federated quality: domains can publish evidence under shared dimensions while consumers set consequence-specific thresholds. A single enterprise score would hide those differences.

W3C [SHACL](https://www.w3.org/TR/shacl/) validates RDF graphs against declared shapes and produces validation results. Shapes can require owner, policy, version, evidence, or lifecycle metadata in federated exchanges. Passing a shape proves declared structural constraints were satisfied under that evaluation, not that governance authority or control effectiveness is genuine.

Together these sources support an architecture with a legitimate coordinating center, explicit role and resource allocation, bounded local authority, interoperable metadata and policy, provenance, measurable quality, and machine-checkable profiles. The particular constitution, decision rights, risk tolerances, and legal obligations remain organizational decisions.

## Prerequisites and Retrieval

You should understand data domains, operating models, organizational authority, enterprise architecture, risk management, privacy, security, legal and records obligations, catalogs, metadata, lineage, data quality, contracts, policies, identity, access control, data products, service objectives, APIs, events, distributed systems, audit, incident response, and lifecycle management.

Retrieve governance, management, authority, accountability, responsibility, decision right, delegation, reservation, domain, federation, subsidiarity, constitution, charter, owner, steward, custodian, producer, consumer, controller, processor, trustee, council, forum, baseline, profile, policy, rule, standard, control, evidence, attestation, assessment, assurance, conformance, effectiveness, exception, waiver, conflict, appeal, quorum, escalation, recusal, externality, obligation, data product, control plane, data plane, portability, recovery, amendment, deprecation, retirement, and exit.

As a retrieval test, consider a marketing domain that wants to publish a customer feature to a fraud domain. Ask who may authorize the purpose; which party defines customer and feature meaning; who owns source quality; who verifies consent, lawful basis, minimization, retention, and geography; whether the platform merely enforces or may decide policy; which contract and versions apply; which evidence is current; who can accept residual risk; how the individual can obtain remedy; and which forum resolves disagreement. A named owner, catalog entry, or green dashboard does not answer those questions.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish governance from management, ownership from stewardship, and accountability from execution;
2. design a federation constitution with reserved, delegated, shared, and prohibited decisions;
3. choose domain boundaries using responsibility, knowledge, control, externalities, and change rather than organization charts alone;
4. define roles, decision records, consultation, escalation, conflict, appeal, recusal, and amendment;
5. establish shared minimum controls while permitting evidence-backed domain specialization;
6. govern data products, metadata, semantics, access, quality, retention, sharing, and change across boundaries;
7. build control-plane services for policy, evidence, exceptions, catalogs, workflows, events, and assurance;
8. measure conformance, effectiveness, service, risk, adoption, and outcomes with explicit denominators;
9. operate incidents, correction, recovery, reorganization, vendor boundaries, and federation exit; and
10. identify conditions under which centralized, federated, or more autonomous governance is appropriate.

## Core Exposition

**Define governance as a decision system.** Begin with recurring decisions: create a dataset, classify a field, approve a purpose, grant access, publish a product, set a quality threshold, accept an exception, change a definition, share externally, retain, delete, correct, or retire.

For each decision, state the object, requester, decider, consulted parties, implementer, evidence, constraints, deadline, effective time, record, appeal, and outcome. Committee names and role charts are secondary representations of this decision topology.

**Separate governance from management.** Governance evaluates stakeholder needs and risk, directs policy and priority, and monitors performance and conformance. Management plans and executes within that direction.

A governance council should not become the operational ticket queue for every access request or metadata edit. Conversely, a platform team cannot make risk-acceptance decisions merely because it implements the control.

**Write a federation constitution.** Define purpose, scope, members, mandatory principles, nondelegable obligations, reserved powers, delegation rules, shared decisions, voting or consent, quorum, recusal, records, evidence, conflicts, appeals, emergency authority, amendments, funding, review, and exit.

Keep the constitution small enough to remain intelligible. Put volatile procedures, profiles, and thresholds in versioned subordinate instruments with explicit authority.

**Identify nondelegable obligations.** Applicable law, contractual commitments, individual rights, fiduciary duties, safety, security, records, audit, and enterprise risk appetite can constrain every domain. A domain may often choose implementation but not waive the obligation.

Map each nondelegable obligation to an accountable authority, enforceable control objective, acceptable evidence, exception policy, reporting path, and remedy. Avoid reducing legal text directly to a Boolean rule without interpretation and review.

**Reserve only genuinely shared decisions.** Enterprise identity namespaces, critical classifications, cross-domain definitions, minimum security and privacy controls, regulated sharing, high-consequence risk acceptance, common interoperability profiles, and federation membership often require shared authority.

If the center reserves every naming, schema, quality, access, and lifecycle decision, federation becomes centralized governance with distributed labor. Reservation must follow consequence, not institutional preference.

**Delegate bounded local decisions.** A delegation names grantor, grantee, decision type, asset scope, purposes, environments, policy version, thresholds, evidence, effective interval, monitoring, revocation, and escalation.

Delegation does not transfer the grantor's accountability unless the governing system explicitly and legitimately changes it. It must be discoverable and testable at the time a decision is made.

**Apply subsidiarity carefully.** Place a decision with the lowest competent authority that understands the context, controls the implementation, and contains the consequences. Escalate when effects cross domains, create shared precedent, affect protected parties, exceed risk tolerance, or cannot be reversed locally.

Low organizational level is not automatically local competence. A domain lacking subject expertise, independence, or capacity should not receive authority merely to make the chart symmetrical.

**Design domains as responsibility boundaries.** A durable domain has a coherent subject or capability, stable language, producers and consumers, operating control, identifiable outcomes, and people able to make and implement decisions.

Avoid equating a domain with a database, application, squad, vendor, or current department. Organizational restructures should not silently reassign data authority or break stable identities.

**Map externalities.** A local schema rename can break consumers; a retention choice can violate a shared record duty; a local customer definition can distort enterprise reporting; a cheap quality threshold can transfer incident cost downstream.

Maintain boundary maps of products, consumers, policies, identities, semantic mappings, quality dependencies, affected populations, financial exposure, and recovery coupling. Use those externalities to set consultation and escalation.

**Make accountability singular at decision scope.** Several people can contribute, approve controls, or implement work, but the system must identify who answers for the resulting decision and unresolved risk.

Avoid multiple undifferentiated `A` entries in a RACI chart. Split the decision or name one accountable role and preserve required concurrence from independent authorities.

**Distinguish owner, steward, and custodian.** An owner is accountable for a bounded outcome and has authority to decide or escalate. A steward coordinates definitions, quality, metadata, issues, and lifecycle. A custodian implements storage, protection, access, backup, deletion, and technical controls.

These functions can be teams rather than individuals. Record role identity separately from current assignee, require deputies, and test capacity, authority, competence, and conflicts of interest.

**Model producer and consumer duties.** Producers publish identity, semantics, provenance, quality evidence, policy, interfaces, changes, service objectives, support, retention, and retirement. Consumers state purpose, authorization, required observations, transformations, local controls, feedback, and exit.

Ownership does not move wholesale with a copy. The producer remains accountable for its contract and assertions; the consumer becomes accountable for its use and derived products.

**Treat platforms as capability providers.** A platform can supply catalogs, policy engines, lineage, quality measurement, workflow, identity, contracts, audit, and self-service paths. It enforces declared rules and records evidence.

Platform operators should not become de facto business owners or risk authorities. Every automated denial or grant must resolve to a policy authority and applicable version.

**Establish a minimum control baseline.** Cover asset and product identity, ownership, metadata, classification, purpose, access, semantics, quality evidence, lineage, change, retention, deletion, incidents, audit, recovery, and closure.

State control objectives and required outcomes before mandating products. Domains can choose implementations when they produce comparable evidence and meet interface requirements.

**Permit local strengthening and specialization.** A health, finance, research, or safety domain may need stricter review, lower access, higher lineage depth, or longer evidence retention. Record the local profile and relation to the baseline.

Do not let customization redefine shared terms incompatibly without a mapping. Domain policy must not silently weaken a nondelegable requirement.

**Define policy precedence without hiding conflict.** Applicable law and rights can constrain contract, enterprise policy, domain policy, and product rules, but simple ordered precedence is insufficient when rules address different actions or jurisdictions.

Normalize policy subjects, assets, actions, purposes, constraints, duties, authorities, versions, and effective time. Detect contradictory permission, prohibition, obligation, retention, and deletion outcomes and route them to a named authority.

**Use profiles as federation contracts.** A profile selects mandatory and optional fields, vocabularies, controls, evidence, thresholds, and extension rules for a use or boundary. Domains publish conformance against immutable profile versions.

Profiles reduce global uniformity while preserving interoperability. Control proliferation becomes a risk when profiles overlap without identity, ownership, compatibility, or retirement.

**Govern data products at boundaries.** A product is more than a dataset. It includes stable identity, purpose, intended consumers, schema, semantics, quality, policy, provenance, interfaces, service objectives, support, change policy, cost, retention, and lifecycle.

Certification should be profile- and version-specific. A product fit for aggregate planning may remain unsafe for individual eligibility decisions.

**Keep authoritative assertions attributable.** A shared catalog can aggregate domain descriptions, central classifications, policy decisions, quality measurements, consumer feedback, and automated observations. Each assertion retains source, authority, method, version, and time.

The catalog's presence is not authority. Interfaces must distinguish asserted, inferred, disputed, verified, stale, superseded, and retired claims.

**Federate semantics deliberately.** Domains own bounded concepts and metrics; shared authorities own selected namespaces, mapping relations, and cross-domain definitions. Preserve disagreement and loss rather than forcing label-based equivalence.

Cross-domain decisions require explicit semantic profiles. A concept accepted for discovery may be inadequate for calculation, policy enforcement, or model training.

**Federate quality evidence.** Define shared dimensions and measurement envelopes, but allow domain metrics and consumer thresholds. Every measurement identifies resource, version, population, window, method, producer, and limitations.

The producer should publish known defects and service behavior. Consumers decide fitness for their consequence within policy and report outcome evidence back to producers.

**Govern access as purpose-bound decision.** Identity and role are inputs, not the complete decision. Evaluate actor, asset, action, purpose, jurisdiction, consent or authority, classification, environment, time, obligations, and requested granularity.

Central policy can set nondelegable controls; domain owners can approve bounded uses; custodians enforce. Emergency access needs explicit authority, short expiry, logging, retrospective review, and remedy.

**Coordinate retention and deletion.** A domain cannot promise deletion without knowing copies, legal holds, records duties, derived products, models, backups, and consumer contracts. Nor can a central schedule understand every operational and scientific need without local evidence.

Use purpose- and record-class-specific schedules, evented obligations, consumer acknowledgement, exception, proof of execution, restore behavior, and reconciliation. Conflicts require legal and governance decisions, not arbitrary maximum retention.

**Use a logical control plane.** Services may include identity and namespace registry, catalogs, policy registry and evaluation, profiles, contracts, workflow, exceptions, evidence, lineage, quality, events, decision records, and assurance dashboards.

The control plane must be versioned, authorized, observable, recoverable, and available enough for its enforcement mode. Central metadata outage must not silently grant access or corrupt local processing.

**Keep the data plane locally evolvable.** Domains can choose storage and compute suited to their workloads when their boundary products meet shared identity, interface, policy, evidence, and lifecycle contracts.

Conformance adapters can bridge technologies, but adapters must not conceal semantic loss, stale policy, or unsupported controls.

**Make governance workflows stateful.** A proposal moves through validation, consultation, risk or legal review, decision, implementation, verification, activation, monitoring, renewal, correction, and closure. Each transition has authority and preconditions.

Email approval without durable identity, scope, evidence, version, and expiry cannot support reliable enforcement or audit.

**Design conflict resolution.** Classify conflicts among authority, policy, meaning, quality, priority, funding, risk, evidence, and timing. Attempt local negotiation where consequences remain local; otherwise escalate through a published forum.

Record positions, evidence, affected parties, recusals, interim controls, deadline, decision, dissent, appeal, effective time, and precedent scope. Do not erase legitimate local definitions to make a dashboard green.

**Support appeal and affected-party remedy.** Governance decisions can deny access, retain data, change definitions, or affect people through downstream systems. Provide challenge paths proportionate to consequence.

Appeal should be independent enough to review the original authority. Preserve original evidence and actions so correction can identify and remedy effects.

**Govern exceptions as debt with an owner.** An exception names requirement, scope, reason, evidence, risk, affected parties, compensating controls, approver, start, expiry, monitoring, renewal limit, and exit conditions.

Auto-expire where safe and fail visibly. Repeated renewal should trigger baseline amendment, investment, or denial—not normalization of an undocumented alternative regime.

**Separate attestation from assessment.** A domain can attest that a control exists. An assessor can inspect design and operation. Independent assurance can challenge evidence for higher-consequence decisions.

None proves perpetual effectiveness. Bind evidence to control version, asset scope, method, sample, period, assessor, findings, and limitations.

**Test policy and evidence interfaces.** Validate schemas, identities, signatures, authority resolution, temporal applicability, conflict detection, default behavior, revocation, stale evidence, consumer interpretation, and fail-safe operation.

Run adversarial cases: unknown owner, two applicable policies, expired delegation, missing purpose, restore of retired exception, compromised steward, partial catalog outage, and cross-jurisdiction transfer.

**Observe the operating model.** Measure unresolved ownership, decision latency, expired evidence, exception age, cross-domain conflicts, consumer incidents, contract adoption, policy-denial reasons, quality breach duration, correction time, and recovery outcomes.

Segment by domain, consequence, product, profile, and affected population. Averages can hide an ungoverned critical asset behind thousands of low-risk catalog entries.

**Distinguish activity, conformance, effectiveness, and outcome.** Meetings held, terms created, and tickets closed are activities. Required metadata present is conformance. Unauthorized use prevented or defects detected is control effectiveness. Better decisions and reduced harm are outcomes.

Do not infer one category from another. Report denominators, uncertainty, counterevidence, and gaming risk.

**Fund the federation.** Shared infrastructure, independent assurance, cross-domain standards, training, and high-consequence remediation require central or pooled investment. Domains need capacity for stewardship, product operation, quality, and consumer support.

Chargeback can reveal demand but can discourage metadata, reporting, or safe sharing. Allocate cost according to control obligation, producer externality, consumer value, and ability to influence the outcome.

**Develop governance capability.** Owners need decision and risk competence; stewards need domain, metadata, quality, facilitation, and lifecycle skills; custodians need implementation and recovery skills; reviewers need independence and policy knowledge.

Provide learning paths, office hours, templates, reference implementations, simulations, and communities of practice. Tool access is not competence.

**Design incidents for federated authority.** An incident can originate in one domain and affect many consumers. Establish severity, notification, evidence preservation, temporary authority, containment, consumer reconciliation, affected-party communication, correction, and review.

The incident commander coordinates response but does not permanently acquire data ownership. Emergency decisions expire and are reviewed.

**Correct governance state immutably.** Do not rewrite an old approval to look correct. Supersede the decision or policy, preserve original evidence, identify affected products and uses, re-evaluate where possible, notify, and record remedy.

Corrections may need both valid time and record time: when the rule should have applied and when the organization learned or decided it.

**Prepare for reorganization.** Transfer role assignments, delegations, products, policies, exceptions, contracts, unresolved issues, evidence, budgets, and on-call duties through an explicit succession plan.

Stable domain and asset identities should survive team renames. Validate that no decision resolves to a departed person or obsolete group.

**Govern vendors and external participants.** Contracts define roles, permitted purposes, instructions, controls, evidence, subcontractors, location, incident notification, audit, portability, deletion, and exit. Platform configuration does not replace these decisions.

Treat vendor attestations as evidence with scope and limitations. Maintain independent inventory and recovery sufficient to change providers.

**Design recovery in governance order.** Back up constitutions, authorities, role assignments, policies, profiles, delegations, decisions, exceptions, catalogs, semantic mappings, contracts, evidence, audit, events, and tombstones.

Restore identity, authority, time, and policy before enabling automation. Reconcile domain copies, test denied and permitted cases, invalidate stale caches, verify critical products, and obtain accountable authorization to resume.

**Design federation exit.** A departing domain or organization exports stable identities, schemas, semantics, policy references, provenance, decisions, exceptions, evidence, histories, unresolved issues, consumer relationships, and tombstones in documented formats.

Revoke authority and credentials, end publication and events, migrate or close consumers, prove deletion where required, preserve historical interpretation, and ensure recovery cannot reactivate the former member.

**Choose the degree of federation by evidence.** Small organizations with tightly coupled work may need centralized governance. Highly autonomous domains with few shared consequences may use lightweight coordination. Regulated or cross-organizational ecosystems may require stronger common profiles and independent assurance.

Revisit allocation when decision latency, incident patterns, externalities, competence, law, organizational boundaries, or technology change. Federation is a revisable design, not a maturity destination.

## Definitions and Notation

Let a governed decision be `q = (object, action, scope, purpose, authority, constraints, evidence, time, outcome, appeal)`. Two decisions with the same label are distinct when any decision-relevant component differs.

Let domain `d = (identity, mandate, subjects, capabilities, authorities, products, consumers, obligations, resources, lifecycle)`. Membership in an organization unit is not sufficient to establish domain authority.

Let decision right `r = (grantor, grantee, decision_type, asset_scope, purpose_scope, constraints, evidence, effective, monitoring, revocation)`. A decision is authorized only if one active right contains all relevant dimensions.

Partition decision types into reserved `Q_c`, delegated `Q_d`, shared `Q_s`, and prohibited `Q_p`. The sets must be defined by scope; a decision may be delegated for low-risk internal use and reserved for external or high-consequence use.

Let baseline profile `b = (controls, evidence, thresholds, extensions, version, authority)`. Domain profile `p_d` conforms when it satisfies every applicable baseline outcome and every declared strengthening, with no unresolved weakening.

Let policy decision `Permit(a,x,u,t)` represent whether actor `a` may perform action `x` for use `u` at time `t`. Unknown authority, purpose, or applicable policy is a distinct outcome from permit or deny.

Let product `p = (identity, domain, purpose, interface, schema, semantics, policy, quality, provenance, service, support, change, retention, version)`. Product certification is always relative to a named profile and evaluation time.

Let evidence item `e = (claim, subject, method, producer, assessor, period, result, limitations, version, integrity)`. Evidence supports a claim under its scope but is not identical to the claim or outcome.

Let exception `w = (requirement, scope, rationale, risk, compensating_controls, owner, approver, start, expiry, monitoring, closure)`. An exception without expiry or closure is an alternative policy and requires constitutional authority.

Let conflict `x = (claims, authorities, scopes, evidence, affected_parties, interim_controls, forum, decision, dissent, appeal, effective)`. A precedence rule can resolve only conflicts it was authorized and specified to resolve.

For applicable controls `A(p,t)`, define conformance `Conf(p,t) = |{c in A(p,t): evidence_current(p,c,t)}| / |A(p,t)|`. Publish missing, not-applicable, excepted, and failed controls separately.

Let `Eff(c,o,w)` measure whether control `c` achieved outcome `o` during window `w` under a declared method. Conformance and effectiveness are different predicates.

Let `Ext(d,q)` be consequences of domain decision `q` outside domain `d`. Subsidiarity permits local decision only when authority is valid and externalities remain within declared tolerance or required consultation resolves them.

Let `Closed(d)` require no active decision right, credential, product publication, consumer contract, exception, event source, unresolved obligation, or recovery path for the departed domain, while required historical records remain resolvable.

## Mechanisms, Invariants, or Proof Structure

Use the following gates to design and review a federated governance system.

**Purpose gate.** State mission, stakeholders, affected parties, decisions, value, harms, boundaries, and conditions that justify federation.

**Constitution gate.** Record principles, mandatory duties, reserved and delegated powers, amendment, funding, evidence, conflict, appeal, emergency authority, and exit.

**Domain gate.** Verify stable mandate, subject knowledge, operating control, products, consumers, outcomes, resources, lifecycle, and externalities.

**Decision-right gate.** Resolve decision type, scope, purpose, authority, consultation, evidence, time, implementation, monitoring, revocation, and appeal.

**Role gate.** Separate accountable outcome owner, operational stewardship, technical custody, production, consumption, risk acceptance, legal interpretation, and independent assurance.

**Baseline gate.** Define minimum identity, metadata, protection, semantics, quality, access, sharing, change, audit, recovery, and closure outcomes.

**Profile gate.** Bind local specializations to baseline versions, extension rules, evidence, thresholds, compatibility, exceptions, and retirement.

**Product gate.** Check purpose, stable identity, interface, schema, meaning, provenance, policy, quality, service, support, change, retention, consumers, and lifecycle.

**Policy gate.** Resolve subject, asset, action, purpose, jurisdiction, permissions, prohibitions, duties, constraints, authority, version, conflict, and default.

**Evidence gate.** Link claim, subject, method, producer, independence, sample, period, integrity, result, limitation, expiry, and counterevidence.

**Exception gate.** Require stated deviation, bounded scope, risk, compensating controls, accountable approval, expiry, monitoring, renewal limit, and closure.

**Conflict gate.** Preserve positions and authorities, protect affected parties, set interim controls, provide a legitimate forum, record dissent, and support appeal.

**Interoperability gate.** Validate identities, metadata, semantics, profiles, policies, evidence, APIs, events, versions, portability, and declared loss.

**Operations gate.** Observe activity, conformance, effectiveness, service, risk, adoption, incident, correction, capacity, cost, and outcome with denominators.

**Incident gate.** Establish severity, temporary authority, containment, evidence, notification, consumer reconciliation, remedy, and retrospective learning.

**Recovery gate.** Restore constitutional authority, identities, policies, delegations, evidence, catalogs, products, decisions, and tombstones before automation.

**Closure gate.** Revoke rights and credentials, close products and consumers, resolve obligations and exceptions, stop events, update recovery, and retain required history.

### Executable evidence: delegated decisions and baseline conformance

This Python example classifies six invented decision rights, evaluates five invented products against a four-control baseline, and summarizes two invented conflicts.

<!-- bijux-verify: {"id":"delegated-decisions-and-baseline-conformance","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"domains=3\ndecision_rights=6\nlocally_decidable=4\nshared_approval=1\ncentrally_reserved=1\nproducts=5\nbaseline_controls=4\nconforming_products=3\nexcepted_products=1\nblocked_products=1\nconflicts=2\nclosed_conflicts=1\nopen_conflicts=1\n","stderr":""}} -->
```python
domains = {"commerce", "risk", "support"}

decision_rights = [
    {"decision": "commerce_quality", "mode": "local"},
    {"decision": "risk_quality", "mode": "local"},
    {"decision": "support_retention_detail", "mode": "local"},
    {"decision": "commerce_schema", "mode": "local"},
    {"decision": "shared_customer_definition", "mode": "shared"},
    {"decision": "external_regulated_transfer", "mode": "central"},
]

baseline = {"owner", "policy", "quality", "lifecycle"}
products = {
    "orders": {"controls": baseline, "exception": False},
    "payments": {"controls": baseline, "exception": False},
    "cases": {"controls": baseline, "exception": False},
    "features": {"controls": {"owner", "policy", "quality"}, "exception": True},
    "legacy_export": {"controls": {"owner", "quality"}, "exception": False},
}

conforming = {
    name for name, product in products.items() if baseline <= product["controls"]
}
excepted = {
    name
    for name, product in products.items()
    if not baseline <= product["controls"] and product["exception"]
}
blocked = set(products) - conforming - excepted
conflicts = {"customer_meaning": "closed", "retention_scope": "open"}

print(f"domains={len(domains)}")
print(f"decision_rights={len(decision_rights)}")
print(f"locally_decidable={sum(r['mode'] == 'local' for r in decision_rights)}")
print(f"shared_approval={sum(r['mode'] == 'shared' for r in decision_rights)}")
print(f"centrally_reserved={sum(r['mode'] == 'central' for r in decision_rights)}")
print(f"products={len(products)}")
print(f"baseline_controls={len(baseline)}")
print(f"conforming_products={len(conforming)}")
print(f"excepted_products={len(excepted)}")
print(f"blocked_products={len(blocked)}")
print(f"conflicts={len(conflicts)}")
print(f"closed_conflicts={sum(state == 'closed' for state in conflicts.values())}")
print(f"open_conflicts={sum(state == 'open' for state in conflicts.values())}")
```

The expected output reports three domains, six decision rights, four local decisions, one shared decision, one central reservation, five products, four baseline controls, three conforming products, one excepted product, one blocked product, two conflicts, one closed conflict, and one open conflict on separate lines.

The evidence is intentionally narrow. Strings do not establish legitimate domains, authorities, policies, controls, products, or conflict outcomes. Set inclusion treats every control as equally important and says nothing about evidence currency, implementation, independence, effectiveness, or consumer fitness. A Boolean exception has no scope, approver, expiry, compensation, risk, or closure. The code does not evaluate law, rights, purpose, semantics, data, enforcement, affected-party outcomes, or recovery. Production assurance requires constitutional authority, complete decision records, versioned profiles, attributable evidence, policy interpretation, representative tests, independent review where warranted, operational observation, incident exercises, correction, and exit verification.

## Alternatives and Trade-Offs

**Centralized governance.** One authority can create consistent rules and clear escalation. It can become slow, context-poor, politically distant, and unable to process domain-scale decisions.

**Federated governance.** Domains retain context and operating authority within a shared constitution. Boundary design, evidence exchange, conflict resolution, and capability disparities require sustained investment.

**Decentralized autonomy.** Teams move quickly with few shared controls. Cross-domain meaning, rights, security, quality, and lifecycle externalities can become invisible or expensive.

**Enterprise council.** Senior representation can reserve priorities and risk decisions. Meetings become ceremonial if members lack preparation, decision authority, or follow-through.

**Network of domain councils.** Local forums improve context and throughput. Shared precedent and incompatible decisions need a coordinating mechanism.

**Named individual owners.** One person gives discoverable accountability. Availability, overload, turnover, conflicts, and insufficient authority create fragility.

**Accountable owner teams.** Teams provide capacity and continuity. The particular decision and answerable role can become ambiguous unless explicitly resolved.

**RACI matrix.** It communicates participation compactly. Static letters rarely specify decision scope, constraints, evidence, effective time, or escalation.

**Decision-right registry.** Machine-resolvable delegations support workflow and enforcement. Maintenance, identity, temporal logic, and false precision add operational cost.

**Policy as prose.** Humans can express nuance and judgment. Implementations diverge unless controls, examples, interpretations, and evidence are linked.

**Policy as code.** Versioned tests and consistent enforcement improve traceability. Code cannot choose legitimate policy and can conceal interpretive or data errors.

**Uniform global baseline.** Comparison and shared services become easier. Excessive detail can impose irrelevant controls and suppress necessary domain specialization.

**Outcome-based baseline.** Domains can innovate and fit local technology. Evidence comparability and assurance become harder.

**Technology-specific baseline.** Controls are concrete and easier to audit. Vendor lock-in and obsolete implementation requirements age poorly.

**Central catalog.** One discovery surface improves search and aggregation. It can become stale, overtrusted, or a bottleneck for domain assertion.

**Federated catalogs.** Domains publish on their own cadence and preserve local richness. Identity, profile, harvesting, ranking, authorization, and availability require coordination.

**Central data platform.** Shared enforcement and operations reduce duplicated capability. The platform can accumulate ownership, coupling, and failure blast radius.

**Domain platforms.** Workload fit and autonomy improve. Duplicate cost and inconsistent controls increase without common interfaces and evidence.

**Prepublication certification.** Risk is reviewed before broad exposure. Review queues slow changes and certification can become a permanent trust badge.

**Continuous conformance.** Drift and expiry become visible quickly. Continuous signals can reward easily measured controls while missing substantive outcomes.

**Self-attestation.** It is scalable and close to implementation. Incentives, misunderstanding, and lack of independence weaken assurance.

**Independent assessment.** Credibility improves for consequential controls. Cost, latency, sample limits, and assessor distance from context remain.

**Consumer-defined quality thresholds.** Fitness aligns with actual decisions. Producers face many thresholds and may not know which defects to prioritize.

**Producer service objectives.** A stable contract simplifies operations. One threshold may be inadequate across consumer consequences.

**Strict policy precedence.** Automated resolution is predictable. Rules with different scope can be incorrectly flattened, hiding real conflict.

**Explicit conflict workflow.** Ambiguity and authority disagreement stay visible. Resolution requires skilled people and can delay use.

**Permanent exceptions.** Legacy operations remain possible. Unbounded deviations erase the baseline and obscure accepted risk.

**Time-bounded exceptions.** Risk and closure stay visible. Frequent renewals consume review capacity and can create operational cliffs.

**Maturity scoring.** A compact score supports portfolio discussion. Ordinal labels can hide critical gaps, incomparable domains, and gaming.

**Decision- and product-level evidence.** Risk is visible at actionable granularity. Collection, retention, authorization, and aggregation cost more.

## Failure Modes and Misconceptions

**“Federation means every domain decides independently.”** Federation requires a shared constitution and coordination for cross-boundary consequences.

**“A central council makes governance centralized.”** A center can reserve only shared decisions while delegating local authority.

**“Decentralization eliminates bureaucracy.”** It can multiply incompatible local procedures and hidden escalation.

**“The organization chart defines domains.”** Reporting lines can change faster than subject, data, capability, and consumer boundaries.

**“Every application is a domain.”** Applications are technical systems and often span or fragment durable responsibility boundaries.

**“Every domain should have identical roles.”** Small and large domains can implement functions differently if authority and outcomes remain clear.

**“Naming an owner creates accountability.”** The owner also needs mandate, competence, time, resources, evidence, and escalation.

**“Several accountable owners are safer.”** Ambiguous accountability often means nobody answers for the specific outcome.

**“The steward owns all data work.”** Producers, custodians, consumers, risk authorities, and executives retain distinct duties.

**“The platform team owns policy because it wrote the rules.”** Implementation authority is not policy legitimacy or risk acceptance.

**“Legal decides every data question.”** Legal interprets obligations; business, risk, technical, and affected-party evidence also shape decisions.

**“A RACI is a decision model.”** It omits asset and purpose scope, constraints, evidence, time, transition, and appeal.

**“If a decision is not reserved, it is delegated.”** Unspecified authority is a governance gap.

**“Delegation transfers all accountability.”** The grantor can retain oversight and nondelegable duties.

**“Local decisions have local consequences.”** Shared identities, reports, models, policies, and consumers transmit externalities.

**“One baseline fits every risk.”** Domains and uses can require justified strengthening and differentiated assurance.

**“Local policy may override the baseline.”** Specialization cannot silently weaken mandatory obligations.

**“Stricter policy always wins.”** Retention and deletion duties can conflict; scope and authority require interpretation.

**“Policy as code removes ambiguity.”** Code executes an interpretation and can faithfully automate the wrong rule.

**“A permit result proves lawful use.”** Input completeness, policy authority, enforcement, purpose, and downstream behavior remain separate.

**“Cataloged means governed.”** A record can be stale, inferred, disputed, incomplete, or unauthorized.

**“The catalog is the source of truth.”** It aggregates assertions whose authorities and versions can differ.

**“A data product is just a clean table.”** Products include meaning, policy, evidence, interface, service, support, and lifecycle.

**“Product certification is universal.”** Fitness is relative to profile, version, consumer, purpose, and time.

**“Producers own consumer outcomes.”** Consumers remain accountable for their purpose, transformations, decisions, and controls.

**“Consumers can ignore producer defects.”** They must report consequential evidence and manage their own risk.

**“Quality can be governed with one score.”** Dimensions, populations, windows, methods, and decision thresholds differ.

**“Lineage transfers accountability.”** Derivation reveals dependencies but does not reassign authority or prove preserved meaning.

**“Provenance proves truth.”** It explains origin and activity, not correctness or legitimacy.

**“A passed schema validates governance.”** Structural conformance does not prove evidence or control effectiveness.

**“Self-attestation is assurance.”** It is one evidence source with incentives and limitations.

**“Audit once means compliant forever.”** Policies, assets, controls, people, threats, and uses change.

**“Exceptions are harmless if approved.”** They create bounded risk and operational debt that require monitoring and closure.

**“Renewing an exception is closure.”** Repetition can reveal an unrealistic baseline or unfunded obligation.

**“Policy precedence resolves every conflict.”** Differing jurisdiction, purpose, authority, and duties often require adjudication.

**“Disagreement shows weak governance.”** Visible, reasoned disagreement can protect legitimate domain or stakeholder interests.

**“Escalation should always go upward.”** Some conflicts require independent review, peer coordination, or affected-party appeal.

**“More governance meetings mean maturity.”** Activity says little about conformance, effectiveness, risk, or outcomes.

**“More catalog coverage means less risk.”** A missing critical product can matter more than thousands of low-risk entries.

**“Automation makes governance scalable.”** It scales both valid policy and systematic mistakes.

**“Central tools create common semantics.”** Shared storage of labels does not establish concept or metric equivalence.

**“Federation reduces platform reliability needs.”** Shared identity, policy, and evidence services can become critical dependencies.

**“An outage should default to permit.”** That can expose protected data; failure behavior must follow consequence and cached authority.

**“An outage should always default to deny.”** That can endanger essential operations; explicitly governed continuity modes are needed.

**“Reorganization automatically transfers ownership.”** Delegations, conflicts, products, evidence, and support require explicit succession.

**“Vendor certification transfers accountability.”** The organization retains duties for selection, instruction, monitoring, use, and exit.

**“Closing access closes the domain.”** Products, events, copies, exceptions, contracts, audit, and restore paths can remain.

**“Federated governance is the final maturity stage.”** Appropriate allocation depends on scale, coupling, risk, capability, and change.

## Worked Examples

### Example 1

A commerce domain may change descriptive fields in its order product locally. Removing the shared order identifier or changing its issuance rule affects fraud, support, finance, and legal evidence, so the delegation requires cross-domain consultation and shared approval. The registry resolves the decision by type and scope rather than by team seniority.

### Example 2

A central privacy authority defines minimum purpose, minimization, rights, transfer, and retention outcomes. The research domain adds an ethics review, restricted environment, and publication disclosure profile. Its additions strengthen the baseline; they do not grant authority to waive individual rights.

### Example 3

A catalog aggregates an owner assertion from the domain, classification from security, policy from privacy, lineage from the platform, and quality measurement from a pipeline. Each assertion retains source and time. A consumer sees that quality is current but the owner's delegation expired, so high-consequence access is blocked.

### Example 4

Support and finance both use `case_closed`. Support means no active work; finance means every financial obligation is settled. A federation forum preserves both concepts, defines mappings and a shared settlement profile, and rejects a proposal to make the labels exactly equivalent.

### Example 5

A legacy export lacks lifecycle metadata. Its owner receives a ninety-day exception with a named risk, restricted consumers, compensating inventory, weekly monitoring, funded remediation, and automatic expiry. A second renewal requires amendment review because the original baseline may be unrealistic for the legacy class.

### Example 6

A policy engine receives two applicable rules: delete after thirty days and retain for a seven-year legal hold. It returns conflict rather than selecting the longest period. Records and privacy authorities resolve scope, preserve the hold, restrict use, record the decision, and define deletion after release.

### Example 7

A domain certifies a product against a discovery profile. A lending team attempts to use it for individual eligibility. The control plane rejects reuse of the discovery certificate because the eligibility profile requires different semantics, quality evidence, fairness review, recourse, and monitoring.

### Example 8

A shared policy service is unavailable. Public catalog discovery continues using a signed, unexpired read policy bundle. A sensitive export fails closed. An emergency clinical workflow uses separately authorized continuity rules, logs every access, and triggers retrospective review after recovery.

### Example 9

A reorganization dissolves the loyalty team. Stable product and concept identities move to commerce, but a succession workflow separately transfers role assignments, budgets, on-call support, delegations, exceptions, consumer contracts, unresolved defects, and evidence. Nothing is reassigned merely from a group rename.

### Example 10

An external data provider exits the federation. The organization freezes new use, exports versioned contracts and provenance, migrates authorized consumers, revokes credentials, closes event subscriptions, verifies required deletion, retains legally required decisions, and tests that disaster recovery cannot reactivate the provider's authority.

## Cross-Program Connections

**Systems Engineering.** Federation is a system of authority, incentives, feedback, boundaries, and externalities. Local optimization can produce enterprise harm unless cross-domain outcomes are observable and correctable.

**Platform Engineering.** Catalogs, policy engines, identity, workflows, contracts, evidence, lineage, quality, events, and paved roads implement the control plane while domains retain bounded product authority.

**API and Service Engineering.** Decision, policy, evidence, exception, and catalog services require stable resources, concurrency, idempotency, authorization, versioning, event semantics, and reconciliation.

**Data Engineering.** Producers operationalize schemas, tests, lineage, quality, retention, deletion, replay, and change commitments whose evidence supports governance decisions.

**Security Engineering.** Least privilege, separation of duties, threat modeling, incident response, key management, evidence integrity, and recovery constrain delegation and enforcement.

**Privacy Engineering.** Purpose, minimization, rights, consent, lawful authority, retention, deletion, affected-party remedy, and ecosystem roles are nondelegable or carefully bounded governance concerns.

**Software Architecture.** Bounded contexts, modularity, contracts, dependency direction, control planes, adapters, and lifecycle design shape the technical feasibility of federation.

**Organizational Design.** Mandates, decision rights, incentives, resources, competence, conflict, and accountability determine whether formal roles can operate.

**Governance, Risk, and Compliance.** Policy authority, controls, exceptions, assessment, audit, residual risk, obligations, evidence, and remedy connect federation to enterprise assurance.

**Analytics Engineering.** Shared metrics, semantic profiles, product contracts, lineage, quality thresholds, and restatement require both domain context and cross-domain authority.

**Machine Learning Engineering.** Training data, features, labels, model outputs, purpose changes, fairness, monitoring, and recourse often cross domains and amplify governance externalities.

**Economics and Finance.** Funding models, chargeback, externalized incident costs, shared infrastructure, option value, and risk concentration influence sustainable allocation of governance work.

## References

1. U.S. Federal Data Strategy, [“Data Governance Playbook”](https://resources.data.gov/assets/documents/fds-data-governance-playbook.pdf), 2020. Retrieved 2026-09-03.
2. U.S. Federal Data Strategy, [“Practices”](https://strategy.data.gov/practices/), retrieved 2026-09-03.
3. National Institute of Standards and Technology, [“NIST Privacy Framework: A Tool for Improving Privacy through Enterprise Risk Management”](https://www.nist.gov/privacy-framework/privacy-framework), 2020. Retrieved 2026-09-03.
4. UK Government Digital Service, [“Data Ownership Model”](https://www.gov.uk/government/publications/data-ownership-in-government/data-ownership-model), 2026. Retrieved 2026-09-03.
5. European Union, [“Interoperable Europe Act”](https://interoperable-europe.ec.europa.eu/Interoperable-Europe-Act-Regulation), 2024. Retrieved 2026-09-03.
6. National Institute of Standards and Technology, [“Cybersecurity Framework 2.0”](https://www.nist.gov/cyberframework), 2024. Retrieved 2026-09-03.
7. W3C, [“Data Catalog Vocabulary (DCAT), Version 3”](https://www.w3.org/TR/vocab-dcat-3/), 2024. Retrieved 2026-09-03.
8. W3C, [“ODRL Information Model 2.2”](https://www.w3.org/TR/odrl-model/), 2018. Retrieved 2026-09-03.
9. W3C, [“PROV-O: The PROV Ontology”](https://www.w3.org/TR/prov-o/), 2013. Retrieved 2026-09-03.
10. W3C, [“Data on the Web Best Practices: Data Quality Vocabulary”](https://www.w3.org/TR/vocab-dqv/), 2016. Retrieved 2026-09-03.
11. W3C, [“Shapes Constraint Language (SHACL)”](https://www.w3.org/TR/shacl/), 2017. Retrieved 2026-09-03.

## Exercises

### Exercise 1

Design a federation constitution for eight business domains, a central data platform, privacy, security, legal, records, and enterprise risk. Specify reserved, delegated, shared, and prohibited decisions; roles; evidence; conflicts; appeals; emergency authority; amendments; funding; and exit.

### Exercise 2

Define a baseline and domain profiles for customer, payments, research, and support products. Cover identity, metadata, semantics, policy, quality, lineage, access, retention, incidents, recovery, and closure while permitting justified local specialization.

### Exercise 3

Design a machine-operable decision-right, policy, evidence, and exception control plane. Include identities, APIs, events, temporal behavior, failure modes, authorization, reconciliation, audit, and tests.

### Exercise 4

Two domains disagree about customer meaning, retention, quality thresholds, and who may approve an external transfer. Design a conflict process with interim controls, evidence, authority, affected parties, recusal, decision, dissent, appeal, implementation, and precedent.

### Exercise 5

A regulated domain is reorganized and its external platform provider will be replaced. Design succession, product and consumer migration, evidence transfer, credential revocation, deletion, historical interpretation, recovery, and proof of closure.

## Answers to the Exercises

### Answer 1

Start with a concise constitution whose purpose is safe, useful, interoperable data decisions. Name membership and mandate. Reserve enterprise identity namespaces, nondelegable privacy, security, legal and records requirements, external regulated sharing, high-consequence risk acceptance, common control profiles, and federation membership. Delegate local schema, documentation, operational quality, support, and product evolution within thresholds. Make cross-domain definitions, shared metrics, common identifiers, major compatibility breaks, and boundary funding shared decisions. Prohibit uses outside law, rights, declared purpose, or accepted risk.

For each decision type, register asset and purpose scope, accountable authority, required consultation or concurrence, evidence, deadline, effective time, implementation owner, monitoring, revocation, and appeal. Owners answer for bounded outcomes; stewards coordinate metadata, quality, issue, and lifecycle work; custodians enforce technical controls; producers and consumers retain contract and use duties. Privacy, security, legal, records, and risk authorities remain independent where required.

Define quorum, recusal, transparent records, dissent, conflict escalation, affected-party remedy, and short-lived emergency authority with retrospective review. Amendments require impact analysis and versioned activation. Fund shared infrastructure and assurance centrally or through a published allocation, while domains receive stewardship and product-operation capacity. Exit revokes authority, closes dependencies, exports portable histories and evidence, and updates recovery. Review the constitution against incidents, latency, capability, and externalities rather than treating it as permanent.

### Answer 2

Create a versioned baseline with outcomes for stable identity, accountable owner and steward, purpose and consumers, schema and semantic contract, classification and access, provenance and lineage, quality measurement envelope, change and compatibility, retention and deletion, incident notification, audit evidence, backup and restore, deprecation, and closure. Define evidence type, currency, authority, severity, and default behavior for every control.

The customer profile adds governed party identity, source authority, matching limitations, consent or purpose, semantic mappings, correction, and affected-party rights. Payments adds integrity, reconciliation, segregation of duties, immutable audit, currency and amount semantics, stricter recovery, and financial records. Research adds protocol, ethics review, minimization, controlled environment, disclosure review, reproducibility, and publication conditions. Support adds case confidentiality, free-text protection, operational timeliness, attachment controls, and case retention.

Each profile identifies its baseline version, additions, stricter thresholds, extension vocabulary, evidence, owner, effective interval, compatibility, exceptions, and retirement. A domain may choose technology and strengthen controls. It cannot redefine shared identity invisibly or weaken mandatory rights. Certify products only against named profile versions and intended uses, and require consumers with higher-consequence uses to supply additional fitness evidence.

### Answer 3

Give actors, roles, domains, assets, products, decision types, policies, controls, profiles, evidence, exceptions, conflicts, and decisions stable identities. A decision-right resource names grantor, grantee, object and purpose scope, constraints, evidence, effective interval, monitoring, and revocation. Policy resources name subject, asset, action, purpose, permission or prohibition, duties, constraints, authority, version, and jurisdiction. Evidence names claim, method, producer, assessor, period, integrity, findings, and limitations. Exceptions add deviation, risk, compensating controls, approver, expiry, and closure.

Expose immutable version reads, current authorized resolution, proposals, conditional decisions, renewals, revocations, and reconciliation. Use optimistic concurrency and idempotent commands. Events distinguish proposal, approval, activation, expiry, revocation, conflict, correction, and closure and carry independent identity, causation, subject, version, and effective time. Store canonical change, decision, audit, and outbox atomically; consumers use inbox deduplication and reconcile from immutable state.

Authorize both resource and field visibility. Protect sensitive policy, purpose, evidence, and behavioral metadata. Test expired delegation, conflicting policy, missing purpose, stale evidence, forged authority, retroactive rule, partial outage, duplicated event, restore, and revoked exception. Decide fail-open, fail-closed, cached, or continuity behavior per consequence. Preserve original decisions and issue corrections rather than rewriting history.

### Answer 4

Open four linked conflict records rather than one vague dispute. Preserve each claim, scope, authority, evidence, consumer impact, affected population, timing, and reversibility. Customer meaning goes to semantic authorities and named cross-domain consumers; retention includes privacy, records, legal, and data owners; quality includes producer capability and consumer consequence; external transfer requires the authority reserved in the constitution.

Apply interim controls: keep domain-specific customer concepts, block unsafe joins, preserve rather than destroy disputed records under restricted use, label insufficient quality, and pause the transfer. Set deadlines and responsible forums. Require recusals for conflicts of interest and obtain independent or affected-party input where consequence warrants it. The decision record states applicable policy versions, findings, rationale, conditions, dissent, effective time, implementation, monitoring, and appeal.

Implement versioned mappings instead of false equivalence, a purpose-specific retention resolution, producer objectives plus consumer thresholds, and the authorized transfer decision with duties and evidence. Notify products and consumers, test policy and technical changes, and monitor outcomes. Mark precedent narrowly so a decision for one jurisdiction or use is not generalized automatically. Preserve appeal and correct affected decisions if later evidence changes the result.

### Answer 5

Inventory stable domain, product, concept, policy, role, delegation, credential, interface, event, consumer, exception, evidence, retention, incident, and recovery identities. Assign a succession authority and dates. Transfer role assignments, budget, stewardship queues, on-call duty, unresolved conflicts, risk acceptances, legal and records obligations, and support contracts explicitly; do not infer transfer from renamed groups.

For the provider replacement, map source and target capabilities, semantics, policy enforcement, evidence, locations, subprocessors, service objectives, history, and deletion behavior. Export immutable metadata, provenance, decisions, audit, schemas, mappings, quality histories, exceptions, and tombstones. Dual-run representative and adversarial products, reconcile counts and decision-relevant observations, canary consumers, preserve rollback, and prevent new dependencies on the departing service.

After acceptance, revoke human and machine credentials, rotate secrets and keys, stop publication and event delivery, close network paths, migrate or terminate consumer contracts, resolve exceptions, and obtain scoped deletion evidence where required. Retain historical interpretation and audit under policy. Restore from backups in an isolated exercise and prove the old provider, roles, credentials, exceptions, and event sources cannot reactivate. Closure requires no active authority or dependency, not merely a completed migration ticket.
