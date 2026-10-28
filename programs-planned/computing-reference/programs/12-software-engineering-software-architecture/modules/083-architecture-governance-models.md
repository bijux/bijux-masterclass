---
module_id: SARCH-083
program: Software Engineering: Software Architecture
level: 2
module_number: 83
title: Architecture Governance Models
status: complete
last_verified: 2026-09-06
---

# Architecture Governance Models

## One-Page Review

### Governing question

How should an organization allocate direction, decision authority, accountability, escalation, and assurance for architecture so that consequential risk is governed without turning architecture into a centralized approval queue?

### Essential definitions

- **governance** is the system by which legitimate authorities set direction, delegate decision rights, monitor outcomes, and hold decision makers accountable;
- **management** plans and executes work within the direction and authority established by governance;
- an **architecture decision right** is authority to decide a bounded class of architectural choices under stated constraints;
- a **decision domain** groups choices with similar stakeholders, consequences, expertise, and escalation needs;
- **centralized governance** reserves a decision class for one enterprise or portfolio authority;
- **federated governance** distributes decisions among domains under shared outcomes, interfaces, and escalation;
- **delegated governance** grants a named team authority within an explicit envelope while the delegator retains oversight obligations;
- **embedded governance** places relevant expertise and evidence close to delivery rather than in a separate final gate;
- **automated assurance** evaluates machine-checkable evidence against a policy, but cannot accept unencoded residual risk;
- an **exception** is a governed, time-bounded departure from a rule with an owner, rationale, consequence, compensating action, and expiry;
- **decision latency** is elapsed time from a decision-ready request to an authorized, communicated outcome;
- **assurance independence** is sufficient separation between implementation and selected evaluation or acceptance duties.

### Central model, mechanism, or theorem

Represent a decision class as

$$
D=(S,A,E,C,R,X),
$$

where $S$ is scope, $A$ accountable authority, $E$ delegated envelope, $C$ required consultation and evidence, $R$ review or monitoring, and $X$ escalation and exception path. Choose the least centralized model that still gives the decision maker legitimate authority, necessary context, competence, capacity, consequence feedback, and system-wide integrity. Centralization is justified by shared irreversible consequence—not by architecture's importance alone.

### Critical invariants

- governing bodies set outcomes, risk direction, delegations, and accountability; they do not outsource responsibility to a board or tool;
- every material decision class has one accountable authority and a discoverable escalation path;
- authority, expertise, information, resources, and consequence feedback are co-located or explicitly connected;
- local decisions remain inside shared legal, safety, security, data, accessibility, financial, and interoperability constraints;
- review depth is proportional to uncertainty, reversibility, blast radius, and consequence;
- evidence is created throughout delivery, not assembled only for a final meeting;
- automated checks state their encoded scope and route residual judgment to authorized humans;
- exceptions are visible, funded, monitored, and retired or incorporated deliberately;
- governance performance includes outcomes, delay, rework, incidents, burden, equity, and trust;
- decision records preserve rationale without converting historical choices into permanent rules.

### Common failures

Common failures include calling an architecture review board “governance”; requiring central approval for every technology choice; delegating execution without authority; distributing decisions without shared invariants; confusing advice with approval; using consensus to hide accountability; applying one model to every decision; reviewing too late; automating vague policy; treating compliance evidence as architecture quality; counting approvals as value; granting permanent exceptions; excluding operators and affected users; and allowing executives to disclaim accountability because specialists signed a document.

### Compact example

A company governs encryption by separating decision classes. The governing body sets protection outcomes and risk tolerance. Security authority owns approved algorithms, key custody, exception criteria, and assurance. Product teams choose implementation within a machine-checkable envelope and own correct data classification and operation. A shared platform supplies key services and evidence. Novel cryptographic designs escalate to specialist review; ordinary conforming use does not. Exceptions expire and appear in the risk register. Governance preserves enterprise protection without placing every release in a security meeting.

### Connections

[SARCH-081](081-conway-s-law-and-team-structures.md) provides organizational dependency analysis and [SARCH-082](082-team-topologies-and-architecture.md) provides responsibility and interaction patterns. [SARCH-084](../ROADMAP.md) next develops standards, principles, and guardrails as governance instruments.

## Governing Question

Architecture governance is not a committee, template, framework purchase, or approval stage. It is the allocation and exercise of authority over architectural direction and consequential decisions. A useful model answers: who sets direction, who may decide what, under which constraints, using which evidence, who must be consulted, who monitors consequences, and where disagreement or exceptional risk goes.

The design problem is asymmetric. Some local decisions are reversible and best made by teams with immediate context. Other choices create enterprise-wide security exposure, irreversible data commitments, safety hazards, supplier lock-in, or interoperability obligations. Centralizing everything creates delay and context loss; decentralizing everything creates uncontrolled shared consequence. Governance maps decision classes to appropriate authority instead of choosing one ideology.

## Why This Matters

Architecture crosses budgets, products, data, operations, risk, and time. Teams can optimize their services while creating incompatible identities, duplicated policy, systemic failure, or unowned lifecycle obligations. Conversely, a central board can optimize diagram uniformity while delaying users, forcing poor local fits, and becoming accountable for decisions it cannot observe in operation.

ISO/IEC 38500:2024, checked 2026-09-06, addresses governance of current and future IT use and distinguishes governance direction and accountability from management activity [1]. Its official revision material emphasizes direction, capability, policy, delegation, performance, accountability, and stakeholder engagement [2]. These concepts apply beyond software architecture, but they clarify why an architecture function cannot itself replace legitimate organizational governance.

NIST CSF 2.0 similarly makes Govern an explicit function around organizational context, risk strategy, roles and authorities, policy, oversight, and supply chains while remaining outcome-oriented rather than prescribing one implementation [4]. The lesson is structural: technical decisions operate inside organizational purpose and risk authority.

## Prerequisites and Retrieval

Retrieve stakeholder, concern, governing body, authority, accountability, responsibility, delegation, management, risk, uncertainty, consequence, reversibility, blast radius, assurance, independence, policy, control, standard, principle, guardrail, exception, evidence, audit, decision record, portfolio, domain, federation, escalation, and lifecycle.

SARCH-061 through SARCH-070 provide trade-off, risk, evidence, and review methods. SARCH-081 and SARCH-082 provide socio-technical boundaries. This chapter governs who decides and how the system remains accountable. SARCH-084 through SARCH-090 develop instruments and operating practices. It does not provide legal advice or displace corporate, public, clinical, safety, financial, privacy, labor, or regulatory authority.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish governance, management, advice, review, assurance, and execution;
2. classify architecture decisions by consequence, scope, reversibility, and context;
3. compare centralized, federated, delegated, embedded, and automated models;
4. specify a complete decision-right record;
5. place decisions at the least centralized competent authority;
6. design proportional review and escalation;
7. preserve independent assurance where consequence requires it;
8. integrate evidence into delivery rather than final gates;
9. measure governance outcomes without approval-count vanity metrics; and
10. evolve governance safely as architecture and organizational capability change.

## Core Exposition

**Distinguish governance from management.** A governing authority sets purpose, direction, risk tolerance, delegation, accountability, and oversight. Management plans, builds, operates, and improves within that framework. Architecture teams support both by framing decisions, supplying evidence, facilitating trade-offs, and monitoring architectural consequences. They govern only where legitimate authority has been explicitly assigned.

An architecture review can advise a product owner, approve a regulated decision under delegation, or assure conformance for a risk authority. These are different acts. Record which one applies. Ambiguous “sign-off” lets management claim approval while reviewers claim advice.

**Inventory decision domains.** Begin with recurring choices: public exposure, identity, cryptography, data authority, retention, interoperability, service objectives, recovery, supplier dependency, platform capability, language/runtime use, shared protocols, safety mechanisms, and exceptions. Include lifecycle decisions—migration, deprecation, and retirement—not just creation.

For each class, identify affected stakeholders, scope, maximum consequence, reversibility, time criticality, expertise, information location, cross-domain effect, governing obligation, and evidence. Do not start by copying the current committee structure; it may be the defect.

**Use subsidiarity with safeguards.** Place a decision as close as practical to the work and consequences, provided the decision maker has legitimate authority, competence, information, capacity, and feedback, and can preserve shared obligations. Escalate when one condition fails or the consequence exceeds the delegation envelope.

Locality is not automatically decentralization. A team might have technical expertise but lack authority to accept privacy risk. A board might have formal authority but lack operational evidence. The governance design must connect both without converting all work into central tickets.

**Centralize narrowly.** Central governance fits decisions whose consequences are shared, irreversible, legally reserved, systemically coupled, or dependent on scarce independent expertise. Examples may include root identity, enterprise data classification, regulated safety acceptance, public cryptographic policy, or a shared irreversible acquisition.

Centralization should own the minimum necessary decision class. A central identity authority can set trust and credential rules without selecting every application's UI library. A safety authority can define evidence and acceptance without implementing every control. Narrow scope reduces queues and preserves local context.

**Federate coherent domains.** Federated governance gives domains real authority under shared outcomes, vocabulary, interfaces, minimum evidence, and escalation. It is neither central consultation nor uncontrolled decentralization. Representatives must be empowered by their domains; shared decisions need a rule stronger than endless consensus.

Federation fits semantic or architectural concerns that span autonomous domains but require local interpretation. Define which matters are local, bilateral, collective, and reserved. Specify conflict resolution, funding, records, and response time. A forum with no authority or follow-through is a discussion group, not governance.

**Delegate explicit envelopes.** Delegation states permitted scope, constraints, evidence, reporting, expiry or review, and escalation. Delegating a decision does not remove the delegator's duty to monitor whether the arrangement works. The recipient needs resources and information, not just accountability.

An envelope might allow teams to select a managed datastore when data class, region, recovery, encryption, and capacity fit declared bounds. Out-of-envelope use triggers specialist review. This converts repeatable low-risk decisions into local work while preserving visibility and risk authority.

**Embed governance in delivery.** Early threat modeling, architecture decision records, contract tests, deployment policies, provenance, fitness functions, and operational evidence make governance continuous. Embedded expertise can help teams interpret policy before design hardens. A final board meeting cannot cheaply repair an incompatible data model or unsafe trust boundary.

Embedded does not mean self-certification for every consequence. Preserve separation where independent challenge or acceptance is needed. The implementer can generate evidence; an authorized independent role may still need to evaluate it.

**Automate only decidable portions.** Machines can check declared regions, versions, signatures, dependency policy, schema compatibility, encryption configuration, topology constraints, or evidence presence. They cannot infer whether a stakeholder concern is missing, an exception is ethically acceptable, or residual risk should be accepted unless that judgment has genuinely been encoded—and many should not be.

Every automated guard states input authority, rule version, applicability, failure behavior, override authority, audit trail, and limitations. A passing check proves conformance to encoded rules on observed inputs, not architectural fitness or legal compliance.

**Make review proportional.** Consider consequence, uncertainty, reversibility, novelty, shared blast radius, evidence strength, and time criticality. A reversible local experiment may need peer review and monitoring. A new cross-border identity authority may need security, privacy, legal, operations, and executive risk acceptance.

Risk-based review is not “skip documentation when fast.” It changes the kind and depth of evidence. Emergency paths must be preauthorized, observable, time-bounded, and followed by correction and learning.

**Govern exceptions as decisions.** An exception record names rule, scope, owner, rationale, consequence, compensating controls, affected stakeholders, evidence, expiry, removal work, and acceptance authority. Expiry is not automatic deletion: it is a forced decision to close, extend with new evidence, or change the rule.

Repeated similar exceptions indicate a defective standard, missing platform capability, unrealistic delegation, or deliberate risk accumulation. Analyze the population. Never normalize silent nonconformance because individual exceptions appear small.

**Close feedback loops.** Decision makers need consequences: delivery delay, incidents, cost, user harm, adoption, exceptions, recovery, and new evidence. An approval body disconnected from operation cannot learn whether its choices work. Assign monitoring and revisit triggers in the decision record.

**Measure governance as a system.** Useful measures include decision latency by class, rework caused by late discovery, exception age, repeated exception clusters, unowned risks, evidence quality, incident contribution, appeal outcomes, team burden, outcome improvement, and stakeholder trust. Approval count, meeting count, document count, or policy pass rate alone rewards activity and can hide harm.

**Evolve the model.** Governance should change as teams gain capability, platforms encode repeatable decisions, risks emerge, laws change, and architecture becomes more or less coupled. Review delegation boundaries and authority maps. Move mature decisions outward; centralize only newly shared consequence; retire obsolete forums and controls.

## Definitions and Notation

Let decision class $D=(S,A,E,C,R,X)$. Scope $S$ states included systems and choices. $A$ is the one accountable authority. Envelope $E$ states delegated permissions and constraints. $C$ names consultation and evidence. $R$ names monitoring, review cadence, and revisit triggers. $X$ names escalation, appeal, emergency, and exception paths.

For a decision instance $d$, define consequence vector $q(d)$ across relevant dimensions such as safety, security, privacy, financial, operational, accessibility, legal, and interoperability. Define reversibility $r(d)\in[0,1]$, where higher values mean more practically reversible within the stated horizon. These observations inform review; they are not commensurable unless an explicit decision model justifies aggregation.

A **governing body** is the person or group ultimately accountable for organizational governance. A **decision forum** is a mechanism that may advise or exercise delegated authority. **Assurance** supplies justified confidence through evidence and evaluation. **Compliance** is conformity to specified requirements; it is not identical to value, safety, or architectural quality.

## Mechanisms, Invariants, or Proof Structure

### Complete-delegation invariant

No delegated decision is valid unless scope, recipient authority, constraints, required evidence, monitoring, and escalation are explicit. Responsibility without decision authority and resources is not delegation.

### Non-compensation invariant

A severe breach in a non-compensable obligation—such as an applicable safety constraint or legal prohibition—cannot be offset by delivery speed or aggregate benefit. The legitimate authority must determine applicability and acceptance; an architecture score cannot.

### Traceable-accountability invariant

For every material outcome, one can trace governing direction to decision class, authorized instance, implementation evidence, observed consequence, and review. Missing traceability triggers investigation; it does not prove misconduct or technical failure by itself.

### Executable routing policy

This finite router illustrates how declared properties can route decisions. It is a schematic policy implemented as executable code, not a universal governance model.

<!-- bijux-verify: {"id":"governance-routing-policy","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"cache size: delegated\nshared identity root: centralized\ndomain vocabulary: federated\nnovel encryption: escalate-specialist\n","stderr":""}} -->
```python
def route(*, shared_blast, irreversible, cross_domain, novel_specialist):
    if novel_specialist:
        return "escalate-specialist"
    if shared_blast and irreversible:
        return "centralized"
    if cross_domain:
        return "federated"
    return "delegated"

cases = {
    "cache size": dict(shared_blast=False, irreversible=False,
                       cross_domain=False, novel_specialist=False),
    "shared identity root": dict(shared_blast=True, irreversible=True,
                                 cross_domain=True, novel_specialist=False),
    "domain vocabulary": dict(shared_blast=False, irreversible=False,
                              cross_domain=True, novel_specialist=False),
    "novel encryption": dict(shared_blast=True, irreversible=False,
                             cross_domain=True, novel_specialist=True),
}
for name, facts in cases.items():
    print(f"{name}: {route(**facts)}")
```

The priority order is policy. Different legitimate contexts can choose differently. The router omits law, evidence quality, emergency, and human consequence, so it can only propose a route for the declared fixture.

### Proposition: approval count is not governance effectiveness

No monotone inference from number of approvals to governance effectiveness is valid without additional assumptions. **Counterexample:** System A centrally approves 1,000 routine changes after long queues while missing one shared data-authority defect. System B delegates routine conforming changes and centrally reviews ten consequential decisions, detecting that defect. A has more approvals but can have worse delay, risk, and outcomes. Therefore count alone cannot order effectiveness.

## Alternatives and Trade-Offs

**Centralized versus delegated.** Centralization offers consistency and concentrated expertise but loses context and creates queues. Delegation improves speed and consequence feedback but needs clear envelopes, capability, and monitoring.

**Federated versus uniform.** Federation respects domain authority and variation; it costs coordination and conflict resolution. Uniform rules simplify interoperability but can force poor fits or encode central blind spots.

**Board review versus embedded practice.** Boards provide broad challenge and visible authority. Embedded practice finds issues earlier. Combine continuous evidence with reserved decision points rather than treating them as exclusive.

**Manual judgment versus automation.** Human judgment handles ambiguity and values; it is slow and inconsistent. Automation is repeatable and scalable within encoded scope; it can entrench a bad rule. Automate established predicates and preserve governed interpretation and appeal.

**Ex ante approval versus ex post monitoring.** Prior approval helps prevent irreversible harm. Monitoring preserves speed for reversible bounded choices. Match mechanism to consequence, detection, and recovery.

**Consensus versus accountable decision.** Consensus can build legitimacy and information sharing. It can also suppress disagreement or make nobody accountable. Define consultation and a final authority, including dissent records and appeal.

## Failure Modes and Misconceptions

1. **“The architecture board is governance.”** A board is only one mechanism under legitimate authority.
2. **“Important means centralized.”** Importance alone does not establish shared or irreversible consequence.
3. **“Delegation transfers accountability completely.”** The delegator retains oversight duties.
4. **“Federated means everyone decides everything.”** Decision domains and escalation must be explicit.
5. **“Consensus removes risk.”** It can hide ownership and silence minority expertise.
6. **“Advice equals approval.”** The action and authority must be recorded.
7. **“Compliance proves good architecture.”** It proves only conformity to applicable requirements and evidence.
8. **“Automation removes judgment.”** It relocates judgment into rules, inputs, applicability, and override.
9. **“A green policy check proves legality.”** Encoded scope and authoritative interpretation remain limited.
10. **“Every exception is failure.”** A governed exception can be the correct response to an edge case.
11. **“Expired means resolved.”** Expiry forces review; closure needs evidence.
12. **“More approvals mean stronger governance.”** Counts can reward delay and low-value activity.
13. **“Architects accept every technical risk.”** Acceptance belongs to the authority accountable for consequences.
14. **“Local teams have all relevant context.”** Shared and affected stakeholders may be outside the team.
15. **“Central experts have all relevant context.”** Operational and user evidence may be local.
16. **“Emergency change suspends governance.”** Preauthorized emergency governance changes route and timing, not accountability.
17. **“Decision records freeze decisions.”** They preserve rationale and revisit triggers.
18. **“Governance is neutral administration.”** It distributes power, burden, voice, and risk and requires ethical scrutiny.

## Worked Examples

### Example 1

**Situation.** An architecture board reviews every library upgrade.

**Reasoning.** Most upgrades are reversible and local within supported versions. Delegate them under provenance, vulnerability, test, and rollback rules. Reserve review for unsupported runtimes, shared protocol changes, or nonconformance. Monitor exceptions and incidents.

**Conclusion.** Narrow delegation removes routine queueing while preserving consequential escalation.

### Example 2

**Situation.** Three domains disagree on the meaning of “active customer.”

**Reasoning.** A central universal definition may erase legitimate context; isolated definitions break enterprise use. Federate: each domain owns contextual meaning, a semantic forum owns mappings and shared claims under empowered representatives, and unresolved enterprise reporting conflicts escalate to the accountable reporting authority.

**Conclusion.** Federated governance can preserve contextual truth and governed interoperability.

### Example 3

**Situation.** A product team requests a new managed database inside approved data-class, region, encryption, recovery, and cost bounds.

**Reasoning.** The platform validates machine-checkable predicates and records evidence. The team owns schema, workload, data truth, and application recovery. No board is needed. If residency or recovery falls outside the envelope, route to the correct risk authority.

**Conclusion.** Automated assurance can operationalize delegation without becoming universal risk acceptance.

### Example 4

**Situation.** A review forum recommends against a design, but a product executive proceeds and later says “architecture approved it.”

**Reasoning.** The forum's act was advisory. The record must name the executive as decision and risk owner, the advice, dissent, evidence, and revisit trigger. If the forum was intended to approve, delegation was defective and must be corrected.

**Conclusion.** Explicit decision acts prevent advice, approval, and accountability from being blurred.

### Example 5

**Situation.** Teams submit forty similar exceptions to an obsolete runtime rule.

**Reasoning.** Review the population, not each case alone. The rule may be unrealistic, migration capability unfunded, or platform support missing. Quantify exposure and expiry; fund a shared migration or revise the standard with legitimate authority. Do not renew exceptions silently.

**Conclusion.** Exception clusters are governance feedback about systemic design.

### Example 6

**Situation.** A safety-critical control passes all automated architecture checks.

**Reasoning.** The checks establish only encoded conformance. Safety analysis, hazard controls, independence, configuration, operational evidence, and authorized acceptance remain. Route the evidence to the safety authority; never let green CI accept residual safety risk.

**Conclusion.** Automated evidence supports but cannot impersonate non-delegated assurance and acceptance.

### Example 7

**Situation.** A federated council requires unanimity from twelve domains and takes months.

**Reasoning.** Classify decisions as local, bilateral, collective, and reserved. Use time-bounded consultation and an empowered accountable authority for collective decisions, with dissent and appeal. Consensus may remain desirable for selected irreversible standards but is not the default.

**Conclusion.** Federation needs executable decision rules, not permanent universal consensus.

### Example 8

**Situation.** During an incident, a team bypasses the normal schema-review route.

**Reasoning.** Invoke a preauthorized emergency envelope: named incident authority, bounded scope, compatibility and backup evidence, audit log, time limit, and rollback. After stabilization, reconcile records, evaluate consequence, repair the durable path, and close or formalize any exception.

**Conclusion.** Emergency governance accelerates decisions while preserving traceability and accountability.

### Example 9

**Situation.** Governance reports 98% policy pass rate, yet teams report growing delay and users experience outages.

**Reasoning.** Pass rate measures encoded conformance, not fitness. Add decision latency, late rework, exception age, incident contribution, recovery, support burden, user outcome, and qualitative evidence. Check whether teams game declarations or the rules omit critical dependencies.

**Conclusion.** Governance must be evaluated by consequences and burden, not green-check volume.

### Example 10

**Situation.** A public health data exchange spans hospitals, agencies, laboratories, vendors, and researchers.

**Reasoning.** No software architecture board has universal authority. Federate semantic and interoperability decisions among empowered authorities; reserve public-health direction, clinical safety, privacy, research, and statutory decisions to legitimate bodies. Delegate technical conformance within explicit envelopes, automate testable profiles, maintain independent assurance, publish appeals, and involve affected communities. Treat emergency access as governed, observable, and temporary.

**Conclusion.** Multi-enterprise architecture governance is an authority federation, not centralized technical control.

## Cross-Program Connections

- [Software Engineering Patterns](../../11-software-engineering-patterns/ROADMAP.md) supplies technical alternatives; governance determines decision rights, not a preferred pattern catalog.
- [Software Delivery and Reliability Engineering](../../14-software-engineering-software-delivery-and-reliability-engineering/ROADMAP.md) owns operational evidence, incidents, and change mechanisms embedded in governance.
- [Data Architecture Engineering](../../20-data-architecture-engineering/ROADMAP.md) owns semantic authority, data governance, and federation for data decisions.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) owns threat and control mechanisms; risk acceptance remains with legitimate authorities.
- [Systems Engineering](../../26-systems-engineering/ROADMAP.md) owns lifecycle, assurance, safety, supplier, and whole-system authority relationships.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md) owns self-service capabilities that can encode delegated envelopes and evidence.

## References

1. ISO/IEC, [ISO/IEC 38500:2024 — Information Technology — Governance of IT for the Organization](https://www.iso.org/standard/81684.html), 3rd ed., published February 2024. Official current record checked 2026-09-06.
2. ISO/IEC JTC 1/SC 40, [“Differences between ISO/IEC 38500:2015 and ISO/IEC 38500:2024”](https://committee.iso.org/sites/jtc1sc40/home/projects/wg-1/published-wg1/content-left-area/isoiec-sc-40-wg-1-develops-the-s/white-paper-on-the-differences-b.html), 2024. Official explanation of revised governance outcomes and framework.
3. ISO, [ISO 37000:2021 — Governance of Organizations — Guidance](https://www.iso.org/standard/65036.html), 2021. Organization-wide governance principles and outcomes.
4. NIST, [*Cybersecurity Framework 2.0*](https://doi.org/10.6028/NIST.CSWP.29), NIST CSWP 29, February 26, 2024. Official outcome framework including Govern; checked 2026-09-06.
5. The Open Group, [*TOGAF Standard, 10th Edition*](https://www.opengroup.org/togaf), 2022. Official framework record and configurable enterprise-architecture guidance; checked 2026-09-06.
6. ISACA, [*COBIT 2019 Framework: Governance and Management Objectives*](https://www.isaca.org/resources/cobit), 2018–2019. Official distinction and objective model; current resource checked 2026-09-06.
7. ISO/IEC/IEEE, [ISO/IEC/IEEE 42020:2019 — Architecture Processes](https://www.iso.org/standard/68982.html), 2019. Architecture lifecycle processes; official record checked 2026-09-06 and noted as published/to be revised.
8. ISO/IEC/IEEE, [ISO/IEC/IEEE 42030:2019 — Architecture Evaluation Framework](https://www.iso.org/standard/68983.html), 2019. Evaluation concepts and evidence framing.
9. Philippe Kruchten, Patricia Lago, and Hans van Vliet, [“Building Up and Reasoning About Architectural Knowledge”](https://doi.org/10.1007/978-3-540-30966-1_4), QoSA 2006. Architecture knowledge and decision rationale.
10. Michael Nygard, [“Documenting Architecture Decisions”](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions), 2011. Origin of the widely used concise ADR form.
11. Len Bass, Paul Clements, and Rick Kazman, *Software Architecture in Practice*, 4th ed., Addison-Wesley, 2021. Stakeholders, quality attributes, evaluation, and architecture competence.
12. John Carver, *Boards That Make a Difference*, 3rd ed., Jossey-Bass, 2006. Policy-governance reasoning used cautiously for direction, delegation, and accountability distinctions.

## Exercises

### Exercise 1

Distinguish governance, management, advice, approval, assurance, and implementation using one architecture decision.

### Exercise 2

Complete $D=(S,A,E,C,R,X)$ for ordinary selection of an internal message broker within an approved platform.

### Exercise 3

A central board takes three weeks to approve reversible service configuration, while shared identity changes receive the same review. Redesign the routing and evidence model.

### Exercise 4

Compare centralized and federated governance for enterprise data semantics. State when each is justified and propose conflict resolution.

### Exercise 5

Design architecture governance for an autonomous-vehicle ecosystem spanning manufacturer, mapping provider, cloud operator, repair network, road authority, regulator, insurers, emergency services, and vehicle owners. Preserve legitimate authority and independent assurance.

## Answers to the Exercises

### Answer 1

For a new public identity provider, governance sets trust direction, risk tolerance, and delegation. Management plans procurement and migration. Architects and specialists may advise on options. An authorized security or enterprise authority approves the bounded trust decision. Assurance independently evaluates required evidence. Product, platform, and supplier teams implement and operate it. One person may occupy several roles only where independence is not required; the record must state which act and authority applies.

### Answer 2

$S$: supported internal event workloads and approved broker offerings. $A$: the product/domain team accountable for workload behavior, under delegation from the platform or technology authority. $E$: approved products, regions, data classes, identity, encryption, retention, availability, recovery, capacity, and cost bounds. $C$: workload evidence, data owner, security classification, platform conformance, recovery test, and affected consumers. $R$: telemetry, cost, incidents, compatibility, quarterly suitability, and triggers for volume, exposure, or provider change. $X$: platform support, security/data/reliability specialist route, exception authority, appeal, and emergency path. A strong answer names both local accountability and the authority that defined and monitors the envelope.

### Answer 3

Delegate reversible configuration when it stays within version, capacity, security, recovery, and cost bounds. Encode testable predicates in platform policy, retain peer review and telemetry, and sample outcomes. Route out-of-envelope or repeatedly failing cases to specialists. Reserve centralized review for the shared identity trust root because its cross-system blast radius, authority, migration, and reversibility differ. Require identity threat, privacy, compatibility, recovery, supplier, and stakeholder evidence and name acceptance authority. Measure latency, late rework, incidents, exceptions, and burden by class. The redesign is risk-classification plus feedback, not merely a faster board.

### Answer 4

Centralize when one definition is legally or operationally authoritative across contexts—for example, a governed enterprise identifier allocation rule—or when inconsistency creates an unacceptable shared consequence. Federation fits concepts whose meanings legitimately vary by domain but must interoperate. Domains own contextual definitions; an empowered semantic forum owns shared claims and mappings; machine-readable contracts and tests expose differences. Define voting or accountable decision rules, time limits, dissent, funding, and escalation to the authority accountable for the enterprise outcome. Do not force consensus or let a central glossary overwrite source authority.

### Answer 5

Treat the ecosystem as a federation of legal and operational authorities. The manufacturer governs vehicle architecture and product safety within regulatory obligations; road and regulatory bodies retain public and approval authority; mapping and cloud providers own contracted service boundaries; repair networks own authorized maintenance evidence; emergency services own response decisions; owners and affected road users require meaningful representation and remedy. Establish shared interface, identity, update, provenance, incident, vulnerability, mapping-quality, telemetry, recall, and recovery decision domains with explicit accountable authorities and escalation. Delegate conforming technical choices inside certified/configured envelopes; automate only testable predicates and retain versioned evidence. Preserve independent safety and cybersecurity assurance, regulator access, supplier audit, field monitoring, appeal, emergency authority, and coordinated recall. No commercial architecture forum may accept public safety, legal, insurance, or individual rights risk outside its mandate, and proprietary telemetry must not erase privacy, due process, accessibility, or human oversight.
