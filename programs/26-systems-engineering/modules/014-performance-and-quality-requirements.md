---
module_id: SYSENG-014
program: Systems Engineering
level: 1
module_number: 14
title: Performance and Quality Requirements
status: complete
last_verified: 2026-08-30
---

# Performance and Quality Requirements

## One-Page Review

### Governing question

How can engineers specify how well a system must perform and which qualities it must exhibit, under explicit workloads, populations, environments, modes, and evidence rules, without turning aspirations, averages, or measurement proxies into unjustified guarantees?

### Essential definitions

- A **performance requirement** quantifies how well or how much a function must execute: time, rate, volume, capacity, accuracy, precision, resource use, range, or another measurable characteristic.
- A **quality requirement** constrains an attribute that affects stakeholder acceptability, such as reliability, availability, safety, security, usability, accessibility, maintainability, compatibility, flexibility, or resilience.
- A **measure** maps observations to a value according to a defined method; a **metric** is a governed use of a measure for assessment or decision.
- A **measurement condition** specifies workload, population, mode, configuration, environment, dependencies, starting state, and observation window.
- A **threshold** separates acceptable from unacceptable observed values; a **target** guides improvement; an **objective** expresses desired outcome. They do not have identical authority.
- **Tolerance** defines permitted deviation around a nominal value or boundary; **margin** is the distance between required limit and predicted/observed capability.
- An **aggregation** summarizes observations—mean, quantile, worst observed, proportion, rate, or distribution—and can hide important variation.
- **Measurement uncertainty** characterizes doubt associated with a result; **sampling uncertainty** arises because observations cover only part of the relevant population/process.
- A **service level objective** is an operational target for a service measure over a window; it becomes a contractual requirement only under the appropriate baseline and authority.
- A **technical performance measure (TPM)** tracks a selected critical characteristic during realization; it is not automatically the requirement itself.

### Central model, mechanism, or theorem

Record a quantitative obligation as:

\[
q=\langle id,subject,function/quality,conditions,population,measure,
method,aggregation,operator,threshold,tolerance,window,confidence,
source,rationale,verification\rangle.
\]

Measurement is conditional:

\[
Y=M(SoI,workload,population,environment,mode,configuration,method).
\]

A statistical requirement may take the form:

\[
P(Y\le T\mid C)\ge p,
\]

but only if \(Y,T,C,p\), sampling, estimation, and acceptance rules are defined. Passing a finite test supports a bounded acceptance claim; it does not prove universal future behavior.

### Critical invariants

- Every measure traces to a stakeholder outcome, function, hazard, constraint, or justified derived need.
- The measured entity, property, unit, direction, method, and decision rule are explicit.
- Workload, population, mode, environment, configuration, dependencies, and observation window accompany every threshold.
- Aggregations preserve relevant tails, subgroups, bursts, and failure states instead of hiding them behind averages.
- Accuracy, precision, resolution, uncertainty, and correctness are not used interchangeably.
- Product quality, quality in use, process quality, and service outcomes remain distinct but traceable.
- Thresholds have evidence, rationale, authority, tolerance, and feasibility analysis; invented precision is marked unresolved.
- Verification method can distinguish satisfaction under representative conditions and reports uncertainty and exclusions.
- Requirements, design margins, operational objectives, budgets, and TPM forecasts remain separate controlled artifacts.
- High-consequence safety, security, clinical, human-performance, and regulatory claims require applicable independent authority.

### Common failures

Failures include “fast,” “scalable,” “user-friendly,” “highly available,” or “secure” without operational definitions; threshold without workload; average without tails; percentage without denominator/window; availability without service boundary; capacity without response quality; accuracy without reference truth and error cost; benchmark on nonrepresentative data; summing incompatible percentiles; treating zero observed failures as zero risk; choosing a taxonomy label as a requirement; turning current instrumentation into the only legitimate measure; and using a green dashboard to claim stakeholder outcome.

### Compact example

Weak: “The emergency-alert service shall be highly available and respond in under two seconds.” Better linked obligations identify the function and conditions: for authorized alert submissions during the defined regional emergency workload, at least 99% of accepted submissions in each rolling five-minute window produce an acceptance or rejection status within two seconds, measured at the stated service boundary with synchronized clocks and specified exclusions. Separate requirements define end-to-end dissemination, dependency loss, recovery, accessibility, correctness, and population coverage. The improved wording is measurable, but its threshold still needs outcome evidence and feasibility review.

### Connections

Retrieve measures of effectiveness from SYSENG-002, uncertainty and assumptions from SYSENG-007–008, operational scenarios from SYSENG-009/012, stakeholder needs from SYSENG-011, and functional requirements from SYSENG-013. Continue to constraints, requirement quality/testability, decomposition, allocation, traceability, and change. Later trade studies, reliability, safety, resilience, verification, validation, and human factors deepen measurement and evidence.

## Governing Question

A function states what the system must do. Stakeholders also care how quickly, accurately, reliably, safely, accessibly, maintainably, and efficiently it does so. These qualities shape architecture and cost, often more strongly than the functional list. Yet quality language is especially vulnerable to ambiguity and proxy substitution.

The governing question joins specification and epistemology: what property matters, how will it be observed, under which conditions, over which population and time, using which aggregation and uncertainty model, and why is the boundary acceptable? A number without these semantics is not precise. It is merely numerically decorated ambiguity.

## Why This Matters

Systems can satisfy nominal function while failing operationally through latency tails, overload collapse, inaccessible interaction, poor recovery, correlated failure, diagnostic burden, or resource exhaustion. Conversely, unjustifiably tight thresholds can force costly architecture, reduce resilience, or exclude viable suppliers without improving stakeholder outcomes. Performance and quality requirements are allocation of scarce design freedom and risk.

ISO/IEC/IEEE 29148:2018 treats measurable performance and quality characteristics as part of well-formed requirements engineering. NASA distinguishes measures of effectiveness (stakeholder/mission view), measures of performance (quantitative supplier view), and selected TPMs used to track critical realization progress. These related measures must not be collapsed into one number.

ISO/IEC 25010:2023 defines a current product-quality model for ICT and software products with nine characteristics and subcharacteristics. ISO/IEC 25023:2016 defines example product-quality measures and is currently published but marked by ISO for revision. Neither supplies universal acceptance thresholds: measures and limits depend on system category, integrity, users, context, and consequence.

## Prerequisites and Retrieval

Before continuing, retrieve:

1. stakeholder value is indexed by stakeholder, outcome, context, distribution, and time;
2. operational concepts define roles, modes, workloads, environments, support, and failure conditions;
3. a functional requirement supplies the behavior whose performance or quality is constrained;
4. assumptions, dependencies, and external service boundaries affect achievable observations;
5. evidence has scope and uncertainty and does not automatically generalize beyond observed conditions;
6. verification compares realization with requirements, while validation returns to stakeholder outcomes;
7. trace links require transformation rationale rather than identifier adjacency.

As a retrieval test, analyze “99.9% reliable.” Ask: reliable with respect to which required function, failure definition, population, mission duration, configuration, maintenance policy, dependencies, and confidence? Is the intended quantity probability of mission success, failure-free time, request success rate, data durability, or availability? The percentage is unusable until its random experiment and decision meaning are defined.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish performance, quality, effectiveness, service objectives, budgets, margins, and TPMs;
2. construct complete measurement definitions with entity, property, unit, method, conditions, aggregation, and decision rule;
3. specify timing, throughput, capacity, accuracy, resource, reliability, availability, usability, maintainability, security, and resilience obligations;
4. select aggregations that reveal relevant distributions, tails, subgroups, bursts, and failure states;
5. reason about tolerance, uncertainty, sample size, confidence, and bounded acceptance claims;
6. derive thresholds from stakeholder outcomes, hazards, constraints, and trade evidence without invented precision;
7. separate product quality from quality in use, process indicators, and operational outcomes;
8. analyze interacting quality attributes, feasibility, margin, and measurement distortion;
9. design verification evidence and monitoring consistent with requirement semantics;
10. state limits and obtain appropriate authority for consequential judgments.

## Core Exposition

**Begin with outcome and function.** A metric is justified because a stakeholder outcome, functional chain, hazard control, interface, or lifecycle obligation depends on it. Ask what adverse outcome occurs if performance is worse and whether the measure predicts that outcome. “Because the dashboard tracks it” is instrumentation provenance, not need rationale.

**Classify the obligation.** Performance commonly covers latency, response time, deadline, throughput, rate, capacity, concurrency, range, accuracy, precision, resource consumption, mass, power, or physical response. Quality attributes organize broader concerns. The boundary is contextual: availability can be a quantitative performance property and a quality characteristic. Classification supports ownership; requirement semantics matter more than the label.

**Name the measured entity and boundary.** End-to-end user response differs from server execution; accepted requests differ from attempted requests; system availability differs from one component's process uptime. Specify start and stop events, inclusion, exclusion, observation location, clock, identity, and responsibility. A narrow boundary may be useful for diagnosis but cannot substitute for the stakeholder-facing obligation.

**Define conditions as part of the requirement.** Record workload mix and arrival pattern, population, data distribution, concurrency, mode, environment, configuration, dependency states, resource limits, warm-up, starting state, and observation window. “Under normal load” is circular unless normal is separately governed. Include peak, burst, degraded, and recovery conditions when outcomes depend on them.

**Choose the property and unit.** Define dimensional meaning and direction. Latency in milliseconds, throughput in completed transactions per second, capacity in concurrent authorized sessions, error in physical units, mass in kilograms, and energy in joules are not interchangeable. For ratios, define numerator, denominator, eligibility, and treatment of missing observations.

**Define the measurement function.** Explain instrumentation, sampling, reference standard, preprocessing, time synchronization, treatment of retries/cancellations/timeouts, censoring, missing data, and calculation. Version the method. Changing a histogram boundary, reference label, or eligibility filter can change the metric without changing the system.

**Select aggregation by consequence.** Mean describes central tendency but can hide a long tail. Median ignores rare severe delay. Quantiles describe a distribution position but require window, estimator, and sample considerations. Maximum observed depends strongly on sample size and is not a universal worst case. Rates obscure clustering. Report distributions and stratified results when consequence is nonlinear or unevenly distributed.

**Write comparison semantics.** Use explicit operator, threshold, tolerance, and boundary inclusion: \(x\le2\,s\) differs from \(x<2\,s\). State whether every event, a proportion, or an aggregate must comply. For a percentile requirement, define eligible population, window, minimum samples, estimator, and low-volume rule. Do not say “p99 average.”

**Distinguish latency, throughput, and capacity.** Latency measures duration for an observation. Throughput measures completed work per time. Capacity identifies the workload envelope within which other requirements hold. Increasing concurrency may raise throughput until queues or contention increase latency and failure. Specify these properties together under a workload model rather than optimizing one in isolation.

**Model queues and bursts.** Long-run arrival rate below average service rate is not sufficient when variability, batching, priority, or finite buffers exist. Observe queue length, wait time, service time, abandonment, rejection, and recovery after bursts. Queueing models and load tests are evidence under assumptions, not universal predictions.

**Define accuracy and its relatives.** Accuracy concerns closeness to a reference or correct classification under a defined task. Precision may mean repeatability or, in classification, positive predictive value; define usage. Resolution is the smallest represented increment. Bias, variance, calibration, sensitivity, specificity, and uncertainty answer different questions. State reference truth, population, cost of errors, and subgroup behavior.

**Specify resource and physical performance.** Mass, power, energy, thermal load, memory, storage, network, consumables, staffing, space, and maintenance time interact. State operational profile and lifecycle condition. Preserve reserve/margin separately from the required limit, because consuming design margin is not automatically a requirement failure but is a management warning.

**Treat quality models as prompts, not checklists.** A taxonomy helps discover omitted concerns and standardize vocabulary. Select attributes because stakeholders and system context require them. Define each as observable properties and scenarios. A label such as “maintainability” cannot be verified until change type, system boundary, competence, tools, environment, restoration condition, and measure are specified.

**Separate product quality and quality in use.** Product response-time behavior may contribute to a user's task completion, but task effectiveness also depends on workflow, training, environment, accessibility, other systems, and policy. Code coverage is a process/product indicator, not reliability or safety outcome. Link layers without claiming one proxy guarantees another.

**Specify reliability and availability carefully.** Reliability concerns successful performance over a stated mission/time and conditions. Availability concerns readiness for required use at an observation point and depends on failure and restoration. The observed ratio

\[
\hat A=\frac{observed\ available\ time}{eligible\ observation\ time}
\]

requires rules for partial service, planned maintenance, dependency failure, measurement gaps, and user impact. It is an estimate or accounting result, not proof of future availability.

**Specify recoverability and resilience as trajectories.** Time to detect, contain, restore minimum service, reconcile, and recover full service can be measured. Also specify retained capability, data/state integrity, authority, degraded duration, and repeated-event behavior. A single recovery-time number can reward unsafe restoration if end-state correctness is absent.

**Operationalize usability and accessibility.** Use representative users, tasks, environments, assistive technologies, learning state, errors, recovery, workload, satisfaction, and outcome measures. Completion averages can exclude people unable to begin. Conformance to applicable accessibility standards may be a constraint; representative evaluation supplies different evidence.

**Operationalize maintainability and supportability.** Identify change/failure classes, diagnostic evidence, access, skills, tools, spares, documentation, environment, and return-to-service criteria. Measure diagnosis, repair, verification, deployment, and recurrence separately. A mean time can conceal rare but operationally dominant repairs.

**Treat safety and security as risk-informed qualities.** “No failures” or “100% secure” is generally not a measurable product obligation. Specify protective, detection, response, recovery, and assurance properties derived from hazards/threats while governing residual risk separately. Passing functional controls does not prove acceptable safety or security.

**Derive thresholds with evidence.** Use stakeholder outcome studies, physiological/physical boundaries, hazard analysis, law and standards interpreted by authority, interface contracts, operational baselines, experiments, models, prototypes, and trade studies. Record rationale, source, uncertainty, feasibility, cost sensitivity, and who may accept residual risk. If evidence is incomplete, use a governed TBR rather than fabricated decimals.

**Analyze interaction and feasibility.** Latency, energy, accuracy, availability, safety, privacy, maintainability, and cost can conflict. Build budgets and models, explore sensitivity, and verify combined workload. Component thresholds do not compose automatically: percentile latencies cannot generally be added to obtain an end-to-end percentile, and independent failure assumptions need evidence.

**Plan acceptance statistics.** Define sampling unit, population, stratification, sample size rationale, estimator, confidence or credible interval where applicable, false-accept/false-reject consequences, missing-data rule, repetitions, seeds/configurations, and acceptance calculation. A threshold on an estimated quantile without an inference rule invites post-hoc judgment.

**Link pre-deployment and operational evidence.** Tests establish behavior in controlled environments; production/field monitoring reveals changing workloads and dependencies. Align metric semantics so they can be compared, while respecting privacy, safety, observability gaps, and operational confounding. Monitoring does not retroactively make a vague requirement precise.

**Use automated record checks as bounded evidence.** The example detects missing condition fields, vague quality text, and missing thresholds in declared records. It does not assess whether measures represent stakeholder value or whether statistical evidence is sufficient.

<!-- bijux-verify: {"id":"performance-quality-record-check","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"records_total=5\nwell_formed_declared=1\nmissing_population=PQ-002\nmissing_window=PQ-004\nmissing_threshold=PQ-003\nvague_quality=PQ-003:highly available\nmissing_uncertainty_rule=PQ-005\nrecord_set_ready=false\nevidence=declared_fields_and_lexical_signals_only\n","stderr":""}} -->
```python
records = [
    {"id": "PQ-001", "property": "response latency", "population": "accepted emergency alerts",
     "condition": "regional peak profile", "aggregation": "p99", "threshold": "<=2", "unit": "s",
     "window": "rolling 5 min", "uncertainty": "minimum 100 samples; defined estimator"},
    {"id": "PQ-002", "property": "task completion", "population": "",
     "condition": "representative assisted-use study", "aggregation": "proportion", "threshold": ">=0.95",
     "unit": "ratio", "window": "study session", "uncertainty": "stratified interval"},
    {"id": "PQ-003", "property": "highly available", "population": "eligible service minutes",
     "condition": "normal and dependency-loss modes", "aggregation": "ratio", "threshold": "",
     "unit": "ratio", "window": "calendar month", "uncertainty": "accounting rule"},
    {"id": "PQ-004", "property": "recovery time", "population": "declared priority incidents",
     "condition": "regional service loss", "aggregation": "p90", "threshold": "<=30", "unit": "min",
     "window": "", "uncertainty": "incident census with exclusions"},
    {"id": "PQ-005", "property": "classification sensitivity", "population": "validated hazard cases",
     "condition": "declared operating domain", "aggregation": "proportion", "threshold": ">=0.98",
     "unit": "ratio", "window": "evaluation release", "uncertainty": ""},
]

required = ("property", "population", "condition", "aggregation", "threshold", "unit", "window", "uncertainty")
vague = ("highly available", "fast", "scalable", "user-friendly")
complete = [r for r in records if all(r[k] for k in required) and r["property"] not in vague]

print(f"records_total={len(records)}")
print(f"well_formed_declared={len(complete)}")
print("missing_population=" + ",".join(sorted(r["id"] for r in records if not r["population"])))
print("missing_window=" + ",".join(sorted(r["id"] for r in records if not r["window"])))
print("missing_threshold=" + ",".join(sorted(r["id"] for r in records if not r["threshold"])))
print("vague_quality=" + ",".join(sorted(f'{r["id"]}:{r["property"]}' for r in records if r["property"] in vague)))
print("missing_uncertainty_rule=" + ",".join(sorted(r["id"] for r in records if not r["uncertainty"])))
print(f"record_set_ready={str(len(complete) == len(records)).lower()}")
print("evidence=declared_fields_and_lexical_signals_only")
```

## Definitions and Notation

Let \(S\) be the system, \(W\) workload, \(P\) population, \(E\) environment, \(M\) mode, \(K\) configuration, and \(H\) observation horizon. A measure is a function \(m(S,W,P,E,M,K,H)\) with a documented procedure and unit.

For observations \(x_1,\ldots,x_n\), the arithmetic mean is \(\bar x=n^{-1}\sum x_i\). An empirical \(p\)-quantile is defined by the selected estimator; tools use differing conventions, so name it. A proportion \(\hat p=k/n\) is incomplete without eligibility and treatment of missing/censored cases.

**Latency** is duration per operation; **throughput** is completed operations per time; **capacity** is the workload boundary within which linked requirements hold; **utilization** is resource use relative to a defined capacity. **Reliability**, **availability**, **maintainability**, **recoverability**, and **resilience** describe different properties even when their measures interact.

**Accuracy**, **precision**, **resolution**, **bias**, **repeatability**, **calibration**, and **uncertainty** retain discipline-specific definitions. Declare which definition applies. **Margin** \(g=T-Predicted) depends on whether larger or smaller is better; always define sign convention.

## Mechanisms, Invariants, or Proof Structure

The mechanism has seven steps: trace the outcome; identify the function/quality; define entity and conditions; define measurement method and aggregation; derive threshold/tolerance; plan inference and verification; review interactions and validation. Each step can invalidate the previous wording.

For requirement \(q\), use the readiness predicate:

\[
Ready(q)=Source\land DefinedProperty\land Conditions\land Measure\land
DecisionRule\land Uncertainty\land Feasible\land Verifiable.
\]

The predicate is an audit structure. Several terms require empirical and domain judgment; a nonempty field is not proof.

Maintain five invariants. **Semantic invariant:** metric meaning is stable across requirement, test, and operation. **Context invariant:** threshold never detaches from workload/population/environment. **Distribution invariant:** aggregation does not erase consequence-relevant variation. **Evidence invariant:** result includes method, uncertainty, exclusions, and raw provenance. **Outcome invariant:** optimization remains linked to stakeholder value and guardrails.

For composed systems, derive end-to-end budgets only under valid algebra and dependency assumptions. Deterministic upper bounds can sometimes sum; empirical quantiles generally cannot without joint-distribution information. Reliability multiplication assumes a specific success structure and independence. State composition assumptions and challenge common-cause behavior.

## Alternatives and Trade-Offs

**Hard bound versus statistical objective.** Hard bounds suit physical/safety limits when demonstrably enforceable. Statistical objectives fit variable workloads but require population, window, estimator, and risk rules. Do not use probabilistic wording to hide an essential hard constraint.

**Mean versus tail versus distribution.** Means are compact; tails reveal rare delay; full distributions support diagnosis. Select by consequence and combine views where one statistic is insufficient.

**Synthetic versus field evidence.** Synthetic tests offer control and repeatability; field data offer realism and drift. Field data are confounded and incomplete; synthetic profiles can be unrepresentative. Maintain semantic alignment and use both proportionally.

**Universal versus segmented threshold.** One threshold simplifies governance but can mask populations or modes. Segmentation reveals inequity and special conditions but increases sample and control complexity. Segment when outcome or risk differs materially.

**Product measure versus outcome measure.** Product measures are actionable for engineering; outcome measures validate value. Neither substitutes for the other. Link them through an explicit causal hypothesis and test it.

**Tight target versus design freedom.** Tighter limits can improve outcomes or merely increase cost and fragility. Explore threshold sensitivity, alternative mechanisms, feasibility, and lifecycle consequences before baseline.

## Failure Modes and Misconceptions

1. **“A number makes a requirement precise.”** Undefined population, method, and condition leave numeric ambiguity.
2. **“Average performance represents users.”** Means can hide tails, abandonment, inaccessible starts, and subgroup harm.
3. **“p99 means worst case.”** It leaves one percent beyond the threshold and depends on estimator/window/sample.
4. **“Component objectives compose.”** Correlation, queues, shared dependencies, and end-to-end boundaries invalidate naive addition or multiplication.
5. **“Zero observed failures proves reliability.”** It supplies finite evidence under tested exposure only.
6. **“Availability equals process uptime.”** Required service, partial degradation, dependencies, and user boundary matter.
7. **“Quality model categories are requirements.”** Categories prompt discovery; projects must derive observable properties and thresholds.
8. **“Benchmark results are portable.”** Hardware, software, data, configuration, workload, and method define the result.
9. **“Monitoring proves causality.”** Operational association can reveal change but not necessarily its mechanism.
10. **“Meeting every metric validates the system.”** Wrong or incomplete measures can all be green while stakeholder outcomes fail.

## Worked Examples

### Example 1

**Situation.** An API requirement says average latency below 200 ms. **Reasoning.** Identify accepted request classes, start/stop boundary, concurrency, payload, cache state, region, dependency mode, and window. A 190 ms mean can coexist with multi-second tail delay. Link median and upper quantile to outcome, plus timeout/error treatment and minimum samples. **Conclusion.** Average alone is not adequate when tail delay affects the operational thread.

### Example 2

**Situation.** A batch pipeline must process one million records per hour. **Reasoning.** Throughput is meaningless without record-size/distribution, transformation mix, input quality, resources, start state, checkpointing, failure, and output correctness. Define completion and rejected-record handling; measure recovery after worker loss. **Conclusion.** Capacity is the envelope in which correctness, latency, and recovery obligations jointly hold.

### Example 3

**Situation.** A sensor is “accurate to 1 degree.” **Reasoning.** Determine quantity, unit, operating range, reference standard, calibration state, bias, repeatability, resolution, environmental conditions, confidence, and whether ±1 is maximum permissible error or statistical interval. **Conclusion.** Accuracy requires a metrological definition, not a lone tolerance.

### Example 4

**Situation.** A service claims 99.9% availability. **Reasoning.** Define service boundary, eligible minutes, partial service, regions/tenants, planned maintenance, dependency failures, measurement gaps, and rolling/calendar window. Monthly 99.9% permits roughly 43.2 minutes under simple accounting, but clustered loss during an emergency may be unacceptable. **Conclusion.** Availability ratio and operational consequence require linked but distinct requirements.

### Example 5

**Situation.** A search system improves overall success from 90% to 94%. **Reasoning.** Stratification shows 98% for dominant-language queries and 62% for a smaller language group. Overall aggregation weights usage, not rights or consequence. Define representative populations, per-group outcomes, uncertainty, and guardrails. **Conclusion.** Distributional requirements prevent aggregate improvement from concealing exclusion.

### Example 6

**Situation.** A repair requirement uses mean time to restore. **Reasoning.** Separate detection, diagnosis, access, parts, repair, verification, and return-to-service; stratify failure class and operating environment. A mean hides rare 30-day supply delays. Include percentile/censoring and minimum service restoration. **Conclusion.** Maintainability is a workflow-conditioned quality, not one universal mean.

### Example 7

**Situation.** Three sequential services each advertise p99 latency of 100 ms. **Reasoning.** Adding yields 300 ms only as an unsupported heuristic: each request may occupy different percentile ranks and latencies may correlate through load/shared dependencies. Measure end-to-end or model the joint distribution; deterministic bounds require different evidence. **Conclusion.** Percentiles do not generally compose by addition.

### Example 8

**Situation.** No failures occur in 1,000 independent test missions. **Reasoning.** This contradicts neither rare risk nor untested conditions. Under a simple binomial model, the rough 95% upper failure-probability bound is about \(3/1000\), subject to independence and representativeness. Common-cause exposure breaks the model. **Conclusion.** Zero observations bound risk only under explicit statistical assumptions; they do not prove perfect reliability.

### Example 9

**Situation.** A portal is declared accessible because automated checks pass. **Reasoning.** Static checks cover detectable rules, not task comprehension, focus order under dynamic changes, assistive-technology interoperability, cognitive load, recovery, language, or real environments. Combine applicable conformance tests with representative task evaluation and issue recourse. **Conclusion.** Automated conformance is useful evidence but not complete accessibility validation.

### Example 10

**Situation.** An AI clinical classifier requires 98% sensitivity. **Reasoning.** Define operating domain, reference labels, disease prevalence, inclusion, subgroup stratification, missing data, confidence interval, version, drift, false-positive consequences, abstention, and workflow outcome. Sensitivity alone omits calibration and clinical benefit. **Conclusion.** A numeric model metric cannot establish safe clinical operation without representative clinical and regulatory evidence.

## Cross-Program Connections

- [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md) uses quality-attribute scenarios and budgets to compare architecture alternatives.
- [Data Engineering](../../19-data-engineering/ROADMAP.md) governs measurement data quality, lineage, missingness, workload distributions, and reproducible aggregation.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) connects protection qualities to threat, risk, detection, response, recovery, and assurance evidence.
- [API & Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) operationalizes latency, throughput, availability, correctness, and compatibility at service boundaries.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md) measures developer outcomes, platform reliability, supportability, and shared-resource behavior without proxy gaming.
- [Cloud & Infrastructure Engineering](../../30-cloud-and-infrastructure-engineering/ROADMAP.md) supplies workload, scaling, failure, regional, resource, and cost evidence for distributed quality claims.

## References

1. ISO/IEC/IEEE. [ISO/IEC/IEEE 29148:2018 — Requirements engineering](https://www.iso.org/standard/72089.html), second edition, 2018. Consulted 2026-08-30.
2. ISO/IEC. [ISO/IEC 25010:2023 — Product quality model](https://www.iso.org/standard/78176.html), second edition, November 2023. Consulted 2026-08-30.
3. ISO/IEC. [ISO/IEC 25023:2016 — Measurement of system and software product quality](https://www.iso.org/standard/35747.html), first edition, June 2016; ISO currently marks it for revision. Consulted 2026-08-30.
4. NASA. [Technical Requirements Definition](https://www.nasa.gov/reference/4-2-technical-requirements-definition/), including measures of performance and technical performance measures. Consulted 2026-08-30.
5. NASA. [Systems Engineering Handbook Appendix](https://www.nasa.gov/reference/system-engineering-handbook-appendix/), Appendix C requirement checklist. Consulted 2026-08-30.
6. SEBoK Editorial Board. [System Requirements Definition](https://sebokwiki.org/wiki/System_Requirements_Definition), *Guide to the Systems Engineering Body of Knowledge*, version 2.14. Consulted 2026-08-30.
7. Jain, R. *The Art of Computer Systems Performance Analysis*. Wiley, 1991.
8. Lilja, D. J. *Measuring Computer Performance: A Practitioner's Guide*. Cambridge University Press, 2000.

## Exercises

### Exercise 1

Explain why “the service shall be fast, scalable, reliable, and user-friendly” is not a usable requirement. Produce a measurement-definition checklist without inventing thresholds.

### Exercise 2

Rewrite “95% of requests finish within one second” for an emergency information service. Define boundary, workload, population, window, exclusions, errors, estimator, sample rule, uncertainty, and linked guardrails.

### Exercise 3

Analyze whether three component availability objectives of 99.9% imply 99.9% end-to-end availability. Compare serial, redundant, dependent, and degraded-service structures.

### Exercise 4

Design a verification strategy for maintainability of a field medical device, including failure classes, roles, environment, censoring, safety, restoration state, sampling, and external authority.

### Exercise 5

Develop performance and quality requirements for an evacuation-routing capability used during wildfire. Include outcomes, workload/environment, timing, accuracy, availability, accessibility, resilience, security/privacy, uncertainty, tradeoffs, and evidence limits.

## Answers to the Exercises

### Answer 1

The sentence names four quality aspirations but no measured entity, function, stakeholder outcome, conditions, population, method, aggregation, threshold, tolerance, window, or acceptance evidence. `Scalable` is especially relational: behavior as workload/resources change. `User-friendly` obscures users, tasks, accessibility, errors, and context. One compound sentence also prevents independent source, trade, allocation, and verification.

For each quality record capture source/outcome; SoI and service boundary; related function; property and operational definition; population/workload/data distribution; mode/environment/configuration/dependencies; start/stop events; measurement method/instrumentation/unit; missing/error/censoring rule; aggregation and segmentation; operator/threshold/tolerance; window and minimum sample; uncertainty/inference and false-decision consequence; feasibility/margin; verification method; and authority. Evidence is needed before thresholds are baselined; unresolved values remain governed TBRs.

### Answer 2

A candidate form is: “For eligible public emergency-information queries received at the public service boundary during the declared regional peak profile, at least 95% in each rolling five-minute window shall produce a complete status response within 1.0 seconds from receipt, using the governed quantile/proportion calculation and low-volume rule.” Then define query classes/payloads, regions, identity states, concurrency/arrival bursts, cache/warm state, dependency modes, synchronized boundary clocks, complete response, retries, cancellations, timeouts, rejected/failed requests, minimum samples, estimator, and confidence/acceptance rule.

Do not exclude failed requests merely to improve latency. Link correctness, freshness, availability, accessibility, privacy, overload/degraded behavior, end-to-end user receipt, and recovery guardrails. Derive 95% and one second from emergency decision/outcome evidence and consequence, not convenience. Test controlled profiles and failure modes, report raw distributions and uncertainty, then compare operational monitoring with identical semantics. Passing the test supports only those configurations and conditions.

### Answer 3

No. If all three are required in series and failures are independent with equal availability \(0.999\), a simplified steady-state estimate is \(0.999^3\approx0.997003\), not 0.999. If components are redundant, service availability depends on success logic, failover coverage, repair, state consistency, and shared dependencies. If failures correlate through power, network, configuration, operator, or traffic, independence multiplication is invalid. If the system offers degraded service, binary component uptime may not match stakeholder availability.

Define end-to-end required service and observation point; architecture success/failure states; partial-service rules; planned maintenance; dependencies; detection/failover/restoration; data correctness; and window. Use reliability/availability models with sensitivity and common-cause cases, failure-injection and recovery tests, and field evidence. Component objectives are budgets or evidence inputs; the end-to-end requirement needs direct semantics and verification.

### Answer 4

Classify failures by safety consequence, affected function, diagnosis access, replace/repair action, software/configuration involvement, parts, and environment. Roles include user/caregiver, trained technician, clinical operator, supplier, quality/safety, and return-to-service authority. Measure detection, diagnosis, safe isolation, logistics delay, active repair, calibration/configuration, verification, restoration, recurrence, and unavailable time separately. Define whether unresolved/censored repairs remain in the sample; a mean that drops them is biased.

Use representative devices, ages, configurations, tools, documentation, competence, homes/clinics, network/power, contamination controls, and seeded plus observed faults. Record distributions and high-consequence cases rather than only averages. A restored state requires verified safe function, correct configuration/calibration, records, notification, and clinical continuity—not power-on. Evidence combines design inspection, maintainability demonstration, fault insertion, service records, human-factors evaluation, and traceability. Internal testing cannot establish clinical safety or regulatory acceptance; applicable clinical, quality, safety, human-factors, maintenance, and regulatory authorities review the plan and residual risk.

### Answer 5

Stakeholder outcomes are timely safe movement, understandable direction, protection of people unable to use the primary channel, responder coordination, and avoidance of routes that increase exposure. Define populations, geography, fire/smoke/weather states, road capacity/closures, connectivity/power loss, demand surges, data ages, vehicle/pedestrian/accessibility needs, and authority. Performance requirements may cover time from authorized state change to route publication, update cadence, query/notification capacity, stale-input detection, and recovery. Accuracy requires authoritative road/hazard reference, spatial/temporal error, uncertainty, and conflict handling—not one generic percentage.

Quality obligations cover availability across regions and degraded modes; comprehensibility and accessibility across language, disability, stress, and devices; resilience through dependency loss and reconciliation; security of authority and resistance to false updates; privacy/minimization of location data; maintainability/support during long incidents; and traceable decision provenance. Segment measures by population and location, retain tails and abandonment, and pair fast routing with safety/exposure guardrails. Explore central versus local data/authority, personalization versus privacy, conservative closure versus mobility, and freshness versus disconnected operation.

Evidence combines scenario and hazard analysis, map/data audits, simulation with sensitivity, load/failure tests, field exercises, representative comprehension/task studies, security review, and after-action operational evidence. Models cannot predict every fire, traffic response, or human decision; historical data may omit unprecedented conditions and marginalized populations. Emergency management, fire behavior, transport, accessibility/community, safety, security/privacy, human-factors, geographic-data, and applicable legal/regulatory authorities must review consequential thresholds. No external review is claimed.
