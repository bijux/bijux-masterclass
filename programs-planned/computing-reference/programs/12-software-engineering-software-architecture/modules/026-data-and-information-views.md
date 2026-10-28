---
module_id: SARCH-026
program: Software Engineering: Software Architecture
level: 1
module_number: 26
title: Data and Information Views
status: complete
last_verified: 2026-09-06
---

# Data and Information Views

## One-Page Review

### Governing question

How can an architecture description make information meaning, identity, authority, representation, movement, transformation, quality, protection, and lifecycle reviewable across systems without collapsing the view into one database schema?

### Essential definitions

- **Information** is data interpreted within a declared semantic and decision context.
- A **concept** is a domain meaning, such as customer, consent, temperature, invoice, or device state.
- A **data element** is a named representation of some aspect of a concept, with type, units, constraints, and missing-value semantics.
- A **schema** constrains the structure and permitted values of a representation; structural validity does not establish semantic truth.
- An **identifier** distinguishes an entity or event within a declared scope, time, and authority.
- A **system of record** is the declared authority for specified facts or state transitions; it is not necessarily the only copy or access path.
- **lineage** records how data moved and transformed; **provenance** records origins, activities, agents, and responsibility needed to assess it.
- A **data quality rule** states fitness-relevant expectations such as validity, completeness, uniqueness, consistency, timeliness, or accuracy with population and measurement method.
- **classification** assigns handling obligations according to sensitivity, harm, law, contract, or business policy.
- A **retention rule** defines how long a data class is kept, when its clock starts, and how deletion, legal hold, backup, and derived copies behave.

### Central model, mechanism, or theorem

Represent an information architecture as

$$
V=(C,D,S,T,O,L,P,Q),
$$

where $C$ is concepts, $D$ data elements and representations, $S$ stores and streams, $T$ transformations, $O$ ownership and authority, $L$ lineage/provenance relations, $P$ protection and lifecycle policies, and $Q$ quality rules.

Every consequential representation should trace to meaning and authority:

$$
d\in D \Rightarrow meaning(d)\in C,\ scope(d),\ owner(d),\ authority(d),\ time(d),\ policy(d),\ quality(d).
$$

Not every field needs maximal metadata, but omitted properties must be an explicit concern decision rather than an accidental ambiguity.

### Critical invariants

- declare stakeholders, decisions, scope, lifecycle state, and abstraction;
- distinguish concept, logical data element, physical representation, stored copy, and observed value;
- define identifiers, entity resolution, authority, version, validity time, and observation time;
- specify units, reference systems, encodings, precision, ranges, null, unknown, absent, redacted, and not-applicable meanings;
- expose creation, validation, transformation, aggregation, publication, access, correction, archival, and deletion;
- preserve lineage and transformation semantics across boundaries;
- distinguish schema validity, semantic validity, data quality, and decision fitness;
- classify information and enforce least collection, least privilege, retention, deletion, and audit;
- define consistency and freshness per copy and reader rather than saying “synchronized”;
- reconcile information with context, runtime, interaction, deployment, security, and operational views;
- bind conformance to versioned schemas, catalog records, samples, reconciliations, and stated evidence limits.

### Common failures

Common failures include treating a physical database schema as the whole information architecture; using one word for different concepts; using different words for the same concept without mapping; omitting units, time basis, and identifier scope; treating `null`, zero, empty, unknown, redacted, and not applicable as interchangeable; assuming syntactic validation proves truth; calling every replicated copy authoritative; losing lineage through transformation; retaining sensitive derived data after deleting its source; reporting quality percentages without a denominator; and claiming a diagram proves production data correctness.

### Compact example

Two systems exchange `temperature: 20`. One means degrees Celsius at sensor event time; the other assumes degrees Fahrenheit at ingestion time. The JSON is valid and the number is in range, yet the information is wrong. The view must specify unit, scale, sensor identity, event time, observation quality, conversion, and authority.

### Connections

[SARCH-017](017-interoperability-tactics.md) supplies semantic contracts; [SARCH-021](021-context-views.md) supplies information crossings; [SARCH-024](024-runtime-interaction-views.md) supplies causal events; [SARCH-025](025-deployment-views.md) supplies storage and processing locations. [SARCH-027](../ROADMAP.md) next develops development and build views. Database, Data, Data Architecture, Security, and Reliability Engineering deepen the mechanisms.

## Governing Question

Software coordinates decisions through information. A field named `status` can represent an observation, desired state, legal fact, cached projection, or guess. A customer identifier can mean a person, household, account, contract, or device. A timestamp can mean event occurrence, receipt, processing, commit, or expiry. Without explicit semantics, systems can exchange perfectly valid bytes and still disagree.

The governing problem is to describe the concepts that matter, their representations and authorities, how they move and change, what quality and protection they require, and how claims are verified. The view must span organizational and runtime boundaries while remaining small enough to review.

## Why This Matters

Information errors propagate. Wrong units can produce physical harm. Weak identity resolution can merge two people or split one person. Stale authorization data can grant or deny access incorrectly. Aggregation can hide bias or make deletion difficult. A retry can duplicate an event. A schema migration can reinterpret historical values without changing bytes.

Performance, availability, modifiability, security, privacy, auditability, interoperability, and analytical validity all depend on information choices. Replication changes freshness and consistency. Encryption changes access and operations. Retention changes cost, legal exposure, and reproducibility. Ownership determines who can correct a fact.

A data and information view creates a shared contract across product, engineering, operations, security, privacy, analytics, records management, and domain experts. It is not a substitute for detailed database design; it gives that design semantic and governance boundaries.

## Prerequisites and Retrieval

Retrieve data, information, concept, entity, attribute, relationship, event, state, identifier, namespace, schema, type, representation, encoding, unit, precision, cardinality, null, validity, authority, system of record, copy, cache, stream, transformation, lineage, provenance, quality, classification, minimization, retention, deletion, legal hold, consistency, freshness, and conformance.

From prior modules, retrieve functional scope, stakeholder concerns, quality scenarios, security and interoperability tactics, observability, context views, runtime interactions, and deployment views. Distinguish business meaning, interface representation, storage model, transport encoding, and analytical projection.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish information concepts, logical elements, representations, values, stores, and copies;
2. define identifier scope, entity resolution, authority, version, and temporal semantics;
3. specify units, precision, missing values, constraints, and reference data;
4. model information lifecycle, transformations, lineage, and provenance;
5. distinguish schema validity, semantic validity, quality, accuracy, and fitness for use;
6. define classification, minimization, access, retention, deletion, and audit obligations;
7. reason about copies, consistency, freshness, conflict, and reconciliation;
8. compare conceptual, logical, physical, flow, lifecycle, and governance projections;
9. identify cross-view mismatches and ambiguous ownership;
10. evaluate information conformance using bounded, versioned evidence.

## Core Exposition

**Frame the information concern.** Name stakeholders, decisions, scope, scenario, lifecycle state, and resolution. A product view may focus on customer and order meaning. A security view focuses on classification, authority, and access. An analytical view focuses on transformations, populations, and reproducibility. A recovery view focuses on durable state, logs, backups, and reconciliation.

ISO/IEC/IEEE 42010:2022 remains the current published architecture-description edition as checked on 2026-09-06. It supports multiple concern-governed models and their correspondences rather than one mandatory data notation [1]. Use several linked projections when one diagram would mix semantics, storage, flow, lifecycle, and protection.

**Begin with concepts, not tables.** Define what each concept means in the domain, its boundaries, relationships, states, and invariants. “Customer” may mean a natural person, legal entity, account holder, purchaser, recipient, or prospect. If contexts use different meanings, name them separately and define translation rather than forcing false uniformity.

Conceptual models describe meaning independent of a storage technology. Logical models define elements, relationships, identifiers, and constraints. Physical models define tables, documents, topics, files, indexes, partitions, encodings, and storage. These levels correspond but are not identical. A denormalized document can represent the same logical concept as several relational tables.

ISO/IEC 11179-1:2023 is the current published framework edition checked on 2026-09-06 for understanding metadata and metadata registries [2]. ISO/IEC 11179-3:2023 specifies common registry facilities including identification, designation, definition, registration, and classification [3]. These standards reinforce a durable point: a data name needs governed meaning and context, not merely a physical type.

**Define data elements completely enough.** Record canonical name, aliases, definition, concept, type, units, reference system, allowed values, precision, range, cardinality, missing-value meanings, examples, authority, sensitivity, and version where relevant. Distinguish validation constraints from observations about actual quality.

Numbers require unit and scale. Currency needs currency code and often valuation time. Geographic coordinates need a reference system. Text needs encoding, normalization, language, and comparison rules where identity depends on it. Time needs event meaning, time zone or offset, precision, clock source, and uncertainty.

`null` is not one universal state. It may mean unknown, not collected, withheld, not applicable, not yet computed, invalid, deleted, or absent from this version. If those distinctions affect decisions, model them as distinct states or tagged reasons. Zero and empty string are values, not generic missing markers.

**Model identity and entity resolution.** State what an identifier names, who issues it, its namespace, uniqueness scope, lifetime, reuse policy, opacity, and exposure. A database primary key may identify a row, not a real-world person. Email addresses, names, and device network addresses are attributes that can change or collide; they are rarely safe universal identities.

Entity resolution is a decision with false-merge and false-split costs. Preserve source identities and evidence when creating a canonical identity. Define confidence, human review, correction, and unmerge behavior. Do not let an analytical linkage silently become an authorization identity.

**Declare authority and copies.** For every consequential fact or transition, name the authority and conflict policy. “System of record” should be scoped: billing may own invoice status, identity may own legal name, and a device may own physical observations. A reporting warehouse can be authoritative for a published report while remaining derived from operational facts.

Classify other representations as replicas, caches, indexes, projections, snapshots, exports, or estimates. State update path, freshness, consistency, invalidation, availability, and behavior when disconnected. A locally available stale copy can improve availability while reducing decision validity.

**Represent temporal semantics.** Separate valid time—when a fact holds in the modeled world—from transaction or system time—when a system recorded it. Also distinguish event occurrence, observation, ingestion, processing, publication, and expiry. Late and corrected data make these differences operational.

An address valid from March may be recorded in April. Replacing the old row destroys the ability to answer “what did we believe on March 20?” or “what was actually valid then?” if those are required questions. Choose current-state, append-only, bitemporal, event, or snapshot models according to decisions and evidence obligations.

**Model state transitions and events.** An event records a claimed occurrence with identity, type, subject, time, source, payload, and provenance. Define whether it is an authoritative fact, a request, or an observation. State ordering scope, duplication, correction, retraction, and replay behavior.

Event streams do not automatically reconstruct truth. Missing events, duplicated delivery, non-deterministic transformations, external effects, and evolving code can change results. If replay is a recovery claim, preserve required artifacts, configuration, reference data, event versions, and ordering semantics.

**Trace flow and transformation.** Show sources, sinks, stores, streams, transformations, filters, joins, aggregations, and publications. For each transformation, define input versions, output meaning, owner, deterministic assumptions, error handling, and lineage. A field copied unchanged may still change meaning when context changes.

W3C PROV-O, a W3C Recommendation, models entities, activities, and agents and relations such as generation, use, derivation, attribution, and association [4]. It provides a standard vocabulary for interoperable provenance. An architecture may use a simpler model, but should preserve enough origin, transformation, and responsibility to support its decisions.

Lineage is not correctness. A complete chain can faithfully show that wrong input produced wrong output. Conversely, missing lineage can make a correct-looking result impossible to audit. Protect provenance itself from tampering and inappropriate disclosure.

**Define quality relative to use.** Quality dimensions include validity, completeness, uniqueness, consistency, timeliness, accuracy, precision, and integrity, but their relevance depends on a decision. A complete dataset can be inaccurate; a valid value can be stale; two consistent copies can share the same systematic error.

For a population $U$ and rule predicate $q(x)$, a conformance ratio is $|\{x\in U:q(x)\}|/|U|$ when $|U|>0$. State population, exclusions, observation window, rule version, sampling, and uncertainty. A 99.9% rate says little if high-risk records are excluded or all failures cluster in one subgroup.

ISO 8000-1:2022 provides the current published overview of the ISO 8000 data-quality series as checked on 2026-09-06 [5]. Use such standards to calibrate vocabulary and governance, while defining project-specific fitness, thresholds, and consequences.

**Protect information through its lifecycle.** Classify data by harm and obligation. Minimize collection, precision, replication, access, and retention. Define purpose, consent or other authority where applicable, least privilege, encryption, key custody, masking, audit, export, correction, deletion, and incident handling.

Derived and aggregated data can remain sensitive. Hashing a low-entropy identifier may not anonymize it. Backups, caches, indexes, logs, training sets, and exports can outlive source deletion. A retention rule needs start event, duration, hold, deletion method, exceptions, evidence, and propagation to derived copies.

**Plan schema and meaning evolution.** Version syntax and semantics. Adding an optional field may be structurally backward compatible while changing business decisions. Renaming a status can break consumers that persist the old value. Changing units without a new field or version silently corrupts interpretation.

Define reader/writer compatibility, dual-read or dual-write interval, migration, historical interpretation, rollback, and retirement. Unknown fields and enum values need policy. Preserve original values when conversions are lossy or disputed. Coordinate with runtime and deployment transitions.

**Reconcile information across boundaries.** Map context exchanges to concepts and policies; messages to schemas and events; components to authority; deployments to storage and jurisdiction; security to classification and access; operations to quality and lineage evidence. The same element name with different meanings, or different authorities for one transition, is a review defect.

**Gather bounded evidence.** Schema validation can establish structure for checked records. Constraint checks can find selected invalid states. Reconciliation can compare authorities and copies. Samples can estimate quality with statistical assumptions. Lineage can show declared transformations. Access logs can show recorded use. Restore tests can observe recovery in a recorded environment.

No one check proves semantic truth or universal fitness. Catalogs drift, instrumentation misses paths, checks encode incomplete rules, and source facts can be wrong. Record versions, populations, times, methods, results, exclusions, owners, and remediation. Review after new source, use, transformation, schema, jurisdiction, threat, incident, or retention obligation.

## Definitions and Notation

Define an information view

$$
V=(C,D,S,T,O,L,P,Q),
$$

where $C$ is domain concepts; $D$ data elements and representations; $S$ stores and streams; $T$ transformations; $O$ ownership and authority; $L$ lineage and provenance; $P$ protection and lifecycle policies; and $Q$ quality rules.

Let $rep(d,c,v)$ mean representation $d$ encodes concept $c$ under semantic version $v$. Let $auth(c,a,t)$ mean authority $a$ governs the stated aspect of concept $c$ at time $t$. These relations prevent a physical field or one organization from becoming globally authoritative by implication.

For nonempty evaluated population $U$ and quality predicate $q_v$ at rule version $v$, define

$$
rate(U,q_v)=\frac{|\{x\in U:q_v(x)=true\}|}{|U|}.
$$

The rate is undefined for an empty population unless policy defines another result. Unknown evaluations should not be silently counted as passing or failing; report them separately.

Define a transformation $t:D_{in}\times R\rightarrow D_{out}\cup E$, where $R$ is versioned reference data and $E$ explicit error outcomes. A lineage edge records input entities, transformation identity and version, responsible agent, output entity, and relevant time. Determinism or reproducibility requires additional assumptions about code, configuration, ordering, and environment.

## Mechanisms, Invariants, or Proof Structure

Use this information-view mechanism.

1. **Frame:** name stakeholders, decisions, scope, scenarios, lifecycle state, and abstraction.
2. **Define concepts:** establish meanings, boundaries, relationships, states, and domain invariants.
3. **Define representations:** specify elements, types, units, reference systems, missing values, versions, and examples.
4. **Assign identity and authority:** record issuers, namespaces, entity resolution, owners, transition authority, and conflict policy.
5. **Map lifecycle:** show creation, validation, movement, transformation, publication, correction, archive, and deletion.
6. **Trace lineage:** bind inputs, reference data, transformations, agents, outputs, errors, and reproducibility assumptions.
7. **Specify quality:** define rules, populations, thresholds, observation windows, consequences, and remediation.
8. **Protect:** classify, minimize, authorize, encrypt, audit, retain, delete, and handle holds and derived copies.
9. **Challenge:** test missing, duplicate, stale, conflicting, reordered, malformed, adversarial, and historically reinterpreted data.
10. **Reconcile and verify:** connect context, runtime, deployment, security, operations, schemas, samples, and evidence limits.

The governing invariants are explicit meaning, scoped identity, declared authority, temporal clarity, preserved transformation semantics, traceable lineage, decision-relative quality, lifecycle protection, evolution compatibility, cross-view correspondence, and bounded evidence.

If every transformation edge in an acyclic lineage graph points from input version to generated output version, following edges backward must terminate at a source. This supports finite ancestry traversal. It does not prove the sources are truthful, the graph is complete, or a transformation is correct; cycles, mutable identities, and omitted external state violate the premises.

## Alternatives and Trade-Offs

**Canonical model versus bounded contexts.** One enterprise model can reduce translation but becomes slow and overgeneralized. Bounded models preserve local meaning but require explicit mappings and accept that some concepts are not equivalent.

**Current state versus event history.** Current state is compact and direct for present decisions. Event history supports audit and reconstruction but requires ordering, correction, versioning, privacy, and deterministic-replay assumptions.

**Central authority versus federated ownership.** Central authority can simplify consistency and governance. Federated ownership aligns expertise and autonomy but requires identity, contract, lineage, and conflict protocols.

**Normalization versus denormalization.** Normalization can reduce update anomalies. Denormalization improves local reads and autonomy but creates freshness, invalidation, duplication, and reconciliation duties. This architectural choice precedes database-specific implementation detail.

**Strict schema versus tolerant evolution.** Strict validation catches defects early but can impede independent change. Tolerant readers support evolution but can silently discard meaning. Compatibility policy must include semantics, not just parsers.

**Fine-grained lineage versus cost and exposure.** Detailed lineage improves diagnosis, audit, and reproducibility. It consumes storage and processing and can reveal sensitive relationships. Capture the resolution justified by decisions and risk.

**Long retention versus minimization.** Retention supports audit, analysis, and recovery. Minimization reduces exposure, cost, and stale misuse. Define purpose and legal or contractual obligations rather than keeping everything indefinitely.

## Failure Modes and Misconceptions

- **The table is the concept.** Physical representation is one implementation of domain meaning.
- **Same name means same meaning.** Context, unit, authority, and time can differ.
- **Different names mean different concepts.** Aliases and historical names may represent one meaning.
- **Valid means true.** Schema validation proves selected structural constraints, not factual accuracy.
- **Null means missing.** Unknown, absent, redacted, not applicable, and deleted may require distinct semantics.
- **A primary key identifies the real-world entity.** It often identifies only a record in one namespace.
- **System of record means universal owner.** Authority must be scoped by fact, transition, context, and time.
- **Replicas are synchronized.** State the consistency, freshness, conflict, and failure model.
- **Lineage proves correctness.** It records derivation; bad inputs and bad transformations remain possible.
- **Aggregation removes sensitivity.** Small groups, joins, and auxiliary data can enable harmful inference.
- **Deleting the source deletes the data.** Derived copies, backups, logs, and exports may remain.
- **A quality percentage speaks for itself.** Population, rule, window, exclusions, and uncertainty are essential.
- **Backward-compatible syntax preserves meaning.** Business semantics can change while parsing succeeds.

## Worked Examples

### Example 1

**Situation.** A sensor sends `temperature: 20`; the receiver expects Fahrenheit.

**Reasoning.** Both systems accept the number and range, yet 20 °C equals 68 °F, while 20 °F is about -6.7 °C. Add unit, scale, sensor identity, event time, precision, and quality status. Convert at a named transformation and preserve the original measurement.

**Conclusion.** Structural compatibility without semantic metadata can produce a valid but dangerous value.

### Example 2

**Situation.** Records for “A. Rahman” and “Amira Rahman” share an address and are merged automatically.

**Reasoning.** Names and addresses are evidence, not stable identity. A false merge exposes one person's history to another. Preserve source identifiers, score evidence, require review above the risk threshold, record the merge decision, and support unmerge and correction.

**Conclusion.** Entity resolution is a consequential, reversible decision—not routine string matching.

### Example 3

**Situation.** A medical form stores missing dosage as `0`.

**Reasoning.** Zero may mean explicitly no dose; missing may mean not recorded; withheld may mean inaccessible. Conflation can suppress follow-up or change treatment. Model tagged states and permit arithmetic only after policy resolves them.

**Conclusion.** Missing-value semantics belong in the information contract.

### Example 4

**Situation.** A sale occurred at 23:58 local time, arrived after midnight UTC, and was processed two hours later.

**Reasoning.** Event time answers when the sale occurred; ingestion time describes arrival; processing time describes transformation; accounting period follows business policy and timezone. Ordering by ingestion misclassifies late events. Preserve all required timestamps with offset, zone rule, precision, and source.

**Conclusion.** One generic timestamp cannot support several temporal questions honestly.

### Example 5

**Situation.** A profile cache says an account is active 30 seconds after the identity authority disabled it.

**Reasoning.** The authority changed at version 42; the cache holds version 41 under a 60-second freshness policy. That may be acceptable for personalization but not authorization. Security decisions must query or subscribe to an appropriately fresh authority and define fail-closed or bounded-stale behavior.

**Conclusion.** Copy fitness depends on use, freshness, and failure policy.

### Example 6

**Situation.** A producer adds enum value `partially_fulfilled`; an old consumer maps unknown values to `complete`.

**Reasoning.** The payload parses but changes meaning unsafely. An old consumer should reject, preserve as unknown, or follow an explicitly safe default. Introduce compatibility tests, versioned semantics, mixed-version rollout, and migration of stored projections.

**Conclusion.** Parser compatibility does not establish semantic compatibility.

### Example 7

**Situation.** A dashboard total comes from orders joined to daily exchange rates and filtered by a fraud model.

**Reasoning.** Record order snapshot, exchange-rate source and date, fraud-model and code versions, join and exclusion rules, transformation run, output identity, and owner. Reproducing the number also requires retained inputs and deterministic or bounded execution assumptions.

**Conclusion.** Useful lineage joins entities, activities, agents, versions, and reference data.

### Example 8

**Situation.** A user requests deletion, but a training table contains derived behavioral features.

**Reasoning.** The lineage graph reveals derived rows, feature snapshots, exports, backups, and model artifacts. Policy determines which must be deleted, retrained, quarantined, retained under hold, or made inaccessible. The system records each outcome and exception without pretending one source-row deletion completed the obligation.

**Conclusion.** Retention and deletion must propagate through lineage under explicit policy.

### Example 9

**Situation.** A report claims 99% email completeness from 990 populated values among 1,000 rows.

**Reasoning.** Ten rows are null, but 200 populated values are placeholders such as `unknown@example.invalid`. Structural non-null rate is 99%; usable-contact rate is at most 79%. Define rule, eligible population, exclusions, window, placeholder detection, and high-risk subgroups.

**Conclusion.** A percentage without semantic rule and denominator can reward bad data.

### Example 10

**Situation.** A wildfire model combines satellite pixels, weather stations, and citizen reports.

**Reasoning.** Preserve source, location reference, observation time, ingestion time, spatial resolution, uncertainty, correction, and license for each input. Transformations align coordinates and time windows without erasing originals. The alert view identifies which model version and evidence caused an alert, protects reporter identity, and expires low-confidence raw reports under policy.

**Conclusion.** High-consequence fusion needs explicit provenance, uncertainty, authority, privacy, and correction.

## Cross-Program Connections

- **Database Engineering:** models, constraints, transactions, indexes, isolation, replication, and recovery implement information storage.
- **Data Engineering:** ingestion, transformation, orchestration, lineage, quality, and observability implement data movement.
- **Data Architecture Engineering:** ownership, domains, metadata, governance, lifecycle, and analytical products deepen enterprise scope.
- **API and Service Engineering:** schemas, identifiers, compatibility, errors, and idempotency expose information at boundaries.
- **Security:** classification, authorization, encryption, minimization, audit, retention, and deletion protect information.
- **Distributed Systems:** replication, consistency, clocks, ordering, conflict, and failure constrain copies.
- **Software Delivery and Reliability Engineering:** migrations, rollout, recovery, telemetry, and incidents provide operational evidence.
- **Systems Engineering:** physical measurements, calibration, uncertainty, hazards, and evidence connect data to the world.

## References

1. ISO/IEC/IEEE, *ISO/IEC/IEEE 42010:2022 Software, systems and enterprise — Architecture description*, 2nd ed., November 2022. Official catalogue; current edition checked 2026-09-06. https://www.iso.org/standard/74393.html
2. ISO/IEC, *ISO/IEC 11179-1:2023 Information technology — Metadata registries (MDR) — Part 1: Framework*, 4th ed., January 2023. Current edition checked 2026-09-06. https://www.iso.org/standard/78914.html
3. ISO/IEC, *ISO/IEC 11179-3:2023 Information technology — Metadata registries (MDR) — Part 3: Metamodel for registry common facilities*, 4th ed., January 2023. Current edition checked 2026-09-06. https://www.iso.org/standard/78915.html
4. Timothy Lebo, Satya Sahoo, Deborah McGuinness, Khalid Belhajjame, James Cheney, David Corsar, Daniel Garijo, Stian Soiland-Reyes, Stephan Zednik, and Jun Zhao, eds., *PROV-O: The PROV Ontology*, W3C Recommendation, 30 April 2013. https://www.w3.org/TR/prov-o/
5. ISO, *ISO 8000-1:2022 Data quality — Part 1: Overview*, 1st ed., April 2022. Current edition checked 2026-09-06. https://www.iso.org/standard/81745.html
6. Martin Kleppmann, *Designing Data-Intensive Applications*, O’Reilly Media, 2017.
7. Eric Evans, *Domain-Driven Design: Tackling Complexity in the Heart of Software*, Addison-Wesley, 2003.
8. David C. Hay, *Data Model Patterns: Conventions of Thought*, Dorset House, 1995.
9. DAMA International, *DAMA-DMBOK: Data Management Body of Knowledge*, 2nd ed., Technics Publications, 2017.

## Exercises

### Exercise 1

Precisely distinguish concept, entity, data element, representation, value, schema, identifier, authority, copy, lineage, and provenance. Explain why no physical table is automatically the concept.

### Exercise 2

A quality check evaluates 2,000 records. 1,860 pass, 80 fail, and 60 cannot be evaluated because reference data is missing. Compute (a) pass rate if unknowns are included in the population and not counted as passes, and (b) pass rate among evaluable records. Explain why both must be labeled.

### Exercise 3

An operational authority corrects a customer's birth date, but cache, warehouse, search index, audit log, backup, and exported partner file contain older values. Design a correction and evidence process without assuming every copy can be overwritten.

### Exercise 4

Compare a single enterprise customer model with bounded customer models for billing, support, delivery, and analytics. Address identity, authority, translation, privacy, evolution, and failure.

### Exercise 5

Transfer the method to a regional water-quality network combining laboratory samples, continuous probes, maintenance records, rainfall, and public alerts. Design the information view for units, locations, time, calibration, detection limits, corrections, lineage, quality, authority, privacy, retention, and alert evidence.

## Answers to the Exercises

### Answer 1

A **concept** is a domain meaning; an **entity** is one distinguishable instance under that meaning. A **data element** describes a representable aspect. A **representation** encodes it; a **value** is one occurrence. A **schema** constrains representations. An **identifier** distinguishes an entity or event within a scope. An **authority** governs a fact or transition. A **copy** reproduces or derives information under freshness and consistency rules. **Lineage** records movement and transformation; **provenance** includes origin, activity, agent, and responsibility.

A table is a physical structure optimized for implementation. It can combine several concepts, split one concept across tables, contain historical and derived values, or represent one context's interpretation. Meaning and authority require governed correspondence beyond the table definition.

### Answer 2

Including all records, the pass rate is $1860/2000=0.93$, or 93%. Among evaluable records, the denominator is $1860+80=1940$, so the pass rate is $1860/1940\approx0.9588$, or 95.88%.

The first describes success over the whole intended population when unknowns do not pass. The second describes rule performance only where evaluation was possible. Reporting only 95.88% hides the 60-record observability defect; reporting only 93% can make reference-data unavailability look like known bad values. Report pass, fail, and unknown counts, both labeled rates, rule version, population, window, and remediation owner.

### Answer 3

Record the corrected value, authority, effective time, correction time, prior value reference, and reason under the operational authority. Publish an identified correction event. The cache refreshes or invalidates; the search index and warehouse consume the correction with observable lag; analytical outputs record which snapshot they used. The partner receives a versioned correction with acknowledgment and escalation if contractual timing is missed.

The audit log should normally append the correction rather than rewrite history. Backups may retain old values under protected retention and restore-time reapplication rules. Legal hold or immutable records may constrain deletion. Maintain a reconciliation ledger across copy type, last version, status, owner, evidence, and exception. Declare which readers may use stale data and which must consult the authority.

### Answer 4

A single enterprise model can standardize identifiers and reduce repeated mapping, but “customer” may become an overloaded compromise and central change can block teams. It also creates a broad privacy and failure boundary. If used, scope authority per fact and permit context-specific extensions rather than claiming universal semantics.

Bounded billing, support, delivery, and analytics models preserve their decisions: payer and contract, contact case, recipient and address, or analytical subject. They require explicit mapping, source identities, conflict policy, lineage, and versioned contracts. Some mappings are partial: a recipient need not be the payer, and an analytical cluster must not become an authorization identity.

A sound design may share a governed core identity while retaining bounded representations and authorities. Compare false merge/split risk, unavailable authority behavior, privacy purpose, change cadence, translation ownership, and correction propagation. No design eliminates semantic governance.

### Answer 5

Define sample, probe observation, station, water body, analyte, calibration, maintenance action, weather observation, assessment, and alert as separate concepts. Each measurement carries station and sensor or laboratory identity, coordinate reference, depth, method, unit, detection limit, precision, event time, receipt time, calibration version, quality flag, and original representation. Below-detection-limit is not zero; missing, invalid, and not sampled are distinct.

Laboratories own certified sample results; probes own raw observations under calibration status; the regional assessment authority owns published classifications and alerts. Transformations normalize units, align location and time windows, handle censored values under declared methods, and preserve originals. Lineage binds source records, calibration, reference thresholds, transformation and model versions, reviewer, and alert.

Quality rules cover calibration validity, plausible rate of change, duplicate samples, spatial coverage, timeliness, and unresolved conflicts with explicit populations. Maintenance-worker and citizen identities are minimized and access-controlled. Raw high-frequency data, certified records, alerts, corrections, backups, and derived public aggregates receive different retention rules. A correction creates a new version, triggers affected assessments, and preserves the historical decision record. Public alerts expose evidence and uncertainty without revealing protected identities or implying measurements prove conditions outside their spatial and temporal support.
