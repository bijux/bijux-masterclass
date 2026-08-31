---
module_id: SYSENG-085
program: Systems Engineering
level: 2
module_number: 85
title: Change Impact Analysis
status: complete
last_verified: 2026-08-31
---

# Change Impact Analysis

## One-Page Review

### Governing question

Before authorizing a change, can the organization identify what may be affected, why and through which dependency, how serious and uncertain each consequence is, which evidence and decisions become invalid or conditional, and what implementation, verification, transition, monitoring, and recovery are required across the full effectivity?

### Essential definitions

- A **change** is a proposed or realized difference between identified before and after states; intent, implementation, and observed outcome are distinct.
- **Change impact analysis (CIA)** is the structured discovery, evaluation, and communication of direct, indirect, interacting, lifecycle, and evidence consequences of a proposed or actual change.
- An **impact path** is a typed causal or dependency chain from a changed item to an affected claim, item, interface, stakeholder, instance, activity, or outcome.
- An **impact candidate** is something found by traceability, dependency analysis, expertise, history, observation, or scenario analysis that requires disposition; discovery alone does not prove material impact.
- **Effectivity** identifies the variants, serials, lots, versions, sites, environments, customers, contracts, modes, dates, or cohorts to which the change and its consequences apply.
- **Evidence invalidation** means prior evidence no longer supports its original claim for the changed configuration without new execution, analysis, or justified equivalence.
- **No-impact rationale** is an evidence-bearing argument explaining why a candidate is unaffected. It is not a blank cell or unchecked box.
- **Cumulative impact** is the combined consequence of several changes whose interaction differs from each change considered alone.
- **Change authority** is the role empowered to accept the change and its residual consequences for a named scope; technical analysis informs but does not replace authority.
- **Closure** requires verified implementation and disposition across effectivity, not merely approved paperwork, merged source, completed manufacture, or initial deployment.

### Central model, mechanism, or theorem

Let $G=(V,E,\tau)$ be a typed dependency graph, with nodes for requirements, design, interfaces, products, data, processes, evidence, people, suppliers, instances, and lifecycle obligations. Given change seeds $S\subseteq V$, static candidate closure is

$$
R_0=S,\qquad R_{k+1}=R_k\cup\{v\mid (u,v)\in E,\ u\in R_k,\ policy(\tau(u,v))\}.
$$

This closure is a search aid, not a completeness proof. For each candidate $v$, evaluate a record

$$
I_v=(path, consequence, severity, likelihood, uncertainty, evidence, action, owner, effectivity).
$$

Authorization is defensible only when material candidates and unknowns are dispositioned by competent authority, interactions are examined, and the transition/evidence plan matches the bounded conclusion.

### Critical invariants

- Compare exact identified before and proposed states; a vague request cannot support bounded analysis.
- Preserve change rationale, alternatives including no change, assumptions, urgency, reversibility, and expected benefit.
- Search forward from changed items to consumers and backward from affected claims to dependencies; use typed relationships rather than undifferentiated link counts.
- Analyze requirements, functions, performance, architecture, interfaces, safety, security/privacy, reliability, human work, data/models, manufacturing/supply, operations, maintenance, evidence, contracts, cost/schedule, and retirement as applicable.
- Treat the change package, enabling systems, build/test tools, procedures, training, facilities, suppliers, and migration/rollback assets as impact candidates.
- Distinguish direct, indirect, emergent, common-cause, cumulative, transitional, operational, and end-of-life consequences.
- Record evidence for both impact and no-impact conclusions; label unknown, inaccessible, stale, inferred, or disputed relationships.
- Analyze variants and actual populations by effectivity; “all systems” and “deployed” are not adequate when fleets diverge.
- Reassess prior verification, validation, safety/security, certification, and acceptance evidence claim by claim.
- Define implementation order, compatibility/coexistence, V&V, monitoring, abort/rollback, communication, records, and old-state retirement before authorization.
- Reopen analysis when scope, assumptions, dependencies, implementation, supplier information, anomaly evidence, or observed state changes.
- Closure accounts for every affected item/instance, unresolved consequence, deviation/waiver, verification result, and residual risk.

### Common failures

Common failures include analyzing only the changed file or part; searching only downstream source dependencies; trusting incomplete trace matrices; treating additive API/schema changes as automatically compatible; ignoring data already stored or in flight; omitting build tools, suppliers, procedures, training, spares, facilities, and retirement; assigning arbitrary risk numbers without calibrated evidence; counting links as severity; copying tests without checking what they prove; accepting “no impact” without rationale; reviewing changes independently when deployed together; forgetting offline sites and disaster recovery; assuming rollback is possible after state migration or physical rework; closing at merge or approval; and using automated graph reachability as a completeness certificate.

### Compact example

A synthetic dependency graph starts at `data_schema`. Typed traversal finds nine downstream candidates across migration, service API, analytics, rollback, stored data, client SDK, conformance evidence, reporting contract, and operator tooling. The result expands search scope; it does not assert that all nine are materially affected or that undiscovered dependencies do not exist. Expert disposition and configuration-specific evidence remain required.

### Connections

Change impact analysis connects baselines, configuration control, requirements traceability, architecture, interfaces, risk, decision analysis, verification/validation, safety/security, data migration, supply/manufacturing, platform deployment, operations, maintenance, certification, evidence reuse, obsolescence, and retirement.

## Governing Question

What must be reconsidered, changed, retested, communicated, monitored, preserved, or retired if the proposed difference is introduced—and what evidence bounds confidence that the search and conclusions are adequate?

The question is deliberately broader than “which files depend on this file?” Systems behave through physical, digital, informational, organizational, human, contractual, and environmental relations. The most consequential impact may be a maintenance action, expired certification assumption, supplier process, stored-data interpretation, recovery limitation, or operator workload that no compiler can discover.

## Why This Matters

A local change can have system consequences through allocation, interfaces, shared resources, timing, state, assumptions, or evidence. Increasing a battery capacity may alter mass, thermal behavior, charging, handling, transport classification, maintenance, and emergency response. Adding an optional API field may break strict consumers, signatures, cache keys, analytics, documentation, or privacy obligations. Replacing a compiler can invalidate timing evidence while source is unchanged.

NASA Configuration Management guidance describes systematic proposal, justification, evaluation, incorporation, and verification of changes. Requirements and Interface Management provide trace and coordination pathways; Technical Risk Management and Decision Analysis provide structured consequence and alternative reasoning; Technical Assessment, Product Verification, and Product Validation connect the proposed change to status and evidence. NIST SP 800-128 specifically connects configuration changes with security impact analysis, testing, approval, implementation, and monitoring for information systems. Each source has its own institutional scope, but together they reinforce an evidence-bearing lifecycle analysis rather than a clerical checklist.

CIA also prevents unnecessary work. A disciplined no-impact argument can preserve valid evidence and avoid indiscriminate regression. The goal is not maximal documentation or universal retesting. It is proportionate discovery and disposition calibrated to consequence, uncertainty, reversibility, novelty, and actual effectivity.

## Prerequisites and Retrieval

Before analyzing a change, retrieve:

1. exact before/proposed configurations, baseline IDs, change set, origin, rationale, expected benefit, urgency, alternatives/no-change case, assumptions, constraints, and responsible owner;
2. system boundary, operational concept, stakeholders, missions/services, modes/states, lifecycle context, environments, criticality, hazards/threats, laws/contracts, and decision authority;
3. requirements and traceability in both directions, including derived requirements, assumptions, rationales, allocations, acceptance criteria, verification methods, and unresolved anomalies;
4. architecture and design structures: functions, behaviors, states, resources, interfaces, dependencies, common services, failure containment, data flows, physical integration, and enabling systems;
5. configuration structures and baseline manifests for hardware, software, firmware, data/schema/models, infrastructure, policies, procedures, facilities, tools, training, suppliers, and evidence;
6. actual populations and effectivity: variants, serials/lots, releases, sites, environments, customers/contracts, cohorts, offline assets, spares, repairs, waivers, and unsupported states;
7. interface agreements, compatibility matrices, consumer/provider inventories, units/timing/errors/security, version/deprecation policy, and external coordination authority;
8. hazard analyses, threat models, privacy assessments, reliability/availability/maintainability models, human factors, environmental analyses, and accepted residual risks;
9. verification/validation records tied to exact configurations, test articles, environments, tools, data, procedures, operators, calibration, anomalies, limitations, and acceptance decisions;
10. manufacturing/supply information: BOM, materials/processes, tooling, work/inspection instructions, approved sources, subtiers, lots, lead time, obsolescence, qualification, stock, field population, and disposal;
11. operational evidence: incidents, telemetry, defects, support cases, maintenance/repair history, capacity, performance, security findings, data quality, workarounds, recovery results, and historical similar changes;
12. transition constraints: sequencing, migration, mixed-version compatibility, rollout, monitoring, rollback/forward recovery, communications, training, documentation, retention, certification, and old-state retirement.

Run a **change thread** from each seed through at least one requirement, architecture/function, interface, realizing item, build/supply path, evidence claim, actual population, operating procedure, recovery path, and retirement obligation. Record gaps rather than silently treating them as no impact.

## Learning Objectives

After completing this module, you should be able to:

1. define exact before/proposed states and distinguish intended, authorized, implemented, and observed changes;
2. build and interrogate typed dependency and trace graphs without overstating their completeness;
3. discover direct, indirect, emergent, cumulative, transitional, and lifecycle impact candidates;
4. analyze functional, performance, interface, safety/security, data, human, supply, operational, contractual, and retirement consequences;
5. assess effectivity across variants, instances, sites, releases, suppliers, customers, and mixed-version transitions;
6. create claim-level evidence invalidation and verification/validation plans;
7. reason about uncertainty, missing relationships, historical analogues, reversibility, and residual risk without false precision;
8. compare alternatives, including no change, using explicit criteria and sensitivity;
9. define implementation, monitoring, abort, rollback/forward recovery, communication, and closure evidence;
10. produce an auditable impact record with bounded conclusions and competent approvals.

## Core Exposition

**Frame the decision before searching.** State the problem/opportunity, exact delta, expected value, deadline, reversibility, baseline, scope, and deciding authority. Separate desired behavior from chosen implementation. Include alternatives: defer, change process, substitute component, limit effectivity, add a compensating control, or accept the current state. A solution-shaped request narrows discovery prematurely.

**Establish exact endpoints.** Compare manifests, requirements, models, code/artifacts, BOM, schemas/data rules, infrastructure/policy, procedures, and actual state. Identify additions, removals, modifications, moves, substitutions, relationship changes, and unchanged-but-reinterpreted items. A renamed unit, default, or field can change meaning without a large textual delta.

**Build typed seed sets.** Seeds include not only edited artifacts but changed assumptions, supplier notices, vulnerabilities, anomalies, operating environments, regulations, data distributions, staffing, and end-of-support events. Classify relationship types: satisfies, allocated-to, depends-on, calls, interfaces, supplies, generated-by, calibrated-by, operated-by, deployed-at, verified-by, mitigates, derived-from, retained-for, and retired-with. Direction and semantics determine traversal.

**Traverse forward and backward.** Forward analysis asks what consumes or depends on the changed item. Backward analysis asks what enables each affected claim or outcome and whether an upstream assumption changed. Trace from requirement to implementation and evidence, then from product and test result back to definitions and tools. Bidirectional search exposes stale or missing links.

**Use multiple discovery lenses.** Combine model/trace traversal, source/dependency analysis, BOM/SBOM, interface and data lineage, fault/hazard/threat analysis, operational telemetry, incident history, supplier knowledge, workshops, checklists, physical inspection, and counterfactual scenarios. Independent lenses reduce common blind spots; agreement between two exports from the same stale database does not.

**Distinguish candidates from consequences.** Graph reachability identifies items to examine. For each candidate, document a plausible mechanism: changed timing violates a control deadline; new material changes outgassing; schema default changes downstream aggregation; policy change prevents recovery access. Disposition as affected, unaffected with rationale, conditionally affected, unknown, or out of scope with named owner. Do not confuse path existence with severity.

**Analyze requirements and purpose.** Determine whether stakeholder needs, constraints, derived requirements, allocations, margins, verification methods, or acceptance criteria change. A design change may reveal an incorrect requirement rather than merely require compliance work. Conversely, unchanged wording can conceal altered assumptions or operational context.

**Analyze behavior, resources, and emergence.** Examine functions, states/modes, timing, concurrency, control, sequencing, failure behavior, resource budgets, margins, coupling, and common-cause pathways. Update mass, power, thermal, throughput, memory, latency, bandwidth, reliability, and capacity analyses as relevant. System-level effects arise when individually acceptable deltas consume shared margin or interact.

**Analyze interfaces and compatibility.** Cover physical, electrical, mechanical, thermal, software/API, protocol, data/schema, security/identity, human, organizational, and contractual interfaces. Evaluate semantics, units, coordinate frames, limits, defaults, timing, errors, ordering, authentication, version negotiation, and deprecation. Identify all providers/consumers and their deployed versions; “additive” does not guarantee compatibility.

**Analyze safety, security, privacy, and resilience.** Revisit hazards, controls, fault trees, threat models, attack surface, trust boundaries, permissions, cryptography, logging, personal data, abuse, emergency response, and recovery. Consider whether the change weakens independence or creates common cause. Fast security remediation still needs scoped impact and post-stabilization reconciliation.

**Analyze data and model consequences.** A schema, transformation, reference table, feature, quality rule, retention policy, model, or upstream sensor change can alter historical comparability and downstream decisions. Address stored and in-flight data, backfill, migration idempotence, lineage, late arrivals, replay, privacy, bias, monitoring, rollback compatibility, and model/evaluation validity.

**Analyze physical production and supply.** Trace drawings, BOM, materials, processes, tooling, facilities, suppliers/subtiers, qualification, inspection, acceptance, packaging, transport, stock, spares, serial/lot effectivity, field retrofit, maintainability, obsolescence, and disposal. A form-fit-function claim needs evidence across the actual environmental and lifecycle obligations.

**Analyze humans and organizations.** Consider workload, staffing, competence, training, procedures, displays/controls, alarms, handoffs, access, support, maintenance, emergency actions, and incentives. Automation can shift rather than remove work. Organizational authority or supplier responsibility changes can break escalation and configuration knowledge even when the technical artifact is unchanged.

**Analyze evidence validity.** Construct rows for each claim and columns for changed assumption/configuration, sensitivity, prior evidence, delta argument, new evidence, owner, and decision. Tests can remain useful as designs, fixtures, and historical results without being executable evidence for the successor. Toolchain, calibration, test data, environment, procedure, and test article are part of evidence configuration.

**Analyze lifecycle and enabling systems.** Include design/build/test/deployment services, calibration, facilities, operations, monitoring, repair, training, support, licensing, retention, archival interpretation, and retirement. Determine whether recovery artifacts remain compatible and whether the old state can be safely removed. Costs and risks displaced into sustainment are still change impacts.

**Handle effectivity explicitly.** Build an affected-population query from configuration status, not memory. Classify each serial, lot, variant, site, release, environment, customer, contract, and spare as applicable, nonapplicable with rationale, pending discovery, or unknown. Define coexistence constraints and how long mixed configurations can remain. Update when discovery finds reality differs from records.

**Evaluate cumulative change.** Rebase analysis when other deltas enter the release or production lot. Examine pairwise and higher-order interactions for shared resources, interfaces, migrations, hazards, tests, and rollback. A set of individually low-risk changes may exceed margin or make diagnosis impossible. Compare the actual integrated candidate, not only isolated tickets.

**Express uncertainty honestly.** Separate evidence-backed likelihood from confidence in the model and completeness of discovery. Use ranges, ordinal categories, sensitivity, scenarios, and explicit unknowns when data do not justify precise probabilities. A score is a prioritization aid, not acceptance authority. High consequence with weak knowledge often demands discovery, containment, prototyping, or staged rollout.

**Compare alternatives transparently.** Define criteria before scoring where practical: mission/value, safety/security, performance, schedule, lifecycle cost, operability, maintainability, evidence burden, reversibility, supplier/contract, and retirement. Record weights, scales, assumptions, uncertainty, veto thresholds, and sensitivity. Avoid compensatory totals that allow unacceptable safety or compliance to be offset by cost.

**Design the transition as part of impact.** Specify implementation order, dependencies, data conversion, physical rework, supplier actions, documentation/training, mixed-version compatibility, verification stages, cohorts, maintenance windows, communication, monitoring, abort thresholds, rollback or forward recovery, and old-state disposition. A technically sound final state can still fail through an unsafe transition.

**Close with observed evidence.** After implementation, verify the intended delta and absence of unacceptable regression, reconcile actual state across effectivity, assess monitoring, resolve anomalies, update baselines/evidence/risks, and record residual limitations. If implementation differs from analysis, reopen it. Closure means the bounded change outcome is known and dispositioned, not that uncertainty vanished.

The following fixture computes a static typed reachability set for one synthetic change seed.

<!-- bijux-verify: {"id":"change-impact-closure-fixture","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"change_seeds=data_schema\nrelationship_edges=10\nimpact_candidates=9\nimpact_order=analytics,client_sdk,conformance_evidence,migration,operator_tool,report_contract,rollback,service_api,stored_data\nterminal_candidates=conformance_evidence,operator_tool,report_contract,rollback,stored_data\nstatus=synthetic_candidate_closure_complete\nevidence=declared_graph_reachability_only\n","stderr":""}} -->
```python
dependencies = {
    "data_schema": ["analytics", "migration", "service_api"],
    "analytics": ["report_contract", "stored_data"],
    "migration": ["rollback", "stored_data"],
    "service_api": ["client_sdk", "conformance_evidence"],
    "client_sdk": ["operator_tool"],
}
seeds = {"data_schema"}
frontier = list(seeds)
reached = set(seeds)
while frontier:
    current = frontier.pop()
    for candidate in dependencies.get(current, []):
        if candidate not in reached:
            reached.add(candidate)
            frontier.append(candidate)

impacts = sorted(reached - seeds)
terminals = sorted(node for node in impacts if node not in dependencies)
edge_count = sum(len(targets) for targets in dependencies.values())
print("change_seeds=" + ",".join(sorted(seeds)))
print(f"relationship_edges={edge_count}")
print(f"impact_candidates={len(impacts)}")
print("impact_order=" + ",".join(impacts))
print("terminal_candidates=" + ",".join(terminals))
print("status=synthetic_candidate_closure_complete")
print("evidence=declared_graph_reachability_only")
```

The fixture assumes the graph and edge direction are complete and correct. It does not discover hidden dependencies, interpret edge semantics, establish material consequence, assess severity or uncertainty, validate evidence, identify actual effectivity, examine interactions, or authorize a change.

## Definitions and Notation

Let change proposal $q=(B,C',\Delta,r,a,e)$ identify before baseline $B$, proposed configuration $C'$, exact delta $\Delta$, rationale $r$, assumptions $a$, and intended effectivity $e$. The realized state $\widehat{C}$ may differ from $C'$ and requires observation.

Let typed graph $G=(V,E,\tau)$ include technical and nontechnical nodes and relation type $\tau$. Candidate closure $R(S,G,p)$ is relative to seed set $S$, graph version, and traversal policy $p$. It is never simply “the impacts.”

For candidate $v$, record $I_v=(path,c,s,l,u,evidence,action,owner,effectivity)$ for path, consequence, severity, likelihood, uncertainty, evidence, action, owner, and effectivity. Some domains use different risk scales; preserve definitions and avoid arithmetic unsupported by the scale.

Let evidence claim $h$ have configuration assumptions $A_h$. If $\Delta\cap A_h\neq\varnothing$ or a causal dependency may have changed, evidence applicability requires reassessment. Nonintersection in an incomplete representation cannot prove invariance.

## Mechanisms, Invariants, or Proof Structure

A defensible impact argument proceeds as follows:

1. identify exact before/proposed state, rationale, alternatives, assumptions, urgency, effectivity, and authority;
2. enumerate change seeds including environment, supplier, policy, organizational, data, and lifecycle changes;
3. traverse typed requirements, architecture, interface, configuration, supply, data, operational, evidence, and retirement relationships forward and backward;
4. supplement recorded relations with domain expertise, historical incidents, observation, physical inspection, hazard/threat reasoning, and adversarial scenarios;
5. assign each candidate a mechanism and disposition, recording no-impact evidence and unknowns;
6. assess interactions, common cause, cumulative releases, mixed configurations, transition, and actual populations;
7. update requirements, models, risks, plans, costs, evidence applicability, V&V, monitoring, recovery, communication, and retirement actions;
8. compare alternatives and sensitivity under explicit criteria and noncompensable constraints;
9. obtain competent approvals for the bounded residual consequences;
10. verify implementation and behavior, reconcile effectivity, and reopen analysis when actual evidence violates assumptions.

The conclusion is conditional on graph coverage, source currency, expert competence, assumptions, effectivity knowledge, and evidence quality. It should say what is known, unknown, accepted, deferred, and monitored—not merely “impact assessed.”

## Alternatives and Trade-Offs

**Checklist versus model-driven analysis.** Checklists efficiently recall known categories but can become ritual. Models expose relationships and support queries but may be stale or incomplete. Use both, plus operational and expert challenge.

**Central review versus delegated analysis.** Central boards see cross-boundary effects but can delay routine work. Delegated low-risk paths can be fast when scope, thresholds, automated evidence, audit, and escalation are explicit. Consequential interfaces and accepted risks still need empowered owners.

**Broad regression versus targeted verification.** Broad regression catches some unmodeled coupling but costs time and can still miss changed semantics. Targeted testing follows mechanisms efficiently but depends on analysis completeness. A risk-based combination uses targeted new evidence plus stable broad detection.

**Quantitative scoring versus qualitative argument.** Calibrated data can support expected-loss or reliability calculations. Ordinal matrices communicate under sparse evidence but arithmetic on categories creates false precision. Always retain causal narrative, uncertainty, thresholds, and sensitivity.

**Big-bang transition versus staged effectivity.** Simultaneous change avoids prolonged mixed versions but concentrates risk and limits learning. Cohorts/canaries provide evidence and rollback opportunities but require compatibility, monitoring, population accounting, and time-bounded coexistence.

**Rollback versus forward recovery.** Rollback fits reversible stateless changes. Data migration, physical modification, compromised credentials, external contracts, or irreversible operations may demand forward correction. Choose based on state and consequence, then test the selected path.

## Failure Modes and Misconceptions

- **“The diff is the impact analysis.”** A diff identifies some changed representations, not their consumers, meanings, actual populations, or consequences.
- **“The trace tool found everything.”** It finds recorded relationships under a policy; missing, stale, semantic, physical, human, supplier, and organizational relations remain possible.
- **“Reachable means affected.”** Reachability creates candidates. Mechanism, context, effectivity, and evidence determine material impact.
- **“Not reachable means unaffected.”** This holds only for a complete, correct model and appropriate traversal—conditions rarely provable for open systems.
- **“No requirement changed.”** Design margin, hazards, timing, support, evidence, or operational value may change without requirement text.
- **“Backward compatible means harmless.”** New defaults, semantics, data collection, capacity, errors, security, and strict consumers can break behavior.
- **“Low-risk changes add linearly.”** Shared margins, correlated failures, migrations, and diagnostic ambiguity create interaction.
- **“More tests settle impact.”** Tests support specified claims for configurations; they do not replace scope discovery, authority, or transition design.
- **“A risk score is a decision.”** It compresses assumptions and may hide veto constraints and uncertainty.
- **“Approval closes the change.”** Implementation, verification, observed effectivity, anomaly disposition, baseline update, and old-state retirement remain.
- **“Rollback is always safe.”** Persistent and physical state may be incompatible or irreversible.
- **“Urgency removes analysis.”** Urgency changes depth and timing; bounded authority, identity, monitoring, recovery, and later reconciliation remain necessary.

## Worked Examples

### Example 1

A fastener supplier changes coating. Direct geometry is unchanged, but candidates include corrosion, friction/torque relation, preload, electrical bonding, outgassing, inspection, worker handling, qualification, supplier lots, stock, field units, maintenance, and disposal. Lot-effectivity and targeted environmental/assembly evidence replace a shallow form-fit-function assertion.

### Example 2

An API adds an optional field. Typed search finds generated clients, strict schema validators, signatures, cache keys, payload limits, privacy notices, analytics, documentation, conformance tests, and stored events. Some consumers are unaffected with evidence; one mobile client rejects unknown fields, so rollout and deprecation change.

### Example 3

A compiler upgrade changes no source. Binary layout, floating-point optimization, warnings, timing, debug symbols, reproducibility, licensing, security findings, and test tools may change. Prior functional tests remain useful historical evidence, while timing/numerical and artifact-specific evidence is rerun against the new build.

### Example 4

A database schema changes a nullable amount to non-null with default zero. Impact extends to migration, historical meaning, incomplete records, analytics, reconciliation, downstream exports, replay, rollback, privacy retention, and operator correction. Zero is not semantically equivalent to unknown, so a convenient migration is rejected.

### Example 5

A battery gains capacity and mass. The analysis revisits endurance benefit alongside structure, center of gravity, thermal load, charger, transport, fire response, lifting ergonomics, acceptance, spares, supplier lead time, maintenance, and end-of-life recycling. A limited prototype effectivity reduces uncertainty before fleet retrofit.

### Example 6

A platform team tightens a default network policy. Source dependency graphs show nothing, but service discovery identifies callbacks, monitoring exporters, recovery access, external identity, vendor support, and disaster-recovery replicas. Staged policy audit mode and observed traffic produce a safer authorization boundary.

### Example 7

Five individually low-risk changes share CPU and memory margin. Isolated analyses pass; the integrated candidate violates latency during failover. Cumulative analysis rebases resource budgets and test configuration, defers one feature, and records that ticket-level approval did not authorize the combined release.

### Example 8

A security vulnerability demands immediate credential rotation and component replacement. Emergency CIA identifies affected artifacts, trust boundaries, offline sites, stored secrets, client compatibility, audit evidence, monitoring, rollback limitations, and temporary authority. Post-stabilization analysis addresses root cause, full regression, baseline reconciliation, and old credential invalidation.

### Example 9

A maintenance procedure replaces two-person inspection with camera-assisted review. The tool changes workload, field of view, lighting, data retention, privacy, competence, failure detection, connectivity, calibration, escalation, and evidence records. A controlled trial compares detection and human performance; automation is not assumed equivalent.

### Example 10

A legacy component reaches end of support. Alternatives include replacement, redesign, inventory buy, service-life limit, isolation, or retirement. CIA spans interfaces, qualification, data conversion, supplier rights, safety/security exposure, spares, training, recovery, certification, customers, cost/schedule, and disposal. The decision preserves explicit uncertainty rather than selecting the lowest unit price.

## Cross-Program Connections

- **Platform engineering:** policy, infrastructure, identity, images, observability, shared services, drift, cohorts, and recovery create dependencies outside application source.
- **API and service engineering:** provider/consumer semantics, schema evolution, compatibility, retries, state, rollout, and deprecation are central impact paths.
- **Data engineering:** lineage, schemas, transformations, reference data, stored history, migrations, quality, privacy, and model validity extend change across time.
- **Object-oriented programming:** interface inheritance, dynamic dispatch, binary/source compatibility, dependency injection, reflection, and shared mutable state complicate reachability.
- **Functional programming:** explicit types and effects improve local reasoning, but runtime, compiler, foreign interfaces, data semantics, and operational dependencies remain.
- **Security and safety:** change can add threats/hazards, weaken controls or independence, invalidate accepted risk, and alter emergency/recovery behavior.
- **Verification and validation:** CIA decides which propositions and evidence configurations remain applicable, need analysis, or require new execution.
- **Supply and operations:** lots, sites, spares, repairs, training, procedures, monitoring, mixed versions, obsolescence, and retirement determine real effectivity.

## References

1. NASA, [Configuration Management, Systems Engineering Handbook section 6.5](https://www.nasa.gov/reference/6-5-configuration-management/), accessed 2026-08-31.
2. NASA, [Decision Analysis, Systems Engineering Handbook section 6.8](https://www.nasa.gov/reference/6-8-decision-analysis/), accessed 2026-08-31.
3. NASA, [Technical Risk Management, Systems Engineering Handbook section 6.4](https://www.nasa.gov/reference/6-4-technical-risk-management/), accessed 2026-08-31.
4. NASA, [Requirements Management, Systems Engineering Handbook section 6.2](https://www.nasa.gov/reference/6-2-requirements-management/), accessed 2026-08-31.
5. NASA, [Interface Management, Systems Engineering Handbook section 6.3](https://www.nasa.gov/reference/6-3-interface-management/), accessed 2026-08-31.
6. NASA, [Technical Assessment, Systems Engineering Handbook section 6.7](https://www.nasa.gov/reference/6-7-technical-assessment/), accessed 2026-08-31.
7. NASA, [Product Verification, Systems Engineering Handbook section 5.3](https://www.nasa.gov/reference/5-3-product-verification/), accessed 2026-08-31.
8. NASA, [Product Validation, Systems Engineering Handbook section 5.4](https://www.nasa.gov/reference/5-4-product-validation/), accessed 2026-08-31.
9. NIST, [SP 800-128, Guide for Security-Focused Configuration Management of Information Systems](https://csrc.nist.gov/pubs/sp/800/128/upd1/final), updated 2019.
10. NASA, [NPR 7123.1B, NASA Systems Engineering Processes and Requirements, Change 4](https://nodis3.gsfc.nasa.gov/displayAll.cfm?Internal_ID=N_PR_7123_001B_&page_name=ALL), effective 2020.

## Exercises

### Exercise 1

Perform a structured CIA for changing an autonomous inspection drone's camera and onboard inference model while retaining the airframe and mission API.

### Exercise 2

The synthetic graph has one seed, ten declared edges, and nine reachable candidates. Six are shown affected, two unaffected with evidence, and one unknown. Compute disposition coverage and explain whether the change is ready for approval.

### Exercise 3

Design CIA and transition control for an API/schema change across one provider, four internal consumers, two external consumers, stored events, and asynchronous offline clients.

### Exercise 4

Assess evidence reuse when a release changes application source, compiler, dependency, database schema, infrastructure policy, operator procedure, and monitoring thresholds.

### Exercise 5

Create an emergency CIA process for a remotely exploitable vulnerability affecting a mixed fleet that includes offline assets, spares, unsupported variants, and regulated customers.

## Answers to the Exercises

### Answer 1

Define before/proposed camera identity, optics, sensor, firmware, mount, mass/power/thermal/data rates and exact model weights, architecture, training/evaluation data lineage, preprocessing, thresholds, runtime, and toolchain. State desired detection benefit, alternatives such as optics-only or offboard processing, operational environments, affected serials, and authority.

Trace mechanical fit, center of gravity, vibration, EMI, power/endurance, thermal, enclosure, calibration, timing, compute/memory, storage/link bandwidth, privacy, cybersecurity, map/geolocation, mission API semantics, operator display, maintenance, spares, supplier lots, transport, recovery, and disposal. Revisit detection requirements, false-positive/negative hazards, flight-control resource coupling, environmental cases, human response, and evidence configuration. Unchanged mission API syntax does not prove unchanged timing or meaning.

Create a delta-to-evidence matrix: bench characterization, calibration, structural/vibration/environmental evidence, power/thermal/endurance, inference accuracy by scenario and subgroup, robustness, timing/resource contention, security/privacy, integrated flight, failure/degraded modes, operator usability, maintenance, and acceptance. Use limited serialized prototypes and monitored missions to reduce uncertainty. Define rollback feasibility for model/firmware and physical retrofit, compatibility with old/new ground tools, effectivity, training, spares, and old-camera disposition. Approval is bounded to tested configurations and conditions; fleet closure follows observed reconciliation.

### Answer 2

Disposition coverage is $(6+2)/9=8/9\approx88.89\%$. The unknown candidate is not safely counted as no impact. The ratio also says nothing about severity, graph completeness, evidence quality, interaction, effectivity, or whether the unknown is a critical claim. Therefore it cannot alone support approval.

Identify the unknown's impact path, owner, reason for uncertainty, potential consequence, affected population, and information needed. Seek authoritative artifacts, observation, expert review, prototype/test, supplier input, or containment. If it remains unknown, the competent authority may reject, defer, narrow effectivity, add monitoring/abort criteria, or accept a bounded residual uncertainty only where policy and consequence allow. Review the two no-impact rationales and six affected-item actions, test cumulative/transition effects, and challenge graph coverage independently. Report the percentage as workflow visibility, not risk reduction.

### Answer 3

Freeze before/proposed schema, semantics, defaults, limits, errors, authentication, timing, ordering, and examples. Inventory every deployed provider and consumer version, external contract, stored/in-flight event, offline queue, replay path, analytics/export, SDK, documentation, test, monitoring, and recovery dependency. Obtain provider, consumer, data/privacy/security, operations, and contractual authority.

Build a compatibility matrix for old/new provider and each consumer, including strict parsing, missing/unknown fields, idempotency, retries, signature/cache behavior, payload limits, and semantic interpretation. Analyze stored-event migration versus dual-read/write, late arrivals, replay, rollback, data quality, privacy/retention, and external notification. Execute contract/conformance, migration/reconciliation, mixed-version, performance, security, failure/recovery, and representative end-to-end tests.

Use version negotiation or additive compatibility only when evidence supports it. Deploy observability first, then provider/consumer cohorts in an order that preserves compatibility. Account for offline clients and define a deprecation window, support behavior, abort thresholds, rollback/forward recovery, external communications, and old-version retirement. Close only after every population is migrated, explicitly exempted/waived, or retired and actual observations support the intended state.

### Answer 4

Create rows for every affected claim. Source changes require requirement/behavior/interface trace and changed-component plus regression evidence. Compiler changes may affect binary, ABI, optimization, timing, numerical behavior, reproducibility, warnings, and debug/security tooling. Dependency changes affect API behavior, defects, licenses, vulnerabilities, and transitive content. Schema changes require stored/in-flight data semantics, migration, reconciliation, compatibility, replay, and rollback. Infrastructure policy affects connectivity, identity, failure, recovery, observability, and external services. Operator procedure changes require human factors, training, access, abnormal/emergency scenarios, and repeatability. Monitoring thresholds affect detection latency, false alarms, incident response, and the validity of operational acceptance evidence.

Retain prior tests as designs and historical evidence. For each proposition, state unchanged assumptions and justified equivalence, analytical update, or new execution. Run targeted evidence for each causal mechanism plus stable broad regression and integrated scenarios; check interactions such as policy blocking telemetry used to judge the new thresholds. Bind results to exact build, schema, infrastructure, data, procedure, operator, and tools. Evidence transfers only at claim level with authority and limitations; no global percentage of unchanged content proves successor validity.

### Answer 5

Predefine emergency triggers, incident authority, technical/security/safety escalation, protected implementation path, minimum evidence, exact configuration capture, monitoring, communications, and reconciliation deadline. Identify vulnerable component versions and transitive exposure; discover actual online/offline devices, spares, repair stock, unsupported variants, sites, customers, contracts, network reachability, credentials, data, and compensating controls. Preserve evidence and do not assume inventory completeness.

Compare containment, disablement/isolation, credential rotation, patch, component upgrade, restricted operation, or shutdown. Analyze compatibility, availability/safety, data, performance, supplier support, build provenance, regulatory/customer notification, offline update, rollback and exploitation risk. Use signed/reproducible artifacts, independent checks where time permits, canaries/cohorts, exploitation/correctness monitoring, abort thresholds, and exact effectivity accounting. Provide bounded instructions for assets that cannot update and quarantine unknown stock.

After stabilization, complete root cause, full dependency/interface/hazard/threat impact, regression and validation; reconcile every asset including repaired returns and spares; decide retain/revise/revert; update baselines, SBOM/BOM, evidence, procedures/training, risks and customer records; expire temporary access and controls; and retire vulnerable artifacts. Unsupported or regulated variants require explicit technical/regulatory/customer disposition, not a dashboard exclusion. Emergency urgency shortens initial analysis but does not erase enduring authority and evidence obligations.
