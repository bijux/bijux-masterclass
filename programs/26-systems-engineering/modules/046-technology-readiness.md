---
module_id: SYSENG-046
program: Systems Engineering
level: 1
module_number: 46
title: Technology Readiness
status: complete
last_verified: 2026-08-31
---

# Technology Readiness

## One-Page Review

### Governing question

What objective evidence shows that every technology critical to a proposed system can perform its required function, at representative scale and integration, in the application-relevant environment—and what work, risk, cost, and schedule remain before commitment?

### Essential definitions

- A **technology** is knowledge, process, method, material, component, software-enabled capability, or combination whose maturity is being assessed for a specified application.
- A **technology readiness level (TRL)** is an ordinal description of demonstrated maturity under defined criteria; it is not a probability of success, quality score, schedule percentage, or universal property independent of use.
- A **technology readiness assessment (TRA)** is a documented, evidence-based evaluation of critical technologies against applicable readiness criteria by a competent team with sufficient objectivity.
- A **critical technology element (CTE)** is an element whose novelty, performance, environment, manufacture, integration, or failure could materially prevent the system from meeting objectives or commitments.
- The **system of interest/application** fixes required functions, performance, architecture, interfaces, scale, quantities, lifecycle, users, and operating environments for the assessment.
- A **laboratory environment** permits controlled demonstration but may omit material stresses, interfaces, scale, operators, variability, or mission conditions.
- A **relevant environment** contains the application conditions needed to expose important performance and failure mechanisms at the assessed stage; its content is technology- and use-specific.
- An **operational/target environment** is the actual or sufficiently representative context of intended use, including interfaces, operators, loads, hazards, maintenance, and mission duration as applicable.
- A **breadboard**, **brassboard**, **model**, **prototype**, and **actual system** imply different representation fidelity; the assessment defines rather than assumes these terms.
- **Heritage** means prior use/evidence, not automatic readiness. Changed architecture, environment, scale, supplier, process, configuration, or mission can invalidate transfer.
- An **Advancement Degree of Difficulty (AD2)** assessment characterizes the challenge of moving from current maturity to required maturity.
- A **technology maturation plan (TMP)** defines evidence-producing work, entry/exit criteria, resources, dependencies, risks, alternatives, decision points, and fallback needed to close readiness gaps.
- **Integration readiness**, **manufacturing readiness**, **operational/adoption readiness**, and **programmatic affordability** complement TRL; a high TRL does not prove them.

### Central model, mechanism, or theorem

For critical technology set (C), application baseline (B), environment definition (E), and evidence package (D), assess each element:

\[
TRL_i=A(c_i,B,E,D_i),\qquad i\in C.
\]

The readiness claim is a tuple, not a bare integer:

\[
R_i=(c_i,configuration,function,scale,interfaces,environment,evidence,date,TRL_i,limits).
\]

For a gate requiring (TRL^*), a conservative weakest-link condition is

\[
Ready(C)=\bigwedge_{i\in C}(TRL_i\ge TRL^*)\land I_{adequate},
\]

where (I_{adequate}) states that system-relevant integration evidence is adequate. An arithmetic average cannot satisfy a low critical element, and component levels cannot establish integrated-system readiness.

### Critical invariants

- Assessment scope names the exact application, baseline, architecture, functions, interfaces, scale, environment, lifecycle, decision gate, and required readiness.
- CTE identification covers hardware, software-enabled behavior, materials, processes, manufacture, human interaction, suppliers, facilities, integration, and enabling products as applicable.
- Terms such as prototype, relevant environment, representative scale, successful demonstration, and heritage are operationally defined before scoring.
- A level is earned only by completed, traceable evidence satisfying every applicable criterion; plans, expert confidence, money spent, elapsed time, or partial success do not substitute.
- Evidence identifies article/configuration, procedures, instruments, conditions, results, acceptance criteria, anomalies, uncertainty, provenance, review, and limitations.
- Performance is demonstrated at the required function, load, duration, quality, safety/security, interfaces, and adverse/boundary conditions proportionate to the claim.
- The assessed level applies to the demonstrated item/use; changes trigger applicability analysis and possible reassessment.
- The system claim respects the lowest critical maturity and integration state; TRLs are not averaged or used to hide unassessed elements.
- Readiness and remaining maturation difficulty are both reported; one ordinal level does not define cost, schedule, risk, or probability of advancement.
- Independent/competent reviewers disclose roles, conflicts, dissent, evidence gaps, and judgment rationale.
- A TMP closes named gaps with measurable exit evidence, realistic schedule/resources, dependencies, risk/uncertainty, fallback, and decision/reassessment points.
- Decision authority records whether to mature, prototype, redesign, use an alternative, defer, accept bounded risk, change commitments, or stop.

### Common failures

Common failures include assigning a TRL to an entire product without identifying CTEs; copying a supplier's level without application evidence; treating TRL as an adjective (“high maturity”); averaging 4, 6, and 8 into 6; declaring readiness from a planned test; using similarity instead of configuration/environment comparison; calling a benign laboratory relevant; scaling output while ignoring heat, stress, timing, data, manufacture, or human behavior; assessing components but not integration; using successful nominal demonstration while hiding anomalies and failed boundary cases; equating a prototype with producibility or supportability; treating software age or deployment count as readiness; assuming heritage survives new hardware/load/interfaces; confusing feasibility with qualification/certification; selecting CTEs after test results; allowing developers alone to approve their evidence; and setting a target date without a maturation network, resources, or fallback.

### Compact example

A system has three critical elements: sensor TRL 6, processor TRL 8, and algorithm/application TRL 5. The arithmetic average is 6.33, but a gate requiring every CTE at least TRL 6 fails because the algorithm lacks a representative-environment demonstration. If the integrated chain also lacks representative interface/timing evidence, component scores cannot establish system readiness. The decision is to execute a bounded maturation demonstration or select a fallback—not round the average or relabel the environment.

### Connections

SYSENG-041–045 define decisions, tradeoffs, integrated forecasts, sensitivity, and uncertainty. Technology maturity is evidence feeding those models, not a replacement for them. SYSENG-047–048 turn remaining gaps into risk statements and controlled mitigation/retirement; SYSENG-049–050 preserve the decision and stakeholder trade. Architecture, interfaces, integration, verification, validation, configuration, cost, and schedule provide the application context and consequences.

## Governing Question

What exactly has been demonstrated, by which configured article, at what scale and integration, under which environment and acceptance criteria—and why is that evidence sufficient for the next irreversible commitment?

This question prevents the common slide from “a principle worked” to “the technology is ready for our system.” The distance may include material behavior, scale, manufacturing variation, interfaces, timing, algorithms, data, operators, facilities, safety/security controls, maintainability, mission duration, and adverse environments. A TRL summarizes demonstration history; the evidence package and gap analysis carry the meaning.

## Why This Matters

Immature technology can produce redesign, test failure, supplier dependence, requalification, performance shortfall, cost growth, and schedule delay. Prematurely freezing an acquisition around uncertain technology transfers discovery into the expensive integration path. Conversely, demanding operational proof too early can suppress valuable innovation. A credible TRA supports a staged decision: what is mature enough now, what evidence comes next, and what fallback protects the mission.

NASA's Technology Readiness Assessment Best Practices Guide standardizes definitions and evidence-oriented assessment for flight and research/technology work. NASA's Systems Engineering Handbook appendix emphasizes determining what was demonstrated and under what conditions, using the product breakdown, identifying the lowest critical maturity, and assessing advancement difficulty. It explicitly warns that changed architecture/environment can reduce the applicability of heritage evidence.

GAO's Technology Readiness Assessment Guide frames high-quality TRAs around credible, objective, reliable, and useful evidence, with critical-technology identification, independent assessment, and maturation planning. DOE guidance similarly connects TRAs and TMPs to major project decisions. ISO 16290 defines TRLs and assessment criteria for space-system hardware and remains confirmed as an international standard. These schemes must be tailored to governing policy and domain; labels that look alike are not assumed equivalent without mapping.

## Prerequisites and Retrieval

Before continuing, retrieve:

1. mission/business outcomes, ConOps, stakeholders/users, lifecycle, system boundary, operating scenarios, mandatory requirements, acceptance authority, and decision gate;
2. current architecture/configuration, product breakdown, functional allocation, interfaces, enabling products, make/buy/reuse, suppliers, quantities, manufacture, operations, maintenance, and retirement;
3. environment definition including loads, duration, variability, physical conditions, data/workload, operators, cyber/threat, facilities, logistics, and coupled adverse states;
4. proposed CTE inventory with novelty, performance, scale, integration, supply/process, human, software, and failure rationales;
5. evidence: analyses, publications, prototypes, test plans/results, configurations, instruments, anomalies, uncertainty, independent replication/review, operational history, and data rights;
6. required TRL definitions under governing policy, entry/exit criteria, equivalent/mismatched frameworks, and related manufacturing/integration/adoption measures;
7. risk register, technical measures/margins, cost-loaded schedule, resources/facilities, AD2/gap analysis, TMP, fallback/descope, and decision records.

As a retrieval test, challenge “the supplier says it is TRL 7.” Ask: under which scale/framework; exact item/version; target application; relevant versus operational environment; interfaces and loads; duration/sample/acceptance; anomalies; who assessed; what changed; and what evidence is accessible. If the answer is a slide with an integer, readiness remains unsubstantiated.

## Learning Objectives

After completing this module, you should be able to:

1. define an application-specific TRA charter, terminology, target level, roles, and evidence standard;
2. identify CTEs systematically across the product, lifecycle, integration, supply, software, and human system;
3. operationalize relevant environment, representation scale/fidelity, and successful demonstration;
4. map evidence to every criterion of an applicable readiness level without interpolation or averaging;
5. audit heritage, supplier, prototype, software, scale-up, and integrated-demonstration claims;
6. distinguish TRL from integration, manufacturing, operational/adoption, qualification, and programmatic readiness;
7. evaluate current maturity separately from advancement difficulty, cost, schedule, and risk;
8. construct a TMP with evidence-producing activities, dependencies, resources, exit criteria, fallback, and gates;
9. organize competent and sufficiently independent assessment, dissent, provenance, and change control;
10. make and communicate a bounded technology decision with monitoring and reassessment triggers.

## Core Exposition

**Charter the TRA before scoring.** Record purpose/decision, sponsor and decision authority, system/application baseline, lifecycle phase, required level and policy, terminology, CTE-identification method, evidence cutoff, assessment and independent-review roles, conflicts, schedule, deliverables, adjudication, and change rules. Do not let results redefine “relevant” or remove inconvenient CTEs.

**Define the application baseline.** Describe functions/performance, architecture, interfaces, materials/processes, scale/quantity, quality/safety/security class, software/data/hardware context, operators, manufacture, verification, deployment, operations/support, and environments. One technology can have different readiness for two applications because conditions and required functions differ.

**Identify CTEs top-down and bottom-up.** Decompose products/functions and inspect anything novel or modified; exceeding demonstrated performance; exposed to new environment/scale/duration; dependent on new materials/process/supplier/facility; enabling a critical function; difficult to integrate, manufacture, verify, operate, maintain, or replace; or whose shortfall creates major consequence. Include cross-cutting interfaces and enabling technology that product-only decomposition misses.

**Record why each element is critical.** Link element to requirements, functions, interfaces, scenarios, failure consequences, novelty, evidence gap, and system decisions. Also record why screened elements are not critical and what change would reopen them. “COTS,” “heritage,” or “software” is not sufficient screening rationale.

**Operationalize terminology.** Define breadboard/model/prototype/actual system; low/high/representative fidelity; laboratory/relevant/operational environment; successful demonstration; critical function; scale; integration; and qualification for the domain. Relevant environment is a set of conditions and mechanisms, not merely a location. A chamber test can be relevant for thermal/vacuum but omit radiation, vibration, interfaces, duty cycle, operators, or contamination.

**Create an environment matrix.** Rows contain environmental dimensions and interactions: temperature, pressure, radiation, vibration, shock, humidity, dust/ice/corrosion, EMI/EMC, loads, duration/cycling/aging, power, data/workload, networks, cyber threats, human workflow, installation/maintenance, and supply/process variation as applicable. Columns compare test and target values, distributions/scenarios, fidelity, rationale, uncertainty, and gaps.

**Define the demonstrated article.** Capture unique configuration, drawings/code/model/data versions, materials/processes, supplier/lot, dimensions, scale, interfaces, firmware, instrumentation, calibration, test fixtures, simulators/stubs, operators, and deviations. “Prototype tested” cannot be reviewed without knowing what the prototype represented and omitted.

**Map evidence criterion by criterion.** For each candidate level, cite the artifact/result satisfying every required criterion. Record missing/partial/contradictory evidence, test acceptance, uncertainty, anomalies, and applicability. Assign the highest level fully supported, not an interpolated decimal or aspirational target. A higher-level-looking test does not necessarily repair missing lower-level knowledge if its success cannot establish the omitted criterion.

**Judge successful demonstration.** Predefine functional/performance thresholds, duration/cycles/sample size, boundary/adverse cases, interfaces, safety/security, repeatability, allowable anomalies, data quality, and analysis. Report all runs and modifications. A demonstration that succeeds after unbaselined tuning or excludes failed trials can still be useful learning, but it does not support the claimed configuration without explicit evidence.

**Treat negative evidence as information.** Failure, anomaly, instability, drift, discrepancy, and unexpected interaction identify mechanisms and gap work. Perform root/contributing-cause analysis, update model/requirements/design/risks, repeat only under controlled rationale, and preserve the history. A passed rerun does not erase an unexplained prior failure.

**Audit heritage transfer.** Compare old and new functions, architecture, interfaces, performance margin, environment, scale, duration, supplier/process, components, software/data, operators, maintenance, and assurance. Establish equivalence dimension by dimension or identify delta qualification/maturation. Operational history in benign conditions does not prove readiness in a new environment.

**Audit supplier evidence.** Obtain sufficient raw/controlled data, configuration, methods, acceptance criteria, anomalies, uncertainty, and review rights. Check whether the supplier's application and framework match yours. Contractual warranty or fixed price changes commercial allocation, not technical consequence. Independently witness, replicate, inspect, or test proportionate to criticality.

**Handle software-enabled technology explicitly.** Define algorithm, code, runtime/hardware, data, models, dependencies, interfaces, timing/resources, security, configuration/update mechanism, human decisions, and operational distribution. Demonstration on synthetic/training data or faster desktop hardware may not transfer. Separate new technological feasibility from disciplined software engineering, verification, validation, assurance, deployment, and sustainment.

**Treat scale as mechanisms, not a multiplier.** Scaling can change surface/volume ratios, heat/mass transfer, stress, turbulence, control authority, manufacturing yield, calibration, data volume, concurrency, coordination, supply, or human workload. Identify dimensionless/causal scaling relations and validate at enough fidelity. A half-scale article is representative only for stated phenomena.

**Assess integration maturity.** Components that separately meet high levels may fail through interface timing, loads, tolerance stack-up, emergent control, shared resources, environment coupling, data semantics, or human workflow. Identify the assembled unit and representative interfaces; evaluate integrated demonstrations. The system readiness cannot exceed evidence for its critical integrated behavior.

**Do not confuse adjacent readiness constructs.** TRL describes technological demonstration maturity. Manufacturing readiness addresses repeatable production, yield, quality, supply and capacity. Integration readiness addresses interface/assembly behavior. Operational/adoption readiness addresses organization, workforce, regulation, business, infrastructure, user acceptance and sustainment. Qualification/certification verifies specified compliance under governed processes. Cost/schedule confidence addresses delivery commitments. Report the multidimensional profile.

**Separate current TRL from advancement difficulty.** Moving from 4 to 5 can be trivial or program-threatening depending on environment facilities, scale, physics, supplier, data, regulatory/ethical constraints, and integration. Assess gaps, novelty, uncertainty, dependencies, resources, facilities, lead time, testability, consequences, and fallback. Do not estimate schedule from the count of TRL steps.

**Build the TMP backwards from evidence.** For each gap define objective, baseline, entrance criteria, article, environment, procedure/model/test, measures/acceptance, work packages, owners, resources/facilities/suppliers/data, dependencies, cost/schedule, risk, decision points, exit artifacts, independent review, reassessment, and configuration control. Include learning iterations and time to analyze anomalies rather than one success-only test date.

**Link maturation to the integrated plan.** Map activities to WBS and logical schedule, cost/resource model, technical measures/margins, risk scenarios, suppliers/facilities, reviews, and architecture freeze/integration dates. Technology maturation should occur before its uncertainty becomes embedded in committed product development when feasible. Protect fallback decision lead time.

**Define off-ramps and alternatives.** Maintain fallback technology, architecture accommodation, modular interface, requirement descope, operational constraint, staged deployment, or stop condition. Define dates and evidence thresholds for switching. A fallback that shares the same immature supplier/process or cannot be integrated in time is not independent protection.

**Organize competent objective assessment.** Include application/system users, relevant disciplines, integration, verification/test, manufacturing/supply, operations/maintenance, software/data, human factors, safety/security, cost/schedule/risk, and domain experts as applicable. Reviewers should not have incentives that make level inflation invisible; disclose conflicts and preserve dissent.

**Report a readiness evidence matrix.** For every CTE show required/current level, criteria, evidence, application/environment/scale, gaps/anomalies, confidence/limitations, AD2, maturation plan, cost/schedule/risk, fallback, owner, and reassessment date. Provide drill-down artifacts; do not compress the decision into a heat map.

**Make the gate decision explicitly.** Choices include proceed because all conditions hold; proceed conditionally with bounded parallel maturation; delay commitment; select mature alternative; change architecture/requirements; conduct an information-producing prototype; or stop. State accepted residual risk and authority. A waiver does not increase TRL; it changes the decision condition.

**Control changes and reassess.** Trigger review on requirements/architecture/interface/environment/scale/supplier/material/process/software/data/facility/operational changes, anomaly, failed test, new evidence, or maturation-plan slip. Preserve prior claims and exact deltas. Technology can become less ready for a changed application even though knowledge has increased.

The following checker illustrates weakest-link gate logic. Its input levels are declared assessment results; the code does not assign official TRLs.

<!-- bijux-verify: {"id":"technology-readiness-gate-check","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"critical_count=3\ntrl_sensor=6\ntrl_processor=8\ntrl_algorithm=5\nlowest_trl=5\naverage_trl=6.33\ntarget_trl=6\nall_at_target=0\nshortfall_count=1\nmissing_integration_evidence=1\ndecision=not_ready_for_target\nevidence=declared_assessment_only\n","stderr":""}} -->
```python
critical = {"sensor": 6, "processor": 8, "algorithm": 5}
target = 6
integration_evidence = False
shortfalls = [name for name, level in critical.items() if level < target]

print(f"critical_count={len(critical)}")
for name in ("sensor", "processor", "algorithm"):
    print(f"trl_{name}={critical[name]}")
print(f"lowest_trl={min(critical.values())}")
print(f"average_trl={sum(critical.values()) / len(critical):.2f}")
print(f"target_trl={target}")
print(f"all_at_target={int(not shortfalls)}")
print(f"shortfall_count={len(shortfalls)}")
print(f"missing_integration_evidence={int(not integration_evidence)}")
ready = not shortfalls and integration_evidence
print("decision=" + ("ready_for_target" if ready else "not_ready_for_target"))
print("evidence=declared_assessment_only")
```

Even if all three inputs were 6 or higher, the gate would remain false until the required integration evidence existed. Real decisions also include policy, evidence quality, risk, cost, schedule, alternatives, and authority.

## Definitions and Notation

Let application baseline (B), product tree (P), CTE set (C\subseteq P), environment vector (E), demonstrated article (A_i), evidence set (D_i), applicable criteria for level (l), (K_l), and assessor judgment rule (J).

Evidence sufficiency for element (i) at level (l):

\[
S(i,l)=\bigwedge_{k\in K_l}J(D_i,A_i,B,E,k)=true.
\]

Assigned level:

\[
TRL_i=\max\{l:S(i,l)\},
\]

subject to the governing framework's cumulative/level rules. This notation exposes that evidence is evaluated for an application; it does not automate professional judgment.

Application-transfer delta can be organized as

\[
\Delta_i=(\Delta function,\Delta performance,\Delta architecture,\Delta interface,
\Delta scale,\Delta environment,\Delta process,\Delta operations).
\]

Zero unexplained material deltas supports reuse of evidence; any delta requires consequence and gap analysis, not an arbitrary TRL subtraction.

For target (l^*), readiness gap set is

\[
G_i=K_{l^*}\setminus K_i^{demonstrated},
\]

augmented by integration, anomaly, evidence-quality, and application-transfer gaps. The TMP maps every gap to evidence-producing work and decision criteria.

## Mechanisms, Invariants, or Proof Structure

**Mechanism 1—application and CTE framing.** Fix system, environment, scale, interfaces, decision, target, terminology, roles, and complete critical-element set.

**Mechanism 2—evidence mapping.** Define articles/environments/criteria, inspect traceable demonstrations and anomalies, and assign only the highest fully supported level.

**Mechanism 3—system and transfer challenge.** Apply weakest-link and integration reasoning; challenge heritage, supplier, software, scaling, manufacture, operations, and changed configurations.

**Mechanism 4—gap and maturation planning.** Assess advancement difficulty and map each gap to resources, schedule logic, risks, evidence, fallback, and reassessment.

**Mechanism 5—independent decision governance.** Review competence/conflicts/dissent, make bounded gate decision, preserve records, monitor changes, and reopen when applicability changes.

The readiness argument is evidential, not a theorem: if all applicable criteria are met by valid evidence for the intended application and integration, the declared level is supported. It cannot prove future success, manufacturability, certification, affordability, adoption, or absence of unknown failure modes.

## Alternatives and Trade-Offs

**TRL scales** provide shared ordinal language. **Evidence matrices/narrative assurance cases** retain application meaning and gaps. Use the level for indexing and the evidence for decisions.

**Component demonstrations** isolate mechanisms cheaply. **Integrated prototypes** reveal interfaces/emergence but cost more and may complicate diagnosis. Plan a learning sequence.

**Laboratory control** improves repeatability and instrumentation. **Relevant/operational testing** improves transfer but adds variability, hazard, access, ethics, and cost. Combine analysis, simulation, test, and operational evidence with explicit credibility.

**Independent assessment** reduces optimism/conflict. **Developer participation** supplies essential knowledge. Structure both, with decision authority separate and findings traceable.

**Mature fallback** reduces commitment risk but can reduce performance or add parallel cost. **Aggressive maturation** may unlock value but needs off-ramps and protected decision time.

**Tailoring** makes TRA proportionate to stakes/domain. **Standardization** supports comparability. Tailor definitions and evidence, not the conclusion desired.

## Failure Modes and Misconceptions

**“TRL is the probability the technology works.”** It is an ordinal demonstration-history classification, not calibrated probability.

**“The average TRL meets the gate.”** A low critical element can prevent the system; ordinal levels are not meaningfully averaged.

**“The supplier's TRL transfers.”** Only if framework, item, application, environment, interfaces, scale, and evidence applicability match.

**“Heritage means TRL 9.”** Prior operation applies to its configuration and environment; change can create new maturation needs.

**“All components are mature, so the system is mature.”** Integration evidence can be the missing critical technology.

**“A prototype proves production.”** It may omit manufacturing yield, quality, supply, maintainability, operations, certification, or cost.

**“A simulation demonstration is equivalent to the target environment.”** Only with sufficient model credibility and representation for the claimed criteria.

**“Passing nominal performance is enough.”** Duration, boundaries, variability, failures/anomalies, safety/security, interfaces, and uncertainty matter.

**“A waiver raises maturity.”** It authorizes a decision condition; evidence and level remain unchanged.

**“One TRL step equals a standard duration.”** Advancement difficulty depends on the actual gap, facilities, mechanisms, evidence, and integration.

## Worked Examples

### Example 1

**No averaging.** Sensor 6, processor 8, algorithm 5 average 6.33, yet a target of 6 fails. Report algorithm gap and integrated-chain evidence; never round an ordinal average into readiness.

### Example 2

**Heritage in a new environment.** A terrestrial pump operated for years but a new application changes fluid, pressure, radiation, thermal cycling, orientation, maintenance, and contamination. Map deltas and demonstrate relevant mechanisms; operational history remains useful but is not automatic target readiness.

### Example 3

**Half-scale thermal prototype.** Geometry is half scale while heat generation per volume and cooling area scale differently. State which thermal/fluid dimensionless relationships are preserved and validate the extrapolation. Visual similarity is not representative thermal evidence.

### Example 4

**Software/data context.** An algorithm works on curated offline data but target use has sensor drift, missing fields, distribution shift, latency/resource constraints, operator override, cyber manipulation, and safe-state needs. Assess the configured algorithm-runtime-data-human chain under representative conditions.

### Example 5

**COTS processor.** A commercial processor is widely deployed, but target radiation, temperature, deterministic timing, lifecycle supply, firmware, and safety assurance differ. Separate processor heritage from application readiness and plan screening, mitigation, qualification, or alternative.

### Example 6

**Successful test with anomaly.** All primary metrics pass, but an unexplained reboot occurs once in 20 cycles. Preserve and investigate it; do not call it irrelevant because the final cycle passed. Readiness depends on consequence, cause, reproducibility, and closure evidence.

### Example 7

**Integration is the technology.** Two high-maturity converters oscillate when connected through a shared control bus and load. Component levels do not cover coupled stability. The assembled interface/control behavior becomes a CTE with representative integration evidence.

### Example 8

**AD2 contrast.** Two elements are both TRL 4. One needs an available chamber test at full scale; the other needs a new material process, supplier line, tenfold scale, long-duration exposure, and unavailable facility. Same current level, radically different maturation risk.

### Example 9

**Fallback expiry.** A mature fallback requires interface freeze by month 8; primary demonstration ends month 10. Without an earlier decision point or adaptable interface, the fallback is fictional. Put the off-ramp and lead time into the integrated schedule.

### Example 10

**Changed configuration after assessment.** Supplier substitutes material and firmware after TRA. Reassess delta effects on demonstrated functions, environment, manufacture, interfaces, safety/security, and anomalies. Keep the prior claim attached to the old configuration.

## Cross-Program Connections

**Platform engineering.** Platform readiness includes control-plane/data-plane behavior, workload/tenant scale, failure domains, upgrades, security, developer operations, vendor dependencies, and adoption; production use elsewhere is not automatic heritage.

**API and service engineering.** New protocols, runtimes, consistency mechanisms, gateways, or cryptography require representative payload, concurrency, dependency, failure, version, migration, and operational evidence.

**Data engineering.** Engines, formats, stream semantics, models, and governance capabilities need representative data volume/skew/quality, replay, lineage, privacy, operations, failure, and migration demonstrations.

**Object-oriented programming.** Framework/library maturity depends on target runtime, language/version, workload, concurrency, security, team/tooling, integration, support, and evolution—not download count.

**Functional programming.** Language/runtime/effect/concurrency technology needs representative performance, interoperability, operations, ecosystem, migration, maintainability, and team evidence beyond elegant prototypes.

## References

1. NASA, *Technology Readiness Assessment Best Practices Guide*, NASA/SP-20205003605, 2020. <https://ntrs.nasa.gov/citations/20205003605>
2. NASA, *Systems Engineering Handbook, Appendix G: Technology Assessment/Insertion*, current web edition. <https://www.nasa.gov/reference/appendix-g-technology-assessment-insertion/>
3. NASA, *Systems Engineering Handbook Appendix: Establishing TRLs*, current web edition. <https://www.nasa.gov/reference/system-engineering-handbook-appendix/>
4. NASA Earth Science Technology Office, *Technology Readiness Levels*, current hardware/software criteria. <https://esto.nasa.gov/trl/>
5. NASA Software Engineering Handbook, *Software Technology Readiness Levels and Milestone Review Alignment*, current web edition. <https://swehb.nasa.gov/spaces/SWEHBVD/pages/240222216/7.12+%E2%80%93+Software+Technology+Readiness+Levels+(STRLs)+and+Milestone+Review+Alignment>
6. U.S. GAO, *Technology Readiness Assessment Guide*, GAO-20-48G, 2020. <https://www.gao.gov/products/gao-20-48g>
7. U.S. Department of Energy, *Technology Readiness Assessment Guide*, DOE G 413.3-4A, Change 1. <https://www.energy.gov/documents/technology-readiness-assessment-guide>
8. U.S. Department of Energy, *Project Management Directives*, current official index for DOE G 413.3-4A. <https://www.energy.gov/projectmanagement/directives>
9. ISO, *ISO 16290:2013 Space systems—Definition of the Technology Readiness Levels and their criteria of assessment*, confirmed 2024. <https://www.iso.org/standard/56064.html>
10. NASA/JPL, *JPL Technology Readiness Assessment Guideline*, official NTRS record. <https://ntrs.nasa.gov/citations/20190025499>

## Exercises

### Exercise 1

A system has CTE levels 7, 6, 4, and 8; its decision gate requires each CTE at least 6 and representative integrated evidence. Compute minimum and arithmetic average, determine gate status when integration evidence is present, and explain why the average is not a readiness result.

### Exercise 2

Create an application-transfer assessment for a battery demonstrated in ground delivery vehicles and proposed for an autonomous high-altitude aircraft. Identify environment, scale, duty, architecture, manufacture, operations, safety, software/control, and evidence deltas; state what current evidence can and cannot support.

### Exercise 3

Audit a supplier claim: “TRL 8 because the prototype passed a 30-minute demo.” The target requires 24-month outdoor operation, 10× throughput, a new enclosure/cooling system, two new interfaces, cybersecurity controls, remote maintenance, and production of 2,000 units.

### Exercise 4

Design a TMP for an integrated sensor/algorithm whose sensor is supported at target level but algorithm-chain evidence is one level short because representative rare-condition data and real-time hardware demonstration are missing. Include gaps, work, evidence, dependencies, resources, anomalies, decision points, fallback, and reassessment.

### Exercise 5

Design a TRA and gate recommendation for a municipal drinking-water treatment technology using a novel contaminant-removal medium. Cover CTEs, water/population/environment, scale/duration, byproducts, manufacturing/supply, operators, monitoring, waste/disposal, safety/regulation, evidence, independence, maturation, fallback, uncertainty, and community impacts.

## Answers to the Exercises

### Answer 1

Minimum is 4. Average is

\[
(7+6+4+8)/4=25/4=6.25.
\]

Even with representative integration evidence, the target condition fails because one CTE is below 6. The average has no valid compensatory meaning: TRLs are ordinal evidence categories, and the level-4 critical element can prevent the system function. Report every CTE, why it is critical, exact evidence/gap, current/target criteria, advancement difficulty, maturation schedule/resources/risks, and fallback. The gate remains not ready unless governing policy authorizes a bounded exception; such authorization does not change the CTE's level.

### Answer 2

Define battery chemistry/cell/module/pack/BMS configuration and compare vehicle versus aircraft functions and power/energy profiles. Deltas include altitude pressure, temperature extremes/gradients, radiation where relevant, vibration/shock, humidity/icing, thermal runaway propagation, oxygen/venting, fire containment, mass/volume constraints, climb/cruise/emergency peak loads, cycling/aging, charging, storage, dispatch reliability, autonomous fault response, communications, and safe landing.

Compare cell count/geometry, series/parallel architecture, cooling/enclosure, wiring/contactors, sensors, BMS hardware/firmware/algorithms/data, aircraft power/control interfaces, redundancy/common causes, maintainability, ground handling, charging infrastructure, emergency response, certification, and operator workflow. Manufacturing deltas include supplier/lot/process, quality/yield, traceability, transport, obsolescence, quantities, repair, and disposal.

Ground history supports chemistry/component behavior only within demonstrated configurations and conditions. It can inform models, failure mechanisms, aging, manufacture, and test ranges, but cannot prove aircraft pack integration, altitude thermal behavior, mass-constrained containment, target duty, autonomous fault management, certification, or flight consequence. Define CTEs at cell/pack/BMS/integration/enabling levels, create an environment/evidence matrix, analyze transfer deltas, then plan progressive cell/module/pack/hardware-in-loop/environment/aircraft demonstrations with anomalies, uncertainty, independent review, fallback chemistry/operating envelope, and reassessment.

### Answer 3

The claim omits applicable framework, target criteria, article configuration/scale, environment, performance thresholds, interfaces, anomalies, assessor, and evidence. A 30-minute prototype demonstration may support a lower-level function under its exact conditions; it cannot establish completed/qualified actual-system evidence for the target.

Map gaps: long-duration weathering/aging and maintenance; tenfold throughput with thermal/fluid/compute/resource scaling; new enclosure and cooling behavior; interface semantics/timing/failure; cybersecurity threat/control/update/recovery; remote diagnostics and human workflow; production process, yield, quality, suppliers, calibration, acceptance and field support for 2,000 units. Include safety, reliability, environmental, regulatory, cost/schedule, and operational consequences.

Obtain raw results, configuration, procedures, acceptance, all failures/tuning, uncertainty, and independent access. Identify CTEs including integrated scale/cooling/interfaces/security/maintenance/manufacture. Assign only the highest fully evidenced level under governing definitions. Build a staged TMP from accelerated/physics-informed aging and full-throughput prototypes through representative outdoor/integrated/pilot operation and production evidence, with decision gates and fallback. Manufacturing and operational readiness remain separate even after technological criteria improve.

### Answer 4

Define the target algorithm function, performance by rare condition/group, error consequence, sensor/input quality, hardware/runtime, latency/resources, interfaces, operators, environment, software/model/data versions, and target criterion. Gaps include representative rare-condition coverage and provenance; label/reference uncertainty; distribution/shift; real-time sensor-to-decision timing; compute/memory/power; interface loss/corruption; fallback/safe behavior; cybersecurity; repeatability; subgroup/adverse metrics; and integration anomalies.

Work packages: curate/acquire governed representative data with ethical/privacy controls; design rare-condition scenarios and coverage rationale; establish reference truth/uncertainty; freeze training/evaluation separation; run offline blind validation; implement on target hardware; verify code/runtime/resources; execute hardware-in-loop and representative environmental/operational tests; inject sensor/interface/timing faults; conduct human/safe-state evaluation; analyze discrepancies; independently reproduce key results. Each has entrance criteria, configured article/data, measures/thresholds, owner, resources/facilities, dependencies, cost/duration, and exit artifacts.

Link data availability before final model freeze, hardware before real-time integration, and anomaly-analysis/retest time before gate. Predefine stop/rework thresholds and decision dates. Fallback may be a validated simpler algorithm, constrained operating envelope, human confirmation, redundant sensing, or architecture accommodation; verify it does not share the same missing evidence and remains selectable in time. Reassess after evidence, anomalies, model/data/code/hardware/interface change, drift, or schedule slip. Do not increase the level from planned tests.

### Answer 5

Charter the specific contaminant(s), source-water systems/seasons/communities, treatment train, regulatory and health outcomes, decision gate, target readiness, applicable definitions, assessor independence, and evidence cutoff. CTEs may include medium chemistry/selectivity/capacity/regeneration, contactor/reactor and hydraulic scale, pretreatment interactions, byproduct/leaching control, online sensing/control, manufacture/quality/supply, waste/regeneration/disposal, and integration with existing operations. Record criticality and screened-element rationale.

Define relevant water matrices: contaminant concentration/speciation, pH, temperature, minerals, natural organic matter, competing contaminants, turbidity, microbes, disinfectants, seasonal/event variation, flow/load, residence time, cycling, fouling, and upset conditions. Representative demonstrations must address scale, duration, media aging/breakthrough, hydraulic behavior, treatment interactions, monitoring uncertainty, operators/maintenance, power/chemicals, safety/security, and waste fate—not only clean laboratory water removal.

Evidence progresses from mechanism and bench proof through representative-water columns, pilot scale, integrated plant demonstration, repeatability, target performance and boundary/upset cases. Preserve negative results, mass balances, byproducts, media constituents, uncertainty, raw data, configurations, methods, and independent laboratory/field review. Assess scale mechanisms, manufacturing lots/yield/contamination, supplier capacity/quality, transport/storage, regeneration/replacement, occupational exposure, residuals disposal, lifecycle cost, environmental justice, affordability, and community acceptance.

The TMP maps every criterion/gap to test/model/work, WBS/schedule/resources, facilities/water access, permits/ethics, owners, acceptance, anomaly resolution, risk, and reassessment. Fallback includes proven treatment, blending/source control, modular bypass, monitoring, safe shutdown, or phased pilot with protected decision lead time. Qualified water/process, chemistry/toxicology, public health, environmental, operations, analytical/metrology, manufacturing/supply, safety/security, regulatory, cost/schedule, and affected-community participants review.

Recommend proceeding only to the next bounded evidence stage unless every target criterion and integrated condition is met. Record residual uncertainty about rare water conditions, chronic byproducts, scale, supply, operations, waste, and community distribution; impose monitoring and reopening for source water, regulation, supplier/process, media, configuration, performance drift, breakthrough, byproduct, incident, or contradictory evidence. A TRL cannot itself establish regulatory approval, population health benefit, affordability, environmental acceptability, or equitable service.
