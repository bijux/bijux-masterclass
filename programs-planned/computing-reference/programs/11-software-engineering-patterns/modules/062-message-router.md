---
module_id: SEPAT-062
program: Software Engineering: Patterns
level: 2
module_number: 62
title: Message Router
status: complete
last_verified: 2026-08-29
---

# Message Router

## One-Page Review

### Governing question

How can an integration flow direct each immutable message to the correct zero, one, or many destination channels under versioned, testable, secure, observable, and failure-aware policy without coupling producers and processors or silently changing message meaning?

### Essential definitions

- A **Message Router** consumes a message from an input channel and republishes it to destination channel(s) selected by routing conditions.
- A **routing rule set** is a versioned policy mapping trusted message facts and context to a finite ordered set of routing actions.
- **first-match**, **best-match**, and **all-match** define how overlapping predicates resolve to one or several destinations.
- A **default route** handles valid messages unmatched by ordinary rules; an **invalid/quarantine route** handles malformed, unauthorized, or unsupported inputs.
- A **Content-Based Router** selects from message content or headers; a **Message Filter** produces zero or one downstream copy.
- A **Recipient List** computes several recipients; a **Routing Slip** carries a planned sequence; a **Dynamic Router** consults changing recipient capabilities.
- **routing transparency** means the producer need not know downstream topology, while operations can still reconstruct the decision.
- A **routing decision record** binds message identity, rule-set version, matched rule, destinations, time, and outcome without exposing sensitive payload.
- **route convergence** means every admitted message reaches a governed terminal state rather than looping or disappearing indefinitely.
- **partial fan-out** occurs when only some intended destination publications become durable.

### Central model, mechanism, or theorem

Let $M$ be valid messages, $D$ allowed destination channels, and $C_v$ a routing configuration version. A router is a policy function

$$
R_v:M\rightarrow D^*,
$$

where $D^*$ is a finite ordered sequence: length zero filters, one routes, and more than one forms a recipient list. Production execution must additionally record publication outcomes. For deterministic replay under historical policy,

$$
m_1=m_2\land v_1=v_2\Rightarrow R_{v_1}(m_1)=R_{v_2}(m_2),

$$

assuming pure predicates and stable referenced data. If rules call mutable services or current authorization, that equality does not hold; the decision evidence or policy inputs must be captured instead.

For a route graph $G=(D,E)$, a decreasing hop budget $h$ establishes finite forwarding only if every hop decrements $h$ and zero is quarantined rather than forwarded:

$$
h_{k+1}=h_k-1,\quad h_k\ge0\Rightarrow \text{at most }h_0\text{ routed hops}.
$$

### Critical invariants

- The router preserves message identity, type/version, causation, payload meaning, and security provenance; transformation belongs to an explicit translator/enricher.
- Only validated, authorized inputs and approved destinations participate in routing.
- Rule precedence and zero/one/many match semantics are explicit; overlap, gaps, and default behavior are tested.
- Every admitted message reaches durable destination publication, explicit filtered outcome, retry, or owned quarantine—never silent disappearance.
- Rule/configuration versions are immutable/auditable and deployments define old/new message and replay semantics.
- Publication retry reuses stable route-decision/output identities so duplicates can be deduplicated.
- Multi-destination routing defines partial-success recovery; it never implies cross-channel atomicity without a real protocol.
- Ordering/partition keys remain correct for each destination; routing cannot promise global order across outputs.
- Route graphs prevent uncontrolled cycles through topology analysis plus bounded hop/route history at runtime.
- Metrics/logs expose decisions, latency, failures, unmatched/overlap, fan-out, loop prevention, and lag without payload or high-cardinality leakage.

### Common failures

Common failures include routing and transforming in one opaque component, first-match rules whose order is accidental, overlapping all-match fan-out, unmatched messages dropped, default routes hiding new event types, rules based on untrusted headers, cross-tenant destination injection, per-message remote lookups without timeout/cache semantics, non-versioned configuration, replay under today's rules by accident, fan-out partial publication, duplicated messages with new identities, loops and amplification, loss of partition key/order, poison retry storms, hot destinations, high-cardinality metrics, and tests containing only one positive example per rule.

### Compact example

A pure first-match router uses immutable `routing-7` rules. EU invoices go to `finance-eu`, other invoices to `finance-global`, and unknown supported envelopes to `quarantine`. Three input dictionaries remain byte-for-byte equivalent at the modeled level, message IDs are preserved, and the decision reports the rule name and configuration version.

### Connections

[SEPAT-061](061-message-channel.md) defines the transport obligations around the router; [SEPAT-063](../ROADMAP.md) translates incompatible message representations. Routing also connects to [Distributed Systems](../../27-distributed-systems-engineering/ROADMAP.md), [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md), [Security Engineering](../../25-security-engineering/ROADMAP.md), and [Platform Engineering](../../29-platform-engineering/ROADMAP.md).

## Governing Question

How should one component own destination selection so producers and processors remain decoupled while routing policy, configuration, correctness, security, delivery, evolution, and operational consequences remain explicit?

The router is not “some if statements between queues.” It is a policy enforcement and topology component whose decision can determine which system sees a fact, which legal region processes data, whether an ordered stream is preserved, and whether downstream work occurs once, many times, or not at all.

## Why This Matters

Without a router, producers often learn every consumer address and embed changing topology. Adding a processor then changes producers; routing logic duplicates across clients; and operations cannot explain why one message reached one service but not another.

Centralized routing localizes destination policy but also concentrates risk. A faulty wildcard can fan out millions of messages, a missing default can lose new types, and a cross-tenant rule can disclose data. Production routing needs the rigor of an API and security policy plus the failure reasoning of messaging.

## Prerequisites and Retrieval

You should understand Message Channel, immutable envelopes, publisher confirms, consumer acknowledgements, outbox/inbox, idempotency, schemas, partitions/order, authorization, configuration deployment, graphs, and observability. Retrieve these facts:

1. Broker acceptance of an input delivery and durable publication to every output are distinct events.
2. Acknowledging input before outputs are durably recorded can lose the routed message; publishing then crashing before input acknowledgement can duplicate it.
3. First-match behavior makes rule order semantic; all-match behavior makes overlap a fan-out decision.
4. A message routed to two independent channels cannot generally be published atomically across both without a shared transaction/protocol.
5. Reusing a message ID does not prevent each consumer from needing its own idempotency boundary.
6. Content and headers can be malformed, spoofed, stale, ambiguous, encrypted, or privacy-sensitive.
7. A graph that is acyclic in configuration can still loop through external bridges or dynamic routes.

## Learning Objectives

After completing this module, you should be able to:

- distinguish a Message Router from channels, brokers, translators, filters, recipients, routing slips, process managers, and service discovery;
- formalize routing as a zero/one/many policy with explicit precedence and default semantics;
- preserve identity, meaning, provenance, partitioning, and security context across a routing hop;
- design transactional/durable input-to-output publication with idempotent retry and partial fan-out recovery;
- version, validate, stage, canary, audit, roll back, and replay routing configuration;
- prevent gaps, unintended overlaps, wildcard amplification, cycles, cross-tenant routing, and destination injection;
- reason about static, content-based, dynamic, recipient-list, and itinerary routing variants;
- bound remote decision dependencies, capacity, fan-out, latency, and downstream pressure;
- instrument route decisions and verify topology, schemas, authorization, ordering, faults, and load;
- review high-stakes routing with named domain, privacy, safety, accessibility, security, and operations owners.

## Core Exposition

### Keep the router's responsibility narrow

The classic router changes destination, not message content. It may append protected routing metadata/history if the envelope contract permits, but business payload translation, enrichment, splitting, aggregation, and processing should be explicit neighboring stages. Narrow responsibility makes replay and diagnosis possible.

If routing requires normalized fields, translate/validate before routing under a named schema. Do not let each predicate interpret units, aliases, or optional fields differently.

### Define zero, one, or many outputs

A filter deliberately returns zero destinations and records why. An exclusive router returns exactly one. A recipient list returns several unique destinations. These cardinalities have different delivery and ownership semantics.

State whether duplicate destination names are collapsed, order matters, a default counts as normal or quarantine, and empty is permitted. For commands, multiple recipients can create multiple actors competing to own one decision; for events, independent fan-out is often appropriate.

### Make predicate semantics total

For every supported schema version, predicates must define missing, null, malformed, unexpected enum, numeric precision/unit, case/Unicode, time zone, boundary, and unknown future values. A rule that throws is a routing failure, not “no match.”

Validate envelope/schema before policy. Use closed destination identifiers from configuration, never an arbitrary message-provided URI. Limit expression complexity, execution time, memory, recursion, and regex behavior.

### Choose match resolution explicitly

**First-match** evaluates ordered rules until one matches; precedence is part of configuration and shadowed rules must be detected. **All-match** evaluates all predicates and returns the union; overlap is expected but fan-out must be bounded. **Best-match** assigns explicit comparable priority/specificity and rejects unresolved ties.

Do not rely on map iteration or UI display order. Validate duplicate priorities, equivalent predicates, unreachable rules, ambiguous ties, and gaps before activation.

### Design defaults by message semantics

A default business destination can provide forward compatibility only when unknown variants are genuinely safe there. Otherwise default to owned quarantine/invalid-message handling. Dropping may be correct for an explicit filter but must produce a decision record and metric.

An ever-growing “other” route hides contract drift. Alert on unmatched/default rate and sample privacy-safe metadata. New type/version deployment should have an explicit producer-consumer-router compatibility plan.

### Preserve the message contract

Keep stable message identity across retry and routing so downstream dedupe/correlation works. Preserve source, type/version, occurred time, tenant, partition key, correlation, causation, and integrity metadata. A route attempt/output publication receives its own derived identity such as `(message_id, rules_version, destination)` without replacing original identity.

If the router unwraps or re-signs an envelope, document trust transition. Do not copy untrusted routing headers into privileged broker properties.

### Close the input-output failure gap

A router can durably store a route decision and intended outputs in one local transaction/inbox-outbox, then acknowledge input. Relays publish each output with stable derived identity and track confirmation. This avoids relying on an unavailable atomic transaction across input broker and all output channels.

Alternatively a broker-native transaction may cover specific channels/partitions, but state exact scope and failure assumptions. On crash after output publish before input ack, retry must recognize existing decision/output identities rather than choose new rules or duplicate effects blindly.

### Treat fan-out as a workflow

For destinations $d_1,\ldots,d_n$, track each intended output independently: pending, confirmed, terminally rejected, cancelled, or quarantined. “Router succeeded” needs a policy—perhaps all mandatory destinations confirmed while optional telemetry may fail separately.

Do not roll back an already observed external message by wishful thinking. Retry missing outputs idempotently, reconcile, or issue explicit compensation/correction where domain semantics allow. Preserve which rule created each obligation.

### Preserve ordering only where promised

Input partition order can be preserved per destination if the router processes/commits in order and uses a consistent output key. Fan-out creates independent streams whose relative delivery/effect order can diverge. Multiple router instances can reorder without per-key sequencing.

If ordered entity transitions matter, bind decision/output to entity version, retain partition key, and have consumers reject/buffer/reconcile duplicates, gaps, and stale versions. A slow/failed destination should not silently determine order policy for unrelated outputs.

### Prevent loops and amplification

Analyze the declared channel-router graph for cycles. Dynamic recipients, bridges, replay, and externally configured targets require runtime defenses: hop count/TTL, route history, origin, visited logical stages, duplicate route-decision detection, and bounded fan-out.

A loop can grow multiplicatively when each pass fans out. Alert on hop-limit, repeated stage, abnormal publish/input ratio, and rapid rule-trigger loops. Quarantine at the safety bound; do not discard evidence or automatically restart the loop.

### Separate routing from orchestration

A router makes a stateless/limited decision about the next destination(s). A Routing Slip carries an itinerary. A Process Manager/Saga maintains long-lived business state, waits for outcomes, handles timeouts, and chooses subsequent commands. Dynamic Router recipients may advertise capabilities but still require bounded discovery semantics.

Do not implement a multi-day order workflow as a giant routing expression. Conversely, do not introduce a workflow engine for a pure type-to-channel mapping.

### Understand common router variants

- **Content-Based Router:** selects based on stable message facts; developed in SEPAT-065.
- **Message Filter:** drops/retains one stream under explicit terminal policy.
- **Recipient List:** computes multiple recipients, often from policy or message metadata.
- **Dynamic Router:** obtains candidate recipients/capabilities at runtime and iterates or selects.
- **Routing Slip:** message carries a controlled sequence of processing steps.
- **Splitter/Aggregator/Scatter-Gather:** alter message cardinality and correlation, beyond basic routing.
- **Publish-Subscribe Channel:** broker topology makes every subscription a recipient; unlike one router decision, groups own independent delivery.

Name the variant because its failure and cardinality semantics differ.

### Govern dynamic decisions

Remote policy, service discovery, feature flags, tenant configuration, or ML classification can inform routing. Define snapshot/version, cache/TTL, timeout, stale behavior, authorization, consistency, and replay. A per-message synchronous remote lookup can turn buffering into a fragile dependency.

If historical replay must reproduce original routing, store the decision and inputs/model/policy version. If replay intentionally uses current policy, label it as reprocessing and prevent duplicate historical business effects.

### Secure the routing plane

Authorize producer to input type/tenant and router to each output. Rules/configuration changes require strong identity, least privilege, review, audit, separation of duties where warranted, signing/integrity, and rollback. Broker ACLs should prevent producers bypassing the router to privileged destinations.

Do not use client-supplied `destination`, role, region, or tenant without trusted derivation/validation. Content inspection may expose sensitive data; route using minimal classified metadata where possible and keep decision logs redacted.

### Version and deploy rules safely

Treat rule set as immutable versioned code/config with schema, owner, rationale, effective window, and checksum. Validate syntax/types/destinations/ACLs, perform static overlap/gap/cycle/reachability analysis, and test a governed corpus including counterexamples and unknown future fields.

Shadow new rules without publishing, compare decisions, bound cardinality/cost changes, canary a subset, monitor, then promote. Preserve prior version for rollback. Define messages already in flight and decisions persisted under the old version.

### Avoid configuration split brain

Router instances must expose active version and converge under a rollout protocol. Mixed versions can route adjacent entity events differently. If that is unsafe, fence activation by epoch, drain, partition assignment, or central decision record.

Control-plane availability should not require every data-plane message to fetch configuration. Cache a verified immutable version and choose fail-closed/stale-safe behavior based on policy.

### Bound performance and blast radius

Budget rule evaluation, remote lookups, fan-out, message size, input/output rates, in-flight decisions, retries, and destination backpressure. One slow output can use independent relay queues to isolate other destinations while preserving per-output obligation.

Reject configuration whose theoretical fan-out or wildcard match exceeds limits. Load-test representative and adversarial distributions, not only uniform data. Consider hot types/tenants/keys and rule evaluation order cost without changing semantics.

### Observe decisions without leaking data

Record input identity (appropriately bounded/hashed), schema/type, tenant class rather than raw tenant where possible, rule-set version, matched rule, destination count/names from a fixed set, decision/publish outcome, duration, retry, hop count, and error category. Trace output publications to input causation.

Metrics include unmatched/default/invalid/denied, overlap/tie, decision latency, fan-out ratio, per-destination confirmation/lag/failure, retries, duplicate decisions, rule-version skew, loop prevention, and quarantine age. Payload and arbitrary rule values do not belong in metric labels.

### Test the policy and mechanism

Use table/property/mutation tests for every rule boundary, missing/null/malformed/unknown fields, precedence, overlap, default, cardinality, identity preservation, destination allowlist, hop budget, and stable replay. Generate counterexamples near numeric/time/string boundaries.

Integration-test real schema validator, policy engine/router runtime, broker ACL/routing, input acknowledgment, output confirms, inbox-outbox, partition/order, rule deployment, and observability. Fault-inject crash before/after decision storage, each output, confirm, and input ack; deny destinations; lose control plane; mix versions; slow one output; loop/duplicate/replay. Load-test worst permitted fan-out and downstream recovery.

### Review high-stakes routing as policy

Routing clinical, financial, safety, or regulated messages can decide who acts and where data travels. Explicitly model jurisdiction, consent/purpose, professional authority, urgency, current state/version, downtime, escalation, and human override. Unknown or conflicting evidence must not fall through a convenient default.

Named domain, affected-user, privacy/legal/regulatory, security, accessibility/human-factors, data, and operations reviewers validate real rules and failure workflows. A correct predicate engine cannot validate the policy it was given.

### Executable model: versioned first-match routing

This finite pure router evaluates two ordered rules and a quarantine default. It preserves its modeled input dictionaries and reports stable identity, destination, matched rule, and rule-set version. It does not publish messages or model concurrency, security, schemas, configuration rollout, or failure.

<!-- bijux-verify: {"id":"message-router-first-match","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"m-1 destination=finance-eu rule=eu-invoice version=routing-7 preserved=True\nm-2 destination=finance-global rule=invoice-default version=routing-7 preserved=True\nm-3 destination=quarantine rule=unmatched version=routing-7 preserved=True\n","stderr":""}} -->
```python
RULES_VERSION = "routing-7"


def decide(message):
    headers = message["headers"]
    if headers["type"] == "invoice-issued" and headers["region"] == "eu":
        return ("finance-eu", "eu-invoice", RULES_VERSION)
    if headers["type"] == "invoice-issued":
        return ("finance-global", "invoice-default", RULES_VERSION)
    return ("quarantine", "unmatched", RULES_VERSION)


messages = [
    {"id": "m-1", "headers": {"type": "invoice-issued", "region": "eu"}, "body": 120},
    {"id": "m-2", "headers": {"type": "invoice-issued", "region": "us"}, "body": 80},
    {"id": "m-3", "headers": {"type": "new-type", "region": "eu"}, "body": 5},
]

snapshots = [repr(message) for message in messages]
for index, message in enumerate(messages):
    destination, rule, version = decide(message)
    preserved = repr(message) == snapshots[index]
    print(f"{message['id']} destination={destination} rule={rule} version={version} preserved={preserved}")
```

### Finite invariant argument

`m-1` satisfies the first conjunction, so first-match returns `finance-eu` and does not evaluate the second return. `m-2` fails the region conjunct but satisfies invoice type, so it returns `finance-global`. `m-3` fails both invoice predicates and reaches quarantine. All decisions return `routing-7` and one rule name.

`decide` only reads dictionaries and returns new strings/tuple; the loop only reads inputs. Therefore each `repr` equals its snapshot and `preserved=True` for this serialized finite trace. Exact output order follows list order. The argument depends on dictionaries containing required fields and on deterministic equality/representation. Production code must validate missing/malformed fields, restrict destinations, persist decisions/outputs, and handle failures; this proof establishes none of those.

### Evidence classification

The snippet report is empirical evidence for three deterministic decisions and input preservation in the stated interpreter. Branch outcomes are independently recomputable. It provides no broker, delivery, transaction, configuration, concurrency, authorization, privacy, performance, or real policy evidence.

## Definitions and Notation

A validated message is $m=(id,type,version,tenant,key,source,causation,payload,metadata)$. Routing policy $C_v$ contains ordered predicates $p_i$, output functions/constant destinations $o_i$, resolution semantics $s$, default $d_0$, allowed destination set $D$, and safety bounds.

For first-match,

$$
R_v(m)=o_k(m),\quad k=\min\{i\mid p_i(m)=\mathrm{true}\},
$$

or default when the set is empty. For all-match, output is the stable deduplicated union of all $o_i(m)$ with true predicates. Best-match additionally requires a total priority/tie policy.

A route-output identity $rid=(m.id,v,rule,destination,ordinal)$ supports idempotent publication tracking without changing $m.id$. Decision record $J=(m.id,v,rule,R_v(m),time,outcomes)$ is protected evidence, not a copy of sensitive payload.

Route graph $G=(D,E)$, maximum hop budget $H$, actual hop $h$, and route history $V_m$ support static and runtime cycle analysis. Fan-out factor $f(m)=|R_v(m)|$ is bounded by configured $F_{max}$.

## Mechanisms, Invariants, or Proof Structure

The mechanism separates four planes: data plane validates and decides; durable execution plane records decision/output obligations and relays them; control plane validates/versions/deploys rules; evidence plane records bounded decisions, metrics, traces, and reconciliation. Combining them in one process is possible, but their ownership and failure boundaries remain distinct.

Safety obligations are:

1. **Preservation:** routing does not alter message meaning/identity/provenance.
2. **Totality:** every admitted supported input yields a governed finite outcome or typed failure.
3. **Destination confinement:** every output belongs to authorized $D$ for tenant/type/context.
4. **Resolution:** rule ordering/overlap/ties/default yield deterministic cardinality under $C_v$.
5. **Durable obligation:** input is not acknowledged before decision/intended outputs are recoverable.
6. **Idempotent execution:** retry under the same decision cannot create a new logical output obligation.
7. **Bounded traversal:** hop/fan-out and cycle policy prevent unbounded amplification.
8. **Version accountability:** each decision binds immutable rule version and compatibility premises.
9. **Ordering honesty:** only scoped per-key/destination order is claimed and consumers validate versions.
10. **Terminal evidence:** every intended output becomes confirmed, explicitly cancelled/rejected, or owned unresolved work.

Finite proofs can establish pure predicate coverage/disjointness for bounded domains, precedence, preservation, and graph bounds. Static analyzers can find declared cycles/shadowed rules. Database/broker fault tests establish implemented recovery under selected failures. Load/security/privacy/domain reviews address other claims. Dynamic remote policy and arbitrary payload domains prevent general exhaustive proof; use constraints, generated counterexamples, runtime guards, and reconciliation.

## Alternatives and Trade-Offs

| Approach | Destination knowledge | Strong fit | Main risk |
|---|---|---|---|
| Producer-directed publish | Producer | Stable simple topology | Producer/consumer coupling, bypass |
| Broker bindings/subscriptions | Broker control plane | Declarative type/topic routing | Hidden rule overlap/vendor semantics |
| Message Router | Central policy component | Governed conditional selection | Bottleneck/policy blast radius |
| Recipient List | Policy/message-derived list | Intended fan-out | Partial publication/amplification |
| Routing Slip | Controlled itinerary | Per-message processing sequence | Tampering/version/loop complexity |
| Dynamic Router | Runtime capability discovery | Changing recipient capabilities | Nondeterminism/dependency latency |
| Process Manager | Stateful workflow owner | Long-lived decisions/timeouts | State/operational complexity |
| Publish-subscribe | Independent subscriptions | Fact fan-out | Each group adds obligation/lag |

Broker-native and application routers can coexist. Ensure exactly one layer owns each decision or prove how filters compose; otherwise diagnosis and coverage become opaque.

## Failure Modes and Misconceptions

- **“A router is just a switch statement.”** It owns versioned policy, delivery obligations, security, configuration, and operational evidence.
- **“It may normalize while routing.”** Hidden transformation changes replay and schema semantics; use an explicit translator.
- **“First matching rule is obvious.”** Precedence is behavior and can shadow later rules.
- **“All matching rules means pub/sub.”** Recipient computation differs from independently governed subscriptions, retention, and group offsets.
- **“Default prevents loss.”** It may silently misroute new/unknown types; quarantine and alert can be safer.
- **“No destination means ignore.”** Filtering is a terminal business outcome that needs policy/evidence.
- **“One message ID prevents duplicates.”** Every output/consumer still needs stable obligation identity and idempotent effect.
- **“Fan-out is atomic.”** Independent channels can partially succeed; track each output.
- **“Replay should use current rules.”** That can change recipients and duplicate effects; state replay purpose/version.
- **“Rule config is harmless.”** It is executable policy with a potentially system-wide security/cost blast radius.
- **“Service discovery makes routing dynamic safely.”** Mutable membership adds timeout, staleness, authorization, and reproducibility problems.
- **“Hop count alone prevents every loop.”** It bounds damage but does not repair topology or duplicated effects.
- **“Preserving input partition preserves all order.”** Outputs are independent and parallel processing changes effect order.
- **“Metrics can label message ID/tenant.”** That creates cardinality/privacy hazards; use bounded dimensions and traces.
- **“Matching tests validate policy.”** They validate encoding; domain/security reviewers validate what should happen.

## Worked Examples

### Example 1

**Situation.** An order producer knows five regional fulfillment queues and chooses one itself.

**Reasoning.** Topology and regional policy are duplicated in producers. Publish one validated order fact/command to an input; a versioned router derives authorized region destination and records the decision.

**Conclusion.** Central routing decouples producers from changing processors.

### Example 2

**Situation.** Rules are `amount > 100` then `amount > 1000`; first-match sends a 5000 transaction to ordinary review.

**Reasoning.** The broader predicate shadows the specific rule. Order specific-first or define explicit priority/best-match and reject shadowed configuration.

**Conclusion.** Rule precedence must be validated as semantics.

### Example 3

**Situation.** An all-match router sends an invoice to `finance` twice because two rules compute the same destination.

**Reasoning.** Define recipient set versus multiset semantics. Usually stable-deduplicate destination obligations while preserving which rules matched for audit.

**Conclusion.** Fan-out cardinality and duplicate recipient policy are explicit.

### Example 4

**Situation.** Router publishes to billing, crashes before analytics, and input redelivers under a newer rule version.

**Reasoning.** Persist original version/decision plus per-output obligations before input ack. Retry missing analytics and recognize confirmed billing by stable route-output identity.

**Conclusion.** Durable decisions prevent partial fan-out from becoming nondeterministic rerouting.

### Example 5

**Situation.** A message header supplies `destination=https://internal-admin`.

**Reasoning.** Untrusted address creates SSRF/privilege bypass. Map validated facts to a closed authorized logical destination set; enforce router and broker ACLs.

**Conclusion.** Routing input is data, never direct authority.

### Example 6

**Situation.** A dynamic router calls a registry for every message; registry outage stops all processing.

**Reasoning.** Use verified versioned capability snapshots/cache with expiry and fail-closed/stale-safe policy, or persist decision. Bound timeout and isolate control from data plane.

**Conclusion.** Dynamic routing must declare dependency and replay semantics.

### Example 7

**Situation.** Channels A and B route to each other, each fan-out also sends back to A.

**Reasoning.** Static graph analysis finds declared cycle; hop budget and route history bound undeclared/bridge loops. Quarantine and alert on repeated stage/amplification.

**Conclusion.** Prevent cycles both before deployment and at runtime.

### Example 8

**Situation.** EU and US messages retain input key, but one output overwrites it with random UUID.

**Reasoning.** Entity transitions lose per-key order and distribute inconsistently. Preserve scoped entity key or define an intentional versioned repartition, and validate consumer versions/gaps.

**Conclusion.** Destination selection includes partition semantics.

### Example 9

**Situation.** A wildcard rule update increases average fan-out from 1.2 to 40 and overloads every consumer.

**Reasoning.** Static maximum, shadow corpus comparison, canary, rate/admission limits, output isolation, and fan-out SLO should reject or contain the change.

**Conclusion.** Rule changes require capacity and blast-radius evidence.

### Example 10

**Situation.** A clinical referral router defaults unknown specialty codes to general scheduling across regions.

**Reasoning.** Unknown code may misroute urgent care or protected data. Quarantine/escalate with patient-safe status, current consent/jurisdiction/urgency checks, accessible operator workflow, audit, and named clinical/privacy review.

**Conclusion.** High-stakes unknowns cannot silently use a convenient default.

## Cross-Program Connections

- [Distributed Systems](../../27-distributed-systems-engineering/ROADMAP.md) develops deterministic state, failure, replication, ordering, delivery, and graph/topology reasoning.
- [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) supplies event/command schemas, compatibility, idempotency, and asynchronous operation contracts.
- [Database Engineering](../../18-database-engineering/ROADMAP.md) grounds inbox-outbox, uniqueness, transactions, decision logs, and reconciliation.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) supplies policy authorization, tenant confinement, SSRF/injection defense, privacy, and control-plane protection.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md) operates configuration rollout, brokers, capacity, telemetry, recovery, and cost controls.
- [Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) provides property, mutation, contract, fault, load, security, and deployment evidence.
- [SEPAT-061](061-message-channel.md) defines input/output delivery; [SEPAT-063](../ROADMAP.md) handles explicit representation translation.

## References

1. Gregor Hohpe and Bobby Woolf, *Enterprise Integration Patterns*, Addison-Wesley, 2003. Message Router and routing specializations.
2. Enterprise Integration Patterns, [“Message Router”](https://www.enterpriseintegrationpatterns.com/patterns/messaging/MessageRouter.html), accessed 2026-08-29. Pattern problem, solution, and responsibility boundary.
3. Enterprise Integration Patterns, [“Messaging Patterns Overview”](https://www.enterpriseintegrationpatterns.com/patterns/messaging/index.html), accessed 2026-08-29. Router variants and relationships.
4. Apache Camel, [“Choice”](https://camel.apache.org/components/4.14.x/eips/choice-eip.html), 4.14 LTS documentation accessed 2026-08-29. Content-based choice mechanics.
5. Apache Camel, [“Recipient List”](https://camel.apache.org/components/4.14.x/eips/recipientList-eip.html), 4.14 LTS documentation accessed 2026-08-29. Multi-recipient routing mechanics and options.
6. Apache Camel, [“Routing Slip”](https://camel.apache.org/components/4.14.x/eips/routingSlip-eip.html), 4.14 LTS documentation accessed 2026-08-29. Itinerary routing mechanics and options.
7. Amazon Web Services, [“Creating Amazon EventBridge event patterns”](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-event-patterns.html), accessed 2026-08-29. Declarative event matching and targets.
8. Amazon Web Services, [“Best practices for Amazon EventBridge event patterns”](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-patterns-best-practices.html), accessed 2026-08-29. Pattern precision, loops, and cost controls.
9. Clemens Vasters et al., [“CloudEvents Specification”](https://github.com/cloudevents/spec), current specification repository accessed 2026-08-29. Stable event context/provenance attributes.
10. Martin Kleppmann, *Designing Data-Intensive Applications*, O’Reilly, 2017. Streams, partitioning, ordering, delivery, derived data, and distributed failure.

## Exercises

### Exercise 1

Given six overlapping routing rules for transaction amount, country, risk, and schema version, define first/all/best-match semantics, find shadows/gaps/ties, and design a counterexample test corpus plus safe default.

### Exercise 2

Design durable routing from one input to three mandatory destinations and one optional analytics destination. Specify decision/output identities, transactions, acknowledgements, confirms, retry, partial success, ordering, and reconciliation.

### Exercise 3

Design a dynamic tenant-aware regional router. Cover trusted inputs, capability/config snapshots, authorization/jurisdiction, cache/control-plane failure, version rollout, replay, loops, capacity, observability, and security tests.

### Exercise 4

Plan migration from producer-directed destinations to a central router without duplicate or lost effects. Include compatibility, shadowing, cutover authority, rollback/forward, and evidence gates.

### Exercise 5

Review a high-stakes clinical referral router. Cover schema/unknowns, urgency/specialty/region/consent, authoritative state, delivery/fan-out, override/escalation, privacy/security, accessibility, operations, verification, and named human review.

## Answers to the Exercises

### Answer 1

Normalize/validate one schema with explicit amount unit/currency, country enum, risk evidence/version, and missing/null behavior. For exclusive routing, use explicit priority: invalid/unsupported schema first to quarantine; denied/jurisdiction restriction; critical risk; high amount; regional ordinary; final owned unmatched. Reject duplicate priority/ties and use specificity only if formally defined. All-match is appropriate only if outputs are independent event subscribers; stable-deduplicate destinations and cap fan-out.

Static analysis checks predicate implication/intersection: e.g., `amount>100` before `amount>1000` shadows the latter under first-match; country rules omit unknown/new codes; inclusive boundaries overlap at exactly 1000; risk missing may throw or fall through. Corpus covers every rule true and false, pairwise/all overlaps, threshold ± smallest unit, unknown/null/malformed schema fields, Unicode/case, unsupported versions, denied tenant/country, and generated property tests that exactly one exclusive terminal result occurs. Default is quarantine/owned review rather than ordinary processing when semantics are unknown.

### Answer 2

Consumer transaction claims input identity and stores immutable `(message_id,rules_version,matched_rule)` decision plus four output rows keyed `(message_id,rules_version,destination)` with mandatory flag, payload reference/digest, partition key, and pending state; then input may be acknowledged. Independent relays publish each row with original message identity/derived output ID, await destination confirmation, and atomically mark confirmed. Uncertain confirmation republishes the same ID; destination consumers remain idempotent.

Overall mandatory success requires all three mandatory confirmations; optional analytics failure is visible under its separate retry/expiry policy and cannot falsely fail already completed business routing. Permanent mandatory rejection quarantines/alerts and stays unresolved until approved cancellation/correction; no rollback is claimed for observed outputs. Preserve entity key/version per destination and sequence obligations appropriately. Reconcile input inbox to decisions, decisions to intended outputs, outputs to confirms, and downstream inbox/effects; alert age, retry, skew, and mismatch. Crash tests cover every storage/publish/confirm/ack boundary.

### Answer 3

Inputs derive tenant, data classification, entity/region, event type/version, and purpose from authenticated producer/envelope plus authoritative policy—not arbitrary destination headers. Immutable signed configuration maps tenant/data class/jurisdiction to an allowlisted logical destination and capability snapshot version. Router and broker ACLs enforce tenant/channel confinement; payload is minimized/encrypted and decision logs redact identifiers.

Data plane caches a verified version and exposes it; control-plane outage uses the last version only within approved validity, otherwise fails closed/quarantines. Activation validates schema/destinations/ACLs/gaps/overlap/cycles/fan-out, shadows and canaries decisions, fences unsafe mixed epochs, and retains rollback. Persist decision version/outputs so delivery retry/replay does not consult changing discovery; intentional current-policy reprocessing is a new governed operation. Hop budget/history, output isolation, per-tenant/fan-out/rate limits, skew tests, and downstream capacity bound damage. Tests cover cross-tenant spoofing, destination injection/SSRF, stale/revoked policy, key rotation, mixed versions, registry loss, loop, hot tenant, replay, and authorization/jurisdiction changes.

### Answer 4

Inventory every producer/type/destination, current IDs, ordering keys, delivery/effect semantics, and bypass ACL. Introduce stable input channel and router in shadow mode: producers continue direct publication while also record or emit a non-effecting shadow input; compare intended destinations, payload digests, order keys, and volumes without delivering twice. Correct rule/schema/authorization differences and exercise fault/load/config rollback.

For one message type/tenant slice, make a transactional producer outbox publish only to router input; router decision/outbox becomes sole destination publisher. Fence producer direct credentials for that slice and use stable business IDs so downstream dedupe protects uncertainty. Monitor outbox-input-decision-output-downstream reconciliation, lag, duplicate/default/quarantine, ordering versions, and effects. Expand canaries. Rollback routes new inputs through the prior producer-compatible bridge or restores one authoritative path—never both. Preserve old/new schema overlap and historical in-flight decisions. Remove direct routes/ACLs only after drain and reconciliation prove zero unresolved/mismatched obligations; retain forward recovery for already routed messages.

### Answer 5

Validate a versioned referral envelope with patient/tenant, originating professional, purpose/consent, specialty code system/version, urgency evidence, location/jurisdiction, accessibility/language needs, referral/version, occurred/expiry, and provenance. Unknown, conflicting, stale, or unsupported specialty/urgency/consent never defaults to ordinary scheduling; it enters a time-bounded, patient-visible, accessible clinical escalation with safe interim guidance under approved policy.

The source transaction stores referral, audit, and outbox. Router rechecks current referral/version/cancellation, jurisdiction/consent/purpose and professional/system authority, persists immutable decision/rules version and mandatory output obligations, then acknowledges. Stable identities/destination inboxes handle retry. Fan-out to clinical scheduling and required safety escalation tracks each confirmation; optional analytics receives minimized/deidentified data under separate authority. Preserve urgency order/key and reject gaps/stale versions.

Protect control-plane changes with clinical/privacy/security approval, separation of duties, audit, allowlists/ACLs, encryption/key rotation, and rollback. UI/work queue distinguishes pending, routed, unavailable, conflicted, overridden, expired, and acknowledged using keyboard/screen-reader/color-independent cues; records override reason and avoids alert fatigue. Test schema boundaries, clinical rule vectors, unknowns, authorization/tenant attacks, crashes/duplicates/gaps/order, partial fan-out, rule mixed versions, outage/loop/load, accessibility, privacy/retention, reconciliation, and disaster recovery. Named clinicians for each specialty/triage, clinical safety/informatics, scheduling staff, patients/representatives, privacy/legal/regulatory, security, accessibility/human-factors, data/messaging/SRE, and incident-response owners review real policy. Automated routing cannot establish clinical correctness.
