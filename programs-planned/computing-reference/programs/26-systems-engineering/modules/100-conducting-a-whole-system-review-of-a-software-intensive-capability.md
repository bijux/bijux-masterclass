---
module_id: SYSENG-100
program: Systems Engineering
level: 2
module_number: 100
title: Conducting a Whole-System Review of a Software-Intensive Capability
status: complete
last_verified: 2026-09-01
---

# Conducting a Whole-System Review of a Software-Intensive Capability

## One-Page Review

### Governing question

How can a review body decide whether a software-intensive capability is ready for a bounded purpose and operating envelope by integrating stakeholder value, requirements, architecture, interfaces, assurance, human and organizational control, operations, recovery, and evolution without replacing judgment with document counts or average scores?

### Essential definitions

- A **whole-system review** is an evidence-based examination of a capability as a configured socio-technical system in its environment, across mission threads, lifecycle modes, authorities, and stakeholder outcomes.
- A **capability** is the evidenced ability of a configured system, people, organization, suppliers, infrastructure, data, and processes to achieve an outcome under stated conditions.
- A **mission thread** is an end-to-end sequence of interactions and state changes through which actors and system elements pursue an outcome.
- A **review basis** is the approved set of purpose, scope, configuration, environments, criteria, authorities, assumptions, evidence, and decision rules used by the review.
- A **closure criterion** states the evidence and authority required to close a requirement, risk, anomaly, action, or decision condition.
- A **finding** is a review conclusion tied to evidence; an **action item** assigns work but is not itself closure.
- A **dissenting opinion** records a material unresolved disagreement, its evidence, consequence, and disposition without forcing artificial consensus.
- **residual risk** is risk remaining after controls, with uncertainty, affected stakeholders, owner, acceptance authority, conditions, monitoring, and renewal triggers.
- A **conditional approval** authorizes only a defined scope while enforceable conditions, limits, monitoring, and stop criteria remain satisfied.
- A **decision package** is the controlled record of recommendation, rationale, evidence, findings, dissent, conditions, authority, residual risk, and follow-up.

### Central model, mechanism, or theorem

For mission thread $q$, configuration $k$, and time $t$, define a review vector

$$
W(q,k,t)=\langle V,B,R,A,I,H,E,O\rangle,
$$

where $V$ is stakeholder value and mission outcome, $B$ system boundary and configuration, $R$ requirements and protected constraints, $A$ architecture and allocation, $I$ interfaces and integration, $H$ human, organizational, policy, and ethical control, $E$ assurance evidence, and $O$ operations, recovery, and evolution. A readiness recommendation is eligible only when every applicable noncompensable gate passes or has an explicitly authorized disposition:

$$
eligible(q,k,t)\Rightarrow V\land B\land R\land A\land I\land H\land E\land O.
$$

This implication does not prove readiness. Evidence truth, unknown hazards, interactions, judgment, future change, and decision legitimacy remain outside the Boolean screen.

### Critical invariants

- Review a named capability, purpose, configuration, population, environment, authority, and period—not a generic product label.
- Trace stakeholder outcomes through mission threads, requirements, architecture, interfaces, verification, validation, operations, and evidence.
- Include software, hardware, data, models, people, organizations, suppliers, policy, infrastructure, and environment when causal.
- Preserve noncompensable safety, security, privacy, legal, ethical, accessibility, and mission constraints outside aggregate scores.
- Evaluate nominal, peak, degraded, emergency, maintenance, recovery, transition, adversarial, and retirement conditions.
- Distinguish verified implementation from validated stakeholder outcome and from accepted residual risk.
- Require configuration identity, provenance, applicability, independence, anomalies, uncertainty, and limitations for every material evidence claim.
- Test interfaces as behavior, timing, semantics, authority, resource, failure, recovery, and change—not only syntax.
- Confirm that human and organizational roles have information, competence, time, authority, resources, feedback, and escalation.
- Close findings by verified outcome and authorized disposition; do not equate action assignment, document delivery, or meeting agreement with closure.
- Record dissent, assumptions, exceptions, unknowns, conditions, stop criteria, and renewal triggers in the decision package.
- Re-review after material technical, operational, organizational, supplier, policy, threat, population, purpose, or environmental change.

### Common failures

Common failures include reviewing slides instead of the configured system; allowing each discipline to present isolated green status; starting with document completeness; sampling only the happy path; accepting component tests as end-to-end validation; averaging away a hard failure; treating security, safety, privacy, human factors, and ethics as appendix checklists; ignoring suppliers and operations; accepting stale evidence; converting every uncertainty into a low probability; closing anomalies by schedule; suppressing dissent; approving conditions nobody can enforce; and issuing a broad readiness statement from a narrow demonstration.

### Compact example

A synthetic review ledger covers three mission threads across eight gates. Twenty-three of twenty-four entries pass, but recovery evidence for the degraded-ordering thread is missing. The readiness gate rejects the whole claim despite a 95.8% pass rate. This demonstrates noncompensable metadata logic only; it cannot establish that any passed assertion, criterion, evidence item, or final decision is correct.

### Connections

This capstone integrates all prior Systems Engineering modules: systems thinking, stakeholders, requirements, architecture, interfaces, models, decisions, risk, safety, security, reliability, integration, verification, validation, operations, resilience, configuration, evolution, systems of systems, emergence, cognitive work, organizations, policy, ethics, and adaptation. It transfers directly to reviews of APIs, platforms, data systems, distributed capabilities, clouds, and software-intensive enterprises.

## Governing Question

What bounded recommendation can a competent review body justify from current evidence about the configured capability, and what conditions, residual risks, uncertainties, dissent, monitoring, and change triggers must accompany that recommendation?

A review is a decision-support control, not a ceremony. Its purpose is not to reward document production or produce consensus. It should expose whether stakeholder outcomes are feasible, protected constraints are enforced, evidence applies, operations can sustain and recover the capability, and legitimate authority can accept what remains.

## Why This Matters

Software-intensive capabilities fail across boundaries. A component satisfies its specification while an interface retries unsafely; a model performs well while data freshness collapses; security blocks emergency work; automation transfers impossible recovery to operators; a supplier changes behavior behind a stable API; each team meets its target while the mission thread fails. Discipline-specific reviews can miss these interactions.

A whole-system review creates a temporary, evidence-rich view of the realized system. It links design intent to configuration and operation, follows representative threads, reconciles claims across specialties, and tests whether decision rights and recovery paths work. It does not replace continuous engineering, operational monitoring, or regulator and stakeholder authority.

ISO/IEC/IEEE 15288:2023 provides a current common framework for system lifecycle processes without prescribing one lifecycle model. NASA's Systems Engineering Handbook provides lifecycle and crosscutting technical-management guidance, while NIST SP 800-160 Volume 1 Revision 1 integrates trustworthy security engineering into the system lifecycle. These are process and practice sources, not universal approval criteria. The review basis must be tailored to the capability and governing authorities.

## Prerequisites and Retrieval

Before convening the review, retrieve:

1. decision requested, decision authority, review charter, independence, conflict disclosures, schedule, consequence, prior decisions, and allowed outcomes;
2. stakeholder map, value model, mission or business outcomes, unacceptable losses, rights, affected populations, environments, and success measures;
3. system-of-interest boundary, external systems, organizational and supplier boundaries, lifecycle stage, operating modes, data and model boundary, and excluded scope;
4. exact review configuration: baselines, builds, models, data, infrastructure, interfaces, dependencies, sites, regions, policies, procedures, staffing, training, waivers, and known unknowns;
5. requirements, assumptions, constraints, allocations, traceability, priorities, verification methods, validation criteria, and unresolved conflicts;
6. architecture views, decisions, rationale, alternatives, interfaces, dependency and trust graphs, resources, failure containment, timing, and evolution mechanisms;
7. end-to-end mission threads across nominal, peak, degraded, emergency, maintenance, recovery, transition, adversarial, and retirement conditions;
8. risk, safety, security, privacy, reliability, resilience, human-factors, organizational, legal, ethical, supplier, and environmental analyses with accepted and open items;
9. evidence index: analyses, models, simulations, tests, inspections, demonstrations, audits, reviews, operational data, incidents, anomalies, complaints, appeals, and corrective actions;
10. evidence metadata: source, configuration, procedure, oracle, participants, environment, uncertainty, independence, anomalies, limitations, reproducibility, and applicability;
11. operations and sustainment: ownership, staffing, observability, support, incident command, dependencies, capacity, backup, restoration, reconciliation, fallback, exercises, and retirement;
12. change state: open releases, migrations, mixed versions, supplier notices, regulatory changes, threat changes, deferred work, sunset plans, and re-review triggers.

Create a **review claim map** before the meeting. For each decision-critical claim, identify stakeholder outcome, thread, requirement or constraint, implemented mechanism, evidence, configuration, owner, residual uncertainty, finding status, and accepting authority. Use the map to select deep dives rather than inviting presentations by organizational chart.

## Learning Objectives

After completing this module, you should be able to:

1. define a bounded whole-system review charter, basis, scope, authority, and decision;
2. construct claim maps and end-to-end mission-thread reviews;
3. integrate requirements, architecture, interface, risk, assurance, operations, and evolution evidence;
4. test noncompensable constraints without relying on average readiness scores;
5. assess configuration identity, evidence quality, independence, applicability, uncertainty, and anomalies;
6. examine human, organizational, supplier, policy, legal, and ethical control inside the causal boundary;
7. distinguish finding, action, closure, waiver, residual risk, dissent, and decision condition;
8. formulate approve, conditionally approve, restrict, defer, reject, or retire recommendations;
9. write a reconstructable decision package with monitoring, stop, and re-review triggers;
10. conduct review as sampling and judgment without claiming exhaustive proof.

## Core Exposition

**Define the decision first.** State exactly what authority must decide: enter integration, begin a pilot, serve a population, release a model, accept a supplier, expand scope, continue operation, or retire. Define possible recommendations and who can issue each. A vague “design review” invites broad reporting without a falsifiable decision.

**Write a review charter.** Specify purpose, scope, configuration cutoff, criteria, methods, membership, independence, records, confidentiality, dissent process, finding severity, closure authority, and schedule. Give reviewers access to evidence and people. Protect the ability to request deeper analysis or recommend against the preferred schedule.

**Select competence and independence.** Include systems, domain, software, hardware where relevant, data, operations, safety, security, privacy, human factors, accessibility, legal or policy, supplier, and stakeholder expertise proportional to consequence. Independence is not ignorance: reviewers need context but should disclose ownership and incentives. A large panel without clear roles can diffuse accountability.

**Freeze the review configuration.** Record immutable identities for artifacts and actual deployment state. Identify differences among reviewed, tested, staged, and planned configurations. If evidence covers a predecessor or analogous system, record the delta and applicability rationale. Stop a review from drifting between versions to answer each question favorably.

**Build a claim map.** Organize around decision-critical claims, not document titles. A claim such as “orders remain correct during dependency failure” connects requirements, architecture, retry and idempotency design, data semantics, human recovery, test results, incidents, monitoring, and residual uncertainty. Missing links become explicit review questions.

**Follow mission threads.** Walk actors, data, control, resources, state, time, authority, and feedback from trigger to outcome. Vary mode, load, environment, participants, failures, attacks, and recovery. Include a thread that crosses the most organizational and supplier boundaries, not only the most common path.

**Challenge the boundary.** Ask what essential service, identity, clock, network, supplier, policy, operator, or environment is treated as external. External does not mean causally irrelevant. Record assumptions and contracts, then examine common cause, correlated failure, and retained obligations. Review the system people actually depend on.

**Reconcile requirements and stakeholder value.** Check that critical requirements derive from stakeholder outcomes and hazards, have measurable fit criteria, allocate coherently, and remain current. Look for orphan requirements, unrepresented stakeholders, incompatible constraints, unverifiable language, and validation gaps. Passing a requirement set does not prove the right system was built.

**Examine architecture as decisions and mechanisms.** Review boundaries, allocations, state ownership, interfaces, dependency concentration, trust, failure containment, resources, timing, observability, recovery, and evolution. Compare rationale with current evidence. A diagram is useful only when tied to actual configuration and behavior.

**Review interfaces end to end.** Check meaning, units, identity, time, provenance, ordering, retries, idempotency, capacity, authority, security, privacy, error behavior, versions, degraded modes, and recovery. Include human and organizational interfaces. A schema-conformant exchange can be semantically wrong, unauthorized, stale, or operationally unusable.

**Integrate risk perspectives.** Combine component failure, unsafe interaction, adversary, misuse, human work, organizational control, supplier, policy, and environmental analysis. Do not merge all results into one probability score. Use a coverage map of losses, hazards, threats, causal scenarios, controls, evidence, residual risk, and ownership.

**Inspect evidence quality.** For every material result, ask what was tested or analyzed, against which oracle, on what configuration, with which participants and environment, under what assumptions, uncertainty, and limitations. Check anomalies and negative results. Repetition improves sampling only when the model and scenario are relevant.

**Distinguish verification and validation.** Verification asks whether realized outputs meet specified requirements; validation asks whether the capability satisfies stakeholder needs in its intended environment. One can pass while the other fails. Review operationally representative workflows, affected outcomes, and alternatives, not only conformance artifacts.

**Test recovery, not just prevention.** Walk detection, diagnosis, authority, containment, graceful degradation, safe stop where applicable, fallback, restoration, reconciliation, communication, remedy, and re-entry. Exercise shared dependencies and partial deployment. A backup file or rollback command is not recovery evidence.

**Review human and organizational feasibility.** Confirm information, workload, competence, staffing, authority, coordination, escalation, and feedback in nominal and exceptional modes. Observe work as done. Check whether policy, incentives, budgets, and supplier relationships support the claimed controls. Human confirmation cannot compensate for opaque or impossibly fast automation.

**Review policy, legality, and ethics in context.** Verify authoritative basis, applicability facts, duty holders, controls, evidence, affected people, notice, contestability, and remedy. Preserve hard prohibitions and rights. Qualified authorities interpret law; reviewers ensure system facts and controls are visible and traced.

**Examine operations as designed capability.** Review ownership, service objectives, capacity, telemetry, alerting, support, on-call, incident command, dependency status, maintenance, backup, restoration, security response, data correction, user communication, and learning. Operational readiness is not a deployment checklist attached after architecture.

**Assess evolution and adaptation.** Identify what may change, who authorizes it, how versions and evidence are linked, which transitions are tested, how mixed states work, and when re-review occurs. For learning systems, inspect objectives, data feedback, change envelope, monitoring, protected constraints, rollback, and remedy. For suppliers, require change notice and exit capability.

**Treat findings precisely.** State condition, criterion, evidence, consequence, affected configuration, severity, owner, required outcome, closure evidence, and authority. Separate observation, concern, nonconformance, and decision-blocking finding according to the charter. Avoid vague actions such as “improve monitoring.”

**Close by outcome.** A plan, ticket, patch, document, or meeting can support closure but does not prove it. Review implementation and the evidence that the criterion now holds, including regression and side effects. Preserve the original finding and closure rationale. If accepted open, record residual risk and legitimate authority rather than relabeling it closed.

**Preserve dissent.** Invite written dissent, identify disputed claims and evidence, and prevent retaliation. The chair may still make a recommendation, but the decision authority should see material disagreement. Forced consensus hides uncertainty and removes an early warning channel.

**Choose an honest recommendation.** Options include approve, conditionally approve, restrict, defer pending evidence, reject, suspend, or retire. Conditions must be enforceable, monitored, owned, time-bounded, and connected to stop authority. Avoid approval language broader than the reviewed configuration and envelope.

**Create a reconstructable decision package.** Record charter, participants and conflicts, basis, configuration, claim map, sampled threads, evidence index, findings, closures, residual risks, assumptions, exceptions, dissent, recommendation, conditions, monitoring, stop criteria, authority, and re-review triggers. Someone outside the meeting should understand what was decided and why.

The following fixture checks declared mission-thread gates. It cannot perform a whole-system review.

<!-- bijux-verify: {"id":"whole-system-review-ledger","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"mission_threads=3\nrequired_gates=8\nchecks=24\npassed_checks=23\nfailed_checks=1\nblocked=degraded_ordering:operations_recovery\nreadiness_gate=reject_incomplete_thread_evidence\nevidence=declared_metadata_only\n","stderr":""}} -->
```python
threads = {
    "nominal_ordering": [True, True, True, True, True, True, True, True],
    "degraded_ordering": [True, True, True, True, True, True, True, False],
    "account_recovery": [True, True, True, True, True, True, True, True],
}
gates = (
    "value", "boundary", "requirements", "architecture",
    "interfaces", "human_governance", "assurance", "operations_recovery",
)
blocked = [
    f"{thread}:{gates[index]}"
    for thread, results in threads.items()
    for index, passed in enumerate(results)
    if not passed
]
checks = len(threads) * len(gates)
print(f"mission_threads={len(threads)}")
print(f"required_gates={len(gates)}")
print(f"checks={checks}")
print(f"passed_checks={checks - len(blocked)}")
print(f"failed_checks={len(blocked)}")
print(f"blocked={','.join(blocked)}")
print("readiness_gate=reject_incomplete_thread_evidence")
print("evidence=declared_metadata_only")
```

## Definitions and Notation

Let mission threads be $Q$, configurations $K$, times $T$, stakeholder outcomes $V$, boundaries $B$, requirements and constraints $R$, architecture $A$, interfaces $I$, human and governance control $H$, assurance evidence $E$, and operations/recovery/evolution $O$.

For thread $q$, configuration $k$, and time $t$, $W(q,k,t)=\langle V,B,R,A,I,H,E,O\rangle$. Each field is an evidence-backed claim with criteria and owner, not a box checked by presence of a document.

Define the review evidence envelope

$$
\Omega_W=\langle purposes,configurations,threads,populations,environments,modes,period,assumptions\rangle.
$$

The review recommendation must not exceed $\Omega_W$. A change outside the envelope requires an applicability analysis, additional evidence, new conditions, or renewed review.

## Mechanisms, Invariants, or Proof Structure

1. **Charter the decision.** Define purpose, authority, outcomes, scope, configuration, criteria, independence, records, and possible recommendations.
2. **Frame stakeholder value.** Identify outcomes, losses, rights, affected populations, environment, alternatives, and noncompensable constraints.
3. **Build claims and threads.** Map decision-critical claims and select representative end-to-end mission, failure, recovery, and evolution threads.
4. **Examine realization.** Reconcile requirements, architecture, allocation, interfaces, integration, configuration, and actual behavior.
5. **Integrate risk and governance.** Cover failure, interaction, threat, human, organization, supplier, policy, ethics, and environmental mechanisms.
6. **Evaluate evidence.** Check provenance, oracle, applicability, independence, uncertainty, anomalies, limitations, validation, and configuration identity.
7. **Assess operation and change.** Test ownership, monitoring, containment, recovery, reconciliation, learning, adaptation, support, and re-review.
8. **Resolve findings.** State criteria and consequences, verify closure, record residual risk, preserve dissent, and prevent score compensation.
9. **Make the bounded decision.** Recommend approval, conditions, restriction, deferral, rejection, suspension, or retirement with legitimate authority.
10. **Sustain the case.** Monitor conditions and outcomes, trigger stop or renewed review, preserve evidence, and update the decision package.

Core invariants are: no review claim lacks a named configuration and envelope; no discipline status substitutes for an end-to-end thread; no hard constraint is averaged away; no evidence item omits applicability and anomalies; no action item is called closure; no residual risk lacks an owner and acceptance authority; no condition lacks enforcement and stop criteria; no dissent is erased; and no approval exceeds the reviewed purpose, configuration, population, environment, and time.

A whole-system review cannot prove absence of unknown failure or guarantee future success. It is disciplined sampling and judgment. Its quality comes from causal integration, evidence integrity, legitimate authority, transparent uncertainty, effective conditions, and continuous renewal.

## Alternatives and Trade-Offs

**Large event versus rolling review.** A major event concentrates attention and independent challenge but can create document surges and stale snapshots. Rolling review keeps evidence current but may fragment the decision. Use continuous claim maintenance with focused decision events.

**Discipline panels versus integrated thread teams.** Discipline panels provide depth and consistent standards; integrated teams expose cross-boundary interactions. Use both, with mission threads forcing reconciliation and named owners for conflicts.

**Broad coverage versus deep sampling.** Broad checklists reduce omission but encourage shallow review. Deep dives expose mechanisms but can miss unsampled areas. Use risk- and decision-based sampling, coverage maps, random challenge where useful, and explicit residual uncertainty.

**Consensus versus recorded dissent.** Consensus simplifies recommendation but can suppress weak signals and power differences. Recorded dissent preserves uncertainty but requires a clear decision authority. Seek evidence-based agreement without making unanimity a closure rule.

**Conditional approval versus deferral.** Conditions can enable bounded learning when controls and stop authority are effective. They become schedule waivers when unowned or unenforceable. Defer when missing evidence or control is decision-critical and exposure cannot be bounded.

**Independent review versus embedded expertise.** Independent reviewers challenge assumptions; embedded engineers know context and history. Pair access and expertise with conflict disclosure, independent leadership, direct evidence, and protected challenge.

## Failure Modes and Misconceptions

- **“The review is a meeting.”** The meeting samples a controlled evidence and decision process.
- **“All teams are green.”** Local status does not establish end-to-end outcome or interaction safety.
- **“The document exists.”** Presence does not establish correctness, applicability, implementation, or outcome.
- **“Requirements passed, so validation passed.”** Conformance and stakeholder fitness are distinct.
- **“Component tests cover the system.”** Interfaces, environment, people, organizations, and recovery create system behavior.
- **“A high readiness score is enough.”** A noncompensable failed gate can block the claim.
- **“Risk is one number.”** Different losses, rights, uncertainties, and causal mechanisms resist false aggregation.
- **“The supplier owns that risk.”** Retained stakeholder and operational obligations cross contracts.
- **“Operators can handle exceptions.”** Feasible workload, information, authority, skill, and recovery require evidence.
- **“Backup means recoverable.”** Restoration, integrity, reconciliation, dependency, timing, and exercised authority matter.
- **“An action plan closes the finding.”** Closure needs verified effect and authorized disposition.
- **“No dissent means agreement.”** Hierarchy, schedule, and process can silence disagreement.
- **“Conditional approval is low risk.”** Conditions need enforceability, monitoring, expiry, and stop authority.
- **“The review approved the product.”** The decision covers only its stated purpose, configuration, and envelope.
- **“Passing once establishes readiness.”** Systems, organizations, threats, law, suppliers, and environments evolve.

## Worked Examples

### Example 1

**Situation:** Every microservice passes tests, but the ordering thread retries non-idempotent payment after timeout. **Reasoning:** Component evidence misses unknown outcome and cross-service recovery. Review the end-to-end contract and fault trace. **Conclusion:** Green components can compose into an unsafe mission thread.

### Example 2

**Situation:** A model card reports strong accuracy, but production features can be twelve hours stale. **Reasoning:** Evaluation assumes current data and does not cover pipeline delay or operator visibility. **Conclusion:** Model evidence does not establish configured capability performance.

### Example 3

**Situation:** Security requires step-up authentication for emergency shutdown. **Reasoning:** During identity failure, the safety action becomes unavailable. Design bounded offline authority, audit, expiry, and reconciliation. **Conclusion:** Whole-system review must reconcile protected constraints rather than approve isolated controls.

### Example 4

**Situation:** A supplier certification is current, but the reviewed service uses an excluded region and subcontractor. **Reasoning:** Scope and actual dependency do not align. Obtain applicable evidence or treat the claim as open. **Conclusion:** Certification labels are not transitive assurance.

### Example 5

**Situation:** A recovery action says “restore from backup.” **Reasoning:** The team has not tested identity, keys, infrastructure, schema migration, replay, reconciliation, or RTO. Exercise the integrated path. **Conclusion:** Recovery is an end-to-end capability, not an artifact.

### Example 6

**Situation:** A review closes a critical finding when a ticket is assigned. **Reasoning:** The causal condition and criterion remain unchanged. Keep it open until implementation and outcome evidence pass or legitimate authority accepts residual risk. **Conclusion:** Work assignment is not closure.

### Example 7

**Situation:** Operators approve an automated decision in under five seconds. **Reasoning:** The review shows no accessible evidence, meaningful override, or workload margin. Treat oversight as ineffective and redesign allocation. **Conclusion:** A human signature is not a system control by itself.

### Example 8

**Situation:** One reviewer disputes launch because load testing omitted correlated regional failover. **Reasoning:** Schedule pressure favors consensus, but the scenario matches common cause and capacity risk. Record dissent and require decision authority to disposition it. **Conclusion:** Dissent is assurance evidence, not process failure.

### Example 9

**Situation:** A pilot is approved for internal experts, then marketing opens it globally. **Reasoning:** Population, language, jurisdiction, support, and load leave the review envelope. Trigger renewed review or enforce scope. **Conclusion:** Operational expansion is a configuration change.

### Example 10

**Situation:** An adaptive service passes launch review, then its vendor changes the base model. **Reasoning:** Behavior and evidence identity change behind the same API. Freeze, stage new evidence, or fall back under predeclared authority. **Conclusion:** Review decisions need executable renewal triggers.

## Cross-Program Connections

- **API and Service Engineering:** whole-service review integrates consumer tasks, behavioral contracts, failure semantics, compatibility, security, operability, and evolution.
- **Platform Engineering:** platform review examines developer outcomes, paved paths, tenancy, policy, control planes, observability, support, adoption, and recovery.
- **Data Engineering:** data capability review follows source-to-outcome lineage, quality, time, contracts, privacy, serving, correction, and deletion.
- **Distributed Systems:** partial failure, time, consistency, replication, coordination, capacity, and recovery shape mission threads.
- **Security Engineering:** trustworthiness, threats, abuse, supply chain, response, and resilience must integrate with mission and safety.
- **Software Architecture:** boundaries, decisions, interfaces, qualities, dependency direction, and evolution become reviewable causal mechanisms.
- **Human Factors:** realistic work, authority, workload, modes, handoffs, accessibility, and recovery determine joint capability.
- **Organizations and Governance:** budgets, incentives, decision rights, suppliers, reporting, regulation, ethics, and learning support or defeat controls.
- **Machine Learning:** data, evaluation, drift, feedback, monitoring, change envelopes, human oversight, and remedy require full-system evidence.
- **Economics and Sustainability:** lifecycle cost, externalities, energy, material, labor, concentration, and retirement affect stakeholder value.

## References

1. NASA, [Systems Engineering Handbook](https://www.nasa.gov/reference/systems-engineering-handbook/), NASA/SP-2016-6105 Revision 2.
2. ISO, [ISO/IEC/IEEE 15288:2023 Systems and software engineering—System life cycle processes](https://www.iso.org/standard/81702.html), 2023.
3. National Institute of Standards and Technology, [Engineering Trustworthy Secure Systems](https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final), SP 800-160 Volume 1 Revision 1, 2022.
4. National Institute of Standards and Technology, [Developing Cyber-Resilient Systems](https://csrc.nist.gov/pubs/sp/800/160/v2/r1/final), SP 800-160 Volume 2 Revision 1, 2021.
5. Nancy G. Leveson and John P. Thomas, [STPA Handbook](https://psas.scripts.mit.edu/home/get_file.php?name=STPA_handbook.pdf), MIT Partnership for Systems Approaches to Safety and Security, 2018.
6. Nancy G. Leveson, [CAST Handbook](https://psas.scripts.mit.edu/home/get_file.php?name=CAST_handbook.pdf), MIT Partnership for Systems Approaches to Safety and Security, 2019.
7. U.S. Government Accountability Office, [Agile Assessment Guide: Best Practices for Adoption and Implementation](https://www.gao.gov/products/gao-24-105506), GAO-24-105506, revised 2023.
8. U.S. Department of Defense, [Systems Engineering Guidebook](https://www.cto.mil/sea/pg/), February 2022, indexed by the Office of the Under Secretary of Defense for Research and Engineering.

## Exercises

### Exercise 1

Create a review charter and claim map for deciding whether a regional emergency-notification capability may enter a public pilot.

### Exercise 2

A review ledger contains four mission threads and nine required gates per thread. Thirty-four gates pass. Compute the pass rate and explain why the two failures can still block approval.

### Exercise 3

Conduct a paper whole-system review of an online payment capability during identity-provider failure and regional failover.

### Exercise 4

Write a finding, closure criterion, residual-risk disposition, dissent record, and conditional approval for an unexercised recovery path.

### Exercise 5

Transfer the capstone method to review a multi-tenant internal developer platform before expanding it from ten expert teams to an enterprise population.

## Answers to the Exercises

### Answer 1

The decision is whether a named configuration may notify residents in selected municipalities for specified hazards during a time-bounded pilot. Authority includes emergency management and any required accessibility, privacy, telecommunications, procurement, and public-accountability roles. Possible outcomes are approve, approve with enforceable conditions, restrict, defer, or reject.

Claims include legitimate alert authority; correct geographic and hazard targeting; timely multi-channel delivery; accessibility and language coverage; privacy and security; carrier and cloud dependency behavior; operator workload and override; false, missed, duplicate, and stale alert control; public correction; fallback; and recovery. Trace each through requirements, architecture, interfaces, configuration, evidence, owner, uncertainty, and remedy.

Threads cover normal alert, mistaken alert and correction, cellular congestion, cloud or identity failure, multilingual accessibility, malicious submission, boundary movement, and restoration. Pilot conditions constrain geography, users, hazards, versions, staffing, hours, and load; provide monitoring, public notice, stop authority, complaint and correction, and re-review triggers. A successful internal demonstration cannot alone justify public exposure.

### Answer 2

There are $4\times9=36$ required gates. With 34 passing,

$$
\frac{34}{36}\times100\%\approx94.4\%.
$$

The missing gates must be named by thread and criterion. A failed emergency-authority gate or absent recovery evidence can be noncompensable: success elsewhere cannot make the affected thread feasible. The score is a navigation aid, not a decision rule.

Review whether the two failures can be eliminated, whether exposure can be bounded so the threads are outside authorized scope, or whether legitimate authority can accept a residual risk without violating a hard constraint. Conditional approval is valid only if conditions are enforceable, monitored, owned, time-bounded, and linked to stop authority. Every passing gate still needs applicable evidence rather than a declared status.

### Answer 3

Define outcomes: correct authorized payment, no duplicate charge, protected account and personal data, timely merchant/customer state, recoverable ledger, and lawful dispute. Freeze application, API, identity, database, queue, region, policy, keys, supplier, data, and operator configurations. Map the payment thread from request and authorization through ledger effect, response, settlement, notification, dispute, and reconciliation.

During identity failure, distinguish existing session, new authorization, privileged operation, machine identity, revocation, and emergency access. During regional failover, inspect replication lag, fencing, idempotency, routing, queue replay, clock, capacity, shared identity and DNS, and split-brain prevention. Combine both because the failover mechanism may require the unavailable identity service.

Evidence includes protocol and contract tests, concurrency histories, fault injection, regional exercise, security tests, data-integrity oracles, load tails, operator simulation, supplier evidence, and prior incidents. Test unknown outcome after timeout and downstream correction. Review incident command, customer support, dispute, restoration, reconciliation, and re-entry. If integrated identity-failure-plus-failover recovery is untested, do not infer it from separate tests; restrict, test, or explicitly disposition the gap.

### Answer 4

**Finding:** In configuration K, the team has not exercised restoration of encrypted customer records after regional loss with the production identity/key dependency; the review criterion requires demonstrated integrity and recovery within the approved objective. Evidence consists of component backup tests only. Consequence includes unavailable service, corrupted restoration, and inability to meet customer and regulatory duties. Severity is decision-blocking for broad launch.

**Closure criterion:** Execute an approved integrated scenario on a representative configuration with qualified roles, unavailable primary region, production-equivalent identity/key paths, measured timing, record-count and semantic-integrity reconciliation, anomaly resolution, repeatability, and independent witness. Update operating procedure and evidence links. The closure authority reviews results and side effects.

**Residual-risk disposition:** If a narrow pilot proceeds without full closure, name remaining scenarios, affected stakeholders, uncertainty, compensating controls, owner, and legitimate acceptance authority. **Dissent:** Record the reviewer who considers the pilot still unjustified, their causal rationale, evidence, and requested alternative. **Conditional approval:** Limit population, data, region, load, and duration; require verified daily recoverability, staffed stop authority, no scope expansion, expiry, and automatic suspension on backup, key, or reconciliation failure. Assignment of the exercise is not closure.

### Answer 5

Define platform outcomes for developers and enterprise stakeholders: safe and fast service delivery, usable self-service, policy consistency, tenancy isolation, reliability, cost control, evidence, and support. The expansion changes population, expertise, workloads, jurisdictions, accessibility needs, support demand, and organizational dependencies, so the ten-team evidence cannot be extrapolated directly.

Review threads for new-service onboarding, routine deployment, policy denial and appeal, secret and identity rotation, dependency failure, tenant isolation, data incident, platform upgrade, rollback, cost anomaly, and disaster recovery. Trace portal, APIs, templates, control plane, clusters or cloud, identity, networking, observability, source and artifact systems, support, security, finance, and suppliers.

Evidence combines usability and cognitive-work studies, policy and security tests, tenant fault and abuse tests, capacity and tail load, upgrade and mixed-version tests, backup/recovery, developer outcome data, accessibility, support simulation, incidents, and cost attribution. Conditions for staged expansion include cohort limits, adoption support, service objectives, exception authority, rollback, monitoring, stop criteria, and re-review at scale thresholds. A platform's paved path is ready only when the whole organizational and technical capability can sustain both ordinary and exceptional work.
