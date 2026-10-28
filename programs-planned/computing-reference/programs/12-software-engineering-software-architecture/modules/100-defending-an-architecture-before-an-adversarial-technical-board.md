---
module_id: SARCH-100
program: Software Engineering: Software Architecture
level: 2
module_number: 100
title: Defending an Architecture Before an Adversarial Technical Board
status: complete
last_verified: 2026-09-06
---

# Defending an Architecture Before an Adversarial Technical Board

## One-Page Review

### Governing question

How can an architect defend a consequential recommendation under rigorous challenge while keeping claims traceable, uncertainty visible, authority legitimate, and the board focused on finding consequential error rather than rewarding confidence or performance?

### Essential definitions

- an **adversarial technical board** is an authorized review forum whose members actively seek counterexamples, unsupported assumptions, failure paths, and superior alternatives;
- a **review charter** fixes the decision, scope, architecture revision, authorities, participants, evidence cutoff, success criteria, outputs, and conduct;
- a **claim** is a bounded proposition about the architecture; a **top claim** supports the requested decision;
- an **argument** connects evidence and assumptions to a claim through explicit reasoning;
- **evidence** is an identified observation, test, analysis, record, or authoritative source with provenance, context, date, and limitations;
- an **assumption** is a premise not established by the current evidence; a **defeater** is a condition or counterargument that could invalidate a claim or its support;
- **burden of production** is the duty to supply enough evidence or reasoning for an issue to be considered; **decision authority** is the legitimate power to accept a recommendation or residual risk;
- a **disposition** records a challenge as supported, conditionally supported, unresolved, refuted, or outside the charter, with rationale;
- **residual risk** remains after controls and evidence; an **action** has an owner, due date, acceptance evidence, and decision consequence;
- **adversarial** describes rigorous opposition to claims, not hostility toward people.

### Central model, mechanism, or theorem

Model the defense as a typed argument graph

$$
G=(C,E,A,D,R),
$$

where $C$ is claims, $E$ evidence, $A$ assumptions, $D$ defeaters, and $R$ typed support or challenge relations. Every decision-critical claim names scope and consequence; every evidence item names revision, environment, method, provenance, date, and limitations; every material defeater receives a disposition.

A useful structural coverage measure is

$$
K=\frac{\sum_{c\in C_*}w(c)I(c\text{ has a permitted disposition})}
        {\sum_{c\in C_*}w(c)},
$$

for critical claims $C_*$. $K=1$ is neither proof nor approval: the claim set may be incomplete, evidence invalid, assumptions false, or authority absent. Readiness is therefore a conjunction of gates, not a confidence score.

### Critical invariants

- the board reviews one named architecture revision against one decision and operating context;
- entrance and success criteria are agreed before advocacy begins;
- top claims trace to scenarios, mechanisms, evidence, assumptions, and defeaters;
- observations, calculations, forecasts, judgments, preferences, and authoritative decisions remain distinct;
- evidence limitations and negative results are presented with favorable results;
- a citation, dashboard, prototype, test, or assurance diagram never proves more than its method and context support;
- critical unknowns are stated with bounds, resolution action, and decision consequence;
- reviewers challenge comparable candidates symmetrically and disclose conflicts of interest;
- affected stakeholders and specialist authorities are represented or recorded as a review gap;
- the chair protects rigorous dissent and stops personal attack, repetition, and scope capture;
- no presenter may accept legal, safety, privacy, security, accessibility, financial, or public-policy risk outside delegated authority;
- every condition has an owner, deadline, closure evidence, and consequence; minutes preserve dissent and rationale.

### Common failures

Common failures include reviewing an unnamed diagram; hiding behind slide volume; rehearsing slogans instead of claims; treating all questions as objections; bluffing an unknown; citing a test from the wrong workload; multiplying correlated evidence; using “industry standard” without a source; confusing control presence with effectiveness; presenting only the preferred candidate; changing success criteria during the meeting; accepting action items with no closure evidence; letting hierarchy suppress dissent; tolerating personal hostility; and calling a time-boxed presentation “proof.”

### Compact example

A board asks whether regional failover meets a 60-second recovery gate. The architect does not answer “we are multi-region.” She identifies claim C7, the exact revision, and a test that isolated one application region but not identity or the control plane. She states that the evidence supports component recovery only, leaves the end-to-end claim unresolved, proposes a production-shaped isolation exercise, names the owner and integrity measures, and says approval must remain conditional. The defense succeeds by exposing the real boundary, not by winning the exchange.

### Connections

[SARCH-070](070-running-an-evidence-based-architecture-review.md) supplies the review mechanism, [SARCH-091](091-architecture-for-regulated-and-safety-critical-systems.md) supplies authority and assurance boundaries, and [SARCH-099](099-comparing-multiple-viable-architectures.md) supplies candidate comparison. This final module integrates the program into defensible professional judgment.

## Governing Question

Architecture defense is not a speech contest. A technically consequential decision may affect service continuity, public rights, safety, privacy, cost, staff workload, and years of change. A board earns its cost by finding an invalid premise, missing stakeholder, unsafe transition, or better alternative before reality does.

The architect's task is neither to surrender at the first objection nor to preserve a preferred design at all costs. It is to make the recommendation, argument, and uncertainty inspectable; answer within the evidence; incorporate valid challenge; and enable the proper authority to decide. A good defense can end in rejection. A confident approval based on a false claim is failure.

## Why This Matters

Architecture descriptions organize concerns, viewpoints, and models, while architecture evaluation judges an architecture against stated concerns and criteria [1], [2]. ATAM demonstrates the value of stakeholder scenarios, risks, sensitivity points, and trade-off points [3]. A final board builds on these disciplines but adds an asymmetric setting: the proponent has prepared a recommendation, reviewers deliberately search for defeaters, and an authority must decide what follows.

High-pressure forums amplify bias. Status, eloquence, slide polish, sunk cost, and deadline pressure can displace evidence. Conversely, indiscriminate criticism can make every claim impossible to satisfy. A governed process defines the decision, the burden for each kind of claim, permitted outcomes, and respectful conduct before the room becomes adversarial.

## Prerequisites and Retrieval

Retrieve stakeholder, concern, quality-attribute scenario, architecture view, constraint, invariant, risk, sensitivity point, trade-off point, evidence, confidence, assurance case, threat model, fitness function, lifecycle cost, migration state, decision record, exception, residual risk, and authority.

From SARCH-001 through SARCH-030 retrieve drivers and audience-specific descriptions. SARCH-051 through SARCH-070 supply distributed failure and evaluation. SARCH-071 through SARCH-090 supply evolution and governance. SARCH-091 through SARCH-099 supply difficult contexts and comparative judgment. The board defense is an integration exercise, not a substitute for those analyses.

## Learning Objectives

After completing this module, you should be able to:

1. charter an adversarial board around a precise decision and authority;
2. build a claim–argument–evidence map with assumptions and defeaters;
3. select evidence proportionate to consequence and identify its limits;
4. prepare a compact decision packet whose assertions are traceable;
5. answer hostile-to-the-claim questions without bluffing or evasion;
6. distinguish factual dispute, model uncertainty, value conflict, and authority question;
7. use counterexamples, negative evidence, and alternative architectures constructively;
8. preserve psychological safety without weakening technical challenge;
9. produce bounded approval, conditions, actions, residual risks, and reopening triggers;
10. recognize when the honest recommendation is defer, revise, or reject.

## Core Exposition

**Charter the decision.** State the decision requested in one sentence: approve a target architecture, authorize a reversible experiment, accept a migration state, or release a bounded capability. Name the architecture revision, system boundary, populations, environments, operational horizon, deadline, evidence cutoff, and alternatives. “Review the architecture” is not a decision.

Identify the convening authority and delegated authorities. A chief architect may decide conformance to an internal platform rule but not waive law, safety obligations, privacy rights, budget authority, or an operator's acceptance duty. Record which specialists advise, which authorities concur, and who owns the final decision.

Define entrance criteria: packet delivered, revision frozen, open questions indexed, evidence accessible, reviewers conflict-checked, required roles present, and known critical gaps declared. Define success criteria as decision readiness, not automatic approval. NASA systems-engineering guidance makes entrance and success criteria explicit for technical reviews and distinguishes an independent standing review board from the project team [6]. Its aerospace process is an instructive calibration, not a universal software mandate.

**Choose an adversarial contract.** “Adversarial” means reviewers try to falsify important claims, produce counterexamples, expose missing scope, and compare alternatives. They challenge the strongest version of the recommendation. Personal ridicule, identity attack, interruption as dominance, surprise scope expansion, and repeated demands already answered are process failures.

The chair enforces equal question access, relevance, evidence citation, time, and conduct. A scribe captures questions and dispositions. An evidence steward resolves artifact identities. A decision authority does not simultaneously suppress dissent. For high-stakes reviews, include independent domain, operations, security, data, accessibility, safety, and affected-user perspectives as applicable.

**Build the top-level argument.** Begin with a bounded claim: “Architecture revision R is fit for decision D in context X through horizon H, subject to conditions Q.” Decompose it by mission outcomes, mandatory constraints, failure and recovery, security/privacy, data integrity, performance/capacity, change, operability, lifecycle cost, transition, and exit.

For each subclaim, record reasoning, evidence, assumptions, and defeaters. Goal Structuring Notation version 3 provides a current community standard for structuring engineering arguments [4]. A neat assurance diagram does not make its premises true. The graph is valuable because it makes unsupported leaves, context, and counterargument visible.

**Calibrate the burden.** The proponent bears the burden of supporting positive claims used to justify the decision. A reviewer who asserts a specific defect should provide a mechanism, counterexample, source, or discriminating question sufficient to make it actionable. The proponent need not prove that no imaginable failure exists; the packet must address the declared context and credible threats proportionately to consequence.

Burden rises with consequence, irreversibility, uncertainty, novelty, privilege, and affected population. A reversible internal experiment needs different evidence from an irreversible clinical cutover. Mandatory gates remain noncompensatory. NIST SP 800-160 Volume 1 Revision 1 treats trustworthiness and security as lifecycle engineering concerns in contested environments [5]; a board cannot replace that engineering with a late checklist.

**Make evidence address the exact claim.** An evidence item states what was observed, by whom, using what method, against which revision, workload, configuration, environment, date, sample, and acceptance criterion. It records outputs and limitations. A unit test supports a component behavior, not regional recovery. A vendor benchmark supports its disclosed configuration, not the board's workload. An analytical proof supports its conclusion only under its premises.

Triangulation uses meaningfully different methods or assumptions. Ten dashboards sourced from one instrumentation defect are one evidence lineage. Two tests sharing the same simulator and fixture are not independent confirmation. Record common causes rather than multiplying confidence.

**Prepare the decision packet.** The pre-read should let a reviewer reconstruct the recommendation without the presenter. Include:

1. decision requested, authority, scope, revision, horizon, and deadline;
2. stakeholders, mandatory gates, prioritized scenarios, and unresolved representation gaps;
3. current and target context, responsibility, runtime, data, deployment, security, operation, delivery, organization, migration, and exit views;
4. considered candidates and the strongest case for each;
5. chosen candidate, trade-offs, transition states, and last reversible point;
6. claim map with evidence, assumptions, defeaters, confidence, and artifact links;
7. negative results, incidents, boundary tests, and rejected hypotheses;
8. residual risks, owners, conditions, review triggers, dissent, and explicit asks.

Use stable claim and evidence IDs. Keep the main packet compact and put reproducible detail behind it. Every chart names units, population, aggregation, time window, source, and revision. Every diagram has semantics. Normative words such as “must” or “shall” identify their authority rather than borrowing force from typography.

**Open with the decision, not history.** In the opening, state the ask, context, binding constraints, recommendation, three controlling claims, decisive evidence, leading alternative, accepted trade-offs, residual risks, and unknowns. Show how the architecture behaves under a representative success scenario and a representative failure scenario.

Do not spend the question budget narrating team chronology. Reviewers can read. The opening creates a falsifiable map: if a controlling claim falls, everyone knows what part of the recommendation changes.

**Use a disciplined answer protocol.** First restate the question and identify its type:

- **clarification:** what does the model or term mean?
- **factual challenge:** what observation supports the claim?
- **mechanism challenge:** why should the design produce that response?
- **premise challenge:** what if a workload, dependency, or policy assumption is false?
- **counterexample:** can one case falsify the general statement?
- **alternative:** why not another architecture or transition?
- **value conflict:** which consequence matters more?
- **authority challenge:** who may accept or waive this condition?

Then answer in four parts: conclusion; evidence or reasoning; boundary/uncertainty; decision consequence. If the answer is unknown, say so, state the best current bound, explain why it matters, name the resolving action, and state whether the decision must defer or can proceed conditionally. Never invent certainty under pressure.

**Track the question live.** The scribe records question ID, linked claim, asker, answer, evidence, disposition, action, owner, deadline, closure evidence, and decision consequence. Spoken agreement is not closure. If the question cannot be resolved synchronously, the board assigns a disposition without forcing an improvisation.

Separate “the board understands the answer” from “the board accepts the risk.” Technical comprehension, evidence adequacy, policy choice, and residual-risk acceptance are different acts.

**Invite attacks on controlling assumptions.** Publish the assumptions most capable of reversing the decision: demand growth, hot-key distribution, identity availability, consistency needs, staff capacity, supplier behavior, migration duration, restore time, or regulatory interpretation. Ask reviewers to construct the smallest counterexample.

Run scenario probes: dependency loss, overload, corrupt data, malicious insider, compromised credential, inaccessible client, old version, rollback, control-plane loss, staff unavailability, supplier exit, and concurrent migration failure. Trace detection, containment, degraded behavior, recovery, reconciliation, and evidence. A board that discusses only nominal boxes has not reviewed the architecture.

**Defend alternatives fairly.** Present the leading rejected alternative at its strongest, with equivalent scope and supporting services. State the conditions under which it becomes preferable. If the preferred architecture received a prototype and the alternative received guesses, the comparison is biased.

SARCH-099's gates, dominance, uncertainty, sensitivity, transition, and reversibility remain in force. The final board should be able to distinguish “candidate loses under present evidence” from “candidate is bad.”

**Expose negative evidence.** Failed tests, incidents, contradictory measurements, and abandoned assumptions are decision assets. Explain the defect found, the model changed, the mitigation, and the retest. Hiding negative evidence corrupts the board's inference and usually makes the residual risk larger.

Absence of observed failure is weak when exposure is low or detection poor. Conversely, one failed test does not prove every architecture instance fails; it may falsify a universal claim or reveal an invalid test. Match inference to design and sample.

**Control quantitative claims.** Show raw values before normalized scores. State units, intervals, distributions, censoring, and scenario. Do not equate structural coverage with truth. If a risk model uses

$$
R=\sum_j p_jL_j,
$$

state how probabilities and losses were estimated, their dependencies, and what is excluded. Do not price legal duties, dignity, or catastrophic safety consequences merely to make them tradeable.

Avoid false precision. A predicted 99.95% availability derived from guessed failure independence is not stronger than its assumptions. Sensitivity and break-even points are more useful than extra decimals.

**Manage disagreement by kind.** Factual disagreement calls for evidence. Model disagreement calls for competing predictions and a discriminating test. Value disagreement calls for legitimate stakeholder deliberation. Authority disagreement calls for governance or legal clarification. Interest conflict requires disclosure and sometimes recusal.

Consensus is not a truth criterion. Preserve minority rationale, especially when a reviewer identifies a credible high-consequence defeater. Equally, one reviewer does not gain an unlimited veto unless the charter or governing authority grants it.

**Protect the people while attacking the claim.** Psychological safety allows a junior operator to say the restore runbook failed and a security reviewer to expose a threat without retaliation. It does not mean shielding the architecture from precise criticism. The chair interrupts personal attacks, demands concrete claim references, and rotates participation.

The ACM Code of Ethics requires computing professionals to contribute to society, avoid harm, be honest and trustworthy, and respect privacy [12]. Those duties argue against deceptive certainty and against review conduct that silences people who hold material evidence.

**Use bounded outcomes.** Define outcome semantics before the meeting:

- **approve:** current evidence supports the scoped decision with recorded residual risk;
- **approve with conditions:** named noncritical conditions may close after authorization, with consequences if they fail;
- **defer:** a decision-critical uncertainty has an achievable evidence action;
- **revise and return:** architecture or argument needs material change;
- **reject:** a gate fails, a controlling claim is refuted, or the recommendation is inferior under the authorized frame;
- **outside authority:** the board cannot make the requested decision.

Never label an unresolved critical gate “conditional” merely to meet a date. Conditions are not a parking lot. Each has closure evidence and an authority who can decide its significance.

**Close the review as an evidence process.** Publish minutes, dispositions, decision rationale, dissent, conditions, actions, and the exact approved revision. Resolve factual transcription errors without erasing disagreement. Link the decision record to implementation constraints and fitness checks.

Reopen on named triggers: evidence failure, architecture drift, incident, workload threshold, regulatory change, supplier change, missed migration checkpoint, assumption expiry, or new affected population. Google SRE's production-readiness material treats readiness as part of an ongoing engagement and improvement model, not a one-time transfer ritual [7].

**Know what a successful defense proves.** It proves only that a governed review considered the named recommendation using the recorded participants, arguments, evidence, and conditions at a time. It cannot prove all defects absent, guarantee production outcomes, confer missing authority, or substitute for external certification. Its value is better error discovery, clearer accountability, and a more reversible, auditable decision.

## Definitions and Notation

Let $C$ be claims, $C_*\subseteq C$ decision-critical claims, $E$ evidence, $A$ assumptions, $D$ defeaters, and $R$ typed relations. A claim is a tuple

$$
c=(\text{statement},\text{scope},\text{revision},\text{authority},\text{consequence}).
$$

An evidence item is

$$
e=(\text{artifact},\text{method},\text{environment},\text{revision},\text{date},\text{provenance},\text{limitations}).
$$

Let $d(c)$ be a disposition and $I(P)$ be 1 when proposition $P$ holds and 0 otherwise. Structural coverage $K$ weights disposed critical claims, but does not measure validity or truth. Let $Q$ be review gates, such as required authority present, revision identified, critical claims traced, and material defeaters disposed. Review readiness requires $\bigwedge_{q\in Q}q$.

## Mechanisms, Invariants, or Proof Structure

**Necessary-not-sufficient proposition.** Suppose the charter requires every critical claim to have a permitted disposition before decision. Then $K=1$ is necessary under that definition. It is not sufficient for a sound decision. Counterexample: every claim is marked supported by a benchmark run against the wrong architecture revision. Coverage is 1, but the evidence is irrelevant, so the recommendation remains unsupported.

**Defeater discipline.** A rebutting defeater supplies reason the claim is false; an undercutting defeater attacks the support relation, such as an invalid workload or shared measurement fault. A defeater can be refuted, mitigated, accepted as residual risk by proper authority, made a condition, or left unresolved. Deleting it is not a disposition.

**Evidence dependence.** If two evidence items share instrumentation, data, implementation, or assumptions, treating their likelihood contributions as independent overstates confidence. Independence must be argued, not inferred from artifact count.

**Executable packet preflight.** This checker enforces a few structural entrance gates. It decides only whether a packet is ready to review; it neither validates evidence nor approves the architecture.

<!-- bijux-verify: {"id":"preflight-board-packet","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"ready=ready_for_review\nmissing-revision=not_ready:architecture revision is missing\nunresolved=not_ready:critical claim C2 is unresolved\nstale=not_ready:evidence E1 is stale (250 days)\nopen-defeater=not_ready:defeater D1 has no disposition\nmissing-authority=not_ready:decision authority is missing\n","stderr":""}} -->
```python
def preflight(packet):
    if not packet.get("revision"):
        return "not_ready:architecture revision is missing"
    if not packet.get("authority"):
        return "not_ready:decision authority is missing"
    for claim in packet["claims"]:
        if claim["critical"] and claim["disposition"] not in {"supported", "conditional"}:
            return f"not_ready:critical claim {claim['id']} is unresolved"
        for evidence_id in claim["evidence"]:
            age = packet["evidence"][evidence_id]["age_days"]
            if age > 180:
                return f"not_ready:evidence {evidence_id} is stale ({age} days)"
    for defeater in packet["defeaters"]:
        if not defeater.get("disposition"):
            return f"not_ready:defeater {defeater['id']} has no disposition"
    return "ready_for_review"

def packet(revision="arch-7f31", authority="service-risk-owner",
           c2="conditional", e1_age=20, d1="mitigated"):
    return {
        "revision": revision,
        "authority": authority,
        "claims": [
            {"id": "C1", "critical": True, "disposition": "supported", "evidence": ["E1"]},
            {"id": "C2", "critical": True, "disposition": c2, "evidence": ["E2"]},
        ],
        "evidence": {"E1": {"age_days": e1_age}, "E2": {"age_days": 10}},
        "defeaters": [{"id": "D1", "disposition": d1}],
    }

cases = [
    ("ready", packet()),
    ("missing-revision", packet(revision="")),
    ("unresolved", packet(c2="unresolved")),
    ("stale", packet(e1_age=250)),
    ("open-defeater", packet(d1="")),
    ("missing-authority", packet(authority="")),
]
for name, candidate in cases:
    print(f"{name}={preflight(candidate)}")
```

The fixed 180-day rule is illustrative and intentionally incomplete. Real freshness depends on claim volatility, revision change, environment, threat evolution, and policy. The checker cannot detect omitted claims, biased reviewers, invalid evidence, or false premises.

## Alternatives and Trade-Offs

**Live interrogation versus asynchronous pre-read.** Live challenge reveals reasoning under pressure; pre-read enables deeper evidence inspection and broader participation. Use both, and never use surprise as a proxy for rigor.

**Claim graph versus narrative packet.** A graph exposes support and defeaters; narrative conveys context and causal sequence. Link them through stable IDs rather than choosing one.

**Independent board versus embedded peers.** Independence reduces commitment bias; embedded peers know the system. Mix roles, disclose conflicts, and reserve authority explicitly.

**Quantitative gates versus expert judgment.** Measures improve falsifiability; novel and socio-technical questions still require judgment. Record both and their limitations.

**Approve with conditions versus defer.** Conditional approval preserves momentum when remaining work is noncritical and bounded. Deferral is honest when a controlling claim or authority is missing. Mislabeling a blocker as a condition transfers risk silently.

**Aggressive challenge versus psychological safety.** Weak challenge misses faults; personal hostility suppresses evidence. Attack claims precisely while protecting participation.

## Failure Modes and Misconceptions

- **“A strong presenter can defend a strong architecture.”** Presentation skill and architectural fitness are different variables.
- **“The board must reach consensus.”** Legitimate authority may decide while preserving dissent.
- **“Every objection must be disproved.”** Challenges need relevance and an actionable mechanism; scope is finite.
- **“Unknown is an admission of incompetence.”** Honest bounds and decision consequences are professional evidence discipline.
- **“More evidence means more confidence.”** Common-cause or irrelevant artifacts add little.
- **“An assurance case proves safety.”** Its claims, inference, evidence, assumptions, and defeaters can still be wrong.
- **“Passing the checklist means approval.”** Structural readiness is not substantive adequacy.
- **“The design passed last quarter.”** Revision, workload, threats, dependencies, and policy may have changed.
- **“A condition can close after launch.”** Only if the charter permits it and failure does not invalidate authorization.
- **“Security signed off.”** Name the person, authority, scope, date, evidence, and residual risk.
- **“The board owns the risk now.”** Risk transfers only through legitimate, explicit authority.
- **“Negative tests weaken the case.”** Disclosed failure and bounded correction strengthen inference.
- **“A red team chooses the architecture.”** It supplies challenge evidence; decision authority remains governed.
- **“Adversarial means combative.”** Hostility reduces information and is not rigor.
- **“Approval is permanent.”** It is scoped to revision, context, assumptions, conditions, and triggers.

## Worked Examples

### Example 1

**Benchmark scope challenge.** A presenter claims 40,000 requests per second from a vendor benchmark. A reviewer asks for workload shape, payload, consistency, topology, tail latency, failure state, and architecture revision. The benchmark used uniform reads and no writes; the board needs skewed mixed traffic during one-zone loss. The architect narrows the claim to read-path capacity and schedules a discriminating test. **Conclusion:** a precise boundary is stronger than defending an irrelevant headline.

### Example 2

**Answering an unknown.** The board asks how long reconciliation takes after a 12-hour partition with 30 million queued events. No test exists. The architect says the value is unknown, gives a storage-throughput lower bound, identifies compaction and conflict rate as uncontrolled variables, makes cutover conditional on a representative replay test, and names an owner. **Conclusion:** honest uncertainty includes a bound, evidence action, and decision consequence.

### Example 3

**Coverage hides a blocker.** Six critical claims have weights 5, 5, 4, 4, 3, and 2, totaling 23. Disposed claims total 19, so $K=19/23\approx0.826$. The unresolved weight-4 claim is prevention of duplicate medication orders. An 82.6% dashboard cannot compensate for it; the safety authority treats it as a gate. **Conclusion:** structural coverage prioritizes work but never averages away a critical obligation.

### Example 4

**Correlated evidence.** Three recovery reports appear independent, but all replay the same sanitized snapshot through the same orchestration script and observe the same faulty clock metric. The board treats them as one evidence lineage and requests a separately instrumented destructive restore in a representative environment. **Conclusion:** artifact count is not evidential independence.

### Example 5

**Universal claim falsified.** The packet says “no acknowledged order can be lost.” One injected control-plane isolation lets an acknowledgment escape before durable replication. A single valid counterexample refutes the universal claim even if 9,999 nominal tests passed. The team changes the acknowledgment boundary and retests failure timing. **Conclusion:** the logical form of a claim determines what evidence can defeat it.

### Example 6

**Strongest alternative.** A team compares its detailed service design against a one-box sketch labeled “monolith.” The board requires equivalent deployment, backup, observability, staffing, data, and migration scope. A modular monolith then meets the same current scenarios with lower transition risk. **Conclusion:** an adversarial board challenges advocacy asymmetry, not merely implementation detail.

### Example 7

**Authority gap.** Engineers and managers approve a benefits system, but no accessibility specialist, frontline operator, privacy authority, or claimant representative reviewed it. The chair records representation and authority gaps rather than interpreting silence as consent. The technical session may resolve mechanisms, but deployment authorization defers. **Conclusion:** technical attendance cannot manufacture missing legitimacy.

### Example 8

**Hostility versus rigor.** A senior reviewer interrupts a junior operator and calls a failed restore “user error.” The chair stops the exchange, asks for the run identifier, expected procedure, observed command, system feedback, and claim affected, then gives the operator uninterrupted time. The failure reveals an unsafe runbook precondition. **Conclusion:** protecting the witness improves adversarial evidence.

### Example 9

**Condition or blocker.** A logging dashboard lacks a cosmetic label; that can close after approval with an owner. The same packet has no tested way to revoke compromised signing keys. Because key compromise is a controlling threat and no bounded mitigation exists, it is not a post-approval action. **Conclusion:** condition severity follows decision consequence, not schedule pressure.

### Example 10

**Defending a reversible choice.** Two architectures remain viable under overlapping estimates. The architect recommends a bounded pilot of the option with cheaper exit, retains the current system as authority, declares abort thresholds, instruments the uncertain workload, and schedules review. The board approves learning rather than pretending one forecast is true. **Conclusion:** a defensible recommendation can be an option with explicit limits.

## Cross-Program Connections

- [Software Engineering: Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) owns test validity, oracles, sampling, and evidence quality.
- [Software Engineering: Delivery and Reliability Engineering](../../14-software-engineering-software-delivery-and-reliability-engineering/ROADMAP.md) owns production readiness, operational validation, and incident learning.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) owns threat analysis, security verification, and risk treatment evidence.
- [Systems Engineering](../../26-systems-engineering/ROADMAP.md) owns lifecycle reviews, stakeholder authority, system alternatives, and technical baselines.
- [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) supplies contract, compatibility, failure, and operational claims that boards commonly challenge.
- [Data Architecture Engineering](../../20-data-architecture-engineering/ROADMAP.md) owns data authority, provenance, retention, privacy, and governance evidence.

## References

1. ISO/IEC/IEEE, *42010:2022 — Software, Systems and Enterprise—Architecture Description*, edition 2, November 2022. [ISO record](https://www.iso.org/standard/74393.html). Published status checked 2026-09-06.
2. ISO/IEC/IEEE, *42030:2019 — Software, Systems and Enterprise—Architecture Evaluation Framework*, edition 1, July 2019. [ISO record](https://www.iso.org/standard/73436.html). ISO confirmed the standard in 2025; it remains published while a revision is under development, status checked 2026-09-06.
3. Rick Kazman et al., *The Architecture Tradeoff Analysis Method*, CMU/SEI-98-TR-008, 1998. [SEI record](https://www.sei.cmu.edu/library/the-architecture-tradeoff-analysis-method/).
4. Assurance Case Working Group, *Goal Structuring Notation Community Standard Version 3*, SCSC-141C, May 2021. [Current standard record](https://scsc.uk/gsn-standard). Version status checked 2026-09-06.
5. Ron Ross, Mark Winstead, and Michael McEvilley, *NIST SP 800-160 Volume 1 Revision 1: Engineering Trustworthy Secure Systems*, November 2022. [NIST record](https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final).
6. NASA, *NASA Systems Engineering Handbook*, NASA/SP-2016-6105 Rev 2, 2016. [NASA handbook](https://www.nasa.gov/wp-content/uploads/2018/09/nasa_systems_engineering_handbook_0.pdf).
7. Michael Wildpaner et al., “SRE Engagement Model,” *The Site Reliability Workbook*, O'Reilly/Google, 2018. [Google SRE edition](https://sre.google/workbook/engagement-model/).
8. Stephen E. Toulmin, *The Uses of Argument*, updated ed., Cambridge University Press, 2003.
9. Daniel Kahneman, Olivier Sibony, and Cass R. Sunstein, *Noise: A Flaw in Human Judgment*, Little, Brown Spark, 2021.
10. David L. Parnas, “On the Criteria To Be Used in Decomposing Systems into Modules,” *Communications of the ACM* 15(12), 1972. [DOI record](https://doi.org/10.1145/361598.361623).
11. Jerome H. Saltzer and Michael D. Schroeder, “The Protection of Information in Computer Systems,” *Proceedings of the IEEE* 63(9), 1975. [MIT-hosted paper](https://web.mit.edu/Saltzer/www/publications/protection/).
12. Association for Computing Machinery, *ACM Code of Ethics and Professional Conduct*, adopted 2018. [Official code](https://www.acm.org/code-of-ethics).

## Exercises

### Exercise 1

**Classify board questions.** Classify each as clarification, factual, mechanism, premise, counterexample, alternative, value, or authority challenge: “Which revision was tested?”, “What happens when identity is reachable but policy storage is not?”, “Why not retain the modular monolith?”, “Who may accept a 20-minute outage?”, and “Your claim says every acknowledgment is durable; here is one valid loss trace.” Give the four-part response each requires.

### Exercise 2

**Compute and critique coverage.** Critical claims have weights (5,4,4,3,2). Claims of weights 5,4,3,2 are disposed; one weight-4 security claim remains unresolved. Compute $K$. Explain why neither the percentage nor four disposed claims authorize approval, and identify the next decision step.

### Exercise 3

**Diagnose a packet.** A 90-slide packet omits the revision, cites a supplier benchmark, presents only the preferred candidate, labels every risk “medium,” has no negative evidence, and asks the board to “sign off.” Identify at least ten defects and redesign the entrance criteria and opening.

### Exercise 4

**Design an adversarial review.** Design a board for replacing a payment platform during peak season. Specify charter, authority, roles, conflict controls, top claims, scenarios, evidence, pre-read, question protocol, outcome semantics, conditions, closure evidence, and reopening triggers.

### Exercise 5

**Transfer to emergency dispatch.** Prepare the defense strategy for a regional emergency-dispatch architecture spanning call intake, location, radio, mobile data, intermittent links, mutual aid, accessibility, privacy, cyberattack, disaster surge, legacy migration, and operator fatigue. State the top claim, gates, evidence, defeaters, unknown-answer protocol, affected authorities, adversarial scenarios, reversible transition, and conditions under which you would recommend rejection.

## Answers to the Exercises

### Answer 1

“Which revision was tested?” is factual: name the revision, evidence record, mismatch if any, and consequence. “What happens when identity is reachable but policy storage is not?” is a mechanism/premise challenge: trace request, cached policy, freshness, fail-open/closed behavior, telemetry, recovery, uncertainty, and decision effect. “Why not retain the modular monolith?” is an alternative challenge: present its strongest comparable case, decisive trade-off, evidence, and reversal condition.

“Who may accept a 20-minute outage?” is an authority challenge: identify the service owner and any regulatory, safety, contractual, or public authority; do not answer with a technical preference. The loss trace is a counterexample: verify that it satisfies the universal claim's premises, then accept refutation or explain precisely why it is out of scope. Each response gives conclusion, evidence/reasoning, boundary, and decision consequence. A label alone is insufficient.

### Answer 2

The total weight is $5+4+4+3+2=18$ and disposed weight is $5+4+3+2=14$, so $K=14/18\approx0.778$. Coverage reports structural disposition under declared weights, not validity, completeness, evidence quality, or authority. The unresolved claim concerns security and may be a gate; strength elsewhere cannot compensate.

Link the claim to its threat scenario, mechanism, evidence, assumptions, and defeaters. The security authority determines the required evidence and acceptance boundary. If a discriminating test or analysis can close it, defer or explicitly bound a reversible experiment. If the gate is refuted or cannot be evidenced by the deadline, revise or reject. Do not relabel it conditional merely to increase $K$.

### Answer 3

Defects include no decision sentence, no architecture revision, ambiguous authority, incomparable scope, supplier-only evidence, undisclosed benchmark workload, no evidence provenance or limitations, no alternative, no transition comparison, ordinal risk labels, no probability/consequence basis, no uncertainty, no negative evidence, no defeaters, no stakeholder/authority map, no success criteria, and undefined “sign off.”

Entrance requires a named revision, decision and horizon, convening authority, mandatory roles, candidate set, gates, scenarios, claim/evidence index, artifact access, evidence cutoff, negative results, unresolved issues, conflicts, conduct, and predefined outcomes. The opening should state the ask, context, gates, recommendation, three controlling claims and evidence, leading alternative, transition, accepted trade-offs, residual risks, unknowns, and what would reverse the decision. Detailed history moves to an appendix.

### Answer 4

The charter requests authorization for a named migration state and peak-season operating boundary, not generic approval. Business risk owners hold financial and customer authority; payment, security, privacy, fraud, operations, data, accessibility, and change authorities concur within their scope. Independent reviewers include platform and incident expertise; implementers present. Conflicts, supplier relationships, and prior advocacy are disclosed, with recusal where authority would be compromised.

Top claims cover transaction integrity, idempotency, authorization, fraud controls, confidentiality, peak capacity, tail latency, dependency failure, regional recovery, reconciliation, observability, operator load, rollback, migration coexistence, cost, and exit. Scenarios include duplicate submission, timeout after commit, stale policy, compromised credential, processor outage, corrupt ledger event, region isolation, load spike, bad deployment, rollback, and disputed settlement. Evidence identifies revisions, production-shaped workloads, failure injection, restore/reconciliation results, threat analysis, contract tests, incident history, and limits.

The pre-read uses stable IDs and includes the strongest alternative and negative results. Questions use conclusion–evidence–boundary–consequence; the scribe records dispositions. Outcomes are approve, conditional, defer, revise, reject, or outside authority. Conditions name owners, deadlines, closure tests, and automatic consequences. Triggers include failed reconciliation, latency or error-budget breach, fraud shift, supplier or regulatory change, missed migration checkpoint, operator overload, and architecture drift. An answer may choose different roles, but it must keep authority, evidence, and risk acceptance distinct.

### Answer 5

The top claim is: named revision R can support authorized regional dispatch populations and mutual-aid operations through declared normal and disaster contexts, subject to explicit transition conditions. Gates include no lost accepted emergency event, unique incident identity, bounded location uncertainty, authenticated but resilient authority, accessible call channels, privacy and retention duties, priority and preemption semantics, safe degraded operation, audited correction, tested recovery, operator workload limits, radio/mobile interoperability, and lawful public authority.

Evidence includes production-shaped call and radio loads; end-to-end latency distributions by population; location uncertainty; link and region isolation; control-plane loss; duplicate/conflicting incident tests; disaster surge; accessibility evaluation with affected users; privacy and threat analysis; compromised dispatcher and credential scenarios; backup restore and reconciliation; mutual-aid exercises; human-factors simulation; legacy parallel-run discrepancies; staffing and training evidence; and exact revision/provenance/limitations. Defeaters include shared telecom dependency, stale maps, correlated location failure, inaccessible fallback, policy-store loss, alert fatigue, malicious issuer, split incident authority, rollback after data divergence, and exhausted staff.

For an unknown, state it, give the present bound, explain the consequence, name the evidence action and owner, and say whether the gate forces deferral. Authorities include emergency-service leadership, dispatch operators, telecommunications and mutual-aid owners, safety, security, privacy, accessibility, labor/human-factors, legal/regulatory, and affected communities; the architecture board cannot impersonate them.

The transition keeps the legacy authority during a bounded parallel run, reconciles every incident, defines one authority at each instant, preserves manual/radio fallbacks, sets abort thresholds, and prohibits irreversible shutdown until independent recovery and accessibility evidence pass. Recommend rejection if a critical gate fails, evidence targets the wrong revision or population, authority is absent, common-cause loss remains uncontrolled, reconciliation cannot preserve incident integrity, degraded modes overload operators, rollback is fictional, or schedule pressure requires hiding a material defeater. A polished defense cannot compensate for any of these conditions.
