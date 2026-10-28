---
module_id: SYSENG-065
program: Systems Engineering
level: 2
module_number: 65
title: Maintainability and Repair
status: complete
last_verified: 2026-08-31
---

# Maintainability and Repair

## One-Page Review

### Governing question

How can systems be designed, supported, measured, and verified so authorized maintainers can detect, isolate, access, restore, verify, and safely return required capability within a stated time and resource envelope—without hiding diagnostic errors, logistics delay, induced faults, or long repair tails behind one MTTR average?

### Essential definitions

- **Maintainability** is the ability of an item, under stated conditions of use and maintenance, to be retained in or restored to a state in which it performs as required, when maintenance is performed under stated procedures and resources.
- The **maintainability function** $M(t)=P(T_R\le t)$ is the probability that a defined maintenance action/restoration is completed within time $t$ under declared conditions.
- **Maintenance** is the combination of technical, administrative, and managerial actions intended to retain or restore an item. **Corrective maintenance** follows a fault/failure; **preventive maintenance** seeks to reduce failure/degradation risk before functional failure.
- **Repairability** concerns the physical/logical ability to restore an item. **Diagnosability** concerns detecting and isolating the relevant fault/state. **Testability** is a design characteristic enabling determination of status and isolation through tests.
- A **maintenance concept** defines what is repaired, replaced, discarded, deferred, remotely restored, or returned to supplier; at which organizational/depot/location level; by whom; with which tools, spares, data, facilities, and constraints.
- A **line-replaceable unit (LRU)** is an item designated for replacement at a stated maintenance level. A **shop-replaceable unit (SRU)** is repaired/replaced within an LRU at another level. These are support decisions, not intrinsic sizes.
- **Fault detection** decides that abnormal behavior exists. **Fault isolation** identifies the replaceable/repairable cause to a declared ambiguity group. **Fault identification** may characterize exact mode/mechanism. These capabilities differ.
- **Diagnostic coverage** is the fraction/probability of relevant faults detected or isolated within required time and conditions. Its denominator and evidence must be defined.
- A **false alarm** declares a fault when the target condition is absent. **No fault found (NFF)** records failure to confirm/isolate a reported fault; it is a diagnostic/process outcome, not proof no fault existed.
- **Active corrective maintenance time** can include diagnosis, access, remove/replace/repair, reassembly, adjustment, checkout and return-to-service steps under a declared convention. **Maintenance downtime** may additionally include logistics and administrative delay.
- **Mean time to repair/restore (MTTR)** is ambiguous until the measured event boundaries, action population, weighting, exclusions and distribution are stated.
- A **maintenance task analysis (MTA)** decomposes tasks into triggers, prerequisites, personnel/skills, tools, data, spares, access, steps, times, hazards, verification, waste and restoration.
- **Maintenance-induced failure** is damage, misconfiguration, contamination, wrong installation, latent fault, security exposure, or unsafe state introduced through maintenance.
- **Level of repair analysis (LORA)** evaluates repair/discard/location alternatives across performance, risk, resources and lifecycle cost; the cheapest unit repair is not necessarily the best system policy.

### Central model, mechanism, or theorem

Represent one corrective restoration in configuration/context $c$ as a chain

$$
T_R=T_{detect}+T_{isolate}+T_{safe}+T_{access}+T_{restore}+T_{reassemble}+T_{verify}+T_{return},
$$

with explicit overlap rather than blind addition when phases proceed concurrently. Logistics and administrative delay can be modeled separately:

$$
T_D=T_R+T_{logistics}+T_{administrative}.
$$

Maintainability is the distribution $M(t)=P(T_R\le t)$, so a requirement should usually include a percentile/probability, such as $M(60\text{ min})\ge0.9$, not only $E[T_R]$.

If restoration time is exponentially distributed with rate $\mu$, then $M(t)=1-e^{-\mu t}$ and $E[T_R]=1/\mu$. If lognormal, then

$$
M(t)=\Phi\left(\frac{\ln t-\mu_{\ln}}{\sigma_{\ln}}\right).
$$

These are candidate statistical models, not design laws. Repair times are often skewed, multimodal, censored, learning-dependent, and conditioned on fault/task/resources.

### Critical invariants

- Maintainability requirements name item/function, configuration, failure/task population, maintenance level, environment, personnel/skill, tools/spares/data/facilities, time origin/end and probability/percentile.
- The maintenance concept and system architecture co-evolve; LRU/SRU boundaries, accessibility, modularity, standardization, redundancy and fault containment are decided before the design freezes.
- Detect, isolate, safe, access, restore, reassemble, verify and return are distinct evidence-bearing phases. Success in one does not imply the next.
- Diagnostic coverage, ambiguity, false alarm, missed detection, isolation error and NFF are measured against a declared fault set and operating modes.
- Maintenance cannot create an unrecognized unsafe or insecure condition. Lockout/tagout, stored energy, contamination, radiation, software/configuration integrity and independent verification are designed in.
- Human reach, posture, force, visibility, protective equipment, cognitive load, labeling, connectors, accessibility and representative environments are verified with intended maintainers.
- Tools, test equipment, adapters, software, cryptographic credentials, technical data, spares and calibration are configuration-controlled and available at the credited level.
- Time observations preserve full distributions/tails and phase decomposition; means are not used as percentile guarantees.
- Demonstrations sample representative faults/tasks/people/configurations and disclose selection, learning, censoring, retries, exclusions and confidence.
- Repair/restoration actions verify required end-to-end function and absence of induced faults, not merely replacement completion or a green built-in test.
- Field discrepancies update design, diagnostics, procedures, spares, training, time models and affected configurations while retaining historical baselines.
- Maintainability contributes to availability and lifecycle support but does not prove reliability, safety, correct diagnosis, supply availability, or repair effectiveness by itself.

### Common failures

Common failures include specifying only “MTTR < 30 min”; starting the clock after diagnosis or parts arrival; choosing LRUs solely by packaging; hiding inaccessible fasteners and connectors; requiring special tools not deployed; using destructive access; placing test points where maintainers cannot reach safely; using identical connectors without keying; ambiguous labels; built-in tests with unknown coverage; alarms that identify symptoms rather than cause; false removals and NFF loops; treating software restart as repair without state/configuration validation; counting expert prototype technicians as representative; stopping a timed demonstration on the first failed attempt; excluding long repairs as outliers; failing to restore guards, seals, calibration or security; verifying only nominal operation; and optimizing repair time while increasing failure probability, hazard, inventory or lifecycle cost.

### Compact example

Seven synthetic corrective tasks include detect, isolate, access, restore and verify phases. Total active restoration times are 35, 43, 30, 65, 52, 38 and 120 minutes: mean 54.7143, median 43, nearest-rank 90th percentile 120, five of seven complete within 60 minutes, and six within 90. Separate diagnostic records show 17 correct isolations and three false removals in twenty attempts. The fixture verifies arithmetic and exposes the long tail; it does not establish a distribution, confidence, representative sampling, safe repair or any system requirement.

### Connections

SYSENG-064 shows how restoration affects availability; SYSENG-065 makes restoration a design and evidence problem. FMEA supplies failure/task populations, fault trees and diagnostics expose isolation needs, configuration management controls interchangeable replacements and software, and human factors/safety govern maintenance execution. Platform/API/data engineering provide telemetry, remote diagnostics, rollback and histories but introduce authorization and dependency failures.

## Governing Question

Can an intended maintainer, in the representative environment and with only credited resources, correctly detect and isolate a representative fault, make the system safe, reach and restore the intended item, verify full required behavior and configuration, and return it to service within the stated probability/time—without introducing another fault or relying on hidden expert intervention?

Maintainability is designed before it is measured. Once enclosure, routing, interfaces, diagnostics, modularity, access and support concept are fixed, a procedure can document difficulty but rarely remove it.

## Why This Matters

Systems spend decades being inspected, updated, calibrated, repaired and modified. Poor maintainability extends outages, drives false removals and spares, exposes maintainers to hazards, creates configuration errors, obscures intermittent faults and raises lifecycle cost. It can defeat redundancy when repair/test disables multiple channels or introduce latent failures through incorrect restoration.

IEC 60300-3-10:2025 treats maintainability and maintenance across the lifecycle and their interfaces with reliability, availability and supportability. IEC 60706-2 addresses requirements and design/development studies; IEC 60706-3 covers verification and data collection; IEC 60706-5 addresses early testability/diagnostics. IEC 60300-3-14:2024 connects supportability and support to performance, cost and risk.

NASA maintainability material frames the chain as diagnose (detect/isolate), restore (repair/validate), and ensure operation, and its engineering case includes maintenance concept, accessibility, fault localization, LORA, LRU identification, prediction and demonstration. This establishes that maintainability is not a late logistics appendix. It is an integrated system quality.

## Prerequisites and Retrieval

Before establishing or accepting maintainability/repair evidence, retrieve:

1. operational/maintenance concept, mission/site constraints, maintenance levels, repair/discard policy, remote support, deferral and restoration authority;
2. item/function/configuration, required capability, failure/task populations, FMEA/FTA/fault-management links, criticality and safe/degraded states;
3. quantitative requirements for $M(t)$, phase times, detection/isolation coverage, ambiguity, false alarms, false removals, NFF, personnel and induced faults;
4. architecture, LRU/SRU boundaries, interfaces, accessibility envelopes, fasteners/connectors, lifting/handling, modularity, interchangeability and standardization;
5. diagnostic sensors, tests, thresholds, fault dictionary, modes/states, coverage evidence, testability model, logs, remote data and failure injection;
6. task analyses, procedures, drawings, parts/tool/test-equipment lists, calibration, software/firmware/configuration/credentials and technical-data versions;
7. personnel skill/authorization, training, staffing/shifts, human-factors ranges, protective equipment, environmental restrictions and communication;
8. spares, repairables, stock/location/replenishment, obsolescence, supplier/depot turnaround, transport, facilities and competing-resource queues;
9. verification/demonstration plan, representative fault/task sampling, maintainers, environments, instrumentation, clock rules, retries, censoring and confidence method;
10. work orders, telemetry, false alarms/NFF, repeat repairs, induced damage, near misses, parts consumption, phase timestamps, configuration changes and corrective actions.

Use a retrieval challenge: follow one long or repeated repair from first symptom through detection, isolation, safeing, access, parts/data/tool availability, restoration, checkout, authorization and recurrence. Compare real timestamps and interventions to the credited model. Missing phases are evidence gaps, not zero-duration tasks.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish maintainability, maintenance, repairability, diagnosability, testability, supportability and availability;
2. define a maintenance concept, levels of repair and LRU/SRU boundaries;
3. specify maintainability distributions, percentiles and task/clock/resource conditions;
4. decompose corrective maintenance and distinguish active time from logistics/administrative delay;
5. design accessibility, modularity, interchangeability, human factors, testability and diagnostic coverage;
6. analyze false alarms, ambiguity, NFF, intermittent faults, software restoration and induced failures;
7. perform maintenance task and level-of-repair trade analyses;
8. design representative maintainability verification/demonstration and interpret samples with uncertainty;
9. close the loop from field repair evidence to design, diagnostics, procedure, support and configuration;
10. communicate bounded maintainability conclusions without converting means into guarantees.

## Core Exposition

**Define the maintenance concept early.** Decide which failures can be deferred, reset, reconfigured, repaired in place, replaced at line, repaired at shop/depot/supplier, or discarded. State site, environment, skill, crew, tools, data, spares and turnaround. Architecture must support that concept; otherwise availability and cost models rest on impossible restoration.

**Derive requirements from user need.** Specify probability of restoration by time for representative task classes, maximum constraints for critical tasks, detection/isolation metrics, ambiguity, false alarms, personnel, environment and support. A single average across trivial and complex tasks hides the failures that determine operations.

**Allocate maintainability carefully.** Allocate system restoration objectives to detection, isolation, access, replacement/repair, checkout and supporting subsystems using task frequency/criticality and architecture. Allocations are design targets, not measured evidence. Reconcile bottom-up task predictions and demonstrations.

**Select repair level and boundaries.** LORA considers downtime, skill, transport, spares, test equipment, repair yield, condemnation, intellectual property, security, cost and risk. A small LRU may improve isolation and inventory but increase connectors/handling; a large LRU speeds line swap but raises spares cost and depot burden.

**Design accessibility.** Provide clearance, reach, visibility, lifting/fixtures, captive fasteners, service loops, drainage, contamination control and non-destructive access. Sequence access so one repair does not require removing unrelated critical items. Evaluate actual postures, gloves, lighting, gravity and restricted spaces.

**Design modularity and interchangeability.** Stable mechanical/electrical/fluid/data/configuration interfaces enable replacement. Key/connect uniquely, prevent wrong orientation, identify effectivity and calibrations, and verify compatibility. Physical fit does not prove firmware, keys, datasets or parameters match.

**Design safe maintenance states.** Identify hazardous energy, pressure, heat, motion, chemicals, radiation, stored charge, lifting, contamination and cybersecurity. Provide isolation, discharge, lockout, interlocks, monitoring and controlled overrides. Maintenance modes must not disable protections silently or propagate unsafe commands.

**Engineer testability.** Begin from fault set and isolation requirement. Place sensors/test points with observability, controllability, resolution, timing and access. Model ambiguity groups and test sequence. A pass/fail light may detect loss but cannot isolate an LRU; excessive sensors can add faults and false alarms.

**Measure diagnostics honestly.** Define denominators: all credible faults, weighted field faults, injected faults or a bounded subset. Separate detection, isolation-to-one, isolation-to-group, missed detection, false alarm and false isolation. Include mode/phase/configuration, latency and unavailable sensors. Do not call a fault “covered” because one lab test detected it once.

**Handle intermittent and NFF events.** Preserve symptom, environment, time, configuration, telemetry and previous actions. Avoid replacing parts until symptom disappears without causal evidence. Reproduce stress, inspect connectors/log timing, and retain returned-unit findings. NFF can mean diagnostic insufficiency, transient environment, configuration mismatch or evidence loss.

**Treat software restoration as engineering.** Restart, failover, rollback, redeploy, restore data/configuration, rotate credentials and patch can restore service or corrupt state. Define authority, rollback compatibility, persistence, data integrity, cybersecurity, observability and end-to-end verification. “Reboot fixed it” is symptom recovery, not root-cause closure.

**Write maintenance task analyses.** For each representative task capture trigger, prerequisites, safeing, steps, dependencies, people/skills, tools/test equipment, consumables/spares, data, access, time distributions, hazards, waste, verification and return-to-service. Identify opportunities for parallel work without unsafe coordination.

**Predict with distributions.** Use analogous task elemental times, expert judgment, prototypes/digital human models and historical data, preserving uncertainty and correlations. Exponential repair is convenient but often unrealistic. Lognormal/gamma/mixture/empirical distributions can represent skew; multimodal tasks may reflect different isolation paths or resource availability.

**Separate clocks.** Active hands-on maintenance, total active corrective time, logistics delay, administrative delay and overall downtime serve different owners/measures. Define pause rules for waiting, shift changes, test, unsuccessful attempts and remote escalation. Preserve phase timestamps so improvement targets the real bottleneck.

**Design verification and checkout.** Confirm the replaced/repaired item, interfaces, configuration, calibration, containment, guards, tools/material removal and full required function under relevant load/mode. Built-in test may share the failed sensor/software. Independent or diverse checks are needed for high consequence.

**Prevent induced failures.** Use keyed interfaces, torque control, contamination barriers, foreign-object accounting, automated configuration checks, independent inspection, safe test modes and tamper-evident records. Track repeat failures shortly after maintenance and expand FMEA/hazard analysis when work creates new modes.

**Plan demonstrations statistically and operationally.** Sample tasks by frequency, criticality, architecture and difficulty rather than choosing easy cases. Use representative trained—not handpicked expert—maintainers and production-representative equipment, procedures and conditions. Predefine success, timing, retries, failures, censoring and confidence.

**Account for learning.** Demonstration repetitions can improve time through familiarity not available in the field. Randomize/rotate tasks and personnel where possible; distinguish first-time from practiced performance. Procedure or design learning is valuable, but do not use a rehearsed team to claim fleet-wide maintainability.

**Analyze observations.** Report mean, median, percentiles, exceedance probabilities, phase contributions, right-censored tasks and confidence/credible intervals. Repair times are often skewed, so a single long repair can be operationally real rather than a removable outlier. Stratify by task/fault/resource/configuration.

**Integrate logistics and workforce.** A quickly replaceable LRU still yields long downtime when no spare, tool, credential or qualified person exists. Connect task demand to stock, repair pipeline, replenishment, shifts, skills, facilities and priority queues. Keep design maintainability and support delay separately visible.

**Use remote and predictive maintenance cautiously.** Telemetry can detect degradation and stage resources; remote commands can restore service. Validate sensor drift, model false positives, communications, security, privacy, degraded connectivity and safe authorization. Prediction shifts maintenance timing and can increase unnecessary work if thresholds are weak.

**Close field feedback.** Link faults, diagnostic paths, removals, repair findings, parts, times, induced issues and repeat events to exact configuration. Update failure dictionaries, procedures, training, spares and design. Preserve prior baselines and distinguish containment from root-cause corrective action.

**Control lifecycle evolution.** New variants, firmware, tools, suppliers and obsolescence change interchangeability and restoration. Revalidate task/effectivity and diagnostic coverage. Archive executable technical data and recovery media/keys; a maintained system must remain supportable after original tools disappear.

The following fixture recomputes phase totals and simple diagnostic proportions for declared synthetic observations.

<!-- bijux-verify: {"id":"maintainability-task-fixture","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"tasks=7\nphases_per_task=5\nrestoration_minutes=35,43,30,65,52,38,120\nmean_restoration_minutes=54.7143\nmedian_restoration_minutes=43\nnearest_rank_p90_minutes=120\ncompleted_within_60_minutes=5\ncompleted_within_90_minutes=6\ncorrect_isolation_fraction=0.8500\nfalse_removal_fraction=0.1500\nstatus=declared_maintainability_fixture_passed\nevidence=synthetic_task_observations_only\n","stderr":""}} -->
```python
tasks = [
    (4, 6, 8, 10, 7),
    (5, 8, 10, 12, 8),
    (3, 5, 7, 9, 6),
    (8, 12, 15, 20, 10),
    (6, 10, 12, 15, 9),
    (4, 7, 9, 11, 7),
    (15, 25, 20, 35, 25),
]
totals = [sum(task) for task in tasks]
ordered = sorted(totals)
diagnostic_attempts = 20
correct_isolations = 17
false_removals = 3
print(f"tasks={len(tasks)}")
print(f"phases_per_task={len(tasks[0])}")
print("restoration_minutes=" + ",".join(str(total) for total in totals))
print(f"mean_restoration_minutes={sum(totals) / len(totals):.4f}")
print(f"median_restoration_minutes={ordered[len(ordered) // 2]}")
print(f"nearest_rank_p90_minutes={ordered[-1]}")
print(f"completed_within_60_minutes={sum(total <= 60 for total in totals)}")
print(f"completed_within_90_minutes={sum(total <= 90 for total in totals)}")
print(f"correct_isolation_fraction={correct_isolations / diagnostic_attempts:.4f}")
print(f"false_removal_fraction={false_removals / diagnostic_attempts:.4f}")
print("status=declared_maintainability_fixture_passed")
print("evidence=synthetic_task_observations_only")
```

These seven selected tasks and twenty diagnostic attempts are too small and unspecified for population inference. The nearest-rank percentile is an empirical order statistic, not a fitted 90th-percentile guarantee.

## Definitions and Notation

Let $T_R$ be restoration time under a specific task/fault/maintainer/resource/context population. Maintainability is $M(t)=F_{T_R}(t)$. For requirement time $t_r$, compliance concerns $P(T_R\le t_r)$ and its uncertainty, not merely $E[T_R]$.

Let fault set $F$, detection result $D$, isolation result $I$ and declared ambiguity group $G(f)$. Useful measures include

$$
C_D=P(D=detected\mid f\in F),
\qquad
C_I=P(I\in G(f)\mid D=detected,f\in F),
$$

with explicit weighting, modes and time limits. False-alarm probability/rate conditions on absence of target faults and observation opportunities; define its denominator.

For right-censored task time $T>c$, recording $c$ as completed biases restoration downward. Survival-analysis or bounded reporting should retain censoring.

## Mechanisms, Invariants, or Proof Structure

A defensible maintainability claim follows this chain:

1. **Requirement validity:** task/fault population, maintainer/resources/environment, time clock and probability target match operational need.
2. **Design validity:** maintenance concept, item boundaries, access, safety, modularity, interfaces, diagnostics and verification enable the task.
3. **Support validity:** people, skills, data, tools, test equipment, spares, facilities and authorization exist at the credited level.
4. **Measurement validity:** representative sampling, timing, attempts, learning, exclusions, censoring and diagnostic denominators are controlled.
5. **Statistical validity:** distribution/percentile/uncertainty methods match data and stratification; means are not misused.
6. **Restoration validity:** end-to-end function/configuration/safety/security are verified and induced failures addressed.
7. **Lifecycle validity:** field discrepancies and changes update design/support/evidence while preserving prior decisions.

A fast part swap that leaves the wrong configuration or fails verification is not a successful restoration.

## Alternatives and Trade-Offs

**Repair in place versus LRU replacement.** In-place repair reduces spares mass/cost but needs skill, access, time and test. LRU swap shortens line time but raises inventory, connectors, configuration and depot burden. Evaluate complete pipeline.

**Built-in versus external diagnostics.** Built-in test provides rapid operational detection but adds sensors/software and common failures. External test can be richer/independent but requires tools/access. Combine according to consequence and isolation need.

**Modularity versus integration.** Modularity improves replacement and ownership but adds interfaces, mass, volume and possible failure points. Integrated designs can improve performance/reliability yet become difficult to diagnose/repair. Optimize lifecycle system value.

**Preventive versus corrective maintenance.** Preventive work can reduce failures but creates downtime, labor and induced risk. Condition-based maintenance can target need but depends on diagnostic validity. RCM and evidence guide policy.

**Local versus centralized/depot support.** Local capability reduces transport delay but duplicates skill/tools/spares. Central repair concentrates expertise but adds logistics and resilience risk. Consider mission criticality, geography and supply disruption.

**Repair versus discard.** Discard can simplify line support for low-cost items; repair reduces waste/supply demand and enables failure analysis. Include data rights, environmental obligations, obsolescence and learning.

## Failure Modes and Misconceptions

- **“Maintainability is MTTR.”** It includes design, diagnostics, safety, resources, task distributions and verification; MTTR needs a clock definition.
- **“Fast replacement means fast restoration.”** Detection, access, spares, configuration and checkout may dominate.
- **“Built-in test found the failed box.”** Coverage, ambiguity, false isolation and shared-test failures require evidence.
- **“No fault found means no fault.”** The fault can be intermittent, contextual, masked, misconfigured or lost with evidence.
- **“Repair is complete when the new part is installed.”** Reassembly, configuration, verification and safe return remain.
- **“Experts prove maintainability.”** Representative authorized maintainers and environments matter; rehearsal/learning can bias time.
- **“Outliers can be deleted.”** Long-tail repairs may dominate operational risk; investigate before exclusion.
- **“Software is infinitely repairable.”** State, data, compatibility, credentials, rollback and root cause constrain restoration.
- **“More diagnostic sensors always help.”** They add cost, faults, false alarms, calibration and cognitive load.
- **“Maintenance cannot reduce safety.”** Disabled protection, wrong parts, contamination, latent configuration and test errors can introduce hazards.

## Worked Examples

### Example 1

A pump is behind two panels and pipework, so its 10-minute replacement becomes a four-hour restoration. Move it to an accessible LRU location with quick-disconnects, lifting support and keyed interfaces. Verify pressure isolation, drainage, contamination, reconnection and full-load leak/function tests. The improvement is end-to-end, not stopwatch removal alone.

### Example 2

Built-in test reports one of four cards but isolates correctly only to a two-card ambiguity group. Operators replace both, doubling spares and false removals. Add discriminating test points or an external test sequence; measure isolation-to-one/group, false isolation and time. A higher detection percentage alone does not solve ambiguity.

### Example 3

Two repair designs both average 45 minutes. Design A is tightly clustered around 45; Design B usually takes 20 but occasionally eight hours when a connector seizes. A 90-minute operational objective favors A unless B's tail cause is removed. Report percentiles and exceedance, not average-only equivalence.

### Example 4

A software service is restored by rollback in six minutes, but the old version cannot read the migrated database. Successful process restart produces corrupt behavior. The restoration chain includes schema compatibility, data integrity, credential/configuration state, canary verification and forward recovery. Rollback speed without end-to-end correctness is not maintainability.

### Example 5

Three identical unkeyed connectors fit adjacent ports. A maintainer swaps two and built-in test passes at idle. Keying, distinct labels, harness reach constraints and automated pin/configuration verification prevent the error. Representative test under poor lighting and gloves checks human factors and full-load behavior.

### Example 6

A field NFF cluster appears only under vibration and cold. Bench testing at room temperature erases the symptom. Preserve logs, returned configuration and connector state; reproduce environment; use high-rate telemetry and inspect fretting. Avoid repeated component swaps that destroy causal evidence and inflate parts demand.

### Example 7

LORA compares line repair, LRU swap/depot repair and discard. Line repair is cheapest per action but needs scarce skill and long downtime; discard increases supply vulnerability; LRU swap requires costly spares but meets mission recovery. Sensitivity to failure demand, transport and obsolescence yields a mixed policy by site/criticality.

### Example 8

A maintainability demonstration selects ten easy tasks performed repeatedly by the design technician. Results cannot support fleet claims. Stratify tasks by frequency/criticality/difficulty, randomly sample, use production hardware/procedures/tools and representative maintainers, predefine retries/failures/censoring, rotate personnel and report uncertainty.

### Example 9

A repair requires a cryptographic signing credential held by one remote team. Hardware and spares are local, but authorization creates a 12-hour tail and a common dependency across sites. Design secure delegated recovery, auditable break-glass policy and offline validation; test revocation/network outage. Security control remains, while support bottleneck is reduced.

### Example 10

Field data show repeat failures after maintenance caused by omitted torque verification. Add captured torque tooling, independent check for critical joints, procedure feedback and training; revise FMEA/hazard analysis and affected configurations. Track post-maintenance recurrence. Closing the procedure action is not proof until implementation and field evidence support it.

## Cross-Program Connections

- **Data engineering:** phase timestamps, work orders, censoring, repeated events, configuration and diagnostic labels determine credible maintainability evidence.
- **API and service engineering:** observability, rollback, state migration, feature flags, runbooks and incident recovery are software maintainability mechanisms.
- **Platform engineering:** self-service diagnostics, deployment/recovery tooling, credentials, on-call skill and shared support services shape restoration time.
- **Object-oriented programming:** modular interfaces and replaceable components aid repair; hidden coupling and global state defeat interchangeability.
- **Functional programming:** immutable state/event logs and pure recovery transformations improve diagnosis and rollback reasoning.
- **Human factors and safety:** access, posture, labels, workload, lockout, verification and representative maintainers constrain every physical task.

## References

1. International Electrotechnical Commission, [IEC 60300-3-10:2025, Maintainability and maintenance](https://webstore.iec.ch/en/publication/65334), edition 2.0, stability date 2028.
2. International Electrotechnical Commission, [IEC 60706-2:2006, Maintainability requirements and studies during design and development](https://webstore.iec.ch/en/publication/3013), edition 2.0, stability date 2027.
3. International Electrotechnical Commission, [IEC 60706-3:2006, Maintainability verification and data](https://webstore.iec.ch/en/publication/3014), edition 2.0, stability date 2027.
4. International Electrotechnical Commission, [IEC 60706-5:2007, Testability and diagnostic testing](https://webstore.iec.ch/en/publication/3015), edition 2.0, stability date 2028.
5. International Electrotechnical Commission, [IEC 60300-3-14:2024, Supportability and support](https://webstore.iec.ch/en/publication/68532), edition 2.0, stability date 2029.
6. Defense Logistics Agency ASSIST, [MIL-HDBK-470, Designing and Developing Maintainable Products and Systems](https://quicksearch.dla.mil/qaDocDetails.aspx?ident_number=120647), authoritative record, accessed 2026-08-31.
7. NASA, [Maintainability Engineering Requirements](https://ntrs.nasa.gov/api/citations/20230015479/downloads/Maintainability.pdf?attachment=true), engineering case, 2023.
8. NASA Engineering and Safety Center, [Evolvable Systems Engineering for Future Human Exploration](https://ntrs.nasa.gov/api/citations/20220002905/downloads/NESC-RP-20-01589_NASA-TM-20220002905final.pdf), maintainability/ISS discussion, 2022.
9. NASA, [Maintainability Allocations](https://ntrs.nasa.gov/api/citations/20160003132/downloads/20160003132.pdf), 2016.
10. NASA Office of Safety and Mission Assurance, [Reliability and Maintainability](https://sma.nasa.gov/sma-disciplines/reliability-and-maintability), current policy and training resources, accessed 2026-08-31.

## Exercises

### Exercise 1

Write a maintainability requirement and restoration chain for replacing a safety-relevant actuator in a remote facility. Define task population, resources, clocks, percentile and verification.

### Exercise 2

Given repair times 20, 25, 30, 35, 40, 60, 180 minutes, compute mean, median, nearest-rank 90th percentile and fractions within 45 and 90 minutes. Explain operational implications.

### Exercise 3

Design diagnostic/testability requirements for ten LRUs where one alarm currently isolates only to groups of three and false alarms drive removals.

### Exercise 4

Compare repair-in-place, LRU swap/depot repair and discard for a high-cost module at three remote sites. Define LORA criteria and uncertainty.

### Exercise 5

Plan a maintainability demonstration and field-feedback system that can support $M(60\text{ min})\ge0.9$ without hiding learning, censoring, NFF or induced failures.

## Answers to the Exercises

### Answer 1

Example: “For the representative actuator failure/task set in configuration F4, two authorized maintainers at the remote site using deployed tools, one stocked LRU, approved technical data and protective equipment shall detect/isolate, safe, access, replace, reassemble, verify full-load operation and return the function to service within 120 minutes with probability at least 0.9 under the specified environmental range.” State confidence/demonstration separately.

Clock starts at valid fault indication or declared demand and ends only after configuration, containment/guards, calibration, full-load function and safety checks plus return authorization. Record detection, isolation, safeing, access, part retrieval, replacement, reassembly, verification and approval; define whether logistics beyond the stocked spare is excluded from this design measure and report operational delay separately.

The task population includes representative actuator modes and access/configurations, not one rehearsed swap. Verification uses production-representative hardware, tools, data, maintainers, PPE, lighting/weather and injected faults. Safety isolation, lifting, stored energy and independent critical checks are mandatory gates; time compliance cannot compensate for unsafe restoration.

### Answer 2

The sorted times are already 20, 25, 30, 35, 40, 60, 180. Mean is $390/7=55.7143$ minutes; median is 35 minutes. The nearest-rank 90th percentile uses rank $\lceil0.9(7)\rceil=7$, so it is 180 minutes. Five of seven (0.7143) finish within 45 minutes, and six of seven (0.8571) within 90.

The median suggests typical repair is short, while the one 180-minute task drives the mean and tail. It should not be deleted without a predefined exclusion and causal justification. Investigate fault/task/resource/configuration causing it. Seven selected observations cannot establish a population 90th percentile or probability target with confidence; stratification, censoring and representative sampling are needed.

### Answer 3

Define the credible fault set by LRU/mode/configuration and requirements for detection within time, isolation to one LRU or declared ambiguity group, missed detection, false alarm per opportunity/time, false isolation/removal and unavailable-test behavior. Link end effects/criticality so high-consequence faults receive stronger coverage and independence.

Build a diagnostic dependency matrix mapping symptoms/tests to faults. Add discriminating test points, diverse signals, controlled stimulation or external tests where they reduce three-LRU ambiguity. Account for sensor/test failures, modes, latency and common power/software. Avoid adding sensors whose false alarms/correlation create more removals.

Verify by representative fault injection across operating/degraded/startup/maintenance modes and environments, including no-fault cases, intermittent faults and multiple plausible symptoms. Report denominators and confidence; trace each removal to teardown finding/NFF. Monitor field false alarm, repeat repair and isolation accuracy by configuration, then update thresholds, design and procedures without relabeling NFF as operator error.

### Answer 4

Criteria include restoration time/tail, mission consequence, local/depot skill and staffing, tools/test/facilities, transport, spares quantity/cost/location, replenishment, repair yield/turnaround, condemnation, failure-analysis learning, configuration/data rights, cybersecurity, safety, environmental waste, obsolescence and lifecycle demand/cost.

Repair in place avoids spare transport but may exceed access/skill time. LRU swap meets line recovery but needs expensive stocks and a depot pipeline. Discard minimizes repair infrastructure but increases procurement, waste and supply disruption. A mixed policy can stock one LRU per critical site, depot-repair high-value returns and discard irreparable subassemblies.

Model uncertainty in failure demand, geographic correlation, transport/supplier lead time, repair yield, no-fault-found rate, technology refresh and common events. Use sensitivity/scenarios rather than one net-present-cost point. Safety and mission recovery are constraints, not merely costs. Pilot representative tasks and validate inventory/turnaround before full adoption.

### Answer 5

Freeze task/fault population, configuration, maintainer/resource/environment, clock boundaries, success/verification and confidence method. Stratify representative tasks by frequency, criticality, item/access and diagnostic difficulty; sample by a predefined design. Use production units, procedures, tools, spares and intended trained maintainers. Rotate people/tasks and distinguish first exposure from rehearsal.

Predefine injected faults, false-alarm/no-fault cases, timing phases, pause rules, retries, abandonment/right censoring, unsafe/incorrect restoration and exclusion criteria. A task passes only after end-to-end function, configuration and safety verification. Analyze $M(60)$ with an appropriate binomial/survival model and confidence interval; report mean, median, tail, phase contributions and failures. Sample size must be planned for the target/confidence, not chosen after results.

Field records preserve symptom, telemetry, configuration, diagnosis, ambiguity, removals, teardown/NFF, full timestamps, personnel/resources, parts, verification, induced issues and repeats. Compare demonstration and field strata, investigate drift and update design/diagnostics/procedures/support. Retain prior baselines. Passing a demonstration supports only the sampled conditions; it does not guarantee future restoration or operational availability.
