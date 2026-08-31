---
module_id: SYSENG-090
program: Systems Engineering
level: 2
module_number: 90
title: Planning Evolution While Preserving System Integrity
status: complete
last_verified: 2026-08-31
---

# Planning Evolution While Preserving System Integrity

## One-Page Review

### Governing question

Can the organization move a system through a sequence of capability, architecture, technology, configuration, operational, and retirement states while preserving explicitly defined mission, safety, security, data, interface, support, evidence, and governance integrity at every authorized intermediate state?

### Essential definitions

- **System evolution** is the governed change of system capability, structure, realization, operation, support, or lifecycle obligations over time.
- **System integrity** is justified coherence among required behavior, architecture, interfaces, actual configuration, data, safety/security controls, evidence, authority, and lifecycle responsibilities for a stated state and context.
- An **evolution roadmap** relates capability outcomes, baselines, increments, dependencies, technology/support horizons, resources, evidence gates, transition states, fallback, and retirement.
- An **integrity invariant** is a property or constraint required to hold across specified operational and transition states; it must be measurable or otherwise assessable and owned.
- A **transition state** is an intermediate configuration during migration, rollout, retrofit, coexistence, degraded operation, emergency change, rollback, or retirement.
- **Evidence continuity** is the explicit determination of which prior claims/evidence remain applicable, become conditional, require update, or are invalidated by change.
- **Transition debt** is the bounded burden of adapters, duplicated systems, compatibility modes, temporary controls, data synchronization, training, waivers, and old-state support.
- **Evolutionary runway** is the architecture, capacity, support, rights, workforce, tools, data, and decision time available to make future change without unacceptable disruption.
- **Integrity debt** is an unresolved inconsistency or weakly evidenced assumption that narrows safe change options; it is not an excuse to defer known unacceptable risk.
- **Evolution closure** establishes the target state and retires superseded state, temporary bridges, obsolete evidence, access, data, stock, contracts, and residual obligations for stated effectivity.

### Central model, mechanism, or theorem

Model evolution as a state-transition system

\[
\mathcal{E}=(C,\Delta,I,E,A),
\]

where $C$ are identified configurations, $\Delta$ authorized transitions, $I$ integrity obligations, $E$ evidence and observations, and $A$ authorities/effectivity. A path

\[
C_0\xrightarrow{\delta_1}C_1\xrightarrow{\delta_2}\cdots\xrightarrow{\delta_n}C_n
\]

is admissible only if every state—not only $C_n$—meets its applicable obligations or carries an explicitly authorized bounded exception:

\[
\forall k,\ \forall i\in I(C_k):\ evidence(i,C_k)\lor accepted\_exception(i,C_k).
\]

This condition is necessary, not sufficient: obligation discovery, evidence quality, interactions, actual-state reconciliation, and competent authority remain essential.

### Critical invariants

- Define integrity as named obligations and evidence for a stated system boundary, context, configuration, effectivity, and decision; avoid a vague “system remains sound” claim.
- Baseline current intended and observed states, open anomalies, accepted risks, support limits, evidence, and residual obligations before planning successors.
- Derive evolution from stakeholder outcomes, operating evidence, environmental change, threats/hazards, support/obsolescence, regulation, and opportunity—not solution fashion.
- Maintain linked capability, requirements, architecture, interface, technology, configuration, evidence, deployment, support, workforce, funding, and retirement roadmaps.
- Treat every mixed-version, migration, degraded, emergency, fallback, and rollback state as an engineered configuration with requirements, authority, monitoring, and time bounds.
- Preserve exact identity, provenance, effectivity, compatibility, data semantics, control ownership, and evidence applicability across transitions.
- Analyze individual and cumulative changes, shared resources, common cause, dependency order, specialist capacity, decision windows, and option loss.
- Apply noncompensable mission, safety, security, legal, privacy, and records constraints before cost/schedule scoring.
- Stage learning with representative prototypes, integration environments, cohorts, failure/security/recovery cases, and explicit promote/hold/rollback criteria.
- Observe actual product/fleet/service state and user outcomes; automation, documents, and dashboards are not substitutes for reconciliation.
- Remove temporary bridges, privileges, duplicated data, old technology, support paths, contracts, and waivers when their bounded purpose ends.
- Replan when requirements, environment, threats, maturity, supply, cost/schedule, evidence, anomalies, actual state, or service horizon changes materially.

### Common failures

Common failures include treating a roadmap as dates and releases; optimizing each change ticket while ignoring the integrated release; assuming architecture diagrams describe actual dependencies; preserving final-state requirements while transition states are unsafe; using backward compatibility as a syntax claim; migrating data without semantic reconciliation; reusing evidence by percentage of unchanged files; changing control and observation systems with the product simultaneously; letting emergency configuration become permanent; carrying adapters, feature flags, dual writes, broad access, old spares, and waivers indefinitely; scheduling by executive deadline rather than evidence readiness; and declaring evolution complete when the target is online but old variants, recovery, customers, suppliers, data, or obligations remain.

### Compact example

A synthetic three-state path requires four declared integrity obligations in every state: service availability, authorization, data integrity, and recovery. The coexistence state initially omits data-integrity evidence, so promotion is rejected. Adding the missing declared evidence makes all twelve state-obligation pairs present and the path eligible for a metadata gate. The fixture does not prove evidence truth, obligation completeness, behavior, or authorization.

### Connections

Evolution planning integrates technical planning, requirements and architecture, interfaces, configuration/baselines, change impact, risk and decision analysis, technology refresh, obsolescence, verification/validation, safety/security, data migration, platform/service rollout, maintainability/support, finance/workforce, operational feedback, decommissioning, and systems-of-systems governance.

## Governing Question

What sequence of bounded states preserves required integrity while delivering useful change, learning from operation, maintaining recovery options, and intentionally retiring superseded complexity?

The target design is only one part of evolution. Many failures occur between baselines: old and new producers disagree on schema meaning, fleet cohorts use incompatible procedures, a migration cannot roll back, an emergency permission survives, or monitoring changes at the same time as the behavior it must judge. Planning must make intermediate states first-class engineering objects.

## Why This Matters

Long-lived systems evolve because stakeholder needs, operating environments, threats, laws, supply, technology, data, organizations, and budgets change. Refusing change can erode integrity through unsupported components, saturated margins and undocumented workarounds. Uncontrolled change can invalidate evidence, fragment configurations and expose users to unsafe transitions. Integrity therefore means disciplined adaptability, not freezing one design.

NASA Technical Planning describes technical management as recursive and iterative, synchronized with project plans and updated when expectations, resources, constraints, risks, reviews or decisions change. It highlights configuration control because design or environment changes can invalidate prior analyses. Requirements, Interface, Risk, Configuration, Data, Assessment, and Decision processes provide complementary control surfaces. NASA Phase E guidance shows systems engineering continuing through operations, maintenance, upgrades and retirement. These NASA lifecycle structures require tailoring, but the system principle is general: evolution couples planning, implementation, observation, evidence and authority.

Planning too much detail far ahead creates false certainty; planning too little hides option loss and long-lead dependencies. Use rolling-wave detail inside durable capability, architectural, integrity and retirement boundaries. Near-term transitions receive executable configuration/evidence plans; later decisions preserve alternatives, interfaces, information and trigger conditions.

## Prerequisites and Retrieval

Before planning or auditing evolution, retrieve:

1. stakeholder outcomes, mission/services, operating concepts, users, environments, modes, hazards/threats, laws/contracts, service horizon, criticality, budgets, decision authority, and retirement obligations;
2. exact current baselines and observed configurations across variants, serials/lots, releases, sites, customers, suppliers, spares/repairs, degraded modes, emergency changes, recovery, unsupported items, and waivers;
3. current requirements, architecture, interfaces, state/behavior models, resource margins, trust/failure boundaries, data flows/semantics, human work, physical integration, support, and external dependencies;
4. operational evidence: outcomes, incidents/anomalies, reliability/availability/maintainability, performance/capacity, security/privacy, data quality, workarounds, user behavior, maintenance, support cost, environmental and supplier evidence;
5. claim/evidence inventory tied to exact configurations: verification, validation, safety cases, threat/privacy assessments, reliability analyses, certifications, acceptance, tools/data/procedures, anomalies, limits, assumptions and owners;
6. capability and requirements roadmap, architecture evolution, technology maturity/refresh, obsolescence/support, supplier, security, data, workforce/skills, facilities/tools, funding/contracts, deployment windows and retirement plans;
7. proposed change portfolio with before/after states, rationale, alternatives, dependencies, cumulative impact, priority/urgency, authority, resources, V&V, transition, monitoring, recovery and effectivity;
8. compatibility and coexistence models for physical parts, software/API/protocol, schema/data, infrastructure/policy, procedures/training, suppliers, tools, spares, sites, customers and recovery;
9. integrity obligations: mission capability, safety/security/privacy, data, interfaces, resource margins, provenance, support, availability, records, environmental and contractual constraints for steady and transitional states;
10. transition definitions: state manifests, entry/exit evidence, cohorts/serials, migration/retrofit, dual operation, monitoring, abort, rollback/forward recovery, communications, training, temporary controls, anomaly handling and maximum duration;
11. option and uncertainty evidence: long-lead items, latest safe decisions, fallback/descope, technology/supplier alternatives, rights, capacity, model uncertainty, cost/schedule ranges, sensitivity and irreversible commitments;
12. closure/removal obligations: old products/services, data, identities, adapters, flags, waivers, stock, repair paths, tools, suppliers/contracts, monitoring, documentation/training, hazardous material, archives and residual owners.

Perform an **evolution thread** from one stakeholder outcome through current requirements/architecture/configuration/evidence, each proposed intermediate state, migration/compatibility, operational observation, target acceptance, fallback, and old-state retirement. Record every point where a claim changes meaning or authority.

## Learning Objectives

After completing this module, you should be able to:

1. define system integrity as explicit configuration- and context-bound obligations rather than stability rhetoric;
2. model evolution as a path of authorized states and transitions with evidence at every state;
3. align capability, architecture, technology, obsolescence, evidence, deployment, support, workforce, funding and retirement roadmaps;
4. preserve architectural seams, compatibility, data semantics, provenance, support and future options;
5. analyze cumulative changes, dependency order, common cause, resource margins and organizational capacity;
6. design mixed-version, migration, emergency, degraded, fallback and rollback states;
7. create claim-level evidence-continuity and invalidation plans;
8. use staged learning, operational observation, decision triggers and adaptive replanning;
9. control integrity debt, transition debt, exceptions and temporary mechanisms with exit criteria;
10. verify target adoption and remove superseded state across complete effectivity.

## Core Exposition

**Define integrity operationally.** List what must remain true: mission/service outcomes, safety controls, security boundaries, privacy purpose, data integrity, interface semantics, resource margins, availability/recovery, configuration provenance, support, legal/contractual and records obligations. Assign owner, evidence, threshold, context and effectivity. Integrity is not perfection; bounded known exceptions can exist under authority.

**Baseline reality, not intent alone.** Compare authoritative baseline with as-built/deployed/maintained state. Capture drift, workarounds, degraded modes, variants, field repairs, emergency changes, unsupported dependencies, open anomalies, waivers, evidence limitations and actual usage. A roadmap beginning from an idealized diagram cannot design a safe first transition.

**Frame evolution as outcomes and pressures.** Record why change is needed: capability gap, environment, operational evidence, hazard/threat, support horizon, supplier, capacity, regulation, cost, workforce or retirement. Separate need from implementation. Include no change, containment, process change, incremental/modular refresh, redesign, external service, capability reduction and retirement.

**Maintain a roadmap system, not one timeline.** Link capability need dates, requirement decisions, architectural seams, technology readiness, obsolescence, interfaces, data, security, suppliers, skills, facilities, funding, contracts, evidence, deployment and retirement. Record dependencies, uncertainty, windows, fallbacks and triggers. Each sub-roadmap has an owner but shared decisions require integrated authority.

**Plan at multiple horizons.** Near-term changes have exact manifests, impact, V&V and transition steps. Mid-term plans define architectural boundaries, capability increments, technology maturation, suppliers, data migration, workforce and decision gates. Long-term plans preserve options, rights, interfaces, records and research while avoiding unsupported detail. Revisit horizons as evidence changes.

**Preserve architectural runway.** Use stable typed interfaces, modular replacement boundaries, portable data, controlled dependencies, resource margin, observability, automated conformance evidence, supply alternatives, supportable tools and revocable identity. Avoid speculative generality: every seam adds coordination, latency, failure modes and version burden. Design for expected variability and high-consequence change.

**Represent every transition state.** Name configuration, effectivity, valid old/new combinations, data state, identities, policies, procedures, support, monitoring, evidence and authority. Include prepositioning, freeze, shadow, dual-write/read, adapter, canary, mixed fleet, restricted mode, rollback and cleanup. No state may exist solely in a deployment script or operator memory.

**Specify transition invariants.** Examples: at most one authoritative writer per record; authorization cannot be weaker than baseline; safety interlock remains independent; old and new protocol combinations obey a matrix; every request is observable; data reconciliation stays within defined tolerance; recovery remains tested; no serial loses support. Test invariants at boundaries and failure conditions.

**Control interface evolution.** Manage syntax, semantics, units, limits, defaults, ordering, timing, errors, identity, privacy and operational expectations. Inventory all consumers/providers and versions. Use negotiation, adapters, dual support or synchronized cutover only with evidence and retirement dates. Additive fields and physical “fit” do not guarantee compatibility.

**Protect data semantics.** Model authoritative source, schema, transformations, lineage, temporal meaning, null/default, units, identity, reference data, privacy, retention and reconciliation. Plan stored/in-flight/late/offline data, backfill, replay, idempotence and rollback. Dual writes can diverge; define comparison, conflict authority and exit.

**Preserve safety, security and privacy through change.** Revisit hazards, controls, fault containment, threats, trust boundaries, identities, keys, permissions, monitoring, personal-data purpose and emergency response for target and transition. Temporary access and bypasses are high-risk configuration items. Changing both control and assurance systems simultaneously can remove independent observation.

**Manage evidence continuity claim by claim.** Build a matrix: claim, current configuration/assumptions, delta, sensitivity, retained evidence, new analysis/execution, anomaly, owner, authority and limitation. Tests remain useful as designs and historical results even when executions no longer prove the successor. Revalidate evidence tools, data, procedures and environments too.

**Analyze the integrated portfolio.** Rebase changes onto the actual candidate release/lot/fleet plan. Examine common resources, interfaces, migrations, hazards/threats, suppliers, test environments, specialists, downtime and rollback. Individually safe changes can exceed margin, create common cause or make anomalies impossible to attribute. Sequence to preserve observation and fallback.

**Use explicit integrity budgets.** Allocate mass, power, thermal, timing, capacity, reliability, downtime, privacy, security exposure, operational workload and support burden where useful. Preserve uncertainty and noncompensable limits. A budget is a coordination model, not permission to consume every margin; retain contingency for unknowns and future change.

**Make decisions under uncertainty.** Define criteria/vetoes, alternatives, scenarios, ranges, sensitivity, reversibility, option value and latest safe decisions. Stage commitments so learning occurs before irreversible supply, architecture, data or contract choices. Do not disguise ordinal judgment as precise probability. High-consequence unknowns may demand prototype, containment or narrower effectivity.

**Prototype representative risk.** Exercise changed mechanisms, scale, environment, mixed versions, failure, security, migration, operations, maintenance and recovery. Preserve negative results and exact configuration. A feature demonstration without transition and failure context is weak evidence for evolution.

**Establish evidence gates.** Each gate states decision, entry evidence, configuration, effectivity, reviewers/authority, criteria, anomalies, observation period, outcomes and next actions. Gate names do not guarantee rigor. Allow promote, hold, narrow, rollback, forward-correct, descope or retire. Material candidate changes require reassessment.

**Observe operations as experiment and obligation.** Instrument outcomes and invariants before rollout. Use canaries/cohorts/serialized lots where appropriate; compare against expected and counterfactual behavior; capture exposure, data quality and detection coverage. No reported incident can reflect low exposure or poor observation. Preserve evidence during automatic remediation.

**Keep actual-state accounting.** Track intended and observed version/configuration per site, serial, supplier lot, customer, environment, spare/repair and recovery. Report pending, offline, failed, rolled back, exempt, unknown and superseded states. Global “deployed” or “100%” is false if denominator excludes obligations.

**Engineer recovery per state.** Identify rollback compatibility for software/data, physical reversibility, spare substitution, safe degraded mode, manual procedures and forward recovery. Preserve old artifacts and skills only while fallback remains authorized. Test recovery from each consequential transition state, not only target backup restoration.

**Bound temporary mechanisms.** Every adapter, feature flag, duplicate pipeline, emergency permission, waiver, manual reconciliation, shadow service and compatibility layer has owner, rationale, configuration, monitoring, cost/risk, maximum duration, exit criteria and removal evidence. Track transition debt visibly. Repeated extensions trigger architectural or authority review.

**Close evolution fully.** Verify target outcomes and configuration, reconcile all effectivity, resolve anomalies, update baselines/evidence/support, remove old interfaces/data/access/stock/tools/contracts, close temporary debt, preserve required archives and accept residual risks. Target online is midpoint when old complexity remains.

**Learn and replan.** Compare forecast with actual capability, reliability, security, data, human work, support, cost/schedule, migration, anomalies and retirement. Update models, requirements, architecture, supplier and workforce plans. Preserve causal lessons rather than delivery chronology. Replanning is controlled response to evidence, not failure of planning.

The following fixture checks declared evidence coverage across three synthetic states.

<!-- bijux-verify: {"id":"evolution-integrity-path-fixture","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"evolution_states=3\nintegrity_obligations=4\nrequired_state_obligation_pairs=12\ninitial_evidenced_pairs=11\ninitial_missing=coexistence:data_integrity\ninitial_promotion=reject_missing_integrity_evidence\nafter_correction_evidenced_pairs=12\nafter_correction_missing=0\nafter_correction_promotion=eligible_for_declared_metadata_gate\nstatus=synthetic_integrity_path_consistent\nevidence=declared_boolean_coverage_only\n","stderr":""}} -->
```python
states = ("current", "coexistence", "target")
obligations = ("service_availability", "authorization", "data_integrity", "recovery")
evidence = {(state, obligation): True for state in states for obligation in obligations}
evidence[("coexistence", "data_integrity")] = False

def missing_pairs(records):
    return sorted(f"{state}:{obligation}" for (state, obligation), present in records.items() if not present)

initial = missing_pairs(evidence)
print(f"evolution_states={len(states)}")
print(f"integrity_obligations={len(obligations)}")
print(f"required_state_obligation_pairs={len(evidence)}")
print(f"initial_evidenced_pairs={len(evidence) - len(initial)}")
print("initial_missing=" + ",".join(initial))
print("initial_promotion=reject_missing_integrity_evidence")

evidence[("coexistence", "data_integrity")] = True
after = missing_pairs(evidence)
print(f"after_correction_evidenced_pairs={len(evidence) - len(after)}")
print(f"after_correction_missing={len(after)}")
print("after_correction_promotion=eligible_for_declared_metadata_gate")
print("status=synthetic_integrity_path_consistent")
print("evidence=declared_boolean_coverage_only")
```

The fixture trusts obligation completeness, state inventory, boolean evidence, authority and semantics. It does not validate evidence quality, system behavior, actual configuration, effectivity, interactions, uncertainty, accepted exceptions, recovery, monitoring, or promotion.

## Definitions and Notation

Let configuration state $C_k=(products,information,relationships,effectivity,authority)$ and transition $\delta_k=(change,impact,implementation,evidence,recovery)$. Let integrity obligation $i=(claim,threshold,context,owner,method)$ apply to selected states/effectivity.

Evidence relation $E(i,C_k)$ means identified evidence supports a bounded claim; it is not a truth predicate by notation alone. Actual observed state $\widehat{C}_{k,t,x}$ may differ from authorized $C_k$ for time $t$ and instance/site $x$ and requires reconciliation.

Transition debt set $D_t$ contains temporary mechanisms with owners and expiry/exit evidence. Integrity debt set $D_i$ contains known unresolved inconsistencies/weak evidence under authority. Neither should be collapsed into one financial number that hides veto obligations.

## Mechanisms, Invariants, or Proof Structure

A defensible evolution argument proceeds as follows:

1. define stakeholder outcomes, changing pressures, service horizon, system/effectivity boundary, integrity obligations, evidence and authorities;
2. baseline intended and observed configurations, behavior, dependencies, support, evidence, anomalies, accepted risks and retirement obligations;
3. align linked capability, requirements, architecture, interface, technology, obsolescence, security, data, workforce, investment, deployment and retirement roadmaps;
4. compare alternatives and define a path of exact steady/intermediate states with compatibility, invariants, effectivity, fallback and closure;
5. analyze direct/cumulative impact, resource/common-cause interactions, evidence continuity, uncertainty, option loss, suppliers, humans, operations and lifecycle consequences;
6. mature and integrate through representative prototypes and claim-level V&V, preserving independent observation and negative evidence;
7. authorize staged transitions using configuration-bound criteria, monitoring, anomalies, abort, rollback/forward recovery and time-bounded exceptions;
8. observe actual fleet/service/product states and stakeholder outcomes, reconcile data/configuration and reopen when assumptions fail;
9. establish target integrity across complete effectivity and remove superseded systems, data, access, support, bridges, waivers and contracts;
10. update models, plans, architecture, evidence and future options from actual outcomes.

The conclusion is bounded by obligation and dependency discovery, model currency, evidence validity, context, effectivity, observation and authority. No roadmap or gate proves future integrity universally.

## Alternatives and Trade-Offs

**Large replacement versus incremental evolution.** Replacement can simplify target architecture but concentrates maturity, migration, evidence and recovery risk. Increments preserve learning/fallback but create coexistence and transition debt. Choose by coupling, urgency, reversibility and support horizon.

**Stable interface versus coordinated change.** Stable contracts isolate consumers but can preserve obsolete semantics or adapters. Coordinated change enables cleaner design but requires aligned authority and deployment. Versioned compatibility with sunset can bridge the two.

**Central roadmap versus federated roadmaps.** Central planning exposes shared constraints but can suppress local knowledge and autonomy. Federated ownership adapts locally but needs common outcomes, interface authorities, data exchange, conflict resolution and integrated evidence.

**Strict freeze versus continuous change.** Freezes stabilize evidence and migration but accumulate queues and delay urgent work. Continuous change reduces batch size but needs immutable configuration, automated evidence, observed-state control and risk-based gates.

**Rollback versus forward recovery.** Rollback works for reversible compatible state; data, physical, security, supplier and contractual changes may require forward correction or safe degraded operation. Plan the actual mechanism at each state.

**Preserve options versus commit early.** Options reduce uncertainty and lock-in but cost money, complexity and time. Early commitment gains scale and focus but can eliminate fallback before evidence is adequate. Use latest responsible decisions with explicit triggers, not indefinite indecision.

## Failure Modes and Misconceptions

- **“Integrity means no change.”** Unsupported, unpatched and workaround-laden stasis can erode integrity; governed adaptation preserves it.
- **“The roadmap is the plan.”** Dates without states, dependencies, evidence, resources, fallback, authority and retirement are weak intent.
- **“Only the target must satisfy requirements.”** Every operational transition state needs applicable integrity and authorization.
- **“Backward compatible means safe.”** Semantics, data, timing, errors, privacy, security, resources and operations may differ.
- **“Unchanged components retain evidence.”** Changed environment, dependency, tool, data, interface or use can invalidate assumptions.
- **“Small changes are independent.”** Shared margins, suppliers, migrations, controls and specialists create cumulative/common-cause effects.
- **“Canary success proves readiness.”** Exposure, representativeness, duration and observation quality bound inference.
- **“Automation guarantees configuration.”** Failed/manual actions and hidden state require observed reconciliation.
- **“Rollback is always available.”** Persistent, physical, credential, supplier and external-contract state may be irreversible.
- **“Temporary mechanisms are harmless.”** Adapters, flags, dual writes, privileges and waivers add enduring risk without exit control.
- **“One owner controls the system.”** Interfaces, suppliers, customers, platforms, regulators and operators hold distributed authority.
- **“Target online means evolution complete.”** Old states, data, access, spares, recovery, customers, evidence and obligations remain until retired.

## Worked Examples

### Example 1

A fleet evolves through old, mixed and new controller states. Each state has compatible firmware/protocol, spares, procedures, diagnostics, safety evidence and serial effectivity. The mixed state expires only after offline units and repair stock are dispositioned.

### Example 2

A schema migration uses dual writes. The integrity invariant is one authoritative reconciliation rule, not simple count equality. Divergence thresholds, late events, idempotent replay, privacy deletion, recovery and a removal date bound transition debt.

### Example 3

A security control and its monitoring platform are scheduled together. The plan sequences independent observability first, then control cohorts, so evidence remains available if behavior changes. Simultaneous replacement would create an assurance blind spot.

### Example 4

Five low-risk changes each consume small latency margin. The integrated release exceeds failover limits. Portfolio analysis defers one feature and rebaselines evidence; ticket-level approvals never authorized the combined state.

### Example 5

A supplier change is technically qualified for new production, but field repair and spares remain old. The roadmap models two authorized configurations, compatibility and cutoff rather than claiming one current product baseline.

### Example 6

An emergency bypass restores service. It has exact effectivity, monitoring, privilege, expiry, recovery and post-incident review. Permanent design change follows full impact and V&V; the emergency state cannot silently become the baseline.

### Example 7

A managed service migration improves support but adds provider and network dependence. Portable data, exit tests, contractual evidence, identity boundaries, offline fallback and cost monitoring preserve future evolutionary runway.

### Example 8

Canary metrics are green, but the cohort lacks high-volume and regulated users. Promotion pauses until representative data, privacy workflows, failure recovery and customer support are exercised. Absence of incident is not sufficient exposure.

### Example 9

A compatibility adapter survives three extensions. Review shows its semantics now constrain architecture and double operations. The organization funds consumer migration, sets an enforced cutoff and verifies adapter/data/access removal instead of normalizing debt.

### Example 10

The target platform serves all online traffic, yet disaster recovery restores the old stack. A recovery drill reveals the gap. Closure waits for new recovery evidence, retired old credentials/images and reconciled support records.

## Cross-Program Connections

- **Platform engineering:** platform roadmaps, golden paths, compatibility, cohorts, policy/identity, observability, recovery and old-stack removal are evolutionary controls.
- **API/service engineering:** consumer autonomy, schemas/protocols, adapters, versioning, state migration, deprecation, traffic and contracts define transition states.
- **Data engineering:** lineage, semantic migration, dual writes, replay, reconciliation, privacy, model validity and archival continuity preserve information integrity.
- **Object-oriented/functional programming:** modular boundaries, types/contracts, dependency/effect control, referential assumptions, characterization/property tests and runtime/toolchains shape evidence continuity.
- **Safety/security:** invariants, independent controls, threat/hazard updates, temporary access, common cause, monitoring and recovery must survive every state.
- **Supply/operations:** lots, sites, fleets, spares, repairs, suppliers, skills, procedures, incidents and service windows determine actual effectivity.
- **V&V/configuration:** exact manifests, baselines, change impact, evidence matrices, anomalies, observed state and authorization underpin every promotion.
- **Lifecycle governance:** investment, option value, technology/obsolescence, support, records, decommissioning and residual ownership complete the evolution path.

## References

1. NASA, [Technical Planning, Systems Engineering Handbook section 6.1](https://www.nasa.gov/reference/6-1-technical-planning/), accessed 2026-08-31.
2. NASA, [Requirements Management, Systems Engineering Handbook section 6.2](https://www.nasa.gov/reference/6-2-requirements-management/), accessed 2026-08-31.
3. NASA, [Interface Management, Systems Engineering Handbook section 6.3](https://www.nasa.gov/reference/6-3-interface-management/), accessed 2026-08-31.
4. NASA, [Technical Risk Management, Systems Engineering Handbook section 6.4](https://www.nasa.gov/reference/6-4-technical-risk-management/), accessed 2026-08-31.
5. NASA, [Configuration Management, Systems Engineering Handbook section 6.5](https://www.nasa.gov/reference/6-5-configuration-management/), accessed 2026-08-31.
6. NASA, [Technical Data Management, Systems Engineering Handbook section 6.6](https://www.nasa.gov/reference/6-6-technical-data-management/), accessed 2026-08-31.
7. NASA, [Technical Assessment, Systems Engineering Handbook section 6.7](https://www.nasa.gov/reference/6-7-technical-assessment/), accessed 2026-08-31.
8. NASA, [Decision Analysis, Systems Engineering Handbook section 6.8](https://www.nasa.gov/reference/6-8-decision-analysis/), accessed 2026-08-31.
9. NASA, [Systems Engineering in Phase E, Appendix T](https://www.nasa.gov/reference/appendix-t-systems-engineering-in-phase-e/), accessed 2026-08-31.
10. NASA, [NPR 7123.1B, NASA Systems Engineering Processes and Requirements, Change 4](https://nodis3.gsfc.nasa.gov/displayAll.cfm?Internal_ID=N_PR_7123_001B_&page_name=ALL), effective 2020.

## Exercises

### Exercise 1

Create an evolution roadmap for an autonomous warehouse platform covering robot hardware, embedded runtime, fleet/cloud services, APIs, data/models, sites, operators, suppliers, support, security and retirement over eight years.

### Exercise 2

An evolution path has four states and six integrity obligations per state. Evidence exists for 21 state-obligation pairs; two have approved time-bounded exceptions and one is missing without disposition. Compute declared covered/authorized proportions and decide whether promotion is supported.

### Exercise 3

Design a mixed-version transition for a provider API, schema, three internal consumers, two external consumers, stored events and offline clients while preserving data, authorization and recovery invariants.

### Exercise 4

Create an evidence-continuity matrix when a release changes source, compiler, dependencies, infrastructure policy, schema, operator procedure and supplier hardware lot.

### Exercise 5

Audit a claim that evolution is complete because the new platform handles 100 percent of measured production traffic.

## Answers to the Exercises

### Answer 1

Define outcomes and integrity: safe navigation/material handling, throughput/availability, security/privacy, data/model validity, support/recovery, site/customer contracts and eight-year horizon. Baseline actual robot serials and parts/lots/firmware; runtimes/dependencies; fleet APIs/services/infrastructure/identity/policy; schemas/events/maps/models; site networks/chargers/facilities; operators/procedures; suppliers, spares/repair/tools, recovery and evidence. Capture incidents, capacity, obsolescence, skills and waivers.

Link capability demand to replaceable compute/sensor architecture, versioned robot-service protocol, portable event/data contracts, model-serving boundary, platform/security roadmap, supplier and skill horizons, site windows, funding and retirement. Near-term states specify manifests and V&V; later choices preserve interfaces, rights, data and fallback. Define invariants for safe stop, authorization, one authoritative mission state, event reconciliation, offline behavior, observability and recovery.

Sequence observation/identity, compatibility, platform/data, robot cohorts and model changes so controls remain visible. Prototype environment/timing/perception, mixed versions, failure/security, migration, maintenance and recovery. Track every robot/site/spare/repair configuration. Bound adapters, dual writes, emergency access and old support with exits. Verify target outcomes, disaster recovery and all effectivity; retire old images/accounts/services/stock/contracts and preserve required evidence. Replan at incidents, support notices, capacity, regulations, maturity and service extensions.

### Answer 2

There are $4\times6=24$ required pairs. Direct evidence covers $21/24=87.5\%$. If the two approved time-bounded exceptions count as authorized dispositions, 23 of 24 pairs are covered or explicitly authorized: $23/24\approx95.83\%$. One pair remains missing without evidence or accepted exception.

Promotion is not supported merely by either percentage. Identify the missing obligation, state, effectivity, consequence and owner. A single absent safety, authorization, data or recovery obligation can be decisive. Obtain evidence, revise the state, narrow effectivity, or secure a legitimate bounded exception only where authority and policy allow. Review the two existing exceptions for rationale, compensating controls, monitoring, expiry and exit; ensure exception interactions do not create common cause.

Challenge obligation/state completeness and evidence quality. Test actual configuration and transition behavior. Percentages express ledger coverage, not risk-weighted integrity. Promotion becomes eligible for decision only after every applicable pair has credible evidence or an authorized bounded exception and noncompensable constraints hold.

### Answer 3

Baseline exact syntax/semantics/defaults/limits/errors/authentication/timing and all deployed provider/consumer versions, external contracts, stored/in-flight/offline events, SDKs, recovery and monitoring. Define old/new compatibility matrix. Integrity invariants include authenticated/authorized access no weaker than baseline, one authoritative record outcome, idempotent processing, traceable schema semantics, reconciled stored/late data, observable requests and tested recovery.

Choose compatible order: introduce consumer tolerance/version negotiation and observability; deploy schema/API capability without changing semantics; migrate internal then selected external cohorts; handle offline clients under version/time policy; backfill/reconcile data; then withdraw old behavior. If dual reads/writes or adapter is used, define conflict authority, comparison thresholds, capacity/security, owner and removal date. Test old/new combinations, strict parsers, retries, ordering, signatures/cache, migration/replay/rollback, privacy, load, failure and recovery.

Record client/customer/site effectivity, pending/offline/failed/exempt states, notices and support. Monitor correctness, authorization, security, latency, errors and reconciliation with abort criteria. Close after every supported consumer migrates or is explicitly retired/waived, stored and late data reconcile, recovery uses the target, old endpoints/keys/routes/data and adapters are removed, and baseline/evidence/support records update.

### Answer 4

Create one row per claim with current evidence/configuration, changed assumption/path, sensitivity, retained reasoning, new evidence, anomaly, owner, authority and limitation. Source changes map to requirements/interfaces/hazards and component/regression tests. Compiler changes affect binaries, ABI, timing, numerical behavior, reproducibility and tools. Dependencies affect behavior, license, vulnerability and transitive content. Infrastructure policy affects identity/network, failure, capacity, observability and recovery. Schema affects stored/in-flight semantics, migration, compatibility, privacy, replay and rollback. Procedure affects human workload, training, errors, abnormal response and repeatability. Supplier lot affects material/process/site, reliability, acceptance, calibration, traceability and physical effectivity.

Check interactions: compiler timing with hardware; policy access to telemetry used for acceptance; schema migration with rollback; procedure with mixed versions; supplier behavior with software thresholds. Preserve old tests as designs/historical evidence, not relabeled executions. Establish exact candidate/test configurations and run targeted change evidence plus stable broad regression and integrated operational/failure/recovery scenarios. Justify no-impact rows; record uncertainty.

Evidence transfer is claim-specific. Resolve anomalies, update safety/security/privacy, SBOM/BOM, baseline, runbooks/training, recovery and fleet/site/lot effectivity. Competent authorities approve bounded claims; no unchanged-file percentage establishes successor integrity.

### Answer 5

First challenge the denominator and measurement: which regions, customers, variants, protocols, modes, scheduled/batch/failure-only paths and observation duration? Production traffic can exclude offline devices, disaster recovery, maintenance, external clients, spares/repair, test/training, legal archives and old customers. Confirm actual target configuration, identity/policy, schema/data, dependencies and monitoring rather than routing alone.

Verify capability, safety/security/privacy, data reconciliation, performance/capacity, reliability, incidents, user/operator outcomes, support and claim-level V&V. Test target backup/restore/failover, degraded modes and forward/rollback recovery. Inventory and disposition old services/endpoints, DNS/routes, accounts/tokens/certificates/vendor access, images/packages/repositories, schemas/data/replicas/backups, adapters/flags/dual pipelines, infrastructure, monitoring, spares/tools, procedures/training, supplier/customer contracts and waivers.

Reconcile every site/serial/customer/recovery effectivity and investigate post-cutoff requests. Remove superseded state or retain it under named support/records authority with security and exit date. Update baselines, evidence, risks and records. One hundred percent of a measured traffic set proves only routing for that set; evolution closes when target integrity and full-population transition/retirement evidence support the bounded decision.
