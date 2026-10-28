---
module_id: DARCH-027
program: Data Architecture Engineering
level: 1
module_number: 27
title: Producer and Consumer Contracts
status: complete
last_verified: 2026-09-03
---

# Producer and Consumer Contracts

## One-Page Review

### Governing question

How can data producers and consumers establish reciprocal, testable, evolvable contracts for meaning, interfaces, quality, service, protection, change, correction, and lifecycle without reducing the agreement to a schema file or transferring all responsibility to one side?

### Essential definitions

- A **producer** creates, adopts, transforms, publishes, or operates data through a governed interface.
- A **consumer** retrieves, subscribes to, transforms, presents, or uses data for a declared decision, workflow, model, product, or obligation.
- A **data contract** is a versioned agreement among accountable parties covering purpose, scope, semantics, interface, quality, service, protection, change, evidence, remedies, and lifecycle.
- A **semantic contract** defines claims, identifiers, grain, time, units, codes, constraints, provenance, derivations, and interpretation limits.
- An **interface contract** defines the technical exchange surface, including protocol, schema, serialization, ordering, delivery, errors, authentication, and compatibility.
- A **consumer declaration** records intended purpose, decisions, populations, transformations, dependencies, protection, service need, and contact.
- **Compatibility** is the ability of declared consumers to continue correct and safe operation after a change; it includes semantics and policy, not only parsing.
- A **contract test** evaluates a machine-checkable obligation at a declared boundary and version; it cannot prove all semantic, legal, or operational obligations.
- A **material change** can affect meaning, fitness, protection, cost, service, or consumer action even when the physical schema is unchanged.
- A **remedy** is the agreed response to nonconformance, such as notice, containment, correction, replay, migration support, escalation, credit, or termination.

### Central model, mechanism, or theorem

Represent a producer-consumer contract as:

`K = (parties, purpose, scope, semantics, interfaces, quality, service, protection, change, evidence, remedies, lifecycle)`

Represent an obligation as:

`o = (actor, trigger, behavior, object, condition, deadline, evidence, exception, escalation)`

A viable contract is reciprocal and bounded. Producers publish accurate descriptions, conforming interfaces, agreed quality and service, change notice, support, and correction. Consumers declare purposes and critical dependencies, validate fitness, use supported interfaces, protect data, report defects, handle errors, and migrate. Accountability remains scoped: a producer cannot guarantee every downstream decision, and a consumer cannot excuse misuse by pointing to technically conforming input.

### Critical invariants

- Every material contract names durable producer and consumer roles, accountable owners, operational contacts, versions, and effective intervals.
- Purpose, users, decisions, populations, jurisdictions, and prohibited uses are explicit enough to assess fitness and protection.
- Semantic obligations cover claims, keys, grain, time, units, codes, nulls, derivations, provenance, uncertainty, and limitations.
- Interface conformance, semantic correctness, quality, service, protection, and decision fitness remain distinct contract dimensions.
- Producers provide change classification and notice; consumers register critical dependencies and complete migrations within agreed support windows.
- Contract tests execute at producer, integration, and consumer boundaries but never substitute for domain, risk, privacy, security, legal, or outcome review.
- Defects and corrections trace affected versions, periods, populations, downstream products, decisions, and evidence without silently overwriting history.
- Consumer transformations create new claims and obligations; lineage does not transfer accountability indefinitely upstream.
- Emergency changes, exceptions, waivers, and overrides are bounded, evidenced, communicated, reviewed, and retired.
- Contract closure addresses consumers, copies, access, retention, holds, historical reproducibility, corrections, and successor obligations.

### Common failures

Common failures are calling a JSON schema the entire contract; naming a team mailbox as both parties; omitting consumer purpose; accepting “analytics” as a use; promising all downstream fitness; requiring consumers to discover breaking changes; treating added fields as always compatible; changing code meaning without schema change; assuming registry validation proves semantics; allowing unregistered consumers but making no unknown-use provision; letting consumers copy data without retention or incident duties; rejecting valid defect reports because transport succeeded; correcting current data without downstream replay; keeping exceptions forever; and deleting retired interfaces while historical decisions remain unreproducible.

### Compact example

The Orders producer exposes events used by Fulfillment and Revenue. A schema registry verifies types, yet a producer changes `status=fulfilled` from “handed to carrier” to “delivered.” Every message still parses, but both consumers act incorrectly. The contract is expanded to define event claims, lifecycle state, effective time, key and ordering rules, quality and service objectives, supported versions, semantic change classification, consumer registrations, test fixtures, notice, migration, correction, and incident escalation. Fulfillment and Revenue declare distinct purposes and validate their own downstream behavior.

### Connections

[DARCH-025](025-source-aligned-aggregate-and-consumer-aligned-data.md) establishes product responsibilities, while [DARCH-026](026-data-products-and-service-expectations.md) makes service behavior measurable. This module binds producers and consumers before [DARCH-028](../ROADMAP.md) analyzes cross-domain dependencies, [DARCH-029](../ROADMAP.md) develops discoverability, and [DARCH-030](../ROADMAP.md) governs portfolios and lifecycle.

## Governing Question

Data crosses an organizational boundary whenever one role publishes and another relies on it, even if both use the same database. The consumer builds assumptions about meaning, timing, quality, errors, and change. The producer builds assumptions about intended use, demand, support, protection, and migration. When those assumptions remain implicit, integration works until an ordinary change exposes disagreement.

A contract makes the relationship inspectable. It does not freeze change or transfer all risk. It states what each side controls, how fitness is evaluated, how evidence is produced, and how disputes, incidents, corrections, and evolution proceed.

## Why This Matters

Schema drift is visible, but semantic drift is often more damaging. A field can retain its name and type while changing unit, population, effective-time rule, source authority, derivation, or permitted use. Technical compatibility checks will pass while decisions fail.

Conversely, not every schema change is materially breaking. A new optional field may be harmless to tolerant consumers, while a corrected description may improve shared meaning. Contract discipline lets teams distinguish syntax, behavior, semantics, service, and policy instead of blocking all change or trusting every change.

The [OpenAPI Specification 3.1.1](https://spec.openapis.org/oas/v3.1.1.html) defines a language-agnostic interface description for HTTP APIs. [AsyncAPI 3.0.0](https://www.asyncapi.com/docs/reference/specification/v3.0.0) describes message-driven interfaces. These specifications support machine-readable exchange contracts but do not determine domain authority, consumer fitness, or lawful use.

[JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12/json-schema-core) defines a core for schema validation and annotation. The [CloudEvents 1.0.2 specification](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md) defines common event metadata. Both improve interoperable validation and event context while leaving business semantics and delivery consequences to the contract.

W3C [DCAT 3](https://www.w3.org/TR/vocab-dcat-3/) supports catalog descriptions of datasets, distributions, services, and relationships. W3C [PROV-O](https://www.w3.org/TR/prov-o/) supports provenance involving entities, activities, agents, and derivations. Discoverability and provenance make obligations traceable, but organizational evidence is still required.

Google's [SRE chapter on Service Level Objectives](https://sre.google/sre-book/service-level-objectives/) provides useful distinctions among indicators, objectives, and agreements. NIST's [Privacy Framework 1.0](https://www.nist.gov/privacy-framework/privacy-framework) provides risk-oriented privacy activities. Contracts must combine service value with purpose and protection instead of optimizing delivery alone.

## Prerequisites and Retrieval

You should understand data products, domains, ownership, stewardship, schemas, events, APIs, quality, service objectives, lineage, provenance, identity, temporal semantics, privacy, security, records, and lifecycle.

Retrieve producer, consumer, contract, obligation, party, purpose, semantic contract, interface, schema, event, endpoint, grain, key, time, quality, SLI, SLO, version, compatibility, breaking change, notice, migration, deprecation, contract test, fixture, lineage, correction, remedy, exception, and termination.

As a retrieval test, inspect “Consumers agree to schema version 4.” Ask who those consumers are; what purposes and decisions they own; which semantics, interfaces, quality, service, protection, and change rules apply; which tests establish conformance; what happens on failure; how versions coexist; and when obligations end. A version number alone cannot answer any of these.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish data contracts from schemas, documentation, service objectives, policies, agreements, and informal expectations;
2. identify producer, consumer, owner, steward, custodian, platform, control, provider, and governing responsibilities;
3. specify purpose, scope, claims, keys, grain, time, units, codes, nulls, derivations, provenance, and limitations;
4. define interface, quality, service, support, protection, evidence, change, remedy, and lifecycle obligations;
5. create consumer declarations that expose decision context, criticality, dependencies, transformations, copies, and migration capability;
6. classify syntactic, behavioral, semantic, quality, service, and policy compatibility for declared consumers;
7. design producer, integration, consumer, monitoring, and recovery tests with explicit evidentiary limits;
8. govern defects, incidents, corrections, replay, restatement, exceptions, disputes, and escalation across boundaries;
9. manage discovery, negotiation, versions, notice, migration, deprecation, unknown consumers, and contract closure;
10. audit reciprocal fulfillment without assuming conformance guarantees correct or lawful downstream decisions.

## Core Exposition

**Begin with parties and decisions.** Name durable producer and consumer roles, accountable owners, stewards, technical operators, and support contacts. Record incumbents separately. A shared mailing list can route work but cannot accept accountability.

For each consumer, identify decisions, workflows, populations, frequency, time, consequence, alternatives, and downstream products. “Analytics” is too broad. Monthly workforce planning, real-time fraud intervention, and statutory reporting impose different obligations.

**Define contract scope.** State product, interfaces, versions, assertions, populations, jurisdictions, environments, start, review, expiry, and exclusions. A contract for one curated table does not silently govern every file in its storage account.

Scope dependencies and derived outputs where relevant. Avoid clauses such as “all future consumer uses” or “all producer data.” Broad language produces untestable obligations and unsafe assumptions.

**Separate contract layers.** The semantic layer describes claims and interpretation. The interface layer describes technical exchange. The quality layer describes fitness characteristics and measures. The service layer describes timing, availability, support, and recovery. The protection layer describes permitted handling. The change layer governs evolution.

These layers relate but do not collapse. A message can satisfy JSON Schema and still carry the wrong unit. A correct value can arrive too late. An available interface can expose data for an undeclared purpose.

**Write semantic claims.** Define subjects, predicates, source authority, adoption rules, identifiers, grain, cardinality, time, units, codes, nulls, defaults, corrections, and uncertainty. For derived values, define inputs, transformations, parameters, versions, and limitations.

Use examples and counterexamples. A formal schema expresses structure well but may not capture the difference between order acceptance, shipment, delivery, and settlement. Narrative and machine-readable semantics should reinforce each other.

**Define identifiers.** State business keys, technical keys, namespace, stability, uniqueness, merge, split, rotation, and mapping behavior. Consumers should not assume an internal row identifier persists across reload or provider migration.

Composite keys and effective intervals can be part of identity. If matching is probabilistic, expose method, confidence, review, and correction rather than presenting a resolved identifier as observed fact.

**Define grain and cardinality.** State what one record, event, row, object, or response represents. For collections, define uniqueness and expected relationships. For repeated messages, distinguish retransmission, duplicate, correction, and new business event.

Consumers must preserve grain or document transformations. Many double-counting failures arise when technically compatible products are joined at different grains. Contract tests can assert uniqueness and cardinality at relevant samples or populations.

**Define time.** Distinguish event, business-effective, source-record, publication, ingestion, processing, correction, and observation times. State timezone, precision, calendars, ordering, lateness, watermark, and restatement.

An event contract should say whether ordering is global, per key, per partition, or absent. Consumers define their late-data and replay behavior. Producers should not promise global ordering that infrastructure cannot provide.

**Define values and nulls.** Document units, scale, currency, sign, rounding, value domains, code authorities, and effective periods. Separate unknown, not applicable, withheld, not collected, invalid, and absent when the distinction matters.

Defaulting missing values can improve convenience but conceal uncertainty. If a contract permits coercion or imputation, label the result and preserve evidence. Consumers own any additional imputations they introduce.

**Define the interface.** Specify protocol, endpoint or topic, method or operation, schema, serialization, compression, pagination, filtering, partitioning, authentication, authorization, delivery, acknowledgement, retry, idempotency, ordering, and error behavior.

OpenAPI, AsyncAPI, JSON Schema, and CloudEvents can express important pieces. Treat specifications as governed artifacts with owners, versions, validation, publication, and change review. Extensions need namespaces and documented interpretation.

**Define delivery semantics honestly.** Terms such as at-most-once, at-least-once, and exactly-once require scope. Exactly-once processing at one broker boundary does not prove one business effect across consumers and side effects.

Provide event identifiers, idempotency keys, replay ranges, retention, ordering scope, duplicate expectations, and acknowledgement meaning. Consumers implement deduplication and idempotent effects where required.

**Define errors.** State how invalid requests, rejected records, partial results, unavailable dependencies, throttling, authorization denial, stale data, poison messages, and internal failures appear. Silent row dropping is rarely acceptable.

Errors should be actionable without disclosing protected internals. Define retryability, consumer correction, producer response, support path, correlation identifiers, and evidence retention.

**Define quality obligations.** For each characteristic, state population, method, window, target, evidence, severity, exception, and response. Source-aligned products may emphasize source fidelity and completeness; aggregates emphasize reconciliation and transformation; consumer products emphasize decision fitness.

Producers report known limitations and missing evidence. Consumers validate critical assumptions at their boundary. Passing producer tests does not eliminate consumer-context checks.

**Define service obligations.** Include freshness, latency, availability, publication schedule, correction time, recovery, support, and communication. Every objective needs an indicator, eligible population, clock, window, target, exclusions, measurement source, breach, and response.

Consumers state required behavior rather than requesting maximal reliability. Producers expose dependencies and achievable tiers. Formal SLAs require legal and commercial review where applicable.

**Define protection obligations.** Record purpose, permitted users, data categories, classification, minimization, access, encryption, locations, providers, sharing, logging, retention, deletion, incident, audit, and jurisdictional constraints.

A producer's willingness to publish does not authorize every downstream use. Consumers remain accountable for purpose, derived copies, access, models, reports, and onward sharing. Qualified privacy, security, legal, records, and ethics review is required by context.

**Create consumer declarations.** A consumer declaration names product version, purpose, decision, population, criticality, interface, expected volume, required service, transformations, downstream dependencies, copies, controls, contact, and migration window.

This is not bureaucracy for every exploratory query. Apply consequence thresholds. Promotion from exploration to recurring or material use should trigger registration and product obligations.

**Make contracts reciprocal.** Producer duties include accurate description, supported interface, quality evidence, service operation, protection, notice, support, correction, and lifecycle. Consumer duties include fitness assessment, supported use, credentials, limits, validation, error handling, feedback, migration, and retirement of copies.

Neither party can outsource judgment entirely. Producers cannot guarantee decisions they do not control. Consumers cannot ignore published limitations or transform data into new claims without owning them.

**Represent obligations precisely.** Write each obligation with actor, trigger, behavior, object, condition, deadline, evidence, exception, and escalation. “Producer will provide timely notice” is weaker than “product owner notifies registered critical consumers at least thirty days before a planned semantic break, except under the documented emergency-change path.”

Avoid promising absolute perfection. State measurable targets and bounded remedies. Some legal, safety, or security controls may be absolute policies rather than budgeted objectives.

**Negotiate from evidence.** Producers bring observed quality and service, architecture constraints, dependency contracts, cost, roadmap, and incident history. Consumers bring decision needs, consequence, alternatives, volume, timing, and migration ability.

Record rejected options and assumptions for material choices. If requirements exceed capability, fund improvement, offer a different tier, create a consumer-specific product, or reject the use. Do not agree and quietly underdeliver.

**Version the contract.** Version semantic, interface, quality, service, protection, and lifecycle components. A single product version can reference component versions, but consumers need a coherent resolved contract.

Use immutable history and effective intervals. Never edit the past definition so old evidence appears conforming. Label drafts, approved versions, deprecated versions, and retired versions clearly.

**Classify change on several axes.** Syntactic change affects parsers. Behavioral change affects delivery or errors. Semantic change affects meaning, grain, time, population, authority, or derivation. Quality and service changes affect fitness. Policy changes affect permitted use or handling.

A new optional field is not always compatible if consumers reject unknown properties or if its presence changes interpretation. Removing a field is not always breaking if no declared consumer uses it, but unknown consumers remain a risk to manage.

**Define compatibility from consumers.** Producer-side schema rules provide fast screening. Consumer-driven contract tests demonstrate expectations for known uses. Integration tests exercise exchange. Production monitoring observes actual behavior.

No one test proves universal compatibility. Maintain a matrix of registered consumers, versions, assumptions, criticality, tests, and migration. Sample semantic and protection effects that code cannot infer.

**Test producer obligations.** Validate schema, required metadata, keys, grain, code domains, temporal rules, quality, error behavior, example fixtures, version publication, and service telemetry before release.

Tests should fail safely and preserve actionable evidence. Generated examples must not leak real sensitive data. Review test coverage and false assurance; a passing fixture represents only its declared cases.

**Test consumer obligations.** Verify supported interface use, tolerant or strict parsing as declared, identity handling, duplicates, ordering, late data, nulls, corrections, errors, access, retention, and migration. Test decisions under degraded input.

Consumers own tests for transformations and downstream outcomes. Reusing producer fixtures helps but does not prove the consumer interpretation. Include negative and boundary cases.

**Use contract tests in delivery.** Run fast checks during authoring, broader integration checks before release, and boundary monitoring in operation. Pin contract and fixture versions. Report which environment and evidence each result covers.

Avoid a central test suite that no party owns. Failed checks need routing, authority, and resolution. Emergency bypasses require reason, scope, approval, expiry, monitoring, and retrospective repair.

**Publish discoverable contracts.** Catalog product, purpose, parties, versions, interfaces, semantics, quality, service, protection, examples, lineage, support, changes, incidents, and lifecycle. Provide machine-readable artifacts and human explanation.

Discovery is not authorization. Catalog visibility should not expose secrets, personal data, vulnerabilities, or confidential contract terms. Use appropriate access while keeping obligations available to authorized consumers.

**Register dependencies.** Link consumers to exact product and contract versions. Capture criticality and contact so notice and incidents reach affected parties. Use runtime lineage and access evidence to find unknown use.

Registration should create value through alerts, support, migration, evidence, and influence. If it only creates forms, consumers will bypass it. Unknown consumers require conservative change analysis, not permanent paralysis.

**Plan change notice.** A notice states what changes, why, affected semantics and interfaces, versions, dates, compatibility, consumer evidence, migration steps, tests, support, fallback, and deprecation.

Choose notice periods based on consumer consequence and migration effort. Track acknowledgement and migration for critical consumers. Publication without reaching operational contacts is not effective notice.

**Run migrations.** Support parallel versions, adapters, mapping, replay, validation, and rollback where risk warrants. Consumers test outputs and decisions, not only connectivity.

Measure migration progress from registered dependencies and observed use. Resolve stragglers by assistance, exception, escalation, or explicit termination. Do not keep every version forever by default.

**Handle emergency change.** Security, legal, corruption, provider, or safety events can require abbreviated notice. Define who authorizes, which consumers are contacted, what degraded behavior applies, how evidence is preserved, and when retrospective review occurs.

Emergency does not erase contract duties; it activates a different bounded path. Restore a supported stable state or publish a durable new version after containment.

**Operate defects and disputes.** A defect report includes product and version, expected and observed behavior, scope, time, evidence, consequence, affected decision, and urgency. Protect sensitive samples.

The producer validates contract conformance; the consumer validates use and transformation. If interpretation differs, stewards and owners review semantics and evidence. Escalation has deadlines and one final authority per scoped decision.

**Correct across the graph.** Determine source cause, affected product versions, periods, populations, consumers, derived products, reports, models, exports, and decisions. Communicate containment, correction, replay, restatement, and limitations.

Preserve both corrected values and evidence of values used historically when required. Consumers own downstream recomputation and decision response under their contract; producers provide bounded correction evidence and support.

**Define remedies.** Internal remedies can include notice, priority correction, support, replay, migration extension, risk escalation, funding, or service review. Commercial agreements may include credits, damages, or termination subject to qualified review.

A service credit rarely repairs a harmful decision. Remedies should prioritize containment, correction, consumer action, learning, and prevention. Avoid incentives to hide nonconformance.

**Govern exceptions.** Record obligation, scope, reason, consequence, controls, approver, parties, evidence, start, expiry, remediation, review, and residual risk. Consumers affected by a material exception need notice.

Do not let repeated waivers become shadow contract. Change the architecture, fund correction, revise the obligation transparently, or discontinue the unsupported use.

**Manage third parties.** Map vendor licenses, provenance, service, quality, correction, audit, security, privacy, location, subcontractor, retention, exit, and termination terms into producer-consumer obligations.

The internal producer cannot promise rights or reliability it did not obtain. Provider limitations remain visible. Maintain alternatives and export evidence for critical products.

**Control cost and demand.** Contracts can specify volume, query patterns, rate, concurrency, retention, egress, and cost allocation. Producers publish capacity and throttling behavior; consumers avoid unbounded or abusive use.

Cost controls must not silently corrupt results. Sampling, truncation, stale caches, or approximate computation require explicit semantics. Capacity changes follow notice and review.

**Measure contract health.** Track registered critical consumers, version adoption, test coverage, conformance, quality and service attainment, changes, notice, migrations, incidents, defects, correction, exceptions, support, and unknown use.

Avoid rewarding number of contracts signed. Sample whether parties understand and exercise them, whether evidence is trustworthy, and whether consumer outcomes improve. High defect reporting can reflect strong detection rather than poor quality.

**Audit reciprocity.** Sample producer claims and consumer declarations. Recompute measures, trace provenance, inspect access and copies, replay a correction, test notice, and exercise escalation. Verify that each party fulfills its own obligations.

Independent review is valuable for high-consequence products. Separate self-attestation, automated tests, operational observations, consumer evidence, and external assurance.

**Manage transfer and succession.** Reorganization, provider change, platform migration, acquisition, or staffing change can alter parties and capacity. Transfer contracts, open defects, exceptions, versions, consumers, tests, evidence, access, support, and liabilities explicitly.

Require successor acceptance and effective dates. A renamed team does not automatically inherit semantic knowledge or operational ability.

**Terminate deliberately.** Contract closure inventories consumers, dependencies, copies, reports, models, credentials, incidents, corrections, retention, legal holds, archival evidence, and successor products. Provide final notice, migration, and support windows.

Remove obsolete access and automated exchange after evidence of closure. Preserve contract history long enough to explain past decisions and fulfill obligations. Termination of delivery does not erase historical accountability.

**Treat contracts as living governance.** Review after material consumer, risk, architecture, dependency, provider, regulatory, cost, or product change. Keep ordinary evolution lightweight while demanding stronger evidence for consequential changes.

The final test is operational: can both parties explain what is exchanged, what it means, why it is fit for the declared use, how each side behaves, how change and failure are handled, and what evidence resolves disagreement? If not, the “contract” is only a schema or promise.

## Definitions and Notation

Let producer `p` and consumer `c` agree on contract `K = (P,S,I,Q,V,R,H,E,M,L)`, where `P` is parties and purpose, `S` semantic scope, `I` interfaces, `Q` quality, `V` service, `R` protection and restrictions, `H` change handling, `E` evidence, `M` remedies, and `L` lifecycle.

An obligation is `o = (actor, trigger, behavior, object, condition, deadline, evidence, exception, escalation)`. Let `Fulfilled(o,t)` mean required evidence shows the obligation was satisfied for its scope at time `t`; absence of detected violation is not equivalent.

Let compatibility vector `X = (x_syntax, x_behavior, x_semantics, x_quality, x_service, x_policy)` for a declared consumer and change. Overall compatibility is not true unless every required dimension for that consumer is acceptable or an approved migration or exception exists.

Represent a registration as `G = (consumer_role, purpose, decision, criticality, product_version, interface, dependencies, transformations, controls, service_need, contact, migration)`. Registration evidence supports impact analysis but does not prove complete consumer discovery.

Contract coverage compares required relationships `D*` with active contracts `K*` and reports missing party, purpose, semantics, test, compatibility policy, incident path, protection term, evidence, migration, or lifecycle rule.

## Mechanisms, Invariants, or Proof Structure

Use ten gates for each material producer-consumer contract.

**1. Party gate.** Name durable roles, accountable owners, stewards, operators, contacts, deputies, authority, and effective intervals.

**2. Purpose gate.** Define users, decisions, populations, jurisdictions, criticality, expected value, alternatives, and prohibited uses.

**3. Semantic gate.** Specify claims, sources, keys, grain, time, units, codes, nulls, derivations, provenance, uncertainty, and limitations.

**4. Interface gate.** Specify operations, protocols, schemas, serialization, identity, delivery, ordering, retries, errors, access, and examples.

**5. Quality and service gate.** Define measures, populations, targets, windows, evidence, availability, freshness, correction, recovery, support, and response.

**6. Protection gate.** Apply purpose, minimization, privacy, security, records, licensing, sharing, provider, jurisdiction, audit, incident, and deletion duties.

**7. Compatibility gate.** Classify syntactic, behavioral, semantic, quality, service, and policy change with tests, notice, versions, and unknown-use treatment.

**8. Operation gate.** Implement discovery, registration, negotiation, monitoring, support, defects, disputes, incidents, corrections, exceptions, and remedies.

**9. Evidence gate.** Preserve approved contracts, test results, telemetry, notices, acknowledgements, decisions, exceptions, migrations, outcomes, and limitations.

**10. Lifecycle gate.** Review, exercise, fund, revise, transfer, deprecate, terminate, revoke, archive, and close obligations deliberately.

The executable example checks four narrow contract failures: missing producer owner, absent consumer purpose, missing compatibility policy, and missing incident path.

<!-- bijux-verify: {"id":"producer-consumer-contract-integrity","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"contracts=4\nvalid=0\nfindings=claims-api:missing-compatibility-policy,customer-events:missing-consumer-purpose,orders-stream:missing-producer-owner,revenue-table:missing-incident-path\nready=false\n","stderr":""}} -->
```python
contracts = (
    {"id": "orders-stream", "producer_owner": False, "consumer_purpose": True, "compatibility": True, "incident_path": True},
    {"id": "customer-events", "producer_owner": True, "consumer_purpose": False, "compatibility": True, "incident_path": True},
    {"id": "claims-api", "producer_owner": True, "consumer_purpose": True, "compatibility": False, "incident_path": True},
    {"id": "revenue-table", "producer_owner": True, "consumer_purpose": True, "compatibility": True, "incident_path": False},
)

findings = []
valid = 0
for contract in contracts:
    local = []
    if not contract["producer_owner"]:
        local.append("missing-producer-owner")
    if not contract["consumer_purpose"]:
        local.append("missing-consumer-purpose")
    if not contract["compatibility"]:
        local.append("missing-compatibility-policy")
    if not contract["incident_path"]:
        local.append("missing-incident-path")
    if local:
        findings.extend(f"{contract['id']}:{finding}" for finding in local)
    else:
        valid += 1

print(f"contracts={len(contracts)}")
print(f"valid={valid}")
print("findings=" + ",".join(sorted(findings)))
print(f"ready={str(valid == len(contracts)).lower()}")
```

The checker validates four declared contract predicates only. It does not prove authority, semantic correctness, interface interoperability, quality, service fulfillment, lawful purpose, adequate protection, compatibility, consumer fitness, incident readiness, remedy enforceability, or production adoption. Those require approved contracts, domain review, generated and sampled tests, integration evidence, operational measurements, exercises, consumer validation, risk and legal review, and accountable acceptance.

## Alternatives and Trade-Offs

**Bilateral versus standardized contracts.** Bilateral negotiation fits special needs but multiplies variation. Standard templates improve scale but can hide context. Establish minimum clauses and extension points, with stronger review for deviations.

**Producer-driven versus consumer-driven tests.** Producer tests cover published behavior consistently; consumer tests reveal real dependencies. Use both and define ownership so neither becomes unmaintained central glue.

**Strict versus tolerant consumption.** Strict parsing exposes unexpected change early but rejects harmless extension. Tolerant parsing supports additive evolution but can hide ignored meaning. Declare extension and unknown-field policies by interface.

**Single versus parallel versions.** One version minimizes operating cost but forces synchronized migration. Parallel versions reduce consumer risk but increase support, correction, and security burden. Bound coexistence with evidence-backed windows.

**Central registry versus distributed contracts.** Central discovery improves consistency and impact analysis; distributed repositories align with product delivery. Federate authoring while publishing authoritative versions and relationships centrally.

**Automated enforcement versus human review.** Automation scales structural, compatibility, and policy checks. Humans evaluate meaning, purpose, risk, exceptions, and consequences. Make both forms of evidence explicit.

**Known-consumer stability versus producer autonomy.** Registered dependencies justify notice and support; excessive coupling can block change. Segment critical consumers, version interfaces, and fund migration rather than promise immobility.

**Rich evidence versus minimization.** Detailed contracts, samples, telemetry, and incidents improve assurance but can expose sensitive data or vulnerabilities. Use synthetic fixtures, controlled evidence, access, retention, and redaction.

## Failure Modes and Misconceptions

1. **A schema is the contract.** It omits purpose, semantics, quality, service, protection, change, remedies, and lifecycle.
2. **The producer owns every downstream outcome.** Consumers own their transformations, interpretation, decisions, and controls.
3. **Consumers only receive obligations.** They must declare purpose, needs, dependencies, handling, feedback, and migration.
4. **Parsing means compatibility.** Meaning, behavior, quality, service, and policy can break independently.
5. **Adding an optional field is always safe.** Strict consumers, code generation, and changed interpretation can break.
6. **No schema change means no breaking change.** Units, codes, populations, grain, time, and derivation can change.
7. **Exactly once eliminates duplicate effects.** Scope, replay, retries, transactions, and downstream side effects still matter.
8. **A registry proves semantics.** Structural validation cannot determine domain truth or consumer fitness.
9. **Unknown consumers prohibit evolution.** Discovery, monitoring, versions, notice, and bounded support manage uncertainty.
10. **A catalog grants permission to use.** Discovery is not access, purpose, legal, or ethical authorization.
11. **Passing producer tests proves consumer behavior.** Consumer transformations and decisions require their own evidence.
12. **Emergency change cancels obligations.** It activates bounded authority, communication, evidence, and review.
13. **Current correction repairs all history.** Downstream products, reports, models, exports, and past decisions require analysis.
14. **A service credit is a complete remedy.** Harm containment, correction, communication, learning, and prevention remain.
15. **More signed contracts mean stronger governance.** Understanding, conformance, response, and outcomes matter.
16. **Reorganization transfers contracts automatically.** Successors need knowledge, authority, capacity, evidence, and acceptance.
17. **Stopping delivery ends the contract.** Copies, access, retention, holds, corrections, and historical evidence may remain.

## Worked Examples

### Example 1

An Orders event retains its schema while `fulfilled` changes meaning. Semantic compatibility fails. The producer publishes a new event version, mapping, notice, fixtures, and migration; consumers validate their workflows before cutover.

### Example 2

A consumer assumes global event ordering, but the producer guarantees order only per account key. The contract exposes partitioning and replay. The consumer redesigns aggregation to use keys, event identifiers, and idempotent updates.

### Example 3

A source product emits null for withheld, unknown, and inapplicable values. The contract introduces explicit reason codes. Consumers migrate models and reports so missingness retains its domain and protection meaning.

### Example 4

A regulator-facing report consumes a revenue table as “analytics.” Registration names the statutory decision, critical periods, reconciliation need, correction, retention, and escalation. Producer and consumer strengthen service and evidence accordingly.

### Example 5

Consumer-driven tests pass for schemas but a currency switches from cents to units. Semantic fixtures and invariant checks detect magnitude failure. The release blocks until a versioned field and migration are ready.

### Example 6

A provider outage prevents publication. The internal producer communicates affected products and periods, activates a verified fallback, and preserves correction responsibility even though provider terms offer a financial credit.

### Example 7

A consumer copies sensitive data into a feature store beyond agreed retention. Reciprocal audit identifies the breach; access and copies are contained, incident analysis proceeds, and the consumer contract and controls are corrected.

### Example 8

An unknown consumer appears during deprecation. Runtime evidence identifies its queries, but no owner exists. Governance bounds a temporary extension, locates accountability, measures risk, and prevents indefinite anonymous support.

### Example 9

A defect correction restates three months of source data. Registered consumers receive affected keys and periods; aggregates replay and reconcile; reports preserve original-decision evidence and publish corrected results under policy.

### Example 10

A retired API still supports archived investigations. Active delivery ends, but contract history, schemas, provenance, access, retention, and correction contacts transfer to an archive role until obligations expire.

## Cross-Program Connections

- **API and service engineering:** OpenAPI, AsyncAPI, authentication, errors, compatibility, versioning, reliability, and deprecation implement interface obligations.
- **Data engineering:** schemas, orchestration, events, tests, registries, lineage, quality, replay, backfill, and serving operationalize contracts.
- **Platform engineering:** catalogs, policy, identity, contract testing, delivery controls, telemetry, discovery, and workflows enable scale.
- **Product management:** users, value, tiers, support, roadmaps, negotiation, adoption, migration, and retirement shape reciprocal commitments.
- **Security and privacy:** purpose, access, minimization, providers, sharing, incidents, retention, evidence, and audit constrain exchange.
- **Software engineering:** consumer-driven contracts, semantic versioning, dependency management, testing, releases, and compatibility provide mature patterns.
- **Legal and commercial practice:** agreements, remedies, licensing, liability, jurisdiction, termination, and provider duties require qualified review.
- **Systems engineering:** interface control, requirements allocation, verification, configuration baselines, change control, traceability, and lifecycle assurance structure contracts.

## References

1. OpenAPI Initiative, *OpenAPI Specification 3.1.1*, 2024. <https://spec.openapis.org/oas/v3.1.1.html>
2. AsyncAPI Initiative, *AsyncAPI Specification 3.0.0*, 2023. <https://www.asyncapi.com/docs/reference/specification/v3.0.0>
3. JSON Schema, *JSON Schema Core: A Media Type for Describing JSON Documents*, Draft 2020-12, 2022. <https://json-schema.org/draft/2020-12/json-schema-core>
4. Cloud Native Computing Foundation, *CloudEvents Specification 1.0.2*, 2022. <https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md>
5. W3C, *Data Catalog Vocabulary (DCAT)—Version 3*, W3C Recommendation, 2024. <https://www.w3.org/TR/vocab-dcat-3/>
6. W3C, *PROV-O: The PROV Ontology*, W3C Recommendation, 2013. <https://www.w3.org/TR/prov-o/>
7. Beyer, B., Jones, C., Petoff, J., and Murphy, N. R., eds., *Site Reliability Engineering: Service Level Objectives*, Google, 2016. <https://sre.google/sre-book/service-level-objectives/>
8. NIST, *Privacy Framework: A Tool for Improving Privacy through Enterprise Risk Management*, Version 1.0, 2020. <https://www.nist.gov/privacy-framework/privacy-framework>

## Exercises

### Exercise 1

Design a producer-consumer contract for an Order Events stream used by Fulfillment, Revenue, and Customer Support. Define reciprocal duties, semantics, delivery, quality, service, protection, change, evidence, remedies, and lifecycle.

### Exercise 2

Analyze a change that adds an optional field, changes a status meaning, reduces freshness, and expands allowed purpose. Classify compatibility for three consumers and design version, notice, test, migration, and approval paths.

### Exercise 3

Create a contract-test strategy spanning producer, registry, integration, consumer, production monitoring, correction, and recovery. State exactly what each layer proves and does not prove.

### Exercise 4

Design a defect and correction workflow for a three-month historical error that affects an aggregate, a model, a regulatory report, and external exports. Include evidence, decisions, replay, communication, and closure.

### Exercise 5

Create a governance model for 500 contracts with known and unknown consumers. Include templates, extensions, discovery, ownership, versioning, automation, exceptions, audits, metrics, transfer, and retirement.

## Answers to the Exercises

### Answer 1

Name the Orders product owner and steward plus accountable owners and contacts for Fulfillment, Revenue, and Support. Define each consumer's purpose, decision, criticality, versions, service need, transformations, copies, and migration capacity. The semantic contract covers order and event identity, lifecycle claims, grain, per-order ordering, event and publication time, money units, status codes, null reasons, corrections, and source authority. The interface specifies topic, CloudEvents attributes, schema, serialization, authentication, authorization, partitioning, acknowledgement, retries, duplicate and replay behavior, retention, and errors.

Quality covers source completeness, identity, validity, temporal sequence, and publication fidelity. Service covers latency, freshness, availability, correction, recovery, support, and incident updates. Protection covers purpose, minimization, fields, access, retention, sharing, and audit. Producers maintain description, conformance, evidence, notice, correction, and support; consumers validate fitness, deduplicate, protect copies, report defects, and migrate. Change classification, tests, parallel versions, remedies, escalation, exceptions, review, and retirement complete the contract.

### Answer 2

Treat the proposal as four independent changes. The optional field may be syntactically additive for tolerant Fulfillment but breaking for a strict generated Revenue client; test each. The status meaning is semantically breaking for every consumer that acts on it even though schema is stable. Reduced freshness is a service change whose acceptability depends on decision deadlines. Expanded purpose is a policy change requiring producer authority plus privacy, security, legal, records, and consumer review as applicable.

Publish a new semantic and interface contract version when required. Provide old/new fixtures, status mapping, quality and service comparison, protection assessment, consumer-driven tests, and migration guidance. Give consequence-based notice and parallel support. Each consumer validates its transformations and decisions. The owner approves semantic scope, service governance approves the supported target, qualified control roles approve purpose changes, and unresolved or emergency cases use bounded escalation with evidence and expiry.

### Answer 3

Producer tests verify declared schemas, keys, domains, time rules, fixtures, quality controls, error forms, and artifact publication within their covered cases. Registry checks validate structural and configured compatibility rules. Integration tests verify protocol, authentication, serialization, delivery, and selected end-to-end examples. Consumer tests express actual parser, semantic, null, ordering, duplicate, transformation, and degraded-mode expectations.

Production monitoring observes real interface, quality, service, errors, and dependency behavior; it does not prove unmeasured semantics. Correction tests exercise affected-key identification, replay, idempotency, downstream reconciliation, and communication. Recovery tests verify restore, ordering, duplicates, history, access, lineage, and consumer outputs. Pin versions and preserve results. None alone proves domain truth, complete population, lawful purpose, every consumer, decision fitness, or all future behavior; combine domain review, sampled evidence, consumer validation, risk review, exercises, and accountable acceptance.

### Answer 4

Declare the defect with product and contract versions, affected claims, keys, populations, periods, evidence, consequence, and uncertainty. Protect samples and preserve original publication evidence. Identify downstream products through registrations, lineage, runtime use, exports, and owner outreach. An incident authority coordinates containment and updates while source and product owners decide correction within scope. Regulatory authority determines filing response; model owner determines retraining or rescoring; export owners address recipients and contracts.

Publish an affected-range manifest and corrected version. Replay source and aggregate idempotently, reconcile totals and quality, rerun model and report validation, and distinguish corrected data from values used in past decisions. Notify consumers with limitations and required action. Track external acknowledgement. Closure requires correction, downstream validation, residual risk, retained evidence, recurrence prevention, and accountable approvals. Operational restoration, regulatory closure, model remediation, and export correction can close on different dates.

### Answer 5

Define mandatory clauses for parties, purpose, semantics, interface, quality, service, protection, change, evidence, remedies, and lifecycle, with governed extensions for domain needs. Product repositories author versioned machine-readable and human contracts; an authoritative catalog publishes resolved versions, relationships, contacts, and status. Stable identifiers connect tests, telemetry, lineage, issues, and consumers. Automation checks completeness, schemas, compatibility, policy, expiry, notice, and migration.

Registration provides alerts, support, evidence, and influence so consumers benefit. Runtime and access evidence identify unknown use, which receives risk-based outreach and conservative change treatment without indefinite support. Federated owners approve local contracts under central minimums; cross-domain conflicts escalate. Track critical coverage, stale contracts, tests, conformance, incidents, changes, migrations, exceptions, unknown consumers, correction, and retirement—not raw contract count. Sample semantics and reciprocal duties, exercise failures, time-bound exceptions, explicitly transfer roles, and close delivery, copies, access, retention, holds, evidence, and successor obligations.
