---
module_id: SYSENG-020
program: Systems Engineering
level: 1
module_number: 20
title: Managing Requirement Change and Conflict
status: complete
last_verified: 2026-08-31
---

# Managing Requirement Change and Conflict

## One-Page Review

### Governing question

How can a team change a baselined requirement—or resolve requirements that cannot all be satisfied—through an authorized, traceable, evidence-bearing decision that preserves system intent, exposes consequences, updates every affected configuration, and verifies the implemented result without pretending that a board vote or impact report eliminates uncertainty?

### Essential definitions

- A **requirement change** adds, deletes, or modifies requirement content, attributes, applicability, priority, source, acceptance criteria, or relationships after a defined reference state.
- A **baseline** is an approved, identified configuration at a point in time that provides the reference against which change is proposed and audited.
- A **change request** is a controlled decision object containing the problem or opportunity, exact proposed delta, rationale, originator, affected baseline, urgency, evidence, and requested disposition.
- **Impact analysis** identifies plausible technical, lifecycle, cost, schedule, risk, safety, security, operational, contractual, regulatory, and organizational consequences relative to named configurations.
- A **requirement conflict** exists when requirements, constraints, assumptions, interpretations, or allocations cannot jointly hold in the relevant scope, or when evidence shows their joint satisfaction is not credible.
- A **Configuration Control Board (CCB)** or equivalent change authority is the body or accountable person authorized to disposition a change within a declared jurisdiction.
- **Disposition** is the recorded decision to approve, reject, defer, request revision, or escalate a change, including rationale, authority, conditions, dissent, and effective configuration.
- **Implementation verification** checks that the approved delta was incorporated completely and only where authorized; **product verification and validation** examine the changed system against requirements and stakeholder use.
- **Requirements volatility** describes change over a defined population and interval; it is an observation requiring interpretation, not automatically evidence of poor discipline.
- **Conflict resolution** is the governed process of establishing facts and authority, generating options, evaluating consequences, negotiating where appropriate, deciding, and recording residual risk.

### Central model, mechanism, or theorem

Treat a change as a state transition over a controlled baseline, not as an edit:

$$
CR=\langle id,B_0,\Delta,R,E,I,A,D,C,B_1,V\rangle,
$$

where $B_0$ is the exact prior baseline, $\Delta$ the proposed semantic delta, $R$ rationale, $E$ supporting evidence, $I$ impact analysis, $A$ competent authority, $D$ disposition, $C$ decision conditions, $B_1$ resulting baseline, and $V$ implementation and outcome evidence.

For a conflict set $Q=\{q_1,\ldots,q_n\}$ under assumptions $H$, a solver finding

$$
H\land\bigwedge_{q\in Q}q=\bot
$$

is evidence that the encoded model is unsatisfiable. It is not proof that stakeholder intent itself is irreconcilable: the encoding, units, scope, versions, and assumptions require review.

An approved decision is ready for closure only if:

$$
Ready=Authorized\land Incorporated\land TraceUpdated\land
ImplementationChecked\land RequiredVVComplete\land ResidualRiskAccepted.
$$

### Critical invariants

- Every request names the exact source and target baseline; silent edits are prohibited.
- The proposed delta is semantic and reviewable, not merely a file diff or vague desired outcome.
- Impact analysis covers both traced candidates and deliberate searches for dependencies missing from the trace graph.
- Decision authority matches the affected technical, contractual, safety, security, regulatory, financial, interface, and operational jurisdictions.
- Approval, implementation, verification, release, and operational acceptance remain separate states.
- Conflicting obligations are never “resolved” by deleting the inconvenient one without source authority and consequence analysis.
- Facts, assumptions, preferences, constraints, priorities, and legal obligations remain distinguishable in conflict deliberation.
- All approved changes update requirements, rationale, trace, architecture, interfaces, budgets, hazards, tests, procedures, training, contracts, and variants as applicable.
- Historical baselines and decision records remain reproducible; current users receive the effective configuration.
- Emergency paths are time-bounded and followed by retrospective review, full documentation, and permanent correction or rollback.
- Metrics expose population, interval, severity, source, and outcome; raw change count is not a quality verdict.
- High-consequence decisions retain independent challenge, dissent, uncertainty, and competent acceptance of residual risk.

### Common failures

Failures include changing text before approval; submitting “improve performance” without an exact delta; analyzing only the edited requirement; using trace reachability as a complete dependency proof; allowing a board without domain authority to accept safety or contractual consequences; confusing majority preference with source authority; voting before facts and options are mature; hiding conflict through ambiguous wording; classifying a major interface change as editorial; approving without funding or owners; updating the specification but not tests or field procedures; closing when code merges rather than when authorized evidence is complete; measuring all changes equally; and treating an emergency bypass as permanent governance.

### Compact example

A hospital transport system has a response-time requirement of 60 seconds, a battery-reserve requirement of eight hours, and a rule limiting charge current in occupied wards. A proposed 30-second response target increases standby sensing and radio use. The requests conflict only under a particular duty-cycle, battery, and charging model. The team identifies the authoritative clinical need, verifies units and modes, tests alternative sensing policies, and analyzes safety, privacy, battery, thermal, network, maintenance, training, cost, and deployed variants. The authorized outcome keeps the eight-hour reserve, adopts 30 seconds only for critical wards using event-triggered sensing, adds a degraded-mode indication, and requires representative verification and clinical validation. Approval does not close the change; incorporation, trace updates, test results, deployment control, and residual-risk acceptance do.

### Connections

This module closes the Level I requirements block by combining stakeholder needs, ConOps, functional and performance requirements, decomposition, allocation, quality, and bidirectional traceability. Later modules extend change reasoning through architecture, interfaces, trade studies, decision records, configuration audits, verification, validation, safety, reliability, security, digital threads, operations, and systems-of-systems governance.

## Governing Question

Change is unavoidable because knowledge arrives over time. Stakeholders discover missing use cases; prototypes expose infeasible thresholds; suppliers revise components; laws and threats evolve; verification uncovers contradictions; operations reveal work as actually performed. The engineering problem is therefore not to prevent change. It is to prevent unexamined change, delayed recognition, incoherent baselines, and decisions whose authority or consequences cannot be reconstructed.

Conflict is similarly normal. Two credible stakeholders can optimize different outcomes; a regulation can constrain an operational goal; independently reasonable subsystem requirements can exceed a shared budget. Conflict becomes dangerous when teams hide it in vague prose, negotiate before identifying authoritative sources, or treat schedule pressure as evidence. The governing question asks how to turn disagreement and change into explicit, bounded, accountable engineering decisions.

## Why This Matters

A one-line requirement edit can alter architecture, interfaces, resource margins, supplier obligations, hazards, verification environments, training, certification evidence, fielded variants, and retirement plans. If those relations are not assessed, teams can build the newly requested behavior while invalidating the system around it. Conversely, indiscriminate control can make harmless corrections so expensive that teams route around governance and create shadow specifications.

NASA requirements-management guidance identifies control, bidirectional traceability, consistency, and lifecycle change to established baselines as connected activities. Its current configuration-management guidance describes systematic proposal, justification, evaluation, authorized incorporation, and verification of implementation. ISO/IEC/IEEE 15288:2023 provides the current system lifecycle process context. ISO/IEC/IEEE 29148:2018 remains published as of 2026-08-31, while ISO records its stage as “to be revised”; it remains useful requirements-engineering guidance but its revision status must accompany currency claims. SEBoK 2.14 treats requirements and configuration management as lifecycle disciplines rather than document administration.

Weak change control creates two opposite risks. Unauthorized changes can release an inconsistent or unsafe product. Excessive ceremony can delay urgent risk reduction, obscure small decisions, and overload the board until review becomes superficial. Proportional control—based on baseline maturity, scope, reversibility, criticality, affected authority, and deployment state—protects integrity without pretending every comma merits the same forum.

## Prerequisites and Retrieval

Before continuing, retrieve these ideas:

1. a requirement has an authoritative source, intended outcome, scope, conditions, and evidence plan;
2. ConOps, architecture, interfaces, budgets, hazards, and verification artifacts carry obligations not visible in isolated text;
3. a baseline makes versions and applicability explicit, and historical evidence applies only to compatible configurations;
4. traceability provides candidate dependency paths but can be incomplete or semantically wrong;
5. decomposition and allocation create many-to-many contributions, so child changes can affect parent closure and sibling margins;
6. verification establishes conformance to requirements, while validation examines fitness for intended use;
7. a decision requires competent authority, not merely technical attractiveness or consensus;
8. executable analysis is bounded by its model, inputs, assumptions, and uncertainty.

As a retrieval test, imagine that a test failure is “fixed” by widening the requirement tolerance until the result passes. Ask whether the original need still holds, whether the failure reflects product behavior or an invalid criterion, who may change the baseline, which downstream and upstream artifacts are affected, and what new verification and validation are required. If those questions are unanswered, the edit is not controlled resolution.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish clarification, correction, enhancement, defect response, waiver, deviation, and baseline change;
2. construct a complete change request with exact versions, semantic delta, evidence, urgency, and requested disposition;
3. perform bounded multidomain impact analysis using trace traversal plus independent dependency search;
4. identify syntactic, semantic, quantitative, authority, resource, interface, temporal, and policy conflicts;
5. separate facts, assumptions, preferences, constraints, risks, and decision authority during conflict resolution;
6. generate and compare resolution options without hiding losses or non-negotiable obligations;
7. design proportional change authority, escalation, quorum, dissent, and conflict-of-interest controls;
8. preserve baseline history, communicate effective changes, and control supplier and deployed variants;
9. verify implementation and re-establish required verification, validation, assurance, and residual-risk evidence;
10. interpret volatility and change-flow metrics without rewarding suppression or encouraging low-value churn.

## Core Exposition

**Define what constitutes change.** A requirement changes when its normative meaning, source, scope, applicability, condition, threshold, unit, tolerance, priority, rationale, allocation, interface, verification method, or acceptance authority changes. Correcting spelling without semantic effect may use lighter control, but a word such as “continuous,” a unit, inequality, or exception can change behavior radically. Classify by semantic consequence after inspection, not by character count.

**Distinguish request types.** A clarification seeks a shared interpretation without changing the approved obligation. A correction repairs an error against existing authoritative intent. An enhancement introduces additional value or scope. A defect response changes product or requirement after evidence exposes a mismatch. A deviation authorizes departure before an event or delivery under stated conditions; a waiver accepts a known nonconformance according to governing terminology. Organizations vary in these labels, so define them locally and preserve the actual authority and effect.

**Identify the controlled baseline.** A request names the exact requirement version and every affected product or interface baseline. “Current” is not durable identification. Record product, release, market, site, supplier, mode, and operational applicability. If the organization cannot reproduce the before state, reviewers cannot determine what is changing, evidence cannot be scoped reliably, and rollback becomes guesswork.

**Write the semantic delta.** Show old and proposed requirement text, changed attributes and relations, and a plain-language account of altered permitted and prohibited behavior. State what does not change. Include effective date, transition behavior, backward compatibility, data migration, and retirement of obsolete interpretations. A textual diff is evidence of characters; the semantic delta explains system consequences.

**Capture origin and rationale.** Identify who observed the problem, the stakeholder or obligation represented, the event or evidence that triggered the request, and why action is needed now. Link incident, test result, regulation, vulnerability, trade study, operational observation, or stakeholder decision. Separate the originator from the authority that owns the source need; an influential requester does not automatically have power to redefine it.

**Screen before deep analysis.** Check completeness, duplicate requests, affected baseline, urgency, apparent jurisdiction, security classification, and whether the issue is actually a requirement change. Return incomplete requests with precise missing information. Screening is not disposition: a screener should not quietly reject a credible safety issue because the form is imperfect.

**Triage proportionally.** Classify consequence, reach, reversibility, urgency, maturity, and deployment state. A reversible pre-baseline model experiment differs from a change to a fielded medical alarm. Establish control levels and escalation triggers in advance. Low-impact decisions may have delegated authority; cross-interface, high-cost, irreversible, regulatory, safety, security, or fielded-product effects require broader competence and authority.

**Establish the change hypothesis.** Express the claim: “Changing X from state $x_0$ to $x_1$ will address evidence P while preserving obligations O under assumptions H.” This forces reviewers to ask what evidence would refute the claim, which constraints remain fixed, and which outcomes must be re-established. Without a hypothesis, analysis becomes a catalog rather than a decision argument.

**Traverse trace relationships.** Starting from the changed node/version, traverse upstream sources and downstream decomposition, allocation, architecture, implementation, verification, validation, and operational artifacts. Traverse horizontal interfaces, budgets, hazards, threats, suppliers, variants, anomalies, waivers, procedures, and training. Filter by edge type and configuration, then inspect relation rationale. The resulting set is a candidate frontier, never an exhaustive proof.

**Search outside recorded trace.** Interview artifact owners; inspect interface registries, bills of material, deployment inventories, shared services, telemetry, incident records, contracts, regulatory commitments, resource models, and organizational procedures. Use domain checklists and adversarial review to find missing edges. Add newly discovered dependencies to trace so analysis improves the system of record rather than remaining a one-off spreadsheet.

**Analyze multiple consequence domains.** At minimum ask about stakeholder value, functions, performance, architecture, interfaces, data, modes, timing, resource budgets, reliability, maintainability, safety, security, privacy, human factors, environment, manufacture, supply, integration, verification, validation, operations, training, support, disposal, cost, schedule, contract, regulation, and existing evidence. Mark each as affected, unaffected with rationale, unknown, or not applicable. “No impact” is a claim requiring basis.

**Quantify without manufacturing certainty.** Recompute budgets and margins under named assumptions. Use ranges or distributions when inputs are uncertain. Separate estimate uncertainty from decision thresholds. If a schedule estimate is $12\pm4$ weeks, do not turn it into a precise 12-week promise. Sensitivity analysis shows which assumptions could reverse the recommendation.

**Detect conflict precisely.** Lexical conflicts use inconsistent terms. Structural conflicts assign incompatible responsibility or scope. Quantitative conflicts exceed a shared mass, power, latency, capacity, reliability, or cost bound. Behavioral conflicts require mutually exclusive actions under the same condition. Temporal conflicts impose impossible ordering or deadlines. Interface conflicts disagree about units, protocols, ownership, or failure semantics. Authority conflicts arise when sources impose incompatible obligations. Evidence conflicts occur when models, tests, or observations disagree.

**Normalize before negotiating.** Put requirements into comparable form: actor, action, object, conditions, mode, threshold, tolerance, unit, temporal qualifier, scope, source, priority, and verification concept. Align versions and configurations. Many apparent conflicts disappear when one statement applies only to maintenance mode, uses milliseconds rather than seconds, or describes a goal rather than a binding constraint. This is clarification, not compromise.

**Build a conflict set.** Create the smallest set of requirements and assumptions that appears jointly infeasible. Include interface and resource constraints that make the contradiction real. A minimal conflict set focuses resolution and prevents unrelated requirements from being weakened. If formal modeling is used, the unsatisfiable core belongs to the encoding; engineers still validate that the model represents the real obligation.

**Establish source authority and negotiability.** Identify laws, contracts, stakeholder needs, safety constraints, architecture decisions, local preferences, and assumptions. Some obligations can only be changed by an external authority; others are design choices masquerading as requirements. Priority is multidimensional: legal precedence, safety consequence, mission criticality, stakeholder value, reversibility, and lifecycle cost cannot always collapse into one score.

**Generate options before choosing.** Options may clarify scope; partition modes or populations; change architecture; reallocate a budget; relax a threshold with evidence; strengthen another control; sequence delivery; introduce a variant; seek source-authority change; accept a bounded deviation; or reject the request. Always include the unchanged baseline when feasible. Record what each option preserves, sacrifices, transfers, and leaves uncertain.

**Use decision methods as aids.** Trade studies, constraint solvers, simulations, prototypes, fault analysis, cost models, and multicriteria matrices structure evidence. Their weights and utilities encode judgments. A high aggregate score cannot override a hard legal or safety constraint, and a feasible solver output may omit human or operational realities. Keep raw evidence, assumptions, sensitivity, and dissent visible beside the recommendation.

**Design competent authority.** The decision forum needs jurisdiction and relevant representation: requirement/source owner, systems engineering, architecture, affected subsystems, interface partners, configuration management, verification, operations, program controls, suppliers, and assurance disciplines as consequences require. Define quorum, voting or accountable decision rule, recusal, escalation, emergency authority, and appeal. Attendance is not authority; consensus is not always required; dissent is evidence to retain.

**Make disposition explicit.** Approve, reject, defer, request revision, or escalate. Record rationale, evidence considered, rejected options, conditions, funding, owners, due dates, effective configurations, required re-verification/re-validation, communications, residual risks, minority opinions, and expiration of temporary relief. “Approved in principle” is unsafe unless its operational meaning is defined.

**Separate approval from implementation.** Approval authorizes a bounded delta; it does not show that artifacts changed correctly. Create coordinated actions for requirements, models, interfaces, budgets, design, code/hardware, supplier documents, tests, safety/security analyses, operations, training, contracts, and deployment. Prevent partial release when dependent actions remain open unless explicitly accepted and controlled.

**Verify change incorporation.** Compare the resulting baseline against the approved change package. Confirm every authorized edit and relation is present, no unauthorized scope entered, identifiers and history remain intact, generated views match the source, and affected parties received the effective configuration. Configuration audit answers “did we build and document the authorized change?”

**Re-establish product evidence.** Determine which previous verification and validation evidence remains applicable. Run affected tests and analyses on the correct configuration, include regression and interaction evidence, resolve anomalies, and obtain required independent assurance. Validation asks whether the changed system still serves intended users in representative contexts. A passing unit test cannot close a changed clinical or operational outcome.

**Release and monitor deliberately.** Identify deployment rings, rollback criteria, migration, feature-state control, operator notices, training, support, telemetry, and observation interval. Monitor both intended improvement and unintended effects. Operational evidence may reveal a new change request; this is learning, not proof that change control failed.

**Handle emergency change.** Define who may act, which evidence is minimally required, how scope is constrained, how configuration is captured, and when retrospective review occurs. Preserve a rollback path where possible. Emergency authority should expire automatically. The post-action board confirms, modifies, or reverses the change and completes missing impact, trace, verification, communication, and risk work.

**Control supplier and interface change.** Contracts and interface agreements define notification, data, approval, lead time, compatibility, and evidence duties. A supplier may change an internal part that preserves nominal form and function yet alters reliability, cybersecurity, material compliance, or maintenance. System authority evaluates system impact; supplier certification is input, not automatic acceptance.

**Manage fielded variants.** Identify every serial number, site, release, option, region, and data schema affected. Avoid marking a request closed because the development baseline changed while deployed assets remain mixed. Maintain as-designed, as-built, as-tested, as-deployed, and as-maintained applicability where required. Evidence from one variant transfers only through an explicit equivalence argument.

**Measure change flow responsibly.** Possible measures include requests by source/severity, age by state, analysis rework, decision latency, implementation lead time, escaped unauthorized change, reopened decisions, post-change defects, impact-prediction precision, and trace debt discovered. Define $N_B$, the number of requirements in the reference baseline, and $A+M+D$, accepted additions, modifications, and deletions over interval $T$:

$$
Volatility_T=\frac{A_T+M_T+D_T}{N_B}.
$$

This rate depends on counting rules, baseline, and interval. High early volatility may reflect productive discovery; suspiciously low volatility may reflect suppression or unrecorded edits. Never target a raw rate without understanding behavior it incentivizes.

**Audit the process and the decisions.** Sample whether changes have exact baselines, credible impacts, proper authority, complete incorporation, current trace, valid evidence, and closure conditions. Seed workflow tests for unauthorized decisions, missing jurisdiction, stale evidence, concurrent edits, emergency expiry, and incomplete deployment. Process conformance does not establish that the engineering decision was correct; substantive review remains necessary.

**Use automation as bounded evidence.** Workflow tools can enforce required fields, immutable history, role authorization, state transitions, links, notifications, and reports. Graph queries can propose affected artifacts; solvers can expose encoded conflicts; continuous checks can detect stale tests. None can certify completeness of dependencies, legitimacy of stakeholder authority, or adequacy of residual risk without human and domain evidence.

The following checker evaluates declared closure fields for five example change requests. It does not inspect the engineering content behind those fields.

<!-- bijux-verify: {"id":"change-closure-record-check","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"requests_total=5\nclosed_declared=1\nmissing_authority=CR-002\nmissing_impact=CR-003\nmissing_incorporation=CR-004\nmissing_vv=CR-005\nopen_or_incomplete=CR-002,CR-003,CR-004,CR-005\nevidence=declared_fields_only\n","stderr":""}} -->
```python
requests = [
    {"id": "CR-001", "disposition": "approved", "authority": "system-ccb",
     "impact": ["interfaces", "operations"], "incorporated": True, "vv": ["VR-91"]},
    {"id": "CR-002", "disposition": "approved", "authority": "",
     "impact": ["security"], "incorporated": True, "vv": ["VR-92"]},
    {"id": "CR-003", "disposition": "approved", "authority": "program-ccb",
     "impact": [], "incorporated": True, "vv": ["VR-93"]},
    {"id": "CR-004", "disposition": "approved", "authority": "interface-board",
     "impact": ["interface"], "incorporated": False, "vv": ["VR-94"]},
    {"id": "CR-005", "disposition": "approved", "authority": "safety-board",
     "impact": ["hazard", "training"], "incorporated": True, "vv": []},
]

closed = [
    item for item in requests
    if item["disposition"] == "approved"
    and item["authority"] and item["impact"]
    and item["incorporated"] and item["vv"]
]
print(f"requests_total={len(requests)}")
print(f"closed_declared={len(closed)}")
for field in ("authority", "impact"):
    print(f"missing_{field}=" + ",".join(item["id"] for item in requests if not item[field]))
print("missing_incorporation=" + ",".join(item["id"] for item in requests if not item["incorporated"]))
print("missing_vv=" + ",".join(item["id"] for item in requests if not item["vv"]))
print("open_or_incomplete=" + ",".join(item["id"] for item in requests if item not in closed))
print("evidence=declared_fields_only")
```

The output establishes only that one in-memory record declares all selected fields. It does not establish that the authority is competent, the impact list complete, incorporation correct, verification valid, validation sufficient, or release safe.

## Definitions and Notation

Let $B_0$ and $B_1$ denote immutable references to the before and after baselines. Let $\Delta(B_0,B_1)$ be the authorized semantic difference, not merely textual difference. Let $G_{B_0}=(V,E)$ be the trace/dependency graph for the prior configuration. For changed artifact set $S$, define:

$$
Candidates(S)=Reach_{G_{B_0}}(S,E_{relevant})\cup D_{external},
$$

where $D_{external}$ records candidates discovered through expert, interface, operational, supplier, contract, and runtime searches outside the graph.

For option $o$, let $Feasible(o,H,C)$ mean it satisfies encoded hard constraints $C$ under assumptions $H$. Let $Evidence(o)$ record analysis, test, observation, uncertainty, and applicability. Let $Authority(o)$ identify the source owners and decision jurisdictions required. Feasibility alone is insufficient:

$$
Acceptable(o)\Rightarrow Feasible(o,H,C)\land AdequateEvidence(o)
\land CompetentAuthority(o)\land ResidualRiskAccepted(o).
$$

For conflict set $Q$, a minimal unsatisfiable subset $U\subseteq Q$ satisfies $H\land\bigwedge U=\bot$ while removal of any encoded member restores satisfiability. “Minimal” concerns that model, not necessarily the smallest or only real-world conflict. Let $RACI$ or another assignment model describe participation, but never infer legal or technical authority solely from a matrix cell.

States should distinguish at least `submitted`, `screened`, `analyzing`, `awaiting-authority`, `approved`, `rejected`, `deferred`, `implementing`, `implemented`, `verifying`, `released`, and `closed`. Local workflows may differ, but merging approval, implementation, and closure erases essential evidence boundaries.

## Mechanisms, Invariants, or Proof Structure

The mechanism is a closed control loop:

1. **Observe and identify:** capture the trigger, exact controlled baseline, source authority, semantic delta, urgency, and initial evidence.
2. **Screen and classify:** verify request quality, route by scope and consequence, identify required jurisdictions, and preserve urgent reports.
3. **Analyze:** traverse trace, search beyond it, model conflicts, quantify impacts and uncertainty, generate alternatives, and expose evidence gaps.
4. **Decide:** convene competent authority, challenge assumptions, record disposition, rationale, conditions, dissent, funding, and residual risk.
5. **Incorporate:** update every affected controlled artifact and relationship without unauthorized scope, maintaining history and applicability.
6. **Verify and validate:** audit incorporation, rerun affected product evidence, examine representative use, and resolve anomalies.
7. **Release and monitor:** communicate effective configurations, deploy controllably, observe intended and unintended outcomes, and close only when criteria hold.

The argument is conditional rather than a proof of universal correctness. If identity, trace, analysis, authority, implementation, evidence, and communication invariants hold, the organization has a reviewable basis for the transition from $B_0$ to $B_1$. It can reproduce what changed, why, who authorized it, what was checked, and which uncertainty remains. The mechanism cannot guarantee that all dependencies were discovered, every model is faithful, or an unforeseen operational interaction will not occur. Independent challenge, monitoring, and reopening remain part of control.

Concurrency requires special care. Two individually approved requests against $B_0$ may interact when combined. Before incorporation, rebase each semantic delta against the actual target baseline, rerun impacted analyses, and identify noncommutative effects:

$$
Apply(\Delta_2,Apply(\Delta_1,B_0))\neq
Apply(\Delta_1,Apply(\Delta_2,B_0)).
$$

A version-control merge without textual conflict does not show semantic compatibility. Release trains and cumulative change packages need integrated verification and an authority responsible for their combined effect.

## Alternatives and Trade-Offs

**Informal owner approval** is fast for pre-baseline, local, reversible work. It fails when crosscutting impacts or external authority are present. **Tiered control** delegates low-risk changes and escalates by triggers; it balances speed and integrity but depends on correct classification and audit.

**Periodic CCB meetings** support shared deliberation and broad visibility but can create queues and rushed agendas. **Asynchronous evidence review with accountable decision** reduces latency and improves written reasoning, but nuanced conflict may need synchronous discussion. A hybrid reserves meetings for contested or high-consequence decisions.

**Consensus** can expose concerns and improve commitment, yet may let one party block a necessary decision or blur who is accountable. **Majority vote** is clear but can outvote source owners or assurance obligations. **Accountable authority after consultation** preserves decision responsibility; escalation and dissent records guard against unilateral blindness.

**Document-centric baselines** are accessible and may fit contracts, but relationships and variants become difficult to query. **Model/database-centric control** enables semantic diffs, trace traversal, and automation, but schema, access, tool qualification, export, and long-term preservation become assurance concerns. Governed documents can remain approved views of an authoritative model if reproducibility is demonstrated.

**Numeric ranking** helps compare options across criteria and run sensitivity analysis. It can conceal noncompensatory constraints and political weights. **Constraint-first elimination plus transparent trade study** keeps mandatory obligations separate from preferences, though judgments still require authority.

**Feature flags and reversible rollout** reduce exposure and provide operational evidence for software-intensive changes. They add configuration states, testing combinations, security paths, and retirement debt. Hardware, contractual, physiological, and legal changes may not be cheaply reversible.

**Change freezes** stabilize integration and release evidence. They can delay urgent corrections and shift work into undocumented channels. Define exceptions, authority, duration, and exit criteria. A freeze protects a baseline; it is not denial that the world changes.

## Failure Modes and Misconceptions

- **“The requirement owner approved it, so impact is covered.”** Ownership supplies authority over one artifact, not every interface, hazard, contract, or deployed system affected.
- **“The diff is small.”** Character count does not measure semantic reach; changing `<` to `≤`, milliseconds to seconds, or “may” to “shall” can be major.
- **“The graph found no downstream nodes.”** That may reveal no impact, missing trace, wrong edge filters, or wrong configuration. Search outside the graph.
- **“The solver proved the requirements conflict.”** It showed the encoded assertions under stated assumptions are unsatisfiable. Validate the model and interpretations.
- **“Stakeholders compromised, so the conflict is resolved.”** Stakeholders cannot bargain away law, contract, physics, or unrepresented affected parties.
- **“We voted.”** A vote does not supply missing evidence, jurisdiction, funding, or acceptance of residual risk.
- **“Approval means done.”** Approval begins controlled incorporation; closure requires implementation, evidence, communication, and applicable release/monitoring.
- **“Regression passed.”** Passing selected tests does not establish unchanged stakeholder outcomes, safety, security, privacy, or field compatibility.
- **“Zero volatility is quality.”** It can mean stable understanding, frozen reporting, or uncontrolled edits. Interpret causes and outcomes.
- **“Emergency means no records.”** Urgency changes timing and minimum evidence, not the need for identity, authority, scope, rollback, and retrospective accountability.
- **“Supplier says form-fit-function is unchanged.”** Materials, firmware, vulnerabilities, reliability, provenance, or manufacturing process may still alter system risk.
- **“A temporary waiver changes the requirement.”** It records bounded acceptance of nonconformance; it does not silently rewrite the approved obligation.

## Worked Examples

### Example 1

**Correcting a unit error.** A pump requirement states 3 L/s, while the source clinical analysis and every allocation use 3 L/min. Assumptions: source analysis is authoritative and the delivered design targets 3 L/min. Reasoning: the one-character correction is semantically large; trace shows alarms, calibration, labels, and tests. The CCB treats it as a baseline correction, verifies no product was built to L/s, updates all artifacts, and repeats affected reviews. Evidence limit: consistent documents do not prove every field label or deployed configuration was found. Conclusion: approve only with inventory and incorporation audit.

### Example 2

**Latency versus battery conflict.** A wildlife collar must transmit location within 10 seconds and operate 18 months on one cell. Measured radio duty cycle makes both impossible under the stated coverage assumption. The team verifies battery and network models, creates event-driven and store-and-forward options, and consults the conservation need owner. Evidence limit: trials cover two seasons, not all terrain. The authority changes the latency requirement to 10 seconds for distress events and 15 minutes otherwise, preserving an explicit outage mode and field-validation plan.

### Example 3

**Interface change across organizations.** A rail operator proposes changing a braking message timestamp from UTC milliseconds to TAI nanoseconds. Trace identifies onboard software, wayside analytics, replay tools, contracts, time synchronization, storage, training, and mixed fleets. A textual schema adapter is insufficient because leap-second semantics and old logs differ. Joint interface authority approves a versioned dual-read transition, forbids ambiguous auto-detection, and requires replay and failover evidence. Conclusion is limited to named fleets and schema versions.

### Example 4

**Safety request from failed verification.** A thermal cutoff misses a fault condition. One proposal widens the requirement so the test passes; another changes sensing architecture. The team returns to the hazard and source safety constraint, confirms the test represents a credible condition, and rejects criterion weakening. Independent safety authority approves redundant sensing with diagnostic coverage and new fault-injection evidence. Passing that campaign supports the specified faults, not universal safety.

### Example 5

**Regulatory conflict with product preference.** A team wants indefinite diagnostic retention for machine-learning improvement, while an applicable privacy obligation requires bounded retention. The product goal is negotiable; the legal obligation is not within the CCB’s power to waive. Options minimize data, separate consented research, aggregate signals, and impose deletion verification. Legal/privacy authority confirms interpretation. The approved requirement records region and data-class applicability; it does not claim one policy fits every jurisdiction.

### Example 6

**Supplier substitution.** A supplier replaces a capacitor with identical nominal ratings. Impact analysis finds different temperature derating, material declaration, failure distribution, and source lead time. Assumptions: the supplier report is authentic but system operating transients exceed its test profile. The change remains pending until system-level stress analysis, sample testing, safety review, and as-built trace are complete. Supplier equivalence is evidence, not system acceptance.

### Example 7

**Concurrent individually safe changes.** One request raises processor frequency to meet latency; another reduces fan speed for noise. Each passes isolated analysis against the old baseline, but together exceed thermal margin. The release authority rebases both onto the candidate integrated baseline, recomputes power and temperature, and selects conditional fan control. Evidence limit: chamber tests cover specified ambient bounds. Conclusion: neither independent approval transfers automatically to the combined package.

### Example 8

**Emergency cybersecurity change.** Active exploitation requires disabling a remote maintenance protocol in fielded controllers. Emergency authority names affected versions, documents operational loss, stages rollout, retains rollback, and adds temporary manual maintenance. Within 48 hours the full board reviews interfaces, safety, supplier contracts, training, and restoration options. Monitoring shows no control instability. The outcome supports continuation of the mitigation during the observation interval; it does not prove absence of alternate attack paths.

### Example 9

**Volatility metric misuse.** Team A records 40 evaluated requests against 800 requirements; Team B reports two requests but engineers edit a shared spreadsheet directly. Their nominal volatility rates are 5% and 0.25%. Audit discovers 63 untracked semantic differences in Team B’s released baseline. Assumptions and counting rules differ, so ranking quality by the reported rate is invalid. The bounded conclusion is that workflow integrity and outcomes must accompany volatility.

### Example 10

**Autonomous vehicle conflict with dissent.** A shuttle operator wants faster door closure to improve throughput; accessibility users require sufficient boarding time and safety analysis limits closing force. Options include sensor-based extension, schedule changes, and mode-specific timing. Tests expose edge cases for mobility devices, and a user representative dissents from the initial sample. The board defers rather than outvotes the concern, expands representative validation, and later approves adaptive timing with monitoring. Approval is bounded to the tested vehicle, sensor, route, and user conditions; residual uncertainty and dissent disposition remain recorded.

## Cross-Program Connections

- **Platform Engineering:** change control maps to service ownership, dependency catalogs, progressive delivery, policy as code, and rollback, while platform teams must avoid turning ticket approval into system assurance.
- **API and Service Engineering:** interface conflicts appear as schema, semantics, versioning, compatibility, service-level objective, and deprecation decisions across independently governed consumers.
- **Data Engineering:** requirement changes affect schemas, lineage, quality contracts, retention, backfills, reproducibility, access policy, and historical interpretation.
- **Object-Oriented Programming:** behavioral subtyping and contracts reveal when a “small” class change violates client expectations beyond compilation boundaries.
- **Functional Programming:** immutable data and explicit state transitions make baseline history and decision workflows easier to reason about; effect boundaries expose external consequences.
- **Safety, security, and governance:** hazard, threat, privacy, clinical, legal, and contractual authorities constrain what a technical change board may decide.

## References

1. ISO, “ISO/IEC/IEEE 29148:2018 — Systems and software engineering — Life cycle processes — Requirements engineering,” published 2018-11; ISO listed the published standard as “to be revised” on 2026-02-16. https://www.iso.org/standard/72089.html
2. ISO, “ISO/IEC/IEEE 15288:2023 — Systems and software engineering — System life cycle processes,” second edition, published 2023-05. https://www.iso.org/standard/81702.html
3. NASA, “6.2 Requirements Management,” NASA Systems Engineering Handbook, especially sections 6.2.1.2.2–6.2.1.2.5. https://www.nasa.gov/reference/6-2-requirements-management/
4. NASA, “6.5 Configuration Management,” NASA Systems Engineering Handbook, especially baselines and configuration change control. https://www.nasa.gov/reference/6-5-configuration-management/
5. NASA Software Engineering Handbook, “SWE-053 — Manage Requirements Changes.” https://swehb.nasa.gov/spaces/7150/pages/16449679/SWE-053+-+Manage+Requirements+Changes
6. NASA Software Engineering Handbook, “SWE-080 — Track and Evaluate Changes.” https://swehb.nasa.gov/spaces/SWEHBVB/pages/32604559/SWE-080+-+Track+and+Evaluate+Changes
7. NASA Software Engineering Handbook, “SWE-082 — Authorizing Changes.” https://swehb.nasa.gov/spaces/7150/pages/16450445/SWE-082+-+Authorizing+Changes
8. NASA, “NPR 7123.1C — NASA Systems Engineering Processes and Requirements,” change 2. https://nodis3.gsfc.nasa.gov/displayAll.cfm?Internal_ID=N_PR_7123_001C_&page_name=all
9. SEBoK Editorial Board, “Requirements Management,” *Guide to the Systems Engineering Body of Knowledge*, version 2.14, released 2026-05-18. https://sebokwiki.org/wiki/Requirements_Management
10. SEBoK Editorial Board, “Configuration Management,” *Guide to the Systems Engineering Body of Knowledge*, version 2.14, released 2026-05-18. https://sebokwiki.org/wiki/Configuration_Management

## Exercises

### Exercise 1

A change request says only, “Increase telemetry quality for the next release.” Rewrite it into a reviewable request structure. State what remains unknown and which information is required before impact analysis or authorization.

### Exercise 2

A drone must return within 120 seconds after link loss, remain below a regulated altitude, retain 25% landing energy reserve, and avoid a newly mapped exclusion zone. A proposed route satisfies any three but not all four under the current wind model. Diagnose the conflict and design a resolution process without selecting a requirement by simple vote.

### Exercise 3

Two approved changes target the same release: CR-A encrypts all sensor traffic and adds 18 ms latency; CR-B reduces the end-to-end deadline from 100 ms to 85 ms. The old measured worst case was 70 ms with 8 ms uncertainty. Analyze the combined package and state a bounded decision.

### Exercise 4

Design a tiered change-control workflow for a small team that operates a fielded public-safety service. Include delegated changes, escalation triggers, emergency authority, evidence states, and closure criteria without requiring the full board for every edit.

### Exercise 5

A clinical decision-support system proposes changing an allergy-alert requirement because users override 70% of alerts. Construct an impact and conflict-resolution plan that does not infer from the override rate alone that alerts are unnecessary.

## Answers to the Exercises

### Answer 1

A reviewable request identifies an immutable request ID; originator and represented stakeholder; exact prior requirement and product baselines; current telemetry definition and measured problem; old and proposed quality semantics including variables, units, conditions, modes, thresholds, tolerances, missing-data behavior, and acceptance criteria; affected products, sites, releases, and interfaces; trigger evidence; rationale and urgency; candidate options including no change; preliminary hazards, security/privacy, bandwidth, power, storage, cost, schedule, supplier, operations, and verification impacts; requested authority and disposition; transition and rollback; and required evidence.

Unknowns include whether “quality” means accuracy, precision, latency, completeness, provenance, sampling rate, or availability; which consumers and decisions depend on telemetry; whether a contractual or safety source governs it; and whether the next release is one configuration or many. Screening should return the request for those facts rather than allow analysts to invent intent. A richer request enables impact analysis but does not establish that the proposed threshold is valuable or feasible.

### Answer 2

Normalize the requirements by mode, location, wind assumption, starting energy, altitude reference, response-time clock, and exclusion-zone authority. Build the smallest conflict set and reproduce infeasibility with route/energy analysis; challenge map currency, forecast uncertainty, navigation performance, and whether 120 seconds describes all loss events. Classify the regulated altitude and exclusion-zone authority rather than treating all four requirements as preferences. Trace the return behavior to safety hazards, operator needs, airspace obligations, energy allocation, communications, geofence data, verification, and field procedures.

Generate options: earlier preventive return, alternate safe landing sites, expanded reserve, slower route within a justified response change, improved wind estimation, or operational restriction under adverse wind. Compare feasibility and residual risk under sensitivity ranges. Aviation/regulatory, safety, operations, requirement-source, and system authorities must disposition affected obligations; a majority cannot waive external rules. The result remains conditional until representative simulation/flight evidence, map-update control, deployment applicability, and residual-risk acceptance are complete.

### Answer 3

Against the old baseline, CR-A produces an estimated worst case of $70+18=88$ ms before uncertainty, while CR-B permits 85 ms. Including the stated 8 ms uncertainty yields a conservative 96 ms observation bound under the same interpretation, so the combined package lacks evidence for the new deadline. Textual merging and independent approvals do not resolve the interaction.

Rebase both changes onto one candidate configuration; confirm whether encryption latency overlaps or adds, whether 70 ms and 8 ms remain applicable, and which modes, payloads, keys, hardware, failures, and loads define worst case. Options include acceleration, hardware support, selective architecture consistent with security sources, retaining 100 ms, or deferring one change. Security authority must judge any reduced protection, and requirement authority must judge deadline changes. A bounded decision is to withhold combined release unless testing/analysis demonstrates the 85 ms criterion with required margin on named configurations or competent authorities approve a different option and its consequences.

### Answer 4

Define three control levels. Delegated owners may approve nonsemantic editorial corrections and reversible pre-release implementation choices within allocated requirements, provided immutable history and automated checks exist. A product change authority handles semantic changes with local cost/schedule effects. The full multidisciplinary authority handles field behavior, public-safety functions, interfaces, data policy, supplier commitments, high cost, irreversibility, unresolved dissent, or cross-team impact. Automatic escalation triggers include safety/security/privacy implications, external obligations, deployed configurations, failed verification, budget-margin breach, uncertain jurisdiction, and interacting changes.

Workflow states separate submission, screening, analysis, authorization, incorporation, verification, release, monitoring, and closure. Emergency authority can enact the minimum bounded mitigation, must record scope and baseline, preserve rollback, notify stakeholders, expire automatically, and receive retrospective review by a fixed deadline. Closure requires authorized incorporation, updated trace/baselines, required regression and outcome evidence, controlled deployment, communication, anomaly disposition, and accepted residual risk. Periodic audits sample delegated decisions and detect semantic changes misclassified as editorial.

### Answer 5

First disaggregate the 70% override rate by alert type, severity, patient population, context, clinician role, site, outcome, and reason. Overrides can indicate poor specificity, workflow mismatch, stale data, legitimate clinical judgment, or unsafe normalization of nuisance alerts. Establish source authority: patient-safety goals, clinical policy, applicable regulation, drug/allergy knowledge, and user needs. Trace the requirement through data provenance, matching logic, severity rules, user interface, timing, audit, downstream prescribing, training, and monitoring.

Analyze false positives, false negatives, near misses, adverse events, response time, alert fatigue, equity, privacy, and downtime. Generate options such as severity tiers, context-sensitive suppression with auditable rationale, improved data quality, deduplication, redesigned presentation, and post-override monitoring. Use representative clinicians and patient-safety/pharmacy experts; preserve dissent and conflicts of interest. Clinical, safety, privacy, regulatory, and product authorities disposition within their jurisdictions. Prospective validation and monitored rollout must measure both burden and missed-harm indicators. The override statistic motivates investigation; by itself it proves neither ineffectiveness nor safety of weakening the requirement.
