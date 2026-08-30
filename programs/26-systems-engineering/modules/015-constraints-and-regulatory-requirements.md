---
module_id: SYSENG-015
program: Systems Engineering
level: 1
module_number: 15
title: Constraints and Regulatory Requirements
status: complete
last_verified: 2026-08-31
---

# Constraints and Regulatory Requirements

## One-Page Review

### Governing question

How can a systems team identify, interpret, transform, reconcile, verify, and maintain genuine constraints and regulatory obligations without mistaking preferences, guidance, inherited design, or decontextualized clauses for authoritative system requirements?

### Essential definitions

- A **constraint** restricts the permitted solution, operation, process, resource, interface, environment, or lifecycle choice rather than directly stating a desired stakeholder outcome.
- A **regulatory requirement** is a binding obligation derived from an applicable law or regulation under a defined jurisdiction, scope, role, classification, date, and authority.
- **Applicability** is the justified determination that a source provision governs a particular entity, product, activity, place, population, transaction, or lifecycle stage.
- A **normative source** establishes obligations under its authority; **guidance** explains or recommends practice but is not automatically binding.
- A **standard** is a governed technical or process document; it becomes mandatory only through law, contract, policy, certification scheme, or another authorized adoption mechanism.
- **Incorporation by reference** makes external material part of an obligation under the incorporating authority and specified edition/scope.
- A **prescriptive constraint** specifies a required means or prohibited choice; a **performance-based obligation** specifies an outcome or property while preserving realization alternatives.
- A **compliance obligation** may apply to the organization, process, personnel, records, evidence, supplier, or product; not every obligation should be assigned to the system of interest.
- A **deviation, waiver, exemption, or alternative means** is valid only under its governing process and authority; engineering convenience cannot create one.
- A **compliance baseline** is a versioned, reviewed mapping from authoritative sources through applicability and interpretation to controlled obligations and evidence.

### Central model, mechanism, or theorem

Represent an external obligation as:

\[
o=\langle id,authority,jurisdiction,source,provision,edition,effectiveDate,
applicability,subject,modality,condition,obligation,exceptions,
interpretation,rationale,derivedRequirements,evidence,owner,status\rangle.
\]

Translation must preserve an auditable chain:

\[
AuthoritativeProvision
\xrightarrow{applicability+interpretation}
ControlledObligation
\xrightarrow{allocation+rationale}
System/Process/EvidenceRequirements.
\]

For each derived requirement \(r\):

\[
ValidTrace(r)\Rightarrow Applicable(source(r))\land
AuthorizedInterpretation(r)\land ScopePreserved(r).
\]

The implication is a review obligation, not legal proof. Engineering review cannot replace competent legal, regulatory, certification, or domain authority.

### Critical invariants

- Use the current authoritative text, jurisdiction, edition, amendment state, effective date, and official language where relevant.
- Establish applicability before deriving a requirement and record the role/classification facts on which applicability depends.
- Preserve source wording and citations separately from interpretation and engineered requirement text.
- Allocate obligations to the correct subject: system, organization, operator, supplier, process, record, evidence, or authority.
- Distinguish binding law/regulation/contract/policy from standards, guidance, industry practice, and preference.
- Preserve conditions, exceptions, definitions, cross-references, thresholds, record horizons, and procedural rights.
- Do not turn a performance-based obligation into a prescriptive design without necessity and authority.
- Conflicts, precedence, deviations, alternative means, and residual uncertainty are explicit and decided by named authority.
- Bidirectional traceability reaches source provision, interpretation, implementation/evidence, change impact, and retirement.
- Compliance evidence never automatically proves safety, security, ethics, effectiveness, accessibility, or stakeholder acceptance.

### Common failures

Failures include citing a blog instead of controlling text; using a regulation title without clause; applying one jurisdiction globally; ignoring definitions or exemptions; treating guidance as law; treating a voluntary standard as optional after contractual incorporation; copying organization duties into product `shall` statements; using “industry standard” without edition; assuming a preferred vendor is mandated; overlooking transition and record obligations; claiming compliance from a checklist; freezing applicability after law, product classification, market, supplier, or use changes; and letting engineers make unreviewed legal conclusions.

### Compact example

A team says, “Privacy law requires all customer data to remain in-country.” The statement may be false or incomplete. Identify jurisdictions, organization roles, data categories, people, processing purposes, transfers, recipients, safeguards, contracts, exceptions, retention, and effective dates. Obtain authorized interpretation of controlling provisions. The actual requirements may concern lawful basis, purpose limitation, access, records, transfer mechanisms, deletion, response rights, and evidence—not one universal storage architecture. Data residency remains a candidate constraint only where a source and applicability analysis justify it.

### Connections

Retrieve assumptions and constraints from SYSENG-008, operational context from SYSENG-009/012, stakeholder needs from SYSENG-011, and functional/performance requirements from SYSENG-013–014. Continue to requirement quality/testability, decomposition, allocation, traceability, and change. Later safety, security, verification, lifecycle, policy, ethics, and systems-of-systems modules deepen assurance and multi-authority governance.

## Governing Question

Engineers work inside a solution space bounded by physics, interfaces, resources, law, policy, contracts, standards, organizational capability, and prior decisions. Some bounds are immutable for a decision; others are provisional, negotiable, misinterpreted, expired, or merely preferred. Treating all of them alike either creates unnecessary design rigidity or leaves real obligations unfulfilled.

The governing question is therefore one of authority-preserving transformation. The team must determine what governs, why it applies, to whom, when, under which conditions and exceptions, what evidence is required, and how it constrains the SoI. That work must remain inspectable when sources, classifications, markets, or designs change.

## Why This Matters

A system can meet stakeholder and functional requirements yet be unlawful to place on a market, impossible to certify, incompatible with an external infrastructure, or unsafe to operate. Conversely, a team can spend years satisfying constraints that no controlling source imposed. Both errors arise when provenance and applicability are replaced by folklore.

ISO/IEC/IEEE 29148:2018 treats constraints, assumptions, required characteristics, and traceability as requirements-engineering information. ISO/IEC/IEEE 15288:2023 places applicable agreements, organizational policies, law, regulation, standards, technology, and lifecycle concepts among influences on system definition. NASA accepts baselined stakeholder constraints as inputs but emphasizes iterative interpretation and complete requirements rather than blind transcription.

Regulation is temporally and jurisdictionally unstable. For example, Regulation (EU) 2024/1689 is an official, directly citable legal text with defined scope, roles, classifications, obligations, amendments, and phased applicability; a summary cannot establish which provisions govern a particular system on a particular date. This module teaches the engineering control mechanism, not legal advice. Competent authority must decide legal meaning and compliance acceptance.

## Prerequisites and Retrieval

Before continuing, retrieve:

1. a constraint restricts choices and needs provenance, scope, owner, validity, and consequence;
2. perceived constraints from stakeholders can be wrong and remain hypotheses until verified;
3. system boundaries and operational roles determine which entity can satisfy an obligation;
4. functions and qualities should remain solution-responsible but avoid unjustified design selection;
5. assumptions require evidence and triggers; they do not become facts through baselining;
6. traceability includes transformation rationale, not only source and target identifiers;
7. verification evidence is bounded, while validation and acceptance depend on stakeholder and authority judgment.

As a retrieval test, assess “We must use the existing identity provider.” Possible sources include a signed interface agreement, organizational policy, acquisition decision, migration constraint, or an architect's preference. Record the exact source, scope, authority, expiration, exception process, operational consequence, and underlying identity outcome. Until then, it is an alleged constraint, not a requirement.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish physical, technical, interface, resource, design, process, contractual, policy, standards, and regulatory constraints;
2. classify authoritative sources, guidance, adopted standards, interpretations, and preferences;
3. construct an applicability analysis using jurisdiction, role, product/activity classification, scope, and date;
4. transform provisions into correctly allocated system, process, organizational, supplier, and evidence requirements;
5. preserve definitions, conditions, exceptions, cross-references, modality, and source language;
6. compare prescriptive and performance-based constraints and avoid design overreach;
7. govern conflicts, precedence, equivalence, waiver, deviation, and alternative means;
8. build provision-to-evidence traceability and change surveillance;
9. review compliance evidence without overclaiming safety, security, ethics, or effectiveness;
10. identify decisions that require legal, regulatory, certification, contracting, safety, or other competent authority.

## Core Exposition

**Inventory constraint classes.** Physical laws bound energy, geometry, material, and timing. External interfaces constrain semantics and form. Resources constrain mass, power, compute, staffing, cost, and schedule. Lifecycle concepts constrain production, operation, support, transition, and disposal. Agreements, contracts, policies, standards, laws, and regulations introduce obligations with different authorities. Design decisions create lower-level constraints only after authorization.

**Record provenance before interpretation.** Capture issuer, jurisdiction, instrument type, exact title/identifier, provision, definitions, annexes, edition/version, publication and effective dates, amendments/corrigenda, official language, source URL/repository, and retrieval date. Preserve a controlled copy or immutable reference where licensing and governance permit. Secondary summaries support discovery, not controlling interpretation.

**Classify source authority.** A statute, regulation, permit condition, regulator decision, court order, contract, internal policy, consensus standard, certification rule, and guidance document have different force. A standard may be voluntary generally but binding for a project because a regulation, contract, procurement term, or policy incorporates a named edition. Record the adoption path.

**Determine applicability systematically.** Identify legal/organizational entity, role (provider, deployer, operator, importer, manufacturer, controller, processor, employer, supplier), product/service/activity classification, intended purpose, foreseeable use, affected people, geography, market, data/material, scale, risk/integrity class, lifecycle stage, and date. Each conclusion cites facts, source provisions, interpreter, uncertainty, and authority.

**Separate facts from conclusions.** “The product processes biometric data for employee access in jurisdiction J” is an applicability fact. “Provision P applies to the operator as role R from date D” is an interpretation. “The access system shall record authorization provenance” is an engineered obligation. Keeping layers separate lets a changed fact invalidate the right conclusions without rewriting history.

**Read definitions and structure.** Legal and normative terms can differ from everyday meanings. Scope clauses, definitions, recitals/purpose, operative provisions, annexes, referenced standards, transition provisions, exemptions, enforcement, and amendment history interact. Never extract one sentence while discarding its defined subject, condition, exception, or cross-reference.

**Preserve modality.** `Shall`, `must`, `may`, prohibition, permission, recommendation, presumption, and conditional duty have distinct effects within their source conventions. Do not strengthen guidance into a mandatory product obligation or weaken a prohibition into a goal. Preserve original text separately so translation can be audited.

**Allocate to the correct entity.** A regulation may require an organization to maintain a management system, appoint a role, assess risk, notify an authority, provide information, preserve records, enable human oversight, or monitor operation. The product may supply capabilities and evidence, but cannot itself satisfy governance, competence, or legal-accountability duties. Build an obligation-allocation table across organization, SoI, operators, suppliers, processes, records, and external authorities.

**Translate with rationale.** For each applicable provision, state interpreted obligation, subject, trigger/condition, prohibited/permitted action, output/evidence, deadline/horizon, exceptions, and acceptance authority. Then derive atomic requirements at the appropriate level. Maintain many-to-many links: one provision may yield several requirements, and one requirement may satisfy several compatible provisions.

**Separate constraint from function and quality.** “Use protocol X version Y” is a design/interface constraint if authorized. “Exchange authenticated status with authority A” is function. “Retain records for H years” combines information behavior and temporal constraint. Types can overlap; explicit classification helps review and change but never replaces semantics.

**Keep program limits out of product semantics.** Cost and schedule can constrain the feasible program and force scope or architecture decisions, but “the system shall cost less than X” is not automatically a technical product requirement with an engineering verification method. Identify whether the bound concerns acquisition price, development expenditure, unit recurring cost, total ownership cost, staffing, delivery date, certification date, or operational budget; state currency, base year, quantities, inclusions, uncertainty, and governing authority. Then trace authorized scope and design decisions. Do not weaken safety, regulatory, or stakeholder obligations silently to fit a budget: expose the conflict and obtain the authority that owns the affected baseline.

**Challenge prescriptive claims.** Ask whether the source actually mandates a means or only an outcome. Performance-based regulation may allow alternative architectures that demonstrate equivalent outcomes. Prescriptive provisions may still contain scoped options or recognized alternative means. Never invent equivalence; follow the governing approval process.

**Handle standards precisely.** Record standard identifier, edition, amendments, clause, conformance target, profile, optional features, normative references, and adoption mechanism. “Comply with ISO standards” is uncontrolled. Check whether a newer edition automatically applies; dated incorporation often fixes an older edition until formally updated.

**Distinguish compliance, certification, and assurance.** Compliance is conformity to applicable obligations. Certification or conformity assessment is a decision under a scheme by an authorized party. Assurance is justified confidence based on evidence. Self-declaration, accredited assessment, regulator approval, and customer acceptance are not interchangeable. State who decides and what evidence they accept.

**Map evidence early.** Evidence can include requirements/design trace, analysis, test, inspection, process records, risk files, supplier declarations, competence/training, configuration history, audit logs, incident records, monitoring, technical documentation, labels/instructions, and post-market action. Evidence itself has authenticity, completeness, retention, access, privacy, and configuration requirements.

**Govern suppliers and inheritance.** A supplier certificate or contract may support a claim within product, version, configuration, use, and time boundaries. It does not transfer all accountability or prove integration compliance. Trace flowed-down obligations, evidence rights, change notification, vulnerability/incident duties, audit/access, substitutes, obsolescence, and termination.

**Resolve conflicts and precedence.** Two obligations can conflict across jurisdictions, contracts, safety, privacy, security, accessibility, records, or technical interfaces. Record the exact conflict and applicable entities rather than averaging it away. Apply governing precedence and seek competent interpretation. Architecture alternatives, market segmentation, restricted operation, or withdrawal may be necessary.

**Manage deviations and alternatives.** A waiver, exemption, deviation, variance, or alternative means needs its formal authority, scope, conditions, duration, evidence, residual risk, notification, and renewal/closure. Internal risk acceptance cannot waive external law. Track temporary decisions so they do not silently become permanent architecture.

**Integrate safety, security, and ethics.** Regulatory compliance may define a floor or one evidence framework. Hazards, adversaries, vulnerable populations, and emerging use can demand additional requirements. NIST SP 800-160 Rev. 1 integrates security requirements and security-driven constraints with broader system requirements and explicitly calls for rationale and stakeholder review. Passing a checklist does not establish trustworthy behavior.

**Maintain temporal validity.** Monitor changes to law, regulation, guidance, standards, permits, contracts, product classification, intended use, markets, suppliers, interfaces, and organizational roles. Record effective and transition dates. Trigger impact analysis across needs, requirements, architecture, evidence, operations, support, deployed configurations, communications, and retirement.

**Review the applicability argument, not only its answer.** A defensible record identifies facts relied upon, contrary facts, definitions applied, sources consulted, interpretive uncertainty, excluded provisions, reviewer competence, and approval. Sample boundary cases—changed intended purpose, a new customer role, remote access from another jurisdiction, a supplier becoming an importer, a model update, or a formerly internal tool offered externally. Ask what fact would reverse the conclusion and ensure operations can detect that trigger. A binary applicable/inapplicable field without this argument is fragile and can conceal motivated interpretation.

**Use tools as indexes, not legal reasoning.** A database can find missing authority, date, applicability, owner, or evidence fields and can notify source changes. It cannot determine legal meaning, jurisdictional conflict, equivalence, or adequate evidence. The executable check below is deliberately bounded to declared records and phrases.

<!-- bijux-verify: {"id":"constraint-obligation-record-check","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"obligations_total=5\nwell_formed_declared=1\nmissing_authority=CO-004\nmissing_applicability=CO-002\nmissing_effective_date=CO-003\nmissing_evidence=CO-005\npreference_signals=CO-004:preferred vendor\nobligation_set_ready=false\nevidence=declared_fields_and_lexical_signals_only\n","stderr":""}} -->
```python
obligations = [
    {"id": "CO-001", "authority": "regulator", "source": "Provision-12", "applicability": "provider in market J",
     "effective_date": "2027-01-01", "subject": "provider", "obligation": "retain conformity records",
     "evidence": ["controlled record index"]},
    {"id": "CO-002", "authority": "contract owner", "source": "Contract-7", "applicability": "",
     "effective_date": "2026-10-01", "subject": "supplier", "obligation": "notify material interface change",
     "evidence": ["notification record"]},
    {"id": "CO-003", "authority": "safety authority", "source": "Safety-4", "applicability": "hazardous operating mode",
     "effective_date": "", "subject": "system", "obligation": "prevent unsafe energization",
     "evidence": ["hazard verification"]},
    {"id": "CO-004", "authority": "", "source": "architecture note", "applicability": "all deployments",
     "effective_date": "2026-08-30", "subject": "system", "obligation": "use preferred vendor",
     "evidence": ["design review"]},
    {"id": "CO-005", "authority": "records authority", "source": "Policy-9", "applicability": "regulated records",
     "effective_date": "2026-12-01", "subject": "organization", "obligation": "preserve record provenance",
     "evidence": []},
]

required = ("authority", "source", "applicability", "effective_date", "subject", "obligation", "evidence")
preferences = ("preferred vendor", "industry standard", "best practice")
complete = [o for o in obligations if all(o[k] for k in required) and not any(p in o["obligation"] for p in preferences)]

print(f"obligations_total={len(obligations)}")
print(f"well_formed_declared={len(complete)}")
print("missing_authority=" + ",".join(sorted(o["id"] for o in obligations if not o["authority"])))
print("missing_applicability=" + ",".join(sorted(o["id"] for o in obligations if not o["applicability"])))
print("missing_effective_date=" + ",".join(sorted(o["id"] for o in obligations if not o["effective_date"])))
print("missing_evidence=" + ",".join(sorted(o["id"] for o in obligations if not o["evidence"])))
hits = sorted(f'{o["id"]}:{p}' for o in obligations for p in preferences if p in o["obligation"])
print("preference_signals=" + ",".join(hits))
print(f"obligation_set_ready={str(len(complete) == len(obligations)).lower()}")
print("evidence=declared_fields_and_lexical_signals_only")
```

## Definitions and Notation

Let \(S\) be authoritative sources, \(F\) applicability facts, \(I\) authorized interpretations, \(O\) controlled obligations, \(R\) engineered requirements, and \(E\) compliance evidence.

Define the trace relations:

\[
Applicable:S\times F\rightarrow\{true,false,undetermined\},
\]

\[
Interpret:(s,f)\mapsto i,\quad Allocate:i\mapsto O,\quad Derive:O\mapsto R,
\quad Demonstrate:(R,E)\mapsto Finding.
\]

`Undetermined` is a legitimate controlled state with owner and resolution plan. A **finding** records what evidence shows under a scheme and scope; it is not universal compliance.

A **hard constraint** is fixed within the decision scope; a **soft constraint** is a trade preference or negotiable limit. Because these labels depend on authority and horizon, record why. An **assumption** is accepted as true for planning pending validation; a **constraint** restricts choice. A **regulatory requirement** arises only after applicability and interpretation, not merely because a regulation exists.

## Mechanisms, Invariants, or Proof Structure

The transformation mechanism has eight passes: discover sources; control versions; establish applicability facts; obtain authorized interpretation; allocate obligations; derive requirements and evidence; reconcile conflicts; monitor changes. Each pass leaves provenance and unresolved items.

Use a readiness predicate:

\[
Ready(o)=Authority(o)\land CurrentSource(o)\land Applicability(o)
\land ScopePreserved(o)\land CorrectSubject(o)\land EvidencePath(o)
\land AuthorizedReview(o).
\]

This is a governance predicate, not legal proof. `CorrectSubject`, `Applicability`, and `AuthorizedReview` require competent judgment.

Maintain five invariants. **Authority invariant:** obligation force traces to a governing source/adoption path. **Applicability invariant:** scope facts and interpretations remain attached. **Fidelity invariant:** modality, definitions, conditions, and exceptions survive translation. **Allocation invariant:** system capabilities do not substitute for organizational duties. **Temporal invariant:** every conclusion is versioned and change-triggered.

Coverage matrices should operate both ways. Every applicable provision is satisfied, explicitly inapplicable with rationale, or unresolved; every compliance-tagged requirement traces upward. Empty rows expose gaps, but the matrix cannot reveal an undiscovered source or wrong legal interpretation.

## Alternatives and Trade-Offs

**Prescriptive versus performance-based obligations.** Prescription simplifies inspection but can freeze technology. Performance-based obligations preserve innovation but demand stronger outcome evidence. Follow source semantics; do not choose merely for engineering convenience.

**Global baseline versus jurisdiction profiles.** One strict global baseline reduces variants but may impose unnecessary cost or still miss incompatible duties. Profiles improve legal fit but increase configuration and evidence complexity. Maintain shared core plus explicit deltas when feasible.

**Manual analysis versus rules engine.** Expert analysis handles ambiguity and authority; automation supports scale, field completeness, dates, and change notification. Encoding an interpretation does not make it correct, so version rules and retain human approval.

**Direct compliance versus alternative means.** Direct prescribed means may ease acceptance. Alternative means can improve outcomes or feasibility but require comparative evidence and formal authorization. Keep the fallback and approval risk explicit.

**Product capability versus organizational control.** Product automation can make duties repeatable and evidenced, but it can also obscure accountable decisions. Allocate each duty by authority, competence, and controllability, then specify enabling product behavior.

**Early constraint versus deferred commitment.** Early genuine constraints prevent infeasible designs. Early alleged constraints destroy option value. Verify source and applicability early while deferring realization choices not yet necessary.

## Failure Modes and Misconceptions

1. **“The regulation applies to the technology.”** Applicability usually depends on entity, role, purpose, activity, geography, classification, and date.
2. **“A standard is either mandatory or voluntary.”** Its force depends on incorporation, contract, policy, or scheme and named edition.
3. **“Legal text can be copied into a system requirement.”** Many duties belong to organizations, people, processes, records, or authorities.
4. **“Compliance equals certification.”** Assessment decisions, assessors, schemes, scope, and evidence differ.
5. **“Certification proves safety or security.”** It supports bounded conformity claims, not every operational outcome or threat.
6. **“The strictest rule everywhere is safest.”** Rules can conflict, and excess collection/retention/control can create harm.
7. **“A vendor certificate transfers responsibility.”** Integration, use, configuration, and ongoing obligations remain.
8. **“Guidance is merely optional.”** It may express accepted interpretation or evidence expectations even when not binding text; classify carefully.
9. **“A waiver is a design note.”** Only the governing authority can grant it under defined scope and conditions.
10. **“The baseline remains valid.”** Sources, facts, roles, intended use, and product configuration change.

## Worked Examples

### Example 1

**Situation.** A privacy requirement says all data must remain in one country. **Reasoning.** Identify controller/processor roles, people, categories, purposes, transfers, recipient locations, safeguards, contracts, exceptions, and controlling provisions. Authorized interpretation may produce lawful-processing, access, transfer, deletion, record, and response obligations rather than local storage. **Conclusion.** Residency is not inferred from a privacy slogan; trace the actual applicable duties.

### Example 2

**Situation.** A contract says “comply with ISO standards.” **Reasoning.** The phrase lacks identifier, edition, clause, product/process scope, conformance target, precedence, and acceptance scheme. Raise a contractual clarification instead of guessing every ISO publication. **Conclusion.** Standards constraints require exact adoption metadata.

### Example 3

**Situation.** A medical-device organization must maintain complaint and corrective-action processes. **Reasoning.** The device can collect diagnostic evidence and support traceability, but governance, investigation, reporting, competence, and disposition belong to organizational processes and named roles. Requirements allocate product, QMS, records, and authority separately. **Conclusion.** Do not assign an organization duty to software because software can assist it.

### Example 4

**Situation.** An accessibility rule is treated as a visual contrast checker. **Reasoning.** Determine the adopted standard/version and applicable content/functions. Derive semantic, keyboard, focus, name/role/value, error, timing, media, and compatibility obligations as applicable, plus process and representative evaluation. Automated checking supplies partial evidence. **Conclusion.** One detectable rule cannot stand for accessibility conformity or usable access.

### Example 5

**Situation.** A safety authority requires prevention of energization with an open guard. **Reasoning.** This prescriptive/prohibitive constraint affects state sensing, command, fault behavior, independence, diagnostic evidence, maintenance, override authority, and verification. Preserve exact scope and permitted service modes. **Conclusion.** Genuine safety constraints can deliberately restrict architecture and need end-to-end evidence.

### Example 6

**Situation.** Two jurisdictions require incompatible record deletion and preservation. **Reasoning.** Map data/record category, legal entity, geography, purpose, hold, requester, retention horizon, exceptions, and precedence. Seek legal authority; explore segregated stores, holds, minimization, jurisdiction profiles, or service limitation. **Conclusion.** Engineering cannot average conflicting duties; explicit authority and architecture strategy are required.

### Example 7

**Situation.** A supplier provides a certificate for a cryptographic module. **Reasoning.** Check scheme, version, configuration, operational environment, algorithms, key lifecycle, dependencies, expiration, vulnerabilities, and integration assumptions. Trace remaining system requirements and supplier change notification. **Conclusion.** Component certification is bounded inherited evidence, not system compliance or security proof.

### Example 8

**Situation.** A team calls its preferred cloud provider a regulatory mandate. **Reasoning.** Inspect the alleged provision. If it requires controls, audit access, location, continuity, or incident notification but names no provider, derive those obligations and compare suppliers. Preserve provider selection as a decision record. **Conclusion.** Do not disguise procurement preference as law.

### Example 9

**Situation.** An AI service may fall under Regulation (EU) 2024/1689. **Reasoning.** Determine provider/deployer/importer roles, intended purpose, system and use classification, geography, exclusions, dates, and changed-use triggers from official text with competent counsel. Map applicable organizational, technical, documentation, monitoring, and evidence duties; do not assume every AI provision applies immediately. **Conclusion.** Regulation title alone cannot establish applicability or a complete requirement set.

### Example 10

**Situation.** Emergency authorization temporarily permits an alternative operating mode. **Reasoning.** Record granting authority, legal basis, system/configuration, geography, start/end, conditions, monitoring, communication, residual risk, records, renewal, revocation, and restoration baseline. Prevent the exception from leaking into ordinary mode. **Conclusion.** Temporary relief is a controlled lifecycle state, not permanent permission.

## Cross-Program Connections

- [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md) records how genuine constraints shape architecture decisions, profiles, and evidence.
- [Data Engineering](../../19-data-engineering/ROADMAP.md) implements provenance, minimization, residency/transfer, retention, deletion, quality, and evidentiary lineage where applicable.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) integrates protection requirements, assurance, threat/risk, policy, and security-driven constraints.
- [API & Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) translates regulatory and contractual boundary duties into service contracts, auditability, and compatibility controls.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md) offers reusable policy/evidence capabilities while preserving application-owner accountability.
- [Cloud & Infrastructure Engineering](../../30-cloud-and-infrastructure-engineering/ROADMAP.md) manages jurisdiction, supplier, region, resilience, configuration, and shared-responsibility constraints.

## References

1. ISO/IEC/IEEE. [ISO/IEC/IEEE 29148:2018 — Requirements engineering](https://www.iso.org/standard/72089.html), second edition, 2018. Consulted 2026-08-31.
2. ISO/IEC/IEEE. [ISO/IEC/IEEE 15288:2023 — System life cycle processes](https://www.iso.org/standard/81702.html), second edition, 2023. Consulted 2026-08-31.
3. NASA. [Technical Requirements Definition](https://www.nasa.gov/reference/4-2-technical-requirements-definition/), *NASA Systems Engineering Handbook*, Rev. 2. Consulted 2026-08-31.
4. NASA. [Systems Engineering Handbook Appendix](https://www.nasa.gov/reference/system-engineering-handbook-appendix/), requirement and technical-planning guidance. Consulted 2026-08-31.
5. SEBoK Editorial Board. [System Requirements Definition](https://sebokwiki.org/wiki/System_Requirements_Definition), *Guide to the Systems Engineering Body of Knowledge*, version 2.14. Consulted 2026-08-31.
6. NIST. [SP 800-160 Volume 1 Revision 1 — Engineering Trustworthy Secure Systems](https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final), November 2022. Consulted 2026-08-31.
7. European Union. [Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj?locale=en), Official Journal, 12 July 2024. Consulted 2026-08-31.
8. NIST. [Cybersecurity Framework 2.0](https://www.nist.gov/cyberframework), February 2024, voluntary guidance unless adopted by an applicable authority. Consulted 2026-08-31.

## Exercises

### Exercise 1

Classify ten constraint sources—physics, external interface, budget, schedule, law, regulation, contract, policy, consensus standard, and architecture decision—by authority, negotiability, verification, change path, and likely requirement subject.

### Exercise 2

Build an applicability and obligation record for a fictional regulation requiring incident notification “without undue delay” for providers of a defined critical service. Preserve ambiguity and identify authority needed.

### Exercise 3

Diagnose “The system shall comply with all applicable privacy and security standards.” Replace it with an auditable transformation and evidence structure without inventing jurisdiction or standards.

### Exercise 4

Compare a global strict baseline with jurisdiction-specific profiles for a service operating in three markets. Address conflicts, configuration, evidence, deployment, support, and change.

### Exercise 5

Develop a constraint/regulatory requirements strategy for an AI-assisted hospital scheduling system. Cover roles, classification, data, accessibility, safety, security, human oversight, suppliers, records, monitoring, change, and external authority.

## Answers to the Exercises

### Answer 1

Physics is externally immutable for the decision and verified by analysis/test; it constrains product behavior/design. An external interface is controlled by its owner/agreement and changes through interface governance. Budget and schedule are program constraints governed by sponsor/project authority; they shape scope and feasibility but should not be miswritten as product behavior. Law and regulation derive force from jurisdiction and applicability and can create organization, product, process, personnel, reporting, and evidence duties. Contracts bind parties and named scope/editions under contracting authority. Policy binds within its organizational authority and may admit exceptions through policy governance.

A consensus standard is not universally mandatory; adoption through regulation, contract, certification, or policy determines force and edition. An architecture decision becomes a lower-level design constraint through approved decision/configuration control and must trace to needs/trades. Negotiability ranges from impossible (physics) through authority-controlled (law/contract/policy) to decision-controlled (architecture). Every item needs source, scope, subject, verification/evidence, owner, validity dates, and change route; labels alone do not determine hardness.

### Answer 2

Record official source/provision, issuer, jurisdiction, publication/effective dates, definition of critical service/provider/incident, thresholds and exclusions, territorial reach, provider role, reporting authority, recipients, content, confidentiality, recordkeeping, enforcement, and cross-references. Facts include the organization's legal entity/role, offered service, market, incidents, users, infrastructure, and dates. Applicability remains `undetermined` until competent interpretation establishes that the service and organization meet definitions.

“Without undue delay” must not be replaced by an invented hour limit. Record the phrase, relevant guidance/decisions, operational consequence, escalation, and legal interpretation. Derived candidates can require incident detection/classification, timestamped escalation, authorized decision, evidence preservation, report preparation/transmission, update/correction, and deadline monitoring, while the organization retains notification judgment. Evidence includes incident timeline, decisions, submissions, acknowledgments, and controlled exceptions. Legal/regulatory authority resolves applicability, reportability, and timeliness.

### Answer 3

The sentence has no obligated subject beyond vague `system`, no source list, jurisdiction, adoption path, edition, clauses, applicability, behavior, evidence, or acceptance authority. `All applicable` delegates discovery and interpretation to whoever reads it and mixes privacy, security, law, standards, organizational processes, and product properties.

Create a controlled source register and applicability matrix. For each source, record official text/version/date, authority/adoption mechanism, facts, interpretation, subject, modality, conditions/exceptions, and owner. Allocate obligations across organization, product, supplier, process, personnel, and evidence. Derive atomic functional, quality, interface, constraint, process, record, and assurance requirements with rationale. Build bidirectional provision-to-requirement-to-architecture/control-to-evidence traces; record inapplicable and unresolved provisions. Establish change monitoring and competent privacy, security, legal, contracting, and certification review. No specific standard or jurisdiction can be inferred from the prompt.

### Answer 4

A global baseline can simplify design, operations, training, and evidence reuse, and may reduce configuration mistakes. It can also impose costly restrictions, create privacy/security conflicts, or still fail jurisdiction-specific procedural duties. Profiles preserve local fit and minimization but multiply requirements, configurations, tests, documentation, supplier terms, deployment controls, user communication, and support knowledge.

Use a shared obligation core only where semantics and evidence truly align. Model jurisdiction deltas with explicit applicability facts and configuration identities. Prevent an unauthorized profile from deployment through release controls and observable configuration. Test common and delta behavior, retain market-specific technical documentation and records, train support/escalation, and plan data/configuration migration when people or services cross markets. Conflicts go to competent authority; possible resolutions include segmentation, stricter compatible behavior, alternative architecture, restricted functionality, or market withdrawal. Source monitoring triggers impact analysis and revalidation for every deployed profile.

### Answer 5

Identify hospital, vendor, deployer/operator, clinician, administrator, patient, processor/controller, supplier, and authority roles; intended purpose and actual use; product/service and risk classifications; jurisdictions; clinical versus administrative decision boundary; data categories/flows; affected populations; and effective dates. Authoritative review determines applicable health, privacy, AI, accessibility, cybersecurity, employment, consumer, records, procurement, and medical-device provisions—none is assumed merely from the label “AI.”

Allocate organizational duties for governance, competence, risk, procurement, oversight, incident handling, transparency, rights/recourse, monitoring, and reporting. Product candidates cover authorized inputs, data provenance/quality, recommendation and uncertainty, human review/override, accessibility, security, logging, version/configuration, explanation/context, correction, failure/degraded behavior, and safe fallback. Supplier obligations cover documentation, evidence access, change/model notification, vulnerabilities/incidents, support, audit, exit, and data/model lifecycle. Preserve schedule fairness and clinical access outcomes separately from compliance proxies.

Evidence includes applicability decisions, risk/hazard/privacy/security analyses, data/model documentation, representative performance and subgroup results, human-factors/accessibility studies, interface and failure tests, change records, training, monitoring, incident/override/recourse records, supplier evidence, and post-deployment review. Changes to intended use, model, data, workflow, market, or supplier trigger reassessment. Internal engineering cannot establish legal applicability, clinical safety, discrimination acceptability, regulatory conformity, or ethical legitimacy; hospital governance, affected stakeholders, clinical/safety, privacy, security, accessibility, labor/ethics, legal, procurement, and applicable regulators/certifiers must decide within their authority. No external review is claimed.
