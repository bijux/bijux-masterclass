---
module_id: SDDM-003
program: Software Engineering: Software Design & Domain Modeling
level: 1
module_number: 3
title: Domain Language and Terminology
status: complete
last_verified: 2026-08-30
---

# Domain Language and Terminology

## One-Page Review

### Governing question

How can a team build a precise, shared, context-bound language that expresses the domain faithfully enough to support decisions, models, code, tests, and operations without pretending that words have one universal meaning?

### Essential definitions

- A **concept** is a unit of knowledge formed from a combination of characteristics; a **designation** is a representation of a concept, such as a term, symbol, or name.
- A **term** is a verbal designation used for a concept in a specialized domain. A **definition** states the concept and distinguishes it from related concepts.
- A **referent** is an individual object, event, relationship, or situation to which a concept may apply.
- A **characteristic** is a property used to describe or distinguish concepts. **Essential characteristics** determine membership for the current modeling purpose.
- A **concept system** relates concepts by generic, partitive, associative, temporal, causal, or other domain relationships.
- **Synonymy** means multiple designations are accepted for one concept; **homonymy** means one designation denotes unrelated concepts; **polysemy** means one designation has related meanings.
- A **context** is the boundary within which a model and its language have a defined meaning. A **ubiquitous language** is a deliberately cultivated language shared by domain experts and developers inside such a context and used in conversation and software.
- A **glossary** records terms; a **domain language** also records distinctions, relationships, rules, examples, authority, and operational use.

### Central model, mechanism, or theorem

Treat every important vocabulary entry as a reviewable claim:

\[
L=(C,T,D,R,E,A,V),
\]

where \(C\) is context, \(T\) the preferred term and accepted aliases, \(D\) the intensional definition, \(R\) concept relationships, \(E\) positive and negative examples, \(A\) source and decision authority, and \(V\) version or validity interval. Language quality is demonstrated when these claims distinguish real cases, support the domain's decisions, and remain traceable into scenarios, model elements, interfaces, code, tests, telemetry, and migration rules.

### Critical invariants

- Define the concept before standardizing its spelling or choosing a class name.
- State the context for every meaning that could differ across teams, jurisdictions, products, or time.
- A definition must not be circular and must distinguish the concept from its nearest alternatives.
- Positive examples establish inclusion; near-miss and counterexamples establish the boundary.
- One concept has one preferred term inside a context unless an explicit migration is underway.
- One term must not silently denote two concepts inside a context.
- Different contexts may legitimately use the same word differently; translation is explicit at their boundary.
- Vocabulary changes are model and compatibility changes, not cosmetic edits.
- Automated checks can detect lexical inconsistency; domain experts remain responsible for semantic adequacy and authority.

### Common failures

Common failures include copying database or vendor vocabulary into the domain model; treating capitalization as semantic agreement; defining a term with itself; confusing a process, state, event, role, and record; allowing synonyms to become competing code concepts; forcing one enterprise-wide meaning across distinct contexts; translating by field name alone; leaving deprecated terms in APIs and telemetry indefinitely; turning a glossary into an unowned document; and assuming a passing linter proves the language matches reality.

### Compact example

A commerce team says an order is **placed** when the customer confirms intent. Payments says the order is placed only after funds are authorized. Fulfillment says it is placed when inventory is allocated. A global definition would hide three events. The team instead names `CheckoutSubmitted`, `PaymentAuthorized`, and `StockAllocated`, and defines `SalesOrder` separately from `FulfillmentOrder`. Boundary messages carry explicit event names and versions. The disagreement was not stylistic: it revealed distinct states, owners, timing, and failure behavior.

### Connections

Retrieve [problem and solution domains](001-distinguishing-the-problem-domain-from-the-solution-domain.md) and [stakeholders, goals, and observable outcomes](002-stakeholders-goals-and-observable-outcomes.md). Continue to [use cases, scenarios, and examples](../ROADMAP.md), then commands, queries, events, policies, rules, and invariants. Strategic context boundaries are developed in Modules 061–070.

## Governing Question

Teams often believe they agree because they reuse the same nouns. Yet a customer may mean the person receiving service, the finance system may mean the legal payer, and a database table named `customer` may contain login accounts. Conversely, two departments may use different words for the same regulated party. How can engineers turn this ambiguity into a language precise enough to reason with, while keeping the language corrigible as knowledge and policy change?

The answer is not “write a glossary once.” Language is part of the model. It selects concepts, draws distinctions, assigns names, and determines which facts can be stated. Those choices shape requirements, APIs, code, data, tests, alerts, reports, and organizational conversations. A weak language makes contradictions look like implementation defects. A strong language makes assumptions and disagreement inspectable.

## Why This Matters

Software can preserve a linguistic mistake with extraordinary consistency. If `active_customer` conflates a person with a current subscription, every schema, cache, metric, authorization rule, and report can reproduce the error. Tests may pass because they use the same mistaken fixture vocabulary. The defect appears only when a real person has two subscriptions, a subscription is sponsored by an employer, or a privacy request applies to a person rather than an account.

Terminology work separates a concept from the words used to designate it. ISO 704:2022 describes principles and methods for terminology work, while ISO 1087:2019 establishes core vocabulary for that discipline. The useful engineering implication is simple: changing a label does not necessarily change a concept, and changing a concept cannot be handled safely as a label-only edit.

Domain-driven design adds a software-design discipline: a model and its language are developed together, and the language is used in speech, diagrams, requirements, and code within an explicit boundary. Eric Evans calls this a ubiquitous language. “Ubiquitous” does not mean universal across an enterprise. It means routinely used and internally coherent within the context where the model applies.

Precision has operational consequences. A status named `complete` is dangerous unless the team can answer: complete according to whom, after which event, reversible until when, and with what evidence? A message named `CustomerDeleted` is dangerous if legal erasure, login disablement, contract termination, and analytical de-identification are different processes. Precise names expose lifecycle and responsibility.

Language is also an inclusion and power issue. The person who controls vocabulary can erase distinctions important to operators or affected people. Domain experts are not only executives; expertise can reside with frontline staff, customers, auditors, support teams, regulators, and people who experience exceptional paths. The language process records sources, conflicts, and decision authority rather than settling truth by seniority.

## Prerequisites and Retrieval

Before this chapter, you should be able to:

1. distinguish facts and goals in the problem domain from choices in the solution domain;
2. identify stakeholders by authority, expertise, impact, and exposure;
3. state an observable outcome without defining it as the chosen feature;
4. recognize that every model is selective and purpose-bound;
5. give positive and negative examples of a category from ordinary programming.

Retrieve a simple set concept. If \(P(x)\) is the membership predicate for concept \(K\), then a useful definition and examples should help reviewers decide whether \(P(x)\) holds for relevant cases. Most domain concepts are not reducible to one timeless predicate, but this framing exposes vague boundaries and hidden context.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish concepts, terms, definitions, designations, characteristics, and referents;
2. construct a context-bound concept system rather than an alphabetized word list;
3. write intensional definitions with genus and distinguishing characteristics;
4. use positive examples, near misses, and counterexamples to test a definition;
5. diagnose synonymy, homonymy, polysemy, overloaded status words, and category errors;
6. reconcile stakeholder language without erasing legitimate contextual differences;
7. reflect domain language in code and tests without forcing every spoken phrase into a type;
8. design translation and versioning when meanings cross boundaries or evolve;
9. automate bounded lexical checks while stating their semantic limitations;
10. review vocabulary for evidence, ownership, bias, exceptions, and operational consequences.

## Core Exposition

Begin with **concepts**, not words. A concept is a unit of knowledge selected for a purpose. The same referent can instantiate several concepts: one person may be a `Borrower` in lending, a `Member` in access control, a `Payer` in billing, and a `DataSubject` in privacy work. These are not four aliases for `Person`; each selects different relationships and rules.

A **term** designates a concept in a specialized language. A term entry should therefore point to a concept record rather than serve as the record's identity. This permits accepted aliases, historical names, translations, abbreviations, and display labels without duplicating the concept. Stable internal identifiers help when a preferred term changes.

Write an **intensional definition** by naming a broader concept and the characteristics that distinguish the narrower concept. “A premium member is a member whose currently effective agreement grants the premium benefit set” is structurally stronger than “a premium member is someone with premium status.” The first invites questions about effective time, agreement, grants, and benefit set; the second merely repeats the label.

An **extensional definition** enumerates members or narrower concepts. It works for a closed, governed set—such as the three permitted risk decisions—but becomes stale when the set is open. Enumerations in code do not prove that the domain category is closed. Ask who may add a case and how older consumers behave.

Definitions should be substitutable only with care. Natural-language definitions explain concepts; replacing every occurrence of a term with its definition can become unreadable or lose grammar. The engineering test is discriminative: can informed reviewers classify important cases consistently and explain disagreements from the stated characteristics?

Build a **concept system**. Generic relations express “is a kind of,” partitive relations express whole and part, and associative relations capture other domain connections. Add temporal, causal, responsibility, and state-transition relationships when they govern behavior. A flat glossary cannot show that a `Shipment` fulfills part of an `Order`, that a `Reservation` precedes allocation, or that a refund reverses a captured payment but not necessarily the sale.

Context comes before standardization. In a sales context, `Customer` may mean the party with whom a commercial relationship exists. In identity, `AccountHolder` may mean the controller of credentials. In support, `Requester` may include prospects. Forcing these into one `Customer` entity creates optional fields and contradictory lifecycle rules. Keep each model coherent and translate at boundaries.

Translation is a model, not a renaming table. Suppose sales `Customer` maps sometimes to billing `Payer`, while one payer can fund many customers and one customer can have several payers over time. A field-to-field mapper loses cardinality, validity, authority, and exceptions. A boundary contract states those semantics and rejects or escalates cases it cannot represent.

Language emerges through examples and disagreement. Ask domain participants to tell concrete stories, identify the objects and events, and challenge each noun and verb: Is this a thing, role, state, event, decision, policy, measurement, or document? What makes an example belong? What is the nearest non-example? When does it begin and end? Who decides? What evidence exists?

Avoid premature noun-to-class mapping. Some domain statements describe relationships, constraints, or processes better than objects. “A claimant may withdraw an undecided claim” contains a role, action, state condition, and policy. Creating classes named `Claimant`, `Withdrawal`, and `Undecided` before understanding identity and lifecycle can harden guesses into structure.

Use the language in executable artifacts selectively. Domain-significant types, functions, commands, events, tests, and error messages should use the preferred terms where doing so preserves meaning. Infrastructure vocabulary remains infrastructure vocabulary: `HttpClient`, `retryBudget`, and `BTreePage` need no theatrical domain synonym. Fidelity means recognizable correspondence, not abolishing technical language.

Tests are language probes. A test named “inactive customer cannot renew” is weak if `inactive` and `renew` are undefined. A scenario such as “a membership whose paid-through date has passed but whose 14-day grace period remains may renew without re-enrollment” exposes time, policy, and state. The example can reveal that `inactive` was one word for several conditions.

Record uncertainty rather than inventing consensus. Candidate terms, disputed definitions, open questions, and conflicting authorities should remain visible with owners and decision dates. An unresolved concept can block a high-risk implementation decision while low-risk exploration continues. False agreement is worse than an explicit gap.

Govern change. A concept record needs provenance, owner or decision forum, review trigger, introduced and deprecated terms, compatibility impact, and affected artifacts. Renaming `user` to `member` may be lexical. Splitting `user` into `AccountHolder`, `Operator`, and `DataSubject` is conceptual and requires data, API, authorization, analytics, and migration analysis.

Do not confuse conformance with adequacy. A terminology linter can require preferred terms and detect banned aliases. It cannot determine whether the preferred concept is the right one, whether a definition reflects law or practice, or whether an omitted distinction harms someone. Those claims require evidence and accountable human review.

The following executable example checks a small, explicit lexical policy. It detects duplicate preferred terms, alias collisions, circular single-term definitions, missing context, and deprecated words in sample artifacts. It does not understand meaning.

<!-- bijux-verify: {"id":"terminology-registry-check","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"concepts=3\npreferred_terms_unique=true\naliases_unambiguous=true\ndefinitions_non_circular=true\ncontexts_present=true\ndeprecated_hits=2\nhit=api:client\nhit=test:client\nsemantic_adequacy=not_proven\nevidence=lexical_policy_only\n","stderr":""}} -->
```python
concepts = [
    {
        "id": "sales.customer",
        "context": "sales",
        "term": "customer",
        "aliases": ["buyer"],
        "definition": "a party participating in an accepted sales relationship",
        "deprecated": ["client"],
    },
    {
        "id": "identity.account_holder",
        "context": "identity",
        "term": "account holder",
        "aliases": ["credential owner"],
        "definition": "a party authorized to control an identity account",
        "deprecated": [],
    },
    {
        "id": "support.requester",
        "context": "support",
        "term": "requester",
        "aliases": ["ticket reporter"],
        "definition": "a party who submits a support request",
        "deprecated": [],
    },
]

artifacts = {
    "api": "client submits order; customer receives confirmation",
    "test": "client without an accepted sales relationship is rejected",
}

preferred = [(c["context"], c["term"]) for c in concepts]
alias_owner = {}
alias_collision = False
for concept in concepts:
    for alias in concept["aliases"]:
        key = (concept["context"], alias)
        alias_collision |= key in alias_owner and alias_owner[key] != concept["id"]
        alias_owner[key] = concept["id"]

def circular(concept):
    words = concept["definition"].lower().split()
    return words == concept["term"].lower().split()

hits = []
for concept in concepts:
    for old_term in concept["deprecated"]:
        for artifact, text in artifacts.items():
            if old_term in text.lower().split():
                hits.append((artifact, old_term))

print(f"concepts={len(concepts)}")
print(f"preferred_terms_unique={str(len(preferred) == len(set(preferred))).lower()}")
print(f"aliases_unambiguous={str(not alias_collision).lower()}")
print(f"definitions_non_circular={str(not any(map(circular, concepts))).lower()}")
print(f"contexts_present={str(all(c['context'] for c in concepts)).lower()}")
print(f"deprecated_hits={len(hits)}")
for artifact, term in hits:
    print(f"hit={artifact}:{term}")
print("semantic_adequacy=not_proven")
print("evidence=lexical_policy_only")
```

## Definitions and Notation

Let a terminology entry be:

\[
e=(i,C,T,S,D,H,R,X,N,A,V),
\]

where:

- \(i\) is a stable concept identifier;
- \(C\) is the context;
- \(T\) is the preferred term;
- \(S\) is the set of admitted synonyms or aliases;
- \(D\) is the definition;
- \(H\) is the set of defining characteristics;
- \(R\) is the set of relationships to other concepts;
- \(X\) and \(N\) are positive examples and negative examples or near misses;
- \(A\) records sources, authority, and unresolved disagreement;
- \(V\) records version, effective time, and deprecation state.

For context \(C\), let \(\mu_C(t)\) map a designation \(t\) to a concept identifier. A useful lexical invariant is:

\[
\forall t,\; |\mu_C(t)| \le 1,
\]

unless ambiguity is explicitly represented and disambiguated. This is not a universal law of natural language. It is an engineering policy for artifacts where silent ambiguity creates defects.

Let \(P_{i,C}(x,t)\) mean that referent \(x\) satisfies concept \(i\)'s defining characteristics in context \(C\) at domain time \(t\). The time parameter matters: a person can be an eligible member today but not yesterday. Recorded time may differ from effective time; Module 071 later develops temporal models.

**Synonymy** is a many-designations-to-one-concept relation. **Homonymy** is one designation shared by unrelated concepts. **Polysemy** is one designation with related senses. In engineering, the diagnostic question is less “which linguistic category is philosophically perfect?” than “could a reader, consumer, or operator choose the wrong rule?”

A **controlled vocabulary** constrains accepted designations. A **taxonomy** organizes concepts, usually through broader/narrower relations. An **ontology** makes richer concepts, relationships, and constraints explicit. A domain model can use elements of all three without claiming philosophical completeness.

## Mechanisms, Invariants, or Proof Structure

Use this repeatable mechanism:

1. **Select the context and decision.** Name what work the language must support and what is outside scope.
2. **Collect utterances and examples.** Preserve who said them, in which situation, and with what authority.
3. **Extract candidate concepts.** Separate referents, roles, states, events, actions, policies, records, and measures.
4. **Build concept relationships.** Identify broader/narrower, whole/part, temporal, causal, ownership, and translation relations.
5. **Write discriminating definitions.** State a broader concept and essential characteristics; avoid circularity and accidental implementation detail.
6. **Test with examples.** Include ordinary cases, boundaries, near misses, exceptions, and historical cases.
7. **Choose preferred designations.** Record synonyms, prohibited or deprecated terms, spelling, and abbreviations after concepts stabilize.
8. **Reflect the language.** Apply it to scenarios, domain types, commands, events, tests, contracts, and operational views where appropriate.
9. **Review with accountable participants.** Resolve or preserve disagreements explicitly; do not vote away law, evidence, or disproportionate impact.
10. **Version and monitor.** Trace semantic changes, migrations, drift, and production evidence.

Four invariants govern the result.

**Concept identity invariant.** A concept's stable identity is not its preferred spelling. Renaming preserves \(i\); splitting or merging changes concept identity and requires explicit mappings.

**Context invariant.** Every assertion is interpreted within a named context. Cross-context equivalence is a claim with conditions, not an assumption from equal labels.

**Discrimination invariant.** Definitions and examples must distinguish the concept from its nearest alternatives for the decisions in scope. If experts classify critical cases differently, the disagreement is evidence to investigate.

**Traceability invariant.** Every domain-significant artifact either uses a governed concept or declares a boundary translation. Every concept important to a guarantee has scenarios, rules, and evidence—not merely prose in a glossary.

The correctness argument is conditional: if sources and authorities are credible, examples cover decision-relevant boundaries, definitions discriminate those examples, translations preserve required distinctions, and implementation artifacts conform, then the language supports the modeled decisions. It does not prove that the selected context is complete or morally legitimate. Those remain validation obligations.

## Alternatives and Trade-Offs

**Emergent language versus early standardization.** Letting language emerge preserves discovery; early standardization helps coordination. Freeze only what downstream compatibility needs, and keep uncertainty visible elsewhere.

**Local language versus enterprise vocabulary.** Local models can be precise and cohesive. Enterprise terms help reporting and integration but often collapse important distinctions. Prefer local truth plus explicit translation to one vague universal model.

**Natural language versus formal schemas.** Conversation carries nuance and evolves cheaply. Schemas and types enforce selected distinctions. Use both: natural language for discovery and explanation, formal artifacts for constraints that justify enforcement.

**Preferred term enforcement versus accepted synonyms.** One preferred term reduces code ambiguity. Synonyms support search, migration, multilingual teams, and stakeholder speech. Store aliases as designations of one concept; do not create duplicate model elements.

**Intensional versus extensional definitions.** Characteristics explain an open category; enumeration is exact for a closed set. A hybrid can define the rule and list currently recognized cases.

**Central curator versus distributed ownership.** A curator improves consistency but can become a bottleneck or impose distant meanings. Domain teams should own local concepts, with a cross-boundary forum for shared contracts and disputes.

**Strict linting versus advisory diagnostics.** Strict checks prevent known deprecated terms from reappearing but can block legitimate quoted, migration, or external-contract language. Scope rules by artifact, context, and effective version; allow reviewed exceptions.

**Translation versus shared kernel.** Translation isolates divergent meanings at a cost in mapping and operations. A shared model reduces translation but couples change and governance. Share only concepts whose meaning and lifecycle truly align.

## Failure Modes and Misconceptions

1. **“Everyone knows what it means.”** Ask for boundary examples; familiarity often hides disagreement.
2. **Dictionary definitions are sufficient.** General language rarely captures local authority, time, lifecycle, and exceptions.
3. **The database schema is the domain model.** It reflects storage and historical choices as well as domain distinctions.
4. **One noun deserves one class.** Concepts may be roles, relations, events, policies, or derived views.
5. **A shared word proves a shared concept.** Homonyms across contexts make this unsafe.
6. **Different words prove different concepts.** Synonyms and translations may designate one concept.
7. **Ubiquitous means enterprise-wide.** The language is ubiquitous inside its bounded modeling context.
8. **A glossary creates alignment.** Alignment requires use, examples, decisions, ownership, and feedback.
9. **Renaming is always cosmetic.** A rename can conceal a split, merge, policy change, or compatibility break.
10. **A linter validates meaning.** It finds declared lexical violations, not missing or false concepts.
11. **Experts cannot disagree.** They may observe different workflows, jurisdictions, times, or incentives.
12. **Technical words must be removed.** Technical concepts remain legitimate in the solution domain and at interfaces.

## Worked Examples

### Example 1

**Question:** Are `customer`, `account`, and `person` synonyms in a subscription service?

**Reasoning:** A person is a legal or natural party; an account is a credential and preference container; a customer participates in a commercial relationship. One person may control several accounts, an organization may be the customer, and an account may exist before purchase. Define each relationship rather than sharing one identifier.

**Conclusion:** Similar referents do not make concepts synonymous.

### Example 2

**Question:** Improve the definition “An active policy is a policy that is active.”

**Reasoning:** The definition is circular. Ask which effective interval, cancellation, suspension, payment, and jurisdiction rules matter. A candidate is: “a policy whose coverage interval contains the evaluation time and for which no effective termination or suspension excludes coverage under the governing contract.” Test reinstatement and retroactive cancellation separately.

**Conclusion:** A discriminating definition names characteristics and evaluation context.

### Example 3

**Question:** Sales and fulfillment both say `order`; should they share one object?

**Reasoning:** Sales owns commercial intent, price, and acceptance. Fulfillment owns allocatable lines, shipment, and delivery. Partial fulfillment and substitution mean cardinalities and lifecycle differ. Translate `SalesOrderAccepted v2` into one or more fulfillment orders under explicit rules.

**Conclusion:** Equal terms across contexts require semantic analysis, not automatic unification.

### Example 4

**Question:** A team uses `cancelled` for a booking before service and for a settled payment reversed later. What is wrong?

**Reasoning:** The word hides different events, authorities, accounting effects, and reversibility. Model `BookingCancelled`, `AuthorizationVoided`, and `PaymentRefunded`; define which workflow triggers each and which states remain possible.

**Conclusion:** Overloaded status words erase causal and lifecycle distinctions.

### Example 5

**Question:** Is “employee” an adequate concept for authorization?

**Reasoning:** Employment status alone may not grant access. Contractors, suspended staff, delegates, and service identities break the shortcut. Authorization needs roles, resources, purpose, organizational relationship, time, and policy evidence.

**Conclusion:** A familiar category must not substitute for the rule the decision actually needs.

### Example 6

**Question:** How should a multilingual team handle `invoice`, `factura`, and `Rechnung`?

**Reasoning:** Do not assume lexical translation proves conceptual equivalence. Compare legal function, tax requirements, issuance event, correction mechanism, and jurisdiction. Keep locale-specific designations and, where concepts differ, separate identifiers with a documented mapping.

**Conclusion:** Translation preserves concepts and differences, not merely words.

### Example 7

**Question:** The preferred term changes from `master account` to `controlling account`. Is this a rename?

**Reasoning:** If identity, relationships, and rules are unchanged, preserve the concept ID, deprecate the old designation, migrate user-facing and internal artifacts, and support compatibility where promised. If control is now time-bounded or shared, the concept changed and needs new semantics.

**Conclusion:** Determine conceptual change before selecting a migration strategy.

### Example 8

**Question:** The terminology checker reports no deprecated words. Is the language correct?

**Reasoning:** It proves only that scanned text follows the declared lexical policy. The registry may omit `DataSubject`, define `Customer` incorrectly, or encode a biased eligibility rule. Review sources, counterexamples, affected people, and production cases.

**Conclusion:** Lexical conformance is bounded evidence, not semantic validation.

### Example 9

**Question:** Support says a ticket is resolved when an agent closes it; customers say it is resolved when the problem no longer recurs.

**Reasoning:** Preserve `AgentClosed`, `CustomerConfirmedResolved`, and `Reopened` as events or observations. Define operational targets against the appropriate one and record cases where confirmation is unavailable. Do not force agreement by renaming all three `Resolved`.

**Conclusion:** Disagreement can reveal distinct observations rather than one bad definition.

### Example 10

**Question:** A benefits system must distinguish applicant, claimant, recipient, payee, representative, and household member. Is that overmodeling?

**Reasoning:** Each role has different eligibility, authority, payment, privacy, and appeal consequences; one person may hold several roles, and roles change over time. Model role assignments and effective intervals, then test minors, delegated representatives, shared households, and retroactive decisions.

**Conclusion:** Complexity is justified when distinctions change rights, rules, or evidence.

## Cross-Program Connections

- [Programming Languages & Semantics](../../01-programming-languages-and-semantics/ROADMAP.md) explains how syntax and semantic interpretation differ; domain terms likewise need an interpretation context.
- [Object-Oriented Programming](../../02-programming-languages-object-oriented-programming/ROADMAP.md) and [Functional Programming](../../03-programming-languages-functional-programming/ROADMAP.md) provide alternative representations for domain concepts and invariants.
- [API & Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) owns external contract representation and compatibility after domain distinctions are selected.
- [Data Architecture Engineering](../../20-data-architecture-engineering/ROADMAP.md) governs shared data semantics, metadata, and cross-domain information models.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) requires precise subject, principal, role, resource, purpose, and authorization vocabulary.
- [Systems Engineering](../../26-systems-engineering/ROADMAP.md) uses concept definition and interface terminology across disciplines and lifecycle artifacts.

## References

1. ISO. [ISO 704:2022 — Terminology work: Principles and methods](https://www.iso.org/standard/79077.html), fourth edition, July 2022. Consulted 2026-08-30.
2. ISO. [ISO 1087:2019 — Terminology work and terminology science: Vocabulary](https://www.iso.org/standard/62330.html), second edition, September 2019. Consulted 2026-08-30.
3. Eric Evans. [*Domain-Driven Design Reference: Definitions and Pattern Summaries*](https://www.domainlanguage.com/ddd/reference/), Domain Language, 2015. Consulted 2026-08-30. See the model, bounded context, and ubiquitous-language definitions.
4. Eric Evans. *Domain-Driven Design: Tackling Complexity in the Heart of Software*. Addison-Wesley, 2004, chapters 1–3 and 14.
5. Martin Fowler. [Ubiquitous Language](https://martinfowler.com/bliki/UbiquitousLanguage.html), 2006. Consulted 2026-08-30. Practitioner explanation of using model language in speech and code.
6. IEEE Computer Society. [Guide to the Software Engineering Body of Knowledge, Software Requirements topics](https://www.computer.org/education/bodies-of-knowledge/software-engineering/topics), SWEBOK v4.0a. Consulted 2026-08-30.
7. ISO/IEC/IEEE. [ISO/IEC/IEEE 29148:2018 — Requirements engineering](https://www.iso.org/standard/72089.html), second edition, November 2018. Consulted 2026-08-30.
8. W3C. [Data on the Web Best Practices: Data Vocabularies](https://www.w3.org/TR/dwbp/#dataVocabularies), W3C Recommendation, 31 January 2017. Consulted 2026-08-30. Official guidance on documented, shared, machine-readable vocabularies and term reuse.

## Exercises

### Exercise 1

Distinguish concept, referent, term, definition, characteristic, and designation using a library loan example.

### Exercise 2

Rewrite the circular definition “A priority incident is an incident with priority” and test it with two positive examples, one boundary case, and two near misses.

### Exercise 3

Diagnose a model in which `user`, `customer`, `account`, and `subscriber` are aliases for one database row. Identify likely failures and propose a concept system.

### Exercise 4

Design a translation between a sales context where `Customer` is a contracting party and a support context where `Requester` is anyone asking for help. Include cardinality, unknown cases, versioning, and failure handling.

### Exercise 5

A national emergency system uses `evacuated` to mean “notification sent,” “person left the danger zone,” and “person registered at a shelter.” Design a terminology review and model that works under incomplete observations and multiple agencies.

## Answers to the Exercises

### Answer 1

The concept `Loan` is the temporary, governed assignment of one lendable copy to one borrower. A particular loan of copy C17 to person P9 is a referent. “Loan” is the preferred English term and verbal designation; “checkout” may be an accepted local synonym or may instead denote the initiating event. A definition could be “an agreement state assigning a lendable copy to a borrower from checkout until return, loss closure, or another authorized termination.” Characteristics include copy identity, borrower role, start, termination condition, and governing policy. A barcode or stable identifier is another designation of a particular referent, not the concept's definition.

### Answer 2

A candidate definition is: “A priority incident is an incident whose assessed impact and urgency meet the currently effective P1 decision rule and require immediate incident-command activation.” Positive examples are a confirmed safety-control loss and a region-wide outage above the declared impact threshold. At the boundary, exactly the minimum affected population passes only if the rule uses \(\ge\), which must be stated. Near misses include a severe-looking alert disproved before assessment and a small isolated failure below the policy threshold. A strong answer identifies policy owner, effective version, evidence, reassessment, and the distinction between an incident's properties and the assigned response category.

### Answer 3

The single row conflates a person or organization, authentication account, commercial customer relationship, and subscription agreement. It fails for organizations with many accounts, one person with several subscriptions, prospects with accounts, sponsored subscribers, account compromise, contract transfer, and privacy requests. Model `Party`, `IdentityAccount`, `CustomerRelationship`, and `SubscriptionAgreement` with explicit identities, cardinalities, states, and effective intervals. Preserve legacy row identifiers as boundary designations during migration; do not use one ID as proof of conceptual identity.

### Answer 4

Sales owns `Customer = party participating in an accepted sales relationship`; support owns `Requester = party or channel that submits a support request`. A customer may create many requesters through employees or automated agents, and a requester may have no customer mapping. The translation therefore returns zero, one, or several candidate customer relationships plus evidence and confidence/authority—not an assumed one-to-one rename. Contracts carry stable concept and schema versions. Unknown or ambiguous mappings retain the support request and route entitlement-sensitive work for review rather than inventing a customer. Tests cover anonymous prospects, organizational delegates, closed relationships, merged parties, and version skew.

### Answer 5

Create distinct observations: `EvacuationNoticeAcceptedByChannel`, `DepartureObserved`, `DangerZoneExitConfirmed`, and `ShelterRegistrationRecorded`. Define their sources, coverage, latency, error modes, location and event identifiers, and effective times. Model `EvacuationStatus` as an evidence-backed assessment rather than one Boolean; unknown is not false and message delivery is not physical safety. Police, transport, shelters, telecommunications providers, and incident command retain their own contexts and translate through versioned event contracts.

Review positive cases, unreachable people, self-evacuation, cross-border movement, duplicate identities, device sharing, delayed shelter data, revoked orders, and people who cannot comply. Named emergency, legal, accessibility, privacy, field-operations, and affected-community representatives must review authority and consequences. Automated checks can validate schema, identifiers, provenance, time bounds, and forbidden equivalences; they cannot prove a person is safe or that the model is operationally adequate.
