---
module_id: SARCH-064
program: Software Engineering: Software Architecture
level: 2
module_number: 64
title: Architecture Fitness Functions
status: complete
last_verified: 2026-09-06
---

# Architecture Fitness Functions

## One-Page Review

### Governing question

Which architectural properties can be checked repeatedly as a system evolves, at what boundary and cadence, and how can those checks constrain drift without mistaking convenient proxies for architectural quality?

### Essential definitions

- An **architecture fitness function** is an objective integrity assessment of one or more architectural characteristics, evaluated repeatedly as change occurs [1].
- An **atomic fitness function** checks one characteristic; a **holistic fitness function** evaluates an emergent end-to-end property across several parts.
- A **static** function inspects artifacts without executing the system; a **dynamic** function observes execution, simulation, experiment, or operation.
- A **triggered** function runs on a change or event; a **continuous** function evaluates frequently enough to constrain drift; a **periodic** function runs on a schedule or decision cadence.
- A **leading indicator** detects a condition before stakeholder harm; a **lagging indicator** records an outcome after exposure.
- A **guardrail** is a mandatory bound; a **target** is a desired value; a **budget** allocates tolerated consumption over a window.
- A **ratchet** prevents regression from an accepted baseline while a legacy system improves incrementally.
- An **exception** is a scoped, owned, expiring authorization to violate a rule; it is not deletion of the rule.
- **Fitness-function coverage** is the traced set of important scenarios and decisions checked by the portfolio, not a percentage of architecture correctness.
- **drift** is divergence between intended architecture and implemented or operated reality.

### Central model, mechanism, or theorem

A fitness function can be specified as

$$
F=(property,scope,measure,threshold,trigger,owner,evidence,action,expiry).
$$

Its verdict is meaningful only for that tuple. The function must distinguish the architectural property from the mechanism and measurement proxy used to observe it.

For a bounded budget $B$ over window $W$, consumptions $c_i$ must satisfy

$$
\sum_{i\in W}c_i\le B.
$$

Examples include error budget, dependency exceptions, public API breaks, policy violations, or unreviewed high-blast-radius changes. A budget manages an explicitly tolerated class; it must not legalize safety, security, privacy, integrity, or accessibility violations that are mandatory gates.

### Critical invariants

- every function traces to a driver, quality scenario, architectural decision, or explicit hazard;
- scope includes artifact, population, environment, version, and measurement boundary;
- the measure has an independent oracle and cannot silently omit failures or missing evidence;
- thresholds have units, rationale, uncertainty, and a named response;
- functions run at the earliest useful boundary and again where end-to-end evidence is required;
- local checks do not claim holistic properties they cannot observe;
- failures cannot be bypassed by relabeling, suppressing data, or moving work outside the measured path;
- exceptions identify owner, rationale, affected scope, compensating control, expiry, and removal condition;
- noisy or obsolete checks are repaired through governed change, not routinely ignored;
- the portfolio evolves with architecture, incidents, threats, standards, and stakeholder needs.

### Common failures

Common failures include renaming ordinary unit tests as architecture checks; measuring only what tooling exposes; enforcing product names instead of durable boundaries; counting dependencies without direction or consequence; checking diagrams but not deployed topology; using averages that hide cohorts; dropping timeouts from latency; turning warnings into permanent noise; allowing nonexpiring exceptions; blocking delivery on flaky remote dependencies; making every check a CI gate; measuring only components; treating SLOs as the whole architecture; and assuming a green dashboard proves safety, security, accessibility, or correctness.

### Compact example

A modular monolith declares that `billing` may depend on `ledger`, while `ledger` must not depend on `billing` or `web`. A build-time function extracts actual imports, rejects forbidden edges, identifies the rule and violating path, and expires any approved exception. A runtime function separately verifies that every accepted invoice produces one attributable ledger intent. The static rule constrains code coupling; it cannot prove the business invariant, so the two functions have distinct oracles and cadences.

### Connections

[SARCH-062](062-quality-attribute-scenarios.md) supplies measurable properties and [SARCH-063](063-risk-sensitivity-and-trade-off-points.md) identifies sensitive decisions worth guarding. [SARCH-065](../ROADMAP.md) next develops dependency and coupling metrics. Delivery and Reliability Engineering owns pipeline and SLO practice; this module owns the architecture-level fitness portfolio.

## Governing Question

Architecture descriptions decay because implementation, infrastructure, data, operations, and organizations change continuously. A review performed every year discovers drift after it has accumulated. Conversely, thousands of ungoverned checks can freeze a system around obsolete decisions.

Fitness functions turn selected architectural intent into repeatable evidence. The discipline is to choose consequential properties, suitable oracles, useful enforcement points, and an evolution process—while preserving what cannot be automated.

## Why This Matters

A dependency boundary can erode one import at a time. A regional design can acquire a global identity dependency. A schema can become impossible to roll back. An SLO can look healthy by excluding errors. Architecture changes through ordinary delivery decisions, so feedback must live near those decisions.

Good fitness functions shorten the distance between drift and correction. They also make architectural governance reviewable: teams know which property is protected, why, how evidence is gathered, who owns failure, and when an exception ends.

## Prerequisites and Retrieval

Retrieve architecture decision, quality attribute, scenario, invariant, risk, sensitivity, trade-off, dependency graph, coupling, policy, test oracle, static analysis, dynamic analysis, contract test, property test, benchmark, SLI, SLO, error budget, conformance, drift, threshold, baseline, ratchet, exception, false positive, false negative, flaky test, enforcement, evidence, and expiry.

From SARCH-021 through SARCH-030 retrieve architecture views and description. SARCH-031 through SARCH-050 supply structural and integration decisions. SARCH-051 through SARCH-060 supply distributed failure properties. SARCH-061 through SARCH-063 supply evaluation, scenario, risk, and sensitivity reasoning.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish architecture fitness functions from ordinary tests and generic metrics;
2. specify property, scope, measure, threshold, trigger, owner, evidence, action, and expiry;
3. choose static, dynamic, atomic, holistic, triggered, continuous, and periodic checks;
4. implement dependency, API, schema, deployment, data, security, and runtime functions;
5. pair leading indicators with lagging end-to-end outcomes;
6. design thresholds, budgets, baselines, ratchets, and exceptions without normalizing harm;
7. prevent proxy gaming, survivor bias, measurement drift, and alert noise;
8. govern function rollout, failure, ownership, evidence retention, and retirement;
9. evaluate coverage and gaps across architecture views and quality scenarios;
10. design a balanced portfolio for unfamiliar high-consequence systems.

## Core Exposition

**Start from architectural intent.** Select properties whose erosion would materially affect quality, risk, or change cost. Examples include dependency direction, single-writer authority, tenant isolation, API compatibility, data residency, deploy independence, recovery capability, and accessible emergency control.

Do not begin with the tool catalog. A linter can enforce available syntax rules, but availability does not make a rule architecturally significant. Trace each function to a scenario, decision record, risk, standard, or incident.

**Specify the whole function.** Name property, scope, measure, threshold, trigger, owner, evidence, action, and expiry conditions. “No cycles” is incomplete: in which graph, after which transformations, with which generated code, and what happens when a violation exists?

Version the rule and its rationale. A result should identify the architecture and input revision. Preserve enough evidence to reproduce failures without retaining prohibited secrets or personal data.

**Distinguish atomic and holistic checks.** An atomic rule may ban a dependency edge, require encrypted transport configuration, or cap queue capacity. It is fast and attributable. A holistic check may exercise region loss, restore a product, measure a user task, or reconcile business outcomes.

Many qualities are emergent. Passing every service health check cannot establish end-to-end order completion. Use atomic checks for mechanisms and holistic checks for outcomes; trace how they support but do not substitute for each other.

**Place checks across the lifecycle.** Editor and pre-commit checks give rapid local feedback. Build and CI checks inspect dependencies, schemas, APIs, images, and policies. Deployment checks inspect topology, permissions, compatibility, and rollout. Runtime functions observe workload and failures. Periodic exercises cover recovery, humans, suppliers, and physical conditions.

The earliest check is not always authoritative. Source analysis cannot see cloud policy drift; runtime measurement cannot prevent an incompatible schema from shipping. Defense in depth means different evidence at appropriate boundaries, not duplication without purpose.

**Use static structure functions.** Extract module, package, service, schema, infrastructure, ownership, or data-flow graphs. Assert allowed directions, forbidden cycles, layer access, bounded public surface, ownership, and generated-code treatment.

Architecture-test libraries such as ArchUnit can express structural rules for a particular ecosystem [2]. The durable artifact is the boundary rule and extraction semantics, not dependence on one library. Validate that reflection, generated code, plugins, dynamic loading, and indirect dependencies do not invalidate the graph.

**Check contracts and evolution.** Compare APIs, events, schemas, configuration, and policy against compatibility rules. Distinguish additive syntax from semantic compatibility. A new optional field may still alter defaults or privacy meaning.

Test producer-old/consumer-new and producer-new/consumer-old combinations across the actual coexistence window. Include migration, backfill, rollback, replay, retention, and deleted data. A schema-diff pass is evidence, not proof of consumer behavior.

**Check deployment architecture.** Compare declared placement, identity, network, storage, policy, resource, and failure-domain constraints with rendered and observed deployment. Enforce cell, region, tenant, key, and control-plane boundaries.

Do not make the deployment control plane the only observer of itself. Independent inventory or probes can detect drift the reconciler normalizes or fails to report. Cold bootstrap and disaster recovery need separate functions.

**Use runtime functions for emergent behavior.** Measure client outcomes, business invariants, freshness, queue age, tail latency, authorization, resource saturation, and recovery. Define populations, timeouts, missing data, versions, and workload.

Google's SRE guidance distinguishes service-level indicators, objectives, and error budgets as operational tools [3]. An SLO can be one fitness function, but architecture needs other properties: data authority, structural coupling, restore, security, and change safety.

**Design failure and recovery functions.** Periodically inject controlled faults or run simulations and exercises for partial failure, failover, stale authority, backlog, identity outage, restore, and reconciliation. Record exact scenario, configuration, workload, oracles, exposure, abort, and limitations.

A successful process restart cannot pass a business recovery function. Measure from impact start through useful service, integrity, security, backlog, and ambiguous outcome repair.

**Guard data architecture.** Check ownership, schema, lineage, residency, retention, deletion, classification, access, freshness, and reconciliation. Static catalog rules detect missing metadata; runtime probes verify actual flow and deletion behavior.

Beware self-reported labels. A dataset marked “EU only” does not prove every replica, backup, log, cache, and support path respects the boundary. Combine declared and observed evidence.

**Guard security properties.** Check least-privilege policies, trust boundaries, credential scope, artifact integrity, dependency provenance, secret exposure, revocation, audit, and recovery access. Use threat scenarios to choose functions.

Security scanners find selected patterns; absence of findings is not absence of vulnerability. Adversarial testing, review, and incident evidence remain necessary. NIST cyber-resilience guidance emphasizes anticipating, withstanding, recovering from, and adapting to adverse conditions across systems [4].

**Include human and accessibility properties.** Some functions require structured review, representative tasks, drills, or audits. An incident-console function can test keyboard and screen-reader completion under alert load against applicable WCAG 2.2 criteria and user evidence [5].

Do not automate away affected people. Conformance rules catch regressions, while representative research and accountable review assess context, comprehension, workload, and harm.

**Set thresholds from consequences.** Derive bounds from scenarios, capacity, safety margins, contracts, law, and empirical distributions. State measurement uncertainty. A convenient round number is not a rationale.

Use warning bands for approaching sensitivity points and hard gates for non-negotiable invariants. Avoid a gate whose required remote service is flaky or outside the team's control; mirror stable evidence or design a governed fallback.

**Use baselines and ratchets for legacy systems.** A legacy dependency graph may already violate the target. Record the accepted baseline, prevent new violations, and require a reduction plan. Ratchets should count meaningful exposure, not encourage splitting one violation into many labels.

Do not ratchet mandatory harm indefinitely. Critical security, safety, privacy, or legal violations need competent handling, containment, and deadlines beyond ordinary improvement policy.

**Govern exceptions.** An exception names exact rule, component, owner, reason, consequence, compensating control, approval, issue, expiry, and removal test. Store it with the governed configuration so it is visible to the function.

Nonexpiring allowlists convert architecture into folklore. Renew only after reviewing evidence and alternatives. Alert before expiry; expiration should have a predesigned behavior rather than surprise production failure.

**Control noise and flakiness.** A function that frequently fails without architectural consequence trains teams to ignore it. Separate infrastructure failure, unavailable evidence, inconclusive result, and property violation. Track false positives and false negatives.

Fix unstable measurement at its cause. Quarantine may be temporary with owner and deadline, but should not report pass. Use repeated measures, confidence intervals, deterministic fixtures, or robust thresholds appropriate to variability.

**Prevent gaming.** Teams may rename modules, exclude timeouts, suppress telemetry, move dependencies behind a facade, split incidents, or narrow measured populations. Review whether the measure remains causally connected to the property.

Pair proxies with outcome guardrails. A dependency count needs direction and consequence. Deployment frequency needs change-failure and recovery evidence. Cost per request needs correctness, latency, and sustainability boundaries.

**Decide enforcement by consequence and confidence.** A fast deterministic rule protecting a mandatory boundary can block immediately. A noisy early metric may warn and collect evidence. A holistic exercise can gate a high-risk release or produce an owned risk decision.

Define escalation and repair. A blocked pipeline without a reachable owner delays work; an alert without decision authority creates noise. Enforcement is an organizational architecture decision too.

**Maintain a portfolio.** Map functions to scenarios, qualities, views, decisions, risks, lifecycle stages, and owners. Look for overconcentration on code structure while data, runtime, recovery, security, people, and suppliers remain uncovered.

Coverage is a traceable argument, not a correctness percentage. Record gaps and why they require manual review, future tooling, field evidence, or external authority.

**Evolve and retire functions.** Add checks after new decisions, incidents, threats, standards, and failure evidence. Revise thresholds when workload or consequences change, preserving history and rationale. Retire a function only when its property disappears, another function demonstrably subsumes it, or accountable governance changes the decision.

Fitness functions are architecture as executable or repeatable evidence. They guide evolution; they do not eliminate architectural judgment.

## Definitions and Notation

Let:

- $F=(p,s,m,t,g,o,e,a,x)$ represent property, scope, measure, threshold, trigger, owner, evidence, action, and expiry;
- $v_F$ be the observed value and $t_F$ its threshold under a declared comparison;
- $B$ be a budget and $c_i$ consumption item $i$ in window $W$;
- $b_0$ be an accepted baseline and $b_n$ the current value under a ratchet;
- $E_F$ be the set of active exceptions for function $F$;
- $P$ be protected scenarios and $M$ the mapping from functions to scenarios;
- **false positive** mean a failure verdict when the protected property is acceptable under the specification;
- **false negative** mean a passing verdict while the protected property is violated;
- **inconclusive** mean available evidence cannot support pass or fail;
- **fitness debt** mean known unprotected or excepted architectural exposure with ownership and treatment—not a generic backlog label.

For a decreasing-is-better ratchet, require $b_n\le b_0$ while planned work lowers $b_0$. The count is meaningful only if extraction and severity remain stable; otherwise the ratchet can be gamed.

## Mechanisms, Invariants, or Proof Structure

### Portfolio procedure

1. Select consequential scenarios, decisions, risks, sensitivities, and mandatory boundaries.
2. Specify each function completely, including oracle, evidence, response, and expiry.
3. Choose the earliest useful static or triggered check and the necessary holistic confirmation.
4. Establish baselines, thresholds, budgets, warning bands, and noncompensatory gates.
5. Implement deterministic evidence capture and explicit pass, fail, inconclusive, and unavailable states.
6. Pilot against known conforming and violating cases, including attempts to game the measure.
7. Assign enforcement by consequence, confidence, reversibility, and owner response.
8. Govern exceptions, false results, outages, evidence retention, and sensitive data.
9. Map portfolio coverage and gaps across views, qualities, lifecycle stages, and stakeholders.
10. Recalibrate, add, replace, or retire functions through reviewed architecture decisions.

### A reproducible static function

The following standard-library example checks one declared dependency direction. It proves only the supplied graph against this rule.

<!-- bijux-verify: {"id":"dependency-boundary","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"PASS: dependency policy\n","stderr":""}} -->
```python
allowed = {
    "web": {"billing"},
    "billing": {"ledger"},
    "ledger": set(),
}
actual = {
    "web": {"billing"},
    "billing": {"ledger"},
    "ledger": set(),
}

violations = sorted(
    (source, target)
    for source, targets in actual.items()
    for target in targets
    if target not in allowed.get(source, set())
)
if violations:
    raise SystemExit(f"forbidden dependencies: {violations}")
print("PASS: dependency policy")
```

Production extraction must also define indirect, generated, reflective, plugin, and external edges. A hidden runtime dependency can pass this example.

### Invariants

- no fitness function lacks a protected property and decision rationale;
- no atomic mechanism check claims an end-to-end outcome;
- no missing or unavailable evidence becomes pass;
- no threshold changes without versioned rationale and impact review;
- no exception lacks exact scope, owner, compensating control, and expiry;
- no proxy remains unchallenged by outcome and gaming tests;
- no portfolio claims exhaustive architectural correctness.

## Alternatives and Trade-Offs

- **Static versus dynamic:** static checks are fast and deterministic; dynamic checks observe emergent behavior at greater cost and variability.
- **Atomic versus holistic:** atomic rules isolate causes; holistic functions validate outcomes but complicate attribution.
- **Build-time versus runtime:** build gates prevent known drift; runtime functions see state, workload, dependencies, and operators.
- **Blocking versus advisory:** blocking protects strong high-confidence invariants; advisory modes collect evidence but can become ignored noise.
- **Absolute threshold versus ratchet:** absolute gates express the target; ratchets make legacy improvement feasible but can normalize old exposure.
- **Rule versus budget:** rules forbid a class; budgets allocate tolerated consumption. Mandatory harm should remain a rule.
- **Central policy versus team-owned functions:** central rules improve consistency; local ownership captures domain context. Shared schemas with federated thresholds can combine them.
- **Generated architecture model versus observed inventory:** generation catches intended drift early; observation catches deployment reality but arrives later.
- **Proxy versus outcome:** proxies are cheap and leading; outcomes are valid but often lagging. Pair them.
- **Deterministic fixture versus production sample:** fixtures reproduce boundaries; production samples cover realism but introduce privacy, variance, and selection limits.
- **Broad coverage versus fast feedback:** more functions cover more concerns; too many slow gates degrade delivery and invite bypass.
- **Automation versus human review:** automation repeats precise checks; humans interpret ambiguous, ethical, social, and novel consequences.

## Failure Modes and Misconceptions

1. **“Every test is a fitness function.”** It must protect a significant architectural characteristic and trace to a decision.
2. **“Green functions prove good architecture.”** The portfolio covers selected properties and can omit decisive concerns.
3. **“Static rules prove runtime isolation.”** Dynamic loading, deployment, identity, and data paths may differ.
4. **“An SLO is the architecture.”** It covers selected service outcomes, not every structural, data, change, or security property.
5. **“More checks mean more quality.”** Noise, duplication, and weak proxies can reduce governance.
6. **“A threshold is objective.”** Boundary, units, consequences, data, and authority determine it.
7. **“Missing telemetry is zero.”** It is unavailable or inconclusive unless independent evidence supports a verdict.
8. **“Warnings are harmless.”** Permanent warnings teach bypass and hide real failures.
9. **“Exceptions are documentation.”** Without expiry and enforcement they become silent policy changes.
10. **“Ratchets always improve architecture.”** Unstable extraction or count splitting can game them.
11. **“A product rule is durable.”** Express the owned property and keep tool choice replaceable.
12. **“Component checks compose automatically.”** Emergent end-to-end behavior needs its own oracle.
13. **“CI is the only cadence.”** recovery, human, supplier, and physical properties need periodic evidence.
14. **“Flaky checks should be retried until green.”** Retrying can hide measurement defects and selection bias.
15. **“Fast delivery justifies bypass.”** Consequence and competent authority determine exception, not urgency alone.
16. **“One global policy fits every product.”** shared intent may require context-specific scope and thresholds.
17. **“Fitness functions remove architects.”** They automate evidence for selected judgments and create new design work.
18. **“Passing is certification.”** Internal checks do not create external assurance or approval.

## Worked Examples

### Example 1

**Enforce a dependency direction.**

**Situation.** A modular monolith requires `ledger` to remain independent of `billing` and `web`.

**Reasoning.** The executable function extracts edges and compares them with an allowed graph. Known legal and forbidden fixtures test the oracle. Generated code, reflection, plugins, and external calls receive explicit extraction policy. A runtime business-invariant function separately verifies that invoice acceptance creates one ledger intent.

**Conclusion.** The static function prevents one coupling form but does not overclaim business correctness.

### Example 2

**Guard schema coexistence.**

**Situation.** Event producers and consumers coexist for 30 days during fleet rollout.

**Reasoning.** CI checks syntax compatibility in both version directions, while semantic fixtures exercise defaults, units, identity, deletion, and unknown fields. Replay tests use the full retention window. An exception for one consumer names owner, isolated topic, compensating translator, seven-day expiry, and removal evidence.

**Conclusion.** Compatibility is a lifecycle property requiring more than an additive-schema diff.

### Example 3

**Pair latency with correctness.**

**Situation.** A service meets p99 latency after changing failures into fast cached responses.

**Reasoning.** The fitness function population begins at client intent, counts timeouts, classifies stale and incorrect results, and gates useful success and freshness alongside latency. Component histograms remain diagnostic. Missing telemetry makes the result inconclusive, and an external probe confirms the path.

**Conclusion.** Outcome guardrails prevent performance optimization from rewarding incorrect availability.

### Example 4

**Constrain cell blast radius.**

**Situation.** A cell architecture promises no cell holds more than 5% of tenants or 8% of peak work.

**Reasoning.** Deployment checks inspect tenant placement and weighted demand, not record count. Runtime checks simulate one-cell loss and verify admission prevents healthy-cell overload. A warning triggers at 4% tenant or 6.5% work; the hard gate blocks new placement above the declared bounds.

**Conclusion.** Static distribution and dynamic failure capacity jointly protect containment.

### Example 5

**Detect residency drift.**

**Situation.** A catalog says regulated records remain in one jurisdiction.

**Reasoning.** Policy checks declared stores, replicas, backups, logs, caches, keys, support routes, and processing locations. Independent inventory and synthetic tagged records verify observed paths. Unknown location or missing scan is inconclusive, not compliant. Exceptions require legal and data authority and expire.

**Conclusion.** Self-reported metadata needs observed end-to-end evidence.

### Example 6

**Ratchet legacy coupling.**

**Situation.** A legacy codebase has 120 forbidden dependency edges and cannot remove them in one release.

**Reasoning.** The baseline is captured with stable extraction, severity, and exact edges. CI forbids new edges and requires current count no greater than 120, while an owned plan lowers the baseline. Renames preserve edge identity, and splitting modules cannot reduce weighted exposure artificially. Critical trust-boundary edges remain absolute failures.

**Conclusion.** A governed ratchet enables improvement without turning the legacy baseline into permission for new drift.

### Example 7

**Test deploy independence.**

**Situation.** Two services are nominally independent but 80% of releases change and deploy together.

**Reasoning.** A leading function detects shared schema, library, pipeline, and approval dependencies; a lagging measure tracks forced co-change with cause, not just correlation. A scenario changes one service under mixed versions and rolls it back independently. The threshold triggers architecture review rather than automatically demanding separation.

**Conclusion.** Co-change is evidence for investigation, while compatibility and deployment tests establish the actual property.

### Example 8

**Make recovery periodic.**

**Situation.** Daily backup checks are green, but no full restore has run since a schema migration.

**Reasoning.** Atomic functions verify creation, integrity metadata, encryption, retention, and independent location. A quarterly holistic function restores the selected clean point into isolated infrastructure, verifies application compatibility and authoritative outcomes, measures resource peaks and time, then reconciles. Schema or key changes expire prior evidence.

**Conclusion.** Backup existence is a leading mechanism check; restored useful service is the outcome function.

### Example 9

**Bound an energy metric.**

**Situation.** A batch platform minimizes joules per completed record by retrying failed large batches until one succeeds.

**Reasoning.** The boundary includes all attempts, storage, network, and checkpoint work over the job intent. Guardrails constrain deadline, correctness, duplicate effect, failure rate, and hardware assumptions. Results report workload and carbon-intensity source separately; joules do not become an unsupported environmental-impact total.

**Conclusion.** Stable identity and full-work boundaries prevent retry waste from disappearing.

### Example 10

**Protect an accessible emergency action.**

**Situation.** An incident console ships weekly and must support keyboard and screen-reader operators.

**Reasoning.** Automated checks cover focus order, accessible name/state, contrast, and keyboard reachability against cited criteria. A release-blocking task fixture exercises acknowledgement and emergency isolation. Periodic representative studies under alert load assess comprehension, time, errors, and recovery. An unavailable assistive-technology runner blocks the relevant gate rather than reporting pass.

**Conclusion.** Automated conformance and human-task evidence form complementary fitness functions, not interchangeable proof.

## Cross-Program Connections

- **Software Testing and Quality Engineering:** owns test design, oracles, static and dynamic analysis, flakiness, coverage, and evidence validity.
- **Software Delivery and Reliability Engineering:** owns CI/CD enforcement, SLOs, error budgets, release health, incidents, and recovery exercises.
- **Platform Engineering:** owns policy engines, deployment inventory, isolation, telemetry, and reusable developer feedback.
- **Security Engineering:** owns threat-derived controls, security testing, exceptions, assurance, compromise, and residual authority.
- **Data Architecture Engineering:** owns data contracts, lineage, residency, retention, deletion, governance, and reconciliation.
- **API and Service Engineering:** owns compatibility, deadlines, errors, idempotency, status, and client outcome contracts.
- **Systems Engineering:** owns physical tests, hazards, lifecycle assurance, human operation, and accountable acceptance.
- **Software Engineering Patterns:** supplies structural mechanisms whose context and drift fitness functions can assess.
- **Algorithm Engineering:** supplies graph, statistical, optimization, and approximation foundations for measurements.
- **Requirements Engineering:** owns driver and requirement traceability, change, conflict, validation, and stakeholder legitimacy.

## References

1. Neal Ford, Rebecca Parsons, Patrick Kua, and Pramod Sadalage, *Building Evolutionary Architectures*, 2nd ed., O'Reilly Media, 2022.
2. ArchUnit, *User Guide*, current documentation; retrieved 2026-09-06. <https://www.archunit.org/userguide/html/000_Index.html>
3. Alex Hidalgo, “Implementing SLOs,” in *The Site Reliability Workbook*, O'Reilly Media, 2018; retrieved 2026-09-06. <https://sre.google/workbook/implementing-slos/>
4. National Institute of Standards and Technology, *Developing Cyber-Resilient Systems: A Systems Security Engineering Approach*, NIST SP 800-160 Volume 2 Revision 1, December 2021. <https://doi.org/10.6028/NIST.SP.800-160v2r1>
5. W3C, *Web Content Accessibility Guidelines (WCAG) 2.2*, W3C Recommendation, 12 December 2024; retrieved 2026-09-06. <https://www.w3.org/TR/WCAG22/>
6. Len Bass, Paul Clements, and Rick Kazman, *Software Architecture in Practice*, 4th ed., Addison-Wesley, 2021.
7. ISO/IEC, *Systems and Software Engineering — Systems and Software Quality Models*, ISO/IEC 25010:2023, November 2023. <https://www.iso.org/standard/78176.html>
8. ISO/IEC/IEEE, *Systems and Software Engineering — Architecture Description*, ISO/IEC/IEEE 42010:2022, November 2022. <https://standards.ieee.org/ieee/42010/6846/>
9. Nicole Forsgren, Jez Humble, and Gene Kim, *Accelerate*, IT Revolution, 2018.
10. Martin Fowler, “Circuit Breaker,” 6 March 2014; retrieved 2026-09-06. <https://martinfowler.com/bliki/CircuitBreaker.html>

## Exercises

### Exercise 1

Define architecture fitness function, atomic, holistic, static, dynamic, triggered, continuous, periodic, leading indicator, lagging indicator, guardrail, target, budget, baseline, ratchet, exception, false positive, false negative, inconclusive, drift, and fitness debt.

### Exercise 2

A legacy graph has 120 forbidden edges. A release removes 18, adds 7 different forbidden edges, and hides 5 through an unscanned plugin path. Compute the reported and actual counts under a naive ratchet, diagnose its failures, and design a stable weighted rule.

### Exercise 3

Diagnose a portfolio containing only code linters and server uptime, with timeouts excluded, missing metrics treated as zero, permanent allowlists, retry-until-green flaky tests, and one global score. Replace it with lifecycle and outcome coverage.

### Exercise 4

Compare static, dynamic, atomic, holistic, build-time, deployment, runtime, and periodic fitness functions for a multi-region financial service. Assign properties, oracles, enforcement, exceptions, and evidence limits.

### Exercise 5

Design an architecture-fitness portfolio for an international smart-water system with treatment plants, pumps, intermittent sensors, local operators, cloud optimization, privacy-sensitive household meters, legacy controllers, safety limits, environmental reporting, and long-lived devices. Cover scenarios, static and dynamic checks, physical and human evidence, thresholds, budgets, ratchets, exceptions, enforcement, gaming, ownership, coverage gaps, and evolution.

## Answers to the Exercises

### Answer 1

An **architecture fitness function** repeatedly assesses a significant architectural characteristic. **Atomic** checks one characteristic; **holistic** checks emergent behavior. **Static** inspects artifacts; **dynamic** observes execution. **Triggered** runs on change or event; **continuous** runs frequently enough to constrain drift; **periodic** runs on schedule. A **leading indicator** precedes harm; a **lagging indicator** records outcome. A **guardrail** is mandatory; a **target** is desired; a **budget** allocates tolerated consumption. A **baseline** is recorded current state; a **ratchet** prevents regression. An **exception** is scoped, owned, compensated, and expiring. **False positive** fails an acceptable property; **false negative** passes a violation; **inconclusive** lacks evidence. **Drift** diverges from intent. **Fitness debt** is owned unprotected or excepted exposure with treatment.

### Answer 2

The naive visible count becomes $120-18+7=109$, so it passes a decreasing count ratchet and may reset baseline to 109. The actual count includes five hidden plugin edges: 114. More importantly, count alone treats all directions and consequences equally; seven new violations should fail even if removals outnumber them, and the scanner's missing path creates false negatives.

Stabilize extraction across source, generated code, plugins, reflection where possible, manifests, and runtime observations. Preserve edge identity and compare sets: no newly forbidden edge is allowed. Weight or gate edges by durable boundary and consequence—for example, trust or authority violations are absolute, while legacy internal edges have a decreasing weighted exposure baseline. Version extraction changes, test known legal/illegal/hidden fixtures, report unavailable coverage, and require every exception to name edge, owner, rationale, control, expiry, and removal evidence.

### Answer 3

Trace consequential scenarios across code, API/schema, data, deployment, control, runtime, recovery, security, accessibility, people, and suppliers. Keep linters only where their rules protect explicit boundaries. Replace uptime with client-intent useful outcomes including errors, timeouts, stale and unknown states, cohorts, missing-data policy, and independent probes. Add contract coexistence, observed topology and identity, residency and deletion, authorization and revocation, tail/capacity, queue age, business invariants, fault/recovery, restore, and representative operator-task functions.

Missing evidence is unavailable or inconclusive, never zero. Repair flakiness and distinguish infrastructure failure from property violation; temporary quarantine keeps owner and deadline and cannot report pass. Convert allowlists to exact expiring exceptions with compensating controls. Preserve response vectors and mandatory gates rather than one score. Assign enforcement by consequence and confidence, pair leading mechanism checks with lagging outcomes, retain evidence and architecture versions, map gaps explicitly, and evolve the portfolio after changes and incidents.

### Answer 4

Static build functions enforce dependency direction, public API/schema compatibility, secret and policy patterns, artifact provenance, and infrastructure constraints. Atomic deployment functions check region/cell placement, identities, permissions, resource bounds, and migration compatibility. Dynamic runtime functions measure client-visible correct outcomes, authorization, freshness, tail latency, saturation, and queue age. Holistic periodic functions inject region and identity failures, restore data, reconcile payments, test cold bootstrap, and exercise operators.

Build gates can block deterministic high-confidence violations. Deployment gates protect mandatory trust, compatibility, and authority boundaries with independent inventory. Runtime objectives page or halt rollout according to consequence and evidence; missing telemetry is inconclusive. Periodic exercises gate high-risk architecture decisions or produce owned findings. Exceptions are exact, approved by competent financial/security/data authority, compensated, observable, and expiring. Each result names workload, data, topology, versions, observer, fault, population, limitations, and evidence expiry; no component pass proves end-to-end financial integrity or regulatory compliance.

### Answer 5

Scenarios cover safe chemical and pressure control, pump deadline, sensor omission or compromise, island operation, cloud loss, full buffer, stale optimization, household privacy, controller update, environmental report, restoration, and operator emergency action. Static functions check control authority, signed artifacts, firmware/hardware compatibility, protocol ranges, network segmentation, data classification/residency/retention, schema coexistence, and configured safety envelopes. Dynamic functions test sensor plausibility, command epoch and expiry, independent actuator state, latency/jitter, buffer age, reconnect drain, authorization/revocation, cloud degradation, energy use, and report reconciliation.

Physical hardware-in-the-loop and authorized plant tests validate interlocks, pumps, chemistry, power, and legacy behavior; representative operator exercises validate alarms, accessibility, manual control, handoff, and recovery. Safety, environmental, privacy, authenticated authority, and no stale actuation are hard guardrails. Budgets may cover telemetry loss or noncritical analytical freshness, not unsafe water. Legacy policy can ratchet ordinary dependency or metadata exposure, while critical safety/security defects require containment and competent deadlines.

Exceptions name exact plant/device/rule, owner, reason, consequence, compensating local control, monitoring, approval, expiry, and replacement proof. Deterministic high-confidence rules block; variable runtime functions use warning and hard bands; unsafe physical tests require safety authority and independent abort. Test gaming through relabeling, omitted offline devices, average-only water quality, suppressed missing telemetry, and cloud-only observation. Owners span plant safety, operations, environmental, privacy, security, device, cloud, data, accessibility, and municipal authority. Map uncovered suppliers, field conditions, populations, attacks, and long-duration failures; add or revise functions after hardware, chemistry, law, climate, workload, incident, or evidence change. No portfolio itself certifies safe drinking water or regulatory compliance.
