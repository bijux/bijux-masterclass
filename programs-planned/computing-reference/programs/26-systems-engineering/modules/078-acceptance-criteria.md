---
module_id: SYSENG-078
program: Systems Engineering
level: 2
module_number: 78
title: Acceptance Criteria
status: complete
last_verified: 2026-08-31
---

# Acceptance Criteria

## One-Page Review

### Governing question

What exact, pre-agreed evidence, configuration, tolerances, delivery conditions, and authority are required to accept, conditionally accept, or reject a system—and what obligations and risks change when that decision is made?

### Essential definitions

- **Acceptance** is an authorized customer's formal decision that an identified product or service satisfies the applicable acceptance basis sufficiently for the specified transfer, use, payment, or lifecycle transition. Its legal effect depends on the governing agreement.
- An **acceptance criterion** is a necessary, decision-ready condition a deliverable must satisfy. It identifies subject, measure or required artifact, method/evidence, environment, threshold/tolerance, timing, and authority.
- The **acceptance basis** is the controlled collection of contract terms, specifications, stakeholder expectations, regulations, standards, approved plans, configurations, and criteria that governs the decision.
- **Acceptance testing** is formal evaluation against acceptance criteria. It can use verification and validation evidence but is not synonymous with all verification, validation, qualification, certification, or operational readiness work.
- A **delivery** or **tender** is the exact product/service and accompanying data offered for acceptance. Physical possession or deployment does not necessarily equal formal acceptance.
- **Conditional acceptance** accepts a nonconforming or incomplete delivery subject to explicit corrections, deadlines, controls, remedies, and authority. Terminology and permissibility depend on the governing context.
- A **deviation/waiver** is authorized departure from a requirement or criterion under defined scope and rationale. It is not an informal agreement to ignore a failure.
- A **latent defect** is a defect not reasonably discoverable by the prescribed inspection/acceptance process; legal treatment depends on contract and jurisdiction.
- A **acceptance data package** links the tendered configuration to results, anomalies, approvals, certifications, manuals, rights/licenses, training, support, and unresolved obligations.
- **Rejection** is the authorized refusal to accept a tender that does not satisfy the acceptance basis, accompanied by controlled notice, disposition, cure/retest rules, and preservation of evidence.

### Central model, mechanism, or theorem

For tendered configuration $x$, define criteria $C=\{c_1,\ldots,c_n\}$. Each criterion has predicate $p_i(x,E_i)$ over controlled evidence $E_i$, criticality $k_i$, and permitted disposition set $D_i$. The decision rule is not a simple average:

$$
A(x)=
\begin{cases}
\text{accept}, & \text{all mandatory }p_i\text{ pass},\\
\text{conditional}, & \text{only authorized conditions remain and controls are approved},\\
\text{reject}, & \text{a blocking criterion fails or evidence is insufficient}.
\end{cases}
$$

Authority, contract, safety, and law constrain $D_i$. High performance elsewhere cannot compensate for a mandatory safety, security, legal, configuration, or delivery failure unless the controlling authority explicitly permits and documents that disposition.

### Critical invariants

- Criteria are agreed before evidence is observed and trace to an authoritative acceptance basis.
- Every criterion is necessary, unambiguous, feasible, measurable or objectively reviewable, and tied to a named decision owner.
- Threshold, statistic, tolerance, units, population, measurement plane, environment, repetitions, uncertainty, and rounding are explicit where quantitative.
- The acceptance article/service and evidence share exact version, build, serial/lot, configuration, data, dependencies, site, and time identity.
- Verification, validation, qualification, certification, readiness, documentation, training, support, rights, security, and transition obligations are included when acceptance depends on them.
- Pass/fail/conditional/not-evaluated states are distinct; missing evidence is not a pass.
- Mandatory or critical failures cannot be averaged away by many low-criticality passes.
- Criteria changes after execution require authorized change control, rationale, impact analysis, and protection against outcome-driven threshold manipulation.
- Deviations and conditional acceptance name scope, owner, due date, controls, residual risk, remedy, retest, and consequence of nonclosure.
- The accepting authority is independent of evidence production to the degree required by governance and retains the ability to reject.
- Acceptance records what transfers—ownership, custody, operational authority, risk, support, payment eligibility, and configuration—and what does not.
- Post-acceptance warranty, latent-defect, correction, monitoring, and reacceptance rights remain governed and traceable.

### Common failures

Common failures include “works as expected”; criteria copied from vague requirements; thresholds chosen after seeing results; evidence from a different build; demo success substituted for controlled tests; pass by average despite a critical failure; unbounded “minor defects”; undocumented side agreements; customer attendance mistaken for authorization; delivery, installation, readiness, and acceptance conflated; accepting software without source/binaries/configuration/data rights/licenses/manuals; accepting services from a dashboard average without sampling; treating certification as proof of intended-use fitness; waiving an unknown risk; conditional acceptance without deadlines/remedies; and assuming acceptance erases warranty or latent-defect obligations.

### Compact example

A synthetic tender has eight criteria. Six pass, one documentation item is eligible for a controlled condition, and the safety-case criterion fails. The decision is rejection because the failure is blocking. After the safety case is cured and re-evaluated, seven criteria pass and one remains conditionally met; the fixture reports that conditional acceptance still requires named authority. It does not make a real contractual, safety, or legal decision.

### Connections

Requirements quality, verification matrices, validation, qualification, certification, anomalies, risk acceptance, contracting, configuration management, release engineering, operational readiness, transition, warranties, service-level management, audit, and governance converge in acceptance criteria.

## Governing Question

Can an authorized decision maker examine the tender and its configuration-linked evidence and determine—without negotiation-by-memory—whether to accept, conditionally accept, or reject it, what transfers at that moment, and what unresolved obligations remain?

Acceptance is not a synonym for technical quality. It is a governed decision at a boundary between provider and receiver. The same verified system may be unacceptable because required training, licenses, data rights, spares, security authorization, installation, manuals, or validation evidence are missing. Conversely, a receiver may be authorized to accept a bounded nonconformance with controls and consideration. Engineering must make the decision legible without pretending to replace contractual or statutory authority.

## Why This Matters

NASA's software acceptance guidance defines acceptance criteria as conditions a product must satisfy for acceptance and emphasizes working with the customer up front, acceptable ranges, importance, V&V, technical data, certifications, rights, maintenance, documentation, and release readiness. NASA Product Transition treats verified and validated products plus enabling resources as the bridge to the next integration level or end user.

The current Federal Acquisition Regulation illustrates why authority and consequences matter. FAR acceptance is the authorized Government acknowledgment of contract conformity; it assigns acceptance responsibility, addresses timing and evidence, usually rejects nonconforming supplies/services, permits bounded conditional acceptance under specified authority, and distinguishes inspection, title/risk, latent defects, and warranties. Private, international, regulated, or internal contexts have different rules, so engineers must identify governing terms rather than generalize FAR as universal law.

Weak criteria move disagreement to the most expensive moment. “High availability,” “complete documentation,” and “no severe defects” invite incompatible interpretations. Strong criteria expose missing measurement definitions, environments, evidence, owners, and remedies while correction is still possible. They also prevent a visually successful demonstration or schedule emergency from silently redefining success.

Acceptance can transfer operational and financial risk. A signature may authorize shipment, payment, title transfer, deployment, or support commencement. Conditional acceptance may create deadlines and remedies. Rejection may trigger cure, replacement, reperformance, or dispute. Technical evidence must therefore be accurate, reproducible, configuration-bound, and honest about uncertainty.

## Prerequisites and Retrieval

Before drafting or applying acceptance criteria, retrieve:

1. governing contract/order/charter, statement of work, specifications, stakeholder expectations, regulations, standards, policies, precedence, definitions, jurisdiction, and authorized acceptance/rejection roles;
2. deliverable/tender inventory with quantities, services, increments, sites, versions, builds, serials/lots, configurations, dependencies, data, documentation, licenses/rights, certificates, support, training, spares, and delivery dates;
3. intended use, ConOps, user/customer needs, criticality, hazards, threats, privacy/ethics, regulatory approvals, operational constraints, and unacceptable outcomes;
4. verification, validation, qualification, certification, assurance, audit, safety/security, reliability, usability, performance, compatibility, and readiness evidence required for this decision;
5. criterion IDs, trace, rationale, criticality, exact subject, preconditions, method, sample/population, environment, instrumentation, units, threshold/tolerance, statistic/window, uncertainty, expected result, and record format;
6. acceptance plan/procedure with article control, customer witnessing, independent roles, facilities, data, entry/abort criteria, deviations, anomaly workflow, retest, schedule, costs, and evidence delivery;
7. configuration-status accounting showing evidence applies to the tendered as-built/as-deployed product and identifying every unverified difference;
8. anomaly/nonconformance register with severity, affected criteria, causal/impact analysis, correction, regression, waiver/deviation authority, residual risk, and closure state;
9. conditional-acceptance rules: allowed classes, technical concurrence, safety/health/security/legal concurrence, correction owner/date, controls, price/payment adjustment, warranty, monitoring, retest, revocation/rejection remedy;
10. transition/readiness evidence for installation, facilities, operators, training, procedures, data migration, backup/restore, support/escalation, maintenance, supply, cybersecurity operations, continuity, and decommissioning;
11. acceptance certificate/record template with tender identity, basis revision, results, exceptions, decision, authority, date/location, transfer effects, reservations, open conditions, warranties, and attachments;
12. post-acceptance obligations and rights: correction, warranty, service levels, latent defects, recall, vulnerability handling, data retention, audit, updates, reacceptance, final payment, and closeout.

Perform a **decision rehearsal**: for each possible pass, fail, missing, ambiguous, or anomalous result, ask who decides, under what clause/authority, with what evidence, by when, what transfers, and what remedy follows. If the answer depends on an unrecorded conversation, the criterion set is not decision-ready.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish acceptance from verification, validation, qualification, certification, readiness, delivery, and payment;
2. identify the acceptance basis, tender, receiver, provider, and authorized decision maker;
3. write testable quantitative and objectively reviewable qualitative criteria;
4. define tolerances, statistics, uncertainty, samples, environments, and evidence applicability;
5. construct a criticality-aware decision rule that prevents compensation of mandatory failures;
6. bind evidence and anomalies to the exact tendered configuration;
7. design controlled acceptance tests, reviews, witnessing, and data packages;
8. govern rejection, correction, retest, waiver, deviation, and conditional acceptance;
9. include transition products, support, rights, documentation, training, and readiness;
10. preserve post-acceptance obligations, reservations, monitoring, and reacceptance triggers.

## Core Exposition

**Identify the governed decision.** State what is being accepted, by whom, from whom, for what purpose and increment, under which authority, at what place/time, and with what effect. System acceptance, shipment authorization, operational authorization, invoice approval, release approval, and site acceptance may be separate decisions.

**Establish one acceptance basis.** Build a controlled hierarchy of contract clauses, specifications, approved changes, stakeholder criteria, standards, and plans. Resolve precedence and ambiguity early. Requirements alone rarely cover delivery artifacts, ownership, licenses, training, support, warranty, or transition.

**Define the tender precisely.** Identify quantities, serial/lot, hardware, software build, configuration, dependencies, data, models, infrastructure, site, documents, rights, and services. Evidence from prototype A cannot accept production unit B without an authorized equivalence argument and sampling scheme.

**Write atomic criteria.** A criterion should express one decision condition. Include criterion ID; trace and rationale; criticality; subject; preconditions; method; environment; inputs; measurement; threshold/tolerance; expected artifact; responsible producer; reviewer/witness; and disposition rule. Avoid combining “secure, performant, reliable, and documented” into one checkbox.

**Make quantitative rules complete.** “Latency below 200 ms” omits measurement endpoints, request classes, load, warmup, sample size, statistic, window, errors, clock accuracy, and rounding. A complete criterion might specify 99th-percentile end-to-end latency at named planes under a controlled workload and configuration, with exclusion and uncertainty rules.

**Make qualitative rules objectively reviewable.** Documentation “complete” can mean every required document ID/version is present, approved, consistent with as-built configuration, searchable, free of blocking open items, and successfully used by representative maintainers in a defined task. Expert judgment is legitimate when qualifications, rubric, evidence, independence, dissent, and authority are recorded.

**Separate entry, execution, and acceptance criteria.** Entry criteria determine readiness to evaluate; test criteria determine individual outcomes; acceptance criteria govern the receiver's decision; exit/transition criteria govern movement onward. A test should not run on an unidentified build merely because schedule pressure satisfies none of these.

**Define criticality and noncompensation.** Classify blocking, mandatory, conditional-eligible, informational, or other governed categories. Safety, security, legal, identity, configuration, and essential mission criteria often need hard gates. Weighting can prioritize discretionary tradeoffs but must not average away forbidden outcomes.

**Control the evidence chain.** Link criterion to requirement/expectation, procedure, exact configuration, calibrated tools, raw data, calculation, result, anomaly, review, and decision. Preserve failed and superseded runs. Hashes, build provenance, serials, environment capture, signed records, and access control support integrity but do not prove technical correctness.

**Plan receiver participation.** Specify who authors, executes, witnesses, observes, analyzes, recommends, and decides. Provider self-test can be valuable; acceptance authority must still receive the evidence and independence required by agreement. Customer presence is not acceptance unless the authorized act occurs.

**Predefine anomaly rules.** State whether a failed run invalidates a criterion, when rerun is allowed, whether correction requires regression, how intermittent results are analyzed, and how test-setup errors are distinguished. Do not delete failures as “bad runs” after examining their inconvenience.

**Use conditional acceptance narrowly.** Confirm it is permitted. Characterize nonconformance and impact, establish safety/intended-use advice, obtain required concurrences, name corrective work/date, impose operational controls, define consideration/payment/warranty and retest, and specify failure-to-cure consequences. Unknown impact is not a safe condition.

**Treat waivers as decisions, not evidence.** A waiver changes the obligation or authorizes departure; it does not turn failed evidence into passed evidence. Record criterion as nonconforming-with-authorized-disposition and preserve residual risk, scope, expiration, dependencies, and authority.

**Include the whole transition package.** Acceptance may require installation, configuration, data migration, manuals, source/object artifacts, SBOMs, keys, licenses, rights, training, spares, calibration, support, incident/vulnerability process, backups, restore proof, monitoring, and disposal. A working executable with missing operational ownership is an incomplete tender.

**Distinguish design acceptance from unit/lot acceptance.** Qualification/validation may establish the design; production acceptance ensures each item or sampled lot conforms. Define sampling, lot formation, process controls, acceptance numbers, destructive-test treatment, traceability, and response to rejection. Do not repeatedly subject every operational item to damaging qualification extremes.

**Record the decision and transfer.** The acceptance record identifies tender, basis, evidence, exceptions, decision, authority, date, conditions, reservations, and consequences. Clarify title/custody, operational authority, risk, payment, support start, warranty, data rights, and open obligations under the governing agreement.

**Preserve post-acceptance controls.** Acceptance does not universally waive latent defects, fraud, gross mistakes, warranties, service obligations, cybersecurity reporting, or recall. State applicable rights rather than relying on assumption. Material changes or corrected conditions may require partial reacceptance.

The following fixture demonstrates a small criticality-aware decision rule.

<!-- bijux-verify: {"id":"acceptance-decision-fixture","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"criteria=8\npassed=6\nfailed=1\nconditionally_met=1\nblocking_failures=safety_case\ninitial_decision=reject\nafter_cure_passed=7\nafter_cure_conditionally_met=1\nafter_cure_decision=conditional_acceptance_requires_authority\nstatus=declared_acceptance_fixture_consistent\nevidence=synthetic_decision_rules_only\n","stderr":""}} -->
```python
criteria = {
    "functional_verification": ("passed", "mandatory"),
    "operational_validation": ("passed", "mandatory"),
    "safety_case": ("failed", "blocking"),
    "security_authorization": ("passed", "mandatory"),
    "as_built_configuration": ("passed", "mandatory"),
    "operator_training": ("passed", "mandatory"),
    "support_readiness": ("passed", "mandatory"),
    "maintenance_manual": ("conditional", "conditional_eligible"),
}

def decide(records):
    blocking = [
        name for name, (status, criticality) in records.items()
        if status == "failed" and criticality in {"blocking", "mandatory"}
    ]
    conditional = [name for name, (status, _) in records.items() if status == "conditional"]
    if blocking:
        return "reject", blocking
    if conditional:
        return "conditional_acceptance_requires_authority", []
    return "accept", []

initial, blocking = decide(criteria)
print(f"criteria={len(criteria)}")
print(f"passed={sum(status == 'passed' for status, _ in criteria.values())}")
print(f"failed={sum(status == 'failed' for status, _ in criteria.values())}")
print(f"conditionally_met={sum(status == 'conditional' for status, _ in criteria.values())}")
print("blocking_failures=" + ",".join(blocking))
print("initial_decision=" + initial)

criteria["safety_case"] = ("passed", "blocking")
after, _ = decide(criteria)
print(f"after_cure_passed={sum(status == 'passed' for status, _ in criteria.values())}")
print(f"after_cure_conditionally_met={sum(status == 'conditional' for status, _ in criteria.values())}")
print("after_cure_decision=" + after)
print("status=declared_acceptance_fixture_consistent")
print("evidence=synthetic_decision_rules_only")
```

The fixture cannot determine criterion adequacy, evidence truth, legal authority, safety, conditional-acceptance permissibility, remedy, or a real decision. It merely prevents a declared blocking failure from being averaged away.

## Definitions and Notation

Let tender $x=(q,v,c,s,d)$ identify quantity/items $q$, versions/builds $v$, configuration $c$, sites/services $s$, and delivery artifacts $d$. Acceptance basis $B_a$ names controlling agreements and revisions. Criterion $c_i=(p_i,k_i,E_i,D_i)$ includes decision predicate, criticality, evidence, and allowed disposition.

Use four-valued result $r_i\in\{\text{pass},\text{fail},\text{conditional},\text{not evaluated}\}$. “Not evaluated” cannot collapse into pass. Decision $A(x,B_a,C,R,\alpha)$ is made by authority $\alpha$ over criteria $C$ and results $R$. A waiver $w_i$ modifies permitted obligation/disposition; it does not rewrite $r_i$.

For measurement $Y$, a threshold rule must identify statistic $T(Y)$, limit $\theta$, comparison direction, rounding, confidence/uncertainty treatment, population, sample, and conditions. Margin $m=T(Y)-\theta$ has meaning only after sign convention and uncertainty are defined.

## Mechanisms, Invariants, or Proof Structure

A defensible acceptance argument follows this chain:

1. identify governing basis, tender, receiver/provider, decision, authority, and transfer consequences;
2. derive traceable atomic criteria covering product, evidence, transition, support, rights, and lifecycle obligations;
3. define thresholds, tolerances, environments, samples, uncertainty, qualitative rubrics, criticality, and disposition rules before execution;
4. establish controlled article/configuration and evidence provenance;
5. execute/witness prescribed inspection, analysis, demonstration, test, review, validation, and readiness work;
6. preserve results, deviations, failures, anomalies, corrections, regression, and technical recommendations;
7. apply noncompensatory gates and authorized waiver/conditional/rejection rules;
8. record the decision, transfer effects, reservations, remedies, open conditions, and post-acceptance obligations;
9. cure/retest or reject as governed, and reaccept when material configuration or obligation changes.

The invariants are prior agreement, authoritative trace, exact tender identity, objective decisionability, evidence integrity, critical-failure visibility, authorized exceptions, explicit transfer, enforceable conditions, and durable auditability.

## Alternatives and Trade-Offs

**Binary versus conditional acceptance.** Binary decisions are clear; conditional acceptance can enable urgent value but transfers risk and monitoring burden. Restrict eligibility and make cure enforceable.

**Customer testing versus supplier evidence.** Customer execution increases direct control but costs time and expertise. Supplier evidence scales when provenance, witnessing, audit rights, sampling, and independent checks match risk.

**Exhaustive versus sampled acceptance.** Every-item inspection reduces sampling uncertainty but may be costly or destructive. Sampling requires defensible lot formation, process stability, risks, and rejection response.

**Objective thresholds versus expert panels.** Numeric thresholds improve repeatability but can optimize proxies. Structured expert review captures complex adequacy but needs qualifications, rubric, evidence, dissent, and authority.

**Acceptance at source versus destination.** Source acceptance finds defects before shipment; destination acceptance captures transit, installation, site, and interface conditions. Assign each criterion to the meaningful plane.

**Single final gate versus incremental acceptance.** Incremental decisions improve feedback and cash flow but create interface, integration, rollback, and partial-ownership risks. Define dependencies and final system acceptance separately.

**Fixed criteria versus controlled learning.** Fixed criteria prevent outcome manipulation; genuine discoveries may require change. Use prospective change authority, rationale, equivalence/impact analysis, and rerun rules.

**Warranty versus pre-acceptance inspection.** Warranty can manage latent/long-term defects but does not replace critical inspection when harm, detection difficulty, or enforcement risk is high.

## Failure Modes and Misconceptions

**“Acceptance equals technical approval.”** It is an authority-owned decision with contractual/organizational consequences.

**“Delivered means accepted.”** Possession, installation, use, and formal acceptance may occur at different times under governing terms.

**“All tests passed.”** The tests may omit validation, configuration, documentation, rights, training, support, or readiness criteria.

**“A majority passes.”** Mandatory failures are not votes.

**“The threshold can be clarified after the run.”** Post-result changes invite bias and require formal control and often new evidence.

**“A waiver makes it conforming.”** It authorizes a bounded departure; preserve the nonconformance and residual risk.

**“Conditional means minor.”** Eligibility depends on impact, authority, controls, remedy, and intended use—not a casual severity label.

**“The customer saw it.”** Witnessing is not acceptance unless the authorized act and record say so.

**“Certification guarantees acceptance.”** Certification addresses its scheme; the acceptance basis may include additional product, use, delivery, and support obligations.

**“Acceptance ends responsibility.”** Applicable warranty, latent-defect, service, correction, security, and record obligations can remain.

## Worked Examples

### Example 1

A criterion says “search is fast.” Rewrite it as a named production build, representative indexed corpus and concurrent workload, measured client-to-result plane, warmup, query mix, successful-response handling, 95th/99th percentile, sample count, 250 ms limit, clock/tool accuracy, raw-result package, and no critical correctness failure. The threshold still requires stakeholder justification; precision does not create relevance.

### Example 2

All avionics tests pass, but the safety case references the prior software build. Configuration identity is blocking even if behavior seems unchanged. Impact analysis and updated evidence are required; schedule pressure cannot substitute for authority.

### Example 3

A receiver takes physical possession of equipment for storage before formal acceptance at destination. Transit damage, count, installation, and site checks remain open under the agreement. The acceptance record must distinguish custody, title/risk, and conformity decision rather than infer them from the loading dock.

### Example 4

A service meets monthly average response time while every Monday peak breaches the user-critical threshold. The acceptance criterion uses percentile/window and representative demand, not a provider-friendly aggregate. Service acceptance also needs measurement ownership, exclusions, credits/remedies, and monitoring.

### Example 5

A maintenance manual has two missing diagrams. Conditional acceptance may be appropriate only if safe operation/maintenance remains possible, authorized parties concur, interim controls exist, corrected pages have owner/date and review, payment/remedy is defined, and nonclosure has consequences. Calling it “minor” supplies none of those facts.

### Example 6

Software passes acceptance tests but the package lacks license notices, SBOM, deployment configuration, backup/restore instructions, and support escalation. The executable is not the entire tender. Artifact criteria reject or condition delivery according to criticality and governing terms.

### Example 7

A factory qualifies a design by extreme testing, then uses lot sampling for production acceptance. One destructive test cannot be applied to every shipped unit. Lot definition, process traceability, acceptance numbers, rejected-lot disposition, and unit-level workmanship checks determine what the sample supports.

### Example 8

A demonstration fails when the test environment loses power. Evidence shows the facility violated a documented entry condition, but the product's restart behavior also corrupts state. The run cannot be erased wholesale. Separate setup nonconformance from a genuine product anomaly, correct both, and rerun affected/regression criteria.

### Example 9

An urgent mission proposes accepting a nonconforming sensor. Technical analysis bounds accuracy loss for one use, operations restricts the envelope, safety concurs, authority approves a time-limited deviation, monitoring and replacement are scheduled, and remedy is recorded. The result remains nonconforming-with-authorized-disposition, not “passed.”

### Example 10

After acceptance, a latent vulnerability is discovered in a bundled dependency. The response depends on contract, warranty, security clauses, severity, exploitability, and operational risk. Acceptance history and SBOM/configuration evidence support impact and remedy; they do not predetermine legal responsibility.

## Cross-Program Connections

- **Platform engineering:** internal platform adoption gates need measurable capability, tenancy, security, operability, migration, support, documentation, and deprecation criteria.
- **API/service engineering:** contract/version behavior, SLO measurement, failure semantics, compatibility, observability, and support obligations become service acceptance evidence.
- **Data engineering:** schema plus semantic quality, lineage, reconciliation, privacy, migration, population coverage, and repeatable data-package identity shape acceptance.
- **Object-oriented/functional programming:** tests and types support conformance, while build provenance, effects, dependencies, documentation, deployment, and operational fitness remain.
- **Security:** authorization to operate, vulnerability handling, SBOM, secrets, incident reporting, residual-risk authority, and supply-chain provenance can be blocking gates.
- **Safety/reliability:** hazard controls, critical anomalies, reliability demonstrations, maintenance, spares, recovery, and noncompensatory thresholds govern transition risk.
- **Statistics:** sampling, producer/consumer risk, confidence, measurement uncertainty, percentiles, censoring, and aggregation determine quantitative decision strength.
- **Law/procurement:** authority, inspection, rejection, cure, title/risk, payment, warranties, remedies, and records depend on explicit governing terms.

## References

1. NASA, [SWE-034 — Acceptance Criteria, Software Engineering Handbook](https://swehb.nasa.gov/spaces/7150/pages/16450634/SWE-034%2B-%2BAcceptance%2BCriteria), accessed 2026-08-31.
2. NASA, [Product Transition, Systems Engineering Handbook section 5.5](https://www.nasa.gov/reference/5-5-product-transition/), accessed 2026-08-31.
3. NASA, [Product Validation, Systems Engineering Handbook section 5.4](https://www.nasa.gov/reference/5-4-product-validation/), accessed 2026-08-31.
4. NASA, [Systems Engineering Handbook Appendices, including V&V and acceptance-plan content](https://www.nasa.gov/reference/system-engineering-handbook-appendix/), accessed 2026-08-31.
5. NASA, [Technical Assessment, Systems Engineering Handbook section 6.7](https://www.nasa.gov/reference/6-7-technical-assessment/), accessed 2026-08-31.
6. NASA, [NPR 7123.1B, NASA Systems Engineering Processes and Requirements, Change 4](https://nodis3.gsfc.nasa.gov/displayAll.cfm?Internal_ID=N_PR_7123_001B_&page_name=ALL), effective 2020.
7. U.S. General Services Administration, [Federal Acquisition Regulation, Subpart 46.1 — General](https://www.acquisition.gov/far/subpart-46.1), FAC 2026-01.
8. U.S. General Services Administration, [Federal Acquisition Regulation, Subpart 46.5 — Acceptance](https://www.acquisition.gov/far/subpart-46.5), FAC 2026-01.
9. U.S. General Services Administration, [Federal Acquisition Regulation 46.407 — Nonconforming supplies or services](https://www.acquisition.gov/far/46.407), FAC 2026-01.
10. U.S. General Services Administration, [Federal Acquisition Regulation 46.703 — Criteria for use of warranties](https://www.acquisition.gov/far/46.703), FAC 2026-01.

## Exercises

### Exercise 1

Rewrite “the analytics service shall be accurate, fast, reliable, secure, and documented” as a decision-ready acceptance-criteria set with evidence, configuration, criticality, and authority.

### Exercise 2

A response-time criterion is 99th percentile no greater than 400 ms. A controlled run has 1,000 successful requests; after sorting ascending, observation 990 is 392 ms and observation 991 is 421 ms. The procedure defines nearest-rank percentile as rank $\lceil pn\rceil$. Decide the criterion and identify missing decision information.

### Exercise 3

Design conditional acceptance for a noncritical report missing two fields while all safety, security, core function, and transition gates pass. Include controls, correction, retest, remedy, and failure-to-cure.

### Exercise 4

An acceptance run used release candidate RC7, but the tender is production build P1 with a compiler upgrade and dependency patches. Decide what evidence can transfer and construct a delta-acceptance plan.

### Exercise 5

Construct an acceptance data package and decision record for a managed service transitioning from supplier operations to the customer's platform team.

## Answers to the Exercises

### Answer 1

Split the statement. Accuracy: define authoritative labeled/reconciled data, task/population classes, metric per class, exclusions, sample, threshold and uncertainty; critical classes are mandatory. Performance: define production build, topology, data volume, concurrency/query mix, client-to-result plane, warmup/window, successful/error treatment, percentile and limit. Reliability: define mission/service interval, availability/failure/recovery measures, planned exclusions, observation or demonstration model, confidence and incident evidence. Security: name required controls, threat scope, scan/penetration/assurance evidence, unresolved severity gates, authorization and vulnerability process. Documentation: enumerate approved as-built architecture, deployment, operations, backup/restore, security, API/data, maintenance and support documents and require successful representative use.

For each, add criterion ID, basis trace, rationale, criticality, exact build/configuration/dependencies/data/environment, procedure/tool version, raw evidence, reviewer/witness, allowed dispositions, and acceptance authority. Add cross-cutting gates for validation, configuration provenance, licensing/rights, SBOM, training, support/on-call, migration/rollback, monitoring and data package. “Secure” cannot be proven universally; criteria support a bounded decision against named obligations and residual-risk authority.

### Answer 2

Nearest-rank rank is $\lceil0.99\times1000\rceil=990$. Observation 990 is 392 ms, so the literal stated criterion passes because $392\le400$ ms. Observation 991 does not determine the prescribed 99th percentile, though the jump should be retained for distribution/tail review and may affect other criteria.

Missing information includes exact build/topology, request population and mix, load/concurrency, client/server measurement planes, clock accuracy, warmup, window, repetitions, errors/timeouts and excluded requests, caching, data size, network/environment, sampling independence, rounding, raw-data integrity, uncertainty/run-to-run variability, required confidence, and whether any class-specific or maximum threshold exists. A single nominal run can satisfy the literal rule without establishing production fitness. Do not change the percentile definition after observing the boundary.

### Answer 3

First confirm contract/policy permits conditional acceptance and that report fields are truly noncritical through technical, user, privacy, financial, legal, safety and security impact analysis. Record the criterion as conditional/nonconforming, not passed. Name affected reports/users/configurations and interim controls—for example a validated alternate source, visible limitation, restricted decisions, manual review and monitoring—with an owner.

Specify corrected schema/content, provider owner, due date, delivery format, documentation and consumer updates, verification and representative user acceptance test, regression for existing fields/export/API, and evidence package. Obtain technical/customer and any required authorities' concurrence. Define payment/price holdback or service credit if applicable, warranty/support effect, monitoring/escalation, and who may remove controls. Failure to cure by the date triggers rejection, suspension, reperformance, or other exact contractual remedy. Any expansion of impact revokes the conditional basis and returns to decision authority.

### Answer 4

RC7 evidence transfers only where P1 equivalence is established. Compare source commit, compiler/linker and flags, dependencies/SBOM, generated code, build environment, platform, configuration defaults, packaging/signing, migrations, tests, known anomalies and runtime behavior. Compiler/dependency changes can affect security, numerical behavior, timing, compatibility and faults even with unchanged source.

Retain requirements trace, test design, stable data/oracles, and unaffected evidence as reusable assets; do not relabel RC7 execution as P1 results. Reproduce P1 build provenance, static/security/license analysis, unit/integration/contract suites, targeted compiler/dependency regression, performance/timing/numerical comparisons, install/upgrade/rollback, data migration, operational smoke/end-to-end and affected validation scenarios. Investigate differences, update documentation/SBOM/authorization and rerun acceptance gates on the tendered environment. Authority approves the documented equivalence/delta rationale; if provenance is insufficient, execute the full prescribed suite.

### Answer 5

Package: governing acceptance basis and approved criteria; tender inventory and service scope; exact code/infrastructure/configuration/data/identity/network/region/dependency state; build/deployment provenance and SBOM/licenses/rights; verification, validation, security, privacy, resilience, performance and migration results; raw/derived evidence and tool versions; architecture/runbooks/SLOs/alerts/dashboards; backup/restore and continuity proof; incidents/problems/known errors; anomaly/waiver register; capacity/cost model; operator training and competency; on-call schedules/escalation/vendor contacts; access/key/certificate transfer; data retention/deletion; support/warranty/remedy; rollback and exit plan.

The decision record identifies supplier/customer, authorized accepter, date, sites/service increment, basis revisions, every criterion result, evidence references, deviations, unresolved conditions, residual risks and concurrences. It states operational authority, access and data custody, service/support start, monitoring and SLO measurement owner, payment effect, open correction owners/dates, remedies, warranty/latent-defect/security obligations, and reacceptance triggers. Conduct a shadow/on-call handover, incident and restore exercises, access verification, representative operations scenario and rollback rehearsal. Acceptance is bounded to the recorded service configuration and transition state; it does not erase supplier obligations or validate future changes.
