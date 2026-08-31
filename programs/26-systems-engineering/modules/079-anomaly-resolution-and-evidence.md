---
module_id: SYSENG-079
program: Systems Engineering
level: 2
module_number: 79
title: Anomaly Resolution and Evidence
status: complete
last_verified: 2026-08-31
---

# Anomaly Resolution and Evidence

## One-Page Review

### Governing question

When observed behavior differs from expectation, how can a team preserve trustworthy evidence, determine what is known and unknown, bound causal and impact claims, correct the controlling mechanism, and demonstrate effective closure without erasing the anomaly's history?

### Essential definitions

- An **anomaly** is an observed departure from expected, predicted, specified, historical, or otherwise noteworthy behavior that requires evaluation. It is a trigger for inquiry, not a diagnosis.
- A **discrepancy** is a difference between two results, artifacts, conditions, or expectations. A discrepancy can arise from product, test, analysis, data, procedure, environment, tool, or interpretation.
- A **nonconformance** is failure to satisfy an applicable requirement, specification, process, or acceptance condition. Not every anomaly is a product nonconformance.
- An **observation** records what was perceived or measured, where and when, by which means, under which configuration. An **interpretation** assigns meaning. Keep them distinguishable.
- A **fact** is a proposition supported to the investigation's declared evidence standard. A hypothesis is a candidate explanation still subject to testing.
- A **causal factor** is an event, condition, action, or absence that contributed to the outcome. Labels such as root, proximate, intermediate, latent, or contributing cause depend on the chosen method and governance.
- **Containment** limits immediate exposure or propagation while preserving evidence. It is not necessarily a permanent correction.
- **Corrective action** changes a cause or controlling condition to prevent recurrence or reduce consequence. **Preventive action** addresses credible similar occurrences beyond the observed instance.
- **Reproduction** recreates the observed behavior under controlled conditions. Failure to reproduce does not prove the anomaly was unreal.
- **Closure evidence** demonstrates that the authorized disposition, correction, verification, regression, impact coverage, and residual-risk decision satisfy predefined closure criteria.

### Central model, mechanism, or theorem

Treat an anomaly record as an evidence graph

\[
G=(O,F,H,T,C,I,A,E),
\]

where observations $O$ and preserved artifacts $F$ support or contradict hypotheses $H$ through tests/analyses $T$; bounded causal conclusions $C$ drive impact assessment $I$, actions $A$, and closure evidence $E$. A sound closure argument requires traceable edges, not merely a plausible story:

\[
O,F \Rightarrow C_{bounded} \Rightarrow I,A \Rightarrow E_{correction+regression+scope}.
\]

The arrows express an assurance argument, not deductive certainty. Alternative explanations, common causes, missing data, changed configurations, and evidence limitations remain explicit.

### Critical invariants

- Preserve the original observation, raw data, configuration, chronology, and failed result; never overwrite failure with the rerun pass.
- Separate symptom, observation, expectation, requirement, classification, hypothesis, cause, impact, action, and disposition.
- Establish who detected, owns, investigates, approves actions, accepts residual risk, and authorizes closure; escalation follows consequence and uncertainty.
- Stabilize unsafe or evidence-destroying conditions before investigation while recording every intervention.
- Bind all evidence to product/build/article, tools, data, environment, procedure, operators, interfaces, clocks, and external dependencies.
- Maintain an immutable chronology using calibrated time or quantified clock relationships; distinguish event time, observation time, log time, and report time.
- Search for prior, duplicate, related, cross-product, supplier, and precursor occurrences without forcing superficial similarity.
- Test competing hypotheses using predictions that could distinguish them; confirmation alone is insufficient.
- A reproduced symptom is not automatically a cause, and a changed component followed by success is not automatically proof of causality.
- Assess systemic extent and consequence: other units, versions, modes, interfaces, users, sites, data populations, hazards, and lifecycle stages.
- Correct product and enabling-process causes as applicable, then verify the correction and run risk-based regression on the exact controlled configuration.
- Closure records unresolved uncertainty, residual risk, lessons, recurrence monitoring, and reopen triggers; administrative completion is not evidence completion.

### Common failures

Common failures include restarting before capturing volatile state; editing logs; accepting screenshots without provenance; calling every discrepancy a product bug; blaming the last actor; using “root cause” as a single-person label; stopping at “operator error”; changing several variables during reproduction; testing only the suspected cause; treating nonreproduction as exoneration; closing because a patch compiled; rerunning only the failed case; discarding failed runs; downgrading severity to meet schedule; applying a local workaround without fleet/supplier impact; confusing containment with correction; and counting closed tickets while recurrence and residual risk remain unknown.

### Compact example

A synthetic data path expects records 100–105. Producer evidence shows all six emitted; a network capture shows all six delivered; the consumer commits five and records a schema rejection for 103. The first observed divergence is therefore at consumer validation for this trace. After a narrowly modeled decoder correction, all six commit and a declared regression passes. This does not prove a real root cause, exclude concurrent faults, establish prevalence, or validate production behavior.

### Connections

Verification, validation, requirements, interfaces, configuration management, observability, causal inference, reliability, safety, security incident response, human factors, supplier quality, change control, regression testing, risk management, lessons learned, and technical decision records all converge in anomaly resolution.

## Governing Question

Can an independent reviewer reconstruct what happened, distinguish evidence from inference, understand why the chosen actions address the bounded causal mechanism and its extent, and verify that closure does not claim more than the evidence supports?

Anomalies are valuable because they contradict a model: the system model, test oracle, configuration record, operating assumption, or team's mental model. The first responsibility is not to explain the surprise quickly; it is to preserve enough state that competing explanations remain testable. A confident story produced after logs rotate, hardware is reset, data are transformed, and the environment changes is weak evidence even when the story is plausible.

## Why This Matters

NASA's active problem/nonconformance/anomaly handbook addresses closed-loop problem reporting. NASA Product Verification guidance says discrepancies should be analyzed for data quality, integrity, correctness, consistency, and validity while the configuration is intact where possible; teams distinguish product nonconformance from poor verification conduct, procedure, facility, or conditions, then record correction and reverification. Technical assessment and configuration management connect results to thresholds, trends, decisions, and controlled baselines.

Higher-consequence events require formal reporting and investigation under applicable policy. NASA mishap material emphasizes facts, timelines, causal-factor analysis, barriers, evidence integration, and corrective recommendations. Those methods can inform proportionate engineering investigations, but an ordinary failed test must not be mislabeled a reportable mishap, nor may local problem tracking replace mandatory safety, security, privacy, regulatory, or legal processes.

Poor anomaly handling corrupts future assurance. Deleting a failed run makes reliability look better; changing severity hides risk; closing on a workaround institutionalizes debt; losing configuration prevents recurrence analysis; and a narrow correction leaves related products exposed. Conversely, an investigation that demands absolute certainty can paralyze action. The goal is a disciplined, bounded decision: what evidence supports, what it contradicts, what remains unknown, what exposure must be contained, and what actions are proportionate.

## Prerequisites and Retrieval

Before investigation or closure, retrieve:

1. anomaly identifier, detection source, reporter, owner, date/time/location, original wording, expected versus observed result, requirement/expectation/oracle, immediate consequence, potential consequence, and reporting obligations;
2. exact system/product/test configuration: hardware serial/lot, software commit/build, firmware, models, data, parameters, feature flags, dependencies, infrastructure, site, network, identity, external services, tools, procedures, operators, and prior changes;
3. raw and derived evidence with provenance: logs, traces, packets, measurements, images, dumps, core files, database state, physical samples, witness accounts, commands, notebooks, calculations, calibration, access history, hashes, retention, and chain of custody where required;
4. chronology with time sources, synchronization error, time zones, monotonic intervals, event/ingest/processing/report times, and known gaps;
5. containment and evidence-preservation actions, including shutdown, isolation, quarantine, traffic stop, access restriction, data snapshot, backup, replacement, and every state-changing intervention;
6. classification, severity/priority, hazard/threat/privacy/mission/financial effects, fleet/population exposure, escalation, notification, independence, and stop-work/return-to-service authority;
7. prior and related problems, recurring signatures, supplier notices, fleet/version/site trends, hazards, risks, waivers, workarounds, changes, maintenance, incidents, and lessons;
8. investigation plan with team expertise, hypotheses, predicted discriminating observations, experiments/analyses, controls, reproduction conditions, instrument adequacy, safety constraints, and decision criteria;
9. causal analysis artifacts: timeline, event/condition model, change/barrier analysis, fault tree or other justified method, supporting/contradicting evidence, alternative hypotheses, uncertainty, and review/dissent;
10. impact/extent analysis across requirements, architecture, hazards, interfaces, variants, suppliers, production, operations, users, data, security, support, and retirement;
11. action plan distinguishing immediate response, containment, correction, corrective/preventive action, owner, authority, due date, resources, verification method, effectiveness measure, regression scope, deployment, and rollback;
12. closure package: original evidence, current classification, bounded cause, impact, completed actions, correction and regression results, exact final configuration, deviations, residual risk/acceptance, recurrence monitoring, lessons, approvals, and reopen triggers.

Perform a **first-divergence trace**: select a failing end-to-end transaction or physical effect and compare expected with observed state at successive authoritative planes. The earliest observable divergence narrows localization, but may still be downstream of a hidden causal mechanism or shared dependency.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish anomaly, discrepancy, nonconformance, defect, incident, mishap, cause, effect, containment, correction, and corrective action;
2. preserve volatile and durable evidence before state-changing intervention;
3. build a configuration-bound chronology from heterogeneous observations and clocks;
4. separate facts, assumptions, hypotheses, interpretations, unknowns, and contradictions;
5. design discriminating tests for competing causal hypotheses;
6. perform proportional change, barrier, event, fault, human/organizational, and common-cause analysis;
7. bound causal conclusions and systemic extent without premature certainty;
8. define correction, corrective/preventive action, verification, regression, and effectiveness monitoring;
9. govern waiver, residual risk, closure, lessons, and recurrence/reopen criteria;
10. create an auditable evidence package without making false external-review or safety claims.

## Core Exposition

**Report before explaining.** Capture expected and observed behavior in neutral language. “Service returned success but no record became durable” is better than “database lost the record.” Record discovery context and immediate impact without requiring the reporter to diagnose.

**Triage consequence and obligations.** Determine immediate safety, security, privacy, environmental, mission, financial, regulatory, and evidence risks. Activate mandatory processes and independent authorities where thresholds apply. Local engineering investigation may proceed in coordination, never as a substitute.

**Contain deliberately.** Protect people, environment, assets, data, and operations. If safe, preserve volatile memory, process/thread state, queues, clocks, power, network sessions, physical positions, and samples before reset. If safety requires immediate intervention, act and document what evidence was necessarily altered.

**Freeze the evidence context.** Snapshot builds, images, packages, configurations, schemas, feature flags, infrastructure, external versions, data, procedures, instruments, and operator roles. Hashing supports integrity; access controls and chain-of-custody discipline scale with consequence. A log without clock, source, retention history, and configuration can mislead.

**Separate epistemic states.** Maintain columns or fields for observed facts, interpreted facts, hypotheses, unknowns, required data, and contradictions. Promote a claim only when its evidence standard is met. Preserve minority/dissenting interpretations rather than forcing early consensus.

**Construct the chronology.** Normalize timestamps only after retaining originals. Quantify skew and precision. Correlate by unique IDs, sequence, physical state, causal acknowledgments, or monotonic intervals. Absence in a log can mean no event, lost telemetry, filtering, rotation, clock error, failed instrumentation, or wrong query.

**Check the test before blaming the product.** Review requirement/oracle, procedure, test article, setup, environment, instruments, calibration, data, analysis code, operator actions, and acceptance logic. A setup problem can coexist with a product defect; do not erase product behavior merely because one test condition was invalid.

**Generate multiple hypotheses.** Include product design/implementation, integration/interface, data, environment, tool/instrument, procedure, configuration, human/organizational, supplier, requirement/oracle, and coincidental explanations. Ask what each predicts that rivals do not.

**Use discriminating evidence.** Change one factor when practical; use controls, counterfactual traces, boundary cases, fault injection, independent measurement, code/history inspection, physical analysis, and repetition. Avoid experiments that alter several variables and yield only another ambiguous pass.

**Treat reproduction carefully.** A reproduction strengthens a mapping between conditions and symptom. It may not identify cause. Nonreproduction can reflect rarity, missing state, timing, observer effects, repaired transients, environment differences, or false initial observation. Record attempt coverage and statistical limits.

**Analyze causal structure.** Build event/condition timelines, change analysis, barrier/control analysis, fault trees, causal-factor charts, five-whys or other methods appropriate to complexity. Do not force one “root.” Causes can include technical, human, procedural, organizational, supplier, and governance conditions. “Operator error” is an outcome requiring analysis of task, interface, training, workload, authority, incentives, and defenses.

**Bound conclusions.** Say “the trace supports schema rejection as the first observed divergence for build X under scenario Y” rather than “the decoder is the root cause of all loss.” State supporting and contradicting evidence, alternatives, missing data, confidence basis, and what observation would reopen the conclusion.

**Assess extent before local closure.** Search other serials/lots, branches, versions, sites, suppliers, interfaces, modes, data populations, user groups, hazards, operations, maintenance, and stored/replayed artifacts. A one-line defect can have fleet-wide exposure; a site-specific misconfiguration can share a provisioning cause.

**Design action against mechanism.** Immediate response stops consequence; containment limits exposure; correction repairs the instance; corrective action prevents recurrence; preventive action addresses analogous risk. Assign owners and measurable completion/effectiveness criteria. Training and reminders are weak when design, access, workload, or process controls remain unchanged.

**Verify correction and regression.** First show the correction changes the predicted mechanism on the exact controlled configuration. Then rerun the failing scenario, boundary/negative cases, affected requirements/interfaces/hazards, and regression selected by dependency/impact analysis. Preserve both original fail and subsequent pass.

**Validate operational resolution.** For anomalies involving intended use, demonstrate that real outcomes, people, procedures, external systems, and environment are restored—not merely that a unit test passes. Confirm deployment, migration, rollback, documentation, training, support, and monitoring.

**Close against criteria.** Closure requires authorized classification/disposition, bounded causal/impact analysis, completed actions, passed correction/regression evidence, updated baselines/hazards/risks/docs, residual-risk decision, lessons/trend coding, and recurrence monitoring. “Cannot reproduce” is a disposition requiring risk rationale, not an automatic closure reason.

**Learn across the system.** Trend anomaly types, repeated components, detection phases, escape paths, times to detection/containment/correction, action effectiveness, and recurrence. Avoid gaming counts: more reports can reflect better reporting culture rather than worse quality. Use leading and consequence-aware measures.

The following fixture demonstrates a narrow first-divergence analysis.

<!-- bijux-verify: {"id":"anomaly-evidence-trace-fixture","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"records_expected=6\nproducer_emitted=6\nnetwork_delivered=6\nconsumer_committed=5\nfirst_missing_id=103\nfirst_divergence=consumer_validation\ncause_status=bounded_to_synthetic_trace\nafter_correction_committed=6\nregression_status=pass\nstatus=declared_anomaly_fixture_consistent\nevidence=synthetic_trace_only\n","stderr":""}} -->
```python
expected = list(range(100, 106))
producer = list(range(100, 106))
network = list(range(100, 106))
consumer = [100, 101, 102, 104, 105]
consumer_rejections = {103: "schema_validation"}

missing = [record_id for record_id in expected if record_id not in consumer]

print(f"records_expected={len(expected)}")
print(f"producer_emitted={len(producer)}")
print(f"network_delivered={len(network)}")
print(f"consumer_committed={len(consumer)}")
print(f"first_missing_id={missing[0]}")

if missing[0] in producer and missing[0] in network and missing[0] in consumer_rejections:
    print("first_divergence=consumer_validation")
print("cause_status=bounded_to_synthetic_trace")

after_correction = list(range(100, 106))
print(f"after_correction_committed={len(after_correction)}")
print("regression_status=pass")
print("status=declared_anomaly_fixture_consistent")
print("evidence=synthetic_trace_only")
```

The fixture assumes complete, correct, synchronized observations and a modeled correction. It cannot establish real log completeness, causality, recurrence probability, safety, systemic extent, concurrent faults, or production effectiveness.

## Definitions and Notation

Let observation $o=(v,t,p,m,c)$ contain value/event $v$, time $t$, observation plane $p$, measurement means $m$, and configuration $c$. Evidence artifact $f$ adds provenance, integrity, access, retention, and transformation history. Hypothesis $h_j$ predicts observations $P(h_j)$ under interventions or conditions.

Evidence discriminates when an observed result has meaningfully different likelihood or compatibility across competing hypotheses. A pass after change $a$ supports causality only when alternatives—state reset, changed load, environment, data, timing, instrumentation, and random variation—are controlled or bounded.

Closure record $R=(C_b,I,A,V,R_g,U)$ contains bounded causal conclusion $C_b$, extent/impact $I$, actions $A$, correction verification $V$, regression/effectiveness evidence $R_g$, and uncertainty/residual risk $U$. It preserves the original failed evidence.

## Mechanisms, Invariants, or Proof Structure

A defensible anomaly-resolution argument follows this chain:

1. report neutral expected/observed behavior and triage consequence, obligations, ownership, and escalation;
2. contain exposure while preserving volatile/durable evidence and recording interventions;
3. freeze configuration, provenance, chronology, requirement/oracle, and evidence gaps;
4. separate facts, interpretations, hypotheses, unknowns, and contradictions;
5. test product, procedure, setup, environment, tools, data, human/organizational, supplier, and oracle hypotheses using discriminating evidence;
6. derive bounded causal conclusions with alternatives and uncertainty;
7. assess extent across product families, interfaces, hazards, operations, users, suppliers, and lifecycle;
8. implement mechanism-linked correction/corrective/preventive action under change control;
9. verify correction, execute risk-based regression and operational resolution, and monitor effectiveness;
10. close only with authority, residual risk, lessons, trend coding, recurrence measures, and reopen triggers.

The invariants are original-evidence preservation, configuration identity, epistemic separation, chronological integrity, competing hypotheses, bounded causality, systemic extent, action-to-cause trace, fail-plus-pass history, authorized closure, and recurrence visibility.

## Alternatives and Trade-Offs

**Immediate reset versus evidence preservation.** Reset may restore service or safety; preservation enables diagnosis. Preplan safe snapshots and record unavoidable interventions.

**Broad containment versus operational continuity.** Quarantine reduces exposure but can create mission loss. Use consequence, uncertainty, alternatives, monitoring, and authority to choose scope.

**Reproduction versus passive evidence.** Reproduction controls conditions but may be unsafe or alter rare state. Logs, physical evidence, models, and fleet observations can complement it.

**Single expert versus cross-functional team.** One expert moves quickly; diverse teams expose interface, human, supplier, safety, and organizational mechanisms. Scale independence and expertise with consequence.

**Fault tree versus event/causal narrative.** Fault trees analyze combinations leading to a top event; timelines and causal-factor charts explain sequence and conditions. Use complementary methods rather than forcing one notation.

**Patch versus design/process correction.** A patch may restore function; design, test, configuration, supplier, training, or governance changes may be needed to prevent similar escape.

**Full regression versus impact-based regression.** Full suites reduce omission but cost time and may still lack relevant cases. Impact analysis selects affected surfaces while stable automated suites provide broad protection.

**Anonymous reporting versus attributable evidence.** Anonymous channels improve hazard discovery; attribution can support follow-up. Protect reporters and separate safety learning from blame while preserving necessary technical evidence.

## Failure Modes and Misconceptions

**“The anomaly is the cause.”** It is the observed departure that starts inquiry.

**“The last change caused it.”** Temporal proximity suggests a hypothesis, not proof.

**“We could not reproduce it.”** State, timing, rarity, missing instrumentation, or changed context can prevent reproduction.

**“Replacing the component fixed it.”** Replacement also resets state and changes configuration; causality remains to be tested.

**“The log has no error.”** Logging can fail, filter, rotate, lag, or observe the wrong plane.

**“Operator error closes the analysis.”** Human action occurs within tasks, interfaces, procedures, training, organization, workload, and barriers.

**“One root cause is required.”** Complex outcomes can have multiple necessary/contributing conditions and common causes.

**“The rerun passed, so delete the failure.”** Both are essential to evidence and recurrence analysis.

**“A waiver resolves the anomaly.”** It authorizes bounded departure/residual risk; it does not prove conformity or correction.

**“Ticket closed means risk closed.”** Administrative status can precede deployment, effectiveness, regression, or recurrence evidence.

## Worked Examples

### Example 1

A test controller restarts a service immediately after a hang, restoring schedule but erasing memory and thread state. The team preserves remaining logs and exact build, records the reset as an intervention, recreates load/timing with added dump triggers, and narrows its conclusion. It cannot claim the original hang's cause from the later reproduction alone.

### Example 2

A sensor value spikes while two instruments disagree. Calibration history shows one reference expired, but independent physical evidence also suggests a transient. The invalid reference weakens one measurement; it does not prove the product healthy. Repeated tests with calibrated independent instruments and environmental capture distinguish hypotheses.

### Example 3

A message appears “sent” in the producer, “delivered” at a proxy, and absent in the database. Plane semantics reveal sent means queued and delivered means forwarded. Correlation IDs show consumer rejection. The symptom location was downstream, but joint traces—not ownership assumptions—localize the first observed divergence.

### Example 4

An operator selects the wrong mode. Investigation finds visually similar controls, ambiguous state feedback, time pressure, stale procedure, and a disabled interlock. Retraining alone does not address design and barrier conditions. Actions modify mode distinction, feedback, procedure, interlock monitoring, and representative scenario verification.

### Example 5

A rare crash cannot be reproduced in 1,000 short trials. Original telemetry shows it followed 36 hours of queue growth and certificate rotation; short tests never enter that state. Duration/state coverage, not trial count alone, controls evidentiary relevance.

### Example 6

A supplier replaces a failed capacitor and the unit passes. Lot records show related date codes across several assemblies. Extent analysis quarantines the lot, tests samples, reviews environmental stress and supplier process, and updates fleet risk. Closing only the returned unit would miss common exposure.

### Example 7

A model predicts a load outside limits, while a physical test does not. Investigation checks model equations, inputs, mesh/convergence, boundary conditions, sensor placement/calibration, fixture stiffness, article dimensions, and synchronization. “Test versus model” is a discrepancy between evidence systems, not automatic validation of either.

### Example 8

A security alert is initially classified as a scanner false positive. Manual reproduction finds exploitability only with an old feature flag active at one site. Configuration status expands the affected population. Security incident obligations and evidence handling govern alongside the engineering anomaly process.

### Example 9

A patch eliminates the failing case but slows recovery under peak load. Impact-based regression includes performance, failover, retry, data integrity, interface versions, and operational recovery. Correction verification without regression would exchange one anomaly for another.

### Example 10

Three low-severity anomalies share a timing signature and bypass the same barrier. Trend analysis treats them as a precursor rather than independent noise, updates the hazard argument, and prioritizes preventive action. Frequency/severity coding alone would hide the common mechanism.

## Cross-Program Connections

- **Platform engineering:** incident timelines, configuration, telemetry, change correlation, containment, rollback, post-incident actions, and fleet-wide remediation use the same evidence discipline.
- **API/service engineering:** request IDs, delivery semantics, retries, timeouts, state, versions, and observation planes determine first divergence and corrective scope.
- **Data engineering:** lineage, event time, transformations, rejects, reconciliation, late data, schema evolution, and data-quality oracles are anomaly evidence.
- **Object-oriented/functional programming:** invariants, contracts, types, effects, property tests, minimized counterexamples, and deterministic replay aid reproduction without proving operational extent.
- **Security:** forensic integrity, chain of custody, containment, disclosure, threat hypotheses, eradication, recovery, and monitoring impose specialized obligations.
- **Safety/reliability:** precursors, hazards, common causes, barriers, FRACAS/PRACA, recurrence, and residual-risk authority turn anomalies into system learning.
- **Human factors:** task, interface, workload, team, procedure, training, culture, authority, and organizational conditions prevent simplistic blame.
- **Statistics/causal inference:** sampling, rare events, censoring, confounding, counterfactuals, likelihood, uncertainty, and change-point/trend analysis bound conclusions.

## References

1. NASA, [NASA-HDBK-8739.18, Procedural Handbook for Program and Project Management of Problems, Nonconformances, and Anomalies](https://standards.nasa.gov/standard/NASA/NASA-HDBK-873918), active record accessed 2026-08-31.
2. NASA, [Product Verification, Systems Engineering Handbook section 5.3](https://www.nasa.gov/reference/5-3-product-verification/), accessed 2026-08-31.
3. NASA, [Product Validation, Systems Engineering Handbook section 5.4](https://www.nasa.gov/reference/5-4-product-validation/), accessed 2026-08-31.
4. NASA, [Technical Assessment, Systems Engineering Handbook section 6.7](https://www.nasa.gov/reference/6-7-technical-assessment/), accessed 2026-08-31.
5. NASA, [Configuration Management, Systems Engineering Handbook section 6.5](https://www.nasa.gov/reference/6-5-configuration-management/), accessed 2026-08-31.
6. NASA, [NPR 7123.1B, NASA Systems Engineering Processes and Requirements, Change 4](https://nodis3.gsfc.nasa.gov/displayAll.cfm?Internal_ID=N_PR_7123_001B_&page_name=ALL), effective 2020.
7. NASA, [NPR 8621.1D, Mishap and Close Call Reporting, Investigating, and Recordkeeping, Change 4](https://nodis3.gsfc.nasa.gov/displayDir.cfm?Internal_ID=N_PR_8621_001D_&page_name=Chapter1), current through 2028.
8. NASA Safety Center, [Mishap Prevention and Organizational Performance](https://www.nasa.gov/nasa-safety-center-mishap-prevention/), updated 2026.
9. NASA, [Spaceflight Mishap Investigation Flight Surgeon Handbook](https://www.nasa.gov/wp-content/uploads/2023/03/spaceflight-mishap-handbook-tagged.pdf), 2021.
10. NASA, [SWE-068 — Evaluate Test Results, Software Engineering and Software Assurance Handbook](https://swehb.nasa.gov/spaces/SWEHBVD/pages/102695451/SWE-068%2B-%2BEvaluate%2BTest%2BResults), accessed 2026-08-31.

## Exercises

### Exercise 1

A distributed order disappears after an API success. Define the initial report, evidence-preservation plan, planes/chronology, competing hypotheses, discriminating tests, and bounded closure criteria.

### Exercise 2

A failure occurs 3 times in 200 trials before a correction and 0 times in 200 afterward. Compute observed rates and explain what can and cannot be concluded about elimination and effectiveness.

### Exercise 3

An operator bypassed an interlock during maintenance. Construct a causal/barrier analysis that avoids stopping at “procedure violation,” and propose actions/evidence.

### Exercise 4

A firmware patch fixes a sensor dropout on one serial number. Design extent analysis and risk-based regression before fleet closure.

### Exercise 5

Create a closure record for a nonreproducible anomaly whose original evidence is credible but incomplete and whose potential consequence is high.

## Answers to the Exercises

### Answer 1

Report neutrally: exact order/tenant/request, expected durable order and acknowledgment semantics, observed API success with absent authoritative record, times/planes, build/configuration, consequence and reporter. Preserve client request/response, correlation/idempotency IDs, gateway/proxy traces, service queues/logs/dumps, database WAL/transactions/replicas, event bus, downstream indexes, identity/routing/configuration, clocks, deployments and raw queries before retry/reset/retention destroys state. Record any containment such as duplicate suppression or traffic isolation.

Trace client creation, gateway acceptance, service validation, transaction begin/commit, outbox/event, replication, read path and downstream effect using original timestamps plus quantified skew. Hypotheses include misleading success semantics, lost async queue item, transaction rollback, wrong shard/tenant, stale replica/read cache, duplicate suppression collision, authorization/filtering, schema rejection, downstream projection delay, telemetry gap, or client identifier error. Each predicts distinct evidence. Reproduce with unique IDs and fault injection at commit/ack/network/restart boundaries; inspect code/config changes and use an independent authoritative query.

Closure requires bounded first divergence and mechanism, impact across tenants/versions/replayed orders, containment, corrected success/commit/idempotency behavior, verification at the causal boundary, regression for duplicates/retries/timeouts/restart/partition/routing/read consistency, operational end-to-end outcome, migration/reconciliation of affected orders, monitoring, exact deployed configuration, residual risk and authority. Preserve the original loss and do not claim universal exactly-once behavior from one corrected trace.

### Answer 2

Observed pre-correction rate is $3/200=0.015=1.5\%$; observed post-correction rate is $0/200=0\%$. The post-correction sample shows no observed failures under those 200 trial conditions and is consistent with improvement. It does not prove the true rate is zero or that the correction caused the difference.

Trials may not represent the rare triggering state, be independent, or match pre-correction load/data/timing/configuration. Other variables, resets, learning, instrumentation, and chance can explain differences. Even with independent identical Bernoulli trials, zero observations gives an upper uncertainty bound rather than elimination (the rough “rule of three” 95% upper bound is about $3/200=1.5\%$, subject to that model). Examine mechanism evidence, matched conditions, duration/state coverage, larger samples where justified, regression, fleet/operational monitoring, and consequence. State “0/200 observed after correction,” not “failure eliminated.”

### Answer 3

Build the event timeline: maintenance goal, system state, work authorization, isolation, interlock status, cues, procedure step, bypass access, supervisor/team communications, action, system response and recovery. Ask why bypass was possible and locally rational: procedure accuracy, time pressure, lockout design, diagnostic need, parts/tools, access control, interface feedback, training, staffing, fatigue, production incentives, prior normalized deviations, escalation, supervision and barrier monitoring.

Analyze barriers: prevention (physical/keyed interlock, authorization, safe diagnostic mode), detection (alarm/audit/independent check), mitigation (energy isolation/fail-safe), and recovery. Identify which were absent, failed or deliberately overridden and why. Actions can include safe maintenance mode, stronger interlock/permit and state indication, updated verified procedure, tool/parts availability, escalation authority, workload/schedule changes, supervisor checks and bypass telemetry—not training alone.

Verify design/access changes and audit behavior; conduct representative maintenance scenarios including fault, time pressure, handoff, unavailable part and emergency; reassess hazards and similar equipment/sites; confirm deployment, competency and monitoring. Preserve human/organizational causal conditions and authorized residual risk.

### Answer 4

Identify affected component design, firmware versions/build options, sensor/vendor lots, serial/date codes, hardware revisions, calibration, interface partners, environmental/load modes, sites, maintenance history, and supplier process. Search anomaly signatures, telemetry, returned units, production tests, deviations and similar code across product families. Determine whether the observed serial is unique, sentinel, or merely the first detected.

Verify patch mechanism with the original serial/configuration and fault-triggering conditions, instrumented at sensor/firmware/interface planes. Regression covers nominal accuracy/timing, boundaries, startup/shutdown, long duration, power/thermal/vibration/EMI as relevant, intermittent transport, calibration, diagnostics, alarms, retry/recovery, resource use, update/rollback, configuration compatibility, safety and security. Test representative hardware/lot/variant samples rather than one unit; update qualification/acceptance if design/process changed.

Plan staged fleet deployment with eligibility rules, backup, rollback, monitoring and recurrence trigger. Reconcile stored data and downstream effects. Closure states tested population and untested variants, supplier corrective action, hazard/risk impact, exact released configuration, regression and operational evidence, residual uncertainty and authority.

### Answer 5

Retain the original neutral report, raw artifacts/provenance, exact configuration, chronology, witness accounts, expectation/oracle, credible-evidence rationale, interventions and gaps. Record every reproduction attempt with conditions, duration/state coverage, instrumentation and differences; do not summarize them as “could not reproduce.” List hypotheses, supporting/contradicting evidence, missing discriminators and why collection is impossible or deferred.

Because consequence is high, classify/escalate under applicable safety/security/regulatory processes, assess worst credible extent, search fleet/prior/supplier data, improve instrumentation, and impose proportionate containment or operational restrictions. Use independent review and authority for return-to-service. Actions may include monitoring/triggers, safe-state behavior, inspections, component quarantine, redundancy checks, procedure changes, or targeted redesign even without a unique cause.

Closure, if authorized, is “unresolved cause with controlled residual risk,” not “no defect.” It identifies exposure model, completed actions, verification/regression, surveillance period and effectiveness measures, open owners/dates, waiver/risk acceptance, evidence retention, review dissent, and automatic reopen triggers such as recurrence, related signature, new supplier data or configuration change. High uncertainty plus high consequence can justify continued open status or nonuse; schedule is not evidence.
