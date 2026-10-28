---
module_id: DARCH-084
program: Data Architecture Engineering
level: 2
module_number: 84
title: Federated Computational Governance
status: complete
last_verified: 2026-09-03
---

# Federated Computational Governance

## One-Page Review

### Governing question

How should independent data domains and enterprise authorities turn shared and local governance decisions into versioned, testable, distributed, enforceable, observable, challengeable, and recoverable computation without centralizing every decision or allowing local autonomy to weaken nondelegable obligations?

### Essential definitions

- **Federated computational governance** is an operating system in which bounded authorities create compatible policies and controls whose decisions and enforcement are automated across a changing data-product topology with attributable evidence and human remedy.
- A **governance constitution** defines nondelegable obligations, reserved and delegated powers, policy precedence, evidence, conflict resolution, amendment, emergency authority, and exit.
- A **global invariant** is a minimum cross-domain requirement needed for rights, security, privacy, safety, records, identity, interoperability, or enterprise operation.
- A **domain policy** specializes governance for local meaning, products, risks, and consumers without silently weakening applicable global invariants.
- **Computational policy** is a versioned decision specification with typed inputs, explicit outcomes, obligations, tests, authority, effective time, and execution semantics.
- A **policy administration point** governs source, interpretation, review, compilation, packaging, approval, distribution, versioning, and retirement.
- A **policy decision point** evaluates trusted inputs against an identified policy set and returns a structured decision.
- A **policy enforcement point** controls the real operation, supplies trusted context, applies the decision and obligations, prevents bypass, and reports effects.
- A **policy information point** supplies governed facts such as identity, classification, purpose, consent, location, risk, relationship, and valid time.
- A **policy bundle** is an immutable, attributable package of policies, schemas, reference data, manifests, dependencies, provenance, signatures, and compatibility metadata.
- **Policy composition** selects applicable global, jurisdictional, domain, product, and consumer rules and resolves their results under an explicit combining contract.
- **Fleet convergence** describes which eligible decision and enforcement points run which compatible policy and data revisions at a stated time.
- A **decision receipt** links the request, input digest, authorities, policy and data revisions, result, reasons, obligations, enforcement outcome, and relevant times.
- An **exception** is an authorized, scoped, time-bounded deviation with risk, compensation, monitoring, review, remedy, and automatic expiry.
- **Effectiveness** asks whether governance changes real behavior and risk; compilation, deployment, conformance, or receipt counts alone do not establish it.
- **Closure** prevents retired authority, rules, bundles, exceptions, caches, or recovery procedures from making new decisions while preserving required history.

### Central model, mechanism, or theorem

Represent federated computational governance as:

`G = (C, A, P, D, E, R, O, X, M, L)`

where `C` is constitution and global invariants, `A` authorities and delegations, `P` policy models and composition, `D` distribution and convergence, `E` decision and enforcement, `R` receipts and assurance evidence, `O` operations and resilience, `X` exceptions, conflicts, challenge, and remedy, `M` measurement and effectiveness, and `L` lifecycle, recovery, and closure. Governance is computational only when an authorized policy revision influences a real operation through a known enforcement point and produces bounded evidence. Governance is federated only when local authority is real, global constraints are explicit, and conflicts have legitimate resolution.

### Critical invariants

- Requirement, interpretation, authority, delegation, rule, policy set, bundle, decision, enforcement, evidence, exception, incident, and remedy have separate stable identities.
- Every executable rule traces to an authorized interpretation and scope; code ownership is not policy authority.
- Domains may strengthen applicable baselines but cannot silently waive nondelegable global obligations.
- Policy composition defines applicability, precedence, conflict, `not_applicable`, indeterminate input, and obligation merging; file or network order decides none of them.
- Decision points and enforcement points are distinct, and every consequential permit or deny can be connected to the protected operation.
- Trusted inputs carry issuer, definition, scope, valid time, observation time, freshness, and sensitivity.
- Bundle activation is attributable and compatible; fleet convergence uses a known eligible denominator and exposes stale, unreachable, and unknown nodes.
- Exceptions and emergency rules are explicit, expiring, monitored, challengeable, and unable to become invisible permanent bypasses.
- Evidence is minimized and protected while retaining enough identity, version, reason, obligation, and effect to investigate and correct decisions.
- Metrics distinguish policy activity, deployment, conformance, enforcement, legitimate friction, harmful effects, control effectiveness, cost, and remedy.
- Recovery restores constitution, authority, identity, trusted facts, current policy, exceptions, holds, and tombstones before resuming automated data operations.
- Closure prevents obsolete policy from returning through caches, offline agents, old images, credentials, backups, or disaster-recovery automation.

### Common failures

Common failures include calling a central approval queue federated; calling a repository computational governance; converting legal prose directly into Booleans; treating policy authors as authorities; allowing local rules to override global obligations; choosing precedence from load order; reducing every decision to allow or deny; trusting caller-supplied classification or purpose; deploying policy without enforcement coverage; recording decisions without effects; counting bundles instead of protected operations; exposing sensitive input in logs; letting exceptions live forever; forcing fail-open behavior on every outage; measuring denial rate as effectiveness; and restoring stale bundles before current identity, revocation, deletion, and hold state.

### Compact example

Ten invented policy changes are evaluated against six declared federation requirements. Four qualify; one each lacks authority, conflicts with a global invariant, targets a stale bundle, lacks an enforcement point, lacks a receipt, or depends on an expired exception. Nine named authorities, four global rules, fourteen domain rules, three policy revisions, five enforcement points, nine declared receipts, one exception, and ten decisions are counted. Executable evidence confirms only those declarations and counts. It proves no lawful authority, semantic correctness, enforcement, federation legitimacy, control effectiveness, fairness, or beneficial outcome.

### Connections

[DARCH-071](071-federated-data-governance.md), [DARCH-072](072-policy-as-code-for-data.md), [DARCH-079](079-audit-and-provenance-architecture.md), [DARCH-080](080-embedding-governance-into-data-flows-and-products.md), [DARCH-081](081-data-mesh-principles.md), [DARCH-082](082-domain-oriented-decentralization.md), and [DARCH-083](083-self-serve-data-platform-capabilities.md) establish federation, executable policy, evidence, embedded controls, mesh principles, domain authority, and platform mechanisms. [DARCH-085](../ROADMAP.md) next examines data-fabric concepts.

## Governing Question

An enterprise council can approve a policy stating that restricted customer data must remain in an allowed region and be used only for an authorized purpose. That approval does not govern an export unless systems can identify the data and purpose, compose applicable global and domain rules, make a decision, enforce it at every export path, record the effect, and correct harmful mistakes.

The governing question joins legitimacy and machinery. Purely centralized decisions ignore domain context and become queues. Purely local rules create incompatible controls and externalities. Pure automation can execute an illegitimate or mistranslated rule at enormous scale. A durable architecture therefore connects human authority, machine-readable policy, distributed enforcement, operational evidence, challenge, and learning.

## Why This Matters

Zhamak Dehghani's [Data Mesh Principles and Logical Architecture](https://martinfowler.com/articles/data-mesh-principles.html) identifies federated computational governance as one of four interdependent data-mesh principles. It combines domain autonomy, global interoperability, a changing topology, and automated execution through the platform. This is an organizational and technical design problem, not the purchase of a policy engine.

The Open Policy Agent [Policy Language](https://www.openpolicyagent.org/docs/policy-language) describes Rego as a declarative language for decisions over structured data. OPA separates decision making from enforcement. A federation can use that separation across different enforcement points, but must still govern authority, typed inputs, result contracts, composition, obligations, and actual protected operations.

OPA [Bundles](https://www.openpolicyagent.org/docs/management-bundles) package policy and data for distribution, support namespace roots and signatures, and report activation failures. The documentation warns about overlapping roots and ordering across multiple sources. Those mechanics illustrate why a federation needs explicit namespace ownership, composition, compatible activation, health, and rollback.

OPA [Decision Logs](https://www.openpolicyagent.org/docs/management-decision-logs) can carry decision identity, queried path, input, result, bundle revision, trace context, and masking metadata. Decision logs support audit and debugging but can contain sensitive inputs, can be dropped under limits, and do not prove that a caller enforced a result. A governance receipt must join a decision to its effect.

OPA's [deployment guidance](https://www.openpolicyagent.org/docs/deploy) distinguishes policy decision points from application enforcement points and discusses placement near callers for latency and reliability. Central, sidecar, embedded, and host-local decisions have different consistency, failure, trust, and operational trade-offs. Topology should follow consequence and dependency, not fashion.

Kubernetes [admission control](https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/) intercepts authenticated and authorized mutation requests before persistence, supports mutating and validating phases, and requires reconciliation for side effects. Admission is a useful enforcement boundary for infrastructure intent. It does not see every read, query, export, derived dataset, restored backup, or provider-side operation.

The CNCF [Platforms White Paper](https://tag-app-delivery.cncf.io/whitepapers/platforms/) frames platforms as curated capabilities serving user needs through self-service. Computational governance belongs in capability contracts and paved paths so domains receive safe defaults and useful explanations. A platform cannot legitimately invent enterprise risk policy merely because it hosts the enforcement mechanism.

The W3C [ODRL Information Model 2.2](https://www.w3.org/TR/odrl-model/) represents permissions, prohibitions, duties, parties, assets, actions, constraints, and policy relationships. It can help exchange usage-policy intent across domains. Its representation does not supply legal interpretation, combining semantics for every environment, or enforcement.

W3C [SHACL](https://www.w3.org/TR/shacl/) represents shapes for validating RDF graphs and structured validation results. Federations can validate that products, contracts, and policies carry required structure. Shape conformance establishes the evaluated graph met selected shapes; it does not prove assertions are true or controls effective.

W3C [PROV-O](https://www.w3.org/TR/prov-o/) represents entities, activities, agents, generation, use, derivation, attribution, association, and delegation. These relations can connect requirements, interpretations, policy artifacts, decisions, enforcement, and derived products. Provenance supports assessment but does not itself establish authority or truth.

NIST's [OSCAL](https://pages.nist.gov/OSCAL/) provides machine-readable models for control catalogs, profiles, implementations, assessment plans, results, and remediation information. Its layering demonstrates that requirement, selected profile, implementation statement, observation, finding, and risk should remain distinct. A machine-readable control description is not automatically an executable rule or effectiveness proof.

NIST's [Cybersecurity Framework 2.0](https://www.nist.gov/cyberframework) organizes outcomes across Govern, Identify, Protect, Detect, Respond, and Recover and supports organizational profiles. Computational governance must cover the full operational loop rather than only preventative admission. Local tailoring remains necessary for data, privacy, product, and jurisdictional obligations.

The [SLSA specification](https://slsa.dev/spec/v1.2/) defines supply-chain security levels and attestation formats, including provenance. Policy bundles are security-sensitive artifacts: source controls, isolated builds, dependency identity, builder trust, signatures, verification, and incident response matter because altered governance code can authorize altered data behavior.

The OpenTelemetry [specification](https://opentelemetry.io/docs/specs/otel/) defines telemetry APIs, SDKs, resources, context propagation, traces, metrics, logs, semantic conventions, and protocols. Shared trace context can correlate policy administration, distribution, evaluation, enforcement, and data operations. Instrumentation and identifiers still require local semantic profiles.

OpenLineage's [object model](https://openlineage.io/docs/spec/object-model/) represents jobs, runs, datasets, and extensible facets. Lineage can help identify derived effects of a bad policy decision or changed obligation. Completeness, stable dataset identity, policy linkage, and cross-engine coverage remain architecture responsibilities.

The Bitol [Open Data Contract Standard](https://bitol-io.github.io/open-data-contract-standard/latest/) supplies machine-readable sections for product fundamentals, schemas, quality, support, pricing, teams, roles, service levels, and infrastructure. A federation can profile contracts as policy inputs while keeping contract declaration distinct from observed product behavior.

Together these sources support distributed policy decisions, controlled artifacts, enforceable boundaries, interoperable descriptions, traceable evidence, and continuous assessment. They do not choose legitimate authorities, resolve law, define enterprise risk appetite, or prove that an automated decision benefits affected people.

## Prerequisites and Retrieval

You should understand federated governance, data mesh, data products, policy as code, authorization, identity, attributes, data contracts, catalogs, classification, privacy, security, retention, lineage, control planes, distributed systems, eventual consistency, software supply chains, observability, incident response, audit, and recovery.

Retrieve constitution, delegation, reserved power, global invariant, domain policy, profile, interpretation, policy administration point, policy decision point, policy enforcement point, policy information point, rule, outcome, obligation, advice, applicability, combining algorithm, namespace, bundle, revision, activation, convergence, receipt, exception, emergency rule, shadow decision, canary, fail open, fail closed, effectiveness, appeal, remedy, recovery, and closure.

As a retrieval test, consider a domain rule that permits analysts to export a consumer dataset for fraud research. Ask who authorized the purpose; which global and local rules apply; how conflict is resolved; which identity, contract, classification, consent, geography, and time facts are trusted; which bundle revision every evaluator runs; where export is intercepted; how masking and retention obligations are applied; what evidence excludes sensitive input; how a person challenges error; and what happens during a partition. A green policy test cannot answer all of these questions.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish federated authority, computational policy, policy distribution, decision, enforcement, and assurance;
2. translate authorized governance interpretations into typed rules, structured outcomes, obligations, and tests without treating code as the authority;
3. compose global, jurisdictional, domain, product, and consumer policies with explicit applicability and conflict semantics;
4. design administration, information, decision, and enforcement points across heterogeneous data systems;
5. package, sign, distribute, activate, observe, roll back, and retire policy bundles across a dynamic fleet;
6. connect decisions to real operations, continuing use, derived data, lineage, and enforcement receipts;
7. govern exceptions, emergency rules, outages, appeals, correction, affected-party remedy, and incident response;
8. measure convergence, coverage, conformance, friction, bypass, effectiveness, cost, and outcomes with honest denominators;
9. migrate committees, tickets, scripts, and incompatible domain rules into a federated computational model; and
10. recover and close governance machinery without restoring obsolete authority or erasing required history.

## Core Exposition

**Begin with decisions, not engines.** Inventory recurring decisions about product publication, access, purpose, contract compatibility, classification, location, sharing, quality, retention, deletion, model use, exception, and retirement. For each, identify authority, scope, affected parties, evidence, implementation, appeal, and consequence.

**Write the constitutional minimum.** State nondelegable obligations, reserved powers, delegated decisions, shared decisions, prohibited actions, global invariants, evidence requirements, conflict rules, emergency power, amendment, review, and exit. Keep volatile thresholds in separately governed profiles.

**Separate authority from authorship.** A privacy officer may authorize an interpretation, a domain steward may supply semantics, a platform engineer may implement it, and a security reviewer may approve the artifact pipeline. Repository ownership alone grants none of those powers.

**Model delegation explicitly.** A delegation names grantor, grantee, decision type, product or data scope, purposes, environments, limits, policy version, evidence, effective interval, revocation, and escalation. The evaluation path verifies current delegation rather than trusting a team label.

**Define global invariants narrowly.** Shared requirements should protect genuine cross-domain externalities: enterprise identity, interoperable product metadata, minimum security and privacy, legal holds, deletion, audit, high-consequence sharing, and incident notification. Excessive global rules recreate centralized delivery.

**Allow bounded strengthening.** A domain can shorten retention, demand stronger authentication, add quality constraints, restrict a use, or require extra monitoring. It cannot silently remove an applicable global deny or obligation. A formal partial order can describe which changes are demonstrably stricter only for a precisely modeled rule family.

**Avoid naïve monotonicity.** Adding a condition can narrow permission but adding a broad deny exception can expand it. Obligations, defaults, missing data, conflicts, time, and rule interaction break simple “local may only strengthen” claims. Test composed behavior rather than relying on labels.

**Trace policy to interpretation.** Each rule references source requirement, authorized interpretation, decision record, scope, owner, reviewer, version, and effective time. When the interpretation changes, create a new traceable revision rather than rewriting history.

**Use typed decision contracts.** Define principals, workloads, teams, tenants, resources, products, fields, actions, purposes, locations, relationships, risk, time, and context. Specify required and optional inputs, authoritative issuers, validation, missing behavior, result vocabulary, reasons, obligations, advice, validity, and latency.

**Use multi-valued outcomes.** `permit`, `deny`, `not_applicable`, `conflict`, and `indeterminate` expose states a Boolean hides. An enforcement point maps each outcome to operational behavior under a reviewed contract. Unknown facts must not be converted silently to permission.

**Treat obligations as executable contracts.** A permit may require masking, aggregation, watermarking, logging, notification, retention, geographic routing, rate limit, approval, or later deletion. The enforcement point must either apply supported obligations and report them or reject the operation.

**Govern policy inputs.** Identity, classification, consent, purpose, location, product contract, risk, and time are policy information. Each fact needs stable identity, definition, issuer, collection path, valid time, observation time, freshness, confidence where relevant, sensitivity, and revocation.

**Do not trust assertions merely because they are structured.** A requester's `purpose="research"` is a claim. Bind purpose to an authorized work item, product use, delegation, or consent context appropriate to the consequence. Treat user-controlled tags and catalog fields according to their trust.

**Compose by authority and scope.** First select policies applicable to actor, product, data, action, purpose, jurisdiction, environment, consumer, and time. Then combine results using an explicit algorithm. Policy filenames, repository paths, event arrival, and evaluator load order do not confer precedence.

**Make conflict visible.** Two legitimate authorities may disagree, or a domain rule may contradict a global invariant. Return a conflict with participating policy identities, scopes, and a resolution path. Quietly choosing the latest or most permissive rule destroys federation evidence.

**Define obligation merging.** Two permits may require different retention, masking, notice, or location duties. State whether obligations intersect, union, override, or conflict by type. Detect impossible combinations before granting a permit.

**Partition policy namespaces.** Assign roots or packages to durable authorities and prevent overlapping ownership. Shared rules live under a shared authority. Validate dependencies, imports, cycles, version ranges, and prohibited references before building a federation bundle.

**Separate administration from runtime.** Administration manages sources, interpretations, schemas, rules, tests, approvals, artifacts, rollout, exceptions, and retirement. Runtime supplies information, evaluates decisions, enforces operations, and emits evidence. Compromise in either plane has different containment and recovery needs.

**Choose a decision topology deliberately.** Central services simplify convergence and audit but add network dependency and concentration. Sidecars and node agents reduce latency but multiply fleet state. Embedded evaluators can cover offline paths but complicate updates and evidence. Hybrid designs need one decision contract and explicit consistency.

**Put enforcement on every material path.** Inventory APIs, SQL, notebooks, batch jobs, streams, object storage, exports, replicas, caches, files, administration, break-glass, backups, and restore. A perfect decision engine beside one gateway leaves alternate paths ungoverned.

**Enforce at adequate granularity.** Dataset-level checks cannot express row, column, record, subject, purpose, aggregate, output, or time conditions. If an engine cannot enforce an obligation, mediate through a capable service, transform the product, or reject that use.

**Cover continuing and derived use.** A permitted read can create a feature, model, report, file, cache, or new data product. Bind derivative identity, provenance, policy, purpose, retention, deletion, and distribution. Re-evaluate when relevant data, actor, purpose, location, consent, or policy changes.

**Package immutable policy state.** A bundle includes policy, schemas, trusted reference data, namespace roots, manifest, dependencies, compiler and engine compatibility, build provenance, digest, signature, authority, and effective interval. Reproducible build and verification reduce artifact substitution risk.

**Test semantics before activation.** Run parsing, types, schemas, positive and negative decision tables, missing and stale inputs, boundaries, properties, mutation, composition, differential evaluation, performance, and enforcement integration. Derive expected results from reviewed interpretations, not current engine output.

**Protect the policy supply chain.** Apply least privilege, separation of duties, reviewed changes, isolated builds, dependency controls, provenance, signing, key rotation, artifact verification, protected storage, and incident response. A malicious policy bundle can produce authorized-looking harm.

**Activate compatible state atomically.** Policy and required reference data must move as a compatible set. Stage, verify, load, run health checks, and switch the active revision. Preserve a last known acceptable revision without assuming it remains safe after schema, identity, or legal changes.

**Measure fleet convergence.** Record eligible evaluators and enforcement points, active bundle digest, data revision, engine and schema versions, activation time, health, last decision, and reachability. Publish stale, failed, unknown, excluded, and quarantined nodes.

**Use shadow and canary evaluation.** Replay retained bounded inputs and compare proposed with active results. Segment allow-to-deny, deny-to-allow, obligation, error, and latency differences by consequence. Shadow evidence reveals change; human interpretation determines whether it is intended.

**Design rollback and roll-forward.** A rollback must restore a mutually compatible policy, schema, data, and engine set. It cannot undo operations already permitted or recreate revoked authority. When external state moved, a corrected forward revision can be safer.

**Issue decision and enforcement receipts.** A receipt identifies request, principal and resource references, action, purpose, policy and data revisions, normalized input digest, outcome, reasons, obligations, enforcement point, operation, effects, and times. Link rather than duplicate sensitive values where possible.

**Minimize evidence.** Decision inputs can expose identity, health, financial, location, or security data. Mask, tokenize, separate, encrypt, restrict, retain, delete, and hold evidence according to purpose. Record evidence gaps and dropped logs; do not imply completeness.

**Provide audience-specific explanations.** Requesters need actionable reasons and correction paths. Operators need dependency and revision details. Auditors need authority, integrity, sampling, and effects. Affected people need understandable grounds, challenge, and remedy without exposure of other protected data.

**Model exceptions as decisions.** An exception identifies requirement, rule, scope, rationale, risk owner, affected parties, compensating controls, monitoring, effective interval, renewal ceiling, closure, and appeal. Generate a bounded executable rule when appropriate but preserve the authoritative exception record.

**Constrain emergency governance.** Break-glass authority names eligible actors, resources, actions, purposes, conditions, duration, obligations, monitoring, notification, and retrospective review. Test automatic expiry and recovery. An incident is not permission to discard evidence.

**Choose outage behavior by consequence.** Fail closed, fail open, last known acceptable bundle, bounded cache, degraded read-only mode, or human authorization each transfers risk. Specify permitted duration, stale-data boundary, evidence, alerting, escalation, review, and exit for every decision class.

**Operate revocation as a service objective.** Measure time from authority, identity, consent, classification, or policy revocation to effective enforcement across the eligible fleet and caches. Average bundle freshness can hide one dangerous stale node.

**Separate conformance from effectiveness.** A policy can compile, pass tests, deploy everywhere, and return expected decisions while users bypass it or legitimate work becomes impossible. Observe real operations, blocked work, appeals, incidents, downstream effects, and stakeholder outcomes.

**Measure friction honestly.** Track decision latency, false blocks, retries, abandonment, support, manual overrides, exception demand, and time to remedy. Segment by domain, product, purpose, consequence, and affected group. Governance that cannot be used safely will be routed around.

**Audit the federation itself.** Review authority concentration, domain representation, conflicts, exception patterns, rule ownership, evidence access, cross-domain effects, policy debt, platform dependency, and appeal outcomes. Computational governance can scale institutional bias as efficiently as good controls.

**Correct effects, not only code.** On a bad rule or bad input, issue a new version, identify affected decisions and operations, follow lineage into derived data, revoke access, delete or repair outputs, notify affected parties, compensate where required, and verify closure. Preserve the original history.

**Plan migration as semantic reconciliation.** Inventory committees, tickets, standards, scripts, engine rules, database grants, cloud policies, contracts, exceptions, identities, enforcement paths, and undocumented practice. Map overlapping meanings and authority before translating syntax.

**Migrate incrementally.** Establish identities and decision contracts, shadow current outcomes, automate bounded high-volume decisions, add receipts, close bypasses, then expand. Preserve a controlled fallback without reintroducing invisible approvals or stale authority.

**Recover governance before data operations.** Restore constitution, authority, delegations, identity, trusted information, current signed bundles, active exceptions, emergency state, legal holds, deletions, tombstones, evidence keys, and time. Then verify convergence before resuming dependent processing.

**Close end to end.** Retire source interpretations, rules, bundles, signing keys, evaluators, caches, exceptions, emergency rules, enforcement bindings, credentials, and recovery activation. Retain controlled historical artifacts and reproducible evaluation where obligations require it.

## Definitions and Notation

Let the governance system be:

`G = (C, A, P, D, E, R, O, X, M, L)`.

Represent an authority as:

`a = (id, source, powers, scope, constraints, effective, revocation, appeal)`.

Represent an executable rule as:

`r = (id, authority, interpretation, scope, inputs, condition, outcome, obligations, version, effective)`.

Let a decision request be:

`q = (principal, action, resource, product, purpose, context, relationships, time)`.

Let `Select(P,q,t)` choose applicable policies from global, jurisdictional, domain, product, and consumer sets. Let:

`Decide(Select(P,q,t), q, I(t)) -> (result, reasons, obligations, valid_until)`

where `I(t)` is identified policy information and `result` belongs to `{permit, deny, not_applicable, conflict, indeterminate}`.

Represent enforcement evidence as:

`e = (decision_id, operation_id, point, resource_version, obligations_applied, status, effects, started, completed)`.

Define convergence at time `t` for target revision `v` as:

`Conv(v,t) = known_eligible_points_at_v / known_eligible_points`.

Unknown and excluded points remain separate counts. A ratio of one over an incomplete denominator proves little.

Define enforcement coverage as:

`Cov = materially_protected_operation_classes / known_material_operation_classes`.

Define revocation latency as:

`T_r = last_unsafe_authority_end - authoritative_revocation_time`.

Define the actual correction set `Impact(d)` as operations and derived effects linked to defective decisions through receipts, telemetry, and lineage. It differs from every request that could theoretically have matched.

Define closure `Closed(v)` to require no active evaluator, bundle, cache, exception, emergency rule, credential, enforcement binding, consumer, or recovery path can use retired revision `v`, while required historical evidence remains controlled.

## Mechanisms, Invariants, or Proof Structure

Use the following assurance gates.

**Constitution gate.** Verify purpose, participants, global invariants, reserved and delegated powers, conflicts, amendment, emergency authority, evidence, remedy, and exit.

**Authority gate.** Verify source, identity, power, scope, delegation chain, constraints, effective time, revocation, independence, and appeal.

**Interpretation gate.** Link requirement, context, findings, affected parties, ambiguity, decision, owner, review, version, and limitations.

**Contract gate.** Type subjects, resources, actions, purposes, context, outcomes, reasons, obligations, validity, errors, latency, and failure behavior.

**Information gate.** Check identity, issuer, definition, collection, valid time, observation time, freshness, confidence, revocation, sensitivity, and minimization.

**Composition gate.** Define applicability, namespace ownership, precedence, combining algorithm, conflicts, not-applicable behavior, indeterminate behavior, and obligation merging.

**Artifact gate.** Protect sources, schemas, tests, dependencies, build, provenance, digest, signature, approval, storage, and compatibility.

**Distribution gate.** Verify staging, activation, canary, convergence, stale nodes, incompatibility, rollback, roll-forward, and revocation objectives.

**Enforcement gate.** Inventory real operations, alternate paths, granularity, obligations, time of use, continuing use, derived outputs, bypass, and receipts.

**Evidence gate.** Join authority, request, bounded inputs, revisions, decision, reasons, obligations, enforcement, effects, integrity, access, retention, and deletion.

**Resilience gate.** Define partitions, fail mode, last-known state, caches, emergency rules, duration, alerts, escalation, review, and exit by consequence.

**Exception gate.** Record requirement, deviation, scope, rationale, risk, compensation, approver, affected parties, monitoring, expiry, renewal, and closure.

**Effectiveness gate.** Measure coverage, convergence, enforcement, friction, bypass, incidents, appeals, remedies, risk, cost, and stakeholder outcomes.

**Correction gate.** Preserve history, find actual effects, publish corrected policy, revoke, repair, notify, support challenge, and verify remedy.

**Recovery gate.** Restore current authority, identity, information, policy, exceptions, holds, deletion, evidence, time, and convergence before processing.

**Closure gate.** Prevent retired authority and artifacts from active or recovery use while preserving controlled historical interpretation and evidence.

### Executable evidence: federated policy-change evaluation

The following program classifies ten invented policy changes against six declared governance requirements.

<!-- bijux-verify: {"id":"federated-policy-change-evaluation","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"changes=10\nqualified=4\nmissing_authority=1\nglobal_conflict=1\nstale_bundle=1\nmissing_enforcement=1\nmissing_receipt=1\nexpired_exception=1\nnamed_authorities=9\nglobal_rules=4\ndomain_rules=14\npolicy_revisions=3\nenforcement_points=5\nreceipts=9\nexceptions=1\ndecision_events=10\n","stderr":""}} -->
```python
changes = [
    {"domain": "orders", "authority": "orders-steward", "global_ok": True, "bundle": "r3", "point": "gateway", "receipt": True, "exception": None, "rules": 2},
    {"domain": "fraud", "authority": "fraud-owner", "global_ok": True, "bundle": "r3", "point": "stream", "receipt": True, "exception": None, "rules": 2},
    {"domain": "science", "authority": "science-owner", "global_ok": True, "bundle": "r3", "point": "workspace", "receipt": True, "exception": None, "rules": 1},
    {"domain": "finance", "authority": "finance-controller", "global_ok": True, "bundle": "r3", "point": "warehouse", "receipt": True, "exception": None, "rules": 2},
    {"domain": "marketing", "authority": None, "global_ok": True, "bundle": "r3", "point": "gateway", "receipt": True, "exception": None, "rules": 1},
    {"domain": "support", "authority": "support-owner", "global_ok": False, "bundle": "r3", "point": "warehouse", "receipt": True, "exception": None, "rules": 1},
    {"domain": "identity", "authority": "identity-owner", "global_ok": True, "bundle": "r1", "point": "gateway", "receipt": True, "exception": None, "rules": 1},
    {"domain": "shipping", "authority": "shipping-owner", "global_ok": True, "bundle": "r3", "point": None, "receipt": True, "exception": None, "rules": 1},
    {"domain": "people", "authority": "people-officer", "global_ok": True, "bundle": "r3", "point": "batch", "receipt": False, "exception": None, "rules": 1},
    {"domain": "research", "authority": "research-owner", "global_ok": True, "bundle": "r3", "point": "workspace", "receipt": True, "exception": "expired", "rules": 2},
]

def evaluate(change):
    if change["authority"] is None:
        return "missing_authority"
    if not change["global_ok"]:
        return "global_conflict"
    if change["bundle"] != "r3":
        return "stale_bundle"
    if change["point"] is None:
        return "missing_enforcement"
    if not change["receipt"]:
        return "missing_receipt"
    if change["exception"] == "expired":
        return "expired_exception"
    return "qualified"

results = [evaluate(change) for change in changes]
print(f"changes={len(changes)}")
for outcome in ["qualified", "missing_authority", "global_conflict", "stale_bundle", "missing_enforcement", "missing_receipt", "expired_exception"]:
    print(f"{outcome}={results.count(outcome)}")
print(f"named_authorities={len({change['authority'] for change in changes if change['authority']})}")
print("global_rules=4")
print(f"domain_rules={sum(change['rules'] for change in changes)}")
print(f"policy_revisions={len({'r1', 'r2', 'r3'})}")
print(f"enforcement_points={len({change['point'] for change in changes if change['point']})}")
print(f"receipts={sum(change['receipt'] for change in changes)}")
print(f"exceptions={sum(change['exception'] is not None for change in changes)}")
print(f"decision_events={len(results)}")
```

The output reports ten changes, four qualified and one of each declared failure, nine named authorities, four global rules, fourteen domain rules, three revisions, five enforcement points, nine declared receipts, one exception, and ten decisions.

The evidence is deliberately narrow. Invented strings and Booleans do not prove legitimate authority, correct global invariants, policy semantics, compatible bundles, enforcement, evidence integrity, exception legitimacy, federation, fairness, or effectiveness. Production assurance requires authoritative records, semantic tests, signed artifact provenance, fleet observations, enforcement integration tests, protected receipts, incident and appeal evidence, and affected-party outcomes.

## Alternatives and Trade-Offs

**Central governance service.** Consistency and visibility improve. Latency, concentration risk, domain-context loss, and central queues can grow.

**Federated policy contribution.** Domains encode local meaning and change faster. Namespace, composition, capability, and assurance demands increase.

**Central decision point.** Convergence is simple and decisions are easy to aggregate. Network partitions and capacity become shared failure modes.

**Distributed decision points.** Latency and autonomy improve. Version skew, observability, revocation, and recovery become harder.

**Embedded evaluator.** Offline and high-throughput paths gain reliability. Upgrades, inventory, evidence, and language compatibility require discipline.

**Admission enforcement.** Bad desired state can be blocked early. Reads, continuing use, runtime drift, and external operations need other controls.

**Runtime enforcement.** Current context and effects are visible. Latency, availability, bypass, and partial effects must be handled.

**Deny overrides.** Conservative combination protects against conflicting permissions. One overly broad deny can halt legitimate cross-domain work.

**Permit overrides.** Explicit enabling rules are easy to express. A narrow local permit can accidentally defeat a critical global control.

**Most-specific rule.** Local context can dominate broad defaults. Specificity needs formal semantics and does not establish superior authority.

**Fail closed.** Unauthorized effects are bounded. Critical legitimate operations can fail during control-plane incidents.

**Fail open.** Availability is preserved. The outage transfers risk to data, people, and later remediation.

**Last known acceptable bundle.** Local operation survives distribution loss. Revocation, consent, classification, and law can make cached policy unsafe.

**Rich decision logs.** Investigation and replay improve. Sensitive input, cost, insider access, and retention exposure increase.

**Minimal receipts.** Privacy and storage risk decrease. Root-cause analysis, correction, and independent assurance may become impossible.

**One policy language.** Tooling and skills consolidate. Domain-specific semantics and heterogeneous enforcement can be distorted.

**Multiple policy languages.** Local fit improves. Equivalence, composition, evidence, migration, and common testing become harder.

**Immediate global rollout.** Revocation and urgent correction are fast. A defective rule can spread enterprise-wide.

**Canary rollout.** Differences and operational defects surface early. The fleet temporarily makes different decisions and needs bounded routing.

**Automatic exception generation.** Delivery friction falls. Authority and risk acceptance can become a hidden code path.

## Failure Modes and Misconceptions

1. **“A council makes governance federated.”** Federation requires bounded local authority and coordination protocols.
2. **“A policy repository makes governance computational.”** Code must reach and govern a real operation.
3. **“Automation makes a rule legitimate.”** Legitimacy comes from authorized interpretation and due process.
4. **“Policy authors are policy authorities.”** Implementation responsibility and decision power are distinct.
5. **“Every governance statement can become a Boolean.”** Ambiguity, conflict, duties, discretion, and missing facts require richer outcomes.
6. **“Global policy should encode every detail.”** Excessive central rules destroy local competence and adaptability.
7. **“Domain autonomy permits local waiver.”** Nondelegable obligations remain binding.
8. **“Local rules only strengthen global rules.”** Composition can expand permission through exceptions, defaults, and interaction.
9. **“Latest policy wins.”** Recency does not establish authority or compatibility.
10. **“Load order is a combining algorithm.”** Incidental order is not governance semantics.
11. **“Deny-overrides solves every conflict.”** It can turn one broad error into an enterprise outage.
12. **“Most-specific means most authoritative.”** Specificity and legitimate power are different relations.
13. **“Unknown means deny.”** Sometimes it means missing evidence, system failure, or non-applicability requiring distinct remedy.
14. **“Permit needs no obligations.”** Legitimate use can require masking, notice, retention, or monitoring.
15. **“Obligations can simply be unioned.”** Duties can contradict or become impossible together.
16. **“Structured input is trusted input.”** Caller-controlled purpose or classification remains an assertion.
17. **“Current attributes have current meaning.”** Definitions, issuer, valid time, observation time, and freshness matter.
18. **“One subject identifier is enough.”** Human, workload, team, tenant, and delegated identities differ.
19. **“One resource identifier is enough.”** Product, distribution, dataset, field, row, version, and derived output can differ.
20. **“A decision proves enforcement.”** The operation may bypass, ignore, or misapply it.
21. **“A policy engine is an enforcement point.”** It returns a decision; another component controls the effect.
22. **“The gateway covers data access.”** SQL, files, jobs, caches, replicas, notebooks, and restore may bypass it.
23. **“Admission controls runtime.”** It sees selected mutations, not every continuing operation.
24. **“Dataset-level enforcement is sufficient.”** Policy may depend on fields, records, purpose, output, and time.
25. **“Initial access governs derived data.”** New products and copies need identity, lineage, policy, and lifecycle.
26. **“A compiled policy is correct.”** Compilation proves language validity, not intended semantics.
27. **“Passing tests prove correctness.”** Tests cover only selected inputs and assertions.
28. **“Line coverage measures policy assurance.”** Decision boundaries, composition, mutation, and integration matter.
29. **“Signed bundles are safe bundles.”** Signatures establish integrity and publisher under a key policy, not correct content.
30. **“Policy and data can deploy independently.”** Incompatible revisions can invert outcomes.
31. **“Deployment success means convergence.”** Unknown, offline, stale, and excluded nodes may remain.
32. **“Average freshness proves revocation.”** One dangerous stale evaluator can preserve authority.
33. **“Rollback is always safe.”** Old policy may conflict with current identity, schema, consent, or law.
34. **“Shadow agreement proves correctness.”** Active and proposed policies can share the same error.
35. **“Decision logs are enforcement evidence.”** They do not show the protected effect occurred or was blocked.
36. **“Log everything for audit.”** Sensitive input and long retention can create new harm.
37. **“No log means no decision.”** Logging can fail or drop events independently of evaluation.
38. **“Exceptions are policy comments.”** They require authority, scope, risk, compensation, expiry, and closure.
39. **“Renewed exceptions remain temporary.”** Repeated renewal can institutionalize an unreviewed baseline change.
40. **“Break glass suspends governance.”** Emergency authority needs narrower scope, stronger evidence, and review.
41. **“Fail closed is always safest.”** It can block safety-critical or recovery operations.
42. **“Fail open preserves service.”** It transfers consequences to data subjects, consumers, and remediation.
43. **“Low denial rate means good governance.”** It can mean permissive rules, bypass, or unsuitable denominators.
44. **“High denial rate means strong governance.”** It can mean false blocks and unusable paths.
45. **“Conformance proves effectiveness.”** Controls can exist without changing harmful behavior.
46. **“A policy platform owns governance decisions.”** It owns capability behavior, not every risk or legal judgment.
47. **“Federation removes central power.”** It makes reserved, delegated, and shared power explicit.
48. **“Correction ends with a new rule.”** Prior decisions, derived effects, people, and products may need remedy.
49. **“Restoring data restores governance.”** Authority, identity, policy, exceptions, holds, and tombstones must be current first.
50. **“Stopping bundle distribution retires policy.”** Caches, images, agents, credentials, and recovery paths can reactivate it.

## Worked Examples

### Example 1

A global rule prohibits exporting restricted identity data outside approved regions. The Identity domain adds a stricter local rule requiring monitored sessions. Composition returns permit only inside an approved region with the monitoring obligation; the local rule cannot create an export exception.

### Example 2

Marketing labels a request `purpose=research`. The information point finds no authorized research work item and returns indeterminate. The enforcement point blocks export and supplies a correction path rather than silently treating the label as trusted purpose.

### Example 3

Two legitimate policies permit an aggregate but require mutually incompatible retention periods. Composition returns conflict with both rule identities. The federation's records and privacy authorities resolve the interpretation instead of relying on file order.

### Example 4

A new bundle changes some permits to denies. Replay and shadow evaluation segment differences by product and consequence. A canary catches an unsupported masking obligation before the bundle reaches all warehouse enforcement points.

### Example 5

An edge evaluator remains on revision `r41` after revocation in `r42`. The convergence denominator lists it as stale, routing stops high-consequence requests to it, and the revocation objective remains failed until the node updates or is removed.

### Example 6

An API records a permit, but an object-store copy job ignores the returned retention obligation. Joining the decision with an enforcement receipt exposes the failure. Decision-log success alone would have concealed it.

### Example 7

A two-hour emergency exception permits responders to query a restricted incident product. The rule limits actors, purpose, fields, output, and time; adds monitoring and notification; expires automatically; and triggers retrospective review.

### Example 8

A policy-engine outage makes public catalog reads use a bounded last-known bundle while restricted exports fail closed. Clinical recovery actions use a separate tightly monitored emergency contract. One universal outage behavior would mishandle at least one class.

### Example 9

A defective consent mapping permitted 37 exports. Receipts identify actual operations, OpenLineage connects six derived products, and the correction process revokes access, deletes invalid copies, notifies owners, and records affected-person remedy.

### Example 10

During disaster recovery, the platform restores current authority, identity, revocations, classifications, legal holds, deletion tombstones, signed bundles, and evidence keys. It verifies evaluator convergence before pipelines resume, preventing an old backup from reviving expired permission.

## Cross-Program Connections

- [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) owns consistent decision APIs, identity propagation, error contracts, idempotency, and enforcement at service boundaries.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md) owns policy distribution, fleet inventory, capability integration, paved paths, supply-chain controls, observability, and recovery mechanisms.
- [Data Engineering](../../19-data-engineering/ROADMAP.md) owns enforcement in pipelines, streams, orchestration, storage, quality, lineage emission, and derived-data lifecycle.
- [Large-Scale Data Systems Engineering](../../21-large-scale-data-systems-engineering/ROADMAP.md) owns engine-level authorization, isolation, query, storage, streaming, consistency, and failure behavior.
- [Database Engineering](../../18-database-engineering/ROADMAP.md) owns database grants, row and column controls, transaction boundaries, audit behavior, backup, restore, and physical deletion.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) owns threat modeling, identity assurance, least privilege, key management, supply-chain integrity, privacy controls, detection, and incident response.
- [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md) owns authority boundaries, decision topology, dependency direction, resilience, compatibility, and evolution of governance services.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies reasoning about partial failure, replication, clocks, convergence, partitions, and impossibility of instantaneous fleet state.
- [Systems Engineering](../../26-systems-engineering/ROADMAP.md) supplies stakeholder, assurance, hazard, lifecycle, recovery, and emergent-risk reasoning for the whole governance system.

## References

1. Zhamak Dehghani, [Data Mesh Principles and Logical Architecture](https://martinfowler.com/articles/data-mesh-principles.html), federated computational governance and logical architecture.
2. Open Policy Agent, [Policy Language](https://www.openpolicyagent.org/docs/policy-language), declarative policy over structured inputs.
3. Open Policy Agent, [Bundles](https://www.openpolicyagent.org/docs/management-bundles), policy distribution, namespace roots, signing, and activation.
4. Open Policy Agent, [Decision Logs](https://www.openpolicyagent.org/docs/management-decision-logs), decision evidence and masking.
5. Open Policy Agent, [How to Deploy OPA](https://www.openpolicyagent.org/docs/deploy), decision-point placement and integration.
6. Kubernetes, [Admission Control](https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/), mutation and validation enforcement boundaries.
7. CNCF Application Delivery Technical Advisory Group, [Platforms White Paper](https://tag-app-delivery.cncf.io/whitepapers/platforms/), platforms as user-centered capabilities.
8. W3C, [ODRL Information Model 2.2](https://www.w3.org/TR/odrl-model/), permissions, prohibitions, duties, parties, assets, and constraints.
9. W3C, [Shapes Constraint Language](https://www.w3.org/TR/shacl/), graph constraints and validation reports.
10. W3C, [PROV-O](https://www.w3.org/TR/prov-o/), provenance entities, activities, agents, and qualified relations.
11. NIST, [Open Security Controls Assessment Language](https://pages.nist.gov/OSCAL/), machine-readable control, implementation, assessment, and remediation models.
12. NIST, [Cybersecurity Framework 2.0](https://www.nist.gov/cyberframework), govern-through-recover risk outcomes and profiles.
13. SLSA, [Specification 1.2](https://slsa.dev/spec/v1.2/), software supply-chain levels and provenance attestations.
14. OpenTelemetry, [Specification](https://opentelemetry.io/docs/specs/otel/), telemetry signals, context, resources, semantics, and protocols.
15. OpenLineage, [Object Model](https://openlineage.io/docs/spec/object-model/), jobs, runs, datasets, events, and facets.
16. Bitol, [Open Data Contract Standard](https://bitol-io.github.io/open-data-contract-standard/latest/), machine-readable data-product contract sections.

## Exercises

### Exercise 1

Design a federation constitution and computational governance model for four domains sharing customer, payment, support, and fraud products. Define reserved, delegated, shared, and prohibited decisions; global invariants; authority records; conflict and appeal; and success measures.

### Exercise 2

Specify a typed decision contract and composition algorithm for exporting a product whose policies depend on principal, purpose, classification, consent, location, retention, and consumer contract. Include multi-valued outcomes, obligations, missing inputs, conflict, and time of use.

### Exercise 3

Design the administration, information, decision, and enforcement topology for a warehouse, stream platform, notebooks, object storage, and external exports. Address bundle distribution, namespace ownership, fleet convergence, alternate paths, receipts, and derived data.

### Exercise 4

Create a rollout, outage, exception, and incident plan for a policy revision that changes high-consequence permits. Include semantic tests, differential evaluation, canary, rollback or roll-forward, fail modes, emergency authority, correction, and remedy.

### Exercise 5

Plan migration from councils, ticket approvals, database grants, cloud policies, pipeline checks, and permanent exceptions to federated computational governance. Include inventory, semantic reconciliation, shadowing, staged enforcement, recovery, and closure.

## Answers to the Exercises

### Answer 1

The constitution reserves enterprise identity, high-consequence external sharing, legal hold, rights fulfillment, and minimum security and privacy. Domains decide local quality, supported purposes, consumer fitness, and stricter controls; shared customer identity and fraud semantics use named cross-domain authorities. Prohibited decisions include waiving law or hiding conflicts. Every delegation binds scope, time, evidence, revocation, and appeal. Measures separate decision lead time, local autonomy, conflict, conformance, enforcement, false blocks, incidents, remedy, and affected-party outcomes.

### Answer 2

The request carries stable principal, workload, team, tenant, product, distribution, fields, action, authorized purpose, consumer contract, source and target location, time, and operation identity. Trusted information adds classification, consent, relationship, retention, holds, and versions. Applicability selects global, jurisdictional, provider, domain, product, and consumer policies. Composition returns permit, deny, not applicable, conflict, or indeterminate with reasons, obligations, and validity. Unsupported or conflicting obligations prevent execution; long-running export rechecks revocation-sensitive facts before effect.

### Answer 3

Administration builds signed compatible bundles under partitioned authority namespaces. Governed information services supply identity, classification, consent, contracts, location, and time. Low-latency local decision points cover warehouse, stream, notebook, storage, and export paths while a central plane inventories revisions and evidence. Enforcement exists at query, job submission, stream subscription, object operation, and egress. Receipts link operation effects, and lineage registers derivatives. Fleet reports every eligible, stale, unknown, or quarantined point rather than only healthy reporters.

### Answer 4

Trace the revision to an approved interpretation, then run types, tables, missing inputs, boundaries, composition, mutation, integration, load, and adversarial tests. Differentially replay bounded cases and classify every permit, deny, obligation, error, and latency change. Canary by low-consequence cohorts before high-consequence paths. Define compatible roll-forward and rollback sets. Assign fail modes per decision class. Emergency rules expire automatically. If harm occurs, preserve history, find operations and derivatives through receipts and lineage, revoke, repair, notify, support challenge, and verify remedy.

### Answer 5

Inventory every decision, authority, standard, interpretation, ticket, grant, rule, identity, information source, engine, path, exception, incident, and restore procedure. Reconcile meaning and power before translating code. Establish stable identities, typed contracts, namespace ownership, global invariants, and receipts. Shadow existing outcomes, automate bounded frequent decisions, add enforcement path by path, and close bypasses only after evidence. Replace permanent exceptions with explicit expiring records. Recovery restores current authority and policy first; closure revokes old grants, agents, caches, keys, bundles, and recovery activation while retaining required history.
