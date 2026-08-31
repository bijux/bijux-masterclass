---
module_id: SYSENG-083
program: Systems Engineering
level: 2
module_number: 83
title: Configuration Identification and Control
status: complete
last_verified: 2026-08-31
---

# Configuration Identification and Control

## One-Page Review

### Governing question

Can the organization uniquely identify what the system is, what defines it, which versions and relationships apply at a stated time and place, and ensure that every authorized change reaches the intended products, information, evidence, and operational instances without unintended divergence?

### Essential definitions

- **Configuration** is the functional and physical characteristics of a product/system and the controlled information that defines, realizes, operates, supports, verifies, and records those characteristics at a point in time.
- A **configuration item (CI)** is a product or aggregation selected for configuration-management attention and treated as a unit for identification, control, status accounting, and verification. Granularity is risk- and decision-dependent.
- **Configuration identification** selects CIs and defines their identifiers, structure, versions, interfaces, product information, baseline relationships, effectivity/applicability, and authoritative representations.
- **Configuration control/change management** evaluates, authorizes, implements, verifies, records, and communicates changes to controlled configurations and their defining information.
- A **configuration baseline** is a formally reviewed/agreed configuration definition at a stated time that thereafter changes only through the applicable control process.
- **Effectivity** states when/where/to which serials, lots, versions, sites, users, modes, contracts, or date ranges a configuration/change applies.
- **As-designed**, **as-built**, **as-tested**, **as-delivered**, **as-deployed**, **as-operated**, **as-maintained**, and **as-retired** configurations are distinct views that must be reconciled, not assumed equal.
- A **bill of materials/product structure** records constituent items and relationships; software/infrastructure/data systems need analogous dependency, image, package, schema, model, policy, and deployment manifests.
- **Configuration status accounting (CSA)** records and reports configuration identifiers, baselines, change state, effectivity, implementation, deviations, waivers, audits, and actual-instance status.
- **Configuration verification/audit** checks that product and defining information agree and that required functional/physical attributes and approved changes are correctly realized.

### Central model, mechanism, or theorem

Represent a configuration at time $t$ as a versioned typed graph

$$
C_t=(N_t,L_t,B_t,E_t,P_t),
$$

where nodes $N$ are CIs/configuration records, links $L$ define composition/interfaces/dependencies, $B$ identifies governing baselines, $E$ effectivity, and $P$ provenance/status. A change $\Delta$ is controlled only if the authorized transition

$$
C_t \xrightarrow[\alpha,\,I,\,V]{\Delta} C_{t+1}
$$

records authority $\alpha$, impact $I$, verified implementation $V$, and actual effectivity. Updating a document, repository, part, database, or running service alone does not prove the configuration transition is complete.

### Critical invariants

- Define the decisions and risks configuration information must support before selecting CIs or tools.
- Every CI and controlled record has stable identity, owner, type, lifecycle state, revision/version, provenance, authoritative source, relationships, effectivity, and retention.
- Identification covers end and enabling products: requirements, models, drawings, code, binaries/images, dependencies, data/schema, infrastructure, procedures, tools, facilities, test assets, training, spares, suppliers, and retirement records as applicable.
- Naming/version schemes distinguish identity, revision, variant, instance, lot/serial, environment, build, release, deployment, and state; labels are not overloaded.
- Interfaces and shared items have multi-party ownership, precedence, compatibility, and change authority.
- Proposed changes preserve original baseline and record need, scope, alternatives, impact, urgency, risk, security/safety, verification/validation, transition, rollback, and retirement consequences.
- Only authorized roles approve changes at the correct technical/contractual/operational authority; emergency paths remain bounded, recorded, reviewed, and reconciled.
- Implementation is traced across every affected configuration item, instance, document/model, supplier, site, evidence package, training/procedure, and support product.
- Build/deployment provenance is reproducible or sufficiently attested; mutable tags and directory names cannot be sole identity.
- As-designed/built/tested/delivered/deployed/maintained states are reconciled; known deviations/waivers remain explicit.
- Status accounting can answer what should be, what is, what changed, why, who approved, where implemented, what evidence applies, and what remains open.
- Monitoring/audits detect unauthorized, undocumented, incomplete, misapplied, stale, counterfeit, or drifted configurations and trigger disposition.

### Common failures

Common failures include controlling documents but not products; one version number for incompatible variants; part numbers unchanged after material/process change; “latest” links and mutable tags; code revision without compiler/dependency/config/data identity; infrastructure declared from source but not observed; databases excluded from release configuration; spreadsheets/macros/models outside control; interface changes approved by one party; emergency fixes never reconciled; change boards approving without impact/evidence; tickets closed when only one site updated; as-built records reconstructed after failure; serial/lot effectivity missing; field repairs undocumented; supplier substitutions hidden; and audits that compare two stale documents rather than product to authoritative definition.

### Compact example

A synthetic release manifest identifies eight configuration dimensions: application, dependencies, container image, infrastructure, data schema, policy, runbook, and test-evidence package. The observed deployment matches seven but uses an older schema, so authorization is rejected despite a complete manifest and matching release label. After the schema is brought to the authorized version, all eight match under the fixture's exact-string rules. Real configuration assurance needs stronger provenance, semantics, observation, and authority.

### Connections

Requirements, architecture, interfaces, technical data, build/release, supply chain, manufacturing, verification/validation, safety/security, operations, incident response, maintenance, audit, baselines, change impact, traceability, provenance, and retirement all depend on configuration identification and control.

## Governing Question

Can an authorized person or automated control reconstruct the exact system and defining information for any consequential decision or event, compare intended with actual configuration, and prove that changes were evaluated and realized across their full effectivity?

Configuration management prevents identity ambiguity from becoming technical risk. A test can pass the wrong build. A correct drawing can describe the wrong serial. A signed container image can run with an unrecorded database migration. A replacement part can share a number while its manufacturing process changed. Without stable identifiers and relationships, impact analysis, evidence reuse, incident diagnosis, rollback, and retirement become guesswork.

## Why This Matters

NASA Configuration Management guidance identifies planning, configuration identification, change management, status accounting, and configuration verification as interconnected functions across the product lifecycle. Its CM plan outline includes baselines, CIs, control boards, nomenclature, hardware/software identification, audits, data, interfaces, phasing, and supplier control. NASA software guidance calls effective identification a prerequisite for control, accounting, and audit.

Modern digital systems make the configuration larger and more dynamic. Source code may be unchanged while dependencies, build image, secrets, feature flags, data, model weights, policy, infrastructure or external services change behavior. NIST SP 800-128 addresses security-focused configuration identification, baseline control, impact analysis, testing, authorization, implementation confirmation and monitoring. Its federal information-system scope is explicit; the broader systems principles still require domain tailoring.

Too much control can obstruct low-risk work; too little can release unsafe or irreproducible products. The answer is not “put everything under the same board.” Identify items by decision consequence, establish control classes/authorities, automate repeatable low-risk paths, and retain stronger review for changes with broad, irreversible, safety/security, contractual, interface or lifecycle effects.

## Prerequisites and Retrieval

Before establishing or auditing configuration identification/control, retrieve:

1. system/lifecycle scope, stakeholders, decisions, criticality, hazards/threats, regulations/contracts, product hierarchy, locations, variants, production/deployment model, suppliers, operations, sustainment, upgrades, and retirement;
2. CM policy/plan with functions, roles, authorities, boards, thresholds/classes, emergency process, interfaces, tools, records, metrics, audits, supplier flow-down, and tailoring;
3. CI-selection criteria based on safety/security, mission/value, interface, independent change, replacement, procurement, evidence, reuse, ownership, support, and retirement consequence;
4. authoritative requirements, architecture, interface definitions, design/product structures, specifications, drawings/models, code/repositories, build/release/deployment definitions, data/schema/models, infrastructure, policies, procedures, facilities, and training;
5. identifier/version/nomenclature rules for item type, family, variant, revision, instance, serial/lot, supplier, environment, build, release, deployment, branch, date, and lifecycle state;
6. baseline definitions, content manifests, approved versions/digests/signatures, precedence, effective date, scope/effectivity, owner, approval, repository, retention, and supersession;
7. as-designed, as-planned, as-procured, as-built, as-tested, as-delivered, as-deployed, as-operated, as-maintained and as-retired records plus deviations/waivers;
8. change request/proposal fields: origin/need, current/proposed state, scope, affected items/relationships/instances, alternatives, impact, priority/urgency, cost/schedule, hazards/threats, supplier, evidence, transition/rollback and authority;
9. implementation plan with tasks, owners, order, compatibility/coexistence, data conversion, sites/serials/lots, production/work instructions, procedures/training, monitoring, verification/validation, acceptance, rollback and old-version retirement;
10. build/supply provenance: source commit, dependencies/locks, compiler/toolchain, generated outputs, artifacts/digests/signatures, SBOM/BOM, suppliers/lots/processes, custody, reproducibility, attestations, promotion and storage;
11. CSA and audit data for approvals, releases, installed base, field changes, drift, failed/partial rollouts, anomalies, waivers, evidence applicability, spare/repair state, supplier notices and end-of-support;
12. recovery/forensic/retirement needs: retained baselines, backups, rollback artifacts, access, final configurations, data/records, licenses/rights, archival formats, deactivation and residual ownership.

Perform a **configuration thread**: select one operational behavior and trace requirement, design/model, parts/code/data/policy, build/procurement, integration/test configuration, delivery/deployment, observed runtime/field instance, maintenance/change history, evidence, and retirement path. Mark every identity or relationship inferred rather than recorded.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish configuration, CI, configuration record, baseline, variant, instance, revision, version, release, deployment, and effectivity;
2. select CI/control granularity based on decisions and risk rather than tool defaults;
3. define stable identifiers, product/dependency structures, authoritative sources, and lifecycle states;
4. represent hardware, software, data, models, infrastructure, procedures, facilities, people/roles, and supplier configurations;
5. reconcile as-designed, built, tested, delivered, deployed, maintained, and retired configurations;
6. design proportionate normal, preapproved/automated, urgent, and emergency change-control paths;
7. perform change impact, authorization, implementation, verification/validation, rollback, status accounting, and communication;
8. establish build/supply provenance and observed-state monitoring without confusing hashes with semantic correctness;
9. audit interface, supplier, fleet/site, evidence, waiver, and field-maintenance effectivity;
10. preserve configuration knowledge and artifacts for incident response, evidence reuse, sustainment, and retirement.

## Core Exposition

**Plan from decisions and consequences.** Identify who needs to know exact configuration for design, procurement, build, test, acceptance, operation, incident, maintenance, regulatory evidence, reuse and retirement. Select rigor and data latency accordingly. A safety-critical serialized item and a reversible documentation draft need different control.

**Select CIs at durable boundaries.** Candidates have independent requirements/function, interfaces, procurement/supplier, build/release, replacement/maintenance, authority, verification, security/safety or retirement significance. Too coarse hides affected components; too fine floods governance. Hierarchical CIs allow top-level control with detailed automated constituent manifests.

**Define the configuration information model.** Represent item types, stable IDs, versions/revisions, variants, instances, lifecycle states, composition/dependencies/interfaces, owners, authoritative sources, provenance, effectivity, baselines, changes, waivers, evidence and actual deployments. Avoid one spreadsheet cell containing an unqueryable comma-separated configuration.

**Design identifiers deliberately.** A part number identifies design/configuration definition under governed rules; a serial identifies an instance; a lot identifies production grouping; a revision identifies controlled definition change; a build/release identifies assembled software artifacts; a deployment identifies promotion to environment/site. Do not encode mutable status or excessive meaning in IDs.

**Control nomenclature and metadata.** Names should be durable and human-usable while machine IDs remain stable. Define allowed characters, uniqueness domains, case, aliases, supersession, label placement, barcode/RFID/digital identifiers, time, supplier identifiers and collision handling. Preserve history when renaming.

**Identify relationships and interfaces.** Composition and dependency are configuration. A software artifact depends on source, generated code, libraries, toolchain and build environment; a deployed service also depends on infrastructure, schema, policy, secrets references, feature flags and external endpoints. Hardware depends on materials, processes, firmware, calibration and supplier lots. Record compatibility and precedence.

**Assign ownership across boundaries.** The owner of an item is not automatically authorized to change every relationship that consumes it. Define custodians for product structures, interfaces, shared schemas, common parts, platform services, reference data and cross-organization baselines; identify technical, contractual, safety, security and operational concurrence. Supplier or platform ownership does not remove downstream impact duties. When ownership transfers, reconcile identifiers, repositories, access, open changes, effectivity, evidence, records and field populations instead of merely changing a contact name.

**Establish authoritative baselines.** A baseline has purpose, content manifest, source revisions/digests, scope/effectivity, date, owner, approval and access. The manifest points to controlled artifacts; it is not merely a folder copy. Baselines are snapshots for decision/change comparison, not claims that design is perfect.

**Capture actual-state configurations.** Build/procurement records establish as-built; test logs/manifests establish as-tested; delivery packages establish as-delivered; inventory/discovery/attestation establishes as-deployed/maintained. Observe reality because declared automation can fail, manual changes occur, and physical substitutions may be mislabeled.

**Initiate changes with an evidence-bearing proposal.** Record need/problem/opportunity, requester, current/proposed configurations, affected baselines/CIs/instances/interfaces, alternatives including no change, rationale, urgency, lifecycle impact, required evidence, transition, rollback and retirement. Keep proposals separate from approvals and implemented state.

**Analyze full impact.** Trace requirements, architecture, interfaces, hazards/threats, reliability, human work, supply/production, verification/validation, operations, data, cost/schedule, contracts, training, maintenance, evidence reuse, variants, sites, stored artifacts and disposal. Automated dependency graphs help; expert semantic and organizational review finds undeclared coupling.

**Use proportionate authority.** Define classes such as editorial, low-risk preapproved, routine board, critical/technical-authority, and emergency. Approval belongs to the accountable owner(s) for affected baselines and interfaces. Separate request, technical assessment, approval, implementation and verification where consequence warrants.

**Control emergency changes.** Establish incident commander/authority, scope/time bounds, evidence capture, peer/safety/security checks, rollback, monitoring and notification. After stabilization, reconcile actual state, complete impact/V&V, decide retain/revert, update baselines and retire temporary access. “Emergency” cannot become a permanent uncontrolled branch.

**Implement as an ordered transition.** Update products and defining information coherently: design, supplier/work instructions, code/build, schema/data, infrastructure/policy, procedures/training, test/acceptance, inventory, sites/serials and support. Manage mixed versions, compatibility, feature flags, rollout cohorts, maintenance windows and rollback.

**Verify both change and configuration.** Confirm the authorized change is correctly implemented and achieves intended behavior without unacceptable regression; also confirm actual product composition/attributes agree with defining information. Use physical inspection, inventory, checksums/signatures, SBOM/BOM comparison, queries/discovery, functional tests, audits and reconciliation as appropriate.

**Account for status and effectivity.** Report proposed/assessed/approved/scheduled/implemented/verified/closed/rejected/superseded state; affected baselines; serials/lots/sites/releases; partial failures; deviations/waivers; evidence; and remaining old configuration. A global “deployed” status is false when one site or spare pool differs.

**Monitor drift and unauthorized change.** Compare observed state to authorized baseline at meaningful cadence. Detect unknown devices/packages, misconfiguration, manual edits, expired policies/certificates, supplier/field substitutions and documentation divergence. Quarantine or risk-assess rather than blindly force remediation that might disrupt operations.

**Measure configuration health without gaming it.** Useful measures include unidentified items, unauthorized changes, stale baselines, incomplete effectivity, implementation latency, failed/partial changes, drift duration, wrong-configuration escapes, unreconciled emergency work, audit findings, dead provenance links and mean time to reconstruct an incident configuration. Interpret trends by criticality and denominator. A rising report count can reflect improved discovery; a fast approval time can hide weak impact review; zero drift can mean excellent automation or no observation. Pair process measures with sampled product-to-definition audits and operational outcomes.

**Protect the control system itself.** Configuration repositories, signing/build services, inventories, scanners, boards, identities and automation are part of the assurance system. Control their code/configuration, privileges, separation of duties, backups, logs, time, availability and recovery. A compromised manifest generator can make false consistency look authoritative. Retain independent comparison paths and test restoration so CM does not depend on one unverified source.

**Preserve configuration for evidence and recovery.** Retain enough source, artifacts, dependencies, tools, data/schema, procedures, product records, decisions and access to reproduce analysis, investigate incidents, repair, rollback and interpret historical evidence. Retention depends on lifecycle/legal/security constraints; secrets themselves need special handling.

**Retire configuration items deliberately.** Identify last instances/dependencies, migrate consumers/data, revoke identities/access, dispose parts/materials, archive required records/artifacts, update product structures and close supplier/support. A CI may be retired from production but still controlled in field support.

The following fixture compares a declared release manifest with observed deployment state.

<!-- bijux-verify: {"id":"configuration-identity-fixture","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"configuration_dimensions=8\ndeclared_manifest_entries=8\nobserved_entries=8\nmatching_entries=7\nmismatches=data_schema\ninitial_authorization=reject_configuration_mismatch\nafter_correction_matching_entries=8\nafter_correction_authorization=eligible_for_declared_metadata_gate\nstatus=declared_configuration_fixture_consistent\nevidence=synthetic_exact_string_comparison_only\n","stderr":""}} -->
```python
declared = {
    "application": "app@4.2.1",
    "dependencies": "lock@sha256:111",
    "container_image": "image@sha256:222",
    "infrastructure": "infra@sha256:333",
    "data_schema": "schema@17",
    "policy": "policy@9",
    "runbook": "runbook@12",
    "test_evidence": "evidence@sha256:444",
}
observed = dict(declared)
observed["data_schema"] = "schema@16"

def mismatches(expected, actual):
    return [key for key in expected if expected[key] != actual.get(key)]

initial = mismatches(declared, observed)
print(f"configuration_dimensions={len(declared)}")
print(f"declared_manifest_entries={len(declared)}")
print(f"observed_entries={len(observed)}")
print(f"matching_entries={len(declared) - len(initial)}")
print("mismatches=" + ",".join(initial))
print("initial_authorization=reject_configuration_mismatch")

observed["data_schema"] = "schema@17"
after = mismatches(declared, observed)
print(f"after_correction_matching_entries={len(declared) - len(after)}")
print("after_correction_authorization=eligible_for_declared_metadata_gate")
print("status=declared_configuration_fixture_consistent")
print("evidence=synthetic_exact_string_comparison_only")
```

The fixture trusts declared observations and exact strings. It does not verify artifact contents, signatures, provenance, semantic compatibility, runtime loading, database state, hidden configuration, authorization, security, behavior, or real deployment integrity.

## Definitions and Notation

Let CI $i=(id,type,rev,state,owner,source)$ and configuration graph $C_t=(N,L,B,E,P)$. A product structure edge can mean contains, depends-on, implements, generated-from, interfaces-with, installed-at, instance-of, supersedes or evidence-for; edge type and effectivity matter.

Change request $q=(C_{before},C_{proposed},scope,rationale,I,V,T,R,\alpha)$ captures before/proposed state, scope, rationale, impact, V&V, transition, rollback and authority. Approval authorizes bounded implementation; it does not assert implementation or success.

Let observed actual state $\widehat{C}_{t,s}$ apply at time $t$ and site/instance $s$. Drift set $D=C_{authorized}\ominus\widehat{C}$ includes missing, extra, mismatched and unknown items/relationships. Semantic consequence requires analysis beyond set difference.

## Mechanisms, Invariants, or Proof Structure

A defensible identification/control argument follows this chain:

1. define lifecycle decisions, risk, CM scope, roles, authorities, control classes and records;
2. select hierarchical CIs and controlled information at durable ownership/change/evidence boundaries;
3. establish stable identifiers, types, variants/instances, relationships, effectivity, authoritative sources and lifecycle states;
4. create controlled baselines/manifests and capture as-designed/built/tested/delivered/deployed/maintained views;
5. propose changes against explicit before/proposed state and analyze full technical/programmatic/operational/lifecycle impact;
6. authorize through appropriate normal/preapproved/emergency paths with interfaces and risk authorities;
7. implement ordered transitions across products, information, instances, evidence, people/procedures and support;
8. verify behavior and configuration, account for actual effectivity, reconcile drift and preserve history;
9. monitor, audit, recover, sustain and retire configurations under continuing ownership.

The invariants are stable identity, typed relationships, explicit effectivity, authoritative baseline, actual-state evidence, proposal/approval/implementation separation, full impact, bounded authority, verified transition, honest status, drift visibility and lifecycle retention.

## Alternatives and Trade-Offs

**Coarse versus fine CIs.** Coarse control reduces overhead but hides dependencies/effectivity; fine control improves precision but floods boards and data. Use hierarchical items and automated constituent manifests.

**Semantic versions versus immutable digests.** Versions communicate compatibility intent; digests identify exact bytes. Use both plus provenance/configuration because neither proves behavior.

**Central board versus delegated control.** Central review integrates impacts; delegated/preapproved automation speeds low-risk work. Define thresholds, guardrails, audits and escalation.

**Declared state versus observed state.** Infrastructure/code-as-definition is reproducible; discovery catches manual/runtime/physical reality. Reconcile rather than choose one fiction.

**Reproducible builds versus attestations.** Reproducibility independently compares outputs; attestations record trusted process/provenance. Use risk-appropriate combinations and secure builders.

**Immediate consistency versus staged effectivity.** Simultaneous updates reduce mixed states but can be impractical. Staged rollout needs compatibility, cohort identity, monitoring, rollback and expiry.

**Automatic drift correction versus investigation.** Auto-remediation limits exposure; it can destroy evidence or break intentional emergency state. Classify/quarantine/escalate before destructive correction where consequence warrants.

**Permanent retention versus minimization.** Long retention aids evidence/support; increases privacy/security/cost and tool-obsolescence burden. Apply declared legal/lifecycle need and protected archival.

## Failure Modes and Misconceptions

**“Version 4.2 identifies the system.”** It omits build, dependencies, data, policy, infrastructure, instance and state.

**“Git is configuration management.”** It versions some files; CI selection, authority, effectivity, actual state, suppliers, evidence and audits remain.

**“A hash proves correctness.”** It identifies bytes under an algorithm, not semantics, provenance, trust, loading or suitability.

**“The manifest says it is deployed.”** Observed runtime/field state can differ.

**“Same part number means interchangeable.”** Material/process/supplier/firmware/tolerance or qualification can differ.

**“Approved means implemented.”** Status must distinguish proposal, approval, rollout, verification and closure.

**“The board approved our side.”** Interface changes require all controlling parties/authorities.

**“Emergency changes bypass CM.”** They use a faster bounded CM path and later reconciliation.

**“Drift should always be overwritten.”** Unknown state may be safety-critical evidence or an authorized-but-unreconciled intervention.

**“Retired means delete the records.”** Support, legal, safety, incident and historical evidence may require controlled retention.

## Worked Examples

### Example 1

A circuit board retains its part number after dielectric material changes. Electrical test passes nominally, but thermal/reliability evidence no longer clearly applies. Proper identification changes revision/effectivity, links supplier process/lot and triggers qualification impact rather than hiding the change.

### Example 2

Application commit is identical across two deployments, yet one loads a newer library and old database schema. Release identity includes lockfile/build image/schema; observed state blocks evidence reuse until configuration and compatibility are reconciled.

### Example 3

An interface enum changes at one supplier. Each side updates its local specification with the same revision number but different content. Multi-party authoritative interface baseline, digest, precedence and approval prevent nominal revision equality from masking divergence.

### Example 4

A field technician installs an equivalent-looking spare during outage. Serial/lot and work order are later captured; impact checks certification, calibration and maintenance data. Emergency restoration remains visible and may require replacement or approved equivalence.

### Example 5

Infrastructure source declares three replicas but a manual incident action leaves four. Discovery detects extra state. Investigation preserves evidence, determines capacity/security/cost impact, then either authorizes source update or removes the instance under controlled recovery.

### Example 6

A machine-learning service uses recorded code/model weights but an unversioned feature transform and live reference table. Predictions cannot be reproduced. Both data/feature pipelines and reference snapshots become CIs with privacy-aware provenance/effectivity.

### Example 7

A test passed hardware serial 17 with firmware 5.1, calibration C and procedure P9. The delivered serial 18 uses firmware 5.2. Evidence transfer requires explicit equivalence/impact and unit acceptance, not copying the pass by product family name.

### Example 8

A security hotfix is deployed before the board meets. Emergency authority, exact patch/build/site list, monitoring and rollback are recorded; after stabilization the team completes impact/regression, updates baseline and removes temporary credentials.

### Example 9

A fleet rollout dashboard says 100%, but two offline units and spares remain old. Effectivity/status distinguishes online deployment, offline pending and spare inventory. Compatibility and vulnerability exposure remain until every relevant instance is dispositioned.

### Example 10

A service is retired, but build tools, source, schema, final data export, incident evidence and client migration records have different retention needs. Retirement closes active identities/endpoints while archival configuration preserves authorized future interpretation without retaining unnecessary secrets.

## Cross-Program Connections

- **Platform engineering:** infrastructure/configuration as code, golden images, policy, identity, deployment cohorts, drift and emergency changes need observed-state CM.
- **API/service engineering:** schemas, protocols, clients/providers, version matrices, feature flags, dependencies, data migrations and endpoint retirement are configuration relations.
- **Data engineering:** schema, pipeline code, reference data, lineage, transformations, quality rules, model/features and retention define reproducible data products.
- **Object-oriented/functional programming:** packages/modules/types, lockfiles, pure/effectful boundaries, generated code and property evidence fit software configuration structures.
- **Supply/manufacturing:** part/revision, serial/lot, materials/process, tooling, work instructions, supplier changes, acceptance and field maintenance establish physical identity.
- **Security:** baseline hardening, SBOM, provenance, access, impact analysis, authorization, continuous monitoring and incident evidence are configuration controls.
- **Verification/validation:** every result is configuration-specific; equivalence, retest, anomaly and change impact depend on accurate identity/effectivity.
- **Records/knowledge:** authoritative sources, status, provenance, retention, access and archival formats make configurations durable beyond teams/tools.

## References

1. NASA, [Configuration Management, Systems Engineering Handbook section 6.5](https://www.nasa.gov/reference/6-5-configuration-management/), accessed 2026-08-31.
2. NASA, [Configuration Management Plan Outline, Appendix M](https://www.nasa.gov/reference/appendix-m-cm-plan-outline/), accessed 2026-08-31.
3. NASA, [SWE-081 — Identify Software Configuration Management Items](https://swehb.nasa.gov/spaces/7150/pages/16450453/SWE-081%2B-%2BIdentify%2BSoftware%2BCM%2BItems), accessed 2026-08-31.
4. NIST, [SP 800-128, Guide for Security-Focused Configuration Management of Information Systems](https://csrc.nist.gov/pubs/sp/800/128/upd1/final), updated 2019.
5. NASA, [Technical Data Management, Systems Engineering Handbook section 6.6](https://www.nasa.gov/reference/6-6-technical-data-management/), accessed 2026-08-31.
6. NASA, [Requirements Management, Systems Engineering Handbook section 6.2](https://www.nasa.gov/reference/6-2-requirements-management/), accessed 2026-08-31.
7. NASA, [Interface Management, Systems Engineering Handbook section 6.3](https://www.nasa.gov/reference/6-3-interface-management/), accessed 2026-08-31.
8. NASA, [Product Verification, Systems Engineering Handbook section 5.3](https://www.nasa.gov/reference/5-3-product-verification/), accessed 2026-08-31.
9. NASA, [Systems Engineering in Phase E, Appendix T](https://www.nasa.gov/reference/appendix-t-systems-engineering-in-phase-e/), accessed 2026-08-31.
10. NASA, [NPR 7123.1B, NASA Systems Engineering Processes and Requirements, Change 4](https://nodis3.gsfc.nasa.gov/displayAll.cfm?Internal_ID=N_PR_7123_001B_&page_name=ALL), effective 2020.

## Exercises

### Exercise 1

Design CI selection, identifiers and configuration structure for an autonomous inspection service spanning robots, software, ML/data, cloud, operators, facilities and suppliers.

### Exercise 2

A release has 12 declared configuration dimensions. Ten match observed state, one is missing and one differs. Compute naive match coverage and define the authorization decision and missing evidence.

### Exercise 3

Create a controlled emergency-change process for a production security vulnerability requiring immediate mitigation and later permanent correction.

### Exercise 4

A supplier proposes a “form-fit-function equivalent” part under the same catalog number. Design identification, impact, qualification, effectivity and fleet handling.

### Exercise 5

Audit whether verification evidence from build 7 can support build 8 after source, compiler, dependency, schema and infrastructure changes.

## Answers to the Exercises

### Answer 1

Select hierarchical CIs by independent behavior/change/evidence/risk: robot platform and serialized instances; sensors/actuators/batteries with firmware/calibration/lots; autonomy/application release; ML model and training/validation data lineage; feature/transformation/reference data; container/build/dependencies; cloud infrastructure/network/identity/policy; schemas/pipelines; mission configuration/geofences; operator console; procedures/training; charging/maintenance facilities/tools; spares and suppliers. Avoid treating every source file as board-level CI while retaining it in lower-level manifests.

Define stable design IDs, revisions, variants, serial/lot, software artifact digests plus semantic release, model/data/schema versions, infrastructure/policy digests, facility/site and deployment/cohort IDs. Typed relationships capture contains, depends, interfaces, installed-on, calibrated-with, trained-for, deployed-at and evidence-for. Baselines identify approved fleet release and site mission package; observed state records each robot/cloud deployment.

Control supplier/firmware/model/data/procedure changes through impact on navigation, perception, safety, privacy, interfaces, operations, verification and stored missions. Status accounts for offline robots/spares and emergency repairs. Audits reconcile physical labels/BOM/calibration, signed software/model artifacts, cloud/schema/policy discovery, operator procedures and evidence. Retirement migrates missions/data, revokes identities, disposes batteries/electronics and preserves required safety/incident/configuration records.

### Answer 2

Naive exact-match coverage is $10/12=83.33\%$. It does not support authorization because one required dimension is absent and one contradicts the authorized manifest; criticality and semantics are unknown. Report 10 matching, 1 missing, 1 mismatched with exact identities rather than a green percentage.

Hold or reject configuration-dependent authorization until governance determines scope. Identify whether observed-state collection failed or the item is truly absent; preserve raw discovery and clocks/provenance. For mismatch, obtain intended/actual versions, contents/digests/signatures, ownership, effectivity, change history and runtime loading. Analyze compatibility, behavior, safety/security, evidence applicability, data/interface and rollback. Correct observed state or authorize a changed baseline under proper impact/V&V, then rediscover and verify all 12. A match proves metadata equality under the method, not functional correctness or provenance.

### Answer 3

Preauthorize an emergency path with trigger/severity, incident commander and technical/security authority, scoped implementers, protected branch/build, independent peer check where time permits, evidence capture, allowed mitigations, test minimums, rollout limits, monitoring, abort and rollback. Record vulnerability/advisory, affected configurations/sites, current/proposed state, threat/exposure, secrets/data, exact artifacts/digests, builders and approvals.

Apply least disruptive containment first when appropriate—feature disable, access restriction, isolation or compensating control—then a signed reproducible patch. Stage canary/cohorts if exposure permits; monitor exploitation indicators, correctness, availability and regressions. Preserve prechange state, logs and rollback artifacts. Status account every instance including offline/spares and communicate operational restrictions.

After stabilization, complete full impact across requirements/interfaces/hazards, root cause, dependency/supply, V&V and incident obligations. Decide retain/revise/revert; update source, locks/SBOM, baseline, documentation/runbooks/training, evidence and inventory; remove temporary access/controls; verify all effectivity and old-version retirement. Emergency speed changes workflow latency, not the need for identity, authority, evidence and reconciliation.

### Answer 4

Do not let catalog equality decide configuration equality. Obtain manufacturer/design identifier/revision, drawings/specs, material, process/site, subtiers, firmware, tolerances, environmental/rating/reliability data, qualification, certifications, obsolescence and lot traceability. Assign internal controlled identity/revision or approved alternate relation; preserve supplier lot/date codes and effective serials/builds.

Impact requirements, interfaces, loads/thermal/electrical/timing, hazards, reliability/maintainability, manufacturing/tooling/inspection, software/firmware, qualification/certification, spares, field procedures, warranty/contracts and disposal. Verify dimensional/interface and functional equivalence, then risk-based environmental/durability/reliability and integrated tests; update analyses and evidence. Independent/technical authority approves where required.

Implement via controlled BOM/drawing/work-instruction/incoming inspection and acceptance updates with start lot/date/serial effectivity. Quarantine mixed/unidentified stock; label and status account old/new spares and field population. Use staged production and monitoring. If not fully equivalent, treat as variant/change, not an alternate. Define retrofit, coexistence, maintenance and rollback/disposition; feed field anomalies back to supplier and design authority.

### Answer 5

Construct a delta matrix. Source changes map to requirements, behavior, tests and hazards. Compiler/toolchain changes can alter optimization, numerical behavior, ABI, timing and generated binaries. Dependency changes affect APIs, faults, licenses and vulnerabilities. Schema changes affect compatibility, data conversion, stored/replayed data and rollback. Infrastructure changes affect topology, identity, resources, timing, failure and observability. Compare build flags, generated code, base images, policies/config/flags and evidence tools/data too.

Retain build-7 requirement trace, test design, fixtures/oracles and unaffected analyses as assets; do not relabel executions. Establish exact build-8 provenance and approved equivalence/no-impact rationale per row. Re-run unit/static/security/licensing, changed-component and interface/contract tests; perform numerical/timing/differential tests for compiler effects; schema migration/reconciliation/old-new compatibility/rollback; infrastructure policy/network/capacity/failure/recovery; and impacted end-to-end validation. Run stable broad regression.

Evidence support is row-specific: unchanged propositions may use similarity with authority; configuration-sensitive results require build-8 execution. Resolve anomalies, update SBOM/schema/infrastructure/runbooks/authorization and observed deployment. Record limitations and prevent global “build 8 verified” from a source-only comparison.
