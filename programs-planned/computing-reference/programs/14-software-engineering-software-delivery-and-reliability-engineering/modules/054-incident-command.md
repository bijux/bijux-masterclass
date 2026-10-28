---
module_id: SDRE-054
program: Software Engineering: Software Delivery & Reliability Engineering
level: 2
module_number: 54
title: Incident Command
status: complete
last_verified: 2026-09-06
---

# Incident Command

## One-Page Review

### Governing question

How can a temporary command system coordinate many capable responders under uncertainty so that authority is explicit, work is bounded, changes do not conflict, evidence survives, and control transfers safely as an incident grows or recedes?

### Essential definitions

- **incident command** is the temporary coordination function accountable for objectives, priorities, roles, constraints, and shared state during a managed incident;
- the **incident commander** (IC) maintains the whole-response view and delegates work; the IC need not be the deepest technical expert or line manager;
- **operations** performs approved investigation and mitigation; **communications** maintains audience-specific updates; **planning** tracks future needs, resources, handoffs, and restoration work;
- **command** establishes authority and objectives; **control** maintains shared state, constraints, and coordinated execution; **communication** moves verified information to responders and stakeholders;
- **delegation** transfers bounded authority for an outcome while accountability and escalation remain explicit;
- **span of control** is the number of direct reports or work cells one lead can coordinate effectively in the current conditions;
- a **command post** is the authoritative coordination location and incident identity, whether physical or virtual;
- an **incident state document** is the live record of impact, roles, objectives, decisions, actions, evidence, risks, and exit criteria;
- **freelancing** is uncoordinated incident action outside assigned authority;
- **command transfer** is an acknowledged change of commander with a state briefing and announcement;
- **unified command** coordinates multiple legitimate authorities without pretending one organization owns every decision;
- **demobilization** deliberately releases roles and resources while preserving monitoring, ownership, and unfinished work.

### Central model, mechanism, or theorem

Command repeatedly executes

$$
\text{assess}\rightarrow\text{set objectives}\rightarrow\text{delegate}\rightarrow
\text{execute}\rightarrow\text{observe}\rightarrow\text{reassess}.
$$

At command-state revision $k$, record $S_k=(I_k,R_k,O_k,A_k,D_k,C_k,X_k)$: impact, roles, objectives, active actions, decisions, communications, and exit criteria. Every accepted event receives a monotonically increasing sequence number. Roles may expand recursively, but each active task has one owner, a boundary, a reporting time, and a stop or escalation condition.

### Critical invariants

- exactly one current command authority is publicly identifiable, or a declared unified-command protocol names joint authorities and conflict resolution;
- the IC owns coordination, not every keyboard and diagnosis;
- one operations path controls production mutations and prevents conflicting changes;
- objectives describe protected outcomes and constraints; tasks remain bounded and attributable;
- facts, hypotheses, decisions, actions, and results are recorded as different fields;
- communication cadence and audiences are assigned rather than improvised by operators;
- sensitive evidence follows specialist access rules without fragmenting common incident identity;
- command transfer requires briefing, explicit acceptance, and announcement;
- exit criteria require user recovery and controlled residual risk, not merely a quiet alert;
- demobilization leaves owners, deadlines, monitoring, evidence, and rollback or restoration work.

### Common failures

Failure patterns include choosing the most senior person automatically, making the IC debug, declaring roles without authority, crowding one channel, assigning work to groups rather than people, allowing production freelancing, confusing hypotheses with facts, issuing commands without read-back, optimizing activity instead of objectives, suppressing dissent, forgetting external dependencies, losing restricted evidence, ambiguous handoffs, ending command when graphs first recover, and retaining a giant response after the incident contracts.

### Compact example

A payment outage spans API, database, network, and vendor teams. Twenty engineers join one channel and three attempt changes. The IC states the objective “stop duplicate charges while preserving accepted orders,” assigns an operations lead as the sole change coordinator, creates database and network cells with named leads, assigns communications and planning, and records a freeze on unrelated deploys. Each proposal includes owner, expected observation, risk, rollback, and deadline. Parallel expertise remains; conflicting mutations stop.

### Connections

[SDRE-053](053-operational-alert-triage.md) produces the initial owned disposition. [SDRE-055](../ROADMAP.md) next develops technical investigation within command, and [SDRE-057](../ROADMAP.md) deepens status communication.

## Governing Question

Incidents create simultaneous demands: protect users, change a live system, gather evidence, answer stakeholders, coordinate dependencies, consider security or legal obligations, schedule relief, and preserve future recovery options. Technical skill alone does not order these demands. When everyone acts independently, locally reasonable actions can conflict: one team rolls back while another migrates data; a vendor changes a dependency without telling the service owner; a communicator announces recovery before user evidence exists.

Incident command supplies a temporary operating system for the response. It does not grant unlimited authority or replace technical ownership. It makes goals, roles, decision rights, constraints, evidence, and communication visible. The command structure must scale with complexity and then shrink. It must survive tool failures, time zones, personnel changes, and conflicting organizational authority.

The governing question is how to gain coordination without bottlenecking every decision through one person. The answer is bounded delegation: centralize objectives, priorities, cross-cutting risk, and shared state; decentralize technical work to qualified role owners; require concise reporting and explicit escalation.

## Why This Matters

Google's SRE incident-management chapter describes unmanaged incidents in which sharp technical focus, poor communication, and freelancing compound harm, then defines incident command, operations, communications, and planning roles [1]. The SRE Workbook similarly separates managing response from resolving the technical problem and emphasizes a clear command line, defined roles, a working record, and early declaration [2]. These sources are experience reports and guidance, not proof that one role vocabulary fits every organization.

The structure is adapted from emergency management. FEMA's National Incident Management System describes common terminology, manageable span of control, modular organization, and explicit command transfer with briefing and notification [5]. Software incidents differ from physical emergencies: production authority, automation, reversible changes, information security, and globally distributed teams alter the mechanisms. The durable lessons are clarity, scalability, accountability, common state, and practiced transfer—not borrowed titles alone.

Current cybersecurity guidance also treats incident response as part of organizational risk management rather than an isolated technical event [6]. A reliability IC must therefore know when to activate security, privacy, safety, legal, customer, or executive authorities. The IC coordinates interfaces but must not decide matters reserved for those roles.

## Prerequisites and Retrieval

Retrieve [SDRE-050](050-writing-a-production-readiness-review.md) for predeclared scenarios and authority; [SDRE-051](051-incident-severity-and-classification.md) for severity; [SDRE-052](052-on-call-design.md) for reachable roles; and [SDRE-053](053-operational-alert-triage.md) for initial disposition and evidence. Recall queues, graphs, expected loss, versioned state, least privilege, two-person controls, and rollback.

## Learning Objectives

After this module, you should be able to:

1. distinguish command, operations, communications, planning, technical ownership, and organizational hierarchy;
2. declare command early with identity, authority, objectives, and a command post;
3. scale a response using bounded delegation and manageable reporting relationships;
4. preserve a versioned common operating picture and decision record;
5. authorize parallel work without permitting conflicting production mutations;
6. reason about decision latency, coordination load, and action risk;
7. perform an explicit command transfer, unified-command negotiation, and demobilization;
8. test incident command through exercises and evidence rather than role names alone.

## Core Exposition

### Declare the command system

Declaration should state incident identity, current severity and confidence, affected outcomes, current IC, authoritative command post and state document, immediate constraints, and next update time. The declarer becomes IC until an explicit transfer unless local policy says otherwise. Early declaration is cheap to reverse; late declaration allows hidden coordination debt to grow [1].

Authority is bounded by preapproved incident policy, employment roles, technical permissions, law, contracts, and safety rules. The IC may stop risky changes, set response priorities, and allocate responders where policy permits. The IC cannot invent access, waive statutory obligations, disclose restricted evidence, or command a vendor beyond contract.

### Separate objectives from tasks

An objective describes an outcome: “prevent new corrupt writes,” “restore read access for the affected region,” or “establish whether credentials were exposed.” A task describes work: “disable endpoint X” or “compare audit logs.” Objectives remain stable enough to coordinate alternatives; tasks change as evidence evolves.

For each operational period, keep a short ordered set of objectives, constraints, and success evidence. Too many priorities mean none are priorities. Reassess after material state change or at a declared cadence. Operations chooses technical tactics within delegated boundaries and returns observations, not only activity.

### Define roles as decision rights

The IC maintains the overall picture, sets priorities, resolves cross-role conflicts, delegates roles, requests resources, and decides command transitions. Operations controls technical response and production mutations. Communications produces verified updates for responders, users, leadership, vendors, and authorities at appropriate detail. Planning tracks resources, future operational periods, handoffs, restoration, dependencies, and work that should not distract current operations.

An undelegated role remains with the IC [1]. This default makes small incidents possible, but it is also a scaling signal: when the IC cannot maintain state or cadence, delegate. Add safety, security, legal, liaison, scribe, or subject-matter roles when consequence requires them. A role title without clear inputs, outputs, authority, and escalation is ceremony.

### Build a command graph

Represent reporting relationships as a rooted directed graph. Every active responder has one incident-role lead for priorities, even if their ordinary manager differs. Cross-cell consultation is allowed; conflicting tasking returns through leads. Let $d(v)$ be the number of direct incident reports to lead $v$. Span of control is contextual, but sustained large $d(v)$ increases update traffic and state loss.

FEMA material uses one supervisor to five subordinates as an optimal reference while explicitly allowing conditions to require different ratios [5]. Treat this as calibration, not a software theorem. Complexity, experience, automation, risk, and communication quality matter. Split a crowded operations group into cells with leads, then require high-level summaries.

### Maintain one common operating picture

The state document begins with current impact, severity/confidence, commander and leads, objectives, constraints, active actions, decisions, known risks, next update, and exit criteria. Below that, keep an append-only timeline with timestamps and authors. Link raw telemetry and restricted evidence rather than copying uncontrolled secrets.

Facts are observations with provenance. Hypotheses are candidate explanations. Decisions select a course under stated evidence and constraints. Actions are mutations or inquiries. Results are observed consequences. Mixing these creates false certainty; deleting disproven hypotheses destroys the reasoning trail.

### Govern production actions

Each mutating action should declare identifier, owner, objective, target and scope, preconditions, expected observation, major risks, rollback or stop rule, authorization, start/end time, and result. Operations sequences changes where interactions are possible. Use idempotency keys or a durable ledger where tools permit. Two-person controls apply to irreversible or high-risk actions according to policy.

The IC approves priority and acceptable cross-cutting risk; qualified operators retain responsibility for technical execution and may refuse unsafe commands. “Command” does not suspend professional judgment. A stop-the-line path must exist when a responder sees unmodeled danger.

### Balance speed and decision quality

Let action $a$ have estimated loss if delayed, $L_d(a,t)$, and estimated action-induced loss $L_a(a)$. Under uncertainty, command compares bounded scenarios rather than pretending to know exact probabilities. A simple decision framing is

$$
E[L\mid a]=p_f(a)L_f(a)+p_s(a)L_s(a),
$$

where failure and success consequences are conditional estimates. Values support explicit reasoning; they do not authorize averaging away safety, confidentiality, or irreversible-loss constraints.

Decision latency can be decomposed as evidence collection, authority lookup, coordination, and execution preparation. Preapproved playbooks reduce authority lookup; role delegation reduces coordination; reversible controls reduce consequence. If delay crosses a harm deadline, choose a conservative reversible action and preserve evidence.

### Control communication channels

Use an authoritative responder channel for coordination, a state document for durable truth, and audience-specific outbound channels. Questions from executives, customers, and vendors should reach communications or liaison rather than interrupt operations. Updates state confirmed impact, actions and results, remaining risk, current needs, and next update time. [SDRE-057](../ROADMAP.md) covers message design in depth.

Channels are dependencies. Maintain out-of-band contact and state access when identity, chat, documentation, or the affected provider fails. Google guidance explicitly warns against relying solely on the system being repaired and recommends clear live handoff [1].

### Transfer command atomically

The outgoing IC briefs incident identity, impact, objectives, command graph, active actions, decisions, hazards, communications, restricted interfaces, resources, and exit criteria. The incoming IC asks questions and explicitly accepts. The transfer gets a sequence number and timestamp, then is announced everywhere authority is consumed.

If the outgoing commander leaves before acceptance, there is a command gap. If both act afterward, there is split command. Treat the transfer like an ownership handoff: prepare, accept, publish, reconcile. Retain the previous IC briefly for clarification without leaving authority ambiguous.

### Use unified command for genuine plural authority

Some incidents cross companies, jurisdictions, safety functions, or independently accountable business units. One software IC cannot erase those authorities. Unified command declares shared objectives, information boundaries, decision domains, and conflict resolution while each authority retains its obligations.

Vendor coordination alone is not unified command if the vendor merely supplies a service. Conversely, a security incident may require a restricted security command cell whose evidence access differs while reliability command retains user-impact and recovery coordination. Record interfaces and avoid copying secrets into broad channels.

### Scale down and terminate deliberately

Command should contract when objectives, work, and communication load contract. Release excess responders explicitly; otherwise they continue uncoordinated observation or changes. Preserve a monitoring owner, rollback window, restoration tasks, stakeholder cadence, and re-escalation trigger.

Exit criteria include protected outcome recovery over a declared interval, controlled ongoing risk, stopped harmful processes, verified monitoring, reconciled changes, assigned residual work, preserved evidence, and authorized communication. Closing command is not declaring root cause. [SDRE-058](../ROADMAP.md) and [SDRE-059](../ROADMAP.md) later preserve timelines and analyze the event.

### Validate command as a system

Exercises should inject notification failure, unavailable leaders, simultaneous changes, contradictory evidence, tool loss, vendor delay, restricted security evidence, time-zone handoff, and fatigue. Observe declaration time, role clarity, unowned tasks, conflicting mutations, update cadence, decision latency, transfer correctness, and exit evidence. A tabletop checks reasoning; a controlled simulation additionally checks tools and access.

The following finite model enforces one current commander and rejects uncoordinated production changes. It is illustrative, not a complete incident platform.

<!-- bijux-verify: {"id":"enforce-command-ownership","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"1 declare commander=alice\n2 assign operations=bob\n3 execute drain-region owner=bob\nREJECT freelance action by carol\n4 transfer commander=dana\n","stderr":""}} -->
```python
class CommandLog:
    def __init__(self):
        self.seq = 0
        self.commander = None
        self.operations = None

    def record(self, text):
        self.seq += 1
        print(f"{self.seq} {text}")

    def declare(self, commander):
        if self.commander is not None:
            raise ValueError("command already active")
        self.commander = commander
        self.record(f"declare commander={commander}")

    def assign_operations(self, actor, lead):
        if actor != self.commander:
            raise PermissionError("only commander assigns operations")
        self.operations = lead
        self.record(f"assign operations={lead}")

    def execute(self, actor, action):
        if actor != self.operations:
            print(f"REJECT freelance action by {actor}")
            return
        self.record(f"execute {action} owner={actor}")

    def transfer(self, outgoing, incoming, accepted):
        if outgoing != self.commander or not accepted:
            raise PermissionError("invalid command transfer")
        self.commander = incoming
        self.record(f"transfer commander={incoming}")


log = CommandLog()
log.declare("alice")
log.assign_operations("alice", "bob")
log.execute("bob", "drain-region")
log.execute("carol", "restart-database")
log.transfer("alice", "dana", accepted=True)
```

The run proves only this event sequence under the recorded interpreter. Real authorization, identity, durability, concurrency, emergency override, and distributed consensus require stronger mechanisms.

## Definitions and Notation

Let $S_k$ be command state after accepted event $k$. Let $IC(S_k)$ be current command authority, $R_k$ role assignments, $O_k$ ordered objectives, $A_k$ active actions, $D_k$ decisions, $C_k$ communication commitments, and $X_k$ exit criteria. Let $owner(q)$ be the single accountable owner of task $q$.

A **fact** has provenance and observation time; a **hypothesis** is a falsifiable candidate explanation; a **decision** records selected action and rejected alternatives; an **action** changes or queries state; a **result** is observed after an action. Confidence belongs to a claim, not a person.

A **role** is a temporary bundle of decision rights and duties. **Ordinary hierarchy** is the persistent management structure. Incident roles can cross that hierarchy but do not remove employment, legal, or technical-control boundaries.

## Mechanisms, Invariants, or Proof Structure

**Single-command invariant.** For ordinary command, $|IC(S_k)|=1$. Unified command replaces this with a declared authority set plus domains and conflict resolution. An informal collection of senior people is neither.

**Single-owner invariant.** Every active task has exactly one accountable role owner. Many executors may collaborate, but ownership by a channel or team is ambiguous.

**Ordered-event invariant.** Accepted state transitions receive increasing sequence numbers. Wall-clock timestamps aid correlation but do not alone establish order across skewed systems.

**Mutation-control argument.** If all production mutations pass through one operations coordination path, conflicting proposals can be detected before execution. This does not prove the chosen action safe; it removes one class of uncoordinated conflict.

**Delegation rule.** A delegation names outcome, authority, constraints, evidence, report time, and escalation condition. Delegating a task without these fields transfers work but not a safe decision boundary.

**Span-of-control argument.** Update edges grow with direct reports. Cells compress detail by making leads summarize, trading some information latency for a tractable command view. Expand or split based on observed coordination load, not a ritual number.

**Transfer atomicity.** Prepare without acceptance leaves old command active; acceptance without publication leaves consumers stale. Safe transfer requires briefing, explicit acceptance, publication, and reconciliation.

**Termination invariant.** Command ends only when exit evidence holds or a named authority accepts residual risk. Quiet tools, absent pages, or exhausted responders are not exit evidence.

## Alternatives and Trade-Offs

**Technical expert as IC versus separate IC.** The expert starts quickly but becomes a coordination bottleneck. A separate practiced IC frees expertise for operations. Small incidents can combine roles until load triggers delegation.

**Centralized approval versus bounded delegation.** Central approval gives one risk view but adds delay. Delegation accelerates parallel work but needs explicit boundaries, reporting, and stop rules.

**Flat response versus recursive cells.** Flat channels preserve direct access at small scale. Cells reduce noise and span at large scale but may filter weak signals. Leads must surface exceptions and dissent.

**Single command versus unified command.** Single command is simpler when one authority exists. Unified command respects plural authority but increases negotiation cost. Do not use it merely because several teams participate.

**Rich document versus minimal state card.** Rich records support handoffs and learning but can consume operators. Keep current state compact at the top and delegate timeline capture.

**Synchronous meetings versus asynchronous updates.** Meetings synchronize complex decisions but interrupt operations. Use short decision-focused checkpoints and durable asynchronous state between them.

**Aggressive action versus staged reversibility.** Large changes may restore service quickly but increase blast radius. Canary, traffic shift, feature disablement, and bounded rollback often buy information with lower risk.

**Fixed roles versus adaptive structure.** Fixed vocabulary improves practiced coordination. Adaptive cells fit incident topology. Keep role semantics stable while changing staffing and decomposition.

## Failure Modes and Misconceptions

1. **“The most senior person must command.”** Incident competence and availability matter; ordinary rank does not define the role.
2. **“The IC should solve the hardest technical problem.”** That abandons whole-response state and coordination.
3. **“Command means every decision waits for one person.”** Bounded delegation is the scaling mechanism.
4. **“More responders always help.”** Unassigned people add communication edges, duplicate work, and mutation risk.
5. **“A channel is a command post.”** It lacks authority unless incident identity, roles, state, and conventions are declared.
6. **“Everyone knows who owns it.”** Ownership must be named and acknowledged.
7. **“A hypothesis in the timeline is a fact.”** Claim type and provenance must remain visible.
8. **“Fast action excuses freelancing.”** Conflicting emergency changes can compound harm.
9. **“Executives can bypass operations.”** Requests enter command; qualified operators retain technical safety duties.
10. **“Five reports is a universal limit.”** Span depends on complexity, risk, skill, and tooling.
11. **“Unified command means consensus on every task.”** It partitions decision domains and defines conflict resolution.
12. **“Security should copy everything into the main room.”** Restricted evidence and common coordination need an explicit interface.
13. **“A handoff message transfers command.”** The incoming commander must accept and all consumers must be notified.
14. **“Green graphs end the incident.”** Exit requires user recovery, controlled risk, monitoring, and residual ownership.
15. **“Practice proves readiness forever.”** people, services, permissions, vendors, and tools change.

## Worked Examples

### Example 1

**Situation.** A customer-visible outage needs API, database, and network teams.

**Reasoning.** The declarer becomes IC, names an operations lead, assigns three cells with one lead each, freezes unrelated changes, and sets “restore safe checkout without duplicate charges” as the first objective. Communications publishes cadence; planning tracks vendor and handoff needs.

**Conclusion.** Stable objectives and bounded cells turn many experts into a coordinated response.

### Example 2

**Situation.** The database expert is also IC and stops updating state for 20 minutes.

**Reasoning.** Command and technical load exceed one person's capacity. The expert briefs a practiced IC, explicitly transfers command, and becomes database lead. The state document and channel announce the change.

**Conclusion.** Separating command from scarce expertise increases both technical and coordination capacity.

### Example 3

**Situation.** Eight responders report directly to operations; every update interrupts the lead.

**Reasoning.** The lead groups work into traffic, storage, and validation cells, each with a named lead and five-minute exception reporting. Direct reporting falls from eight to three while raw evidence remains linked.

**Conclusion.** Recursive delegation compresses coordination without deleting detail.

### Example 4

**Situation.** One engineer rolls back while another migrates the same database.

**Reasoning.** Both actions were locally plausible but interact. Operations pauses both, restores a known state if safe, records action identifiers and observations, then sequences a bounded rollback before reconsidering migration.

**Conclusion.** A single mutation coordination path prevents a class of self-inflicted compound failures.

### Example 5

**Situation.** A manager orders a destructive repair without a rollback or second operator.

**Reasoning.** The operator invokes stop-the-line policy. The IC restates the objective, requests a reversible containment alternative, and applies required two-person authorization for irreversible work. Organizational rank does not waive technical controls.

**Conclusion.** Command authority remains bounded by safety and professional responsibility.

### Example 6

**Situation.** A new IC receives “things look better” at shift change.

**Reasoning.** The transfer pauses. The outgoing IC briefs impact, severity, objectives, active changes, hypotheses, hazards, communication commitments, resources, and exit tests. The incoming IC reads back, accepts, and the change is sequenced and announced.

**Conclusion.** Command transfer is a state transition, not a casual update.

### Example 7

**Situation.** A vendor and customer each control systems required for recovery.

**Reasoning.** Internal command cannot direct external operators. Liaison records contractual requests, decision deadlines, evidence boundaries, and fallback. If both organizations bear independent authority, they establish shared objectives and escalation while retaining their domains.

**Conclusion.** Coordination across boundaries requires explicit interfaces, not imaginary authority.

### Example 8

**Situation.** A possible credential leak accompanies an availability outage.

**Reasoning.** A restricted security lead owns sensitive evidence and containment duties; the common IC owns user impact, operational objectives, dependencies, and cadence. Sanitized facts and action constraints cross the interface. Broad channels do not receive secrets.

**Conclusion.** Specialized command can preserve confidentiality without fragmenting incident identity.

### Example 9

**Situation.** Proposed mitigation has 30% chance of causing a 100-unit loss and 70% chance of limiting ongoing loss to 10 units.

**Reasoning.** The illustrative conditional expectation is $0.3(100)+0.7(10)=37$ units. Waiting is estimated to lose at least 60 units before the next decision. This favors action under the model, but hard safety constraints, probability uncertainty, reversibility, and alternative actions still govern.

**Conclusion.** Explicit estimates clarify a decision; they do not turn uncertainty into fact or waive constraints.

### Example 10

**Situation.** User indicators recover for five minutes and the room immediately disbands.

**Reasoning.** An active traffic shift has not been reconciled, monitoring has one failed region, customers await updates, and rollback remains open. Command contracts but retains IC, operations, and communications until the stable interval, monitoring, changes, and residual owners satisfy exit criteria.

**Conclusion.** Demobilize progressively from evidence, not relief or silence.

## Cross-Program Connections

- [SARCH-088](../../12-software-engineering-software-architecture/modules/088-federated-decision-making.md) develops durable federated authority; incident command applies temporary bounded delegation under urgency.
- [SEC-089](../../25-security-engineering/ROADMAP.md) owns security-specific communication and legal coordination boundaries.
- [SYSENG-049](../../26-systems-engineering/modules/049-decision-records-and-rationale.md) supplies durable decision-record reasoning for incident decisions.
- [SYSENG-097](../../26-systems-engineering/modules/097-organizations-as-part-of-the-system.md) treats organizations and authority as part of system behavior.
- [PLAT-087](../../29-platform-engineering/modules/087-incident-response-for-shared-platforms.md) applies command interfaces to multi-tenant platform scope.

## References

1. Andrew Stribblehill, “Managing Incidents,” in *Site Reliability Engineering: How Google Runs Production Systems*, O'Reilly Media, 2016. [Official online edition](https://sre.google/sre-book/managing-incidents/). Accessed 2026-09-06.
2. Jennifer Mace et al., “Incident Response,” in *The Site Reliability Workbook*, O'Reilly Media, 2018. [Official online edition](https://sre.google/workbook/incident-response/). Accessed 2026-09-06.
3. Adam Crume et al., “Incident Management Guide,” Google Site Reliability Engineering resources, current online edition. [Official guide](https://sre.google/resources/practices-and-processes/incident-management-guide/). Accessed 2026-09-06.
4. Google Site Reliability Engineering, “Example Incident State Document,” official online appendix, 2015. [Official example](https://sre.google/sre-book/incident-document/). Accessed 2026-09-06.
5. Federal Emergency Management Agency, *National Incident Management System*, Third Edition, October 2017. [Official publication](https://training.fema.gov/EMIWeb/IS/IS700b/Handouts/National_Incident_Management%20System_Third%20Edition_October_2017.pdf). Accessed 2026-09-06.
6. Alexander Nelson, Sanjay Rekhi, Murugiah Souppaya, and Karen Scarfone, *Incident Response Recommendations and Considerations for Cybersecurity Risk Management: A CSF 2.0 Community Profile*, NIST SP 800-61 Revision 3, April 2025. [Official publication](https://csrc.nist.gov/pubs/sp/800/61/r3/final). Accessed 2026-09-06.

Current source-specific claims were checked on 2026-09-06. Role names and example thresholds are adaptable policy, not universal law. Emergency-management concepts are applied by analogy with explicit software-system boundaries; this chapter does not claim affiliation, certification, legal authority, or external review.

## Exercises

### Exercise 1

Distinguish incident command, incident commander, operations, communications, planning, ordinary management, technical ownership, delegation, and unified command.

### Exercise 2

A response has 18 technical responders reporting directly to one operations lead. Design a command graph with a maximum contextual span of five. State the number of first-level cells, ownership rules, and information-loss controls.

### Exercise 3

Design a production-action record and authorization flow for an emergency traffic shift that may overload the destination region. Include stop, rollback, concurrency, and evidence requirements.

### Exercise 4

Compare keeping a sole database expert as IC with transferring command to a trained generalist. Decide roles for an incident involving corruption, customer communication, and vendor recovery.

### Exercise 5

At a cross-company handoff, identity service is unavailable, the outgoing IC is exhausted, the vendor disputes scope, a security investigation is restricted, and graphs recently recovered. Design the transfer, authority model, fallback tooling, and exit decision.

## Answers to the Exercises

### Answer 1

Incident command is the coordination function; the IC owns whole-response objectives, priorities, roles, and state. Operations controls technical work and production mutations. Communications owns verified audience-specific updates. Planning owns future resources, handoffs, restoration, and residual work. Ordinary management persists outside the temporary response and does not automatically determine incident roles. Technical owners retain expertise and safe execution duties. Delegation transfers bounded outcome authority with constraints, reporting, and escalation. Unified command coordinates several legitimate authorities through shared objectives and explicit domains; it is not an unstructured committee.

### Answer 2

Create at least four first-level cells because $\lceil18/5\rceil=4$. For example, traffic, application, data, and validation cells can contain five, five, four, and four responders, each with one lead reporting to operations. Every task has one owner; cross-cell requests pass through leads when priorities or mutations conflict. Leads report objective, observations, actions, risks, and exceptions at a fixed cadence. Raw evidence stays linked, responders can raise stop-the-line concerns directly, and operations may split a cell if complexity—not headcount alone—overloads its lead. The maximum of five is a local exercise constraint, not universal doctrine.

### Answer 3

Record action ID, owner, objective, source and destination scope, current loads, capacity margin, dependencies, preconditions, expected user evidence, risk, start deadline, stop thresholds, rollback command, approver, second operator where required, timestamps, and result. Operations checks no conflicting change is active and reserves destination capacity. Shift a bounded fraction first; compare source and destination SLIs plus saturation through an independent path. Stop on destination threshold, new integrity errors, or lost observability. Roll back using the pretested route. The IC approves objective and cross-cutting risk; the qualified operator validates execution safety and may refuse unsafe work.

### Answer 4

Transfer IC to the trained generalist so the scarce database expert leads data operations. The IC maintains corruption impact, priorities, role boundaries, customer and vendor interfaces, and evidence constraints. Data operations stops harmful writes, protects copies, and evaluates recovery. Communications owns verified customer cadence. A vendor liaison tracks entitlement, requests, evidence, and deadlines. Security or legal specialists join if corruption may involve tampering or regulated data. The expert can advise command but should not simultaneously coordinate the whole response, execute recovery, and answer stakeholders.

### Answer 5

Use the tested out-of-band command post and contact tree rather than the failed identity service. The outgoing IC gives a concise verbal and durable briefing from an accessible replicated state record; the incoming IC reads back and explicitly accepts before the outgoing IC rests. Announce the sequenced transfer on every working channel and reconcile stale role displays later. Establish unified objectives with the vendor only if it has independent operational authority; otherwise use liaison and contract escalation while internal command retains user accountability. Security keeps restricted evidence in its authorized cell and shares sanitized impact, constraints, and required actions. Recent graph recovery is provisional because identity and monitoring dependencies are impaired. Maintain command until independent user evidence holds for the exit interval, active changes are reconciled, security and vendor interfaces have owners, communications are complete, and re-escalation triggers are tested.
