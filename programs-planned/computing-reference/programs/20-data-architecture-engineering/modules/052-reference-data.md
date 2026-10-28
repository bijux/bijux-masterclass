---
module_id: DARCH-052
program: Data Architecture Engineering
level: 2
module_number: 52
title: Reference Data
status: complete
last_verified: 2026-09-03
---

# Reference Data

## One-Page Review

### Governing question

How should an enterprise govern and distribute shared codes, classifications, units, calendars, locales, statuses, and other reference values so that systems interpret them consistently without freezing change, hiding external authority, breaking historical meaning, or forcing every consumer onto one release at once?

### Essential definitions

- **reference data** is a governed set of values used to classify, constrain, label, route, calculate, or interpret other data across more than one context.
- A **reference-data set** is a named, scoped collection with an identifier, steward, authority, schema, release policy, and lifecycle.
- A **reference value** is an identified member of a set, usually carrying a code, canonical meaning, labels, status, provenance, and effective interval.
- A **code** is a machine-oriented identifier within a declared namespace; its spelling alone does not establish meaning.
- A **label** is a human-readable rendering for a language, audience, or context; labels may change while identifiers remain stable.
- A **release** is an immutable, identifiable publication of a reference-data set and its metadata.
- **effective time** states when a value or relationship applies in the represented domain; **publication time** states when a release became available.
- A **crosswalk** is a versioned set of mappings between values in different schemes, with relationship, cardinality, confidence, context, and provenance.
- A **consumer binding** records which set, release or compatibility range, fields, mappings, and fallback behavior a consumer uses.
- **retirement** ends future use of a value or release while preserving the evidence needed to interpret historical records.

### Central model, mechanism, or theorem

Represent a reference-data architecture as:

`R = (outcomes, sets, authorities, values, semantics, time, mappings, releases, distribution, protection, service, ownership, evidence, lifecycle)`

The stable unit is not an unqualified code such as `A`, `US`, or `01`. It is a value identity inside a named scheme and version or effective context. A useful logical key is therefore `(scheme_id, value_id)`, while interpretation also considers release, valid interval, jurisdiction, language, mapping context, and consumer purpose. Releases are immutable; corrections create new releases or explicitly versioned amendments. Consumers report their bindings, and publishers preserve old releases long enough to replay, audit, migrate, or explain historical facts.

### Critical invariants

- Every shared set has a declared purpose, namespace, authority, steward, schema, consumers, release policy, service expectations, and retirement owner.
- Codes are unique only inside their declared scheme and are never silently recycled for a different meaning.
- Stable value identifiers are separated from mutable labels, descriptions, display order, and implementation metadata.
- Effective time, publication time, ingestion time, and consumer activation time remain distinct.
- Published releases are immutable and content-addressable or otherwise verifiably identified.
- Add, change, deprecate, replace, merge, split, and retire operations have explicit compatibility semantics.
- Unknown, other, not applicable, withheld, invalid, unmapped, and source unavailable remain distinct states.
- Crosswalks state direction, relation, cardinality, version pair, context, confidence or decision, provenance, and unresolved cases.
- Distribution contracts cover API, event, file, cache, embedded, offline, replay, correction, reconciliation, and failure behavior.
- Historical interpretation remains possible after external updates, internal migrations, consumer upgrades, and platform retirement.

### Common failures

Common failures are treating reference tables as ownerless configuration; assuming a short code is globally unique; editing a published release in place; using current labels to explain old events; confusing effective time with load time; accepting upstream changes without impact analysis; copying an external standard without recording its edition or license; inventing local codes without a namespace; mapping many values to one without acknowledging information loss; treating unmapped as other; changing display order as if it were semantic; distributing files without checksums or manifests; embedding lists in application binaries without dependency inventory; allowing stale caches to appear current; supporting only latest-version lookups; deleting retired values that historical facts still reference; measuring success by row counts; and decommissioning a service while consumers, exports, rules, or retained releases remain.

### Compact example

An order-status set publishes release `2026-09`. `ACTIVE` applies until day 10 and `SUSPENDED` applies from day 10. A lookup at day 9 returns `ACTIVE`; a lookup at day 10 returns `SUSPENDED`. Deprecated alias `LEGACY` still resolves to replacement `ACTIVE` for a bounded migration period, while an unrecognized code returns typed state `unresolved`, not `OTHER`. The release, boundary, alias rule, and consumer action are all explicit.

### Connections

[DARCH-017](017-event-schemas-and-information-models.md), [DARCH-018](018-temporal-and-historical-modeling.md), [DARCH-023](023-data-ownership-and-accountability.md), [DARCH-026](026-data-products-and-service-expectations.md), and [DARCH-051](051-master-data-and-golden-records.md) establish schema, time, ownership, product, and shared-entity boundaries. This module establishes reference-data architecture; [DARCH-057](../ROADMAP.md) later deepens shared code sets and controlled vocabularies.

## Governing Question

Shared values appear deceptively small. Country, currency, language, unit, product class, legal form, risk band, order status, reason code, and reporting period may each fit in a compact table. Yet a changed value can alter validation, routing, pricing, aggregation, regulatory reporting, access, and historical interpretation across hundreds of systems.

The governing question is which architecture lets publishers change reference meaning deliberately and lets consumers adopt that change safely. The answer must preserve authority, version, time, mapping, provenance, protection, availability, compatibility, and closure—not merely host a downloadable list.

## Why This Matters

The W3C [SKOS Reference](https://www.w3.org/TR/skos-reference/) models identified concepts, labels, semantic relations, collections, and mappings between concept schemes. OASIS [Code List Representation (Genericode)](https://docs.oasis-open.org/codelist/genericode/v1.0/os/genericode-v1.0-os.html) specifies a model and XML representation for code lists. These specifications demonstrate that a governed scheme contains more than two columns named code and description.

The [IANA Time Zone Database](https://www.iana.org/time-zones) is periodically updated when political decisions change offsets, boundaries, or daylight-saving rules. The IANA [Media Types registry](https://www.iana.org/assignments/media-types/media-types.xhtml) and the [Language Subtag Registry](https://www.iana.org/assignments/language-subtag-registry/language-subtag-registry) demonstrate authoritative registries with explicit namespaces and maintained entries. External authority does not remove enterprise obligations: adopters still choose a release, assess impact, test consumers, preserve evidence, and plan failure behavior.

Unicode [UTS #35](https://unicode.org/reports/tr35/) defines exchange structures for locale data and addresses identifiers, aliases, dates, numbers, currencies, time zones, units, and canonicalization. [RFC 5646](https://www.rfc-editor.org/rfc/rfc5646) defines language tags and their relationship to the IANA registry. HL7 FHIR's [Terminology Module](https://hl7.org/fhir/terminology-module.html) separates code systems from value sets and makes version-aware terminology use explicit. These sources cover different domains, but each shows why namespace, edition, subset, mapping, and consumer context matter.

W3C [PROV-O](https://www.w3.org/TR/2013/REC-prov-o-20130430/) provides a vocabulary for provenance, while NIST [SP 800-160 Volume 1 Revision 1](https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final) frames trustworthy systems engineering across the lifecycle. Reference data is an operational dependency whose origin, transformation, publication, use, recovery, and retirement need evidence.

## Prerequisites and Retrieval

You should understand identifiers, namespaces, logical and physical data models, temporal modeling, schemas, master data, source authority, APIs, events, files, caches, compatibility, lineage, access control, reliability, recovery, and governance.

Retrieve reference data, scheme, set, value, code, stable identifier, label, description, definition, namespace, authority, steward, provenance, release, edition, effective time, publication time, deprecation, replacement, alias, crosswalk, mapping relation, cardinality, subset, profile, consumer binding, immutable publication, checksum, cache, reconciliation, migration, and retirement.

As a retrieval test, inspect “use the standard country list.” Ask which standard and edition, which territories and exceptional values, which identifiers, whether historical entities matter, which labels and languages, which consumers, which effective date, what local extensions exist, who approves an update, how mappings work, and what happens when the upstream source or distribution path is unavailable.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish reference data from master data, transactions, configuration, metadata, and controlled vocabularies;
2. define reference-data sets, namespaces, value identities, labels, semantics, authority, provenance, and lifecycle;
3. model releases, effective intervals, corrections, aliases, deprecations, replacements, merges, splits, and retirement;
4. separate source editions from enterprise releases and consumer activation;
5. design crosswalks that expose direction, relation, cardinality, context, confidence, and information loss;
6. compare APIs, events, files, databases, libraries, embedded snapshots, and federated lookup;
7. define compatibility, migration, cache, offline, failure, replay, reconciliation, and recovery behavior;
8. protect sensitive classifications, licensed lists, mappings, usage evidence, and administrative operations;
9. assign publisher, source, domain, platform, consumer, protection, incident, and retirement responsibilities; and
10. measure adoption, freshness, mapping coverage, unsafe drift, decision outcomes, cost, and verified closure.

## Core Exposition

**Start with decisions and interpretations.** Identify the facts whose meaning depends on the set, the decisions that use them, actors, deadlines, consequences, and tolerable fallback.

A list shared only because copying is convenient may not justify enterprise governance. A small list that changes payment routing or statutory reporting may require strict release assurance.

**Define reference data by behavior.** Reference data classifies, constrains, labels, routes, calculates, or interprets other data. Values are reused and change on a governed cadence.

Size does not decide the category. A large taxonomy can be reference data; a three-value workflow state can be local configuration if it has no shared semantic contract.

**Distinguish master data.** Master data describes individually managed entities such as suppliers, products, parties, locations, or assets. Reference data supplies categories, statuses, units, and allowed values used to describe them.

A currency code is reference data; an issued payment instrument is not. A product category is reference data; a product with identity, ownership, and lifecycle is master data.

**Distinguish transactions and observations.** An order status value is reference data. The event that an order entered that status at a particular time is transactional history.

Do not overwrite events when a label or mapping changes. Interpret each fact against the scheme and temporal context it actually used.

**Distinguish configuration.** Configuration controls how one implementation behaves. Reference data carries shared domain meaning across contexts.

The boundary can move. A routing reason created locally can become enterprise reference data when several products depend on consistent semantics and governance.

**Distinguish metadata and vocabulary.** Reference-data entries have metadata such as owner, source, release, and provenance. A vocabulary may provide richer linguistic and semantic relationships than an operational list.

This module focuses on enterprise architecture around governed values and releases. DARCH-057 develops controlled-vocabulary design more deeply.

**Inventory sets before centralizing them.** Record scheme identifier, purpose, authority, source, fields, value count, change rate, consumers, contracts, protection, local extensions, mappings, and historical requirement.

Find embedded constants, spreadsheet copies, database tables, vendor packages, validation rules, transformation code, reports, models, caches, and manual procedures. The visible reference service is rarely the whole dependency graph.

**Give every scheme a namespace.** Codes are unique only within a set. `A`, `01`, `USD`, or `ACTIVE` has no stable meaning without the scheme identifier.

Use durable scheme and value identifiers. Do not infer namespace from a file path, database name, application, label, or current publisher hostname unless that is an intentional stable contract.

**Separate identity from notation.** A value identity should survive changes to its preferred code, spelling, label, description, language, ordering, or publication format when the underlying concept remains the same.

Some external schemes define the code itself as the identifier. Preserve that rule, but still qualify it by scheme and version and avoid encoding mutable display meaning into internal keys.

**Separate code from label.** Codes serve machine exchange; labels serve people in languages and contexts. A label can be corrected without changing value identity.

Store language and audience for labels. Do not use English text as a primary key, and do not assume one translation preserves every legal or domain nuance.

**Write definitions, not only descriptions.** A useful entry states inclusion, exclusion, scope, authority, and examples where ambiguity matters.

“Inactive” is weak if one system means temporarily unavailable and another means permanently closed. A shared code is valuable only when consumers share enough interpretation.

**Record source authority.** For an external set, record organization, authoritative location, edition, terms, retrieval evidence, checksum, and local transformation.

For an internal set, name the business owner empowered to define meaning and the steward responsible for operations. Platform teams can publish a set without owning its semantics.

**Model enterprise adoption separately.** An upstream edition is not automatically the enterprise release. The organization may validate, subset, extend, map, translate, or schedule it before publication.

Keep source edition, ingestion generation, enterprise release, and consumer activation separate so teams can explain which content was available and which content a decision actually used.

**Make releases immutable.** A release binds scheme metadata, schema version, entries, relations, mappings, provenance, validation evidence, and publication time.

If an error is found, publish a corrected release or an explicitly governed amendment. Silent in-place edits destroy reproducibility and cache coherence.

**Use verifiable release identity.** Give every release a durable version and manifest. Include file names, sizes, digests, record counts, schema, source editions, creation process, and signatures where consequence warrants them.

A semantic version alone is not content evidence. A digest alone is not a compatibility promise. Use both when each answers a different question.

**Separate temporal axes.** Effective time describes the domain. Publication time describes publisher availability. Ingestion time describes platform receipt. Activation time describes consumer use.

A tax classification may become legally effective before a consumer deploys it. A corrected release may be published today about a period last year. One `updated_at` field cannot represent these cases.

**Define interval boundaries.** State whether intervals are closed, open, or half-open and which time zone and calendar apply. Half-open `[start, end)` intervals avoid overlap at adjacent boundaries.

Validate that values expected to be exclusive do not overlap and that required coverage has no gap. Preserve planned future values without making them active early.

**Do not recycle codes silently.** Reusing a retired code for new meaning makes historical records ambiguous, especially when facts omit scheme release.

Prefer permanent retirement or a new identifier. If an external authority reuses notation, preserve edition and effective context and assess whether an internal stable identifier is required.

**Model change types explicitly.** Addition, label correction, definition change, metadata change, deprecation, replacement, alias, merge, split, scope change, and deletion have different consumer effects.

Classify each change semantically. A one-character edit to a definition can be more disruptive than adding ten unused values.

**Deprecation is not deletion.** Deprecated values remain interpretable but should not be selected for new facts after a stated boundary.

Publish warning, replacement if one exists, effective and support dates, migration guidance, and exception path. Not every deprecated value has a one-to-one replacement.

**Represent replacement carefully.** A replacement relation can be exact, broader, narrower, context-dependent, or absent.

If old value `RETAIL` splits into `STORE` and `ONLINE`, mapping old facts automatically loses information. Preserve `RETAIL` historically and require context or unresolved state for forward migration.

**Treat merge and split as migrations.** A merge may combine previously distinct meanings; a split may require information not present in old records.

Version mappings, identify affected consumers and facts, simulate impact, and define whether old data is preserved, reclassified, or left explicitly unresolved.

**Make exceptional states typed.** Unknown means the value is not known; other means known but outside enumerated categories; not applicable means the classification does not apply.

Withheld, redacted, invalid, unmapped, pending, source unavailable, and retired are also different. Collapsing them into `UNKNOWN` or null damages quality measurement and decisions.

**Control local extensions.** Some consumers need values absent from an external scheme. Give extensions their own namespace, owner, definition, protection, lifecycle, and mapping status.

Do not forge upstream-looking codes. Decide whether an extension can cross organizational boundaries and what happens if the authority later creates a colliding or equivalent value.

**Model subsets as products.** A value set used for one field may select part of a larger code system and add constraints, ordering, or context.

Record the source scheme and version, inclusion rules, exclusions, owner, intended field, and expansion evidence. Copying selected rows creates a new governed artifact even when values originate elsewhere.

**Treat crosswalks as first-class data.** A mapping connects a source scheme version to a target scheme version in a declared direction and context.

Record source value, target value or set, relation, cardinality, rule or reviewer, confidence where applicable, evidence, effective interval, status, and unresolved reason.

**State mapping relation.** Exact equivalence, close equivalence, broader, narrower, related, transformed, and no-match are not interchangeable.

An `exact` label should be defensible for the intended scope. A many-to-one reporting rollup is usually broader aggregation, not semantic equality.

**State mapping cardinality.** One-to-one is easiest. One-to-many needs selection context; many-to-one loses distinctions; many-to-many often needs rules and source attributes.

Never hide cardinality behind a single target column. Consumers must know whether a deterministic answer exists.

**Preserve mapping direction.** A source-to-target mapping may not be invertible. Broader and narrower relations reverse, while transformation rules may discard source detail.

Publishing both directions by mechanically swapping columns creates false claims. Validate each required direction independently.

**Version both mapping endpoints.** A crosswalk valid for scheme A release 4 and scheme B release 9 may not hold after either changes.

Bind endpoint versions or compatible ranges and test them at publication. “Current-to-current” is not reproducible.

**Design authoring workflow.** Proposals need requester, rationale, affected meanings, effective date, consumers, mappings, protection, and expected compatibility.

Reviewers need domain authority and evidence. High-consequence sets may need separation of duties, dual approval, legal review, scheduled publication, or emergency correction procedures.

**Validate content structurally and semantically.** Structural checks cover schema, types, uniqueness, required fields, interval form, referential integrity, and manifest digest.

Semantic checks cover definitions, overlap, exclusivity, hierarchy cycles, mappings, allowed transitions, jurisdiction, language, authority, and domain-specific rules. Passing JSON Schema does not prove sound classification.

**Test changes against consumers.** Build an impact inventory from declared bindings, runtime observations, contracts, embedded dependencies, rules, reports, models, and manual work.

Test new values, removed values, label changes, mapping drift, ordering, payload size, latency, cache refresh, historical queries, offline operation, rollback, and unknown behavior.

**Publish release notes for machines and people.** Provide a machine-readable change set plus human explanation of meaning, effective dates, compatibility, migration, and known limitations.

Row-level diffs do not explain why a classification changed. Narrative-only notes do not support automated impact analysis. Publish both.

**Choose distribution by need.** APIs support filtered and current lookup; files support reproducible bulk and offline use; events support change notification; databases support internal query; libraries simplify embedding.

No channel is universally best. A coherent architecture can publish one governed release through several channels while preserving identical identities and manifests.

**Use APIs for bounded lookup.** Define scheme and release selection, value lookup, search, pagination, language, effective-time queries, error types, caching headers, authorization, and rate limits.

Avoid an endpoint that returns “the current meaning” without exposing the resolved release. Support historical lookup when facts and audits require it.

**Use files as immutable artifacts.** Publish complete snapshot, schema, manifest, checksum, source and license metadata, release notes, and optional delta.

Consumers should verify integrity before activation and install atomically. Partial extraction or mixing files from different releases must fail visibly.

**Use events as notifications or changes with care.** An event can announce a release, carry an idempotent change, or invalidate caches.

Define ordering, duplicate handling, replay, correction, compaction, retention, and snapshot recovery. Consumers still need a way to establish or repair complete state.

**Govern database sharing.** A shared table can provide low-latency internal reads but couples consumers to physical schema, platform availability, and access topology.

Publish a stable logical contract, isolate releases, prevent consumer writes, expose resolved version, and support export or service alternatives for migration.

**Inventory embedded snapshots.** A library or application image can deliver fast offline lookup and deterministic builds, but values update only when the consumer upgrades.

Record which binary contains which release. Define maximum staleness, emergency override, compatibility window, and end-of-support behavior.

**Design caches as replicas.** Cache keys include scheme, release or resolved channel, language, context, and effective query where relevant.

Use versioned immutable entries or safe invalidation. Define stale-if-error rules by consequence, and never report stale data as fresh merely because the cache responded.

**Support offline and degraded modes deliberately.** A point-of-sale terminal may continue with a pinned tax or currency set; a sanctions-sensitive workflow may need to stop when required reference data is expired.

State maximum age, allowed operations, warnings, reconciliation, and recovery. Availability policy belongs to the decision, not just the platform.

**Define compatibility dimensions.** Schema compatibility concerns fields and types. Semantic compatibility concerns meaning. Population compatibility concerns allowed values. Operational compatibility concerns latency, size, and channel behavior.

Adding an optional field may be schema-compatible while changing the meaning of an existing code is not. Adding a value can break exhaustive switches even if the schema is unchanged.

**Use consumer bindings.** Record consumer, purpose, fields, channel, pinned release or update channel, acceptable range, activation process, fallback, owner, and last confirmation.

Self-declaration is not enough. Compare the registry with request telemetry, artifact downloads, package inventories, database queries, configuration, and business process evidence.

**Separate publish from activate.** A publisher can release content without forcing simultaneous cutover. Consumers may validate and activate in cohorts within an agreed window.

Track release availability, consumer readiness, actual activation, exceptions, and end of support. Avoid indefinite multi-version operation without owners and cost limits.

**Make migration observable.** Measure bound consumers, contacted owners, tested consumers, activated releases, failures, exceptions, stale requests, old file downloads, and unresolved mappings.

Traffic decline alone does not prove migration. Batch, offline, seasonal, disaster-recovery, and manual consumers may remain invisible.

**Reconcile replicas and consumers.** Compare release identity, record counts, keyed digests, mappings, effective intervals, and representative queries.

Reconciliation should localize differences. One whole-file checksum detects change but does not show which values or consumers are wrong.

**Plan correction propagation.** A bad value or mapping may have affected validation, transactions, reports, models, and decisions before correction.

Publish correction relation, severity, affected releases and intervals, consumer action, replay guidance, and closure evidence. Updating the source table does not repair downstream consequences.

**Preserve reproducibility.** Retain releases, schemas, mappings, code, manifests, source evidence, and enough execution context to interpret past facts.

Retention need not mean keeping everything forever. Define legal, operational, analytical, and audit periods, then preserve or delete consistently across stores and backups.

**Protect reference data proportionately.** Public code lists may be openly readable, but unpublished classifications, internal risk levels, export-controlled mappings, usage logs, and administrative functions may be sensitive.

Apply authentication, authorization, integrity protection, approval controls, audit, secrets management, and minimization to the relevant surfaces. “Reference” does not mean harmless.

**Respect licenses and attribution.** External data can impose access, redistribution, attribution, modification, or update conditions.

Record terms with each source and derived release. Ensure files, APIs, caches, backups, and downstream exports remain permitted before treating external data as an unrestricted enterprise asset.

**Engineer the service.** Define availability, latency, throughput, release frequency, propagation, freshness, retention, support window, error budget, and capacity.

Observe by scheme, release, channel, region, consumer, cache state, lookup result, mapping state, and error type. Aggregate uptime can hide a stale or incomplete critical set.

**Control release failure.** Use staged validation, signed or verified artifacts, canaries, cohort activation, compatibility tests, rollback, and preserved prior release.

If consumers write new facts with a new value, rolling the publisher back may not make those facts understandable to old consumers. Rollback planning includes population compatibility and forward repair.

**Recover more than the current rows.** Recovery includes identities, releases, histories, mappings, source editions, manifests, signatures, permissions, consumer bindings, workflows, audit, and publication positions.

Exercise restore into isolation, verify digests and relations, then reconcile representative consumers. A database restore alone may reproduce neither service behavior nor evidence.

**Assign decision rights.** Domain owners define semantics; source authorities define external or upstream content; stewards operate workflow; platform teams run publication; consumers own correct binding and migration.

Security, privacy, legal, records, reliability, finance, and incident owners contribute according to consequence. A central data office cannot absorb every domain decision by declaration.

**Measure usefulness, not table volume.** Useful measures include semantic defects, unsafe unknown handling, mapping coverage by consequence, consumer staleness, correction time, release adoption, decision error, support burden, and cost.

Counts of lists, values, downloads, or API calls are context. They do not prove consistent interpretation or improved outcomes.

**Plan succession and retirement.** Define how authority, namespace, releases, aliases, mappings, consumers, contracts, retained history, and obligations move or close.

Stop authoring, then publication, channels, credentials, and infrastructure only after consumer and retention evidence permits it. Test that old caches, packages, jobs, restores, or source feeds cannot resurrect unsupported data.

## Definitions and Notation

Let a reference value version be:

$$
v=(S,id,c,L,D,τ_e,τ_p,σ,P),
$$

where $S$ is scheme identity, $id$ is stable value identity, $c$ is code notation, $L$ is a language- and context-qualified label set, $D$ is definition and relations, $\tau_e$ is effective interval, $\tau_p$ is publication evidence, $\sigma$ is lifecycle status, and $P$ is provenance.

Let immutable release $r_j=(S,j,V_j,M_j,X_j,H_j)$ bind scheme, release identifier, value versions $V_j$, metadata $M_j$, crosswalks $X_j$, and verifiable manifest $H_j$.

For an instant $t$, define half-open applicability:

$$
Applicable(v,t) \iff v.start \leq t \land (v.end=\bot \lor t < v.end).
$$

Let mapping assertion $x=(S_s,j_s,id_s,S_t,j_t,T,κ,γ,C,P)$ record source and target schemes, releases, identifiers, mapping relation $T$, cardinality $\kappa$, confidence or governed decision $\gamma$, context $C$, and provenance $P$.

Define `FitReference(R, u, t)` as a review predicate requiring justified use, stable namespace, accountable authority, explicit semantics and time, immutable releases, qualified mappings, compatible distribution, protected and recoverable operation, consumer evidence, and lifecycle closure for use $u$ at time $t$.

## Mechanisms, Invariants, or Proof Structure

Use ten architecture gates.

**1. Outcome gate.** Name interpreted facts, decisions, consumers, deadlines, harms, fallback, value, and assurance depth.

**2. Scheme gate.** Define set purpose, namespace, identifiers, schema, values, definitions, labels, relations, extensions, and scope exclusions.

**3. Authority gate.** Record external or internal authority, domain owner, steward, provenance, license, approval rights, and escalation.

**4. Temporal gate.** Separate effective, publication, ingestion, and activation time; define interval boundaries, history, planned values, and correction semantics.

**5. Release gate.** Publish immutable identified releases with manifests, checks, source editions, change classification, notes, and retained evidence.

**6. Mapping gate.** Bind endpoint versions, direction, relation, cardinality, context, confidence, provenance, information loss, and unresolved cases.

**7. Distribution gate.** Define API, file, event, database, library, cache, offline, replay, failure, reconciliation, and correction contracts.

**8. Compatibility gate.** Evaluate schema, semantic, population, and operational change; inventory bindings; test consumers; stage activation; and close exceptions.

**9. Service and protection gate.** Bound availability, freshness, integrity, access, licensing, capacity, observability, incident response, recovery, and retained evidence.

**10. Lifecycle gate.** Assign ownership, measure outcomes and cost, manage succession, migrate consumers, retire channels, and verify closure.

Passing these gates establishes evidence for one scoped use. It does not prove that an upstream authority is error-free, every mapping is exact, every consumer has activated, or one publication mechanism fits all consequences.

### Executable evidence

The executable example checks a half-open effective-time boundary and distinguishes deprecated alias resolution from an unknown code.

<!-- bijux-verify: {"id":"reference-release-effective-lookup","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"scheme_id=order-status\nrelease=2026-09\nday_9_code=ACTIVE\nday_10_code=SUSPENDED\nunknown_code=unresolved\ndeprecated_code=LEGACY\nreplacement_code=ACTIVE\nconsumer_action=migrate-before-retirement\n","stderr":""}} -->
```python
release = {
    "scheme_id": "order-status",
    "version": "2026-09",
    "values": [
        {"code": "ACTIVE", "start": 0, "end": 10},
        {"code": "SUSPENDED", "start": 10, "end": None},
    ],
    "aliases": {"LEGACY": "ACTIVE"},
}


def lookup_as_of(day):
    matches = [
        value
        for value in release["values"]
        if value["start"] <= day
        and (value["end"] is None or day < value["end"])
    ]
    assert len(matches) == 1
    return matches[0]["code"]


unknown = "UNKNOWN" if "UNKNOWN" in release["aliases"] else "unresolved"

print(f"scheme_id={release['scheme_id']}")
print(f"release={release['version']}")
print(f"day_9_code={lookup_as_of(9)}")
print(f"day_10_code={lookup_as_of(10)}")
print(f"unknown_code={unknown}")
print("deprecated_code=LEGACY")
print(f"replacement_code={release['aliases']['LEGACY']}")
print("consumer_action=migrate-before-retirement")
```

The result proves only the declared boundary, uniqueness assertion, alias lookup, and typed unresolved result for one in-memory release. It does not prove domain semantics, authority, completeness, compatibility, external correctness, clock interpretation, production distribution, cache freshness, consumer activation, protection, recovery, or decision safety.

## Alternatives and Trade-Offs

**Federated ownership with shared contracts.** Domains publish their own sets and a catalog discovers them. This preserves semantic authority but asks consumers to integrate several services and policies.

**Central reference-data service.** One platform supplies workflow, releases, APIs, files, and audit. It reduces duplicated mechanics while risking a bottleneck or false transfer of domain authority.

**Authoritative-source passthrough.** Consumers receive an external scheme with minimal transformation. Provenance stays simple, but local compatibility, subsets, extensions, and outage behavior remain consumer burdens.

**Curated enterprise release.** The organization validates, maps, profiles, and schedules upstream content. It provides coherent adoption at the cost of delay, operations, and potential divergence.

**Pinned versions.** Deterministic interpretation and reproducible builds improve, but consumers can become stale and accumulate upgrade debt.

**Moving channels such as current or supported.** Security and regulatory changes propagate faster, but reproducibility requires recording the resolved release and activation event.

**Lookup API.** Central behavior, filtered results, and current status are convenient; runtime dependency, latency, rate limits, and outage policy become important.

**Immutable snapshot file.** Bulk, replay, and offline use are strong; consumers must install, validate, index, and upgrade it correctly.

**Embedded library.** Local latency and developer ergonomics improve; dependency scanning, release lag, language parity, and emergency correction become harder.

**Exact mappings only.** Claims stay conservative but coverage may be low. Broader or contextual mappings increase utility only if consumers can handle ambiguity and information loss.

**Immediate global activation.** Consistency arrives quickly, but one defect can spread widely and lagging consumers can fail. Cohort activation contains risk while extending multi-version support.

**Retain all releases.** Historical interpretation is easy, but storage, licensing, access, and deletion duties grow. Bounded retention can work when archival and audit needs are explicit.

Choose by consequence, authority, change rate, consumer count, temporal need, offline requirement, mapping ambiguity, protection, license, reliability, migration capacity, cost, and exit.

## Failure Modes and Misconceptions

1. **Reference data is just a lookup table.** The architecture includes authority, meaning, releases, mappings, distribution, consumers, evidence, and lifecycle.
2. **A code is globally meaningful.** A code is interpreted inside a namespace, version, time, and context.
3. **Labels are identities.** Labels are mutable, multilingual renderings.
4. **Current values explain history.** Historical facts may require the release and effective meaning used then.
5. **Publication time equals effective time.** Domain applicability and publisher availability are separate axes.
6. **A standard needs no governance.** Adoption, transformation, testing, licensing, failure, and retirement remain local responsibilities.
7. **A new value is always backward compatible.** Exhaustive consumers can reject or misroute it.
8. **Deprecation means deletion.** Deprecated values remain necessary for interpretation and migration.
9. **Every old value has one replacement.** Splits, merges, and context-dependent changes can be ambiguous.
10. **Unmapped means other.** Lack of a mapping is not a semantic category.
11. **Crosswalks are reversible.** Cardinality and information loss frequently prevent inversion.
12. **Schema validation proves semantic quality.** Valid fields can still encode overlapping, contradictory, or unauthorized meanings.
13. **One current endpoint is enough.** Replay, audit, migration, and correction often require version-specific lookup.
14. **Events eliminate snapshots.** Consumers need bootstrap and repair state.
15. **Caches are transparent.** Staleness, keys, invalidation, and degraded behavior affect decisions.
16. **High availability means current data.** A service can respond successfully with an old or incomplete release.
17. **Download counts prove adoption.** Activation and correct use require consumer evidence.
18. **Turning off the service retires the set.** Embedded copies, files, rules, reports, histories, credentials, and duties remain.

## Worked Examples

### Example 1

Two domains use code `A`: one means active account and another means air shipment. Events carry scheme identifiers as well as codes, preventing accidental joins. **Conclusion:** namespace qualification is part of the value.

### Example 2

A country label changes spelling while the value identity and historical facts remain stable. Interfaces select localized labels from the relevant release instead of rewriting transactions. **Conclusion:** identity and presentation evolve differently.

### Example 3

An upstream time-zone release arrives after a political change. The enterprise validates supported runtimes, publishes a pinned release, canaries affected regions, and tracks consumer activation. **Conclusion:** external authority still requires adoption engineering.

### Example 4

Risk band `MEDIUM` splits into `MEDIUM_LOW` and `MEDIUM_HIGH`. Old records lack the score needed to choose, so the migration preserves `MEDIUM` historically and reports forward mapping as unresolved. **Conclusion:** splits cannot manufacture missing information.

### Example 5

A reporting crosswalk maps five detailed product classes to one regulatory class. It is directional, many-to-one, and broader—not exact. **Conclusion:** cardinality and relation expose information loss.

### Example 6

A mobile application embeds currency metadata. The consumer registry links application build to reference release and blocks use after a bounded support date unless an approved offline exception applies. **Conclusion:** embedded data needs dependency and staleness control.

### Example 7

An API is healthy but its upstream ingestion stalled. Responses include resolved release and age, while a payment workflow rejects an expired compliance set and a reporting workflow uses a marked stale snapshot. **Conclusion:** degraded policy follows consequence.

### Example 8

A corrected mapping changes prior reports. The publisher identifies affected releases and consumers, supplies replay guidance, and obtains reconciled report totals before closing the incident. **Conclusion:** correction extends beyond republishing rows.

### Example 9

A confidential internal investigation status shares the same platform as public locale data. Read paths, administrative changes, logs, exports, and backups receive different controls by set. **Conclusion:** protection is classification-specific, not platform-wide by assumption.

### Example 10

A retired reference service has zero API traffic but an annual batch, old container image, spreadsheet macro, disaster-recovery job, and retained file export still depend on it. Closure waits for migration or explicit retirement of each dependency. **Conclusion:** observed live traffic is incomplete lifecycle evidence.

## Cross-Program Connections

- **Data engineering:** source ingestion, temporal modeling, release assembly, validation, files, events, reconciliation, replay, history, and deletion implement reference-data flows.
- **Platform engineering:** catalogs, workflow, artifact storage, APIs, eventing, caches, policy, telemetry, recovery, tenancy, and paved upgrades support publishers and consumers.
- **API and service engineering:** resource identity, version negotiation, filtering, localization, errors, caching, idempotency, compatibility, and retirement shape lookup contracts.
- **Software engineering:** typed identifiers, exhaustive matching, package dependency management, feature rollout, contract tests, and safe fallback determine consumer behavior.
- **Security and privacy:** integrity, administrative privilege, internal classifications, usage evidence, licensing, access, audit, retention, and incident response constrain operation.
- **Analytics and machine learning:** classifications, cohorts, features, labels, mappings, reproducible training, drift, and historical evaluation depend on pinned meaning.
- **Organizational design:** domain authority, stewardship, platform ownership, consumer responsibility, approval, escalation, and funding make governance real.
- **Reliability engineering:** release failure, stale caches, fan-out, source outage, backpressure, degraded modes, recovery, and correction define service risk.
- **Economics and decision science:** misclassification cost, mapping information loss, upgrade burden, value of consistency, option value, and exit cost guide investment.
- **Systems engineering:** stakeholder outcomes, interfaces, configuration control, provenance, assurance, hazards, lifecycle, and verification frame the whole reference system.

## References

1. W3C, *SKOS Simple Knowledge Organization System Reference*. <https://www.w3.org/TR/skos-reference/>
2. OASIS, *Code List Representation (Genericode) Version 1.0*. <https://docs.oasis-open.org/codelist/genericode/v1.0/os/genericode-v1.0-os.html>
3. IANA, *Time Zone Database*. <https://www.iana.org/time-zones>
4. IANA, *Media Types*. <https://www.iana.org/assignments/media-types/media-types.xhtml>
5. IANA, *Language Subtag Registry*. <https://www.iana.org/assignments/language-subtag-registry/language-subtag-registry>
6. Unicode Consortium, *Unicode Technical Standard #35: Unicode Locale Data Markup Language*. <https://unicode.org/reports/tr35/>
7. IETF, *RFC 5646: Tags for Identifying Languages*. <https://www.rfc-editor.org/rfc/rfc5646>
8. HL7, *FHIR Terminology Module*. <https://hl7.org/fhir/terminology-module.html>
9. W3C, *PROV-O: The PROV Ontology*. <https://www.w3.org/TR/2013/REC-prov-o-20130430/>
10. NIST, *SP 800-160 Volume 1 Revision 1: Engineering Trustworthy Secure Systems*. <https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final>

## Exercises

### Exercise 1

Design reference-data architecture for country, currency, language, status, or classification values used across at least five systems. Define outcomes, schemes, identities, authority, time, releases, mappings, distribution, protection, service, ownership, and retirement.

### Exercise 2

An upstream authority publishes a release that adds two values, deprecates one, changes three labels, and splits one classification into two. Design impact assessment, enterprise publication, consumer activation, and historical interpretation.

### Exercise 3

Scheme A has eight detailed values; scheme B has four broad values. Design a crosswalk that includes one-to-one, many-to-one, one-to-many, and unmapped cases without overstating equivalence.

### Exercise 4

A critical lookup API remains available but serves a release that expired six hours ago because ingestion stalled. Design detection, degraded behavior, incident response, correction, and recovery for low- and high-consequence consumers.

### Exercise 5

An organization plans to retire a central reference-data platform after transferring authoring to domains. Define evidence that consumer dependencies and lifecycle obligations have actually moved or ended.

## Answers to the Exercises

### Answer 1

Name the facts and decisions that use each value, including deadlines, misclassification harms, offline needs, and fallback. Define a durable scheme identifier and stable value identities distinct from code notation and localized labels. Record definitions, inclusion and exclusion, effective intervals, status, source edition, provenance, license, and authority. Separate external authority, domain owner, steward, platform operator, consumer owner, protection owner, and incident decision maker.

Publish immutable enterprise releases with schemas, manifests, digests, source editions, validations, changes, and limitations. Model external-to-enterprise and local-extension mappings with direction, relation, cardinality, context, and unresolved states. Offer channels justified by use: versioned APIs, signed or verified snapshots, release events, internal query, or embedded packages. Register consumer bindings and resolved releases; test history, new values, stale caches, outage, rollback, replay, and correction. Measure decision defects, staleness, mapping coverage, adoption, correction time, and cost. Retain necessary versions, then retire channels, copies, credentials, contracts, and obligations with accountable evidence.

### Answer 2

Retrieve and verify the upstream artifact, edition, publication evidence, terms, and difference from the prior pinned source. Classify changes semantically rather than by row count. New values can break exhaustive consumers; deprecation needs support and migration dates; labels affect interfaces, search, and reports but should not change identity; the split requires context and may leave old facts unresolved. Identify affected validations, switches, mappings, reports, rules, models, files, caches, packages, and manual procedures from declared bindings and observed evidence.

Create an immutable enterprise candidate release, retaining the old release. Validate schema, uniqueness, intervals, definitions, mappings, localization, and manifests. Supply machine change set and human release notes. Run contract, historical, mapping, load, cache, offline, and rollback tests. Canary willing consumers, track actual activation, and retain a compatibility window with an owner and end date. Historical records keep the old value and release; do not invent a split result without evidence. Close only after critical consumers reconcile, exceptions are explicit, and correction and recovery paths have been exercised.

### Answer 3

Bind the crosswalk to exact releases of A and B and declare A-to-B direction and reporting context. Each mapping row records source identity, target identity or set, relation, cardinality, rule or reviewer, confidence if meaningful, provenance, interval, and status. One-to-one values may be exact only when definitions and scope justify that claim. Several detailed A values mapping to one B value are many-to-one broader rollups; acknowledge lost detail and do not mechanically invert them.

An A value mapping to several B values needs a selection rule and additional attributes. If those attributes are absent, return ambiguous or unresolved rather than choose arbitrarily. Values with no defensible target receive typed no-match or unmapped state, not `OTHER`. Test endpoint definitions and representative facts, quantify coverage weighted by consequence, publish known limitations, and version the crosswalk whenever either endpoint or mapping decision changes. Validate any required B-to-A mapping separately because reversal is not implied.

### Answer 4

Detect the stall from source position, expected release or heartbeat, resolved release age, and consumer-specific freshness objectives—not just HTTP success. Freeze publication of incomplete state and preserve the last verified artifact. Responses expose scheme, resolved release, age, and degraded status. Low-consequence consumers may use the pinned stale release within a declared maximum age with warning and later reconciliation. High-consequence consumers may fail closed, queue work, or invoke an approved manual authority when the required set is expired.

Declare an incident with affected schemes, releases, regions, consumers, decisions, and source evidence. Stop retries from amplifying load, restore ingestion into isolation, validate the candidate, compare keyed content and mappings, and publish through a canary. If stale decisions occurred, identify them from consumer bindings and usage evidence, replay or review them, and track acknowledgement. Recover releases, manifests, permissions, histories, mappings, positions, and audit—not only current rows. Close after freshness is restored, critical consumers reconcile, exceptions are owned, and recurrence controls are verified.

### Answer 5

Inventory every scheme, namespace, value history, mapping, source contract, proposal and approval workflow, release, API, event, file, database view, package, cache, validation rule, transformation, report, model, manual procedure, consumer binding, credential, license, backup, retention rule, hold, and correction path. For each semantic decision and operational capability, name the receiving domain or shared service and verify authority, funding, support, protection, recovery, and escalation. Preserve stable identities and version-resolution behavior or publish a governed migration.

Run old and new publication in bounded comparison, migrate consumers by cohort, and reconcile releases, values, mappings, temporal lookups, and representative decisions. Observe long-cycle and offline consumers, not only live API traffic. Stop new authoring, then release publication and channels only after dependencies move or explicitly end. Revoke administrative and consumer access, close workflows, delete prohibited copies, preserve required releases and provenance, transfer license and records duties, and exercise recovery without the old platform. Test that archived jobs, container images, spreadsheets, backups, and disaster-recovery procedures cannot silently restore unsupported reference data.
