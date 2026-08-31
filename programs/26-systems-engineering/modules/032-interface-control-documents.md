---
module_id: SYSENG-032
program: Systems Engineering
level: 1
module_number: 32
title: Interface Control Documents
status: complete
last_verified: 2026-08-31
---

# Interface Control Documents

## One-Page Review

### Governing question

How can two or more independently owned elements establish a precise, jointly controlled, verifiable boundary contract that remains usable across design, procurement, integration, operation, and change?

### Essential definitions

- An **interface requirement** states a necessary, verifiable obligation at a boundary. It belongs in the applicable requirements baseline even when displayed in an interface document.
- An **interface requirements document (IRD)** organizes requirements imposed on the interfacing parties. Local usage varies, so the document's declared purpose and authority matter more than its acronym.
- An **interface control document (ICD)** is a configuration-controlled technical agreement that identifies the interface, both sides' responsibilities, applicable constraints, and change authority. It may contain requirements, definitions, drawings, tables, and verification mappings.
- An **interface definition document (IDD)** describes an offered or established interface, often from one provider's perspective. Description alone does not prove bilateral agreement or compatibility.
- An **interface control drawing** controls geometric, mechanical, electrical, or other drawing-based characteristics at an interface plane.
- An **interface plane** is the declared physical or conceptual boundary at which responsibilities and measurable conditions are assigned.
- A **provided obligation** is what one endpoint guarantees at the interface; a **required obligation** is what the other endpoint assumes or accepts.
- An **applicable document** is binding only to the extent invoked. A **reference document** is informative unless another controlling statement makes it binding.
- **Precedence** states which controlled source governs when statements conflict. It must not be used to tolerate known inconsistency.
- **Interface compatibility** means every relevant guarantee, demand, assumption, environment, behavior, and lifecycle condition of the connected endpoints can be satisfied together.
- A **verification mapping** links a stable interface requirement to method, level, configuration, conditions, responsible party, pass criterion, and retained evidence.
- A **deviation** authorizes departure for a specific future unit or activity; a **waiver** commonly accepts a known nonconformance in an existing unit. Programs must define their own controlled terminology.
- A **version compatibility matrix** identifies which independently released endpoint versions are permitted to interoperate and under what conditions.

### Central model, mechanism, or theorem

Model endpoint (A)'s guarantees as (G_A), endpoint (B)'s acceptable demands as (R_B), and the applicable shared environment as (E). For an (A\rightarrow B) transfer, compatibility requires:

$$
E\land G_A \Rightarrow R_B.
$$

For a scalar interval, including bounded path loss or uncertainty, a sufficient envelope check is:

$$
[g_{min}-\delta_{-},\;g_{max}+\delta_{+}]\subseteq[r_{min},\;r_{max}].
$$

Real interfaces require a conjunction across semantics, units, geometry, timing, state/mode, capacity, faults, authority, safety, security, environment, lifecycle, and version. Passing one dimensional check does not establish compatibility.

An ICD record can be represented as:

$$
D=\langle id,scope,plane,endpoints,applicability,authority,precedence,
obligations,assumptions,verification,changes,evidence,version,status\rangle.
$$

The document is adequate only when these declarations are mutually consistent with both endpoint baselines and with the authoritative interface data. Signatures establish approval, not physical or behavioral truth.

### Critical invariants

- Scope, boundary, interface plane, endpoints, variants, lifecycle interval, modes, and excluded concerns are explicit.
- Every normative obligation has a stable identifier, a responsible side, measurable condition, applicability, rationale/trace, and verification mapping.
- Both sides' guarantees and assumptions are written separately; “shared responsibility” never hides ownership.
- Units, reference frames, sign conventions, tolerances, uncertainty, sampling basis, and conversions accompany numerical values.
- Message syntax and transport are not substitutes for semantics, authority, ordering, timing, state transitions, error behavior, and recovery.
- Applicable and reference documents are distinguished, revisions are pinned, and precedence is explicit.
- The ICD does not silently duplicate higher-level requirements; controlled sources and displayed views remain traceable.
- All affected endpoint representatives participate in technical validation and approval; the named change authority controls baselined changes.
- Each change receives compatibility, safety, security, verification, schedule, supplier, and operational impact analysis before disposition.
- Open values and assumptions have bounded interim constraints, owners, decision evidence, due conditions, and affected requirements.
- Verification records identify the exact endpoint versions, article, environment, equipment, procedures, acceptance criteria, results, anomalies, and retained evidence.
- A released ICD and the version compatibility matrix agree with the configurations authorized for integration and operation.

### Common failures

Common failures include using an ICD acronym without defining its authority; naming only one endpoint; locating the interface plane inside both suppliers' responsibility or neither's; declaring the latest revision of every external standard applicable; copying requirements into several documents; specifying pin numbers but not signal semantics; naming a field without units or valid range; using nominal values without tolerance or transient limits; mixing coordinate frames; omitting initialization, timeout, retry, degraded mode, maintenance, and shutdown; assigning changes to a generic integration team; treating a signed document as proof of compatibility; approving incompatible endpoint versions; leaving unresolved values unbounded; accepting a supplier data sheet as system verification; and changing a boundary without re-verifying downstream behavior.

### Compact example

A power source guarantees 27–29 V at its connector. Harness loss can reduce voltage by at most 1.2 V and does not raise it. The receiving controller accepts 24–28 V at its connector. Delivered voltage is therefore 25.8–29 V. The lower bound is acceptable, but the upper bound exceeds the receiver limit by 1 V. Both suppliers may satisfy their component specifications while the interface is incompatible. An adequate ICD pins the two measurement planes, steady-state and transient conditions, load range, polarity, return path, grounding, connector and pin assignment, current/inrush limits, protection behavior, test method, and change authority. Approval cannot repair the numerical mismatch; architecture or requirements must change.

### Connections

SYSENG-031 produces the controlled interface inventory. This module turns selected interface candidates into governed, verifiable contracts. SYSENG-033 deepens the technical characteristics of data, control, mechanical, electrical, and human interfaces. SYSENG-034–040 use interface definitions to develop physical architecture, integration sequence, verification, and validation. Requirements, configuration management, supplier management, safety, security, human factors, operations, and technical data management all depend on the same interface identities and baselines.

## Governing Question

What information, authority, evidence, and change discipline must an interface control document provide so that independently developed elements can be integrated without relying on oral knowledge, ambiguous ownership, or accidental compatibility?

The answer is not a universal template. It is a controlled boundary contract whose content is tailored to the interface's risks and media while preserving a common assurance structure: explicit scope and plane; identified parties and authority; separately stated provided and required obligations; units, frames, modes, and versions; traceable decisions; compatibility reasoning; verification mappings; and controlled change. The acronym is secondary. A project may use IRD, ICD, IDD, interface agreement, drawing, schema, protocol specification, or a model repository. What matters is the declared normative role of each artifact and the consistency of the complete controlled information set.

## Why This Matters

Integration failures are often lawful local implementations of an unlawful global agreement. A source produces exactly its specified voltage, timestamp, load, message, torque, or alarm; a receiver accepts exactly its own specified envelope; yet the two envelopes do not overlap. Each team can present passing unit tests while the assembled system fails. The ICD exists to make this boundary-level reasoning explicit early enough to influence design and procurement.

Interfaces also cross ownership. Different organizations use different vocabularies, coordinate systems, release schedules, assumptions, evidence practices, and commercial incentives. A verbal promise may disappear with staff turnover. A slide may not be configuration controlled. A provider API page may change without consumer approval. A mechanical drawing may pin geometry but omit load cases. A single database field may represent local time on one side and UTC on the other. Durable control requires one discoverable source of authority and a disciplined relationship among models, specifications, drawings, code/schema repositories, and verification evidence.

NASA's current Interface Management guidance identifies definition, compatibility, strict control, integration, and verification as connected activities. It lists IRDs, ICDs or drawings, IDDs, and interface control plans as possible work products rather than declaring one universal artifact. It also states that baselined interface changes should undergo requirements change management and that interfaces requiring approval from all sides require unanimous approval. NASA's current Appendix L outline requires purpose and scope, precedence, responsibility and change authority, binding and reference documents, interface-plane responsibilities, coordinate systems, engineering units, tolerances, conversion, and domain-specific requirements. These are strong content prompts, not a license to copy a generic outline without tailoring.

An ICD has multiple consumers. Architects use it to judge compatibility and coupling. Suppliers use it to design endpoint behavior. Integrators use it to assemble and configure products. Verification teams derive conditions and acceptance criteria. Operators use version and mode restrictions. Safety and security specialists inspect hazardous energy, command authority, trust boundaries, and fault behavior. Configuration managers need baselines and change decisions. Acquirers need an enforceable allocation of obligations. A useful ICD must support these decisions without pretending that one document contains all lower-level design detail.

## Prerequisites and Retrieval

Before continuing, retrieve these ideas:

1. system and element boundaries determine where responsibility can be assigned;
2. interface identification records candidate endpoints, kinds, modes, ownership, and discovery evidence;
3. a requirement is necessary, singular enough to verify, feasible, unambiguous, and traceable;
4. logical architecture defines what must interact before selecting physical realization;
5. physical architecture introduces connectors, paths, dimensions, loads, energy, environments, and installation constraints;
6. state and mode models define when transfers are permitted, required, or prohibited;
7. configuration baselines identify the exact versions against which evidence is valid;
8. verification asks whether a product conforms to specified requirements, whereas validation asks whether the resulting system serves intended use in context.

As a retrieval test, inspect the statement “System A sends pressure to System B over the standard interface.” Ask: Which physical or logical plane? Absolute or gauge pressure? What units? What reference datum? Which range, accuracy, resolution, sample time, latency, freshness, and invalid indication? Which endpoint converts units? What happens at startup, calibration, sensor failure, communication loss, and maintenance? Which versions interoperate? Who can change the definition? What evidence establishes conformance on each side and end-to-end compatibility? If these questions are unanswered, the statement is an interface candidate, not a sufficient controlled contract.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish an interface register, requirement, IRD, ICD, IDD, control drawing, agreement, implementation specification, and verification record;
2. define the normative purpose, scope, interface plane, endpoints, applicability, exclusions, precedence, and change authority of an interface document;
3. express provider guarantees, consumer demands, assumptions, and environmental constraints as compatible, verifiable obligations;
4. specify units, tolerances, conversions, coordinate frames, sign conventions, timing, states, protocols, loads, and lifecycle conditions without ambiguity;
5. structure interface information across requirements, models, drawings, schemas, and repositories while avoiding uncontrolled duplication;
6. evaluate scalar envelopes and multidimensional contracts for compatibility, margins, uncertainty, and edge cases;
7. create verification mappings with methods, configurations, conditions, pass criteria, responsibilities, and retained evidence;
8. govern unresolved decisions, anomalies, deviations, waivers, versions, and changes without masking risk;
9. conduct bilateral technical review and distinguish approval evidence from compatibility evidence;
10. tailor the depth and form of an ICD to interface criticality while preserving the assurance invariants.

## Core Exposition

**Declare the artifact's role.** Begin with a document-control statement: whether the artifact defines requirements, describes an offered interface, records a joint agreement, controls a drawing, plans interface management, or presents a generated view of model data. State which parts are normative. Acronyms are inconsistent across industries; a title does not establish authority. If the authoritative values reside in a requirements database or schema repository, the rendered ICD must identify its source and generation/version rules.

**Fix the scope and interface plane.** Name the system of interest, both endpoint baselines, physical or conceptual interface plane, lifecycle interval, variants, configurations, modes, environments, and exclusions. A power requirement measured at the source connector differs from one measured after the harness. A network service boundary at a load balancer differs from an internal service-to-database boundary. A mechanical plane should be locatable from controlled datums. Ambiguous planes create gaps or overlaps in responsibility.

**Identify parties and responsibilities.** Name the organization and technical owner for each endpoint, the interface owner or working group, approving authorities, configuration-management authority, anomaly coordinator, and verification responsibility. Use a responsibility matrix if necessary, but express concrete verbs: defines, supplies, accepts, measures, verifies, approves, releases, monitors, and resolves. “Both parties are responsible” is incomplete unless joint action and each side's individual duties are stated.

**Establish precedence without manufacturing conflict.** List binding applicable documents separately from informative references. Pin editions, revisions, profiles, and invoked clauses. State which source controls if a conflict is discovered and how the conflict is resolved. Avoid “latest version” for a binding standard: it delegates change authority to an external publisher and makes the baseline non-reproducible. Do not repeat higher-level requirements merely to make the ICD look complete; use stable trace links or controlled generated views.

**Give every obligation a stable identity.** A normative statement needs an ID, responsible side, applicability, condition, required outcome, units and tolerance where relevant, rationale, source/parent trace, and verification mapping. Stable IDs permit reviews, changes, tests, anomalies, and waivers to refer to the same obligation. Renumbering for visual neatness destroys history; preserve IDs and mark retired obligations with rationale.

**Separate guarantees from demands.** For every direction, state what the providing side guarantees at the plane and what the receiving side requires or accepts. A provider's nominal behavior is not a guarantee. A consumer's preferred value is not necessarily a hard limit. Record whether bounds are inclusive, under what loads and environments they apply, and how uncertainty is handled. Then demonstrate implication or envelope containment. For bidirectional behavior, repeat the analysis in both directions.

**Define semantics before encoding.** Name each information item, physical quantity, command, event, material, force, or human action in domain terms. Define meaning, origin, validity, authority, units, range, precision, freshness, lifecycle, and invalid/unknown representation. Only then define encoding, field width, pin, connector, protocol, topic, file, display, or control. Two endpoints can parse the same bytes yet disagree about whether a timestamp denotes occurrence, receipt, or publication.

**Control numerical meaning.** Declare engineering units, measurement plane, coordinate frame, datum, axis orientation, handedness, sign convention, reference condition, nominal value, minimum/maximum, tolerance, accuracy, precision, resolution, uncertainty, conversion, rounding, and saturation. Distinguish specification tolerance from measurement uncertainty. If conversion is permitted, assign who performs it and define rounding and overflow behavior. Use drawings for geometry but retain stable requirement links.

**Describe states, modes, and sequences.** Define initialization, discovery, negotiation, authentication, ready, active, inhibited, degraded, maintenance, update, shutdown, and recovery behavior as applicable. Specify allowed transitions, triggers, preconditions, acknowledgements, timeouts, retries, duplicate handling, cancellation, compensation, and idempotency. A steady-state field table is insufficient when interoperability depends on sequence.

**Specify timing and ordering.** Identify the time scale and source, clock synchronization assumptions, timestamp semantics, latency measurement points, response deadlines, sample rate, jitter, freshness, ordering scope, concurrency behavior, and loss/duplication policy. State percentile or worst-case basis and observation interval. “Real time” and “immediate” are not verifiable conditions.

**Specify capacity and resource envelopes.** Define throughput, burst, queue, storage, connection, power, current, thermal, fluid, load, force, duty-cycle, attention, or staffing envelopes. State whether values are sustained, peak, simultaneous, or mutually exclusive. Account for overhead and transient behavior. Consumers must not infer that a rated maximum can be sustained under every environmental or mode combination.

**Cover faults and absence.** Define detection of malformed, stale, missing, late, duplicated, contradictory, out-of-range, mechanically misaligned, leaking, overheated, overloaded, unauthorized, or unsafe interaction. State containment, indication, timeout, fail-safe/degraded behavior, retry limits, reconciliation, recovery authority, and evidence. Absence of a message or human response has no meaning without a time basis and expected state.

**Control authority and security.** Identify who may issue commands, update configuration, access data, connect equipment, override interlocks, approve a human action, and change the interface. Define identity, authentication, authorization, integrity, confidentiality, anti-replay, audit, key/certificate lifecycle, data classification, privacy, retention, and secure failure as applicable. Security controls are interface semantics, not an external appendix to be added later.

**Address safety and human use.** Record hazardous energies, inhibits, interlocks, safe states, command confirmation, conflicting authority, protective grounding, guarding, labeling, accessibility, workload, alarm priority, visibility, reach, force, anthropometric range, language, training, maintenance access, and emergency action. Human interfaces include procedures, tools, environment, staffing, and organizational handoffs—not only screen layout.

**Tailor by physical domain.** Mechanical interfaces need datums, dimensions, envelopes, material/contact constraints, fasteners, torque, stiffness, loads, alignment, finish, access, and assembly sequence. Electrical interfaces need voltage/current, polarity, grounding/bonding, isolation, impedance, power quality, transients, protection, EMC, connectors, pins, and mating cycles. Fluid and thermal interfaces need media, cleanliness, compatibility, pressure, temperature, flow, leakage, heat transfer, contamination, connection/disconnection, and venting. Data/control interfaces need semantics, schemas, protocols, timing, state, errors, security, and version rules. A single interface may couple several domains that must be analyzed together.

**Represent linked information without duplication.** An interface definition may span a requirement database, architecture model, drawing, data schema, protocol repository, hazard record, and verification system. Define one authoritative owner for each data item. Use stable identifiers and controlled references. Generate human-readable views where practical. Automated consistency checks can catch missing IDs or mismatched versions, but human review is still needed for meaning, physical feasibility, and operational fitness.

**Bound unresolved information.** Early ICDs may contain decisions that are not yet final. Record the unresolved item as a controlled issue with affected obligations, responsible decision owner, interim safe or design envelope, evidence needed, decision criterion, due event, and escalation path. An empty cell or vague marker transfers risk invisibly to implementers. If no defensible interim envelope exists for a critical item, the affected design cannot claim a stable baseline.

**Evaluate compatibility explicitly.** Build a compatibility matrix by characteristic and mode. Compare source guarantee with receiver acceptance, path effect, shared environment, uncertainty, and margin. Check both directions. Examine combinations, not only individual maxima: peak power, maximum thermal load, high throughput, emergency operation, or human workload may coincide. Record the analysis method and evidence limits. Compatibility is a system claim and needs system-level ownership.

**Map every requirement to verification.** For each interface requirement, select inspection, analysis, demonstration, or test; name the verifying side and witness/acceptance authority; identify article and configuration; define environment, equipment, stimulus, measurement points, accuracy, procedure, pass/fail criteria, and retained result. Some requirements need separate provider, consumer, and integrated verification. A supplier certificate is useful evidence only within its declared configuration and conditions.

**Plan integration evidence.** Define pre-mate inspections, fit checks, electrical continuity/insulation, leak checks, schema conformance, simulators, emulators, golden datasets, contract tests, hardware-in-the-loop tests, end-to-end tests, fault injection, security tests, human-in-the-loop evaluation, and post-integration monitoring as applicable. Identify safe constraints for first connection. Record anomalies against the exact baseline and test context.

**Control versions and releases.** Assign the ICD a configuration identifier and baseline. Identify endpoint hardware, software, firmware, data, procedure, and model versions. Maintain a compatibility matrix rather than assuming identical version numbers imply compatibility. Define backward/forward compatibility, negotiation, deprecation, coexistence, rollback, migration, and support windows. Release notes cannot silently modify normative behavior.

**Govern changes bilaterally.** A change request should identify affected requirement IDs, current and proposed values, reason, urgency, endpoint versions, architecture impacts, safety/security effects, verification impact, cost/schedule/supplier effects, operational transition, rollback, and affected evidence. Obtain the approvals required by the interface-control plan. Rebaseline and notify all data consumers. Emergency changes still require retrospective control and evidence.

**Manage anomalies, deviations, and waivers.** Record observed versus expected behavior, affected article/version, conditions, evidence, containment, consequence, and disposition authority. A deviation or waiver must be bounded in configuration, quantity, time, and use. It must not edit the underlying requirement or establish precedent silently. Determine whether the discrepancy reveals an erroneous requirement, a nonconforming implementation, an invalid test, or an incomplete system assumption.

**Conduct joint technical validation.** Representatives from both endpoints, integration, verification, operations, configuration management, and relevant specialty disciplines should review the controlled content. Walk nominal, boundary, degraded, emergency, maintenance, update, and recovery scenarios. Recompute critical envelopes. Inspect units, frames, authority, and versions. A signature records that authorized people approved a baseline; it is not evidence that every calculation or implementation is correct.

**Tailor with explicit rationale.** A low-criticality internal interface may be governed by a versioned schema and contract tests with a short control record. A safety-critical supplier boundary may need an IRD, ICD, drawings, models, hazard links, formal change board, independent verification, and witnessed integration. Tailoring removes irrelevant formality, not essential clarity. Record why omitted content does not apply.

**Preserve decision history.** Retain rationale for critical limits, rejected alternatives, assumptions, change dispositions, anomaly corrections, and verification exceptions. Future engineers need to know whether a value is physically necessary, allocated by budget, inherited from a standard, selected for compatibility, or merely conventional. Without rationale, later optimization can erase a system-level constraint.

**State evidence limits.** Document review can show declaration quality and cross-reference consistency, not product conformance. Unit tests can show behavior for tested cases, not every physical environment. Type/schema validation can show structural conformance, not semantic agreement. A successful pairwise test does not establish compatibility under all multi-element loads, faults, versions, or human conditions. Keep conclusions bounded to examined baselines and evidence.

The following executable check examines five simplified ICD section records. It verifies declared control fields only; it cannot establish semantic or physical compatibility.

<!-- bijux-verify: {"id":"icd-control-record-check","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"records_total=5\nwell_formed_declared=1\nmissing_scope=ICD-002\nmissing_endpoints=ICD-003\nmissing_change_authority=ICD-004\nmissing_verification=ICD-005\nunresolved=ICD-002,ICD-003,ICD-004,ICD-005\nevidence=declared_control_fields_only\n","stderr":""}} -->
```python
records = [
    {"id": "ICD-001", "scope": "Controller-to-actuator command boundary",
     "endpoints": ["Controller R3", "Actuator A2"],
     "change_authority": "Joint Interface Board",
     "verification": ["CMD-101: test at 40 ms deadline"]},
    {"id": "ICD-002", "scope": "", "endpoints": ["Source", "Load"],
     "change_authority": "Power Interface Board", "verification": ["PWR-201: test"]},
    {"id": "ICD-003", "scope": "Service boundary", "endpoints": [],
     "change_authority": "Service Interface Board", "verification": ["API-301: contract test"]},
    {"id": "ICD-004", "scope": "Mounting plane", "endpoints": ["Frame", "Payload"],
     "change_authority": "", "verification": ["MECH-401: inspection and load analysis"]},
    {"id": "ICD-005", "scope": "Operator alarm boundary", "endpoints": ["Console", "Operator"],
     "change_authority": "Human Systems Board", "verification": []},
]
required = ("scope", "endpoints", "change_authority", "verification")
valid = [record for record in records if all(record[field] for field in required)]
print(f"records_total={len(records)}")
print(f"well_formed_declared={len(valid)}")
for field in required:
    print(f"missing_{field}=" + ",".join(r["id"] for r in records if not r[field]))
print("unresolved=" + ",".join(r["id"] for r in records if r not in valid))
print("evidence=declared_control_fields_only")
```

Even `ICD-001` could contain an incorrect deadline, mismatched time basis, unsafe command authority, or incompatible implementation. The checker proves only that selected declarations are populated.

## Definitions and Notation

Let endpoint (A) provide an item to endpoint (B) across path (P) in configuration (c\in C), mode (m\in M), and environment (e\in E).

Provider guarantee set:

$$
G_A(c,m,e)=\{x\mid A\text{ guarantees item }x\text{ at its declared plane}\}.
$$

Path transformation:

$$
T_P(x,c,m,e)=\text{item observable at the receiver plane after path effects}.
$$

Receiver acceptance set:

$$
R_B(c,m,e)=\{y\mid B\text{ accepts }y\text{ while satisfying its obligations}\}.
$$

Directional compatibility is:

$$
\forall(c,m,e)\in Applicable:\quad T_P(G_A(c,m,e))\subseteq R_B(c,m,e).
$$

For scalar guaranteed interval (G=[g_l,g_u]), additive path effect (D=[d_l,d_u]), and receiver interval (R=[r_l,r_u]):

$$
T_P(G)=G+D=[g_l+d_l,g_u+d_u],
$$

$$
Compatible\iff r_l\le g_l+d_l\land g_u+d_u\le r_u.
$$

Define lower and upper margins:

$$
M_l=(g_l+d_l)-r_l,\qquad M_u=r_u-(g_u+d_u).
$$

Both must be nonnegative. Negative margin quantifies an envelope violation on that bound; positive margin is not automatically a reliability margin unless uncertainty and applicable extremes are already included.

For an interface contract with characteristics (K), compatibility is conjunctive:

$$
Compatible(D)=\bigwedge_{k\in K} Compatible_k.
$$

This formulation exposes why averaging scores is unsafe: excellent documentation for nine characteristics cannot compensate for one incompatible voltage, load, coordinate frame, command authority, or hazardous state transition.

Let normative obligations be (Q), endpoint baselines be (B_A,B_B), and verification records be (V). Useful trace relations include:

$$
allocates\subseteq Q\times\{A,B,Joint\},\quad
implementedBy\subseteq Q\times(B_A\cup B_B),\quad
verifiedBy\subseteq Q\times V.
$$

Trace completeness indicators may identify missing declarations:

$$
C_V=\frac{|\{q\in Q:\exists v,(q,v)\in verifiedBy\}|}{|Q|}.
$$

(C_V=1) means every listed requirement has a verification mapping. It does not prove that the list is complete, the method is adequate, the evidence passed, or the system is compatible.

A change request can be modeled as:

$$
\Delta=\langle id,affected\_ids,old,new,rationale,impact,approvals,
transition,reverification,disposition\rangle.
$$

A version compatibility relation $K_V\subseteq V_A\times V_B\times C$ records approved endpoint-version/configuration triples. Compatibility is a controlled relation, not an inference from version-number ordering.

## Mechanisms, Invariants, or Proof Structure

The core reasoning mechanism is assume–guarantee compatibility. Each endpoint specification is locally satisfiable only under assumptions about the other side and the environment. The ICD externalizes those assumptions, assigns them, and checks that the opposite side guarantees them. For (A\rightarrow B):

1. define the exact planes and applicable states;
2. derive (A)'s guaranteed output envelope from its baseline;
3. transform the envelope through harness, network, medium, operator, or environment effects;
4. derive (B)'s accepted input envelope and required semantics;
5. prove containment or identify a counterexample;
6. map the controlled obligations to implementation and verification evidence;
7. repeat for reverse flows, faults, lifecycle conditions, and configuration combinations.

This is a proof structure, not a claim that every interface can be reduced to intervals. Protocol state machines require trace/refinement reasoning. Mechanical interfaces require geometric and load compatibility. Human interfaces require empirical evidence under representative tasks and populations. Security requires adversarial analysis. The general invariant is that every receiver assumption has a justified guarantee, environmental condition, operational control, or explicitly accepted risk.

**Scope invariant.** Every normative statement is interpretable against one declared boundary, plane, configuration, mode, environment, and lifecycle interval. If applicability is implicit, two reviewers may reach opposite conclusions while reading the same value.

**Ownership invariant.** Each obligation has exactly one accountable providing or controlling side, even when approval is joint. Joint approval means all required parties consent to the boundary contract; it does not erase delivery responsibility.

**Meaning invariant.** Each exchanged item has one controlled semantic definition per applicable version. Encoding aliases and display labels trace to that definition. If meanings differ by mode or version, the distinction is explicit and detectable.

**Dimensional invariant.** Numerical comparisons use compatible dimensions, units, reference frames, planes, sign conventions, and statistical bases. A numerical equality between incompatible quantities is meaningless.

**Envelope invariant.** For every permitted configuration and relevant extreme, the provider/path output remains within the receiver's accepted domain. Nominal-point equality is insufficient.

**State invariant.** Every permitted event or command has defined legality, authority, effect, acknowledgement, error behavior, and recovery for the states in which it can occur. Prohibited events have defined detection and response where risk warrants it.

**Configuration invariant.** Every integration and operational configuration is a member of the approved version compatibility relation. Verification evidence names the same baselines or documents justified equivalence.

**Trace invariant.** Each interface requirement traces upward to need/architecture/hazard/decision where applicable and downward to endpoint implementation allocation and verification evidence. Displayed copies do not create competing authorities.

**Change invariant.** A baselined semantic or numerical change cannot become effective until its affected configurations, parties, analyses, evidence, transition, and rollback are dispositioned by the declared authority.

**Evidence invariant.** A conformance claim is bounded by article, baseline, environment, method, measurement uncertainty, procedure, result, and anomalies. Approval and successful execution of unrelated tests cannot substitute for this evidence.

An adversarial review attempts to break these invariants. It selects minimum and maximum values; conflicting modes; startup and shutdown; old/new version pairs; clock loss; duplicate or delayed messages; wrong units; reversed polarity; tolerance stack-up; simultaneous peak loads; operator overload; maintenance equipment; unauthorized commands; failed conversion; and emergency change. One counterexample disproves the universal compatibility claim for the asserted scope.

## Alternatives and Trade-Offs

**Single document versus federated authoritative data.** A single PDF is easy to review, sign, archive, and contractually reference, but it becomes stale when drawings, schemas, requirements, and tests evolve separately. A federated model/repository reduces duplication and enables queries, but access, tool interoperability, human review, supplier exchange, and long-term preservation become harder. A strong hybrid assigns authority per data class and generates a signed/released human-readable baseline.

**Bilateral ICD versus provider IDD.** A bilateral ICD is appropriate where both sides share change authority and compatibility responsibility. A provider IDD scales when many consumers accept a product interface controlled by the provider. The latter needs versioning, compatibility policy, deprecation notice, and consumer qualification; calling it an agreement does not grant consumers veto power. State the governance honestly.

**Requirement-centered versus design-centered content.** Requirement-centered documents preserve solution freedom and verification clarity. Design-centered documents—drawings, schemas, protocol state machines—can remove implementation ambiguity needed for interchangeability. Over-specification constrains suppliers; under-specification moves decisions to integration. Control only characteristics necessary for compatibility, safety, interchangeability, compliance, and lifecycle support.

**One interface record versus domain-specific documents.** A unified record preserves cross-domain coupling and shared authority. Separate electrical, mechanical, software, safety, and human documents let specialists work effectively. If separated, stable interface identity, shared applicability, synchronized baselines, and cross-domain review are essential; otherwise a connector change can satisfy one document and violate another.

**Natural language versus formal/model-based specification.** Natural language handles rationale and diverse stakeholders but permits ambiguity. Tables, schemas, state machines, interface models, and machine constraints improve precision and automated checking but can encode the wrong semantics precisely. Use multiple representations with declared authority and consistency checks; avoid two normative representations of the same fact unless their equivalence is controlled.

**Point values versus envelopes.** Point values simplify design and tests but ignore variation. Broad envelopes preserve supplier freedom but increase endpoint burden and may reduce performance. Allocate compatible envelopes with justified margin, then verify boundary and transient conditions. Do not narrow an envelope after procurement without impact analysis.

**Synchronous release versus independent versioning.** Synchronized endpoint releases simplify compatibility but couple schedules and rollback. Independent releases improve delivery autonomy but require negotiation, backward compatibility, coexistence, contract testing, monitoring, and a maintained compatibility matrix. Choose based on operational and supplier realities, not software fashion.

**Formal change board versus delegated control.** A joint board provides visibility for high-impact supplier or safety boundaries but may slow low-risk changes. Delegated authorities and change classes can improve flow if criteria, notification, audit, and escalation are explicit. No process should permit a locally “minor” change to alter externally observable semantics without interface impact assessment.

**Pre-integration verification versus integrated discovery.** Simulators, analysis, inspections, and contract tests retire incompatibility early. They may omit physical or emergent effects. Integrated tests discover real behavior but are late and expensive. Layer evidence: specification review, model analysis, endpoint conformance, pairwise integration, system scenarios, faults, and operational monitoring.

## Failure Modes and Misconceptions

**“An ICD is just a template.”** A template prompts sections; it cannot determine boundary, authority, critical characteristics, or evidence. Tailoring requires technical judgment and recorded rationale.

**“The interface is controlled because both sides signed.”** Signatures prove a baseline was approved by identified authorities. They do not prove the values are compatible, implementations conform, or evidence remains valid after change.

**“The API schema is the ICD.”** A schema can govern structure and types. It rarely defines domain semantics, command authority, timing, ordering, privacy, errors, modes, deprecation, operational ownership, or end-to-end verification by itself.

**“A connector drawing defines the electrical interface.”** It can define pins and geometry while omitting voltage quality, current, grounding, shielding, transient, protection, EMC, fault, and mating requirements.

**“Nominal values match, so the interface is compatible.”** Compatibility concerns worst applicable envelopes, path effects, uncertainty, transients, and combinations. Two nominal 28 V components can be incompatible at their allowed extremes.

**“Each supplier passed its unit tests.”** Local conformance does not imply system compatibility if the two specifications contain a gap, use different planes, or omit environment and path effects.

**“The latest standard applies.”** This creates a moving baseline and delegates change. Pin the edition and invoked provisions; evaluate later revisions through controlled change.

**“Precedence resolves inconsistency.”** Precedence tells implementers what controls temporarily. Known contradictions still need correction, impact assessment, and notification because different teams may have implemented the losing statement.

**“Both sides own it.”** Vague joint ownership produces unowned conversions, tests, and anomalies. Allocate individual obligations and name the joint decision mechanism.

**“Open values are harmless until detailed design.”** Unbounded values permit divergent designs. Record a conservative interim envelope or admit that the affected baseline is not yet stable.

**“Passing one integrated test proves compatibility.”** The conclusion is limited to the tested articles, versions, configuration, environment, stimulus, loads, and observations. Boundary, fault, lifecycle, and coexistence cases may remain untested.

**“Backward compatibility follows from version numbering.”** Compatibility is behavior, not arithmetic. Maintain explicit supported pairs and test them.

**“A waiver changes the requirement.”** A bounded acceptance of nonconformance does not silently rewrite the controlled requirement. Permanent change follows the normal change process.

**“Document completion means interface work is complete.”** Interface control continues through procurement, realization, integration, operations, maintenance, update, anomaly resolution, and retirement.

## Worked Examples

### Example 1

**Command semantics and acknowledgement.**

An emergency-notification controller sends `ACTIVATE(zone, message_id)` to a siren gateway. A field-only description says `zone` is an integer and `message_id` is a UUID. It does not establish whether ACTIVATE replaces a current message, queues behind it, or is rejected; which side authorizes the command; whether duplicate UUIDs are idempotent; or what an acknowledgement means.

The controlled contract defines: the controller is the command authority in `ready` and `degraded-network` modes; `zone` identifies a controlled geographic set, not a gateway-local index; a repeated `message_id` has no additional effect; acknowledgement `accepted` means the gateway durably recorded a valid command, not that all sirens sounded; delivery status is a separate event; invalid authority returns `forbidden`; unavailable zones return `unserviceable`; acknowledgement is due within 500 ms measured from gateway receipt; and timeout triggers one status query before escalation. Provider, receiver, and integrated tests map to separate IDs. The improvement is semantic and evidential, not merely syntactic.

### Example 2

**Power-envelope incompatibility.**

Source guarantee at plane (P_S): $G=[27,29]$ V for load 0.5–4 A. Harness drop from (P_S) to receiver plane (P_R): $D=[-1.2,0]$ V. Receiver acceptance: $R=[24,28]$ V.

$$
T_P(G)=[27-1.2,29+0]=[25.8,29]\text{ V}.
$$

Margins are:

$$
M_l=25.8-24=1.8\text{ V},\qquad M_u=28-29=-1.0\text{ V}.
$$

The negative upper margin is a counterexample. Options include limiting source output to 28 V at the relevant conditions, increasing receiver tolerance to 29 V with verified design impact, adding regulation, or relocating the controlled plane. The ICD must also address transient voltage, ripple, inrush, current limit, polarity, return, grounding, protection, and test uncertainty. Averaging (1.8) and (-1.0) is invalid because both bound invariants must pass.

### Example 3

**Mechanical plane and coordinate frame.**

A payload supplier reports center of mass as $(120,20,-5)$ mm, while the carrier computes bolt loads using its own frame. Both use millimetres, but the payload frame origin is the payload centroid and (+z) points outward; the carrier origin is mounting-datum intersection and (+z) points inward. Direct substitution reverses an offset and changes the moment.

The control drawing defines datum planes A/B/C, origin, right-handed axes, direction, transformation matrix, tolerance, payload envelope, hole pattern, fastener class, torque, stiffness, static/dynamic loads, surface finish, keep-out volume, and measurement method. Each endpoint retains internal frames, but values crossing the interface use the controlled frame. A fit check verifies geometry; analysis verifies load compatibility; inspection verifies fastener and torque; integrated modal test addresses coupled dynamics. “Same units” was necessary but insufficient.

### Example 4

**Fluid and thermal coupling.**

A cooling supplier guarantees flow 8–12 L/min at its pump outlet. The instrument requires at least 9 L/min at its inlet when dissipating 4 kW. The hose, filter, elevation, fluid viscosity, and valve create pressure-dependent loss, so flow cannot be verified from the pump rating alone.

The ICD fixes outlet and inlet planes; fluid composition and cleanliness; inlet temperature; pressure and flow envelopes; maximum pressure drop versus flow; allowable leakage; connector, seal, and material compatibility; venting and fill procedure; contamination control; valve state; fault isolation; heat rejection; and sensor accuracy. A system analysis couples the pump curve and path resistance, then a representative loop test measures flow at worst temperature and filter condition. The conclusion is bounded to the modeled and tested fluid properties; an alternate coolant requires change review.

### Example 5

**Human alarm interface.**

A control system requirement says “display a high-temperature alarm to the operator.” The console team implements red text; the operations team assumes an audible alarm, persistent indication, acknowledgement, and a response procedure. The statement crosses a human/organizational boundary but does not allocate the complete interaction.

The ICD section defines triggering condition and hysteresis, severity, priority among concurrent alarms, visual and audible presentation, persistence, acknowledgement meaning, silencing rules, response deadline basis, authority, accessibility, environmental noise and lighting, logging, training/procedure reference, loss-of-display behavior, and maintenance suppression. Verification includes software stimulus, display inspection, alarm timing measurement, and human-in-the-loop validation with representative operators and competing workload. The empirical study supports specified contexts; it does not prove universal human performance.

### Example 6

**Supplier IDD versus joint agreement.**

A cloud identity provider publishes an IDD and controls releases. Twenty consumers cannot unanimously approve every provider change. Calling the IDD a bilateral ICD would misstate authority.

The program instead declares the provider IDD normative for protocol behavior at pinned versions; a consumer interface agreement controls tenant configuration, claims used, availability assumptions, data classification, key rotation coordination, incident notification, accepted provider versions, fallback, and exit strategy. The provider owns protocol evolution under contracted notice; the program board owns which version enters the system baseline. Automated conformance tests run against a staging tenant, while operational monitoring checks certificate expiry and claim anomalies. Governance matches the real relationship.

### Example 7

**Controlled change impact.**

The actuator supplier proposes reducing command timeout from 100 ms to 60 ms to detect faults faster. The change appears local. Impact analysis shows that the controller's worst-case response is 75 ms during log rotation, the integration simulator uses 100 ms, the safety analysis credits timeout for fault detection, operator procedures reference a 100 ms retry sequence, and fielded controller release R3 cannot change remotely.

The request identifies affected requirements, versions, hazard controls, tests, procedures, field configurations, cost, schedule, transition, and rollback. The board rejects immediate rebaseline, accepts a future 80 ms requirement for R4 after performance work, and preserves 100 ms for R3. The compatibility matrix distinguishes actuator firmware versions supporting both profiles. Without controlled impact analysis, the “safer” local change would create false fault trips and mixed-fleet incompatibility.

### Example 8

**Bounded unresolved decision.**

During preliminary design, a sensor supplier has not selected between 50 Hz and 100 Hz output. Leaving sample rate blank lets the analytics team assume 100 Hz and the network team budget 50 Hz.

The controlled issue states that the interface shall support 100 samples/s at 64 bytes/sample for allocation and capacity analysis until selection; latency and freshness limits apply at both rates; the sensor owner must provide power/noise evidence; the analytics owner must provide detection-performance evidence; selection occurs before detailed design review; and either choice requires the same version-negotiation field. The interim 51.2 kbit/s payload rate excludes framing overhead, which the network budget adds explicitly. The bound may overdesign the network temporarily, but it prevents divergent infeasible baselines.

### Example 9

**Version coexistence and migration.**

Service version S2 adds required field `policy_epoch`; client C1 neither sends nor understands it. Service S2 can accept C1 requests by deriving an epoch from authenticated tenant configuration, but S3 will remove that behavior. A release note saying “backward compatible” is too vague.

The compatibility matrix authorizes ((C1,S2)) through a stated date with derived-value telemetry, ((C2,S2)) and ((C2,S3)) without exception, and prohibits ((C1,S3)). The contract defines negotiation, default provenance, audit record, warning threshold, migration owner, rollback, and retirement condition. Contract tests cover each authorized pair; deployment policy blocks unauthorized combinations. Compatibility is attached to observable behavior and controlled time bounds, not version-number order.

### Example 10

**Verification record and bounded conclusion.**

Requirement `IF-TIME-014` states: “In normal mode, the gateway shall publish accepted-command status within 500 ms of receipt at gateway plane GP-1 for loads up to 200 commands/s.” The verification record names gateway hardware H2, firmware 4.6.1, simulator 3.2, synchronized monotonic clocks, network profile N7, 20–30 °C environment, 200 commands/s for 30 minutes, timestamp measurement points, 2 ms instrument uncertainty, pass criterion that every observed latency is at most 500 ms, and retained raw log digest. Maximum observed latency is 472 ms; no loss occurs.

The defensible conclusion is that the tested article and configuration conformed under those conditions. It does not establish performance above 200 commands/s, in degraded mode, at temperature extremes, with firmware 4.7, or under clock failure. Those require other evidence or explicit analysis. The ICD links the result and its scope; it does not rewrite a passing test as universal proof.

## Cross-Program Connections

**Platform engineering.** Platform APIs, identity, policy, observability, quotas, and deployment contracts are interfaces with independently released consumers. Provider-controlled IDDs, compatibility matrices, contract tests, deprecation policies, and operational monitoring translate classic ICD discipline into platform products.

**API and service engineering.** OpenAPI, AsyncAPI, protobuf, and schema repositories can be authoritative encodings, but service compatibility also depends on semantics, state, timing, errors, idempotency, authorization, versioning, and operational constraints. An ICD framework prevents schema-valid semantic failure.

**Data engineering.** Data contracts need ownership, meaning, quality, units, freshness, lineage, schema evolution, backfill/replay behavior, privacy, retention, and verification. Producer guarantees and consumer acceptance sets provide a rigorous model for pipeline compatibility.

**Object-oriented programming.** A programming interface exposes operations and invariants while hiding implementation. Liskov-style substitutability resembles an assume–guarantee obligation: a replacement must not strengthen accepted preconditions or weaken promised postconditions in a way that breaks clients. Runtime type compatibility alone does not prove semantic compatibility.

**Functional programming.** Typed functions make domains and codomains explicit, while algebraic data types expose variants and invalid states. Pure composition helps local reasoning, but effects, time, failure, resources, and distributed versions still require controlled contracts beyond a type signature.

**Requirements and verification.** The ICD is a view and control surface for boundary requirements. Requirement quality, bidirectional traceability, method selection, configuration identification, and retained results connect specification to conformance claims.

**Configuration and supplier management.** Interface values cross contractual and organizational boundaries. Baselining, applicable-document revision control, change authority, notification, version support, anomaly disposition, and evidence delivery belong in acquisition and supplier agreements as well as technical repositories.

**Safety, security, and human factors.** Hazardous energy, command authority, shared resources, trust boundaries, degraded behavior, alarms, maintenance, and emergency actions emerge at interfaces. Specialty analyses both derive interface obligations and challenge their sufficiency.

## References

1. NASA, *Systems Engineering Handbook, Section 6.3: Interface Management*, current web edition, updated 2023. <https://www.nasa.gov/reference/6-3-interface-management/>
2. NASA, *Systems Engineering Handbook, Appendix L: Interface Requirements Document Outline*, current web edition, updated 2023. <https://www.nasa.gov/reference/appendix-l-interface-requirements-document-outline/>
3. NASA, *NPR 7123.1B, NASA Systems Engineering Processes and Requirements, Change 4*, current directive. <https://nodis3.gsfc.nasa.gov/displayAll.cfm?Internal_ID=N_PR_7123_001B_&page_name=ALL>
4. NASA, *Systems Engineering Handbook, Section 5.2: Product Integration*, current web edition, updated 2023. <https://www.nasa.gov/reference/5-2-product-integration/>
5. NASA, *Systems Engineering Handbook, Section 6.5: Configuration Management*, current web edition, updated 2023. <https://www.nasa.gov/reference/6-5-configuration-management/>
6. Object Management Group, *Systems Modeling Language Version 2.0*, formal specification, 2025. <https://www.omg.org/spec/SysML/2.0>
7. Object Management Group, *Systems Modeling Language Version 2.0, Part 1: Language Specification*, formal document, 2025. <https://www.omg.org/spec/SysML/2.0/Language/PDF>
8. ISO/IEC/IEEE, *15288:2023 Systems and software engineering—System life cycle processes*, 2023. <https://www.iso.org/standard/81702.html>
9. ISO/IEC/IEEE, *42010:2022 Software, systems and enterprise—Architecture description*, 2022. <https://www.iso.org/standard/74393.html>

## Exercises

### Exercise 1

A 5 V sensor guarantees 4.75–5.25 V at its output plane. A cable introduces a voltage change from -0.20 V to 0 V. The receiver accepts 4.60–5.10 V at its input plane. Determine the delivered interval, lower and upper margins, and compatibility. State what the arithmetic does and does not establish.

### Exercise 2

Rewrite the weak statement “The navigation service shall quickly send position in standard coordinates to the display” as a small set of controlled interface obligations. Include planes/endpoints, semantics, reference frame, units, timing, invalid data, responsibility, and verification. You may choose defensible numerical values, but label them as design assumptions for the exercise.

### Exercise 3

Classify each artifact and state its likely normative role: (a) an interface register row naming two candidate endpoints; (b) a provider-published protocol and schema controlled only by the provider; (c) a jointly approved drawing controlling mounting datums and bolt pattern; (d) a report containing measured latencies for one released version pair; and (e) a document allocating requirements to both parties and defining joint change authority. Explain why the artifact name alone is not decisive.

### Exercise 4

A supplier proposes changing a temperature field from whole degrees Celsius in an 8-bit signed integer to tenths of a degree Celsius in a 16-bit signed integer. Build a minimum change-impact checklist covering semantics, encoding, units/range, versions, implementations, operations, safety/security, verification, transition, and rollback. Decide whether approval by the supplier alone is sufficient for a jointly controlled interface.

### Exercise 5

Review this verification claim: “ICD compliance passed because 100 requests completed successfully.” Identify at least eight missing pieces of evidence and write a bounded replacement conclusion using reasonable assumed test details.

## Answers to the Exercises

### Answer 1

The path interval is $D=[-0.20,0]$ V. Therefore:

$$
T_P(G)=[4.75-0.20,5.25+0]=[4.55,5.25]\text{ V}.
$$

Receiver interval is $[4.60,5.10]$ V. Margins are:

$$
M_l=4.55-4.60=-0.05\text{ V},\qquad
M_u=5.10-5.25=-0.15\text{ V}.
$$

Both are negative, so the declared worst-case envelopes are incompatible. At the low extreme the delivered voltage may be 0.05 V below acceptance; at the high extreme it may be 0.15 V above acceptance. Nominal 5 V agreement does not repair either counterexample.

The calculation establishes incompatibility if the intervals, planes, path model, and applicability are correct and simultaneous extremes are possible. It does not establish transient response, current capacity, ripple, grounding, noise, protection, temperature behavior, measurement uncertainty, or implementation conformance. Next work must confirm those assumptions and change source regulation, receiver acceptance, path design, or the declared operational envelope before claiming compatibility.

### Answer 2

One defensible exercise answer is:

1. `NAV-IF-001`: In normal-navigation mode, Navigation Service N4 shall publish geodetic position at logical plane NP-1 to Display Service D2 using WGS 84 latitude, longitude, and ellipsoidal height; latitude and longitude shall be decimal degrees and height shall be metres.
2. `NAV-IF-002`: Each position shall carry `occurrence_time`, defined as the instant represented by the navigation solution, encoded as UTC with declared leap-second handling, plus a monotonic sequence number scoped to one N4 startup instance.
3. `NAV-IF-003`: Under the exercise assumption of at most 20 updates/s, N4 shall publish a valid or explicitly invalid position within 200 ms of occurrence, measured from the navigation solution timestamp to receipt at D2 plane DP-1.
4. `NAV-IF-004`: N4 shall set validity to `invalid` when horizontal protection level exceeds the exercise-assumed 25 m limit or when solution age exceeds 500 ms; D2 shall not display invalid data as a current valid position and shall indicate loss of valid navigation within 1 s.
5. `NAV-IF-005`: N4 owns coordinate conversion and validity computation; D2 owns presentation and stale-data indication; the Joint Navigation Interface Board owns changes to the semantic fields, frame, timing, and validity rules.
6. `NAV-IF-006`: Verification shall include schema inspection, known-point coordinate analysis, boundary tests at 200/500 ms, injected invalidity, and an integrated N4–D2 test on the approved version pair; each record shall name configuration, environment, timestamps, accuracy, criteria, and retained logs.

The numerical values are design assumptions for this exercise, not universal navigation requirements. A real project must derive them from operational need, accuracy budgets, hazards, platform behavior, and stakeholder validation. The rewrite separates meaning, encoding, timing planes, invalid behavior, ownership, and evidence.

### Answer 3

(a) The register row is discovery/control metadata for an interface candidate. It identifies work but is not a sufficient interface contract.

(b) The provider-controlled protocol/schema is most like an IDD or provider interface specification. It can be normative for consumers under a contract, but it is not bilaterally controlled merely because consumers depend on it.

(c) The jointly approved datum and bolt drawing is an interface control drawing. It is normative for the characteristics it explicitly controls, but likely needs linked load, material, tolerance, assembly, and verification obligations.

(d) The latency report is verification evidence. It records results for a specified configuration and context; it should not become the source of the requirement it tested.

(e) The jointly controlled allocation/change document functions as an IRD or ICD depending on project definitions. Its declared scope, normative clauses, ownership, and authority determine the role.

Names are not decisive because organizations use the acronyms differently. A document titled “ICD” may be an uncontrolled provider description, while a versioned schema plus a short signed control record may collectively form the enforceable interface baseline. Review the authority, normative content, parties, configuration control, trace, and evidence relationship.

### Answer 4

The minimum impact checklist includes:

- confirm whether the physical meaning remains temperature at the same measurement plane and occurrence time;
- state old and new unit/scale explicitly: integer °C versus integer count representing 0.1 °C;
- compare representable ranges: signed 8-bit whole degrees gives -128 to 127 °C; signed 16-bit tenths gives -3276.8 to 3276.7 °C unless further constrained;
- define accuracy, resolution, rounding, saturation, missing/invalid values, byte order, alignment, field identifier, and schema/protocol framing;
- identify every producer, consumer, recorder, gateway, display, alarm, analytics job, test tool, simulator, archive, and replay path;
- analyze thresholds, historical data, units shown to operators, alarm/hazard logic, overflow, corrupted-length handling, authorization, signing/checksum coverage, and data-classification impact;
- enumerate old/new endpoint pairs and determine whether dual encoding, version negotiation, translation, or coordinated cutover is used;
- update controlled requirements, schemas, compatibility matrix, training/procedures, monitoring, and data lineage;
- run boundary/invalid tests, conversion analysis, contract tests for every authorized pair, integrated alarm tests, and replay/backfill tests;
- define deployment order, observation period, rollback trigger, rollback representation, retained evidence, and retirement of the old form.

Supplier-only approval is insufficient if the interface is jointly controlled. The declared joint authority must disposition the semantic, safety, operational, compatibility, and transition impacts. If governance instead grants the supplier unilateral evolution authority, that fact and the consumer notification/qualification rules must already be part of the controlled agreement.

### Answer 5

Missing evidence includes at least: the requirement IDs tested; endpoints and measurement planes; request semantics and payload distribution; provider and consumer versions; hardware/configuration; mode and environment; load rate, concurrency, and duration; timing source and measurement uncertainty; latency/error/ordering acceptance criteria; boundary and invalid cases; faults and retries; security context; number of failures or anomalies; retained raw results; procedure/tool versions; and whether 100 successes represent all attempts or only completed requests.

A bounded replacement conclusion could read:

“For client C2.4 and service S5.1 in normal mode, using test environment E7 and procedure P-19, 100 of 100 sequential valid requests at 10 requests/s returned semantically correct responses within the required 300 ms at planes CP-1 and SP-1. Maximum observed latency was 184 ms with 2 ms measurement uncertainty; no errors or retries were observed. The retained log and configuration digest are linked to requirements API-021, API-024, and API-031.”

Then state the limit: “This result supports conformance for the tested valid sequential workload and version pair. It does not establish behavior under concurrency, maximum load, malformed or unauthorized requests, timeout/retry, degraded network, failure recovery, other versions, or production environment.” That conclusion is useful precisely because it does not claim more than the evidence supports.
