---
module_id: SEPAT-065
program: Software Engineering: Patterns
level: 2
module_number: 65
title: Content-Based Router
status: complete
last_verified: 2026-08-29
---

# Content-Based Router

## One-Page Review

### Governing question

How can a router inspect validated message content and choose the correct destination through versioned predicates whose types, precedence, coverage, overlap, unknown/error behavior, security, explainability, performance, and deployment blast radius are rigorously controlled?

### Essential definitions

- A **Content-Based Router (CBR)** examines message content or trusted envelope fields and routes the message to a channel selected by conditions.
- A **predicate** maps a validated message and fixed policy context to `true`, `false`, `unknown`, or evaluation error.
- **first-match** selects the earliest true predicate; **all-match** selects every true predicate; **best-match** selects a unique highest-priority/specificity match.
- **coverage** means every admitted message has a governed outcome; **disjointness** means no two exclusive predicates are simultaneously true.
- A **shadowed rule** can never win because an earlier predicate covers all messages it matches.
- A **default rule** is an explicit final policy, not implicit success; an **invalid route** handles malformed/unsupported input.
- **three-/four-valued evaluation** distinguishes false from missing/unknown and from runtime failure.
- A **policy corpus** is a governed set of positive, negative, boundary, overlap, unknown, and adversarial messages with expected decisions.
- **decision explanation** identifies rule/policy version and privacy-safe evaluated facts; it does not dump payload or reveal sensitive policy details.
- **blast radius** is the maximum message volume, fan-out, cost, disclosure, or downstream load a rule change can affect.

### Central model, mechanism, or theorem

Let admitted semantic message domain be \(M\), destinations \(D\), and predicates \(p_1,\ldots,p_n:M\to\{T,F,U,E\}\). A complete exclusive partition under strict two-valued assumptions requires

\[
\forall m\in M:\bigvee_i p_i(m)=T
\]

and pairwise disjointness

\[
\forall m\in M,\ i\ne j:\neg(p_i(m)=T\land p_j(m)=T).
\]

First-match can tolerate overlap, but rule order becomes semantic:

\[
R_v(m)=d_k,\quad k=\min\{i\mid p_i(m)=T\}.
\]

`U` or `E` must follow explicit fail-closed, quarantine, or reviewed fallback policy; silently coercing them to `F` can route incomplete or failed evidence through an ordinary default.

For numeric intervals, boundary correctness is established by precise closed/open sets. For example, `standard: a<100000` and `review: a>=100000` cover and partition integer minor-unit amounts; using `>` in the second creates a gap at exactly 100000.

### Critical invariants

- Validate and type the envelope/content before predicates; unsupported versions/malformed values never fall through as ordinary false.
- Rules read only trusted, authorized, semantically defined fields with explicit units, presence, enum, text, and time behavior.
- Resolution semantics, priority/order, default, unknown, error, and zero/many-match behavior are explicit and versioned.
- Exclusive policies are proven/tested for coverage/disjointness or deliberately use documented precedence with overlap analysis.
- Destination identifiers come from a closed authorized set; content cannot inject an address or privileged channel.
- Evaluation is pure/deterministic for fixed message/policy/reference versions; remote lookups/enrichment are separate or captured.
- Expression language/runtime is sandboxed, typed where possible, resource-bounded, and unable to perform arbitrary I/O/code execution.
- Policy change is validated, shadowed, canaried, rate/fan-out bounded, auditable, and reversible without mixed-version ambiguity.
- Decision/output identity, message identity, partition key, provenance, and content remain preserved for retry/replay.
- Observability measures rule outcomes, unknown/error/default, overlap/shadow, latency, version skew, and downstream impact without sensitive/high-cardinality data.

### Common failures

Common failures include routing raw/unvalidated JSON, missing treated as null/false, unknown enum sent to default, cents versus dollars threshold, floating-point money, inclusive-boundary gaps, broad rule shadowing a specific one, all-match accidental fan-out, regex denial of service, arbitrary `eval`, remote policy lookup per message, client-supplied destination, cross-tenant headers, sensitive-field inspection/logging, policy updates without version/replay, mixed router versions, wildcard amplification, default hiding schema evolution, and positive-only tests that never exercise near-boundary counterexamples.

### Compact example

A versioned first-match policy validates required keys, gives blocked risk highest priority, routes EU invoices at or above 100000 minor units to `manual-eu`, other high amounts to `manual-global`, and smaller amounts to `standard`. Exact-boundary, below-boundary, blocked, and missing-field messages produce four typed deterministic outcomes without mutating input.

### Connections

[SEPAT-064](064-canonical-data-model.md) supplies stable semantics for inspected content; [SEPAT-066](../ROADMAP.md) distributes facts through Publish-Subscribe Channels. CBR also connects to [Programming Languages and Semantics](../../01-programming-languages-and-semantics/ROADMAP.md), [Security Engineering](../../25-security-engineering/ROADMAP.md), [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md), and [Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md).

## Governing Question

When routing depends on message facts, what makes the predicates a trustworthy, complete, secure, reproducible policy rather than fragile conditionals that silently misclassify new, missing, ambiguous, or adversarial content?

Content-based routing is attractive because it decouples producers and processors while expressing business selection centrally. It is dangerous because content is complex, evolving, and sometimes untrusted; a one-character boundary or rule-order change can redirect a large stream.

## Why This Matters

Routing can determine financial review, regional processing, fraud quarantine, privacy jurisdiction, service tier, or clinical escalation. A syntactically correct predicate can still use wrong units, stale policy, or an untrusted field.

Production correctness therefore spans semantic data contracts, logic, configuration rollout, broker delivery, capacity, security, and human policy review. The router must explain and bound its decision without leaking the content it inspected.

## Prerequisites and Retrieval

You should understand Message Router, Message Translator, Canonical Data Model, schemas/types, Boolean and many-valued logic, predicates/sets, exact numeric/time semantics, authorization, expression sandboxes, property/mutation testing, and canary deployment. Retrieve these facts:

1. JSON/query selection can return no node, several nodes, null, or a value; these are not interchangeable.
2. Numeric representations/ranges differ; money thresholds require currency and exact scale.
3. String comparison depends on Unicode, case, locale, normalization, and sometimes code-point semantics.
4. First-match overlap is resolved by order, not eliminated; all-match overlap changes fan-out.
5. A schema-valid optional field may be absent from older messages, and a new enum may be unknown to old policy.
6. General-purpose evaluation can perform unsafe I/O, consume unbounded resources, or execute attacker-controlled code.
7. A content decision may expose sensitive categories even when the payload is encrypted in transit.

## Learning Objectives

After completing this module, you should be able to:

- formalize CBR rules as typed many-valued predicates and explicit resolution semantics;
- establish coverage, disjointness, precedence, overlap, shadow, ties, defaults, and unknown/error policy;
- write safe predicates over presence, enums, exact numbers/units, strings, collections, and time;
- choose and constrain expression languages, query selectors, policy engines, or compiled code;
- preserve message/provenance/partition semantics while durably executing routing decisions;
- protect destination allowlists, tenant/purpose authorization, sensitive inputs, and policy control plane;
- version, statically analyze, shadow, canary, fence, roll back, and replay content policy;
- bound evaluation, fan-out, rate, downstream load, and loop/amplification risk;
- construct exhaustive boundary/counterexample/property/mutation/fuzz/fault/load evidence;
- require named domain and affected-user review for high-stakes routing semantics.

## Core Exposition

### Validate before evaluating

Authenticate/integrity-check and size-bound the envelope, decode safely, select explicit type/schema version, validate shape, then construct typed semantic values. Predicates should not repeatedly parse raw strings or guess versions.

Malformed, unauthorized, and unsupported-version messages take distinct invalid/quarantine routes. They are not ordinary nonmatches.

### Use stable semantic fields

Route on fields whose owner and meaning are defined: amount plus currency/scale, region/jurisdiction provenance, risk status plus model/policy version, lifecycle version, occurrence time role. Prefer canonical envelope/content where it truly preserves meaning.

Avoid mutable display labels and fields added for one UI. Do not infer sensitive decisions from proxy attributes without reviewed policy.

### Model presence as logic

For each referenced field define missing, null, empty, zero/false, unknown code, redacted, and invalid. `exists(x) and x == value` differs from treating missing as a default. If missing evidence is safety-critical, route to unavailable/review rather than standard.

Short-circuit semantics must not hide errors. An expression that avoids accessing missing data may be valid, but the policy should remain understandable and tested.

### Define numeric predicates exactly

Use integer minor units or exact decimal under named currency/scale. State inclusivity, minimum/maximum, overflow, NaN/infinity policy, coercion, and conversion/rounding. Never compare the textual representation of numbers unless that is the contract.

Boundary corpus includes threshold, one representable unit below/above, zero, negative, max/min, wrong currency/scale, and malformed types.

### Define string predicates explicitly

State exact versus normalized/case-folded/locale-aware comparison. Normalize only contract-defined keys; preserve display/original text. Regex/glob/prefix semantics and escaping must be fixed across runtimes.

Compile safe regex with length/complexity/time limits or use engines avoiding catastrophic backtracking. Treat user strings as values, not expression fragments.

### Define time predicates with roles

Choose occurrence/effective/recorded/processing time and zone/precision. Use half-open intervals where appropriate and define late events, daylight transitions, skew, expiry, and policy effective windows. `now()` makes replay nondeterministic unless evaluation time is captured as policy input.

For “business hours,” use versioned calendar/zone/holiday rules; do not compare UTC hour to local policy implicitly.

### Define collection predicates

Specify any/all/exact membership, duplicates, order, missing/empty, and cardinality. A JSONPath nodelist may contain zero or several nodes; comparing “the value” without cardinality policy is ambiguous.

Bound collection/depth traversal. Do not route based on the first object-property iteration or unspecified array ordering.

### Choose resolution semantics

First-match is clear when precedence is business policy: denied/invalid before privileged or ordinary paths, specific before broad. All-match suits intentional independent fan-out but requires destination dedupe and maximum cardinality. Best-match requires explicit total priority and tie rejection.

For exclusive decision tables, strive for mutually exclusive/collectively exhaustive predicates. If full mathematical proof over an infinite domain is impractical, combine constraint solving/static analysis, generated boundary tests, runtime guards, and unmatched/overlap telemetry.

### Detect shadowing and gaps

Rule \(p_j\) is shadowed under first-match if every message satisfying \(p_j\) also satisfies an earlier \(p_i\). Interval/set implication is often mechanically decidable. Gaps are regions where no ordinary rule matches; overlap regions satisfy several.

Render decision tables/partitions for reviewers. Static analysis must understand the expression subset; otherwise label results incomplete and rely on corpus/runtime evidence too.

### Design default and unknown policy

Default can be a legitimate ordinary route only if every unmentioned valid case is safe there. For open enums/new versions/security evidence, default often means owned review/quarantine. Alert on default/unknown rate because it detects contract drift.

`U` differs from `F`: unknown says evidence is absent/unrecognized; false says evidence contradicts the predicate. `E` says evaluation failed. Preserve these distinctions in outcomes.

### Keep evaluation pure and reproducible

Given identical typed message, policy version, and immutable reference inputs, decision should be identical. Separate content enrichment and current authorization lookups, or capture their versions/evidence. Persist decision for delivery retry.

Historical replay either reuses original decision/policy inputs or intentionally reclassifies under current policy as a new governed operation. Do not accidentally reroute old facts through `latest`.

### Select an expression mechanism deliberately

Compiled application code offers types/tooling but couples policy release. Decision tables/config DSLs improve review but need rigorous semantics. CEL/OPA-style engines can sandbox/compile policy if input types, custom functions, resource limits, versions, and control-plane security are governed. JSONPath selects nodes; it is not by itself a complete business policy language.

Never use arbitrary language `eval`, dynamic imports/reflection, shell, filesystem/network, or unrestricted regex. Compile once/validate before activation; evaluate many under time/memory/operation budgets.

### Authorize both inspection and destination

Router identity needs permission to read the fields it inspects and publish only allowlisted channels for tenant/type/purpose/region. A producer cannot self-declare `trusted`, `risk=low`, or a destination without authoritative validation.

Predicate definitions can reveal security thresholds. Restrict control-plane read/write, audit changes, sign/checksum artifacts, separate duties for high-risk policy, and prevent producers from bypassing router ACLs.

### Minimize privacy exposure

Prefer classified metadata or purpose-specific derived facts over raw health, financial, demographic, or behavioral payload inspection. Field derivation itself must have an owner, version, consent/purpose, retention, and bias/fairness review where relevant.

Decision records store rule/version/outcome and minimal protected evidence/digests, not full payload or sensitive values. Metrics use bounded rule/outcome labels.

### Close the input-output delivery gap

Persist inbox claim, message/policy decision, and intended output identity in one local transaction; acknowledge input after recoverable obligation. Relay output with confirms and stable IDs. Retry the persisted decision rather than re-evaluating under a changed policy.

All-match tracks each output independently and defines mandatory/optional partial success. Downstream consumers remain idempotent.

### Preserve partitioning and order

Keep scoped entity key/version when required. Router instances must process/commit per-key order or consumers enforce versions/gaps. Mixed policy versions can route adjacent state transitions differently; fence epochs/drain or prove this is safe.

Content-based repartitioning is an explicit topology migration with skew and resharding consequences.

### Version and deploy policy

Immutable artifact includes predicates, order/priority, destinations, defaults, schema support, reference versions, bounds, owner/rationale, tests, checksum, and effective window. Validate syntax/types, destination/ACLs, coverage/overlap/shadow/ties/cycles, compatibility, and theoretical fan-out/rate.

Shadow against representative live/historical data without effects; compare old/new decisions, privacy-safe counts, downstream capacity, and high-risk changes. Canary bounded traffic, monitor, promote/fence, and retain rollback. Define in-flight decisions and instance version convergence.

### Bound blast radius

Estimate match rate by rule/type/tenant, fan-out, message size, destination concurrency/capacity, and cost. Reject unbounded wildcard/prefix/absence patterns that unexpectedly match future fields/types. Rate-limit per source/tenant/destination and isolate slow outputs.

A policy loop can generate new matching events; include origin/type/hop controls and alert amplification ratio.

### Explain decisions safely

Return/persist policy version, matched rule ID, destination, resolution path, and bounded reason codes. For no-match/unknown/error, identify missing/unsupported category without exposing secret thresholds or personal values to unauthorized callers.

Explanations must be derived from the same evaluation, not a separate approximation. They support audit/debugging, not proof that policy is fair or correct.

### Test the predicate space

For each rule: positive, negative, threshold ± unit, missing/null/empty/unknown/malformed, wrong version/unit/currency/zone/case, overlap with every other rule, and default. Property tests assert exclusive cardinality/allowed destinations; mutation flips operators/bounds/order/default and should fail.

Use combinatorial/decision-table generation, constraint solving for reachable overlaps/gaps, fuzz parser/expression limits, differential old/new/runtimes, and historical shadow corpus. Fault-test evaluation timeout/error, control-plane loss/tamper, mixed versions, decision transaction/output publish/ack crash. Load-test worst match/fan-out/skew and backlog recovery.

### Review high-stakes predicates with humans

Fraud, sanctions, credit, clinical triage, safety, eligibility, and regulatory routing encode consequential policy. Named domain/legal/privacy/safety experts and affected users validate inputs, thresholds, unknown handling, escalation, bias, appeals/override, and accessibility.

Automated coverage/disjointness proves logical shape under encoded premises, not substantive justice, clinical safety, or legal compliance.

### Executable model: typed first-match threshold policy

The finite function validates four required fields, applies blocked-risk priority, then exact minor-unit threshold and EU specialization, and returns rule/version. It models no broker, authorization, expression sandbox, configuration rollout, or concurrency.

<!-- bijux-verify: {"id":"content-router-policy","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"m-1 outcome=routed destination=manual-eu rule=high-eu version=risk-route-4 preserved=True\nm-2 outcome=routed destination=standard rule=ordinary version=risk-route-4 preserved=True\nm-3 outcome=routed destination=quarantine rule=blocked version=risk-route-4 preserved=True\nm-4 outcome=invalid reason=missing-field version=risk-route-4 preserved=True\n","stderr":""}} -->
```python
POLICY_VERSION = "risk-route-4"
REQUIRED = ("id", "risk", "amount_minor", "region")


def route(message):
    if any(field not in message for field in REQUIRED):
        return ("invalid", None, "missing-field", POLICY_VERSION)
    if message["risk"] == "blocked":
        return ("routed", "quarantine", "blocked", POLICY_VERSION)
    if message["amount_minor"] >= 100000 and message["region"] == "eu":
        return ("routed", "manual-eu", "high-eu", POLICY_VERSION)
    if message["amount_minor"] >= 100000:
        return ("routed", "manual-global", "high-global", POLICY_VERSION)
    return ("routed", "standard", "ordinary", POLICY_VERSION)


messages = [
    {"id": "m-1", "risk": "clear", "amount_minor": 100000, "region": "eu"},
    {"id": "m-2", "risk": "clear", "amount_minor": 99999, "region": "eu"},
    {"id": "m-3", "risk": "blocked", "amount_minor": 900000, "region": "eu"},
    {"id": "m-4", "risk": "clear", "region": "us"},
]

snapshots = [repr(message) for message in messages]
for index, message in enumerate(messages):
    outcome, destination, rule, version = route(message)
    preserved = repr(message) == snapshots[index]
    if outcome == "routed":
        print(f"{message['id']} outcome={outcome} destination={destination} rule={rule} version={version} preserved={preserved}")
    else:
        print(f"{message['id']} outcome={outcome} reason={rule} version={version} preserved={preserved}")
```

### Finite invariant argument

`m-1` has all fields, is not blocked, equals threshold, and is EU, so inclusive `>=` selects `high-eu`. `m-2` is one minor unit below threshold and reaches ordinary. `m-3` is blocked, so first-match priority returns quarantine before amount/region branches. `m-4` lacks `amount_minor`; validation returns invalid before predicate access.

The function only reads inputs and returns immutable values; snapshots remain equal. Every finite message produces exactly one outcome and fixed policy version in list order. This argument assumes required values have correct types/units/enums and Python comparisons succeed. Production validation, authorization, persistence, delivery, capacity, deployment, and policy correctness remain unmodeled.

### Evidence classification

The snippet report is empirical evidence for exact-boundary, below-boundary, priority, missing-field, and preservation behavior in one interpreter. Branch reasoning is independently recomputable. It provides no exhaustive domain partition, broker, transaction, security, configuration, load, fairness, or real policy evidence.

## Definitions and Notation

Typed admitted domain is \(M_v\) for message schema version \(v\). Policy artifact \(P_k=(predicates,order,outputs,defaults,bounds,schemas,references)\). Predicate result lattice is \(B_4=\{T,F,U,E\}\); the policy defines short-circuit and terminal handling rather than assuming ordinary Boolean coercion.

For two-valued subset, coverage region is \(\cup_i S_i=M\), where \(S_i=\{m:p_i(m)=T\}\). Overlap is \(S_i\cap S_j\), gap is \(M\setminus\cup_iS_i\), and first-match shadowing of \(j\) occurs when \(S_j\subseteq\cup_{i<j}S_i\).

Decision record \(J=(message\_id,schema\_v,policy\_k,rule,outcome,destination,time,evidence\_digest)\) is protected and immutable. Stable output identity binds `(message_id, policy_k, destination)` for idempotent relay.

## Mechanisms, Invariants, or Proof Structure

Mechanism stages: authenticate/bound/decode; validate schema and construct typed semantic input; evaluate compiled immutable policy; resolve matches/default/unknown/error; authorize closed destination; transactionally record inbox/decision/output; acknowledge input; publish idempotently; observe/reconcile.

Safety invariants are typed input, explicit many-valued handling, allowed destination, deterministic fixed-version decision, governed exclusive/fan-out cardinality, content/message preservation, durable output obligation before ack, stable retry identity, bounded evaluation/fan-out/hops, version convergence, and privacy-safe evidence.

For finite enums/intervals and restricted predicates, partition proof can enumerate/solve cells. Infinite strings/collections/custom functions usually require layered evidence: type/static analysis, generated boundary/counterexample properties, mutation/fuzz, historical shadow, runtime guards/telemetry, fault/load/security testing, and human policy review. Passing one layer does not prove the others.

## Alternatives and Trade-Offs

| Approach | Policy locus | Strong fit | Main risk |
|---|---|---|---|
| Compiled first-match code | Application release | Typed stable rules | Release coupling/hidden order |
| Decision table/DSL | Versioned config | Reviewable predicates | DSL semantics/tooling limits |
| Broker-native filters | Broker control plane | Simple metadata/content selection | Vendor semantics/limited evidence |
| Policy engine | Dedicated runtime/artifact | Shared complex policy | Dependency/control-plane complexity |
| Producer-selected channel | Producer | Simple authoritative classification | Topology/policy duplication/bypass |
| Consumer-side filter | Each consumer | Subscription autonomy | Wasted delivery/inconsistent policy |
| Message Filter | One pass/drop choice | Deliberate zero/one outcome | Silent loss if ungoverned |
| Process Manager | Stateful workflow | Decisions depend on history/outcomes | More state/operations |

Use the least powerful expression mechanism that precisely captures policy and can be secured, tested, and operated.

## Failure Modes and Misconceptions

- **“No match means false.”** It may mean missing, unknown version, parse failure, or policy error.
- **“Default guarantees completeness.”** It can hide gaps/new types and unsafe unknowns.
- **“First-match rules need not be disjoint.”** True, but order is then business semantics and shadowing must be reviewed.
- **“All-match is harmless.”** It can multiply effects/cost and partially publish.
- **“Schema validation makes fields trustworthy.”** Provenance/authorization and semantic units still matter.
- **“JSONPath is a policy engine.”** It selects nodes; resolution, types, errors, and authority remain.
- **“Use floating point for thresholds.”** Money/regulated quantities need exact representation/policy.
- **“Missing optional field is ordinary.”** It may be essential evidence for a new correctness rule.
- **“Regex is only data.”** Pathological patterns/input can consume unbounded CPU.
- **“Call a service inside the rule.”** It makes availability, consistency, authorization, and replay implicit.
- **“Latest policy should handle retry.”** Delivery retry should execute persisted original obligation, not reclassify.
- **“Explain by logging payload.”** That violates minimization and can leak policy-sensitive values.
- **“Canary percentage bounds impact.”** A broad high-volume tenant/type may dominate; bound by semantic dimensions and capacity.
- **“Coverage tests validate fairness.”** Logical completeness does not validate policy effects or bias.
- **“Automation approves high-stakes thresholds.”** Named experts and affected users remain required.

## Worked Examples

### Example 1

**Situation.** `amount > 1000` and `amount < 1000` route high/low transactions.

**Reasoning.** Exact 1000 is a gap. Use one complementary boundary such as `<1000` and `>=1000`, plus unit/currency/type validation.

**Conclusion.** Boundary sets must cover the domain deliberately.

### Example 2

**Situation.** First rule `amount>=100`, second `amount>=1000` routes 5000 to ordinary review.

**Reasoning.** Broad first rule shadows specific. Reorder or use explicit priorities/disjoint intervals; static implication analysis should reject shadowing.

**Conclusion.** Rule order can overturn intended specificity.

### Example 3

**Situation.** Missing `risk_score` evaluates as zero and routes standard.

**Reasoning.** Unknown evidence becomes low risk. Preserve missing/unknown/error and route to reviewed unavailable policy.

**Conclusion.** False and unknown require different outcomes.

### Example 4

**Situation.** Threshold 1000 means dollars, but event amount is cents.

**Reasoning.** Schema number passes; semantic unit is wrong. Require exact amount/currency/scale and mapping version before evaluation.

**Conclusion.** Predicates depend on semantic contracts.

### Example 5

**Situation.** All-match country and VIP rules both return `priority`, publishing twice.

**Reasoning.** Stable-deduplicate destination obligations while recording both matches, or define multiset behavior explicitly; cap fan-out and keep downstream idempotent.

**Conclusion.** Overlap and destination multiplicity are separate questions.

### Example 6

**Situation.** Regex `(a+)+$` evaluates against attacker-controlled long text.

**Reasoning.** Backtracking can exhaust CPU. Use bounded safe engine/pattern subset, length/time budgets, compile before activation, and fuzz adversarial inputs.

**Conclusion.** Expression safety includes computational complexity.

### Example 7

**Situation.** Rule uses `processing_time < deadline`; replay next month chooses another route.

**Reasoning.** Capture evaluation/occurred time and policy version or persist decision. Intentional reclassification is a new operation.

**Conclusion.** Ambient time destroys deterministic replay.

### Example 8

**Situation.** New optional `sanctions_status` is absent for old messages, which fall to fulfillment.

**Reasoning.** Technically compatible addition is semantically mandatory. Fence old versions, route absence to review, and coordinate producer/policy/consumer rollout.

**Conclusion.** Compatibility must include decision meaning.

### Example 9

**Situation.** A wildcard policy update routes 40% of traffic to a manual queue sized for 0.2%.

**Reasoning.** Shadow-match rate, per-tenant skew, downstream capacity/cost, canary, rate/admission, and automatic halt should catch/contain it.

**Conclusion.** Predicate correctness includes operational blast radius.

### Example 10

**Situation.** Clinical triage rule treats unknown oxygen saturation as normal and sends routine care.

**Reasoning.** Unknown measurement is not reassuring. Use explicit unavailable state, current clinical context/authority, time-bounded escalation, accessible workflow, audit, and named clinical/safety review.

**Conclusion.** High-stakes defaults must fail/degrade under reviewed policy.

## Cross-Program Connections

- [Programming Languages and Semantics](../../01-programming-languages-and-semantics/ROADMAP.md) develops types, logics, evaluation, parsing, program equivalence, and resource-safe languages.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) supplies policy authorization, safe evaluation, tenant confinement, injection/SSRF defense, privacy, and control-plane security.
- [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) develops schema/version contracts, message metadata, idempotency, and asynchronous operations.
- [Distributed Systems](../../27-distributed-systems-engineering/ROADMAP.md) grounds deterministic decisions, delivery, ordering, failure, configuration convergence, and replay.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md) operates policy rollout, brokers, telemetry, rate limits, capacity, rollback, and recovery.
- [Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) supplies decision-table, property, mutation, fuzz, differential, fault, load, and fairness evidence.
- [SEPAT-064](064-canonical-data-model.md) supplies stable semantics; [SEPAT-066](../ROADMAP.md) develops independent subscriber delivery.

## References

1. Gregor Hohpe and Bobby Woolf, *Enterprise Integration Patterns*, Addison-Wesley, 2003. Content-Based Router, Message Filter, Message Router, and routing variants.
2. Enterprise Integration Patterns, [“Content-Based Router”](https://www.enterpriseintegrationpatterns.com/patterns/messaging/ContentBasedRouter.html), accessed 2026-08-29. Pattern problem, solution, and relationships.
3. Apache Camel, [“Choice”](https://camel.apache.org/components/4.14.x/eips/choice-eip.html), 4.14 LTS documentation accessed 2026-08-29. Content-based choice/otherwise mechanisms.
4. Amazon Web Services, [“Event pattern syntax”](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-create-pattern.html), accessed 2026-08-29. Declarative event field/value matching and comparison operators.
5. Amazon Web Services, [“Best practices for EventBridge event patterns”](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-patterns-best-practices.html), accessed 2026-08-29. Pattern precision, loops, volume, and cost guidance.
6. Open Policy Agent, [“Policy Language”](https://www.openpolicyagent.org/docs/policy-language), current documentation accessed 2026-08-29. Declarative policy evaluation and language semantics.
7. Common Expression Language, [“CEL Overview”](https://cel.dev/overview/cel-overview), accessed 2026-08-29. Embedded safe, portable, compile-once/evaluate-many expressions.
8. IETF, [“JSONPath: Query Expressions for JSON”](https://www.rfc-editor.org/rfc/rfc9535.html), RFC 9535, 2024. JSON node selection, nodelists, syntax, and semantics.
9. JSON Schema, [“JSON Schema Core, Draft 2020-12”](https://json-schema.org/draft/2020-12/json-schema-core), accessed 2026-08-29. Schema vocabularies, identifiers, references, and validation architecture.
10. Martin Kleppmann, *Designing Data-Intensive Applications*, O’Reilly, 2017. Streams, partitioning, delivery, derived data, and distributed failure.

## Exercises

### Exercise 1

Construct an exclusive decision table for amount, currency, region, risk, and schema version. Prove/test coverage/disjointness, state unknown/error policy, and identify mutations that must fail.

### Exercise 2

Design a safe policy DSL/runtime for CBR. Specify type system, functions, selection semantics, budgets, compilation, versioning, authorization, explanations, testing, and control-plane deployment.

### Exercise 3

Design durable all-match routing to up to five destinations. Cover duplicate destinations, mandatory/optional outputs, transaction/ack/confirm, partial success, retry/replay, partition/order, fan-out/capacity, and reconciliation.

### Exercise 4

Plan a breaking rule change adding a semantically mandatory field while old messages/consumers remain. Cover compatibility, shadow, fencing, canary, rollback/forward, in-flight decisions, and evidence.

### Exercise 5

Review a high-stakes clinical triage CBR. Cover typed inputs/unknowns/time, thresholds/provenance, authority/privacy, explainability, bias/appeal, accessible escalation, delivery/operations, verification, and named human review.

## Answers to the Exercises

### Answer 1

First reject unsupported schema, malformed/missing currency/amount/region/risk, and unauthorized tenant. Then blocked/denied risk routes quarantine regardless of amount. For supported clear risk: wrong/unknown currency routes review; EUR with amount `<100000` routes standard-EU, EUR with `>=100000` manual-EU; USD similarly partitions at a separately reviewed threshold; unknown region routes review. Every typed admissible combination reaches one terminal branch and ordered invalid/blocked branches precede ordinary decisions.

For each fixed currency/region cell, integer intervals `<t` and `>=t` are disjoint and cover; enum branches are disjoint only if risk/currency/region are single closed typed values. Unknown/open enum is a separate value, not false. Evaluation errors quarantine/retry by category, never default ordinary. Generate Cartesian enum cells and threshold ±1/zero/min/max, missing/null/wrong type/scale/version; assert exactly one allowed outcome. Mutations changing `>=` to `>`, swapping blocked order, defaulting unknown, removing currency check, changing threshold/unit, or making all-match must fail corpus/properties.

### Answer 2

Use a non-Turing-complete typed expression language over versioned message schemas: explicit optional/presence types, exact integers/decimals, bounded strings/lists/maps/time, closed function registry, and four-valued outcomes. Selection returns typed zero/one/many nodes with explicit cardinality operators; comparisons reject type/unit mismatch. No arbitrary I/O, reflection, dynamic code/imports, recursion, filesystem/network, or unsafe regex. Bound AST size/depth, collection traversal, operations, allocation and evaluation time.

Compile/type-check once against schema; validate rule IDs/order/priority/default, destinations/ACLs, overlap/gaps/shadows/ties/cycles and fan-out. Immutable signed/checksummed artifact binds schemas/reference versions, owner/rationale/tests/effective window. Runtime receives typed input, artifact and captured evaluation context only; emits same-evaluation reason codes and privacy-safe decision evidence.

Control plane uses least privilege, review/separation for high-risk changes, audit, shadow corpus/live comparison, canary bounded by tenant/type/rate, policy-version telemetry, fencing for unsafe mixed epochs, rollback and emergency stop. Tests include decision tables/boundaries, properties/mutations, parser/expression fuzz, differential runtime versions, policy tamper/ACL, timeout/control loss, crash/relay, worst fan-out/skew/load, and historical replay.

### Answer 3

After typed evaluation, stable-deduplicate logical destinations while recording all matching rules. Enforce maximum five and allowlist/ACL. In one local transaction claim input identity, store policy version/decision, and create output rows keyed `(message_id, policy_version, destination)` with mandatory flag, key/version, pending status and protected evidence; then acknowledge input. Relays publish each output with stable ID and confirm independently.

Overall success means every mandatory output confirmed; optional outputs have their own retry/expiry/cancellation policy and cannot undo observed mandatory publications. Uncertain confirm republishes same ID; downstream effects deduplicate. Permanent mandatory rejection stays owned/quarantined until approved correction/cancellation; no fictitious cross-channel rollback. Preserve entity partition key/version per destination and define per-output order; one slow output is isolated.

Bound per-message fan-out, rate/tenant, message bytes, relay concurrency and downstream capacity. Persisted original decision drives delivery retry; intentional current-policy replay is a new operation. Reconcile input inbox, decision, intended outputs, confirms, destination inbox/effects and terminal exceptions; monitor fan-out ratio, partial age, retries, lag and mismatch. Fault-test crash at decision/output/ack/confirm boundaries and recover backlog under one destination outage.

### Answer 4

Classify the new field as semantically mandatory: old schema absence cannot mean safe default. Create a new message/policy major version or explicit transition state. New producers emit field after authoritative derivation; new policy validates it; old messages route to owned compatibility/review path. Consumers unable to honor the field are fenced from privileged effects before producers rely on it.

Inventory active/retained versions and in-flight decisions. Shadow new policy on historical/live typed data, quantify absence/unknown and decision/capacity changes, validate domain/security outcomes, then canary producer+router+consumer slices under stable IDs and one effect authority. Persist policy version/decision so retries do not re-evaluate. Fence activation epoch/drain if adjacent entity events cannot use mixed policy. Monitor version skew, default/review, outcomes, downstream effects and reconciliation.

Rollback stops new classification for new inputs only through a defined old-safe route; it cannot erase observed new outputs. Forward-recover already accepted new decisions. Retain old/new adapters/policies for in-flight/retention and emergency correction. Complete only after all required producers populate evidence, all effect consumers enforce it, old backlog is reviewed/reconciled, mixed versions drained, rollback/forward rehearsed, and no ordinary path treats absence as false.

### Answer 5

Typed input distinguishes patient/tenant, clinical condition/measurement with code system/version, exact value/unit/qualifier/range, observed/effective time and freshness, provenance/method/quality, symptoms/comorbidities, referral/order version, consent/purpose, clinician/system authority, and explicit unknown/unavailable/conflicting/redacted states. Validate dimensional and clinical applicability; thresholds bind guideline/policy version and population/context. Unknown or evaluation error never becomes normal; it triggers time-bounded clinically approved escalation or fail-safe workflow.

Authorize actor/patient/purpose/tenant and output clinical team/region; minimize/encrypt data and redact explanations/telemetry. Persist rule/policy version, reason codes, source evidence digest, decision/output obligations, overrides/appeals and corrections. Explain in understandable terms without exposing sensitive thresholds to unauthorized parties. Review disparate impact/measurement availability and give human override/appeal under audited policy.

Accessible workflow clearly differentiates urgent, routine, unavailable, conflicted, stale, overridden and unresolved states with keyboard/screen-reader/color-independent cues and mitigates alert fatigue. Test independently reviewed clinical vectors, thresholds ± resolution, units/qualifiers/unknowns/freshness, property/mutation/decision-table coverage, authorization/privacy attacks, duplicates/gaps/order, crashes/partial routing, policy mixed versions, outage/load/backlog, accessibility and disaster recovery/reconciliation. Named clinicians/triage nurses, clinical safety/informatics, relevant laboratory/pharmacy experts, patients/representatives, guideline/legal/regulatory/privacy, security, accessibility/human-factors, data/messaging/SRE, and incident-response owners review real policy. Logical completeness and green code do not establish clinical safety or fairness.
