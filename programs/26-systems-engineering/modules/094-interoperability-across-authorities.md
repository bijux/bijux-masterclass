---
module_id: SYSENG-094
program: Systems Engineering
level: 2
module_number: 94
title: Interoperability Across Authorities
status: complete
last_verified: 2026-08-31
---

# Interoperability Across Authorities

## One-Page Review

### Governing question

How can independently authorized organizations make systems, data, processes, people, and decisions work together for a bounded outcome when no participant may unilaterally define every requirement, meaning, policy, change, or acceptance decision?

### Essential definitions

- **Interoperability** is the evidenced ability of named participants to exchange and use information, services, resources, or effects correctly enough to achieve a specified outcome under stated conditions.
- An **authority** is a person, role, organization, jurisdiction, or mechanism legitimately empowered to decide, approve, veto, fund, operate, enforce, or accept risk for a stated scope.
- **legal and policy interoperability** means the interaction is permitted and its duties, purposes, rights, liabilities, and constraints are mutually workable.
- **organizational interoperability** aligns responsibilities, processes, resources, escalation, service commitments, and decision rights across participants.
- **semantic interoperability** preserves intended meaning across identities, concepts, units, codes, time, provenance, quality, uncertainty, and context.
- **technical interoperability** provides compatible protocols, representations, physical interfaces, security mechanisms, error behavior, capacity, and versions.
- **operational interoperability** enables trained people and systems to execute end-to-end procedures with acceptable timing, workload, availability, degradation, recovery, and support.
- **assurance interoperability** provides mutually acceptable evidence, configuration identity, evaluation methods, residual-risk decisions, and continuing monitoring.
- An **interoperability profile** selects and constrains standards, versions, options, extensions, semantics, policies, and evidence for a use case.
- An **effective agreement** is the complete set of applicable authorities, obligations, precedence, and constraints for one interaction—not merely the existence of a signed document.

### Central model, mechanism, or theorem

For thread $q$, coalition $C$, and time $t$, define the layer vector

\[
I(q,C,t)=\langle L,O,S,T,R,A\rangle,
\]

where $L$ is legal/policy, $O$ organizational, $S$ semantic, $T$ technical, $R$ operational, and $A$ assurance interoperability. A readiness claim is eligible only if every applicable noncompensable layer meets its defined gate:

\[
eligible(q,C,t)\Rightarrow L\land O\land S\land T\land R\land A.
\]

The implication is necessary, not sufficient. Layer discovery, evidence truth, interactions, hazards/threats, actual configuration, human action, and stakeholder outcomes remain outside a Boolean ledger.

### Critical invariants

- Bound every claim by outcome, thread, participants, authority, configuration, environment, time, and evidence.
- Identify who can define, approve, fund, implement, operate, verify, veto, waive, and change each cross-boundary obligation.
- Treat legal, organizational, semantic, technical, operational, and assurance layers as coupled; do not let one passing layer compensate for a prohibited or unsafe one.
- Specify profiles rather than naming standards alone; control versions, options, extensions, mappings, and conformance interpretations.
- Establish authoritative identities, concepts, units, event times, reference data, provenance, quality, corrections, and error semantics.
- Bind exchanged data and actions to purpose, jurisdiction, classification, privacy, retention, onward use, audit, and redress.
- Align end-to-end processes, service windows, capacity, training, incident command, degraded modes, recovery, and support.
- Define precedence and dispute resolution when authorities, policies, requirements, or evidence disagree.
- Verify both provider and consumer behavior plus representative end-to-end outcomes, failures, recovery, and changes.
- Maintain effectivity across participant versions, profiles, agreements, credentials, policies, exceptions, and actual deployments.
- Fund imposed obligations and expose local/global incentives; voluntary adoption is not enforceable interoperability.
- Reassess after material law, policy, authority, membership, meaning, standard, version, threat, incident, dependency, or operating change.

### Common failures

Common failures include declaring interoperability after a ping or successful parse; assuming a common standard has one interpretation; treating advisory guidance as enforceable authority; exchanging data without lawful purpose; aligning schemas but not concepts or time; ignoring human procedures and workload; assigning coordination without funding or escalation; testing only producers; using a central gateway to conceal unresolved semantics; allowing local extensions to become incompatible dialects; treating certification as permanent; accepting averages that hide excluded jurisdictions; failing to propagate correction or revocation; and claiming end-to-end readiness from layer counts.

### Compact example

A synthetic ledger has three critical threads and six required layer checks per thread. Seventeen of eighteen checks pass; legal authority for one eligibility-data thread is missing, so the gate rejects the claim. Adding a declared authority makes the metadata ledger complete but does not prove that the authority is valid, implementations conform, people can operate, risks are acceptable, or outcomes occur.

### Connections

This module builds on SoS characteristics, constituent independence, federated architectures, interfaces, requirements, configuration, risk, security/privacy, V&V, and evolution. It prepares emergent risk, cognitive work, organizations, policy/regulation/ethics, adaptive systems, and whole-system review.

## Governing Question

What must be jointly specified, authorized, implemented, exercised, observed, and governed so that independently controlled participants can produce a dependable end-to-end outcome without inventing a central authority that does not exist?

Interoperability is relational and purpose-bound. System A is not simply “interoperable.” It may interoperate with B for one message profile and normal mode, but not with C for semantic correction, emergency load, privacy purpose, or recovery. Across authorities, correctness includes legitimacy and operational commitment as well as technical compatibility.

## Why This Matters

Cross-border public services, healthcare, emergency response, finance, transport, energy, defense, research, supply networks, and digital identity depend on participants governed by different laws, budgets, policies, missions, suppliers, and release cycles. A technically elegant interface cannot authorize disclosure, allocate staff, reconcile contradictory meanings, compel migration, or accept another organization's residual risk.

The European Commission describes the Interoperable Europe Act as a co-owned cooperation framework that entered into force in April 2024, with a board, mandatory interoperability assessments for relevant cross-border changes, a portal, and support measures. The associated European tradition distinguishes legal, organizational, semantic, and technical layers. This chapter adds explicit operational and assurance layers because executable procedures and mutually acceptable evidence are essential engineering objects. The EU structure is an authoritative public-sector example, not a universal governance prescription.

NASA interface-management guidance requires organizational responsibility, jointly agreed parameters, interface working structures, change processes, rationale, assumptions, anomalies, and updated agreements. Its Interface Requirements Document outline asks for precedence and approval/change authority. Those practices remain valuable across organizations, but a joint working group can only act within delegated powers.

NIST SP 800-47 Revision 1 addresses protection of information exchanged before, during, and after exchange and the agreements needed to manage risk. NIST SP 800-63C-4 makes trust-agreement roles, purposes, attribute release, retention, redress, vetting, and effective terms concrete for identity federation. Identity federation is only one interoperability domain, but it demonstrates why protocol success and legitimate reliance are separate.

GAO-26-107466 reports a current federal data case in which multiple organizations provide coordination and guidance but no designated governance agency establishes and enforces government-wide interoperability requirements; efforts therefore remain fragmented and depend on voluntary adoption. That finding is bounded to the reviewed U.S. federal award and eligibility-data context. It provides direct evidence for distinguishing convening, advising, standardizing, and enforcing authority.

## Prerequisites and Retrieval

Before making or reviewing an interoperability claim, retrieve:

1. the stakeholder outcome, mission thread, scenario, environment, modes, time horizon, criticality, measures, and exact decision to support;
2. participants and affected nonparticipants, including owners, operators, users, funders, regulators, jurisdictions, data controllers, suppliers, auditors, and risk authorities;
3. formal and practical decision rights for requirements, standards, semantics, interfaces, data release, identity, policy, funding, deployment, operations, incidents, evidence, exceptions, and retirement;
4. applicable laws, regulations, policies, contracts, licenses, classifications, privacy purposes, records duties, accessibility, safety/security obligations, liability, and redress;
5. end-to-end business/mission processes: triggers, eligibility, handoffs, decisions, information and physical flows, service windows, human work, outcomes, failure, and recovery;
6. canonical concepts and local models: identities, entities, codes, units, reference data, event/effective/processing time, provenance, uncertainty, quality, corrections, and version mappings;
7. protocols, physical boundaries, schemas, profiles, standards versions, options, extensions, endpoints, credentials, limits, ordering, retries, idempotency, errors, and support;
8. trust and exchange agreements: populations, purposes, attributes/data, assurance, authorized releasers, recipients, retention, onward use, monitoring, incidents, redress, changes, and termination;
9. organizational commitments: owners, resources, service levels, staffing, training, escalation, dispute resolution, decision times, emergency authority, and communications;
10. assurance agreements: conformance methods, reference implementations/data, test environments, evidence formats, configuration/effectivity, reviewers, anomalies, risk acceptance, and expiry;
11. actual versions and state across participants, gateways, mappings, agreements, keys, policies, datasets, waivers, degraded modes, offline members, support, and unknowns;
12. incidents, exercises, consumer/provider conformance, end-to-end tests, load, security/privacy, failure/recovery, operational observations, complaints, exclusions, and stakeholder outcomes.

Run an **authority-and-meaning trace** for one critical data element or command. From origin to effect, ask who may create it, what it means, who may release and receive it, how it is transformed, which policy applies, who acts on it, how errors are corrected, which version/evidence applies, and who resolves disagreement.

## Learning Objectives

After completing this module, you should be able to:

1. define interoperability as a bounded, evidenced relationship rather than a system property;
2. analyze legal/policy, organizational, semantic, technical, operational, and assurance layers;
3. distinguish advisory, standard-setting, funding, approval, enforcement, and risk-acceptance authorities;
4. build a use-case-specific interoperability profile with precedence and change control;
5. align identity, concepts, units, time, provenance, quality, corrections, and error behavior;
6. design agreements for purpose, protection, operations, evidence, redress, and lifecycle;
7. plan provider, consumer, coalition, failure, recovery, and operational validation;
8. manage versions, mappings, gateways, exceptions, migration, and retirement across independent cadences;
9. identify exclusion, incentive, common-cause, and metric risks;
10. issue narrow readiness conclusions with explicit limitations and reassessment triggers.

## Core Exposition

**Begin with an outcome and thread.** “Make agencies interoperable” is not actionable. “Determine benefit eligibility within 24 hours using applicant-authorized income and residency evidence across named agencies” is closer. It identifies a decision, data, time, participants, and affected person. Derive interfaces from the thread, including denial, correction, appeal, delay, outage, and withdrawal.

**Treat interoperability as a relation.** Write $Interop(A,B,q,e,t)$, not $Interop(A)$. Name direction: A can send records B parses does not imply B can return corrections A can apply. Name versions and populations. Multilateral behavior adds policy conflicts, shared-resource contention, loops, and transformations absent from pairwise tests.

**Separate authority functions.** One body may convene; another publishes voluntary standards; a funder sets grant conditions; a regulator mandates behavior; a data controller authorizes release; an operator controls deployment; a technical authority accepts evidence; a court or appeals body resolves rights. A committee title cannot substitute for this map. Verify practical mechanisms: budget, credential, configuration access, contract remedy, statutory power, certification, or operational command.

**Analyze legal and policy interoperability first.** Determine lawful basis or authority, purpose, population, jurisdiction, classification, data minimization, retention, onward use, subject rights, records, accessibility, safety/security, procurement, and liability. Identify conflicts and precedence. Sometimes the correct engineering outcome is no exchange, aggregated data, computation near the source, consent, a legislative change, or a narrower service.

**Align organizational processes.** Map each participant's entry criteria, decisions, handoffs, service calendars, exceptions, evidence, escalation, and closure. A 200-ms API does not satisfy a 24-hour outcome if human review queues for a week. Define operating-level commitments, capacity, funding, training, contacts, incident roles, dispute paths, and authority during emergencies.

**Establish semantic contracts.** Syntax identifies fields; semantics establish identity and meaning. Define entity matching, canonical concepts, code systems, units, scale, precision, uncertainty, null/default, temporal meaning, reference-data versions, provenance, quality, correction, and local mappings. Every lossy mapping states information discarded and decisions for which it is unacceptable.

**Control time explicitly.** Distinguish event, observation, effective, publication, receipt, processing, and decision times. State timezone, calendar, precision, clock uncertainty, freshness, ordering, late data, retroactive changes, and expiry. Authorities may define different effective dates. A technically ordered stream can still apply the wrong law or tariff if effective time is confused with arrival time.

**Create technical profiles.** A standard often contains optional features, versions, extensions, transport choices, error interpretations, and security parameters. Select a profile: protocol and schema versions, mandatory/forbidden options, identifiers, encoding, limits, retries, idempotency, ordering, errors, timeouts, security, privacy, discovery, and deprecation. Publish machine-testable artifacts where useful, but keep prose rationale and authority.

**Design effective agreements.** Enumerate parties and populations; purpose; authorized actions and releases; data/attributes; profiles and assurance; responsibilities; funding; service levels; retention/onward use; audit; incident notification; redress; exception; change; termination; and precedence. If several agreements apply, determine the effective combined terms for the transaction and resolve conflicts before operation.

**Protect information end to end.** Classification and protections follow information before, during, and after exchange. Model source, channel, intermediary, recipient, derived data, logs, backups, analytics, and disposal. Authenticate parties, authorize purpose, minimize disclosure, protect integrity/confidentiality/availability, preserve provenance, audit appropriate actions, and propagate correction or revocation where required.

**Make consumer obligations explicit.** Producers cannot guarantee useful interoperability alone. Consumers validate issuer and version, interpret semantics, enforce purpose, handle errors and duplicates, observe freshness, retain provenance, apply corrections, protect data, and report anomalies. Consumer-driven cases expose ambiguities, but one consumer's expectations do not automatically govern every participant.

**Govern standards and mappings.** Assign authority for profiles, vocabulary, reference data, mappings, conformance, exceptions, and versions. Include affected participants and users without creating veto deadlock. Record rationale and dissent. Voluntary consensus can build legitimacy; high-consequence mandatory behavior needs a legitimate enforcement or admission mechanism plus funding and appeal.

**Coordinate change across cadences.** Define material changes, notice horizons, impact response, compatibility windows, dual support, migration, test evidence, emergency changes, rollback, and retirement. Track actual effectivity. A provider may publish a new version while consumers remain on old profiles, agreements cite earlier definitions, or regulation changes meaning without any schema change.

**Use gateways transparently.** Gateways, brokers, adapters, and translators can bridge authority, protocol, or semantic boundaries. Treat them as governed constituents: document transformation, loss, policy, identity, provenance, capacity, failure, security/privacy, observation, support, and change. They cannot create legal authority or semantic equivalence. Give transitional gateways removal criteria.

**Design conformance as evidence, not ceremony.** Test normative requirements, profiles, schemas, mappings, negative cases, errors, security/privacy, performance, and version combinations. Use authoritative reference data and preserve configurations/results. Certification scope and expiry must be explicit. Self-attestation, independent assessment, bilateral acceptance, and regulatory certification provide different assurance; select by risk and authority.

**Test the end-to-end coalition.** Exercise representative data, users, jurisdictions, modes, load, degraded participants, contradictory inputs, time boundaries, malicious cases, policy denial, correction, appeal, incident, recovery, and re-entry. Verify technical behavior, human work, service times, decision quality, rights, safety/security, and outcomes. Pairwise passes do not necessarily compose.

**Measure inclusion and denominator.** Interoperability can work for modern systems while excluding small municipalities, older devices, disabled users, minority languages, low-connectivity regions, or partners under different law. Report participating and eligible populations, failure/exclusion reasons, distributions, and unknowns. A high transaction success rate over admitted traffic can hide people unable to enter the process.

**Align incentives and funding.** One authority may bear implementation, privacy, support, and incident costs while another receives benefits. Unfunded mandates and voluntary standards predict delay or superficial conformance. Allocate shared funding, assistance, reusable components, transition time, and proportionate evidence. Avoid metrics that reward rejecting complex cases or suppressing error reports.

**Plan dispute and redress.** Technical disagreement, policy conflict, incorrect identity, semantic mismatch, denied service, harmful action, and data misuse need routes to suspend, investigate, correct, compensate where applicable, appeal, and learn. Preserve evidence and identify the authority whose decision is final for each issue. Redress is part of operational interoperability, not external paperwork.

**Maintain an interoperability case.** Link claim, thread, participants, layers, authorities, profile, agreement, configuration, evidence, risks, exceptions, outcomes, and validity period. Update after change or incident. This resembles an assurance case but does not prove all future behavior. It makes the basis and limits of the readiness decision reviewable.

The fixture checks declared layer coverage only.

<!-- bijux-verify: {"id":"cross-authority-interoperability-ledger-fixture","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"critical_threads=3\nrequired_layers_per_thread=6\nrequired_layer_checks=18\ninitial_passing_checks=17\ninitial_missing=benefit_eligibility:legal_policy\ninitial_decision=reject_missing_noncompensable_layer\nafter_correction_passing_checks=18\nafter_correction_missing=0\nafter_correction=eligible_for_declared_layer_gate\nstatus=synthetic_interoperability_ledger_consistent\nevidence=declared_boolean_layer_coverage_only\n","stderr":""}} -->
```python
layers = {"legal_policy", "organizational", "semantic", "technical", "operational", "assurance"}
threads = {
    "emergency_alert": set(layers),
    "benefit_eligibility": set(layers) - {"legal_policy"},
    "capacity_exchange": set(layers),
}
required = len(threads) * len(layers)
passing = sum(len(passed) for passed in threads.values())
missing = sorted(f"{thread}:{layer}" for thread, passed in threads.items() for layer in layers - passed)

print(f"critical_threads={len(threads)}")
print(f"required_layers_per_thread={len(layers)}")
print(f"required_layer_checks={required}")
print(f"initial_passing_checks={passing}")
print(f"initial_missing={','.join(missing)}")
print("initial_decision=reject_missing_noncompensable_layer")
threads["benefit_eligibility"].add("legal_policy")
print(f"after_correction_passing_checks={sum(len(passed) for passed in threads.values())}")
print(f"after_correction_missing={sum(len(layers - passed) for passed in threads.values())}")
print("after_correction=eligible_for_declared_layer_gate")
print("status=synthetic_interoperability_ledger_consistent")
print("evidence=declared_boolean_layer_coverage_only")
```

## Definitions and Notation

Let $A$ be authorities, $C_t$ participating coalition, $Q$ threads, $X$ exchanged information/resources/actions, and $V$ versions/configurations. For thread $q$, layer predicate $I_j(q,C_t,V)$ records whether defined evidence meets the applicable gate for $j\in\{L,O,S,T,R,A\}$.

An interoperability claim is

\[
Claim=\langle outcome,q,C_t,V,environment,thresholds,evidence,exceptions,authority,validity\rangle.
\]

For obligation $o$, $Auth(o)$ is the authority able to accept it and $Mech(o)$ the funding, contract, statute, admission gate, credential, configuration, or operational mechanism that makes it actionable. $Auth(o)\neq\varnothing$ without $Mech(o)$ can still be a practical authority gap.

Semantic mapping $m:D_1\rightarrow D_2$ may be partial or lossy. Record its domain, codomain, version, preconditions, unmapped values, information loss, provenance, and decisions for which it is valid. Never infer equivalence from the existence of $m$.

## Mechanisms, Invariants, or Proof Structure

1. **Frame the outcome.** Name thread, participants, users, environment, modes, thresholds, time, and decision authority.
2. **Map authorities.** Separate legal/policy, organizational, semantic, technical, operational, assurance, funding, exception, and redress powers.
3. **Analyze layers.** Derive obligations and noncompensable gates for legal/policy, organization, semantics, technology, operation, and assurance.
4. **Specify profile and agreement.** Resolve standards, versions, options, meanings, purpose, responsibilities, precedence, evidence, change, and exit.
5. **Implement bidirectionally.** Cover producers, intermediaries, consumers, humans, corrections, errors, monitoring, and support.
6. **Baseline effectivity.** Track actual participants, configurations, agreements, keys, policies, mappings, exceptions, and validity.
7. **Verify and validate.** Test provider, consumer, pair, coalition, negative, load, security/privacy, failure, recovery, redress, and outcomes.
8. **Decide with limitations.** Record evidence, anomalies, residual risks, authority, exclusions, validity, and triggers.
9. **Operate and learn.** Observe service, semantics, policy, decisions, inclusion, incidents, complaints, and stakeholder outcomes.
10. **Govern evolution.** Assess changes, migrate, reverify, revoke invalid evidence, retire debt, and update agreements.

Invariants include: no exchange without purpose and authority; no standard without a profile where optionality matters; no semantic mapping without version and loss; no cross-boundary obligation without an empowered, resourced owner; no certification generalized beyond scope; no readiness claim without consumer and end-to-end evidence; no exception without authority, monitoring, expiry, and exit; and no material change assumed compatible without impact and evidence.

No formal proof establishes interoperability for an open socio-technical coalition. The mechanism structures necessary evidence and governance. Unmodeled conditions, disputed authority, strategic behavior, implementation defects, environmental change, and human adaptation require continuing validation.

## Alternatives and Trade-Offs

**Mandatory standard versus voluntary profile.** Mandates can align participants when legitimate authority, funding, enforcement, and appeal exist. They can freeze poor designs or exceed jurisdiction. Voluntary profiles build consensus and experimentation but may produce partial adoption. Match mechanism to criticality and authority.

**Bilateral agreements versus multilateral framework.** Bilateral terms fit local risks but scale poorly and can conflict. A shared framework reduces duplication and establishes common profiles, yet creates governance, legitimacy, common-cause, and exception challenges. Allow explicit local constraints without uncontrolled dialects.

**Canonical model versus mappings.** A canonical model reduces pairwise translation and supports common analysis. It can become overly broad, politically contested, or semantically shallow. Local mappings preserve domain richness but multiply maintenance and loss. Use bounded canonical concepts plus governed extensions and mappings.

**Central gateway versus direct exchange.** A gateway simplifies protocol, policy, and observation, but becomes a concentration point and may conceal semantic disagreement. Direct exchange preserves autonomy and failure isolation but increases pairwise controls. Hybrid profiles with distributed enforcement often balance the two.

**Pre-certification versus runtime evidence.** Certification provides a reviewable admission gate but ages as configurations change. Runtime conformance detects drift but cannot replace legal approval, validation, or deep failure testing. Bind both to configuration and triggers.

**Broad sharing versus purpose-limited exchange.** Broad data increases reuse and future option value but raises privacy, classification, sovereignty, security, quality, and misuse risk. Purpose-specific products minimize exposure but need new governance for new uses. Prefer minimum sufficient exchange with explicit expansion decisions.

## Failure Modes and Misconceptions

- **“They exchanged a message.”** Connectivity and syntax do not establish meaning, permission, operational use, or outcome.
- **“Both implement the standard.”** Versions, profiles, options, extensions, interpretations, and defects may differ.
- **“The board owns interoperability.”** Determine whether it can mandate, fund, enforce, waive, and resolve disputes.
- **“A data-sharing agreement permits every use.”** Purpose, population, recipient, attributes, retention, and onward use are bounded.
- **“Canonical fields have canonical meaning.”** Identity, units, reference data, time, and local practice can still diverge.
- **“Technical acceptance transfers risk.”** Each competent authority must understand and accept its applicable residual risk.
- **“Provider conformance is enough.”** Consumer interpretation, policy, correction, and operational behavior are equally necessary.
- **“The gateway solves legacy semantics.”** It can only implement explicit transformations and makes loss its own risk.
- **“A signed agreement is effective forever.”** Law, parties, purpose, versions, keys, evidence, and operating conditions change.
- **“An average success rate proves access.”** The denominator may exclude people, regions, systems, languages, or failure modes.
- **“Voluntary adoption will converge.”** Local incentives and budgets may rationally favor delay or divergence.
- **“Emergency overrides are interoperability.”** They need lawful triggers, bounded scope, safeguards, records, and reversion.
- **“More centralized governance eliminates disputes.”** It may lack legitimacy, local knowledge, jurisdiction, or operational control.
- **“Pairwise interoperability composes.”** Multilateral loops, contention, policy conflict, and shared dependencies can defeat it.
- **“Complete layer coverage proves readiness.”** Boolean ledgers cannot establish evidence truth or real outcomes.

## Worked Examples

### Example 1

**Situation:** Two emergency systems successfully exchange an alert. **Reasoning:** Both parse the schema, but one interprets `expires_at` as UTC and the other as local time; one cancels on expiry while the other keeps the alert active. **Conclusion:** Technical syntax passed, temporal semantics and operational behavior failed; define timezone, effective/expiry semantics, clock uncertainty, and cancellation evidence.

### Example 2

**Situation:** A benefits agency requests tax data through a secure API. **Reasoning:** Encryption and authentication succeed, but the tax authority has no legal basis to disclose the requested detail for that eligibility purpose. An authorized yes/no or income-band response may suffice. **Conclusion:** Legal/policy interoperability is noncompensable; redesign the data product or obtain legitimate authority.

### Example 3

**Situation:** A national committee publishes a voluntary address standard. **Reasoning:** It cannot fund migration or require adoption. Agencies retain local formats and only easy records map correctly. Labeling the committee “owner” hides the gap. **Conclusion:** Add legitimate mandate/admission conditions, funding and transition support, or state that interoperability remains voluntary and partial.

### Example 4

**Situation:** Hospitals use the same diagnosis code but different effective editions. **Reasoning:** A code denotes different concepts across release dates, and one local extension is unknown elsewhere. Attach code-system URI/version/effective time, map explicitly, preserve the source, and reject unsafe unknowns. **Conclusion:** Shared code strings do not establish semantic equivalence.

### Example 5

**Situation:** Rail and bus APIs each promise 99.9% availability. **Reasoning:** A journey planner also requires aligned stop identity, schedules, disruption semantics, and a staffed handoff when accessibility assistance changes. Technical uptime can be high while the accessible journey fails. **Conclusion:** Measure the end-to-end operational thread and affected users, not only service endpoints.

### Example 6

**Situation:** A gateway maps `unknown` eligibility to `false` because the target schema is Boolean. **Reasoning:** The mapping discards epistemic state and causes denial rather than review. Add a tri-state target or explicit exception workflow and record mapping loss. **Conclusion:** A technically valid transformation can be semantically and ethically unacceptable.

### Example 7

**Situation:** An identity assertion is valid but a relying organization applies an obsolete role. **Reasoning:** Authentication, audience, and signature pass; attribute freshness and local authorization lifecycle fail. Bound session/attribute age, propagate change/revocation, and re-evaluate sensitive actions. **Conclusion:** Identity interoperability informs but does not guarantee current authorization.

### Example 8

**Situation:** Five organizations pass pairwise tests, then a full exercise overloads a shared reference-data service. **Reasoning:** Every pair used a small fixture; simultaneous cache misses produce common-cause latency and inconsistent fallbacks. **Conclusion:** Coalition scale and shared dependencies require representative load, degradation, and recovery tests.

### Example 9

**Situation:** A regulation changes the legal effective date for reporting while the schema remains unchanged. **Reasoning:** Producers use transaction date; consumers apply receipt date. Both remain syntactically conformant but calculate different obligations. Version the policy/semantic profile and effective-time rule, assess in-flight records, and reverify. **Conclusion:** Interoperability can break without any API change.

### Example 10

**Situation:** A conformance certificate covers version 2.1 in a laboratory. **Reasoning:** Production runs version 2.1 plus a local extension, different policy, a gateway, and larger payloads; the certificate predates a security fix. **Conclusion:** Treat certification as scoped evidence, reconcile actual configuration, test deltas and operations, and set expiry/reassessment triggers.

## Cross-Program Connections

- **Platform Engineering:** shared gateways, policy, identity, catalogs, observability, and deployment controls can enable or dominate cross-authority interoperability.
- **API and Service Engineering:** profiles, schemas, protocol semantics, versioning, idempotency, errors, SLOs, compatibility, and deprecation provide technical mechanisms.
- **Data Engineering:** entity resolution, code systems, units, temporal semantics, lineage, quality, correction, privacy, and data contracts underpin useful exchange.
- **Object-Oriented Programming:** behavioral contracts and substitutability illuminate interface expectations, but separate legal and organizational authorities require negotiated commitments.
- **Functional Programming:** typed transformations expose partiality and loss; real interoperability additionally includes policy, effects, time, authority, and human work.
- **Cybersecurity and Privacy:** trust, least privilege, purpose limitation, classification, exchange agreements, keys, monitoring, incident response, and revocation constrain use.
- **Distributed Systems:** partial failure, clocks, retries, consistency, shared dependencies, and partitions explain many technical interoperability failures.
- **Human Factors:** terminology, procedures, workload, accessibility, handoffs, trust, escalation, and redress determine operational success.
- **Governance and Law:** mandates, voluntary standards, contracts, jurisdiction, liability, appeal, and enforcement determine feasible obligations.
- **Verification and Validation:** conformance, configuration, coalition tests, operational evidence, and stakeholder outcomes bound every acceptance claim.

## References

1. European Commission, [Interoperable Europe Act](https://commission.europa.eu/publications/interoperable-europe-act_en), entered into force 11 April 2024, accessed 2026-08-31.
2. European Union, [Regulation (EU) 2024/903 laying down measures for a high level of public sector interoperability across the Union](https://eur-lex.europa.eu/eli/reg/2024/903/oj), 13 March 2024.
3. NASA, [Interface Management, Systems Engineering Handbook section 6.3](https://www.nasa.gov/reference/6-3-interface-management/), accessed 2026-08-31.
4. NASA, [Appendix L: Interface Requirements Document Outline](https://www.nasa.gov/reference/appendix-l-interface-requirements-document-outline/), accessed 2026-08-31.
5. NASA, [Crosscutting Technical Management, Systems Engineering Handbook section 6.0](https://www.nasa.gov/reference/6-0-crosscutting-technical-management/), accessed 2026-08-31.
6. NIST, [Managing the Security of Information Exchanges, SP 800-47 Revision 1](https://www.nist.gov/publications/managing-security-information-exchanges), July 2021.
7. NIST, [Digital Identity Guidelines: Federation and Assertions, SP 800-63C-4](https://csrc.nist.gov/pubs/sp/800/63/C/4/final), July 2025.
8. NIST, [SP 800-63C-4 Trust Agreement Management and Requirements](https://pages.nist.gov/800-63-4/sp800-63c.html), July 2025.
9. NIST, [Federal Policy on Standards](https://www.nist.gov/standardsgov/federal-policy-standards), updated 1 July 2026.
10. U.S. Government Accountability Office, [Federal Data: Congressional Action Needed to Improve Interoperability of Award and Payment Eligibility Data, GAO-26-107466](https://files.gao.gov/reports/GAO-26-107466/index.html), June 2026.

## Exercises

### Exercise 1

Build a six-layer interoperability analysis for a cross-jurisdiction emergency shelter-capacity exchange.

### Exercise 2

Three threads each require six layer gates. Thread A passes six, B passes five, and C passes four. Compute raw coverage, then explain why neither the total nor a weighted average establishes readiness.

### Exercise 3

Diagnose a data exchange where schemas and transport conform but decisions diverge because participants use different identities, reference-data versions, and effective-time rules.

### Exercise 4

Design governance, profiles, evidence, migration, and redress for an interoperability program whose central office can convene and fund but cannot mandate participant adoption.

### Exercise 5

Transfer the framework to cross-border recognition of professional credentials involving issuers, regulators, employers, digital wallets, identity providers, and applicants.

## Answers to the Exercises

### Answer 1

Frame the thread: an authorized coordinator locates safe, accessible shelter capacity for a displaced person within a stated region and time. **Legal/policy:** establish authority and purpose for location, household, health/accessibility, immigration-sensitive, and safeguarding data; minimize fields; define jurisdictions, retention, onward use, rights, and emergency powers. **Organizational:** name shelter owners, municipalities, coordinator, data stewards, staffing, update frequency, reservation authority, escalation, incident roles, funding, and service windows.

**Semantic:** define shelter/site identity, bed versus room, household grouping, accessibility features, age/sex/family constraints, pets, medical support, available/reserved/occupied/out-of-service, event/effective time, capacity uncertainty, provenance, and corrections. **Technical:** profile API/events, schema/version, identifiers, authentication, authorization, limits, idempotency, ordering, errors, encryption, and deprecation. **Operational:** train staff, reconcile phone/manual updates, handle no connectivity, stale capacity, reservation races, transport, denial, fallback, and recovery. **Assurance:** conformance fixtures, representative exercises, security/privacy review, load and partition tests, configuration/effectivity, anomalies, risk acceptance, and operational monitoring.

The readiness claim names participating shelters/jurisdictions, versions, update threshold, scenarios, evidence date, exclusions, and authority. Include people who cannot use digital channels and audit whether admitted-transaction metrics hide excluded populations.

### Answer 2

There are $3\times6=18$ required layer checks. Passing checks are $6+5+4=15$, so raw coverage is $15/18=5/6\approx83.33\%$. This arithmetic only counts declared gates. It does not identify which three fail.

A missing legal authority can prohibit the interaction; missing semantic identity can produce wrong decisions; missing operational recovery can make a safety-critical thread unusable. These are not generally compensable by stronger technical performance elsewhere. A weighted average imports subjective weights and can still hide a veto constraint. Thread C could also be the only life-safety thread, while Thread A is optional.

List failures by thread/layer, consequence, owner, evidence, and authority. Resolve each, redesign or narrow the thread, or accept an exception only where legitimate and noncompensable constraints permit. Challenge layer completeness and evidence quality. Readiness is considered per bounded thread after all applicable veto gates and integrated evidence hold; 83.33% is ledger coverage, not readiness probability or risk.

### Answer 3

Trace one divergent decision. Identity may use local person or organization identifiers with collisions, merges, reused numbers, or different matching rules. Establish authoritative namespaces, issuer, lifecycle, crosswalk confidence, duplicate/merge/split handling, and manual resolution. Preserve source identifiers and provenance.

Reference data may use different code-system editions or local extensions. Attach system URI, version/effective date, map explicitly, record unmapped values and loss, and reject unsafe unknowns. Time may mean occurrence, observation, effective, filing, receipt, processing, or decision. Define each timestamp, timezone/calendar, precision, uncertainty, retroactivity, freshness, ordering, and the policy version selected by effective time.

Create shared fixtures for collisions, renamed entities, old/new codes, local extensions, daylight-saving boundaries, late/corrected events, retroactive policy, duplicates, and conflicting sources. Test producers, transformations, consumers, decisions, correction, and audit. Bind evidence to actual versions. Passing transport/schema remains valid narrow evidence; semantic and decision interoperability require the additional contract and end-to-end results.

### Answer 4

State the authority honestly: the office convenes parties and conditions its own funding, but cannot command all releases or participation. Charter a forum with participant/data/policy/technical/operational/risk/user representation, scope, decisions, quorum, conflict, records, response times, and escalation. Use grants, cost sharing, reusable tools, reference services, technical assistance, admission to funded services, published evidence, and reciprocal benefits to encourage adoption. Do not describe voluntary guidance as mandatory.

Prioritize bounded threads. For each, publish a versioned profile covering standards options, semantics, identity/time/reference data, policy/purpose, service processes, security/privacy, evidence, and errors. Establish bilateral or multilateral agreements accepted by competent parties. Fund implementation and transition. Provide reference data, conformance suites, test environments, implementation guidance, and an exception process.

Track declared and observed participants/configurations. Require change notice where agreements permit, offer compatibility windows and migration evidence, and retire old profiles with support and exit dates. Measure adoption denominator, excluded populations, semantic/operational outcomes, incidents, and burden—not downloads. Redress handles incorrect decisions and data misuse. If a critical participant declines, narrow the coalition/outcome, negotiate stronger authority, or report the gap; a green central dashboard cannot create adoption.

### Answer 5

Frame a credential claim such as “this named applicant holds credential X, issued by authority Y, currently valid for practice scope Z in jurisdiction J,” not a universal equivalence. **Legal/policy:** determine issuing and recognizing authority, regulated scope, privacy purpose, applicant rights, fraud handling, retention, appeal, and cross-border rules. **Organizational:** assign issuer, regulator, employer, wallet/identity provider, verification service, support, incident, correction, and redress roles.

**Semantic:** define person identity, issuer, credential type/level, learning or practice outcomes, specialties, restrictions, issue/effective/expiry/revocation, status, jurisdiction, evidence, and mappings. Avoid mapping two credentials as equivalent merely because labels match. **Technical:** profile signed credentials/assertions, issuer discovery, keys, audience/challenge, presentation, status/revocation, selective disclosure where suitable, errors, versions, and offline bounds. **Operational:** cover applicant consent/presentation, employer review, exceptions, name changes, inaccessible technology, manual verification, suspected fraud, outage, and correction. **Assurance:** vet issuers and wallets as applicable, test verifier behavior, key/status freshness, privacy/security, representative cases, and actual decisions.

The recognizing regulator retains authorization; a cryptographically valid credential proves neither current status nor legal permission to practice. Minimize attributes and give applicants understandable terms and appeal. Bind conclusions to jurisdictions, credential/profile versions, assurance, status time, and evidence. Reassess issuer compromise, key rotation, revocation, regulatory change, wallet migration, and semantic mapping changes.
