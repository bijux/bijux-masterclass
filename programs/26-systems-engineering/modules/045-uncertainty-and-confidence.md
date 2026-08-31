---
module_id: SYSENG-045
program: Systems Engineering
level: 1
module_number: 45
title: Uncertainty and Confidence
status: complete
last_verified: 2026-08-31
---

# Uncertainty and Confidence

## One-Page Review

### Governing question

What is unknown or variable about a system claim, what evidence and assumptions support its quantified range, and what—precisely—does a stated confidence level permit a decision maker to conclude?

### Essential definitions

- **Uncertainty** is incomplete knowledge or variability affecting descriptions, measurements, models, forecasts, outcomes, or decisions.
- **Aleatory variability** denotes modeled variation inherent in the represented process; **epistemic uncertainty** denotes limited knowledge. The distinction is conditional on boundary, information, and intended action—not a permanent property of a number.
- A **measurand** is the particular quantity intended to be measured, including conditions and definition needed to interpret it.
- **Measurement uncertainty** is a parameter describing dispersion reasonably attributable to a measurement result; it is not automatically the error from an unknowable true value.
- **Standard uncertainty** is expressed like a standard deviation. **Combined standard uncertainty** propagates components, including covariance. **Expanded uncertainty** is (U=ku_c) with stated coverage factor (k) and basis.
- A **frequentist confidence interval** is produced by a procedure whose long-run coverage has a declared level under repeated data generation and model assumptions; after observation, the fixed parameter is not assigned that frequentist probability.
- A **Bayesian credible interval** contains a declared posterior probability conditional on likelihood, prior/model, data, and computation.
- A **prediction interval/distribution** concerns a future or unobserved outcome, including process variability and parameter uncertainty as modeled; it is not a parameter interval.
- A **tolerance interval** aims to contain a stated proportion of a population with stated confidence under its assumptions.
- A **confidence level (cost/schedule)** often denotes simulated probability of meeting a threshold under a forecast model, not statistical confidence in a parameter estimate.
- **Calibration** evaluates whether stated probabilities or intervals achieve appropriate frequencies on relevant cases; **sharpness/precision** describes concentration and is valuable only with calibration/validity.
- **Model-form uncertainty** concerns inadequacy among equations, structure, boundary conditions, algorithms, or representations, not merely uncertain parameter values.
- **Decision confidence** is a bounded judgment about robustness and evidence sufficiency for an action; it must not be manufactured by averaging unrelated confidence numbers.

### Central model, mechanism, or theorem

For measured/model inputs (X) with covariance matrix (\Sigma) and output (Y=f(X)), first-order uncertainty propagation near (x) is

$$
u_c^2(Y)\approx \nabla f(x)^T\Sigma\nabla f(x).
$$

This is a local approximation and depends on model adequacy, differentiability, input uncertainty, and covariance. Simulation or other methods may be needed for nonlinearity, discontinuity, tails, or non-Gaussian/dependent inputs.

For a binomial proportion with (k) successes in (n) independent representative trials, (\hat p=k/n), the Wilson interval with normal quantile (z) is

$$
\frac{\hat p+z^2/(2n)\ \pm\ z\sqrt{\hat p(1-\hat p)/n+z^2/(4n^2)}}{1+z^2/n}.
$$

Its coverage is a property of the procedure under the sampling model, not a certificate that future operational success lies in the interval. Dependence, nonrepresentative conditions, definition changes, and model discrepancy can dominate sampling uncertainty.

### Critical invariants

- Every uncertainty statement names the quantity/claim, system configuration, population/scenario, lifecycle state, data date, unit, threshold, and decision use.
- Sources are inventoried across measurement, sampling, process variability, parameters, model form, scenarios, human/organizational behavior, suppliers, operations, preferences, and unknown exclusions.
- Classification as aleatory/epistemic states the boundary and action; reducibility is tested rather than assumed.
- Statistical intervals state procedure/interpretation, assumptions, sample design, confidence/credibility/coverage level, sidedness, and multiplicity where relevant.
- Measurement results state measurand, corrections, uncertainty components, covariance, propagation, coverage factor, and probability/coverage basis if asserted.
- Forecast distributions preserve dependence, common cause, conditional scenarios, constraints, model validity, and structural alternatives.
- Data are representative of the intended population/environment/configuration or the transfer/extrapolation gap is explicit.
- Zero observed failures, narrow intervals, high model fit, or many simulations do not establish absence of rare/common-mode or omitted failures.
- Parameter, prediction, tolerance, measurement, forecast, and decision confidence are never substituted for one another.
- Confidence is calibrated/backtested where possible and widened or qualified for model discrepancy, selection, drift, and extrapolation.
- Evidence quality, independence, traceability, relevance, and contradictory results accompany numerical uncertainty.
- Decision reporting shows threshold probabilities, consequences, sensitivity, robust alternatives, information value, residual ignorance, dissent, and reopening triggers.

### Common failures

Common failures include writing “95% confident” without naming the quantity or semantics; interpreting a confidence interval as 95% probability the fixed parameter is inside; treating a credible interval as prior-free; using a parameter interval to predict an individual outcome; confusing standard deviation, standard error, expanded uncertainty, tolerance, and specification limits; assuming (k=2) always means 95%; omitting covariance; replacing model-form uncertainty with wider parameter distributions; fitting and validating on the same data; treating test conditions as operationally representative; using zero failures to claim perfect reliability; assuming trials are independent when common causes exist; assigning unjustified distributions to ignorance; mixing probabilities from different baselines; reporting marginal P50 cost/date as joint P50; ignoring multiple comparisons and selection; counting simulations as evidence; and compressing uncertainty into a red/yellow/green color.

### Compact example

In 100 declared independent representative trials, 80 succeed. The estimate is 0.800. A symmetric normal/Wald 95-percent interval is [0.7216, 0.8784]; a Wilson interval using (z=1.96) is about [0.7112, 0.8666]. The methods differ because finite-sample interval construction matters. Neither interval covers model discrepancy, dependence, changed configuration, untested environments, severity, or future drift. “80% ± something” is meaningful only after those limits are stated.

### Connections

SYSENG-041–044 define preferences, trade studies, integrated forecasts, and sensitivity drivers. This module governs how uncertainty and confidence are expressed. SYSENG-046–048 apply evidence to readiness and risk; SYSENG-049–050 preserve rationale and select architectures under bounded knowledge. Verification, validation, technical assessment, configuration, and operational learning continually update these claims.

## Governing Question

When a report states “95 percent,” does it mean coverage of a measurement interval, confidence-procedure coverage for a parameter, posterior probability under a Bayesian model, population content with confidence, forecast probability of meeting cost/date, simulated mission success, or a reviewer’s qualitative confidence? What evidence justifies that interpretation and what uncertainty remains outside it?

The number alone cannot answer. Systems engineering combines physical variability, incomplete knowledge, sparse tests, heterogeneous populations, models, expert judgments, supplier claims, human behavior, and changing configurations. Each supports different mathematics and different decisions. Confidence becomes useful only when its object, semantics, evidence, and limits are explicit.

## Why This Matters

False precision can create unsafe requirements, underfunded programs, brittle architectures, unfair impacts, and irreversible commitments. Excessive vagueness can be equally harmful: “anything may happen” provides no basis for margin, test planning, reserve, monitoring, or choice. The goal is calibrated specificity—quantify what evidence supports, preserve what it does not, and connect uncertainty to action.

NASA's current Risk Management Handbook defines uncertainty broadly as imperfect knowledge or physical variability and treats risk analysis as one input to deliberative risk-informed decisions. NASA Decision Analysis requires uncertainty characterization and asks whether reducing uncertainty could credibly change a ranking. NASA modeling and simulation credibility guidance requires documented model credibility and robustness rather than treating numerical output as ground truth.

NIST measurement guidance requires uncertainty components, methods, degrees of freedom where appropriate, combined uncertainty, coverage factor, and the basis for any probability/confidence interpretation. GAO cost guidance requires risk/uncertainty analysis tied to the technical baseline and updates with actual evidence. NASA joint cost/schedule guidance maps risks and uncertainty into linked models. Across these contexts, the same percentage can have different semantics; disciplined reporting prevents accidental substitution.

## Prerequisites and Retrieval

Before continuing, retrieve:

1. exact system claim, configuration, population/environment, lifecycle phase, decision threshold, consequence, authority, deadline, and reversibility;
2. measurement/test definitions, sampling plan, inclusion/exclusion, instrumentation/calibration, corrections, censoring/missingness, data lineage, and raw observations;
3. physical/statistical/forecast models, parameters, priors where used, boundary/initial conditions, structural alternatives, code/version, and verification/validation evidence;
4. uncertainty/risk register with sources, dependence/common cause, scenarios, distributions/intervals, evidence, reducibility, owners, and information actions;
5. requirements/allocations/margins, cost-loaded schedule, technical measures, operational profiles, human/supplier factors, and historical calibration;
6. probability, conditional probability, likelihood, sampling, descriptive statistics, interval estimation, covariance, propagation, simulation, and sensitivity basics;
7. review roles including domain, statistics/metrology, modeling, safety/security, human factors, operations, ethics, affected stakeholders, and decision authority as applicable.

As a retrieval test, challenge “availability is 99.9% with 95% confidence.” Ask whether availability is time, demand, user, function, or site based; observation horizon; planned exclusions; independent events/common causes; repair/censoring; configuration and load; parameter or future-service interval; statistical method; and whether 99.9 is estimate, lower bound, requirement, or contractual objective. Without those answers, the statement cannot guide design or acceptance.

## Learning Objectives

After completing this module, you should be able to:

1. inventory uncertainty sources and state their boundary, evidence, dependence, and reducibility;
2. distinguish aleatory variability from epistemic uncertainty without treating the labels as absolute;
3. distinguish measurement, confidence, credible, prediction, tolerance, and forecast intervals/probabilities;
4. calculate and interpret a Wilson interval and zero-failure reliability bound under declared assumptions;
5. propagate measurement/model input uncertainty with sensitivity coefficients and covariance;
6. identify sampling, selection, multiplicity, distribution, dependence, extrapolation, and model-form limits;
7. build coherent joint scenarios and avoid false independence or double counting;
8. assess calibration, sharpness, validation, and evidence relevance;
9. design uncertainty-reducing evidence actions by decision value;
10. communicate decision confidence with explicit unknowns, thresholds, consequences, dissent, and reopening triggers.

## Core Exposition

**Define the claim before its uncertainty.** Specify quantity, unit, system/configuration, population/scenario, operating conditions, time horizon, data date, estimator/model, threshold, and intended decision. “Reliability,” “cost,” or “performance” can have many denominators and boundaries. Uncertainty around an undefined claim is not rigorous.

**Create an uncertainty inventory.** Include measurement resolution/calibration/drift/bias, sampling, missing/censored data, natural/process variability, parameter estimation, model form, discretization/numerics, boundary/initial conditions, environment/operations, human behavior, suppliers, schedule/resources, risk events, preference/value models, data transformations, configuration change, and unmodeled/unknown mechanisms. Map each source to QoIs and decisions.

**Use aleatory/epistemic labels as modeling decisions.** Weather variability may be aleatory for one launch decision but reducible through better near-term forecast for another. Manufacturing variation may be controlled through process change. A “known distribution” still has parameter/model uncertainty. Record boundary, time horizon, potential information/control, and why a representation is appropriate.

**Separate uncertainty from error and tolerance.** Error is difference between a measurement and a reference/true quantity when meaningfully available; uncertainty characterizes doubt/dispersion attributed to the result. A specification tolerance is an allowed product range, not measurement uncertainty. Accuracy, bias, precision, repeatability, reproducibility, resolution, and uncertainty are related but not synonyms.

**Build a measurement uncertainty budget.** Define measurand and measurement equation; correct known significant effects; list Type A components evaluated statistically and Type B components evaluated by other information; convert to standard uncertainties; identify sensitivity coefficients and covariance; combine them; evaluate degrees of freedom/coverage factor as applicable; and report result with unit, uncertainty, (k), and basis. Type A does not mean random and Type B systematic; the labels describe evaluation method.

**Propagate covariance.** For (Y=f(X)), the gradient-covariance relation includes cross terms. Shared calibration, environment, processing, or reference standards make covariance nonzero. Omitting positive covariance can understate uncertainty; negative covariance can reduce it in a particular combination. Estimate dependence from paired data, physical structure, or bounded scenarios, and disclose weak evidence.

**Know frequentist interval semantics.** A 95-percent confidence procedure is designed so that, under assumptions and repeated sampling, approximately 95 percent of constructed intervals cover the fixed parameter. For the observed interval, frequentist language does not assign a 0.95 probability to that fixed parameter. Coverage may be approximate/discrete and can degrade after optional stopping, selection, misspecification, dependence, or nonrepresentative sampling.

**Use intervals suited to the data.** The simple Wald interval (\hat p\pm z\sqrt{\hat p(1-\hat p)/n}) performs poorly near 0/1 or with small samples and can yield impossible bounds. Wilson or exact methods have different coverage/width properties. State sidedness: reliability acceptance often needs a one-sided lower bound, not a symmetric interval. Predefine the method rather than select the most favorable after observation.

**Know Bayesian interval semantics.** A Bayesian posterior follows

$$
p(\theta\mid D,M)\propto p(D\mid\theta,M)p(\theta\mid M).
$$

A 95-percent credible interval contains 95 percent posterior probability conditional on model, prior, data, and computation. Inspect prior sensitivity, likelihood/model discrepancy, identifiability, convergence, and predictive calibration. A posterior can be narrow and wrong under a poor model.

**Distinguish parameter and prediction uncertainty.** Estimating a mean response becomes more precise with data; predicting one future observation still includes process variability. Forecast a new supplier delivery, patient outcome, component life, or incident using a predictive distribution appropriate to its population and dependencies. A narrow parameter interval is not a narrow outcome interval.

**Use tolerance intervals for population coverage.** A tolerance interval aims to cover a stated population proportion with stated confidence. It answers neither the confidence interval for a mean nor the prediction interval for a single observation. Distribution-free and parametric methods have different data needs and assumptions; heterogeneous subpopulations may invalidate pooled coverage.

**Represent model-form uncertainty.** Compare plausible structures, fidelities, boundary conditions, failure logic, datasets, algorithms, and lifecycle assumptions. Validation residuals and out-of-sample discrepancies can inform model inadequacy but may not extrapolate. Do not force all structural ignorance into a convenient normal parameter. Use ensembles, discrepancy terms, scenario envelopes, robust bounds, or explicit unresolved alternatives with justified semantics.

**Validate in the intended context.** Verification asks whether equations/code are solved/implemented correctly; validation asks whether the model adequately represents the real system for the intended use. Match configurations, regimes, scales, populations, and QoIs. Separate calibration/training from validation, preserve blind/holdout evidence when possible, and scrutinize thresholds/tails where the decision lies.

**Assess calibration and sharpness.** Across comparable cases, do 90-percent intervals cover near 90 percent, and do probability forecasts correspond to observed frequencies? Stratify by regime/group/time; aggregate calibration can hide local failure. Prefer narrower forecasts only among adequately calibrated/valid ones. Use proper scoring and residual diagnostics when appropriate, but no score replaces domain validity.

**Model joint outcomes.** Cost, date, performance, safety, reliability, and stakeholder impacts share causes. Preserve correlation and conditional scenarios. Marginal 70-percent confidence in cost and date does not imply 70-percent joint confidence, nor generally 49 percent. Combine only outputs from compatible baselines and samples.

**Address sparse and zero-failure evidence.** With zero failures in (n) independent representative Bernoulli demands, a one-sided exact lower confidence bound for success probability is

$$
R_L=\alpha^{1/n}
$$

at confidence (1-\alpha). For 100 tests and (\alpha=0.05), (R_L\approx0.9705), not 1. This says nothing about untested failure modes, dependence, mission duration, severity, or changed configuration. Rare/common-cause claims need stronger evidence and modeling.

**Account for selection and multiplicity.** Inspecting many measures and reporting only the most favorable interval biases confidence. Multiple comparisons raise the chance of at least one false signal. Predefine primary claims, adjust or control error where relevant, report all material analyses, and distinguish exploratory from confirmatory evidence.

**Elicit expert judgment structurally.** Define quantities/scenarios, train on probability concepts and biases, elicit quantiles/probabilities individually before discussion, request rationale/evidence, test coherence, preserve disagreement, and calibrate/weight only under a defensible protocol. Consensus is not automatically accuracy; do not hide dissent in an average distribution.

**Update with new evidence under change control.** Record prior estimate/model, incoming evidence, configuration, method, result, effect on uncertainty and decision, and remaining conflicts. Bayesian or frequentist updating still requires compatible data-generating conditions. If the system or population changed, model that change rather than treating all observations as exchangeable.

**Distinguish information from mitigation.** A test may reduce epistemic uncertainty but cannot remove inherent variability; a redesign may change the outcome distribution without increasing knowledge; a monitor may reveal state before action; reserve absorbs consequences. Compare cost, schedule, risk, ethics, and decision value. More information is useful when it can change or condition action before commitment.

**Construct decision confidence deliberately.** Combine technical evidence through an explicit risk/decision model and deliberation; do not average “80% model confidence,” “90% supplier confidence,” and “95% test confidence.” Show probability/range of outcomes, threshold and consequence, sensitivity, model/evidence credibility, alternative robustness/regret, controllability, and stakeholder preferences. Decision authority owns acceptance.

**Communicate layered uncertainty.** Report point/central estimate only with interval/distribution/scenarios, semantics, assumptions, data/model identity, dependence, validation/calibration, tail/threshold results, evidence gaps, contradictions, affected groups, and triggers. Use frequencies or natural counts when they improve understanding. Avoid decimals unsupported by evidence.

**Preserve residual ignorance.** “Unknown unknowns” cannot receive a verified distribution by declaration. Use architectural resilience, defense in depth, margins/reserves, monitoring, diversity, graceful degradation, safe states, staged/reversible commitments, anomaly investigation, and learning. State what the quantitative model excludes.

The following checker compares two binomial interval procedures and a one-sided zero-failure bound under their declared sampling assumptions.

<!-- bijux-verify: {"id":"binomial-confidence-check","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"estimate=0.8000\nwald_low=0.7216\nwald_high=0.8784\nwilson_low=0.7112\nwilson_high=0.8666\nzero_failure_lower_n100=0.9705\nwald_one_of_one_low=1.0000\nwald_one_of_one_high=1.0000\nwilson_one_of_one_low=0.2065\nwilson_one_of_one_high=1.0000\nevidence=declared_binomial_models_only\n","stderr":""}} -->
```python
from math import sqrt

def wald(k, n, z=1.96):
    p = k / n
    half = z * sqrt(p * (1 - p) / n)
    return p - half, p + half

def wilson(k, n, z=1.96):
    p = k / n
    denominator = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denominator
    half = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denominator
    return center - half, center + half

k, n = 80, 100
w_low, w_high = wald(k, n)
u_low, u_high = wilson(k, n)
bad_low, bad_high = wald(1, 1)
one_low, one_high = wilson(1, 1)
print(f"estimate={k / n:.4f}")
print(f"wald_low={w_low:.4f}")
print(f"wald_high={w_high:.4f}")
print(f"wilson_low={u_low:.4f}")
print(f"wilson_high={u_high:.4f}")
print(f"zero_failure_lower_n100={0.05 ** (1 / 100):.4f}")
print(f"wald_one_of_one_low={bad_low:.4f}")
print(f"wald_one_of_one_high={bad_high:.4f}")
print(f"wilson_one_of_one_low={one_low:.4f}")
print(f"wilson_one_of_one_high={one_high:.4f}")
print("evidence=declared_binomial_models_only")
```

The one-of-one Wald interval collapses to `[1,1]`, illustrating why an easy formula can be profoundly misleading at a boundary. Wilson is not a remedy for nonrepresentative or dependent tests.

## Definitions and Notation

Let claim quantity (Q), data (D), system/configuration (B), operating population/scenario (S), model (M), parameters (\theta), evidence (E), and decision threshold (L).

A complete uncertainty assertion can be represented as

$$
U_Q=(Q,B,S,D,M,E,\mathcal{I},\gamma,A),
$$

where (\mathcal{I}) is interval/distribution/scenario representation, (\gamma) its declared probability/coverage semantics if any, and (A) assumptions/applicability. Omitting these fields makes reuse unsafe.

For independent standard-uncertainty components, the first-order special case is

$$
u_c(Y)=\sqrt{\sum_i c_i^2u^2(X_i)},\qquad c_i=\frac{\partial f}{\partial X_i}.
$$

With covariance:

$$
u_c^2(Y)=\sum_ic_i^2u_i^2+2\sum_{i<j}c_ic_ju_{ij}.
$$

Expanded uncertainty is (U=ku_c); (k) alone does not guarantee coverage without distribution/degrees-of-freedom/basis.

For a future outcome (Y_{new}), predictive inference is

$$
p(Y_{new}\mid D,M)=\int p(Y_{new}\mid\theta,M)p(\theta\mid D,M)d\theta
$$

in a Bayesian representation; it retains outcome variability and parameter uncertainty conditional on model.

For joint commitments:

$$
P_J=Pr(C\le C^*,T\le T^*,P\ge P^*\mid B,M,E,A),
$$

explicitly conditional on baseline, model, evidence, and assumptions.

## Mechanisms, Invariants, or Proof Structure

**Mechanism 1—claim definition.** Fix quantity, baseline, population/scenario, horizon, threshold, consequence, evidence date, and decision.

**Mechanism 2—uncertainty inventory and representation.** Identify sources, dependence, reducibility/control, evidence, structural alternatives, and justified intervals/distributions/scenarios.

**Mechanism 3—quantification.** Use measurement budgets, sampling intervals, Bayesian/posterior prediction, propagation, simulation, bounds, or structured scenarios with exact semantics and assumptions.

**Mechanism 4—credibility challenge.** Verify computation; review representativeness, model form, dependence, selection, multiplicity, validation, calibration, extrapolation, and contradictory evidence.

**Mechanism 5—decision and learning.** Compare thresholds/consequences, robustness and information value; choose action/mitigation/monitoring/reserve; preserve residual ignorance and reopening triggers.

Quantification is conditional. More data can reduce sampling or parameter uncertainty but cannot automatically correct bias, model form, population shift, dependence, omitted hazards, or illegitimate objectives.

## Alternatives and Trade-Offs

**Frequentist methods** offer repeated-sampling error guarantees under assumptions. **Bayesian methods** directly express conditional probability about parameters/predictions but require priors and full model scrutiny.

**Parametric intervals** can be efficient with a valid distribution. **Nonparametric/resampling methods** reduce some distribution assumptions but still need representative/dependence-aware data and may struggle in tails/small samples.

**Analytic propagation** is transparent and fast locally. **Monte Carlo/numerical propagation** handles nonlinearity and complex distributions but adds computation and does not cure model misspecification.

**Probability distributions** enable expectation/quantile decisions when evidence supports them. **Intervals, possibility structures, and scenario sets** avoid false precision under deep uncertainty but support different decision rules.

**More testing** reduces some uncertainty but costs time/resources and may create ethical/safety exposure. **Robust or adaptive design** can reduce sensitivity to uncertainty without estimating it precisely.

**Pooled evidence** increases sample size. **Stratified/hierarchical evidence** preserves group/context differences but needs more modeling and data. Pool only when exchangeability is defensible.

**One model** simplifies communication. **Model ensembles/scenarios** expose structural uncertainty but need rules that avoid treating arbitrary model counts as probabilities.

## Failure Modes and Misconceptions

**“Uncertainty is just standard deviation.”** It includes sampling, bias, model form, scenarios, dependence, extrapolation, and ignorance beyond a single dispersion measure.

**“95% confidence means a 95% chance the parameter is inside.”** That is not the frequentist interpretation; a Bayesian interval may have posterior probability under stated prior/model.

**“Prediction interval and confidence interval are interchangeable.”** One concerns future outcomes; one often concerns a parameter such as a mean.

**“k=2 means 95%.”** Coverage depends on distribution, degrees of freedom, method, and stated basis.

**“No failures means 100% reliable.”** Finite representative tests yield a bound under assumptions and cannot cover untested/common-mode failures.

**“Monte Carlo trials are evidence.”** They explore a model; empirical evidence supports inputs and model validity.

**“Independent estimates can be multiplied.”** Only compatible events under justified dependence permit a joint probability calculation.

**“A narrow interval proves accuracy.”** It can be precisely biased, misspecified, selected, or extrapolated.

**“Aleatory uncertainty cannot be reduced.”** Control, conditioning, boundary change, or new observables can alter what is variable; labels are contextual.

**“Decision confidence is one computed percentage.”** It combines modeled outcomes with credibility, values, consequences, constraints, and deliberative authority.

## Worked Examples

### Example 1

**Wilson versus Wald.** With 80/100 successes, the embedded checker produces differing approximate 95-percent intervals. Report selected procedure and assumptions; do not choose the narrower/favorable interval after observing data.

### Example 2

**One success is weak evidence.** One of one passes. Wald gives `[1,1]`; Wilson gives about `[0.2065,1]`. Neither covers nonrepresentative test conditions. A perfect observed fraction is not perfect demonstrated reliability.

### Example 3

**Measurement uncertainty with covariance.** Output (Y=X_1-X_2), standard uncertainties both 2, covariance +3. Then variance is (4+4-2(3)=2), so (u_c=\sqrt2). If covariance were ignored, (u_c=\sqrt8). Dependence and subtraction sign matter; validate covariance evidence.

### Example 4

**Parameter versus prediction.** A large dataset estimates average repair time precisely, but individual repairs still vary widely by fault, technician, parts, and environment. Staffing needs the predictive workload distribution and dependencies, not only a confidence interval for the mean.

### Example 5

**Zero-failure bound.** One hundred independent representative demands with no failure give a 95-percent one-sided lower reliability bound about 0.9705. This cannot substantiate 0.99999, common-cause resilience, long-duration operation, or a modified design.

### Example 6

**Model-form disagreement.** Two validated-in-range thermal models agree nominally but diverge near a phase change. Treat model structure/regime as a factor, gather boundary evidence, and use a conservative/robust decision; widening one model's parameter standard deviation may not represent the discontinuity.

### Example 7

**Marginal versus joint confidence.** Cost meets its cap in 70 percent of coherent simulations and date in 70 percent, but both may meet in 55 percent due to dependence. Neither 70 nor 49 percent follows as joint confidence without joint samples/model.

### Example 8

**Selection bias.** A team tests 30 configurations and reports only the one with the best sample reliability and its unadjusted interval. The selection process makes that interval optimistic. Separate exploration, confirm the selected configuration on new evidence, and report multiplicity.

### Example 9

**Expert disagreement.** Safety experts give materially different tail probabilities because their failure boundaries differ. Preserve individual rationales and models, resolve definition/evidence gaps, and analyze decisions across judgments; averaging can erase a credible adverse mechanism.

### Example 10

**Reopening after drift.** Operational workload shifts beyond validation data. The team flags applicability breach, recalibrates/validates, updates predictive and subgroup intervals, assesses incidents and decisions, preserves the old claim/configuration, and reopens acceptance rather than silently updating a dashboard.

## Cross-Program Connections

**Platform engineering.** Capacity, adoption, SLO, cloud cost, team productivity, incident and migration forecasts require workload/population definitions, tails, dependence, drift, and calibrated operational evidence.

**API and service engineering.** Latency/availability/error predictions need request/dependency correlation, version/configuration, retry/common cause, censored telemetry, and future-load prediction rather than confidence in an average only.

**Data engineering.** Quality/freshness/completeness claims depend on sampling, missing-not-at-random data, lineage, schema changes, late data, distributions, subgroup coverage, and model drift.

**Object-oriented programming.** Defect/change/performance evidence depends on codebase/team/workload/test populations and selection; narrow benchmark intervals do not establish architectural maintainability.

**Functional programming.** Type/effect claims, concurrency, performance, ecosystem and migration evidence must separate formal guarantees from assumptions, empirical variability, modeling, and organizational uncertainty.

## References

1. NIST, *Technical Note 1297: Guidelines for Evaluating and Expressing the Uncertainty of NIST Measurement Results*, current web edition. <https://www.nist.gov/pml/nist-technical-note-1297>
2. NIST, *Technical Note 1297, Section 7: Reporting Uncertainty*. <https://www.nist.gov/pml/nist-technical-note-1297/nist-tn-1297-7-reporting-uncertainty>
3. NIST, *Technical Note 1297, Appendix A: Law of Propagation of Uncertainty*. <https://www.nist.gov/pml/nist-technical-note-1297/nist-tn-1297-appendix-law-propagation-uncertainty>
4. NASA, *Risk Management Handbook Version 2.0, Part 1*, NASA/SP-20240014019, 2024. <https://ntrs.nasa.gov/citations/20240014019>
5. NASA, *Risk Management Handbook Version 2.0, Part 2*, NASA/SP-20240014326, 2024. <https://ntrs.nasa.gov/citations/20240014326>
6. NASA, *NASA Risk-Informed Decision Making Handbook*, NASA/SP-2010-576. <https://ntrs.nasa.gov/citations/20100021361>
7. NASA, *Systems Engineering Handbook, Section 6.8: Decision Analysis*, current web edition. <https://www.nasa.gov/reference/6-8-decision-analysis/>
8. NASA, *NASA-HDBK-7009A: Handbook for Models and Simulations*, 2019. <https://standards.nasa.gov/sites/default/files/standards/NASA/A/0/nasa-hdbk-7009a.pdf>
9. U.S. GAO, *Cost Estimating and Assessment Guide*, GAO-20-195G. <https://www.gao.gov/products/gao-20-195g>
10. NASA, *Cost Estimating Handbook, Appendix J: Joint Cost and Schedule Confidence Level Analysis*. <https://www.nasa.gov/wp-content/uploads/2020/11/ceh_appj.pdf>

## Exercises

### Exercise 1

For 45 successes in 50 independent representative trials, compute the estimate and approximate 95-percent Wald and Wilson intervals using (z=1.96). Interpret them correctly and list important uncertainty they exclude.

### Exercise 2

For measurement model (Y=2X+Z), standard uncertainties (u_X=1.5), (u_Z=2), and covariance (u_{XZ}=1), compute combined standard uncertainty by first-order propagation. Compare with the independence assumption and explain the sign of the covariance contribution.

### Exercise 3

A component has zero failures in 200 independent representative demands. Compute the one-sided 95-percent lower reliability bound. Determine how many zero-failure demands are required to demonstrate a lower bound of at least 0.99 under the same idealized model.

### Exercise 4

Critique a report stating: “The design is safe with 99% confidence because 10,000 Monte Carlo runs produced only 100 failures. All inputs were independent normal distributions chosen by experts; the model was calibrated and validated on the same 20 tests; runs outside solver limits were discarded.” Design a corrective assessment.

### Exercise 5

Design an uncertainty and confidence case for an autonomous ferry operating in fog, ice, mixed traffic, communications loss, and human takeover. Cover claims, populations/scenarios, measurements, tests, model form, dependence, rare/common causes, human factors, calibration/validation, confidence semantics, evidence actions, decision authority, residual ignorance, and reopening.

## Answers to the Exercises

### Answer 1

(\hat p=45/50=0.90). Wald standard error is

$$
\sqrt{0.9(0.1)/50}=0.04243,
$$

so the approximate interval is

$$
0.90\pm1.96(0.04243)=[0.8168,0.9832].
$$

Wilson has denominator (1+1.96^2/50=1.076832), center

$$
(0.90+1.96^2/100)/1.076832\approx0.87146,
$$

and half-width about 0.08506, giving approximately `[0.7864,0.9565]` (minor last-digit differences can result from rounding intermediate values).

These are intervals from procedures under the binomial independent representative-trial model; 95 percent describes procedure coverage, not posterior probability for the fixed success probability. They exclude population/configuration mismatch, dependence/common causes, environmental/human variation not represented, measurement/misclassification, selection/stopping, model change/drift, severity, and untested failure modes. A one-sided lower bound may better fit an acceptance decision.

### Answer 2

Sensitivity coefficients are (c_X=2) and (c_Z=1). Including covariance:

$$
u_c^2(Y)=2^2(1.5^2)+1^2(2^2)+2(2)(1)(1)=9+4+4=17,
$$

so

$$
u_c(Y)=\sqrt{17}\approx4.123.
$$

Assuming independence removes the cross term, giving (\sqrt{13}\approx3.606). Positive covariance increases uncertainty because both coefficients have the same sign: shared positive movement reinforces (Y). For a subtractive model or negative covariance, the cross contribution can reduce variance. This calculation assumes first-order propagation and credible covariance; it does not validate linearity, distributions, or the measurement model.

### Answer 3

For (n=200) and (\alpha=0.05),

$$
R_L=0.05^{1/200}=\exp(\ln(0.05)/200)\approx0.98513.
$$

To require (R_L\ge0.99), solve

$$
0.05^{1/n}\ge0.99.
$$

Taking logs (both negative) gives

$$
n\ge\frac{\ln(0.05)}{\ln(0.99)}\approx298.07.
$$

Thus at least 299 zero-failure independent representative demands are required under this model. The bound does not cover dependence, demand heterogeneity, censoring, changed configuration, common causes, untested modes, or mission-duration scaling.

### Answer 4

The 1-percent simulated failure fraction is an estimate conditional on the model/input distributions, not “99% confidence” that the real design is safe. Ten thousand runs reduce Monte Carlo sampling error but add no empirical validation. Independent normals can allow impossible values, erase common causes and correlations, and poorly represent bounded, skewed, discrete, or conditional hazards. Expert choices require structured elicitation, evidence, ranges, disagreement, and sensitivity. Using the same 20 tests for calibration and validation overstates predictive evidence. Discarding solver failures may remove adverse physical regions and biases results unless inputs are invalid under predeclared constraints.

Define safety claims, thresholds/consequences, configurations, operational populations/scenarios, rare/common causes, affected groups, and decision authority. Inventory measurement, sampling, parameter, model-form, numerical, environment, operational, human, and unknown uncertainty. Repair feasible joint input models with evidence and dependencies; treat structural alternatives and expert disagreement explicitly. Diagnose every failed run, improve numerical methods, classify predeclared invalid configurations, or treat valid failures as adverse outcomes.

Separate calibration/training and independent validation; add targeted tests near safety boundaries and adverse regimes, compare models, check residuals and predictive calibration, and preserve extrapolation limits. Quantify simulation estimator uncertainty and convergence but report physical/model uncertainty separately. Analyze tail/joint failure, severity, sensitivity, robust alternatives, defense in depth, monitoring/safe states, information value, and residual ignorance. Independent domain/statistical/safety/human/operational review and formal authority acceptance are required; a Monte Carlo percentage cannot certify safety.

### Answer 5

Define claims for collision avoidance, route keeping, docking, passenger safety, availability, takeover success/time, communications resilience, and environmental limits by ferry configuration, software/model version, sensors, route, vessel/traffic class, loading, speed, crew, season, visibility/ice state, communications, and lifecycle. State whether each number is measurement uncertainty, parameter confidence, predictive probability/interval, population tolerance, simulated risk, or requirement margin.

Build evidence from calibrated sensor measurements, representative sea trials, simulator/scenario tests, incident/near-miss data, component/supplier reliability, communications/weather/traffic records, human-in-the-loop takeover studies, maintenance, and operational monitoring. Define sampling frames, censoring/missingness, corrections, covariance, population transfer, and subgroup/route/crew effects. Separate calibration/training from blind or independent validation and use staged trials with stop/safe-state criteria.

Model coupled fog/ice/sensor degradation, vessel behavior, traffic density, navigation geometry, communications/common infrastructure, cyber faults, power, software modes, crew attention/workload/trust, takeover timing, and rescue response. Preserve conditional dependence and compound/rare/common-cause scenarios. Compare plausible perception, behavior, failure, and human models; validate in intended regimes and state extrapolation. Analyze margins, predictive/tolerance distributions, tails and joint mission events rather than mean accuracy.

Use sensitivity and information value to target boundary tests, diverse traffic interactions, degraded sensors, communications loss, ice transitions, false alarms, and takeover. Mitigate with redundancy/diversity, geofencing, speed/route constraints, conservative weather limits, independent watchkeeping, safe stop/return, monitoring, incident learning, and staged autonomy. Qualified maritime, autonomy, controls, software, cybersecurity, human-factors, metrology/statistics, safety, regulatory, operator, crew, passenger/accessibility, and emergency stakeholders review the case.

Decision authority records accepted operating domain, evidence, uncertainty semantics, residual risks, constraints, monitoring, fallback, dissent, and triggers. Reopen on software/sensor/configuration, route/traffic/weather population, supplier, crew procedure, regulation, calibration drift, incident/near miss, model discrepancy, or observed coverage failure. Quantified confidence cannot establish safety beyond the validated domain or eliminate unforeseen compound failures.
