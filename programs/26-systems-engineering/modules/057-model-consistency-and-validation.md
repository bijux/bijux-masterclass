---
module_id: SYSENG-057
program: Systems Engineering
level: 2
module_number: 57
title: Model Consistency and Validation
status: complete
last_verified: 2026-08-31
---

# Model Consistency and Validation

## One-Page Review

### Governing question

How can engineers determine whether a configured system model is internally coherent, correctly implemented and adequate for a declared decision—without converting a successful rule check, simulation fit or review into a claim stronger than its evidence?

### Essential definitions

- **Well-formedness** means an artifact satisfies the grammar, metamodel constraints and other construction rules of its declared language/version.
- **Conformance** is demonstrated fulfillment of a specified standard, schema, profile or contract. The claim must name the exact conformance target and tested scope.
- **Consistency** means selected model statements can coexist under declared semantics and project invariants. It is relative to scope, configuration, logic and assumptions; absence of a detected contradiction is not truth.
- **Completeness** is sufficient coverage relative to an explicit purpose, scope and required information set. No finite model is complete in every possible respect.
- A **model rule** is an executable or reviewable predicate over model content. A **violation** is evidence that the rule predicate failed; it is not automatically an engineering defect until applicability and rule correctness are confirmed.
- **Static validation** evaluates model rules without executing the modeled behavior. **Dynamic analysis** evaluates executions, state exploration, simulations or generated implementations under declared semantics.
- **Verification of a model** asks whether the conceptual model, mathematics, data transformations, software and numerical implementation were built as intended and solve the stated equations/rules correctly.
- **Validation of a model** asks whether the model and its results adequately represent the relevant real or virtual referent for an intended use over a declared domain.
- **Product verification** assesses conformance to specified requirements. **Product validation** assesses satisfaction of stakeholder needs and intended use. These system-lifecycle meanings must not be collapsed into language-tool “validation.”
- A **validation referent** is the observation, experiment, accepted higher-fidelity model, benchmark, operational record or expert/domain body of knowledge against which adequacy is assessed.
- **Calibration** estimates model parameters or corrections from data. Reusing the same evidence as independent validation without disclosure creates leakage and optimistic results.
- **Uncertainty qualification** identifies, characterizes and communicates input, parameter, numerical, model-form and scenario uncertainty relevant to conclusions.
- **Sensitivity analysis** determines how output or decision behavior changes with inputs, parameters, assumptions or model form.
- **Credibility** is the justified confidence in model-and-simulation results for a particular use. It depends on evidence, risk and authority, not one universal score.
- A **false positive** is a reported violation where the model is acceptable under the intended rule; a **false negative** is an undetected consequential defect. Both matter when designing checks.
- **Acceptance criteria** are predeclared conditions for accepting evidence or a model for a use. **Accreditation/authorization** is a designated authority's decision to approve use; tools do not confer it automatically.

### Central model, mechanism, or theorem

Let a controlled model at commit/configuration $c$ be $M_c$, a set of consistency rules be $R=\{r_1,\ldots,r_n\}$ and each rule return pass, fail, unknown or not-applicable:

$$
V(M_c,R)=\{(r_i,x,status,evidence): status\ne pass\}.
$$

A release policy may require zero unresolved severity-weighted violations, but the policy must preserve `unknown` rather than silently treating it as pass. For intended use $u$ and validation domain $D_u$, compare model response $y_M(x)$ with referent $y_R(x)$ using predeclared metrics $m_j$ and thresholds $\tau_j$:

$$
A(M,u,D_u)=\bigwedge_j m_j(y_M,y_R;D_u)\le \tau_j.
$$

Even when $A$ is true, the warranted conclusion is bounded: the tested model version was adequate under the sampled conditions, metrics, uncertainty treatment and decision consequences. It does not establish universal validity, correctness outside $D_u$, or validity after model/data/configuration change.

### Critical invariants

- Every check identifies model project, branch/commit, system configuration, language/library/profile, tool/rule-set version, query scope, access context and timestamp.
- Syntax, schema, metamodel, project-rule, cross-view, physical, behavioral, numerical, evidence and stakeholder checks remain distinguishable.
- `fail`, `unknown`, `not applicable`, `waived`, `suppressed`, `not run` and `tool error` are separate states with owner and rationale.
- Rules are themselves versioned, tested on positive and negative fixtures, reviewed for applicability and monitored for false positives/negatives.
- Stable identity, type, ownership, multiplicity, units, direction, mode, lifecycle and configuration agree across authoritative views and integrations.
- Requirements, design properties, calculations, verification cases, executions and results refer to the same applicable subject/baseline unless a controlled transformation states otherwise.
- Derived facts are reproducible from authored facts and one declared derivation implementation; cached results cannot silently outrank sources.
- Behavioral analysis states semantics, initial conditions, environment, scheduling/concurrency, bounds, solver and termination/unknown handling.
- Model verification covers conceptualization, equations/rules, implementation, data processing, numerics and independent limiting/regression cases as applicable.
- Model validation defines intended use, domain, referent, evidence independence, metrics, acceptance thresholds, uncertainty and consequences before results are interpreted.
- Calibration, verification, validation and operational monitoring datasets are separated or their reuse and statistical dependence are disclosed.
- Validation includes relevant boundary, adverse, rare, degraded and out-of-distribution detection cases—not only nominal fit.
- Passing evidence is configuration-controlled, reproducible and expires/reopens on material changes, discrepancies, domain shift or new consequences.
- A model result informs a decision; acceptance remains with an identified technical/decision authority and includes limitations and residual risk.

### Common failures

Common failures include calling every tool diagnostic “validation”; equating syntactic validity with correct semantics; checking only visible diagrams; ignoring hidden/filtered elements and access-limited query results; treating no violations as completeness; letting `unknown` become pass; suppressing warnings without expiry; creating thousands of noisy rules; testing rules only on passing fixtures; comparing names instead of identities; mixing variants, modes or units; validating a calculation with the spreadsheet from which it was copied; calibrating and validating on one dataset; tuning thresholds after seeing results; using average error when boundary error drives the decision; ignoring solver nonconvergence; claiming correlation proves causation; extrapolating beyond validation domain; validating a model once and reusing it after change; and asking a tool vendor's conformance claim to substitute for project evidence.

### Compact example

A synthetic thermal-controller fixture has typed usages, one configured connection, units, two requirements and two verification-case mappings. Eight local consistency rules pass. Three held-out synthetic temperatures differ from predictions by 1 °C each, below a predeclared 2 °C mean-absolute-error teaching threshold. This establishes only that the declared fixture and arithmetic meet those checks. It does not establish SysML conformance, physical model validity, statistical power, requirement compliance, safety or fitness for a real controller decision.

### Connections

SYSENG-051–056 establish authoritative, requirement, behavior, structure, parametric and SysML content. SYSENG-057 tests coherence and evidence boundaries across that content. SYSENG-058–060 will transform, thread, review and tool-enable models; each depends on trustworthy validation states and reproducible configuration.

## Governing Question

Can an independent reviewer reproduce every model check and validation conclusion for the exact baseline, distinguish what kind of claim each check supports, inspect unresolved/unknown results, and explain why the available evidence is adequate for the intended decision and no broader?

If the answer is only “the model is green,” neither consistency nor validity is established. Green may mean a parser succeeded, a query returned no rows, a simulation completed, a dashboard filtered warnings, or a threshold was met. Each is evidence at a different layer.

## Why This Matters

Models integrate claims from stakeholders, requirements, architecture, interfaces, behavior, quantities, analyses and verification. Contradictions can remain invisible because each diagram looks reasonable: the power port direction disagrees with the behavior flow, the mass calculation uses another variant, the requirement is verified against a superseded prototype, or a generated table reflects a stale cache. Consistency rules make such relations testable at scale.

Consistency is not validation. A perfectly consistent fictional model can be wrong about reality; an empirically useful approximation can contain deliberately simplified semantics. NASA-STD-7009B therefore treats modeling and simulation credibility across a lifecycle and requires project-defined acceptance criteria approved by delegated technical authority. The 2026 NASA-HDBK-7009B supplies current implementation guidance. Both emphasize intended use, verification, validation, uncertainty, sensitivity, data and result use rather than a single model-quality badge.

The final SysML 2.0 and KerML 1.0 specifications define many semantic constraints and validation rules. These support language-level correctness, including configured-variant rules, but they do not decide whether a project's system boundary, requirements or physics are right. NASA's product verification and validation guidance likewise distinguishes compliance with specified requirements from satisfaction of stakeholder expectations in the intended environment. The same words occur at multiple layers; disciplined qualifiers prevent category errors.

## Prerequisites and Retrieval

Before planning checks, retrieve:

1. intended uses, decisions, users, lifecycle stage, consequences, required confidence and designated acceptance authority;
2. exact project/branch/commit, configuration/variant, modes, environments, system boundary, time horizon and evidence cutoff;
3. language/metamodel, standard/domain libraries, project profile/ontology, extensions, API/schema, tool and derivation-rule versions;
4. stakeholder expectations, requirements, interfaces, architecture, behaviors, properties, calculations, analyses, hazards, risks and verification plans/results;
5. model governance: authorities, package ownership, identity/naming, review states, waivers/suppressions, merge rules, access controls and release gates;
6. conceptual-model assumptions, equations/algorithms, source code, solver/numerical settings, datasets, preprocessing and random seeds;
7. calibration and validation referents with provenance, uncertainty, configuration, sampling/coverage, independence and known limitations;
8. existing rule catalog, severity model, fixtures, expected results, false-positive/negative history, runtime, query completeness and prior baselines.

Use a retrieval test: “The model passed validation.” Ask which model and commit, what kind of validation, intended use/domain, referent and independence, metrics/thresholds, uncertainty, boundary cases, unresolved findings, authority and expiration trigger. Without these, “passed” is not a reusable claim.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish well-formedness, conformance, consistency, completeness, verification, validation, credibility and acceptance;
2. construct a layered consistency strategy covering language, project, cross-view, configuration, behavior, quantitative and evidence rules;
3. define rules with scope, severity, diagnostics, owners, exceptions and tested fixtures;
4. preserve unknown, tool-error and not-run states rather than converting absence of evidence into pass;
5. validate identity, trace, interface, unit, behavioral and configuration invariants across one model baseline;
6. verify conceptual, mathematical, software, data-processing and numerical implementations;
7. design intended-use validation with independent referents, predeclared metrics, thresholds, uncertainty and domain limits;
8. analyze sensitivity, boundary behavior, extrapolation and evidence leakage;
9. govern waivers, regressions, changes and revalidation triggers;
10. communicate bounded conclusions and residual risk to technical and decision authorities.

## Core Exposition

**Begin with the claim ladder.** A file can parse yet violate metamodel rules. A conforming model can violate project invariants. A consistent model can implement wrong equations. A correctly implemented model can be empirically inadequate. An adequate model can be misused outside its domain. A valid-for-use model can support a poor decision if consequences, uncertainty or stakeholder values are mishandled. Label each gate.

**Define scope before rules.** State packages, element states, configurations, modes, supplier partitions and access context included. Decide whether incomplete exploratory content is allowed and how it is marked. A repository-wide check with hidden access restrictions may return a misleadingly clean result. Preserve partial-query and permission evidence.

**Layer rule families.** Language rules cover grammar, metamodel constraints and reference resolution. Project-semantic rules cover approved types, ownership, metadata and method. Cross-view rules cover shared identity and authority. Configuration rules prevent variant/mode/baseline mixing. Domain rules cover units and interface compatibility. Behavioral rules cover reachability, deadlock or timing assumptions. Evidence rules cover verification coverage, execution and applicability. Keep the families and conclusions distinct.

**Make every rule a governed object.** Record identifier, question, rationale, formal predicate or manual procedure, scope, exclusions, severity, diagnostic, remediation owner, rule version, author/reviewer and evidence. Include positive, negative, boundary and malformed fixtures. A rule that has never caught its seeded defect is not trusted merely because its code runs.

**Design actionable diagnostics.** A useful finding names violating element identities, commit, expected invariant, observed values, configuration and likely owners. “Model invalid: 372 errors” creates suppression behavior. Group causal violations so one missing type does not produce hundreds of secondary errors without explanation.

**Represent four-valued outcomes.** Use at least pass, fail, unknown and not-applicable, plus execution error/not-run where operationally important. Unknown arises when required data, permissions, solver result or applicability is missing. It is not pass. Define release policy for each severity and state; high-consequence unknowns usually require resolution or explicit authority.

**Control exceptions.** A waiver/suppression identifies rule and finding, affected elements/configurations, justification, compensating control, approver, issue/risk, creation and expiry/review trigger. Re-evaluate after model/rule changes. Do not suppress by message substring or globally disable a noisy rule without preserving the gap.

**Check identity and authority.** Detect duplicate IDs, unresolved references, name collisions, superseded elements still exposed, conflicting sources and manual copies. Verify that views, calculations and generated documents resolve to authoritative elements at the selected commit. Same display name is never sufficient.

**Check type, multiplicity and containment.** Resolve every consequential usage, feature and relationship to approved definitions/libraries. Check specialization compatibility, feature subsetting/redefinition, ownership, composite/reference semantics and multiplicities. Language-valid open-world semantics may still require stricter project closed-world completeness gates; state this as project policy.

**Check configuration compatibility.** Assign variant, serial/build, maturity, environment, mode, effective time and evidence applicability as needed. Walk every reasoning path from requirement through design and analysis to verification. Reject or explicitly transform cross-baseline links. Configuration mismatch often produces plausible numbers, making it more dangerous than syntax failure.

**Check interfaces bidirectionally.** For each connection, validate end existence/ownership, port type, direction/conjugation, conveyed item, units, multiplicity, mode and configured participants. Cross-check sender/receiver behavior and external interface contract. Then invoke discipline-specific electrical, mechanical, data/protocol, human and safety checks. A generic systems model cannot fully validate every domain contract.

**Check requirements and evidence state.** Requirement identity, subject, assumptions, required constraints, source and applicability must agree with design. Distinguish trace/derive/satisfy claims from verification coverage; case definition from execution; execution from reviewed result; pass from waiver. Coverage without evidence is planned work, not compliance.

**Check behavior under explicit semantics.** Static checks find missing initial states, unreachable references and ill-typed flows. Dynamic checks may explore reachability, deadlock, livelock, invariant violations, temporal properties, resource bounds and scenarios. State abstraction, scheduler/fairness, time model, environment inputs and search bounds. “No counterexample within bound” is not an unbounded proof.

**Check quantities and calculations.** Enforce quantity kinds, units/reference conditions, dimensions, sign conventions, input/output direction, domains and authoritative bindings. Recompute independent golden cases, limiting cases and adversarial boundaries. Inspect solver convergence, residuals, tolerance, initialization, multiple solutions and numerical stability. Successful termination is not correctness.

**Check views and generated artifacts.** A viewpoint determines selection and rendering. Regenerate from controlled model commit and generator version; compare source identities and values, not just pixels. Flag manual edits to generated facts, stale source digests, omitted critical concerns and filtered unresolved elements. Human narrative remains governed alongside generated content.

**Verify the conceptual model.** Domain experts inspect system boundary, entities, causal mechanisms, conservation laws, assumptions, omitted phenomena, environmental/operational scenarios and intended outputs. A software unit test cannot catch an elegant implementation of the wrong conceptual model.

**Verify mathematics and implementation.** Trace equations and logic to the conceptual model and sources. Review derivations, dimensions, algorithms, discretization and approximations. Test code with analytic solutions, manufactured solutions where appropriate, independent implementations, regression fixtures and boundary inputs. Validate preprocessing and mappings; data-pipeline defects can dominate model error.

**Qualify numerical error.** Separate model-form/input uncertainty from discretization, iteration, sampling and floating-point error. Perform mesh/time-step/sample/tolerance convergence studies appropriate to the method. Check nondeterminism and seeds. Report solver failures and unstable regions instead of imputing attractive values.

**Define intended use and risk.** Validation rigor depends on what result will decide and the consequence of error. Specify output measures, domain ranges, accuracy/resolution/timing required, decisions/thresholds, users and fallback. A model adequate for ranking concepts may be inadequate for safety certification or real-time control.

**Choose validation referents deliberately.** Prefer independent, configuration-relevant observations or tests over copied calculations. Where physical data are unavailable, use accepted benchmarks, higher-fidelity models, expert elicitation and cross-model comparisons, but label the weaker evidence. Assess measurement uncertainty, representativeness, data quality and discrepancies in the referent itself.

**Separate calibration and validation.** Freeze calibration data, objective/loss, parameters, priors/bounds and fitting process. Reserve independent validation cases or use honest resampling/hierarchical designs where data are scarce. Preserve selection and preprocessing decisions. Repeatedly tuning after validation failures turns validation into calibration.

**Predeclare metrics and acceptance.** Select metrics that align with decisions: bias, absolute/relative error, distributional distance, coverage, event detection, rank stability, constraint violations or decision loss. Averages can hide worst-region failures; relative error fails near zero. Define thresholds and aggregation before results. Include measurement and sampling uncertainty around metrics.

**Cover the domain.** Map evidence across input space, configurations, modes, environments and time. Include nominal, boundary, adverse, degraded, failure/recovery and decision-threshold cases. Identify extrapolation/out-of-distribution conditions. Validation is a domain map, not one global adjective.

**Analyze sensitivity and uncertainty.** Identify influential inputs, interactions, common causes, model-form alternatives and decision breakpoints. Propagate credible uncertainty and compare it with margin. If results are insensitive to observed inputs for the wrong reason, investigate. Target new evidence where uncertainty and decision sensitivity overlap.

**Investigate discrepancies.** Preserve raw data and stop automatic promotion on unexpected difference. Check configuration alignment, measurements, preprocessing, implementation, numerics, parameters, model form and environmental assumptions. Do not tune a correction factor until discrepancy cause and downstream effects are understood.

**Build a credibility argument.** Assemble intended use, model description/version, verification evidence, validation evidence/domain, uncertainty, sensitivity, prior-use history, discrepancies, limitations, rule results and responsible reviewers. Authority weighs evidence against consequence and residual risk. A scalar score may summarize but must not hide failed or unknown critical factors.

**Automate continuously, review periodically.** Run fast local rules during authoring, affected-scope checks on changes, complete gates at merge/release and deeper dynamic/empirical assessments on planned triggers. Trend newly introduced versus inherited findings. Automation keeps the model inspectable; multidisciplinary review decides whether rules and conclusions remain meaningful.

**Reopen on change.** Revalidation triggers include equations/code/data/library/tool changes, altered configuration/domain/intended use, new discrepancy, shifted environment/population, supplier change, higher consequence, expired evidence and rule correction. Use change-impact analysis to rerun the necessary evidence, but periodically sample outside the predicted impact set to detect missing dependencies.

The following checker applies eight local rules to a synthetic model fixture and evaluates three independent synthetic validation points against a predeclared teaching threshold. It is neither a SysML validator nor real engineering validation.

<!-- bijux-verify: {"id":"model-consistency-validation-fixture","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"rules=8\nrule_violations=0\nvalidation_cases=3\nvalidation_mae_c=1.0\nvalidation_threshold_c=2.0\nvalidation_acceptance=1\nstatus=declared_consistency_and_validation_checks_passed\nevidence=synthetic_fixture_only\n","stderr":""}} -->
```python
definitions = {"Battery", "Controller", "PowerPort"}
usages = {
    "pack": {"type": "Battery", "owner": "system", "configuration": "A"},
    "controller": {"type": "Controller", "owner": "system", "configuration": "A"},
    "pack.supply": {"type": "PowerPort", "owner": "pack", "configuration": "A"},
    "controller.input": {"type": "PowerPort", "owner": "controller", "configuration": "A"},
}
ports = {
    "pack.supply": {"item": "ElectricPower", "unit": "W"},
    "controller.input": {"item": "ElectricPower", "unit": "W"},
}
connections = [{"source": "pack.supply", "target": "controller.input", "configuration": "A"}]
requirements = {"REQ-TEMP", "REQ-POWER"}
verification_cases = {"VC-TEMP": "REQ-TEMP", "VC-POWER": "REQ-POWER"}

rules = [
    len(usages) == len(set(usages)),
    all(usage["type"] in definitions for usage in usages.values()),
    all(usage["owner"] for usage in usages.values()),
    all(connection["source"] in usages and connection["target"] in usages for connection in connections),
    all(ports[c["source"]]["item"] == ports[c["target"]]["item"] for c in connections),
    all(ports[c["source"]]["unit"] == ports[c["target"]]["unit"] for c in connections),
    all(usages[c["source"]]["configuration"] == c["configuration"] == usages[c["target"]]["configuration"] for c in connections),
    requirements <= set(verification_cases.values()),
]

predicted_c = [119.0, 151.0, 181.0]
observed_c = [120.0, 150.0, 180.0]
threshold_c = 2.0
mae_c = sum(abs(p - o) for p, o in zip(predicted_c, observed_c)) / len(observed_c)
violations = sum(not rule for rule in rules)
accepted = mae_c <= threshold_c

print(f"rules={len(rules)}")
print(f"rule_violations={violations}")
print(f"validation_cases={len(observed_c)}")
print(f"validation_mae_c={mae_c:.1f}")
print(f"validation_threshold_c={threshold_c:.1f}")
print(f"validation_acceptance={int(accepted)}")
print("status=" + ("declared_consistency_and_validation_checks_passed" if violations == 0 and accepted else "declared_check_failure"))
print("evidence=synthetic_fixture_only")
```

Three hand-selected points and one average-error threshold offer almost no evidence about tails, bias, uncertainty, independence, domain coverage or decision consequences. The example teaches separation of checks, not approval of a thermal model.

## Definitions and Notation

Let each check result be

$$
z=(rule,modelCommit,configuration,scope,status,severity,evidence,owner,expiry).
$$

The status space is $S=\{pass,fail,unknown,notApplicable,error,notRun\}$. Waiver and suppression are governance dispositions attached to a finding; they should not overwrite the original `fail` or `unknown` observation.

For a consistency graph $G=(E,R)$, project invariants may include identity uniqueness, referential closure, type compatibility, unit compatibility and configuration compatibility. Pairwise consistency does not imply global consistency when constraints interact. Likewise, a model can be logically satisfiable yet omit a required element; consistency and purpose-relative completeness are separate.

For validation cases $i=1,\ldots,n$, residual $e_i=y_{M,i}-y_{R,i}$. Common metrics include

$$
MAE=\frac{1}{n}\sum_i|e_i|,\qquad RMSE=\sqrt{\frac{1}{n}\sum_i e_i^2}.
$$

Metrics require units, grouping/weights, uncertainty and sampling context. Neither metric alone exposes sign bias, extreme-region error, correlation, distribution mismatch or decision loss.

Define the validated domain record

$$
D_v=(inputs,configurations,modes,environments,time,evidence,metrics,thresholds,uncertainty).
$$

Use outside $D_v$ is extrapolation unless justified by additional evidence. Any change to the model, referent or intended use may alter $D_v$.

## Mechanisms, Invariants, or Proof Structure

**Gate composition.** Let $L$ be language checks, $P$ project/cross-model checks, $I$ implementation verification, $E$ empirical validation and $A$ authority acceptance. A release argument is a conjunction under declared policy, not an average score:

$$
release = L\land P\land I\land E\land A.
$$

A not-applicable gate needs rationale. An unknown high-consequence gate remains unresolved. Passing later gates does not erase an earlier contradiction.

**Rule soundness and sensitivity.** For a bounded fixture population, rule soundness concerns avoiding false positives and defect sensitivity concerns finding seeded/applicable defects. Test both. Real model spaces are open-ended, so a finite fixture suite cannot prove universal soundness or completeness.

**Trace invariant.** For any requirement conclusion, traverse authoritative requirement $\rightarrow$ configured subject/design $\rightarrow$ method/case $\rightarrow$ execution $\rightarrow$ result $\rightarrow$ approval. Every node shares compatible configuration and time/evidence applicability. Missing or mismatched links yield unknown/fail according to policy, never inferred pass.

**Validation invariant.** Intended use, model version, referent, data split, metrics, thresholds and uncertainty are fixed before final evaluation. Deviations are recorded and evaluation repeated with preserved history. This reduces hindsight tuning but does not eliminate bias or evidence limitations.

**Bounded conclusion.** A validation claim has the form: “Model $M_c$ met criteria $C$ for use $u$ over tested domain $D_v$ using evidence $E$ subject to limitations $L$.” Deleting any qualifier makes the claim easier to misuse.

No theorem here proves that passing these gates guarantees a successful system. The structure prevents category errors and makes evidence auditable; engineering judgment and empirical reality remain decisive.

## Alternatives and Trade-Offs

**Strict versus progressive consistency.** Strict rules protect baselines and safety-critical content. Progressive profiles allow exploration with explicit unknowns. Use lifecycle/status-aware gates, then tighten before consequential decisions; do not let exploratory exceptions silently reach release.

**Central versus federated validation.** A central engine offers uniform rules and reporting but may lack domain/tool semantics. Federated checks preserve specialist capability but complicate identity, configuration and evidence aggregation. Define shared result contracts and authority while retaining domain ownership.

**Closed-world versus open-world policy.** Closed-world project checks can flag missing declarations; open-world semantics allow unspecified facts to remain possible. Closed-world gates improve release completeness but can reject legitimate partial models. State the assumption per question rather than relying on tool defaults.

**Static analysis versus execution/search.** Static checks are fast, deterministic and broad; dynamic analysis reveals paths, timing and solver behavior but depends on scenarios/bounds. Combine them and preserve inconclusive results.

**Physical tests versus higher-fidelity/cross-model referents.** Physical observations are often strongest but expensive, sparse or unsafe. Cross-model comparisons are useful early but can share errors. Build an evidence ladder and disclose common provenance.

**Single metric versus decision-focused suite.** One metric simplifies gates but hides failure structure. A metric suite captures bias, variance, boundaries and decisions but risks multiple-comparison and interpretation problems. Predeclare a small consequence-aligned set with diagnostic plots/cases.

**Automatic suppression versus governed waiver.** Suppression controls noise; it can normalize defects. Require identity, rationale, owner, compensating control and expiry, and trend suppressed risk separately.

## Failure Modes and Misconceptions

**“No errors means consistent.”** The rules may be incomplete, inapplicable, not run or access-limited. Report coverage and unknowns.

**“Consistent means correct.”** Consistency only means no contradiction under selected semantics. Validate conceptual and empirical adequacy.

**“Tool validation proves SysML conformance.”** Name exact language version, conformance points and tests. Vendor/project rules are additional layers.

**“Verification case coverage means requirements pass.”** Coverage is planning. Require execution, applicable evidence, verdict and review.

**“The model matches test data, so it is valid.”** Check independence, calibration leakage, uncertainty, domain, metrics and alternative explanations.

**“Low average error is enough.”** Inspect bias, boundaries, subgroups, tails, decision thresholds and uncertainty.

**“Unknown can be ignored.”** Missing permission/data, solver indeterminacy or incomplete search can hide consequential defects. Route unknown explicitly.

**“A waiver fixes the model.”** It accepts bounded residual risk under authority; the finding remains historically true.

**“Validation lasts forever.”** Model, data, environment, configuration and intended use evolve. Define triggers and monitor discrepancies.

**“Independent review means a different dashboard user.”** Independence concerns responsibility, evidence provenance and freedom to challenge assumptions, implementation and acceptance—not merely another login.

## Worked Examples

### Example 1

**Identity mismatch.** A generated interface table and diagram show `BusA`, but their element IDs refer to different configurations. A name-based rule passes. An identity/configuration rule fails and prevents release. Review confirms one table was generated from a supplier branch; the fix restores authoritative mapping rather than renaming the duplicate.

### Example 2

**Requirement coverage illusion.** Every requirement has a verification case, so coverage is 100 percent. Evidence rules find that 14 cases never executed, three executions target an earlier prototype and one result is inconclusive. The report separates planned coverage, applicable execution coverage and pass evidence instead of publishing one optimistic percentage.

### Example 3

**Port semantic mismatch.** Two ports share item name `Power` and connect cleanly. Quantity rules reveal watts on one end and watt-hours on the other; behavior reveals one is instantaneous supply and the other stored energy. The connection is remodeled and domain review adds voltage/current/transient requirements.

### Example 4

**Bounded behavior search.** State exploration finds no deadlock within 40 events. A longer adversarial scenario reaches a retry-exhaustion state with no transition. The original result is retained as “no counterexample within bound 40,” not “deadlock free.” A recovery transition and unbounded proof obligation or larger justified analysis follow.

### Example 5

**Variant contamination.** A mass model passes units and arithmetic but combines flight-variant structure with prototype measurements. Configuration-path checking rejects the result. Engineers either bind flight estimates or create a controlled transformation explaining why prototype evidence applies, including uncertainty.

### Example 6

**Rule defect.** A rule flags all untyped exploratory usages as release errors and produces 8,000 findings. Positive/negative fixtures expose missing lifecycle-state scope. The corrected rule gates only governed baseline content while an advisory rule reports exploration debt. Existing suppressions are reviewed rather than bulk-carried.

### Example 7

**Calibration leakage.** A thermal model is tuned and evaluated on the same hot-day test series, reporting 0.5 °C error. Held-out hardware lots show 4 °C bias near the requirement threshold. The team reclassifies the first result as calibration fit, updates uncertainty/model form and designs independent validation.

### Example 8

**Misleading average.** Queue-delay prediction has acceptable global MAE, but errors are severe during emergency peaks that drive staffing decisions. Decision-weighted and boundary metrics fail. The validated domain excludes disruption use until peak mechanisms and evidence improve.

### Example 9

**Partial API query.** A consistency service retrieves one page of elements after an authorization filter and reports zero dangling relationships. The evidence contract detects incomplete pagination and reduced access scope, returning `unknown`. After complete privileged retrieval, two unresolved supplier references appear.

### Example 10

**Change-triggered revalidation.** A solver library update changes convergence near a design boundary while regression means remain similar. Version impact rules trigger limiting cases, tolerance study and validation replay. One rank ordering flips, reopening the trade decision. The old evidence remains valid only for the old toolchain/configuration.

## Cross-Program Connections

**Platform engineering.** Policy-as-code, configuration validation, golden-path tests and SLO evidence need scoped rules, exception governance and runtime revalidation.

**API and service engineering.** Contract/schema checks, consumer tests, integration tests and production validation are distinct. Pagination, auth filtering and partial failure can turn a clean query into unknown.

**Data engineering.** Schema, lineage and quality rules protect pipelines; statistical validation requires representative datasets, leakage control, drift monitoring and uncertainty.

**Object-oriented programming.** Type systems and class invariants prevent some invalid states, while integration, temporal behavior and intended-use adequacy require broader tests and evidence.

**Functional programming.** Pure functions and property tests strengthen reproducibility; effects, state exploration, dataset provenance and empirical validation still define system boundaries.

## References

1. Object Management Group, *OMG Systems Modeling Language, Version 2.0, Part 1: Language Specification*, formal/2026-03-02. <https://www.omg.org/spec/SysML/2.0/Language/PDF>
2. Object Management Group, *Kernel Modeling Language, Version 1.0*, formal/2026-03-01. <https://www.omg.org/spec/KerML/1.0/PDF>
3. Object Management Group, *About the OMG Systems Modeling Language Specification Version 2.0*. <https://www.omg.org/spec/SysML/2.0>
4. Object Management Group, *Systems Modeling API and Services, Version 1.0*, formal/2026-03-04. <https://www.omg.org/spec/SystemsModelingAPI/1.0/PDF>
5. NASA, *Standard for Models and Simulations*, NASA-STD-7009B, active 2024. <https://standards.nasa.gov/standard/nasa/nasa-std-7009>
6. NASA, *NASA-STD-7009B: Standard for Models and Simulations*, public PDF. <https://standards.nasa.gov/sites/default/files/standards/NASA/B/1/NASA-STD-7009B-Final-3-5-2024.pdf>
7. NASA, *NASA Handbook for Models and Simulations: An Implementation Guide for NASA-STD-7009B*, NASA-HDBK-7009B, 2026. <https://standards.nasa.gov/system/files/tmp/NASA-HDBK-7009B_Final%2002-03-2026.pdf>
8. NASA, *NASA Systems Modeling Handbook for Systems Engineering*, NASA-HDBK-1009A, active 2025. <https://standards.nasa.gov/standard/NASA/NASA-HDBK-1009>
9. NASA, *Systems Engineering Handbook, 5.3 Product Verification*. <https://www.nasa.gov/reference/5-3-product-verification/>
10. NASA, *Systems Engineering Handbook, 5.4 Product Validation*. <https://www.nasa.gov/reference/5-4-product-validation/>

## Exercises

### Exercise 1

Design a consistency-rule catalog and release policy for a safety-relevant battery-control model, including unknowns, fixtures, diagnostics and waivers.

### Exercise 2

Audit a “fully validated” model that parsed successfully, passed 2,000 rules, was calibrated and tested on one dataset, and reports low mean error.

### Exercise 3

Plan verification and validation for a flood-prediction model used first for planning and later for automated evacuation alerts.

### Exercise 4

Define a cross-tool consistency check for requirements, architecture, calculations and verification evidence accessed through APIs with different permissions.

### Exercise 5

A rule-engine and solver upgrade changes findings and results one week before a release. Define impact analysis, regression, authority and reporting.

## Answers to the Exercises

### Answer 1

Fix intended uses, safety consequences, project/commit/configuration, language/libraries/toolchain and release authority. Organize rules by language/reference resolution; project identity/ownership/status; definition/usage/type/multiplicity; configuration/mode; port/item/direction/unit; behavior performer/state/recovery; quantitative dimensions/bindings/solver; requirement-subject and case coverage; execution/result applicability; and hazard/barrier/evidence trace. Each rule records ID, rationale, predicate, scope/exclusions, severity, diagnostic fields, owner, version and remediation guidance.

Create passing, failing, malformed and boundary fixtures. Seed defects such as duplicate ID, unresolved type, cross-variant connection, W/Wh mismatch, unreachable safe state, stale calculation input, verification result from another prototype and hidden high-severity unknown. Require the rule to find applicable seeds without flagging valid exploratory/status-excluded cases. Measure runtime and causal diagnostic grouping; review false-positive/negative history.

Use pass/fail/unknown/not-applicable/error/not-run. Release blocks on any unresolved critical fail, critical unknown, tool error or incomplete query. Lower findings require risk-ranked disposition. A waiver preserves original finding, affected baseline/configuration, rationale, compensating evidence, owner/approver, linked risk and expiry/reopen trigger. Never let a global suppression mask new instances.

Run fast checks on authoring, affected-scope checks on change and full checks at merge/release. Independent domain reviews assess battery physics, controls, electrical/thermal interfaces, hazards and evidence beyond generic rules. Publish rule-set/model versions, counts by state/severity, newly introduced findings, waived risk, coverage limitations and exact release authority. Passing the catalog supports consistency; safety acceptance still requires model verification, intended-use validation and system evidence.

### Answer 2

Decompose “fully validated.” Parsing establishes syntax only. Identify the exact 2,000 rules, versions, scope, access, fixtures, outcomes, unknown/not-run states and suppressions. Determine whether they cover metamodel, project semantics, identity, configuration, behavior, units, evidence and domain invariants, and whether noisy correlated rules inflate the count. Re-run against the controlled commit and inspect representative passing and failing diagnostics.

Reconstruct intended use, domain, consequence, conceptual model, equations, implementation, solver and data pipeline. Verify equations/units, code, preprocessing, numerical convergence, limiting cases and independent regression. Check that the rule engine cannot validate omitted physics or wrong requirements simply because encoded relations are coherent.

Audit data provenance and split. If calibration and evaluation use the same observations, relabel the low error as fit, not independent validation. Preserve parameters and tuning decisions; create held-out configurations/time/sites/hardware or a justified resampling design. Check leakage through preprocessing, feature engineering and repeated threshold tuning. Assess referent measurement uncertainty and shared source errors.

Predeclare decision-aligned metrics/thresholds and examine signed residuals, subgroups, boundary/tail/degraded cases, distributions and decision flips—not mean error alone. Map evidence domain and test extrapolation detection. Propagate parameter/input/model-form/numerical uncertainty and perform sensitivity. Report what passed, what remains unknown, corrected claim/domain and residual risk. Only the named authority may accept the model for the bounded use.

### Answer 3

Treat planning and automated alerting as separate intended uses with sharply different consequences, latency and evidence criteria. Define geographic/temporal domain, rainfall/river/coastal inputs, terrain/infrastructure, sensor networks, forecast horizon, outputs, populations, operator actions and environmental/climate regimes. Build a conceptual model with hydrology/hydraulics, boundary conditions, control structures, data assimilation and failure assumptions; review it with domain and emergency stakeholders.

Verify governing equations/approximations, discretization, conservation, code, geospatial transformations, datum/units/time alignment, sensor preprocessing, numerical convergence/stability, deterministic seeds/versioning and analytic/manufactured/benchmark cases. Test missing/late/corrupt sensors, infrastructure changes and solver failure. Keep tool errors observable.

For planning, validate against independent historical events and surveys across representative catchments/regimes. Metrics may include level/extent/arrival-time bias, spatial overlap, uncertainty coverage and ranking robustness. Planning may tolerate slower computation and coarser conservative uncertainty if limitations are clear. Validate scenario conclusions and sensitivity to climate/land-use assumptions.

For alerts, require prospective or strictly held-out event evidence near action thresholds, rare/rapid events, subgroup/location impacts, end-to-end latency/availability, false-alarm/missed-event consequences, human interpretation and fallback. Predeclare alert decision loss and escalation. Use redundant observations and operational exercises; model validation cannot replace alert-system product verification/validation.

Maintain separate accreditation decisions and domains. Monitor residuals, sensor/data drift, terrain/infrastructure and climate shifts; define automatic out-of-domain/fail-safe behavior. Revalidate on model/code/data/threshold/network/process changes and after discrepancies. Publish uncertainty and bounded claims to operators without overstating sparse extreme-event evidence.

### Answer 4

Define a common identity/configuration contract: canonical element IDs or governed mappings, project/branch/commit, effective configuration/mode, schema/API/tool version, authoritative owner and source digest. Enumerate cross-tool invariants: requirements resolve to configured subjects; architecture ports/interfaces align with behavioral flows; calculations bind authoritative properties with units; verification cases and executions reference applicable requirement/design baselines; generated views cite source commits.

For each API principal, record accessible scope, authorization filters, pagination, query, errors and completeness token/count. Never compare “all elements” results unless both sides demonstrate complete authorized retrieval. Missing because inaccessible is unknown, not absent. Preserve source records and transformation/mapping versions in an evidence graph or controlled snapshot; do not silently write corrections into downstream copies.

Run local conformance checks first, then normalize only declared semantics. Join by identity mappings, not names. Emit violations with source IDs/commits and observed mismatch; emit unknown for unresolved IDs, partial pages, stale snapshots, unsupported constructs or incompatible configuration. Test with fixtures containing renames, duplicate names, deleted/superseded elements, cross-variant links, unit conversions, inconclusive verification and restricted supplier data.

Assign source/domain owners to adjudicate findings. A legitimate federated difference may need a transformation or local exception; preserve rationale, authority and expiry. At release, report pass/fail/unknown by invariant and source, query/access limitations, snapshot age, transformations and waivers. Sample source systems manually and perform round-trip/negative tests. Cross-tool consistency supports traceability; it does not validate the underlying requirement, architecture, physics or product.

### Answer 5

Freeze release candidate, old/new rule engine, rules, solver/libraries, configuration, inputs, seeds and outputs. Do not overwrite prior evidence. Classify changes: specification/rule semantics, parsing/query scope, derived relationships, numerical algorithm/defaults, tolerances, platform dependency or diagnostics only. Obtain vendor/change records but verify behavior independently.

Run controlled A/B regression on positive/negative/boundary rule fixtures and representative model baselines. Explain every added, removed or changed finding; detect false positives/negatives and unknown/error handling changes. For solver results, run analytic/golden/limiting cases, convergence/tolerance/initialization studies, residuals, failed/multiple solutions and decision-sensitive production cases. Compare full outputs and decision classifications, not rounded dashboards.

Trace differences to requirements, interfaces, budgets, hazards, verification and pending decisions. If the old engine missed a real critical defect, block and correct the model/evidence. If the new engine is wrong, retain the qualified old toolchain or narrowly waive with compensating independent checks and a tracked correction. If numerical changes flip a decision, reopen analysis/validation rather than choosing the preferred output.

Re-run affected empirical validation and uncertainty/sensitivity when model results change materially. Independent rule, numerical, domain, configuration, safety and release authorities review evidence proportionate to consequence. The release authority decides whether to adopt, defer or block; schedule pressure is recorded as risk, not validation evidence.

Report exact versions, comparison matrix, changed findings/results, causal analysis, regression/validation status, waivers, residual risk and future triggers. Preserve both evidence packages. Update baselines only after approval, then monitor. A week-before-release change is not inherently unacceptable, but unexplained evidence differences are.
