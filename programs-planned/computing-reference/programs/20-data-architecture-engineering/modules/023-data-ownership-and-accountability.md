---
module_id: DARCH-023
program: Data Architecture Engineering
level: 1
module_number: 23
title: Data Ownership and Accountability
status: complete
last_verified: 2026-09-03
---

# Data Ownership and Accountability

## One-Page Review

### Governing question

How can an organization assign and enforce accountable decision rights for data meaning, use, quality, protection, access, products, incidents, change, and lifecycle without confusing ownership with legal title, physical custody, technical administration, stewardship, or unrestricted control?

### Essential definitions

- **Accountability** is the obligation to answer for decisions and outcomes, ensure action, provide evidence, and accept escalation or consequence.
- A **data owner** is an organizationally authorized accountable role for a precisely scoped set of data decisions and outcomes; the title does not imply personal property rights.
- **Decision right** is authority to make or approve a named decision within limits, such as defining meaning, accepting quality risk, granting access, or retiring a product.
- **Responsibility** is an assigned duty to perform work; it can be delegated, while ultimate accountability may remain with the delegator.
- **Stewardship** is expert operational care for definitions, rules, quality, metadata, issue resolution, and adoption under delegated authority.
- **Custody** is operational control of storage, processing, transmission, backup, or deletion mechanisms.
- A **data product owner** is accountable for consumer value and the product contract, including quality, service, support, change, protection, and lifecycle.
- A **source authority** decides which assertion is authoritative for a subject, predicate, context, jurisdiction, use, and time.
- **Governance** evaluates, directs, and monitors organizational data use and protection; **management** plans and operates within that direction.
- **Accountability evidence** links decision, scope, authority, resources, action, outcome, review, exception, and escalation through time.

### Central model, mechanism, or theorem

Represent an accountability assignment as:

`A = (subject, accountable_role, decisions, outcomes, scope, authority, obligations, resources, evidence, escalation, effective_time)`

Represent a decision record as:

`D = (question, options, constraints, evidence, decision, approver, rationale, conditions, review, outcome)`

An owner label is valid only if the role has clear decision rights, sufficient authority and resources, measurable outcomes, evidence duties, conflict and escalation paths, and lifecycle coverage. Accountability must be singular for a defined decision scope, but execution and consultation can be distributed across stewards, custodians, producers, consumers, risk functions, and service providers.

### Critical invariants

- Every material data decision and outcome has exactly one accountable organizational role at a declared scope; this need not mean one person owns all data.
- Accountability, responsibility, consultation, information, stewardship, custody, processing, legal roles, and source authority remain distinct.
- The accountable role has sufficient mandate, competence, capacity, budget, access, and escalation power to affect the outcome.
- Delegation names task, limits, recipient, evidence, duration, oversight, and revocation; it does not erase the delegator's retained accountability.
- Authority is scoped by subject, predicate, product, purpose, jurisdiction, time, lifecycle, and risk rather than a vague domain name.
- Conflicts among business value, quality, security, privacy, legal, records, safety, and consumer needs use explicit decision and escalation rules.
- Access approval, data use, quality-risk acceptance, model change, incident response, and retirement have durable decision evidence.
- Vendors and platform teams can accept contractual or operational responsibility without silently becoming accountable for the organization's domain meaning or lawful use.
- Temporary absence, reorganization, transfer, and retirement have succession rules so accountability never becomes an orphaned catalog field.
- Governance measures outcomes and evidence, not the percentage of assets carrying an owner label.

### Common failures

Common failures are naming a senior executive as owner of every dataset; assigning a team mailbox with no decision rights; setting two accountable owners to avoid disagreement; making data engineers responsible for business definitions; treating storage administrators as legal or semantic owners; assuming producers own every downstream use; asking stewards to fix quality without process authority; delegating work without oversight; approving access without purpose or expiry; letting product owners accept legal or security risk outside mandate; confusing GDPR controller obligations with an internal owner title; outsourcing operations and accountability together; measuring governance by completed RACI cells; leaving owners unchanged after reorganization; and recording decisions only in transient meetings.

### Compact example

A Customer Profile product lists the Chief Data Officer, CRM manager, platform team, privacy officer, and analytics lead as “owners.” No one can approve definition changes or resolve consent conflicts. The organization replaces the label with a decision matrix: the Party domain executive is accountable for identity semantics and source corrections; the product owner for consumer contract and SLOs; the privacy controller role for lawful-purpose obligations; security for risk controls within its mandate; platform custody for technical operation; stewards for definitions and quality workflows. Cross-cutting conflicts escalate to a data governance body, and every exception has scope, evidence, expiry, and review.

### Connections

[DARCH-021](021-business-capabilities-and-data-domains.md) establishes domain and product candidates, while [DARCH-022](022-domain-boundaries.md) scopes their models and interactions. This module assigns decision accountability before [DARCH-024](../ROADMAP.md) details stewardship work, [DARCH-026](../ROADMAP.md) defines service expectations, and [DARCH-028](../ROADMAP.md) addresses federated governance.

## Governing Question

“Who owns this data?” is usually several questions compressed into one. Who defines it? Who may write it? Who determines authoritative truth? Who approves access and purpose? Who funds quality? Who runs the platform? Who supports consumers? Who responds to an incident? Who bears legal obligations? Who decides retirement?

Answering with one person's name creates either impossible breadth or false assurance. The correct design decomposes decision types, assigns one accountable role to each scope, links supporting responsibilities, and ensures authority and resources match expectations. Ownership then becomes a governed mechanism for decisions and outcomes rather than an honorific.

## Why This Matters

Unowned data decays. Definitions diverge, quality issues circulate, access accumulates, consumers receive no notice, and incidents cross organizational gaps. Nominal ownership is nearly as dangerous: dashboards look complete while listed people cannot change source processes or fund remediation.

[ISO/IEC 38505-1:2026](https://www.iso.org/standard/87195.html) applies governance principles to the effective, efficient, acceptable use and protection of data and addresses governing-body direction and confidence. It locates data accountability within organizational governance rather than only IT administration.

[ISO 8000-150:2022](https://www.iso.org/standard/80753.html) specifies considerations for establishing and documenting roles and responsibilities in data-quality management. This reinforces that durable role implementation requires documentary evidence, not just a chart.

The NIST [Cybersecurity Framework 2.0](https://www.nist.gov/publications/nist-cybersecurity-framework-csf-20) places roles, responsibilities, and authorities in its Govern function and links leadership accountability, communication, enforcement, resources, and improvement. Data accountability must likewise include authority, resources, and feedback.

Legal accountability has its own vocabulary. The EU [General Data Protection Regulation](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679) includes an accountability principle and obligations for controllers to implement and demonstrate appropriate measures. An internal “data owner” title neither creates nor displaces controller, processor, data-subject, supervisory, or other legal roles; qualified counsel must map them in context.

## Prerequisites and Retrieval

You should understand data domains, products, assertions, authority, governance, management, quality, security, privacy, records, risk, organizational design, service operation, and lifecycle.

Retrieve accountability, responsibility, authority, ownership, stewardship, custody, control, controller, processor, producer, consumer, system of entry, system of reference, product owner, decision right, mandate, delegation, segregation of duties, conflict of interest, RACI, RAPID, approval, exception, attestation, evidence, escalation, succession, and outcome.

As a retrieval test, inspect “Finance owns Customer data.” Ask which finance role; person or accountable position; which Customer concept; which assertions, products, jurisdictions, uses, and times; which decisions it may make; which outcomes it answers for; what authority and budget it has; who performs work; how privacy, security, and domain conflicts resolve; and who succeeds it. Without those coordinates, ownership is not operational.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish accountability, responsibility, authority, ownership, stewardship, custody, processing, production, consumption, and legal roles;
2. decompose data governance into explicit decision types and outcome obligations;
3. assign singular accountability at a precise subject, predicate, product, purpose, jurisdiction, time, and risk scope;
4. verify that role mandate, competence, capacity, funding, access, segregation, and escalation support the assignment;
5. design delegation, consultation, execution, evidence, review, and revocation without losing accountability;
6. establish decision and escalation paths across domain, product, platform, security, privacy, legal, records, risk, and executive roles;
7. govern source authority, quality-risk acceptance, access, use, change, incident, correction, and retirement decisions;
8. preserve accountability through service providers, reorganizations, absence, succession, mergers, transfers, and product retirement;
9. measure accountability through decisions, outcomes, issue resolution, consumer evidence, incidents, and assurance rather than labels;
10. create reviewable records that demonstrate what was decided, by whom, under what authority, with what evidence and result.

## Core Exposition

**Begin with decisions, not titles.** List recurring decisions: define a concept, establish a business key, select a source authority, approve a schema change, accept a quality exception, authorize a purpose, classify data, approve access, set retention, correct history, publish a product, respond to an incident, and retire an asset.

For each, state outcome and consequence. A title becomes meaningful only after it is attached to named decisions. “Data Owner” without a decision inventory encourages people to assume someone else holds authority.

**Define accountability precisely.** An accountable role must answer for the outcome, ensure responsibilities are assigned, obtain resources, monitor evidence, resolve or escalate conflicts, and accept review. It need not perform every task or approve every routine action.

Make accountability singular per decision scope. Two accountable roles create ambiguity when they disagree. Split the scope, name a higher adjudicator, or identify one final decision authority while documenting required concurrence.

**Distinguish role from person.** Assign accountability to durable organizational roles such as Head of Claims Domain or Customer Profile Product Owner, then record incumbents and effective intervals. Personal assignments aid contact and audit, but architecture should survive staff turnover.

Define deputies, absence coverage, succession, vacancies, onboarding, offboarding, and conflict-of-interest handling. A departed employee must not remain the only catalog owner or access approver.

**Separate governance and management.** Governing bodies evaluate stakeholder needs and risk, direct priorities and policies, and monitor performance and conformance. Management plans, builds, operates, and reports within that direction. Organizations may use different formal structures, but the decision layers should be visible.

A governance council that edits every metadata field is micromanaging. A domain team that sets enterprise risk appetite is overreaching. Escalation connects the layers without collapsing them.

**Separate semantic authority and technical custody.** Domain experts define meaning and authoritative assertions. Custodians operate databases, pipelines, backups, access enforcement, and deletion mechanisms. One team may hold both roles, but record them separately.

A cloud platform provider can preserve availability and encryption while knowing nothing about correct customer status. A business owner can define retention purpose but require a records and platform team to implement deletion. Evidence must join both sides.

**Separate product and source accountability.** A source-aligned product may align product and source authority closely. An aggregate or consumer-aligned product owns its definition, derivation, consumer support, and SLOs while upstream domains retain authority for source assertions.

When a derived product finds a defect, it reports evidence upstream. It does not silently edit source history. The product owner decides whether the derived output is fit for its consumers and how to disclose limitations.

**Scope source authority by predicate.** One Party domain might own legal identity, another workflow contact, another risk assessment. Even within one entity, authority varies by attribute, relationship, context, jurisdiction, and time.

Represent source-of-entry, source-of-reference, and source-of-insight roles. Entry proves where an assertion was captured, not that it is true. Reference authority may depend on evidence and effective period. Insight is derived and must retain lineage.

**Distinguish stewardship.** Stewards maintain definitions, rules, metadata, quality monitoring, issue triage, lineage, training, and adoption. They often have deep expertise but act under delegated decision policies. [DARCH-024](../ROADMAP.md) develops these roles further.

Do not make a steward accountable for a source-process defect if they cannot change the process, secure funding, or compel an owner. Give them escalation and defined delegated authority, and measure whether issues lead to action.

**Distinguish producers and consumers.** Producers create or publish data under a contract. Consumers select and use it correctly, obey access and purpose, handle versions, and report issues. Neither role alone defines organizational accountability for every lifecycle decision.

Consumers may own downstream interpretations and harms. A model team cannot blame a technically valid source if it used data outside the documented scope. Shared responsibility needs clear interfaces, not diluted accountability.

**Recognize legal roles.** Laws and contracts may define controller, joint controller, processor, covered entity, business associate, records custodian, statistical authority, fiduciary, or regulated officer. Map these with counsel for the applicable jurisdiction and facts.

Do not assume an internal RACI changes external obligations. A controller may remain accountable when a processor performs work. Joint legal responsibility is not the same as placing two names in one internal “A” cell.

**Build an accountability matrix by decision.** Rows should be decisions or outcomes, not broad assets; columns should be durable roles. Record accountable, decision authority, responsible execution, mandatory concurrence, consultation, notification, evidence owner, and escalation.

RACI can be useful but is often underspecified. Define what R, A, C, and I mean locally, enforce one accountable role per row, and attach authority and response expectations. For high-consequence decisions, use a decision-rights record rather than relying on a letter.

**Match authority to accountability.** Check whether the role can set policy, change source processes, allocate budget, prioritize engineering, approve risk within limits, suspend use, notify consumers, and escalate. If not, either grant authority or assign accountability elsewhere.

Also check competence and information. Authority without domain knowledge or evidence produces arbitrary decisions. Provide stewards, counsel, security, privacy, engineering, consumer, and operational input.

**Fund the obligation.** Ownership requires time, people, tools, training, and support capacity. A part-time owner of hundreds of products cannot review changes, incidents, and consumer needs credibly. Resource planning should reflect data value, complexity, sensitivity, and risk.

NIST CSF 2.0 explicitly connects roles and authorities with resources. Track unfunded responsibilities as risks rather than declaring governance complete.

**Design delegation.** A delegation states delegator, delegate, task or decision, limits, prerequisites, duration, evidence, review, escalation, and revocation. It should be discoverable by affected actors and systems.

Accountability may remain with the delegator even when authority to perform or approve is delegated. Verify legal and policy constraints; some decisions require independence or cannot be delegated. Delegation chains should be finite and auditable.

**Apply segregation of duties.** High-risk actions may require separate requester, approver, executor, and reviewer. Examples include privileged access, deletion, financial corrections, model deployment, retention overrides, and evidence destruction.

Separation should reduce fraud and error without making routine work impossible. Define emergency paths with time-bound access, logging, after-the-fact review, and revocation. Do not let one omnibus owner bypass every control.

**Manage conflicts of interest.** A product owner may favor adoption while privacy limits use; a source team may minimize reported defects; a platform team may optimize cost at the expense of recovery. Declare interests and independent challenge where consequence warrants.

Escalation should name the deciding role and criteria. Consensus is valuable for learning but cannot be the only mechanism when action is time-bound. Record dissent and conditions.

**Assign definition decisions.** Define who approves concept identity, names, definitions, keys, grain, time semantics, value domains, codes, units, constraints, and deprecation. Require affected consumer and domain consultation without giving every consumer veto power.

Version decisions and preserve rationale. A definition can change business behavior while schemas remain constant. Notify and migrate consumers under the product contract.

**Assign quality accountability.** Quality is fitness for use, so source and product roles both matter. The source authority owns prevention and correction within its process; the product owner owns declared objectives and consumer disclosure; consumers own proper use and feedback.

Define who sets thresholds, monitors, triages, funds remediation, accepts temporary exceptions, communicates limitations, and closes issues. ISO 8000-150's roles-and-responsibilities emphasis supports documentary evidence of this operating model.

**Assign access and use decisions.** Access approval is not one decision. Separate entitlement, purpose, legal basis, data minimization, environment, duration, export, onward sharing, and exceptional use. Automate within approved policy while preserving evidence.

The semantic owner may advise need and sensitivity but may not be authorized to determine legal basis or accept security risk. Privacy, security, legal, records, and ethics functions hold their own mandates. Define joint input and one final authority for each question.

**Use accountability for privacy risk.** NIST's [Privacy Framework](https://www.nist.gov/privacy-framework/privacy-framework) connects business drivers, roles, responsibilities, privacy outcomes, and operations. Its [accountability guidance](https://www.nist.gov/privacy-framework/using-privacy-framework-11) describes communication among executives, business/process managers, and implementation personnel.

Privacy accountability includes understanding data-processing ecosystem roles. Providers, controllers, processors, partners, and consumers exchange requirements and evidence through contracts and profiles. Internal ownership remains only one layer.

**Assign protection decisions.** Name accountability for classification, threat assessment, control objectives, access policy, encryption, key management, monitoring, vulnerability response, incident command, notification, recovery, and risk acceptance.

NIST CSF 2.0's Govern function illustrates leadership, role, policy, oversight, and supply-chain concerns. Technical custodians implement controls; leadership remains accountable for organizational risk within governance structures.

**Assign lifecycle decisions.** Creation, collection, acquisition, publication, change, retention, archive, legal hold, deletion, withdrawal, and retirement need decision owners. Ownership often disappears at the end of a project even though data remains accessible.

Define trigger, evidence, approvals, execution, verification, exceptions, and consumer communication for each transition. A retention owner sets authorized policy; custodians execute; records and legal roles govern holds; product owners migrate consumers.

**Assign incident roles before incidents.** Define detection, triage, containment, source correction, consumer notification, legal and regulatory assessment, public communication, recovery, evidence preservation, and lessons learned. Name incident commander and domain-specific decision authorities.

A data-quality incident can become security, privacy, financial, safety, or reputational harm. Escalation criteria should depend on consequence and scope, not which team first saw the alert.

**Create decision records.** Capture question, scope, options, constraints, consulted evidence, decision, approver authority, rationale, dissent, conditions, expiry or review, implementation, validation, and outcome. Link exact model, policy, product, and code versions.

Do not record protected personal deliberation unnecessarily. Preserve enough evidence for accountability while applying access, minimization, retention, and legal privilege. Meeting attendance does not prove approval.

W3C [PROV-O](https://www.w3.org/TR/prov-o/) distinguishes entities, activities, agents, attribution, association, and delegation. Those constructs can express who influenced or performed an activity, but provenance attribution is not by itself organizational accountability or legal responsibility.

**Use catalogs as routing mechanisms.** W3C [DCAT 3](https://www.w3.org/TR/vocab-dcat-3/) includes publisher, creator, contact, rights, access, version, and catalog-record concepts. A catalog can route consumers to accountable roles and product metadata.

Avoid one free-text `owner` field. Store role identity, organization, scope, decision rights, contact, delegate, effective interval, review date, escalation, and links to policy and product. Validate stale or vacant assignments.

**Govern exceptions.** An exception record names requirement, exact scope, reason, evidence, risk, affected people and consumers, accountable approver, compensating controls, start, expiry, monitoring, remediation, and closure proof.

Exceptions without expiry become shadow policy. Repeated exceptions reveal an infeasible standard, missing platform capability, underfunded domain, or strategic risk. Governance should analyze patterns, not merely renew tickets.

**Escalate by consequence.** Routine definition disputes can remain in a domain. Cross-domain identity or contract disputes may go to a federated forum. High privacy, security, legal, safety, financial, or mission risks require specialized and executive authority.

Publish service objectives for decisions and escalations. A quality exception awaiting approval for months is an operational failure. Include emergency authority and retrospective review.

**Handle service providers.** Contracts specify processing instructions, controls, service levels, incident duties, audit rights, deletion, portability, subcontractors, and exit. Providers remain accountable for their contractual performance while the organization retains its non-transferable governance and legal obligations.

Verify provider evidence rather than assuming certification covers every use. Maintain an internal accountable sponsor and technical owner. Plan exit before lock-in turns “ownership” into inability to retrieve or delete data.

**Handle federated domains.** Domain teams make local product and semantic decisions; shared governance sets interoperability, protection, evidence, and risk requirements. Every federated policy has an owning authority, domain obligations, enforcement mechanism, exception path, and feedback loop.

Do not centralize all decisions in the name of accountability. Accountability can be distributed by precise scopes. It becomes fragmented only when boundaries and escalation are unclear.

**Handle cross-domain products.** One team is accountable for an aggregate product's consumer outcomes and derivation. Upstream domains remain accountable for source contracts. Shared steering can advise priorities, but final product decisions need one owner.

Record dependency SLOs, quality propagation, incident coordination, change notice, and fallback. The aggregate owner cannot accept source risk on behalf of an upstream authority; it can decide whether to continue serving, disclose limitation, or change derivation.

**Design accountability for models and automation.** Automated decisions need owners for purpose, data, model, rules, validation, deployment, monitoring, human review, incidents, and retirement. “The algorithm decided” is not an accountable role.

Separate model developer, validator, deployer, business decision owner, data product owner, and risk approver where necessary. Record overrides and feedback. Generated decisions remain attributable to organizational processes and agents.

**Test the operating model.** Run scenarios: conflicting definitions, source defect, urgent access, vendor breach, privacy complaint, correction request, failed deletion, schema break, biased model output, lost owner, regional rule change, and product retirement.

Ask who decides, who acts, by when, with which evidence, under what authority, and who escalates. If participants give inconsistent answers, the matrix is not implemented. Exercise systems and contact paths, not just documents.

**Measure accountability outcomes.** Track unowned decisions, stale assignments, time to decision, time to acknowledge and resolve issues, repeated exceptions, consumer notification, quality objectives, access review, deletion verification, incident outcomes, overdue risks, and completed succession.

Interpret carefully. Fast decisions can be reckless; few escalations can indicate clarity or suppression. Review samples for rationale and results. Survey whether producers, consumers, stewards, and custodians know their obligations.

**Audit authority and evidence.** Select material decisions and trace assignment, mandate, consultation, evidence, approval, implementation, monitoring, and outcome. Verify that the approver held authority at that time and that separation and conflict rules were followed.

An owner field populated after an incident does not prove prior accountability. Preserve recorded-time history. Record missing evidence as a finding rather than reconstructing it from memory.

**Govern succession and reorganization.** Assignments have effective intervals and organizational role IDs. Reorganization plans map decisions, assets, products, open risks, incidents, exceptions, contracts, budgets, and consumer relationships to successor roles.

Require explicit acceptance. A renamed team does not automatically understand or fund inherited obligations. During transition, state who has final authority and when the transfer becomes effective.

**Retire accountability deliberately.** An accountability assignment ends only when the data or product is retired, obligations transfer, or the decision scope ceases. Archives, backups, legal holds, models, reports, and derived products can outlive active service.

Record successor, retained evidence, access, protection, support, deletion, and review. A catalog's `retired` status should not orphan historical requests or incidents.

**Treat ambiguity as a governance defect.** If no role can accept a decision, escalate rather than assigning the nearest engineer. If two authorities conflict, preserve both positions and invoke the governing rule. If authority is absent, leadership must create it or accept the risk explicitly.

The durable test is simple: when a consequential question arises, can the organization identify who may decide, what they must consider, how action will occur, and what evidence will show the outcome? If not, ownership is ceremonial.

## Definitions and Notation

Let `Q` be a class of data decisions. An accountability assignment is:

`A(Q) = (role, scope, authority, obligations, resources, evidence, escalation, interval)`

Require exactly one final accountable role for each `(Q, scope, interval)`. Several responsible, consulted, concurring, or informed roles may exist. Overlapping final authority must be resolved by partition or an explicit adjudicator.

Let `CanDecide(role,q,t)` mean the role has mandate at time `t`, `Knows(role,q,t)` means necessary information and competence are available, and `CanAct(role,q,t)` means resources and mechanisms exist. A credible assignment needs all three for its declared decision class; a catalog label alone establishes none.

Represent delegation as `G = (delegator, delegate, duty, authority_limit, evidence, start, end, oversight, revoke)`. Delegation can transfer execution or bounded authority. Whether legal or organizational accountability transfers is a separate policy question.

Let a decision record be `D = (q, O, C, E, d, a, r, K, v)`, where `O` is options, `C` constraints, `E` evidence, `d` decision, `a` approving authority, `r` rationale, `K` conditions, and `v` review and outcome verification.

An accountability coverage audit constructs required decision scopes `Q*` and active assignments `A*`, then reports missing, overlapping, expired, vacant, under-authorized, under-resourced, or untested assignments. Coverage is evidence of assignment, not proof of good outcomes.

## Mechanisms, Invariants, or Proof Structure

Use ten gates for every material accountability assignment.

**1. Decision gate.** Name the decision or outcome, consequence, frequency, deadline, exact data/product scope, and stakeholders.

**2. Role gate.** Assign one durable accountable organizational role and current incumbent with effective interval, deputies, succession, and conflict handling.

**3. Authority gate.** Verify mandate, limits, independence, legal/policy basis, required concurrence, and escalation.

**4. Capability gate.** Provide competence, information, capacity, budget, tools, access, and operational support proportionate to risk.

**5. Responsibility gate.** Assign execution, stewardship, custody, production, consultation, notification, evidence, and consumer duties without diluting accountability.

**6. Protection gate.** Map legal and ecosystem roles; enforce security, privacy, purpose, records, safety, ethics, and segregation obligations.

**7. Evidence gate.** Preserve assignment, decision, rationale, delegation, implementation, exception, monitoring, review, outcome, and limitation records.

**8. Escalation gate.** Define conflicts, thresholds, service objectives, emergency authority, appeals, dissent, and governing-body paths.

**9. Exercise gate.** Test representative definition, quality, access, use, incident, correction, vendor, absence, reorganization, and retirement scenarios.

**10. Lifecycle gate.** Review assignments, resources, results, transfers, vacancies, exceptions, successors, archives, and closure continuously.

The executable example checks four narrow assignment failures: no accountable role, missing decision authority, overlapping accountability, and absent evidence obligations.

<!-- bijux-verify: {"id":"data-accountability-integrity","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"assignments=4\nvalid=0\nfindings=catalog:overlapping-accountability,consent:missing-evidence-duty,customer:missing-accountable-role,payments:missing-decision-authority\nready=false\n","stderr":""}} -->
```python
assignments = (
    {"id": "customer", "accountable_roles": 0, "decision_authority": True, "evidence_duty": True},
    {"id": "payments", "accountable_roles": 1, "decision_authority": False, "evidence_duty": True},
    {"id": "catalog", "accountable_roles": 2, "decision_authority": True, "evidence_duty": True},
    {"id": "consent", "accountable_roles": 1, "decision_authority": True, "evidence_duty": False},
)

findings = []
valid = 0
for assignment in assignments:
    local = []
    if assignment["accountable_roles"] == 0:
        local.append("missing-accountable-role")
    if assignment["accountable_roles"] > 1:
        local.append("overlapping-accountability")
    if not assignment["decision_authority"]:
        local.append("missing-decision-authority")
    if not assignment["evidence_duty"]:
        local.append("missing-evidence-duty")
    if local:
        findings.extend(f"{assignment['id']}:{finding}" for finding in local)
    else:
        valid += 1

print(f"assignments={len(assignments)}")
print(f"valid={valid}")
print("findings=" + ",".join(sorted(findings)))
print(f"ready={str(valid == len(assignments)).lower()}")
```

The checker validates four declared assignment predicates only. It does not prove lawful authority, competence, adequate resources, correct decisions, implemented responsibility, protection, source truth, vendor performance, incident readiness, succession, or outcomes. Those require organizational mandates, legal and risk review, operational exercises, decision samples, evidence audits, and governing oversight.

## Alternatives and Trade-Offs

**Central versus domain accountability.** Central authority improves uniformity and enterprise risk oversight but can be distant and slow. Domain accountability improves context and action but needs federated rules and escalation. Split decisions by scope rather than ideology.

**Role versus named-person assignment.** Roles survive turnover and express mandate; named people improve routing and personal clarity. Maintain both with effective intervals, deputies, and succession.

**One broad owner versus decision-specific owners.** One owner simplifies catalogs but creates impossible breadth. Decision-specific ownership is accurate but more complex. Use product/domain summaries that link to an explicit decision matrix.

**Consensus versus final authority.** Consensus builds shared understanding but can delay urgent action. Final authority resolves deadlock but may miss expertise. Require consultation or concurrence where justified and name the final decision role.

**Manual versus policy-automated approval.** Manual review handles nuance but scales poorly. Automation improves speed and consistency within explicit rules. Preserve owner authority over policy, exceptions, and monitoring.

**Embedded versus independent control roles.** Embedded experts understand context and flow; independent roles strengthen challenge and segregation. Combine embedded support with independent oversight for high-consequence decisions.

**Permanent versus time-bound delegation.** Permanent delegation reduces repeated overhead but can drift beyond competence or mandate. Time-bound delegation improves review at administrative cost. Match duration to risk and organizational stability.

**Rich decision evidence versus minimization.** Detailed records improve audit and learning but can expose sensitive facts, legal strategy, or personal data. Preserve necessary rationale and provenance with access, privilege, and retention controls.

## Failure Modes and Misconceptions

1. **Ownership means property.** Internal data ownership is an accountability metaphor unless law or contract says otherwise.
2. **One executive can own all enterprise data.** Governance leadership can be accountable for the framework while decisions remain distributed.
3. **A team mailbox is an accountable role.** It lacks clear mandate, incumbent, and consequence unless formally defined.
4. **Two accountable owners improve collaboration.** They often make final authority ambiguous.
5. **Responsibility and accountability are interchangeable.** Work can be delegated while answerability remains.
6. **The steward owns every quality outcome.** Source-process authority and product decisions may lie elsewhere.
7. **The database administrator owns the data.** Custody does not establish semantics, lawful use, or business authority.
8. **The producer owns every downstream outcome.** Consumers own their interpretation and use under the contract.
9. **A data owner can approve any access.** Purpose, legal, privacy, security, records, and ethics mandates constrain authority.
10. **An internal owner is the legal controller.** Legal roles depend on governing law and actual processing facts.
11. **Outsourcing transfers accountability.** Many governance and legal duties remain with the organization.
12. **A completed RACI proves implementation.** Participants must understand, exercise, and evidence the roles.
13. **Authority without budget is enough.** Unresourced accountability is ceremonial.
14. **Meeting attendance proves approval.** Decisions need explicit authority, rationale, scope, and recorded outcome.
15. **Exceptions are harmless temporary records.** Without expiry and remediation they become shadow policy.
16. **A reorganization automatically transfers ownership.** Successors must accept decisions, risks, products, and evidence.
17. **More catalog owner fields mean stronger governance.** Outcomes, issue resolution, evidence, and assurance matter.

## Worked Examples

### Example 1

A customer table names the CDO as owner. Definition disputes still wait months. Decision decomposition assigns identity semantics to Party leadership, product commitments to a product owner, and enterprise governance to the CDO, each with resources and escalation.

### Example 2

A steward detects invalid supplier tax identifiers but cannot change onboarding. The Supplier-domain owner funds validation at entry, while the steward owns monitoring and issue coordination. Closure evidence links source correction to downstream reconciliation.

### Example 3

A platform team approves every data access because it controls storage. The model separates policy enforcement custody from purpose, entitlement, privacy, and security decisions. Automated grants require all scoped approvals and expiry.

### Example 4

Two vice presidents are both marked accountable for Revenue. Disputes persist over refunds. The scope splits: Finance owns recognized-revenue policy; Commerce owns order and refund assertions; a Revenue product owner owns the published derivation and consumer SLO.

### Example 5

A vendor hosts a sensitive archive and holds operational encryption duties. The organization retains a controller and records authority, internal sponsor, product accountability, audit rights, deletion evidence, incident obligations, and an exit plan.

### Example 6

An urgent fraud investigation requests broad data. Emergency authority permits bounded access for a declared purpose and duration with independent approval, logging, minimization, notification, expiry, and retrospective review.

### Example 7

A machine-learning model denies applications. Accountability is divided across business decision owner, model owner, training-data product owners, validation, deployment custody, privacy/security, appeal operations, and executive risk governance, with one final authority per decision.

### Example 8

A domain owner delegates schema approval during leave. The delegation names versions, compatible changes, risk limits, evidence, dates, and escalation. A breaking change remains outside the delegate's authority and escalates.

### Example 9

A reorganization dissolves the Loyalty team. Transfer inventory covers products, consumers, definitions, open defects, access, retention, contracts, incidents, budget, and on-call. The successor explicitly accepts obligations before the old assignment ends.

### Example 10

A product retires while backups and annual reports still contain its data. Active service ownership ends only after consumers migrate; archive, records, security, deletion, and historical support obligations transfer to named successor roles.

## Cross-Program Connections

- **Business and enterprise architecture:** governance, capabilities, operating models, decision rights, organization, value, and outcomes locate accountability.
- **Data engineering:** producers, pipelines, quality checks, lineage, corrections, backfills, and serving operations implement assigned duties.
- **Platform engineering:** identity, policy enforcement, catalogs, observability, evidence, workflows, and recovery support accountable domains.
- **Security and privacy:** risk ownership, legal roles, access, purpose, controls, incidents, notification, and assurance constrain decision authority.
- **Product management:** consumer value, roadmaps, contracts, SLOs, support, change, cost, and retirement define product accountability.
- **Software engineering:** code ownership, review, deployment, service operation, incident response, and dependency contracts provide implementation analogies.
- **Records and legal practice:** retention, holds, discovery, privilege, controller/processor relationships, and regulatory evidence shape lifecycle roles.
- **Systems engineering:** responsibility assignment, configuration authority, hazard acceptance, verification independence, traceability, and lifecycle supply assurance patterns.

## References

1. ISO/IEC, *38505-1:2026 Information technology—Governance of data—Part 1*, 2026. <https://www.iso.org/standard/87195.html>
2. ISO, *8000-150:2022 Data quality—Part 150: Data quality management: Roles and responsibilities*, 2022. <https://www.iso.org/standard/80753.html>
3. Pascoe, C., Quinn, S., and Scarfone, K., *The NIST Cybersecurity Framework (CSF) 2.0*, NIST CSWP 29, 2024. <https://www.nist.gov/publications/nist-cybersecurity-framework-csf-20>
4. NIST, *Privacy Framework: A Tool for Improving Privacy through Enterprise Risk Management*, Version 1.0, 2020. <https://www.nist.gov/privacy-framework/privacy-framework>
5. European Parliament and Council, *Regulation (EU) 2016/679 (General Data Protection Regulation)*, 2016. <https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679>
6. W3C, *PROV-O: The PROV Ontology*, W3C Recommendation, 2013. <https://www.w3.org/TR/prov-o/>
7. W3C, *Data Catalog Vocabulary (DCAT)—Version 3*, W3C Recommendation, 2024. <https://www.w3.org/TR/vocab-dcat-3/>
8. U.S. Office of Management and Budget, *M-19-23 Phase 1 Implementation of the Foundations for Evidence-Based Policymaking Act of 2018*, 2019. <https://www.whitehouse.gov/wp-content/uploads/2019/07/M-19-23.pdf>

## Exercises

### Exercise 1

Create an accountability matrix for customer identity definitions, source corrections, product contracts, quality exceptions, access, privacy purpose, incidents, retention, and retirement. Explain every final authority.

### Exercise 2

Analyze a case where the platform team is listed as owner of all warehouse data. Reassign semantic, product, custody, quality, security, privacy, consumer, and lifecycle decisions while preserving operational clarity.

### Exercise 3

Design a delegation and succession policy for domain and product owners. Include absence, limits, competence, evidence, emergency authority, revocation, vacancy, transfer, and review.

### Exercise 4

Plan an accountability exercise for a critical data-quality incident that also creates privacy and financial risk. Define scenario, roles, decisions, timing, evidence, escalation, recovery, and learning.

### Exercise 5

Design an accountability assurance dashboard that avoids vanity metrics. Include coverage, authority, resources, decision evidence, issue outcomes, exceptions, incidents, consumer results, and audit sampling.

## Answers to the Exercises

### Answer 1

Assign Party-domain leadership accountability for identity concept, key, authoritative sources, and corrections. A Customer Profile product owner is accountable for contract, quality objectives, support, versioning, and retirement. Source-process owners are accountable for preventing and correcting defects in their workflows. Privacy and legal roles decide lawful purpose and controller obligations; security decides control and risk matters within mandate; records authority decides retention and holds; custodians execute access and deletion.

One final role exists per decision scope, with mandatory consultation or concurrence where needed. Document subject, predicate, product, jurisdiction, purpose, time, risk limit, outcome, authority, resources, evidence, and escalation. Consumers own correct use and migration. Incidents name one commander while domain, product, privacy, security, legal, finance, communication, and operations retain scoped decisions. Retirement transfers archive and historical obligations explicitly.

### Answer 2

The platform team owns warehouse service reliability, policy-enforcement mechanisms, storage, compute, backup, recovery, and technical support. It does not automatically define Customer, Revenue, or Claim semantics. Domain roles own source definitions, authoritative assertions, and corrections. Product owners own published derivations, consumer contracts, SLOs, quality objectives, and change communication.

Stewards maintain metadata and coordinate issues; source owners fund prevention; consumers own use; security/privacy/legal/records roles provide or hold mandated decisions. Implement a catalog decision matrix, automated policy paths, and escalation. Direct writes require domain authority. Operational incidents begin with the platform when infrastructure fails and with products/domains when data meaning fails, with one cross-functional commander for combined events. Preserve lineage so custody never masquerades as source authority.

### Answer 3

Assign durable roles and current incumbents with effective intervals. A delegation names delegator, delegate, exact decisions or duties, authority and risk limits, required knowledge, start/end, evidence, oversight, escalation, and revocation. Breaking contracts, high risk acceptance, legal obligations, and privileged actions may require higher or independent authority. Emergency delegation is time-bound, logged, least-privileged, and reviewed afterward.

Each role has trained deputies and absence activation. Vacancy triggers escalation to a named superior rather than an unmonitored mailbox. Reorganization transfer inventories products, decisions, open risks, incidents, exceptions, access, contracts, budget, on-call, archives, and consumers. Successors explicitly accept, and historical records retain prior incumbents. Review assignments periodically and after incidents, scope changes, or transfers.

### Answer 4

Simulate a source defect that overstates balances, affects a published product, exposes protected attributes in an exception file, and changes financial reports. Trigger detection and require triage, severity, containment, source correction, consumer notice, access revocation, privacy and legal assessment, financial restatement, recovery, and executive escalation under deadlines.

Observe whether one incident commander coordinates while source, product, platform, security, privacy, legal, finance, records, and communications make their scoped decisions. Capture timestamps, evidence, approvals, dissent, actions, validation, and unresolved risk. Test off-hours contacts and unavailable owners. Afterward compare expected and actual authority, time, communication, and outcomes; fund remediation; revise playbooks and contracts; and retest rather than counting attendance as readiness.

### Answer 5

Show required decision scopes with active, singular, non-vacant assignments and effective dates. Flag overlapping, expired, under-authorized, unresourced, and unexercised roles. Measure decision and escalation latency, overdue reviews, open and repeated exceptions, quality-issue acknowledgement and resolution, consumer notification, access review, deletion verification, incident containment and recovery, successor acceptance, and product-retirement closure.

Add outcome measures such as quality-objective attainment, contract breakage, consumer satisfaction, recurrence, policy conformance, and residual risk. Sample decisions to trace mandate, evidence, rationale, implementation, and result. Report missing or inaccessible evidence. Segment by consequence rather than rewarding raw owner-field coverage. Pair metrics with narratives and independent assurance; few incidents or escalations can mean strong control or weak detection.
