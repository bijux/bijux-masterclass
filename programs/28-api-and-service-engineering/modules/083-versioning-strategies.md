---
module_id: API-083
program: API & Service Engineering
level: 2
module_number: 83
title: Versioning Strategies
status: complete
last_verified: 2026-09-02
---

# Versioning Strategies

## One-Page Review

### Governing question

When incompatible API meanings must coexist, what exactly is versioned, how does a client select it, which guarantees are immutable versus updated in place, and how will routing, caches, SDKs, state, security, observability, migration, and retirement remain coherent?

### Essential definitions

- An **API version** identifies a governed contract lens: operations, representations, behaviors, and stability available to a client.
- A **major channel** such as `v1` is usually updated in place with compatible additions/fixes; incompatible meaning moves to another major version.
- A **snapshot version** is an immutable or compatibility-frozen dated/numbered contract selected explicitly.
- A **stability channel** such as alpha, beta/preview, or stable communicates lifecycle promises, not chronological order alone.
- **version scope** is the surface controlled by one identifier: service, interface, operation family, representation, schema, or event type.
- **version negotiation** resolves a client's explicit selector to one supported contract; it is not feature detection by guesswork.
- A **version adapter** maps a selected external contract to/from one canonical domain model while preserving its semantics.
- **version sprawl** is the multiplying code, test, documentation, security, data, and support cost of coexisting variants.

### Central model, mechanism, or theorem

Let $V$ be supported API contracts, $O_v$ operations in version $v$, $S_v$ representations/state transitions, and $C_v$ client/intermediary classes. A minimum verification surface is proportional to

$$
E=\sum_{v\in V}|O_v|\,|S_v|\,|C_v|,
$$

before rollout, region, authorization, failure, and rollback dimensions. Mint a version only when it creates a meaningful compatibility boundary whose migration benefit exceeds this durable cost. One identifier resolves exactly one documented contract; clients treat identifiers as opaque equality values.

### Critical invariants

Version contract, service deployment, SDK/package release, schema ID, resource revision, event subject sequence, and data migration epoch are distinct. Selection has one canonical location and unambiguous precedence; conflicting selectors fail. Missing-version behavior is explicit and stable. Unsupported/retired versions return a stable error, not silent fallback.

Every version has exact artifacts, stability, owner, support/deprecation dates, changelog, client generation, test matrix, and telemetry. Caches and signatures vary on the selector. Authorization is reevaluated and version choice cannot unlock privileges. External adapters converge on one authoritative effect/state model or specify deliberate isolation. Security/corruption fixes may be backported or exceptionally break a version under governed policy.

### Common failures

Using version for deployment or database schema; putting `v2` in a path with no semantic policy; exposing patch versions that force needless client pins; mutable dated snapshots; choosing “latest” implicitly; header and query selectors disagreeing; cache omitting a header version; versioning requests but not errors/webhooks/docs/SDKs; old version calling new behavior accidentally; forking business logic and data per version; comparing opaque dates to infer capabilities; capability flags exploding into hidden versions; GraphQL versioning the whole endpoint for one field; major version without migration/deprecation; unsupported selector falling back; and treating emergency fixes as forbidden because a version is frozen.

### Compact example

An API supports dated snapshots `2025-06-01` and `2026-03-10` via one header. The gateway validates one selector, routes to a version screen/adapter, records requested/resolved values, and includes the selector in cache variance. An unknown date returns a stable unsupported-version error with supported choices. It never selects the nearest date or “latest,” because a date is an opaque contract identifier. **Conclusion:** versioning is deterministic contract selection, not chronology guessing.

### Connections

[Backward and Forward Compatibility](081-backward-and-forward-compatibility.md) defines the coexistence matrix; [Additive and Breaking Changes](082-additive-and-breaking-changes.md) determines when a boundary is needed. [Media Types and Content Negotiation](005-content-negotiation.md), [Protocol Buffers and Schema Evolution](052-protocol-buffers-and-schema-evolution.md), and [Event Versioning](069-event-versioning.md) provide selector and format mechanics. The next module governs deprecation and sunset.

## Governing Question

Which versioning boundary and selector minimize long-lived ecosystem cost while giving clients deterministic semantics, providers room to evolve, and operators enough control to migrate, secure, observe, and retire every supported variant?

## Why This Matters

Versioning is frequently introduced as a URL decoration after a break has already been designed. That misses the hard work. The provider must decide what contract the identifier selects, how old and new behaviors coexist over one domain state, how clients pin and upgrade, how caches and gateways distinguish representations, how security fixes reach old versions, and when support ends.

Too little versioning makes incompatible changes surprise existing clients. Too much creates parallel products: duplicated handlers and models, divergent authorization, inconsistent fixes, SDK/documentation explosion, fragmented telemetry, and versions no one can retire. A version number is cheap; a supported version is a durable operational obligation.

Different ecosystems benefit from different strategies. A public REST API may expose major versions in paths or dated snapshots in a header. A GraphQL schema often evolves additively at one endpoint with field deprecation. A binary RPC API may put a major in its package. Events need writer schema/type identity for replay rather than a request-time selector. Capability negotiation may be narrower than a service-wide version.

The correct choice follows change cadence, client control, stability promise, caching and intermediary behavior, state model, migration horizon, and platform capabilities. The invariant is deterministic, documented contract selection with explicit lifecycle—not loyalty to path, header, date, or number syntax.

## Prerequisites and Retrieval

Retrieve [Content Negotiation](005-content-negotiation.md), [API Contracts and Behavioral Guarantees](021-api-contracts-and-behavioral-guarantees.md), [OpenAPI Structure](023-openapi-structure.md), [Protocol Buffers and Schema Evolution](052-protocol-buffers-and-schema-evolution.md), [GraphQL Schema Design](055-graphql-schema-design.md), [Event Versioning](069-event-versioning.md), [Backward and Forward Compatibility](081-backward-and-forward-compatibility.md), and [Additive and Breaking Changes](082-additive-and-breaking-changes.md).

Retrieve current/historical specifications and generated SDKs; all selectors/defaults/routing; gateway, cache, CDN, signature, WAF, and observability behavior; consumer/stability/support commitments; incompatible change history; shared domain/state and adapter architecture; rollout/rollback/failover paths; docs/changelogs; usage by version; security backport policy; preview/experimental controls; deprecation/sunset policy; and cost/capacity for supporting multiple versions.

## Learning Objectives

After completing this module, you can:

1. distinguish API versions from deployments, releases, SDKs, schemas, resource revisions, and data epochs;
2. decide whether compatible evolution, capability negotiation, or a new version is appropriate;
3. compare path, header, query, media-type, package, channel, and dated-snapshot strategies;
4. choose whole-service, interface, operation-family, representation, or event version scope;
5. define immutable versus rolling semantics, missing/default selection, and unsupported-version errors;
6. route/cache/sign/authorize/observe versioned traffic without ambiguity or downgrade;
7. implement adapters over a canonical domain model while preserving per-version behavior and effects;
8. publish matched specifications, SDKs, docs, changelogs, stability, and support windows;
9. test selection, mixed versions, state, rollout, rollback, security backports, and retirement; and
10. quantify and govern version sprawl across code, operations, consumers, and lifecycle.

## Core Exposition

### Separate every version dimension

Create a version map before choosing syntax. Distinguish:

- external API contract/version lens;
- protocol/media/serialization format;
- Protobuf/OpenAPI/JSON Schema document identity;
- generated SDK/package version;
- service application artifact/deployment/configuration;
- resource revision/ETag and optimistic-concurrency version;
- domain entity sequence/event subject version;
- event type/schema revision;
- database schema/data migration epoch; and
- preview/feature visibility or tenant entitlement.

One `version` field cannot safely encode all of them. An API `v2` client can receive resource revision 19 from server artifact 8.4 using schema fingerprint X while a migration epoch advances internally. Names such as `apiVersion`, `resourceRevision`, `schemaId`, and `producerArtifact` prevent coupling.

Google AIP-162 deliberately distinguishes resource revision from API version. Event versioning in API-069 likewise separates payload contract from subject order and producer release. Preserve those distinctions in logs, tokens, storage, and support tooling.

### Decide whether to version

First attempt compatible evolution from API-081/082: additive optional capability with old defaults, tolerant readers, expand–migrate–contract, deprecation, and adapters. Do not mint a major version for every field; clients should receive compatible fixes and additions without constant migration.

Create a new contract boundary when old and new meanings cannot coexist safely: removed/retyped required concepts, incompatible units or lifecycle, changed effect semantics, closed validation/state, or an architectural correction whose adapter would lie. A boundary makes the difference selectable; it does not make it good.

Use capability negotiation when one narrow orthogonal feature varies and a combinatorial version fork would be wasteful. Capabilities need stable names/semantics, authenticated eligibility, interaction rules, cache variance, expiry, and tests. A bag of interacting feature flags becomes hidden versions and is harder to reason about.

Use no request-time version for a GraphQL schema that can evolve additively through client-selected fields and deprecation. Introduce a separate field/type or endpoint only for genuinely incompatible meaning. Use writer schema/type identity for retained events because historical data selects its reader path.

### Choose the version scope

Whole-service major versions are simple to explain and generate but force clients to migrate unrelated operations and duplicate large surfaces. They work when changes are coherent across the service or platform lacks finer screens.

Interface/resource/operation-family scope limits migration blast radius and support cost, but clients may use several versions in one application and need consistent cross-interface semantics. Google AIP-185 describes interface-based versioning with version screens over one service and version-agnostic resource storage.

Representation/media scope is useful when the resource semantics remain stable but format differs. Content negotiation selects a media type/version; method, errors, links, and caches still need agreement. Do not hide changed side effects as a representation detail.

Event type/schema scope follows immutable facts and replay. Version only the event contract that changed; do not reuse API request version or entity sequence. Cross-type workflows still need migration and deduplication.

Choose the smallest scope that is semantically coherent and operationally governable. Too fine creates version combinations; too broad couples unrelated evolution.

### Define rolling channel versus frozen snapshot

A rolling major channel such as `/v1` receives compatible additions and fixes in place; clients pin the major, not every release. Google AIP-185 describes this style for stable major channels and recommends no exposed minor/patch for its APIs. State exactly what may change within the channel.

A dated/numbered snapshot gives clients a compatibility lens. Older snapshots remain unchanged except governed backports; new incompatible behavior uses a new identifier. GitHub's REST API uses a date-valued header, publishes breaking changes in new versions, and applies additive changes across supported versions under its policy.

Dates communicate release chronology to humans but clients should compare identifiers only for equality. Google AIP-184 explicitly treats its formatted version identifiers as opaque externally. Do not ask clients to infer that later dates contain a capability or that the nearest earlier date is compatible.

Immutable does not mean vulnerable forever. Define allowed security, privacy, legal, corruption, and severe reliability interventions. Backport fixes where semantics can remain; if an emergency break is required, communicate and observe it as an exception.

### Use path major versions deliberately

Path versions such as `/v1/orders` are visible in links, docs, logs, gateways, and caches. Routing is straightforward; browser/tool support is broad. They also make the version part of resource identifiers and can duplicate route trees.

Decide whether `/v1/orders/7` and `/v2/orders/7` identify the same domain resource through different contract lenses or distinct resources. Usually resource identity should remain stable across versions, with adapters translating. Links in representations should stay within the selected contract unless explicitly typed.

Only expose major stability boundaries in the path; `/v1.7.3` forces clients to bind to implementation releases and fragments routes. Compatible additions/fixes occur within major policy. A preview might use a distinct channel such as `v2beta` only under explicit stability/lifecycle rules.

Do not route by simple string prefix without canonicalization and authorization. Unknown/retired majors return stable errors, not the closest handler.

### Use header or query snapshot selection deliberately

Header selection keeps resource URIs stable and supports one routing tree with version-aware screens/adapters. It is less visible in browsers and must be explicitly included in cache variance, signatures, logging, CORS allowlists, proxies, SDKs, and support tooling.

Query selection is visible, easy for simple clients, and naturally participates in many cache keys, but can leak into logs/links and be mistaken for an ordinary filter. Reserve one exact parameter and canonical form.

If both mechanisms exist for ecosystem flexibility, permit at most one per request or require equality; conflicting values must fail. Google AIP-184/AIP-4236 specify mutual exclusivity for their header/query selectors to prevent ambiguity.

Define missing behavior: reject, or select a documented stable default for legacy clients. A moving “latest” default turns an unversioned call into an uncontrolled breaking upgrade. Record requested, resolved, and defaulted versions separately.

### Use media type versioning when representation is the boundary

A versioned vendor media type or parameter in `Accept`/`Content-Type` can select representation while preserving URI. It aligns with HTTP content negotiation and is valuable when consumers genuinely understand media negotiation.

Complex `Accept` precedence, proxies, browser tooling, documentation, and client libraries can make it hard to operate. Define exact supported media ranges, quality precedence, request and response content types, `Vary`, cache behavior, and `406`/`415` outcomes.

Do not overload media type version to change authentication, side effects, or resource identity invisibly. Those may require an API/operation boundary rather than serialization negotiation.

RFC 9110 describes media types as data format plus processing model and defines proactive negotiation/caching semantics. Follow HTTP rather than inventing substring matching.

### Use package and service identifiers for RPC

Protobuf/gRPC APIs commonly include major/stability in the package/service name, generating distinct client symbols and RPC paths. This allows old and new stubs in one process when naming/dependencies do not collide. Google AIP-185 requires major version in its Protobuf package and parallel major use during transition.

Package versioning does not eliminate wire/source compatibility review within a major. Preserve tag/type rules, error/deadline/metadata semantics, and generated-library stability. Shared messages across major packages can create dependency coupling; prefer owned adapters/canonical domain types over new version importing old public version internals.

Reflection, service discovery, auth policy, health, gateways, metrics, and rate limits must distinguish service versions. Do not expose a new RPC service while routing it to old incompatible implementation by default.

### Model stability separately from sequence

Alpha/experimental, beta/preview, and stable are commitments about change, support, data durability, SLOs, and production suitability. A version can be newer but less stable. Document whether preview is a superset of stable, can break in place, has data migration, and has a hard expiry.

Google AIP-181 distinguishes stability levels and notes emergency breaks; AIP-185 describes channel-, interface-, release-, and visibility-based strategies. These are policies for that ecosystem, not universal naming rules. Adopt one local taxonomy and do not call an unsupported experiment “v1” merely for appearance.

Preview traffic needs isolated quotas/capacity/failure domains where volatility could harm stable users. Preview data must have a graduation/migration or deletion contract. Do not let client-controlled preview label bypass tenant entitlement.

Features should graduate by compatibility and evidence, not by renaming alone. Deprecated preview functionality should not silently appear as stable.

### Treat selectors as an exact protocol

Specify grammar, case/normalization, maximum length, allowed characters, location, mutual exclusivity, default, supported set, unknown/expired response, response echo, and whether redirects preserve selection. Clients treat values as opaque.

Reject malformed/unknown versions before expensive work. Do not fall back from `v3` to `v2`; a request may be unsafe under old semantics. Distinguish malformed, unknown, preview-not-entitled, deprecated, and retired outcomes without disclosing private versions.

Echo resolved version in a response header/metadata and include it in error responses so clients/support can prove the contract used. Generated clients pin an explicit version unless legacy policy deliberately defaults.

Version selection is not authorization. Authenticate/authorize the operation/resource/feature after resolution, and enforce visibility/entitlement server-side. Sign the selector when request signing covers semantics.

### Make routing and caching version-aware

Central resolution at the edge reduces inconsistent parsing, but downstream services still need trusted resolved context or version-specific routes. Strip/overwrite untrusted internal headers. All components agree on one canonical resolved version.

For path/query selectors, caches often key naturally but must preserve canonicalization. For header/media selection, generate correct `Vary` or explicit cache key dimensions; otherwise one client's representation can be served to another version. CDN, application cache, idempotency records, ETags, and response signatures need the selected contract where representation/semantics differ.

Rate limits, quotas, SLOs, dashboards, and alerts may segment by version while protecting shared dependency capacity. A preview or old inefficient version cannot starve stable current traffic. Version routing must not multiply retry/failover amplification from API-080.

Regional deployments support the advertised version before routing. A control-plane catalog that announces a version too early creates selective failure.

### Adapt at the boundary, unify the domain

Prefer version-specific transport models and adapters around one canonical domain/application decision. Decode old/new inputs to explicit canonical commands; apply one authorization/idempotency/state transition; encode results under the selected contract. This avoids parallel business logic drifting.

Adapters must preserve each version's promised defaults, errors, field presence, ordering, limits, and side-effect semantics. If old and new semantics cannot map to one canonical operation without lying, use separate domain commands/handlers with explicit ownership rather than a giant conditional.

Do not create a database per API version by default. Use schema evolution and version-aware adapters over one source of truth, with rollback/state compatibility. Separate stores may be justified for genuinely separate products or risk isolation, but synchronization/identity become distributed-system problems.

Version-specific idempotency/outcome lookup must converge on one effect identity where operations represent the same business action. A client retrying through another version must not duplicate a payment.

### Publish complete version artifacts

For every supported version publish an immutable/traceable contract artifact, behavior notes, stability, operations/fields/errors/limits, SDK/library compatibility, examples, changelog from prior version, migration guide, support/deprecation/sunset, and owner/contact.

Generated SDKs state which API contract they target. SDK package version is not automatically the API version: one SDK release may support several contracts or update without API change. Avoid names that make users infer false equivalence.

Docs selectors must remain pinned when navigating and code samples must send the shown version. Search results and portals should distinguish current, preview, deprecated, and retired. Machine discovery can enumerate public supported versions without revealing private entitlements.

Once a snapshot identifier is published, do not mutate its incompatible semantics. Corrections/clarifications and backports are recorded with artifact provenance.

### Govern defaults and upgrades

Explicit pinning prevents surprise but leaves clients on old versions. Defaults simplify legacy use but can hide which contract runs. If a default exists, freeze it per documented policy, echo it, measure it, and migrate callers to explicit selectors. Never advance it silently across a break.

Client upgrade is an explicit workflow: read changelog/migration guide, update SDK/spec, test both response and effect semantics, canary, observe, and change selector. Server support for both versions enables independent pace but needs a published window.

Avoid client algorithms like “request latest supported date” in production. They turn provider publication into immediate uncontrolled rollout. Discovery helps tooling/operators choose and test; stable clients pin.

Downgrade/fallback to an older version occurs only through an application-approved semantic path, never automatically on parse/auth/error. Attackers can exploit automatic downgrade to bypass newer controls.

### Observe version lifecycle

Record requested, resolved, defaulted, malformed/unknown/deprecated/retired selectors; operation; client/SDK identity where privacy-safe; tenant; region; adapter path; error; latency; response size; state/effect version; and fallback/translation. Do not log credentials or sensitive payloads.

Measure traffic, unique active consumers, error/latency/SLO, unknown selectors, default usage, deprecated fields/operations, adapter failures, parity, support cost, vulnerabilities/backports, and last-seen time by version. Segment shared resource consumption.

Inventory combines registration, telemetry, contracts, partner/support records, SDK distribution, batch/offline/recovery paths, and direct attestation. Recent traffic alone cannot prove an old version unused.

Version sprawl metrics include handlers/adapters, contract/SDK artifacts, test cells, documentation, security patches, incidents, and on-call cognitive load. Use them to drive migration, not to delete without evidence.

### Secure and operate old versions

All supported versions receive authentication, authorization, isolation, privacy, dependency, vulnerability, and reliability maintenance. An old contract is not permission to use an obsolete cipher, broken authorization, or exposed dependency.

Backport safe internal/security fixes without changing promised external semantics. If the fix necessarily breaks inputs/outputs, use emergency policy: smallest scope, clear error, direct communication, compensating migration, monitoring, and governance record. Stability policy must say this before crisis.

Protect version catalogs and routing from enumeration of private versions, selector injection, normalization collision, cache poisoning, signature exclusion, and downgrade. Preview visibility is an entitlement, not a string the caller grants itself.

Capacity-plan popular old versions until sunset. Throttling them early is itself a contract/lifecycle change unless declared.

### Test every version boundary

Validate selector grammar, conflict, default, unknown, deprecated, retired, preview entitlement, redirect, signing, cache variance, and response echo. Exercise through gateways/CDNs/proxies and direct internal transports.

Run each supported contract against shared canonical state and version adapters: requests, responses, errors, defaults, ordering, pagination, auth, idempotency, consistency, limits, latency, and side effects. Test old/new clients, SDKs, regions, rollouts, rollback, backup restore, long-running operations, and cross-version retries.

Mutation tests remove version cache variance, allow conflicting selectors, fall back unknown versions, drift old adapter behavior, leak preview fields, and write rollback-unreadable state; gates must catch them.

Rehearse migration and sunset with shadow/canary traffic and stable unsupported-version behavior. A version is not ready merely because its route returns `200`.

## Definitions and Notation

Let $V$ be supported API contracts. For version $v$, let $O_v$ be operation set, $S_v$ representation/state-transition classes, and $C_v$ client/intermediary classes. Let $E=\sum_{v\in V}|O_v||S_v||C_v|$ be a simple lower-bound proxy for verification surface before environment/failure dimensions.

Let selector $q$ resolve through deterministic function $R(q,a)$ under authenticated context $a$ to exactly one contract $v$ or a typed error. Let $D$ be defaulted requests, $T$ total requests, and default ratio $d=D/T$. Let $U_v$ be credibly inventoried consumers of $v$ and $M_v$ confirmed migrated; $M_v/U_v$ is meaningful only when inventory completeness is justified.

A **contract lens/screen** is the version-specific visible subset and behavior over a service. A **channel** is a rolling contract at one major/stability level. A **snapshot** is a pinned contract identifier. A **variant/decorator** distinguishes a deliberate lineage/stability/private view under one naming policy. A **support window** is the interval during which the provider operates and secures the contract.

## Mechanisms, Invariants, or Proof Structure

**Sprawl bound.** Each supported version adds operation-by-state-by-client verification cells. Because rollout, region, auth, failure, and rollback multiply further, $E$ is a lower-bound cost indicator. It does not predict test count exactly; it proves version creation is not free.

**Deterministic resolution.** If one request can carry conflicting path/header/query/media selectors and precedence is implicit, two intermediaries can resolve different contracts. Requiring one canonical selector or equality plus a single resolver makes $R(q,a)$ a function; unknown values produce error rather than semantic fallback.

**Cache counterexample.** If response depends on header-selected version but cache key omits that header, identical URI/auth-visible requests for $v_1$ and $v_2$ can share an entry, so at least one receives the wrong contract. Correct cache variance or separate routes is necessary.

**Canonical-effect argument.** When $v_1$ and $v_2$ represent the same business command, mapping both through stable effect identity and one authoritative transition prevents version choice/retry from creating two effects. Separate duplicated handlers without a common invariant can diverge even if schemas look correct.

Operational invariants are: version dimensions distinct; version only meaningful incompatible boundaries; scope coherent; selector opaque/deterministic; snapshots/channels policy explicit; caches/signatures/auth correct; one domain authority; artifacts matched; upgrades explicit; old versions maintained; lifecycle observable; and retirement evidence-backed.

## Alternatives and Trade-Offs

Path versions maximize visibility/routing simplicity but alter URIs and duplicate route surfaces. Header selection preserves resource URIs and supports snapshots but needs careful caches, signatures, SDKs, and debugging. Query selection is visible/cache-friendly but pollutes links/logs. Media types align with representation negotiation but are harder for many clients.

Rolling majors reduce client churn and version count but require strong compatible-change discipline. Frozen snapshots provide deterministic pinning but multiply backports, docs, SDKs, and test cells. Dated identifiers aid human chronology but must remain opaque to client logic.

Whole-service scope is simple but couples migrations. Fine interface scope reduces blast radius but increases combinations and cross-interface reasoning. Capability flags avoid large versions for narrow features but can become ungoverned hidden variants.

One canonical domain model reduces drift and duplicate effects but makes adapters long-lived. Forked implementations allow radical redesign but duplicate fixes, state, authorization, and operations. Use separate domains only when semantics truly diverge.

Explicit version requirement prevents ambiguity but burdens simple/legacy clients. A stable default eases onboarding but hides pins and eventually blocks retirement. Echo and migrate defaults deliberately.

Supporting old versions longer helps consumers but increases security and operational cost. Short windows accelerate evolution but demand inventory, migration tooling, communication, and contractual alignment.

## Failure Modes and Misconceptions

- “Put `v1` in the URL.” Syntax without semantics/lifecycle is decoration.
- “Version equals deployment.” Deployments change far more often than public contracts.
- “SDK 3.2 means API v3.” Package and contract versions are independent.
- “Date means clients can compare.” Treat identifiers as opaque equality values.
- “Latest is safest.” Automatic latest is an uncontrolled breaking rollout.
- “Frozen means no security fixes.” Supported versions still require safety maintenance.
- “Header versions do not affect caches.” They must vary the representation/cache key.
- “Query and header can both work.” Conflicts create ambiguous routing unless forbidden/equal.
- “Unknown version can use nearest.” Silent fallback violates requested semantics.
- “A new major permits anything.” It still needs coherent design, state, migration, and security.
- “Each version gets its own database.” That creates synchronization and identity problems by default.
- “One handler with conditionals is unified.” It may be an unreadable divergent product without adapters/invariants.
- “GraphQL must use `/v2` for every change.” Client-selected additive fields and deprecation often avoid it.
- “Feature flags eliminate versions.” Interacting flags can create many hidden contracts.
- “Preview label grants access.” Entitlement is authorized server-side.
- “No traffic means retire.” Offline, partner, failover, and replay consumers may be dormant.
- “Versioning replaces compatibility.” Every supported version must still evolve compatibly within its promise.

## Worked Examples

### Example 1

`/v1/orders/7` and `/v2/orders/7` are two contract lenses on order 7, not two orders. Both adapters authorize the same resource and use one effect/idempotency authority; v2 exposes a new money model while v1 retains its promised representation.

### Example 2

A request sends `X-Api-Version: 2026-03-10`. The resolver compares equality against supported identifiers and returns that exact contract. It does not infer features from the date or choose the nearest version if unsupported.

### Example 3

Unversioned legacy calls default to `2022-11-28`; the response echoes it. Advancing the default to `2026-03-10` would upgrade clients silently, so the provider instead measures/default-migrates clients to explicit pins before retirement.

### Example 4

Two versions share `/orders/7` and are selected by header, but the CDN cache key omits the header. A v1 response is served to v2. Adding correct `Vary`/cache-key version dimension and tests prevents cross-contract contamination.

### Example 5

A request supplies header `2026-03-10` and query `$apiVersion=2025-06-01`. The gateway returns a stable ambiguous-selector error. Choosing one by undocumented precedence would let proxies and origins disagree.

### Example 6

A GraphQL service adds `displayName` and deprecates `fullName`. Existing operations select only `fullName`, so they keep their result shape without `/v2`. Usage evidence and deprecation migrate clients before field removal.

### Example 7

Event contract `OrderShipped.v2`, subject version 19, producer release 8.4, and API request version `2026-03-10` are logged separately. Reusing one `version=19` would make replay, routing, and support ambiguous.

### Example 8

Three API versions each expose 60 operations, two representation/state classes, and four client/intermediary classes. The simple lower bound is $3\times60\times2\times4=1{,}440$ cells before regions, auth, failure, and rollback—evidence that another version has durable cost.

### Example 9

V1 accepts `amountCents`; v2 accepts `amountMinorUnits` plus exponent. Both adapters create one canonical money command and share the same idempotency effect key. A timeout retry through another version cannot charge twice.

### Example 10

A critical authorization vulnerability affects two supported snapshots. The provider backports the check where possible; where old request shape cannot be made safe, it returns a new precise error, notifies affected clients, monitors rejects, and records an exceptional break rather than leaving the version vulnerable.

## Cross-Program Connections

[Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md) supplies boundary adapters, canonical domain models, strangler migration, and ownership.

[Database Engineering](../../18-database-engineering/ROADMAP.md) provides one-source-of-truth state evolution, migrations, rollback, backups, and cross-version idempotency records.

[Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) covers mixed versions, partial rollout, consistency, effect identity, replay, failover, and convergence.

[Network Engineering](../../24-network-engineering/ROADMAP.md) explains routing, proxies, caches/CDNs, content negotiation, headers, signatures, and regional propagation.

[Security Engineering](../../25-security-engineering/ROADMAP.md) governs entitlement, downgrade, normalization, cache poisoning, old-version maintenance, and emergency breaks.

[Platform Engineering](../../29-platform-engineering/ROADMAP.md) owns version catalogs/screens, gateways, SDK/doc generation, telemetry, compatibility gates, backports, and lifecycle automation.

## References

1. Google, [AIP-184: API Version Identifiers](https://google.aip.dev/184).
2. Google, [AIP-185: API Versioning](https://google.aip.dev/185).
3. Google, [AIP-181: Stability Levels](https://google.aip.dev/181).
4. GitHub, [REST API Versions](https://docs.github.com/en/rest/about-the-rest-api/api-versions).
5. IETF, [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html).
6. GraphQL Foundation, [GraphQL Specification, October 2021](https://spec.graphql.org/October2021/).
7. Semantic Versioning, [Semantic Versioning 2.0.0](https://semver.org/).

## Exercises

### Exercise 1

Choose a versioning strategy for a public REST API with uncontrolled mobile/partner clients, quarterly incompatible changes, shared resources, CDN caching, generated SDKs, and a required two-year support window. Define selector, scope, default, and lifecycle.

### Exercise 2

Design deterministic resolution for path, header, query, and media type when a legacy estate already uses several. Cover conflict, normalization, caching, signing, authorization, errors, echo, and observability.

### Exercise 3

Compare `/v1` rolling majors, dated snapshots, GraphQL additive evolution, and capability negotiation for changes to one optional report feature plus a later incompatible payment model.

### Exercise 4

Design the adapter/state architecture for v1 and v2 payment commands so retries, rollback, reconciliation, auth, errors, and migration preserve one effect while representations differ.

### Exercise 5

Create a production-readiness and retirement test plan for three supported versions, one preview channel, two regions, a CDN, old/new SDKs, candidate-written state, and a possible emergency security backport.

## Answers to the Exercises

### Answer 1

Use explicit dated snapshot selection in one header when platform/cache tooling can support it; path majors are also viable if URL visibility outweighs snapshot granularity. Version the coherent public interface/resource families, keep one canonical resource identity/state, and publish immutable compatibility screens with additive fixes/backports. Require explicit pins for new clients; freeze/echo a documented legacy default rather than moving “latest.” CDN keys/`Vary`, signatures, gateways, SDKs, docs, errors, and metrics include the resolved version. Publish at least two years of support after a successor, with deprecation/sunset and migration guides. New snapshots are justified only for incompatible changes; compatible additions can flow under policy. Inventory partners/mobile tails and operate/security-patch every supported snapshot.

### Answer 2

Choose one canonical external selector for new traffic. At the edge, parse path/header/query/media according to an explicit legacy table, normalize exact grammar, and allow at most one semantic value; conflicting values fail before routing. Unknown/retired/private-not-entitled values return distinct stable public-safe errors without nearest fallback. Produce one trusted resolved context, strip untrusted internal copies, echo the resolved value, and authorize the selected operation independently. Include it in cache keys/`Vary`, idempotency/ETag representation context, and request signatures. Record requested sources, normalized/resolved/defaulted value, conflict/error, client, route, region, cache, and adapter. Migrate legacy forms with telemetry and a sunset rather than permanent precedence ambiguity.

### Answer 3

A single optional report feature should usually be additive/opt-in in `/v1`, a GraphQL field selected by interested clients, or a named capability if it truly needs gated experimental semantics; a new service version is excessive. GraphQL deprecation/usage can evolve fields without endpoint versions. A dated preview can expose the report to uncontrolled REST clients if platform screens are established. The incompatible payment model deserves a new major/snapshot/operation because units/effects cannot be silently changed. Keep old/new payment contracts concurrently, adapt to one money/effect domain, publish migration/support, and retire with evidence. Capability flags must not combine into an undocumented payment contract.

### Answer 4

Define separate v1/v2 transport commands and encoders, then map both through explicit validated canonical money and payment commands. Preserve version-specific omission/default/error behavior at adapters. Authenticate/authorize once against the same resource/effect; derive one stable idempotency/effect key independent of version. Store canonical payment state plus enough original contract/provenance for exact response/outcome lookup. Deploy rollback artifacts able to read candidate state or gate v2 writes; rehearse in-flight timeout and cross-version retry. Reconcile adapter input/result/effect parity, reject ambiguous conversions, and never downcast unsupported precision silently. Migrate clients before retiring v1 reads/docs/SDKs and only later remove old state/provenance after recovery horizons.

### Answer 5

Validate selector grammar/conflicts/default/unknown/deprecated/retired/preview entitlement and response echo through both regions/CDN. Prove cache/signature isolation and catalog propagation before routing. Run each old/new SDK against every promised version for requests, responses, errors, defaults, pagination, auth, idempotency, effects, latency/size, and shared state; include rolling deployment, regional skew, rollback reading candidate state, backup restore, long operations, and failover. Isolate preview quota/capacity/data and verify it cannot be self-granted. Mutation-test missing cache variance, silent fallback, selector conflict, preview leak, adapter drift, and duplicate effect. Rehearse a safe backport and an unavoidable emergency break with error/communication/monitoring. Retirement requires credible consumer inventory including dormant/partner/recovery paths, migration confirmation, sunset notices, stable `410`/unsupported behavior, expired rollback/backups, and clean post-sunset telemetry.
