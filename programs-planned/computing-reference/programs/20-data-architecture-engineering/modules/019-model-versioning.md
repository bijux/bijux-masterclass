---
module_id: DARCH-019
program: Data Architecture Engineering
level: 1
module_number: 19
title: Model Versioning
status: complete
last_verified: 2026-09-03
---

# Model Versioning

## One-Page Review

### Governing question

How can an organization change conceptual, logical, physical, canonical, exchange, vocabulary, mapping, and policy models while preserving exact identity, compatibility claims, historical interpretation, consumer safety, migration evidence, and accountable retirement?

### Essential definitions

- A **model identity** names a continuing governed subject, such as the enterprise Customer logical model; a **model version identity** names one immutable released state of that subject.
- A **version scheme** defines the syntax, ordering, and meaning of version identifiers. A version string has no inherent compatibility semantics outside that scheme.
- A **released artifact** is a fixed, retrievable representation approved for use. Its content digest distinguishes exact bytes or canonical content from a mutable label.
- A **change set** is the explicit difference between a version and one or more parents, classified by affected meaning, structure, constraints, dependencies, and consumers.
- **Backward compatibility** usually asks whether a newer reader or consumer can accept older producer data; **forward compatibility** asks whether an older reader can accept newer producer data. The terms must declare direction because communities use them inconsistently.
- **Structural compatibility** concerns shape and validation; **semantic compatibility** concerns preserved meaning; **behavioral compatibility** concerns consumer decisions and side effects; **operational compatibility** concerns deployment and coexistence.
- A **compatibility policy** defines allowed changes and evidence for a scope, direction, version horizon, population, and consumer class.
- A **migration** transforms data, references, mappings, implementations, or decisions from one version context to another while preserving declared invariants and recording loss.
- A **version lineage** is a directed graph of derivation, supersession, fork, merge, profile, extension, and mapping relationships among exact versions.
- A **support window** is the governed interval during which a version receives compatibility, correction, security, operational, or migration support.

### Central model, mechanism, or theorem

Represent a released model version as:

`V = (model_id, version_id, parents, scope, semantics, artifacts, dependencies, effective_time, authority, provenance, lifecycle)`

Treat compatibility as a scoped relation rather than a property of one version:

`Compat(producer_version, consumer_version, use, data_population, policy, time, evidence)`

A label such as `2.1.0`, `2026-09`, or `revision-47` identifies or orders a release under a declared scheme. It does not prove that a reader parses it, a rule still means the same thing, a workflow behaves safely, historical records remain interpretable, or a deployment can coexist. Those are separate claims requiring evidence.

### Critical invariants

- A stable model identity and an immutable version identity are distinct and globally resolvable in their governed scope.
- Every released artifact is immutable, content-addressable or digest-verified, provenance-linked, and reproducibly retrievable.
- Every version declares its parents, change set, scope, authority, dependencies, effective time, lifecycle state, and support policy.
- Compatibility always names direction, producer and consumer versions, use, format or interface, representative data population, policy, horizon, and evidence.
- Structural acceptance never stands in for semantic, behavioral, operational, privacy, or safety compatibility.
- Changes to identity, grain, units, code meaning, defaults, nullability, cardinality, authority, time, protection, or derivation receive semantic review even when syntax remains valid.
- Released models, profiles, vocabularies, code lists, mappings, generated schemas, validators, documentation, and implementations can evolve independently and therefore have distinct version identities.
- Consumers and stored populations remain discoverable so impact analysis includes unknown, dormant, batch, replay, export, and archival paths.
- Breaking releases have an approved migration, coexistence, cutover, reconciliation, rollback, and retirement strategy before production use.
- Historical data retains or can resolve the exact model, vocabulary, mapping, rule, and interpretation context needed for authorized reconstruction.

### Common failures

Common failures are overwriting a released model; treating a branch name or mutable URL as a version; applying Semantic Versioning without defining the public contract; calling an additive field universally compatible; testing only syntax; ignoring defaults and unknown enum behavior; changing a unit without changing a type; renaming identity without aliases or mappings; reusing deleted field numbers; versioning a schema but not its code list; hiding local profiles behind the base version; recording only the latest mapping; forgetting long-lived stored data; claiming compatibility from a registry setting alone; forcing all consumers into a flag-day migration; dual-writing without reconciliation; preserving obsolete sensitive fields forever; and retiring a version while replay, archive, or legal processes still depend on it.

### Compact example

Version `Customer/1.4.0` contains optional `marketingConsent: boolean`, where absence means “not collected.” A proposed `1.5.0` adds enum `consentStatus = {GRANTED, DENIED, UNKNOWN}` and derives the old flag. Both JSON documents can be made structurally valid, but the meanings are not automatically interchangeable: `false` might historically combine denial and missing evidence. The release therefore versions the logical model, JSON schema, code list, derivation rule, and mapping separately; tests old and new consumers on representative null and historical cases; records information loss; supports both interfaces during migration; and prevents analytics from interpreting mapped `UNKNOWN` as `DENIED`.

### Connections

[DARCH-015](015-shared-vocabulary-and-business-glossaries.md) establishes governed terms and codes. [DARCH-016](016-canonical-models-and-their-trade-offs.md) and [DARCH-017](017-event-schemas-and-information-models.md) supply canonical and event artifacts that evolve. [DARCH-018](018-temporal-and-historical-modeling.md) separates business validity from recorded history. This module establishes version identity and compatibility evidence before [DARCH-020](../ROADMAP.md) reconciles conflicting models.

## Governing Question

Models change because domains, laws, evidence, organizations, technologies, and consumer needs change. The hard problem is not assigning the next number. It is preserving the meaning of every decision that crosses the change.

A model may appear in a diagram, catalog, JSON Schema, Avro record, protobuf message, table definition, transformation, API, event, validation rule, code list, data product, generated class, and human procedure. These representations do not necessarily change together. One version number attached to “the model” can therefore conceal several independent release lines.

Versioning must answer five questions. Which exact artifact was used? How does it relate to predecessors and derivatives? What changed in structure and meaning? Which producer-consumer uses remain valid? How will stored data and running systems move, coexist, or remain historically interpretable? A sound version record makes those questions decidable from durable evidence rather than team memory.

## Why This Matters

An unnoticed model change can alter invoices, eligibility, clinical interpretation, fraud decisions, regulatory reports, access controls, machine-learning features, and scientific results. Parsers may continue to accept bytes while decisions silently change. Conversely, a syntactic change that appears dramatic may be safely bridged by an exact mapping.

[Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html) requires a declared public API, makes released contents immutable, and connects major, minor, and patch increments to incompatible changes, compatible functionality, and fixes. Those rules are valuable when a model has a precise public contract. They do not decide what the contract includes or whether schema acceptance preserves domain meaning.

Serialization systems make direction and representation concrete. The Protocol Buffers [proto3 language guide](https://protobuf.dev/programming-guides/proto3/#updating) distinguishes binary wire-safe, wire-compatible, and wire-unsafe changes, warns against reusing deleted field numbers, and notes that a wire-safe change can still break application code. Apache Avro's [specification](https://avro.apache.org/docs/1.12.0/specification/) resolves writer and reader schemas using names, aliases, defaults, promotion rules, and exact schema context. Neither mechanism proves that a widened type, default, alias, or enum evolution preserves a consumer's business decision.

Versioning also supports discovery and repeatability. W3C's [Data on the Web Best Practices](https://www.w3.org/TR/dwbp/) recommends a version indicator and version history so consumers can identify revisions, compare them, and reproduce work. A trustworthy data architecture extends that record to models, dependencies, transformations, policies, and evidence.

## Prerequisites and Retrieval

You should understand conceptual, logical, and physical models; canonical models; schemas; contracts; entities and keys; events; temporal modeling; metadata registries; serialization; validation; APIs; deployments; migrations; provenance; security; privacy; and testing.

Retrieve model identity, version identity, revision, release, edition, artifact, digest, tag, branch, immutable, lineage, parent, fork, merge, supersede, deprecate, retire, compatibility, backward, forward, full, transitive, structural, semantic, behavioral, operational, producer, consumer, reader, writer, profile, extension, vocabulary, code list, mapping, migration, backfill, adapter, negotiation, support window, coexistence, cutover, rollback, reconciliation, and historical interpretation.

As a retrieval test, examine the claim “Customer 2.1 is backward compatible.” Ask: Which Customer artifact? Backward in which direction? Which producer and consumer versions? JSON, Avro, database, API, events, or analytics? Which profile, code list, mapping, default, and implementation? Which historical and future values? Which use and policy? What test evidence? Until those coordinates are supplied, the statement is not an actionable compatibility claim.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish model identity, version identity, artifact digest, source revision, deployment, and data-record version;
2. define a version scheme whose scope and change semantics fit conceptual, logical, physical, exchange, vocabulary, mapping, and policy artifacts;
3. classify model changes by structure, semantics, behavior, operations, protection, and historical effect;
4. express compatibility as a directional, scoped, evidence-backed relation among exact producer and consumer versions;
5. evaluate additive, subtractive, restrictive, relaxing, rename, split, merge, type, unit, cardinality, default, code, identity, grain, and temporal changes;
6. construct version lineages for parents, forks, merges, profiles, extensions, mappings, and dependency constraints;
7. discover consumers and stored populations, calculate blast radius, and govern deprecation and support windows;
8. design adapters, transformations, backfills, dual operation, cutovers, reconciliation, rollback, and retirement;
9. preserve exact historical interpretation while meeting retention, privacy, security, and records-management obligations;
10. build executable structural, semantic, behavioral, population, migration, deployment, and recovery evidence for version claims.

## Core Exposition

**Separate the identities.** A continuing model identity answers “which governed subject?” A version identity answers “which released state?” A source-control commit identifies repository state. A digest identifies exact content under a canonicalization rule. A deployment identity identifies running software. A record version identifies one state of a domain record. These may be linked, but none substitutes for another.

For example, `urn:example:model:customer` can remain stable while `2026.3` names a release. The release may contain a logical-model document, JSON Schema, Avro schema, mappings, diagrams, and tests with separate digests. Service build `8.14.2` may implement that model, while customer record version `57` describes an optimistic-lock or history position. Using `version` for all four without qualification creates false joins and invalid comparisons.

**Make releases immutable.** Once consumers can depend on an artifact, changing content behind the same version identifier destroys reproducibility. Correct an error by releasing a new version, even if the correction appears editorial. If byte-level changes do not alter semantics, record that classification; do not erase the earlier bytes.

Use content digests to detect mutation, not to communicate domain compatibility. Define canonicalization when whitespace, key order, generated timestamps, signatures, or equivalent serializations vary. Preserve raw signed artifacts when legal or supply-chain evidence requires exact bytes. A digest proves equality only under its algorithm and input procedure.

**Define the public contract before choosing a scheme.** Semantic Versioning is useful only after the public API is precise. For a data model, the public contract might include element names, identifiers, types, cardinalities, value domains, units, constraints, defaults, null and absence semantics, temporal rules, code lists, ordering, uniqueness, error behavior, privacy classification, and guarantees to named consumer classes.

A semantic version can communicate intended change class, but evidence remains authoritative. A minor version that adds an optional field might break strict validators, exhaustive match statements, database projections, signatures, canonical hashes, payload limits, privacy assessments, or consumers that reject unknown properties. A major number warns of possible incompatibility but does not mean every use is incompatible.

Calendar versions, monotonically increasing revisions, editions, and opaque identifiers can be equally appropriate. Calendar versions reveal release time but not compatibility. Sequential revisions are simple but not descriptive. Content hashes guarantee exactness but are unfriendly for negotiation. Often combine a human release label, immutable identifier, and digest.

**Version artifacts independently but release coherently.** A conceptual model, logical model, physical schema, vocabulary, code list, mapping, profile, API contract, event schema, validation rules, generated code, and documentation have different change rates. Give each durable identity and version. Then define a release manifest that pins a compatible set.

This avoids claiming that a code-list correction requires a new table-schema version while still making the dependency visible. It also prevents a service from advertising logical model `3.0` while silently using mapping `2.4` and vocabulary `2025-11`. A release bill of materials should record exact identifiers, digests, constraints, tools, and provenance.

**Model lineage as a graph.** Linear `previous_version` works only for a single trunk. Real model families fork for jurisdictions, products, tenants, experiments, standards editions, and vendor extensions. A new release may merge two lines or derive a profile from a base without superseding it.

Represent typed edges: `derived-from`, `supersedes`, `corrects`, `profiles`, `extends`, `maps-to`, `compatible-with-under`, and `replaces-for-use`. A version may have multiple parents. Do not infer ancestry merely from numeric comparison. Record whether a fork is temporary, independently governed, or prohibited from merging.

[ISO/IEC 11179-3:2023](https://www.iso.org/standard/78915.html) describes registry facilities for identification, designation and definition, registration, classification, and mapping among registry items. A metadata registry informed by those concerns can preserve distinct model items and relationships rather than flattening everything into one filename and status.

**Classify the full change.** A change record should describe affected elements, old and new assertions, reason, source, authority, dependency changes, expected compatibility, consumers, data population, protection effect, migration, and evidence. Review at least these classes:

- editorial or presentational changes;
- additive or subtractive elements and values;
- relaxed or tightened constraints;
- rename, alias, move, split, merge, and reclassification;
- type, representation, encoding, precision, scale, unit, and reference-system changes;
- optionality, null, absence, default, and cardinality changes;
- identifier, equality, grain, aggregation, and uniqueness changes;
- code-list, vocabulary, definition, authority, and mapping changes;
- temporal validity, recorded history, ordering, retention, and correction changes;
- derivation, validation, workflow, decision, privacy, access, and lifecycle changes.

“No schema diff” does not mean no model change. A definition can change while the field remains a string. A currency can change while the number remains decimal. A policy can reinterpret absence. A new derivation can change a metric. These semantic-only changes may be the most dangerous because structural tools cannot see them.

**Define compatibility direction explicitly.** Let `P_o` be an old producer, `P_n` a new producer, `C_o` an old consumer, and `C_n` a new consumer. One backward-reading test might ask whether `C_n(P_o(data))` succeeds and preserves required meaning. One forward-reading test might ask whether `C_o(P_n(data))` does so. State the convention instead of trusting the adjective.

Full compatibility usually combines both directions. Transitive compatibility extends a claim across all supported prior versions rather than only the immediately previous version. Pairwise compatibility is not automatically transitive: adapters, defaults, accumulated constraints, and population changes can produce `Compat(A,B)` and `Compat(B,C)` without `Compat(A,C)`.

Compatibility also has a horizon. “All versions since 3.0,” “current and previous minor,” and “records produced in the last 13 months” are different obligations. The registry policy should state which pairs are tested and which remain unsupported.

**Separate compatibility dimensions.** Syntactic compatibility means the representation can be tokenized or decoded. Structural compatibility means it validates against shape and constraints. Semantic compatibility means values preserve defined concepts. Behavioral compatibility means the consumer's outcomes and side effects remain acceptable. Operational compatibility means versions can be deployed, routed, monitored, and recovered together.

A protobuf reader may preserve an unknown field while application code drops it during read-modify-write. An Avro default may allow reading but manufacture a value that was never observed. A JSON Schema validator may accept a document while a consumer treats a newly admitted enum as impossible. Test the dimensions separately and never summarize a narrower result as universal compatibility.

**Treat data population as part of the claim.** Schema-level possibility differs from observed or future data. A type narrowing from 64-bit to 32-bit may pass current data yet reject future valid values. A newly required field may be backfilled for stored rows but absent from messages still produced by offline devices. Conversely, an incompatible theoretical branch may be unreachable under a governed profile.

Define populations: historical store at a snapshot, current production sample, boundary fixtures, generated valid instances, invalid adversarial instances, future contract domain, and protected or rare cohorts. Population evidence can support a bounded migration decision; it cannot redefine the model silently.

**Analyze additions carefully.** Adding an optional field is often reader-friendly but can affect strict `additionalProperties` rules, canonical serialization, signatures, payload size, privacy exposure, object constructors, exhaustive transformations, and round trips. Adding an enum value is safe only when old consumers preserve, ignore, map, or reject it as designed.

The proto3 guide explicitly warns that binary wire-safe changes can break language-level code and advises reserving removed numbers and names. Thus a registry should record wire format, generated-language versions, JSON/text use, unknown-field behavior, and application tests—not simply “protobuf compatible.”

**Analyze removals and renames.** Removal may be safe for a reader that ignores unknown fields but unsafe for producers, required consumers, stored queries, or round trips. Reserve identifiers where the wire format requires it. Deprecate before removal when consumers need time. Preserve aliases or mappings only when they are unambiguous and semantically exact.

Avro aliases can help map a writer's old name to a reader's new name, and defaults can fill a field absent from writer data. The Avro specification also makes the writer schema part of correct interpretation. An alias does not prove that the renamed concept retained identity, nor does a default prove that the synthesized value was historically true.

**Analyze constraints, defaults, and absence.** Tightening a maximum, making an optional field required, reducing cardinality, closing an open vocabulary, or prohibiting null can reject old data. Relaxing a constraint may admit new data that old consumers mishandle. Both directions need examination.

Defaults are executable semantics. Distinguish default-on-write, default-on-read, UI suggestion, missing-value interpretation, and business fallback. Record whether default application changes provenance. `country = US` synthesized for old records is not equivalent to a source-provided country and should not silently become evidence.

**Protect identity and grain.** Changing a business key, entity boundary, equality rule, or record grain affects references and aggregates even if fields retain names. Splitting `Customer` into `Person` and `Organization`, merging household members, or changing one row per order to one row per line requires identity mappings, collision rules, lineage, referential migration, and reconciled counts.

Mappings may be one-to-one, one-to-many, many-to-one, conditional, probabilistic, manual, or impossible. Version the mapping and its decision authority. A crosswalk is not necessarily invertible. Preserve unresolved and conflicting cases instead of fabricating exact correspondence.

**Version units, reference systems, and codes.** A decimal without its unit is not stable meaning. Changing meters to feet, gross to net, nominal to real currency, local to UTC time, or one geodetic reference system to another requires conversion rules, precision and rounding policy, source retention, and acceptance tolerances.

Code values depend on code-system identity and version. Reusing a code for a new meaning destroys historical interpretation. Adding or retiring a code affects exhaustive consumers, reports, and mappings. Version value sets, code systems, language labels, definitions, and equivalence claims separately where their lifecycles differ.

**Represent profiles and extensions.** A base standard version rarely describes the actual local contract. Profiles constrain cardinality, bind value sets, add extensions, select options, or impose workflow rules. A consumer needs base version plus exact profile and dependencies.

OASIS [Universal Business Language 2.4](https://docs.oasis-open.org/ubl/UBL-2.4.html) distinguishes the UBL version from customization and profile identifiers and provides upgrade and schema-change material. The pattern generalizes: base, customization, profile, and implementation release are separate coordinates. Flattening them into “UBL 2.4” hides local incompatibility.

**Negotiate versions at the interaction boundary.** A version can be selected through media types, headers, paths, capability documents, schema identifiers, manifests, or explicit payload metadata. The method must resist ambiguity and downgrade. Multiple indicators must agree or fail under policy.

HL7 FHIR's [version management](https://hl7.org/fhir/versions.html) adapts semantic-version ideas to a specification lifecycle and distinguishes FHIR specification versions from implementing software versions. Its guidance on [managing multiple FHIR versions](https://fhir.hl7.org/fhir/versioning.html) describes capability, media-type, and profile signals and requires a coherent interaction version. This demonstrates why model, specification, profile, interaction, and software coordinates cannot be collapsed.

Version negotiation must define unsupported-version errors, caching, intermediary behavior, fallback, observability, and security. Silent fallback can become a downgrade attack or a semantic error. Do not let a proxy remove the version signal while retaining a cached body under another contract.

**Build a consumer inventory.** Search source repositories, registries, query logs, lineage systems, subscriptions, access records, data contracts, dashboards, exports, notebooks, models, partners, devices, and archival procedures. Name accountable owners and last-seen evidence. “No known consumer” is an uncertainty statement, not proof of no consumer.

Include dormant and delayed paths: quarterly jobs, annual reports, disaster recovery, event replay, dead-letter reprocessing, litigation discovery, partner file exchange, mobile clients, long-lived devices, caches, backups, and derived training data. Define how unknown consumers affect change approval.

**Calculate blast radius through dependencies.** Traverse the version graph across profiles, schemas, code lists, mappings, generated code, transformations, storage, interfaces, products, reports, and controls. Record direct and transitive dependencies with exact constraints. Detect cycles and contradictory requirements.

Impact analysis should ask what can fail, what can change silently, which data must be reinterpreted or transformed, which protections change, and which evidence expires. Rank consequences by consumer use rather than field count. A one-line definition change can have more impact than adding fifty unused elements.

**Deprecate with a contract.** Deprecation communicates intended removal or reduced support. State announcement date, replacement, migration guide, support window, security policy, telemetry, owner, exceptions, and retirement criteria. A warning in documentation is insufficient if consumers cannot discover it in their workflow.

Support may include read compatibility, write acceptance, correctness fixes, security fixes, migrations, or operational hosting; name which. Emergency security retirement may shorten normal windows but still needs risk acceptance and consumer coordination. Do not promise indefinite compatibility while deleting the people and infrastructure needed to maintain it.

**Choose a migration pattern by invariant.** An adapter translates at an interaction boundary. An upcaster converts old events or messages during read. A backfill rewrites or augments stored data. Dual read compares interpretations. Dual write produces two representations. Shadow processing compares outcomes without controlling production. A materialized projection can isolate consumers from source evolution.

Each pattern moves risk. Adapters accumulate complexity and may be lossy. Upcasting makes historical replay depend on current code. Backfills can erase provenance or violate retention. Dual writes can diverge. Shadowing may omit side effects. Projections can become stale. Record ownership, duration, performance, protection, and retirement conditions.

**Design cutover and rollback together.** Define entry criteria, frozen baselines, migration batches, validation, traffic cohorts, canaries, observability, stop conditions, rollback data, and authority. A code rollback may not reverse writes already emitted under the new model. Rollback therefore needs data compatibility, reverse mapping or quarantine, and reconciliation.

For irreversible splits, merges, deletions, or transformations, preserve authorized source evidence and mappings long enough to reconcile. State where information loss is accepted. Test partial completion, retries, duplicates, ordering, concurrent updates, late arrivals, and restoration from backups.

**Reconcile dual operation.** Compare counts, keys, referential coverage, aggregates, null and code distributions, boundary values, decisions, side effects, and protected cohorts. Classify differences as expected mapping effects, timing differences, source defects, implementation defects, or unresolved conflicts.

Do not require byte equality when models intentionally differ. Reconciliation operates on declared invariants and tolerances. Conversely, equal row counts do not prove identity, units, semantics, or decisions. Retain evidence sufficient to explain accepted differences.

**Preserve historical interpretation.** A stored record should resolve the model, writer schema, profile, vocabulary, mapping, rule set, and relevant implementation context used to create or decide from it. Store direct references or ensure deterministic resolution through an immutable manifest.

Historical interpretation differs from converting all history to today's model. Both views can be useful: an as-was view reproduces prior meaning, while a restated view applies a declared new interpretation. Label them and preserve lineage. Never present a lossy migration as the original historical fact.

JSON Schema Draft 2020-12 [Core](https://json-schema.org/draft/2020-12/json-schema-core) defines schema resources, identifiers, dialects, vocabularies, and reference behavior. Pinning the dialect and exact resources matters because the same-looking keywords may be interpreted under different vocabularies or implementations. Validation output should include the schema and dialect identity, not only pass or fail.

**Govern corrections and withdrawn releases.** A flawed release may need a successor, security advisory, withdrawal, or forbidden-use status. Do not mutate it. Record which claims were wrong, affected populations and consumers, containment, replacement, notification, and reassessment evidence.

Withdrawal does not mean erasure. Historical decisions may still need the artifact under restricted access. If law or privacy requires deletion, retain a non-sensitive tombstone, digest, lineage, and limitation where authorized so absence is not mistaken for a version that never existed.

**Integrate security and privacy.** A model change can introduce sensitive fields, broaden allowed values, reduce minimization, change purpose, expose inference, alter access partitions, weaken validation, or retain legacy data. Threat-model parsers, adapters, registries, negotiation, and downgrade behavior.

Old versions often lack later security controls. Support windows need vulnerability and incident policy. Migration copies, dual stores, fixtures, and compatibility logs expand exposure. Apply classification, least privilege, encryption, retention, deletion, redaction, audit, and non-production-data rules to every versioned artifact and population.

**Use registries as evidence systems, not oracles.** A schema registry can store artifacts, enforce configured compatibility algorithms, and associate subjects with versions. Its result is bounded by supported format, configuration, normalization, and comparison scope. It may not know application behavior, semantics, population, privacy, deployment order, or historical mapping.

Record registry product and policy version, subject naming, compatibility mode, exemptions, and test result. Require additional semantic and operational review proportional to consequence. An administrator changing registry mode is itself a governed policy version change.

**Test claims at multiple levels.** Static schema diffing catches structural changes. Reader-writer matrices test exact implementation pairs. Golden fixtures test known boundaries. Generative tests explore valid and invalid domains. Property tests assert invariants. Historical replays test stored populations. Differential and shadow tests compare outcomes. Migration rehearsals test operations, and recovery exercises test rollback.

Include negative tests: unknown versions, conflicting indicators, removed codes, extreme numbers, absent and null fields, unknown enums, malformed payloads, old signatures, partial migrations, duplicate writes, delayed events, and unauthorized legacy access. Evidence should record tool versions, artifacts, digests, fixtures, environment, results, and limitations.

**Make lifecycle states enforceable.** Useful states include draft, candidate, released, deprecated, withdrawn, retired, and archived. Define permitted transitions and who authorizes each. Draft identifiers must not masquerade as released stability. A candidate may be immutable for testing yet unsupported for production.

Retirement requires more than elapsed time. Verify consumer cessation, stored-data strategy, replay and recovery paths, legal and records obligations, security disposition, archive readability, mapping availability, and operational removal. Keep lifecycle state queryable at both current and historical times.

**Record uncertainty honestly.** Some old artifacts, consumers, meanings, or mappings will be unknown. Mark them unknown with search evidence, risk, owner, and disposition. Do not invent parentage, compatibility, effective dates, or semantic equivalence to make a registry look complete.

Version governance succeeds when a future investigator can retrieve the exact artifact, understand the change and authority, determine the supported uses, reproduce evidence, and explain migrations and limitations. Neat version strings are helpful; preserved meaning is the objective.

## Definitions and Notation

Let `M` be a stable model identity and `V_i` an immutable released version of it. Let `A(V_i)` be the set of artifacts in its release manifest and `H(a)` the recorded digest of artifact `a` under a declared algorithm and canonicalization. Integrity requires retrieved `a'` to satisfy `H(a') = H(a)`; that equality says nothing by itself about correctness or compatibility.

Let `P_i` and `C_j` denote exact producer and consumer implementations associated with model versions. Define:

`Compat(P_i, C_j, u, D, p, t, E)`

where `u` is the use, `D` the relevant data population or domain, `p` the compatibility policy, `t` the time or support horizon, and `E` the evidence. The predicate is directional. Swapping producer and consumer requires a separate evaluation.

Let `G = (V, E)` be a version lineage graph. Nodes are exact artifact or release versions. Typed directed edges record parentage, derivation, profiling, extension, mapping, correction, or supersession. A numeric ordering function may order labels inside one scheme, but it does not create lineage edges or prove reachability.

For a change set `Δ(V_i,V_j)`, define a classification vector:

`K = (syntax, structure, semantics, behavior, operations, protection, history)`

Each coordinate records affected or unaffected, evidence, uncertainty, and consequence. A release is not “non-breaking” merely because its syntax coordinate is unchanged.

A mapping `f: D_i -> D_j` may be partial, many-to-one, or lossy. Record its domain, codomain, version, preconditions, output provenance, and loss function `L(x)`. If no inverse exists, rollback cannot rely on `f^-1`; it must retain source evidence or use another governed reconstruction.

Distinguish lifecycle time from business effectivity. `released_at`, `deprecated_at`, and `retired_at` describe model governance. `effective_from` describes when the model is authorized for a use. Recorded-time history describes when the registry held each assertion. These can differ and may require bitemporal treatment from [DARCH-018](018-temporal-and-historical-modeling.md).

## Mechanisms, Invariants, or Proof Structure

Use ten gates for each release or compatibility claim.

**1. Baseline gate.** Resolve the stable model identity, exact parent versions, immutable artifacts, digests, source revisions, release manifest, authority, and reproducible retrieval.

**2. Identity gate.** Verify element identity, keys, grain, references, profiles, extensions, vocabulary identities, and independent artifact versions. Reject ambiguous reuse of names, codes, or identifiers.

**3. Change-classification gate.** Review structural, semantic, behavioral, operational, protection, and historical effects, including changes invisible to schema diff tools.

**4. Dependency gate.** Traverse direct and transitive dependencies across models, schemas, code lists, mappings, rules, generated code, services, data products, archives, and controls.

**5. Compatibility gate.** State direction, exact producer and consumer, use, format, policy, population, horizon, and evidence. Test pairwise and transitive claims explicitly.

**6. Consumer gate.** Inventory active, dormant, external, unknown, batch, replay, archive, device, and recovery consumers; assign owners and assess consequence and uncertainty.

**7. Migration gate.** Specify adapters, transformations, backfills, coexistence, reconciliation, cutover, rollback, information loss, late data, and failure handling.

**8. Protection gate.** Reassess classification, minimization, authorization, validation, threat model, downgrade resistance, retention, deletion, audit, and sensitive migration copies.

**9. Evidence gate.** Preserve schema diffs, reader-writer matrices, fixtures, semantic assertions, population analysis, replay, migration rehearsal, deployment observations, recovery results, approvals, and limitations.

**10. Lifecycle gate.** Define candidate, release, deprecation, correction, withdrawal, support, retirement, archive, notification, and historical-resolution rules with accountable authority.

The executable example checks four narrow release-record invariants: released artifacts are immutable, lineage names a parent, compatibility claims have tests, and breaking changes have migrations.

<!-- bijux-verify: {"id":"model-version-integrity","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"models=4\nvalid=0\nfindings=customer-schema:mutable-release,order-model:missing-lineage,pricing-mapping:untested-compatibility,risk-profile:missing-migration\nready=false\n","stderr":""}} -->
```python
models = (
    {"id": "customer-schema", "release_immutable": False, "parent_version": "1.4.0", "compatibility_tests": True, "breaking": False, "migration": ""},
    {"id": "order-model", "release_immutable": True, "parent_version": "", "compatibility_tests": True, "breaking": False, "migration": ""},
    {"id": "pricing-mapping", "release_immutable": True, "parent_version": "3.2", "compatibility_tests": False, "breaking": False, "migration": ""},
    {"id": "risk-profile", "release_immutable": True, "parent_version": "2.0", "compatibility_tests": True, "breaking": True, "migration": ""},
)

findings = []
valid = 0
for model in models:
    local = []
    if not model["release_immutable"]:
        local.append("mutable-release")
    if not model["parent_version"]:
        local.append("missing-lineage")
    if not model["compatibility_tests"]:
        local.append("untested-compatibility")
    if model["breaking"] and not model["migration"]:
        local.append("missing-migration")
    if local:
        findings.extend(f"{model['id']}:{finding}" for finding in local)
    else:
        valid += 1

print(f"models={len(models)}")
print(f"valid={valid}")
print("findings=" + ",".join(sorted(findings)))
print(f"ready={str(valid == len(models)).lower()}")
```

The checker validates four declared registry predicates only. It does not prove artifact authenticity, semantic identity, actual compatibility, complete consumer discovery, mapping correctness, migration safety, privacy, security, deployment coexistence, rollback, historical interpretation, or accountable approval. Those require exact artifacts, domain expertise, representative populations, implementation matrices, operational rehearsals, protected evidence, and independent challenge.

## Alternatives and Trade-Offs

**Semantic versus calendar versus opaque versions.** Semantic versions communicate intended compatibility when the public contract is precise. Calendar versions communicate release cadence. Opaque revisions avoid overclaiming. Combine human labels with immutable IDs and digests where useful.

**Single release version versus independently versioned artifacts.** One number is easy for users but hides divergent schemas, vocabularies, mappings, and profiles. Independent versions are accurate but increase dependency complexity. A pinned release manifest provides a coherent middle layer.

**Version in path versus metadata.** Paths are visible and easy to route but can spread version concerns through clients. Headers, media types, capability documents, or payload metadata separate identity from location but can be stripped, cached incorrectly, or ignored. Define one authoritative negotiation policy and consistency rules.

**Strict rejection versus tolerant reading.** Strict readers expose unexpected change early. Tolerant readers support evolution but can ignore meaningful data or produce lossy round trips. Tolerance must be intentional, observable, and bounded by semantics.

**Transform on read versus migrate on write.** Read-time transformation preserves raw history and delays cost but makes every read depend on adapters. Write-time migration simplifies later reads but can be irreversible and operationally expensive. Many systems retain raw source plus versioned normalized projections.

**Central registry versus federated ownership.** A central registry improves discovery and uniform controls but can become a bottleneck or false oracle. Federated registries preserve domain authority but complicate cross-domain resolution. Federate ownership with common identifiers, evidence fields, and discovery protocols.

**Flag-day versus coexistence.** A flag-day avoids long-lived adapters but concentrates coordination and rollback risk. Coexistence supports gradual migration but increases dual behavior, storage, and reconciliation. Select by consumer control, consequence, and reversibility.

**Preserve old runtime versus preserve interpretable artifacts.** Keeping old software can reproduce behavior but creates security and operability risk. Reimplementation from preserved specifications may differ. High-consequence histories may require immutable artifacts, test vectors, emulation strategy, and documented limits rather than indefinite public exposure.

## Failure Modes and Misconceptions

1. **A version number proves compatibility.** It communicates a claim under a scheme; evidence proves only bounded relations.
2. **Semantic Versioning applies automatically to data models.** It first requires a precise public contract and change semantics.
3. **An additive field is always safe.** Strict readers, signatures, exhaustive code, limits, privacy, and round trips may break.
4. **Schema validation proves semantic compatibility.** A valid value can change units, definitions, authority, or decisions.
5. **Backward and forward are self-explanatory.** Always state producer-reader direction and use.
6. **Pairwise compatibility is transitive.** Defaults, adapters, constraints, and accumulated changes can invalidate distant pairs.
7. **A rename with an alias is identical.** The concept may have changed despite mechanical resolution.
8. **Defaults recover missing historical facts.** They synthesize values and require distinct provenance.
9. **Wire-safe means application-safe.** Generated code, business logic, and read-modify-write behavior can still fail.
10. **The base standard version identifies the contract.** Profiles, extensions, vocabularies, mappings, and local rules also matter.
11. **No known consumers means no consumers.** Dormant, external, archival, replay, and unknown paths require risk treatment.
12. **Dual write guarantees equivalence.** Partial failures, retries, ordering, and lossy mappings cause divergence.
13. **Rollback is just deploying old code.** New-model writes may be unreadable or semantically irreversible.
14. **Historical data should always be upgraded in place.** That can erase as-was meaning, evidence, and reproducibility.
15. **Registry compatibility settings are sufficient governance.** They rarely cover semantics, populations, privacy, operations, or retirement.
16. **Old versions can be retained forever without cost.** They expand attack surface, privacy exposure, and maintenance obligations.
17. **One linear predecessor field captures lineage.** Forks, merges, profiles, corrections, and mappings require typed graph relationships.

## Worked Examples

### Example 1

A team changes `customer_id` from a locally assigned integer to a global string and calls it a physical migration. The change alters identity, equality, references, deduplication, and collision policy. The release versions the logical model and mappings, retains both identifiers during coexistence, reconciles one-to-many conflicts, and prevents an automatic rollback that would discard global-only identities.

### Example 2

An Avro reader adds a default country of `US`, allowing it to read older records. Structural resolution succeeds, but international historical records without country are now misclassified. The corrected design records `UNKNOWN` with synthesized provenance, backfills only from authoritative evidence, and bounds compatibility to parsing rather than factual equivalence.

### Example 3

A protobuf message removes field 7 and later reuses field 7 for a different concept. Delayed messages are decoded with the new meaning. The team restores field-number reservation, withdraws the unsafe schema, inventories stored payloads, quarantines ambiguous data, and adds registry checks for reserved numbers and names.

### Example 4

An API adds an enum value `PENDING_REVIEW`. Its wire schema is accepted, but an older mobile client uses an exhaustive branch and crashes. Compatibility evidence expands from schema diffing to generated-client matrices, unknown-value tests, telemetry, and an explicit fallback behavior before release.

### Example 5

A billing model changes `amount` from cents as integer to major currency units as decimal without changing the field name. Every document remains syntactically valid while totals change by 100. The model introduces an explicit amount type with currency and scale, publishes a breaking version, converts with declared rounding, and reconciles invoices and ledger postings.

### Example 6

Two jurisdictions profile the same base claims standard. Both advertise base version 4.0, but one requires a national identifier and the other forbids it. Exchanges negotiate base, profile, and value-set versions; mismatched indicators fail rather than silently selecting the base schema.

### Example 7

A warehouse backfills all history into model 3 and deletes model 2 columns. A regulator later asks what a 2024 decision meant under then-current rules. The architecture retains authorized raw model-2 evidence, immutable rule and vocabulary versions, and a versioned mapping so it can present both as-was and restated views with limitations.

### Example 8

During dual write, the old store succeeds and the new store times out. A retry creates duplicate new records while a later correction reaches only the old store. The migration adds idempotent identities, a durable change log, completeness checkpoints, bidirectional reconciliation, quarantine, and cutover criteria based on decisions rather than row counts.

### Example 9

A schema registry reports that version 12 is backward compatible with version 11. A fraud service still changes approvals because a code definition was revised outside the schema. The release manifest pins the code system and decision rule, semantic fixtures cover affected cases, and registry success is recorded as structural evidence only.

### Example 10

A deprecated clinical profile reaches its retirement date, but disaster-recovery tests reveal archived messages that only the old validator can interpret. Retirement pauses until the archive has exact schemas, value sets, conversion tests, restricted retrieval, and a recovery path. The obsolete public endpoint can close without losing authorized historical interpretation.

## Cross-Program Connections

- **API and service engineering:** media types, paths, capability negotiation, consumer contracts, generated clients, deprecation, and gateway routing expose versions.
- **Platform engineering:** registries, artifact stores, provenance, policy enforcement, deployment orchestration, telemetry, secrets, recovery, and retirement operationalize them.
- **Data engineering:** schema evolution, CDC, event replay, lake formats, backfill, dual pipelines, point-in-time processing, and quality rules depend on exact versions.
- **Database engineering:** migrations, views, constraints, online schema change, temporal tables, catalogs, and rollback implement model transitions.
- **Programming languages:** algebraic data types, exhaustive matching, codecs, package constraints, type generation, and property tests reveal compatibility boundaries.
- **Distributed systems:** rolling deployment, delayed messages, retries, partitions, caches, and partial failure require coexistence and reconciliation.
- **Security and privacy:** downgrade attacks, legacy vulnerabilities, purpose change, minimization, sensitive migrations, retention, and deletion affect support policy.
- **Systems engineering:** configuration baselines, effectivity, traceability, change control, safety cases, maintenance, and retirement supply lifecycle assurance patterns.

## References

1. Preston-Werner, T., *Semantic Versioning 2.0.0*. <https://semver.org/spec/v2.0.0.html>
2. Google, *Protocol Buffers Language Guide (proto3): Updating a Message Type*, current documentation. <https://protobuf.dev/programming-guides/proto3/#updating>
3. Apache Software Foundation, *Apache Avro 1.12.0 Specification*. <https://avro.apache.org/docs/1.12.0/specification/>
4. W3C, *Data on the Web Best Practices*, W3C Recommendation, 2017. <https://www.w3.org/TR/dwbp/>
5. Bhutton, B., et al., *JSON Schema: A Media Type for Describing JSON Documents*, Draft 2020-12 Core. <https://json-schema.org/draft/2020-12/json-schema-core>
6. ISO/IEC, *11179-3:2023 Information technology—Metadata registries—Part 3: Metamodel for registry common facilities*, 2023. <https://www.iso.org/standard/78915.html>
7. HL7 International, *FHIR Version Management Policy and Managing Multiple FHIR Versions*, Release 5. <https://hl7.org/fhir/versions.html>
8. OASIS Open, *Universal Business Language Version 2.4*, OASIS Standard, 2024. <https://docs.oasis-open.org/ubl/UBL-2.4.html>

## Exercises

### Exercise 1

Define a version record and compatibility claim for an Order logical model, JSON Schema, code list, and mapping released together. Distinguish identities, digests, parents, direction, population, policy, evidence, and lifecycle.

### Exercise 2

Classify a change from optional integer `temperature_celsius` to required decimal `temperature` with a unit code. Analyze old and new producers and consumers, historical data, defaults, precision, privacy, migration, and rollback.

### Exercise 3

Design a reader-writer compatibility matrix for three versions of an event schema. Version 2 adds an enum value; version 3 splits one field into two. Include structural, semantic, behavioral, population, and transitive tests.

### Exercise 4

Plan gradual migration of a customer identity model across twelve services, a warehouse, mobile clients, partner exports, archived events, and disaster recovery. Include discovery, coexistence, reconciliation, cutover, rollback, security, and retirement.

### Exercise 5

A registry reports “backward compatible” for a new schema. Construct an assurance review that determines what the result proves, what it omits, and which additional evidence is required before a high-consequence eligibility service adopts it.

## Answers to the Exercises

### Answer 1

Create stable identities for Order logical model, JSON Schema, fulfillment-status code list, and logical-to-JSON mapping. Each release version names parents, change set, authority, effective use, lifecycle state, artifact URI, digest algorithm and digest, provenance, support window, and dependencies. A bundle manifest pins the four exact versions and its own immutable identity; it does not replace their independent histories.

A compatibility record names old producer, new consumer, Order submission use, JSON representation, relevant profile, historical snapshot plus boundary fixtures, policy version, time horizon, and evidence from schema diff, reader tests, semantic assertions, and decision comparison. The reverse direction is a separate record. Lineage includes derived mapping and profile relationships. Deprecation and retirement remain lifecycle assertions with recorded history, consumer notification, and migration criteria.

### Answer 2

The change renames a field, widens representation from integer to decimal, externalizes unit, changes optionality, and potentially changes precision and absence semantics. A new consumer can read old data only through a mapping that supplies unit `Cel` from the old field's definition and preserves missingness rather than inventing a temperature. A consumer that requires the value cannot accept legitimately absent old records without a governed exception. An old consumer cannot safely read arbitrary new data because the unit may differ and decimal precision may be lost.

Version the logical model, schema, unit vocabulary, and mapping. Retain source value, scale, unit, provenance, and conversion result. Test negative temperatures, decimal boundaries, missing and null values, unexpected units, rounding, and old generated code. Backfill only where source semantics are known; quarantine ambiguous records. Assess whether more precise measurement increases sensitivity. Coexist through an adapter and compare converted values within declared tolerance. Rollback retains the new source because conversion to integer Celsius may be lossy.

### Answer 3

Construct all required ordered pairs among producer versions `P1`, `P2`, `P3` and consumer versions `C1`, `C2`, `C3`, not only adjacent releases. For version 2, test old consumers receiving the new enum, new consumers receiving old values, unknown-value preservation, exhaustive generated code, read-modify-write, and decision fallback. For version 3, test whether the split fields can reconstruct the old field and whether the old field can populate both new concepts without ambiguity.

Structural tests decode and validate. Semantic fixtures state expected meaning. Behavioral tests compare decisions and side effects. Population tests replay representative history and generate boundary instances. Explicitly test `P3 -> C1` even if `P2 -> C1` and `P3 -> C2` pass; compatibility is not assumed transitive. Record format, code generator and runtime versions, profile, policy, fixtures, digests, results, expected loss, and unsupported pairs.

### Answer 4

Inventory synchronous calls, events, tables, caches, code, dashboards, devices, exports, partner agreements, quarterly jobs, archives, replay, backups, and recovery procedures; assign owners and record unknowns. Publish immutable old and new model bundles with identity mappings and protection review. Introduce globally idempotent identifiers and adapters, then migrate controlled cohorts while retaining old references.

Dual reads and writes require durable change capture and reconciliation of identity counts, collisions, references, decisions, late events, and partner acknowledgments. Mobile and partner support windows may determine coexistence length. Secure mapping tables and migration logs as sensitive linking data. Cutover requires consumer telemetry, archive and recovery tests, acceptable reconciliation, and rollback readiness. Rollback retains new writes and reverse-maps only proven cases. Retire old write paths after all criteria pass; preserve restricted schemas, mappings, and interpretable archives for authorized history.

### Answer 5

Record the registry product, version, subject, exact old and new schema digests, normalization, configured compatibility mode, direction, and result. Inspect its algorithm to determine whether it checks immediate or transitive versions, which format rules it understands, and whether aliases, defaults, unknown fields, or references are resolved. That evidence supports only the stated structural relation.

Add a precise eligibility contract; schema and dependency diff; writer-reader matrices for deployed languages and runtimes; fixtures for absence, null, defaults, enums, numerical boundaries, protected cohorts, and invalid data; semantic review of definitions, units, codes, authority, time, and derivations; replay of an authorized historical snapshot; differential eligibility decisions; privacy, security, and downgrade review; rolling-deployment and rollback rehearsal; consumer inventory; migration reconciliation; monitoring; and accountable approval. Document unknown consumers and residual risk. Adoption is justified by this bounded evidence set, not by the registry label alone.
