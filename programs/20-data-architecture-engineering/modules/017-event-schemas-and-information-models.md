---
module_id: DARCH-017
program: Data Architecture Engineering
level: 1
module_number: 17
title: Event Schemas and Information Models
status: complete
last_verified: 2026-09-03
---

# Event Schemas and Information Models

## One-Page Review

### Governing question

How can a team model, encode, evolve, publish, consume, retain, and replay events so that each record preserves what occurred, to which subject, when, under whose authority, with what evidence and causal context—without confusing delivery attempts, commands, snapshots, or schema-valid payloads with trustworthy domain facts?

### Essential definitions

- An **occurrence** is something that happens in a domain or system during an interval or at an instant.
- An **event record** is an immutable assertion describing an occurrence and its context; corrections create new records rather than silently rewriting the original assertion.
- An **event notification** informs consumers that an occurrence was asserted and may carry full data, a delta, a reference, or minimal routing information.
- An **event schema** specifies the structural representation, constraints, identifiers, types, and compatibility rules for a class of event records.
- An **information model** defines the concepts, identities, relationships, grain, time, provenance, authority, missingness, and rules that the schema represents.
- **Event identity** distinguishes one asserted occurrence record; **subject identity** identifies what the event concerns; delivery and processing-attempt identities distinguish transport work.
- **Occurrence time** is when the asserted occurrence happened; observed, recorded, published, ingested, and processed times describe later lifecycle moments.
- **Causation** links an event to the command, event, decision, or activity that produced it; **correlation** groups records for a declared analytical or workflow purpose.

### Central model, mechanism, or theorem

Represent an event contract as:

`E = (event_identity, event_type, subject, occurrence_time, source, authority, causation, payload, schema, provenance, controls, lifecycle)`

A trustworthy event contract binds semantic identity and grain to a versioned schema, defines every time and relationship, distinguishes producer from fact authority, and specifies duplicate, ordering, correction, retention, replay, compatibility, protection, and failure behavior. A broker can deliver a schema-valid message exactly once under a narrow mechanism while a consumer still applies the same business occurrence twice; transport guarantees do not replace semantic idempotency.

### Critical invariants

- Event type names a stable class of occurrence, not merely a topic, table operation, or implementation method.
- The pair or tuple defining event identity is unique within an explicit producer/source scope and remains stable across retries of the same notification.
- Subject identity, event identity, correlation identity, causation identity, trace identity, and delivery identity remain separate.
- Occurrence, observation, recording, publication, ingestion, and processing times are named and never collapsed silently.
- Every payload element maps to a governed concept, grain, authority, valid time, missingness rule, and protection purpose.
- Producers identify what they observed or decided and do not claim authority they do not possess.
- Ordering claims declare key, scope, clock or sequence authority, gaps, duplicates, reordering, and recovery behavior.
- Corrections, retractions, supersession, and late facts preserve lineage to prior assertions and do not mutate history invisibly.
- Writer-reader compatibility is tested semantically across exact schema versions; parsing alone is insufficient.
- Retention and replay preserve schemas, code/rule versions, identities, provenance, protection, side-effect policy, and reconciliation evidence.

### Common failures

Common failures are naming events in the present tense; publishing commands as facts; using database row changes as domain meaning; generating a new event ID on retry; treating broker offsets as event identity; using one timestamp called `created_at`; omitting subject or authority; placing mutable current state in a supposedly immutable historical record; sending only changed fields without absence semantics; assuming topic order is global; treating correlation as causation; relying on schema defaults that invent old facts; deleting or editing prior events to correct them; replaying into live side effects without fencing; logging sensitive payloads; and claiming compatibility because consumers deserialize successfully.

### Compact example

An order service emits `OrderUpdated` with a UUID, `created_at`, and the current order JSON. Retries mint new UUIDs, warehouse and payment consumers interpret omitted fields differently, and replay triggers duplicate refunds. The redesign emits bounded facts such as `OrderAccepted` and `OrderCancellationApproved`. Event identity is stable across delivery retries; order identity is separate. Occurred, recorded, and published times are explicit. Each event names producer, decision authority, schema version, causation, and prior assertion where corrected. Consumers store processed event identities, apply idempotent transitions, and fence external effects during replay.

### Connections

[DARCH-014](014-entities-relationships-and-business-keys.md) governs event and subject identity, [DARCH-015](015-shared-vocabulary-and-business-glossaries.md) governs event terminology, and [DARCH-016](016-canonical-models-and-their-trade-offs.md) evaluates shared exchange contracts. This module prepares [DARCH-018](../ROADMAP.md) on temporal and historical modeling and [DARCH-019](../ROADMAP.md) on model versioning.

## Governing Question

Events appear simple: a name, timestamp, and JSON object. The difficult part is deciding what the record asserts. Did an order actually become accepted, did a service request acceptance, did a database row change, or did a monitoring system observe a response? These are different occurrences, authorities, and consequences even if all carry `order_id` and `status`.

An event schema must sit on an information model. Field types cannot tell a consumer whether `time` means occurrence or ingestion, whether `customer_id` identifies a person or account, whether absence means unchanged or unknown, whether a producer is authoritative, or whether a correction replaces an earlier assertion. Without those semantics, syntactic interoperability accelerates inconsistent decisions.

The governing question spans the complete lifecycle: creation, validation, publication, transport, duplication, ordering, consumption, storage, correction, evolution, replay, protection, and retirement. Each stage can preserve or corrupt meaning. Durable event architecture makes the boundaries explicit and testable.

## Why This Matters

Events decouple producers and consumers in time and deployment. They support integration, audit, automation, state reconstruction, analytics, observability, and responsive workflows. They also persist mistakes. An ambiguous event copied to dozens of consumers becomes a long-lived semantic contract that is difficult to recall.

The [CloudEvents specification](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md) defines a vendor-neutral event envelope with required context such as `id`, `source`, `specversion`, and `type`, plus optional subject, time, data schema, content type, and extensions. Its source-plus-ID rule helps consumers recognize duplicate delivery of the same event. The envelope deliberately does not define every domain payload or processing rule.

The [AsyncAPI 3.0.0 specification](https://www.asyncapi.com/docs/reference/specification/v3.0.0) describes message-driven APIs, channels, operations, messages, payload schemas, correlation identifiers, bindings, traits, and examples. It can document a contract, but correct documentation depends on the underlying event semantics and actual runtime behavior.

Event histories also create governance obligations. A false assertion can outlive source correction; a schema default can rewrite the apparent past; a replay can repeat payments or notifications; identifiers and payloads can enable broad correlation; retention can conflict with deletion and legal-hold duties. These are information-architecture decisions, not broker configuration details.

## Prerequisites and Retrieval

You should understand domain modeling, schemas, APIs, messages, distributed systems, clocks, queues and logs, delivery guarantees, idempotency, compatibility, provenance, security, privacy, observability, retention, and recovery.

Retrieve occurrence, event, event record, notification, command, fact, state, snapshot, delta, envelope, payload, event type, subject, source, authority, event identity, correlation, causation, trace, occurrence time, observed time, recorded time, published time, ingested time, processed time, sequence, partition, offset, duplicate, retry, idempotency, correction, retraction, supersession, replay, backfill, and reconciliation.

As a retrieval test, inspect `{"type":"customer.updated","id":"9","time":"2026-09-03T10:00:00Z"}`. Ask which occurrence is asserted, which customer concept and identifier scheme apply, who produced and authorized it, what changed, whether omitted fields are unchanged or unknown, which time is encoded, which schema version governs it, what caused it, whether ID 9 is source-qualified, and how retries, corrections, and replay behave. The JSON is valid but semantically incomplete.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish occurrences, event records, notifications, commands, state snapshots, change records, logs, and processing attempts;
2. define event type, semantic grain, subject identity, source, authority, causation, correlation, and provenance;
3. model occurrence, observation, recording, publication, ingestion, and processing time without conflation;
4. design envelopes and payloads with explicit schemas, content types, versions, extensions, and protection metadata;
5. choose among full-state, delta, reference, and decision-event payloads with clear absence and authority semantics;
6. specify duplicate, retry, idempotency, ordering, partition, gap, late-arrival, and concurrency behavior;
7. model corrections, retractions, supersession, compensation, and disputed assertions without rewriting history;
8. evaluate writer-reader compatibility, defaults, aliases, enums, unknown fields, and semantic change across versions;
9. plan retention, archive, replay, backfill, side-effect fencing, recovery, deletion, and reconciliation;
10. verify event contracts through structural, semantic, producer-consumer, temporal, failure, protection, and lifecycle evidence.

## Core Exposition

**Start with the occurrence.** Name event types in past tense when they assert completed facts: `OrderAccepted`, `PaymentCaptured`, `ShipmentDispatched`. Past tense does not itself guarantee truth, but it prompts the right question: what occurred? `UpdateCustomer` is a command; `CustomerUpdated` may still be too broad; `customer-table-row-changed` is a technical change fact rather than a domain decision.

Write inclusion and exclusion criteria. `PaymentCaptured` may mean an authorized payment provider confirmed settlement capture, not that a UI received a click, a database status field changed, or money reached a bank account. Record the governing workflow state, authority, and counterexamples.

One real-world occurrence can produce several event records for different purposes. A database write, domain transition, audit assertion, and telemetry record may all describe aspects of one activity. Give each record its own type and identity, then link them through causation or trace context. Do not assume they are interchangeable.

**Separate event, notification, and message.** An occurrence happens in the domain. An event record asserts information about it. A notification communicates that assertion. A message is a transport unit that can contain an event, command, reply, or batch. One event notification may be delivered many times and wrapped in different messages.

This distinction clarifies identity. Retrying the same event notification preserves event identity while creating another delivery attempt. Re-emitting a corrected assertion creates a new event identity linked to the earlier event. Copying the event to another transport does not create a new business occurrence.

**Define semantic grain.** State exactly what one event instance represents. `InventoryAdjusted` might represent one item-location adjustment, one counted batch, one reconciliation decision, or one transaction affecting many positions. Grain determines keys, payload cardinality, ordering, and idempotency.

Avoid event types that combine unrelated occurrences. `CustomerAndOrderUpdated` makes authority, retry, partial failure, and evolution difficult. An atomic business decision can include several related facts when its invariant requires them, but state the transaction boundary and whole-event meaning.

**Layer the contract.** Separate domain information model, event context/envelope, payload schema, serialization format, protocol binding, channel configuration, and processing policy. The same event model can be encoded as JSON or Avro and transported by HTTP or a log. Changes in one layer need not redefine all others, but exact version combinations belong in evidence.

CloudEvents illustrates an abstract event context with format and protocol bindings. Use such an envelope to standardize routing metadata without pretending it defines payload meaning. Domain fields still require glossary concepts, identities, constraints, units, time, provenance, and authority.

**Define event type identity.** Use a stable, namespaced type identifier independent of a topic or class name. Record owner, definition, versioning policy, subject kind, authority, schema references, allowed extensions, lifecycle, and examples. A topic can carry several event types; one type can appear on several channels.

Renaming code should not silently rename the event contract. Do not reuse a retired type name for a different occurrence. If semantic meaning breaks, create a new type or major version and plan coexistence. A type registry should preserve historical definitions.

**Distinguish identities.** Event identity recognizes the same asserted occurrence record across duplicate deliveries. Subject identity identifies the entity concerned. Command identity identifies a request. Correlation identity groups related messages for a declared purpose. Causation identity points to the direct trigger. Trace and span identities represent distributed execution. Delivery identity and broker offset identify transport work.

Do not overload `id`. Qualify event identity by source when the scheme requires it. CloudEvents specifies uniqueness for the combination of source and ID and allows a duplicate resend to retain the same ID. Consumers still need retention and scope for deduplication; they cannot remember every identifier forever without policy.

An event may concern multiple subjects, but declare a primary subject for routing if the envelope supports one and represent other roles in the payload. Subject identifiers need scheme, issuer, namespace, validity, and type. A UUID distinguishes records but does not resolve real-world identity.

**Separate producer, source, and authority.** The process publishing a message may not own the fact. A change-data-capture connector produces an event from a database, while a payment provider is the external authority for capture state and the application is authority for its decision to fulfill. Record observation chain and responsible authority.

Use provenance to distinguish asserted, observed, inferred, enriched, and copied information. A consumer should know whether a value came directly from the authoritative decision, from a projection, or from a later lookup. Preserve conflicts where no approved resolution exists.

The W3C [PROV-O Recommendation](https://www.w3.org/TR/prov-o/) offers entity, activity, agent, generation, usage, derivation, attribution, and related provenance constructs. It can inform event lineage, while local domain rules still determine what counts as authoritative evidence.

**Model time explicitly.** Occurrence time answers when the event happened according to the domain or source clock. Observed time answers when an observer detected it. Recorded time answers when the assertion was registered. Published and ingested times describe movement. Processed time belongs to a consumer attempt. These can differ substantially.

OpenTelemetry's [Logs Data Model](https://opentelemetry.io/docs/specs/otel/logs/data-model/) distinguishes event timestamp from observed timestamp and includes trace context and resource/instrumentation information. That distinction is broadly useful even when the event is not telemetry.

Record clock authority, precision, time zone or offset, uncertainty, and interval semantics. RFC 3339 defines an [Internet timestamp profile](https://www.rfc-editor.org/rfc/rfc3339.html), not the truth of the clock or the meaning of a timestamp. A formatted instant can still be wrong, estimated, or semantically misnamed.

Do not use ingestion time as occurrence time merely because it is available. Late and offline producers, network partitions, batch imports, and corrections make them diverge. Event-time analytics need watermarks, lateness policies, retractions, and recomputation; operational workflows may need both.

**Represent causality carefully.** A direct cause is not the same as a shared correlation. A command may cause one decision event, which causes several downstream events. A business process ID can correlate all of them without proving causal order. Record relationship type and direction.

W3C [Trace Context](https://www.w3.org/TR/trace-context/) standardizes trace identifiers and propagation fields for distributed tracing. Trace topology is execution evidence, not automatically domain causation. Retries, asynchronous work, sampling, and batch processing can separate them.

Use causation chains to diagnose loops and support idempotency, but prevent unbounded headers. Store durable lineage separately where necessary. Security review should treat trace and correlation IDs as linkable identifiers.

**Choose payload style from consumer needs.** A full-state event carries a snapshot at a declared time and version. It simplifies independent reads but can be large, expose excess data, and overwrite concurrent facts if treated as authoritative wholesale. A delta event carries changes; it is compact but needs precise before/after, absence, ordering, and baseline semantics.

A notification with a resource reference minimizes duplication but couples consumers to source availability, authorization, and current state. By fetch time, the resource may differ from the occurrence. A decision event carries facts sufficient for a specific consequence and can be more stable than a generic entity update.

Hybrid designs carry stable identifiers, material decision facts, provenance, and optional reference. State whether payload values reflect occurrence time, publication time, or current lookup. Do not label a full state “event sourcing” merely because it travels through a broker.

**Define absence and change.** In a patch, omitted can mean unchanged, unknown, redacted, unsupported, or cleared. Null can mean an explicit new absence or a missing value. Create an operation or variant that distinguishes set, clear, unchanged, unknown, and prohibited where consequences require it.

For full snapshots, declare completeness: all current fields, all fields visible to this purpose, or a partial projection. Include projection/profile identity. Consumers must not delete local data merely because a minimized field is absent.

**Bind schemas exactly.** Identify schema language, artifact URI or digest, name, namespace, version, profile, and content type. A human-friendly version string can coexist with a content digest. Consumers need deterministic retrieval or bundled artifacts for archive and replay.

JSON Schema [Draft 2020-12](https://json-schema.org/draft/2020-12) provides structural and validation vocabularies for JSON instances. Apache Avro's [1.12.0 specification](https://avro.apache.org/docs/1.12.0/specification/) defines schemas, encoding, defaults, aliases, and writer-reader resolution. Their mechanisms differ; neither encodes complete business meaning by itself.

Store the writer schema with or resolvable from retained data. Pin validators and code generators. A mutable registry entry called `latest` makes historical replay non-reproducible. Sign or checksum governed artifacts where integrity matters.

**Treat schema defaults cautiously.** In reader-writer systems, a default can provide a value when old data lacks a new field. That improves structural readability but does not prove the old producer asserted the value. If the field changes price, rights, jurisdiction, routing, risk, or identity, use explicit unknown or evidence-backed migration.

Avro defaults are used in schema resolution when a reader has a field absent from the writer; they do not mean writers may omit arbitrary required values at encoding. Document the exact mechanism rather than transferring assumptions from another schema language.

**Design enums and open sets.** Closed enums catch unexpected values but can break future producers and cause consumers to map unknown members to dangerous defaults. Open strings support evolution but weaken validation. A union of known value plus explicit unknown representation can preserve safety.

Bind codes to system, version, authority, validity, and display. Never reuse codes with new meanings. Consumer behavior for unknown, deprecated, or unmapped codes must be explicit: preserve, quarantine, ignore for a bounded use, or reject.

**Plan compatibility semantically.** Backward compatibility asks whether new readers can process old writer data; forward compatibility asks whether old readers can process new writer data. Full compatibility combines directions under exact rules. Transitive policies extend comparisons across more than adjacent versions.

Parsing is only structural compatibility. Renaming a field through an alias can preserve values while changing meaning. Adding an optional field can change signatures, validation, generated code, exhaustive matching, or decisions. Relaxing a constraint can send values old consumers never handled.

Maintain a producer-consumer matrix of schema versions, profiles, operations, code lists, and behavioral assumptions. Test old/new pairs with positive, negative, boundary, unknown, and protected fixtures. Record which consumers may ignore which additions.

**Define ordering scope.** Total global order is expensive and often unnecessary. Partition ordering applies only within a partition and under transport guarantees. Business order may depend on per-subject sequence, source sequence, occurrence time, or causal predecessor.

Declare ordering key, sequence issuer, start, gaps, duplicates, wrap or reset, concurrency, partition changes, clock behavior, and recovery. Sequence number 7 from two producers is not comparable without a common authority. Broker offsets are physical positions, not portable domain sequence.

Consumers should handle late, duplicate, and out-of-order events according to state-machine rules. Buffering has limits. Some operations commute; others require version checks, conflict resolution, or manual review. Do not sort by timestamp and assume causality when clocks are independent.

**Design idempotency around effects.** Deduplicating by event identity prevents repeated application of the same record within the deduplication horizon. It does not prevent two distinct events from asserting the same business effect. Use business operation keys or state preconditions when needed.

Store the identity and outcome atomically with consumer state where possible. Define retention longer than maximum retry and replay windows. On expiration, duplicates can reappear. External effects such as payments, emails, and device commands need downstream idempotency keys and reconciliation.

“Exactly once” must name scope: broker write, transactional read-process-write, state store, or end-to-end business effect. Network uncertainty means a caller may not know whether an external effect happened. Design query, retry, and compensation protocols.

**Model corrections and retractions.** An immutable event record can contain a false assertion. Correct it with a new event identifying the target assertion, correction type, changed facts, reason, authority, effective time, recorded time, and evidence. Preserve both records and compute the accepted view under versioned rules.

A retraction says the prior assertion should not be used under stated scope; it does not erase that it was published. Supersession replaces one assertion with another. Compensation creates a new domain action to counter consequences; it is not historical correction. Distinguish all three.

Consumers need correction policy. Some projections can recompute; external emails cannot be unsent; payments may require refunds; safety decisions may need notification and human review. Track propagation and unresolved consequences.

**Handle transaction boundaries.** The outbox pattern can atomically record a domain state change and publication intent within one local transaction, reducing lost-message gaps. Change data capture can transport committed changes. Neither proves that the emitted event has good domain semantics.

Define when an event becomes authoritative: at local commit, external confirmation, quorum, or later adjudication. If several aggregates must change atomically, document the actual consistency boundary. A saga yields several events and compensations, not one hidden global transaction.

Publication can fail after commit. Dispatch retries must retain event identity and payload or governed equivalent. Monitor stuck outbox records, duplicate sends, ordering, and poison payloads. Recovery needs the schema and rule versions used at creation.

**Separate domain events from change events.** A domain event expresses a meaningful occurrence. A change event expresses insert, update, delete, or field difference in a data store. Change events are useful for replication and integration when consumers need source fidelity, but table structure and transaction order become contracts.

Do not rename every row update into a business fact. A status column can change due to correction, backfill, migration, or domain transition. Enriching CDC with semantics requires evidence and transaction context. Preserve source lineage and distinguish inferred events.

**Specify channels without embedding meaning in them.** Topic or routing-key names help distribution but are operational resources with partitions, retention, access, and versions. Event type belongs in the record contract. Consumers should validate allowed type-channel combinations without treating a topic name as sole proof.

Define producer and consumer ownership, delivery mode, partition key, ordering, retention, compaction, maximum size, batching, compression, dead-letter handling, retry, backpressure, quotas, encryption, and recovery. AsyncAPI can document channels and operations, but deployed configuration must be checked for drift.

**Govern dead letters and quarantine.** Invalid, unauthorized, unrecognized, or repeatedly failing events need distinguishable handling. A dead-letter queue can become an unprotected data lake. Apply access, encryption, retention, deletion, redaction, capacity, alerting, replay approval, and evidence.

Do not endlessly retry deterministic schema failures. Classify transient transport, dependency, data, authorization, version, and code defects. Preserve original bytes and metadata when authorized, error evidence, attempts, and remediation decision. Reprocessing should be idempotent.

**Protect event data.** Events replicate widely and persist. Minimize payload to declared consumers and purposes. Apply classification, tenancy, consent or legal basis where applicable, authorization, encryption, signing, integrity, residency, retention, deletion, subject access, and incident response.

Metadata can be sensitive: subjects, types, sources, trace IDs, and timestamps reveal activity. Avoid personal identifiers in topic names and partition keys where unnecessary. Logs, metrics, traces, schema examples, dead letters, test fixtures, replays, and backups need the same protection analysis.

Deletion in an append-only history requires a governed strategy: encryption-key destruction, tombstones, redaction projections, retention expiry, or segregated payload stores may help under specific requirements. No technical pattern alone establishes legal adequacy.

**Design authenticity and integrity.** Transport authentication identifies a connection, not necessarily the original producer after relays. Record producer identity and trust boundary. Use signatures, authenticated metadata, checksums, or secure channels according to threat model, including key rotation and replay protection.

Do not sign a serialization that intermediaries legitimately rewrite without defining canonical bytes or detached claims. Bind critical context and payload together. Verify algorithm, key, issuer, audience, time, revocation, and failure behavior. Valid signatures prove key use, not factual truth.

**Plan retention and compaction.** Retention should consider business history, replay, audit, debugging, privacy, legal holds, cost, schema availability, and source recovery. Broker retention and authoritative archive retention can differ. Document the system of record for events.

Log compaction may retain only the latest value per key, which is a state reconstruction mechanism, not full event history. Tombstones and delete semantics need exact platform behavior. If audit needs every assertion, preserve an uncompacted authorized archive.

**Engineer replay as a controlled operation.** Define source interval, event types, schema/rule versions, target consumers, ordering, speed, deduplication, side-effect fencing, checkpoints, observability, authorization, rollback, and reconciliation. Mark replay context separately without changing original event identity.

Consumers should distinguish rebuilding a projection from repeating external effects. Use shadow outputs, dry runs, isolated topics, transactional swaps, or explicit replay modes. Test with corrected, late, duplicate, unknown-version, and poison events.

Reproducibility requires original data and exact reducer code, dependencies, mappings, reference-data versions, and configuration. If current rules intentionally reinterpret history, label it as a new projection rather than claiming identical replay.

**Support backfill without forging history.** A backfilled event derived from historical rows was recorded now about an earlier occurrence. Preserve occurrence time if evidenced, plus derivation, recorded/published time, source snapshot, method version, confidence, and limitations. Do not imply it was emitted at occurrence time.

Backfills can collide with live events. Define cut line, overlap, deduplication, sequence, late-arrival handling, and authority. Validate counts, identities, invariants, sampled semantics, and consumer outcomes. Aggregate equality alone does not prove event correspondence.

**Observe semantic health.** Measure publication latency by named time points, duplicate rate, out-of-order rate by scope, invalid schemas, unknown types and codes, mapping loss, consumer lag, dead letters, correction rate, replay divergence, dedup store misses, and unprocessed versions.

Metrics need denominators and windows. Zero dead letters can mean perfect data or disabled validation. Low correction rate can mean accurate facts or absent feedback. Combine telemetry with audits, consumer reports, incident analysis, and source reconciliation.

**Govern the lifecycle.** Maintain event type registry, schema and profile artifacts, owners, producers and consumers, channels, keys, authorities, mappings, examples, compatibility matrix, retention, controls, reviews, and deprecation state. Discover runtime drift.

Change approval should include domain, consumer, operations, security, privacy, records, and compliance expertise proportional to consequence. Emergency fixes still need recorded authority and follow-up evidence. Retire only after producers stop, lag and archives are addressed, consumers acknowledge exit, replays are migrated, and protected copies are handled.

## Definitions and Notation

Let an event contract be:

`E = (I, T, S, O, R, A, C, P, H, V, G, L)`

where `I` is event identity, `T` event type, `S` subject identities and roles, `O` occurrence time, `R` source and recording context, `A` assertion authority, `C` causation/correlation, `P` payload and provenance, `H` schema/encoding/binding, `V` validation and compatibility evidence, `G` delivery/processing/protection controls, and `L` correction, retention, replay, and lifecycle.

For source `s` and event identifier `i`, define deduplication identity `d = (s, i)` when the contract gives that tuple uniqueness. A retry of the same notification preserves `d`; a corrected assertion receives new `d2` and relates to `d` by an explicit correction or supersession relation.

Let named times be `t_occ`, `t_obs`, `t_rec`, `t_pub`, `t_ing`, and `t_proc`. A normal pipeline may observe `t_occ <= t_obs <= t_rec <= t_pub <= t_ing <= t_proc`, but clocks, estimates, batching, imports, and corrections can violate apparent timestamp order. Record clock authority and uncertainty rather than assuming the inequality.

For consumer state transition `F(state, event)`, semantic idempotency for duplicate event `e` requires `F(F(s,e),e) = F(s,e)` for the declared effect scope. This property can be achieved by event-identity deduplication or naturally idempotent state logic; it does not automatically include external effects outside that state.

## Mechanisms, Invariants, or Proof Structure

Use ten gates to design and assure event contracts.

**1. Occurrence gate.** Define event type, semantic grain, inclusion, exclusion, subject, decision consequence, and counterexamples.

**2. Identity and authority gate.** Separate event, subject, command, causation, correlation, trace, delivery, and processing identities; name source and fact authority.

**3. Time and provenance gate.** Define occurrence, observation, recording, publication, ingestion, processing, clocks, uncertainty, derivation, and evidence.

**4. Information-model gate.** Specify concepts, relationships, keys, units, states, missingness, cardinality, valid time, and constraints before serialization.

**5. Schema and envelope gate.** Bind type, schema/profile versions, content type, format, protocol, extensions, codes, defaults, examples, and artifact integrity.

**6. Delivery and ordering gate.** Define retries, duplicates, idempotency, partitions, sequences, gaps, concurrency, late data, errors, dead letters, and backpressure.

**7. Evolution gate.** Test writer-reader pairs, unknowns, aliases, enums, semantic changes, coexistence, migration, rollback, correction, and supersession.

**8. Protection gate.** Apply minimization, purpose, authentication, authorization, integrity, confidentiality, residency, retention, deletion, audit, and incident controls.

**9. Replay and recovery gate.** Preserve original identities and artifacts, fence effects, control backfill, checkpoint, reconcile, restore, and retain historical interpretation.

**10. Outcome and lifecycle gate.** Monitor semantic health, drift, consumers, incidents, correction propagation, cost, deprecation, and verified retirement.

The executable example checks four narrow event-registry failures: missing occurrence time, missing schema version, retry identity instability, and missing fact authority.

<!-- bijux-verify: {"id":"event-contract-integrity","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"events=4\nvalid=0\nfindings=customer-updated:missing-schema-version,inventory-adjusted:unstable-retry-identity,order-cancelled:missing-authority,payment-captured:missing-occurrence-time\nready=false\n","stderr":""}} -->
```python
events = (
    {"id": "payment-captured", "occurrence_time": "", "schema_version": "2", "stable_retry_id": True, "authority": "payment-provider"},
    {"id": "customer-updated", "occurrence_time": "2026-09-03T10:00:00Z", "schema_version": "", "stable_retry_id": True, "authority": "customer-service"},
    {"id": "inventory-adjusted", "occurrence_time": "2026-09-03T10:01:00Z", "schema_version": "3", "stable_retry_id": False, "authority": "inventory-ledger"},
    {"id": "order-cancelled", "occurrence_time": "2026-09-03T10:02:00Z", "schema_version": "4", "stable_retry_id": True, "authority": ""},
)

findings = []
valid = 0
for event in events:
    local = []
    if not event["occurrence_time"]:
        local.append("missing-occurrence-time")
    if not event["schema_version"]:
        local.append("missing-schema-version")
    if not event["stable_retry_id"]:
        local.append("unstable-retry-identity")
    if not event["authority"]:
        local.append("missing-authority")
    if local:
        findings.extend(f"{event['id']}:{finding}" for finding in local)
    else:
        valid += 1

print(f"events={len(events)}")
print(f"valid={valid}")
print("findings=" + ",".join(sorted(findings)))
print(f"ready={str(valid == len(events)).lower()}")
```

The checker validates four declared registry predicates only. It does not prove that occurrences happened, subjects resolve, clocks are correct, producers are authoritative, schemas preserve meaning, delivery is ordered, processing is idempotent, protection is adequate, replay is safe, or consumers are compatible. Those require domain authority, representative fixtures, implementation evidence, failure exercises, and accountable review.

## Alternatives and Trade-Offs

**Fact event versus command.** Facts support independent reaction and history; commands request a specific action and allow rejection. Naming a command as a fact hides decision authority. Many workflows legitimately use both with causation links.

**Domain event versus change event.** Domain events preserve business meaning and stability but require deliberate production. Change events preserve source mutations and can be generated automatically but couple consumers to storage and need interpretation.

**Full state versus delta.** Full state simplifies independent consumption and recovery but increases size, exposure, and overwrite risk. Deltas minimize transfer but require baseline, ordering, absence, and correction semantics.

**Embedded data versus reference.** Embedded facts preserve occurrence-time context and source independence. References reduce duplication but couple consumers to current source availability and authorization. Hybrid payloads can carry decision facts plus links.

**Closed enum versus open code.** Closed enums validate known values but impede evolution. Open codes preserve future values but require runtime handling. Versioned code systems with explicit unknown behavior balance them.

**Central schema registry versus bundled schemas.** A registry improves discovery and policy but adds availability and mutation risk. Bundled artifacts aid replay and autonomy but can drift. Immutable digests and synchronized caches support both.

**Global order versus scoped order.** Global order simplifies some reasoning but reduces availability and scale. Per-subject or partition order is cheaper but requires concurrency and cross-key conflict handling.

**Long retention versus minimized history.** Long histories support audit and replay but raise cost, exposure, deletion, and version-preservation burdens. Retain only what authorized purposes require and verify recovery separately.

## Failure Modes and Misconceptions

1. **Every message is an event.** Messages can contain commands, replies, documents, events, or batches.
2. **Past-tense naming proves a fact.** Semantics and authority, not grammar, establish the assertion.
3. **A database update is a domain event.** It may be migration, correction, backfill, or implementation detail.
4. **One `id` field covers all identity.** Event, subject, command, correlation, cause, trace, delivery, and attempt identities differ.
5. **One timestamp is enough.** Occurrence, observation, recording, publication, ingestion, and processing support different questions.
6. **Correlation proves causation.** Grouping does not establish direct cause or temporal order.
7. **Schema-valid means true.** Structural conformance cannot prove occurrence, authority, or semantic correctness.
8. **Defaults make old events complete.** Reader substitutions may invent facts absent from old assertions.
9. **Topic order is global business order.** Ordering depends on partition, producer, key, sequence, clock, and recovery.
10. **Exactly once prevents duplicate effects.** Guarantees are scoped; external side effects and distinct duplicate facts still need controls.
11. **Immutable means never corrected.** Corrections and retractions should append governed assertions rather than rewrite history.
12. **Event sourcing means keeping messages.** Reconstruction requires authoritative events, exact reducers, versions, ordering, and replay evidence.
13. **A reference is equivalent to embedded state.** Later retrieval can return changed or unavailable information.
14. **Dead letters are harmless diagnostics.** They can accumulate sensitive payloads and unresolved business consequences.
15. **Replay is just republishing.** It requires authorization, side-effect fencing, version control, checkpoints, and reconciliation.

## Worked Examples

### Example 1

A UI emits `OrderPlaced` before the order service validates inventory and terms. The record is renamed `OrderPlacementRequested`; the authoritative service later emits `OrderAccepted` or `OrderRejected`, linked by command and causation identity.

### Example 2

A publisher generates a new UUID after every timeout. One captured payment arrives three times with three event IDs and causes duplicate fulfillment. Publication retries now preserve source-plus-event ID, and fulfillment also guards the business transition atomically.

### Example 3

An event has `created_at` from the broker. A mobile device was offline for two days, so analytics assigns activity to the wrong period. The schema adds source occurrence time with clock quality plus observed, recorded, published, and ingested times.

### Example 4

`CustomerUpdated` omits `phone`. One consumer interprets unchanged; another deletes it. The contract replaces ambiguous partial objects with operations for set, clear, and unchanged, plus explicit unknown/redacted states and a profile identifier.

### Example 5

An Avro reader default supplies `country = "US"` for old events. Old Canadian orders become taxable in the wrong jurisdiction. The new reader preserves unknown, and an evidence-backed enrichment process emits derived assertions with source and rule version.

### Example 6

Inventory events are ordered within product partitions, but a repartition changes keys. Consumers receive sequence 51 before 50. The contract defines per-position authoritative version checks, gap detection, snapshot recovery, and conflict quarantine rather than timestamp sorting.

### Example 7

A customer deletion request removes the operational row, but event payloads, dead letters, replay archives, and schema examples retain identifiers. The lifecycle inventory applies authorized redaction or deletion strategy to every copy and preserves only permitted audit evidence.

### Example 8

A false `ShipmentDelivered` event triggered billing. A retraction alone cannot undo the invoice. The carrier issues a correction; billing records a compensating credit, customer support receives a notification, projections recompute, and propagation status remains auditable.

### Example 9

A replay rebuilds a search index but also sends millions of customer emails. Consumers introduce explicit rebuild mode, shadow output, external-effect fencing, event-ID checkpoints, rate limits, and reconciliation before production replay approval.

### Example 10

A CDC stream labels every status update `AccountClosed`. Backfills and typo corrections look like closures. The design preserves raw change events for replication and emits `AccountClosureApproved` only from the governed workflow with authority, cause, and effective time.

## Cross-Program Connections

- **API and service engineering:** asynchronous APIs, commands, events, contracts, idempotency, versioning, gateways, and consumer tests expose event semantics.
- **Data engineering:** streams, watermarks, windows, late data, CDC, event sourcing, replay, backfill, lineage, and lakehouse histories consume event contracts.
- **Platform engineering:** brokers, registries, generators, policy, observability, dead-letter handling, encryption, retention, and replay tooling enforce controls.
- **Database engineering:** transactions, outboxes, logs, keys, temporal tables, constraints, and projections connect state changes to publication.
- **Distributed systems:** clocks, ordering, consensus, partitions, retries, delivery guarantees, idempotency, and recovery determine observable behavior.
- **Security and privacy:** producer identity, authorization, integrity, confidentiality, correlation, minimization, retention, and deletion apply across copies.
- **Programming languages:** algebraic data types, exhaustive matching, serialization, schema resolution, immutable values, and reducers encode event models.
- **Systems engineering:** interface events, state transitions, traceability, configuration baselines, verification, hazards, and lifecycle evidence parallel event assurance.

## References

1. Cloud Native Computing Foundation, *CloudEvents Specification 1.0.2*, 2022. <https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md>
2. AsyncAPI Initiative, *AsyncAPI Specification 3.0.0*, current web edition. <https://www.asyncapi.com/docs/reference/specification/v3.0.0>
3. Apache Software Foundation, *Apache Avro 1.12.0 Specification*, 2024. <https://avro.apache.org/docs/1.12.0/specification/>
4. JSON Schema, *Draft 2020-12 Specification*, 2022. <https://json-schema.org/draft/2020-12>
5. Klyne, G., and Newman, C., *RFC 3339: Date and Time on the Internet: Timestamps*, IETF, 2002. <https://www.rfc-editor.org/rfc/rfc3339.html>
6. OpenTelemetry Authors, *Logs Data Model*, current specification. <https://opentelemetry.io/docs/specs/otel/logs/data-model/>
7. W3C, *PROV-O: The PROV Ontology*, Recommendation, 2013. <https://www.w3.org/TR/prov-o/>
8. W3C, *Trace Context*, Recommendation, 2021. <https://www.w3.org/TR/trace-context/>

## Exercises

### Exercise 1

Design an event contract for `PaymentCaptured`. Include occurrence boundary, event and subject identity, source and authority, times, causation, payload, schema, retries, ordering, correction, protection, retention, and replay.

### Exercise 2

Compare full-state, delta, reference-only, and decision-event payloads for customer address change. State authority, absence, time, privacy, availability, and consumer trade-offs.

### Exercise 3

Evaluate adding a required `jurisdiction` field with reader default `US`, renaming `customerId` to `partyId` through an alias, and adding enum member `SUSPENDED`. Analyze structural and semantic compatibility for old and new writers/readers.

### Exercise 4

Design processing for duplicate, late, out-of-order, corrected, and replayed inventory events across partition changes. Include identities, sequences, state preconditions, gaps, checkpoints, side effects, and reconciliation.

### Exercise 5

Review an event platform that retains all payloads forever, sends invalid events to one dead-letter topic, allows consumers to replay themselves, and reports “exactly once.” Identify missing scopes, controls, evidence, and a safer lifecycle.

## Answers to the Exercises

### Answer 1

Define Payment Captured as the payment provider's authoritative confirmation that a specified capture against an authorized payment instrument succeeded for an amount and currency under a merchant account. Exclude request receipt, authorization, settlement, application status update, and UI acknowledgment. Use source-qualified event identity stable across retries; identify payment, authorization, merchant, order relationship where permitted, and capture operation separately.

Record provider occurrence time with clock/precision, application observation and recording time, publication time, producer, provider authority, causative capture command, correlation and trace identities without conflating them. Payload includes amount, currency, provider capture identifier, status, partial/full indicator, source evidence, and protected references—not unnecessary instrument data. Bind exact schema/profile and content type. Define per-payment version or sequence, duplicate retention, atomic consumer state, refund/fulfillment idempotency, correction and dispute events, signed/authenticated transport as required, minimization, residency, retention, replay fencing, reconciliation, and owner-reviewed tests.

### Answer 2

A full-state event can preserve the address visible at change time and support independent consumers, but it may expose extra personal data and overwrite facts outside the producer's authority. State completeness, purpose, address assertion identity, valid time, source, and profile. A delta is smaller but must distinguish set, clear, unchanged, unknown, and redacted; it needs a baseline and ordering.

A reference-only notification minimizes payload but fetches current rather than event-time state, couples consumers to availability and authorization, and may fail after deletion. A decision event such as DeliveryDestinationValidated can carry only address-derived facts necessary for one shipping decision, reducing exposure but not serving every consumer. Keep the authoritative address assertion and change cause separate from projections. Choose per declared purpose, and document loss, time, access, retries, correction, retention, and consumer behavior.

### Answer 3

A new reader can structurally read old data with default `US`, but the value was not asserted and may be semantically false. Use unknown or evidence-backed migration for any consequential use. New writers requiring jurisdiction can break old readers depending on unknown-field and validation behavior. Test exact schema mechanism.

An alias may preserve field transfer, but `customerId` and `partyId` are semantically compatible only if they identify the same concept, scheme, and population. If customer role became broader Party identity, the change is breaking despite successful resolution. Adding `SUSPENDED` breaks old exhaustive readers or unsafe fallbacks even when the wire parser accepts it. Define explicit unknown handling, stage consumers, bind code-system versions, run writer-reader and decision tests, support coexistence and rollback, and retain historical writer semantics.

### Answer 4

Use source-qualified event IDs for duplicate detection and a governed inventory-position identity plus authoritative version or sequence for business order. Store event identity and state transition atomically. Reject or quarantine invalid backward versions, buffer bounded gaps, request a versioned snapshot when gaps exceed policy, and apply commutative adjustments only when the operation semantics support it.

During partition change, preserve position sequence authority or publish a cutover marker and baseline; broker offsets from old and new partitions are not comparable. Corrections reference target assertions and recompute projections. Replay uses original identities and schema/reducer versions, isolated or fenced side effects, checkpoints, rate limits, and explicit target state. Reconcile counts, per-position quantities, versions, gaps, duplicates, negative-stock rules, and sampled source facts before cutover.

### Answer 5

“All forever” lacks purpose, classification, jurisdiction, legal hold, deletion, encryption/key lifecycle, cost, archive authority, schema retention, and retirement rules. One dead-letter topic mixes tenants, sensitivities, error classes, permissions, and remediation. Self-service replay can repeat payments, notifications, access changes, or device commands. “Exactly once” fails to name broker, state, time window, external effects, and failure assumptions.

Inventory event types, consumers, authorities, data classes, purposes, and obligations. Set per-type retention and protected archives; minimize payloads; isolate dead letters by risk and tenant; preserve original evidence; classify transient versus deterministic failure; assign owners and remediation windows. Replay requires authorization, exact interval and artifacts, idempotency, side-effect fencing, checkpoints, quotas, monitoring, dry run or shadow target, rollback, and reconciliation. Report scoped delivery and processing guarantees with duplicate and outcome evidence rather than a universal slogan.
