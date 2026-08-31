---
module_id: SYSENG-084
program: Systems Engineering
level: 2
module_number: 84
title: Baseline Management
status: complete
last_verified: 2026-08-31
---

# Baseline Management

## One-Page Review

### Governing question

Can the organization identify the exact approved technical state used for a decision, control every subsequent departure from that state, reconcile the approved definition with actual products and deployments, and preserve enough authority, provenance, effectivity, and evidence to support change, recovery, audit, sustainment, and retirement?

### Essential definitions

- A **baseline** is a formally reviewed and agreed configuration definition at a stated time, established for a stated decision or control purpose, and thereafter changed only through its authorized control process.
- A **baseline manifest** identifies the controlled artifacts, versions, relationships, provenance, scope, effectivity, approval, and authoritative locations that constitute the baseline. A folder, branch, tag, or release name alone is not a manifest.
- **Baseline establishment** is the decision that specified content satisfies declared entry criteria and becomes the authorized reference for later work or comparison. It does not prove perfection.
- **Baseline control** preserves the established state and permits only authorized changes with impact analysis, implementation evidence, status accounting, and verification.
- **Effectivity** identifies the dates, versions, variants, serials, lots, sites, environments, customers, contracts, modes, or operational instances to which a baseline or change applies.
- **Current baseline** means current for an explicitly named scope and decision. Several valid baselines can coexist for different products, sites, contracts, or lifecycle purposes.
- **As-designed**, **as-built**, **as-tested**, **as-delivered**, **as-deployed**, and **as-maintained** records describe distinct actual or intended views. None should silently overwrite another.
- **Supersession** establishes a successor and the conditions under which it replaces an earlier baseline. Superseded does not necessarily mean disposable.
- A **deviation or waiver** authorizes a bounded departure under defined terms; it does not silently rewrite the baseline.
- **Reconciliation** compares baseline definition, approved changes, and observed actual state, then dispositions every missing, extra, mismatched, unknown, or unapplied item.

### Central model, mechanism, or theorem

Represent baseline $B_k$ as

$$
B_k=(p, M_k, R_k, E_k, A_k, T_k, S_k),
$$

where $p$ is purpose, $M$ the immutable content manifest, $R$ typed relationships, $E$ effectivity, $A$ authority and approvals, $T$ establishment time, and $S$ authoritative storage/provenance. A successor is legitimate only through a controlled transition

$$
B_k \xrightarrow[\alpha,\,I,\,V,\,Q]{\Delta} B_{k+1},
$$

where $\Delta$ is the exact change set, $\alpha$ proper authority, $I$ impact analysis, $V$ verified implementation, and $Q$ reconciliation of affected actual configurations. A new tag without this evidence is only a label.

### Critical invariants

- Every baseline states its decision purpose, scope, content, authority, establishment criteria, effective point, and change path.
- Every manifest entry has stable identity, exact version or digest where appropriate, authoritative source, owner, relationships, and retention expectations.
- Approval records identify what was reviewed, by whom, under which role, against which criteria, with open conditions and dissent visible.
- Baseline establishment freezes the reference; corrections are controlled changes or clearly recorded administrative amendments, never silent edits.
- Effectivity distinguishes design families from physical instances and global releases from site, cohort, contract, or environment applicability.
- Requirements, interfaces, design, code, dependencies, data/schema, infrastructure, procedures, test assets, evidence, production, operations, suppliers, and support products are included when decision-relevant.
- Baseline types and review names are tailored to the organization and acquisition model; a NASA taxonomy is useful context, not a universal mandate.
- Approved definition, authorized changes, and actual product state are reconciled before evidence is transferred or readiness is claimed.
- A change is not closed merely because it was approved, merged, manufactured, or deployed; its full effectivity and verification must be accounted for.
- Deviations and waivers preserve the baseline, bounded applicability, risk acceptance, expiration, compensating controls, and closure conditions.
- Superseded baselines remain retrievable for rollback, incident reconstruction, certification, contractual evidence, field support, and records retention as required.
- Mutable references, undocumented tool state, inaccessible supplier data, and unrecoverable dependencies cannot be the sole basis of a durable baseline.

### Common failures

Common failures include calling a repository tag a baseline; approving a document list without exact revisions; silently replacing files under an approved link; assuming one “current” baseline across variants and sites; omitting toolchains, schemas, policy, data, procedures, suppliers, or test configuration; confusing a requirements baseline with an as-built product; closing a change while offline units remain old; treating waivers as baseline edits; losing conditions and dissent from review minutes; allowing an emergency deployment to become the new baseline automatically; copying evidence to a successor without delta analysis; retaining artifacts but not the means or rights to interpret them; and auditing a baseline against another stale declaration instead of observed reality.

### Compact example

A service baseline contains six exact manifest entries. A proposed candidate changes the application and schema, but only the application change is authorized. Exact comparison reports one unauthorized difference and rejects establishment. After the schema is restored, all entries agree with the authorized candidate and the candidate becomes eligible for governance approval. The synthetic check proves declared-string consistency only; it does not prove artifact provenance, semantic compatibility, correct deployment, or proper authority.

### Connections

Baseline management joins configuration management, requirements, architecture, interfaces, decision gates, technical data, change impact, build and supply provenance, verification and validation, operations, security, incident recovery, certification, maintenance, fleet management, and retirement.

## Governing Question

Can a decision-maker answer, without reconstructing history from memory, exactly what definition was approved, what actual configuration was assessed, which instances it covers, what has changed since, and whether the evidence remains valid?

A baseline is an epistemic and governance boundary. It gives later comparisons a stable reference and gives authorized people a shared object of decision. Stability does not mean immobility: systems must evolve. It means that evolution is expressed as an explicit, reviewable transition rather than a silent mutation of the reference.

## Why This Matters

Without controlled baselines, teams cannot reliably perform impact analysis because the “before” state moves. Verification evidence can be attached to the wrong build. Suppliers may manufacture against different revisions. Operators may recover to an image whose database, policy, or runbook is incompatible. Certification claims can outlive the configuration they actually assessed. A decision gate can appear complete while reviewers each saw different artifacts.

NASA's Configuration Management guidance describes baselines as agreed descriptions of configuration-item attributes at a point in time and makes baseline establishment part of configuration identification. It also connects configuration change management, status accounting, and configuration verification. NASA describes functional, allocated, product, and as-deployed baselines for its context. Those names illuminate progressively different decision needs, but another enterprise may organize baselines around contracts, product lines, releases, safety cases, regulated submissions, or continuous service operations.

NIST SP 800-128 treats baseline configuration as part of security-focused configuration management and connects change control with security impact analysis, testing, approval, implementation, and monitoring. Its scope and terminology should be tailored outside federal information systems. The durable principle is broader: an approved secure state must be sufficiently exact to compare with proposed and observed states.

Baselines are expensive when their scope is vague or every edit demands the same authority. They are dangerous when reduced to ceremony. Proportionate baseline management puts high rigor around consequential decision boundaries while automating exact identity, comparison, provenance, and status wherever possible.

## Prerequisites and Retrieval

Before establishing or auditing a baseline, retrieve:

1. the decision the baseline supports, including stakeholders, accountable authority, lifecycle context, risk, contractual/regulatory constraints, and required longevity;
2. the configuration-management plan, baseline types, selection rules, entry/exit criteria, control thresholds, board charters, emergency paths, audit rules, tools, repositories, access, and records policy;
3. product/system breakdown, configuration-item list, ownership, variants, serials/lots, sites, environments, suppliers, external services, operational modes, and retirement responsibilities;
4. authoritative requirements, architectures, interface definitions, analyses, models, drawings, specifications, source, build definitions, dependencies, generated artifacts, infrastructure, schema/data, policies, procedures, training, facilities, and support information;
5. manifest fields and identity rules, including artifact ID, version/revision/digest, source, relationship, provenance, owner, status, effectivity, license/rights, sensitivity, retention, and retrieval test;
6. establishment evidence: review package, notices, criteria, attendees and roles, approvals, conditions, dissent, open actions, waivers/deviations, date/time, and signed or otherwise protected decision record;
7. as-designed, procured, built, tested, delivered, deployed, operated, maintained, repaired, and retired records plus the evidence configuration for each consequential result;
8. proposed and approved changes with before/after state, affected baselines and instances, impact, authority, implementation plan, verification/validation, rollout, rollback, status, and closure evidence;
9. baseline relationships: derives-from, allocates, implements, interfaces-with, built-from, tested-as, delivered-as, deployed-as, supersedes, branches-from, and evidence-for;
10. observed-state mechanisms such as inventory, product inspection, BOM/SBOM, signed manifests, queries, discovery, attestation, calibration, build records, deployment records, supplier certificates, and maintenance logs;
11. measures and exceptions: stale baselines, unresolved review actions, unauthorized drift, missing provenance, incomplete effectivity, unimplemented changes, expired waivers, inaccessible artifacts, and restoration failures;
12. historical recovery needs, including incident and legal holds, certification, customer support, field populations, repair, rollback, archival formats, decryption/key custody, tool availability, and rights to reproduce supplier content.

Choose one consequential claim and perform a **baseline thread**: identify its governing baseline, exact artifacts and relationships, approval, applicable actual instance, implemented changes, evidence configuration, deviations, and successor. Label every inferred link and every inaccessible artifact.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish a controlled baseline from a snapshot, branch, tag, release, document set, backup, and current actual state;
2. define baseline purpose, scope, manifest, authority, entry criteria, effectivity, provenance, and retention;
3. tailor baseline types and timing to decisions rather than mechanically copying a lifecycle taxonomy;
4. establish a baseline through evidence-bearing review and protect it against silent mutation;
5. relate requirements, allocated/design, product, release, deployed, operational, evidence, and recovery baselines without conflating them;
6. analyze and authorize changes against an immutable before-state;
7. manage variants, fleets, sites, suppliers, mixed-version transitions, deviations, waivers, and emergency configurations;
8. reconcile intended baseline content with as-built, as-tested, as-deployed, and as-maintained reality;
9. evaluate evidence transfer, supersession, rollback, archival durability, and baseline retirement;
10. design automation and measures that strengthen rather than simulate configuration control.

## Core Exposition

**Begin with a decision, not a directory.** A baseline exists to anchor an agreement or later comparison: requirements commitment, interface coordination, design release, supplier build, verification readiness, deployment authorization, safety case, operational recovery, or retirement. Name the consumers and decisions first. Otherwise the baseline either collects everything indiscriminately or omits the information that later determines correctness.

**Define the baseline contract.** Record purpose, owner, approving authority, scope, entry criteria, manifest schema, required evidence, review method, effective event/time, control class, allowed amendment process, access, retention, and supersession rules. State what the baseline does not claim. A requirements baseline may support allocation without describing an as-built product; a deployment baseline may describe authorized runtime state without proving mission effectiveness.

**Use a content-addressable manifest where feasible.** Each entry should identify a logical item and exact representation. Digests are strong detectors of byte differences but do not prove trusted origin, semantic equivalence, safety, or completeness. Hardware may require design revision, serial/lot, process, material, firmware, calibration, and supplier provenance rather than a file hash. Services need source and binaries/images plus dependencies, build environment, schemas, infrastructure, policy, runtime configuration, and external compatibility assumptions.

**Model relationships, not only inventory.** A pile of correct files can still describe an incoherent system. The manifest should express allocation, composition, generation, dependency, interface, compatibility, deployment, and evidence links. Define precedence when sources disagree. Record optional and conditional items. Validate that relationship endpoints exist and that the graph is meaningful for the decision.

**Separate labels from identity.** A human label such as `release-12` helps communication. Exact identity may require immutable artifact digests, document revisions, signed records, supplier lot, schema migration state, and environment configuration. Protect label-to-manifest binding. If a mutable tag can move after approval, preserve the resolved commit or digest and audit tag movement rather than trusting the label.

**Tailor baseline families.** NASA's functional, allocated, product, and as-deployed baselines provide one coherent pattern: top-level performance, allocated configuration-item requirements, production/support definition, then deployed state. Use that taxonomy when it fits the governing environment. A continuously delivered service might instead establish product intent, platform compatibility, release candidate, authorized deployment, and recovery baselines. A regulated device may organize design inputs, design outputs, manufacturing, device history, and submission evidence. The names matter less than explicit purpose and relationships.

**Establish through a real decision.** Assemble the exact review package before review starts. Freeze or uniquely identify it. Evaluate declared criteria, not presentation quality. Record reviewer roles, quorum or authority rules, evidence considered, anomalies, assumptions, conditions, dissent, actions, and disposition. Approval must bind to the reviewed manifest. If material content changes after review, determine whether targeted concurrence or a new review is required; do not backfill approval onto unseen content.

**Keep open work visible.** A baseline can be established with bounded conditions only when policy and consequence allow. Each condition needs owner, due date or event, closure evidence, impact, and authority. A large unresolved requirement or failed safety test cannot be disguised as an “action item.” Define thresholds that require withholding establishment.

**Protect the established reference.** Make artifacts and metadata immutable or tamper-evident according to consequence. Restrict write authority; preserve audit logs, signatures, clocks, and backups; test retrieval. Administrative corrections such as a misspelled description must follow a defined amendment path that preserves original and correction. Content changes become proposed successors or controlled changes.

**Control change as a transition.** Start from exact $B_k$. Describe proposed delta, rationale, alternatives, affected requirements/interfaces/risks, actual instances, suppliers, data, operations, evidence, cost/schedule, transition, rollback, training, maintenance, and retirement. Identify the approval authority for each affected baseline and interface. Approval authorizes a bounded change; it does not establish that implementation occurred or succeeded.

**Preserve effectivity.** A change may apply to new production after a date, specified serials, one customer, selected sites, a software cohort, or a particular contract. Store effectivity as queryable structured data. During rollout, old and new configurations can both be authorized under defined compatibility and duration. Report pending, unreachable, failed, rolled-back, exempt, and unknown instances rather than replacing them with a global percent complete.

**Reconcile definition with reality.** Compare baseline and approved deltas to as-built/actual observation. Determine missing, extra, mismatched, unknown, duplicated, and incorrectly related items. Investigate whether the definition, observation, product, or authorization is wrong. Do not automatically force actual state to a possibly stale baseline; a safe observed correction or emergency change may need to become a controlled successor.

**Bind evidence to configuration.** Verification and validation results identify the tested article, software/build, dependencies, data/schema, infrastructure, procedures, tools, environment, operators, calibration, and acceptance criteria as relevant. When a successor is proposed, create a delta-to-evidence matrix. Reuse unchanged reasoning only with justified equivalence; rerun configuration-sensitive evidence. “Only configuration changed” is not a rationale because configuration can change behavior.

**Treat deviations and waivers as overlays.** Preserve the unchanged baseline, requirement or definition, authorized departure, rationale, risk, approvers, compensating controls, exact effectivity, duration, monitoring, and closure. Prevent an expired waiver from remaining embedded in actual state. Repeated waivers may reveal that the baseline or requirement needs deliberate revision, but repetition is not implicit change authorization.

**Manage emergency state explicitly.** Predefine triggers, bounded authority, minimum identity/evidence, rollback, monitoring, communication, and reconciliation deadlines. Capture prechange and changed configurations during the event. After stabilization, decide to revert, retain through normal approval, or replace with a permanent correction. An incident commander's permission to mitigate is not necessarily authority to establish the enduring baseline.

**Coordinate suppliers and shared interfaces.** Contract for configuration data, notification thresholds, approval/concurrence, lot/serial traceability, preservation, audit access, tool formats, rights, and obsolescence. A supplier release can be internally controlled yet incompatible with the system baseline. Shared interface changes need all affected authorities and explicit compatibility/effectivity.

**Design recovery baselines.** A rollback point must include stateful dependencies and instructions, not merely an old binary. Identify database/schema/data compatibility, secrets or key references, infrastructure, policy, external contracts, stored messages, feature flags, and runbooks. Test restoration in a representative environment. Some physical changes are irreversible, so recovery may require a forward correction, spare substitution, or safe degraded configuration.

**Supersede without erasing history.** A successor record states its parent(s), exact delta, establishment evidence, effective scope, coexistence rules, migration status, and retirement conditions. Branching may be legitimate for product variants or customers; record merge or divergence policy. Keep older baselines accessible for field units, incident reconstruction, evidence interpretation, contractual obligations, and rollback until retention/disposition authority permits removal.

**Audit the system of control.** Sample from both directions: baseline to product and product to baseline. Inspect manifest completeness, immutable binding, authority, open conditions, change state, effectivity, actual reconciliation, evidence applicability, waivers, supplier content, retrieval, and restoration. Also audit the tools, identities, automation, signing, databases, and access that generate baseline records.

**Measure outcomes and latency together.** Track baselines with overdue conditions, stale or inaccessible entries, unapproved mutations, unexplained drift, changes lacking effectivity, implementation-to-reconciliation time, wrong-baseline escapes, evidence invalidations, expired waivers, and restoration success. Normalize by population and criticality. Zero findings can mean excellent control or no observation; rapid board throughput can mean efficient automation or shallow review.

The following fixture tests a deliberately narrow declared-manifest gate.

<!-- bijux-verify: {"id":"baseline-transition-fixture","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"baseline_entries=6\nauthorized_delta_entries=1\ncandidate_changed_entries=2\nunauthorized_differences=data_schema\ninitial_establishment=reject_unauthorized_difference\ncorrected_changed_entries=1\ncorrected_unauthorized_differences=0\ncorrected_establishment=eligible_for_governance_approval\noriginal_baseline_unchanged=true\nstatus=synthetic_baseline_transition_consistent\nevidence=declared_exact_string_comparison_only\n","stderr":""}} -->
```python
baseline = {
    "application": "app@sha256:111",
    "dependencies": "lock@sha256:222",
    "data_schema": "schema@17",
    "infrastructure": "infra@sha256:333",
    "policy": "policy@9",
    "runbook": "runbook@12",
}
authorized_delta = {"application": "app@sha256:444"}
candidate = dict(baseline)
candidate.update(authorized_delta)
candidate["data_schema"] = "schema@18"

def changed(before, after):
    keys = sorted(set(before) | set(after))
    return [key for key in keys if before.get(key) != after.get(key)]

candidate_changes = changed(baseline, candidate)
unauthorized = [key for key in candidate_changes if key not in authorized_delta]
print(f"baseline_entries={len(baseline)}")
print(f"authorized_delta_entries={len(authorized_delta)}")
print(f"candidate_changed_entries={len(candidate_changes)}")
print("unauthorized_differences=" + ",".join(unauthorized))
print("initial_establishment=reject_unauthorized_difference")

candidate["data_schema"] = baseline["data_schema"]
corrected_changes = changed(baseline, candidate)
corrected_unauthorized = [key for key in corrected_changes if key not in authorized_delta]
print(f"corrected_changed_entries={len(corrected_changes)}")
print(f"corrected_unauthorized_differences={len(corrected_unauthorized)}")
print("corrected_establishment=eligible_for_governance_approval")
print(f"original_baseline_unchanged={str(baseline['application'].endswith('111')).lower()}")
print("status=synthetic_baseline_transition_consistent")
print("evidence=declared_exact_string_comparison_only")
```

This fixture trusts the dictionaries and the declared authorization. It does not authenticate artifacts or approvers, verify signatures or provenance, discover actual state, analyze semantics, test compatibility or behavior, establish effectivity, or prove that governance should approve the corrected candidate.

## Definitions and Notation

Let baseline $B=(p,M,R,E,A,T,S)$ contain purpose $p$, manifest $M$, relationships $R$, effectivity $E$, authority $A$, establishment time $T$, and storage/provenance $S$. Manifest entry $m=(id,rev,digest,source,owner,state)$ uses fields appropriate to its medium; a digest may be unavailable or insufficient for a physical item.

Let actual configuration $\widehat{C}_{t,x}$ be observed at time $t$ for instance/site $x$. Let authorized changes active for that effectivity be $\Delta^*_{t,x}$. Expected state is a domain-aware application $C^*_{t,x}=apply(B,\Delta^*_{t,x})$, not necessarily textual overlay.

Define discrepancy set

$$
D_{t,x}=compare(C^*_{t,x},\widehat{C}_{t,x}),
$$

partitioned into missing, extra, mismatched, unknown, and relationship discrepancies. A naive coverage $c=m/n$ reports matching entries but cannot weight criticality, completeness, semantic correctness, provenance, or observational trust.

Supersession relation $B_j \prec_E B_k$ means $B_k$ replaces $B_j$ only for effectivity $E$. Outside $E$, the older baseline may remain current. This prevents a single global “latest” ordering from erasing valid variants and field populations.

## Mechanisms, Invariants, or Proof Structure

A defensible baseline argument follows this chain:

1. state the decision purpose, system/product boundary, effectivity dimensions, risks, stakeholders, and authority;
2. select configuration items and controlled information sufficient for that decision;
3. build an exact manifest with typed relationships, provenance, authoritative sources, retention, and retrieval;
4. define establishment criteria and freeze the review object;
5. evaluate technical completeness, consistency, risk, evidence, conditions, interfaces, actual-state relevance, and downstream consequences;
6. bind the authorized decision to the reviewed manifest and preserve dissent, conditions, and open work;
7. prevent silent mutation and route proposed deltas through proportionate impact analysis and authority;
8. implement approved changes across their exact effectivity and capture as-built/deployed/maintained state;
9. verify change behavior and reconcile actual configuration to expected configuration;
10. establish a successor when its criteria are met, preserve parentage and coexistence, and retain earlier baselines according to support and records needs.

The proof obligation is bounded: it supports the named decision for the named configuration and evidence. It does not establish universal system correctness. If content identity, authority, effectivity, actual-state observation, or evidence binding is missing, the conclusion must be weakened or withheld.

## Alternatives and Trade-Offs

**Document baselines versus model/graph baselines.** Document sets are portable and reviewable but relationships can be implicit. Graph-backed baselines support queries and impact analysis but require schema governance and durable export. A common pattern is an immutable manifest plus referenced human-readable and machine-readable artifacts.

**Periodic establishment versus continuous baselining.** Periodic gates concentrate multidisciplinary review and suit contractual or irreversible decisions. Continuous delivery can generate immutable candidate manifests and automated evidence for every build, then apply stronger human authority only at risk thresholds. Continuous creation of snapshots is not continuous approval.

**Central board versus delegated control.** A central board sees cross-system effects but can become a bottleneck. Delegated authorities accelerate bounded low-risk changes but require explicit scope, automated policy, escalation, audit, and interface ownership. Hybrid control usually matches varied consequences better.

**Monolithic versus federated manifests.** One manifest simplifies discovery but can be huge and cross ownership boundaries. Federated signed manifests scale ownership and supplier/platform autonomy but need stable references, trust, compatibility, availability, and coordinated supersession.

**Exact replication versus sufficient preservation.** Full environments maximize reconstruction but may be expensive, insecure, licensed, or technically impossible. Preservation can combine source, artifacts, dependency archives, virtualized tools, schemas, representative data, procedures, and attestations. State the residual uncertainty and test retrieval.

**Rollback versus forward recovery.** Software rollback is attractive when state compatibility is preserved. Database changes, physical rework, consumed materials, security exposure, or external migrations may make reversal unsafe. Baselines should support the actual recovery strategy rather than promise reversible change universally.

## Failure Modes and Misconceptions

- **“The tag is the baseline.”** A tag may locate one source state but omit build, dependencies, configuration, data, approvals, evidence, and effectivity; mutable tags are especially weak.
- **“Approved means correct.”** Approval means authorized acceptance against stated criteria and known evidence. Unknown defects and bounded conditions may remain.
- **“Current is singular.”** Multiple valid variants, contracts, sites, cohorts, field units, and maintenance states can coexist.
- **“The document baseline is the product.”** Definition and actual realization are different objects requiring reconciliation.
- **“Every baseline must use the same taxonomy.”** Baseline families should match decisions and governance; borrowed names without purpose create ceremony.
- **“A hash proves trust.”** It detects byte equality to a named value. It does not prove trusted origin, completeness, semantics, execution, or approval.
- **“An approved change updates the baseline.”** Approval, implementation, verification, actual reconciliation, and successor establishment are distinct states.
- **“A waiver changes the requirement.”** It authorizes a bounded departure while preserving the original requirement/baseline unless formal change occurs.
- **“Deployment complete means effectivity complete.”** Offline units, spares, supplier stock, data replicas, customer installations, and disaster-recovery environments may remain old.
- **“Rollback means redeploy the old binary.”** Stateful data, schemas, messages, policy, keys, infrastructure, and external contracts can prevent safe restoration.
- **“Evidence transfers because most files are unchanged.”** Applicability depends on the proposition and changed causal pathways, not file-count percentage.
- **“Archive means recoverable.”** Missing tools, formats, keys, rights, metadata, or knowledge can make retained bits unusable.

## Worked Examples

### Example 1

A review package for a flight-control requirement baseline links to “current” documents. One interface document changes during review. Reviewers therefore did not assess one stable object. The team resolves exact revisions, reruns affected review, records conditions, and binds approval to an immutable manifest. The conclusion is limited to requirements agreement, not product readiness.

### Example 2

A manufacturer releases a product baseline with drawings, BOM, material/process specifications, work instructions, acceptance tests, and approved suppliers. A supplier later moves heat treatment to another facility under the same part number. The proposed change triggers material/process, reliability, qualification, contractual, lot-effectivity, and field-impact analysis. Catalog identity alone cannot preserve baseline equivalence.

### Example 3

A web service repository is tagged `2026.08`, but the running service also depends on a container base, lockfile, schema 18, infrastructure definition, authorization policy, feature flags, and reference data. The deployment baseline records all dimensions and the site/cohort effectivity. A source tag remains a useful entry, not the whole baseline.

### Example 4

Three hospitals run two authorized device configurations because one site has not completed a sensor retrofit. The successor baseline supersedes the older one only for listed serials at two sites. Status accounting preserves the third site's valid older configuration, its compensating inspection, due date, spares, and eventual migration.

### Example 5

A safety analysis was approved against design baseline B7. B8 changes a mounting bracket and maintenance access but not nominal function. Delta analysis checks load paths, environmental qualification, human maintenance, hazards, inspection, drawings, spares, and training. Some functional test evidence transfers; structural and maintenance evidence is updated. “No requirement changed” would have missed relevant evidence.

### Example 6

A critical vulnerability requires immediate policy restriction and service patch. Emergency authority records the prechange configuration, exact artifacts, affected regions, limited approvals, monitoring, and rollback. After stabilization, the team performs complete impact/regression, reconciles all regions, removes temporary access, and establishes a normal successor. The emergency deployment never silently becomes the enduring baseline.

### Example 7

A release candidate differs from its parent in application and database schema, but authorization covers only the application. The fixture's exact comparison rejects it. Restoring the schema makes it eligible for approval, not approved: reviewers still need provenance, test evidence, compatibility, effectivity, and authority.

### Example 8

An operator reports that the approved infrastructure baseline declares three instances while discovery finds four. The extra instance served traffic during an incident. The team preserves forensic evidence and assesses safety, security, data, capacity, and cost before disposition. Blindly deleting drift could harm service; silently changing the baseline would erase an unauthorized action.

### Example 9

A recovery drill can fetch an old application image but cannot restore its schema, signing certificate chain, dependency repository, or vendor-licensed decoder. The nominal archive is not a recovery baseline. The team defines lawful retained dependencies, key/verification custody, schema snapshots, test data, instructions, and periodic restoration evidence, while excluding unnecessary secrets and personal data.

### Example 10

A product line retires baseline P4 after the last supported unit is dismantled. Before disposition, it confirms no spares, contracts, certification records, incident holds, training systems, or downstream variants still depend on P4. Required manifests and evidence move to durable archival formats; obsolete credentials and deployable endpoints are revoked. Retirement is a controlled decision, not deletion by age.

## Cross-Program Connections

- **Platform engineering:** golden images, infrastructure, policies, cluster add-ons, deployment manifests, drift, promotion, and recovery need immutable identity plus observed-state reconciliation.
- **API and service engineering:** schema/protocol versions, consumer-provider compatibility, rollout cohorts, feature flags, data migrations, and endpoint retirement determine baseline effectivity.
- **Data engineering:** pipeline code, schemas, quality rules, reference data, lineage, orchestration, storage, and historical datasets are necessary for reproducible data-product baselines.
- **Object-oriented programming:** packages, class/interface contracts, generated code, binary compatibility, build tools, and dependency graphs bind source design to released artifacts.
- **Functional programming:** module types, pure-core assumptions, effect runtimes, compiler settings, lockfiles, algebraic laws, and property-test evidence form configuration-sensitive claims.
- **Security engineering:** hardened configurations, provenance, SBOMs, exceptions, impact analysis, authorization, monitoring, incident changes, and restoration are baseline concerns.
- **Verification and validation:** every result has an evidence configuration; successor claims require explicit equivalence and retest decisions.
- **Operations and sustainment:** fleet/site actual state, maintenance, repairs, spares, calibration, recovery, obsolescence, and retirement determine which baseline is truly applicable.

## References

1. NASA, [Configuration Management, Systems Engineering Handbook section 6.5](https://www.nasa.gov/reference/6-5-configuration-management/), accessed 2026-08-31.
2. NASA, [Configuration Management Plan Outline, Appendix M](https://www.nasa.gov/reference/appendix-m-cm-plan-outline/), accessed 2026-08-31.
3. NIST, [SP 800-128, Guide for Security-Focused Configuration Management of Information Systems](https://csrc.nist.gov/pubs/sp/800/128/upd1/final), updated 2019.
4. NASA, [Technical Data Management, Systems Engineering Handbook section 6.6](https://www.nasa.gov/reference/6-6-technical-data-management/), accessed 2026-08-31.
5. NASA, [Requirements Management, Systems Engineering Handbook section 6.2](https://www.nasa.gov/reference/6-2-requirements-management/), accessed 2026-08-31.
6. NASA, [Interface Management, Systems Engineering Handbook section 6.3](https://www.nasa.gov/reference/6-3-interface-management/), accessed 2026-08-31.
7. NASA, [Technical Assessment, Systems Engineering Handbook section 6.7](https://www.nasa.gov/reference/6-7-technical-assessment/), accessed 2026-08-31.
8. NASA, [Product Verification, Systems Engineering Handbook section 5.3](https://www.nasa.gov/reference/5-3-product-verification/), accessed 2026-08-31.
9. NASA, [Systems Engineering in Phase E, Appendix T](https://www.nasa.gov/reference/appendix-t-systems-engineering-in-phase-e/), accessed 2026-08-31.
10. NASA, [NPR 7123.1B, NASA Systems Engineering Processes and Requirements, Change 4](https://nodis3.gsfc.nasa.gov/displayAll.cfm?Internal_ID=N_PR_7123_001B_&page_name=ALL), effective 2020.

## Exercises

### Exercise 1

Design a baseline family and manifest for an autonomous warehouse system spanning robots, fleet services, maps/data, cloud infrastructure, operators, facilities, suppliers, and safety evidence.

### Exercise 2

An authorized deployment baseline contains 15 required entries. Observation finds 12 exact matches, one missing item, one mismatched item, and one extra item. Compute naive required-entry coverage and define the decision, evidence limits, and disposition workflow.

### Exercise 3

Design establishment and change control for a multi-organization interface baseline whose provider and three consumers deploy on different cadences.

### Exercise 4

Determine whether verification evidence from baseline B12 can support B13 after changes to source, compiler, dependency, schema, infrastructure, procedure, and one sensor supplier lot.

### Exercise 5

Create a recovery and retirement strategy for a ten-year-old regulated service whose artifacts exist but whose build service, signing keys, database engine, and vendor tool are near end of support.

## Answers to the Exercises

### Answer 1

Define baseline purposes rather than one universal snapshot. A system-intent baseline contains mission, safety/security, top-level requirements, operational concepts, interfaces, fleet behavior, and verification strategy. Robot product baselines contain mechanical/electrical design, BOM and approved suppliers, firmware, calibration, acceptance, manufacturing/repair instructions, and serialized effectivity. A service-release baseline contains source, build/toolchain, dependencies, signed artifacts, schemas, APIs, infrastructure, identity/policy, feature configuration, maps/reference data, observability, runbooks, training, and evidence. A site operational baseline binds facility layout, geofences, chargers, networks, robot serials, service release, operator authorization, local procedures, and recovery configuration.

Use hierarchical manifests with immutable IDs/digests where meaningful and physical revision/serial/lot/process records where hashes are insufficient. Relationships include installed-on, calibrated-with, built-from, depends-on, deployed-at, compatible-with, trained-for, and evidence-for. Authority includes product, facility, safety, security, data, operations, supplier, and interface owners according to impact. Effectivity identifies robot serials, site, fleet cohort, time, mode, and supplier lots.

Establishment criteria require resolved critical hazards/interfaces, complete provenance, representative integrated tests, site acceptance, trained operators, recovery evidence, and bounded open conditions. Observed inventory and service discovery reconcile each site. Changes route by consequence; emergency paths preserve exact identity and later reconciliation. Baselines and evidence remain available for incidents, maintenance, spares, customer obligations, and battery/electronics disposal. This design does not claim every low-level source file needs board approval: lower-level signed manifests can be governed by preapproved automation.

### Answer 2

Required-entry exact-match coverage is $12/15=80\%$. The extra item is not in the denominator, but it remains a discrepancy. This percentage cannot justify deployment because criticality, semantic compatibility, provenance, observation trust, relationship correctness, and behavior are unknown. Report all four categories: 12 matching, 1 missing, 1 mismatched, and 1 extra.

Hold configuration-dependent authorization unless a bounded policy explicitly permits the discrepancies. First verify observation completeness, clocks, identity, source, and effectivity. For the missing item, decide whether it is absent, inaccessible, renamed, or outside scope. For the mismatch, compare intended/actual content, approval history, compatibility, and evidence. For the extra, preserve operational or forensic evidence and determine whether it is unauthorized, required but omitted from the baseline, or a discovery error.

Assess requirements, interfaces, safety/security, data, operations, rollback, and evidence applicability. Correct actual state, correct the baseline through authorized change, or approve a bounded deviation with compensating controls and expiration. Rediscover and verify. Even 15/15 plus removal of the extra would prove agreement only under the observation/comparison method, not product correctness.

### Answer 3

Define one authoritative interface manifest with protocol/schema, semantics, units, timing, errors, security, compatibility, test suite, examples, ownership, and exact version/digest. Record provider and each consumer's supported versions and deployment populations. The interface authority includes empowered representatives of provider and affected consumers; local ownership cannot unilaterally change shared meaning.

For establishment, freeze the review object, execute contract/conformance and representative integration evidence, resolve semantic conflicts, record conditions, and bind approvals to the manifest. Model effectivity by provider release, consumer version, site/customer, and time. Define supported coexistence and deprecation windows rather than assuming simultaneous deployment.

Every proposal supplies before/after semantics, compatibility matrix, consumer impact, migration, data transformation, security, monitoring, rollback, tests, documentation, and retirement. Additive syntax is not automatically backward compatible if semantics, limits, defaults, or authorization change. Deploy canaries where appropriate, status account every consumer population, monitor old/new behavior, and close only after affected effectivity is verified or explicitly waived. Supersede the interface baseline with parentage while retaining older versions until no supported consumer or evidence obligation depends on them.

### Answer 4

Build a delta-to-claim matrix rather than calculate unchanged-file percentage. Source changes map to requirements, hazards, interfaces, behavior, and tests. Compiler changes can affect generated code, ABI, timing, optimization, and numerical results. Dependencies affect behavior, licensing, vulnerabilities, and failure modes. Schema changes affect migration, compatibility, stored data, rollback, and evidence fixtures. Infrastructure affects identity, topology, resources, timing, resilience, and observability. Procedure changes affect human performance and repeatability. The supplier lot requires material/process/site, acceptance, calibration, reliability, interchangeability, and traceability analysis.

Preserve B12 tests, fixtures, trace links, and reasoning as inputs. Establish exact B13 provenance and classify each claim as unaffected with rationale, analytically updated, or requiring new execution. Re-run changed-component, interface, regression, schema migration/rollback, infrastructure failure/recovery, procedural usability, supplier acceptance/qualification, and integrated system evidence according to risk. Check interactions—for example compiler timing with sensor behavior or schema migration with rollback.

Evidence transfer is therefore proposition-specific. B12 evidence remains historical evidence for B12; cited parts may support B13 only with documented equivalence and authority. Resolve anomalies, update safety/security and operational records, bind new results to exact B13 test configurations, and state residual limits. A blanket declaration that B13 is verified because most content is unchanged is unsupported.

### Answer 5

Inventory exact source, generated artifacts, dependencies, schemas/data formats, infrastructure, policy, procedures, evidence, tool licenses, contractual rights, supported field/customer configurations, and legal/records obligations. Test retrieval now. Distinguish goals: incident interpretation may need readable records, rollback needs runnable artifacts and compatible state, while future modification may need a reproducible build environment.

Create immutable manifests and lawful archives for source, binaries/images, dependency packages, database dumps or representative privacy-safe data, migrations, vendor inputs/outputs, verification tools, manuals, and checksums/signatures. Preserve certificate-chain verification information without retaining unnecessary active private keys. Where possible, containerize or virtualize the build and database environment, export vendor formats to durable neutral representations, document known semantic loss, and obtain escrow or replacement rights. Establish new signing and trust procedures for rebuilt artifacts rather than pretending expired keys remain operationally valid.

Run restoration and interpretation drills in isolated representative infrastructure. Verify schema migration and recovery, external interface substitutes, clock/certificate assumptions, and operator procedures. If full reproduction is impossible, retain verified released binaries plus attested build history and explicitly limit future claims. Plan supported-customer migration, final data export, credential revocation, endpoint shutdown, vendor-tool disposition, and retention/legal holds. Retire only after no field, contract, incident, certification, or evidence dependency remains; preserve the minimal durable record and securely dispose of sensitive or licensed material under authority.
