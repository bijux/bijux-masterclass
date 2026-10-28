---
module_id: SEPAT-087
program: Software Engineering: Patterns
level: 2
module_number: 87
title: Saga
status: complete
last_verified: 2026-08-29
---

# Saga

## One-Page Review

### Governing question

How can one business intent make durable progress across independently owned transactional boundaries, recover from partial failure, and expose unresolved outcomes without pretending that the whole distributed operation has atomic rollback or isolation?

### Essential definitions

- A **saga** is a long-lived transaction decomposed into a sequence or dependency graph of local transactions, with durable coordination and application-defined recovery.
- A **local transaction** atomically changes state inside one participant's consistency boundary.
- A **compensating transaction** is a new authorized business action that semantically offsets a committed action; it is not time reversal or physical database rollback.
- **forward recovery** retries or chooses another forward action until the intent can finish.
- **backward recovery** executes compensations toward an acceptable alternative terminal state.
- A **saga instance** is one durable execution identified independently of messages and attempts.
- A **step/effect identity** is a stable idempotency key for one logical participant effect across retries.
- **orchestration** gives a durable coordinator explicit workflow state and command decisions; **choreography** distributes progress through participant events.
- A **pivot** is a domain-specific point after which backward recovery is no longer the intended strategy; later steps must normally be retriable or escalated.
- A **semantic lock** is a domain-visible pending/reserved state that constrains conflicting work without holding a global database lock.
- An **ambiguous outcome** means the caller cannot tell whether a participant committed, commonly after a lost response.

### Central model, mechanism, or theorem

For a sequential saga

$$
S = T_1;T_2;\ldots;T_n,
$$

each $T_i$ commits locally. If progress fails after $T_k$, one possible backward-recovery path is

$$
C_{k};C_{k-1};\ldots;C_1,
$$

where each $C_i$ semantically compensates $T_i$. This notation is a protocol plan, not an atomicity theorem: other transactions can observe intermediate states; $C_i$ can fail; some effects are irreversible; and dependency order, not wall-clock completion, governs parallel compensation. Correctness therefore comes from explicit invariants, durable state transitions, stable effect identities, idempotent participants, isolation countermeasures, reconciliation, and truthful terminal states.

### Critical invariants

- Every participant owns and atomically validates its local state; no coordinator writes participant databases directly.
- Saga, step, attempt, message, and effect identities are distinct and durably related.
- A participant applies at most one logical effect per stable effect identity, even when delivery is repeated.
- Coordinator transition and required outgoing intent are not separated by an unrecorded crash window; a transactional outbox or equivalent durable handoff closes it.
- State distinguishes not-started, dispatched, committed, failed, outcome-unknown, compensating, compensated, and manual-review conditions.
- Compensation records its preconditions, authority, deadline, dependency order, result, and residual effect.
- Timeout, cancellation, and missing acknowledgement never prove that an issued effect did not commit.
- Concurrent sagas preserve named business invariants through reservation, version checks, escrow, commutativity, reread/revalidation, or another explicit countermeasure.
- Stale coordinators and workers are fenced by generation/epoch where concurrent ownership could corrupt progress.
- Every saga eventually reaches a defined terminal state or an owned, observable escalation state; “stuck somewhere” is not a state model.

### Common failures

Common failures include calling compensation “rollback”; updating saga state and publishing a command non-atomically; generating a new idempotency key on every retry; interpreting timeout as failure; compensating an outcome-unknown action before reconciling it; assuming reverse wall-clock order for parallel work; deleting audit history as compensation; failing to authorize refunds/cancellations independently; leaving concurrent isolation anomalies unnamed; letting choreography become an invisible cyclic workflow; keeping orchestration state only in memory; retrying permanent business rejection; permitting old leases to issue effects; changing workflow definitions underneath live instances; treating dead-letter storage as resolution; and reporting success while a physical or financial effect remains uncertain.

### Compact example

An order saga reserves stock, captures payment, and requests shipment. Shipment rejects before creating a shipment. The durable coordinator marks that step failed, refunds the captured payment using the original charge-derived effect identity, then releases the reservation. If the payment response had been lost, it would first query/reconcile the charge identity rather than immediately issue a refund. The terminal state is `compensated`, not “rolled back”: refund and reservation-release records remain, fees or exchange-rate differences may remain, and failures route to owned manual review.

### Connections

[SEPAT-032](032-command.md) supplies explicit requests, [SEPAT-038](038-state.md) supplies durable state-machine reasoning, [SEPAT-062](062-message-router.md) and [SEPAT-066](066-publish-subscribe-channel.md) clarify message coordination, while [SEPAT-081](081-retry-with-bounded-backoff.md) and [SEPAT-082](082-timeout-and-deadline.md) constrain attempts and uncertainty. The successor [Transactional Outbox](../ROADMAP.md) closes the local-state/message publication gap used by practical sagas.

## Governing Question

How should engineers design a distributed business workflow whose participants commit independently, whose intermediate state is externally observable, whose messages can be duplicated or delayed, and whose partial effects may require compensation, forward recovery, or human judgment?

The Saga pattern answers by making the workflow a durable protocol. It does not restore single-database ACID across services. Instead, it names local commit boundaries, possible intermediate states, recovery actions, concurrency rules, and evidence needed to show that each business invariant survives partial failure.

## Why This Matters

Independent services, external providers, humans, devices, and long-running approvals cannot usually share one short transaction. Holding locks across minutes or organizations harms availability and autonomy; some participants do not support prepare/commit at all. Yet “eventual consistency” alone is not a design. An order that captures money but never allocates stock, a trip that books one nonrefundable leg, or an account closure that leaves active credentials needs an explicit resolution protocol.

Sagas let local owners retain their data and transaction mechanisms while coordinating a wider intent. The cost is weaker isolation and more application responsibility. Intermediate states become visible. Recovery can take time. Compensation can fail or only partially offset harm. Operations needs enough durable evidence to determine what happened and enough authority to repair it. These are correctness requirements, not merely observability features.

The original 1987 Saga model addressed long-lived database transactions by splitting them into smaller transactions with compensating transactions. Modern service architectures extend the idea across independently deployed participants and unreliable messaging. The durable principle survives tool changes: model business progress and recovery explicitly at each independently committed boundary.

## Prerequisites and Retrieval

Learners should retrieve:

- atomicity, consistency, isolation and durability within a local transaction;
- at-least-once message delivery, duplicate detection and idempotency;
- state machines, commands, events and correlation identifiers;
- bounded retry, deadlines, timeouts and ambiguous remote outcomes;
- optimistic concurrency, conditional writes, reservations and invariants;
- transactional outbox/inbox ideas and reconciliation loops;
- authorization, audit, privacy and operational ownership.

Before continuing, explain why “the request timed out, so the charge failed” is invalid after the charge command crossed the network boundary.

## Learning Objectives

After this module, learners can:

1. distinguish saga recovery from distributed atomic rollback;
2. define saga, step, attempt, message and effect identities precisely;
3. model forward, compensation, ambiguous and escalation states durably;
4. choose orchestration or choreography from workflow forces rather than fashion;
5. design semantic compensation, pivot placement and dependency-aware ordering;
6. identify saga isolation anomalies and choose domain countermeasures;
7. close coordinator/participant messaging gaps with durable handoff patterns;
8. handle duplicate, delayed, reordered, stale and outcome-unknown work safely;
9. version, observe, reconcile and operate long-lived instances;
10. verify safety and liveness through boundary fault injection and named review.

## Core Exposition

### Start with the business invariant and local boundaries

Do not begin with a workflow engine. State the business intent, unacceptable states, acceptable temporary states, terminal outcomes, and independently owned consistency boundaries. “Place order” might require that captured value is eventually matched by deliverable inventory or compensated, that inventory is never oversold, and that every unresolved monetary effect has an owner. It does not necessarily require that observers see all changes simultaneously.

For each participant identify the local transaction $T_i$: its command preconditions, atomic state change, durable result, emitted fact/next intent, stable effect identity, and possible compensation $C_i$. A participant—not the coordinator—enforces its local invariants. The coordinator may decide *when* to request a reservation, but inventory decides whether the reservation is legal and commits it atomically.

If every step truly requires immediate global isolation, or an irreversible action must be atomically coupled to unrelated stores, decomposition may be the wrong boundary. Co-locate the invariant, redesign the business promise, use a shared transaction where technically and organizationally justified, or accept an explicit manual control. A saga cannot manufacture compensation for an irreversible external fact.

### Identity is multidimensional

One `correlation_id` is usually insufficient. Separate:

- **saga ID**: one business workflow instance;
- **step ID**: the logical workflow node, such as `capture-payment`;
- **effect ID**: the one business effect the participant must deduplicate;
- **attempt ID**: a particular dispatch/lease execution;
- **message ID**: one transport envelope;
- **entity/version**: participant state and optimistic-concurrency generation;
- **workflow version**: the definition that governs this instance.

A retry normally preserves saga, step and effect identity while creating a new attempt and message identity. If every retry invents a new effect ID, an idempotent participant correctly performs multiple logical effects. If unrelated business operations reuse an effect ID, legitimate work is suppressed. Scope keys by participant, operation, tenant and business identity; retain deduplication records for at least the maximum replay/recovery horizon.

Idempotency does not mean “the handler ran once.” It means repeated requests for one logical effect converge on the same committed result. The participant should atomically record effect identity, validated request fingerprint, resulting entity/version, and response material with the local mutation. A duplicate with a conflicting fingerprint is an integrity error, not a cache hit.

### Make the saga a durable state machine

An in-memory chain of remote calls is not a durable saga. Persist a state machine with legal transitions and evidence. Useful step states include `not_started`, `dispatch_pending`, `dispatched`, `committed`, `business_rejected`, `retry_wait`, `outcome_unknown`, `compensation_pending`, `compensating`, `compensated`, `compensation_failed`, and `manual_review`. Names may differ, but collapsing uncertainty into failure loses correctness.

Each transition records saga/workflow version, step/effect identity, prior state/version, trigger/message, attempt and fencing epoch, timestamps/deadline, participant evidence, next eligible time, and error classification. Use conditional writes so two workers cannot both advance the same state version. A lease alone is insufficient: a paused old worker can wake after expiry. A monotonically increasing fencing token must be checked wherever stale execution could issue or record a conflicting action.

The transition “record step committed, then publish next command” contains a crash gap. If the process dies between the writes, the saga stalls; reversing the order may dispatch work that durable saga state does not know. Atomically record the transition and an outgoing message/intent in one local transaction, then relay it—the Transactional Outbox pattern covered next. Consumers likewise need an inbox/deduplication boundary where delivery is at least once.

### Compensation is semantic, conditional and fallible

A database rollback removes uncommitted changes before other transactions can depend on them. Saga compensation happens after commit and observation. It therefore creates a new fact. Refunding a charge does not erase the charge: fees, exchange-rate changes, loyalty points, notifications, fraud signals or reporting entries may persist. Cancelling shipment may fail after physical pickup. Deleting records can destroy required audit evidence.

Define compensation from the business invariant:

- preconditions: which committed effect and version may be offset;
- authority: which principal/policy can refund, release or revoke;
- effect identity: stable and deduplicated independently from the forward action;
- behavior if already compensated or superseded;
- deadline and retry classification;
- residual effects that remain after compensation;
- evidence and escalation when automatic compensation is illegal or impossible.

Compensations must themselves tolerate duplicate delivery and ambiguous responses. If `refund` times out, retrying with the same refund effect identity or querying the provider is safe; creating another refund identity may over-refund. If the forward outcome is unknown, reconcile it before choosing a compensation whose precondition assumes commitment.

Reverse sequence is a useful default only for a linear dependency chain. For a dependency graph, compensate in reverse topological order: an effect must not be undone while a dependent effect still relies on it. Independent branches may compensate concurrently if their participants and business invariants allow. Wall-clock completion order can differ from dependency order and is not a sufficient algorithm.

### Forward recovery, backward recovery and pivots

Not every failure should compensate. Classify outcomes:

- transient technical failures may retry with bounded backoff and the same effect identity;
- permanent business rejection may select an alternative or start backward recovery;
- ambiguous results require query/reconciliation;
- policy or authority expiration may require a new approval;
- irreparable or high-risk outcomes require manual review.

Some designs distinguish compensatable steps before a **pivot**, the pivot itself, and retriable steps after it. For example, reservations can be released before a nonrefundable ticket is issued; after issuance, remaining bookkeeping may be driven to completion. This classification is a design aid, not a universal theorem. A “retryable” step still needs a durable idempotent protocol and may encounter permanent rejection. Pivot placement should minimize irreversible commitment before uncertainty is reduced.

Forward recovery is often better once a valuable/irreversible effect exists. If a parcel has physically shipped, completing records and notifying the customer may preserve more truth than pretending cancellation. Backward recovery is appropriate only when compensations produce an acceptable state. Mixed recovery is normal: compensate one branch, retry another, then escalate residual uncertainty.

### Saga isolation is not database isolation

Local transactions can each be serializable while the overall saga is not isolated. Between steps, other work can read or modify intermediate state. Common anomalies include:

- a dirty-like read of a state that will later be compensated;
- a lost update when another workflow changes data before compensation;
- a nonrepeatable read between validation and later action;
- write skew across independently checked constraints;
- oversubscription when many sagas pass the same availability check;
- compensation that overwrites a legitimate later change.

Choose explicit countermeasures by invariant:

- **semantic locks/pending states** expose `reserved`, `pending_close`, or `transfer_in_progress` so conflicting actions follow domain rules;
- **reservations/escrow** allocate bounded rights before irreversible use;
- **version/conditional writes** reject stale forward or compensation updates;
- **commutative operations** reduce order sensitivity;
- **reread and revalidate** immediately before commitment;
- **pessimistic local locking** protects a participant's short critical section;
- **single-writer/partition ownership** serializes a named entity where justified.

Semantic locks can reduce availability and become stranded; they need expiry policy that does not equate time expiry with absence of an issued effect. Compensation should target the version/effect it created, not restore an old full snapshot over newer legitimate state.

### Orchestration and choreography

In **orchestration**, a durable process manager stores workflow state, interprets participant outcomes, and issues commands. It centralizes visibility and complex branching. It must be highly available, versioned and fenced, but it does not own participant data or bypass local validation. “Central coordinator” does not have to mean one process or one failure domain; durable replicated state and resumable workers remove the in-memory single point.

In **choreography**, participants react to events and emit events that trigger others. It can suit small, stable flows where events are meaningful beyond the saga and ownership remains clear. As participants and branches grow, the workflow graph becomes implicit across deployments. Cycles, accidental coupling, global timeout logic, compensation ownership and end-to-end testing become difficult. A correlation trace is not a substitute for an explicit state owner.

Hybrids are common: an orchestrator owns the business protocol while participants publish domain events for observers; or a small choreographed sequence is supervised by a reconciliation process. Choose from change rate, number of steps/branches, audit needs, team ownership, failure handling and visibility—not from a false centralization-versus-decoupling slogan.

### Time, cancellation and ambiguous outcomes

Deadlines bound waiting, not truth. Distinguish:

- a client deadline for the synchronous response;
- a per-attempt timeout;
- a step/business deadline;
- an authorization or reservation expiry;
- a maximum reconciliation/escalation horizon.

When the client stops waiting, the saga may continue asynchronously and return an operation identifier. Cancellation can prevent undispatched future work, but cannot erase committed steps. It becomes another command with authorization, state/version preconditions and possibly compensations.

The most dangerous boundary is commit followed by lost acknowledgement. Marking this `failed` risks duplicate action; marking it `committed` without evidence risks skipping required work. Record `outcome_unknown`, query by stable effect identity where possible, consume later authoritative events, and escalate if no reliable observation exists. Provider APIs that cannot accept/query idempotency identities may require reconciliation against statements or human investigation; the residual risk is architectural.

### Deterministic state and compensation trace

The following pure model commits reservation and charge, observes a definite shipment failure, and then compensates according to the linear dependency order. It demonstrates state ordering only.

<!-- bijux-verify: {"id":"sepat-087-saga-trace","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"forward=reserve:committed,charge:committed,ship:failed\ncompensation=refund-charge:committed,release-reservation:committed\nterminal=compensated\neffects=charge-refunded,reservation-released\n","stderr":""}} -->
```python
steps = [
    ("reserve", "committed"),
    ("charge", "committed"),
    ("ship", "failed"),
]
compensations = {
    "charge": ("refund-charge", "charge-refunded"),
    "reserve": ("release-reservation", "reservation-released"),
}

forward = []
committed = []
for name, outcome in steps:
    forward.append(name + ":" + outcome)
    if outcome == "committed":
        committed.append(name)
    else:
        break

compensation = []
effects = []
for name in reversed(committed):
    action, effect = compensations[name]
    compensation.append(action + ":committed")
    effects.append(effect)

print("forward=" + ",".join(forward))
print("compensation=" + ",".join(compensation))
print("terminal=compensated")
print("effects=" + ",".join(sorted(effects)))
```

This execution proves the exact deterministic list traversal and output for one definite failure. It omits durable storage, local transactions, messages, concurrency, duplicated delivery, outcome ambiguity, idempotency, authorization, compensation failure, isolation, parallel dependencies, workflow upgrades and external effects.

### Versioning, operations and security

Long-lived instances outlive deployments. Persist the workflow definition/version chosen at creation. Compatible code must interpret old states and message schemas; migrations require explicit invariants, replay tests and rollback plans. Do not silently insert a new mandatory step into active instances or reinterpret old terminal states. Participant contract evolution needs tolerant readers, schema compatibility and retained idempotency semantics.

Operate by state, age and ownership. Metrics include starts/terminal outcomes, step latency and attempts, retry/compensation rates, outcome-unknown age, stuck transitions, outbox/inbox lag, duplicate/conflict counts, workflow version, deadline breaches, manual-review backlog and invariant alarms. Traces aid diagnosis but durable records are the source of recovery truth. Bound labels and protect customer/payment data.

Reconciliation scanners find nonterminal instances with no eligible worker, stale dispatches, unmatched participant evidence, or expired authority. A dead-letter queue preserves a failed message but does not resolve the business intent; it must feed an owned repair workflow. Runbooks state safe replay/query/compensation actions and when automation stops.

Every forward and compensating command uses least privilege, authenticated tenant/entity binding, replay protection and current authority. Compensation often has more financial or destructive privilege than the forward action and deserves separate authorization, limits and audit. Avoid placing secrets or sensitive full payloads in saga logs. Operator tools need dual control for high-impact repair, immutable audit, previews, and idempotent actions.

### Verification strategy

Test every durable boundary: before local commit, after commit before outbox relay, before/after broker acknowledgement, before participant handling, after participant commit before response, before/after coordinator transition, and during compensation. Inject crash/restart, duplicate, delay, reordering, partition, stale lease, clock skew, dependency outage, schema skew and poison data. For each injection, assert named invariants and eventual terminal/escalation behavior—not merely process recovery.

Use model/state-machine tests to enumerate legal transitions and impossible combinations. Property tests can assert one logical participant effect per effect identity and no compensation before known/safely reconciled commitment. Concurrency tests target reservations, version checks and semantic locks. Replay tests run old workflow/message versions. Production game days validate dashboards, repair tools, access control, rate limits and human handoff in an isolated owned environment.

Financial, medical, legal, safety or irreversible workflows require named domain and risk reviewers. Automated checks can validate structure, transitions and arithmetic but cannot decide whether a refund, revocation, disclosure or physical intervention is an ethically and legally adequate compensation.

## Definitions and Notation

Let saga instance $S$ contain workflow-versioned steps $V=\{v_1,\ldots,v_n\}$ with dependency DAG $G=(V,E)$. Let $T_i$ be participant $i$'s local forward transaction and $C_i$ its optional compensating transaction. Let $sid$, $step_i$, $eid_i$, $aid_{i,j}$, and $mid_{i,j}$ denote saga, step, stable effect, attempt and message identities. Let $q_i$ be durable step state, $g$ a fencing generation, and $d_i$ a step/business deadline.

An idempotent participant implements a logical mapping where all valid duplicate requests carrying the same $eid_i$ and fingerprint return the same committed effect/result. This is not a claim about exactly-once transport or exactly-once handler execution.

A terminal saga state is domain-defined: `completed`, `compensated`, `partially_compensated_manual_review`, or another explicit outcome. “Compensated” means the specified compensations committed; it does not imply restoration of every historical or physical condition.

## Mechanisms, Invariants, or Proof Structure

**Local safety.** Each $T_i$ atomically checks local preconditions, applies one effect for $eid_i$, and records replay evidence. Therefore duplicates with the same identity cannot multiply that participant effect, assuming identity retention and transaction isolation are adequate.

**Durable progress.** A coordinator transition and its next outgoing intent are atomically recorded. At-least-once relays may duplicate delivery, but participant deduplication makes repetition safe. Fair retry/reconciliation can then resume after crashes. This is a conditional liveness argument: permanent outages, expired authority or impossible compensation terminate in explicit escalation rather than automatic completion.

**Backward recovery.** For a linear prefix of known committed compensatable steps, compensating in reverse dependency order avoids removing a prerequisite while its dependent effect remains. For DAGs, any reverse topological order satisfies that dependency constraint; business-specific dependencies can add edges.

**Isolation safety.** Saga structure alone provides no global isolation. A proof must name each cross-step invariant and show how reservation, escrow, versioning, commutativity, serialization or revalidation preserves it under concurrent instances.

**Ambiguity safety.** `outcome_unknown` prevents the coordinator from assuming either commit or noncommit. Resolution uses effect-identity query, authoritative event/reconciliation, or manual evidence before mutually incompatible forward/compensating actions.

**Fencing safety.** Conditional state version plus monotonically increasing generation rejects stale workers at durable issue/record boundaries. If a participant ignores the token and accepts non-idempotent stale effects, coordinator fencing alone is insufficient.

**Residual-state honesty.** Compensation proves only the postconditions it specifies. Fees, audit records, notifications, external observations and physical effects remain unless separately addressed. Terminal state and user communication must expose material residuals.

## Alternatives and Trade-Offs

| Alternative | Prefer when | Limitation relative to a saga |
|---|---|---|
| one local ACID transaction | invariant fits one owned store/boundary | cannot span independent providers or long human work |
| distributed transaction/2PC | all participants support it and blocking/coordination trade-offs are acceptable | availability, operational and organizational coupling; external effects often unsupported |
| redesign/colocate invariant | global atomicity is truly required | can reduce autonomy or require major boundary change |
| orchestration | complex branching, deadlines, compensation and audit need one state owner | coordinator complexity, versioning and operational dependency |
| choreography | small stable event flow with clear ownership | implicit graph, cycles and recovery visibility grow difficult |
| forward-only workflow | irreversible effect should drive completion | may require long retries/escalation and cannot undo harm |
| reservation/escrow | scarce rights can be allocated before pivot | expiry, stranded capacity and contention need policy |
| human reconciliation | law, safety, ambiguity or irreversibility defeats automation | latency, cost and operator-error risk; needs owned queue/tools |
| best-effort eventual consistency | discrepancies are low-risk and independently repairable | too weak for bounded/high-impact invariants |

## Failure Modes and Misconceptions

- **Saga means distributed rollback.** Local commits and observations remain; compensation is new work.
- **Every action has an inverse.** Email, disclosure, shipment and physical harm may be irreversible.
- **A timeout is a failed step.** It may be a committed effect with a lost acknowledgement.
- **Exactly-once messaging solves it.** Transport claims do not replace participant effect identity and atomic deduplication.
- **Idempotency key per attempt is safe.** It multiplies logical effects across retries.
- **Reverse completion order is always correct.** Parallel branches follow dependency order.
- **Compensation cannot fail.** It has the same network, business, authority and capacity risks as forward work.
- **Local serializability gives saga isolation.** Other workflows observe and change state between steps.
- **Restore the old snapshot.** It can overwrite legitimate later changes.
- **Choreography has no coordinator.** Coordination still exists, but may be hidden across consumers.
- **An orchestrator owns all data.** Participants retain local invariants and authority.
- **A workflow engine creates correctness.** Durable execution cannot invent business invariants or adequate compensation.
- **Retry every exception.** Permanent rejection, conflict, expiry and corruption require distinct handling.
- **Lease expiry cancels old work.** A paused worker may resume unless fenced and deduplicated.
- **Dead-letter means handled.** It stores evidence; the business intent remains unresolved.
- **Compensated means original state restored.** Residual financial, informational and physical effects may remain.

## Worked Examples

### Example 1

An order reserves one item, captures €80, then receives a definite “address invalid” before shipment creation. The dependency chain is reserve → charge → ship. Backward recovery first refunds the charge and then releases inventory. Each action has a stable effect identity. The conclusion is `compensated`; the charge/refund audit trail remains and the system does not claim atomic rollback.

### Example 2

A payment request times out after dispatch. Immediate compensation is unsafe: the charge might have committed, but a refund might arrive before the provider exposes it or might itself duplicate. The saga records `outcome_unknown`, queries the provider by charge effect ID, and consumes authoritative settlement evidence. Only after commitment is established does cancellation policy request one idempotent refund. The conclusion is that ambiguity is a state requiring reconciliation, not an error code to guess away.

### Example 3

Two travel branches reserve hotel and car concurrently; both depend on a payment authorization, while ticketing depends on both. Ticketing fails before issue. Reverse wall-clock order might release authorization before car/hotel cancellation. The dependency DAG instead cancels hotel and car (in parallel if allowed), then releases authorization. Reverse topological order, augmented with business dependencies, preserves prerequisites during compensation.

### Example 4

An inventory saga reads ten units available; another saga does the same; both later request seven. A read-then-write choreography oversells. Inventory instead atomically creates reservations against an escrowed available balance, so only one seven-unit reservation succeeds. The rejected saga chooses an alternative. Local reservation—not the existence of a saga—preserves the stock invariant.

### Example 5

A coordinator records “payment committed” and crashes before publishing `create-shipment`. With separate writes, the instance can stall forever. It instead records the transition and outbox command in one local transaction. A relay republishes until acknowledged; shipment deduplicates by effect identity. At-least-once delivery plus atomic durable handoff and idempotent effects closes the lost-command window without claiming exactly-once execution.

### Example 6

A cancellation restores an entire pre-saga customer snapshot after a concurrent address update. The compensation silently loses the new address. The corrected action conditionally clears only the `pending_order_id` field/effect created by this saga and checks entity version or a commutative marker set. Compensation must target its own semantic delta, not overwrite later legitimate state.

### Example 7

A workflow definition adds fraud review between charge and shipment while thousands of old instances are active. Reinterpreting their step numbers corrupts recovery. New instances receive workflow version 4; version 3 handlers remain readable and replay-tested until all old instances terminate or undergo an explicit verified migration. The durable definition is part of instance state, not merely deployment code.

### Example 8

A choreographed onboarding flow grows from three participants to twelve, with cycles for rejection and no service able to answer “who owns completion?” Traces show messages but not legal global transitions. The team introduces a process manager that owns saga state and deadlines while participants retain data ownership and publish domain events. This is an evidence-based shift to orchestration, not a rejection of event-driven integration.

### Example 9

A refund compensation repeatedly fails because the original operator's delegated authority expired. Technical retry cannot repair authorization. The saga enters `manual_review`, preserves the forward/refund identities and evidence, alerts an owned queue, and offers an audited reauthorization action with dual control. Escalation is a legitimate designed terminal/holding state; infinite retries are not liveness.

### Example 10

A medical-device provisioning saga installs configuration remotely, updates monitoring, and notifies staff. A device acknowledgement is lost and configuration could affect treatment. The system does not retry with a new identity or mark success from a coordinator record. It queries signed device generation/state, fences stale commands, blocks conflicting workflows, and enters human review if evidence disagrees. Named clinical, safety, device, security and operations reviewers must approve compensation and fail-safe behavior; software tests alone cannot establish clinical adequacy.

## Cross-Program Connections

- [Software Design and Domain Modeling](../../09-software-engineering-software-design-and-domain-modeling/ROADMAP.md): aggregates, bounded contexts, domain events and business invariants define saga boundaries.
- [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md): service ownership, coupling, process managers and evolutionary boundaries.
- [Software Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md): state-model, fault-injection, replay, concurrency and recovery tests.
- [Database Engineering](../../18-database-engineering/ROADMAP.md): local transactions, isolation anomalies, conditional writes, outbox/inbox and durable logs.
- [Security Engineering](../../25-security-engineering/ROADMAP.md): command/compensation authority, replay defense, tenant binding and audit privacy.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md): partial failure, ambiguity, idempotency, delivery semantics, fencing and liveness.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md): workflow runtimes, observability, repair tooling, deployment/version operations and game days.

## References

1. Garcia-Molina, Hector, and Kenneth Salem. “Sagas.” *Proceedings of ACM SIGMOD*, 1987, pp. 249–259. <https://doi.org/10.1145/38713.38742>
2. Gray, Jim, and Andreas Reuter. *Transaction Processing: Concepts and Techniques*. Morgan Kaufmann, 1992.
3. Bernstein, Philip A., Vassos Hadzilacos, and Nathan Goodman. *Concurrency Control and Recovery in Database Systems*. Addison-Wesley, 1987. <https://www.microsoft.com/en-us/research/people/philbe/book/>
4. Hohpe, Gregor, and Bobby Woolf. *Enterprise Integration Patterns*. Addison-Wesley, 2003.
5. Kleppmann, Martin. *Designing Data-Intensive Applications*. O'Reilly, 2017.
6. Richardson, Chris. *Microservices Patterns*, 2nd ed. Manning, 2025.
7. Microsoft. “Saga Distributed Transactions Pattern.” Azure Architecture Center. <https://learn.microsoft.com/en-us/azure/architecture/patterns/saga>
8. Microsoft. “Compensating Transaction Pattern.” Azure Architecture Center. <https://learn.microsoft.com/en-us/azure/architecture/patterns/compensating-transaction>
9. Amazon Web Services. “Saga Orchestration Pattern.” AWS Prescriptive Guidance. <https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/saga-orchestration.html>
10. Fowler, Martin. “What Do You Mean by ‘Event-Driven’?” 2017. <https://martinfowler.com/articles/201701-event-driven.html>
11. Fowler, Martin. “Patterns for Distributed Transactions Within a Microservices Architecture.” 2021. <https://martinfowler.com/articles/patterns-of-distributed-systems/>
12. Bailis, Peter, et al. “Coordination Avoidance in Database Systems.” *Proceedings of the VLDB Endowment* 8(3), 2014. <https://www.vldb.org/pvldb/vol8/p185-bailis.pdf>

The original paper grounds the durable concept; official platform pages describe current service-architecture terminology and cautions. Official web sources were checked on 2026-08-29. Exact workflow-runtime, broker and provider guarantees are version/deployment specific and must be verified against the deployed system.

## Exercises

### Exercise 1

Define the identity and durable-state model for an order saga that reserves inventory, captures payment and creates shipment. Include duplicate and ambiguous outcomes.

### Exercise 2

A saga has dependencies authorization → {hotel, car} → ticket. Hotel and car complete in either order; ticket fails definitely before issue. Derive a valid compensation order and explain why reverse wall-clock completion is not the rule.

### Exercise 3

Diagnose a coordinator that writes `step_complete`, publishes the next command separately, creates a new idempotency key on timeout, treats dead-letter storage as resolution, and relies on a lease without fencing. Redesign its correctness boundaries.

### Exercise 4

Compare orchestration and choreography for a twelve-participant insurance claim with branching evidence collection, deadlines, regulatory audit, irreversible notices and frequent workflow change. Propose an approach and its trade-offs.

### Exercise 5

Design a saga for remote industrial equipment activation spanning payment, entitlement, device configuration and safety inspection. State invariants, pivot/compensation policy, isolation controls, ambiguity handling, security, verification and human review.

## Answers to the Exercises

### Answer 1

Use one saga ID and workflow version, stable logical steps (`reserve`, `capture`, `create-shipment`), a stable participant-scoped effect ID per step, a fresh attempt/message ID per delivery, entity versions and a fencing generation. A retry preserves the effect ID and request fingerprint. Each participant atomically validates, mutates and stores deduplication/result evidence; a conflicting fingerprint is rejected.

Persist legal states including dispatch-pending/dispatched, committed, business-rejected, retry-wait, outcome-unknown, compensation states and manual review. Atomically bind every coordinator transition to its outgoing intent through an outbox. Duplicate commands return the prior effect result. A timeout after dispatch becomes outcome-unknown and is queried/reconciled by effect ID; it does not generate a new charge/shipment or assume failure. Terminal outcomes distinguish completed, compensated and unresolved/manual-review, with residual effects recorded.

### Answer 2

The forward DAG is authorization before both hotel and car, and both before ticket. Because ticket failed before issue, it needs no compensation. Hotel and car may be cancelled in parallel or either order if there is no added domain dependency. Authorization is released only after both cancellations complete. Valid sequences include `cancel-hotel; cancel-car; release-authorization`, the reverse first two, or concurrent hotel/car cancellation followed by release.

Reverse wall-clock completion is accidental scheduling order. If authorization happened to finish last but is a prerequisite for the reservations, undoing it first can violate compensation preconditions. Reverse topological dependency order retains prerequisites until dependents are removed. Any additional provider/business rule must appear as another edge.

### Answer 3

Separate state/publish writes create two unsafe windows: commit then crash loses progress; publish then commit can create an unknown effect. Record state transition plus outgoing command in one local transaction and relay at least once. The participant atomically deduplicates the stable logical effect ID and stores its result. Retries create new attempt/message IDs but retain effect identity; timeout becomes outcome-unknown until query or authoritative evidence resolves it.

Dead-letter storage feeds an owned reconciliation workflow with alert, repair action, evidence and SLA; it is not terminal resolution. Use conditional saga-state versions and monotonically increasing fencing generations. Require participants or durable issue boundaries to reject stale generations where duplicate identity alone cannot prevent conflicting work. Add bounded classified retries, invariant alarms, workflow-version replay, and manual escalation for permanent or ambiguous cases.

### Answer 4

Prefer a durable orchestrated process manager because the workflow has many participants, branches, timers, audit obligations, irreversible communications and frequent coordinated change. It owns claim-workflow state, definition version, deadlines, decisions and compensations; evidence, payment and notice services retain their data and local invariants. Participants can still publish domain events for other consumers, so orchestration does not forbid event-driven integration.

Benefits are an explicit legal state graph, one completion owner, visible timers/ambiguity, controlled versioning and testable recovery. Costs are coordinator design/availability, schema compatibility, operational tooling and possible excessive coupling if it contains participant business logic. Replicated durable state, resumable/fenced workers, outbox/inbox, least-privilege commands and replay/model tests address mechanisms—not the domain adequacy of compensation. Irreversible notices require preconditions/pivot placement and named regulatory review.

### Answer 5

Define invariants: entitlement cannot be active without valid payment and passed inspection; one activation effect exists per device generation; conflicting configuration workflows cannot overlap; every issued device command is reconciled; unsafe/unknown device state blocks activation. Payment and entitlement use local atomic idempotent effects. Device configuration uses signed tenant/device/generation-bound commands, monotonic fencing, read-back evidence and a semantic `activation_pending` lock. Inspection records are authoritative and versioned.

Place reversible reservation/authorization steps before the pivot. Treat physical energization or an irreversible configuration as a pivot only after safety inspection and connectivity/evidence checks; afterward prefer forward recovery to consistent monitoring/entitlement records. Refund/revoke/reconfigure actions are semantic compensations with separate authority and residual-cost disclosure. A lost device acknowledgement becomes outcome-unknown and is resolved from signed device state or manual inspection, never a fresh identity retry.

Verify every commit/message/acknowledgement boundary with crash, duplicate, delay, reorder, partition, stale worker, provider outage, authority expiry, workflow upgrade and concurrent activation. Assert device-generation uniqueness, entitlement/payment consistency, no unsafe activation and eventual completed/compensated/escalated ownership. Security review covers command signing, replay, tenant binding, operator dual control and audit privacy. Named controls, device, functional-safety, security, payments/legal, reliability/operations and field-service reviewers must approve hazard analysis, compensation limits, fail-safe behavior and recovery drills; automated evidence cannot substitute for them.
