---
module_id: SYSENG-055
program: Systems Engineering
level: 2
module_number: 55
title: Parametric Models
status: complete
last_verified: 2026-08-31
---

# Parametric Models

## One-Page Review

### Governing question

How can engineers bind configured system properties to calculations and constraints so budgets, margins, sensitivities and tradeoffs are reproducible and dimensionally valid—while preserving provenance, uncertainty, correlation, solver behavior and intended-use limits?

### Essential definitions

- A **parametric model** is a governed network of typed quantities, values, equations/calculations, predicates/constraints, bindings, configurations, assumptions and evidence used to reason quantitatively about a system.
- A **quantity kind** is a measurable property such as mass, duration, energy or temperature difference. A **unit** is a chosen reference scale for expressing a quantity value. Equal numeric values with different quantity kinds need not be comparable.
- A **value property** is a modeled property of a definition or configured usage whose value has type, quantity kind, unit, source, status, configuration and uncertainty metadata.
- A **calculation** maps declared inputs to outputs using an expression or algorithm. A **constraint** is a Boolean predicate or relation that permissible values must satisfy.
- A **binding** asserts that a parameter and a property represent the same value in the modeled context; copying a number does not preserve binding or provenance.
- A **budget** allocates a limited resource or performance quantity across contributors and margins under an explicit composition rule.
- A **limit/requirement** defines an allowable bound. An **allocation** assigns a portion to an element. An **estimate** predicts a value. A **measurement** observes a measurand. Their authority and uncertainty differ.
- **Margin** is the signed difference or ratio between a governing limit/capability and an estimated demand using declared sign convention and configuration. Margin is not uncertainty or reserve.
- **Reserve** is controlled capacity/resources held by an authority for future allocation or uncertainty/risk response; it should not be hidden inside estimates.
- **Tolerance** is an allowed variation in a specified property or process. **Uncertainty** describes incomplete knowledge about a value/result. They are not synonyms.
- **Sensitivity** measures how output changes with an input or assumption. **Identifiability** concerns whether available evidence can distinguish parameter values or model structures.
- **Calibration** estimates parameters from data. **Validation** assesses model agreement/adequacy against reality or an acceptable referent for an intended use and domain.
- **Covariance/correlation** captures dependence among uncertain inputs; assuming independence can substantially misstate aggregate uncertainty.
- A **solver configuration** specifies algorithm, direction, initialization, tolerances, stopping criteria, versions and failure handling for evaluating coupled relations.

### Central model, mechanism, or theorem

Let configured inputs be vector $x$, parameters $\theta$, outputs $y$, constraints $g$, evidence state $E$ and configuration $\gamma$:

\[
y=f(x,\theta;\gamma),\qquad g(x,y,\theta;\gamma)\le 0.
\]

Every quantity carries dimension $dim(q)$. Addition/subtraction require compatible dimensions; multiplication/division compose them. A result is meaningful only when bindings preserve quantity kind, unit conversion and configuration.

For differentiable $y=f(x_1,\ldots,x_n)$, first-order combined uncertainty includes covariance:

\[
u_y^2\approx \sum_i\left(\frac{\partial f}{\partial x_i}\right)^2u_i^2
+2\sum_{i<j}\frac{\partial f}{\partial x_i}\frac{\partial f}{\partial x_j}u_{ij}.
\]

This approximation requires local linearity and credible uncertainty inputs. Simulation or other methods may be needed for nonlinear, discontinuous, bounded, multimodal or tail-sensitive models.

### Critical invariants

- Every quantitative conclusion names intended use, baseline/configuration, mode/environment, model/version, input cutoff, solver and authoritative output owner.
- Each property has stable identity, quantity kind, dimension/unit, direction/status, source/provenance, applicability and uncertainty or an explicit absence rationale.
- Requirements, allocations, estimates, measurements, assumptions, calibration parameters, reserves and margins are distinguishable.
- Equations and constraints expose definitions, sign conventions, reference conditions, domains, piecewise logic, corrections and limitations.
- Bindings connect authoritative properties; no manual duplicate silently becomes an independent source.
- Dimensional and unit checks occur before numerical interpretation, including offset units, reference frames, gauge/absolute values and currency/time bases.
- Budget composition matches physics/logic: additive, maximum, root-sum-square, probabilistic, nonlinear or scenario-specific as justified.
- Conservation and balance invariants include every material contributor, loss, conversion and boundary flow for the declared scope.
- Uncertainty includes relevant Type A/statistical and Type B/other components, model form, data, calibration, numerical and scenario uncertainty as applicable.
- Correlations, common causes and shared assumptions are represented or bounded; independence is never the silent default for consequential conclusions.
- Solver convergence, infeasibility, multiple solutions, discontinuities, initialization and numerical tolerance are observable and never converted to a plausible value silently.
- Sensitivity, break-even, boundary and adversarial cases test decision robustness; calibration data are not reused as independent validation without disclosure.
- Verification checks equations/code/implementation; validation checks intended-use adequacy against relevant referents. Neither is implied by a green constraint.
- Changes propagate across properties, equations, requirements, structure, behavior, hazards, tests, decisions and generated reports with historical baselines retained.

### Common failures

Common failures include storing untyped numbers; mixing mass and force or energy and power; ignoring temperature offsets, time/currency bases or gauge/absolute pressure; treating an equality as a one-way algorithm without solver rules; double-counting derived inputs; binding properties from different variants; using nominal values for worst cases; adding quantities whose composition is max/RSS/nonlinear; hiding reserve inside estimates; calling positive point margin “high confidence”; omitting correlation; using percentages on near-zero or signed bases; accepting solver output after nonconvergence; calibrating and validating on the same data; fitting parameters outside physical meaning; extrapolating beyond domain; reporting excessive digits; replacing a controlled property with a spreadsheet copy; changing an input to make a constraint pass; and presenting Monte Carlo percentiles without distributions, dependence, seed, sample adequacy or model validity.

### Compact example

A teaching spacecraft budget sums three declared mass terms to 160 kg against a 175 kg limit, three point power loads to 260 W against 320 W supply, and two hours of constant 260 W demand to 520 Wh against 600 Wh usable battery energy. The arithmetic yields positive point margins. It does not establish worst-case duty cycle, conversion losses, temperature/aging effects, correlated growth, transient peaks, battery delivery power, uncertainty or probability of compliance.

### Connections

SYSENG-051 governs model authority, SYSENG-052 supplies quantitative requirements, SYSENG-053 supplies state/time/duty behavior and SYSENG-054 supplies configured properties and allocations. SYSENG-055 binds them into analyzable relations. SYSENG-056–060 address language, consistency, simulation, reviews and tools; earlier uncertainty, sensitivity, readiness, risk and trade modules govern conclusions drawn from the numbers.

## Governing Question

Can a reviewer reproduce each displayed result from authoritative configured properties, understand every quantity and equation, see which assumptions and evidence support it, determine whether the solver actually succeeded, and explain how uncertainty and model validity bound the decision?

If the answer is “the dashboard is green,” the quantitative argument is incomplete. A parametric model should expose the chain from requirement and physical/operational meaning through calculation and evidence, not make arithmetic look more authoritative by placing it in a system model.

## Why This Matters

System qualities couple. Increasing battery capacity adds mass and thermal load; redundancy adds power and failure paths; lower latency increases compute/network demand; tighter manufacturing tolerance raises cost/yield risk. Parametric models make these couplings executable and support early budget balancing, sensitivity and trade studies. Poor models propagate a wrong unit, stale configuration or hidden correlation with extraordinary efficiency.

NASA-HDBK-1009A integrates calculations/parametric content into system modeling and generated work products. SysML 2.0 defines calculations with directed parameters/results and constraints as predicates. NASA-STD-7009B requires modeling and simulation to be verified and validated with a recorded domain for intended use. Its 2026 handbook provides current implementation guidance. NASA Technical Assessment uses measures and trends for technical decisions.

NIST Technical Note 1297 distinguishes uncertainty components and provides first-order propagation including covariance and sensitivity coefficients. It also stresses clear reporting of components, methods and coverage factors. Those measurement principles do not automatically define design-forecast uncertainty, but their discipline—define the measurand/model, include material inputs and report assumptions—transfers usefully.

## Prerequisites and Retrieval

Before constructing a parametric model, retrieve:

1. exact decision/intended use, system boundary, configuration/variant, lifecycle, modes/scenarios, environments, time/currency base and required confidence/consequence;
2. quantitative requirements/limits, allocations, reserves, acceptance criteria, rationale, authority and waivers;
3. structure/property hierarchy, behaviors/duty cycles, interfaces/boundary flows, resources, budgets, hazards and decisions;
4. authoritative measurements, tests, supplier data, estimates, forecasts, expert judgments and external datasets with configuration/provenance;
5. quantity kinds, units, reference conditions/frames, tolerances, conversions, sign conventions and significant-digit policy;
6. equations/algorithms, constraint definitions, bindings, composition rules, corrections, domains, assumptions and model-form alternatives;
7. probability distributions/intervals, correlations, calibration/validation data, uncertainty/sensitivity evidence and data-quality limitations;
8. solver/tool/library/code versions, initialization, tolerances/stopping, seeds/samples, validation checks, logs and prior baselines.

Use a retrieval test: “Power margin is 20 percent.” Ask demand versus supply convention, operating mode/duty/time window, DC/AC and voltage/reference, average/peak/transient, conversion and harness losses, battery temperature/age/state, redundancy/fault state, measurement/estimate source, uncertainty/correlation, reserve, exact configuration and authority. A percentage without a denominator and conditions is not an engineering conclusion.

## Learning Objectives

After completing this module, you should be able to:

1. represent value properties, calculations, constraints and bindings with stable configured semantics;
2. distinguish limit, allocation, estimate, measurement, tolerance, reserve, uncertainty and margin;
3. perform quantity-kind, dimensional, unit/reference and sign-convention checks;
4. choose and justify budget composition, conservation and coupling relations;
5. expose input/output provenance, assumptions, corrections and domains;
6. configure and diagnose solvers for coupled, nonlinear, discontinuous or underdetermined relations;
7. propagate uncertainty with correlation and select alternatives when first-order methods fail;
8. analyze sensitivity, identifiability, break-even boundaries, robustness and value of information;
9. verify implementation and validate intended-use adequacy without data leakage or extrapolation;
10. baseline, review, communicate and update quantitative conclusions with bounded evidence claims.

## Core Exposition

**Frame the quantitative question.** State whether the model supports feasibility screening, allocation, optimization, supplier acceptance, safety margin, certification, operations or trade selection. Name configuration, scenarios, consequence and decision threshold. Required fidelity and credibility depend on use; a concept estimate need not be a certification model.

**Define the modeled quantity.** Specify physical/operational meaning, system boundary, mode, reference, population/statistic, time horizon and method. “Mass” can mean dry, wet, current best estimate, measured as-built or launch limit. “Latency” needs events, load and percentile. Use stable quantity kinds and controlled units.

**Classify every value.** Mark requirement limit, allocation, design estimate, measured observation, supplier guarantee, assumed value, calibration parameter, derived result, reserve or margin. Record owner, source, date, method, configuration, status, uncertainty and expiration. This prevents a convenient estimate from quietly replacing a requirement.

**Model calculations and predicates separately.** A calculation produces a value from directed inputs under an algorithm. A constraint tests permissible relationships. Mathematical equality may support multiple solve directions, but a production workflow must specify which variables are known/unknown, solver and solution selection. Do not let a modeling tool infer authority from solvability.

**Bind rather than transcribe.** Connect a calculation parameter to the authoritative system property or controlled snapshot. If tool federation requires copying, record source ID/version, transformation, digest, refresh/failure and precedence. Detect stale bindings. Never edit the downstream copy to resolve an upstream problem.

**Check dimensions and units first.** Validate dimension algebra and explicit conversions. Offset units such as Celsius need affine conversion; angles may be dimensionless mathematically but semantically critical; gauge and absolute pressure differ; mass and force require gravitational context; nominal currency needs year/exchange/inflation bases. Preserve unit metadata through APIs/exports.

**Define sign and margin conventions.** For a maximum demand limit, margin may be $L-E$; for a minimum capability, $E-L$. State whether positive is favorable and denominator for percent margin. Handle negative/zero baselines and asymmetric thresholds explicitly. Do not compare margins with different conventions.

**Construct budgets from physics and ownership.** Identify every contributor, allocation owner and reserve authority. Choose sum, maximum, convolution, RSS, envelope, conditional or nonlinear composition. Prevent double counting of parent and child estimates. Reconcile allocated totals with governing limit and reserve; report unallocated and overallocated portions.

**Model conservation and conversion.** Define control volume/boundary and balance sources, sinks, storage, losses and transformations for mass, energy, charge, data, money or population. Check steady versus transient conditions. An apparently balanced internal model can omit an external boundary flow.

**Represent behavior-dependent parameters.** Bind duty cycles, modes, states, workload, environmental conditions and event sequences. Average power times duration may miss peak delivery, startup, sleep transition and failures. Use scenario-specific values or time models and aggregate only with justified exposure weights.

**Represent uncertainty explicitly.** List measurement, manufacturing, environment, operating, supplier, forecast, calibration, numerical and model-form components. Distinguish variability from epistemic uncertainty when decisions need it. Use intervals, distributions, ensembles or scenarios appropriate to evidence. Avoid false probability when only bounds/judgments exist.

**Include dependence.** Shared suppliers, environmental drivers, measurement calibration, growth rules and common models correlate inputs. Record covariance/correlation or scenario/common-factor structure. Independence is an assumption requiring justification. Perfectly correlated contributors add differently from independent contributors.

**Choose propagation method.** First-order propagation works near a smooth operating point with modest uncertainty. Use analytic higher-order, interval, polynomial, sampling, surrogate or scenario approaches for nonlinear/discontinuous/tail behavior. Validate transformations and convergence/sample adequacy. Compare methods near decision boundaries.

**Configure coupled solvers.** Identify algebraic loops, differential/discrete coupling, discontinuities, inequality constraints and multiple solutions. Set initialization, scaling, bounds, tolerance, stopping and failure handling. Check residuals and constraint violation. A solver returning a number after maximum iterations is not success.

**Test identifiability.** Multiple parameter sets can fit the same data. Inspect sensitivity rank, correlations, posterior/profile likelihood or experiment design as appropriate. Do not present calibrated parameter precision the data cannot support. Prefer new evidence targeting decision-sensitive ambiguity.

**Analyze sensitivity and boundaries.** Compute local/global sensitivity, scenarios, break-even values, rank/feasibility flips and interaction effects. Check extremes, missing contributors and adversarial combinations. Translate influential inputs into design control, measurement, supplier action, reserve, risk or monitoring.

**Calibrate without hiding discrepancy.** Define parameters eligible for calibration and physical/prior bounds. Preserve raw data, preprocessing, objective/loss, weights, algorithm and fit diagnostics. Do not tune correction factors merely to pass a requirement. Record residual structure and competing model forms.

**Validate independently.** Compare predictions to independent, configuration-relevant test/field/prototype or accepted referent data across intended domain. Predefine metrics/tolerances, inspect bias/distribution/boundaries and document validation domain. Calibration data can support fit but are not independent validation unless properly partitioned and disclosed.

**Verify implementation.** Check equations against sources, dimensions, code/tool transcription, algorithms, solvers, numerical precision, test cases, limiting cases and independent calculations. Version source, libraries, unit databases and environments. Verification says the model was built as intended; it does not prove the intended model represents reality.

**Manage surrogate and reduced models.** Record training/design space, high-fidelity source, errors, constraints and extrapolation detection. Validate at held-out/boundary points. A fast surrogate enables optimization but can invent attractive solutions outside its domain.

**Report honestly.** Show configured inputs, outputs, margins, uncertainty/intervals, sensitivity, model/solver status, evidence and limitations. Use meaningful significant digits. Distinguish current, predicted, allocation and requirement lines. State probability meaning and coverage factor/basis; avoid color-only dashboards.

**Govern change.** Trace a property/equation change to requirements, structure, behavior, interfaces, other budgets, hazards, verification, suppliers, cost/schedule and decisions. Recompute with controlled toolchain, compare baselines and review unexpected differences. Preserve the model that supported each prior decision/build.

The following checker computes three point budgets from declared values. It verifies arithmetic and positive margins only; it does not model uncertainty, transients, losses, correlation, aging, mode changes or physical validation.

<!-- bijux-verify: {"id":"parametric-budget-point-check","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"mass_terms=3\nmass_total_kg=160.0\nmass_limit_kg=175.0\nmass_margin_kg=15.0\nmass_margin_pct=8.6\npower_terms=3\npower_total_w=260.0\npower_supply_w=320.0\npower_margin_w=60.0\nenergy_required_wh=520.0\nbattery_usable_wh=600.0\nenergy_margin_wh=80.0\nconstraint_violations=0\nstatus=declared_budgets_within_limits\nevidence=declared_point_estimates_only\n","stderr":""}} -->
```python
mass_kg = {"payload": 42.0, "bus": 88.0, "propellant": 30.0}
mass_limit_kg = 175.0
power_w = {"payload": 120.0, "avionics": 80.0, "thermal": 60.0}
power_supply_w = 320.0
duration_h = 2.0
battery_usable_wh = 600.0

mass_total = sum(mass_kg.values())
mass_margin = mass_limit_kg - mass_total
power_total = sum(power_w.values())
power_margin = power_supply_w - power_total
energy_required = power_total * duration_h
energy_margin = battery_usable_wh - energy_required
violations = sum(value < 0 for value in (mass_margin, power_margin, energy_margin))

print(f"mass_terms={len(mass_kg)}")
print(f"mass_total_kg={mass_total:.1f}")
print(f"mass_limit_kg={mass_limit_kg:.1f}")
print(f"mass_margin_kg={mass_margin:.1f}")
print(f"mass_margin_pct={100 * mass_margin / mass_limit_kg:.1f}")
print(f"power_terms={len(power_w)}")
print(f"power_total_w={power_total:.1f}")
print(f"power_supply_w={power_supply_w:.1f}")
print(f"power_margin_w={power_margin:.1f}")
print(f"energy_required_wh={energy_required:.1f}")
print(f"battery_usable_wh={battery_usable_wh:.1f}")
print(f"energy_margin_wh={energy_margin:.1f}")
print(f"constraint_violations={violations}")
print("status=" + ("declared_budgets_within_limits" if violations == 0 else
                   "declared_budget_violation"))
print("evidence=declared_point_estimates_only")
```

The point energy calculation also assumes constant simultaneous load and usable energy already accounts for all losses/limits. Those assumptions must be replaced or justified for a real battery and mission profile.

## Definitions and Notation

Let quantitative property record be

\[
q=(id,kind,value,unit,source,status,\gamma,mode,time,uncertainty,version).
\]

Let maximum-type margin $M_{max}=L-E$ and minimum-type margin $M_{min}=E-L$. Percent margin requires declared denominator $d$:

\[
M_\%=100\frac{M}{d},\qquad d\ne 0.
\]

Constraint residual $r=g(z)$ and solver tolerance $\epsilon$ permit a numerical check $r\le\epsilon$, but engineering acceptance may require physical margin far larger than numerical tolerance.

Sensitivity coefficient $c_i=\partial f/\partial x_i$ is local and carries units $unit(y)/unit(x_i)$. Normalization improves comparison but can obscure scale choices; report both where useful.

## Mechanisms, Invariants, or Proof Structure

**Mechanism 1—question and quantities.** Define intended use, configuration, property semantics, authority, provenance, units and value classes.

**Mechanism 2—relations and budgets.** Define calculations, predicates, bindings, sign, composition, conservation, behavior dependence and reserve.

**Mechanism 3—uncertainty and computation.** Represent uncertainty/dependence, choose propagation, configure solvers and diagnose identifiability.

**Mechanism 4—credibility.** Perform sensitivity/boundary checks, calibration, independent validation and implementation verification with domain limits.

**Mechanism 5—decision and lifecycle.** Report margins/confidence honestly, trace risk/trades, govern changes and preserve historical configured evidence.

Arithmetic correctness is necessary but insufficient. The quantitative argument also needs semantic correctness, credible inputs, appropriate model form, successful computation and intended-use validation.

## Alternatives and Trade-Offs

**Declarative constraints** allow multiple solve directions and integration. **Directed calculations** are easier to execute/review. Use explicit solver direction and avoid accidental underdetermination.

**Analytic models** expose mechanisms and sensitivities. **Numerical simulation** handles richer nonlinear/time behavior but raises verification and computational burdens. Use the simplest credible model for the decision.

**Intervals** avoid unjustified probability. **Distributions** support risk decisions when evidence/interpretation justify them. **Scenarios** capture structural/model alternatives. Often use all three without conflation.

**Tight coupling to authoritative properties** reduces drift but can make models/toolchains brittle. **Snapshots** improve reproducibility but can stale. Govern source versions, refresh and precedence.

**High-fidelity models** improve represented phenomena but can obscure assumptions and be unidentifiable. **Reduced/surrogate models** enable exploration but need domain/error controls.

**Central budget ownership** preserves reserve and consistency. **Distributed estimates** improve domain fidelity. Federate contributions with one composition/authority and review cadence.

## Failure Modes and Misconceptions

**“The units cancel, so the model is valid.”** Dimensional consistency cannot establish correct physics, scope or data.

**“Positive margin means compliant.”** Point margin can be overwhelmed by uncertainty, mode, transient or omitted contributors.

**“Tolerance is uncertainty.”** Tolerance specifies allowable variation; uncertainty states knowledge about realized/measured value.

**“Independent is conservative.”** It may under- or overstate tails depending on sign/dependence. Model plausible correlation.

**“More Monte Carlo samples fix the model.”** Sampling reduces numerical error for the declared distributions/model, not model-form or input bias.

**“A solver value is a solution.”** Check convergence, residuals, bounds, multiplicity and physical plausibility.

**“Calibration proves accuracy.”** Fit can exploit flexibility; validate independently in the intended domain.

**“The strictest input is worst case.”** Coupled worst cases depend on signs, constraints, correlation and feasible combinations.

**“A spreadsheet and system-model result match.”** They may share the same wrong source or formula; verify independently.

**“Percent margin is comparable across budgets.”** Denominators, sign, uncertainty and consequence differ.

## Worked Examples

### Example 1

**Mass/force error.** A supplier reports weight in newtons and a model binds it to kilograms. Dimensional validation blocks the sum; gravitational context/conversion and authority are corrected.

### Example 2

**Temperature offset.** Averaging Celsius values after treating conversion as scale-only produces error. The quantity library uses affine conversion and distinguishes temperature from temperature difference.

### Example 3

**Correlated growth.** Three subsystem estimates share one maturity growth factor. Independent RSS understates aggregate uncertainty; a common-factor/covariance model changes reserve need.

### Example 4

**Mode-specific power.** Average nominal power passes, but simultaneous startup peak violates supply/current/voltage constraints. Behavior and transient electrical models govern the boundary case.

### Example 5

**Algebraic loop.** Thermal loss changes temperature, resistance and loss. The nonlinear solver needs bounds, initialization, residual/convergence checks and multiple-solution analysis.

### Example 6

**Calibration leakage.** A degradation model reports excellent error on the data used to fit parameters. Held-out lots/climates reveal bias; the validation domain and uncertainty are revised.

### Example 7

**Hidden double count.** A subsystem total and its components both feed system mass. Identity/provenance and parent-child rules detect the duplicate contribution.

### Example 8

**Surrogate extrapolation.** An optimizer selects a design outside the surrogate training envelope. Domain detection rejects it and requests high-fidelity evaluation/new sampling.

### Example 9

**Budget authority.** Teams consume all allocated capacity while program reserve is counted twice. One controlled composition separates allocations, current estimates, reserve and governing limit.

### Example 10

**Field discrepancy.** Observed energy use exceeds prediction. Engineers align configuration/duty/weather/sensor calibration, test implementation and model form before updating parameters or requirement.

## Cross-Program Connections

**Platform engineering.** Capacity, cost, latency, availability and error budgets require workload/mode, correlation, reserve and runtime-validation semantics.

**API and service engineering.** Queueing, retry, rate-limit, payload, bandwidth and SLO models require units, distributions, dependencies and protocol behavior.

**Data engineering.** Volume, freshness, quality, compute/storage and pipeline-cost models need lineage, event-time behavior, uncertainty and configured datasets.

**Object-oriented programming.** Domain value objects and invariants can enforce units/contracts, while performance/resource evidence remains system- and runtime-dependent.

**Functional programming.** Pure calculations, types and property tests improve reproducibility; numerical methods, effects, data provenance and validation still govern conclusions.

## References

1. NASA, *NASA Systems Modeling Handbook for Systems Engineering*, NASA-HDBK-1009A, active 2025. <https://standards.nasa.gov/standard/NASA/NASA-HDBK-1009>
2. Object Management Group, *Systems Modeling Language Specification Version 2.0*, 2025. <https://www.omg.org/spec/SysML/2.0>
3. NASA, *Standard for Models and Simulations*, NASA-STD-7009B, active 2024. <https://standards.nasa.gov/standard/nasa/nasa-std-7009>
4. NASA, *NASA Handbook for Models and Simulations*, NASA-HDBK-7009B, active 2026 index. <https://standards.nasa.gov/systems-and-subsystem-test>
5. NASA, *Systems Engineering Handbook, Section 6.7: Technical Assessment*, current web edition. <https://www.nasa.gov/reference/6-7-technical-assessment/>
6. NASA, *Systems Engineering Handbook, Section 6.8: Decision Analysis*, current web edition. <https://www.nasa.gov/reference/6-8-decision-analysis/>
7. NIST, *Technical Note 1297: Guidelines for Evaluating and Expressing the Uncertainty of NIST Measurement Results*, current web edition. <https://www.nist.gov/pml/nist-technical-note-1297>
8. NIST, *Technical Note 1297, Appendix A: Law of Propagation of Uncertainty*. <https://www.nist.gov/pml/nist-technical-note-1297/nist-tn-1297-appendix-law-propagation-uncertainty>
9. NASA, *Cost Estimating Handbook, Appendix G: Cost Risk and Uncertainty Methodologies*. <https://www.nasa.gov/wp-content/uploads/2020/11/ceh_appg.pdf>
10. NASA, *Systems Engineering Handbook, Section 6.6: Technical Data Management*, current web edition. <https://www.nasa.gov/reference/6-6-technical-data-management/>

## Exercises

### Exercise 1

Turn the point spacecraft budget into a decision-capable mass, power and energy model with modes, uncertainty, correlation, reserve, transient constraints and validation evidence.

### Exercise 2

Audit a parametric model containing unitless values, duplicated copied inputs, a solver that reached iteration limit, independent triangular distributions, a 12-percent positive margin and no validation domain.

### Exercise 3

Design a coupled thermal-electrical battery model for cold-start feasibility, including equations, states, uncertainty, solver controls, evidence and safety limits.

### Exercise 4

Explain how to calibrate and validate a queueing/capacity model used for a public service whose demand changes by location, time and disruption state.

### Exercise 5

A supplier changes a component estimate and the system dashboard remains green. Define the impact, recomputation, review and decision evidence needed before accepting the new margin.

## Answers to the Exercises

### Answer 1

Fix mission/system configuration, lifecycle, environments and decisions. Separate mass requirement/launch capability, program reserve, subsystem allocations, current best estimates, measured as-built values and growth uncertainty. Include every configured hardware/software-enabling physical contributor, propellant/consumables, harness/fasteners/adapters and contingency without parent-child double count. State dry/wet and reference gravity only where weight matters.

Create behavior-derived power/energy profiles for startup, nominal mission phases, communication, peak compute, thermal extremes, degraded/fault/recovery, charging and safe modes. Model simultaneous versus mutually exclusive loads, duty cycles, transients, conversion/harness losses, voltage/current limits and timing. Battery usable energy and deliverable power depend on temperature, age, state of charge, rate, cell imbalance, protection and reserve; do not use one scalar universally.

For every input record source, configuration, estimate/measurement/requirement class, unit, method, date, uncertainty and owner. Represent supplier/maturity/environment common factors and correlations. Use interval/scenario/probabilistic propagation appropriate to evidence, with sensitivity and break-even analysis. Keep management reserve under explicit authority and report probability/coverage/basis rather than point margin alone.

Verify equations, units, binding freshness, profiles, solver and limiting cases independently. Validate subsystem/system predictions against representative test, prototype and flight/field evidence without reusing all calibration data. Record domain and discrepancies. Report mass, peak/current/voltage and energy margins by scenario, uncertainty, influential contributors, constraint violations and unmodeled risks. Link changes to requirements, structure, behavior, thermal/power interfaces, risk, verification and decisions; monitor as-built/operated updates.

### Answer 2

Freeze the model, tool/library/solver version, input snapshot and output logs. Identify intended use, configuration and governing constraints before interpreting 12 percent. Assign quantity kinds, units, reference conditions and time/currency bases to every value; quarantine incompatible or ambiguous bindings. Trace each copied input to one authority, remove duplicate contributions and use controlled bindings/snapshots with freshness evidence.

Treat iteration-limit output as failed or indeterminate, not a solution. Inspect equations, algebraic loops, scaling, initialization, bounds, discontinuities, multiple solutions, residuals and constraint violations. Re-run only after solver acceptance/stopping criteria and failure handling are defined; compare an independent calculation or alternative solver on benchmark/limiting cases.

Challenge triangular distributions: source/min-mode-max meaning, bounded support, evidence, epistemic versus variability and configuration. Map shared supplier, environment, calibration, growth and model assumptions into covariance/common-factor/scenarios. Independence is not conservative by definition. Test alternative distributions/bounds and tail-sensitive outcomes.

Recompute point and uncertainty-aware margins with explicit limit, estimate, reserve, sign and denominator. Run sensitivity, boundary, worst-feasible and break-even cases. Establish conceptual and empirical validation for intended use, referent data, metrics, acceptance and domain; keep calibration/validation separate. Report prior results invalid, corrected outputs, limitations and impact on requirements, architecture, risk, suppliers, test and decision. A green result returns only after evidence, not formatting.

### Answer 3

Define cell/module/pack configuration, chemistry/lot/age, initial state of charge and temperature distribution, ambient/cooling, startup load/current profile, duration, controller/protection and cold-start success/safety criteria. Couple open-circuit voltage and internal resistance to temperature, state of charge, age and rate; current to demanded electrical power and terminal voltage; heat generation to resistive/electrochemical loss; thermal balance to heat capacity, conduction/convection and cooling; energy/state-of-charge integration to time. Include contactor/precharge and heater behavior.

Model modes/states before start, preheat/precharge, cranking/load, run, protection trip and recovery. Constraints cover minimum terminal voltage, maximum current, cell temperature/gradient, power delivery, isolation and no unsafe charge/discharge. Units and reference signs must be explicit. Nonlinear feedback exists: low temperature raises resistance, which increases loss/heating and voltage drop.

Inputs include measured/calibrated cell curves, manufacturing/aging variation, thermal properties/contact resistance, sensor bias, ambient/load profiles and control timing. Represent correlations within lots/cells and common environment, model-form discrepancy and extrapolation. Configure transient solver step/tolerance, bounds, initialization, event detection, residual/energy conservation and nonconvergence handling. Explore multiple/boundary outcomes.

Verify equations/code/dimensions against controlled sources, analytic limiting cases and independent energy balance. Calibrate only eligible parameters using planned data. Validate with held-out cells/modules/packs across cold temperatures, age, SOC, rates and relevant boundary/fault cases, recording domain. Analyze sensitivity and value of information. Stage use with conservative margins/protection and link model version/input configuration to each decision; reopen on chemistry/lot/age/control/environment or discrepancy changes.

### Answer 4

Define intended decisions: staffing, capacity, facility/routing, admission control or emergency reserve. Define service requests, classes/priorities, arrival and service processes, abandon/retry/return, queues, routing, resources/skills/shifts, geography, opening hours, dependencies and disruption modes. Outcomes include wait distributions/percentiles, abandonment, completion quality, access/equity, utilization, overtime and failure—not average throughput alone.

Collect versioned request/event logs with stable IDs and clock semantics, staffing/schedule/absence, service start/end and outcome, location/population/access, routing, closures, incidents and environment. Audit missing/censoring, duplicate events, policy changes and people excluded from digital logs. Segment time/location/request classes where mechanisms differ while avoiding overfit.

Calibrate arrival/service/abandon/routing/resource parameters and dependencies on a training period/sites with uncertainty and plausible priors/bounds. Model correlation, seasonality, batch arrivals, common disruptions, priority/preemption and human adaptation. Preserve loss function and residual diagnostics. Identifiability may require observations or designed pilots rather than more fitting.

Validate prospectively or on held-out periods/sites/events, including peaks, outages, staff shortages and policy changes. Compare wait/queue/utilization/outcome distributions and subgroup/location performance with predeclared metrics. Validate conceptual rules with workers/users. Report domain and transportability limits. Use scenario/sensitivity/break-even analysis and conservative reserve for tail/disruption. Monitor drift and recalibrate/revalidate through controlled versions; never let aggregate fit erase unequal access or service quality.

### Answer 5

Preserve supplier old/new source documents/models, part/software version, configuration/applicability, method, data, assumptions, uncertainty, approval/change notice and effective date. Determine whether the value is requirement/guarantee, current estimate, measurement or model output and whether quantity kind, units/reference/mode match the bound property. Do not overwrite the old baseline.

Trace the property through bindings, conversions, budgets, coupled equations, modes, interfaces, thermal/power/mass/performance, hazards, verification, cost/schedule, spares/maintenance and decisions. Check whether the same supplier driver affects other inputs, creating correlation or double count. Assess variant and as-built applicability. Validate model/dashboard refresh, source digest and generator/solver logs.

Recompute with controlled toolchain, convergence/residual/constraint checks and independent spot calculation. Compare baseline deltas and explain nonlinear secondary changes. Update uncertainty/distributions/covariance, not just point value. Run sensitivity, boundary, break-even and relevant scenario/tail analysis. Separate limit, allocation, reserve, estimate and margin; identify whose reserve/acceptance authority is affected.

Review with property/budget owner, supplier/interface, domain, configuration, risk and decision authorities. Require updated verification/validation if method, component or domain changed. Record dissent and evidence gaps. If accepted, authorize new configured baseline, propagate downstream artifacts/tests/risks/contracts and preserve supersession. Monitor delivered/field values and trigger reopening on variance, configuration, validation, supplier or margin/confidence thresholds. A green dashboard is output, not acceptance evidence.
