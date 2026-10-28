---
module_id: DARCH-012
program: Data Architecture Engineering
level: 1
module_number: 12
title: Logical Data Models
status: complete
last_verified: 2026-09-03
---

# Logical Data Models

## One-Page Review

### Governing question

How can a team translate conceptual meaning into precise, technology-independent information structures and constraints while preserving identity, time, provenance, compatibility, and alternatives for later physical realization?

### Essential definitions

- A **logical data model** specifies information structures, types, keys, relationships, constraints, derivations, and lifecycle semantics in a chosen data-modeling paradigm without committing to a particular database product, deployment, index, partition, or encoding.
- A **logical record type** groups named fields and constraints representing an information unit; it is not automatically a physical row, document, or message.
- A **business key** is a value or tuple whose uniqueness and stability follow from a bounded domain rule; a **surrogate identifier** is introduced for representation or processing and does not create business identity.
- A **functional dependency** `X -> Y` states that equal values of attribute set `X` imply equal values of `Y` within a declared relation and scope.
- A **normal form** is a structural condition intended to reduce specified redundancy and update anomalies under stated dependencies.
- **Optionality** states whether a value or relationship may be absent under a model rule; **missingness semantics** explain why an observed representation lacks a value.
- A **logical constraint** restricts permitted states or transitions; enforcement may later be allocated to databases, services, pipelines, workflows, or human authority.
- A **mapping** states how conceptual elements correspond to logical structures, including transformation, loss, scope, version, and evidence.

### Central model, mechanism, or theorem

Represent a logical model as:

`L = (structures, types, keys, dependencies, constraints, time, mappings, versions)`

For every in-scope conceptual proposition, the logical model must provide a representable, constrained, and traceable encoding or an explicit disposition. For every logical element, it must provide conceptual justification or identify necessary technical metadata. Logical validity requires structural well-formedness and constraint satisfiability; adequacy additionally requires scenario coverage, semantic fidelity, feasible evolution, and evidence. Passing schema validation establishes only the encoded fragment.

### Critical invariants

- Every logical structure names purpose, conceptual source, identity, grain, authority, lifecycle, and applicable version.
- Business identity and representation identifiers remain distinct; keys state issuer, uniqueness scope, stability, reuse, and temporal rules.
- Fields define value semantics, type, unit, scale, precision, allowed values, missingness, sensitivity, provenance, and derivation as applicable.
- Relationships state participant roles, cardinality, optionality, ownership, referential behavior, time, and integrity obligations.
- Dependencies and normalization decisions are supported by domain rules rather than inferred from a convenient sample.
- Repeated, multivalued, ordered, and n-ary facts preserve their grain instead of being packed into ambiguous fields.
- Current state, history, events, valid time, recorded time, correction, deletion, and retention are modeled deliberately.
- Constraints state enforcement responsibility, transaction or consistency boundary, failure behavior, evidence, and exceptions.
- Conceptual-to-logical and cross-paradigm mappings record transformation and information loss; similar names do not prove equivalence.
- Physical concerns may inform feasibility, but products, indexes, partitions, files, and topology do not silently define logical meaning.

### Common failures

Common failures are relabeling an existing schema as logical; treating each concept as one record; choosing surrogate keys before identity rules; assuming a primary key is a business key; deriving dependencies from a small dataset; comma-separating repeated values; using null for unknown, absent, inapplicable, redacted, and not-yet-known; forgetting grain; putting state and event in one mutable row; encoding units in field names; copying source enumerations without meaning; normalizing mechanically; denormalizing without anomaly analysis; omitting referential and lifecycle behavior; confusing JSON validation with semantic completeness; and declaring a model technology-independent while embedding vendor types or deployment mechanisms.

### Compact example

A logical `Order` record contains customer name, three product columns, current status, total, and nullable cancellation date. Conceptual review shows orders have stable business identifiers, parties act in roles, lines repeat, prices carry currency and tax basis, status changes are events, and absence of cancellation can mean active, rejected, unknown, or legacy-missing. The revised logical model separates Order, Order Party Role, Order Line, Monetary Amount, Status Transition, and source assertions with explicit keys, grain, time, and constraints. A relational, document, or event realization can now preserve the same commitments with declared trade-offs.

### Connections

[DARCH-011](011-conceptual-data-models.md) supplies concepts, identity, relationships, contexts, and rules. This module makes them structurally precise. [DARCH-013](../ROADMAP.md) protects the separation from physical realization, while [DARCH-014](../ROADMAP.md) deepens entities, relationships, and business keys. Later modules cover normalization, canonical models, history, schemas, events, and evolution.

## Governing Question

A conceptual model says what distinctions matter. A logical model decides how those distinctions can be represented and constrained in an information model. It introduces record, relation, field, key, reference, collection, graph, message, union, enumeration, constraint, and temporal structures without yet choosing a particular storage engine or deployment.

This is not a purely mechanical translation. One conceptual relationship may become a reference, associative structure, nested collection, edge, assertion, or event. One conceptual entity may need several logical structures for identity, history, roles, and claims. Conversely, one logical projection may combine several concepts for an exchange or decision. Each choice changes expressible constraints and evolution behavior.

The logical model must serve declared uses without becoming their first physical optimization. It should be precise enough to test keys, cardinalities, types, dependencies, missingness, temporal rules, and compatibility, while retaining alternatives for storage, access paths, distribution, and encoding.

## Why This Matters

Weak logical models make semantic error executable. If grain is unstated, totals double-count. If business keys are unstable, corrections split identity. If missingness is ambiguous, absence becomes false. If units and time zones are implicit, values compare incorrectly. If events are overwritten by state, audit and reconstruction fail.

E. F. Codd's [1970 relational-model paper](https://doi.org/10.1145/362384.362685) argued for independence from internal representation and described data through relations rather than machine access paths. That separation remains central even when the chosen logical paradigm is relational, document, graph, event, or RDF. The paper does not imply that every logical model must be relational or that SQL implementations perfectly realize relational theory.

ISO/IEC [9075-1:2023](https://www.iso.org/standard/76583.html) defines the conceptual framework and terminology used by the SQL standard family, including tables, data types, schema objects, and integrity constraints. It is authoritative for standardized SQL concepts within its scope, not a substitute for domain analysis, a complete logical-design method, or proof of portability across products.

Logical modeling makes architecture review possible before physical commitments dominate. Teams can compare paradigms, expose information loss, validate constraints with fixtures, plan compatibility, and assign enforcement. The result becomes a contract between meaning and realization.

## Prerequisites and Retrieval

You should understand conceptual models, sets and relations, records, data types, identity and identifiers, cardinality, events and state, valid and recorded time, provenance, bounded contexts, interfaces, constraints, data quality, and basic database operations.

Retrieve entity type, value type, role, event, logical relation, tuple, attribute, record, field, key, candidate key, foreign key, reference, collection, node, edge, triple, functional dependency, determinant, normal form, union, enumeration, optionality, missingness, grain, invariant, derivation, schema, writer and reader, compatibility, and physical realization.

As a retrieval test, inspect `customer_id STRING NOT NULL`. Ask which customer concept and context it identifies, who issues it, where uniqueness holds, whether it changes or is reused, whether it is a business or surrogate key, how merges and splits work, what the string grammar is, which versions accept it, and what evidence enforces the rule. Syntax alone answers almost none of these questions.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish conceptual, logical, physical, storage, and exchange models;
2. define logical structures by purpose, grain, identity, fields, relationships, constraints, time, authority, and version;
3. select and document candidate, primary, alternate, surrogate, composite, and external keys;
4. state functional and multivalued dependencies and apply normalization from domain rules;
5. represent optional, missing, unknown, inapplicable, redacted, disputed, and not-yet-observed information honestly;
6. model repeating, ordered, n-ary, temporal, historical, event, state, and assertion structures;
7. compare relational, document, graph, RDF, event, and message logical paradigms;
8. allocate integrity constraints across bounded consistency and authority domains;
9. design versioning, compatibility, migration, and deprecation before physical rollout;
10. validate logical structure, semantics, scenarios, mappings, constraints, and evidence without overclaim.

## Core Exposition

**Bind the model to purpose and context.** Record model identifier, owner, stakeholders, competency questions, conceptual baseline, boundaries, lifecycle and jurisdiction, expected uses, source authority, status, version, effective interval, assumptions, and exclusions. A universal “enterprise logical model” without purposes or contexts tends to become either vague or coercive.

**Define each structure's grain.** Grain states what one occurrence represents. One row per order, one message per accepted state transition, one node per governed identity, or one assertion per source-subject-predicate-valid-interval are different grains. State uniqueness and temporal scope. Many aggregation and join defects are grain mismatches disguised as arithmetic errors.

For each structure record stable identifier, logical name, purpose, grain, conceptual mapping, keys, fields, relationships, constraints, lifecycle, authority, provenance, security classification, quality obligations, version, and examples. Keep display layout separate from logical order unless order itself has meaning.

**Select a logical paradigm deliberately.** A relational model uses relations, tuples, attributes, domains, keys, and constraints. A document model organizes nested objects, arrays, alternatives, and references. A property graph uses nodes, labeled or typed relationships, and properties. RDF represents graph statements as triples with IRIs, literals, and blank nodes. Event and message models represent occurrences and exchange contracts. Each supports different constraints and evolution patterns.

The W3C [RDF 1.1 Concepts](https://www.w3.org/TR/rdf11-concepts/) specification defines RDF graphs, triples, IRIs, blank nodes, and literals. RDF's graph semantics are not the same as a property graph, and neither is merely a relational schema drawn with circles. State exact paradigm and semantics rather than using “graph” generically.

One architecture can use several paradigms. The obligation is to preserve conceptual commitments and define mappings, not make every representation identical. A relational authority store, event contract, document API, graph projection, and analytical star can coexist if identity, meaning, time, loss, and ownership are controlled.

**Map conceptual elements explicitly.** A mapping record should name conceptual source, logical target, mapping type, conditions, transformation, cardinality, temporal semantics, loss, authority, version, evidence, and reverse-map limitations. Common types include direct representation, decomposition, composition, role realization, event projection, derived field, code mapping, and deliberately unmapped technical metadata.

One concept need not become one structure. Person identity, identifiers, names, addresses, roles, assertions, and history may require several structures. One structure need not map to one concept: an exchange message can compose Order, Buyer Role, Delivery Commitment, and Price Assertion for a bounded action.

**Model value domains.** Define logical type, lexical grammar, semantic domain, unit, scale, precision, range, normalization, collation, time zone, language, encoding assumptions, allowed values, special values, and validation. `decimal(10,2)` cannot state currency, tax basis, rounding, or meaning. `timestamp` cannot state event, validity, clock, offset, precision, or uncertainty.

Prefer explicit types such as Monetary Amount plus Currency, Temperature plus Unit and Measurement Method, or Zoned Instant plus source-clock evidence. Decide whether the pair is atomic for consistency and exchange. Do not encode semantic units only in names like `weight_kg`; that invites incompatible copies.

**Establish keys from identity rules.** Candidate keys are minimal attribute sets that uniquely identify an occurrence under stated rules. Choose a primary logical key for references, but preserve alternate keys when meaningful. Record issuer, uniqueness scope, stability, reuse prohibition or interval, nullability, case/collation, canonicalization, correction, merge/split, and source evidence.

Surrogate identifiers help when business keys are large, mutable, private, composite, delayed, or source-specific. They do not eliminate the business uniqueness rule or identity-resolution problem. A generated UUID can distinguish records while two records still refer to the same person, or one record changes which person it represents.

Composite keys can express grain honestly: `(order_id, line_number)` or `(sensor_id, observed_at, sequence)` may identify occurrences within scope. A single surrogate can simplify references but must not hide the composite candidate key and its constraints.

**Define relationships and references.** Map participant roles, direction, cardinality, optionality, identifying status, ownership, lifecycle, time, referential actions, and cross-boundary authority. A foreign-key-like reference says how logical identity is connected; it does not by itself decide physical co-location or synchronous enforcement.

Referential behavior must match lifecycle. On retirement, should dependent data be prohibited, cascaded, retained with historical reference, anonymized, re-parented, or marked unresolved? Automatic cascade can destroy evidence; indefinite restriction can defeat lawful deletion. Model the semantic rule and allocate later enforcement with appropriate authority.

**Represent many-to-many and n-ary facts at their own grain.** An Order Line relates Order, Product Offer, Quantity, Price Assertion, and fulfillment conditions. Flattening product columns or storing comma-delimited identifiers loses cardinality, typing, independent time, and constraints. Nested arrays can preserve repetition, but their element identity, order, uniqueness, and update semantics still need definition.

**State dependencies before normalization.** A functional dependency `X -> Y` is a claim about all permitted instances under a declared scope, not a correlation in sampled data. Derive it from identity, policy, or domain invariants and challenge exceptions. If `postal_code -> city` holds only in one country and period, scope it; do not normalize globally from local observations.

Normalization decomposes structures to reduce specified redundancy and anomalies while preserving information and, ideally, dependencies. First, second, third, Boyce–Codd, fourth, and fifth normal forms address different dependency structures. Apply the level justified by dependencies and uses; “normalized” without named rules is not evidence.

Lossless decomposition means joining decomposed relations under applicable constraints reconstructs the original permitted information without spurious tuples. Dependency preservation asks whether constraints can be enforced without recombining structures. A decomposition may be lossless yet make important constraints expensive or distributed.

**Analyze anomalies rather than worship form.** Update anomalies allow one fact to disagree across copies; insertion anomalies require unrelated facts; deletion anomalies erase facts unintentionally. Denormalization can be a legitimate logical projection for exchange or analytics when authority, refresh, derivation, reconciliation, and anomaly controls are explicit. Physical duplication for performance belongs later.

**Model missingness deliberately.** Absence can mean unknown, not yet observed, not applicable, withheld, redacted, invalid, lost, not authorized, or genuinely optional. One null marker cannot preserve all distinctions. Choose separate status, assertion, union/variant, related structure, or explicit value when the distinction affects decisions.

SQL null and three-valued logic have precise operation-dependent consequences that surprise teams expecting ordinary equality. A nullable field definition must state allowed reason and downstream logic. Never infer domain optionality solely because a source column contains nulls; nulls may be defects or migration artifacts.

Document and message schemas also distinguish missing, explicit null, empty, defaulted, and unknown fields differently. JSON Schema [Draft 2020-12](https://json-schema.org/draft/2020-12) separates core and validation vocabularies and can constrain JSON instances. Schema validity does not assign business meaning to absence or guarantee producer/consumer behavior.

**Model alternatives and variants.** Use tagged unions or discriminated variants when an occurrence can take one of several structures. State discriminator authority, exhaustiveness, unknown variant behavior, shared fields, and compatibility. Optional fields are not a safe substitute for variants when combinations must be prohibited.

Enumerations need stable codes, definitions, authority, effective intervals, ordering semantics, unknown-value behavior, extension rules, and deprecation. Display labels are not codes. Consumers must distinguish unrecognized future values from corrupt input and from a legitimate `UNKNOWN` domain value.

**Separate event, state, and command.** A command requests action, an event records an occurrence, and state represents a condition, often derived from events and rules. One mutable `status` field loses transition history, actor, cause, evidence, and correction. An event-only model may make current decisions expensive or ambiguous without projection rules and versioned reducers.

Define event identity, subject, type, occurred and recorded time, sequence, producer, authority, payload, causation, correlation, idempotency, correction/retraction, schema version, and retention. Define state projection, invariants, checkpoint, replay, late events, conflicts, and rebuild evidence.

**Represent time and history.** Distinguish valid time from recorded or transaction time, event time from processing time, intervals from instants, planned from actual, and source clock from normalized time. State inclusive/exclusive endpoints, granularity, zone, leap/clock policy, uncertainty, overlap, and correction.

History patterns include versioned assertions, effective-dated structures, append-only events, bitemporal relations, snapshots, and change logs. These are not interchangeable. Choose based on competency questions: what was believed, what was valid, what changed, who asserted it, and whether prior decisions must be reconstructed.

**Model provenance and assertions.** When sources can disagree, represent assertion identity, subject, value or relationship, source, authority, evidence, valid interval, recorded time, confidence, classification, and adjudication. A single “source_system” field on a mastered row cannot explain per-attribute or relationship provenance.

Derived fields name expression, input versions, rule version, rounding, effective interval, owner, and recomputation behavior. Avoid storing a derivation as if independently authoritative. If materialized, define reconciliation and what happens when past rules or inputs change.

**Specify integrity beyond syntax.** Include type, domain, uniqueness, referential, cardinality, exclusivity, conditional, aggregate, temporal, transition, cross-structure, and authorization constraints. State severity, enforcement point, consistency boundary, failure behavior, remediation, exception, monitoring, and evidence.

Some constraints cannot be transactionally enforced in one system. A cross-domain invariant may require reservation, workflow, reconciliation, or compensating action. Do not weaken the logical rule to match one enforcement mechanism. Record the lag or risk and who may accept it.

**Design access and minimization logically.** Mark sensitivity, purpose, subject groups, jurisdictions, retention, deletion, aggregation, and allowed projections. A single wide logical record can create unnecessary access even if physical permissions later hide fields. Define minimum decision-specific projections and protected joins where consequence warrants.

**Plan versioning and compatibility.** Give every governed model and exchange schema stable identity and version semantics. Classify changes by backward/forward readability, semantic compatibility, constraint strengthening/weakening, data migration, defaulting, unknown-value behavior, and consumer use. Syntactic compatibility is not semantic compatibility.

Apache Avro's [specification](https://avro.apache.org/docs/current/specification/) defines primitive and complex schemas, names, aliases, defaults, and writer/reader schema resolution. Protocol Buffers' [proto3 guide](https://protobuf.dev/programming-guides/proto3/) documents field-number identity, reservation, unknown fields, and compatibility implications. These are concrete exchange technologies; their rules illustrate why logical identity and evolution must be explicit without making either the universal logical model.

Defaults deserve special care. A reader default can supply a value when an older writer lacks a field; it does not prove that value was true when the record was written. Distinguish assumed-for-reading, domain default, system-generated value, and unknown.

**Validate at several layers.** Check naming, unique identifiers, references, type expressions, key minimality, dependency implications, normal forms, cardinality satisfiability, subtype/variant coverage, temporal overlap, forbidden combinations, mapping coverage, schema fixtures, compatibility, and migration reversibility. Walk domain scenarios and counterexamples with authoritative stakeholders.

Generate positive, negative, boundary, historical, missing, conflicting, future-version, and adversarial instances. Test round trips and writer/reader pairs. A validator proves conformance only to the loaded schema and rule set; it cannot prove conceptual adequacy, source truth, complete constraints, or physical performance.

**Prepare for physical design without performing it.** Record workload and quality scenarios, volume/rate ranges, latency, concurrency, consistency, locality, retention, recovery, security, portability, and cost constraints as physical design inputs. Do not add indexes, partitions, vendor data types, compression, topic counts, or region placement to the logical baseline.

Maintain mappings from logical structures to each physical realization with transformation, enforcement allocation, exceptions, evidence, and reverse impact. Several physical models may realize one logical model, and one physical store may implement several logical projections.

## Definitions and Notation

Let a logical model be:

`L = (S, D, K, F, R, C, T, M, V)`

where `S` is structures, `D` value domains, `K` keys, `F` functional and other dependencies, `R` relationships/references, `C` constraints/derivations, `T` temporal and lifecycle semantics, `M` conceptual and cross-model mappings, and `V` versions and compatibility rules.

For relation schema `R(A1,...,An)`, a functional dependency `X -> Y` means that for every permitted instance `r(R)` and tuples `t1,t2` in `r`, `t1[X] = t2[X]` implies `t1[Y] = t2[Y]`. The premise excludes unspecified null semantics; if missing markers are allowed, define comparison and applicability before claiming the dependency.

For decomposition `R -> R1,...,Rn`, losslessness means the applicable join of projections reconstructs every permitted `R` instance without spurious information. This property depends on dependencies and join semantics; it does not prove that the original schema captured correct domain meaning.

A logical mapping is `m = (concept, structure, kind, condition, transform, cardinality, time, loss, authority, version, evidence)`. Coverage measures help find gaps, but one unmapped critical concept or one unjustified structure may outweigh many simple direct mappings.

## Mechanisms, Invariants, or Proof Structure

Use ten gates to construct and assure a logical data model.

**1. Purpose gate.** Bind decisions, competency questions, conceptual baseline, contexts, lifecycle, authority, evidence, and exclusions.

**2. Structure and grain gate.** Define each relation, record, document, graph, assertion, event, state, or projection by one-occurrence meaning.

**3. Type and field gate.** Specify semantic domains, grammar, units, scale, precision, allowed values, missingness, provenance, sensitivity, and derivation.

**4. Identity and key gate.** Establish candidate and reference keys, issuers, uniqueness scope, stability, reuse, correction, merge/split, and surrogate purpose.

**5. Relationship and dependency gate.** Model roles, arity, cardinality, optionality, references, lifecycle, functional dependencies, and anomaly conditions.

**6. Time and assertion gate.** Separate events, state, commands, valid/recorded time, history, provenance, conflict, correction, and retraction.

**7. Constraint and authority gate.** State permitted structures and transitions, enforcement allocation, consistency boundary, failures, exceptions, and evidence.

**8. Mapping and evolution gate.** Trace conceptual and cross-paradigm mappings, information loss, versions, writer/readers, defaults, migrations, and deprecation.

**9. Challenge gate.** Run structural checks, dependency analysis, scenario instances, counterexamples, compatibility matrices, round trips, and stakeholder review.

**10. Physical-handoff gate.** Preserve logical commitments and supply workload, quality, security, recovery, retention, portability, and cost constraints to physical design.

The executable example checks four frequent logical-model defects: missing business-key semantics, a repeating group, ambiguous null, and a numeric measure without a unit.

<!-- bijux-verify: {"id":"logical-model-integrity","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"items=4\nvalid=0\nfindings=customer:missing-business-key,order-line:repeating-group,order:ambiguous-null,price:missing-unit\nready=false\n","stderr":""}} -->
```python
items = (
    {"id": "customer", "business_key": "", "repeating": False, "nullable": False, "missing_reason": "n/a", "measure": False, "unit": "n/a"},
    {"id": "order-line", "business_key": "order+line", "repeating": True, "nullable": False, "missing_reason": "n/a", "measure": False, "unit": "n/a"},
    {"id": "order", "business_key": "order-number", "repeating": False, "nullable": True, "missing_reason": "", "measure": False, "unit": "n/a"},
    {"id": "price", "business_key": "offer+interval", "repeating": False, "nullable": False, "missing_reason": "n/a", "measure": True, "unit": ""},
)

findings = []
valid = 0
for item in items:
    local = []
    if not item["business_key"]:
        local.append("missing-business-key")
    if item["repeating"]:
        local.append("repeating-group")
    if item["nullable"] and not item["missing_reason"]:
        local.append("ambiguous-null")
    if item["measure"] and not item["unit"]:
        local.append("missing-unit")
    if local:
        findings.extend(f"{item['id']}:{finding}" for finding in local)
    else:
        valid += 1

print(f"items={len(items)}")
print(f"valid={valid}")
print(f"findings={','.join(sorted(findings))}")
print(f"ready={str(not findings).lower()}")
```

The checker validates four declared registry predicates. It does not prove business uniqueness, dependency truth, normalization, semantic correctness, complete missingness, enforcement, compatibility, or physical fitness. Those require domain rules, representative instances, formal analysis, consumer tests, and implementation evidence.

## Alternatives and Trade-Offs

**Relational versus document.** Relations make dependencies and joins explicit; documents preserve aggregates and nested exchange shapes. Documents can duplicate shared facts, while relations can distribute an aggregate across structures. Choose by semantics and contracts before physical performance.

**Graph versus tabular.** Graphs make varied relationship traversal direct; tabular models support well-understood relational constraints and set operations. Either can model connections, but identity, edge semantics, constraints, and mappings differ.

**Normalized authority versus denormalized projection.** Normalized structures reduce selected anomalies. Denormalized projections simplify bounded reads or exchange. Govern source, derivation, refresh, reconciliation, and consumer semantics.

**Natural versus surrogate keys.** Business keys communicate domain identity but can be mutable, composite, sensitive, or delayed. Surrogates simplify references but hide duplicates unless business rules remain enforced. Often both are required.

**Null versus explicit variants.** Null is compact and widely supported but conflates reasons and complicates logic. Variants or assertion structures preserve meaning but add complexity. Preserve distinctions that change decisions.

**Current state versus event history.** Current state supports immediate decisions; events support audit and reconstruction. Combining state projections with governed events often works, provided reducer versions, corrections, and reconciliation are explicit.

**Strict compatibility versus semantic correction.** Compatibility reduces disruption but can preserve harmful meaning. Breaking change may be necessary. Use coexistence, adapters, migration, consumer evidence, and explicit retirement.

## Failure Modes and Misconceptions

1. **Logical means a vendor-neutral ERD.** Logical paradigms include relations, documents, graphs, RDF, events, and messages with precise semantics.
2. **One concept becomes one record.** Identity, roles, events, assertions, and history often require several structures.
3. **Primary key means business identity.** A storage-friendly identifier may only distinguish records.
4. **Sample uniqueness proves a key.** Keys derive from domain rules and authority, then require evidence.
5. **Null means optional.** Missingness has several causes with different consequences.
6. **Normalization is automatic quality.** It depends on correct dependencies, losslessness, preservation, uses, and constraints.
7. **Nested means denormalized.** Nesting expresses ownership and grain; anomaly depends on duplicated authority and update semantics.
8. **Schema-valid means meaningful.** Syntax and encoded constraints do not prove source truth or conceptual adequacy.
9. **Backward readable means compatible.** Consumers may parse data while interpreting changed meaning incorrectly.
10. **Default means historical truth.** Reader substitution is not evidence about the writer's event.
11. **Events eliminate state.** Decisions often need governed projections and replay semantics.
12. **Logical models ignore operations.** They preserve physical choice but must expose workload, lifecycle, security, and recovery constraints for handoff.

## Worked Examples

### Example 1

A customer relation uses email as primary key. Email changes, can be shared, and is not issued by the organization. The model introduces governed Party identity, Contact Point assertions, validity, verification, and a surrogate reference while retaining applicable business uniqueness rules.

### Example 2

An invoice contains `item1`, `item2`, and `item3`. A fourth item requires a schema change, and item-level tax cannot be represented. Invoice Line becomes a repeating structure with `(invoice_id, line_number)` grain, Product Offer reference, quantity, price/tax assertions, and ordering semantics.

### Example 3

`closed_at = null` means open for new records, migrated without history for old records, and redacted for investigations. A status plus Closure Assertion with reason, source, valid and recorded time preserves the three cases and prevents “all null means active.”

### Example 4

A postal-code sample always determines city. Cross-country data and historical changes violate the dependency. The model scopes Postal Assignment by country, code authority, and valid interval rather than decomposing from a false global dependency.

### Example 5

A document embeds customer name in every order. Orders must preserve the contractual name at acceptance, while current contact corrections must propagate. The model distinguishes Order Party Snapshot from current Party Name Assertion, making intentional history separate from accidental duplication.

### Example 6

A graph edge `OWNS` connects people and accounts but lacks role, percentage, legal basis, and interval. Ownership Interest becomes an identified n-ary assertion with holder, asset, share, jurisdiction, agreement, source, and time. A graph realization may still encode it as a node or rich edge.

### Example 7

An event schema adds `country = "US"` as a reader default. Old records from Canada are silently misclassified. The model marks jurisdiction unknown for old writers, requires source evidence, and uses migration/enrichment rather than treating a compatibility default as fact.

### Example 8

Two normalized relations are losslessly decomposed but an exclusivity rule spans both and cannot be enforced locally. The model retains the rule, allocates coordinated workflow and reconciliation, and records the consistency delay instead of claiming full integrity from normal form.

### Example 9

An order-status event is replayed after a reducer change and produces a different current state. The model versions event semantics and reducer, records correction events, binds snapshots to versions, and tests rebuild equivalence before migration.

### Example 10

A physical warehouse star is presented as the enterprise logical model. Its customer dimension merges household, account, and person for one reporting use. The team preserves it as a derived analytical projection and restores mappings to bounded conceptual identities and authoritative logical structures.

## Cross-Program Connections

- **Database engineering:** relations, dependencies, keys, normal forms, constraints, transactions, temporal models, and indexes connect logical commitments to implementation.
- **Data structures:** records, trees, graphs, sets, maps, sequences, and algebraic variants provide representational choices with distinct invariants.
- **API and service engineering:** resources, messages, commands, events, compatibility, idempotency, and consumer contracts are logical information models at boundaries.
- **Data engineering:** source schemas, pipelines, event time, lineage, quality, projections, and lakehouse tables implement and test logical models.
- **Platform engineering:** schema registries, catalogs, policy engines, identity, tenancy, and paved-road tooling can enforce governed logical conventions.
- **Programming languages:** type systems, optional and union types, serialization, equality, and versioned code generation mirror logical-model choices.
- **Security and privacy:** minimization, purpose, identifiers, joins, missingness, provenance, retention, and deletion depend on logical structure.
- **Systems engineering:** information exchanges, interface contracts, state, scenarios, configuration, and lifecycle evidence bound model adequacy.

## References

1. Codd, E. F., “A Relational Model of Data for Large Shared Data Banks,” *Communications of the ACM*, 13(6), 1970. <https://doi.org/10.1145/362384.362685>
2. ISO/IEC, *9075-1:2023 Information technology—Database languages SQL—Part 1: Framework*, 2023. <https://www.iso.org/standard/76583.html>
3. W3C, *RDF 1.1 Concepts and Abstract Syntax*, Recommendation, 2014. <https://www.w3.org/TR/rdf11-concepts/>
4. JSON Schema, *Draft 2020-12 Specification*, 2022. <https://json-schema.org/draft/2020-12>
5. Object Management Group, *Unified Modeling Language 2.5.1*, 2017. <https://www.omg.org/spec/UML/>
6. Apache Software Foundation, *Apache Avro Specification*, current web edition. <https://avro.apache.org/docs/current/specification/>
7. Protocol Buffers, *Language Guide (proto3)*, current web edition. <https://protobuf.dev/programming-guides/proto3/>
8. W3C, *Shapes Constraint Language (SHACL)*, Recommendation, 2017. <https://www.w3.org/TR/shacl/>

## Exercises

### Exercise 1

Translate a conceptual order model into logical relational structures. Include Order, Party Role, Line, Product Offer, Price Assertion, Address/Delivery Destination, events, current state, keys, dependencies, references, missingness, time, and constraints without physical indexes or vendor types.

### Exercise 2

A relation `Enrollment(student_id, student_name, course_id, course_title, instructor_id, instructor_name, grade)` has proposed dependencies. State necessary scope assumptions, identify plausible candidate keys and dependencies, analyze anomalies, and propose a lossless decomposition without claiming the sample proves the rules.

### Exercise 3

Design a logical representation for phone contact that distinguishes unknown, not applicable, withheld, invalid, unverified, verified, revoked, and redacted states. Include value grammar, country context, owner, valid/recorded time, source, purpose, and history.

### Exercise 4

Evaluate a change that adds a required enum field with reader default `STANDARD` to a versioned event. Analyze syntactic readability, semantic compatibility, old data, unknown future values, producer rollout, consumers, replay, migration, and deprecation.

### Exercise 5

Review a logical model for clinical observations across relational storage, FHIR-like JSON exchange, and an RDF research projection. Specify conceptual mappings, identity, units, reference ranges, subject/specimen, time, provenance, missingness, constraints, information loss, access, versions, and validation evidence.

## Answers to the Exercises

### Answer 1

Define Order at one accepted commercial request per governed order identifier. Order Party Role relates Order, Party, role type, agreement, and interval. Order Line uses `(order_id, line_number)` as one candidate key and references Product Offer; quantity has unit. Price Assertion relates offer, amount, currency, tax basis, quantity band, market, and valid interval. Delivery Destination references a governed address assertion and serviceability decision rather than copying an unexplained string.

Order Event records submission, acceptance, rejection, amendment, cancellation, fulfillment, and correction with event identity, subject, occurred/recorded time, producer, cause, version, and idempotency. Current Order State is a versioned derivation with reconciliation. Define candidate/alternate/surrogate keys, role and line cardinalities, monetary invariants, event transition rules, missing-reason variants, provenance, valid time, retention, and conceptual mappings. Do not choose table indexes, partitions, engine types, or deployment.

### Answer 2

Possible rules are `(student_id, course_id) -> grade`, `student_id -> student_name`, `course_id -> course_title, instructor_id`, and `instructor_id -> instructor_name`, but course-to-one-instructor may fail for team teaching or term changes. The enrollment key likely also needs term or section; grades may have attempts or components. Validate identity, temporal scope, and authority before accepting dependencies.

Under the simplified rules, repeated names/titles create update anomalies, a course or student cannot be inserted without enrollment, and deleting the last enrollment can erase descriptive facts. A decomposition into Student, Instructor, CourseOffering, and Enrollment can be lossless when shared keys and dependencies satisfy the lossless-join test. Preserve `(student_id, offering_id)` or a richer enrollment key, references, and dependencies. Team teaching may require OfferingInstructor. The proposed result is conditional on rules, not inferred from the sample.

### Answer 3

Model Contact Point Assertion rather than one nullable phone field. It contains assertion ID, party or role, contact type, raw supplied value under protection, parsed country calling context and normalized value, source, purpose, valid and recorded intervals, verification state/evidence/time, authority, sensitivity, and lifecycle. Status is a controlled variant: unknown, not applicable, withheld, supplied-invalid, unverified, verified, revoked, or redacted, with allowed fields and transitions.

Unknown and withheld do not become empty strings; redaction preserves that a protected assertion exists without exposing it. Grammar and normalization depend on country/context and should not invent reachability. Retain assertion history and correction/revocation, define uniqueness only where authoritative, and restrict projections by purpose. Delivery success is separate empirical evidence from syntactic validity or verification.

### Answer 4

Old binary messages may be readable by a new consumer using a default, but `STANDARD` was never asserted by old producers. If the field changes routing, pricing, rights, or risk, substituting it is a semantic fabrication. New messages may be unreadable or misinterpreted by old consumers; future enum values need unknown handling rather than fallback to an unrelated member.

Define the field's meaning and authority, reserve an explicit `UNSPECIFIED` wire value if appropriate, and distinguish reader fallback from domain fact. Inventory producers/consumers, test every writer-reader pair, stage consumers before producers, monitor unknowns, bind replay to schema and reducer versions, backfill only from evidence, and maintain coexistence. Deprecate the old version after lag, archives, replay, rollback, and consumer evidence satisfy exit criteria.

### Answer 5

Begin with conceptual Observation, Subject, Specimen, Observable Property, Method, Result, Unit, Reference Range, Performer, Device, and Assertion/Correction. Define identity and version for observations and subjects, specimen linkage, status, valid/recorded times, method, provenance, uncertainty, missing reasons, and access purpose. Numeric results pair value with unit and conversion authority; reference ranges include population, method, unit, interval, and source.

Map to normalized relational structures, bounded JSON resources, and RDF classes/properties with typed, versioned mappings. Record nesting, code-system, blank-node/IRI, reference, decimal, ordering, and absent-field differences. State information lost by each projection and prohibit unsafe reverse inference. Validate schemas/shapes, keys, references, units, temporal and status rules, code mappings, round trips, future versions, negative fixtures, and access projections. Clinical and research adequacy still requires authorized domain, privacy, safety, and empirical review beyond structural conformance.
