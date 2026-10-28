---
module_id: DARCH-059
program: Data Architecture Engineering
level: 2
module_number: 59
title: Governance of Shared Data
status: complete
last_verified: 2026-09-03
---

# Governance of Shared Data

## One-Page Review

### Governing question

How should an enterprise assign authority, accountability, policy, controls, funding, evidence, and lifecycle duties for shared data so that reuse creates value without obscuring risk or leaving cross-domain decisions ownerless?

### Essential definitions

- **Data governance** is the system by which authority directs, constrains, oversees, and accounts for decisions about data and its use.
- **Data management** is the execution of practices that acquire, describe, maintain, protect, deliver, improve, retain, and dispose of data under governance.
- **Shared data** is data whose meaning, quality, availability, protection, or evolution affects decisions in more than one accountable boundary.
- A **data owner** is the individual accountable for a defined data asset or domain and its consequential decisions; ownership is not legal possession.
- A **data steward** performs delegated semantic, quality, metadata, issue, and lifecycle work within explicit authority.
- A **data custodian** operates technical controls and services without inheriting semantic or business authority merely by hosting data.
- A **consumer owner** is accountable for a consumer's interpretation, local controls, fitness assessment, and response to upstream change.
- A **decision right** states which role may propose, approve, execute, challenge, escalate, or review a named class of decision.
- A **policy** states required or prohibited outcomes and conditions; a **standard** narrows acceptable implementation; a **control** supplies a mechanism and evidence.
- An **exception** is a bounded, approved departure from a policy or standard with rationale, risk owner, compensating controls, expiry, and closure criteria.
- A **critical data element** is a data element whose failure can materially harm a declared decision, obligation, service, person, or mission.
- **Accountability evidence** connects a decision, authorized role, applied control, observed outcome, exception, and corrective action over time.

### Central model, mechanism, or theorem

Represent governance as:

`G = (outcomes, scope, decisions, rights, owners, policies, standards, controls, services, consumers, evidence, funding, escalation, lifecycle)`

Governance is fit only when every consequential decision class has an accountable owner, affected parties can be heard, authority and escalation are explicit, required controls produce reviewable evidence, exceptions expire or close, and observed outcomes feed correction. Central governance should own enterprise-wide risk direction and cross-boundary rules; domain owners should decide within their semantic authority; platforms should enforce declared controls without becoming accidental owners of meaning.

### Critical invariants

- Governance begins with business, mission, legal, ethical, security, privacy, and reliability outcomes rather than a tool or committee chart.
- Each shared asset, critical element, policy, control, issue, exception, service, and retirement decision has one named accountable owner.
- Decision rights distinguish proposal, approval, execution, consultation, challenge, escalation, assurance, and informed parties.
- Semantic owner, source owner, product owner, steward, custodian, control owner, consumer owner, and risk specialist remain distinct roles.
- Policies expose scope, authority, rationale, obligations, prohibitions, effective time, precedence, evidence, exception path, review, and retirement.
- Quality is evaluated against named uses, populations, dimensions, rules, thresholds, consequences, and consumer decisions.
- Access permission does not establish purpose fitness, ethical acceptability, semantic compatibility, or lawful reuse.
- Exceptions are visible, risk-accepted, compensated, monitored, time-bounded, and closed; repeated exceptions trigger policy or architecture review.
- Consumers own local interpretation, transformations, caches, derived data, decisions, and timely adoption of governed changes.
- Governance evidence measures control and decision outcomes, not only meetings, catalog entries, training, or policy publication.
- Federated governance preserves common invariants while allowing domains to choose local mechanisms within explicit bounds.
- Retirement closes data, products, policies, controls, issues, exceptions, access, contracts, evidence, retention, and recovery obligations.

### Common failures

Common failures are equating governance with a council; naming a department instead of an accountable person; making the hosting platform the data owner; assigning one steward every responsibility but no authority; using RACI without naming decisions; requiring central approval for every low-risk change; letting domains redefine shared identifiers incompatibly; publishing policies without controls or evidence; declaring quality “high” without a use; measuring metadata population instead of decision improvement; granting access without purpose and retention; leaving exceptions permanent; excluding consumers from change decisions; funding shared data as temporary overhead; allowing committees to accept risk they do not own; and retiring services while copies, contracts, incidents, or legal duties remain.

### Compact example

Three proposed shared-data changes pass through an explicit approval policy. A personal, high-risk customer standard has data-owner, consumer-owner, privacy, and security approval; a shared product label has its required owners; a supplier bank-routing change lacks consumer-owner approval and relies on an expired exception. The first two are ready, the third is blocked, and no decision is ownerless. This proves only the small routing rule, not the wisdom or legal sufficiency of the approvals.

### Connections

[DARCH-023](023-data-ownership-and-accountability.md), [DARCH-024](024-stewardship-roles.md), [DARCH-026](026-data-products-and-service-expectations.md), [DARCH-027](027-producer-and-consumer-contracts.md), [DARCH-051](051-master-data-and-golden-records.md), [DARCH-057](057-shared-code-sets-and-controlled-vocabularies.md), and [DARCH-058](058-master-data-change-propagation.md) establish the governed assets and operational boundaries. [DARCH-060](../ROADMAP.md) next assembles an MDM capability without centralizing every domain.

## Governing Question

Shared data creates dependencies that no single delivery team can resolve alone. A customer identifier can be authoritative in one domain, enriched in another, screened by a third, embedded in dozens of products, and constrained by privacy, security, records, contract, and jurisdictional duties. If no one owns the cross-boundary decisions, inconsistency becomes structural.

The governing question is which allocation of authority and evidence lets an enterprise make those decisions quickly at the right level, protect legitimate interests, fund shared obligations, learn from outcomes, and close duties across the full data lifecycle.

## Why This Matters

NIST's [Cybersecurity Framework 2.0](https://www.nist.gov/publications/nist-cybersecurity-framework-csf-20) makes Govern a distinct function involving organizational context, risk strategy, roles, policy, oversight, and supply-chain risk. The [NIST Privacy Framework 1.0](https://www.nist.gov/privacy-framework/privacy-framework) treats privacy as enterprise risk management rather than a late access-control check. These frameworks are not data-governance operating models, but they demonstrate why direction, roles, risk tolerances, controls, and feedback must connect.

The U.S. [Federal Data Strategy Practices](https://strategy.data.gov/practices/) call for sufficient authority, roles, structures, policies, and resources to govern strategic data and protect confidentiality and privacy. The UK government's [Data Ownership Model](https://www.gov.uk/government/publications/data-ownership-in-government/data-ownership-model) treats ownership as lifecycle accountability rather than possession and distinguishes owners, stewards, custodians, and shared-data responsibilities. Its [Data Sharing Governance Framework](https://www.gov.uk/data-ethics-guidance/data-sharing-governance-framework) emphasizes strategic alignment of sharing systems and processes. Local enterprises must adapt these ideas to their legal and organizational context.

The W3C [Data Quality Vocabulary](https://www.w3.org/TR/vocab-dqv/) supports explicit quality dimensions, metrics, measurements, policies, annotations, and feedback while noting that fitness depends on perspective. The W3C [ODRL Information Model 2.2](https://www.w3.org/TR/odrl-model/) models permissions, prohibitions, duties, constraints, parties, assets, and conflict strategies; machine-readable policy still requires an agreed profile and enforcement semantics. W3C [PROV-O](https://www.w3.org/TR/2013/REC-prov-o-20130430/) provides a vocabulary for entities, activities, agents, and qualified provenance.

The OECD [Recommendation on Enhancing Access to and Sharing of Data](https://legalinstruments.oecd.org/en/instruments/OECD-LEGAL-0463) frames sharing as a risk-benefit and rights problem across the data value cycle. NIST [SP 800-160 Volume 1 Revision 1](https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final) frames trustworthiness as a lifecycle engineering concern. Governance must therefore join value, rights, risk, engineering, operation, evidence, and disposal rather than optimize one in isolation.

## Prerequisites and Retrieval

You should understand data domains, ownership, stewardship, data products, contracts, master and reference data, quality, metadata, lineage, access control, privacy, security, records, legal obligations, service management, risk, organizational design, economics, audit, and lifecycle engineering.

Retrieve governance, management, ownership, accountability, responsibility, authority, delegation, stewardship, custody, decision right, policy, standard, procedure, control objective, control, evidence, assurance, risk acceptance, exception, waiver, compensating control, critical data asset, critical data element, data product, purpose, consumer obligation, council, forum, escalation, issue, remediation, maturity, and dependency closure.

As a retrieval test, inspect “the governance board owns customer data.” Ask which person is accountable, which customer boundary and uses, which decisions the board may make, what domain authority remains, which consumers and risk specialists participate, how policy is enforced, what evidence is reviewed, who funds remediation, how exceptions expire, and who accepts consequences. A meeting invitation is not an operating model.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish governance, management, ownership, stewardship, custody, product operation, risk oversight, and assurance;
2. define shared-data scope from decisions, dependencies, outcomes, rights, risks, and lifecycle obligations;
3. allocate proposal, approval, execution, challenge, escalation, and review rights to named accountable roles;
4. design a federated operating model that preserves enterprise invariants without centralizing domain meaning;
5. translate policy into standards, controls, evidence, exception workflows, and corrective action;
6. govern quality, metadata, lineage, contracts, access, privacy, security, licenses, retention, and deletion together;
7. assign producer, platform, consumer, and third-party responsibilities for shared copies and derived data;
8. fund and prioritize shared-data work using criticality, dependency, consequence, and measurable value;
9. evaluate governance through decision speed, control effectiveness, issue closure, adoption, trust, and harm; and
10. migrate or retire governance structures only after authority and dependency closure.

## Core Exposition

**Begin with outcomes and affected people.** Identify the decisions, services, obligations, rights, benefits, and harms that depend on shared data.

Governance exists to improve those outcomes under legitimate constraints. A catalog, council, or policy library is an instrument, not the purpose.

**Define why the data is shared.** Name the producers, consumers, populations, decisions, transformations, jurisdictions, and time horizons.

Data reused by two reports is not necessarily enterprise master data. Data used by one small service can still require strong governance when consequences are severe.

**Distinguish governance from management.** Governance sets direction, delegates authority, constrains choices, oversees results, and holds decision makers accountable.

Management implements processes and services within that direction. Blurring them lets governing bodies micromanage while operational failures remain ownerless.

**Distinguish ownership from possession.** A database administrator, cloud provider, platform team, or recipient can hold a copy without owning its business meaning.

Ownership is accountable decision authority for a defined boundary. Legal property, privacy controllership, records custody, and contractual rights can allocate other duties and must be analyzed separately.

**Name the asset boundary.** Define the domain, entities, attributes, relationships, identifiers, code sets, metadata, interfaces, histories, and derived products in scope.

“Customer data” is too broad when identity, contact preference, credit status, service interaction, and analytics segments have different authorities.

**Identify shared-data decisions.** Inventory decisions about definitions, identifiers, sources, matching, survivorship, quality, access, permitted use, change, service levels, retention, correction, funding, and retirement.

Roles become concrete only when tied to decisions. A generic owner list leaves collision points unresolved.

**Assign one accountable owner per decision class.** Accountability means answerability for outcome and authority to decide or escalate.

Several people can contribute or execute. A committee can deliberate, but a named person must accept or reject the consequence within delegated authority.

**Separate semantic ownership.** The semantic owner decides meaning, scope, keys, relationships, state transitions, and authoritative-source policy.

Technical hosting does not confer those rights. The semantic owner must still consult consumers whose decisions reveal hidden ambiguity.

**Separate source ownership.** A source owner is accountable for capture at an operational boundary, including validation, provenance, correction, and timely publication.

It may not own enterprise-wide consolidation or every downstream interpretation. Contracts must show where responsibility changes.

**Separate product ownership.** A shared-data product owner is accountable for discoverability, access, service, support, roadmap, adoption, and product economics.

Product ownership does not silently supersede semantic or legal authority. One person can hold several roles, but the decisions remain distinguishable.

**Separate stewardship.** Stewards can maintain definitions, rules, mappings, metadata, issues, review queues, and change communications under delegated authority.

Do not make stewards accountable for outcomes when they lack budget, enforcement rights, or escalation access.

**Separate custody and platform operation.** Custodians implement storage, encryption, access, backup, monitoring, retention jobs, and infrastructure controls.

They own reliable execution within their service boundary, not whether a customer is the same person or a supplier may be approved.

**Name control owners.** A control owner defines how a control objective is achieved, tested, evidenced, corrected, and retired.

Control execution can be automated by a platform or performed by a domain. Failed automation still has an accountable human owner.

**Name consumer owners.** A consumer owner is accountable for declared purpose, local mapping, transformation, cache, derived data, quality assessment, access, change adoption, decisions, and disposal.

Publishing governed data does not transfer all risk to the producer. Consumers can misuse accurate data or retain stale copies.

**Engage risk specialists as decision participants.** Privacy, security, legal, records, ethics, accessibility, finance, safety, compliance, and audit roles bring distinct authority and expertise.

They should not become a generic veto queue. Define which consequences trigger consultation, approval, challenge, or independent assurance.

**Use decision rights, not role labels alone.** For each decision, identify proposer, approver, executor, mandatory consultees, challenger, escalation owner, evidence reviewer, and informed parties.

RACI can summarize participation but often obscures veto, challenge, and escalation. Record actual authority and response time.

**Define delegation.** An enterprise owner can delegate routine definition and quality decisions to domain stewards within thresholds.

Delegation states scope, limits, evidence, duration, substitution, escalation, and revocation. It does not erase the delegating owner's accountability.

**Design forums around collision points.** A domain forum can resolve local semantics. A cross-domain forum can resolve shared identity, vocabulary, contracts, or investment conflicts.

An executive body should address risk appetite, unresolved trade-offs, funding, and accountability—not review field names.

**Give every forum a charter.** State purpose, authority source, decision types, membership by role, quorum, conflicts of interest, input, evidence, service time, records, appeal, and sunset.

A forum that can discuss but not decide or escalate increases delay without reducing risk.

**Choose centralization by decision, not organization chart.** Centralize enterprise risk direction, common identifiers, required controls, cross-domain arbitration, and shared investment where coordination value exceeds cost.

Keep domain semantics and routine execution close to knowledgeable owners. Federation is explicit allocation, not absence of governance.

**Define non-negotiable invariants.** Examples include stable identity, accountable ownership, purpose recording, least privilege, lineage, temporal history, audit evidence, retention, and tested recovery.

Domains can choose tools and workflows that prove these invariants. Platform paved roads can reduce cost without becoming mandatory semantic monopolies.

**Use tiers proportional to consequence.** Classify assets and elements by decision criticality, sensitivity, legal duty, dependency fan-out, change rate, recoverability, and harm.

Higher tiers can require more independent review, tighter freshness, stronger lineage, formal change windows, or recovery testing. Do not govern every column identically.

**Identify critical data elements through decisions.** Trace which elements can alter material decisions or obligations.

A field is not critical because an executive recognizes its name. Record the decision path, failure mode, threshold, population, owner, and evidence.

**Build a policy hierarchy.** Enterprise policy states required outcomes and risk boundaries. Standards specify acceptable patterns; procedures guide execution; controls implement and evidence requirements.

Local policies can specialize within authority. Define precedence and conflict resolution across enterprise, jurisdiction, contract, domain, and consumer rules.

**Make policies decision-ready.** Include stable identity, authority, rationale, scope, definitions, required and prohibited outcomes, roles, conditions, effective time, evidence, exceptions, review, supersession, and retirement.

Vague policy creates inconsistent enforcement. Excessive implementation detail makes it obsolete when technology changes.

**Distinguish policy text from executable policy.** Machine-readable rules can encode permissions, prohibitions, obligations, constraints, and duties.

An expression language does not supply legal interpretation, complete context, conflict resolution, enforcement placement, or human judgment. Publish a governed profile and test semantics.

**Place controls at effective boundaries.** Prevent invalid creation near the authoritative write; enforce access at every serving path; validate propagation at interfaces; verify disposal in copies and backups.

A central dashboard that observes failure after consequential use is detection, not prevention.

**Specify control evidence.** Define what event, log, attestation, sample, test, reconciliation, approval, or outcome demonstrates operation.

Evidence includes subject, object, policy version, control version, time, result, actor, source, integrity, retention, reviewer, and limitations.

**Do not mistake automation for governance.** Automated schema checks, access decisions, quality rules, and retention jobs improve consistency and scale.

Humans still own rule selection, false outcomes, exceptions, corrections, changed context, and consequences.

**Design exceptions as governed objects.** An exception records policy and clause, affected assets and consumers, rationale, risk, owner, approval, compensating controls, evidence, start, expiry, review, and closure.

An email saying “temporarily approved” is neither bounded nor discoverable.

**Require exception expiry.** At expiry, close, renew through fresh risk review, or block the nonconforming use.

Automatic renewal hides permanent architecture debt. Repeated similar exceptions indicate an unrealistic policy, missing capability, or neglected investment.

**Keep risk acceptance with the risk owner.** A governance office can validate process and advise; it should not accept operational, legal, privacy, financial, or safety consequences outside its authority.

Record residual risk, affected parties, monitoring, escalation, and reconsideration triggers.

**Govern definitions as products.** A term has identity, definition, scope, owner, status, examples, exclusions, synonyms, related models, source, version, and consumers.

Glossary publication does not create agreement. Bind terms to data elements, contracts, rules, decisions, and adoption evidence.

**Govern identifiers and relationships.** Stable identifiers, business keys, merge and split rules, hierarchy semantics, aliases, and temporal validity affect every consumer.

Changes require impact analysis and migration evidence proportional to dependency fan-out.

**Treat reference data and vocabularies separately.** Govern concept authority, code system, value set, labels, mappings, versions, deprecation, and unknown states.

Do not let each consumer privately reinterpret a shared status code while claiming enterprise consistency.

**Govern quality for use.** Define the decision, population, time, quality dimension, rule, measurement method, threshold, consequence, owner, and response.

One dataset can be fit for aggregate planning and unfit for individual eligibility. Quality is not one context-free score.

**Separate rule, metric, threshold, and issue.** A rule evaluates records or aggregates; a metric summarizes results; a threshold triggers a decision; an issue records unacceptable consequence and remediation.

Passing a threshold does not prove truth. Sampling, reference sources, labels, and measurement error need disclosure.

**Publish quality evidence.** Consumers need measurement scope, time, method, exclusions, lineage, freshness, unresolved issues, and confidence.

Producer self-assessment is useful but not the only voice. Consumer feedback and independent assurance can reveal fitness gaps.

**Govern metadata as operational data.** Ownership, classification, contracts, schemas, quality, lineage, service status, policy bindings, and lifecycle states require their own authority and freshness.

A catalog with stale owners and broken links can increase risk by creating false confidence.

**Require minimum discovery metadata by tier.** A critical asset should expose purpose, domain, owner, steward, schema, glossary bindings, source, consumers, quality, classification, access, service, change, retention, and support.

Completeness counts are diagnostic. Verify that people can actually find, understand, obtain, and use the correct asset.

**Govern lineage for decisions.** Capture authoritative source, transformations, mappings, versions, policies, and consumer outputs at the granularity needed for impact and correction.

Column lineage alone may miss identity resolution, manual approval, model inference, or off-platform files.

**Make producer-consumer contracts mutual.** Producers define semantics, quality, service, change, correction, protection, and support. Consumers declare purpose, dependencies, local transformations, adoption duties, incident contact, feedback, and exit.

The contract is an accountable relationship, not only a schema file.

**Govern access and use separately.** Authentication and authorization decide whether a request may reach data. Purpose, ethics, contract, consent, confidentiality, competition, export, and records rules constrain what may be done afterward.

An authorized analyst can still perform a prohibited or harmful use.

**Apply least data and least duration.** Share the minimum fields, population, precision, history, frequency, and retention needed for the declared outcome.

Wide extracts transfer hidden obligations. Prefer purpose-specific views, aggregation, tokenization, clean rooms, or controlled query where appropriate.

**Keep privacy risk contextual.** Identify people, data actions, affected groups, problematic consequences, likelihood, impact, controls, residual risk, and recourse.

Compliance with one rule does not prove that a use is fair, expected, accurate, or harmless.

**Keep security governance integrated.** Classify shared data, model threats, bind identities, minimize privileges, encrypt, log, monitor, respond, and recover.

Security controls should follow every API, event, file, cache, catalog, support tool, dead letter, export, and backup—not only the authoritative store.

**Govern contracts, licenses, and intellectual property.** Record source terms, permitted uses, attribution, geographic and temporal constraints, derivative rights, onward sharing, audit, deletion, and termination.

Open access does not mean ownerless or maintenance-free. Third-party data creates responsibility for the received copy without changing the original publisher's authority.

**Govern retention and deletion end to end.** Map record classes, purposes, legal holds, minimum and maximum periods, systems, derived data, archives, backups, and recipient duties.

Retention is not “keep forever in case.” Deletion evidence must address propagation and restoration paths while preserving legitimate audit where required.

**Govern external sharing as a relationship.** Identify provider, recipient, authority, purpose, legal basis, terms, technical channel, quality, support, onward use, incident handling, correction, return, and exit.

Openness, non-discriminatory access, and conditioned access are different arrangements with different controls.

**Include affected stakeholders.** Data subjects, frontline staff, customers, partners, communities, consumers, and operators can reveal consequences invisible to owners.

Participation does not mean every stakeholder decides every matter. Define how input influences decisions and how dissent or appeal is recorded.

**Govern change as a product lifecycle.** Proposals expose rationale, affected definitions, schemas, rules, policies, consumers, risk, migration, compatibility, effective time, and rollback or correction.

Emergency change can use an accelerated path, but still requires authority, evidence, retrospective review, and closure.

**Make issue management consequential.** An issue records affected asset and decisions, severity, evidence, population, time, owner, containment, remediation, consumer notification, validation, and closure.

Ticket closure is not outcome restoration. Verify corrected data propagated and affected decisions were addressed.

**Escalate based on thresholds.** Escalation can depend on unresolved time, harm, regulatory duty, cross-domain conflict, exception expiry, control failure, or funding block.

Avoid escalation that merely adds more observers. Route to a role with authority to decide or resource the work.

**Fund shared data deliberately.** Shared-data work includes stewardship, source correction, product operation, metadata, controls, support, migrations, consumer adoption, recovery, and retirement.

Chargeback can reveal cost but can also discourage beneficial reuse. Central subsidy can create commons value but weaken demand signals. Choose funding by incentives and accountable outcomes.

**Prioritize by risk-adjusted value.** Combine decision value, harm reduction, affected population, dependency fan-out, obligation, effort, uncertainty, and reversibility.

Do not prioritize solely by executive visibility or issue counts. Preserve capacity for systemic controls and unplanned correction.

**Measure governance throughput carefully.** Decision lead time, exception age, issue closure, change adoption, and access turnaround reveal friction.

Faster is not always better; segment by decision class and verify quality, inclusion, and outcomes. Slow high-risk deliberation can be appropriate while routine decisions should not queue centrally.

**Measure effectiveness, not theater.** Track prevented harm, reduced decision error, improved discovery-to-use, fewer unresolved conflicts, quality fitness, freshness, control reliability, consumer adoption, recovery, and trusted exit.

Meeting count, training completion, policy count, owner coverage, and catalog population are leading or activity measures, not final value.

**Audit the decision trail.** Preserve proposal, evidence, alternatives, participants, declared conflicts, authority, decision, rationale, conditions, dissent, effective time, controls, outcomes, exceptions, and later review.

Auditability supports learning and accountability; it should not encourage collecting unnecessary personal detail.

**Use independent assurance proportionally.** High-consequence controls and governance claims may need reviewers independent of design and operation.

Independence, competence, scope, evidence access, sampling, limitations, findings, and remediation must be explicit. Self-review remains useful but is not independent assurance.

**Assess maturity by capability and outcomes.** Examine whether authority, policy, metadata, quality, protection, services, evidence, funding, learning, and lifecycle closure work across representative decisions.

A numeric maturity level compresses context. Preserve strengths, gaps, consequences, dependencies, and target capabilities behind the score.

**Design for organizational change.** Owners leave, domains split, products merge, regulations change, platforms migrate, and vendors exit.

Use deputies, role directories, succession, periodic attestation, transfer records, and orphan detection so authority does not disappear silently.

**Exercise incident governance.** Define who can contain access, freeze publication, correct authority, notify consumers, accept degraded use, communicate externally, preserve evidence, and resume service.

Incident command does not permanently transfer semantic ownership. Retrospectives should update rules, controls, funding, and architecture.

**Retire governance obligations by closure.** When an asset or product ends, resolve owners, consumers, contracts, policies, exceptions, issues, access, copies, histories, retention, holds, support, monitoring, recovery, and successor authority.

Archive evidence under named custody and revoke obsolete authority. An inactive committee or deleted catalog entry does not prove closure.

## Definitions and Notation

Let `A` be shared data assets, `D` decision classes, `R` roles, `P` policies, `K` controls, `E` evidence records, `X` exceptions, and `C` consumers.

For `d ∈ D`, let `asset(d)` be its scope, `impact(d)` its consequence class, `accountable(d) ∈ R` its accountable owner, `approve(d) ⊆ R` required approvers, and `challenge(d) ⊆ R` authorized challengers.

Define ownership coverage:

`Coverage_D = |{d ∈ D : accountable(d) is named and active}| / |D|`

Coverage measures assignment, not competence, authority, funding, or effective decisions.

For policy `p`, let `scope(p)`, `authority(p)`, `effective(p,t)`, `requires(p)`, `prohibits(p)`, `evidence(p)`, and `exceptions(p)` describe its operative contract.

For control `k`, let `objective(k)`, `mechanism(k)`, `owner(k)`, `frequency(k)`, `result(k,t)`, and `limitations(k)` remain distinct.

For exception `x`, write `policy(x)`, `risk_owner(x)`, `controls(x)`, `start(x)`, `expiry(x)`, `status(x)`, and `closure(x)`. A usable exception at time `t` requires approval, `start(x) ≤ t < expiry(x)`, operating compensating controls, and compatible scope.

For use `u` and quality dimension `q`, let `M(a,u,q,t)` be the measurement of asset `a` under a versioned method at time `t`, and `T(u,q)` the decision threshold. Passing is contextual:

`Fit(a,u,t) = ∧q decision_rule_q(M(a,u,q,t), T(u,q))`

This predicate cannot prove that measurements are unbiased, complete, or sufficient for every use.

Let `Outcome(d,t)` denote observed benefits, harms, service effects, and obligations associated with decisions of class `d`. Governance feedback connects outcome evidence to review of rights, policy, controls, resources, and architecture.

Define governance fitness:

`FitGovernance(G) = Purpose ∧ Scoped ∧ Accountable ∧ Authorized ∧ Participatory ∧ PolicyBound ∧ Controlled ∧ Evidenced ∧ ExceptionBound ∧ ConsumerAware ∧ Funded ∧ Adaptive ∧ Protected ∧ Recoverable ∧ Closed`

This is an assurance framework, not proof that a governance structure is legitimate or effective in every jurisdiction and social context.

## Mechanisms, Invariants, or Proof Structure

**Purpose gate.** Trace shared-data governance to named decisions, value, rights, obligations, risks, affected parties, and prohibited outcomes.

**Scope gate.** Define assets, elements, relationships, copies, derivatives, consumers, jurisdictions, temporal boundaries, and lifecycle obligations.

**Authority gate.** Prove the source and limits of ownership, delegation, approval, challenge, escalation, assurance, and risk acceptance.

**Role-separation gate.** Distinguish semantic, source, product, stewardship, custody, control, consumer, specialist, and assurance responsibilities even when one person holds several.

**Policy gate.** Validate policy identity, precedence, scope, definitions, requirements, prohibitions, evidence, effective time, exceptions, review, and retirement.

**Control gate.** Connect each control objective to mechanism, owner, deployment boundaries, test, evidence, limitations, failure response, and correction.

**Exception gate.** Require rationale, residual risk, risk owner, approval, compensating controls, monitoring, expiry, renewal evidence, and closure.

**Consumer gate.** Verify purpose, local interpretation, mappings, transformations, protection, adoption, quality fitness, feedback, incident response, and disposal.

**Outcome gate.** Measure decision and control effects by consequence class; separate activity, coverage, throughput, effectiveness, and assurance.

**Federation gate.** Preserve enterprise invariants and arbitration while proving domains have real authority, capability, funding, and interoperable evidence.

**Lifecycle gate.** Trace change, succession, incident, migration, contract exit, retention, deletion, evidence custody, recovery, and final dependency closure.

### Executable evidence: consequence-based approvals and expiring exceptions

This illustrative policy derives required approvers from shared scope, personal data, and criticality, then blocks a proposal whose missing approval is covered only by an expired exception.

<!-- bijux-verify: {"id":"shared-data-decision-rights-contract","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"decisions=3\nready_for_activation=2\nblocked=1\nexpired_exceptions=1\nmissing_for_supplier_bank_routing=consumer_owner\norphan_decisions=0\npolicy_version=2026-09\n","stderr":""}} -->
```python
policy_version = "2026-09"
as_of = "2026-09-03"
decisions = [
    {
        "id": "customer_contact_standard",
        "owner": "customer_data_owner",
        "shared": True,
        "personal": True,
        "criticality": "high",
        "approvals": {"data_owner", "consumer_owner", "privacy", "security"},
        "exception_expiry": None,
    },
    {
        "id": "product_display_label",
        "owner": "product_data_owner",
        "shared": True,
        "personal": False,
        "criticality": "medium",
        "approvals": {"data_owner", "consumer_owner"},
        "exception_expiry": None,
    },
    {
        "id": "supplier_bank_routing",
        "owner": "supplier_data_owner",
        "shared": True,
        "personal": False,
        "criticality": "high",
        "approvals": {"data_owner", "security"},
        "exception_expiry": "2026-08-31",
    },
]

def required_approvals(decision):
    required = {"data_owner"}
    if decision["shared"]:
        required.add("consumer_owner")
    if decision["personal"]:
        required.add("privacy")
    if decision["criticality"] == "high":
        required.add("security")
    return required

ready = []
blocked = {}
expired_exceptions = 0
for decision in decisions:
    missing = required_approvals(decision) - decision["approvals"]
    expiry = decision["exception_expiry"]
    exception_active = expiry is not None and as_of < expiry
    if expiry is not None and not exception_active:
        expired_exceptions += 1
    if missing and not exception_active:
        blocked[decision["id"]] = missing
    else:
        ready.append(decision["id"])

missing = sorted(blocked["supplier_bank_routing"])
print(f"decisions={len(decisions)}")
print(f"ready_for_activation={len(ready)}")
print(f"blocked={len(blocked)}")
print(f"expired_exceptions={expired_exceptions}")
print(f"missing_for_supplier_bank_routing={','.join(missing)}")
print(f"orphan_decisions={sum(not d['owner'] for d in decisions)}")
print(f"policy_version={policy_version}")
```

The example proves only deterministic evaluation of three in-memory records under one invented policy. It does not establish that these roles are sufficient, approvals are genuine, owners are competent, the policy is lawful or ethical, risks are acceptable, controls operate, stakeholders participated, evidence is tamper-resistant, or outcomes are beneficial.

## Alternatives and Trade-Offs

**Centralized versus federated governance.** Centralization can standardize risk direction and resolve enterprise conflicts, but it can bottleneck local decisions and lose domain knowledge. Federation can place decisions near expertise, but it requires explicit invariants, interoperable evidence, capability, and arbitration.

**Asset ownership versus domain ownership.** Asset-level owners give precise accountability for products and datasets. Domain owners can coordinate semantics across assets, but their scope may become vague; use decision and asset boundaries beneath the domain.

**One owner versus collective deliberation.** One accountable owner prevents diffusion. Councils improve representation and challenge; combine deliberative input and recorded dissent with a named authorized decision maker.

**Mandatory platform versus control outcomes.** One platform can cheaply enforce common controls and evidence. Outcome-based standards allow local mechanisms and reduce lock-in, but assurance and interoperability cost more.

**Preventive versus detective controls.** Prevention blocks prohibited states early but can interrupt legitimate work when rules are incomplete. Detection supports learning and exceptions but allows exposure before correction; choose by consequence and reversibility.

**Manual versus automated policy.** Manual review handles ambiguity and social context but scales poorly and varies. Automated policy is fast and repeatable but encodes incomplete models; retain versioned rules, explanation, appeal, monitoring, and human ownership.

**Uniform governance versus risk tiers.** Uniform requirements appear fair and simple but overgovern low-risk data and under-specify critical uses. Tiering focuses effort but can be gamed or become stale; govern classification and review.

**Producer-defined quality versus consumer fitness.** Producer measures support common baselines and source correction. Consumers know local consequences; use shared evidence plus purpose-specific acceptance instead of one universal score.

**Open access versus conditioned sharing.** Openness can maximize reuse and transparency. Conditioned access can protect people, organizations, contracts, and legitimate interests; minimize restrictions while making terms, reasons, and appeal visible.

**Central funding versus chargeback.** Central funding supports common goods and broad adoption but can obscure demand. Chargeback reveals consumption cost but can deter beneficial reuse and encourage shadow copies; align funding with externalities.

**Permanent policy versus sunset and review.** Stable policy aids predictability. Mandatory review and sunset prevent obsolete rules from persisting, but careless expiry can remove needed safeguards; separate review due date from automatic loss of protection.

**Self-assurance versus independent review.** Owners can assess frequently and cheaply. Independent assurance adds challenge and credibility for material risk, while increasing cost and lead time; scope independence proportionally.

## Failure Modes and Misconceptions

1. **“Governance is the data council.”** Governance includes authority, decisions, controls, evidence, resources, correction, and lifecycle beyond meetings.
2. **“The platform owns the data because it hosts it.”** Custody and service operation do not grant semantic or business authority.
3. **“A named team is accountable.”** Accountability needs a person or formally occupied role with authority, resources, and escalation.
4. **“RACI resolves decision rights.”** It can omit veto, challenge, risk acceptance, delegation limits, appeal, and response time.
5. **“Federated means every domain chooses independently.”** Federation preserves shared invariants and arbitration while delegating bounded decisions.
6. **“One global standard guarantees interoperability.”** Adoption, semantics, mappings, versions, exceptions, and consumer behavior still require evidence.
7. **“Passing access control makes the use acceptable.”** Purpose, necessity, quality, ethics, contract, retention, and consequence remain.
8. **“Quality is a dataset score.”** Fitness depends on use, population, time, method, threshold, and decision consequence.
9. **“More metadata means better governance.”** Stale or unused metadata can create false confidence and operating cost.
10. **“Policy publication is implementation.”** Controls, evidence, exceptions, incidents, and outcomes determine whether policy operates.
11. **“Automated controls remove human accountability.”** People still choose rules and own false positives, false negatives, and consequences.
12. **“An exception is temporary because the document says so.”** It needs machine-observable expiry, monitoring, and closure.
13. **“The governance office can accept all data risk.”** Risk acceptance belongs to roles authorized for the affected consequence.
14. **“Producers own downstream misuse.”** Producers retain contract duties; consumers own local purpose, transformations, decisions, and disposal.
15. **“Open data needs no owner.”** Accuracy, maintenance, versioning, provenance, terms, correction, and retirement still need accountability.
16. **“Training completion proves behavior.”** It is activity evidence, not proof of correct decisions or reduced harm.
17. **“A maturity score proves capability.”** It compresses scope, evidence quality, uneven domains, and actual outcomes.
18. **“Stopping publication retires the asset.”** Copies, contracts, access, issues, exceptions, retention, backups, and recovery duties remain.

## Worked Examples

### Example 1

A customer domain owns identity semantics while regional systems capture contact details and a central product serves consolidated views. Decision rights assign identity rules to the customer data owner, source validation to regional owners, product service to its product owner, controls to named platform owners, and local use to consumer owners. A cross-domain forum resolves only collisions; it does not approve every correction. The conclusion is federated accountability with explicit interfaces, not shared ambiguity.

### Example 2

A board proposes making every catalog field mandatory for every dataset. Dependency analysis shows that critical assets lack owners and lineage while low-risk temporary research data would incur high documentation cost. The governance body defines tiered minimum metadata and tests discovery tasks for representative users. The conclusion is that useful, fresh metadata by risk tier is stronger than uniform population counts.

### Example 3

A credit decision model uses an address field that is 98 percent complete, above the enterprise threshold. Missingness is concentrated in one vulnerable population, and absence changes eligibility. The consumer owner rejects fitness for that decision, opens a source issue, establishes an interim review control, and measures outcomes by group. The conclusion is that aggregate quality can pass while decision fitness fails.

### Example 4

A product team requests full customer records for service personalization. Its declared use needs region and preference category, not name, birth date, identity documents, or complete history. Governance approves a purpose-specific view with expiry, access evidence, consumer retention, and prohibited onward use. The conclusion is that legitimate reuse does not justify maximum data transfer.

### Example 5

A domain cannot meet a lineage standard before launch. The authorized risk owner approves a 60-day exception covering named fields, with manual impact review, restricted change types, daily reconciliation, funding, and a fixed remediation owner. The exception expires automatically and cannot renew without new evidence. The conclusion is bounded risk treatment, not silent policy abandonment.

### Example 6

Three domains define “active supplier” differently because procurement eligibility, payment ability, and directory visibility are distinct states. The council rejects one overloaded enterprise term, assigns separate concepts and mappings, and requires consumers to bind explicitly. The conclusion is semantic interoperability through qualified meanings, not forced lexical uniformity.

### Example 7

A third-party reference dataset permits internal risk analysis but prohibits onward redistribution. The receiving owner records license, source version, derived-field rules, authorized consumers, retention, audit, and termination. An external report publishes aggregates that pass disclosure review rather than raw codes. The conclusion is that responsibility for a received copy includes respecting upstream rights and governing derivatives.

### Example 8

A shared identifier incident merges two people and propagates to screening, support, analytics, and an external processor. Incident authority freezes new propagation, the semantic owner approves the split, product owners publish corrections, consumer owners repair decisions, privacy and legal roles assess notification, and audit retains evidence. The conclusion is coordinated correction with unchanged role accountability.

### Example 9

Governance metrics show 100 percent owner assignment and 95 percent training completion, yet exceptions average 420 days and consumer changes miss deadlines. The enterprise adds decision lead time by class, expired exceptions, stale ownership, issue recurrence, adoption lag, control failures, recovery evidence, and harm measures. The conclusion is that coverage and activity metrics require outcome and lifecycle evidence.

### Example 10

A shared-data council is being replaced by domain forums and an enterprise risk forum. The migration maps every decision class, policy, exception, issue, control, asset, owner, escalation, budget, record, and audit obligation to the new model. Both structures process representative decisions in parallel before old authority is revoked. The conclusion is governance retirement by authority and dependency closure, not organizational announcement.

## Cross-Program Connections

- **Data engineering:** contracts, quality checks, lineage capture, orchestration, backfills, reconciliation, observability, retention, and correction implement governed outcomes in pipelines.
- **API and service engineering:** resource authority, schemas, authorization, purpose-specific views, rate and quota policy, asynchronous contracts, deprecation, and audit expose governance at interfaces.
- **Platform engineering:** catalogs, identity, policy enforcement, evidence, templates, self-service workflows, tenancy, reliability, and recovery reduce the cost of compliant execution.
- **Security engineering:** risk governance, authentication, authorization, classification, cryptography, privacy, logging, incident response, and assurance constrain every shared-data path.
- **Software architecture:** domain boundaries, context maps, shared kernels, dependency direction, product ownership, evolution, and fitness functions shape feasible governance allocation.
- **Organizational design:** delegation, incentives, forums, conflict, decision latency, funding, succession, and accountability determine whether the formal model operates.
- **Economics and decision science:** public goods, externalities, information value, option value, uncertainty, reversibility, and opportunity cost guide prioritization.
- **Systems engineering:** stakeholder needs, requirements, interface control, risk, configuration, verification, validation, assurance, operation, and disposal frame lifecycle evidence.

## References

1. National Institute of Standards and Technology, [The NIST Cybersecurity Framework 2.0](https://www.nist.gov/publications/nist-cybersecurity-framework-csf-20).
2. National Institute of Standards and Technology, [The NIST Privacy Framework 1.0](https://www.nist.gov/privacy-framework/privacy-framework).
3. U.S. Federal Data Strategy, [Practices](https://strategy.data.gov/practices/).
4. UK Government, [Data Ownership Model](https://www.gov.uk/government/publications/data-ownership-in-government/data-ownership-model).
5. UK Government, [Data Sharing Governance Framework](https://www.gov.uk/data-ethics-guidance/data-sharing-governance-framework).
6. W3C, [Data on the Web Best Practices: Data Quality Vocabulary](https://www.w3.org/TR/vocab-dqv/).
7. W3C, [ODRL Information Model 2.2](https://www.w3.org/TR/odrl-model/).
8. W3C, [PROV-O: The PROV Ontology](https://www.w3.org/TR/2013/REC-prov-o-20130430/).
9. OECD, [Recommendation of the Council on Enhancing Access to and Sharing of Data](https://legalinstruments.oecd.org/en/instruments/OECD-LEGAL-0463).
10. National Institute of Standards and Technology, [SP 800-160 Volume 1 Revision 1: Engineering Trustworthy Secure Systems](https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final).

## Exercises

### Exercise 1

For a shared customer asset used by identity, billing, fraud, support, analytics, and external processors, define the governance scope, decision inventory, role allocation, policy hierarchy, controls, evidence, funding, escalation, and lifecycle.

### Exercise 2

A company has a central data council, 400 policies, 97 percent owner coverage, and a populated catalog, but decisions take months and quality incidents recur. Diagnose the operating model and design evidence that distinguishes activity, coverage, throughput, control effectiveness, and outcomes.

### Exercise 3

Design an exception workflow for a critical product feed that cannot yet meet freshness and lineage standards. Include authority, risk, compensating controls, monitoring, expiry, renewal, remediation, consumer communication, and closure.

### Exercise 4

Compare centralized, federated, and domain-autonomous governance for identifiers, vocabularies, access, quality, product service, and consumer use. Propose a decision-by-decision target model.

### Exercise 5

Two organizations will share protected supplier data for a joint resilience program, then end the partnership after three years. Design governance from negotiation through operation, incident, change, correction, and exit.

## Answers to the Exercises

### Answer 1

Define the asset as identified customer entities, authoritative identifiers, match and survivorship evidence, approved attributes, relationships, histories, code bindings, propagation interfaces, metadata, quality evidence, and purpose-specific products—not every interaction merely associated with a customer. Inventory decisions about meaning, capture, identity, correction, access, purpose, quality, change, service, propagation, retention, deletion, incidents, external sharing, funding, and retirement. Assign one accountable person for each class: semantic owner, regional source owners, product owner, stewards, technical custodians, control owners, consumer owners, and privacy, security, legal, records, ethics, and assurance participants with explicit approval or challenge rights.

Create enterprise policies for identity, protection, purpose, evidence, retention, and risk; standards for contracts, stable identifiers, metadata, quality methods, access, lineage, propagation, correction, and recovery; local procedures for execution; and controls at authoritative writes, product boundaries, consumer access, exports, caches, processors, and disposal. Evidence includes approved revisions, provenance, access decisions, quality measures by use and population, consumer bindings, propagation and activation, exceptions, incidents, repair, retention, deletion, and recovery tests. Fund common identity and product service centrally or through a durable allocation model while consumers fund local adoption and use controls. Escalate semantic conflict, critical harm, expired exceptions, unowned issues, and investment blocks to roles with decision authority. Close processors, copies, derived data, contracts, credentials, holds, histories, and backups at lifecycle end.

### Answer 2

The evidence shows artifacts and assignments, not effective governance. Inspect whether owners are individuals with authority and budget, policies identify decisions and controls, the council has a charter and escalation power, domains can decide routine matters, consumers participate, exceptions expire, and recurrent incidents receive root-cause investment. Sample consequential decisions end to end: proposal, required evidence, participants, authority, decision time, control deployment, consumer adoption, observed outcome, issue correction, and closure. Separate delay caused by appropriate high-risk review from queueing caused by central micromanagement.

Report activity measures such as meetings, training, policy publication, and rule runs; coverage measures such as active owners, classified critical elements, bound consumers, and evidenced controls; throughput measures such as lead time and backlog by decision class; effectiveness measures such as false control outcomes, stale metadata, recurring issues, expired exceptions, propagation lag, and repair time; and outcome measures such as reduced decision error, prevented harm, improved discovery-to-use, service continuity, rights protection, and verified exit. Use denominators, scope, time, tier, confidence, and limitations. Replace unused or contradictory policies, delegate routine decisions, route collisions to specialized forums, fund systemic remediation, and verify changed outcomes rather than celebrating a revised chart.

### Answer 3

Name the exact feed, fields, consumers, decisions, current freshness and lineage gaps, affected population, plausible harms, obligations, and why conforming before the deadline is infeasible. The authorized operational or business risk owner—not the governance office alone—reviews alternatives and residual risk with semantic owner, product owner, consumer owners, reliability, security, privacy, legal, and records roles as triggered. Record the policy clauses, scope, start, fixed expiry, accountable remediation owner, budget, milestones, prohibited expansions, and conditions that revoke the exception early.

Compensating controls can include reduced consumer scope, manual validation for critical decisions, source-to-consumer reconciliation, daily freshness checks, immutable manifests, change freeze on untraceable fields, on-call escalation, and consumer-visible status. Monitor control results, incidents, lag, untraceable changes, population impact, and remediation progress. Notify consumers before activation and on any breach of threshold. Renewal requires fresh evidence, alternatives, residual-risk acceptance, and a new bounded term; it is not automatic. Closure requires the normal standards to pass, affected consumers to activate the conforming path, temporary controls and access to retire safely, evidence to archive, and any decisions harmed during the exception to be corrected.

### Answer 4

Centralized governance is strongest for common risk appetite, mandatory protection and evidence, enterprise identity namespaces, shared legal obligations, and arbitration; applied universally, it becomes slow and detached. Federated governance defines common invariants while delegating domain semantics, routine quality, product operation, and local controls to capable owners with interoperable evidence. Domain autonomy maximizes local speed but is unsafe where identifiers, meanings, risks, or changes cross boundaries. Choose per decision rather than choosing one label for the whole enterprise.

Centralize allocation and non-reuse rules for enterprise identifiers while domains own entity-specific creation and correction. Give concept authorities ownership of vocabularies and require versioned mappings rather than one council editing every term. Centralize minimum access, purpose, logging, privacy, and security outcomes; let domains implement approved mechanisms, preferably through platform capabilities. Let producers publish source quality evidence and consumer owners decide fitness for local uses under enterprise measurement rules. Assign product owners service and support, with platform teams accountable only for their capability boundaries. Require consumers to register purpose, transformations, adoption, incidents, and disposal. Use cross-domain forums for conflicts, an executive risk forum for unresolved consequence and funding, and independent assurance for selected critical controls.

### Answer 5

During negotiation, name provider and recipient owners, affected people and stakeholders, purpose, benefit, prohibited uses, data scope, quality, identity and vocabulary semantics, jurisdictions, legal authority, confidentiality, intellectual property, onward sharing, derived data, decision consequences, and exit conditions. Establish a signed relationship contract plus machine-readable or executable controls where semantics are sufficiently precise. Register products, schemas, mappings, lineage, processing locations, sub-processors, users, support contacts, incident duties, correction channels, retention, deletion, audit, assurance, cost, and change authority.

During operation, use least data and duration, strong identities, purpose-specific access, encryption, logging, quality and freshness evidence, consumer fitness review, periodic access recertification, reconciliation, recovery testing, and stakeholder recourse. Changes to purpose, fields, participants, jurisdiction, mappings, or risk trigger impact review and versioned acceptance. Incidents define containment authority, evidence preservation, notification, correction, decision remediation, and safe resumption. At the three-year exit, freeze new transfer at an agreed point, reconcile deliveries, resolve issues and exceptions, return or delete copies and derived data as required, close processors and credentials, preserve required records under named custody, test that backups cannot restore active use, and document surviving legal or audit duties. Both organizations' accountable owners accept closure; stopping the network connection is insufficient.
