---
module_id: SDRE-026
program: Software Engineering: Software Delivery & Reliability Engineering
level: 1
module_number: 26
title: Canary Deployment
status: complete
last_verified: 2026-09-06
---

# Canary Deployment

## One-Page Review

### Governing question

How can a release receive enough representative production exposure to reveal important regressions while bounding harm, preserving attribution, and making promotion decisions honestly?

### Essential definitions

- a **canary** is a partial, time-bounded deployment of a candidate evaluated against a control and absolute safety criteria;
- the **control** is the currently accepted subject used for contemporaneous comparison;
- an **allocation unit** is the stable entity assigned to control or candidate: request, session, user, tenant, device, partition, region, or work item;
- **exposure** is candidate-handled work and the users, data, resources, or error budget placed at risk;
- a **representative population** contains the workload properties relevant to the claims being evaluated;
- a **guardrail** is an absolute condition whose breach stops or reverses exposure;
- a **promotion criterion** is declared evidence required to expand exposure;
- **attribution** is the justified connection between observed differences and the candidate rather than unrelated change;
- **contamination** occurs when subjects, traffic, or effects mix so comparison no longer identifies treatment;
- **minimum detectable effect** is the smallest difference an evaluation is designed to detect with stated error probabilities;
- a **false positive** rejects a sound candidate; a **false negative** promotes a harmful candidate;
- **sequential testing** examines accumulating evidence repeatedly and therefore needs a stopping rule that controls error.

### Central model, mechanism, or theorem

For candidate traffic fraction $f$, duration $T$, request rate $\lambda$, and conditional candidate failure probability $p_c$, expected candidate-induced failures under a simple homogeneous model are

$$
E[F]=f\lambda T p_c.
$$

If independent exposures each encounter a rare defect with probability $p$, the probability of seeing at least one occurrence in $n$ exposures is $1-(1-p)^n$. To obtain detection probability at least $q$,

$$
n\ge\frac{\ln(1-q)}{\ln(1-p)}.
$$

The assumptions rarely hold exactly; use the result to expose sample-size limits, not to certify safety.

### Critical invariants

- the canary and control are immutable, version-tagged deployment subjects;
- allocation is stable at the unit required for state and user experience;
- candidate exposure has declared population, size, duration, maximum harm, and owner;
- guardrails use absolute service and business constraints as well as relative comparison;
- telemetry binds to subject, cohort, operation, time, and outcome;
- control and candidate experience comparable external conditions or confounding is recorded;
- promotion criteria and stopping rules are fixed before observing favorable results;
- missing, delayed, low-volume, or contaminated signals never count as success;
- state, schema, side effects, and rollback remain compatible throughout exposure;
- expansion proceeds only after evidence; a halt limits harm but does not prove causality.

### Common failures

Failures include selecting only healthy servers, routing easy requests to the candidate, allocating each request for a stateful workflow, comparing morning control with evening candidate, using fleet-wide averages, ignoring absolute SLO failure because candidate and control fail equally, choosing metrics after looking at results, repeatedly testing without error control, running too briefly for queues or leaks, exposing one giant tenant as “1%,” permitting canary writes without rollback compatibility, overlapping unrelated releases, treating no alerts as evidence, and automatically rolling back irreversible effects.

### Compact example

A candidate receives a stable 5% of accounts, stratified across region and plan. Metrics are tagged by digest and cohort. Absolute correctness, security, and SLO guardrails stop exposure immediately; latency and error differences require predeclared sample and duration. After one complete billing cycle, sufficient traffic, healthy dependencies, and clean data reconciliation, exposure advances to 20%. Missing telemetry holds at 5%; it never promotes.

### Connections

[SDRE-025](025-blue-green-deployment.md) prepares full environments and traffic switching. [SDRE-027](../ROADMAP.md) develops replacement mechanics during rolling deployment. Testing and Quality Engineering owns experimental design; this module owns release-risk control.

## Governing Question

Pre-production testing cannot reproduce every production input, dependency, data distribution, timing pattern, or failure interaction. Sending a candidate everywhere discovers those differences at maximum blast radius. A canary deliberately spends a bounded amount of production exposure to learn before broad rollout.

The difficult engineering is not selecting “5%.” The team must decide what constitutes an independent exposure, which population represents risk, how long delayed behavior takes to appear, which metrics are attributable, what error rates are tolerable, and which state changes make retreat unsafe. Canarying is a controlled production evaluation, not a green dashboard ritual.

## Why This Matters

Google's SRE Workbook defines canarying as a partial and time-limited deployment followed by evaluation to decide whether rollout should continue [1]. It stresses representative population, duration, attributable metrics, absolute measures, and special treatment of noninteractive work. Those principles are implementation-independent.

A smaller cohort usually reduces candidate-caused harm roughly in proportion to exposure under a homogeneous model. But small cohorts also reduce statistical power, hide rare paths, and may overload the few candidate instances. Canary design balances detection speed, representativeness, service objectives, and error-budget cost.

Current Kubernetes documentation illustrates replica-based stable/canary coexistence and notes that replica counts influence traffic ratio [2]. That ratio is only approximate when request rates, connection reuse, topology, or instance capacity differ. Routing measurement, not replica count alone, establishes exposure.

## Prerequisites and Retrieval

Retrieve deployment subject, digest, control, experiment, population, sample, metric, distribution, mean, quantile, variance, probability, independence, confidence, hypothesis, SLO, error budget, traffic routing, session, queue, state compatibility, rollback, and causal confounding.

From SDRE-020 retrieve feedback latency and non-negotiable evidence, from SDRE-022 evidence scope, from SDRE-024 state compatibility, and from SDRE-025 routing authority and draining. Statistical testing complements engineering guardrails; it does not replace them.

## Learning Objectives

After completing this module, you should be able to:

1. define candidate, control, allocation unit, exposure, and decision policy;
2. choose stable, representative, risk-aware populations;
3. distinguish relative comparison from absolute guardrails;
4. estimate exposure cost and rare-defect detection limits;
5. identify confounding, contamination, dependence, and selection bias;
6. select metrics across correctness, reliability, performance, security, and business outcomes;
7. choose durations from traffic volume and mechanism timescales;
8. design canaries for streams, queues, batch, tenants, regions, and stateful work;
9. govern halt, rollback, roll forward, and exposure expansion;
10. audit an automated canary controller without overstating its evidence.

## Core Exposition

**Define the subject and hypothesis.** Identify exact artifact, configuration, flags, dependencies, and migrations. State which changes are under evaluation and what failures they could cause. If candidate and control differ in several unknown ways, a detected regression may block release but diagnosis will be harder.

A useful hypothesis is operational: “At comparable workload, candidate checkout errors remain below the absolute SLO threshold and do not exceed control by more than 0.2 percentage points; p99 latency does not regress more than 10%; payment duplication remains zero.” Vague goals such as “looks healthy” cannot govern automation.

**Choose the allocation unit.** Per-request allocation gives volume quickly but can make one user's workflow alternate between versions. Session or user allocation preserves experience and cache behavior. Tenant allocation prevents cross-version state interaction but one large tenant may dominate exposure. Region allocation tests infrastructure integration yet confounds geography and dependency behavior. Partition or work-item allocation fits pipelines.

Use deterministic hashing over stable identity plus experiment seed when appropriate. Record assignment and actual handling; retries, proxies, failover, and queue redelivery can cross cohorts. Exclude only for a declared safety reason, not to make the candidate look good.

Stratify when relevant: region, device, plan, request class, data size, dependency, and risk. A random 1% may contain no rare enterprise tenants or no large objects. A risk-targeted canary can deliberately include hard cases but its result cannot be generalized to populations it did not cover.

**Bound exposure.** Declare fraction, maximum users or tenants, maximum requests or jobs, time, data scope, regional scope, privileged operations, and error-budget spend. Percentages obscure concentration: one tenant can represent 1% of tenants and 40% of revenue or writes.

Under a simple model, incremental failures attributable to a candidate with excess failure probability $\Delta p$ are approximately $f\lambda T\Delta p$. Use pessimistic bounds for stop policy. Security compromise, duplicated payment, corrupted data, or safety hazard may have a zero-tolerance guardrail independent of expected count.

**Establish a valid control.** Compare candidate and control concurrently so traffic cycles and dependency incidents affect both. Ensure they receive comparable inputs and resource conditions. Candidate placement on newer hosts or a quieter zone can bias latency; sharing one saturated dependency can make both fail together.

Relative comparison catches changes when baselines drift, but absolute measures protect users. If control errors at 20% and candidate at 19%, the candidate is relatively better yet the service is unacceptable. Both subjects changing together may signal dependency failure or metric corruption. Gate on SLOs, invariants, and comparison.

Avoid overlapping releases whose cohorts or metrics contaminate one another. If unavoidable, model the factorial combinations and ensure attribution; most delivery systems should serialize high-risk canaries for operational clarity.

**Select attributable metrics.** Start with correctness invariants and externally observed outcomes. Include error ratios by operation, latency distributions, saturation, resource leaks, queue age, retries, dependency calls, cache behavior, data reconciliation, security denials, and business results. Fleet averages, process uptime, and one success count are weak.

Tag every event with candidate/control subject, assignment, actual handler, request class, and time, without leaking sensitive identity. Metric aggregation interval must be no longer than useful decision intervals. Monitor telemetry completeness and lag as first-class guardrails.

Quantiles need adequate samples and comparable distributions. An apparent p99 from 80 requests is essentially an extreme observation, not a stable tail estimate. Means can hide tail regressions. Inspect distributions or multiple quantiles and define minimum counts.

**Choose duration by mechanisms.** Duration must cover enough independent work and the timescale of plausible defects: cache warm-up, garbage collection, connection renewal, certificate refresh, memory growth, queue cycles, scheduled jobs, billing cycles, and dependency failover. “Thirty minutes” has no evidentiary meaning without such a hypothesis.

For an independent rare path with occurrence probability $p$, zero observations in $n$ requests is unsurprising when $n$ is small. To have probability $q$ of at least one observation, solve $1-(1-p)^n\ge q$. At $p=0.001$ and $q=0.95$, $n\ge2994.23$, hence at least 2,995 exposures. Real traffic is clustered and dependent, so the effective sample can be smaller.

Time-of-day matters. Off-peak traffic may miss saturation defects; one weekday misses weekly work. Long canaries delay delivery and increase exposure to unrelated environmental changes. Use the shortest duration that meets declared traffic and mechanism coverage, not a ritual duration.

**Design decisions before data.** Define pass, hold, halt, rollback, and inconclusive states. A pass requires all mandatory evidence and sufficient sample. Hold means more time or data is needed. Halt stops expansion on a breach. Rollback changes traffic or subject only when safe. Inconclusive preserves uncertainty rather than converting it to success.

Repeatedly inspecting ordinary fixed-sample significance tests and stopping when favorable inflates error rates. Use a predeclared fixed horizon or a statistically valid sequential design. Multiple metrics and segments also increase false discoveries; reserve hard automatic actions for robust guardrails and use expert review for ambiguous evidence.

Confidence intervals and tests require assumptions about independence, stationarity, assignment, missingness, and metric distribution. State them. Operational decisions also weigh effect magnitude and harm: a statistically detectable 0.01 ms change may be irrelevant, while one proven duplicate charge is decisive.

**Advance in controlled stages.** A progression might be one instance with synthetic probes, 1% of low-risk stable users, 5% stratified traffic, 25%, 50%, then full rollout. Each stage has its own sample, duration, capacity, and error-budget limits. Evidence from earlier stages contributes only where assumptions remain.

Promotion changes the population and possibly dependency load, so re-evaluate after every expansion. A 5% canary does not establish behavior at full cache pressure or connection count. Hold at a stage when telemetry is absent or control is unhealthy.

**Handle noninteractive work.** For queues or pipelines, keep a work unit within one cohort across stages. Observe end-to-end completion and output quality, not just worker health. Canary duration must exceed work-unit duration. Use dry-run or two-phase mutation when effects can be compared before commit; otherwise choose reversible low-risk units and idempotent effects. Google's data-pipeline guidance emphasizes these adaptations [3].

For stateful protocols, allocate sessions or entities. For singleton operations, use fencing. For mobile or offline clients, candidate assignment and result latency may span days. For machine-learning models, distinguish operational safety from model-quality evaluation and data drift.

**Respond without false causality.** A guardrail breach justifies halting exposure. It does not prove the candidate caused the breach. Preserve candidate, control, routing, dependency, and telemetry evidence. If both degrade, investigate common cause. If only candidate degrades with comparable inputs, attribution strengthens.

Rollback must respect database and external effects. Stop new candidate admissions, drain bounded work, disable risky feature paths, reconcile state, and return traffic only to a compatible subject. Some failures require roll forward or incident containment instead of binary rollback.

**Automate conservatively.** The controller validates exact subjects, assignment policy, stage order, minimum samples, duration, guardrails, comparison, telemetry completeness, state compatibility, rollback readiness, and error-budget authorization. It serializes conflicting canaries and uses idempotent, generation-checked route changes.

Record hypotheses, metrics, thresholds, exclusions, stage exposure, actual cohorts, observations, decisions, actors, overrides, and limitations. Review false positives, false negatives, time to detection, escaped regressions, and user impact to recalibrate the policy without tuning it merely to pass releases.

## Definitions and Notation

Let $Z_i\in\{0,1\}$ assign exposure $i$ to control or candidate, $Y_i$ be its outcome, and $X_i$ relevant covariates. Causal comparison requires assignment and missingness assumptions; a raw difference $E[Y\mid Z=1]-E[Y\mid Z=0]$ is not automatically the candidate effect.

Let $p_0$ and $p_1$ be control and candidate failure probabilities and $\Delta=p_1-p_0$. Let $f$ be candidate traffic fraction, $\lambda$ total rate, and $T$ duration. Expected candidate exposures are $n\approx f\lambda T$ and candidate failures $fp_1\lambda T$ under a stationary homogeneous model.

For independent defect opportunity probability $p$, detection probability after $n$ exposures is

$$
P_{detect}=1-(1-p)^n.
$$

Dependence, uneven assignment, repeated users, and missing telemetry reduce the meaning of nominal $n$.

## Mechanisms, Invariants, or Proof Structure

**Exposure bound.** If at most fraction $f$ is routed to the candidate and enforcement is correct, candidate-caused request harm is bounded to that routed population for request-local effects. Shared resource exhaustion, corrupt state, and external side effects can violate the locality assumption.

**Rare-defect derivation.** Under independent identical opportunities, probability of no occurrence is $(1-p)^n$; its complement yields detection. Taking logarithms of $(1-p)^n\le1-q$ gives the sample bound because both logarithms are negative.

**Attribution counterexample.** Candidate runs only in a slower region and has higher latency. The observed difference combines subject and region, so it does not identify a candidate effect. Concurrent stratified allocation reduces this confound.

**Absolute-guardrail argument.** Equal candidate and control failure can arise from a shared dependency. Relative difference is zero while users are harmed, so comparison alone cannot authorize promotion.

**Executable canary policy.** The model checks sample, duration, telemetry, absolute guardrail, relative regression, error budget, and state compatibility. It is not a statistical test or traffic controller.

<!-- bijux-verify: {"id":"canary-decision-policy","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"healthy=promote\nlow_sample=hold:sample\nshort_duration=hold:duration\nmissing_telemetry=halt:telemetry\nabsolute_breach=halt:absolute\nrelative_breach=halt:regression\nbudget_breach=halt:budget\nincompatible_state=halt:state\nrare_defect_minimum=2995\nfive_percent_of_20_percent=0.010\n","stderr":""}} -->
```python
import math

def decide(sample, duration_min, telemetry, candidate_error, control_error,
           budget_spend, state_compatible=True):
    if not telemetry:
        return "halt:telemetry"
    if not state_compatible:
        return "halt:state"
    if candidate_error > 0.02:
        return "halt:absolute"
    if candidate_error - control_error > 0.003:
        return "halt:regression"
    if budget_spend > 0.10:
        return "halt:budget"
    if sample < 5000:
        return "hold:sample"
    if duration_min < 30:
        return "hold:duration"
    return "promote"

print(f"healthy={decide(8000, 45, True, 0.006, 0.005, 0.04)}")
print(f"low_sample={decide(900, 45, True, 0.006, 0.005, 0.04)}")
print(f"short_duration={decide(8000, 10, True, 0.006, 0.005, 0.04)}")
print(f"missing_telemetry={decide(8000, 45, False, 0.006, 0.005, 0.04)}")
print(f"absolute_breach={decide(8000, 45, True, 0.021, 0.020, 0.04)}")
print(f"relative_breach={decide(8000, 45, True, 0.010, 0.005, 0.04)}")
print(f"budget_breach={decide(8000, 45, True, 0.006, 0.005, 0.11)}")
print(f"incompatible_state={decide(8000, 45, True, 0.006, 0.005, 0.04, False)}")
n = math.ceil(math.log(1 - 0.95) / math.log(1 - 0.001))
print(f"rare_defect_minimum={n}")
print(f"five_percent_of_20_percent={0.05 * 0.20:.3f}")
```

## Alternatives and Trade-Offs

**Request versus entity allocation.** Requests produce samples quickly; entity allocation preserves state and experience. Choose the smallest stable unit that prevents harmful mixing.

**Random versus targeted population.** Random allocation supports general comparison. Targeted high-risk cohorts expose important paths sooner but limit generalization and may concentrate harm.

**Before/after versus concurrent control.** Before/after is simple but confounds time. Concurrent control improves attribution but shares dependencies and needs correct routing tags.

**Fixed horizon versus sequential evaluation.** Fixed designs simplify error reasoning but may react slowly. Valid sequential designs stop sooner while requiring explicit statistical machinery.

**Automatic versus reviewed promotion.** Automation is consistent for strong signals. Human review handles ambiguous trade-offs but can introduce delay and bias. Both use predeclared policy.

**Canary versus blue-green.** Canary limits initial exposure; blue-green prepares a complete alternate environment. They can be combined by sending a fraction to the prepared environment.

**Canary versus shadow.** Canary outputs are authoritative and expose users. Shadow traffic can compare safely only if effects are suppressed, but it cannot prove authoritative write behavior.

## Failure Modes and Misconceptions

- **“One percent means low risk.”** concentration and shared effects can create large harm.
- **“Replica ratio equals traffic ratio.”** connections and load skew invalidate it.
- **“Random means representative.”** rare important segments may be absent.
- **“More traffic always improves evidence.”** dependence and contamination limit information.
- **“No alert means pass.”** telemetry or sample may be missing.
- **“Candidate equals control, so healthy.”** both can violate absolute objectives.
- **“A significant result is important.”** effect magnitude and harm matter.
- **“A nonsignificant result proves equality.”** the evaluation may lack power.
- **“Check until green.”** repeated uncorrected looks inflate false decisions.
- **“Average latency is enough.”** tail and request mix can regress.
- **“Thirty minutes is representative.”** mechanism cycles determine duration.
- **“Rollback limits every effect.”** data and external actions may persist.
- **“A halt proves candidate guilt.”** it bounds exposure while preserving investigation.
- **“Canarying replaces pre-production tests.”** it spends real production risk.
- **“Automation removes judgment.”** policy encodes judgment and needs recalibration.

## Worked Examples

### Example 1

**Choose user allocation.** Per-request routing makes one shopping session alternate between incompatible carts. Hashing user identity keeps the workflow together. Conclusion: stable user allocation trades some sample independence for coherent behavior.

### Example 2

**Compute exposure cost.** At 10,000 requests/s, 5% candidate traffic, 20 minutes, and candidate failure probability 2%, expected candidate failures are $0.05\cdot10{,}000\cdot1{,}200\cdot0.02=12{,}000$. Conclusion: a “small” percentage can still spend substantial harm at scale.

### Example 3

**Detect a rare path.** A defect opportunity occurs in 0.1% of independent requests. For 95% probability of at least one occurrence, the bound requires 2,995 requests. Conclusion: 500 clean requests provide weak evidence about this path.

### Example 4

**Expose selection bias.** Green runs only on new hosts in a low-latency zone while control spans old hosts. Faster green latency cannot be attributed to code. Conclusion: balance or stratify infrastructure covariates.

### Example 5

**Use an absolute guardrail.** Control errors are 8% and candidate errors 7.5%; relative comparison favors candidate, but the SLO limit is 1%. Conclusion: hold the release and address the common incident.

### Example 6

**Reject a tiny p99.** Candidate receives 80 requests. The reported p99 is approximately one of the largest observations and has high uncertainty. Conclusion: wait for the declared tail sample rather than treating the dashboard label as stable evidence.

### Example 7

**Canary a queue.** Assign whole video jobs by stable job ID, keep every stage in its cohort, suppress final publication for a dry-run subset, and compare output plus end-to-end duration. Conclusion: worker CPU alone cannot evaluate pipeline correctness.

### Example 8

**Respond to missing data.** Candidate telemetry stops while user traffic continues. The controller halts new exposure and preserves current routing or returns safely; it does not interpret absence as zero errors. Conclusion: observability health is a guardrail.

### Example 9

**Avoid repeated peeking.** A team tests every minute with a fixed-horizon threshold and promotes at the first favorable result. This creates many chances for random success. Conclusion: use a fixed decision time or a valid sequential stopping rule.

### Example 10

**Handle irreversible writes.** A candidate emits malformed invoices. Routing rollback stops new candidate work but cannot retract issued invoices. The incident plan fences issuance, reconciles records, and applies compensation. Conclusion: canary scope must bound persistent effects, not merely compute.

## Cross-Program Connections

- **Statistics and Data Science:** sampling, power, intervals, sequential tests, and bias govern inference.
- **Testing and Quality Engineering:** pre-production tests, oracles, fault injection, and experiment design create complementary evidence.
- **Distributed Systems:** allocation, retries, queues, fencing, and shared dependencies affect contamination.
- **Platform Engineering:** routing, cohort identity, telemetry, and rollout controllers implement policy.
- **Database Engineering:** state compatibility and reconciliation determine rollback safety.
- **Security Engineering:** rare high-impact events and privileged cohorts require hard guardrails.
- **Data Engineering:** pipeline canaries need stable work units and end-to-end output comparison.
- **Software Architecture:** tenant boundaries, sessions, state ownership, and side effects define allocation.

## References

1. Google, [SRE Workbook, Chapter 16: “Canarying Releases”](https://sre.google/workbook/canarying-releases/), 2018; retrieved 2026-09-06.
2. Kubernetes Documentation, [“Managing Workloads”](https://kubernetes.io/docs/concepts/workloads/management/), current documentation retrieved 2026-09-06. Used only for the replica-based stable/canary example; routing guarantees remain mechanism-specific.
3. Google, [SRE Workbook, Chapter 13: “Data Processing Pipelines”](https://sre.google/workbook/data-processing/), 2018; retrieved 2026-09-06.
4. George Casella and Roger Berger, *Statistical Inference*, second edition, Duxbury, 2002. Used for probability and hypothesis-testing foundations.
5. David Siegmund, *Sequential Analysis: Tests and Confidence Intervals*, Springer, 1985. Used for sequential-decision cautions.
6. Ron Kohavi, Diane Tang, and Ya Xu, *Trustworthy Online Controlled Experiments*, Cambridge University Press, 2020. Used for allocation, guardrails, instrumentation, and experiment validity.
7. Jez Humble and David Farley, *Continuous Delivery*, Addison-Wesley, 2010, Chapters 10 and 12.
8. Google, [*Site Reliability Engineering*, Chapter 8: “Release Engineering”](https://sre.google/sre-book/release-engineering/), 2016; retrieved 2026-09-06.

## Exercises

### Exercise 1

Define canary, control, allocation unit, exposure, guardrail, contamination, false positive, and false negative. Explain why “no alert” is not a promotion criterion.

### Exercise 2

A service receives 5,000 requests/s. A 4% canary runs for 15 minutes with candidate failure probability 1.5%. Compute expected candidate exposures and failures under the simple model.

### Exercise 3

A candidate is faster, but it runs only in one quiet region on new hardware and receives unauthenticated reads while control handles all writes. Diagnose the inference defects and redesign allocation.

### Exercise 4

Compare fixed-horizon and sequential canary evaluation across detection delay, false-decision control, operational simplicity, repeated observation, and emergency guardrails.

### Exercise 5

Design a canary for a monthly payroll pipeline with large tenants, irreversible bank submissions, a six-hour work unit, and rare jurisdiction rules. Define unit, population, effects, duration, metrics, stopping, and promotion.

## Answers to the Exercises

### Answer 1

A canary is partial time-bounded candidate exposure; control is the accepted comparator; allocation unit is the stable assigned entity; exposure is work and harm placed at risk; a guardrail is an absolute stop condition; contamination mixes subjects or effects; a false positive rejects a sound candidate; a false negative promotes a harmful one. No alert may mean no defect, insufficient traffic, missing telemetry, wrong metrics, delayed behavior, or an insensitive threshold. Promotion requires positive evidence of sample, duration, telemetry completeness, guardrails, compatibility, and declared comparisons.

### Answer 2

Duration is $15\cdot60=900$ seconds. Candidate exposures are $0.04\cdot5{,}000\cdot900=180{,}000$. Expected candidate failures are $180{,}000\cdot0.015=2{,}700$. These expectations assume stationary homogeneous traffic and do not give a deterministic failure count or candidate-attributable excess over control.

### Answer 3

Region, hardware, authentication, and operation type all confound subject with treatment, so latency difference does not identify code effect and writes are untested. Run candidate and control concurrently within comparable region/hardware strata, deterministically assign stable users or sessions, preserve authentication and operation mix, and record assignment plus actual handler. If writes are too risky, label read-only evidence narrowly and add a separate bounded, compatible write canary before general promotion.

### Answer 4

A fixed-horizon design declares sample and decision time, simplifying error-rate reasoning but potentially waiting after a clear regression. An ordinary fixed test cannot be peeked at repeatedly without changing its false-positive behavior. A valid sequential design declares interim looks, boundaries, and stopping rules, often detecting large effects sooner but requiring more statistical and operational machinery. Neither delays hard correctness, security, or SLO guardrails: those halt immediately under predeclared policy. Promotion still requires practical effect assessment and state compatibility.

### Answer 5

Use a whole payroll run for a stable tenant as the unit; never split one payroll across subjects. Select several small, consenting or internally controlled tenants plus synthetic cases stratified by jurisdiction, while separately exercising rare-rule fixtures. Candidate performs the full six-hour computation but writes proposed payments to an isolated ledger or two-phase pending state; it cannot submit to banks. Compare employee counts, gross-to-net conservation, taxes, rounding, jurisdiction outcomes, runtime, retries, and ledger reconciliation against control. Duration covers complete runs and delayed validation. Any invariant mismatch, missing output, telemetry gap, or budget breach halts. Human payroll review authorizes a narrowly fenced first real submission only after dry-run evidence; idempotency keys prevent duplicates. Broader promotion requires representative large tenants and every required jurisdiction, not merely a percentage of rows.
