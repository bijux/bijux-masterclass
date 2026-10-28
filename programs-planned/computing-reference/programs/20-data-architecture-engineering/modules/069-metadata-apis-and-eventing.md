---
module_id: DARCH-069
program: Data Architecture Engineering
level: 2
module_number: 69
title: Metadata APIs and Eventing
status: complete
last_verified: 2026-09-03
---

# Metadata APIs and Eventing

## One-Page Review

### Governing question

How should metadata services expose authoritative reads, controlled mutations, searches, traversals, bulk exchange, subscriptions, and change events so humans and machines can integrate safely under concurrency, retries, partial failure, evolving schemas, authorization, and historical replay?

### Essential definitions

- A **metadata API** is a governed interface for reading, proposing, validating, changing, searching, traversing, or exporting metadata resources and assertions.
- A **metadata event** is an immutable statement that a relevant metadata occurrence or accepted state transition happened, identified and contextualized for asynchronous consumers.
- A **command** requests an action; an **event** states an occurrence; a **query** requests information. Their authority and retry semantics differ.
- A **proposal** is requested metadata change that has not yet passed authorization, validation, conflict resolution, and acceptance.
- An **accepted change** is a committed authoritative transition with stable identity, previous and resulting versions, provenance, and decision evidence.
- A **representation** is the current or historical content transferred for a resource; it is not the resource itself.
- A **strong validator** such as an appropriate ETag can identify a selected representation for conditional requests.
- **Optimistic concurrency** applies a mutation only if the client's expected version or validator still matches authoritative state.
- An **idempotency key** identifies one intended mutation within a declared principal and scope so a retry can return the first outcome without repeating the effect.
- A **cursor** is an opaque continuation token bound to a query, ordering, authorization context, and snapshot or consistency model.
- An **outbox** records accepted state and publishable events atomically so committed changes cannot be lost between storage and broker publication.
- An **inbox** records consumed event identity and outcome so redelivery does not repeat an already applied side effect.
- **At-least-once delivery** can redeliver; **at-most-once delivery** can lose; **effectively-once processing** requires scoped identity, deduplication, atomic effects, and bounded assumptions.
- A **tombstone** is an explicit lifecycle event or representation indicating removal or retirement while preserving enough identity and provenance for convergence.
- **Reconciliation** compares API state, event history, consumer projections, offsets, and source authorities to detect and repair divergence.

### Central model, mechanism, or theorem

Represent a metadata interface system as:

`M = (I, R, Q, C, V, E, D, P, A, O, S, L)`

where `I` is identity, `R` resource representations, `Q` query and traversal, `C` commands and proposals, `V` validation and version control, `E` accepted events, `D` delivery and deduplication, `P` projections and reconciliation, `A` authorization and audit, `O` operation and recovery, `S` schemas and compatibility, and `L` lifecycle closure. A successful command response and an event delivery are different facts. Safe integration requires stable identities, conditional mutation, atomic state-event recording, explicit delivery guarantees, authorization-aware representations, schema evolution, replay, and proof that consumers converge or surface unresolved gaps.

### Critical invariants

- Resource identity, representation version, request identity, proposal identity, decision identity, event identity, delivery identity, and trace identity remain distinct.
- Safe reads have no intended mutation; method semantics and status codes match actual behavior.
- Every accepted mutation records actor, authority, expected version, validated input, resulting version, policy decision, time, and audit evidence.
- Idempotency keys are scoped to principal and operation and reject reuse with a different request digest.
- Conditional mutation fails visibly on stale versions rather than silently applying last-write-wins.
- Canonical state and its outbox event are committed atomically; publication and consumer application are separately observable.
- Event consumers tolerate duplication, bounded reordering, late arrival, unknown schema, and poison content without inventing state.
- Event envelopes name producer, event identity, type, subject, occurrence time, data schema, content type, tenant, and correlation as applicable.
- Event data is sufficient to apply a declared transition or points to immutable authorized state that remains resolvable for the replay horizon.
- Search, pagination, graph traversal, subscriptions, errors, and events preserve the caller's disclosure boundary.
- Consumer projections expose source offset, schema support, staleness, reconciliation status, and reset history.
- Deprecation and retirement close endpoints, subscriptions, producers, consumers, credentials, caches, replays, and recovery without making retained history uninterpretable.

### Common failures

Common failures include using `GET` to mutate; treating `POST` retries as safe without idempotency; using timestamps as universal versions; applying blind `PATCH`; defining null ambiguously in merge patch; letting JSON Patch address unauthorized fields; returning `200` for every outcome; embedding secrets in error details; offset pagination over changing results; encoding server state in forgeable cursors; allowing GraphQL field selection to bypass authorization; emitting requested changes as accepted facts; publishing after commit without an outbox; assigning a new event ID on retry; promising exactly once without scope; relying on broker order across keys; making consumers fetch mutable `latest`; silently dropping unknown event versions; retrying poison events forever; dead-lettering without reconciliation; using correlation IDs for deduplication; logging full sensitive events; replaying into live side effects without isolation; and retiring APIs while old publishers still emit.

### Compact example

Five invented mutation requests target one metadata record at version 3. Two changes apply, one replay returns its original result, one stale write conflicts, and one forbidden-field proposal is rejected; the final version is 5. Two accepted changes create two outbox events. Five delivery attempts to two consumers include one duplicate, resulting in four consumer applications, one deduplicated delivery, and two consumers converged at version 5. Executable evidence proves only this in-memory policy and arithmetic—not HTTP compliance, durability, atomic transactions, broker delivery, authorization, schema compatibility, or distributed convergence.

### Connections

[DARCH-019](019-model-versioning.md), [DARCH-027](027-producer-and-consumer-contracts.md), [DARCH-061](061-metadata-architecture.md), [DARCH-062](062-metadata-harvesting-and-synchronization.md), [DARCH-064](064-lineage-architecture.md), [DARCH-067](067-schema-registries.md), and [DARCH-068](068-data-catalog-architecture.md) establish version, contract, metadata, lineage, registry, and catalog foundations. [DARCH-070](../ROADMAP.md) next connects technical metadata to business meaning.

## Governing Question

Metadata serves people through pages and machines through APIs, connectors, event streams, webhooks, and exported files. A catalog UI that works interactively can still fail as an integration platform if mutations overwrite one another, search pagination skips results, consumers cannot resume, event schemas drift, permissions leak through facets, or accepted state and emitted events diverge.

The governing question is how to give each interaction precise semantics under retries and partial failure. Reads, commands, proposals, decisions, snapshots, deltas, and events must be distinguished. A correct architecture makes accepted state inspectable through APIs, communicates transitions without claiming impossible delivery guarantees, preserves provenance and authorization, and supplies reconciliation paths when asynchronous consumers inevitably diverge.

## Why This Matters

[RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html) defines HTTP resources, representations, methods, status codes, validators, conditional requests, content negotiation, authentication challenges, safe methods, and idempotent methods. Metadata APIs benefit from those semantics: `GET` retrieves without intended mutation, `PUT` expresses replacement with idempotent intent, validators support concurrency, and status codes distinguish success, conflict, precondition failure, absence, and authorization.

[RFC 9111](https://www.rfc-editor.org/rfc/rfc9111.html) defines HTTP caching, freshness, validation, invalidation, and cache-control behavior. Metadata representations can be expensive and widely reused, yet they often contain authorization-sensitive and rapidly changing claims. Explicit cache keys, validators, private or public controls, and invalidation semantics are correctness and disclosure requirements.

[RFC 9457](https://www.rfc-editor.org/rfc/rfc9457.html) defines Problem Details for HTTP APIs using fields including `type`, `status`, `title`, `detail`, and `instance`, with extension members. A stable problem type can let clients distinguish validation, version conflict, authorization, unsupported schema, rate limit, and projection-staleness outcomes without parsing human prose.

[RFC 6902](https://www.rfc-editor.org/rfc/rfc6902.html) defines JSON Patch as an ordered sequence of `add`, `remove`, `replace`, `move`, `copy`, and `test` operations addressed by JSON Pointer. JSON Patch can express precise metadata edits and precondition-like tests, but the service must authorize every resolved path, apply the sequence atomically, and avoid leaking protected values through diagnostics.

[RFC 7396](https://www.rfc-editor.org/rfc/rfc7396.html) defines JSON Merge Patch by example: object members can be added or replaced, while `null` signals removal. It is compact for object-shaped resources but poorly fits cases in which explicit null is a meaningful metadata value or arrays need element-level edits. Media type and field semantics must be explicit.

[RFC 8288](https://www.rfc-editor.org/rfc/rfc8288.html) defines Web Linking, link context, target, relation type, and attributes. Metadata resources can expose typed links to versions, predecessors, successors, owners, schemas, terms, distributions, services, lineage, next pages, and documentation without hard-coding every relation into bespoke response fields.

The [OpenAPI Specification 3.1.1](https://spec.openapis.org/oas/v3.1.1.html) describes HTTP APIs using paths, operations, parameters, request bodies, responses, callbacks, webhooks, security, links, and Schema Objects. It supports machine-readable review and generation, but an OpenAPI document must still specify real concurrency, pagination, idempotency, authorization, and lifecycle behavior in sufficient detail.

The [AsyncAPI Specification 3.0.0](https://www.asyncapi.com/docs/reference/specification/v3.0.0) models message-driven APIs with servers, channels, operations, messages, correlation, security, reusable components, and protocol bindings. It distinguishes channel addresses from operations and accommodates events, commands, requests, and responses. A metadata event contract needs both protocol-neutral meaning and binding-specific delivery details.

The [CloudEvents 1.0.2 specification](https://github.com/cloudevents/spec/blob/ce@v1.0.2/cloudevents/spec.md) defines a common event envelope with required `id`, `source`, `specversion`, and `type`, plus optional `subject`, `time`, `datacontenttype`, and `dataschema`. The producer must make `source` plus `id` unique for distinct events, while a duplicate resend can reuse the same ID. This supports transport-independent event identity but does not create end-to-end exactly-once effects.

The [GraphQL October 2021 specification](https://spec.graphql.org/October2021/) defines schemas, queries, mutations, subscriptions, validation, execution, response shape, errors, introspection, and type-system evolution. GraphQL can reduce over-fetching across heterogeneous metadata graphs, but field-level authorization, query cost, caching, pagination, mutation concurrency, and subscription recovery remain application responsibilities.

Together these sources establish reusable interface mechanisms without choosing a complete metadata design. The architecture must bind them to stable catalog identity, accepted assertion semantics, policy, event history, consumer projections, and operating guarantees.

## Prerequisites and Retrieval

You should understand metadata architecture, catalogs, HTTP, REST, GraphQL, JSON, APIs, events, message brokers, schemas, compatibility, optimistic concurrency, transactions, event sourcing, outbox and inbox patterns, pagination, authorization, caching, distributed systems, observability, disaster recovery, and lifecycle governance.

Retrieve resource, representation, media type, method safety, idempotence, validator, ETag, conditional request, precondition, idempotency key, request digest, problem type, JSON Pointer, JSON Patch, Merge Patch, cursor, snapshot, query, mutation, subscription, command, proposal, decision, event, source, subject, correlation, causation, sequence, partition, offset, outbox, inbox, at-least-once, replay, tombstone, projection, checkpoint, dead letter, webhook, backpressure, reconciliation, deprecation, and retirement.

As a retrieval test, consider a client that times out after `POST /metadata/changes`, then sees an `asset.updated` event twice and a search result that still shows the old owner. Ask whether the first request committed; which idempotency key and digest identify its intent; which entity version it expected; whether the event describes a proposal or accepted state; whether both deliveries share event identity; which consumer checkpoint and schema apply; whether the search projection lags or rejected the event; whether authorization changes the visible representation; and which reconciliation operation can repair it. A timeout and duplicate event alone answer none of those questions.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish resource, representation, query, command, proposal, accepted change, event, delivery, projection, and trace identities;
2. design HTTP and GraphQL metadata reads and mutations with precise safety, idempotency, validation, status, and concurrency semantics;
3. choose replacement, JSON Patch, Merge Patch, domain operations, and assertion APIs by meaning and authorization boundary;
4. build stable pagination, filtering, field selection, graph traversal, bulk export, and temporal reads;
5. specify metadata events using stable envelopes, schemas, versions, subject identity, causation, ordering, and tombstones;
6. implement transactional outbox, consumer inbox, retry, backpressure, dead-letter, replay, and reconciliation patterns;
7. design webhooks and subscriptions with authentication, delivery proof, rotation, filtering, resume, and abuse controls;
8. protect metadata APIs, caches, errors, query surfaces, events, logs, tenants, and behavioral telemetry;
9. operate SLOs, lag, schema adoption, consumer health, projection correctness, recovery, migration, and economics; and
10. deprecate and retire interfaces and event types without breaking retained metadata history.

## Core Exposition

**Start from interaction intent.** Classify each operation as query, command, proposal, decision, notification, or event. State actor, authority, target, expected version, side effects, result, retry behavior, latency, consistency, and audit.

A request to suggest a glossary term is not the same as a steward's decision to accept it. An event that a proposal was submitted is not an event that authoritative metadata changed.

**Model resources before endpoints.** Give stable identities to cataloged resources, catalog records, assertions, relationships, vocabularies, workflows, quality measurements, schemas, consumers, and subscriptions. Design representations and operations around those identities.

Avoid RPC names that conceal resource state and concurrency. Domain operations remain appropriate when replacement or generic patch cannot express required invariants, but their requested and accepted outcomes should still be addressable.

**Separate resource and representation.** A URI identifies a resource; a response transfers a selected representation. Content negotiation, viewer authorization, field masks, time, and version can produce different representations of the same resource.

Validators apply to selected representations. If two viewers see different fields, a shared cache key or ETag must not let one receive the other's content.

**Use safe methods safely.** `GET` and `HEAD` should not create stewardship assignments, mark notifications read, register subscriptions, or cause externally significant mutations merely because a crawler retrieves a link.

Operational logging and cache warming can occur, but clients and intermediaries rely on safe intent. Model action endpoints with methods whose semantics permit change.

**Use idempotent method semantics accurately.** Repeating `PUT` or `DELETE` has the same intended effect, although responses and audit observations can differ. `POST` is not generally idempotent, but a domain service can make a specific operation safely retryable through an idempotency contract.

Do not call every request “idempotent” because duplicates are rare. Define intent identity, storage horizon, scope, response replay, conflict, and side effects.

**Design idempotency keys.** Bind a client-supplied key to authenticated principal, tenant, operation, target scope, normalized request digest, and expiry. Persist the outcome before acknowledging success.

A retry with the same key and digest returns the original status and resource or decision identity. Reusing the key with a different digest is a conflict. Keys do not replace resource version checks: two different intended requests can still race.

**Use optimistic concurrency.** Return a strong validator or explicit immutable state version. Require `If-Match` or an expected version for consequential mutation. Apply the command only if it still targets the state the client reviewed.

On mismatch, return current version identity or a safe link to retrieve it, not a silent merge. Whether a client retries automatically depends on field ownership and domain semantics.

**Distinguish precondition failure from business conflict.** A failed representation precondition can use HTTP's precondition status semantics. A proposal can also be structurally current but conflict with governance rules or another active workflow.

Use stable problem types and machine-readable extensions to differentiate stale validator, duplicate identity, policy denial, invalid transition, unresolved assertion conflict, schema error, and rate limit.

**Make errors useful and safe.** A problem response can include type URI, status, title, detail, instance, trace, field paths, validation codes, current version, retry guidance, and documentation link.

Do not expose hidden resource existence, protected current values, query text, credentials, stack traces, topology, or another tenant's identifiers. Human detail is not a stable parser contract.

**Choose replacement deliberately.** `PUT` is appropriate when the client can provide a complete replacement representation and the server defines omitted-field behavior. It supports clear idempotent intent and conditional mutation.

Replacement becomes dangerous when the representation mixes server-managed, source-managed, inferred, and human-managed fields. Separate resources or use domain operations so a client cannot erase fields it never saw.

**Use JSON Patch for precise operations.** JSON Patch expresses ordered operations and can include `test`. It handles individual array positions and distinguishes removal from null assignment.

Authorize every source and target path after pointer resolution, constrain allowed operations, apply the document atomically, validate final domain state, and bound operation count, path depth, and document size. Array indexes are fragile under concurrent reordering.

**Use Merge Patch for simple object changes.** Merge Patch is concise when null means removal and arrays can be replaced wholesale. Advertise `application/merge-patch+json` and document each field's mutability.

Do not use it when explicit null is a meaningful assertion value unless the resource model supplies another representation. Avoid pretending an array element can be safely merged.

**Prefer domain operations for semantic transitions.** `claim-owner`, `approve-term`, `resolve-conflict`, `certify-purpose`, `deprecate`, and `retire` can express actor, preconditions, evidence, and state-machine rules more clearly than arbitrary patch.

Make the operation request a durable proposal when approval is asynchronous. Return its identity and status location rather than holding an HTTP connection for organizational latency.

**Separate proposal and acceptance.** Store proposed change, submitter, request identity, target version, patch or intent, evidence, policy, validation, and expiry. Acceptance records reviewer or automated authority, decision, resulting entity version, event identities, and reason.

Consumers of authoritative metadata should subscribe to accepted changes, not infer acceptance from proposal submission. Audit consumers may subscribe to both with distinct event types.

**Validate in layers.** Authenticate, authorize operation and fields, parse media type, validate schema, resolve references, check size, normalize identity, apply preconditions, evaluate domain invariants, policy, and workflow state, then commit.

Return stable diagnostics for each layer. A schema-valid patch can still violate ownership authority, lifecycle, relationship cardinality, or legal policy.

**Commit state and outbox atomically.** In one transaction, persist the new canonical version, audit or decision record, idempotency outcome, and outbox event. A dispatcher later publishes pending events and records delivery attempts or broker acknowledgement.

Without an outbox, a crash after state commit but before publish loses notification; publish before commit can announce a transition that rolls back. Distributed transactions are another option but usually increase coupling and operating complexity.

**Give events independent identity.** A state version identifies resulting state. An event ID identifies one occurrence. A request ID identifies one submitted intent. A trace ID connects observations. A correlation ID connects a conversation. A causation ID points to the triggering event or command.

Do not deduplicate by correlation ID because several legitimate events can share one workflow. A republished identical occurrence retains event identity; a compensating or superseding occurrence gets a new identity and causal link.

**Use a stable event envelope.** Include specification or envelope version, event ID, source, type, subject, occurrence time, data content type, data schema, tenant or partition context, trace, correlation, causation, and producer version as policy allows.

CloudEvents supplies portable core attributes. Define metadata-specific extensions sparingly and register their meaning. Keep sensitive routing context out of broadly visible headers.

**Name event types by durable occurrence.** Examples include `catalog.assertion.accepted`, `catalog.relationship.retired`, `catalog.resource.deprecated`, `catalog.profile.validation-failed`, and `catalog.projection.rebuilt`.

Avoid types such as `metadata.updated` whose consumers must diff arbitrary blobs to find meaning. Avoid organizational names and temporary implementation steps. State whether type version changes are in the type name, data schema, or both.

**Define subject identity.** The envelope subject should resolve within the declared source. Carry full stable entity identity in data where required. A mutable display path should not be the only subject key.

For field or relation events, state whether the subject is the parent resource, assertion, edge, or field identity. Partitioning and authorization often depend on this choice.

**Choose notification versus state-transfer events.** A notification event contains identity, version, occurrence, and a link for authorized retrieval. A state-transfer event carries enough accepted state or delta for a consumer to apply locally.

Notification is small and ensures current authorization at fetch, but couples consumers to API availability and can collapse intermediate history if they fetch `current`. State transfer supports replay and offline projections but increases size, disclosure, compatibility, and deletion obligations.

**Use immutable retrieval links.** If an event points to state, link to the exact accepted version rather than mutable current or latest. Define retention and authorization for the replay horizon.

If immutable state can later be legally erased, consumers need an explicit redaction or unavailability outcome and reconciliation policy rather than silently receiving different content under the same identity.

**Define event data semantics.** A snapshot event contains a complete representation under a schema. A delta event describes change from a named prior version to a named resulting version. A domain event describes occurrence and may not reconstruct full state.

Do not call an arbitrary partial object a patch without defining application rules. Include before values only when necessary and authorized; they increase disclosure and retention.

**Version event schemas.** Register immutable data schemas and define backward, forward, and transitive compatibility relative to consumers and retained events. Preserve envelope semantics separately from data schema.

Adding optional data can still break strict consumers, signatures, size limits, or semantics. Test actual serializers, generated code, filters, and subscribers.

**Document event-driven APIs.** AsyncAPI can specify servers, channels, operations, messages, security, bindings, and correlation. Document producer and consumer roles, channel address, partition key, retention, ordering, retry, redelivery, schema, dead letter, replay, and support.

A protocol-neutral document does not replace binding details such as Kafka compaction, AMQP acknowledgement, webhook HTTP response, or cloud queue visibility timeout.

**Define ordering scope.** Brokers commonly order within a partition, not across a topic or system. Select partition keys such as stable entity identity when per-entity order matters.

Cross-entity invariants cannot rely on total order unless architecture explicitly provides it. Carry resulting entity version and causal dependencies so consumers can detect gaps and stale arrivals.

**Handle late and out-of-order events.** A consumer compares source authority, entity identity, event identity, effective time, and resulting version. It can ignore an older projection update without discarding the audit event.

Do not sort solely by producer timestamp under clock skew. Sequence numbers require a declared allocator and scope; gaps need timeout, fetch, or replay policy.

**Design at-least-once processing.** Assume an event can arrive repeatedly after acknowledgement loss, consumer restart, broker redelivery, replay, or dispatcher retry. Record `(source, event_id)` in an inbox atomically with the consumer effect.

Bound inbox retention according to redelivery and replay. If IDs can be reused after expiry, effectively-once claims end at that boundary.

**Avoid universal exactly-once claims.** A broker transaction can give strong guarantees inside a supported topology. External APIs, email, policy engines, caches, and databases can still observe duplicates or partial effects.

State the exact boundary: one partition to one transactional projection, one idempotent downstream operation, or one database transaction. Provide compensation and reconciliation outside it.

**Design retries by error class.** Retry transient transport, throttling, and availability failures with exponential backoff, jitter, budget, and broker-aware delay. Do not retry permanent schema, authorization, identity, or invariant errors unchanged.

Preserve first failure, attempt count, next eligibility, last error class, and age. Global retry storms can overwhelm recovering metadata services.

**Use dead letters as workflow, not disposal.** A dead-letter record preserves original event or secure reference, identity, source position, schema, error, attempts, consumer version, time, and replay authorization.

Assign ownership, alerting, triage, repair, replay, expiry, and reconciliation. A growing dead-letter queue is accepted divergence until resolved.

**Apply backpressure.** Bound consumer concurrency, queues, payload sizes, graph expansions, webhook fan-out, and per-tenant work. Pause partitions or shed noncritical projections before memory collapse.

Prioritize security, lifecycle, and tombstone events when safe, but preserve per-entity ordering. Expose lag by event type, tenant, partition, and age.

**Build inbox projections deliberately.** Each consumer records supported schemas, last source positions, per-entity versions, deduplication state, projection build version, failures, and reset history.

Projection application should be deterministic under replay. If current time, external mutable state, or randomness affects output, capture inputs or accept nonreproducibility explicitly.

**Reconcile projections.** Compare authoritative entity versions, event-log positions, consumer checkpoints, counts, digests, tombstones, and sampled representations. Identify missing, duplicate, unauthorized, stale, and impossible states.

Repair by replay, targeted snapshot, or rebuild from a known checkpoint. Record repair identity and verify user-visible API or search results, not merely queue drain.

**Design cursor pagination.** Define a deterministic order with a unique tie-breaker. Bind opaque cursors to normalized filters, sort, field selection, tenant, authorization context, page size limits, and snapshot or consistency token.

Offset pagination over changing metadata can duplicate or skip rows. Keyset cursors improve continuity but do not create snapshot isolation. Expired or mismatched cursors should fail explicitly.

**Expose pagination links.** Return next and previous links or cursors and document whether total counts are exact, approximate, authorized, and snapshot-consistent. Calculating a global total can be costly and can leak hidden resources.

Do not let clients edit opaque cursors. Sign or store server state and rotate keys without invalidating every active session unexpectedly.

**Design filtering and sorting.** Use stable field names, operators, value types, timezone semantics, null behavior, case rules, repeated parameter semantics, maximum clauses, and cost limits.

Only expose filters authorized for the viewer. An error saying “hidden owner exists” can disclose as much as a result.

**Bound graph traversal.** Accept typed edge sets, directions, depth, time, confidence, lifecycle, and result limits. Return continuation for frontiers rather than expanding an unbounded lineage graph.

Apply authorization at every node and edge and prevent hidden intermediates from being inferred through path length, counts, or timing. State whether paths are complete under the viewer's permissions.

**Support temporal reads.** Consumers may need state at an accepted version, effective time, or event offset. Define what each axis means and whether assertions observed later but effective earlier appear.

Immutable version reads enable audit and event resolution. Current reads are convenient but not reproducible unless the resolved version is recorded.

**Design bulk exchange separately.** Bulk export and import need manifests, snapshot identity, profile and schema versions, file digests, partitions, compression, encryption, authorization, expiry, resume, errors, counts, and reconciliation.

Do not push millions of records through a page API. Use asynchronous jobs with stable status, result location, cancellation, idempotency, and cleanup.

**Use links and discoverability.** Typed Web Links can connect current representation, immutable versions, predecessor, successor, schema, profile, owner, terms, lineage, distribution, service, problem documentation, next page, and subscription.

Link relations need stable semantics and authorization. A link target can be hidden even when the source is visible.

**Use GraphQL for connected reads where appropriate.** A typed graph lets clients select entity, assertions, terms, quality, lineage, and ownership in one operation. Persisted queries can bound trusted use and improve caching.

Enforce authorization during field and edge resolution, not after constructing a full graph. Bound depth, aliases, fragments, list sizes, resolver fan-out, and total cost; prevent introspection from exposing forbidden schema where necessary.

**Use mutations conservatively in GraphQL.** Mutation fields execute serially at the top level, but that is not global transaction or concurrency safety. Carry expected versions and idempotency keys in mutation input and return typed result or stable problem detail.

Do not encode every business error as transport success without a consistent client contract. Preserve audit and outbox behavior shared with HTTP mutations.

**Treat subscriptions as resumable views.** A live connection can notify clients, but disconnects are normal. Define cursor or event offset, resume window, initial snapshot, filters, authorization recheck, schema, keepalive, backpressure, and overflow.

A subscription without durable resume is a notification convenience, not a complete change feed. Reconciliation remains necessary.

**Design webhooks as untrusted outbound calls.** Validate destination ownership, restrict schemes and ports, prevent server-side request forgery, resolve DNS safely, control redirects, sign content, include timestamp and delivery identity, rotate secrets, and support endpoint disablement.

Receivers acknowledge quickly and process asynchronously. Retries reuse event and delivery identity as declared. Do not put sensitive metadata into a URL.

**Authenticate events end to end.** Broker transport authentication identifies a connection, not necessarily original event provenance after forwarding. Bind producer identity, source, schema, tenant, and content integrity through trusted infrastructure or signatures where boundaries require it.

Define key rotation, algorithm agility, clock tolerance, replay protection, canonical bytes, verification failure, and archival validation. Encryption and signature serve different purposes.

**Authorize publication and subscription.** Separate permissions to propose, mutate, approve, publish event types, create subscriptions, consume channels, replay history, inspect dead letters, and export bulk state.

Prevent a publisher from forging another source or tenant. Event filters and topic names are not sufficient authorization boundaries by themselves.

**Protect caches.** API caches key on full URI, method, selected headers, authorization or private scope, media type, field mask, temporal version, and representation encoding as applicable.

Use validators and cache control explicitly. Invalidate or revalidate current resources after accepted mutations, while immutable version representations can be cached longer. Never cache sensitive problem detail publicly.

**Protect query privacy.** Search strings, filters, graph subjects, field selections, webhook destinations, and subscriptions reveal user intent and hidden investigations.

Minimize, classify, redact, aggregate, and retain them by declared purpose. Avoid logging full request or event bodies by default.

**Rate-limit by cost and authority.** Count not only requests but mutation weight, patch operations, graph fan-out, query complexity, result bytes, subscriptions, replay volume, export size, webhook destinations, and failed authorization.

Expose retry guidance where safe. Isolate tenants so one reindex or replay cannot exhaust runtime reads or security events.

**Version APIs by compatibility surface.** Consider resource representation, media type, fields, null and omission, enum values, error types, pagination, filters, sorting, authentication, rate limits, links, event types, schemas, channels, retention, and delivery.

Prefer additive evolution only when clients tolerate unknown fields and enum values. Test real generated clients and persisted queries. Publish support and removal windows.

**Coordinate snapshot and event bootstrap.** A new consumer needs a consistent snapshot plus a change position. Acquire or label the snapshot at offset `o`, load it idempotently, then consume events after `o`.

If snapshot creation and event capture are not coordinated, define overlap and deduplication or gap detection. “Export current, then subscribe” can miss changes between the two operations.

**Design replay modes.** Replay can rebuild a projection, repair a range, test a new consumer, or reproduce history. Isolate side effects, specify source offsets or time, preserve event identity, label replay context, throttle, and audit.

Never point an unmodified production notification consumer at a replay stream. Email, ticket, access, and policy actions need dry-run, inbox reset rules, or idempotent external operations.

**Support schema adoption.** Track producer schema version, consumer supported range, unknown version failures, upgrade status, and retained history. Canary new event schemas to shadow consumers and compare outcomes.

Do not delete old schemas while retained events or snapshots reference them. Compatibility pass is necessary but consumer activation remains separate.

**Observe the command path.** Measure requests, authorization, validation, precondition failures, idempotent replays, conflicts, accepted changes, latency, transaction failure, outbox depth, publish lag, and audit persistence by operation and tenant.

High conflict can indicate healthy concurrency protection or a poor workflow. Interpret rates using attempted mutations and client behavior.

**Observe the event path.** Measure produced, published, broker-acknowledged, delivered, redelivered, deduplicated, applied, rejected, retried, dead-lettered, replayed, and reconciled events.

Track end-to-end accepted-state-to-consumer-visible latency, not just broker lag. Preserve denominators and event age distributions.

**Set separate SLOs.** Current entity read, immutable version read, search, traversal, mutation acceptance, proposal decision, event publication, delivery, projection freshness, subscription recovery, export, and reconciliation have different objectives.

Define correctness and completeness alongside latency and availability. A fast stream that silently loses tombstones violates its purpose.

**Test contracts at several layers.** Validate OpenAPI and AsyncAPI documents, schemas, media types, error examples, links, generated clients, filters, cursors, patch semantics, field authorization, ETags, retries, idempotency, outbox, duplicates, ordering, gaps, unknown versions, dead letters, replay, and reconciliation.

Use model-based and property testing for state transitions. Inject failures before and after commit, outbox publish, acknowledgement, inbox write, projection apply, and webhook response.

**Recover the whole interface.** Back up canonical state, versions, assertions, idempotency outcomes, proposals, decisions, audit, outbox, event log or durable archive, subscription state, inboxes as needed, schemas, cursor keys, webhook secrets, policies, and checkpoints.

Restore into isolation, verify identities and digests, rebuild projections, exercise historical reads, replay without external effects, test authorization and signatures, rotate exposed secrets, reconcile, then resume publishers before consumers according to the recovery plan.

**Migrate with dual evidence.** Inventory clients, endpoints, operations, fields, errors, cursors, generated SDKs, event producers, consumers, filters, schemas, channels, offsets, replays, webhooks, and SLOs. Map semantic differences, not only payload shapes.

Shadow reads, dual-write through one authority or publish an accepted change log, compare responses and projections, canary clients, preserve rollback, and reconcile. Avoid two independently writable authorities without conflict ownership.

**Deprecate visibly.** Responses, schemas, documentation, client libraries, dashboards, and events should name replacements, dates, scope, and migration. Track actual use by authenticated client and event consumer.

Do not infer safety from low aggregate traffic. Scheduled annual jobs and disaster recovery can be important consumers.

**Retire completely.** Disable old writes first, close producers, migrate consumers and replays, end subscriptions and webhooks, remove aliases and routes, revoke credentials and signing keys as scheduled, stop outbox dispatch, update schemas and recovery, and preserve required historical resolution.

Test that old events cannot recreate retired state, old clients receive a stable terminal outcome, and restored backups do not restart obsolete publishers.

## Definitions and Notation

Let metadata resource `r` have authoritative immutable state versions `v_0, v_1, ...`. Let `Rep(r, v, u, m)` be the representation of version `v` visible to principal `u` under media type or field mask `m`.

Let request `q = (principal, tenant, operation, target, expected, body, key, digest)`. Idempotency map `I(principal, tenant, operation, key)` stores request digest and original outcome. Same key with a different digest is a conflict.

Let conditional transition `T(r, v_i, q) -> (v_{i+1}, d, e)` occur only when `q.expected = v_i` and validation and authorization pass. Here `d` is decision evidence and `e` is an outbox event.

Let atomic commit invariant be `Committed(v_{i+1}) ⇔ Committed(d) ∧ Committed(I_q) ∧ Committed(e_outbox)` for the transaction's governed components. Broker acknowledgement is not inside that equivalence unless a distributed transaction explicitly includes it.

Let event `e = (source, id, type, subject, occurred, schema, data, cause, correlation, version)`. Event identity is `(source, id)`. Content digest can detect corruption but does not replace event identity or producer authentication.

For consumer `c`, inbox key `J_c(source, id)` records processing outcome. Application function `Apply_c(state, e)` should be deterministic under supported schema and context. If `J_c` already records success, redelivery returns the stored outcome without repeating effect.

Let an entity event carry prior version `p(e)` and resulting version `n(e)`. A consumer at version `k` can apply a contiguous transition when `p(e)=k`; `p(e)>k` signals a gap, and `n(e)≤k` often signals stale or duplicate state projection, subject to event semantics.

Let accepted log offset be `o_a`, broker-published offset `o_b`, and consumer checkpoint `o_c`. Publication lag and consumption lag are distinct. Offset equality does not prove content correctness, so reconciliation compares entity versions and digests too.

Let cursor `κ = Protect(query_digest, sort, last_key, snapshot, tenant, auth_epoch, expiry)`. Protection can be server-side opacity or authenticated encoding. A cursor is valid only for its bound context.

Let delivery attempts `A(e,c)` include redeliveries and applications `P(e,c)` include successful first effects. Deduplication count is `|A| - |distinct successfully applied event-consumer pairs|` only under complete observation.

Let end-to-end event freshness at time `t` be `t - accepted_time(e)` for the consumer-visible application, not merely broker enqueue latency.

Let convergence predicate `Conv(c, r, v, o)` require consumer `c` to represent authorized projection of resource `r` at authoritative version `v`, to have processed through required offset `o`, and to have no unresolved dead-letter or schema gap affecting `r`.

Let retirement closure `Closed(x)` require old mutation routes, event production, consumers, subscriptions, webhooks, credentials, caches, replay, and recovery publishers to be inactive while retained representations and schemas remain resolvable as policy requires.

## Mechanisms, Invariants, or Proof Structure

Use the following gates to design and review metadata APIs and eventing.

**Intent gate.** Classify query, command, proposal, decision, snapshot, delta, event, and notification; state actor, authority, target, effect, response, retry, and audit.

**Identity gate.** Separate resource, representation, version, request, idempotency key, proposal, decision, event, delivery, correlation, causation, trace, subscription, and checkpoint identities.

**HTTP gate.** Align resource URI, method safety and idempotence, media type, negotiation, status, validator, precondition, link, cache, redirect, and authentication challenge.

**Mutation gate.** Define replacement, patch, domain operation, allowed fields, normalization, validation, expected version, atomicity, response, and compensation.

**Error gate.** Publish stable problem types, statuses, field codes, safe detail, retry guidance, trace, localization, redaction, and compatibility.

**Query gate.** Define field selection, filter, sort, cursor, snapshot, temporal axis, graph bounds, totals, authorization, cost, and partial results.

**Commit gate.** Atomically persist accepted state, decision, audit, idempotency outcome, and outbox; make dispatch replayable and observable.

**Envelope gate.** Specify event source, ID, type, subject, time, schema, content type, tenant, version, correlation, causation, trace, and integrity.

**Semantics gate.** Distinguish occurrence, notification, snapshot, delta, proposal, acceptance, deletion, deprecation, retirement, correction, and compensation.

**Delivery gate.** Declare channel, partition key, ordering, acknowledgement, retention, retry, redelivery, backpressure, poison handling, dead letter, and replay.

**Consumer gate.** Track supported schemas, inbox, checkpoint, per-entity version, gap, late event, atomic effect, external side effect, reset, and activation.

**Subscription gate.** Govern filter, start position, snapshot, resume, authorization recheck, destination proof, signature, secret rotation, overflow, disablement, and deletion.

**Compatibility gate.** Version API representations, errors, filters, cursors, links, event envelopes, data schemas, channels, bindings, retention, and consumer support.

**Protection gate.** Enforce tenant isolation, least privilege, field disclosure, secure cache, query privacy, event integrity, secret handling, rate limits, audit, and export policy.

**Operations gate.** Measure command outcomes, conflicts, outbox lag, publication, delivery, deduplication, rejection, dead letters, schema adoption, end-to-end freshness, and cost.

**Reconciliation gate.** Compare canonical versions, outbox, event history, broker positions, consumer checkpoints, projection digests, tombstones, and user-visible state; repair and verify.

**Recovery gate.** Restore identities, state, idempotency, proposals, decisions, audit, outbox, event archives, schemas, subscriptions, secrets, inboxes, checkpoints, and projections in safe order.

**Closure gate.** End writes, producers, consumers, routes, subscriptions, webhooks, credentials, caches, replay, and recovery while preserving required historical interpretation.

### Executable evidence: conditional mutations and idempotent delivery

This Python example applies five invented metadata mutation requests, records accepted changes in an in-memory outbox, and delivers those events at least once to two in-memory consumers.

<!-- bijux-verify: {"id":"conditional-mutations-and-idempotent-delivery","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"mutation_requests=5\napplied_mutations=2\nidempotent_replays=1\nversion_conflicts=1\npolicy_rejections=1\nfinal_version=5\noutbox_events=2\ndelivery_attempts=5\nconsumer_applications=4\nduplicate_deliveries=1\nconverged_consumers=2\n","stderr":""}} -->
```python
record = {
    "version": 3,
    "owner": "commerce",
    "description": "Order data",
}
outbox = []
idempotency = {}
counters = {"applied": 0, "replay": 0, "conflict": 0, "rejected": 0}

requests = [
    {
        "key": "request-a",
        "digest": "description-v4",
        "expected": 3,
        "patch": {"description": "Authoritative order data"},
    },
    {
        "key": "request-a",
        "digest": "description-v4",
        "expected": 3,
        "patch": {"description": "Authoritative order data"},
    },
    {
        "key": "request-b",
        "digest": "stale-owner",
        "expected": 3,
        "patch": {"owner": "analytics"},
    },
    {
        "key": "request-c",
        "digest": "forbidden-classification",
        "expected": 4,
        "patch": {"classification": "public"},
    },
    {
        "key": "request-d",
        "digest": "owner-v5",
        "expected": 4,
        "patch": {"owner": "commerce-data"},
    },
]

allowed_fields = {"owner", "description"}
for request in requests:
    stored = idempotency.get(request["key"])
    if stored is not None:
        assert stored["digest"] == request["digest"]
        counters["replay"] += 1
        continue
    if not set(request["patch"]) <= allowed_fields:
        counters["rejected"] += 1
        idempotency[request["key"]] = {"digest": request["digest"], "status": "rejected"}
        continue
    if request["expected"] != record["version"]:
        counters["conflict"] += 1
        idempotency[request["key"]] = {"digest": request["digest"], "status": "conflict"}
        continue

    previous = record["version"]
    record.update(request["patch"])
    record["version"] += 1
    event = {
        "id": f"event-{record['version']}",
        "previous": previous,
        "version": record["version"],
        "state": dict(record),
    }
    outbox.append(event)
    idempotency[request["key"]] = {
        "digest": request["digest"],
        "status": "applied",
        "version": record["version"],
    }
    counters["applied"] += 1

delivery_attempts = [
    ("search", outbox[0]),
    ("search", outbox[0]),
    ("audit", outbox[0]),
    ("search", outbox[1]),
    ("audit", outbox[1]),
]
consumers = {"search": {"version": 3}, "audit": {"version": 3}}
inboxes = {"search": set(), "audit": set()}
applications = 0
duplicates = 0

for consumer, event in delivery_attempts:
    if event["id"] in inboxes[consumer]:
        duplicates += 1
        continue
    assert consumers[consumer]["version"] == event["previous"]
    consumers[consumer] = dict(event["state"])
    inboxes[consumer].add(event["id"])
    applications += 1

print(f"mutation_requests={len(requests)}")
print(f"applied_mutations={counters['applied']}")
print(f"idempotent_replays={counters['replay']}")
print(f"version_conflicts={counters['conflict']}")
print(f"policy_rejections={counters['rejected']}")
print(f"final_version={record['version']}")
print(f"outbox_events={len(outbox)}")
print(f"delivery_attempts={len(delivery_attempts)}")
print(f"consumer_applications={applications}")
print(f"duplicate_deliveries={duplicates}")
print(f"converged_consumers={sum(value['version'] == record['version'] for value in consumers.values())}")
```

The expected output reports `mutation_requests=5`, `applied_mutations=2`, `idempotent_replays=1`, `version_conflicts=1`, `policy_rejections=1`, `final_version=5`, `outbox_events=2`, `delivery_attempts=5`, `consumer_applications=4`, `duplicate_deliveries=1`, and `converged_consumers=2` on separate lines.

The evidence is intentionally narrow. Dictionaries are not durable transactions. The key has no principal, tenant, operation, expiry, secure digest, concurrent access, or conflicting-digest path. A set membership check is not field-level authorization. Integer versions have one process as allocator. The outbox is not atomic with a database commit and is never dispatched through a broker. Event IDs, schemas, source, times, tenants, signatures, offsets, retries, gaps, dead letters, and external effects are absent. Delivery order is hand-selected, and inbox updates are not atomic with effects. Matching version integers proves only this toy projection, not authorized content equality or distributed convergence. Production assurance requires transactional failure injection, durable idempotency, conditional HTTP tests, schema and compatibility checks, partition and ordering tests, broker redelivery, consumer restart, poison events, reconciliation, security review, recovery, and end-to-end outcome evidence.

## Alternatives and Trade-Offs

**REST-style resource API.** Uniform HTTP semantics, caching, links, validators, and broad tooling work well for stable resources. Connected metadata can require multiple calls or carefully designed compound representations.

**GraphQL API.** Clients select connected fields and can evolve across one typed graph. Resolver authorization, query cost, caching, persisted queries, field deprecation, and error semantics are more complex.

**gRPC or typed RPC.** Strong code generation, streaming, deadlines, and efficient binary transport suit internal services. Browser and cache interoperability, ad hoc discovery, and public evolution can be less convenient.

**Bulk files.** Snapshot manifests scale for interchange and bootstrap. They introduce job lifecycle, object-store security, snapshot consistency, resume, expiration, schema, and event-overlap obligations.

**Complete replacement.** Clear state and idempotent intent make `PUT` attractive. Mixed field authority and large representations make accidental erasure likely.

**JSON Patch.** Precise ordered edits, tests, and null distinction support fine changes. Pointer authorization, arrays, concurrent structure, diagnostics, and operation complexity require care.

**JSON Merge Patch.** Compact object updates are easy for clients. Null-as-remove and whole-array replacement cannot express every metadata domain safely.

**Domain commands.** Intent, authority, evidence, and lifecycle transitions are explicit. More operations and client coupling need durable naming and compatibility governance.

**Synchronous validation and acceptance.** Callers get immediate results and simple workflows. Expensive review, federation, and long-running policy checks can cause timeouts and tight coupling.

**Asynchronous proposals.** Durable status supports human or distributed approval. Clients must poll or subscribe, proposals can expire, and accepted results need clear linkage.

**Polling current state.** Simple clients need no broker. It wastes requests, misses intermediate transitions, and creates latency and conditional-read complexity.

**Change events.** Consumers receive timely transitions and can build projections. Delivery, schema, ordering, replay, protection, and operations are substantial commitments.

**Notification events.** Small messages and fetch-time authorization minimize copied sensitive metadata. API availability, thundering fetch, immutable version retention, and collapsed history can hurt.

**State-transfer events.** Consumers rebuild independently and replay deterministically. Payload size, disclosure, schema evolution, duplication, and legal erasure costs increase.

**Delta events.** Efficient changes preserve transition detail. Consumers need exact prior versions, gap repair, patch semantics, and periodic snapshots.

**Snapshot events.** Application is simple and late consumers need less state. Large payloads, redundant transfer, and lost intermediate intent reduce efficiency and audit detail.

**Domain occurrence events.** Rich intent supports workflows and analytics. They may not reconstruct current state without a reducer and stable historical semantics.

**Transactional outbox.** It closes the commit-to-publish loss gap using local atomicity. Dispatch lag, duplicates, cleanup, ordering, and monitoring remain.

**Dual write to store and broker.** It looks simple and low latency. Partial failure inevitably creates state-without-event or event-without-state unless a coordinated transaction exists.

**Broker transactions.** They provide strong guarantees within supported resources. Cross-system effects, operational coupling, vendor semantics, and recovery can narrow usefulness.

**At-least-once delivery.** Durable retry reduces loss. Every consumer must deduplicate and make effects idempotent or compensatable.

**At-most-once delivery.** Low overhead avoids duplicate processing. Lost metadata lifecycle or policy events can leave projections permanently wrong.

**Compacted current-state topic.** New consumers bootstrap latest keyed state efficiently. Intermediate history, proposal evidence, ordering across keys, and tombstone retention need other stores.

**Immutable event log.** Audit and arbitrary replay are powerful. Retention, privacy, schema support, storage, redaction, and consumer reset become expensive.

**Broker subscriptions.** Durable offsets and scalable fan-out suit trusted systems. Network, identity, tenancy, and client operations can be heavy.

**Webhooks.** External consumers integrate using HTTP. Destination proof, SSRF, signatures, retries, secret rotation, rate limits, and replay require a delivery platform.

**GraphQL subscriptions or server-sent streams.** Interactive updates fit UIs. Long-lived connection scale and missing durable resume can make them unsuitable as authoritative change feeds.

**Offset pagination.** Familiar and supports random page numbers. Inserts and deletes cause skips and duplicates, while large offsets can be costly.

**Keyset cursor pagination.** Stable continuation and efficient indexes suit changing collections. Arbitrary jumps, backward navigation, mutable sort values, and token governance complicate clients.

**Public caches.** They reduce latency and server cost for genuinely public immutable metadata. Most enterprise metadata varies by authorization and lifecycle, making leakage risk high.

**Private revalidated caches.** They preserve viewer boundaries and reduce payload transfer. Key cardinality, invalidation, auth changes, and shared-client correctness still matter.

## Failure Modes and Misconceptions

**“HTTP is only transport.”** Method, validator, status, cache, link, and representation semantics directly affect correctness and interoperability.

**“GET can perform a small action.”** Crawlers, retries, prefetchers, and caches assume safe intent. Hidden mutation creates surprising effects.

**“PUT and POST are interchangeable.”** They communicate different resource and idempotency expectations even when both carry JSON.

**“An idempotency key makes every retry safe.”** Scope, digest, storage, expiry, concurrency, response, and external side effects must be defined.

**“Idempotency replaces version checks.”** It deduplicates one intent; it does not resolve two distinct concurrent intents.

**“A timestamp is a version.”** Clock skew, resolution, simultaneous writes, and reordered events make raw time insufficient as a concurrency token.

**“Last write wins is acceptable for metadata.”** It can erase reviewed ownership, classification, meaning, or lifecycle with a stale crawler or client.

**“PATCH means partial update.”** Media type defines patch semantics. JSON Patch and Merge Patch have materially different behavior.

**“Null always clears a field.”** In Merge Patch null removes; in a domain representation it might mean explicit unknown. Define both.

**“JSON Patch paths are already authorized.”** A syntactically valid pointer can target server-managed or hidden fields; resolve and authorize every operation.

**“A 200 response is enough.”** Creation, no-content, accepted async work, conflicts, preconditions, validation, rate limits, and absence need distinct semantics.

**“Error detail should show everything.”** Current protected values and topology can leak through validation and conflict diagnostics.

**“A proposal event means metadata changed.”** Only an accepted decision changes authoritative state unless the domain explicitly models otherwise.

**“An event is a command with past-tense naming.”** Events state occurrences and should not require one designated consumer to make them true.

**“Event ID is the entity ID.”** One entity experiences many events; one event can concern several entities.

**“Correlation ID deduplicates delivery.”** A workflow can contain many legitimate events sharing correlation. Use event identity.

**“A content hash is event identity.”** Repeated identical state can arise from distinct occurrences; signatures and provenance also require context.

**“Publishing after commit is reliable enough.”** A process crash in the gap loses an event unless an outbox or coordinated transaction closes it.

**“The outbox provides exactly once.”** Dispatch can duplicate after acknowledgement loss. Consumers still need inbox and effect semantics.

**“The broker preserves global order.”** Most guarantees are partition-scoped. Cross-key consumers need explicit causal or reconciliation logic.

**“Timestamps sort events safely.”** Clocks and network delay do not provide one authoritative sequence.

**“At-least-once means duplicates are harmless.”** Duplicate tickets, access changes, notifications, and counters can cause real harm without idempotent effects.

**“Exactly once is an end-to-end property.”** Guarantees apply only inside named systems, transactions, identifiers, and retention horizons.

**“Retry every error.”** Invalid schemas, forbidden fields, missing authority, and broken invariants will consume capacity until repaired.

**“A dead-letter queue solves poison events.”** It stores unresolved divergence and requires ownership, repair, replay, and reconciliation.

**“Current-state fetch repairs every event gap.”** It loses intermediate audit and can be unauthorized or unavailable; consumers need declared semantics.

**“Events can point to latest.”** Replay later may retrieve different state. Link immutable versions.

**“Optional event fields never break consumers.”** Strict decoders, signatures, size, semantics, and enum handling can still fail.

**“Schema compatibility proves consumer readiness.”** Generated code, filters, bindings, policy, deployment, and retained history require activation evidence.

**“Offset pagination is stable enough.”** Changing collections create duplicates and omissions even if the API is fast.

**“Opaque cursor means secure cursor.”** Unsigned encodings can be modified; even signed tokens can leak sensitive filters.

**“Total count is harmless.”** Counts can disclose hidden entities and be expensive or inconsistent.

**“GraphQL prevents over-fetching.”** Clients can request enormous nested graphs or trigger N+1 work without cost controls.

**“GraphQL field errors do not affect security.”** Partial responses and introspection can reveal protected schema and existence.

**“Subscriptions replace durable events.”** Disconnects and expired resume windows require snapshots and reconciliation.

**“Webhook HTTPS is sufficient authenticity.”** Receivers need source verification and replay protection; senders need destination proof and SSRF controls.

**“Signing the event encrypts it.”** Integrity and confidentiality are distinct.

**“Topic access protects every field.”** Broad events can reveal values beyond a subscriber's field authority.

**“Cache invalidation is only performance.”** Stale ownership, classification, lifecycle, or authorization can cause wrong actions and disclosure.

**“API logs are operationally harmless.”** Bodies, queries, filters, webhook URLs, errors, and headers can contain sensitive metadata and secrets.

**“Replay is just resetting an offset.”** External effects, schema support, inbox retention, authorization, and load make replay a governed operation.

**“Queue drained means consumers converged.”** Rejected, dead-lettered, skipped, unauthorized, or wrongly applied events can leave divergent state.

**“API and event models may evolve independently.”** They describe one domain; incompatible identity or lifecycle semantics create irreconcilable projections.

**“Low usage means safe retirement.”** Rare scheduled jobs, offline clients, replay, and recovery may be critical.

## Worked Examples

### Example 1

An editor retrieves asset version 12 with a strong ETag, changes the description, and submits a conditional domain command with an idempotency key. Another steward changed ownership first, so the stale request fails its precondition. The client retrieves version 13 and presents a field-aware merge; it does not blindly retry and erase the new owner.

### Example 2

A JSON Patch adds a glossary relation and uses `test` on the current lifecycle. The service resolves and authorizes each pointer, rejects a second operation targeting server-managed audit fields, applies nothing, and returns a stable problem type with safe paths. Sequential syntax does not weaken transaction atomicity.

### Example 3

A Merge Patch sets `description` and sends `support_contact: null`. The API contract defines null as removal for this media type and rejects use on an assertion resource where explicit unknown is meaningful. Clients negotiate the exact patch format instead of posting an unlabeled partial JSON object.

### Example 4

A term proposal returns `202 Accepted` with proposal identity and status link. Events `term.proposal-submitted` and later `term.assertion-accepted` have different types and event IDs connected by causation. Catalog projections consume only accepted changes; audit and workflow systems consume both.

### Example 5

The service commits asset version 21, decision evidence, idempotency outcome, and outbox event in one database transaction. The dispatcher publishes twice after losing an acknowledgement. Each consumer inbox deduplicates by source and event ID atomically with its projection, producing one effect while retaining both delivery attempts in telemetry.

### Example 6

A consumer sees entity transition 14-to-15, then 16-to-17. The prior-version mismatch reveals missing version 16. It pauses that entity, fetches immutable version 16 or replays the absent event, verifies the chain, and resumes. It does not apply version 17 over version 15 because the broker partition appears mostly ordered.

### Example 7

A search collection changes while a client pages. A cursor binds the authorized query, sort by modification time plus unique ID, snapshot token, last key, tenant, authorization epoch, and expiry. If privileges change, the cursor fails explicitly rather than continuing under its earlier visibility.

### Example 8

A GraphQL query requests an asset, fields, downstream lineage, owners, quality, and terms. Authorization runs at every resolver, traversal depth and list sizes are bounded, and the response marks paths incomplete under viewer permissions. A persisted query serves the common UI path while a separate bounded endpoint handles large asynchronous lineage export.

### Example 9

A webhook subscriber proves control of its endpoint, receives a secret, and verifies signed body, timestamp, event ID, and delivery ID. The sender blocks private-network destinations and unsafe redirects, retries transient failures with the same event identity, disables repeated permanent failures, and offers authenticated replay after repair.

### Example 10

A new search projection obtains a snapshot labeled at event offset 800, loads it idempotently, and consumes events beginning after 800. Shadow queries compare authorized results against the old projection. Migration records dead letters and digests; only after convergence does traffic shift, while rollback retains both the snapshot and event position.

## Cross-Program Connections

**API and Service Engineering.** Resource modeling, HTTP semantics, OpenAPI, GraphQL, concurrency, idempotency, errors, pagination, compatibility, authentication, rate limits, and lifecycle are core service-design concerns applied to metadata.

**Platform Engineering.** Metadata APIs and event streams become platform products with client libraries, paved integration paths, tenancy, quotas, SLOs, change management, support, incident response, and exit strategies.

**Data Engineering.** Brokers, CDC, snapshots, partitioning, checkpoints, late data, replay, stream processing, projections, and reconciliation determine whether metadata consumers see correct current and historical state.

**Distributed Systems Engineering.** Partial failure, atomic commit, outbox and inbox, ordering scope, duplicate delivery, conflict, causal identity, backpressure, and convergence are distributed-state problems.

**Software Engineering Patterns.** Command-query separation, optimistic concurrency, event sourcing, transactional outbox, idempotent consumer, saga compensation, materialized view, anti-corruption layer, and state machine provide reusable structures.

**Security Engineering.** Field authorization, cache variation, query privacy, webhook SSRF, signatures, replay protection, secret rotation, tenant isolation, audit, and schema supply chains define the protection surface.

**Programming Languages and Compilers.** JSON Pointer evaluation, patch interpretation, schema validation, generated clients, GraphQL type systems, event deserialization, unknown fields, and canonical signing bytes depend on precise language semantics.

**Site Reliability Engineering.** Command latency, outbox age, publish and consumer lag, retries, dead letters, projection freshness, subscription recovery, capacity, failover, and restore require separate indicators and error budgets.

**Governance, Risk, and Compliance.** Proposals, approvals, version evidence, event retention, audit, sensitive metadata, export, erasure, access decisions, and retirement need accountable policy and review.

**Testing and Quality Engineering.** Contract tests, state-machine models, fault injection, property tests, schema matrices, replay, differential projections, authorization cases, and reconciliation reveal guarantees that happy-path examples miss.

**Information Retrieval.** Search APIs require authorization-aware filtering, stable cursor pagination, facets, ranking fields, snapshots, and query privacy while metadata events update derived indexes.

**Systems Engineering.** APIs, databases, brokers, dispatchers, consumers, webhooks, schemas, caches, and human workflows form one system; local success metrics do not prove end-to-end convergence.

## References

1. IETF, [“RFC 9110: HTTP Semantics”](https://www.rfc-editor.org/rfc/rfc9110.html), 2022. Retrieved 2026-09-03.
2. IETF, [“RFC 9111: HTTP Caching”](https://www.rfc-editor.org/rfc/rfc9111.html), 2022. Retrieved 2026-09-03.
3. IETF, [“RFC 9457: Problem Details for HTTP APIs”](https://www.rfc-editor.org/rfc/rfc9457.html), 2023. Retrieved 2026-09-03.
4. IETF, [“RFC 6902: JavaScript Object Notation (JSON) Patch”](https://www.rfc-editor.org/rfc/rfc6902.html), 2013. Retrieved 2026-09-03.
5. IETF, [“RFC 7396: JSON Merge Patch”](https://www.rfc-editor.org/rfc/rfc7396.html), 2014. Retrieved 2026-09-03.
6. IETF, [“RFC 8288: Web Linking”](https://www.rfc-editor.org/rfc/rfc8288.html), 2017. Retrieved 2026-09-03.
7. OpenAPI Initiative, [“OpenAPI Specification 3.1.1”](https://spec.openapis.org/oas/v3.1.1.html), 2024. Retrieved 2026-09-03.
8. AsyncAPI Initiative, [“AsyncAPI Specification 3.0.0”](https://www.asyncapi.com/docs/reference/specification/v3.0.0), 2023. Retrieved 2026-09-03.
9. Cloud Native Computing Foundation, [“CloudEvents Specification 1.0.2”](https://github.com/cloudevents/spec/blob/ce@v1.0.2/cloudevents/spec.md), 2022. Retrieved 2026-09-03.
10. GraphQL Foundation, [“GraphQL Specification, October 2021 Edition”](https://spec.graphql.org/October2021/), 2021. Retrieved 2026-09-03.

## Exercises

### Exercise 1

Design HTTP and GraphQL interfaces for catalog resources, assertions, relationships, workflows, search, lineage traversal, versions, and bulk export. Specify identity, media types, methods, status, errors, authorization, ETags, idempotency, patching, pagination, cost, and audit.

### Exercise 2

Design an event contract for accepted metadata assertion, relation, lifecycle, quality, and schema changes. Specify envelope, types, subjects, data semantics, schemas, channels, partitioning, ordering, retention, replay, tombstones, and compatibility.

### Exercise 3

A service commits metadata to a database, publishes to a broker, updates search and graph projections, and invokes policy webhooks. Design outbox, inbox, retries, dead letters, backpressure, side-effect idempotency, checkpoints, observability, and reconciliation under failures.

### Exercise 4

Design a secure external metadata subscription platform using broker subscriptions, webhooks, and snapshot exports. Cover destination proof, authentication, signatures, encryption, filters, field authorization, tenancy, query privacy, quotas, resume, key rotation, incidents, and deletion.

### Exercise 5

An organization must replace metadata API v1 and event stream v1 while 900 clients, 150 consumers, retained events, generated SDKs, webhooks, offline exports, and disaster recovery depend on them. Design compatibility, dual operation, activation, rollback, migration, and retirement.

## Answers to the Exercises

### Answer 1

Give stable URIs and identities to resources, immutable versions, assertions, relations, proposals, decisions, jobs, and exports. `GET` retrieves authorized current or immutable representations with media type, field mask, strong validator, cache policy, typed links, and temporal semantics. Consequential writes require authenticated authority, idempotency key scoped to principal and operation, expected version or `If-Match`, layered validation, and audit. Use `PUT` only for complete client-owned replacements; JSON Patch for precise atomic operations with path authorization; Merge Patch only where null-as-remove and array replacement are valid; domain commands for claim, approve, certify, deprecate, and retire.

Return stable RFC 9457 problem types for parse, schema, field, authorization, precondition, conflict, transition, rate, and projection outcomes without leaking hidden values. Search filters an authorized corpus and uses opaque protected keyset cursors bound to query, sort, snapshot, tenant, auth epoch, and expiry. Totals disclose their accuracy and scope. Lineage traversal bounds types, direction, time, confidence, depth, fan-out, and cost and marks permission-limited results. Bulk exports are asynchronous resources with snapshot identity, manifest, digests, encryption, resume, expiry, and reconciliation.

GraphQL resolvers authorize fields and edges, batch source access, enforce depth and cost, cap lists, and use persisted operations for common paths. Mutations carry expected version and idempotency input and share the canonical command, decision, audit, and outbox implementation with HTTP. Version API schemas, null and omission, enums, error types, filters, sorting, links, cursor semantics, auth, and rate limits; test generated clients and model-based transitions.

### Answer 2

Use an envelope with specification version, unique `(source,id)`, durable event type, stable subject, occurrence time, data content type, immutable schema URI, tenant or authority, producer version, trace, correlation, and causation where allowed. Separate proposal-submitted, assertion-accepted, relationship-retired, resource-deprecated, resource-retired, quality-measured, schema-linked, and correction events. A duplicate resend retains source and ID; a correction is a new event linked causally.

Choose semantics explicitly: accepted changes can carry complete resulting assertion or resource state, or a delta naming exact previous and resulting versions. Notifications link immutable authorized versions, never `latest`. Tombstones identify retired subject, previous version, reason, replacement, authority, and retention. Register format and schema versions and test real consumers beyond structural compatibility. Preserve old schemas throughout event retention.

Document channels, send and receive operations, messages, security, bindings, partition key, acknowledgement, redelivery, retention, compaction, dead letter, and replay in AsyncAPI. Partition by stable subject when per-entity ordering matters. Carry version chain so gaps and stale arrivals are detectable; do not promise cross-subject total order. Bootstrap new consumers with a snapshot labeled at offset and then events after that position, using overlap and deduplication if atomic coordination is unavailable.

### Answer 3

In one local transaction persist canonical version, decision and audit, idempotency outcome, and outbox event. A dispatcher claims pending rows safely, publishes with stable event identity, records broker acknowledgement, and retries transient failures with jitter and budgets. State, search, graph, and policy consumers each keep inbox entries keyed by source and event ID atomically with local effects. External policy calls use a downstream idempotency key and record request and result so consumer restart does not repeat action blindly.

Partition by entity; carry previous and resulting versions. On gap, quarantine that entity and fetch immutable versions or replay rather than blocking unrelated partitions indefinitely. Classify errors: retry transport and rate conditions; route permanent schema, authorization, identity, and invariant failures to owned dead-letter workflow. Preserve original identity, source position, schema, consumer version, error, attempts, timestamps, and repair. Bound queues and concurrency; prioritize lifecycle and security without violating required order.

Measure accepted commands, conflicts, outbox age, publish attempts, broker acknowledgements, delivery, redelivery, inbox duplicate, application, reject, retry, dead-letter age, checkpoint, per-entity gap, search and graph projection lag, webhook outcomes, and end-to-end accepted-to-visible latency. Reconcile canonical versions and digests against outbox, event history, checkpoints, projection state, tombstones, and user-visible queries. Repair by targeted snapshot or replay, record repair, and verify policy effects. Inject crashes around every transaction and acknowledgement boundary and test restore and replay in isolation.

### Answer 4

Separate permission to discover a subscription, create it, select event types and fields, consume history, request replay, export snapshot, inspect failure, rotate secret, and delete. Bind every subscription to tenant, principal, purpose, filter, field disclosure profile, source position, expiry, and authorization epoch. Re-evaluate authorization on delivery and replay; do not rely only on topic or URL secrecy. Minimize and retain query and filter telemetry deliberately.

For brokers, use tenant-isolated identity, ACLs, quotas, schema registry, offsets, retention, and audit. For webhooks, prove endpoint control, allow safe HTTPS destinations, block private networks and unsafe DNS or redirects, sign canonical body plus timestamp and delivery identity, rotate overlapping secrets, bound clock and replay, and disable persistent failures. Receivers acknowledge quickly and process with inboxes. Encrypt sensitive event data or use small notification events that fetch immutable state under current authorization.

Snapshot exports use asynchronous jobs, immutable snapshot and event offset, manifest, schema and profile versions, object digests, encryption, short-lived access, expiry, resumable parts, counts, and deletion audit. Subscriptions support initial snapshot, cursor or offset, durable resume window, backpressure, overflow state, dead letters, and reconciliation. Incident response revokes credentials, disables destinations, preserves evidence, identifies delivered identities, rotates keys, corrects metadata, notifies affected parties, and verifies replay or deletion according to policy.

### Answer 5

Inventory every operation, URI, representation, media type, field, enum, null behavior, problem type, authentication flow, rate limit, cursor, link, SDK, GraphQL query, event source, type, subject, schema, channel, binding, partition, retention, consumer offset, webhook, export, and replay path. Map v1 to v2 semantics and identify changes that adapters cannot safely hide. Preserve stable resource identity and immutable historical version resolution.

Publish v2 OpenAPI and AsyncAPI contracts and compatibility fixtures. Shadow reads and compare viewer-authorized representations. Route all mutations through one canonical command authority that can serve both versions, preventing dual-write conflict. Emit one accepted internal change and derive v1 and v2 events with traceable mapping; compare projections. Provide generated SDKs, dual-schema consumer libraries, snapshot-at-offset bootstrap, and webhook test tools. Canary clients and consumers by consequence, record activation, observe unknown fields, conflicts, errors, lag, dead letters, and business outcomes, and retain routing rollback.

Deprecate with headers, schemas, documentation, dashboards, direct owner notices, replacement examples, and dates. Track authenticated use including rare scheduled and recovery clients. Freeze v1 writes, close proposals, migrate publishers, then consumers, replays, webhooks, and exports. Remove routes, topics, subscriptions, secrets, signing keys, caches, dispatchers, SDK publication, and recovery startup only after closure. Preserve v1 schemas, immutable representations, event archives, identity maps, audit, and a governed historical resolver for the retention horizon; restore-test that backups cannot restart v1 production.
