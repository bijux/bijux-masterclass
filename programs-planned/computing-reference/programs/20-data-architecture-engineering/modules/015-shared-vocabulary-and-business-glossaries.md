---
module_id: DARCH-015
program: Data Architecture Engineering
level: 1
module_number: 15
title: Shared Vocabulary and Business Glossaries
status: complete
last_verified: 2026-09-03
---

# Shared Vocabulary and Business Glossaries

## One-Page Review

### Governing question

How can an organization create, use, and evolve shared vocabulary so that people and systems can interpret important concepts consistently while preserving legitimate contextual differences, sources, authority, uncertainty, language, and change history?

### Essential definitions

- A **concept** is a unit of knowledge established by a distinguishing combination of characteristics within a domain and context.
- A **designation** is a representation of a concept, such as a term, name, symbol, abbreviation, or code.
- A **definition** states the concept's distinguishing meaning within a declared scope; it is not merely a synonym, data type, or example.
- A **business glossary** is a governed collection of concept entries, designations, definitions, relations, usage rules, provenance, ownership, status, and mappings for one or more communities.
- A **controlled vocabulary** constrains permitted designations or values for a purpose and may include preferred, alternate, deprecated, and hidden labels.
- A **concept scheme** organizes concepts and their labels, notes, semantic relations, and mappings under a governed scope.
- A **bounded context** is a domain boundary within which a particular model and vocabulary have defined meaning and authority.
- A **semantic mapping** is an evidence-backed relationship between concepts or designations in different schemes, such as exact, close, broader, narrower, or related—not an unconditional claim of sameness.

### Central model, mechanism, or theorem

Represent a glossary concept entry as:

`G = (concept_id, scope, definition, designations, relations, rules, examples, authority, provenance, status, time, mappings)`

Represent a designation as:

`D = (lexical_form, language, locale, designation_type, acceptability, source, valid_time)`

Shared understanding does not require one word to have one enterprise-wide meaning. It requires that each material use resolve to a versioned concept in a known scope, that conflicting or narrower meanings remain explicit, and that mappings state their strength and permitted use. A glossary is fit only when its terms participate in decisions, contracts, models, controls, and tests—not when many entries merely exist.

### Critical invariants

- Concepts have stable identifiers independent of mutable preferred labels.
- Every definition states scope and distinguishes the concept from neighboring concepts without circularity.
- Terms, abbreviations, codes, translations, and aliases are designations of concepts, not the concepts themselves.
- Each designation carries language or notation, acceptability, source, and lifecycle status.
- Homonyms remain separate concept entries; synonyms and translations do not create duplicate concepts.
- Broader, narrower, partitive, associative, dependency, and mapping relations remain semantically distinct.
- “Exact,” “close,” “broader,” and “related” mappings are asserted only with evidence, purpose, authority, and version.
- Every approved entry has an accountable owner, steward, source, status, effective time, review trigger, and change history.
- Glossary terms trace to data models, schemas, policies, metrics, APIs, reports, and controls where the meaning is operational.
- Metrics measure use, coverage, ambiguity, conflict, change impact, and decision outcomes—not raw term count alone.

### Common failures

Common failures are defining words instead of concepts; copying dictionary prose without domain scope; writing circular definitions; treating examples as definitions; selecting one label and deleting legitimate local meanings; using a spreadsheet with no identifiers or history; confusing synonymy with equivalence; declaring all mappings exact; mixing class hierarchy with part-of structure; translating terms without translating concepts and usage; letting software field names become authoritative language; assigning nominal owners who never decide; publishing drafts as approved truth; changing definitions without impact analysis; and measuring success by entry volume or page views.

### Compact example

Sales defines “customer” as a party with an accepted order during the last 24 months. Support uses it for any party with an active support entitlement. Finance uses “customer” for a legal counterparty with an open receivable. An enterprise glossary does not force these into one vague sentence. It creates distinct Customer Purchasing Role, Support Entitlement Holder, and Receivable Counterparty concepts, records “customer” as a context-qualified designation for each, and maps them to the broader Party concept. Reports and APIs bind to the exact concept identifier and rule version. A cross-domain metric specifies which roles count, the observation date, exclusions, and owner.

### Connections

[DARCH-011](011-conceptual-data-models.md) defines conceptual boundaries, [DARCH-012](012-logical-data-models.md) formalizes structures, [DARCH-014](014-entities-relationships-and-business-keys.md) governs identity and relationships, and this module makes the language around those commitments explicit. [DARCH-016](../ROADMAP.md) will examine canonical models and their trade-offs.

## Governing Question

Words are overloaded, contextual, political, multilingual, and historically contingent. “Account” may mean a ledger container, login credential, customer arrangement, cloud tenancy, or sales target. “Active” can refer to authentication, subscription, billing, recent activity, legal status, or operational readiness. A shared glossary must make these meanings navigable without pretending the differences do not exist.

The governing problem is interpretation under responsibility. Who may define the concept? For which decisions does the definition apply? Which designation should a community use? How does the term map to schemas and policies? What happens when two contexts disagree? How do consumers learn that meaning changed? A list of prose answers none of these unless the glossary is connected to authority, evidence, operational artifacts, and lifecycle controls.

The goal is semantic coordination, not linguistic uniformity. Local vocabularies often encode real responsibilities. Architecture should identify common concepts where evidence supports them, preserve necessary contextual distinctions, and create explicit mappings at integration boundaries. Forced consensus can be as dangerous as ungoverned ambiguity.

## Why This Matters

Ambiguous vocabulary creates silent defects. Two teams can exchange a syntactically valid `customer_status` while interpreting different populations and state transitions. A regulator, finance team, and product team can calculate “revenue” from different recognition rules. A security policy can grant “owner” privileges while the source system means billing contact. These errors often pass schema validation because the field names and types align.

ISO 704:2022 describes [principles and methods for terminology work](https://www.iso.org/standard/79077.html), including relations among objects, concepts, definitions, and designations. ISO 1087:2019 supplies a [vocabulary for terminology work](https://www.iso.org/standard/62330.html). These standards support a crucial distinction: a lexical expression and the concept it designates are not interchangeable.

The W3C [SKOS Reference](https://www.w3.org/TR/skos-reference/) provides a common model for concepts, preferred and alternate labels, notations, documentation, semantic relations, collections, schemes, and inter-scheme mappings. It shows why a governed vocabulary requires more structure than a two-column term-definition sheet. SKOS is still a representation language; local correctness depends on domain authority and evidence.

A trustworthy glossary improves onboarding, model review, API and event design, catalog search, policy interpretation, metric reproducibility, data quality, interoperability, impact analysis, and audit. It also reveals disagreements early. Recording a disputed definition with owners and consequences is more useful than hiding it behind a broad sentence that every group interprets differently.

## Prerequisites and Retrieval

You should understand conceptual modeling, bounded contexts, identifiers, metadata, provenance, data catalogs, schemas, APIs, metrics, governance, language and locale, versioning, and change management.

Retrieve object, concept, characteristic, designation, term, proper name, symbol, notation, definition, intensional definition, extensional definition, context, domain, concept system, concept scheme, preferred label, alternate label, hidden label, abbreviation, synonym, homonym, polysemy, broader, narrower, partitive, associative, exact match, close match, source, authority, owner, steward, status, valid time, recorded time, deprecation, supersession, and traceability.

As a retrieval test, inspect the entry `active customer: a customer who is active`. Ask which concept “customer” denotes, what “active” means, the observation date, qualifying events or states, exclusions, authority, purpose, source, examples and counterexamples, related schemas, and change history. The sentence is grammatical but circular and unusable.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish concepts, objects, designations, definitions, codes, data elements, and glossary entries;
2. scope vocabulary by domain, community, decision, jurisdiction, language, and time;
3. write intensional definitions that distinguish neighboring concepts without circularity or hidden rules;
4. govern preferred, alternate, deprecated, hidden, abbreviated, translated, and symbolic designations;
5. model generic, partitive, associative, dependency, and rule relationships without conflating them;
6. create evidence-backed exact, close, broader, narrower, and related mappings across concept schemes;
7. assign ownership, stewardship, review, approval, dispute, exception, and change responsibilities;
8. connect glossary concepts to data models, fields, APIs, events, metrics, policies, controls, and catalog assets;
9. validate structural, semantic, linguistic, operational, and lifecycle quality with positive and negative evidence;
10. plan vocabulary migration, notification, compatibility, rollback, and retirement across consumers.

## Core Exposition

**Model concepts before labels.** A concept is the governed meaning; a term is one designation. Give the concept a stable identifier that does not change when the preferred label changes, a translation improves, or an abbreviation is deprecated. Otherwise links from schemas, reports, and policies break whenever editorial wording changes.

One term can designate several concepts. `Account` may point to Bank Account, User Account, Customer Account, or Chart-of-Accounts Entry. These are homonymous designations, not one concept with a very broad definition. Conversely, `client`, `customer`, and `buyer` might be alternate designations of one concept in a specific context, or they might identify distinct roles. Domain analysis, not string similarity, decides.

**Declare the vocabulary scope.** State domain, owning community, included decisions, excluded uses, audiences, jurisdictions, languages, source authorities, model versions, and lifecycle. “Enterprise glossary” is not a scope. An enterprise can host a federation of schemes with mappings and a small shared core rather than one undifferentiated namespace.

Bounded contexts are not excuses for chaos. Each context should define concepts precisely, and integration contracts should state mappings. Nor should the enterprise core absorb every local nuance. Promote a concept only when several contexts need the same meaning and governance can sustain it.

**Build a complete concept entry.** Record concept identifier, preferred designation by language and context, alternate and deprecated designations, definition, scope note, examples, counterexamples, distinguishing characteristics, broader/narrower/related concepts, rules, data and policy mappings, source, owning authority, steward, contributors, status, valid and recorded time, version, review date, change note, and open issues.

Not every entry needs equal detail. Risk and reuse determine depth. A label used only for catalog navigation may need less assurance than “eligible customer” in credit decisions or “personal data” in policy. Define quality profiles so critical concepts receive stronger evidence, approval, testing, and notification.

**Write definitions that distinguish.** An intensional definition commonly names a broader concept and the characteristics that distinguish the target. “A premium subscription is a subscription whose active agreement includes the premium service tier” identifies genus and difference, though the referenced concepts also need definition. An extensional definition enumerates members and is appropriate only when the set is governed and maintainable.

Avoid circularity: `active account` cannot be “an account that is active.” Avoid obscurity: do not define a common term solely through a more specialized undefined term. Avoid negative definitions when a positive boundary is available. Avoid embedding contingent procedure into timeless meaning; link the eligibility rule and version when the concept depends on calculation.

Use one definition for one concept. A sentence joined by “or” may conceal several concepts. State necessary and sufficient conditions only when domain authority warrants them. If the definition is descriptive rather than fully decisive, label the limitation and connect formal rules or examples.

**Test with examples and counterexamples.** Positive examples show intended inclusion. Counterexamples distinguish close neighbors. Boundary cases reveal uncertainty and rule gaps. For “fulfilled order,” test partial shipment, digital delivery, cancellation after shipment, replacement, return, and backorder. Ask which states and events matter at which time.

Examples do not replace definitions because they cannot enumerate every case. They provide evidence that reviewers share interpretation and support executable fixtures. Each example should cite the concept and rule version; otherwise a future change can make old examples misleading.

**Separate labels by role.** A preferred label is the chosen display or authoring designation in a language and scheme. Alternate labels support search and familiar usage. Hidden labels can support misspellings or legacy forms without endorsing them. Deprecated labels need replacements, effective dates, reason, and consumer guidance.

Do not use alternate labels to hide different meanings. If `subscriber` sometimes means newsletter recipient and sometimes paid service holder, create separate concepts. Search can present both with scope. Abbreviations need expansions and context; `AC` can mean alternating current, access control, or account. Codes and notations are governed designations, not definitions.

SKOS separates concepts from lexical labels and supports preferred, alternate, and hidden labels. It also constrains labeling combinations within language. Adopt such structures deliberately; a tool that stores multiple labels still cannot determine whether they are true synonyms.

**Handle language and locale as meaning-bearing context.** Translation is not word substitution. A target-language term may have broader, narrower, or culturally distinct meaning. Record language tag, locale if applicable, source, translator or authority, review status, definition in that language, and mapping strength. Do not declare an exact translation merely because a dictionary offers one word.

Multilingual review should consider legal terms, domain conventions, grammatical form, gender and inclusivity, abbreviations, search behavior, and right-to-left rendering where relevant. Machine translation can propose candidates but does not approve domain meaning. Preserve source and review evidence.

**Distinguish relation types.** Generic relations organize kind-of structure: Savings Account is a kind of Deposit Account under stated definitions. Partitive relations organize parts: Account Number is part of an Account Identifier representation, not a kind of Account Identifier. Associative relations connect concepts without hierarchy: Customer is related to Order.

Dependency and rule relations express additional semantics: Shipment requires a Destination; an Eligible Applicant satisfies an Eligibility Rule. Do not overload `related to` for every link or infer transitivity. A broader label can reflect classification convenience rather than formal subclass semantics, so state intended reasoning behavior.

Concept hierarchies need cycle, orphan, depth, multiple-parent, and disjointness review. Multiple parents may be correct. A cycle in a generic hierarchy usually signals definitional error, while cycles in associative relations can be harmless. Validators must know relation semantics.

**Keep vocabulary separate from data dictionaries.** A glossary defines domain concepts and language. A data dictionary describes data elements such as table columns, fields, formats, constraints, and owners. A catalog inventories datasets, APIs, reports, models, and other assets. These resources should link rather than collapse into one record shape.

A field named `cust_id` can implement or reference a Customer Account Identifier concept, but its physical type and nullability belong to the data dictionary. One concept may map to many fields; one field may combine or approximate several concepts. Mappings need transformation, scope, version, loss, evidence, and steward.

ISO/IEC 11179-3:2023 describes [registry common facilities](https://www.iso.org/standard/78915.html) involving identification, designation, definition, classification, and registration. The W3C [Data Catalog Vocabulary](https://www.w3.org/TR/vocab-dcat-3/) provides a vocabulary for cataloged resources and distributions. These are complementary: a glossary concept, a registered metadata item, and a cataloged dataset are related but not identical artifacts.

**Make business rules explicit.** A definition states meaning; a business rule constrains or derives business behavior. “Preferred customer” may be shorthand for a classification produced by a versioned rule. Do not bury threshold values, exception order, observation windows, or approval authority in a prose definition that cannot be tested.

The OMG [SBVR 1.5 specification](https://www.omg.org/spec/SBVR/1.5/) addresses business vocabulary and business rules with formal semantics and natural-language expression. Teams can borrow the discipline of separating noun concepts, verb concepts, and rules without adopting every formal construct. The key is traceability from wording to the operational rule and governed facts.

When a rule changes but the underlying concept does not, version the rule separately. When the concept boundary changes, version the concept definition and assess every mapping and consumer. A metric can keep its label while changing population or timing; that is a semantic breaking change even if dashboards still render.

**Record provenance and authority.** Every entry should say who asserted it, from which source, through what activity, when, and under which authority. Provenance is not an editorial footnote. It helps consumers distinguish a legal definition, industry standard, internal policy decision, domain convention, inferred mapping, and draft proposal.

The W3C [PROV-O Recommendation](https://www.w3.org/TR/prov-o/) provides concepts for entities, activities, agents, and provenance relations. A glossary can represent a definition version as an entity, the approval as an activity, and the owning council as an agent. The model does not prove that the authority was appropriate; governance must establish that.

Source precedence requires policy. A statutory definition may govern regulatory reporting while an internal operational definition governs routing. Do not overwrite one with the other. Record both scopes and the rule selecting them. If authority is disputed, expose the dispute and prohibit high-impact automated use until resolved.

**Assign ownership that can decide.** An owner is accountable for meaning and consequences. A steward maintains entries, evidence, workflow, and mappings. Subject-matter experts contribute knowledge. Data and system owners implement mapped controls. A governance forum resolves cross-boundary disputes. One person can fill several roles, but the decision rights should be explicit.

Define who may propose, review, approve, reject, supersede, deprecate, and retire. Require conflict-of-interest or specialist review where risk warrants it. Set service expectations for unresolved issues and emergency corrections. Ownership without time, authority, and escalation is merely a name in a field.

**Use lifecycle states.** Useful states include proposed, under review, approved, conditionally approved, disputed, deprecated, superseded, and retired. Draft entries should not silently appear as authoritative in code generation or policy. Disputed entries can remain discoverable with restrictions and competing proposals.

Separate valid time from recorded time. A definition approved today may become effective next quarter; a correction entered today can state that prior wording was wrong from an earlier date. Preserve immutable version history, change notes, approver, evidence, affected links, and notification. Never edit an approved definition in place without a new version.

**Map rather than flatten.** Two contexts can have overlapping but unequal concepts. State `exact`, `close`, `broader`, `narrower`, or `related` only after comparing definitions, populations, time, rules, and consequences. An exact mapping should support substitution for the declared uses; lexical similarity is insufficient.

SKOS distinguishes mapping properties and notes important semantic differences. Use the weakest mapping supported by evidence. `Customer` in sales may be broader than `Receivable Counterparty` because it includes purchasers with no open receivable. A crosswalk can define a transformation for one report without claiming conceptual equality.

Mappings need direction, source/target scheme and versions, owner, purpose, evidence, confidence or status, valid time, known loss, and tests. Review chains: if A is close to B and B close to C, A is not thereby exact with C. Automated mapping propagation requires explicit formal rules and safeguards.

**Connect vocabulary to operational artifacts.** Link concept identifiers to entity models, logical attributes, database fields, message fields, API resources, event types, policies, controls, quality rules, metrics, reports, machine-learning features, support playbooks, and training. State mapping kind: represents, identifies, classifies, measures, derives, constrains, or mentions.

A link alone is insufficient. Record version, transform, applicability, coverage, loss, and validation. A column may approximate a concept only for one country. A dashboard may label “active users” while calculating login events over 28 days. That derivation and observation window belong in the mapping and metric contract.

Operational links turn glossary changes into impact analysis. If a concept boundary changes, affected schemas, rules, consumers, tests, and communications can be found. Without these links, a glossary is a publishing site detached from the architecture it claims to govern.

**Design APIs and machine access.** Provide stable concept identifiers, content negotiation or explicit formats, version retrieval, language selection, search, relations, mappings, provenance, status, change feeds, and bulk export. Define availability, authorization, caching, pagination, rate limits, integrity, and recovery for glossary services used at runtime.

Avoid coupling critical transaction processing to an online glossary lookup when meanings can be version-bound at deployment. A registry can supply build-time validation and change notifications, while artifacts retain the resolved concept version. Runtime resolution may be appropriate for dynamic classification, but failure and stale-cache behavior must be explicit.

Machine-readable forms need human-readable definitions and vice versa. JSON, RDF, CSV, or database schemas encode structure; none guarantees reviewers understand the boundary. Preserve round-trip identity and versions across formats. Escape, Unicode, language tags, and multiline definitions require tests.

The [DCMI Metadata Terms](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/) demonstrate persistent terms with labels, definitions, comments, domains, ranges, and versioning context. Reuse established terms when their semantics fit; do not import familiar labels while changing meaning invisibly.

**Validate structural quality.** Check required identifiers, scope, definition, labels, language tags, owner, source, status, dates, and unique preferred label rules. Detect duplicate identifiers, exact duplicate definitions, unresolved references, invalid lifecycle transitions, prohibited label combinations, hierarchy cycles where relevant, orphan concepts, and dangling mappings.

Structural validity is necessary but weak. A complete form can contain a circular, politically compromised, or incorrect definition. Separate parser and schema checks from semantic, domain, linguistic, and operational review.

**Validate semantic quality.** Review concept unity, necessary distinctions, definition form, circularity, hidden assumptions, overlap, contradiction, relation correctness, mapping strength, examples, counterexamples, and fit for declared decisions. Compare against source authorities and adjacent concepts. Test whether independent reviewers classify boundary cases consistently.

Exact inter-annotator agreement is not always achievable, but disagreement is evidence. Investigate whether the definition, examples, task, training, or domain itself is ambiguous. Report sampling, reviewers, method, result, and limitations rather than declaring the vocabulary “clear.”

**Validate operational quality.** Trace critical concepts to actual schemas, metrics, policies, and workflows. Query whether mapped artifacts use approved versions. Test change notifications, deprecated-term search, compatibility, exports, recovery, and access controls. Inspect support tickets, incident reviews, model defects, and reconciliation failures for semantic causes.

Measure unresolved conflicts, stale reviews, unmapped critical assets, deprecated-term use, failed validations, time to decision, consumer acknowledgment, and outcome changes. High search traffic can mean usefulness or confusion. Low traffic can mean stability or irrelevance. Interpret metrics with qualitative evidence.

**Prevent automation overclaim.** Language models and similarity tools can suggest candidate definitions, synonyms, mappings, duplicates, and examples. They can also invent sources, flatten context, amplify historical bias, and generate fluent circularity. Record model and prompt versions, input authorization, output provenance, reviewer decisions, and prohibited uses.

No generated entry becomes approved solely because it passes style checks. High-impact concepts require accountable domain and policy review. Protect confidential definitions and identifiers from unauthorized model services. Evaluate multilingual and minority-context performance rather than assuming dominant-language quality transfers.

**Manage change as semantic migration.** A rename with unchanged concept identity differs from a definition change. A new alternate label can be additive; changing an exact mapping to close can invalidate joins; splitting one concept into two requires reclassification; merging concepts can erase distinctions. Classify the change before selecting compatibility strategy.

Inventory consumers and mapped artifacts. Define old and new identifiers/versions, coexistence, redirects, transformation, ambiguity, backfill, notification, acknowledgment, cutover, rollback, reconciliation, and retirement. Preserve historical interpretation. Do not relabel past events under today's definition unless the projection explicitly requests current semantics.

**Federate responsibly.** A central platform can provide identifiers, metadata model, workflows, search, APIs, validation, access, and change feeds. Domain teams should own meanings where expertise and consequences reside. An enterprise council governs shared concepts and mappings, not every local label.

Federation needs minimum interoperability rules: scheme identity, versioning, language, provenance, status, relation semantics, mapping categories, ownership, and notification. Local autonomy without these rules recreates silos; central control without domain authority creates unusable abstractions.

**Retire with evidence.** A term can remain searchable as deprecated while prohibited for new use. A concept can be superseded by one or several concepts. Record replacement mapping, effective date, reason, affected consumers, migration state, retention, and final retirement approval. Preserve versions needed to interpret historical contracts, records, and decisions.

Removal from the user interface is not retirement. Check code, schemas, configuration, queries, reports, model features, training, cached exports, documentation, and external consumers. A retired concept identifier should not be reassigned.

## Definitions and Notation

Let a glossary entry be:

`G = (I, S, F, D, R, B, E, A, P, Z, T, M)`

where `I` is stable concept identity, `S` scope, `F` definition, `D` designations, `R` semantic relations, `B` business rules and examples, `E` operational artifact links, `A` authority and ownership, `P` provenance, `Z` lifecycle status, `T` valid/recorded time and version, and `M` inter-scheme mappings.

For designation `d`, use:

`d = (form, language, locale, kind, acceptability, source, valid_time)`

Kinds can include term, proper name, abbreviation, symbol, notation, or code. Acceptability can include preferred, admitted, deprecated, or hidden under the scheme's policy. Two equal lexical forms do not imply equal concept identity.

Represent a mapping assertion as:

`m = (source_concept, target_concept, relation, purpose, evidence, authority, valid_time, versions, loss)`

where relation may be exact, close, broader, narrower, or related. Mapping acceptance is conditional on declared use. Transitivity is never assumed merely because several mappings share a label.

For a glossary dependency graph with concepts as nodes and definitional references as directed edges, a cycle is a review finding when it prevents grounding the involved definitions. This graph check can detect structural circularity; it cannot establish that acyclic definitions are true or intelligible.

## Mechanisms, Invariants, or Proof Structure

Use ten gates to design and assure a shared vocabulary.

**1. Purpose and scope gate.** Define communities, decisions, domains, languages, jurisdictions, consumers, risk, exclusions, and evidence threshold.

**2. Concept gate.** Identify concept, distinguishing characteristics, neighboring concepts, positive examples, counterexamples, and stable identifier.

**3. Definition gate.** Check scope, genus and difference where appropriate, referenced concepts, circularity, hidden rules, testability, and source.

**4. Designation gate.** Govern preferred, alternate, hidden, abbreviated, symbolic, coded, deprecated, and translated labels by language and context.

**5. Relation and mapping gate.** Distinguish generic, partitive, associative, dependency, exact, close, broader, narrower, and related claims with evidence.

**6. Authority and provenance gate.** Record owner, steward, source, contributors, approval activity, decision rights, conflicts, and limitations.

**7. Operationalization gate.** Trace concepts to models, fields, APIs, events, rules, metrics, reports, controls, and tests with mapping semantics.

**8. Challenge gate.** Test homonyms, false synonyms, circularity, overlap, boundary cases, multilingual differences, hierarchy cycles, mapping chains, and adversarial use.

**9. Lifecycle and change gate.** Govern proposal, review, approval, dispute, versioning, effective time, notification, coexistence, migration, rollback, supersession, and retirement.

**10. Outcome gate.** Measure coverage of critical uses, ambiguity, conflict, stale entries, mapping quality, deprecated use, decision latency, incidents, and consumer outcomes.

The executable example checks four narrow glossary-registry failures: a missing context, a circular definition, a missing accountable owner, and an unqualified equivalence mapping.

<!-- bijux-verify: {"id":"glossary-integrity","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"entries=4\nvalid=0\nfindings=customer:missing-context,order:circular-definition,revenue:missing-owner,subscriber:unqualified-equivalence\nready=false\n","stderr":""}} -->
```python
entries = (
    {"id": "customer", "context": "", "circular": False, "owner": "sales", "mapping": "none", "mapping_evidence": True},
    {"id": "order", "context": "commerce", "circular": True, "owner": "operations", "mapping": "none", "mapping_evidence": True},
    {"id": "revenue", "context": "finance", "circular": False, "owner": "", "mapping": "none", "mapping_evidence": True},
    {"id": "subscriber", "context": "media", "circular": False, "owner": "product", "mapping": "exact", "mapping_evidence": False},
)

findings = []
valid = 0
for entry in entries:
    local = []
    if not entry["context"]:
        local.append("missing-context")
    if entry["circular"]:
        local.append("circular-definition")
    if not entry["owner"]:
        local.append("missing-owner")
    if entry["mapping"] == "exact" and not entry["mapping_evidence"]:
        local.append("unqualified-equivalence")
    if local:
        findings.extend(f"{entry['id']}:{finding}" for finding in local)
    else:
        valid += 1

print(f"entries={len(entries)}")
print(f"valid={valid}")
print("findings=" + ",".join(sorted(findings)))
print(f"ready={str(valid == len(entries)).lower()}")
```

The checker validates four declared registry predicates only. It does not prove concept correctness, definition quality, source authority, linguistic adequacy, synonymy, mapping equivalence, hierarchy semantics, operational adoption, legal interpretation, or fitness for automated decisions. Those require domain evidence, authorized review, representative boundary cases, consumer tests, and lifecycle governance.

## Alternatives and Trade-Offs

**Central glossary versus federated schemes.** Centralization improves search, identifiers, workflow, and shared governance but can erase domain nuance and bottleneck decisions. Federation preserves ownership but requires interoperable metadata, mappings, and discovery. A shared platform with domain-owned schemes is often effective.

**Plain-language definition versus formal semantics.** Plain language supports broad review but permits ambiguity. Formal logic supports inference and consistency checks but adds skill and modeling cost and can formalize the wrong concept precisely. Use the degree of formality warranted by consequence.

**One preferred term versus multiple accepted terms.** One preferred designation improves consistency in authored artifacts. Alternate labels improve search, transition, and community acceptance. Too many admitted labels can preserve ambiguity; too few can make the glossary undiscoverable.

**Reuse versus local definition.** Reusing an external vocabulary supports interoperability and reduces reinvention when semantics fit. Local definitions preserve context when they do not. Import by stable identifier and version; do not copy a label while silently changing meaning.

**Exact mapping versus transformation.** Exact mapping simplifies substitution but requires strong equivalence evidence. Transformation can reconcile bounded differences while exposing loss and rules. Prefer honest close or directional mappings to convenient but false equality.

**Runtime resolution versus version binding.** Runtime glossary lookup supports dynamic updates but adds availability and semantic drift. Build or deployment binding improves reproducibility but needs change distribution. Choose by freshness, consequence, and recovery needs.

**Broad access versus restricted definitions.** Open access improves reuse and challenge. Some definitions, mappings, examples, or policies reveal confidential strategy or sensitive categories. Separate public concept metadata from protected evidence and operational rules where necessary.

## Failure Modes and Misconceptions

1. **A glossary is a list of terms and definitions.** Governed concepts also need scope, identifiers, relations, sources, authority, status, time, mappings, and operational links.
2. **One enterprise word should have one meaning.** Legitimate contexts can require distinct concepts linked by explicit mappings.
3. **A term is a concept.** Labels change and can be synonymous, homonymous, translated, abbreviated, or deprecated.
4. **A dictionary definition is sufficient.** General-language prose may not distinguish the domain boundary or decision rule.
5. **Examples define the concept.** They illustrate inclusion and boundaries but cannot replace a definition and rule.
6. **Broader means part of.** Generic, partitive, associative, and dependency relations have different semantics.
7. **Same label means exact match.** Lexical equality provides little evidence of conceptual equivalence.
8. **Translation preserves exact meaning.** Legal, cultural, and technical scope can differ across languages.
9. **A catalog field is the business concept.** Physical metadata and domain semantics are related through mappings, not identity.
10. **Approved means permanently true.** Meanings, authorities, laws, products, and decision needs change; versions and effective time matter.
11. **Ownership is an email address.** Effective ownership includes decision rights, review duty, escalation, and consequence accountability.
12. **More terms means more maturity.** Unused, duplicated, vague, or stale entries can increase semantic risk.
13. **Automation can approve obvious mappings.** Similarity proposes candidates; equivalence is a scoped domain claim.
14. **Renaming is always cosmetic.** A label change can affect code, search, training, policy, and external contracts.
15. **Deletion completes retirement.** Historical interpretation and consumer migration often require persistent identifiers and deprecated records.

## Worked Examples

### Example 1

Sales, support, and finance each use “customer” for different roles. The glossary creates three scoped concepts with one shared broader Party concept, context-qualified labels, exact operational rules, and close or related mappings rather than one vague enterprise definition.

### Example 2

An entry defines `active subscription` as “a subscription that is active.” Review replaces circularity with qualifying agreement state, service period, cancellation and suspension handling, observation time, rule version, examples, and counterexamples.

### Example 3

A bank glossary lists `account` once. Mapping reveals deposit accounts, loan accounts, user login accounts, and general-ledger accounts. Each receives a stable concept identifier; search retains the shared label and displays scope to prevent accidental joins.

### Example 4

An English `controller` privacy term is translated with a word that means technical operator in another language. Linguistic and legal review creates a jurisdiction-scoped designation and definition, maps it to the source concept as close rather than exact, and records the applicable policy authority.

### Example 5

A catalog says a column exactly represents Revenue. The column actually sums invoices at issue time, while the approved Revenue concept uses recognition events and excludes taxes. The mapping becomes an approximation for one report, and the misleading field is scheduled for migration.

### Example 6

A taxonomy records Engine broader than Automobile because the engine appears below automobile in navigation. Review changes this partitive relationship to part-of and prevents subclass inference that every engine is an automobile.

### Example 7

Two vocabularies both contain `subscriber`. One means any newsletter recipient; the other means a paid contract holder. String similarity suggests an exact match, but definition and population tests show overlap only. The approved mapping is related, with a transformation for one campaign use.

### Example 8

A policy definition changes next quarter. The glossary publishes a future effective version, notifies linked API and metric owners, tests coexistence, retains the current version for historical events, and blocks new artifacts from binding to the superseded version after cutover.

### Example 9

An automated tool proposes 400 synonyms from embeddings. Stewards sample by domain and find abbreviations, misspellings, related concepts, and several sensitive categories. Only reviewed candidates become alternate or hidden labels; the proposal model and decisions remain provenance.

### Example 10

A retired product category disappears from search, but historical reports use its code. The system restores the persistent concept record as deprecated, links its replacements, preserves validity, prevents new classification, and retains enough metadata to interpret old reports.

## Cross-Program Connections

- **Database engineering:** metadata registries, constraints, reference tables, search, temporal versions, and lineage persist glossary structures and mappings.
- **API and service engineering:** resource names, field semantics, error taxonomies, events, compatibility, and documentation should resolve to governed concepts.
- **Data engineering:** catalogs, schemas, metrics, quality rules, lineage, semantic layers, and transformations operationalize vocabulary.
- **Platform engineering:** registry services, workflow, policy, identity, APIs, change feeds, validation, and access controls enable federated governance.
- **Programming languages:** names, types, namespaces, deprecation, documentation, and static checks mirror lexical and semantic design concerns.
- **Security and privacy:** terms such as principal, owner, consent, personal data, and deletion require precise contextual meaning and authority.
- **Machine learning:** labels, features, target definitions, taxonomy mappings, annotation guidance, and drift depend on versioned concepts.
- **Systems engineering:** interface definitions, requirement terms, configuration items, traceability, authority, and change control require shared interpretation.

## References

1. ISO, *ISO 704:2022 Terminology work—Principles and methods*, 2022. <https://www.iso.org/standard/79077.html>
2. ISO, *ISO 1087:2019 Terminology work and terminology science—Vocabulary*, 2019, confirmed 2025. <https://www.iso.org/standard/62330.html>
3. ISO/IEC, *11179-3:2023 Information technology—Metadata registries—Part 3: Metamodel for registry common facilities*, 2023. <https://www.iso.org/standard/78915.html>
4. W3C, *SKOS Simple Knowledge Organization System Reference*, Recommendation, 2009. <https://www.w3.org/TR/skos-reference/>
5. Object Management Group, *Semantics of Business Vocabulary and Business Rules 1.5*, 2019. <https://www.omg.org/spec/SBVR/1.5/>
6. W3C, *Data Catalog Vocabulary (DCAT)—Version 3*, Recommendation, 2024. <https://www.w3.org/TR/vocab-dcat-3/>
7. W3C, *PROV-O: The PROV Ontology*, Recommendation, 2013. <https://www.w3.org/TR/prov-o/>
8. Dublin Core Metadata Initiative, *DCMI Metadata Terms*, current web edition. <https://www.dublincore.org/specifications/dublin-core/dcmi-terms/>

## Exercises

### Exercise 1

Create a complete concept entry for “active customer” in a subscription business. Include scope, distinguishing definition, terms, rules, examples, counterexamples, relations, mappings, owner, source, status, time, operational links, and review triggers.

### Exercise 2

Review a glossary where `account`, `user`, `member`, and `customer` are declared synonyms. Identify likely concepts and roles, propose a concept system, and state which mappings can and cannot be exact.

### Exercise 3

Design a multilingual terminology workflow for an eligibility policy used in English, French, and Arabic across two jurisdictions. Include translation, legal/domain review, language tags, definitions, mappings, effective time, disputes, and consumer notification.

### Exercise 4

Define structural, semantic, operational, and outcome validation for a 5,000-entry federated glossary. Include sampling, graph checks, boundary cases, mapped assets, deprecated use, metrics, and limitations.

### Exercise 5

Plan a semantic migration that splits one `Customer` concept into `Purchasing Party`, `Support Entitlement Holder`, and `Receivable Counterparty`. Cover identifiers, old/new mappings, schemas, APIs, metrics, history, coexistence, ambiguity, rollback, reconciliation, and retirement.

## Answers to the Exercises

### Answer 1

Create a stable concept identifier within the subscription-commercial scheme. Scope it to monthly business reporting and define Active Customer as a Party with at least one customer role linked to a subscription whose service entitlement is effective at the observation instant, is not terminated, and satisfies the approved suspension treatment. Link, rather than bury, the exact state and date rule. Exclude prospects, expired trials, canceled future subscriptions after their end, billing contacts with no customer role, and users of another party's subscription.

Record `active customer` as preferred English label, approved abbreviations or alternate labels, and deprecated legacy terms. Relate it to Party, Customer Role, Subscription, and Service Entitlement. Map it as close—not exact—to finance's paying counterparty if unpaid but entitled parties are included. Assign the commercial-policy owner and data steward, cite the agreement and metric specifications, mark the entry approved with valid and recorded time, and link fields, event states, metric code, dashboard, tests, and policy. Review on subscription-state, suspension-policy, jurisdiction, or metric changes and test new boundary cases.

### Answer 2

Likely concepts include Person or Organization, User Account, Membership, Customer Role, and possibly Contract Party. A user account is a credentialed system object; membership is participation in a group or program; customer is a commercial role; account can also mean financial arrangement or login record. One Party may hold several user accounts and memberships, while one organizational customer account may have several users.

Create separate stable concepts and named role relationships. Preserve each overloaded lexical form as a context-qualified designation. Exact mappings are possible only where definitions, populations, time, and purpose support substitution—for example, a legacy `member` field might exactly represent Membership under one program version. User and customer are usually related, not exact. Member may be broader or narrower than customer depending on program rules. Record unknown cases and test examples rather than forcing a universal hierarchy.

### Answer 3

Maintain one source concept identifier only if the policy meaning is truly shared; otherwise create jurisdiction-specific concepts and map them. Author definitions and rule references in each language, with BCP 47-compatible language tags and locale where required. Record preferred and alternate designations, source text, translator, legal and domain reviewers, approval, validity, and known non-equivalence.

Use bilingual or multilingual boundary cases: residency, age cutoffs, document status, exceptions, and effective dates. Legal review decides jurisdictional authority; linguistic review checks natural usage and ambiguity; domain review checks operational classification. A disputed translation remains proposed or disputed and cannot drive automated rejection. Publish future effective versions, notify policy engines, APIs, forms, training, support, and reporting owners, require acknowledgment for high-risk consumers, test old/new decisions, retain historical interpretation, and define rollback to the prior approved rule without erasing decisions already made.

### Answer 4

Structural checks cover stable IDs, schemes, required fields, language tags, preferred-label constraints, owners, sources, statuses, dates, valid transitions, unresolved references, duplicate records, hierarchy cycles by relation type, orphans, and dangling mappings. Semantic review samples by risk and domain, checks definition form, circularity, overlap, counterexamples, relation meaning, mapping strength, sources, and independent classification of boundary cases.

Operational checks trace critical concepts to actual schemas, APIs, rules, metrics, policies, and tests; detect mappings to superseded versions; test search, export, authorization, notifications, recovery, and machine interfaces. Outcome measures include critical-use coverage, unresolved disputes, stale reviews, deprecated-term usage, mapping rejection, incident contributions, time to decision, and consumer acknowledgment. Report sampling frames, reviewer expertise, agreement methods, inaccessible systems, and unreviewed languages. Passing graph and schema checks does not prove domain correctness or adoption.

### Answer 5

Preserve the old Customer concept identifier as a historical, then deprecated concept. Create three new stable identifiers with definitions, role and time semantics, owners, sources, examples, and rules. Map old Customer to each new concept as broader, related, or a documented transformation according to actual historical population; do not claim three exact replacements.

Inventory every mapped field, API, event, metric, policy, report, model feature, document, and external consumer. Add explicit role fields or resources, version contracts, and define how existing ambiguous records classify. Some need evidence-backed backfill; others remain legacy-unknown. Run old and new metrics in parallel, publish mapping and change feeds, collect consumer acknowledgments, and reconcile counts plus boundary cases. Cut over with one authoritative version per decision, retain adapters and historical evaluation, and define rollback that restores old consumption without deleting new evidence. Retire new uses of Customer only after producers and consumers migrate; preserve its versions indefinitely where required to interpret past records.
