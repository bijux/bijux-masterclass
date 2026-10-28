---
module_id: DARCH-065
program: Data Architecture Engineering
level: 2
module_number: 65
title: Ontologies and Knowledge Graphs
status: complete
last_verified: 2026-09-03
---

# Ontologies and Knowledge Graphs

## One-Page Review

### Governing question

How should an enterprise identify concepts and things, formalize selected semantics, integrate attributable assertions, reason under declared regimes, validate operational expectations, serve bounded queries, and evolve a knowledge graph without confusing a useful model with complete or unquestionable knowledge?

### Essential definitions

- An **ontology** is an explicit, governed specification of concepts, relations, axioms, and intended interpretations for a bounded domain or purpose.
- A **knowledge graph** is an operated graph-shaped information product that connects identified things, concepts, assertions, sources, and context for defined decisions and queries.
- An **RDF graph** is a set of subject-predicate-object triples whose subjects are IRIs or blank nodes, predicates are IRIs, and objects are IRIs, blank nodes, or literals.
- An **RDF dataset** contains one default graph and zero or more named graphs, allowing multiple graphs to be handled while keeping selected boundaries.
- An **IRI** is a global identifier in RDF syntax; governance determines its intended referent, persistence, resolution, and lifecycle.
- A **blank node** denotes an existentially described resource without globally naming it; a serialization label for a blank node is not a durable identifier.
- A **class** denotes a category of resources; an **individual** is a resource considered as an instance; a **property** denotes a relation.
- An **axiom** is a formal statement interpreted under a declared semantics, such as a subclass, equivalence, disjointness, domain, range, or property-characteristic statement.
- **Entailment** is the relation by which a graph or ontology logically implies another statement under a named entailment regime.
- The **open-world assumption** means failure to establish a statement does not normally establish its negation.
- The **non-unique-name assumption** means distinct identifiers are not automatically interpreted as distinct things unless semantics or policy establishes that difference.
- A **shape** describes structural expectations and validation targets for a data graph; shape conformance is not identical to ontology consistency or real-world truth.
- A **competency question** is a representative question the model and system are expected to answer under stated data, inference, time, and access conditions.
- **Ontology alignment** records qualified correspondences between terms in different models; it does not require merging their authorities or asserting universal equivalence.

### Central model, mechanism, or theorem

Represent an enterprise knowledge-graph capability as:

`K = (I, O, D, A, P, R, V, Q, S, G, C)`

where `I` is identity and reference, `O` ontologies and profiles, `D` attributable data graphs, `A` acquisition and alignment, `P` provenance and policy, `R` reasoning regimes, `V` validation and assurance, `Q` queries and interfaces, `S` storage and operations, `G` governance and protection, and `C` change and closure. Fitness is relative to named competency questions, source authority, graph scope, ontology version, entailment regime, validation profile, time, confidence, and access view. An entailed statement follows from accepted premises under declared semantics; it is not thereby observed, source-authoritative, current, ethically legitimate, or operationally safe.

### Critical invariants

- Every governed IRI has an owner, intended referent or use, persistence rule, resolution behavior, collision policy, and retirement path.
- Prefixes and compact terms are serialization conveniences; expanded IRIs, not local abbreviations or labels, determine RDF identity.
- Ontology axioms, source assertions, inferred statements, mappings, shapes, policy decisions, and user annotations remain distinguishable and attributable.
- Class membership, subclass, part-of, broader concept, instance, role, and implementation type are not collapsed into one hierarchy.
- Domain and range axioms have entailment consequences under RDFS-style semantics; they are not merely input-validation declarations.
- Open-world reasoning does not interpret missing properties as false, invalid, zero, empty, or nonexistent.
- Distinct IRIs do not prove distinct referents, and matching labels do not prove identical referents.
- The chosen reasoning profile is explicit, tested for consistency and performance, and bounded to semantics consumers understand.
- Validation reports name the shapes graph, data graph, inference preparation, focus nodes, severity policy, and version used.
- Queries declare dataset, named-graph scope, entailment regime, time or snapshot, access view, limits, and completeness assumptions.
- Sensitive facts can be inferred from nonsensitive-looking paths; authorization applies to queries, results, graph structure, exports, and inference.
- Retirement preserves identifiers, ontology versions, mappings, provenance, decisions, and required historical interpretations while ending active unsupported use.

### Common failures

Common failures include treating a property graph product as an ontology; minting IRIs from mutable labels; using blank-node labels as cross-file keys; assuming different IRIs mean different things; using `rdfs:domain` as a UI field restriction; modeling part-of as subclass; declaring equivalence to improve search; expecting open-world inference to report missing data; expecting OWL to enforce required fields; mixing inferred triples with source facts without provenance; loading every vocabulary into one reasoning regime; joining graphs on strings; exposing SPARQL without cost or authorization controls; counting triples as value; and deleting deprecated vocabularies so historical assertions become uninterpretable.

### Compact example

Five asserted triples define two subclass axioms, a property's domain and range, and one relationship. A deliberately small RDFS-style closure derives a transitive subclass, types the relationship subject and object, and propagates those types upward. The executable check produces eleven triples after two inference rounds and finds no violations of two illustrative operational constraints. It does not implement full RDFS, OWL, RDF datatype semantics, inconsistency detection, source authentication, closed-world validation, or real-domain correctness.

### Connections

[DARCH-014](014-entities-relationships-and-business-keys.md), [DARCH-015](015-shared-vocabulary-and-business-glossaries.md), [DARCH-020](020-reconciling-conflicting-models-across-systems.md), [DARCH-057](057-shared-code-sets-and-controlled-vocabularies.md), [DARCH-061](061-metadata-architecture.md), [DARCH-063](063-business-glossaries-and-term-governance.md), and [DARCH-064](064-lineage-architecture.md) establish identity, vocabulary, reconciliation, metadata, meaning, and provenance foundations. [DARCH-066](../ROADMAP.md) next develops semantic interoperability.

## Governing Question

Organizations build knowledge graphs to connect fragmented identifiers, vocabulary, documents, operational data, metadata, policies, lineage, people, products, and evidence. The graph can expose relationships hidden by tables and application boundaries. It can also magnify ambiguity: an elegant path may combine incompatible times, sources, meanings, confidence levels, or permissions.

The governing question is how to make graph meaning explicit enough to support defensible inference and interoperability, yet bounded enough to remain understandable, operable, secure, and changeable. The aim is not to encode the whole enterprise or replace every database. It is to create a governed semantic capability for decisions whose value justifies formalization and graph integration.

## Why This Matters

W3C [RDF 1.1 Concepts and Abstract Syntax](https://www.w3.org/TR/rdf11-concepts/) defines RDF graphs as sets of triples using IRIs, blank nodes, and literals, and RDF datasets as a default graph plus named graphs. It distinguishes abstract graph meaning from concrete serializations and notes that RDF's data model is atemporal even though graphs can describe time and sources can expose changing snapshots.

W3C [RDF 1.1 Semantics](https://www.w3.org/TR/rdf11-semantics/) provides model-theoretic semantics and entailment regimes for RDF and RDFS. This gives terms such as entailment, interpretation, consistency, and recognized datatype precise roles. Enterprise rules must name which regime is actually implemented rather than calling any graph traversal “reasoning.”

[RDF Schema 1.1](https://www.w3.org/TR/rdf-schema/) defines vocabulary for classes, properties, subclass, subproperty, domain, range, labels, comments, resources, containers, and related constructs. Domain and range participate in inference: a triple using a property can entail types for its subject or object. They are not equivalent to form-field constraints.

W3C's [OWL 2 overview](https://www.w3.org/TR/owl2-overview/) describes ontologies in terms of classes, properties, individuals, data values, axioms, and multiple syntaxes and semantics. OWL can express richer knowledge than RDF Schema, including equivalence, disjointness, restrictions, and property characteristics, but expressivity changes reasoning cost and modeling risk.

The [OWL 2 Profiles](https://www.w3.org/TR/owl2-profiles/) define restricted language profiles—EL, QL, and RL—selected for different computational properties and application structures. Architecture should choose the least expressive profile that satisfies competency questions and operational constraints rather than assuming maximum expressivity is maturity.

[SPARQL 1.1 Query](https://www.w3.org/TR/sparql11-query/) defines graph-pattern matching, filters, optional patterns, unions, subqueries, aggregates, property paths, and queries over RDF datasets. A standards-conforming language does not remove the need for dataset scoping, authorization, cost controls, pagination, timeouts, query governance, and explanation.

W3C [SHACL](https://www.w3.org/TR/shacl/) defines shapes graphs, data graphs, focus nodes, targets, constraints, validation results, severities, and conformance. SHACL can express operational expectations such as cardinality, datatype, class, and path conditions. Validation remains separate from entailment and from whether the underlying claims are true or legitimate.

W3C [SKOS](https://www.w3.org/TR/skos-reference/) models concept schemes, concepts, preferred, alternative, and hidden labels, documentation, semantic relations, collections, and mappings. It is suitable for many knowledge-organization systems without turning every business term into a logically defined OWL class.

W3C [PROV-O](https://www.w3.org/TR/prov-o/) models entities, activities, agents, derivation, generation, use, attribution, association, delegation, and qualified influence. Knowledge graphs need provenance not only for domain data but also for ontology versions, mappings, extraction activities, inferred views, validation reports, and graph publications.

[JSON-LD 1.1](https://www.w3.org/TR/json-ld11/) defines a JSON-based syntax for RDF and mechanisms such as contexts, expansion, compaction, flattening, framing, node identifiers, types, language, and graph containers. A friendly JSON representation can improve API adoption, but contexts and compact terms must be versioned and protected because they influence expansion into RDF identifiers.

## Prerequisites and Retrieval

You should understand conceptual and logical modeling, identifiers, graphs, sets and relations, schemas, data types, controlled vocabularies, metadata, provenance, APIs, query processing, logic, distributed systems, security, privacy, governance, testing, versioning, and lifecycle engineering.

Retrieve ontology, knowledge graph, vocabulary, taxonomy, thesaurus, schema, class, individual, property, axiom, assertion, triple, quad, subject, predicate, object, IRI, prefix, literal, datatype, language tag, blank node, skolemization, graph, named graph, RDF dataset, interpretation, entailment, consistency, open world, unique name, subclass, subproperty, domain, range, equivalence, disjointness, restriction, profile, reasoner, materialization, query rewriting, shape, focus node, constraint, severity, conformance, competency question, alignment, mapping, provenance, confidence, and closure.

As a retrieval test, inspect “every employee must have exactly one manager.” Ask whether this is a real-world policy, a source-data validation constraint, or a logical axiom; whether contractors and executives are employees; whether manager absence means unknown or invalid; whether multiple asserted managers are inconsistent under the chosen model; which time and organization apply; which source has authority; and what remediation should occur. The same sentence can require SHACL validation, OWL semantics, application logic, or governance—not an interchangeable triple.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish ontologies, vocabularies, taxonomies, thesauri, schemas, knowledge graphs, and ordinary graph databases;
2. model RDF resources, triples, datasets, IRIs, blank nodes, literals, datatypes, languages, and named-graph boundaries;
3. explain entailment, open-world semantics, non-unique names, inconsistency, and the difference between inference and validation;
4. choose RDF Schema, SKOS, OWL constructs and profiles, SHACL, and application rules according to purpose;
5. design stable namespaces, concept identities, ontology modules, alignments, provenance, versions, and deprecation;
6. acquire, resolve, normalize, reconcile, and publish assertions without erasing source authority or uncertainty;
7. design reasoning, materialization, query, API, access, and redaction behavior with explicit guarantees;
8. validate competency questions, logical consistency, graph quality, operational constraints, security, and performance;
9. operate graph ingestion, indexes, reasoners, caches, change propagation, recovery, and cost; and
10. migrate and retire ontology and graph capabilities while preserving historical interpretation.

## Core Exposition

**Begin with competency questions.** Write representative questions and decisions before choosing a graph technology or ontology language.

Examples include which products satisfy a regulated composition rule, which data assets implement a business concept, which suppliers connect to a vulnerable component, and which evidence supports a policy claim. State required sources, time, confidence, latency, explanation, and failure behavior.

**Define the world modeled.** Name domains, jurisdictions, organizations, systems, populations, asset classes, time spans, viewpoints, and exclusions.

An “enterprise knowledge graph” still has a boundary. Claims outside it may be unknown, inaccessible, excluded, or delegated to another authority; they are not false merely because the graph lacks them.

**Separate ontology from graph.** An ontology specifies selected vocabulary and semantics. A knowledge graph operates assertions about particular resources, often using several ontologies plus local profiles, provenance, constraints, indexes, and services.

A labeled property graph can be a useful knowledge graph without OWL semantics. An OWL ontology can exist without a populated operational graph. Architecture names each layer rather than treating “graph” as one product feature.

**Choose the weakest adequate formalism.** A glossary may need definitions and governance. SKOS may support concept schemes and mappings. RDF Schema may support simple class and property inference. OWL profiles may support richer logical conclusions. SHACL may enforce operational structure.

Greater expressivity can reveal useful conclusions and contradictions but raises modeling, explanation, performance, and governance cost. Formalize only distinctions whose consequences and ownership are understood.

**Govern IRIs as durable public contracts.** Define namespace ownership, identifier minting, intended referent, normalization, dereference or resolution, persistence, versioning, redirects, collision detection, aliases, merges, splits, compromise, and retirement.

Avoid embedding mutable labels, organizational structure, storage locations, or sensitive facts in identifiers. A resolvable HTTP IRI can aid documentation but resolution availability is distinct from RDF identity.

**Distinguish identifiers from prefixes and labels.** Prefixes such as `ex:` abbreviate namespace IRIs in a serialization or query. They are not part of the RDF abstract graph and can differ between documents.

Labels are language- and community-dependent display text. Joining by compact term or label can conflate distinct concepts and split identical ones.

**Use blank nodes with bounded intent.** Blank nodes express existence without globally naming a resource and work well for local structures that have no independent identity.

Serialization blank-node labels are local and must not become integration keys. Mint governed IRIs or systematic Skolem IRIs when resources require stable cross-graph reference, update, provenance, or access control.

**Model literals precisely.** Record lexical form, datatype IRI, and language tag where applicable. Distinguish the literal term from its value: different lexical forms can denote the same value under a datatype.

Validate datatype lexical spaces and canonicalization policy at boundaries. Do not silently coerce invalid values into apparently valid facts.

**Treat triples as claims under interpretation.** A triple asserts that a predicate relation holds between resources denoted by its subject and object. Its source, graph, time, confidence, and authority are not inherent in the three terms.

Attach provenance through named-graph profiles, qualified assertion resources, immutable publications, or another explicit pattern. Document the semantics because an RDF graph name does not by itself have one universal interpretation.

**Design named-graph boundaries.** Named graphs can preserve source imports, ontology modules, releases, tenants, security partitions, evidence classes, or snapshots.

Do not assume a named graph automatically means source, ownership, truth, or time. Define default-graph construction, union behavior, graph-name referent, version, access, and lifecycle.

**Separate classes, individuals, and metamodeling.** Ask whether a resource is a category, a particular thing, a role, a state, a record, or a concept used for classification.

OWL 2 supports several modeling styles, but consumers must understand which semantic layer they query. Accidental class-individual punning or mixing schema and instance data can produce surprising results.

**Model subclass carefully.** `A rdfs:subClassOf B` means every instance of A is an instance of B under RDFS semantics. It is not a generic parent-child link.

Organizational containment, product composition, process sequence, topic grouping, SKOS broader concepts, and database inheritance require distinct relations. Misusing subclass contaminates every downstream inference.

**Model subproperty carefully.** A subproperty statement means every pair related by the narrower property is also related by the broader property.

Do not use it solely to group properties in a UI. If the entailment is not defensible for every pair, use an annotation or separate organizing relation.

**Understand domain and range.** Under RDFS semantics, using a property can entail that its subject belongs to the property's domain class and its object belongs to its range class.

Domain and range are therefore modeling assertions, not simply instructions that reject nonconforming inputs. Use shapes or application validation when the aim is to report invalid data rather than infer types.

**Use equivalence sparingly.** Class, property, or individual equivalence has broad logical consequences. Similar labels, overlapping extensions, shared identifiers in one source, and approximate mappings do not justify exact equivalence.

Prefer explicit close, broader, narrower, related, conditional, or transformation mappings with provenance and limitations. One false equivalence can merge large graph regions.

**State disjointness intentionally.** Disjoint classes allow a reasoner to detect inconsistency when one resource belongs to incompatible classes under the model.

Real domains change, source classification can be incomplete, and roles can coexist over time. Confirm scope and temporal assumptions before encoding disjointness as timeless fact.

**Understand open-world reasoning.** If the graph contains no manager for an employee, open-world semantics normally treats the manager as unknown, not absent.

Closed-world business checks require a declared completeness boundary and validation or application policy. Negation-as-failure must not be smuggled into ontology reasoning.

**Understand non-unique names.** Two IRIs can denote the same thing unless the model or application establishes difference. Conversely, one IRI should not be reused for changing referents.

Identity resolution produces evidence and decisions about sameness. Keep candidates, exact identity, aliases, representations, and conflicting source identities distinct.

**Separate assertion from entailment.** Source graphs contain asserted statements. A reasoner derives entailed statements under a regime and ontology version.

Preserve inference provenance: premises or justification, rule or regime, ontology version, reasoner version, materialization time, and retraction behavior. Never let inferred triples masquerade as source testimony.

**Choose an OWL profile by workload.** OWL 2 EL supports large ontologies with many classes and existential restrictions; QL supports query answering through relational-style data access; RL supports rule-oriented reasoning. Full OWL 2 supports greater expressivity with different computational tradeoffs.

Confirm the precise profile and engine behavior from the governing specification and implementation. “Supports OWL” is not a usable service contract.

**Choose a reasoning strategy.** Forward materialization computes consequences during ingestion; backward chaining derives them during queries; query rewriting transforms queries; hybrid systems cache selected conclusions.

Materialization accelerates reads but amplifies storage and retraction cost. Query-time methods preserve flexibility but can increase latency and denial-of-service exposure. Tie strategy to competency questions and change rate.

**Bound inference.** Select ontology modules, graph scopes, rule sets, recursion, path length, result size, timeout, memory, and consistency response.

Do not combine every imported ontology and source into one unrestricted closure. Inconsistent or explosive regions should be isolated, diagnosed, and governed rather than silently ignored.

**Separate validation from reasoning.** A reasoner asks what follows and whether statements can be jointly interpreted. A shape validator checks whether targeted graph nodes satisfy operational constraints.

An OWL minimum-cardinality restriction can assert that a value exists without requiring an explicit triple. A SHACL minimum count can report a missing explicit value under the validation dataset. Choose the behavior the decision needs.

**Design shapes as governed contracts.** Record shapes-graph identity and version, target selection, paths, constraints, severity, messages, inference preparation, exception, remediation owner, and activation.

Validation can be recursive or implementation-sensitive at advanced boundaries. Maintain conformance tests and avoid letting a generic “warning” become an unreviewed policy bypass.

**Use SKOS for knowledge organization.** Model concepts independently of words, group them into schemes, use language-tagged preferred and alternate labels, and distinguish semantic relations from mappings across schemes.

Do not turn every glossary concept into an OWL class. Some concepts organize retrieval or discourse without defining sets of individuals under formal semantics.

**Model n-ary relations explicitly.** RDF predicates are binary, but many enterprise facts involve actor, object, role, jurisdiction, amount, confidence, source, and interval.

Create an identified relation or event resource whose properties carry participants and qualifiers. Define uniqueness and lifecycle; do not hide crucial qualifiers in an unparseable string.

**Model time explicitly.** RDF graphs are atemporal snapshots; domain vocabularies can represent events, intervals, valid time, transaction time, observation time, and version.

Decide whether an assertion resource, named graph, entity version, or temporal index carries time. A current union graph cannot safely answer historical questions without retained versions and query semantics.

**Model provenance of assertions.** Identify source entity, acquisition activity, agent, extraction or mapping version, publication, evidence, confidence, review, derivation, and correction.

Provenance supports assessment; it does not make the assertion true. An authentic source can be outdated, biased, mistaken, or authoritative only for a limited predicate.

**Separate source authority by predicate.** A human-resources system may authoritatively assert employment status, a team directory reporting relationships, and a glossary concept meaning.

Store source-specific graphs and construct decision views through explicit policy. Technical ingestion order must not choose semantic authority.

**Acquire data through governed connectors.** Sources include databases, APIs, files, streams, documents, catalogs, registries, models, and manual workflows.

For each, define identity mapping, predicate ownership, snapshot and incremental boundaries, deletion, schema change, provenance, validation, quarantine, replay, reconciliation, and closure.

**Treat extraction as an assertion process.** Natural-language, image, model, and heuristic extraction produces candidates with model version, prompt or configuration where appropriate, confidence, evidence span, language, and review state.

Do not publish machine-extracted relations as unquestioned facts. Preserve negative and ambiguous review outcomes so repeated extraction does not recreate rejected claims.

**Resolve entities conservatively.** Normalize candidate identifiers and labels for search, then compare domain keys, attributes, time, provenance, relationships, and conflict evidence.

Represent candidate, possible match, exact identity, source alias, and rejected match distinctly. Merging nodes is a consequential governance action with downstream inference and access effects.

**Align ontologies rather than flattening them.** Preserve each ontology's namespace, version, authority, assumptions, and model boundaries. Publish qualified mappings whose relation, direction, evidence, confidence, transformation, and limitations are explicit.

Test mappings against competency questions and counterexamples. Local interoperability can succeed through profiles and transformations without universal ontological agreement.

**Version ontology releases.** Record immutable release identifiers, imports, axioms, annotations, shapes, mappings, change classification, compatibility, effective time, migration, and support window.

Keep stable term IRIs when meaning remains compatible; use successor terms when essential meaning changes. Never silently replace the document behind a version IRI.

**Analyze semantic diffs.** Textual triple diffs identify additions and removals but may miss entailment changes. Compute affected classes, properties, constraints, mappings, queries, materialized conclusions, and consumers under the selected regime.

A removed redundant axiom may have no semantic effect; one equivalence addition can have enormous effect. Test representative closures and competency queries.

**Design query datasets.** Specify which graph is default, which named graphs are visible, whether a union is used, which ontology and inferred graph apply, and which time and tenant are selected.

The same SPARQL text can return different answers under different dataset and entailment configurations. Return or expose an answer profile so consumers can interpret results.

**Govern property paths.** Property paths make reachability concise but can cross cycles, relation types, sources, and hidden graph regions.

Apply path allowlists, depth or cost bounds, timeout, result limits, provenance explanation, and access filtering. A path is a query match, not automatically a causal or semantic proof.

**Use OPTIONAL and absence carefully.** Optional patterns preserve solutions when a match is missing. Missing bindings can mean absence, unknown data, inaccessible graph, incompatible version, inference disabled, or query error.

Do not transform every unbound result into “false.” Expose completeness and access limitations where they affect decisions.

**Design APIs beyond raw SPARQL.** Stable domain APIs can expose bounded resources, searches, traversals, explanations, validation, versions, and changes while hiding store-specific complexity.

Raw SPARQL remains valuable for expert exploration but needs parsing limits, prepared patterns, authorization, federation controls, audit, and resource governance. Avoid string concatenation of untrusted query fragments.

**Publish JSON-LD profiles deliberately.** Version contexts, protect term definitions where needed, define `@id`, `@type`, containers, language, base, and graph behavior, and test expansion and round trips.

Compact JSON that looks familiar can expand to unexpected IRIs when contexts drift or are overridden. Cache and authenticate remote contexts according to risk.

**Protect graph semantics.** Access control can depend on tenant, graph, class, predicate, subject, object, provenance, purpose, time, and inferred sensitivity.

Apply authorization before and after inference as needed. A permitted collection of individual triples can jointly reveal a restricted fact through joins or reasoning.

**Prevent inference leakage.** Attackers can ask counts, Boolean questions, alternative paths, timing-sensitive queries, or repeated near-identical queries to infer protected facts.

Use query templates, minimum groups, noise only where justified, denial explanations, budgets, caching, rate limits, monitoring, and expert threat analysis. Simple triple filtering may be insufficient.

**Validate ontology consistency.** Check syntax, imports, profile conformance, unsatisfiable classes, unintended equivalence, disjointness conflicts, datatype issues, property characteristics, cycles under local policy, and expected entailments.

Consistency is model-relative. A consistent ontology can be irrelevant or wrong, and an inconsistent data graph may result from a valuable source conflict that should remain visible.

**Validate data and shapes.** Check identifiers, datatype lexical forms, language tags, required provenance, graph ownership, predicate authority, shape conformance, duplicates, cardinalities, value ranges, referential targets, and exception lifecycle.

Validate before and after inference when downstream behavior depends on entailed types. State whether inferred triples participate in focus-node selection and constraints.

**Test competency questions.** Maintain positive, negative, boundary, contradictory, multilingual, temporal, access-restricted, and performance cases.

Record expected answers, ontology and dataset versions, entailment regime, shapes, query, access role, and tolerances. A query returning rows is not evidence it answers the intended question.

**Observe quality by dimension.** Measure identity resolution precision and recall, source coverage, predicate coverage, provenance coverage, validation results, inconsistency, mapping agreement, staleness, orphan resources, label coverage, query success, explanation quality, correction, and decision outcomes.

Do not compress all dimensions into one graph-quality score. Publish denominators, samples, confidence, limitations, owners, and corrective work.

**Operate ingestion and reasoning.** Define event acceptance, lag, quarantine, retry, checkpoint, reconciliation, ontology activation, inference build, index build, query availability, cache invalidation, and rollback.

Use isolated versioned graph builds for consequential changes. Promote only after validation and representative queries; do not expose a half-loaded or half-reasoned graph.

**Plan for retraction.** Monotonic logical entailment assumes premises accumulate, but operational graphs correct and delete assertions. Track dependencies between derived and asserted facts or rebuild affected closures.

Deleting one premise may retract many conclusions. Cache and materialization architecture must preserve enough justification to avoid stale inferences.

**Reconcile independently.** Compare graph inventory and assertions with authoritative sources, ontology release manifests, mapping registries, query expectations, and access policies.

Ordinary ingestion and reconciliation should not share every resolver, filter, or checkpoint. Agreement between two views built by the same faulty mapping is weak evidence.

**Recover deterministically.** Back up or reproduce source snapshots, immutable ontology releases, mappings, contexts, shapes, provenance, assertions, checkpoints, policy, query profiles, and consumer configuration.

Rebuild into isolation, verify digests and signatures where used, rerun inference and validation, compare competency answers, test access, and reconcile before promotion.

**Manage economics.** Costs include vocabulary design, domain review, identity resolution, extraction, licensing, provenance, storage, indexes, materialization, query compute, validation, access controls, evidence retention, correction, and specialized skills.

Measure time to integrate trusted sources, resolve ambiguity, answer consequential questions, and repair errors—not only triples loaded or ontologies reused.

**Migrate with semantic evidence.** Inventory namespaces, IRIs, blank-node patterns, graphs, ontologies, imports, mappings, contexts, shapes, rules, query datasets, consumers, inference, access, history, and recovery.

Dual-publish representative snapshots, compare canonicalized graph content where appropriate, closures, validation results, competency answers, performance, and authorization. Record every lossy translation.

**Retire without semantic amnesia.** Stop new assertions only after source authority and consumers move. Preserve term and version IRIs, ontology releases, mappings, provenance, contexts, shape versions, query profiles, and decision evidence for required history.

Remove old writers, remote-context dependencies, imports, endpoints, credentials, caches, replicas, and recovery paths only after closure proves they cannot silently reactivate obsolete semantics.

## Definitions and Notation

Let:

- `U` be resources in a universe of discourse;
- `I` be IRIs and `B` blank nodes;
- `L` be literals with lexical form, datatype IRI, and optional language tag;
- `T` be RDF triples in `(subject, predicate, object)` order;
- `D = (G0, {(n_i, G_i)})` be an RDF dataset with default graph `G0` and named graphs `G_i`;
- `O` be ontology axioms and imports under a declared semantics;
- `H` be shapes and operational validation profiles;
- `P` be source, extraction, mapping, and publication provenance;
- `M` be ontology and identity mappings;
- `R` be a selected entailment regime and reasoning configuration;
- `Q` be competency queries with dataset, time, access, and answer profiles; and
- `C` be consumers and decision records.

An RDF triple is:

`t = (s, p, o) in (I union B) x I x (I union B union L)`.

The predicate is always an IRI in RDF 1.1 abstract syntax. A literal cannot be a subject, and prefix notation is not part of the triple identity.

For graph `G`, ontology `O`, and regime `R`, write:

`G union O |=_R t`

when every interpretation satisfying the accepted graph and ontology under `R` also satisfies triple `t`. This is entailment, not observation or source attribution.

Let `Asserted(t, g, p)` mean source graph `g` asserts `t` with provenance `p`. Let `Inferred(t, J, R, v)` mean a reasoning operation under regime `R` and ontology version `v` derived `t` from justification `J`.

These predicates must not be collapsed. A query can return the same triple from several assertions and inference paths with different authority.

Under a simplified RDFS interpretation:

`(A subClassOf B) and (x type A) => (x type B)`

`(p domain A) and (x p y) => (x type A)`

`(p range B) and (x p y) => (y type B)`.

The latter two are entailment rules, not violation reports.

For shapes graph `H`, data graph `G`, focus-node selection `F`, and validation preparation `v`, write:

`Validate(H, G, F, v) = (conforms, results)`.

The result is relative to those inputs and an implementation. It does not state that `G` is complete or true.

Let `CQ = (question, dataset, ontology, regime, shapes, time, access, expected)` be a competency test. A passing test reproduces the expected answer under those declared conditions.

For a mapping `m`, use:

`m = (source_term, target_term, relation, direction, scope, evidence, confidence, version, authority, limitations)`.

Mapping relation may be exact, close, broader, narrower, related, conditional, transformative, incompatible, or unresolved. Avoid reducing it to Boolean equality.

A knowledge-graph capability is fit only if:

`FitKG = Identity and Semantics and Authority and Provenance and Reasoning and Validation and Query and Protection and Operations and Evolution and Closure`.

Each conjunct requires evidence tied to named competency questions and consumer consequences.

## Mechanisms, Invariants, or Proof Structure

Use the following gates to design and review an ontology and knowledge-graph capability.

**Outcome gate.** Name competency questions, decisions, harms, users, sources, answer profiles, latency, history, explanation, and failure behavior.

**Boundary gate.** Define domains, jurisdictions, organizations, systems, populations, graph scopes, time, viewpoints, inclusions, exclusions, and delegated authorities.

**Identity gate.** Govern namespace, IRI, referent, logical and physical identity, blank nodes, Skolem IRIs, aliases, merges, splits, collision, persistence, resolution, and retirement.

**Literal gate.** Validate lexical form, datatype, value interpretation, language, normalization, units, precision, timezone, missingness, and sensitive encoding.

**Ontology gate.** Select vocabulary, class, property, axiom, annotation, module, import, profile, expressivity, ownership, documentation, and version.

**Semantic gate.** Distinguish class, instance, subclass, subproperty, part, role, state, broader concept, domain, range, equivalence, disjointness, restriction, and mapping consequences.

**Assertion gate.** Preserve source graph, predicate authority, time, confidence, provenance, review, status, correction, and evidence for each consequential claim class.

**Acquisition gate.** Define connector, extraction, mapping, identity resolution, snapshot, increment, deletion, quarantine, replay, reconciliation, and closure behavior.

**Alignment gate.** Preserve model boundaries and qualify relation, direction, scope, evidence, confidence, transformation, version, authority, and counterexamples.

**Reasoning gate.** Declare regime, profile, modules, rules, graph scopes, strategy, limits, inconsistency behavior, justification, materialization, invalidation, and performance.

**Validation gate.** Separate ontology consistency, profile conformance, data integrity, shape validation, source verification, competency tests, and real-domain review.

**Temporal gate.** Define assertion valid time, observation, transaction, publication, ontology effective time, correction, snapshot, and historical belief views.

**Query gate.** Specify default and named graphs, inference, shapes, time, tenant, access, property paths, limits, timeout, ordering, pagination, explanation, and completeness.

**Interface gate.** Version SPARQL endpoints, domain APIs, JSON-LD contexts, representations, errors, rate limits, changes, deprecation, and consumer activation.

**Protection gate.** Classify graphs, predicates, nodes, provenance, ontology, mappings, queries, inference, exports, telemetry, and administrative capabilities; test joint inference and side channels.

**Operations gate.** Measure inventory, ingestion, acceptance, lag, quarantine, reconciliation, reasoning, validation, indexes, query service, cache, support, cost, and outcomes.

**Correction gate.** Retract or supersede assertions and mappings, preserve explanation, invalidate inferences and caches, revalidate, notify affected consumers, and repair decisions.

**Recovery gate.** Restore sources, releases, mappings, contexts, shapes, assertions, provenance, policy, checkpoints, indexes, queries, and consumers; reconcile before activation.

**Closure gate.** End unsupported writes, imports, remote contexts, endpoints, credentials, caches, replicas, exports, support, and recovery while preserving required semantic history.

### Executable evidence: bounded RDFS closure and shape check

This Python example computes only transitive subclass, type propagation, and domain and range consequences for a tiny trusted graph, then applies two illustrative closed-world operational checks.

<!-- bijux-verify: {"id":"bounded-rdfs-closure-and-shape-check","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"initial_triples=5\nclosure_triples=11\ninferred_triples=6\ninference_rounds=2\nsubclass_axioms=3\nalice_types=3\nbob_types=2\nconstraint_violations=0\nexample_constraints_pass=true\n","stderr":""}} -->
```python
initial = {
    ("ex:Employee", "rdfs:subClassOf", "ex:Person"),
    ("ex:Manager", "rdfs:subClassOf", "ex:Employee"),
    ("ex:manages", "rdfs:domain", "ex:Manager"),
    ("ex:manages", "rdfs:range", "ex:Employee"),
    ("ex:alice", "ex:manages", "ex:bob"),
}

triples = set(initial)
inference_rounds = 0

while True:
    inferred = set()
    snapshot = list(triples)

    for child, predicate, parent in snapshot:
        if predicate == "rdfs:subClassOf":
            for next_child, next_predicate, next_parent in snapshot:
                if next_predicate == "rdfs:subClassOf" and next_child == parent:
                    inferred.add((child, "rdfs:subClassOf", next_parent))

    for property_id, predicate, class_id in snapshot:
        if predicate == "rdfs:domain":
            for subject, used_property, _ in snapshot:
                if used_property == property_id:
                    inferred.add((subject, "rdf:type", class_id))
        if predicate == "rdfs:range":
            for _, used_property, object_id in snapshot:
                if used_property == property_id:
                    inferred.add((object_id, "rdf:type", class_id))

    for resource, predicate, class_id in snapshot:
        if predicate == "rdf:type":
            for child, relation, parent in snapshot:
                if relation == "rdfs:subClassOf" and child == class_id:
                    inferred.add((resource, "rdf:type", parent))

    new_triples = inferred - triples
    if not new_triples:
        break
    triples.update(new_triples)
    inference_rounds += 1

alice_types = {object_id for subject, predicate, object_id in triples if subject == "ex:alice" and predicate == "rdf:type"}
bob_types = {object_id for subject, predicate, object_id in triples if subject == "ex:bob" and predicate == "rdf:type"}
subclass_axioms = {triple for triple in triples if triple[1] == "rdfs:subClassOf"}

constraint_violations = 0
for subject, predicate, object_id in triples:
    if predicate == "ex:manages":
        constraint_violations += (subject, "rdf:type", "ex:Manager") not in triples
        constraint_violations += (object_id, "rdf:type", "ex:Employee") not in triples

print(f"initial_triples={len(initial)}")
print(f"closure_triples={len(triples)}")
print(f"inferred_triples={len(triples - initial)}")
print(f"inference_rounds={inference_rounds}")
print(f"subclass_axioms={len(subclass_axioms)}")
print(f"alice_types={len(alice_types)}")
print(f"bob_types={len(bob_types)}")
print(f"constraint_violations={constraint_violations}")
print(f"example_constraints_pass={str(constraint_violations == 0).lower()}")
```

The expected output reports `initial_triples=5`, `closure_triples=11`, `inferred_triples=6`, `inference_rounds=2`, `subclass_axioms=3`, `alice_types=3`, `bob_types=2`, `constraint_violations=0`, and `example_constraints_pass=true` on separate lines.

The evidence is deliberately narrow. Compact strings are not expanded or validated IRIs. The closure implements only four invented RDFS-style rules and ignores axiomatic triples, subproperties, containers, datatypes, blank nodes, graph boundaries, OWL, inconsistency, and justifications. The final checks are closed-world application conditions, not SHACL execution. Trusted triples do not prove authoritative or accurate facts. Production assurance requires conforming parsers and reasoners, ontology and profile tests, shapes-engine tests, provenance and identity verification, source reconciliation, competency questions, adversarial inference and access tests, performance limits, recovery exercises, and accountable domain acceptance.

## Alternatives and Trade-Offs

**Relational integration.** Relational schemas and views provide mature constraints, transactions, optimization, and skills. Cross-domain semantic links and heterogeneous evolution may require many joins and custom mappings; graph capability should complement rather than reflexively replace them.

**Property graph.** Property graphs often provide direct labels and properties on nodes and edges plus efficient traversal. Semantics, interchange, identity, and inference vary by product and model; define them explicitly.

**RDF knowledge graph.** RDF supplies global identifiers, a standard graph model, multiple serializations, formal semantics, and SPARQL. It introduces unfamiliar open-world and identity behavior and requires careful graph, ontology, and provenance governance.

**Document search and retrieval.** Search can answer discovery questions cheaply without formal modeling. It cannot by itself provide stable entity identity, declared relations, logical inference, or deterministic structured answers.

**Glossary or SKOS scheme.** Lightweight concepts and labels support navigation, terminology, and mapping with lower governance cost. They do not define every concept as a logical class or support all desired entailments.

**RDF Schema.** Simple subclass, subproperty, domain, and range semantics are widely understandable. Domain and range inference can surprise teams that expect validation, and expressive limits remain.

**OWL 2 EL.** EL suits large class-rich ontologies and classification workloads. Its supported constructs are restricted; verify that competency questions fit rather than assuming profile names guarantee performance.

**OWL 2 QL.** QL is designed around query answering over large data through rewriting. Richer class-expression needs may fall outside the profile, and source database semantics still need alignment.

**OWL 2 RL.** RL supports rule-oriented scalable reasoning. Rule materialization, equality, inconsistency, and retraction can still be operationally expensive.

**Full OWL 2.** Greater expressivity can represent complex domain constraints and yield powerful conclusions. Modeling skill, computational cost, explanation, and consumer misunderstanding grow substantially.

**Application rules.** Code can implement procedural, closed-world, temporal, and consequence-specific behavior. Semantics can fragment across services and become hard to inspect unless rules are versioned, tested, and linked to concepts.

**SHACL validation.** Shapes provide explicit operational constraints and structured reports. They do not replace source verification, ontology consistency, or domain legitimacy, and complex shapes can be expensive.

**Forward materialization.** Read queries are fast and conclusions can be inspected. Storage, update amplification, provenance, and retraction become difficult.

**Query rewriting or backward reasoning.** Conclusions remain tied to current premises and flexible query profiles. Query plans can grow, latency is less predictable, and access filtering is harder.

**One canonical ontology.** A single model simplifies some queries and governance. It can erase bounded contexts, create central bottlenecks, and turn approximate mappings into false universal truth.

**Federated ontologies.** Domains retain authority and conceptual fit. Alignment, discovery, cross-domain querying, version coordination, and conflict require shared capabilities.

**Central graph store.** Centralization simplifies indexing, inference, and traversal. It concentrates sensitive relationships, operational risk, cost, and semantic power.

**Federated query.** Sources retain control and freshness. Availability, latency, semantic drift, authorization, query planning, and consistent snapshots become difficult.

**Full provenance retention.** Detailed source and inference evidence improves assurance and correction. Storage, disclosure, licensing, retention, and query complexity increase.

**Curated decision views.** Bounded graphs improve trust, performance, and comprehension. They require continuous product ownership and may omit exploratory value.

## Failure Modes and Misconceptions

1. **“A graph database is an ontology.”** Storage topology does not specify logical meaning.
2. **“An ontology is the knowledge graph.”** Ontology axioms and populated operational assertions are different layers.
3. **“More triples mean more knowledge.”** Duplication, noise, stale facts, and meaningless links can grow counts.
4. **“An IRI is meaningful because it resolves.”** Resolution and intended referent require governance; RDF identity is not network availability.
5. **“Prefixes are namespaces in the graph.”** Prefixes are syntax conveniences; expanded IRIs determine identity.
6. **“Blank-node labels are stable IDs.”** Their scope is local to a serialization or implementation context.
7. **“Different IRIs always mean different things.”** RDF and OWL do not generally assume unique names.
8. **“Matching labels mean the same concept.”** Labels are language- and context-dependent lexical forms.
9. **“Subclass means any parent-child relation.”** It asserts inclusion of every instance under the semantics.
10. **“Part-of is a subclass.”** Composition and classification have different consequences.
11. **“Domain restricts who may use a property.”** RDFS domain use entails subject type; it is not an input form rule.
12. **“Range rejects wrong objects.”** RDFS range entails object type; validation requires a constraint profile.
13. **“Missing means false.”** Open-world reasoning treats many missing statements as unknown.
14. **“A cardinality axiom requires a stored value.”** Logical existence can be satisfied without an explicit named value.
15. **“A shape is an ontology axiom.”** Validation conditions and logical semantics answer different questions.
16. **“Conformance proves truth.”** Shapes test a graph under a profile, not source accuracy or legitimacy.
17. **“Consistency proves correctness.”** A consistent model can describe the wrong world.
18. **“Equivalence improves harmless discoverability.”** It can merge classes, properties, or individuals throughout inference.
19. **“Importing a standard vocabulary guarantees interoperability.”** Profiles, versions, identifiers, values, and use constraints still differ.
20. **“One ontology should replace domain models.”** Bounded meanings and authorities can legitimately coexist.
21. **“A reasoner discovers new observations.”** It derives consequences of premises under semantics.
22. **“Inferred facts need no provenance.”** Regime, premises, versions, and computation matter to explanation and retraction.
23. **“One reasoner result is portable.”** Profiles, supported features, graph scope, datatypes, and inconsistency handling can differ.
24. **“Named graphs inherently mean provenance.”** Their interpretation is application-defined.
25. **“The default graph is always the union.”** Dataset construction is part of the query contract.
26. **“A property path proves a semantic relationship.”** It proves a pattern match under selected data and path semantics.
27. **“OPTIONAL returning unbound proves absence.”** Data, access, time, and inference may be incomplete.
28. **“JSON-LD is ordinary JSON with links.”** Context expansion determines RDF identifiers and structure.
29. **“Remote contexts are harmless metadata.”** Drift or compromise can change expansion and meaning.
30. **“Entity resolution is a string join.”** Sameness requires domain, time, source, and conflict evidence.
31. **“Machine extraction produces facts.”** It produces attributable candidates with error and bias.
32. **“Triple filtering prevents disclosure.”** Joins, inference, counts, timing, and repeated queries can leak facts.
33. **“Materialized inference updates itself.”** Retraction requires dependency tracking or safe recomputation.
34. **“Deleting an old ontology cleans the system.”** Historical graphs and decisions can become uninterpretable.

## Worked Examples

### Example 1

A product catalog uses stable IRIs for product models, organizations, and regulated materials. Labels exist in six languages and can change independently. Supplier identifiers remain source-specific until reviewed identity mappings establish equivalence; the graph never merges companies merely because normalized names match.

### Example 2

A team models `manages` with domain `Manager` and range `Employee`. When a source asserts that Alice manages Bob, the reasoner entails those types. The ingestion team had expected invalid inputs to be rejected, so architects move the operational checks into shapes and retain the ontology axioms only after confirming their universal semantic intent.

### Example 3

A record lacks a termination date. An open-world query reports the date as unknown. A compliance profile validates a closed monthly employee roster declared complete by HR and reports a missing required date only for records with termination status. The entailment and validation answers coexist without contradiction.

### Example 4

A business glossary concept “active customer” remains a SKOS concept with multilingual labels and scoped mappings. A formal eligibility ontology defines classes for one regulated decision. The system links the glossary concept to the ontology artifact through a qualified mapping rather than claiming the concept and class are universally identical.

### Example 5

Two domain ontologies use different models for address: one treats it as a mutable entity and another as a time-bounded role at a location. A cross-domain profile transforms only the fields needed for shipping and records information loss. It rejects `owl:equivalentClass` even though both classes have the English label “Address.”

### Example 6

A knowledge-extraction model proposes that a supplier uses a restricted component. The graph stores candidate assertion, document span, model and configuration version, confidence, extraction activity, and review state in a protected graph. Only accepted assertions enter the procurement decision view; rejected candidates remain bounded evidence against automatic reintroduction.

### Example 7

A SPARQL property path can cross ownership, subsidiary, supplier, and component relations to identify vulnerability candidates. The production API allows only approved path templates, bounds depth and runtime, checks predicate and node access, returns provenance per hop, and labels hidden boundaries rather than exposing unrestricted federation.

### Example 8

An ontology release adds equivalence between two widely used classes. Textual diff shows one triple, but semantic-diff tests reveal thousands of new inferred types and several disjointness conflicts. The release is blocked until the mapping is weakened, affected shapes are updated, and competency questions pass.

### Example 9

A remote JSON-LD context changes a compact term from one predicate IRI to another. The ingestion system pins and verifies approved context versions, expands documents before acceptance, and quarantines unexpected context digests. A friendly JSON payload therefore cannot silently change graph meaning.

### Example 10

During graph-platform migration, teams export immutable source graphs, ontology releases, mappings, contexts, shapes, and provenance. They compare expanded and canonicalized representations where suitable, inference closures, validation reports, competency answers, authorization, latency, and recovery. Every unsupported inference feature is recorded as loss before consumers activate the replacement.

## Cross-Program Connections

- **Data engineering:** source extraction, snapshots, change events, normalization, identity resolution, graph construction, reconciliation, and materialized views populate knowledge graphs.
- **API and service engineering:** identifiers, content negotiation, JSON-LD contexts, SPARQL and domain APIs, pagination, errors, authorization, rate limits, versioning, and deprecation shape graph access.
- **Platform engineering:** namespace registries, ontology repositories, connector frameworks, reasoners, validation services, graph storage, secrets, observability, tenancy, recovery, and cost enable self-service.
- **Database engineering:** indexing, query optimization, recursive evaluation, transactions, consistency, temporal storage, compression, partitioning, and backup determine operational behavior.
- **Logic and discrete mathematics:** interpretations, relations, entailment, satisfiability, monotonicity, complexity, graph traversal, closure, and countermodels ground semantic claims.
- **Software engineering:** type systems, schemas, modules, dependency management, semantic versioning, compilers, tests, and package publication resemble ontology lifecycle mechanisms.
- **Machine learning engineering:** embeddings, extraction, entity resolution, retrieval, feature construction, model provenance, confidence, evaluation, and feedback interact with symbolic graphs.
- **Security engineering:** namespace control, authenticated publication, integrity, query injection, access, graph inference, side channels, incident response, and dependency trust constrain service.
- **Privacy engineering:** linkability, sensitive relations, purpose, minimization, inference, redaction, retention, correction, and cross-border sharing shape graph design.
- **Human-computer interaction:** labels, multilingual display, search, explanation, uncertainty, provenance, accessible visualizations, and correction channels determine whether users understand answers.
- **Organizational design:** domain authorities, ontology owners, stewards, source owners, platform teams, consumers, reviewers, and affected communities hold different decision rights.
- **Systems engineering:** stakeholder questions, boundaries, interface control, configuration, hazards, verification, validation, assurance cases, and lifecycle govern semantic infrastructure.

## References

1. W3C, [“RDF 1.1 Concepts and Abstract Syntax”](https://www.w3.org/TR/rdf11-concepts/), 2014. Retrieved 2026-09-03.
2. W3C, [“RDF 1.1 Semantics”](https://www.w3.org/TR/rdf11-semantics/), 2014. Retrieved 2026-09-03.
3. W3C, [“RDF Schema 1.1”](https://www.w3.org/TR/rdf-schema/), 2014. Retrieved 2026-09-03.
4. W3C, [“OWL 2 Web Ontology Language Document Overview, Second Edition”](https://www.w3.org/TR/owl2-overview/), 2012. Retrieved 2026-09-03.
5. W3C, [“OWL 2 Web Ontology Language Profiles, Second Edition”](https://www.w3.org/TR/owl2-profiles/), 2012. Retrieved 2026-09-03.
6. W3C, [“SPARQL 1.1 Query Language”](https://www.w3.org/TR/sparql11-query/), 2013. Retrieved 2026-09-03.
7. W3C, [“Shapes Constraint Language (SHACL)”](https://www.w3.org/TR/shacl/), 2017. Retrieved 2026-09-03.
8. W3C, [“SKOS Simple Knowledge Organization System Reference”](https://www.w3.org/TR/skos-reference/), 2009. Retrieved 2026-09-03.
9. W3C, [“PROV-O: The PROV Ontology”](https://www.w3.org/TR/prov-o/), 2013. Retrieved 2026-09-03.
10. W3C, [“JSON-LD 1.1”](https://www.w3.org/TR/json-ld11/), 2020. Retrieved 2026-09-03.

## Exercises

### Exercise 1

Design an ontology and knowledge-graph profile for products, components, suppliers, materials, jurisdictions, and restrictions. Specify competency questions, identity, classes, properties, mappings, source authority, provenance, reasoning, shapes, time, access, and correction.

### Exercise 2

A team encoded required fields with OWL cardinality restrictions, encoded UI categories as subclasses, and uses domain and range to reject data. Diagnose the semantic errors and design a corrected division among ontology axioms, SKOS organization, SHACL validation, and application policy.

### Exercise 3

Three graphs describe the same organizations with different identifiers, names, parent relationships, effective dates, and confidence. Design entity resolution and ontology alignment without assuming unique names, string equality, or universal equivalence.

### Exercise 4

A knowledge graph reports 600 million triples, 99.2 percent shape conformance, and median query latency of 120 milliseconds. Design a scorecard for semantic, source, identity, provenance, inference, validation, query, protection, operation, economics, and decision outcomes.

### Exercise 5

Migrate a central RDF store using mutable ontologies, live remote JSON-LD contexts, forward materialization, and unrestricted SPARQL into a governed federated capability. Design versioning, semantic diffs, dual publication, query comparison, authorization, retraction, recovery, activation, and retirement.

## Answers to the Exercises

### Answer 1

Start with questions: which products contain a restricted material in a jurisdiction at an effective time; which suppliers and evidence support the claim; which components become candidates after a rule change; and what remains unknown. Mint persistent IRIs under owned namespaces for logical products, component versions, supplier source identities, material concepts, jurisdictions, rules, assertions, and evidence. Model composition, supply, classification, applicability, and restriction as distinct relations; use n-ary assertion resources when quantity, role, interval, source, or confidence matters.

Preserve source graphs and predicate authority. Resolve suppliers through governed candidates and decisions rather than names. Use SKOS for material vocabularies and qualified cross-scheme mappings; use an appropriately bounded OWL or RDFS profile only for defensible entailments. Define shapes for required version, provenance, units, intervals, and decision inputs. Version ontology, mappings, shapes, rules, and graph snapshots. Test positive, negative, boundary, conflicting, historical, unknown, and protected questions. Authorize nodes, edges, provenance, inference, and exports; record redaction. Corrections supersede claims, invalidate conclusions, notify affected product decisions, and preserve the earlier belief view.

### Answer 2

OWL cardinality restrictions describe logical classes and may entail that some value exists without requiring a stored explicit value; use SHACL minimum and maximum counts when a declared-complete data profile must contain explicit fields. A subclass axiom means every instance of the child is an instance of the parent, so UI grouping that lacks that inclusion belongs in SKOS collections, broader relations, annotations, or presentation configuration. RDFS domain and range infer types from property use; they do not reject inputs. Keep them only when those type consequences are universally intended.

Define ontology axioms for stable domain semantics and logical inference, SKOS for concepts and navigational organization, SHACL for target-specific structural and value checks, and application policy for workflow, permissions, exceptions, remediation, and transactions. Name the data and shapes graphs, inference preparation, ontology version, focus nodes, severity, and completeness assumption. Add counterexamples showing missing, multiple, unexpected, unknown, and temporally scoped values. Test both inferred consequences and validation reports so teams do not replace one semantic confusion with another.

### Answer 3

Preserve every source identifier, graph, claim, date, confidence, and authority. Mint enterprise identity-decision resources only where cross-source use requires them. Generate candidates from normalized names and identifiers, then compare legal identifiers, jurisdictions, addresses, time, parent evidence, domain keys, and contradictions. Model candidate, possible match, exact same referent, source alias, historical predecessor, and rejected match separately. Distinct IRIs do not prove difference, and shared names do not prove sameness.

Keep each source ontology and relationship meaning. Map parent, owner, member, subsidiary, reporting unit, and brand only after testing direction, transitivity, legal versus operational scope, and time. Use exact equivalence rarely; prefer close, conditional, broader, narrower, or transformative mappings with versions and counterexamples. Let decision profiles select authoritative predicates rather than ingestion order. Measure resolution precision and recall on representative labeled cases, preserve appeals and splits, recompute inference and access after merges, and ensure history can explain past organization structures.

### Answer 4

Triple count measures volume, conformance measures only selected shapes and targets, and median latency hides expensive or denied questions. Define critical competency questions and decisions, then segment source inventory by authority, domain, time, graph, predicate, and criticality. Measure source and predicate coverage, freshness, deletion and correction, stable IRI and referent governance, unresolved and false identity merges, label and language coverage, provenance and evidence, mapping confidence, ontology profile conformance, consistency, unintended equivalence, expected entailments, stale materialization, and retraction accuracy.

For validation, report shapes and graph versions, focus-node coverage, severity, exceptions, false positives and negatives, and remediation. For queries, test answer correctness, completeness assumptions, explanation, time, named-graph scope, access, tail latency, path cost, timeouts, pagination, and injection resistance. Test joint inference, hidden paths, counts, timing, remote context integrity, and exports. Measure ingestion and reasoning lag, quarantine, reconciliation, availability, cache invalidation, recovery point and time, rebuild comparison, storage and compute, ontology and steward effort, integration lead time, correction time, prevented errors, and consumer decision success. Keep dimensions and denominators visible.

### Answer 5

Inventory every namespace, IRI policy, graph, blank-node pattern, ontology and import, mapping, context, shape, rule, source, connector, assertion class, provenance record, materialized conclusion, query dataset, endpoint, consumer, access rule, cache, backup, and obligation. Publish immutable ontology, mapping, shape, and context releases with digests and effective times. Expand and verify JSON-LD against pinned contexts. Compute textual and semantic diffs, affected conclusions, validation changes, competency answers, and consumers before activation.

Create federated source graphs with explicit authority and a curated decision view. Dual-publish representative snapshots, compare expanded graph content where suitable, closures, justifications, shape reports, queries, redaction, tail performance, and failure behavior. Bound SPARQL with authorized datasets, templates or quotas, path limits, timeouts, result controls, and audit. Track premises for materialized conclusions or rebuild safe isolated closures on retraction. Test source outage, conflict, remote-context failure, inconsistent ontology, rollback, replay, and restoration. Activate consumers by consequence and reconcile. Retire old writes only after sources and consumers move; remove live contexts, endpoints, credentials, caches, and recovery paths while preserving resolvable historical semantics and evidence.
