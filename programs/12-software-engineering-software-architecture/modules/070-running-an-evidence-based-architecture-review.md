---
module_id: SARCH-070
program: Software Engineering: Software Architecture
level: 2
module_number: 70
title: Running an Evidence-Based Architecture Review
status: complete
last_verified: 2026-09-06
---

# Running an Evidence-Based Architecture Review

## One-Page Review

### Governing question

How can a review team turn stakeholder concerns, architecture descriptions, measurements, experiments, incidents, and expert judgment into a bounded decision without converting a meeting, checklist, or evidence count into false assurance?

### Essential definitions

- a **review charter** states the decision, scope, architecture revision, participants, authority, evidence cutoff, confidentiality, outputs, and follow-through;
- a **claim** is a proposition about an architecture, such as a response meeting a measure under stated conditions;
- **evidence** is information used to support or challenge a claim; its relevance, provenance, validity, independence, freshness, and limitations matter;
- an **argument** connects evidence and assumptions to a claim rather than merely attaching documents;
- a **quality-attribute scenario** names source, stimulus, environment, affected artifact, response, and response measure;
- a **finding** is a traced conclusion such as a risk, nonrisk, sensitivity point, trade-off point, constraint violation, evidence gap, or unresolved disagreement;
- an **evidence gap** identifies a decision-relevant claim for which evidence is missing, unsuitable, stale, or contradictory;
- **triangulation** compares evidence produced through meaningfully different methods, populations, or failure assumptions;
- a **decision condition** is a requirement, experiment, mitigation, expiry, or residual-risk action attached to an outcome;
- **closure evidence** is the specified observation needed to resolve a finding; status change alone is not closure.

### Central model, mechanism, or theorem

Represent a review as a trace relation

$$
T\subseteq D\times S\times A\times C\times E\times F,
$$

where $D$ is drivers and constraints, $S$ scenarios, $A$ architecture decisions and mechanisms, $C$ claims, $E$ evidence, and $F$ findings. Every material finding must trace backward to its decision context, and every decision-critical claim must have a disposition. Structural coverage can be measured, but it does not measure truth: ten reports copied from one invalid test are not stronger than one.

### Critical invariants

- the review asks a decision question and identifies who has authority to answer it;
- the architecture revision, deployed state, environment, workload, and evidence cutoff are explicit;
- affected stakeholders and specialist authorities are represented or recorded as a gap;
- claims are falsifiable and tied to scenarios and mechanisms;
- evidence is reviewed for provenance, relevance, validity, independence, freshness, and limitations;
- missing or conflicting evidence becomes a finding rather than an optimistic assumption;
- observations, inferences, judgments, and accountable decisions remain distinguishable;
- ordinal priorities are not multiplied or averaged as calibrated quantities;
- nonrisks and approvals remain scoped to conditions and expire when those conditions change;
- every action names an owner, deadline, decision consequence, and closure evidence.

### Common failures

Common failures include reviewing slides rather than the named architecture; inviting only implementers; using product names as mechanisms; accepting dashboards without metric definitions; accepting tests from an unrepresentative environment; counting artifacts instead of assessing evidence; hiding uncertainty behind red/amber/green; treating absence of incidents as proof; letting a deadline redefine acceptance criteria; suppressing dissent; confusing a mitigation plan with implemented mitigation; approving while critical claims remain undisposed; and closing findings from ticket status rather than new evidence.

### Compact example

A team claims that regional failover restores checkout within 60 seconds. Its diagram shows two regions, but the only evidence is a component restart test in one region. The review traces the scenario through detection, routing, identity, data authority, queue recovery, and client retries. It records the component test as relevant only to restart, identifies no end-to-end failover evidence, and makes the gate conditional on a production-like isolation exercise with integrity and recovery measures. The result is not “red”; it is a precise claim, gap, owner, test, and decision consequence.

### Connections

[SARCH-069](069-cost-models-and-unit-economics.md) supplies comparable cost evidence. [SARCH-061](061-architecture-tradeoff-analysis-method.md) supplies ATAM as one structured evaluation method. [SARCH-071](../ROADMAP.md) next examines drift between architectural intent and reality.

## Governing Question

An architecture review exists to reduce decision risk. It should reveal whether a proposed or deployed architecture can plausibly satisfy its important outcomes, which assumptions remain exposed, and what evidence would change the decision. It is not a ceremony for obtaining a favorable color or signature.

Evidence-based does not mean evidence-only. Stakeholders decide what outcomes matter; architecture reasoning explains mechanisms; measurements and experiments test selected claims; authorized leaders accept residual consequences. A sound review makes those roles and inferential steps visible.

## Why This Matters

Architecture creates long-lived commitments across teams, data, contracts, operations, and failure domains. A review held after those commitments are irreversible becomes documentation theater. A review held early but without concrete claims becomes opinion exchange. The useful window is early enough to change and mature enough to analyze.

Poor review evidence also creates asymmetric harm. A benchmark may ignore the slowest cohort, a recovery test may omit corrupted state, a threat assessment may exclude administrators, or a cost model may count attempts instead of successful outcomes. The meeting can be orderly while the conclusion is invalid. Evidence discipline exposes those boundaries before a decision inherits them.

## Prerequisites and Retrieval

Retrieve stakeholder, concern, decision authority, scope, quality attribute, scenario, architecture view, decision record, traceability, hypothesis, falsification, measurement validity, sampling, confidence interval, performance model, dependency graph, failure mode, threat model, cost model, risk, residual risk, sensitivity point, trade-off point, and assurance case.

SARCH-061 through SARCH-069 form the review kit: structured trade-off analysis, measurable scenarios, risk and sensitivity, automated fitness evidence, dependency and coupling metrics, capacity models, reliability models, threat models, and unit economics. This chapter integrates them into review execution. It does not replace formal verification, security assessment, safety or hazard analysis, accessibility evaluation, financial approval, legal review, or domain certification.

## Learning Objectives

After completing this module, you should be able to:

1. charter an architecture review around a consequential and answerable decision;
2. select participants, roles, independence, confidentiality, and decision rights;
3. assemble and baseline an architecture and evidence package;
4. express decision-critical claims through scenarios, mechanisms, assumptions, and measures;
5. classify evidence by provenance, relevance, validity, independence, freshness, and uncertainty;
6. challenge experiments, models, production data, incidents, and expert judgment appropriately;
7. facilitate analysis, dissent, prioritization, and specialist referrals without false consensus;
8. synthesize risks, nonrisks, gaps, sensitivities, trade-offs, and themes with traceability;
9. issue approve, conditionally approve, defer, reject, or out-of-scope outcomes without overclaiming;
10. govern actions, closure evidence, expiry, and re-review triggers.

## Core Exposition

**Choose the decision.** Begin with the change or commitment the review can affect: select a candidate architecture, authorize implementation, enter a migration, expose a new interface, accept a supplier, change a reliability target, or continue a deployed design. State the alternatives and the default if no decision is made.

An open-ended question such as “Is the architecture good?” has no stable evidence boundary. A useful question names system, revision, lifecycle point, outcomes, constraints, horizon, and authority. Several decisions may require several reviews rather than one meeting with an unlimited scope.

**Write the charter.** Record sponsor, accountable decision maker, review lead, review team, architecture team, stakeholders, specialist authorities, scope, exclusions, architecture baseline, evidence cutoff, agenda, confidentiality, outputs, and follow-up. State whether the review is advisory or a formal gate.

The charter also defines conflict handling. Reviewers disclose authorship, vendor, reporting, or delivery interests. Independence is not binary: a designer may supply unique knowledge, while an evaluator outside the delivery line may challenge it. Record where independent expertise is unavailable.

**Select representative participants.** Include the people who own consequences, not merely components. Depending on the system, that may include users, operations, development, product, support, security, privacy, accessibility, safety, data governance, finance, legal, procurement, suppliers, and downstream integrators.

Representation is an evidence issue. One manager cannot necessarily speak for operators or affected users. If a group cannot participate, gather its evidence through interviews or studies and record the limitation. Protect psychological safety, language access, disability access, time-zone equity, and dissent.

**Baseline the object under review.** Identify architecture description version, code or configuration revision, deployment inventory, environment, data schema, supplier version, and active decision records. Distinguish intended, implemented, deployed, and observed architecture. ISO/IEC/IEEE 42010:2022 distinguishes an architecture from the architecture description that expresses it [2].

Reconcile diagrams against runtime discovery, configuration, telemetry, and operator knowledge. A clean diagram can omit an identity issuer, support console, data export, batch path, feature flag, or recovery dependency that dominates the decision. Differences become findings, not silent diagram edits.

**Prepare an evidence inventory.** Index requirements, views, decision records, models, tests, benchmarks, production measures, incidents, experiments, threat assessments, cost analyses, supplier attestations, audits, and known unknowns. For each artifact, record owner, creation time, method, population, environment, version, transformations, access restrictions, and claimed use.

An inventory is not an argument. A hundred artifacts can leave the central claim unsupported. The inventory makes provenance inspectable and prevents the meeting from discovering basic access failures; analysis determines which evidence is fit for which claim.

**Define scenarios and claims.** Translate drivers into quality-attribute scenarios. Then state claims that can be challenged: “Under one-region isolation at forecast peak, admitted payment intents reach one terminal state within 45 seconds without duplicate capture.” This claim names failure, workload, response, measure, and integrity.

Decompose broad claims. Availability may depend on detection, isolation, routing, authority, state, capacity, retry, and recovery claims. A test of routing supports only the routing claim. The argument explains how component evidence and assumptions combine—or fail to combine—into the system claim.

**Trace mechanisms.** For every selected scenario, follow stimulus through architecture elements, decisions, state transitions, dependencies, resource limits, trust boundaries, and human actions to the response. Name the mechanism intended to meet each measure and what could invalidate it.

Do not accept “managed,” “event-driven,” “zero trust,” or “active-active” as mechanisms. Expand labels into authority, consistency, queueing, retry, isolation, detection, recovery, and operational behavior. Record unknown implementation or deployment detail as an evidence gap.

**Classify evidence by claim.** Direct observation of the full scenario in a representative environment may be strong for observed behavior. Component tests, analytical models, simulations, historical incidents, formal proofs, standards conformance, expert judgment, and supplier evidence answer different questions.

Evaluate at least:

- **provenance:** who or what produced the evidence, from which inputs and transformations;
- **relevance:** whether it addresses the actual claim and decision;
- **internal validity:** whether the method supports the stated inference;
- **external validity:** whether the environment, population, and workload transfer;
- **independence:** whether purported corroboration shares data, tool, author, model, or failure cause;
- **freshness:** whether architecture and conditions still match;
- **resolution:** whether aggregation hides important cohorts, tails, or states;
- **uncertainty:** which sampling, model, measurement, and unknown errors remain;
- **reproducibility:** whether an authorized reviewer can repeat or inspect the method;
- **integrity:** whether custody, version, and transformation are trustworthy.

**Challenge measurements.** Ask what population entered numerator and denominator, how events were sampled, which time window applies, how missing telemetry was treated, and whether units match the scenario. A mean does not establish a percentile; a global percentile does not describe a region or tenant; request success does not establish workflow correctness.

Measurement systems can fail with the system. During overload, dropped telemetry can make the observed population look healthier. Correlate client, service, dependency, and business-outcome evidence. Preserve raw-enough data and calculation versions for review within governance constraints.

**Challenge experiments.** Inspect hypothesis, controlled change, environment, workload, test article, duration, warm-up, repetitions, stopping rules, instrumentation, failure injection, negative cases, and deviations. Confirm that the tested artifact matches the reviewed revision.

A passing component test cannot establish an emergent system property without a justified composition argument. Conversely, one failed test may reveal a real counterexample even if it does not estimate failure frequency. Treat counterexample and frequency claims separately.

**Challenge analytical and formal models.** Review notation, assumptions, boundary conditions, parameter sources, sensitivity, calibration, and correspondence between model and architecture. A queueing result assumes arrival and service behavior; a reliability product assumes independence; a proof covers only the formalized model.

Recompute decisive results independently. Test zero, threshold, peak, failure, adversarial, and recovery cases. A model is valuable when it exposes sensitive assumptions and predicts observations, not when its equations are impressive.

**Use production evidence carefully.** Production measurements represent actual operation within their observed history. They can reveal mix, tail, common dependencies, and human behavior absent from laboratories. They do not cover future scale, unobserved failures, new architecture, or rare adversarial paths automatically.

Absence of observed incidents gives an upper-bound problem, not zero risk. Define detection coverage and exposure time before learning from incident counts. Near misses, support cases, recovery delays, and manual overrides can challenge a nominal success metric.

**Use incident evidence for mechanism learning.** Reconstruct timeline, state, decisions, signals, contributing conditions, impact, response, and recovery. Avoid treating a single root-cause label as the architecture explanation. Ask which boundary allowed propagation and which assumptions failed.

An incident is direct evidence that a path was feasible under its conditions. It is not proof that the proposed mitigation eliminates every related path. Trace corrective mechanisms to tests and operational observations.

**Handle supplier evidence.** Contracts, service descriptions, certifications, test reports, software bills of materials, attestations, and support records may constrain the supplier claim. Check exact product, version, region, configuration, responsibility boundary, period, exceptions, and right to inspect.

A certification is evidence of its stated assessment scope, not proof of system security or suitability. Architecture must analyze integration, customer configuration, shared dependencies, failure response, data exit, and supplier change. Attach expiry and notification conditions.

**Triangulate meaningfully.** Combine evidence with different failure modes: an analytical capacity model, controlled load test, and production peak observation; a protocol proof, implementation test, and incident history; a cost forecast and invoice reconciliation. Agreement increases confidence only to the extent the methods are independently informative.

Three dashboards derived from one event stream are one measurement lineage. Multiple reviewers reading the same incomplete document are not independent evidence. Map shared sources and assumptions before calling results corroborated.

**Do not create a confidence machine.** High/Medium/Low evidence labels can support triage if their rubric is explicit. They are ordinal, context-specific judgments. Multiplication, averaging, or colorful aggregation does not create calibrated probability.

If quantitative uncertainty matters, use an appropriate statistical or decision model with defensible inputs. Otherwise report evidence, counterevidence, unknowns, and sensitivity in plain terms. Precision must follow measurement, not presentation style.

**Facilitate analysis rather than advocacy.** The architecture team explains decisions and evidence; reviewers question mechanisms and consequences; affected stakeholders prioritize outcomes; specialist authorities judge domain obligations; the decision maker owns the outcome. The facilitator protects these roles.

Use structured rounds, anonymous input, or separate interviews when hierarchy suppresses concerns. Record material disagreement and its basis. Consensus is not required for a valid review; undisclosed dissent is a validity defect.

**Prioritize analysis.** Time is finite. Prioritize by stakeholder importance, severity, uncertainty, irreversibility, novelty, coupling, evidence weakness, and cost of learning. Safety, legal, security, privacy, accessibility, or severe minority consequences may override popularity.

Record a disposition for every decision-critical claim: supported within scope, contradicted, inconclusive, delegated to named specialist work, deferred with rationale, or out of scope with an owner. Claims just below the analysis cutoff remain visible.

**Write findings as traceable arguments.** A finding names scenario, affected decision, claim, evidence and counterevidence, assumptions, inference, consequence, uncertainty, owner, and closure evidence. “Scalability risk” is not actionable. “At forecast peak, the single partition reaches the tested saturation boundary before admitted demand, and no shedding contract protects priority work” is.

Distinguish observation from inference. “The test reached 8,000 requests per second” is an observation. “The architecture cannot meet 10,000 in the target environment” is an inference requiring environment and scaling arguments. “Defer launch” is a decision, not a test result.

**Synthesize themes without erasing detail.** Related findings may reveal implicit authority, shared control-plane coupling, missing workload ownership, untested recovery, stale architecture description, or supplier dependence. A theme should cite its supporting findings and identify system-level action.

Do not replace findings with a heat map. Aggregation can hide the exact decisions and evidence needed for repair. Preserve the trace ledger beneath summaries.

**Issue a bounded outcome.** Useful review outcomes include approve within stated scope, approve with conditions, defer pending evidence, reject a candidate relative to the decision criteria, or refer a question outside review authority. Define what approval means and does not mean.

A conditional approval lists conditions, owners, deadlines, closure evidence, and the consequence of failure. Conditions that can be ignored are recommendations, not gate conditions. A review must not approve around an unmet nondelegable safety or legal constraint.

**Govern closure.** A risk closes when the decision changes, valid new evidence changes the conclusion, the scenario is explicitly removed by authorized stakeholders, or accountable authority accepts the residual consequence within its power. Creating a ticket, assigning an owner, or writing a plan does not close it.

Independently check material closure evidence. Preserve original finding, response, evidence, decision, and date. Reopen when assumptions, workload, dependency, supplier, threat, regulation, team capability, or deployed architecture changes.

**Make the review reproducible.** The durable review package contains charter, participant roles, architecture baseline, scenarios, claims, evidence index, analysis notes, findings, dissent, decision, actions, closure criteria, limitations, and access controls. Protect sensitive material while keeping enough provenance for authorized audit.

The next review should be able to determine what changed. Stable identifiers for scenarios, decisions, evidence, and findings make drift and recurrence visible. SARCH-071 develops drift and erosion as architectural phenomena.

## Definitions and Notation

Let:

- $D$ be decision drivers, constraints, and acceptance criteria;
- $S$ be review scenarios;
- $A$ be architecture decisions, mechanisms, and assumptions;
- $C$ be explicit claims, with $C^*\subseteq C$ the decision-critical claims;
- $E$ be evidence artifacts and observations;
- $F$ be findings;
- $R_E\subseteq E\times C$ be the declared support or challenge relation;
- $T\subseteq D\times S\times A\times C\times E\times F$ be the review trace;
- $V(e,c)$ be a structured validity assessment of evidence $e$ for claim $c$, not a universal scalar;
- $x$ be the identified architecture revision and $\tau$ the evidence cutoff;
- **disposition** be supported within scope, contradicted, inconclusive, delegated, deferred, or out of scope;
- **closure condition** be the evidence and authority required to change a finding's state.

A structural coverage indicator is

$$
K=\frac{|\{c\in C^*: \exists e\in E,(e,c)\in R_E\}|}{|C^*|},
$$

when $|C^*|>0$. $K$ reveals unsupported critical claims. It does not measure evidence quality, claim truth, or architecture fitness. If every claim cites the same invalid artifact, $K=1$ while the review remains unsound.

## Mechanisms, Invariants, or Proof Structure

### Review execution procedure

1. Charter the decision, authority, alternatives, baseline, scope, participants, cutoff, outputs, and follow-through.
2. Reconcile intended, implemented, deployed, and observed architecture.
3. Build a provenance-bearing evidence inventory and state known access gaps.
4. Elicit drivers and measurable scenarios from representative stakeholders.
5. Decompose decision-critical system claims and trace their mechanisms and assumptions.
6. Evaluate evidence relevance, validity, independence, freshness, resolution, uncertainty, reproducibility, and integrity.
7. Analyze nominal, boundary, failure, adversarial, recovery, and evolutionary cases.
8. Record observations, inferences, dissent, findings, themes, and specialist referrals separately.
9. Issue a bounded outcome with conditions, owners, closure evidence, expiry, and decision consequences.
10. Reconcile actions and re-review when evidence or architecture changes.

### Executable structural coverage check

This script checks only whether a toy review ledger attaches at least one evidence identifier to each critical claim. It deliberately reports a gap. It cannot assess whether the evidence is valid or whether the claim is true.

<!-- bijux-verify: {"id":"critical-claim-coverage","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"critical claims=3\nsupported critical claims=2\nstructural coverage=0.67\nunsupported=C-RECOVERY\n","stderr":""}} -->
```python
claims = [
    {"id": "C-CAPACITY", "critical": True, "evidence": ["E-LOAD-17"]},
    {"id": "C-INTEGRITY", "critical": True, "evidence": ["E-PROP-04", "E-FAULT-09"]},
    {"id": "C-RECOVERY", "critical": True, "evidence": []},
    {"id": "C-COST", "critical": False, "evidence": ["E-FORECAST-03"]},
]

critical = [claim for claim in claims if claim["critical"]]
supported = [claim for claim in critical if claim["evidence"]]
unsupported = [claim["id"] for claim in critical if not claim["evidence"]]

print(f"critical claims={len(critical)}")
print(f"supported critical claims={len(supported)}")
print(f"structural coverage={len(supported) / len(critical):.2f}")
print(f"unsupported={','.join(unsupported)}")
```

### Review invariants

- every outcome is tied to one decision charter and architecture revision;
- every material driver has scenario coverage or an explicit gap;
- every critical claim has a disposition and every supporting artifact has provenance;
- every finding traces to scenario, decision, claim, evidence, inference, and consequence;
- every quantitative result retains definition, population, unit, period, method, and uncertainty;
- every experiment identifies the test article and representative-environment limits;
- every nonrisk and approval states assumptions, scope, expiry, and re-review triggers;
- every material dissent remains visible to the decision maker;
- every condition names closure evidence and a consequence if unmet;
- no review claims certification beyond its explicit authority and evidence.

## Alternatives and Trade-Offs

**Independent review versus embedded review.** Independent reviewers reduce delivery-line pressure and bring comparative experience, but need time to learn the system. Embedded reviewers understand context and can follow through, but may share assumptions and incentives. Combine informed participation with independent challenge and disclose conflicts.

**Synchronous workshop versus asynchronous review.** Workshops expose interactions quickly and support shared reasoning. They can privilege fast or senior speakers and consume scarce time. Asynchronous evidence review supports depth and access across time zones but fragments debate. Use pre-review and individual input before a focused analysis session.

**Broad review versus deep review.** Broad coverage catches omitted concerns but can remain superficial. Deep scenario traces test mechanisms but sample fewer concerns. First map the full decision surface, then select risk-based deep traces and preserve explicit dispositions for the remainder.

**Checklist versus scenario analysis.** Checklists provide repeatable prompts and regulatory mapping. They can invite superficial completion and miss system-specific interactions. Scenarios reveal behavior and trade-offs; checklists should seed and audit coverage rather than substitute for reasoning.

**Production evidence versus controlled experiment.** Production data offers realistic mix and human behavior but weak control and incomplete rare-event coverage. Experiments isolate mechanisms and failure cases but may lack external validity. Triangulate and state the transfer argument.

**Quantitative score versus trace ledger.** Scores enable portfolio sorting but collapse heterogeneous evidence, uncertainty, and severe constraints. A trace ledger preserves actionable detail but is harder to summarize. Use summaries only as navigation to claims and findings, never as their replacement.

**Gate versus advisory review.** A gate can prevent irreversible or dangerous commitment when authority and criteria are real. It can create schedule theater and evidence gaming. Advisory review encourages early learning but may be ignored. Match authority to consequence and make conditions enforceable.

**Open report versus restricted annex.** Broad visibility supports learning and accountability. Threats, personal data, contracts, and vulnerabilities may require controlled access. Keep the method, decisions, owners, and nonsensitive rationale visible while governing sensitive evidence separately.

## Failure Modes and Misconceptions

1. **“A review is a meeting.”** Analysis begins in preparation and ends only with governed closure.
2. **“More documents mean more evidence.”** Relevance and validity matter more than count.
3. **“The diagram is the architecture.”** It is a versioned description that may diverge from deployment and operation.
4. **“A product label explains the mechanism.”** Behavior comes from configuration, state, authority, workload, and failure handling.
5. **“One passing test proves the system claim.”** Composition and environment require an argument.
6. **“Production history proves future readiness.”** Future demand, changes, and unobserved events remain outside the sample.
7. **“No incidents means no risk.”** Detection gaps and rare exposure prevent that inference.
8. **“Three dashboards triangulate.”** Shared source and transformations can make them one evidence lineage.
9. **“A confidence color is a probability.”** Ordinal labels are not calibrated numerical belief.
10. **“Consensus establishes correctness.”** Groups can share missing knowledge or incentives.
11. **“Dissent blocks the review.”** Recorded, evidence-based disagreement can improve the decision.
12. **“Certification covers integration.”** It covers only its stated product, version, controls, period, and assessment boundary.
13. **“A model with precise output is accurate.”** Assumptions, parameters, and correspondence determine validity.
14. **“A mitigation plan mitigates risk.”** Only implemented and evidenced mechanism changes can do so.
15. **“Conditional approval means approve now and check later.”** Conditions require owners, evidence, deadlines, and consequences.
16. **“A closed ticket closes a finding.”** Closure follows specified evidence or accountable acceptance.
17. **“The reviewer owns residual risk.”** The authorized stakeholder owns acceptance within their remit.
18. **“Architecture approval certifies the product.”** Review scope cannot establish universal correctness, safety, security, or compliance.

## Worked Examples

### Example 1

**Situation.** A charter asks whether “the new platform is ready,” but the sponsor expects a supplier choice while engineers expect a production-readiness decision.

**Reasoning.** The alternatives, criteria, evidence, and authority differ. Supplier choice needs responsibility, contract, exit, and comparative capability evidence. Production readiness needs deployed configuration, operations, capacity, recovery, and support evidence. The lead splits the questions and identifies separate decision makers.

**Conclusion.** Ambiguous decision scope invalidates evidence selection; charter repair precedes analysis.

### Example 2

**Situation.** A team claims that a queue prevents checkout overload because requests are accepted asynchronously.

**Reasoning.** The review decomposes the claim into admission bound, durable acceptance, queue capacity, processing capacity, deadline, retry behavior, poison handling, and shedding. A queue-depth dashboard supports observed occupancy only. A capacity model and overload test reveal that accepted work can exceed its deadline for two hours.

**Conclusion.** Tracing claim to mechanism converts a plausible pattern label into a measurable latency and capacity risk.

### Example 3

**Situation.** The reviewed diagram shows isolated tenant databases; deployment inventory shows two tenants sharing one database during migration.

**Reasoning.** The review freezes both artifacts, records the architecture revision mismatch, and tests which scenarios depend on isolation. It does not silently redraw the diagram. Security, noisy-neighbor, backup, and rollback claims become inconclusive until the temporary topology and its controls are analyzed.

**Conclusion.** Description drift is evidence, and the deployed state controls claims about current behavior.

### Example 4

**Situation.** A report says mean latency is 120 milliseconds against a 500-millisecond 99th-percentile objective.

**Reasoning.** A mean cannot establish a percentile. The review requests the eligible request population, latency definition, sampling, window, missing-event treatment, and percentile calculation. It segments region and operation, revealing one write cohort with 99th percentile 780 milliseconds.

**Conclusion.** A correctly computed but irrelevant statistic does not support the claim; definition and population are part of evidence.

### Example 5

**Situation.** A capacity model predicts 12,000 requests per second, while a production-like load test saturates at 8,500.

**Reasoning.** Reviewers compare model and test boundaries. The model assumes a 90% cache hit rate and no synchronous audit write; the test observes 72% and includes the required audit. Replacing parameters predicts 8,640, close enough to make cache behavior and audit latency sensitivity points rather than discarding the model.

**Conclusion.** Conflict can improve a model when evidence traces the violated assumptions; choosing the favorable number would be invalid.

### Example 6

**Situation.** A signed-artifact control has a design proof for signature verification and an integration test, but incident history shows operators can deploy through an emergency path that skips verification.

**Reasoning.** The proof supports the verifier algorithm under its model, and the test supports the normal path. Neither covers deployment authority. The review records the emergency path as a counterexample to the system claim and requires uniform mediation or separately governed emergency controls with audit and recovery.

**Conclusion.** Strong evidence for a component cannot overcome an unmodeled bypass at the architecture boundary.

### Example 7

**Situation.** Most stakeholders rank a five-minute screen-reader outage low because it affects a small cohort; an accessibility specialist identifies it as blocking emergency account recovery.

**Reasoning.** The facilitator preserves the minority scenario and the legal and harm context rather than averaging votes. The scenario is escalated to the appropriate accessibility and legal authorities and remains a release constraint pending accessible recovery evidence.

**Conclusion.** Popularity is not severity or authority; representative dissent can expose a nondelegable constraint.

### Example 8

**Situation.** A supplier presents a certification issued two years ago for a previous major version and a different region.

**Reasoning.** The review records issuer, scope, controls, exceptions, period, version, region, and customer responsibilities. It treats the certification as historical evidence for the assessed boundary, not current evidence for the integrated system. The supplier must map changes and provide applicable assurance or the claim remains a gap.

**Conclusion.** Evidence expires through architecture and context change even when the document itself remains authentic.

### Example 9

**Situation.** A launch gate has three critical claims: peak capacity is supported, payment integrity is supported, and regional recovery has no evidence.

**Reasoning.** The structural indicator is $2/3$, but the review does not call the architecture 67% ready. Recovery is a required quality, so the outcome is defer or conditional approval only if policy permits a pre-launch exercise as an enforceable condition. The finding names owner, scenario, test environment, integrity measures, deadline, and failure consequence.

**Conclusion.** Coverage identifies the gap; the importance and authority of the missing claim determine the decision.

### Example 10

**Situation.** A review previously accepted manual database promotion based on a 20-minute runbook test. An incident later takes 95 minutes because the named operator lacks current credentials and the replica needs reconciliation.

**Reasoning.** The incident directly contradicts assumptions about authority and state. The team reopens the finding, revises the scenario to include on-call access and divergent state, and requires repeated recovery exercises under representative staffing. The original review record remains for traceability.

**Conclusion.** Review outcomes are conditional and revisable; operational counterevidence must update the architecture claim.

## Cross-Program Connections

- [SARCH-061](061-architecture-tradeoff-analysis-method.md) owns the ATAM workflow; this module generalizes evidence handling, decision outcomes, and closure across review methods.
- [SARCH-064](064-architecture-fitness-functions.md) supplies automated conformance signals; this module places them within a broader claim and evidence argument.
- [SARCH-066](066-performance-and-capacity-models.md), [SARCH-067](067-availability-and-reliability-models.md), [SARCH-068](068-threat-modeling-at-architecture-scale.md), and [SARCH-069](069-cost-models-and-unit-economics.md) supply specialist evidence models integrated here.
- [STQE-037](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) owns testing strategy and its cost; architecture review owns the decision-level interpretation and boundary of that evidence.
- [API-083](../../28-api-and-service-engineering/modules/083-versioning-strategies.md) owns API versioning mechanisms; architecture review checks how compatibility evidence supports system evolution claims.
- [PLAT-082](../../29-platform-engineering/modules/082-control-plane-capacity.md) owns control-plane capacity mechanisms; architecture review tests their relevance to cross-system scenarios and dependencies.

## References

1. Rick Kazman, Mark Klein, and Paul Clements, *ATAM: Method for Architecture Evaluation*, CMU/SEI-2000-TR-004, Software Engineering Institute, August 2000, https://www.sei.cmu.edu/library/atam-method-for-architecture-evaluation/ (retrieved 2026-09-06).
2. ISO/IEC/IEEE 42010:2022, *Software, systems and enterprise—Architecture description*, 2nd ed., November 2022, https://www.iso.org/standard/74393.html (retrieved 2026-09-06).
3. ISO/IEC/IEEE 42020:2019, *Software, systems and enterprise—Architecture processes*, 1st ed., July 2019, confirmed current in 2025 and marked for revision in 2026, https://www.iso.org/standard/68982.html (retrieved 2026-09-06).
4. ISO/IEC/IEEE 15026-2:2022, *Systems and software engineering—Systems and software assurance—Part 2: Assurance case*, 2nd ed., November 2022, https://www.iso.org/standard/80625.html (retrieved 2026-09-06).
5. National Aeronautics and Space Administration, *NASA Systems Engineering Handbook*, NASA/SP-2016-6105 Rev. 2, 2016, especially technical reviews and decision analysis, https://www.nasa.gov/reference/systems-engineering-handbook/ (retrieved 2026-09-06).
6. U.S. Government Accountability Office, *Technology Readiness Assessment Guide: Best Practices for Evaluating the Readiness of Technology for Use in Acquisition Programs and Projects*, GAO-20-48G, January 2020, revised February 2020, https://www.gao.gov/products/gao-20-48g (retrieved 2026-09-06).
7. Ron Ross, Mark Winstead, and Michael McEvilley, *Engineering Trustworthy Secure Systems*, NIST SP 800-160 Vol. 1 Rev. 1, November 2022, https://doi.org/10.6028/NIST.SP.800-160v1r1 (retrieved 2026-09-06).
8. Robert K. Yin, *Case Study Research and Applications: Design and Methods*, 6th ed., SAGE, 2018. Evidence sources, validity, rival explanations, and case-study inference.
9. Douglas C. Montgomery, *Design and Analysis of Experiments*, 10th ed., Wiley, 2019. Experimental design, validity, replication, and analysis.
10. Stephen Toulmin, *The Uses of Argument*, updated ed., Cambridge University Press, 2003. Claims, grounds, warrants, qualifications, and rebuttals.

## Exercises

### Exercise 1

Distinguish claim, evidence, argument, finding, decision, condition, and closure evidence. Explain why an evidence inventory is not an assurance argument.

### Exercise 2

A review has five decision-critical claims. Four cite evidence, but three of those cite the same stale component benchmark. Compute structural coverage and explain what can and cannot be inferred.

### Exercise 3

A proposed active-active service has a passing routing test, a database vendor availability statement, and 18 months without a regional incident. Diagnose the evidence for a claim of correct 60-second regional failover and design the missing evidence work.

### Exercise 4

Design an evidence-based review for selecting between an internal shared platform and an external managed service. Include charter, stakeholders, scenarios, evidence, conflicts, outcome types, and closure.

### Exercise 5

A hospital proposes an AI-assisted medication workflow. The vendor supplies benchmark accuracy, clinicians report alert fatigue, and a deadline is tied to funding. Run a bounded architecture-review analysis covering safety, privacy, accessibility, model drift, integration, downtime, override, and accountable authority.

## Answers to the Exercises

### Answer 1

A claim is a proposition about architecture behavior. Evidence is information offered to support or challenge it. An argument states how evidence and assumptions justify the claim and where that inference is limited. A finding is the review's traced conclusion about risk, adequacy, trade-off, sensitivity, constraint, disagreement, or evidence gap. A decision is the accountable choice. A condition is an enforceable requirement attached to that choice. Closure evidence is the specified observation or authority needed to change a finding's state.

An inventory establishes discoverability and provenance, not relevance or sufficiency. Ten artifacts may address a component while none supports the system claim; they may share one invalid data source. A complete answer distinguishes documents from the reasoning that connects them and keeps reviewer inference separate from decision authority.

### Answer 2

Structural coverage is $4/5=0.8$ because four critical claims have at least one linked artifact. It reveals one structurally unsupported claim. It does not establish that 80% of the architecture is ready, that the four claims are true, or that evidence is independent and current.

The three claims relying on one stale component benchmark need separate relevance, external-validity, freshness, and composition review. They may all remain inconclusive. The review should identify which architecture revision and system scenarios the benchmark covers, reproduce decisive results in a representative environment, and obtain different evidence where failure modes differ. Reject any answer that multiplies document count into confidence.

### Answer 3

The routing test supports route change only under its test conditions. The vendor statement must be checked for product, version, region, configuration, exclusions, data authority, and customer responsibilities. Eighteen incident-free months are weak without exposure frequency and detection coverage and do not exercise a regional failure.

Decompose the claim into detection, isolation, traffic shift, identity, configuration, data consistency, stale-writer fencing, capacity during failure, queue and retry recovery, client behavior, integrity, and return to normal. Run a production-like regional-isolation exercise at representative peak and state, with timed end-to-end outcomes, duplicate and loss checks, operator authority, telemetry from clients through dependencies, abort conditions, and recovery validation. An analytical dependency and capacity model should predict the exercise; discrepancies become findings.

### Answer 4

Charter the decision, candidates, two- or three-year horizon, architecture revisions, required outcomes, evidence cutoff, advisory or gate authority, and default. Include product, users, platform and application engineers, operations, security, privacy, accessibility, data governance, finance, procurement, legal, support, and supplier roles as relevant; disclose vendor and delivery interests.

Scenarios should cover nominal and peak demand, tenant isolation, region or provider loss, control-plane compromise, data retention and exit, version change, incident support, cost growth, migration, and retirement. Compare equivalent quality. Evidence includes deployed prototypes, load and failure experiments, dependency and threat models, cost and migration models, contract and assurance scope, incident history, staffing evidence, and customer outcome data. Record conflicts and unknowns instead of averaging them. Outcomes may approve, condition, defer, reject relative to criteria, or refer specialist questions. Every condition needs an owner, deadline, evidence, failure consequence, expiry, and re-review trigger.

### Answer 5

The review must not decide that funding urgency lowers clinical safety. Charter the decision as authorization of a specific workflow, model version, patient population, deployment, and operating mode. Include clinicians, pharmacists, patients or representatives, safety, privacy, security, accessibility, clinical engineering, operations, data governance, legal and regulatory authorities, and the vendor. Preserve conflicts of interest and dissent.

Claims cover appropriate recommendations by cohort, harmful omission and commission, calibration and drift, provenance and privacy, accessible presentation, integration correctness, latency, downtime, fallback, clinician override, alert burden, audit, update, rollback, and recovery. Vendor benchmark evidence is checked for population and external validity; local silent or limited trials test representative workflow without transferring unsupervised authority. Alert-fatigue evidence challenges realized safety even if model discrimination is high. Analyze malicious input and supplier loss, and require post-deployment monitoring with stop rules.

The architecture review may recommend a constrained, reversible evaluation or defer deployment. Only authorized clinical, safety, privacy, legal, and regulatory bodies can accept their respective consequences. Funding deadlines are recorded as drivers, not evidence. Conditions specify population, supervision, fallback, access, monitoring, independent evaluation, incident response, closure evidence, and automatic suspension. This answer is a review model, not medical, safety, privacy, security, accessibility, legal, or regulatory approval.
