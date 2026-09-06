---
module_id: SARCH-094
program: Software Engineering: Software Architecture
level: 2
module_number: 94
title: Architecture for Machine-Learning-Enabled Products
status: complete
last_verified: 2026-09-06
---

# Architecture for Machine-Learning-Enabled Products

## One-Page Review

### Governing question

How should architects integrate learned behavior into a product so that data, training, evaluation, serving, decisions, human authority, monitoring, change, and retirement form one governable system rather than an opaque model endpoint?

### Essential definitions

- a **machine-learning-enabled product** uses an empirically fitted model in a consequential product path;
- **intended use** names the task, population, environment, decision role, user, and prohibited uses for a model-enabled capability;
- a **feature** is an input representation used by a model; a **label** is an observed or constructed training or evaluation target;
- **training-serving skew** is a material difference between feature or transformation semantics during training and inference;
- **data leakage** lets training or evaluation use information unavailable at the intended prediction time or improperly shared across splits;
- **distribution shift** is a change between development data and operational inputs, outcomes, populations, or relationships;
- **drift** is a time-indexed change in a monitored distribution or performance relationship, not automatically evidence of harm;
- **calibration** relates predicted confidence or probability to observed frequency within a defined population;
- **decision policy** maps model outputs plus rules, costs, context, and authority into actions;
- a **model registry** records governed model identity, lineage, evaluation, approvals, deployment, and lifecycle;
- **shadowing** runs a candidate without giving it decision authority; a **canary** gives bounded real authority or exposure;
- **fallback** is explicitly designed behavior when a model, feature, dependency, or evidence path is unavailable or untrusted;
- **feedback loop** occurs when system outputs alter future observations or labels;
- **human oversight** is a designed allocation of information, time, competence, authority, and appeal—not a generic “human in the loop.”

### Central model, mechanism, or theorem

Represent an ML-enabled product release as

$$
M=(U,D,F,T,V,S,P,O,G,L),
$$

where $U$ is intended use and affected population, $D$ data provenance and rights, $F$ feature and label semantics, $T$ training lineage, $V$ evaluation and uncertainty, $S$ serving topology, $P$ decision policy and authority, $O$ operational observation and feedback, $G$ governance and change gates, and $L$ fallback, incident, appeal, and retirement lifecycle. A model artifact is releasable only as part of a coherent version of this tuple.

### Critical invariants

- every inference is attributable to model, feature, policy, and relevant data versions;
- training, evaluation, and serving transformations have explicit semantic parity or known differences;
- evaluation matches intended population, time, decision role, costs, and failure modes;
- model output is not silently promoted into decision authority;
- missing, late, poisoned, unauthorized, or out-of-range input has bounded behavior;
- protected, sensitive, copyrighted, personal, and derived data remain governed across collection, training, serving, logging, and deletion;
- aggregate performance cannot hide a mandatory subgroup, rare harm, or abstention failure;
- shadow and canary paths cannot duplicate consequential effects;
- fallback is tested under the same capacity, safety, security, and usability conditions in which it will be needed;
- monitoring distinguishes input shift, output shift, delayed labels, system failure, policy change, and actual outcome degradation;
- retraining cannot bypass review merely because it is automated;
- models, datasets, features, prompts, indexes, policies, and temporary experiments have retirement and rollback or roll-forward plans.

### Common failures

Common failures include wrapping a model with an API and calling the architecture complete; optimizing one offline metric; random splitting of time-correlated data; leakage through post-outcome features; training code that differs from serving code; logging sensitive prompts indefinitely; treating confidence as calibrated probability; thresholding without decision costs; calling drift a model failure; retraining automatically on poisoned feedback; allowing a shadow model to send messages; using a human reviewer with no time or authority; rolling back a model while retaining incompatible features or indexes; and assuming a foundation model provider owns the product's obligations.

### Compact example

A lender uses a model to prioritize applications for human review. The architecture records intended use and prohibited automatic rejection, versions source snapshots and feature definitions, splits evaluation by application time and relevant groups, and tests calibration and review workload. Online features carry event time and provenance; the serving response includes model version, uncertainty, and missingness. A policy service—not the model—routes cases, preserves statutory notices, and guarantees an appeal path. A candidate shadows first, then canaries within review capacity. Monitoring covers data quality, selection, delayed outcomes, workload, subgroup errors, overrides, and appeals. Rollback restores the compatible model-feature-policy set, while legitimate lending authorities retain decision and risk acceptance.

### Connections

[SARCH-064](064-architecture-fitness-functions.md) supplies repeated architectural evidence, [SARCH-068](068-threat-modeling-at-architecture-scale.md) supplies adversarial analysis, and [SARCH-091](091-architecture-for-regulated-and-safety-critical-systems.md) supplies assurance and legitimate authority. [SARCH-095](../ROADMAP.md) next examines multi-tenant platforms. Machine-learning programs own algorithm derivation; this module owns product-system integration.

## Governing Question

A learned model is one component in a larger decision and feedback system. It depends on historical data, constructed targets, transformations, training code, infrastructure, evaluation choices, deployment configuration, live features, downstream policy, users, and an environment that changes after release. Its behavior is empirical: tests support claims for sampled conditions, not all possible inputs. Architecture must therefore make uncertainty, provenance, authority, observation, and change first-class.

The design target is not “serve predictions.” It is to produce bounded product outcomes under intended and unintended conditions. That may require a deterministic rule, an abstention, human review, a smaller local model, a previous approved model, or no automation. A more accurate benchmark model can be worse when it is too slow, costly, opaque, fragile, unfairly selective, privacy-invasive, or impossible to recover.

## Why This Matters

Sculley and colleagues describe system-level ML debt including entanglement, hidden feedback loops, undeclared consumers, data dependencies, configuration, and changes in the external world [3]. Breck and colleagues propose production-readiness tests spanning data, model development, infrastructure, and monitoring rather than model accuracy alone [4]. These works remain useful because they expose architectural surfaces that a model artifact does not contain.

NIST AI RMF 1.0 is a voluntary, rights-preserving, non-sector-specific framework organized around govern, map, measure, and manage [1]. NIST's maintained page checked 2026-09-06 says version 1.0 is under revision; this chapter therefore cites the exact version and does not imply regulatory compliance. ISO/IEC 42001:2023 specifies requirements for an organizational AI management system [2]. A management framework can organize accountability, but neither framework proves a particular system safe, fair, lawful, or effective.

## Prerequisites and Retrieval

Retrieve supervised and unsupervised learning, training, validation, test set, feature, label, objective, loss, metric, confusion matrix, precision, recall, threshold, calibration, uncertainty, distribution, sampling, leakage, drift, bias, variance, overfitting, model, inference, batch, online, stream, registry, lineage, provenance, canary, shadow, feedback loop, privacy, threat, fallback, incident, appeal, and retirement.

SARCH-041 through SARCH-060 provide integration, data, deployment, observability, partial-failure, region, control-plane, queue, event, and edge boundaries. SARCH-061 through SARCH-070 provide scenario, risk, evidence, threat, cost, and review methods. SARCH-091 through SARCH-093 provide safety, high-change, and scale judgment. This chapter does not replace statistical learning theory, domain validation, privacy engineering, security testing, safety assurance, law, or human-subject research.

## Learning Objectives

After completing this module, you should be able to:

1. define intended use, affected populations, decision role, and prohibited use;
2. map data, feature, label, training, evaluation, model, policy, and serving lineage;
3. prevent leakage and training-serving semantic skew;
4. select evaluation evidence from decisions and consequences rather than one metric;
5. design batch, online, edge, and generative inference boundaries;
6. separate prediction from policy, action, and legitimate authority;
7. design shadow, canary, fallback, rollback, retraining, and retirement paths;
8. monitor system, data, performance, feedback, subgroup, and human outcomes;
9. analyze privacy, security, abuse, supplier, and generative-model risks; and
10. reject ML when deterministic or human-centered mechanisms are better.

## Core Exposition

**Begin with the decision system.** Name whose situation is represented, what observation arrives, what the model estimates, what policy consumes it, which action follows, who bears false-positive and false-negative consequences, and who may contest or override. Document conditions in which no prediction should occur. Intended use must be narrow enough to test; “fraud detection” is not a use case until transaction stage, actors, response, latency, and authority are known.

**Establish a non-ML baseline.** Compare a rule, existing workflow, simple statistical method, search, and no automation. The baseline supplies causal discipline, operational fallback, and incremental value. ML is warranted when learned generalization addresses a real decision and its total benefits survive data, infrastructure, risk, and human costs. Do not automate a policy dispute by encoding historical outcomes as labels.

**Treat data as governed product state.** Record source, collection purpose, consent or other authority, population, sampling, time, units, schema, missingness, transformations, annotators, quality limits, retention, access, and deletion. Separate event time from processing time. Dataset documentation such as datasheets makes intended uses and limitations reviewable [7]. Documentation is evidence organization, not proof that data is representative or lawful.

**Define labels as claims.** A label can be delayed, censored, selectively observed, contested, or changed by the system. “Fraud confirmed” may exist only for investigated transactions, creating selection bias. A click measures interaction, not satisfaction. A hospital code may reflect care and billing processes, not biological truth. Version label construction and preserve raw provenance so changes can be audited and backfilled without rewriting history silently.

**Prevent leakage by time and entity.** Split data at the unit and time boundary of intended generalization. The same patient, device, customer, document, or near-duplicate in train and test can inflate performance. Features produced after the decision time cannot be used for that decision. Fit normalization, imputation, vocabularies, and selection only on permitted training data. Test pipelines for temporal availability, not merely column presence.

**Make feature semantics reusable and attributable.** Training and serving need the same definition of unit, window, timezone, join, default, freshness, and entity identity. Reusing transformation code helps but does not ensure equal source timing or availability. Each feature response should expose value, event time, computation version, and missingness where consequences warrant. Feature stores can centralize mechanisms while still spreading semantic errors widely.

**Reproduce training as a governed build.** Identify source snapshots, code, dependencies, environment, random seeds and nondeterminism, feature/label definitions, hyperparameters, objective, hardware assumptions, and output digest. A registry entry links model identity to this lineage, evaluation, intended use, approval, and deployment. Exact bitwise reproduction may be unavailable on some accelerators; record that limitation rather than inventing determinism.

**Evaluate the decision, not only the predictor.** Start with a confusion matrix or task-appropriate output analysis by population and operating condition. Threshold selection embeds costs and capacity. For a binary classifier, with false-positive cost $C_{FP}$ and false-negative cost $C_{FN}$, an illustrative expected loss is

$$
L=C_{FP}FP+C_{FN}FN,
$$

but legitimate costs are rarely exhausted by two numbers. Add calibration, ranking, abstention, latency, availability, privacy, security, accessibility, workload, appeals, distributional slices, rare events, and counterfactual or causal evidence where the claim requires it. A held-out metric does not prove benefit after the model changes user behavior.

**Keep policy outside the score.** A score or generated text is not an authorized action. A versioned decision layer applies threshold, business rules, constraints, uncertainty, capacity, jurisdiction, and human authority. It records score, policy, reasons available, and result without exposing unnecessary sensitive features. This separation allows the same model to support different legitimate policies and lets policy change without secretly retraining meaning.

**Design abstention and fallback.** Define missing-feature, out-of-distribution, low-confidence, conflict, timeout, provider failure, capacity exhaustion, and suspected-attack behavior. Fallback may be a deterministic safe rule, cached prior state, human review, smaller model, delayed decision, or explicit unavailability. It must fit actual review capacity and preserve required service. A human queue that grows beyond decision deadlines is automated denial disguised as oversight.

**Choose serving topology from consequence.** Batch inference provides reproducible snapshots but can be stale. Online inference uses current context but adds dependencies and latency. Streaming updates reduce delay while increasing ordering and replay complexity. Edge inference improves locality and offline behavior but complicates model distribution, hardware diversity, privacy, revocation, and observability. A cascade can reduce cost by escalating selected cases, but its router becomes a model and privacy boundary.

**Separate deploy, shadow, release, and authority.** A shadow model receives mirrored inputs and produces no consequential side effect. Ensure its logging and feature access are authorized. Compare it against outcomes and the incumbent without assuming agreement means correctness. Canary a coherent model-feature-policy set for a bounded population only after offline gates. Abort on safety, security, privacy, fairness, capacity, or domain guardrails even when aggregate utility improves.

**Version the whole inference contract.** Record request schema, preprocessing, feature versions, model, tokenizer or encoder, prompt and retrieval configuration where relevant, policy, postprocessing, and dependency versions. Mixed versions need compatibility rules. Rollback must restore a compatible set; reverting weights while retaining a new tokenizer or feature meaning can be worse than staying forward.

**Monitor multiple causal layers.** System signals cover availability, latency, capacity, dependency failure, and error. Data signals cover schema, missingness, range, freshness, provenance, and distribution. Model signals cover outputs, uncertainty, calibration, slice behavior, and delayed labeled performance. Decision and human signals cover actions, overrides, workload, complaints, appeals, harm, and outcomes. Drift is a diagnostic trigger; it does not identify cause or prescribe retraining.

**Control feedback.** Recommendations shape exposure; fraud holds determine which cases are investigated; rankings affect clicks that become labels. Log eligibility, assignment, exposure, nonselection, policy, and downstream observation so the missing counterfactual is visible. Reserve exploration only where authorized and safe. Audit whether optimization narrows future data, disadvantages populations, or creates self-confirming labels.

**Govern retraining as change.** A scheduled pipeline can validate inputs, train, evaluate, and propose a candidate. It should not automatically acquire authority unless risk and evidence justify that gate. Compare with incumbent and baseline, inspect changed populations, reproduce material results, approve intended use, stage release, and monitor. Data deletion, corrected labels, new law, changed workflow, or supplier model update can require reevaluation even without metric drift.

**Threat-model the ML lifecycle.** Analyze training-data poisoning, label manipulation, model or prompt injection, adversarial inputs, extraction, inversion, membership inference, sensitive logging, dependency compromise, denial of wallet, and abuse of generated output. Bound tool access and external writes. Treat retrieved documents and model output as untrusted content. Conventional authentication and least privilege remain necessary; “AI safety” is not a substitute for security engineering.

**Treat generative behavior as nondeterministic untrusted proposal.** Validate structured outputs, constrain tools, isolate execution, cite or retain evidence where the use demands it, and require confirmation for consequential actions. Retrieval augments context but does not guarantee truth, freshness, authorization, or resistance to injected instructions. NIST AI 600-1 is a cross-sectoral generative-AI profile accompanying AI RMF 1.0 [8]; it informs risk elicitation but cannot decide a product's controls by checklist.

**Plan incidents and retirement.** Be able to stop authority, preserve evidence, identify affected inferences, notify appropriate owners, repair downstream effects, revoke credentials or models, and provide appeal. Retain sufficient lineage without violating deletion and minimization duties. Retirement removes endpoints, features, training jobs, datasets where permitted, caches, embeddings, prompts, monitors, access, and undeclared consumers. A model that is no longer served can still persist in downstream decisions and data.

## Definitions and Notation

For a binary decision over a stated evaluation population, use $TP$, $FP$, $TN$, and $FN$. Precision is $TP/(TP+FP)$ when the denominator is nonzero; recall is $TP/(TP+FN)$ when its denominator is nonzero. These measures describe different conditional populations and do not encode consequence, prevalence stability, calibration, or causal value.

Let $v=(v_d,v_f,v_t,v_m,v_p,v_s)$ identify dataset, feature, training, model, policy, and serving configuration. Let $x_t$ be information legitimately available at decision time $t$, $\hat y=f_{v_m}(x_t)$ a model output, and $a=\pi_{v_p}(\hat y,x_t,c)$ an action under policy and context $c$. Architecture must not erase the distinction between $\hat y$ and $a$.

## Mechanisms, Invariants, or Proof Structure

### Lineage invariant

Every consequential action can identify the exact coherent data/feature/model/policy/serving configuration and intended-use record that produced it, subject to privacy and retention constraints.

### No-silent-authority invariant

A model, shadow, retraining pipeline, supplier update, or generated response cannot acquire new consequential authority without the declared policy and governance transition.

### Evaluation-boundary invariant

Every performance claim names population, time, sampling, exclusions, metric, threshold, uncertainty, and decision role; transfer beyond that boundary is labeled unverified.

### Fallback-capacity invariant

If release depends on human or deterministic fallback, that path has capacity and correctness evidence for the failure and surge conditions that invoke it.

### Executable release-gate illustration

<!-- bijux-verify: {"id":"ml-release-gate","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"ready: canary\nstale data: block\nweak slice: block\nno fallback: block\nshadow effects: block\n","stderr":""}} -->
```python
def gate(*, lineage, data_current, mandatory_slices,
         fallback_tested, shadow_side_effects):
    if not lineage or not data_current:
        return "block"
    if not mandatory_slices or not fallback_tested:
        return "block"
    if shadow_side_effects:
        return "block"
    return "canary"

cases = {
    "ready": (True, True, True, True, False),
    "stale data": (True, False, True, True, False),
    "weak slice": (True, True, False, True, False),
    "no fallback": (True, True, True, False, False),
    "shadow effects": (True, True, True, True, True),
}
for name, facts in cases.items():
    print(f"{name}: {gate(lineage=facts[0], data_current=facts[1], mandatory_slices=facts[2], fallback_tested=facts[3], shadow_side_effects=facts[4])}")
```

This predicate demonstrates a fail-closed ordering only. Boolean evidence cannot express statistical uncertainty, domain validity, proportionality, lawful basis, safety, fairness, or legitimate authority.

### Proposition: equal aggregate accuracy does not imply equal decision behavior

Two classifiers can each make 90 correct predictions in 100 while one has ten false positives and the other ten false negatives. If actions and consequences differ, identical accuracy coexists with materially different behavior. Therefore aggregate accuracy cannot determine policy fitness.

### Proposition: reproducible training does not imply valid deployment

A pipeline can reproduce identical weights from a biased, leaked, obsolete dataset. Reproducibility establishes repeatability of a build under conditions, not validity of data, intended use, or outcomes. Therefore reproducible training does not imply valid deployment.

## Alternatives and Trade-Offs

**Rule versus learned model.** Rules provide explicit behavior and direct policy control; models can generalize complex patterns but add empirical uncertainty and data dependence. Hybrid designs still need one authority model.

**Batch versus online inference.** Batch is easier to reproduce and isolate; online uses current context but adds latency and dependency failure. Freshness and consequence determine the path.

**Central versus edge serving.** Central serving eases update and monitoring; edge serving supports privacy, latency, and disconnection while making hardware compatibility, revocation, and evidence harder.

**Single model versus cascade.** A cascade can reduce cost or defer uncertainty but creates router error, correlated failure, privacy transfer, and multiple-version observability.

**Automatic versus governed retraining.** Automation reduces toil and staleness; governance protects intended use and consequences. Automate evidence production before automating authority.

**Rollback versus forward repair.** Rollback is fast when feature, policy, data, and downstream state remain compatible. Forward repair is necessary after irreversible decisions, supplier changes, or incompatible representations.

## Failure Modes and Misconceptions

1. **“The model is the product.”** Data, policy, serving, users, and feedback determine outcomes.
2. **“Accuracy is enough.”** Prevalence, error types, calibration, slices, costs, and actions matter.
3. **“Random train/test split prevents leakage.”** Time, entities, near-duplicates, and post-outcome features can cross it.
4. **“Shared transformation code prevents skew.”** Data availability, event time, joins, defaults, and source behavior can still differ.
5. **“Confidence is probability.”** Scores require calibration evidence for the relevant population.
6. **“Drift means retrain.”** It is a signal; cause may be data failure, seasonality, policy, attack, or benign change.
7. **“No drift means no harm.”** Stable distributions can contain persistent failure or missed subgroups.
8. **“Human review makes it safe.”** Reviewers need time, information, competence, authority, and appeal.
9. **“Shadow mode is harmless.”** It can expose data, spend resources, and accidentally trigger effects.
10. **“The feature store owns feature meaning.”** Domain owners retain semantics and consequences.
11. **“A registry provides governance.”** Records help; decisions, evidence, authority, and enforcement still matter.
12. **“Retraining is a routine deployment.”** New data can change behavior and affected populations.
13. **“Rollback means old weights.”** Compatible features, policy, tokenizer, retrieval, and state must return together.
14. **“More data removes bias.”** More data can amplify selection, historical policy, and labeling defects.
15. **“Explainability proves correctness.”** An explanation can be plausible, unstable, incomplete, or about the wrong model.
16. **“Retrieval makes generation factual.”** Sources can be wrong, stale, unauthorized, absent, or malicious.
17. **“A provider owns the risk.”** Product integrators own their use, data, policy, fallback, and affected users.
18. **“Offline improvement guarantees product improvement.”** Feedback and changed behavior break that implication.
19. **“Deterministic settings make generative output guaranteed.”** software, hardware, provider, and model changes can alter behavior.
20. **“Documentation certifies trustworthiness.”** Documentation exposes evidence and gaps; it does not decide acceptability.

## Worked Examples

### Example 1

**Situation.** A churn model scores 92% accuracy, but only 5% of customers churn.

**Reasoning.** A classifier that always predicts “stay” scores 95% accuracy and is useless for identifying churn. Define the action and capacity: retention staff can contact 1,000 customers. Evaluate precision among selected customers, recall of valuable preventable churn, calibration, incremental treatment effect, cost, contact burden, and subgroup outcomes. Compare with a deterministic baseline and randomized controlled allocation where appropriate. Do not infer that contact caused retention from model ranking alone.

**Conclusion.** A model metric has meaning only relative to prevalence, decision, intervention, and evidence design.

### Example 2

**Situation.** A hospital deterioration model uses “ICU transfer within six hours” as an input to predict ICU transfer.

**Reasoning.** The feature occurs after or as part of the target decision and leaks the outcome. Random row splitting will not reveal the temporal impossibility. Reconstruct features from event-time snapshots available before the prediction cutoff, split by patient and time, and involve clinical experts in label and intended-use review. Compare with existing escalation and test missing/late observations. The model can advise; clinical authority and safety assurance remain external.

**Conclusion.** Temporal availability is a semantic invariant, not a data-frame property.

### Example 3

**Situation.** Training computes “spend in the last 30 days” at midnight UTC, while serving subtracts 30 calendar days in local time.

**Reasoning.** Daylight-saving transitions, late events, timezone, refunds, and boundary inclusion produce skew. Define event time, interval endpoints, currency, refund treatment, lateness, and timezone once. Generate offline and online implementations from the governed definition or compare them continuously using historical replay and live samples. Carry definition version and freshness with the feature. Block serving if missingness exceeds its contract.

**Conclusion.** Shared names and code are insufficient without shared temporal and domain semantics.

### Example 4

**Situation.** A fraud model lowers aggregate loss but holds far more legitimate payments for one region.

**Reasoning.** Inspect exposure, prevalence, label selection, calibration, false holds, confirmed loss, review delay, abandonment, appeal, and downstream account action by relevant slices. Separate model score from regional decision policy and review capacity. A higher threshold may reduce false holds while increasing fraud; legitimate owners must evaluate both. Investigate data and policy differences rather than deleting the slice. Canary with hard harm and workload guardrails.

**Conclusion.** Aggregate value cannot authorize concentrated harm; policy and capacity are part of model release.

### Example 5

**Situation.** A candidate ranking model runs in shadow beside production.

**Reasoning.** Mirror only authorized inputs, identify candidate outputs, and prohibit writes to ranking, notifications, billing, or user profiles. Account for doubled feature and inference capacity. Compare on eligible requests, not just successful shadow calls; log incumbent exposure and delayed outcomes. Agreement measures sameness, not correctness. Before canary, validate feedback effects, experiment interaction, rollback, and candidate-specific monitoring.

**Conclusion.** Shadowing provides bounded comparative evidence only when it has no hidden authority or selection bias.

### Example 6

**Situation.** A vision model on warehouse vehicles becomes unavailable, so all cases go to one remote operator.

**Reasoning.** At peak, 200 vehicles each generate four uncertain cases/minute, but the operator can resolve 20/minute. The fallback saturates fortyfold and is not a fallback. Keep independent physical interlocks and bounded local stop behavior; prioritize and distribute review; reduce operating envelope; expose degraded mode; and test prolonged outage. Model advice cannot replace safety-rated control without the applicable assurance.

**Conclusion.** Fallback must be safe and capacity-feasible under the condition that invokes it.

### Example 7

**Situation.** A model's input distribution shifts after a mobile application changes a default value.

**Reasoning.** Schema remains valid, but missingness and value frequency change. Correlate the shift with client version and transformation lineage. Replay old/new representations, check slice outputs and eventual labels, and determine whether meaning changed or only encoding. Do not retrain on mixed semantics. Repair the client or version feature meaning, then reevaluate the model and policy. Record which prior decisions may be affected.

**Conclusion.** Drift diagnosis must connect data lineage, semantics, outcomes, and remediation.

### Example 8

**Situation.** A support assistant retrieves internal documents and can issue refunds through a tool.

**Reasoning.** Treat user text, retrieved documents, and generated tool arguments as untrusted. Authorize retrieval per user and document, filter secrets before logging, version corpus and prompt, validate structured refund arguments, enforce deterministic amount and account limits outside the model, and require confirmation for consequential cases. Separate citation display from source correctness. Test prompt injection, poisoned documents, denial of wallet, false claims, missing sources, and provider outage; provide a non-generative support path.

**Conclusion.** Retrieval and generation propose content; deterministic controls and legitimate agents authorize effects.

### Example 9

**Situation.** An automated weekly retraining pipeline improves AUC and deploys directly.

**Reasoning.** AUC can improve while calibration, a mandatory slice, latency, or false-positive cost worsens. The pipeline should freeze data lineage, validate deletion and label windows, compare baseline/incumbent/candidate, evaluate slices and decision thresholds, test serving compatibility, and create a proposal. A risk-based gate approves canary authority. Monitor delayed outcomes before promotion. Preserve the prior coherent bundle and forward-repair plan.

**Conclusion.** Automate reproducible evidence; grant production authority through explicit policy.

### Example 10

**Situation.** A municipality predicts housing-inspection priority from historical enforcement records.

**Reasoning.** Historical inspections reflect prior allocation, complaints, access, and enforcement policy, so uninspected properties lack equivalent labels. Map affected tenants and owners, legal purpose, privacy, accessibility, and appeal. Compare needs-based rules and random audit. Record eligibility and nonselection; use the model only for bounded prioritization, never to waive mandatory inspection or impose penalty without evidence. Include inspectors and communities in outcome evaluation. Monitor geographic allocation, false negatives, complaints, repairs, displacement risk, and feedback. Retain public authority and an auditable correction process.

**Conclusion.** Architecture must expose selective labels and public authority rather than laundering policy through prediction.

## Cross-Program Connections

- [Data Engineering](../../19-data-engineering/ROADMAP.md) owns reliable ingestion, transformation, orchestration, and data-quality operations.
- [Data Architecture Engineering](../../20-data-architecture-engineering/ROADMAP.md) owns data meaning, provenance, authority, privacy, and lifecycle.
- [Algorithms Engineering](../../16-algorithm-engineering/ROADMAP.md) owns algorithmic complexity and empirical algorithm evaluation.
- [Testing and Software Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) owns test design, statistical oracles, reliability, and quality evidence.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) owns adversarial ML depth, identity, application security, privacy threats, and incident controls.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md) owns reusable training, registry, feature, serving, and observability capabilities as internal products.

## References

1. Elham Tabassi, [*Artificial Intelligence Risk Management Framework (AI RMF 1.0)*](https://doi.org/10.6028/NIST.AI.100-1), NIST AI 100-1, January 2023; NIST status and revision notice checked 2026-09-06.
2. ISO/IEC, [ISO/IEC 42001:2023, *Information technology — Artificial intelligence — Management system*](https://www.iso.org/standard/42001), edition 1, December 2023; official published status checked 2026-09-06.
3. D. Sculley et al., [“Hidden Technical Debt in Machine Learning Systems”](https://research.google/pubs/hidden-technical-debt-in-machine-learning-systems/), NeurIPS 2015, pp. 2503–2511.
4. Eric Breck et al., [“What's Your ML Test Score? A Rubric for ML Production Systems”](https://research.google/pubs/whats-your-ml-test-score-a-rubric-for-ml-production-systems/), NeurIPS Reliable ML Workshop, 2016.
5. Chip Huyen, *Designing Machine Learning Systems*, O'Reilly, 2022. Data, training, serving, distribution shift, monitoring, and continual learning.
6. Margaret Mitchell et al., [“Model Cards for Model Reporting”](https://research.google/pubs/model-cards-for-model-reporting/), FAT* 2019.
7. Timnit Gebru et al., [“Datasheets for Datasets”](https://doi.org/10.1145/3458723), *Communications of the ACM* 64(12), 2021, pp. 86–92.
8. Chloe Autio et al., [*Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile*](https://doi.org/10.6028/NIST.AI.600-1), NIST AI 600-1, July 2024; official record checked 2026-09-06.
9. Nithya Sambasivan et al., [“Everyone Wants to Do the Model Work, Not the Data Work: Data Cascades in High-Stakes AI”](https://research.google/pubs/everyone-wants-to-do-the-model-work-not-the-data-work-data-cascades-in-high-stakes-ai/), CHI 2021.
10. Solon Barocas, Moritz Hardt, and Arvind Narayanan, *Fairness and Machine Learning: Limitations and Opportunities*, MIT Press, 2023.
11. Ian Goodfellow, Yoshua Bengio, and Aaron Courville, [*Deep Learning*](https://www.deeplearningbook.org/), MIT Press, 2016. Optimization, generalization, representation, and sequence models.
12. ISO/IEC, [ISO/IEC 23053:2022, *Framework for Artificial Intelligence Systems Using Machine Learning*](https://www.iso.org/standard/74438.html), edition 1, June 2022.

## Exercises

### Exercise 1

Define intended use, feature, label, training-serving skew, leakage, drift, calibration, decision policy, shadow, canary, and fallback. Explain why a model endpoint is not a complete ML product architecture.

### Exercise 2

For 1,000 evaluated cases, a classifier has $TP=120$, $FP=80$, $TN=760$, and $FN=40$. Compute precision, recall, accuracy, and expected loss when $C_{FP}=2$ and $C_{FN}=9$. State at least six limitations of choosing a release solely from these values.

### Exercise 3

Diagnose a training pipeline that randomly splits transaction rows, computes 90-day customer aggregates from the full table, uses chargeback labels observed up to a year later, and serves aggregates from a separate stream. Propose corrected temporal, entity, lineage, and parity controls.

### Exercise 4

Design the complete candidate-to-retirement lifecycle for a model that prioritizes customer-support tickets. Include baseline, data and label provenance, evaluation, slices, workload, shadow, canary, policy, human authority, monitoring, feedback, retraining, incident, rollback, appeal, and removal.

### Exercise 5

A coastal community considers an ML system combining satellite images, local sensors, fishing reports, and weather forecasts to advise harmful-algal-bloom closures. Design an architecture that handles missing and unequal data, intermittent connectivity, scientific uncertainty, livelihood impacts, public communication, privacy, security, model change, and legitimate closure authority.

## Answers to the Exercises

### Answer 1

Intended use names task, population, environment, decision role, users, and prohibited use. A feature is a model input representation; a label is a constructed training or evaluation target. Training-serving skew is a difference in transformation or source semantics between development and inference. Leakage exposes unavailable or improperly shared information. Drift is a time-indexed distribution or relationship change. Calibration relates stated confidence to observed frequency for a population. Decision policy maps output and context to action. Shadowing runs without authority; canarying grants bounded exposure. Fallback is designed behavior when the ML path is unavailable or untrusted. An endpoint omits data rights and lineage, feature timing, evaluation, policy, authority, feedback, monitoring, recovery, appeal, and retirement.

### Answer 2

Precision is $120/(120+80)=0.60$. Recall is $120/(120+40)=0.75$. Accuracy is $(120+760)/1000=0.88$. The illustrative loss is $2(80)+9(40)=160+360=520$ cost units. These values omit uncertainty and repeated sampling; whether cases represent the intended future population; subgroup and intersectional behavior; calibration; latency and availability; abstentions and missing inputs; label validity and delay; intervention effects; privacy, security, accessibility, and safety; review capacity; appeals; distribution shift; and whether the chosen costs have legitimate units and authority. Compare thresholds and baselines within the whole decision system rather than promoting the model from four aggregates.

### Answer 3

Random rows can place the same customer and later transactions in both training and test. Full-table aggregates leak future behavior into earlier examples. A one-year label requires a maturity cutoff or explicit censoring, so recent cases cannot be treated as negatives. A separate serving stream can differ in event time, lateness, refunds, deduplication, timezone, and missingness.

Define a prediction timestamp for each eligible transaction. Build every feature only from events available before it. Split by time and customer or otherwise prevent entity contamination; retain a final future holdout. Freeze a chargeback observation window and distinguish matured negatives from unknown outcomes. Version raw snapshots, eligibility, label construction, aggregates, code, dependencies, and model. Use one governed feature definition for batch and stream, carry event time and definition version, and continuously compare offline reconstruction with online values. Test late and duplicate events, clock boundaries, missing sources, corrections, and replay. Reevaluate when payment or investigation policy changes.

### Answer 4

Define intended use as queue prioritization, not automatic ticket closure. Compare first-in-first-out, severity rules, search, and current triage. Version ticket sources, consent and retention, language and channel populations, eligibility, label such as time-to-valid-resolution, and annotation uncertainty. Prevent post-resolution leakage and split by customer and time. Evaluate ranking utility, urgent-ticket recall, calibration or confidence, language/accessibility slices, latency, agent workload, wait distributions, false deprioritization, and customer outcomes.

Register the coherent data-feature-model-policy bundle. Shadow with no routing effect and authorized logging. Canary within staffed capacity with guardrails for urgent misses, queue age, subgroup delay, complaints, and system load. A policy layer applies severity rules and lets qualified agents reprioritize with reasons; customers can escalate and appeal. Monitor sources, missingness, output distribution, delayed outcomes, overrides, queues, security, and feedback because routing changes future response labels. Retraining creates a candidate subject to the same gates. Incidents stop model authority and restore a compatible baseline or repair forward; affected tickets are identified and requeued. Retirement removes serving, features, training jobs, permissions, monitors, and undeclared consumers while retaining lawful decision evidence.

### Answer 5

Treat sensing, scientific advice, and legal closure as separate authorities. Record source identity, location, time, calibration, units, resolution, weather context, rights, and missingness for satellite, sensor, report, and forecast data. Local reports require consent, protection against retaliation, language and accessibility support, and provenance without unnecessary identity exposure. Store immutable raw observations and version quality corrections. Intermittent sites retain bounded local capture and public-safety procedures; delayed data is visibly stale, not silently current.

Build versioned features by geographic and time window, preserving uncertainty and non-observation. Evaluate by season, location, species, sensor coverage, weather, community, and historical closure regime with marine scientists; avoid treating prior closure as biological truth. Compare scientific thresholds and no-ML baselines. The model returns bloom evidence and uncertainty, while a policy layer combines laboratory confirmation, public-health constraints, livelihood impact, and authorized human judgment. It may abstain. Only the legally designated authority issues, changes, or lifts a closure and provides reasons, accessible multilingual notice, correction, and appeal.

Shadow on historical and live data without publishing closures; canary only as advice under an approved study. Test missing satellite passes, failed and poisoned sensors, false reports, storms, novel blooms, geographic shift, network loss, cyberattack, model/provider outage, and simultaneous regional demand. Fallback uses conservative scientific protocol and qualified local communication within real staffing capacity. Monitor data coverage, model outputs, laboratory results, false and missed alerts, time to decision, geographic and community impacts, appeals, compliance, privacy, and recovery. Retraining records corrected labels and changed ecology; it cannot auto-authorize closure. Public-health, marine-science, environmental, fisheries, Indigenous/local community, livelihood, accessibility, privacy, security, and legal authorities own real review and residual decisions.
