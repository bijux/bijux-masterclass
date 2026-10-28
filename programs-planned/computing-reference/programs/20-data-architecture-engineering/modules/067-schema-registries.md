---
module_id: DARCH-067
program: Data Architecture Engineering
level: 2
module_number: 67
title: Schema Registries
status: complete
last_verified: 2026-09-03
---

# Schema Registries

## One-Page Review

### Governing question

How should an organization identify, validate, version, distribute, evolve, operate, and retire machine-readable schemas so producers and consumers can exchange data safely without mistaking structural compatibility for semantic or behavioral compatibility?

### Essential definitions

- A **schema** is a machine-readable declaration of permitted representation structure, types, constraints, references, and annotations in a particular language and dialect.
- A **data contract** adds producer and consumer responsibilities, meaning, quality, service levels, policy, ownership, and lifecycle that a schema alone usually cannot express.
- A **schema registry** is a governed service that stores immutable schema artifacts and versions, assigns and resolves identifiers, applies validation and compatibility policy, records metadata and provenance, and supports controlled distribution and lifecycle.
- An **artifact** is a governed registry object such as an Avro schema, Protocol Buffers file, JSON Schema document, OpenAPI description, or AsyncAPI document.
- An **artifact version** is an immutable historical state of an artifact. Labels such as `latest`, `candidate`, or `production` are mutable pointers and are not version identities.
- A **subject**, **group**, or **namespace** is a registry-specific ownership and compatibility boundary. Its name does not necessarily identify schema content.
- A **global identifier** identifies a stored registry version or content object according to one registry's rules; it is not automatically portable across regions or products.
- A **fingerprint** is a digest over defined bytes or a canonical form. It supports comparison only when algorithm, canonicalization, dialect, and scope are known.
- A **writer schema** describes the representation written by a producer; a **reader schema** describes the view requested by a consumer.
- **Backward compatibility** commonly asks whether a new reader can consume data written under an older schema; **forward compatibility** commonly asks whether an old reader can consume data written under a newer schema.
- **Full compatibility** requires both directions under a stated format-specific rule. **Transitive** compatibility compares a candidate with every relevant prior version rather than only the latest.
- A **schema reference** is a typed dependency from one artifact version to another resolvable artifact version or identifier.
- **Registration** creates or discovers an artifact version after validation and policy checks; **resolution** retrieves the correct immutable schema and dependency closure for an identifier.

### Central model, mechanism, or theorem

Represent a governed registry capability as:

`R = (I, A, V, F, D, C, P, M, S, O, L)`

where `I` is identity and namespaces, `A` artifacts, `V` immutable versions, `F` formats and dialects, `D` dependency graphs, `C` compatibility and validation, `P` promotion policy, `M` metadata and provenance, `S` security and supply-chain controls, `O` operation and recovery, and `L` lifecycle closure. A registration decision is valid only relative to a named subject, format, dialect, candidate content, dependency closure, comparison set, compatibility direction, policy version, and effective time. Passing that decision proves neither semantic equivalence nor consumer readiness.

### Critical invariants

- Every stored version is immutable, retrievable by durable identity, attributable to a source, and linked to its exact format and dialect.
- Namespace identity, artifact identity, version identity, content identity, and mutable aliases remain distinct.
- Compatibility direction is stated from writer and reader perspectives; `backward` is never treated as an unqualified synonym for safe.
- Compatibility is evaluated using the selected schema language's rules, not a universal field-difference heuristic.
- Latest-only and transitive comparison sets are explicit and reproducible.
- References resolve to immutable versions, and registration, promotion, export, replication, and recovery preserve the dependency closure.
- A successful schema check does not waive semantic, quality, privacy, authorization, operational, or business-behavior review.
- Producers do not silently create production schemas through runtime auto-registration unless an explicitly accepted policy permits it.
- Wire identifiers and envelopes are versioned contracts; unknown identifiers fail predictably without corrupt interpretation.
- Caches have bounded staleness, authorization behavior, integrity checks, eviction policy, and a declared response to registry unavailability.
- Replication preserves identity or records deterministic translation; failover never guesses which content an identifier denotes.
- Deprecation and retirement identify active producers, consumers, stored data, generated code, references, replay paths, and recovery dependencies before removal.

### Common failures

Common failures include using `latest` in reproducible jobs; equating a subject name with content identity; hashing noncanonical text and calling it semantic identity; applying Avro rules to Protobuf or JSON Schema; checking only the most recent version; ignoring references; reusing deleted Protobuf field numbers; treating optionality as identical across formats; allowing every runtime to auto-register; promoting before consumers activate; trusting a green compatibility check as business safety; embedding an identifier without its registry authority; operating an unbounded cache; failing closed for every transient lookup or failing open with stale unauthorized content; replicating content without stable IDs; deleting versions needed to read history; and logging sensitive schemas or payload examples.

### Compact example

A subject has an accepted record schema with required `order_id: string` and `amount: long`. Candidate v2 adds `currency: string` with default `USD`; a simplified policy accepts it in both directions. Candidate v3 changes `amount` to `string` and adds required `status` without a default; the same policy reports two backward issues and one forward issue and rejects it. Executable evidence confirms the invented bookkeeping and three distinct fingerprints. It does not implement or validate Avro, Protobuf, JSON Schema, canonicalization, serialization, references, semantic compatibility, or production registry behavior.

### Connections

[DARCH-017](017-event-schemas-and-information-models.md), [DARCH-019](019-model-versioning.md), [DARCH-027](027-producer-and-consumer-contracts.md), [DARCH-036](036-change-data-capture-architecture.md), [DARCH-061](061-metadata-architecture.md), [DARCH-062](062-metadata-harvesting-and-synchronization.md), and [DARCH-066](066-semantic-interoperability.md) establish the modeling, contract, metadata, and meaning foundations. [DARCH-068](../ROADMAP.md) next develops data catalog architecture.

## Governing Question

Distributed systems must interpret data after the producer has deployed, while consumers upgrade at different times, events remain in logs, files wait in object stores, replicas fail over, and code generators change. A schema copied into source repositories cannot by itself answer which version wrote a record, whether dependencies are intact, which evolution policy applied, or who approved production use.

The governing question is therefore not merely where to store schema text. It is how to make representation agreements identifiable, immutable, resolvable, reviewable, and operable across autonomous producers and consumers while preserving format semantics and historical evidence. A useful registry is a control plane for schema artifacts, not the owner of all domain meaning and not a substitute for consumer testing.

## Why This Matters

The [Apache Avro specification](https://avro.apache.org/docs/1.12.0/specification/) defines schemas for primitive and complex types, binary encoding, writer and reader schemas, schema resolution, aliases, defaults, logical types, parsing canonical form, and fingerprints. Avro demonstrates why compatibility depends on the relationship between the schema that wrote data and the schema used to read it. The text of a record schema is not merely documentation; it participates in decoding.

The [Protocol Buffers proto3 guide](https://protobuf.dev/programming-guides/proto3/) assigns numeric tags to fields in the binary wire format and warns that deleted field numbers and names should be reserved. It distinguishes binary wire-safe, conditionally safe, and unsafe changes and separately discusses JSON mapping. A rename can be binary-compatible because the tag remains stable while still breaking JSON or application code. Registry policy must therefore know the representation and usage surface being protected.

[JSON Schema Core](https://json-schema.org/draft/2020-12/json-schema-core.html) defines JSON Schema documents, dialects, vocabularies, identifiers, references, dynamic references, annotations, validation outcomes, and bundling. [JSON Schema Validation](https://json-schema.org/draft/2020-12/json-schema-validation.html) defines assertion and annotation keywords for structural constraints and the treatment of formats. A registry cannot responsibly label content only `JSON Schema`; it must preserve dialect, vocabulary expectations, reference behavior, and validation policy.

The [OpenAPI Specification 3.1.1](https://spec.openapis.org/oas/v3.1.1.html) describes HTTP APIs, operations, parameters, request and response bodies, security, links, callbacks, webhooks, and Schema Objects aligned with a JSON Schema dialect. An OpenAPI document is a graph of interface contracts rather than a single message record. Compatibility analysis must consider operation behavior, media types, status codes, security, and client generation as well as schemas.

The [AsyncAPI Specification 3.0.0](https://www.asyncapi.com/docs/reference/specification/v3.0.0) models asynchronous APIs using channels, operations, messages, bindings, correlation, security, and reusable components. Its artifacts can refer to message payload schemas but also capture interaction structure and protocol concerns. Storing only extracted payload shapes loses material contract context.

The [CloudEvents 1.0.2 specification](https://github.com/cloudevents/spec/blob/ce@v1.0.2/cloudevents/spec.md) defines event context attributes such as `id`, `source`, `type`, `subject`, `time`, and `dataschema`. A `dataschema` URI can identify the schema governing `data`, but changing the schema does not necessarily change the event `type`, and changing an event's semantics may require a new type even when shape stays compatible. Registry identity and event identity serve different purposes.

[Confluent Schema Registry schema evolution documentation](https://docs.confluent.io/platform/current/schema-registry/fundamentals/schema-evolution.html) distinguishes backward, forward, full, and transitive compatibility and notes format-specific behavior for Avro, Protobuf, and JSON Schema. These labels are useful only with their precise comparison set, reader-writer orientation, and implementation semantics.

The [Apicurio Registry concepts documentation](https://www.apicur.io/registry/docs/apicurio-registry/3.3.x/getting-started/assembly-registry-concepts-glossary.html) distinguishes groups, artifacts, immutable artifact versions, global identifiers, content identifiers, references, rules, and lifecycle state. The vocabulary shows that registry implementations expose different identity and policy models. Architecture should define required semantics before binding clients to one product's nouns.

[RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html) defines HTTP semantics including methods, status codes, validators, conditional requests, caching, authentication challenges, and content negotiation. Registry APIs benefit from those standard mechanisms: an immutable version can have a strong validator, a mutable alias can require conditional mutation, and caches can revalidate without inventing proprietary concurrency behavior.

Together these sources show why the registry boundary is consequential. Wrong resolution can make valid bytes decode into wrong values; over-strict policy can freeze useful evolution; under-strict policy can distribute breaking contracts; missing history can make replay impossible; and unavailable or compromised registries can stop or corrupt an entire data plane.

## Prerequisites and Retrieval

You should understand data modeling, data contracts, APIs, events, serialization, schemas, compatibility, distributed systems, identifiers, hashing, dependency graphs, metadata, provenance, authorization, caching, replication, disaster recovery, CI/CD, generated code, observability, migration, and retirement.

Retrieve schema, schema language, dialect, vocabulary, artifact, subject, group, namespace, version, global ID, content ID, fingerprint, canonicalization, normalization, writer schema, reader schema, backward compatibility, forward compatibility, full compatibility, transitive compatibility, reference, dependency closure, registration, lookup, resolution, validation, promotion, alias, provenance, generated code, envelope, cache, replication, reconciliation, recovery point, recovery time, deprecation, retirement, and revocation.

As a retrieval test, consider the integer `42` in an event envelope carrying schema ID `817`. Ask which registry authority issued `817`; whether the ID is global, regional, tenant-scoped, or content-derived; which format and dialect apply; whether referenced schemas are available; whether the producer encoded with the registered version; whether the consumer is authorized to resolve it; what happens during outage; whether cached content is still trusted; and what semantic meaning the decoded field carries. The number alone answers none of these questions.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish schemas, contracts, registry artifacts, versions, subjects, identifiers, fingerprints, aliases, and semantic concepts;
2. model immutable storage, dependency closure, provenance, promotion, and lifecycle for multiple schema languages;
3. explain writer-reader resolution and backward, forward, full, latest-only, and transitive compatibility without reversing their direction;
4. compare Avro, Protobuf, JSON Schema, OpenAPI, AsyncAPI, and CloudEvents registry needs;
5. design registration, lookup, resolution, validation, search, export, and conditional mutation APIs;
6. choose naming, normalization, fingerprinting, reference, and generated-code policies without conflating identity layers;
7. integrate registry checks with producer and consumer CI/CD while controlling auto-registration and mutable aliases;
8. design secure runtime resolution, caches, envelopes, multitenancy, replication, failover, recovery, and reconciliation;
9. measure compatibility decisions, dependency health, consumer activation, operational reliability, and business outcomes; and
10. migrate and retire schemas while preserving historical decoding, replay, audit, and recovery.

## Core Exposition

**Define the registry's authority boundary.** State which artifact kinds it accepts, which environments and tenants it serves, which identifiers it issues, which policies it enforces, and which decisions remain with domain owners.

A registry may be authoritative for approved schema bytes without being authoritative for the business definition of `order`, legal permission to expose a field, or whether a consumer may act on it. Make those boundaries visible in APIs, metadata, and documentation.

**Separate schema from contract.** A schema can specify type, cardinality, structural constraints, references, and annotations. A complete data contract can also specify meaning, ownership, timeliness, completeness, privacy, quality, error behavior, support, compatibility promises, and consumer obligations.

Link a schema version to the applicable contract version. Do not stretch custom schema annotations until they become an ungoverned contract language, and do not accept schema validity as evidence that contract service levels or semantics hold.

**Separate identity layers.** Common layers include registry authority, tenant, group or namespace, subject or artifact, artifact version, global version ID, content ID, fingerprint, format-native identifier, event type, API operation, and semantic concept.

Two subjects can intentionally contain identical bytes under different owners and policies. One subject can contain multiple versions with different bytes. Two textual documents can normalize to one structural form. One fingerprint algorithm can change or collide. Model each relationship instead of compressing it into a single `schema_id` column.

**Choose durable namespaces.** Names should express stable ownership or contract boundaries, not deployment chronology, mutable teams, brokers, or incidental topic names. Define allowed characters, case, Unicode handling, maximum length, tenant isolation, reservation, rename, redirect, transfer, and non-reuse.

A topic-based subject strategy is convenient when one topic has one value contract. It becomes awkward when a topic contains several event types, when records move between topics, or when key and value have separate compatibility needs. Record-based naming improves reuse but can couple independent domains that happen to share a record name. No strategy is universally correct.

**Make versions immutable.** Once a version is accepted, its content, format, dialect, references, creation principal, timestamp, and decision evidence should not change. Corrections create a new version or append separately governed metadata with an audit trail.

Immutability allows a consumer to reproduce decoding and a reviewer to reproduce policy. If mutable documentation is useful, separate it from the signed or hashed artifact and preserve both histories where consequential.

**Treat aliases as pointers.** Labels such as `latest`, `stable`, `approved`, `production`, or `recommended` can help humans and deployment automation. They are mutable routing decisions, not evidence of the version used yesterday.

Resolve an alias once during a controlled deployment, record the immutable target, and use that identity for execution. Update aliases through authorized conditional requests so two promoters cannot silently overwrite each other.

**Record format and dialect.** `application/json` does not identify JSON Schema. A JSON Schema draft, declared dialect, supported vocabularies, base URI, reference rules, and validation options affect interpretation. Protobuf edition or syntax and imported descriptors matter. Avro protocol and schema artifacts differ. OpenAPI 3.1 and AsyncAPI 3.0 are not interchangeable payload schema languages.

Reject artifacts whose declared dialect is unsupported rather than silently validating under a default. Store the validator implementation and version in decision evidence because validators can disagree or change.

**Preserve original and normalized forms.** Original bytes are evidence of what was submitted and may carry comments, order, whitespace, annotations, or signatures. A normalized or canonical form can support comparison, caching, deduplication, and fingerprinting.

Normalization must be format- and dialect-specific and versioned. Sorting arbitrary JSON keys is not Avro parsing canonical form, not JSON Schema semantic equivalence, and not a safe transformation of every document. Never discard the original merely because a normal form exists.

**Define fingerprints precisely.** A fingerprint declaration includes the input form, normalization version, digest algorithm, output encoding, and collision response. It might mean digest of original bytes, canonical schema, descriptor set, or dependency bundle.

Hash equality can establish equality of the hashed representation under the algorithm assumption. It cannot establish equal ownership, compatible policy, equivalent semantics, or authorization. Hash inequality can arise from irrelevant presentation differences unless canonicalization is justified.

**Model references as a graph.** Schemas can import, include, or reference other schemas and components. Each edge needs a reference name or URI, target authority, immutable target identity, resolution policy, and integrity expectation.

Validate the entire closure. Detect missing targets, forbidden cross-tenant edges, unsupported cycles, inconsistent dialects, duplicate names, depth or size explosions, and mutable external references. A root artifact is deployable only when its closure is deployable.

**Bundle deliberately.** Bundling can improve offline resolution, reproducibility, signing, and recovery. It can also duplicate dependencies, hide shared updates, or change reference scope if performed incorrectly.

Define whether a bundle preserves original identifiers, how embedded resources are indexed, which dependency versions it includes, and how its bundle fingerprint relates to individual artifact fingerprints. Test unbundling and independent resolution.

**Understand writer and reader schemas.** A producer writes bytes according to a writer schema. A consumer may read them using another schema, subject to the format's resolution rules. Registry lookup must supply enough identity for the correct relationship.

An Avro reader can resolve selected differences using rules for records, aliases, defaults, promotions, arrays, maps, enums, fixed values, and unions. Do not reduce this to “new fields are safe.” Defaults are used during reading when a writer lacks a reader field; they do not generally mean a producer may omit any value at write time.

**State compatibility direction.** In the common registry vocabulary, backward compatibility asks whether consumers using the candidate schema can read data written under a comparison schema. Forward compatibility asks whether readers using a comparison schema can read data written under the candidate.

Write the reader and writer pair beside every policy. Teams frequently reverse the terms. If a product defines them differently, expose the concrete pairs in reports and APIs so labels cannot conceal ambiguity.

**Choose the comparison set.** Latest-only checks compare the candidate with one selected previous version. Transitive checks compare it with all applicable historical versions. A branch, environment, or lifecycle filter can further change the set.

Store the exact comparison version IDs and policy version in the decision. “Passed backward compatibility last quarter” is not reproducible if the subject history or default policy later changes.

**Recognize format-specific evolution.** In Avro, reader-writer resolution, defaults, aliases, union rules, and type promotion are central. In Protobuf binary encoding, field numbers and wire types dominate; reserved numbers protect against accidental reuse, while JSON names and generated APIs create additional surfaces. In JSON Schema, validation describes acceptable instances, so compatibility can be reasoned about as relationships between instance sets, but references, dialect, annotations, and open-content defaults complicate the result.

OpenAPI and AsyncAPI compatibility includes operations, messages, channels, parameters, status codes, security, bindings, and generated clients. A registry should dispatch to a format-aware validator rather than pretend one diff engine protects every artifact.

**Define structural compatibility mathematically where useful.** Let `L(S)` denote the set of instances accepted by schema `S` under a fixed dialect and evaluation policy. A candidate reader is structurally backward-compatible with an old writer when every relevant old instance is accepted by the candidate reader: `L(S_old) ⊆ L(S_new)` under the chosen model.

That set relation is an abstraction, not a universal registry algorithm. Serialization, default insertion, code generation, constraints not expressible in the language, finite implementation limits, and application behavior can make the practical relationship narrower.

**Keep syntax and semantics separate.** Adding an optional `currency` field can be structurally compatible while changing the meaning of `amount`. Reusing a field for a new business definition can preserve bytes and break every decision. Changing enum interpretation without changing symbols can escape structural checks entirely.

Require semantic review for meaning, unit, identity, missingness, time, policy, default behavior, and consumer consequence. Link the accepted schema to term, contract, and decision evidence.

**Validate before compatibility.** First parse the artifact using its declared format and dialect. Resolve references. Run structural and format validation. Apply organization policies such as naming, documentation, restricted types, depth, size, security, and ownership. Only then compare a valid candidate against valid baselines.

A compatibility result over invalid or partially resolved artifacts is misleading. Preserve each stage and its diagnostics separately.

**Make policy scoped and versioned.** A policy names artifact kind, environment, subject pattern, compatibility mode, comparison set, validation profile, exception process, effective interval, and owner. Avoid a global default silently governing unrelated contracts.

Policy changes can be breaking even when no schema changes. Version them, simulate them against existing histories, review the changed rejection and acceptance sets, and preserve which policy decided each registration.

**Design an explicit registration workflow.** A submitter proposes content with subject, format, dialect, references, metadata, intended change, and idempotency key. The service authenticates and authorizes; parses; resolves; validates; fingerprints; finds duplicates; selects baselines; checks policy; records diagnostics; and either rejects or creates an immutable candidate version.

Creation need not mean production approval. Separate technical acceptance from promotion when consequence warrants independent review or consumer evidence.

**Separate lookup from registration.** Lookup asks whether equivalent governed content already exists; registration may create state and consume a version number. A client retry must not create duplicate versions after a timeout.

Support an idempotency key bound to principal, scope, and request digest, or define content-addressed create semantics. Return conflict if the same key is reused for different input.

**Use lifecycle states carefully.** Useful states might include `candidate`, `validated`, `approved`, `active`, `deprecated`, `retired`, and `revoked`. Define allowed transitions, required evidence, approvers, timing, rollback, and whether state belongs to an artifact or version.

Do not change immutable schema content during a state transition. Revocation should block unsafe future use according to policy while retaining evidence and a controlled way to interpret historical data.

**Promote with consumer evidence.** A producer's compatibility check is only one gate. Identify consumers, their current reader versions, code-generation runtimes, caches, replay obligations, and activation status. Run contract and integration tests against representative old and new data.

Promotion can require a threshold or explicit acceptance for high-consequence consumers. Nonresponsive consumers are unresolved risk, not automatic approval.

**Control auto-registration.** Runtime auto-registration makes local development easy but can couple application availability to control-plane mutation, bypass review, leak experimental schemas, fragment subjects, and grant producers excessive permissions.

Prefer CI registration and controlled promotion for production. Runtime producers can resolve an approved immutable ID from deployment configuration and fail startup if their compiled or generated schema fingerprint differs. If runtime registration is retained, constrain scopes, environments, policy, quotas, audit, and rollback.

**Bind generated code to evidence.** Generated classes depend on the immutable root and reference closure, schema compiler and plugins, language runtime, generator options, and sometimes naming configuration. Record all of them.

A schema can remain unchanged while a new generator changes equality, optionality, unknown-field handling, JSON names, or validation behavior. Test generated artifacts and publish a reproducible provenance statement instead of treating code generation as a pure function of schema text.

**Design envelopes explicitly.** A wire envelope can carry a magic value, format, registry authority, schema or content ID, message metadata, and payload. Define byte order, identifier width, error handling, authentication coverage, compression ordering, and upgrade path.

Avoid assuming that a small numeric ID is globally meaningful. Cross-cluster replication, tenant boundaries, restore, or vendor migration can map the same number to different content. Include or derive enough authority context to resolve deterministically.

**Fail safely on unknown IDs.** A consumer must not decode unknown bytes using `latest`, a guessed schema, or a structurally similar class. Choices include retrying a trusted registry, using a verified cache, quarantining the message, delaying a partition, or dead-lettering with traceable evidence.

The correct choice depends on consequence, ordering, volume, retry budget, and recovery design. Preserve the raw envelope and payload under access controls when later replay is authorized.

**Design caches as security and correctness components.** Cache keys include registry authority, tenant, immutable ID, representation, and perhaps authorization context. Entries carry integrity evidence, fetch time, policy, expiry, and reference closure.

Immutable content can be cached for long periods, but authorization to retrieve it and revocation response may change. Separate content immutability from access and trust freshness. Bound memory and disk, prevent eviction storms, deduplicate concurrent misses, and observe stale or negative entries.

**Use HTTP semantics deliberately.** Retrieval of immutable versions can return strong ETags and explicit cache controls. Mutable aliases and metadata can use ETags with `If-Match` to prevent lost updates. Create can return a stable resource location; validation errors should have machine-readable diagnostics; pagination should use stable cursors.

Define `404` versus authorization-hidden absence, `409` for state conflicts, `412` for failed preconditions, `422` or other chosen validation response, and retryable server failures consistently. Client libraries should not reinterpret every error as “schema missing.”

**Support discovery without turning the registry into the catalog.** Search by owner, domain, format, lifecycle, tag, dependency, and creation interval helps operators. Registry search remains centered on artifacts and versions.

A data catalog usually adds datasets, systems, products, lineage, stewardship, quality, access, and business discovery. Synchronize selected metadata with clear authority and reconciliation instead of forcing either platform to impersonate the other.

**Govern metadata.** Useful fields include owner, steward, domain, description, sensitivity, contract link, source repository, source commit, build identity, ticket, compatibility intent, consumers, effective interval, support window, deprecation reason, and legal constraints.

Classify metadata as immutable submission evidence, append-only review evidence, or mutable operational annotation. Attribute every mutation. Avoid storing payload examples containing personal or secret data merely to make a schema understandable.

**Protect schema confidentiality.** Schemas reveal internal entities, field names, identifiers, security mechanisms, business workflows, and planned features. Apply least privilege by tenant, group, artifact, environment, operation, and lifecycle.

Separate read, register, promote, change-policy, delete, export, replicate, and administer permissions. Use short-lived service identity, audit decisions, redact sensitive diagnostics, encrypt transport and storage, and review bulk enumeration risk.

**Protect integrity and provenance.** Record submitter identity, source repository and commit, build attestation where available, original bytes, fingerprint declaration, decision policy, validator versions, approvers, and timestamps. Sign exports or manifests when crossing trust boundaries.

A digest fetched over an untrusted channel does not authenticate itself unless a trusted statement binds the expected digest to the artifact. Protect the registry control plane as supply-chain infrastructure.

**Isolate tenants and quotas.** Tenant boundaries apply to namespace enumeration, numeric IDs, content deduplication, timing side channels, references, search, caches, logs, backups, and operational support—not only authorization checks on `GET`.

Rate-limit expensive parse and reference expansion, maximum artifact size, dependency depth, version count, requests, export, and compatibility simulations. A malicious schema graph can consume CPU or memory even without payload data.

**Replicate with identity semantics.** Choose whether IDs are globally allocated, region-prefixed, content-derived, or translated during replication. Preserve source authority and a bijective mapping when translation occurs.

Replicate root versions, references, metadata classes, policy evidence, lifecycle, and tombstones in a causal order that never exposes a root before its dependencies. Detect split-brain registration and define the authority for reconciliation.

**Design backup and restore for interpretability.** Backups include artifacts, all versions, original and normalized forms, reference graphs, identity sequences or maps, policies, metadata history, aliases, lifecycle, audit evidence, credentials configuration, and exports needed for consumers.

Restore into an isolated environment, verify counts and fingerprints, resolve closures, compare sampled and high-consequence IDs, test authorization, exercise consumers, and reconcile before traffic moves. A database restore that reassigns IDs is data corruption from the consumer's perspective.

**Plan degraded operation.** Some consumers can continue using verified immutable cached schemas; some producers can continue emitting known approved IDs; some high-consequence flows must pause if authorization or revocation freshness cannot be established.

Define maximum offline duration, cached working set, restart behavior, cache prewarming, unknown-ID response, backpressure, queue capacity, recovery ordering, and reconciliation. Test cold starts during registry outage rather than assuming warm caches.

**Observe decisions and dependencies.** Measure registrations proposed, accepted, rejected, deduplicated, promoted, deprecated, retired, and revoked by reason and denominator. Measure resolution volume, hit rate, miss rate, latency, error, stale use, unknown IDs, reference depth, broken edges, policy evaluation, and consumer version lag.

Trace identifiers and decision IDs without logging payloads or entire sensitive schemas. Alert on symptoms tied to consumer harm: sudden unknown IDs, cross-region mismatch, increasing stale-cache use, unresolved dependencies, failed promotion tests, or active deprecated versions.

**Define service objectives by path.** Registration and compatibility simulation can tolerate different latency and availability from runtime ID resolution. Search and analytics need not share the runtime availability target. Recovery objectives should reflect the amount of schema history consumers can reconstruct elsewhere.

Measure tail latency and cold-cache behavior. An excellent average can hide one partition blocked on a slow reference chain.

**Test at several layers.** Test parser conformance, dialect behavior, reference resolution, canonicalization, fingerprints, validator consistency, compatibility fixtures, policy selection, lifecycle transitions, authorization, idempotency, conditional updates, pagination, cache behavior, envelope decoding, failover, restore, and reconciliation.

Then test producers and consumers using real serializers, generated code, old and new data, unknown fields, default behavior, boundary values, invalid payloads, replay, rollback, and business outcomes. Curate false-positive and false-negative compatibility cases from incidents.

**Treat exceptions as governed debt.** A compatibility override records the exact candidate, baselines, failed rules, business justification, affected consumers, compensating controls, approver, expiry, rollback, and follow-up.

An override should not mutate history into a false pass. Preserve the original diagnostics and expose exception rates so policy is not weakened invisibly through routine waivers.

**Evolve the registry API itself.** Clients depend on authentication, identifier representation, error models, ordering, pagination, filtering, rate limits, and cache headers. Version or compatibly evolve these behaviors and publish support windows.

Avoid making vendor-specific response shapes the domain abstraction used by every application. A bounded client layer can preserve the organization's identity and policy model while adapters map product differences.

**Plan vendor and region migration.** Export original content, normalized forms, IDs, aliases, references, metadata classes, policy and decisions, lifecycle, and audit evidence. Decide whether wire IDs remain stable, receive authority prefixes, or require envelope translation.

Dual-resolve and compare fingerprints and closures. Shadow compatibility decisions on a representative corpus. Migrate producers and consumers by capability, retain rollback, and reconcile before retiring the old authority.

**Deprecate before retirement.** Deprecation announces replacement, rationale, affected consumers, support end, migration procedure, and monitoring. It does not make old data unreadable.

Track production emissions and reads by immutable ID, generated package use, persisted payloads, replay horizons, reference edges, caches, backups, and disaster-recovery paths. A version with no current producer may remain essential to read retained history.

**Close the lifecycle completely.** Stop old registration, emission, aliases, generated-code publication, subscriptions, transformations, permissions, cache prewarming, replication, and support only after dependencies are closed. Preserve immutable versions for the governed retention period or a verifiable archive/resolver path.

Retirement evidence states who verified consumer closure, what history remains, how replay works, which credentials were removed, how recovery avoids reactivation, and how a later auditor resolves an old identifier.

## Definitions and Notation

Let `a` denote a registry authority and `n` a tenant or namespace. Let `s` be a subject or artifact identity inside that authority and namespace. Let `v` be an immutable artifact version. The tuple `(a, n, s, v)` is more informative than a bare integer ID.

Let `B(v)` be the original submitted bytes for version `v`, `F(v)` its declared format and dialect, `N_q(B(v))` a normal form produced by normalization policy `q`, and `H_h(x)` a digest using algorithm `h`. A fingerprint can be declared as `fp(v) = (q, h, H_h(N_q(B(v))))`.

Let `Ref(v)` be the direct reference set of `v`. Let `Cl(v)` be the transitive dependency closure, including `v`, under a fixed resolution policy. A version is resolvable only if every required member of `Cl(v)` exists, is authorized for the operation, has expected integrity, and can be interpreted under supported formats and dialects.

Let `W` be a writer schema and `R` a reader schema. Define `Resolve(W, R, x)` as the format-specific attempt to interpret datum `x`, written under `W`, through `R`. Compatibility is always a quantified claim over selected schemas and data, not an intrinsic adjective attached to one file.

For comparison set `P = {p_1, ..., p_k}` and candidate `c`, define common registry orientations:

- backward: `Resolve(p_i, c, x)` succeeds for relevant data written under each selected `p_i`;
- forward: `Resolve(c, p_i, x)` succeeds for relevant data written under `c` and read by each selected `p_i`;
- full: both relations hold;
- transitive: `P` includes every applicable historical version rather than one selected predecessor.

Let `L(S)` be the instance language accepted by a validation schema `S` under a fixed dialect, vocabulary support, reference environment, and options. Language inclusion can approximate structural compatibility for validation languages: widening acceptance suggests backward reader compatibility; narrowing acceptance suggests forward reader compatibility. It says nothing by itself about serializers or business meaning.

Let `Dec(c, P, r, e)` be the immutable compatibility decision for candidate `c`, comparison versions `P`, rule/policy version `r`, and evaluation environment `e`, including validator versions and dependency identities. Re-evaluation under different `r` or `e` is a new decision.

Let `State(v, t)` be a version's lifecycle state at time `t`, recorded through attributed transitions. Content remains immutable even though state can evolve.

Let `A_t(label)` be the immutable version targeted by mutable alias `label` at time `t`. Reproducible execution records `A_t(label)`, not just `label`.

Let `E(m)` be the schema identifier carried by message `m`, and `Auth(m)` the registry authority context. Safe decode requires deterministic resolution of `(Auth(m), E(m))`; equality of `E` without equality of authority does not imply equal schema.

Define consumer activation `Act(c, v, t)` as evidence that consumer `c` is prepared for version `v` at time `t`, including code, configuration, generated artifacts, tests, and deployment. Registration and activation are separate facts.

Define a registry SLO over operation `o`, population `U`, interval `T`, threshold `z`, and success predicate `ok`: `SLO(o) = |{u ∈ U: ok(u) and latency(u) ≤ z}| / |U|`. Publish exclusions and denominator; do not mix runtime resolution with administrative search.

## Mechanisms, Invariants, or Proof Structure

Use the following gates to design or review a schema registry.

**Authority gate.** Name registry authorities, tenants, environments, artifact classes, domain owners, platform owners, policy owners, and boundaries of semantic responsibility.

**Identity gate.** Define namespace, subject, artifact, immutable version, global ID, content ID, fingerprint, native identifier, alias, collision, rename, transfer, and non-reuse.

**Format gate.** Record language, syntax or edition, dialect, vocabulary, media type, parser, validator, compiler, generator, options, and support window.

**Immutability gate.** Preserve original bytes, normalized representation, references, provenance, creation evidence, and historical retrieval. Put mutable metadata and aliases on audited resources.

**Reference gate.** Resolve immutable targets, verify integrity and authorization, detect cycles and missing edges, bound graph expansion, and export and recover the entire closure.

**Validation gate.** Separate parse, format conformance, reference resolution, organization lint, security policy, compatibility, semantic review, contract testing, and consumer outcome testing.

**Compatibility gate.** State writer, reader, direction, latest or transitive comparison set, format-specific rule, policy version, validator version, diagnostics, and exception.

**Registration gate.** Authenticate, authorize, validate scope, enforce quotas, parse, resolve, normalize, fingerprint, deduplicate, compare, decide, persist atomically, and return idempotently.

**Promotion gate.** Require intended environment, owner approval, consumer inventory, activation evidence, rollout, rollback, support interval, and mutable pointer precondition.

**Envelope gate.** Specify authority, ID semantics, format, framing, integrity coverage, compression, encryption, unknown-ID response, and protocol evolution.

**Cache gate.** Key by full authority and identity, verify content, bundle references, bound resources, define staleness and authorization, deduplicate misses, and test cold starts.

**Protection gate.** Enforce tenant isolation, least privilege, secret handling, schema sensitivity, diagnostic redaction, rate limits, audit, integrity, provenance, export control, and supply-chain trust.

**Operations gate.** Separate runtime and administrative SLOs; observe resolution, cache, registration, decisions, references, consumers, region consistency, cost, and incidents.

**Recovery gate.** Restore identities, content, references, policy evidence, aliases, metadata, authorization, and audit; compare fingerprints and exercise consumers before failover.

**Migration gate.** Export completely, map identities deterministically, shadow resolution and compatibility, dual-run, reconcile, canary consumers, retain rollback, and close old authority.

**Retirement gate.** Stop producers, close consumers, remove aliases and permissions, preserve retained history, prove replay, expire exceptions, update recovery, and record closure.

### Executable evidence: simplified record compatibility policy

This Python example evaluates two candidate record descriptions against one accepted version. The invented policy treats equal types as compatible, permits a new reader field only when it has a default, and assumes an old reader ignores fields written only by a new writer.

<!-- bijux-verify: {"id":"simplified-record-compatibility-policy","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"subjects=1\ncandidate_versions=2\naccepted_candidates=1\nrejected_candidates=1\nregistered_versions=2\nbackward_issues=2\nforward_issues=1\ncompatibility_issues=3\ndefaults_added=1\nunique_fingerprints=3\n","stderr":""}} -->
```python
ABSENT = object()

accepted = {
    "order_id": {"type": "string", "default": ABSENT},
    "amount": {"type": "long", "default": ABSENT},
}

candidates = [
    {
        "order_id": {"type": "string", "default": ABSENT},
        "amount": {"type": "long", "default": ABSENT},
        "currency": {"type": "string", "default": "USD"},
    },
    {
        "order_id": {"type": "string", "default": ABSENT},
        "amount": {"type": "string", "default": ABSENT},
        "status": {"type": "string", "default": ABSENT},
    },
]


def reader_issues(writer, reader):
    issues = []
    for name, reader_field in reader.items():
        writer_field = writer.get(name)
        if writer_field is None:
            if reader_field["default"] is ABSENT:
                issues.append((name, "reader field has no writer value or default"))
        elif writer_field["type"] != reader_field["type"]:
            issues.append((name, "writer and reader types differ"))
    return issues


backward_results = [reader_issues(accepted, candidate) for candidate in candidates]
forward_results = [reader_issues(candidate, accepted) for candidate in candidates]
accepted_candidates = sum(
    not backward and not forward
    for backward, forward in zip(backward_results, forward_results)
)


def fingerprint(record):
    return tuple(
        (name, field["type"], field["default"] is not ABSENT, repr(field["default"]))
        for name, field in sorted(record.items())
    )


all_versions = [accepted, *candidates]
backward_issues = sum(len(result) for result in backward_results)
forward_issues = sum(len(result) for result in forward_results)
defaults_added = sum(
    field["default"] is not ABSENT
    for candidate in candidates
    for name, field in candidate.items()
    if name not in accepted
)

print("subjects=1")
print(f"candidate_versions={len(candidates)}")
print(f"accepted_candidates={accepted_candidates}")
print(f"rejected_candidates={len(candidates) - accepted_candidates}")
print(f"registered_versions={1 + accepted_candidates}")
print(f"backward_issues={backward_issues}")
print(f"forward_issues={forward_issues}")
print(f"compatibility_issues={backward_issues + forward_issues}")
print(f"defaults_added={defaults_added}")
print(f"unique_fingerprints={len({fingerprint(version) for version in all_versions})}")
```

The expected output reports `subjects=1`, `candidate_versions=2`, `accepted_candidates=1`, `rejected_candidates=1`, `registered_versions=2`, `backward_issues=2`, `forward_issues=1`, `compatibility_issues=3`, `defaults_added=1`, and `unique_fingerprints=3` on separate lines.

The evidence is intentionally format-neutral and much simpler than every real schema language. The first candidate passes because its additional field has a default for the candidate reader and the old reader is assumed to ignore it. The second candidate produces a backward type mismatch, a backward missing-default issue, and a forward type mismatch. Those rules do not implement Avro resolution, Protobuf wire compatibility, JSON Schema language inclusion, OpenAPI or AsyncAPI evolution, canonicalization, serialization, aliases, unions, numeric promotion, enums, unknown fields, references, logical types, dialects, or generated-code behavior. Tuple uniqueness is not a cryptographic fingerprint and proves no semantic identity. Production assurance needs format conformance suites, validator differential tests, dependency graphs, real serializers and readers, generated-code tests, historical payload replay, semantic and security review, consumer activation, failure injection, recovery, and accountable approval.

## Alternatives and Trade-Offs

**Central enterprise registry.** One service can standardize identity, policy, tooling, discovery, and operations. It can also become a latency dependency, organizational bottleneck, high-value security target, and false owner of domain meaning.

**Federated domain registries.** Domains retain autonomy, local formats, policy, and failure isolation. Cross-domain discovery, authority identity, envelope portability, replication, and consistent minimum controls become harder.

**Repository-only schemas.** Version control provides review, provenance, branching, and developer workflow. Runtime lookup, global identifiers, subject compatibility, cross-repository dependency closure, and consumer observability require additional machinery.

**Registry as derived deployment.** Git remains the source of truth and CI publishes immutable versions to runtime registries. This gives auditable change control but needs reconciliation so manual or failed publications cannot diverge from declared state.

**Registry-first authoring.** Interactive APIs make experimentation and discovery fast. Unless every mutation returns to source control with durable review, authorship and disaster recovery can become opaque.

**Content-addressed identity.** Digests make equality checks, deduplication, caching, and cross-system verification attractive. They produce long identifiers, require precise canonicalization, cannot express ownership or lifecycle, and need an algorithm migration plan.

**Sequential global IDs.** Small identifiers make wire envelopes compact and lookup efficient. They require a durable allocator, expose cardinality, collide across authorities, complicate restore and migration, and cannot be verified without resolution.

**Subject-scoped versions.** Human-readable subject and monotonic version pairs support review and compatibility history. Renames, cross-subject reuse, multi-region allocation, and wire size need explicit treatment.

**Topic-based subjects.** They align with broker configuration and work well when each topic has one contract. Multi-event topics, key/value separation, routing changes, reuse, and domain ownership can make topic identity an unstable schema boundary.

**Record-based subjects.** They encourage reuse by record identity. Identically named records from different contexts can collide, and one compatibility policy can couple producers that are operationally independent.

**Latest-only compatibility.** It is faster and allows a controlled chain of pairwise changes. A candidate can pass against the newest version while breaking an older reader or retained datum still in service.

**Transitive compatibility.** It protects a broader history and supports slow consumers and replay. It costs more, can freeze accumulated mistakes, and still cannot establish semantics or application behavior.

**Strict global policy.** Uniform controls are easy to explain and audit. Different formats, domains, retention horizons, and consequences need different safe evolution rules, so global strictness can become either paralyzing or superficial.

**Scoped policy with exceptions.** It matches consequence and format. Governance, simulation, precedence, and exception expiry become more complex and must remain observable.

**Runtime auto-registration.** It reduces friction and ensures a producer can discover an ID for its local schema. It adds mutation during startup or traffic, broad permissions, drift, accidental subjects, review bypass, and a new availability coupling.

**CI registration and promotion.** It produces repeatable evidence before runtime and supports separation of duties. Deployments need a way to carry approved immutable IDs and coordinate consumers without manual bottlenecks.

**Online resolution for every message.** It centralizes current authorization and avoids large local caches. Latency, cost, rate limits, and registry outages can stop the data plane.

**Immutable local caches.** They improve throughput and degraded operation. They require complete authority-aware keys, bounds, reference closure, prewarming, integrity, and a response to changed access or revocation.

**Embedded schemas.** Self-describing payloads improve portability and offline decoding. They increase size, disclosure, parsing risk, and opportunities for untrusted content; identity and approval still need evidence.

**Compact schema IDs.** They minimize message overhead and centralize schemas. They require reliable resolution and stable authority semantics throughout retention and disaster recovery.

**Bundled dependency closure.** A bundle supports reproducible generation, export, signing, and offline consumers. It can duplicate shared dependencies and must preserve identifiers and reference semantics.

**Live external references.** Shared definitions can update centrally and reduce duplication. Mutable remote content destroys reproducibility and can introduce supply-chain or availability failures, so production references should resolve to immutable governed targets.

**Hard deletion.** It can satisfy narrowly interpreted cleanup or reduce attack surface. It can make retained data undecodable, break dependencies, invalidate audit, and corrupt restored backups. Tombstone or restricted archival access is usually safer for governed history.

**Long retention.** It preserves replay, audit, and migration. It increases storage, disclosure, key management, legal, and operational obligations; retention should derive from data and contract lifecycles rather than “forever.”

**Build versus buy.** A product accelerates proven storage, format support, APIs, and integrations. Vendor semantics, export completeness, ID portability, compatibility behavior, limits, and recovery must be tested. A custom service offers exact fit but assumes a difficult distributed-systems and language-semantics burden.

## Failure Modes and Misconceptions

**“The schema registry owns the truth.”** It may own the approved serialized artifact. Domain meaning, source authority, legal permission, quality, and consumer decisions usually have other accountable owners.

**“A schema is a data contract.”** Structure is one part of a contract. Timeliness, meaning, completeness, access, support, incidents, lifecycle, and consequences require additional agreement and evidence.

**“One schema ID is globally unique.”** An integer is usually meaningful only within an authority or cluster. Carry authority context or use a globally designed identity and prove migration behavior.

**“The subject name identifies the content.”** A subject is a policy and history boundary. Several versions and sometimes identical content across subjects invalidate that shortcut.

**“Same fingerprint means same contract.”** It means equal normalized input under stated algorithm assumptions. Ownership, purpose, semantics, classification, policy, and lifecycle can differ.

**“Different fingerprint means breaking change.”** Whitespace, ordering, descriptions, annotations, or normalization changes can alter some digests without affecting accepted data. Use format-aware comparison and retain both original and normalized evidence.

**“Backward compatible means every consumer is safe.”** It covers a stated reader-writer structural relation. Consumer code, JSON mapping, generated APIs, business rules, semantics, performance, and deployment can still break.

**“Optional is universal.”** Absence, null, default, zero value, unknown field, presence tracking, and generated accessor behavior differ by schema language and runtime.

**“Adding a field is always safe.”** The format may require a default, a strict consumer may reject unknown content, size or privacy can change, and a new field can alter meaning or behavior.

**“Deleting a field is safe if nobody writes it.”** Old retained data, replay, generated code, analytical jobs, and unknown consumers can still depend on it. Protobuf tags also must not be reused.

**“Renaming is cosmetic.”** It may be binary-safe under stable Protobuf tags yet break JSON, reflection, queries, generated code, mappings, metrics, and human interpretation.

**“A default is only convenience.”** Defaults participate in reader behavior and can invent values for absent historical fields. The chosen default needs semantic review and tests.

**“Transitive checks guarantee evolution forever.”** They cover selected structural rules across stored versions. They do not cover unregistered schemas, consumers, meaning, external references, generator changes, or runtime limits.

**“The latest version is reproducible.”** It is a moving pointer. Resolve and record an immutable version and closure at build or deployment time.

**“References reduce all duplication.”** They introduce graph resolution, availability, authorization, cycles, version pinning, export, replication, and recovery obligations.

**“A URL reference is immutable.”** A URI identifies; it does not guarantee that returned content never changes. Pin identity and integrity under a governed resolver.

**“Auto-registration prevents drift.”** It can register drift as a new approved-looking version. Compare compiled schema to an approved immutable identity and make mutation a separate authority.

**“If the registry is down, use latest from cache.”** Cache entries need authority, immutable ID, integrity, closure, and trust state. Guessing by alias can silently decode with the wrong contract.

**“Fail open preserves availability.”** Decoding unknown bytes with guessed content preserves traffic by sacrificing correctness. Quarantine, backpressure, or verified cached operation is safer.

**“Fail closed is always safe.”** Blocking a safety event or exhausting a broker partition can cause harm. Define consequence-aware degraded behavior, capacity, and recovery.

**“Replicating the schema table is disaster recovery.”** IDs, sequences, references, policies, aliases, metadata, authorization, audit, and consumer caches are part of recoverable identity.

**“Multi-region active-active is just database replication.”** Concurrent registration, numeric allocation, subject policy, alias mutation, reference order, and split brain require explicit consistency and conflict rules.

**“Schemas are not sensitive because they contain no rows.”** Names and structures reveal identifiers, internal capabilities, security assumptions, and business plans. Examples and annotations can contain actual sensitive values.

**“Administrators need unrestricted access.”** Separate operational duties and use audited emergency access. Bulk export and policy mutation are high-consequence operations.

**“Logs should include the rejected schema.”** Full content can leak sensitive design or secrets. Log decision identity and safe diagnostics; secure detailed evidence separately.

**“A successful restore proves correctness.”** Consumers must resolve historical IDs and reference closures to identical content. Compare fingerprints, permissions, envelopes, and actual decoding.

**“No current producer means safe deletion.”** Stored events, files, database blobs, backups, replays, and legal evidence can require the old writer schema long after emission ends.

**“The registry is the data catalog.”** Registry and catalog metadata overlap, but artifact resolution and business data discovery have different authority, users, lifecycle, and SLOs.

**“Vendor compatibility labels are portable.”** Products can differ in supported versions, dialects, normalization, references, defaults, and rule details. Test a corpus before migration.

**“A green dashboard proves safety.”** High availability and pass rates can coexist with wrong policy, missing consumers, semantic drift, or undecodable history. Measure outcomes and reconcile.

## Worked Examples

### Example 1

An order event uses Avro. Version 1 contains `order_id` and `amount_minor`; version 2 adds `currency` with an appropriate reader default. The registry records the exact Avro implementation, writer-reader comparison, references, policy version, and consumer replay test. Domain review also determines that historical `amount_minor` was implicitly USD; a structural pass alone would have hidden that semantic assumption.

### Example 2

A Protobuf service removes field 7, `legacy_status`. The `.proto` reserves both number 7 and the old name. Binary fixtures confirm unknown-field behavior across supported runtimes, while JSON and generated-client tests identify consumers still using `legacyStatus`. The registry records separate binary and JSON judgments instead of calling the rename universally safe.

### Example 3

A JSON Schema 2020-12 artifact references shared address and money schemas by immutable registry URI. Registration resolves the closure, rejects a mutable `main` reference, records vocabularies, and bundles the approved dependencies for offline validation. A change that narrows `postal_code` matches is evaluated as an instance-language restriction and then reviewed for jurisdictional meaning.

### Example 4

An OpenAPI description adds a required request header to an existing operation. Its component schemas remain unchanged and individually compatible, yet older clients cannot make accepted requests. Interface-level comparison rejects production promotion until a staged server behavior and client migration exist.

### Example 5

An AsyncAPI document changes a message payload safely but moves an operation to a different channel binding and changes delivery assumptions. Payload compatibility passes; protocol and operational review fail. The version remains a candidate until broker configuration, retry behavior, security, and consumers are tested.

### Example 6

A CloudEvent preserves `type=com.example.order.created` while changing `dataschema`. The new shape is structurally readable, but `amount` changes from authorized total to pre-tax subtotal. Semantic review requires a new event type or explicit contract migration because the same type would lead consumers to apply the wrong business interpretation.

### Example 7

A producer times out after submitting a schema. It retries with the same idempotency key and identical request digest; the registry returns the already-created immutable version. A retry with the same key and different content receives a conflict. No duplicate version or ambiguous audit record is created.

### Example 8

During a registry outage, running consumers decode known IDs from a signed, prewarmed cache containing complete dependency closures. Unknown IDs enter a bounded quarantine and pause affected partitions before capacity is exhausted. Cold-starting instances remain unready. After recovery, the system resolves and verifies quarantined IDs, replays in order, and reconciles counts.

### Example 9

Two regions once allocated numeric ID 9001 to different content. Migration introduces authority-qualified envelope IDs and an explicit translation map. Dual-resolution compares content fingerprints and reference closures before traffic shifts. The team does not merge the tables and hope subject names disambiguate history.

### Example 10

A deprecated customer schema has no live producers, but seven years of retained events and a disaster-recovery replay use it. Retirement removes its production alias and registration permission but preserves restricted immutable resolution, dependencies, integrity evidence, and restore tests until the event retention obligation ends.

## Cross-Program Connections

**API and Service Engineering.** Registries for OpenAPI, AsyncAPI, and message payloads complement API lifecycle, contract testing, content negotiation, error models, and versioning. HTTP validators, conditional requests, cache controls, authentication, and stable resource identity directly shape registry APIs.

**Platform Engineering.** A registry is a platform control plane with tenancy, golden paths, client libraries, policy, self-service, SLOs, quotas, audit, disaster recovery, and migration concerns. Platform convenience must not erase domain authority or create hidden runtime coupling.

**Distributed Systems Engineering.** Global identifiers, immutable logs, concurrent registration, caching, replication, split brain, failover, backpressure, and reconciliation are distributed-systems problems. The required consistency differs for immutable reads, alias mutation, ID allocation, and search.

**Data Engineering.** Batch files, streams, CDC records, lake tables, and generated transformations need durable writer identities and historical schemas. Replay horizons and late data make deletion and latest-only assumptions dangerous.

**Software Engineering Patterns.** Anti-corruption layers, adapters, dependency inversion, immutable value objects, state machines, and content-addressed storage help isolate product-specific APIs while preserving registry intent.

**Programming Languages and Compilers.** Parsing, abstract syntax, name resolution, type systems, canonical forms, compiler versions, code generation, unknown-field behavior, and runtime representation determine what “same schema” and “compatible” mean in practice.

**Security Engineering.** Registry compromise can distribute malicious or misleading contracts across many services. Least privilege, provenance, signing, supply-chain attestations, tenant isolation, audit, secret hygiene, and secure recovery are central controls.

**Site Reliability Engineering.** Resolution latency, cache hit rate, cold starts, saturation, dependency depth, quarantine capacity, recovery objectives, failover exercises, and error budgets connect artifact governance to service reliability.

**Governance, Risk, and Compliance.** Schemas expose classifications, retention-relevant structures, policy annotations, and approval evidence. Exceptions, deletion, restricted history, cross-border replication, and access logs need accountable governance.

**Testing and Quality Engineering.** Compatibility fixtures, property tests, differential validators, historical payload replay, generated-client matrices, mutation tests, failure injection, restore drills, and semantic outcome tests reveal false confidence from shallow diffs.

**Systems Engineering.** The registry is one component in a producer-broker-consumer system. Local optimization of pass rate or latency can create emergent coupling, migration deadlock, or systemic outage unless interfaces, feedback, capacity, and lifecycle are considered end to end.

**Information Architecture.** Stable naming, findability, metadata authority, navigation, deprecation notices, and links between technical artifacts and human concepts affect whether people select the correct schema instead of merely one that looks familiar.

## References

1. Apache Software Foundation, [“Apache Avro 1.12.0 Specification”](https://avro.apache.org/docs/1.12.0/specification/), 2024. Retrieved 2026-09-03.
2. Google, [“Protocol Buffers Language Guide (proto3)”](https://protobuf.dev/programming-guides/proto3/), current guide. Retrieved 2026-09-03.
3. JSON Schema, [“JSON Schema: A Media Type for Describing JSON Documents,” Draft 2020-12](https://json-schema.org/draft/2020-12/json-schema-core.html), 2022. Retrieved 2026-09-03.
4. JSON Schema, [“JSON Schema Validation: A Vocabulary for Structural Validation of JSON,” Draft 2020-12](https://json-schema.org/draft/2020-12/json-schema-validation.html), 2022. Retrieved 2026-09-03.
5. OpenAPI Initiative, [“OpenAPI Specification 3.1.1”](https://spec.openapis.org/oas/v3.1.1.html), 2024. Retrieved 2026-09-03.
6. AsyncAPI Initiative, [“AsyncAPI Specification 3.0.0”](https://www.asyncapi.com/docs/reference/specification/v3.0.0), 2023. Retrieved 2026-09-03.
7. Cloud Native Computing Foundation, [“CloudEvents Specification 1.0.2”](https://github.com/cloudevents/spec/blob/ce@v1.0.2/cloudevents/spec.md), 2022. Retrieved 2026-09-03.
8. Confluent, [“Schema Evolution and Compatibility”](https://docs.confluent.io/platform/current/schema-registry/fundamentals/schema-evolution.html), current documentation. Retrieved 2026-09-03.
9. Apicurio, [“Apicurio Registry Concepts”](https://www.apicur.io/registry/docs/apicurio-registry/3.3.x/getting-started/assembly-registry-concepts-glossary.html), 2025. Retrieved 2026-09-03.
10. IETF, [“RFC 9110: HTTP Semantics”](https://www.rfc-editor.org/rfc/rfc9110.html), 2022. Retrieved 2026-09-03.

## Exercises

### Exercise 1

Design a registry model for Avro events, Protobuf services, JSON Schema documents, OpenAPI descriptions, and AsyncAPI descriptions across four domains and three environments. Specify authority, naming, identity, formats, versions, references, policy, metadata, APIs, and ownership.

### Exercise 2

An Avro subject has 18 historical versions, a 90-day rolling producer fleet, consumers that replay five years, and one proposed field addition with a default. Design compatibility, semantic, consumer, rollout, rollback, and evidence gates. Explain latest-only versus transitive policy.

### Exercise 3

A platform currently permits runtime auto-registration and embeds cluster-local numeric IDs in events. It must move to two active regions and allow registry outages without corrupt decoding. Design the authority-qualified envelope, registration workflow, caching, replication, conflict, degraded mode, and migration.

### Exercise 4

Design a security, reliability, and observability review for a multi-tenant schema registry. Include threats, permissions, integrity, sensitive metadata, quotas, SLOs, indicators, alerts, backups, restore, reconciliation, and incident correction.

### Exercise 5

A company is replacing one registry product with another while 600 producers, 1,400 consumers, generated packages, retained streams, and disaster-recovery systems depend on it. Design export, identity mapping, shadowing, dual-running, activation, rollback, retirement, and historical interpretation.

## Answers to the Exercises

### Answer 1

Define a registry authority URI and isolate tenants or domains, environments, and privileges. Use durable domain-owned groups and artifact names, not temporary team or broker names. Distinguish subject identity, immutable version, portable authority-qualified ID, product-local numeric ID, content fingerprint, semantic concept, API operation, event type, and mutable alias. Preserve original content and a format-specific normal form with declared algorithm. Versions are immutable; aliases and lifecycle transitions are separate audited resources.

Register exact format and dialect: Avro schema or protocol, Protobuf syntax or edition plus descriptor/import closure, JSON Schema dialect and vocabulary, OpenAPI 3.1.1, or AsyncAPI 3.0.0. References target immutable authorized versions and registration validates the closure. Dispatch parse and compatibility to format-specific engines. Scope policies by domain, artifact kind, and environment; preserve comparison sets and validator versions. Add semantic and consumer gates beyond structure. Metadata identifies owner, steward, sensitivity, contract, source commit, generator, consumers, support, and retention.

Expose idempotent submit, lookup, immutable resolve, reference traversal, validation, compatibility simulation, version listing, search, state transition, conditional alias update, export, and audit APIs. Use stable pagination and machine-readable diagnostics. Domains own meaning and compatibility intent; the platform owns service operation and minimum safety controls; security owns protection baselines; consumers own activation evidence. Synchronize discovery metadata into a catalog without transferring authority.

### Answer 2

State orientation concretely: the candidate reader must resolve data written by selected old writer schemas for backward compatibility; selected old readers must resolve candidate-written data for forward compatibility. A latest-only check protects only the relationship with version 18. A transitive check compares the candidate with all historical versions applicable to the five-year replay horizon, or with an explicitly justified retained subset. Store exact baselines, policy, validator, references, and diagnostics.

Confirm the default is legal for Avro resolution and semantically correct for historical data; distinguish a reading default from producer omission behavior. Inspect changes in meaning, units, privacy, size, and quality. Inventory consumers, reader versions, code generators, caches, replay paths, and unknown-field behavior. Generate old and new code, serialize representative and boundary data with actual writers, read through supported readers, replay sampled history, and test business outcomes. Register as candidate, publish immutable ID, canary producers, compare dual reads, monitor errors and lag, and retain producer and consumer rollback.

Do not let the 90-day producer rollout define the entire compatibility horizon when consumers replay five years. If transitive structural policy blocks a safe migration because of obsolete mistakes, use a precise, expiring exception with affected versions, consumer proof, compensation, and approval; never rewrite history into a pass. Promote only after required consumers activate, and preserve every writer schema needed for retained events.

### Answer 3

Introduce an envelope carrying a format/version marker, registry authority or region-independent authority ID, immutable portable schema identity, and payload. Maintain a signed mapping to existing cluster-local IDs during transition. Never resolve an unfamiliar numeric ID against another region's table. Define global allocation, content-derived portable IDs, or deterministic translation; test collisions and restore.

Move production mutation to CI: validate source-controlled content and references, simulate format-aware compatibility, register idempotently, collect approvals and consumer evidence, promote, then inject the immutable identity into deployment. Runtime identities may resolve but not register. During migration, dual-publish or translate envelopes under controlled sampling, dual-resolve both registries, compare original bytes, normalized fingerprints, references, and actual decode, and retain rollback.

Replicate dependencies before roots and include policies, metadata history, lifecycle, aliases, audit, and tombstones. For concurrent mutation, give one authority ownership per subject or use globally conflict-free allocation and conditional alias changes. Consumers cache verified immutable closures keyed by full authority and ID, with bounds and prewarming. During outage, known IDs use trusted cache within declared policy; unknown IDs enter bounded quarantine or backpressure. Test cold start, capacity, recovery order, replay, and reconciliation before claiming availability.

### Answer 4

Threat-model unauthorized read, enumeration, cross-tenant reference, malicious expansion, oversized artifact, parser exploit, policy weakening, illicit registration or promotion, ID substitution, provenance forgery, cache poisoning, backup theft, audit deletion, and administrator abuse. Classify schemas and metadata; remove sensitive examples and secrets. Separate permissions for read, register, promote, policy, lifecycle, export, replication, and administration. Use workload identity, least privilege, short-lived credentials, audited emergency access, encryption, trusted provenance, signed exports, parser isolation, dependency and size limits, quotas, and redacted diagnostics.

Separate runtime resolution SLOs from registration, simulation, search, and analytics. Measure tail latency, availability, correctness, cache hits and stale use, unknown IDs, reference depth and failure, regional mismatch, registration decisions, exception age, consumer lag, saturation, quarantine, cost, and incidents with denominators. Alert on harm-oriented symptoms rather than raw traffic alone. Trace authority-qualified IDs and decision IDs without logging sensitive content.

Back up every immutable representation, identity map and sequence, reference graph, decision and policy evidence, alias history, lifecycle, authorization configuration, audit, and required signing state. Restore in isolation; compare counts and fingerprints; resolve closures; test permissions, cold and warm caches, historical envelopes, representative consumers, and failover. Reconcile regions and source repositories before activation. Incident correction revokes unsafe future use when necessary, preserves evidence, identifies affected messages and consumers, publishes a replacement, replays under authority, and verifies downstream repair.

### Answer 5

Inventory authorities, subjects, versions, original and normalized content, IDs, fingerprints, references, policies, compatibility results, aliases, lifecycle, metadata, permissions, producers, consumers, generators, client libraries, envelopes, caches, retained data, backups, and recovery paths. Export through documented APIs and independently verify counts, bytes, closures, and metadata classes. Test both products against a curated corpus to identify differences in format versions, canonicalization, references, and compatibility behavior.

Choose identity strategy explicitly. If wire IDs can remain stable, prove the new registry preserves their mapping. Otherwise introduce authority-qualified portable IDs and a durable bijective translation table; never silently renumber historical envelopes. Shadow reads and compatibility decisions, compare diagnostics and actual serializer behavior, and resolve every mismatch. Replicate dependencies before root artifacts and preserve old policy evidence even if the new engine reports a different result.

Dual-run resolution, then canary producers and consumers by consequence. Record consumer activation and immutable versions, generated compiler and runtime provenance, cache behavior, replay results, latency, errors, and business outcomes. Retain routing and data rollback until reconciliation is clean. Deprecate the old authority, stop new registration and aliases, remove producer mutation, watch old reads, close consumers, revoke credentials, stop replication and cache prewarming, and update disaster recovery. Preserve a restricted resolver or verifiable archive for every retained payload, and test that restored historical systems cannot reactivate the old production control plane.
