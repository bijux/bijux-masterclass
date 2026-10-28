---
module_id: API-021
program: API & Service Engineering
level: 1
module_number: 21
title: API Contracts and Behavioral Guarantees
status: complete
last_verified: 2026-09-01
---

# API Contracts and Behavioral Guarantees

## One-Page Review

### Governing question

What must an API promise beyond message shape so an independent consumer can act correctly under success, failure, concurrency, retries, caching, and change?

### Essential definitions

- An **API contract** is the public set of syntactic, semantic, behavioral, security, operational, and evolution promises on which consumers may rely.
- A **precondition** is a condition the consumer must establish before an operation is entitled to its normal postcondition.
- A **postcondition** is an observable condition promised after a specified successful outcome.
- An **invariant** is a condition preserved across every admitted public transition.
- A **failure contract** maps rejected, conflicted, unavailable, and uncertain outcomes to stable meanings and recovery choices.
- A **conformance claim** states which contract version and obligations an implementation satisfies, with evidence and known limits.

### Central model, mechanism, or theorem

For operation $o$, describe a contract tuple $K_o=(I_o,P_o,E_o,S_o,F_o,T_o,A_o,V_o)$: accepted inputs, preconditions, effects, successes, failures, temporal properties, authorization/visibility, and evolution rules. A schema can constrain $I_o$ and some response shapes, but it cannot alone establish the remaining components. Consumers need the whole tuple to decide whether to invoke, interpret, retry, cache, compensate, or migrate.

### Critical invariants

Method and status semantics agree with HTTP. Every success has a stated observable postcondition. Every public failure has a stable recovery meaning. Authorization governs effects and disclosed data. Retry behavior distinguishes idempotent, deduplicated, and unknown outcomes. Concurrency rules identify the state/version on which a decision was based. Limits and temporal promises name scope and measurement. Compatible evolution preserves all documented consumer assumptions, not merely parseability.

### Common failures

Calling an OpenAPI file the whole contract; documenting only happy-path examples; returning `200` for rejected work; claiming idempotency while duplicating side effects; using `500` for state conflicts; exposing retryable and terminal failures identically; promising “real time” without a bound; treating an SLO as a per-request guarantee; changing enum meaning without changing its spelling; and declaring compatibility because old JSON still parses.

### Compact example

`PUT /preferences/42` accepts a complete caller-owned preference representation with `If-Match`. Success means the stored preference equals the accepted representation and returns its new validator. A stale validator yields a conflict with refresh guidance; a repeated identical successful request has no additional effect. The contract says nothing about which table stores it. **Conclusion:** shape, precondition, effect, concurrency, and retry behavior together form the useful promise.

### Connections

[Designing an API from Consumer Tasks Rather Than Database Tables](020-designing-an-api-from-consumer-tasks-rather-than-database-tables.md) supplies consumer intent. [HTTP Methods and Their Semantics](002-http-methods-and-their-semantics.md), [Conditional Requests](006-conditional-requests.md), and [Idempotency and Safety](008-idempotency-and-safety.md) supply protocol foundations. The successors [JSON Schema](../ROADMAP.md) and [OpenAPI Structure](../ROADMAP.md) encode important structural portions of the contract.

## Governing Question

Which observable promises must be specified, tested, and evolved so consumers can reason about an API without depending on its source code, database, deployment, or accidental behavior?

## Why This Matters

A request can validate against a schema and still be unusable. The server might apply it twice after a retry, return success before durable effect, expose stale data without saying so, change authorization filtering, reorder a collection, or turn a correctable conflict into an opaque failure. None of those defects is prevented by knowing that a field is a string.

An API is a distributed boundary. Producer and consumer deploy independently, observe different clocks and failures, and may communicate through caches, proxies, gateways, and generated clients. The contract is therefore the shared reasoning surface. It must say not only which messages are legal, but what those messages mean and which observable behaviors remain stable.

OpenAPI 3.2.0, published 2025-09-19 and current when checked on 2026-09-01, describes a language-agnostic interface description for HTTP APIs and supports documentation and tooling. It is valuable, but an OpenAPI Description is not evidence that an implementation honors every described effect, ordering, authorization, latency, or compatibility promise. RFC 9110 remains authoritative for HTTP method and response semantics; RFC 9111 defines caching behavior; RFC 9457 defines the current Problem Details format. The contract combines those protocol rules with domain-specific promises.

## Prerequisites and Retrieval

Retrieve resources, representations, HTTP method properties, status codes, headers, content negotiation, validators, caching, problem details, idempotency, authorization, transactions, consistency, deadlines, rate limits, versioning, and testing. Distinguish specification from implementation, policy from guarantee, and observed behavior from promised behavior.

## Learning Objectives

By the end of this module, you should be able to:

1. enumerate structural and behavioral dimensions of an API contract;
2. write preconditions, postconditions, invariants, and failure meanings;
3. specify concurrency, retries, caching, ordering, and temporal expectations;
4. separate per-operation guarantees from service objectives and policies;
5. assess whether a contract description is complete enough for consumer decisions; and
6. design conformance evidence and compatible evolution rules.

## Core Exposition

### Treat the contract as layered

The contract has several connected layers:

- **interaction syntax:** method, target, headers, media types, and message schemas;
- **domain semantics:** resource, field, command, state, and problem meanings;
- **behavior:** preconditions, effects, postconditions, invariants, ordering, and duplicates;
- **security:** authentication context, authorization, tenant scope, and disclosure rules;
- **time and operations:** freshness, completion, retention, quotas, and availability expectations;
- **evolution:** compatibility, deprecation, version selection, and consumer migration; and
- **evidence:** examples, tests, monitoring, and conformance records.

No single artifact must contain every sentence, but the contract must be discoverable and internally consistent. A machine-readable description can reference prose semantics. A problem type URI can identify recovery documentation. An SLO document can define aggregate objectives. Scattered information without ownership, versioning, and cross-links is not a usable contract.

### Specify inputs and preconditions separately

An input schema answers whether a message has an accepted structure. A precondition answers whether the requested transition is valid in the current context. `amount` may be a positive decimal of the right currency shape, yet capture can still fail because authorization expired or the remaining capturable amount is smaller.

State who supplies each input and which values the service derives. Define defaulting, normalization, omitted versus explicit null, unknown fields, repeated fields, and cross-field constraints. If order matters, say so. If two representations are equivalent after normalization, define that equivalence where it affects signatures, idempotency, or caching.

Preconditions may include target existence, lifecycle state, version, authority, quota, time window, or related-resource state. Identify which are checked atomically with the effect. A precondition checked early and allowed to change before commit is not protective unless the implementation rechecks or isolates it.

### State observable effects and postconditions

Do not define success as “returned 2xx.” Define what a successful status entails. For creation, say whether a resource now exists, how it is identified, whether the representation is current, and which effects may still be pending. For deletion, say whether the resource is immediately absent, tombstoned, asynchronously purged, or merely scheduled for deletion.

Separate accepted, committed, and externally propagated. `202 Accepted` means processing has been accepted, not completed. If a write returns before search or replicas catch up, specify read-your-write behavior, observation endpoint, version token, or bounded lag if promised. Never imply stronger consistency than the system provides.

An invariant is stronger than one endpoint's result. Examples include “a captured amount never exceeds the authorized remainder,” “resource names are never reassigned,” and “a tenant never observes another tenant's object.” Identify the boundary over which the invariant holds and the exceptions, such as administrative recovery.

### Design failures for decisions

HTTP status codes give generic semantics. Domain failures often need a stable problem type and fields that let consumers decide. RFC 9457 identifies a problem type primarily by its `type` URI and warns against exposing implementation debugging detail.

Classify failures by next action:

- correct input and resubmit;
- authenticate or obtain authority;
- refresh state or validator and reconsider;
- wait according to a retry policy;
- observe an accepted operation;
- reconcile an unknown effect using request identity; or
- stop because the intent is terminally rejected.

The same HTTP status can carry different stable problem types, while one domain problem should not wander across contradictory statuses without a versioned reason. Define whether problem extension members are required, optional, or advisory. Human `detail` text is not a machine contract.

### Specify duplicate and retry behavior

Safety, HTTP idempotency, application deduplication, and exactly-once effects are different claims. A safe method is intended for information retrieval without requested state change. An idempotent method has the same intended effect after multiple identical requests as after one, though logs and response details can differ. A non-idempotent operation can offer deduplication through a scoped request key.

For every operation, answer:

- may a client retry after connection loss, timeout, or `5xx`?
- what constitutes the same logical request?
- how long is duplicate identity retained and in what scope?
- does a duplicate return the original result, current state, or a conflict?
- which downstream side effects share the protection?
- how is an unknown outcome reconciled?

Do not promise exactly once merely because a table has a unique key. External notifications, provider calls, and callbacks can escape that transaction.

### Define concurrency and ordering

Concurrent clients can make individually valid requests conflict. State whether updates use last-write-wins, validators, versions, idempotent commands, serialized transitions, or domain merge rules. A version token is opaque unless its comparison and scope are defined. A client should know whether a stale write is rejected, merged, or accepted over newer state.

Collections need ordering and pagination contracts. “Sorted by creation time” is incomplete if timestamps tie; add a stable tie-breaker. Cursor meaning, snapshot behavior, insert/delete effects, retention, and invalidation determine whether traversal can miss or repeat elements. Events need partition and key scope before any ordering claim is meaningful.

### Include cache and representation behavior

Caching changes observation. Define cacheability using HTTP directives, validators, and `Vary`, not consumer folklore. RFC 9111 permits reuse only under its requirements and distinguishes private from shared caches. Sensitive responses need deliberate storage rules. A response that varies by authorization, locale, or media type must not be keyed as if all consumers were equivalent.

Representations may omit fields, embed projections, or be stale. Define whether absence means unknown, unauthorized, not applicable, or not requested. If a field is derived from eventually consistent data, state its observation model. Validators should correspond to the selected representation semantics for the conditional operation they protect.

### Bound time, capacity, and availability claims

“Fast,” “real time,” and “highly available” are not testable contracts. When time matters, name start and end events, percentile or maximum, population, region, payload, load, exclusions, and measurement location. A per-request deadline guarantee differs from a monthly latency objective. An SLO describes an aggregate target and error budget; it normally does not promise that one request succeeds.

Document request size, page size, rate, concurrency, retention, timeout, and result limits with enforcement behavior. A rate limit without identity scope, window algorithm, headers, and recovery rule is incomplete. Avoid promising implementation constants that need safe tuning; specify minimum supported bounds or discoverable policy when appropriate.

### Make security promises observable but non-disclosing

State credential requirements, scopes or permissions, object-level checks, tenant boundaries, delegated authority, and sensitive-field visibility. A `404` used to conceal resource existence can be a deliberate contract. Error, timing, count, and pagination behavior must not undo that concealment.

Consumers also need to know what the service will not accept or echo: unknown writable fields, secrets in URLs, untrusted callback targets, or client-supplied audit identity. Security behavior is not an invisible implementation detail when it determines legitimate requests and observable results.

### Separate guarantee, objective, policy, and example

Normative language should be deliberate. A **guarantee** is an obligation consumers may rely on within its scope. An **objective** is a measured target that can tolerate a bounded miss rate. A **policy** is a changeable rule, ideally discoverable and bounded by contractual minima. An **example** illustrates one valid exchange but does not constrain all exchanges unless explicitly made normative.

Avoid accidental guarantees. If documentation always shows one enum order, consumers may infer order even when it is not meaningful. If a field is labeled “internal” but published for years, removal can still break real consumers. Contract review must consider explicit promises and reasonably induced dependencies while maintaining a disciplined supported surface.

### Build conformance evidence

Derive tests from each contract dimension. Schema validation checks shapes. State-machine tests check admitted transitions. Model-based and property tests check invariants. Contract tests verify consumer/provider examples. Fault injection checks timeouts, partial effects, retries, and unknown outcomes. Authorization matrices test roles, objects, fields, and non-disclosure. Cache tests pass through real intermediaries.

The bounded checker below verifies a small transition contract. It proves nothing about a deployed service; it demonstrates how preconditions, successes, failures, and idempotent duplicates become executable assertions.

<!-- bijux-verify: {"id":"behavioral-contract-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"submit:draft->submitted\nduplicate:draft->submitted\nstale:version-conflict\napprove:submitted->approved\ninvariant=terminal_approved\nevidence=bounded_transition_contract\n","stderr":""}} -->
```python
state = {"status": "draft", "version": 1}
seen = {}

def transition(command, expected_version, request_id):
    if request_id in seen:
        return seen[request_id]
    if expected_version != state["version"]:
        return "version-conflict"
    allowed = {("draft", "submit"): "submitted", ("submitted", "approve"): "approved"}
    next_status = allowed.get((state["status"], command))
    if next_status is None:
        return "invalid-transition"
    before = state["status"]
    state.update(status=next_status, version=state["version"] + 1)
    result = f"{before}->{next_status}"
    seen[request_id] = result
    return result

print("submit:" + transition("submit", 1, "r1"))
print("duplicate:" + transition("submit", 1, "r1"))
print("stale:" + transition("approve", 1, "r2"))
print("approve:" + transition("approve", 2, "r2"))
assert state == {"status": "approved", "version": 3}
print("invariant=terminal_approved")
print("evidence=bounded_transition_contract")
```

Monitor conformance continuously, but do not turn observed implementation quirks into promises silently. When observation differs from specification, decide whether the implementation is defective, the contract is incomplete, or a versioned contract change is required.

### Evolve meaning, not just shape

Compatibility is behavioral. Adding an optional response field is often structurally additive, but can break signature verification, strict decoders, cache keys, or “exact object” comparisons. Adding an enum value can break exhaustive clients. Changing default order, authorization filtering, retry timing, or error classification can break without any schema diff.

Maintain an inventory of supported consumers and contract versions. Classify changes by each contract layer, test representative consumers, publish deprecation and sunset policy, and provide migration evidence. A compatibility claim must name the consumer assumptions preserved and the observation boundary.

## Definitions and Notation

For public operation $o$, define:

$$
K_o=(I_o,P_o,E_o,S_o,F_o,T_o,A_o,V_o),
$$

where $I_o$ is accepted input, $P_o$ preconditions, $E_o$ effects, $S_o$ success outcomes, $F_o$ failures, $T_o$ temporal and ordering properties, $A_o$ authorization and visibility, and $V_o$ evolution rules.

Let implementation trace $\tau$ contain public request, response, and later observable effects. Conformance means $\tau\models K_o$ under a named contract version and environment assumptions. This notation does not claim that one finite test proves universal conformance.

A **normative guarantee** is a scoped obligation. An **SLO** is an aggregate service-level objective. A **policy** is a governed rule that may change within contractual bounds. A **problem type** is a stable machine-identified failure meaning. A **validator** is metadata used to select or condition on a representation state. **Behavioral compatibility** preserves documented decisions an existing consumer can make, not merely its ability to parse bytes.

## Mechanisms, Invariants, or Proof Structure

1. Identify the consumer decision and operation scope.
2. Specify input ownership, normalization, and structural constraints.
3. State atomically checked preconditions.
4. Define effects, successes, and observable postconditions.
5. Enumerate failure meanings and recovery choices.
6. Define duplicates, retries, concurrency, ordering, and cache behavior.
7. State authorization, tenant, field, and non-disclosure rules.
8. Bound time, capacity, retention, and operational expectations.
9. Encode machine-readable portions and link normative prose.
10. Derive conformance tests and evolution rules from the full contract.

The **semantic invariant** keeps method, status, and domain meaning aligned. The **recovery invariant** makes each failure actionable. The **retry invariant** prevents documented retry from multiplying unintended effects. The **authority invariant** covers both mutation and disclosure. The **evolution invariant** preserves supported consumer decisions across compatible change.

## Alternatives and Trade-Offs

**Prose-first versus description-first.** Prose expresses nuanced behavior but can drift and resist tooling. A structured description enables generation and linting but cannot capture every guarantee. Use one governed contract with machine-readable and prose components rather than declaring either sufficient alone.

**Strong guarantee versus weaker explicit model.** Strong consistency or latency bounds simplify clients but cost capacity and resilience. A weaker, precise model with versions, pending states, and reconciliation is better than an untrue strong promise.

**Generic errors versus domain problem types.** Generic statuses maximize reuse but may not guide recovery. Domain types add clarity and maintenance. Mint one only when the consumer needs distinct machine behavior.

**Strict rejection versus tolerant reading.** Rejecting unknown request fields catches mistakes and prevents silent intent loss. Ignoring unknown response fields enables additive evolution. The correct policy differs by direction and must be stated.

**Fixed limits versus discoverable policy.** Fixed contractual limits aid planning but constrain operations. Discoverable limits allow tuning but require stable minima, scope, and change behavior.

## Failure Modes and Misconceptions

A schema is not a behavioral contract. A `2xx` is not a domain postcondition. Idempotent does not mean identical response bytes. A retryable status does not prove the original effect did not occur. A validator is not useful without representation scope. Eventual consistency is not permission to return arbitrary old state forever. An availability SLO is not a guarantee for one request. An undocumented enum value is still a contract defect. A mocked example is not provider conformance evidence. A passing provider test does not prove every consumer assumption is supported.

## Worked Examples

### Example 1

**Situation:** A schema permits `status: "approved"` in an update. **Reasoning:** Shape validity does not grant transition authority. Remove service-owned status from generic input and define an approval operation with actor, state, and version preconditions. **Conclusion:** schema and authorization/transition contract solve different problems.

### Example 2

**Situation:** Creation returns `201` with an ID, but the resource is not readable for ten seconds. **Reasoning:** Either promise read-after-write through the returned version, return an accepted operation, or document bounded delayed visibility. **Conclusion:** creation success requires an observation contract.

### Example 3

**Situation:** A client times out after a payment request. **Reasoning:** The outcome is unknown, not automatically failed. A scoped request key and lookup lets the client reconcile before retrying. **Conclusion:** failure to receive a response is not evidence that no effect occurred.

### Example 4

**Situation:** Two clients update version 7. **Reasoning:** With `If-Match`, one commits version 8 and the other receives a precondition failure, refreshes, and re-decides. Last-write-wins would instead accept both and lose one intent. **Conclusion:** concurrency behavior is a consumer-visible guarantee.

### Example 5

**Situation:** A list promises creation-time order but two items share a timestamp. **Reasoning:** Add stable ID as a tie-breaker and bind the cursor to both values and a snapshot policy. **Conclusion:** deterministic pagination requires total ordering and traversal semantics.

### Example 6

**Situation:** A shared cache reuses a personalized response. **Reasoning:** Authorization and selection headers were absent from safe cache controls. Mark the response private or non-storable and define `Vary` where negotiation is safe. **Conclusion:** cache behavior belongs in the security and representation contract.

### Example 7

**Situation:** An API returns `payment-declined` and `provider-unavailable` as one generic error. **Reasoning:** The first normally stops or changes payment method; the second may permit bounded retry. Stable problem types support different recovery. **Conclusion:** failures should be distinguished by consumer action.

### Example 8

**Situation:** Documentation says “99.9% available.” **Reasoning:** Specify period, eligible requests, regions, status classification, maintenance, measurement source, and exclusions; identify it as an SLO rather than per-request success. **Conclusion:** operational claims require scope and kind.

### Example 9

**Situation:** A new enum value is added to a response. **Reasoning:** Old exhaustive clients may crash although JSON parses. Provide an unknown-value strategy, consumer evidence, or a versioned change. **Conclusion:** additive syntax can be behaviorally breaking.

### Example 10

**Situation:** A mock and provider both match response schemas, but the provider sends email twice on duplicate requests. **Reasoning:** Add a behavioral duplicate test and observe the external-effect ledger. **Conclusion:** conformance evidence must cover effects, not only messages.

## Cross-Program Connections

[Software Testing and Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) supplies oracle and evidence design. [Software Delivery and Reliability Engineering](../../14-software-engineering-software-delivery-and-reliability-engineering/ROADMAP.md) owns operational objectives and release evidence. [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies failure, consistency, and time models. [Security Engineering](../../25-security-engineering/ROADMAP.md) supplies authority and non-disclosure reasoning. The API program owns their externally observable composition.

## References

1. R. Fielding, M. Nottingham, and J. Reschke, [*RFC 9110: HTTP Semantics*](https://www.rfc-editor.org/rfc/rfc9110.html), Internet Standard, June 2022. Checked 2026-09-01.
2. R. Fielding, M. Nottingham, and J. Reschke, [*RFC 9111: HTTP Caching*](https://www.rfc-editor.org/rfc/rfc9111.html), Internet Standard, June 2022. Checked 2026-09-01.
3. M. Nottingham, E. Wilde, and S. Dalal, [*RFC 9457: Problem Details for HTTP APIs*](https://www.rfc-editor.org/rfc/rfc9457.html), Standards Track, July 2023. Checked 2026-09-01.
4. OpenAPI Initiative, [*OpenAPI Specification 3.2.0*](https://spec.openapis.org/oas/v3.2.0.html), 19 September 2025. Latest published version checked 2026-09-01.
5. Bertrand Meyer, *Object-Oriented Software Construction*, 2nd ed. Prentice Hall, 1997. Used for durable precondition, postcondition, and invariant foundations.

## Exercises

### Exercise 1

For `POST /reports`, list one obligation in each contract component $I,P,E,S,F,T,A,V$.

### Exercise 2

A service returns `202` for image processing and usually finishes within two minutes. Write a precise accepted-work contract covering identity, observation, terminal states, retry, cancellation, retention, and timing language.

### Exercise 3

Diagnose a `PATCH /users/{id}` contract that accepts every response field, ignores unknown input, uses last-write-wins, and returns database errors. Propose the smallest coherent repairs.

### Exercise 4

Compare a monthly 99.9% availability SLO with a per-request deadline. Explain what a consumer may infer from each and design evidence for both.

### Exercise 5

An API adds an optional `risk` object, a new `pending_review` enum value, a stricter authorization filter, and a different default sort. Classify each change structurally and behaviorally, then propose a safe rollout.

## Answers to the Exercises

### Answer 1

$I$: accepted title and bounded content schema with omission/null rules. $P$: caller may create in the target workspace and quota remains. $E$: one report resource is created under the logical request identity. $S$: `201` returns its stable URI, representation, and validator. $F$: invalid content, forbidden workspace, quota exhaustion, duplicate conflict, and unavailable dependency have distinct recovery meanings. $T$: committed report is readable through the returned URI under the stated consistency model. $A$: only authorized fields are accepted and returned. $V$: additive response fields are ignorable and breaking semantic changes require the version/deprecation process.

### Answer 2

Return `202` with a stable operation URI and bind duplicate submissions to one logical image-processing request. Define queued, running, succeeded, failed, canceled, and expired states; terminal success links the image result, while terminal failure carries a stable problem type. Retrying the same submission returns the same operation during the retention window. Cancellation is best effort and states the race with completion. Retain terminal status and result links for a declared period, after which retrieval has defined expiry semantics. “Usually within two minutes” is an objective unless a percentile, population, load, region, clock boundaries, and enforcement are stated; do not present it as a hard per-operation deadline.

### Answer 3

The endpoint permits mass assignment, silently discards intent, loses concurrent writes, and leaks persistence. Define operation-specific writable fields and reject unknown request fields. Mark derived identity, role, tenant, audit, and lifecycle fields read-only. Require a validator or version for conflicting updates and return a stable refresh/reconsider problem. Translate unique, foreign-key, and transaction errors into safe domain problems. These repairs can retain `PATCH` if remaining fields truly represent partial caller-owned state; authority-sensitive transitions need separate commands.

### Answer 4

A monthly 99.9% SLO says the measured eligible population may contain up to the defined error-budget fraction; it does not promise one request succeeds. Evidence comes from agreed server/client-side indicators, event classification, period and regional aggregation, and exclusion audits. A per-request deadline says the client stops waiting at a named duration or the server commits to a bounded response under explicit conditions. Evidence requires end-to-end clock boundaries, timeout propagation, load/payload fixtures, and checks that late effects are canceled or reconciled. Both need scope, but their quantifiers differ.

### Answer 5

The optional object is structurally additive, yet can break strict decoders, signatures, or exact comparisons. The enum value is syntactically valid but breaks exhaustive logic without an unknown strategy. Stricter authorization changes visible membership and may be required for security, but it is behaviorally breaking and needs incident/security handling plus consumer communication. Default sort changes pagination and user decisions even if schemas are unchanged. Inventory affected consumers; add tolerant decoding and enum handling first; offer explicit sort and stable cursors; test authorization and non-disclosure; expose or version the changed semantics; use telemetry and staged rollout; publish migration and deprecation where advance notice is safe.
