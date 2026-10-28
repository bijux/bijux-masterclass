---
module_id: PLAT-076
program: Platform Engineering
level: 2
module_number: 76
title: Platform Policy as Code
status: complete
last_verified: 2026-09-02
---

# Platform Policy as Code

## One-Page Review

### Governing question

How should a platform express, test, distribute, enforce, observe, change, exempt, and retire policy as governed software so that every protected path receives a reproducible decision without turning policy tooling into an unavailable or unaccountable control plane?

### Essential definitions

- **policy** is a rule or decision procedure that constrains actions and states according to organizational intent.
- **policy as code** represents executable policy, tests, metadata, data dependencies, and lifecycle in version-controlled, reviewable artifacts.
- A **policy decision point (PDP)** evaluates policy against input and policy data; a **policy enforcement point (PEP)** requests or obtains the decision and makes it effective.
- A **decision contract** defines input schema, output schema, entrypoint, semantics, errors, latency, freshness, and fail behavior between PDP and PEP.
- **policy data** is non-code information used during evaluation, such as approved registries, tenant tiers, risk classifications, or role bindings.
- A **bundle** is an atomic, versioned distribution unit containing policy, data, metadata, and optionally signatures.
- **audit/shadow mode** evaluates and records policy without blocking; **enforce mode** makes denial or mutation effective.
- **backtesting** evaluates a candidate policy against historical or current real inputs before promotion.
- An **exception** is a narrow, owned, justified, approved, time-bounded override represented and reviewed as policy data or code.
- **decision provenance** identifies policy/bundle version, data revision, engine/runtime version, entrypoint, input identity, result, and decision ID.
- **coverage of enforcement** means every route capable of the protected effect crosses an effective PEP, including controllers, break-glass paths, and direct APIs.
- **semantic compatibility** means a policy and its input/output/data schemas preserve the meaning expected by every consumer, not merely parse successfully.

### Central model, mechanism, or theorem

Represent a decision as

$$
D=P_v(e,I_s,X_r,C)=(result,reasons,obligations,metadata),
$$

where $P_v$ is policy bundle version $v$, $e$ is the named entrypoint, $I_s$ is input conforming to schema version $s$, $X_r$ is policy data revision $r$, and $C$ is bounded context. A PEP may enforce $D$ only when the decision contract, policy/data freshness, provenance, and local fail policy hold. The security property is end-to-end: policy correctness does not protect an action if a bypass path omits enforcement, transforms the input incorrectly, ignores the result, or evaluates a stale/unknown contract.

### Critical invariants

- Human-readable intent, machine decision, owner, scope, severity, rationale, and remediation remain traceable to one durable policy identifier.
- Policy inputs and outputs have versioned schemas; missing, unknown, malformed, or ambiguous values have explicit semantics.
- Deny-by-default or allow-by-default is chosen per decision contract and risk, never inherited accidentally from undefined evaluation.
- Tests include allowed, denied, boundary, missing-data, adversarial, error, and compatibility cases; no-test success is not accepted.
- Candidate policy is evaluated against representative fleet/historical inputs before blocking rollout, and observed violations have owners/remediation.
- Policy and data are promoted as immutable, attributable revisions; distributed engines report exactly which revision is active.
- Every protected effect has a coverage map proving all direct, indirect, asynchronous, privileged, and recovery paths cross a PEP.
- The PEP enforces the complete result and obligations; logging a denial without preventing the effect is audit, not enforcement.
- Exceptions are minimal in subject/resource/action/scope, owned, approved, visible, expiring, and automatically re-evaluated or removed.
- Runtime policy latency, availability, memory, and input size have budgets; expensive policy cannot silently become a platform outage.
- Stale policy/data, PDP timeout, engine error, and bundle failure use explicit risk-tier behavior with bounded last-known-good operation.
- Decision logs exclude secrets and unnecessary personal data while retaining version, reason, identity, and correlation needed to explain an outcome.

### Common failures

Policy text disconnected from executable rule; “policy repo” with no enforcement; one giant rule set; hidden defaults; undefined treated as allow; mutable external data fetched during evaluation; unversioned input; tests containing only happy paths; golden snapshots approved without semantic review; CI check skipped by direct API; audit results assumed historical; admission policy protecting creation but not controllers or updates; webhook outage set fail-open without risk decision; signed bundle whose source was unreviewed; bundle version active on only half the fleet; policy and data updated non-atomically; denial without stable reason; sensitive input dumped to decision logs; exception with no expiry; emergency bypass becoming normal path; policy author approving own privileged change; and rollback restoring a known-vulnerable policy.

### Compact example

Policy `PLAT.IMAGE.001` states that production workloads must use digest-pinned images from approved registries and carry an owner. Its decision contract consumes a normalized workload document and returns `allow`, stable reason codes, and remediation. Unit/property tests cover valid images, tag-only references, lookalike registries, missing owners, init/ephemeral containers, unknown schema, and malformed input. CI evaluates manifests; admission is the authoritative PEP; background audit finds pre-existing drift. A signed bundle with policy and registry data moves from test to shadow to canary enforcement, then fleet enforcement after latency and violation thresholds pass. A one-workload exception names owner, digest, reason, ticket, and expiry; an automated controller removes it and alerts before expiry.

### Connections

This module turns the decision/enforcement architecture from [PLAT-066](066-policy-decision-and-enforcement-points.md) into a governed software lifecycle. It consumes tenant, quota, human identity, and workload identity established by [PLAT-071](071-tenant-models.md), [PLAT-073](073-resource-quotas.md), [PLAT-074](074-identity-federation.md), and [PLAT-075](075-workload-identity.md). PLAT-077 applies it at admission; PLAT-078 applies it to supply-chain evidence; PLAT-079 makes decisions and exceptions auditable.

## Governing Question

How can a platform make policy changes reviewable and repeatable like software changes while preserving the legal, risk, operational, and human judgment that policy represents?

Encoding a rule is the smallest part. A production policy system needs authoritative intent, ownership, schemas, test evidence, distribution, enforcement coverage, staged activation, current data, failure behavior, observability, exception governance, rollback, and retirement.

The platform must also distinguish kinds of policy. Admission policy constrains desired state at an API boundary. Runtime authorization constrains each action. CI policy provides early feedback. Continuous audit detects existing drift. Mutation/defaulting changes objects. None is a complete substitute for the others.

## Why This Matters

Manual review and prose standards do not scale with self-service. Teams need immediate, consistent decisions at the interfaces where they create environments, deploy workloads, request privileges, publish artifacts, or cross tenant boundaries.

Centralizing every decision in one remote service can create latency and availability coupling. Copying policy into every service produces semantic drift. Policy as code allows logically centralized governance with distributed low-latency evaluation—provided revision and decision provenance remain observable.

Policy code is security-critical production software. A small predicate error can deny every deployment or admit a dangerous configuration everywhere. An overbroad exception can defeat stronger underlying rules. The delivery process therefore needs stricter evidence and safer rollout than ordinary formatting changes.

Policy is also a product interface. A denial without an actionable reason drives bypass attempts and support load. A rule that changes without notice breaks teams. Stable identifiers, documentation, previews, migration windows, and useful remediation are part of correctness.

## Prerequisites and Retrieval

Retrieve authorization models, principals, resources, actions, attributes, tenants, least privilege, default deny, schemas and API versioning, declarative programming, logic and set operations, pure functions, unit/property/differential testing, static analysis, fuzzing, CI/CD, signed artifacts, Git review, semantic versioning, Kubernetes admission and controllers, infrastructure as code, distributed caches, eventual consistency, clocks, observability, SLOs, incident response, and governance.

Distinguish policy intent from implementation; policy code from policy data; decision from enforcement; validation from mutation; admission from runtime authorization; CI feedback from authoritative enforcement; deny from error or undefined; warning from allowance; current-state audit from historical audit; syntactic from semantic compatibility; bundle activation from fleet convergence; rollback from restoration of unsafe state; exception from silent bypass; control-plane distribution from data-plane evaluation; and policy correctness from enforcement coverage.

## Learning Objectives

After completing this module, you should be able to:

1. translate policy intent into stable identifiers, decision contracts, schemas, rules, reasons, and remediation;
2. choose policy languages and enforcement modes by decision surface rather than tool fashion;
3. separate policy logic, policy data, platform normalization, and enforcement responsibility;
4. construct unit, boundary, adversarial, property, compatibility, performance, and backtest evidence;
5. package, sign, distribute, activate, observe, roll back, and retire immutable policy revisions;
6. prove enforcement coverage across CI, admission, controllers, APIs, runtime, and recovery paths;
7. stage changes through preview, audit/shadow, canary, and enforce modes with explicit promotion criteria;
8. govern exceptions and emergency bypasses without creating permanent invisible privilege;
9. define behavior for stale data, timeouts, engine errors, partial rollout, and control-plane outage; and
10. diagnose a decision from input, policy/data/engine versions, reasons, obligations, and PEP evidence.

## Core Exposition

### Begin with intent, authority, and a policy identifier

Before writing Rego, CEL, YAML, or application code, state the durable intent. Identify the risk owner authorized to define the requirement, the platform owner who implements it, affected teams, protected effect, scope, enforcement severity, and evidence for exceptions.

Assign a stable identifier such as `PLAT.NET.004`. The identifier survives wording, engine, and repository changes. It appears in documentation, code metadata, tests, denial reasons, exception records, dashboards, and incident reports.

Write a concise normative statement and rationale. Define allowed and denied states, exemptions, remediation, rollout, and retirement. Avoid embedding organizational folklore only in code comments or ticket history.

Trace high-level control to one or more executable rules. A broad requirement like “production data is isolated” needs separate decisions for tenant identity, storage, network access, encryption, backup, and privileged operations; one ambiguous predicate cannot prove it.

### Define the decision contract

A policy engine evaluates structured input and data at a named entrypoint. Document exact input schema, output schema, types, required fields, normalization, defaults, error values, maximum size, latency, policy/data freshness, and enforcement meaning.

Return more than a Boolean when operators and users need explanation. A decision can include `allow`, stable reason codes, human messages, severity, remediation link, obligations, and provenance. Keep reason codes stable even when prose improves.

Distinguish `deny`, `not_applicable`, `unknown`, `error`, and `timeout`. Collapsing all non-true states into either allow or deny by language accident produces unsafe or disruptive behavior.

Version schemas independently from policy bundles. Reject incompatible input at the PEP or adapter. If old and new consumers coexist, publish compatibility tests and explicit deprecation windows.

### Normalize inputs at an owned boundary

Raw provider and Kubernetes objects change shape across versions. A policy adapter can translate them into a stable platform decision document with canonical principal, tenant, action, resource, environment, provenance, and requested state.

Normalization is security-sensitive. Preserve distinctions such as omitted versus empty, user request versus controller mutation, image tag versus digest, human actor versus workload identity, and original versus defaulted fields.

Validate schema before evaluation. Bound nested collections and strings to prevent expensive evaluation. Reject duplicate, ambiguous, or lossy encodings.

Keep transformation logic testable and versioned. If CI and admission normalize differently, identical manifests can receive different decisions even with the same policy code.

### Separate policy code from policy data

Policy code expresses durable reasoning. Policy data supplies changeable facts: approved registries, tenant classifications, vulnerability thresholds, geographic constraints, business hours, or role assignments.

Give policy data a schema, authority, owner, revision, freshness, and lifecycle. A spreadsheet downloaded at evaluation time is not governed data. Prefer validated snapshots or bounded, authenticated services with explicit failure semantics.

Package code and the data required for a reproducible decision together or record exact independent revisions. Atomic activation avoids a new rule observing an old data shape.

Minimize runtime dependencies. Each network lookup during evaluation expands latency, outage, and time-of-check/time-of-use risk. Replicate compact data to local PDPs when staleness can be bounded; use online lookup only when currency outweighs that cost.

### Choose a language and engine by the contract

Open Policy Agent is a general-purpose engine. Rego reasons declaratively over structured input and data; OPA can run alongside services, in a host process, or behind an API and can consume bundles and emit decision/status telemetry.

Kubernetes ValidatingAdmissionPolicy evaluates CEL expressions in the API server. It reduces external webhook dependency for compatible validations but addresses Kubernetes admission, not every platform policy surface.

Gatekeeper uses constraint templates and constraints, supports admission and audit, and can support shift-left evaluation. Kyverno supplies Kubernetes-oriented validate, mutate, generate, cleanup, and image-verification policy types and reporting. Capabilities and versions evolve; choose the narrowest maintained mechanism whose semantics match the contract.

Application-native authorization can understand rich domain objects and transactions. Infrastructure engines standardize cross-cutting controls. A platform may use several engines while maintaining common identifiers, inputs, results, lifecycle, and evidence.

### Keep validation, mutation, generation, and authorization distinct

Validation accepts or denies an object or request. Mutation changes it. Generation creates related resources. Authorization permits a principal to perform an action. Audit evaluates existing state. Each has different idempotency, ordering, side-effect, and failure concerns.

Prefer explicit defaults close to the API schema and transparent templates over surprising mutation. Users should be able to preview the effective object. Mutating webhooks or policies can interact in order-dependent ways and must be idempotent.

Do not use admission validation as runtime authorization. A valid deployment may later make unauthorized tenant requests. Conversely, runtime checks cannot prevent a privileged or dangerous pod configuration from entering the cluster.

If a policy returns obligations—add label, obtain approval, encrypt field, restrict route—define which component performs and verifies them. An ignored obligation is not enforcement.

### Design safe defaults and total decisions

For security authorization, default deny is normally appropriate: only positively established allowed cases proceed. For advisory lint, an unknown check may warn. Availability controls can have different fail behavior based on risk.

Make the entrypoint total over its declared schema: every valid input returns one recognized decision. Explicitly handle empty sets, unknown enum values, new API versions, missing optional data, and not-applicable resources.

Avoid negative-only rules that assume an exhaustive forbidden list. An allowlist may be safer for high-risk actions, but it needs governed updates and usable errors. For complex policy, combine baseline denials with explicit capabilities.

Test undefined behavior in the chosen language. A rule that does not produce a value is not automatically equivalent to a deliberate denial unless the decision contract and PEP make it so.

### Build a layered test portfolio

Unit tests cover each rule with allowed and denied examples. Boundary tests exercise equality, just-above/below thresholds, empty/missing values, maximum sizes, Unicode/case normalization, and clock edges.

Adversarial tests use lookalike registries, path traversal, duplicated fields, wildcard subjects, nested containers, controller-generated objects, stale data, and attempts to exploit exceptions. Property tests assert invariants across generated inputs, such as “untrusted registry is never allowed in production.”

Compatibility tests run old/new schema consumers and data revisions. Differential tests compare candidate versus current policy and investigate every changed decision. Golden snapshots help detect broad change but cannot replace reviewing whether the new result is correct.

Performance tests measure p50/p95/p99 latency, memory, compilation/activation, and worst-case inputs under concurrency. Ensure the test command fails when no tests execute and record tool/engine versions.

### Backtest against realistic inputs

Before enforcement, evaluate candidate policy against current fleet state, recent admission requests, representative API traces, or sanitized production-shaped fixtures. Backtesting identifies existing violations, hidden object variants, and unexpected decision changes.

Protect privacy and secrets in captured inputs. Normalize and minimize them. Record the sampling window, coverage, exclusions, data revision, and result counts.

Classify violations: genuine defect, policy bug, input adapter bug, legitimate exception, legacy debt, or unknown. Assign remediation owner and deadline. Do not turn on enforcement while known business-critical violations have no safe path.

Backtesting is evidence, not proof of future correctness. Pair it with constructed edge and adversarial cases and runtime shadow observation.

### Treat policy repositories as production systems

Use CODEOWNERS or equivalent review ownership, protected branches, required tests, signed/attributable changes, dependency scanning, reproducible builds, and separation of duties for privileged policy.

Policy authors should not unilaterally approve rules that grant them access. Require risk/domain approval for intent and platform approval for operational safety. Emergency change has explicit narrow authority and retrospective review.

Organize by decision domain and ownership, not a single undifferentiated directory. Share libraries carefully: a low-level helper change can alter hundreds of rules. Pin and test dependencies.

Generate documentation from policy metadata only when metadata is authoritative and human-reviewed. Do not let generated prose disguise missing rationale or stakeholder communication.

### Package immutable, verifiable bundles

A bundle includes compiled/source policy, required data, manifest, schema metadata, version/revision, dependency/runtime constraints, and integrity/provenance. OPA bundles can be signed; engines should activate only after validation and signature verification when configured.

Build once and promote the same digest through environments. Rebuilding from the same branch later may incorporate different dependencies or data. Record source commit, builder, tests, artifact digest, signer, and approval.

Activation is atomic per engine: a failed new bundle leaves last-known-good active. Multiple independently owned bundle roots need non-overlap and compatibility; otherwise loading order or conflicts can cause errors.

Protect bootstrap verification keys out of band. If the same untrusted discovery document supplies the keys that authorize itself, signature checking is circular.

### Distribute policy with convergence visibility

Logically centralized management can distribute bundles to local PDPs for low latency and availability. Each instance reports active revision, last successful download and activation, failure, engine version, labels/environment, and health.

Define propagation SLO and maximum allowed staleness. A policy is not “deployed” when published; it is deployed when the required fleet fraction has activated it and stragglers are handled.

Use canary rings and monotonic promotion criteria. Stop on activation error, denial spike, latency regression, unknown decision, or incompatible consumer. Do not let automatic rollback restore a version known to admit an exploited path; roll forward to a safe revision when required.

For urgent deny policy, pre-plan faster distribution and compensating enforcement at gateways or identity/role systems. Measure actual worst-case convergence through drills.

### Map and prove enforcement coverage

List the protected effect and every path that can cause it: portal, public/internal API, CLI, GitOps controller, operator/controller, direct cloud API, Kubernetes API, batch workflow, administrator, break-glass, restore, and asynchronous retry.

For each path identify PEP, entrypoint, normalized input version, decision source, enforcement behavior, failure mode, policy freshness, and evidence. A CI check is useful feedback but not authoritative if direct submission can bypass it.

Controllers require special analysis. Admission sees the controller identity and generated object; policy may need trustworthy provenance about the initiating resource or user. Audit mode may lack request-time identity fields.

Test bypass empirically. Attempt the effect through every documented and discovered route, including old API versions, subresources, update/patch/delete, dry-run, restore, and privileged maintenance paths.

### Stage audit, canary, and enforcement

Begin with local/CI feedback so developers can repair before submission. Deploy candidate in shadow/audit mode to observe real decisions without blocking. Compare it to current enforced revision.

Define promotion thresholds: test and backtest pass; no unexplained decision diff; violation inventory owned; evaluation error below limit; latency within budget; all required PEPs reporting candidate; documentation and exceptions ready.

Canary enforce on low-risk tenants/clusters or a representative ring with rapid rollback/forward. Watch user impact and bypass—not only engine health. Then expand in controlled steps.

Audit is not enforcement. Reports often represent current resources and may omit denied requests or request-only identity fields. Export events if historical evidence is required.

### Govern exceptions as first-class artifacts

An exception states policy ID/version range, exact subjects/resources/actions, environment/tenant, reason, risk, compensating controls, owner, approver, creation, expiry, renewal limit, and evidence/ticket.

Default expiry should be short relative to risk. Alert owner and approver before expiry; remove automatically unless renewed through the same review. Test that expired, widened, malformed, or orphaned exceptions deny.

Keep exception logic centralized and compositional. Scattered `if team == ...` branches are invisible privilege. A broad exception must not suppress unrelated policies.

Dashboards show exception count, age, scope, upcoming expiry, renewals, and usage. An unused exception can be removed; a heavily used one may reveal impractical policy or unresolved debt.

### Define error, timeout, and stale behavior

For each entrypoint decide what happens when input is invalid, policy is undefined, PDP times out, bundle activation fails, data is stale, logging is unavailable, or the remote control plane is unreachable.

High-impact authorization normally fails closed. Lower-risk availability paths may use a bounded last-known-good decision or local bundle. Never fail open merely because all engine failures are represented as “falsey” or because a webhook default was copied.

Budget evaluation time below caller timeout and cancellation. Use local evaluation for hot paths, precompute indexes/data, constrain input, and load-test adversarial cases. Circuit breakers must not bypass security; they may shed the protected operation.

Logging failure should not usually stop all decisions, but buffer/drop behavior, privacy, and audit requirements must be explicit. Surface telemetry loss as a control degradation.

### Make decisions explainable and observable

For each evaluation record decision ID, timestamp, entrypoint, result, stable reasons, policy/bundle and data revisions, engine version, PEP identity, normalized input fingerprint or safe fields, latency, and enforcement outcome.

OPA decision logs can include query input and bundle metadata; apply masking before export. Secrets, bearer tokens, personal data, and large object bodies should not be logged by default.

Separate decision from enforcement evidence. A PDP may return deny while a buggy PEP proceeds. Correlate decision ID with API/admission/audit outcome and downstream effect.

Metrics include decisions by result/reason/policy, undefined/error/timeout, p95/p99 evaluation, activation failures, revision lag, stale data, audit violations, bypass probes, exception use/expiry, and user remediation success.

### Change and retire policy safely

Classify changes as tightening, loosening, refactoring with intended equivalence, schema change, data change, or engine/runtime change. Required approvals and rollout differ.

For equivalence refactors, differential tests should show no decision changes across corpus and generated properties. For tightening, inventory new denials and provide migration. For loosening, require explicit risk authority and prove scope does not expand unintentionally.

Rollback reactivates a known immutable bundle only when it is still safe and compatible. Preserve incident block rules and revoked exceptions. Record why rollback occurred and which revisions were active.

Retirement removes rule, documentation, tests only after consumers, exceptions, dashboards, data, and enforcement mappings are gone or migrated. Keep durable audit/provenance so old decisions remain explainable.

## Definitions and Notation

Let policy identifiers be $K$, bundle versions be $V$, input schema versions be $S$, data revisions be $R$, entrypoints be $E$, and enforcement points be $F$.

A reproducible decision is

$$
D=P_v(e,I_s,X_r,C)=(q,\rho,O,m),
$$

where $q\in\{allow,deny,not\_applicable,unknown,error\}$, $\rho$ is a set of stable reasons, $O$ is a set of obligations, and $m$ contains safe provenance.

For protected effect $z$, let $Paths(z)$ be all paths capable of causing it and $pep(p)$ the effective enforcement point for path $p$. Coverage is

$$
Covered(z)\iff \forall p\in Paths(z),\ \exists f\in F:\ pep(p)=f\land Effective(f,P_v,z).
$$

Let $a_f$ be the active bundle revision at PEP/PDP instance $f$, $v$ the target, and $t_0$ publication time. Convergence at time $t$ is

$$
G_v(t)=\frac{|\{f\in F_{required}:a_f(t)=v\}|}{|F_{required}|}.
$$

Promotion may require $G_v(t)=1$ for critical PEPs and a lower documented threshold for temporarily unavailable non-critical instances, with a maximum propagation interval $t-t_0\le L$.

For exception $x$ define

$$
x=(k,subjects,resources,actions,scope,owner,approver,t_c,t_e,controls).
$$

It applies only if request dimensions are subsets/matches of its explicit scope and current time is before expiry $t_e$. Absence, ambiguity, or expiry does not match.

## Mechanisms, Invariants, or Proof Structure

### Policy delivery and enforcement mechanism

1. Establish authoritative intent, durable policy ID, owner, protected effect, scope, severity, rationale, and remediation.
2. Define entrypoint and versioned input/output schemas, decision states, obligations, latency/freshness, and fail behavior.
3. Implement normalized input adapter, policy logic, governed data, metadata, and narrow exception model.
4. Run syntax/type/static checks plus allow, deny, boundary, missing-data, adversarial, property, compatibility, and performance tests.
5. Differential-test and backtest candidate against representative current/historical inputs; classify every material change.
6. Build one immutable bundle with exact policy/data/dependency revisions, provenance, digest, approval, and signature.
7. Deploy to local/CI preview and runtime audit/shadow; observe result, error, latency, and violation ownership.
8. Verify enforcement coverage for every effect path, PEP contract, bypass, subresource, controller, direct API, and recovery path.
9. Canary enforce under explicit promotion/stop/rollback-or-forward criteria, then expand while measuring fleet convergence.
10. Enforce the full decision and obligations; correlate decision and outcome while masking sensitive inputs.
11. Reconcile stale instances, policy data, violations, and exceptions; remove expired or orphaned artifacts automatically.
12. Exercise outage, compromise, rollback, migration, engine upgrade, and retirement while keeping historical decisions explainable.

### Intent invariant

Every executable rule and exception traces to an authorized, durable policy statement and owner. Generated code or tool configuration cannot silently become organizational policy.

### Decision invariant

For every schema-valid input, the entrypoint returns exactly one recognized result with versioned semantics; unknown, error, and timeout cannot be mistaken for deliberate allow.

### Distribution invariant

An engine activates only a validated, attributable, compatible bundle and reports its active revision. Partial convergence remains visible and blocks promotion where critical coverage requires unanimity.

### Enforcement invariant

Every path to a protected effect crosses a PEP that supplies contract-valid input and makes the current policy decision and obligations effective. Preview, logging, and audit do not satisfy this invariant.

### Exception invariant

Every override is narrower than the governed policy surface, attributable to owner and approver, bounded by expiry and compensating controls, visible in decisions, and non-matching when malformed or stale.

### Proof sketch: pre-merge policy cannot enforce a bypassable effect

Suppose all manifests submitted through repository pipeline $p_1$ pass policy check $P$, but an operator or controller can create the same protected resource through direct API path $p_2$. If $p_2$ has no equivalent authoritative PEP, choose a manifest $m$ denied by $P$ and submit it through $p_2$. The protected effect occurs despite perfect correctness and availability of the pre-merge check.

Therefore policy correctness on $p_1$ cannot establish the system property unless every path in $Paths(z)$ is covered by effective enforcement. CI remains valuable for feedback and evidence, but an admission or resource-native enforcement point must cover direct effects. This is a coverage argument under the assumed path inventory; discovering new paths expands the proof obligation.

### Executable policy audit

This synthetic evaluator classifies nine production workload requests using schema, environment, owner, digest pinning, registry, and exception-expiry checks. It demonstrates total result ordering only; it is not an admission controller or a substitute for policy-engine conformance tests.

<!-- bijux-verify: {"id":"platform-policy-audit","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"allowed=4\nschema=1\nowner=1\ndigest=1\nregistry=1\nexception=1\n"}} -->
```python
requests = [
    (1, "team-a", True, "registry.example", True),
    (1, "team-b", True, "registry.example", True),
    (1, "team-c", True, "registry.example", True),
    (1, "team-d", True, "registry.example", True),
    (2, "team-a", True, "registry.example", True),
    (1, "", True, "registry.example", True),
    (1, "team-a", False, "registry.example", True),
    (1, "team-a", True, "lookalike.example", True),
    (1, "team-a", True, "registry.example", False),
]

counts = {name: 0 for name in ("allowed", "schema", "owner", "digest", "registry", "exception")}
for schema, owner, pinned, registry, exception_valid in requests:
    if schema != 1:
        counts["schema"] += 1
    elif not owner:
        counts["owner"] += 1
    elif not pinned:
        counts["digest"] += 1
    elif registry != "registry.example":
        counts["registry"] += 1
    elif not exception_valid:
        counts["exception"] += 1
    else:
        counts["allowed"] += 1

for name, count in counts.items():
    print(f"{name}={count}")
```

### Verification strategy

Validate policy and data schemas, type/static checks, metadata completeness, dependency pins, bundle contents, digest/signature, and engine compatibility. Ensure test discovery fails on empty suites.

Exercise allowed, denied, not-applicable, unknown, error, timeout, missing/extra/oversized inputs, adversarial encodings, policy-data staleness, exception edges, and deterministic reason codes.

Backtest and differential-test current versus candidate on normalized representative inputs. Benchmark worst-case policies and load PDP/PEP concurrency.

Inject bundle/control-plane/logging/data/PDP outage, corrupt signature, partial activation, slow evaluation, engine upgrade, rollback, expired exception, and direct bypass. Correlate policy decision with the real effect.

## Alternatives and Trade-Offs

- **Prose/manual review versus executable policy.** Prose conveys nuance; executable policy supplies repeatability. Keep traceability and reserve judgment where automation is inappropriate.
- **Central remote PDP versus distributed local PDP.** Central service improves currency/control; local evaluation reduces latency/outage coupling but requires versioned distribution and staleness management.
- **General-purpose engine versus domain-native policy.** General engines unify lifecycle; native mechanisms expose precise domain semantics and fewer adapters.
- **Rego versus CEL versus Kubernetes-oriented YAML/CEL policy.** Rego supports rich structured decisions; CEL is embedded and bounded in several APIs; Kubernetes-oriented systems improve resource ergonomics. Choose by contract and operations.
- **Validation versus mutation.** Validation is explicit and explainable; mutation can supply defaults but creates ordering and surprise. Preview effective objects.
- **Admission versus runtime enforcement.** Admission blocks unsafe desired state; runtime controls actions and changing context. Use both when the threat spans both.
- **CI versus authoritative PEP.** CI gives fast feedback and review evidence; only non-bypassable runtime/admission enforcement protects direct paths.
- **Policy code versus external policy data.** Code suits durable logic; data suits changing facts. Both need authority, schema, revision, and tests.
- **Snapshot versus online lookup.** Snapshot evaluation is reproducible and available; lookup can be fresher but adds latency and failure/time-of-check concerns.
- **Single bundle versus multiple roots.** Single atomic bundle simplifies compatibility; multiple ownership domains scale teams but require non-overlap and dependency contracts.
- **Boolean versus structured decision.** Boolean is simple; structured reasons/obligations/provenance improve explanation and downstream enforcement while expanding schema.
- **Default deny versus default allow.** Deny minimizes unauthorized action; allow favors availability/advisory use. Choose explicitly per risk and handle unknown separately.
- **Audit versus immediate enforce.** Audit discovers impact safely; enforcement protects now. A staged path needs deadlines so shadow mode does not become permanent.
- **Fleet-wide versus canary activation.** Fleet-wide closes inconsistency quickly; canary limits blast radius but temporarily produces revision diversity.
- **Automatic rollback versus controlled roll-forward.** Rollback restores service quickly; it may restore unsafe policy. Preserve security incident constraints.
- **Embedded exceptions versus separate exception data.** Embedded branches are easy to code; governed exception records improve visibility, expiry, and review.
- **Golden tests versus semantic properties.** Goldens catch broad diffs; properties express durable invariants. Use both and review changed outputs.
- **Verbose decision logs versus minimization.** Rich inputs aid debugging; they leak secrets/personal data and cost storage. Record safe provenance and masked fields.
- **Shared helper libraries versus duplicated small rules.** Libraries reduce repetition; changes amplify blast radius. Version, pin, and test dependents.
- **One policy repository versus federated ownership.** One repo improves discovery/control; federated domain repos improve ownership. A common delivery contract can govern both.

## Failure Modes and Misconceptions

- “Policy as code means writing rules in YAML” omits authority, tests, delivery, and enforcement.
- “A policy repository is an enforcement point” confuses source with effect.
- “If CI passes, direct APIs are safe” ignores bypass paths.
- “Admission protects runtime operations” covers desired state only.
- “Audit mode blocks violations” records rather than prevents.
- “A current policy report is historical evidence” may contain only current state.
- “A valid signature proves good policy” proves approved artifact origin/integrity, not semantics.
- “Compilation success proves correctness” omits decision and coverage tests.
- “One happy-path unit test is sufficient” misses denials and boundaries.
- “Undefined is the same as explicit deny” depends on language and PEP contract.
- “All failures should fail open for availability” converts control outage into privilege.
- “All failures should fail closed everywhere” can create unsafe platform outage without risk-tier design.
- “External data is always current” ignores source, cache, clocks, and synchronization.
- “Policy and data can roll independently” can break schemas and semantics.
- “Bundle published means bundle deployed” ignores activation and fleet convergence.
- “Latest is a sufficient version” prevents reproduction and rollback analysis.
- “Mutation is harmless defaulting” can change ownership, security, and later validation.
- “The engine sees the original user everywhere” controllers and audit may change or omit identity.
- “A denial message can include the full input” risks secrets and personal data.
- “Decision logging proves enforcement” a PEP may ignore or misapply the result.
- “A broad team exception is temporary” scope tends to expand and persist without expiry.
- “Ticket closure removes the override” needs automated policy reconciliation.
- “Policy authors can approve their own access” violates separation of duties.
- “Rollback is always safe” may restore a known vulnerability or revoked exception.
- “A language migration is only syntax” evaluation, undefined, ordering, and numeric semantics may change.
- “Retiring the rule means deleting its file” leaves consumers, exceptions, data, docs, and unexplained historical decisions.

## Worked Examples

### Example 1

An image policy consumes canonical fields for environment, all container kinds, registry host, digest, owner, and provenance. It denies tag-only production images and lookalike `registry.example.attacker` while allowing an exact approved host and digest.

Stable reasons `IMAGE_DIGEST_REQUIRED` and `REGISTRY_NOT_APPROVED` let CI, admission, docs, and metrics agree.

### Example 2

The current rule treats missing `tenant_class` as undefined. One PEP interprets undefined as allow and another as deny. The team versions the output contract, makes result total, and adds missing/unknown class tests.

Consumers refuse the incompatible schema until upgraded, preventing silent divergent enforcement.

### Example 3

Candidate quota policy denies 1,800 existing workloads. Backtesting classifies 1,720 as legacy debt, 60 as adapter errors involving absent defaults, and 20 as valid exceptions.

The team fixes normalization, creates bounded debt remediation, encodes 20 expiring exceptions, reruns the corpus, then starts canary enforcement.

### Example 4

OPA instances download signed bundle digest `sha256:abc` with revision `2026-09-02.4`. Status reports show 98 of 100 active; two clusters have an incompatible built-in.

Promotion stops because critical convergence requires all clusters. Engine compatibility test and upgrade precede reactivation; publication alone was not success.

### Example 5

CI rejects privileged pods, but an operator creates one directly with `kubectl`. The coverage map identifies admission as missing authoritative PEP.

After deploying admission policy, bypass tests cover create/update, controllers, ephemeral-container subresource, restore, and authorized break-glass.

### Example 6

A deployment controller creates pods for a human-authored custom resource. Admission observes controller service account, not necessarily the original user. Policy authenticates controller, validates trusted owner/provenance fields, and authorizes the custom resource separately at its own admission boundary.

It does not trust a pod annotation that any workload creator could forge.

### Example 7

A critical legacy workload receives exception to `PLAT.NET.004` for one namespace, workload UID, destination, port, and seven days, with named owner/approver and compensating network monitoring.

Alerts fire at two days and six hours. Without approved renewal the exception stops matching automatically; unrelated network policy remains active throughout.

### Example 8

Bundle service fails. Local PDPs continue with signed last-known-good bundle while its maximum age is valid. Status alerts on staleness. High-risk entrypoint whose data requires five-minute freshness denies after that limit; low-risk immutable image rule continues longer under its contract.

No engine fetches or accepts an unsigned substitute.

### Example 9

A Rego helper refactor claims equivalence. Unit tests pass, but differential evaluation over a million sanitized inputs finds 37 changes involving empty arrays. Property test reveals empty `allowed_regions` should deny.

The refactor is corrected before bundle build; golden approval alone would have hidden the semantic regression.

### Example 10

Policy engine returns deny with decision ID `d-82`; the API still writes the object because an adapter treats HTTP 200 as allowance. Correlated enforcement telemetry detects the effect after denial.

Contract test requires parsing the structured result and verifies no downstream write. Policy decision logs alone would not prove protection.

## Cross-Program Connections

- **Security Engineering:** default deny, least privilege, threat modeling, separation of duties, secure failure, and incident response govern policy risk.
- **API and Service Engineering:** schemas, versioning, error contracts, gateways, authorization, idempotency, and backward compatibility define PDP/PEP interfaces.
- **Programming Languages:** declarative semantics, totality, types, undefined values, purity, evaluation order, and static analysis affect decision correctness.
- **Software Testing:** unit, property, fuzz, differential, mutation, golden, coverage, and performance methods establish evidence.
- **Distributed Systems:** replicated bundles/data, convergence, staleness, clocks, partial failure, and atomic activation shape consistency.
- **DevOps and Delivery Engineering:** Git review, CI gates, immutable artifacts, signing, promotion, canaries, rollback, and provenance deliver policy.
- **Kubernetes Engineering:** admission, CEL, webhooks, controllers, subresources, audit, and resource schemas are major policy surfaces.
- **Data Engineering:** policy data authority, schemas, snapshots, lineage, freshness, reconciliation, and privacy make decisions reproducible.
- **Reliability Engineering:** latency/error budgets, local evaluation, last-known-good state, overload, expiry, and recovery prevent control-caused outages.
- **Governance and Compliance:** normative intent, ownership, evidence, exception approval, retention, attestation, and control mapping make policy accountable.

## References

1. Open Policy Agent. [Policy Language](https://www.openpolicyagent.org/docs/policy-language). Retrieved 2026-09-02.
2. Open Policy Agent. [OPA Management APIs and Architecture](https://www.openpolicyagent.org/docs/management-introduction). Retrieved 2026-09-02.
3. Open Policy Agent. [Bundles](https://www.openpolicyagent.org/docs/management-bundles). Retrieved 2026-09-02.
4. Open Policy Agent. [Decision Logs](https://www.openpolicyagent.org/docs/management-decision-logs). Retrieved 2026-09-02.
5. Open Policy Agent. [Status](https://www.openpolicyagent.org/docs/management-status). Retrieved 2026-09-02.
6. Open Policy Agent. [Policy Testing](https://www.openpolicyagent.org/docs/policy-testing). Retrieved 2026-09-02.
7. Open Policy Agent. [Policy Performance](https://www.openpolicyagent.org/docs/policy-performance). Retrieved 2026-09-02.
8. Kubernetes. [Validating Admission Policy](https://kubernetes.io/docs/reference/access-authn-authz/validating-admission-policy/). Retrieved 2026-09-02.
9. Kubernetes. [Dynamic Admission Control](https://kubernetes.io/docs/reference/access-authn-authz/extensible-admission-controllers/). Retrieved 2026-09-02.
10. Kubernetes. [Admission Controllers](https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/). Retrieved 2026-09-02.
11. OPA Gatekeeper. [How to Use Gatekeeper](https://open-policy-agent.github.io/gatekeeper/website/docs/howto/). Retrieved 2026-09-02.
12. OPA Gatekeeper. [Enforcement Points](https://open-policy-agent.github.io/gatekeeper/website/docs/enforcement-points/). Retrieved 2026-09-02.
13. Kyverno. [Policy Types Overview](https://kyverno.io/docs/policy-types/overview/). Retrieved 2026-09-02.
14. Kyverno. [Policy Reports](https://kyverno.io/docs/guides/reports/). Retrieved 2026-09-02.

## Exercises

### Exercise 1

Define a decision contract for production image policy. Include normalized input, structured results, undefined/error behavior, data authority, latency/freshness, and PEP obligations.

### Exercise 2

Design the test and backtest portfolio for changing a policy from “approved registry” to “approved registry plus signed digest and current vulnerability threshold.”

### Exercise 3

Build an enforcement coverage map for environment deletion initiated through portal, API, CLI, GitOps, controller, administrator, break-glass, and restore paths.

### Exercise 4

Design signed bundle distribution to 400 PDP instances across 40 clusters. Include compatibility, canaries, convergence, stale behavior, rollback/roll-forward, and telemetry.

### Exercise 5

Define an exception system for a high-impact network isolation policy. Include scope, approval, expiry, compensating controls, observability, renewal, and incident handling.

## Answers to the Exercises

### Answer 1

Entrypoint `platform/image/v1/decision` accepts schema v1 with request ID, canonical workload UID, tenant/environment, actor/workload principal, operation, and every regular/init/ephemeral container containing exact registry host, repository, digest/tag, and provenance. Adapter rejects malformed, duplicated, oversized, or unsupported versions.

Policy data snapshot identifies approved registry host IDs/roots and environment requirements with owner, revision, and maximum age. Output is exactly one of allow, deny, not-applicable, unknown, or error plus stable policy/reason IDs, severity, remediation, obligations, bundle/data revisions, and decision ID. Unknown/error/timeout deny production admission; preview returns diagnostics but cannot be authoritative.

PEP evaluates before persistence, enforces denial, verifies any obligation, and correlates decision with API outcome. Budget might allocate 20 ms p99 inside an 80 ms admission timeout and require registry data no older than one hour. Logs store safe parsed fields/fingerprint, never credentials or full secret-bearing objects.

### Answer 2

Unit tests cover each approved/unapproved registry, signed and unsigned digest, threshold below/equal/above, missing and stale scan data, all container kinds, environments, exceptions, and reason codes. Boundary/adversarial tests cover tag/digest confusion, registry prefix lookalikes, alternate ports/case/Unicode, multi-arch manifests, duplicated fields, oversized lists, unknown schema, forged attestations, and clock edges.

Property tests assert production allow implies exact approved host, immutable digest, valid signature/provenance, current scan, and severity within threshold. Compatibility tests run old/new adapters and policy data. Differential tests compare current and candidate; performance tests use maximum workloads and large evidence.

Backtest current fleet, recent requests, and known denied fixtures with retrieval window, sampling, exclusions, and sanitized data. Classify every new denial or allowance. Assign legacy remediation and narrow exceptions. Candidate advances to shadow only after no unexplained diff, then canary enforcement after error/latency and ownership thresholds pass.

### Answer 3

Define protected effect as durable deletion of environment and dependent resources. Portal is not a PEP; backend deletion API authenticates and authorizes tenant/action/resource and records decision. CLI uses the same API. Direct internal API and old versions route through identical middleware. GitOps controller is authenticated as workload, and the desired deletion resource is separately authorized at admission/reconciliation.

Cloud/Kubernetes controllers receive scoped credentials and cannot independently delete outside the authorized workflow; their actions carry request/delegation ID. Administrator direct cloud/API path is restricted, monitored, and either passes native policy or requires explicit emergency workflow. Break-glass uses individual identity, narrow role, dual approval where feasible, expiry, and after-action review. Restore reconciles tombstones/current policy and cannot resurrect delete capability or bypass authorization.

For each path record PEP, entrypoint/schema, active revision/freshness, fail behavior, and enforcement evidence. Test direct, async retry, race, restore, old client, and subresource paths. Coverage remains incomplete until every path has effective denial, not merely logging.

### Answer 4

Build one immutable signed bundle from reviewed commit with policy/data schemas, exact data, dependency/runtime requirements, tests, provenance, digest, and approval. Publish by digest. Verification keys are bootstrapped out of band; each PDP validates signature, schema, compile, and engine compatibility before atomic activation, retaining last-known-good.

Promote to test, shadow fleet, then one cluster per compatibility class, 10%, 50%, and 100%. Stop on decision diff outside approval, activation error, p99 regression, denial spike, or undefined/error. Required critical instances must reach target revision; unreachable instances have a bounded remediation window and cannot serve high-risk decisions beyond maximum staleness.

Status reports PDP/cluster labels, engine version, active revision, download/activation times and errors; decisions report bundle/data revision and latency. Roll back only to a still-safe compatible digest; after security tightening use safe roll-forward. Test bundle outage, corrupt signature, thundering herd, mixed engine, stale cache, and control-plane recovery.

### Answer 5

Model each exception with stable ID, policy ID/compatible versions, exact workload principals, tenant, namespaces/resources, destinations/ports/actions, environment, risk reason, ticket, owner, independent approver, compensating controls, creation, hard expiry, renewal count, and evidence. Unknown or expired record never matches.

Store exception data under the same review, test, bundle signing, promotion, and decision provenance controls. Require scope-subset validation so exception cannot disable unrelated rules. Default to days, alert owner/approver before expiry, remove automatically, and require fresh evidence/approval for renewal. Cap renewals and escalate chronic debt.

Decision logs include exception ID and safe subject/resource, while dashboards show count, scope, use, age, renewals, and upcoming expiry. Incident response can revoke the exception immediately, deny at another PEP during propagation, and investigate usage. Emergency bypass is separate, individual, narrow, expiring, alerted, and retrospectively reviewed; it never edits an exception invisibly.
