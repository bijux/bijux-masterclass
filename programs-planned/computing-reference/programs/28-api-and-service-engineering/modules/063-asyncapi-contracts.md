---
module_id: API-063
program: API & Service Engineering
level: 2
module_number: 63
title: AsyncAPI Contracts
status: complete
last_verified: 2026-09-02
---

# AsyncAPI Contracts

## One-Page Review

### Governing question

How should an application-centered AsyncAPI document describe message-driven servers, channels, operations, messages, schemas, replies, security, and protocol bindings so the artifact is a verified production contract rather than documentation that drifts from broker policy and runtime behavior?

### Essential definitions

- An **AsyncAPI document** is a machine-readable description of one application's message-driven API under a declared AsyncAPI Specification version.
- An **application** sends messages, receives messages, or both; operation direction is stated from that documented application's perspective.
- A **server** is a broker, service, or other endpoint through which the application exchanges messages, identified by host/path/protocol/security and optional bindings.
- A **channel** is an addressable component through which messages are organized and exchanged; a channel key is a document identifier while its address is protocol-facing.
- An **operation** describes an application action, `send` or `receive`, against a referenced channel and its messages.
- A **message** describes headers, payload, content/schema format, correlation, bindings, traits, examples, and semantic documentation for a command, event, request, or response.
- A **binding** supplies protocol-specific information at server, channel, operation, or message scope; it does not redefine application meaning.
- A **component** is a reusable definition; referencing it does not mean the application uses it unless it is connected to an active document surface.
- **contract drift** is disagreement among AsyncAPI, schemas, broker/ACL configuration, generated artifacts, producer/consumer behavior, and deployment.

### Central model, mechanism, or theorem

Treat the contract as a typed graph

$$
A=(S,C,O,M,K,R),
$$

where servers $S$, channels $C$, operations $O$, messages $M$, schemas/components $K$, and references $R$ must resolve consistently. Structural validity is necessary but deployment conformance additionally requires

$$
declared(A)=observed(runtime)=authorized(policy)
$$

for the governed surface: application directions, addresses, protocols/bindings, message types/schemas, security, reply/correlation, and limits. Equality means semantic agreement under documented mappings, not byte-for-byte identity.

### Critical invariants

The document has one durable application identity, owner/contact, semantic version, exact AsyncAPI version, and intended environments. Every operation is named from the application's perspective and references one channel; every allowed message is explicit. Channel address/parameters match deployed routing and tenant rules. Messages distinguish event/command/request/reply meaning, stable identity, schema/content type, correlation/causation, examples, classification, bounds, and compatibility ownership. Servers declare protocol/version, safe variables, security alternatives/scopes, and exact binding versions where applicable.

References are pinned/resolvable/reproducible and do not import untrusted mutable content during production processing. Reuse through components/traits preserves clarity; overrides/merge semantics are tested. AsyncAPI validation, lint, schema compatibility, examples, generated artifacts, broker policy, ACLs, producers/consumers, and observability are verified together. The document never claims delivery, ordering, replay, idempotency, or business acknowledgement guarantees merely because the format can describe a channel.

### Common failures

One document describes an entire enterprise instead of one coherent application; send/receive direction reversed; sender document mechanically inverted into a receiver document; channel key confused with address; wildcard tenant address lacks parameter constraints; messages listed on a channel but absent from operation intent; generic “message” unions without discriminator; schemas inline-copy and drift; correlation points to a missing/untrusted value; reply address is attacker-controlled; secrets/default credentials in server variables; security declared only at connection while domain authorization is omitted; binding/version mismatch with broker; traits hide contradictory headers; references use mutable branches; generated code is treated as complete behavior; examples contain real personal data; docs render while parser/registry fails; and deployment changes topic/ACL/retention without contract checks.

### Compact example

An inventory application document identifies production/staging Kafka servers, a parameterized `inventory.{region}.events` address, a `sendInventoryReserved` operation, and allowed `InventoryReserved` message. The message references the governed CloudEvents envelope and Avro payload, documents event semantics/order key/classification, supplies synthetic valid examples, and declares Kafka binding details. CI resolves references, validates AsyncAPI/schema, checks registry compatibility, generates docs/tests, and compares provisioned topic/ACL policy. **Conclusion:** the document becomes trustworthy only when application meaning and deployed infrastructure are reconciled continuously.

### Connections

[Commands, Events, and Messages](061-commands-events-and-messages.md) defines interaction meaning; [Event Schema Design](062-event-schema-design.md) defines payload compatibility; [API Contracts and Behavioral Guarantees](021-api-contracts-and-behavioral-guarantees.md) defines contract evidence. The next modules specialize channel design, partition/order keys, delivery guarantees, and replay.

## Governing Question

What exact message-driven surface does this application implement, how is that surface bound to protocols, schemas, security, routing, replies, and environments, and what automated evidence proves the document agrees with deployed behavior and policy?

## Why This Matters

Message-driven systems are often documented in prose scattered across broker tickets, schema registries, source code, dashboards, and team memory. Producers and consumers disagree on addresses, directions, message kinds, headers, security, and versions. Infrastructure changes silently. The system works until a new consumer, replay, region, or incident exposes the mismatch.

AsyncAPI creates a machine-readable center for this contract. It can drive documentation, linting, schema checks, examples, generated interfaces, tests, catalog discovery, and provisioning reconciliation. Version 3.1.0 describes application servers, channels, send/receive operations, messages, replies, correlation IDs, schemas, security, components, and protocol bindings without assuming one topology or protocol.

The format cannot supply facts omitted from the design. A syntactically valid document may still reverse direction, name an ambiguous event, overstate delivery, expose secrets, or describe a topic no deployment provisions. Generated code can serialize bytes while mishandling idempotency, authorization, backpressure, or acknowledgements. A contract becomes operational evidence only when semantics and runtime are verified.

Application perspective is especially important. “Publish” and “subscribe” can be ambiguous across brokers and intermediaries. AsyncAPI 3.x uses `send` and `receive` relative to the documented application. A producer and consumer normally deserve their own documents because their operations, descriptions, servers, security, bindings, and infrastructure can differ; mechanically reversing actions is explicitly unsafe.

## Prerequisites and Retrieval

Retrieve [API Contracts and Behavioral Guarantees](021-api-contracts-and-behavioral-guarantees.md), [OpenAPI Structure](023-openapi-structure.md), [Contract-First and Code-First Workflows](028-contract-first-and-code-first-workflows.md), [Commands, Events, and Messages](061-commands-events-and-messages.md), and [Event Schema Design](062-event-schema-design.md). Know the application's deployed broker/protocol, server endpoints, channel/address policy, schema registry, authentication/authorization, delivery/order/replay contract, owner, and supported environments.

Retrieve the exact AsyncAPI Specification, binding specifications, parser/generator versions, schema dialects/formats, broker/provider documentation, and organization extensions used. Treat “latest” documentation as research; pin production artifacts and toolchains to reviewed versions.

## Learning Objectives

After completing this module, you can:

1. scope an AsyncAPI document around one application and its perspective;
2. model servers, channels, addresses/parameters, operations, and messages without direction ambiguity;
3. express request/reply, correlation, traits, components, references, examples, and multiple schema formats;
4. apply protocol bindings without leaking protocol details into domain meaning;
5. document authentication/security while preserving domain authorization obligations;
6. modularize contracts without reference or trait-merge drift;
7. align AsyncAPI, schema registry, broker configuration, ACLs, generated artifacts, and runtime behavior;
8. build lint, validation, compatibility, generation, contract, and deployment gates;
9. evolve and publish application contracts with consumer-safe versioning; and
10. diagnose drift through observability, inventories, and reconciliation.

## Core Exposition

### Scope one application and perspective

Begin with the application—not the broker, domain, or enterprise. Give it a durable URI/URN identity, title, API version, description, owner/contact, lifecycle, tags, and external domain/runbook links. State whether the document represents a deployable service, device, adapter, or logical application group and what is excluded.

Operations describe what this application implements. If it emits `OrderConfirmed`, its action is `send`; if it consumes that message, its action is `receive`. The channel may be connected through a broker or direct protocol, but direction remains from the application. Names such as `sendOrderConfirmed` and `receiveOrderConfirmedForBilling` are durable and unambiguous.

Do not derive a receiver document by flipping `send` to `receive`. The receiver may connect to a different server, receive from a forwarded/read-only channel, use another binding, have consumer-group configuration, accept only a subset, and describe different handling/security. AsyncAPI 3.1.0 warns that infrastructure and wording do not invert mechanically.

Choose document boundaries that produce clear ownership and release. A monolith with several tightly coupled modules may have one application document; independently deployed services should usually have separate documents even when sharing component packages. A catalog can compose discovery without pretending all operations share one lifecycle.

### Declare root metadata intentionally

The root `asyncapi` value selects specification syntax/semantics; `info.version` versions the described application API, not the AsyncAPI spec or deploy build. The application `id` should remain globally/durably unique. Document compatibility/deprecation policy and link to domain semantics, operational SLOs, retention, and support.

`defaultContentType` is useful only when truly common; message-specific content type wins where formats differ. Tags support catalog grouping but should not replace ownership/classification fields. External documentation links need durable accessible locations, versions, and checks; a local path or mutable chat link is not a contract.

Specification extensions use `x-` fields for organization needs. Define their schema, scope, ownership, versioning, tooling behavior, and whether they are annotations or enforced policy. Avoid dumping arbitrary metadata that different tools interpret inconsistently. Promote widely required concepts through governed extensions and tests.

### Model servers and environments

Servers identify connection/exposure details: host, optional pathname, protocol/protocol version, variables, security alternatives, tags, and bindings. Use separate named entries for production, staging, regions, or protocols only when the document's operations/messages genuinely apply. Do not publish internal production addresses in a public contract without threat review.

Variables constrain environment/region/namespace substitutions with enums/defaults/descriptions/examples. They are configuration templates, not secret stores. Never place passwords, tokens, private keys, or real credentials in examples/defaults. Generated/deployment tools receive secrets through protected mechanisms.

Declare protocol version supported by the actual platform/client matrix. Protocol name alone cannot describe TLS, broker features, retention, replication, limits, or service-provider semantics. Put protocol-specific fields in versioned server/channel/operation/message bindings and link operational policy where binding coverage ends.

Security schemes document connection/server alternatives and OAuth flows/scopes or other mechanisms supported by the specification. Clarify logical OR among alternatives and scope meaning. This does not replace channel/message/domain authorization: the runtime still binds trusted principal/tenant and authorizes send, receive, type, subject, and business action.

### Separate channel key from address

Within `channels`, each map key is a document identifier used by references. The channel object can carry an address expression, parameters, messages, servers, bindings, description, and tags. Choose a stable semantic key even if physical address changes by environment.

Address is protocol-facing. Parameterized addresses such as `orders.{region}.events` require each parameter's location/description and constrained values. Tenant/user-controlled parameters need strict allowlists, normalization, length/cardinality, ACL, and provisioning rules; never let documentation imply arbitrary broker paths are authorized.

Do not use a wildcard as an unbounded topology promise. State whether channel instances are pre-provisioned or dynamic, who creates/deletes them, maximum cardinality, retention, partitioning, tenant isolation, and discovery. Some details belong in bindings or external platform policy; link and test them.

The channel's `messages` map defines messages that may be carried, but operation references determine what this application sends/receives. Avoid channel unions so broad that consumers must accept unrelated commands/events with incompatible security or retention. A discriminator/type envelope and message selection remain explicit.

### Model operations as implemented actions

Every operation has a stable operation ID/key, `action` send/receive, channel reference, summary/description, messages where narrowing is needed, security/traits/tags/bindings, and optionally reply. Describe semantic responsibility: trigger, validation, acknowledgement boundary, side effects, idempotency, ordering, errors, retries, and recovery links.

The contract should say whether `receiveInventoryReserved` acknowledges after broker delivery, durable inbox, projection commit, or another boundary; AsyncAPI syntax cannot infer it. Document deadlines/expiry, delivery/replay assumptions, poison/redrive, and backpressure in descriptions/extensions linked to enforceable platform policy.

Keep operation names application-centric. A processor can receive one event and send another; these are two operations with causation relationship, not one magical transform. Use correlation/causation fields in message schemas and traces/observability rather than relying on naming.

### Describe messages completely

A message object can name/title/summary/description, headers, payload, correlation ID, content type, schema format, traits, examples, tags, external docs, and bindings. Define business kind—command/event/request/reply/document/notification—and exact semantics from prior modules. The format describes a carrier; it does not classify meaning automatically.

Headers contain application metadata that is stable across the operation contract. Protocol-defined transport headers belong in bindings/protocol. Separate stable message/event/command ID, type/version, source/subject, tenant/classification, correlation/causation, trace, and delivery attempt. Document which identity drives deduplication and which values are trusted.

Payload schema can use the AsyncAPI Schema Object or a Multi Format Schema Object/reference for JSON Schema, Avro, Protobuf, and other supported formats. Set `schemaFormat` and `contentType` exactly. Pin external schema identity/version/fingerprint; do not copy schemas inline across documents and let them diverge.

Document limits not always expressible in schema: total encoded/decompressed bytes, nesting, collections, compression, rate, and unknown type behavior. Examples are synthetic, valid, minimal plus representative/edge, and free of real credentials or personal data. CI validates examples against headers/payload and binding/profile.

### Express correlation and replies safely

Correlation ID objects use runtime expressions to identify a value in message headers or payload. Ensure every permitted message actually contains the location with correct type/format; validate examples. Correlation groups conversation and is not necessarily message identity or deduplication.

Operation reply describes response relationship and reply channel/address. Define reply message variants—accepted, rejected, progress, completed, failed—and terminality. A reply object does not make a broker interaction synchronous or guarantee a response. Deadline/TTL, outstanding-request bounds, late reply, lost reply, idempotency, and outcome lookup remain documented behavior.

Do not accept arbitrary reply addresses from untrusted payload without policy. Use provisioned/scoped reply channels or validated allowlisted address expressions. Bind tenant/principal, limit cardinality/lifetime/size, prevent amplification, and clean up. Correlation values cannot authorize access to replies.

### Reuse components and traits carefully

Components hold reusable schemas, messages, security schemes, parameters, operation/message traits, correlation IDs, bindings, and server/channel fragments supported by the spec. References reduce duplication only when ownership and compatibility boundaries align.

Prefer small semantic packages: a governed envelope/header trait, shared domain value schema, standard security scheme, or telemetry metadata. Do not create a giant global message trait whose defaults silently impose wrong retention, classification, or acknowledgement on every domain.

Trait merge behavior and overrides must be understood by the selected spec/tool version. Conflicting fields, arrays, security, tags, and bindings can render differently across tools. Resolve the complete document in CI and inspect/golden-test output. Reuse never exempts the final application surface from review.

External references are pinned to immutable releases/digests, retrieved through trusted registries/repositories, access-controlled, cached for reproducible builds, and cycle/path/size constrained. Avoid branch URLs and runtime network resolution of message-provided schemas. License/provenance and supply-chain scanning apply to shared artifacts/tools.

### Apply bindings at the right scope

Bindings attach protocol-specific information to servers, channels, operations, and messages. Use the official binding specification and declare/check its version where the binding supports it. Server binding describes connection/broker properties; channel binding describes address/topic/queue properties; operation binding describes publish/subscribe/send/receive behavior; message binding describes protocol representation such as keys/headers/content.

Do not put domain invariants into a Kafka/AMQP/MQTT binding, and do not put partition/retention protocol configuration into a generic payload schema. Separate concerns so another binding can carry the same event meaning without semantic drift.

Not every infrastructure feature is representable. Topic partitions/replication/retention, ACL resources, consumer groups, dead-letter policies, quotas, encryption, and managed-service settings may live in infrastructure-as-code/policy. Link them with stable identities and reconcile rather than invent unsupported AsyncAPI fields ad hoc.

Version mismatch is a failure: parser may accept core 3.1.0 while generator ignores a newer binding property. Maintain a tested matrix of AsyncAPI spec, bindings, parser, linter, generator, registry/schema, and broker/provider versions.

### Make security and privacy executable

Model connection authentication/security accurately for each server. Add organization extensions or linked policy for channel operation and domain authorization. CI compares declared scopes/principals with broker ACL/IAM resources; integration tests prove allowed and denied send/receive per tenant/type.

Message schemas carry classification and field-level minimization evidence. Examples, rendered docs, catalogs, generated fixtures, test logs, and mocks are disclosure surfaces. Use synthetic data and access controls. References must not expose internal hosts or secrets in public output.

Threat-model address parameters, reply routing, schema references, deserialization, compression, high-cardinality channels/tags, oversized examples, extension processing, code generation templates, and documentation rendering. Treat the contract/toolchain as software supply chain; pin dependencies and sandbox generation where appropriate.

### Build a contract delivery pipeline

On each change:

1. parse against the pinned AsyncAPI JSON Schema/parser;
2. lint organization rules for application scope, naming, ownership, descriptions, direction, addresses, security, bindings, classifications, and limits;
3. resolve references offline/reproducibly and detect cycles/unpinned sources;
4. validate message header/payload schemas and every example;
5. run schema-registry backward/forward/transitive checks plus semantic review;
6. generate docs/types/stubs/tests into governed outputs and detect unexpected diff;
7. run producer/consumer contract tests, negative auth tests, and serialization/runtime matrices;
8. reconcile broker/IaC servers/channels/bindings/ACLs/quotas and deployment metadata;
9. publish immutable contract/catalog artifact before incompatible runtime use; and
10. canary/observe rollout with rollback and deprecation evidence.

Treat generated artifacts as derivatives; edit the source contract/schema, not generated output. Generation does not implement business handlers, atomicity, authorization, idempotency, retry, or backpressure. Review generated dependencies/API ergonomics and pin templates/tool versions.

### Verify runtime conformance and drift

Contract tests produce/consume every message variant through target serializers and broker test environment, checking headers, content/schema IDs, routing/address parameters, correlation/reply, unknowns, limits, security denies, and acknowledgement/failure behavior. Fault tests cover broker outage, duplicate, reorder, poison, schema registry outage, expired credentials, ACL change, reply timeout, and redrive.

Deployment reconciliation compares declared servers/protocols/channel addresses/binding properties/security with infrastructure-as-code and provider APIs. Some differences are deliberate environment overlays; encode an approved mapping and fail unknown drift. Do not let docs CI provision destructive infrastructure without explicit separated authority.

Runtime telemetry observes application/operation/message IDs, schema/type versions, channels/partitions, safe tenant dimensions, successes/rejections, age/lag, ack/outcome latency, unknown schema/type, decode errors, size, retries, dead-letter/redrive, reply timeouts, and authorization denies. Avoid credentials/payloads and control cardinality.

Compare observed message types/schemas/directions to the contract. An undeclared producer, unused declared operation, wrong schema ID, or unexpected channel is drift. Route alerts to the documented owner and update either implementation/policy or contract through review—never silently bless production accidents.

### Evolve and publish contracts deliberately

Version `info.version` for the application API under a documented policy. Compatible message/schema additions may be minor; breaking operation/channel/security/message semantics require major/coexistence/migration. The AsyncAPI `asyncapi` field changes only when adopting a specification version.

Plan producer/consumer rollout from actual compatibility. Publish new schema/contract first, update tolerant consumers, then producers; or use another proven order. For breaking change, introduce new message type/channel/operation where needed, dual publish from one source identity, migrate consumers, monitor parity, deprecate, stop, and retain old contract/schema for replay/support horizon.

Catalog publication includes immutable artifact digest, application/owner, version, lifecycle, environments, schemas, bindings, compatibility/support, and deprecation dates. Consumer discovery should not depend on scraping a mutable main branch. Rollback preserves the previous contract and runtime compatibility.

## Definitions and Notation

Let document graph $A=(S,C,O,M,K,R)$ contain servers, channels, operations, messages, components/schemas, and references. Define $resolve(A)$ as the complete pinned graph and $surface(A)$ as reachable non-component operations/messages. Let runtime observations $B$, infrastructure/policy configuration $P$, and declared contract $D=surface(resolve(A))$.

Conformance relation $D\approx B\approx P$ requires semantic agreement for each governed property, allowing documented environment mappings. Let $U_D$ be declared operations and $U_B$ observed operations; undeclared runtime drift is $U_B\setminus U_D$, while unused/stale declaration is $U_D\setminus U_B$ subject to observation-window caveats.

Let generator/parser/binding/schema/broker version tuple $V=(v_a,v_p,v_b,v_s,v_k)$ identify the tested toolchain. A green contract under one $V$ does not prove another version tuple behaves identically.

## Mechanisms, Invariants, or Proof Structure

1. Bound one application, owner, lifecycle, perspective, and exclusions.
2. Pin AsyncAPI/tool/binding/schema versions and durable application/API identity.
3. Model actual servers/environments/security without secrets.
4. Define semantic channel keys, deployed addresses/parameters, messages, and binding scope.
5. Define application-centric send/receive operations and reply/correlation behavior.
6. Reference governed schemas and document message semantics, identity, classification, bounds, compatibility, and examples.
7. Reuse components/traits only with pinned provenance and resolved-output tests.
8. Validate/lint/resolve/schema-check/generate/test/reconcile before publication and rollout.
9. Compare declared, observed, and authorized surfaces continuously.
10. Evolve with compatibility-aware ordering, coexistence, rollback, deprecation, and retained artifacts.

Counterexample to structural sufficiency: a document validates with `receive` for `OrderConfirmed`, while runtime publishes it. All references and schemas are valid, yet perspective and ACL policy are wrong. Counterexample to code-generation sufficiency: generated consumer decodes the event but acknowledges before durable inbox; crash loses work despite matching types.

## Alternatives and Trade-Offs

**One application document versus domain catalog bundle.** One document gives clear ownership/release; bundles aid discovery. Compose catalogs from separately versioned application contracts rather than blur perspectives.

**Inline schemas versus external registry references.** Inline improves standalone readability but duplicates/drifts. External immutable schemas centralize compatibility but need reproducible resolution/cache. A bundled release artifact can offer both.

**Core-only versus detailed bindings.** Core-only is portable and simpler; bindings make deployment/protocol behavior precise but tie to binding/tool versions. Include details needed for contract and reconcile the rest with IaC.

**Manual docs versus generation.** Handwritten prose captures nuance but drifts; generated docs/types/tests stay structural but omit behavior not modeled. Use machine generation plus reviewed semantic/runbook content.

**Contract-first versus implementation extraction.** Contract-first enables consumer/infrastructure review before code. Extraction discovers actual structures quickly but may preserve accidental behavior. Either requires runtime drift reconciliation and one canonical owner.

**Shared components versus local clarity.** Shared envelope/security/value definitions reduce inconsistency; deep global references hide ownership and expand blast radius. Version small stable components and render resolved application views.

**Provision from contract versus reconcile contract with IaC.** Direct provisioning reduces duplication but may exceed format/provider coverage and raises destructive authority. Often use dedicated IaC as source for infrastructure, with bidirectional validation against AsyncAPI.

## Failure Modes and Misconceptions

1. One “enterprise AsyncAPI” mixes independent application perspectives and lifecycles.
2. Send/receive is interpreted from broker or peer rather than documented application.
3. A consumer contract is generated by mechanically flipping a producer contract.
4. Channel map key, physical address, and domain event type are conflated.
5. Parameterized/wildcard channels omit constraints, provisioning, ACL, and cardinality.
6. Message kind, acknowledgement, order, delivery, replay, and idempotency are assumed from syntax.
7. Correlation/reply paths are missing, unbounded, or attacker-controlled.
8. Server variables/examples leak credentials or internal details.
9. Security scheme is mistaken for message/domain authorization.
10. Binding property/version disagrees with broker/provider/tool support.
11. Global traits/components create hidden conflicts or incompatible blast radius.
12. Mutable/untrusted references destroy reproducibility and supply-chain safety.
13. Generated code/documentation is treated as runtime conformance proof.
14. Real payloads/personal data leak into examples, catalogs, fixtures, and logs.
15. Contract, registry, broker/IaC, ACL, and runtime evolve independently without drift detection.

## Worked Examples

### Example 1

An order service sends `OrderConfirmed`; its operation action is `send`. Billing's separate document receives the same semantic message through a forwarded regional channel and uses `receive`. Flipping the producer document would miss billing's server, consumer binding, ACL, and inbox acknowledgement.

### Example 2

Channel key `regionalOrderEvents` has address `orders.{region}.events`. `region` is enum-constrained to deployed values; IaC provisions each instance with quotas/ACLs. Tenant is not an arbitrary address parameter, preventing unbounded topology and cross-tenant routing.

### Example 3

A channel permits three event messages, but an analytics application receives only two. Its operation explicitly selects those messages; tests reject the third and ACL/router policy agrees. Channel membership alone does not force every application to implement every message.

### Example 4

`GenerateReport` send operation declares reply variants `ReportAccepted`, `ReportCompleted`, and `ReportRejected`, correlation in a stable header, controlled reply channel, and deadline. Documentation states broker ack is not report completion and links outcome query for lost/late reply.

### Example 5

One CloudEvents header/message trait is shared, but tenant classification and payload remain event-specific. Resolved-document golden tests catch a trait change that accidentally made `subject` optional before publication.

### Example 6

A Kafka message binding declares key schema aligned with `orderId`; channel binding identifies topic properties supported by the binding version. Partition count, retention, replication, and ACLs live in IaC and are reconciled through stable channel identity.

### Example 7

An OAuth server scheme lists allowed flows/scopes, while an organization extension/link defines per-operation tenant/action policy. Negative integration tests prove a principal allowed to connect cannot publish an unauthorized message type or subject.

### Example 8

An external Avro schema reference points to a mutable branch and changes without AsyncAPI diff. CI rejects it, requiring immutable registry ID/release digest and cached bundle. Rebuilds now produce the same resolved contract.

### Example 9

Generator produces valid consumer classes, but fault test shows offset commit occurs before projection transaction. The type contract passes while behavioural acknowledgement fails. Implementation changes to atomic checkpoint/projection or durable inbox before conformance is claimed.

### Example 10

Runtime telemetry observes `CustomerMerged` schema ID on an undeclared channel. Reconciliation flags $U_B\setminus U_D$; the team discovers an emergency producer bypassed the outbox and ACL workflow. They disable it, repair delivery through the authoritative source, and add policy enforcement rather than editing the contract to bless drift.

## Cross-Program Connections

[Software Engineering Patterns](../../11-software-engineering-patterns/ROADMAP.md) supplies interfaces, adapters, generated-code boundaries, and ownership. [Data Engineering](../../19-data-engineering/ROADMAP.md) consumes catalogs, schemas, lineage, and stream contracts. [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies delivery, order, broker, and replay reasoning.

[Security Engineering](../../25-security-engineering/ROADMAP.md) governs identity, ACL/IAM, data classification, untrusted parsing, and supply chain. [Platform Engineering](../../29-platform-engineering/ROADMAP.md) owns parser/generator/registry/broker/IaC paved roads and drift detection. [Systems Engineering](../../26-systems-engineering/ROADMAP.md) contributes interface control, configuration baselines, verification, and lifecycle management.

## References

1. AsyncAPI Initiative. “AsyncAPI Specification 3.1.0.” <https://www.asyncapi.com/docs/reference/specification/v3.1.0>
2. AsyncAPI Initiative. “AsyncAPI Document Concepts.” Retrieved 2026-09-02. <https://www.asyncapi.com/docs/concepts/asyncapi-document>
3. AsyncAPI Initiative. “AsyncAPI Bindings Specifications.” Retrieved 2026-09-02. <https://github.com/asyncapi/bindings>
4. AsyncAPI Initiative. “AsyncAPI JSON Schema Versions.” Retrieved 2026-09-02. <https://github.com/asyncapi/spec-json-schemas>
5. JSON Schema Project. “JSON Schema Draft 2020-12.” <https://json-schema.org/draft/2020-12>
6. Cloud Native Computing Foundation. “CloudEvents Specification 1.0.2.” <https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md>
7. IETF. “RFC 3986: Uniform Resource Identifier (URI): Generic Syntax.” January 2005. <https://www.rfc-editor.org/rfc/rfc3986.html>

## Exercises

### Exercise 1

For an application that emits `PaymentCaptured` and receives `RefundRequested`, identify document scope, application identity/version, servers, channels, operation directions, messages, schemas, security, bindings, acknowledgement/outcome, and owner metadata. Explain direction from the application perspective.

### Exercise 2

Review a channel with key/address both `events`, messages `AnyMessage`, operation `subscribeEvents`, no parameters/security/bindings, and external schema URL on a main branch. List at least twelve contract risks and propose a durable shape.

### Exercise 3

Design AsyncAPI request/reply for `GenerateInvoiceExport` with accepted/progress/completed/rejected replies. Define correlation, reply channel/address, deadline, idempotency, bounds, late/lost replies, authorization, examples, and tests without claiming synchronous or exactly-once behavior.

### Exercise 4

Design CI/CD and runtime drift controls for an AsyncAPI 3.1.0 Kafka application using Avro registry schemas and infrastructure-as-code. Include pinned tools/bindings, validation, schema compatibility, examples, generation, ACLs, negative/fault tests, reconciliation, publication, rollout, and rollback.

### Exercise 5

Design a multi-application emergency-response contract catalog: dispatch command authority, unit-status events, dashboard receiver, partner webhook adapter, and analytics consumer. State document boundaries/perspectives, shared components, bindings/security, versioning, behavioural guarantees, and cross-document verification.

## Answers to the Exercises

### Answer 1

Document one payment application with durable URI/URN ID, `info.version`, owner/contact/lifecycle, spec version 3.1.0, environments, and exclusions. Declare actual broker/server host/path/protocol/version, safe variables, security and binding. Use semantic channel keys such as `capturedPayments` and `refundCommands`, each with deployed address/parameters, server membership, allowed messages, bindings, and descriptions.

`sendPaymentCaptured` has action `send` because the documented application emits the fact. `receiveRefundRequested` has action `receive` because it handles the command. Direction is never from broker or peer perspective. Messages reference immutable governed envelope/payload schemas with exact content/schema format; stable IDs/type/source/subject/tenant/classification/correlation/causation/order keys; synthetic examples; bounds; and compatibility owner.

Document that publish/broker ack is not refund outcome. The receive operation validates current authorization, deadline, precondition/idempotency and produces accepted/rejected/completed outcome through a declared status/reply mechanism. Bind server connection security plus channel/message/domain policy and negative tests. Protocol-specific key/header/queue/topic behavior belongs in exact binding versions; IaC/registry policy is linked and reconciled.

### Answer 2

Risks include ambiguous application scope/owner/perspective; key conflated with address; address lacks domain/environment/tenant meaning; no address parameters/constraints; generic message hides command/event/reply type; no discriminator or schema variants; operation name uses ambiguous subscribe rather than application `receive`; no operation message selection; absent servers/protocol/version; no connection security or domain authorization; no bindings; mutable schema branch; no content/schema format; no identity/correlation/classification/bounds; no acknowledgement/delivery/order/replay meaning; no compatibility/version; no safe examples; no IaC/ACL mapping; and no drift evidence.

Create one application document with durable ID/version/owner. Use stable channel key such as `confirmedOrders` and environment-mapped address `orders.{region}.confirmed` with enum region/provisioning/ACL/cardinality policy. Define `receiveOrderConfirmedForAnalytics` or actual action, explicit allowed message(s), governed immutable schema/CloudEvents profile, synthetic examples, classification, correlation/order key, and behavioural description. Declare servers/security/binding versions and reconcile address/topic/ACL/retention/partition policy to IaC. Pin schema registry ID/release digest and bundle for reproducible CI.

### Answer 3

The requester application has `sendGenerateInvoiceExport`; worker has a separate `receiveGenerateInvoiceExport`. Command message carries stable command/message ID, tenant/actor, export scope/options, issued time/deadline, idempotency fingerprint/precondition, controlled reply-route token, correlation/causation, schema/classification/bounds. Reply messages are distinct typed `InvoiceExportAccepted`, `InvoiceExportProgress`, `InvoiceExportCompleted`, and `InvoiceExportRejected`; operation reply references only controlled channel/address and correlation expression points to a required stable header.

Accepted means durable command acceptance, not completion. Progress is bounded/coalescible and nonterminal; completed provides protected object/reference/checksum/expiry; rejected states safe reason; terminality is documented. Provisioned/scoped reply channel binds requester tenant/principal, limits cardinality/lifetime/rate/bytes, and rejects arbitrary addresses/amplification. Deadline stops new acceptance but does not roll back committed work; late replies are recorded/discarded by policy. Lost reply resolves through same-ID outcome query/replay.

Examples cover every variant with synthetic data. Tests validate schemas/correlation, same-ID duplicate/different-fingerprint conflict, unauthorized tenant/reply address, expired command, lost/late/duplicate/reordered progress, worker crash after commit before reply, oversized output, reply flood, registry/broker outage, cleanup, and redrive. Broker settlement and delivery attempts are observed separately from application outcome; no exactly-once claim is made.

### Answer 4

Pin AsyncAPI 3.1.0, parser/linter/generator, Kafka binding version, Avro/runtime/registry versions, and generation templates in a reproducible toolchain. Parse against official schema; lint scope/owner/direction/naming/addresses/parameters/messages/security/classification/bounds/binding fields; resolve only immutable trusted references into a release bundle; validate every header/payload/example. Run Avro transitive writer/reader compatibility plus semantic/consumer review and language/runtime fixture matrix.

Generate docs/types/test scaffolds to governed outputs and fail unexpected drift; never hand-edit derivatives. Contract tests send/receive every declared type through target broker serializers, verify key/header/schema ID/address/correlation, and assert handler ack/outcome semantics. Negative tests cover invalid schema, unknown type, oversize/decompression, wrong key, unauthorized principal/tenant/topic/action. Fault tests cover duplicate/reorder, broker/registry outage/cache, poison/dead-letter/redrive, credential expiry, ACL change, lag/backpressure, process death, and recovery.

IaC remains authoritative for clusters/topics/partitions/replication/retention/quotas/encryption/ACL/service accounts; stable mappings reconcile those properties with AsyncAPI server/channel/bindings/security. CI plans/read-only compares by default; provisioning authority is separately controlled. Publish immutable AsyncAPI bundle/digest/catalog and schemas before producers. Roll out compatible consumers/producers in proven order with canary telemetry, then deprecate. Preserve previous bundle/schema/generated artifacts and runtime compatibility for rollback/replay.

Runtime compares observed application/operation/message/schema/channel/direction against declared surface and ACL policy, with safe telemetry for errors, unknowns, lag, acks/outcomes, and denies. Alert undeclared runtime or stale declared surfaces to owner, using an adequate observation window. Restore drills recover registry IDs, contract catalog, IaC, ACLs, and toolchain evidence.

### Answer 5

Create separate documents for independently deployed applications: dispatch authority, unit telemetry/status producer, dashboard projection/edge receiver, partner webhook adapter, and analytics consumer. Each has durable identity/version/owner, actual servers/security/bindings, and send/receive operations from its own perspective. Do not invert one shared document. A catalog links their contracts and declared message compatibility.

Dispatch authority receives `DispatchUnit` command and sends typed accepted/rejected/completed outcomes plus authoritative facts from one transaction/outbox. It documents command deadline/current authorization/idempotency/precondition/outcome lookup. Unit producer sends `UnitStatusChanged` facts with unit/incident subject versions, stable IDs, occurred time, tenant/classification, correction/gap rules. Dashboard receives authorized minimized projection events and may expose SSE separately; partner adapter receives allowed facts and sends signed webhooks; analytics receives minimized retained facts with replay semantics.

Share small pinned components: CloudEvents-like envelope/header schemas, trusted tenant/correlation/causation fields, domain value types, security schemes, and classifications. Keep payload schemas/event ownership/versioning per domain. Use exact Kafka/AMQP/HTTP binding versions as applicable; webhook behavior may have its own AsyncAPI HTTP binding/adapter contract and external delivery policy. Connection security plus channel ACL and domain authorization are all tested.

Cross-document verification checks producer message/schema against every declared receiver, registry transitive compatibility, addresses/forwarders, partition keys/order, ACL/IAM, retention/replay, and webhook mapping. It verifies acknowledgement layers, inbox/outbox, duplicates/gaps, redrive, sensitive-field minimization, and tracing without confusing transport with business completion. IaC reconciliation checks broker and adapter configuration.

For breaking facts/commands introduce new type/operation/channel only as required, publish contracts/schemas first, update tolerant consumers, dual publish from one authority with identity mapping, compare parity, deprecate, and retain old artifacts for replay horizon. Fault exercises cover command response loss, producer duplicate, consumer gap/lag, registry/broker/region failure, auth revocation, partner outage/redrive, dashboard slow clients, and analytics replay. Catalog ownership never replaces application/domain ownership.
