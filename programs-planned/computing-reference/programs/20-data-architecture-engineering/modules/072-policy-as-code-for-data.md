---
module_id: DARCH-072
program: Data Architecture Engineering
level: 2
module_number: 72
title: Policy as Code for Data
status: complete
last_verified: 2026-09-03
---

# Policy as Code for Data

## One-Page Review

### Governing question

How should an organization translate authorized data policy into versioned, testable, distributable, explainable, and enforceable decision logic without confusing executable rules with legal interpretation, governance authority, complete context, or proof of compliant outcomes?

### Essential definitions

- **Policy** is an authoritative statement of required, permitted, prohibited, or discretionary behavior for a defined scope.
- **Policy as code** is a governed executable representation of selected policy decisions, constraints, obligations, and evidence requirements.
- A **policy source** is the authoritative law, regulation, contract, standard, organizational decision, risk acceptance, or domain rule from which an executable rule is derived.
- A **policy rule** maps typed facts and context to a declared decision, reasons, obligations, advice, and evidence under a specific policy version.
- A **policy administration point** manages policy source, authorship, review, versions, distribution, activation, and retirement.
- A **policy decision point** evaluates a request against policies and relevant data and returns a structured decision.
- A **policy information point** supplies authoritative subject, resource, action, purpose, environment, and relationship attributes.
- A **policy enforcement point** obtains a decision and correctly applies it to the protected operation and its continuing effects.
- A **decision contract** defines inputs, identity, types, missing-data behavior, possible outcomes, reasons, obligations, version evidence, latency, and failure behavior.
- **Permit**, **deny**, **not applicable**, **conflict**, and **indeterminate** are distinct outcomes; reducing all uncertainty to a Boolean can create unsafe behavior.
- An **obligation** is an action that must be performed with or after a decision, such as masking, logging, notification, deletion, watermarking, or review.
- A **policy bundle** is an immutable, identified, integrity-protected set of executable policies, schemas, trusted data, manifests, and metadata distributed for evaluation.
- **Policy conformance** means an artifact satisfies declared structural and semantic requirements; **policy effectiveness** asks whether enforcement achieved the intended outcome.
- **Decision evidence** links a request, normalized inputs, applicable policy and data versions, result, reasons, obligations, enforcement observation, and time without unnecessarily retaining sensitive data.
- **Closure** retires policy sources, compiled artifacts, bundles, caches, decisions, exceptions, enforcement hooks, and recovery paths while preserving required historical interpretation.

### Central model, mechanism, or theorem

Represent a policy-as-code system as:

`P = (A, S, I, R, D, E, V, T, O, L)`

where `A` is legitimate authority, `S` source and interpretation, `I` typed input and authoritative attributes, `R` rules and composition, `D` decision semantics, `E` enforcement and evidence, `V` versions and distribution, `T` tests and assurance, `O` operation and outcome feedback, and `L` lifecycle and closure. Correct engine evaluation is necessary but insufficient: policy intent is preserved only when source interpretation, input truth, rule composition, bundle activation, enforcement, obligations, continuing use, and correction all satisfy the decision contract.

### Critical invariants

- Every executable rule traces to an authorized source, interpretation decision, owner, reviewer, scope, version, and effective interval.
- Principal, resource, action, purpose, environment, policy, attribute, and decision identities are stable and unambiguous.
- Missing, stale, conflicting, untrusted, or out-of-scope inputs do not silently become safe default values.
- Decision results distinguish permit, deny, not applicable, conflict, and indeterminate where the decision contract requires them.
- A permit is unusable until every mandatory obligation is acknowledged or completed at the required enforcement boundary.
- Policy and trusted data activate atomically by compatible immutable versions; partial rollout is visible.
- Enforcement covers the actual operation, data granularity, derived outputs, continuing use, and time-of-check/time-of-use risk named by policy.
- Decision evidence identifies the evaluated versions and enforcement result while minimizing sensitive input and output retention.
- Test, validation, compilation, signature, deployment, activation, and outcome evidence remain distinct.
- Exceptions and emergency rules are narrower than ordinary policy, time-bounded, attributable, observable, and tested for removal.
- Correction preserves original decisions and identifies affected actions rather than rewriting policy history.
- Retirement removes active evaluation and enforcement dependencies and cannot be undone silently by restore or replay.

### Common failures

Common failures include translating ambiguous prose directly into a Boolean; treating repository ownership as policy authority; embedding identity and purpose assumptions in application code; using deny-by-default without defining indeterminate and essential continuity; accepting self-asserted attributes; reading mutable external data during supposedly reproducible evaluation; distributing unsigned unversioned files; activating policy and data separately; testing syntax but not decision tables; reviewing only permit cases; treating shadow decisions as enforcement evidence; logging secrets and sensitive attributes; returning permit before obligations can be enforced; ignoring filters, caches, exports, copies, and derived data; trusting a decision after relevant state changes; allowing emergency rules to persist; and restoring retired bundles after disaster recovery.

### Compact example

Eight invented data requests are evaluated under two policy versions and four toy rules. Six requests have complete required inputs. Three are permitted, three denied, and two indeterminate. The permitted decisions produce five obligation instances across three obligation types. Two regions, six purposes, five resources, and three high-consequence requests appear. Executable evidence confirms only those declared values and branches. It proves no policy authority, attribute truth, legal correctness, enforcement, obligation completion, security, privacy, or beneficial outcome.

### Connections

[DARCH-027](027-producer-and-consumer-contracts.md), [DARCH-057](057-shared-code-sets-and-controlled-vocabularies.md), [DARCH-064](064-lineage-architecture.md), [DARCH-069](069-metadata-apis-and-eventing.md), [DARCH-070](070-connecting-technical-metadata-to-business-meaning.md), and [DARCH-071](071-federated-data-governance.md) establish contracts, vocabularies, provenance, interfaces, meaning, and decision authority. [DARCH-073](../ROADMAP.md) next develops classification architecture.

## Governing Question

Data policies govern access, collection, sharing, purpose, residency, quality, retention, deletion, schema, classification, disclosure, and derived use. Prose alone can be interpreted inconsistently and applied too late. Code can make selected decisions repeatable and observable, but it can also automate a mistaken interpretation at enormous scale.

The governing question is therefore not how to convert every policy sentence into a rule. It is how to choose executable decisions, preserve traceability to legitimate authority, define trustworthy inputs and complete outcomes, validate composition, distribute and activate versions safely, enforce at the real boundary, and detect when policy-as-code behavior diverges from intent or harms affected parties.

## Why This Matters

The [Open Policy Agent documentation](https://www.openpolicyagent.org/docs) describes a general-purpose engine that evaluates structured input against policies and data while separating policy decision-making from enforcement. This separation is architecturally useful, but it places a precise obligation on the caller: the enforcement point must supply correct context, interpret the result, perform obligations, and govern failure.

OPA's [Policy Language documentation](https://www.openpolicyagent.org/docs/policy-language) describes Rego as a declarative language for reasoning over structured documents such as JSON. Declarative rules can be reviewed and tested separately from application control flow. They still require an authorized policy model, stable schemas, bounded built-ins, and disciplined rule composition.

OPA's [Management APIs and Architecture](https://www.openpolicyagent.org/docs/management-introduction) describes distributed evaluators coordinated by bundle, decision-log, status, and discovery APIs. Co-located evaluation can improve latency and availability while a logical control plane distributes policy. It also creates version-skew, telemetry, revocation, and fleet-convergence problems that must be designed explicitly.

OPA [Bundles](https://www.openpolicyagent.org/docs/management-bundles) package policies and data, support namespace roots, signatures, snapshots, deltas, and eventual distribution. Signed atomic bundles protect integrity and coherent activation, but a valid signature establishes publisher and bytes—not source authority, semantic correctness, or safe enforcement.

OPA [Decision Logs](https://www.openpolicyagent.org/docs/management-decision-logs) can include decision identity, input, result, bundle revision, path, timestamp, trace context, metrics, and masks. This supports audit and debugging. Because policy input can reveal identity, purpose, health, employment, location, and protected data, collection, erasure, masking, access, retention, and deletion are themselves governed decisions.

The [Cedar Policy Language Reference Guide](https://docs.cedarpolicy.com/) describes authorization in terms of principal, action, resource, context, policies, entities, and schemas. Cedar separates application logic from authorization and supplies validation and analysis. Its scope illustrates a crucial boundary: an authorization engine can answer a well-formed request under supplied facts, but callers remain responsible for identity, data, enforcement, and the authorization model.

Cedar's [Policy Validation guidance](https://docs.cedarpolicy.com/policies/validation.html) explains validation against a schema before use and describes soundness for many evaluation errors when requests conform to that schema. Schema validation catches important type and reference mistakes. It does not prove that the schema models the correct policy, attributes are truthful, every request is checked, or obligations are fulfilled.

NIST [SP 800-162](https://csrc.nist.gov/pubs/sp/800/162/upd2/final) defines attribute-based access control as authorization based on subject, object, requested-operation, and sometimes environment attributes evaluated against policy, rules, or relationships. The guidance highlights both fine-grained sharing and the governance challenge of attribute definition, issuance, quality, trust, administration, and lifecycle.

NIST [SP 800-207, Zero Trust Architecture](https://csrc.nist.gov/pubs/sp/800/207/final) describes policy decision and enforcement concepts, continual evaluation, and resource-focused protection. Zero trust does not mean querying every remote fact synchronously or treating every request identically. It reinforces explicit signals, least privilege, dynamic decisions, enforcement, monitoring, and assumptions about component trust.

The OASIS [XACML 3.0 Core Specification](https://docs.oasis-open.org/xacml/3.0/xacml-3.0-core-spec-os-en.html) defines a policy language, request and response model, combining algorithms, obligations, advice, and architectural roles including administration, decision, information, and enforcement points. Its multi-valued results show why `allow = true or false` is often too weak for composed enterprise policy.

W3C [ODRL 2.2](https://www.w3.org/TR/odrl-model/) models policies over assets using permissions, prohibitions, duties, constraints, parties, actions, profiles, and conflict strategies. ODRL is useful for interoperable usage-policy expression. Its model does not by itself enforce duties or establish that a permission is lawful, current, applicable, or understood identically by two parties.

Together these sources establish practical languages, evaluation models, administration and enforcement boundaries, typed validation, distribution, evidence, attribute-based decisions, and interoperable usage expressions. They do not remove the need for legitimate interpretation, domain meaning, trustworthy facts, affected-party safeguards, and observed enforcement outcomes.

## Prerequisites and Retrieval

You should understand data governance, authorization, privacy, security, contracts, legal interpretation, data classification, purpose limitation, identity and access management, schemas, type systems, logic, testing, CI/CD, cryptographic signatures, APIs, events, distributed systems, caching, observability, incident response, audit, recovery, and lifecycle management.

Retrieve source policy, interpretation, authority, policy administration point, policy decision point, policy information point, policy enforcement point, principal, resource, action, purpose, context, environment, attribute, relationship, issuer, trust, freshness, permit, deny, not applicable, indeterminate, conflict, obligation, advice, combining algorithm, default, bundle, manifest, root, revision, signature, compilation, activation, rollout, decision evidence, shadow evaluation, differential test, mutation test, exception, emergency rule, time of check, time of use, continuing use, correction, and closure.

As a retrieval test, consider a rule that returns `permit` for an analyst reading a customer table for fraud detection. Ask who authorized fraud use; which person, service, and session the principal denotes; which table version and fields are covered; who asserted analyst role and fraud purpose; whether geography, consent, investigation, time, device, and sensitivity are current; which policies composed; which columns or rows must be masked; how export and derived features are controlled; whether every query path enforces the decision; what happens during policy outage; and which evidence proves obligations completed. The word `permit` preserves none of those answers.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish authoritative policy, interpretation, executable representation, evaluation, enforcement, evidence, and outcome;
2. define typed decision contracts with explicit identities, attributes, results, reasons, obligations, versions, and failure behavior;
3. allocate policy administration, decision, information, and enforcement responsibilities across a data architecture;
4. model access, purpose, classification, residency, quality, retention, deletion, and sharing decisions without unsafe Boolean collapse;
5. design policy repositories, schemas, tests, review, builds, signatures, bundles, rollout, rollback, and fleet convergence;
6. establish attribute authority, freshness, provenance, revocation, minimization, and reconciliation;
7. test rule logic, composition, defaults, conflicts, obligations, enforcement integration, and historical decisions;
8. operate decision telemetry, explanations, privacy, SLOs, incidents, exceptions, emergency modes, and correction;
9. evaluate embedded, sidecar, centralized, compiled, static, and runtime enforcement trade-offs; and
10. migrate and retire policy implementations without losing historical interpretation or reactivating obsolete rules.

## Core Exposition

**Start with an authoritative decision, not a language.** Name the decision to automate, policy source, issuing authority, interpretation owner, affected parties, protected resource, action, purpose, scope, risks, and appeal.

Do not begin by translating a PDF line by line. Many sentences establish goals, discretion, definitions, procedures, evidence, or human judgment rather than executable predicates.

**Separate source, interpretation, and implementation.** A source policy may be law, contract, standard, enterprise decision, domain rule, or risk acceptance. An interpretation record explains how it applies to a defined situation. Executable rules implement selected parts of that interpretation.

Trace all three with stable identifiers and versions. A source amendment does not become active code until impact, interpretation, testing, approval, and rollout occur.

**Define policy authority.** Repository write access, code review status, or platform administration does not establish authority to permit use, waive a right, set retention, or accept risk.

Every rule names its authoring and approving authorities, delegation, scope, effective interval, review date, and revocation path. Require independent concurrence when separation of duties applies.

**Model a decision contract.** Specify principal, resource, action, purpose, context, relevant relationships, required attributes, issuer trust, freshness, policy selection, possible results, reasons, obligations, advice, evidence, latency, and failure mode.

Version the contract separately from individual policies. Callers and evaluators must agree on input types and result semantics before a bundle can be considered compatible.

**Give all participants stable identity.** A username, table path, display label, role string, query text, or IP address is not necessarily stable identity. Resolve principal, service, workload, tenant, resource, field, product, policy, purpose, and decision through authorities and namespaces.

Avoid constructing identity from mutable labels inside policy. Renames, aliases, merged accounts, copied tables, and reused paths can silently change meaning.

**Type policy inputs.** Define entity types, field shapes, enumerations, optionality, units, time, code systems, hierarchy, and relationship direction. Validate policies against the schema and requests against their input contract.

A string called `country` can denote citizenship, residence, billing, storage, request origin, or legal establishment. Type names must carry the distinction that policy needs.

**Govern attributes as data products.** For each attribute, identify semantic definition, subject, issuer, collection method, evidence, confidence where applicable, valid time, observation time, expiry, revocation, classification, and permitted use.

Treat self-asserted purpose, copied role, stale group membership, inferred sensitivity, and cached location differently from authoritative, current facts. Policy correctness cannot exceed input correctness.

**Minimize policy input.** Send only attributes needed for the named decision. A general identity profile or full resource document can disclose far more than evaluation requires.

Use opaque stable identifiers and bounded attributes where possible. Protect input at rest, in transit, in memory, traces, errors, tests, and logs.

**Represent purpose explicitly.** Purpose is not reliably inferred from endpoint, team, dashboard, or role. Use a governed purpose identifier bound to requester, workflow, contract, policy, and time.

Prevent callers from selecting any purpose string that yields permit. High-consequence purposes require authoritative assignment or evidence and continuing-use controls.

**Choose result semantics deliberately.** Permit and deny are not enough when no policy applies, required data is missing, sources conflict, evaluation fails, or obligations cannot be executed.

Define `not_applicable`, `indeterminate`, and `conflict` as first-class outcomes where needed. The enforcement contract maps each to fail-closed, continuity, escalation, or another explicit behavior.

**Define defaults by consequence.** Deny-by-default protects many confidentiality decisions. It can also interrupt safety-critical or legally required access. Permit-by-default preserves availability but can expose protected data.

Design default behavior per action and consequence, with signed cached policy, bounded continuity rules, emergency authority, evidence, and review. Never let an engine error accidentally select the permissive branch.

**Model obligations separately from permission.** A decision may permit a query only with row filters, column masking, aggregation, watermarking, logging, notification, purpose binding, deletion, or review.

Return obligations as typed, versioned requirements. The enforcement point must support and acknowledge every mandatory obligation or treat the result as unusable.

**Treat advice as nonbinding.** Advice can recommend user messages, review, or optimization without determining authorization. Do not encode a mandatory privacy, security, or legal duty as optional advice.

Record which components consume advice and whether omission affects only experience or the protected outcome.

**Define rule composition.** Multiple policies can permit, deny, require duties, or not apply. Choose combining behavior by policy authority and scope: deny-overrides, permit-overrides, first-applicable, only-one-applicable, ordered priority, consensus, or explicit conflict.

Do not choose a universal algorithm for convenience. Retention and deletion, public interest and confidentiality, local and cross-border rules, and emergency access can require structured adjudication rather than precedence.

**Make policy selection explicit.** Select policies by stable resource, action, purpose, tenant, jurisdiction, profile, effective time, and authority. Avoid loading every rule and hoping nonapplicable conditions remain harmless.

Record the considered set as well as the applicable set. Missing a policy because discovery or metadata failed is not the same as a legitimate not-applicable result.

**Separate policy administration.** The administration capability stores sources, interpretations, schemas, rules, tests, approvals, bundles, rollout state, exceptions, and retirement.

Protect it with strong identity, separation of duties, branch and release controls, integrity, audit, backup, and emergency procedures. Unauthorized policy modification can be equivalent to unauthorized data access.

**Separate decision from enforcement.** A decision point evaluates. An enforcement point intercepts the real operation, supplies trusted input, interprets the result, applies obligations, prevents bypass, and reports outcome.

Putting a policy engine beside a service does not ensure every code path calls it. Inventory batch jobs, SQL consoles, caches, exports, replicas, files, notebooks, admin tools, and recovery paths.

**Place enforcement at the right granularity.** Dataset-level access may be insufficient when rules vary by row, column, cell, record state, subject, purpose, aggregation, or output.

Enforce as close as practical to the operation with enough context. If a storage system cannot express the obligation, mediate through a capable service or deny that use.

**Cover derived and continuing use.** A permitted read can produce a file, feature, model, report, cache, or external disclosure. Initial access policy does not automatically govern those new assets.

Propagate qualified policy and provenance, require derivative registration, bind purpose and retention, and re-evaluate when data, purpose, actor, location, or policy changes.

**Address time of check and time of use.** A permit can become stale between decision and execution because membership, consent, classification, legal hold, resource version, or emergency state changes.

Bind decisions to operation identity, resource version, policy and attribute versions, short validity, and nonce or transaction where needed. Recheck long-running or high-consequence operations.

**Prefer deterministic evaluation kernels.** Given identical policy, trusted data, input, engine, and time context, evaluation should be reproducible. Avoid arbitrary network calls and mutable clocks inside the kernel.

Fetch and validate external facts before evaluation or through governed, bounded providers. Represent evaluation time explicitly and record nondeterministic values when they cannot be eliminated.

**Design policy repositories for intent.** Group artifacts by stable policy domain and authority rather than deployment sequence. Keep source links, interpretation, schema, rules, fixtures, properties, and documentation adjacent where conventions permit.

Use code ownership to route review, not to substitute for approval authority. Protect generated and compiled artifacts from hand editing.

**Compile and validate before activation.** Parse, type-check, validate schemas and references, analyze unreachable or contradictory rules, enforce metadata, and build immutable artifacts.

Compilation success proves language conformance, not policy correctness. Preserve compiler, language, dependency, schema, and optimization versions for reproducibility.

**Use representative decision tables.** For every rule, enumerate permitted, denied, not-applicable, conflict, and indeterminate cases across boundaries. Include missing, empty, stale, duplicated, conflicting, malformed, and unauthorized attributes.

Derive expected outcomes from reviewed interpretation, not from current engine output. Otherwise a defective implementation becomes its own oracle.

**Add property and metamorphic tests.** Check invariants such as a broader untrusted role cannot increase access, expired consent cannot permit, adding unrelated attributes does not alter results, and stricter classification does not expand disclosure.

Properties are scoped; exceptions and policy changes can invalidate monotonic assumptions. State domains and preconditions precisely.

**Use mutation testing.** Delete a deny, invert an operator, change a boundary, remove an obligation, alter a combining algorithm, or stale an attribute. The test suite should fail.

Surviving policy mutations reveal weak decision coverage even when line or rule coverage is high.

**Test composition.** Evaluate policies individually and in their deployed set. Check precedence, duplicate rules, namespace collision, profile inheritance, obligations, conflict, and not-applicable behavior.

The most dangerous defect can emerge only when two locally correct policies combine.

**Test enforcement integration.** Prove the protected operation cannot proceed on deny, conflict, indeterminate, timeout, malformed result, unsupported obligation, stale bundle, or engine failure according to contract.

Test alternate endpoints, retries, caches, pagination, bulk operations, background work, exports, restore, and administrative paths. A correct decision unused is no control.

**Build immutable policy bundles.** A bundle includes policies, schemas, trusted reference data, manifest, namespace roots, dependencies, build provenance, digest, signature, authority, and compatibility metadata.

Sign after reproducible build. Verification proves integrity and trusted publisher under key policy; it does not prove semantic approval or safe content.

**Activate compatible state atomically.** Policies and referenced data must switch together. A new rule evaluated against an old classification map can invert decisions.

Stage, verify, load, validate, and atomically activate a complete revision. Preserve the last known acceptable bundle and make activation failure visible.

**Govern namespace ownership.** Multiple domains can contribute policy only within assigned roots or packages. Overlapping ownership and undefined load order create nondeterministic or failed state.

The control plane validates roots, dependencies, imports, and composition before release. Cross-domain rules use an explicit shared authority.

**Roll out with observation.** Promote through development, test, replay, shadow, canary, bounded production, and wider activation according to consequence.

Shadow evaluation compares proposed and active decisions without enforcing the proposal. It provides difference evidence, not proof that either decision is correct.

**Analyze decision differences.** Segment allow-to-deny, deny-to-allow, obligation changes, error changes, affected resources, principals, purposes, geographies, and high-consequence workflows.

Investigate expected and unexpected differences against policy interpretation and real outcomes. Aggregate counts alone can hide one catastrophic newly permitted path.

**Define fleet convergence.** Report evaluator identity, active bundle digest, schema and engine versions, last successful activation, health, and decision traffic. Set objectives for rollout and revocation.

Do not call deployment complete while active evaluators remain unknown or stale. Quarantine or route around incompatible instances where consequence requires it.

**Plan rollback and roll-forward.** Rollback restores a compatible bundle set and does not erase decisions already made. Schema or external state changes can make an old policy unsafe.

Prefer a corrected forward version when historical dependencies have moved. Test both paths with current and retained requests.

**Design decision evidence.** Record decision identity, request identity, principal and resource references, action, purpose, normalized input digest or bounded attributes, policy and data revisions, engine, result, reasons, obligations, enforcement receipt, and times.

Evidence must support investigation without becoming a high-risk copy of every input. Apply minimization, masking, separation, access, retention, deletion, integrity, and legal holds.

**Provide bounded explanations.** Explanations identify applicable rule and source, relevant facts, missing information, conflict, obligations, and challenge path without revealing protected attributes or exploitable policy internals.

Different audiences need different views: requester, operator, auditor, domain owner, affected person, and security responder.

**Observe evaluation and enforcement.** Measure decisions by outcome and reason, errors, latency, cache age, bundle convergence, attribute freshness, unsupported obligations, bypass attempts, shadow differences, exceptions, and enforcement acknowledgements.

Use explicit denominators and segment by policy, version, domain, action, purpose, resource class, and consequence. A low global denial rate is neither success nor failure by itself.

**Separate conformance and effectiveness.** A rule can validate, compile, pass tests, deploy, and return expected decisions while callers omit enforcement or users route around the control.

Measure protected-operation outcomes, sampled enforcement, unauthorized effects prevented, legitimate work blocked, appeals, incidents, and affected-party evidence.

**Treat policy performance as correctness.** Latency, availability, throughput, memory, and dependency behavior affect whether applications bypass, time out, retry, or use stale results.

Set objectives by action consequence. Test worst-case rules, adversarial inputs, cache behavior, thundering herds, and control-plane partitions.

**Cache decisions narrowly.** Cache only when key includes every decision-relevant input and version and validity ends before any required freshness boundary. Revocation and resource change must invalidate or outlive no unsafe entry.

Caching a permit by principal and resource while omitting purpose, action, context, policy, consent, or classification can disclose data.

**Design outage modes.** Options include fail closed, fail open, last known acceptable signed bundle, cached decision, degraded read-only mode, emergency rule, or manual authorization.

Choose per decision and document risks, duration, evidence, alerting, review, and exit. Test partitions between enforcement, evaluator, attribute providers, and control plane.

**Govern emergency policy.** Break-glass rules name authority, eligible actors, resources, actions, purpose, conditions, obligations, time limit, monitoring, notification, and retrospective review.

Store them separately, test them regularly, and prove automatic expiry. Emergency access must not become an undocumented permanent bypass.

**Model exceptions explicitly.** A waiver identifies source requirement, rule, scope, reason, risk, affected parties, compensating controls, approver, effective interval, monitoring, renewal limit, and closure.

Generate narrower executable policy where appropriate, but preserve the exception decision as authority. A comment or hard-coded identifier is not adequate evidence.

**Correct decisions without erasing history.** When a rule, source interpretation, schema, attribute, or enforcement point was wrong, issue a new version and preserve the original evaluation record.

Find affected actions through decision evidence and lineage, assess actual effects, revoke or remediate, notify, re-evaluate where meaningful, support appeal, and record closure.

**Protect the policy supply chain.** Threat-model source repositories, CI runners, dependencies, compilers, artifact stores, signing keys, distribution services, evaluator configuration, and decision telemetry.

Use reviewed changes, least privilege, isolated builds, dependency control, attestations, signatures, key rotation, verification, and incident response proportionate to policy consequence.

**Migrate policy languages semantically.** Inventory source interpretations, schemas, functions, combining algorithms, defaults, errors, obligations, data providers, decision contracts, integrations, tests, and retained decisions.

Translate representative and adversarial cases, run differential evaluation, explain every difference, canary enforcement, preserve rollback, and record unsupported semantics. Syntax conversion alone is not migration.

**Retire end to end.** Deprecate source interpretations and rules, publish replacements, migrate enforcement points and consumers, stop bundle distribution, revoke keys and credentials, expire caches and exceptions, and update recovery.

Retain policies, schemas, engines or reproducible evaluators, trusted data versions, decision evidence, interpretations, approvals, and correction records for required history. Prove restore cannot reactivate retired authority.

## Definitions and Notation

Let source policy `s = (authority, identifier, version, jurisdiction, scope, effective)`. Let interpretation `i = (s, question, findings, owner, evidence, decision, limitations, version, effective)`.

Let request `q = (principal, action, resource, purpose, context, relationships, time)`. Each identity resolves through a named authority and each attribute carries issuer, valid time, observation time, and trust.

Let executable policy `p = (i, schema, rules, data_dependencies, composition, result_contract, version)`. Code without an interpretation link is an untraced implementation assertion.

Let result `d` belong to `{permit, deny, not_applicable, conflict, indeterminate}` and carry `reasons`, `obligations`, `advice`, `policy_revision`, `data_revision`, and `valid_until` as required.

Let evaluation `Eval(p,q,a,t) -> d`, where `a` is authoritative attribute state and `t` explicit evaluation time. Reproducibility requires the same semantics, versions, inputs, and bounded nondeterminism.

Let enforcement receipt `e = (decision_id, operation_id, enforcement_point, obligations, status, resource_version, started, completed, effects)`. A decision without a conforming receipt does not prove enforcement.

Let bundle `b = (manifest, roots, policies, schemas, data, dependencies, build, digest, signature, revision, compatibility)`. Activation is an atomic transition from one verified compatible bundle state to another.

Let fleet state `G(t) = {active_revision(node,t)}`. Convergence to revision `v` is established only over the known eligible evaluator denominator, with excluded and unreachable nodes published.

Let policy coverage `Cov(S) = |{decision classes in S with reviewed positive, negative, boundary, missing, conflict, and failure cases}| / |S|`. Rule or line coverage is a different measure.

Let differential set `Delta(v_old,v_new,Q) = {q in Q : Eval(v_old,q) != Eval(v_new,q)}`. Equality over test population `Q` proves no behavior outside `Q`.

Let time-of-use predicate `Fresh(d,o,t)` require that decision `d` still covers operation `o`, relevant identities and versions match, obligations remain satisfiable, and `t` precedes expiry or required recheck.

Let correction set `Impact(d_bad)` contain actual operations and derived effects tied by decision and enforcement evidence, not merely every request that could theoretically have matched.

Let closure predicate `Closed(p_v)` require no active bundle, evaluator, cache, enforcement point, exception, emergency rule, consumer, or recovery path can use retired policy version `p_v`, while required historical reproduction remains controlled.

## Mechanisms, Invariants, or Proof Structure

Use the following gates to design and review policy as code for data.

**Authority gate.** Verify source, issuer, delegation, interpretation, owner, reviewer, scope, effective time, amendment, and appeal.

**Decision-contract gate.** Define principal, resource, action, purpose, context, relationships, outcomes, reasons, obligations, evidence, latency, and failure behavior.

**Identity gate.** Resolve stable principal, workload, tenant, resource, field, product, policy, purpose, decision, and enforcement identities.

**Attribute gate.** Check definition, type, issuer, collection, trust, valid time, observation time, expiry, revocation, sensitivity, and minimization.

**Rule gate.** Trace interpretation, conditions, defaults, boundaries, functions, nondeterminism, result, reasons, obligations, and limitations.

**Composition gate.** Select applicable policies, combining algorithms, authority precedence, conflicts, not-applicable behavior, and cross-domain ownership.

**Repository gate.** Protect source, review, separation of duties, schemas, tests, dependencies, build, provenance, and generated artifacts.

**Test gate.** Run syntax, types, decision tables, boundaries, missing input, properties, mutation, composition, differential, performance, and adversarial cases.

**Bundle gate.** Verify manifest, roots, policies, data, schemas, dependencies, reproducible build, digest, signature, revision, and compatibility.

**Rollout gate.** Exercise replay, shadow, difference analysis, canary, convergence, last-known state, rollback, and roll-forward.

**Enforcement gate.** Cover actual operation, granularity, bypass, obligations, time of use, continuing use, derived outputs, and receipt.

**Evidence gate.** Link request, bounded input, versions, result, explanation, obligations, enforcement, integrity, access, retention, and deletion.

**Operations gate.** Observe outcomes, reasons, latency, errors, freshness, convergence, unsupported obligations, bypass, appeals, incidents, and effectiveness.

**Continuity gate.** Define fail modes, cached authority, emergency rules, manual paths, duration, monitoring, review, and exit.

**Exception gate.** Record deviation, scope, reason, risk, affected parties, compensation, approval, expiry, monitoring, renewal, and closure.

**Correction gate.** Preserve history, identify actual effects, issue corrected policy, remediate, notify, support challenge, and verify repair.

**Closure gate.** Remove active rules, bundles, evaluators, caches, exceptions, enforcement paths, credentials, and recovery activation while retaining required interpretation.

### Executable evidence: multi-valued policy decisions and obligations

This Python example evaluates eight invented requests with four simple rules and counts decision outcomes and obligations.

<!-- bijux-verify: {"id":"multi-valued-policy-decisions-and-obligations","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"requests=8\ncomplete_inputs=6\npermit=3\ndeny=3\nindeterminate=2\npolicy_versions=2\npolicy_rules=4\nobligation_instances=5\nunique_obligations=3\nregions=2\npurposes=6\nresources=5\nhigh_consequence=3\n","stderr":""}} -->
```python
requests = [
    {"resource": "catalog", "classification": "public", "purpose": "analytics", "region": "eu"},
    {"resource": "cases", "classification": "confidential", "purpose": "support", "region": "us"},
    {"resource": "features", "classification": "restricted", "purpose": "fraud", "region": "us"},
    {"resource": "features", "classification": "restricted", "purpose": "marketing", "region": "us"},
    {"resource": "payments", "classification": "confidential", "purpose": "billing", "region": "eu", "export_to": "us"},
    {"resource": "profiles", "classification": "confidential", "purpose": "research", "region": "eu", "consent_required": True, "consent": False},
    {"resource": "cases", "classification": "confidential", "purpose": None, "region": "us"},
    {"resource": "profiles", "classification": None, "purpose": "analytics", "region": "eu"},
]

def evaluate(request):
    if request["classification"] is None or request["purpose"] is None:
        return "indeterminate", set()
    if request["classification"] == "restricted" and request["purpose"] != "fraud":
        return "deny", set()
    if request.get("export_to") not in {None, request["region"]}:
        return "deny", set()
    if request.get("consent_required") and not request.get("consent"):
        return "deny", set()
    obligations = {"audit"}
    if request["classification"] == "confidential":
        obligations.add("mask_direct_identifiers")
    if request["classification"] == "restricted":
        obligations.add("monitor_session")
    return "permit", obligations

decisions = [evaluate(request) for request in requests]
obligations = [item for _, required in decisions for item in required]

print(f"requests={len(requests)}")
print(f"complete_inputs={sum(r['classification'] is not None and r['purpose'] is not None for r in requests)}")
print(f"permit={sum(result == 'permit' for result, _ in decisions)}")
print(f"deny={sum(result == 'deny' for result, _ in decisions)}")
print(f"indeterminate={sum(result == 'indeterminate' for result, _ in decisions)}")
print("policy_versions=2")
print("policy_rules=4")
print(f"obligation_instances={len(obligations)}")
print(f"unique_obligations={len(set(obligations))}")
print(f"regions={len({r['region'] for r in requests})}")
print(f"purposes={len({r['purpose'] for r in requests if r['purpose'] is not None})}")
print(f"resources={len({r['resource'] for r in requests})}")
print(f"high_consequence={sum(r['classification'] == 'restricted' or 'export_to' in r for r in requests)}")
```

The expected output reports eight requests, six complete inputs, three permits, three denials, two indeterminate results, two policy versions, four rules, five obligation instances, three obligation types, two regions, six purposes, five resources, and three high-consequence requests on separate lines.

The evidence is intentionally narrow. Strings and dictionaries do not establish identity, attribute authority, source policy, interpretation, trusted time, resource version, or jurisdiction. Four imperative branches are not a production policy language or combining algorithm. `None` represents only two missing fields and no stale, conflicting, malformed, or untrusted input. Returned obligation names are not enforced or acknowledged. The code does not protect operations, derived data, logs, caches, exports, or continuing use. Production assurance requires authorized interpretations, typed contracts, validated policies, trusted attributes, composition tests, signed coherent bundles, enforcement integration, decision and obligation receipts, protected evidence, rollout and outage exercises, outcome monitoring, correction, and controlled retirement.

## Alternatives and Trade-Offs

**Prose-only policy.** Nuance and discretion remain visible to people. Interpretation and enforcement vary and evidence is difficult to aggregate.

**Policy as code.** Selected decisions become repeatable, testable, versioned, and observable. Mistaken interpretations can scale quickly and exclude necessary judgment.

**Policy embedded in applications.** Local context and performance are strong. Rules fragment, drift, and require application releases to change.

**External policy engine.** Decision logic and governance can be shared. Availability, latency, input contracts, versioning, and enforcement integration become explicit dependencies.

**Central evaluator.** Active policy can change consistently and evidence centralizes. Network latency, outage blast radius, capacity, and data disclosure increase.

**Sidecar or local evaluator.** Decisions are low-latency and resilient to network loss. Fleet convergence, revocation, telemetry, and evaluator lifecycle become harder.

**Embedded library.** In-process evaluation reduces hops and can use application types. Engine upgrades and bundle management couple to application builds.

**Compiled WebAssembly or native artifact.** Portable local execution can be fast. Supported language features, runtime consistency, debugging, and evidence need validation.

**Declarative rules.** Authors focus on desired decisions and composition can be analyzed. Debugging evaluation and understanding negation or set semantics require skill.

**Imperative rules.** Familiar control flow integrates easily. Side effects, hidden state, ordering, and incomplete analysis increase risk.

**Boolean result.** Callers integrate simply. Missing inputs, conflicts, not-applicable rules, obligations, and errors can be collapsed unsafely.

**Structured multi-valued result.** Uncertainty, reasons, duties, and versions remain explicit. Enforcement clients become more complex and must support the full contract.

**Deny-overrides.** Confidentiality risk is bounded when any applicable prohibition wins. Erroneous or overly broad denies can block legitimate or essential use.

**Permit-overrides.** Explicit exceptions and positive grants are easy to express. One broad permit can defeat protective rules.

**Ordered precedence.** Results are predictable and simple to explain. Ordering can conceal genuine authority or scope conflicts.

**Explicit conflict.** Disagreement remains visible for adjudication. Operations need bounded continuity and escalation.

**Static admission policy.** Infrastructure, schema, and configuration defects are blocked before activation. Runtime identity, purpose, data values, and continuing use remain unknown.

**Runtime policy.** Current request context supports fine-grained decisions. Latency, availability, bypass, and time-of-use risks grow.

**Source-generated rules.** Templates reduce authoring variation. Generation can hide semantics and create large opaque output.

**Handwritten rules.** Domain nuance and direct review improve. Repetition, inconsistency, and maintenance effort increase.

**Central policy data.** Attribute semantics and updates can be coordinated. A large mutable shared data document increases coupling and blast radius.

**Domain-owned policy data.** Authorities stay close to source. Trust, freshness, interfaces, and failure composition require federation.

**Snapshot bundles.** Coherent complete state and rollback are straightforward. Large bundles cost bandwidth and activation time.

**Delta bundles.** Frequent small changes are efficient. Ordering, base revision, loss, compaction, and recovery become more complex.

**Synchronous attribute lookup.** Decisions use fresh authoritative facts. Provider latency or failure enters every protected operation.

**Replicated attributes.** Evaluation is fast and resilient. Staleness, revocation, reconciliation, and disclosure must be bounded.

**Full decision logs.** Investigation and replay have rich context. Sensitive-data duplication, retention, insider access, and volume increase.

**Minimal decision evidence.** Privacy and cost improve. Reproduction, explanation, correction, and audit may become impossible.

**Shadow rollout.** Behavioral differences are visible without immediate effect. Historical traffic may omit rare or future cases and active policy may already be wrong.

**Immediate activation.** Urgent corrections move quickly. Unexpected broad changes and rollback risk increase.

**Long permit caching.** Latency and availability improve. Revocation, purpose, consent, classification, and policy changes can be ignored.

**Per-request evaluation.** Freshness and evidence improve. Cost, latency, and dependency load grow.

## Failure Modes and Misconceptions

**“Policy as code means all policy becomes code.”** Definitions, discretion, evidence, procedure, authority, and human judgment can remain outside executable predicates.

**“Code is the authoritative policy.”** Authority originates in governed sources and decisions unless explicitly established otherwise.

**“The repository owner is the policy owner.”** Technical administration and legitimate decision authority are distinct.

**“Code review is policy approval.”** Reviewers may lack delegation, legal context, risk authority, or affected-party perspective.

**“A readable rule is unambiguous.”** Input identity, types, defaults, time, composition, and enforcement can still differ.

**“Schema-valid means policy-correct.”** Validation catches structural errors, not mistaken intent or false attributes.

**“Authentication supplies authorization context.”** Identity proof does not establish action, resource, purpose, relationships, or policy.

**“Roles are sufficient attributes.”** Fine-grained decisions can require resource, purpose, environment, relationship, time, and risk.

**“Attributes are facts.”** They can be self-asserted, inferred, stale, conflicting, forged, or scoped differently.

**“Purpose follows from role.”** The same analyst can act for fraud, marketing, support, research, or curiosity.

**“Country is a single policy attribute.”** Citizenship, residence, storage, request origin, and legal establishment are distinct.

**“Missing means false.”** Missing, false, unknown, withheld, stale, and not applicable can require different behavior.

**“Every result should be Boolean.”** Conflict and indeterminate states should not silently become permit or deny.

**“Deny by default solves policy failure.”** Essential operations and rights can require governed continuity paths.

**“Permit by default preserves usability.”** It can disclose or process data without authority.

**“A permit is the end of enforcement.”** Filters, masking, logging, notification, retention, and continuing use can remain mandatory.

**“Obligations are optional hints.”** Mandatory duties must block or constrain the operation when unsupported.

**“Advice is an obligation.”** Mixing them makes enforcement inconsistent.

**“The strictest rule always wins.”** Deletion and preservation duties can conflict and require scoped interpretation.

**“Policy order expresses authority.”** File or load order is not a legitimate precedence decision.

**“No applicable policy means deny.”** That may be the enforcement mapping, but it is not the same policy result.

**“The engine discovers every policy.”** Selection can omit rules because identity, metadata, or distribution failed.

**“A policy engine is an enforcement point.”** It decides; another component must intercept and constrain the actual operation.

**“One gateway enforces all data use.”** Batch, direct SQL, caches, replicas, exports, notebooks, and restore paths can bypass it.

**“Dataset access controls every field.”** Row, column, record-state, purpose, and output obligations may differ.

**“A permitted read permits every derivative.”** Copies, features, reports, and models create new governed resources and uses.

**“A decision remains valid for the session.”** Consent, membership, classification, policy, and resource state can change.

**“External lookups make policy fresh.”** They also introduce nondeterminism, latency, failure, and disclosure.

**“Compilation proves correctness.”** It proves selected language and type properties under a toolchain.

**“Unit tests prove deployed behavior.”** Bundle assembly, policy composition, input mapping, and enforcement can still fail.

**“Line coverage proves policy coverage.”** Decisions need positive, negative, boundary, missing, conflict, and failure cases.

**“Current output is the test oracle.”** That makes existing defects appear correct.

**“Property tests need no scope.”** Policy exceptions and nonmonotonic rules can invalidate vague invariants.

**“Signed bundles are approved policies.”** Signatures prove integrity and key possession, not semantic authorization.

**“Policies and data may deploy independently.”** Version skew can reverse outcomes.

**“Eventual consistency is harmless.”** Mixed revisions can permit in one enforcement point and deny in another.

**“Deployment success means fleet convergence.”** Unknown, partitioned, or inactive evaluators can remain stale.

**“Shadow agreement proves correctness.”** Both active and proposed policies can share the same defect.

**“Few decision differences mean low risk.”** One newly permitted high-consequence path can dominate.

**“Rollback restores the past.”** External schemas, attributes, keys, and enforcement integrations may have changed.

**“Decision logs are ordinary telemetry.”** They can contain highly sensitive identity, purpose, resource, and policy data.

**“More logging always improves audit.”** Excess data increases disclosure and may still omit enforcement outcome.

**“An explanation should expose the whole trace.”** It can leak protected facts and enable policy probing.

**“Low policy latency proves success.”** A fast wrong or bypassed decision is not an effective control.

**“Permit cache keys can be simple.”** Omitted purpose, action, context, version, or attribute can authorize the wrong request.

**“Emergency policy can be added later.”** Untested break-glass paths fail or persist during real incidents.

**“An exception is a hard-coded allowlist.”** It needs authority, scope, risk, compensation, expiry, monitoring, and closure.

**“Changing the rule corrects prior decisions.”** Past uses and derived effects require impact analysis and remedy.

**“Syntax translation migrates policy.”** Languages can differ in defaults, composition, errors, types, functions, and obligations.

**“Deleting the source file retires policy.”** Bundles, caches, evaluators, exceptions, enforcement points, and backups can remain active.

## Worked Examples

### Example 1

A customer export rule traces to a contract, privacy interpretation, and domain approval. Its request schema distinguishes data-subject residence, storage region, destination, and requester location. A plain `country` string is rejected as indeterminate rather than guessed.

### Example 2

A policy permits support agents to read case records but returns obligations to mask payment tokens, limit rows to assigned cases, watermark bulk output, and log access. The query service supports three duties but not watermarking, so bulk export is denied while interactive access remains available.

### Example 3

A domain policy permits seven-day debugging retention while a legal hold requires preservation and a privacy policy requires deletion after purpose ends. The decision point returns conflict with applicable authorities. The enforcement point isolates the data and blocks unrelated use until an authorized record resolves scope.

### Example 4

A policy bundle contains rules, a Cedar-like entity schema, a purpose vocabulary, classification reference data, a manifest, build provenance, and a signature. Evaluation nodes verify, stage, test, and atomically activate it. Nodes on the old digest remain visible and cannot serve the newly regulated export path.

### Example 5

A proposed rule is shadowed against thirty days of requests. Most differences are expected new denials, but one allow-to-deny difference affects emergency treatment. Review finds the input omitted a governed continuity flag. The schema, rule, tests, and interpretation are corrected before canary enforcement.

### Example 6

A mutation test removes the `consent.active` requirement. Existing happy-path tests still pass, but a reviewed negative case now permits marketing use and fails the build. Another mutation removes a masking obligation and is caught by the enforcement integration suite.

### Example 7

A local evaluator loses the control plane. Public discovery continues with its unexpired signed bundle. Confidential export fails closed. An essential fraud stream uses a separately approved continuity bundle for fifteen minutes, emits decision and enforcement evidence, and alerts its accountable owner.

### Example 8

An analyst's group membership is valid for one hour, but a high-consequence query runs for four hours. The execution service binds its permit to policy, attribute, and snapshot versions, rechecks membership and legal-hold state at checkpoints, and terminates before writing a prohibited output.

### Example 9

Decision logs originally captured complete requests, including sensitive case descriptions. The evidence model is redesigned to retain stable references, selected decision attributes, input digest, policy and data revisions, result, reasons, obligations, and enforcement receipt. Restricted forensic access retrieves full context only from the authoritative case system when permitted.

### Example 10

An organization migrates from one policy language to another. It preserves typed request and response contracts, translates composition and missing-data behavior explicitly, replays retained decisions, tests adversarial fixtures, explains every differential result, canaries enforcement, and keeps the old evaluator isolated for historical reproduction until closure.

## Cross-Program Connections

**Programming Languages.** Syntax, types, name resolution, declarative semantics, evaluation order, totality, effects, compilation, optimization, and interpreters determine what policy code can safely express.

**Formal Methods.** Model checking, theorem proving, satisfiability, property tests, equivalence, counterexamples, and bounded analysis can challenge policy behavior while remaining scoped to the model.

**Security Engineering.** Authentication, authorization, least privilege, separation of duties, zero trust, key management, supply-chain integrity, threat modeling, and incident response underpin policy authority and enforcement.

**Privacy Engineering.** Purpose, consent, minimization, rights, retention, deletion, sensitive inference, evidence protection, and affected-party remedy require more than access control.

**API and Service Engineering.** Decision APIs need stable contracts, idempotency, concurrency, errors, versioning, latency, caching, availability, events, and protected observability.

**Platform Engineering.** Repositories, templates, schemas, test harnesses, builders, signing, bundle distribution, evaluators, decision telemetry, and paved enforcement paths form a policy platform.

**Data Engineering.** Pipelines, queries, schemas, lineage, quality, classifications, exports, retention, deletion, and derived products are both inputs to and targets of policy enforcement.

**Distributed Systems.** Replication, consistency, partitions, clocks, atomic activation, convergence, retries, caching, and recovery govern which policy actually decides at each node.

**Software Supply Chain.** Source review, dependency controls, reproducible builds, attestations, signatures, artifact stores, key rotation, and verification protect executable policy artifacts.

**Governance, Risk, and Compliance.** Authority, interpretation, controls, exceptions, evidence, assurance, residual risk, correction, and appeal establish why code may govern an action.

**Site Reliability Engineering.** Policy latency, availability, error budgets, fleet state, overload, degraded modes, rollback, incident command, and disaster recovery affect protected operations.

**Human-Computer Interaction.** Explanations, consent, denials, missing-information prompts, challenge paths, and operator workflows determine whether people can understand and correct policy decisions.

## References

1. Open Policy Agent, [“Open Policy Agent Documentation”](https://www.openpolicyagent.org/docs), retrieved 2026-09-03.
2. Open Policy Agent, [“Policy Language”](https://www.openpolicyagent.org/docs/policy-language), retrieved 2026-09-03.
3. Open Policy Agent, [“Management APIs and Architecture”](https://www.openpolicyagent.org/docs/management-introduction), retrieved 2026-09-03.
4. Open Policy Agent, [“Bundles”](https://www.openpolicyagent.org/docs/management-bundles), retrieved 2026-09-03.
5. Open Policy Agent, [“Decision Logs”](https://www.openpolicyagent.org/docs/management-decision-logs), retrieved 2026-09-03.
6. Cedar Policy, [“Cedar Policy Language Reference Guide”](https://docs.cedarpolicy.com/), retrieved 2026-09-03.
7. Cedar Policy, [“Policy Validation”](https://docs.cedarpolicy.com/policies/validation.html), retrieved 2026-09-03.
8. National Institute of Standards and Technology, [“SP 800-162: Guide to Attribute Based Access Control Definition and Considerations”](https://csrc.nist.gov/pubs/sp/800/162/upd2/final), 2019. Retrieved 2026-09-03.
9. National Institute of Standards and Technology, [“SP 800-207: Zero Trust Architecture”](https://csrc.nist.gov/pubs/sp/800/207/final), 2020. Retrieved 2026-09-03.
10. OASIS, [“eXtensible Access Control Markup Language Version 3.0 Plus Errata 01”](https://docs.oasis-open.org/xacml/3.0/xacml-3.0-core-spec-os-en.html), 2017. Retrieved 2026-09-03.
11. W3C, [“ODRL Information Model 2.2”](https://www.w3.org/TR/odrl-model/), 2018. Retrieved 2026-09-03.

## Exercises

### Exercise 1

Design policy as code for a data-export decision involving employees, contractors, services, confidential and restricted fields, purpose, geography, consent, legal holds, device trust, and emergency access. Specify authority, schemas, attributes, outcomes, obligations, evidence, enforcement, and appeal.

### Exercise 2

Design a policy repository and delivery pipeline for twelve domains and four thousand evaluators. Include source interpretation, ownership, testing, builds, signing, bundle roots, compatible data, rollout, convergence, rollback, telemetry, and compromise response.

### Exercise 3

Create an assurance strategy for retention and deletion policy that spans warehouse tables, object storage, streams, search indexes, caches, notebooks, model features, exports, backups, legal holds, and consumer copies.

### Exercise 4

A new policy bundle changes five percent of decisions in shadow mode. Design differential analysis, risk segmentation, review, canary, enforcement verification, SLOs, rollback or roll-forward, communication, and correction.

### Exercise 5

Migrate access, purpose, and masking rules from embedded application code and one legacy policy language to a shared policy platform. Preserve semantics, availability, historical decisions, exceptions, and retirement evidence.

## Answers to the Exercises

### Answer 1

Start from authorized source and interpretation records for confidentiality, employment, contracts, purpose, geography, consent, legal holds, and emergency duties. Define a request with stable principal or workload, resource and field-set version, export action, governed purpose, destination, environment, device, time, and operation identity. Schemas distinguish employee from contractor or service and distinguish subject residence, storage, requester, and destination regions. Each attribute has definition, issuer, valid time, freshness, trust, sensitivity, and revocation.

Return permit, deny, not applicable, conflict, or indeterminate with reasons, applicable versions, expiry, and typed obligations. Obligations can filter rows, mask direct identifiers, aggregate, watermark, encrypt, log, notify owners, bind destination and purpose, register the derivative, set retention, and prohibit onward transfer. Conflicting legal hold and deletion becomes explicit conflict. Missing purpose, unknown classification, stale device trust, or unsupported masking becomes indeterminate and maps to bounded enforcement behavior.

The export service is the enforcement point and writes only after all obligations are installed. It binds the decision to snapshot, policy, attribute, and destination versions and emits an enforcement receipt. Emergency access has narrower eligibility, short expiry, heightened logging, notification, and retrospective review. Evidence is minimized and protected. Denial explanations disclose safe reasons and challenge paths. Tests cover every role, class, purpose, region, missing attribute, conflict, expiry, bypass, output, retry, and outage case.

### Answer 2

Partition repositories and bundle roots by durable domain authority plus a shared namespace for cross-domain decisions. Every rule links to source, interpretation, decision contract, schema, owner, approver, scope, and effective time. Protect changes with least privilege, separation of duties, signed commits where required, reviewed dependencies, isolated builds, and generated-artifact controls.

Run parsing, types, schema validation, decision tables, missing and malformed input, property, mutation, composition, differential, performance, and enforcement-contract tests. Build policies, compatible reference data, schemas, manifest, roots, dependencies, provenance, digest, signature, engine compatibility, and expiry into immutable bundles. Use independent signing authority and rotation with dual-key transition.

Promote through replay, shadow, segmented difference review, canary, and fleet rollout. Each evaluator reports identity, engine, active digest, activation time, health, and traffic. Define convergence and revocation objectives over the known eligible denominator; route high-consequence traffic away from stale nodes. Keep a verified compatible last-known bundle, define rollback and roll-forward, and test control-plane partitions.

Collect minimized decision and enforcement evidence with revisions, reasons, obligations, latency, and errors. Alert on unknown nodes, signature failures, stale attributes, unsupported duties, unexpected differences, and bypass. On compromise, revoke signing and administration credentials, stop affected distribution, identify activated bundles and decisions, deploy a trusted corrected revision, reconcile effects, rotate keys, and validate that recovery media cannot restore compromised authority.

### Answer 3

Define retention and deletion by data class, purpose, subject, jurisdiction, record duty, source and derivative type, valid event, and time basis. Identify authoritative policy and the forum for conflicts such as legal hold versus erasure. Give every physical and logical resource stable identity and lineage across tables, objects, events, indexes, caches, notebooks, features, exports, backups, and consumer contracts.

Admission controls require classification, owner, schedule, legal-hold integration, derivative registration, and supported deletion before publication. Runtime policy decides new collection, copying, export, hold, and deletion initiation. Scheduled enforcement emits per-resource execution and failure evidence. Consumers acknowledge obligations and propagate qualified retention metadata; they do not merely copy an upstream date when their lawful or contractual role differs.

Test boundary dates, time zones, late events, absent creation time, conflicting holds, restored backups, immutable storage, partial deletion, replay, derived aggregates, model retraining, and departed consumers. Reconcile policy inventory, storage inventory, lineage, and execution receipts. Sample actual absence and blocked access after deletion, not just successful job status. Preserve minimal proof and required audit without retaining deleted content. Appeals and corrections identify affected uses and restore only under legitimate authority.

### Answer 4

Classify each difference as permit-to-deny, deny-to-permit, result-to-error, not-applicable or conflict change, obligation change, reason change, or expiry change. Segment by policy source, rule, resource class, field, principal type, purpose, geography, domain, consumer, volume, reversibility, affected population, and consequence. Inspect individual high-consequence changes even when counts are small.

Compare each change with the reviewed interpretation, expected decision table, source and attribute versions, and real enforcement behavior. Add fixtures for unexplained cases and mutation tests for missed boundaries. Obtain domain, privacy, security, legal, or risk approval according to authority. Canary low-consequence read paths first and separately canary denials and obligations; do not infer safety for exports from discovery traffic.

Monitor decision and enforcement outcomes, latency, errors, unsupported obligations, bypass, fleet digest, appeals, and operational impact. Set abort thresholds by class. Roll back only if the prior bundle remains compatible and safer; otherwise issue a corrected forward bundle. Preserve decisions already made, locate actual operations via receipts, revoke or remediate newly unsafe effects, notify affected owners or people as required, and document expected differences and closure.

### Answer 5

Inventory every embedded check, library, configuration, legacy rule, default, input mapping, attribute provider, combining behavior, error path, obligation, exception, caller, cache, batch job, export, administrative path, and retained decision. Establish canonical typed decision contracts and authoritative interpretations before translating syntax. Give purposes, resources, actions, classifications, and identities stable namespaces.

Wrap or instrument old enforcement to capture representative decisions without copying excessive sensitive input. Implement the shared rules and use differential replay across positive, negative, boundary, missing, conflict, and failure cases. Explain language differences in negation, missing data, hierarchy, types, functions, ordering, composition, and errors. Add enforcement integration tests proving callers honor structured outcomes and obligations.

Run old enforcement as authority while shadowing the new platform, then canary by reversible low-consequence paths. Preserve last-known compatible local bundles for bounded outages. Migrate exceptions into explicit scoped, expiring authority records. Move one enforcement boundary at a time, monitor decision and effect evidence, and retain rollback until current schemas and attributes make it unsafe.

Deprecate embedded and legacy paths, prevent new use, remove bypasses and duplicate checks, stop bundle or configuration distribution, expire caches, revoke credentials, update runbooks and recovery, and prove restore cannot reactivate old authority. Retain source interpretations, schemas, rules, evaluator versions or reproducible artifacts, reference data, approvals, and historical decision evidence for the required period.
