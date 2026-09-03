---
module_id: DARCH-057
program: Data Architecture Engineering
level: 2
module_number: 57
title: Shared Code Sets and Controlled Vocabularies
status: complete
last_verified: 2026-09-03
---

# Shared Code Sets and Controlled Vocabularies

## One-Page Review

### Governing question

How should an enterprise design, govern, publish, map, and retire shared code sets and controlled vocabularies so that systems exchange stable identifiers while people retain precise, multilingual, contextual meaning?

### Essential definitions

- A **controlled vocabulary** is a governed collection of identified concepts, labels, definitions, notes, relationships, and lifecycle states used consistently for a declared domain and purpose.
- A **concept** is the identified unit of meaning in a scheme; it remains distinct from its code notation and human-readable labels.
- A **concept scheme** is a named, scoped collection of concepts and semantic relationships under common authority and governance.
- A **code system** assigns codes and meanings within a namespace and version; code equality outside that scope is not semantic equality.
- A **code list** is an enumerated set of coded entries and metadata, often used for exchange or validation.
- A **value set** selects or computes the concepts or codes permitted for a particular field, decision, jurisdiction, workflow, or release.
- A **notation** is a machine-oriented lexical code associated with a concept inside a declared scheme.
- A **preferred label** is the primary human rendering for one language and context; **alternative labels** support synonyms; **hidden labels** can support search without normal display.
- A **definition** states concept meaning and scope; a label alone is not a definition.
- A **semantic relation** connects concepts as broader, narrower, related, equivalent, or another declared relationship.
- A **mapping assertion** states a qualified relation between concepts in different schemes, including direction, versions, context, provenance, and limitations.
- An **expansion** is a versioned materialization of a value-set definition under specific parameters and underlying code-system versions.

### Central model, mechanism, or theorem

Represent vocabulary architecture as:

`V = (outcomes, schemes, concepts, notations, labels, definitions, relations, subsets, mappings, versions, workflows, publication, protection, service, ownership, evidence, lifecycle)`

The stable semantic key is not an unqualified string such as `A`, `LOW`, or `01`; it is concept identity inside a named scheme. Notations and labels can change while concept identity persists. A value set is a governed selection over one or more code systems, not a duplicate code system. A mapping is a claim with relation and context, not a universal equality. Releases and expansions are immutable and reproducible; corrections create new evidence rather than silently altering what historical facts meant.

### Critical invariants

- Every scheme has a stable identifier, purpose, domain boundary, authority, steward, consumers, version policy, and retirement owner.
- Concept identity remains separate from notation, preferred label, alternative label, hidden label, definition, display order, and path.
- Notations are unique according to declared scheme, version, case, and normalization rules and are never silently recycled for different meaning.
- Preferred-label cardinality, language tags, scripts, contexts, and editorial policies are explicit.
- Definitions state inclusion, exclusion, ambiguity, and intended use; labels alone do not carry semantic contracts.
- Direct broader and narrower assertions remain distinct from transitive closure; associative and equivalence mappings use their own relations.
- Code systems, value-set definitions, expansions, and consumer bindings expose exact versions and parameters.
- Add, revise, deprecate, replace, merge, split, map, unmap, and retire operations preserve identity, provenance, history, and consumer impact.
- Exact, close, broader, narrower, related, transformed, and no-match mappings remain distinct and directional.
- Unknown, other, not applicable, invalid, withheld, unmapped, deprecated, and source unavailable remain distinct states.
- APIs, files, events, caches, indexes, and embedded packages expose release, freshness, completeness, compatibility, and correction.
- Protection and licenses follow concepts, internal classifications, mappings, search logs, histories, exports, and backups.

### Common failures

Common failures are using labels as keys; assuming a code is globally meaningful; copying external values without source edition; treating a value set as a code system; assigning two preferred labels in one language without contextual distinction; stripping language tags; defining concepts by circular synonyms; making every relationship `parent`; confusing broader with part-of; claiming exact equivalence from similar labels; inverting many-to-one mappings; recycling deprecated codes; deleting retired concepts referenced by history; changing an expansion in place; using latest terminology for replay; treating successful membership validation as semantic fitness; embedding unversioned lists in applications; counting published concepts as adoption; and retiring a terminology service while consumer bindings, mappings, or old expansions remain.

### Compact example

A risk scheme has three active concepts with stable IDs and one preferred English label each. Deprecated code `MEDIUM` split into `MEDIUM_LOW` and `MEDIUM_HIGH`; therefore its replacement relation is `narrower-choice-required`, and a record lacking the distinguishing evidence remains `unresolved`. The publisher does not choose one replacement or reinterpret history. Release `2026-09`, the split relation, and the migration limitation travel with the vocabulary.

### Connections

[DARCH-017](017-event-schemas-and-information-models.md), [DARCH-018](018-temporal-and-historical-modeling.md), [DARCH-023](023-data-ownership-and-accountability.md), [DARCH-026](026-data-products-and-service-expectations.md), [DARCH-052](052-reference-data.md), and [DARCH-056](056-hierarchy-management.md) establish information, time, ownership, product, reference, and hierarchy boundaries. This module deepens semantic artifacts; [DARCH-058](../ROADMAP.md) next develops master-data change propagation.

## Governing Question

Shared codes determine whether records validate, interfaces render correctly, searches retrieve relevant concepts, decisions route to the right workflow, reports aggregate comparable categories, and systems interpret each other's events. A stable spelling with unstable meaning is more dangerous than an explicit breaking change.

The governing question is which semantic and operational architecture lets concept owners evolve meaning deliberately while publishers produce reproducible releases and consumers bind safely to the right scheme, value set, language, version, and mapping.

## Why This Matters

The W3C [SKOS Reference](https://www.w3.org/TR/skos-reference/) distinguishes concept identity, notations, preferred, alternative and hidden labels, notes, broader and narrower relations, collections, and mapping relations. The [SKOS Primer](https://www.w3.org/TR/skos-primer/) illustrates how controlled vocabularies can be represented and linked. SKOS is a knowledge-organization model; local applications still define domain policy, constraints, and lifecycle.

OASIS [Code List Representation (Genericode)](https://docs.oasis-open.org/codelist/genericode/v1.0/os/genericode-v1.0-os.html) provides a model and XML representation for code lists. HL7 FHIR's [Terminology Module](https://hl7.org/fhir/terminology-module.html) separates code systems from value sets. FHIR [CodeSystem](https://hl7.org/fhir/R5/codesystem.html) represents code-system metadata and concepts, while [ValueSet `$expand`](https://hl7.org/fhir/valueset-operation-expand.html) makes version- and parameter-aware expansion explicit. These mechanisms demonstrate why a code, its governing system, a permitted subset, and a computed expansion are different artifacts.

[RFC 5646](https://www.rfc-editor.org/rfc/rfc5646) defines language tags used to qualify human-language content. The W3C [Data Quality Vocabulary](https://www.w3.org/TR/vocab-dqv/) provides a framework for quality metadata rather than one universal quality judgment. W3C [PROV-O](https://www.w3.org/TR/2013/REC-prov-o-20130430/) provides provenance concepts, and NIST [SP 800-160 Volume 1 Revision 1](https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final) frames trustworthy lifecycle engineering. A vocabulary is a governed semantic product, not merely a file.

## Prerequisites and Retrieval

You should understand reference data, identifiers, namespaces, data models, hierarchy management, temporal versions, APIs, events, search, validation, localization, provenance, access control, reliability, recovery, and governance.

Retrieve concept, concept scheme, code system, code list, value set, expansion, namespace, stable identifier, notation, preferred label, alternative label, hidden label, language tag, definition, scope note, editorial note, collection, broader, narrower, related, exact match, close match, broad match, narrow match, deprecation, replacement, mapping, profile, extension, binding, release, and retirement.

As a retrieval test, inspect “standardize the status codes.” Ask which domain and decisions, whether codes represent one scheme or several, concept identity, definitions, languages, effective time, hierarchy, permitted subsets, mappings, external authority, extensions, consumer bindings, compatibility, unknown behavior, release process, protection, and historical interpretation apply. A shared enum without those answers is only shared syntax.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish reference data, code list, code system, concept scheme, taxonomy, thesaurus, controlled vocabulary, value set, expansion, and ontology;
2. separate concept identity from code notation, labels, definitions, notes, relationships, and presentation;
3. define multilingual label and search policies using qualified language, script, audience, and status;
4. model direct semantic relations, hierarchy, collections, mappings, and cross-scheme equivalence without overstating entailment;
5. design immutable releases, value-set definitions, parameterized expansions, consumer bindings, compatibility, and replay;
6. govern proposals, editorial review, deprecation, replacement, merge, split, extension, correction, and retirement;
7. validate structural, lexical, semantic, mapping, temporal, and consumer-specific constraints;
8. publish vocabularies through APIs, files, events, indexes, caches, and packages with service and recovery contracts;
9. protect sensitive classifications, licensed content, mappings, search evidence, and administrative functions; and
10. assign ownership, measure semantic outcomes, migrate consumers, and verify closure.

## Core Exposition

**Start with interpretation and decisions.** Identify fields, messages, searches, reports, rules, and decisions whose meaning depends on the vocabulary.

The need is not “one list.” It is consistent enough interpretation for a declared population and purpose, with safe evolution.

**Define the semantic boundary.** State domain, included and excluded concepts, intended granularity, jurisdictions, time, audiences, consumers, and prohibited uses.

A “status” scheme can mix workflow state, legal state, availability, and data-quality state unless the boundary is explicit.

**Distinguish controlled vocabulary from reference data.** Reference data emphasizes governed values used across systems. A controlled vocabulary adds explicit concept identity, lexical forms, definitions, notes, and semantic relations.

Many artifacts are both. The distinction guides which semantic mechanisms and editorial roles are required.

**Distinguish taxonomy and thesaurus.** A taxonomy often emphasizes hierarchical classification. A thesaurus also supports synonyms, related concepts, scope notes, and richer navigation.

Neither term alone specifies machine constraints, versioning, or consumer binding. Publish the actual model and policies.

**Distinguish ontology.** An ontology can express formal classes, properties, axioms, and entailments about a domain. A vocabulary can organize terms without claiming those formal semantics.

Do not call a broader category an `is-a` relationship unless that interpretation is intended and validated.

**Give the scheme stable identity.** Use a durable URI or namespace and record title, purpose, publisher, owner, version policy, license, languages, and lifecycle.

Do not use a file path or current host name accidentally as permanent identity. Define resolution and succession.

**Give concepts stable identity.** A concept ID should persist while preferred label, notation, definition wording, placement, and display order change without altering underlying meaning.

If meaning changes materially, create a new concept or explicit versioned semantic change instead of hiding it behind the old ID.

**Separate notation from identity.** Codes support exchange with systems that need compact strings. Qualify notation by scheme, version, case sensitivity, and normalization.

One concept may have legacy and current notations; the same notation may appear in unrelated schemes. Never join by code alone.

**Define code uniqueness.** State whether comparison is case-sensitive, whitespace-significant, Unicode-normalized, or constrained by syntax.

Apply the same rules to authoring, files, APIs, indexes, validators, and consumers. Silent case folding can merge distinct externally governed codes.

**Do not recycle codes silently.** Historical facts may store only notation and scheme version. Reusing a retired code for new meaning makes them ambiguous.

Prefer permanent retirement. If an external authority reuses a code, preserve version and consider an internal stable concept identifier.

**Separate labels from definitions.** A label names a concept for people; a definition states meaning, boundaries, and relevant conditions.

“Closed” can mean no longer trading, no longer editable, or temporarily unavailable. Shared labels without definitions can increase false confidence.

**Use preferred labels deliberately.** Define whether one preferred label is allowed per concept, language tag, script, audience, or application context.

If two English renderings are both needed, qualify contexts or choose one preferred and one alternative. Do not silently duplicate primary labels.

**Use alternative labels for legitimate variants.** Synonyms, abbreviations, former names, domain variants, and common phrases can improve discovery.

Record language, context, status, and provenance. An alternative label should not imply exact semantic equivalence outside the concept.

**Use hidden labels cautiously.** Misspellings, deprecated forms, and search-only strings can support retrieval without being displayed as recommended terminology.

They can also introduce offensive, sensitive, or misleading text into indexes and logs. Govern access and presentation separately.

**Qualify natural language.** Store language tags, scripts where necessary, translation status, translator or source, review, and effective version.

Do not infer language from user location or application locale. Machine translation is a derived assertion requiring review proportional to consequence.

**Preserve source wording.** External concepts can carry authoritative labels and definitions while local renderings, summaries, and annotations remain separate.

Do not edit source meaning silently. Record source edition, retrieval, transformation, and local responsibility.

**Write scope notes.** Clarify when to use a concept, when not to, how it differs from neighbors, and what ambiguous cases require review.

Editorial notes can record drafting rationale without publishing internal discussion to all consumers. Classify notes by audience.

**Model concepts, not just rows.** A concept can have multiple labels, notations, definitions, notes, mappings, hierarchy placements, collections, and lifecycle states.

A flat two-column export can be a distribution view, not the complete authority model.

**Use direct semantic relations.** Assert immediate broader, narrower, and related relationships according to scheme policy.

Keep direct edges separate from transitive closure. Consumers need to know whether a returned relation was asserted or inferred.

**Define hierarchy semantics.** Broader can mean generic class, partitive whole, or instance relationship in different vocabulary traditions.

If those distinctions matter, model relation subtypes. Do not assume every broader path supports the same logical entailment or rollup.

**Permit polyhierarchy where meaning requires it.** A concept may have several broader concepts. Navigation can follow several valid paths.

Validate cycles and disallowed relation combinations. Define how search expansion, display, and reporting handle multiple paths.

**Use associative relations separately.** `related` connects concepts without claiming parentage or equivalence.

Overusing it creates an unhelpful dense graph. Require editorial reason and intended consumer behavior where scale matters.

**Use collections for presentation or grouping.** A curated or ordered collection can group concepts without asserting a semantic parent.

Do not turn menu structure into taxonomy or infer membership transitivity unless the model declares it.

**Distinguish code system from value set.** A code system defines codes and their meanings. A value set selects codes permitted for a use.

Several fields can bind different value sets from one system. One value set can draw from multiple systems with pinned versions.

**Make value-set rules explicit.** Include or exclude enumerated concepts, descendants, property filters, imported sets, status, jurisdiction, and effective time.

Record the rule language and semantics. A dynamic definition can yield different members when underlying systems change.

**Treat expansion as a result artifact.** An expansion records the materialized member set, parameters, underlying versions, generation time, server or process, and digest.

Do not mutate a persisted expansion. Generate a new identified artifact when inputs or parameters change.

**Pin expansion parameters.** Language, active-only filter, hierarchy behavior, pagination, system versions, display inclusion, and local extensions can change output.

Consumers need enough metadata to reproduce membership. “Expanded today” is insufficient.

**Separate membership from fitness.** Validation can show that a code belongs to a bound value set under a version. It does not prove the code correctly describes a real case.

Domain validation still evaluates evidence, effective time, actor authority, and business rules.

**Treat mappings as assertions.** A mapping states source and target scheme, versions, concept IDs, relation, direction, context, provenance, status, and effective interval.

Do not store one target code column and call every row equivalent. Mapping meaning is part of the data.

**Distinguish exact and close mappings.** Exact mapping asserts interchangeability strong enough for the declared scope; close mapping indicates similarity that may not support substitution.

Review definitions and use cases, not labels alone. Similar words often conceal different boundaries.

**Distinguish broader and narrower mappings.** A detailed source concept can map to a broader target category for reporting while losing information.

The inverse cannot reconstruct the detail. Preserve mapping direction and avoid mechanical inversion.

**Model mapping cardinality.** One-to-one can still be inexact. Many-to-one aggregates distinctions. One-to-many requires context or unresolved choice. Many-to-many often needs a transformation rule.

Expose information loss and required attributes. Never force an arbitrary single target for interface convenience.

**Version both mapping endpoints.** A mapping between source release 3 and target release 8 can become invalid if either definition changes.

Bind exact releases or supported ranges and retest at publication. “Current to current” cannot reproduce old decisions.

**Control local extensions.** When upstream schemes lack needed concepts, issue local identities in a distinct namespace with definition, owner, mapping status, and lifecycle.

Do not forge upstream-looking codes. Plan collision and migration if the authority later introduces an equivalent concept.

**Govern profiles and subsets.** A local profile can restrict labels, properties, relations, or allowed concepts while citing the upstream scheme and version.

Publishing a subset creates consumer commitments. Give it ownership, release, compatibility, quality, and retirement policy.

**Define editorial workflow.** Proposals include need, concept boundary, definition, labels, relations, examples, effective time, source, consumers, and compatibility impact.

Reviewers need domain expertise, terminology skill, language coverage, legal or policy input, and separation of duties proportional to consequence.

**Use candidate status.** Draft or candidate concepts can be tested without becoming valid codes for production facts.

Control visibility and prevent applications from binding to unapproved IDs. Promotion creates an immutable release decision.

**Classify changes semantically.** New concept, label correction, translation addition, definition clarification, meaning change, hierarchy move, mapping change, deprecation, merge, split, and deletion affect consumers differently.

Text size does not determine compatibility. A small definition change can alter decisions widely.

**Deprecate rather than erase.** Deprecated concepts remain interpretable for historical facts but should not be selected for new data after a boundary.

Publish reason, date, replacement relation if any, migration guidance, support window, and exceptions.

**Handle concept replacement carefully.** A corrected notation can alias one concept. A meaning split often requires several narrower successors and additional evidence.

Return unresolved when old facts lack that evidence. Do not choose the most popular successor and call it migration.

**Treat merge as semantic change.** Combining concepts can erase distinctions. Preserve old IDs, mappings, effective intervals, source facts, and rationale.

Decide whether historical facts remain on old concepts or are restated. Label both policies explicitly.

**Preserve editorial provenance.** Record author, reviewers, sources, evidence, transformations, approvals, release, and supersession for concepts and mappings.

Provenance supports correction and trust but does not prove that a definition is objectively right.

**Publish immutable releases.** Bind scheme metadata, concepts, notations, labels, definitions, relations, mappings, value-set definitions, validation, manifest, and source editions.

Use stable release identity plus content digests. A digest proves content equality, not semantic compatibility.

**Publish machine and human change records.** Machine-readable diffs identify affected IDs and relation types. Human notes explain meaning, consequence, migration, and limitations.

Neither alone is enough. Consumers need automation and judgment.

**Define compatibility dimensions.** Syntax covers code forms and schemas; population covers allowed members; semantics covers meaning; lexical compatibility covers labels and search; operational compatibility covers size and service.

Adding a code can break exhaustive switches. Correcting a label can alter reports or search. Schema-compatible does not mean decision-compatible.

**Register consumer bindings.** Record consumer, field, purpose, code system, value set, version or channel, expansion parameters, language, fallback, activation, and owner.

Compare declarations with API requests, files, packages, database queries, validation rules, models, and runtime observations.

**Support pinned and moving bindings.** Pinned releases enable reproduction. Moving channels can deliver timely corrections.

Even a moving consumer records the exact release resolved for each decision or deployment. Define support window and upgrade duty.

**Publish APIs deliberately.** Support scheme and release resolution, concept lookup, code validation, labels by language, search, relations, mappings, value-set expansion, and history.

Return system, version, code, concept ID, result type, and relevant parameters. Avoid a bare Boolean membership response without context.

**Bound search semantics.** Define tokenization, normalization, stemming, language, preferred and alternative labels, hidden-label behavior, ranking, fuzzy matching, and limits.

Search result relevance is not exact semantic match. Expose concept identity and definition before selection.

**Publish files as verifiable artifacts.** Include schemas, full snapshots, optional deltas, manifests, digests, record counts, languages, source and license metadata, and release notes.

Consumers install atomically and reject mixed releases. Flat exports state which semantic details they omit.

**Use events as notifications and changes.** Concept, label, definition, relation, mapping, value set, expansion, release, and retirement events have different consequences.

Define ordering, idempotency, replay, retention, correction, compaction, and snapshot recovery. Events do not replace complete state.

**Manage caches by full key.** Include scheme, version or channel, value set, expansion parameters, language, context, and effective time.

An expansion cached without underlying versions can silently change meaning. Versioned immutable artifacts simplify safe caching.

**Manage embedded vocabularies.** Generated enums and application packages give low-latency validation but update only when software deploys.

Inventory package-to-release binding, unknown-code behavior, maximum staleness, emergency correction, and end of support.

**Design unknown behavior first.** Consumers will encounter new, deprecated, unauthorized, malformed, unmapped, and unavailable codes.

Define reject, preserve, quarantine, warn, or degrade by decision. Never map unknown automatically to `OTHER` unless that category truly applies.

**Validate structurally.** Check identifiers, notation uniqueness, case rules, language tags, preferred-label cardinality, required definitions, reference integrity, interval shape, manifests, and schemas.

Structural validity is necessary but not sufficient for meaningful concepts.

**Validate semantic consistency.** Review concept overlap, gaps, circular definitions, hierarchy cycles, incompatible relation types, mapping claims, replacements, and value-set purpose.

Use domain examples and adversarial cases. Automated checks can surface candidates but accountable experts decide meaning.

**Validate consumer impact.** Test exhaustive switches, database constraints, user interfaces, search, reports, rules, mappings, models, packages, caches, payload size, latency, history, and rollback.

Prioritize by consequence and actual bindings. A low-use code can still drive a critical annual process.

**Measure vocabulary quality in context.** Track unresolved classification, overlap disputes, missing concepts, synonym retrieval, mapping coverage, stale consumers, correction time, and decision outcomes.

Concept count, label count, or search clicks are activity signals. Quality is fitness for named uses, not maximal size.

**Protect sensitive semantics.** Internal risk levels, investigations, unreleased products, export classifications, and mappings can reveal protected information.

Control read, search, traversal, administration, exports, logs, histories, and backups. Public labels do not make usage evidence public.

**Respect license and attribution.** Record external terms, permitted transformation, redistribution, attribution, access, update obligations, and derived-product conditions.

Validate that APIs, files, caches, packages, backups, and consumer exports comply before publication.

**Engineer service objectives.** Define availability, validation latency, expansion time, search latency, release frequency, freshness, propagation, retention, and correction.

Observe by scheme, version, value set, parameter, language, result state, consumer, and region. Healthy API uptime can hide stale terminology.

**Control expensive expansions and traversals.** Recursive imports, broad descendant rules, large mappings, and unbounded search can exhaust service resources.

Set depth, size, time, and recursion limits; detect cycles; cache by full key; apply backpressure; and return typed incomplete or failed results.

**Design degraded behavior.** Some consumers can use a pinned verified expansion during outage; others must stop when a safety-critical set expires.

State maximum age, allowed operations, warning, reconciliation, and recovery. Do not use an arbitrary latest cache.

**Recover the semantic system.** Restore schemes, concept identities, histories, labels, definitions, relations, mappings, value sets, expansions, sources, workflows, approvals, permissions, and consumer bindings.

Rebuild search and closure indexes from authoritative releases, verify digests and representative queries, then reconcile consumers.

**Assign ownership.** Domain owners decide meaning; vocabulary stewards manage editorial workflow; language reviewers own qualified renderings; mapping owners own cross-scheme claims.

Platform, source, consumer, protection, legal, reliability, incident, records, and retirement owners retain their decisions.

**Plan migration.** Compare identities, codes, definitions, labels, relations, mappings, value-set membership, expansions, bindings, APIs, files, and embedded packages.

Use shadow releases, consumer tests, cohorts, compatibility windows, and explicit end dates. Preserve old versions for required historical interpretation.

**Retire with evidence.** Inventory schemes, concepts, codes, mappings, value sets, expansions, channels, caches, packages, validators, rules, reports, models, consumers, credentials, and histories.

Stop authoring and publication only after consumers migrate, retained releases have custody, access is revoked, prohibited copies are deleted, and restore cannot resurrect unsupported semantics.

## Definitions and Notation

Let concept version $c=(S,id,N,L,D,R,t_e,t_o,s,P)$ contain scheme $S$, stable concept identity $id$, notations $N$, qualified labels $L$, definitions and notes $D$, semantic relations $R$, effective interval $t_e$, transaction interval $t_o$, lifecycle status $s$, and provenance $P$.

Let code identity be $(S,v,n)$ for scheme, version, and notation under declared case and normalization rules. An unqualified notation $n$ is not a stable semantic key.

Let value-set definition $Q=(id,v,I,E,F,P)$ bind identity, version, inclusions $I$, exclusions $E$, filters or imports $F$, and purpose $P$. Expansion is:

$$
X=Expand(Q,\{S_i,v_i\},parameters,t),
$$

and records every underlying code-system version and parameter that affects membership or display.

Let mapping $m=(S_a,v_a,id_a,S_b,v_b,id_b,r,d,C,P)$ contain endpoint schemes, versions, concepts, relation $r$, direction $d$, context $C$, and provenance $P$.

Define `FitVocabulary(V,u,t)` as a review predicate requiring justified purpose, stable semantic identity, qualified lexical and relational meaning, reproducible versions and subsets, honest mappings, safe publication, protected and recoverable operation, accountable outcomes, and lifecycle closure for use $u$ at time $t$.

## Mechanisms, Invariants, or Proof Structure

Use ten architecture gates.

**1. Outcome gate.** Name vocabulary-dependent fields, searches, decisions, consumers, harms, fallback, value, and assurance depth.

**2. Scheme gate.** Define domain, purpose, stable namespace, concept identity, notations, authority, languages, license, scope, and exclusions.

**3. Lexical gate.** Govern preferred, alternative, and hidden labels; language and script; definitions; notes; source wording; search; and presentation.

**4. Relation gate.** Define direct hierarchy, transitive inference, associative links, collections, relation subtypes, polyhierarchy, cycles, and consumer behavior.

**5. Subset gate.** Separate code systems, value-set definitions, profiles, imports, filters, expansions, parameters, underlying versions, and membership fitness.

**6. Mapping gate.** State endpoint versions, relation, direction, cardinality, context, provenance, information loss, unresolved cases, and validation.

**7. Lifecycle gate.** Control proposals, candidate status, semantic change classes, deprecation, replacement, merge, split, extension, correction, releases, and history.

**8. Contract gate.** Publish APIs, search, files, events, caches, packages, bindings, compatibility, unknown behavior, correction, and consumer activation.

**9. Protection and service gate.** Bound sensitive semantics, licensing, access, logs, availability, expansion and search resources, degraded behavior, incidents, and recovery.

**10. Ownership gate.** Assign semantic, editorial, language, mapping, platform, consumer, protection, legal, records, incident, migration, and retirement decisions.

Passing these gates supports a scoped semantic product. It does not prove that every definition is complete, every mapping is exact, every expansion is suitable, or every consumer interprets a code correctly.

### Executable evidence

The executable example validates preferred-label cardinality and preserves unresolved migration after one deprecated concept splits into two narrower successors.

<!-- bijux-verify: {"id":"controlled-vocabulary-split-contract","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"active_concepts=3\npreferred_labels_en=3\nduplicate_preferred_labels=0\ndeprecated_code=MEDIUM\nreplacement_relation=narrower-choice-required\nmigration_state=unresolved\nscheme_version=2026-09\n","stderr":""}} -->
```python
concepts = [
    {"id": "risk-low", "code": "LOW", "status": "active", "pref": {"en": "Low"}},
    {"id": "risk-medium-low", "code": "MEDIUM_LOW", "status": "active", "pref": {"en": "Medium low"}},
    {"id": "risk-medium-high", "code": "MEDIUM_HIGH", "status": "active", "pref": {"en": "Medium high"}},
]
deprecated = {
    "code": "MEDIUM",
    "successors": ["risk-medium-low", "risk-medium-high"],
}

english_labels = [concept["pref"]["en"] for concept in concepts]
duplicates = len(english_labels) - len(set(english_labels))
relation = "narrower-choice-required" if len(deprecated["successors"]) > 1 else "replacement"

print(f"active_concepts={len(concepts)}")
print(f"preferred_labels_en={len(english_labels)}")
print(f"duplicate_preferred_labels={duplicates}")
print(f"deprecated_code={deprecated['code']}")
print(f"replacement_relation={relation}")
print("migration_state=unresolved")
print("scheme_version=2026-09")
```

The result proves only list cardinality, string uniqueness, and branching on two successor IDs for one in-memory scheme. It does not prove definitions, label quality, language coverage, semantic relations, mapping fitness, migration evidence, authority, compatibility, production publication, protection, recovery, or consumer interpretation.

## Alternatives and Trade-Offs

**Flat code list.** Exchange and validation are simple, but definitions, multilingual labels, relations, mappings, and editorial evidence may be inadequate.

**Controlled concept scheme.** Meaning and navigation become richer; governance, tooling, versioning, and consumer learning costs increase.

**Formal ontology.** Machine reasoning can express stronger semantics; modeling complexity, inference surprises, performance, and expertise demands rise.

**External authoritative scheme.** Interoperability and shared maintenance improve; local fitness, licensing, cadence, extensions, and outage remain enterprise concerns.

**Local scheme.** Domain fit and change control improve; cross-enterprise mapping, duplication, and external exchange burden grow.

**Pinned code-system version.** Reproduction improves while updates and urgent corrections require migration.

**Moving supported channel.** Timely changes reach consumers, but each resolved decision must record the actual version.

**Dynamic value-set definition.** Compact reusable rules adapt to underlying systems; membership can drift unless endpoint versions are pinned.

**Persisted expansion.** Membership is reproducible and fast; storage, cache, and regeneration responsibilities increase.

**Exact mappings only.** Semantic claims remain conservative while cross-scheme coverage may be low.

**Contextual broader or close mappings.** Utility improves if consumers understand loss and ambiguity; misuse as equality becomes a risk.

**Runtime terminology service.** Central validation, search, and expansion stay current; latency, availability, capacity, and outage policy become dependencies.

**Embedded generated package.** Local speed and build determinism improve; release lag, language parity, dependency inventory, and emergency correction become harder.

Choose by semantics, authority, interoperability, change rate, consumer need, historical interpretation, language, mapping ambiguity, protection, license, reliability, cost, and exit.

## Failure Modes and Misconceptions

1. **A controlled vocabulary is just a two-column table.** Concepts, labels, definitions, relations, versions, mappings, consumers, and governance matter.
2. **Code strings are globally meaningful.** Scheme, version, case, and context qualify notation.
3. **A preferred label is concept identity.** Labels are mutable human renderings.
4. **One preferred label works for every audience.** Language, script, jurisdiction, discipline, and context can differ.
5. **Synonyms prove equivalence.** Lexical similarity does not establish matching boundaries.
6. **Broader always means subclass.** Generic, partitive, instance, and navigation relations can differ.
7. **A value set defines code meanings.** It selects permitted concepts from code systems.
8. **An expansion can be updated in place.** It is a result under pinned inputs and parameters.
9. **Membership validation proves correct classification.** It proves only permitted membership under a binding.
10. **Mappings are reversible.** Direction, cardinality, and information loss often prevent inversion.
11. **Exact-looking labels justify exact mapping.** Definitions and use context determine relation.
12. **Every deprecated code has one replacement.** Splits, merges, and scope changes can require context or unresolved state.
13. **Adding a value is always compatible.** Exhaustive consumers, reports, and rules can fail.
14. **Unknown is other.** Unrecognized, unmapped, withheld, and known-outside-list are distinct.
15. **Search result means semantic match.** Search ranking only retrieves candidates.
16. **Generated enums solve versioning.** Embedded packages can become stale and reject new codes.
17. **Service uptime means terminology is current.** Underlying systems, expansions, and caches can be stale.
18. **Turning off authoring retires the vocabulary.** Bindings, packages, mappings, validators, history, and obligations remain.

## Worked Examples

### Example 1

Code `A` means active in one scheme and adult in another. Events carry system, version, and code, preventing a false join. **Conclusion:** notation requires namespace and version.

### Example 2

Concept `risk-high` keeps its identity while its English preferred label changes from “Elevated” to “High” and the old text becomes an alternative label. **Conclusion:** lexical change need not change meaning.

### Example 3

A French translation is pending expert review. The API returns the verified English label with translation status instead of presenting machine output as authoritative French. **Conclusion:** multilingual labels require qualified provenance.

### Example 4

A product concept has two broader categories for material and use. Search follows both, while reporting binds a separate exclusive value set. **Conclusion:** relation behavior depends on consumer purpose.

### Example 5

A clinical field binds a value set that includes active descendants from two pinned code-system releases. Its expansion records filters, versions, language, and digest. **Conclusion:** definition and expansion are distinct artifacts.

### Example 6

An old detailed code maps to a broader reporting category. The reverse map returns several candidates and requires source detail. **Conclusion:** broader mappings are directional and lossy.

### Example 7

Deprecated `MEDIUM` splits into two concepts. Historical records remain `MEDIUM`; forward migration returns unresolved without the missing risk measure. **Conclusion:** migration must not invent distinctions.

### Example 8

A generated application enum cannot parse a newly added code. Contract tests and a bounded unknown state prevent the consumer from silently mapping it to `OTHER`. **Conclusion:** population compatibility differs from schema compatibility.

### Example 9

An internal investigation vocabulary is read-restricted, but search logs still reveal queried subjects and rare categories. Logs receive the same purpose and retention controls. **Conclusion:** usage evidence can be sensitive.

### Example 10

An old terminology API has no traffic, yet annual reports, validation rules, local mappings, container packages, and retained expansions depend on it. **Conclusion:** retirement requires binding and artifact closure.

## Cross-Program Connections

- **Data engineering:** source ingestion, concept and relation versions, mapping pipelines, expansion builds, snapshots, events, reconciliation, replay, and deletion implement semantic products.
- **Platform engineering:** catalogs, terminology services, search, workflow, artifact storage, APIs, caches, policy, observability, recovery, and paved upgrades support publishers and consumers.
- **API and service engineering:** qualified codes, version negotiation, value-set validation, expansion, search, localization, caching, typed errors, and deprecation shape contracts.
- **Software engineering:** generated types, exhaustive branches, tolerant readers, package dependencies, contract tests, feature rollout, and unknown handling determine adoption safety.
- **Security and privacy:** internal classifications, licensed terms, mapping disclosure, search and usage evidence, administration, access, audit, retention, and deletion constrain service.
- **Analytics and machine learning:** labels, taxonomies, training targets, features, cohorts, hierarchical metrics, drift, and reproducibility depend on pinned semantics.
- **Organizational design:** semantic authority, editorial stewardship, language and mapping review, consumer responsibility, escalation, and funding determine real governance.
- **Reliability engineering:** expansion load, recursive imports, caches, release propagation, stale packages, degraded modes, recovery, and correction define service risk.
- **Economics and decision science:** misclassification loss, mapping information loss, editorial and translation cost, upgrade burden, interoperability value, and exit cost guide investment.
- **Systems engineering:** stakeholder outcomes, interfaces, configuration control, evidence, hazards, lifecycle, and verification frame semantic assurance.

## References

1. W3C, *SKOS Simple Knowledge Organization System Reference*. <https://www.w3.org/TR/skos-reference/>
2. W3C, *SKOS Simple Knowledge Organization System Primer*. <https://www.w3.org/TR/skos-primer/>
3. OASIS, *Code List Representation (Genericode) Version 1.0*. <https://docs.oasis-open.org/codelist/genericode/v1.0/os/genericode-v1.0-os.html>
4. HL7, *FHIR Terminology Module*. <https://hl7.org/fhir/terminology-module.html>
5. HL7, *FHIR CodeSystem*. <https://hl7.org/fhir/R5/codesystem.html>
6. HL7, *FHIR ValueSet `$expand`*. <https://hl7.org/fhir/valueset-operation-expand.html>
7. IETF, *RFC 5646: Tags for Identifying Languages*. <https://www.rfc-editor.org/rfc/rfc5646>
8. W3C, *Data on the Web Best Practices: Data Quality Vocabulary*. <https://www.w3.org/TR/vocab-dqv/>
9. W3C, *PROV-O: The PROV Ontology*. <https://www.w3.org/TR/2013/REC-prov-o-20130430/>
10. NIST, *SP 800-160 Volume 1 Revision 1: Engineering Trustworthy Secure Systems*. <https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final>

## Exercises

### Exercise 1

Design a shared controlled vocabulary for risk, product classification, workflow status, or another domain. Define scheme, concepts, codes, labels, definitions, relations, subsets, mappings, releases, publication, protection, ownership, and lifecycle.

### Exercise 2

An external code system changes labels, deprecates three concepts, splits one concept, and adds twelve codes. Design enterprise adoption and consumer migration.

### Exercise 3

Create a value set that draws from two code systems and varies by jurisdiction and effective date. Define reproducible expansion, validation, and failure behavior.

### Exercise 4

Two schemes require one-to-one, many-to-one, one-to-many, and unmapped correspondences. Design honest mapping artifacts and consumer contracts.

### Exercise 5

An organization plans to retire its terminology service after moving vocabularies to domain products. Define evidence that semantics, consumers, history, protection, and correction obligations moved or ended.

## Answers to the Exercises

### Answer 1

Name the fields, searches, decisions, consumers, consequences, and excluded uses. Give the scheme and every concept stable identities separate from code and label. Define notation syntax, case and normalization, non-reuse, preferred-label cardinality, language and script, alternative and hidden labels, definitions, scope notes, examples, direct relations, collections, status, effective and transaction time, and provenance. State whether hierarchy is polyhierarchical and what consumers infer.

Define value sets and profiles separately from the code system, pin expansion inputs and parameters, and model mappings with endpoint versions, relation, direction, cardinality, context, and limitations. Govern proposals, candidate status, review, deprecation, split, merge, extension, correction, release, and retirement. Publish immutable APIs, files, events, indexes, and packages with manifests, compatibility, unknown handling, freshness, recovery, and consumer bindings. Protect sensitive terms and usage evidence, respect licenses, assign semantic and operational owners, measure decision outcomes, and verify migration and closure.

### Answer 2

Retrieve and verify the upstream edition, provenance, license, and complete diff against the prior pinned source. Classify changes semantically. Label changes can affect interfaces and search but should not alter concept identity. Deprecations need support dates and mapping relations. The split cannot be migrated without distinguishing evidence. New codes can break exhaustive consumers even when payload schema is unchanged. Identify value sets, mappings, validators, reports, rules, models, interfaces, caches, files, and generated packages through declared bindings and observed dependencies.

Create an immutable enterprise candidate release retaining source identity and local annotations separately. Validate notations, labels, definitions, relations, mappings, value-set expansions, language coverage, and manifests. Publish machine and human change notes. Test consumers, search, unknown behavior, historical facts, performance, rollback, and recovery. Activate by cohort under a bounded compatibility window. Preserve old codes for history; return unresolved for split migration without evidence. Track actual release activation and close only after critical consumers reconcile and exceptions have owners and deadlines.

### Answer 3

Give the value-set definition stable identity and version. State purpose, bound field, jurisdictions, effective intervals, inclusions, exclusions, filters, imported sets, hierarchy behavior, and allowed status. Bind exact code-system versions or a governed supported range. Treat jurisdiction and date as explicit parameters, not ambient server configuration. An expansion records definition version, underlying systems, parameters, generation process and time, language, members, status, and content digest.

Validate code membership against the exact expansion used, returning system, version, code, result, and reason. Membership does not establish correct real-world classification. Cache by the full expansion key and publish immutable artifacts for offline users. Define maximum age, missing upstream behavior, recursive-import and size limits, and whether a critical consumer fails closed or uses a pinned verified expansion. Retain historical expansions for replay, publish corrections as new versions, and reconcile runtime service, files, packages, and consumers after recovery.

### Answer 4

Bind mappings to exact source and target scheme releases and a declared direction and use. Each assertion contains source and target concept IDs, relation, cardinality, context, evidence, author or rule, review, status, effective interval, and provenance. Use exact only when definitions and boundaries support substitution. Many source concepts mapping to one target are broader aggregation and lose detail. One source mapping to several targets requires additional context; without it return ambiguous or unresolved. No defensible target is `no-match` or `unmapped`, not `OTHER`.

Publish machine mappings and human limitations, coverage weighted by consequence, and representative tests. Do not derive reverse mappings by swapping columns; validate the reverse use independently. Consumers declare whether they accept exact, close, broader, or contextual relations and how they handle sets and unresolved results. Version the mapping whenever either endpoint or mapping judgment changes. Preserve mapping generation used for each converted fact and reconcile changed conversions before consumer activation.

### Answer 5

Inventory every scheme, namespace, concept, notation, label, definition, relation, mapping, value-set definition, expansion, profile, extension, proposal, approval, release, API, file, event, search index, cache, generated package, validator, rule, report, model, consumer binding, credential, license, history, backup, retention rule, deletion path, and incident duty. For each semantic and operational decision, name the receiving domain product and owner or prove it is no longer required.

Run old and new services in bounded comparison across identities, codes, labels, definitions, relations, mappings, expansions, search, validation, languages, history, latency, and correction. Migrate consumers by cohort, including annual, offline, manual, and disaster-recovery users. Freeze and transfer authoring at explicit releases, drain events, preserve required versions under named custody, revoke access, remove prohibited copies, and test recovery without the old service. Verify that old packages, caches, jobs, or backups cannot resurrect unsupported terminology before accountable closure.
