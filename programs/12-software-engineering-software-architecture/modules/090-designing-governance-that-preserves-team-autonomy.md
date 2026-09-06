---
module_id: SARCH-090
program: Software Engineering: Software Architecture
level: 2
module_number: 90
title: Designing Governance That Preserves Team Autonomy
status: complete
last_verified: 2026-09-06
---

# Designing Governance That Preserves Team Autonomy

## One-Page Review

### Governing question

How can an organization give teams real authority and capability to make timely local architecture decisions while preserving shared outcomes, reserved obligations, interoperability, learning, and accountability?

### Essential definitions

- **team autonomy** is bounded authority and practical capability to decide, act, observe consequences, and correct course for an owned outcome;
- a **decision domain** is the subject, scope, resources, and consequences over which an owner can decide;
- a **delegation envelope** states outcomes, granted decisions, constraints, capabilities, evidence, feedback, and escalation;
- a **reserved decision** remains with an organizational, legal, safety, security, privacy, financial, contractual, public, or other legitimate authority;
- an **externality** is a material consequence imposed outside the deciding team's owned scope;
- **subsidiarity** places decisions at the lowest level competent and authorized to manage their consequences;
- a **guardrail** bounds a property or action while preserving meaningful choice inside the safe region;
- a **platform** supplies supported capabilities that reduce repeated complexity rather than merely centralizing tools;
- **assurance** is justified confidence based on evidence, not an approval ceremony;
- **reversibility** is the practical ability to restore an acceptable state inside relevant time and consequence bounds;
- **local optimization** improves a team measure while potentially worsening a shared outcome;
- **psychological safety** concerns interpersonal risk and voice; it supports but is not identical to decision authority.

### Central model, mechanism, or theorem

Model an autonomy-preserving governance envelope as

$$
G=(Y,D,B,K,E,F,X,L),
$$

where $Y$ is owned outcomes, $D$ delegated decisions, $B$ boundaries and reserved authority, $K$ capabilities and resources, $E$ required evidence, $F$ consequence feedback, $X$ exception and escalation paths, and $L$ lifecycle. A team is not autonomous merely because approval is absent. It needs authority, competence, resources, access, supported mechanisms, and observability to act and recover within $G$.

### Critical invariants

- every outcome and decision class has an accountable authority;
- delegated decisions state scope, constraints, resources, evidence, and escalation;
- decisions stay local only when material consequences are locally observable and manageable;
- reserved authority is explicit and cannot be inferred from technical ownership;
- standards define the minimum shared semantic, trust, safety, and operational core;
- guardrails reject only within declared evidence and return actionable reasons;
- platforms reduce consumer burden without becoming mandatory through hidden dependency or funding power;
- reversible, bounded experiments receive faster paths than irreversible shared changes;
- teams can contest facts, appeal decisions, and request conforming alternatives or exceptions;
- feedback includes outcomes, delay, burden, incidents, near misses, exceptions, and affected voices;
- governance artifacts, delegations, and controls have version, review, and retirement paths;
- autonomy is evaluated through safe outcomes and decision capability, not approval avoidance alone.

### Common failures

Common failures include declaring “you build it, you run it” without authority or resources; removing approvals while keeping central access queues; requiring central review of reversible local changes; allowing teams to redefine shared identities; standardizing every implementation; using a platform monopoly as autonomy; treating self-service as unsupported self-rescue; confusing consultation with consent; delegating blame but not budgets; using metrics to rank teams; suppressing dissent in the name of speed; routing every novel case as an exception; and assuming identical governance fits every consequence.

### Compact example

An orders team owns fulfillment outcomes. Its envelope delegates internal data structures, algorithms, deployment timing, and capacity within cost, recovery, privacy, and interface bounds. A platform supplies identity, deployment, telemetry, and recovery evidence. The team can ship a reversible cache change locally after automated checks. A change to the shared order event requires affected consumers; a new retention purpose routes to privacy authority; an unrecognized recovery mechanism uses alternative compliance. The team observes customer and operational consequences and can rollback. Governance samples outcomes and evolves the envelope instead of approving every release.

### Connections

[SARCH-083](083-architecture-governance-models.md) establishes governance and delegation. [SARCH-085](085-golden-paths-and-paved-roads.md) and [SARCH-089](089-managing-exceptions-and-technical-risk.md) supply supported paths and bounded departures. [SARCH-091](../ROADMAP.md) next applies judgment where regulation and safety constrain autonomy more strongly.

## Governing Question

Architecture governance must do two things often framed as opposites: let people closest to a problem use local knowledge, and ensure local choices do not silently transfer harm or destroy shared capabilities. Central approval can make responsibility appear clear while delaying feedback and concentrating blind spots. Unbounded local choice can be fast while fragmenting semantics, trust, recovery, and accountability.

The design target is neither maximum decentralization nor minimum process. It is the shortest legitimate decision path for each consequence. That requires explicit delegation, usable capabilities, shared evidence, appeal, and learning. Autonomy is a property of a socio-technical decision system, not a slogan about teams.

## Why This Matters

ISO/IEC 38500:2024 is the current third edition of the governance-of-IT standard and addresses effective, efficient, and acceptable current and future use of IT by organizations [1]. ISO/IEC/IEEE 42020:2019 defines governance, management, architecting, and enablement processes across architecture lifecycles; ISO confirmed it in 2025 and marks it to be revised [2]. Neither mandates an architecture review board or a team topology. They help distinguish governing direction and monitoring from local management and execution.

NIST CSF 2.0 added Govern as a first-class function and emphasizes organizational context, risk strategy, roles, policy, oversight, and supply-chain risk; it states outcomes rather than prescribing one implementation [3], [4]. This supports outcome-oriented envelopes, but a security framework does not define all product, labor, safety, or public authority.

Parnas's information-hiding criterion connects modularity with hiding design decisions likely to change [7]. Conway's observation connects communication structures and designs [8]. These works explain why decision and system boundaries interact, not why any manager or team has legitimate authority. Team Topologies supplies practitioner language for stream-aligned ownership, platform products, enabling teams, specialist subsystems, and interaction modes [5]. The model must be tested against context rather than used as a reorganization recipe.

## Prerequisites and Retrieval

Retrieve governance, direction, oversight, management, authority, accountability, responsibility, delegation, autonomy, capability, competence, decision domain, envelope, externality, subsidiarity, reserved authority, conformance, guardrail, platform, assurance, evidence, reversibility, escalation, appeal, exception, feedback, cognitive load, psychological safety, outcome, and local optimization.

SARCH-081 and SARCH-082 supply socio-technical graphs and topology concepts. SARCH-083 through SARCH-089 supply governance models, standards, guardrails, paved roads, reference architectures, forums, federation, and exception management. This module synthesizes those instruments into one autonomy-preserving operating design. It does not prescribe corporate structure, employment policy, legal delegation, clinical authority, or safety certification.

## Learning Objectives

After completing this module, you should be able to:

1. define team autonomy as bounded authority plus capability rather than absence of review;
2. construct a delegation envelope for an owned outcome;
3. distinguish delegated, shared, reserved, and escalated decisions;
4. route decisions by consequence, coupling, reversibility, and evidence;
5. design minimum shared standards, guardrails, platforms, and evidence;
6. expose access, budget, expertise, and operational dependencies that create false autonomy;
7. design consultation, objection, appeal, exception, and emergency paths;
8. measure governance latency and burden without ranking teams;
9. detect local optimization and cumulative system risk; and
10. evolve delegation as capability, architecture, and obligations change.

## Core Exposition

**Start with owned outcomes.** Name customer, mission, operational, financial, accessibility, security, privacy, safety, and ecosystem outcomes the team can influence and observe. “Own service A” is a component boundary, not necessarily an outcome. Trace work and consequences across design, build, run, support, recovery, retirement, and learning.

**Map actual decision rights.** Inventory who may decide, and who controls repositories, environments, data, identities, budgets, suppliers, production access, incident action, standards, and risk acceptance. Compare formal delegations with real queues and vetoes. A chart can say “autonomous product team” while five central groups hold every capability required for a production change.

**Define a decision domain.** List recurring choices and classify them as delegated, bilateral, collective, or reserved. Internal algorithm selection may be delegated. A producer-consumer contract may be bilateral. Shared identity semantics may be collective. A statutory retention interpretation remains reserved. Scope by consequence rather than title or organizational rank.

**Write the delegation envelope.** For each class, record owned outcomes, granted authority, constraints, required consultation, capabilities and budget, evidence, observation, escalation, exception, and review. Delegation includes permission to act and means to discharge responsibility. “The team is accountable for availability” is incoherent if it cannot change capacity, dependencies, recovery, or on-call conditions.

**Apply subsidiarity with competence.** Place a decision at the lowest level that can understand, act on, observe, and recover from its material consequences. Move it upward or sideways when consequences cross domains or authority. Build capability so decisions can later move outward. Subsidiarity is not “teams decide”; it is a conditional placement test.

**Minimize the shared core.** Standardize only what shared outcomes require: identity, protocol semantics, data meaning, interoperability, security boundaries, safety constraints, evidence, compatibility, and operational behavior. Preserve local algorithms, internal models, workflow, and tooling where diversity does not export unmanaged cost. Profiles and mappings often preserve truth better than one universal implementation.

**Make the conforming path easy.** Paved roads combine documentation, templates, automation, supported components, observability, recovery, and service ownership. Their power should come from consumer value and demonstrated outcomes. If an alternative is possible only through executive escalation while the platform gets guaranteed funding, “voluntary” adoption is fiction. Publish constraints, service levels, contribution, exit, and alternative routes.

**Use guardrails near action.** Encode established predicates at design, build, admission, or runtime points where correction is cheap and evidence is authoritative. Return pass, fail, or inconclusive with rule, observation, consequence, and remediation. A gate that blocks without an owner converts governance cost into team delay. Novel judgment remains human and appealable.

**Route by reversibility and blast radius.** A reversible local experiment inside the envelope should have a short path and observable rollback. An irreversible change to shared data, trust, public behavior, or safety needs broader authority and evidence. Reversibility includes detection and recovery time; a rollback command is useless if harm is immediate or lost data cannot be reconstructed.

**Separate advice, consultation, assurance, and approval.** Communities and architects advise. Affected parties are consulted or share a contract decision. Assurance evaluates evidence. Approval exercises authority. Combining them in vague “architecture sign-off” makes a recommendation feel mandatory and lets authorities hide behind expert opinion. Publish which interaction is happening.

**Enable teams instead of accumulating review.** If a team lacks threat modeling, recovery design, performance analysis, or domain knowledge, pair with an enabling capability and define exit evidence. If work is irreducibly specialist, provide a supported service or clear shared decision. Permanent mandatory consultation for routine work signals a missing capability, unclear rule, or bad boundary.

**Preserve objection and appeal.** Autonomy includes the ability to challenge an incorrect rule, stale fact, inaccessible process, harmful default, or provider decision. Objections name mechanism and consequence; authorities respond. Protect dissent and record unresolved concerns. Psychological safety improves the chance concerns surface, but it cannot substitute for decision rights or remedies [10].

**Design exception and emergency paths.** An exception is not permission to negotiate every rule. It is a scoped, evidenced, owned, expiring departure. Emergency authority is predeclared, narrow, observable, and reconciled. Both paths teach governance where standards and platforms fail. If the ordinary route cannot handle legitimate variation, fix the route.

**Expose dependencies and power.** Platforms, budget owners, senior architects, security specialists, and shared data owners exercise de facto governance through access and defaults. Make service contracts, funding, priority, escalation, and consumer voice explicit. A platform backlog consumers cannot influence is a central queue even if its API is self-service.

**Close consequence feedback.** Teams need customer, operational, cost, security, privacy, accessibility, dependency, and recovery evidence at a useful cadence. Governing authorities need aggregate concentration, incident, exception, and burden evidence. Feedback travels both ways: direction and tolerance outward, results and changed context inward.

**Measure decision flow, not theater.** Trace request-to-decision time, active work, wait, rework, late discovery, appeal, exception age, guardrail false results, platform task success, incidents, recovery, cognitive burden, and stakeholder outcomes. Segment by decision class and affected group. Approval count, deployment count, and meeting attendance cannot establish good governance.

**Evolve the envelope.** Review after incidents, material architecture change, new regulation, supplier change, persistent delay, exception clusters, control failures, or demonstrated capability. Move established decisions into local authority and automation; centralize newly shared or irreversible consequence; retire obsolete rules. Preserve versioned history so changed authority is reconstructable.

## Definitions and Notation

Let $G=(Y,D,B,K,E,F,X,L)$. $Y$ is the set of outcomes and accountable owners. $D$ maps recurring decisions to delegated domains. $B$ declares constraints, shared commitments, externalities, and reserved authority. $K$ supplies competence, budget, access, services, and operational capacity. $E$ specifies evidence and assurance. $F$ returns local and aggregate consequences. $X$ defines consultation, escalation, appeal, exception, and emergency. $L$ defines version, review, evolution, and retirement.

For decision $d$, let $A(d)$ be materially affected domains, $R(d)$ any reserved authority, $v(d)$ practical reversibility, $c(d)$ coupling, and $u(d)$ decision-relevant uncertainty. These are not necessarily scalar or commensurable. Routing is a policy over declared observations, not a theorem derived from team count.

A team has **nominal autonomy** when a document says it may decide. It has **effective autonomy** when authority, capability, resources, access, observability, and recovery are sufficient in practice. It has **unbounded discretion** when constraints are absent; that is not the target.

## Mechanisms, Invariants, or Proof Structure

### Authority-capability invariant

Every delegated responsibility is paired with sufficient decision authority, capability, resources, access, evidence, and escalation. If one is absent, supply it, narrow responsibility, or route the decision elsewhere.

### Consequence-boundary invariant

A decision remains local only while material consequences stay inside the team's owned and observable outcomes. A shared externality or reserved obligation changes the route even when implementation resides in one repository.

### Minimum-shared-core invariant

Every shared constraint traces to an outcome, authority, affected scope, evidence method, exception or appeal, and lifecycle. Constraints without this trace are candidates for removal; local choices without it remain local by default.

### Feedback-and-evolution invariant

Every governance route produces decision, implementation, and consequence evidence that can revise delegation, capability, rule, or platform. A process that only records approvals cannot learn whether its design works.

### Executable routing screen

<!-- bijux-verify: {"id":"autonomy-governance-router","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"cache policy: local-decision\nconsumer schema: shared-decision\nretention purpose: reserved-authority\nunknown recovery: clarify-evidence\nnovel reversible test: bounded-experiment\nwide irreversible change: governance-review\n","stderr":""}} -->
```python
def route(*, reserved, affected_domains, evidence_known,
          inside_envelope, reversible):
    if reserved:
        return "reserved-authority"
    if not evidence_known:
        return "clarify-evidence"
    if affected_domains > 1:
        return "shared-decision"
    if inside_envelope:
        return "local-decision"
    if reversible:
        return "bounded-experiment"
    return "governance-review"

cases = {
    "cache policy": (False, 1, True, True, True),
    "consumer schema": (False, 3, True, False, False),
    "retention purpose": (True, 1, True, False, False),
    "unknown recovery": (False, 1, False, False, False),
    "novel reversible test": (False, 1, True, False, True),
    "wide irreversible change": (False, 1, True, False, False),
}
for name, facts in cases.items():
    print(f"{name}: {route(reserved=facts[0], affected_domains=facts[1], evidence_known=facts[2], inside_envelope=facts[3], reversible=facts[4])}")
```

The router is a fictional first screen. Real routing needs legitimate authority, multidimensional consequences, affected people, detectability, time, uncertainty, dependency, and appeal.

### Proposition: removing approval is insufficient for autonomy

Suppose team $t$ no longer needs architecture approval, but only platform group $p$ can provision production capacity and $p$ has an unbounded queue. Team $t$ cannot execute its production decision without $p$. Therefore approval removal can coexist with no effective ability to act; it is insufficient to establish effective autonomy.

### Proposition: local autonomy does not guarantee a shared outcome

Two teams independently and legitimately reduce local storage by deleting replay history. A shared recovery objective requires at least one complete history. Each local metric improves, yet recovery becomes impossible. Thus local authority and local improvement do not compose into a guaranteed system outcome without a shared invariant.

## Alternatives and Trade-Offs

**Central approval versus delegated envelope.** Central review concentrates expertise and authority but adds queues and weakens local feedback. Delegation speeds routine decisions but needs clear outcomes, capability, monitoring, and escalation. Reserve central approval for legitimate shared or irreversible consequence.

**Rules versus principles.** Rules make repeated obligations clear and automatable but can freeze assumptions. Principles preserve judgment but can become slogans or discretionary power. Use rules for established bounds and principles for genuine trade-offs, with examples and appeal.

**Platform path versus local capability.** Platforms reduce repeated burden and increase consistency. They can also create lock-in, common failure, and central priority power. Preserve clear product responsibility, alternatives, contribution, portability where needed, and consumer evidence.

**Ex ante review versus ex post assurance.** Prior review helps prevent irreversible harm. Outcome monitoring preserves speed for reversible decisions. Combine early evidence and automated bounds with risk-based sampling and post-decision learning.

**Uniform versus contextual delegation.** Uniformity is simple and appears fair. Different domains have different consequences, competence, coupling, and authority. Contextual envelopes fit reality but need transparent criteria so variation does not become favoritism.

## Failure Modes and Misconceptions

1. **“Autonomy means no constraints.”** Useful autonomy operates inside legitimate outcome boundaries.
2. **“No approval means authority.”** Access, budget, capability, and dependencies may still block action.
3. **“Ownership means all risk can be accepted locally.”** Reserved and external consequences route elsewhere.
4. **“Every team should choose every tool.”** Shared semantics and lifecycle cost can justify standards.
5. **“One stack creates autonomy.”** Uniform implementation may reduce choice without reducing burden.
6. **“Self-service means self-support.”** A platform still owns service quality and escalation.
7. **“A platform is neutral.”** Defaults, access, funding, and backlog priority distribute power.
8. **“Consulted means consenting.”** Decision protocols must state authority and objection handling.
9. **“An architect's advice is approval.”** Expertise and authority are different roles.
10. **“Reversible means a rollback button exists.”** Detection, lost state, and recovery time determine reversibility.
11. **“Local metrics compose.”** Independent improvements can violate a shared invariant.
12. **“The same envelope is fair for every team.”** Consequence and capability differ.
13. **“Guardrail pass proves fitness.”** It proves only a declared predicate on evidence.
14. **“Few exceptions prove good governance.”** Hidden bypass or abandoned work may suppress requests.
15. **“More deployments prove autonomy.”** Frequency can coexist with trivial scope or unsafe change.
16. **“Psychological safety grants authority.”** Voice and formal decision rights are complementary.
17. **“Delegation is permanent.”** New coupling or obligation can change the appropriate route.
18. **“Centralization is always anti-autonomy.”** Shared services and reserved decisions can expand meaningful local capability.

## Worked Examples

### Example 1

**Situation.** An orders team wants to change an internal cache eviction policy.

**Reasoning.** Its envelope owns latency and cost, permits internal algorithms, and requires resource, reliability, security, and rollback evidence. No shared contract changes. The team runs checks, deploys gradually, observes results, and can reverse before material harm.

**Conclusion.** A reversible in-envelope decision stays local without an architecture meeting.

### Example 2

**Situation.** The same team removes a field consumed by billing and support.

**Reasoning.** Repository ownership does not contain the consequence. Route to an affected-domain contract decision with semantics, compatibility, migration funding, consumer evidence, rollout, and retirement. Unaffected domains need not approve.

**Conclusion.** Autonomy ends at unmanaged shared externality, not at a source-code boundary.

### Example 3

**Situation.** A service team can deploy without review but waits three weeks for a central production identity.

**Reasoning.** Map the dependency and decision. Provide a platform API with bounded identity profiles, automatic evidence, support, and escalation; delegate issuance inside the profile. Keep novel trust-root decisions reserved. Measure end-to-end task success and wait, not portal availability.

**Conclusion.** Effective autonomy requires operational capability, not merely removal of sign-off.

### Example 4

**Situation.** A security architect recommends one database, and teams treat the recommendation as mandatory.

**Reasoning.** Separate advice from an authoritative standard. If the protected outcome requires encryption, recovery, patching, and support rather than the product, publish those requirements and a conforming-alternative path. If interoperability requires one technology, document authority, scope, evidence, and lifecycle.

**Conclusion.** Clear instrument semantics prevent expert influence from becoming invisible policy.

### Example 5

**Situation.** A team proposes an unfamiliar but reversible queue configuration.

**Reasoning.** It is outside the paved path but affects one domain and can be detected and rolled back inside safe bounds. Authorize a bounded experiment with hypothesis, traffic limit, observation, abort threshold, owner, and expiry. Feed results into the platform and standard.

**Conclusion.** Reversible experiments let governance learn without turning novelty into either prohibition or unlimited discretion.

### Example 6

**Situation.** Three teams each delete local replay data to reduce storage cost.

**Reasoning.** Trace the shared disaster-recovery invariant: at least one independently usable event history must survive. Allocate ownership, retention, restoration tests, funding, and change consultation. Teams remain free to optimize other storage inside that invariant.

**Conclusion.** A minimum shared core protects system outcomes while preserving local design choice.

### Example 7

**Situation.** A platform reports 95% adoption and calls this evidence of autonomy.

**Reasoning.** Inspect consumer task success, lead time, cognitive burden, incident and recovery outcomes, support wait, exceptions, lock-in, alternative routes, and who can influence priorities. Adoption may reflect value, mandate, budget asymmetry, or missing alternatives.

**Conclusion.** Platform consumption is an input to evaluation, not proof of consumer agency or outcome.

### Example 8

**Situation.** A domain has repeated mandatory architecture consultations for routine recovery design.

**Reasoning.** Classify why: ambiguous outcome, missing expertise, no testing environment, or reserved consequence. Clarify the standard, provide recovery fixtures and telemetry through a platform, use time-bounded enablement, and delegate when the team demonstrates operation and diagnosis. Retain central authority only for shared recovery assumptions.

**Conclusion.** Capability transfer can move decisions outward without weakening assurance.

### Example 9

**Situation.** A privacy guardrail blocks a legitimate accessibility feature because classification metadata is wrong.

**Reasoning.** Return inconclusive or fail according to consequence, show the disputed input, route correction to its data owner, protect an accessible appeal, and allow only a legitimately authorized bounded path. Investigate whether the rule systematically burdens a cohort. Do not tell the product team simply to bypass or abandon the feature.

**Conclusion.** Autonomy requires contestable facts and remedies, not only fast automated denial.

### Example 10

**Situation.** A regional transit authority delegates passenger-information displays to product teams while emergency messages remain centrally governed.

**Reasoning.** Delegate layout, routine scheduling, and experiments inside accessibility, language, latency, security, and content-source bounds. Provide supported data and deployment platforms. Reserve emergency authority and public-safety semantics, but preauthorize local fallback messages when connectivity fails. Observe rider outcomes, accessible delivery, regional variation, incidents, and recovery; include public and operator feedback in envelope review.

**Conclusion.** Public-service autonomy can be local and adaptive while preserving legitimate shared and emergency authority.

## Cross-Program Connections

- [Software Engineering Patterns](../../11-software-engineering-patterns/ROADMAP.md) owns implementation-level forces, responsibilities, and variation mechanisms.
- [Testing and Software Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) owns test evidence and automated-oracle limits.
- [Software Delivery and Reliability Engineering](../../14-software-engineering-software-delivery-and-reliability-engineering/ROADMAP.md) owns delivery flow, operational feedback, recovery, and reliability governance.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) owns threat, authorization, control, and reserved security decisions.
- [Systems Engineering](../../26-systems-engineering/ROADMAP.md) owns whole-system requirements, stakeholders, hazards, assurance, and lifecycle authority.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md) owns platform product design, self-service, guardrails, consumer experience, and platform governance in depth.

## References

1. ISO/IEC, [ISO/IEC 38500:2024, *Information technology — Governance of IT for the organization*](https://www.iso.org/standard/81684.html), 3rd ed., February 2024; official published status checked 2026-09-06.
2. ISO/IEC/IEEE, [ISO/IEC/IEEE 42020:2019, *Software, systems and enterprise — Architecture processes*](https://www.iso.org/standard/68982.html), 1st ed., July 2019; official record shows 2025 confirmation and status “to be revised,” checked 2026-09-06.
3. Cherilyn Pascoe, Stephen Quinn, and Karen Scarfone, [*The NIST Cybersecurity Framework (CSF) 2.0*](https://doi.org/10.6028/NIST.CSWP.29), NIST CSWP 29, February 2024; official published record checked 2026-09-06.
4. NIST, [*Cybersecurity Framework 2.0: Resource & Overview Guide*](https://www.nist.gov/cyberframework), 2024; official framework and resource status checked 2026-09-06.
5. Matthew Skelton and Manuel Pais, [*Team Topologies: Organizing Business and Technology Teams for Fast Flow*](https://teamtopologies.com/book), 2nd ed., IT Revolution, September 2025; official book and maintained concept material checked 2026-09-06.
6. Elinor Ostrom, “Beyond Markets and States: Polycentric Governance of Complex Economic Systems,” *American Economic Review*, vol. 100, no. 3, pp. 641–672, 2010, [DOI 10.1257/aer.100.3.641](https://doi.org/10.1257/aer.100.3.641). Institutional calibration, not a direct prescription for software teams.
7. David L. Parnas, “On the Criteria To Be Used in Decomposing Systems into Modules,” *Communications of the ACM*, vol. 15, no. 12, pp. 1053–1058, 1972, [DOI 10.1145/361598.361623](https://doi.org/10.1145/361598.361623).
8. Melvin E. Conway, [“How Do Committees Invent?”](https://www.melconway.com/Home/Committees_Paper.html), *Datamation*, vol. 14, no. 4, pp. 28–31, April 1968.
9. Nicole Forsgren, Jez Humble, and Gene Kim, *Accelerate: The Science of Lean Software and DevOps*, IT Revolution, 2018. Delivery capability, loosely coupled architecture, and outcome-measurement context.
10. Amy C. Edmondson, “Psychological Safety and Learning Behavior in Work Teams,” *Administrative Science Quarterly*, vol. 44, no. 2, pp. 350–383, 1999, [DOI 10.2307/2666999](https://doi.org/10.2307/2666999).
11. Michael Nygard, [“Documenting Architecture Decisions”](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions), November 2011. Decision context, status, and consequence recording.
12. Len Bass, Paul Clements, and Rick Kazman, *Software Architecture in Practice*, 4th ed., Addison-Wesley, 2021. Stakeholders, quality attributes, trade-offs, and architectural evidence.

## Exercises

### Exercise 1

Distinguish nominal autonomy, effective autonomy, and unbounded discretion. Give one technical example of each.

### Exercise 2

Route these choices and justify each route: an internal cache threshold; removal of a field used by two consumers; a new purpose for regulated personal data; an unfamiliar reversible load-balancing experiment; and a shared root-certificate change.

### Exercise 3

Diagnose this statement: “The payments team is autonomous: it needs no architecture approval, but infrastructure owns all production access, security owns releases, and finance owns capacity with no service commitments.” Identify the missing envelope fields and propose a coherent repair.

### Exercise 4

Design a delegation envelope for a team owning customer-notification outcomes. Include outcomes, decision classes, boundaries, capabilities, evidence, feedback, exception, appeal, and lifecycle.

### Exercise 5

A national museum network wants local teams to experiment with exhibit technology while preserving accessibility, collections safety, visitor privacy, cybersecurity, and public accountability. Design autonomy-preserving governance for routine, shared, novel, and emergency decisions.

## Answers to the Exercises

### Answer 1

Nominal autonomy is documented permission: a service charter says the team may set capacity. Effective autonomy adds working budget, access, skills, telemetry, recovery, and authority, so the team can actually set and correct capacity inside bounds. Unbounded discretion omits constraints: a team changes shared identity semantics without consumer, security, privacy, or authority boundaries. The first may be fiction, the second is the target, and the third exports unmanaged consequences. Equivalent examples pass when they distinguish declared permission, practical capability, and absence of legitimate bounds.

### Answer 2

The internal cache threshold is local if it remains inside resource, reliability, and recovery bounds. Field removal is a bilateral or collective contract decision among producer and affected consumers with compatibility and migration. A new regulated-data purpose routes to the reserved privacy or legal authority plus relevant product ownership. The unfamiliar reversible load-balancing change can be a bounded local experiment when blast radius, observation, abort, and recovery are adequate. A shared root certificate is a shared and likely reserved trust decision because compromise, compatibility, and recovery cross domains. A strong answer changes the route when facts such as irreversibility, public obligation, or wider consumers change.

### Answer 3

Approval has disappeared, but effective authority and capability have not. Missing fields include owned outcomes; delegated release, capacity, and incident rights; access; budget; platform service contracts; security decision semantics; evidence; response times; escalation; exception; and consequence feedback. Repair by separating hard security and financial bounds from routine mechanisms, providing supported production and identity capabilities, delegating conforming release and capacity changes, defining service objectives and escalation for providers, supplying budget envelopes and telemetry, and retaining explicit routes for novel security or material financial decisions. Narrow payments accountability until these means exist. The team cannot honestly own outcomes it cannot influence.

### Answer 4

Define outcomes such as timely, correct, consented, accessible, cost-bounded, and recoverable notifications. Delegate templates within approved semantics, scheduling, internal algorithms, bounded experiments, deployment, and capacity. Make shared customer identity, preference meaning, accessibility minima, legal consent interpretation, emergency content, and cross-channel contracts shared or reserved as appropriate. Supply messaging, identity, preference, testing, telemetry, and rollback platforms with support. Require delivery, opt-out, accessibility, security, cost, and recovery evidence. Return customer and operational outcomes to the team and aggregate systemic failures to governance. Provide contested-fact appeal, alternative-compliance and expiring-exception paths, incident authority, and explicit consumer consultation. Review the envelope after incidents, regulation, channel changes, repeated exceptions, or demonstrated capability.

### Answer 5

Map legitimate authorities and affected people first: museum governing bodies, collections and safety specialists, accessibility and privacy authorities, cybersecurity, local curators and operators, vendors, visitors, and relevant public oversight. Delegate reversible local exhibit layout, content sequencing, and interaction experiments inside accessibility, environmental, network, privacy, recovery, and cost bounds. Standardize a minimum shared identity, telemetry, update, provenance, accessibility, and incident core; provide supported device and content platforms without banning justified alternatives. Shared visitor identity or cross-museum data requires affected-domain decisions; collections hazards, statutory accessibility, privacy purpose, and public-safety matters stay reserved. Novel experiments use bounded pilots with informed evidence, observation, stop thresholds, and affected-user feedback. Preauthorize emergency isolation and accessible fallback, then reconcile. Measure visitor outcomes, excluded cohorts, conservation conditions, incidents, recovery, provider burden, exceptions, and decision delay. A model answer must preserve local curatorial learning while refusing to let autonomy self-authorize harm or turn a platform default into public legitimacy.
