---
module_id: DARCH-024
program: Data Architecture Engineering
level: 1
module_number: 24
title: Stewardship Roles
status: complete
last_verified: 2026-09-03
---

# Stewardship Roles

## One-Page Review

### Governing question

How can an organization design stewardship as an authoritative, staffed, measurable operating capability for data definitions, metadata, quality, issues, controls, and consumer support without making stewards ceremonial owners, clerical catalog maintainers, or substitutes for accountable decision makers?

### Essential definitions

- **Data stewardship** is the sustained operational care of defined data and metadata under delegated authority, including maintenance, monitoring, issue coordination, evidence, and escalation.
- A **stewardship object** is the bounded subject under care: a concept, term, code set, attribute, schema, dataset, product, rule, quality control, lineage path, access classification, or issue queue.
- A **steward role** is a durable organizational role assigned duties, authority limits, capacity, service objectives, evidence obligations, and escalation for stewardship objects.
- A **business or domain steward** applies domain knowledge to meaning, rules, source assertions, quality expectations, and issue disposition.
- A **technical steward** maintains implementation metadata, schemas, lineage, controls, observability, and remediation coordination without silently deciding business meaning.
- A **metadata steward** curates discoverability, definitions, classifications, relationships, provenance, ownership links, and lifecycle state in governed metadata systems.
- A **quality steward** operates measurement, triage, root-cause coordination, exception tracking, and verification while accountable owners fund and accept material risk.
- **Delegated authority** is a bounded permission to decide or act on specified matters; it names limits, evidence, review, duration, and escalation.
- A **stewardship service objective** states expected response, decision, correction, publication, or review performance for a defined class of work.
- **Stewardship evidence** demonstrates assignment, work intake, decision basis, action, approval, result, exception, escalation, and lifecycle history.

### Central model, mechanism, or theorem

Represent a stewardship assignment as:

`S = (object, steward_role, duties, delegated_authority, inputs, workflows, service_objectives, evidence, escalation, effective_time)`

A viable assignment requires a named role, precise object, executable duties, sufficient competence and capacity, bounded authority, a supported workflow, measurable service expectations, durable evidence, and a path to an accountable owner. Stewardship distributes expert operational care; it does not erase ownership, legal responsibility, technical custody, producer obligations, consumer responsibility, or governing oversight.

### Critical invariants

- Every material stewardship object has a discoverable role assignment or an explicit reason and deadline for remaining unassigned.
- Stewardship duties and delegated decision rights are explicit; a steward is never expected to influence an outcome without authority or escalation.
- Accountable owners retain final answerability for scoped outcomes and risk even when stewards perform or approve routine work.
- Business meaning, technical implementation, metadata, quality, privacy, security, records, product, and reference-data concerns remain distinguishable even when one person fills several roles.
- Steward assignments name incumbents, deputies, effective intervals, capacity, required competence, conflicts, and succession.
- Work enters governed queues with priority, consequence, status, service objective, evidence, owner, dependencies, and escalation thresholds.
- Definition, schema, code, quality, classification, access, lineage, and lifecycle changes follow reviewable policies rather than informal edits.
- Stewardship evidence is proportionate, protected, retained, and linked to the object and decision; activity counts alone do not prove outcomes.
- Automation can route, validate, enrich, and enforce approved policy, but material semantic and risk judgments retain accountable human oversight.
- Stewardship performance is assessed through coverage, timeliness, recurrence, adoption, quality, consumer outcomes, control operation, capacity, and learning.

### Common failures

Common failures are appointing volunteer stewards without protected time; using a steward title as a substitute for an owner; assigning hundreds of assets to one person; expecting stewards to fix source defects without process authority; reducing stewardship to glossary entry; combining business and technical decisions without boundaries; opening issue queues without service objectives; measuring metadata fields completed rather than consumer outcomes; granting broad access because a steward needs evidence; failing to preserve decision rationale; allowing governance councils to perform every routine edit; treating tools as the operating model; leaving conflicts unresolved; and letting role assignments expire silently after reorganization.

### Compact example

A Supplier data domain lists a procurement analyst as steward for 340 tables. The analyst receives defect emails but cannot change onboarding rules, obtain engineering work, or escalate overdue corrections. The organization replaces the title with three bounded assignments: a domain steward maintains supplier concepts, codes, and rule proposals; a quality steward operates monitored controls and the defect queue; a technical steward maintains schemas, lineage, and remediation evidence. The Supplier owner grants routine approval limits, funds capacity, and accepts material exceptions. Service objectives vary by consequence, unresolved items escalate automatically, and the catalog links assignments, evidence, metrics, deputies, and effective dates.

### Connections

[DARCH-023](023-data-ownership-and-accountability.md) establishes accountable decision rights. This module turns delegated operational care into explicit roles and workflows before [DARCH-025](../ROADMAP.md) addresses data-product thinking, [DARCH-026](../ROADMAP.md) defines contracts and service expectations, and [DARCH-028](../ROADMAP.md) develops federated governance.

## Governing Question

“Who is the steward?” is not answered by a contact field. The useful questions are: steward of what; for which duties; under whose authority; with what competence, capacity, tools, and evidence; to what service expectation; and what happens when ordinary authority is insufficient?

Stewardship is the operational connective tissue between policy and daily data work. It translates accountable direction into maintained definitions, reviewed metadata, measured quality, resolved issues, usable products, applied controls, and informed consumers. When authority, workflow, and capacity are absent, the steward becomes a human routing label. When boundaries are absent, the steward can become an unelected owner or a control bottleneck. Good role design occupies the disciplined middle.

## Why This Matters

Data architecture decays through ordinary events: a source field changes, a term gains a second interpretation, a code is retired, a new consumer uses an old extract, a quality threshold begins failing, a classification becomes stale, or a lineage edge disappears. Owners cannot perform every maintenance action, and engineers cannot infer every domain rule. Stewardship supplies continuous expert care at the point where meaning and implementation meet.

[ISO 8000-150:2022](https://www.iso.org/standard/80753.html) addresses roles and responsibilities for data-quality management. Its relevance is structural: quality work requires documented responsibility, not an informal expectation that someone notices and acts.

[ISO 8000-61:2016](https://www.iso.org/standard/63086.html) presents a process reference model for data-quality management. Stewardship roles become operational when their work participates in repeatable planning, control, assurance, and improvement processes rather than isolated catalog campaigns.

[ISO/IEC 11179-3:2023](https://www.iso.org/standard/78915.html) specifies registry metamodel and basic attributes for metadata registries. A metadata steward needs explicit objects, identifiers, definitions, relationships, status, and administration rules so curation is more than prose editing.

W3C [DCAT 3](https://www.w3.org/TR/vocab-dcat-3/) provides a vocabulary for describing catalogs, datasets, data services, and distributions. W3C [PROV-O](https://www.w3.org/TR/prov-o/) supports interoperable provenance descriptions. These standards illustrate why catalog and provenance stewardship need defined structures and relationships, while local governance still determines authority, completeness, and fitness.

NIST's [Privacy Framework 1.0](https://www.nist.gov/privacy-framework/privacy-framework) and [Cybersecurity Framework 2.0](https://www.nist.gov/publications/nist-cybersecurity-framework-csf-20) connect roles, responsibilities, governance, risk, controls, and improvement. Stewardship cannot be separated from protection: metadata, samples, issue details, access, and evidence can themselves expose sensitive information.

OMB [M-19-23](https://www.whitehouse.gov/wp-content/uploads/2019/07/M-19-23.pdf) describes federal data governance and agency data roles. Its institutional setting is specific, but it reinforces the general distinction between durable organizational responsibilities and ad hoc volunteer work. Each organization must adapt role design to its laws, mandates, labor model, scale, and risk.

## Prerequisites and Retrieval

You should understand data domains, ownership, accountability, decision rights, products, metadata, schemas, lineage, quality, controls, privacy, security, records, service management, workflow, and organizational design.

Retrieve steward, custodian, owner, producer, consumer, subject-matter expert, metadata registry, catalog, business glossary, reference data, quality rule, issue, exception, change, provenance, lineage, classification, delegated authority, service objective, queue, triage, escalation, attestation, evidence, competence, capacity, segregation of duties, and succession.

As a retrieval test, inspect “The customer steward maintains Customer data.” Ask whether Customer means a concept, source system, product, table, attribute, or population; which duties “maintains” includes; which edits or approvals the role may make; what must escalate; what queue receives work; which deadlines apply; where evidence lives; how consumers participate; and who covers absence. If these cannot be answered, the statement identifies a hope, not an operating role.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish stewardship from ownership, accountability, custody, production, consumption, control ownership, and legal roles;
2. classify business, domain, technical, metadata, quality, privacy, security, records, product, reference-data, and analytics stewardship responsibilities;
3. define stewardship objects at useful semantic, product, implementation, control, and lifecycle scopes;
4. design charters that join duties, delegated authority, limits, competence, capacity, evidence, service objectives, and escalation;
5. build intake, triage, assignment, investigation, decision, remediation, validation, communication, and closure workflows;
6. govern glossary, schema, code, quality, lineage, classification, access, issue, exception, and consumer-support work;
7. distribute stewardship across domains while preserving enterprise interoperability, protection, and escalation;
8. apply automation without delegating unsupported semantic, legal, privacy, security, or risk judgments to tools;
9. measure coverage, workload, timeliness, recurrence, adoption, outcomes, control operation, and role health;
10. preserve stewardship through absence, reorganization, provider change, product retirement, and archival obligations.

## Core Exposition

**Begin with stewardship objects.** A role cannot steward “all Customer data” usefully unless the organization defines the relevant concepts, assertions, products, schemas, rules, classifications, and processes. Inventory objects at the level where recurring decisions and care occur.

Objects can nest. A domain steward may oversee Party semantics; a term steward curates `legal customer`; a reference-data steward manages customer-type codes; a product steward maintains a Customer Profile contract; and technical stewards care for implementations. Record relationships without assuming the broadest role performs every task.

**Write a stewardship charter.** A charter identifies purpose, objects, duties, authority, limits, accountable owner, required collaborators, work sources, workflow, service objectives, evidence, metrics, tools, funding, deputies, escalation, review, and termination. It is an operational contract, not a biography.

Use stable role identifiers and separately record incumbents. A charter assigned only to a person's name becomes stale at departure. A charter assigned only to a committee can make action anonymous. Combine durable role, named incumbent, effective interval, deputy, and accountable reporting line.

**Distinguish stewardship from ownership.** An owner answers for scoped decisions and outcomes, grants authority, secures resources, accepts defined risk within mandate, and resolves or escalates material conflicts. A steward performs sustained expert care and may decide routine matters within delegated limits.

A steward can approve a nonbreaking description correction while a material meaning change goes to the owner. A quality steward can close a verified defect but cannot accept an exception above the owner's risk threshold. This division increases throughput without diluting final accountability.

**Distinguish stewardship from custody.** Custodians operate storage, processing, access enforcement, backup, recovery, and deletion mechanisms. Technical stewards may work closely with custodians, yet implementation control does not establish semantic authority or lawful-purpose authority.

Conversely, a domain steward cannot directly alter a protected production table merely because the definition is wrong. Changes follow engineering, security, records, and release controls. Stewardship connects meaning to implementation through approved workflows.

**Distinguish role families.** Business or domain stewards curate concepts, rules, source interpretations, quality expectations, and issue priorities. Technical stewards maintain schemas, mappings, lineage, control configuration, operational metadata, and remediation coordination. Metadata stewards govern identifiers, descriptions, classifications, relationships, provenance, and lifecycle state.

Quality stewards operate measures, thresholds, monitoring, triage, root-cause coordination, exceptions, and verification. Reference-data stewards govern code sets, mappings, hierarchies, effective dates, and distribution. Product stewards maintain contracts, discoverability, support, consumer feedback, change notices, and evidence. These are lenses, not universal job titles.

**Add protection and records expertise.** Privacy stewards help connect purpose, data categories, subjects, notices, rights, minimization, sharing, and retention to local policy and qualified legal review. Security stewards connect classification, threats, controls, access, monitoring, incidents, and exceptions. Records stewards connect schedules, holds, disposition, archives, and evidence.

These roles do not automatically carry statutory authority. Their charters must show when they advise, concur, approve, operate a control, or escalate to a legally or organizationally accountable role. Combining them can improve context but may weaken independent challenge.

**Define analytics and AI stewardship.** Analytics stewards maintain metric definitions, dimensional meaning, approved transformations, interpretation limits, and report lineage. AI-oriented stewards may curate training-data descriptions, provenance, labeling guidance, usage constraints, evaluation evidence, and monitoring inputs.

Machine-generated descriptions, classifications, mappings, quality suggestions, and lineage should be labeled with method, confidence, source, time, and review state. A language model's plausible definition is not adopted business meaning. Human review should be proportional to consequence and uncertainty.

**Specify duties as verbs and outputs.** “Support metadata” is too vague. Prefer: review proposed terms; validate definition structure; map synonyms; confirm owner; record source; classify sensitivity; reconcile conflicts; publish approved versions; notify consumers; and retire superseded entries.

For each duty, state trigger, input, authority, output, evidence, service objective, and handoff. This exposes missing capabilities. If the steward must investigate defects but cannot access lineage or samples, the assignment is not executable.

**Delegate authority deliberately.** List decisions the steward may make without further approval: correct typographical metadata, accept a mapping within an approved code set, close a verified issue, or publish a preapproved compatible schema update. Define monetary, risk, semantic, privacy, security, operational, and compatibility limits.

Also list prohibited or escalated decisions: changing a regulated definition, accepting a critical defect, expanding purpose, overriding retention, granting privileged access, suppressing an incident, or breaking a product contract. Ambiguity encourages either paralysis or unauthorized action.

**Check competence.** A domain steward needs domain language, processes, sources, downstream uses, and decision context. A technical steward needs platform, schema, lineage, control, and release knowledge. Every steward needs governance workflow, evidence, protection, conflict, and escalation literacy appropriate to the role.

Use role profiles, onboarding, mentoring, communities of practice, observed work, and periodic qualification. Training completion alone does not prove competence. Examine decisions, issue investigations, consumer interactions, and correct escalation.

**Protect capacity.** Stewardship is work. Estimate incoming changes, issues, reviews, consultations, incidents, evidence, and improvement. Allocate protected time, staffing, tools, and backup. A role assigned as “ten percent when available” should not carry a critical queue with a one-day response objective.

Track arrival rate, work age, active load, waiting dependencies, rework, and leave coverage. Persistent backlog can indicate insufficient capacity, poor automation, excessive scope, unclear authority, or upstream process failure. It is a governance risk, not a personal productivity defect.

**Design an intake contract.** Define accepted channels and required fields: object, reporter, observed behavior, expected behavior, consequence, evidence, affected consumers, time window, sensitivity, urgency, and requested outcome. Provide a safe route for confidential or protected reports.

Normalize duplicates without erasing independent evidence. A catalog form can improve structure, but emergency and accessibility paths remain necessary. Automatically acknowledge receipt and identify routing, priority, owner, and expected next update.

**Triage by consequence and uncertainty.** Priority should consider safety, legal, privacy, security, financial, operational, consumer, reputational, and decision effects; breadth; duration; reversibility; deadline; evidence quality; and recurrence. Volume alone is not severity.

The steward may classify routine work under policy. High-consequence or uncertain cases require owner, security, privacy, legal, records, risk, or incident involvement. Record triage basis and allow reassessment as facts change.

**Operate an issue lifecycle.** A useful lifecycle includes intake, validation, classification, assignment, containment, investigation, decision, remediation, verification, communication, closure, and learning. Status names alone are insufficient; define entry, exit, evidence, authority, and clock behavior.

Separate “resolved” from “closed.” A workaround may restore output while root cause remains. Verification should check affected periods, downstream copies, derived products, reports, models, caches, exports, and consumer decisions. Closure records residual risk and recurrence prevention.

**Set service objectives.** Define acknowledgement, triage, decision, containment, correction, metadata publication, review, and consumer-notification expectations by consequence class. State measurement boundaries, business calendars, pauses, dependencies, exclusions, breach handling, and escalation.

Do not reward superficial closure. Pair timeliness with reopen rate, recurrence, correctness, consumer confirmation, and root-cause completion. Critical defects may prioritize containment and communication before permanent correction.

**Curate shared meaning.** A glossary term needs stable identity, preferred name, definition, scope, examples, exclusions, synonyms, related concepts, source, owner, steward, status, version, effective date, and change history. Definition quality requires domain reasoning, not merely template completion.

Resolve competing terms by showing context rather than forcing false uniformity. `Customer` may differ legitimately between contracting, billing, service, and legal contexts. Stewardship should make differences discoverable, map relationships, and identify which meaning applies to each product and decision.

**Govern schemas and models.** Stewards review whether implementations preserve approved meaning, keys, cardinality, units, codes, time, null semantics, and classifications. Technical stewards connect conceptual and logical decisions to physical schemas and transformations.

Schema review should fit delivery flow. Machine checks can enforce compatibility, naming, required metadata, and policy. Humans examine meaning, consumer impact, risk, and exceptions. Emergency change paths require later evidence and reconciliation.

**Govern reference data.** Code sets and hierarchies often cross products. A reference-data steward maintains canonical identifiers, descriptions, mappings, effective periods, ownership, distribution, consumer impact, and retirement rules.

Never overwrite historical meaning when a code changes. Version mappings and distinguish correction from business-effective change. Consumers need notice, migration windows, and rules for late-arriving facts and historical recomputation.

**Operate quality stewardship.** Translate declared fitness needs into measurable rules with object, dimension, population, computation, threshold, window, severity, owner, steward, consumers, exceptions, and response. Monitor both data results and control operation.

The quality steward validates signals, coordinates root cause, connects source and product actors, maintains evidence, and verifies correction. The role should not absorb accountability for defects created by processes it cannot change. Escalation moves unresolved structural causes to accountable leadership.

**Maintain lineage and provenance.** Lineage links transformations and movement; provenance describes origins, activities, agents, and derivations. Stewards define required granularity, ensure critical paths are captured, validate material edges, and reconcile technical traces with business meaning.

Automated lineage can be incomplete for manual uploads, external files, dynamic queries, or semantic logic. Record coverage and confidence. Missing lineage is itself a managed issue, especially when it impairs incident response, correction, rights handling, or audit.

**Steward classification and access metadata.** Maintain sensitivity, criticality, subject category, purpose constraints, jurisdiction, retention, sharing, and control metadata under qualified policy. Classification changes should trigger impact review and control reconciliation.

Stewards may recommend or apply approved classifications; they do not acquire unrestricted access to content. Use least privilege, masked evidence, controlled samples, logging, purpose limitation, and time-bound access. Issue records and catalog descriptions may themselves require protection.

**Connect producers and consumers.** Producers explain creation processes, limits, changes, and known defects. Consumers describe decisions, fitness needs, incidents, and usage. Stewards maintain the feedback loop and translate reports into actionable work.

Do not let stewardship become a buffer that hides producers from consumers. Direct collaboration is often necessary, while the steward preserves routing, commitments, evidence, and consistent interpretation. Repeated consumer confusion indicates a product or definition defect.

**Use forums with clear purposes.** Steward communities share patterns and resolve cross-domain questions. Domain forums handle local definitions and priorities. Enterprise forums decide interoperability, shared semantics, standards, and escalated conflicts. Control functions provide independent challenge.

Every forum should have decision scope, quorum, inputs, outputs, evidence, response expectations, and escalation. Meetings are not the operating model. Routine work should continue through queues and delegated policies between meetings.

**Federate stewardship.** Central teams can define minimum metadata, tooling, training, assurance, and enterprise issue paths. Domain stewards contribute context and act near source processes and products. Federation succeeds when local autonomy and shared obligations are both explicit.

Common vocabulary does not require one universal definition. Require identifiers, context, mappings, product contracts, and conflict paths. Central teams should not become a bottleneck; domains should not create incompatible local rules without visibility.

**Design segregation and challenge.** The same steward may propose and implement a low-risk description change. High-risk access, deletion, financial corrections, regulated terms, critical exceptions, or evidence destruction may require separate approval, execution, and review.

Define conflict-of-interest disclosure and substitution. A steward whose performance is measured by low defect counts should not unilaterally suppress defects. Independent sampling and consumer feedback reduce incentives to curate appearances rather than outcomes.

**Automate bounded work.** Tools can detect missing fields, validate formats, infer candidate lineage, suggest classifications, route issues, calculate clocks, enforce approval paths, notify consumers, and preserve history. Policy-as-code can prevent many routine violations.

Automation needs an owner, version, test evidence, failure handling, override policy, and monitoring. False positives create queue overload; false negatives create false assurance. Preserve the distinction among observed fact, inferred metadata, steward assertion, and owner-approved decision.

**Integrate tools without worshiping them.** A catalog, registry, ticket system, lineage service, quality platform, repository, and messaging channel may each hold part of the record. Define a system of record for assignments, objects, decisions, work status, and evidence, with stable links among them.

Buying a catalog does not supply authority, capacity, or adoption. Minimize duplicate entry, support accessible workflows, expose relevant context at decision time, and design for export and provider exit. Stewardship must survive a tool replacement.

**Measure role health and outcomes.** Coverage asks whether critical objects have viable assignments, not whether every table has a name. Work measures include arrival, age, breaches, dependencies, reopens, recurrence, and capacity. Outcome measures include definition adoption, quality attainment, consumer success, corrected source processes, control effectiveness, and reduced ambiguity.

Segment results by consequence and object. Averages can hide one critical overdue issue among hundreds of trivial completions. Pair quantitative measures with sampled decisions, interviews, exercises, and independent assurance.

**Manage exceptions.** An exception names rule, object, reason, evidence, consequence, controls, approver, steward, affected consumers, start, expiry, remediation, review, and residual risk. A steward can administer the record and approve only within delegated limits.

Expired exceptions should not renew silently. Repeated exceptions reveal unrealistic standards, insufficient investment, or structural source defects. Trend them and require accountable decisions about correction or policy change.

**Exercise the operating model.** Test a disputed term, breaking schema, critical quality failure, incorrect classification, missing lineage, access complaint, provider outage, steward absence, cross-domain conflict, and product retirement. Observe routing, authority, evidence, clocks, communication, and escalation.

Exercises should reveal weak design without blaming participants for following it. Record findings, owners, deadlines, and verification. Retest material failures. A role chart that has never met a contested decision is unproven.

**Preserve continuity.** Assign deputies, maintain runbooks, document open work, and rotate knowledge. On departure, revoke access, transfer queues, preserve evidence, update incumbent records, notify collaborators, and verify acceptance.

Reorganizations require object and obligation inventories. A new team name does not automatically inherit competence or capacity. Temporary gaps escalate to the accountable owner; they do not become permanent orphan states.

**Close stewardship deliberately.** Retirement examines active products, downstream copies, historical reports, models, contracts, holds, retention, rights, incidents, and support. Transfer surviving duties to archival, records, security, product, or successor-domain roles.

Preserve assignment and decision history for the required period. Remove obsolete access and queue routing. A retired catalog entry remains discoverable enough to explain history without suggesting active support.

**Treat powerless stewardship as a design defect.** If stewards repeatedly request action with no response, leadership must grant authority, resource accountable teams, revise service commitments, or accept and record risk. Adding training or another form will not repair missing mandate.

The practical test is whether a steward can receive a material question, assemble evidence, decide within bounds or reach the right authority, coordinate action, inform affected parties, and demonstrate the result within an agreed time. Anything less is a directory entry.

## Definitions and Notation

Let `O` be a stewardship object. Define an assignment:

`S(O) = (r, d, a, i, w, q, e, x, t)`

where `r` is the durable steward role, `d` duties, `a` delegated authority and limits, `i` required inputs and collaborators, `w` supported workflows, `q` service objectives, `e` evidence obligations, `x` escalation, and `t` effective interval.

Let `Incumbent(r,t)` and `Deputy(r,t)` identify current people separately from the durable role. Let `Competent(r,O,t)` and `Capacity(r,O,t)` state evidenced capability and available work capacity. An assignment can exist syntactically while failing operationally when either predicate is false.

Represent a work item as `W = (object, class, reporter, evidence, consequence, priority, assignee, state, clocks, dependencies, decisions, actions, validation, communications, closure)`. State transitions require declared evidence and authority rather than a status-label change alone.

For service class `c`, define `SLO_c = (event, target, window, calendar, pauses, exclusions, measure, breach, escalation)`. Timeliness metrics require these semantics; a percentage without population and clock rules is not reproducible.

A coverage audit computes required objects `O*`, assignments `S*`, and reports missing steward, expired incumbent, absent delegated authority, missing workflow, absent service objective, insufficient capacity, missing deputy, inaccessible evidence, or missing escalation. Coverage does not prove correct judgment or good outcomes.

## Mechanisms, Invariants, or Proof Structure

Use ten gates to assess a material stewardship assignment.

**1. Charter gate.** Define purpose, objects, duties, accountable owner, consumers, boundaries, effective interval, and termination.

**2. Scope gate.** Identify exact concepts, attributes, products, schemas, rules, codes, controls, jurisdictions, uses, and lifecycle states under care.

**3. Authority gate.** Grant routine decision rights, name limits and required concurrence, and prohibit unsupported risk or legal decisions.

**4. Competence gate.** Verify domain and technical knowledge, governance literacy, protection awareness, training, observed practice, deputies, and conflicts.

**5. Workflow gate.** Implement intake, triage, assignment, investigation, decision, remediation, validation, communication, closure, and learning.

**6. Quality and metadata gate.** Maintain definitions, schemas, codes, lineage, provenance, classifications, quality rules, exceptions, and product context.

**7. Protection gate.** Apply least privilege, purpose, minimization, security, privacy, records, segregation, evidence protection, and incident paths.

**8. Service gate.** Set consequence-based objectives, capacity, priority, clock rules, dependency handling, consumer expectations, and breach escalation.

**9. Evidence gate.** Preserve assignments, changes, decisions, approvals, actions, tests, outcomes, limitations, exceptions, and review history.

**10. Lifecycle gate.** Exercise roles and manage absence, reorganization, provider change, succession, retirement, archival duties, measurement, and improvement.

The executable example checks four narrow assignment failures: no named steward, absent delegated authority, missing escalation, and missing service objective.

<!-- bijux-verify: {"id":"stewardship-role-integrity","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"assignments=4\nvalid=0\nfindings=consent-metadata:missing-escalation,customer-glossary:missing-steward,product-catalog:missing-service-objective,supplier-quality:missing-delegated-authority\nready=false\n","stderr":""}} -->
```python
assignments = (
    {"id": "customer-glossary", "steward": False, "authority": True, "escalation": True, "service_objective": True},
    {"id": "supplier-quality", "steward": True, "authority": False, "escalation": True, "service_objective": True},
    {"id": "consent-metadata", "steward": True, "authority": True, "escalation": False, "service_objective": True},
    {"id": "product-catalog", "steward": True, "authority": True, "escalation": True, "service_objective": False},
)

findings = []
valid = 0
for assignment in assignments:
    local = []
    if not assignment["steward"]:
        local.append("missing-steward")
    if not assignment["authority"]:
        local.append("missing-delegated-authority")
    if not assignment["escalation"]:
        local.append("missing-escalation")
    if not assignment["service_objective"]:
        local.append("missing-service-objective")
    if local:
        findings.extend(f"{assignment['id']}:{finding}" for finding in local)
    else:
        valid += 1

print(f"assignments={len(assignments)}")
print(f"valid={valid}")
print("findings=" + ",".join(sorted(findings)))
print(f"ready={str(valid == len(assignments)).lower()}")
```

The checker validates four declared assignment predicates only. It does not prove lawful or organizational authority, competence, adequate capacity, correct definitions, complete lineage, effective controls, fulfilled service objectives, good decisions, source correction, consumer success, or production readiness. Those require local mandates, role observation, protected access, workflow evidence, sampled decisions, exercises, outcome measures, risk and legal review, and accountable approval.

## Alternatives and Trade-Offs

**Central versus embedded stewards.** Central stewards improve consistency, independence, and shared expertise but can lack context and become a queue bottleneck. Embedded stewards understand processes and relationships but may diverge or face local incentives. Federate minimum controls and communities while locating ordinary action near domains.

**Dedicated versus part-time roles.** Dedicated stewards offer capacity and identity for high-volume or high-consequence objects. Part-time roles preserve practitioner context and may suit smaller scopes. In either case, size work, protect time, supply deputies, and expose overload.

**Role specialization versus consolidation.** Separate domain, technical, quality, metadata, privacy, and product roles clarify expertise and challenge but increase handoffs. Consolidation lowers coordination cost but risks conflicts and excessive breadth. Combine roles only with explicit boundaries and competence.

**Approval versus policy-bounded autonomy.** Requiring owner approval for every edit preserves central control but slows routine care. Delegated authority improves throughput but needs limits, evidence, sampling, and revocation. Reserve owner decisions for material meaning, risk, cost, and conflict.

**Queue-based versus relationship-based work.** Queues improve visibility, priority, and evidence; relationships speed clarification and build trust. Support direct collaboration while ensuring consequential work, commitments, and outcomes enter the record.

**Uniform versus consequence-based service.** One objective is simple but wastes attention on trivial work and under-serves critical issues. Consequence tiers improve allocation but require reliable classification, reassessment, and protection from priority gaming.

**Manual versus automated curation.** Manual review handles nuance; automation scales detection, enrichment, routing, and enforcement. Preserve provenance, confidence, exception paths, human review, and monitoring for automated output.

**Rich evidence versus minimization.** Detailed issue and decision records improve learning and assurance but can reveal personal data, vulnerabilities, confidential strategy, or privileged advice. Capture necessary facts with access, retention, redaction, and purpose controls.

## Failure Modes and Misconceptions

1. **A steward is the data owner.** Stewardship performs delegated care; final accountability and risk acceptance remain separately assigned.
2. **A subject-matter expert is automatically a steward.** Expertise does not supply charter, authority, capacity, workflow, or evidence duty.
3. **Stewardship is catalog entry.** Metadata curation is one responsibility within a broader operating capability.
4. **Technical stewards decide business meaning.** They preserve implementation semantics and escalate domain ambiguity.
5. **Business stewards can bypass engineering controls.** Semantic authority does not grant unrestricted production access.
6. **Quality stewards own every defect.** Source processes and product owners retain scoped outcome obligations and funding authority.
7. **Volunteer effort is free capacity.** Unprotected stewardship competes with primary duties and produces hidden backlog.
8. **One steward can cover every table in a domain.** Scope must match workload, consequence, competence, and deputies.
9. **A council can steward all routine work.** Collective forums are useful for standards and conflicts but weak as anonymous work queues.
10. **More resolved tickets means better data.** Premature closure and repeated defects can inflate activity while outcomes worsen.
11. **A tool creates stewardship.** Tools support objects and workflows; they do not create mandate, judgment, resources, or adoption.
12. **Generated metadata is authoritative.** Inference needs provenance, confidence, review state, and consequence-based validation.
13. **Stewards need broad data access.** Least privilege and protected evidence remain necessary.
14. **No escalations means the model works.** It may mean stewards cannot escalate or participants bypass the process.
15. **Training proves competence.** Decisions, investigations, exercises, and outcomes provide stronger evidence.
16. **Reorganization transfers duties automatically.** Successors need explicit objects, work, authority, evidence, capacity, and acceptance.
17. **Retirement ends all stewardship.** Historical, archival, rights, incident, retention, and consumer duties may continue.

## Worked Examples

### Example 1

A glossary has 4,000 terms and one nominal steward. The organization classifies critical terms, assigns domain stewards with deputies, delegates routine editorial changes, sets review objectives, and routes cross-domain conflicts to an enterprise semantic authority.

### Example 2

A quality steward receives duplicate-supplier alerts but procurement controls onboarding. The steward validates evidence, opens source remediation, tracks affected products, and escalates repeated failures. The Supplier owner funds prevention and accepts any bounded exception.

### Example 3

Automated lineage omits spreadsheet uploads used in regulatory reporting. The technical steward labels coverage limits, adds manual provenance capture, prioritizes the critical gap, verifies the end-to-end path, and retains evidence rather than presenting the graph as complete.

### Example 4

A domain steward proposes changing `active customer` from a twelve-month to six-month window. Because the change affects contracts, reporting, and models, delegated editorial authority is insufficient. The owner decides after consumer, finance, legal, and technical impact review.

### Example 5

A product catalog description is generated from schemas. The product steward reviews meaning and limitations, marks generated provenance and confidence, corrects sensitive details, obtains owner approval for material claims, and publishes an effective version with consumer notice.

### Example 6

A privacy steward discovers that issue tickets contain unmasked identifiers. The team restricts access, redacts retained records, changes intake guidance, provides protected evidence channels, tests the control, and evaluates whether notification or further response is required.

### Example 7

Two domains publish incompatible country codes. Reference-data stewards document authority, mappings, effective intervals, and consumer impact. A cross-domain forum chooses an exchange representation while allowing justified local codes behind explicit product contracts.

### Example 8

The only payments steward goes on leave during a schema migration. A trained deputy activates under a dated assignment, can approve compatible changes, and escalates breaking changes. Queue transfer and decision evidence preserve continuity.

### Example 9

A steward dashboard reports 99 percent ticket closure, but issues recur monthly. Measures add reopen rate, source-process correction, downstream validation, consumer confirmation, and recurrence. Leadership funds structural remediation instead of rewarding rapid administrative closure.

### Example 10

A retired analytics product remains embedded in annual reports. The product steward transfers historical definitions, lineage, support, retention, and correction duties to an archive role, removes obsolete routing and access, and preserves discoverable decision history.

## Cross-Program Connections

- **Data engineering:** schemas, pipelines, tests, observability, lineage, remediation, backfills, and release controls implement stewarded decisions.
- **Platform engineering:** catalogs, identity, workflow, policy enforcement, evidence, notifications, queues, and metrics provide stewardship infrastructure.
- **Product management:** contracts, consumers, support, service objectives, roadmaps, feedback, change communication, and retirement shape product stewardship.
- **Security and privacy:** classification, access, purpose, controls, incidents, minimization, risk, and evidence constrain stewardship work.
- **Software engineering:** code ownership, maintainers, review rules, issue triage, service operation, and dependency management offer useful analogies with different objects.
- **Business and enterprise architecture:** capabilities, domains, operating models, decision rights, organization, value, and governance locate roles and escalation.
- **Records and legal practice:** legal roles, retention, holds, disposition, privilege, contracts, and regulatory evidence affect authority and lifecycle.
- **Systems engineering:** configuration management, interface control, verification independence, anomaly resolution, assurance, and lifecycle responsibility parallel disciplined stewardship.

## References

1. ISO, *8000-150:2022 Data quality—Part 150: Data quality management: Roles and responsibilities*, 2022. <https://www.iso.org/standard/80753.html>
2. ISO, *8000-61:2016 Data quality—Part 61: Data quality management: Process reference model*, 2016. <https://www.iso.org/standard/63086.html>
3. ISO/IEC, *11179-3:2023 Metadata registries (MDR)—Part 3: Metamodel for registry common facilities*, 2023. <https://www.iso.org/standard/78915.html>
4. W3C, *Data Catalog Vocabulary (DCAT)—Version 3*, W3C Recommendation, 2024. <https://www.w3.org/TR/vocab-dcat-3/>
5. W3C, *PROV-O: The PROV Ontology*, W3C Recommendation, 2013. <https://www.w3.org/TR/prov-o/>
6. NIST, *Privacy Framework: A Tool for Improving Privacy through Enterprise Risk Management*, Version 1.0, 2020. <https://www.nist.gov/privacy-framework/privacy-framework>
7. Pascoe, C., Quinn, S., and Scarfone, K., *The NIST Cybersecurity Framework (CSF) 2.0*, NIST CSWP 29, 2024. <https://www.nist.gov/publications/nist-cybersecurity-framework-csf-20>
8. U.S. Office of Management and Budget, *M-19-23 Phase 1 Implementation of the Foundations for Evidence-Based Policymaking Act of 2018*, 2019. <https://www.whitehouse.gov/wp-content/uploads/2019/07/M-19-23.pdf>

## Exercises

### Exercise 1

Design stewardship charters for a Customer domain, Customer Profile product, identity schema, customer-type reference set, and customer-quality issue queue. Define objects, duties, authority, limits, competence, capacity, evidence, service objectives, and escalation.

### Exercise 2

Redesign a volunteer stewardship network in which 30 analysts each steward hundreds of tables without protected time. Include consequence-based scope, workload estimation, role families, deputies, tooling, funding, forums, and assurance.

### Exercise 3

Create an end-to-end workflow for a critical data-quality issue that affects a regulated report and exposes sensitive data in evidence. Include intake, triage, protection, containment, decision rights, correction, validation, communication, closure, and learning.

### Exercise 4

Design a federated metadata-stewardship model for six domains that disagree about shared terms and codes. Preserve legitimate local meaning while enabling exchange, discovery, provenance, protection, and enterprise escalation.

### Exercise 5

Build a stewardship assurance scorecard that avoids catalog-completion and ticket-closure vanity metrics. Define coverage, workload, capacity, timeliness, quality, recurrence, adoption, consumer outcomes, control operation, lifecycle, and sampling.

## Answers to the Exercises

### Answer 1

Assign the Customer domain steward concepts, domain rules, source interpretations, and cross-product issue coordination under the Customer owner. Assign the product steward contract metadata, consumer support, quality disclosures, change notices, and lifecycle under the product owner. Assign the technical steward schema semantics, mappings, lineage, compatibility evidence, and implementation coordination. Assign the reference-data steward identifiers, labels, mappings, effective intervals, distribution, and retirement. Assign the quality steward rules, signals, triage, root-cause coordination, exceptions, verification, and recurrence analysis.

Each charter names exact objects and routine decisions. Typographical corrections, approved compatible mappings, and verified issue closure can be delegated; regulated meaning changes, breaking schemas, critical exceptions, new purposes, and material risk escalate. Record competence, allocated capacity, deputy, queue, consequence-based response and correction objectives, evidence locations, collaborators, effective dates, and review. Link every role to one accountable owner without pretending the owner performs every duty.

### Answer 2

Inventory work by critical object and consequence rather than assigning every physical table equally. Group tables beneath domain concepts, products, schemas, controls, and shared reference objects. Estimate issue arrivals, changes, reviews, consumer consultations, incidents, and evidence work. Establish dedicated stewards for high-volume or high-consequence scopes and protected part-time roles for smaller scopes. Separate domain, technical, metadata, quality, and protection responsibilities where competence or independence requires it.

Grant bounded authority, create supported queues and service objectives, and assign deputies. Automate completeness checks, routing, reminders, safe evidence links, and routine policy enforcement while preserving human semantic decisions. Fund training and communities of practice. Monitor age, breaches, recurrence, capacity, adoption, consumer outcomes, and role vacancies. Sample work and exercise absences and conflicts. Escalate unfunded demand to accountable owners instead of hiding it as analyst underperformance.

### Answer 3

The intake record captures affected report, data objects, period, expected and observed results, decision consequence, protected evidence location, reporter, and known consumers. Automated acknowledgement starts a critical clock without copying sensitive values into general tickets. A quality steward validates the signal; privacy and security roles protect evidence and assess exposure; an incident lead coordinates containment; the source owner directs process correction; the product owner directs consumer disclosure and output recovery; and regulated-report authority decides filing consequences.

Trace lineage, bound affected populations and periods, suspend or label unsafe outputs, preserve evidence, and notify authorized consumers. Correct the source and derived states through controlled releases and backfills. Independent validation checks source, product, report, access, caches, and downstream copies. Closure requires authority, consumer communication, residual risk, and recurrence action—not merely restored output. Retain records under appropriate access and schedule, measure every clock, review the role response, fund structural prevention, and retest the scenario.

### Answer 4

The central stewardship capability defines stable identifiers, minimum metadata, definition structure, context fields, provenance, status, versioning, protection, exchange requirements, tooling, assurance, and an enterprise conflict path. Each domain assigns stewards who curate local concepts and codes, document sources and consumers, and decide within delegated domain authority. Shared objects receive named reference-data or semantic stewards and accountable owners.

Do not force one `Customer` definition when contracting, billing, service, and legal contexts differ. Publish each scoped concept, explicit relationships, transformations, compatibility limits, and product usage. For exchange, select shared identifiers or mapped representations with effective intervals and loss rules. DCAT-like catalog relationships and provenance descriptions improve discovery but do not decide business authority. Cross-domain disputes use documented evidence, required consultation, deadlines, one final authority, dissent, and appeal. Metrics cover adoption, unresolved conflicts, mapping defects, consumer comprehension, and stale relationships.

### Answer 5

Coverage reports critical objects with active role, incumbent, deputy, charter, authority, workflow, service objective, capacity, and escalation. It flags vacancies, expired assignments, inaccessible evidence, excessive spans, and unsupported duties. Workload shows arrivals, age distribution, waiting dependencies, consequence, rework, and available capacity. Timeliness uses declared acknowledgement, triage, decision, containment, correction, review, and notification clocks with breach causes.

Outcome measures include definition adoption, schema and code compatibility, quality-objective attainment, source-process correction, recurrence, lineage coverage and confidence, classification accuracy, exception expiry, consumer success, and control operation. Lifecycle measures cover reviews, succession acceptance, access revocation, transfers, and retirement closure. Segment by consequence and avoid averages that hide critical failures. Sample assignments, decisions, evidence, and closures; interview producers and consumers; exercise incidents and absences; distinguish self-assessment from independent review; and require funded action on findings.
