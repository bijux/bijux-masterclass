---
module_id: DARCH-014
program: Data Architecture Engineering
level: 1
module_number: 14
title: Entities, Relationships, and Business Keys
status: complete
last_verified: 2026-09-03
---

# Entities, Relationships, and Business Keys

## One-Page Review

### Governing question

How can a team define stable entity identity, meaningful relationships, and governed business keys across time, systems, and organizations without confusing records, generated identifiers, similarity, or convenient storage references with the things the data claims to represent?

### Essential definitions

- An **entity** is a distinguishable thing, actor, place, event, agreement, role, or other subject about which the model makes governed assertions.
- **Identity criteria** are the domain conditions under which two observations refer to the same entity, different entities, or an unresolved match hypothesis.
- A **relationship** is a typed, directed or undirected association among two or more entity roles, with its own meaning, cardinality, time, authority, and possibly attributes or identity.
- A **business key** is a domain-recognized attribute or tuple used under stated rules to identify an entity within a defined scheme, issuer, namespace, scope, and time.
- A **candidate key** is any minimal attribute set that a declared rule makes unique for instances in a relation; a primary key is the candidate selected for a particular representation.
- A **surrogate key** is a system-assigned identifier that distinguishes records or model instances without, by itself, establishing real-world identity.
- An **identifier scheme** governs syntax, issuer authority, namespace, allocation, validation, uniqueness, reassignment, reuse, retirement, and resolution.
- An **identity assertion** records that an identifier, observation, or record refers to an entity, including source, method, evidence, confidence, time, and adjudication state.

### Central model, mechanism, or theorem

Represent an entity definition as:

`E = (type, identity_criterion, lifecycle, keys, relationships, authority, evidence)`

Represent a governed business key as:

`K = (scheme, issuer, namespace, components, canonicalization, uniqueness_scope, valid_time, reuse_rule, authority, evidence)`

A key is not merely a value. It is a governed claim that canonicalized components uniquely denote an entity within a declared boundary and interval. A UUID or sequence can make record identifiers practically distinct, but generated uniqueness does not prove that two records concern different real-world entities or that one record continues to denote the same entity after a merge, split, correction, or reassignment.

### Critical invariants

- Every entity type has explicit identity criteria, lifecycle boundaries, inclusion rules, and non-examples.
- Record identity, entity identity, business identity, and identity-resolution confidence remain separate claims.
- Every business key declares scheme, issuer, namespace, canonicalization, uniqueness scope, time, reuse/reassignment policy, and evidence.
- Candidate-key minimality and uniqueness are rules to establish and enforce, not conclusions drawn from a clean sample.
- Every relationship names its participant roles, meaning, arity, cardinality, optionality, validity, authority, and lifecycle behavior.
- Relationship attributes belong to the relationship or an association entity when they depend on the whole participant tuple.
- Cardinality and optionality are scoped to a population, state, and time; they are not timeless diagram decorations.
- Merges, splits, aliases, duplicates, corrections, and disputed matches preserve lineage and do not silently rewrite historical identity.
- Referential controls cover creation, change, absence, deletion, retirement, history, and cross-boundary reconciliation.
- Sensitive and predictable identifiers receive purpose, exposure, access, correlation, retention, and rotation analysis.

### Common failures

Common failures are treating a table row as the entity; using `id` without scheme or issuer; making a UUID the business identity; selecting a key because current data happens to be unique; omitting tenant, country, issuer, edition, or time from uniqueness scope; normalizing strings without domain authority; using a mutable email or phone number as permanent identity; reusing retired identifiers; collapsing person, account, customer, employee, and role; encoding an n-ary fact as unrelated binary links; attaching relationship attributes to one participant; drawing cardinalities without lifecycle scope; cascading deletion through required history; inferring equality from fuzzy similarity; joining sensitive identifiers for an undeclared purpose; and resolving duplicates by overwriting evidence.

### Compact example

A service uses email as `customer_id` and later introduces a UUID primary key. Neither choice settles customer identity. Email addresses change, may be shared, and are controlled by an external provider; UUIDs distinguish local records but allow duplicates. The model defines Party, Customer Role, Contact Point Assertion, and Account separately. A governed customer-number scheme names the issuer, tenant namespace, canonicalization, non-reuse rule, and validity. UUIDs remain internal record references. Potential duplicate parties produce match hypotheses with evidence and adjudication; approved merges preserve aliases and lineage. Orders reference the customer role that existed at acceptance, so later identity correction does not falsify history.

### Connections

[DARCH-011](011-conceptual-data-models.md) establishes bounded domain concepts, [DARCH-012](012-logical-data-models.md) formalizes technology-independent structure, and [DARCH-013](013-physical-models-and-their-separation.md) maps logical commitments to implementations. This module deepens identity, relationships, and keys before later modules address schemas, reference data, master data, interoperability, distribution, quality, migration, privacy, and governance.

## Governing Question

Data systems manipulate records, yet organizations make decisions about customers, products, contracts, shipments, accounts, locations, devices, claims, and events. Architecture must explain when records refer to the same subject, when apparently identical values concern different subjects, how subjects participate in relationships, and which identifiers are authoritative for which purposes.

The question has no universal answer such as “use UUIDs” or “prefer natural keys.” It requires a bounded identity criterion, lifecycle, authority, evidence, and consequences. A hospital patient number, tax identifier, device serial, product code, email, database sequence, and biometric match differ in issuer, population, stability, sensitivity, collision risk, reuse, and legal or operational meaning. Each can be useful while remaining unsafe as an unconditional identity claim.

Relationships make identity operational. An invoice belongs to a legal party in a buyer role, a device is installed at a site during an interval, and a person is authorized for an account under an agreement. If the model collapses role into entity, ignores time, or misplaces attributes, later joins and deletes change meaning. Correct entity and key definitions therefore precede physical foreign keys and integration matching.

## Why This Matters

Identity errors propagate broadly. Duplicate customers fragment service and consent. False merges expose one person's data to another. Reused asset numbers corrupt maintenance history. An omitted issuer joins unrelated identifiers. A many-to-many relationship forced into one foreign key loses facts. A cascade delete removes evidence that a historical agreement existed. A key change can break APIs, events, caches, warehouses, audits, and recovery.

Chen's [entity-relationship paper](https://doi.org/10.1145/320434.320440) proposed a modeling view centered on entities, relationships, and attributes. Codd's [relational-model paper](https://doi.org/10.1145/362384.362685) supplied a formal basis for relations and data independence. These foundations remain useful, but modern architectures cross services, organizations, graphs, event streams, probabilistic matching, privacy boundaries, and long-lived histories. The notation alone does not decide identity.

Identifier governance is an architectural concern. GS1's [identification-key overview](https://www.gs1.org/standards/id-keys) distinguishes keys for trade items, locations, logistic units, assets, service relationships, documents, consignments, shipments, and other subjects. The lesson is not that every domain should adopt GS1. It is that meaningful identifiers are coupled to what they identify and to allocation rules administered by an authority.

RFC 9562 defines [UUIDs](https://www.rfc-editor.org/rfc/rfc9562.html) and discusses generation, collision, uniqueness, and security considerations. A UUID can be an excellent distributed record identifier. It still says nothing by itself about whether a record denotes a person, a person's customer role, an account, a registration, or a possible duplicate. Architectural assurance keeps those layers separate.

## Prerequisites and Retrieval

You should understand conceptual and logical modeling, relations, attributes, tuples, sets, functions, constraints, events and state, temporal validity, provenance, APIs, distributed systems, security, privacy, and data quality.

Retrieve entity, entity type, instance, identity criterion, role, value object, event, assertion, aggregate, strong entity, weak entity, existence dependence, association entity, relationship, arity, participant, role name, cardinality, optionality, candidate key, superkey, primary key, alternate key, composite key, business key, natural key, surrogate key, external identifier, issuer, namespace, canonicalization, uniqueness scope, reassignment, reuse, alias, crosswalk, merge, split, match hypothesis, referential integrity, valid time, recorded time, and lineage.

As a retrieval test, inspect the value `123456789`. Ask what kind of thing it identifies, which scheme defines it, who issued it, which namespace and population it belongs to, how formatting and check digits work, when it is valid, whether it can be reused, whether it is sensitive, what evidence binds it to an entity, and what a match means. Until those questions are answered, it is a string of digits—not a defensible business key.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish entity identity from record identity, roles, observations, values, and match hypotheses;
2. define entity types with identity criteria, boundaries, lifecycle, authority, and evidence;
3. model binary, recursive, ternary, and higher-arity relationships with named roles and relationship attributes;
4. scope cardinality, optionality, and existence dependence by population, state, and time;
5. distinguish superkeys, candidate keys, primary and alternate keys, business keys, surrogates, and external identifiers;
6. specify identifier schemes with issuers, namespaces, canonicalization, allocation, validation, non-reuse or reassignment, and resolution;
7. analyze composite, mutable, delayed, sensitive, distributed, and only-probabilistically unique keys;
8. govern aliases, crosswalks, duplicate detection, match decisions, merges, splits, corrections, and historical lineage;
9. allocate referential creation, update, deletion, retirement, history, and reconciliation controls across system boundaries;
10. design identity and relationship changes with consumer impact, migration, rollback, evidence, and accountable approval.

## Core Exposition

**Begin with the subject, not the table.** Ask what decisions require the subject, what counts as one instance, what starts and ends its lifecycle, and which observations distinguish sameness from difference. A row may represent the subject, a version, a role, a snapshot, an event, an assertion, a relationship, or a processing artifact. Naming all of these `customer` creates ambiguity that no primary-key syntax can repair.

Define inclusion and exclusion. A Party may include people and organizations but exclude accounts. A Customer may be a role a Party plays under a commercial relationship, not a permanent subtype of person. A Product Model differs from a serialized Item. A Location differs from a postal address assertion. An Order differs from its current projection and its status-change events. These distinctions determine identity and lifecycle.

**Separate type identity from role identity.** The same person can be a customer, employee, guarantor, beneficiary, and authorized representative at different times. Roles commonly depend on another entity or agreement and have their own identifiers, states, permissions, and intervals. If `Person` contains one customer number and one employer, the model may incorrectly prohibit multiple roles or make role termination look like person deletion.

Model a role as a relationship or association entity when it needs attributes, history, or references. `AccountPartyRole(account, party, role_type, interval, authority)` can support multiple parties and roles without multiplying person records. A role identifier may be a valid business key for the participation while remaining invalid as a person identifier.

**Distinguish values, entities, events, and assertions.** A currency amount is usually a value determined by amount and currency; it does not need independent identity merely because it occupies a row. A Shipment is an entity with lifecycle. A Delivery Attempt is an event. “Device D was installed at Site S from t1” is an assertion or relationship instance with source and time. Give independent identity only when references, lifecycle, corrections, evidence, or competing assertions require it.

Value objects can be equal by their component values. Entities can remain the same while attributes change. Events are normally immutable occurrences, though assertions about them can be corrected. Assertions can conflict without implying that the underlying subject duplicated. Confusing these equality rules causes false deduplication or accidental proliferation.

**Define identity criteria explicitly.** Identity criteria describe the grounds for sameness, not merely available fields. For a legal organization, criteria may depend on jurisdiction, registration authority, organization form, and registration number during an interval. For a serialized asset, manufacturer scheme and serial assignment may be relevant, but refurbished or reserialized assets need policy. For a person, no single commonly collected attribute may be globally unique or stable.

Write positive and negative examples. Two customer accounts can belong to one person. Two people can share a household address and phone. One renamed organization can retain legal identity. A merger can end two legal entities and create another, or one entity can survive, depending on authoritative rules. A corrected birth date does not create a new person. Such cases expose whether criteria concern the domain or a current storage convention.

**Treat identity as time-dependent when the domain is.** An identifier can be valid only during an interval, an account can be transferred, a role can expire, and a registration can be reassigned under some schemes. Use valid time for when a claim applies in the domain and recorded time for when the system learned or stored it. Historical queries need the identity and relationship rules applicable to the questioned time, not only today's crosswalk.

Never reuse identifiers when the scheme prohibits it. When reuse is permitted, references need scheme, issuer, namespace, and relevant time to avoid joining different entities. Soft deletion does not make a key safely reusable. Archives, backups, messages, reports, and external consumers can preserve the old association long after an operational row disappears.

**Understand strong, weak, and dependent identity.** A strong entity can be identified without including another entity's key under the chosen model. A weak or identifying-dependent entity requires an owner or context. An invoice line numbered `4` is identified only within invoice `INV-27`; its key is `(invoice, line_number)`. A room number may require building. A version number requires the versioned object.

Existence dependence is related but not identical to key dependence. A payment instruction may have a globally assigned ID yet be prohibited from existing without an account. Conversely, a line may keep historical existence after its invoice is retired. Record identifying relationship, lifecycle dependence, creation rule, deletion behavior, and retention separately.

**Model relationships as domain facts.** A relationship has a verb-like meaning and named participant roles. `supplies` between Organization and Product is incomplete if the relevant fact is that a supplier offers a product to a buyer under a contract in a region and interval. Promote the association to `SupplyAgreementLine(supplier, buyer, product, agreement, region, interval, terms)` when the whole tuple determines facts.

Binary relationships connect two roles; recursive relationships connect instances of one type in distinct roles, such as parent organization and subsidiary. Ternary and higher-arity relationships connect several roles in one irreducible fact. Replacing a ternary relationship with three binaries can assert combinations that never existed. A clinician, patient, and treatment-plan authorization is not equivalent to independent clinician-patient, patient-plan, and clinician-plan links.

**Name relationship roles.** `Person relates_to Person` is ambiguous. `guardian` and `dependent`, `manager` and `report`, or `predecessor` and `successor` convey direction. For symmetric relationships such as siblinghood, state symmetry and whether self-relations are allowed. For transitive or acyclic relationships, state and enforce those properties only where the domain actually warrants them.

UML's [2.5.1 specification](https://www.omg.org/spec/UML/) supplies association, association-end, multiplicity, aggregation, and related modeling constructs. OWL 2's [structural specification](https://www.w3.org/TR/owl-syntax/) supplies formal key and property constructs under ontology semantics. They are useful modeling languages with different assumptions; neither notation substitutes for domain evidence, closed-world data constraints, operational enforcement, or lifecycle governance.

**Scope cardinality and optionality.** “One customer has many orders” hides at least four questions. Must every Order have exactly one buyer role at acceptance? Can a draft lack one temporarily? Can an order have multiple jointly liable buyers? Can one buyer place zero orders? Is the rule current-state, historical, per tenant, or per jurisdiction?

Specify minimum and maximum participation for each role, qualifying state, time, population, and enforcement point. Optionality can mean legitimately absent, not yet known, not applicable, withheld, redacted, or temporarily incomplete. These cases have different workflow and risk. Cardinalities often change across states: a draft can have zero lines, while an accepted order must have at least one.

**Place attributes at their determining grain.** If `ownership_percentage` depends on owner, asset, share class, and interval, it belongs to the ownership relationship. Putting it on Person implies one percentage for all assets; putting it on Asset implies one owner. If several sources can assert different percentages, add assertion identity, source, recorded time, confidence, and adjudication.

The same rule applies to price, membership status, authorization level, distance, sequence, and agreement terms. Ask which participant tuple and time determine the value. If the answer is the relationship, model it there. If the relationship requires references, lifecycle, or attributes, give it explicit identity without pretending it is a standalone physical object.

**Define superkeys, candidate keys, and selected keys.** A superkey is any attribute set whose declared rule uniquely identifies tuples in the scoped relation. A candidate key is a minimal superkey: removing any component loses the uniqueness guarantee. A relation can have several candidate keys. Selecting one as primary is a design decision; the others remain alternate keys whose business uniqueness may still require enforcement.

Minimality is semantic, not a performance preference. `(tenant_id, account_number, created_at)` is not a candidate key if `(tenant_id, account_number)` already identifies the account. Adding attributes can make samples look unique while concealing an incomplete identity rule. Conversely, dropping issuer, tenant, edition, jurisdiction, or time can create collisions that small fixtures do not reveal.

**Define business keys as governed schemes.** “Natural key” can misleadingly suggest that an identifier is intrinsic. Many business identifiers are issued artifacts: account numbers, registration numbers, catalog codes, tracking numbers, and document numbers. Record the scheme name and version, identified entity type, issuer and allocation authority, namespace, components and order, syntax, canonicalization, check mechanism, uniqueness scope, valid interval, reassignment/reuse rules, status, resolution method, evidence, and steward.

ISO/IEC 11179-3:2023 describes a [metamodel for registry common facilities](https://www.iso.org/standard/78915.html), including identification, designation, definition, classification, and registration concerns. ISO/IEC 9075-1:2023 provides the [SQL framework](https://www.iso.org/standard/76583.html) within which implementations define keys and referential constraints. Architecture uses these sources within their scope: metadata registry and SQL language standards do not decide the organization's domain identity criteria.

**Canonicalize without inventing identity.** Canonicalization maps accepted surface forms to a comparison form: removing permitted separators, normalizing case under a scheme, validating a check digit, or representing a component tuple consistently. Preserve raw supplied values when evidence or audit requires them. Apply scheme-specific rules before comparison.

Do not strip punctuation, accents, leading zeros, or whitespace universally. `0012` and `12` may be different product codes; case may matter; Unicode normalization may alter legacy identifiers; a display formatter may not define equality. Canonicalization can find equivalent encodings of the same issued identifier. It cannot prove that two different identifiers name the same entity.

**Use surrogate keys for the right job.** Sequences, UUIDs, and other opaque IDs make references compact, stable, and locally manageable. They help create records before an external business identifier exists and decouple physical relationships from mutable business attributes. They should normally be meaningless outside their governed system boundary.

RFC 9562 notes UUID variants and practical uniqueness considerations, including that absolute global uniqueness cannot be guaranteed without shared knowledge. Choose version and generation controls for ordering, privacy, collision, and security needs. Still enforce applicable business keys. If duplicate Party records each receive a unique UUID, the database has unique records and unresolved entity identity.

Avoid exposing sequential identifiers where enumeration reveals volume or enables unauthorized access. Randomness does not grant authorization. Time-ordered identifiers can leak creation time. Identifiers embedded in logs, URLs, analytics, and support tools become correlators. Treat design, access, observability, and retention together.

**Handle mutable and delayed keys.** Some business identifiers arrive after entity creation; others can be corrected or legitimately change. Give the entity a stable internal reference, represent the business identifier as a versioned assertion, enforce one current association where applicable, and preserve prior aliases with validity and reason.

A mutable key in an API path, event partition, warehouse dimension, or foreign-key network has large migration cost. Use explicit redirects, alias resolution, consumer compatibility, replay handling, and retirement. Never update history merely to make old records display the current identifier unless the use explicitly requests a current-state projection.

**Govern crosswalks and aliases.** A crosswalk maps identifiers across schemes or systems. Each mapping needs source and target scheme, entity type, direction, relationship kind, validity, source, evidence, method, confidence or decision status, approver, and history. “Same as” is too strong when the mapping means successor, replacement, household member, duplicate candidate, or product-equivalent-for-one-use.

Crosswalks can be one-to-one, one-to-many, many-to-one, or time-dependent. A source system may split one record into two; two records may merge into one master; a product code may represent a pack while another represents an item. State allowed multiplicity and information loss. Reconciliation should surface orphaned, ambiguous, contradictory, expired, and cyclic mappings.

**Treat entity resolution as evidence-based decision-making.** Probabilistic or rule-based matching proposes that observations refer to the same entity. It does not discover a metaphysical key. Record compared features, normalization, model/rule version, score and calibration, thresholds, blocking strategy, source quality, missingness, decision, reviewer where required, and consequences.

False merges and false splits have asymmetric harm. Set thresholds by use: marketing deduplication, fraud investigation, clinical treatment, access control, and regulatory reporting cannot share one unexamined threshold. Protected or proxy attributes can create disparate error. Samples need representative populations, temporal drift, adversarial cases, and privacy authorization.

Keep match hypotheses separate from approved identity assertions. A likely match may support a queue without granting account access or combining records. For high-impact actions, require stronger evidence, human adjudication, or authoritative verification. Preserve negative decisions and reasons enough to avoid endless rematching while respecting retention limits.

**Design merges and splits as governed events.** A merge does not simply delete the losing record. Record surviving or newly created entity identity, source identities, effective and recorded time, reason, evidence, authority, attribute-resolution decisions, affected relationships, aliases, downstream propagation, rollback conditions, and audit. Prevent old identifiers from being reassigned.

A split reverses an over-merged identity or represents a real domain division. Allocate assertions, roles, events, relationships, permissions, and history to resulting entities with provenance. Some facts remain ambiguous and should not be guessed. Downstream systems need versioned change events and reconciliation rather than a silent rewrite.

Legal merger, data-record consolidation, household change, and account linking are different operations. Name the event precisely. A legal entity can merge while customer accounts stay separate; duplicate records can consolidate while the represented person remains one continuous entity.

**Allocate referential integrity through lifecycle.** A foreign key checks one physical reference under a database's semantics. Architectural referential integrity also covers entity existence, type, state, role, time, tenant, authorization, version, and authority. A reference valid today may not have been valid when an event occurred.

For every relationship define creation prerequisites, atomicity boundary, deferred or immediate validation, update rules, delete/retire behavior, history, orphan policy, retries, idempotency, bulk-load bypass, cross-service failure, reconciliation, monitoring, remediation, and exception authority. Restrict, cascade, nullify, tombstone, archive, and retain are business choices, not universal defaults.

Cross-system references may use reservations, synchronous checks, replicated registries, signed assertions, asynchronous reconciliation, or compensating workflow. State consistency delay and decision consequence. Never claim a global uniqueness or referential rule when enforcement exists only per shard, tenant, region, or service unless that boundary is the declared scope.

**Preserve grain in composite keys.** Composite keys often express identity honestly. `(invoice_id, line_number)` identifies a line within an invoice; `(scheme, issuer, value, valid_from)` may distinguish reused identifiers; `(sensor_id, observed_at, sequence)` may distinguish observations under declared device rules. Flattening these into a hash or surrogate can ease references but must not erase the governed uniqueness rule.

Composite width can affect APIs, messages, storage, and joins, but physical inconvenience is not evidence that components are unnecessary. Use a surrogate for transport or implementation while retaining a uniqueness constraint and mapping. Conversely, do not retain accidental source-row components in a business key merely because they are available.

**Protect identifier data.** Identifiers can be personal, confidential, commercially sensitive, or linkable even when they contain no descriptive attributes. A stable pseudonym across contexts enables correlation. Hashing a low-entropy identifier without a secret can be reversible by enumeration. Tokenization, keyed transforms, scoped pseudonyms, encryption, and access controls have different threat and resolution properties.

Minimize identifier propagation. Define purposes, audiences, contexts, logs, telemetry, test fixtures, URLs, exports, caches, backups, retention, breach response, and subject-right processes where applicable. Use separate pairwise or context-specific identifiers when cross-context linkage is unnecessary. Security and privacy review must consider the issuer, resolver, mapping store, and people able to join namespaces.

**Design distributed uniqueness deliberately.** A central allocator can enforce a sequence but adds dependency and availability concerns. Partitioned allocation can combine issuer and local number. UUIDs or sufficiently random identifiers reduce coordination but retain collision handling and do not enforce business uniqueness. Time-based schemes need clock, node, rollback, predictability, and ordering analysis.

Write the true guarantee: unique per tenant, unique per issuer, collision probability under assumptions, centrally checked before acceptance, or eventually detected and reconciled. Define behavior on collision, network partition, retry, restoration, and concurrent creation. Backup restoration into a live namespace can duplicate sequences even when normal allocation was safe.

**Separate identifier validation from entity verification.** Syntax, length, character set, and check digit can show that a value is well-formed. Registry lookup can show it was allocated. Neither necessarily proves that the presenter controls it, that it currently belongs to the claimed entity, or that the entity is trustworthy. Record each evidence level and its freshness.

Verification can depend on authoritative lookup, credentials, documents, possession, attestation, or human review. Define failure and unavailable behavior. Caching a successful lookup requires validity and revocation rules. Avoid turning temporary resolver failure into either permanent rejection or blind acceptance without explicit risk policy.

**Version identity rules and schemas.** Entity boundaries, issuer policy, normalization, allowed key components, and matching models change. Version the rule set, effective time, owner, rationale, compatibility, migration, and affected consumers. Retain enough earlier semantics to interpret historical records and replay events.

An identity-rule change can be more disruptive than a field addition. Adding issuer to a formerly global-looking identifier changes keys, URLs, joins, events, permissions, deduplication, caches, and reports. Plan coexistence, mapping, backfill, ambiguity handling, cutover, rollback, reconciliation, and retirement. Do not fabricate missing issuer values to make migration pass.

**Govern with evidence.** Maintain entity and relationship definitions, identifier-scheme registry, key inventory, crosswalk ownership, uniqueness and orphan metrics, match-quality evidence, merge/split log, exception register, consumer map, and lifecycle tests. Every control should name owner, implementation, bypasses, measurement, threshold, response, and review trigger.

Evidence includes domain decisions, issuer specifications, profiling across relevant populations, constraint results, negative fixtures, concurrency tests, collision exercises, resolver behavior, migration rehearsals, consumer tests, privacy/security assessment, and production observations. Profiling can refute a proposed key; it cannot prove a timeless business rule.

## Definitions and Notation

Let an entity definition be:

`E = (T, I, L, K, R, A, V)`

where `T` is entity type and boundary, `I` identity criteria, `L` lifecycle, `K` governed keys, `R` permitted relationships and roles, `A` authority, and `V` evidence and versions.

Let a business-key definition be:

`K = (S, U, N, C, F, Q, W, X, A, V)`

where `S` is scheme, `U` issuer, `N` namespace, `C` ordered components, `F` canonicalization and validation, `Q` uniqueness scope, `W` valid-time rule, `X` reuse/reassignment rule, `A` authority, and `V` evidence/version. A key value without these coordinates is underspecified.

For relation `r` with attribute set `H`, attribute set `X` is a superkey when the declared constraints imply that no two distinct tuples in the scoped relation agree on `X`. It is a candidate key when it is a superkey and no proper subset is a superkey. This is conditional on the declared population, time, and rule set; finite sample uniqueness is insufficient.

Represent a relationship instance as:

`R = (type, participants_by_role, attributes, valid_time, recorded_time, authority, evidence, lifecycle)`

The relationship's grain is the smallest participant-role tuple plus temporal or version coordinates that distinguishes one governed relationship assertion. Its key can be composite, externally issued, or surrogate-backed, but its semantic uniqueness remains explicit.

An identity-resolution assertion can be represented as:

`M = (observations, proposition, method_version, evidence, score, decision, authority, valid_time, recorded_time)`

where `proposition` might be same-entity, different-entity, successor, alias, or unresolved. A score is not a decision, and a decision for one permitted use is not automatically valid for another.

## Mechanisms, Invariants, or Proof Structure

Use ten gates to design and assure entities, relationships, and keys.

**1. Scope gate.** Name the domain, population, jurisdictions, tenants, decisions, consumers, time horizon, and consequences. Reject unqualified claims of global identity or uniqueness.

**2. Entity gate.** Define subject, type, inclusion, exclusion, identity criteria, lifecycle, roles, values, events, assertions, examples, and counterexamples.

**3. Key gate.** Register scheme, issuer, namespace, components, canonicalization, allocation, validation, uniqueness scope, validity, reuse, resolution, sensitivity, authority, and evidence.

**4. Relationship gate.** Define type, arity, participant roles, grain, attributes, cardinality, optionality, symmetry/order, temporal scope, and relationship identity.

**5. Lifecycle gate.** Cover creation, activation, change, suspension, retirement, deletion, history, valid and recorded time, identifier reassignment, and dependent-entity behavior.

**6. Authority and evidence gate.** Separate supplied, syntactically valid, allocated, verified, matched, adjudicated, and authoritative claims; version sources and decisions.

**7. Challenge gate.** Test duplicates, collisions, shared values, mutable values, missing issuers, reused numbers, aliases, false merges, false splits, adversarial inputs, and inaccessible authorities.

**8. Mapping and distribution gate.** Trace aliases, crosswalks, systems, services, shards, regions, caches, events, histories, enforcement scope, reconciliation, and recovery behavior.

**9. Protection gate.** Analyze purpose, exposure, enumeration, predictability, correlation, authorization, cryptography, logs, retention, deletion, and incident consequences.

**10. Governance and change gate.** Assign owners, approvals, metrics, exceptions, consumer impact, compatibility, migration, rollback, reconciliation, and retirement evidence.

The executable example checks four narrow registry failures: a surrogate treated as business identity, a business key without issuer, a relationship without temporal scope, and an identifier scheme that permits reuse despite a required non-reuse predicate.

<!-- bijux-verify: {"id":"entity-key-integrity","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"items=4\nvalid=0\nfindings=customer:surrogate-as-identity,membership:missing-issuer,ownership:missing-time,shipment:reusable-key\nready=false\n","stderr":""}} -->
```python
items = (
    {"id": "customer", "uses_surrogate_as_identity": True, "issuer": "crm", "temporal": True, "reuse_prohibited": True},
    {"id": "membership", "uses_surrogate_as_identity": False, "issuer": "", "temporal": True, "reuse_prohibited": True},
    {"id": "ownership", "uses_surrogate_as_identity": False, "issuer": "registry", "temporal": False, "reuse_prohibited": True},
    {"id": "shipment", "uses_surrogate_as_identity": False, "issuer": "carrier", "temporal": True, "reuse_prohibited": False},
)

findings = []
valid = 0
for item in items:
    local = []
    if item["uses_surrogate_as_identity"]:
        local.append("surrogate-as-identity")
    if not item["issuer"]:
        local.append("missing-issuer")
    if not item["temporal"]:
        local.append("missing-time")
    if not item["reuse_prohibited"]:
        local.append("reusable-key")
    if local:
        findings.extend(f"{item['id']}:{finding}" for finding in local)
    else:
        valid += 1

print(f"items={len(items)}")
print(f"valid={valid}")
print("findings=" + ",".join(sorted(findings)))
print(f"ready={str(valid == len(items)).lower()}")
```

The checker validates four declared registry predicates only. It does not prove entity boundaries, real-world uniqueness, key allocation, relationship truth, temporal correctness, issuer authority, non-reuse in production, privacy, security, probabilistic match quality, referential enforcement, or migration fitness. Those require authoritative rules, representative data, implementation tests, operational evidence, and accountable review.

## Alternatives and Trade-Offs

**Business key versus surrogate key.** Business keys expose domain identity and support exchange but may be composite, mutable, delayed, sensitive, or externally governed. Surrogates simplify internal references and change but do not prevent business duplicates. Many sound designs use both and govern their mapping.

**Central allocation versus decentralized generation.** A central allocator can enforce one namespace and sequential policy but creates coordination and dependency. Decentralized UUID or partitioned generation improves autonomy but shifts assurance to collision assumptions, issuer composition, reconciliation, and business-key enforcement.

**Composite key versus opaque reference.** Composite keys preserve scope and grain visibly but increase payload and migration surface. Opaque references simplify transport but can hide missing issuer or context. Retain semantic uniqueness even when an opaque implementation key is selected.

**Relationship versus association entity.** A simple relationship is compact when it has no independent attributes, references, or lifecycle. An association entity supports terms, provenance, time, status, and identity but adds modeling and operational structure. Choose according to the fact's grain.

**Deterministic versus probabilistic resolution.** An authoritative identifier can support deterministic matching under its scheme. Probabilistic matching handles incomplete observations but introduces thresholds, bias, uncertainty, and adjudication. Do not turn a probabilistic score into an unconditional key.

**Global master identity versus bounded identities.** One enterprise identifier can simplify integration but centralizes authority and creates broad correlation and blast radius. Bounded identities respect context and autonomy but require governed crosswalks. Use the least expansive identity necessary for decisions.

**Hard delete versus retained tombstone.** Hard deletion minimizes retained data but may allow reuse, dangling references, or lost audit. Tombstones preserve non-reuse and lineage but carry retention and privacy costs. Define legal, safety, historical, and operational obligations with authorized reviewers.

**Immediate versus eventual cross-boundary integrity.** Synchronous validation gives stronger decision-time assurance but couples availability and latency. Asynchronous reconciliation preserves autonomy but permits temporary orphan, duplicate, or stale states. State the consequence and remediation window.

## Failure Modes and Misconceptions

1. **Every noun is an entity.** Some nouns are values, roles, events, assertions, projections, or attributes; independent identity requires a reason.
2. **One row equals one real thing.** Rows can be duplicates, versions, observations, relationships, snapshots, or processing artifacts.
3. **A UUID solves identity.** It distinguishes generated values under assumptions; it does not resolve domain sameness.
4. **The primary key is the business key.** Primary-key selection is representational; alternate business uniqueness still needs governance and enforcement.
5. **Unique in the sample means a key.** Profiling can find violations but cannot establish a universal domain rule.
6. **Natural means immutable.** Most business identifiers are issued and can be corrected, retired, reassigned, or scoped.
7. **A string is globally unique.** Uniqueness requires scheme, issuer, namespace, population, canonicalization, and time.
8. **Every relationship is binary.** Decomposing an irreducible n-ary fact can invent combinations and misplace attributes.
9. **Cardinality never changes.** Minimum and maximum participation often depend on lifecycle state and time.
10. **Cascade delete is referential correctness.** It may destroy required history or propagate an erroneous identity decision.
11. **A match score is an identity decision.** Scores require calibration, threshold, use, evidence, authority, and consequence analysis.
12. **Merging means deleting a duplicate.** Safe consolidation preserves lineage, aliases, decisions, relationships, propagation, and reversal paths.
13. **Hashed identifiers are anonymous.** Stable or low-entropy hashes can remain linkable or enumerable.
14. **Local uniqueness is global uniqueness.** Shard, tenant, service, region, and issuer boundaries must match the declared guarantee.
15. **Well-formed means verified.** Syntax and check digits do not prove allocation, control, current association, or trustworthiness.

## Worked Examples

### Example 1

A CRM gives each row a UUID and reports zero duplicate IDs. Two imports create separate rows for the same organization. The model keeps UUID as record identity, defines Legal Organization identity by authoritative jurisdictional registration, represents uncertain matches separately, and enforces applicable registration keys without claiming universal global coverage.

### Example 2

A university treats email as Student identity. Alumni lose addresses, people change names, and applicants can share family mailboxes. The university issues a non-reused student number within its namespace, stores email as a versioned Contact Point Assertion, and keeps Application, Enrollment, and Student Role identities separate from Person.

### Example 3

Warehouse bin `A-17` is unique in one building but collides in another. The business key becomes `(facility_identifier, bin_code)` under the facility operator's scheme. A surrogate bin ID supports internal references, while moves and facility renaming preserve historical location assignments and valid intervals.

### Example 4

An ownership table stores `person_id`, `asset_id`, and `percentage` without time. It cannot represent changing shares, classes, legal basis, or competing sources. Ownership Interest becomes an association entity keyed by governed participants, class, basis, and interval, with assertion source, recorded time, and adjudication status.

### Example 5

A shipment number can be reused by different carriers. Joining on the visible number merges unrelated histories. The integration uses `(carrier_scheme, carrier_issuer, shipment_number, applicable_interval)` and retains raw formatting, canonical form, source evidence, and carrier-specific reuse rules.

### Example 6

A graph models a clinician, patient, and care plan as three pairwise edges. It then infers that every clinician connected to the patient is authorized for every plan. A ternary Plan Authorization relationship records clinician role, patient, plan, purpose, scope, issuer, and validity, preventing invented combinations.

### Example 7

A matching model assigns 0.91 probability that two customer records concern the same person. Marketing accepts matches above 0.85, but account recovery demands authoritative verification. The architecture stores one hypothesis and separate purpose-bounded decisions; it does not merge security credentials from the marketing threshold.

### Example 8

Two accounts were wrongly merged. The split process restores source record identities, reallocates contact and consent assertions by evidence, marks disputed transactions unresolved, rotates affected access credentials, emits versioned corrections, and reconciles downstream caches and warehouses without fabricating certainty.

### Example 9

A tenant-local database enforces unique `invoice_number`, but a reporting lake joins numbers across tenants. The key registry states uniqueness per issuing tenant and fiscal series. Exchange records carry tenant issuer, series, number, and issue date; a generated warehouse key remains only a projection reference.

### Example 10

A device serial passes length and check-digit validation, so a service treats the caller as device owner. The model separates syntactic validity, manufacturer allocation, physical possession, ownership relationship, and authorization. Ownership requires its own evidence and interval; identifier knowledge alone grants no access.

## Cross-Program Connections

- **Database engineering:** keys, uniqueness, referential constraints, transactions, temporal relations, and indexes implement bounded portions of identity governance.
- **Data structures:** sets, maps, graphs, tuples, disjoint-set structures, indexes, and probabilistic filters support identity and relationship operations with different guarantees.
- **API and service engineering:** resource identifiers, URLs, idempotency keys, tokens, events, aliases, and versioning expose identity decisions across boundaries.
- **Data engineering:** ingestion keys, deduplication, slowly changing dimensions, entity resolution, lineage, late data, and reconciliation depend on explicit identity semantics.
- **Platform engineering:** identity registries, schema services, tenancy, policy engines, secrets, observability, and paved-road libraries can enforce scheme and exposure rules.
- **Security engineering:** authentication subjects, principals, credentials, authorization relationships, enumeration resistance, and correlation limits require layered identity.
- **Privacy engineering:** linkability, pseudonymization, purpose limitation, minimization, retention, access, correction, and deletion are shaped by identifier design.
- **Systems engineering:** system boundaries, interface items, configuration identity, traceability, lifecycle, authority, and change control parallel entity and relationship assurance.

## References

1. Chen, P. P., “The Entity-Relationship Model—Toward a Unified View of Data,” *ACM Transactions on Database Systems*, 1(1), 1976. <https://doi.org/10.1145/320434.320440>
2. Codd, E. F., “A Relational Model of Data for Large Shared Data Banks,” *Communications of the ACM*, 13(6), 1970. <https://doi.org/10.1145/362384.362685>
3. ISO/IEC, *11179-3:2023 Information technology—Metadata registries—Part 3: Metamodel for registry common facilities*, 2023. <https://www.iso.org/standard/78915.html>
4. ISO/IEC, *9075-1:2023 Information technology—Database languages SQL—Part 1: Framework*, 2023. <https://www.iso.org/standard/76583.html>
5. GS1, *GS1 Identification Keys*, current web edition. <https://www.gs1.org/standards/id-keys>
6. Davis, K., Peabody, B., and Leach, P., *RFC 9562: Universally Unique IDentifiers (UUIDs)*, IETF, 2024. <https://www.rfc-editor.org/rfc/rfc9562.html>
7. W3C, *OWL 2 Web Ontology Language Structural Specification and Functional-Style Syntax*, Second Edition, 2012. <https://www.w3.org/TR/owl-syntax/>
8. Object Management Group, *Unified Modeling Language 2.5.1*, 2017. <https://www.omg.org/spec/UML/>

## Exercises

### Exercise 1

Design entity and identity definitions for a marketplace containing people, organizations, seller accounts, storefronts, product offers, orders, and shipments. State roles, lifecycles, business and surrogate keys, issuer namespaces, relationship grain, cardinality by state, and non-examples.

### Exercise 2

A data sample contains 10 million membership rows. `email` is unique, `member_number` is unique within each club, and a generated UUID is globally distinct in the sample. Evaluate proposed keys, identify what evidence and scope are missing, and design a governed membership identity that supports email change and club merger.

### Exercise 3

Model a property ownership relationship among party, property, ownership class, jurisdiction, instrument, percentage, and time. Explain why independent binary links are insufficient, identify candidate keys, and define history, corrections, and referential lifecycle behavior.

### Exercise 4

Design a cross-system entity-resolution workflow for customer records. Include observations, features, normalization, deterministic rules, probabilistic score, thresholds by use, evidence, adjudication, merge and split events, aliases, security/privacy boundaries, monitoring, and rollback.

### Exercise 5

Review a proposal to expose sequential database IDs in API URLs, replace all business keys with UUIDv7, and remove alternate uniqueness constraints. Analyze record identity, business identity, distributed generation, enumeration and time leakage, duplicate creation, compatibility, migration, and evidence.

## Answers to the Exercises

### Answer 1

Define Person and Legal Organization as Party kinds with distinct authoritative identity criteria. Seller Account is an account entity issued by the marketplace and held by one or more Parties through time-bounded Account Party Roles. Storefront is a published commercial presence operated by a Seller Account; it is not the same as the legal organization. Product Offer relates seller account, offered product, market, terms, currency, and valid interval. Order records an accepted commercial request; Shipment records a carrier movement obligation or execution, not merely an order status.

Use marketplace-issued non-reused account, storefront, and order numbers with issuer and tenant or marketplace namespace. Keep stable internal surrogates for references. External party registrations and carrier shipment keys remain scheme-qualified assertions. Product offers may use `(seller_account, seller_sku, market, valid_from)` if issuer rules establish that grain. State draft versus active cardinalities: a draft offer can lack approval, while an active offer requires seller, product, price terms, market, and interval. One order can have several shipments; one shipment can fulfill lines from several orders only if the business process allows it. Preserve roles and history when a person leaves an organization or an account changes operators.

### Answer 2

The sample proves only observed distinctness after the sample's current normalization. Email is externally controlled, mutable, sometimes shared, sensitive, and not necessarily unique beyond the dataset. `member_number` is promising only as `(club_issuer, member_number)` under allocation and non-reuse rules. The UUID can identify rows under its generation history but does not prove membership or person identity.

Define Membership as a relationship or association entity between Club and Party with status and valid interval. Register the member-number scheme: issuing club, namespace, syntax, canonicalization, allocation, uniqueness per club, validity, reuse, aliases, and evidence. Use a stable internal membership ID while enforcing the current business key. Represent email separately as a contact assertion. For a club merger, decide whether old memberships continue, terminate, or map to new memberships; preserve old qualified numbers as aliases, prevent unsafe reassignment, communicate versioned mappings, and reconcile consumers. Do not collapse Party identity merely because two memberships share an email.

### Answer 3

Model Ownership Interest as an association entity with owner Party role, owned Property role, ownership class, jurisdiction, governing Instrument, percentage or interest form, valid interval, recorded interval, source assertion, authority, and adjudication state. Three independent links—Party to Property, Party to Instrument, and Instrument to Property—can combine facts that were never asserted and cannot place percentage or class at the correct grain.

A candidate business key might include property registry identifier, owner identifier under accepted scheme, ownership class, instrument identifier, and effective start, but only authoritative registry rules can establish minimality and correction behavior. A surrogate can support references. New instruments create or amend interests; corrections preserve prior recorded assertions. Restrict deletion of referenced authoritative parties or properties, allow retirement while retaining historical relationships, handle unknown or disputed owners explicitly, and reconcile percentages within the exact class and interval without assuming every jurisdiction requires totals of 100 percent.

### Answer 4

Ingest source records as immutable or versioned observations with source record identity, provenance, valid/recorded time, and permitted purpose. Normalize each feature under a field-specific rule while preserving raw evidence. Apply authoritative exact identifiers only within their schemes; use blocking rules to form candidates and a versioned model to produce calibrated scores. Record missingness and source reliability.

Set decision thresholds and review requirements by consequence. A marketing suppression decision may tolerate different error from credential linking, payment, or safety action. Keep hypotheses separate from approved same-entity assertions. An adjudicated merge records survivor or new identity, aliases, attribute and relationship resolution, authority, propagation, and rollback. A split reallocates assertions only with evidence and flags ambiguity. Restrict access to raw identifiers and crosswalks, assess proxy bias and linkability, monitor false merges/splits and drift, test adversarial cases, emit versioned changes, and reconcile downstream systems. Rollback restores identity assertions and access boundaries rather than merely undeleting rows.

### Answer 5

Sequential IDs provide simple internal references but expose order and approximate volume and can support enumeration when authorization is weak. Authorization must never depend on identifier obscurity. UUIDv7 can improve decentralized generation and approximate time ordering, but time ordering itself leaks timing and does not establish business identity. Collision and generation controls still need evidence.

Removing alternate uniqueness constraints allows multiple records for the same governed account, registration, or order even though every UUID remains unique. Retain registered business keys and their qualified uniqueness, with surrogates as implementation references. Inventory all URLs, events, foreign references, caches, warehouses, logs, and external contracts before changing identifiers. If public opaque IDs are needed, define a stable scoped scheme, authorization, rotation or alias policy, and error behavior. Migrate through coexistence and mappings, detect ambiguous duplicates before cutover, test retries and restoration, preserve rollback, and verify consumers. Neither UUID adoption nor successful schema migration proves corrected domain identity.
