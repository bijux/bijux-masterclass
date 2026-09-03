---
module_id: DARCH-051
program: Data Architecture Engineering
level: 2
module_number: 51
title: Master Data and Golden Records
status: complete
last_verified: 2026-09-03
---

# Master Data and Golden Records

## One-Page Review

### Governing question

How should an enterprise create and operate shared representations of customers, organizations, products, suppliers, locations, assets, and other core entities without erasing source authority, uncertainty, historical assertions, purpose, protection, or accountability behind the phrase “single source of truth”?

### Essential definitions

- **master data** describes durable, widely reused business entities whose identity and core attributes cross processes, applications, and analytical products.
- A **master-data domain** is a governed class of entities, attributes, relationships, decisions, owners, policies, and lifecycle rules, such as party, product, supplier, location, or asset.
- A **source record** is one source system's versioned assertion about an entity under that system's authority and context.
- A **master entity** links one or more source records believed to concern the same scoped real-world or institutional object.
- A **master identifier** is a stable identifier for the mastered entity; it does not replace source identifiers or prove identity by itself.
- A **cross-reference** maps a master identifier to source system, source record identifier, effective interval, status, and linkage evidence.
- A **golden record** is a governed, versioned representation selected or composed from source assertions for declared consumers and purposes.
- A **survivorship policy** determines which eligible assertions contribute to a golden attribute or relationship; detailed match and survivorship design follow in later modules.
- A **registry style** links and indexes source records while leaving most mastered values in source systems.
- A **consolidation style** copies, standardizes, matches, and publishes master views primarily for downstream consumption.
- A **coexistence style** synchronizes mastered values between a hub and participating systems under divided authoring rules.
- A **centralized transactional style** makes the master-data service authoritative for declared master mutations and distributes approved results.

### Central model, mechanism, or theorem

Represent master-data architecture as:

`G = (outcomes, domains, entities, sources, assertions, identity, policies, golden views, workflows, publication, protection, service, ownership, evidence, lifecycle)`

A golden record must preserve how each selected value was derived: source record, authority, effective and observation time, policy and rule version, confidence or decision, steward action, and prior version. “Golden” means fit for a declared use under current evidence, not ontological certainty. Some attributes remain authoritative in source domains; some become centrally authored; some are computed; some remain contested or multi-valued. The architecture must expose those distinctions rather than flatten them into one unexplained row.

### Critical invariants

- Every master-data domain has named decisions, entities, boundaries, authorities, consumers, value, harms, and lifecycle owners.
- Source records and identifiers remain traceable after linking, standardization, selection, correction, merge, split, and deletion.
- Master identifiers are stable within declared scope and never recycled across different entities.
- Golden attributes expose source, policy, version, effective time, status, and uncertainty appropriate to their consequence.
- Conflicting assertions are preserved or retired by explicit policy; absence, unknown, withheld, invalid, and not-applicable remain distinct.
- Registry, consolidation, coexistence, and centralized styles state who may author each attribute and how changes propagate.
- Match, merge, split, survivorship, hierarchy, stewardship, and override decisions are versioned, reviewable, reversible where possible, and auditable.
- Protection follows source values, standardized forms, linkage keys, cross-references, golden views, histories, exports, metadata, and backups.
- Publication defines contract, freshness, completeness, correction, deletion, compatibility, failure, reconciliation, and consumer migration.
- Retirement closes source feeds, authoring, identifiers, cross-references, APIs, events, files, histories, credentials, and retained obligations.

### Common failures

Common failures are calling every shared table master data; launching MDM without consumer decisions; treating a golden record as universally true; discarding source assertions after consolidation; assigning one authoritative source to every attribute by organizational politics; selecting the latest timestamp without clock and authority semantics; conflating entity identity with a preferred name or address; overwriting conflicts; forcing multi-valued relationships into scalar fields; recycling master IDs; merging entities without reversible evidence; propagating hub corrections back to sources that remain authoritative; allowing two systems to author the same field without conflict policy; publishing whole records when consumers need purpose-limited views; measuring success by records loaded; ignoring manual-review queues; replaying old source data with current rules into live masters; and decommissioning the hub while consumers, cross-references, or deletion duties remain.

### Compact example

Two records link to master party `party-100`. CRM asserts a verified email on day 5; billing asserts a newer but unverified email on day 7. Policy version 4 selects verified contact authority before recency, so the golden contact view publishes the CRM email with source, reason, effective time, and version. The billing assertion remains visible to authorized stewards and can trigger investigation. A marketing view may exclude the email if purpose or consent does not permit it. The master entity is shared; the published golden view is purpose- and policy-specific.

### Connections

[DARCH-017](017-event-schemas-and-information-models.md), [DARCH-018](018-temporal-and-historical-modeling.md), [DARCH-022](022-domain-boundaries.md), [DARCH-023](023-data-ownership-and-accountability.md), [DARCH-026](026-data-products-and-service-expectations.md), and [DARCH-050](050-mapping-data-workloads-to-platforms-and-serving-systems.md) establish information, ownership, domain, product, and platform boundaries. This module introduces the block; [DARCH-052](../ROADMAP.md) through DARCH-056 deepen reference data, identity resolution, match and survivorship, hierarchies, and stewardship workflows.

## Governing Question

Fragmented systems often hold different identifiers, names, classifications, addresses, statuses, and relationships for what appears to be the same customer, supplier, product, or asset. A centralized “truth” project can reduce duplication—or create a new opaque authority that broadcasts errors everywhere.

The governing question is which shared entity representation improves named decisions while preserving the evidence needed to explain disagreement, change policy, correct mistakes, protect people and organizations, recover from failures, and eventually migrate or retire the mastering system.

## Why This Matters

Microsoft's [Master Data Management in Microsoft Purview](https://learn.microsoft.com/en-us/purview/data-governance-master-data-management) describes publishing golden master-data assets into governed data products. IBM's [Data Concepts](https://www.ibm.com/docs/en/ws-and-kc?topic=data-concepts) distinguishes source records and composed entities and retains source identifiers. These provider models are useful mechanisms; they do not prove a golden record's fitness for a particular decision.

IBM's [InfoSphere MDM Technologies](https://www.ibm.com/docs/en/imdm/12.0.0?topic=overview-infosphere-mdm-technologies) distinguishes virtual, physical, and hybrid capabilities. Its [Persistence of the Golden Record](https://www.ibm.com/docs/en/imdm/11.6.0?topic=mdm-persistence-golden-record) describes survivorship criteria and persisted composite views. Architecture must choose authoring, storage, synchronization, and evidence boundaries from organizational needs, not from product terminology.

W3C [PROV-O](https://www.w3.org/TR/2013/REC-prov-o-20130430/) provides a vocabulary for provenance. The [OpenLineage object model](https://openlineage.io/docs/next/spec/object-model/) represents datasets, jobs, runs, and events. NIST's [Privacy Framework](https://www.nist.gov/privacy-framework/privacy-framework) addresses privacy risk management, Google's [Addressing Cascading Failures](https://sre.google/sre-book/addressing-cascading-failures/) covers overload and retry amplification, and NIST [SP 800-160 Volume 1 Revision 1](https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final) frames trustworthy lifecycle engineering. Master data combines identity, provenance, policy, operations, and consequence.

## Prerequisites and Retrieval

You should understand conceptual and logical models, bounded contexts, identifiers, source authority, temporal data, data products, quality, lineage, privacy, access control, APIs, events, consistency, recovery, and organizational governance.

Retrieve master data, master-data domain, entity, source record, assertion, master identifier, cross-reference, linkage, golden record, composite view, registry, consolidation, coexistence, centralized authoring, standardization, match, merge, split, survivorship, hierarchy, stewardship, override, provenance, publication, synchronization, and retirement.

As a retrieval test, inspect “create one customer truth.” Ask which kinds of customer or party, legal and household boundaries, decisions, source systems, attributes, authoritative operations, identifiers, histories, disagreements, purposes, protections, consumers, latency, error consequences, owners, and exit conditions apply. “One” and “truth” hide the architecture.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish master data, source records, master entities, cross-references, golden views, reference data, and transactional facts;
2. frame master-data domains from decisions, shared entities, source authority, reuse, consequence, and value;
3. model attribute-level assertions, provenance, effective time, confidence, policy, and uncertainty;
4. compare registry, consolidation, coexistence, and centralized transactional implementation styles;
5. define master identifiers, linkage, survivorship, overrides, versioning, and reversible correction boundaries;
6. publish purpose-limited master products through APIs, events, files, and analytical views with compatible contracts;
7. handle propagation, loops, conflict, latency, replay, reconciliation, recovery, and migration;
8. protect identities, linkages, derived sensitivity, consent, retention, deletion, and metadata;
9. assign domain, source, master-product, stewardship, platform, consumer, protection, and incident responsibilities; and
10. measure decision improvement, quality, queue health, adoption, risk, cost, and verified retirement.

## Core Exposition

**Start with shared decisions.** Name the processes and decisions harmed by fragmented entity identity or inconsistent attributes, their actors, deadlines, consequences, and fallback.

MDM is justified when a shared representation improves enough cross-system outcomes to fund its policy, stewardship, integration, and operational burden.

**Define the master-data domain.** Specify entity type, scope, lifecycle, attributes, relationships, identifiers, source systems, decisions, consumers, and owner.

“Customer” may mean legal party, account holder, user, household, prospect, beneficiary, or organization. Do not merge those concepts for convenience.

**Distinguish master from reference data.** Master data identifies durable entities with individual lifecycle and relationships. Reference data supplies controlled codes, classifications, units, and allowed values.

A product is master data; product category codes are reference data. Their governance connects but their identity and change patterns differ.

**Distinguish master from transactions.** Orders, claims, payments, visits, and readings record events or activities. Parties, products, locations, and assets participate in them.

Do not copy all transaction history into a golden record. Publish derived summaries separately with source and time semantics.

**Model source records as assertions.** A source record states that source $s$ observed or authored value $v$ for entity candidate $e$ under context, effective time, transaction time, status, and evidence.

Preserving the assertion lets the enterprise explain why a golden value changed and revisit a policy without reacquiring lost evidence.

**Separate record and entity.** A record is a source representation. A master entity links records believed to refer to the same scoped object.

One entity can have several legitimate records and one record can be ambiguous. Matching is an evidence-based decision, not a simple row collapse.

**Define master identity.** A master identifier needs namespace, entity type, issuer, creation event, version status, aliases, merge and split lineage, non-reuse, and resolution behavior.

It should not encode mutable meaning such as region, status, or category. Preserve source identifiers in cross-references.

**Treat cross-references as governed history.** Map master ID to source system, source record ID, effective interval, linkage status, rule or review evidence, and prior state.

Consumers may need to resolve identifiers as of a past time. Overwriting mappings breaks audit and correction.

**Define the golden view's purpose.** State which consumers and decisions it supports, included attributes and relationships, freshness, quality, uncertainty, protection, and service expectations.

One entity may have different legitimate views for fulfillment, compliance, analytics, support, and marketing because authority and permitted purpose differ.

**Reject universal truth claims.** A golden record is a current governed synthesis under sources, rules, and decisions. Sources can be wrong, late, incomplete, or context-specific.

Expose provenance and contested states. Confidence language must not imply certainty beyond evidence.

**Define attribute authority.** For each attribute, identify who may originate, verify, correct, override, expire, or delete it and under which context.

Legal name, shipping address, risk classification, preferred contact, and marketing segment can have different authorities and purposes.

**Preserve multiplicity.** People can have several names, addresses, roles, accounts, contact points, citizenships, or organizational relationships with types and intervals.

Forcing one “best” scalar can destroy valid context. A golden view may select a preferred value while the entity model retains the set.

**Model absence explicitly.** Distinguish unknown, not collected, not applicable, withheld, redacted, invalid, expired, disputed, and source unavailable.

Blank and null are not universal semantics. Golden selection and consumers need typed reasons.

**Version policies and outputs.** A master version binds source assertions, link set, standardization, match, survivorship, reference data, overrides, and policy versions.

Changing rules can change many entities without any source edit. Publish a new generation and preserve the prior explanation.

**Choose registry style deliberately.** A registry maintains identifiers, cross-references, linkages, and perhaps a dynamically assembled view while source systems retain mastered values.

It minimizes central copies but depends on source availability, latency, compatible access, and stable authority.

**Choose consolidation style deliberately.** Consolidation ingests source records, standardizes, links, selects, and publishes master views for analytics or downstream use.

Sources usually remain authoritative. Downstream corrections need a route to the right owner rather than silent hub edits.

**Choose coexistence style deliberately.** A hub and participating systems share authoring according to attribute and workflow rules, with synchronized changes.

Coexistence can improve operational consistency but creates loop, conflict, latency, and unknown-outcome hazards.

**Choose centralized transactional style deliberately.** The master service becomes authoritative for declared creation and mutation operations, and other systems consume its results.

This can clarify ownership but requires migration of business workflow, availability, latency, authorization, and recovery—not only data loading.

**Use hybrid styles by domain or attribute.** Product may be centrally authored while party identity is registry-based and supplier views are consolidated.

Document each boundary. “Hybrid” should not excuse ambiguous write authority.

**Separate standardization from identity.** Parsing, normalization, transliteration, address formatting, and code mapping improve comparison but can lose cultural or source meaning.

Keep original values, transformation version, locale, and errors. Equal normalized strings do not prove same entity.

**Separate matching from survivorship.** Matching decides which records belong to an entity. Survivorship decides which eligible assertions appear in a view.

A trusted source for identity may not be trusted for contact preference. Keep rule sets and evidence distinct.

**Make automated decisions reviewable.** Record candidate records, features or comparisons, thresholds, rule or model version, score, decision, uncertainty, and review path.

High-consequence merges and splits may require human confirmation, dual control, or delayed publication.

**Design reversible merge and split.** Preserve pre-merge identifiers, records, relationships, downstream aliases, source references, versions, and affected consumers.

A mistaken merge can expose one person's information to another. Correction must propagate quickly and verifiably.

**Use overrides carefully.** An override names attribute or linkage, value or decision, reason, evidence, approver, scope, effective interval, expiry, and precedence.

Permanent unexplained overrides hide policy defects. Review and retire them.

**Model hierarchy separately.** Parent-child, ownership, reporting, product composition, geography, and household relationships have types, sources, effective intervals, cycles, and confidence.

A single `parent_id` cannot represent every hierarchy. DARCH-055 develops this topic.

**Define stewardship workflows.** Route suspected duplicates, conflicts, missing authority, source errors, policy exceptions, hierarchy issues, and consumer disputes by domain and consequence.

Queues need priority, service objectives, evidence, separation of duties, escalation, workload limits, and closure reasons.

**Ingest through source contracts.** Define source record identity, schema, attributes, authority, event and transaction time, ordering, snapshots, changes, deletes, corrections, quality, and replay.

A successful load does not prove a complete or semantically stable source population.

**Establish snapshot-change handoff.** Initial bulk loads and ongoing changes need a compatible boundary so records are neither lost nor double-applied.

Record source epochs and positions. Reconcile after handoff at entity and attribute level.

**Prevent synchronization loops.** Tag change origin, master version, source position, workflow, and propagation intent.

If a hub publishes a value back to a source and then reingests it as new authority, versions can oscillate or overwrite better evidence.

**Resolve concurrent authorship.** Where multiple systems may write, define attribute ownership, command routing, conflict detection, precedence, rejection, compensation, and human escalation.

Last arrival is rarely a sufficient business rule. Clock order may not equal effective authority.

**Publish stable contracts.** APIs, events, files, and views expose master ID, source cross-references where authorized, attribute provenance, version, effective time, status, quality, and correction behavior.

Consumers declare whether they need full entity, purpose-specific view, identifier resolution, changes, or bulk snapshot.

**Separate commands from mastered facts.** A consumer requests a correction or relationship change through an authorized command. The master service validates ownership and publishes the accepted fact.

Direct target-table patches bypass policy, provenance, events, and downstream correction.

**Define freshness by attribute and use.** An entity can contain a legal name confirmed yesterday, a risk status from minutes ago, and an address pending review.

One record timestamp hides mixed freshness. Expose relevant source and master versions.

**Plan for incomplete entities.** Define minimum publishable attributes, provisional status, missing reasons, quality, consumer fallback, and later enrichment.

Rejecting every incomplete entity can erase important populations; accepting silently can create unsafe decisions.

**Reconcile sources, hub, and consumers.** Compare source records, cross-references, entity memberships, selected attributes, deletes, positions, versions, and consumer acknowledgements at compatible cutoffs.

Aggregate counts cannot detect wrong merges or values. Sample and keyed evidence are necessary.

**Design correction propagation.** A source correction, steward split, policy change, consent update, or deletion can affect golden views, caches, indexes, warehouses, models, reports, and external consumers.

Publish stable correction identity and affected versions. Track completion by consequence.

**Protect linkage as sensitive data.** Connecting accounts, devices, addresses, family members, employers, and transactions can create sensitivity beyond each source record.

Hashing identifiers does not remove linkability. Restrict cross-references, match evidence, histories, and graph relationships.

**Apply purpose limitation to views.** A support agent, fraud investigator, analyst, supplier manager, and marketing system need different attributes and relationship scope.

Avoid distributing the full golden record by default. Minimize at the publication boundary.

**Propagate consent and legal constraints.** Record purpose, lawful basis or authority where applicable, consent state, retention, holds, deletion, licensing, and geographic restrictions.

Conflicting obligations require qualified governance. MDM software does not decide legal interpretation.

**Audit human and automated changes.** Capture who or what changed source mapping, entity membership, preferred values, overrides, policy, export, or access, with before and after versions.

Protect audit evidence from unauthorized editing and excessive exposure.

**Set service objectives at consumer boundaries.** Define identifier resolution latency, master publication freshness, update completion, queue age, API availability, batch release, reconciliation, and correction time.

System uptime alone does not prove master data is current or fit.

**Control capacity and backpressure.** Bound source bursts, matching work, large entities, stewardship queues, bulk exports, replay, consumer fan-out, and retries.

Prioritize urgent splits, protection changes, and critical corrections over low-consequence enrichment.

**Design degraded modes.** Decide whether consumers use last-known master state, source fallback, partial view, queued command, or fail closed when the hub or a source is unavailable.

Fallback to sources can overload them and reintroduce inconsistent identity. Test it.

**Recover evidence before publishing.** Restore source contracts and positions, master IDs, cross-references, link decisions, assertions, policies, overrides, histories, and consumer versions in compatible order.

Rebuilding only current golden rows loses explanation and can select different results.

**Replay in isolation.** Pin source boundaries, standardization, match and survivorship rules, reference data, code, policy, and target namespace.

Compare memberships, attributes, uncertainty, queue volume, protection, and consumer impact before cutover.

**Assign ownership by decision.** Domain owners define entities and authoritative processes; source owners own assertions; master-product owners own shared contracts; stewards resolve governed exceptions; platform teams operate capabilities.

Consumers own their interpretation and fallback. Protection, legal, records, security, and incident roles remain explicit.

**Measure business and data outcomes.** Track reduced duplicate handling, successful cross-system resolution, decision improvement, correction time, false merge and split findings, conflict age, consumer adoption, incidents, cost, and retired duplication.

Record count and match rate alone can reward unsafe merging. Balance precision, recall, coverage, and consequence.

**Migrate by domain and consumer.** Inventory sources, identifiers, attributes, rules, histories, interfaces, consumers, decisions, and service dependencies.

Run shadow mastering, compare entities and views, review high-risk differences, publish aliases, migrate cohorts, preserve rollback, and time-box dual authority.

**Retire without orphaning identity.** Resolve identifier aliases, active source feeds, consumer references, APIs, events, files, histories, backups, overrides, cases, credentials, and deletion obligations.

Preserve required lineage while deleting prohibited data. Verify no old feed or replay recreates retired masters.

## Definitions and Notation

Let source assertion $a=(s,r,e,k,v,t_e,t_o,q,p)$ contain source $s$, source record $r$, entity candidate $e$, attribute key $k$, value $v$, effective time $t_e$, observation or transaction time $t_o$, quality or confidence $q$, and policy context $p$.

Let master entity version $m_j=(id,L_j,A_j,R_j,P_j)$ bind stable master identifier, source-record linkage set $L_j$, retained assertions $A_j$, selected golden representation $R_j$, and policy and decision evidence $P_j$.

For attribute $k$ and purpose $u$, a survivorship function produces either a selected assertion, a governed set, or a typed unresolved state:

$$
R_j(k,u)=Select(A_j(k),Authority,Time,Quality,Consent,Policy_j,u).
$$

Selection does not delete nonselected assertions. It creates an explainable view under versioned policy.

Define `FitMaster(G,d,t)` as a review predicate requiring justified decisions, clear domain and authority, stable identity, retained provenance, appropriate golden views, controlled workflows, protected publication, service and recovery evidence, accountable ownership, economic value, and lifecycle closure at time $t$.

## Mechanisms, Invariants, or Proof Structure

Use ten architecture gates.

**1. Outcome gate.** Name cross-system decisions, entities, consumers, deadlines, consequences, fallback, and value.

**2. Domain gate.** Define entity boundaries, attributes, relationships, sources, master versus reference and transaction scope, and owners.

**3. Authority gate.** Assign source, hub, and workflow rights for creation, verification, correction, override, expiration, and deletion.

**4. Identity gate.** Define master IDs, source cross-references, linkage evidence, non-reuse, merge, split, aliases, and history.

**5. Golden-view gate.** Preserve assertions and publish purpose-specific selections with policy, provenance, time, quality, uncertainty, and versions.

**6. Integration gate.** Define source contracts, snapshots, changes, positions, loops, conflicts, replay, reconciliation, and correction propagation.

**7. Protection gate.** Govern linkage, derived sensitivity, consent, purpose, minimization, authorization, retention, deletion, and audit.

**8. Service gate.** Bound freshness, availability, latency, queues, capacity, degraded behavior, recovery, and incident response.

**9. Ownership gate.** Assign domain, source, product, stewardship, platform, consumer, protection, decision, and retirement accountability.

**10. Lifecycle gate.** Compare styles, measure value, manage policy and schema change, migrate authority and consumers, and verify retirement.

Passing a gate supports a scoped master-data product. It does not make every selected value certain, every source wrong, or every consumer authorized.

### Executable evidence

The executable example selects a preferred contact while preserving the conflicting source assertion.

<!-- bijux-verify: {"id":"golden-record-provenance-contract","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"entity_id=party-100\ncandidate_assertions=2\nselected_email=verified@example.com\nselected_source=crm\nselection_reason=verified-contact-policy\nconflicting_assertion_preserved=true\ngolden_version=4\n","stderr":""}} -->
```python
assertions = [
    {
        "source": "crm",
        "email": "verified@example.com",
        "verified": True,
        "observed_day": 5,
    },
    {
        "source": "billing",
        "email": "newer@example.com",
        "verified": False,
        "observed_day": 7,
    },
]

selected = max(
    assertions,
    key=lambda item: (item["verified"], item["observed_day"]),
)
conflicts_preserved = all(item in assertions for item in assertions)

print("entity_id=party-100")
print(f"candidate_assertions={len(assertions)}")
print(f"selected_email={selected['email']}")
print(f"selected_source={selected['source']}")
print("selection_reason=verified-contact-policy")
print(f"conflicting_assertion_preserved={str(conflicts_preserved).lower()}")
print("golden_version=4")
```

The result proves only the declared ordering and preservation check for two in-memory assertions. It does not prove entity identity, source authority, contact ownership, verification validity, survivorship fitness, consent, production history, propagation, protection, recovery, or consumer decision safety.

## Alternatives and Trade-Offs

**No enterprise MDM.** Domains publish their own products and consumers integrate when cross-domain need is limited. This avoids a hub while duplicating resolution and policy work.

**Registry style.** Central linkage and identifier resolution minimize copied values but depend on distributed source availability and compatible semantics.

**Consolidation style.** Central golden views support analytics and downstream products while sources retain authoring. Corrections and latency need clear routes.

**Coexistence style.** Hub and sources synchronize selected attributes. It supports operational consistency but increases conflict and loop complexity.

**Centralized transactional style.** One service owns master mutations. It clarifies some authority while creating a critical operational dependency and migration burden.

**Single golden row.** Simple consumers can read one representation, but multiplicity, context, provenance, and uncertainty may be lost.

**Assertion-preserving entity.** Rich evidence supports explanation and new policies, at the cost of model, storage, interface, and consumer complexity.

**Rule-based selection.** Rules are explainable and deterministic but can be brittle. Statistical methods can handle ambiguity but need evaluation, thresholds, monitoring, and review.

**Real-time propagation.** Lowers lag for critical operations while increasing coupling and outage amplification. Scheduled releases can provide coherent evidence when delay is acceptable.

**One multi-domain platform.** Shared capabilities reduce duplication. Domain-specific products can preserve clearer meaning, ownership, scale, and failure isolation.

Choose by decisions, cross-system reuse, authority distribution, latency, uncertainty, protection, correction consequence, source capability, stewardship capacity, economics, and exit.

## Failure Modes and Misconceptions

1. **Golden means objectively true.** It means selected under evidence and policy for a scope.
2. **One entity needs one scalar value per attribute.** Context and time can make several values valid.
3. **The newest value always wins.** Authority, verification, effective time, and purpose can dominate arrival time.
4. **Matching and survivorship are the same.** Entity membership and preferred representation are distinct decisions.
5. **A master ID proves identity.** It records a decision and scope; evidence and history remain necessary.
6. **Central storage creates central authority.** Copying data does not transfer business mutation rights.
7. **A registry has no data risk.** Cross-references and linkages can be highly sensitive.
8. **Coexistence means every system may write.** Attribute and workflow authority must remain explicit.
9. **Standardization is lossless.** Normalization can erase source, locale, formatting, or cultural meaning.
10. **High match rate means high quality.** Unsafe false merges can raise the rate.
11. **Manual review guarantees correctness.** Reviewers need evidence, policy, training, quality checks, and manageable queues.
12. **Full records should be shared for convenience.** Purpose-limited views reduce misuse and exposure.
13. **Replication makes the hub recoverable.** Rules, link history, overrides, positions, and evidence also need recovery.
14. **Replay reproduces masters.** Changed rules, reference data, sources, or policies can change outcomes.
15. **Consumers automatically adopt corrections.** Version and completion evidence must cross each boundary.
16. **One MDM style fits every domain.** Authority and use patterns differ.
17. **Turning off the hub retires MDM.** Identities, copies, feeds, cases, credentials, and duties remain.

## Worked Examples

### Example 1

A legal name comes from a verified identity workflow, a shipping address from the latest fulfilled order, and marketing preference from consent records. **Conclusion:** golden attributes can have different authorities within one entity.

### Example 2

A person has two current addresses: residence and seasonal correspondence. The model retains both with type and interval while one purpose-specific view selects correspondence. **Conclusion:** preference does not erase multiplicity.

### Example 3

A registry links hospital patient identifiers but retrieves clinical demographics from each hospital. Source outage makes the virtual view partial and visibly degraded. **Conclusion:** registry style retains runtime source dependency.

### Example 4

A consolidated supplier product publishes approved views nightly while procurement systems remain authoritative. Steward corrections route to procurement rather than patching the consolidation table. **Conclusion:** storage and authoring authority differ.

### Example 5

A coexistence hub publishes a corrected address back to CRM. Origin and master-version tags stop CRM's echo from becoming a newer competing assertion. **Conclusion:** synchronization needs loop prevention.

### Example 6

Two accounts are wrongly merged, exposing contact history across people. The system restores prior IDs and memberships, publishes a split correction, invalidates caches, and identifies affected consumers. **Conclusion:** reversibility and impact lineage are safety properties.

### Example 7

A policy change prefers verified phone numbers over newest observations. Shadow recomputation shows 8% of entities would change and creates a steward queue for high-risk cases. **Conclusion:** rule changes are data migrations.

### Example 8

A marketing consumer requests the full party record but needs only preferred language and eligible contact channel. A minimized view excludes fraud flags, government IDs, and household links. **Conclusion:** one master entity supports different protected products.

### Example 9

Hub uptime is high while a source feed is stalled. Attribute-level freshness and source positions reveal that risk status is stale even though profiles remain available. **Conclusion:** availability is not master-data currency.

### Example 10

A retired product domain has no API calls but still appears in backups, cross-reference resolution, batch files, override queues, and replay configuration. **Conclusion:** retirement requires dependency and retained-data closure.

## Cross-Program Connections

- **Data engineering:** source contracts, standardization, change capture, entity processing, publication, reconciliation, history, and deletion implement MDM flows.
- **Platform engineering:** identity, workflow, eventing, APIs, metadata, policy, observability, recovery, tenancy, and paved operations support master products.
- **API and service engineering:** identifier resolution, inquiry, command, bulk, event, correction, and version contracts shape consumer integration.
- **Security and privacy:** linkability, purpose, minimization, consent, access, audit, retention, deletion, and incident scope intensify when records combine.
- **Machine learning:** probabilistic matching and entity features require evaluation, thresholds, provenance, drift monitoring, human review, and safe fallback.
- **Organizational design:** domain authority, stewardship, decision rights, source ownership, consumer responsibility, and escalation determine real governance.
- **Reliability engineering:** source gaps, queues, fan-out, backpressure, degraded views, recovery, replay, reconciliation, and correction time define service.
- **Economics and decision science:** false merge and split costs, value of shared identity, review capacity, propagation burden, uncertainty, and exit cost guide investment.
- **Systems engineering:** stakeholder outcomes, evidence, hazards, system boundaries, lifecycle assurance, and verification keep mastering accountable.

## References

1. Microsoft, *Master Data Management in Microsoft Purview*. <https://learn.microsoft.com/en-us/purview/data-governance-master-data-management>
2. IBM, *Data Concepts in IBM Master Data Management*. <https://www.ibm.com/docs/en/ws-and-kc?topic=data-concepts>
3. IBM, *InfoSphere MDM Technologies*. <https://www.ibm.com/docs/en/imdm/12.0.0?topic=overview-infosphere-mdm-technologies>
4. IBM, *Persistence of the Golden Record*. <https://www.ibm.com/docs/en/imdm/11.6.0?topic=mdm-persistence-golden-record>
5. W3C, *PROV-O: The PROV Ontology*. <https://www.w3.org/TR/2013/REC-prov-o-20130430/>
6. OpenLineage, *Object Model*. <https://openlineage.io/docs/next/spec/object-model/>
7. NIST, *Privacy Framework*. <https://www.nist.gov/privacy-framework/privacy-framework>
8. Google, *Site Reliability Engineering: Addressing Cascading Failures*. <https://sre.google/sre-book/addressing-cascading-failures/>
9. NIST, *SP 800-160 Volume 1 Revision 1: Engineering Trustworthy Secure Systems*. <https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final>

## Exercises

### Exercise 1

Design master-data architecture for a customer or party domain. Define decisions, entity scope, sources, identifiers, assertions, golden views, style, publication, protection, service, ownership, and lifecycle.

### Exercise 2

CRM, billing, and support disagree on a customer's name, address, contact preference, and risk status. Explain why one source-level priority list is insufficient and design attribute-level authority and evidence.

### Exercise 3

Compare registry, consolidation, coexistence, and centralized transactional styles for a global supplier domain with regional authoring and shared compliance screening.

### Exercise 4

A rule change and replay merge 12,000 entities differently while live source changes continue. Design containment, comparison, correction, and safe cutover.

### Exercise 5

An organization plans to retire its MDM hub after moving applications to domain services. Define evidence that mastering functions and obligations have actually transferred or ended.

## Answers to the Exercises

### Answer 1

Define whether the entity is legal party, customer account, user, household, or another scoped type; never collapse these by label. Name decisions such as fulfillment, service, compliance, fraud review, and analytics, with deadlines and false-merge or split consequences. Inventory source records, identifiers, attribute authorities, histories, corrections, deletes, consent, and quality. Create stable nonreused master IDs and temporal cross-references while retaining every source assertion and linkage decision.

Choose style by authoring: registry when sources retain values and can serve them; consolidation for governed downstream views; coexistence for divided operational authorship; centralized service when master commands truly move. Publish purpose-limited views with attribute provenance, policy, version, freshness, quality, and correction contracts. Protect linkages and histories; define queues, capacity, degraded behavior, recovery, replay, and reconciliation. Assign domain, source, product, steward, platform, consumer, protection, and decision owners. Measure decision outcomes and correction safety, then migrate and retire feeds, IDs, copies, cases, and duties explicitly.

### Answer 2

A whole-source ranking assumes one system is best for every meaning. CRM may own sales-facing preferred name, billing may own invoice address, support may record a temporary contact channel, and a qualified risk workflow may own risk status. Recency clocks can differ, multiple addresses may be simultaneously valid, consent can prohibit one purpose, and a source may only observe rather than author an attribute.

For each attribute define semantics, multiplicity, source roles, origination and verification rights, effective and observation time, quality, consent, expiration, correction, override, and purpose. Retain original assertions and standardized forms. The golden view selects or returns a governed set with source, reason, policy version, time, and uncertainty. Route conflicts to the right owner; do not overwrite them. Different consumers receive minimized views, and corrections propagate through stable entity and version identities with reconciliation.

### Answer 3

Registry style fits when regional systems remain authoritative, can respond reliably, and compliance can resolve identifiers then query current facts; its weakness is source dependency and distributed semantics. Consolidation fits shared screening and analytics by copying records into coherent releases while regions retain writes; it introduces lag and correction routing. Coexistence fits when compliance decisions or approved supplier attributes must flow back, but requires exact field ownership, origin tags, conflict rules, loop prevention, idempotency, and reconciliation. Centralized transactional style fits only if supplier creation and master changes truly move to one service with global availability, regional authorization, and migration of business workflow.

A hybrid is plausible: regional sources author operational details, a registry maintains cross-references, a consolidated protected view supports screening, and centrally approved compliance status propagates through coexistence. Define jurisdiction and purpose, source and hub positions, attribute authority, provisional states, fail-closed screening behavior, stewardship, correction times, and regional recovery. Avoid calling the hybrid complete while write ownership remains ambiguous.

### Answer 4

Stop the replay from publishing into live masters, preserve its inputs, code, rule and reference versions, and mark any exposed results invalid. Keep live ingestion and authoritative commands on the last trusted policy. Inventory affected master IDs, source memberships, aliases, selected attributes, downstream views, caches, decisions, and protection incidents. Determine whether the rule intentionally changed identity or whether replay boundaries, current rules, or source versions caused divergence.

Recompute in an isolated namespace from a pinned snapshot plus a captured change boundary. Compare old and new memberships, especially high-consequence merges and splits; sample evidence, estimate steward queue capacity, and obtain domain and protection approval. Apply live deltas to the shadow state, rerun comparisons, then cut over through a versioned generation with aliases and correction events. Rate-limit downstream propagation, track acknowledgements, preserve rollback, reconcile sources and consumers, and never let an older replay overwrite newer live decisions.

### Answer 5

Inventory every master domain, ID namespace, cross-reference, source feed, linkage and survivorship rule, override, hierarchy, stewardship case, API, event, file, consumer, cache, analytical copy, model, report, backup, credential, contract, retention rule, hold, and deletion path. For each capability name the receiving domain service or prove it is no longer required. Define authority-transfer times, identifier resolution and aliases, history custody, correction routing, protection, service objectives, incidents, and recovery.

Run old and new mastering in bounded comparison, migrate consumers by cohort, reconcile entity memberships and values, and preserve qualified rollback. Stop new hub authoring, then feeds and publication only after calls and queues cease. Transfer or close unresolved cases, revoke access, delete prohibited copies, preserve required provenance, update deletion discovery, terminate licenses and infrastructure, and test that old sources, jobs, backups, or replays cannot resurrect retired masters. Record accountable closure rather than inferring retirement from low traffic.
