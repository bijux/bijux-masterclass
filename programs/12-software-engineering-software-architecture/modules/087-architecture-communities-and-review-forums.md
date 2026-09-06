---
module_id: SARCH-087
program: Software Engineering: Software Architecture
level: 2
module_number: 87
title: Architecture Communities and Review Forums
status: complete
last_verified: 2026-09-06
---

# Architecture Communities and Review Forums

## One-Page Review

### Governing question

How should an organization cultivate architectural learning and run review forums so that knowledge travels, consequential decisions receive appropriate challenge, dissent remains visible, and neither community participation nor meeting attendance is mistaken for authority or assurance?

### Essential definitions

- a **community of practice** is a sustained learning partnership among people who share a domain of practice and improve it through participation;
- a **review forum** is a chartered setting that examines a defined proposal, claim, or evidence package and produces an advisory, decision, or assurance output;
- an **architecture guild** is an organizational label that may describe a community, a governance body, or both; its name does not define authority;
- **decision authority** is legitimate power to make a bounded decision and accept its organizational consequences;
- **assurance** is evidence-based confidence work performed with stated independence and scope;
- **representation** is participation by people able to bring affected concerns and evidence, not merely a headcount of departments;
- **psychological safety** is a shared belief that interpersonal risk-taking is safe within a group;
- a **technical objection** states a specific mechanism, consequence, assumption, or evidence problem;
- **rough consensus** seeks resolution of material objections rather than unanimity or majority counting;
- **forum debt** is accumulated waiting, repeated review, unresolved decisions, and unmaintained knowledge caused by an unhealthy forum system.

### Central model, mechanism, or theorem

Charter each forum as

$$
F=(P,S,R,A,I,O,D,C,L),
$$

where $P$ is purpose, $S$ scope and decision classes, $R$ participants and representation, $A$ authority and roles, $I$ intake and evidence, $O$ outputs and records, $D$ dissent, conflict, appeal, and escalation, $C$ capacity and service expectations, and $L$ learning and lifecycle. A community may cultivate knowledge without $A$ containing decision authority. A review body cannot acquire authority merely because experts attend it.

### Critical invariants

- learning, advice, decision, risk acceptance, assurance, and execution are distinguishable acts;
- every forum publishes purpose, scope, membership model, authority, inputs, outputs, and escalation;
- decision records name the accountable authority, evidence, rationale, dissent, conditions, and revisit trigger;
- affected concerns and specialist authorities are represented or recorded as evidence gaps;
- participation is accessible across status, location, language, disability, time zone, and employment relation where relevant;
- material objections are answered on substance rather than defeated by rank, volume, or votes;
- reversible in-envelope choices avoid scarce synchronous review;
- queues, preparation, interruption, and follow-through fit funded qualified capacity;
- confidential evidence is protected without making decisions unaccountable;
- repeated questions and exceptions feed standards, paths, references, teaching, and forum redesign.

### Common failures

Common failures include calling an approval board a community; making community attendance compulsory; letting a voluntary guild own production risk; hiding authority behind “architecture says”; reviewing every change; inviting only senior architects; requiring unanimity; treating a vote as technical resolution; accepting slide decks without evidence; surprising teams in meetings; allowing reviewers to introduce requirements late; suppressing dissent; recording only the final color; holding inaccessible office hours; using confidential evidence to avoid explanation; measuring meeting volume; leaving actions unowned; and preserving a forum after its purpose disappears.

### Compact example

A voluntary architecture community hosts case clinics, writes shared vocabulary, and curates reference examples. It cannot approve systems. A separate weekly review forum handles only cross-domain, high-consequence, or out-of-envelope decisions. Its charter says the forum advises; a named product executive decides, while security and privacy authorities retain their domains. Proposals arrive asynchronously with scenarios and evidence; reviewers record objections before the meeting. Routine conforming changes bypass it. The record names advice, decision owner, dissent, conditions, and closure evidence. Repeated identity questions become a paved capability and teaching session.

### Connections

[SARCH-086](086-reference-architectures.md) supplies reusable knowledge for communities to curate and forums to specialize. [SARCH-088](../ROADMAP.md) next examines federated authority across domains. [SARCH-070](070-running-an-evidence-based-architecture-review.md) supplies detailed review evidence discipline.

## Governing Question

Architecture is learned through real design, operation, failure, explanation, and challenge. No central document or expert group can anticipate every domain. Communities allow practitioners to exchange situated knowledge and develop shared competence. Review forums create a bounded place for challenge, advice, decision, or assurance when consequences cross local boundaries.

The two mechanisms fail when their identities blur. A community becomes coerced governance; an approval body claims the trust associated with peer learning; or an advisory forum becomes the invisible decision maker. Healthy architecture practice requires both social learning and explicit authority, with different participation, records, capacity, and success evidence.

## Why This Matters

Lave and Wenger developed situated learning and legitimate peripheral participation as an account of learning through participation in practice [1]. Wenger later developed communities of practice through mutual engagement, joint enterprise, and shared repertoire [2]. Brown and Duguid argued from workplace studies that actual work, learning, and innovation often differ from canonical descriptions [3]. These traditions warn against reducing a community to a meeting series or information-distribution list.

Wenger-Trayner's current overview calls communities of practice sustained learning partnerships and notes that they can become stale, defensive, or siloed [4]. A community needs cultivation, boundary connections, and renewal; it does not automatically generate good architecture or equitable participation.

Formal architecture processes serve another purpose. ISO/IEC/IEEE 42020:2019 establishes governance, management, architecting, and enablement process descriptions across architecture lifecycles; the official ISO record currently lists the published standard at stage 90.92, “to be revised” [8]. It does not require one universal architecture board. Organizations must design forums suited to their decisions while checking the status of the guidance they cite.

DORA's 2019 survey research reported that high-performing groups favored community-oriented strategies for spreading practices and warned about centralized centers of excellence becoming bottlenecks and losing contact with work [7]. This is useful population evidence with stated research boundaries, not proof that naming a guild causes performance. Local baseline, participation, decision, delivery, and outcome evidence remains necessary.

## Prerequisites and Retrieval

Retrieve community of practice, situated learning, domain, practice, membership, facilitation, psychological safety, stakeholder, concern, authority, advice, approval, assurance, risk acceptance, review charter, quality-attribute scenario, claim, evidence, conflict of interest, dissent, rough consensus, quorum, escalation, appeal, queue, service expectation, decision record, and retrospective.

SARCH-030 supplies audience-aware communication. SARCH-061 and SARCH-070 supply structured and evidence-based reviews. SARCH-082 supplies team interaction modes. SARCH-083 supplies governance authority. SARCH-084 supplies standards and guardrails. This module focuses on social-learning and forum systems; it does not replace personnel policy, labor representation, legal consultation, safety governance, security review, accessibility research, or independent audit.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish communities, guilds, working groups, review forums, boards, and assurance bodies;
2. define a community domain, membership model, learning activities, facilitation, and renewal;
3. charter a review forum with explicit authority and decision classes;
4. design intake, preparation, synchronous discussion, outputs, and follow-through;
5. select representative participants and record missing perspectives;
6. facilitate technical dissent without demanding unanimity or counting rank;
7. route decisions proportionately and avoid centralized review queues;
8. estimate review capacity and recognize overload before quality collapses;
9. protect confidential evidence while preserving accountable conclusions; and
10. evaluate learning and review systems without activity or approval theater.

## Core Exposition

**Inventory actual groups.** List communities, guilds, councils, design clinics, architecture boards, standards groups, office hours, security reviews, change bodies, and informal expert networks. For each, record who attends, what work occurs, which decisions people believe it makes, what records exist, and what consequences follow. Names are unreliable; behavior exposes the real system.

**Separate forum archetypes.** A community cultivates practice through voluntary or intrinsically motivated participation. A working group produces a bounded artifact and disbands. A design clinic offers early advice. A review forum challenges a defined proposal. A decision board exercises delegated authority. An assurance body independently evaluates selected claims. One meeting can sequence several acts, but its record and roles must distinguish them.

**Cultivate a community around practice.** Define a meaningful domain and invite people who practice or are learning it. Use case clinics, incident learning, pattern critique, code or model walkthroughs, teaching, mentoring, open questions, and joint experiments. Maintain an accessible repertoire of terms, examples, decisions, failures, and contacts. Community leaders convene learning; they do not become permanent gatekeepers.

**Design entry and belonging.** Provide newcomer routes from observing to contributing and leading. Rotate facilitation and presentation. Support remote and asynchronous participation, captioning, readable artifacts, time-zone variation, and multiple ways to ask questions. Watch for status, language, employer, discipline, disability, gender, race, and location dynamics that can make nominal openness exclusionary.

**Protect psychological safety without weakening rigor.** Edmondson's field study of 51 manufacturing teams associated team psychological safety with learning behavior under its model and population [6]. In architecture practice, leaders can invite uncertainty, acknowledge their own errors, separate critique from identity, prohibit retaliation, and reward early risk disclosure. Safety does not mean freedom from technical challenge; it makes honest challenge possible.

**Charter review forums by decision.** State purpose, decision classes, exclusions, authority, chair, facilitator, recorder, required specialists, quorum if relevant, intake, evidence cutoff, service expectations, output types, escalation, appeal, confidentiality, conflicts, and lifecycle. If the forum advises, name the decision authority outside it. If it decides, record the delegation boundary and non-delegated authorities.

**Route proportionately.** Local, reversible, in-envelope decisions should use standards, peer review, automated evidence, and team authority. Shared irreversible contracts, novel threats, cross-domain data meaning, large blast radius, or nonconformance may need broader review. Emergency routes change timing and attendance under prior authorization; they do not erase accountability.

**Prepare asynchronously.** Use a concise decision brief: context, stakeholders, drivers, options, recommendation, scenarios, architecture views, evidence, assumptions, risks, dissent, requested decision, and deadline. Reviewers declare conflicts and submit questions early. The meeting should resolve decision-relevant disagreements, not discover an unread proposal.

**Make evidence inspectable.** Link exact architecture, code, configuration, tests, measurements, incidents, threat analysis, cost models, supplier terms, and known gaps. Protect sensitive details through access controls and scoped summaries. “Security approved” is not reusable evidence; record the claim, authority, scope, conditions, and expiry without exposing secrets.

**Facilitate objections, not performances.** Ask an objector to state the mechanism, consequence, affected stakeholder, assumption, and evidence that make an option unacceptable. Ask proponents to answer or change the design. RFC 7282 explains IETF rough consensus as addressing technical objections rather than equating consensus with unanimity, majority voting, persistence, or volume [10]. It is an Informational RFC, not a universal governance rule, but its distinction is useful for technical facilitation.

**Keep rank from deciding technical truth.** Authority may legitimately decide after considering evidence, but rank is not evidence. Use structured rounds, written input, independent pre-reads, and explicit dissent to reduce anchoring and dominance. Name who made the decision so a group discussion cannot diffuse accountability.

**Record meaningful outputs.** Distinguish approve, conditionally approve, advise, defer, reject, refer to another authority, and out-of-scope. Record architecture revision, decision owner, participants and missing perspectives, claims, evidence, rationale, conditions, dissent, actions, closure evidence, expiry, and revisit triggers. A meeting recording or green status is not a decision record.

**Close evidence, not tickets.** Conditions need owners, dates, decision consequences, and the observation required for closure. A mitigation plan is not an implemented mitigation. Re-review when critical assumptions, architecture, supplier, scale, threat, law, or evidence changes.

**Fund qualified capacity.** Count intake, preparation, meetings, follow-through, specialist coverage, facilitation, and interruption. Average capacity does not absorb bursts, correlated reviews, leave, conflicts, or scarce specialties. When demand exceeds capacity, narrow scope, delegate routine decisions, improve paths and evidence, add qualified reviewers, or change delivery commitments. Do not shorten review until it becomes ceremonial.

**Connect community and forum learning.** Anonymized recurring questions, risks, non-fits, and incidents can become community sessions, standards, reference updates, or paved capabilities. Communities can generate candidate practices; authorized governance adopts mandatory ones. Forum findings must not expose confidential or personal data in broad community channels.

**Measure distinct outcomes.** For communities, observe participation breadth, newcomer progression, reciprocal contribution, cross-boundary connections, artifact use, competence transfer, and member-reported value. For review forums, observe decision latency, wait and preparation, late rework, evidence gaps, recurrence, dissent disposition, conditions, incidents, exceptions, and affected outcomes. Attendance, meeting count, approval rate, and document count are activity measures.

**Renew or retire.** Communities can split, merge, change domain, or end when learning energy disappears. Forums should be reviewed when decision classes, automation, organizational authority, risk, or demand changes. Remove forums whose work is safely delegated. Preserve decision records and learning even when the meeting structure ends.

## Definitions and Notation

Let $F=(P,S,R,A,I,O,D,C,L)$. Purpose $P$ states the outcome. Scope $S$ lists included and excluded decision classes. $R$ defines membership, participation, and representation. $A$ defines advisory, decision, risk, assurance, and execution roles. $I$ defines intake, evidence, preparation, and process. $O$ defines outputs, records, conditions, and closure. $D$ defines dissent, conflicts, appeal, and escalation. $C$ defines qualified capacity, cadence, service expectations, and overload action. $L$ defines learning, evaluation, renewal, and retirement.

For review class $i$ in a planning window, let arrival count be $n_i$ and mean qualified effort be $s_i$ minutes. Let $m$ reviewers each contribute $h$ review hours and let $f\in(0,1]$ reserve usable focus after coordination and other duties. Planned load and nominal capacity are

$$
W=\sum_i n_i s_i,\qquad H=60mhf.
$$

The ratio $\rho=W/H$ is a planning signal, not a queueing theorem. It ignores burst timing, service-time variation, skill constraints, absence, dependencies, and rework. A value below one does not guarantee timely review.

A **community** learns through practice. A **committee** is a formally constituted group. A **forum** is a setting for interaction. A **board** usually implies governance but needs explicit delegation. A **guild** is only a label. **Consensus** is a decision process; **authority** determines who may decide; **assurance** evaluates claims. These dimensions can combine but must remain visible.

## Mechanisms, Invariants, or Proof Structure

### Act-authority invariant

Every durable output identifies whether it is learning, advice, decision, risk acceptance, assurance, or execution and names the responsible role. Advice cannot be reported as approval; group participation cannot erase the accountable decision maker.

### Representation-and-gap invariant

Each decision-critical concern has an appropriate participant or a recorded evidence and authority gap. Attendance by one senior leader does not prove representation of operators, users, specialists, suppliers, or affected communities.

### Objection-disposition invariant

Every material objection is recorded as accepted, mitigated, answered with rationale and evidence, referred, or unresolved. Majority support and deadline pressure are not dispositions. The authorized decision may proceed with unresolved dissent only when that consequence and authority are explicit.

### Capacity-integrity invariant

When demand exceeds qualified capacity, the system changes scope, delegation, staffing, or commitments. It does not preserve throughput by silently removing evidence, representation, reasoning, or records.

### Executable capacity screen

<!-- bijux-verify: {"id":"review-capacity-screen","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"routine-heavy: load=660 capacity=864 rho=0.76 status=headroom\ncross-domain-burst: load=1050 capacity=864 rho=1.22 status=overload\nscarce-specialist: load=300 capacity=144 rho=2.08 status=overload\n","stderr":""}} -->
```python
def screen(name, reviews, reviewers, hours, focus):
    load = sum(count * minutes for count, minutes in reviews)
    capacity = reviewers * hours * 60 * focus
    rho = load / capacity
    status = "headroom" if rho <= 0.8 else "overload" if rho > 1 else "tight"
    print(f"{name}: load={load} capacity={capacity:.0f} rho={rho:.2f} status={status}")

screen("routine-heavy", [(12, 30), (3, 100)], 3, 8, 0.6)
screen("cross-domain-burst", [(5, 90), (4, 150)], 3, 8, 0.6)
screen("scarce-specialist", [(3, 100)], 1, 4, 0.6)
```

The thresholds are fictional planning policy. The calculation does not model queues or prove reviewer competence, quality, fairness, or response time.

### Proposition: unanimous attendance cannot prove legitimate approval

Suppose every attendee supports a design, but the forum is advisory and the data-protection authority required for the decision is absent. Attendance is unanimous while the forum lacks decision authority and a required concern remains unresolved. This counterexample refutes the implication from unanimous room agreement to legitimate approval.

### Proposition: higher approval rate cannot prove better review

Forum A approves every proposal after superficial inspection; Forum B defers some proposals until evidence gaps close and delegates trivial decisions before intake. A's approval rate is higher, yet nothing follows about decision quality, latency, burden, or outcomes. Approval percentage has no unconditional monotone relationship to forum effectiveness.

## Alternatives and Trade-Offs

**Community versus center of excellence.** A community distributes learning and connects practice, but participation and artifact maintenance can be uneven. A funded expert center offers concentrated capacity and accountability, but can become a queue and detach from work. Combine enabling specialists and communities when roles, funding, and exit are explicit.

**Asynchronous review versus meetings.** Written review broadens time-zone access, preserves reasoning, and reduces scheduling. Synchronous discussion helps resolve coupled disagreement and build shared understanding. Use async preparation by default and meetings for unresolved interaction, not status recital.

**Open membership versus selected representation.** Open communities encourage discovery and newcomers. Decision forums need bounded participants and authority, but selection can exclude affected voices. Publish criteria, rotate roles, invite concern owners, and record gaps.

**Consensus versus accountable decision.** Consensus can improve commitment and reveal objections but may deadlock or hide compromise. Accountable decision is faster and clearer but can ignore knowledge if consultation is weak. Use time-bounded deliberation, substantive objection handling, explicit authority, dissent records, and appeal.

**Central forum versus federated review.** Centralization supports cross-domain consistency and scarce expertise but creates distance and queues. Federation keeps context local but needs shared semantics, escalation, and assurance. The next module develops this boundary in depth.

**Recorded transparency versus confidentiality.** Broad records improve learning and accountability; security, privacy, personnel, legal, and supplier evidence may need restriction. Separate protected evidence from a durable decision summary that exposes scope, authority, rationale, conditions, and limitations.

## Failure Modes and Misconceptions

1. **A guild is automatically a community of practice.** Shared practice and learning must exist.
2. **A community can approve architecture.** It needs explicit delegated authority to make decisions.
3. **A board name creates governance.** Authority, scope, and accountability must be defined.
4. **More attendees improve representation.** Concern coverage and ability to contribute matter.
5. **Senior architects represent all users.** Status does not confer lived or specialist evidence.
6. **Psychological safety means no criticism.** It enables candid, respectful technical challenge.
7. **Consensus means unanimity.** Legitimate processes may proceed after substantive objections are addressed.
8. **A vote resolves technical objections.** Votes measure preferences under a rule; they do not answer mechanisms or evidence.
9. **Every architecture change needs the forum.** Routine in-envelope decisions should be delegated.
10. **A meeting is the review.** Intake, evidence, preparation, decisions, conditions, and closure form the review.
11. **Green means assured.** Scope, evidence, independence, conditions, and expiry bound assurance.
12. **Confidential means unrecorded.** Protect evidence while retaining accountable summaries.
13. **Fast decisions prove efficiency.** Missing preparation or challenge can shift cost into rework and incidents.
14. **Approval rate measures quality.** It is easily gamed through intake and superficial review.
15. **Communities replace funded support.** Volunteers cannot own mandatory service or incident obligations.
16. **One time zone is sufficient for an open forum.** Access barriers distort participation and evidence.
17. **Repeated exceptions are isolated cases.** Clusters can reveal obsolete policy or missing capability.
18. **Forums should persist indefinitely.** Changed scope or safe delegation can make them unnecessary.

## Worked Examples

### Example 1

**Separate community learning from approval.** An architecture guild runs monthly incident clinics and maintains pattern examples. Teams begin describing its informal recommendations as mandatory. The guild publishes a charter stating that it learns and advises, labels artifacts by evidence and status, and routes proposed requirements to authorized governance. **Conclusion:** protecting voluntary learning requires an explicit boundary from authority.

### Example 2

**Expose the real decision maker.** A review forum advises against a cross-domain integration, but an executive proceeds and later says “architecture approved it.” The record identifies the forum's advisory output, the executive's decision and risk ownership, dissent, evidence, conditions, and revisit trigger. **Conclusion:** group deliberation must not diffuse accountable decision authority.

### Example 3

**Remove routine review load.** A board reviews every supported library update and accumulates a six-week queue. Most changes are local, reversible, within compatibility policy, tested, and rollback-capable. Delegate them under automated evidence and peer review; retain forum review for shared protocols, unsupported runtimes, and nonconformance. **Conclusion:** proportional routing protects scarce review capacity and team autonomy.

### Example 4

**Recompute forum capacity.** Three reviewers each have eight hours per planning window, but only 60% is usable after coordination. Capacity is $3\times8\times60\times0.6=864$ minutes. A burst of five 90-minute and four 150-minute reviews needs $1{,}050$ minutes, so $\rho=1.22$. Narrowing preparation would corrupt quality; the forum instead moves routine work, adds specialists, or changes commitments. **Conclusion:** overload should change the system, not silently weaken review.

### Example 5

**Record a representation gap.** A customer-identity proposal includes developers, security, and product leadership but no support staff, accessibility expertise, privacy authority, or people affected by account recovery. Rather than claiming broad stakeholder review, the facilitator records gaps, gathers research and specialist input, and defers decisions those authorities must make. **Conclusion:** a crowded room can remain evidentially incomplete.

### Example 6

**Handle a minority technical objection.** Ten participants prefer a shared event schema; one domain expert shows that its time model cannot represent corrections required by the domain. The chair does not call a vote. The group traces examples, adds bitemporal semantics, or records why another design addresses the issue. **Conclusion:** minority size does not determine technical validity.

### Example 7

**Protect confidential assurance evidence.** A forum reviews a supplier's sensitive penetration report. Access is restricted, but the durable decision summary records exact supplier scope, product version, period, exclusions, assessor relationship, unresolved findings, conditions, owner, and expiry. **Conclusion:** confidentiality constrains disclosure, not accountable reasoning.

### Example 8

**Connect community learning to a paved capability.** Several teams bring opaque identity-policy failures to community clinics. Anonymized evidence shows the same missing preview and inconsistent error codes. The platform team builds a shared explanation capability; governance versions the applicable rule; the forum's exception volume falls. **Conclusion:** repeated social-learning evidence should improve durable system capability.

### Example 9

**Diagnose a gamed approval metric.** A forum reports 99% approval by rejecting incomplete proposals before they receive case IDs and approving the remainder conditionally. Teams report long informal pre-review and unresolved conditions. Measure discovery-to-decision, total wait, preparation, returns, conditions, closure evidence, late rework, incidents, and user experience across all attempted cases. **Conclusion:** denominator design can turn approval rate into theater.

### Example 10

**Transfer the model to regional public health.** A review forum considers exchange of outbreak data among clinics, laboratories, public authorities, and researchers. It distinguishes public-health authority, clinical responsibility, privacy and legal authority, technical advice, and independent assurance; includes affected communities and accessibility; protects patient evidence; records dissent and jurisdictional gaps; and supports emergency timing with retrospective closure. **Conclusion:** architecture forums coordinate technical reasoning but cannot invent public authority or waive rights.

## Cross-Program Connections

- [SARCH-070](070-running-an-evidence-based-architecture-review.md) supplies claims, scenarios, evidence assessment, findings, and closure.
- [SARCH-082](082-team-topologies-and-architecture.md) supplies platform, enabling, complicated-subsystem, and stream-aligned interaction boundaries.
- [SARCH-083](083-architecture-governance-models.md) supplies decision rights, delegation, assurance, exceptions, and accountability.
- [SARCH-084](084-standards-principles-and-guardrails.md) supplies the governed instruments that community learning may propose but cannot authorize by itself.
- [SARCH-086](086-reference-architectures.md) supplies knowledge products whose creation and evolution need communities and governed review.
- [PLAT-094](../../29-platform-engineering/modules/094-support-models-and-enabling-teams.md) distinguishes funded support, communities of practice, and bounded enabling engagements.
- [DARCH-071](../../20-data-architecture-engineering/modules/071-federated-data-governance.md) applies communities and federated authority to data domains.

## References

1. Jean Lave and Etienne Wenger. *Situated Learning: Legitimate Peripheral Participation*. Cambridge University Press, 1991.
2. Etienne Wenger. *Communities of Practice: Learning, Meaning, and Identity*. Cambridge University Press, 1998.
3. John Seely Brown and Paul Duguid. “Organizational Learning and Communities-of-Practice: Toward a Unified View of Working, Learning, and Innovation.” *Organization Science* 2(1), 1991, pp. 40–57. [DOI](https://doi.org/10.1287/orsc.2.1.40).
4. Etienne Wenger-Trayner and Beverly Wenger-Trayner. “Communities of Practice.” Current author-maintained overview. [Official author page](https://www.wenger-trayner.com/communities-of-practice/). Retrieved 2026-09-06.
5. Etienne Wenger-Trayner, Beverly Wenger-Trayner, Phil Reid, and Claude Bruderlein. *Communities of Practice Within and Across Organizations: A Guidebook*. 2nd ed., Social Learning Lab. [Official guidebook page](https://www.wenger-trayner.com/cop-guidebook/). Retrieved 2026-09-06.
6. Amy Edmondson. “Psychological Safety and Learning Behavior in Work Teams.” *Administrative Science Quarterly* 44(2), 1999, pp. 350–383. [DOI](https://doi.org/10.2307/2666999).
7. Nicole Forsgren, Dustin Smith, Jez Humble, and Jessie Frazelle. *2019 Accelerate State of DevOps Report*. DORA and Google Cloud, 2019. [Official report page](https://dora.dev/research/2019/dora-report/). Retrieved 2026-09-06.
8. ISO/IEC/IEEE. *ISO/IEC/IEEE 42020:2019, Software, systems and enterprise — Architecture processes*. Edition 1, July 2019; published, marked to be revised. [Official ISO record](https://www.iso.org/standard/68982.html). Retrieved 2026-09-06.
9. ISO/IEC/IEEE. *ISO/IEC/IEEE 42010:2022, Software, systems and enterprise — Architecture description*. Edition 2, November 2022. [Official ISO record](https://www.iso.org/standard/74393.html). Retrieved 2026-09-06.
10. Pete Resnick. *RFC 7282: On Consensus and Humming in the IETF*. Informational, June 2014. [Official RFC Editor record](https://www.rfc-editor.org/info/rfc7282). Retrieved 2026-09-06.
11. Matthew Skelton and Manuel Pais. *Team Topologies: Organizing Business and Technology Teams for Fast Flow*. 2nd ed., IT Revolution, 2025.
12. Michael Nygard. “Documenting Architecture Decisions.” 15 November 2011. [Author's article](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions). Retrieved 2026-09-06.

## Exercises

### Exercise 1

Distinguish a community of practice, working group, design clinic, advisory review forum, decision board, and assurance body. Explain why the label “architecture guild” is insufficient.

### Exercise 2

Trace a cross-domain API decision from intake through asynchronous preparation, forum discussion, technical objection, advice, accountable decision, conditions, closure evidence, community learning, and revisit trigger. Identify each distinct act and authority.

### Exercise 3

A weekly forum has four reviewers with six hours each at 50% usable focus. It expects eight 45-minute routine reviews, four 120-minute cross-domain reviews, and two 180-minute assurance cases. Recompute load, capacity, and $\rho$; diagnose why the arithmetic remains insufficient and propose a safe response.

### Exercise 4

Design a paired community and review-forum system for an organization with six domains, one platform team, scarce security expertise, and teams across four time zones. Address learning, authority, representation, routing, accessibility, capacity, records, and measurement.

### Exercise 5

Design an architecture review forum for an AI-assisted benefits-eligibility system in public administration. Address affected people, authority, evidence, privacy, accessibility, bias, security, appeals, vendor conflicts, dissent, confidentiality, monitoring, emergency changes, and limits of architectural review.

## Answers to the Exercises

### Answer 1

A community of practice sustains peer learning in a domain. A working group produces a bounded artifact and ends. A design clinic offers early collaborative advice. An advisory forum challenges a proposal but does not decide. A decision board has delegated authority for declared classes. An assurance body evaluates claims with stated independence and scope. “Architecture guild” may name any mixture and says nothing about membership, authority, evidence, outputs, or accountability. Its charter and observed behavior must identify the actual mechanism.

### Answer 2

Intake records the requested API decision, stakeholders, options, scenarios, evidence, owner, and deadline. Asynchronous review produces questions, conflict declarations, and concern-specific objections. In the forum, facilitation separates mechanism and evidence from preference. The forum issues advice unless delegated to decide. A named authority makes and records the decision; specialist authorities retain security, privacy, or other reserved acts. Conditions name owners and observations for closure. Anonymized recurring learning enters the community and may improve a standard, reference, or path through its proper authority. The decision record includes assumptions and triggers such as consumer growth, contract change, incidents, or evidence expiry. Learning, advice, assurance, decision, implementation, and risk acceptance remain distinct.

### Answer 3

Load is $8\times45+4\times120+2\times180=1{,}200$ minutes. Nominal capacity is $4\times6\times60\times0.5=720$ minutes, so $\rho=1{,}200/720\approx1.67$: planned demand exceeds capacity by 480 minutes. The model ignores arrival bursts, reviewer skill, conflicts, absence, preparation variation, rework, and response targets. Delegate routine in-envelope cases to peer and automated evidence, reserve scarce specialists for relevant concerns, improve asynchronous preparation, add funded qualified capacity, or change delivery commitments. Do not preserve apparent throughput by dropping evidence or representation.

### Answer 4

Create an open architecture community with rotating time-zone sessions, asynchronous case discussions, accessible artifacts, mentoring, incident learning, and domain contributions. It has no approval authority. Create a federated review forum with one empowered representative per relevant domain, platform participation, on-demand security, a trained facilitator and recorder, explicit advisory or decision delegation, conflict declarations, and an appeal route. Local reversible in-envelope decisions stay with teams; cross-domain contracts, novel threats, and nonconformance enter the forum. Use async briefs and written objections before synchronous discussion. Publish durable summaries with protected annexes. Track participation breadth, newcomer growth, knowledge use, total review wait, preparation, dissent disposition, conditions, recurrence, and outcomes. Fund security capacity and do not make office hours the only route.

### Answer 5

The forum cannot create lawful public authority. Its charter names the benefits authority as decision owner and preserves independent legal, privacy, accessibility, security, procurement, and equality responsibilities. Representation includes applicants, rejected applicants, disability and language advocates, case workers, appeals staff, data owners, security, social-policy experts, affected communities, and vendor-independent technical expertise. Evidence covers data provenance and representativeness, model and rule behavior, error distribution, explanations, human review, accessibility, privacy, threats, outages, appeals, vendor claims, and alternatives, with protected sensitive material and accountable summaries. Conflicts and dissent are recorded; technical votes do not erase objections. Conditions require owners, deadlines, monitoring, appeal access, rollback, and closure evidence. Emergency changes use preauthorized bounded routes and retrospective review. Architecture review can assess mechanisms and evidence but cannot prove fairness, legality, dignity, public legitimacy, or absence of harm; continuing independent oversight and affected-person remedy remain necessary.
