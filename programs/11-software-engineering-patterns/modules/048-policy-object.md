---
module_id: SEPAT-048
program: Software Engineering: Patterns
level: 1
module_number: 48
title: Policy Object
status: complete
last_verified: 2026-08-28
---

# Policy Object

## One-Page Review

### Governing question

How can a changeable domain decision be represented by a named, versioned, testable object while required facts, decision outcomes, explanations, policy selection, failure defaults, authorization boundaries, temporal validity, and high-stakes governance remain explicit?

### Essential definitions

- A **Policy Object** encapsulates one coherent decision rule or rule family behind a domain-named decision interface.
- **policy facts** are immutable, validated inputs needed to decide; they exclude ambient hidden state.
- A **decision** is a typed outcome plus stable reasons, policy version, and bounded evidence metadata.
- **applicability** determines whether a policy governs the given case; it is distinct from a deny/no-match outcome.
- **policy selection** chooses a policy version by explicit jurisdiction, product, tenant, effective time, or experiment assignment.
- **effective interval** defines when one version may govern new decisions.
- **indeterminate** means required facts or a trustworthy policy decision are unavailable; it is not ordinary false.
- A **Policy Decision Point (PDP)** evaluates authorization policies; a domain Policy Object may supply facts or rules but does not replace enforcement, authentication, and current authorization context.
- **decision provenance** records the stable policy/rule-set version and fact/evidence references needed to explain or reconstruct a decision.

### Central model, mechanism, or theorem

For validated facts (x\in X), explicit context (c\in C), and immutable policy version (p_v), evaluation is

$$
decide(p_v,x,c)\to d\in\{approve,deny,not\_applicable,indeterminate,error\}\times Reasons\times v.
$$

Determinism means equal normalized (p_v,x,c) yields the same decision. It holds only when time, data/model/configuration versions, randomness, and external facts are captured. A passing finite evaluator trace does not establish that the underlying policy is lawful, fair, safe, current, or domain-correct.

### Critical invariants

- The policy owns one named decision and declares required facts, context, preconditions, outcomes, and authority.
- Evaluation is pure/deterministic for a fixed versioned snapshot, or external effects/failures are modeled outside the policy.
- Approve, deny, not-applicable, indeterminate, and error remain distinct; defaults match consequence and fail safely for authorization/security.
- Policy selection is validated, versioned, effective-dated, auditable, and not controlled by untrusted callers.
- Reasons are stable and sufficient for review without leaking thresholds, personal data, secrets, or protected decision logic.
- The action boundary revalidates time-sensitive facts, authorization, and transactional invariants; a policy decision does not reserve state.
- Unknown policy types/versions or missing required facts cannot silently fall through to a permissive default.
- Technical execution evidence is separated from domain, legal, fairness, safety, human, and regulatory approval.

### Common failures

Common failures include `GenericPolicy` with a bag of strings, reading the clock/database inside rules, mutable singleton configuration, booleans that collapse unavailable into deny or permit, caller-selected favorable policy versions, precedence hidden in unordered collections, conflicting rules resolved by iteration order, catch-all permit, authorization checks far from enforcement, explanations exposing fraud/security thresholds, serializing executable code/class names, retroactively re-evaluating history under today's policy, cache keys missing version/context, policy sprawl with no owner, and treating green tests as proof that policy itself is right.

### Compact example

A versioned return policy evaluates immutable facts. An unopened item within 30 days is approved with `within-window`; an opened non-defective item is denied; a defective item is approved under a distinct defect reason. Each decision carries version `v3`.

### Connections

[SEPAT-047](047-event-listener-and-callback.md) separates notifications from durable obligations; [SEPAT-049](../ROADMAP.md) builds valid test fixtures. Policy Object connects to [Software Design and Domain Modeling](../../09-software-engineering-software-design-and-domain-modeling/ROADMAP.md), [Security Engineering](../../25-security-engineering/ROADMAP.md), and [Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md).

## Governing Question

Which volatile decision deserves an explicit policy boundary, who owns and versions it, which facts and outcomes make it honest, and where must authorization, transactions, effects, and human governance remain separate?

Policy Object is often a domain-named Strategy, but the emphasis is on governed decision semantics: version, applicability, reasons, and evidence. A short stable invariant that belongs naturally inside an aggregate should remain there.

## Why This Matters

Eligibility, pricing, routing, retention, refund, review, and risk decisions change by jurisdiction, product, date, tenant, or contract. Scattered conditionals make precedence, history, ownership, and tests hard to locate. A Policy Object gives the decision one vocabulary and interface.

Reification can also create a dangerous pseudo-rules engine. If policies fetch arbitrary data, perform effects, select themselves, or report only booleans, the abstraction hides rather than controls change.

## Prerequisites and Retrieval

You should understand Strategy, Specification, immutable values, domain invariants, authorization, versioning, time, caching, and testing. Retrieve these facts:

1. A business policy, security policy, organizational guideline, and executable rule set can differ in authority and scope.
2. Applicability, denial, missing information, and evaluator failure are different outcomes.
3. A current decision can become stale before an action commits.
4. Historical reproducibility requires the policy and relevant fact versions used then, not only current source code.
5. Authorization evaluates subject, object/resource, operation/action, environment, and trusted policy/attributes.
6. Explanations can reveal sensitive thresholds and data even when the final decision is safe to disclose.

## Learning Objectives

After completing this module, you should be able to:

- identify decisions that benefit from a governed Policy Object;
- define versioned facts, context, outcome algebra, applicability, and explanations;
- isolate pure evaluation from fact gathering and action effects;
- design deterministic policy selection, precedence, conflict, and effective-time behavior;
- distinguish Policy Object from Strategy, Specification, validation, configuration, rules engines, and authorization systems;
- secure policy loading, caller inputs, caching, explanations, and rollout;
- test decision tables, boundaries, properties, version skew, faults, and migrations;
- review high-stakes policies without overstating software evidence.

## Core Exposition

### Name the decision

Use names such as `ReturnEligibilityPolicy`, `ShipmentRoutingPolicy`, or `RetentionDecisionPolicy`. State one governing question and the authority that owns its criteria. Avoid `BusinessRules`, `PolicyManager`, and generic field/operator bags.

If a policy contains unrelated pricing, authorization, validation, and notification rules, split by decision and owner. Composition can coordinate typed policies later.

### Define immutable policy facts

Create a minimal fact snapshot with stable types, units, provenance/version, validation status, and captured evaluation time. Gather database/service/model facts before evaluation through an application workflow.

Do not let leaves query repositories or read ambient clocks/config. That makes order, timeout, retry, consistency, and reproduction invisible.

### Use a decision algebra

A Boolean is sufficient only when false has exactly one safe meaning and callers need no explanation. Otherwise return typed outcomes: approve, deny, not applicable, indeterminate, and error, plus stable reason codes and policy version.

Define how compound outcomes combine. In authorization, indeterminate/error ordinarily cannot become permit. In a recommendation policy, not-applicable may delegate to another explicit policy rather than deny.

### Separate applicability from outcome

A Swedish consumer-return policy may be inapplicable to a business purchase in another jurisdiction. That does not mean the purchase is denied; a selector must find the governing policy or report no applicable policy.

Each policy declares applicability using trusted context. The selector detects zero or multiple applicable policies and follows a defined conflict rule—never “first in hash-map iteration.”

### Make selection explicit

Select using server-owned jurisdiction, contract/product, tenant configuration, effective instant, feature assignment, and policy catalog version. Validate that the chosen policy is approved and compatible with fact schema.

Clients may request a product operation but must not submit `policy_version=most_permissive`. Overrides require separate authority, reason, bounded scope, expiration, and audit.

### Version semantics, not only code

Give the policy/rule set a stable semantic identifier and version. Source commit/container version alone may include unrelated code and does not identify business meaning.

Persist decision policy version and bounded fact/evidence references where reproduction/audit requires it. Retain according to privacy and records rules; do not copy all personal data into a decision log.

### Define effective time

Distinguish publication, approval, effective-from/to, evaluation, occurrence, and action times. Decide which one selects policy. Late-arriving events may be evaluated under policy effective at occurrence, while current authorization uses the current policy.

Time zones, inclusive/exclusive endpoints, daylight-saving transitions, clock source, and backdating permissions need tests. Do not call `now()` independently inside multiple rules.

### Define precedence and conflicts

If rules overlap, use explicit priority with stable tie-breaking, specificity order, decision tables, or a conflict error. Document whether deny-overrides, permit-overrides, first-applicable, only-one-applicable, or aggregate scoring applies.

Security standards often require deny-by-default, but domain recommendation/pricing policies may need a different typed fallback. Do not universalize one combining algorithm.

### Keep evaluation pure

Policy evaluation should not send messages, mutate aggregates, reserve inventory, charge, or log authoritative audit as a side effect. It returns a decision/effect proposal over one snapshot.

An application command validates authorization, freshness, invariants, and transaction state, applies the action, and records required audit/outbox data. Retry of a pure policy is safe; retry of effects needs idempotency.

### Revalidate at the action boundary

Stock eligibility, credit limit, policy version, account state, or user authority may change after evaluation. Carry versions/expiry and compare or re-evaluate inside the relevant transaction/workflow.

A decision is evidence for action, not a reservation. For long-running approvals, model an approval artifact with explicit validity, revocation, scope, and signer authority.

### Design explanations by audience

Return stable reason codes and a bounded structured trace of applicable rules, facts references, and outcomes. Localize messages outside the policy. Different views serve customers, operators, auditors, and developers.

Redact fraud thresholds, security relationships, medical details, personal data, and model internals. Explanation completeness and contestability are governance questions, not just serialization features.

### Distinguish authorization policy

A domain `DiscountPolicy` is not an access-control PDP. Authorization enforcement must occur on every protected action using authenticated subject, resource, action, environment, current trusted attributes/policy, tenant scope, and fail-safe defaults.

A Policy Object can implement a PDP component, but the system still needs policy administration/information/enforcement points, current data, audit, and protection from tampering. Never trust a client-computed permit.

### Secure policy definitions

If policies are data-driven, define a small versioned allowlisted language with typed fields/operators, depth/node/value limits, deterministic semantics, and no arbitrary code/class loading. Sign/approve artifacts and control who can publish/activate/override them.

Validate unknown constructs and schema versions as errors. Sandbox/resource-bound model or plugin evaluation and expose only least-authority data/capabilities.

### Cache only complete decisions

Cache keys include semantic policy version, normalized facts or their immutable version, context/jurisdiction/tenant, captured time bucket where valid, model/config version, and authorization scope if applicable. TTL cannot replace revocation correctness.

Do not cache indeterminate/error as deny or permit unless explicitly modeled. Bound entries and sensitive values; invalidate/expire on policy or fact change and instrument stale/incorrect-hit tests.

### Roll out policies safely

Validate syntax/schema, static constraints, decision-table completeness, forbidden references, and signatures before activation. Replay representative historical fixtures, compare old/new decisions, quantify changed cohorts/reasons, and review intended deltas.

Use shadow evaluation without applying effects, controlled cohorts, monitoring, explicit rollback to an approved version, and audit of activation. Dual evaluation must not double effects or disclose alternative sensitive decisions.

### Test the decision surface

Test every outcome, applicability boundary, truth/decision table row, inclusive endpoint, missing/malformed/stale fact, zero/multiple applicable policies, precedence conflict, unknown version, time zone/DST, cache key, selection authority, explanation redaction, and action-time revalidation.

Property/metamorphic tests require valid assumptions: increasing risk might never improve approval within one policy domain, but exceptions/threshold discontinuities must be modeled. Mutation tests should catch flipped operators, missing deny, wrong priority, omitted tenant, and error-to-permit collapse.

## Definitions and Notation

Let immutable policy version (p_v), validated fact snapshot (x_s), explicit context (c), decision outcomes (O), reasons (R), and evaluation function

$$
E(p_v,x_s,c)=(o,r,v),\quad o\in O.
$$

For deterministic evaluation,

$$
(p_v,x_s,c)=(p'_v,x'_s,c')\Rightarrow E(p_v,x_s,c)=E(p'_v,x'_s,c').
$$

This equality requires normalization and captured external inputs. Action correctness additionally requires freshness/authorization/invariant checks that are not implied by (E).

## Mechanisms, Invariants, or Proof Structure

### Policy Object design procedure

1. Name one decision, its domain owner/authority, scope, consequence, and exact claim.
2. Define typed immutable facts/context, provenance, versions, time, and validation.
3. Define applicability and a complete decision/reason algebra including indeterminate/error.
4. Implement pure deterministic evaluation with explicit precedence/conflict semantics.
5. Govern selector, version/effective interval, publication, override, and rollback.
6. Separate action authorization/freshness/transaction/effects and protect explanations/definitions.
7. Design complete cache keys, bounded observability, historical evidence, and retention.
8. Test tables, boundaries, properties, faults, version migration, rollout, and high-stakes review.

### Executable finite model

The following pure policy evaluates three fixed return cases and emits stable reasons/version. It demonstrates one deterministic decision table only; it does not establish legal correctness, fact trust, selection, authorization, time semantics, persistence, or rollout safety.

<!-- bijux-verify: {"id":"policy-object-decisions","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"unopened=approve:within-window:v3\nopened=deny:opened-item:v3\ndefective=approve:defect:v3\n","stderr":""}} -->
```python
class ReturnPolicy:
    def __init__(self, version, window_days):
        self.version = version
        self.window_days = window_days

    def decide(self, days_since_purchase, opened, defective):
        if defective:
            return ("approve", "defect", self.version)
        if opened:
            return ("deny", "opened-item", self.version)
        if days_since_purchase <= self.window_days:
            return ("approve", "within-window", self.version)
        return ("deny", "window-expired", self.version)


def render(label, decision):
    outcome, reason, version = decision
    return label + "=" + outcome + ":" + reason + ":" + version


policy = ReturnPolicy("v3", 30)
print(render("unopened", policy.decide(12, False, False)))
print(render("opened", policy.decide(12, True, False)))
print(render("defective", policy.decide(45, True, True)))
```

Rule order gives the defect exception precedence over opened/window rules. That precedence is a stated example choice, not a claim about any jurisdiction or seller's obligations.

## Alternatives and Trade-Offs

- **Aggregate method:** best for a stable invariant naturally owned by one entity.
- **Strategy:** general replaceable algorithm; Policy Object is often a Strategy with stronger decision/version/governance semantics.
- **Specification:** composable proposition over candidates; useful inside a policy but often too Boolean for decisions/reasons.
- **Validation result:** reports malformed/invalid input; does not decide among valid business alternatives.
- **Decision table/DMN:** reviewable finite combinations and business tooling; requires governed execution semantics.
- **Rules engine/policy language:** dynamic administration and many rules; adds conflict, security, operations, and debugging complexity.
- **Configuration:** supplies parameters; executable decision behavior still needs ownership and validation.
- **Machine-learning model:** estimates/scorers with uncertainty and drift; requires a policy wrapper and model governance.
- **Authorization PDP:** specialized security decision architecture with enforcement and trusted attribute flows.

Prefer the smallest explicit decision abstraction that preserves vocabulary, versions, evidence, and authority.

## Failure Modes and Misconceptions

- **“Policy is another word for if statement.”** It merits an object only with coherent ownership/change/reuse/governance.
- **“Strategy and Policy are unrelated.”** Policy Object is frequently a domain-governed Strategy specialization.
- **“False is denial.”** Not-applicable, indeterminate, error, and no-match may differ materially.
- **“The policy can gather its own facts.”** Hidden I/O destroys snapshot, failure, and reproduction clarity.
- **“Current code reconstructs history.”** Policy, facts, context, and external model/config versions may have changed.
- **“Client choice enables flexibility.”** Untrusted selection can become downgrade or favorable-policy abuse.
- **“Explanations should show everything.”** Transparency must respect privacy, security, fraud, and trade-secret constraints.
- **“Caching decisions is easy.”** Missing version/context/revocation inputs yields stale or cross-tenant decisions.
- **“A permit means action is safe.”** Enforcement, freshness, transaction, and domain invariants remain.
- **“Tests certify policy legitimacy.”** Domain/legal/fairness/safety review is independent.

## Worked Examples

### Example 1

Two return rules match; explicit defect priority selects one reason. An unordered rule set changes results between runs. **Conclusion:** Conflict/precedence is policy semantics.

### Example 2

No regional policy applies. Returning deny hides configuration error; `no_applicable_policy` stops processing. **Conclusion:** Applicability is not denial.

### Example 3

Fraud data service times out. Authorization/payment policy returns indeterminate/error, not permit or ordinary customer denial. **Conclusion:** Missing evidence needs a typed safe outcome.

### Example 4

Caller submits last year's permissive version. Server selector uses current approved effective policy. **Conclusion:** Policy selection is an authority boundary.

### Example 5

Evaluation approves stock allocation at version 7; inventory changes before commit. Transactional revalidation rejects stale evidence. **Conclusion:** A decision does not reserve state.

### Example 6

Customer explanation reveals an exact fraud threshold. Audience-specific reason `manual-review-required` avoids disclosure. **Conclusion:** Explanations need security/privacy design.

### Example 7

Cache key includes customer ID but omits tenant and policy version, reusing another context's permit. Complete versioned keys fix it. **Conclusion:** Decision caches are security/domain state.

### Example 8

New policy is shadow-evaluated on historical/current traffic and changes an unintended cohort. Activation is blocked before effects. **Conclusion:** Compare decisions, not only code/tests.

### Example 9

An ML score is treated directly as approval. A versioned policy maps calibrated uncertainty, thresholds, missing features, and human review. **Conclusion:** A model is not the whole policy.

### Example 10

A clinical eligibility policy passes all fixtures but source criteria, subgroup effects, workflow, and safety lack review. **Conclusion:** Executable consistency is not clinical validity.

## Cross-Program Connections

- **Programming Languages and Semantics:** pure functions, effects, algebraic outcomes, determinism, and partiality define evaluation.
- **Software Design and Domain Modeling:** ubiquitous language, aggregates, services, specifications, and contexts determine ownership.
- **Security Engineering:** PDP/PEP, trusted attributes, fail-safe defaults, least privilege, policy administration, and audit constrain authorization.
- **Database Engineering:** snapshots, effective-dated records, transactions, indexes, and historical evidence persist policies/decisions.
- **Distributed Systems:** stale facts, partial failure, retries, version negotiation, and cache invalidation constrain remote evaluation.
- **API and Service Engineering:** versioned schemas, reason codes, compatibility, authorization, and redaction expose decisions.
- **Data and AI Engineering:** model/features versions, uncertainty, drift, subgroup evidence, and monitoring govern model-backed policies.
- **Testing and Quality Engineering:** decision tables, boundaries, properties, mutation, differential, fault, and replay tests provide evidence.
- **Cloud and Platform Engineering:** artifact approval, deployment, feature rollout, observability, rollback, and secrets own operations.
- **Safety and High-Assurance Engineering:** traceability, hazard analysis, independent review, human factors, and controlled change exceed code tests.

## References

1. Erich Gamma et al., *Design Patterns: Elements of Reusable Object-Oriented Software*, Addison-Wesley, 1994, ISBN 978-0-201-63361-0. Defines Strategy, also historically described as Policy, and related behavioral composition.
2. Eric Evans, *Domain-Driven Design: Tackling Complexity in the Heart of Software*, Addison-Wesley, 2003, ISBN 978-0-321-12521-7. Provides domain services, Specifications, bounded contexts, and explicit model language.
3. Martin Fowler, *Analysis Patterns: Reusable Object Models*, Addison-Wesley, 1997, ISBN 978-0-201-89542-1. Provides reusable domain models for rules, temporal facts, and accountability.
4. NIST, [Guide to Attribute Based Access Control Definition and Considerations](https://csrc.nist.gov/pubs/sp/800/162/upd2/final), SP 800-162, updated 2019. Defines ABAC subject/object/operation/environment evaluation and policy architecture considerations.
5. OWASP Foundation, [Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html), accessed 2026-08-28. Provides least privilege, deny-by-default, every-request enforcement, safe failure, logging, and testing guidance.
6. Object Management Group, [Decision Model and Notation 1.5](https://www.omg.org/spec/DMN/1.5/About-DMN), 2024. Defines decision models, decision tables, and executable decision semantics.
7. Ronald G. Ross, *Principles of the Business Rule Approach*, Addison-Wesley, 2003, ISBN 978-0-201-78893-8. Covers explicit business-rule ownership, vocabulary, and governance.
8. Martin Kleppmann, *Designing Data-Intensive Applications*, O'Reilly, 2017, ISBN 978-1-4493-7332-0. Provides consistency, time, versioning, event, and distributed-data foundations relevant to decision snapshots.

## Exercises

### Exercise 1

Trace the executable policy and state precisely which rule, determinism, selection, and domain-validity claims it does and does not establish.

### Exercise 2

Design a complete typed decision algebra and precedence policy for shipment routing with unavailable facts.

### Exercise 3

Design policy selection, version/effective-time governance, caching, and historical evidence for a multi-jurisdiction service.

### Exercise 4

Plan a controlled migration between two policy versions with measurable decision parity/deltas and rollback.

### Exercise 5

Review a model-backed high-stakes Policy Object without claiming legal, fairness, clinical, safety, or regulatory correctness.

## Answers to the Exercises

### Answer 1

For unopened day 12, defect/opened are false and (12\le30), so approve/within-window/v3. For opened day 12, defect false and opened true, so deny/opened-item/v3 before checking window. For defective day 45 with opened true, the first rule approves/defect/v3, demonstrating explicit defect precedence.

The run establishes three deterministic finite routes, reason/version propagation, boundary operation order, and exact Python output. It does not establish negative/zero/day-30/31 behavior, input validation, applicability, policy selection/approval/effective time, fact provenance, authorization, action freshness, persistence/cache/rollout, any jurisdiction's return law, fairness, or high-stakes suitability.

### Answer 2

Use outcomes `route(plan)`, `no_route(reason)`, `not_applicable`, `indeterminate(missing_or_stale_fact)`, and `error(invalid_fact_or_policy)`, each with policy/facts versions and bounded reasons. Capture shipment, origin/destination, carrier capabilities/capacity/price/ETA/carbon snapshot, dangerous-goods/weather/restrictions, tenant/service contract, and evaluation instant. Validate units/currencies/time zones and source freshness before pure evaluation.

Hard legal/safety restrictions exclude a route; missing required restriction/capacity evidence yields indeterminate; malformed facts yield error. Among feasible routes, explicit lexicographic or weighted policy ranks service compliance, deadline, risk, cost, then stable tie-breaker—never unordered iteration. No feasible route differs from no applicable regional policy. The booking command authenticates/authorizes, rechecks capacity/rates/restrictions and shipment version, then reserves idempotently. Test complete decision tables, boundaries, ties, unavailable/stale data, conflicting restrictions, and retries.

### Answer 3

Maintain an approved policy catalog keyed by stable semantic ID/version with jurisdiction/product/tenant scope, fact-schema range, publication/approval/effective intervals, signer/authority, status, and artifact digest. Server selector uses trusted contract/jurisdiction and captured occurrence/evaluation time; zero/multiple matches are explicit errors, while authorized time-bounded overrides are separately recorded. Unknown/incompatible artifacts fail safely.

Cache keys contain policy digest/version, normalized fact snapshot/version, tenant/jurisdiction/product, relevant time bucket, external model/config versions, and authorization scope; bound TTL/entries and support revocation. Decision record stores decision/reasons, policy digest/version, selector/context, fact/evidence references/digests, evaluation/occurrence/action times, actor/system version, and override—minimized under retention/privacy rules. Test DST/endpoints, backdating, rolling schema/version skew, tenant isolation, cache invalidation, policy revocation, historical replay, and deletion obligations.

### Answer 4

Define the intended semantic delta and approval criteria before implementation. Validate new artifact/schema, static constraints, decision-table coverage, forbidden facts/operators, signatures, determinism, resource bounds, and reason compatibility. Build authoritative boundary/golden fixtures and replay representative historical/current data, comparing outcome/reason/cohort/subgroup/financial/operational changes with uncertainty and explicit expected exceptions.

Deploy shadow evaluation with identical versioned facts but no alternate effects, instrument bounded mismatch categories, and have domain/security/legal/fairness/operations owners review. Roll out by deterministic server-owned cohort with stable assignment, guardrails, monitoring, incident/runbook, and one-click rollback to still-approved prior version. Preserve both version evidence. Fault-test selector/catalog outage, missing facts, version skew, cache, rollback, and action revalidation; stop rollout on unexplained mismatches or unsafe error/default behavior.

### Answer 5

Define decision purpose, authority, population, action/consequence, data/model sources, outcomes/uncertainty, protected attributes/proxies, exclusions, time horizon, override/appeal, human role, hazards, and exact claim. Version policy wrapper, model, training/evaluation data lineage, features/preprocessing, thresholds, calibration, facts, explanation, and monitoring. Distinguish no-match/deny, missing feature, out-of-distribution, model unavailable, evaluator error, and human deferral; default according to consequence and never auto-permit on uncertainty.

Evidence requires source-policy/requirements traceability, representative and subgroup performance/error/calibration with uncertainty, external/temporal/site validation where applicable, data quality/leakage/drift and causal/proxy review, adversarial/privacy/security tests, interpretability/contestability, human-factors/workflow trials, action-time/fault/resource testing, monitoring/appeal/incident/rollback, and applicable legal/regulatory quality records. Named domain/clinical, ML/statistics, fairness, safety, security/privacy, legal/regulatory, quality, human-factors, and operations reviewers approve. Software structure and passing fixtures establish no high-stakes validity or fitness.
