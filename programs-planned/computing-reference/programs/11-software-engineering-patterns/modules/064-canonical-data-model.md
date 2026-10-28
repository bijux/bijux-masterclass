---
module_id: SEPAT-064
program: Software Engineering: Patterns
level: 2
module_number: 64
title: Canonical Data Model
status: complete
last_verified: 2026-08-29
---

# Canonical Data Model

## One-Page Review

### Governing question

When should multiple systems integrate through a shared canonical semantic model, and how can that model reduce translation coupling without becoming a universal enterprise schema, lowest-common-denominator vocabulary, centralized release bottleneck, privacy leak, or hidden owner of every domain?

### Essential definitions

- A **Canonical Data Model (CDM)** is an application-independent integration vocabulary through which participating applications translate messages.
- A **bounded canonical model** serves one coherent domain/integration community with named scope and owners; it is not an organization's universal object model.
- A **source/target adapter** translates a participant's local contract to/from the canonical contract at an anti-corruption boundary.
- A **semantic concept** has a definition, identity, lifecycle, invariants, units/code systems, presence, provenance, ownership, and examples—not merely a field name.
- A **canonical envelope** standardizes cross-cutting message metadata; a **canonical payload** standardizes domain meaning. They can evolve separately.
- **semantic intersection** includes only meanings all participants share; **semantic union** includes every participant's concepts. Either extreme can be harmful.
- An **extension point** carries explicitly namespaced, governed noncanonical data without pretending it is universally understood.
- A **schema registry** stores versions and checks structural compatibility; it cannot establish semantic correctness.
- A **canonical version** is an immutable contract release with compatibility, migration, retention, and ownership evidence.
- **semantic drift** occurs when the same canonical term acquires divergent meanings across producers, adapters, consumers, or time.

### Central model, mechanism, or theorem

With $n$ systems that each require directed translation to every other system, pairwise mappings can reach

$$
E_{pair}=n(n-1).
$$

If every system has one inbound and one outbound adapter to a canonical model, the edge count is at most

$$
E_{canonical}=2n,
$$

so $n(n-1)>2n$ for $n>3$. This is only a topology count: canonical adapters may be more semantically complex, some pairwise edges may not exist, and governance/evolution costs can dominate.

Let local semantic domains be $L_i$, canonical domain $C_v$, encoders $e_i:L_i\rightharpoonup C_v$, and decoders $d_i:C_v\rightharpoonup L_i$. For a promised lossless local subset $L_i^*$, require

$$
\forall x\in L_i^*,\quad d_i(e_i(x))\equiv_i x.
$$

Cross-system success additionally requires that the canonical concept itself has one governed meaning; matching JSON shapes do not imply semantic commutativity.

### Critical invariants

- Scope is one named bounded domain/integration community with explicit non-goals and accountable semantic owners.
- Local systems retain their own domain models; adapters prevent canonical infrastructure concerns from leaking inward.
- Every canonical field/type has definition, identity/lifecycle, presence, units/code system, time semantics, provenance, privacy classification, and examples/counterexamples.
- Canonical IDs are stable, namespaced, collision/reuse governed, and traceable to authoritative local identity without erasing source provenance.
- Unknown, missing, null, empty, redacted, default, invalid, and unsupported states remain explicit.
- Version/schema evolution is additive or intentionally breaking under a compatibility matrix; wire compatibility never substitutes for meaning review.
- Translation loss at every local/canonical edge is declared, reviewed, measured, and reconciled.
- Security/purpose/tenant/jurisdiction rules prevent the canonical model from becoming an over-broad disclosure bus.
- Governance has bounded decision time, change ownership, deprecation, extension, incident, and emergency procedures.
- Adoption is incremental and reversible; no simultaneous rewrite or dual-authoritative business effect is required.

### Common failures

Common failures include a global enterprise schema, committee-owned nouns with no behavior/owner, mirroring one dominant application's database, lowest-common-denominator records, union-of-everything optional fields, generic `entity` and `status`, ID collisions, missing/null collapse, incompatible units/code systems, canonical events modeled as mutable entity snapshots, arbitrary extension bags, schema registry treated as semantic governance, release train bottlenecks, breaking changes hidden under optional fields, adapters leaking canonical types into domains, sensitive fields broadcast to every consumer, pairwise mappings surviving alongside canonical paths, and migration without parity/reconciliation/retirement.

### Compact example

Two invoice sources use cents integer and two-decimal text. Independent adapters produce the same canonical business projection—invoice ID, exact `amount_minor=12345`, and `EUR`—while retaining distinct provenance outside semantic equality. A source with three decimal places is rejected because the canonical minor-unit contract cannot represent it without rounding policy.

### Connections

[SEPAT-063](063-message-translator.md) establishes edge translation and loss accounting; [SEPAT-065](../ROADMAP.md) uses canonical content in routing policy. Canonical modeling connects to [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md), [Data Architecture Engineering](../../20-data-architecture-engineering/ROADMAP.md), [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md), and [Security Engineering](../../25-security-engineering/ROADMAP.md).

## Governing Question

How can a shared integration vocabulary reduce the number and inconsistency of mappings while preserving bounded domain autonomy, semantic precision, evolution speed, security, provenance, and operational accountability?

A canonical model is a coordination mechanism, not a technical file format. It moves coupling from many pairwise relationships into common concepts and governance. That trade is valuable only when participants genuinely share a stable semantic core and can operate its lifecycle.

## Why This Matters

As integrations grow, pairwise translators duplicate decisions about identity, status, money, time, and errors. One change can require many mappings, and two paths may interpret the same concept differently. A canonical vocabulary can centralize shared definitions and reduce edges.

Centralization can also magnify mistakes. A misleading `customer`, `amount`, or `active` field contaminates every adapter. A universal model can erase bounded-context meanings and force every team onto one release cadence. Production-grade canonicalization is deliberately scoped, governed, versioned, and empirically justified.

## Prerequisites and Retrieval

You should understand Message Translator, schemas/serialization, bounded contexts, anti-corruption layers, domain identity, events versus commands/documents, compatibility, schema registries, authorization/privacy, migrations, and organizational ownership. Retrieve these facts:

1. Two bounded contexts may use the same word for different concepts or different words for the same concept.
2. Local domain models optimize local decisions; an integration contract should not automatically replace them.
3. Wire/schema compatibility can preserve parsing while defaults, units, or meaning change.
4. A union of all source fields creates optionality and ambiguity; an intersection can omit essential distinctions.
5. Retained messages and historical replay extend compatibility obligations beyond currently deployed applications.
6. Central schemas expose data broadly unless channels, purposes, fields, and consumers remain authorized/minimized.
7. Fewer mapping edges do not prove lower total cost or better correctness.

## Learning Objectives

After completing this module, you should be able to:

- distinguish a bounded Canonical Data Model from a universal enterprise model, database schema, envelope standard, ontology, and local domain model;
- quantify pairwise versus canonical mapping topology while naming the model's assumptions and omitted costs;
- identify a coherent integration community and define canonical scope/non-goals;
- model concepts, identities, presence, money/units/time, code systems, provenance, events, and privacy precisely;
- design local anti-corruption adapters and explicit loss/extension policies;
- establish semantic ownership, schema registry, compatibility, governance, deprecation, and emergency change procedures;
- compare semantic intersection, union, modular core/extensions, consumer contracts, and pairwise mapping;
- migrate incrementally with shadowing, one authoritative path, reconciliation, rollback/forward, and retirement;
- verify adapters/model using contract, property, mutation, historical, differential, security, fault, load, and governance evidence;
- reject or constrain canonicalization where high-stakes meanings, autonomy, privacy, or change rates make it unsafe.

## Core Exposition

### Begin with an integration community

Name the business capability/domain, participating contexts, integration use cases, concepts actually exchanged, owners, consumers, change rates, retention, and prohibited uses. A canonical model for “commerce fulfillment events” can be coherent; “all enterprise data” rarely is.

Document non-goals: it may not model internal pricing algorithms, HR records, analytics-wide history, UI state, or every vendor extension. Non-goals prevent semantic sprawl and privacy creep.

### Respect bounded-context meanings

“Customer” can mean contracting party in billing, authenticated account in identity, recipient in fulfillment, or person receiving clinical care. Do not collapse them because names resemble each other. Map explicit relationships such as `billing_party_ref` and preserve context/provenance.

Use context maps and anti-corruption layers. The canonical model serves exchange; each context translates into local types and enforces its own invariants.

### Choose canonical granularity by message semantics

Model domain facts/commands/documents for integration use cases, not a giant mutable entity graph. `InvoiceIssued` states an immutable occurrence; `InvoiceSnapshot` is a document valid at a version/time; `IssueInvoice` is a command with one owner. They need different fields and delivery semantics.

Avoid canonical CRUD endpoints/messages whose optional fields mean “patch,” “unknown,” or “not relevant” interchangeably. Name intent and lifecycle.

### Define concepts beyond fields

Each concept record includes stable name/namespace, plain-language and formal definition, authoritative owner/source, identifiers, lifecycle/states, invariants, presence/cardinality/order, units/code system/version, time semantics, provenance/quality, sensitivity/purpose/retention, examples, counterexamples, and change history.

Machine-readable schema is one artifact. Human semantic documentation, test vectors, mapping/loss records, and governance decisions are equally durable contract evidence.

### Design identity explicitly

Do not assume every system's integer `id` shares a namespace. Canonical identity may be a namespaced source ID, authoritative master ID with crosswalk, or domain-generated stable ID. Define collision, merge/split, correction, deletion, reuse, aliases, and tenant/partition scope.

Preserve source identity/provenance even when a master ID exists. Identity resolution is often probabilistic/governed workflow, not a pure translator; false merges can be worse than duplicates.

### Model presence and knowledge

Canonical types must distinguish missing/not provided, explicitly null/not applicable, empty/known none, unknown code, unavailable, redacted, invalid, and defaulted. Do not force every participant to invent fake values for required fields it cannot know.

Conditional requirements can depend on message type/state/version. Document defaults as reader behavior and semantic meaning, not just schema syntax.

### Standardize quantities and money

Canonical values carry exact amount/value, unit/currency, scale/precision, measurement method/uncertainty where relevant, and rounding/conversion policy/version. Prefer canonical units only when conversion is exact or reviewed; retain original value/unit/provenance for regulated/scientific evidence.

Do not infer currency from country or units from field names. Dimensional validation rejects kilogram-to-pound mistakes and impossible conversions.

### Standardize time without flattening it

Separate occurred, effective, recorded, published, processed, and valid-from/to times. Use instants with precision and source clock/provenance; preserve zone/civil-time intent for schedules. Define interval boundaries, late events, corrections, and ordering/version relationships.

A canonical `timestamp` with no semantic role invites consumers to compare incomparable times.

### Govern code systems and enumerations

Identify code system, version, code, display/translation, and unknown/other semantics. Stable canonical codes should not mirror transient database enum ordinals. New source codes map to explicit unknown/quarantine or canonical extensions rather than ordinary defaults.

For clinical/scientific/legal taxonomies, terminology services and human governance may be required. Preserve original source code and mapping version.

### Balance intersection and union

The intersection of all local models is easy to share but may omit the distinctions that justify integration. The union captures everything but creates a sparse god schema no participant fully understands. Prefer a modular semantic core required by named use cases plus governed optional modules/extensions.

An extension is namespaced, typed, versioned, classified, size-bounded, and owned. An arbitrary JSON `attributes` bag bypasses compatibility, security, discoverability, and meaning review.

### Separate envelope and payload

A canonical envelope can standardize message ID, type/version, source, subject, tenant/partition key, occurred/recorded time, correlation/causation, content type/schema, trace linkage, and security classification. CloudEvents offers a general event-context model, but domain payload semantics remain yours.

Do not put mutable authorization tokens or every HTTP header into the envelope. Envelope evolution and payload/domain versions can differ; bind both explicitly.

### Keep local models autonomous

Local applications should not use generated canonical classes as their internal domain model by default. That imports integration optionality, version cadence, serialization annotations, and foreign concepts into business logic. Adapt at an explicit boundary.

Shared libraries can reduce mechanical duplication but may create synchronized deployment coupling. Prefer schemas/test fixtures and independently generated/implemented adapters where language/team autonomy matters.

### Define adapter obligations

Each local-to-canonical and canonical-to-local adapter declares supported versions, semantic mapping, loss ledger, identity/provenance, defaults, errors, authorization, deterministic reference versions, and compatibility. Validate both sides and reconcile outputs.

Adapters are owned jointly enough to avoid “integration team's guess,” but one team must be operationally accountable. Consumer contract tests must not freeze undocumented implementation quirks.

### Reduce edges honestly

The $n(n-1)$ versus $2n$ comparison assumes complete directed pairwise connectivity and bidirectional canonical adapters. Real systems form sparse graphs, some flows are one-way, and a canonical adapter may contain per-consumer variants. Count current/prospective mappings, changes, defects, and review cost rather than relying on asymptotics alone.

Canonicalization wins when concepts recur and remain coherent across many flows. Pairwise translation can be clearer for two systems or specialized semantics.

### Establish semantic governance

Name owners/stewards for each domain module and an accountable decision process. Define proposal template, impact analysis, domain/privacy/security review, compatibility evidence, decision deadline, dispute/escalation, versioning, deprecation, incident/correction, and emergency procedure.

Governance must be fast enough for product change. Measure lead time, breaking changes, adapter lag, default/unknown rates, semantic incidents, and deprecation completion. A committee with no authority or SLA creates shadow schemas.

### Use a registry but know its limits

A schema registry can identify schemas, enforce format-specific backward/forward/full compatibility, store references, and integrate CI. It cannot determine that `amount` changed cents to dollars, `active` changed meaning, or a new optional sensitive field is authorized.

Pair structural checks with semantic review, golden/counterexample vectors, classification/purpose metadata, adapter tests, and historical replay.

### Version for deployed and retained reality

Compatibility direction depends on who reads old/new data. Transitive checks matter when consumers replay long retention. Additive optional fields are only safe when old readers ignore them without changing correctness and new readers handle absence semantically.

Breaking changes use new type/major version or explicit migration. Keep old canonical versions/adapters until producers, consumers, retained messages, backfills, and recovery procedures no longer need them. Reserve removed field identifiers under the serialization format.

### Avoid synchronized release trains

Use compatibility windows and tolerant, semantically safe readers so producers/consumers deploy independently. Do not require every participant to upgrade for every canonical addition. Publish support matrices and active version telemetry.

If one invariant requires simultaneous change, coordinate explicitly or introduce an expand/transition/contract protocol with one authoritative meaning at each point.

### Secure and minimize canonical data

Classify every field and message type; authorize producer, consumer group, tenant, purpose, field, region, and administration. Separate channels/contracts when audiences/retention differ. A canonical superset must not be broadcast to consumers that need a subset.

Use purpose-built projections/content filters or distinct messages, encryption, tokenization, key rotation, retention/deletion, audit, and redacted observability. Extensions and provenance can contain sensitive source identifiers and need equal controls.

### Handle corrections and deletion

Canonical facts are not magically immutable truth. Model correction/supersession/retraction with stable lineage and target reconciliation. Define deletion/redaction/legal-hold semantics across retained logs, schemas, adapters, projections, quarantine, and backups.

Do not reuse identity after deletion or edit historical messages invisibly. Privacy deletion may require crypto-shredding/tombstone workflows whose analytical/audit consequences are reviewed.

### Migrate incrementally

Inventory pairwise flows, semantics, IDs, versions, effects, and owners. Select a coherent high-value concept, define canonical contract, build adapters beside one existing path, and shadow-compare without duplicate effects. Reconcile identities/counts/amounts/statuses/loss.

Cut over one producer-consumer flow with stable operation/message IDs and one authoritative effect path, canary, rollback/forward, and observability. Expand only after evidence. Retire old translators/channels/ACLs after drain and reconciliation; otherwise the architecture gains rather than removes mappings.

### Provide escape hatches without semantic anarchy

When a local concept is not canonical, choices are namespaced extension, specialized pairwise contract, new domain module, or keep it local. Record why and who owns it. Do not force urgent unsafe meaning into `metadata`.

Review extensions for promotion when several participants independently need the same stable concept. Remove/deprecate with retention evidence.

### Observe model health

Track schema/mapping versions, adapter support/lag, unknown/default/null/redacted/extension rates, loss categories, validation/quarantine, field usage, message size, compatibility failures, semantic incidents, governance lead time, deprecation age, pairwise bypasses, and reconciliation mismatches. Use bounded labels and privacy-safe traces.

Unused fields and always-populated extensions signal mismatch. Frequent breaking changes may reveal wrong boundaries; zero changes may reveal bypass/shadow schemas.

### Verify model, adapters, and governance

Validate schemas/references and compatibility matrices. Golden/counterexample tests reviewed by domain owners; property/metamorphic/round-trip tests for identity, units, presence, ordering, and invariants; mutation tests ensure incorrect mappings fail; differential/shadow tests compare paths; fuzz size/depth/unknowns.

Integration-test registry, serializers, channels, adapters, auth/privacy, old/new rolling versions, retained replay, corrections/deletion, quarantine/redrive, and crash/publish boundaries. Load-test largest permitted messages/extension and replay. Reconcile authoritative sources to canonical/downstream effects. Exercise governance proposal, emergency correction, deprecation, and disaster recovery—not just code.

### Review high-stakes canonical concepts separately

Clinical, financial, identity, safety, scientific, and legal concepts require domain-specific code systems, evidence/provenance, uncertainty, qualifiers, corrections, and access policy. A generic enterprise `Observation` or `Risk` can be dangerously vague.

Named experts and affected users validate each high-stakes module and operator workflow. If meanings cannot be unified safely, retain separate contexts and explicit translations.

### Executable model: two sources, one canonical invoice projection

This finite model adapts one integer-minor-unit source and one canonical two-decimal-text source into the same business projection. It preserves adapter-specific provenance separately and rejects unsupported three-decimal scale. It does not establish that invoices from real systems share identity or semantics.

<!-- bijux-verify: {"id":"canonical-invoice-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"a=accepted b=accepted semantic_same=True amount_minor=12345 currency=EUR\nbad=invalid reason=unsupported-scale\n","stderr":""}} -->
```python
CANONICAL_VERSION = "billing-invoice-2"


def parse_two_decimals(text):
    parts = text.split(".")
    if len(parts) != 2 or len(parts[1]) != 2:
        return ("invalid", None)
    return ("accepted", int(parts[0]) * 100 + int(parts[1]))


def from_system_a(source):
    return {
        "status": "accepted",
        "invoice_id": source["invoice_id"],
        "amount_minor": source["cents"],
        "currency": source["currency"],
        "canonical_version": CANONICAL_VERSION,
        "provenance": ("system-a", source["message_id"]),
    }


def from_system_b(source):
    status, amount_minor = parse_two_decimals(source["amount"])
    if status == "invalid":
        return {"status": "invalid", "reason": "unsupported-scale"}
    return {
        "status": "accepted",
        "invoice_id": source["invoice_ref"],
        "amount_minor": amount_minor,
        "currency": source["currency_code"],
        "canonical_version": CANONICAL_VERSION,
        "provenance": ("system-b", source["event_id"]),
    }


a = from_system_a({"message_id": "a-1", "invoice_id": "inv-7", "cents": 12345, "currency": "EUR"})
b = from_system_b({"event_id": "b-9", "invoice_ref": "inv-7", "amount": "123.45", "currency_code": "EUR"})
business_fields = ("invoice_id", "amount_minor", "currency", "canonical_version")
semantic_same = all(a[field] == b[field] for field in business_fields)
print(f"a={a['status']} b={b['status']} semantic_same={semantic_same} amount_minor={a['amount_minor']} currency={a['currency']}")
bad = from_system_b({"event_id": "b-10", "invoice_ref": "inv-8", "amount": "1.234", "currency_code": "EUR"})
print(f"bad={bad['status']} reason={bad['reason']}")
```

### Finite invariant argument

System A copies `12345`; System B splits `123.45` into integer parts 123 and 45, computing `123*100+45=12345`. Both adapters map local invoice reference to `inv-7`, currency to `EUR`, and version to `billing-invoice-2`; therefore the four-field semantic projection is equal. Their provenance tuples intentionally differ and are excluded from semantic equality while remaining preserved.

`1.234` has three fractional characters, so `parse_two_decimals` returns invalid and the adapter returns `unsupported-scale` without inventing rounding. The trace assumes nonnegative canonical numeric text, valid integer characters, two-digit currency scale, trusted IDs, and serialized execution. A production parser must handle signs/ranges/leading forms and validate schemas, identity correspondence, currency, authorization, provenance, and publication.

### Evidence classification

The snippet report is empirical evidence for two equal finite projections and one scale rejection. Arithmetic and equality are independently recomputable. It provides no proof that real local concepts are equivalent, IDs refer to one invoice, schemas are compatible, adapters are secure, or governance/migration/operations work.

## Definitions and Notation

Participating local semantic domains are $L_1,\ldots,L_n$, bounded canonical semantic domain at version $v$ is $C_v$, and adapters are partial $e_{i,v}:L_i\rightharpoonup C_v$ and $d_{i,v}:C_v\rightharpoonup L_i$. Each result includes provenance/loss or typed rejection.

Canonical concept $c$ is tuple $(name,definition,owner,identity,lifecycle,presence,units,codes,time,provenance,classification,invariants,examples)$. Schema $S_v$ encodes part of $C_v$; $S_v$-valid does not imply $C_v$-semantically valid.

Pairwise directed mapping graph has up to $n(n-1)$ edges under complete connectivity. Canonical star has inbound/outbound adapters up to $2n$. Total cost $K$ includes edge implementation plus semantic governance, adapter complexity, release/operations, migration, and incident cost; edge count alone is not $K$.

Semantic round-trip $d_i(e_i(x))\equiv_i x$ applies only on declared lossless subset. Cross-context projection equivalence $e_i(x)\equiv_C e_j(y)$ must state which canonical properties are compared and preserve different provenance.

## Mechanisms, Invariants, or Proof Structure

The mechanism has six owned layers: bounded semantic model/modules; machine schemas/registry; local anti-corruption adapters; message channels/envelopes; governance/control plane; and evidence/operations. A schema repository without domain ownership and adapters is not a CDM.

Core invariants are bounded scope, local autonomy, one definition/owner per canonical concept, stable namespaced identity/provenance, explicit presence/units/time/codes, version accountability, declared edge loss, authorized/minimized disclosure, compatibility across active/retained versions, and one authoritative effect path during migration.

The edge-reduction proof is arithmetic under complete directed connectivity: $n(n-1)-2n=n(n-3)>0$ for $n>3$. It does not prove cost reduction; counterexamples include sparse graphs, highly specialized semantics, and expensive governance. Semantic safety requires adapter proofs/tests on subsets plus reviewed canonical definitions. Current-state integration, historical replay, security, and organizational governance require empirical and human evidence.

## Alternatives and Trade-Offs

| Approach | Coupling locus | Strong fit | Main risk |
|---|---|---|---|
| Pairwise contracts/translators | Each system pair | Few/specialized integrations | Duplicate/inconsistent mappings |
| Bounded Canonical Data Model | Shared domain vocabulary | Many recurring coherent concepts | Central semantic/release coupling |
| Consumer anti-corruption model | Each consumer | Strong autonomy | Repeated interpretation |
| Producer-owned event contract | Producer domain | Authoritative facts | Consumer-specific demands leak in |
| Data product/domain contracts | Federated owners | Analytical/data sharing | Cross-product semantic mismatch |
| Shared database model | Storage schema | Controlled legacy/reporting | Ownership/security/evolution coupling |
| Ontology/knowledge graph | Explicit concepts/relations | Discovery/inference/interoperability | Governance/tool/reasoning complexity |
| Envelope-only standard | Cross-cutting metadata | Diverse payload domains | Does not solve payload semantics |

A portfolio is normal: canonical core for common commerce events, producer contracts for specialized facts, consumer anti-corruption at local boundaries, and pairwise mapping for exceptions.

## Failure Modes and Misconceptions

- **“Canonical means one model for the enterprise.”** Meaning is bounded; universal models erase contexts and autonomy.
- **“Fewer edges prove lower cost.”** Adapter/governance/migration complexity can exceed pairwise cost.
- **“Use the union of every schema.”** It yields sparse optional fields and no participant understands all combinations.
- **“Use only the intersection.”** It may omit essential distinctions and force out-of-band fields.
- **“Schema registry governs semantics.”** It checks structural rules, not meaning, units, privacy, or owner intent.
- **“Canonical classes should be domain classes.”** Integration types can contaminate local invariants and release cadence.
- **“Optional fields are backward compatible.”** Old readers may ignore a field essential to new correctness; new readers may misread absence.
- **“Extensions solve every exception.”** Arbitrary bags bypass contracts, discoverability, compatibility, and security.
- **“Master ID eliminates provenance.”** Source lineage remains essential for correction, audit, and false-match recovery.
- **“One `timestamp` is enough.”** Occurrence, effective, recorded, and processing times have different semantics.
- **“One canonical event can serve every audience.”** Data minimization, purpose, retention, and latency often require separate messages.
- **“Dual publish makes migration safe.”** It can cause duplicate/divergent effects without one authority and reconciliation.
- **“No schema changes means stability.”** Teams may bypass governance through shadow fields/channels.
- **“Canonical model is automatically DDD.”** A shared integration schema is not a bounded context's rich behavioral model.
- **“Technical agreement proves high-stakes meaning.”** Named domain and affected-user review remains required.

## Worked Examples

### Example 1

**Situation.** Five systems each maintain direct mappings to every other system.

**Reasoning.** Complete directed topology has 20 mappings; inbound/outbound canonical edges have at most 10. If invoice/customer meanings recur coherently, a bounded CDM may reduce duplication; measure adapter/governance cost.

**Conclusion.** Edge arithmetic motivates investigation, not automatic adoption.

### Example 2

**Situation.** Identity calls an authenticated account “customer”; billing means contracting legal party.

**Reasoning.** They are related, not identical. Model separate canonical concepts/relationships and source provenance; do not merge into generic `customer_id`.

**Conclusion.** Bounded meanings override vocabulary coincidence.

### Example 3

**Situation.** Canonical order schema is the union of 14 systems and has 480 mostly optional fields.

**Reasoning.** Valid combinations/invariants are unknowable and disclosure expands. Split by message intent/domain module, required semantic core, governed typed extensions, and specialized pairwise contracts where needed.

**Conclusion.** A union schema is not a coherent model.

### Example 4

**Situation.** A new optional `sanctions_blocked` field is ignored by old fulfillment consumers.

**Reasoning.** Wire compatibility exists but correctness does not. Introduce a version/protocol that prevents old consumers acting without required policy evidence, with rollout fencing and audit.

**Conclusion.** Semantically mandatory information cannot hide as technically optional.

### Example 5

**Situation.** Canonical amount uses decimal but omits currency and scale.

**Reasoning.** Adapters infer differently by country/tenant. Require exact value, ISO currency, scale/rounding/policy provenance and reconcile totals.

**Conclusion.** Canonical syntax must carry complete quantity meaning.

### Example 6

**Situation.** Every message includes the full canonical customer record for convenience.

**Reasoning.** Consumers receive fields beyond purpose, retention and consent differ, and stale snapshots proliferate. Publish purpose-specific minimized events/documents with references and authorized enrichment.

**Conclusion.** Canonical does not mean maximal payload.

### Example 7

**Situation.** Governance takes four months, so teams add unregistered fields inside `metadata`.

**Reasoning.** Shadow schema indicates governance failure. Set bounded proposal SLA, modular owners/emergency path, typed extensions with review, telemetry, and promotion/deprecation policy.

**Conclusion.** Operational governance quality is part of architecture correctness.

### Example 8

**Situation.** Migration dual-publishes direct and canonical messages to the same payment consumer.

**Reasoning.** Stable business/operation IDs and consumer dedupe help, but one path must be authoritative for effects. Shadow the other or route to comparison sink; reconcile before cutover.

**Conclusion.** Dual paths need explicit effect authority.

### Example 9

**Situation.** Canonical code `ACTIVE` merges active subscription, active user login, and active legal entity.

**Reasoning.** One generic lifecycle creates false implications. Define context-specific states and transitions; share only relations/facts truly common.

**Conclusion.** Generic status fields manufacture semantic drift.

### Example 10

**Situation.** A canonical clinical `observation.value` holds exact, ranges, censored values, qualitative results, and unknowns as one number/string.

**Reasoning.** Meaning and safety qualifiers disappear. Use reviewed typed alternatives with code system/version, unit, comparator/range, method, time, status/correction, provenance, and access policy—or keep contexts separate.

**Conclusion.** High-stakes concepts require precise domain modules, not generic enterprise containers.

## Cross-Program Connections

- [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md) develops boundaries, coupling, architecture decisions, governance, and evolutionary fitness.
- [Data Architecture Engineering](../../20-data-architecture-engineering/ROADMAP.md) develops domain data products, contracts, metadata, lineage, quality, and federated governance.
- [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) supplies message/API contract design, compatibility, idempotency, and consumer evolution.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) supplies classification, purpose/field authorization, tenant isolation, privacy, integrity, and audit.
- [Database Engineering](../../18-database-engineering/ROADMAP.md) grounds identity, schema migration, constraints, registries/stores, and reconciliation.
- [Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) provides contract, property, mutation, differential, historical, fault, load, and governance evidence.
- [SEPAT-063](063-message-translator.md) provides edge adapters; [SEPAT-065](../ROADMAP.md) routes on governed canonical content.

## References

1. Gregor Hohpe and Bobby Woolf, *Enterprise Integration Patterns*, Addison-Wesley, 2003. Canonical Data Model, Message Translator, Normalizer, and related integration patterns.
2. Enterprise Integration Patterns, [“Canonical Data Model”](https://www.enterpriseintegrationpatterns.com/patterns/messaging/CanonicalDataModel.html), accessed 2026-08-29. Pattern problem, solution, and relationships.
3. Eric Evans, *Domain-Driven Design: Tackling Complexity in the Heart of Software*, Addison-Wesley, 2004. Bounded contexts, context maps, ubiquitous language, and anti-corruption layers.
4. Martin Fowler, [“Bounded Context”](https://martinfowler.com/bliki/BoundedContext.html), 2014. Model boundaries and contextual meaning.
5. Clemens Vasters et al., [“CloudEvents Specification”](https://github.com/cloudevents/spec/blob/main/cloudevents/spec.md), current specification accessed 2026-08-29. Common event context attributes and protocol bindings.
6. JSON Schema, [“JSON Schema Core, Draft 2020-12”](https://json-schema.org/draft/2020-12/json-schema-core), accessed 2026-08-29. JSON schema vocabularies, identifiers, references, and validation architecture.
7. Apache Avro, [“Specification”](https://avro.apache.org/docs/current/specification/), current specification accessed 2026-08-29. Schemas, defaults, names, encoding, and schema resolution.
8. Confluent, [“Schema Registry API Reference”](https://docs.confluent.io/platform/current/schema-registry/develop/api.html), accessed 2026-08-29. Schema identity/version and backward/forward/full compatibility modes.
9. Martin Kleppmann, *Designing Data-Intensive Applications*, O’Reilly, 2017. Encoding/evolution, dataflows, streams, derived data, and distributed-system trade-offs.
10. Zhamak Dehghani, *Data Mesh*, O’Reilly, 2022. Domain-oriented data ownership, data products, self-service platform, and federated governance.

## Exercises

### Exercise 1

For six systems and a sparse set of nine directed integrations, compare pairwise and canonical topology/cost. Define evidence that would justify or reject a bounded canonical model.

### Exercise 2

Design a bounded canonical invoice-event module. Specify intent/types, identity, presence, money/tax, lifecycle, time, provenance, privacy, extensions, versions, adapters, loss, and invariants.

### Exercise 3

Design semantic governance and schema-registry workflow that supports independent deployment without allowing wire-compatible semantic corruption. Include metrics and emergency correction.

### Exercise 4

Plan incremental migration from direct order translators to a CDM. State shadow/canary/cutover authority, stable identity, compatibility, historical replay, reconciliation, rollback/forward, and retirement gates.

### Exercise 5

Review a proposed canonical clinical observation model. Cover code systems, values/units/qualifiers/ranges, presence/unknown, identity/time/provenance/corrections, privacy/purpose, accessible operations, verification, boundaries, and named human review.

## Answers to the Exercises

### Answer 1

Six fully connected systems would have 30 directed mappings; canonical in/out adapters at most 12. But current sparse graph has nine, so canonical increases nominal edges to 12 before retiring anything. Build a change graph: which concepts recur across edges, mapping defects/divergence, forecast integrations, change frequency, retained history, semantic overlap, adapter effort, governance/operational capability, security audiences, and migration cost.

Justify CDM if several flows repeatedly map the same coherent concepts, domain owners can define them precisely, projected edge/change/incident reduction exceeds governance/adaptation cost, and privacy/version autonomy can be preserved. Reject or limit it if concepts are specialized/context-conflicting, graph stays sparse/stable, one-way producer contracts suffice, central cadence is unacceptable, or canonical payload broadens access. Run one shadow vertical slice and compare semantic correctness, change effort, latency/size, incident diagnosis, and governance lead time before scaling.

### Answer 2

Bound scope to billing invoice facts, not order/payment/customer internals. Types include `InvoiceIssued`, `InvoiceCorrected`, `InvoiceCancelled`, and purpose-built `InvoiceSnapshot`; commands are separate. Envelope carries stable event ID/type/version/source/tenant, invoice subject, occurred/recorded time, correlation/causation, schema/content classification. Invoice identity is namespaced/stable with correction lineage/version; billing party is a scoped reference, not generic customer.

Money uses exact decimal/minor amount plus ISO currency, scale/rounding policy; lines have stable order/ID, quantity/unit, net/tax/gross and policy/tax jurisdiction/version with reconciliation `sum(lines)=totals` under stated rounding. Presence distinguishes missing, not applicable, known empty, redacted, unknown. Lifecycle transitions and correction/supersession are explicit. Provenance binds authoritative ledger/source, mapping/reference versions and loss. Privacy classifies party/address/tax fields and publishes minimized variants to authorized purposes.

Core has required shared fields; extensions are namespaced, typed, versioned, bounded, classified and owned. Immutable major/minor versions, compatibility matrix and registry checks pair with semantic vectors/review. Each adapter declares local/canonical versions, identity, exact arithmetic, statuses, errors and loss. Invariants validate tenant, currency, totals, line order, lifecycle/version/time and provenance; database/consumer reconciliation and domain/finance/tax/privacy review remain required.

### Answer 3

Proposal names concept owner, problem/use cases, precise definition/non-goals, schema diff, examples/counterexamples, identity/presence/units/time/codes/provenance, privacy/purpose/retention, producer/consumer impact, adapter/loss, compatibility matrix, migration/replay, test evidence, deprecation and rollback. Domain steward decides meaning; schema/platform validates format; privacy/security review exposure; affected producer/consumer owners review operations. Set decision SLA and escalation.

CI validates syntax/references, subject ownership, backward/forward/transitive mode appropriate to retention, generated old/new reader/writer matrix, golden/property/mutation/historical fixtures, classification metadata, and adapter contracts. Semantic review explicitly asks whether optional/default/enum/unit meaning changes despite wire compatibility. Registry IDs/checksums and immutable release decision are audited; instances expose active versions.

Metrics track proposal lead time, compatibility/semantic-review failures, adapter support lag, unknown/default/null/extension/loss, validation/quarantine, version skew, breaking changes, bypass schemas, deprecation age, and semantic incidents. Emergency correction can stop/fence affected types, publish signed corrected version/advisory, quarantine unsafe data, notify owners, reconcile/correct downstream, preserve evidence, and run post-incident governance review—not mutate old schema silently.

### Answer 4

Inventory direct sources/targets, schemas/semantics, IDs, channels, versions, ordering/delivery/effects, retained messages, auth/privacy, and owners. Select one coherent order fact, define CDM plus source/canonical and canonical/target adapters, and validate historical/adversarial fixtures. Shadow canonical outputs to a comparison sink while direct path alone causes effects; compare identities, counts, money, statuses, order, loss, size/latency, and privacy.

Canary one tenant/type: producer writes one stable outbox input; router/translator path uses same business/event IDs; only chosen path is authoritative at target while other stays shadow. Old/new schemas coexist under tested compatibility; persist mapping/canonical versions for in-flight/replay. Monitor outbox/channel/adapter/target effects and reconciliation. Roll back new inputs to direct authority without undoing observed canonical effects; forward-recover already accepted canonical obligations.

Expand after zero unexplained mismatches and acceptable capacity/governance. Historical reproduction uses recorded versions; intentional remap is a new authorized backfill with dedupe/checkpoint/comparison. Retire a direct translator/channel/ACL only when traffic drained, retained obligations handled, downstream effects reconciled, rollback/forward rehearsed, docs/on-call updated, and telemetry proves no callers. Never leave dual authoritative effect paths.

### Answer 5

Bound the module to one clinical integration community/use case; do not make one universal observation. Model patient/tenant/specimen/order/result/analyte identity; terminology code/system/version/display; value as typed exact decimal, coded, ordinal, text, range, ratio or quantity; comparator/censoring such as `<`/`>`; unit/system/version; reference range with population/method context; abnormal/critical flags; status preliminary/final/corrected/cancelled; collection/effective/recorded times with zone/precision; instrument/method/laboratory provenance; uncertainty/quality and correction/supersession lineage.

Presence distinguishes not measured, unavailable, unknown, not applicable, redacted and confirmed absent; never map them to normal/zero. Original source value/code/unit and mapping versions remain. Purpose-specific minimized messages and field/channel authorization enforce patient/tenant/professional/purpose/consent/jurisdiction; encrypt, audit, retain/delete under policy, and protect extensions/quarantine/provenance.

Accessible operator workflows display units, qualifiers, source/freshness, uncertainty, correction/conflict and unavailable states with keyboard/screen-reader/color-independent cues; provide time-bounded clinical escalation, not silent defaults. Verify official terminology/clinical vectors, dimensional/boundary/property/mutation, historical/differential adapter tests, schema compatibility, duplicates/gaps/corrections, authorization/privacy attacks, parser fuzz, crash/replay/load, reconciliation, accessibility, and disaster recovery. Named laboratory specialists, treating clinicians/pharmacists as relevant, clinical safety/informatics, terminology experts, patients/representatives, privacy/legal/regulatory, security, accessibility/human-factors, data/integration/SRE, and incident-response owners review real semantics. If meanings cannot be unified safely, retain separate models and explicit translators.
