---
module_id: DARCH-020
program: Data Architecture Engineering
level: 1
module_number: 20
title: Reconciling Conflicting Models Across Systems
status: complete
last_verified: 2026-09-03
---

# Reconciling Conflicting Models Across Systems

## One-Page Review

### Governing question

How can an organization integrate systems whose identities, concepts, structures, grains, codes, units, time semantics, constraints, authorities, and protections disagree without disguising loss, manufacturing equivalence, or destroying legitimate local meaning?

### Essential definitions

- A **model perspective** is a system's bounded interpretation of domain objects, concepts, facts, rules, and responsibilities for a declared use.
- A **model conflict** exists when two perspectives cannot both be applied as if they made the same assertion under the same identity, context, time, and authority.
- A **correspondence** states a reviewed relationship between source and target elements or concepts, such as exact, close, broader, narrower, related, conditional, disjoint, or unmapped.
- A **mapping rule** is an executable or declarative transformation from a source version and context to a target version and context, including preconditions and loss.
- **Reconciliation** is the governed process of preserving, relating, translating, selecting, combining, or escalating differing assertions so a specific decision can proceed with traceable limitations.
- A **survivorship rule** chooses or composes assertions for a purpose; it does not establish universal truth.
- A **crosswalk** is a versioned set of correspondences among identifiers, concepts, codes, or fields.
- **Grain** is what one record or assertion represents. Grain mismatch occurs when records aggregate, split, or scope the domain differently.
- **Semantic loss** is information, distinction, evidence, or uncertainty that a mapping cannot preserve in its target representation.
- An **unresolved conflict** is a first-class result requiring quarantine, multiple presentation, human adjudication, or a bounded fallback—not an integration defect to hide.

### Central model, mechanism, or theorem

Represent a model assertion as:

`A = (model_version, subject, predicate, value, identity, grain, context, valid_time, recorded_time, authority, provenance, protection)`

Represent a reconciliation rule as:

`R = (source_version, target_version, relation, precondition, transform, loss, inverse, authority, effective_time, evidence)`

Two fields with the same label are not equivalent unless their subjects, predicates, value domains, identity, grain, context, time, authority, and protection align for the intended use. Reconciliation is therefore a typed, directional, versioned, evidence-backed relation—not a column rename or winner-takes-all merge.

### Critical invariants

- Source assertions remain attributable to exact system, model, version, authority, and time; reconciliation never erases their provenance.
- Lexical similarity never establishes conceptual identity, and different labels do not establish conceptual difference.
- Every mapping declares direction, relation type, preconditions, cardinality, versions, context, loss, reversibility, authority, and evidence.
- Identity mappings distinguish same entity, possible match, related entity, household, account, role, and record linkage.
- Grain, units, reference systems, precision, cardinality, absence, defaults, code versions, and temporal semantics are reconciled explicitly.
- Conflicting authoritative assertions can coexist; a purpose-specific view records selection or composition policy rather than rewriting sources.
- Exact, close, broader, narrower, related, conditional, disjoint, and unmapped correspondences remain distinct and are not assumed transitive.
- Transformations preserve unmapped values, failures, uncertainty, and loss as observable outcomes.
- Security classification, purpose, consent, residency, retention, and access obligations survive mappings and derived combinations.
- Reconciliation is tested on boundary, contradictory, missing, duplicate, many-to-many, historical, protected, and round-trip cases before cutover.

### Common failures

Common failures are joining on names; declaring all “customer” concepts identical; using one universal enterprise model as a forced truth; treating the source of record as authoritative for every attribute and time; applying a one-to-one mapping to many-to-many identities; collapsing absent, unknown, not applicable, withheld, and false; translating codes without version or context; converting units without reference systems and precision; comparing snapshot and event grain; dropping unmatched values; hiding ambiguous matches; assuming mapping composition is transitive; overwriting sources after survivorship; using current mappings for history; validating only target shape; and combining data in ways that violate purpose, consent, residency, or access boundaries.

### Compact example

A sales system defines Customer as a buying account, support defines Customer as a contact person, and finance defines Customer as a legal debtor. `customer_id` values do not identify the same kind of object. Reconciliation introduces Account, Person, Party, and Debtor roles; maps each local identifier to its owned entity with confidence and time; represents account-person and debtor-account relationships explicitly; retains unresolved duplicates; and publishes purpose-specific views. No source is renamed into false agreement, and finance's debtor authority does not automatically decide marketing identity.

### Connections

[DARCH-014](014-entities-relationships-and-business-keys.md) supplies identity and relationship discipline. [DARCH-015](015-shared-vocabulary-and-business-glossaries.md) establishes concepts and terminology. [DARCH-016](016-canonical-models-and-their-trade-offs.md) explains canonical mediation, while [DARCH-018](018-temporal-and-historical-modeling.md) and [DARCH-019](019-model-versioning.md) provide time and version coordinates. This module completes the block before [DARCH-021](../ROADMAP.md) introduces business capabilities and data domains.

## Governing Question

Systems differ because they were built for different decisions. A retailer's “product” may be a sellable offer, a warehouse's product a stocked item, a manufacturer's product a design family, and a regulator's product an authorized formulation. Their disagreement is often legitimate. An integration that forces the labels into one record can become less truthful than the sources.

Reconciliation begins by asking what each model asserts, under which scope, at what grain, for which time, and by whose authority. It then chooses a purpose-specific relation: preserve both, map conditionally, translate, aggregate, disaggregate with evidence, select a survivor, create a new mediating concept, or leave unresolved. The objective is controlled interoperability, not uniformity for its own sake.

## Why This Matters

Model conflicts propagate into money, access, safety, operations, analytics, and accountability. A legal customer merged with a contact person can disclose data to the wrong party. A kilograms-to-pounds error can disrupt treatment or shipping. An order header compared to an order line can double revenue. A current address can overwrite the address known when a decision was made.

Terminology discipline is foundational. [ISO 704:2022](https://www.iso.org/standard/79077.html) distinguishes objects, concepts, designations, and definitions and provides principles for terminology work. Shared spelling is only a designation clue; reconciliation must compare the concepts and their domains.

Metadata registration and mapping supply durable structure. [ISO/IEC 11179-3:2023](https://www.iso.org/standard/78915.html) specifies registry concerns including identification, designation and definition, registration, classification, and mapping among registry items. Those separations help preserve local items and explicit mappings instead of mutating a global dictionary.

Knowledge-organization standards illustrate relation strength. W3C's [SKOS Reference](https://www.w3.org/TR/skos-reference/) distinguishes exact, close, broader, narrower, and related matches and deliberately avoids transitivity for `closeMatch`. The broader lesson is that “mapped” is not one semantic relationship and composition can compound error.

## Prerequisites and Retrieval

You should understand entities, relationships, keys, conceptual and logical models, canonical models, schemas, vocabularies, code lists, temporal modeling, versioning, metadata, transformations, distributed systems, security, privacy, data quality, and migration.

Retrieve perspective, assertion, concept, designation, definition, intension, extension, identity, grain, authority, provenance, source of record, system of entry, system of reference, system of insight, correspondence, crosswalk, equivalence, exact match, close match, broader, narrower, related, conditional, disjoint, unmapped, mapping, transformation, normalization, mediation, survivorship, golden record, match, merge, split, loss, reversibility, round trip, quarantine, reconciliation, and adjudication.

As a retrieval test, compare `status = ACTIVE` from two systems. Ask: status of which entity or role? Active for which process? Does absence differ from inactive? Which code-system version? At which valid and recorded time? Which authority? Can one account be active for support but inactive for billing? What mapping relation and evidence apply? Without these coordinates, `ACTIVE -> ACTIVE` is a lexical coincidence, not reconciliation.

## Learning Objectives

After completing this module, you should be able to:

1. inventory local model perspectives without assuming one is universally canonical or authoritative;
2. classify lexical, conceptual, identity, structural, grain, cardinality, code, unit, temporal, authority, quality, and protection conflicts;
3. distinguish exact, close, broader, narrower, related, conditional, disjoint, and unmapped correspondences;
4. specify directional, versioned mapping rules with preconditions, cardinality, loss, inverse behavior, provenance, and evidence;
5. reconcile identities and relationships without collapsing persons, parties, accounts, roles, devices, records, and households;
6. align units, reference systems, precision, code systems, defaults, absence, uncertainty, and temporal contexts;
7. govern sources of entry, reference, and authority at attribute, relationship, purpose, jurisdiction, and time scope;
8. design canonical mediation, pairwise translation, federation, semantic layers, event normalization, and purpose-specific views;
9. verify transformations with fixtures, constraints, differential tests, round trips, reconciliation, lineage, and operational evidence;
10. preserve privacy, security, retention, residency, consent, and accountable unresolved-conflict handling through integration.

## Core Exposition

**Begin with perspectives, not tables.** Document why each system exists, the decisions it supports, its owned responsibilities, and the questions its model answers. A warehouse table is evidence of implementation, not a complete conceptual definition. Interview domain authorities and inspect validations, workflows, events, reports, contracts, and historical behavior.

Record each model's boundary. A support case may refer to a caller, affected user, paying account, entitled organization, and device. Calling every reference `customer` loses roles that the workflow relies on. Preserve the local distinctions before proposing common concepts.

**Write assertions in full.** Compare `(subject, predicate, value)` only after adding identity, grain, context, time, authority, provenance, model version, and protection. “Account 17 is active” is incomplete when active can mean billable, enabled, under contract, recently used, or not closed.

Treat definitions as testable commitments. Include necessary and distinguishing characteristics, allowed values, exclusions, examples, counterexamples, and decision use. A glossary entry that merely repeats a label cannot support a mapping.

**Classify conflicts before resolving them.** Different conflict classes need different remedies:

- lexical: same concept with different labels, or same label for different concepts;
- identity: incompatible entity boundaries, keys, continuity, equality, or match criteria;
- structural: nesting, field organization, type, optionality, and representation differ;
- grain: one assertion represents a line, order, account, day, episode, or aggregate;
- cardinality: one-to-one, one-to-many, ordered, unique, or optional relationships differ;
- semantic: definitions, value meanings, rules, or interpretations differ;
- code: code-system identity, edition, hierarchy, status, or local extension differs;
- measurement: unit, scale, precision, reference system, calibration, or rounding differs;
- temporal: event time, valid time, recorded time, interval, snapshot, or correction differs;
- authority: systems own different attributes, contexts, jurisdictions, or decision uses;
- epistemic: observed, asserted, inferred, estimated, disputed, or unknown status differs;
- protection: purpose, consent, classification, access, retention, or residency differs.

A conflict can occupy several classes. Changing one country code may look lexical but also alter jurisdiction, taxation, residency, sanctions, and historical validity. Record the vector rather than choosing one convenient label.

**Separate labels, concepts, and objects.** ISO terminology principles distinguish a designation such as a term from the concept it denotes and the objects to which the concept applies. This prevents both homonym and synonym errors. `client` and `customer` may denote the same concept in one context; `customer` may denote several concepts across sales, support, and finance.

Use persistent concept and element identities, scoped definitions, examples, and provenance. Do not make a common English word the global identifier. Multilingual labels further demonstrate why strings cannot carry identity.

**Type correspondences.** A correspondence should say more than `source = target`. Useful relations include:

- exact for interchangeable concepts within the declared use;
- close for sufficiently similar concepts whose differences remain material elsewhere;
- broader and narrower for inclusion of extensions;
- related for an association without equivalence;
- conditional for a relation that depends on other values or context;
- disjoint for concepts that must not be merged;
- unmapped for a known absence of valid target representation;
- unknown or disputed when review cannot yet classify the relation.

SKOS provides a formal vocabulary for several of these relations and warns about mapping composition. Use its precise semantics when applicable, but do not misuse an information-retrieval relation as proof of operational substitutability in every domain.

**Make direction explicit.** A mapping from source `S` to target `T` need not work from `T` to `S`. A source concept may split into two targets based on context. Several source codes may collapse into one target code, destroying an inverse. An exact-looking field projection can lose provenance or absence distinctions.

HL7 FHIR's [ConceptMap](https://www.hl7.org/fhir/conceptmap.html) treats mappings as directional, records a relationship from source to target, permits multiple targets, and supports dependencies needed to choose among them. This is a useful model beyond healthcare: translation needs direction, contextual conditions, and the ability to say no valid mapping exists.

**Declare cardinality and totality.** A mapping can be one-to-one, one-to-many, many-to-one, many-to-many, partial, or set-valued. State whether every source value must map, every target can be produced, and multiple outputs are alternatives or a required set.

Never handle missing mappings with an undocumented catch-all target. `OTHER`, `UNKNOWN`, `UNMAPPED`, and `NOT_APPLICABLE` have different meanings. Preserve the original value and mapping result so future rule versions can reprocess it.

**Reconcile identity before attributes.** Field alignment is unsafe if records refer to different entities. Distinguish natural persons, legal persons, accounts, contracts, households, roles, devices, locations, documents, and representations. Define continuity: when does an entity remain the same across rename, ownership change, reissue, merger, or split?

Identity resolution should output match assertion, confidence or rule, evidence, authority, time, version, and disposition. A probabilistic match is not an equality fact. False merges contaminate every mapped attribute, while false splits fragment histories. High-consequence merges require challenge and reversible evidence.

Keep source identifiers and mapping tables. A global identifier can coordinate references, but it should not erase owned local identity. Record `same-as`, `possible-match`, `successor`, `alias`, `member-of`, and other relations explicitly rather than overloading one equivalence edge.

**Align grain before joining.** An order total and line amount differ by grain. A daily account balance and transaction event differ by temporal aggregation. A household preference and person consent differ by subject. Joining them on an identifier can produce plausible but false results.

Write a grain statement: “one row per X, per Y, at Z time, under authority A.” To map a finer grain to a coarser grain, define aggregation, currency/unit conversion, deduplication, effective time, missing inputs, late data, and correction behavior. Disaggregation requires source evidence; proportional allocation is an estimate, not recovered detail.

**Reconcile structures through semantics.** A nested address object and flat address columns may represent the same components, but ordering, repetition, type, and absence behavior still matter. A full name string cannot always split into given and family names. A list may be ordered in one model and an unordered set in another.

Use model transformations whose inputs and outputs are exact versions. The Object Management Group's [MOF Query/View/Transformation specification](https://www.omg.org/spec/QVT/) defines model query, view, and transformation languages in the MOF ecosystem. Regardless of technology, transformations should be treated as versioned model artifacts with declared preconditions and traces, not disposable scripts.

**Treat null and absence as a small ontology.** Common states include not observed, not provided, withheld, inapplicable, not yet known, no value exists, invalid, redacted, and lost in mapping. SQL null, omitted JSON property, empty string, zero, and sentinel code may implement different subsets.

Build explicit mappings for these states. A target that supports only one null necessarily loses distinctions; record that loss and retain source provenance. Do not let a default transform “unknown” into a business fact.

**Reconcile vocabularies with scope and version.** Code mapping requires source system, source version, target system, target version, relation, context, effective interval, and authority. Labels are documentation, not code identity. A code can be inactive but historically valid; a code's meaning can be corrected or disputed.

Map hierarchy carefully. A source code narrower than a target can usually roll up for some analytics, but mapping the target back requires choosing among children. Close matches may support search but not billing or clinical decisions. Store unmapped, ambiguous, and deprecated cases.

**Convert measurements completely.** Identify quantity kind, unit system and version, scale, offset, reference condition, coordinate/reference system, precision, accuracy, uncertainty, and rounding. Temperature Celsius-to-Fahrenheit is affine, not a simple multiplier. Currency conversion requires rate type, market, authority, and time. Geographic coordinates require a datum.

Test zero, negative, extrema, overflow, precision boundaries, and round trips. If rounding loses information, state tolerances and retain the source value. Do not convert a qualitative score as though it were a physical measurement merely because both are numeric.

**Align temporal semantics.** Determine whether a field represents occurrence, observation, validity, recording, publication, ingestion, or processing time. Reconcile instants with intervals, local civil time with UTC instants, current snapshots with histories, and retroactive corrections with append-only events.

A current snapshot cannot recreate prior state. An event stream cannot automatically supply valid-time intervals. Mapping today's code or rule onto old data creates a restated view, not an as-was history. Pin model, mapping, vocabulary, calendar/zone, and rule versions for reproducibility.

**Scope authority per assertion.** “System of record” is often too broad. One system may be authoritative for legal name, another for delivery address, and another for risk status. Authority can depend on jurisdiction, product, workflow state, valid time, evidence quality, and intended decision.

Distinguish system of entry, authoritative reference, operational execution, and analytical derivation. A source can faithfully record a user's assertion without proving it true. Survivorship selects values for a specified view; it should cite policy and preserve competing assertions.

**Do not confuse quality with authority.** A complete, fresh source may lack domain authority. An authoritative registry may be delayed. Quality dimensions—validity, completeness, timeliness, consistency, uniqueness, accuracy evidence—inform reconciliation but do not mechanically select truth.

Record why one assertion was chosen, composed, or rejected. When authorities conflict, escalate under an adjudication policy, present plural views, or quarantine. Silent last-write-wins merely delegates authority to arrival order.

**Choose an integration topology intentionally.** Pairwise mappings minimize a shared center but grow roughly with system pairs and can diverge. A canonical model reduces interface count but can become a lowest-common-denominator or centralized domain takeover. A semantic mediation layer preserves correspondences while translating at boundaries. Federation lets domains publish owned contracts and mappings.

Hybrids are common: shared concepts and identity protocols, domain-owned models, purpose-specific canonical messages, and explicit mappings. Choose based on coupling, change rate, governance, performance, consequences, and ownership—not diagram symmetry.

**Keep canonical models bounded.** A canonical model should serve a declared integration context, not claim to replace every local perspective. Preserve extensions and unmapped local meaning. Avoid a giant optional structure that says almost nothing and still requires consumer-specific interpretation.

A canonical hub can amplify a bad mapping to every participant. Version it, test all edges, and keep source-to-canonical and canonical-to-target loss visible. Sometimes direct mapping is safer for two systems with a specialized shared use.

**Represent mappings as governed artifacts.** A mapping record includes exact source and target model versions; source and target paths or concept IDs; relation; conditions; transformation; cardinality; default/absence handling; loss; inverse or non-invertibility; temporal effectivity; author; reviewer; evidence; tests; and lifecycle.

W3C's [R2RML](https://www.w3.org/TR/r2rml/) is an example of a mapping language that makes relational-to-RDF transformations declarative and executable. Its particular target is not universal, but the architectural lesson is: mapping logic can be identified, reviewed, validated, versioned, and tested independently of application code.

**Preserve transformation provenance.** For every derived assertion, record source artifacts, mapping version, activity, execution, agent or service, time, parameters, warnings, and output identity. The W3C [PROV-O ontology](https://www.w3.org/TR/prov-o/) provides terms for entities, activities, agents, usage, generation, attribution, and derivation that can express these chains.

Provenance must be useful, not merely voluminous. It should answer which sources and rules produced a value, who authorized them, what was lost, and whether the result can be regenerated. Secure provenance because it can reveal sensitive relationships and system internals.

**Validate both shapes and cross-model invariants.** Source validation proves the input meets its declared model. Target validation proves the output meets the target shape. Neither proves the transformation preserved meaning. Add relational assertions: totals reconcile, references resolve, units convert within tolerance, disjoint codes do not merge, required provenance exists, and protected values do not leak.

W3C's [Shapes Constraint Language](https://www.w3.org/TR/shacl/) defines validation of data graphs against shapes graphs and produces structured validation reports. Constraint technologies can make reconciliation failures inspectable, but their result remains bounded to the shapes, data graph, processor, and entailment regime supplied.

**Test mapping composition.** If `A -> B` and `B -> C` exist, do not infer that `A -> C` is acceptable. The first mapping may collapse a distinction required by the second. Defaults, context, identity, and version intervals can also differ.

Generate direct composition tests and compare them with approved direct mappings where available. Detect cycles, contradictory correspondences, non-confluent transformations, and path-dependent outputs. Record which paths are authorized for which use.

**Use round trips as evidence, not a universal criterion.** For a purported lossless mapping `f` with inverse `g`, test `g(f(x)) = x` over the declared domain. For normalization, equality may be semantic rather than byte-for-byte. For intentionally lossy mappings, test preserved invariants and explicit loss markers.

Round-trip success on fixtures does not prove total invertibility. Generate boundary values and representative populations, and inspect collisions where multiple sources map to one target. Never invent an inverse for a many-to-one mapping.

**Operationalize unresolved outcomes.** A mapping engine should emit success, conditional success, unmapped, ambiguous, conflicting, invalid, and execution-failure outcomes separately. Route them to retry, quarantine, human review, source correction, or accepted-loss workflows with owners and service objectives.

Monitor rates by model version, mapping rule, source, target, code, protection class, and time. A sudden fall in unmatched rows can be suspicious if a catch-all rule began hiding errors. Sample accepted mappings as well as failures.

**Plan migration and coexistence.** Baseline source and target versions, inventories, counts, identities, quality, protections, and mappings. Run transformations in shadow or batch, compare invariants, adjudicate exceptions, and establish checkpoints. Capture concurrent source changes so the baseline does not drift unnoticed.

During coexistence, define which system can write which assertion, how changes propagate, how loops and duplicates are prevented, and how corrections flow. Use stable operation and source identities. Reconcile after retries and partial failure rather than assuming delivery means equivalence.

**Protect rollback.** A rollback must restore an operationally and semantically coherent state. If the target introduced distinctions the source cannot represent, rolling code back can lose data. Retain source evidence, forward changes, mappings, checkpoints, and quarantine under authorized protection.

Define stop conditions before cutover: mismatch rate, unresolved high-consequence cases, reference failures, protected-data leakage, latency, duplicate side effects, or missing provenance. Exercise rollback from partial batches and live writes.

**Carry security and privacy through derivation.** Mapping can broaden audience, join identities, infer sensitive facts, move data across residency boundaries, or change purpose. Target classification should be at least as restrictive as source obligations unless an accountable policy authorizes transformation.

Consent and purpose are not ordinary booleans to aggregate. One source's marketing consent may apply to a channel, controller, purpose, jurisdiction, and interval. Combining it with a global preference can violate the original scope. Retain policy coordinates and enforce them at mapping and access time.

Mappings, linkage tables, golden records, and provenance are themselves sensitive. Limit access, encrypt, audit, retain only as justified, and test deletion and correction propagation. Derived data can remain personal or confidential even after source fields are renamed.

**Govern human adjudication.** Some conflicts need domain judgment. Provide the reviewer with source assertions, definitions, evidence, authorities, versions, time, protection, and downstream consequence. Record decision, rationale, scope, approver, effective time, and appeal or correction path.

Avoid interfaces that force a false binary answer when “insufficient evidence,” “both valid in different contexts,” or “requires source correction” is correct. Measure consistency among reviewers and revisit rules when disagreement is systematic.

**Publish purpose-specific products.** A reconciled analytical view, operational command, regulatory report, and search index may need different survivorship and loss tolerances. Give each output a contract, authority, lineage, refresh semantics, quality evidence, and limitations.

Do not market a “golden record” as universal truth. It is a governed projection for named uses. Keep source assertions and conflict history where authorized so corrections and alternative views remain possible.

**Make decisions auditable.** A future reviewer should be able to retrieve exact source and target models, mapping and policy versions, inputs, outputs, reconciliation results, approvals, and observed limitations. If evidence was deleted lawfully, record the limitation without reconstructing facts.

Reconciliation is complete for a use only when consumers understand the output contract, unresolved cases are governed, operational behavior is stable, protection is verified, and source meaning remains traceable. A green pipeline with silently collapsed distinctions is not success.

## Definitions and Notation

Let `S_i` and `T_j` be exact source and target model versions. A source assertion is `a_s` and a target assertion is `a_t`. A mapping is a partial relation or function:

`R_ij: (a_s, context, time) -> {a_t, unresolved, unmapped, invalid}`

The output is not limited to a value; it includes outcome, provenance, loss, and warnings. A mapping is total only if every valid source assertion in its declared domain has an authorized result. Totality should never be fabricated with an undifferentiated fallback.

Define an assertion signature:

`Sig(a) = (subject_kind, predicate_concept, value_domain, identity, grain, context, valid_time, authority)`

Lexically identical fields can be candidates for comparison, but exact correspondence for a use requires compatible signatures and protection obligations. Differences can be resolved, preserved, or declared irrelevant only through policy and evidence.

For a mapping `f: D_s -> D_t`, the collision set for target `y` is `C_y = {x in D_s | f(x)=y}`. If `|C_y| > 1`, the target does not identify which source value occurred without additional provenance. A proposed inverse is therefore not a function over that result unless context restores the distinction.

Let `P = R_ab ; R_bc` be composed mapping from A through B to C. Approval of `R_ab` and `R_bc` does not imply approval of `P`; relation meaning, preconditions, loss, versions, and use must be re-evaluated. This formalizes why mapping networks need path governance.

A survivorship function `W(assertions, purpose, policy_version, as_of)` returns selected assertions plus rationale and rejected or unresolved alternatives. `W` produces an authorized view; it does not alter the source assertions or prove metaphysical truth.

## Mechanisms, Invariants, or Proof Structure

Use ten gates for each reconciliation surface.

**1. Perspective gate.** Identify systems, purposes, boundaries, owners, model versions, decisions, and local concepts without imposing premature equivalence.

**2. Assertion gate.** Record subject, predicate, value domain, identity, grain, context, temporal semantics, authority, provenance, and protection for compared elements.

**3. Conflict gate.** Classify lexical, identity, structural, grain, cardinality, semantic, code, measurement, temporal, authority, epistemic, quality, and protection conflicts.

**4. Correspondence gate.** Assign directional exact, close, broader, narrower, related, conditional, disjoint, unmapped, unknown, or disputed relations with scope and evidence.

**5. Transformation gate.** Specify exact versions, preconditions, cardinality, rules, defaults, absence, loss, inverse behavior, provenance, failures, and lifecycle.

**6. Authority gate.** Define attribute-, relationship-, context-, jurisdiction-, time-, and purpose-specific authorities; govern survivorship, plural views, and adjudication.

**7. Validation gate.** Test source and target shape, semantic invariants, identities, references, counts, aggregates, units, times, mapping paths, round trips, and representative populations.

**8. Protection gate.** Preserve classification, purpose, consent, access, residency, retention, deletion, audit, and inference controls across sources, mappings, outputs, and provenance.

**9. Operational gate.** Control coexistence, change capture, idempotency, ordering, retries, quarantine, reconciliation, observability, cutover, rollback, recovery, and correction.

**10. Evidence gate.** Retain exact artifacts, digests, fixtures, reports, exceptions, approvals, limitations, lineage, operational observations, and retirement evidence.

The executable example checks four narrow mapping-record failures: an unscoped equivalence, missing unit conversion, grain loss without an allocation rule, and survivorship without authority.

<!-- bijux-verify: {"id":"model-reconciliation-integrity","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"mappings=4\nvalid=0\nfindings=amount:missing-unit-rule,consent:missing-authority,customer-status:unscoped-equivalence,order-line:unhandled-grain-loss\nready=false\n","stderr":""}} -->
```python
mappings = (
    {"id": "customer-status", "relation": "exact", "scope": "", "unit_change": False, "unit_rule": "", "grain_change": False, "allocation_rule": "", "survivorship": False, "authority": ""},
    {"id": "amount", "relation": "conditional", "scope": "invoice", "unit_change": True, "unit_rule": "", "grain_change": False, "allocation_rule": "", "survivorship": False, "authority": ""},
    {"id": "order-line", "relation": "broader", "scope": "revenue", "unit_change": False, "unit_rule": "", "grain_change": True, "allocation_rule": "", "survivorship": False, "authority": ""},
    {"id": "consent", "relation": "conditional", "scope": "email-marketing", "unit_change": False, "unit_rule": "", "grain_change": False, "allocation_rule": "", "survivorship": True, "authority": ""},
)

findings = []
valid = 0
for mapping in mappings:
    local = []
    if mapping["relation"] == "exact" and not mapping["scope"]:
        local.append("unscoped-equivalence")
    if mapping["unit_change"] and not mapping["unit_rule"]:
        local.append("missing-unit-rule")
    if mapping["grain_change"] and not mapping["allocation_rule"]:
        local.append("unhandled-grain-loss")
    if mapping["survivorship"] and not mapping["authority"]:
        local.append("missing-authority")
    if local:
        findings.extend(f"{mapping['id']}:{finding}" for finding in local)
    else:
        valid += 1

print(f"mappings={len(mappings)}")
print(f"valid={valid}")
print("findings=" + ",".join(sorted(findings)))
print(f"ready={str(valid == len(mappings)).lower()}")
```

The checker validates four declared mapping-record predicates only. It does not prove conceptual identity, complete conflict discovery, mapping correctness, identity resolution, authority, semantic preservation, conversion accuracy, protection, migration safety, source truth, or successful adjudication. Those require domain definitions, exact versions, representative populations, executable transformations, independent constraints, operational evidence, and accountable review.

## Alternatives and Trade-Offs

**Pairwise mappings versus canonical mediation.** Pairwise mappings preserve specialized agreements but multiply with participants. Canonical mediation reduces interfaces but can flatten local meaning and centralize change. Bound canonical models by use and keep edge loss visible.

**Materialized versus virtual reconciliation.** Materialized products offer predictable performance and frozen evidence but become stale and duplicate protected data. Virtual views retain source freshness but couple availability and mapping execution. Choose by latency, reproducibility, protection, and failure tolerance.

**Deterministic versus probabilistic identity matching.** Deterministic rules are explainable but may miss legitimate matches. Probabilistic linkage increases recall but creates uncertain equality and review burden. Never promote scores to identity without thresholds, evidence, consequences, and reversal.

**Central survivorship versus plural assertions.** A single value simplifies consumers but hides disagreement and context. Plural assertions preserve truth claims but require consumers to apply policy. Publish purpose-specific survivors while retaining authorized alternatives and rationale.

**Early normalization versus late interpretation.** Early normalization reduces repeated work but can erase source distinctions. Late interpretation preserves evidence but distributes complexity. Retain raw assertions and produce governed normalized views where consequence warrants.

**Strict quarantine versus best-effort fallback.** Quarantine protects correctness but delays flows. Fallback maintains availability but may misclassify. Define which uses allow degraded results and make them observable; high-consequence decisions may require fail-closed behavior.

**Declarative versus imperative transformations.** Declarative mappings improve inspection and analysis. Imperative code handles complex context and workflows. Both require versioning, tests, lineage, and bounded semantics; generated opacity is not governance.

**Automated versus human adjudication.** Automation is repeatable and scalable for explicit rules. Human review handles contextual ambiguity but is slower and inconsistent. Route by consequence and uncertainty, instrument reviewer agreement, and turn stable decisions into governed rules.

## Failure Modes and Misconceptions

1. **Same label means same concept.** Homonyms are common across bounded contexts.
2. **Different labels mean different concepts.** Synonyms, languages, and local terminology can designate one concept.
3. **A canonical model is enterprise truth.** It is a bounded mediation contract whose authority and loss must be explicit.
4. **The source of record owns every attribute.** Authority varies by assertion, context, jurisdiction, purpose, and time.
5. **A mapping is naturally reversible.** Many-to-one, defaults, rounding, aggregation, and omission destroy inverses.
6. **Exact match is safe in every use.** Correspondence scope and operational substitutability still require evidence.
7. **Mappings compose automatically.** Intermediate loss and conflicting conditions make paths non-transitive.
8. **Target validation proves a correct transformation.** Valid output can preserve the wrong identity, meaning, unit, or time.
9. **Unknown and false are interchangeable.** This manufactures facts and corrupts decisions.
10. **A global identifier solves semantics.** It coordinates identity but does not align roles, predicates, grain, or authority.
11. **Last-write-wins reconciles conflict.** It makes arrival order an undocumented authority policy.
12. **Aggregation can be undone.** Disaggregation without evidence is allocation or estimation, not recovery.
13. **Current mappings correctly interpret history.** Models, codes, rules, authorities, and time contexts change.
14. **Golden records contain universal truth.** They are purpose-specific derived products with survivorship and limitations.
15. **Unmapped values should be dropped.** They are evidence of scope, drift, defects, or legitimate local meaning.
16. **More integration data is always better.** Linking can violate minimization, purpose, consent, residency, and inference constraints.
17. **A successful cutover ends reconciliation.** Late data, corrections, replay, recovery, model evolution, and retirement continue.

## Worked Examples

### Example 1

Sales Customer is an account, support Customer is a caller, and finance Customer is a debtor. Reconciliation models Account, Person, Party, and roles, preserving local identifiers and relationship validity. It rejects a universal customer join and publishes separate service and receivables views.

### Example 2

One system records `ACTIVE` for enabled login; another records `ACTIVE` for a paid subscription. The mapping classifies the values as related rather than exact, derives an “eligible to sign in” view from both predicates and time, and preserves cases where only one is active.

### Example 3

A source reports weight in pounds to one decimal; a target expects kilograms to three decimals. The mapping pins unit definitions, multiplies by the exact conversion factor, records source precision, rounds only for presentation, tests extrema, and retains original values for audit and rollback.

### Example 4

A warehouse stores one row per order while an event system emits one row per line adjustment. Direct joining multiplies totals. The reconciled model declares grains, groups events by order and valid window, handles reversals and late events, and verifies totals against source-controlled examples.

### Example 5

A legacy code `X` can mean either “expedited” or “external” depending on transaction type. The crosswalk is conditional on that type, yields ambiguous when context is absent, and never maps `X` through an unconditional catch-all.

### Example 6

Two identity services disagree whether records represent the same person. Instead of merging, the integration stores competing match assertions with evidence, confidence, algorithm version, and reviewer decision. Protected attributes are not disclosed until the authorized threshold and purpose are met.

### Example 7

A CRM address is current-only; a policy system needs the address valid when a contract was signed. Reconciliation cannot derive history from the CRM snapshot. It marks the historical address unknown, seeks documentary evidence, and avoids copying today's address into the earlier decision.

### Example 8

A global preference says “no marketing,” while a regional system records email consent for one product and period. Survivorship does not choose the newest boolean. It evaluates controller, purpose, channel, jurisdiction, evidence, and valid time, then applies the more restrictive authorized rule with provenance.

### Example 9

Mappings A-to-B and B-to-C both pass local tests, but B collapses two source risk categories that C treats differently. Composition tests reveal the collision. The architecture creates a direct A-to-C rule for that use and labels the mediated path unsupported.

### Example 10

After cutover, the target accepts all rows and counts match, yet revenue differs. Investigation shows target defaults treated missing discounts as zero while the source excluded unknown discounts. Reconciliation adds absence states, recalculates aggregates, reports restated history separately, and expands monitoring beyond row counts.

## Cross-Program Connections

- **Data engineering:** transformations, CDC, event normalization, late data, lineage, quality, backfill, quarantine, and reconciliation execute mappings at scale.
- **Database engineering:** keys, constraints, joins, views, reference data, temporal queries, migrations, and transaction semantics expose model conflicts.
- **API and service engineering:** boundary contracts, anti-corruption layers, adapters, negotiation, error models, and consumer compatibility localize translation.
- **Platform engineering:** schema and metadata registries, lineage, policy engines, orchestration, observability, secrets, and recovery support governed mappings.
- **Machine learning:** entity resolution, feature definitions, label semantics, training-serving skew, uncertainty, and drift depend on reconciled meaning.
- **Security and privacy:** identity linkage, inference, purpose, consent, residency, minimization, retention, deletion, and access constrain integration.
- **Programming languages:** types, parsers, algebraic outcomes, total functions, partial functions, property tests, and provenance structures encode mapping behavior.
- **Systems engineering:** interface control, configuration baselines, traceability, discrepancy reports, change control, hazards, and verification support reconciliation assurance.

## References

1. ISO, *ISO 704:2022 Terminology work—Principles and methods*, 2022. <https://www.iso.org/standard/79077.html>
2. ISO/IEC, *11179-3:2023 Information technology—Metadata registries—Part 3: Metamodel for registry common facilities*, 2023. <https://www.iso.org/standard/78915.html>
3. W3C, *SKOS Simple Knowledge Organization System Reference*, W3C Recommendation, 2009. <https://www.w3.org/TR/skos-reference/>
4. HL7 International, *FHIR ConceptMap*, Release 5. <https://www.hl7.org/fhir/conceptmap.html>
5. Object Management Group, *MOF Query/View/Transformation Specification*, Version 1.3, 2016. <https://www.omg.org/spec/QVT/>
6. W3C, *R2RML: RDB to RDF Mapping Language*, W3C Recommendation, 2012. <https://www.w3.org/TR/r2rml/>
7. W3C, *PROV-O: The PROV Ontology*, W3C Recommendation, 2013. <https://www.w3.org/TR/prov-o/>
8. W3C, *Shapes Constraint Language (SHACL)*, W3C Recommendation, 2017. <https://www.w3.org/TR/shacl/>

## Exercises

### Exercise 1

Reconcile “customer” across a sales account system, support contact system, and legal debtor register. Define entities, roles, identities, relations, authority, time, unresolved cases, and purpose-specific outputs.

### Exercise 2

Design a versioned crosswalk between two product-status code systems where mappings are exact, broader, conditional, ambiguous, and unmapped. Include composition, history, provenance, testing, and change governance.

### Exercise 3

Map a line-level order event model into a daily account summary. Specify grain, identity, event corrections, currency and units, time windows, late data, aggregation, loss, reconciliation, and rollback.

### Exercise 4

Evaluate pairwise, canonical, and federated topologies for six domains that exchange party and consent data. Compare mapping count, ownership, change coupling, protection, performance, evidence, and failure isolation.

### Exercise 5

Plan migration from two conflicting identity stores into a reconciled service. Cover match evidence, false merges and splits, human adjudication, coexistence, security, deletion, observability, cutover, rollback, and retirement.

## Answers to the Exercises

### Answer 1

Model Party as a continuity abstraction, Account as the buying arrangement, Person as an individual, ContactRole as a support relationship, and DebtorRole as a legal obligation. Preserve each source identifier and exact model version. Map relationships rather than asserting that every Customer record is the same entity. Identity correspondences can be exact, possible, disjoint, successor, or unresolved, with evidence and valid/recorded time.

Sales is authoritative for account configuration, support for locally observed contact interactions, and the legal register for debtor status within its jurisdiction and effective interval. None is globally authoritative for person identity. Publish a sales account view, support contact view, and receivables view with scoped survivorship. Quarantine ambiguous matches and restrict cross-source attributes until purpose and access permit linkage. Keep source assertions, mapping versions, decisions, and corrections auditable.

### Answer 2

Give both code systems and every code stable identities and exact versions. Each crosswalk row names source and target versions, direction, relation, context predicates, valid interval, author, authority, evidence, and outcome. Use exact only for interchangeability in the declared use; broader/narrower for hierarchy; conditional where product class or jurisdiction selects a target; ambiguous for several candidates; and unmapped when no valid target exists.

Preserve the original code and mapping outcome. Do not compose close or conditional relationships automatically through a third scheme. Test every source code, invalid and retired codes, missing context, multiple targets, historical versions, hierarchy rollups, and round trips where invertibility is claimed. Version the crosswalk when either scheme or rule changes, run impact analysis, notify consumers, and keep historical mappings resolvable.

### Answer 3

Declare source grain as one assertion per order line adjustment event and target grain as one account, currency, and business day. Resolve order, line, account, currency, occurrence time, valid time, event identity, correction/supersession, and model version before aggregation. Convert monetary units with pinned currency and rate policy; deduplicate by event identity and apply reversals exactly once.

Define window zone and half-open boundaries, watermark, late-event policy, reopening and restatement behavior, and unknown-account quarantine. The mapping is intentionally lossy because line sequence and detail are absent from the summary; retain event lineage and counts. Reconcile sums, counts, accounts, currencies, corrections, and boundary fixtures against the event source. Rollback restores the previous summary projection and replays retained authoritative events with its exact reducer version.

### Answer 4

Pairwise translation preserves each bilateral use and isolates a canonical failure, but up to thirty directed edges among six domains are possible and semantic decisions can diverge. One canonical party-and-consent model reduces interface count but centralizes ownership, couples release schedules, and risks flattening purpose, controller, channel, jurisdiction, and time. Federation keeps domain contracts authoritative and publishes shared identities, correspondence types, discovery, and policy conventions, but requires mature governance and runtime resolution.

Use a hybrid: domain-owned models, a shared party identity protocol, a narrowly scoped consent exchange contract, and versioned edge mappings. Enforce purpose and residency before movement, preserve consent coordinates, cache only within retention, and validate each path. Measure latency, unresolved outcomes, mapping drift, and protection violations. Keep failures at one edge from corrupting the shared registry, and retain exact lineage and test evidence for every supported route.

### Answer 5

Baseline both stores, exact models, identities, links, protected attributes, histories, quality, consumers, and recovery paths. Define deterministic and probabilistic match rules with versions, thresholds, evidence, and consequence tiers. Preserve possible-match and disjoint outcomes; require human review for high-impact ambiguous merges. Record reviewer rationale and allow later split or correction.

Introduce a new reconciliation identity without erasing source identifiers. Run shadow matching, sample accepted and rejected cases, test protected cohorts, and monitor false-merge/split indicators. During coexistence, capture changes idempotently, prevent propagation loops, reconcile attributes by scoped authority, and propagate corrections and authorized deletions. Cut over consumers in cohorts with stop conditions. Rollback retains new assertions and linkage evidence; it never blindly writes merged data back to sources. Retire old services only after consumer, archive, replay, access, deletion, and disaster-recovery evidence passes, while retaining authorized historical interpretation and limitations.
