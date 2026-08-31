---
module_id: SYSENG-044
program: Systems Engineering
level: 1
module_number: 44
title: Sensitivity Analysis
status: complete
last_verified: 2026-08-31
---

# Sensitivity Analysis

## One-Page Review

### Governing question

Which uncertain inputs, assumptions, model structures, stakeholder preferences, and boundary conditions can materially change a system conclusion—and what action follows when the conclusion is fragile?

### Essential definitions

- **Sensitivity analysis (SA)** studies how variation in model inputs or assumptions relates to variation in outputs, decisions, rankings, or threshold events.
- **Uncertainty analysis (UA)** characterizes the range/distribution/credibility of outputs induced by uncertain inputs and models. UA asks “how uncertain?”; SA asks “what drives it?”
- A **factor** is any varied input: physical parameter, requirement, cost rate, duration, probability, correlation, model choice, scenario, preference weight, or policy assumption.
- A **quantity of interest (QoI)** is the output analyzed, such as mass, lifecycle cost, completion date, reliability, score difference, probability of success, or selected alternative.
- **Local sensitivity** describes response near a point, often by a partial derivative or finite difference.
- **One-at-a-time (OAT) analysis** changes one factor while holding others fixed. It supports simple traceability but cannot generally reveal interactions or full-range nonlinear behavior.
- **Elasticity** is a dimensionless local response: (E_i=(\partial y/\partial x_i)(x_i/y)).
- **Global sensitivity analysis (GSA)** explores factors over declared ranges/distributions, varying them jointly to capture nonlinearities and interactions.
- A **main effect** is variation attributable to a factor alone; an **interaction effect** occurs when a factor's influence depends on another factor.
- A **Sobol first-order index** is the fraction of output variance associated with a factor's main effect under stated probabilistic/independence assumptions; a **total-effect index** includes all interactions involving it.
- **Screening** cheaply identifies probably non-influential and potentially influential factors before expensive analysis.
- A **break-even boundary** is a factor combination where alternatives tie or a threshold changes state.
- **Robustness** is stability of a decision-relevant conclusion over credible variations, not merely small derivative magnitude at one nominal point.
- A **sensitivity audit** challenges framing, model structure, ranges/distributions, dependence, metrics, computation, and use—not only numerical results.

### Central model, mechanism, or theorem

For model (Y=f(X_1,\ldots,X_k;M)) with model choice (M), local sensitivity at nominal (x^0) is

\[
c_i=\left.\frac{\partial f}{\partial x_i}\right|_{x^0},
\]

or central finite difference

\[
c_i\approx\frac{f(x^0+h_ie_i)-f(x^0-h_ie_i)}{2h_i}.
\]

Magnitude depends on units and step; use scaled changes, elasticity, or decision-relevant ranges for comparison.

For independent uncertain inputs and square-integrable output, variance-based decomposition motivates

\[
S_i=\frac{Var_{X_i}(E[Y\mid X_i])}{Var(Y)},
\]

and total effect

\[
S_{T_i}=1-\frac{Var_{X_{\sim i}}(E[Y\mid X_{\sim i}])}{Var(Y)}.
\]

If (S_{T_i}-S_i) is large, interactions involving (X_i) matter. These indices answer a variance-apportionment question under the declared input distribution; they are not universal physical importance or causal effect.

### Critical invariants

- The decision/question, model version, QoIs, baseline, stakeholders, analysis owner, and action authority are fixed before interpreting sensitivity.
- Every factor has operational meaning, unit, baseline, range/distribution/scenario, provenance, dependence, feasibility constraints, and reason for variation.
- Ranges are evidence-based and decision-relevant; arbitrary ±10 or ±20 percent changes are not passed off as uncertainty.
- Values and combinations remain physically, logically, legally, temporally, and organizationally feasible or are clearly labeled stress cases.
- Local/OAT results are not generalized to nonlinear full-range behavior or interactions.
- Global methods vary all relevant factors jointly and preserve correlation, conditional structure, common causes, and scenario coherence.
- The method matches the QoI: output level, variance, quantile, tail probability, constraint violation, rank, regret, or decision switch can yield different importance.
- Structural choices, excluded factors, boundary conditions, algorithms, discretization, preference models, and data transformations are challenged alongside numeric parameters.
- Sampling design, seeds, convergence, estimator uncertainty, surrogate error, and failed/model-invalid runs are recorded.
- Importance is interpreted with controllability, decision leverage, evidence quality, time/cost of information, and affected stakeholders.
- A robust conclusion survives credible joint variations and alternative plausible models; a fragile conclusion exposes break-even regions and response options.
- Results reproduce from governed inputs/code and are reported with assumptions, limitations, counterexamples, and reopening triggers.

### Common failures

Common failures include varying only easy numeric inputs; choosing ranges after seeing results; using identical percentages for quantities with different uncertainty; ranking raw derivatives with incompatible units; calling a tornado chart global; holding correlated factors fixed independently; generating impossible combinations; screening away factors before examining interactions; analyzing mean output when the decision concerns a tail; interpreting Sobol indices as causal; treating low variance contribution as unimportant near a hard threshold; using a surrogate outside its validation domain; hiding non-convergent simulations; ranking preferences without swing semantics; changing weights without renormalization; ignoring alternative-dependent normalization and rank reversal; reporting a stable score instead of stable selection; and commissioning more data without linking it to a decision.

### Compact example

For (Y=10+2X+3Z+4XZ) with independent equiprobable (X,Z\in\{-1,1\}), the four outputs are 9, 7, 5, and 19; mean is 10 and variance is 29. Orthogonality attributes 4/29 to X's main effect, 9/29 to Z's main effect, and 16/29 to interaction. Total effects are 20/29 and 25/29. At nominal `(0,0)`, local derivatives are 2 and 3 and reveal nothing about the interaction that causes 55.2 percent of variance. Neither analysis is wrong; they answer different questions.

### Connections

SYSENG-041–043 provide decision, trade, and integrated forecast models whose robustness now needs testing. SYSENG-045 distinguishes uncertainty and confidence; SYSENG-046–048 apply evidence and risk; SYSENG-049–050 use sensitivities to preserve rationale and select architectures. Requirements, interfaces, configurations, validation evidence, and stakeholder values determine credible factor ranges and action thresholds.

## Governing Question

What must vary, over which credible domain and dependence structure, to learn whether an engineering conclusion is stable—and how should the team distinguish a mathematical driver from an actionable decision lever?

A sensitivity ranking without this framing is easy to misuse. A parameter can dominate variance because its range is broad, not because the system equation is steep. A controllable design variable can be locally influential but precisely known. A rare scenario can dominate safety consequence while contributing little to ordinary output variance. A preference weight can reverse a choice without changing physical performance. A model boundary can matter more than every numeric input yet never appear in a tornado chart.

## Why This Matters

Models compress evidence and assumptions into conclusions. Sensitivity analysis opens that compression: it identifies what produces the result, where a decision changes, which evidence is valuable, and whether a claimed margin survives credible variation. It can guide design margin, requirements negotiation, prototype/test selection, risk mitigation, reserve, monitoring, model improvement, and stakeholder deliberation.

NASA's current Decision Analysis guidance requires assumptions, uncertainty, sensitivity, robustness of rankings, and limitations to accompany recommendations. NASA Design Solution Definition includes robustness with effectiveness, lifecycle cost, schedule, risk, and maturity. NASA's modeling and simulation credibility guidance treats results robustness as a documented assessment of sensitivity and the relationship between modeled and real-world-system response.

GAO's current Cost Estimating and Assessment Guide requires sensitivity analysis linked to technical baseline parameters and assumptions and explicitly rejects subjective percentage variation without valid basis. NIST uncertainty guidance defines partial derivatives as sensitivity coefficients in first-order propagation and retains covariance terms when inputs are dependent. JRC global-sensitivity work distinguishes main and total effects and emphasizes interactions across the full declared input space.

Sensitivity is not merely “wiggle the inputs.” It is an experimental design conducted on a model. Like any experiment, it needs a question, treatments, domain, controls, response variables, execution record, analysis method, and limits on inference.

## Prerequisites and Retrieval

Before continuing, retrieve:

1. decision frame, authority, alternatives, mandatory constraints, stakeholder objectives/preferences, consequences, deadline, and reversibility;
2. controlled model/code/data/configuration, equations or executable interface, calibration/validation evidence, applicability domain, numerical tolerances, and known failure modes;
3. factor registry with definitions, units, baselines, distributions/ranges/scenarios, provenance, evidence strength, dependence, controllability, and owners;
4. QoIs and decision rules: levels, margins, cost/date/performance thresholds, safety tails, reliability, rank, score difference, regret, or selected alternative;
5. uncertainty model, risk scenarios, covariance/correlation/common causes, conditional logic, feasibility constraints, and structural alternatives;
6. sample-design, experimental-design, regression, calculus, probability/variance, conditional expectation, ranking, and visualization basics;
7. computational budget, parallelism, stochastic seeds, convergence criteria, surrogate plan, independent reproduction, records, and review roles.

As a retrieval test, inspect “battery life is most sensitive to temperature.” Ask: battery/model/configuration; temperature range/distribution and location; operating/load/profile; response metric (mean life, fifth percentile, threshold failure); other factors varied jointly; dependence; local or global method; numerical convergence; and whether temperature can be controlled or only monitored. Without those answers, “most sensitive” is not actionable.

## Learning Objectives

After completing this module, you should be able to:

1. charter a sensitivity analysis around a decision, QoI, model, domain, authority, and action;
2. build a traceable factor registry including structural and preference assumptions;
3. calculate local derivatives, finite differences, elasticities, and break-even values;
4. design and interpret OAT/tornado analyses without claiming interactions or global coverage;
5. use factorial/screening experiments to detect nonlinearity and interactions;
6. explain first-order and total-effect variance indices and their dependence assumptions;
7. select methods for scalar, vector, temporal, spatial, threshold, tail, and ranking QoIs;
8. preserve feasible joint inputs, correlations, conditional scenarios, and model validity;
9. audit sampling convergence, surrogate error, stochastic noise, and failed runs;
10. translate sensitivity into design, evidence, monitoring, mitigation, or decision actions with bounded claims.

## Core Exposition

**Charter the analysis.** Record the decision, alternatives, decision authority, model/configuration/version, baseline, QoIs, factors, domain, method family, computational budget, acceptance/convergence criteria, review, outputs, and actions. A test for design leverage differs from uncertainty prioritization, model debugging, risk control, requirement negotiation, or stakeholder-preference robustness.

**State the analysis question precisely.** Useful questions include: Which uncertain inputs dominate output variance? Which controllable parameters move margin most? What combinations cause violation? Which assumptions reverse the selected alternative? What evidence would reduce decision uncertainty? Which model structures produce materially different forecasts? A generic “find important variables” objective invites ambiguous rankings.

**Build a factor registry.** For each factor record ID/name, meaning, units, baseline, lower/upper/support, distribution or discrete cases, evidence/source/date, epistemic versus aleatory interpretation where useful, dependencies, feasibility rules, control authority, measurement/update route, affected model components, and rationale. Include environmental/operational scenarios, human behavior, supplier/resource states, correlations, algorithms, boundary/initial conditions, calibration parameters, discount rates, lifecycle horizons, value-function anchors, and weights.

**Separate factor influence from factor uncertainty.** For a linear local approximation (Y\approx f(x^0)+\sum_i c_i(X_i-x_i^0)), output uncertainty contribution depends on both sensitivity coefficient (c_i) and input uncertainty. A steep derivative with negligible input uncertainty may not drive forecast variance; a moderate derivative with broad uncertainty may. A controllable design factor can remain important even if it contributes little uncertainty.

**Select decision-relevant QoIs.** Do not default to mean response. Analyze performance margin, maximum temperature, fifth-percentile reliability, 95th-percentile latency, completion-date exceedance, lifecycle-cost tail, joint success probability, score difference, probability/range of rank, maximum regret, or harmed subgroup when those govern decisions. Vector/time/spatial outputs may require features or functional methods; aggressive scalar reduction can hide when/where failure occurs.

**Perform local differential analysis.** Analytic derivatives, automatic differentiation, adjoints, or finite differences reveal direction and slope near a point. Check step-size convergence: too large mixes curvature; too small exposes rounding/solver noise. Use dimensionless elasticity or scale inputs by credible changes before comparison. Nondifferentiability, discrete choices, thresholds, state changes, and solver branching require other methods.

**Use OAT scenarios for explainability.** Evaluate low/baseline/high values with all else fixed and report output delta. A tornado chart sorts these conditional deltas. This is valuable for traceability, stakeholder discussion, and debugging. It is not joint uncertainty propagation; “holding all else fixed” may violate correlations or operational coherence. Label impossible corners or replace them with conditional cases.

**Locate break-even and threshold boundaries.** Solve (f(x)=L) for a requirement threshold or (V_A(x)-V_B(x)=0) for decision switching. In multiple dimensions, map the boundary and identify which side each credible scenario occupies. Report distance/margin in meaningful units and uncertainty about the boundary. A stable total score can conceal frequent rank switches near zero score difference.

**Use factorial experiments to reveal interactions.** Two-level full factorial designs estimate main and interaction contrasts efficiently for a few factors. Fractional factorial designs trade runs for aliasing; document generators and which effects cannot be separated. Center points reveal curvature. Screening methods such as Morris elementary effects can identify non-influential factors and signs of nonlinearity/interactions, but rankings depend on domain and sampling design.

**Apply regression/correlation carefully.** Standardized regression coefficients, rank correlation, and partial correlation can screen relationships when model behavior and sampling assumptions fit. Correlation is not causation; correlated inputs make attribution difficult; nonlinear or nonmonotonic relationships can cancel. Inspect residuals, transformations, collinearity, heteroscedasticity, and predictive validation.

**Understand variance decomposition.** With independent inputs and an appropriate square-integrable model, Sobol first-order indices measure main-effect shares and total-effect indices include all interactions. First-order indices may sum below one; the gap reflects interactions. Total-effect indices can sum above one because interactions are counted for every involved factor. A small first-order but large total effect means the factor matters through interactions.

**Do not force independent-input indices onto dependent systems.** Physical, policy, and data constraints can correlate inputs. Breaking dependence creates implausible combinations and changes both output distribution and attribution. Use conditional sampling, copulas/causal or scenario models, dependence-aware sensitivity methods, or report results under several justified dependence structures. Explain what “importance” means when effects are shared.

**Treat categorical and structural factors explicitly.** Compare alternative equations, solvers, fidelity levels, physical assumptions, failure logic, requirement interpretations, lifecycle boundaries, and preference models as discrete cases or model ensembles. Parameter sensitivity conditional on one structure cannot establish structural robustness. If structures are not meaningfully probabilistic, use scenario envelopes rather than invented probabilities.

**Preserve feasibility.** Reject or repair combinations violating conservation, geometry, resource capacity, temporal order, safety/legal bounds, or conditional definitions. Sampling “mass,” “power,” and “architecture” independently may describe no buildable system. Parameterize independent latent/design variables from which feasible quantities derive, or use constrained designs and declare changed measure semantics.

**Separate uncertainty propagation and attribution.** UA estimates output distribution/range under a model of inputs. SA attributes aspects of output variation or decision switching. A narrow output distribution can coexist with high normalized sensitivity indices; the indices divide a small variance. A wide distribution can have no single dominant factor because interactions/structural uncertainty dominate.

**Handle stochastic models.** Replicate at identical inputs to estimate intrinsic simulation noise. Use common random numbers carefully for comparisons, nested designs, or emulators that distinguish noise from response. A single run per input can rank random noise. Record seeds/streams, warm-up, horizon, replications, and stopping rules.

**Use surrogates with governed error.** Gaussian processes, polynomial chaos, response surfaces, trees, neural networks, or reduced models can make global analysis affordable. Train over the analysis domain using suitable designs, reserve independent validation, inspect error near thresholds/tails, propagate surrogate uncertainty when material, and retain simulator spot checks. High average accuracy does not ensure correct decision boundaries.

**Check computation and convergence.** Version code/data/environment; validate sampling distributions and dependencies; test known functions; compare independent implementations or analytic cases; track effective sample size and estimator uncertainty; repeat designs/seeds; inspect index stability; record invalid/failed runs; and avoid silently replacing failures with nominal values. More samples cannot correct a misspecified model or domain.

**Audit the analysis adversarially.** Ask which factors were excluded, who chose ranges, whether the baseline favors a recommendation, whether the QoI hides tails/groups, whether a normalization creates rank reversal, whether factors double count one cause, whether independence is false, whether a model fails in adverse regions, and whether the decision would change under an equally plausible structure or stakeholder preference.

**Translate importance into action.** For influential and controllable factors, redesign, allocate margin, constrain operations, or set control limits. For influential and uncertain factors, test, prototype, collect data, improve models, qualify suppliers, or monitor leading indicators. For influential preferences, obtain legitimate stakeholder/authority clarification. For influential structural assumptions, compare models and gather discriminating evidence. For non-influential factors under a broad credible domain, simplify cautiously and record the domain.

**Prioritize information by decision value.** Reducing the largest variance contributor is not automatically best. Consider probability of changing action, consequence, evidence cost, decision deadline, reducibility, and whether uncertainty is shared/irreducible. A modest factor near a decision boundary may have higher information value than the largest contributor to output variance.

**Report robustness honestly.** Publish factor definitions/domains, model/QoIs, method and assumptions, dependence, convergence/error, main/interaction/total effects, break-even maps, decision-switch frequency, counterexamples, feasible stress cases, action mapping, limitations, and data/code identity. “Robust” means stable over the declared credible set—not correct under unknown omitted mechanisms.

The following checker provides an analytic test case with a dominant interaction that a nominal local analysis cannot reveal.

<!-- bijux-verify: {"id":"factorial-sensitivity-check","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"mean=10.000\nvariance=29.000\nmain_x=0.138\nmain_z=0.310\ninteraction_xz=0.552\ntotal_x=0.690\ntotal_z=0.862\nlocal_dx_at_origin=2.000\nlocal_dz_at_origin=3.000\nvariance_reconciles=1\nevidence=declared_factorial_model_only\n","stderr":""}} -->
```python
from itertools import product

def model(x, z):
    return 10 + 2 * x + 3 * z + 4 * x * z

outputs = [model(x, z) for x, z in product((-1, 1), repeat=2)]
mean = sum(outputs) / len(outputs)
variance = sum((value - mean) ** 2 for value in outputs) / len(outputs)
components = {"x": 2**2, "z": 3**2, "xz": 4**2}

print(f"mean={mean:.3f}")
print(f"variance={variance:.3f}")
print(f"main_x={components['x'] / variance:.3f}")
print(f"main_z={components['z'] / variance:.3f}")
print(f"interaction_xz={components['xz'] / variance:.3f}")
print(f"total_x={(components['x'] + components['xz']) / variance:.3f}")
print(f"total_z={(components['z'] + components['xz']) / variance:.3f}")
print(f"local_dx_at_origin={2:.3f}")
print(f"local_dz_at_origin={3:.3f}")
print(f"variance_reconciles={int(sum(components.values()) == variance)}")
print("evidence=declared_factorial_model_only")
```

This exact orthogonal decomposition is a teaching case. Real indices need suitable sampling/estimators, convergence evidence, dependence treatment, and model-validity review.

## Definitions and Notation

Let (X=(X_1,\ldots,X_k)) be factors with declared joint domain/distribution (D), (M) model structure, (Y=f(X;M)) output, and (q(Y)) the decision-relevant QoI.

Local coefficient and elasticity:

\[
c_i=\frac{\partial q}{\partial x_i},\qquad E_i=c_i\frac{x_i}{q},
\]

where elasticity is undefined or unstable near (x_i=0) or (q=0) and requires meaningful ratios.

Finite-difference convergence compares several (h_i), not one arbitrary step:

\[
c_i(h)=\frac{q(x+h_ie_i)-q(x-h_ie_i)}{2h_i}.
\]

For two-level coded factors (-1,+1), main and interaction effects can be estimated by orthogonal contrasts. In the teaching model

\[
Y=\beta_0+\beta_1X_1+\beta_2X_2+\beta_{12}X_1X_2,
\]

with independent equiprobable coded inputs,

\[
Var(Y)=\beta_1^2+\beta_2^2+\beta_{12}^2.
\]

For a decision between alternatives (a,b), score/utility difference is

\[
\Delta(X,M,W)=V_a-V_b.
\]

The switch boundary is (\Delta=0); a robustness summary should describe which credible region has (\Delta>0), (=0), or (<0), not merely sensitivity of each score separately.

For a threshold (L), define failure indicator

\[
I_F(X)=\mathbf{1}\{q(f(X))>L\}
\]

for upper-bound requirements. Sensitivity of (q) and sensitivity of (Pr(F)) answer different questions.

## Mechanisms, Invariants, or Proof Structure

**Mechanism 1—decision framing.** Fix decision, authority, model, QoIs, conclusions to stress, computational budget, and actions.

**Mechanism 2—factor/domain governance.** Register numeric, categorical, structural, scenario, and preference factors with evidence-based domains, dependencies, feasibility, and control.

**Mechanism 3—layered analysis.** Begin with analytic/local/OAT checks, add factorial/screening methods, then apply global/dependence-aware methods proportionate to nonlinearity, interaction, stakes, and cost.

**Mechanism 4—computational credibility.** Verify implementation, sampling, convergence, stochastic noise, surrogate validity, failed runs, and reproducibility.

**Mechanism 5—decision translation.** Map drivers and break-even regions to design, evidence, monitoring, mitigation, stakeholder authority, simplification, or commitment change.

The inference remains bounded by model validity and the declared factor domain. Sensitivity shows conditional dependence within that analytical world; it cannot discover an omitted mechanism that never enters the model.

## Alternatives and Trade-Offs

**Analytic/automatic derivatives** can be fast and precise locally. **Finite differences** are broadly accessible but step- and noise-sensitive. Neither alone covers discontinuities or broad interactions.

**OAT/tornado charts** are explainable and cheap. **Factorial/global designs** expose interactions and nonlinearities but require more runs and careful attribution.

**Morris screening** supports many factors with modest cost and flags nonlinearity/interactions qualitatively. **Variance-based methods** quantify main/total contributions but may be expensive and depend strongly on probabilistic/domain assumptions.

**Regression/correlation methods** are efficient for near-linear/monotonic behavior. **Moment-independent, distributional, or classifier-based methods** may better address multimodal outputs, tails, and threshold regions.

**Monte Carlo/quasi-Monte Carlo** offers flexible propagation. **Designed quadrature/polynomial chaos** can converge faster for smooth low/moderate-dimensional problems but struggles with discontinuity or high dimension.

**Detailed simulation** preserves mechanisms but costs runs. **Surrogates** enable exploration but introduce approximation and boundary risk.

**Probabilistic domains** support variance/probability statements. **Interval, scenario, or robustness sets** avoid false probabilities when evidence cannot support distributions but yield different importance concepts.

## Failure Modes and Misconceptions

**“Sensitivity and uncertainty are synonyms.”** UA measures output uncertainty; SA attributes response or decision changes. They are complementary.

**“Largest derivative means greatest risk.”** Units, input range/uncertainty, consequence, threshold location, dependence, and control determine relevance.

**“A tornado chart covers the uncertainty space.”** It conditionally varies one factor and normally misses interactions and joint extremes.

**“First-order indices sum to one.”** Only when there are no interactions (under the decomposition assumptions). A gap can be the key result.

**“Total effects should sum to one.”** Interactions are counted in several total-effect indices, so their sum can exceed one.

**“A low index makes a factor safe to fix.”** The conclusion holds only for the QoI, domain, dependence, model, and accuracy required; threshold/tail relevance may differ.

**“Uniform distributions are neutral.”** Bounds and density shape express beliefs/coverage and can materially change sensitivity.

**“Correlation can be ignored for convenience.”** It changes feasible combinations, output uncertainty, and attribution semantics.

**“Stable ranking proves the decision.”** Stability within a model does not validate alternatives, evidence, preferences, ethics, or omitted factors.

**“More samples repair weak assumptions.”** Sampling reduces estimator error; it does not repair invalid ranges, broken models, or missing mechanisms.

## Worked Examples

### Example 1

**Local derivative with units.** Cost model (C=5+0.08m+2r) uses mass (m) in kg and labor rate (r) in thousands. Raw sensitivities 0.08 and 2 cannot be ranked because their units/scales differ. Over credible changes Δm=20 and Δr=1.5, local impacts are 1.6 and 3 cost units; state both ranges and linearity limits.

### Example 2

**Finite-difference step.** A solver's QoI changes by 0.102, 0.0101, 0.0004, and erratically for successively smaller perturbations. Compare central differences, solver tolerance, and repeated evaluations; choose a converged region or use differentiation designed for the solver. The smallest step is not automatically most accurate.

### Example 3

**Interaction missed by OAT.** The embedded model has local slopes 2 and 3 at the origin, while the (4XZ) term contributes 16/29 of variance. Test factor combinations or global effects before claiming main-effect ranking captures behavior.

### Example 4

**Requirement boundary.** Thermal response is (T=70+0.5p+3a), limit 90 °C, with power deviation (p) and airflow state (a). Boundary is (0.5p+3a=20). Plot feasible/credible pairs and identify monitoring/control; separate ordinary states from fan-failure scenarios rather than assigning independent ranges that create nonsense.

### Example 5

**Decision weight break-even.** Alternatives have values A=(0.9,0.4), B=(0.6,0.8) and weights `(w,1-w)`. (\Delta=0.7w-0.4), so tie is (w=4/7). Report which stakeholder-authorized swing-weight interval lies on either side; do not vary one weight without maintaining normalization and scale meaning.

### Example 6

**Tail QoI changes priorities.** Mean latency is driven by normal request size, while probability of exceeding 500 ms is driven by cache-loss state and a shared dependency. Analyze tail indicator/quantile and conditional scenarios; mean-output Sobol ranks cannot answer the SLO question.

### Example 7

**Correlated cost and schedule factors.** Productivity, duration, and labor cost share one staffing/learning mechanism. Sampling each independently creates high-productivity/long-duration combinations inconsistent with the model. Sample team capability and work difficulty, then derive dependent productivity, duration, cost, and rework.

### Example 8

**Surrogate boundary error.** A surrogate has 1 percent average error but smooths a discontinuous controller mode switch near the safety threshold. Add boundary-focused validation, classify regimes, compare simulator traces, and include surrogate error; average accuracy does not support the decision.

### Example 9

**Low variance, high leverage.** A software retry limit is known exactly and contributes no forecast variance, but changing it strongly affects overload recovery. It is a design/control sensitivity, not an uncertainty contributor. Keep controllability and uncertainty-prioritization analyses separate.

### Example 10

**Information action.** Supplier lead-time uncertainty is the largest schedule driver, but the decision is already robust to it; reliability-model structure is smaller in variance yet crosses the architecture boundary. A discriminating reliability test may have more decision value than refining lead-time data.

## Cross-Program Connections

**Platform engineering.** Stress adoption, workload, tenant mix, service limits, staffing, cloud/vendor changes, failure correlation, migration, and developer preferences; tail SLO and cost conclusions often interact.

**API and service engineering.** Analyze payload/concurrency, dependency latency/failure, retry/timeouts, consistency choices, versions, caching, and client behavior using tail and incident QoIs rather than averages only.

**Data engineering.** Explore volume/skew/freshness, schema and late data, partitioning, compute/storage prices, replay, quality, privacy, and workload correlation; surrogate benchmarks need workload-domain validation.

**Object-oriented programming.** Design sensitivity includes dependency structure, mutation/aliasing, dispatch, allocation, team change patterns, tests, and runtime workload—not lines of code alone.

**Functional programming.** Analyze effect boundaries, strict/lazy evaluation, concurrency, persistent structures, type/model choices, migration, team learning, and workload; ecosystem/operational assumptions can dominate syntax-level performance.

## References

1. NASA, *Systems Engineering Handbook, Section 6.8: Decision Analysis*, current web edition. <https://www.nasa.gov/reference/6-8-decision-analysis/>
2. NASA, *Systems Engineering Handbook, Section 4.4: Design Solution Definition*, current web edition. <https://www.nasa.gov/reference/4-4-design-solution-definition/>
3. NASA, *Systems Engineering Handbook, Section 6.7: Technical Assessment*, current web edition. <https://www.nasa.gov/reference/6-7-technical-assessment/>
4. NASA, *NASA-HDBK-7009A: Handbook for Models and Simulations*, 2019. <https://standards.nasa.gov/sites/default/files/standards/NASA/A/0/nasa-hdbk-7009a.pdf>
5. NASA, *NASA Risk-Informed Decision Making Handbook*, NASA/SP-2010-576. <https://ntrs.nasa.gov/citations/20100021361>
6. U.S. GAO, *Cost Estimating and Assessment Guide*, GAO-20-195G. <https://www.gao.gov/products/gao-20-195g>
7. U.S. GAO, *Schedule Assessment Guide*, GAO-16-89G. <https://www.gao.gov/products/gao-16-89g>
8. NIST, *Technical Note 1297, Appendix A: Law of Propagation of Uncertainty*. <https://www.nist.gov/pml/nist-technical-note-1297/nist-tn-1297-appendix-law-propagation-uncertainty>
9. NIST/SEMATECH, *e-Handbook of Statistical Methods: Propagation of Error Considerations*. <https://www.itl.nist.gov/div898/handbook/mpc/section5/mpc55.htm>
10. A. Saltelli, S. Tarantola, and K. Chan, *A Quantitative Model-Independent Method for Global Sensitivity Analysis of Model Output*, official European Commission JRC record, 1997. <https://publications.jrc.ec.europa.eu/repository/handle/JRC15044>

## Exercises

### Exercise 1

For (y=100+4x+2z+3xz), compute local derivatives at `(0,0)` and `(1,1)`. Explain why one local point cannot characterize the interaction over `x,z in [-1,1]`.

### Exercise 2

For the embedded model (Y=10+2X+3Z+4XZ) with independent equiprobable coded factors, compute mean, variance contributions, first-order indices, interaction share, total-effect indices, and their sums. Interpret without causal overclaim.

### Exercise 3

Alternative A has value (V_A=w(0.85)+(1-w)(0.45)); B has (V_B=w(0.60)+(1-w)(0.80)). Find the break-even weight, determine the preferred alternative at `w=0.50` and `w=0.70`, and design a sensitivity report for an authorized credible interval `w in [0.45,0.75]`.

### Exercise 4

Audit an analysis that selects eight inputs from a 60-input model, applies independent uniform ±20 percent ranges, runs 200 samples without a seed, replaces solver failures with baseline output, fits an unvalidated linear regression, analyzes mean safety margin, and declares the design robust because coefficients are small.

### Exercise 5

Design a sensitivity analysis for a regional emergency communications system with mobile and fixed nodes, shared power/transport dependencies, uncertain hazard scenarios, coverage/capacity/latency/reliability/cost outcomes, diverse communities, and a staged architecture decision. Cover framing, factor registry, feasible dependence, methods, validation, decision boundaries, information value, action, and reporting.

## Answers to the Exercises

### Answer 1

\[
\frac{\partial y}{\partial x}=4+3z,\qquad \frac{\partial y}{\partial z}=2+3x.
\]

At `(0,0)` the derivatives are 4 and 2. At `(1,1)` they are 7 and 5. The derivative for each factor changes with the other factor, which is precisely the interaction. At other corners, slopes can shrink or change sign: at `z=-1`, (\partial y/\partial x=1); at `x=-1`, (\partial y/\partial z=-1). One local ranking is conditional on the nominal point and says nothing by itself about full-range variance, threshold crossing, or feasibility. Use factorial contrasts or a global design over the justified joint domain and select a decision-relevant QoI.

### Answer 2

The four outputs are 9, 7, 5, and 19, so mean is 10. With orthogonal independent coded factors, variance contributions are coefficient squares: X main 4, Z main 9, and XZ interaction 16; total variance is 29.

\[
S_X=4/29=0.1379,\quad S_Z=9/29=0.3103,
\]

\[
S_{XZ}=16/29=0.5517.
\]

First-order sum is (13/29=0.4483); adding interaction gives one. Total effects are

\[
S_{T_X}=(4+16)/29=20/29=0.6897,
\]

\[
S_{T_Z}=(9+16)/29=25/29=0.8621.
\]

Their sum is (45/29=1.5517) because shared interaction is counted in both. These are exact variance shares for this declared distribution/model. They do not establish causation, physical importance outside `{-1,1}`, controllability, consequence, or evidence value.

### Answer 3

\[
V_A=0.45+0.40w,qquad V_B=0.80-0.20w.
\]

Set equal: (0.45+0.40w=0.80-0.20w), so (0.60w=0.35) and

\[
w^*=7/12\approx0.5833.
\]

At (w=0.50), A=0.65 and B=0.70, so B leads by 0.05. At (w=0.70), A=0.73 and B=0.66, so A leads by 0.07. The credible interval crosses the boundary: B is preferred below 0.5833 and A above it, with a tie at the boundary.

The report preserves raw performance and fixed value mappings, defines the swing represented by (w), identifies legitimate preference authority/stakeholder views, plots score difference over `[0.45,0.75]`, adds performance/scale uncertainty and interactions, and states no robust single ranking under weight uncertainty alone. It can request preference clarification, identify an information action, report close alternatives, or seek a design that dominates. It must not choose the weight after seeing the preferred result.

### Answer 4

The factor subset may exclude dominant numeric, categorical, structural, boundary, scenario, or preference assumptions; document screening rationale and test excluded-factor plausibility. Independent uniform ±20 percent ranges lack evidence, erase correlations/conditional feasibility, and may create impossible systems. Build a factor registry from data, physics, scenarios, experts, and authority; model dependence and constraints; distinguish uncertainty ranges from stress cases and design ranges.

Two hundred runs may or may not support the chosen estimator/dimension; predefine design, seed/streams, convergence metrics, replications, and independent checks. Solver failures can identify adverse regions or numerical/model limits; replacing them with baseline output biases sensitivity toward zero. Diagnose/classify failures, improve solver/model, constrain invalid inputs transparently, or treat valid adverse failures as outcomes.

An unvalidated linear regression may miss nonlinearity, interactions, tails, and discontinuities. Validate residuals/predictions on held-out data and compare factorial/screening/global or threshold-focused methods. Mean safety margin can be positive while tail failure is unacceptable; analyze minimum/quantile/exceedance and scenario-specific margins. Small coefficients can result from scaling, narrow ranges, cancellation, noise, or poor fit and cannot establish robustness. Map credible joint variations and structural models to threshold/decision switching, independently reproduce, disclose limits, then tie results to mitigation, testing, monitoring, or design change.

### Answer 5

Charter the staged decision among mobile/fixed/hybrid architectures, deployment regions/populations, hazard and recovery horizons, authority, mandatory emergency-service obligations, decision dates, reversibility, and QoIs: coverage by community, capacity, latency tails, availability/recovery, responder/public usability, interoperability, safety/security/privacy, lifecycle cost, deployment time, and joint mission success. Preserve subgroup/geographic outcomes rather than one average.

Register hazard intensity/path/duration, grid and fuel states, transport access, tower/backhaul/common cloud dependencies, mobile inventory/travel/setup, terrain/building propagation, demand surge/location, priority policy, battery/generator performance, staffing/training, maintenance, spectrum/interference, cyberattack, supplier lead time, cost rates, weather, adoption, architecture/control logic, and preference/coverage equity rules. For each state units, evidence, range/distribution/scenario, epistemic status, dependencies, feasibility, owner, and control are explicit.

Use conditional hazard scenarios or a causal/dependency model so grid, transport, backhaul, demand, and repair do not vary incoherently. Parameterize feasible architectures and resource capacities. Start with analytic/local and OAT checks for traceability; use designed screening for many factors, factorial cases for architecture × hazard × dependency interactions, and global/robust scenario analysis for threshold/tail and rank QoIs. Map boundaries where any community loses minimum coverage, latency/recovery exceeds limits, resources exhaust, cost/date commitments fail, or architecture ranking changes. Analyze structural propagation/repair models and stakeholder preference scenarios, not only numeric parameters.

Verify model units, conservation/resource logic, network routing, failure/recovery states, historical-event and exercise behavior, numerical convergence, stochastic replication/seeds, failed runs, and any surrogate near boundaries; obtain independent communications, emergency-management, infrastructure, security, human-factors, cost, and community review. Compare sensitivities across hazards and dependence models.

Translate controllable drivers into prepositioning, diversity, hardening, power/fuel, mutual aid, priority/control, alternate backhaul, training, spares, monitoring, or staged pilots. Direct information actions to uncertain factors capable of changing the staged choice, especially field propagation, setup/repair, shared-dependency recovery, and community access—not automatically the largest variance share. Report domains, dependencies, driver and interaction results, joint failure/rank regions, counterexamples, affected-community outcomes, estimator/model error, actions, residual risk, dissent, and reopening triggers. Stability within modeled hazards is not proof of equitable access, emergency effectiveness, cybersecurity, supplier delivery, or resilience to omitted compound events.
