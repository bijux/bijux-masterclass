---
module_id: SEPAT-070
program: Software Engineering: Patterns
level: 2
module_number: 70
title: Designing an Integration Flow from Message Semantics
status: complete
last_verified: 2026-08-29
---

# Designing an Integration Flow from Message Semantics

## One-Page Review

### Governing question

How can an integration flow be derived from the meaning and obligations of its messages so that channel topology, routing, transformation, delivery, ordering, scaling, security, recovery, and completion all preserve the domain contract end to end?

### Essential definitions

- **message semantics** state what a message means, who has authority, why it exists, which recipients owe what, when it is applicable, and which outcome completes it.
- A **command** requests one decision owner to attempt an action; an **event** records a fact that independent subscribers may react to; a **document message** transfers a representation for an explicitly named use.
- A **semantic envelope** binds stable identity, type/schema, source, occurred/requested time, tenant, correlation/causation, ordering key, classification, expiry, and payload/claim integrity.
- An **obligation set** is the set of independently owned effects or terminal decisions created by accepting a message.
- A **flow stage** validates, routes, translates, stores, dispatches, applies, or observes a message under an explicit input/output contract.
- A **semantic preservation invariant** requires every stage either to preserve authoritative meaning and identity or to emit a named, reviewable transformation with provenance.
- **delivery semantics** describe transport attempts; **effect semantics** describe accepted business changes. They are separate contracts.
- A **terminal outcome** is completed effect, valid rejection/cancellation/expiry, supersession/compensation, or owned unresolved/dead-letter state under policy.
- A **flow decision record** captures the semantic facts, selected patterns, alternatives, guarantees, assumptions, owners, evidence, and lifecycle.
- An **end-to-end claim** is no stronger than the weakest unverified boundary across producer, broker, stages, stores, consumers, external effects, and operations.

### Central model, mechanism, or theorem

Represent a flow as directed graph \(G=(V,E)\). For message \(m\), semantic contract \(S_0(m)\) creates obligation set \(O(m)\). Each stage \(v_i\) applies a typed transition

\[
T_i:(S_i,m_i)\rightarrow(S_{i+1},m_{i+1},e_i),
\]

where \(e_i\) is durable evidence. Correct composition requires each transition to preserve stable identity, authority, provenance, security classification, ordering scope, and outstanding obligations unless an explicit authorized rule changes them.

For obligation \(o\in O(m)\), at-least-once transport may yield \(D_{m,o}\ge1\), while an idempotent/conditional effect boundary targets \(E_{m,o}\in\{0,1\}\). Flow completion is

\[
Complete(m)\iff\forall o\in O(m),\ outcome(m,o)\in Terminal_{policy}.
\]

Broker acceptance, one subscriber acknowledgement, or an empty queue is not this predicate.

### Critical invariants

- Message kind follows domain authority: commands have one decision owner; events are immutable facts; documents name representation, authority, and permitted use.
- Producer state and publication are closed with an outbox/transactional protocol or an explicitly weaker contract and reconciliation.
- Stable message, causation, correlation, entity, operation, tenant, schema, and payload identity survive every hop and retry.
- Channel and subscription cardinality match the obligation set; worker replicas do not accidentally multiply logical effects.
- Routers decide from authenticated minimal facts, translators preserve provenance and do not invent authority, and canonical models stay bounded by ownership.
- Ordering is scoped to a key/partition/workflow and enforced at the effect boundary with sequence/version/gap behavior.
- Every effect uses idempotency or conditional state, and acknowledgements occur only after the promised durable boundary.
- Retry, deadlines, dead letters, replay, corrections, and cancellation preserve identity and current authorization/applicability.
- Payload, Claim Check, traces, logs, and failure stores enforce classification, minimization, integrity, retention, and tenant/purpose isolation.
- Every stage has owner, capacity/backpressure, SLO, observable evidence, version compatibility, failure policy, and tested recovery.

### Common failures

Common failures include choosing a broker before defining meaning, broadcasting commands, treating events as mutable instructions, one canonical schema owned by nobody, content routing on untrusted fields, losing source/causation during translation, confusing groups with subscribers, global-order promises on partitioned flows, acknowledging before effects, claiming exactly once across remote side effects, retrying expired work, redriving with new business identity, deleting claimed payload before slow subscribers, treating a DLQ as completion, autoscaling past downstream capacity, logging sensitive envelopes, using traces as audit, dual publishing without equivalence evidence, and declaring the flow correct because happy-path messages moved through it.

### Compact example

`ChargePayment` is a command with one payments owner, stable operation ID, `order_id` ordering key, deadline, and one terminal result. It goes to a point-to-point command channel; competing workers share one subscription. A translator validates the version without changing authority. A transaction claims the operation, writes the charge/result outbox, then acknowledges. Transient provider failures use bounded delayed retry; ambiguous effects reconcile by provider idempotency key; expired or invalid commands terminate under policy; unresolved cases enter a payments-owned quarantine. `PaymentCharged` is then published as an event to independent subscribers—it is not the original command broadcast.

### Connections

[SEPAT-061](061-message-channel.md) through [SEPAT-069](069-dead-letter-channel.md) supply the component patterns composed here; [SEPAT-071](../ROADMAP.md) begins concurrency/reactive implementation with Reactor. Flow design also connects to [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md), [Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md), [Security Engineering](../../25-security-engineering/ROADMAP.md), [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md), and [Platform Engineering](../../29-platform-engineering/ROADMAP.md).

## Governing Question

Given a domain interaction, how do we derive—not merely assemble—an integration flow whose topology and failure behavior are justified by message meaning, ownership, and terminal obligations?

Pattern catalogs provide vocabulary, not a recipe. A Publish-Subscribe Channel is excellent for independent reactions to a fact and dangerous for a command with one owner. Claim Check reduces broker bytes but creates a storage and lifecycle dependency. Competing Consumers add capacity but weaken completion order. Design therefore begins with semantic facts and uses patterns as consequences.

## Why This Matters

Integration failures often cross team and system boundaries: an accepted order never publishes; a translation changes currency meaning; one subscriber acknowledgement hides another's lag; a retry charges twice; or a redrive reactivates an expired instruction. Each component may be locally healthy while the end-to-end obligation is wrong.

A semantics-first method makes those contracts reviewable before products and code harden them. It supports capacity planning, version evolution, threat modeling, fault testing, operational ownership, and high-stakes review. It also prevents architecture diagrams from implying guarantees that no mechanism or evidence establishes.

## Prerequisites and Retrieval

You should understand domain invariants, commands/events/documents, transactions/outbox/inbox, all patterns in SEPAT-061–069, schemas, idempotency, ordering, queueing, authorization, observability, and recovery. Retrieve these facts:

1. Message transport decouples time and location but not meaning, schema, authority, identity, or capacity.
2. A command normally has one decision owner; an event may create independent subscriber obligations.
3. Producer publication, broker delivery, consumer effects, outgoing publication, and external side effects are distinct boundaries.
4. Delivery attempts can repeat; stable idempotency/conditional effects establish business uniqueness within a stated scope.
5. Partitioned order is scoped, and concurrent completion can differ from delivery order.
6. Retry is safe only when identity, effect state, current authority/applicability, deadline, and capacity remain valid.
7. Monitoring shows evidence about execution; it does not replace durable obligation/effect/audit state.

## Learning Objectives

After completing this module, you should be able to:

- elicit a message semantic contract from domain authority, intent/fact, recipients, identity, time, ordering, payload, security, and outcomes;
- derive point-to-point, publish-subscribe, partition, subscription, and worker topology from obligation cardinality;
- place validation, routing, translation, Claim Check, idempotency, acknowledgement, retry, and dead-letter boundaries;
- model an integration flow as typed transitions with preservation invariants and durable evidence;
- distinguish transport guarantees from end-to-end effect and completion claims;
- calculate fan-out work, stage bottlenecks, retry amplification, storage/retention, and downstream concurrency bounds;
- design version evolution, migration, correction, replay, and rollback without changing historical meaning;
- threat-model producers, envelopes, routes, payload stores, subscribers, observability, and recovery tooling;
- produce a verification matrix spanning contracts, code, brokers, databases, faults, load, security, operations, and human review;
- critique a product diagram or “exactly once” claim by tracing every obligation and failure window.

## Core Exposition

### Start with a semantic interview

Ask: What happened or is requested? Who is authoritative? Is there one decision owner or several independent reactions? What stable identity distinguishes occurrence, message, entity, operation, correlation, and causation? When did the fact occur; when does a command expire? What order matters and within which key? Which fields are authoritative, sensitive, large, or derived? What outcomes satisfy or cancel each obligation?

Write answers before naming a broker. Unclear ownership is a domain problem that topology cannot repair. If two services believe they own `ApproveLoan`, define the decision boundary or workflow instead of publishing the command to both.

### Classify command, event, document, and query

A command is imperative and can be rejected; the receiver owns the decision/effect. An event is past-tense evidence of a fact and should not be revoked by editing old bytes—corrections are new facts. A document transfers a representation such as a claim, statement, image, or snapshot; specify authoritative source, as-of time, schema, integrity, and use. A query requests information and often has request/reply latency and privacy semantics distinct from durable messaging.

One business interaction may use several kinds: `PlaceOrder` command, `OrderPlaced` event, and `OrderSummary` document. Do not reuse one ambiguous `OrderMessage` schema and infer meaning from optional fields.

### Define the semantic envelope

Specify source plus stable message ID, type and semantic version, occurred/requested/published times, subject/entity, tenant, correlation and causation IDs, operation/idempotency ID, ordering key and sequence/version where required, deadline/expiry, content type/schema, payload or Claim Check digest/length, classification/purpose, and trace context.

Not every field belongs in every message. Minimize and authenticate the envelope; do not place personal data in trace identifiers. Separate business identity from transport delivery tags and observability correlation.

### Derive obligation cardinality and channels

One command owner implies a point-to-point logical channel/subscription even if many worker instances compete. An event creates one obligation per matched durable subscriber under the declared membership/retention semantics; separate consumer groups represent separate responsibilities. A targeted document may use a recipient list or direct channel; broad facts use pub/sub.

Define zero-recipient behavior. An event may validly have no current subscriber while retained for later; a command with no owner is a routing failure. Dynamic filters and subscriptions change obligation sets and require version/effective-time governance.

### Close the producer gap

Write authoritative state and an outbox record in one local transaction when omission would violate the contract. A relay publishes the same message identity until broker confirmation and records progress. Reconcile aged outbox rows and duplicates. Change-data capture is an implementation option only if its event semantics, ordering, filtering, schema and recovery are owned.

If atomic publication is impossible and loss is acceptable, state the weaker guarantee and compensating detection. Do not let “asynchronous” mean unowned omission.

### Choose routing facts and topology

Route on stable authenticated facts: message type, tenant, region, capability, priority, or domain category. Define missing/null/unknown/error semantics and a routing table/version. Content-Based Routers should not fetch sensitive Claim Check payload merely to decide, nor trust producer-controlled fields for authorization.

Static topology is easier to reason about. Dynamic routing needs registry consistency, admission, cache staleness, ownership, and audit. Always specify unroutable and duplicate-route outcomes.

### Place transformations at owned boundaries

Translate transport/envelope/schema where a team owns the semantic mapping. Record input/output types, versions, identity and provenance, loss/default rules, units, time zones, precision, enum handling, and unknown-field behavior. A translator may change representation; it cannot manufacture authority or pretend a lossy mapping is reversible.

Use a canonical model only within a bounded integration domain with a clear owner and version policy. Prefer explicit translators between stable domain contracts over one enterprise schema that accumulates every concept and couples every release.

### Select payload strategy

Inline small routinely needed content. Use Claim Check for large, sensitive, or rarely needed bytes when the object/version, digest, authorization, retention, region and deletion protocol are stronger than a bare URL. Keep routing facts in the minimal envelope. Chunking is a separate sequence/aggregation protocol, not an invisible workaround.

Capacity includes message bytes, replicas, fan-out, retry, object reads/egress, scanning, serialization, and retained history. The lowest nominal product size limit is not the only threshold.

### Partition and dispatch for order and scale

Name the ordering invariant: per entity, account, workflow, or none. Choose a stable partition/message-group key and validate sequence/entity version at effects. Global order sharply limits parallelism and often encodes an unstated domain problem.

Competing consumers scale one obligation up to partition and downstream capacity. Bound prefetch/in-flight work; account for skew and heterogeneous jobs. Explicit dispatch is appropriate when capability, locality, priority, affinity, or resource requirements make workers non-equivalent.

### Define acknowledgement and effect boundaries

At each consumer: authenticate/validate; claim stable `(subscription,message,operation)` or expected entity version; commit effect and outgoing outbox; then acknowledge/checkpoint. A crash after commit but before acknowledgement becomes a harmless dedupe/reconciliation path, not a repeated effect.

Remote effects need their own idempotency key, state machine, or reconciliation. Product transactions may atomically cover selected broker records and outputs; document exactly which stores and external effects are outside scope.

### Design retry, deadlines, and terminal outcomes

Classify transient outage, throttling, conflict, malformed input, integrity mismatch, unsupported schema, unauthorized request, expired command, permanent domain rejection, and internal defect. Assign attempt/time/cost/deadline budgets, jittered delay, circuit/admission behavior, owner, and terminal route.

Dead-letter transfer preserves unresolved evidence only if it is safe/reconciled. Redrive follows remediation, current-state/authorization/effect checks, dry run, canary and rate limits with original identity. Cancellation, rejection, expiry, supersession and accepted loss are explicit domain outcomes, not exception strings.

### Define subscription independence and flow completion

For events, enumerate logical subscribers and their effect, owner, lag SLO, retention, idempotency, retry, dead letter, replay and deletion policies. One group's progress never satisfies another. Adding a group changes fan-out cost, disclosure and ownership even if producer code stays unchanged.

Maintain an obligation/effect ledger for workflows requiring global completion knowledge. Otherwise report per-subscription outcomes honestly rather than inventing one “event processed” flag.

### Evolve and migrate contracts

Publish compatibility rules and retained fixtures. Additive fields are safe only when absence, unknown values, validation and old readers preserve meaning. A breaking semantic change gets a new type/version and explicit translation/migration horizon.

During dual publish/write, define authoritative stream, identity relationship, equivalence predicate, divergence metric, consumer cutover, rollback and retirement. Duplicating publications without a ledger can double effects. Replays use historical schemas/translators and immutable payloads; corrections are linked new messages.

### Secure every boundary

Authenticate producers, brokers, relays, routers, translators, stores, consumers and operators. Authorize publish/consume/admin by type, source, tenant, purpose, field, region and operation. Revalidate current authority for delayed high-impact commands. Prevent confused-deputy routing and cross-tenant keys.

Encrypt appropriately, minimize payloads, protect Claim Checks and DLQs, rotate keys/credentials, audit configuration/redrive, redact telemetry, and treat schemas/route rules as governed code. Trace context is correlation, not authorization or durable audit evidence.

### Model capacity and backpressure end to end

For serial stages, sustainable throughput is bounded by the slowest effective stage, including downstream effects. Fan-out work is \(\sum_m|O(m)|\) before retries. Retry amplification and catch-up after outage consume additional capacity. Partition skew makes aggregate averages misleading.

Set per-stage queues, concurrency, prefetch, rate/tenant quotas, storage/lag budgets and overload policies. Backpressure cannot travel automatically across every asynchronous boundary; define how signals become admission, throttling, pause, retention extension, or explicitly permitted shedding.

### Make evidence part of the design

For each stage record accepted/rejected counts, input/output identity/type/version, latency, queue/oldest age, attempts, route/translation version, effect/checkpoint, publication, integrity, authorization, retry/dead-letter, and terminal outcome. Trace causal paths with opaque IDs while keeping durable ledgers for correctness/audit.

Reconciliation compares producer state/outbox, broker obligations, payload objects, subscriber checkpoints, effect/inbox rows, outgoing messages and terminal failures. Dashboards are views over evidence, not the evidence itself.

### Verify the composed protocol

Review semantic contract and invariants first. Test schemas and mappings with boundary/unknown/old/new fixtures; run executable snippets/unit/property/model tests; integrate real broker/database/object/identity systems; inject crashes before/after every durable boundary; corrupt/reorder/duplicate/delay; expire leases/tokens; fail dependencies/regions; load steady, burst, skew and catch-up; test redrive/restore/key rotation; and conduct threat/privacy/operational exercises.

High-stakes flows additionally need named domain, safety, legal, privacy and practitioner review. Automation cannot prove clinical, financial or universal correctness.

## Definitions and Notation

| Symbol or term | Meaning |
| --- | --- |
| \(G=(V,E)\) | Directed integration-flow graph of stages and channels |
| \(S_i\) | Semantic contract visible before stage \(i\) |
| \(T_i\) | Typed, evidence-producing stage transition |
| \(O(m)\) | Logical obligation set created for message \(m\) |
| \(D_{m,o}\) | Delivery attempts for obligation \(o\) of \(m\) |
| \(E_{m,o}\) | Accepted business effects for that obligation |
| \(C_i\) | Sustainable useful capacity of stage \(i\) |
| \(h(m)\) | Stable partition/order key when required |
| correlation | Groups related interactions; does not imply causation or authority |
| causation | Identifies the message/decision that directly caused another message |
| terminal policy | Enumerated outcomes that close or explicitly retain an obligation |
| semantic drift | Change in meaning without corresponding contract/version/provenance change |

For a serial path, useful throughput is upper-bounded by \(\min_i C_i\). For fan-out, work grows with obligation count and each obligation has independent attempts/effects. These are capacity/accounting models, not latency or liveness proofs.

## Mechanisms, Invariants, or Proof Structure

### Composition argument

Assume the producer creates authenticated semantic contract \(S_0\). Every stage validates its input, preserves stable identity/authority/provenance/classification/outstanding obligations, or records an authorized typed change, and emits durable evidence. By induction over a finite path, the final effect can be traced to \(S_0\) with every semantic change explicit. A stage that silently defaults, drops identity, changes type, or loses obligations breaks the induction.

### Effect-safety argument

For each obligation, all delivery/redrive attempts reuse stable operation identity and commit through an atomic unique or conditional effect boundary before acknowledgement. Thus \(E_{m,o}\le1\). A valid available attempt plus recovery may establish \(E_{m,o}\ge1\); this liveness premise is separate. Flow completion additionally requires every obligation to reach an allowed terminal state.

### Capacity bound

Every message on a serial path must traverse every required stage, so no useful completion rate can exceed the least stage capacity. Fan-out creates independent downstream work and retries add load. Downstream saturation can reduce service and increase failure probability, so autoscaling an upstream stage cannot defeat the minimum bound and may worsen it.

### Executable semantic decision model

The deterministic model derives topology and payload strategy from declared message semantics and rejects a command with multiple owners. It is a decision-table illustration, not a broker, schema validator, authorization system, transaction, capacity model, or proof that the selected flow is sufficient.

<!-- bijux-verify: {"id":"semantic-flow-decisions","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"charge kind=command channel=point_to_point groups=1 key=order_id payload=claim delivery=at_least_once\norder kind=event channel=publish_subscribe groups=3 key=order_id payload=inline delivery=at_least_once\ninvalid=rejected reason=command_requires_one_owner\nchecks=identity,schema,authorization,idempotency,terminal_outcome\n","stderr":""}} -->
```python
def derive_flow(spec):
    if spec["kind"] == "command" and len(spec["owners"]) != 1:
        raise ValueError("command_requires_one_owner")
    if spec["kind"] == "event":
        channel = "publish_subscribe"
        groups = len(spec["subscribers"])
    else:
        channel = "point_to_point"
        groups = 1
    payload = "claim" if spec["payload_bytes"] > spec["inline_limit"] else "inline"
    return {
        "channel": channel,
        "groups": groups,
        "key": spec["ordering_key"],
        "payload": payload,
        "delivery": "at_least_once",
    }


charge = {
    "kind": "command",
    "owners": ["payments"],
    "subscribers": [],
    "ordering_key": "order_id",
    "payload_bytes": 400000,
    "inline_limit": 262144,
}
order = {
    "kind": "event",
    "owners": ["orders"],
    "subscribers": ["billing", "search", "audit"],
    "ordering_key": "order_id",
    "payload_bytes": 1200,
    "inline_limit": 262144,
}

for name, spec in [("charge", charge), ("order", order)]:
    flow = derive_flow(spec)
    print(
        f"{name} kind={spec['kind']} channel={flow['channel']} "
        f"groups={flow['groups']} key={flow['key']} "
        f"payload={flow['payload']} delivery={flow['delivery']}"
    )

invalid = dict(charge)
invalid["owners"] = ["payments", "orders"]
try:
    derive_flow(invalid)
except ValueError as error:
    print(f"invalid=rejected reason={error}")

checks = ["identity", "schema", "authorization", "idempotency", "terminal_outcome"]
print(f"checks={','.join(checks)}")
```

## Alternatives and Trade-Offs

| Decision | Alternative | Advantage | Cost or risk |
| --- | --- | --- | --- |
| Point-to-point command | Broadcast command | One decision owner and effect boundary | Requires explicit result/workflow for other interested parties |
| Pub/sub event | Direct callbacks | Independent subscribers and buffering | Fan-out obligations, retention, disclosure and schema evolution |
| Domain contracts/translators | Enterprise canonical model | Local ownership and bounded coupling | More explicit mappings to govern |
| Inline payload | Claim Check | One delivery boundary and low read latency | Broker bytes/exposure/limits |
| Claim Check | Inline payload | Specialized large/sensitive storage | Extra availability, authorization and lifecycle boundary |
| Partitioned order | Global order | Parallelism with per-key correctness | Key skew, rebalance and gap handling |
| At-least-once plus idempotency | At-most-once | Recovery without arbitrary effect duplication | Inbox/effect-state complexity |
| Choreographed reactions | Orchestrated workflow | Team independence and extensibility | Harder global completion/compensation visibility |
| Orchestrated workflow | Choreography | Explicit state, deadlines and compensation | Central workflow coupling/availability |
| Broker-managed retry/DLQ | Application workflow | Operational simplicity | Product-specific semantics and limited domain context |

Choose the smallest topology that expresses the actual obligations. More patterns do not imply a better design. A direct transactional call can be correct for a tightly coupled invariant; asynchronous messaging is not a universal replacement.

## Failure Modes and Misconceptions

- **“Start with the broker feature list.”** Products implement mechanisms; semantics determine which are appropriate.
- **“Everything is an event.”** Commands and documents have different authority, rejection, ownership, and completion.
- **“One topic decouples everyone.”** Shared schema, retention, security, partitions, cost and operational ownership remain coupling.
- **“A consumer group is a subscriber.”** Instances within one group share one obligation; separate groups create fan-out obligations.
- **“The canonical model removes translation.”** It relocates translation and can centralize semantic coupling.
- **“Correlation ID is idempotency ID.”** Correlation groups work; effect identity must name the logical operation.
- **“Broker order is business order.”** Concurrency, partitions, retries and effects require scoped sequence/version enforcement.
- **“At-least-once means duplicate effects.”** It means duplicate attempts; effect boundary determines accepted effects.
- **“Exactly once covers the flow.”** Product transactions cover named resources and cannot universally include arbitrary remote effects.
- **“Outbox solves the consumer side.”** Each effect/outgoing boundary needs inbox/conditional state and publication recovery.
- **“Trace completeness proves business completion.”** Sampling/loss and observation are not the obligation ledger.
- **“Retry preserves intent forever.”** Deadlines, current authorization, domain state and prior effects can invalidate it.
- **“DLQ means terminal.”** It is normally an owned unresolved state awaiting resolution.
- **“Dual publish is a safe migration.”** Without shared identity/equivalence and cutover rules it can diverge or double effects.
- **“Passing integration tests proves the design.”** Fault, load, skew, security, restore, evolution and human-domain evidence remain.

## Worked Examples

### Example 1

**Situation.** `ChargeCard` is sent to payments, fraud, and audit groups because all are “interested.”

**Reasoning.** It is a command: exactly one payments authority decides/executes the charge. Fraud may participate synchronously/as a decision dependency or consume facts; audit consumes `PaymentCharged`/`PaymentDeclined` events. Broadcasting the command risks multiple ownership and effects.

**Conclusion.** Route the command point-to-point to one owner and publish immutable outcome events for independent reactions.

### Example 2

**Situation.** `OrderPlaced` feeds billing, search, and analytics, each with several replicas.

**Reasoning.** The fact creates three logical obligations, not the sum of replicas. Use pub/sub with one durable group/subscription per responsibility. Each owns its lag, idempotency, retries, DLQ and retention. Scaling billing workers does not create another billing obligation.

**Conclusion.** Topology follows three independent reactions; worker count follows capacity.

### Example 3

**Situation.** A partner sends a tax document containing `amount=100`, currency omitted, and local date `03/04/26`.

**Reasoning.** A translator cannot guess currency/date convention. Reject/quarantine or require authoritative partner metadata. If mapping exists, record source schema, currency, date zone/format, precision and translator version; preserve original document identity/provenance.

**Conclusion.** Translation makes stated mappings, not semantic inventions.

### Example 4

**Situation.** A 40 MiB clinical image must accompany a small imaging event.

**Reasoning.** Keep patient/tenant, event/type, immutable object version, digest, length, classification and safe routing facts in the authenticated envelope; store bytes through Claim Check. Subscribers authenticate and reauthorize purpose, stream/verify content, and retain the object through every obligation. Do not publish a long-lived bearer URL.

**Conclusion.** Claim Check changes payload transport while preserving semantic and lifecycle contracts.

### Example 5

**Situation.** Account updates require per-account order; the stream has 32 partitions and 60 workers.

**Reasoning.** Partition by stable account ID. At most 32 traditional group members actively own partitions; hot accounts can dominate. Consumers require expected entity version/gap handling, because rebalance/retry and concurrent effects can still complicate outcomes.

**Conclusion.** Per-key order and bounded parallelism are explicit; global order and 60-way useful concurrency are not.

### Example 6

**Situation.** A consumer writes inventory state, publishes `InventoryReserved`, then acknowledges; it crashes between each step in tests.

**Reasoning.** Put inbox/operation claim, inventory conditional update and outgoing outbox in one database transaction. Relay the event idempotently; acknowledge input after commit. Crashes before commit retry the work; after commit retries observe the claim; relay failure leaves outbox evidence.

**Conclusion.** The durable transaction boundary converts crash windows into retry/reconciliation paths.

### Example 7

**Situation.** Notification provider errors trigger five immediate retries and then DLQ, even after the notification deadline.

**Reasoning.** Classify throttling/outage, use jittered delayed retry within deadline and provider capacity, preserve notification operation ID, and check prior provider result. Once expired, record cancellation/escalation rather than redrive. DLQ transfer/evidence needs an owner and resolution SLO.

**Conclusion.** Retry policy derives from changed-condition likelihood and business time, not a universal count.

### Example 8

**Situation.** One million events/hour match eight subscribers; each has 2% first-attempt retry.

**Reasoning.** Baseline obligation work is eight million deliveries/hour. Approximate one extra first retry per failed obligation adds 160,000 deliveries/hour, before replication/bytes/catch-up. Capacity and cost must be per group and downstream; producer call rate hides fan-out.

**Conclusion.** Fan-out accounting belongs in admission and capacity design.

### Example 9

**Situation.** A team migrates `CustomerChanged-v1` to v2 by publishing both with unrelated IDs.

**Reasoning.** Consumers may execute both and cannot compare equivalence. Define one authoritative occurrence identity, relationship between v1/v2, mapping/equivalence predicate, shadow consumers, divergence metrics, cutover ownership, rollback, and retirement. Prefer one event with compatible evolution when semantics allow.

**Conclusion.** Migration is a verified protocol, not duplicate traffic.

### Example 10

**Situation.** Hospital discharge triggers pharmacy, transport, records, and patient-notification work; consent and discharge status can change.

**Reasoning.** `DischargeApproved` is an authoritative fact only after clinical transaction/outbox. Each subscriber has independent obligation and current-state checks. Commands to transport/pharmacy have one owner, deadlines and cancellation. Partition by encounter where order matters; protect clinical payloads/claims; reconcile effects; escalate unresolved critical work to named humans.

**Conclusion.** High-stakes flow completion is a ledger of scoped, authorized outcomes—not one event acknowledgement.

## Cross-Program Connections

- [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md): bounded contexts, quality attributes, ADRs and evolution frame the flow decision record.
- [Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md): contract/property/model/fault/load/security/restore tests provide layered evidence.
- [Security Engineering](../../25-security-engineering/ROADMAP.md): identity, authorization, classification, integrity, key lifecycle, threat modeling and audit constrain every boundary.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md): failure ambiguity, ordering, idempotency, consensus limits and recovery explain end-to-end guarantees.
- [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md): service contracts, deadlines, idempotency, compatibility and dependency behavior connect synchronous and asynchronous boundaries.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md): broker/storage policies, quotas, telemetry, deployment, redrive and ownership make flows operable.

## References

1. Hohpe, Gregor, and Bobby Woolf. *Enterprise Integration Patterns*. Addison-Wesley, 2003. Messaging channels, construction, routing, transformation, endpoints, and systems-management patterns.
2. Hohpe, Gregor. *Enterprise Integration Patterns* pattern catalog. <https://www.enterpriseintegrationpatterns.com/patterns/messaging/>. Accessed 2026-08-29.
3. Cloud Native Computing Foundation. *CloudEvents Specification*, version 1.0.2 and current repository. <https://github.com/cloudevents/spec/blob/main/cloudevents/spec.md>. Accessed 2026-08-29.
4. AsyncAPI Initiative. *AsyncAPI Specification 3.0.0*. <https://www.asyncapi.com/docs/reference/specification/v3.0.0>. Accessed 2026-08-29.
5. W3C. *Trace Context*, W3C Recommendation, 23 November 2021. <https://www.w3.org/TR/trace-context/>.
6. OASIS. *Advanced Message Queuing Protocol (AMQP) Version 1.0*, 2012. <https://docs.oasis-open.org/amqp/core/v1.0/os/amqp-core-overview-v1.0-os.html>.
7. RabbitMQ. “Consumer Acknowledgements and Publisher Confirms.” Current documentation. <https://www.rabbitmq.com/docs/confirms>. Accessed 2026-08-29.
8. Apache Kafka. “Design.” Current documentation. <https://kafka.apache.org/design/>. Accessed 2026-08-29.
9. Fowler, Martin. *Patterns of Enterprise Application Architecture*. Addison-Wesley, 2002. Data source, distribution, concurrency, and domain patterns.
10. Kleppmann, Martin. *Designing Data-Intensive Applications*. O'Reilly, 2017. Encoding, replication, transactions, distributed faults, batch and stream processing.
11. Vernon, Vaughn. *Implementing Domain-Driven Design*. Addison-Wesley, 2013. Bounded contexts, domain events, integration, and context mapping.
12. Nygard, Michael T. *Release It!*, 2nd ed. Pragmatic Bookshelf, 2018. Stability, timeouts, circuit breakers, bulkheads, capacity and production feedback.

Protocol versions, broker guarantees, transaction scopes, quotas, CloudEvents/AsyncAPI features and trace bindings evolve. Current official sources were checked on 2026-08-29; implementations must verify exact product, protocol, client, queue type, storage, security and configuration behavior.

## Exercises

### Exercise 1

Given `ApproveRefund`, `RefundApproved`, and `RefundStatement`, classify each message, identify its authority/recipient obligations, and choose a logical channel topology.

### Exercise 2

A serial flow has stage capacities 900, 650, 800, and 500 useful messages/s. Each accepted event fans out to four subscribers; 5% of subscription attempts retry once. Derive the serial upper bound and expected downstream obligation attempts per 1,000 events under the simplified model. State what cannot be concluded.

### Exercise 3

Design the semantic envelope and effect transaction for `ReserveShipment(order_id, shipment_id, expected_version, deadline)`, including producer publication, ordering, Claim Check option, retry, result event, acknowledgement, and terminal outcomes.

### Exercise 4

Critique a design that publishes commands to one topic, lets any interested group act, translates missing fields with defaults, commits offsets before HTTP effects, uses payload URLs as authorization, globally retries forever, and purges the DLQ weekly. Produce a safer target flow and verification plan.

### Exercise 5

Design and review an integration flow for cross-border emergency blood-product allocation among hospitals. Address authority, message kinds, identity, order, inventory concurrency, privacy, payloads, translation, deadlines, delivery/effects, fan-out, compensation, failure isolation, current-state authorization, capacity, observability, recovery, and named human evidence.

## Answers to the Exercises

### Answer 1

`ApproveRefund` is a command: one refunds authority owns decision and effect, so use one logical point-to-point command channel/subscription with competing replicas only for capacity. `RefundApproved` is an immutable event from that authority; billing adjustment, notification and audit may each own a durable pub/sub subscription, while uninterested services have no obligation. `RefundStatement` is a document representation with authoritative source, as-of time, schema, integrity and named recipients/use; deliver directly or through recipient-specific channels, using Claim Check if large/sensitive. Preserve causation from command to outcome event and correlation across the case; do not use the statement as a command.

### Answer 2

Every message on the serial path must traverse every stage, so the upper bound is

\[
\min(900,650,800,500)=500\text{ messages/s}.
\]

Four subscribers create \(4\times1000=4000\) baseline obligation attempts. A 5% one-time retry adds \(0.05\times4000=200\), for 4,200 expected attempts under the simplified assumptions. This does not prove throughput or latency because fan-out stages may have different capacities, retry failures may correlate, message costs/sizes vary, partitions skew, downstream effects bind, queues absorb bursts, and the 500/s stage might occur before or after fan-out. Load/fault measurements and topology detail are required.

### Answer 3

Envelope fields include source/message ID, command type/version, requested/published time, tenant, `order_id` subject and ordering key, `shipment_id`, stable reservation operation ID, expected aggregate version, deadline, correlation/causation, schema/content type, classification, trace context, and payload or immutable Claim Check version/digest/length. One shipping authority owns a point-to-point subscription; replicas compete but partition/message-group by order when order transitions require serialization.

Producer commits requesting domain state and outbox command atomically; relay publishes same ID until confirmed. Consumer authenticates, validates schema/deadline/current authority and claim integrity, then in one transaction claims `(shipping-subscription,operation_id)`, conditionally updates shipment/inventory at `expected_version`, records terminal result and result-event outbox. Commit precedes acknowledgement. Outbox publishes `ShipmentReserved`, `ShipmentRejected`, or explicit cancellation/expiry fact with causation. Transient storage/dependency failure uses bounded delayed retry within deadline; version conflict re-reads/re-evaluates under domain policy; malformed/unauthorized/integrity failure quarantines; ambiguous external carrier effects use stable provider idempotency/reconciliation. Retry observes the operation record, not a second reservation.

### Answer 4

Broadcast commands create multiple decision owners; arbitrary defaults invent semantics; early offset commit loses ambiguous HTTP work; a URL is neither immutable identity nor current authorization; infinite retry amplifies permanent/outage failures; purging destroys unresolved evidence. Split each command to one owner and publish outcome events for independent subscribers. Define authenticated semantic envelopes and explicit loss/error translation rules. Use outbox/inbox or conditional effect state, stable HTTP idempotency keys and reconciliation, then checkpoint. Replace bare URLs with immutable Claim Check descriptors and authenticated purpose-bound redemption. Classify bounded retries by deadline/cost, isolate unresolved work with provenance/owner, and record terminal resolution rather than purge.

Verification begins with authority/obligation and schema/mapping review; fixtures for missing/unknown/old/new fields; duplicate/reorder/deadline/current-auth tests; crashes before/after effect/outbox/checkpoint; HTTP ambiguous-result simulation; claim corruption/expiry/access tests; broker/DLQ target outage; fan-out/skew/catch-up/downstream load; redrive canary; security/privacy threat tests; restore/key rotation; and reconciliation of producer, broker, claim, effect and terminal ledgers. Strong business or safety claims require named domain/practitioner review.

### Answer 5

A designated allocation authority owns `OfferBloodProduct`/`AcceptAllocation` commands and authoritative `ProductAllocated`, `OfferExpired`, `AllocationCancelled`, and `ProductTransferred` events. Hospitals do not all execute one broadcast command; recipient offers are individually addressed, deadline-bound and correlated to one allocation/workflow. Stable product, allocation, message, operation, hospital/tenant, causation and version identities are distinct. Inventory updates use one conditional transaction per product/version; partition/order by product or allocation and reject gaps/stale generations.

The envelope carries only required routing and safety facts, classification, origin/time-zone-normalized timestamps, deadline, compatibility schema, and signed provenance. Sensitive clinical documents use immutable encrypted Claim Checks with digest/length, region/purpose authorization, short-lived access minted at redemption, and retention across obligations. Translators explicitly map blood-type/product codes, units, expiry/time zone and regulatory identifiers; unknown/lossy mappings fail closed. Producer state plus outbox closes publication gaps; consumers use inbox/conditional effects, stable external idempotency and acknowledgement after durable commit.

Independent audit, logistics and safety subscribers each own lag, effects, retries and terminal evidence. Retry only while product, transport time, authority, recipient eligibility and deadline remain current; cancellation/supersession propagates as versioned workflow state. Ambiguous acceptance pauses the product workflow and escalates to authorized coordinators; compensation/reallocation is an explicit decision, never blind redrive. Security quarantine separates integrity/identity anomalies, and dead-letter transfer is confirmed/reconciled.

Capacity covers emergency bursts, per-hospital fairness, cold-chain/logistics providers, downstream concurrency, cross-region outage and catch-up. Observe oldest deadline slack, per-allocation state/sequence, attempts/effects, authorization, claim integrity, translation, subscriber lag, unresolved failures and human escalation using pseudonymous identifiers. Reconcile authority inventory, outbox, broker obligations, hospital responses, logistics effects, claimed documents and terminal outcomes. Test duplicate/concurrent acceptance, stale offers, clock/expiry boundaries, translation errors, region/key/identity/provider failures, malicious payloads, partitions, restore and manual fallback. Production approval requires named transfusion-medicine, logistics, safety, security, privacy, legal/regulatory and operations reviewers with simulation and incident-drill evidence.
