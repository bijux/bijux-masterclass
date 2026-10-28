---
module_id: DARCH-011
program: Data Architecture Engineering
level: 1
module_number: 11
title: Conceptual Data Models
status: complete
last_verified: 2026-09-03
---

# Conceptual Data Models

## One-Page Review

### Governing question

How can a team model the concepts, identities, relationships, events, rules, and distinctions that matter to a domain without prematurely encoding one application's schema, one process, or one stakeholder's vocabulary as universal truth?

### Essential definitions

- A **conceptual data model** is a technology-independent, purpose-bounded account of domain concepts, relationships, identity, distinctions, constraints, and meaning.
- A **concept** is a unit of meaning used for reasoning in a declared context; its label is not its definition.
- An **entity type** classifies things treated as having identity through time; an **instance** is one occurrence classified by a type.
- A **value type** describes a value and its semantics, unit, scale, precision, or allowed domain without independent business identity.
- A **relationship type** states a semantically named association among concept roles, with applicability, cardinality, temporality, and constraints.
- A **role** is context-dependent participation in a relationship or situation; it should not automatically become a permanent subtype.
- An **event** is an occurrence with identity and time that may change state, establish evidence, or connect participants.
- An **invariant** is a rule intended to hold over a defined scope and time; a **derivation** explains how a fact follows from other facts.
- A **semantic authority** is the role or source authorized to define or adjudicate meaning for a bounded subject.

### Central model, mechanism, or theorem

Represent a conceptual model as:

`C = (concepts, relations, identities, constraints, contexts, authorities, evidence)`

Interpretation is valid only relative to purpose, scope, time, and authority. A model is adequate for decision `d` when it distinguishes every materially different case needed by `d`, avoids distinctions irrelevant to `d`, and makes identity, relationship, rule, uncertainty, and disputed meaning explicit. Conceptual completeness is therefore bounded; a larger model is not necessarily a better one.

### Critical invariants

- Every concept has stable identity, preferred term, definition, scope, examples, counterexamples, authority, status, and effective period.
- The model distinguishes type from instance, entity from role, event from state, value from identifier, and concept from physical representation.
- Every relationship is named as a domain proposition and defines participant roles, direction, cardinality, optionality, time, and applicable constraints.
- Identity states which observations refer to the same continuing thing, who may assert or merge identity, and how ambiguity and change are represented.
- Classification hierarchies state whether subtypes are disjoint, exhaustive, overlapping, temporary, or context-specific.
- Time-sensitive facts state valid time, recording time, duration, sequence, and correction semantics as needed.
- Definitions avoid circularity, hidden implementation, undefined terms, and criteria that cannot distinguish examples from counterexamples.
- Differences among vocabularies are mapped explicitly; similarity of labels never proves equivalence.
- Automated conformance checks state their logical assumptions and do not prove domain truth, completeness, or stakeholder agreement.

### Common failures

Common failures are reverse-engineering tables and calling the result conceptual; naming boxes without definitions; using `Customer`, `User`, or `Party` as universal categories; confusing a role with a kind of person; treating a mutable code as identity; omitting events and time; reading optionality from missing data; turning every attribute into an entity or every entity into a table; forcing one canonical vocabulary across legitimate contexts; hiding uncertain or contested meaning; adding `Other` to make a hierarchy appear exhaustive; mixing instance examples into type definitions; and declaring ontology or UML syntax validation to be business validation.

### Compact example

A university model equates `Student` with a row in the enrollment system and assigns one permanent student number. Interviews reveal applicant, admitted person, enrolled learner, course participant, researcher, employee, and alumnus are roles with different time intervals and authorities. One person may hold several simultaneously; two records may refer to one person; some learners have no institutional number yet. The conceptual model separates Person identity, Participation roles, Admission and Enrollment events, identifiers issued by authorities, and context-specific relationships. Logical schemas can now vary without redefining the domain.

### Connections

[DARCH-009](009-architecture-views-and-stakeholders.md) determines whose concerns the model serves, and [DARCH-010](010-writing-a-data-architecture-charter.md) bounds authority and purpose. [DARCH-012](../ROADMAP.md) translates conceptual commitments into logical structures; later modules address physical separation, semantics, identity, canonical exchange, history, and evolution.

## Governing Question

A conceptual model is an agreement about meaning precise enough to support consequential decisions. It asks what kinds of things the domain recognizes, how they are identified, which relationships and events matter, what can coexist, how facts vary through time and context, and who has authority to decide disputed semantics.

It deliberately postpones storage and transport choices. A conceptual `Agreement` is not a table; `is party to` is not a foreign key; `Money` is not a decimal column; and a one-to-many relationship does not select embedded documents or normalized relations. Those choices belong to logical and physical design after meaning is sufficiently clear.

Conceptual models remain selective. A hospital, insurer, public-health agency, and patient may all use `encounter` differently for legitimate purposes. The goal is not to discover a context-free dictionary hidden in reality. It is to represent relevant distinctions, overlaps, authorities, and mappings honestly enough for a bounded decision.

## Why This Matters

Semantic defects propagate. If `customer` alternately means a legal contracting party, a household, a person using a service, and a marketing target, then metrics, access rules, retention, interfaces, models, and decisions can be internally consistent yet mutually misleading. Repair after implementation requires data conversion, contract changes, historical reinterpretation, and governance work.

Peter Chen's original [entity–relationship paper](https://doi.org/10.1145/320434.320440) proposed a model intended to incorporate important semantic information and help unify different views of data. Modern conceptual modeling includes entities and relationships but also roles, events, identity, time, rules, authority, uncertainty, and multiple contexts. The historical source motivates semantic separation; it does not make one ER notation sufficient for every domain.

ISO/IEC [11179-3:2023](https://www.iso.org/standard/78915.html) specifies metadata-registry information as a conceptual data model and covers registry items, identification, designation, definition, registration, and classification. It is useful discipline for governed concepts and definitions, not a ready-made domain model.

Good models reduce accidental coupling. Multiple applications can realize the same conceptual commitments differently. Changes can be classified as clarified meaning, new context, new logical representation, or physical migration instead of being collapsed into “schema change.” Conceptual models also expose disagreements early, when alternatives remain reversible.

## Prerequisites and Retrieval

You should understand stakeholders, concerns, bounded contexts, data products and flows, systems of record, principles, drivers, constraints, risk, architecture views, charters, basic sets and relations, identifiers, state, events, and data lifecycle.

Retrieve type, instance, entity, value, role, event, state, relationship, participant, cardinality, optionality, subtype, classification, identity, identifier, definition, designation, synonym, homonym, context, authority, invariant, derivation, valid time, transaction time, provenance, and evidence.

As a retrieval test, inspect a box labeled `Customer`. Ask whether it denotes a person, organization, account, contract party, service user, buyer role, household, or mastered record; which context and time apply; what establishes identity; whether a thing can enter or leave the category; who defines it; and which decisions require the distinction. A box that cannot answer these questions is a placeholder, not yet a concept.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish conceptual, logical, and physical data models and prevent implementation leakage;
2. define concepts through purpose, identity, necessary distinctions, examples, counterexamples, authority, and scope;
3. distinguish entity types, value types, roles, events, states, and representations;
4. model semantically named relationships with participants, cardinality, optionality, time, and constraints;
5. analyze identity, identifiers, matching, merging, splitting, and authority without equating records with real-world things;
6. construct subtype and classification structures with explicit disjointness, completeness, and context;
7. represent temporal, historical, disputed, derived, and uncertain facts;
8. map vocabularies across bounded contexts without forcing false equivalence;
9. review models with scenarios, examples, counterexamples, competency questions, and invariants;
10. govern versioning, decisions, evidence, change impact, and transition into logical design.

## Core Exposition

**Start with purpose and competency questions.** State the entity or domain, stakeholder decisions, scenarios, scope, lifecycle interval, jurisdictions, authoritative sources, and exclusions. Write questions the model must answer: Can one person hold several customer roles? Which agreement authorizes a service? What was the classification when a decision occurred? Which correction superseded a reported event? Questions discipline abstraction and later provide tests.

Do not begin with every noun in workshop notes. Candidate concepts earn inclusion when their identity, distinction, relationship, rule, or lifecycle affects an in-scope decision. A model for billing may need Agreement, Obligation, Charge, Payment, Adjustment, Party, and Account roles but not every user-interface label.

**Build a concept register before polishing diagrams.** For each concept record stable identifier, preferred term, definition, context, type category, identity criterion, synonyms and forbidden aliases, examples, counterexamples, properties, relationships, invariants, source, semantic owner, contributors, status, effective interval, uncertainty, decisions using it, and mappings.

Definitions should be intensional enough to distinguish membership, not merely enumerate familiar instances. Avoid “a customer is a customer record,” circular chains, unexplained adjectives, and definitions that encode one department's procedure. Use positive criteria, necessary qualifications, scope notes, and exclusions. Test with edge cases.

**Distinguish concept from designation.** A word or label designates a concept within a language and context. The same concept may have synonyms; the same word may be a homonym for different concepts. Multilingual labels can differ in granularity and connotation. Give the concept stable identity and govern labels separately.

W3C [SKOS](https://www.w3.org/TR/skos-reference/) supports concept schemes, preferred and alternative labels, notes, broader/narrower and associative relations, and mappings such as exact or close match. It is valuable for controlled vocabularies. Its flexible knowledge-organization semantics should not be mistaken for all domain constraints or for OWL class semantics.

**Choose the right modeling category.** An entity type classifies continuing or identifiable things such as Person, Organization, Agreement, Asset, or Claim. A value type captures meaning carried by a value, such as Currency Amount, Temperature, Percentage, Postal Code, or Time Interval. A role captures participation, such as Buyer, Beneficiary, Approver, or Custodian, often with context and duration.

An event records that something occurred: Order Submitted, Consent Withdrawn, Specimen Collected, Ownership Transferred, or Measurement Observed. State describes a condition over an interval. Treating events as mutable state destroys chronology and evidence; treating every state change as an unrelated event can obscure enduring identity. Model both when the decision needs both.

**Establish identity explicitly.** Identity answers when two observations refer to the same thing through time and change. It is not identical to an identifier. A passport number, account code, URI, database key, biometric match, or supplier reference is issued or observed under authority and may be missing, reused, revoked, corrected, or conflicting.

Record identity criterion, identifier schemes and issuers, uniqueness scope, validity interval, evidence, matching confidence, merge and split authority, conflict rules, and consequences. Avoid universal “golden record” language when identity remains probabilistic or context-dependent. Preserve source assertions and decisions rather than erasing ambiguity.

**Name relationships as propositions.** `Party places Order`, `Agreement creates Obligation`, and `Measurement observes Property of Asset` communicate more than `has`, `contains`, or an unlabeled line. Define participant roles, direction, arity, inverse phrasing, cardinality, optionality, exclusivity, ordering, temporal applicability, derivation, and evidence.

Cardinality is a domain claim, not a database default. “Each order has exactly one buyer” might fail for joint purchase, anonymous sale, marketplace agency, or historical migration. Specify whether the rule applies at creation, acceptance, settlement, or current view. Unknown membership differs from prohibited absence.

Relationships can have their own identity, attributes, time, and evidence. Employment connects Person and Organization with position, interval, contract, status, and authority. Reifying such a relationship as Participation may be clearer than attaching changing fields to either participant. This is a semantic choice, not automatically a join table decision.

**Model n-ary situations when meaning requires them.** A Price may relate Product, Market, Currency, Customer Segment, Quantity Band, and Valid Interval. Decomposing it into binary relations can imply combinations that never existed. Model the situation or assertion as a concept with participants and constraints, then let logical design choose representation.

**Use attributes cautiously.** A conceptual property represents a meaningful characteristic, not a convenient column. Define value type, unit, scale, allowed values, time, provenance, authority, optionality, multiplicity, derivation, and sensitivity as relevant. If a property has identity, lifecycle, internal structure, multiple authorities, or relationships, it may deserve its own concept.

**Construct classifications deliberately.** Subtyping usually means every instance of subtype is an instance of supertype. State discriminator, necessary conditions, inheritance, disjointness, completeness, overlap, and evolution. Do not use subtypes merely to group a report or encode a temporary role.

`Person` and `Organization` may be disjoint subtypes of Legal Actor in one legal context. `Customer` and `Supplier` are often overlapping roles. `ActiveCustomer` is likely time-dependent classification. `Other` is not evidence that categories are exhaustive; it may hide an evolving or purpose-specific taxonomy.

W3C [OWL 2](https://www.w3.org/TR/owl-syntax/) provides formally defined classes, properties, individuals, axioms, and restrictions with explicit semantics. It can support inference and consistency analysis under chosen profiles and assumptions. Open-world reasoning, identifier semantics, profile restrictions, and modeling choices must be understood; an ontology reasoner does not discover missing domain facts or decide contested meaning.

**Represent time as meaning, not decoration.** Distinguish when a fact is valid in the domain from when it was recorded, corrected, or learned. Model events, intervals, states, effective dates, planned dates, uncertainty, sequence, and granularity. Ask whether a relationship can recur, overlap, be retroactively corrected, or remain unknown.

For “Alex lives at Address A,” clarify person identity, the meaning of lives at, household or mailing distinction, valid interval, assertion source, confidence, and recording time. A current-address field cannot answer historical eligibility or notification evidence without additional semantics.

**Separate facts, assertions, and beliefs.** Different sources may assert conflicting classifications. Instead of forcing one value, model Assertion with subject, predicate, value, source, authority, time, evidence, confidence, status, and adjudication. The governed current conclusion can coexist with original claims and later correction.

**Express invariants and derivations.** Natural-language rules should name quantification, scope, time, exceptions, authority, and consequence. Examples include “an accepted order must have at least one accountable buyer role” or “a withdrawal cannot take effect before the assertion exists.” Test whether rules are definitional, policy-imposed, empirically observed, or implementation-enforced.

Do not force all conceptual rules into one logic. UML multiplicity, first-order constraints, controlled natural language, decision tables, temporal logic, and executable checks have different expressiveness and reasoning costs. Select notations by stakeholder interpretation and risk. Preserve the authoritative prose and rule semantics when tooling is weaker.

The Object Management Group's [UML 2.5.1 specification](https://www.omg.org/spec/UML/) supplies class, association, generalization, property, and multiplicity constructs. UML can express useful conceptual models when stereotypes and conventions are governed. Its availability does not make class diagrams implementation-independent or semantically complete by default.

**Handle context explicitly.** A bounded context is a scope within which terms and rules have controlled meaning. Models can overlap without sharing identical concepts. Maintain mappings such as equivalent-under-condition, narrower, broader, transforms-to, references, or no-safe-map. State direction, loss, assumptions, authority, version, and intended use.

“Exact match” is a strong claim. Two concepts with similar definitions may differ by jurisdiction, time, eligibility, granularity, identity, or purpose. A many-to-one transformation may be appropriate for reporting but unsafe for operational decisions. Preserve the mapping's decision context.

**Distinguish conceptual, logical, and physical layers.** Conceptual models focus on domain meaning. Logical models organize information structures and constraints independent of a particular storage product, though they may choose paradigms. Physical models choose tables, columns, topics, files, indexes, partitions, encoding, placement, and performance mechanisms.

Leakage indicators include vendor names, table prefixes, surrogate keys, JSON layout, column types, indexes, partitions, storage paths, and API transport. Some implementation evidence can reveal domain concepts, but remove the mechanism from the conceptual assertion. Conversely, do not demand a conceptual box for every physical artifact such as retry queues or indexes.

**Connect, do not collapse, the layers.** Trace conceptual concepts and relationships to logical structures with mapping semantics, transformation, loss, version, and evidence. One concept may map to several logical representations; one aggregate may combine several concepts. Preserve unmapped technical state and justify it.

**Validate through scenarios and counterexamples.** Walk create, identify, relate, classify, change, correct, merge, split, dispute, delete, retain, transfer, recover, and retire scenarios. Use normal, boundary, invalid, ambiguous, historical, concurrent, cross-jurisdiction, and adversarial cases. Ask domain experts and affected stakeholders to decide example membership and explain disagreements.

Competency questions should be answerable from the model at its declared abstraction: Which agreements were valid when a benefit was denied? Can one organization act as buyer and supplier? Which source asserted the address? What happens when identity is split? A conceptual model need not contain data or query optimization, but it must make required meaning representable.

**Use machine checks without overclaim.** Validate stable identifiers, duplicate terms, undefined references, missing relationship roles, cardinality syntax, subtype cycles, disjointness contradictions, required metadata, and competency-query fixtures. W3C [SHACL](https://www.w3.org/TR/shacl/) defines shapes and validation conditions for RDF graphs. SHACL conformance is evidence about a data graph under a shapes graph, not proof that conceptual definitions reflect reality.

**Govern the model.** Assign semantic owners by bounded subject, not one universal committee. Record proposals, reviewers, evidence, decisions, dissent, effective versions, compatibility, downstream mappings, migration, and deprecation. Changes to meaning require impact analysis across requirements, policies, interfaces, data products, quality rules, lineage, metrics, access, retention, models, and historical interpretation.

A diagram export is not the authoritative model unless its source, semantics, status, and governance make it so. Store machine-readable and human-readable forms together when possible. Retain decisions and examples so future editors understand why distinctions exist.

## Definitions and Notation

Let a conceptual model be:

`C = (T, V, R, I, K, X, A, E)`

where `T` is entity/event/role types, `V` value types, `R` relationship types, `I` identity and identifier rules, `K` invariants and derivations, `X` contexts and mappings, `A` semantic authorities, and `E` sources, examples, decisions, and evidence.

For type `t`, let `Ext(t, x, c, τ)` mean that instance `x` is classified by `t` in context `c` at valid time `τ`. This makes classification contextual and temporal when required. It does not assert that every type is mutable or that all models use open-world semantics.

For relationship `r` with participant roles `p1...pn`, write `r(p1:x1,...,pn:xn,τ,e)` for an occurrence valid at time `τ` with evidence `e`. Cardinality constrains participating relationship occurrences under a declared scope and time, not the number of non-null foreign keys in one snapshot.

A context mapping is `m = (source, target, relation, condition, transformation, loss, authority, version, evidence)`. Equivalence requires stronger evidence than a usable directional transformation. Unknown mapping is not identity.

## Mechanisms, Invariants, or Proof Structure

Use nine gates to construct and assure a conceptual data model.

**1. Purpose gate.** Define decisions, stakeholders, competency questions, domain, scope, time, jurisdictions, sources, exclusions, and evidence threshold.

**2. Concept gate.** Register concepts with identity, category, definition, context, examples, counterexamples, authority, status, and use.

**3. Identity gate.** Specify sameness criteria, identifier schemes, issuers, validity, matching, ambiguity, merge/split, and decision authority.

**4. Relationship gate.** Define domain propositions, participant roles, arity, direction, cardinality, optionality, time, constraints, and evidence.

**5. Classification gate.** Check roles versus types, subtype criteria, inheritance, overlap, disjointness, completeness, and evolving categories.

**6. Time and assertion gate.** Represent events, states, valid/recorded time, provenance, conflict, uncertainty, correction, and derivation.

**7. Context gate.** Preserve bounded vocabularies and define directional mappings, conditions, loss, authority, versions, and unsafe cases.

**8. Challenge gate.** Run scenarios, examples, counterexamples, competency questions, invariants, structural checks, and stakeholder review.

**9. Governance gate.** Record decisions, dissent, versions, change impact, logical mappings, migration, deprecation, and review triggers.

The executable example checks four frequent modeling defects: missing concept scope, implementation leakage, an overloaded category presented as one type, and a relationship without cardinality.

<!-- bijux-verify: {"id":"conceptual-model-integrity","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"items=4\nvalid=0\nfindings=account:physical-leakage,customer:missing-scope,party:overloaded-category,resides-at:missing-cardinality\nready=false\n","stderr":""}} -->
```python
items = (
    {"id": "customer", "kind": "concept", "scope": "", "definition": "party in a buyer role", "physical": False, "cardinality": "n/a", "overloaded": False},
    {"id": "account", "kind": "concept", "scope": "billing", "definition": "unit for recording obligations", "physical": True, "cardinality": "n/a", "overloaded": False},
    {"id": "party", "kind": "concept", "scope": "contracting", "definition": "person, company, household, or account row", "physical": False, "cardinality": "n/a", "overloaded": True},
    {"id": "resides-at", "kind": "relationship", "scope": "eligibility", "definition": "person resides at place", "physical": False, "cardinality": "", "overloaded": False},
)

findings = []
valid = 0
for item in items:
    local = []
    if not item["scope"]:
        local.append("missing-scope")
    if item["physical"]:
        local.append("physical-leakage")
    if item["overloaded"]:
        local.append("overloaded-category")
    if item["kind"] == "relationship" and not item["cardinality"]:
        local.append("missing-cardinality")
    if local:
        findings.extend(f"{item['id']}:{finding}" for finding in local)
    else:
        valid += 1

print(f"items={len(items)}")
print(f"valid={valid}")
print(f"findings={','.join(sorted(findings))}")
print(f"ready={str(not findings).lower()}")
```

The checker validates four declared registry predicates. It does not prove that a scope is appropriate, a definition is accurate, cardinality holds in reality, categories are complete, identities are correct, stakeholders agree, or a model is fit for production. Those require authoritative sources, examples, counterexamples, scenarios, and domain validation.

## Alternatives and Trade-Offs

**Broad enterprise model versus bounded-context models.** A broad model supports discovery and shared direction but tends toward vague least-common-denominator terms. Bounded models preserve precise local meaning but need mappings. Use an enterprise semantic map over governed context models rather than demanding one universal schema.

**ER or UML versus ontology languages.** ER and UML are accessible and strong for structured relationships. OWL supports formal semantics and inference. Expressiveness increases modeling and computational obligations. Choose by competency questions, audience, interoperability, and assurance need.

**Natural language versus formal constraints.** Natural language supports domain participation but permits ambiguity. Formal constraints enable checking but can encode the wrong interpretation precisely. Maintain controlled definitions and formalizations with trace and examples.

**Entity-first versus event-first modeling.** Entity-first models clarify enduring identity and current relationships. Event-first models preserve chronology, causation, and evidence. Important domains often need both plus explicit state derivation.

**One authoritative concept versus preserved assertions.** A governed conclusion simplifies consumption. Preserving source assertions supports audit, uncertainty, and correction. Retain both when disagreement or provenance affects decisions.

**Minimal model versus comprehensive ontology.** Minimal models are teachable and decision-focused. Comprehensive models improve reuse but cost more and may introduce irrelevant commitments. Expand only from evidenced use and change impact.

**Strict standardization versus semantic translation.** Standardization reduces integration variation. Translation protects legitimate context. Standardize shared obligations and mapping contracts while leaving nonessential local distinctions autonomous.

## Failure Modes and Misconceptions

1. **The ERD is conceptual because it has no data types.** Table-shaped structure can still encode implementation assumptions.
2. **The label defines the concept.** Meaning requires definition, scope, authority, examples, and exclusions.
3. **An entity becomes a table.** Conceptual identity and physical persistence are separate choices.
4. **A foreign key proves a relationship.** It implements one representation, not necessarily the domain proposition or time semantics.
5. **Customer is a kind of person.** It is often a contextual role held by people or organizations.
6. **Identifier equals identity.** Identifiers have issuers, scopes, validity, errors, and lifecycle.
7. **Missing means optional.** Missing data can indicate unknown, not applicable, unavailable, withheld, or defective.
8. **Subtype lists are exhaustive.** State disjointness, completeness, overlap, and evolution explicitly.
9. **Exact match is harmless.** False equivalence propagates semantic error across contexts.
10. **Formal logic discovers truth.** Reasoning derives consequences of encoded axioms and semantics.
11. **One committee owns all meaning.** Authority is bounded by domain, policy, decision, and jurisdiction.
12. **A stable diagram needs no versioning.** Meaning, scope, sources, decisions, and mappings evolve.

## Worked Examples

### Example 1

A marketplace calls buyers, sellers, visitors, support contacts, and organizations `User`. The model introduces Actor, Account, Person, Organization, and time-bounded Buyer/Seller roles. Authentication Account no longer stands in for a legal actor, and one organization can act through several accounts without multiplying identity.

### Example 2

A hospital stores `admit_date` on Patient. Review distinguishes Admission event, Encounter episode, inpatient status, and recording timestamp. Retroactive correction can now change the recorded admission assertion without rewriting the event's original provenance.

### Example 3

A utility assumes one meter per premises. Boundary cases show meter replacement, shared buildings, mobile assets, and several meters measuring one service point. The model separates Meter, Installation, Service Point, Premises, Measurement Channel, and effective relationships.

### Example 4

Two systems share `Account`: one means contractual ledger; another means login credential. An exact mapping would authorize incorrect joins. The context map marks the concepts distinct and relates them only through a party-authorized servicing relationship.

### Example 5

A model makes Individual and Business exhaustive subtypes of Customer. Sole traders and public bodies violate the partition, while Customer is a role rather than a legal kind. The team models Legal Actor kinds separately and allows overlapping Customer roles under agreements.

### Example 6

An address model contains one current string. Eligibility needs residence during a benefit interval; delivery needs serviceability at dispatch; audit needs assertion source. Place, Postal Address, Residence, Delivery Destination, Assertion, and time are separated.

### Example 7

A product price is attached as one attribute. Regional currency, customer segment, quantity band, tax inclusion, campaign, and valid interval reveal an n-ary Pricing Assertion. The logical model may later optimize common cases without losing conceptual qualifiers.

### Example 8

An ontology reasoner reports no inconsistency. Competency review finds there is no concept for consent withdrawal, and the open-world model does not treat an absent permission as denial. Logical consistency remains true for the encoded ontology; privacy adequacy does not.

### Example 9

Identity matching merges two people using name and birth date. The conceptual model treats Match Hypothesis and Identity Decision as distinct, retaining evidence, confidence, authority, merge, challenge, and split. A reversible decision replaces an asserted metaphysical fact.

### Example 10

A schema migration renames `client` to `customer`, and leaders claim semantic alignment. Definitions show one includes prospects and the other requires an active agreement. The conceptual mapping is narrower-under-condition, so the interface adds qualification rather than relabeling rows.

## Cross-Program Connections

- **Database engineering:** conceptual meaning informs keys, dependencies, constraints, normalization, temporal structures, and physical design without being reducible to them.
- **Object-oriented programming:** classes, objects, values, roles, aggregates, and inheritance resemble modeling constructs but have different runtime and identity commitments.
- **Functional programming:** algebraic data types and pure transformations can encode distinctions and invariants after conceptual categories are established.
- **API and service engineering:** resources, commands, events, schemas, and compatibility rules need stable semantics and context mappings.
- **Data engineering:** pipelines, lineage, quality rules, master data, event processing, and metrics inherit conceptual identity and temporal meaning.
- **Knowledge graphs and AI:** vocabularies, ontologies, embeddings, retrieval, and model features require provenance, context, mappings, and limits on inferred equivalence.
- **Security and privacy:** identity, roles, purpose, sensitivity, consent, retention, and affected parties depend on precise distinctions and authority.
- **Systems engineering:** stakeholder views, information models, states, interfaces, scenarios, and lifecycle evidence provide broader system context.

## References

1. Chen, P. P.-S., “The Entity-Relationship Model—Toward a Unified View of Data,” *ACM Transactions on Database Systems*, 1(1), 1976. <https://doi.org/10.1145/320434.320440>
2. ISO/IEC, *11179-3:2023 Information technology—Metadata registries—Part 3: Metamodel for registry common facilities*, 2023. <https://www.iso.org/standard/78915.html>
3. Object Management Group, *Unified Modeling Language 2.5.1*, 2017. <https://www.omg.org/spec/UML/>
4. W3C, *SKOS Simple Knowledge Organization System Reference*, Recommendation, 2009. <https://www.w3.org/TR/skos-reference/>
5. W3C, *OWL 2 Web Ontology Language Structural Specification and Functional-Style Syntax, Second Edition*, Recommendation, 2012. <https://www.w3.org/TR/owl-syntax/>
6. W3C, *Shapes Constraint Language (SHACL)*, Recommendation, 2017. <https://www.w3.org/TR/shacl/>
7. W3C, *RDF 1.1 Concepts and Abstract Syntax*, Recommendation, 2014. <https://www.w3.org/TR/rdf11-concepts/>
8. ISO/IEC, *21838-1:2021 Information technology—Top-level ontologies—Part 1: Requirements*, 2021. <https://www.iso.org/standard/71954.html>

## Exercises

### Exercise 1

Create a conceptual model for a library loan domain. Distinguish intellectual work, edition, copy, digital license, person, organization, membership, borrower role, reservation, loan, renewal, return, loss, and fine. State identity, key relationships, time, and counterexamples.

### Exercise 2

Review the claim “Every customer has exactly one address.” Identify at least eight ambiguities or counterexamples, then propose concepts, relationships, scopes, and temporal qualifiers that support delivery and residency decisions separately.

### Exercise 3

Three contexts define `Active Account`: login within 90 days, nonzero balance, and an unexpired contract. Design directional mappings and explain why shared labels do not justify exact equivalence.

### Exercise 4

A subtype model says every Party is exactly one of Person, Organization, or Other; Customer and Supplier are subtypes of Person. Identify modeling defects and redesign kinds, roles, overlap, completeness, and context.

### Exercise 5

Design a conceptual-model review for an adverse-benefit decision. Include competency questions, identity, source assertions, valid/recorded time, affected stakeholders, authority, corrections, appeals, privacy, examples, counterexamples, formal checks, evidence limits, and change governance.

## Answers to the Exercises

### Answer 1

Model Work as the intellectual creation, Edition as a publication realization, Copy as a physical exemplar, and Digital License as a governed right to access an edition. Person and Organization have enduring identity criteria; Membership relates an actor to the library over an interval; Borrower is a role in Reservation and Loan. Reservation requests an eligible edition or copy under policy. Loan relates borrower role, lendable resource, checkout event, due obligation, renewals, return or loss, and applicable policy.

Identifiers include ISBN for editions under its scheme, barcodes for copies under library authority, member identifiers for memberships, and license identifiers from providers; none is universal identity. State valid and recording time for loans, renewals, returns, and corrections. An ebook access is not a physical Copy, a translation may be another Edition or Work under governed policy, a visitor is not necessarily a Member, and a Fine is an assessed obligation rather than the overdue state itself.

### Answer 2

Ambiguities include customer as person, organization, account, or role; address as place, postal designation, delivery destination, residence, billing destination, or contact string; permanent versus temporary; one versus several simultaneous addresses; historical versus current; household versus individual; unknown versus optional; international formats; homelessness or confidentiality; joint accounts; and address validity versus serviceability.

Model Actor, Agreement, Customer Role, Place, Postal Address, Residence, Delivery Destination, Address Assertion, and Delivery Eligibility. `Actor holds Customer Role under Agreement` is time-bounded. `Person resides at Place` has valid interval, source, confidence, and protection. `Delivery Destination designates Place` is evaluated for a shipment, carrier, time, and serviceability. Cardinalities and requiredness apply per decision context; neither absent residence nor multiple delivery destinations automatically violates the other.

### Answer 3

Create `RecentlyAuthenticatedAccount`, `BalanceBearingAccount`, and `ContractuallyActiveAccount` in their owning contexts, each with definition, authority, clock, effective interval, and evidence. A source concept may imply none, one, or several targets. For example, a contractually active account does not imply recent login or nonzero balance; recent login may occur after contract expiry; nonzero balance may persist on closed accounts.

Mappings should be directional predicates such as “qualifies for outreach when contract active and not suppressed” or transformations into a reporting category with explicit conditions and loss. Mark the three-way exact mapping unsafe. A shared display label is a homonym across contexts, not equivalence evidence.

### Answer 4

`Other` has no positive identity criterion and hides incompleteness. Person and Organization may not cover collectives, agencies, or jurisdiction-specific legal actors, and “exactly one” needs authoritative scope. Customer and Supplier are commonly roles held by Person or Organization, can overlap, and vary through time and agreement; making them Person subtypes excludes organizational customers and suppliers.

Define Actor or Legal Actor with locally justified kinds and explicit disjointness/completeness. Model Customer Role and Supplier Role as time-bounded participation in agreements or transactions. Allow one actor to hold both, state role-entry/exit rules and authority, and keep unknown or unclassified status explicit rather than forcing Other. Map jurisdiction-specific classifications rather than claiming universality.

### Answer 5

Frame questions such as who was the decision subject, which eligibility rule and version applied, which facts and source assertions were valid then, which identity resolution linked them, what evidence supported the outcome, and how correction or appeal changes it. Include decision subjects, applicants, representatives, caseworkers, policy/legal authority, data owners, privacy/security, accessibility, auditors, and affected groups.

Model Person, Application, Benefit Program, Eligibility Rule, Evidence Item, Source Assertion, Identity Hypothesis, Decision, Reason, Notice, Correction, Appeal, and Outcome with valid and recording time, versions, provenance, authority, uncertainty, and access. Test mistaken identity, conflicting income assertions, retroactive policy, missing data, duplicate applications, protected address, late correction, joint household, inaccessible notice, and successful appeal. Check identifiers, references, required roles, temporal order, rule/version trace, prohibited inference, and competency queries. Passing checks proves only encoded structure. Govern definitions, disputes, decisions, model versions, downstream mappings, privacy review, migration, and re-evaluation triggers.
