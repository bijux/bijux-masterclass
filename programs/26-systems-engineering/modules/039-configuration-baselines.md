---
module_id: SYSENG-039
program: Systems Engineering
level: 1
module_number: 39
title: Configuration Baselines
status: complete
last_verified: 2026-08-31
---

# Configuration Baselines

## One-Page Review

### Governing question

How can a program establish a coherent, reproducible, auditable reference configuration across requirements, architecture, interfaces, hardware, software, data, procedures, environments, and evidence while still permitting controlled change and field variation?

### Essential definitions

- A **configuration** is the interrelated functional, performance, physical, and operational characteristics of a product or system at a declared time and applicability.
- A **configuration item (CI)** is an item or aggregation selected for configuration management because its identity, changes, status, and integrity need explicit control.
- A **configuration baseline** is a formally reviewed and agreed description of one or more CIs at a point in time that becomes the reference for controlled change.
- A **baseline configuration** is the approved configuration realized or intended for a system/context; some standards reverse or specialize this terminology, so define local usage.
- **Configuration identification** selects CIs, product structures, attributes, documents/models, identifiers, versions, variants, and control authority.
- **Effectivity/applicability** states which serials, lots, sites, regions, versions, modes, dates, customers, or operational contexts a configuration or change governs.
- **Configuration change control** evaluates, authorizes, implements, verifies, communicates, and records changes to controlled items and baselines.
- **Configuration status accounting (CSA)** records and reports the current and historical identity, baseline, change, implementation, deviation, audit, and release state of CIs.
- A **functional baseline** describes approved top-level performance, functional, interoperability, interface, and verification obligations; an **allocated baseline** distributes them to subordinate CIs; a **product baseline** describes the producible/fieldable design and acceptance information; an **as-deployed baseline** records the realized deployed configuration. Names and timing vary by organization.
- An **as-designed**, **as-built**, **as-tested**, **as-deployed**, and **as-maintained** configuration describe different lifecycle states that must be reconciled rather than assumed identical.
- A **functional configuration audit (FCA)** examines whether a CI's functional/performance evidence satisfies its approved requirements. A **physical configuration audit (PCA)** examines whether the realized product and its records match the approved product definition; applicable practice and contract define exact scope.
- A **snapshot** captures state; a **release** packages authorized deliverables; a **baseline** adds formal agreement and change reference. None of these terms alone guarantees completeness or deployability.

### Central model, mechanism, or theorem

Represent a baseline as:

$$
B=(I,R,A,P,T),
$$

where (I) is the controlled item/version set, (R) the relations among items, (A) applicability/effectivity, (P) provenance and approval, and (T) the establishment time/event. Baseline coherence requires all referenced items to exist and their versions, interfaces, requirements, procedures, and evidence to be mutually applicable:

$$
Coherent(B)\Rightarrow ClosedRefs(B)\land Compatible(B)\land Applicable(B)
\land Authorized(B)\land Reproducible(B).
$$

For documented set (D) and observed realized set (O):

$$
Missing=D\setminus O,\qquad Unrecorded=O\setminus D,
$$

$$
J(D,O)=\frac{|D\cap O|}{|D\cup O|}.
$$

The Jaccard index is only a discrepancy-discovery aid. (J=1) for item labels does not prove correct versions, settings, connections, behavior, requirements, or evidence.

A change is not complete at approval. Its controlled progression is:

$$
proposed\rightarrow analyzed\rightarrow authorized\rightarrow implemented
\rightarrow verified\rightarrow incorporated\rightarrow communicated,
$$

with rejected, superseded, deferred, failed, rolled-back, and partially effective states preserved.

### Critical invariants

- Each baseline has stable identity, type/purpose, scope, lifecycle state, establishment event/time, owner, approval authority, applicability, and predecessor/successor relations.
- Every CI has stable identity, type, version/revision, ownership, product-structure position, sources, attributes, applicability, and evidence.
- Baseline membership is a closed, immutable historical record; change creates a controlled successor or authorized deviation rather than rewriting history.
- A baseline is internally coherent: requirements, architecture, interfaces, designs, parts, builds, data, procedures, environments, and tests refer to compatible versions and applicability.
- Functional, allocated, product, as-built, as-tested, as-deployed, and as-maintained views are traceable but never assumed identical.
- Approved, implemented, verified, released, installed, activated, and retired change states remain distinguishable.
- Every change records source, rationale, affected items/relations, technical and lifecycle impacts, alternatives, authority, effectivity, implementation, verification, rollback, and communication.
- Interface changes are agreed and controlled on both sides and across intermediaries, not closed by one endpoint alone.
- Supplier, reused, commercial, open-source, external-service, data/model, tool, facility, and human/procedure dependencies have enough identity and change information for the governed decision.
- Status accounting can answer what is approved, built, tested, deployed, maintained, different, open, and authorized for any governed serial/site/version/configuration.
- Audits compare authoritative product information, actual realized state, and functional evidence; repository labels or checksums alone are insufficient.
- Emergency/redline changes are bounded, authorized, recorded, reconciled promptly, and never allowed to become invisible permanent state.
- Access, provenance, authenticity, integrity, retention, backup, reproducibility, and recovery protect configuration records throughout lifecycle and retirement.
- Any claim based on a configuration names that configuration and is reassessed when an applicable change occurs.

### Common failures

Common failures include calling every saved file a baseline; using `latest` or mutable tags; baselining documents independently so their revisions conflict; controlling source but not build tools, dependencies, configuration, data, infrastructure, or deployed state; confusing inventory with product structure; assigning overly coarse CIs that hide critical changes or overly fine CIs that overwhelm control; assuming approved change is installed everywhere; losing serial/lot/site effectivity; letting supplier substitutions bypass interface and evidence analysis; editing a released baseline in place; using checksums as proof of technical correctness; keeping as-built redlines outside status accounting; mixing verified and unverified patches; failing to reconcile as-tested with as-deployed; treating a rollback label as a recoverable state; and retiring assets without preserving required records, keys, data disposition, or reconstruction knowledge.

### Compact example

A controller integration baseline names hardware serial H-17/mod M2, firmware build hash F8, FPGA image P4, calibration C11, interface contract IC-6 revision D, wiring drawing W3 revision B, parameter set K9, time-service profile T2, test procedure TP-14 revision C, emulator E5, and facility configuration L7. Each is individually current, but coherence fails if TP-14 C expects interface IC-6 C or calibration C11 belongs to serial H-16. The baseline is a governed compatible set, not a folder of current artifacts.

### Connections

SYSENG-031–038 create and exercise interfaces, physical elements, subsystem boundaries, integration order, and readiness evidence. This module establishes the exact references that make those claims reproducible. SYSENG-040 uses controlled interface/configuration states in the integration plan. Requirements, risk, decisions, verification, validation, suppliers, safety, security, software/data, operations, maintenance, and retirement all depend on configuration identity and change trace.

## Governing Question

Which characteristics and work products must be fixed as the authoritative reference for a decision or lifecycle state, and how can their mutual consistency, realized implementation, controlled evolution, and historical reconstruction be demonstrated?

A baseline is neither “everything is frozen” nor “the files we happen to have.” It stabilizes a defined scope so work, contracts, tests, integration, deployment, and change can refer to the same truth. The baseline can evolve through authorized successor states; its historical content must not drift silently.

## Why This Matters

Complex systems exist in several simultaneous representations: stakeholder and technical requirements, architecture models, interface contracts, product structures, drawings, parts, hardware modifications, source/builds, configurations, datasets/models, procedures, tools, facilities, deployed instances, and evidence. If identities and applicability diverge, a test can pass the wrong article, a repair can use an incompatible drawing, a supplier can ship an unapproved option, or an operation can rely on a property removed months earlier.

NASA's current Configuration Management guidance describes CM as providing product visibility and change control across the lifecycle and identifies planning, configuration identification, change management, status accounting, and verification. It distinguishes functional, allocated, product, and as-deployed baselines. NASA's CM standard emphasizes identifying configurations over time, controlling changes, maintaining integrity/traceability, and preserving records. These named baselines reflect NASA practice; other organizations tailor terminology and establishment events.

NIST's security-focused configuration guidance defines baseline configurations as formally reviewed, agreed specifications used for future builds/releases/changes and includes architecture, interconnections, settings, software loads, procedures, topology, and component placement. Security configuration is one important viewpoint, not the whole system baseline. Physical, functional, human, data, environmental, supplier, and lifecycle characteristics remain governed.

Configuration management enables learning rather than preventing it. Engineers can change a baseline when the impact is understood, authority agrees, implementation is controlled, verification is defined, and affected stakeholders receive the new state. Without that discipline, “move fast” becomes inability to reproduce defects, compare alternatives, trust evidence, or know what is operating.

## Prerequisites and Retrieval

Before continuing, retrieve:

1. system boundary, product structure, lifecycle states, configurations/variants, sites/serials/lots, owners, suppliers, and change authorities;
2. stakeholder/technical requirements, architecture, allocations, budgets, interfaces, hazards, verification/validation, and decisions;
3. hardware drawings/modifications, parts/materials, software/firmware/FPGA source and builds, dependencies/tools, parameters, data/models, and infrastructure;
4. procedures, work instructions, training/qualification, facilities, fixtures, calibration, instrumentation, test environments, and external services;
5. current functional/allocated/product/deployed/maintained definitions or the repository's equivalent baseline taxonomy;
6. change requests, deviations/waivers, anomalies, redlines, supplier notices, vulnerability/obsolescence items, and implementation/effectivity status;
7. status accounting, release/repository controls, provenance, signatures/digests, access, retention, backup, recovery, and audit practices;
8. set difference, graph/reference closure, compatibility, traceability, evidence applicability, and lifecycle change impact.

As a retrieval test, inspect `release 7.4 is deployed`. Ask which source commit, build environment, dependencies, artifact digest, configuration, schema/data/model, feature flags, secrets/certificates, infrastructure, region/tenant, external APIs, migration, procedure, tests, approval, rollout wave, exceptions, and rollback state apply. A marketing version is not an as-deployed baseline.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish configuration, CI, baseline, baseline configuration, snapshot, release, inventory, product structure, and realized instance;
2. distinguish functional, allocated, product, as-designed, as-built, as-tested, as-deployed, and as-maintained states;
3. select CI granularity and stable identifiers based on change, evidence, supplier, safety/security, and lifecycle needs;
4. define a coherent multi-domain baseline with explicit membership, relations, applicability, provenance, and authority;
5. conduct change impact, authorization, implementation, verification, effectivity, communication, and rollback control;
6. maintain status accounting that separates approval from realization across serials/sites/versions;
7. audit reference closure, cross-view consistency, documented-versus-actual state, and functional evidence;
8. govern supplier, commercial, open-source, external-service, data/model, tool, procedure, facility, and human dependencies;
9. control emergency changes, deviations, branch/variant baselines, and lifecycle transitions without erasing history;
10. state what identifiers, checksums, automation, and audits establish and what still requires semantic and physical evidence.

## Core Exposition

**Define local terminology.** Standards and organizations use `baseline`, `configuration baseline`, `baseline configuration`, and named lifecycle baselines differently. Publish a glossary, baseline taxonomy, establishment/approval criteria, control authorities, and relationships. Do not assume a supplier's `released` means your `product baseline`.

**Scope the system and lifecycle.** State system/product, boundary, product layer, lifecycle interval, variants, sites, deployed populations, suppliers, regulatory/contract context, and decisions the CM system supports. Configuration needed for a laboratory model differs from that needed for production, operation, maintenance, and incident reconstruction.

**Select configuration items deliberately.** A CI deserves distinct control when changes have independent requirement/interface/evidence, supplier, safety/security, version, release, maintenance, reuse, replacement, certification, or lifecycle consequences. Too coarse hides impact; too fine floods the board with meaningless transactions. CI selection can evolve through controlled change.

**Give every CI stable identity.** Record identifier, name/type, parent/product-structure use, definition versus instance, owner, supplier, version/revision/modification state, serial/lot/site, source and authoritative repository, controlled attributes/documents/models, interfaces, applicability, status, approvals, evidence, and history. Names such as `controller-final` are not durable identities.

**Separate definition, usage, and instance.** One connector definition may appear in several product usages; one product definition may have thousands of serialized instances. A change may affect the definition, selected usages, a production lot, or one repaired unit. Preserve these distinctions so resources and effectivity are neither duplicated nor generalized falsely.

**Model product structure and other relations.** Whole–part structure, interface, allocation, deployment, requirements, verification, supplier, data lineage, build dependency, spatial placement, and work relationships are different graphs. The baseline references all necessary views through governed identities; a bill of materials alone does not represent behavior or deployment.

**Establish baseline purpose and criteria.** Define why the baseline exists, what decisions/work may rely on it, required maturity/evidence, membership rules, approval authority, establishment event, effective date, and successor policy. Do not baseline immature content merely because a review date arrived; document gaps and authority explicitly.

**Construct an explicit baseline manifest.** List every controlled CI version and relationship; requirements/specifications; architecture/interface models; drawings/BOM/material/process; source/build/artifacts/dependencies; configuration/data/model/schema; procedures/tools/facilities; verification/validation records; deviations; and applicability needed for the scope. Use machine-readable manifests where useful, with human-reviewable rationale.

**Check reference closure.** Every referenced identifier/version must resolve to an authorized object or a declared external dependency. Detect dangling links, mutable references, deleted artifacts, inaccessible supplier records, circular derivations, and unpinned tools. Closure does not prove compatibility but prevents a baseline that cannot be reconstructed.

**Check cross-view coherence.** Trace requirements to architecture and verification; logical allocations to physical CIs; interface endpoints to exact versions; drawings to parts; source to build artifact; data schema/model to code; procedure expected values to interface/configuration; hazard controls to implementation/test; and deployed items to support instructions. `Current` in each repository can still be mutually inconsistent.

**Make applicability explicit.** Record serial/lot/unit ranges, sites/regions, hardware mods, software compatibility, customer/mission, environment, option, date, mode, and exceptions. Use effectivity expressions whose semantics are reviewed. Avoid copying one baseline per variant without controlled shared/variant structure; avoid a giant baseline that shows incompatible alternatives simultaneously.

**Protect provenance and integrity.** Record author/source, review, approval/signature, timestamps, toolchain, derivation, custody, repository, release, and digest where appropriate. Cryptographic hashes can show byte identity relative to a trusted value; they do not show who should have approved it, whether the content is safe/correct, or whether it applies.

**Distinguish baseline from snapshot and release.** A repository commit or database snapshot preserves state. A release selects packaged deliverables. A baseline adds formal agreement and controlled future change. A release may implement one baseline for one target while containing deployment scripts, notes, and migration assets; an operational baseline records what actually became active.

**Control change from source to closure.** Change records include stable ID, source/problem/opportunity, affected baselines/CIs/instances/interfaces/requirements/hazards/evidence, rationale, alternatives, benefits, cost/schedule/risk, backwards compatibility, supplier/regulatory impact, verification/validation, migration, effectivity, implementation, rollback, authority, and communication.

**Perform multidirectional impact analysis.** Traverse upward to parent requirements/outcomes, downward to implementations/tests, laterally across interfaces/shared resources, temporally across lifecycle states/field populations, and externally across suppliers/operators/regulators. Search data/schema, security, safety, human, manufacturing, logistics, maintenance, training, and retirement impacts.

**Separate change states.** `Approved` permits action. It does not mean drawings updated, part installed, software deployed, staff trained, test passed, or field fleet incorporated. Track planned/actual implementation by serial/site/version and evidence. Preserve rejected, withdrawn, superseded, deferred, failed, rolled-back, and partially effective changes.

**Define effectivity before rollout.** Identify which new production units, retrofit units, sites, regions, versions, modes, and dates receive the change, with prerequisites and excluded states. Prevent incompatible mixed configurations or design their interoperability deliberately. Record transition states, not only before and after.

**Verify and validate the change.** Confirm implementation matches authorized definition, affected requirements/interfaces/hazards are verified, regression covers credible impact, and intended stakeholder/lifecycle outcome remains valid where applicable. Close change only after status records, baselines, support/training, supplier information, and downstream evidence are updated.

**Maintain configuration status accounting.** The system should answer: What baseline is approved? What changed and why? Which configuration is designed, built, tested, deployed, and maintained? Which instances incorporate change X? Which deviations/anomalies remain? Which evidence applies? What differs between baselines? Who authorized it? Can the prior state be reconstructed?

**Reconcile as-designed and as-built.** Capture material/part substitutions, manufacturing deviations, rework, software loads, calibration, wiring/assembly, serial/lot, inspection, and redlines. An as-built record is not trustworthy merely because work orders closed. Audit representative/critical physical state and resolve discrepancies.

**Reconcile as-tested.** Record the exact article, versions, settings, fixtures, environment, procedure, instrumentation/calibration, test data, patches, anomalies, and deviations used. If the tested configuration differs from the intended deployment, analyze whether evidence transfers and what regression is required.

**Reconcile as-deployed and as-maintained.** Deployment adds site infrastructure, accounts/keys, external services, data, settings, network, operators, and local variations. Maintenance adds replacements, repairs, patches, calibration, cannibalization, temporary measures, and wear state. Update records promptly and audit high-risk drift.

**Govern software and build reproducibility.** Control source, dependencies, compiler/interpreter, build scripts, containers/toolchains, flags, generated code, artifact digests/signatures, SBOM/provenance, configuration, schemas/migrations, infrastructure, test evidence, and release approvals. Reproducible bytes help but do not prove behavior or deployment identity.

**Govern data and models.** Datasets, schemas, taxonomies, features, parameters, trained-model weights, preprocessing code, evaluation sets, seeds where meaningful, licenses/consent, lineage, quality, drift thresholds, and retention can change system behavior. Baseline them to the resolution needed for reproduction, safety, privacy, audit, and operations.

**Govern external and supplier dependencies.** Pin exact products/options/firmware/services/contracts/APIs/certificates and capture guarantees, evidence, data rights, change notice, obsolescence, support, vulnerability response, and alternates. If a service cannot be frozen, baseline the contract, observed/configured state, monitoring, compatibility envelope, and response to provider change.

**Govern procedures, people, and facilities appropriately.** Procedures, work instructions, training content, role definitions, facility configurations, fixtures, and tools can be CIs. Individual qualifications/status need protected authoritative linkage and applicability, not indiscriminate copying into product repositories. Configuration control must respect privacy and organizational authority.

**Manage branches and variants.** Define a common core, variation points, allowed combinations, compatibility rules, derived manifests, and separate evidence. Prevent branch fixes from disappearing or merging into the wrong product. A variant baseline should be reproducible without assuming `main plus tribal knowledge`.

**Control emergency changes.** Establish who may authorize which deviations, required minimum analysis/testing, bounded effectivity and duration, logging, marking, communication, monitoring, rollback, and deadline for normal-board reconciliation. Emergency authority accelerates control; it does not eliminate identity or evidence.

**Perform functional and physical audits with purpose.** An FCA-like review checks functional/performance evidence against approved obligations. A PCA-like review checks realized product/records against approved product definition. Tailor scope to contract and risk. Sample-based audits state sampling limits; digital inventory checks do not replace physical inspection or semantic review.

**Preserve rollback honestly.** A prior artifact alone is not a rollback baseline. Preserve compatible hardware/firmware, schema/data conversion, configuration, keys/certificates, external contracts, infrastructure, procedures, spares, access, and evidence. Practice recovery for consequential systems. Some changes are irreversible; record that before approval.

**Retain and retire configurations.** Define retention for requirements, designs, source/builds, parts/materials, changes, evidence, operational records, anomalies, supplier data, licenses, keys, and decisions. At retirement, preserve legal/safety/knowledge records, dispose data/secrets/material safely, and record final/de-integrated state.

**State evidence limits.** A manifest proves declarations; a hash proves byte identity under trust assumptions; a clean diff proves textual difference; an audit samples or examines stated scope. None alone proves requirement correctness, physical conformity, compatibility, reproducibility, security, safety, or operational fitness.

The following checker finds selected declaration gaps in six CI records. It cannot establish baseline coherence or actual-product conformity.

<!-- bijux-verify: {"id":"configuration-item-record-check","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"items_total=6\nwell_formed_declared=1\nmissing_version=CI-002\nmissing_applicability=CI-003\nmissing_source=CI-004\nmissing_owner=CI-005\nmissing_evidence=CI-006\nunresolved=CI-002,CI-003,CI-004,CI-005,CI-006\nevidence=declared_fields_only\n","stderr":""}} -->
```python
items = [
    {"id": "CI-001", "version": "4.2", "applicability": ["site-a"],
     "source": "repo://controller@a18f", "owner": "Control Lead", "evidence": ["release-42"]},
    {"id": "CI-002", "version": "", "applicability": ["site-a"],
     "source": "supplier://sensor", "owner": "Sensor Lead", "evidence": ["receipt-7"]},
    {"id": "CI-003", "version": "schema-9", "applicability": [],
     "source": "repo://schema@92b1", "owner": "Data Lead", "evidence": ["migration-test"]},
    {"id": "CI-004", "version": "rev-c", "applicability": ["build-4.2"],
     "source": "", "owner": "Interface Lead", "evidence": ["approval-3"]},
    {"id": "CI-005", "version": "cal-11", "applicability": ["serial-h17"],
     "source": "metrology://cal-11", "owner": "", "evidence": ["certificate-11"]},
    {"id": "CI-006", "version": "proc-d", "applicability": ["site-a", "build-4.2"],
     "source": "docs://procedure/proc-d", "owner": "Operations Lead", "evidence": []},
]
fields = ("version", "applicability", "source", "owner", "evidence")
valid = [item for item in items if all(item[field] for field in fields)]
print(f"items_total={len(items)}")
print(f"well_formed_declared={len(valid)}")
for field in fields:
    print(f"missing_{field}=" + ",".join(item["id"] for item in items if not item[field]))
print("unresolved=" + ",".join(item["id"] for item in items if item not in valid))
print("evidence=declared_fields_only")
```

`CI-001` may still be semantically wrong, incompatible with siblings, unreproducible, or absent from the actual site. Populated fields are necessary declarations, not a successful audit.

## Definitions and Notation

Let configuration items be (I), item versions (V_i), baselines (B), realized instances (X), relations (R), changes $\Delta$, and applicability contexts (A).

A baseline membership function selects one authorized version/state for each required role under applicability (a):

$$
b_a:I_{required}(a)\rightarrow V,
$$

subject to allowed combinations and reference closure. Optional/multiple/redundant uses require explicit cardinality and role identity rather than one simplistic version per definition.

For baseline versions (B_1) and (B_2):

$$
Added=B_2\setminus B_1,\quad Removed=B_1\setminus B_2,
$$

$$
Changed=\{i:version_{B_1}(i)\ne version_{B_2}(i)\}.
$$

These sets require stable identity and normalized applicability. A textual diff can miss semantic change and can overstate regenerated formatting.

Documented/observed reconciliation uses set difference as in the review, plus attribute comparison:

$$
Mismatch=\{i\in D\cap O:attrs_D(i)\not\equiv attrs_O(i)\}.
$$

Equivalence $(\equiv)$ must be defined per attribute and decision.

Change record lifecycle function:

$$
state(\delta,x,t)\in\{proposed,analyzed,authorized,implemented,verified,
incorporated,rejected,deferred,failed,rolledBack,superseded\},
$$

because effectivity may differ by instance (x) and time (t).

## Mechanisms, Invariants, or Proof Structure

**Mechanism 1—configuration planning.** Define scope, terminology, CI selection, baselines, repositories, roles/authorities, change classes, status accounting, audits, supplier/data/security controls, tools, metrics, access, retention, and training.

**Mechanism 2—identification.** Assign stable identities and controlled attributes to definitions, usages, instances, relations, documents/models, builds, datasets, procedures, and evidence. Define applicability and product/variant structure.

**Mechanism 3—baseline establishment.** Assemble the manifest, resolve references, check cross-view compatibility, review maturity/evidence, capture known deviations, approve, sign/release, protect the historical record, and communicate authorized use.

**Mechanism 4—change control.** Receive, classify, analyze multidirectional impact, compare alternatives, define effectivity and verification/rollback, decide with proper authority, implement, verify, reconcile, update successors/status/support, and communicate.

**Mechanism 5—status accounting.** Continuously correlate baseline, CI, change, instance, anomaly, deviation, audit, evidence, and lifecycle state so stakeholders can query exact current and historical truth.

**Mechanism 6—verification/audit.** Compare approved definition, realized product, functional evidence, and records; document discrepancy and sampling limits; correct/retest; and close under authority.

The integrity argument requires:

1. stable identity and applicability;
2. closed, compatible, authorized baseline membership;
3. immutable history with controlled successor changes;
4. traceable implementation/effectivity and evidence;
5. reconciliation of documented and realized states;
6. recoverable records and explicit limitations.

Automation can check structure, signatures, digests, references, allowed combinations, and observed inventory. Human/domain review is still required for semantic, physical, safety, security, supplier, and lifecycle correctness.

## Alternatives and Trade-Offs

**Coarse CI granularity** reduces administrative work but hides change/evidence boundaries. **Fine granularity** improves precision but increases relationship, board, and status-accounting cost. Select by consequence and independent lifecycle.

**Document-centric CM** fits regulated physical work and signed deliverables. **Model/repository-centric CM** improves linkage and automation. Both need authoritative identity, approvals, applicability, released views, and durable access.

**Central control boards** preserve cross-system authority but can bottleneck. **Delegated control** accelerates local change but needs change classes, boundaries, escalation, shared-interface control, and status synchronization.

**Immutable artifacts/manifests** support reproducibility and audit. **Mutable operational resources** are sometimes unavoidable. Control desired state, observed state, drift, provider contracts, monitoring, and reconciliation.

**One common baseline** maximizes uniformity. **Variant/site baselines** reflect real differences. Use inheritance/composition with compatibility rules rather than uncontrolled forks or fictional sameness.

**Manual audits** inspect physical and semantic reality. **Automated discovery** scales and detects drift. Combine them; tooling sees only what it can identify and access.

**Rapid emergency change** reduces immediate exposure. **Normal change control** supplies broader analysis/evidence. Predesign an accelerated governed path with forced reconciliation.

## Failure Modes and Misconceptions

**“A baseline freezes change.”** It creates a known reference from which controlled change proceeds.

**“Git commit equals baseline.”** A commit can identify source state; it may omit approval, build, dependencies, hardware, data, environment, procedure, evidence, and applicability.

**“The newest revision is correct.”** It may not apply to the item/site or be compatible with sibling revisions.

**“Approved means deployed.”** Approval, implementation, verification, release, installation, activation, and fleet incorporation are distinct.

**“The BOM is the configuration.”** It omits relations, software/data/settings, interfaces, procedures, environments, evidence, and instances.

**“The hash proves correctness.”** It proves only byte identity relative to a trusted reference and algorithm assumptions.

**“As-built matches design unless a deviation exists.”** Unrecorded substitution, rework, load, setting, damage, and process drift are precisely why reconciliation/audit exists.

**“Testing release X validates every deployment of X.”** Infrastructure, configuration, data, external services, credentials, site/people, and post-test changes can differ.

**“Rollback means redeploy the old binary.”** Data/schema, hardware, keys, external messages, configuration, and operational state may make that impossible.

**“Emergency fixes can be documented later.”** They must be identified and bounded immediately; later reconciliation completes rather than begins control.

**“CM is clerical.”** Configuration identity determines whether technical analysis and evidence refer to the real system.

## Worked Examples

### Example 1

**Coherent software/hardware baseline.** A controller release manifest names source commit, compiler/container digest, libraries, firmware/FPGA, hardware mod, interface profile, calibration, parameter set, schema, procedure, facility emulator, and expected-test dataset. Automated checks resolve every artifact and allowed combination.

Review finds the procedure expects parameter `limit_v2` absent from the parameter set. Every artifact exists and is signed, yet the set is incoherent. The baseline is corrected or procedure applicability changes before approval.

### Example 2

**Individually current documents conflict.** Drawing D revision F defines a 48 V connector; ICD revision H still states 28 V; test procedure revision J expects a 30 V current limit. Each repository labels its file current.

Cross-view compatibility fails. The change board determines intended design, affected parts/tests/hazards, corrects controlled successors, verifies installed effectivity, and prevents teams from assembling a baseline by selecting independent `latest` artifacts.

### Example 3

**Effectivity by serial and lot.** A bracket change applies to units serial 101–140 except 117, which received a repair; new production from serial 141 uses a supplier alternate. Strength evidence differs by material lot.

Status accounting relates design revision, change, serial, repair, supplier/lot, inspection, and test evidence. `Model B` is insufficient identity for maintenance or fleet claims.

### Example 4

**Approved but not implemented.** Change EC-52 adds a watchdog and is approved for all sites. Site A deploys and verifies it; Site B is scheduled; Site C cannot update because its bootloader is incompatible.

The baseline successor is approved, but as-deployed states differ. Status reports show effectivity and risk; operations do not claim fleet closure. Site C needs prerequisite change or alternate mitigation, with separate verification and communication.

### Example 5

**Documented versus observed drift.** Baseline (D) declares eight item identities. Field observation (O) finds nine; seven are common, one declared item is absent, and two observed items are unrecorded.

$$
|D\setminus O|=1,\quad |O\setminus D|=2,
$$

$$
J(D,O)=7/(8+9-7)=7/10=0.70.
$$

The 0.70 index directs investigation; it does not grade safety. The team identifies versions/settings/relations, quarantines unauthorized changes if needed, corrects reality or records through authorized change, and reassesses evidence.

### Example 6

**Emergency redline.** A leaking field line is rerouted under emergency authority. The redline names unit, drawing, material, route, interfaces, hazard controls, inspection/pressure test, photos, approver, operating limits, monitoring, and expiry.

Within the mandated window, engineering performs full impact, updates design/product/as-maintained records or restores the original, evaluates sibling susceptibility, and communicates maintenance instructions. The redline never becomes an invisible permanent configuration.

### Example 7

**Data/model baseline.** A predictive service release pins training data snapshot/lineage, consent/license, feature code, schema, preprocessing, model weights, hyperparameters, evaluation sets, thresholds, runtime libraries, hardware profile, monitoring, and rollback criteria.

A source-code tag without dataset and feature definitions cannot reproduce behavior. A model digest proves weight identity, not fitness, fairness, privacy, robustness, or drift control.

### Example 8

**External service cannot be frozen.** A payment provider updates infrastructure continuously. The system baseline records API/version, contract semantics, credentials/policies, regions, quotas, known behaviors, certification/test evidence, monitoring, provider change notice, and fallback.

Provider internals remain outside control. The architecture governs the compatibility envelope and detection/response. An outage or unannounced behavior change is not erased by saying the local baseline was unchanged.

### Example 9

**Rollback baseline is incomplete.** A deployment package retains the old application image but applies an irreversible schema migration and rotates keys while external messages are emitted.

Redeploying the image will not restore readable data, keys, or external state. Change analysis either makes migration backward compatible, preserves tested backup/reconciliation and key recovery, or declares irreversibility with stronger rollout controls. `Rollback available` must name the whole recoverable state.

### Example 10

**As-maintained and retirement.** A long-lived facility has replaced sensors, patched controllers, locally repaired harnesses, updated procedures, expired suppliers, and accumulated calibration/evidence. Before retirement, the team baselines current hazardous energy, materials, data/keys, connected external systems, records, and safe de-integration procedure.

Retirement state records discharged energy, removed assets, destroyed/transferred data and credentials, retained evidence, disposed materials, and residual obligations. The original product baseline cannot safely describe the final system.

## Cross-Program Connections

**Platform engineering.** Source, build, artifact, image, infrastructure, policy, secrets/certificates, data/schema, region/tenant, deployment, and observed drift form platform baselines.

**API and service engineering.** Contract/schema versions, compatibility, provider/consumer effectivity, gateway/policy, credentials, quotas, and external behavior require bilateral change trace.

**Data engineering.** Dataset/schema/catalog/lineage/quality/transformation/model/retention and as-processed state must be reproducible and governed.

**Object-oriented programming.** Package versions and dependency locks identify code inputs, while runtime wiring, configuration, data, build toolchains, and deployed instances complete the governed state.

**Functional programming.** Referentially transparent transformations aid reproduction when exact functions and inputs are identified; effects, external state, runtime, and operational configuration remain.

**Security and supply chain.** Provenance, signed artifacts, SBOMs, vulnerability/configuration state, supplier changes, keys, and access protect baseline integrity but do not replace semantic assurance.

**Verification and operations.** Evidence is valid only for named configurations; field anomalies and maintenance must feed status accounting and regression decisions.

## References

1. NASA, *Systems Engineering Handbook, Section 6.5: Configuration Management*, current web edition. <https://www.nasa.gov/reference/6-5-configuration-management/>
2. NASA, *NASA-STD-0005: NASA Configuration Management Standard*. <https://standards.nasa.gov/node/210>
3. NASA, *NASA-HDBK-1004: Configuration Management Guidance*. <https://standards.nasa.gov/sites/default/files/standards/NASA/Baseline/0/2020_04_01_nasa_hdbk_1004_approved.pdf>
4. NASA, *NPR 7123.1B: NASA Systems Engineering Processes and Requirements*, Change 4. <https://nodis3.gsfc.nasa.gov/displayAll.cfm?Internal_ID=N_PR_7123_001B_&page_name=ALL>
5. NIST, *SP 800-128: Guide for Security-Focused Configuration Management of Information Systems*. <https://csrc.nist.gov/pubs/sp/800/128/upd1/final>
6. NIST, *SP 800-171 Revision 3*, Configuration Management requirements. <https://csrc.nist.gov/pubs/sp/800/171/r3/final>
7. NIST Computer Security Resource Center, *Configuration Baseline—Glossary*. <https://csrc.nist.gov/glossary/term/configuration_baseline>
8. NASA, *Systems Engineering Handbook, Section 6.3: Interface Management*, current web edition. <https://www.nasa.gov/reference/6-3-interface-management/>
9. NASA, *Systems Engineering Handbook, Section 6.6: Technical Data Management*, current web edition. <https://www.nasa.gov/reference/6-6-technical-data-management/>
10. ISO/IEC/IEEE, *15288:2023 Systems and software engineering—System life cycle processes*, 2023. <https://www.iso.org/standard/81702.html>

## Exercises

### Exercise 1

Documented baseline set (D) contains 12 item identities; observed configuration (O) contains 13. Ten identities are common. Compute $|D\setminus O|$, $|O\setminus D|$, and (J(D,O)). Explain at least five things the result cannot establish.

### Exercise 2

A change record is approved globally. It has been implemented on 60 of 100 devices, verified on 45, and activated on 40. Ten implemented devices failed verification; five await verification. Describe the configuration/change states without saying “70% complete” or declaring the fleet changed. What actions and records are required?

### Exercise 3

A new power module applies to production lots L20 onward, except export variant E, and to field units serial 500–650 only after harness change H7. Define the effectivity logic in prose or predicates. List configuration and evidence records needed to avoid installing an incompatible combination.

### Exercise 4

Critique: “Production always deploys the latest signed container from main, so its configuration is controlled and rollback is guaranteed.” Identify at least twelve gaps and propose a durable baseline manifest.

### Exercise 5

Design configuration baselines and status accounting for a hospital medication-delivery system spanning pump hardware/firmware, drug library, patient/order/record interfaces, network/time/identity, clinical procedures, nurses, pharmacy, biomedical maintenance, facilities, data/privacy, suppliers, evidence, and retirement.

## Answers to the Exercises

### Answer 1

Common identities are 10, so:

$$
|D\setminus O|=12-10=2,
$$

$$
|O\setminus D|=13-10=3,
$$

and union size is (12+13-10=15):

$$
J(D,O)=10/15=2/3\approx0.6667.
$$

This cannot establish correct versions/revisions; correct settings; correct connections/locations; functional conformance; requirement or interface satisfaction; whether the extra/missing items are consequential; authorized deviations; evidence validity; safety/security; or whether identification tooling saw the full system. Investigate each difference and compare attributes/relations before deciding correction, authorization, quarantine, or evidence impact.

### Answer 2

The global change definition is `authorized`. Instance effectivity differs:

- 40 devices: implemented, verified, and activated under their evidence;
- 5 devices: implemented and verified but not activated (because 45 verified minus 40 activated);
- 10 devices: implemented but verification failed;
- 5 devices: implemented and awaiting verification;
- 40 devices: not implemented.

The ten failures require containment, anomaly/root-cause assessment, affected-baseline/interface/hazard analysis, correction or rollback, regression, and determination whether the same defect threatens the 45 passes or remaining fleet. The five awaiting verification cannot activate. The five verified-not-active need deployment prerequisites/status. The 40 not implemented retain the predecessor as-maintained baseline and associated risks.

Status accounting records each device/serial/site, predecessor/new version, prerequisite configuration, timestamps, work order, installer, verification method/result/anomalies, activation, rollback, and communications. Leadership decides rollout pause/continue/repair under risk authority. No fleet-wide claim is valid until defined effectivity and closure criteria are met.

### Answer 3

One expression is:

$$
Eligible(x)=((lot(x)\ge L20)\land variant(x)\ne E)
\lor(500\le serial(x)\le650\land incorporates(x,H7)),
$$

provided production and field populations are distinguished so the union does not accidentally include an export field unit if export exclusion is universal. If variant E is always excluded, write:

$$
variant(x)\ne E\land((production(x)\land lot(x)\ge L20)
\lor(field(x)\land500\le serial(x)\le650\land incorporates(x,H7))).
$$

Records include unit identity/variant/lot/serial/site; old/new module part/version/supplier/lot; harness H7 design, installed/inspection state, connector/pinout/polarity; power/thermal/mechanical interfaces and budgets; firmware/config compatibility; change approval/effectivity; installation procedure/tools/training; receipt/acceptance; verification/regression; hazard/security impact; deviation/anomaly; as-built/as-maintained update; spares; rollback; and operator/maintenance communication. Review export/regulatory and mixed-fleet constraints explicitly.

### Answer 4

Gaps include mutable `latest`; branch head not an approved source; source commit absent; build workflow/toolchain/dependencies absent; signed-by-whom/authorized-for-what absent; artifact digest/provenance/SBOM absent; target platform/hardware absent; runtime configuration/feature flags absent; infrastructure/network absent; schemas/migrations/data/models absent; secrets/certificates/policies absent; external-service contracts absent; region/tenant effectivity absent; deployment wave/observed state absent; tests/anomalies/waivers absent; approval absent; monitoring absent; rollback lacks compatible data/schema/keys/external state; and prior artifact availability alone does not prove recovery.

A durable manifest names product/release/baseline ID; source commit; reproducible build definition/toolchain/dependency lock; artifact digest/signature/provenance/SBOM; base/runtime/host versions; infrastructure and network topology; configuration/flags/policies; schema/migration/data/model versions; identity/certificates by protected references; external APIs/quotas; region/tenant/site applicability; deployment procedure and automation version; evidence, anomalies, deviations, risk, and approvals; rollout/canary/observability/stop thresholds; current observed instances; and tested rollback/reconciliation configuration. Secrets remain in an authorized protected system while the baseline records identity/version/applicability, not secret material.

### Answer 5

Use related baselines rather than one frozen document pile:

1. **Functional baseline:** clinical outcomes and performance, correct patient/drug/dose/rate/order, alarm, availability, usability, privacy/security, interoperability, maintenance, lifecycle, interfaces, and verification/validation obligations.
2. **Allocated baseline:** obligations allocated across pump mechanics/fluid path/power/sensing, embedded firmware/control, display/alarms, drug-library management, patient/order/record integration, network/time/identity, clinical/pharmacy/biomedical work systems, facilities, suppliers, and cross-cutting safety/security/data ownership.
3. **Product baseline:** exact drawings/BOM/material/disposables; hardware mods; firmware/source/build/toolchain; calibration; libraries/schemas/config; interface contracts; network/security profiles; procedures/training/tools; manufacturing/acceptance/integration/verification; approved supplier options; service/support/cleaning; and controlled evidence.
4. **As-built/as-tested:** pump serial/lot/options, installed firmware/library/config, disposable/fixture, calibration, exact test environments/data/procedures/instrumentation, results, anomalies, waivers, and evidence applicability.
5. **As-deployed/as-maintained:** site/ward, pump serial, active firmware/library/config/certificates, record/order/patient interfaces, network/time/identity, alarms, facility/charging, assigned procedures/training state, replacements/repairs/calibration, patches, local deviations, observed drift, and current risk.

Status accounting answers which pump/site uses which drug library and interface schema; which change/recall affects it; whether hardware/firmware/library combinations are allowed; which nurses/pharmacy/biomedical roles/procedure revisions apply through protected workforce systems; which calibrations and disposables are valid; which anomalies/waivers remain; and which evidence supports the exact state.

Every change traces clinical rationale, hazards, human workflow, interfaces, privacy/security, suppliers, effectivity, mixed-version behavior, verification/validation, training, rollout, monitoring, rollback/reconciliation, and authority. Emergency clinical or security changes use bounded fast control and forced reconciliation. External EHR/identity/time/network services are governed through contract/version/configuration/monitoring even when internals cannot be frozen.

Retirement records safe fluid/energy state, cleaning, hazardous/material disposal, patient/audit data retention/deletion, credential/key revocation, library/software records, supplier/service termination, removed units, retained safety/regulatory evidence, and final configuration. Baselines and audits support traceability; they do not themselves prove clinical safety, regulatory conformity, cybersecurity, human usability, or correct patient operation.
