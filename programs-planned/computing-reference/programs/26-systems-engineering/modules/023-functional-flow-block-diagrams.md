---
module_id: SYSENG-023
program: Systems Engineering
level: 1
module_number: 23
title: Functional Flow Block Diagrams
status: complete
last_verified: 2026-08-31
---

# Functional Flow Block Diagrams

## One-Page Review

### Governing question

How can a team use Functional Flow Block Diagrams to express the sequence, selection, concurrency, iteration, references, and completion logic of system functions across scenarios—without mistaking graphical order for measured timing, confusing control flow with exchanged data, or claiming behavioral completeness from a readable diagram?

### Essential definitions

- A **Functional Flow Block Diagram (FFBD)** is a behavioral view that represents system functions and the logical/time sequence of functional events.
- An **Enhanced FFBD (EFFBD/eFFBD)** adds constructs for information/data and control flows, resources, timing, or executable semantics according to the chosen method/tool.
- A **function block** names a purposeful transformation with a stable identifier; its detailed input/output contract remains governed outside or behind the view.
- A **functional flow** states an execution dependency or permitted progression, not necessarily transfer of a material or data item.
- A **sequence** requires one function or construct to satisfy its completion condition before the next is enabled.
- An **AND split/join** activates concurrent branches and defines their synchronization/completion rule; “parallel” need not mean simultaneous processor execution.
- An **OR/XOR selection** activates one or more eligible branches according to explicit guard and exclusivity semantics.
- An **iteration/loop** repeats a function or subflow over a domain or until a completion/exit condition, with bounded progress and failure behavior.
- A **reference block** connects the view to another controlled diagram or function detail without duplicating it.
- A **scenario path** is one admissible traversal through the FFBD under named initial state, mode, guards, events, and configuration.
- A **deadlock** is a reachable state in which required progress is impossible; **livelock** permits continuing activity without required outcome.
- **Reachability** means a node/path can be reached in the encoded graph or execution semantics; it does not establish feasibility, correctness, or safety in the realized system.

### Central model, mechanism, or theorem

Model an FFBD as:

$$
M=\langle F,N,E,G,J,L,R,\sigma_0,\Omega\rangle,
$$

where $F$ are function blocks, $N$ control constructs, $E$ directed execution relations, $G$ guards, $J$ join/completion rules, $L$ loops, $R$ references, $\sigma_0$ initial execution state, and $\Omega$ required outcomes.

A valid scenario path requires more than graph adjacency:

$$
Valid(p,s,m,c)\Rightarrow Reachable(p)\land Guards(p,s,m,c)
\land JoinRules(p)\land LoopBounds(p)\land InterfaceContracts(p),
$$

for state $s$, mode $m$, and configuration $c$.

Under explicitly sequential, non-overlapping execution, path latency may be bounded by:

$$
T_p=\sum_{f\in p}T_f+\sum_{e\in p}T_e+T_{queue}+T_{sync}.
$$

Other concurrency, retry, scheduling, and physical dynamics need their own composition model.

### Critical invariants

- Each diagram names system boundary, parent function, decomposition level, scenario/mode, configuration, notation profile, version, and owner.
- Every function block has a stable action-object identity and trace to its governed contract and source rationale.
- Arrows distinguish execution/control dependency from data, matter, energy, resource, or interface exchange.
- AND, inclusive OR, exclusive choice, merge, join, iteration, replication, and conditional exit use defined and paired semantics.
- Guards are mutually understood, complete for the claimed case set, testable where possible, and owned by an authority/source.
- Concurrent branches state activation, independence/shared resources, synchronization, cancellation, timeout, and partial-failure behavior.
- Loops state entry, domain, progress measure, completion, maximum/timeout, state accumulation, and failure/escape disposition.
- References resolve to immutable compatible versions and do not hide circular or missing behavior.
- Parent boundary inputs, outputs, pre/postconditions, modes, performance, and failure obligations remain preserved by scenario paths.
- Nominal, alternate, degraded, emergency, startup, shutdown, maintenance, update, recovery, and retirement paths are included according to declared scope.
- Static graph checks, animation, simulation, or model execution remain bounded by encoded semantics and inputs.
- Diagrams are reviewed with state, interface, timing, resource, failure, trace, and physical evidence rather than used as a solitary architecture proof.

### Common failures

Failures include drawing a process flowchart without a controlled function model; assuming left-to-right spacing expresses duration; using an arrow to mean both “then” and “sends message”; leaving AND branches without a defined join; labeling a choice OR when exactly one branch is required; omitting default/error guards; creating loops with no progress or timeout; hiding essential behavior behind stale references; showing nominal success only; duplicating functions across diagrams until versions diverge; using hierarchical numbering as execution order; ignoring shared-resource contention between “parallel” branches; treating every reachable path as permitted; and declaring the FFBD complete because a tool finds no disconnected blocks.

### Compact example

An emergency-message FFBD begins with receive request, then validates content and authority. An exclusive decision routes invalid requests to reject-and-record or valid requests to an AND split: protect content and determine destinations may proceed concurrently after their required inputs exist. A synchronization rule enables durable enqueue. Route selection iterates over eligible channels with attempt limit, deadline, idempotent message identity, and escape to operator escalation. Acknowledgement validation branches to complete-and-record or retry/escalate. Data objects such as protected message and acknowledgement appear only in an enhanced view with typed contracts; ordinary arrows retain execution semantics.

### Connections

FFBDs provide behavioral views for the function contracts and decompositions of SYSENG-021–022. They work with upcoming state/mode models, behavioral scenarios, logical components, allocation, control/data flows, alternatives, interfaces, timing analysis, resource budgets, failure analysis, verification, and configuration control.

## Governing Question

A hierarchy says what child functions belong under a parent, but not how they unfold. Real systems sequence preparation and action, choose among modes, run activities concurrently, wait for synchronization, retry after failure, and terminate or escalate. An FFBD makes this execution structure visible so engineers can review end-to-end scenarios and derive behavioral requirements.

The diagram is still an abstraction. Its arrow can state precedence while omitting actual data, latency, scheduling, physical dynamics, or actor responsibility. Its branches can be visually clear but semantically incomplete. The governing question is therefore how to create a controlled behavioral model whose constructs mean something precise enough to analyze and verify, while keeping evidence limits explicit.

## Why This Matters

Behavioral defects often hide between individually correct functions. Two parallel branches contend for the same resource. A decision has no branch for stale input. A retry repeats a non-idempotent action. A join waits forever after one branch is cancelled. A maintenance path bypasses authentication. These are composition problems that a functional hierarchy or requirement list rarely exposes.

NASA’s current handbook glossary defines an FFBD as a block diagram of system functions and their time sequence, and an enhanced FFBD as additionally representing control and data flows. NASA’s current Logical Decomposition guidance calls for functions to be arranged in logical sequence so operational use can be traced end to end. SEBoK 2.14 describes scenarios of functions as sequences synchronized by control flows and identifies FFBD/eFFBD among relevant behavioral modeling techniques. The older NASA Appendix F remains useful for notation examples—sequence, AND/OR, iteration, loop, replication, go/no-go, references—but must be treated as historical guidance rather than a current standard mandate.

FFBDs add value when they answer review questions: Can an outcome be reached? Which function enables which? What happens on no-go? Which work can overlap? What must synchronize? How does retry terminate? Their value declines when diagrams are decorative exports with undefined symbols, stale references, or no link to requirements and verification.

## Prerequisites and Retrieval

Before continuing, retrieve:

1. each function has a typed input/output/state/performance/failure contract;
2. decomposition hierarchy expresses parent-child contribution but not execution semantics;
3. operational scenarios and modes define contexts that behavioral paths must cover;
4. boundary preservation requires child behavior to reproduce the parent contract;
5. traceability and configuration identify exact sources, functions, interfaces, and evidence;
6. control flow is distinct from data, matter, energy, and resource flow;
7. verification evidence is configuration- and condition-specific;
8. executable model results prove only encoded properties under stated assumptions.

As a retrieval test, examine `sense → decide → act`. Ask what triggers sensing, whether “decide” can execute on stale/missing input, whether sensing repeats, whether action awaits authorization, how feedback closes the loop, and what occurs when actuation fails. The three arrows answer none of those questions without semantics.

## Learning Objectives

After completing this module, you should be able to:

1. define an FFBD viewpoint, scope, parent, scenario/mode, version, and notation profile;
2. distinguish functional sequence from data/resource exchange and physical connectivity;
3. model sequence, concurrency, inclusive/exclusive selection, merges, joins, iteration, replication, and references;
4. specify guard, enablement, completion, cancellation, synchronization, timeout, and failure semantics;
5. manage hierarchical FFBD levels without confusing numbering with time;
6. enumerate and challenge scenario paths across nominal and off-nominal cases;
7. connect FFBD paths to state, interface, timing, resource, hazard/threat, and verification models;
8. detect unreachable functions, missing exits, deadlock/livelock candidates, unintended bypasses, and ambiguous constructs;
9. use execution/simulation evidence without overclaiming real-system behavior;
10. review high-consequence flows with independent challenge and bounded conclusions.

## Core Exposition

**Define the viewpoint.** Record diagram ID/version, parent function, system boundary, abstraction level, lifecycle phase, configuration, operational scenario/mode, included/excluded actors, and decision purpose. State which FFBD/EFFBD notation profile and tool semantics apply. A symbol borrowed from another method must not silently change meaning.

**Start from controlled functions.** Reuse function IDs and action-object names from the functional architecture. Do not create near-duplicate blocks merely to make a diagram read naturally. A function block references a richer contract; the FFBD emphasizes execution relationships. If the path reveals a missing transformation, add it through functional-model governance.

**Anchor entry and required outcomes.** Define initial execution state, triggering event/condition, parent preconditions, and terminal outcomes. Distinguish successful completion, degraded completion, cancellation, safe termination, escalation, and unrecovered failure. A path should not simply stop at the page edge.

**Use sequence intentionally.** `A → B` means B becomes eligible only after A meets its defined completion condition, subject to guards and other prerequisites. It does not say B consumes A’s output unless an interface relation states that. It does not quantify delay or forbid internal overlap unless the semantic profile says so.

**Separate control and object flows.** In an ordinary FFBD, arrows primarily express functional progression. In an enhanced model, render data/information, matter, energy, resources, and triggers using distinct connectors, labels, or views. A control condition can enable a function without being transformed; a data object can arrive while another control prevents execution. Keep these distinctions queryable.

**Model concurrency with AND constructs.** An AND split enables multiple branches according to the profile. Define whether all start together, merely become eligible, or require separate resources. At the join, state whether all branches must complete, a quorum suffices, or cancellation is possible. Analyze race, contention, shared state, common cause, timeout, and partial result.

**Model selection with precise choice.** An exclusive choice selects exactly one eligible branch; inclusive OR permits one or more. Define evaluation instant, guard priority, overlaps, gaps, default/no-match behavior, authority, and evidence. Use a merge appropriate to the split. An unlabeled diamond or OR symbol cannot communicate these semantics reliably.

**Write guards as reviewable predicates.** A guard references governed state/inputs with units, thresholds, validity, freshness, uncertainty, and mode. Avoid prose such as “if appropriate.” If guards overlap, define priority or allowed concurrency. If none holds, define wait, reject, fallback, or failure; do not assume impossible.

**Represent go/no-go and failure exits.** Many decisions concern whether a function completed acceptably. Define the observation and authority behind `go`. A self-reported success flag may not independently demonstrate physical effect. Route no-go to diagnose, retry, degrade, rollback, safe-state, or escalation with bounded rules.

**Model iteration.** Identify the repeated subflow, domain or state being traversed, progress measure, maximum attempts/time, state carried between iterations, success condition, cancellation, and exhausted disposition. Verify idempotency or compensating behavior where side effects repeat. An unbounded loop may be a valid continuous-control mode, but its lifecycle exit and safety behavior still require definition.

**Distinguish iteration from replication.** Iteration repeats over time or a domain; replication creates coordinated instances or applies a function across members, potentially concurrently. Define instance identity, resource bounds, aggregation, failure isolation, ordering, and completion. A “for each device” replication may need quorum rather than all-device success.

**Use references instead of copies.** A reference block identifies target diagram/function, version rule, entry/exit contract, and configuration compatibility. Validate that references resolve and do not form forbidden recursion. If recursion is legitimate, define base/termination semantics. Copies become inconsistent and defeat traceability.

**Manage hierarchy.** A top-level FFBD shows mission-scale progression; lower-level diagrams expand a function. Hierarchical numbering supports identity and trace, not necessarily chronology. Ensure lower-level entry/exit behavior preserves the referenced parent block. A parent flow should not depend on hidden lower-level exit that its contract does not expose.

**Build scenario slices.** A large master model can generate views for nominal, degraded, emergency, maintenance, update, startup, shutdown, recovery, and retirement cases. Each slice records initial state, guards, configuration, actors, expected outcomes, and exclusions. Do not merge all modes into one unreadable drawing or let separate drawings drift.

**Enumerate paths carefully.** For finite bounded models, enumerate or sample paths to required outcomes, failure exits, and prohibited nodes. Branch/loop combinations can explode, so prioritize critical scenarios, boundary values, pairwise interactions, hazards, threats, and changed areas. Absence from sampled paths is not proof of unreachability.

**Analyze reachability.** Identify unreachable required functions/outcomes, unintended paths that bypass authorization or safety controls, terminal nodes without disposition, and references that cannot resolve. Reachability uses the encoded guards/state model; a graph-only traversal may report infeasible paths or miss dynamically enabled ones.

**Analyze deadlock and livelock.** Joins, shared resources, circular waits, lost events, and contradictory guards can block progress. Retry/recovery can create livelock. Specify wait-for relations, fairness/scheduling assumptions, timeouts, progress measures, and escape. Model checking can strengthen evidence within formalized bounds.

**Analyze timing.** Attach execution and communication bounds/distributions, scheduling assumptions, clock references, queues, resource contention, synchronization, retry, and physical response. For AND branches, completion often depends on the maximum branch time plus overhead, not their sum, but shared resources can serialize them. Diagram spacing has no numeric meaning.

**Analyze resources.** Functions that appear concurrent may share processor, operator, power, bandwidth, test equipment, or physical access. Connect FFBD execution to resource models and allocation. A logically valid schedule can be physically infeasible. Include priority inversion, preemption, exhaustion, and recovery where relevant.

**Integrate state and modes.** FFBD flow and state-machine transitions provide complementary views. State enables functions and functions cause state change. Cross-check triggers, guards, invariants, and terminal states. Avoid representing all state semantics as a combinatorial FFBD; SYSENG-024 treats state/mode models directly.

**Integrate interfaces.** For every adjacent or cooperating function, inspect typed input/output compatibility. A sequence edge is not an interface contract. Enhanced views can show objects, but authoritative schema, unit, timing, quality, security, and ownership remain governed. Add adapter functions when transformation is real.

**Integrate failure, hazard, and threat analysis.** Trace hazardous or adversarial paths, controls, detection, containment, and recovery. Ask whether maintenance or emergency routes bypass controls, a failed branch can falsely satisfy a join, or an attacker can manipulate a guard. FFBDs help structure analysis; they do not replace FMEA, fault trees, STPA, threat modeling, or assurance cases.

**Derive requirements and verification.** Behavioral analysis can derive sequencing, synchronization, timeout, retry, initialization, shutdown, and diagnostic requirements. Record their source rationale and authority. Link each path/construct to verification stimuli, state, expected progression/outcome, timing, configuration, oracle, negative cases, and evidence limitations.

**Control change.** When a requirement, function, interface, mode, or resource changes, traverse affected diagrams, guards, paths, timing, derived requirements, tests, and operational procedures. Preserve historical versions. Generated views must identify the authoritative semantic model and generator version.

**Review readability without sacrificing semantics.** Use consistent direction, limited crossing, clear labels, scope notes, legends, references, and page boundaries. Split views by scenario or level, not by arbitrary page size. A reader should be able to follow paths, but visual elegance cannot hide missing exception branches.

**Use execution as bounded evidence.** An executable EFFBD can animate paths, check constraints, or simulate timing. Record model version, semantics, solver/runtime, inputs, random seeds, bounds, and results. Animation showing success is one trace, not exhaustive verification. Formal claims require correct properties and abstraction arguments.

The following checker finds selected declared defects in a simplified FFBD record. It does not implement FFBD execution semantics.

<!-- bijux-verify: {"id":"ffbd-structure-record-check","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"nodes_total=7\nedges_total=7\nreachable_from_start=6\nunreachable=F-ORPHAN\nmissing_guard=E-3\nmissing_join_rule=F-JOIN\nterminal_without_outcome=F-FAIL\nevidence=declared_graph_only\n","stderr":""}} -->
```python
nodes = {
    "START": {"kind": "start"},
    "F-VALIDATE": {"kind": "function"},
    "F-SELECT": {"kind": "choice"},
    "F-SEND": {"kind": "function"},
    "F-JOIN": {"kind": "join", "rule": ""},
    "F-FAIL": {"kind": "function"},
    "F-ORPHAN": {"kind": "function"},
}
edges = [
    ("E-1", "START", "F-VALIDATE", "always"),
    ("E-2", "F-VALIDATE", "F-SELECT", "valid"),
    ("E-3", "F-SELECT", "F-SEND", ""),
    ("E-4", "F-SELECT", "F-FAIL", "no-route"),
    ("E-5", "F-SEND", "F-JOIN", "sent"),
    ("E-6", "F-JOIN", "F-VALIDATE", "retry"),
    ("E-7", "F-VALIDATE", "F-JOIN", "cancelled"),
]
outcomes = {"F-JOIN"}
reachable = {"START"}
changed = True
while changed:
    changed = False
    for _, source, target, _ in edges:
        if source in reachable and target not in reachable:
            reachable.add(target)
            changed = True
terminals = {node for node in reachable if not any(source == node for _, source, _, _ in edges)}
print(f"nodes_total={len(nodes)}")
print(f"edges_total={len(edges)}")
print(f"reachable_from_start={len(reachable)}")
print("unreachable=" + ",".join(sorted(set(nodes) - reachable)))
print("missing_guard=" + ",".join(edge_id for edge_id, _, _, guard in edges if not guard))
print("missing_join_rule=" + ",".join(node for node, attrs in nodes.items() if attrs["kind"] == "join" and not attrs.get("rule")))
print("terminal_without_outcome=" + ",".join(sorted(terminals - outcomes)))
print("evidence=declared_graph_only")
```

The checker treats nonempty guard strings as valid and ignores state, modes, feasibility, concurrency, timing, loop termination, and semantic outcomes. Its reachability result is structural only.

## Definitions and Notation

Let $Succ_M(f,s,m,c)$ denote functions/control constructs enabled after $f$ under state, mode, and configuration. Let a run be $\rho=\sigma_0\xrightarrow{a_1}\sigma_1\cdots$, where actions include function start/complete, event, split, join, timeout, and cancellation. Define $Outcome(\rho)$ and $Trace(\rho)$ at the parent boundary.

For required cases $K$, a scenario-coverage claim may be written:

$$
\forall k\in K:\exists \rho\in Runs(M,k): RequiredOutcome(k,\rho).
$$

This existential property does not rule out unsafe runs. A safety invariant instead seeks:

$$
\forall \rho\in Runs(M,K_{assured}): \Box Safe(\rho),
$$

within the modeled state space and fairness/environment assumptions. Formal notation clarifies the claim but cannot validate the abstraction by itself.

For concurrent branches $b_1,\ldots,b_n$ with independent execution and all-branch join, an ideal bound may be:

$$
T_{AND}=T_{split}+\max_i T_{b_i}+T_{join}.
$$

If branches share resources or one depends on another’s object flow, the independence assumption fails. Resource scheduling or a different functional structure must determine the bound.

## Mechanisms, Invariants, or Proof Structure

Use this behavioral-model loop:

1. **Frame:** select parent, boundary, level, scenario/mode, initial state, configuration, outcomes, and notation profile.
2. **Lay out nominal flow:** connect controlled functions by explicit completion/enablement semantics from trigger to outcome.
3. **Add logic:** define AND, choice, merge/join, iteration, replication, reference, guard, timeout, and cancellation behavior.
4. **Add off-nominal behavior:** model invalid, failed, delayed, degraded, emergency, maintenance, recovery, and termination paths.
5. **Integrate semantics:** cross-check function contracts, objects/interfaces, state/modes, time, resources, hazards/threats, and parent boundary preservation.
6. **Analyze:** inspect reachability, paths, deadlock/livelock, timing, shared resources, bypasses, and unresolved references; execute/formalize where valuable.
7. **Trace and verify:** link sources, derived requirements, tests, rationale, results, and limitations; baseline and change-control the semantic model.

The result is a reviewable behavioral argument, not a proof that the realized system will execute exactly as drawn. Confidence depends on semantic precision, model fidelity, scenario and state coverage, empirical evidence, and independent review proportional to consequence.

## Alternatives and Trade-Offs

**Classic FFBDs** communicate sequence and functional logic compactly. **EFFBDs** integrate objects, triggers, resources, and timing but demand stronger tool/profile governance. Use only the semantics reviewers and validators can inspect.

**SysML activity diagrams** offer standardized action/object/control constructs and are widely integrated with architecture models. **BPMN** can suit organizational workflows; **state machines** excel at state-dependent behavior; **sequence diagrams** emphasize interactions; **Petri nets** support concurrency analysis. Select by question, not fashion, and map semantics when using coordinated views.

**One master diagram** reduces duplicate truth but becomes unreadable. **Generated scenario/level views** improve review while preserving one semantic source, provided generation fidelity and versioning are verified. Hand-maintained duplicates are risky.

**Informal diagrams** are quick for discovery. **Executable/formal models** enable stronger checks but cost precision and abstraction work. Increase rigor with consequence, concurrency complexity, and need for assurance.

**Explicit failure branches** enlarge diagrams but expose recovery and verification. Separate failure views can improve readability, yet they must remain connected to nominal state and shared functions. Never hide failure behavior merely to keep a page clean.

## Failure Modes and Misconceptions

- **“Arrow means data moves.”** In an FFBD it normally indicates execution flow; object flow needs distinct semantics.
- **“Parallel means simultaneous.”** It usually means concurrently enabled; scheduling/resources determine execution.
- **“OR means exactly one.”** Inclusive OR and XOR differ; declare the rule.
- **“The join waits for everything.”** Only if its completion semantics say so, including cancellation/failure.
- **“Looping until success is safe.”** Define progress, attempts, time, idempotency, resource limits, and exhausted outcome.
- **“Numbering gives sequence.”** Identifiers usually reflect hierarchy; arrows and constructs govern flow.
- **“Reachable means feasible.”** Encoded graph reachability ignores unmodeled state, resources, physics, and semantics.
- **“Every required node is reachable, so the model is complete.”** Unsafe paths, missing modes, interfaces, failures, or functions can remain.
- **“Animation validates behavior.”** It demonstrates selected runs under tool semantics.
- **“The FFBD replaces other views.”** State, interface, timing, resource, physical, safety, security, and evidence models remain necessary.

## Worked Examples

### Example 1

**Cold-chain startup.** Initialize → self-check → validate sensors branches on go/no-go. Go enables concurrent estimate-state and prepare-cooling; their join requires both current state and ready actuator before control begins. No-go enters degraded hold and alarm. Diagram timing is supplemented by measured bounds. Tests cover named sensors and temperatures, not every packing or failure combination.

### Example 2

**Flood warning selection.** Validate observations, forecast threshold, then XOR between no-warning monitoring and warning authorization. An “uncertain” guard routes to human review with deadline and conservative escalation. Guards specify probability/quality semantics. Historical replay supports known events; it cannot establish behavior under novel weather or unavailable observers.

### Example 3

**Aircraft braking concurrency.** After demand validation, wheel-state estimation and actuator-readiness assessment are concurrently enabled. A join requires current estimates from all required channels or defined degraded quorum. Control and feedback iterate at bounded period. Functional logic supports hazard analysis, but safe braking requires dynamic, hardware, runway, human, and certification evidence.

### Example 4

**Secure recovery loop.** Establish claimant evidence, assess risk, choose an eligible proof channel, validate response, and retry over a limited channel domain. Each attempt has identity and rate limit; exhaustion locks and escalates. Sending a code is object flow, not execution arrow. Tests cover modeled attacks and channels, not universal identity assurance.

### Example 5

**Water treatment go/no-go.** Treat water → sample → analyze → decision. Go routes product to storage; no-go isolates, records, diagnoses, and conditionally reprocesses. The loop has batch identity and maximum cycles. A passing online sensor cannot alone authorize potability; regulatory laboratory and process evidence retain their scope.

### Example 6

**Warehouse order replication.** After reservation, pick function replicates across item lines with bounded workers. Join requires all mandatory lines or explicit partial-order policy; substitutions follow separate authorization. Shared aisle/robot capacity invalidates naive maximum-branch timing. Load tests support modeled demand and resources only.

### Example 7

**Satellite safe mode.** Detect anomaly enables parallel stabilize attitude, preserve energy, and establish communication opportunity. Join semantics do not require immediate ground contact to preserve survival outcome. Recovery choice depends on resource state and authority. Simulation is bounded by modeled faults, orbit, and dynamics.

### Example 8

**Clinical alert escalation.** Validate patient/context → calculate bounded risk → clinical-policy choice → present alert and start timer. Acknowledgement completes; timeout escalates; contradictory data routes to human assessment rather than ordinary suppression. Retrospective runs support specified data and workflow, not safe clinical deployment by themselves.

### Example 9

**Privacy deletion.** Authenticate request, resolve scope, then replicate locate/delete across controlled stores. Legal-hold guard excludes items with recorded authority; join aggregates success, failure, and unreachable stores rather than falsely declaring completion. Backup expiry is referenced as a versioned subflow. Evidence is bounded by the lineage inventory.

### Example 10

**Shuttle door control.** At stop and authorization, warn then command close while monitoring obstruction. Obstruction guard cancels closing and initiates reverse; maximum retries escalate to operator and inhibit motion. A join between confirmed closure and interlock state enables departure. Fixture tests cover specified objects; representative accessibility and independent safety evidence remain necessary.

## Cross-Program Connections

- **Platform Engineering:** delivery/recovery workflows use branching, concurrency, retry, rollback, approvals, and observability with FFBD-like semantics.
- **API and Service Engineering:** orchestration/choreography, sagas, timeouts, idempotency, and compensation require explicit control versus message flow.
- **Data Engineering:** DAG schedulers model dependencies and retries, but data lineage, state, quality, and backfill semantics go beyond reachability.
- **Object-Oriented Programming:** sequence of collaborations can realize FFBD paths; method-call diagrams are not automatically system behavior.
- **Functional Programming:** workflow composition, algebraic choices, and effect handling can implement precise control logic while external time/resources remain modeled.
- **Safety and security:** FFBD paths help reveal bypass, unsafe sequencing, failed joins, retry abuse, and recovery gaps when integrated with assurance analyses.

## References

1. ISO, “ISO/IEC/IEEE 15288:2023 — Systems and software engineering — System life cycle processes,” second edition, published 2023-05. https://www.iso.org/standard/81702.html
2. NASA, “System Engineering Handbook: Appendix,” definitions of FFBD and Enhanced FFBD and note on Functional, Timing, and State Analysis. https://www.nasa.gov/reference/system-engineering-handbook-appendix/
3. NASA, “4.3 Logical Decomposition,” NASA Systems Engineering Handbook. https://www.nasa.gov/reference/4-3-logical-decomposition/
4. NASA, *Systems Engineering Handbook*, NASA/SP-2007-6105 Rev. 1, historical Appendix F notation examples. https://explorers.larc.nasa.gov/HPSMEX/MO/pdf_files/NASA_SP-2007-6105_Rev_1.pdf
5. SEBoK Editorial Board, “Logical Architecture,” *Guide to the Systems Engineering Body of Knowledge*, version 2.14. https://sebokwiki.org/wiki/Logical_Architecture
6. SEBoK Editorial Board, “Functional Architecture,” *Guide to the Systems Engineering Body of Knowledge*, version 2.14. https://sebokwiki.org/wiki/Functional_Architecture
7. SEBoK Editorial Board, “Modeling Standards,” *Guide to the Systems Engineering Body of Knowledge*, version 2.14. https://sebokwiki.org/wiki/Modeling_Standards
8. White, T., Stoller, S., Greene, W., Christenson, R., and Bowen, B., “Development of the Functional Flow Block Diagram for the J-2X Rocket Engine System,” NASA NTRS 20070031871, 2007. https://ntrs.nasa.gov/citations/20070031871
9. INCOSE, “Relationships Between Common Graphical Representations Used in System Engineering,” resource metadata for Long (1995). https://www.incose.org/resource/7-4-2-relationships-between-common-graphical-representations-used-in-system-engineering/

## Exercises

### Exercise 1

Create an FFBD for `authorize and dispense fuel` covering nominal operation, invalid authorization, unavailable payment network, nozzle removal, cancellation, flow cutoff, receipt, and emergency stop. Distinguish control from matter/data flow.

### Exercise 2

Two AND branches have bounded durations 180 ms and 260 ms; split/join overhead is 15 ms and 20 ms. A shared resource serializes a 90 ms segment in branch A with a 120 ms segment in branch B. Calculate the ideal independent bound, then explain why it is invalid and give a conservative serialized bound under stated assumptions.

### Exercise 3

Review a choice with guards `temperature > 80`, `temperature < 90`, and no default. Diagnose overlaps/gaps and design exclusive, uncertainty-aware behavior.

### Exercise 4

Design a bounded retry subflow for delivering an emergency message over three channels. Include identity, channel selection, timeout, idempotency, acknowledgement, resource limits, cancellation, and exhausted outcome.

### Exercise 5

Construct an assurance plan for an FFBD controlling autonomous medication delivery. State what graph checks, model execution, timing analysis, fault injection, clinical validation, and independent review can and cannot establish.

## Answers to the Exercises

### Answer 1

Trigger `request fueling` leads to establish session and validate equipment readiness. Authorization and safety-state validation can be concurrently enabled if their inputs/resources are independent; their join requires both valid. Authorization failure rejects and records. Network unavailable branches to controlled offline policy or deny—never implicit approval. After authorized nozzle removal, select grade/limit, enable pump, and begin metered fuel transfer while concurrently monitoring emergency stop, nozzle/vehicle state, flow anomaly, authorization limit, and user cancellation.

Any cutoff event disables energy/flow before final accounting. Normal completion stops flow, verifies zero flow, closes transaction, updates authorization, produces receipt, and records evidence. Emergency stop enters safe isolation, alarms, and requires authorized reset. FFBD arrows express execution; payment messages are data flows, fuel is matter flow, electrical power is resource/energy, and emergency stop is control. Evidence remains bounded by tested pumps, networks, fuels, failure conditions, and applicable safety/payment authority.

### Answer 2

With independent concurrent branches and all-branch join:

$$
T_{ideal}=15+\max(180,260)+20=295\ \text{ms}.
$$

The independence assumption is false because branch segments needing the shared resource cannot overlap. If each branch duration includes its respective shared segment, all nonshared work can otherwise overlap, and the two shared segments serialize without extra switching, a conservative construction is split overhead plus the larger nonshared remainder plus both shared segments plus join overhead:

$$
15+\max(180-90,260-120)+90+120+20
=15+140+210+20=385\ \text{ms}.
$$

This is conditional, not a universal worst case. Actual ordering, preemption, queues, blocking, resource setup, branch dependencies, jitter, and scheduling policy can increase or reduce it. Validate with a resource-aware schedule/model and integrated timing evidence on named configurations.

### Answer 3

The first two guards overlap for $80<T<90$, so an exclusive-choice model has ambiguous eligibility. Values exactly 80 and 90 have only the `<90` and `>80` branches respectively, but the meaning of each branch remains unclear; invalid/missing/stale/uncertain measurements have no route. Define a calibrated measurement $T$, timestamp/freshness, uncertainty $u$, mode, and policy thresholds.

One exclusive policy might be: `high` if the conservative lower bound $T-u\ge90$; `normal` if upper bound $T+u\le80$; `uncertain-band` otherwise; and `invalid` for missing, stale, out-of-range, or failed-quality input. Give each branch an outcome—protective action, nominal continuation, further measurement/human review, or safe degraded response—and define priority if emergency constraints override. Thresholds and conservatism require source authority; a diagram does not decide them.

### Answer 4

Assign immutable message ID and deadline, validate authority/content, determine eligible ordered channels, and initialize attempt/channel state. For each eligible channel, prepare a channel-specific representation, transmit idempotently, start timeout, and validate authenticated acknowledgement matching message, recipient, and version. Valid acknowledgement completes and cancels outstanding attempts. Timeout or retryable failure advances attempt under per-channel/global limits; permanent failure advances channel. Duplicate acknowledgement is recorded without repeating the external action.

The loop bounds total attempts, elapsed time, bandwidth/energy, and concurrent sends. Cancellation requires competent authority and records disposition. When channels exhaust or deadline approaches, escalate to operator/alternate operational procedure and emit explicit undelivered/uncertain outcome—never success. Tests can cover encoded loss, duplication, delay, corruption, and channel failures; they cannot prove availability of every real network or recipient response.

### Answer 5

Structural checks verify unique IDs, resolved references, declared guards, paired constructs, reachability, terminal outcomes, and trace presence. Model execution enumerates or samples encoded runs and can reveal deadlock, livelock, bypass, or bad state under bounded semantics. Timing/resource analysis evaluates deadlines, contention, synchronization, and retry under stated distributions/bounds. Formal model checking can establish encoded invariants over a bounded/formal state space if abstraction and properties are correct.

Fault injection tests sensor, computation, communication, actuator, power, stale/duplicate data, and recovery behavior on named configurations. Physical measurement verifies commanded versus delivered dose and independent interlocks. Clinical/human-factors validation examines prescription interpretation, alarm response, workflow, representative populations, and outcomes. Cybersecurity, privacy, safety, regulatory, and configuration evidence remain separate. Independent reviewers challenge assumptions, omitted paths, common cause, model fidelity, and residual risk. No graph, animation, test suite, or retrospective accuracy result establishes universal clinical safety; conclusions remain bounded to authorized configurations, patients, contexts, failures, and evidence.
