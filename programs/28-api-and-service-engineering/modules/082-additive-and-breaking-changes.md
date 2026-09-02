---
module_id: API-082
program: API & Service Engineering
level: 2
module_number: 82
title: Additive and Breaking Changes
status: complete
last_verified: 2026-09-02
---

# Additive and Breaking Changes

## One-Page Review

### Governing question

Does a proposed API delta merely add a safely ignorable capability, or does it invalidate any justified assumption of a supported client, server, intermediary, stored state, generated SDK, or operating workflow—and how can the change be delivered without surprise?

### Essential definitions

- A **delta** is the exact syntactic and behavioral difference between a governed baseline and candidate contract.
- An **additive change** adds a surface or capability without removing or redefining an existing one; additive shape alone does not prove compatibility.
- A **breaking change** requires some supported consumer/operator to change to preserve correctness, availability, security, or expected behavior.
- A **behavioral break** changes results, effects, errors, ordering, defaults, limits, timing, or security while syntax may remain unchanged.
- A **silent break** returns syntactically successful but materially wrong behavior to an old consumer.
- **expand–migrate–contract** first adds coexistence support, migrates consumers/state with evidence, then removes the old surface.
- A **compatibility exception** is an explicitly approved, scoped, communicated break with mitigation and expiry—not a reclassification as safe.

### Central model, mechanism, or theorem

Let $H$ be the supported coexistence scenarios from API-081, $A_h$ the justified observable assumptions for scenario $h$, and $O_b(h)$/$O_c(h)$ baseline/candidate observations and effects. A delta is non-breaking only if

$$
\forall h\in H,\ \forall a\in A_h,\quad a(O_b(h))\Rightarrow a(O_c(h)).
$$

Finding one supported counterexample proves a break. Passing a schema diff proves only the rules encoded by that tool; it cannot quantify unknown semantics, stored state, generated source, or operational envelopes.

### Critical invariants

Classify the whole public contract: protocol and schema, source/binary SDK, defaults and behavior, errors, authorization, quotas, latency/size, ordering/consistency, state, rollback, and lifecycle. “Additive” and “compatible” are separate review fields. Omission of every new request input preserves old behavior. New output information is safe for actual old readers and does not expand reachable variants unsafely.

No old field/type/operation is removed, renamed, repurposed, narrowed, or silently stopped until migration evidence satisfies its retirement criteria. Parallel old/new representations have deterministic precedence and one authoritative effect. Emergency security/legal/corruption changes are labeled as breaks, narrowly controlled, and monitored.

### Common failures

Calling a response-field or enum addition universally safe; adding required input; changing default under an optional field; changing null/absence; returning new errors/statuses; fixing a “bug” that clients depend on; increasing output length; tightening or loosening constraints without downstream review; changing units, timezone, order, pagination, consistency, or side effects; adding an operation that collides in generated code; moving Protobuf definitions; adding GraphQL union members to exhaustive clients; changing auth scopes or rate limits; deleting after a calendar date without usage proof; dual writes diverging; contracting before rollback/state migration; and hiding an urgent break inside a patch.

### Compact example

A candidate adds optional request field `pageSize`, defaulting to 100. The old endpoint returned all 800 matching items. The OpenAPI diff reports an optional addition, and every response parses, but old clients omit the field and now see only 100 items while believing the list is complete. The change is additive in shape and breaking in behavior. **Conclusion:** classify from old consumer outcomes, not edit direction.

### Connections

[Backward and Forward Compatibility](081-backward-and-forward-compatibility.md) supplies direction, horizon, and coexistence matrices. [Validation Constraints](025-validation-constraints.md), [Protocol Buffers and Schema Evolution](052-protocol-buffers-and-schema-evolution.md), [GraphQL Schema Design](055-graphql-schema-design.md), and [Event Versioning](069-event-versioning.md) expose format-specific deltas. The next module chooses versioning strategy when coexistence cannot preserve one contract.

## Governing Question

For every proposed contract, behavior, state, and operational delta, what counterexample would make it breaking for the supported horizon, and what expansion, migration, negotiation, version, or exception makes delivery honest and reversible?

## Why This Matters

API change review often stops at a colored schema diff: green additions are approved, red removals are blocked. That is useful automation and a dangerous mental model. An added field can change a default; an added enum value can crash a client; an added route can collide in a generated SDK; a relaxed input constraint can create state an older server cannot read. A response with the same shape can change money, ordering, authorization, retryability, or latency.

Consumers depend on both documented and reasonably stable observed behavior. Some dependencies are unjustified bugs; others reveal missing contract. Correcting the provider may still cause production impact. Calling the change a “bug fix” does not remove that impact or the need for evidence, sequencing, communication, and possibly a major contract.

Breakage costs are asymmetric. A parse failure is visible; a silently truncated list, changed unit, broadened authorization result, or duplicate side effect may look successful. A small provider edit can force thousands of consumers to coordinate. Conversely, preserving every accidental behavior indefinitely makes security and evolution impossible.

The practical discipline is to describe the semantic delta, search for supported counterexamples across the full horizon, distinguish compatible additions from breaking changes, and select a delivery pattern whose transition states are safe. Versioning communicates a break; it does not itself migrate consumers or state.

## Prerequisites and Retrieval

Retrieve [API Contracts and Behavioral Guarantees](021-api-contracts-and-behavioral-guarantees.md), [Validation Constraints](025-validation-constraints.md), [Request and Response Modeling](024-request-and-response-modeling.md), [Error Translation](035-error-translation.md), [Protocol Buffers and Schema Evolution](052-protocol-buffers-and-schema-evolution.md), [GraphQL Schema Design](055-graphql-schema-design.md), [Event Schema Design](062-event-schema-design.md), [Event Versioning](069-event-versioning.md), and [Backward and Forward Compatibility](081-backward-and-forward-compatibility.md).

Retrieve the baseline/candidate specifications and generated artifacts; semantic contract and examples; serializers/validators; default, error, auth, quota, pagination, ordering, consistency, and side-effect behavior; active consumer and intermediary evidence; persisted state and rollback artifacts; replay/webhook/subscription patterns; performance/security/privacy budgets; deprecation policy; release/version policy; and previous compatibility waivers or incidents.

## Learning Objectives

After completing this module, you can:

1. distinguish additive syntax, compatible behavior, breaking behavior, and emergency exceptions;
2. write a semantic delta across protocol, schema, source, behavior, operations, security, and state;
3. classify additions/removals/renames/types/requiredness/defaults/constraints/enums/errors and limits;
4. analyze REST/JSON, Protobuf/gRPC, GraphQL, webhooks/events, generated SDKs, and intermediaries;
5. find counterexamples using the supported compatibility horizon and real consumer assumptions;
6. recognize silent breaks in pagination, ordering, units, authorization, consistency, retries, and side effects;
7. design expand–migrate–contract transitions with precedence, dual operation, rollback, and retirement evidence;
8. choose additive field, parallel field/operation, negotiation, adapter, or new version/type;
9. govern bug fixes and urgent security/legal/corruption breaks honestly; and
10. build automated and empirical gates that intentionally catch known breaking mutations.

## Core Exposition

### Write the delta before labeling it

Produce a structured change record, not merely a textual diff. Name the baseline and candidate artifacts, affected operations/messages/SDK symbols/state, old behavior, new behavior, unchanged guarantees, supported horizon, rollout and rollback paths, consumer evidence, and proposed classification.

Cover routes/methods, media types, request/response/header/trailer schemas, errors/statuses, auth scopes, defaults, validation, ordering, pagination, consistency, side effects, idempotency, retries, limits, latency/size, generated code, stored state, webhooks/events, and documentation that consumers reasonably implement.

For every changed element, write old input-to-output/effect examples and candidate examples. Include absence, null, zero, empty, boundary values, unknowns, concurrency, partial failure, and rollback state. “No intended behavior change” is a hypothesis that needs comparison.

Separate motivation from classification. A performance improvement, security fix, simplification, or standards correction may be valuable and still breaking. The reason informs priority and migration; it does not alter consumer impact.

### Use counterexamples, not edit colors

From API-081, take every supported coexistence scenario $h$ and its justified assumptions. Try to construct an old valid request, state, or workflow whose observation/effect violates one assumption under the candidate. One valid supported counterexample is enough to classify the delta as breaking for that horizon.

Examples of assumptions include: accepted inputs remain accepted; omitted inputs retain behavior; existing fields remain present and meaningful; output sets remain safely interpretable; status/error codes preserve client decisions; ordering/cardinality/consistency remain within contract; effects occur once; authorization never broadens improperly; deadlines/limits remain feasible; and rollback reads candidate state.

Automated schema rules can search a large syntactic space. Human/domain review and executable behavioral fixtures search semantics. Production evidence identifies which assumptions are actually used. None substitutes for the others.

If no counterexample is found, state what was tested and what remains unknown. “Non-breaking” is a scoped claim, not proof about every unregistered consumer.

### Classify genuinely additive operations

A new independent operation can be additive when old routes, behavior, quotas, auth, generated names, and discovery remain unchanged, and consumers must opt in. Still test route ambiguity, method/path collision, gateway policy, OpenAPI operation IDs, generated SDK symbols, shared quotas, navigation links, and wildcard routing.

An added optional response expansion or query feature is safer when absent requests receive byte/semantically equivalent old responses. An opt-in field must not consume shared quota or latency for old clients unexpectedly. Cache keys and `Vary`/representation negotiation include the opt-in dimension.

New event/webhook types can surprise wildcard subscribers, generic routers, schema validators, quotas, and billing. “Consumers did not subscribe by exact type” is a required assumption, not automatic truth. Provide filtering and unknown-type policy.

Adding a new API alongside an old one is structurally additive but creates ownership and lifecycle obligations. Avoid two partially overlapping operations with ambiguous precedence or divergent effects.

### Evaluate request field additions

An optional request field is compatible for old clients only when omission produces their old result/effect. The new server must distinguish absent from explicit zero/false/empty/null where semantics differ. Default behavior belongs in the public contract and tests.

It is also compatible with old servers only if new clients do not send the field to them, the old server safely ignores it by contract, or capability/version negotiation routes correctly. Strict JSON input validators commonly reject unknown properties; do not assume bidirectional support.

Required request additions are breaking. So are making optional fields required, requiring previously optional headers, or adding mandatory auth context. Use server derivation, staged optional collection, new operation/version, or a migration that proves all writers updated before enforcement.

Security-sensitive commands should usually reject unknown fields rather than silently ignore a misspelled control. Plan extension points explicitly instead of trading correctness for accidental forward tolerance.

### Evaluate response field additions

A response property addition can be compatible when actual old readers ignore/preserve unknown properties, signature/canonicalization and cache logic remain valid, response size/latency stay within bounds, and the addition does not redefine old fields. Closed validators and generated DTOs can reject it.

Read-modify-write clients may drop the field and overwrite state. Mark server-owned/output-only data, use PATCH/field masks, preserve unknowns, and enforce conditional updates. Adding sensitive data can also expand disclosure even if parsing succeeds.

Populating an old optional field that was historically absent is an output-set expansion and can break clients that assumed absence. Changing serialization of default/null fields can break presence-sensitive logic, hashes, signatures, or diffs.

An opt-in field/expansion avoids old reader exposure but needs cache variance and authorization. Do not make old requests pay its computation cost.

### Treat enum, union, and subtype growth as reachable behavior

Adding a request enum value is usually safe for old clients because they will not send it, but new clients must not send it to old servers without negotiation. Adding a response enum value, union member, resource subtype, error code, or webhook type expands what old readers can receive.

Old exhaustive switches may fail compilation, throw, or enter an unsafe default. Domain policy decides whether unknown means quarantine, render generically, retry later, preserve raw value, deny, or fail. Never coerce an unknown payment/auth state into a known success/allow value.

Protobuf binary wire rules may call enum or field additions safe, while generated-source or application logic breaks. GraphQL adding a field is normally opt-in because the client selects fields; adding a possible union/interface/enum result affects code that handles the selected field.

Deploy tolerant readers before enabling new writers/values. Observe readiness by actual version/behavior, not a dependency declaration.

### Classify removals, renames, and moves

Removing an operation, field, enum value, error, header, media type, auth method, or SDK symbol is breaking while any supported consumer or state depends on it. Making a field conditionally absent is still a removal for scenarios where it was guaranteed.

Rename equals remove plus add. Keep the old name during migration with deterministic precedence if both appear, response parity, conflict rejection, and one internal canonical representation. Never let two values silently disagree.

Wire-safe moves can break source. Moving a Protobuf declaration between files or packages can change generated imports/symbols; changing an OpenAPI operation ID changes SDK method names; reorganizing schema components can affect codegen even if HTTP is identical.

Contract only after usage evidence, state migration, rollback expiry, partner/dormant/recovery checks, and published retirement policy. A deadline without proof is notice, not safe removal.

### Classify types, formats, units, and precision

Changing a field type is generally breaking across schema, generated source, validation, storage, and semantics, even when a wire encoding can parse both. Introduce a new explicitly named field and migrate.

Keeping type while changing format is equally risky: IPv4 to IPv6 in one string, numeric ID to composite ID, UTC instant to local date, kilograms to grams, cents to decimal currency, unordered set to ordered priority list, or snapshot to delta. Consumers build storage and decisions around definitions.

Widening numeric range or string/array length can break old readers/storage/downstreams; narrowing rejects previously valid data. Increasing precision can change equality/hashes; decreasing precision loses value. Changing Unicode normalization/case/collation changes identity and ordering.

Never infer semantic compatibility from JSON's generic `number`/`string` or from Protobuf wire-type compatibility. Units, authority, scale, timezone, null/absence, and invariants are part of the field.

### Classify constraints in both directions

Tightening request validation is breaking if a previously valid supported request becomes invalid: smaller max, stricter regex, reduced enum, forbidden unknowns, required combination, or changed time window. It may be necessary for security/correctness, but still needs exception/migration handling.

Loosening input validation seems additive but can create values old consumers, rollback servers, stores, indexes, or downstream APIs cannot handle. It can also expand abuse cost. Candidate output/state domains must remain within every promised reader's capability.

Tightening output guarantees can sometimes help, but changing variability may expose hidden client assumptions. Loosening an output bound directly expands what clients must accept. Treat documented and reasonably relied-on limits as contract.

Validation error structure, error code, field paths, aggregation, and fail-fast versus collect-all behavior can be machine-consumed. Stable identifiers matter even when human prose may change.

### Classify defaults, behavior, and side effects

Default changes are behavior changes applied precisely to old clients that omit new information. Review timeouts, sorting, page size, consistency, locale, filters, expansion, retry, conflict, and feature defaults. Keep old default or require explicit opt-in/version.

Changing an operation from synchronous completion to accepted asynchronous work, from create to upsert, from replace to merge, from idempotent to non-idempotent, or from one effect to several is breaking. So is altering duplicate handling, concurrency conflict, read-after-write, or partial-success semantics.

“Bug fix” requires a contract analysis. If implementation contradicted an explicit safe contract and consumers could not reasonably rely on it, restoring the contract may be compatible by policy. If behavior was longstanding, documented by examples, or widely relied on, abrupt correction can break. Measure, communicate, stage, and consider a new mode/version.

Silent data changes deserve stricter review than visible errors. Wrong successful money, permissions, counts, or state can propagate before detection.

### Classify status, error, retry, and failure behavior

Status codes and stable error types drive retry, fallback, user messaging, compensation, and alerting. Changing `409` to `503` can turn a permanent conflict into a retry storm; changing `404` to `200 null` can make caches or existence checks wrong.

Adding a new possible error is an output-variant addition. It is compatible only if old clients have a safe generic path and the new condition does not violate promised success. Reusing an old code for a different cause is a semantic break.

Changing timeout, cancellation, rate-limit, retry-after, idempotency, or unknown-outcome behavior affects distributed effects. Preserve effect identity and do not cause old retries to duplicate work. Error text can be non-contractual, but machine-readable code/type, fields, and retryability must be explicit.

Changing from fail-fast to partial results or vice versa alters success accounting. Make completeness/provenance explicit and opt in where old clients assume all-or-nothing.

### Classify security and policy changes

Adding required scopes/claims/authentication methods breaks callers without them. Removing authorization checks is a security regression even if requests succeed. Changing tenant visibility, redaction, consent, retention, or field classification can be incompatible with both clients and law/policy.

New response fields need least-privilege review; additive disclosure is not harmless. New filter/query capabilities can enable enumeration or expensive abuse. New defaults cannot broaden access for old callers.

Critical vulnerability, legal, privacy, or corruption fixes may require an immediate break. Label the impact, use the narrowest server-side mitigation, preserve safe traffic, provide precise stable errors and migration guidance, notify affected owners/channels, monitor, and record the exception/expiry.

Never weaken validation or retain an insecure legacy path merely to make a compatibility dashboard green. Compatibility governance exists to manage justified exceptions, not forbid safety.

### Classify operational envelope changes

Old clients embody timeouts, concurrency, buffers, pagination loops, and quotas. Increasing response size, latency, stream duration, connection count, or cost can trigger timeouts/retries and overload while schemas pass. Decreasing rate limits or burst capacity rejects previously sustainable workflows.

Changing pagination defaults/completeness, ordering, consistency, cacheability, ETags, compression, streaming framing, or backpressure changes the operational protocol. Measure old client behavior at tail/boundary conditions.

Adding eager computation for a new response field can harm old requests. New optional features should consume cost only when selected, with separate quota and cache dimensions as needed.

SLO changes are contract changes when promised. An implementation improvement that stays within bounds is internal; a new requirement on client timeout/retry logic is breaking.

### Use expand–migrate–contract

**Expand:** add the new field/operation/state in a way old behavior still works. Deploy readers that understand both forms. Define one canonical internal meaning, precedence/conflict rules, adapters, dual-read/write invariants, telemetry, and rollback compatibility. Keep new emission gated.

**Migrate:** enable new writers/consumers gradually; backfill or translate state with checksums/reconciliation; shadow and compare; track old/new usage, parity, errors, unknowns, and business effects. Keep rollback safe and repairable. Dual write from one authoritative transaction/outbox, not independent best effort.

**Contract:** stop old emission only after supported consumers and recovery paths migrated; then remove old reads/state/code/schema after rollback/artifact/backup/replay horizons expire. Update registry/contracts and delete flags/adapters intentionally. Contracting is its own reviewed change.

At every stage, transition-state invariants matter more than target architecture elegance. If both fields are accepted, conflicting values must not choose unpredictably. If both event types publish, one occurrence must not cause two effects.

### Choose a delivery pattern

Use a simple additive field when absence is honest and all old readers tolerate new output. Use parallel old/new fields when meaning can coexist with precedence and bounded migration. Use a new operation/resource/event type when semantics or side effects differ materially. Use content/capability negotiation when representations/capabilities can be selected safely.

Use an adapter/upcaster/downcaster only when translation is deterministic and preserves required meaning. Lossy downcasting needs explicit policy and must not hide safety-relevant data. Use a new major API version when no single contract can preserve the supported assumptions.

Versioning is not a waiver. Both versions need implementation, data, auth, observability, support, and retirement. Avoid versioning every additive feature; avoid mutating an old version for a true break.

### Build gates and evidence

Run schema diff against exact baselines with rules for OpenAPI/JSON Schema/Protobuf/GraphQL and generated source. Compile old/new SDKs, run serialization/unknown round trips, and test request/response directions. Keep golden behavioral fixtures for defaults, errors, ordering, pagination, limits, auth, effects, and rollback state.

Mutation-test the gate: remove/rename fields, add required input and response enum values, change types/defaults/status/limits/order, drop unknown fields, and write candidate-only state. Each intended breaking mutation should fail the relevant gate. Otherwise coverage is ceremonial.

Combine consumer-driven contracts with provider invariants and usage evidence. Known consumer tests cannot authorize violation of provider security/data invariants; provider specs cannot reveal every actual parsing/storage assumption. Sample/shadow production safely and protect sensitive data.

Review records include baseline/candidate digests, classified deltas, horizon, counterexamples tried, test results, consumer/state evidence, rollout/rollback, security/operational review, exception, and retirement criteria. Monitor after release for unknowns, old paths, errors, latency, retries, and business parity.

## Definitions and Notation

Let baseline behavior be $b$, candidate behavior $c$, supported coexistence set be $H$, and justified assumption set for scenario $h$ be $A_h$. Let $O_b(h)$ and $O_c(h)$ be complete observations/effects under baseline and candidate. A breaking counterexample is $(h,a)$ such that $a(O_b(h))$ holds but $a(O_c(h))$ does not.

Let $U$ be observed unique supported consumers, $M$ confirmed migrated consumers, and migration coverage $m=M/U$ only when inventory $U$ is itself credible. Let $D$ be dual-produced occurrences and $P$ parity matches; parity ratio $p=P/D$ describes observed equality under a defined comparator but cannot prove semantic correctness by itself.

An **old path** is any deprecated input/output/operation/state behavior retained during migration. A **contract gate** is an automated or manual check tied to a declared compatibility dimension. A **breaking budget** is not permission to break silently; it is a governance mechanism for weighing necessity, affected population, mitigation, and migration cost.

## Mechanisms, Invariants, or Proof Structure

**Counterexample rule.** Compatibility is universally quantified over the supported horizon; therefore one valid supported scenario whose justified assumption becomes false proves the candidate breaking for that claim. Absence of a found counterexample is only as strong as the modeled horizon and assumptions.

**Additive-shape counterexample.** Adding optional `pageSize=100` to an endpoint that previously returned all 800 items changes old clients' omitted-input result from 800 to 100. The schema set expanded, yet completeness semantics contracted. Thus syntactic addition does not imply behavioral compatibility.

**Expand–migrate–contract invariant.** During expansion, old and new representations map to one canonical meaning with deterministic conflict policy; during migration, every occurrence/effect remains singular and parity/reconciliation is observable; contraction occurs only after old dependencies and rollback/recovery horizons end. Violating any stage can corrupt or strand mixed-version state.

**Evidence limitation.** If $M=U$, measured migration coverage is 100%, but an incomplete $U$ omits dormant/unknown consumers. Usage ratio proves retirement only when inventory construction, observation window, failover/replay/partner coverage, and false-negative controls are justified.

Operational invariants are: semantic delta explicit; additive separated from compatible; supported counterexamples searched; defaults preserve old behavior; reachable variants safe; state/rollback included; dual paths converge on one effect; contraction evidence-based; exceptions honest; and gates tested with known breaks.

## Alternatives and Trade-Offs

Preserving the old surface minimizes consumer disruption but adds code, schema, documentation, security exposure, and test burden. Immediate replacement simplifies the provider but transfers coordination and outage risk to consumers. Expand–migrate–contract buys safety with temporary complexity.

Parallel fields are easy to discover but bloat contracts and create precedence conflicts. New operations/types isolate meaning but fragment usage and lifecycle. Negotiation avoids blanket exposure but complicates caches, routing, downgrade security, and testing.

Strict schema-diff blocking is fast and consistent but over/under-classifies semantics. Manual review catches meaning but can be inconsistent and slow. Combine encoded policy, domain scenarios, consumer evidence, and accountable exceptions.

Treating observed behavior as contract protects consumers but can fossilize bugs. Treating only documentation as contract enables correction but can surprise real production. Weigh reasonableness, duration, prevalence, harm, security, and migration path explicitly.

Dual write speeds migration but introduces divergence and double-effect risk. On-read translation avoids background rewrite but adds tail latency and may leave cold data untested. Offline backfill is measurable but operationally heavy. Select based on authority, volume, correctness, and rollback.

Major versions make breaks visible but multiply maintenance and do not solve data/state migration. Compatible additive evolution keeps one ecosystem but cannot preserve genuinely different semantics forever.

## Failure Modes and Misconceptions

- “Green diff means compatible.” It covers only encoded structural rules.
- “Additive means safe.” Defaults, output variants, size, cost, and semantics can break.
- “Optional means harmless.” Omission behavior may change.
- “New enum value is additive.” Old exhaustive readers can fail or choose unsafe defaults.
- “Loosening validation cannot break.” It can create unreadable state or abusive cost.
- “Longer IDs are compatible.” Client storage, buffers, URLs, and signatures may be bounded.
- “Error additions are safe.” Old retry/fallback logic may not handle them.
- “Bug fixes are never breaking.” Supported observed behavior may change materially.
- “Security urgency makes it non-breaking.” It justifies an exception, not a false label.
- “A new version solves migration.” Consumers, state, auth, and operations still coexist.
- “Dual write guarantees parity.” Partial failure/order/retry can diverge or duplicate effects.
- “Deprecated means removable.” Usage, dormant/recovery, agreement, and horizon evidence remain.
- “No current traffic means unused.” Offline, batch, partner, failover, and replay paths may be dormant.
- “One adapter can translate anything.” New semantics may be lossy or impossible to downcast.
- “Successful HTTP response proves no break.” Silent wrong data/effects are worse.
- “Only schemas are public.” SDK symbols, limits, timing, errors, and behavior are public too.
- “Patch release means safe.” A version label reports classification; it cannot make a break compatible.

## Worked Examples

### Example 1

`pageSize` is added as optional with default 100 to an endpoint that returned all 800 items. Old clients omit it and see a syntactically valid 100-item response without paging. The additive schema delta is a breaking completeness/default change.

### Example 2

Response field `riskBand` is added. Four clients ignore unknown properties; one partner validates `additionalProperties: false` and rejects the payload. The field is not compatible with the declared five-consumer horizon until negotiation or partner migration.

### Example 3

Response enum gains `PENDING_REVIEW`. An old payment client maps unknown values to `FAILED` and retries, risking duplication. Deploy an explicit unknown/quarantine path and idempotent outcome lookup before enabling the new value.

### Example 4

Identifier maximum grows from 32 to 64 characters. Of 12 known consumers, two store `VARCHAR(32)`. Provider validation became looser, but new output would truncate downstream. Introduce a parallel opaque identifier/migration or retain the old bound.

### Example 5

An endpoint changes `409 version_mismatch` to `503 unavailable`. A client retries up to three times, turning one permanent conflict into four attempts. Same response schema, breaking error and operational behavior.

### Example 6

`weight` remains a JSON number but changes kilograms to grams. Old code multiplies by 1,000 again. Add `weightGrams`, retain `weightKg`, specify precedence, migrate readers/writers, compare values, then retire the old field.

### Example 7

New server writes workflow state `REVIEWING`; rollback server only reads `OPEN`/`CLOSED`. Request/response diffs pass, but rollback breaks. Keep emission gated until all rollback artifacts read `REVIEWING`, or define roll-forward recovery.

### Example 8

A GraphQL object gains field `displayName`; existing operations do not select it, so their result shape is unchanged. Removing deprecated `fullName`, however, invalidates 37 observed persisted queries. Addition and removal are separate deltas with separate classification and retirement evidence.

### Example 9

A migration dual-publishes old/new webhooks for 10,000 occurrences. Comparator finds 9,998 parity matches, so $p=9{,}998/10{,}000=99.98\%$. The two mismatches block contraction; even 100% observed parity would still require complete consumer/side-effect and horizon evidence.

### Example 10

Inventory lists 40 consumers and 38 confirmed migrations, so $m=38/40=95\%$. The remaining two are a quarterly billing job and disaster-recovery tool. Recent traffic would show 100% on the new path, but contraction would break dormant critical consumers.

## Cross-Program Connections

[Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md) supplies adapters, strangler transitions, independent deployability, and expand–migrate–contract boundaries.

[Database Engineering](../../18-database-engineering/ROADMAP.md) provides online schema change, dual read/write, backfill, checksums, constraints, rollback, and state compatibility.

[Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) covers mixed versions, idempotency, duplicate effects, partial failure, replay, and state-machine evolution.

[Security Engineering](../../25-security-engineering/ROADMAP.md) governs validation, auth/scope changes, disclosure, downgrade resistance, urgent fixes, and exception risk.

[Systems Engineering](../../26-systems-engineering/ROADMAP.md) connects configuration baselines, interface deltas, change control, transition-state integrity, evidence, and supplier impact.

[Platform Engineering](../../29-platform-engineering/ROADMAP.md) owns schema/source diff gates, consumer inventory, SDK generation, rollout controls, telemetry, waivers, and deprecation automation.

## References

1. Google, [AIP-180: Backwards Compatibility](https://google.aip.dev/180).
2. Protocol Buffers, [Language Guide (proto3): Updating a Message Type](https://protobuf.dev/programming-guides/proto3/).
3. GraphQL Foundation, [GraphQL Specification, October 2021](https://spec.graphql.org/October2021/).
4. IETF, [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html).
5. JSON Schema, [JSON Schema Core, Draft 2020-12](https://json-schema.org/draft/2020-12/json-schema-core).
6. Microsoft, [Azure REST API Guidelines](https://github.com/microsoft/api-guidelines/blob/vNext/azure/Guidelines.md).
7. Semantic Versioning, [Semantic Versioning 2.0.0](https://semver.org/).

## Exercises

### Exercise 1

Classify a proposal that adds optional request `includeHistory`, response enum `reviewState`, new `429` errors, doubles identifier length, and tightens date validation. For each, give a breaking counterexample and safe delivery pattern.

### Exercise 2

Design expand–migrate–contract for renaming `amountCents` to `amountMinorUnits` while adding explicit currency exponent, across REST, events, stored state, SDKs, retries, rollback, and replay.

### Exercise 3

A team claims a pagination change and faster eventual-consistency response are internal implementation improvements. Build behavioral tests and decide when they are breaking.

### Exercise 4

Define a compatibility exception process for an urgent authorization vulnerability that requires rejecting previously accepted requests and adding a new error. Preserve as much safe traffic as possible.

### Exercise 5

Create a change gate and mutation suite covering OpenAPI/JSON, Protobuf, GraphQL, generated SDKs, semantic defaults/errors/limits, operational envelopes, candidate-written state, consumer evidence, and contraction.

## Answers to the Exercises

### Answer 1

`includeHistory` is compatible for old clients only if omission preserves old results/cost and new clients do not send it to old servers; gate/opt in. `reviewState` can break exhaustive old readers; deploy unknown handling before emission or negotiate a new representation. New `429` can break clients that treat the prior outcomes differently or retry unsafely; define stable retry guidance, update tolerant readers, and canary. Longer IDs can overflow stores/URLs/signatures; retain the bound or migrate consumers via a parallel opaque ID. Stricter dates reject formerly valid requests; inventory actual forms, accept/canonicalize both during migration, then contract or govern a justified security/correctness exception. Test state and rollback for all new values.

### Answer 2

Expand by adding `amountMinorUnits` plus `currencyExponent`, retaining `amountCents`, and mapping both to one canonical money type. Define exact conflict rejection and never infer exponent from mutable current data. SDKs expose new fields without removing old symbols. Events publish one occurrence/effect with both fields or a new explicit type; replay retains original evidence. Stored rows add new columns/representation; backfill deterministically with checksums. Deploy all readers, including rollback, before new writes; preserve idempotency keys across both forms. Migrate clients/producers gradually and compare values/effects. Contract only after consumers, archives, backups, rollback artifacts, and replay tools no longer require cents, then reserve/retire old schema identifiers.

### Answer 3

Fixture the old collection's completeness, page boundaries, order, duplicates, count, cursor, and omission behavior. If an old client that omits paging now receives a partial set, the change is breaking even if latency improves. For the consistency change, create write-then-read histories across resource/list/search/cache; if the faster response returns data older than the promised floor or changes pending/error to stale success, it is breaking. If both changes stay inside documented semantics and operational bounds for every supported cell, they can be internal. Compare tail latency, response size, retries, and goodput so a nominal speedup does not shift cost or failure behavior.

### Answer 4

State plainly that previously accepted unsafe requests will now be rejected. Identify the smallest vulnerable shapes/tenants/operations and add a narrowly scoped server guard with stable machine error, remediation link, and correlation. Avoid disabling the whole API if safe requests can continue. Notify owners and security/legal/support channels; provide client validation/migration tooling where disclosure is safe. Canary or staged-enforce if the threat permits, but do not retain an exploitable path for compatibility. Monitor rejects, affected versions, false positives, attacks, and business effects. Record approver, rationale, scope, effective time, exception/communication, follow-up contract change, and removal of temporary controls.

### Answer 5

Pin exact baselines and run format-specific structural diffs, serializer/unknown round trips, and old/new generated-source compilation. Add behavioral fixtures for omission/null/default, enums/unions, errors/retryability, ordering/pagination, units/formats/limits, auth, idempotency/effects, latency/size/quota, and rollback reading candidate state. Execute consumer/provider contracts plus provider invariants and usage/state evidence. Mutation tests intentionally remove/rename fields, add required input/unknown output variants, change defaults/status/type/limits/order, discard unknowns, broaden disclosure, and write unreadable state; each must trip a named gate. Contraction additionally requires credible inventory, dormant/partner/recovery/replay coverage, parity/reconciliation, expired rollback/backup horizons, and scoped approval for any exception.
