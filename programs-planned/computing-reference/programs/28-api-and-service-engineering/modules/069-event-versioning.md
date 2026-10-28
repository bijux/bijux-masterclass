---
module_id: API-069
program: API & Service Engineering
level: 2
module_number: 69
title: Event Versioning
status: complete
last_verified: 2026-09-02
---

# Event Versioning

## One-Page Review

### Governing question

How can event producers, contracts, registries, brokers, consumers, archives, and replay tooling evolve independently while every historical fact remains interpretable and its meaning does not change silently?

### Essential definitions

- An **event type** names a stable kind of fact and its semantic contract.
- A **writer schema** is the schema used to encode one event; a **reader schema** is the schema a consumer uses to interpret it.
- **backward compatibility** means a newer reader can consume data written by an older writer under the selected format/policy.
- **forward compatibility** means an older reader can consume data written by a newer writer; **full compatibility** requires both directions.
- **transitive compatibility** checks a candidate against all governed historical versions, not only its immediate predecessor.
- A **breaking change** violates wire, structural, source-code, validation, or domain-semantic expectations for supported consumers/data.
- An **upcaster** deterministically maps an older representation into a newer internal representation without changing the historical fact.
- An **event revision/type version** identifies payload-contract evolution; a **subject version** orders state transitions for one domain entity. They are not interchangeable.

### Central model, mechanism, or theorem

Let writer versions be $W_i$, reader versions $R_j$, and compatibility predicate $C(R_j,W_i)$. A rollout is safe only for every producer/consumer pair that can coexist and every retained/replayed writer version:

$$
\forall (i,j)\in P_{coexist/replay},\quad C(R_j,W_i)=true
$$

and the decoded meaning satisfies domain invariants. Schema-registry acceptance can establish format-specific structural compatibility; it cannot prove units, defaults, authorization meaning, required business behavior, or side effects.

### Critical invariants

Historical event bytes/schema identity remain recoverable for the full retention/audit horizon. Envelope specification version, content type, event type/revision, data-schema identifier, registry ID/version, producer release, and subject version have distinct fields and meanings. Same event ID never names semantically different content. Compatible changes preserve event meaning; breaking changes use a new event type/major contract and explicit migration/coexistence.

Every candidate is checked against the actual wire format, generated-code/source dependencies, open/closed content model, consumer tolerance, retained writer set, and semantic contract. Defaults represent a valid known interpretation, not convenient zero/empty values. Unknown enum/union variants have policy. Producers deploy only when active consumers can read them; consumer migrations account for old retained data and replay. Upcasters are deterministic, versioned, tested, observable, and preserve original evidence.

### Common failures

Using one `version` field for schema, envelope, and subject order; treating registry schema ID as domain version; editing a registered schema in place; checking only latest-to-latest; assuming “add optional field” is semantically safe; meaningful default fabricated for missing history; changing units/timezone/identifier interpretation without type change; reusing Protobuf field numbers; consumers exhaustively switch on enum; closed JSON objects reject new fields; dropping unknown fields during read-modify-write; changing CloudEvents `specversion` for payload evolution; dual publishing with different event IDs/facts; upcaster performs live I/O; deleting writer schemas; and replaying old data through only current happy-path tests.

### Compact example

`OrderShipped` originally records `weightKg`. A team wants grams and renames the field to `weight` while keeping a numeric type. Wire/registry checks might accept an alias or optional transition, but the meaning is ambiguous and old consumers multiply the wrong unit. The safe design keeps the old event stable, introduces an explicit `weightGrams` field with clear precedence during a compatible window or a new major event type for the semantic break, tests mixed readers/writers, and preserves original schema for replay. **Conclusion:** structural compatibility is necessary but not semantic compatibility.

### Connections

[Event Schema Design](062-event-schema-design.md) defines the contract surface; [AsyncAPI Contracts](063-asyncapi-contracts.md) publishes channel/message operations. [Ordering and Partition Keys](065-ordering-and-partition-keys.md), [Idempotent Consumers](067-idempotent-consumers.md), and [Dead-Letter Handling](068-dead-letter-handling.md) protect migrations and replay. The next module integrates all of these into an asynchronous API design.

## Governing Question

What exact compatibility relation must hold among every active and retained writer/reader, and what release, migration, upcasting, replay, and retirement controls preserve both decodability and domain meaning across event evolution?

## Why This Matters

Events outlive deployments. A synchronous request usually meets a currently running server; an event can wait in a backlog, archive for years, cross a bridge, feed an unknown consumer, or replay after every original producer is gone. Changing its contract affects software and data distributed across time.

“Version” is overloaded. CloudEvents `specversion` identifies the envelope specification, not the domain payload revision. A registry schema ID identifies stored schema content, not subject order. An order's `orderVersion=19` expresses domain state progression, not that the event uses contract v19. A producer application release can change without changing any public contract. Conflating these dimensions makes routing, deduplication, compatibility, and incident diagnosis unreliable.

Serialization formats provide different evolution mechanisms. Avro resolves writer and reader schemas using names, aliases, defaults, unions, and promotion rules. Protocol Buffers uses stable field numbers and has distinct binary-wire, JSON, and generated-source compatibility concerns. JSON Schema behavior depends on vocabulary, validators, and whether the content model permits unknown properties. Registry compatibility modes define a check direction and history depth but do not replace format specifications or consumer behavior.

Most costly breaks are semantic. A field can keep the same type while its unit, timezone, reference authority, null meaning, precision, privacy classification, or lifecycle changes. An enum addition can crash an exhaustive switch. A default can invent facts never observed. Safe evolution couples automated structural checks with domain review, consumer evidence, mixed-version tests, and governed rollout.

## Prerequisites and Retrieval

Retrieve [Event Schema Design](062-event-schema-design.md), [AsyncAPI Contracts](063-asyncapi-contracts.md), [Ordering and Partition Keys](065-ordering-and-partition-keys.md), [Idempotent Consumers](067-idempotent-consumers.md), and [Dead-Letter Handling](068-dead-letter-handling.md). Be able to distinguish immutable event identity, event type, schema identifier, producer release, and subject sequence.

Retrieve the exact serialization specification/version, registry implementation/configuration and subject naming, canonicalization/fingerprint rules, generated-code/runtime versions, all supported consumer languages, active/lagging deployments, retained/archive writer schemas, replay horizon, channel topology, and downstream data contracts. Inventory manual/deserializer/upcaster logic and consumers outside the central registry.

## Learning Objectives

After completing this module, you can:

1. separate envelope, event-type, payload-schema, registry, producer, and subject versions;
2. express backward, forward, full, and transitive compatibility as reader/writer relations;
3. evaluate format-specific evolution for Avro, Protobuf, JSON Schema, and envelopes;
4. detect semantic breaks that structural compatibility checks cannot prove;
5. choose additive evolution, upcasting, new event type, dual publication, or migration;
6. sequence mixed-version producer and consumer rollout safely;
7. preserve writer schemas, original bytes, identities, and lineage for replay;
8. govern registries, compatibility baselines, waivers, deprecation, and retirement;
9. test the full reader/writer/replay matrix with fixtures, properties, and shadow traffic; and
10. operate version adoption, decode/upcast failures, unknown variants, and migration parity.

## Core Exposition

### Separate every version dimension

Create a version map for each event flow:

- envelope/protocol specification, such as CloudEvents `specversion`;
- media/content type and serialization format version;
- stable domain event type plus major/breaking revision policy;
- data schema URI/name/fingerprint/registry subject, ID, and ordinal version;
- producer application artifact/configuration;
- consumer semantic implementation version;
- subject/entity sequence used for ordering and optimistic concurrency;
- message/event ID used for identity and deduplication; and
- migration/routing epoch used during topology changes.

Never expose one generic `version` and infer its meaning from context. Prefer names like `orderVersion`, `eventType`, `dataschema`, `schemaId`, and `producerArtifact`. Document which are routing/filtering inputs, which are informational, and which are invariant-critical.

CloudEvents defines `specversion` for the CloudEvents context. Its primer explicitly leaves payload versioning to producers and distinguishes `type` from `dataschema`. A backward-compatible payload change generally keeps stable type; a breaking payload change generally changes type and schema reference. Do not increment envelope `specversion` because `OrderShipped` gained a field.

Registry ordinal versions are local to a subject and policy; schema IDs may be global or scoped depending on implementation. Neither should enter domain ordering. Store enough identity/fingerprint to retrieve the exact writer schema even after migration.

### Define compatibility as a matrix

For every candidate writer $W_n$ and reader $R_j$, test whether the reader can decode and correctly interpret output. Backward compatibility usually asks whether the new reader reads old writers. Forward asks whether old readers read new writer. Full asks both. Transitive variants extend comparison to all governed historical versions rather than only previous.

Names are easy to reverse, so state the sentence beside configuration: “new consumers can read all retained old events” or “old consumers can read new events during rolling deployment.” Identify the baseline set and direction in review evidence.

Compatibility policy follows lifecycle. If old data is replayed indefinitely, new consumers need transitive backward compatibility or maintained upcasters. If producers roll before every old consumer disappears, new writer output must be readable/ignorable by those consumers. If both conditions apply, full/transitive constraints may be appropriate.

One registry subject may contain versions that are structurally related but semantically unrelated if subject naming is wrong. Compatibility passing within such a subject proves little. Bind subject to durable event/data-contract ownership and prevent accidental cross-type registration.

### Evaluate Avro evolution precisely

Avro readers use both writer and reader schemas. The specification defines record field matching, aliases, defaults for fields absent from writer data, unions, enum defaults, and type promotions. Preserve the exact writer schema or its resolvable registry identity with every datum/archive.

Adding a reader field requires a valid default when old writer records lack it under the intended resolution. The default is a read-time value, not evidence that the producer observed it. Choose `unknown`/absence when historical truth is unknown; do not use zero, empty, or current configuration if that implies a fact.

Renaming can use aliases, but implementation support and multi-language behavior must be tested. Removing a writer field may be readable by a reader that ignores it, yet old readers of new data may need a default from their own schema. Union branch order/default rules and enum additions/defaults deserve explicit fixtures.

Numeric promotion can decode but still alter precision or domain constraints. A `long` to `float` relationship is not automatically acceptable for cents, IDs, or timestamps. Format resolution is structural evidence, not semantic approval.

### Evaluate Protobuf evolution precisely

Protocol Buffers binary compatibility depends heavily on stable field numbers and wire types. Never renumber/reuse a removed field; reserve old numbers and names. Add fields with presence/default behavior understood across languages. Preserve unknown fields when messages are forwarded or read-modify-written.

Binary-wire-safe does not imply ProtoJSON-safe or generated-source-safe. Field names matter in JSON; generated packages/files/types affect source dependencies; language APIs treat presence and unknown enum values differently. Select and document the compatibility layer consumers actually use.

Enum evolution must tolerate unknown numeric values. Exhaustive business switches need an unknown path that quarantines, ignores, or safely defaults according to contract. Never reinterpret an existing enum number. Type changes that share a wire representation can still change API/source or semantic meaning.

Official Protobuf guidance lists wire-safe and unsafe updates; tools such as Buf compare candidate schemas with a baseline under wire, wire-JSON, package, or file rule sets. Configure the strictness that matches real consumers and still perform semantic review.

### Evaluate JSON event evolution precisely

JSON's syntax is self-describing, but consumer behavior is not. A tolerant parser may ignore unknown properties; a closed JSON Schema with `additionalProperties: false`, strict binding, validation gateway, generated class, or exhaustive mapping can reject them. Inventory actual reader modes.

Adding optional property is backward-compatible for new readers of old data only if absence is handled. It is forward-compatible for old readers of new data only if they ignore/preserve the property. Tightening a constraint, changing `required`, pattern, range, format, nullability, `oneOf`, or content model may reject existing data.

JSON numbers do not encode domain precision/unit. Moving from integer cents to decimal currency, string timestamp to local date, or opaque ID to parseable composite is semantic evolution even if a broad schema accepts both.

Use immutable schema URIs/fingerprints for versions; do not serve mutable different content from one cacheable URI when historical reproducibility matters. Pin JSON Schema dialect/vocabulary because keyword meaning and tooling support differ.

### Detect semantic compatibility

For each field, review name, definition, unit, scale, precision, timezone, coordinate/reference system, authority, allowed values, null/absence/default, cardinality, ordering, uniqueness, privacy, freshness, lifecycle, and invariants. For the event as a whole, review occurrence trigger, aggregation boundary, subject identity, causation, finality, and correction rules.

Changes that often hide behind compatible syntax include:

- kilograms to grams; seconds to milliseconds;
- UTC instant to local time or changed timezone assumption;
- gross to net amount or tax inclusion;
- temporary to global identifier authority;
- “unknown” changed to “not applicable”;
- list changed from set/unordered to priority order;
- snapshot changed to delta;
- preliminary event changed to legally final fact;
- PII classification/retention/purpose expanded; and
- subject key/version semantics changed.

Write semantic assertions and consumer scenarios, not only schema examples. If the meaning changes incompatibly, create a new explicit field/type/major event rather than ask consumers to infer by producer release/date.

### Choose an evolution strategy

Use additive compatible evolution when the same event fact and type remain stable, old consumers can ignore new information, new consumers have honest absence behavior, and the full compatibility matrix passes.

Use an upcaster when historical representations map deterministically to a current internal model. Keep original bytes/schema/ID, record upcaster chain/version, and make the mapping pure: no current database lookup, clock, random value, network service, or mutable configuration. Unknown historical data stays unknown. Upcasters simplify domain code but create a critical long-lived migration library.

Use a new event type/major version for incompatible meaning, trigger, required data, key, unit without safe coexistence, or wire break. Decide whether channels change or type filtering suffices. Do not mutate old type meaning.

Use dual publication/translation during migration when consumers need time. Generate both representations from one authoritative source/outbox with shared causation and an explicit identity policy. Consumers must not perform the business effect twice; route by supported type or deduplicate a common logical occurrence/effect identity.

Use offline rewrite only for a derived, governed dataset where provenance, checksums, rollback, audit, and consumers allow it. Never silently rewrite an immutable event log and pretend the new bytes were originally emitted.

### Design upcasters and downcasters

An upcaster receives original writer schema/version and value, validates invariants, and emits a canonical current representation plus provenance. Chains $v1\rightarrow v2\rightarrow v3$ reuse steps but can accumulate bugs/performance and become order-dependent. Direct $v1\rightarrow current$ mappings are easier to optimize/verify per source version but duplicate logic. Choose intentionally and retain golden fixtures.

Upcasters should be total for every valid historical event or return a typed quarantine error. They never change event ID, occurred time, subject version, or causation. If a missing value cannot be inferred, represent absence/unknown or require a separate enrichment step whose output is a new derived fact, not fabricated history.

Downcasters for old consumers are riskier because new meaning may have no old representation. Define lossy policy explicitly and never discard fields needed for safety. Prefer keep-old-producer/dual-event migration over arbitrary downcast for high-risk commands/events.

Record original schema fingerprint, target model version, upcaster artifact, result fingerprint, latency, and failure without exposing payload. Determinism tests run the same input repeatedly and across supported implementations.

### Sequence mixed-version rollout

For an additive change intended to support old consumers, deploy tolerant/new consumers first when possible, then enable new producers. Verify old readers ignore/preserve additions and new readers handle old retained events. Feature flags/canaries reduce producer population but do not change compatibility requirements.

For a breaking new type, publish contract/registry entry, deploy consumers able to accept both, shadow/compare, then dual publish or translate from one source. Track adoption by actual event/read success, not repository dependency versions. Stop old type only after all registered and observed consumers, dormant jobs, replayers, partners, and disaster paths migrate.

Rollback matters. A producer rollback must still read its current source state and avoid emitting invalid old schema. A consumer rollback must tolerate already-published new events. Registry policy should block incompatible rollback registrations as well as forward changes.

Multi-region/asynchronous deployment extends coexistence windows. Registry propagation, schema cache, bridge, and artifact lag must be tested. Never assume “deployed everywhere” is instantaneous evidence.

### Govern schema registry and contracts

Registry stores schemas and applies format-specific compatibility under subject/configuration. Define subject naming, ownership, allowed formats, compatibility mode/direction in plain language, transitivity, normalization/fingerprint, references, immutability, authorization, audit, replication, availability, cache behavior, and deletion policy.

Keep compatibility configuration as reviewed code and prevent producers from bypassing registry. CI compares candidate against the same governed baseline; server-side registration enforces it. A waiver is scoped by type/version/time/consumers, includes migration and removal, and cannot merely disable checks globally.

Schema registration success does not certify producer serializer behavior or consumer deployment. Validate encoded fixtures against registered writer schema and read them with supported consumers. Protect registry from subject squatting, schema poisoning, unauthorized compatibility weakening, and destructive deletion.

Publish human-readable semantics, examples, owners, lifecycle, privacy, ordering/idempotency, and deprecation beside machine schema/AsyncAPI. Generated docs do not replace a stable domain contract.

### Preserve history and replayability

For every event retain/recover exact writer schema/dialect/registry reference, serialization/content type, original bytes or lossless form, event identity/type, and provenance. Back up/replicate registry consistently with logs and archives. A restored log whose schema IDs now resolve differently is corrupted even if bytes survived.

New consumers must process the oldest replay-eligible version or declare a migration boundary with snapshot/upcaster/archive reader. Test full retention, not only recent samples. Compaction can remove intermediate facts; schema evolution and replay semantics must account for what remains.

Do not delete schemas because no current producer uses them while retained data still references them. Registry hard deletion, subject reuse, or ID collision across environments can make disaster recovery impossible. Use immutable promotion/mapping between environments rather than assuming numeric IDs match.

Reprocessing with new consumer code can intentionally produce a new derived projection, but original events do not change. Store replay run/version/high-water and isolate effects so a rebuild does not resend payments/emails.

### Observe and verify evolution

Build a reader-writer fixture matrix across all retained writer versions, active/candidate/rollback reader versions, languages/runtimes, binary/JSON paths, upcasters, and unknown fields/enums. Structural checks run in CI; integration tests serialize with actual writer and deserialize/interpret with actual reader.

Property tests assert old meaning survives round trips, unknown fields remain where required, upcasting is deterministic/idempotent, defaults do not violate invariants, and subject/event identities remain stable. Mutation tests introduce field removal, number reuse, enum, closed-object, unit, null, precision, and type errors and require gates to fail.

Shadow consumers compare counts, decode/upcast errors, field presence/unknown rates, semantic invariants, state checksums, subject versions/gaps, latency, and side-effect intent. Dead letters cluster by schema/type/producer/consumer release. Dashboards show writer-version distribution and last-seen active/dormant consumers so retirement has evidence.

Fault tests cover registry unavailable/stale/cache collision, incompatible registration, rollout/rollback interleaving, region lag, dual-publish partial failure, bridge header loss, archived replay, deleted schema attempt, corrupt fingerprint, and upcaster failure. Reconciliation ties source facts to both old/new types and projections.

## Definitions and Notation

Let $W_i$ be writer schema/type version $i$, $R_j$ reader implementation/schema $j$, and $C(R_j,W_i)$ the conjunction of decode, structural, and declared semantic compatibility. Let retained writer set be $H$, active/candidate/rollback reader set $A$, and coexistence pair set $P\subseteq H\times A$.

Backward for candidate reader $R_n$ over history requires $C(R_n,W_i)$ for required old $i$; forward for old reader $R_i$ and candidate writer $W_n$ requires $C(R_i,W_n)$. Full requires both directions. Transitive policy quantifies over all governed prior versions, not only $n-1$.

Let stable event identity be $m$, event type/major contract be $\tau$, writer schema fingerprint be $s_i$, and subject version be $v$. Evolution may change $s_i$ compatibly while keeping $\tau$; incompatible meaning creates $\tau'$. Neither $s_i$ nor $\tau$ substitutes for subject order $v$ or identity $m$.

## Mechanisms, Invariants, or Proof Structure

1. Inventory active, lagging, dormant, partner, replay, and rollback producers/consumers plus retained writer versions.
2. Separate envelope, format, event type, schema, registry, producer, consumer, subject, and migration version dimensions.
3. Define compatibility direction/history in reader-writer sentences and format-specific rules.
4. Review semantic meaning, defaults, unknowns, units, identifiers, trigger, privacy, key, and ordering invariants.
5. Choose additive change, pure upcaster, new type/major, dual publication, or governed derived rewrite.
6. Enforce immutable registry subjects/schemas, compatibility baselines, CI/server checks, authorization, and audit.
7. Deploy consumers/producers in an order safe for every coexistence and rollback pair.
8. Preserve exact writer schema/original evidence and deterministic conversion for the full replay horizon.
9. Verify the complete matrix with fixtures, language runtimes, shadow state, failure injection, and semantic assertions.
10. Retire only after observed adoption, retention/replay boundaries, parity, rollback window, and consumer owner sign-off.

Proof sketch: if every possible pair $(W_i,R_j)$ during deployment/replay satisfies $C$, identity/type semantics are invariant, and conversions are deterministic and evidence-preserving, then mixed versions remain decodable and semantically acceptable within the declared matrix. Registry structural checks can establish only part of $C$. Missing dormant readers, nontransitive history, semantic changes, mutable schema resolution, or effecting dual consumption breaks the conclusion.

## Alternatives and Trade-Offs

**Compatible in-place type evolution versus new major type.** In-place avoids channel/type proliferation but constrains future changes and demands tolerant readers. New type makes break explicit but needs coexistence, migration, and retirement.

**Schema version in payload versus registry/envelope reference.** Explicit payload revision aids routing/debugging across systems; registry fingerprint avoids duplicated/mutable numbering. Use clear distinct identity, often both, without generic `version`.

**Latest-only versus transitive compatibility.** Latest-only permits stepwise changes whose endpoints may not interoperate with old retained data. Transitive protects long replay at stronger evolution cost.

**Upcaster chain versus direct-to-current.** Chain centralizes incremental changes but accumulates dependency/performance; direct mappings isolate history versions but duplicate transformation logic.

**Dual publish versus consumer translation.** Dual publish eases consumers but increases producer/topology/duplicate risk. Consumer translation centralizes reading but distributes upcaster/runtime complexity.

**Open versus closed JSON content model.** Open supports additive evolution but may hide typos/unvalidated data. Closed detects unexpected fields but makes additions forward-breaking unless readers coordinate.

**Strict source compatibility versus wire-only compatibility.** Source rules protect generated-code clients and imports; wire-only permits refactoring but may break build/API users. Select actual contract surface.

**Permanent historical schemas versus migrated snapshot boundary.** Permanent support maximizes replay flexibility at maintenance cost. Snapshot/migration boundary simplifies consumers but needs verified completeness, lineage, rollback, and audit.

## Failure Modes and Misconceptions

1. CloudEvents `specversion` is changed for domain payload evolution.
2. Registry ID/version or producer release is treated as subject sequence.
3. “Backward compatible” is stated without naming new reader/old writer direction.
4. Candidate is checked only against immediate predecessor despite older retained data.
5. Registry subject combines unrelated event types or wrong ownership boundary.
6. Registered schema is edited/deleted/reused while historical data references it.
7. Optional/additive structural change has incompatible semantic default or behavior.
8. Unit, timezone, identifier authority, snapshot/delta, or finality changes silently.
9. Protobuf field number is changed/reused or JSON/source compatibility is ignored.
10. Enum/union/unknown field reaches exhaustive or lossy consumer.
11. JSON reader is stricter than the assumed open schema policy.
12. Upcaster invents historical data from current clock/database/configuration.
13. Dual publication creates two business effects or divergent logical facts.
14. Producer deploys before old consumers can tolerate new writer data.
15. Rollback consumer cannot read events already emitted by new producer.
16. Registry/cache/bridge differs across regions/environments without fingerprint verification.
17. Replay loses exact writer schema or runs effecting handlers during projection rebuild.
18. Old type retires based on dependency inventory rather than observed use and retention evidence.

## Worked Examples

### Example 1

`OrderCreated` adds optional `salesChannel` whose absence means `unknown`. New readers consume old events with unknown; old tolerant readers ignore the addition. Mixed-language fixtures and semantic analytics behavior pass before producer enablement.

### Example 2

A team adds `isFraud=false` as a default to old events even though no historical assessment occurred. Schema resolution succeeds but meaning is false. The contract uses `fraudAssessmentStatus=unknown|clear|suspected` and does not fabricate clear history.

### Example 3

Protobuf field 7 is removed. Its number and name are reserved permanently. A new field uses 12; binary, JSON, generated-source, unknown-field forwarding, and old-reader tests run under the chosen compatibility policy.

### Example 4

A JSON consumer binds strictly and rejects unknown properties despite a producer assuming tolerant JSON. The compatibility matrix exposes the forward break; consumers deploy tolerance before the producer adds `warehouseZone`.

### Example 5

An Avro field `customerId` becomes `accountId` with an alias and unchanged authority. Cross-language writer/reader fixtures verify alias resolution. If authority also changed, a new field/type would be required regardless of alias.

### Example 6

Historical v1 shipment events lack carrier class. A pure upcaster emits `carrierClass=unknown`, preserves original ID/time/order version and schema fingerprint, and records conversion version. It never queries today's carrier database.

### Example 7

`PriceCalculated` changes from tax-exclusive to tax-inclusive meaning. The producer introduces a new major event type with explicit components, dual publishes from one outbox, and downstream billing selects one type/effect identity instead of consuming both.

### Example 8

A registry uses backward compatibility against only the previous version. v2 adds a default, v3 removes it under a stepwise-permitted path, but a v3 reader cannot replay v1. Transitive checks or a maintained v1 upcaster would have caught the horizon gap.

### Example 9

Region B's registry cache maps numeric ID 41 differently after disaster restoration. Consumers verify schema fingerprint/subject mapping and stop rather than decode bytes under the wrong schema. Restoration treats registry and log as one consistency set.

### Example 10

The old event type has no live traffic for 30 days, but a quarterly regulatory job and two-year archive still read it. Retirement waits for job migration and an explicit archive/snapshot/upcaster boundary; last-seen dashboard alone is insufficient.

## Cross-Program Connections

[Database Engineering](../../18-database-engineering/ROADMAP.md) supplies schema migration, immutable history, constraints, snapshots, and transactional rollout. [Programming Languages and Semantics](../../01-programming-languages-and-semantics/ROADMAP.md) supplies type systems, serialization, generated APIs, sum types, and unknown-variant handling.

[Data Engineering](../../19-data-engineering/ROADMAP.md) uses schema-on-read/write, registry, backfill, replay, data contracts, and versioned transformations. [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies mixed-version deployment, partial failure, replication, identity, and compatibility boundaries.

[Platform Engineering](../../29-platform-engineering/ROADMAP.md) owns registry availability/policy, CI gates, artifact promotion, rollout telemetry, and disaster restoration. [Security Engineering](../../25-security-engineering/ROADMAP.md) contributes contract authorization, schema poisoning defense, privacy classification, audit, and safe retirement. [Systems Engineering](../../26-systems-engineering/ROADMAP.md) contributes interface configuration control, change impact, verification matrices, traceability, and lifecycle evidence.

## References

1. Apache Software Foundation. “Apache Avro Specification.” Retrieved 2026-09-02. <https://avro.apache.org/docs/1.12.0/specification/>
2. Google. “Protocol Buffers: Language Guide (proto3), Updating a Message Type.” Retrieved 2026-09-02. <https://protobuf.dev/programming-guides/proto3/#updating>
3. Confluent. “Schema Evolution and Compatibility for Schema Registry.” Retrieved 2026-09-02. <https://docs.confluent.io/platform/current/schema-registry/fundamentals/schema-evolution.html>
4. JSON Schema. “JSON Schema Core, Draft 2020-12.” <https://json-schema.org/draft/2020-12/json-schema-core>
5. Cloud Native Computing Foundation. “CloudEvents Specification 1.0.2.” <https://github.com/cloudevents/spec/blob/ce@v1.0.2/cloudevents/spec.md>
6. Cloud Native Computing Foundation. “CloudEvents Primer 1.0.2: Versioning of CloudEvents.” <https://github.com/cloudevents/spec/blob/ce@v1.0.2/cloudevents/primer.md#versioning-of-cloudevents>
7. Buf. “Detecting Breaking Changes.” Retrieved 2026-09-02. <https://buf.build/docs/breaking/>

## Exercises

### Exercise 1

For an event envelope containing `specversion`, `type`, `dataschema`, `schemaId`, `producerVersion`, `orderVersion`, and `id`, define each dimension, uniqueness/scope, routing role, and whether it should change for an additive field, breaking semantic change, producer patch, and later order transition.

### Exercise 2

Build the required compatibility matrix for four retained writer versions, two active reader versions, one candidate reader, and one rollback reader. State the pair count for exhaustive testing and how backward, forward, full, and transitive policies cover—or fail to cover—the matrix.

### Exercise 3

Review these proposed changes for Avro, Protobuf, and JSON consumers: add optional field, rename field, add enum value, remove field, change integer cents to decimal dollars, and close JSON additional properties. Identify structural/wire/source and semantic concerns and propose safe migrations.

### Exercise 4

Design an upcasting subsystem for six years of retained order events across five payload versions and three languages. Include purity, original evidence, schema retrieval, chain/direct choice, unknowns, performance, cache, deterministic tests, failures, observability, and disaster recovery.

### Exercise 5

Plan migration from `PaymentAuthorized.v1` to an incompatible `PaymentDecision.v2` across 40 consumers, three regions, archived replay, and effecting workflows. Include contracts, dual publication/identity, rollout/rollback, parity, registry, ordering/idempotency, dead letters, security, retirement, and proof of completion.

## Answers to the Exercises

### Answer 1

`specversion` identifies the envelope specification and changes only when that specification/binding requires it, not for payload evolution. `type` identifies the stable domain event kind; keep it for compatible additions and change its major/type identity for incompatible semantic contract. `dataschema` identifies the payload schema resource/fingerprint/version and normally changes for every schema revision. `schemaId` is a registry lookup identity under documented registry scope; it changes when a new schema is registered and is not portable domain order.

`producerVersion` identifies implementation artifact/config for diagnosis and may change on patches without contract change. `orderVersion` is authoritative per-order subject sequence and changes for each ordered state transition, regardless of schema. `id` identifies one immutable event occurrence in combination with source/tenant scope and must not change across retry, bridge, replay, or alternate compatible representations according to the documented dual-publish identity policy.

Adding a compatible field changes data schema/registry ID, not envelope type/specversion or an existing event's order/id. Breaking meaning creates a new type/major and schema; it may share causation with an alternate representation but cannot reuse one ID for different semantic content unless the contract defines representations as the same occurrence without ambiguity. Producer patch changes only producer artifact. A later order transition has a new event ID and higher `orderVersion`, even if schema/type stay unchanged.

### Answer 2

There are four retained writers and four reader implementations (two active, one candidate, one rollback), so exhaustive retained writer-reader testing has $4\times4=16$ pairs. If a candidate new writer will also coexist, add it as a fifth writer, yielding $5\times4=20$ pairs; explicitly include any old active writers not represented in retained fixtures.

Backward compatibility for the candidate reader tests it against required old writer versions—four pairs—but says nothing about the two active or rollback readers reading a new writer. Forward compatibility tests old readers against the candidate writer but says nothing about the candidate reader replaying history. Full combines both directions around the candidate but a nontransitive registry mode may compare only the immediate prior schema and miss v1/v2.

Transitive backward checks candidate reader/schema against all governed old writers; transitive forward/full extend the relevant directions across history. Registry results still do not test application implementations, languages, semantic invariants, producer encodings, or rollback binaries. The executable 16/20-pair matrix is the evidence, with policy used as a gate rather than a substitute.

### Answer 3

An optional field is often safe for new readers of old data when absence/default is valid and for old readers of new data only when they tolerate/preserve unknowns. Avro needs correct reader default; Protobuf presence/JSON/source behavior varies; JSON closed readers may reject. Test semantic absence.

Rename: Avro may use tested alias; Protobuf binary retains field number but JSON/generated source name changes; JSON needs dual fields/translation or new schema/type. Preserve old name during a window and define precedence. Adding enum value requires reader unknown/default behavior; exhaustive switches can break even if wire permits it. Do not reinterpret existing numbers/symbols.

Removing a field may be backward-readable by new consumers but forward-breaking for old consumers of new writers and source-breaking; reserve Protobuf number/name. Retain/deprecate until readers migrate or create new major. Cents-to-dollars is a semantic unit/precision break even if numeric promotion parses; add explicit `amountMinor`/currency scale or new major, dual publish, and reconcile.

Changing JSON from open to `additionalProperties: false` tightens validation and can reject every historical/new extension. Introduce a new schema/type or first inventory/remove unknowns and coordinate all writers/readers with transitive fixtures. For every format, separate wire decode, validation, generated source API, unknown preservation, and domain meaning.

### Answer 4

Retain original bytes/lossless form, event ID/type/subject version/time/causation, writer schema fingerprint/registry subject-ID mapping, content type/dialect, and source coordinates. Replicate/back up registry and log/archive consistently; verify fingerprints on restore. A schema resolver retrieves immutable writer schemas into a bounded fingerprint-keyed cache whose corruption/staleness fails closed.

Define one canonical internal model with explicit unknown/absence. Each historical version has a pure deterministic converter: no network, current database, clock, randomness, or mutable config. With five versions, direct-to-current mappings isolate each source and avoid long chains; shared verified primitives reduce duplication. If using chain, snapshot every intermediate contract and test composition/direct equivalence. Language implementations consume common golden input/output bytes/fingerprints and semantic invariants.

Run all valid fixtures, boundary values, unknown enum/field, corrupt schema/fingerprint, repeated conversion, concurrency, and cross-language comparisons. Property tests require same input→same result, identity/order/time preservation, and no invented fact. Unsupported valid history returns typed quarantine with original evidence; it never partially applies effects.

Measure source/target version, upcast latency/cache hit/failure class, unknown/default use, volume/age, and result fingerprint with safe IDs. Capacity-test full six-year replay and isolate projection rebuild from business effects. Disaster tests restore registry/cache/artifacts/archive, replay checksums/high-water, missing schema, and rollback converter. Converter artifacts and schemas remain retained as long as replay or audit requires them.

### Answer 5

Publish immutable v1 and v2 semantic contracts, schemas, owners, privacy, effect/order/idempotency behavior, and a mapping table explaining the incompatibility. Register under separate governed subjects/types with transitive policies and regional fingerprint parity. Generate both from one authoritative payment transaction/outbox so they cannot diverge; carry shared causation/payment decision ID and explicit representation identity. Effecting consumers route to exactly one supported type and use the same stable business effect ID to prevent double action.

Inventory all 40 consumers plus dormant jobs, partners, dead-letter/redrive paths, archives, disaster and rollback artifacts. Deploy consumers that can accept v2 or select v1 first across three regions; shadow non-effecting v2 projections and compare counts, decision/status/amount invariants, subject versions, IDs, latency, and DLQs. Then canary dual publication per region/tenant, preserving ordering keys and transactional publication. Rollback consumers remain able to handle already-emitted v2 or traffic routes back to dual-compatible versions.

Monitor actual last-seen/read/decode/upcast/effect outcomes by consumer version; reconcile authoritative payment decisions to v1, v2, inbox/effect/outbox, and projections. Quarantine same-causation divergence, unknown schema, ordering gaps, or uncertain effect. Registry unavailability/cache mismatch and regional lag fail safely. Secure registration, compatibility settings, schema reads, PII, and migration controls with audit.

Archived replay either retains a v1 reader/upcaster into a non-effecting canonical model or establishes a verified snapshot/migration boundary. Do not replay both types into effects. Stop v1 only after all 40/dormant/external/disaster paths have observed migration, backlog/DLQ are drained or dispositioned, parity holds through the maximum observation/rollback window, and archive policy is proven. Preserve v1 schemas/contracts/upcasters while retained data references them; retirement evidence records consumer owner sign-off, high-water marks, checksums, and rollback/removal plan.
