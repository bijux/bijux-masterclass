---
module_id: DARCH-097
program: Data Architecture Engineering
level: 2
module_number: 97
title: Data Contract Migration
status: complete
last_verified: 2026-09-03
---

# Data Contract Migration

## One-Page Review

### Governing question

How can producers and consumers migrate a data contract without losing required meaning, compatibility, behavior, quality, service, policy, evidence, or recoverability—and without allowing transitional forms to become permanent ambiguity?

### Essential definitions

- A **data contract** is a versioned agreement binding identified producers and consumers to data identity, purpose, schema, semantics, behavior, quality, service, policy, support, change, and lifecycle obligations.
- A **contract migration** is the governed transition from one contract baseline to another across declarations, implementations, data, producers, consumers, policies, operations, evidence, and retirement.
- A **contract identity** is a stable identifier distinct from contract version, schema fingerprint, transport endpoint, dataset location, product name, and implementation.
- A **contract obligation** is one testable promise about structure, meaning, behavior, quality, service, governance, support, change, recovery, or closure.
- **Structural compatibility** means old and new serializers, validators, readers, or writers can exchange declared forms under a named direction and technology.
- **Semantic compatibility** means exchanged values retain their intended concepts, units, code meanings, time, identity, applicability, and consumer interpretation.
- **Behavioral compatibility** means delivery, ordering, idempotency, defaults, errors, retries, side effects, and lifecycle behavior remain acceptable.
- **Directional compatibility** states which versioned writer or producer can be consumed by which versioned reader or consumer; “backward compatible” is incomplete without direction and technology.
- **Expand-migrate-contract** is a transition in which a producer first supports old and new forms, consumers then move under evidence, and obsolete form and behavior finally close.
- A **compatibility envelope** is the explicit set of old/new version pairs, encodings, data populations, operations, defaults, unknowns, transformations, and behaviors that are supported.
- A **contract conformance result** is evidence from a named declaration, implementation, fixture, population, scenario, version, environment, and observation time; it is not universal proof.
- A **contract exception** is a time-bounded, owned deviation with affected consumers, obligations, risk, compensating control, successor, evidence, expiry, and escalation.
- **Contract closure** proves obsolete declarations, schemas, fields, codes, endpoints, channels, files, policies, fixtures, credentials, consumers, adapters, recovery artifacts, and authority cannot silently return.

### Central model, mechanism, or theorem

Represent a contract migration as:

`M = (O, B, I, S, P, C, Q, G, T, E, R, L)`

where `O` is outcomes, purposes, users, producers, consumers, and affected decisions; `B` is old, transition, target, deployed, and retired baselines; `I` is contract, schema, dataset, message, operation, field, code, metric, and implementation identities; `S` is structure, encoding, defaults, presence, nulls, constraints, and schema resolution; `P` is semantics, grain, units, time, identity, history, correction, and behavior; `C` is producer, consumer, interface, transport, compatibility, and transformation; `Q` is quality, service, performance, availability, recovery, support, and cost; `G` is ownership, governance, security, privacy, policy, evidence, and exceptions; `T` is rollout, expand-migrate-contract, dual publication, shadowing, cutover, rollback, and correction; `E` is tests, fixtures, registry, lineage, telemetry, consumer verification, decisions, and limitations; `R` is risk, uncertainty, stop conditions, and replanning; and `L` is deprecation, sunset, adoption, debt, retirement, identifier reservation, nonactivation, and closure. Schema compatibility is only one predicate inside a successful contract migration.

### Critical invariants

- Contract, version, schema, dialect, fingerprint, field, code, semantic definition, producer, consumer, implementation, fixture, result, exception, decision, and retirement have stable identities.
- Proposed, approved, expanded, migrating, authoritative, deprecated, sunset, quarantined, retired, restored, and closed states remain distinguishable.
- Old and target contracts are versioned baselines; generated files and registry entries cannot silently replace approved intent.
- Producer-writer and consumer-reader compatibility is tested in both required directions across exact formats, encodings, versions, defaults, unknowns, and historical data.
- Structural compatibility never substitutes for semantic, behavioral, quality, service, policy, or decision compatibility.
- Grain, identity, units, codes, nulls, presence, time, history, correction, aggregation, and applicability are preserved or changed explicitly.
- One implementation or governed transformation owns derivation when old and new forms coexist; independent dual writes require reconciliation.
- Consumers migrate through observed execution and decision evidence, not acknowledgments, registration, or elapsed time.
- Security, privacy, purpose, classification, access, retention, deletion, audit, and policy decisions hold across old, new, translated, cached, replayed, and recovered forms.
- Rollback accounts for target-only values and meanings; recovery restores contracts, registries, policies, data, implementations, consumers, and authority coherently.
- Every transition adapter, duplicate declaration, compatibility branch, exception, fixture, and support obligation has owner, cost, expiry, and removal test.
- Closure reserves or tombstones obsolete identities and proves restored schemas, clients, producers, registries, and automation cannot regain authority.

### Common failures

- Calling a schema file the complete contract.
- Using “backward compatible” without naming writer, reader, encoding, version, and data population.
- Treating parser success as semantic or behavioral correctness.
- Adding optional fields whose absence, null, default, unknown, and empty meanings differ.
- Reusing field numbers, codes, names, or identifiers after removal.
- Changing units, time, identity, grain, correction, or aggregation under an unchanged version.
- Publishing both forms from independent logic and creating competing truth.
- Declaring consumers migrated because they registered, acknowledged, or passed a mock test.
- Contracting before cached, batch, partner, historical replay, and recovery consumers move.
- Leaving old schemas, policies, adapters, credentials, registry aliases, and restore paths able to reactivate.

### Compact example

An order event replaces `amount` and `currency` fields with a governed money object and replaces free-form status with a versioned code. The producer expands one authoritative implementation to derive both forms, preserving decimal precision, units, unknowns, event and valid time, correction, and original values. Exact Avro writer/reader combinations, JSON representation, old and new consumers, defaults, unknown fields, enum behavior, registry policy, access, retention, replay, errors, service, and recovery are tested. Consumers move by observed identity through daily, month-end, partner, and recovery cycles. Target-only codes block full rollback after a recorded boundary. The old fields contract only when traffic, lineage, caches, stored messages, fixtures, SDKs, schemas, policies, and recovery artifacts show no authorized dependence; their identifiers remain reserved.

### Connections

[DARCH-017](017-event-schemas-and-information-models.md), [DARCH-019](019-model-versioning.md), [DARCH-023](023-data-ownership-and-accountability.md), [DARCH-026](026-data-products-and-service-expectations.md), [DARCH-027](027-producer-and-consumer-contracts.md), [DARCH-045](045-semantic-and-metrics-layers.md), [DARCH-055](055-registry-consolidation-and-coexistence-styles.md), [DARCH-066](066-semantic-interoperability.md), [DARCH-067](067-schema-registries.md), [DARCH-079](079-audit-and-provenance-architecture.md), [DARCH-093](093-transition-architectures.md), [DARCH-095](095-legacy-integration-retirement.md), and [DARCH-096](096-cloud-data-migration.md) establish schemas, versions, ownership, product obligations, semantics, registries, evidence, transition, retirement, and migration. [DARCH-098](../ROADMAP.md) next governs architecture standards and reference patterns.

## Governing Question

A proposed “schema update” may add one optional field. That field can change message size, serializer behavior, generated code, validation, signatures, caches, defaulting, null handling, authorization, quality rules, metrics, storage, replay, and consumer decisions. A renamed status may preserve the wire value but change meaning. A compatible Avro reader may overflow an application type. An old Protocol Buffers reader may preserve unknown fields in binary yet lose them through JSON conversion. A new contract file may pass registry rules while the deployed producer still emits the old behavior.

The governing question is therefore not whether a schema checker returns compatible. It is how every required obligation moves from one versioned baseline to another across real producers, consumers, historical data, policies, operations, and recovery. A defensible migration establishes stable identities, makes direction and scope explicit, separates structure from meaning and behavior, expands through one authoritative derivation, verifies consumers with production-shaped evidence, manages exceptions, contracts obsolete forms, and proves they cannot return.

## Why This Matters

The Bitol [Open Data Contract Standard](https://bitol-io.github.io/open-data-contract-standard/latest/) provides sections for schema, quality, service, roles, support, pricing, team, and infrastructure concerns. Its breadth demonstrates that a data contract is more than a serialization schema. A standard representation enables tooling and exchange, but local authority, correctness, implementation, and consumer acceptance still require evidence.

The JSON Schema [specification](https://json-schema.org/specification) identifies the current 2020-12 specification and separates core and validation vocabularies while supporting dialect and vocabulary declarations. Schema behavior depends on which dialect and vocabularies an implementation supports; copying keywords without declaring or testing the dialect can change validation.

The Apache Avro [specification](https://avro.apache.org/docs/current/specification/) defines writer and reader schemas, schema resolution, defaults, aliases, unions, logical types, encodings, canonical form, and fingerprints. Compatibility can depend on the serialized data and binary or JSON encoding. Schema resolution is powerful, but it does not prove business meaning or application range safety.

The Protocol Buffers [proto3 language guide](https://protobuf.dev/programming-guides/proto3/) documents field numbers as wire identities, rules for updating messages, unknown fields, reserved numbers and names, enum behavior, and distinctions among binary and JSON compatibility. Wire-safe or wire-compatible change can still be lossy or unsafe in particular applications.

The OpenAPI Initiative's [OpenAPI Specification](https://spec.openapis.org/oas/latest.html) describes HTTP operations, parameters, schemas, responses, security, extensions, and deprecation. The AsyncAPI Initiative's [current specification](https://www.asyncapi.com/docs/reference/specification/latest) describes asynchronous channels, operations, messages, servers, security, and bindings. These interface descriptions connect schema to interaction context but do not prove runtime conformance or consumer migration.

Pact's [How Pact Works](https://docs.pact.io/getting_started/how_pact_works) explains consumer-driven contract interactions and provider verification against published expectations. Such tests expose actual consumer assumptions more directly than provider-only examples, yet their coverage is limited to represented consumers, interactions, states, and environments.

The [Semantic Versioning specification](https://semver.org/) relates version-number changes to an explicitly declared public API. Its discipline is useful for communicating compatibility intent. Data contracts often involve multiple structural, semantic, service, and policy dimensions, so a version number does not replace a change classification or migration proof.

Danilo Sato's [Parallel Change](https://martinfowler.com/bliki/ParallelChange.html) describes expand, migrate, and contract for backward-compatible interface change. It supplies a strong transition structure and also exposes a common lifecycle failure: expansion and migration occur, but contraction never removes obsolete behavior.

IETF [RFC 9745](https://www.rfc-editor.org/rfc/rfc9745.html) defines an HTTP `Deprecation` response header and lifecycle documentation link while stating that deprecation does not itself change resource behavior. IETF [RFC 8594](https://www.rfc-editor.org/rfc/rfc8594.html) defines the `Sunset` header for expected future unavailability. These signals support API contract migration but do not establish client discovery, compatibility, acceptance, or safe closure.

OpenLineage's [object model](https://openlineage.io/docs/spec/object-model/) identifies datasets, jobs, runs, events, namespaces, names, and facets. Stable lineage can connect contract versions to production runs and downstream consumers, provided instrumentation coverage and identity mappings are verified.

The Open Policy Agent [policy-language documentation](https://www.openpolicyagent.org/docs/policy-language) describes structured policy decisions over runtime inputs. The OpenTelemetry [specification](https://opentelemetry.io/docs/specs/otel/) standardizes telemetry signals, resources, context, and semantic conventions. Contract rollout needs both enforceable policy and observable version use, while accounting for missing context, sampling, batch work, and failure.

NASA [Configuration Management](https://www.nasa.gov/reference/6-5-configuration-management/) emphasizes identified configuration items, controlled baselines, version distinction, change control, status accounting, verification, audits, and consistency between a product and its information. A contract, its implementation, registry state, tests, documentation, and deployed behavior must remain distinguishable and traceable.

NASA [Product Transition](https://www.nasa.gov/reference/5-5-product-transition/) emphasizes readiness of the product, receiving environment, users, operators, documentation, support, acceptance, and captured work products. Contract migration is complete only when consuming systems and people accept the new baseline and transitional enabling products can close.

Together these sources support broad contract obligations, explicit schema dialects, directional schema resolution, wire evolution, interface descriptions, consumer-driven verification, version communication, expand-migrate-contract, lifecycle signaling, lineage, policy, telemetry, configuration control, and receiving-user readiness. They do not define local semantics, find every consumer, prove implementation conformance, authorize policy change, establish an observation horizon, validate rollback, or demonstrate closure. Those conclusions require local owners, deployed artifacts, production-shaped data, consumer decisions, operational evidence, and recovery exercises.

## Prerequisites and Retrieval

You should understand data products, producer and consumer ownership, schemas, serialization, APIs, events, files, tables, registries, semantic models, identifiers, null and presence semantics, time, compatibility, generated code, versioning, lineage, policy, quality, service objectives, deployment, canaries, change capture, replay, recovery, transition architecture, deprecation, and retirement.

Retrieve contract identity, version, baseline, obligation, structural compatibility, semantic compatibility, behavioral compatibility, writer schema, reader schema, dialect, vocabulary, encoding, field number, reserved identifier, default, presence, null, unknown field, enum, alias, fingerprint, compatibility direction, envelope, expansion, consumer migration, contraction, conformance, exception, deprecation, sunset, rollback, and closure.

As a retrieval test, inspect replacing an order event and analytical table contract. Ask which producers and consumers use each version; which binary, JSON, table, and generated-code forms exist; how identity, grain, money, status, nulls, time, history, corrections, ordering, errors, quality, service, policy, and recovery behave; which old readers consume new writers and new readers consume old writers; which stored data must replay; how registries and deployed artifacts agree; which consumers are cached, batch, partner, or restored; how target-only values roll back; and which proof reserves old identifiers and removes all obsolete forms.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish a data contract from schema, registry record, interface description, test, documentation, and implementation;
2. identify contract, version, schema, fingerprint, field, code, producer, consumer, fixture, result, exception, and lifecycle identities;
3. classify structural, semantic, behavioral, quality, service, policy, support, recovery, and lifecycle obligations;
4. state directional compatibility across exact writer, reader, encoding, dialect, protocol, implementation, and historical population;
5. design expand-migrate-contract transitions with authoritative derivation, mappings, consumer cohorts, evidence, rollback, and contraction;
6. test defaults, presence, nulls, unknown fields, enums, identifiers, types, precision, time, history, ordering, errors, and semantic decisions;
7. align declarations, registries, producers, consumers, policies, lineage, telemetry, documentation, and deployed baselines;
8. migrate stored and in-flight data through replay, transformation, reconciliation, correction, and recovery;
9. govern deprecation, sunset, exceptions, adoption, transition debt, identifier reservation, retirement, and nonactivation; and
10. write contract migration receipts that expose evidence, decisions, limitations, residual risk, and closure.

## Core Exposition

**Begin with the contract outcome.** Name the product, purpose, producers, consumers, affected decisions, baseline burden, desired change, mandatory constraints, owner, approval authority, evidence horizon, countermetrics, and reconsideration trigger. “Move to schema version two” names a mechanism, not a user outcome.

**Separate contract artifacts.** The approved contract, schema, API or event description, registry record, generated code, fixtures, consumer expectations, producer implementation, policy, documentation, telemetry, and deployed configuration are distinct configuration items. Give each identity, version, owner, digest, state, and relationship. A green registry entry cannot prove the producer emits it.

**Define contract identity independently of location.** Dataset path, endpoint, topic, table, file, and service may change while the logical contract continues. Conversely, reusing one location for changed meaning does not preserve identity. Define when a change is a new version of one contract, a new contract, a profile, or an implementation revision.

**Model the complete obligation set.** Include purpose; producers and consumers; identity; schema and encoding; semantics; grain; units; time; history; correction; behavior; delivery; ordering; errors; quality; service; security; privacy; support; change; recovery; cost; deprecation; and closure. Mark each obligation required, conditional, informative, or intentionally absent with owner and evidence.

**Establish old and target baselines.** Capture approved declarations, registry state, producer and consumer builds, generated artifacts, deployed configuration, stored data, observed messages or rows, policies, service, support, incidents, and known deviations. The target baseline states desired obligations and acceptance evidence; it is not complete merely because its schema compiles.

**Discover actual producers and consumers.** Combine code search, build dependencies, registry access, gateway and broker identities, topic subscriptions, query and lineage logs, file transfers, model and report inventories, access decisions, billing, schedules, caches, support tickets, recovery procedures, owner interviews, and consumer confirmation. Label declared, configured, observed, inferred, confirmed, rejected, and unknown use.

**Include transitive and stored consumers.** A stream sink becomes a table; a table feeds a model; a file is retained for replay; a mobile or partner client caches a schema; a disaster image restores old code. Migration evidence must cover direct runtime use, downstream decisions, stored payloads, historical reprocessing, and recovery.

**Choose the change boundary.** A migration unit might be one field, code set, message, operation, dataset, table, metric, consumer cohort, producer cohort, or product. The unit should preserve coherent semantics and authority while bounding blast radius, compatibility, observation, rollback, and retirement. Arbitrary schema-file boundaries can split linked meanings.

**Classify every change.** Record additions, removals, renames, type changes, constraints, defaults, presence, nulls, unknowns, enums, codes, units, time, grain, keys, order, delivery, errors, policy, quality, service, support, and lifecycle. For each, classify wire or structural behavior, semantic effect, consumer effect, historical effect, and operational effect.

**State compatibility direction.** For every required pair, name producer or writer version, consumer or reader version, serialization or storage form, encoding, dialect, generated runtime, and data population. Test old writer to new reader, new writer to old reader, and mixed deployments where required. “Backward” and “forward” are too easily reversed without the matrix.

**Distinguish parseability from safe use.** A reader may parse a wider numeric type while application code narrows it. Unknown fields may survive binary relay but disappear through JSON conversion. An added enum value may parse into an unrecognized branch. A default may supply a syntactically valid but semantically false value. Validate application decisions, not only decoder exit.

**Declare dialect and vocabulary.** For JSON Schema, record the specification dialect, required vocabularies, format behavior, reference resolution, identifiers, and validator version. Different implementations may treat annotations, formats, unevaluated content, references, or unknown keywords differently. Pin and test exact tools rather than assuming keyword portability.

**Respect wire identities.** In tag-based formats, field numbers and enum numeric values can outlive names. Never reuse removed identifiers unless the protocol and every historical consumer make that safe; reservation or tombstoning is the usual durable choice. Test binary, JSON, text, and generated-code behavior separately when all are used.

**Understand writer-reader resolution.** In schema-resolving formats, defaults, aliases, unions, promotions, logical types, names, and canonical forms determine what readers can consume. Preserve the writer schema with stored data and messages. Compatibility depends on direction and actual values; theoretical type promotion does not prove application range or precision.

**Treat defaults, absence, null, empty, and unknown separately.** A missing field can mean not captured, not applicable, not authorized, default behavior, or unknown. Null may be a value, deletion, or absence. Empty string, zero, and empty collection may be meaningful. Specify producer emission, reader interpretation, storage, validation, quality, and policy for each state.

**Version enums and code sets as governed semantics.** Adding a code can break exhaustive switches, metrics, policies, reports, and models even when the wire format accepts it. Define identifier, label, meaning, applicability interval, unknown behavior, mapping, grouping, deprecation, reservation, and consumer response. Test unexpected and future values.

**Protect identity and grain.** Changes to keys, deduplication identity, entity resolution, event identity, table grain, aggregation, or cardinality affect joins, retries, corrections, privacy, and consumer decisions. Model one-to-one, split, merge, and many-to-many mappings with applicability and correction rather than treating them as field renames.

**Make units and precision explicit.** Store currency, unit, scale, rounding, overflow, timezone, calendar, coordinate system, and measurement convention as contract obligations. A compatible numeric type can still change value through conversion or aggregation. Test boundaries and consumer tolerances from domain rules.

**Version time and history.** Distinguish event, processing, ingestion, valid, transaction, and observation time. Define zones, calendars, precision, intervals, late data, corrections, deletions, restatements, and retention. Historical rows or messages written under old semantics need the correct writer contract and reference data during replay.

**Define behavioral obligations.** For APIs, events, files, and tables, record operation, delivery, ordering, idempotency, duplication, retry, timeout, partial failure, pagination, snapshot consistency, error representation, side effects, acknowledgment, and correction. Structure can remain unchanged while behavior breaks consumers.

**Define quality and service as scoped commitments.** Bind completeness, validity, uniqueness, consistency, timeliness, freshness, latency, availability, support, incident, recovery, retention, and change notice to named populations, windows, exclusions, measurement points, clocks, and owners. A global adjective like “fresh” is not testable.

**Carry security and privacy obligations.** Record purpose, classification, owner, identity, access, field- and row-level policy, encryption, residency, retention, deletion, legal hold, audit, minimization, masking, and incident response. A new field can change classification and authorized consumers even when structurally optional.

**Design expand-migrate-contract.** First expand the authoritative producer or transformation so old and new forms are derivable and observable. Then migrate consumers by cohort with fixtures, support, telemetry, policy, replay, and acceptance. Finally contract obsolete forms and all enabling artifacts. Define entry, exit, stop, rollback, and expiry for each lifecycle state.

**Prefer one authoritative derivation.** Generate old and new representations from one governed semantic state or transformation. Independent old and new writes create partial failure, ordering, and meaning divergence. If separate implementations are necessary, define transaction identity, ordering, reconciliation, correction, authority, and bounded duration.

**Make transformations explicit and reversible where required.** Record source and target contract versions, field and code mappings, precision, loss, defaults, provenance, applicability, reference data, errors, and inverse behavior. Some transformations are intentionally lossy; authorize the loss, preserve source where required, and determine rollback feasibility before exposure.

**Migrate historical and in-flight data.** Inventory tables, files, topics, queues, caches, snapshots, backups, dead letters, retries, and replay logs. Bind old data to writer contract and transform at read, copy, replay, or rewrite time under versioned mappings. Reconcile population, identity, values, order, policy, lineage, and decisions.

**Test a compatibility matrix.** Exercise exact producer, consumer, serializer, validator, registry, transport, storage, and generated-code versions. Cover old-old, old-new, new-old, new-new, mixed deployment, stored data, malformed values, unknown fields, new enum codes, boundary numbers, missing and null values, errors, retries, and recovery.

**Use consumer-driven evidence carefully.** Consumer expectations and provider verification can expose actual interactions and states. Ensure critical consumers are represented, provider states are meaningful, data variability and policies are covered, and contracts do not merely encode outdated implementation details. Passing interactions do not prove unrepresented behavior.

**Use production-shaped fixtures.** Include common, boundary, malformed, rare, privacy-sensitive, high-volume, historical, late, corrected, deleted, unknown, and future-value cases. Give fixtures provenance, classification, minimization, version, expected result, and expiry. Synthetic examples avoid sensitive data but may miss real distribution and semantic edge cases.

**Align registry policy with contract policy.** Define subject or identity strategy, version allocation, compatibility mode and direction, approval, ownership, signatures, retention, deletion, replication, disaster recovery, and emergency override. Test exact registry behavior and clients. A permissive mode can admit breaking changes; an overly strict mode can block safe semantic evolution.

**Separate validation from authorization.** Schema, lint, compatibility, conformance, policy, quality, service, and consumer tests answer different questions. Passing all may still not authorize a semantic change or sunset. Record who may approve each obligation and residual risk.

**Observe deployed contract versions.** Instrument producers, consumers, datasets, messages, operations, contract identifiers, schema fingerprints, registry versions, transformation versions, policy decisions, errors, latency, and outcomes. Avoid high-cardinality exposure while preserving useful identities. Sampling and uninstrumented batch or offline work limit adoption claims.

**Trace contract versions through lineage.** Attach contract and semantic identities to dataset, job, run, event, interface, and consumer evidence. Test lineage coverage with known flows and replays. Lineage should support impact analysis, discrepancy diagnosis, policy, correction, recovery, and retirement—not merely visualization.

**Canary by consequence and representation.** Choose consumer, producer, data, operation, region, and workload cohorts that cover critical semantics without uncontrolled impact. Define control, duration, delayed cycles, countermetrics, divergence thresholds, expansion, pause, stop, rollback, and decision authority. A successful low-risk reader does not prove a high-consequence writer.

**Treat contract errors as part of migration.** Define how producers reject invalid input, consumers handle unknown data, validators fail, registries are unavailable, transformations quarantine records, retries behave, and operators correct defects. Preserve actionable diagnostics without leaking sensitive values. Test fail-open and fail-closed choices explicitly.

**Plan rollback around target-only meaning.** Once producers emit new codes, identities, precision, fields, or behaviors, old consumers may not represent them. Define whether rollback maps, quarantines, partitions, compensates, preserves target authority, or becomes unsafe after a point. Test stored state and external decisions, not only deployment reversal.

**Exercise recovery across versions.** Restore contracts, schemas, registries, signatures, producer and consumer builds, mappings, policies, data, messages, offsets, lineage, fixtures, documentation, and authority in dependency order. Verify historical writer schemas remain available and retired versions do not become authoritative.

**Prepare consumers and operators.** Provide migration guides, change examples, fixtures, generated artifacts, environments, credentials, policy, service, support, incident procedures, deadlines, and decision paths. Verify real builds and executions. Training and acknowledgment support migration but do not establish it.

**Govern exceptions as real architecture.** Name consumer, versions, obligations, reason, risk, compensating control, owner, support, cost, expiry, successor, evidence, and escalation. Exceptions must affect compatibility and retirement plans. Repeated extension indicates the target or migration strategy needs reconsideration.

**Signal deprecation and sunset.** Publish dates, successor, migration documentation, supported versions, changed obligations, support, exceptions, and contact through appropriate machine and human channels. Keep behavior consistent with declared state. Measure consumer action; elapsed time alone does not authorize contraction.

**Contract only after evidence.** Confirm new producer and consumer behavior, stored and replayed data, policy, service, support, recovery, rare cycles, partner use, caches, SDKs, and target-only meanings. Then stop old publication, reading, transformation, policy, and support in bounded order. Continue observing attempted use.

**Remove transition debt.** Delete or retire dual fields, schemas, aliases, mappings, adapters, compatibility branches, views, topics, endpoints, files, fixtures, credentials, policies, tests, documentation, monitors, capacity, and support that no longer serve an authorized purpose. Preserve only governed records needed for history or audit.

**Reserve obsolete identities.** Tombstone field numbers, enum codes, names, paths, subjects, schema fingerprints, endpoints, topics, contract versions, and product identities where reuse could awaken old code or reinterpret stored data. A reserved identifier is a safety control, not clutter.

**Test nonactivation.** Restore old producer and consumer builds, registry backups, cached schemas, infrastructure definitions, and recovery images in isolation. Reserved identifiers, revoked credentials, policy denial, removed routes, tombstones, and authority controls should prevent obsolete behavior from publishing or consuming as current.

**Measure contract migration outcomes.** Compare producer lead time, consumer breakage, incident rate, data quality, semantic defects, adoption, support toil, service, recovery, policy violations, transition debt, and user decisions with baseline. Count compatibility theater as failure: more contract files without trusted behavior is not improvement.

**Preserve a migration receipt.** Bind outcomes, baselines, identities, obligations, change classifications, direction matrix, exact versions, mappings, fixtures, tests, consumer evidence, policies, lineage, telemetry, exceptions, decisions, rollout, rollback, recovery, deprecation, sunset, contraction, retirement, nonactivation, outcomes, residual risk, dissent, and limitations.

## Definitions and Notation

Let a contract migration be:

`M = (O, B, I, S, P, C, Q, G, T, E, R, L)`.

`O` contains product purpose, producers, consumers, affected users and decisions, baseline burdens, desired outcomes, mandatory constraints, countermetrics, approval authority, and evidence horizon.

`B = (b_old, b_transition, b_target)` contains approved contract declarations and observed implementations for old, coexistence, and target states. A baseline binds contract, schema, registry, code, policy, fixtures, documentation, deployments, stored data, and evidence time.

`I` contains identities for contract, version, dataset, schema, dialect, fingerprint, message, operation, field, tag, enum code, metric, producer, consumer, implementation, fixture, conformance result, exception, and lifecycle decision.

`S` contains structural declarations and resolution. Define a directional compatibility claim:

`compatible(writer_v, reader_v, encoding, dialect, runtime, population, obligations)`.

The claim applies only to the named direction and scope. Reversing writer and reader or changing encoding can change the result.

`P` contains semantic and behavioral obligations. A semantic field definition is:

`field = (identity, concept, type, unit, precision, presence, null, default, codes, time, applicability, correction)`.

A field name and physical type are insufficient to determine meaning.

`C` contains producer, consumer, interface, transport, storage, transformation, compatibility envelope, and deployment combinations. A compatibility matrix `K` maps required writer-reader pairs to evidence:

`K[writer_v, reader_v, form, population] = result`.

`Q` contains data quality, service, performance, availability, delivery, recovery, support, pricing, measurement windows, exclusions, owners, and evidence.

`G` contains ownership, decision rights, change control, security, privacy, purpose, classification, access, residency, retention, deletion, legal hold, audit, policy, exceptions, and evidence custody.

`T` contains expand, consumer migration, contraction, transformations, dual publication, shadowing, canaries, cutover, rollback, correction, and authority. Lifecycle state is:

`proposed -> approved -> expanded -> migrating -> target_authoritative -> deprecated -> sunset -> retired -> closed`.

Urgent security or safety changes may skip normal states, but their authority, impact, remediation, and evidence remain explicit.

`E` contains declaration validation, schema resolution, conformance, consumer-driven tests, fixtures, registry results, policy tests, lineage, telemetry, replay, consumer decisions, incidents, outcomes, and limitations.

`R` contains risks, assumptions, dependency uncertainty, unsupported combinations, divergence, thresholds, pause and stop conditions, rollback limits, points of no return, dissent, and replanning triggers.

`L` contains adoption, deprecation, sunset, exceptions, transition debt, retirement, identifier reservation, archival writer schemas, nonactivation, evidence retention, and closure.

Every obligation `o` receives a migration disposition:

`move(o) -> preserve | change_approved | terminate_approved | unresolved`.

Any required obligation mapped to `unresolved` blocks target authority or contraction.

A contract change `c` is admissible only if:

`Admit(c) = owner and semantics and producer and consumer and policy_service and retirement`.

`owner` binds authority and outcome; `semantics` provides explicit preservation or approved change; `producer` proves required writer behavior; `consumer` proves required readers and decisions; `policy_service` covers governance, quality, service, and recovery; and `retirement` provides contraction and nonactivation. These are necessary gates in this model, not proof that every contract migration is safe.

A version number communicates intended change class but does not compute it:

`version = communicate(classification, baseline, policy)`.

Determining major, minor, patch, date, generation, or another scheme depends on the contract's declared public obligations and governance. SemVer syntax alone cannot classify semantic, policy, or service impact.

## Mechanisms, Invariants, or Proof Structure

The assurance argument moves from an observed contract baseline to accepted target behavior and removal of obsolete authority.

**Outcome gate.** Bind purpose, product, producers, consumers, affected decisions, baseline burden, desired result, mandatory constraints, owner, approval, evidence horizon, and reconsideration triggers.

**Identity gate.** Give contract, version, schema, dialect, fingerprint, message, operation, field, code, metric, producer, consumer, implementation, fixture, result, exception, and retirement stable identities.

**Configuration gate.** Version approved declarations, schemas, interface descriptions, registry state, generated code, fixtures, implementations, policies, documentation, stored data, deployed configuration, and observed behavior.

**Discovery gate.** Combine code, builds, registry access, gateways, brokers, subscriptions, queries, lineage, transfers, reports, models, identity, schedules, caches, support, recovery, interviews, and consumer confirmation.

**Obligation gate.** Enumerate purpose, identity, structure, encoding, semantics, grain, units, time, history, correction, behavior, delivery, ordering, errors, quality, service, security, privacy, support, change, recovery, cost, and closure.

**Change-classification gate.** Identify additions, removals, renames, types, constraints, defaults, presence, nulls, unknowns, codes, units, keys, grain, time, behavior, policy, quality, service, support, and lifecycle effects.

**Direction gate.** Define old-writer/new-reader, new-writer/old-reader, old-old, new-new, mixed deployment, stored-data, replay, encoding, dialect, runtime, and population requirements.

**Structural gate.** Test exact schema, serializer, validator, registry, generated-code, transport, storage, and reader/writer versions across boundary and malformed values.

**Semantic gate.** Version concepts, identity, grain, units, currencies, precision, codes, presence, nulls, time, history, correction, aggregation, applicability, and consumer interpretation.

**Behavior gate.** Verify delivery, ordering, idempotency, duplicates, retry, timeout, pagination, partial failure, errors, acknowledgments, side effects, replay, and correction.

**Quality gate.** Bind completeness, validity, uniqueness, consistency, timeliness, freshness, integrity, distributions, windows, exclusions, measurement points, clocks, owners, and remediation.

**Service gate.** Bind latency, availability, throughput, support, incidents, notice, retention, recovery-time, data-loss, and cost obligations by population and scenario.

**Policy gate.** Preserve purpose, classification, identity, access, field and row policy, encryption, residency, minimization, retention, deletion, legal hold, audit, incident, and exception controls.

**Transformation gate.** Record source and target versions, field and code mappings, defaulting, precision, loss, provenance, applicability, reference data, errors, inverse behavior, and correction.

**Historical gate.** Bind tables, files, topics, queues, caches, snapshots, backups, dead letters, retries, writer schemas, positions, transformations, replay, and reconciliation.

**Matrix gate.** Execute required producer-consumer-form-population combinations including old, new, mixed, stored, malformed, unknown, boundary, error, retry, policy, and recovery cases.

**Fixture gate.** Govern provenance, classification, minimization, contract version, coverage, expected decisions, generated values, mutation, freshness, and expiry.

**Consumer-evidence gate.** Verify represented expectations, provider states, actual builds, production-shaped executions, downstream decisions, rare cycles, partner use, caches, and recovery.

**Registry gate.** Test identity strategy, version allocation, compatibility mode and direction, approval, signatures, retention, replication, recovery, deletion, emergency override, and exact clients.

**Deployment gate.** Compare contract declarations, registry entries, generated artifacts, producer output, consumer input, policies, documentation, and actual deployed versions for consistency.

**Lineage gate.** Propagate stable contract and semantic identities through datasets, jobs, runs, events, interfaces, transformations, consumers, replays, corrections, and retirements.

**Telemetry gate.** Observe producer, consumer, contract, schema, fingerprint, operation, transformation, policy, error, latency, adoption, decision, and outcome with privacy and cardinality controls.

**Exposure gate.** Bound producer, consumer, data, operation, region, and workload cohorts; control side effects, duration, countermetrics, divergence, expansion, pause, stop, rollback, and authority.

**Error gate.** Test invalid input, unknown values, registry unavailability, validator failure, transformation quarantine, retry, operator correction, fail-open, fail-closed, and diagnostic safety.

**Rollback gate.** Treat target-only fields, codes, meanings, precision, state, and external decisions through mappings, quarantine, partitioned authority, compensation, or an explicit point of no return.

**Recovery gate.** Restore contracts, schemas, registries, signatures, builds, mappings, policy, data, messages, offsets, lineage, fixtures, documentation, and authority in dependency order.

**Readiness gate.** Prepare producers, consumers, owners, platform, security, privacy, support, operations, partners, documentation, credentials, environments, procedures, capacity, and decisions.

**Exception gate.** Bind consumer, versions, obligations, reason, risk, controls, owner, support, cost, expiry, successor, evidence, escalation, and effect on contraction.

**Lifecycle gate.** Publish expansion, supported versions, deprecation, sunset, successor, changes, migration guidance, support, exceptions, and contact through machine and human channels.

**Contraction gate.** Prove producer and consumer acceptance, historical replay, policy, service, recovery, rare use, partner use, cache closure, target-only meaning, and exception closure before removal.

**Debt gate.** Remove obsolete fields, schemas, mappings, adapters, compatibility branches, views, topics, endpoints, files, fixtures, credentials, policies, tests, docs, monitors, capacity, and support.

**Reservation gate.** Tombstone field numbers, codes, names, paths, subjects, fingerprints, endpoints, topics, versions, and product identities whose reuse could corrupt stored data or awaken old code.

**Nonactivation gate.** Restore old producers, consumers, registries, cached schemas, deployments, and recovery images in isolation; verify reservation, trust removal, policy denial, route removal, and authority controls contain them.

**Outcome gate.** Compare change lead time, breakage, incidents, quality, semantic defects, adoption, support, service, recovery, policy violations, debt, and user decisions with baseline.

**Receipt gate.** Bind outcomes, baselines, identities, obligations, classifications, matrices, versions, mappings, fixtures, tests, consumers, policies, lineage, telemetry, exceptions, rollout, rollback, recovery, lifecycle, contraction, reservation, nonactivation, outcomes, risk, dissent, and limitations.

### Executable evidence: contract-change admission

The following program classifies ten invented contract changes against six mandatory gates.

<!-- bijux-verify: {"id":"contract-change-admission","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"changes=10\nadmissible=4\nmissing_owner=1\nsemantic_gap=1\nproducer_break=1\nconsumer_unready=1\npolicy_service_gap=1\nmissing_retirement=1\ncontract_forms=8\naffected_products=7\nlifecycle_states=5\nmigration_receipts=10\ndecision_events=10\n","stderr":""}} -->
```python
changes = [
    {"form": "event", "products": {"orders"}, "state": "expanded", "owner": True, "semantics": True, "producer": True, "consumer": True, "policy_service": True, "retirement": True},
    {"form": "api", "products": {"customer", "orders"}, "state": "migrating", "owner": True, "semantics": True, "producer": True, "consumer": True, "policy_service": True, "retirement": True},
    {"form": "table", "products": {"finance"}, "state": "authoritative", "owner": True, "semantics": True, "producer": True, "consumer": True, "policy_service": True, "retirement": True},
    {"form": "file", "products": {"partner"}, "state": "retired", "owner": True, "semantics": True, "producer": True, "consumer": True, "policy_service": True, "retirement": True},
    {"form": "metric", "products": {"risk"}, "state": "draft", "owner": False, "semantics": True, "producer": True, "consumer": True, "policy_service": True, "retirement": True},
    {"form": "feature", "products": {"risk", "customer"}, "state": "expanded", "owner": True, "semantics": False, "producer": True, "consumer": True, "policy_service": True, "retirement": True},
    {"form": "stream", "products": {"inventory"}, "state": "migrating", "owner": True, "semantics": True, "producer": False, "consumer": True, "policy_service": True, "retirement": True},
    {"form": "reference", "products": {"catalog"}, "state": "authoritative", "owner": True, "semantics": True, "producer": True, "consumer": False, "policy_service": True, "retirement": True},
    {"form": "event", "products": {"orders", "partner"}, "state": "migrating", "owner": True, "semantics": True, "producer": True, "consumer": True, "policy_service": False, "retirement": True},
    {"form": "table", "products": {"finance", "catalog"}, "state": "retired", "owner": True, "semantics": True, "producer": True, "consumer": True, "policy_service": True, "retirement": False},
]

def evaluate(change):
    if not change["owner"]:
        return "missing_owner"
    if not change["semantics"]:
        return "semantic_gap"
    if not change["producer"]:
        return "producer_break"
    if not change["consumer"]:
        return "consumer_unready"
    if not change["policy_service"]:
        return "policy_service_gap"
    if not change["retirement"]:
        return "missing_retirement"
    return "admissible"

results = [evaluate(change) for change in changes]
print(f"changes={len(changes)}")
for outcome in ["admissible", "missing_owner", "semantic_gap", "producer_break", "consumer_unready", "policy_service_gap", "missing_retirement"]:
    print(f"{outcome}={results.count(outcome)}")
print(f"contract_forms={len({change['form'] for change in changes})}")
print(f"affected_products={len(set().union(*(change['products'] for change in changes)))}")
print(f"lifecycle_states={len({change['state'] for change in changes})}")
print(f"migration_receipts={len(changes)}")
print(f"decision_events={len(results)}")
```

The output reports ten changes, four admissible and one of each declared failure, eight contract forms, seven affected products, five lifecycle states, ten receipts, and ten decisions.

The evidence is deliberately narrow. Invented Booleans, labels, and sets establish deterministic gate order and counts only. They do not establish owner authority, semantic correctness, producer compatibility, consumer readiness, policy or service conformance, retirement completeness, schema safety, rollback, recovery, or stakeholder value. Production assurance requires approved baselines, exact schemas and implementations, historical populations, compatibility matrices, fixtures, producer and consumer verification, registry and policy tests, lineage, telemetry, canaries, replay, recovery exercises, adoption, contraction, and nonactivation evidence.

## Alternatives and Trade-Offs

**One-time breaking change.** Transitional code and dual support are minimized. Consumer coordination, downtime, blast radius, historical compatibility, and rollback burden increase.

**Expand-migrate-contract.** Producer and consumer change can be bounded and observed. Duplicate forms, adapters, support, policy, ambiguity, and duration increase; contraction must be funded.

**New contract identity.** Changed meaning and lifecycle are unmistakable, and old consumers cannot silently attach. Discovery, migration, duplication, mappings, and portfolio complexity increase.

**New version of one contract.** Continuity and discovery are simpler. Major semantic or product changes can be obscured, and compatibility claims require careful scoping.

**Provider-driven compatibility.** Producer implementation and central registry policy can move quickly. Unrepresented consumer assumptions and decisions remain hidden.

**Consumer-driven verification.** Actual interaction expectations influence provider validation. Consumer coverage can be incomplete, tests can encode implementation accidents, and cross-consumer coherence remains a product decision.

**Strict compatibility mode.** Many structural breaks are prevented early. Safe semantic evolution can be blocked, while structurally compatible semantic breaks still pass.

**Permissive compatibility mode.** Teams can evolve diverse contracts and correct historical mistakes. Consumer risk and governance burden rise.

**Schema-on-write migration.** Invalid forms are rejected before publication, and producer accountability is clear. Flexibility, late-binding use, and recovery from novel data may decrease.

**Schema-on-read migration.** Historical data can retain writer forms and readers evolve independently. Every consumer bears resolution complexity, and unsupported old schemas can strand data.

**Rewrite stored history.** Target consumers and operations see one representation. Cost, custody, corruption risk, provenance, rollback, and reinterpretation increase.

**Transform at read or replay.** Original evidence remains and version-specific mapping can be explicit. Repeated cost, latency, mapping availability, and runtime complexity persist.

**Dual fields in one payload.** Consumers can migrate incrementally with one transport. Payload growth, contradictory values, policy duplication, and forgotten contraction are risks.

**Parallel topics, tables, or endpoints.** Authority and lifecycle can be separated clearly. Duplication, routing, ordering, cost, discovery, and synchronization grow.

**Default new fields.** Old data can parse without rewrite. A convenient default can invent false meaning and hide missing data.

**Require explicit presence.** Missing meaning remains visible and correctable. Old producers and stored records may fail until migrated.

**Reserve removed identities forever.** Stored data and old code cannot reinterpret reuse. Namespace capacity and cosmetic cleanliness are reduced.

**Reuse identifiers after observation.** Schemas may appear compact. Rare or restored consumers and historical payloads can be corrupted; evidence burden is extreme.

**Semantic versioning.** Change intent is communicated through familiar version classes. Multi-dimensional data-contract impact and pre-release behavior may not map cleanly.

**Date or generation versioning.** Order and provenance can be obvious. Compatibility impact is not communicated without separate classification.

**Central contract governance.** Identity, tooling, compatibility, evidence, and policy can be consistent. Review queues may lack domain meaning and slow safe change.

**Federated contract ownership.** Producers and consumers stay close to semantics and outcomes. Shared identity, interoperability, global policy, and cross-domain obligations need common governance.

## Failure Modes and Misconceptions

1. **“The schema is the contract.”** Purpose, semantics, behavior, quality, service, policy, support, and lifecycle remain.
2. **“The registry entry is the deployed truth.”** Producers and consumers may run different artifacts or configuration.
3. **“One version identifies every artifact.”** Contract, schema, code, registry, policy, fixtures, and deployments differ.
4. **“Changing a path creates a new contract.”** Logical identity can persist across transport and location.
5. **“Keeping a path preserves contract identity.”** Meaning can change incompatibly under the same endpoint.
6. **“Backward compatible is unambiguous.”** Writer, reader, direction, encoding, runtime, and population must be named.
7. **“Parser success proves compatibility.”** Application range, meaning, behavior, policy, and decisions can fail.
8. **“Wire safe means lossless.”** Unknowns, conversions, JSON, generated code, and application models can lose data.
9. **“Old writer to new reader is enough.”** New writer to old reader and mixed deployment may also be required.
10. **“Schema compatibility covers stored data.”** Actual historical values, writer schemas, and encodings determine resolution.
11. **“Optional means harmless.”** Absence, null, default, empty, unknown, policy, and business meaning can differ.
12. **“A default repairs missing meaning.”** It can fabricate a valid-looking false value.
13. **“Null and absent are interchangeable.”** They may encode deletion, unknown, inapplicable, or unauthorized states.
14. **“Unknown fields always survive.”** JSON conversion, application mapping, and reserialization can discard them.
15. **“Adding an enum value is safe.”** Exhaustive branches, reports, metrics, models, and policies can fail.
16. **“Removed field identifiers can be reused later.”** Stored data and restored code can reinterpret them.
17. **“Renaming preserves meaning.”** Concepts, identity, history, and applicability may change.
18. **“Same name and type preserve meaning.”** Units, precision, time, codes, and correction may differ.
19. **“Numeric widening is always safe.”** Applications, databases, generated code, and downstream conversions may narrow.
20. **“Floating values can replace decimal money.”** Precision, rounding, aggregation, and decisions can change.
21. **“UTC conversion solves time.”** Business zones, calendars, valid intervals, cutoffs, and ambiguity remain.
22. **“A new key is merely a field change.”** Joins, deduplication, privacy, corrections, and cardinality change.
23. **“Schema validators agree.”** Dialect, vocabulary, formats, references, and unknown keywords can differ.
24. **“Canonical fingerprints prove semantic identity.”** Documentation and application meaning may be excluded.
25. **“Generated code is the contract.”** Generator and runtime choices add another versioned interpretation.
26. **“Independent dual publication remains synchronized.”** Partial failure, ordering, and semantic drift create divergence.
27. **“An adapter is a neutral mapping.”** It owns loss, defaults, policy, errors, and lifecycle.
28. **“Historical rewrite is just maintenance.”** Provenance, custody, rollback, legal evidence, and meaning can change.
29. **“Replay uses the current contract.”** Historical data requires the writer contract and applicable reference state.
30. **“A row count proves migration parity.”** Keys, values, order, history, deletes, and decisions can differ.
31. **“Provider tests represent every consumer.”** Hidden assumptions and unmodeled states remain.
32. **“Consumer-driven tests prove the full contract.”** Only represented interactions, consumers, states, and data are covered.
33. **“Synthetic fixtures are representative.”** Real distributions, rare codes, privacy, scale, and historical defects may differ.
34. **“Production examples are safe fixtures.”** They can leak sensitive data and become stale or ungoverned.
35. **“Strict registry compatibility prevents all breaks.”** Semantic, behavioral, service, and policy changes can pass.
36. **“Permissive registry mode makes teams independent.”** Consumers absorb unbounded coordination and risk.
37. **“Validation authorizes change.”** Product, policy, risk, and lifecycle decisions require named authority.
38. **“A conformance result is timeless.”** Versions, data, environments, policies, and implementations change.
39. **“Lineage automatically finds every consumer.”** Missing instrumentation and unstable identities create blind spots.
40. **“Telemetry proves adoption.”** Sampling, batch work, caches, partners, and disaster clients can be invisible.
41. **“A small canary proves a contract safe.”** High-consequence writers, rare values, scale, and delayed cycles remain.
42. **“Fail open always protects availability.”** Invalid or unauthorized data can corrupt downstream decisions.
43. **“Fail closed always protects correctness.”** Lost critical data and unsafe retries can cause harm.
44. **“Rollback is deployment reversal.”** New fields, codes, meanings, stored data, and decisions require treatment.
45. **“Registry backup proves recovery.”** Schemas, signatures, builds, mappings, policies, offsets, data, and authority must align.
46. **“Acknowledgment means consumer migration.”** The deployed build and real decision path may remain old.
47. **“Deprecation or sunset authorizes contraction.”** Consumer, history, recovery, exception, and risk evidence must pass.
48. **“Old fields can remain forever at no cost.”** Payload, policy, code, support, ambiguity, and attack surface grow.
49. **“Deleting the schema closes the version.”** Caches, stored data, generated code, backups, and identifiers can reactivate.
50. **“More contract files mean better contracts.”** Trusted behavior and outcomes, not declaration count, establish value.

## Worked Examples

### Example 1

An order producer adds an optional `currency` field with a default of USD. Old records include CAD amounts whose currency was carried in another table. The new schema parses, but the default invents false meaning. Migration instead joins governed historical currency, represents unknown explicitly, versions applicability, and tests consumer decisions.

### Example 2

An Avro writer changes an integer to a long and passes schema resolution. A consumer maps the result into a 32-bit application type and fails only at boundary values. The compatibility matrix includes actual runtime models and boundary fixtures rather than treating wire promotion as end-to-end proof.

### Example 3

A Protocol Buffers field is removed and its number reused for a new concept. Old binary payloads then decode historical value as the new field. The migration restores the original reservation, assigns a new number, tests binary, JSON, stored, and relay paths, and tombstones both old name and number.

### Example 4

Two JSON Schema validators disagree about `format` and unevaluated properties because they use different dialect and vocabulary support. The contract declares the 2020-12 dialect, required vocabularies, reference behavior, validator versions, and expected output before compatibility evidence is accepted.

### Example 5

An API deprecation header and sunset date reach interactive clients, but a monthly batch and an old mobile build remain. Credential, operation, and version telemetry plus a bounded probe expose them. Each receives successor artifacts and an owned decision before the endpoint contracts.

### Example 6

An event producer emits old and new money fields from separate implementations. A timeout updates only one form. Reconciliation catches contradictory values; the design moves to one authoritative money state and derives both representations through a versioned mapping with declared rounding.

### Example 7

Consumer-driven tests cover three services but omit a regulatory extract. Provider verification is green while the extract fails on a new enum. The consumer inventory, code-set tests, and quarterly-cycle evidence become explicit gates; passing represented pacts is no longer treated as universal compatibility.

### Example 8

Historical feature data is replayed using the current code set rather than the one valid when events occurred. Model outputs drift. The replay binds writer schema, semantic version, reference-data interval, transformation, and policy to each historical segment and records intentional differences.

### Example 9

A target contract introduces a deletion state that old consumers cannot represent. Canary evidence passes for reads, but full rollback would resurrect deleted records. The authority model partitions the affected population and establishes a point after which roll-forward correction is safer.

### Example 10

After contraction, an isolated recovery test restores an old registry, cached schema, producer image, and topic route. Reserved identifiers, revoked credentials, tombstones, and policy denial prevent publication. The test discovers an obsolete compatibility adapter and fixture package, which are removed before closure.

## Cross-Program Connections

- [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) provides operation contracts, OpenAPI, versioning, compatibility, errors, gateways, client migration, deprecation, sunset, canaries, and endpoint closure.
- [Data Engineering](../../19-data-engineering/ROADMAP.md) implements schema evolution, registry integration, transformations, replay, historical migration, quality, lineage, telemetry, reconciliation, and pipeline contraction.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md) supplies contract registries, policy gates, CI checks, code generation, deployment evidence, consumer catalogs, observability, support, recovery, and paved migration workflows.
- [Database Engineering](../../18-database-engineering/ROADMAP.md) grounds types, constraints, schemas, tables, views, transactions, stored data, compatibility, migration, backup, restore, and schema retirement.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) explains ordering, duplication, delivery, idempotency, partial failure, consistency, clocks, retries, convergence, rollback, and replay.
- [Software Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) contributes contract, compatibility, property, mutation, boundary, integration, end-to-end, regression, and evidence-quality testing.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) governs identities, authorization, sensitive fields, schemas, suppliers, failures, incidents, retention, recovery, and secure closure.
- [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md) provides public interfaces, seams, adapters, parallel change, architectural fitness, evolutionary design, and decision records.
- [Large-Scale Data Systems Engineering](../../21-large-scale-data-systems-engineering/ROADMAP.md) supplies serialization, storage, logs, schemas, streaming, distributed state, scaling, metadata, and recovery mechanics.
- [Systems Engineering](../../26-systems-engineering/ROADMAP.md) supplies configuration items, controlled baselines, interface coordination, transition, readiness, verification, validation, risk, lifecycle, and disposal.

## References

1. Bitol, [Open Data Contract Standard](https://bitol-io.github.io/open-data-contract-standard/latest/), schema, quality, service, roles, support, pricing, team, and infrastructure obligations.
2. JSON Schema, [Specification](https://json-schema.org/specification), current dialect, core and validation vocabularies, meta-schemas, outputs, and migration information.
3. Apache Avro, [Specification](https://avro.apache.org/docs/current/specification/), writer and reader schemas, resolution, defaults, aliases, unions, logical types, encodings, canonical form, and fingerprints.
4. Protocol Buffers, [Proto3 Language Guide](https://protobuf.dev/programming-guides/proto3/), field numbers, unknown fields, updating message types, reserved identities, enums, binary, JSON, and wire compatibility.
5. OpenAPI Initiative, [OpenAPI Specification](https://spec.openapis.org/oas/latest.html), HTTP operations, parameters, schemas, responses, security, extensions, versions, and deprecation.
6. AsyncAPI Initiative, [Specification](https://www.asyncapi.com/docs/reference/specification/latest), asynchronous channels, operations, messages, servers, security, and bindings.
7. Pact, [How Pact Works](https://docs.pact.io/getting_started/how_pact_works), consumer expectations, interaction contracts, provider states, publication, and provider verification.
8. Semantic Versioning, [Semantic Versioning 2.0.0](https://semver.org/), public API declaration, version precedence, compatibility intent, deprecation, and dependency guidance.
9. Danilo Sato, [Parallel Change](https://martinfowler.com/bliki/ParallelChange.html), expand-migrate-contract interface evolution and contraction risk.
10. IETF, [RFC 9745: The Deprecation HTTP Response Header Field](https://www.rfc-editor.org/rfc/rfc9745.html), lifecycle signaling, deprecation dates, documentation links, and unchanged resource behavior.
11. IETF, [RFC 8594: The Sunset HTTP Header Field](https://www.rfc-editor.org/rfc/rfc8594.html), communicating expected future unavailability of resources.
12. OpenLineage, [Object Model](https://openlineage.io/docs/spec/object-model/), dataset, job, run, event, namespace, name, and facet identities.
13. Open Policy Agent, [Policy Language](https://www.openpolicyagent.org/docs/policy-language), structured policy decisions, inputs, rules, tests, and runtime context.
14. OpenTelemetry, [Specification](https://opentelemetry.io/docs/specs/otel/), signals, resources, context, semantic conventions, sampling, compatibility, and versioning.
15. NASA, [Configuration Management](https://www.nasa.gov/reference/6-5-configuration-management/), configuration identity, baselines, change control, accounting, verification, audits, and product-information consistency.
16. NASA, [Product Transition](https://www.nasa.gov/reference/5-5-product-transition/), product, site, user, operator, documentation, support, acceptance, and transition work products.

## Exercises

### Exercise 1

Design a contract migration for an order event that replaces local money and status fields with governed types. Include outcomes, baselines, identities, obligations, change classifications, compatibility directions, dialects, encodings, mappings, producers, consumers, history, and closure.

### Exercise 2

Build a compatibility matrix and fixture portfolio for Avro, Protocol Buffers binary and JSON, JSON Schema, an HTTP API, and stored table data. Cover versions, runtimes, defaults, presence, nulls, unknowns, enums, identifiers, numbers, time, malformed data, errors, and consumer decisions.

### Exercise 3

Specify expand-migrate-contract execution for producers and consumers. Include authoritative derivation, transformations, dual forms, registry policy, consumer-driven tests, lineage, telemetry, canaries, quality, service, policy, errors, and stop conditions.

### Exercise 4

Design historical replay, rollback, and recovery for a contract that adds target-only codes, changes identifiers, and corrects event time. Cover writer schemas, stored messages, positions, mappings, reference data, lineage, policy, consumers, external decisions, and points of no return.

### Exercise 5

Write exception, deprecation, sunset, contraction, identity-reservation, nonactivation, outcome, and receipt requirements for a contract portfolio. Include cached, batch, partner, rare, restored, and undocumented consumers plus all transitional artifacts.

## Answers to the Exercises

### Answer 1

State the product purpose, affected decisions, owner, desired outcome, baseline burden, constraints, evidence horizon, and approval. Give the logical contract, old and target versions, schemas, fingerprints, fields, codes, producers, consumers, implementations, fixtures, results, and lifecycle decisions stable identities. Enumerate structure, encoding, identity, grain, decimal precision, currency, status meaning, presence, nulls, defaults, event and valid time, history, correction, delivery, ordering, errors, quality, service, policy, support, recovery, and closure obligations. Classify each change structurally, semantically, behaviorally, historically, operationally, and by consumer effect. Define old-writer/new-reader and new-writer/old-reader requirements for every encoding and runtime. Use one authoritative money and status state to derive old and new forms. Version mappings and loss. Discover direct, transitive, stored, batch, partner, cached, and recovery consumers. Contract only after replay, consumer, policy, recovery, and nonactivation evidence passes.

### Answer 2

List exact contract, schema, serializer, validator, registry, generator, runtime, transport, storage, producer, and consumer versions. Test old-old, old-new, new-old, new-new, mixed deployment, stored payloads, relay and reserialization, and historical replay. Include minimum, maximum, overflow, decimal, absent, null, default, empty, unknown fields, unknown enum codes, removed and reserved identifiers, aliases, unions, logical types, references, dialect vocabularies, malformed content, error behavior, retries, and policy decisions. For Protocol Buffers, separate binary, JSON, and text effects; for Avro, preserve writer schemas and actual values; for JSON Schema, pin dialect, vocabularies, references, and format assertions; for APIs, test operation, behavior, authentication, errors, and side effects; for tables, test types, constraints, grain, time, and stored history. Govern fixture provenance, classification, minimization, version, expected decision, and expiry. Record evidence scope and uncovered combinations.

### Answer 3

Expand the authoritative producer or transformation so old and new forms derive from one governed semantic state; if separate publication remains, define transaction identity, ordering, reconciliation, correction, and bounded duration. Version source and target contracts, mappings, defaults, loss, errors, and inverse behavior. Configure registry identity, compatibility direction, approval, signatures, recovery, and override. Publish fixtures, generated artifacts, environments, credentials, support, and guides. Verify critical consumer expectations and provider states without assuming they cover all use. Attach contract identities to lineage and telemetry; observe producer, consumer, schema, fingerprint, operation, transformation, policy, errors, service, and decisions. Canary representative producer, consumer, data, operation, and workload cohorts. Enforce quality, service, security, privacy, retention, and deletion. Stop on semantic divergence, unknown consumers, invalid policy, service regression, unrecoverable target-only state, or failed rollback.

### Answer 4

Bind each stored table, file, topic, queue, cache, snapshot, backup, dead letter, and retry to its writer contract, encoding, position, semantic version, mapping, reference data, policy, and lineage. Transform at read, replay, copy, or rewrite time according to explicit provenance and loss. Reconcile population, identity, values, ordering, time, deletes, corrections, policies, and consumer decisions. For target-only codes, define old-consumer unknown behavior, mapping or quarantine, affected decisions, and authority. For changed identifiers, model one-to-one, split, merge, collision, applicability, and correction. Preserve original event time and separately record processing and migration time. Test rollback of new data and external decisions; partition authority or establish a point after which roll-forward is safer. Recover contracts, registries, signatures, builds, mappings, schemas, policy, data, offsets, lineage, fixtures, docs, and authority together, while keeping historical writer schemas available.

### Answer 5

Give each exception consumer, versions, obligations, reason, risk, controls, owner, support, cost, expiry, successor, evidence, escalation, and effect on contraction. Publish deprecation date, sunset, successor, changed obligations, migration guide, artifacts, support, exceptions, and contact through contract, registry, interface, and human channels. Observe actual versions and decisions across daily, close, partner, rare, batch, cached, and recovery cycles. Contract old publication, reading, transformations, policies, and support only when those consumers, stored data, target-only meanings, recovery, and exceptions close. Remove fields, schemas, aliases, mappings, adapters, branches, views, topics, endpoints, files, fixtures, credentials, policies, tests, docs, monitors, capacity, and support. Reserve tags, codes, names, paths, subjects, fingerprints, and versions. Restore old builds and registries in isolation to test denial. Compare breakage, incidents, quality, semantic defects, adoption, toil, service, recovery, policy, debt, and decisions with baseline, and bind all evidence, decisions, risk, dissent, and limitations in the receipt.
