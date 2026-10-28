---
module_id: SYSENG-073
program: Systems Engineering
level: 2
module_number: 73
title: Analysis, Inspection, Demonstration, and Test
status: complete
last_verified: 2026-08-31
---

# Analysis, Inspection, Demonstration, and Test

## One-Page Review

### Governing question

Which verification method—or defensible combination of methods—can generate objective evidence adequate for this exact requirement, configuration, condition, consequence, and decision without claiming more than the method can observe or infer?

### Essential definitions

- **Inspection** determines conformance by examining an item, record, drawing, code, marking, workmanship feature, configuration, or directly measurable static attribute without exercising the relevant dynamic function. It can use calibrated measurement; it is not limited to unaided sight.
- **Analysis** derives a conformance judgment from mathematical reasoning, calculation, data reduction, formal reasoning, modeling/simulation, similarity, or other analytical techniques. Its credibility depends on premises, model form, inputs, numerical implementation, uncertainty, domain, and review.
- **Demonstration** operates, adjusts, reconfigures, or uses an item to show a specified capability, commonly with limited detailed quantitative data. It is appropriate when observable successful performance is the criterion; it is weak when margins, distributions, or precise limits matter.
- **Test** applies controlled inputs or conditions to an article and records detailed response data against predeclared quantitative or categorical criteria. Test observes sampled conditions, not every possible future state.
- A **method** describes how evidence is produced; the **purpose** is the requirement-conformance claim. A test may also support validation, qualification, acceptance, or model correlation, but those purposes remain distinct.
- An **oracle** is the predeclared rule that maps observations and uncertainty to pass, fail, or inconclusive.
- **Measurement uncertainty** characterizes dispersion and doubt attributable to the measurement result. It is different from product variability, model uncertainty, and operational variability, though all can affect a decision.
- A **guard band** tightens the acceptance region relative to the requirement limit to manage decision risk under uncertainty.
- **Verification by similarity** uses evidence from a heritage item plus an explicit comparison showing that differences do not invalidate the claim.
- **Triangulation** uses methods with sufficiently different assumptions or failure modes to strengthen a claim; repeating one hidden assumption through several tools is not independent corroboration.

### Central model, mechanism, or theorem

For requirement $r$, choose method set $M_r$ by constructing an inference chain

$$
r,B,C \longrightarrow O \longrightarrow M \longrightarrow D \longrightarrow J,
$$

where $B$ is the requirement and product baseline, $C$ applicable conditions, $O$ required observables, $M$ selected method/article/environment/procedure, $D$ configuration-bound data or findings with uncertainty, and $J$ the bounded conformance judgment. Method adequacy requires: the observable represents the required property; the activity covers applicable conditions; assumptions and decision error are controlled; anomalies remain visible; and the conclusion is no broader than the evidence.

### Critical invariants

- Select method from the requirement and inference need, not from an inherited matrix or preferred team tool.
- Define the object, baseline, conditions, article, environment, procedure, oracle, uncertainty, data, and limitations for every method.
- Inspection can establish only attributes actually observable with qualified access and instruments.
- Analysis cannot be stronger than its premises, inputs, model validity, numerical verification, uncertainty treatment, and domain of applicability.
- Demonstration establishes observed capability under declared scenarios; it does not silently establish quantitative margin, reliability, or exhaustive behavior.
- Test provides discrete evidence under controlled conditions; finite passing samples do not prove universal absence of failure.
- Qualification stresses, verification criteria, validation context, acceptance screens, and certification packages retain separate purposes even when they reuse data.
- Combined methods preserve separate claims, assumptions, and discrepancies; agreement is meaningful only when failure modes are not wholly shared.
- Configuration identity includes hardware/software, dependencies, parameters, data, interfaces, tools, models, instrumentation, procedures, and people where behavior depends on them.
- Raw observations remain separable from transformations, findings, discrepancy dispositions, waivers, and authorization.
- A waiver authorizes defined nonconformance; it does not convert a failed method result into passed verification.
- Change impact analysis determines whether method, coverage, and evidence remain valid.

### Common failures

Common failures include assigning every requirement to test; calling document review “analysis” to avoid inspection rigor; using simulation without model validity; treating heritage as automatic similarity; demonstrating a quantitative tolerance with no instrumentation; measuring what is easy instead of what the requirement states; testing nominal points but claiming the envelope; ignoring warm-up, aging, loads, modes, interactions, and recovery; accepting a mean when a percentile or maximum is required; using an instrument whose uncertainty consumes the tolerance; changing thresholds after observing data; rerunning until pass without preserving failures; claiming independence from models sharing inputs; confusing zero observed failures with proven reliability; and declaring “test error” without causal evidence.

### Compact example

A synthetic four-claim package uses inspection for a required label, guarded analysis for an 85°C limit, demonstration for a nine-step service action, and test for a 150 ms latency limit. All four bounded criteria pass: the label matches; predicted temperature 82°C plus 2°C model allowance remains below 85°C; all nine declared actions complete; and the maximum of five sampled latencies is 130 ms. These results establish only the synthetic criteria. Five latency samples cannot prove a population tail, one scripted demonstration cannot prove every maintainer succeeds, and the analysis allowance is not automatically a validated uncertainty bound.

### Connections

Requirements determine observables and oracles; planning determines levels, articles, facilities, resources, and readiness; model V&V qualifies analysis; metrology qualifies inspection/test data; human factors qualifies demonstrations; configuration and anomaly control preserve evidence; validation and acceptance use but do not redefine the results.

## Governing Question

Can the team justify why its selected methods make the specified property observable and decidable over the applicable configuration and conditions, while bounding measurement, model, sampling, human, environment, and interpretation uncertainty?

The four labels are not administrative categories. They encode different inference mechanisms. Inspection reasons from direct examination. Analysis reasons through a model or derivation. Demonstration reasons from observed use/capability with limited data. Test reasons from controlled stimulation and detailed measured response. The same physical event can produce several evidence types, but every credited claim needs an explicit chain.

## Why This Matters

Method mistakes create false assurance and waste. Testing a static marking in an environmental chamber is expensive but adds little; inspecting a complex timing property is impossible; demonstrating a safety margin without quantitative measurement is misleading; analyzing a phenomenon with an invalid model is precise fiction. Good selection yields adequate evidence at proportionate cost and risk.

NASA's current Product Verification guidance defines analysis, demonstration, inspection, and test while emphasizing controlled requirements/configuration, prepared environments, approved procedures, enabling products, calibrated instrumentation, discrepancy handling, result analysis, and reports. NASA's technical-planning and V&V-outline guidance treats method selection as dependent on product form, hierarchy, lifecycle timing, resources, and intended evidence. FAA's Test and Evaluation Handbook provides a parallel operational taxonomy and requirement-matrix usage. These sources are contextual guidance, not proof that one vocabulary fits every governing standard.

Method choice affects architecture. If a critical internal property becomes inaccessible after assembly, the team may add built-in test, telemetry, access points, modular separation, proof-carrying artifacts, or lower-level verification. If a requirement demands an operational tail percentile, the design must support representative load generation and trustworthy time. Verification design and system design therefore co-evolve.

Evidence also carries decision risk. Measurement error can falsely accept a nonconforming item or falsely reject a conforming one. Model-form error can shift every analytical result. Human demonstrations can overestimate performance when expert testers replace representative maintainers. Finite tests may miss rare states. A method package is credible when these risks are identified, quantified where possible, challenged, and matched to consequence.

No single method dominates. Tests observe reality but only at sampled conditions and can be hazardous or destructive. Analysis can cover large domains and impossible conditions but depends on abstractions. Inspection is direct but limited to observable attributes. Demonstration communicates capability effectively but often lacks precision and repeatability. Strong programs use the least burdensome adequate method and corroborate high-consequence claims with methods whose limitations differ.

## Prerequisites and Retrieval

Before approving a method, retrieve:

1. exact requirement identifier/text, source/rationale, applicability, criticality, modes, conditions, thresholds, tolerances, units, timing, statistical meaning, and controlled baseline;
2. product/system configuration, hierarchy, architecture, interfaces, internal states, operational profiles, hazards, threats, failures, degraded/recovery behavior, human allocations, and external dependencies;
3. governing definitions, standards, certification/qualification/acceptance rules, independence requirements, authority, and approved tailoring;
4. proposed observable and its causal relationship to the required property, including proxies, transformations, latent variables, and possible confounders;
5. candidate methods, levels, article pedigree, environment, procedure, instrumentation/tools/models, data, people, resources, schedule, safety/security controls, and cost;
6. oracle with pass/fail/inconclusive regions, guard bands, uncertainty, statistical confidence/power, missing/outlier rules, stopping rule, and decision authority;
7. inspection access, illumination, resolution, sampling, instrument calibration, workmanship standards, document/code/drawing versions, and reviewer competence;
8. analysis equations, assumptions, boundary/initial conditions, parameter/input sources, model-form limits, numerical algorithms, mesh/time convergence, code verification, validation/correlation, sensitivity, uncertainty, and peer review;
9. demonstration scenario, initial state, scripted/allowed actions, participant population, training, equipment, workload, observation/recording, success definition, repetitions, abort, and representativeness;
10. test article/configuration, stimuli, range/interactions, preconditioning, controls, instrumentation loading, calibration/time sync, sampling, environment fidelity, repeatability, destructive effects, data acquisition/reduction, and teardown;
11. heritage/similarity evidence, old/new differences, original requirement/environment/use, manufacturing/supplier change, anomalies, data quality, and residual work;
12. discrepancy, invalid-run, deviation/waiver, corrective action, regression/retest, evidence retention, review, reporting, closure, and change-impact process.

Use an **inference audit**: begin with the intended judgment and work backward through decision rule, transformed result, raw observation, sensor/reviewer/model, procedure, article, environment, baseline, and requirement. Then challenge each arrow: could a different product state create the same observation, or could the required property hold while the method reports failure? These are false-accept and false-reject paths.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish analysis, inspection, demonstration, and test by inference mechanism rather than label;
2. derive observables and oracles from controlled requirements;
3. select method, level, article, conditions, and evidence quality proportionate to consequence;
4. assess measurement, model, numerical, sampling, operational, and human uncertainty;
5. use guard bands and inconclusive regions without changing requirements post hoc;
6. construct credible analysis through model verification, validation-for-use, sensitivity, and uncertainty;
7. design demonstrations that show bounded capability without implying unmeasured margins;
8. design tests that cover interactions, tails, failure/recovery, and instrumentation effects honestly;
9. combine methods and similarity evidence without double-counting shared assumptions;
10. report observations, findings, anomalies, dispositions, and limitations as distinct evidence objects.

## Core Exposition

**Parse the requirement first.** Identify subject, action/property, conditions, threshold, units, duration, population, exceptions, and required confidence. “The service shall respond quickly” cannot support a method. “At 2,000 admitted requests/s, 99.9% of complete transactions shall respond within 250 ms over a 60-minute interval” defines a much clearer test/analysis problem, though measurement and population details remain.

**Identify the true observable.** A proxy is defensible only when its relationship to the requirement is established. CPU utilization does not verify response time. A green indicator does not verify safe state unless indicator logic and physical state are independently linked. Trace transformations and potential confounders.

**Choose inspection for direct attributes.** Use inspection for identity, dimensions, markings, installed items, workmanship, record presence, static configuration, code/document conformance, and accessible physical features. Define equipment, sampling, access, illumination, resolution, calibration, reference standard, reviewer competence, and evidence capture. Dimensional measurement is an inspection even when quantitative.

**Challenge inspection subjectivity.** Visual workmanship criteria need defect exemplars, lighting/magnification, surface preparation, sampling, independent review, and disagreement rules. A checklist item “acceptable” without a reference and record is not objective evidence.

**Choose analysis for derivable claims.** Closed-form calculation, finite-element/thermal/network modeling, formal verification, static analysis, probabilistic reliability, data reduction, and similarity can establish properties not directly observable or safely testable. Specify equations/model, domain, inputs, assumptions, implementation, numerical error, validation data, uncertainty, sensitivity, and review.

**Separate model verification and validation.** Verify that the computational implementation solves the intended equations/logic correctly through review, unit/benchmark tests, convergence, conservation, and numerical checks. Validate that the model adequately represents the real phenomenon for this use. A correct solver of the wrong physics is not credible analysis.

**Quantify analytical margin.** Compare prediction plus appropriately combined uncertainty/margin with the requirement boundary. Avoid inserting an unexplained “engineering factor.” If uncertainty overlaps the boundary, the judgment may be inconclusive, prompting better data, test correlation, redesign margin, or authorized risk treatment.

**Use similarity as structured analysis.** Identify heritage configuration and evidence, then compare function, materials, geometry, manufacturing, software, interfaces, loads, environment, duty cycle, aging, maintenance, supplier, and consequence. Bound every difference. “Same family” is not a similarity argument.

**Choose demonstration for observable capability.** Demonstrations suit reachability, installation/removal, transport, start/stop, mode transition, servicing, basic human interaction, and other behaviors where successful operation is the criterion. Define scenario, participants, actions, initial/final state, allowed assistance, observation, repetition, and forbidden outcomes.

**Do not smuggle measurement into demonstration.** If a requirement contains a precise time, force, error, rate, percentile, or margin, detailed calibrated data usually make the activity a test (or test-plus-analysis), even if an audience observes it. The label matters because data quality and procedure rigor follow the claim.

**Choose test for controlled detailed evidence.** Specify inputs, combinations, ranges, article, modes, workload, environment, instrumentation, sampling, preconditioning, duration, repetitions, uncertainty, data reduction, oracle, and abort/recovery. Test the actual property rather than a convenient proxy.

**Cover the domain deliberately.** Use requirement boundaries, equivalence classes, design of experiments, pairwise/higher interactions, operational distributions, worst cases, transitions, and targeted adversarial cases. Nominal midpoint success says little about corners. Continuous domains require justified sampling and analysis between points.

**Distinguish performance distribution from measurement uncertainty.** Repeated latency varies because the system/workload varies; timestamp uncertainty affects each measurement. Estimate both. A percentile requirement needs a sampling model, sufficient observations, representative population, confidence, and rules for dependence/warm-up/censoring.

**Manage decision error.** If measured value $y$ has expanded uncertainty $U$ and upper limit $L$, accepting only when $y+U\le L$ is a simple conservative guard rule; other governing rules may allocate consumer/producer risk differently. State the rule before results and do not confuse uncertainty with safety margin.

**Account for instrumentation effects.** Sensors add mass, resistance, latency, load, heat, traffic, or observer effects. Logging can alter scheduling. Test harnesses can bypass real interfaces. Analyze intrusion and compare instrumented/uninstrumented behavior where material.

**Represent humans honestly.** A demonstration by expert designers may establish mechanical possibility but not representative maintainability or usability. Define anthropometry, skills, training, fatigue, PPE, tools, accessibility, workload, communication, and organizational conditions. Use validation evidence separately when intended-use claims are evaluated.

**Test fault and recovery behavior.** Verification includes applicable invalid inputs, boundary states, timeouts, partial failures, common dependencies, degraded modes, safe shutdown, data reconciliation, restart, rollback, maintenance, and recovery. Fault injection itself needs containment, realism, timing, and observability.

**Plan destructive and hazardous evidence.** Use dedicated qualification articles, analysis, coupon/component tests, margins, remote facilities, staged escalation, abort criteria, and equivalence evidence. Never endanger a unique deliverable or people merely because “test is strongest.”

**Combine methods with explicit division of labor.** Inspection confirms configuration; test correlates model and observes selected cases; analysis spans the envelope; demonstration shows operational steps. Map which conclusion each supports. If all use the same erroneous input, agreement does not triangulate.

**Preserve discrepancies and invalid runs.** Stop/contain as required, freeze configuration and raw data, classify product/procedure/environment/tool/instrument/data/execution causes, analyze impact, correct under change control, and rerun affected work. A later pass does not erase the original anomaly or regression implications.

**Report bounded judgments.** Record requirement/baseline, product configuration, method, article, conditions, procedure, tools/instruments/models, raw/processed data, uncertainty, findings, discrepancies, corrective actions, retest, reviewers, result, and limitations. “Pass” without this evidence is unauditable.

The following executable fixture illustrates one bounded claim per method.

<!-- bijux-verify: {"id":"verification-methods-fixture","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"claims=4\nmethods=analysis,demonstration,inspection,test\ninspection_label=passed\nanalysis_temperature_guarded=passed\ndemonstration_service_steps=passed\ntest_sampled_latency=passed\nmaximum_sampled_latency_ms=130\nstatus=declared_method_fixture_consistent\nevidence=synthetic_bounded_method_results_only\n","stderr":""}} -->
```python
label_observed = "EMERGENCY ISOLATION"
label_required = "EMERGENCY ISOLATION"
predicted_temperature_c = 82
analysis_allowance_c = 2
temperature_limit_c = 85
service_steps = [True] * 9
latency_samples_ms = [90, 95, 110, 130, 100]
latency_limit_ms = 150

results = {
    "inspection_label": label_observed == label_required,
    "analysis_temperature_guarded": (
        predicted_temperature_c + analysis_allowance_c <= temperature_limit_c
    ),
    "demonstration_service_steps": all(service_steps),
    "test_sampled_latency": max(latency_samples_ms) <= latency_limit_ms,
}

print(f"claims={len(results)}")
print("methods=analysis,demonstration,inspection,test")
for claim, passed in results.items():
    print(f"{claim}={'passed' if passed else 'failed'}")
print(f"maximum_sampled_latency_ms={max(latency_samples_ms)}")
print("status=declared_method_fixture_consistent")
print("evidence=synthetic_bounded_method_results_only")
```

The fixture does not establish inspection competence, model validity, uncertainty adequacy, representative maintainers, latency distribution, configuration control, or real compliance. Its five latency observations cannot support a population-tail claim.

## Definitions and Notation

Let $x$ be the true property, $L$ an upper requirement limit, $y$ a measured or predicted result, and $U$ an uncertainty/allowance defined under a stated method. A conservative rule may accept when $y+U\le L$, reject when a governing rejection rule is met, and otherwise return inconclusive. This rule is illustrative; contracts and standards can specify different decision rules.

For test cases $z_i$ drawn or selected from applicable domain $\Omega$, observations $d_i=f(O,c,z_i)+\epsilon_i$ combine product response and measurement error. Evidence at finite $z_i$ does not establish behavior for all $z\in\Omega$ without a justified partition, interpolation/model, exhaustive finite domain, or other inference.

For an analysis model $\hat f(z,\theta)$, distinguish parameter/input uncertainty $\theta$, model-form discrepancy, numerical error, and observation uncertainty. Sensitivity asks how outputs change with inputs/assumptions; validation-for-use compares model behavior with relevant reality; verification checks implementation/numerics.

## Mechanisms, Invariants, or Proof Structure

A defensible method decision follows this chain:

1. parse the controlled requirement and applicable domain;
2. identify the property, observable, and acceptable decision error;
3. select method, level, article, conditions, and oracle;
4. establish competence and credibility of instruments, reviewers, models, simulators, procedures, data, and people;
5. execute under configuration control and preserve raw evidence/deviations;
6. quantify measurement/model/sampling/operational uncertainty and challenge false-accept paths;
7. compare evidence with the predeclared rule, record fail/pass/inconclusive, and disposition discrepancies;
8. bound the conclusion and determine affected re-verification after change.

The governing invariants are observable validity, baseline/configuration identity, predeclared oracle, uncertainty visibility, evidence preservation, and claim proportionality. A more expensive method does not compensate for violating them.

## Alternatives and Trade-Offs

**Inspection versus demonstration.** Inspection is efficient for state/attribute; demonstration proves an action can occur. If correct installation must be visible and removable within time, use inspection for installation/configuration and instrumented test or demonstration for removal depending on precision.

**Analysis versus test.** Analysis covers broad/extreme domains and design exploration; test observes the real article at sampled points. Use test to correlate/validate models and analysis to extend bounded conclusions. Neither automatically overrides contradictory evidence.

**Demonstration versus test.** Demonstration suits qualitative capability and audience comprehension. Test suits detailed quantitative criteria, repeatability, margins, distributions, and diagnostics. Instrumentation alone does not decide; the credited claim does.

**Single versus combined method.** One method minimizes cost and conflicting records when it is adequate. Combined methods reduce uncertainty and expose different failure modes for high-consequence or model-dependent claims, but create configuration/alignment work and possible double counting.

**Direct versus proxy measurement.** Direct observables reduce modeling assumptions but may be inaccessible/intrusive. Proxies enable practical evidence but require a validated causal mapping and uncertainty budget.

**Physical versus virtual evidence.** Virtual methods safely scale conditions and faults; physical evidence captures unmodeled reality. Hybrid, software/hardware/human-in-loop configurations need interface, timing, and model credibility definitions.

**Deterministic versus statistical oracle.** Deterministic thresholds suit repeatable bounded properties. Variable/nondeterministic outcomes need population, sampling, dependence, confidence/power, and acceptable error rates. A deterministic maximum over a tiny sample is not a tail guarantee.

**Heritage similarity versus new work.** Similarity saves destructive/costly repetition when equivalence is strong. Novel environment, supplier, software, interface, duty, aging, or consequence narrows credit and requires targeted evidence.

## Failure Modes and Misconceptions

**“Test is strongest.”** A poorly designed test measures the wrong thing at a few points. Strength is claim-relative.

**“Inspection is only visual.”** Inspection includes qualified direct examination and dimensional/static measurement, plus controlled document/code/record review where appropriate.

**“Analysis means simulation.”** Analysis also includes calculation, proof, static analysis, data reduction, reliability/statistical reasoning, and similarity. Each needs premises and uncertainty.

**“The model is validated because it matches one test.”** Agreement may be calibration, coincidence, or shared bias. Validate across relevant phenomena/domain with reserved data and uncertainty.

**“Demonstrated once means reliable.”** One success shows bounded possibility under those conditions, not a probability or population result.

**“Five passing samples meet the maximum.”** They meet only the sampled-case oracle. A universal or percentile claim needs justified coverage/statistics.

**“Measurement is inside the limit, so pass.”** If uncertainty overlaps the boundary, decision risk may require a guard band or inconclusive result.

**“Rerunning to pass is harmless.”** Selective unrecorded reruns bias evidence. Preserve all runs and predeclare retry/invalid-run rules.

**“Two simulations independently agree.”** Shared equations, inputs, libraries, mesh, calibration data, or developers can create common-mode error.

**“Customer attendance makes a validation.”** Purpose/reference determine verification versus validation. Witnessing does not change the claim.

## Worked Examples

### Example 1

**Situation.** A requirement says every emergency handle shall have a durable red label with exact text.

**Reasoning.** Inspection is direct: identify production configuration, label material/color/text reference, lighting or calibrated color method, adhesion/workmanship criterion, access, sampling if multiple units, photographs/records, and reviewer. Pull-force durability may require a separate test or qualification.

**Conclusion.** Inspection closes observable label attributes; it does not prove durability conditions absent additional evidence.

### Example 2

**Situation.** A beam shall remain below 200 MPa for an inaccessible worst load; strain test is available at two lower loads.

**Reasoning.** Use verified finite-element or analytical model with controlled geometry/material/boundary/load inputs, convergence and uncertainty. Correlate with calibrated strain tests at reachable loads, investigate residuals, and propagate uncertainty to worst load. Accept only under the declared margin rule.

**Conclusion.** Combined test and analysis can cover the inaccessible condition, bounded by correlation and model domain.

### Example 3

**Situation.** A filter cartridge shall be replaceable without tools.

**Reasoning.** Demonstration on production-representative assembly can show removal/replacement with hands only. Define initial state, access, gloves/PPE, representative maintainer, allowed actions, correct final state, damage/leak prohibition, repetitions, and recording. If a maximum replacement time exists, instrument it as a test.

**Conclusion.** Demonstration is adequate for tool-free capability; quantitative maintainability needs test/statistical evidence.

### Example 4

**Situation.** A service shall keep 99.9th-percentile latency below 250 ms at declared load.

**Reasoning.** Design a test population/window, workload mix, admission policy, dependencies, modes, warm-up, time synchronization, sample size/confidence, dependence treatment, missing/censored requests, and percentile estimator. Instrumentation overhead and retry semantics matter. Analysis may extend to rare workload combinations.

**Conclusion.** A few fast requests or average latency cannot verify the tail requirement.

### Example 5

**Situation.** A team claims similarity because the new battery has the same part number as heritage.

**Reasoning.** Compare revision, cells/materials, supplier/site/process, firmware, age/storage, duty, thermal environment, charge algorithm, interfaces, loads, qualification standard, anomalies, and counterfeit/lot controls. Same number may conceal change. Bound credit and test differences.

**Conclusion.** Similarity is an analysis with evidence, not a naming shortcut.

### Example 6

**Situation.** Predicted temperature is 83.8°C, instrumented test reads 83.5°C, limit is 85°C, and expanded measurement/model uncertainties are about 2°C and 3°C.

**Reasoning.** Both central values pass, but their uncertainty regions overlap the limit. Do not average them as independent if they share boundary inputs/calibration. Investigate uncertainty, improve measurement/model, add margin, or apply the governing decision rule; result may be inconclusive.

**Conclusion.** Agreement of point estimates does not establish adequate guarded margin.

### Example 7

**Situation.** Formal analysis proves an access-control function enforces its policy model.

**Reasoning.** Verify proof/toolchain assumptions, model-to-code mapping, configuration, identities, storage, error handling, deployment policy, interfaces, and excluded side channels. Test integration and adversarial conditions not represented. The proof is strong within its abstraction, not universal security proof.

**Conclusion.** Formal analysis closes modeled properties only; implementation/environment mapping needs separate evidence.

### Example 8

**Situation.** An environmental test fails once, passes twice after reseating a connector, and the first run is labeled “setup error.”

**Reasoning.** Preserve all data/configuration. Determine whether seating is production/maintenance-representative, procedure ambiguous, connector design sensitive, instrumentation intrusive, or article nonconforming. Assess cause and impacted requirements, correct under control, then retest/regress. Two passes do not erase failure.

**Conclusion.** “Setup error” is a hypothesis requiring evidence and disposition.

### Example 9

**Situation.** Expert pilots demonstrate a recovery maneuver successfully, so the system is claimed usable by line pilots.

**Reasoning.** The demonstration may prove physical/control capability under expert operation. It does not validate representative training, workload, cue recognition, fatigue, or success distribution. Plan human-in-loop validation and, if specified, quantitative response/error verification.

**Conclusion.** Bound the demonstration to expert capability; do not generalize the participant population.

### Example 10

**Situation.** A data pipeline passes end-to-end output comparison, but the test uses a tiny clean dataset and no late, duplicate, or corrupt events.

**Reasoning.** Inspect schema/configuration/lineage, analyze transformation invariants, test representative volume and distribution, inject boundary/late/duplicate/reordered/corrupt cases, verify replay/reconciliation and observability, and demonstrate operator recovery if required. Preserve exact data/tool versions.

**Conclusion.** Nominal output equality is one bounded test, not verification of production data semantics and recovery.

## Cross-Program Connections

- **API/service engineering:** contract inspection, formal/schema analysis, workflow demonstration, and load/failure tests support distinct protocol and operational claims.
- **Platform engineering:** reproducible environments, observability, fault injection, deployment controls, and artifact provenance determine test credibility.
- **Data engineering:** dataset configuration, statistical populations, lineage, transformation invariants, replay, drift, and reconciliation affect both method and oracle.
- **Object-oriented programming:** inspections/reviews, unit/contract tests, state-space analysis, mocks, and integration tests need honest abstraction boundaries.
- **Functional programming:** types, equational reasoning, proof, property-based tests, and effect modeling offer complementary analytical/test evidence.
- **Security:** static/formal analysis, inspection, demonstration, penetration/fuzz testing, and threat simulation cover different adversarial claims.
- **Reliability/safety:** statistical demonstrations, accelerated tests, hazard controls, common cause, margins, destructive qualification, and uncertainty require method combinations.
- **Human factors:** demonstrations/tests need representative populations, tasks, equipment, workload, and decision rules.
- **Metrology/statistics:** calibration, traceability, uncertainty, guard bands, design of experiments, confidence, and power bound measured claims.
- **Governance:** baselines, readiness, anomalies, waiver, acceptance, certification, and change control preserve technical truth.

## References

1. NASA, [Product Verification, Systems Engineering Handbook section 5.3](https://www.nasa.gov/reference/5-3-product-verification/), updated 2023.
2. NASA, [Systems Engineering Handbook Glossary](https://www.nasa.gov/reference/appendix-b-glossary/), accessed 2026-08-31.
3. NASA, [Verification and Validation Plan Outline, Systems Engineering Handbook Appendix I](https://www.nasa.gov/reference/appendix-i-verification-and-validation-plan-outline/), accessed 2026-08-31.
4. NASA, [Technical Planning, Systems Engineering Handbook section 6.1](https://www.nasa.gov/reference/6-1-technical-planning/), accessed 2026-08-31.
5. NASA, [Product Validation, Systems Engineering Handbook section 5.4](https://www.nasa.gov/reference/5-4-product-validation/), accessed 2026-08-31.
6. Federal Aviation Administration, [Test and Evaluation Handbook, Version 5.0](https://www.faa.gov/sites/faa.gov/files/about/office_org/headquarters_offices/ang/TEHandbook.pdf), 2020.
7. Federal Aviation Administration, [Safety Issues and Shortcomings with Requirements Definition, Validation, and Verification Processes](https://www.faa.gov/sites/faa.gov/files/aircraft/air_cert/design_approvals/air_software/TC-16-39.pdf), 2016.
8. NIST, [Technical Note 1297: Guidelines for Evaluating and Expressing the Uncertainty of NIST Measurement Results](https://www.nist.gov/pml/nist-technical-note-1297), 1994; official current landing page accessed 2026-08-31.
9. NASA, [NASA-STD-7009: Standard for Models and Simulations](https://standards.nasa.gov/standard/nasa/nasa-std-7009), official standards record accessed 2026-08-31.
10. NASA, [NASA Systems Engineering Handbook, NASA/SP-2016-6105 Rev. 2](https://www.nasa.gov/wp-content/uploads/2018/09/nasa_systems_engineering_handbook_0.pdf), 2016.

## Exercises

### Exercise 1

Choose method(s) and justify observables, article, conditions, and oracle for: a serial-number marking; a maximum processor temperature across the operating envelope; tool-free filter replacement; a 99.95% successful recovery requirement; and absence of unauthorized privilege escalation under a specified policy model.

### Exercise 2

A pressure requirement has upper limit 100.0 kPa. A calibrated instrument reports 99.2 kPa with expanded uncertainty 1.1 kPa. An analyst reports 98.7 kPa with model allowance 2.0 kPa. Apply the simple guarded rule in this chapter separately, discuss correlation, and determine the honest status.

### Exercise 3

Design a combined inspection-analysis-test package for verifying an end-to-end data freshness requirement across sensors, network, pipeline, storage, API, and display. Include clocks, transformations, missing data, uncertainty, and fault/recovery cases.

### Exercise 4

Evaluate a proposed similarity claim between a qualified industrial controller and a new controller with the same enclosure and CPU but new firmware, supplier memory, power board, network, environment, and maintenance interval. Partition reusable and new evidence.

### Exercise 5

A team has 30 passing automated test reruns after two initial failures. Logs from the failures are incomplete; dependencies and test environment mutate daily. Construct a technically honest disposition and recovery plan, including what cannot be concluded.

## Answers to the Exercises

### Answer 1

Serial marking: inspection of production article against controlled content, location, legibility, durability/standard, with qualified access and record; durability may require test. Temperature: verified/validated-for-use thermal analysis spanning loads/environment/modes with sensitivity/uncertainty, correlated by instrumented tests at selected corners on representative article; oracle uses upper limit plus governing uncertainty/margin. Tool-free replacement: demonstration with representative article, maintainer, PPE/access, initial/final configuration, no tools/assistance/damage; instrumented test if time/force thresholds apply. Recovery success of 99.95%: controlled statistical test or operationally representative trials with defined population, failure types, independence/dependence, sample/confidence, duration, oracle, and analysis for untested space; one demonstration is inadequate. Privilege escalation: formal/static analysis against a precise policy/model plus code/model mapping, configuration inspection, integration and adversarial tests/fuzzing for implementation/environment/side-channel assumptions.

Each conclusion remains bounded by configuration and the requirement's actual quantifier. Multiple methods are warranted where model-to-reality, abstraction-to-implementation, or static-to-dynamic gaps dominate.

### Answer 2

For the illustrative upper-limit rule $y+U\le L$, measurement gives $99.2+1.1=100.3$ kPa, so it does not pass the guarded rule. Analysis gives $98.7+2.0=100.7$ kPa, also not passing. Central values below 100 are insufficient. Depending on the governing rejection rule, these results may be inconclusive rather than proof of nonconformance.

Do not average the two results automatically. They may share pressure calibration, boundary conditions, material or environment inputs, or the test may calibrate the model. Investigate uncertainty budgets, instrument resolution/calibration/loading, model form/input/numerical error, configuration match, and discrepancies. Improve measurement/model, increase design margin, or apply the contract/standard decision rule through proper authority. Honest status under only the stated rule is “not demonstrated as conforming; inconclusive pending disposition,” not pass.

### Answer 3

Define freshness from physical event time to displayed/consumed value, including source-clock accuracy, acquisition, buffering, network, event-time semantics, pipeline queues/windows, storage commit, API/cache, rendering, and user-visible timestamp. Inspect configurations, schemas, clock-sync policy, lineage, retention, cache/queue settings, and deployed versions. Analyze worst-case/queueing and timestamp uncertainty, clock drift, transformation semantics, and coverage between test points, with validated assumptions.

Test a representative integrated configuration using a traceable event/time source and synchronized measurement points. Cover load distributions, bursts, geography, partitions, clock skew, late/duplicate/reordered/corrupt events, backlog, cache invalidation, failover, replay, and recovery. Record missing/censored observations and instrumentation overhead. Oracle states the required percentile/maximum, interval, population, accuracy/uncertainty, stale-data behavior, and prohibited silent success. Reconcile physical/event/processing/observation time explicitly. Inspection establishes configuration, analysis covers domains, and test observes end-to-end behavior; none alone closes every freshness claim.

### Answer 4

Potentially reusable: enclosure dimensions/material/markings evidence if supplier/process/revision and environment remain within qualification; CPU evidence for unchanged part/revision/clock/cooling and applicable loads. Even these need configuration and anomaly comparison.

New or substantially reworked: firmware requirements, code/static/formal/unit/integration evidence; supplier-memory timing/endurance/error behavior; power-board electrical, thermal, EMC, fault and safety evidence; network protocol/performance/security/interoperability; new environmental stresses; and maintenance/aging effects from changed interval. Reassess thermal/power interactions because the “same” CPU/enclosure now sees new board/firmware/load. Reuse prior methods, fixtures, models, and procedures only after their configuration/use validity is shown. Produce a difference matrix, similarity rationale per claim, targeted correlation, and system/interface tests. “Same controller family” cannot close altered evidence domains.

### Answer 5

Preserve all available runs and mark the two failures unresolved/incompletely observed; do not let 30 reruns erase them. Freeze current product, dependency, environment, data, seed, tool, and test versions. Reconstruct changes across runs, improve logging and chain of custody, reproduce in a controlled immutable environment, and determine whether product, dependency, environment, timing, resource contention, test harness, oracle, or execution caused failure. Treat flakiness as an anomaly with consequence-based severity.

Define retry and invalid-run criteria before further runs. Repair the product or evidence system under change control, then run targeted reproduction, affected regression, boundary/stress variants, and independent review where consequence warrants. Control dependencies and environment; preserve every result. If failures cannot be reproduced or causally invalidated, the affected requirement remains inconclusive or failed under its governing rule. Thirty conditional passes support behavior in those mutable runs only; they do not prove absence of the original defect, reliability probability, or production conformance.
