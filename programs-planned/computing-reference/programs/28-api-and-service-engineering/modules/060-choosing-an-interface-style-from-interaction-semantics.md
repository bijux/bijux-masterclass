---
module_id: API-060
program: API & Service Engineering
level: 2
module_number: 60
title: Choosing an Interface Style from Interaction Semantics
status: complete
last_verified: 2026-09-02
---

# Choosing an Interface Style from Interaction Semantics

## One-Page Review

### Governing question

Given an interaction's actors, direction, initiation, timing, durability, data shape, failure recovery, client environment, and operational ownership, which interface style makes the required semantics explicit at acceptable lifecycle cost—and where should a portfolio use different styles rather than force one protocol everywhere?

### Essential definitions

- **interaction semantics** are the observable obligations of an exchange: who initiates, who can speak, what messages mean, when effects commit, what acknowledgement proves, and how failure is recovered.
- An **interface style** is a coherent set of abstractions and wire conventions, such as resource-oriented HTTP, RPC, GraphQL, event/message APIs, webhook delivery, SSE, WebSocket, polling, or batch transfer.
- A **hard constraint** is a requirement whose violation disqualifies a candidate; a **preference** changes relative fitness but can be traded.
- **temporal coupling** requires participants to be available in overlapping time; **spatial coupling** requires knowledge of a participant's address or identity.
- **interaction topology** describes requester/responder, one-to-many publish/subscribe, producer-to-subscriber callback, one-way observation, or bidirectional session relationships.
- **delivery state ownership** identifies which participant or durable intermediary records attempts, offsets, acknowledgements, and recovery state.
- A **semantic adapter** translates between interface styles while preserving identities, deadlines, authorization, acknowledgement, ordering, and failure meaning.
- **portfolio governance** manages multiple justified styles through shared identity, policy, schema, observability, lifecycle, and support standards.

### Central model, mechanism, or theorem

Let requirement vector $R=(D,I,T,U,L,O,F,S,C)$ encode direction, initiator, topology/durability, user/client environment, latency, ordering, failure recovery, schema/query needs, and operational constraints. For candidate style $s$, first require every hard predicate:

$$
feasible(s,R)=\bigwedge_{h\in H} h(s,R).
$$

Only feasible styles are scored. With preference weights $w_i$, evidence-backed fit $f_i(s)\in[0,5]$, and lifecycle risks/costs $r_j(s)\in[0,5]$:

$$
score(s)=\sum_i w_i f_i(s)-\sum_j v_j r_j(s).
$$

The numbers organize evidence; they do not manufacture truth. Sensitivity analysis, concrete failure traces, prototype evidence, and explicit assumptions decide close or high-risk cases.

### Critical invariants

Decide semantics before syntax. A chosen style must express initiation, direction, acknowledgement, commit, partial result, cancellation, timeout, retry, idempotency, ordering scope, replay/resume, backpressure, authentication, authorization, versioning, discovery, observability, and retirement. Hard constraints are never compensated by a high weighted score. Compare the whole production path—including gateways, browsers, proxies, brokers, generated clients, stores, support, and incident response—not a framework demo.

Prefer the simplest style that satisfies the interaction and its future evidence-backed variability. Use HTTP resources when uniform methods, representations, intermediaries, conditional requests, links, and broad reach are central. Use RPC for operation-shaped, strongly typed service calls and explicit unary/streaming methods. Use GraphQL when authorized clients genuinely need variable hierarchical data selection across a governed graph. Use event/message APIs when decoupling, durable fan-out, replay, or independent consumers dominate. Use webhooks for producer-owned delivery to externally operated server endpoints; SSE for one-way HTTP event feeds; WebSocket for frequent bidirectional sessions. Use polling or batch when latency tolerates them and simplicity/offline operation matters.

### Common failures

Starting from the team's favorite framework; treating REST as URL spelling; treating RPC as local calls; choosing GraphQL to avoid domain modeling; choosing events to hide synchronous dependencies; calling a webhook a queue; using WebSocket merely because the product says “real time”; scoring an infeasible option; double-counting correlated benefits; hiding assumptions inside scores; benchmarking serialization while ignoring end-to-end work; comparing mature production HTTP against prototype alternatives; ignoring browsers, firewalls, SDK languages, accessibility, offline behavior, schema evolution, abuse controls, observability, and on-call capability; translating status or cancellation incorrectly in a gateway; creating dual-write sources of truth; proliferating styles without governance; and adopting one enterprise-wide style for interactions with incompatible semantics.

### Compact example

A logistics product needs public shipment lookup, internal route optimization, partner status notifications, and a live operator board. Public lookup uses resource-oriented HTTPS with conditional GET because reach, cache validation, and stable identifiers dominate. Internal optimization uses bounded unary gRPC because the call is typed and operation-shaped. Partner notifications use signed, retrying webhooks backed by an outbox because partners host endpoints and may be unavailable. The operator board uses SSE because updates are one-way; commands remain idempotent HTTP operations. **Conclusion:** one domain can expose a coherent portfolio when each boundary has distinct interaction semantics and all styles share identity, policy, event IDs, schemas, telemetry, and lifecycle governance.

### Connections

[Outside-In API Requirements](011-outside-in-api-requirements.md), [Remote Procedure Call Semantics](051-remote-procedure-call-semantics.md), [Unary and Streaming gRPC](053-unary-and-streaming-grpc.md), [GraphQL Authorization and Cost Control](058-graphql-authorization-and-cost-control.md), and [Webhooks, Server-Sent Events, and WebSockets](059-webhooks-server-sent-events-and-websockets.md) supply the evidence this synthesis uses. The next block develops commands, events, messages, event schemas, and asynchronous delivery in depth.

## Governing Question

What observable interaction must participants support, which constraints are non-negotiable, and which interface style—or deliberately governed combination—delivers those semantics with the least total complexity and clearest failure recovery?

## Why This Matters

Interface choices become organizational commitments. They shape client code, gateways, schemas, authentication, caching, brokers, deployment topology, test harnesses, documentation, telemetry, support skills, and deprecation work. A protocol that looks concise in one handler can impose years of hidden lifecycle cost on every consumer.

Teams often compare labels rather than semantics: “REST versus GraphQL,” “gRPC versus events,” or “WebSocket versus polling.” These pairs are not always substitutes. A typed request/response command, a durable fact distributed to unknown future consumers, a client-composed read projection, and a live bidirectional editing session solve different interaction problems. Selecting one style by fashion can make the protocol fight its requirement.

The opposite mistake is uncontrolled variety. Every new style adds policy integration, schema tooling, client libraries, testing, observability, deployment, incident response, and security review. A healthy portfolio therefore uses the fewest styles that materially simplify distinct classes of interaction. It standardizes cross-cutting semantics while allowing justified boundary-specific protocols.

A defensible choice is traceable. Reviewers can see requirements, hard constraints, candidate evidence, failure traces, assumptions, sensitivities, prototype results, ownership, and reconsideration triggers. The artifact is not a beauty contest; it is a compact engineering argument.

## Prerequisites and Retrieval

Retrieve [Outside-In API Requirements](011-outside-in-api-requirements.md), [Long-Running Operations](018-long-running-operations.md), [Bulk and Batch Operations](019-bulk-and-batch-operations.md), [Designing an API from Consumer Tasks Rather Than Database Tables](020-designing-an-api-from-consumer-tasks-rather-than-database-tables.md), [Remote Procedure Call Semantics](051-remote-procedure-call-semantics.md), [Unary and Streaming gRPC](053-unary-and-streaming-grpc.md), [GraphQL Schema Design](055-graphql-schema-design.md), [GraphQL Execution, Resolvers, and Batching](056-graphql-execution-resolvers-and-batching.md), [GraphQL Pagination and Incremental Delivery](057-graphql-pagination-and-incremental-delivery.md), [GraphQL Authorization and Cost Control](058-graphql-authorization-and-cost-control.md), and [Webhooks, Server-Sent Events, and WebSockets](059-webhooks-server-sent-events-and-websockets.md).

Be able to distinguish request, command, fact/event, representation, response, acknowledgement, durable acceptance, business completion, transport order, domain order, retry, replay, resume, backpressure, cache freshness, and cancellation. Retrieve current specifications for any candidate that enters the decision; do not decide from remembered brand descriptions.

## Learning Objectives

After completing this module, you can:

1. derive an interaction profile from actor outcomes and failure obligations;
2. separate hard feasibility constraints from weighted preferences;
3. compare HTTP resources, RPC/gRPC, GraphQL, event/message APIs, webhooks, SSE, WebSocket, polling, and batch without collapsing their semantics;
4. identify delivery-state, schema, authorization, ordering, and recovery ownership for each candidate;
5. construct a transparent weighted decision and perform sensitivity analysis;
6. design prototypes that test decisive uncertainty rather than polished happy paths;
7. choose and govern hybrid portfolios without dual semantic ownership;
8. preserve semantics through gateways and adapters;
9. record an architecture decision with evidence and reversal triggers; and
10. verify the chosen style through contract, fault, load, security, and operability tests.

## Core Exposition

### Start with an interaction, not a protocol

Name one bounded interaction. Identify actors and trust zones, initiator, receiver, direction of application messages, cardinality, message frequency/size, and whether participants are simultaneously online. State the desired outcome and the observable boundary at which the caller may proceed.

Classify the principal message. A query asks for information without intending domain change. A command requests an effect and can be accepted, rejected, completed, or left uncertain. An event states a fact that already occurred. A representation describes current or selected resource state. A stream is a sequence with start, progress, terminal, gap, and cancellation semantics. Blurring these categories creates misleading acknowledgements and retry behavior.

Write the failure story before the success story. What if the request or response is lost? What if a consumer is offline for hours? What if one of ten downstream operations fails? Can a caller safely retry? Where is acceptance recorded? How is uncertain completion queried? What ordering scope is required? How does a slow participant bound upstream work? How are credentials revoked during a long session? These answers eliminate unsuitable candidates faster than syntax comparisons.

### Build the interaction profile

Record at least the following dimensions:

1. **Actors and reach.** Public browser, mobile app, partner server, internal service, device, analyst, or bulk data system; network and trust boundaries; supported languages and intermediaries.
2. **Initiator and direction.** Client pull, producer push to registered endpoint, one-way server feed, client stream, server stream, or simultaneous bidirectional conversation.
3. **Topology and cardinality.** One-to-one, aggregation, fan-out, fan-in, broadcast, dynamic subscription, or unknown future consumers.
4. **Time and availability.** Synchronous response window, latency objective, frequency, burst, offline duration, and whether participants must overlap in availability.
5. **Meaning and completion.** Query, command, fact, current representation, incremental result, progress, or conversation; what accepted/completed/failed means.
6. **Delivery and recovery.** Loss/duplicate tolerance, retry owner, idempotency key, durable log/inbox, replay horizon, resume token, reconciliation, dead-letter, and uncertain-result query.
7. **Ordering and concurrency.** Per-resource, per-partition, per-stream, causal, or no order; expected conflict resolution and optimistic concurrency.
8. **Data shape and access.** Stable resource views, operation-specific messages, variable client projections, graph traversal, large objects, bulk files, or continuous telemetry.
9. **Evolution and discovery.** Provider/consumer release independence, schema registry or IDL, runtime discovery, compatibility rules, version negotiation, and deprecation horizon.
10. **Security and governance.** Principal propagation, object/field/message authorization, data minimization, tenant isolation, egress/SSRF boundaries, abuse cost, audit, and retention.
11. **Operations.** Gateway/broker/load balancer support, observability, load shedding, draining, regional topology, disaster recovery, incident tools, on-call competence, and cost.

Make unknowns explicit. “Low latency” is not a requirement until a percentile, path, load, and user consequence are stated. “Exactly once” is normally an unresolved business-effect requirement until identity, atomicity, deduplication retention, and reconciliation are defined.

### Eliminate candidates with hard constraints

Hard constraints are binary only when backed by evidence. A browser that cannot use the required native gRPC stack without a bridge is a client-environment constraint. A consumer that must process after a twelve-hour outage needs durable retained delivery somewhere; a live socket alone is infeasible. A third-party partner behind ordinary HTTPS ingress cannot be required to join an internal broker. A one-way kiosk feed may not justify a bidirectional transport. A response that must use shared HTTP cache semantics rules out candidates that do not expose compatible HTTP request/cache semantics unless an adapter owns them.

Avoid fake constraints. “The team already knows it” is a cost/preference, not semantic feasibility. “Leadership chose GraphQL” is governance context, not proof that every workload is a graph query. Conversely, a regulatory requirement for auditable durable acceptance may genuinely disqualify an ephemeral-only path.

Document why each candidate passes or fails each hard predicate. If an adapter makes it feasible, include the adapter's availability, semantics, operations, and ownership in the candidate; do not credit a protocol with capabilities supplied invisibly by another system.

### Compare resource-oriented HTTP

Resource-oriented HTTP is strong when interactions revolve around enduring identities and representations, broad client reach, uniform methods/status semantics, content negotiation, conditional requests, caches, links, and ordinary infrastructure. RFC 9110 defines resources, representations, safe/idempotent method properties, validators, preconditions, caching-related semantics, authentication context, and status codes independently of HTTP version.

It fits public/partner APIs, CRUD-plus-lifecycle resources, conditional updates, simple synchronous commands represented as action/job resources, and reads that benefit from validators or shared/private caches. OpenAPI can describe HTTP operations, parameters, bodies, responses, security, and callbacks for tooling, but a description document does not supply domain semantics or runtime enforcement.

Costs appear when operation-shaped workflows are contorted into arbitrary nouns, when many client views cause endpoint proliferation or over/under-fetching, or when a long-lived interactive conversation is forced into repeated stateless calls. HTTP can carry streaming representations and asynchronous job patterns; “HTTP” does not mean CRUD or blocking completion. Decide from the chosen method/status/body/cache/retry contract, not the transport label.

### Compare RPC and gRPC

RPC is strong when the domain exposes named operations, callers and services coordinate typed contracts, generated clients matter, and request/response or bounded streaming shapes are known. gRPC defines unary, server-streaming, client-streaming, and bidirectional-streaming methods; per-direction order is preserved within an individual call. It also exposes deadlines, cancellation, metadata, status, and trailers.

It fits internal service commands/queries, control planes, strongly typed polyglot systems, and streams whose lifetime/flow control can be governed. The IDL creates a deliberate schema surface and generated stubs reduce mechanical disagreement.

Costs include browser/intermediary compatibility, gateway translation, generated-code distribution, load balancing/draining of long calls, schema discipline, and the misleading local-call abstraction. A successful server effect can still be uncertain to the client when a response or deadline races; cancellation does not roll back completed work. Streaming RPC is not a durable event log. Application identities, acks, checkpoints, replay, and idempotency remain necessary where required.

### Compare GraphQL

GraphQL is strong when authorized clients need variable hierarchical projections over a coherent domain graph, product views evolve independently, a type system and introspection/tooling aid composition, and the organization can govern resolver execution. The September 2025 specification defines typed schemas, queries, mutations, subscriptions, validation, execution, response data, and errors; it does not choose storage, authorization policy, cost controls, or federation architecture.

It fits product-facing read composition with genuine selection variability and graph relationships. It can reduce endpoint proliferation and let clients request fields congruent with view hierarchies. Mutations can expose typed domain actions, though they still need idempotency, concurrency, and completion semantics.

Costs include field- and relationship-complete authorization, N+1/batching/caching discipline, pagination, partial data/error handling, query demand estimation, runtime resource containment, trusted-operation lifecycle where used, observability by operation/field, and schema ownership. It is a poor excuse to expose an ungoverned database, avoid domain boundaries, or let arbitrary clients construct expensive cross-service plans.

### Compare durable event and message APIs

Event/message APIs are strong when producers and consumers should be temporally decoupled, events must survive outages, fan-out/replay/consumer groups matter, or unknown future consumers need facts. A broker or durable log may own retention, offsets, redelivery, partition order, and backpressure. AsyncAPI 3.0.0 provides a description model for message-driven APIs, channels, operations, messages, servers, and bindings; CloudEvents 1.0.2 provides a portable event metadata envelope. Neither description/envelope chooses business delivery guarantees, authorization, compatibility, or operational policy automatically.

They fit domain event distribution, ingestion pipelines, audit/rebuild feeds, asynchronous workflows, and high-volume decoupled processing. Commands can use messaging when durable queued acceptance and asynchronous outcome are explicit, but commands require one logical owner and should not be broadcast as facts.

Costs include broker/platform ownership, schema registry and compatibility, duplicates, poison messages, partition/order design, consumer lag, replay side effects, retention/privacy, dead-letter/redrive, tracing across time, and eventual-consistency UX. Events do not remove coupling; they move it into schema, meaning, time, ordering, and operational dependencies. A synchronous caller that needs an immediate authoritative answer may still require a request/response boundary.

### Compare webhooks, SSE, WebSocket, polling, and batch

Webhooks fit producer-to-external-server notification where the producer owns durable attempts and the receiver owns an HTTPS endpoint. They require stable event IDs, signatures or mutual authentication, replay/idempotency, endpoint-control proof, SSRF-safe egress, retry classification, disablement, and redrive. They are not a durable consumer-owned queue.

SSE fits a client-opened, one-way server-to-browser HTTP event feed. WHATWG defines `text/event-stream`, event/data/id/retry fields, Last-Event-ID, and reconnection behavior. Application retention, authorization, gap/reset, queue bounds, proxy flushing, and effect idempotency remain required. It is often simpler than a bidirectional socket for progress, notification, and read-model updates.

WebSocket fits frequent low-latency bidirectional sessions. RFC 6455 defines opening handshake and framed transfer, not a domain message protocol, durable history, application acknowledgement, or reconnection recovery. Versioned envelopes, authorization per action/resource, bounds, backpressure, resume/snapshot, reauthentication, drain, and reconnect jitter are application/operations obligations.

Polling is strong when updates are infrequent, latency is tolerant, offline/restricted clients matter, or infrastructure simplicity dominates. Conditional GET, cursors, and jitter can reduce waste. Long polling can reduce empty requests but retains reconnect/server resource concerns. Batch/file/object transfer fits very large data, scheduled exchange, offline processing, reconciliation, or analytical snapshots when transactional latency is unnecessary. It needs manifests, checksums, schema/version, atomic publication, access control, retention, and restartability.

### Score preferences without laundering assumptions

After feasibility filtering, choose decision criteria tied to outcomes: semantic clarity, client reach, latency, throughput, cacheability, projection flexibility, temporal decoupling, durable replay, evolution, security enforceability, observability, operational maturity, developer/tooling support, and total lifecycle cost. Define anchors for each score before scoring candidates. “5 for operability” might mean existing production platform, staffed ownership, tested failure tooling, capacity evidence, and supported telemetry; “1” might mean prototype only.

Use weights agreed by accountable stakeholders, not tuned after seeing the winner. Record source/evidence for every non-obvious score. Keep correlated criteria from dominating: latency, efficiency, and performance may represent the same evidence. Separate provider convenience from total consumer and operator cost.

Run sensitivity analysis. Change uncertain scores and weights through plausible ranges. If the winner changes easily, the decision is not robust; obtain better evidence, simplify criteria, or preserve reversibility. If two styles are close, prefer simpler lifecycle ownership unless a prototype reveals a decisive difference.

### Prototype the uncertainty and failure path

A useful spike tests a disputed constraint through the real path. For public HTTP, exercise target clients, gateway, authorization, cache validators, error contract, and rate limits. For gRPC, exercise supported languages, proxy/service mesh, deadlines, cancellation, message limits, balancing, and drain. For GraphQL, use representative operations to test authorization completeness, normalized cost, resolver calls, pagination, partial errors, and schema tooling. For events, test broker outage, duplicate, reorder, lag, replay, poison handling, schema evolution, and redrive. For SSE/WebSocket, include target proxies/browsers, slow consumers, reconnect herds, credential expiry, process death, and deployment drain.

Measure end-to-end user or service outcomes, not serialization alone. Record payload sizes, dependency calls, CPU/memory, queue growth, p50/p95/p99 latency, error/recovery behavior, operator steps, and observability gaps under a named workload. A benchmark without workload, environment, versions, warm-up, and failure conditions is not portable evidence.

### Design a coherent hybrid portfolio

One product may justifiably use several styles, but each interaction needs one semantic owner. A resource HTTP API may accept an idempotent command and return a job resource; an outbox publishes resulting facts to a broker; a projection service supplies GraphQL reads; an SSE edge sends authorized UI updates; partner notifications use webhooks. This is coherent if command identity, commit boundary, event identity, source of truth, authorization, and recovery remain singular.

Avoid dual writes from a handler to database and broker; use a transactional outbox or equivalent atomic boundary. Avoid two public interfaces that both claim independent ownership of the same mutation without shared idempotency/concurrency semantics. Avoid gateways that convert an asynchronous acceptance into a false synchronous success.

Standardize cross-style identity, tenant context, trace/causation, deadlines, error taxonomy, idempotency, schema compatibility, deprecation, data classification, telemetry, SLOs, incident ownership, and support policy. Permit exceptions through a decision record with owner and exit/review criteria.

### Preserve semantics through adapters

Adapters are production components, not neutral plumbing. An HTTP-to-gRPC gateway maps methods, status, headers/metadata, deadlines, cancellation, streaming, errors, and identity. A broker-to-webhook dispatcher maps durable offsets into attempts and HTTP acknowledgements. An event-to-SSE projection maps retained domain events into authorized client sequences and gap/reset behavior. A GraphQL resolver may call RPCs but must preserve cancellation, authorization context, batching, and error redaction.

Specify information that cannot be preserved. HTTP cache validation may not survive an RPC facade automatically. gRPC streaming trailers and partial records may not map cleanly to a buffered JSON response. GraphQL partial data/errors do not equal one HTTP operation failure. Broker acknowledgement may mean durable receipt while webhook 2xx may mean receiver durable acceptance. WebSocket close does not reveal command outcome.

Test adapters with loss, timeout, cancellation, duplicate, partial response, auth change, oversize data, overload, and version skew. Trace both external and internal identities without logging credentials or sensitive payloads. Assign capacity, deployment, and incident ownership; an adapter introduces another failure boundary.

### Record and revisit the decision

The architecture decision record includes context, interaction profile, hard constraints, candidates, feasibility table, weighted matrix with anchors/evidence, sensitivity, prototype results, chosen style, semantic contract, required platform capabilities, security/privacy analysis, migration plan, consequences, owner, and review triggers.

Use semantic triggers rather than calendar-only review: new public/browser client, offline duration beyond retention, fan-out growth, p99/queue/SLO breach, schema ownership conflict, authorization gap, unsupported language, gateway limitation, broker maturity, incident pattern, regulatory retention change, or deprecation of a dependency. State what evidence would reverse the decision.

Migration preserves identities and boundaries. Shadow reads may compare representations; dual publish requires one source of event identity and monitored parity; command migration requires shared idempotency and one authoritative commit. Define rollback before traffic movement and remove the old path after measured adoption and deprecation—not indefinite parallel semantics.

## Definitions and Notation

Let interaction profile $R=(A,I,D,T,L,F,O,Q,E,G)$ contain actors/trust zones $A$, initiator $I$, direction/topology $D$, time/availability $T$, latency/load $L$, failure/recovery $F$, ordering $O$, query/data shape $Q$, evolution $E$, and governance/operations $G$.

Let $S$ be candidate styles, $H$ hard predicates, $P$ preference criteria, $f_i(s)\in[0,5]$ evidence-backed fit, $w_i\ge0$ preference weight, $r_j(s)\in[0,5]$ lifecycle risk/cost, and $v_j\ge0$ risk weight. Candidate $s$ is admissible only if $feasible(s,R)$ is true. Score ranks admissible candidates but does not prove fitness.

Let $\Delta$ be the smallest plausible evidence/weight change that reverses the top ranking. Small $\Delta$ indicates fragility and need for better evidence or reversibility. A semantic adapter $g:s_1\rightarrow s_2$ is correct only if every required invariant is preserved or the loss is explicit and accepted.

## Mechanisms, Invariants, or Proof Structure

1. **Bound the interaction.** Name actors, outcome, message meaning, trust boundary, source of truth, and lifecycle.
2. **Write failure traces.** Lost request/response, offline consumer, duplicate, reorder, slow receiver, process death, version skew, authorization change, and overload reveal semantic needs.
3. **Classify obligations.** Mark each requirement as hard, preference, assumption, unknown, or derived consequence; give an owner and evidence.
4. **Generate real alternatives.** Include the simplest feasible baseline—often polling or ordinary HTTP—and adapters/platform components required by each candidate.
5. **Filter feasibility.** Reject any style that cannot satisfy a hard predicate across the actual end-to-end path.
6. **Score transparently.** Define anchors, weights, evidence, and costs; do not double-count or tune after the result.
7. **Analyze sensitivity.** Vary uncertain values and expose which assumptions control the outcome.
8. **Prototype decisive uncertainty.** Test production-like clients, intermediaries, failure, security, backpressure, drain, and observability.
9. **Specify semantics.** Document acknowledgement, commit, partial result, deadline/cancellation, retry/idempotency, order, replay/resume, bounds, authorization, evolution, and retirement.
10. **Govern and revisit.** Record ownership, verification, rollout/rollback, triggers, and evidence that would reverse the choice.

Invariant: every effect has one authoritative commit and stable identity across retries/adapters. Invariant: every asynchronous sequence names durable-state owner, ordering scope, replay horizon, and gap behavior. Invariant: every long-lived interaction has bounds, cancellation/expiry, reauthorization, drain, and recovery. Invariant: every client-visible projection applies current authorization independently of transport. Invariant: no adapter strengthens an acknowledgement or delivery claim without implementing the missing persistence/atomicity evidence.

## Alternatives and Trade-Offs

**One enterprise standard versus a governed portfolio.** One standard reduces tooling/support variance but can force mismatched semantics. A portfolio improves fit but multiplies platform surfaces. Prefer a small approved set with entry criteria, shared cross-cutting controls, and exception review.

**Synchronous request/response versus asynchronous acceptance.** Synchronous calls give immediate correlation and simpler reasoning when work is bounded and participants are available. Asynchronous work absorbs outages/bursts and decouples time, but introduces status resources/events, duplicate handling, lag, reconciliation, and eventual outcomes.

**Provider-shaped versus consumer-shaped reads.** HTTP endpoints and RPC methods give providers explicit bounded contracts and caching/cost control. GraphQL offers client projection flexibility and product velocity but transfers demand/authorization/governance complexity to the graph platform.

**Ephemeral stream versus durable log.** SSE, WebSocket, and streaming RPC provide live delivery with transport flow control; a broker/log provides retention, offsets, replay, and decoupled consumption. They can compose, but the live edge must expose gaps and snapshot recovery instead of pretending to retain history.

**Generated IDL clients versus ubiquitous protocols.** gRPC/Protobuf and other IDLs provide strong schemas and generated code; HTTP/JSON has broad reach and inspectability. Generated clients add distribution/version/toolchain ownership, while handwritten loose clients risk contract drift.

**Direct integration versus adapter.** Direct support preserves protocol capabilities and removes a hop. An adapter can centralize policy and widen reach but introduces semantic translation, capacity, latency, security, observability, and failure ownership. Include it in the architecture and score.

**Build capability versus adopt platform.** A managed gateway, graph platform, broker, or event service can accelerate maturity, but portability, quotas, pricing, regional behavior, observability, incident authority, and exit cost become part of the choice. Evaluate the production service, not only the abstract protocol.

## Failure Modes and Misconceptions

1. **Style before semantics.** A favored technology dictates requirements after the fact.
2. **REST reduced to nouns.** Uniform method, status, representation, conditional, cache, and link semantics disappear behind URL aesthetics.
3. **RPC treated as local.** Deadlines, partial failure, retries, cancellation races, and uncertain effects are ignored.
4. **GraphQL as database exposure.** Resolver cost, field authorization, pagination, ownership, and demand control are postponed.
5. **Events as decoupling magic.** Consumers remain coupled to fact meaning, schema, ordering, retention, and time.
6. **Live connection as durability.** WebSocket/SSE/gRPC stream is assumed to provide history, application acknowledgement, or reconnect recovery.
7. **Webhook as exactly-once queue.** Lost responses, duplicates, SSRF, signing, disablement, and redrive are omitted.
8. **Hard constraint in a weighted sum.** A disqualified candidate wins by accumulating irrelevant preferences.
9. **False precision.** Scores lack anchors/evidence, correlated benefits are counted twice, and weights are tuned to a desired result.
10. **Microbenchmark selection.** Serialization throughput substitutes for end-to-end authorization, dependency, network, queue, and operator evidence.
11. **Prototype asymmetry.** The incumbent is judged by production incidents while the new style is judged by a hello-world path.
12. **Invisible adapter.** Gateway/broker/edge behavior supplies missing capabilities but its semantic losses and ownership are not evaluated.
13. **Two sources of truth.** Parallel interfaces commit independently or generate different command/event identities.
14. **Lowest provider effort wins.** Consumer integration, security, support, incident, evolution, and retirement costs are externalized.
15. **No reversal trigger.** A once-reasonable decision survives changed clients, scale, risk, or platform capability indefinitely.

## Worked Examples

### Example 1

A public catalog needs globally reachable reads, stable resource IDs, language negotiation, cache validation, and occasional conditional updates. Resource-oriented HTTPS passes hard browser/intermediary constraints and exposes GET validators plus If-Match updates. GraphQL projection flexibility is not evidenced; gRPC needs a public bridge. Choose HTTP resources and OpenAPI description, with polling for low-frequency changes.

### Example 2

Two internal services perform a typed `ReserveCapacity` command with bounded request/response, strict deadline propagation, supported generated clients, and no offline requirement. Unary gRPC fits the operation shape and platform maturity. The contract still adds idempotency key, authoritative outcome lookup, cancellation checks, message limits, and status mapping because RPC cannot remove uncertain completion.

### Example 3

A mobile product renders many evolving hierarchical views over customer-authorized commerce data. Measurements show endpoint proliferation and substantial over-fetching; the organization has schema ownership, field authorization, batching, pagination, cost analysis, and trusted-operation support. Governed GraphQL becomes feasible and scores highest for projection variability. Payments remain explicit idempotent mutations with domain policy, not arbitrary resolver writes.

### Example 4

An order service must distribute `OrderConfirmed` facts to billing, fulfillment, analytics, and future consumers; consumers may be offline for hours and need replay. A durable broker/event API passes hard fan-out and retention constraints. A synchronous call chain fails temporal-coupling and independent-recovery requirements. Transactional outbox, stable event ID, partition by order, schema compatibility, consumer inbox, lag/poison/redrive operations, and privacy retention complete the choice.

### Example 5

A SaaS producer notifies partner-controlled servers of invoice changes. Partners accept HTTPS but cannot join the internal broker. Signed webhook delivery backed by the producer outbox fits boundary topology. Endpoint-control challenge, SSRF-safe egress, stable event ID, exact-body signature with timestamp/key ID, classified retries, partner bulkheads, receiver inbox, disablement, and redrive are part of the interface—not optional platform details.

### Example 6

A browser build dashboard receives one-way progress and completion events; commands already use HTTP. SSE satisfies direction and native browser reach with less protocol surface than WebSocket. The service defines event IDs, bounded retention, Last-Event-ID validation, reset-to-snapshot, heartbeats, proxy no-buffer tests, per-tenant authorization, queue bounds, disconnect cleanup, and reconnect jitter. Conditional polling remains fallback.

### Example 7

A multiplayer editor needs frequent low-latency bidirectional operations and presence. WebSocket passes direction/frequency constraints where polling and SSE-plus-POST would complicate the session. The application protocol adds versioned operation IDs, base document version, per-document sequence, explicit accept/result messages, bounded queues/rates/frames, snapshot/resume, reauthorization, credential expiry, slow-client disconnect, drain, and recovery query.

### Example 8

A monthly regulator export is hundreds of gigabytes, must be reproducible, checksum-verifiable, encrypted, resumable, and retained. Batch object transfer with manifest and immutable snapshot beats GraphQL, RPC streaming, or events. The control plane uses HTTPS to request/status the export; the data plane uses authorized object download. Separate styles preserve job and bulk-data semantics.

### Example 9

An API gateway exposes public HTTP while internal services use gRPC. The candidate is not “free HTTP plus gRPC”: the gateway must preserve request identity, deadlines, cancellation, authentication context, size limits, status/error details, streaming behavior, traces, and drain. A test shows one gRPC error was mapped to HTTP 200 with an error body, violating client retry semantics. The decision remains conditional until mapping and contract tests are fixed.

### Example 10

A team scores HTTP, GraphQL, and gRPC for a partner query interface. gRPC wins narrowly only when “performance” weight is high, but target partner clients require ubiquitous HTTPS and the bridge lacks streaming/error parity; reach is a hard constraint, so gRPC is infeasible despite its score. Between HTTP and GraphQL, sensitivity changes the result when projection variability moves one point. The team prototypes five real workflows and finds stable representations, choosing simpler HTTP with a review trigger if measured endpoint/view divergence grows.

## Cross-Program Connections

[Software Engineering Patterns](../../11-software-engineering-patterns/ROADMAP.md) supplies boundaries, adapters, commands, events, and ownership patterns. [Distributed Systems](../../27-distributed-systems-engineering/ROADMAP.md) supplies partial failure, clocks, ordering, replication, consensus, and delivery reasoning. [Network Engineering](../../24-network-engineering/ROADMAP.md) supplies transport, proxy, connection, capacity, and loss constraints. [Security Engineering](../../25-security-engineering/ROADMAP.md) supplies trust modeling, identity, authorization, abuse resistance, and cryptographic lifecycle.

[Systems Engineering](../../26-systems-engineering/ROADMAP.md) contributes stakeholder needs, trade studies, interfaces, verification, and lifecycle decisions. [Platform Engineering](../../29-platform-engineering/ROADMAP.md) owns paved roads for gateways, brokers, graph/RPC infrastructure, policy, telemetry, and developer workflows. [Cloud and Infrastructure Engineering](../../30-cloud-and-infrastructure-engineering/ROADMAP.md) contributes regional availability, managed-service limits, cost, shared responsibility, and disaster recovery.

The interface decision is therefore a system boundary decision. It cannot be made solely by API authors or from a payload schema; it consumes evidence and assigns obligations across consumers, producers, platform, security, operations, and governance.

## References

1. IETF. “RFC 9110: HTTP Semantics.” June 2022. <https://www.rfc-editor.org/rfc/rfc9110.html>
2. OpenAPI Initiative. “OpenAPI Specification, latest published version.” Retrieved 2026-09-02. <https://spec.openapis.org/oas/latest.html>
3. gRPC Authors. “Core concepts, architecture and lifecycle.” Retrieved 2026-09-02. <https://grpc.io/docs/what-is-grpc/core-concepts/>
4. GraphQL Specification Project. “GraphQL Specification, September 2025 Edition.” <https://spec.graphql.org/September2025/>
5. AsyncAPI Initiative. “AsyncAPI Specification 3.0.0.” <https://www.asyncapi.com/docs/reference/specification/v3.0.0>
6. Cloud Native Computing Foundation. “CloudEvents Specification 1.0.2.” <https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md>
7. WHATWG. “HTML Living Standard: Server-Sent Events.” Retrieved 2026-09-02. <https://html.spec.whatwg.org/multipage/server-sent-events.html>
8. IETF. “RFC 6455: The WebSocket Protocol.” December 2011. <https://www.rfc-editor.org/rfc/rfc6455.html>

## Exercises

### Exercise 1

Classify these statements as hard constraint, preference, assumption/unknown, or derived consequence for a proposed customer interface: target customers can make outbound HTTPS calls; p99 must be “fast”; customers may be offline for eight hours and must receive every accepted invoice event; the team knows gRPC; a managed broker is available internally; payloads are expected to remain below 64 KiB. Explain what evidence or clarification each needs.

### Exercise 2

Compare resource-oriented HTTP, unary gRPC, GraphQL, and durable messaging for an internal inventory interaction that supports current-stock queries, reserve commands, and distribution of stock-adjusted facts. State whether one style should own all three or a portfolio should be used. Define acknowledgement and uncertain-result recovery.

### Exercise 3

Three feasible candidates have fit/risk values using

$$
score=4C+3E+2O-3R,
$$

where $C$ is client reach, $E$ evolution fit, $O$ operability, and $R$ lifecycle risk. HTTP has $(5,3,5,1)$, GraphQL $(4,5,3,3)$, and gRPC $(2,4,4,2)$. Compute scores. Then explain why the matrix cannot override a hard browser constraint and perform one sensitivity observation.

### Exercise 4

Design an evidence spike comparing SSE and WebSocket for a browser incident console that mostly receives updates but occasionally sends acknowledgements and control commands. Include decisive requirements, production path, failure/adversarial cases, measurements, and a decision rule.

### Exercise 5

An emergency-management platform needs public resource reads, operator commands, live dashboards, inter-agency facts, partner callbacks, and nightly geospatial exports. Propose a governed interface portfolio. For each boundary define semantic owner, identity/authorization, acknowledgement/commit, retry or replay, ordering, backpressure, evolution, observability, and recovery. Describe adapters, verification, and reconsideration triggers.

## Answers to the Exercises

### Answer 1

Outbound HTTPS capability is a hard reach constraint only after confirming TLS versions, authentication, proxy/firewall, payload, response-time, inbound-webhook prohibition, and client libraries. “Fast” is an unknown: define interaction, geography/path, load, percentile, budget, and consequence before it can become hard or weighted. Eight-hour offline receipt is a hard durability/retention constraint once “every accepted event,” maximum outage, ordering, replay, and recovery objectives are precise; an ephemeral live connection alone is infeasible.

Team gRPC knowledge is a preference/cost advantage, not semantic feasibility. Internal managed broker availability is an enabling assumption and operability preference until service limits, retention, regions, ownership, tenancy, recovery, client boundary, and SLO evidence are checked; it does not make the broker reachable to customers. The 64 KiB expectation is an assumption requiring production distributions, growth, compression/decompression, metadata, batch/fan-out, adversarial limit, and oversize behavior. If enforced, it yields derived schema/message limits and a large-object indirection path.

### Answer 2

Use a portfolio with one inventory domain owner. Current-stock query is a cache-aware authorized HTTP resource when broad reach/conditional reads matter, or unary gRPC if all clients share the internal typed platform; choose from measured client/platform evidence. `ReserveStock` is an explicit idempotent command, preferably unary gRPC in this stated internal environment, with reservation ID/idempotency key, expected stock version, deadline, typed outcome, and `GetReservation` recovery.

On successful command handling, one authoritative transaction commits reservation/stock version and transactional outbox record. RPC OK means documented completed commit; deadline/unavailable after dispatch is uncertain, never rollback proof, so the caller queries/retries with the same identity. `StockAdjusted` is a past-tense immutable fact published from the outbox to durable messaging. Broker acknowledgement to producer means durable platform acceptance under the selected configuration; consumer acknowledgement means that consumer's documented checkpoint/processing boundary, not all business consumers completed.

Partition facts by inventory item or facility-item according to required order, state this scope, and make consumers idempotent by event ID. Define retention/replay, schema compatibility, authorization by tenant/facility, lag/backpressure, poison/redrive, reconciliation of stock version versus consumer projection, and trace/causation from command through event. HTTP/gRPC adapters must share identity and policy and must not create a second mutation source.

### Answer 3

HTTP: $4(5)+3(3)+2(5)-3(1)=20+9+10-3=36$. GraphQL: $4(4)+3(5)+2(3)-3(3)=16+15+6-9=28$. gRPC: $4(2)+3(4)+2(4)-3(2)=8+12+8-6=22$. HTTP ranks first among candidates declared feasible.

If native target-browser support without a bridge is hard and the gRPC candidate cannot provide it, gRPC must be removed before scoring; even a hypothetical higher total cannot repair infeasibility. If a supported bridge is added, its semantic mapping, latency, deployment, security, observability, and lifecycle risk belong in the candidate.

One sensitivity observation: GraphQL needs nine more points to overtake HTTP. Raising its evolution fit cannot do that because it is already 5. If HTTP client reach fell from 5 to 3, HTTP would lose 8 points and score 28, tying GraphQL; that assumption is decision-critical. Alternatively reducing GraphQL lifecycle risk from 3 to 1 adds 6, still leaving it at 34. The analysis suggests validating HTTP reach and GraphQL lifecycle maturity rather than debating minor operability scores.

### Answer 4

First quantify update frequency/size/burst, command frequency, required one-way/bidirectional latency, target browsers, proxies/CDNs, connection duration/count, offline/replay window, authorization changes, and operator consequences. Baseline candidate A is SSE for updates plus idempotent HTTP POST commands; candidate B is a versioned WebSocket subprotocol for both directions. Both need snapshot recovery, event/command identities, current authorization, queue/rate/size/lifetime bounds, and polling fallback if required.

Exercise real authentication, ingress, CDN/proxy, load balancer, service, event source, regional path, and supported browsers. Test SSE record fragmentation, multiline/blank dispatch, heartbeats, buffering/compression, Last-Event-ID forgery/expiry, slow readers, gap/reset, and POST response loss. Test WebSocket Origin/subprotocol, message type/state, application ack, oversize/compression bomb, floods, slow queues, ping/pong versus ack, credential expiry, resume forgery, process death, failover, and drain. For both, trigger tenant revocation and mass reconnect with jitter.

Measure end-to-end p50/p95/p99 update and command outcome latency, bytes/CPU/memory per connection, maximum stable connections, outbound queue age/bytes, drops/gaps, reconnect recovery time/load, proxy compatibility, operator visibility, and implementation/on-call burden. Choose SSE+HTTP if command frequency is low, it meets latency/capacity/recovery targets, and WebSocket has no material advantage. Choose WebSocket only if measured bidirectional frequency/coordination yields a decisive outcome benefit and its subprotocol/lifecycle platform meets all bounds. Record thresholds and reversal triggers.

### Answer 5

Public reads use resource-oriented HTTPS/OpenAPI with stable resource IDs, OAuth-bound tenant/agency authorization, cache-control/ETag and conditional GET, pagination, rate/size limits, problem details, schema compatibility, safe telemetry, and snapshot reconciliation. Operator commands use idempotent HTTPS or unary gRPC behind a controlled client boundary; command ID, actor/role/resource policy, expected version, deadline, authoritative transaction, explicit accepted/completed outcome, and status query resolve ambiguity.

The authoritative command transaction writes a transactional outbox. Inter-agency facts use a durable broker and CloudEvents-like governed envelope: stable event ID/type/version/source/subject/time/tenant/classification, partition/order by incident or resource where required, producer durable acceptance, consumer inbox/checkpoint, retention/replay, lag/bulkheads, poison/redrive, schema compatibility, privacy retention, traces, and reconciliation. No consumer treats broker receipt as global workflow completion.

Live dashboards use authorized SSE projections because direction is primarily server-to-browser: tenant/incident-bound sequence, retained window, Last-Event-ID validation, snapshot reset, heartbeat, proxy flush, per-client queue/connection/replay limits, revocation, reconnect jitter, and polling fallback. Commands stay on the idempotent command API. If future measured interaction becomes frequent and bidirectional, a WebSocket decision can be reopened with application ack/resume and lifecycle evidence.

Partner callbacks use signed HTTPS webhooks dispatched from durable event state: verified endpoint control, SSRF-safe egress, stable event identity, timestamp/key ID/rotation, replay/inbox, classified jittered retry, Retry-After policy, per-partner isolation, disablement, dead-letter/redrive, schema/minimization, and audit. Webhook 2xx means receiver durable acceptance only under the contract.

Nightly geospatial exports use an asynchronous job resource/control API plus immutable encrypted object/batch data with manifest, schema/coordinate reference version, counts, checksums, atomic publication, resumable authorized access, expiry/retention, and reproducibility. Job acceptance differs from export completion; clients poll/status or receive a fact/webhook and verify manifest before replace/merge.

Adapters include HTTP-to-command service, outbox-to-broker, broker-to-SSE authorized projection, broker-to-webhook dispatcher, and export worker/object gateway. Each preserves command/event/trace/tenant identity, deadlines where meaningful, acknowledgement strength, errors, limits, and audit; semantic losses are documented. Verify contracts and schemas plus loss-after-commit, duplicate/reorder, outage/replay, authorization revocation, cross-tenant IDs, slow consumers, overload, poison events, broker/region failure, proxy buffering, SSRF, signature rotation, export interruption/checksum, deployment drain, and disaster recovery.

Shared governance owns identity/policy, schema registry/compatibility, event taxonomy, idempotency, telemetry, SLOs, data classification, retention, incident tooling, deprecation, and exception review. Reconsider on client/topology change, replay-window breach, fan-out or connection growth, repeated semantic incidents, authorization gaps, SLO/queue/cost thresholds, platform maturity/change, regulatory retention, or demonstrated need for different interaction direction. Migration retains one authoritative command commit and stable identities throughout.
