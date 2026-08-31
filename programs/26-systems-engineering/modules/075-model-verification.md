---
module_id: SYSENG-075
program: Systems Engineering
level: 2
module_number: 75
title: Model Verification
status: complete
last_verified: 2026-08-31
---

# Model Verification

## One-Page Review

### Governing question

Does the implemented model faithfully realize its controlled conceptual/mathematical specification and solve or execute it with quantified error for the intended calculation, before any claim is made that the model adequately represents the real system?

### Essential definitions

- A **model** is a purposeful abstraction expressed in text, mathematics, diagrams, logic, data structures, executable code, learned parameters, or combinations. A **simulation** executes/manipulates a model over inputs, state, and time.
- A **conceptual model** defines included entities, relationships, behavior, assumptions, boundaries, abstractions, equations/logic, and intended outputs before implementation details.
- **Model verification** provides evidence that the implemented model accurately represents its specified conceptual/mathematical description and that a calculation is performed accurately enough for its intended use. It asks whether the model was implemented and solved right.
- **Model validation** assesses whether the model/simulation adequately represents relevant real-world behavior for an intended use. A verified model can be invalid; a validation comparison using unverified code is ambiguous.
- **Code verification** finds implementation defects by comparison with exact/benchmark solutions, manufactured solutions, independent calculations, invariants, tests, and formal/static methods.
- **Calculation (solution) verification** estimates numerical error in a particular simulation due to discretization, iteration, roundoff, stochastic sampling, and incomplete convergence.
- **Conceptual-model verification** checks that the controlled implementation specification is internally consistent, complete enough, dimensionally/semantically well formed, and faithfully transformed into lower representations.
- A **benchmark** is a controlled problem with a trustworthy expected solution or property used to assess implementation or calculation behavior. Agreement among codes is not truth if they share errors.
- The **method of manufactured solutions (MMS)** chooses an analytical solution, derives the forcing/source required to make it exact, and checks whether numerical implementation recovers the expected convergence.
- An **invariant** is a property that must hold through model execution, such as conservation, probability normalization, type/unit consistency, ordering, bounds, or state-machine legality.

### Central model, mechanism, or theorem

Separate the transformation chain

$$
S \xrightarrow{T_1} C \xrightarrow{T_2} M \xrightarrow{T_3} I \xrightarrow{N(h,\tau,\epsilon)} Y,
$$

where $S$ is source intent/requirements, $C$ conceptual model, $M$ mathematical/logical specification, $I$ implementation, and $Y$ computed output under discretization $h$, solver tolerance $\tau$, and finite precision/stochastic error $\epsilon$. Verification checks each transformation and estimates solution error. Validation compares appropriately verified outputs with relevant reality for intended use. Calibration adjusts parameters; it does not prove either transformation correctness or model adequacy outside calibration evidence.

### Critical invariants

- State the model's intended use, decision, required outputs, accuracy, domain, and consequence before selecting verification rigor.
- Keep conceptual specification, equations/logic, implementation, configuration, inputs, solver, mesh/time step, libraries, compiler/runtime, random seeds, and results version-bound.
- Verify transformations between representations; a syntactically valid generated model can be semantically wrong.
- Distinguish code verification from calculation verification and both from validation, calibration, uncertainty quantification, and sensitivity analysis.
- Use exact, manufactured, benchmark, limiting, invariant, metamorphic, and independent-reference tests with known coverage and limitations.
- Demonstrate expected convergence in the asymptotic regime before extrapolating order or error.
- Separate discretization, iterative, roundoff, sampling, input/parameter, and model-form errors.
- Conservation and other invariants are necessary but rarely sufficient; wrong solutions can conserve.
- Validation data must not be used to tune away implementation defects; verify before interpreting empirical mismatch.
- Random/stochastic/agent/ML models require deterministic components, distributions, seeds, statistical oracles, preprocessing, and nondeterminism to be controlled.
- Tool qualification, independent implementation, or review rigor is proportionate to consequence and common-mode risk.
- Changes to equations, code, data/preprocessing, solver, dependencies, hardware/precision, parameters, or use trigger impact analysis and regression verification.

### Common failures

Common failures include equating a running model with a verified model; using experimental agreement as code verification; validating before checking implementation; comparing only against another code with shared heritage; tuning parameters to hide bugs; testing nominal cases but not boundaries/limits; checking outputs without conservation/unit/state invariants; accepting one mesh/time step; claiming convergence outside the asymptotic regime; ignoring solver and roundoff error; using a benchmark whose expected solution is uncertain; omitting preprocessing and postprocessing; failing to version inputs/seeds/libraries; mistaking sensitivity analysis for correctness; treating model-checker/proof assumptions as reality; and reusing verification after a solver or platform change without impact analysis.

### Compact example

For $y'=-y$, $y(0)=1$, explicit Euler at $t=1$ gives 0.34867844, 0.35848592, and 0.36323244 for 10, 20, and 40 equal steps, while the exact value is $e^{-1}=0.36787944$. Errors are 0.01920100, 0.00939352, and 0.00464700; refinement ratios 2.044 and 2.021 approach two, consistent with first-order error halving. This verifies one numerical behavior for one equation/domain/implementation. It does not validate any physical model or prove every branch correct.

### Connections

MBSE model consistency, transformations/code generation, parametric analysis, requirement verification, simulation-based evidence, reliability/safety models, software testing, numerical analysis, data/ML pipelines, configuration management, and decision analysis all depend on model verification before model outputs can carry assurance weight.

## Governing Question

Can the model team trace every output used in a decision through a controlled implementation and specification, demonstrate that implementation defects and numerical errors are acceptably bounded over the relevant calculation domain, and clearly separate that claim from empirical validity and real-world prediction?

“The model matches the data” is not enough. A bug can be compensated by a calibrated parameter; an invalid physical assumption can cancel a numerical error; experiment and simulation can share the same preprocessing defect. Verification isolates whether the implemented abstraction behaves as specified. Only then can validation interpret differences between model and reality.

## Why This Matters

Models decide architecture, margins, safety limits, schedules, costs, controls, operations, and certification evidence. Many conditions are too hazardous, rare, expensive, or inaccessible to test directly. If model implementation or solution error is unknown, apparent precision creates more danger than an honest absence of prediction.

NASA-STD-7009B, active in its official standards record with a 2024 document date, establishes lifecycle credibility practices for models and simulations and requires intended-use/acceptance considerations through delegated technical authority. NASA's associated handbook explicitly recommends verification before empirical validation so implementation defects are not discovered while interpreting reality agreement. NASA Glenn guidance further distinguishes code error evaluation from calculation error estimation.

Model verification applies beyond computational physics. A SysML state machine can contain unreachable, deadlocked, nondeterministic, or illegal transitions. A requirements model can violate types, multiplicities, units, or trace constraints. A reliability model can double-count dependent events. A cost model can mix real and nominal values. A discrete-event simulation can schedule events in the wrong order. An ML pipeline can implement preprocessing differently in training and inference. Each needs specification-to-implementation evidence.

The rigor is decision-relative. A qualitative trade-space screening model may tolerate larger numerical error than a model setting a safety-critical clearance. But intended use does not excuse bugs; it determines required coverage, error bounds, independence, review, and evidence. A model can be verified for one calculation class and unverified for another.

Verification also enables useful failure. When numerical error, implementation uncertainty, or uncovered domain is explicit, decision makers can add margin, commission a benchmark, refine the mesh, change solver, collect data, or avoid the model. An unbounded “validated model” label blocks that engineering judgment.

## Prerequisites and Retrieval

Before crediting model verification, retrieve:

1. intended use, decision, stakeholders/authority, consequences, required outputs/accuracy, domain/range/scenarios, extrapolation, acceptance criteria, and governing modeling standard;
2. source requirements, conceptual model, real-world-system boundary, entities, relationships, assumptions, omissions, abstractions, state/mode, interfaces, coordinate frames, units, scales, and rationale;
3. mathematical/logical specification: equations, algorithms, constraints, initial/boundary conditions, constitutive/closure relations, event semantics, probability laws, parameter definitions, and expected properties;
4. implementation architecture, source/generated code, model files, schemas, transformations, APIs, preprocessing/postprocessing, solver, libraries, compiler/runtime, hardware/precision, and configuration;
5. input/parameter/data provenance, units, transformations, calibration, correlations, ranges, distributions, missingness, random generators/seeds, and scenario configuration;
6. verification plan and requirements: transformations, functions/branches, domains, tolerances, invariants, conservation, exact/benchmark/manufactured cases, limiting cases, metamorphic properties, differential references, and regression;
7. numerical settings: mesh/spatial/temporal discretization, formal order, iterative tolerance, nonlinear/linear solvers, convergence criteria, stabilization, adaptivity, roundoff, sampling, and termination;
8. benchmark/reference provenance, analytical derivation, independent implementation, expected uncertainty, applicability, and known defects;
9. test results, convergence studies, residuals, invariant errors, coverage, failed cases, discrepancies, corrective actions, reviews, tool qualification, and reproducible artifacts;
10. calculation-specific error estimate, asymptotic-range evidence, mesh/time/solver sensitivity, sampling error, numerical instability, and unresolved implementation risk;
11. validation/calibration evidence kept distinct: experiment configuration, measurement uncertainty, data independence, parameter fitting, discrepancy, and validation domain;
12. change history, evidence impact, release/version, archival/reproduction instructions, operating constraints, limitations, user competence, and re-verification triggers.

Perform a **transformation audit**: take one decision-critical output and trace backward through postprocessing, solver result, discrete model, equations/logic, conceptual assumptions, source requirement, inputs, and configuration. At every arrow ask what test proves the transformation preserves intended semantics. Then run forward with a case whose answer/property is known independently.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish model verification, model validation, calibration, sensitivity analysis, and uncertainty quantification;
2. distinguish conceptual-model, code, and calculation/solution verification;
3. trace model transformations and configurations from source intent to output;
4. design exact, benchmark, manufactured, limiting, invariant, metamorphic, and differential checks;
5. conduct and interpret mesh/time-step/order-of-accuracy studies;
6. separate discretization, iterative, roundoff, sampling, parameter/input, and model-form error;
7. verify state, discrete-event, stochastic, probabilistic, MBSE, generated, and ML models appropriately;
8. assess independent-reference and tool/common-mode risk;
9. construct a bounded model-verification report and evidence package;
10. determine when model change or new intended use requires re-verification.

## Core Exposition

**Define the model as a system.** Identify requirements, architecture, interfaces, configurations, lifecycle, users, operating environment, verification, validation, release, change, and retirement. Models used for decisions deserve the same discipline as delivered software/hardware, scaled to consequence.

**Freeze intended use.** State decision, outputs, domain, accuracy, confidence, extrapolation, and consequence. Verification coverage depends on these. A solver verified for smooth subsonic flow is not thereby verified for shocks; a state model verified for nominal transitions may not cover recovery.

**Control the conceptual model.** Record what exists, how it interacts, which phenomena are represented or omitted, scales, boundaries, assumptions, and abstractions. Review internal consistency, dimensional meaning, conservation, causal direction, state completeness, probability normalization, and requirement trace.

**Verify representation transformations.** Check textual requirements to SysML/logic, diagrams to equations, equations to discrete form, model-to-code generation, schema serialization, unit/coordinate conversion, and result postprocessing. Round-trip tests, semantic comparison, typed constraints, generated-code review, and traceable transformations expose silent drift.

**Verify code against known truth.** Use unit tests for functions and boundary/error paths; exact analytical solutions; trusted benchmarks; manufactured solutions; independent hand calculations; conservation/invariants; limiting cases; symmetry; metamorphic relations; and independent implementations. Design cases to isolate terms and interactions.

**Use manufactured solutions correctly.** Choose a sufficiently rich smooth solution, substitute it into the governing equations to derive forcing, apply consistent boundaries, and check observed convergence order. MMS verifies implemented operators and formal accuracy; it does not validate the original physical model.

**Verify calculations, not only code releases.** Even correct code can produce inaccurate results because a mesh is coarse, time step large, iteration incomplete, simulation too short, sample small, or arithmetic unstable. Record calculation-specific resolution, tolerances, residuals, convergence, precision, and error estimates.

**Establish asymptotic convergence.** Refine resolution systematically, keep other errors smaller, compare solutions with a norm relevant to the output, and estimate observed order. Ratios can mislead on non-monotone, singular, discontinuous, chaotic, adaptive, or pre-asymptotic problems. Inspect fields and functionals, not one convenient scalar.

**Control iterative error.** Solver residual is not necessarily solution error. Define stopping criteria relative to discretization error and output sensitivity. Check conservation/balance and rerun tighter tolerances. Nonlinear convergence to a wrong branch is possible.

**Assess roundoff and conditioning.** Vary precision, ordering, scaling, platform, and solver where material. Catastrophic cancellation, ill-conditioning, nondeterministic parallel reductions, overflow/underflow, and unit scale can dominate. Reproducible bits are not always required, but bounded decision outputs are.

**Verify stochastic models statistically.** Test random-number generator use, distribution sampling, seed/replay, independence/correlation, event ordering, stationarity/warm-up, replication, confidence intervals, and analytic moments for simplified cases. A single trajectory cannot verify a distributional implementation.

**Verify discrete-event semantics.** Define simultaneous-event priority, clocks, queue discipline, resource contention, cancellation, retries, termination, and initialization. Use tiny hand-traceable scenarios, conservation of entities/value, event-log invariants, and metamorphic changes such as splitting an equivalent arrival stream.

**Verify state and behavioral models.** Check syntactic well-formedness, types, guard completeness/overlap, determinism where required, unreachable states, deadlock/livelock, safety/liveness properties, timing, hierarchy/history, and interface events. Model checking proves properties only for the encoded model and assumptions.

**Verify algebraic/parametric models.** Check units, dimensions, sign conventions, coordinate frames, dependencies, cycle solution, real/nominal bases, ranges, constraints, and hand-calculated cases. Spreadsheet models require formula inspection, locked ranges, independent recomputation, and input/output separation.

**Verify reliability/safety models.** Check Boolean logic, minimal cut/path sets, event identity, probability bounds, dependency/common cause, mission time, repair assumptions, mutually exclusive/exhaustive states, and comparison with enumeration/simulation for small systems. Correct arithmetic on wrong independence remains invalid modeling, addressed also in validation/assumption review.

**Verify ML and data-driven implementations.** Control training/inference preprocessing, feature ordering/units, missing values, tokenization, label mapping, architecture, weights/checkpoints, precision/quantization, randomness, batching, serving code, thresholds, postprocessing, and version. Use reference vectors, invariants, metamorphic properties, cross-framework comparisons, gradient checks where applicable, and train/serve parity. Generalization, fairness, and intended-use accuracy belong to validation, though implementation verification is prerequisite.

**Challenge code comparison.** Independent codes can share equations yet use different discretizations, implementations, and teams, improving defect detection. Shared libraries, meshes, inputs, benchmarks, or ancestry create common-mode risk. Agreement is evidence, not an exact oracle.

**Separate calibration.** Calibration chooses parameters to improve agreement. Freeze verification cases before calibration where practical, and rerun them after implementation change. Never let fitted parameters compensate for a sign, unit, boundary, or algorithm defect.

**Separate sensitivity and UQ.** Sensitivity identifies influential inputs; UQ propagates specified uncertainties; neither shows code implements the model. They can expose suspicious insensitivity, discontinuity, or nonphysical response, generating verification tests.

**Use progressive complexity.** Begin with units and simplified exact problems, then coupled benchmarks, realistic calculations, and edge cases. When a complex case fails, smaller isolating cases support diagnosis. Retain regression suites across all previously found defects.

**Review evidence independence.** High-consequence models may require independent derivation, code implementation, verification team, benchmark, or technical review. Independence reduces shared error but must retain competence and configuration access.

**Report what remains unverified.** List functions/domains/branches not covered, unresolved anomalies, numerical regimes without convergence, dependence on unqualified tools/data, platform sensitivity, and user constraints. “Verified model” without a for-what statement is misleading.

The following executable fixture checks expected first-order convergence for one simple implementation.

<!-- bijux-verify: {"id":"model-verification-convergence-fixture","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"equation=y_prime_equals_minus_y\nexact_y_at_1=0.36787944\nsteps_10_solution=0.34867844\nsteps_10_error=0.01920100\nsteps_20_solution=0.35848592\nsteps_20_error=0.00939352\nsteps_40_solution=0.36323244\nsteps_40_error=0.00464700\nerror_ratio_10_to_20=2.044\nerror_ratio_20_to_40=2.021\nobserved_behavior=consistent_with_first_order_convergence\nstatus=declared_convergence_fixture_consistent\nevidence=synthetic_single_equation_numerical_behavior_only\n","stderr":""}} -->
```python
from math import exp

def explicit_euler(steps):
    step = 1.0 / steps
    value = 1.0
    for _ in range(steps):
        value += step * (-value)
    return value

exact = exp(-1.0)
solutions = {steps: explicit_euler(steps) for steps in (10, 20, 40)}
errors = {steps: abs(value - exact) for steps, value in solutions.items()}
print("equation=y_prime_equals_minus_y")
print(f"exact_y_at_1={exact:.8f}")
for steps in (10, 20, 40):
    print(f"steps_{steps}_solution={solutions[steps]:.8f}")
    print(f"steps_{steps}_error={errors[steps]:.8f}")
print(f"error_ratio_10_to_20={errors[10] / errors[20]:.3f}")
print(f"error_ratio_20_to_40={errors[20] / errors[40]:.3f}")
print("observed_behavior=consistent_with_first_order_convergence")
print("status=declared_convergence_fixture_consistent")
print("evidence=synthetic_single_equation_numerical_behavior_only")
```

The observed ratios near two are consistent with first-order global error for this smooth problem and implementation. They do not prove all code branches, different equations, stiffness, stability, floating-point platforms, physical adequacy, or operational prediction.

## Definitions and Notation

Let the real-world system be $R$, conceptual model $C$, mathematical model $M$, implementation $I$, and simulation output $Y_h$. Model validation concerns adequacy of $M/C$ relative to $R$ for use $u$. Verification concerns $I\approx M$ and numerical $Y_h\approx Y$, the exact solution of $M$, within use-relevant error.

For formal order $p$ and characteristic resolution $h$, an asymptotic discretization error may behave $e_h\approx Ch^p$. Refining $h$ by factor two gives $e_h/e_{h/2}\approx2^p$. Observed order

$$
p_{obs}=\frac{\log(e_h/e_{h/2})}{\log 2}
$$

is meaningful only when errors use a trustworthy reference and calculations lie in an appropriate convergence regime.

Decompose total prediction discrepancy conceptually into implementation/numerical error, input/parameter uncertainty, measurement error, and model-form discrepancy; correlations and nonlinear interactions prevent naïve addition. Verification targets implementation and calculation error, while recording interactions with the others.

## Mechanisms, Invariants, or Proof Structure

A defensible model-verification claim follows this chain:

1. define intended use, outputs, domain, accuracy, consequence, and acceptance authority;
2. baseline conceptual/mathematical/logical specification and transformations;
3. control implementation, inputs, dependencies, solver, platform, precision, and configuration;
4. derive verification requirements from terms, branches, invariants, limits, algorithms, and transformations;
5. execute exact/manufactured/benchmark/metamorphic/independent tests and preserve failures;
6. estimate calculation-specific discretization, iterative, roundoff, and sampling errors;
7. review coverage, common-mode risk, anomalies, corrections, regressions, and limitations;
8. authorize bounded use or require more evidence, then reverify after impactful change.

The central invariants are transformation fidelity, configuration identity, independent known-property oracles, error separation, convergence evidence, and separation of verification from empirical validity.

## Alternatives and Trade-Offs

**Analytical solution versus benchmark.** Exact solutions offer strong oracles but often only simple cases. Benchmarks add complexity but contain reference uncertainty. Use a hierarchy and document trust.

**MMS versus natural exact cases.** MMS exercises implemented terms systematically and convergence order; manufactured forcing may be nonphysical and miss boundary/constitutive regimes. Combine with physical limiting and benchmark cases.

**Unit/property tests versus end-to-end model runs.** Units isolate defects; integrated runs expose transformations/coupling. Both are needed because local correctness does not prove composition.

**Formal proof/model checking versus dynamic tests.** Formal methods cover encoded state spaces/properties under assumptions; dynamic tests catch toolchain, numeric, data, platform, and mapping defects. Preserve abstraction limits.

**Independent implementation versus reference code.** Independent derivation reduces common-mode risk but costs expertise/time. Reference implementations accelerate checks but may share defects. Match independence to consequence.

**Uniform versus adaptive refinement.** Uniform studies are interpretable and expensive; adaptive methods target error but make convergence/error estimation and mesh comparison harder. Verify adaptation indicators and conservation.

**Bitwise reproducibility versus statistical/numerical equivalence.** Bitwise equality aids debugging but may be impractical across parallel hardware. Define output tolerances/distributional invariants appropriate to decision without accepting uncontrolled nondeterminism.

**Tool-generated versus handwritten implementation.** Generation improves consistency and trace, but generator/templates/configuration become verification subjects. Handwritten code gives control with more transcription risk.

## Failure Modes and Misconceptions

**“It matches experiments, so code is verified.”** Calibration or error cancellation can produce agreement. Use known mathematical/logical truth for verification.

**“No compiler errors means model verification.”** Syntax/type success does not establish semantic transformation or numerical accuracy.

**“Residual is small, so solution is accurate.”** Residual-to-error relation depends on conditioning, discretization, norm, scaling, and solver.

**“A finer mesh is truth.”** It may still be pre-asymptotic, unstable, wrong geometry/physics, or converging to a wrong branch.

**“Conservation proves correctness.”** Many wrong solutions conserve globally. Check local behavior, terms, order, boundaries, and other invariants.

**“Two codes agree independently.”** Investigate shared ancestry, libraries, inputs, meshes, algorithms, and benchmark calibration.

**“Sensitivity analysis verifies the model.”** It shows response to inputs, not fidelity of implementation.

**“Validation absorbs numerical error.”** Unestimated numerical error contaminates empirical discrepancy and calibration.

**“Random outputs cannot be verified.”** Distributional moments, invariants, seeds, event semantics, and analytic simplified cases provide statistical oracles.

**“A model is verified forever.”** New use, domain, solver, dependency, precision, hardware, data, or transformation can invalidate credit.

## Worked Examples

### Example 1

**Situation.** A thermal code uses Celsius where the equation requires absolute temperature in a radiation term.

**Reasoning.** Dimensional/unit review and limiting benchmark expose the semantic implementation defect even if calibrated emissivity matched one experiment. Fix conversion, add typed units and regression tests, rerun verification and invalidate affected validation/calibration.

**Conclusion.** Empirical agreement cannot compensate for an incorrect model transformation.

### Example 2

**Situation.** A second-order solver shows errors 0.12, 0.07, and 0.04 under halving mesh size.

**Reasoning.** Ratios 1.71 and 1.75 are below expected four. Possible causes include pre-asymptotic grids, singularities, geometry, boundary treatment, iterative error, reference error, or implementation defect. Refine further, isolate terms, tighten solver, inspect norms/fields, and use MMS.

**Conclusion.** Do not claim formal order until observed convergence is explained in the relevant regime.

### Example 3

**Situation.** A state machine compiles but occasionally deadlocks.

**Reasoning.** Check guard completeness/overlap, event priority, timeouts, hierarchy/history, concurrent regions, unreachable states, and liveness. Model-check bounded properties and execute minimal traces. Compilation verified syntax only.

**Conclusion.** Behavioral model verification requires semantic state/transition properties, not tool acceptance.

### Example 4

**Situation.** A Monte Carlo queue model reproduces the analytic mean for M/M/1 but not variance.

**Reasoning.** Inspect random distributions, interarrival/service parameterization, warm-up, termination, event ordering, independence, replications, and variance estimator. Matching mean tests one moment and can conceal correlation or sampling defects.

**Conclusion.** Verify stochastic implementations with multiple analytic/distributional properties and statistical uncertainty.

### Example 5

**Situation.** A spreadsheet lifecycle model has correct totals but one cost appears twice with opposite signs in intermediate sheets.

**Reasoning.** Totals cancel accidentally. Trace formulas/ranges, units/time basis, named inputs, sign conventions, dependencies, and hand cases. Use conservation/reconciliation and perturb each input to check expected response.

**Conclusion.** Output agreement can hide paired defects; transformation and sensitivity structure must be verified.

### Example 6

**Situation.** Generated code differs from the source model after a tool upgrade.

**Reasoning.** Freeze model, generator/template/configuration/runtime versions; compare semantic intermediate representation; run golden/reference vectors, round-trip and regression tests; inspect release notes/known issues; qualify tool or independently verify critical generated behavior.

**Conclusion.** The generator is part of the evidence chain and tool changes trigger re-verification.

### Example 7

**Situation.** Two CFD codes agree within 0.5% for drag.

**Reasoning.** Determine shared geometry, mesh generator, turbulence model, boundary data, property tables, libraries, discretization ancestry, and calibration. Compare independent methods, conduct refinement/uncertainty, and benchmark simpler cases. Agreement is encouraging but not an oracle.

**Conclusion.** Quantify common-mode risk before calling cross-code comparison independent verification.

### Example 8

**Situation.** An ML model's notebook and serving endpoint disagree on the same record.

**Reasoning.** Compare schema, feature order/units, missing values, normalization, categorical mapping, tokenization, checkpoint, precision/quantization, batching, threshold, and postprocessing. Create canonical reference vectors and train/serve parity regression.

**Conclusion.** Implementation verification includes the entire data-to-decision pipeline, not only learned weights.

### Example 9

**Situation.** A fault tree tool reports top probability greater than one.

**Reasoning.** Use small enumerated cases; inspect event identity, repeated/basic dependence, mutually exclusive states, gate algorithms, approximations, common cause, and probability bounds. Cross-check exact Boolean enumeration and simulation.

**Conclusion.** Probability bounds and small known cases are powerful invariants for safety/reliability model verification.

### Example 10

**Situation.** A verified orbit model is reused for a long-duration mission with different perturbations and precision needs.

**Reasoning.** Prior code tests may transfer, but new terms, integration horizon, accumulated roundoff, step control, coordinate/time standards, ephemerides, events, and output accuracy require impact analysis and calculation verification. Model validity also needs separate reassessment.

**Conclusion.** Verification credit is use/domain/configuration specific, not a permanent model badge.

## Cross-Program Connections

- **API/service engineering:** executable contract/reference models need semantic, state, timing, and generator verification before conformance results are trusted.
- **Platform engineering:** reproducible builds, controlled runtimes, artifact provenance, numerical hardware, and automation underpin model evidence.
- **Data engineering:** schemas, units, feature transformations, lineage, missingness, train/serve parity, and postprocessing are model implementation.
- **Object-oriented programming:** class invariants, state encapsulation, generated code, numerical libraries, and collaboration tests affect model fidelity.
- **Functional programming:** equational reasoning, algebraic laws, pure reference implementations, types, and property tests provide strong verification oracles.
- **Numerical computing:** discretization, stability, conditioning, convergence, solver tolerance, precision, and manufactured solutions govern calculation error.
- **Reliability/safety:** fault trees, RBDs, Markov/state models, hazards, dependencies, and probability calculations require invariant and small-case checks.
- **Security:** formal models and proofs need implementation/tool/assumption mapping; model checking is not real-world threat validation.
- **MBSE/digital threads:** model transformations, consistency constraints, traceability, code generation, and authoritative configurations require semantic verification.
- **Decision analysis:** model credibility, error bounds, sensitivity, limitations, and intended use determine how much decision weight outputs deserve.

## References

1. NASA, [NASA-STD-7009: Standard for Models and Simulations—official active record](https://standards.nasa.gov/standard/nasa/nasa-std-7009), accessed 2026-08-31.
2. NASA, [NASA-STD-7009B: Standard for Models and Simulations](https://standards.nasa.gov/sites/default/files/standards/NASA/B/1/NASA-STD-7009B-Final-3-5-2024.pdf), 2024.
3. NASA, [NASA-HDBK-7009A: Handbook for Models and Simulations](https://standards.nasa.gov/sites/default/files/standards/NASA/A/0/nasa-hdbk-7009a.pdf), 2019.
4. NASA Glenn Research Center, [Verification Assessment](https://www.grc.nasa.gov/www/wind/valid/tutorial/verassess.html), accessed 2026-08-31.
5. NASA Glenn Research Center, [Overview of CFD Verification and Validation](https://www.grc.nasa.gov/www/wind/valid/tutorial/overview.html), accessed 2026-08-31.
6. NASA Kennedy Space Center, [Modeling and Simulations FAQ](https://public.ksc.nasa.gov/mns/faq/), accessed 2026-08-31.
7. U.S. Department of Energy Office of Nuclear Energy, [Predictive Simulation and V&V/UQ](https://www.energy.gov/ne/predictive-simulation), accessed 2026-08-31.
8. NIST, [PFHub Benchmark 7: Method of Manufactured Solutions](https://pages.nist.gov/pfhub/benchmarks/benchmark7.ipynb/), accessed 2026-08-31.
9. NIST, [A B C of Engineering Statistics and a Reference Benchmark Approach to V&V of Multi-Physics Simulations](https://www.nist.gov/publications/b-c-engineering-statistics-and-reference-benchmark-approach-verification-and-validation), 2005.
10. NASA, [Modeling and Simulation of Engineering Systems](https://ntrs.nasa.gov/api/citations/20010110412/downloads/20010110412.pdf), 2001.

## Exercises

### Exercise 1

Classify each activity as conceptual-model verification, code verification, calculation verification, validation, calibration, sensitivity analysis, or UQ: unit checking; matching wind-tunnel data; fitting drag coefficient; grid refinement; perturbing density inputs; proving state-machine deadlock freedom; and propagating a parameter distribution.

### Exercise 2

For errors 0.040, 0.011, and 0.0030 under two successive halvings of $h$, compute observed orders for each pair. Interpret cautiously and list at least four reasons the result may not prove global second-order correctness.

### Exercise 3

Design verification for a discrete-event emergency-department simulation with patient arrivals, priority queues, shared rooms, staff shifts, abandonment, and transfer. Include hand cases, invariants, stochastic checks, event semantics, and calculation error.

### Exercise 4

A neural network matches validation data but its serving system uses a different missing-value rule and quantized precision. Construct a verification and evidence-repair plan while separating model validity.

### Exercise 5

Assess reuse of a verified thermal model after changes to geometry, mesh generator, contact model, solver library, GPU precision, operating envelope, and intended decision from screening to safety-margin certification.

## Answers to the Exercises

### Answer 1

Unit checking is conceptual/mathematical and transformation verification; it can also be an implementation invariant. Matching wind-tunnel data is validation when the experiment/domain/use are appropriate. Fitting drag coefficient is calibration. Grid refinement is calculation verification and may support code-order checks when a known solution is available. Perturbing density inputs is sensitivity analysis. Proving encoded state-machine deadlock freedom is formal model/code verification within the encoded assumptions. Propagating a parameter distribution is UQ.

Activities can interact but their claims do not merge. A calibrated model is not necessarily valid; sensitivity/UQ do not establish correct implementation; a proof of the model does not validate reality; and validation data interpretation is ambiguous if verification error is uncontrolled.

### Answer 2

For halving, $p=\log(e_h/e_{h/2})/\log2$. First pair: $\log(0.040/0.011)/\log2\approx1.86$. Second: $\log(0.011/0.0030)/\log2\approx1.87$. These are near but below two and consistent with approaching second-order behavior under some assumptions.

They do not prove global second-order correctness because the reference solution/error may be uncertain; grids may not be asymptotic; iterative/roundoff error may contaminate; singularities/discontinuities/boundaries reduce order; only one output norm/location may be checked; mesh/refinement may not be systematic; code terms/branches outside this case remain untested; error cancellation can mimic order; geometry/input changes may accompany refinement; and physical model validity is separate. Use MMS/exact cases, more refinements, multiple norms/fields, tightened solvers, and term-isolating benchmarks.

### Answer 3

Baseline entities, attributes, arrival/service distributions, priority and preemption, room/staff resources, shift/calendar rules, abandonment/transfer, event priority for simultaneous events, clocks, initialization/warm-up, termination, randomness, and outputs. Use tiny deterministic hand traces: one patient/no queue; two priority classes arriving together; room unavailable; staff shift boundary; abandon exactly at service event; transfer while queued. Define tie-breaking explicitly.

Invariants include patient conservation by mutually exclusive state, nonnegative queue/resources/time, resource capacity, chronological event processing, unique completion/abandon/transfer, probability normalization, and audit reconciliation. Compare simplified M/M/1 or known queue moments where assumptions match; test sampled distributions, correlations, seeds/replay, independent replications, confidence intervals, and variance—not only means. Metamorphic cases scale arrival/service time consistently, remove capacity constraints, or split equivalent streams. Verify calculation error from warm-up, run length, replications, rare-event sampling, and stochastic confidence. Validation against real workflows/data and intended-use outcomes remains separate.

### Answer 4

Freeze notebook and serving configurations, schema, preprocessing, missing-value semantics, feature order/units, checkpoint, framework/library, precision/quantization, batching, threshold, and postprocessing. Create canonical vectors spanning missingness, boundaries, categories, extreme values, and typical records with expected intermediate features/logits/output. Compare train/evaluation/serve transformations stepwise. Decide and specify one authoritative missing-value rule, fix or update requirements/model deliberately, and regression-test it.

Quantify quantization error over representative and adversarial vectors, check class/rank/threshold flips, numerical stability, supported hardware, and tolerance. Verify exported weights/architecture, reference framework versus endpoint, deterministic settings or statistical bounds, and artifact digest. Preserve prior mismatch as anomaly and invalidate affected empirical validation until the implementation under validation is identified. Then reassess accuracy/generalization/fairness/calibration with independent data for the intended use; good prior validation cannot excuse train/serve implementation mismatch.

### Answer 5

Partition change. Geometry invalidates geometric representation and old calculation results. A new mesh generator requires quality metrics, conservation, MMS/benchmark and convergence checks; old solver code tests may partly transfer but old meshes do not. Contact-model change alters mathematical specification and requires unit/limit/benchmark/correlation work. Solver-library change requires API/algorithm/configuration comparison, regression, convergence, tolerances, known defects, and possibly independent reference. GPU precision requires roundoff, nondeterminism, conditioning, scaling, cross-precision/platform, and output-bound checks. Expanded envelope requires new boundary/parameter/coupling cases and calculation verification.

Changing intended use from screening to safety certification raises accuracy, independence, coverage, uncertainty, trace, review, and authority needs even if code were unchanged. Reestablish acceptance criteria, critical outputs/margins, model assumptions/domain, verification plan, independent review, configuration control, and calculation-specific error bounds. Reuse unaffected unit/exact/manufactured tests with provenance, but rerun under the new implementation/platform. Perform separate model validation and UQ for the new real-world domain/decision. Prior “verified” status is supporting evidence, not sufficient certification credit.
