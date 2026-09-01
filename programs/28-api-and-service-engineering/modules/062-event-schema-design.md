---
module_id: API-062
program: API & Service Engineering
level: 2
module_number: 62
title: Event Schema Design
status: complete
last_verified: 2026-09-02
---

# Event Schema Design

## One-Page Review

### Governing question

How should an event schema encode an immutable domain fact, interoperable envelope, precise data meaning, privacy and ordering context, and an evolution contract that remains safe for independently deployed producers, consumers, retained history, and replay?

### Essential definitions

- An **event schema** is the governed structural and semantic contract for one immutable fact type, including envelope, data, constraints, compatibility, and lifecycle metadata.
- A **writer schema** describes data emitted by a producer; a **reader schema** is the view a consumer uses to interpret it.
- **backward compatibility** means the new reader can consume data written with the old schema; **forward compatibility** means the old reader can consume data written with the new schema. Exact definitions depend on serialization and policy.
- **semantic compatibility** means existing consumers' justified interpretations remain valid, not merely that bytes can be decoded.
- An **event type** names one enduring business fact; a **schema version** identifies a representation contract for that meaning.
- **presence**, **null**, **default**, **empty**, and **unknown** are distinct states unless the contract deliberately equates them.
- A **logical type** gives domain meaning to a physical representation, such as timestamp, decimal amount, duration, or UUID.
- An **upcaster** transforms a historical representation into a newer in-memory view without rewriting the original fact.
- A **schema registry** governs identities, versions, compatibility checks, ownership, retrieval, and lifecycle; it does not prove semantic correctness.

### Central model, mechanism, or theorem

Let $V(S)$ be values structurally accepted by schema $S$, $decode(w,r,x)$ the format-specific writer-to-reader resolution, and $M_S(x)$ the documented meaning. A new reader $r_1$ is backward compatible with old writer $w_0$ only if

$$
\forall x\in V(w_0): decode(w_0,r_1,x)\text{ succeeds and }M_{r_1}(x)\simeq M_{w_0}(x).
$$

Structural acceptance without meaning preservation is insufficient. Adding optional `currency` with default `USD` is unsafe if old records included non-USD amounts. Compatibility therefore combines schema-tool checks, semantic review, historical samples, consumer contracts, and replay tests.

### Critical invariants

One event type expresses one past-tense fact owned by the authority that commits it. Envelope identifies event, type, source, subject, occurrence/production time, schema/content type, tenant/audience/classification, causation/correlation, and partition/order context; transport attempts remain separate. Payload encodes state-at-event-time, not accidental database layout or mutable current truth. Every field documents domain meaning, unit, precision/range, timezone, identifier namespace, presence/null/default semantics, sensitivity, and bounds.

Evolution never silently changes meaning, unit, authority, cardinality, or privacy of an existing field/type. Additions have safe reader behavior; removals preserve wire identifiers/names according to format; enum consumers handle planned unknowns; generated-code/runtime versions are tested; retained history remains readable under the declared replay horizon. Breaking semantic change creates a new type/version and explicit coexistence/migration. Registry checks are enforced in delivery workflow, but owners also review domain, security, data, and consumer impact.

### Common failures

Serializing an ORM/entity; one giant `EntityUpdated`; commands disguised as events; present-tense names; event ID regenerated on retry; database primary key without namespace; local timestamps; floating-point money; ambiguous integers/units; conflating occurred and published time; absent/null/default treated interchangeably; new required field without history strategy; optional field with false default; enum expansion crashing exhaustive consumers; repurposing deleted Protobuf tags; renaming without format-aware alias/reservation; changing numeric/string representation in place; attaching sensitive snapshots “for convenience”; envelope metadata duplicated inconsistently inside data; schema compatibility set to “none”; passing registry checks while changing semantics; upcasters performing I/O or side effects; rewriting retained facts; and replaying with only the latest generated classes untested.

### Compact example

`PaymentCaptured` carries CloudEvents-like identity/source/type/subject/time plus schema reference. Data contains payment ID, order ID, amount as integer minor units, ISO currency, processor reference token, capture sequence, and occurred-at instant. It excludes card details and mutable customer/order snapshots. Adding optional `captureChannel` with explicit `UNKNOWN` handling can be compatible; changing `amountMinor` from cents to decimal major units under the same field is not. **Conclusion:** wire shape, domain meaning, privacy, and historical resolution evolve as one contract.

### Connections

[Commands, Events, and Messages](061-commands-events-and-messages.md) supplies semantic taxonomy and identity. [JSON Schema](022-json-schema.md), [Protocol Buffers and Schema Evolution](052-protocol-buffers-and-schema-evolution.md), and [Choosing an Interface Style from Interaction Semantics](060-choosing-an-interface-style-from-interaction-semantics.md) supply representation and boundary foundations. The next module expresses event-driven contracts with AsyncAPI.

## Governing Question

Which fact is authoritative, what exact meaning and constraints does every envelope/data field carry, and how can old and new producers, consumers, tools, retained events, and replay coexist without silent reinterpretation, disclosure, or operational failure?

## Why This Matters

Event schemas outlive the code that first emits them. Durable logs retain old representations; independent consumers upgrade at different times; replay can send years of history through today's software. A schema change that looks harmless during producer compilation can corrupt analytics, route data to the wrong tenant, crash old consumers, or reinterpret money and time.

Syntax validators answer only part of the question. A JSON field can remain a number while its unit changes from cents to dollars. An enum can gain a structurally valid value that an exhaustive consumer treats as impossible. A new optional field can default incorrectly for historical records. A broader payload can be backward-decodable yet violate privacy retention. Semantic compatibility requires domain and consumer evidence.

The envelope also shapes operations. Stable event/source/subject identity enables deduplication and diagnostics. Type/schema references enable resolution. Partition keys and subject versions support scoped order and gap detection. Classification and tenant context constrain routing and access. These fields are not decorative metadata; they are governed behavior.

A durable event contract balances autonomy with minimization. Too-thin events force every consumer to synchronously fetch mutable current state, harming replay and historical meaning. Too-rich snapshots couple consumers to a producer's internal model and replicate sensitive data indefinitely. Good schema design begins from the fact and justified consumer decisions, then includes the smallest stable state-at-time evidence those decisions need.

## Prerequisites and Retrieval

Retrieve [API Contracts and Behavioral Guarantees](021-api-contracts-and-behavioral-guarantees.md), [JSON Schema](022-json-schema.md), [Request and Response Modeling](024-request-and-response-modeling.md), [Validation Constraints](025-validation-constraints.md), [API Threat Modeling](041-api-threat-modeling.md), [Protocol Buffers and Schema Evolution](052-protocol-buffers-and-schema-evolution.md), [Choosing an Interface Style from Interaction Semantics](060-choosing-an-interface-style-from-interaction-semantics.md), and [Commands, Events, and Messages](061-commands-events-and-messages.md).

Know the chosen serialization version, registry compatibility semantics, generated-code/runtime matrix, broker envelope/binding, retention/replay horizon, consumer inventory, data classification, deletion policy, and domain source of truth. Retrieve exact specifications; JSON Schema, Avro, Protobuf, CloudEvents, and registry products have different resolution rules.

## Learning Objectives

After completing this module, you can:

1. derive event types and payloads from authoritative domain facts rather than storage rows;
2. separate standard envelope attributes, application metadata, and event data;
3. specify identifiers, time, numbers, units, money, enums, collections, and presence precisely;
4. select JSON Schema, Avro, or Protobuf with awareness of their evolution mechanics;
5. evaluate backward, forward, full, and semantic compatibility from writer/reader perspectives;
6. design additive and breaking changes across retained history;
7. govern schema registry identities, ownership, review, publication, and deprecation;
8. protect sensitive event data through minimization, classification, retention, and erasure design;
9. build upcasters and replay paths without side effects or hidden I/O; and
10. verify schemas through tooling, fixtures, consumer contracts, fuzzing, replay, and production telemetry.

## Core Exposition

### Begin with the fact and authority

Name an event in past tense after the domain transition: `OrderConfirmed`, `InventoryReserved`, `PolicyCancelled`. State the invariant and source transaction that make it true. Identify the producer/domain owner authorized to assert it. A table update or UI interaction is implementation evidence, not automatically a business event.

Prefer specific types over a universal `EntityChanged`. Specific facts make consumer intent, authorization, retention, evolution, and observability reviewable. A generic change envelope with before/after blobs exports storage layout and forces consumers to reverse-engineer meaning. If change-data capture is intentionally the product, label it as database change data with its own schema and limitations, not as domain facts.

Separate facts from commands and notifications. `SendInvoice` is an instruction; `InvoiceIssued` is a fact; `InvoiceRefreshAvailable` may be a coalescible prompt. Their schemas require different target/audience, deadline, outcome, retention, and replay behavior.

Write a semantic definition independent of fields: trigger/commit boundary, invariants, exclusions, subject, order key, occurrence time, duplicate identity, correction model, audience, retention, and known consumers. Field design follows this contract.

### Separate envelope, metadata, and data

Use a consistent envelope across the portfolio. CloudEvents 1.0.2 offers core context attributes including `specversion`, `id`, `source`, `type`, `subject`, `time`, `dataschema`, `datacontenttype`, and data. Adopt an exact profile and binding. Do not assume the standard supplies tenant, classification, sequence, correlation, causation, delivery, authorization, or compatibility policy; add governed extensions where necessary.

Envelope fields describe the event and exchange context. Data fields describe the fact. Avoid duplicating `eventId`, type, occurred time, or subject in both unless a documented representation boundary requires it; duplicates can disagree. Transport fields such as partition, offset, delivery count, broker timestamp, signature, and attempt are not immutable fact data and should remain in the binding/observation layer.

A useful governed envelope includes stable globally/scopingly unique event ID, type and schema version/reference, source, subject, occurred time, produced time, tenant/audience/classification, content type, correlation and causation, and subject version/partition key if domain order needs them. Trace context may travel separately and must not become event identity or authorization.

Version the event representation, not deployment/build. A schema fingerprint/registry ID resolves exact wire shape; a semantic major/minor policy communicates meaning when useful. Document whether type name changes across incompatible versions and how parallel consumers subscribe.

### Model payload from consumer decisions

List justified decisions consumers make from the event: allocate shipment, update a projection, calculate revenue, notify a user, audit a transition. Include state-at-event-time needed for those decisions when fetching current state would be wrong or unavailable. Exclude fields no legitimate consumer needs.

Thin events with identifiers reduce duplication and sensitivity but create runtime dependency and lose historical state if consumers fetch later. Rich events improve autonomy/replay but widen coupling, payload, and retention risk. Use stable domain value objects rather than entire source aggregates. A payment fact may include amount/currency/status transition and safe processor reference, not customer profile, card details, every order field, and internal ORM metadata.

Distinguish event-carried state from notification-carried state. If payload is merely a hint, consumers must fetch and cannot assume every transition is represented. If replay/reconstruction is promised, ensure the event set actually contains required facts, corrections, initialization, and schema history.

### Design identifiers and references

Each identifier documents entity type, authority/namespace, uniqueness scope, stability, case/normalization, opacity, length/character bounds, and whether reuse is forbidden. `id: "123"` is ambiguous across tenants and entity types. Prefer separate `orderId`, `customerId`, or typed nested reference over a polymorphic ID/type pair unless polymorphism is truly governed.

Event ID remains stable across delivery attempts and format bindings. Subject ID identifies the entity, not the event. Correlation groups a workflow and is not deduplication. Causation points to the command/event that triggered the fact. Trace ID supports diagnostics and can change with sampling/boundaries. Registry schema ID identifies representation, not domain fact.

References can be opaque IDs, URIs, or compound keys. Avoid embedding mutable human names as identity. If a consumer needs display text at event time, label it as a snapshot value separately from stable identity. Never authorize based only on possession of an opaque ID in a message.

### Represent time and sequence precisely

Separate `occurredAt`—when the authoritative transition happened—from `producedAt`/broker timestamps. For delayed/offline ingestion, also distinguish device-observed time and server-received time with clock-quality metadata if relevant. Do not overwrite one with another.

Use an exact instant representation with UTC offset rules and precision, commonly RFC 3339 strings or a format logical type. State leap-second/precision/truncation behavior. Local date, local time, and time zone identifier are different domain values; scheduling “09:00 Europe/Stockholm” cannot be reduced permanently to one UTC instant.

Wall-clock time does not prove order. If consumers need subject order/gap detection, include authoritative aggregate version or monotonic sequence and define its scope, start, rollover, reset, and correction behavior. Partition key should derive consistently from the same ordering subject where possible. Cross-subject causality needs explicit causation/preconditions or reconciliation.

### Specify numbers, money, units, and precision

Document physical/logical unit in field name or schema documentation: `distanceMeters`, `durationMillis`, `temperatureCelsius`. Never change unit while retaining name/type. State valid range, precision, rounding, and sentinel prohibition. Avoid magic values such as `-1` for unknown; use explicit presence/status.

Money is amount plus currency and often scale. Use integer minor units only when currency-specific scale and range are defined, or a decimal logical type/string with exact precision/scale rules. Binary floating point is unsafe for exact monetary accounting. Do not add currency later with a guessed default if historic amounts could have multiple currencies.

Large integers can lose precision in some JSON/JavaScript paths. Choose string, bounded safe integer, decimal, or binary logical type based on clients and test actual encoders. Protobuf and Avro physical/logical mappings differ by language/runtime; generated type alone does not document business range.

### Define presence, null, default, and empty

For every field state whether it is required on the wire, nullable, optional/absent, defaulted by reader, or conditionally present. Define the meaning of missing versus explicit null, empty string, empty collection, zero, `UNKNOWN`, and redacted. These often represent unknown, not applicable, not collected, cleared, or withheld—different facts.

Defaults are semantic claims about old data. In Avro, reader/writer schema resolution and reader defaults matter; a default does not mean writers omit a field merely because it equals the default. In JSON Schema, `default` is annotation, not automatic mutation of instances. In Protobuf, scalar presence/default behavior depends on field form and language/runtime. Test the exact stack.

Adding a field with a syntactically valid default can be semantically false. Historical shipping records without `expedited` might safely read false only if the old process could never expedite; otherwise use unknown/absence or derive through an audited migration. Defaults must be justified from historical invariants.

### Design enums and open taxonomies

Enums improve constrained meaning but are evolution hazards. Old consumers may fail on new symbols even when the serialization format preserves unknown values. Generated languages differ in unknown-enum handling and exhaustive switches. Define whether taxonomy is closed, open with `UNKNOWN/OTHER`, or string code governed externally.

Do not use `UNKNOWN` to swallow values that require distinct safety behavior. A payment status unknown to an old consumer should normally trigger safe quarantine/reconciliation, not be treated as unpaid or complete. Define fallback per decision.

In Protobuf, follow exact field/tag and enum rules: do not reuse field numbers; reserve deleted numbers/names; keep a zero-valued enum member; avoid incompatible type changes; test unknown-field preservation across languages/JSON conversions. In Avro, enum defaults and reader resolution have format-specific behavior. Schema-tool acceptance does not prove application switches are safe.

### Bound collections and polymorphism

Every string, bytes, array, map, nested object, and union has size/depth/cardinality bounds enforced before expensive processing. Event size limits include envelope and encoding overhead. Large documents belong in object storage with authorized reference, checksum, and lifecycle rather than unbounded broker payload.

Avoid arbitrary maps such as `attributes: object` as an escape hatch. They defeat documentation, compatibility, authorization, cost, and privacy review. Use typed extension points with namespaced keys, value schemas, quotas, and ownership only when extensibility is a real requirement.

For variants, use a discriminated union/oneof and define unknown variant behavior. Do not allow discriminator and payload to disagree. A new variant is not automatically safe for old consumers. Version nested reusable types carefully; changing a shared type affects every event that references it.

### Understand format-specific compatibility

JSON Schema Draft 2020-12 can constrain JSON instances with vocabularies for structure/validation and annotations. Compatibility is not built-in writer/reader resolution: registry tools implement policies by comparing schemas. Open versus closed objects, required fields, `additionalProperties`/`unevaluatedProperties`, unions, numeric ranges, and `format` vocabulary behavior require exact tool/runtime tests.

Avro carries writer schema identity/context and defines reader/writer schema resolution, named types, aliases, defaults, numeric promotion, records, enums, unions, and logical types. Adding a reader field with a valid default can support old data; deleting/renaming and union/enum changes require resolution analysis. Test the actual registry and languages.

Protobuf uses stable numeric field tags and preserves unknown fields in normal binary flows, enabling many additive changes. Tag reuse is dangerous because old data/new code can reinterpret bytes. Generated language/API behavior, presence, enums, maps, oneof, JSON conversion, and runtime versions must be included. Reserve removed tags and names.

No format eliminates semantic review. Choose from ecosystem, clients/languages, human readability, size/performance evidence, code generation, registry support, logical types, evolution model, security tooling, and long-term archival requirements.

### Define compatibility from deployment topology

Backward compatibility matters when new consumers read old retained data. Forward compatibility matters when old consumers receive new producer data. Full compatibility requires both under the registry's precise algorithm. Transitive compatibility checks a new schema against all relevant historical versions rather than only the last.

Map real rollout: multiple producer versions, multiple consumer versions, replay readers, connectors, warehouses, stream processors, webhooks, archives, and disaster-recovery restores. A producer-first rollout may require old readers to accept new data; consumer-first may require new readers to accept old data. In durable fan-out, mixed versions and history often make transitive constraints appropriate.

Structural compatibility is one gate. Semantic compatibility reviews field meaning, invariants, units, defaults, authorization, classification, routing/partitioning, cardinality, cost, and consumer decisions. Operational compatibility reviews message size, registry availability/cache, CPU/memory, generated code, and failure behavior.

### Evolve additively when semantics permit

Safe additions commonly use optional fields with honest missing behavior, new event types for new facts, new consumers, and additive documentation/constraints that do not reject historic valid data. Yet narrowing a numeric range, closing an object, adding a required property, or tightening pattern may reject old history. Widening accepted input may make consumers observe values they cannot handle.

Deprecate before remove; measure producers/consumers and retained history. For Protobuf reserve removed tags/names. For Avro use supported aliases/defaults only with tested reader/writer pairs. For JSON document unknown-property behavior and avoid silently dropping security-relevant data during round-trip.

For incompatible meaning, create a new type/version, publish both from one authoritative transition where necessary, migrate consumers, monitor parity, stop old publication, retain resolution artifacts through history, and retire subscriptions. Dual publication must share event/causation identity mapping and avoid two sources of truth.

Never rewrite original events merely to make the latest schema convenient. Corrections are new facts; archival compaction/snapshots have separately governed lineage and reproducibility.

### Build pure, governed upcasters

An upcaster maps old representation to a new in-memory view. It should be deterministic, pure, bounded, version-to-version, and tested against real historical fixtures. It must not call mutable databases, current APIs, clocks, random generators, or external effects; otherwise replay changes with time and availability.

Some missing facts cannot be invented. If old events lack currency and no invariant determines it, an upcaster cannot honestly choose USD. Preserve unknown, join an explicit versioned reference dataset in a governed projection pipeline, or migrate through a documented data-quality process. Label inferred fields and provenance.

Keep old schemas, upcasters, generated artifacts/toolchains where needed, and compatibility tests for the retention horizon. Chain length and performance need limits; periodically create governed snapshots/compacted forms without erasing authoritative lineage.

### Govern the registry and delivery workflow

Choose registry subject/identity strategy by semantic owner and compatibility boundary, not topic naming accident. One subject per event type/major version is often easier to reason about than unrelated record types sharing a compatibility history. Define canonical schema location, owner, reviewers, compatibility mode, allowed formats, naming, documentation, classification, examples, and deprecation.

The delivery workflow lints/schema-validates, checks compatibility transitively as required, generates/tests code, runs producer/consumer contract fixtures, scans sensitive fields, checks bounds, verifies AsyncAPI/reference synchronization, and publishes immutable schema artifacts before producers use them. Production rejects unknown/unapproved schemas or quarantines per policy; it does not fetch arbitrary schemas from untrusted message URLs.

Registry availability strategy includes producer/consumer caches, immutable IDs, startup/runtime failure behavior, revocation/incident handling, access control, audit, backup/restore, and disaster recovery. Schema publishing is privileged. Consumers can read only needed schemas; credentials never appear in events.

Inventory producers/consumers through declared ownership plus observed telemetry, recognizing dynamic/replay consumers may not be continuously active. Require explicit exception for breaking compatibility and a migration artifact—not a toggle to “none.”

### Test data, meaning, and history

Test schema syntax and canonical/fingerprint behavior, then old-writer/new-reader and new-writer/old-reader matrices across supported languages/runtime versions. Include missing/null/default/unknown enum/unknown field, min/max/overflow/precision, Unicode, timestamps/time zones, nested/collection bounds, union variants, malformed/truncated/oversized/decompression inputs, and duplicate fields where parser behavior matters.

Use golden historical events from each deployed version, sanitized without changing edge semantics. Consumer contract tests assert decisions and failure modes, not only deserialization. Property/fuzz tests generate valid and invalid boundaries. Differential tests compare libraries/languages and JSON/binary conversions.

Replay into isolated projections with side effects disabled, bounded rate, checkpoint, counts/checksums/invariants, schema/upcast telemetry, and comparison to authoritative snapshots. Observe unknown type/schema, decode rejection, default use, unknown enum, payload size, upcast path/latency, quarantine/redrive, and consumer lag without logging sensitive bodies.

## Definitions and Notation

Let event type $T$ have schema versions $S_0,\ldots,S_n$. Let writer $w_i$ emit values $V(w_i)$ and reader $r_j$ interpret via format-specific $decode(w_i,r_j,x)$. Let $M_i(x)$ be documented domain meaning and $D_k$ a consumer decision function.

Structural backward compatibility of $r_j$ with $w_i$ requires successful resolution for every valid historical $x$ in the governed domain. Semantic compatibility additionally requires old justified decisions remain safe: $D_k(M_j(x))$ must preserve the relevant invariant, not merely return a value.

Let event envelope $E=(id,type,source,subject,time,schema,tenant,classification,causation,correlation,sequence)$ and data $P$. Transport attempt/broker metadata $A$ is separate. Let replay horizon $H$ define which writer versions and fixtures must remain readable.

## Mechanisms, Invariants, or Proof Structure

1. Name one immutable fact, authority, source commit, subject, and correction model.
2. Separate standard envelope/profile, governed extensions, domain data, and transport metadata.
3. Derive minimal state-at-event-time payload from justified consumer decisions and privacy constraints.
4. Specify every field's meaning, ownership, type, unit, precision/range, time/ID namespace, presence/default, bounds, sensitivity, and examples.
5. Define ordering key/version, duplicate identity, causation/correlation, and replay horizon.
6. Select format/registry and write exact backward/forward/transitive policy from rollout topology.
7. Evaluate structural, semantic, security, operational, and historical compatibility.
8. Use additive change where honest; otherwise create new type/version with coexistence and migration.
9. Keep upcasters pure and historical schemas/fixtures reproducible.
10. Gate publication and verify producer/reader matrices, consumers, fuzz boundaries, replay, and operations.

Counterexample to structural sufficiency: old schema accepts integer `amount=100` meaning cents. New schema keeps integer but documents dollars. Every decoder succeeds while value changes from 1.00 to 100.00 currency units; semantic compatibility fails. Counterexample to optional-addition safety: historical field omission cannot distinguish false from unknown, so default false corrupts decisions when true was previously possible.

## Alternatives and Trade-Offs

**Thin fact versus event-carried state.** Thin reduces duplication/sensitivity but couples consumers to mutable source reads. Rich improves autonomy and replay but expands schema/privacy/lifecycle cost.

**JSON Schema versus Avro versus Protobuf.** JSON is broadly inspectable and schema validation expressive; Avro emphasizes writer/reader resolution and data systems; Protobuf emphasizes compact tagged binary and generated APIs. Ecosystem and exact evolution behavior outweigh generic rankings.

**Closed versus open objects/taxonomies.** Closed shapes catch typos and bound input; open shapes ease extension but hide unknown data/cost/security. Controlled namespaced extension points can balance both.

**One evolving type versus new event type.** Additive representation evolution preserves subscriptions. New type is clearer for changed fact/authority/meaning but requires coexistence, migration, and possibly dual publish.

**Upcast on read versus material migration.** Upcast preserves immutable history and centralizes interpretation but adds runtime chain/cost. Material derived snapshots speed reads but require lineage, reproducibility, and invalidation. Do not overwrite source facts.

**Central governance versus domain ownership.** Central standards improve interoperability/security; domain owners understand meaning. Federated governance should combine domain approval with platform/security/data gates rather than transfer semantic ownership to a registry team.

**Transitive strictness versus delivery speed.** Strong transitive compatibility protects retained history and slow consumers but constrains change. Exceptions can be justified only with complete consumer/history migration and evidence, not by disabling the gate casually.

## Failure Modes and Misconceptions

1. Event schema mirrors a database entity instead of a domain fact.
2. One generic changed-event forces consumers to infer semantics from diffs.
3. Envelope and payload duplicate identity/time/type and can disagree.
4. IDs lack authority, tenant scope, entity type, or stability definition.
5. Time zone, unit, scale, range, rounding, or precision is implicit.
6. Missing, null, empty, zero, default, unknown, and redacted collapse.
7. An optional field/default invents false historical facts.
8. Enum/additive field passes registry but crashes or misleads old consumers.
9. Removed Protobuf tags are reused or conversions discard unknown fields.
10. A field keeps shape while meaning, unit, authority, or classification changes.
11. Rich event leaks personal/secret data into durable replicas and dead letters.
12. Upcaster calls current state or performs external side effects.
13. Registry compatibility algorithm is treated as semantic proof.
14. Only latest producer/consumer pair is tested; retained history is ignored.
15. Breaking change disables compatibility without consumer inventory, coexistence, rollback, or migration.

## Worked Examples

### Example 1

`OrderConfirmed` is derived from one authoritative order transition. It includes order/customer references, committed total amount/currency, confirmation version, occurred time, and fulfillment facts needed at that point—not the full mutable customer and catalog records. Event ID is stable across broker retries.

### Example 2

`amountMinor=1234`, `currency=SEK` means exactly 12.34 SEK only under the documented scale rule. Changing `amountMinor` to a floating major-unit number is incompatible despite a permissive JSON number schema; introduce a new field/type and migrate.

### Example 3

Adding `expedited=false` to old shipment events is rejected because old systems did support expedited shipments but did not record the flag. The new reader preserves absence/unknown; a separate historical enrichment dataset may infer values with provenance.

### Example 4

A new payment-status enum value `REVERSED` reaches an old consumer. Its exhaustive switch crashes. The registry's structural check was insufficient. The contract is revised to require unknown-safe quarantine and outcome reconciliation; consumer fixtures include future symbols before producer rollout.

### Example 5

A Protobuf field `customer_email = 7` is removed for privacy. Tag 7 and name are reserved, never reused for `customer_segment`; otherwise retained bytes could be interpreted as the new field. A minimized tokenized customer reference replaces the leaked attribute through a new version.

### Example 6

An Avro reader adds `captureChannel` with default `UNKNOWN`. Old writer/new reader resolution succeeds. Semantic review confirms old producers truly could not distinguish channels and every consumer treats `UNKNOWN` as reconciliation-required, so the addition is approved with fixtures.

### Example 7

An IoT event separates device-observed local time, device zone/offset, server-received instant, and clock quality. Subject sequence—not timestamps—orders readings. Consumers can analyze clock drift without pretending receipt time is measurement time.

### Example 8

A producer wants `attributes: object` for future flexibility. Review replaces it with a discriminated set of bounded measurement variants plus a namespaced extension map limited to approved scalar types/count/bytes. Unknown extensions do not affect authorization/routing.

### Example 9

`CustomerDeleted` history is retained for audit but cannot retain direct identity indefinitely. The schema uses a scoped pseudonymous subject token and minimal reason category; key lifecycle, legal hold, derived projections, dead-letter copies, and replay authorization implement erasure policy.

### Example 10

A three-version projection replay uses immutable registry IDs and pure S0→S1→S2 upcasters. Historical fixtures reveal S0 timestamps lacked offsets, so the upcaster emits explicit `timeQuality=UNKNOWN` instead of consulting current customer locale. Counts, subject versions, and totals are compared before cutover.

## Cross-Program Connections

[Data Engineering](../../19-data-engineering/ROADMAP.md) consumes schemas for ingestion, lineage, quality, streaming, and replay. [Database Engineering](../../18-database-engineering/ROADMAP.md) contributes transactions, change capture, constraints, and historical models. [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies logs, order, delivery, and compatibility under independent deployment.

[Security Engineering](../../25-security-engineering/ROADMAP.md) governs classification, minimization, field protection, retention, and untrusted decoding. [Software Engineering Patterns](../../11-software-engineering-patterns/ROADMAP.md) contributes value objects, anti-corruption layers, and event ownership. [Platform Engineering](../../29-platform-engineering/ROADMAP.md) supplies registry, generation, policy gates, telemetry, replay, and paved roads.

## References

1. JSON Schema Project. “JSON Schema Draft 2020-12.” Published 16 June 2022. <https://json-schema.org/draft/2020-12>
2. Apache Software Foundation. “Apache Avro 1.12.0 Specification.” <https://avro.apache.org/docs/1.12.0/specification/>
3. Protocol Buffers Authors. “Language Guide (proto3).” Retrieved 2026-09-02. <https://protobuf.dev/programming-guides/proto3/>
4. Protocol Buffers Authors. “Proto Best Practices.” Retrieved 2026-09-02. <https://protobuf.dev/best-practices/dos-donts/>
5. Cloud Native Computing Foundation. “CloudEvents Specification 1.0.2.” <https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md>
6. AsyncAPI Initiative. “AsyncAPI Specification 3.0.0.” <https://www.asyncapi.com/docs/reference/specification/v3.0.0>
7. IETF. “RFC 3339: Date and Time on the Internet: Timestamps.” July 2002. <https://www.rfc-editor.org/rfc/rfc3339.html>

## Exercises

### Exercise 1

Review an event with fields `id`, `type`, `time`, `customer`, `amount`, `status`, and `metadata`. Identify at least twelve missing semantic decisions before implementation, including envelope separation, identity, time, money, enum, extensions, privacy, order, and bounds.

### Exercise 2

For an old `ShipmentDispatched` schema, evaluate these changes structurally and semantically: add optional `carrier`; add required `currency`; widen `weightGrams` integer maximum; rename `trackingId`; add enum `RETURNING`; reuse deleted Protobuf tag 9; change `occurredAt` from UTC instant to local time. State format-dependent considerations.

### Exercise 3

Define writer versions W0/W1 and reader versions R0/R1 for a field `temperatureCelsius`. W1 adds optional `sensorAccuracyCelsius`; R1 defaults missing accuracy to `0`. Explain backward and forward questions and construct a semantic counterexample to the default.

### Exercise 4

Design a schema registry workflow for a transitive, five-year replay horizon across JSON Schema, Avro, or Protobuf. Include subject strategy, ownership, compatibility, generation/runtime matrices, fixtures, consumer evidence, privacy, publication, rollout, exception, restore, and telemetry.

### Exercise 5

Design `PatientObservationRecorded` for a multi-tenant healthcare integration. Define fact/authority, envelope, subject/order, times, identifiers, measurement/value variants, units, presence, correction, privacy, compatibility, replay, and tests. Avoid making clinical claims beyond the schema mechanics.

## Answers to the Exercises

### Answer 1

Decisions include: whether `id/type/time` are governed envelope fields and must not be duplicated; event-ID uniqueness scope/issuer/stability; exact past-tense fact and authority; source and subject/entity namespace; occurred versus produced/broker time; timestamp format/offset/precision; subject version/partition order; schema/content type/version/reference; tenant/audience/classification; causation/correlation/trace distinction; whether `customer` is stable reference or sensitive snapshot; amount currency/unit/scale/range/precision/rounding; status taxonomy and unknown behavior; missing/null/default semantics; metadata key/value ownership and bounds; payload/string/nesting/cardinality limits; retry immutability; retention/erasure; authorized consumers; and correction/replay behavior.

Replace generic `metadata` with typed fields or a bounded namespaced extension point whose contents cannot affect security/routing silently. Replace generic `status` with the exact transition fact or a governed value documented at occurrence time. Minimize customer data to the justified reference/snapshot fields. Document examples and invalid boundaries, not only a permissive shape.

### Answer 2

Optional `carrier` can be backward-readable by new readers if missing means unknown and forward-readable by old readers only if their format/parser tolerates unknown fields; semantic review checks whether old consumers need it, its code/identity taxonomy, and privacy. Required `currency` breaks old history unless reader resolution supplies an honest default or migration; a guessed currency is unsafe.

Widening `weightGrams` maximum lets new writers emit values old readers may reject/overflow, so forward compatibility can fail; new readers accepting old values is backward-compatible structurally. It may also change transport/resource bounds. Renaming `trackingId` requires format-specific alias/migration: Avro reader aliases may resolve; Protobuf retains numeric tag while generated API name changes but JSON-name/users need tests; JSON has no automatic alias and often needs coexistence/upcast.

Adding `RETURNING` may decode yet break old exhaustive logic; require unknown-safe behavior, fixtures, or new version/type. Reusing Protobuf tag 9 is forbidden because retained old bytes can be reinterpreted; reserve number/name. Changing UTC instant to local time changes meaning, ordering, and information and is incompatible even if both serialize as strings; create a new field/type with explicit zone/local semantics.

### Answer 3

W0 writes required temperature only. W1 writes temperature and optional accuracy. R1 reading W0 asks backward compatibility: can it decode absent accuracy and preserve meaning? R0 reading W1 asks forward compatibility: does the format/runtime ignore/preserve unknown accuracy and do R0 decisions remain safe without it?

Defaulting missing accuracy to 0 asserts perfect measurement. An old sensor might have ±2°C accuracy; R1 could admit a reading into a safety-sensitive “accuracy ≤0.5°C” decision incorrectly. Structural decoding succeeds while meaning fails. Preserve absent/unknown, use an optional uncertainty/range or quality state, and require consumers to handle unknown conservatively. Only a historical invariant that all W0 sensors truly had zero uncertainty—which is unrealistic—could justify 0.

### Answer 4

Use one compatibility subject per semantic event type/major boundary (or a documented equivalent) with immutable schema IDs and exact format/version. Domain owner approves fact/field meaning; platform owns registry/CI/runtime; security/privacy and data owners approve classification, retention, and replay; consumer owners declare decisions and supported versions. Require backward/forward/full transitive mode based on producer-first/consumer-first and mixed five-year history, documented against the registry algorithm.

CI validates schema/canonical fingerprint, naming/documentation/examples/bounds, CloudEvents/AsyncAPI linkage, field classifications, and prohibited patterns. Run every supported writer/reader and generated-code/runtime language pair against sanitized golden events for every retained version, including missing/null/default, unknown enum/field, number/time extremes, Unicode, unions/oneof, oversize/malformed/decompression, and JSON/binary conversions. Consumer contract tests assert decisions, not merely decode.

Publish immutable schema before producer deployment; canary new consumers/producers in the rollout order the compatibility model supports. Observe schema IDs/types, unknown/rejection/default/upcast paths, payload size, lag/quarantine without payload leakage. Exceptions require owner, affected producer/consumer/history inventory, new major/type or coexistence plan, dual-publish parity, rollback, deadline, and approval—never compatibility `none` alone.

Registry has least-privilege publish/read, audit, caches with immutable IDs, defined outage behavior, backups and restore drills including IDs/subjects/compatibility config/artifacts. Retain schemas, fixtures, upcasters, toolchains/generated sources as needed for five years. Replay drills validate counts/checksums/invariants and privacy/erasure. Deprecation uses observed plus declared consumers and retains resolution until history expires.

### Answer 5

Define the fact narrowly: an authorized clinical-record authority committed one observation record; the event does not itself diagnose or recommend treatment. Use a type such as `PatientObservationRecorded` with stable event ID, exact source/tenant organization, opaque scoped patient/encounter/observation subject references, occurred time, produced time, schema/content type, classification, causation/correlation, and per-patient or per-observation version/order only if the domain contract can provide it.

Data includes observation ID/version, code-system URI/version plus code/display as governed, status at event time, performer/reference where justified, effective instant or period with timezone/precision, issued time, and a discriminated value: quantity with decimal value/unit/system/code and range/precision; coded value; string with strict bounds; boolean; or absent-data reason. Discriminator and value agree; unknown variant/status is safe-quarantined. Missing, null, not-collected, unknown, not-applicable, redacted, and corrected are distinct.

Minimize direct identifiers and narrative; use scoped tokens/references, field classification, tenant/audience authorization, encryption, retention/legal hold/erasure/key lifecycle, protected dead-letter/fixtures, and audit. Never use event IDs or trace context as permission. Corrections are new linked facts with version/causation; do not edit retained event. Thin versus carried clinical state is selected from authorized consumer/replay needs without copying the full patient record.

Use an exact standard profile/serialization and registry ID. Define numeric decimal/range/unit semantics and timestamps without floating/unit ambiguity. Compatibility is transitive across retained history and independently deployed consumers; new codes/variants/defaults require consumer decision tests. Breaking clinical meaning gets a new type/major and coexistence plan; pure upcasters cannot invent missing clinical facts.

Verify schema and writer/reader matrices, historic sanitized fixtures, code/unit/value combinations, presence states, decimal/time/Unicode boundaries, unknown codes/variants, oversized narrative/arrays, cross-tenant IDs, authorization changes, duplicate/reorder/gap/correction, registry outage, poison/quarantine/redrive, replay with effects disabled, retention/erasure, and reconciliation to authorized source snapshots. Clinical domain and compliance experts must approve actual code systems, safety semantics, and policy; the schema mechanics alone do not establish clinical correctness.
