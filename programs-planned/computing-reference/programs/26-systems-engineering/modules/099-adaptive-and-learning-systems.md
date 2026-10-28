---
module_id: SYSENG-099
program: Systems Engineering
level: 2
module_number: 99
title: Adaptive and Learning Systems
status: complete
last_verified: 2026-09-01
---

# Adaptive and Learning Systems

## One-Page Review

### Governing question

How can engineers authorize, constrain, observe, validate, and reverse systems whose behavior changes through learning, feedback, configuration, policy, users, organizations, or environment after initial verification?

### Essential definitions

- An **adaptive system** changes behavior, structure, parameters, allocation, or policy in response to observations, experience, goals, or environment.
- A **learning system** uses data or interaction to update an internal model, policy, representation, or decision rule; learning may occur during development, deployment, or both.
- **online adaptation** changes behavior using operational observations while the system is deployed; **offline adaptation** produces a new candidate outside the serving path before controlled release.
- A **policy** maps observed state or belief to action; in machine learning, the word does not imply legal or organizational policy.
- **distribution shift** is a change in the joint or conditional distributions relevant to inputs, labels, outcomes, participants, or environment.
- **concept drift** is change in the relationship the system is intended to model, such as the mapping from observations to outcomes.
- A **feedback loop** exists when system outputs affect future inputs, labels, behavior, exposure, incentives, or measurements.
- A **change envelope** specifies which parameters, behaviors, data, rates, populations, and operating conditions may change without renewed authorization.
- A **runtime assurance boundary** separates an adaptive or complex function from an independently justified monitor, constraint, fallback, or recovery path.
- **rollback** restores a known eligible configuration and reconciles state and consequences; it is more than redeploying old code.

### Central model, mechanism, or theorem

Let system state be $x_t$, action $u_t$, environment $e_t$, observations $z_t$, and adaptive parameters or policy state $\theta_t$:

$$
x_{t+1}=F_{\theta_t}(x_t,u_t,e_t),\qquad
\theta_{t+1}=A(\theta_t,z_t,g_t),
$$

where $g_t$ represents objectives and constraints used by the adaptation mechanism. Safe authorization cannot depend only on improved objective value. For protected constraints $C_j$, an update is eligible only under a bounded gate such as

$$
eligible(\theta_{t+1})\Rightarrow envelope\land evidence\land \bigwedge_j C_j\land monitor\land rollback\land authority.
$$

The implication is necessary, not sufficient. Models, data, monitors, constraints, and rollback can all be incomplete or wrong.

### Critical invariants

- Identify everything that can adapt: models, thresholds, rules, configurations, teams, users, markets, suppliers, and operating procedures.
- Bound objectives, protected constraints, change dimensions, rate, data, authority, environment, population, and cumulative movement.
- Separate exploration, candidate generation, evaluation, authorization, deployment, observation, and rollback.
- Preserve immutable identity and provenance for code, model, data, features, policy, parameters, evaluation, decision, and deployment.
- Evaluate outcomes and distributions, not only training loss or aggregate predictive performance.
- Analyze feedback, strategic response, selection, delayed labels, missing counterfactuals, and measurement changed by the system itself.
- Use independent runtime constraints, containment, graceful degradation, stop, and fallback where consequence demands them.
- Test boundary, shift, misuse, adversarial, degraded, recovery, interaction, and cumulative-update scenarios.
- Make adaptation state, intent, uncertainty, active version, limits, and action effects observable to responsible people and systems.
- Protect affected-person notice, review, appeal, correction, and remedy where decisions create material effects.
- Treat rollback as a planned state transition with compatibility, data reconciliation, and downstream consequence handling.
- Reauthorize after change outside the envelope, invalidated assumptions, monitor failure, unacceptable impact, or governance change.

### Common failures

Common failures include calling any configuration change learning; optimizing a proxy without protected constraints; evaluating only static held-out data; treating drift as input distance alone; training on decisions created by the prior model; accepting delayed or selective labels as ground truth; allowing silent vendor updates; promoting a candidate on average improvement; monitoring a metric the model directly influences; assuming a kill switch is reachable; rolling back code without state or remedy; leaving exploration active in high-consequence contexts; combining interacting learners without system analysis; and claiming continuous learning while operating an undocumented sequence of manual changes.

### Compact example

A synthetic candidate-update ledger checks improvement, step bound, subgroup floor, independent monitor, rollback readiness, and authority. Five of six conditions pass, but rollback readiness is false, so promotion is rejected. This demonstrates declared gate logic only; it does not validate the data, objective, subgroup selection, monitor independence, actual rollback, or safety of the candidate.

### Connections

This module builds on requirements, architecture, control, risk, safety, verification, validation, configuration, operations, resilience, emergence, human factors, organizations, and normative assurance. It prepares whole-system review and connects to online services, platform release control, data pipelines, distributed feedback, cybersecurity, and machine-learning operations.

## Governing Question

What control structure allows a system to improve or adapt without silently moving outside the conditions, values, evidence, authority, and recovery mechanisms that justified its use?

Adaptation can be valuable when environments change, faults occur, workloads move, users learn, or static rules cannot cover the problem. It also changes the object of assurance. A system verified at release may become a family of configurations connected by update rules, data pipelines, feedback, and human decisions. Engineering must assure both configurations and transitions.

## Why This Matters

Many systems adapt without a machine-learning model. Autoscalers change resource allocation; routing protocols learn paths; operators revise thresholds; users change behavior around controls; organizations change staffing and procedure; suppliers update managed services. Machine learning adds data-dependent behavior and statistical uncertainty, but the systems problem is broader: state changes after evidence was collected.

Learning systems can create endogenous data. A recommender changes exposure, a fraud model changes adversary behavior, a pricing agent changes demand, and a clinical alert changes which cases receive attention. Later observations are therefore not neutral samples of the world before deployment. Without causal and governance discipline, retraining can reinforce its own prior decisions.

Current guidance illustrates bounded change control. FDA's 2025 final guidance for predetermined change control plans for AI-enabled device software functions describes planned modifications, development and validation methods, and impact assessment within its regulated scope. NIST AI RMF and its generative-AI profile organize lifecycle risk work but are voluntary frameworks. ISO/IEC 42001 specifies an AI management system. These sources do not universally authorize online learning; applicability, domain regulation, and consequence determine what may adapt.

## Prerequisites and Retrieval

Before authorizing adaptation, retrieve:

1. stakeholder outcomes, protected rights and constraints, hazards, threats, unacceptable behaviors, service goals, ethical limits, and acceptance authority;
2. system boundary and adaptive elements: software, models, policies, thresholds, rules, features, data, infrastructure, users, operators, suppliers, organizations, and external agents;
3. baseline identity and evidence: code, model, parameters, data, features, dependencies, configuration, environment, population, evaluation, approvals, known limits, and operating history;
4. adaptation objective, loss or reward, constraints, optimization method, search space, update rate, stopping rule, exploration, randomization, and cumulative-change limits;
5. data-generating process: provenance, sampling, exposure, labels, delay, missingness, correction, consent or authority, retention, leakage, poisoning, and system-created feedback;
6. change envelope: allowed parameters, behaviors, populations, purposes, data sources, environments, magnitude, cadence, duration, and prohibited changes;
7. evaluation design: reference and shadow modes, offline tests, counterfactual limits, subgroup analysis, uncertainty, stress, adversarial testing, causal checks, and independent review;
8. deployment control: candidate registry, approvals, staged exposure, isolation, canary or cohort policy, holdout where ethical, observability, stop, rollback, and re-entry;
9. runtime assurance: independent constraints, monitor coverage, latency, false positives and negatives, failure behavior, authority, safe state, and fallback capability;
10. human and organizational control: operator process models, workload, override, escalation, incident command, supplier notification, affected-person contestability, and remediation;
11. operational observations: outcome distributions, drift, calibration, errors, near misses, overrides, appeals, disparate impact, resource use, attacks, and delayed consequences;
12. change and retirement processes for invalidated evidence, new law, new purpose, model or data obsolescence, unsupported dependencies, accumulated technical debt, and irreversible effects.

Construct an **adaptation trace**. Select one proposed update and trace trigger, source data, transformation, objective, candidate identity, evaluation, protected constraints, approving authority, deployment population, runtime observation, stop condition, rollback, downstream reconciliation, affected-person remedy, and evidence renewal.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish adaptation, learning, configuration, optimization, evolution, and ordinary nondeterminism;
2. model coupled plant, policy, observation, objective, and update dynamics;
3. define a change envelope and protected constraints for adaptive behavior;
4. analyze distribution shift, concept drift, feedback, strategic response, and selective labels;
5. design candidate evaluation, staged authorization, runtime assurance, stop, rollback, and re-entry;
6. maintain identity, provenance, lineage, and evidence across repeated updates;
7. evaluate interacting learners, human adaptation, and organizational changes;
8. design monitoring tied to causal mechanisms and actionable thresholds;
9. preserve rights, human authority, contestability, and remedy during adaptation;
10. state bounded assurance without claiming that historical performance proves future safety.

## Core Exposition

**Inventory every adaptation path.** List automatic and manual parameter updates, model replacement, feature changes, prompt and retrieval changes, configuration, autoscaling, routing, rules, supplier releases, operator workarounds, and user response. A system advertised as frozen may still adapt through data, policy, or dependency changes. Conversely, a scheduled retrain is not online learning if promotion remains a separately authorized release.

**Define the adaptation objective.** State what is optimized and why it relates to stakeholder value. Identify proxies, weights, horizons, discounting, and constraints. An objective that rewards clicks, throughput, or short-term prediction can damage safety, fairness, long-term utility, or recovery. Preserve noncompensable constraints outside a weighted score.

**Bound the change envelope.** Specify what may change, by how much, how often, from which data, for which population and purpose, under which environment. Limit cumulative movement as well as each small step; many individually acceptable changes can leave the validated region. Treat an envelope as an authorization boundary, not evidence that every interior point is safe.

**Separate learning from deployment.** Candidate generation can run frequently while promotion remains controlled. Use immutable candidate identity, reproducible pipelines, independent evaluation, protected tests, approval, staged exposure, and rollback. High-consequence domains may require offline learning only or predetermined categories of modification. Do not let infrastructure convenience decide authority.

**Model the observation process.** Sensors, labels, outcomes, and user reports are delayed, selective, noisy, and affected by prior actions. A fraud model observes investigated cases, not all fraud; a medical system observes outcomes influenced by treatment; a recommender observes exposed items. Record missing counterfactuals and avoid treating operational labels as unbiased truth.

**Analyze distribution shift precisely.** Input drift, label prevalence, conditional relationship, population, measurement process, policy, and environment can shift differently. Distance in feature space may not predict outcome harm, while a small input change can cross a decision threshold. Tie monitors to causal hypotheses and decision consequences rather than one generic drift score.

**Study feedback and strategic behavior.** Outputs alter who participates, what is recorded, and how actors respond. Beneficial adaptation can produce Goodhart effects; capable adversaries probe and poison the learner. Model short and long loops, delays, incentives, spillovers, and multi-agent response. Evaluate the combined system, not a frozen model in isolation.

**Control exploration.** Exploration collects information by choosing uncertain actions. Bound which actions, people, contexts, and consequences may be exposed; use prior evidence, ethical and legal authority, monitoring, and stop conditions. Some actions are unacceptable regardless of expected reward. Offline simulation does not automatically justify real-world exploration.

**Evaluate candidates on multiple axes.** Compare outcome quality, calibration, subgroup and intersectional effects, safety, security, privacy, robustness, latency, resource cost, human workload, explanation, accessibility, and recovery. Include failures, outliers, missing data, adversarial inputs, and shift. Predefine decision rules and retain unexpected regressions instead of tuning until one dashboard turns green.

**Use temporal and external validation.** Random splits often leak time, entity, or environment. Hold out future periods, sites, devices, institutions, or populations as the claim requires. Preserve a locked evaluation set where possible, but recognize repeated use can overfit organizational decisions to the benchmark. Refresh with governed provenance and keep comparability.

**Stage exposure deliberately.** Shadow mode observes without acting but cannot capture all behavioral feedback. Canaries expose a bounded cohort but may still harm or contaminate shared state. A/B tests need legitimate randomization, power, guardrails, interference analysis, and remedy. Progressive delivery is an evidence strategy only when cohorts, metrics, thresholds, and rollback are justified.

**Build runtime assurance.** An independent monitor or safety filter can constrain adaptive action, detect envelope exit, and transfer control to a simpler fallback. Independence is a claim requiring separate failure, data, and authority analysis. The monitor must act within the hazard time scale and fail predictably. A guard that shares the same corrupted sensor or model may be common cause.

**Design fallback and graceful degradation.** A fallback must be available, compatible, understandable, adequately capable, and practiced. It may serve fewer users or functions under explicit priority. Manual fallback needs workload, skill retention, state reconstruction, and timing evidence. Safe stop can itself create harm for essential services, so define controlled degradation and recovery.

**Make rollback a stateful operation.** Record compatibility of schemas, features, caches, embeddings, policies, and dependent services. An older model may not understand new features; decisions already made may require correction or remedy. Test rollback during partial deployment and after data migration. Define forward repair when rollback cannot undo the consequence.

**Maintain full lineage.** Link every output and decision as required to system, model, code, configuration, data snapshot, feature logic, objective, policy, supplier, and runtime context. Protect privacy and retention while preserving sufficient evidence. A model version string without data and feature provenance is weak identity.

**Monitor outcomes, not only model health.** Track protected constraints, affected-person outcomes, calibration, failure severity, disparity, resource impact, complaints, appeals, overrides, containment, and recovery. Model metrics can remain stable while the surrounding process harms people. Define thresholds, owners, authority, and actions before deployment.

**Handle delayed outcomes.** Some harms or benefits appear after weeks or years. Maintain cohorts and evidence long enough under legitimate retention, use leading indicators, and avoid promoting repeatedly before prior changes mature. When delay exceeds safe learning cadence, narrow the envelope or use stronger prior evidence and independent constraints.

**Govern human and organizational adaptation.** Operators change strategies around automation; teams tune procedures; leaders change targets; users game or abandon the system. Observe work as done and treat adaptations as causal evidence. Do not criminalize every workaround or let invisible manual patches become the true control system. Incorporate safe learning into supported design.

**Manage interacting learners.** Pricing agents, recommenders, autoscalers, markets, and human organizations can create oscillation, collusion, cascade, or resource depletion even when each optimizes locally. Simulate and monitor joint dynamics, constrain shared resources and forbidden outcomes, vary update cadences, and retain global stop authority.

**Retire adaptation responsibly.** Stop learning when evidence, monitoring, data authority, support, or rollback becomes inadequate. Freeze a known configuration only if it remains eligible. Notify affected roles, preserve required evidence, remove data and access according to policy, transition users, and monitor delayed consequences. Retirement is part of the lifecycle case.

The following fixture checks declared candidate-update conditions. It cannot validate a real adaptive system.

<!-- bijux-verify: {"id":"adaptive-update-gate","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"candidate=model-42\nrequired_conditions=6\npassed_conditions=5\nfailed_conditions=1\nblocked=rollback_ready\npromotion_gate=reject_candidate\nevidence=declared_boolean_fixture_only\n","stderr":""}} -->
```python
candidate = "model-42"
conditions = {
    "objective_improves": True,
    "step_within_envelope": True,
    "subgroup_floor_preserved": True,
    "independent_monitor_ready": True,
    "rollback_ready": False,
    "authority_recorded": True,
}
blocked = [name for name, passed in conditions.items() if not passed]
print(f"candidate={candidate}")
print(f"required_conditions={len(conditions)}")
print(f"passed_conditions={sum(conditions.values())}")
print(f"failed_conditions={len(blocked)}")
print(f"blocked={','.join(blocked)}")
print("promotion_gate=reject_candidate")
print("evidence=declared_boolean_fixture_only")
```

## Definitions and Notation

Let $x_t\in X$ be system state, $u_t\in U$ action, $e_t\in E$ environment, $z_t\in Z$ observation, $\theta_t\in\Theta$ adaptive policy state, and $g_t$ objective and constraint state. $F_\theta$ describes system transition and $A$ the update mechanism. Neither must be fully known.

Define a change envelope

$$
\Gamma=\langle parameters,behaviors,data,populations,purposes,environments,step,cumulative,rate\rangle.
$$

Define evidence envelope

$$
\Omega_A=\langle versions,data,populations,scenarios,environments,interactions,duration,assumptions\rangle.
$$

An update inside $\Gamma$ is authorized for consideration, not proved safe. Evidence from $\Omega_A$ does not automatically cover a new distribution, interacting agent, objective, supplier version, or cumulative path.

## Mechanisms, Invariants, or Proof Structure

1. **Frame outcomes and constraints.** Identify stakeholders, purpose, harms, rights, hazards, threats, service goals, and authority.
2. **Inventory adaptation.** Include automated, manual, human, organizational, supplier, and environmental change paths.
3. **Specify dynamics and objective.** Model state, observation, update, feedback, delay, proxy, constraints, and interaction.
4. **Bound the envelope.** Limit parameters, behavior, data, population, purpose, environment, rate, and cumulative movement.
5. **Control data and lineage.** Preserve authority, provenance, sampling, labels, transformations, identity, privacy, and reproducibility.
6. **Evaluate candidates.** Use representative, temporal, subgroup, stress, adversarial, causal, human, and recovery evidence.
7. **Authorize and stage.** Separate candidate generation from promotion; define cohorts, gates, independent review, and stop authority.
8. **Assure runtime behavior.** Monitor protected outcomes, constrain actions, contain failure, degrade safely, and preserve fallback.
9. **Rollback, reconcile, and remedy.** Restore compatible state, correct downstream effects, support appeal, and control re-entry.
10. **Learn and reauthorize.** Investigate outcomes, update models, renew evidence, narrow or expand envelopes, and retire when needed.

Core invariants are: no adaptive objective overrides a protected constraint; no update lacks immutable identity and provenance; no operational label is assumed unbiased without analysis; no candidate promotes on aggregate improvement alone; no monitor lacks action authority; no fallback is credited without feasibility evidence; no rollback ignores state and consequence; no change outside the envelope inherits approval; and no historical performance establishes future behavior outside its evidence envelope.

There is no proof that finite evaluation anticipates every future environment or strategic response. The goal is controlled adaptation: bounded authority, independent constraints, observable transitions, representative evidence, effective recovery, and explicit residual uncertainty.

## Alternatives and Trade-Offs

**Frozen model versus online learning.** A frozen model simplifies identity and approval but can become stale. Online learning responds quickly but couples operation to data quality, feedback, security, and update control. Scheduled offline retraining is often the intermediate design.

**Global model versus local adaptation.** One model improves consistency and pooled evidence; local models fit context but fragment assurance and may have small samples. Hierarchical or federated approaches add coordination, privacy, and aggregation assumptions.

**Performance versus interpretability.** More complex models may improve some metrics while complicating diagnosis, explanation, verification, and recovery. Interpretability is audience- and decision-specific; simple models can still be unfair or unsafe. Choose against the whole assurance need.

**Exploration versus protection.** Exploration reduces uncertainty and can improve long-term outcomes, but exposes participants to uncertain actions. Use simulation, historical evaluation, constrained exploration, informed authority, monitoring, and hard prohibitions according to consequence.

**Fast update versus mature evidence.** Rapid promotion responds to drift but delayed outcomes may not yet reveal harm. Slow updates improve observation but prolong known deficiencies. Use severity-based gates, leading indicators, staged exposure, and constrained emergency corrections.

**Central update authority versus federated autonomy.** Central control supports consistency and global constraints but creates bottlenecks and common cause. Federated adaptation fits local context but requires shared invariants, identity, evidence exchange, dispute resolution, and global containment.

## Failure Modes and Misconceptions

- **“Adaptive means intelligent.”** A thermostat adapts; sophistication does not imply good objectives or outcomes.
- **“The model learns from reality.”** It learns from a measured, selected, delayed, and often policy-shaped sample.
- **“Drift is one number.”** Input, label, concept, population, process, and outcome shifts differ.
- **“Better loss means better system.”** Proxies can improve while protected stakeholder outcomes worsen.
- **“Small updates are safe.”** Cumulative movement and interaction can exit the validated region.
- **“Shadow mode proves deployment.”** It omits action-created feedback, workload, incentives, and some failures.
- **“A/B testing is ethically neutral.”** Randomization, exposure, harm, interference, consent or authority, and remedy matter.
- **“A monitor guarantees safety.”** Coverage, independence, latency, shared sensors, failure, and authority limit it.
- **“A kill switch is enough.”** Detection, access, timing, safe state, downstream effects, and re-entry need design.
- **“Rollback restores the past.”** Data, state, schemas, users, and prior decisions may have changed irreversibly.
- **“Human override closes the risk.”** People need information, time, skill, authority, and feasible alternatives.
- **“The vendor handles drift.”** Integrated purpose, population, feedback, and remedy remain deployment-specific.
- **“Continuous learning requires automatic promotion.”** Learning and release authority can be separate.
- **“Stable averages mean no harm.”** tails, subgroups, rare hazards, and delayed effects can move independently.
- **“Retiring the model ends impact.”** Stored decisions, downstream copies, learned behavior, and affected people persist.

## Worked Examples

### Example 1

**Situation:** A fraud model retrains on investigated cases. **Reasoning:** Prior scores determine investigation, so labels are selectively observed and adversaries adapt. Use exploration only where legitimate, independent audits, delayed outcomes, and causal caution. **Conclusion:** Operational labels are produced by the control policy.

### Example 2

**Situation:** An autoscaler learns demand patterns but all services optimize local latency. **Reasoning:** Simultaneous scaling exhausts a shared quota and destabilizes the platform. Enforce global resource constraints and coordinate update cadence. **Conclusion:** Locally beneficial learners can create system-level oscillation.

### Example 3

**Situation:** A clinical model improves aggregate sensitivity after retraining. **Reasoning:** Specific sites and demographic groups regress, and rollback was not tested against the new feature schema. Reject promotion until protected floors and recovery are evidenced. **Conclusion:** Average improvement cannot compensate for subgroup or rollback failure.

### Example 4

**Situation:** A recommender's click metric rises. **Reasoning:** Exposure changes future data, low-click content loses observation, and session length displaces user well-being. Use diverse outcomes, controlled holdouts where ethical, and feedback analysis. **Conclusion:** The learner changes the world it measures.

### Example 5

**Situation:** A vendor changes a hosted model without changing the endpoint. **Reasoning:** Output behavior, safety filters, latency, data handling, and evaluation coverage change. Require version notice, staged comparison, stop authority, and fallback. **Conclusion:** Stable APIs do not imply stable adaptive behavior.

### Example 6

**Situation:** A robot planner explores a shorter route near people. **Reasoning:** Expected time improves, but exploration can enter an unvalidated physical region. Constrain action with independent safety bounds and test in simulation and controlled environments first. **Conclusion:** Uncertainty reduction does not justify prohibited exposure.

### Example 7

**Situation:** Operators repeatedly override a false alarm and the learner reduces its weight. **Reasoning:** Overrides may reflect expertise, fatigue, missing context, or production pressure; a rare true hazard may share the signal. Investigate mechanism before using override as a label. **Conclusion:** Human adaptation is evidence, not clean ground truth.

### Example 8

**Situation:** Daily candidates each move a threshold by less than 1%. **Reasoning:** After months, the threshold and served population differ materially from the baseline. Track cumulative distance and require periodic rebaselining and renewed validation. **Conclusion:** Step bounds do not control cumulative drift.

### Example 9

**Situation:** Rollback redeploys yesterday's model but predictions remain inconsistent. **Reasoning:** Feature computation and cached embeddings changed, and prior adverse decisions remain downstream. Version the full pipeline, invalidate caches, reconcile decisions, and support remedy. **Conclusion:** Model rollback is not system rollback.

### Example 10

**Situation:** A pricing agent and consumers learn each other's behavior. **Reasoning:** Prices oscillate and correlated agents may create unfair or unlawful outcomes without explicit collusion code. Bound actions, monitor market and stakeholder effects, and retain external governance. **Conclusion:** Multi-agent adaptation requires whole-system analysis.

## Cross-Program Connections

- **Platform Engineering:** model registries, feature systems, progressive delivery, policy gates, telemetry, rollback, and incident response provide adaptation infrastructure.
- **API and Service Engineering:** version identity, behavioral contracts, idempotency, asynchronous jobs, rate limits, and vendor changes shape adaptive control.
- **Data Engineering:** provenance, labels, leakage, time, quality, feedback, retention, feature reuse, and correction determine learning evidence.
- **Distributed Systems:** partial failure, delayed feedback, clocks, coordination, replication, and shared resources affect update and rollback semantics.
- **Security Engineering:** poisoning, evasion, model theft, prompt injection, supply chain, abuse, and monitor compromise create adaptive adversaries.
- **Human Factors:** reliance, override, skill decay, workload, process models, and recovery mediate joint adaptation.
- **Organizational Engineering:** objectives, authority, incentives, suppliers, incident learning, and resource allocation control what adapts.
- **Policy and Ethics:** purpose, protected rights, impact assessment, notice, contestability, change authorization, and remedy constrain adaptation.
- **Control Theory:** stability, observability, controllability, delay, robustness, saturation, and runtime constraints provide analytical foundations.
- **Economics:** strategic behavior, feedback, market response, exploration cost, externalities, and distribution explain system-level effects.

## References

1. National Institute of Standards and Technology, [Artificial Intelligence Risk Management Framework 1.0](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10), NIST AI 100-1, 2023.
2. National Institute of Standards and Technology, [Generative Artificial Intelligence Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence), NIST AI 600-1, 2024.
3. U.S. Food and Drug Administration, [Predetermined Change Control Plan Guidance for AI-Enabled Device Software Functions](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/marketing-submission-recommendations-predetermined-change-control-plan-artificial-intelligence), final guidance, 2025.
4. ISO, [ISO/IEC 42001:2023 Artificial intelligence management system](https://www.iso.org/standard/42001), 2023.
5. Richard S. Sutton and Andrew G. Barto, [Reinforcement Learning: An Introduction, Second Edition](http://incompleteideas.net/book/the-book-2nd.html), MIT Press, 2018.
6. D. Sculley et al., [Hidden Technical Debt in Machine Learning Systems](https://papers.nips.cc/paper_files/paper/2015/hash/86df7dcfd896fcaf2674f757a2463eba-Abstract.html), Advances in Neural Information Processing Systems 28, 2015.
7. Dario Amodei et al., [Concrete Problems in AI Safety](https://arxiv.org/abs/1606.06565), 2016.
8. Nancy G. Leveson and John P. Thomas, [STPA Handbook](https://psas.scripts.mit.edu/home/get_file.php?name=STPA_handbook.pdf), MIT Partnership for Systems Approaches to Safety and Security, 2018.

## Exercises

### Exercise 1

Distinguish a frozen model, scheduled offline retraining, online learning, adaptive control, and human or organizational adaptation in one service.

### Exercise 2

A candidate gate contains eight required conditions and six pass. Compute the pass rate, then explain why the result cannot authorize deployment when rollback and subgroup evidence are missing.

### Exercise 3

Construct an adaptation trace for an online fraud-detection system with delayed and selective labels.

### Exercise 4

Design runtime assurance, graceful degradation, rollback, reconciliation, and re-entry for an adaptive traffic-routing service.

### Exercise 5

Evaluate two interacting learning pricing agents from objectives, feedback, market impact, law, ethics, monitoring, and stop authority.

## Answers to the Exercises

### Answer 1

A frozen model keeps parameters fixed between explicit releases, though its inputs, users, dependencies, and environment can still change. Scheduled offline retraining uses new data to create a candidate outside the serving path; evaluation and promotion remain controlled release decisions. Online learning updates parameters or policy from operational data while deployed, coupling assurance directly to data and runtime update controls.

Adaptive control changes action according to observed state and may use a fixed designed law rather than learning from accumulated experience. Autoscaling and feedback control are adaptive even without machine learning. Human adaptation includes new strategies, overrides, and workarounds; organizational adaptation includes changed targets, staffing, policy, and approval paths.

Inventory each path separately with objective, authority, change envelope, evidence, observation, rollback, and interaction. Calling the whole service “static” because its model is frozen misses environment, configuration, and human change. Calling all changes “AI learning” obscures distinct causal and governance mechanisms.

### Answer 2

The descriptive pass rate is

$$
\frac{6}{8}\times100\%=75\%.
$$

Promotion still fails. If subgroup evidence is missing, a protected population may regress despite aggregate benefit. If rollback readiness is missing, detection of harm may not lead to timely containment or restoration. These are noncompensable conditions, not points in an average.

Review every passing field as evidence, not a boolean asserted by the candidate owner. Validate objective relevance, change envelope, data provenance, evaluation independence, monitor coverage, authority, and operational compatibility. Add the missing evidence and exercise rollback including state and downstream consequences. Then repeat the whole gate; 100% metadata completeness is still only eligibility for an authorized decision, not proof of future safety.

### Answer 3

Define losses, protected customer rights, fraud and service objectives, error costs, action authority, and prohibited outcomes. Trace transaction and account observations, prior model score, investigation selection, challenge or chargeback, delayed confirmed outcome, missing labels, and adversary response. Separate event time, observation time, and label maturity.

The update objective must address fraud loss, false blocks, unequal impact, appeal, workload, and security without averaging away protected floors. Use propensity or experimental methods only where assumptions and ethics support them; preserve a random or policy-independent audit sample if lawful and feasible. Treat investigator decisions and overrides as noisy, policy-shaped observations.

Create immutable data, feature, code, model, objective, evaluation, and approval identity. Evaluate temporal and population holdouts, emerging attacks, calibration, subgroup and merchant effects, adversarial cases, queue capacity, appeal outcomes, and delayed labels. Stage exposure with limits, monitor system outcomes and data-generation changes, and define stop, rollback, reconciliation, customer correction, and remedy. Reauthorize when attack, purpose, population, data, law, or supplier changes outside the envelope.

### Answer 4

Protected constraints include prohibited roads or vehicle classes, emergency access, capacity, safety, privacy, fairness, and bounded travel disruption. The adaptive planner can optimize routes inside an authorized graph and rate envelope. An independent constraint service checks closures, legal restrictions, capacity, and hazard zones using separately validated inputs and fails to conservative routes when necessary.

Monitor constraint violations, congestion propagation, travel-time tails, neighborhood burden, emergency response, sensor freshness, route oscillation, user overrides, and shared dependency health. Define time-scale-appropriate stop authority and an operations view of active policy, change, reason, confidence, and predicted effect. Graceful degradation may freeze updates, reduce optimization scope, or return to signed static routes.

Rollback restores planner, map, rules, caches, and routing state consistently; it also stops issuing old recommendations and reconciles vehicles already committed. Exercise partial rollout, stale maps, monitor failure, network partition, and mass fallback. Re-entry requires causal diagnosis, repaired evidence, compatible state, staged exposure, and authorized acceptance. A static fallback that creates citywide gridlock is not automatically safe.

### Answer 5

Map each agent's observations, objectives, actions, update cadence, inventory, cost, competitor signals, and constraints plus consumer and competitor response. Local revenue or inventory optimization can create oscillation, tacit coordination, discriminatory effects, shortage, or manipulation. Shared vendor data and identical algorithms can correlate behavior even without direct communication.

Analyze applicable competition, consumer, pricing, privacy, and sector rules with qualified review. Ethical analysis covers essential access, power, transparency, distribution, vulnerable populations, and remedy. Establish hard prohibited practices and action/rate bounds outside the reward, plus audit identity, explanation, appeal where relevant, and manual fallback.

Use agent-based and economic simulation as exploratory evidence, historical and synthetic adversarial scenarios, sensitivity to objectives and cadence, controlled staged deployment where lawful, and independent market monitoring. Watch unexplained price correlation, oscillation, inventory margin, disparity, complaints, strategic response, and rollback failure. Give a competent authority the ability to freeze learning or pricing and restore a lawful baseline. Simulation cannot prove future market behavior or legality.
