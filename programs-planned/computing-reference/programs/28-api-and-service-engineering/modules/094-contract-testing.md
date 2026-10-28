---
module_id: API-094
program: API & Service Engineering
level: 2
module_number: 94
title: Contract Testing
status: complete
last_verified: 2026-09-02
---

# Contract Testing

## One-Page Review

### Governing question

How can producers and consumers verify, before release and without coordinating every deployment, that each supported interaction still satisfies the syntax, semantics, protocol behavior, and compatibility on which real consumers depend?

### Essential definitions

- A **contract** is the externally observable obligation between a provider and a consumer: accepted inputs, produced outputs, protocol behavior, semantics, errors, timing/order assumptions, and compatibility policy.
- A **schema test** checks an instance or description against structural rules. It cannot alone prove business meaning or runtime behavior.
- A **provider contract test** checks a provider against a provider-owned description or invariant suite.
- A **consumer-driven contract** records a consumer's concrete expectations and verifies them against the provider.
- A **provider state** is controlled fixture/setup information required to make an interaction deterministic without prescribing hidden implementation details.
- A **verification result** binds a contract version, provider version, environment/configuration, test tool/version, and outcome.
- A **deployment gate** decides whether a specific artifact may enter an environment from verified compatibility evidence, not merely whether tests once passed on a branch.
- A **false contract** is an assertion that passes but does not represent a supported production obligation; an **overfit contract** asserts incidental fields/order/values and blocks safe change.

### Central model, mechanism, or theorem

Let $R(c)$ be the interactions required by deployed consumer version $c$, $G(p)$ the interactions guaranteed by provider version $p$, and $E(c,p)$ the shared protocol/environment assumptions. Compatibility for that pair requires

$$
R(c)\subseteq G(p) \quad\land\quad E(c,p).
$$

A contract suite samples and encodes evidence about this relation; it does not prove the entire relation unless the modeled interaction space is exhaustive. Safe deployment requires verified edges for every relevant consumer-provider pair, current provenance, production-faithful semantics, and a policy for unknown consumers.

### Critical invariants

Contract ownership, supported consumers, source of truth, dialect/tool versions, matching rules, semantic assertions, provider states, and verification provenance are explicit. Tests exercise the deployable provider artifact at its public boundary with production-equivalent serialization, middleware, auth, errors, and configuration. Consumer expectations express needs rather than captured accidents.

Every supported deployed consumer has a current verified path to the candidate provider. New consumer expectations do not falsely block an unchanged provider; accepted expectations cannot later fail silently. Schema, examples, generated clients, mocks, tests, registry records, and implementation detect drift. Secrets and personal data never enter contract artifacts. Contract tests complement unit, integration, end-to-end, robustness, security, performance, and production observation.

### Common failures

Treating OpenAPI validation as behavioral proof; snapshotting whole payloads; accepting any matcher; asserting generated IDs/timestamps/order; testing mocks on both sides; provider tests that stub the endpoint under test; provider states that bypass behavior; fixtures unlike production; happy-path only; omitted errors/headers/content negotiation/auth/pagination/idempotency; consumer contracts published without branch/version provenance; stale or orphan contracts; every proposed consumer change blocking provider main; unverified deployed consumers; broker outage freezing all delivery; secrets in examples; nondeterminism; replaying mutating interactions unsafely; confusing wire compatibility with application compatibility; testing only latest/latest; and declaring end-to-end health from contract success.

### Compact example

Mobile consumer v7 needs `GET /orders/{id}` to return status `200`, content type JSON, string `id`, enum `state`, and nullable `deliveryWindow`; it ignores additive fields. Its contract uses type/enum/nullability matchers and an owned provider state. Candidate provider p12 returns an undocumented `404` for the fixture because an authorization filter changed. Schema-only comparison passes, but provider verification fails the supported v7 edge. **Conclusion:** interaction verification catches observable behavior that description diffing misses, while narrow matchers preserve additive evolution.

### Connections

[Behavioral Guarantees](021-api-contracts-and-behavioral-guarantees.md), [JSON Schema](022-json-schema.md), [OpenAPI](023-openapi-structure.md), [Mocking](029-mocking-and-consumer-exploration.md), [Protocol Buffers](052-protocol-buffers-and-schema-evolution.md), [AsyncAPI](063-asyncapi-contracts.md), [Compatibility](081-backward-and-forward-compatibility.md), [Consumer Evidence](085-consumer-inventory-and-usage-evidence.md), and [Contract Governance](088-schema-registries-and-contract-governance.md) supply the contract and lifecycle foundations. The next module continues with integration and end-to-end testing of assembled systems.

## Governing Question

How should teams select contract-test forms, encode consumer-relevant semantics without overfitting, verify synchronous/asynchronous and alternative interfaces, govern evidence across versions, and use failures as safe deployment signals rather than brittle coordination?

## Why This Matters

Services fail at boundaries even when both repositories have green unit tests. A renamed field, different null behavior, stricter parser, changed default, missing error, altered header, reused Protobuf number, GraphQL nullability change, or event timing assumption can break a consumer without preventing either component from compiling.

Large end-to-end suites find some boundary failures but are slow, stateful, difficult to diagnose, and combinatorially incomplete. Manual integration windows recreate coordinated release. Static schema diffs are fast but cannot establish that the running artifact emits or accepts the declared behavior.

Contract testing creates narrower, earlier evidence: a consumer states what it uses; a provider proves a candidate still supplies it. The useful unit is not “the API passed” but a versioned compatibility edge with provenance. That permits independent deployment only when consumer inventory and evidence are sound.

The danger is false confidence or governance gridlock. An under-specified contract misses failures. An over-specified recording makes harmless additions or nondeterministic values breaking. A stale contract protects nobody. The discipline is to encode supported externally observable obligations at the cheapest faithful boundary and retain other test layers for other risks.

## Prerequisites and Retrieval

Retrieve [API Contracts and Behavioral Guarantees](021-api-contracts-and-behavioral-guarantees.md), [JSON Schema](022-json-schema.md), [OpenAPI Structure](023-openapi-structure.md), [Validation Constraints](025-validation-constraints.md), [Examples and Executable Documentation](027-examples-and-executable-documentation.md), [Mocking and Consumer Exploration](029-mocking-and-consumer-exploration.md), [Error Translation](035-error-translation.md), [Protocol Buffers](052-protocol-buffers-and-schema-evolution.md), [GraphQL Schema Design](055-graphql-schema-design.md), [AsyncAPI Contracts](063-asyncapi-contracts.md), [Backward and Forward Compatibility](081-backward-and-forward-compatibility.md), [Consumer Inventory and Usage Evidence](085-consumer-inventory-and-usage-evidence.md), [Schema Registries and Contract Governance](088-schema-registries-and-contract-governance.md), and [Independent Evolution](090-evolving-an-api-without-coordinated-consumer-releases.md).

Retrieve the provider/consumer artifact versions and deployed inventory; canonical OpenAPI/GraphQL/Protobuf/AsyncAPI/schema revisions; generated clients/serializers; matching rules and examples; provider states/fixtures; auth/gateway/middleware/config; supported operations and errors; registry/broker publication and verification history; branch/environment/deployment metadata; flaky/quarantined results; retirement policy; personal/secret-data controls; and incidents escaped by the suite.

## Learning Objectives

After completing this module, you can:

1. distinguish schema, provider, consumer-driven, bidirectional, compatibility, integration, and end-to-end testing;
2. model contracts as versioned consumer requirements and provider guarantees rather than example snapshots;
3. choose exact values, type/range/regex/collection matchers, invariants, and generative cases without under- or over-specification;
4. design deterministic provider states that preserve public behavior and implementation freedom;
5. verify HTTP, gRPC/Protobuf, GraphQL, event, webhook, and streaming obligations at faithful boundaries;
6. record immutable provenance and construct safe deployment gates across deployed version pairs;
7. handle pending expectations, unknown consumers, stale contracts, broker outages, nondeterminism, and flaky tests;
8. protect secrets/personal data and prevent malicious or unauthorized contracts from controlling delivery;
9. diagnose failures by separating contract defect, consumer defect, provider regression, state/config drift, and tool mismatch; and
10. integrate contract evidence with governance and broader testing without claiming guarantees it cannot provide.

## Core Exposition

### Define the observable contract

A contract is larger than a payload schema. For HTTP it can include method/target, parameter serialization, headers, authentication context, content negotiation, status/error semantics, body constraints, caching/concurrency metadata, idempotency, pagination, and ordering. For messages it includes channel, envelope, key, headers, schema, semantic meaning, delivery/order/replay expectations, and acknowledgments. For streaming it includes establishment, message sequence, cancellation, backpressure, terminal status, and resumability.

Classify each assertion as syntax, structural validation, protocol semantic, domain semantic, policy, quality, or environment assumption. Contract tests are strongest for deterministic boundary observations. Latency SLOs, broad security properties, capacity, distributed consistency, and user journeys normally need other evidence even when a contract mentions them.

Name the authority. Provider-owned published contracts define what is offered. Consumer-driven interactions define what a known consumer uses. Neither should silently supersede the other. Reconcile them through governance and verification.

### Select the test form

Schema conformance validates descriptions and instances. It is cheap and broad over structural constraints but says little about implementation drift or business semantics. Provider contract tests exercise an artifact against its published description and invariants; they suit public/open ecosystems with unknown consumers.

Consumer-driven contract testing lets each consumer record minimal expectations using a mock/provider DSL, publish the interaction, and have the real provider replay and verify it. It is valuable where consumers are identifiable and teams can exchange evidence. Pact documents this consumer/provider model and provider replay.

Bidirectional approaches independently verify a consumer against its declared request/response contract and a provider against its own contract, then compare those contracts. They reduce replay coupling but depend on description completeness and compatible semantic interpretation.

Compatibility/diff checks compare schema or IDL revisions. They catch classes of structural break quickly but cannot prove runtime implementation, auth, middleware, defaults, or state behavior. Combine forms according to risk.

### Model requirements and guarantees

Build a matrix whose rows are consumer versions and columns provider versions. An edge is supported only when the exact contract/version has a successful verification by the candidate artifact under accepted environment assumptions. “Latest passes latest” proves one edge, not independent evolution.

Let $D$ be deployed consumers and candidate provider $p'$. A basic gate requires

$$
\forall c\in D:\; verified(c,p')\land fresh(c,p')\land trusted(c,p').
$$

The policy must decide unknown/unregistered consumers, inactive branches, experimental expectations, emergency changes, and evidence age. A public API cannot enumerate all consumers, so provider-owned compatibility and deprecation policy dominate; consumer-driven evidence is supplemental.

Avoid inferring use from a contract alone. Join registry metadata to runtime consumer inventory, versions, last-seen evidence, owner, environment, and support status. Retire only through explicit policy.

### Write consumer tests from actual needs

Start from consumer code behavior. What request does it construct? Which response status, headers, fields, types, enum values, null/absence distinctions, ordering, and error details affect decisions? Encode those and nothing incidental.

Use exact matching for identifiers or values whose exact semantics matter: status code, media type, discriminator, currency, authorization decision, or command name. Use type, regex, range, or collection matchers for generated IDs, timestamps, unordered items, and variable counts. A loose “any string” matcher is wrong when the consumer parses an ISO timestamp or switches on an enum.

Test negative and boundary interactions: omitted versus null, empty versus absent collection, unknown enum, min/max values, duplicate key, malformed request, unauthorized/forbidden/not-found conflict, rate limit, conditional update, partial result, and retry/replay behavior. Prefer multiple meaningful interactions over a recorded production transcript.

Treat mock success as consumer-test evidence only. The provider has not yet agreed. Ensure the consumer test actually parses/uses the mock response; otherwise a hand-written expectation can diverge from consumer code.

### Design provider states without coupling internals

An interaction needs deterministic preconditions: “order 42 exists and belongs to tenant A,” not “insert this row into table X with internal flag Y.” The provider owns mapping from named state to setup through public/test-support APIs, isolated fixtures, or controlled seed data.

Provider-state handlers must be idempotent, isolated, authorized, observable, and unavailable in production. They should not stub the provider code being verified or bypass authentication/business rules that the interaction asserts. Separate setup failure from interaction failure.

Control clocks, identifiers, external dependencies, and eventual completion deliberately. If the observable contract is asynchronous, wait on a bounded public condition rather than sleeping. Clean up or namespace runs for parallelism.

Production-equivalent middleware matters: serializers, validation, auth translation, gateway headers, content negotiation, error handlers, feature flags, and configuration. A direct controller call is not boundary verification.

### Verify provider behavior

Fetch only authorized applicable contract versions using branch/environment/deployment selectors. Validate signatures/provenance and tool/dialect compatibility. Build the provider artifact once, start it with known configuration, establish each provider state, replay the request/message, and match response/side effects against expectations.

Publish immutable result metadata: contract digest/version, consumer version/branch/environment, provider artifact digest/version/branch, verifier and plugin versions, configuration/environment identity, timestamp, result, and diagnostic link. Do not overwrite history.

Classify failures. The provider may have regressed; the consumer may request unsupported behavior; the contract may overfit; provider state may be wrong; infrastructure may be unavailable; or matcher semantics may differ. Never weaken matchers automatically to make a build green.

Run accepted contracts on provider change and new expectations on publication. Cache immutable successful results, but invalidate on provider artifact, contract, verifier semantics, relevant config, or environment-assumption change.

### Prevent new expectations from freezing providers

A consumer can publish a desired interaction before the provider implements it. If that expectation immediately fails the provider's main build, consumers can accidentally control provider delivery. Pending/experimental status separates a proposal from an accepted obligation.

Acceptance occurs through provider verification and support policy, not merely publication. Once an interaction has been accepted for a supported branch/environment, a later provider failure is a breaking regression. A new pending expectation should block the consumer from deploying where unsupported, while leaving an unchanged provider releasable. Pact's pending-pact mechanism is one implementation of this principle.

Authorization is essential. Only owned consumer identities can publish under their namespace; only provider owners can accept support; metadata transitions are audited. Expired or abandoned contracts follow an owner-notified retirement policy.

### Test description and implementation together

OpenAPI defines a language-neutral description of HTTP API capabilities; JSON Schema supplies dialect-specific validation vocabulary. Validate the document, lint local rules, compare revisions, generate boundary cases, verify provider responses and accepted requests, and verify consumer SDK serialization. A schema-valid document can still omit semantic constraints or differ from implementation.

Pin the OpenAPI and JSON Schema dialect. `format` behavior and vocabulary support vary; a keyword ignored by a validator does not enforce a contract. Test the exact validators/generators used in delivery.

For Protobuf/gRPC, compile descriptors, run compatibility checks, reserve removed field numbers/names, and test old/new generated clients against candidate servers. Binary wire safety does not guarantee application safety: added enum values can break exhaustive application logic, changed defaults can alter meaning, and streaming/deadline/status behavior is outside message shape.

For GraphQL, validate and diff schema types, nullability, arguments, directives, and deprecations; execute persisted/observed operations against the candidate. A field can remain in schema yet fail due to resolver/auth/error/null propagation or cost policy. Test exact operation documents and variables.

For AsyncAPI/event interfaces, validate operations, channels, bindings, envelope and payload dialect; verify producers emit consumer-readable messages and consumers tolerate allowed evolution. Also test key/partition, headers, ordering boundaries, duplicates, replay, acknowledgment, and side effects. Schema compatibility alone cannot prove event meaning or delivery behavior.

### Cover errors and cross-cutting behavior

Contracts that cover only `200` responses preserve the easiest path. Model stable error taxonomy, status/code/body, retryability, correlation, rate-limit and deprecation metadata, authentication challenges, validation paths, partial failures, and redaction. Do not assert volatile diagnostic text unless it is deliberately contractual.

Exercise gateway/mesh behavior only where it is part of the supported boundary. Verify the deployable route and policies rather than duplicating gateway implementation details in every consumer contract. Preserve end-user context and tenant isolation in fixtures.

For mutating interactions, use isolated synthetic tenants, idempotency keys, bounded fakes for irreversible external effects, and outcome verification. Provider replay must not charge a real card or send a real message.

### Govern deployment evidence

The gate asks “can consumer artifact c and provider artifact p be deployed together in environment e?” Build the answer from immutable verification edges plus deployment inventory. Check both directions when consumer and provider release independently: candidate consumer against deployed providers, candidate provider against deployed consumers.

Define behavior during registry/broker outage. A short outage may use recent signed immutable evidence for unchanged artifacts; a novel pair without evidence should fail closed or require risk-authorized exception. Record exception owner, scope, expiry, rollback, and later reconciliation.

Monitor contract coverage by supported consumer/operation/error—not line coverage. Track verification age, orphan owners, pending duration, flaky rate, escaped incidents, false breaks, time to resolve, and deployment blocks. High contract count is not success.

### Keep the test portfolio honest

Unit tests prove local logic. Static compatibility tests catch known description/IDL changes. Contract tests verify boundary obligations between versions. Integration tests find composition/configuration/storage/dependency failures. End-to-end tests exercise selected journeys. Fuzzing explores unexpected inputs and state sequences. Load/security/chaos tests probe other properties. Production observation reveals real distributions and unknown consumers.

Periodically perform mutation audits: intentionally remove a used field, change nullability/status/content type, alter enum/error, or break auth propagation. The expected contract test must fail. If it does not, close the gap. Also make a safe additive change; overfit contracts should not fail.

Review escaped incidents and delete contracts that assert no durable obligation. The goal is a small trustworthy compatibility net, not a museum of every historical response.

## Definitions and Notation

Let $C$ be consumer versions, $P$ provider versions, $R(c)$ required interactions, and $G(p)$ guaranteed interactions. Let $D_e\subseteq C$ be consumers deployed/supported in environment $e$. Let $V(c,p,e)$ mean an immutable trusted, fresh verification exists under accepted assumptions. Let $K(c,p)$ mean semantic compatibility, not merely parseability.

A **matcher** is a predicate over an observed value/structure. **Provider state** denotes a named externally meaningful precondition. A **pending expectation** is proposed but not yet an accepted provider obligation. **Provenance** identifies the contract, artifacts, tools, configuration, and authority behind evidence. **Drift** is divergence among declared contract, tests, generated artifacts, mocks, implementation, and runtime behavior.

## Mechanisms, Invariants, or Proof Structure

**Subset argument.** If consumer c only operates correctly for interactions $R(c)$, provider p can support it only if every required interaction is among provider guarantees: $R(c)\subseteq G(p)$. One passing example witnesses one element; it cannot establish all untested elements.

**Deployment-graph argument.** For candidate p entering e, safety evidence requires $\forall c\in D_e:V(c,p,e)\land K(c,p)$. Testing latest consumer only leaves older deployed nodes without an edge; therefore latest/latest is insufficient whenever versions coexist.

**Overfitting counterexample.** A contract asserts generated request ID equals `a1` although the consumer accepts any nonempty UUID. Provider changes to `b2`; contract fails while consumer remains correct. Exact incidental equality is therefore not a valid compatibility requirement.

**Schema insufficiency counterexample.** Both responses validate against a schema allowing state strings, but consumer switches on `paid|failed` and provider emits `pending_review`. Structural validation succeeds while application compatibility fails. Schema conformance cannot entail semantic compatibility.

## Alternatives and Trade-Offs

Provider-owned conformance scales to unknown consumers and preserves product authority, but may miss real use assumptions. Consumer-driven contracts expose actual needs and localize failures, but require identity, inventory, lifecycle, provider states, and protection from consumer overreach. Bidirectional comparison reduces replay/state coupling but trusts description completeness.

Exact golden/snapshot tests are readable and catch broad output changes, but overfit dynamic/additive data. Semantic matchers preserve evolution, but weak predicates miss defects. Generative contract tests expand boundary coverage, but require reproducible seeds, valid domain generators, and shrinking diagnostics.

Real dependencies maximize fidelity but add slowness, nondeterminism, cost, and unsafe effects. Simulators isolate and reproduce but may drift. Testcontainers/local brokers can improve protocol fidelity without providing production topology. Choose the smallest boundary that includes the behavior at risk.

Central brokers provide discovery, version graph, provenance, and deployment gates but become critical governance infrastructure. Repository-local artifacts are simpler but make cross-team inventory and retirement harder. Signed replicated evidence can bound broker outage risk.

## Failure Modes and Misconceptions

- “The schema is the contract” omits protocol and domain behavior.
- “The mock passed, so integration works” skips provider verification.
- “Record production traffic” captures accidents, secrets, and incomplete meaning.
- “Match everything exactly” blocks harmless nondeterminism and additive evolution.
- “Match everything by type” permits invalid enum, range, format, and relation changes.
- “Latest passes latest” ignores deployed version combinations.
- “Every published expectation is supported” gives consumers unilateral release control.
- “Provider states may set internals however convenient” can bypass the behavior tested.
- “Wire compatible means application compatible” ignores generated code and semantics.
- “Contract tests replace integration/E2E” ignores configuration and composition.
- “Passing once is enough” ignores artifact, contract, tool, config, and age provenance.
- “More contracts mean more safety” rewards duplication, staleness, and false obligations.
- “Broker unavailable means skip” turns missing evidence into permission.
- “Fixtures are harmless” ignores tenant leakage, secrets, and irreversible effects.
- “Flaky tests can be retried away” destroys the gate's evidentiary meaning.

## Worked Examples

### Example 1

A client reads `total.currency` and `total.amount`; a snapshot asserts every response field. Replace the snapshot with exact currency semantics, numeric amount constraints, required nesting, and permissive unrelated/additive fields. **Conclusion:** assert the consumer's dependency, not the whole representation.

### Example 2

Provider changes missing `nickname` to explicit null. JSON types still look plausible, but a consumer distinguishes absent as “not loaded” from null as “known none.” Add separate interactions for both states. **Conclusion:** absence/null semantics are contractual when behavior differs.

### Example 3

There are four deployed consumer versions and one candidate provider. Latest/latest tests one of four necessary edges, covering $1/4=25\%$ of the required provider-to-deployed-consumer graph. **Conclusion:** gate against inventory, not recency.

### Example 4

A generated timestamp changes every run. Exact equality flakes; regex alone accepts invalid dates. Use a type/format-aware matcher plus an invariant that `createdAt` is not after `updatedAt`. **Conclusion:** combine shape with semantic relations.

### Example 5

New consumer publishes an unsupported filter. Mark it pending: provider main remains releasable, consumer deployment is blocked, and provider verification records failure until accepted. **Conclusion:** proposal and accepted obligation need different lifecycle states.

### Example 6

Protobuf field 7 is removed and later reused for a different meaning. Old bytes are misread. Compatibility test rejects reuse and requires reserving number and name. **Conclusion:** descriptor rules prevent a class of corruption, though application tests remain necessary.

### Example 7

GraphQL schema still exposes nullable `order`, but resolver now throws an authorization error that null-propagates the parent. Persisted-operation verification catches changed data/error behavior. **Conclusion:** schema diff alone misses execution semantics.

### Example 8

An event payload remains valid, but producer changes partition key from account to random UUID. Per-account ordering breaks. Add key/envelope and ordered-pair verification with synthetic broker. **Conclusion:** message contract extends beyond payload schema.

### Example 9

Provider-state setup inserts directly into a table and skips normalization performed by public creation. Verification passes impossible data. Replace it with owned fixture builder using domain rules. **Conclusion:** deterministic setup must still create reachable states.

### Example 10

Broker is unavailable during release. Candidate provider and all deployed consumer/contract digests are unchanged from signed evidence verified six hours ago within a 24-hour policy; gate permits with audit. A new pair has no edge and is blocked. **Conclusion:** bounded cached evidence is different from skipping verification.

## Cross-Program Connections

[Software Engineering: Testing & Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) supplies test design, oracles, property-based testing, mutation, nondeterminism, coverage, and quality evidence.

[Software Engineering Patterns](../../11-software-engineering-patterns/ROADMAP.md) supplies ports/adapters, boundary ownership, dependency inversion, and test doubles.

[Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies partial failure, ordering, time, replay, consistency, messaging, and version coexistence.

[Platform Engineering](../../29-platform-engineering/ROADMAP.md) supplies artifact provenance, CI/CD gates, service catalogs, paved workflows, test environments, policy, and developer experience.

[Security Engineering](../../25-security-engineering/ROADMAP.md) supplies test-data protection, artifact integrity, authorization, tenant isolation, threat modeling, and exception governance.

## References

1. OpenAPI Initiative, [OpenAPI Specification 3.2.0](https://spec.openapis.org/oas/v3.2.0.html), 19 September 2025.
2. JSON Schema, [Draft 2020-12](https://json-schema.org/draft/2020-12), 16 June 2022.
3. Pact, [Provider Testing](https://docs.pact.io/implementation_guides/python/docs/provider).
4. Pact, [Pending Pacts](https://docs.pact.io/pact_broker/advanced_topics/pending_pacts).
5. Protocol Buffers, [Language Guide: Updating a Message Type](https://protobuf.dev/programming-guides/proto3/#updating).
6. GraphQL Foundation, [GraphQL Specification, September 2025](https://spec.graphql.org/September2025/).
7. AsyncAPI Initiative, [AsyncAPI Specification 3.0.0](https://www.asyncapi.com/docs/reference/specification/v3.0.0).

## Exercises

### Exercise 1

Classify the assertions for an HTTP order lookup into schema, protocol, domain semantic, policy, and non-contract quality concerns. Choose exact versus semantic matchers and explain exclusions.

### Exercise 2

Environment production has consumer versions c1, c2, and c4. Candidate provider p9 has fresh trusted verification for c1 and c4; p8 passed c2, and the provider change affects authorization middleware. Determine the gate outcome and evidence needed.

### Exercise 3

Design consumer-driven contracts and provider states for a payment creation endpoint with authentication, idempotency, validation, insufficient funds, ambiguous response loss, and irreversible external charging.

### Exercise 4

Compare provider-owned conformance, consumer-driven replay, bidirectional contract comparison, and end-to-end testing for a public API with unknown clients plus three first-party clients.

### Exercise 5

An event migration adds an enum, changes partition key, introduces compression, and moves from at-least-once to an undocumented deduplicating broker mode. Create the contract evidence and rollout gate for old/new producers and consumers.

## Answers to the Exercises

### Answer 1

Schema: object/field types, required/nullable, enum/range/pattern, array constraints. Protocol: method/path encoding, auth challenge, status, content type, caching/ETag, conditional behavior, error envelope. Domain: order identity/tenant, monetary currency+amount relation, state-transition meaning, visibility, absence/null meaning. Policy: supported versions, deprecation, rate quota, unknown consumer and verification age. Quality outside ordinary contract: latency distribution/capacity, broad availability, penetration resistance, internal algorithm. Exact-match stable discriminators/status/media type/currency and specifically requested IDs; use type/format/range/collection matchers for generated IDs/times/additive fields, plus relational invariants. Exclude internal storage, call graph, log text and incidental ordering unless observable and promised.

### Answer 2

Block p9. Required gate is $V(c1,p9)\land V(c2,p9)\land V(c4,p9)$ under production assumptions. The p8→c2 result cannot transfer because artifact changed and authorization middleware is relevant; freshness alone would not create provenance for p9. Verify c2's immutable accepted contract against exact p9 artifact with production-equivalent middleware/config/auth state, publish contract/consumer/provider/tool/config digests, and then re-evaluate. If c2 is demonstrably no longer deployed/supported, update inventory through audited retirement rather than ignoring it. An authorized risk exception needs scope, expiry, rollback, monitoring and later reconciliation.

### Answer 3

Consumer interactions cover missing/invalid credential, tenant mismatch, valid create, validation error, insufficient funds, repeated identical idempotency key returning same outcome, same key/different fingerprint conflict, and response loss followed by retry/outcome lookup. Match exact status/error code/currency and idempotency semantics; match generated payment ID/time by format and invariant. Provider states say authenticated tenant with funded account, insufficient account, existing committed payment for key+fingerprint, and conflicting key—not database rows. Set them through isolated domain-aware fixtures. Verify candidate at public middleware boundary with synthetic payment rail that records one irreversible-intent call and supports deterministic ambiguity. Assert one durable effect, stored result, dedupe, tenant/object authorization and replay. Never contact a real rail; contract tests do not replace transactional integration/failure testing.

### Answer 4

Use provider-owned OpenAPI/JSON Schema conformance and compatibility policy as the authoritative baseline because unknown public clients cannot publish a complete consumer graph. Verify deployable implementation requests/responses/errors/auth against it and preserve deprecation rules. Add consumer-driven replay for three identified first-party clients to expose their exact operation/null/error assumptions and gate candidate provider against deployed versions; pending status protects provider from unaccepted requests. Bidirectional comparison can reduce replay cost where both sides maintain sufficiently semantic descriptions, but does not prove runtime behavior. Retain a small end-to-end suite for gateway, identity, configuration, dependencies and journeys. Production telemetry discovers client/version/operation usage without treating absence as immediate retirement proof.

### Answer 5

Version matrix includes old/new producers × old/new consumers × broker/config modes. Schema/descriptor checks establish whether added enum is representable; consumer execution must prove unknown-enum behavior. Contract includes envelope/content encoding and verifies old consumers can decompress or routing prevents compressed messages reaching them. Partition key is semantic: produce ordered account event pairs and prove per-account placement/order for required operations. Delivery contract explicitly remains at-least-once unless every consumer effect/deduplication invariant and recovery/replay path supports stronger semantics; broker dedup is not silently substituted. Stage new consumers first with dual-read capability, then canary new producer/compression/key by cohort/topic/version, observe decode failures, unknown enum, duplicates/order/lag, and retain rollback/replay. Gate each deployed edge with immutable artifact/schema/config/broker provenance; block any pair without evidence or nonnegotiable ordering/idempotency compatibility.
