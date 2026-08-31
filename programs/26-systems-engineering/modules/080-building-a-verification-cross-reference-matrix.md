---
module_id: SYSENG-080
program: Systems Engineering
level: 2
module_number: 80
title: Building a Verification Cross-Reference Matrix
status: complete
last_verified: 2026-08-31
---

# Building a Verification Cross-Reference Matrix

## One-Page Review

### Governing question

How can a verification cross-reference matrix provide a complete, configuration-controlled, bidirectionally traceable map from every applicable requirement to an adequate verification strategy and from every closure decision to trustworthy, reviewable evidence?

### Essential definitions

- A **verification cross-reference matrix (VCRM)** is a controlled index connecting requirements to verification methods, levels, conditions, procedures, articles/configurations, results, anomalies, evidence, and approval. Organizations also use names such as requirements verification matrix (RVM), verification requirements matrix (VRM), verification compliance matrix/spreadsheet, or compliance matrix.
- A **verification row** is the governed record for one atomic verification obligation. One requirement can require multiple rows when modes, variants, allocations, criteria, or methods differ.
- **Vertical traceability** connects stakeholder/system requirements through lower-level requirements, design/implementation, verification, and evidence across hierarchy.
- **Horizontal traceability** connects peer/interface requirements, assumptions, shared obligations, configurations, and evidence across boundaries.
- A **verification method** states the evidence-producing approach—commonly analysis, inspection, demonstration, or test—with project-specific definitions. Method names alone do not define adequacy.
- **Verification level** identifies where in the product/system hierarchy evidence is produced and where compliance is concluded.
- An **evidence pointer** is a durable, versioned reference to a result/report/data set, not text such as “test passed.”
- **Closure authority** is the role empowered to approve the verification result, anomaly disposition, equivalence, or waiver under governance.
- **Applicability** states whether a requirement/obligation governs a product/configuration. “Not applicable” requires rationale and authority, not omission.
- A **coverage audit** checks completeness, uniqueness, valid relationships, evidence/configuration currency, status logic, and unresolved exceptions—not merely row count.

### Central model, mechanism, or theorem

Model the VCRM as a typed trace graph rather than a flat checklist. For requirement set $R$, verification activities $V$, evidence artifacts $E$, configurations $C$, anomalies $A$, and authorities $U$, closure of requirement $r$ is admissible only if

\[
\operatorname{close}(r) \Rightarrow
\operatorname{applicable}(r)\land
\operatorname{atomic}(r)\land
\operatorname{adequatePlan}(r,V)\land
\operatorname{executed}(V,C)\land
\operatorname{supports}(E,r,V,C)\land
\operatorname{resolved}(A)\land
\operatorname{approved}(U).
\]

Rows are projections of this graph. A green status is valid only when underlying nodes and edges exist, agree on exact baselines/configurations, and satisfy closure rules.

### Critical invariants

- Reconcile the matrix against the authoritative requirement baseline; every applicable atomic “shall” or governed obligation has trace, and every row names its source/revision.
- Requirement identifiers are stable and unique; text changes, splits, merges, moves, deletions, and supersession preserve history and impact.
- Applicability and tailoring are explicit, justified, approved, scoped, and versioned.
- Each row records verification objective/criterion, method, level, article, configuration, environment, procedure/model, responsible owner, planned event, and dependencies before execution.
- Methods are chosen by evidence need; “test” or “analysis” is not an adequate strategy without conditions, outputs, uncertainty, and acceptance logic.
- Evidence pointers resolve to immutable or controlled artifacts with provenance, raw/derived relationship, tool/data versions, result, and limitations.
- Planned, ready, executed, passed, failed, blocked, waived, not applicable, and closed are distinct states with controlled transitions.
- A pass cannot close a row when the evidence applies to a different requirement revision, product build, article, environment, or procedure.
- Anomalies, deviations, waivers, limitations, partial coverage, and retest/regression remain linked and visible.
- Parent closure is derived from justified child/allocation/interface evidence plus system-level integration as required; it is not copied upward automatically.
- One evidence artifact can support multiple requirements only with explicit applicability and independent criterion evaluation; shared evidence is not shared status.
- Matrix health is audited for missing, orphaned, duplicate, stale, contradictory, circular, and compensating traces throughout change.

### Common failures

Common failures include one spreadsheet row per paragraph; copied requirement text without source revision; blank rows assumed not applicable; method letters without procedures; unresolved fields persisting to closure; evidence links to mutable folders; green status from a different build; requirement changes without stale flags; parent pass copied from children; interface requirements owned by neither side; one test report closing many requirements without criterion mapping; waivers hidden in notes; test failures overwritten by reruns; row counts used as coverage; filters hiding open items; formula/manual-status drift; and a beautiful matrix that cannot reconstruct any result.

### Compact example

A synthetic matrix has four requirement rows. Three contain evidence, but one evidence package belongs to build 1.9 rather than current build 2.0; the fourth is still planned. Only two closures are admissible, so the matrix is incomplete despite three displayed passes. After current-build evidence is linked for the stale row and the planned row is executed, all four satisfy the declared synthetic rules. This checks metadata consistency only, not technical adequacy.

### Connections

Requirements engineering, architecture/allocation, interface control, verification planning, test/analysis, validation, anomaly resolution, acceptance, configuration management, data governance, model-based systems engineering, assurance cases, reviews, change control, CI, and audit all rely on trustworthy verification cross-references.

## Governing Question

Can a reviewer start from any applicable requirement and reach the exact adequate evidence and closure authority—and start from any evidence artifact or anomaly and identify every requirement, configuration, and decision it affects—without relying on tribal knowledge?

A matrix earns value through relationships, not cells. A requirement identifier next to “Test / Pass” says little: it omits what was tested, at which level, using which article/build, under what conditions, against what criterion, with which procedure and data, whether anomalies remain, and who approved closure. The matrix must expose the assurance chain while keeping large artifacts outside the table.

## Why This Matters

NASA's Requirements Verification Matrix appendix says each “shall” should have a unique identifier and definitive source, with an approach for how all requirements are verified. Product Verification guidance calls for results in a compliance/verification matrix or equivalent to trace compliance for each product requirement. The V&V plan outline allows the matrix to reside in a requirements system with pointers, reinforcing that the durable information model matters more than a particular document format.

The VCRM also coordinates future work. Early rows reveal unverifiable requirements, scarce facilities, inappropriate levels, missing instrumentation, destructive articles, model-credibility needs, interface dependencies, and schedule conflicts. Late rows summarize completion only because the planning and evidence relationships were maintained continuously.

Weak matrices create false closure. Counts can show 100% when excluded requirements were silently filtered, copied parent status double-counts evidence, or a pass applies to a retired build. Conversely, overly dense tables become unreadable. The durable design separates authoritative entities—requirements, activities, configurations, artifacts, anomalies, decisions—then renders role-specific views.

## Prerequisites and Retrieval

Before baselining or auditing a VCRM, retrieve:

1. authoritative requirement sources and revisions, unique IDs, text, rationale, owners, priorities/criticality, applicability, modes/states, verification success criteria, parent/child/allocation/interface/derived traces, and approved tailoring;
2. product breakdown, system architecture, interfaces, variants/options, sites, lifecycle phases, models, software/hardware/data/human elements, suppliers, and verification levels;
3. verification policy and method definitions, independence/authority, risk classification, qualification/acceptance strategy, reuse/similarity rules, model/simulation credibility, statistical and uncertainty standards;
4. verification objective and pass/fail criterion for every row, including units, tolerances, boundaries, populations, sample/statistic, measurement plane, environment, modes, repetitions, uncertainty, and forbidden outcomes;
5. planned methods/activities, procedure/report/model IDs and revisions, articles/serials/builds/configurations, facilities, environments, tools/instruments/calibration, data, responsible owners, witnesses/reviewers, events, and dependencies;
6. execution evidence: raw data, logs, observations, calculations, analysis notebooks/reports, inspection records, demonstrations, test reports, hashes/provenance, dates, results, limitations, and reproducibility instructions;
7. anomalies, failures, deviations, waivers, exceptions, corrective actions, retests, regression, residual risks, approvals, and open/closure state;
8. configuration baselines and change history for requirements, product, procedures, models, tools, data, facilities, interfaces, and evidence packages;
9. status/state-machine definitions, allowed transitions, required fields/gates, closure roles, electronic signatures/records, audit history, access controls, and retention;
10. lifecycle/review needs: planned-versus-complete views, critical/open items, facility and article demand, supplier delivery, readiness gates, acceptance/certification packages, and operational re-verification;
11. import/export/API/schema definitions, identifiers, relationship cardinalities, generated views, formulas/queries, validation rules, backups, migration, and source-of-truth ownership;
12. prior audits and reconciliation reports for missing/orphaned/duplicate/stale/contradictory rows, unresolved links, dead evidence pointers, inconsistent statuses, and unauthorized manual edits.

Perform a **two-way walk**. Sample requirements by criticality and follow each forward to closure evidence. Sample evidence reports, anomalies, changes, and waivers independently and walk backward to all affected rows. Forward-only audits miss orphan evidence and untraced failures.

## Learning Objectives

After completing this module, you should be able to:

1. define the VCRM as a typed, configuration-controlled trace/evidence model;
2. derive one or more verification obligations from atomic requirements, modes, variants, allocations, and criteria;
3. select methods and levels based on evidence adequacy and risk;
4. design fields for planning, execution, evidence, anomaly, approval, and lifecycle use;
5. distinguish applicability, plan readiness, execution result, anomaly disposition, waiver, and closure;
6. bind every result to exact requirement/product/procedure/tool/data/environment baselines;
7. model many-to-many requirement/activity/evidence relationships without status copying;
8. automate schema, referential-integrity, stale-link, status-transition, and coverage audits;
9. generate concise review dashboards without hiding authoritative detail or open risk;
10. migrate and govern spreadsheet, repository, database, and model-backed matrices durably.

## Core Exposition

**Start with purpose and authority.** Define which baselines and decisions the matrix supports: planning, design review, qualification, requirement closure, acceptance, certification, operations, or all with scoped views. Name source-of-truth systems, custodians, approvers, update cadence, and conflict resolution.

**Reconcile the requirement population.** Import or reference exact requirement IDs/source revisions. Check unique IDs, atomicity, binding language, applicability, modes/variants, duplicates, conflicts, parent/child/allocation/interface traces, and unverifiable wording. Do not “fix” requirement text inside the matrix; route controlled changes to the requirement baseline.

**Choose row granularity intentionally.** One requirement may map to several criteria or activities: normal and degraded modes, hardware variants, sites, qualification and acceptance, inspection plus test, or component plus integrated verification. Give each obligation a stable row ID and relate it to the same requirement. Conversely, one activity can serve multiple rows if each criterion is evaluated separately.

**Record source and applicability.** Store source document/model ID and revision, requirement ID/text checksum or authoritative link, product applicability, lifecycle/mode/variant, tailoring rationale, approving authority, and effective dates. A missing row and an approved not-applicable row are different states.

**Define the verification objective.** Translate requirement into observable proposition without silently changing it. Record what evidence would establish conformance, including units, ranges, tolerance, sample/statistic, uncertainty, boundaries, adverse conditions, measurement plane, duration, and expected output. If this cannot be written, return to requirement clarification.

**Select method and level.** Analysis can establish properties not directly testable, inspection confirms attributes, demonstration shows observable operation, and test measures response under controlled stimuli; organizational definitions govern. Combinations are common. Choose the lowest level with observable property and adequate fidelity, then add higher-level integration/interface evidence where emergence matters.

**Plan the evidence producer.** Link procedure/model/report plan; exact article class and intended serial/build; environment/facility; instruments/tools/data and calibration/credibility; owner; independent witness/reviewer; predecessor dependencies; planned event; and reuse/similarity basis. Track readiness separately from completion.

**Use explicit states.** A useful state machine can include proposed, planned, plan-approved, ready, executed-pass, executed-fail, analysis-pending, blocked, disposition-pending, waiver-approved, closure-approved, superseded, and not-applicable-approved. Define transitions and required fields. A pass is an observation; closure is an authority decision after anomalies/configuration are resolved.

**Link evidence rather than embed it.** Store durable artifact ID/version/hash, repository/location, producing activity, configuration, raw-data lineage, tools/data, date, result, reviewer, limitations, and retention. Links must be resolvable by authorized future reviewers. Avoid mutable “latest/report.pdf” paths.

**Bind configuration on both sides.** Compare requirement revision and applicability with the configuration verified. Evidence metadata identifies software commit/build, hardware serial/lot/revision, firmware, data/model/tool versions, flags, infrastructure, interfaces, environment, and procedure. Change impact marks affected closures stale until justified or reverified.

**Model anomalies as first-class relations.** Link every discrepancy/failure to affected activity, row, requirement, configuration, evidence, corrective action, waiver and rerun. Preserve failed evidence. A later pass does not remove the anomaly; closure logic checks disposition and regression.

**Handle similarity and reuse explicitly.** Record source product/configuration, target, commonality/differences, validity domain, analysis, risk, authority, and restrictions. “Same design” is not a method. Evidence reuse may close several rows only where each requirement's criterion is supported.

**Derive hierarchical closure carefully.** Child evidence can support allocated portions, but system requirements may concern end-to-end performance, interaction, shared resources, emergent safety, or intended context. Define roll-up rules and required integrated activities. Never set a parent green solely because all children are green unless the allocation is demonstrably complete and composition preserves the property.

**Automate integrity, not judgment.** Validate schema, required fields, identifier uniqueness, referential integrity, legal states/transitions, coverage, dead links, configuration mismatch, stale dates/digests, orphan evidence/anomalies, duplicate rows, and closure gates. Automation can detect missing metadata; it cannot decide whether a test genuinely verifies a complex requirement.

**Build review views from authoritative data.** Provide totals by requirement source/product/level/method/status/criticality; open critical rows; upcoming events; facility/article demand; failed/anomaly/waiver lists; stale evidence; change impact; and closure burn-up. Always expose denominators and filters. Keep authoritative IDs and drill-down links.

**Audit semantic quality.** Sample rows for criterion adequacy, method/level fit, environment, article fidelity, uncertainty, evidence content, anomaly resolution, independence, and conclusion scope. A 100%-complete schema can contain weak engineering.

**Audit negative space.** Compare the matrix with requirements sources, architecture, interface inventories, hazard controls, change records, anomaly systems, test catalogs, and evidence repositories. Items found outside the matrix can reveal omitted obligations, orphan evidence, unpropagated changes, or failures hidden by an apparently complete denominator.

**Govern change continuously.** When requirements, architecture, interfaces, product, procedures, models, tools, data, environments, or evidence change, compute affected rows and owners. Record rationale and approval for “no impact.” Rebaseline views while preserving prior snapshots and decision history.

**Scale the implementation.** A small controlled spreadsheet can work with stable IDs, protected schema, validation, review, and version control. Larger programs benefit from requirement/configuration/test/data systems or graph/model repositories. Export human-readable snapshots for reviews; do not create competing hand-edited sources.

The following fixture demonstrates metadata closure gates for four rows.

<!-- bijux-verify: {"id":"verification-matrix-integrity-fixture","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"requirements=4\nmatrix_rows=4\nunique_requirement_ids=4\nrequirements_with_methods=4\nrequirements_with_evidence=3\nconfiguration_current=3\nadmissible_closures=2\nopen_or_invalid_rows=R-003,R-004\ninitial_matrix_decision=incomplete\nafter_correction_admissible_closures=4\nafter_correction_matrix_decision=complete_for_declared_metadata_rules\nstatus=declared_matrix_fixture_consistent\nevidence=synthetic_metadata_only\n","stderr":""}} -->
```python
current_build = "2.0"
rows = {
    "R-001": {"method": "test", "evidence": "EV-101", "build": "2.0", "anomaly": "closed"},
    "R-002": {"method": "inspection", "evidence": "EV-102", "build": "2.0", "anomaly": "closed"},
    "R-003": {"method": "analysis", "evidence": "EV-103", "build": "1.9", "anomaly": "closed"},
    "R-004": {"method": "demonstration", "evidence": None, "build": "2.0", "anomaly": "closed"},
}

def closable(row):
    return bool(row["method"] and row["evidence"] and row["build"] == current_build and row["anomaly"] == "closed")

invalid = [requirement_id for requirement_id, row in rows.items() if not closable(row)]
print(f"requirements={len(rows)}")
print(f"matrix_rows={len(rows)}")
print(f"unique_requirement_ids={len(set(rows))}")
print(f"requirements_with_methods={sum(bool(row['method']) for row in rows.values())}")
print(f"requirements_with_evidence={sum(bool(row['evidence']) for row in rows.values())}")
print(f"configuration_current={sum(row['build'] == current_build for row in rows.values())}")
print(f"admissible_closures={sum(closable(row) for row in rows.values())}")
print("open_or_invalid_rows=" + ",".join(invalid))
print("initial_matrix_decision=incomplete")

rows["R-003"]["build"] = "2.0"
rows["R-004"]["evidence"] = "EV-104"
print(f"after_correction_admissible_closures={sum(closable(row) for row in rows.values())}")
print("after_correction_matrix_decision=complete_for_declared_metadata_rules")
print("status=declared_matrix_fixture_consistent")
print("evidence=synthetic_metadata_only")
```

The fixture checks only method presence, evidence presence, one build string, and anomaly state. It cannot assess requirement completeness, method adequacy, evidence truth, configuration equivalence, anomaly quality, authority, or actual compliance.

## Definitions and Notation

Let graph $G_v=(N,L)$ contain typed nodes for requirements $R$, activities $V$, evidence $E$, configurations $C$, anomalies $A$, waivers $W$, and authorities $U$. Typed links include verifies, produces, applies-to, executed-on, depends-on, affected-by, supersedes, disposes, and approves.

For requirement $r$, coverage $\Gamma(r)$ is the set of verification obligations across criteria, modes, variants, levels, and lifecycle. Completeness requires every applicable element of $\Gamma(r)$ to have an adequate planned and ultimately closed path; raw row count is not coverage.

Define currency predicate $Q(e,r,c)$ that checks evidence $e$ applies to requirement revision and configuration $c$ under approved equivalence/change impact. Closure status is derived from valid relations and authority, not an independently editable color.

## Mechanisms, Invariants, or Proof Structure

A defensible VCRM construction and closure argument follows this chain:

1. govern source systems, baselines, identifiers, responsibilities, decisions, schema, and history;
2. reconcile all applicable atomic requirements and their hierarchy/interface/allocation traces;
3. derive stable verification obligations by criterion, mode, variant, level, and lifecycle;
4. define observable success criteria and select adequate methods/levels;
5. plan activities, articles/configurations, environments, procedures/models, tools/data, owners, independence, and dependencies;
6. execute under control and link immutable/provenanced evidence, results, limitations, and anomalies;
7. verify configuration currency, disposition, regression, reuse/similarity, and authority before closure;
8. audit forward/backward coverage, integrity, semantics, change impact, and dashboards;
9. preserve snapshots, decisions, and stale/superseded history through change and operations.

The invariants are authoritative reconciliation, stable identity, explicit applicability, observable criteria, adequate method/level, exact configuration, durable evidence, anomaly visibility, derived status, bidirectional trace, authorized closure, and change currency.

## Alternatives and Trade-Offs

**Spreadsheet versus database/model.** Spreadsheets are accessible and flexible; databases/models enforce relationships, concurrency, workflows, and scale. Governance and export/import integrity matter more than tool prestige.

**One row per requirement versus per obligation.** One row is compact but hides modes/methods/variants. Obligation rows express coverage but need stable relationship IDs and roll-up views.

**Embedded evidence versus links.** Embedding creates self-contained snapshots but duplication/staleness. Controlled links preserve authoritative artifacts; package immutable review snapshots where longevity/access requires.

**Manual status versus derived status.** Manual status handles judgment but drifts. Derive mechanical gates and reserve explicit authority decisions for semantics/exceptions.

**Central matrix versus federated ownership.** Central governance improves consistency; federated teams own domain detail. Use common schema/IDs, interface ownership, automated reconciliation, and clear authority.

**Strict closure gates versus risk-based tailoring.** Strict gates prevent false green; tailoring handles consequence and cost. Make risk classification and approval explicit, never silent omission.

**Full evidence duplication versus reusable activities.** Reuse saves effort but creates coupling and change impact. Evaluate each criterion independently and track shared evidence dependencies.

**Document snapshot versus live system.** Snapshots support reviews and records; live systems support current planning. Record source query/filter/baseline/time so the snapshot is reproducible.

## Failure Modes and Misconceptions

**“One row per shall is complete.”** Requirements can need several obligations, and non-requirement obligations can govern acceptance/certification separately.

**“Method=T is a plan.”** It omits objective, conditions, level, article, procedure, data, criteria, and evidence.

**“Pass means closed.”** Configuration, anomalies, limitations, regression, and authority remain.

**“A link proves evidence.”** It may be mutable, dead, inaccessible, wrong-build, or semantically irrelevant.

**“All child requirements passed.”** Allocation may be incomplete and system interaction/emergence unverified.

**“One report closes twenty rows.”** Only explicit criterion-to-result mappings support each row.

**“Not in the matrix means not applicable.”** Omission is indistinguishable from a gap; record rationale and approval.

**“100% complete is meaningful.”** Denominator, filters, criticality, stale evidence, waivers, and semantic adequacy determine meaning.

**“Automation guarantees correctness.”** It enforces declared rules, not engineering adequacy or evidence truth.

**“The matrix is final after verification.”** Operational changes, anomalies, upgrades, and reuse can reopen or stale closures.

## Worked Examples

### Example 1

A requirement specifies response under nominal and degraded network modes. One test row with nominal evidence cannot close both. Two obligations share the requirement but define distinct conditions, criteria, procedures and results; roll-up requires both plus any interaction coverage.

### Example 2

A test report links to 15 requirements but reports only one aggregate “system passed.” The matrix is not evidence-complete. Add named test cases/results and criterion mappings, or restrict credit to the proposition actually demonstrated.

### Example 3

A thermal analysis supports flight configuration 3.1, then material and geometry change. Automated dependency links mark affected rows stale. Engineering impact can justify unaffected rows or require rerun; unchanged green cells are not acceptable change analysis.

### Example 4

An interface timing requirement appears in both supplier matrices with different clocks and percentiles. Horizontal reconciliation establishes one authoritative semantic contract, paired responsibilities and integrated evidence. Two local passes cannot compensate for incompatible criteria.

### Example 5

A requirement is “not applicable” to an uncrewed variant. The row records variant scope, rationale, architecture evidence and approval. When a later variant adds remote human intervention, applicability impact reopens the decision.

### Example 6

Four child component requirements pass, but a parent requires end-to-end latency. Summing worst-case budgets is an analysis row; integrated timing test supplies complementary evidence. Parent closure depends on complete allocation and composition, not copied child colors.

### Example 7

A qualification test on one hardware unit supports a production family. The matrix records article pedigree, lot/design equivalence, qualification envelope, unit/lot acceptance strategy, deviations and authority. It does not duplicate the qualification pass onto every serial without the production-conformance argument.

### Example 8

A software row passes, fails after a dependency update, then passes after correction. All three executions and anomaly remain linked. Closure points to the current-build pass, correction/regression and disposition while historical evidence supports trend and audit.

### Example 9

A spreadsheet dashboard shows 98% because 200 open rows are filtered out as “future.” A reproducible view exposes baseline, denominator, lifecycle cutoff and excluded states. Percent complete becomes a planning metric, not a compliance claim.

### Example 10

A model-based repository generates the review matrix. A hand-edited PDF marks a waiver closed but the source model does not. Governance declares the model authoritative, rejects the manual divergence, applies approved waiver data upstream and regenerates a signed snapshot.

## Cross-Program Connections

- **Platform engineering:** capability requirements map to automated checks, performance/resilience exercises, security evidence, operational readiness and adoption outcomes across versions.
- **API/service engineering:** interface contracts, consumer/provider tests, version pairs, load/failure cases, traces and SLO evidence require horizontal configuration-bound rows.
- **Data engineering:** lineage, schema/quality checks, population/time windows, reconciliation and evidence reproducibility make data verification traceable.
- **Object-oriented/functional programming:** types, contracts, properties, unit/integration tests and proofs can be evidence nodes but need requirement/configuration/result mappings.
- **Security/safety:** controls, hazards, threats, assurance cases, independent authority, waivers and residual risk impose noncompensatory closure paths.
- **Configuration/data management:** baselines, identifiers, provenance, hashes, access, retention, changes and reproducible views keep the matrix truthful.
- **Graph/data modeling:** many-to-many typed relations, constraints, queries and derived views prevent flat-table duplication from becoming the conceptual model.
- **CI/CD:** automation can update execution evidence and stale status while approval, adequacy, risk and applicability remain governed decisions.

## References

1. NASA, [Appendix D: Requirements Verification Matrix](https://www.nasa.gov/reference/appendix-d-requirements-verification-matrix/), accessed 2026-08-31.
2. NASA, [Appendix I: Verification and Validation Plan Outline](https://www.nasa.gov/reference/appendix-i-verification-and-validation-plan-outline/), accessed 2026-08-31.
3. NASA, [Product Verification, Systems Engineering Handbook section 5.3](https://www.nasa.gov/reference/5-3-product-verification/), accessed 2026-08-31.
4. NASA, [Requirements Management, Systems Engineering Handbook section 6.2](https://www.nasa.gov/reference/6-2-requirements-management/), accessed 2026-08-31.
5. NASA, [Configuration Management, Systems Engineering Handbook section 6.5](https://www.nasa.gov/reference/6-5-configuration-management/), accessed 2026-08-31.
6. NASA, [Technical Data Management, Systems Engineering Handbook section 6.6](https://www.nasa.gov/reference/6-6-technical-data-management/), accessed 2026-08-31.
7. NASA, [Technical Assessment, Systems Engineering Handbook section 6.7](https://www.nasa.gov/reference/6-7-technical-assessment/), accessed 2026-08-31.
8. NASA, [Appendix C: How to Write a Good Requirement](https://www.nasa.gov/reference/appendix-c-how-to-write-a-good-requirement/), accessed 2026-08-31.
9. NASA, [NASA-HDBK-1009A, Systems Modeling Handbook for Systems Engineering](https://standards.nasa.gov/system/files/tmp/2025-03-12-NASA-HDBK-1009A.pdf), 2025.
10. NASA, [NPR 7123.1B, NASA Systems Engineering Processes and Requirements, Change 4](https://nodis3.gsfc.nasa.gov/displayAll.cfm?Internal_ID=N_PR_7123_001B_&page_name=ALL), effective 2020.

## Exercises

### Exercise 1

Design the schema and closure rule for a VCRM supporting hardware, software, data and human-in-the-loop requirements across two product variants.

### Exercise 2

A baseline contains 240 applicable requirements. The matrix has 238 unique requirement IDs, 245 rows because some requirements have multiple obligations, 220 rows marked passed, 8 failed, 10 planned, 5 passed rows with stale configurations, and 3 failed rows with approved waivers. Calculate useful counts and explain why no single completion percentage is sufficient.

### Exercise 3

A performance test report is proposed to close twelve requirements. Define the evidence mapping and audit needed to accept or limit reuse.

### Exercise 4

A requirement and software build both change after closure. Construct automated stale-impact rules plus the engineering review needed for reclosure.

### Exercise 5

Migrate a heavily formatted spreadsheet VCRM into a repository/database-backed authoritative model without losing history, authority, or review usability.

## Answers to the Exercises

### Answer 1

Use entities for Requirement, VerificationObligation, Activity, Criterion, ProductVariant/Configuration, Article, Environment, Procedure/Model, Tool/Instrument/Data, EvidenceArtifact, Execution, Anomaly, Action, Waiver, Review/Approval and Change. Stable IDs and typed relations cover source/revision, parent/child/allocation/interface, applies-to, verified-by, executed-on, produces, supports, affected-by, disposes, supersedes and approves. Avoid embedding variant lists or comma-separated evidence IDs.

One requirement can yield obligations per variant, mode, criterion and level. Shared obligations explicitly list applicability. Required fields include observable criterion, method/level, owner, planned activity, configuration, environment, evidence, result, anomaly state, reviewer and authority. Hardware rows capture serial/lot/article pedigree and calibration; software captures commit/build/dependencies/config; data captures schema/population/time/lineage; HITL captures participant/task/environment/training and protected evidence.

Closure is derived only when requirement/applicability is current, every mandatory obligation has approved plan and qualifying execution, evidence provenance/configuration matches, result passes or authorized disposition is linked, anomalies/actions/regression are closed, limitations fit the claim, and named authority approves. Parent/system closure additionally checks allocation completeness and integrated properties. Variant A never inherits Variant B status without approved equivalence.

### Answer 2

There are at least two missing applicable requirement IDs because $240-238=2$. The 245 rows are obligations, not the requirement denominator. Row states total $220+8+10=238$, so seven of 245 rows have an unreported or inconsistent state unless categories overlap or data definitions differ. Five displayed passes are stale, leaving at most 215 current passed rows before other closure gates. Three failed rows have waivers; they remain failed-with-authorized-disposition, not empirical passes.

A naive row-pass percentage is $220/245\approx89.80\%$; current displayed passes would be $215/245\approx87.76\%$. Neither measures requirement closure because some requirements have multiple obligations, two requirements are missing, seven row states are unexplained, stale evidence is invalid, waived failures require roll-up rules, and criticality/anomalies/authority are unknown. Report separate reconciled requirement coverage, obligation planning/execution/current-pass/fail/waiver/closure, missing/inconsistent records, and critical open items with explicit denominators/filters.

### Answer 3

For each of the twelve requirements, identify exact revision/text, applicability and atomic criterion; map it to named report section, test case, stimulus, measurement plane, raw data and result. Confirm the test configuration/article/build/environment and procedure match each row, the workload/sample/statistic/tolerance/uncertainty and boundary conditions support its proposition, and failure/error handling is visible. One aggregate performance number may support only one shared proposition.

Audit report provenance, raw-data lineage, instruments/clocks/tools, calibration, exclusions, calculations, independent review, anomalies and limitations. Check that requirements are not duplicates whose counts exaggerate evidence and that shared setup creates correlated rather than independent evidence. Link one execution/report to many obligations through explicit criterion-result records; do not copy a generic pass. Limit reuse where a requirement needs different variant, mode, level, percentile, duration, interface or operational condition, and create additional activities. Future report/configuration changes mark every dependent row for impact.

### Answer 4

Automation compares requirement revision/text digest/applicability/criterion and product configuration dependencies. A requirement text or criterion change marks its obligations plan/evidence/closure stale. A software build/dependency/config/schema/interface change marks executions/evidence on the prior configuration stale for all linked rows. Propagate through parent, shared evidence, interface and assurance-case relations; notify owners; prohibit closure roll-up; preserve prior state. A changed ID with unchanged semantics still needs controlled supersession/equivalence, not string matching alone.

Engineering classifies each change and interaction: what behavior/assumption moved, affected requirements/hazards/interfaces/data/modes, whether old procedures/oracles remain valid, evidence sensitivity, regression and operational consequences. Outcomes are approved no-impact with rationale, analysis/similarity credit, targeted re-verification/regression, or broader reopen. Execute on exact new baseline, resolve anomalies, update documents/models and obtain closure authority. Automation finds declared dependencies; semantic review finds missing ones.

### Answer 5

Inventory sheets, formulas, macros, hidden rows/columns, filters, comments, links, attachments, status colors, identifiers, authorities and historical snapshots. Declare the target source of truth and schema; map fields to normalized entities/relations and controlled vocabularies. Assign stable IDs, preserve legacy IDs, source cell/snapshot provenance, timestamps, authors/approvals, failed/superseded results and attachments. Do not import green fill as closure without reconstructing gates.

Clean and reconcile in staged reports: requirement baseline coverage, duplicates, many-to-many relationships, applicability, methods, states, evidence links, anomalies, configurations and authorities. Quarantine ambiguous records for owner decisions. Validate referential integrity, counts by original views, sampled two-way trace, hashes/files, state transitions and regenerated dashboards. Run old and new systems in controlled parallel for a bounded period, freeze legacy edits at cutover, archive signed/readable snapshots, and document rollback.

Provide role-specific generated tables/dashboard exports with stable URLs/IDs and review baselines so usability is not lost. Train owners, establish change workflow, access/retention/backups, schema/API tests, audit cadence and migration acceptance criteria. Retire the spreadsheet as authoritative only after approved reconciliation; retain it as a historical record, not a competing editable source.
