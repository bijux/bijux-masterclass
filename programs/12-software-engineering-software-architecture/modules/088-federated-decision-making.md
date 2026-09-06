---
module_id: SARCH-088
program: Software Engineering: Software Architecture
level: 2
module_number: 88
title: Federated Decision Making
status: complete
last_verified: 2026-09-06
---

# Federated Decision Making

## One-Page Review

### Governing question

How can semi-autonomous domains make local architecture decisions quickly while coordinating shared semantics, interfaces, risks, and resources without recreating central command, producing incompatible local optima, or diffusing accountability across a council?

### Essential definitions

- a **federation** is a set of semi-autonomous decision domains joined by explicit shared agreements and coordination mechanisms;
- a **decision domain** is a bounded subject, authority, resources, and consequences over which an accountable owner can decide;
- **subsidiarity** places a decision at the lowest level with the competence and authority to manage its consequences;
- an **externality** is a material consequence imposed outside the deciding domain;
- a **local decision** affects one domain inside a shared envelope;
- a **bilateral decision** requires agreement between two domains;
- a **collective decision** creates or changes a shared commitment among several domains;
- a **reserved decision** belongs to a governing, legal, safety, security, privacy, financial, or other authority that federation cannot override;
- a **decision protocol** defines proposal, representation, evidence, deliberation, rule, timeout, output, dissent, appeal, and change;
- a **compatibility window** is a bounded period in which specified old and new contract versions coexist.

### Central model, mechanism, or theorem

Represent a federation as

$$
G=(N,J,Q,P,E,X,L),
$$

where $N$ is decision nodes and accountable owners, $J$ jurisdictions and reserved authorities, $Q$ decision classes and routing rules, $P$ proposal and deliberation protocols, $E$ evidence and observable outcomes, $X$ conflicts, appeals, exits, and emergencies, and $L$ compatibility and lifecycle. Route by consequence and authority, not organizational rank: one-domain in-envelope work stays local; pairwise commitments are bilateral; shared semantics and multi-domain externalities are collective; reserved matters go to their legitimate authority.

### Critical invariants

- every decision class has one accountable owner or an explicit joint-authority rule;
- local autonomy ends where material externalities or reserved authority begin;
- shared rules are the minimum needed for common outcomes, interoperability, and bounded risk;
- representation follows affected concerns, not equal headcount by default;
- proposals identify versions, alternatives, affected domains, evidence, costs, and migration;
- silence, absence, quorum, majority, and consensus have declared meanings and limitations;
- dissent and unresolved objections remain attached to the decision;
- compatibility, rollout, rollback, exit, and stranded-consumer handling are decided with the change;
- emergency protocols alter timing under prior authority and require reconciliation;
- decision latency, burden, exceptions, incidents, and domain outcomes feed protocol evolution.

### Common failures

Common failures include calling centralized approval federation; allowing local decisions to bind consumers silently; requiring unanimity for everything; using majority voting to dismiss technical objections; giving every domain an equal vote despite unequal impact or authority; treating nonresponse as consent without notice; centralizing all semantic definitions; letting each domain redefine shared identifiers; negotiating every case from scratch; omitting compatibility and funding; letting councils accept legal or safety risk; permanent emergency exceptions; opaque side agreements; and measuring meeting attendance as federation health.

### Compact example

Six product domains own local data models, but three exchange a shared customer-status event. Each domain may change internal storage locally. Changes to the event are collective among affected producers and consumers under an enterprise identity rule that remains reserved. A proposal supplies scenarios, schema diff, compatibility plan, consumer evidence, cost allocation, security impact, and expiry. One consumer's valid temporal-semantics objection blocks the proposed removal until addressed; an unrelated domain need not approve. A named event-contract owner records the final decision and migration window.

### Connections

[SARCH-087](087-architecture-communities-and-review-forums.md) supplies learning and review forums. [SARCH-089](../ROADMAP.md) next examines exception and technical-risk management. [SARCH-083](083-architecture-governance-models.md) supplies the broader governance model; this module develops federation protocols and boundary mechanics.

## Governing Question

Architectural knowledge and consequences are distributed. Domain teams understand local language, workflows, and failure. Platform and enterprise owners understand shared capabilities and cumulative exposure. Security, privacy, safety, legal, finance, and public authorities retain decisions that technical teams cannot legitimately absorb. Federation connects these centers without pretending they are one authority.

The hard problem is not decentralization alone. It is deciding which choices can remain local, which require coordination, how affected parties participate, how disagreement ends, and who remains accountable. Without an executable protocol, federation becomes either central review under a friendlier name or incompatible autonomy followed by crisis negotiation.

## Why This Matters

Parnas's information-hiding criterion places module boundaries around design decisions likely to change, reducing unnecessary coordination [5]. Conway observed a relationship between communication structures and designed systems [6]. Together they suggest why decision boundaries and interaction paths influence architecture, but neither determines legitimate organizational authority or the correct federation for a given context.

Ostrom's work on polycentric systems examines multiple centers of decision making and emphasizes experimentation and learning at several scales while acknowledging leakage, inconsistent policies, gaming, and free-riding risks [3], [4]. Software organizations can borrow the questions, not claim direct transfer from environmental governance. Architectural resources, authority, employment, law, and consequences differ.

ISO/IEC 38500:2024 is the current third edition of the governance-of-IT standard and addresses the organization's current and future use of IT [1]. ISO/IEC/IEEE 42020:2019 defines governance, management, architecting, and enablement processes and is currently published but marked to be revised [2]. These sources reinforce explicit governance and lifecycle, not one prescribed council topology.

## Prerequisites and Retrieval

Retrieve governance, authority, accountability, delegation, autonomy, domain, bounded context, externality, subsidiarity, federation, polycentricity, interoperability, semantic contract, standard, profile, conformance, proposal, quorum, consensus, veto, dissent, appeal, escalation, compatibility, migration, exception, emergency authority, and evidence.

SARCH-082 supplies team topology. SARCH-083 supplies governance arrangements and decision classes. SARCH-084 supplies shared standards and guardrails. SARCH-087 supplies communities and review forums. This module owns how semi-autonomous domains route, negotiate, record, implement, and evolve shared decisions. It does not replace corporate governance, labor agreements, law, regulation, public authority, or domain-specific safety processes.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish federation from centralization, isolated decentralization, and informal coordination;
2. map decision domains, authorities, dependencies, and externalities;
3. classify local, bilateral, collective, and reserved decisions;
4. design a decision protocol with representation, evidence, rules, deadlines, dissent, and appeal;
5. preserve domain semantics while governing shared contracts;
6. choose consensus, consent, accountable decision, or voting rules with explicit limits;
7. plan compatibility, rollout, cost allocation, exit, and emergency change;
8. prevent power, expertise, and participation asymmetries from becoming invisible authority;
9. evaluate federation through decision and outcome evidence; and
10. redesign a federation when its topology no longer matches architectural consequences.

## Core Exposition

**Map the decision system as it exists.** Inventory formal delegations, implicit vetoes, platform controls, standards, budgets, suppliers, review forums, on-call ownership, data authority, and who pays when decisions fail. Compare official charts with actual escalation and side agreements. A federation diagram without power and consequence is incomplete.

**Define decision nodes.** Each node needs a bounded subject, accountable owner, competence, resources, evidence access, and escalation. Nodes may be product domains, platforms, shared services, assurance functions, governing bodies, suppliers, or public authorities. A representative attending a council is not necessarily authorized to commit a node.

**Classify decisions by affected scope.** Local decisions remain within one domain and the shared envelope. Bilateral decisions alter a contract between two nodes. Collective decisions change a shared semantic, protocol, capability, or cumulative risk. Reserved decisions belong to another authority regardless of how many technical domains agree. Classification can change when evidence reveals wider externalities.

**Apply subsidiarity with capability and consequence.** Place work as locally as possible only when the node can observe and manage relevant consequences. A team may choose its internal algorithm. It cannot unilaterally change an event field used by five consumers or accept organization-wide identity risk. Escalating every unfamiliar choice is equally harmful; build competence and bounded envelopes so local authority can grow.

**Minimize the shared core.** Standardize identifiers, contract semantics, compatibility, trust, evidence, and operational behavior only to the extent needed for shared outcomes. Preserve domain-specific concepts where forced uniformity would erase truth. Use profiles and mappings rather than one overloaded canonical model when contexts differ.

**Write the decision protocol.** Define who may propose, required metadata, discovery of affected nodes, notice, evidence, response periods, facilitator, decision rule, veto or reserved authority, dissent, appeal, output, implementation, verification, and revision. A protocol should handle absence, conflict of interest, urgent need, and an unresponsive dependency.

**Select representation by concern.** Equal domain representation can protect voice, but impact is rarely equal. Include producers, consumers, operators, platform owners, specialists, funders, and affected stakeholders according to the decision. Record missing perspectives. Do not let the team with the most staff, budget, meeting fluency, or executive access become the default federation.

**Use decision rules deliberately.** Consensus can expose objections and build commitment but can deadlock. Consent asks whether a proposal is safe enough to try inside bounds, not whether it is everyone's favorite. Majority voting can decide preferences under legitimate bylaws but cannot make an unresolved technical or legal problem false. Accountable decision after consultation is often clear, provided dissent and authority remain explicit. RFC 7282's treatment of rough consensus emphasizes addressing technical objections rather than counting heads; it is IETF Informational guidance, not a universal rule [9].

**Separate veto from objection.** A technical objection supplies a mechanism and consequence. A veto is a decision right granted by authority. Specialists may identify nonconformance without owning the business decision; reserved authorities may prohibit action inside their mandate. Publish these differences before conflict.

**Federate semantics through contracts and mappings.** A domain owns its model. Shared use requires declared meaning, identity, time, units, nullability, provenance, lifecycle, and error behavior. Use translations when concepts legitimately differ. A shared term is not governed by choosing one label; consumers need versioned semantics and counterexamples.

**Bundle migration with decision.** A shared change is incomplete without affected versions, compatibility window, rollout order, consumer readiness, observability, rollback, data repair, funding, support, and retirement. The proposer cannot externalize migration cost silently. Name who maintains old and new paths and when obligations end.

**Keep a federated decision record.** Record decision identity, class, reference version, proposal owner, affected nodes, authorities, evidence, options, objections, rule used, accountable outcome, conditions, funding, implementation owners, compatibility, verification, appeal, and revisit trigger. Link local records so later readers can reconstruct the distributed rationale.

**Handle timeout explicitly.** Silence can mean agreement, lack of authority, inaccessible process, overload, or missing notice. Define when no response permits a reversible experiment, when it escalates, and when action must wait. Never treat silence as acceptance of irreversible harm or reserved obligations.

**Preauthorize emergencies.** Define triggers, incident authority, bounded changes, communication, evidence, rollback, expiry, and retrospective reconciliation. Emergency action may temporarily bypass ordinary consultation, not legal authority or durable accountability. Repeated emergency use signals a broken normal protocol.

**Support exit and nonparticipation.** A federation needs rules for joining, leaving, supplier replacement, data and contract exit, stranded consumers, and retained obligations. A domain cannot exit a shared contract instantly after others relied on it. Conversely, permanent lock-in undermines autonomy and bargaining legitimacy.

**Observe the decision system.** Measure end-to-end decision time, wait, participation gaps, objections, reopenings, compatibility defects, migration burden, exceptions, emergency use, incidents, local autonomy, and shared outcomes. Approval count and council attendance describe activity. Qualitative evidence reveals coercion, shadow decisions, and burdens hidden by aggregate metrics.

**Evolve topology.** When a bilateral contract becomes infrastructure for twenty domains, its authority and assurance likely need change. When a shared standard no longer has consumers, retire it. Split overloaded councils, merge duplicated semantics, and move stable decisions into platforms and guardrails. Federation is an architecture that must evolve with dependencies.

## Definitions and Notation

Let $G=(N,J,Q,P,E,X,L)$. $N$ is the set of decision nodes with owners and capabilities. $J$ maps subjects to organizational and reserved jurisdictions. $Q$ maps decision characteristics to local, bilateral, collective, or reserved classes. $P$ defines proposal, deliberation, and decision protocols. $E$ stores claims, evidence, records, implementation, and outcomes. $X$ defines conflict, appeal, emergency, and exit. $L$ defines versions, compatibility, migration, and topology evolution.

For decision $d$, let $A(d)\subseteq N$ be materially affected nodes and let $R(d)$ be any reserved authority. Cardinality helps but is insufficient: one domain's privacy decision may still be reserved, while ten independent local upgrades may remain local. Externality, authority, coupling, reversibility, and evidence determine routing.

A **federation** coordinates semi-autonomous nodes through agreements. **Decentralization** merely distributes decisions. **Polycentricity** emphasizes multiple interacting centers. **Subsidiarity** is a placement principle. **Consensus** is a decision process. **Interoperability** is an outcome. None implies the others automatically.

## Mechanisms, Invariants, or Proof Structure

### Accountable-node invariant

Every decision has an accountable owner authorized for its class. A council can deliberate collectively, but “the federation decided” is incomplete unless the protocol defines joint authority and its accountability.

### Bounded-autonomy invariant

A node may decide locally only when it stays inside shared constraints and does not impose unmanaged material externalities. Disagreement with a preference is not an externality; compatibility breakage, shared-resource exhaustion, or transferred risk may be.

### Shared-change invariant

Every collective contract change includes affected nodes, semantic version, compatibility, migration, funding, implementation, verification, and retirement. Approval without an executable transition is incomplete.

### Reserved-authority invariant

No technical quorum, consensus, executive preference, or emergency label can transfer a reserved decision outside the authority that legitimately owns it.

### Executable routing policy

<!-- bijux-verify: {"id":"federated-decision-router","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"internal cache: local\nproducer consumer contract: bilateral\nshared identity claim: collective\nregulated retention: reserved-authority\nlocal outside envelope: federated-review\n","stderr":""}} -->
```python
def route(affected, in_envelope=True, shared_semantics=False, reserved=False):
    if reserved:
        return "reserved-authority"
    if len(affected) == 1 and in_envelope and not shared_semantics:
        return "local"
    if len(affected) == 2 and not shared_semantics:
        return "bilateral"
    if shared_semantics or len(affected) > 2:
        return "collective"
    return "federated-review"

cases = {
    "internal cache": ({"orders"}, True, False, False),
    "producer consumer contract": ({"orders", "billing"}, True, False, False),
    "shared identity claim": ({"orders", "billing", "support"}, True, True, False),
    "regulated retention": ({"records"}, True, False, True),
    "local outside envelope": ({"search"}, False, False, False),
}
for name, facts in cases.items():
    print(f"{name}: {route(*facts)}")
```

The router is a fictional first screen. Real classification needs legitimate authority, evidence about consequences, three-valued uncertainty, and appeal.

### Proposition: majority agreement cannot prove safe externalities

Suppose four of five domains benefit from removing a compatibility field, while the fifth cannot process the new contract and would lose transactions. A four-to-one vote can pass while imposing a known material externality. Therefore majority support alone cannot prove the change safely manages shared consequences.

### Proposition: local optimization can worsen the federation

Two domains each reduce their own storage cost by deleting replay history, but their shared recovery process requires at least one complete history. Both local cost metrics improve while federation recovery becomes impossible. This counterexample refutes unconditional inference from every measured local improvement to collective improvement.

## Alternatives and Trade-Offs

**Centralized authority** makes accountability and global consistency clearer but can create queues, weak local fit, and concentrated failure. **Federation** preserves local knowledge and experimentation but pays coordination, protocol, and compatibility cost. **Isolated decentralization** is fast until shared consequences emerge.

**Unanimity** protects every participating node but permits holdout and delay. **Majority** terminates decisions but may impose asymmetric costs. **Consent** supports bounded experiments but requires clear safety envelopes. **Accountable decision after consultation** is decisive but depends on legitimate authority and substantive objection handling.

**Canonical semantics** simplifies aggregation but can erase domain truth. **Mappings** preserve meaning but add translation and lineage burden. **Shared kernel plus profiles** can balance them if precedence and versioning are explicit.

**Permanent councils** provide continuity but accumulate scope. **Temporary working groups** focus expertise but can disappear before implementation. Use working groups to develop bounded proposals and stable owners to govern durable contracts.

**Synchronous negotiation** builds mutual understanding but excludes some participants and consumes time. **Asynchronous proposals** improve traceability and access but can prolong ambiguity. Combine written evidence and deadlines with meetings for unresolved coupled issues.

## Failure Modes and Misconceptions

1. **Federation means every team decides everything.** Authority remains bounded by shared consequences.
2. **Federation means a central council.** A council can reproduce centralized approval.
3. **Equal votes mean equitable power.** Impact, authority, resources, and participation remain unequal.
4. **Local ownership implies unilateral contract change.** Consumers hold legitimate interests in shared behavior.
5. **A shared term has one universal meaning.** Context may require governed mappings.
6. **Consensus requires unanimity.** Processes can address objections without universal preference.
7. **Majority resolves technical risk.** Voting does not change mechanisms or evidence.
8. **Specialists automatically own vetoes.** Objection, assurance, and reserved authority differ.
9. **Silence is consent.** It may indicate absence, overload, or inaccessible notice.
10. **Decision ends at approval.** Migration, funding, verification, and retirement remain.
11. **Local metrics compose.** Independent improvements can create collective failure.
12. **Shared standards should be comprehensive.** Excess common rules suppress useful domain variation.
13. **Emergency action is ungoverned.** It needs prior authority, scope, expiry, and reconciliation.
14. **Federation eliminates escalation.** It needs clearer conflict and appeal paths.
15. **Platforms are neutral implementation.** Defaults distribute authority, cost, and constraints.
16. **Participation proves representation.** Delegation and affected concerns require evidence.
17. **Exit should be immediate.** Reliance creates transition and retained obligations.
18. **One topology fits forever.** Dependency and authority changes require redesign.

## Worked Examples

### Example 1

**Keep a reversible choice local.** An orders team changes its internal cache eviction algorithm inside cost, reliability, security, and rollback envelopes. No shared contract or resource changes. The team decides and records evidence locally; a federation council adds no value. **Conclusion:** federation preserves local authority when consequences remain local.

### Example 2

**Route a bilateral contract.** Orders produces an event consumed only by billing. A field's meaning and retry behavior change. Both domains agree on semantics, version, compatibility window, tests, rollout, and rollback; the contract owner records the decision. **Conclusion:** pairwise dependency needs bilateral authority, not organization-wide voting.

### Example 3

**Govern a shared semantic.** Six domains use “active customer,” but lifecycle and legal meanings differ. The federation defines a narrow shared identity plus contextual domain states and mappings, rather than forcing one Boolean. Enterprise reporting claims name their interpretation. **Conclusion:** interoperability can require mappings instead of semantic erasure.

### Example 4

**Respect reserved authority.** Four domains agree to retain sensitive logs indefinitely for debugging. Privacy and records authorities identify incompatible obligations. Technical consensus cannot accept that risk; the design uses bounded retention, protected access, and a lawful exception process. **Conclusion:** federation cannot vote away reserved authority.

### Example 5

**Answer a minority compatibility objection.** Four consumers can adopt schema version 3; one critical settlement consumer cannot distinguish a removed state. The group traces lost transactions and retains a compatibility field until the consumer migrates. **Conclusion:** affected consequence, not headcount, determines whether an objection is material.

### Example 6

**Break unanimity deadlock safely.** Twelve domains must approve every standard, so one absent representative blocks routine corrections. The protocol changes: affected domains and reserved authorities participate; a named owner decides after a response window; unresolved material objections escalate; unrelated domains need not consent. **Conclusion:** executable scope and timeout rules improve federation without ignoring dissent.

### Example 7

**Allocate migration cost.** A platform proposes a new identity token that lowers central operating cost but forces thirty consumers to update. The proposal includes consumer inventory, dual-read window, adapters, funding, support, telemetry, rollback, and retirement. Cost is evaluated across the federation, not only the platform budget. **Conclusion:** proposers must expose transferred work.

### Example 8

**Use emergency authority.** A shared certificate path is compromised. A preauthorized incident lead rotates trust roots, publishes affected versions, monitors failure, and permits bounded compatibility. After containment, domains reconcile records, repair clients, review authority use, and retire the emergency path. **Conclusion:** speed and accountability can coexist through prior protocol.

### Example 9

**Detect local optimization failure.** Two services delete replay history to reduce their own storage cost. Cross-service recovery required either history to reconstruct settlement. Local dashboards improve, but the architecture loses recoverability. The shared contract assigns one durable source and tests reconstruction. **Conclusion:** federation evidence must include collective scenarios.

### Example 10

**Transfer federation to clinical research.** Hospitals retain local clinical and legal authority while sharing a research protocol, metadata semantics, privacy constraints, audit evidence, and revocation behavior. A joint forum cannot waive patient rights or regulator authority; power and funding asymmetries are recorded; withdrawal, incident, and exit paths are explicit. **Conclusion:** technical federation coordinates shared work but does not merge legitimate authorities.

## Cross-Program Connections

- [SARCH-082](082-team-topologies-and-architecture.md) supplies organizational interaction and cognitive-load boundaries.
- [SARCH-083](083-architecture-governance-models.md) supplies governance, delegation, assurance, and decision-class foundations.
- [SARCH-084](084-standards-principles-and-guardrails.md) supplies minimum shared rules and conformance evidence.
- [SARCH-087](087-architecture-communities-and-review-forums.md) supplies forums for learning, deliberation, and review.
- [DARCH-071](../../20-data-architecture-engineering/modules/071-federated-data-governance.md) applies federation to data ownership, semantics, and policy.
- [SYSENG-093](../../26-systems-engineering/modules/093-federated-architectures.md) owns system-of-systems federation across operational and organizational boundaries.
- [API-088](../../28-api-and-service-engineering/modules/088-schema-registries-and-contract-governance.md) applies shared decision rules to API schemas and consumer compatibility.

## References

1. ISO/IEC. *ISO/IEC 38500:2024, Information technology — Governance of IT for the organization*. Edition 3, February 2024. [Official ISO record](https://www.iso.org/standard/81684.html). Retrieved 2026-09-06.
2. ISO/IEC/IEEE. *ISO/IEC/IEEE 42020:2019, Software, systems and enterprise — Architecture processes*. Edition 1, July 2019; published, marked to be revised. [Official ISO record](https://www.iso.org/standard/68982.html). Retrieved 2026-09-06.
3. Elinor Ostrom. *Governing the Commons: The Evolution of Institutions for Collective Action*. Cambridge University Press, 1990.
4. Elinor Ostrom. “Polycentric Systems for Coping with Collective Action and Global Environmental Change.” *Global Environmental Change* 20(4), 2010, pp. 550–557. [DOI](https://doi.org/10.1016/j.gloenvcha.2010.07.004).
5. David L. Parnas. “On the Criteria To Be Used in Decomposing Systems into Modules.” *Communications of the ACM* 15(12), 1972, pp. 1053–1058. [DOI](https://doi.org/10.1145/361598.361623).
6. Melvin E. Conway. “How Do Committees Invent?” *Datamation* 14(4), 1968, pp. 28–31. [Author archive](https://www.melconway.com/Home/Committees_Paper.html). Retrieved 2026-09-06.
7. Eric Evans. *Domain-Driven Design: Tackling Complexity in the Heart of Software*. Addison-Wesley, 2003.
8. Matthew Skelton and Manuel Pais. *Team Topologies: Organizing Business and Technology Teams for Fast Flow*. 2nd ed., IT Revolution, 2025.
9. Pete Resnick. *RFC 7282: On Consensus and Humming in the IETF*. Informational, June 2014. [Official RFC Editor record](https://www.rfc-editor.org/info/rfc7282). Retrieved 2026-09-06.
10. Michael Nygard. “Documenting Architecture Decisions.” 15 November 2011. [Author's article](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions). Retrieved 2026-09-06.
11. Len Bass, Paul Clements, and Rick Kazman. *Software Architecture in Practice*. 4th ed., Addison-Wesley, 2021.
12. ISO. *ISO 37000:2021, Governance of organizations — Guidance*. Edition 1, September 2021. [Official ISO record](https://www.iso.org/standard/65036.html). Retrieved 2026-09-06.

## Exercises

### Exercise 1

Distinguish local, bilateral, collective, and reserved decisions. Explain why the number of affected domains is useful but insufficient for classification.

### Exercise 2

Trace a shared-event change through proposal, affected-node discovery, evidence, objections, decision rule, accountable outcome, compatibility, implementation, verification, dissent, and retirement.

### Exercise 3

A federation requires unanimity from fifteen domains for every platform change. Decisions take three months, side agreements proliferate, and one domain bears most migration cost. Diagnose at least six protocol defects and propose bounded corrections.

### Exercise 4

Design a federated decision topology for four product domains, a platform, security, privacy, finance, and a shared analytics function. Specify local envelopes, bilateral and collective contracts, reserved authority, forums, evidence, cost allocation, and escalation.

### Exercise 5

Design a federation protocol for exchanging wildfire evacuation information among municipalities, emergency services, telecom providers, accessibility organizations, mapping suppliers, and the public. Address authority, semantics, urgency, privacy, accessibility, misinformation, failures, compatibility, power, evidence, appeal, and limits.

## Answers to the Exercises

### Answer 1

A local decision affects one node inside shared constraints. A bilateral decision changes a commitment between two nodes. A collective decision changes shared semantics, protocols, resources, or externalities across several nodes. A reserved decision belongs to a specific governing or specialist authority regardless of technical agreement. Cardinality can suggest coordination cost, but one-domain retention may be legally reserved, while many independent in-envelope upgrades remain local. Authority, externality, coupling, reversibility, and evidence determine class.

### Answer 2

The producer proposes an exact schema and semantic diff with drivers, alternatives, versions, and timing. Dependency evidence identifies all producers, consumers, operators, and reserved authorities. Each affected node checks data meaning, compatibility, performance, security, operations, cost, and migration. Objections state mechanisms and consequences. The declared rule—such as accountable contract-owner decision after material objections are addressed—produces a named outcome with dissent. The record includes dual-version behavior, rollout order, consumer readiness, funding, telemetry, rollback, repair, and old-version retirement. Implementation owners execute; verification observes both protocol and business outcomes; unresolved conditions remain open and trigger re-review.

### Answer 3

Defects include overbroad scope, universal rather than affected representation, unanimity deadlock, no timeout or escalation, unclear authority, hidden side decisions, absent cost allocation, no proportional local envelope, and likely inaccessible evidence. Classify changes as local, bilateral, collective, or reserved. Require only affected nodes and authorities; name an accountable owner; time-box consultation; record material objections and appeal; delegate reversible in-envelope changes; publish proposals and decisions; allocate migration funding by consequence and benefit; and monitor total latency, bypass, rework, incidents, and asymmetric burden. Retain unanimity only where a legitimate agreement truly requires it.

### Answer 4

Product domains own internal models and implementation inside shared security, privacy, cost, and platform envelopes. Bilateral API and event contracts belong to named producer-consumer owners. Collective identity, telemetry, deployment, and analytics semantics use affected-domain forums with platform and analytics owners. Security and privacy retain reserved control and risk authorities; finance retains budget authority. Proposals include scenarios, evidence, externalities, compatibility, cost, and exit. Automated conformance handles stable predicates; forums address novel or shared decisions. A named owner decides under each protocol, with dissent, conditions, appeal, emergency authority, and verification. Costs are allocated explicitly rather than hidden in consumers. Repeated disputes trigger shared-capability or protocol redesign.

### Answer 5

Municipalities and emergency services retain lawful warning and evacuation authority; telecom and mapping suppliers own contracted delivery boundaries; accessibility and community representatives supply affected-user evidence; no technical council can merge these authorities. Govern location, time, severity, source, expiry, correction, language, accessibility, privacy, provenance, and delivery semantics with versioned profiles. Emergency protocols allow authenticated rapid publication, redundant channels, offline and degraded operation, rollback or correction, and later reconciliation. Threat and failure analysis covers spoofing, stale maps, network loss, overload, rumor amplification, inaccessible formats, location exposure, and supplier outage. Compatibility preserves older consumers during bounded windows. Records expose authority, evidence, dissent, supplier conflicts, conditions, and outcomes; appeal and correction remain reachable. Metrics cover reach, timeliness, accessibility, false and stale messages, recovery, and public reports without claiming conformance proves safety, trust, equitable access, legality, or lives saved.
