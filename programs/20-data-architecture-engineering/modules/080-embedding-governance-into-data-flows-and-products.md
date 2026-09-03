---
module_id: DARCH-080
program: Data Architecture Engineering
level: 2
module_number: 80
title: Embedding Governance into Data Flows and Products
status: complete
last_verified: 2026-09-03
---

# Embedding Governance into Data Flows and Products

## One-Page Review

### Governing question

How should data products and flows carry ownership, meaning, purpose, policy, quality, security, privacy, residency, retention, provenance, and remedy through every lifecycle transition so governance is an observable product capability rather than a detached approval meeting, metadata form, or final release gate?

### Essential definitions

- A **data product** is an owned, versioned capability that supplies defined data or decisions to named consumers through supported interfaces, service expectations, governance, and lifecycle.
- A **data flow** is a graph of collection, receipt, validation, storage, transformation, publication, access, sharing, retention, deletion, and recovery transitions.
- A **data contract** is an attributable agreement describing product identity, schemas, semantics, ownership, quality, policy, service expectations, compatibility, evidence, and change procedures.
- A **control point** is a defined lifecycle boundary where context is evaluated and an action is allowed, denied, transformed, obligated, quarantined, or escalated.
- A **policy decision point** evaluates facts and rules to return a versioned decision and obligations.
- A **policy enforcement point** applies a decision at the resource and action boundary and reports the observed result.
- An **obligation** is a required action associated with a decision, such as masking, location restriction, logging, notification, retention assignment, review, or deletion.
- An **exception** is a bounded, authorized deviation with rationale, compensating controls, owner, affected scope, evidence, expiry, review, and revocation.
- A **policy bundle** is an immutable, attributable set of executable rules, data, schemas, tests, dependencies, and release metadata.
- A **governance assertion** links an object version to ownership, class, purpose, basis, contract, quality, location, retention, or other governed meaning with provenance and state.
- A **product acceptance gate** evaluates whether a data-product version is fit to publish for specified consumers and purposes; it is not a claim of universal correctness.
- **Continuous control monitoring** compares expected policy and controls with deployed configuration, decisions, actions, evidence, exceptions, and outcomes.
- **Control effectiveness** is evidence that a control produces its intended bounded risk or outcome improvement, not merely that configuration exists.
- A **quarantine** is a protected state that prevents ordinary consumption while preserving identity, evidence, ownership, and a path to disposition.
- A **governance receipt** records context, rule and decision versions, enforcement action, obligations, result, time, evidence, and limitations.
- **Closure** retires product versions, consumers, contracts, policy, exceptions, copies, access, schedules, and recovery paths while preserving required evidence and non-resurrection controls.

### Central model, mechanism, or theorem

Represent embedded governance as:

`G = (P, O, C, M, E, F, A, R, V, L)`

where `P` is product and purpose, `O` ownership and accountability, `C` contracts and controlled meaning, `M` metadata and provenance, `E` evaluation and enforcement, `F` flow and lifecycle, `A` assurance and evidence, `R` risk, exceptions, and remedy, `V` value and outcome measurement, and `L` lifecycle and closure. Governance is embedded when each important transition carries enough identity and context to make, enforce, observe, challenge, and recover the applicable decision. A catalog entry or green pipeline alone does not satisfy that condition.

### Critical invariants

- Product, dataset, schema, contract, assertion, policy, decision, enforcement action, obligation, exception, evidence, and outcome have separate stable identities and versions.
- Every product names accountable owner, domain, consumers, purposes, interfaces, semantics, quality, service expectations, policy, lifecycle, and support path.
- Every flow edge identifies immutable input and output versions, activity, agent, contract, policy context, location, effective time, and observed outcome.
- Governance context travels with the data or remains resolvable through stable protected references; names and mutable tags are insufficient.
- Decision and enforcement remain distinct: an allowed decision does not prove the write, transform, export, retention, or deletion happened correctly.
- Missing, stale, conflicting, inferred, waived, not applicable, and unknown governance state remains explicit and cannot silently become compliant.
- Controls apply at collection, write, read, transform, join, publish, share, export, retain, delete, restore, and retire boundaries according to risk.
- Fail-closed, quarantine, fail-open, degradation, and human-review behavior is selected explicitly for each boundary and failure mode.
- Exceptions are scoped and expiring, cannot rewrite base policy, and are visible to owners, consumers, assurance, incident, and recovery processes.
- Metrics distinguish metadata coverage, decision coverage, enforcement, effectiveness, operational cost, incidents, remedy, consumer value, and affected-party outcomes.
- Product and policy changes preserve compatibility and historical interpretation; rollback cannot reactivate revoked purpose, stale access, or deleted data.
- Recovery restores current identity, contract, policy, exceptions, keys, retention, deletion, and evidence before ordinary processing resumes.

### Common failures

Common failures include creating a catalog with no enforcement; calling every table a product; naming an owner who lacks authority or capacity; treating a schema as a full contract; storing policy in prose only; centralizing every decision in one committee; duplicating rules in every pipeline; trusting mutable tags; evaluating only at publication; ignoring reads, exports, restores, and deletions; treating policy decisions as observed outcomes; blocking critical operations when policy infrastructure fails without a safety design; failing open silently; allowing permanent exceptions; measuring only pass rates; rewarding metadata volume; coupling rules to physical names; breaking consumers without negotiated change; letting rollback restore obsolete permissions; and making governance so burdensome that teams route data around it.

### Compact example

Ten invented data-flow transitions are evaluated against seven declared governance requirements. Three are allowed; one each lacks an accountable owner or classification, has an incompatible schema, unauthorized purpose, disallowed residency, unknown retention, or unregistered consumer. Six products, eight lifecycle stages, three policy versions, and ten decisions are counted. Executable evidence confirms only those declarations and counts. It proves no real ownership, classification, contract, purpose, location, retention, enforcement, compliance, control effectiveness, product value, or beneficial outcome.

### Connections

[DARCH-061](061-metadata-architecture.md), [DARCH-064](064-lineage-architecture.md), [DARCH-069](069-metadata-apis-and-eventing.md), [DARCH-071](071-federated-data-governance.md), [DARCH-072](072-policy-as-code-for-data.md), and [DARCH-079](079-audit-and-provenance-architecture.md) establish metadata, provenance, interfaces, federated authority, executable policy, and evidence. [DARCH-081](../ROADMAP.md) next develops data-mesh principles.

## Governing Question

A dataset may have an owner and description in a catalog while an unregistered notebook reads it, a pipeline drops its purpose metadata, a replica moves to a forbidden region, a schema change silently alters meaning, and a restore revives an expired exception. Governance exists on paper yet fails in the flow.

The governing question is how to connect policy and accountability to every consequential data transition. Durable design makes compliant paths easier than bypasses, distributes authority to the correct domain, supplies shared enforcement primitives, records decisions and effects, measures outcomes, supports challenge and remedy, and continues to work during change, outage, migration, and recovery.

## Why This Matters

The NIST [Privacy Framework](https://www.nist.gov/privacy-framework) organizes privacy-risk management through Identify-P, Govern-P, Control-P, Communicate-P, and Protect-P functions and supports profiles tied to organizational priorities and systems, products, and services. It is a voluntary risk framework, not a prescriptive data-product implementation. Its lifecycle and governance emphasis helps connect product activities to privacy outcomes rather than to a single compliance flag.

NIST's [Cybersecurity Framework 2.0](https://www.nist.gov/cyberframework) adds the Govern function to Identify, Protect, Detect, Respond, and Recover and is intended for organizations of varied size and sector. Profiles, tiers, outcomes, supply chains, roles, policy, oversight, and continuous improvement help frame embedded controls. The framework does not select product-specific data semantics or legal duties.

NIST [SP 800-53 Release 5.2.0](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final) provides security and privacy controls across access, audit, assessment, configuration, contingency, identification, planning, program management, privacy processing, risk, acquisition, integrity, and supply chain. Controls are selected, tailored, implemented, and assessed within an authorization and risk context; attaching a control identifier to a dataset does not prove implementation or effectiveness.

W3C [DCAT 3](https://www.w3.org/TR/vocab-dcat-3/) models catalogs, datasets, data services, distributions, versions, series, relationships, qualified attributions, and resources for discovery and interoperability. It provides durable vocabulary for product discovery and distribution metadata. It does not define local ownership authority, service levels, access decisions, or product fitness.

W3C [Data Quality Vocabulary](https://www.w3.org/TR/vocab-dqv/) represents quality dimensions, metrics, measurements, policies, annotations, standards, and provenance. It supports attributable quality evidence instead of one `quality_score`. Organizations still choose valid dimensions, samples, thresholds, consequences, and decision processes.

W3C [ODRL Information Model 2.2](https://www.w3.org/TR/odrl-model/) represents policies with permissions, prohibitions, duties, assets, parties, actions, constraints, profiles, conflicts, and relations. It shows why use governance requires party, asset, action, context, and obligation rather than a sensitivity tag alone. Local profiles and enforcement semantics remain necessary.

W3C [SHACL](https://www.w3.org/TR/shacl/) validates RDF graphs against shapes and returns results with focus nodes, paths, severities, messages, and source constraints. Shapes can require governance metadata or contract structure. Conformance proves only that the supplied graph met the supplied shapes during that evaluation, not that claims are true or controls effective.

W3C [PROV-O](https://www.w3.org/TR/prov-o/) relates entities, activities, agents, derivations, attribution, association, delegation, generation, use, and invalidation. Embedded governance needs provenance connecting policy and product versions to transformations and outcomes. Provenance records claims and dependencies; it does not automatically assign accountability or prove correctness.

The Open Policy Agent [Policy Language](https://www.openpolicyagent.org/docs/policy-language) documentation describes declarative rules over structured data and APIs for policy evaluation. Its [decision-log documentation](https://www.openpolicyagent.org/docs/management-decision-logs) describes reporting policy decisions with configuration for masking, upload, and failure behavior. These are implementation capabilities; safe input schemas, bundle governance, enforcement, evidence, availability, and privacy remain architectural responsibilities.

Kubernetes [admission-controller documentation](https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/) distinguishes mutating and validating admission after authentication and authorization but before object persistence. Admission illustrates a platform control point, ordering concerns, failure policy, reinvocation, side effects, and matching. It does not govern data already stored, runtime reads, external systems, or human outcomes.

OpenLineage's [object model](https://openlineage.io/docs/spec/object-model/) defines job, run, dataset, and facet concepts for extensible lineage. Stable run and dataset identities can connect governance decisions to actual transformations. Producers must still capture exact semantics, versions, missing events, and policy context.

[CloudEvents](https://cloudevents.io/) provides a common event envelope and bindings intended to improve interoperability across services and platforms. A standard envelope can carry event identity, source, type, subject, time, and data-content information, while domain schemas and governance meaning remain separately versioned.

The Bitol [Open Data Contract Standard](https://bitol-io.github.io/open-data-contract-standard/latest/) defines an open, machine-readable structure for data-contract metadata, including product information, schemas, service levels, quality, roles, terms, and links. It is a community specification rather than universal authority. Its value is a portable contract envelope that organizations can profile, validate, and connect to enforcement.

Together these sources support risk-based governance, explicit organizational outcomes, controls, catalogs, quality evidence, usage policies, structural validation, provenance, policy decisions, platform admission, lineage events, event envelopes, and machine-readable contracts. A working governance architecture composes them around actual products and flows.

## Prerequisites and Retrieval

You should understand data products, domains, metadata, schemas, semantics, contracts, lineage, quality, privacy, security, identity, access, policy as code, event-driven systems, databases, pipelines, streaming, platform engineering, observability, incident response, retention, deletion, and recovery.

Retrieve data product, product owner, domain, consumer, contract, interface, schema, semantic version, service level, quality objective, purpose, classification, policy bundle, decision point, enforcement point, obligation, admission, validation, mutation, quarantine, exception, waiver, compensating control, expiry, provenance, receipt, continuous monitoring, control effectiveness, outcome, paved road, and closure.

As a retrieval test, inspect a pipeline badge that says `governance: passed`. Ask which product and version; which owner and consumers; which contract, schema, purpose, classifications, locations, policies, decisions, exceptions, retention, quality, lineage, and evidence were evaluated; which writes and reads were enforced; whether obligations executed; whether deployed behavior matches the evaluated artifact; what happens during policy outage; and which outcomes improved. The badge answers none of these questions.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish governance policy, metadata, decision, enforcement, evidence, assurance, and outcome;
2. define data products with accountable ownership, consumers, purposes, interfaces, contracts, service expectations, and lifecycle;
3. place control points across collection, write, transform, publish, read, join, share, export, retain, delete, restore, and retire transitions;
4. design decision and enforcement APIs with stable context, versions, obligations, failure semantics, and receipts;
5. embed classification, purpose, quality, residency, retention, provenance, identity, access, and deletion requirements into flows;
6. govern schemas and contracts through compatibility, negotiation, deployment, observation, deprecation, and consumer migration;
7. implement bounded exceptions, quarantine, correction, incident response, rollback, and recovery;
8. build shared platform capabilities and domain-owned profiles without central bottlenecks or uncontrolled divergence;
9. measure control coverage, effectiveness, operational friction, product value, incidents, remedy, and affected-party outcomes; and
10. identify where automation must defer to domain, legal, privacy, security, records, safety, consumer, and affected-person judgment.

## Core Exposition

**Begin with the product and decision.** Identify the data capability, accountable domain, consumers, purposes, decisions supported, affected people, value, harms, obligations, and end-of-life conditions. A table becomes a product only when someone owns its fitness and lifecycle for defined consumers.

**Define accountability as capacity.** An owner needs authority to accept or stop changes, resources to operate controls, access to domain expertise, a support path, and escalation. A name copied into a catalog without these properties is a routing hint, not accountable ownership.

**Separate organizational roles.** Distinguish product owner, data steward, source authority, custodian, platform operator, policy owner, privacy and security reviewers, records owner, consumer, and affected stakeholder. One person can hold several roles, but the responsibilities and conflicts remain visible.

**Model consumers explicitly.** Register human, service, pipeline, report, model, partner, regulator, and public consumers with principal, purpose, interface, contract version, data scope, location, service expectation, and lifecycle. Unknown consumers make safe compatibility and retirement impossible.

**Treat purpose as an executable dimension.** Carry purpose identity from request or workflow through policy evaluation, data access, transformation, output, retention, and evidence. Do not infer purpose solely from team, role, endpoint, or environment.

**Define the product boundary.** Include authoritative data versions, schemas, semantic definitions, APIs or distributions, policies, quality, provenance, service objectives, support, incidents, retention, deletion, and recovery. External dependencies and shared platform controls are part of the contract even when owned elsewhere.

**Use stable product identity.** Names, paths, topics, tables, and dashboards change or are reused. Give product and distribution versions durable identifiers and validity intervals. Preserve aliases and succession so consumers and audit evidence remain interpretable.

**Make contracts multi-dimensional.** Define physical schemas, business semantics, units, code sets, keys, nulls, event time, valid time, granularity, quality, availability, freshness, purpose, classification, access, residency, retention, lineage, change, evidence, and support. A serialization schema is only one part.

**Separate contract from observation.** The contract says what should be true. Measurements and receipts say what was observed. Preserve violations, uncertainty, samples, and missing measurements rather than rewriting the contract or declaring compliance from intent.

**Version contract meaning.** Syntactic compatibility can coexist with semantic breakage. Changing currency, population, aggregation, null meaning, event-time policy, code set, source authority, purpose, or retention needs an explicit semantic version and consumer analysis.

**Negotiate change with consumers.** Classify changes by each contract dimension, identify consumers and dependencies, provide proposed and effective versions, tests, shadow data, migration windows, rollback semantics, and retirement. Silence is not consent when a consumer cannot observe the proposal.

**Represent governance assertions.** Attach ownership, classification, purpose, basis, quality, location, retention, contract, and policy through attributable assertions with object version, scope, issuer, evidence, state, effective interval, and limitations. Multiple authorities and conflicts can coexist.

**Keep unknown state explicit.** `unknown`, `not assessed`, `inferred`, `proposed`, `verified`, `conflicting`, `exception`, `not applicable`, `expired`, and `revoked` are different. Defaulting missing metadata to public, global, indefinite, allowed, or high quality turns data gaps into policy decisions.

**Propagate context by rule.** Define how assertions transfer through copy, projection, filter, join, aggregation, masking, tokenization, model training, export, and deletion. Recompute output classes and purposes from transformation semantics and evidence; do not blindly copy or drop tags.

**Place controls on lifecycle edges.** Govern collection, ingest, validation, quarantine, write, change, transform, join, publish, discover, read, query, export, share, retain, hold, delete, restore, and retire. The highest-risk edge may be an internal notebook read or backup restore, not the public API.

**Identify decision points.** A decision point receives principal, delegation, action, resource and version, product, purpose, contract, data attributes, environment, jurisdiction, time, policy version, and relevant evidence. It returns decision identity, effect, obligations, explanation reference, validity, and uncertainty.

**Identify enforcement points.** Application, API gateway, database, query engine, pipeline orchestrator, stream processor, object store, export service, catalog, model gateway, and recovery workflow can enforce different actions. Map every decision to the component that can actually prevent or shape the effect.

**Separate decision from enforcement.** Record evaluation, delivery, application, target effect, obligation completion, and independent observation. A decision can be correct but ignored; an enforcement point can apply a stale decision; a successful command can produce a partial outcome.

**Choose local or centralized evaluation deliberately.** Central services simplify policy and evidence but add latency and outage concentration. Local sidecars or libraries improve availability but drift. Signed bundles and local evaluation can balance these concerns when distribution, revocation, and result collection are designed.

**Version policy bundles immutably.** Bind rule source, compiled form, data, schemas, dependencies, tests, approvals, signatures, build, release, effective interval, supersession, and rollback constraints. The decision records the exact evaluated digest, not only a policy name.

**Validate policy inputs.** Missing actor, purpose, resource version, classification, location, contract, or time should not be interpreted through language defaults. Validate schemas and semantic constraints before evaluation and return explicit indeterminate state when required facts are absent.

**Model obligations as work.** Masking, encryption, location routing, logging, notification, retention assignment, approval, watermarking, scanning, or deletion must have target, owner, deadline, idempotency, status, evidence, retry, and escalation. An allowed decision with an unexecuted obligation is not complete.

**Choose failure behavior by consequence.** Fail closed for unacceptable disclosure; quarantine ambiguous writes; use recently valid bounded decisions where safe; degrade nonessential analytics; preserve safety-critical operation with compensating evidence; or require human review. Never rely on one global `fail_open` switch.

**Design quarantine as a governed state.** Preserve immutable object identity, source, reason, classifications, access, owner, deadline, evidence, correction, release, and disposition. Quarantine must not become an unmonitored indefinite warehouse or a bypass for ordinary consumers.

**Embed classification early.** Classify at source design and collection, validate at ingest, recompute through transformations, and enforce at read, share, export, incident, retention, and deletion. Scanning a published warehouse is a useful detection layer, not the primary design mechanism.

**Embed data quality in decisions.** Link metrics and measurements to product versions, dimensions, methods, samples, windows, producers, thresholds, consumers, and consequences. Decide whether bad quality blocks, quarantines, warns, routes, or permits bounded use according to purpose and harm.

**Avoid quality as one score.** Accuracy, completeness, conformance, uniqueness, consistency, timeliness, lineage, representativeness, and fitness differ. A weighted score can hide a fatal failure. Preserve component measurements and consumer-specific acceptance.

**Embed privacy and purpose controls.** Minimize fields and rows, separate purposes, restrict linkability, mask or tokenize at suitable boundaries, account for rights and consent, control downstream recipients, and preserve deletion state. A `PII` tag cannot select all required behavior.

**Embed security controls.** Authenticate workload and user identity, authorize exact actions, encrypt and manage keys, isolate tenants, validate inputs, protect integrity, audit reads and administration, scan dependencies, respond to incidents, and recover current policy before data.

**Embed residency and sovereignty.** Resolve subject, controller, contract, purpose, system, operation, location, support access, keys, replicas, backups, transfers, and time. Enforce placement and access during scheduling, storage, processing, support, export, recovery, and provider change.

**Embed retention and holds.** Assign record class, authority, trigger, schedule, disposition, and evidence at creation. Overlay scoped holds before destructive actions. Propagate changes to copies and derivatives. A storage lifecycle setting is an enforcement mechanism, not the authoritative schedule.

**Embed deletion and non-resurrection.** Identify subject and object versions, target dependencies, retained exceptions, actions, recipients, backups, models, evidence, and tombstones. Imports, events, migrations, and restores check current deletion state before ordinary processing.

**Use provenance to connect decisions and effects.** Link product, contract, policy, input, transformation, agent, environment, output, quality, enforcement, and publication versions. Provenance supports impact analysis and reconstruction but remains an attributed assertion requiring validation.

**Emit governed lifecycle events.** Events include stable identity, source, type, subject, product and object version, effective and record time, schema, contract, purpose, policy, decision, trace, outcome, and protected evidence references. Standard envelopes do not replace domain semantics.

**Register data before broad consumption.** Publishing can require owner, contract, classification, purpose profile, quality evidence, lineage, service expectations, support, retention, location, access policy, incident path, and deprecation plan. Apply risk-based requirements rather than paperwork identical for every product.

**Govern discovery separately from access.** A consumer may learn that a product exists without viewing sensitive schema or samples. Catalog search, preview, request, approval, access, query, export, and renewal are separate actions with separate evidence.

**Make the governed path the easy path.** Platform templates can provision product identity, repositories, schemas, contract validation, lineage emission, policy evaluation, secrets, storage, observability, retention, quality, documentation, and support integration. Defaults remain reviewable and domain profiles remain explicit.

**Avoid platform capture.** Shared capabilities should offer stable interfaces and escape paths for justified needs. A central platform team cannot own every domain meaning or risk decision. Federate semantic and purpose authority while centralizing reusable technical controls and evidence.

**Design for legacy systems.** Use gateways, change capture, proxy enforcement, scheduled reconciliation, protected manifests, and bounded exceptions when native controls are absent. Record gaps honestly and fund retirement; do not label compensating detection as equivalent prevention.

**Govern notebooks and ad hoc tools.** Authenticate identities, register purpose and environment, limit source and output, control packages and network, apply time-bound workspaces, capture queries and lineage, scan exports, propagate deletion, and expire storage. Innovation environments are product consumers, not exemptions.

**Govern machine-learning flows.** Connect training purpose, data rights, feature provenance, labels, model and configuration, evaluation populations, decision use, explanation, monitoring, retraining, deletion, and retirement. Model approval does not authorize every deployment or downstream decision.

**Govern external sharing.** Bind recipient identity, contract, purpose, fields, token domain, location, allowed processing, onward transfer, retention, deletion, audit, incident, rights, evidence, and closure. Technical delivery and recipient compliance remain separate states.

**Make exceptions first-class.** An exception names rule, scope, object and version, consumer, purpose, risk, rationale, approver, compensating controls, evidence, start, expiry, review, revocation, and removal plan. Base policy remains unchanged and exception use is observable.

**Prevent exception permanence.** Require the shortest defensible validity, notify owners before expiry, fail to quarantine or deny where safe, and measure renewals and aging. Repeated exceptions can reveal a bad platform control or legitimate policy mismatch; investigate rather than automatically renew.

**Test policy and controls.** Use unit and property tests, schema tests, adversarial contexts, deny and indeterminate cases, bundle verification, integration tests at enforcement points, fault injection, performance tests, shadow decisions, canaries, and recovery exercises. A rule test cannot prove application enforcement.

**Observe deployed reality.** Compare catalog and contract assertions with storage, schemas, lineage, identities, queries, locations, retention, policies, exceptions, outputs, and backups. Drift detection needs an owner, severity, containment, correction, evidence, and deadline.

**Measure coverage with denominators.** Track expected products, producers, consumers, lifecycle edges, policy decisions, enforcement points, obligations, measurements, copies, and recovery paths. Unknown inventory cannot disappear from the denominator to make coverage green.

**Measure effectiveness and value.** Relate controls to prevented or detected harm, faster remedy, fewer unsafe releases, lower exposure, better decisions, reliable products, consumer adoption, reduced rework, incident severity, and affected-party experience. Separate these from configuration and activity counts.

**Measure friction honestly.** Track integration effort, decision latency, false blocks, overrides, exception time, developer workarounds, consumer wait, support load, and abandonment. Excess friction is both an operational problem and a signal that bypass risk is increasing.

**Audit governance itself.** Record contract, policy, assertion, ownership, exception, approval, decision, enforcement, measurement, correction, and retirement changes. Restrict access to sensitive governance metadata and review privileged administrators.

**Support explanation and challenge.** Return safe reason identifiers, applicable product and policy versions, obligations, missing facts, owner, remedy, and appeal path. Preserve challenges and corrections without exposing protected rule logic or other subjects' data.

**Respond to incidents across the graph.** A wrong classification, policy defect, compromised bundle, stale exception, missing lineage, quality failure, residency breach, overretention, or deleted-data resurrection affects products, consumers, outputs, models, and decisions. Traverse provenance, contain, correct, notify, remedy, and verify.

**Make rollback governance-aware.** Rolling back code, schema, policy, contract, or data can create incompatible meaning or revive revoked access. Define which versions may coexist and which safety, purpose, deletion, or retention changes are irreversible.

**Migrate through governed compatibility.** Inventory products, consumers, contracts, policies, decisions, assertions, exceptions, lineage, copies, evidence, and restore paths. Dual-evaluate and observe, migrate cohorts, reconcile outcomes, preserve historical interpretation, and retire obsolete paths explicitly.

**Recover governance before flows.** Restore trusted identities, product and contract registries, current policy bundles, exception expiry, keys, schedules, holds, deletion tombstones, lineage, evidence, and incident blocks. Quarantine data until its current governance state is resolvable.

**Close products deliberately.** Announce deprecation, stop new consumers, migrate or end existing use, revoke access, stop flows, reconcile outputs and recipients, apply retention and deletion, retire policy and exceptions, preserve required evidence, and test that restore cannot republish the product.

## Definitions and Notation

Let embedded governance be:

`G = (P, O, C, M, E, F, A, R, V, L)`.

Represent a data product version as:

`p = (id, domain, owner, consumers, purposes, interfaces, contract, service, policy, lifecycle)`.

Represent a lifecycle transition as:

`f = (input_version, activity, agent, purpose, contract, policy_decision, enforcement, output_version, effective_time, record_time, evidence)`.

Represent an exception as:

`x = (rule, scope, purpose, risk, rationale, approver, compensation, evidence, start, expiry, review, revocation)`.

For a requested action `a`, a bounded decision function is:

`decision = PDP(principal, delegation, action, resource_version, product, purpose, contract, assertions, environment, time, policy_version)`.

An enforcement receipt should link that decision to the observed target effect and each obligation. It should not treat the decision response itself as execution.

Define decision coverage as:

`C_d = governed_decisions / expected_governable_actions`.

Define enforcement coverage as:

`C_e = observed_enforcements / decisions_requiring_enforcement`.

Define obligation completion as:

`C_o = verified_obligations / required_obligations`.

Define exception exposure as:

`X_t = Σ(scope_weight(x) × active_duration(x))`.

The weight is an explicit local risk model, not a universal scalar. Each measure requires product, edge, consumer, purpose, interval, source, exclusions, uncertainty, and owner.

## Mechanisms, Invariants, or Proof Structure

Use these assurance gates.

**Product gate.** Establish stable product identity, domain, accountable owner, consumers, purpose, value, harms, interfaces, support, and lifecycle.

**Contract gate.** Version schema, semantics, keys, time, quality, service, policy, location, retention, provenance, change, evidence, and compatibility.

**Assertion gate.** Resolve ownership, classification, purpose, basis, quality, location, retention, and other claims with authority, evidence, state, and time.

**Flow gate.** Identify every collection, write, transformation, join, publication, read, share, export, retention, deletion, restore, and retirement edge.

**Decision gate.** Validate context and evaluate the exact immutable policy bundle, returning decision identity, effect, obligations, reason, validity, and uncertainty.

**Enforcement gate.** Apply the current decision at the component capable of controlling the effect and record observed target and obligation outcomes.

**Failure gate.** Select deny, quarantine, bounded cached decision, degradation, safety override, or human review for policy, context, network, and evidence failures.

**Exception gate.** Require scoped risk, rationale, compensation, evidence, owner, approval, expiry, review, revocation, and removal.

**Evidence gate.** Link product, contract, assertions, policy, decision, enforcement, obligations, measurements, exceptions, incidents, and outcomes through provenance.

**Assurance gate.** Test rules, inputs, bundles, enforcement integrations, adversarial contexts, faults, drift, recovery, and historical interpretation.

**Value gate.** Measure coverage, effectiveness, risk, friction, consumer value, harm, remedy, and affected-party outcomes with denominators.

**Correction gate.** Contain policy or product defects, traverse affected lineage, revoke unsafe state, correct outputs and decisions, notify, remedy, and verify.

**Migration gate.** Dual-evaluate, observe, reconcile, migrate consumers and flows, preserve history, constrain rollback, and retire bypasses.

**Recovery gate.** Restore current identity, contracts, policy, exceptions, schedules, holds, deletion, evidence, and incident state before data processing.

**Closure gate.** End consumers and flows, revoke access, settle outputs and recipients, apply disposition, preserve evidence, and prevent restoration.

### Executable evidence: governed-flow transition evaluation

This program classifies ten invented lifecycle transitions using seven declared governance checks.

<!-- bijux-verify: {"id":"governed-flow-transition-evaluation","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"transitions=10\nallowed=3\nmissing_owner=1\nmissing_classification=1\nincompatible_schema=1\nunauthorized_purpose=1\nresidency_violation=1\nretention_unknown=1\nunregistered_consumer=1\nproducts=6\nstages=8\npolicy_versions=3\ndecision_events=10\n","stderr":""}} -->
```python
transitions = [
    {"product": "orders", "stage": "ingest", "policy": "p3", "owner": True, "classified": True, "schema": True, "purpose": True, "residency": True, "retention": True, "consumer": True},
    {"product": "orders", "stage": "transform", "policy": "p3", "owner": True, "classified": True, "schema": True, "purpose": True, "residency": True, "retention": True, "consumer": True},
    {"product": "campaigns", "stage": "publish", "policy": "p2", "owner": True, "classified": True, "schema": True, "purpose": True, "residency": True, "retention": True, "consumer": True},
    {"product": "profiles", "stage": "ingest", "policy": "p3", "owner": False, "classified": True, "schema": True, "purpose": True, "residency": True, "retention": True, "consumer": True},
    {"product": "telemetry", "stage": "write", "policy": "p1", "owner": True, "classified": False, "schema": True, "purpose": True, "residency": True, "retention": True, "consumer": True},
    {"product": "orders", "stage": "publish", "policy": "p3", "owner": True, "classified": True, "schema": False, "purpose": True, "residency": True, "retention": True, "consumer": True},
    {"product": "profiles", "stage": "read", "policy": "p3", "owner": True, "classified": True, "schema": True, "purpose": False, "residency": True, "retention": True, "consumer": True},
    {"product": "claims", "stage": "replicate", "policy": "p2", "owner": True, "classified": True, "schema": True, "purpose": True, "residency": False, "retention": True, "consumer": True},
    {"product": "telemetry", "stage": "retain", "policy": "p1", "owner": True, "classified": True, "schema": True, "purpose": True, "residency": True, "retention": False, "consumer": True},
    {"product": "research", "stage": "export", "policy": "p2", "owner": True, "classified": True, "schema": True, "purpose": True, "residency": True, "retention": True, "consumer": False},
]

def evaluate(transition):
    if not transition["owner"]:
        return "missing_owner"
    if not transition["classified"]:
        return "missing_classification"
    if not transition["schema"]:
        return "incompatible_schema"
    if not transition["purpose"]:
        return "unauthorized_purpose"
    if not transition["residency"]:
        return "residency_violation"
    if not transition["retention"]:
        return "retention_unknown"
    if not transition["consumer"]:
        return "unregistered_consumer"
    return "allowed"

results = [evaluate(transition) for transition in transitions]
print(f"transitions={len(transitions)}")
for outcome in ["allowed", "missing_owner", "missing_classification", "incompatible_schema", "unauthorized_purpose", "residency_violation", "retention_unknown", "unregistered_consumer"]:
    print(f"{outcome}={results.count(outcome)}")
print(f"products={len({transition['product'] for transition in transitions})}")
print(f"stages={len({transition['stage'] for transition in transitions})}")
print(f"policy_versions={len({transition['policy'] for transition in transitions})}")
print(f"decision_events={len(results)}")
```

The output reports ten transitions, three allowed outcomes, one of each declared failure, six products, eight lifecycle stages, three policy versions, and ten decisions.

The evidence is deliberately narrow. Invented Booleans do not establish real ownership, classification, schema compatibility, purpose, residency, retention, consumer registration, policy meaning, enforcement, or outcome. Evaluation order hides multiple failures, and the code performs no data operation or obligation. Production assurance requires authoritative assertions, immutable product and contract versions, validated context, real decision and enforcement integrations, independent observations, exception governance, affected-party review, incident correction, and recovery exercises.

## Alternatives and Trade-Offs

**Central governance approval.** Decisions can be consistent. Domain context, latency, queues, and bottlenecks grow.

**Federated domain authority.** Meaning and accountability stay close to work. Shared controls and cross-domain consistency need strong coordination.

**Prose policies.** Human nuance is expressible. Enforcement and drift are hard to observe.

**Policy as code.** Decisions are testable and distributable. Inputs, semantics, bundle supply chain, and human judgment remain.

**Central decision service.** Rule rollout and evidence are unified. Latency and outage become systemic.

**Local policy evaluation.** Availability and performance improve. Bundle drift and revocation become harder.

**Fail closed.** Unsafe effects are prevented. Availability and safety-critical work can suffer.

**Fail open.** Service continues. Disclosure and policy bypass can become silent.

**Quarantine.** Ambiguous data is contained. Backlogs, sensitive storage, and indefinite limbo need control.

**Mutating enforcement.** Systems can add defaults or masks. Hidden changes can alter meaning and surprise owners.

**Validating enforcement.** Intent remains explicit. Consumers must repair rejected work.

**Rich contracts.** Meaning and expectations are visible. Authoring and evolution require real ownership.

**Minimal schemas.** Adoption is easy. Semantic, policy, quality, and lifecycle gaps persist.

**Strict compatibility.** Consumers are protected. Valuable changes slow and legacy semantics linger.

**Negotiated compatibility.** Context-specific evolution improves. Consumer inventory and coordination are required.

**Preventive controls.** Harm can be stopped early. False blocks and integration complexity rise.

**Detective controls.** Legacy adoption is easier. Harm may occur before correction.

**Shared platform templates.** Paved paths reduce repeated engineering. Defaults can become rigid or falsely universal.

**Product-specific controls.** Domain fit improves. Duplication and inconsistent assurance grow.

**Permanent product ownership.** Stable support is possible. Organization and domain boundaries change.

**Lifecycle ownership transfer.** Authority can follow reality. Provenance, consumer trust, and historical interpretation must transfer.

**Broad observability.** Gaps and drift are visible. Governance metadata can enable surveillance or disclosure.

**Minimal evidence.** Privacy and cost improve. Reconstruction and independent assurance can weaken.

## Failure Modes and Misconceptions

1. **“A catalog means governance is embedded.”** Discovery metadata does not enforce lifecycle decisions.
2. **“Every table is a data product.”** Products require consumers, ownership, interfaces, expectations, and lifecycle.
3. **“An owner field creates accountability.”** Authority, capacity, duty, and escalation must be real.
4. **“The steward owns every decision.”** Domain, legal, security, privacy, records, and platform authorities differ.
5. **“A schema is a complete contract.”** Semantics, quality, purpose, policy, service, and change remain.
6. **“Backward-compatible syntax preserves meaning.”** Units, population, nulls, and time can change silently.
7. **“No consumer complaint means compatibility.”** Consumers can be unknown, broken, or unable to detect drift.
8. **“Metadata tags are facts.”** They are assertions with source, state, evidence, and time.
9. **“Missing classification means public.”** Absence is uncertainty, not authorization.
10. **“The highest label always propagates.”** Output meaning depends on transformation and context.
11. **“Encryption lowers classification.”** It changes exposure controls, not underlying meaning automatically.
12. **“A purpose can be inferred from role.”** The same role can act for many purposes.
13. **“Access control is all governance.”** Quality, meaning, retention, rights, location, and outcomes remain.
14. **“Publication is the only control point.”** Reads, writes, joins, exports, deletes, and restores matter.
15. **“Internal pipelines are trusted.”** Workloads, dependencies, credentials, and configuration can fail.
16. **“A policy decision proves enforcement.”** The target action may ignore or misapply it.
17. **“Successful enforcement proves outcome.”** Downstream effects and obligations can remain incomplete.
18. **“One decision service fits every edge.”** Latency, availability, context, and consequence differ.
19. **“Fail closed is always safest.”** It can create safety or availability harm.
20. **“Fail open is an availability feature.”** It is a risk decision requiring bounds and evidence.
21. **“Cached decisions remain valid.”** Identity, policy, purpose, object, and revocation can change.
22. **“Policy names identify evaluated rules.”** Immutable bundle versions and inputs are required.
23. **“Rule tests prove integration.”** Enforcement wiring and target effects need independent tests.
24. **“Obligations are documentation.”** They require owned execution, evidence, retry, and escalation.
25. **“Mask on read satisfies minimization.”** Collection, storage, processing, and export may remain excessive.
26. **“A PII tag selects privacy controls.”** Purpose, subject, basis, sensitivity, location, and rights matter.
27. **“A region tag proves residency.”** Processing, support, keys, replicas, backups, and recovery can cross borders.
28. **“A TTL implements retention governance.”** Authority, trigger, holds, action, and evidence remain.
29. **“Deletion is a pipeline cleanup.”** Rights, exceptions, recipients, backups, and non-resurrection remain.
30. **“Quality is one score.”** Aggregation can conceal a fatal dimension.
31. **“Passed quality means fit for every use.”** Fitness depends on consumer and decision.
32. **“Lineage automatically assigns accountability.”** A dependency graph does not determine authority or duty.
33. **“A standard event envelope supplies semantics.”** Domain meaning and versions remain separate.
34. **“Admission controls govern runtime data.”** Later reads, processes, and external systems can bypass them.
35. **“The platform team owns domain meaning.”** Shared infrastructure cannot decide every semantic question.
36. **“Domains should build every control.”** Repetition causes divergence and weak shared assurance.
37. **“Legacy systems cannot be governed.”** Gateways and reconciliation can provide bounded controls and evidence.
38. **“Notebooks are exempt experimentation.”** They are consequential consumers and exporters.
39. **“Model approval governs all deployments.”** Purpose, population, data, version, and decision context change.
40. **“A sharing contract proves recipient behavior.”** Technical state and downstream evidence remain separate.
41. **“Exceptions should edit the policy.”** This hides deviations and weakens historical interpretation.
42. **“An approved exception can be permanent.”** Scope, risk, evidence, and context change.
43. **“A high pass rate proves effectiveness.”** Easy or missing decisions can dominate the denominator.
44. **“More metadata means more control.”** Unused or false assertions can increase confusion.
45. **“Developer friction is unrelated to risk.”** Excess burden encourages bypass and shadow flows.
46. **“Governance administrators need no oversight.”** Their changes affect every product and decision.
47. **“Rollback always restores safety.”** It can revive revoked permissions or deleted data.
48. **“Migration can drop old semantics.”** Historical evidence and consumers depend on them.
49. **“Recovery begins with restoring data.”** Current policy, identities, holds, and tombstones come first.
50. **“A retired product is just hidden in the catalog.”** Consumers, flows, access, copies, policy, and recovery remain.

## Worked Examples

### Example 1

An orders product publishes stable identity, owner, consumers, monetary semantics, event-time rules, schema, quality, availability, classification, purposes, locations, retention, lineage, support, and change windows. Consumer tests run against a proposed version before publication.

### Example 2

An ingest gateway validates source, product, contract, schema, classification, purpose, region, retention, and producer identity. Valid records enter a versioned stream; ambiguous records enter governed quarantine with owner and deadline; rejected events retain bounded evidence.

### Example 3

A query engine sends principal, delegation, action, dataset version, product, purpose, fields, location, policy digest, and time to a decision point. It applies row and column obligations, records actual query and export effects, and prevents cache reuse under different context.

### Example 4

A schema change is syntactically additive but changes `revenue` from gross to net. Semantic compatibility analysis marks it breaking, identifies reports and models through lineage, publishes a new contract version, dual-runs outputs, migrates consumers, and retires the old meaning.

### Example 5

A quality rule finds stale clinical codes. The product is still available for historical reconciliation but blocked for current care decisions, with consumer-specific acceptance, owner escalation, affected decisions, correction evidence, and deadline.

### Example 6

A residency policy routes an EU subject's data and keys to approved resources, restricts remote support, validates processors and backups, and records placement and access. Recovery chooses current authorized locations rather than restoring the original topology blindly.

### Example 7

A legal hold prevents deletion of selected messages while ordinary access is removed. The exception records exact matter scope and protected authority; product analytics cannot use preserved copies. Release later recomputes the retention schedule rather than deleting immediately.

### Example 8

A notebook environment receives time-bound consumer identity, declared purpose, approved product versions, masked fields, network limits, lineage capture, query audit, export scanning, and automatic expiry. Local artifacts follow source deletion and retention.

### Example 9

A legacy mainframe cannot call policy APIs. A gateway limits exports, scheduled reconciliation compares source manifests with registered consumers and purposes, and a bounded exception records gaps. Native modernization and retirement remain funded deliverables.

### Example 10

A product closes after consumers migrate, jobs stop, access and policy revoke, exceptions end, recipients reconcile, retention and deletion execute, evidence transfers, and restore testing proves that old data and permissions cannot republish it.

## Cross-Program Connections

**Software Engineering Patterns.** Contracts, adapters, anti-corruption layers, policy patterns, versioning, and domain boundaries shape maintainable embedded governance.

**Data Engineering.** Pipelines, streams, schemas, quality, lineage, orchestration, retries, backfills, publication, and deletion are primary enforcement surfaces.

**API and Service Engineering.** Product, policy, contract, decision, obligation, exception, evidence, and lifecycle APIs need stable semantics and safe errors.

**Platform Engineering.** Templates, identity, policy distribution, admission, secrets, observability, storage, recovery, and developer experience create governed paved paths.

**Security Engineering.** Authentication, authorization, integrity, confidentiality, key management, threat models, incidents, and privileged access protect control systems.

**Privacy Engineering.** Purpose, minimization, classification, consent, rights, residency, sharing, retention, deletion, affected people, and remedy shape decisions.

**Machine Learning Engineering.** Feature, training, model, evaluation, deployment, inference, decision, monitoring, and retirement flows need governed provenance.

**Product Management.** Consumers, value, service expectations, adoption, support, trade-offs, deprecation, outcomes, and accountability distinguish products from assets.

**Software Testing and Verification.** Contract, policy, property, integration, adversarial, drift, fault, canary, and recovery tests establish bounded evidence.

**Systems Engineering.** Organizations, people, incentives, dependencies, controls, failure behavior, migration, and emergent outcomes must align end to end.

## References

1. NIST, [Privacy Framework](https://www.nist.gov/privacy-framework), privacy-risk outcomes and profiles across systems, products, and services.
2. NIST, [Cybersecurity Framework 2.0](https://www.nist.gov/cyberframework), Govern, Identify, Protect, Detect, Respond, and Recover outcomes.
3. NIST, [SP 800-53 Release 5.2.0](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final), security and privacy control catalog.
4. W3C, [DCAT 3](https://www.w3.org/TR/vocab-dcat-3/), catalogs, datasets, services, distributions, versions, and relationships.
5. W3C, [Data Quality Vocabulary](https://www.w3.org/TR/vocab-dqv/), dimensions, metrics, measurements, policies, and provenance.
6. W3C, [ODRL Information Model 2.2](https://www.w3.org/TR/odrl-model/), permissions, prohibitions, duties, parties, assets, actions, and constraints.
7. W3C, [SHACL](https://www.w3.org/TR/shacl/), graph validation, shapes, results, paths, constraints, and severities.
8. W3C, [PROV-O](https://www.w3.org/TR/prov-o/), entities, activities, agents, derivation, attribution, association, and delegation.
9. Open Policy Agent, [Policy Language](https://www.openpolicyagent.org/docs/policy-language) and [Decision Logs](https://www.openpolicyagent.org/docs/management-decision-logs), declarative evaluation and decision evidence.
10. Kubernetes, [Admission Controllers](https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/), mutating and validating control points and failure policy.
11. OpenLineage, [Object Model](https://openlineage.io/docs/spec/object-model/), jobs, runs, datasets, and extensible facets.
12. Cloud Native Computing Foundation, [CloudEvents](https://cloudevents.io/), interoperable event envelopes and bindings.
13. Bitol, [Open Data Contract Standard](https://bitol-io.github.io/open-data-contract-standard/latest/), machine-readable product, schema, quality, service, role, and term metadata.

## Exercises

### Exercise 1

Define a governed customer-orders data product. Specify owner, consumers, purposes, contract, schemas, semantics, quality, service, classifications, policy, locations, retention, lineage, evidence, change, support, and closure.

### Exercise 2

Map control points for an event from mobile collection through ingest, stream processing, warehouse, feature generation, model inference, dashboard export, retention, deletion, and recovery. Define context, decisions, enforcement, obligations, and failure behavior.

### Exercise 3

Design a policy decision and enforcement architecture supporting central policy ownership, local evaluation, immutable bundles, typed indeterminate state, obligations, exceptions, decision receipts, revocation, outage behavior, and recovery.

### Exercise 4

Design continuous governance assurance for 500 products and 4,000 consumers. Include inventory, assertions, drift, quality, contracts, decisions, enforcement, exceptions, incidents, friction, value, remedy, and denominators.

### Exercise 5

Migrate catalog-only governance and manual approvals into embedded product and flow controls across modern cloud pipelines, notebooks, partner exports, and two legacy systems. Include rollout, comparison, rollback, recovery, and retirement.

## Answers to the Exercises

### Answer 1

Give the orders product a durable identity and accountable commerce-domain owner with authority, operations capacity, support, escalation, and succession. Register checkout, fulfillment, finance, customer support, analytics, and fraud consumers with exact purposes, principal types, interfaces, fields, regions, and service expectations. Define order, line, payment-reference, status, refund, and event identities; units and currencies; code sets; nulls; event and valid time; granularity; ordering; and correction.

The contract versions schema and semantics alongside completeness, uniqueness, reconciliation, freshness, availability, classification, approved purposes, access, token domains, residency, retention, holds, deletion, provenance, evidence, incidents, deprecation, and change. Measurements are separate versioned observations. Proposed changes identify lineage and consumers, run compatibility tests, dual-publish when needed, and require explicit migration. Closure stops new consumers, migrates dependencies, revokes access, settles recipients, applies schedules and erasure, preserves minimum evidence, and prevents restore from republishing.

### Answer 2

At collection, validate app and subject context, consent or purpose, minimization, classification, and region. At ingest, authenticate producer, validate contract and schema, assign immutable identity, retention, and provenance, and quarantine ambiguity. At streaming, authorize joins and transformations, propagate or recompute assertions, enforce location and quality, and record input offsets and output versions. Warehouse publication requires owner, contract, lineage, quality evidence, policy, registered consumers, and support.

Feature generation binds approved purpose, source and feature versions, subject edges, deletion, and training restrictions. Inference checks model, population, purpose, decision authority, explanation, and monitoring. Dashboard queries enforce rows, columns, small-group and export rules; exports bind recipient and lifecycle. Retention evaluates schedules and holds; deletion executes target plans and tombstones; recovery restores current identity, contract, policy, exceptions, keys, holds, and deletion before data. Every point records decision separately from observed enforcement and obligations, with consequence-specific deny, quarantine, degradation, or review behavior.

### Answer 3

Store policy source, data, schemas, tests, dependencies, approvals, signatures, build evidence, effective interval, and rollback constraints in immutable bundles. Distribute verified bundles to local evaluators beside APIs, query engines, pipelines, object access, and recovery workflows. Inputs use stable principal, delegation, action, resource and version, product, purpose, contract, assertions, environment, jurisdiction, and time schemas. Missing required facts return typed indeterminate, never a default allow.

Decisions return stable ID, bundle digest, effect, obligations, reasons, validity, and uncertainty. Enforcement points record delivery, application, target effect, obligation completion, and independent observation. Exceptions overlay rather than edit policy and carry exact scope, risk, compensation, evidence, approval, expiry, and revocation. Urgent bundle revocation overrides caches. Outage policies differ by action: deny sensitive export, quarantine writes with unknown class, use bounded recent decisions for low-risk reads, or preserve safety service with escalation. Recovery restores trusted bundles, revocations, exceptions, identities, evidence, and tombstones before evaluation.

### Answer 4

Create denominators for expected products, owners, consumers, contracts, lifecycle edges, assertion types, decisions, enforcement points, obligations, measurements, copies, and recovery paths. Reconcile catalog claims with schemas, storage, identity, query logs, lineage, locations, schedules, backups, and deployed bundles. Measure assertion authority, age, conflict and unknown state; contract compatibility and consumer migration; quality by dimension and decision; decision latency and coverage; enforcement and obligation receipts; and exception scope-duration, renewal, expiry, and removal.

Separate activity from effectiveness. Track unsafe releases prevented or detected, exposure duration, product incidents, overretention, resurrection, wrong decisions, remedy time, recurrence, consumer reliability, decision usefulness, affected-party reports, and residual uncertainty. Measure friction through integration effort, false blocks, overrides, wait time, workarounds, support, and abandonment. Sample and independently test high-risk controls, inject policy and network faults, exercise recovery, audit governance administrators, and assign every gap a severity, owner, containment, deadline, and verification.

### Answer 5

Inventory assets, true products, owners, consumers, purposes, flows, manual approvals, schemas, meanings, classifications, locations, schedules, policies, exceptions, notebooks, exports, legacy interfaces, evidence, incidents, and recovery. Preserve catalog assertions as attributed legacy claims rather than treating them as verified. Define product identities, multidimensional contracts, lifecycle events, decision context, policy bundles, enforcement receipts, exception objects, and control-point profiles.

Start with shadow validation and decisions on representative cloud flows, compare with human outcomes, correct semantics, then enforce low-risk contracts and high-consequence disclosure edges with canaries and rollback. Provision notebook and partner paths through governed templates. Place gateways and reconciliation around legacy systems, recording prevention gaps as expiring exceptions with retirement owners. Migrate consumers in cohorts, compare outputs and obligations, traverse lineage for incidents, and test restore with current policy and deletion. Retire forms and approvals only when equivalent authority, challenge, and evidence exist; revoke bypasses and verify old paths cannot resume through rollback or recovery.
