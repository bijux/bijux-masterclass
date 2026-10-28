---
module_id: SDRE-055
program: Software Engineering: Software Delivery & Reliability Engineering
level: 2
module_number: 55
title: Technical Investigation Under Pressure
status: draft
last_verified: 2026-09-06
---

# Technical Investigation Under Pressure

## One-Page Review

### Governing question

How can responders reduce uncertainty about a live failure quickly enough to guide safe action, while resisting cognitive bias, protecting users and evidence, and avoiding experiments that make the incident worse?

### Essential definitions

- a **problem statement** describes the observed deviation, affected outcome, scope, onset, and evidence confidence without asserting a cause;
- a **system model** describes relevant components, interfaces, state, dependencies, control paths, and expected behavior;
- a **hypothesis** is a falsifiable candidate explanation; a **prediction** states what evidence should follow if it is true;
- a **discriminating observation** changes the relative plausibility of competing hypotheses;
- a **probe** observes a bounded property; an **intervention** changes input, configuration, traffic, code, or state to test or protect;
- a **baseline** is a comparable known condition; a **cohort** is a group selected by a declared property for comparison;
- **correlation** is statistical or temporal association; **causation** requires a mechanism and evidence that alternatives do not explain as well;
- **confounding** occurs when another variable affects both the suspected cause and the observed outcome;
- **selection bias** arises when observed requests, hosts, logs, or users are not representative of the affected population;
- **observer effect** is investigation-induced behavior change, such as load from tracing or cache warming by probes;
- an **evidence ledger** records facts, provenance, hypotheses, tests, results, decisions, and uncertainty without rewriting history;
- a **stopping rule** says when to act, escalate, abandon a line of inquiry, or defer deeper diagnosis.

### Central model, mechanism, or theorem

Use a bounded hypothetico-deductive loop:

$$
\text{observe}\rightarrow\text{model}\rightarrow\text{hypothesize}\rightarrow
\text{predict}\rightarrow\text{test}\rightarrow\text{update}.
$$

For hypotheses $H_i$ and evidence $E$, Bayesian updating is

$$
P(H_i\mid E)=\frac{P(E\mid H_i)P(H_i)}{\sum_jP(E\mid H_j)P(H_j)}.
$$

Numbers may be qualitative or approximate; the discipline is to expose priors, predictions, and disconfirming evidence. Choose the lowest-risk test that most separates plausible hypotheses before the harm deadline. Investigation remains subordinate to [SDRE-054](054-incident-command.md) objectives and [SDRE-056](../ROADMAP.md) mitigation.

### Critical invariants

- distinguish observed fact, derived measurement, hypothesis, decision, action, and result;
- start from user or protected-property deviation, then traverse mechanisms;
- preserve original queries, time ranges, units, filters, versions, and raw references;
- seek evidence that could disconfirm the favored hypothesis;
- compare like cohorts and account for deployments, traffic, topology, clocks, retries, caches, and sampling;
- one coordinated production intervention changes one interpretable factor where practical;
- every test has owner, prediction, risk bound, stop rule, and expected observation time;
- missing telemetry is an observation about the evidence system, not proof of health;
- security, privacy, safety, and destructive-state boundaries constrain investigation;
- stop debugging and mitigate or escalate when continuing harm outruns information value.

### Common failures

Common failures include solving the alert name, anchoring on the last incident, searching dashboards without a question, confusing temporal proximity with cause, comparing mismatched populations, trusting averages, ignoring retries and queues, running broad commands, changing multiple variables, sampling away the affected cohort, querying with inconsistent clocks, contaminating evidence, leaking sensitive context, duplicating experiments across responders, and continuing root-cause work while irreversible harm grows.

### Compact example

Checkout errors rise after a release. The initial prior favors the release, but errors occur only in a region that did not receive it. A region-by-version cohort table disconfirms simple release causation and raises a shared dependency hypothesis. One trace shows both old and new application versions timing out at the same payment endpoint. Traffic shift improves both cohorts. The release remains correlated in time but is no longer the leading causal explanation.

### Connections

[SDRE-053](053-operational-alert-triage.md) bounds impact and disposition; [SDRE-054](054-incident-command.md) coordinates investigators and mutations. [SDRE-056](../ROADMAP.md) chooses protection before root cause, while [SDRE-058](../ROADMAP.md) deepens evidence preservation and timeline construction.

## Governing Question

Production investigation occurs in an adversarial cognitive environment. Evidence is incomplete, systems continue changing, alerts compete for attention, users are harmed, and observers want confident answers. The cost of a wrong inference is not merely intellectual: responders may roll back a healthy release, overload a surviving region, destroy forensic state, expose sensitive data, or delay containment.

The investigator's job is not to produce the fastest plausible story. It is to reduce decision-relevant uncertainty. That means defining the deviation precisely, selecting a model at the right boundary, keeping several plausible hypotheses alive, deriving different predictions, and obtaining evidence whose result changes action. Sometimes the rational output is “cause remains unknown; this reversible mitigation is still justified.”

Pressure changes the process but does not abolish it. Tests must be smaller, communication more explicit, and stopping rules stricter. Incident command protects investigators from duplicate requests and coordinates interventions. Investigators protect command from confident but weak causal claims.

## Why This Matters

Google's SRE troubleshooting chapter explicitly presents troubleshooting as hypothetico-deductive iteration and warns against irrelevant symptoms, unsafe tests, improbable pet theories, prior-incident anchoring, and spurious correlation [1]. It also observes that generic method and system-specific knowledge are complementary: a rigorous loop without a correct system model is slow, while expertise without explicit testing can become intuition defended as fact.

Distributed systems make evidence perspectival. Client latency, server latency, dependency latency, queue residence, and retry-amplified work may all describe different intervals. Aggregate metrics obscure cohorts; logs omit dropped events; traces are sampled; clocks disagree; and dashboards can share one broken pipeline. Google's monitoring guidance distinguishes symptoms from causes and black-box from white-box observations [2]. Neither perspective is sufficient alone.

Current OpenTelemetry documentation distinguishes traces, metrics, logs, and baggage as different signal concepts [5]. Its context-propagation guidance also warns that incoming context can be forged and outgoing identifiers or baggage can expose sensitive information [6]. Therefore correlation identifiers are useful joins, not trusted causal or authorization claims.

## Prerequisites and Retrieval

Retrieve [SDRE-031](031-observability-versus-monitoring.md) through [SDRE-040](040-instrumenting-a-service-for-diagnosis.md) for signal semantics and instrumentation; [SDRE-047](047-failure-domains.md) and [SDRE-048](048-redundancy-and-diversity.md) for topology and common modes; and [SDRE-051](051-incident-severity-and-classification.md) through [SDRE-054](054-incident-command.md) for consequence, ownership, triage, and coordination. Recall conditional probability, Bayes' rule, queues, percentiles, sampling, causal graphs, and controlled experiments.

## Learning Objectives

After this module, you should be able to:

1. write a cause-neutral problem statement with scope, onset, and confidence;
2. construct a minimal system and failure model at the user-to-dependency boundary;
3. generate, rank, test, and retire competing hypotheses;
4. update beliefs with likelihood evidence without manufacturing false precision;
5. design low-risk discriminating probes and controlled interventions;
6. diagnose cohort, time, sampling, retry, cache, and queue distortions;
7. coordinate parallel investigators through an evidence ledger and command structure;
8. apply stopping rules when mitigation, escalation, or evidence protection outranks diagnosis.

## Core Exposition

### Begin with a cause-neutral problem statement

Write what deviates from which expectation: affected user operation or protected property, observed behavior, population and geography, start and current interval, comparison baseline, evidence sources, and uncertainty. “Database incident” names a presumed owner and cause. “Confirmed checkout requests in region A exceed the five-second latency objective since 14:03 UTC; region B and read-only operations appear normal; telemetry is complete through 14:07” is testable.

Update the statement as evidence changes, but retain prior revisions. A shrinking scope can be as diagnostic as a growing one. State negative evidence carefully: “no errors in sampled traces” means something different from “all requests succeeded.”

### Draw the smallest useful system model

Trace the protected operation across client, edge, service, queue, datastore, external dependency, and response. Mark data transformations, state ownership, retry boundaries, timeouts, concurrency controls, deployment versions, and telemetry points. Include the control plane when it can change the data plane.

The model should answer where the symptom could be introduced and where it could merely be observed. Begin coarse enough to guide partitioning. Add detail only when a hypothesis needs it. A complete architecture diagram built during an outage is usually a distraction.

### Establish the timeline and change surface

Use a common time basis and record clock source, skew uncertainty, and event provenance. Collect alert evaluation, first user impact, deployments, flags, schema changes, traffic shifts, certificate changes, capacity events, dependency notices, and investigator actions. Temporal order can exclude impossible causes, but proximity alone does not establish causation.

The change surface includes gradual and external changes: workload mix, data distribution, expiring credentials, autoscaling, compaction, cache turnover, quota, feature exposure, and dependency behavior. “No deploy” is not “no change.”

### Generate a hypothesis portfolio

Derive candidates from the system model and failure modes. Cover application, data, infrastructure, network, dependency, configuration, capacity, security, and observability paths as relevant. Phrase each so it could be false: “new release mishandles requests with empty locale” rather than “release issue.”

Rank hypotheses by prior plausibility, consequence if missed, test cost, and distinguishability. A low-probability catastrophic hypothesis may deserve an early safe check. Do not create an exhaustive list that consumes the response; keep a short active portfolio and a parked set.

### Derive predictions before querying

For each hypothesis, write predicted differences: affected versions, regions, operations, tenants, hosts, dependency calls, time windows, or state transitions. Also write a disconfirming result. Then choose observations that partition candidates.

Suppose $H_1$ predicts only new-version failures, $H_2$ predicts all versions in one region, and $H_3$ predicts write-only failures. A version-by-region-by-operation table provides more discrimination than another global error chart. Prediction-first work reduces dashboard tourism and post hoc storytelling.

### Update beliefs without false precision

Bayes' rule formalizes how evidence changes relative belief. Exact probabilities are rarely known during an incident, but likelihood direction remains useful. Evidence expected under every hypothesis has little discriminating value. Evidence far more likely under one hypothesis should move attention, subject to data quality.

Assume priors $P(H_D)=0.5$, $P(H_X)=0.3$, and $P(H_O)=0.2$ for deployment, dependency, and overload. If evidence “only the new canary fails” has likelihoods $0.9$, $0.2$, and $0.3$, unnormalized weights are $0.45$, $0.06$, and $0.06$. Normalizing by $0.57$ gives approximately $0.789$, $0.105$, and $0.105$. These are illustrative judgments, not measured causal probabilities.

Do not discard a hypothesis solely because one noisy test lowers it. Track evidence independence: five dashboards derived from one metric stream are one evidential lineage. Consider whether selection, instrumentation, or the incident itself changes likelihoods.

### Compare cohorts correctly

Useful cohort dimensions include version, region, availability zone, tenant, operation, request origin, data shard, hardware class, feature flag, and dependency route. Ensure numerator and denominator refer to the same population and interval. Compare exposure, not labels alone: a “control” region receiving different traffic is not a clean control.

Beware survivorship. Successful requests may be traced at a higher rate than failures, failed clients may never reach the server, and overloaded hosts may stop exporting. Percentiles aggregated across cohorts can reverse conclusions. Preserve counts and missingness alongside rates.

### Follow one request or state transition end to end

Aggregate symptoms locate scope; a concrete representative exemplar exposes mechanisms. Select an affected request or object without copying sensitive data broadly. Follow identifiers through boundaries, comparing client, service, dependency, and durable state. Validate identifier authenticity and collision assumptions.

OpenTelemetry context propagation can correlate signals across service boundaries, but current guidance warns about forged incoming context and disclosure through outgoing context or baggage [6]. Treat trace IDs as joins, not authorization or proof that events share a trustworthy actor.

### Understand queues, retries, and timeouts

A measured 500 ms dependency call can produce five-second user latency through queueing, retry backoffs, hedges, connection acquisition, and serial timeouts. Build a latency budget:

$$
T_{user}=T_{queue}+\sum_{k=1}^{m}(T_{attempt,k}+T_{backoff,k})+T_{local}.
$$

Check concurrency, arrival rate, service rate, queue depth and age, cancellation, retry ownership, and timeout ordering. Retries can turn partial slowness into overload. Falling throughput during saturation may make utilization metrics look deceptively lower.

### Choose safe probes before interventions

A passive probe queries existing evidence. An active probe generates controlled work. An intervention changes the system. Escalate risk in that order when time permits. Every active step states target, expected result under each hypothesis, blast radius, rate, data sensitivity, cleanup, stop condition, and observation deadline.

Use production experiments only when the expected information or protection justifies their risk and command authorizes them. Prefer one factor at a time. When factors cannot be isolated, document the coupled intervention and restrict the causal claim.

### Measure information value and action value

For hypotheses with distribution $p$, uncertainty can be summarized by entropy

$$
H(p)=-\sum_i p_i\log_2p_i.
$$

Expected information gain of test $Q$ is current entropy minus expected posterior entropy. The highest-information test is not always best: it may be slow, destructive, sensitive, or irrelevant to immediate action. Choose by decision value under harm and risk constraints.

A reversible traffic shift may both protect users and discriminate regional hypotheses. Conversely, a memory dump might contain high diagnostic value but unacceptable secrets. Command weighs information, mitigation, safety, and evidence preservation.

### Coordinate parallel investigation

Incident command assigns hypothesis or system-boundary cells, not “everyone investigate.” Each cell records question, owner, prediction, query or action, time range, result, interpretation, confidence change, and next step. Shared changes remain controlled by operations.

Converge at short checkpoints. Merge duplicate hypotheses, surface contradictions, and stop low-value branches. The evidence ledger prevents two teams from repeating a dangerous test and lets incoming responders distinguish what was observed from what was inferred.

### Defend against cognitive and social pressure

Anchoring favors the first explanation. Availability bias favors memorable past incidents. Confirmation bias selects supportive evidence. Authority bias overweights senior claims. Action bias changes the system merely to appear responsive. Outcome bias later judges a decision using facts unavailable at the time.

Countermeasures are structural: explicit alternatives, disconfirming predictions, independent query reproduction, confidence labels, predeclared stopping rules, and permission to challenge. Calm language matters: “evidence raises H1” is more accurate and less socially sticky than “we found the cause.”

### Stop investigation at the right time

Stop and mitigate when continuing harm, irreversibility, security exposure, or shrinking recovery options exceed the value of more evidence. Stop a branch when its prediction fails under reliable observation or its next test cannot change action. Escalate when authority, expertise, capacity, or evidence access is missing.

Do not force root cause during response. Record the best current causal model and unresolved alternatives. Deep reproduction, counterfactual testing, and systemic analysis can continue after stability with safer tools and preserved evidence.

### A bounded Bayesian update

The following executable model performs one transparent update. It requires mutually exclusive listed hypotheses and supplied likelihood judgments; it does not discover causes.

<!-- bijux-verify: {"id":"update-incident-hypotheses","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"deployment: 0.789\ndependency: 0.105\noverload: 0.105\n","stderr":""}} -->
```python
priors = {
    "deployment": 0.5,
    "dependency": 0.3,
    "overload": 0.2,
}
likelihood = {
    "deployment": 0.9,
    "dependency": 0.2,
    "overload": 0.3,
}

weights = {name: priors[name] * likelihood[name] for name in priors}
normalizer = sum(weights.values())
if normalizer <= 0:
    raise ValueError("evidence has zero probability under every hypothesis")

for name, weight in weights.items():
    print(f"{name}: {weight / normalizer:.3f}")
```

Observed behavior is limited to these inputs under the recorded interpreter. The rounded outputs sum to 0.999; the unrounded posterior sums to one. Real hypotheses may overlap, likelihoods may be unknown, and missing candidates can dominate.

## Definitions and Notation

Let $O$ be the observation set with provenance, $M$ the current system model, $\mathcal H=\{H_1,\ldots,H_n\}$ the active hypothesis set, and $E$ new evidence. Let $Q$ be a test with outcomes $e_q$, risk $R(Q)$, duration $T(Q)$, and action relevance $V(Q)$.

A **necessary condition** must hold for a hypothesis to be true; a **sufficient condition** guarantees the conclusion under stated assumptions. An **exemplar** is one selected case; it does not establish population frequency. A **negative result** disconfirms only what the test could observe with declared sensitivity.

Let $t_o$ be source observation time, $t_c$ collection time, and $t_q$ query time. Confusing them invents sequence. Let $S$ denote sample inclusion; observed rates estimate $P(Y\mid S)$, which need not equal population $P(Y)$.

## Mechanisms, Invariants, or Proof Structure

**Cause-neutrality invariant.** The problem statement remains valid if the leading hypothesis changes. If changing the suspected cause invalidates the statement, it encoded a conclusion.

**Hypothesis falsifiability.** Each active $H_i$ produces at least one prediction whose reliable failure lowers it. Unfalsifiable labels such as “distributed systems issue” do not guide tests.

**Bayesian normalization.** With mutually exclusive and exhaustive hypotheses and positive evidence probability, posterior weights sum to one. Missing hypotheses make the normalized portfolio conditionally complete, not globally complete.

**Evidence-lineage invariant.** Correlated views sharing one source do not count as independent confirmation. Record collection and transformation paths.

**Cohort comparability.** A contrast supports inference only to the extent exposure, selection, interval, and measurement are comparable. Differences identify hypotheses; they do not automatically identify causes.

**Intervention safety.** A production test needs bounded blast radius, authorized owner, expected observations, stop rule, cleanup, and conflict check. Absence of one converts investigation into uncontrolled change.

**One-factor principle.** Changing one interpretable factor improves attribution. It is a design preference, not always feasible; coupled changes require weaker conclusions.

**Stopping invariant.** Investigation cannot consume the entire harm or recovery deadline. Mitigation, escalation, and evidence preservation are valid outputs before diagnosis.

## Alternatives and Trade-Offs

**Top-down versus bottom-up.** User-to-dependency traversal anchors consequence; resource-to-user traversal can quickly identify a physical cliff. Use the direction that best partitions candidates, then reconcile both.

**Broad query versus exemplar trace.** Aggregates establish prevalence and cohorts; exemplars reveal sequence and mechanism. Neither alone supports both scope and causation.

**Passive observation versus active intervention.** Passive work has lower system risk but may leave ambiguity. Interventions can discriminate quickly while changing the evidence and system.

**Expert intuition versus explicit portfolio.** Expertise supplies strong priors and useful tests. Explicit alternatives expose bias and make reasoning transferable.

**Fast approximate query versus exact slow query.** Approximation supports urgent direction if error bounds and blind spots are known. Exactness that arrives after the decision deadline has little operational value.

**Central investigator versus parallel cells.** One investigator preserves coherence but limits throughput. Cells explore in parallel but require command, hypothesis ownership, and shared evidence.

**Rollback as test versus rollback as mitigation.** Improvement after rollback supports a release-related mechanism but can be confounded by cache, traffic, or dependency recovery. Protect users first; phrase causal evidence carefully.

**Live diagnosis versus deferred reproduction.** Live state may contain unique evidence, while production testing risks harm. Preserve enough evidence, stabilize, then reproduce under safer control.

## Failure Modes and Misconceptions

1. **“The alert tells us what broke.”** It reports one rule's interpretation of signals.
2. **“The latest deploy caused it.”** Temporal order is necessary but insufficient.
3. **“This resembles last month's incident.”** Similar symptoms can arise from different mechanisms.
4. **“Five dashboards confirm it.”** They may share one collector, query, or aggregation.
5. **“No logs means nothing happened.”** Sampling, buffering, overload, access, or collection may explain absence.
6. **“A trace is the whole population.”** It is one selected execution, possibly sampled.
7. **“Averages summarize latency.”** They hide tails, cohorts, and mixture changes.
8. **“Retry success means dependency health.”** Retries can mask and amplify failure.
9. **“One changed variable proves cause.”** Other state can change concurrently.
10. **“More instrumentation is risk-free.”** It consumes resources, changes timing, and can expose data.
11. **“Senior confidence is evidence.”** Claims still require provenance and predictions.
12. **“Parallel work always accelerates diagnosis.”** Duplicate queries and conflicting interventions can reduce information.
13. **“A failed test falsifies the hypothesis.”** Only if the test could reliably observe its prediction.
14. **“Root cause is required before mitigation.”** Ongoing harm can make that policy irrational.
15. **“Recovered service proves the diagnosis.”** Recovery may be coincidental, partial, or caused through another mechanism.

## Worked Examples

### Example 1

**Situation.** A page says `DatabaseSlow`, but only image-upload requests fail in one region.

**Reasoning.** Rewrite the problem as an operation-, region-, and time-bounded symptom. The database metric becomes evidence, not the title. A dependency map shows uploads uniquely call object storage before database commit; storage latency partitions the failure.

**Conclusion.** Cause-neutral framing prevents the alert name from collapsing the search space incorrectly.

### Example 2

**Situation.** Deployment, dependency, and overload hypotheses have priors 0.5, 0.3, and 0.2; canary-only failure likelihoods are 0.9, 0.2, and 0.3.

**Reasoning.** Weights are 0.45, 0.06, and 0.06; their sum is 0.57. Posteriors are approximately 0.789, 0.105, and 0.105. The evidence makes deployment investigation more valuable without proving it.

**Conclusion.** Explicit likelihood reasoning changes priorities while preserving uncertainty and missing-hypothesis risk.

### Example 3

**Situation.** Four hypotheses predict different failure partitions across version and region.

**Reasoning.** A global error chart is compatible with all four. A two-dimensional cohort query shows old and new versions fail only in region A, rejecting version-only predictions and raising regional dependency or capacity candidates. Counts show equal exposure.

**Conclusion.** A discriminating query is one whose outcomes separate hypotheses, not merely add detail.

### Example 4

**Situation.** Aggregate latency is high, but sampled traces show normal service execution.

**Reasoning.** Trace sampling excludes requests that time out before headers arrive. A client exemplar shows 4.2 seconds waiting for a connection before the traced server span begins. Pool queue age and acquisition time explain the missing interval.

**Conclusion.** Align measurement boundaries before treating apparently contradictory latency evidence as contradiction.

### Example 5

**Situation.** Dependency attempts average 300 ms, yet user latency is 2.1 seconds.

**Reasoning.** The path performs three 300 ms attempts with 200 ms and 400 ms backoffs, plus 500 ms queueing and 100 ms local work: $500+3(300)+200+400+100=2{,}100$ ms. Attempt latency alone omitted queue and policy time.

**Conclusion.** Reconstruct the whole latency budget, including retries, backoff, and queues.

### Example 6

**Situation.** Errors begin two minutes after release 7.4, so rollback is proposed.

**Reasoning.** The only failing region still runs 7.3, while healthy regions run both. A simultaneous route-policy change affects the failing region. Traffic diversion restores it; rollback remains available but does not match exposure.

**Conclusion.** Change correlation generates hypotheses; exposure and mechanism decide whether they survive.

### Example 7

**Situation.** Restarting a cache node makes errors disappear, and the team declares corrupt cache state.

**Reasoning.** Restart also sheds load, moves traffic, resets connections, and warms a different shard. The intervention changed several factors. Preserve the recovery observation but list competing mechanisms; later reproduce with targeted key inspection and controlled shard movement.

**Conclusion.** Successful treatment can mitigate without uniquely identifying cause.

### Example 8

**Situation.** Service logs show responses before clients report request start.

**Reasoning.** Hosts differ by 90 seconds and dashboards use collection time for one source. Ordering by wall time is invalid. Trace causal edges and monotonic local durations preserve partial order; clock skew becomes a recorded evidence limitation.

**Conclusion.** Timestamp precision does not imply cross-system temporal accuracy.

### Example 9

**Situation.** A trace-baggage field contains an account email and is forwarded to a third-party API.

**Reasoning.** Investigation stops broad propagation, activates security/privacy owners, restricts evidence, and correlates through an internal opaque identifier. Current OpenTelemetry guidance warns that baggage can reach unintended downstream resources and lacks built-in integrity guarantees [6].

**Conclusion.** Observability context is neither a safe secret store nor trusted identity evidence.

### Example 10

**Situation.** Three teams independently test the same database by restarting replicas, changing pool limits, and shifting traffic.

**Reasoning.** Results become uninterpretable and safety margin shrinks. Incident command pauses changes, assigns queue, storage, and traffic hypotheses, records baselines, and sequences reversible tests with predictions and stop rules.

**Conclusion.** Parallel investigation needs hypothesis ownership and serialized interacting interventions.

## Cross-Program Connections

- [SARCH-028](../../12-software-engineering-software-architecture/modules/028-operational-views.md) supplies runtime views used to bound the investigation model.
- [ALGE-092](../../16-algorithm-engineering/modules/092-benchmark-design-and-reproducibility.md) develops controlled measurement and reproducibility outside incident urgency.
- [OS-095](../../22-operating-systems/modules/095-kernel-observability-and-ebpf.md) owns kernel-level instrumentation and its evidence boundaries.
- [SYSENG-045](../../26-systems-engineering/modules/045-uncertainty-and-confidence.md) provides broader uncertainty and confidence reasoning.
- [API-097](../../28-api-and-service-engineering/modules/097-api-metrics-logs-and-traces.md) provides API-boundary telemetry semantics.

## References

1. Chris Jones, “Effective Troubleshooting,” in *Site Reliability Engineering: How Google Runs Production Systems*, O'Reilly Media, 2016. [Official online edition](https://sre.google/sre-book/effective-troubleshooting/). Accessed 2026-09-06.
2. Rob Ewaschuk, “Monitoring Distributed Systems,” in *Site Reliability Engineering: How Google Runs Production Systems*, O'Reilly Media, 2016. [Official online edition](https://sre.google/sre-book/monitoring-distributed-systems/). Accessed 2026-09-06.
3. Mike Ulrich, “Emergency Response,” in *Site Reliability Engineering: How Google Runs Production Systems*, O'Reilly Media, 2016. [Official online edition](https://sre.google/sre-book/emergency-response/). Accessed 2026-09-06.
4. Jennifer Mace et al., “Incident Response,” in *The Site Reliability Workbook*, O'Reilly Media, 2018. [Official online edition](https://sre.google/workbook/incident-response/). Accessed 2026-09-06.
5. OpenTelemetry Authors and Cloud Native Computing Foundation, “Signals,” current official documentation, modified March 10, 2026. [Official documentation](https://opentelemetry.io/docs/concepts/signals/). Accessed 2026-09-06.
6. OpenTelemetry Authors and Cloud Native Computing Foundation, “Context Propagation” and “Baggage,” current official documentation. [Context propagation](https://opentelemetry.io/docs/concepts/context-propagation/) and [baggage guidance](https://opentelemetry.io/docs/concepts/signals/baggage/). Accessed 2026-09-06.

Current source-specific claims were checked on 2026-09-06. Named tools illustrate current signal and propagation behavior; the durable method is cause-neutral framing, explicit hypotheses, discriminating evidence, bounded experimentation, uncertainty-aware updating, and command-coordinated action.

## Exercises

### Exercise 1

Distinguish problem statement, fact, derived measurement, hypothesis, prediction, probe, intervention, result, correlation, and causal conclusion.

### Exercise 2

Three mutually exclusive hypotheses have priors 0.4, 0.4, and 0.2. Evidence has likelihoods 0.1, 0.6, and 0.5. Compute the posterior distribution and state two reasons it may not represent real causal probability.

### Exercise 3

User latency is 3.4 seconds. Requests wait 700 ms for a connection and make two 800 ms dependency attempts separated by 300 ms backoff; local work is 200 ms. Account for the remaining time and design a measurement to locate it without assuming a cause.

### Exercise 4

A rollback, traffic shift, and cache restart occur together and service recovers. Evaluate the causal evidence and design safer follow-up tests that do not endanger recovered service.

### Exercise 5

An incident affects one regulated tenant, traces are sampled, clocks disagree, the leading expert insists it is a repeat incident, and data loss may become irreversible in four minutes. Design the investigation, mitigation boundary, evidence handling, command coordination, and stopping rule.

## Answers to the Exercises

### Answer 1

A problem statement describes the deviation without cause. A fact is a sourced observation; a derived measurement applies declared transformation. A hypothesis is a falsifiable explanation, and a prediction is expected evidence under it. A probe observes; an intervention changes the system. A result is what follows a test or action. Correlation is association. A causal conclusion additionally needs temporal possibility, mechanism, predictions, alternatives, and evidence appropriate to the claim. An intervention result can support causation but remains confounded if several factors changed.

### Answer 2

Weights are $0.4(0.1)=0.04$, $0.4(0.6)=0.24$, and $0.2(0.5)=0.10$, totaling $0.38$. Posteriors are approximately $0.1053$, $0.6316$, and $0.2632$. They are conditional on the listed hypotheses being mutually exclusive and exhaustive and on accurate priors and likelihoods. Real candidates may overlap or be omitted; likelihood judgments may be subjective, evidence may share lineage, and sampling or incident behavior may change observation probabilities.

### Answer 3

Known time is $700+2(800)+300+200=2{,}800$ ms, leaving 600 ms. Do not label it network time by subtraction alone. Instrument monotonic timestamps at client dispatch, connection queue entry/exit, each attempt boundary, serialization, network send/receive, server entry/exit, retry scheduler, and client completion for a bounded representative cohort. Reconcile boundary overhead and sampling; compare clocks only through causal spans or measured skew. Preserve end-to-end counts so timed-out requests are not excluded.

### Answer 4

Recovery establishes that the joint intervention preceded improvement, not which action caused it. It may also coincide with external recovery or load change. Preserve exact timing, scope, and observations; avoid undoing protection solely for diagnosis. In a safe environment, replay the failure state and vary rollback, traffic, and cache separately. In production only if risk permits, compare unaffected cohorts or future canaries, inspect version exposure, move a tiny traffic fraction with stop rules, and validate cache state without restart. Phrase the live conclusion as “recovery followed the combined intervention; causal contribution unresolved.”

### Answer 5

State the tenant-specific protected outcome, four-minute irreversibility deadline, source freshness, sampling, and clock uncertainty. Activate the data-loss hard override and incident command; freeze or isolate the destructive path through an authorized reversible control before the deadline. Give the expert's repeat hypothesis a prediction but maintain alternatives from the system model. Preserve restricted tenant evidence in the authorized security/privacy or data cell, using opaque identifiers in the common ledger. Obtain an unsampled bounded state check or durable-record comparison, record source times and causal ordering instead of forcing wall-clock order, and assign hypothesis cells while serializing mutations through operations. Stop investigation early enough to execute protection; escalate if access or authority is missing. Resume deeper causal work after durable state and user exposure are controlled.
