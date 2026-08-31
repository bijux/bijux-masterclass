---
module_id: SYSENG-086
program: Systems Engineering
level: 2
module_number: 86
title: Obsolescence Management
status: complete
last_verified: 2026-08-31
---

# Obsolescence Management

## One-Page Review

### Governing question

Can the organization detect and forecast loss of availability, support, capability, rights, knowledge, or compliance early enough to choose and implement a technically sound, lifecycle-cost-effective response without compromising mission, safety, security, evidence, supply integrity, or recoverability?

### Essential definitions

- **Obsolescence** is the loss or impending loss of practical availability, supportability, suitability, compatibility, producibility, maintainability, security, legal usability, or interpretability of an item or capability.
- **Diminishing manufacturing sources and material shortages (DMSMS)** concerns loss or reduction of sources or material availability; it is an important physical-supply subset of broader obsolescence management.
- An **obsolescence issue** is a configuration-specific mismatch between required service horizon/capability and forecast availability or support.
- A **notice** is supplier, maintainer, regulator, standard, vulnerability, service, or internal information indicating change or discontinuance. It is a trigger for verification and analysis, not proof of fleet impact by itself.
- **Service horizon** is the period and conditions over which the system and support solution must remain acceptably operable, maintainable, secure, compliant, and recoverable.
- **Lead time to impact** includes discovery, decision, procurement, redesign, qualification, certification, production, deployment, training, and fleet transition—not merely supplier delivery.
- A **resolution** is an authorized response such as monitoring, alternate source, lifetime buy, reclamation, repair, emulation, technology refresh, redesign, service substitution, isolation, reduced support, or retirement.
- **Proactive management** monitors risks and prepares responses before immediate shortage or support loss; **reactive management** responds after an issue already constrains delivery or operation.
- **Continuity evidence** supports that the chosen response preserves required behavior and obligations for stated configurations and effectivity.
- **Issue closure** requires verified resolution across the affected population and sustainment plan; placing an order or selecting a substitute is not closure.

### Central model, mechanism, or theorem

For item $i$, compare required service horizon $H_r(i)$ with support/availability horizon $H_s(i)$ and resolution lead time $L(i)$:

$$
slack(i)=H_s(i)-now-L(i).
$$

Negative slack signals that the forecast resolution window is already missed under current assumptions. Positive slack is not proof of low risk because horizon and lead-time estimates may be uncertain. Evaluate an issue record

$$
O_i=(identity, usage, population, horizon, uncertainty, consequence, options, evidence, owner, trigger).
$$

Prioritization supports attention; competent authority chooses a response using mission consequence, uncertainty, lifecycle cost, technical feasibility, security/safety, effectivity, and strategic value.

### Critical invariants

- Define the system service horizon, required capabilities, configurations, populations, and support concept before classifying an item obsolete.
- Maintain exact configuration and usage identity: manufacturer/source, part/version, revision, lot/serial, supplier, license, dependencies, locations, quantities, and critical relationships.
- Monitor hardware, materials/processes, software/firmware, dependencies, data formats, models, cloud/external services, standards, tools, test equipment, facilities, documentation, rights, suppliers, and skills.
- Verify notices against authoritative sources and actual usage; map them to assemblies, variants, sites, spares, repairs, evidence, and downstream customers.
- Forecast detection-to-impact time with uncertainty and include analysis, contracting, qualification, certification, production, rollout, training, and old-state retirement.
- Evaluate alternatives against requirements, interfaces, hazards/threats, reliability, producibility, maintainability, cybersecurity, data, evidence, cost/schedule, and retirement.
- Do not assume an alternate with the same catalog description is form-fit-function-process-software-evidence equivalent.
- Treat lifetime buys as inventory and degradation decisions involving demand uncertainty, storage life, counterfeit exposure, handling, test, refresh, ownership, and surplus disposition.
- Preserve authorized sources, provenance, intellectual-property/license rights, build/test capability, calibration, knowledge, and archival interpretability.
- Integrate obsolescence resolutions with configuration control, change impact, V&V, baselines, supply quality, rollout/effectivity, and risk acceptance.
- Track implementation for every affected instance, spare pool, repair path, site, supplier, version, and customer/contract.
- Reopen issues when demand, service life, supplier status, vulnerability, regulation, field failure, lead time, cost, or actual configuration changes.

### Common failures

Common failures include waiting for a discontinuance notice; monitoring purchased parts but not embedded dependencies or subtiers; treating end-of-sale and end-of-support as the same date; trusting a vendor roadmap as a guarantee; failing to inventory actual versions; buying lifetime stock without demand, storage, counterfeit, or shelf-life analysis; using brokers without provenance and test controls; selecting drop-in replacements from dimensions alone; ignoring compiler, database, operating-system, cloud, certificate, data-format, license, and skill obsolescence; allowing unsupported systems without compensating controls and exit dates; duplicating redesigns across product lines; qualifying a substitute but not fielding it; and closing an issue while old fleets, spares, repairs, or recovery environments remain exposed.

### Compact example

A synthetic inventory records six items and declared support horizons. A simple policy marks three with at most twelve months as urgent candidates, two at thirteen through twenty-four months as planned candidates, and one beyond twenty-four months as monitor. The output prioritizes investigation only. It does not validate supplier facts, demand, consequence, lead time, uncertainty, substitution feasibility, or authority.

### Connections

Obsolescence management connects lifecycle planning, configuration identification, product structure, supply and parts management, asset inventory, technology roadmaps, risk and decision analysis, change impact, qualification, verification/validation, cybersecurity, maintenance, capacity, contracts and rights, knowledge preservation, technology refresh, and retirement.

## Governing Question

Which capabilities and dependencies may become unavailable or unacceptable before the system's obligations end, and what response preserves the best bounded lifecycle outcome?

Obsolescence is relative, not an intrinsic label. A discontinued component with verified stock beyond the last supported unit may pose little exposure. A currently sold service with a six-month forced migration can threaten a long-lived regulated system. A source archive is insufficient if its compiler, signing process, license, test equipment, schema, or knowledgeable maintainers disappear.

## Why This Matters

Late discovery converts options into emergencies. Redesign and qualification that could have been coordinated with a planned refresh instead become schedule-critical. Scarce purchases invite counterfeit or degraded stock. Unsupported software accumulates vulnerabilities and compatibility gaps. Lost proprietary formats or licenses can make historical evidence unreadable. Retired skills can prevent safe repair even when parts remain.

The U.S. Department of Defense SD-22 guidance treats DMSMS management as a multidisciplinary, risk-based process to identify issues, assess potential readiness/schedule impact, analyze resolution strategies, and implement a cost-effective choice. NASA MSFC-STD-3620 establishes active requirements for proactive EEE-parts obsolescence management in its stated scope. These sources are valuable but hardware/DMSMS practices must be extended deliberately to software, data, services, tools, people, and rights.

NIST Cybersecurity Framework 2.0 implementation examples include plans for software/service and hardware end-of-life maintenance support and obsolescence, plus replacing unsupported versions commensurate with risk. Security is one dimension: a forced upgrade can introduce safety, compatibility, availability, evidence, or privacy risk. An integrated systems view avoids optimizing availability while degrading the mission.

## Prerequisites and Retrieval

Before establishing or auditing obsolescence management, retrieve:

1. system lifecycle and service horizons, missions/services, criticality, operational environments, populations, variants, sites, customers/contracts, regulations, support concept, budgets, and retirement plans;
2. product/configuration structures and authoritative inventories for hardware, materials, firmware, software, libraries, containers, operating systems, schemas/data formats, models, infrastructure, services, policies, tools, facilities, documentation, licenses, suppliers, and skills;
3. exact item/source identity, revisions/versions, approved alternates, composition and dependencies, subtiers, quantities, locations, serials/lots, installed base, spares, repair stock, demand/consumption, shelf/storage life, and provenance;
4. supplier/manufacturer lifecycle states, product-change/discontinuance notices, last-order/ship dates, support and security dates, roadmaps, service terms, financial/source health, geopolitical/logistics constraints, and confidence/source date;
5. operational and sustainment evidence: failure/removal rates, repair yield, turnaround, cannibalization, demand variability, maintenance burden, vulnerabilities, incidents, performance/capacity, license use, support cases, and knowledge gaps;
6. resolution lead times for analysis, sourcing, contracting, intellectual-property access, design, prototyping, qualification, certification, manufacturing, data migration, deployment, training, fleet retrofit, and old-state disposition;
7. requirements, architecture, interfaces, margins, hazards/threats, reliability/maintainability, human factors, data lineage, certification, and verification/validation evidence that a resolution may affect;
8. supply-quality and counterfeit controls, authorized distribution, traceability, storage/handling, incoming inspection, destructive/nondestructive test, calibration, screening, and suspect-item disposition;
9. software/service preservation: source, build recipes, dependencies, toolchains, artifacts/signatures, SBOM, schemas, infrastructure, keys/trust, documentation, test environments, data migration, licenses/rights, and recovery evidence;
10. resolution history and reuse opportunities across product lines, including alternates, redesigns, qualification results, nonrecurring engineering, open issues, lessons, and common interfaces;
11. governance: roles, monitoring cadence, alert thresholds, issue states, prioritization, boards/authorities, escalation, funding, supplier flow-down, metrics, audit, and records retention;
12. candidate transition details: exact effectivity, coexistence, production/repair cutoff, inventory disposition, fielding order, monitoring, rollback/forward recovery, communications, training, and retirement.

Perform an **obsolescence thread** for one mission-critical function: trace requirement to design, constituent parts/software/data/services, suppliers and toolchains, evidence, installed population, spares/repair, operators, recovery, retention, and retirement. Mark inferred inventories, single sources, unsupported dependencies, inaccessible rights, and untested preservation.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish DMSMS, end-of-sale, end-of-support, functional obsolescence, technical debt, shortage, and loss of knowledge/rights;
2. define service horizons and build a configuration-specific obsolescence inventory;
3. monitor authoritative notices, market/support signals, vulnerabilities, standards, suppliers, skills, and internal capability;
4. estimate time-to-impact and resolution lead time with uncertainty rather than false precision;
5. map an issue to exact product structures, populations, evidence, and lifecycle obligations;
6. compare monitoring, alternate source, lifetime buy, repair, emulation, refresh, redesign, substitution, isolation, and retirement;
7. perform change impact and qualification for physical, digital, data, service, and process resolutions;
8. manage counterfeit, storage, shelf-life, licensing, provenance, cybersecurity, and knowledge risks;
9. implement and verify resolutions across production, field, spares, repairs, sites, recovery, and customers;
10. measure program effectiveness through exposure and outcomes rather than notice counts alone.

## Core Exposition

**Define the obligation horizon.** Start with how long and under what conditions the capability must operate, be produced, repaired, audited, recovered, or interpreted. Separate production, warranty, operational support, regulatory record, and archival horizons. Include extension scenarios; programs often outlive nominal dates.

**Broaden the object of management.** Monitor physical parts and materials/processes, but also firmware, source and binaries, transitive dependencies, compilers/build services, operating systems, databases, data formats, models, cloud APIs, certificates, identity systems, test/calibration equipment, facilities, documentation, licenses, suppliers, and skilled roles. An available assembly can be unusable when one enabling capability disappears.

**Establish exact usage visibility.** Resolve manufacturer part numbers, internal numbers, alternates, revisions, versions, lots, serials, supplier sites, source status, dependency trees, quantities, locations, and product usage. Reconcile declared BOM/SBOM and service catalogs with as-built, installed, repaired, and recovery configurations. Unknown usage is exposure, not zero demand.

**Create a monitoring strategy.** Combine contractual notification, manufacturer/authorized-distributor notices, standards/regulatory changes, vulnerability and support feeds, supplier reviews, product roadmaps, inventory/demand, maintenance evidence, market analysis, engineering knowledge, and periodic configuration scans. Record source, retrieval time, confidence, affected identity, and verification. Duplicate feeds can share one upstream blind spot.

**Distinguish lifecycle signals.** Introduction, active sale, not-recommended-for-new-design, product change, last-time-buy, end-of-sale, last shipment, maintenance-only, security-only, and end-of-support are different states. Vendors use inconsistent terminology. Record exact services remaining, dates, conditions, regions, versions, and contractual commitments rather than one red/green status.

**Forecast exposure with uncertainty.** Estimate required quantities/capacity and resolution lead time using ranges and scenarios. Include attrition, repair yield, scrap, growth, surge, shelf life, storage loss, cannibalization, fleet extensions, supplier delay, qualification failure, and rollout. Compare earliest plausible impact with latest safe decision point. Do not turn an uncertain vendor date into a precise countdown.

**Prioritize by consequence and option loss.** Consider mission/safety/security, single-source status, installed population, demand, support horizon, notice maturity, design coupling, lead time, evidence burden, supply integrity, cost/schedule, and ability to contain or reverse. The item with the nearest last-buy date is not always the highest program risk; a lower-level common item or lost tool may dominate several systems.

**Open an owned issue.** Record identity, authoritative evidence, affected assemblies/configurations/populations, stock and demand, service horizon, impact date range, consequence, uncertainty, candidate strategies, owner, decision date, funding, status, dependencies, and escalation triggers. Link—not duplicate—shared issues across product lines while preserving local effectivity and authority.

**Analyze no-action honestly.** Continuing unchanged may be rational when obligations end before exposure or verified stock/support is sufficient. Include vulnerability, failure, contractual, knowledge, and extension scenarios. “No action” should define monitoring triggers and contingency, not disappear from the register.

**Evaluate continued support or isolation.** Extended vendor support, internal maintenance, compensating security controls, network isolation, restricted operation, or reduced capability can buy time. Assess staffing, source/rights, vulnerability response, hardware repair, recovery, compliance, operational burden, common cause, and an exit plan. Isolation is not absolute if data, media, people, or maintenance cross the boundary.

**Evaluate alternate sources and substitutes.** Confirm design ownership and exact differences in materials, process, site, firmware, quality controls, tolerances, interfaces, timing, environmental performance, reliability, security, data semantics, licenses, and lifecycle. Flow through drawing/BOM, work instructions, supplier approval, incoming inspection, qualification, acceptance, spares, repair, documentation, and serial/lot/version effectivity.

**Evaluate lifetime buys carefully.** Forecast quantity with uncertainty and service extension; assess authorized sourcing, date/lot traceability, counterfeit risk, shelf life, storage environment, periodic test, degradation, packaging, handling, refresh, insurance/ownership, tax and working capital, single-event loss, inventory visibility, repair consumption, and surplus disposal. A purchase preserves items, not necessarily tools, knowledge, software compatibility, or licenses.

**Evaluate repair, reclamation, and emulation.** Repair or harvest can extend physical availability but needs failure modes, donor provenance, screening, workmanship, calibration, residual life, configuration and certification. Emulation/virtualization can preserve behavior but must cover timing, peripherals, data, licenses, security, environment, operations, and recovery. Both can defer redesign while accumulating concentrated support risk.

**Evaluate refresh and redesign.** Technology refresh can restore support, security, capacity, skills, and supply competition, but expands change impact. Revisit requirements, interfaces, architecture, hazards/threats, reliability, human work, data migration, tooling, manufacturing, operations, evidence, certification, training, rollout, recovery, and retirement. Coordinate multiple known issues when integration risk is controlled; avoid a giant untestable replacement justified solely by age.

**Preserve knowledge, rights, and evidence.** Secure source/design data, specifications, models, manufacturing processes, test methods, calibration, repair procedures, tooling definitions, schemas, representative lawful data, build environments, dependencies, licenses, escrow, supplier rights, decisions, and trained roles. Verify that retained information is readable and sufficient by performing builds, repairs, restorations, or interpretation drills.

**Control supply integrity.** Shortage pressure increases broker, relabeling, counterfeit, salvage, and degraded-stock exposure. Prefer authorized sources and contractual provenance. Where exceptional sources are considered, apply risk-based authentication, inspection, test, traceability, segregation, technical authority, and disposition. A functional sample does not establish lot-wide authenticity or long-term reliability.

**Integrate resolution into change control.** Perform change impact against the exact baseline and variants. Define requirements, interfaces, qualification, regression, safety/security, supplier, data, operations, transition, and retirement evidence. Approval authorizes a bounded resolution; it does not prove availability or implementation.

**Manage effectivity and transition.** Specify which new production, lots, serials, repairs, software versions, sites, customers, and spares receive the resolution. Support mixed configurations with compatibility and time limits. Update maintenance/training, diagnostics, inventory, provisioning, recovery, documentation, and certification. Quarantine ambiguous stock and prevent old parts or unsupported images from re-entering through repair.

**Verify closure in reality.** Confirm sourcing or redesign, qualification/acceptance, production incorporation, fielding, stock disposition, repair capability, support agreements, software/service migration, observed configuration, and residual monitoring. An implemented alternate in new production does not close exposure in field units or spares unless their disposition is explicit.

**Measure prevention and outcome.** Track exposed critical items, unknown usage, overdue decisions, negative decision slack, issues discovered reactively, shortage-caused downtime/delay, counterfeit/suspect escapes, resolution lead time, avoided-cost assumptions, unresolved unsupported software, lifetime-buy losses, reuse of qualified resolutions, and recovery/preservation test success. Normalize by population and consequence. More alerts can reflect better visibility; few issues can mean poor discovery.

The following fixture applies one deliberately simple horizon policy to declared synthetic inventory.

<!-- bijux-verify: {"id":"obsolescence-horizon-fixture","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"inventory_items=6\nurgent_candidates=3\nplanned_candidates=2\nmonitor_candidates=1\nearliest_support_horizon_months=5\nurgent_items=compiler,flight_processor,supplier_process\nstatus=synthetic_horizon_triage_consistent\nevidence=declared_support_months_only\n","stderr":""}} -->
```python
support_months = {
    "flight_processor": 5,
    "operating_system": 14,
    "database": 28,
    "compiler": 9,
    "test_instrument": 18,
    "supplier_process": 6,
}
urgent = sorted(item for item, months in support_months.items() if months <= 12)
planned = sorted(item for item, months in support_months.items() if 12 < months <= 24)
monitor = sorted(item for item, months in support_months.items() if months > 24)
print(f"inventory_items={len(support_months)}")
print(f"urgent_candidates={len(urgent)}")
print(f"planned_candidates={len(planned)}")
print(f"monitor_candidates={len(monitor)}")
print(f"earliest_support_horizon_months={min(support_months.values())}")
print("urgent_items=" + ",".join(urgent))
print("status=synthetic_horizon_triage_consistent")
print("evidence=declared_support_months_only")
```

This fixture trusts declared months and arbitrary thresholds. It omits service horizon, resolution lead time, uncertainty, demand, stock, consequence, dependencies, supplier truth, actual usage, security/safety, cost, feasibility, and authority. Its categories start investigation; they do not select a resolution.

## Definitions and Notation

Let required service horizon be $H_r$, forecast support horizon $H_s$, resolution lead time $L$, and review time $t$. Decision slack $s=H_s-t-L$ uses consistent units. Because $H_s$ and $L$ are uncertain, represent ranges or distributions when evidence supports them; a point estimate can hide the earliest credible loss.

Let issue $O_i=(id,U,P,H,C,X,A)$ include exact identity, usage $U$, affected population $P$, horizon evidence $H$, consequences $C$, uncertainty $X$, and alternatives $A$. Resolution $r$ has lifecycle cost, schedule, benefit, risk, evidence burden, effectivity, and residual exposure—not only purchase price.

Demand balance for a lifetime buy can be sketched as $Q_{need}=Q_{forecast}+Q_{attrition}+Q_{test}+Q_{uncertainty}-Q_{usable\ stock}$. Every term requires assumptions; excess and shortage both have consequences. This expression is planning notation, not a universal inventory formula.

## Mechanisms, Invariants, or Proof Structure

A defensible obsolescence argument follows this chain:

1. define required capabilities, service/records horizons, configurations, actual populations, support concept, and authorities;
2. establish exact cross-domain item identity, usage, dependencies, suppliers, quantities, rights, tools, evidence, and skills;
3. monitor multiple authoritative and operational sources, verify signals, and record source currency/uncertainty;
4. forecast impact and latest safe decision using demand, stock/support, degradation, extension scenarios, and total resolution lead time;
5. assess mission, safety/security, readiness, interfaces, reliability, maintainability, data, evidence, contract, cost/schedule, and retirement consequences;
6. compare no action, support/isolation, sourcing/buy/repair, emulation, refresh/redesign, substitution, and retirement under explicit criteria;
7. choose through competent authority and integrate funding, contracting, change control, qualification, configuration, transition, and recovery;
8. implement across exact production/field/spare/repair/software/site/customer effectivity;
9. verify technical behavior, supply integrity, actual incorporation, support capability, records, and old-state disposition;
10. continue monitoring because horizons, demand, vulnerabilities, suppliers, and service obligations change.

The conclusion is bounded by inventory completeness, source reliability, forecast uncertainty, actual service extension, and response feasibility. “Resolved” should name the population and remaining assumptions.

## Alternatives and Trade-Offs

**Reactive versus proactive management.** Reactive work avoids monitoring cost for irrelevant items but loses options and increases emergency cost. Proactive work preserves decision time but can create alert noise. Risk-based tiering and shared monitoring focus effort on critical, long-lead, common, uncertain dependencies.

**Lifetime buy versus redesign.** A buy may be fast and avoid qualification but concentrates storage, forecast, counterfeit, and future compatibility risk. Redesign restores availability and capability but carries engineering, evidence, schedule, transition, and certification burden. Compare full remaining lifecycle and extension scenarios.

**Commercial upgrade versus frozen preservation.** Upgrades provide security/support and skills but force recurring migration. Frozen environments preserve behavior but accumulate vulnerability, hardware, license, knowledge, and recovery risk. Hybrid isolation and planned replacement can be time-bounded bridges.

**Common redesign versus local resolution.** A shared redesign amortizes nonrecurring cost and reduces variants, but coordination expands scope and schedule. Local resolutions are faster but duplicate evidence and fragment support. Use common interfaces and reusable qualification where effectivity and authority allow.

**Vendor support versus internal capability.** Vendor support transfers some maintenance burden but creates dependency on commercial priorities and terms. Internal/escrow capability improves control but requires rights, competence, tools, security response, and continuing investment.

**Replacement versus retirement.** Replacement preserves capability but may not be worth lifecycle cost or transition risk. Retirement can remove exposure when stakeholders, data, contracts, downstream dependencies, safety/security, and records are deliberately handled.

## Failure Modes and Misconceptions

- **“Obsolete means unavailable.”** Availability, support, suitability, security, and interpretability are separate; stock can exist after support ends.
- **“A notice proves impact.”** Verify exact identity, usage, effectivity, dates, source, and contractual meaning.
- **“The BOM is the inventory.”** Actual builds, repairs, software, services, tools, spares, subtiers, and undocumented substitutions may differ.
- **“Positive stock balance solves it.”** Demand, degradation, test, scrap, counterfeit, disaster, extensions, knowledge, tools, and compatibility remain.
- **“Same part description means equivalent.”** Materials, process, site, firmware, tolerances, quality, reliability, security, and evidence can differ.
- **“Virtualization preserves software forever.”** Licenses, dependencies, clocks, keys, peripherals, data, vulnerabilities, host platforms, and skills remain.
- **“Unsupported means replace immediately.”** Consequence, compensating controls, feasibility, transition risk, and authority determine response; unsupported exposure stays explicit.
- **“The newest technology is the best resolution.”** Novelty can increase integration, evidence, supply, training, and lifecycle risk.
- **“A last-time buy closes the issue.”** Receipt, authentication, storage, periodic test, ownership, demand monitoring, deployment, and disposal continue.
- **“Qualification closes the issue.”** Production, fleet, spares, repairs, recovery environments, documentation, and old-state disposition need effectivity.
- **“One vendor roadmap is a forecast.”** Roadmaps can change; triangulate and model uncertainty.
- **“Retirement is deletion.”** Consumers, data, evidence, credentials, materials, contracts, and records require disposition.

## Worked Examples

### Example 1

A processor receives a last-time-buy notice. The program maps it to three board variants, ground spares, repair stock, compiler/toolchain, radiation evidence, and a ten-year extension scenario. A bounded buy covers near-term repairs while a compatible redesign is qualified; provenance, storage, periodic test, and surplus disposition remain controlled.

### Example 2

An operating system reaches security end of support before a regulated service retires. Options include paid support, isolation, upgrade, application migration, or early retirement. The decision considers vulnerabilities, device drivers, database, validation, operator training, availability, recovery, customer notification, and exit date—not just license cost.

### Example 3

A cloud provider announces retirement of an API. Inventory finds production, analytics, backup restoration, and one rarely exercised disaster-recovery workflow. Contract tests and telemetry cover common paths; a recovery drill exposes the hidden dependency. Migration closes only after both normal and recovery configurations are observed.

### Example 4

A polymer is restricted by new regulation. Impact analysis covers performance, environmental exposure, supplier processes, worker safety, qualification, existing stock, field repairs, waste, documentation, contracts, and regional effectivity. A substitute that passes nominal strength still needs aging and compatibility evidence.

### Example 5

A calibration laboratory closes. Instruments remain physically available, but traceable calibration, procedures, fixtures, reference standards, turnaround, transport, and competent staff become the obsolescence issue. The program qualifies another laboratory and updates intervals, evidence, shipping, spares, and contracts.

### Example 6

A proprietary data format is no longer supported. The archive contains files but not a licensed decoder version or complete semantics. The organization secures rights, preserves a controlled reader, exports to a durable format, validates samples and edge cases, records transformation loss, and tests future interpretation.

### Example 7

A broker offers scarce parts after authorized channels close. Low price and passing functional samples do not establish authenticity or residual life. The program considers redesign and reclamation, then applies provenance review, lot segregation, authentication, screening, technical authority, and serialized effectivity to any exceptional purchase.

### Example 8

Only two maintainers understand a legacy control language. Skill loss is tracked like a support dependency. Documentation, paired maintenance, training, emulator/build preservation, exercised recovery, succession, and a staged rewrite reduce exposure. Headcount alone would miss concentrated knowledge and rights.

### Example 9

A model-serving framework deprecates the version used for a safety-relevant classifier. Migration can change preprocessing, kernels, numerical behavior, latency, hardware, model format, monitoring, and reproducibility. Differential, scenario, robustness, timing, security, and operational evidence bind the new stack to the claim.

### Example 10

A last-time buy appears cheaper than redesign under nominal retirement. Sensitivity shows a three-year service extension exhausts stock and leaves no qualified option. The decision funds a limited buy plus interface-preserving redesign, explicitly valuing option retention and avoiding false precision in forecast demand.

## Cross-Program Connections

- **Platform engineering:** operating systems, Kubernetes/cloud APIs, identity, images, policy engines, observability, certificates, and managed services carry forced support horizons.
- **API and service engineering:** provider retirement, protocol/schema versions, client populations, deprecation, external contracts, migration, and recovery determine effectivity.
- **Data engineering:** formats, databases, pipelines, catalogs, lineage tools, models, storage media, privacy rights, and interpretability can become obsolete independently.
- **Object-oriented/functional programming:** language/runtime/compiler/package ecosystems, binary interfaces, build reproducibility, foreign dependencies, and maintainer knowledge shape software longevity.
- **Supply and manufacturing:** DMSMS, materials/processes, authorized sources, lots, counterfeit avoidance, storage, qualification, spares, repairs, and tooling are core physical concerns.
- **Security:** unsupported components accumulate exposure; compensating controls, isolation, patch capability, inventory, monitoring, and exit plans need risk authority.
- **Verification/validation:** every alternate, migration, emulation, repair, or redesign needs claim-specific continuity evidence and configuration binding.
- **Lifecycle and finance:** roadmaps, options, nonrecurring engineering, inventory carrying cost, service extensions, contracts, rights, and retirement determine total value.

## References

1. U.S. Department of Defense, [SD-22, Diminishing Manufacturing Sources and Material Shortages](https://quicksearch.dla.mil/qsDocDetails.aspx?ident_number=275490), active document dated 2026-01-06, accessed 2026-08-31.
2. NASA, [MSFC-STD-3620, Electrical, Electronic, and Electromechanical Parts Obsolescence Management and Control Requirements](https://standards.nasa.gov/standard/MSFC/MSFC-STD-3620), active baseline, accessed 2026-08-31.
3. NIST, [Cybersecurity Framework 2.0 Implementation Examples](https://www.nist.gov/document/csf-20-implementations-pdf), accessed 2026-08-31.
4. NIST, [SP 800-40 Rev. 4, Guide to Enterprise Patch Management Planning](https://csrc.nist.gov/pubs/sp/800/40/r4/final), published 2022.
5. NIST, [SP 800-128, Guide for Security-Focused Configuration Management of Information Systems](https://csrc.nist.gov/pubs/sp/800/128/upd1/final), updated 2019.
6. NASA, [Configuration Management, Systems Engineering Handbook section 6.5](https://www.nasa.gov/reference/6-5-configuration-management/), accessed 2026-08-31.
7. NASA, [Technical Risk Management, Systems Engineering Handbook section 6.4](https://www.nasa.gov/reference/6-4-technical-risk-management/), accessed 2026-08-31.
8. NASA, [Technical Data Management, Systems Engineering Handbook section 6.6](https://www.nasa.gov/reference/6-6-technical-data-management/), accessed 2026-08-31.
9. NASA, [Systems Engineering in Phase E, Appendix T](https://www.nasa.gov/reference/appendix-t-systems-engineering-in-phase-e/), accessed 2026-08-31.
10. NASA, [NPR 7123.1B, NASA Systems Engineering Processes and Requirements, Change 4](https://nodis3.gsfc.nasa.gov/displayAll.cfm?Internal_ID=N_PR_7123_001B_&page_name=ALL), effective 2020.

## Exercises

### Exercise 1

Design an obsolescence-management system for an autonomous warehouse platform spanning robots, batteries, sensors, embedded software, cloud services, data, facilities, tools, suppliers, and operators.

### Exercise 2

A part has 30 months until stated last shipment. Redesign and qualification are estimated at 18–27 months, contracting at 3–6 months, and fleet transition at 4–8 months. Calculate the nominal range of decision slack if the activities are sequential and interpret it.

### Exercise 3

Compare lifetime buy, alternate source, redesign, extended support/isolation, and retirement for an unsupported controller used by 400 field units with uncertain five-to-ten-year remaining service.

### Exercise 4

Create a continuity-evidence plan for migrating a long-lived data service from an end-of-support database and proprietary archive format.

### Exercise 5

Audit whether an obsolescence issue can close after a substitute part is qualified and incorporated into new production while older field units, repairs, spares, and supplier stock remain.

## Answers to the Exercises

### Answer 1

Define production, operational, repair, recovery, and records horizons by warehouse/site and extension scenarios. Build a hierarchical configuration inventory: serialized robots; controllers, sensors, motors, radios and battery lots; firmware/runtime/dependencies; cloud APIs, images, infrastructure, identity/policy and observability; schemas, maps, models/reference data; chargers/network/facility interfaces; diagnostic/calibration/build/test tools; procedures/training; suppliers/subtiers, licenses, rights, and skilled roles. Reconcile declared and observed configurations, spares and repair stock.

Tier monitoring by criticality, commonality, lead time, single source and uncertainty. Consume verified manufacturer/provider notices, security/support feeds, supply/demand/failure data, standards/regulation, supplier health and internal skill/tool evidence. Each issue maps identity to assemblies, robot serials, sites, evidence and service horizon; it records date ranges, confidence, stock/demand, consequence, options, owner, funding and trigger.

Evaluate no action, buy/support, alternate/repair, service substitution, refresh/redesign and retirement across safety, security/privacy, navigation/performance, interfaces, availability, maintenance, data/model behavior, supplier quality, evidence, operations/training, recovery, cost and disposal. Use controlled pilots and effectivity for migrations. Verify production, field, spares, repairs, recovery and actual service state before closure. Measures include critical exposure, unknown usage, negative slack, reactive discovery, downtime, suspect supply, unsupported software, resolution latency and preservation drills—not alert count alone.

### Answer 2

Sequential total resolution lead time ranges from $18+3+4=25$ months to $27+6+8=41$ months. With 30 months until stated last shipment, nominal decision slack ranges from $30-41=-11$ months to $30-25=5$ months. The pessimistic credible case is already eleven months late, while the optimistic case leaves only five months.

This does not mean availability ends at last shipment or that each duration is independent. Verify last-order versus last-shipment dates, stock/demand, overlap opportunities, supplier commitment and uncertainty. Model redesign failure/rework, contracting and certification concurrency, production capacity, field access, extensions and inventory. Open urgent action now: preserve interim supply/support, fund design discovery, identify alternates, bound effectivity and establish escalation. A point estimate near the midpoint would hide meaningful negative slack; competent authority decides using consequence and options, not arithmetic alone.

### Answer 3

First identify controller revisions/firmware, unit serials/sites, spares/repair stock, failure/removal rates, interfaces, hazards, security exposure, support skills/tools, certification, customer contracts and actual service scenarios. Five versus ten years materially changes all options.

A lifetime buy minimizes near-term integration but carries forecast, storage/degradation, counterfeit/provenance, single-loss, repair and extension risk; it does not restore patches or knowledge. An alternate source may preserve design but needs process/site/material/firmware, quality, reliability, security and qualification evidence. Redesign can restore support and capability but has architecture/interface, safety/security, software, certification, training, retrofit, recovery and schedule risk. Extended support plus isolation buys time if source/rights, patching, staffing, monitoring and an exit plan are credible; isolation may constrain operations. Retirement avoids replacement only if stakeholders, data, contracts, safety and downstream dependencies can be closed.

Use scenarios and sensitivity rather than one forecast. A robust hybrid may buy authenticated stock for near-term failures, contract support/containment, and develop an interface-compatible redesign with pilot effectivity. Define decision triggers, funding, qualification, fleet cohorts, mixed-version diagnostics, spares/repair cutoff, old-stock disposition and observed closure. Authority may choose different mixes by customer or criticality; document residual unsupported exposure.

### Answer 4

Baseline database engine/configuration, schema, stored procedures, extensions, drivers, application/query behavior, collation/time/numeric semantics, access/policy, backup/recovery, performance, monitoring, source data and proprietary format/decoder versions, licenses and keys. Preserve representative lawful datasets including nulls, boundaries, corrupt/legacy records, time zones, encodings and large volumes; identify privacy and retention limits.

Define target schema/format and semantic mappings with explicit loss. Build repeatable extraction, transformation, validation, reconciliation and idempotent restart. Evidence includes record/count/control totals, constraints/referential integrity, sampled and property-based semantic comparison, query/report/API equivalence, performance/capacity, security/privacy, concurrency, late/in-flight data, failure injection, backup/restore, rollback or forward recovery, and user/operational validation. Independently test the archive reader/export and retain manifests, checksums, provenance and transformation logs.

Run shadow/dual processing or staged datasets where risk permits; reconcile differences before cohorts. Bind tests to exact engine, drivers, schema, infrastructure, code, data, tools and procedures. Train operators, update incidents/support and monitor correctness, latency and resource use. Retain old systems only as long as required and secured; verify future interpretation after access/tool changes. Close when all effectivity is migrated or explicitly dispositioned, recovery is proven, records obligations are met, and obsolete credentials/services/licenses are retired.

### Answer 5

Qualification and new-production incorporation close only two parts of the resolution. Audit the original issue scope and effectivity. Identify every older serial/site, installed part and firmware, spare and repair pool, depot/work-in-progress, supplier/contract manufacturer stock, returns, training/test articles, recovery configuration and customer/contract. Reconcile records with physical inspection or trusted inventory and preserve lot/provenance.

For older field units decide continued authorized operation, retrofit at maintenance, run-to-failure replacement, restricted use, waiver, or retirement. Verify mixed-version compatibility, diagnostics, procedures/training, safety/security, maintenance, certification and evidence. Segregate and label old/new spares; update BOM/drawings/work and inspection instructions, provisioning, repair rules and software configuration. Prevent obsolete parts from re-entering through supplier or depot stock. Dispose or retain old stock under authorized shelf-life, counterfeit, hazardous-material, contractual and records controls.

Closure requires implemented and verified disposition for every population plus residual monitoring. If field use remains authorized, the original shortage may be resolved for production while a separate support exposure stays open with owner, stock/demand, risk, triggers and end date. Report that bounded state rather than a global closed flag.
