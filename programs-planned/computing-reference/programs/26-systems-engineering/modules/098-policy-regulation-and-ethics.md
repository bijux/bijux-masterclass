---
module_id: SYSENG-098
program: Systems Engineering
level: 2
module_number: 98
title: Policy, Regulation, and Ethics
status: complete
last_verified: 2026-09-01
---

# Policy, Regulation, and Ethics

## One-Page Review

### Governing question

How can engineers translate overlapping policy, legal, regulatory, contractual, standards, and ethical obligations into traceable system constraints, accountable decisions, verifiable evidence, and effective remedy across jurisdictions and lifecycle changes?

### Essential definitions

- A **policy** is an authoritative statement of objectives, principles, rules, or expected conduct for a defined institution or scope.
- A **law** is a binding rule created or recognized by a competent legal authority; its applicability and interpretation depend on jurisdiction, facts, status, and time.
- A **regulation** is a binding rule or requirement issued under delegated legal authority and enforced through an institutional process.
- A **standard** specifies agreed requirements, guidance, or practices; it is not automatically binding unless incorporated by law, contract, policy, certification, or another authority.
- **ethics** is reasoned evaluation of what ought to be done in light of values, duties, rights, consequences, relationships, character, justice, and affected interests.
- A **right** is a justified claim or protected freedom held by a person or group; a corresponding duty identifies who must respect, protect, fulfill, or provide remedy for it.
- A **duty holder** is the actor legally, contractually, institutionally, or ethically responsible for an obligation within a defined scope.
- **applicability** is the justified determination that an authority and obligation govern a particular actor, system, activity, population, place, and time.
- **procedural justice** concerns the fairness, consistency, transparency, participation, contestability, and impartiality of a decision process.
- **remedy** is an accessible process that can stop, correct, compensate, explain, review, or otherwise address a violation or harmful outcome.

### Central model, mechanism, or theorem

For obligation $o$ in context $c$ at time $t$, define the normative trace

$$
N(o,c,t)=\langle B,J,S,D,C,E,R\rangle,
$$

where $B$ is authoritative basis, $J$ applicable jurisdiction or institution, $S$ covered subjects, systems, and activities, $D$ operative duty or prohibition, $C$ implemented control, $E$ evidence, and $R$ review, appeal, or remedy. A completion claim is eligible only if every applicable noncompensable element is justified:

$$
eligible(o,c,t)\Rightarrow B\land J\land S\land D\land C\land E\land R.
$$

This is a traceability gate, not legal interpretation or moral proof. Authorities may conflict, facts may be contested, controls can fail, and ethical duties can exceed enforceable minimums.

### Critical invariants

- Identify the authoritative text, version, effective status, jurisdiction, scope, definitions, exceptions, and competent interpreter before deriving a requirement.
- Separate binding law and contract from voluntary guidance, organizational policy, technical standard, and ethical recommendation.
- Translate normative language into system behavior without discarding purpose, affected rights, procedural safeguards, documentation, or remedy.
- Maintain bidirectional traceability from basis and stakeholder value through duty, control, evidence, owner, decision, and change trigger.
- Treat legality as necessary where applicable, not sufficient for ethical acceptability, safety, fairness, legitimacy, or public trust.
- Identify affected people, including non-users, workers, communities, future populations, and those unable to participate or appeal.
- Preserve hard prohibitions and rights; do not let a composite benefit or risk score compensate for a noncompensable constraint.
- Make material automated decisions observable, attributable, contestable, and reversible where the governing duty requires it.
- Analyze disparate impacts, accessibility, privacy, security, safety, labor, environment, power, and distribution—not only aggregate utility.
- Establish authority for exceptions, waivers, risk acceptance, disclosure, notification, appeal, correction, compensation, and retirement.
- Bind evidence to actual system, model, data, population, supplier, jurisdiction, deployment, purpose, and period.
- Reassess after legal, policy, factual, jurisdictional, ownership, model, data, purpose, population, supplier, or operating change.

### Common failures

Common failures include treating a framework as law; copying controls from another jurisdiction; asking counsel for approval without supplying system facts; reducing ethics to a principles poster; equating consent with fairness; performing impact assessment after design is fixed; assuming anonymization eliminates risk; testing group averages while hiding intersectional harm; documenting explainability without enabling challenge; declaring human oversight while denying time or authority; treating certification as permanent compliance; outsourcing a regulated function without retained control; keeping an exception forever; and interpreting the absence of enforcement as permission or ethical acceptance.

### Compact example

A synthetic registry contains three obligations and six required trace fields each. Seventeen of eighteen fields are present, but the adverse-decision obligation lacks an appeal/remedy path. The gate rejects readiness despite a 94.4% pass rate. This demonstrates noncompensable metadata completeness only; it cannot establish applicability, legal sufficiency, ethical legitimacy, control effectiveness, or accessible remedy.

### Connections

This module builds on stakeholders, requirements, governance, risk, assurance, security/privacy, operations, systems of systems, interoperability, emergent risk, cognitive work, and organizational control. It prepares adaptive-system governance and whole-system review while connecting to data stewardship, API policy, platform guardrails, machine-learning evaluation, accessibility, and software supply chains.

## Governing Question

What evidence shows that a software-intensive capability is permitted, constrained, accountable, and worthy of deployment for its actual purpose, population, place, and time—and that affected people have meaningful protection and remedy when it fails?

Engineers do not replace legislators, regulators, courts, counsel, ethicists, domain professionals, or affected communities. They do determine what the system senses, infers, stores, exposes, decides, permits, blocks, logs, and repairs. Normative obligations become real or illusory through architecture, data, interfaces, operations, contracts, and organizational authority. That makes policy, regulation, and ethics an engineering concern throughout the lifecycle.

## Why This Matters

The same service may be subject to privacy, consumer, safety, employment, accessibility, cybersecurity, sector, procurement, records, intellectual-property, and competition rules, plus contracts and internal policies. Applicability can depend on where people are located, who acts in which role, what data and purpose are involved, and whether the system materially influences a consequential decision. A generic “compliant” label loses those conditions.

Ethical analysis addresses questions that enforceable rules may leave open: which benefits and burdens are created, whose autonomy is constrained, who was excluded from design, whether a technically lawful practice exploits power, and what duties exist under uncertainty. Ethical principles can conflict. Transparency can expose privacy or security; equal treatment can preserve unequal conditions; aggregate benefit can burden a minority. Engineering must expose these conflicts to legitimate decision makers rather than silently encoding one answer.

Current primary frameworks illustrate different authorities. The EU AI Act is binding EU legislation within its scope; GDPR is binding data-protection law within its scope. The Council of Europe AI Framework Convention creates treaty obligations for parties according to its status and implementation. UNESCO's AI ethics recommendation and NIST AI RMF provide influential but differently authoritative guidance. Their similar vocabulary does not make their legal force, covered actors, or required evidence interchangeable.

## Prerequisites and Retrieval

Before making a normative assurance claim, retrieve:

1. system purpose, intended and prohibited uses, deployment contexts, actors, populations, jurisdictions, lifecycle stage, and material decisions or effects;
2. stakeholder values, rights, unacceptable harms, benefits, burdens, power relations, accessibility needs, environmental effects, and available alternatives;
3. authoritative legal and regulatory texts, definitions, recitals or explanatory material where relevant, amendments, effective status, territorial reach, exceptions, enforcement, and competent guidance;
4. contracts, procurement duties, licenses, certifications, insurance conditions, collective agreements, organizational policies, professional codes, standards, and public commitments;
5. legal-entity roles and supply-chain roles: developer, provider, deployer, operator, controller, processor, employer, public authority, importer, distributor, vendor, and subcontractor as applicable;
6. data inventory, purpose, provenance, legal basis, sensitivity, retention, sharing, inference, model use, cross-border flow, access, correction, deletion, and security;
7. system architecture and behavior: inputs, outputs, models, confidence, automation, human authority, logging, interfaces, dependencies, failure modes, updates, rollback, and retirement;
8. affected decision process: notice, explanation, participation, consent where relevant, review, appeal, correction, compensation, and alternative channel;
9. impact evidence disaggregated across relevant groups, contexts, time, severity, likelihood, reversibility, cumulative effects, and uncertainty;
10. ownership and governance: duty holders, interpreters, approvers, independent review, exception authority, risk acceptance, incident reporting, regulator contact, and remedy operations;
11. verification evidence: trace matrices, tests, audits, impact assessments, threat and safety analyses, accessibility reviews, records, operational monitoring, complaints, and corrective action;
12. change triggers and horizon scanning for new law, guidance, facts, purpose, data, models, suppliers, jurisdictions, affected populations, enforcement, and social expectations.

Build a **normative trace** for one consequential outcome. Quote or precisely cite the operative source outside the chapter as allowed by its license; record the interpretation and facts; derive a testable duty; map technical and organizational controls; identify evidence, residual uncertainty, decision authority, notice, appeal, remedy, and renewal trigger. Have qualified legal or policy reviewers validate jurisdiction-specific interpretation when stakes require it.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish law, regulation, policy, contract, standard, certification, ethics, and professional guidance;
2. determine what facts and authority are needed for an applicability analysis;
3. translate normative duties into traceable technical and organizational controls;
4. identify rights, duty holders, affected stakeholders, benefits, burdens, power, and remedy;
5. reason across duty-, consequence-, rights-, justice-, care-, and virtue-oriented ethical perspectives;
6. recognize conflicts among jurisdictions, principles, objectives, and stakeholder interests;
7. design impact assessments that influence decisions before commitment and continue through operation;
8. define meaningful transparency, human oversight, contestability, evidence, and redress;
9. govern exceptions, suppliers, monitoring, incidents, and normative change;
10. state bounded conclusions without offering unsupported legal or moral certainty.

## Core Exposition

**Separate sources by authority.** Record issuer, instrument type, jurisdiction, covered actors, binding status, version, effective date, and relationship to other sources. A statute, agency rule, regulator guidance, harmonized standard, contract, corporate policy, and ethics code can all influence design, but in different ways. Do not cite a voluntary framework as if it creates a legal permission or defense.

**Establish applicability from facts.** Legal conclusions depend on system facts. Document entities, roles, locations, users, affected people, purpose, data, decision, sector, scale, and deployment method. Supply counsel or regulators with architecture and operational detail rather than a product slogan. Revisit applicability when the purpose, population, or distribution channel changes.

**Preserve normative purpose.** A requirement should express the protected interest as well as the implementation. “Store a consent flag” can miss whether consent is informed, specific, freely given, revocable, and applicable. “Provide an explanation field” can miss whether a person can understand and challenge a decision. Derive controls that preserve the duty under real use, failure, and power asymmetry.

**Treat requirements as a connected case.** Link each obligation to basis, interpretation, affected actors, system behavior, owner, evidence, exception, remedy, and change trigger. Keep the reverse link from implementation and evidence to the source. When a source or design changes, traverse both directions. A spreadsheet can hold identifiers; it cannot replace interpretation or control effectiveness.

**Identify rights and duty holders.** Rights language becomes actionable when paired with who must do what, when, for whom, and how a violation can be challenged. Distinguish duties to refrain, protect, provide, disclose, document, consult, monitor, or remedy. Include affected non-users and workers. Avoid making the least powerful participant carry the burden of detecting every violation.

**Use several ethical lenses.** Duty and rights ask what must not be traded away. Consequence analysis compares benefits, harms, likelihood, magnitude, distribution, and alternatives. Justice asks who receives benefits, burdens, voice, and remedy. Care attends to dependency, vulnerability, and relationships. Virtue and professional responsibility ask what competent, honest stewardship requires. The lenses reveal conflicts; they do not produce an automatic score.

**Reject false commensuration.** Some harms can be compared or mitigated; others are prohibited or require independent justification. Do not subtract a privacy violation from aggregate convenience or let high average accuracy compensate for an inaccessible appeal. Record hard constraints separately from optimizable objectives. Escalate irreducible conflict to legitimate authority with affected-party input.

**Engage affected stakeholders meaningfully.** Participation must occur early enough to influence purpose, requirements, and alternatives. Compensate expertise where appropriate, provide accessible formats, protect vulnerable participants, and report how input changed decisions. Consultation does not transfer accountability or establish consent from an entire population.

**Perform impact assessment before commitment.** Describe intended benefit, alternatives including non-deployment, affected groups, causal pathways, rights, severity, likelihood, reversibility, cumulative effects, uncertainty, controls, residual impact, owners, and decision thresholds. Repeat at material change and during operation. An assessment written after procurement is advocacy unless it can still stop or reshape the system.

**Disaggregate evidence.** Aggregate metrics can conceal concentrated harm. Analyze relevant groups and intersections with sufficient privacy protection and statistical humility. Small samples, missing labels, selection effects, measurement error, historical inequity, and shifting populations limit conclusions. Lack of evidence about a group is uncertainty, not evidence of no harm.

**Engineer privacy beyond secrecy.** Address lawful and ethical purpose, data minimization, inference, linkage, retention, access, correction, deletion, sharing, security, and power. Pseudonymization and anonymization claims need attack- and context-aware evidence. Privacy can be harmed by observation, prediction, exposure, manipulation, or loss of practical obscurity even without a conventional breach.

**Make transparency audience- and decision-specific.** Regulators, auditors, operators, affected people, and the public need different information. Provide source, purpose, limits, data relevance, decision role, uncertainty, ownership, and challenge path at the right time. Full source-code release may be useless or unsafe; a vague summary may be insufficient. Transparency supports accountability but does not substitute for acceptable behavior.

**Design human oversight as control.** A reviewer needs competence, independence, information, time, authority, and feasible alternatives. Measure override, agreement, escalation, and outcomes, but avoid targets that reward ritual approval. Prevent automation bias and rubber stamping through case design, uncertainty visibility, sampling, independent checks, and accountability. A human signature cannot legalize or legitimize a prohibited system.

**Enable contestability and remedy.** Notify affected people when appropriate; explain material grounds; offer accessible human review; preserve evidence; allow correction; suspend harmful effects where required; and define escalation, compensation, or other remedy. Appeal data should feed system learning without penalizing appellants. Track access, delay, reversal, disparity, recurrence, and unresolved harm.

**Control exceptions and waivers.** State authority, scope, basis, duration, compensating controls, affected people, evidence, review, and expiry. Some prohibitions cannot be waived by organizational preference. Emergency exceptions should be narrow, visible, reversible, and reconciled. Repeated exceptions often indicate an infeasible policy or a business model in conflict with the duty.

**Govern suppliers and models.** Contracts should expose facts needed for the retained obligation: data sources, model and version, limitations, evaluation, incidents, vulnerabilities, subprocessors, changes, audit, continuity, deletion, and exit. A vendor claim or certification does not transfer the deploying organization's contextual duties. Validate integrated outcomes and preserve the ability to stop or replace the dependency.

**Maintain evidence and records proportionately.** Record decisions, interpretations, versions, tests, incidents, overrides, changes, and residual risk with integrity and access controls. More retention can itself violate privacy or increase security risk. Define purpose, audience, retention, legal hold, deletion, and provenance. Evidence must be usable by reviewers and affected processes, not merely archived.

**Monitor law and social context.** Normative status changes through legislation, judicial decisions, regulator guidance, enforcement, standards, treaties, contracts, and public expectations. Assign owners and cadence, but also event triggers. Freeze the authority snapshot used for each decision and record when a new source requires reassessment. Do not silently apply future, draft, or foreign rules as current binding law.

**State bounded conclusions.** A review can conclude that identified duties are traced and controls evidenced for specified entities, purposes, jurisdictions, configurations, populations, and dates, subject to named limitations. It cannot guarantee universal legality or ethical acceptance. Qualified authorities retain their roles, and affected people retain rights to challenge.

The following fixture checks declared normative-trace metadata. It cannot interpret a law or establish ethical legitimacy.

<!-- bijux-verify: {"id":"normative-trace-ledger","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"obligations=3\nrequired_fields=6\nchecks=18\npassed_checks=17\nfailed_checks=1\nblocked=adverse_decision:remedy\nreadiness_gate=reject_incomplete_normative_trace\nevidence=declared_metadata_only\n","stderr":""}} -->
```python
obligations = {
    "purpose_limitation": {
        "basis": True, "scope": True, "owner": True,
        "control": True, "evidence": True, "remedy": True,
    },
    "adverse_decision": {
        "basis": True, "scope": True, "owner": True,
        "control": True, "evidence": True, "remedy": False,
    },
    "security_notification": {
        "basis": True, "scope": True, "owner": True,
        "control": True, "evidence": True, "remedy": True,
    },
}
fields = ("basis", "scope", "owner", "control", "evidence", "remedy")
blocked = [
    f"{name}:{field}"
    for name, trace in obligations.items()
    for field in fields
    if not trace[field]
]
checks = len(obligations) * len(fields)
print(f"obligations={len(obligations)}")
print(f"required_fields={len(fields)}")
print(f"checks={checks}")
print(f"passed_checks={checks - len(blocked)}")
print(f"failed_checks={len(blocked)}")
print(f"blocked={','.join(blocked)}")
print("readiness_gate=reject_incomplete_normative_trace")
print("evidence=declared_metadata_only")
```

## Definitions and Notation

Let normative sources be $B$, jurisdictions and institutions $J$, covered subjects and systems $S$, duties and prohibitions $D$, controls $C$, evidence $E$, and remedy or review $R$. Context $c$ includes actors, purpose, population, data, system, deployment, and facts; time $t$ includes version and legal status.

For each obligation, $N(o,c,t)=\langle B,J,S,D,C,E,R\rangle$. A missing element may mean the obligation is not yet actionable, the control is incomplete, or the trace does not justify a completion claim. A “pass” is itself a reviewable assertion, not truth created by the ledger.

Define the normative evidence envelope

$$
\Omega_N=\langle entities,purposes,jurisdictions,populations,systems,data,suppliers,period,assumptions\rangle.
$$

Claims outside $\Omega_N$ require applicability and evidence review. Ethical reasoning also considers affected interests beyond the set of enforceable obligations represented in $N$.

## Mechanisms, Invariants, or Proof Structure

1. **Frame purpose and impact.** Name intended benefit, alternatives, stakeholders, affected people, rights, harms, power, and prohibited outcomes.
2. **Identify authorities.** Classify law, regulation, policy, contract, standard, certification, professional duty, and ethical guidance by force and scope.
3. **Establish applicability.** Record actors, roles, jurisdictions, activities, data, decisions, definitions, exceptions, status, and qualified interpretation.
4. **Derive obligations.** Preserve normative purpose while defining duties, prohibitions, thresholds, procedures, and affected rights.
5. **Map controls and ownership.** Connect technical and organizational behavior, duty holders, resources, exceptions, suppliers, and evidence.
6. **Analyze ethical conflict.** Apply rights, duties, consequences, justice, care, professional responsibility, alternatives, and noncompensable constraints.
7. **Design participation and remedy.** Provide meaningful stakeholder input, notice, oversight, challenge, correction, appeal, and redress.
8. **Verify impacts and controls.** Test representative populations, failures, misuse, accessibility, security, privacy, distribution, and operational outcomes.
9. **Decide transparently.** Record authority, rationale, dissent, uncertainty, residual impact, conditions, and stop or renewal criteria.
10. **Monitor and evolve.** Track law, guidance, system change, complaints, disparity, incidents, exceptions, supplier change, and control effectiveness.

Core invariants are: no applicability claim lacks authoritative basis and relevant facts; no voluntary framework is represented as binding law; no hard right or prohibition is averaged away; no human oversight lacks meaningful control; no impact assessment is prevented from changing the decision; no exception lacks authority and expiry; no supplier claim replaces contextual assurance; no material adverse decision lacks the required challenge and remedy; and no normative conclusion escapes its envelope and date.

There is no algorithm that resolves every conflict among law, rights, values, consequences, and institutional authority. The engineering discipline is to expose the conflict, preserve protected constraints, produce trustworthy evidence, enable legitimate decision and remedy, and keep the case current.

## Alternatives and Trade-Offs

**Rules versus principles.** Detailed rules improve consistency and testability but can become obsolete or invite boundary gaming. Principles adapt to context but require judgment and can create uncertainty. Combine protected principles with scoped controls, examples, evidence, and review.

**Ex ante approval versus continuous oversight.** Predeployment review can prevent harm but may freeze assumptions. Continuous monitoring sees actual outcomes but cannot justify exposing people to prohibited or irreversible harm. Use consequence-based entry gates plus operating limits, monitoring, stop authority, and renewal.

**Transparency versus privacy and security.** Disclosure supports accountability and challenge but can expose personal data, intellectual property, or attack paths. Tailor information to audience and purpose, protect necessary detail, and ensure secrecy claims do not eliminate independent scrutiny or affected-person rights.

**Uniform treatment versus equitable outcomes.** Identical procedures can be simple and consistent while preserving historical or accessibility barriers. Tailoring can improve substantive access but risks stereotyping or unequal rules. Analyze relevant differences, rights, evidence, and affected-party input.

**Innovation sandbox versus full deployment.** Bounded experimentation can generate evidence with limited exposure, but “pilot” labels do not erase law or harm. Define participants, consent or authority, constraints, duration, monitoring, remedy, data handling, exit, and prohibition on uncontrolled expansion.

**Internal governance versus external assurance.** Internal teams know the system and can respond quickly; independent reviewers provide challenge and legitimacy but may lack context. Preserve reviewer competence, access, independence, conflict disclosure, and management responsibility. Neither structure guarantees correctness.

## Failure Modes and Misconceptions

- **“Compliance is a checklist.”** Applicability, interpretation, implementation, effectiveness, evidence, and remedy remain contextual.
- **“A standard is the law.”** Standards become binding only through a relevant authority or agreement.
- **“Legal means ethical.”** Law sets obligations and permissions, not a complete account of justice, care, legitimacy, or professional duty.
- **“Ethics is subjective opinion.”** Ethical reasoning can make values, rights, duties, consequences, and conflicts explicit and reviewable.
- **“Consent makes the use fair.”** Consent may be unavailable, coerced, uninformed, overly broad, or irrelevant to other duties and impacts.
- **“An impact score decides.”** Scores conceal value judgments, uncertainty, distribution, and noncompensable constraints.
- **“Anonymized data is risk-free.”** Linkage, inference, context, and future data can restore identification or create group harm.
- **“Transparency requires source code.”** Useful transparency depends on audience, decision, timing, and ability to act.
- **“A human reviewer solves automation risk.”** Oversight without time, information, independence, authority, and alternatives is ceremonial.
- **“Accuracy proves fairness.”** Measurement validity, subgroup effects, allocation, process, rights, and remedy are separate.
- **“The vendor is compliant.”** A supplier's claim may not cover the deployer's purpose, population, integration, or jurisdiction.
- **“Certification is permanent.”** Scope, versions, conditions, surveillance, and system change bound it.
- **“No complaint means no harm.”** People may lack notice, access, evidence, safety, or confidence that complaint can help.
- **“A waiver removes the duty.”** Authority and law determine what can be waived; ethical and stakeholder consequences remain.
- **“Future regulation can be handled later.”** Architecture and data choices can make later rights, evidence, or remedy prohibitively difficult.

## Worked Examples

### Example 1

**Situation:** A team cites a voluntary risk framework as proof that an automated hiring system is lawful. **Reasoning:** The framework structures risk work but does not determine employment-law applicability or authorize processing. Build separate legal, contractual, and ethical traces. **Conclusion:** Similar control language does not make authorities interchangeable.

### Example 2

**Situation:** A lender reports equal aggregate model accuracy across two groups. **Reasoning:** Approval errors, pricing, appeal access, data validity, and intersectional effects differ. Evaluate decision and remedy outcomes under applicable duties. **Conclusion:** Aggregate predictive performance cannot establish procedural or distributive fairness.

### Example 3

**Situation:** A hospital obtains broad consent for secondary model training. **Reasoning:** Power, specificity, withdrawal, patient expectations, data minimization, public interest, and alternative bases still matter. **Conclusion:** A consent record is not a universal ethical or legal permission.

### Example 4

**Situation:** A fraud service gives every denial a generic “risk detected” message. **Reasoning:** The text protects model detail but does not enable meaningful review. Provide decision-relevant grounds, evidence correction, accessible human appeal, and fraud-resistant disclosure. **Conclusion:** Transparency must support action, not merely exist.

### Example 5

**Situation:** A public-benefits system requires caseworker confirmation of automated recommendations. **Reasoning:** Caseload targets, hidden features, and no override path produce rubber stamping. Reallocate time and authority, show material evidence and uncertainty, sample decisions, and monitor reversals. **Conclusion:** Human presence is not human control.

### Example 6

**Situation:** A platform retains detailed logs indefinitely for accountability. **Reasoning:** Retention improves investigation but increases privacy, breach, access, and chilling risks. Define purpose-specific fields, access, integrity, retention, legal holds, aggregation, and deletion. **Conclusion:** Evidence preservation is itself a constrained design problem.

### Example 7

**Situation:** A model performs poorly for a small linguistic community absent from the evaluation set. **Reasoning:** Missing data creates uncertainty and potential exclusion, not proof of no disparity. Restrict use, gather legitimate evidence with community involvement, or provide a reliable alternative. **Conclusion:** Unknown impact needs control, not optimistic imputation.

### Example 8

**Situation:** An emergency policy waives normal review for thirty days, but the system never expires the flag. **Reasoning:** A bounded exception becomes default behavior. Encode scope and expiry, require reconciliation, notify owners, and block renewal without evidence and authority. **Conclusion:** Exception lifecycle belongs in system state.

### Example 9

**Situation:** A vendor updates a foundation model behind a stable API. **Reasoning:** Behavior, data handling, evaluation, explanation, and affected outcomes can change without schema change. Require version notice, evidence, staged validation, rollback, and renewed normative traces. **Conclusion:** Contract and interface stability do not preserve compliance or ethics.

### Example 10

**Situation:** A jurisdiction-specific assessment is copied to a global deployment. **Reasoning:** Covered actors, rights, languages, social conditions, remedies, and regulators differ. Identify common controls, then perform local applicability and impact analysis. **Conclusion:** Normative assurance is not automatically portable.

## Cross-Program Connections

- **Platform Engineering:** policy-as-code, admission controls, identity, evidence, exceptions, and paved paths operationalize but do not interpret normative duties.
- **API and Service Engineering:** notice, consent, purpose, error semantics, audit, versioning, deprecation, and appeal require explicit contracts and ownership.
- **Data Engineering:** collection, lineage, quality, minimization, retention, deletion, access, inference, and cross-border flow carry legal and ethical effects.
- **Security Engineering:** confidentiality, integrity, availability, abuse prevention, disclosure, logging, and incident duties interact with rights and safety.
- **Distributed Systems:** replication, jurisdiction, consistency, deletion, identity, and partial failure complicate enforcement and remedy.
- **Machine Learning:** data validity, bias, uncertainty, explainability, monitoring, drift, feedback, model change, and human oversight shape impact.
- **Human Factors:** notice, comprehension, meaningful choice, workload, authority, accessibility, and contestability determine whether procedural safeguards work.
- **Organizational Engineering:** duty holders, resources, incentives, suppliers, independent review, reporting, and remediation make policy real.
- **Economics:** externalities, market power, information asymmetry, distribution, and opportunity cost illuminate who benefits and bears harm.
- **Environmental Engineering:** energy, water, material extraction, disposal, and intergenerational impact broaden the system boundary.

## References

1. European Union, [Regulation (EU) 2024/1689 laying down harmonised rules on artificial intelligence](https://eur-lex.europa.eu/eli/reg/2024/1689/oj?locale=en), Official Journal of the European Union, 2024.
2. European Union, [Regulation (EU) 2016/679 General Data Protection Regulation](https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng/), Official Journal of the European Union, 2016.
3. Council of Europe, [Framework Convention on Artificial Intelligence and Human Rights, Democracy and the Rule of Law](https://www.coe.int/en/web/artificial-intelligence/the-framework-convention-on-artificial-intelligence), CETS No. 225, opened for signature 2024.
4. National Institute of Standards and Technology, [Artificial Intelligence Risk Management Framework 1.0](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10), NIST AI 100-1, 2023.
5. UNESCO, [Recommendation on the Ethics of Artificial Intelligence](https://www.unesco.org/en/articles/recommendation-ethics-artificial-intelligence?hub=66929), adopted 2021.
6. Office of the United Nations High Commissioner for Human Rights, [Guiding Principles on Business and Human Rights](https://www.ohchr.org/documents/publications/guidingprinciplesbusinesshr_en.pdf), HR/PUB/11/4, 2011.
7. Association for Computing Machinery, [ACM Code of Ethics and Professional Conduct](https://www.acm.org/code-of-ethics), 2018.
8. IEEE Standards Association, [IEEE 7000-2021: Model Process for Addressing Ethical Concerns during System Design](https://standards.ieee.org/ieee/7000/6781/), 2021.

## Exercises

### Exercise 1

Classify eight common normative sources for a cloud health service by authority and explain why their requirements cannot be merged into one undifferentiated checklist.

### Exercise 2

A trace ledger contains five obligations and seven required fields per obligation. Thirty-three fields pass. Compute the pass rate and explain why the two missing fields may still block release.

### Exercise 3

Construct a normative trace for an automated adverse eligibility decision, including basis, applicability, control, evidence, human authority, notice, appeal, correction, and remedy.

### Exercise 4

Design an ethical impact assessment for a city proposal to deploy computer vision in public transit stations.

### Exercise 5

Evaluate how a platform team should operationalize jurisdiction-specific data-retention and deletion duties without pretending that policy-as-code interprets the law.

## Answers to the Exercises

### Answer 1

The sources might include a national health-privacy statute, regulator rule, regulator guidance, patient contract or notice, cloud-provider agreement, ISO or industry security standard, organizational data policy, and a professional ethics code. Record issuer, jurisdiction, binding status, covered actors and activities, version, enforcement, and incorporation path for each.

The statute and rule may be binding within scope; guidance may explain regulator expectations without identical legal force; a contract binds its parties and can add duties; a standard is voluntary unless incorporated; policy binds through organizational authority; a professional code creates professional expectations and may influence discipline or interpretation. None automatically overrides a conflicting higher authority.

Create linked traces because definitions, purposes, evidence, exceptions, and remedies differ. Common controls such as access logging may support several obligations, but retain separate rationales and tests. Qualified reviewers determine conflicts and applicability. The resulting system case can show coverage without claiming that technical compliance with one source establishes every other duty.

### Answer 2

There are $5\times7=35$ required fields. With 33 passing,

$$
\frac{33}{35}\times100\%\approx94.3\%.
$$

The aggregate cannot compensate for a missing noncompensable element. If one obligation lacks authoritative basis, its interpretation may be invented; if an adverse decision lacks remedy, an affected person may have no effective protection. Identify each failure by obligation and field, consequence, owner, and authority.

Also validate the passing assertions. A cited basis may be obsolete, jurisdiction wrong, control ineffective, evidence unrepresentative, or remedy inaccessible. The ledger supports completeness review only. Release requires a context-specific decision by competent authority with verified controls, open uncertainty, and no unresolved hard prohibition.

### Answer 3

Define the decision, affected benefit or service, entities, jurisdiction, population, data, model role, and whether automation makes or materially supports the result. Cite the authoritative legal, contractual, policy, and ethical bases separately and record qualified interpretation. Identify protected interests such as non-discrimination, privacy, due process, accuracy, accessibility, and timely service.

Controls include purpose and feature limits, data quality and provenance, representative evaluation, uncertainty thresholds, prohibited proxy review, caseworker information and independent authority, reason capture, notice in accessible language, evidence access, correction, appeal, suspension where required, and alternative service channel. Preserve model, policy, data, and decision versions without excessive retention.

Evidence covers subgroup and intersectional outcomes, false adverse decisions, override and appeal behavior, accessibility, delay, workload, security, drift, and remedy completion. The duty holder owns correction and compensation or other remedy; an independent authority can review disputed cases. Monitor reversals, complaint access, repeated errors, and changed law or purpose. A high accuracy score or caseworker click does not close the trace.

### Answer 4

First test the necessity and alternatives: staffing, lighting, help points, non-biometric sensors, limited event detection, or no deployment. Identify purposes and prohibit expansion such as generalized identity tracking without new authority. Map riders, workers, children, disabled people, marginalized communities, bystanders, law enforcement, vendors, and non-users whose movement is captured.

Analyze safety benefit, surveillance and chilling effects, discrimination, misidentification, accessibility, labor effects, data breach, function creep, environmental cost, and unequal station coverage. Consider rights, duties, consequences, distributive and procedural justice, relationships of trust, and power. Establish legitimate public participation early, publish limitations, and preserve dissent.

If a bounded use remains eligible, minimize fields and retention, constrain zones and purpose, separate identity, secure access, log use, test groups and conditions, provide notice and non-punitive alternatives, restrict sharing, and create independent complaint, correction, and remedy. Define stop thresholds and sunset. A pilot needs the same applicability analysis and must not become permanent through inertia.

### Answer 5

The platform should not decide which law applies. Legal and data-governance owners provide versioned, jurisdiction- and purpose-specific policy decisions with source, interpretation, data classes, actors, retention clocks, holds, deletion semantics, exceptions, evidence, and effective dates. The platform translates approved decisions into reusable controls and exposes where automation cannot implement the duty.

Capabilities may include classification metadata, policy versioning, region and purpose binding, retention scheduling, hold precedence, deletion propagation, backup expiry, supplier requests, immutable decision evidence, reconciliation, exception expiry, and dashboards. APIs must distinguish request acceptance from verified deletion and preserve failures for remediation. Access and evidence retention need their own minimization controls.

Test clock boundaries, reclassification, conflicting jurisdictions, legal holds, replicas, derived data, model artifacts, offline stores, supplier failure, restoration, appeals, and policy migration. Require owner review for unclassified data and conflicts. Monitor overdue deletion, orphan stores, expired holds, exceptions, and unverifiable supplier outcomes. Policy-as-code reliably executes an approved interpretation; it neither creates that interpretation nor guarantees lawful, ethical outcomes.
