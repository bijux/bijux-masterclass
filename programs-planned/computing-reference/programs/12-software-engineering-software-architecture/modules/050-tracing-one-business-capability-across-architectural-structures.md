---
module_id: SARCH-050
program: Software Engineering: Software Architecture
level: 1
module_number: 50
title: Tracing One Business Capability Across Architectural Structures
status: complete
last_verified: 2026-09-06
---

# Tracing One Business Capability Across Architectural Structures

## One-Page Review

### Governing question

How can an architect trace one business capability from stakeholder intent through code, runtime interactions, data, deployment, integration, security, operation, and evidence so that separate architectural views describe one coherent system rather than unrelated diagrams?

### Essential definitions

- A **business capability** is an enduring ability the organization or system must provide, independent of one workflow screen or component.
- A **capability thread** is a bounded end-to-end trace of one capability through concerns, decisions, structures, state transitions, failure, operation, and evidence.
- An **obligation** is a required behavior, quality, policy, or constraint that the thread must preserve.
- A **trace link** states a justified relationship between artifacts, such as an obligation realized by a component or an invariant enforced by a data authority.
- **horizontal traceability** connects peer views at the same abstraction level; **vertical traceability** connects intent to implementation and evidence.
- A **view** is a representation of a system from a viewpoint for particular concerns; no single view is the architecture.
- A **realization element** is a module, runtime component, data structure, deployable, identity, operational procedure, or control that helps satisfy an obligation.
- A **handoff** transfers data, control, authority, or responsibility across a boundary.
- A **terminal outcome** is success, explicit rejection, cancellation, timeout with known disposition, or another state a caller and operator can distinguish.
- **trace debt** is missing, stale, ambiguous, or contradictory linkage that prevents reliable change or diagnosis.

### Central model, mechanism, or theorem

Model a capability thread as typed graph $G_t=(V,E,\tau)$. Vertices include stakeholders, scenarios, obligations, decisions, modules, runtime components, data authorities, messages, deployables, identities, controls, operational actions, and evidence. Edge type $\tau(e)$ explains the relation: motivates, realizes, invokes, reads, writes, emits, deploys-as, authorizes, observes, recovers, or contradicts.

For obligations $O$ with risk weights $w_i>0$, a review aid is

$$
C_w=\frac{\sum_i w_i I_i}{\sum_i w_i},
$$

where $I_i=1$ only when obligation $i$ has an accepted realization and evidence path. Coverage reveals omissions; it does not prove correctness, adequate quality, or valid weights.

### Critical invariants

- begin with a named actor, trigger, outcome, scope, and quality scenario;
- state business invariants and authority before assigning components;
- every view uses stable element identities and an explicit legend;
- every handoff names payload, semantics, owner, trust, timeout, retry, duplicate, ordering, and failure behavior as applicable;
- every state mutation has one authority, durable identity, concurrency rule, and recovery meaning;
- runtime, data, code, deployment, ownership, and security boundaries are distinguished;
- happy path, rejection, partial failure, duplicate, timeout, recovery, and manual operation are traced;
- asynchronous acceptance is not reported as business completion;
- artifact, configuration, secret, flag, and topology revisions remain distinct;
- quality claims connect to mechanisms and measurable evidence;
- contradictions between views are defects to resolve, not documentation preferences;
- links are updated or removed when the realized system changes;
- the trace remains chapter-sized and decision-oriented, not an inventory of everything;
- review coverage never substitutes for technical, operational, or stakeholder validation.

### Common failures

Common failures include starting from a diagram instead of an obligation; naming one component “refund service” and declaring the capability traced; omitting declined and unknown outcomes; drawing calls without authority or state semantics; assigning one database to multiple writers; showing modules that do not map to runtime or deployment; hiding a queue behind a synchronous success response; treating logs as evidence without outcome identifiers; ignoring manual repair; using different names for the same element across views; copying one diagram for every audience; counting trace links without checking meaning; and leaving the trace unchanged after architecture evolution.

### Compact example

For “issue an authorized refund,” the customer or agent triggers a request with order, amount, reason, and idempotency key. Policy decides eligibility; the refund authority creates one durable refund identity and reserves against the refundable balance; a payment adapter sends an idempotent provider request; a ledger authority records financial effect; an event informs notification and analytics. A timeout after provider submission becomes `provider_outcome_unknown`, not success or automatic retry. Deployment, identity, configuration, observability, reconciliation, and operator repair all link back to that outcome model.

### Connections

[SARCH-021](021-context-views.md) through [SARCH-030](030-creating-an-architecture-description-for-different-audiences.md) supply view construction; [SARCH-041](041-system-of-record-boundaries.md) through [SARCH-049](049-configuration-and-environment-topology.md) supply state, integration, deployment, and configuration structures. [SARCH-051](../ROADMAP.md) next treats partial failure as an architectural constraint.

## Governing Question

Architecture descriptions divide complexity into views. A context view shows actors and external systems. Module, runtime, data, deployment, and operational views answer different questions. Division is necessary, but it creates a risk: each view can be locally plausible while their combined story is impossible.

A capability thread tests coherence by following one valuable outcome through every structure it depends on. The objective is not maximum documentation. It is enough connected evidence to explain behavior, quality, ownership, failure, and change from end to end.

## Why This Matters

Stakeholders experience capabilities, not diagrams. A customer asks whether a refund happened. Finance asks whether the ledger balances. Security asks who authorized it. Operations asks how to recover an unknown provider outcome. Developers ask which module owns the invariant. A release engineer asks which deployables and configuration revisions were active.

When these answers cannot be connected, change becomes hazardous. A team alters an API without finding a batch reconciler. A queue improves availability but changes the meaning of acceptance. A database migration breaks rollback. An incident has thousands of logs but no durable outcome identity.

Tracing one capability exposes such gaps at manageable scale. It is a review method, communication device, and change-impact map. It is not a substitute for system-wide threat modeling, performance testing, or complete architecture evaluation.

## Prerequisites and Retrieval

Retrieve stakeholder, concern, quality attribute scenario, invariant, module, component, connector, process, deployment node, data authority, schema, API, message, identity, trust boundary, idempotency, timeout, retry, observability, recovery, artifact, configuration, and evidence.

From SARCH-003 through SARCH-010 retrieve context, drivers, constraints, decisions, and framing; SARCH-021 through SARCH-030 provide architectural views; SARCH-031 through SARCH-040 provide style forces; and SARCH-041 through SARCH-049 provide data, integration, edge, cache, deployment, and environment consequences.

## Learning Objectives

After completing this module, you should be able to:

1. scope a capability thread by actor, trigger, outcome, and quality scenario;
2. state obligations and invariants before selecting realization elements;
3. connect context, module, runtime, data, deployment, and operational views with stable identities;
4. trace authority and state across synchronous, asynchronous, batch, and external handoffs;
5. distinguish acceptance, progress, terminal outcome, evidence, and recovery;
6. expose security, privacy, configuration, and deployment assumptions along the thread;
7. trace normal, rejected, duplicate, delayed, partially failed, and repaired paths;
8. use weighted coverage as an omission signal without mistaking it for proof;
9. detect contradictions and stale links across views;
10. produce a bounded capability narrative useful to stakeholders, implementers, reviewers, and operators.

## Core Exposition

**Choose one enduring capability.** Prefer a business ability such as issuing a refund, admitting a patient, allocating inventory, or dispatching a crew. A screen, endpoint, database table, or service name is an implementation surface, not necessarily the capability.

Bound the thread. Name initiating actors, trigger, input, successful outcome, rejected outcomes, systems of interest, and excluded adjacent work. “Issue a refund” may include authorization, payment, ledger, notification, and reconciliation while excluding original order fulfillment and general accounting close.

**Start with stakeholder obligations.** Capture business result, quality scenarios, policy, compliance, and operational needs. For refunding: never exceed refundable balance; one approved intent produces at most one financial effect; authorized roles and reason rules apply; the caller learns a durable disposition; provider ambiguity is reconciled; evidence supports dispute and audit.

Obligations should be testable or reviewable. “Secure and reliable” is too vague. State stimulus, context, expected response, and measure: for example, after an operator submits during provider timeout, the system returns a durable refund ID within two seconds and reaches a reconciled terminal state within the declared objective without duplicating payment.

**State authority and invariants before components.** Decide what facts exist and who may establish them. The order authority owns paid and refundable amount. The refund authority owns refund lifecycle. The ledger owns accounting entries. The external provider owns its payment execution result, although the system must maintain its own evidence.

An invariant spanning authorities needs a protocol, not a shared adjective. Preventing excess refund may require reservation against the order balance, serialized decisions, or a compensating policy. A diagram with two services both writing `refunded_amount` leaves authority ambiguous.

**Give every element stable identity.** Use one identifier and meaning across views: `refund-api`, `refund-domain`, `refund-store`, `payment-adapter`, `refund-worker`, `ledger-api`. A module and runtime component may share a stem but should not be silently conflated.

Keep a small element dictionary: identifier, type, owner, responsibility, authoritative data, deployable, and critical dependencies. View-specific aliases are allowed only with explicit mapping. Stable identity makes contradictions discoverable.

**Trace the context boundary.** Identify customers, support agents, finance operators, payment providers, identity providers, ledger, notification, and analytics. For each crossing, state business purpose, data classification, initiating direction, and trust assumption.

Context views should not expose internal sequence detail. Their job is to reveal actors, external authority, data exchange, and responsibility. An external payment provider is not a subordinate component simply because an arrow points to it.

**Trace code structure.** Map obligations to modules and public interfaces. Policy evaluation, lifecycle transitions, provider adaptation, persistence, and evidence formatting should have clear ownership. Dependency direction should protect domain rules from provider and framework volatility.

A code module realizes only part of the capability. Record which runtime component loads it and which artifact contains it. Otherwise a clean module diagram can hide a single process, duplicated library policy, or unexpected deployment coupling.

**Trace runtime interaction.** Begin from trigger and enumerate messages, calls, decisions, state transitions, and terminal outcomes. Include correlation and idempotency identities. State what each response means.

A `202 Accepted` response means durable acceptance only if the request was durably recorded. It does not mean the provider paid or the ledger posted. A `200` from an adapter does not establish end-to-end success if a later commit can fail. Each boundary needs a precise success vocabulary.

**Trace adverse paths, not only the sequence diagram's center.** Include invalid request, unauthorized actor, ineligible order, duplicate submission, concurrency conflict, provider decline, timeout before send, timeout after send, duplicate provider callback, ledger rejection, queue delay, worker crash, and recovery.

Unknown outcome is a first-class state when an external side effect may have occurred but acknowledgement was lost. Blind retry can duplicate effects. Query by idempotency identity, reconcile provider records, and expose bounded operator action.

**Trace data structure and lifecycle.** Identify entities, records, events, retention, classification, lineage, and authority. A refund record should distinguish intent, authorization, reservation, provider attempt, provider outcome, ledger reference, terminal state, and repair history.

Define legal transitions and concurrency control. Retained events and batch exports can outlive runtime versions. Privacy deletion may remove customer attributes while financial evidence must remain under policy. Backups and restoration are part of the data path when they affect recovery.

**Trace integration semantics.** Choose synchronous calls for immediate decisions when the caller needs bounded response. Use asynchronous work for decoupling and durable progress, but expose acceptance separately from completion. Use batch for reconciliation when latency permits and independent recomputation is valuable.

For every handoff, record payload schema, semantic meaning, ownership, authentication, authorization, deadline, retry, idempotency, ordering, duplicate handling, compatibility, and observability. Transport choice does not supply these properties automatically.

**Trace deployment and release.** Map runtime components to immutable artifacts, deployment units, regions, zones, and failure domains. Identify which changes can release independently and which compatibility windows are required.

If `refund-api` and `refund-worker` read the same lifecycle records, rolling one independently requires compatible state and message schemas. A separate pipeline is insufficient. State migration, rollback, and retained-message behavior belong in the thread.

**Trace configuration and secrets.** Record the non-secret revisions that select provider endpoint, timeout, retry budget, queue, currency policy, and feature activation. Record opaque secret versions and workload identities without values.

Configuration can change behavior without a new artifact. The incident reconstruction key therefore includes artifact, configuration, secret version, flags, and topology. A test performed under one tuple does not automatically cover another.

**Trace security and privacy.** Identify principals, authentication, authorization decisions, separation of duties, data classification, minimization, encryption boundaries, audit, and abuse cases. A support agent may request a refund but require supervisor approval above a threshold.

Protect idempotency and correlation identifiers from becoming authorization tokens. Validate amount and order ownership at the authoritative boundary. Consider insider abuse, replay, provider impersonation, evidence tampering, and excessive data exposure to notification or analytics.

**Trace operational ownership.** Assign owners for APIs, queues, stores, provider integration, ledger contract, configuration, and incident decisions. Define signals for accepted, pending, declined, unknown, posted, repaired, duplicated, and aged work.

Runbooks should use durable identities and state, not guesses from log timestamps. Include safe pause, traffic containment, provider query, replay rules, reconciliation, repair authorization, and stakeholder communication. Manual work is part of the architecture when automation cannot safely conclude.

**Connect quality claims to evidence.** Availability mechanisms might include durable acceptance, queueing, regional redundancy, and degraded reads. Performance mechanisms include bounded synchronous work and capacity. Security mechanisms include workload identity and authorization. Modifiability mechanisms include owned contracts and compatible deployment.

For each claim, state measurement and limitations. Queue age measures delay, not financial correctness. Error rate can be low while refunds post twice. Reconciliation and ledger invariants supply different evidence.

**Use trace matrices selectively.** A matrix from obligations to realization and evidence exposes empty rows and overcentralized columns. Weighted coverage can prioritize review, but weights are judgments and binary links can be shallow.

Review link meaning. An obligation linked to “logs” is incomplete unless logs contain durable identity, protected fields, retention, queryability, and a process that reaches a conclusion. One mechanism may serve several obligations, creating a concentration risk worth examining.

**Check cross-view consistency.** Ask whether every runtime component maps to code and deployment; every write maps to an authority and schema; every external actor appears in trust analysis; every deployable has identity and configuration; every failure has an observable state and owner; every operational action respects domain invariants.

Contradictions are findings. If a runtime view shows direct provider access while a security view requires all payment egress through a gateway, resolve the architecture or the view. Do not preserve both as audience-specific simplifications without an explicit abstraction relation.

**Trace change impact.** When an obligation, schema, provider, deployable, or policy changes, traverse its typed links. Changing currency representation may affect API, lifecycle invariant, store, messages, ledger, exports, configuration, compatibility, and repair tools.

Graph reachability suggests candidates, not complete impact. Dynamic discovery, undocumented consumers, organizational process, and emergent behavior can remain. Combine trace links with repository search, runtime telemetry, owner review, and tests.

**Calibrate depth to risk.** A low-risk display preference may need a short thread. Financial, clinical, or safety capabilities require more explicit authority, failure, security, evidence, and manual recovery. The method scales by selecting relevant obligations, not by copying a universal checklist verbatim.

Stop when the trace answers the governing concerns and has explicit boundaries. Do not turn one thread into a disguised design for the entire enterprise. Adjacent capabilities should be linked as dependencies with their own owners.

**Keep traces current.** Store durable architecture descriptions near their owners, version them, and review them when contracts, deployment, authority, or recovery change. Automated checks can validate links and identifiers, but semantic currency needs accountable review.

Trace debt is operational risk. Remove dead elements, repair ambiguous links, and record unresolved uncertainty. A smaller truthful trace is more valuable than a comprehensive-looking stale one.

## Definitions and Notation

Let:

- $O=\{o_1,\ldots,o_n\}$ be capability obligations;
- $w_i>0$ be the review-assigned risk weight of obligation $o_i$;
- $I_i\in\{0,1\}$ indicate whether reviewers accept a realization and evidence path for $o_i$;
- $G_t=(V,E,\tau)$ be a directed typed trace graph;
- $\tau(e)$ be the declared semantic type of edge $e$;
- $R(v)$ be vertices reachable from a changed vertex $v$ through selected edge types;
- **scenario** mean an actor or condition applying a stimulus in a context and expecting a measurable response;
- **business invariant** mean a property that must hold across allowed domain state transitions;
- **authority** mean the component or institution permitted to establish a fact;
- **realization** mean a mechanism or structure that contributes to an obligation;
- **evidence path** mean the observations and review procedure used to judge an obligation;
- **capability slice** mean the explicitly included actors, outcomes, structures, and failures for one thread.

$C_w$ is undefined if no obligations or positive weights exist. It is a coverage signal only: $C_w=1$ can coexist with incorrect mechanisms, weak evidence, missing obligations, correlated failures, or biased weights.

## Mechanisms, Invariants, or Proof Structure

### Capability-thread procedure

1. Name the capability, actors, trigger, successful and rejected outcomes, boundary, and exclusions.
2. State functional, quality, policy, security, privacy, and operational obligations.
3. Define authoritative facts, business invariants, identities, and state transitions.
4. Create stable identifiers for context, code, runtime, data, deployment, and operational elements.
5. Trace the normal path and label every handoff's semantics.
6. Trace rejection, duplicate, concurrency, timeout, partial failure, recovery, and manual paths.
7. Map each runtime element to module, artifact, deployable, identity, configuration, and owner.
8. Map every mutation to authority, storage, concurrency, retention, migration, and evidence.
9. Map obligations to mechanisms and evidence; calculate coverage only as an omission aid.
10. Resolve contradictions, record uncertainty, review with affected owners, and version the trace.

### Refund invariants

- total reserved plus completed refund for an order never exceeds its authorized refundable balance;
- one approved refund identity produces at most one intended external financial effect;
- terminal state is monotonic unless an explicit repair transition records authority and reason;
- provider outcome and ledger posting remain distinguishable facts;
- every externally visible disposition refers to a durable refund identity;
- an unknown provider outcome prevents blind resubmission under a new identity;
- manual repair preserves original intent, evidence, and separation of duties.

### Cross-view consistency checks

- **context to runtime:** every external interaction has a runtime connector and owner;
- **runtime to data:** every read or write names data authority and consistency assumption;
- **runtime to module:** every responsibility is implemented by an owned module or declared external system;
- **runtime to deployment:** every process maps to an artifact, node class, identity, and failure domain;
- **deployment to configuration:** every deployable has compatible configuration, secret, and topology revisions;
- **obligation to evidence:** every quality or policy claim has a mechanism, observation, and decision rule;
- **failure to operation:** every nonterminal or ambiguous state has detection, owner, bounded action, and escalation.

### Weighted coverage example

Suppose six obligations have weights $5,5,4,4,3,2$. Accepted evidence exists for all except one weight-5 obligation. Then covered weight is $18$, total weight is $23$, and $C_w=18/23\approx0.7826$. The number highlights a high-risk omission; it does not imply the capability is “78.26% correct.”

## Alternatives and Trade-Offs

| Choice | Benefit | Cost or risk | Suitable use |
|---|---|---|---|
| narrative thread | accessible causal story | omissions can hide in prose | stakeholder and onboarding review |
| typed graph | reachability and consistency queries | modeling and maintenance cost | complex or high-change capability |
| obligation matrix | exposes empty rows | shallow links can inflate coverage | review preparation |
| sequence view | precise temporal path | weak on ownership and deployment | runtime and failure reasoning |
| data lifecycle view | authority and retention clarity | weak on user interaction | state-heavy capability |
| deployment overlay | failure and release visibility | can obscure domain meaning | operational and rollout review |
| one end-to-end owner | clear accountability | overload or centralization | coherent bounded capability |
| federated owners | specialist autonomy | handoff and escalation complexity | capabilities spanning strong authorities |
| generated links | catches structural drift | cannot judge semantics | stable identifiers and repository checks |
| manual review | contextual judgment | variable and costly | invariants, evidence, and trade-offs |

Use several compact representations when concerns differ. Do not force every stakeholder to consume one overloaded diagram.

## Failure Modes and Misconceptions

1. **“The service named after the capability owns the whole capability.”** External authorities, data, operations, and teams still participate.
2. **“A happy-path sequence is an end-to-end trace.”** Rejection, ambiguity, repair, deployment, and evidence remain absent.
3. **“Every arrow means the same thing.”** Calls, events, reads, authority, ownership, and deployment require typed semantics.
4. **“One database guarantees invariants.”** Multiple writers and ambiguous transactions can still violate them.
5. **“Asynchronous acceptance is success.”** Durable intent, provider execution, ledger posting, and notification are different states.
6. **“Timeout means failure.”** The remote effect may have occurred; unknown is distinct from rejected.
7. **“Retries provide reliability.”** Non-idempotent or newly identified retries can duplicate effects.
8. **“Logs prove the outcome.”** Missing identity, tampering, sampling, retention, or unobserved effects can defeat the claim.
9. **“A module view maps directly to deployment.”** modules, processes, artifacts, and deployables are different structures.
10. **“Separate deployables are independently releasable.”** Shared schemas and incompatible state can force lockstep.
11. **“Security is one box beside the flow.”** identity, authorization, minimization, integrity, and abuse constraints cross every handoff.
12. **“Operations begin after design.”** detection, recovery, reconciliation, and manual authority shape state and interfaces.
13. **“Full coverage proves quality.”** accepted links can be wrong and obligations or evidence can be incomplete.
14. **“Reachability gives complete change impact.”** undocumented and dynamic dependencies remain.
15. **“Different views may contradict because they serve different audiences.”** abstraction may differ, but shared facts cannot conflict silently.
16. **“Once documented, a trace remains true.”** architecture, policy, ownership, providers, and recovery procedures evolve.

## Worked Examples

### Example 1

**Situation.** Scope a thread for issuing a refund.

**Reasoning.** Actor is customer or authorized agent; trigger is an eligible refund request; success is a durable terminal refund plus ledger reference. Rejections include unauthorized, ineligible, invalid amount, and policy denial. Include refund lifecycle, payment execution, ledger, notification, reconciliation, and audit. Exclude original fulfillment and general ledger close. Add latency, no-duplicate-effect, recovery, and evidence scenarios.

**Conclusion.** A precise boundary makes end-to-end reasoning possible without modeling the entire commerce system.

### Example 2

**Situation.** Two agents concurrently request refunds of 70 monetary units against a refundable balance of 100.

**Reasoning.** Independent read-then-write decisions can approve 140 units. The order or refund authority must serialize reservation, use conditional update, or apply an equivalent invariant-preserving protocol. One request reserves 70; the other sees 30 remaining and is rejected or reduced under policy. Ledger and provider calls occur only after reservation identity exists.

**Conclusion.** Tracing authority exposes a concurrency invariant that component naming alone hides.

### Example 3

**Situation.** The API records a refund and returns `202 Accepted` before worker execution.

**Reasoning.** The response means durable intent accepted under refund ID, not money returned. Status exposes `pending`, `provider_unknown`, `declined`, `posted`, or another terminal disposition. Notification must not say “refunded” at acceptance. Queue and worker evidence connects intent to eventual outcome.

**Conclusion.** Response semantics must align with the actual state reached in the runtime trace.

### Example 4

**Situation.** A provider times out after receiving a refund command.

**Reasoning.** The effect may exist. Record attempt identity and state `provider_outcome_unknown`; do not issue a new provider identity. Query or reconcile using the original idempotency key. If the provider confirms success, continue ledger posting; if confirmed absent, retry under the same identity where supported. Escalate unresolved cases.

**Conclusion.** Unknown outcome is a designed state with reconciliation, not a generic error.

### Example 5

**Situation.** A runtime diagram lets both refund worker and support tool update refund status directly.

**Reasoning.** The data view must identify one authority. Route support action through an authorized repair command that validates current state, separation of duties, and allowed transition. Record original and repaired facts. The tool may read a projection but does not gain write authority from database connectivity.

**Conclusion.** Cross-view checking turns ambiguous multiple writers into an explicit controlled protocol.

### Example 6

**Situation.** Designers choose a queue between API and provider worker.

**Reasoning.** Queueing permits durable acceptance and load leveling, but adds delay, duplicates, ordering questions, poison records, replay, and operational ownership. Persist intent and outbox transition atomically or reconcile gaps. Define age objectives, idempotent consumption, dead-letter policy, and status semantics.

**Conclusion.** An asynchronous connector changes the capability contract and recovery model, not just performance.

### Example 7

**Situation.** Refund API and worker deploy independently while sharing lifecycle records.

**Reasoning.** Map each to artifact, identity, configuration, and schema versions. Expand schema before either depends on new fields; make readers tolerate mixed revisions; retain old message handling through rollback; stage provider configuration separately. Test API-new/worker-old and API-old/worker-new paths.

**Conclusion.** The deployment view validates whether claimed release independence survives shared state.

### Example 8

**Situation.** Six obligations have weights $5,5,4,4,3,2$; one weight-5 security obligation lacks accepted evidence.

**Reasoning.** Total is $23$ and covered weight is $18$, so $C_w=18/23\approx0.7826$. More importantly, the absent row is high risk. Review the missing authorization mechanism and evidence before release. Do not average it away with many low-weight links or call the system 78.26% safe.

**Conclusion.** Weighted coverage prioritizes omissions but is not a correctness score.

### Example 9

**Situation.** A support agent reuses another customer's refund ID to query status.

**Reasoning.** A durable identifier supports correlation but does not authorize access. The API authenticates the principal, checks role, case assignment or customer ownership, and field-level disclosure. Audit records purpose and decision. Notification and analytics receive minimized data, not full payment evidence.

**Conclusion.** Identity that connects a trace must not become a bearer capability accidentally.

### Example 10

**Situation.** Finance finds provider refunds absent from the internal ledger after a regional incident.

**Reasoning.** Reconciliation joins provider effect identity, refund lifecycle, queue history, and ledger reference. Operators pause unsafe replay, classify confirmed provider success with missing ledger post, and submit an authorized idempotent repair. Evidence records actor, old state, provider proof, ledger result, artifact/configuration context, and customer communication.

**Conclusion.** Operational recovery completes the capability thread when automation loses continuity.

## Cross-Program Connections

- **Software Design and Domain Modeling:** owns aggregates, policies, domain events, and code-level invariant realization.
- **Software Engineering Patterns:** supplies code and interaction patterns without owning capability-level architecture.
- **Software Delivery and Reliability Engineering:** owns rollout, telemetry, incident response, and delivery mechanics in depth.
- **API and Service Engineering:** owns endpoint semantics, idempotency, compatibility, authentication, and client contracts.
- **Database Engineering:** owns transactions, concurrency, schema migration, durability, and recovery mechanics.
- **Data Architecture Engineering:** owns lineage, governance, analytical use, and enterprise information relationships.
- **Security Engineering:** owns threat modeling, authorization, cryptography, audit protection, and abuse resistance.
- **Distributed Systems Engineering:** owns partial failure, messaging, consistency, replication, and recovery protocols.
- **Systems Engineering:** extends traceability across hardware, people, procedures, physical environment, and lifecycle assurance.

## References

1. Len Bass, Paul Clements, and Rick Kazman, *Software Architecture in Practice*, 4th ed., Addison-Wesley, 2021.
2. ISO/IEC/IEEE, *42010:2022 Software, systems and enterprise—Architecture description*, 2nd ed., November 2022. <https://www.iso.org/standard/74393.html>
3. Nick Rozanski and Eóin Woods, *Software Systems Architecture*, 2nd ed., Addison-Wesley, 2011.
4. Simon Brown, “The C4 model for visualising software architecture,” current web edition, retrieved 2026-09-06. <https://c4model.com/>
5. Eric Evans, *Domain-Driven Design*, Addison-Wesley, 2003.
6. David Lorge Parnas, “On the Criteria To Be Used in Decomposing Systems into Modules,” *Communications of the ACM* 15(12), 1972. <https://doi.org/10.1145/361598.361623>
7. NIST, *Systems Security Engineering: Considerations for a Multidisciplinary Approach in the Engineering of Trustworthy Secure Systems*, SP 800-160 Vol. 1 Rev. 1, November 2022. <https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final>
8. Matthew Skelton and Manuel Pais, *Team Topologies: Organizing Business and Technology for Fast Flow of Value*, 2nd ed., IT Revolution, 2025. <https://itrevolution.com/product/team-topologies/>

## Exercises

### Exercise 1

Define business capability, capability thread, obligation, trace link, horizontal traceability, vertical traceability, view, realization element, handoff, terminal outcome, trace debt, authority, and evidence path.

### Exercise 2

Seven obligations have weights $6,5,5,4,3,2,1$. Accepted realization and evidence exist for all except one weight-5 obligation and the weight-2 obligation. Compute weighted coverage, state the uncovered weight, and explain why the result is not a quality percentage.

### Exercise 3

Diagnose a food-delivery cancellation flow that returns success after publishing a message, lets the app and courier service both update cancellation state, retries a restaurant charge reversal with a new identifier after timeout, and has no reconciliation owner. Produce the minimum corrected authority, states, handoff semantics, and recovery path.

### Exercise 4

Compare narrative, typed graph, trace matrix, runtime sequence, and data-lifecycle representations for reviewing a regulated insurance-claim approval capability. Choose a combination and define consistency checks, owners, evidence, and maintenance triggers.

### Exercise 5

Trace the capability “recall and prevent use of a contaminated medicine lot” across manufacturer, regulator, distributor, pharmacy, hospital, prescribing system, patient communication, and offline clinical operation. Cover scope, obligations, authority, identities, runtime and batch paths, data, deployment, configuration, security, privacy, partial failure, evidence, reconciliation, manual authority, and recovery.

## Answers to the Exercises

### Answer 1

A **business capability** is an enduring organizational or system ability. A **capability thread** is its bounded end-to-end trace across concerns, structures, failure, and evidence. An **obligation** is required behavior, quality, policy, or constraint. A **trace link** is a justified relationship between artifacts. **Horizontal traceability** connects peer views; **vertical traceability** connects intent to realization and evidence. A **view** represents the system for selected concerns. A **realization element** is a module, component, store, deployable, control, procedure, or other mechanism. A **handoff** transfers data, control, authority, or responsibility. A **terminal outcome** is a distinguishable final disposition. **Trace debt** is missing, stale, ambiguous, or contradictory linkage. **Authority** may establish a fact. An **evidence path** connects observations and review procedure to an obligation.

### Answer 2

Total weight is $6+5+5+4+3+2+1=26$. Uncovered weight is $5+2=7$, so covered weight is $19$ and $C_w=19/26\approx0.7308$, or 73.08% as a coverage calculation. It is not a quality percentage because weights are judgments, obligations may be missing, accepted links may be weak or wrong, failures may correlate, and binary indicators ignore mechanism and evidence strength. The weight-5 gap deserves explicit review rather than being hidden by the aggregate.

### Answer 3

Publishing establishes at most durable cancellation intent, so return an ID and `accepted`, not completed cancellation. One order or cancellation authority owns states such as `requested`, `courier_release_pending`, `restaurant_reversal_unknown`, `reconciled`, `cancelled`, and `rejected`; app and courier submit commands rather than writing state. Each message carries cancellation identity, order identity, schema, and idempotency key. A timeout after charge-reversal submission becomes unknown; query or reconcile under the original provider identity and never create a blind duplicate. Define reservation and compensation rules for courier and restaurant, observable queue age and unknown outcomes, an owner and deadline for reconciliation, authorized repair transitions, and customer wording that matches actual disposition.

### Answer 4

Use a short narrative for stakeholder intent and exclusions, a typed graph for obligations, authorities, owners, and reachability, runtime sequences for approval and adverse paths, a data lifecycle for evidence and retention, and a matrix to expose uncovered obligations. Stable element IDs connect all forms. Check that every external party has a trust boundary; every runtime write has one authority; every decision maps to policy version and evidence; every component maps to module, deployable, identity, and owner; and every unknown state has recovery. Legal, claims, security, operations, and engineering owners review their links. Re-review on policy, provider, schema, authority, deployment, retention, threat, or recovery change. Generated link checks support but do not replace semantic review.

### Answer 5

Scope the capability from a regulator or manufacturer declaring a lot recall through preventing dispense or administration and reconciling exposed inventory and patients. The regulator and manufacturer own distinct recall facts; a governed recall authority creates a durable recall ID, affected product and lot identities, severity, scope, issue time, effective time, supersession, and evidence. Distributors, pharmacies, hospitals, and prescribing systems ingest authenticated versioned notices through real-time and batch paths, deduplicate by recall identity, and retain last-known-good lists for offline operation under explicit freshness limits.

Inventory and clinical authorities map local stock and administrations to canonical lot identity. Runtime checks block or warn according to current clinical policy; asynchronous notification is not proof that stock was quarantined or a patient contacted. Deployment views map gateway, decision, inventory, and notification components to artifacts and failure domains; configuration identifies policy and routing revisions, while secret versions and workload identities remain protected. Authorization, separation of duties, minimized patient data, audit integrity, and anti-forgery controls cross every handoff.

Trace delayed notice, unknown lot mapping, duplicate or withdrawn recall, network partition, old software, clock error, failed barcode scan, patient unreachable, and emergency use when alternatives are unavailable. Effective-state evidence records which sites and devices loaded which revision, blocked actions, remaining inventory, exposures, acknowledgements, and stale nodes. Reconciliation compares manufacturer shipments, distributor movement, local inventory, dispensing, administration, returns, and destruction. Local clinical leadership has bounded documented manual authority during disconnection; reconnection preserves newer legitimate local decisions, resolves conflicts by authority and scope, and escalates unresolved exposure. Recovery tests cold bootstrap, corrupt package, authority outage, backup restoration, and manual operation. Full credit requires distinguishing notice delivery, prevention, quarantine, patient response, and final reconciliation rather than calling message publication “recall complete.”
