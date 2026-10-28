---
module_id: API-081
program: API & Service Engineering
level: 2
module_number: 81
title: Backward and Forward Compatibility
status: complete
last_verified: 2026-09-02
---

# Backward and Forward Compatibility

## One-Page Review

### Governing question

Which old and new clients, servers, intermediaries, stored representations, and generated libraries can coexist, in which direction, for which operations and states, without losing wire validity, source/runtime usability, meaning, security, or operational safety?

### Essential definitions

- **backward compatibility** generally means a new reader/implementation can consume or serve an older writer/client contract.
- **forward compatibility** generally means an old reader/implementation can tolerate a newer writer/server contract.
- **full compatibility** requires both directions for the governed version sets.
- **transitive compatibility** compares a candidate with every supported historical version, not only its immediate predecessor.
- **wire compatibility** preserves encoding, parsing, routing, and protocol exchange.
- **source/binary compatibility** preserves compilation, generated APIs, linking, and runtime loading.
- **semantic compatibility** preserves the decisions and effects a reasonable supported consumer is entitled to make.
- A **compatibility horizon** is the oldest/newest client, server, schema, state, or replay version the provider promises to support.

### Central model, mechanism, or theorem

Let $C_i$ be client version $i$, $S_j$ server version $j$, $o$ an operation, $x$ a reachable resource/system state, and $K(C_i,S_j,o,x)$ the conjunction of request acceptance, response interpretation, source/runtime usability, semantic preservation, security, and operational bounds. A rollout is compatible only if

$$
\forall (i,j,o,x)\in H_{coexist},\quad K(C_i,S_j,o,x)=true,
$$

where $H_{coexist}$ includes rollout, rollback, retries, caches, stored state, delayed messages, and disaster paths—not merely the latest client talking to the latest server.

### Critical invariants

Compatibility is always directional, scoped, and evidence-backed. Request and response directions are checked separately because each side alternates writer and reader roles. Old clients retain old defaults, effects, errors, ordering, cardinality, limits, and security outcomes. New clients remain safe during server rollback only when that pairing is promised.

Unknown fields and enum values have explicit policy; tolerant reading never authorizes unknown input or hides typos. New servers can read all supported old state, and any rollback server can read or safely reject state written during rollout. Intermediaries, SDKs, validators, caches, webhooks, batch jobs, and partner clients are part of the matrix. Structural checks are necessary but cannot prove semantics or operations.

### Common failures

Calling every additive schema change safe; adding a required request field; making an omitted option default differently; returning a new enum to an exhaustive old client; removing a response field still used; changing error/status/retry semantics; adding pagination but making old clients see only the first page; widening identifiers beyond stored columns; tightening validation on previously accepted values; changing ordering, units, null/absence, precision, or authorization; rejecting unknown response fields; blindly ignoring unknown command fields; losing Protobuf unknowns through JSON; latest-to-latest testing only; rollout state unreadable after rollback; and assuming documentation or a version number creates compatibility.

### Compact example

A new server adds optional request field `includeArchived`. Old clients omit it. If omission preserves the old behavior—exclude archived records—the new server can read old requests. But if the new default includes archived records, the wire still parses while results and authorization exposure change. Meanwhile an old response DTO configured to reject unknown fields can fail when the server returns `archiveReason`. **Conclusion:** an “optional field addition” is compatible only after both request and response directions plus semantics are tested against actual consumers.

### Connections

[Protocol Buffers and Schema Evolution](052-protocol-buffers-and-schema-evolution.md), [GraphQL Schema Design](055-graphql-schema-design.md), and [Event Schema Design](062-event-schema-design.md) provide format-specific mechanics. [Event Versioning](069-event-versioning.md) covers retained asynchronous data. The next modules classify changes, choose versions, govern deprecation, and gather consumer evidence.

## Governing Question

For every version pair that can meet during deployment, rollback, replay, caching, failover, or long-lived client use, what exact compatibility dimensions must hold, and what evidence proves the old justified behavior remains safe?

## Why This Matters

An API is a contract distributed into software the provider may not control. Mobile applications update slowly; browser tabs remain open; partners deploy quarterly; generated SDKs embed types; batch jobs wake rarely; gateways validate cached schemas; messages and webhooks arrive late; disaster recovery restores older artifacts. “We deployed both sides together” is rarely a durable assumption.

Compatibility is not one property. Bytes can parse while generated code no longer compiles. Source code can compile while a new enum reaches an exhaustive switch. A response can preserve fields while changing ordering, units, error codes, latency, or authorization. A new server can work with an old client, yet a rollback to the old server can fail after the new client or server wrote new state.

Direction is often confused. In a request, the client is writer and server is reader; in a response, the server is writer and client is reader. “The API is backward compatible” therefore hides at least two relations. A safe rollout may also require new-client/old-server support, whereas a public API might explicitly promise only old-client/new-server compatibility.

Compatibility enables independent delivery only when its horizon and evidence are real. Excessive promises can freeze design forever; vague promises externalize migration cost to consumers. The engineering task is to define supported populations and behavior precisely, design for evolution, verify every coexistence path, and route genuine breaks through explicit migration and lifecycle governance.

## Prerequisites and Retrieval

Retrieve [Content Negotiation](005-content-negotiation.md), [Error Translation](035-error-translation.md), [Filtering, Sorting, and Pagination](017-filtering-sorting-and-pagination.md), [Idempotency Keys](037-idempotency-keys.md), [Protocol Buffers and Schema Evolution](052-protocol-buffers-and-schema-evolution.md), [GraphQL Schema Design](055-graphql-schema-design.md), [Event Schema Design](062-event-schema-design.md), [Event Versioning](069-event-versioning.md), and [Consistency and Read-After-Write Expectations](079-consistency-and-read-after-write-expectations.md).

Retrieve the normative API descriptions and historical baselines; actual serializers/deserializers and validators; generated SDK artifacts and compiler/runtime versions; active client/server/intermediary inventory; routes, media types, headers, status and error codes; defaulting and validation behavior; persisted representations and migration state; caches and signatures; webhooks/events/replay horizons; partner contracts; deployment/rollback/failover procedures; usage evidence; support/stability policy; and incident history involving contract drift.

## Learning Objectives

After completing this module, you can:

1. state backward, forward, full, and transitive compatibility without reversing reader/writer direction;
2. construct request, response, client/server, state, and intermediary coexistence matrices;
3. separate wire, source, binary/runtime, structural, semantic, operational, security, and temporal compatibility;
4. define a finite compatibility horizon from actual lifecycle and support obligations;
5. reason about defaults, absence, unknown fields, enums, validation, errors, ordering, limits, and pagination;
6. evaluate JSON/HTTP, Protocol Buffers/gRPC, GraphQL, webhooks, and generated SDK surfaces;
7. preserve rollback and disaster compatibility with state written during mixed-version operation;
8. choose tolerance, strictness, negotiation, adapters, and capability discovery without hiding defects;
9. build automated and empirical compatibility evidence across real supported consumers; and
10. make a scoped compatibility claim with explicit exceptions, migration, telemetry, and retirement criteria.

## Core Exposition

### State direction as a sentence

Avoid using “backward” or “forward” alone. Say: “the new server accepts requests from clients released since January,” “the old mobile client safely interprets responses from the new server,” or “the candidate reader consumes every retained writer schema.” The sentence identifies writer, reader, direction, horizon, and surface.

For a synchronous call, split the exchange:

- request: client $C_i$ writes and server $S_j$ reads;
- response: server $S_j$ writes and client $C_i$ reads;
- effect: both must agree on command semantics, state transition, idempotency, and errors; and
- future operations: state written by the pair must remain readable by supported later/rollback pairs.

Common API guidance calls old-client/new-server support backward compatibility. Data-schema guidance often calls a new reader consuming old writer data backward compatibility and an old reader consuming new writer data forward compatibility. These are consistent only after roles are explicit.

Do not infer symmetry. A new server may accept old requests while its richer response breaks old clients. An old server may reject a new optional request field even though the new server handles old clients. Declare each promised cell.

### Define the compatibility horizon

No system supports all historical software forever by accident. Define supported client releases/SDK major versions, server rollback artifacts, API stability channel, media/schema versions, stored resource generations, event/webhook retention, intermediary versions, and geographic deployment lag. Include a time window only when time maps to identifiable versions.

The horizon comes from product obligations and operating reality: mobile adoption tails, partner agreements, offline devices, long-running jobs, regional rollout duration, rollback retention, backup age, and legal replay/audit needs. Preview/beta surfaces may promise less, but the reduced promise must be explicit before adoption.

Transitive compatibility matters when the horizon spans more than the immediately previous version. Passing $v_3$ against $v_2$ and $v_2$ against $v_1$ does not prove $v_3$ against $v_1$; defaults or fields can be added and later removed while adjacent checks pass.

Retirement shrinks the horizon only with evidence that affected consumers/state are gone or migrated. Calendar age and “no one complained” are not inventory.

### Build the coexistence matrix

List client versions on one axis and server versions on the other. Mark which cells can occur during steady state, rollout, rollback, region skew, failover, or customer lag. For each cell, enumerate operations and reachable states. Add intermediaries where they transform/validate messages.

If four supported clients can meet three server artifacts across two critical operations, there are $4\times3\times2=24$ client-server-operation cells before state, media type, and intermediary variants. Risk-based selection can reduce executions, but not by silently deleting promised cells. Pairwise/property techniques complement fixtures for large dimensions.

Build separate writer-reader matrices for persisted schemas, cached representations, webhooks, and events. A client-server table cannot prove that a rollback server reads a resource created by the candidate or that a restored consumer reads a delayed webhook.

Record unsupported cells explicitly with negotiation or a stable error. Accidental partial behavior is worse than an honest incompatibility because consumers may commit state before discovering the mismatch.

### Separate compatibility dimensions

**Wire compatibility** covers method/path, framing, media type, encoding, field/tag representation, parsing, routing, and protocol rules. **Structural compatibility** covers required/optional fields, types, constraints, and schema resolution. These establish that messages can be exchanged.

**Source compatibility** asks whether consumer source written against an old SDK compiles against a new SDK. **Binary/runtime compatibility** asks whether already-compiled code links, loads, reflects, serializes, and runs. Package moves, method signature changes, generated naming, dependencies, and runtime upgrades can fail without a wire break.

**Semantic compatibility** asks whether valid old assumptions remain true: meaning, units, defaults, cardinality, ordering, identity, lifecycle, side effects, consistency, and error decisions. Google AIP-180 explicitly distinguishes source, wire, and semantic compatibility and warns that visible behavior can break consumers even when syntax survives.

**Operational compatibility** covers documented sizes, latency/deadline feasibility, pagination, quotas, rate limits, retryability, concurrency, streaming behavior, and resource cost. **Security compatibility** covers authentication, authorization, privacy, signatures, redaction, and threat controls. **Temporal/state compatibility** covers persisted data, caches, tokens, in-flight operations, replay, rollout, rollback, and disaster restoration.

A release claim names every applicable dimension. “Schema diff passed” means only what that tool and rule set actually checked.

### Preserve old behavior when requests omit additions

Adding an optional request field helps evolution only if omission preserves the old behavior for every supported client. The default is an API semantic, not merely the serializer's zero value. Document it and test absence separately from explicit false, zero, empty, and null.

A new required request field is incompatible with old writers. Making a formerly optional field required also rejects previously valid messages. If the new information is essential, derive it safely, negotiate a capability/new operation, or introduce a new major contract and migration.

New validation can break old callers: tighter ranges/patterns, normalized identifiers, forbidden combinations, smaller payload limits, mandatory headers, changed timestamp rules, or newly rejected unknown fields. Security corrections can justify a break, but urgency does not make the change compatible; use exception governance and communication.

Request tolerance must be deliberate. Ignoring arbitrary unknown command fields can hide misspellings such as `transferAmout`, create false belief that a control applied, and later change behavior when the server learns the field. Strict commands can coexist with extensibility through declared extension containers, capability negotiation, or versioned schemas.

### Make responses safe for old readers

Response additions are safe only if old clients actually tolerate them. Many JSON parsers ignore unknown properties, but closed schemas, generated DTOs, signature/canonicalization, validation gateways, exhaustiveness checks, and hand-written mappings may reject or lose them. Test real clients rather than invoke a generic JSON rule.

Existing response fields cannot disappear, become conditionally absent, change nullability/presence, or stop being populated within a promise that old clients rely on. Renaming is remove-plus-add. Keep the old field with defined precedence during migration, then retire it through lifecycle evidence.

Changing field format, maximum length, unit, precision, timezone, identity authority, or construction algorithm can break downstream storage and parsing while type remains `string` or `number`. AIP-180 treats visible format and string-bound changes as compatibility concerns for this reason.

Avoid returning new enum/union variants unless the contract declared the set extensible and supported readers have unknown handling. “Unknown” must not silently map to an unsafe known state. Preserve raw value where forwarding or later recovery matters.

### Treat absence, null, and defaults as values

Absence can mean unspecified, inherited, unknown, not computed, redacted, or no change. Null can mean cleared, missing, inapplicable, or unknown. Zero/empty can be a real value. Collapsing these states during evolution changes commands and patches.

For every added field, specify old-writer/new-reader behavior and new-writer/old-reader behavior. A new reader of old data needs an honest default/absence representation. An old reader of new data must ignore/preserve the field only if its decision remains safe without it.

Changing whether a default-valued field is serialized can break presence-sensitive consumers and signatures. AIP-180 calls this out directly. Canonicalization, ETags, hashes, cache keys, and patch/diff logic require tests when representation presence changes.

Never backfill a convenient current value as historical truth. If old resources lack `taxJurisdiction`, “current customer jurisdiction” may be wrong for a past order. Represent unknown or migrate from authoritative evidence.

### Keep enums and variants open where evolution requires it

An enum used only as closed request input can reject unknown values safely, while an enum returned by the server often needs an unknown/future case. Generated languages differ: some preserve numeric unknowns, some create sentinel values, and exhaustive source switches can fail compilation or runtime.

Adding a variant changes the set of reachable states. Old clients that default unknown payment state to `FAILED` may retry a committed payment; clients that default unknown authorization decision to allow create a vulnerability. Define fail-safe, quarantine, display, retry, and preservation behavior by domain.

Protobuf binary guidance permits many additive fields and enum values on the wire, but explicitly notes application/source risks. Preserve field numbers, reserve removed numbers/names, and test binary, ProtoJSON, generated source, and unknown-field round trips separately. Converting through JSON or field-by-field copy can discard unknown Protobuf fields.

For GraphQL, clients select response fields, so adding an object field normally does not change existing result shapes. Removing a selected field invalidates documents/persisted queries. Use schema deprecation metadata and observed operation usage before removal. Adding enum/union possibilities still affects exhaustive client logic.

### Preserve HTTP and error semantics

Method safety/idempotency, status codes, redirects, cache directives, validators, headers, media types, and problem/error identifiers are contract. Changing `404` to `200 null`, `409` to retryable `503`, or synchronous `201` to `202` changes client control flow even if payload schema is additive.

RFC 9110 supports HTTP extensibility by requiring proxies to forward most unrecognized fields and recommending recipients ignore unrecognized header/trailer fields. That protocol rule does not mean an application should ignore arbitrary unknown JSON commands, nor does it make a new field's semantics safe.

Stable machine-readable error code/type matters more than mutable prose. Preserve retryability, idempotency outcome, authorization disclosure, and correlation semantics. Adding a new documented error can be breaking if old clients assumed it was unreachable and cannot act safely.

Content negotiation is a compatibility mechanism only when supported representations are independently governed. Send `Vary` correctly, keep cache keys distinct, return stable unsupported-media outcomes, and do not change an existing media type's meaning silently.

### Protect collections, ordering, and limits

Adding pagination after an endpoint returned the complete collection can be semantically breaking: old clients may treat the first page as the whole set. AIP-180 uses this kind of default-behavior problem as an example. Introduce a new operation/version or preserve the old default within a safe bounded horizon and migrate consumers.

Changing default sort, tie-breaker, duplicate behavior, filtering, case/locale/collation, consistency, or snapshot semantics changes results without a schema diff. Adding items or new resource subtypes can expose exhaustiveness assumptions.

Widening documented string/identifier/array limits can break client databases, UI, signed buffers, or downstream APIs even though the provider accepts more. Tightening limits rejects previously valid requests. Record min/max/cardinality and test boundary values across clients.

Operational compatibility also includes response size and latency. Adding eagerly populated fields can exceed mobile bandwidth or gateway limits. New server-side work can exceed old client timeouts and trigger retries. Prefer explicit selection/expansion with preserved defaults and measured budgets.

### Include generated SDKs and intermediaries

Generated SDKs create another public surface: packages/modules, class and method names, overloads, optionality, async/paging abstractions, exceptions, dependencies, minimum runtimes, and serialization behavior. A wire-safe schema move can change imports or generated symbols; Google guidance notes that moving Protobuf definitions between files can break generated source even when the wire stays valid.

Gateways, WAFs, schema validators, proxies, meshes, caches, signing middleware, and adapters can reject, strip, reorder, normalize, or transform new information. HTTP header extensibility can fail if a configured intermediary blocks it. Contract tests must traverse representative production paths.

Read-modify-write clients are especially dangerous. An old client reads a new representation, drops unknown fields, and writes the reduced object back. Use PATCH/field masks, preservation-capable serialization, server-owned/output-only fields, and concurrency preconditions.

Client libraries should not silently paper over server incompatibility by retrying a different operation or dropping rejected fields unless that adapter is a governed semantic translation. Observe fallback use and retire it deliberately.

### Design tolerance without permissiveness

The robustness principle—be liberal in what you accept—can aid extension but can also create ambiguity, security bypasses, and divergent implementations. Be precise about what is extensible. Ignore unknown response metadata when safe; reject unknown money-transfer command fields; preserve unknown protocol fields when forwarding; quarantine unknown safety-critical variants.

Define closed versus open sets at every extension point. Namespaced extension maps need ownership, type/size limits, authorization, collision rules, privacy classification, signing behavior, and forwarding policy. Extension data must not mutate core behavior without negotiated semantics.

Readers should accept all documented historical representations, not malformed near-misses. Writers should emit one canonical form. Broad multi-form input can be a migration adapter with telemetry and removal criteria; indefinite ambiguity makes security and testing harder.

Tolerant behavior is compatible only if it preserves meaning. Silently clipping an oversized amount or mapping an unknown role to administrator achieves parse success by violating the contract.

### Preserve state compatibility and rollback

Mixed-version servers often share databases, caches, object stores, queues, and tokens. Candidate code may write a new state, enum, encoding, index assumption, encryption format, or workflow transition that the rollback artifact cannot read. API compatibility therefore includes expand/migrate/contract data evolution.

Before rollout, test old server reading state written by new server for every reachable candidate feature. If impossible, gate new writes until rollback is no longer needed, use dual-readable encoding, deploy a forward-compatible old reader first, or define roll-forward recovery. Do not claim ordinary rollback when state makes it unsafe.

Long-running operations and idempotency records cross releases. A retried old request must find the same result after upgrade; a rolled-back server must not duplicate an effect because it cannot parse the candidate's record. Tokens/cursors/cache entries either remain valid through the horizon or fail with a stable restart/migration outcome.

Backups extend the state horizon. Restoring old data into new code and new data into retained disaster artifacts needs explicit compatibility or migration. Schema catalogs and encryption keys are part of the recovery set.

### Sequence deployment and rollback

For a compatible additive capability, deploy readers/tolerant consumers first, verify them, then enable writers/producers. During server rollout, route old clients through both old and new servers in tests/canaries. During client rollout, remember new clients can hit old regions/servers unless routing or negotiation prevents it.

Feature flags should suppress emission/use, not redefine the same field unpredictably. Capabilities can be negotiated explicitly, but a client-supplied version header is not proof that its whole behavior matches; treat it as one governed input.

Canary evidence covers response interpretation and side effects, not only HTTP success. Shadow safe reads; compare result semantics; use idempotent/simulated paths for commands. Rollback rehearsals include candidate-written state and in-flight operations.

Regional, cache, registry, and CDN propagation create coexistence beyond the deployment scheduler's view. Keep compatibility until evidence shows all paths converged and rollback retention expired.

### Verify the matrix in layers

Start with schema/spec diff rules mapped to the actual format and policy. Run serializer round trips, unknown-field/enum preservation, generated-source compilation, binary/runtime loading, and old/new SDK integration. Use golden requests/responses/errors/tokens for supported versions.

Then test semantics: omitted/default/null fields, boundary values, ordering, pagination completeness, side effects, idempotency, authorization, retry decisions, consistency, and performance budgets. Run both directions for each promised cell and include malformed/adversarial inputs so tolerance does not become permissiveness.

Consumer/provider contract tests provide evidence for known expectations, but they are incomplete if consumers are unregistered or tests omit behavior. Production traffic replay/shadowing, SDK telemetry, gateway logs, deprecation signals, and support inventory reveal actual use. Protect sensitive payloads and avoid equating absence of observed traffic with proof of no consumer.

Mutation testing should deliberately remove/rename fields, add variants, change defaults/status/order/limits, strip unknowns, and write candidate-only state; gates should fail. A compatibility system never tested with known breaks may be ceremonial.

### Make claims and exceptions auditable

Record candidate and baseline artifacts, horizon, matrix cells, dimensions, tools/rules, fixtures, semantic decisions, consumer evidence, state/rollback result, performance/security review, exceptions, and approvers. Say “wire-compatible for Protobuf binary between v4 and v5” rather than “backward compatible.”

Compatibility exceptions can be necessary for a vulnerability, legal rule, corruption risk, or unsustainable legacy. Classify the change honestly as breaking, narrow its scope, communicate, offer migration/adapter where safe, monitor impact, and establish removal/support dates. Security need changes priority, not vocabulary.

Track unknown-field/enum encounters, validation failures, old/default path use, error/status distribution, negotiation failures, SDK/client versions, deprecated operation use, state-read failures, and rollback/canary outcomes. Compatibility is an ongoing service property until the horizon retires.

## Definitions and Notation

Let $C_i$ and $S_j$ denote client and server artifacts. Let $W_i$ and $R_j$ denote a writer and reader for one message/state surface. Let $o$ be an operation, $x$ a reachable state, and $K(C_i,S_j,o,x)$ a compatibility predicate spanning declared dimensions. Let $H_{coexist}$ be all supported tuples that can meet.

For reader/writer schemas, backward compatibility of candidate reader $R_n$ over historical writer set $H_W$ requires $K(R_n,W_i)$ for every required $W_i\in H_W$. Forward compatibility of an old reader $R_i$ with candidate writer $W_n$ requires $K(R_i,W_n)$. Full is their conjunction; transitive expands the baseline beyond $n-1$.

A **baseline** is the governed artifact/set against which a candidate is checked. A **compatibility cell** is one version/operation/state pairing. An **extension point** is an explicitly open part of a contract. An **unknown** is syntactically valid data the current reader does not define. A **semantic default** is the contract behavior for absence, independent of language zero values. An **adapter** translates between explicitly understood contracts.

## Mechanisms, Invariants, or Proof Structure

**Direction decomposition.** For a request/response exchange, compatibility requires both new-server reading old-client request and old-client reading new-server response, plus preserved effect semantics. Proving only one direction is insufficient because writer/reader roles reverse at the response boundary.

**Adjacent-version counterexample.** Let $v_1$ contain optional field $a$, $v_2$ add replacement $b$ while retaining $a$, and $v_3$ remove $a$. Adjacent checks can accept $v_2$ versus $v_1$ and $v_3$ versus $v_2$ under selected rules, while a $v_1$ consumer cannot read the required meaning from $v_3$. Therefore adjacent compatibility is not transitive without a transitive rule or retained adapter.

**Structural/semantic counterexample.** A request adds optional Boolean $includeArchived$ and remains structurally decodable when absent. If absence changes from excluding to including archived records, the old client's observed result and possibly authorization exposure change. Structural compatibility cannot prove semantic compatibility.

**Rollback-state argument.** Even if every old request works against the new server, rollback is unsafe when the new server writes reachable state outside the old server's read domain. Safe rollback requires the candidate's write domain be a subset of the old reader's valid domain, an adapter/migration exists, or new writes remain gated until rollback is relinquished.

Operational invariants are: direction and horizon explicit; all promised coexistence cells covered; wire/source/semantic/operational/security/state dimensions separated; omissions preserve old behavior; unknowns governed; state and rollback safe; intermediaries/SDKs included; and every claim tied to reproducible evidence.

## Alternatives and Trade-Offs

Indefinite backward compatibility minimizes forced client work but accumulates old semantics, code paths, test matrix, and security/support cost. A bounded published horizon enables change but requires accurate inventory, deprecation, migration, and enforcement.

Strict input validation catches typos and attacks but makes unplanned extensions fail. Tolerant readers ease evolution but can hide intent or discard unknowns. Use explicit open extension points and asymmetry: commands are often closed; responses/metadata may be safely open.

Additive coexistence avoids a major version but can create dual fields, precedence rules, response bloat, and long cleanup. A new version/type isolates semantics but duplicates operations and fragments consumers. Choose based on whether one coherent meaning can exist during the horizon.

Runtime negotiation supports heterogeneous capability but adds branches, cache variance, downgrade security, and observability needs. Static version pinning is simpler but increases version population and migration burden. Capability negotiation should describe concrete features, not substitute for contract testing.

Generated SDKs improve usability and compile-time checking but expand source/binary compatibility obligations across languages. Raw HTTP can be more tolerant yet moves parsing/semantic mistakes to every consumer. Govern both the wire and published libraries.

Transitive validation is safer for long horizons but costs more and can prevent removing ancient constraints. Snapshot/migration boundaries intentionally reset the historical set, but require preserved readers, transformed data, audit, and explicit consumer cutover.

## Failure Modes and Misconceptions

- “Backward compatible” is enough. Direction, surface, horizon, dimensions, and evidence are missing.
- “It parses, so it works.” Wire success says nothing about meaning, effects, or operations.
- “Adding is always safe.” Required inputs, defaults, enums, response strictness, size, and semantics can break.
- “Optional means compatible.” Omission must preserve old behavior; null/zero/empty are separate.
- “JSON readers ignore unknowns.” Actual validators, DTOs, signatures, and mappings may not.
- “Ignore every unknown request.” Typos and unrecognized security controls can become silent failures.
- “Protobuf says wire-safe.” ProtoJSON, generated source, enum logic, and semantics can still break.
- “Old client/new server passed.” Response direction, new-client/old-server, state, and rollback remain.
- “Latest against latest is representative.” Compatibility is a cross-version matrix.
- “Adjacent checks imply transitive compatibility.” Add-then-remove breaks older horizons.
- “No schema change means no API change.” Defaults, ordering, errors, limits, auth, and performance are contract.
- “A new error is harmless.” Client retry/fallback/user decisions may assume the old set.
- “Bigger limits help clients.” Stored columns, buffers, signatures, and downstream APIs may be bounded.
- “GraphQL additions are all safe.” New enum/union outcomes and changed resolver semantics still matter.
- “A feature flag guarantees rollback.” Candidate-written state or tokens can remain incompatible.
- “Version header proves capability.” It is a claim, not evidence of parser/behavior.
- “A security break is compatible.” It may be necessary, but remains a governed break.
- “No traffic means no consumer.” Dormant jobs, offline devices, failover, and partners may be invisible.

## Worked Examples

### Example 1

A new server adds optional request field `includeArchived`. Old clients omit it. When absence means the prior behavior—exclude archived—the request direction is compatible. When absence means include, the same wire-valid request changes result and authorization exposure, so semantic compatibility fails.

### Example 2

A response gains `archiveReason`. Three old clients ignore unknown JSON properties, but a fourth uses a closed validator and rejects the entire response. The change is not compatible with the promised four-client horizon until that client updates or the field is negotiated/versioned.

### Example 3

A server adds response enum value `PENDING_REVIEW`. An old client exhaustively maps `APPROVED` and `DENIED`, then crashes on anything else. The wire parser succeeds, but forward-read and semantic compatibility fail. An explicit unknown/quarantine path must ship before emission.

### Example 4

An endpoint formerly returned all 800 items. The new server defaults to 100-item pages, but the old client never follows `next`. It silently reports 100 as the total. Adding pagination reduced response size yet broke collection semantics; preserve the old behavior temporarily or use a new negotiated/versioned operation.

### Example 5

A conflict previously returned `409` with stable code `version_mismatch`; the candidate returns retryable `503`. An old client automatically retries and amplifies a permanent conflict. The payload still validates, but error decision and operational compatibility fail.

### Example 6

Documented resource IDs grow from at most 32 to 64 characters. The provider and JSON schema accept them, but a partner stores `VARCHAR(32)`. IDs truncate and later collide. A looser server constraint can be a breaking output change across the real consumer horizon.

### Example 7

During client-first rollout, new client $C_2$ sends optional `mode=precise` to old server $S_1$, which rejects unknown values. Old-client/new-server tests pass, but the $C_2/S_1$ rollback/region-skew cell fails. Capability gating prevents emission until all eligible servers support it.

### Example 8

New server $S_2$ writes workflow state `REVIEWING`; rollback server $S_1$ recognizes only `OPEN` and `CLOSED`. Requests were compatible, but rollback cannot load resources touched by $S_2$. Gate the state, deploy a tolerant $S_1$ reader first, or use roll-forward recovery.

### Example 9

A GraphQL schema deprecates `fullName` and adds `displayName`. Existing queries continue selecting `fullName`, so removing it immediately invalidates persisted documents. Keep resolving the deprecated field, observe operation usage, migrate clients, then remove only beyond the support horizon.

### Example 10

Four client releases can meet three server artifacts for two critical operations: $4\times3\times2=24$ cells. The team adds old/new persisted states and gateway validator versions as explicit dimensions, uses generated pairwise cases for broad coverage, and keeps full fixtures for money-moving and rollback cells.

## Cross-Program Connections

[Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md) governs published boundaries, adapters, independent deployability, and expand/migrate/contract structure.

[Database Engineering](../../18-database-engineering/ROADMAP.md) provides schema/data compatibility, online migration, dual-readable state, rollback, and backup restoration.

[Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) explains mixed versions, partial rollout, replay, idempotency, state machines, and failure recovery.

[Security Engineering](../../25-security-engineering/ROADMAP.md) governs strictness, downgrade resistance, authorization semantics, privacy changes, signatures, and urgent breaking exceptions.

[Systems Engineering](../../26-systems-engineering/ROADMAP.md) connects interface control, configuration baselines, compatibility matrices, suppliers, lifecycle horizons, and verification evidence.

[Platform Engineering](../../29-platform-engineering/ROADMAP.md) owns schema-diff gates, SDK generation, deployment/capability controls, contract telemetry, catalogs, and deprecation tooling.

## References

1. Google, [AIP-180: Backwards Compatibility](https://google.aip.dev/180).
2. Protocol Buffers, [Language Guide (proto3): Updating a Message Type and Unknown Fields](https://protobuf.dev/programming-guides/proto3/).
3. IETF, [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html).
4. GraphQL Foundation, [GraphQL Specification, October 2021](https://spec.graphql.org/October2021/).
5. JSON Schema, [JSON Schema Core, Draft 2020-12](https://json-schema.org/draft/2020-12/json-schema-core).
6. Microsoft, [Azure REST API Guidelines](https://github.com/microsoft/api-guidelines/blob/vNext/azure/Guidelines.md).
7. Microsoft Azure Architecture Center, [API Design for Microservices](https://learn.microsoft.com/en-us/azure/architecture/microservices/design/api-design).

## Exercises

### Exercise 1

Define the compatibility horizon and matrices for a public HTTP/JSON API with four mobile releases, two generated SDK majors, three deployable server artifacts, a gateway validator, 90-day idempotency records, and one-year backups.

### Exercise 2

Analyze a change adding optional request `currency`, response enum `settlementState`, and a longer payment ID. Classify request/response/source/semantic/operational/state risks and design a compatible rollout.

### Exercise 3

A three-version history adds field `b` in v2 and removes field `a` in v3 after migrating current clients. Explain why adjacent checks can pass but transitive compatibility fail, and define the required gate or migration boundary.

### Exercise 4

Design strictness and unknown-data policy for money-transfer commands, ordinary resource responses, HTTP extension headers, Protobuf relay messages, and GraphQL enum/union results. Include security and read-modify-write.

### Exercise 5

Create an evidence plan for rolling out a candidate server that changes pagination internals, error mapping, generated SDKs, persisted workflow state, and response timing without intending a public version change. Include rollback and exception handling.

## Answers to the Exercises

### Answer 1

Identify the four mobile artifacts and two SDK majors by actual serializer/runtime behavior, not labels; identify three current/rollback server artifacts and gateway schema versions. Build request, response, and effect cells for every pairing reachable through rollout, customer lag, region skew, and rollback. Add writer-reader tables for 90-day idempotency records and for every state/schema generation restorable from one-year backups; either current code migrates all of them or a preserved recovery reader does. Include media types, errors, operations, tokens/cursors, and intermediary transformations. Mark unsupported new-client/old-server cells with capability gating. The horizon ends only with mobile/SDK usage evidence, expired records, retired rollback artifacts, and backup migration/recovery proof.

### Answer 2

Old clients omit `currency`, so the new server needs an honest old semantic—perhaps derive the account's existing fixed currency only where unambiguous; otherwise the field cannot be merely optional. New clients must not send it to old servers without capability gating. `settlementState` requires unknown handling in old generated and hand-written clients before new values are emitted; unsafe default mapping is forbidden. Longer payment IDs can overflow storage, UI, signatures, and downstream providers, so survey/test the promised horizon and introduce a new opaque field/format migration if needed. Preserve idempotency/effect identity and database readability, deploy tolerant readers before writers, canary actual SDKs, and keep rollback from emitting/reading unsupported state.

### Answer 3

V2 can read/write `a` and `b`, so it coexists with v1; v3 can coexist with v2 if v2 already prefers `b`. But v1 does not know `b`, and v3 no longer carries `a`, so the v1/v3 cell fails. Compatibility is not automatically transitive. If v1 remains supported, gate v3 against every historical baseline and retain/derive `a`. Otherwise create an explicit migration boundary: inventory and migrate/retire v1 consumers and data, preserve an adapter for retained history if required, document the new baseline, and only then shrink the horizon.

### Answer 4

Money-transfer commands are closed: reject unknown fields with precise diagnostics so misspelled amounts or safety controls cannot be ignored; add negotiated/versioned extension points only with ownership and limits. Ordinary responses may allow unknown properties if actual clients ignore or preserve them safely; read-modify-write uses PATCH/field masks so old clients cannot erase new data. Follow RFC 9110 forwarding/ignore rules for unrecognized end-to-end headers while blocking hop-by-hop/security-sensitive fields as specified. Protobuf relays preserve unknown binary fields and avoid JSON/field-by-field loss. GraphQL clients request known fields, but enum/union results use an explicit unknown/future branch that fails safely. Never map unknown authorization/payment states to allow/success.

### Answer 5

Diff the normative contract and generated surfaces against every supported baseline, then compile/run old and candidate SDKs across the coexistence matrix. Fixtures assert pagination completeness/order/cursors, stable errors and retryability, omission/default/null behavior, authorization, idempotency, and timing within old deadlines. Load/shadow safe reads through the gateway and compare result semantics, first-attempt latency, response size, and error distribution. Write every candidate workflow state and prove rollback server reading/acting safely; rehearse in-flight operation and idempotency lookup across rollback. Canary by consumer/region with capability flags and observe versions/unknowns/deprecated paths. If security or correctness requires a break, label it, scope it, communicate/migrate, approve the exception, and monitor impact rather than weakening the compatibility claim.
