---
module_id: SYSENG-087
program: Systems Engineering
level: 2
module_number: 87
title: Technology Refresh
status: complete
last_verified: 2026-08-31
---

# Technology Refresh

## One-Page Review

### Governing question

Can the organization renew selected technologies at the right architectural and operational boundary to preserve or improve required capability, supportability, security, and lifecycle value—while controlling maturity, integration, transition, evidence, fleet effectivity, recovery, and retirement risk?

### Essential definitions

- A **technology refresh** is a governed replacement or renewal of technology within a system to sustain or improve capability and lifecycle viability while deliberately managing affected interfaces and obligations.
- **Technology insertion** introduces a new or materially changed technology into a system context; insertion may occur within a refresh but is not synonymous with routine version update.
- A **technology roadmap** relates capability needs, system evolution, technology options/maturity, dependencies, decision windows, investments, and transition events over time.
- A **refresh boundary** identifies the components, interfaces, data, processes, suppliers, tools, and operational populations changed or intentionally held stable.
- **Readiness** is evidence that a technology has demonstrated relevant properties in a defined environment and integration context. It is not age, popularity, procurement status, or a context-free number.
- A **reference environment** captures representative loads, interfaces, hazards/threats, data, users, operations, manufacturing, maintenance, and failure conditions for evaluation.
- **Transition debt** is the temporary or enduring burden of coexistence, adapters, duplicated operations, migrations, training, waivers, and old-state support created by a refresh.
- A **fallback** is an evidence-backed alternative path if maturation or insertion criteria are not met; it is more than optimism that the old system can remain indefinitely.
- **Refresh effectivity** specifies which variants, serials, sites, customers, releases, environments, and recovery configurations receive the new technology and when.
- **Refresh closure** requires verified target capability and support plus disposition of superseded technology, temporary bridges, data, access, inventory, contracts, and residual obligations.

### Central model, mechanism, or theorem

For candidate option $o$ and context $x$, define an evidence record

$$
T(o,x)=(capability, maturity, integration, support, security, evidence, transition, uncertainty).
$$

A roadmap decision is not $\max$ technology novelty. It selects a bounded path under required capability $C_r$, noncompensable constraints $K$, lifecycle value, and uncertainty:

$$
o^*=\arg\max_{o\in O_{feasible}} V(o),\qquad O_{feasible}=\{o:C(o)\succeq C_r\land K(o)=true\}.
$$

Scoring can organize evidence but cannot make infeasible safety, security, legal, or mission states acceptable. The transition must then demonstrate the candidate in its integration and operational context and reconcile every affected instance.

### Critical invariants

- Start with capability, obligation, risk, service horizon, and decision window—not a preferred product or fashionable architecture.
- Baseline the current system, actual population, evidence, support burden, constraints, and viable “do nothing yet” case.
- Define architectural seams and stable interface intent before choosing refresh scope; include hidden state and enabling systems.
- Assess candidate maturity for the intended function, scale, environment, supply, security, operations, and integration—not the vendor demonstration.
- Separate technology development/maturation from product integration and production/operational readiness.
- Evaluate requirements, interfaces, hazards/threats, reliability, data, humans, manufacturing/supply, operations, maintenance, V&V, contracts, cost/schedule, recovery, and retirement.
- Preserve independent evidence, alternatives, fallback, performance descopes, uncertainty, and decision triggers.
- Prototype representative risk, including failure, load, migration, mixed versions, maintenance, security, and recovery—not only the happy-path feature.
- Bind verification and validation to exact candidate configuration, environment, tools, data, procedures, operators, and limitations.
- Plan compatibility, data/state migration, cohorts, monitoring, abort, rollback or forward recovery, communications, training, and old-state retirement.
- Track effectivity across all field units, sites, spares, repair paths, disaster recovery, customers, and temporary bridges.
- Reassess roadmap and refresh when maturity evidence, dependency/support horizons, requirements, environment, cost/schedule, anomalies, or service life changes.

### Common failures

Common failures include equating newer with better; starting from a vendor solution; using technology-readiness levels without context or evidence; assuming heritage readiness transfers to a new architecture/environment; refreshing a component while ignoring interfaces, data, tools, operators, suppliers, recovery, or certification; hiding immature development inside integration schedules; choosing wholesale replacement without testing incremental options; using weighted scores to offset a veto constraint; prototyping only nominal behavior; postponing migration and retirement work; supporting old/new stacks indefinitely; declaring rollout complete while offline or recovery environments remain old; and retaining the superseded stack “just in case” without security, ownership, test, or exit criteria.

### Compact example

A synthetic ordinal matrix compares patching the legacy stack, a modular refresh, and full replacement across mission fit, support horizon, transition feasibility, and lifecycle value. Under declared weights, modular refresh scores 48, full replacement 42, and legacy patch 36. This arithmetic checks only the declared table; it does not validate scales, weights, feasibility, maturity, evidence, uncertainty, or authorization.

### Connections

Technology refresh joins architecture evolution, technology assessment, roadmapping, obsolescence, configuration and baseline control, change impact, technical risk and decision analysis, prototyping, integration, supply strategy, data migration, verification/validation, platform and service rollout, operations, maintenance, cybersecurity, financing, and retirement.

## Governing Question

Which capability-preserving evolution path should be selected now, what evidence makes it credible in this system context, and how will the organization enter the new state and leave the old one without unmanaged exposure?

Refresh is not merely replacement. It is a lifecycle intervention into a functioning socio-technical system. A faster processor may require power, thermal, software, timing, tooling, qualification, supply, and maintenance changes. A managed database may remove local operations while introducing provider, network, jurisdiction, cost, recovery, and forced-upgrade dependencies. The transition can carry more risk than the target architecture.

## Why This Matters

Systems accumulate aging technology, expiring support, security gaps, saturated margins, scarce skills, costly maintenance, brittle interfaces, and lost supply options. Refresh performed too late becomes emergency redesign. Refresh performed too early can discard valid evidence, introduce immature dependencies, and consume resources without meaningful capability value.

NASA Appendix G describes technology assessment/insertion as a systematic systems-engineering activity and explicitly warns that heritage technology applied in a new architecture or environment does not retain its old readiness automatically. GAO's Technology Readiness Assessment Guide emphasizes credible, objective, reliable, useful assessment and notes that immature technologies have contributed to delays and cost growth. These acquisition-oriented sources require tailoring for continuous services, but the central lesson holds: readiness is demonstrated for an intended use and context.

DoD SD-22 connects DMSMS strategy with technology roadmapping, refreshment, and insertion so known obsolescence and planned evolution inform one another. NIST CSF 2.0 examples call for replacing end-of-life software/services and hardware commensurate with risk. Coordinating support pressure with architecture and capability roadmaps can preserve lower-cost options without letting obsolescence alone dictate the design.

## Prerequisites and Retrieval

Before selecting or auditing a technology refresh, retrieve:

1. stakeholder outcomes, missions/services, required capability, criticality, hazards/threats, operational environments, service horizon, laws/contracts, budgets, time windows, and accountable authority;
2. current baselines and observed population: requirements, architecture, interfaces, configurations, variants, serials/lots, sites, releases, customers, spares, repairs, recovery, waivers, and unsupported states;
3. current performance/capacity/margins, reliability/availability/maintainability, incidents, security/privacy, data quality, human workload, supply/support, skills, cost, energy/environmental burden, and technical debt with trend evidence;
4. obsolescence and support forecasts for components, materials/processes, software/dependencies, services, standards, data formats, tools, facilities, suppliers, licenses/rights, and knowledge;
5. architecture seams and coupling: functional allocation, states/modes, interfaces, protocols/schemas, timing, resources, trust boundaries, physical integration, deployment units, supply boundaries, data stores, and enabling systems;
6. candidate alternatives, including continue/contain, targeted upgrade, adapter, alternate source/service, modular refresh, larger redesign, replacement, outsourcing/insourcing, capability reduction, and retirement;
7. candidate evidence: exact configuration, demonstrated function, scale, environment, interfaces, loads, failure/security conditions, manufacturing/supply, support, standards, licenses, independent assessments, anomalies, and limitations;
8. maturation plan with critical technology elements, gaps, experiments, prototypes, success/failure criteria, independent review, resources, schedule, learning decisions, fallback, and descope;
9. full change impact across requirements, architecture, interfaces, safety/security/privacy, reliability, human factors, data, manufacturing, suppliers, facilities, operations, maintenance, evidence/certification, contracts, and disposal;
10. transition: compatibility matrix, data/state migration, physical retrofit, production cutoff, cohorts, monitoring, communications, training, support, abort criteria, rollback/forward recovery, spares/repair, and old-state retirement;
11. lifecycle cost and schedule ranges, dependencies, capacity, nonrecurring/recurring costs, migration/dual-operation, qualification, support, licensing, exit, residual value, contingencies, and uncertainty/sensitivity;
12. governance: roadmap ownership, decision cadence, criteria/vetoes, technical authority, configuration/change control, supplier/customer coordination, evidence records, measures, and triggers for reassessment.

Perform a **refresh thread** for one capability: trace its current requirements and observed behavior through architecture, components/software/data/services, interfaces, evidence, suppliers/tools, operations/maintenance, recovery, cost, and retirement; then trace the proposed path through every changed assumption and transitional state.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish refresh, upgrade, insertion, modernization, redesign, migration, sustainment, and retirement;
2. connect capability, architecture, obsolescence, support, investment, and transition roadmaps;
3. define refresh boundaries and stable seams that reduce repeated system-wide change;
4. assess maturity and advancement difficulty for an intended application and environment;
5. compare incremental, modular, wholesale, service, containment, and retirement alternatives;
6. design representative prototypes and maturation evidence with fallback and decision triggers;
7. analyze lifecycle impact, cost, schedule, uncertainty, opportunity cost, and option value;
8. create claim-level V&V and readiness evidence for exact integrated configurations;
9. plan migration, mixed configurations, monitoring, recovery, training, fielding, and old-state retirement;
10. govern refresh portfolios and measure capability/support outcomes rather than technology turnover.

## Core Exposition

**Frame the capability problem.** State what outcome is threatened or newly valuable, for whom, by when, in which modes/environments, and over what service horizon. Quantify current and forecast gaps: capacity exhaustion, unsupported dependency, vulnerability, reliability decline, supply loss, maintenance burden, skill scarcity, regulatory change, data growth, or opportunity. Separate need from a proposed technology.

**Baseline the current path.** “Do nothing” means continue current support, risk, cost, performance, and contingency—not zero cost. Record exact configurations and actual population, support agreements, stock, evidence, incidents, workarounds, margins, skill/tool dependencies, and retirement plan. Forecast credible service extension and failure scenarios. This provides the comparison and fallback boundary.

**Align roadmaps.** Relate capability demand, system/architecture evolution, technology maturity, obsolescence, suppliers, security, standards, data, facilities, workforce, funding, contracts, and deployment windows. Record assumptions and triggers rather than a decorative timeline. Coordinate refresh with planned maintenance or releases only when maturity and evidence support the date; calendar coincidence is not readiness.

**Choose a coherent boundary.** Refresh at an interface that can be specified, tested, owned, versioned, and supported. Boundaries may be physical modules, service APIs, data contracts, platform layers, tool adapters, or operational capabilities. Account for hidden coupling: timing, resource contention, state, calibration, defaults, error semantics, human work, supplier processes, and certification evidence.

**Design for repeated refresh.** Stable modular interfaces, replaceable units, adapters, portable data, automated conformance tests, dependency manifests, observability, supply alternatives, and documented operational contracts preserve future options. Modularity is not free: interfaces add latency, cost, failure modes, governance, and version burden. Place seams where expected evolution and consequence justify them.

**Identify critical technology elements.** Find elements whose maturity, performance, manufacture, integration, security, or support is essential and insufficiently demonstrated. Include software, algorithms, data, materials/processes, tooling, infrastructure, suppliers, humans, and operations. Avoid labeling the entire system one readiness level; different elements and integration paths have distinct evidence.

**Assess readiness in context.** Define relevant environment and demonstration before rating. Examine exact configuration, scale, interfaces, loads, failure conditions, data, users, manufacturing, maintenance, security, supply, and duration. Independent reviewers challenge evidence and conflicts. A commercial product proven elsewhere can become immature for a new safety-critical architecture, extreme environment, data distribution, or scale.

**Separate maturation from integration.** Technology maturation demonstrates that critical elements can meet intended properties. Product integration establishes coherent system behavior, manufacturability/deployability, operations, support, and evidence. Hiding maturation inside an integration schedule creates optimistic dependencies and late discovery. Establish criteria and fallback dates before commitment becomes irreversible.

**Prototype the uncertainty.** Build experiments around the hardest assumptions: environmental limits, timing, resource contention, interoperability, migration, security, failure containment, maintainability, operator workload, production yield, supplier repeatability, and recovery. Use representative scale and data. Record negative results, configuration, procedures, anomalies, and limitations. A polished demonstration can be weak evidence if it avoids the critical context.

**Compare architectural alternatives.** Include continued sustainment/containment, targeted replacement, adapter/wrapper, alternate service/source, modular refresh, broad redesign, outsourced/managed service, capability reduction, and retirement. Define criteria and veto constraints before scoring where practical. Consider mission fit, safety/security, maturity, interfaces, support horizon, flexibility, supply, data, operations, evidence, transition, recovery, cost/schedule, and disposal.

**Model lifecycle value and uncertainty.** Include development, integration, qualification/certification, procurement, licensing, infrastructure, data migration, dual operation, training, support, energy, downtime, exit, retirement, residual value, and contingencies. Use ranges and sensitivity. Discounting and expected values can aid comparison, but rare severe consequences, strategic options, and noncompensable obligations need explicit treatment.

**Perform full change impact.** Trace changed technology to requirements, architecture, interfaces, hazards/threats, reliability, human work, data, manufacturing, supply, facilities, build/test tools, operations, maintenance, evidence, contracts, and retirement. Reassess supposedly unchanged elements whose environment or assumptions changed. Analyze cumulative refreshes and shared platform dependencies.

**Engineer data and state migration.** Inventory stored, in-flight, cached, replicated, archived, and externally held state. Define semantic mapping, reconciliation, privacy/retention, ordering, idempotence, late arrivals, corruption, replay, coexistence, rollback compatibility, and deletion. Test boundary/legacy cases and recovery. Copy completion is not semantic migration success.

**Plan coexistence deliberately.** Old and new variants may coexist during production, fleet retrofit, service cohorts, or customer migration. Define compatibility matrices, adapters, routing, diagnostics, spares, repairs, training, monitoring, duration, and ownership. Prevent a temporary bridge from becoming an undocumented permanent subsystem; give it exit criteria and removal evidence.

**Build a claim-level evidence plan.** For each required capability and constraint, identify prior evidence, changed assumptions, transfer rationale, new analysis/test/demonstration/inspection, configuration, environment, data, tools, owner, acceptance, and limitation. Cover nominal, boundary, failure, security, recovery, maintenance, migration, performance, and operational scenarios. Technology readiness does not substitute for integrated product verification and validation.

**Field through evidence gates.** Use laboratory, representative environment, pilot, canary/cohort, production/operational readiness, and broader deployment stages as risk warrants. Each gate has entry evidence, authority, observation period, success/failure criteria, anomaly disposition, and abort/recovery. Do not expand solely because no incident was reported; verify observation quality and exposure.

**Control configuration and provenance.** Identify candidate source/design, artifacts, dependencies, build/manufacturing process, supplier/site/lot, schema/data, infrastructure/policy, procedures, tools, and evidence. Promote immutable or controlled manifests. Observe actual installed configurations because rollout automation and physical work can diverge from declarations.

**Design recovery honestly.** Rollback may be possible for stateless software but unsafe after irreversible physical modification, data migration, external contract change, credential compromise, or old-supplier exit. Prepare and test the applicable fallback: rollback, forward correction, safe degraded mode, spare substitution, manual procedure, or shutdown. Define the last safe decision point.

**Retire the superseded stack.** Inventory old hardware/software/services, data, credentials, network paths, adapters, inventory, spares, tools, licenses, contracts, documentation, training, supplier obligations, and evidence. Preserve only what incidents, field support, certification, law, contracts, or future interpretation require. Remove attack surface and duplicated operational burden; securely dispose and update configuration/status records.

**Govern a refresh portfolio.** Shared technologies can create common benefit and common-cause risk. Coordinate interfaces, platforms, suppliers, migration capacity, test environments, specialist teams, downtime, and funding. Sequence initiatives to preserve fallback and avoid simultaneous changes that make anomalies uninterpretable. Reuse evidence only with explicit equivalence.

**Measure outcomes.** Track capability gap closed, support horizon gained, risk exposure removed, reliability/availability, security, performance/capacity, operational workload, lifecycle cost range, migration reconciliation, coexistence duration, unresolved bridge debt, wrong-configuration escapes, recovery success, affected-population completion, and old-stack removal. Deployment count and technology age are not value measures.

The following fixture computes one synthetic ordinal comparison.

<!-- bijux-verify: {"id":"technology-refresh-options-fixture","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"criteria=4\noptions=3\nlegacy_patch_score=36\nmodular_refresh_score=48\nfull_replacement_score=42\nhighest_declared_score=modular_refresh\nscore_margin=6\nstatus=synthetic_weighted_table_consistent\nevidence=declared_ordinal_arithmetic_only\n","stderr":""}} -->
```python
weights = {"mission_fit": 4, "support_horizon": 3, "transition_feasibility": 3, "lifecycle_value": 2}
ratings = {
    "legacy_patch": {"mission_fit": 3, "support_horizon": 1, "transition_feasibility": 5, "lifecycle_value": 3},
    "modular_refresh": {"mission_fit": 4, "support_horizon": 4, "transition_feasibility": 4, "lifecycle_value": 4},
    "full_replacement": {"mission_fit": 5, "support_horizon": 5, "transition_feasibility": 1, "lifecycle_value": 2},
}
scores = {option: sum(weights[key] * values[key] for key in weights) for option, values in ratings.items()}
ranking = sorted(scores, key=lambda option: (-scores[option], option))
print(f"criteria={len(weights)}")
print(f"options={len(ratings)}")
for option in ("legacy_patch", "modular_refresh", "full_replacement"):
    print(f"{option}_score={scores[option]}")
print(f"highest_declared_score={ranking[0]}")
print(f"score_margin={scores[ranking[0]] - scores[ranking[1]]}")
print("status=synthetic_weighted_table_consistent")
print("evidence=declared_ordinal_arithmetic_only")
```

The fixture assumes complete criteria, valid ordinal multiplication, justified weights/ratings, feasibility, independence, and no uncertainty. It does not establish maturity, evidence, cost, risk, constraints, sensitivity, transition success, operational value, or authority. Real decisions retain the underlying evidence and veto thresholds.

## Definitions and Notation

Let current system $C_0$, proposed target $C_1$, and transition states $C_{0\rightarrow1}(t,e)$ vary with time $t$ and effectivity $e$. Transition risk can exceed steady-state risk; analyze both.

Let candidate record $T(o,x)$ hold capability, maturity, integration, support, security, evidence, transition, and uncertainty in context $x$. Readiness claims without $x$ are incomplete. A readiness level is an ordinal summary under a defined method, not probability of success.

Let option value $V(o)$ include lifecycle benefit and cost under scenarios, while constraint predicate $K(o)$ represents mandatory safety, security, legal, mission, or policy conditions. Weighted scores may rank only options already feasible under $K$.

## Mechanisms, Invariants, or Proof Structure

A defensible refresh argument follows this chain:

1. define stakeholder capability, service horizon, gap, constraints, risks, decision window, and authority;
2. baseline exact current configurations, populations, performance, evidence, support, cost, dependencies, and retirement path;
3. align capability, architecture, technology, obsolescence, supply, security, workforce, investment, and deployment roadmaps;
4. define refresh boundary, stable interfaces, critical elements, representative environment, and maturity gaps;
5. compare sustainment, targeted/modular/broad replacement, service, containment, reduction, and retirement alternatives under vetoes and uncertainty;
6. mature critical technology through representative experiments with independent challenge, criteria, fallback, and decision triggers;
7. perform full change impact and claim-level V&V for integrated candidate and transitional configurations;
8. control provenance, migration, compatibility, cohorts, monitoring, anomaly response, recovery, training, suppliers, and communications;
9. reconcile actual effectivity and demonstrate required capability and support in operation;
10. remove or preserve superseded technology under explicit support, security, evidence, records, and disposal authority.

The conclusion is bounded by the evaluated context, configuration, maturity evidence, scenarios, and transition population. New environment, architecture, scale, data, supplier, or use can invalidate readiness assumptions.

## Alternatives and Trade-Offs

**Incremental refresh versus wholesale replacement.** Incremental work limits scope and preserves evidence but can retain constraints and adapters. Replacement can simplify the target but concentrates maturity, migration, evidence, schedule, and recovery risk.

**Open standards versus proprietary integration.** Open interfaces can improve competition and portability but do not guarantee quality or compatibility. Proprietary solutions may integrate faster and offer accountable support but create rights, pricing, roadmap, data-exit, and forced-migration exposure.

**Managed service versus owned capability.** A service transfers infrastructure and patching burden but adds provider, network, jurisdiction, observability, cost, and exit dependencies. Ownership gives control but requires skill, tools, supply, security response, and capital.

**Early adoption versus proven technology.** Early adoption may provide advantage and longer relevance but carries immature evidence and ecosystem volatility. Proven technology reduces novelty risk but may offer shorter support horizon. Prototypes, options, and staged effectivity can separate learning from commitment.

**Adapter bridge versus direct migration.** Adapters preserve compatibility and pace transitions but add semantics, latency, failure modes, attack surface, tests, and retirement debt. Direct migration reduces steady-state complexity but may demand synchronized change.

**Rollback versus forward recovery.** Rollback protects reversible changes; stateful, physical, security, and external changes may require forward repair. Design and test the applicable recovery path rather than promise universal reversibility.

## Failure Modes and Misconceptions

- **“Newer is better.”** Value depends on required capability, context, evidence, support, transition, and lifecycle obligations.
- **“Commercially proven means ready here.”** Architecture, environment, scale, safety, data, security, supply, and operations can differ.
- **“One readiness level describes the system.”** Critical elements and integrations have distinct maturity evidence.
- **“A roadmap is a committed date list.”** A useful roadmap exposes dependencies, assumptions, alternatives, evidence, windows, and triggers.
- **“The prototype worked.”** Ask which configuration, environment, scale, loads, failures, data, users, duration, and acceptance criteria.
- **“Weighted score chose the answer.”** Scales, weights, vetoes, uncertainty, sensitivity, and evidence require authority and judgment.
- **“Interfaces stay unchanged.”** Timing, defaults, errors, resource use, state, security, and human semantics can change behind syntax.
- **“Migration is copying.”** Meaning, ordering, completeness, privacy, reconciliation, replay, and recovery determine correctness.
- **“Canary success proves fleet readiness.”** Exposure, observation, variants, offline assets, environments, and duration may be insufficient.
- **“We can always roll back.”** Data, physical changes, credentials, contracts, suppliers, and external state may be irreversible.
- **“Running both is safer.”** Dual stacks add attack surface, drift, staffing, diagnosis, data divergence, and cost unless bounded.
- **“Deployment closes refresh.”** Spares, repairs, recovery, customers, bridges, credentials, data, contracts, and old-stack retirement remain.

## Worked Examples

### Example 1

A processor refresh offers performance but changes power, thermal, timing, compiler, firmware, radiation evidence, board layout, supplier, repair, and spares. A representative prototype and limited serialized effectivity precede redesign commitment; the old processor remains controlled until field and repair disposition completes.

### Example 2

A monolith-to-services proposal scores high on scalability but multiplies interfaces, state, identity, observability, deployment, and operator burden. A modular extraction at a stable business boundary closes the real capacity/support gap with lower transition risk. Fashion does not set scope.

### Example 3

A database migration preserves row counts but changes null ordering, collation, time precision, transaction isolation, query plans, and recovery. Semantic reconciliation, performance/failure tests, shadow reads, privacy controls, and restoration evidence bound the rollout.

### Example 4

A heritage sensor was mature in a laboratory aircraft but moves to a colder, higher-vibration autonomous platform with new processing. Its old readiness does not transfer automatically. Environmental, interface, timing, calibration, failure, model-data, maintenance, and operational evidence are refreshed.

### Example 5

A managed cloud service removes hardware obsolescence but adds API retirement, region/jurisdiction, network, identity, data-egress, cost, observability, recovery, and contract dependencies. The architecture includes portable data, exit tests, provider monitoring, and fallback rather than declaring obsolescence eliminated.

### Example 6

A fleet uses an adapter so old clients can coexist with a new protocol. The adapter has explicit semantics, capacity, security, monitoring, owner, conformance tests, expiration, and removal criteria. Offline clients are accounted for; the bridge does not become invisible permanent infrastructure.

### Example 7

A prototype demonstrates nominal throughput with synthetic data. It has not tested peak skew, corrupted input, failover, privacy deletion, recovery, operator response, or sustained load. The decision funds targeted experiments rather than interpreting a demonstration as production readiness.

### Example 8

A refresh combines five changes and anomalies become hard to attribute. The portfolio sequences identity and observability first, then platform, data, and application cohorts, preserving diagnostic baselines and fallback. Coordination reduces common-cause and specialist-capacity risk.

### Example 9

Old hardware is removed, but recovery images, privileged accounts, spare stock, licenses, vendor access, repair instructions, and training labs remain. Closure inventories and dispositions each item, retains only required evidence/support, revokes access, and verifies that retired assets cannot re-enter service.

### Example 10

An ordinal table favors modular refresh by six points. Sensitivity to transition weight reverses the top two choices, and full replacement violates a downtime veto. The board therefore uses the table to expose assumptions, not to authorize by arithmetic; it selects modular learning gates with a legacy fallback.

## Cross-Program Connections

- **Platform engineering:** golden paths, cluster/runtime upgrades, cloud/service dependencies, identity/policy, observability, cohorts, and old-platform removal are refresh mechanisms.
- **API and service engineering:** stable contracts, compatibility matrices, adapters, version negotiation, state migration, deprecation, and consumer effectivity enable bounded evolution.
- **Data engineering:** database/format/pipeline/model refresh requires lineage, semantics, historical comparison, privacy, reconciliation, replay, and recovery.
- **Object-oriented/functional programming:** module boundaries, interfaces/types, dependency isolation, effects, runtime/compiler changes, and characterization/property tests influence refresh seams and evidence.
- **Supply/manufacturing:** parts, materials/processes, tools, suppliers, producibility, qualification, lots, stock, repairs, and field retrofit shape physical refresh.
- **Security/safety:** refresh can remove unsupported exposure yet introduce new hazards, trust boundaries, common cause, and evidence needs.
- **Verification/validation:** technology maturity, integrated verification, operational validation, and fleet monitoring are distinct evidence layers.
- **Lifecycle management:** architecture, obsolescence, investment, workforce, support, records, recovery, and retirement roadmaps must converge.

## References

1. NASA, [Technology Assessment/Insertion, Systems Engineering Handbook Appendix G](https://www.nasa.gov/reference/appendix-g-technology-assessment-insertion/), accessed 2026-08-31.
2. U.S. Government Accountability Office, [GAO-20-48G, Technology Readiness Assessment Guide](https://www.gao.gov/products/gao-20-48g), reissued 2020.
3. U.S. Department of Defense, [SD-22, Diminishing Manufacturing Sources and Material Shortages](https://quicksearch.dla.mil/qsDocDetails.aspx?ident_number=275490), active document dated 2026-01-06.
4. NIST, [Cybersecurity Framework 2.0 Implementation Examples](https://www.nist.gov/document/csf-20-implementations-pdf), accessed 2026-08-31.
5. NASA, [Decision Analysis, Systems Engineering Handbook section 6.8](https://www.nasa.gov/reference/6-8-decision-analysis/), accessed 2026-08-31.
6. NASA, [Technical Risk Management, Systems Engineering Handbook section 6.4](https://www.nasa.gov/reference/6-4-technical-risk-management/), accessed 2026-08-31.
7. NASA, [Configuration Management, Systems Engineering Handbook section 6.5](https://www.nasa.gov/reference/6-5-configuration-management/), accessed 2026-08-31.
8. NASA, [Product Verification, Systems Engineering Handbook section 5.3](https://www.nasa.gov/reference/5-3-product-verification/), accessed 2026-08-31.
9. NASA, [Product Validation, Systems Engineering Handbook section 5.4](https://www.nasa.gov/reference/5-4-product-validation/), accessed 2026-08-31.
10. NASA, [NPR 7123.1B, NASA Systems Engineering Processes and Requirements, Change 4](https://nodis3.gsfc.nasa.gov/displayAll.cfm?Internal_ID=N_PR_7123_001B_&page_name=ALL), effective 2020.

## Exercises

### Exercise 1

Design a technology-refresh roadmap for an autonomous warehouse platform spanning robot compute/sensors, embedded runtime, fleet services, data/models, cloud, facilities, tools, suppliers, operators, and a twelve-year service horizon.

### Exercise 2

Recompute the fixture scores. Then increase transition-feasibility weight from 3 to 6 and explain why the resulting ranking still does not authorize a choice.

### Exercise 3

Assess the readiness of a commercially proven vision system proposed for a safety-relevant outdoor inspection robot in a new climate, architecture, scale, and operating concept.

### Exercise 4

Create an evidence and transition plan for replacing an end-of-support database, service API, and identity provider while clients and sites migrate at different rates.

### Exercise 5

Audit whether a refresh can close after all online production traffic uses the new platform but offline assets, disaster recovery, spares, repair tools, adapters, old data, accounts, and contracts remain.

## Answers to the Exercises

### Answer 1

Start from capability and obligations: throughput, navigation/safety, availability, security/privacy, environmental range, recovery, maintainability, site/customer commitments, production/repair and twelve-year support. Baseline serialized robots, compute/sensor/battery lots and firmware; runtimes/dependencies; services/APIs/infrastructure/identity/policy; schemas/maps/models/data lineage; chargers/networks/facilities; build/test/calibration/diagnostic tools; suppliers, licenses, skills, procedures, evidence, spares and recovery. Reconcile actual sites and forecast capacity, failures, support and obsolescence.

Build linked capability, architecture, technology, obsolescence, supplier, security, workforce, investment and site-window roadmaps. Candidate seams include replaceable compute/sensor modules, versioned robot-service protocol, portable event/data contracts, model-serving interface, and facility adapter. Identify critical technologies and representative environments; prototype thermal/power/timing, perception distributions, radio/site interference, security, failure/recovery, repair/calibration and operator workload.

Compare sustainment, targeted component changes, modular refresh, managed services and retirement by vetoes and scenario value. Establish fallback and latest safe decisions. Sequence observability/identity and compatibility first; use lab, pilot robots/sites, cohorts, mixed-version tests, training, spares/repair conversion and recovery drills. Bind evidence to exact configurations and serial/site effectivity. Retire adapters, old images/accounts/services, stock and contracts when every site, offline robot, repair path and recovery configuration is dispositioned. Reassess annually and at support, anomaly, regulation, capacity or service-life triggers.

### Answer 2

Original scores are legacy patch $4(3)+3(1)+3(5)+2(3)=36$; modular refresh $4(4)+3(4)+3(4)+2(4)=48$; full replacement $4(5)+3(5)+3(1)+2(2)=42$. Modular refresh leads full replacement by six.

With transition weight 6, scores become legacy $12+3+30+6=51$, modular $16+12+24+8=60$, and full replacement $20+15+6+4=45$. Modular remains first; legacy becomes second. This sensitivity reveals that the declared ratings favor transition and that full replacement is fragile under that preference.

The ranking cannot authorize because ordinal multiplication, weights, rating evidence, independence, completeness, uncertainty and scale meaning are unvalidated. Safety/security/legal/mission vetoes may exclude an option. Costs, maturity, interactions, operational populations and fallback are absent. Review evidence behind each rating, vary uncertain values/weights, evaluate scenarios and noncompensable constraints, then use competent authority. The table structures discussion; it is not a decision theorem.

### Answer 3

Define the critical functions and exact product configuration: optics/sensor, processing, firmware/software/model, training/evaluation data, preprocessing, mounting, calibration, power/thermal, interfaces and supplier/manufacturing. Define relevant outdoor environment: temperature, precipitation, lighting/glare, contamination, vibration, weather extremes, electromagnetic conditions, backgrounds, distances/speeds, connectivity, maintenance, people/obstacles and mission duration. Map safety claims and failure/degraded modes.

Examine commercial evidence for configuration, scale, data distribution, environment, latency, reliability, security, privacy, supply, maintenance and anomalies. Do not transfer a context-free readiness label. Identify gaps and advancement difficulty. Run calibrated laboratory/environmental tests, representative datasets and scenario coverage, robustness/boundary/adversarial cases, timing/resource contention, integrated robot tests, fault injection, degraded modes, cybersecurity, maintenance/calibration, operator response and outdoor pilots over sufficient duration. Track false positives/negatives by consequential scenario, not aggregate accuracy alone.

Independent reviewers challenge relevance and evidence. Define maturation criteria, fallback sensor/operational restriction, abort thresholds and serialized pilot effectivity. Product verification and operational validation follow technology assessment. Approval is bounded to the demonstrated architecture, environment, software/model/data, serials and conditions; changed climate, scale, model or mount triggers reassessment.

### Answer 4

Baseline database/schema/data semantics, API contracts/consumers and identity flows/roles/credentials, including recovery, offline sites, external clients, tools, policy, observability and exact versions. Define target semantics, compatibility matrices and trust boundaries. Analyze stored/in-flight/cached data, transactions, collation/time/nulls, retries/idempotence, tokens/sessions, authorization defaults, audit, privacy/retention, capacity, failure and rollback.

Build claim-level evidence: migration counts/control totals and semantic reconciliation; query/report behavior; API contract/conformance and old/new combinations; identity authentication, authorization, revocation, federation and break-glass; performance/load; security/threat; failure/failover; backup/restore; late/offline replay; observability/incident; operator/customer validation. Bind all results to exact configurations, data, tools and procedures.

Deploy observability and compatibility first. Use shadow/dual reads or writes only with reconciliation and exit rules. Sequence identity/API/database changes so every intermediate combination is authorized; pilot cohorts/sites, monitor correctness/security/performance, and define abort/forward-recovery. Inventory every client and offline site. Update training, runbooks, support and customer notices. Remove bridges, old credentials/providers, database access, APIs and duplicated data only after all effectivity and recovery are verified and retention obligations dispositioned.

### Answer 5

Online production traffic establishes only one population. Audit the refresh manifest and intended effectivity against observed configuration. Inventory offline assets and next-connect behavior; disaster-recovery infrastructure, images, data and procedures; spare hardware and embedded versions; repair/diagnostic/calibration/build tools; compatibility adapters and routes; archived/replicated/cached old data; identities, keys, service accounts and vendor access; licenses, support and supplier/customer contracts; training and evidence dependencies.

For each item decide migrate, retain under controlled field support or records need, isolate with risk/exit date, revoke, return, securely dispose, or retire. Test offline update and mixed-version behavior, repair/spare insertion controls, disaster restoration into the new target, adapter removal, data reconciliation/deletion, credential revocation and contract exit. Preserve minimal historical configurations/evidence where incidents, certification, law or support require them without leaving active attack paths.

Closure needs observed target capability, all-population configuration reconciliation, resolved anomalies, validated recovery, updated baseline/support/evidence, and verified removal or bounded retention of the old stack. If offline or regulated populations remain intentionally old, state that effectivity and keep an owned support/risk issue; do not report global closure.
