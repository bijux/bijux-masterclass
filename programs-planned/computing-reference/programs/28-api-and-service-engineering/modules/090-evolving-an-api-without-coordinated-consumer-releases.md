---
module_id: API-090
program: API & Service Engineering
level: 2
module_number: 90
title: Evolving an API Without Coordinated Consumer Releases
status: complete
last_verified: 2026-09-02
---

# Evolving an API Without Coordinated Consumer Releases

## One-Page Review

### Governing question

How can an API evolve while independently deployed old and new consumers, servers, producers, readers, SDKs, cached artifacts, queued messages, and rollback versions coexist, without requiring one simultaneous release or accumulating permanent compatibility machinery?

### Essential definitions

- **independent evolution** lets participants deploy on separate schedules while remaining within an explicit compatibility envelope; it does not mean no communication or governance.
- A **mixed-version window** is the interval during which several producer/consumer/server/client/schema/config versions can interact.
- **expand–migrate–contract** first introduces compatible capacity, then moves/verifies use, then removes legacy behavior after evidence.
- A **compatibility envelope** is the set of version/capability pairs and behaviors promised to interoperate.
- **dual read** accepts old and new representations; **dual write** emits or persists both; **dual serve** provides old and new views/operations.
- A **translation boundary** maps contracts explicitly while preserving identity, semantics, errors, security, idempotency, and observability.
- **capability negotiation** chooses supported behavior explicitly; it must be authenticated/bounded and cannot infer safety from version strings alone.
- A **contraction gate** is the evidence conjunction required before disabling or removing the old path.

### Central model, mechanism, or theorem

At time $t$, let active callers/producers be $P_t$, active servers/consumers/readers be $C_t$, and $A(p,c)$ mean their request/response or writer/reader interaction preserves the promised semantics. Safety during an independent rollout requires

$$
\forall t\ \forall p\in P_t\ \forall c\in C_t:\ A(p,c),
$$

for every pair routing/replay can actually create. A test of only newest-to-newest proves one cell, not the matrix. Expand–migrate–contract reduces the active matrix in controlled stages; contraction waits for consumer/effect evidence, retry/queue/cache/rollback horizons, healthy observability, and explicit exceptions.

### Critical invariants

Each stage states accepted/emitted semantics, pairwise compatibility, ordering, rollback, and failure response. Expansion precedes dependence; new readers/servers tolerate the governed old form before new writers/clients emit the new form. Defaults/presence/unknown fields/enums/errors/authorization/limits remain explicit. Adapters are versioned, observable, idempotent where effects occur, and removable.

Schema compatibility never proves behavioral compatibility. Traffic percentage never proves consumer completeness. Tolerant reading is bounded and must not accept ambiguous or unsafe input. Rollback includes state, queues, caches, schemas, generated clients, and effects—not code alone. Legacy removal follows deprecation, consumer inventory, direct migration evidence, and full horizon coverage.

### Common failures

Big-bang release calendar; server-first/client-first assumed universally safe; “additive” required field/default/enum changes; old client crashes on unknown response field; new writer emits before all relevant readers accept; dual write diverges; backfill races live writes; alias fields disagree; adapter loses auth/idempotency/error meaning; capability inferred from User-Agent; downgrade attack; version header stripped by cache/proxy; old/new cache entries collide; latest-only schema check; generated SDK lags; queue/replay resurrects old form; canary sees only new clients; rollback code cannot read new state; shadow traffic creates effects; aggregate traffic hides dormant consumers; compatibility flag becomes permanent; and old path removed before retry/cache/DR horizons.

### Compact example

`name` is being replaced by structured `given_name`/`family_name`. The server first accepts both but stores one canonical model; conflicting forms fail deterministically. Responses keep `name` while optionally adding structured fields only for clients known to tolerate them. Consumers migrate and prove outcomes. After all required consumers, replays, caches, SDKs, and rollback versions are safe, writes to `name` are rejected, then the field is deprecated and removed under policy. **Conclusion:** a field rename is a staged semantic/data migration, not a simultaneous schema edit.

### Connections

[Contracts](021-api-contracts-and-behavioral-guarantees.md), [Idempotency Keys](037-idempotency-keys.md), [Protocol Buffers Evolution](052-protocol-buffers-and-schema-evolution.md), [Event Versioning](069-event-versioning.md), [Compatibility](081-backward-and-forward-compatibility.md), [Change Classification](082-additive-and-breaking-changes.md), [Versioning](083-versioning-strategies.md), [Deprecation](084-deprecation-and-sunset.md), [Consumer Inventory](085-consumer-inventory-and-usage-evidence.md), and [Schema Registries](088-schema-registries-and-contract-governance.md) supply the mechanisms synthesized here.

## Governing Question

What compatibility model, migration stages, adapters, negotiation, tests, observability, rollout/rollback controls, consumer evidence, and contraction gates allow a provider to evolve requests, responses, schemas, behavior, state, and operations without synchronized consumer deployments?

## Why This Matters

Coordinated releases do not scale across independently owned services, partner organizations, mobile/offline clients, SDK versions, regions, queues, caches, or disaster recovery. Even within one deployment, rolling updates create mixed versions. Treating synchronization as a prerequisite makes every API change a distributed transaction across organizations—with no atomic commit.

Independent evolution transfers complexity into the contract and migration. The provider must know which version pairs can meet, which semantics each accepts/emits, when new behavior becomes depended on, how state is represented, and how rollback works. “Backward compatible” without direction and population is too vague.

The hardest breakages are invisible to schema tools: default/presence, new enum behavior, authorization, timing, ordering, retries, side effects, errors, limits, consistency, and business meaning. An additive response field can break strict decoders; an optional request field can change a default for old clients; a new event can reorder effects.

Compatibility scaffolding also has cost and risk. Dual paths can diverge, adapters hide failures, and flags become permanent. A complete plan includes contraction from the beginning: ownership, metrics, migration tasks, expiry, terminal behavior, and cleanup.

## Prerequisites and Retrieval

Retrieve [API Contracts and Behavioral Guarantees](021-api-contracts-and-behavioral-guarantees.md), [Idempotency Keys](037-idempotency-keys.md), [Protocol Buffers and Schema Evolution](052-protocol-buffers-and-schema-evolution.md), [Event Versioning](069-event-versioning.md), [Backward and Forward Compatibility](081-backward-and-forward-compatibility.md), [Additive and Breaking Changes](082-additive-and-breaking-changes.md), [Versioning Strategies](083-versioning-strategies.md), [Deprecation and Sunset](084-deprecation-and-sunset.md), [Consumer Inventory and Usage Evidence](085-consumer-inventory-and-usage-evidence.md), [Design Reviews](087-design-reviews.md), [Schema Registries and Contract Governance](088-schema-registries-and-contract-governance.md), and [API Product Ownership](089-api-product-ownership.md).

Retrieve exact old/new contracts and semantic diffs; deployed client/server/producer/consumer/SDK/schema/config versions; routing/service discovery/gateway/cache behavior; consumer inventory/use/cadence/criticality; queues/replay/retention; state/data schema and migrations; compatibility/contract/generated-client tests; auth/authorization/privacy; retries/idempotency/concurrency/ordering; SLO/capacity/cost; feature/capability flags; telemetry provenance; rollout/rollback/DR; notices/exceptions; and removal ownership/dates.

## Learning Objectives

After completing this module, you can:

1. model active producer/consumer and client/server compatibility as an explicit mixed-version matrix;
2. distinguish backward/forward/full, structural/behavioral, wire/source/generated/runtime, and latest/transitive guarantees;
3. design expand–migrate–contract stages with entry/exit evidence and bounded overlap;
4. evolve fields, requiredness, defaults, enums, errors, operations, versions, events, and state safely;
5. implement dual read/write/serve and translation boundaries without ambiguity, lost security, or duplicate effects;
6. use explicit capability negotiation safely across proxies, caches, authentication, downgrade, and lifecycle;
7. test relevant pairwise combinations, generated clients, replay, retry, rollback, and semantic outcomes;
8. deploy with flags/cohorts/canaries/shadows while separating attempts, logical operations, and effects;
9. prove migration across active, dormant, partner, offline, batch, queue, failover, and recovery paths; and
10. contract and remove legacy machinery through deprecation evidence without recreating a big-bang release.

## Core Exposition

### Define the independently evolving population

Inventory logical consumers and deployed artifacts, not just current request versions. Include server replicas/regions, gateway policies, client applications/SDKs, mobile/offline installations, partners, jobs, webhooks, event producers/consumers, queues/replay, caches, backup/restore, failover, support/incident tools, and rollback images.

Map what can actually interact through routing, load balancing, subscriptions, retained data, and recovery. A client may hit old or new server during rolling deployment; a new consumer may replay old events; rollback may pair old code with new database state.

State the compatibility promise by direction and dimension: old client/new server requests and responses; new client/old server; old reader/new writer; new reader/old writer; schema/wire/source/generated language; syntax/structure/meaning/security/timing/operations.

Set the mixed-version horizon from deployment lag, mobile/partner support, retries, idempotency retention, cache TTL, queue/event retention, replay/backfill, offline cadence, rollback, backup, and DR—not an arbitrary release interval.

### Build and test the compatibility matrix

List relevant rows and columns by actual capability/contract version, not every build SHA. For each possible pair, test request decoding/validation/defaulting, authorization, effect/idempotency, response/error decoding, unknown values, limits, and observable outcome.

Add writer/reader matrices for stored/queued representations and old/new application/state schemas. Test generated SDK versions/languages because valid schemas can generate incompatible source APIs or strict decoders.

Include negative cells explicitly: a new capability may require new server; routing/negotiation must prevent that pair rather than wish it away. If any load balancer can route new client to old server, the pair is active until routing changes safely.

Automate representative matrix tests in CI and preproduction; validate runtime version/capability telemetry. Do not let the matrix become a spreadsheet detached from deployed truth.

### Classify the change beyond schema shape

Review syntax, validation accepted sets, required/optional/null/presence/default, enum/union/open types, identifier/units/time, operation/resource/state, errors/status/retryability, auth/scopes, quotas/performance, ordering/consistency, side effects/idempotency, caching, observability, docs/SDK, and lifecycle.

Google AIP-180 catalogs backward-compatibility considerations including removal/rename/type changes and field behaviors within its scope. Format-specific tools add evidence, but local runtime/consumer semantics remain decisive.

An additive field can break clients that reject unknowns, generated exhaustive matching, hashes/signatures, cache keys, or privacy assumptions. A server accepting a new optional input may make an old default context-dependent. An enum addition can route old code to unsafe fallthrough.

Document intended old/new semantics and ambiguity rules before choosing mechanism.

### Plan expand–migrate–contract as a state machine

Define durable stages with owner, exact artifacts, entry evidence, actions, emitted/accepted forms, routing, metrics, abort/rollback, exit gate, deadline, and next stage. Typical stages are prepare, expand readers/servers, enable new writes/calls for controlled cohorts, migrate/backfill/verify, make new canonical, stop old creation/use, deprecate, contract/remove, and cleanup.

Expansion must be deployed everywhere it is needed before any participant depends on it. For writer/reader systems, deploy readers that accept both before writers emit new. For new client capability served by new server only, route only proven capable pairs or deploy server support fleet-wide first.

Migration proves target business effects, not merely copied rows/calls. Contraction stops new old-form creation before removal and waits through all relevant horizons.

Every temporary path has creation reason, owner, observability, expiry/removal condition, and cleanup test from day one.

### Evolve request and response fields

To add request capability, first make new server accept the field while preserving old-client semantics when absent. Do not change old default silently. Validate authorization/overposting, conflicts with old fields, idempotency fingerprint, and logging/privacy.

To add response fields, confirm old clients tolerate unknown fields or gate/project responses by explicit capability/version. Generated clients and signatures/cache representations need tests. Never assume generic JSON implies tolerant readers.

For rename/split/merge/type/unit changes, accept old/new forms at a translation boundary, define canonical internal model, conflict/precedence and round-trip/loss rules, migrate stored state, and keep old responses/views until consumers move. Reject contradictory dual inputs deterministically rather than guess.

For requiredness, roll out validation only after all entitled writers supply the field and old queued/replayed data is handled. A schema “required” flip before that is breaking.

### Evolve defaults, presence, enums, and errors

Absence, explicit null/zero/empty, and default can carry different meaning. Preserve presence where the protocol/runtime supports it; adapters must not collapse “unset” into a value that changes behavior. Version or add explicit policy when default meaning must change.

Treat enums as open or closed deliberately. New values require old-consumer behavior: preserve/unknown wrapper, safe fallback, capability-gated emission, or new version. “Default to first enum” can be destructive.

Error evolution includes status/code/type, retryability, partial effects, field violations, correlation, and SDK exception mapping. Adding a new error variant can break exhaustive consumers even when success schema is unchanged.

RFC 9413 explains risks of applying the robustness principle too broadly. Be tolerant only of specified ignorable extensions; reject ambiguous, malformed, unauthorized, or semantically unsafe input consistently so bugs and attacks do not become de facto contract.

### Use dual read, write, and serve safely

Dual read maps old and new representations into one canonical model and records source/version/conflicts. It must preserve auth, tenant, validation, idempotency, and error semantics. Test malformed and conflicting forms.

Dual write risks partial success, order races, divergent transformations, and doubled effects. Prefer one transactional canonical write plus derived projection/outbox/backfill. If two systems must be written, define source of truth, idempotent reconciliation, failure state, monitoring, and recovery.

Dual serve can keep old and new views/operations from one canonical state. Avoid two business implementations drifting. Compare outputs/effects for cohorts and make legacy use visible.

Backfill coordinates with live writes using version/sequence/watermark, idempotency, conflict policy, bounded load, pause/resume, reconciliation, and completion proof. Row count equality is insufficient when semantics transform.

### Design translation boundaries and adapters

Place adapters at owned boundaries: gateway façade, service endpoint, client/SDK shim, event upcaster/downcaster, anti-corruption layer, or data projection. Choose based on trust, state/effect ownership, latency, failure, and removal.

Version adapter logic and test both directions for loss, defaults, unknowns, errors, auth context, quotas, cache keys, correlation, retries/idempotency, and observability. A translation that turns denial into not-found or drops an idempotency key changes contract.

Do not chain unbounded adapters across versions. Prefer supported-to-canonical mappings and explicit unsupported terminal behavior. Measure each legacy path and dependency.

Adapters reduce coordination at deployment time but do not eliminate consumer communication or migration responsibility.

### Negotiate capabilities explicitly and safely

Negotiate only when multiple behaviors must coexist and ordinary additive compatibility is insufficient. Use stable media types/profiles, protocol version/capability fields, or authenticated registration tied to actual deployment—not User-Agent/IP guesses.

Define who offers/selects, defaults when absent, unsupported response, cache `Vary`/keying, proxy/header behavior, signature coverage, downgrade resistance, privacy, and lifecycle. A capability bit means exact semantics, not “new client.”

Avoid a combinatorial flag protocol. Capabilities with dependencies/conflicts need coherent profiles and server-side validation. Log selected profile safely and expose diagnostics.

Test stripped/duplicated/malformed headers, stale registration, mixed replicas, cache collisions, malicious downgrade/upgrade claims, and rollback.

### Evolve operations, versions, and endpoints

Add a new operation/resource/version alongside old when semantics cannot be safely extended. Keep shared state/effects consistent and define cross-version identifiers, idempotency, authorization, concurrency, and visibility.

Route version explicitly and consistently across gateway/service/cache/docs/SDK. Default-version changes are behavioral changes; do not silently move absent-version clients.

Use branch-by-abstraction internally so implementation can migrate without exposing infrastructure topology. Deploy compatible façade/adapter before moving backends; preserve rollback/state.

Deprecate old surface with exact scope, replacement, dates, runtime signals, direct notice, migration tooling, and evidence. RFC 9745’s Deprecation header/link can contribute HTTP signaling but does not itself change behavior or prove receipt.

### Evolve events, queues, and replay

Deploy compatible readers/consumers before writers emit new event shape/value. Pin schema identity, choose backward/forward/transitive guarantees from retained data and rollback, and test real generated readers.

Do not mutate historical event meaning. Upcast at read/projection boundaries with versioned deterministic logic; preserve raw event/audit. A new event type may be safer than reinterpreting an old one.

Account for topic/channel, key/partition, ordering, delivery, deduplication, retries/dead-letter, correlation, and effect semantics—not payload alone. Dual publishing can duplicate/reorder effects; give events stable identity and consumers idempotent transition plans.

Replay/backfill expands the active compatibility population to every retained version. Removal waits until all supported consumers/recovery paths can process or a governed migration transforms retained data.

### Evolve persistent state and caches

Use expand/contract database migrations: additive nullable columns/tables/indexes, compatible code, dual/derived representation, backfill, verify, switch canonical reads/writes, stop old writes, then constrain/drop. Exact ordering depends on data store semantics.

Rollback code must read/write current state. Destructive schema changes or new-only values can make rollback impossible even when binaries roll back. Define roll-forward when true rollback is unsafe.

Version migrations, make them idempotent/resumable, limit load/locks, and reconcile semantic totals/effects. Backups and restores containing old/new state need tests.

Cache keys include representation/profile/version/auth/tenant dimensions. Purge/TTL/validation prevents old/new semantic collision; downstream/CDN behavior is part of the matrix.

### Roll out with cohorts, flags, canaries, and shadows

Separate code deployment from capability activation. Flags are server-controlled, scoped by consumer/tenant/region/operation, default-safe, audited, observable, and expiring. They do not replace public contract/version when consumers depend on behavior.

Canary cohorts cover representative old/new clients, critical/low-volume consumers, regions, payloads, and failures. A canary of internal newest SDK proves little about partners/offline clients.

Shadowing compares parsing/results/performance without causing real side effects, messages, charges, notifications, or sensitive-data expansion. Where effects cannot be suppressed, use recorded/synthetic safe tests instead.

Define promotion/abort thresholds for correctness, authorization, effects, errors, latency/capacity/cost, old/new parity, and telemetry health. Monitor logical operations/effects separately from attempts.

### Design rollback and recovery before rollout

For every stage ask: can old code receive new request/event/state/config? Can new consumers process old replay? Can routing/cache/SDK/config revert? What effects have already occurred? How is partial backfill/dual write reconciled?

Rollback may mean disable new emission while keeping expanded readers, route capability cohorts back, restore adapter, or roll forward with correction. Never remove expansion needed to read already-created new state.

Keep rollback artifacts/config/schema/access and capacity available through the promised horizon. Test regional failover, queue backlog, disaster restore, and incident tooling—not only ordinary deploy reversal.

State migrations and external effects make code rollback non-atomic. Record point of no return and decision authority.

### Observe migration and prove contraction readiness

Measure per trusted logical consumer/deployment: requested/resolved contract, capability, old/new fields/operations/events, success/error, logical operation/effect, region, SDK, last seen, expected cadence, and migration evidence. Minimize sensitive/high-cardinality data and disclose sampling/drop/retention.

Track unknown/unattributed traffic, failed old calls, dual conflicts, adapter transformations/loss, old writes/new reads, schema IDs, replay/backfill progress, state reconciliation, cache/profile selection, flag cohorts, and telemetry health.

Contraction requires every required consumer migrated/retired/excepted; target semantic/effect success; no unexplained old use across retry/cache/queue/offline/seasonal/DR horizon; healthy evidence; replacement SLO/capacity/security; rollback/recovery updated; notice/support complete; and terminal behavior rehearsed.

Traffic share is not enough. One migrated high-volume client can hide many critical low-volume consumers. Direct attestation and scheduled/recovery rehearsal close dormant gaps.

### Contract, remove, and learn

Stop creation of legacy data/use before removing reads. Reject old writes/calls with the documented terminal response only after entitlement ends; observe fallout and retain abort route if planned.

Remove flags, adapters, aliases, dual writes/reads/serves, routes, schemas, SDK branches, tests, dashboards/alerts, docs, credentials/scopes, state columns, reconciliation jobs, and capacity. Preserve audit, decisions, raw events, backups, and investigation evidence as required.

Verify no hidden dependency remains through code/config/schema/reference/catalog searches and runtime observation. Update ownership/support/runbooks and close exceptions.

Review escaped assumptions, matrix gaps, detection, consumer effort, compatibility tooling, lead time, and legacy duration. Feed lessons into style guides, registries, contract tests, SDKs, and product policy.

## Definitions and Notation

Let $P_t$ be active caller/client/writer versions and $C_t$ active server/consumer/reader versions at time $t$. $A(p,c)$ means their complete interaction preserves the promised contract for relevant inputs, outputs, effects, security, and failure semantics. Safe mixed operation requires $A$ for every actually reachable pair.

Let $H$ be the maximum relevant horizon across deployment, retry, idempotency, cache, queue/retention/replay, offline/seasonal, rollback, backup, and disaster paths. Let credible required logical consumers be $U$ and confirmed migrated $M$, with $m=M/U$ for $U>0$; this is distinct from new-request share.

An **expansion** adds compatibility capacity before dependence. **Migration** moves and verifies consumers/data/effects. **Contraction** removes legacy support after gates. A **canonical model** is the authoritative internal meaning to which representations map; it is not automatically one wire schema.

## Mechanisms, Invariants, or Proof Structure

**Pairwise matrix argument.** During rolling deployment, routing can pair old/new clients with old/new servers. Testing only new/new leaves old/new, new/old, and old/old unproved. Safety requires every reachable cell or routing that makes an unsafe cell unreachable with evidence.

**Reader-before-writer invariant.** If a new writer emits representation $x$ before reader $r$ can accept $x$, routing/replay can deliver $x$ to $r$ and fail. Deploying all relevant readers first removes that failure cell before emission; rollback readers must also remain compatible.

**Traffic counterexample.** One migrated consumer generates 99.9% of calls while 100 unmigrated consumers generate 0.1%. New-traffic share is 99.9%, yet consumer migration can be $1/101\approx0.99\%$. Traffic cannot prove contraction readiness.

**Floating tolerance counterexample.** A parser silently accepts unknown misspelled security field `autorization_scope` and applies a default. Producers come to depend on the typo and attackers exploit ambiguity. Broad permissiveness creates an accidental contract; bounded extensibility plus explicit rejection avoids this ossification/security failure.

Operational invariants are: active population/matrix explicit; reader/server expansion before emission/dependence; old semantics preserved when capability absent; canonical/conflict rules deterministic; adapters secure/idempotent/observable; state/effects/replay included; rollback stage-specific; evidence per consumer/outcome; temporary paths owned/expiring; contraction conjunctive; and cleanup complete.

## Alternatives and Trade-Offs

Additive in-place evolution minimizes surface count but accumulates optionality/ambiguity. New version/operation is clearer but duplicates support and requires migration. Choose from semantic distance, consumer capability, horizon, and lifecycle cost.

Server-side adapters centralize migration and update instantly but add latency/blast radius and may lack consumer context. Client/SDK adapters distribute load/context but depend on consumer releases—the constraint being reduced. Prefer provider-owned boundary for compatibility, then remove it after migration.

Dual write accelerates cutover but creates divergence/partial failure. Backfill plus canonical write is simpler but takes time and may lag. Use outbox/projection/reconciliation when dual representation is unavoidable.

Capability negotiation avoids many major versions but can create combinatorial behavior, cache/security risks, and permanent flags. Coherent profiles or explicit versions are better for large semantic changes.

Strict readers expose defects early but reject legitimate extensions. Tolerant readers support bounded evolution but can hide producer bugs. Specify ignorable extension points and reject ambiguous/unsafe inputs.

Long overlap accommodates slow/offline consumers and rollback but costs complexity/security. Short overlap reduces debt but externalizes migration risk. Derive horizon from evidence and provide explicit exceptions, not wishful dates.

## Failure Modes and Misconceptions

- “Independent releases mean no coordination.” The contract, signals, policy, and evidence coordinate participants.
- “Additive means safe.” Unknown fields/enums/defaults/semantics can break.
- “Deploy server first.” Safe order depends on request and response directions.
- “New readers with new writers are enough.” Mixed and rollback pairs remain.
- “Old clients ignore unknown JSON.” Strict/generated clients may reject it.
- “Optional cannot break.” Absence/default/authorization/effects can change.
- “Tolerant means accept anything.” Ambiguity and invalid security input must fail.
- “Dual write keeps systems equal.” Partial failure and races cause divergence.
- “Feature flag is not a contract.” Consumers can depend on flagged behavior.
- “User-Agent negotiates version.” It is spoofable/ambiguous and cache-unsafe.
- “Schema registry passed.” Behavioral/generated/runtime compatibility remains.
- “Canary passed.” The cohort may omit old, rare, partner, or recovery paths.
- “Rollback is redeploying old code.” New state/events/effects may be unreadable/irreversible.
- “99.9% traffic migrated.” Consumer completeness may be near 1%.
- “Zero old traffic means safe.” Telemetry failure or dormant cadence can look identical.
- “Leave adapter just in case.” Permanent unowned compatibility code is risk.

## Worked Examples

### Example 1

New response field breaks a strict old mobile decoder. Server gates the expanded representation by an authenticated capability profile while a tolerant app update rolls out; removal follows supported app-version evidence.

### Example 2

Request field changes from absent-default `standard` to new desired `express`. Provider adds explicit `service_level` but preserves `standard` when absent; clients opt in. Default is not flipped silently.

### Example 3

`name` splits into structured fields. Dual read maps to canonical identity, rejects conflicts, preserves old response projection, backfills with provenance, migrates consumers, then contracts.

### Example 4

Protobuf writer reuses deleted field number 7. Compatibility tooling rejects it; number/name remain reserved so old bytes are never reinterpreted.

### Example 5

New writer would emit enum `PAUSED`; old reader performs exhaustive matching. Emission stays capability-gated until readers preserve unknown values or update safely.

### Example 6

Dual database writes partially fail. A transactional canonical write plus outbox-derived legacy projection and idempotent reconciliation replaces the unsafe two-write path.

### Example 7

New event consumer successfully replays current schema but fails five-year-old events. Transitive history/replay tests block removal of its upcaster until retained data is migrated or support changes explicitly.

### Example 8

One client creates 99.9% of calls; 100 low-volume clients remain old. Traffic migration is 99.9%, consumer migration is $1/101\approx0.99\%$; contraction remains blocked.

### Example 9

Rollback binary cannot read new non-null database state. The stage plan keeps expanded old-compatible representation and uses roll-forward correction rather than claiming binary rollback.

### Example 10

After migration, code search finds an incident tool using the old endpoint. Its owner runs a recovery rehearsal on replacement before the route/adapter/credentials are removed.

## Cross-Program Connections

[Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md) supplies evolutionary architecture, branch by abstraction, adapters, boundaries, decision records, and technical-debt control.

[Software Testing & Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) supplies compatibility matrices, contract/differential/property tests, generated-client tests, fault injection, and evidence quality.

[Database Engineering](../../18-database-engineering/ROADMAP.md) supplies online schema change, dual representation, backfill, transactional outbox, consistency, rollback, backups, and reconciliation.

[Data Engineering](../../19-data-engineering/ROADMAP.md) supplies schema evolution, lineage, replay/backfill, pipeline compatibility, data quality, and migration observability.

[Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies mixed versions, rolling deploys, retries/idempotency, ordering, queues, consistency, partitions, recovery, and failure amplification.

[Platform Engineering](../../29-platform-engineering/ROADMAP.md) supplies flags, cohorts, routing, registries, semantic diffs, contract tests, progressive delivery, telemetry, catalogs, and policy gates.

## References

1. Google, [AIP-180: Backwards Compatibility](https://google.aip.dev/180).
2. IETF, [RFC 9413: Maintaining Robust Protocols](https://www.rfc-editor.org/rfc/rfc9413.html).
3. Protocol Buffers, [Language Guide (proto 3): Updating a Message Type](https://protobuf.dev/programming-guides/proto3/#updating).
4. GraphQL Foundation, [GraphQL Specification, September 2025](https://spec.graphql.org/September2025/).
5. IETF, [RFC 9745: The Deprecation HTTP Response Header Field](https://www.rfc-editor.org/rfc/rfc9745.html).
6. Kubernetes, [Deprecation Policy](https://kubernetes.io/docs/reference/using-api/deprecation-policy/).
7. OpenAPI Initiative, [OpenAPI Specification](https://spec.openapis.org/oas/latest.html).

## Exercises

### Exercise 1

Construct the active compatibility matrix and rollout order for old/new mobile clients, gateway versions, server replicas, SDKs, and database schemas where a new request capability and response field are introduced during rolling deployment.

### Exercise 2

Design an expand–migrate–contract plan to rename/split a field, change its default, backfill stored state, and preserve rollback, including conflict, idempotency, cache, generated-client, and removal evidence.

### Exercise 3

One migrated consumer generates 99.9% of requests while 100 consumers remain old. Compute consumer migration, explain why traffic cannot authorize contraction, and define sufficient evidence.

### Exercise 4

Design an event-schema evolution across new producers, old/new consumers, five years of retained events, replay, dual publishing, and regional disaster recovery without coordinated release.

### Exercise 5

Audit a migration that reports “complete” because old traffic is zero. It still has a gateway adapter, capability flag, old SDK, database alias column, queue upcaster, exception, rollback image, and quarterly recovery tool. Decide what can be removed and in what order.

## Answers to the Exercises

### Answer 1

Rows/columns include old/new mobile/SDK request+response behavior, gateway profile/header/cache behavior, old/new server replicas, and old/new code against expanded database state. Test every routable client→gateway→server pair plus server→client response/error, auth, default, unknown field, idempotency/effect, cache key, and rollback. First add nullable/state capacity and deploy servers/gateways that accept old/new request but preserve old absence default and keep old response. Verify old clients against new fleet. Then publish SDK/new client and enable new request/response only for authenticated capable cohort; ensure gateway never routes capability to unsupported replica and cache varies by profile. Observe outcomes, expand cohort, backfill/verify state. Stop new old writes only after all writers/queues/rollback handle new. Keep database expansion while rollback is possible. Contract response/field/state after consumer, cache, retry, offline, rollback, and recovery horizons plus direct evidence.

### Answer 2

Specify old/new meanings and canonical model. Add new structured fields nullable and deploy dual-read translation accepting either; preserve old default when neither supplied, reject conflicting old/new, include canonical request semantics in idempotency fingerprint, and retain authorization/validation. Write canonical new state transactionally and derive old projection; version/watermark an idempotent resumable backfill, coordinate live writes, reconcile semantic counts/effects, and avoid two independent writes. Serve old and new response projections with profile-correct cache keys; test strict/generated old/new clients and errors. Deploy readers before writers. Migrate clients and prove target effects. Stop old writes, keep old reads through queue/cache/offline/rollback horizon, make new constraints only after old data is gone, then deprecate/remove old projection/field/column/adapter/flag/tests/docs. Rollback before point of no return disables new emission while expanded readers/state remain; after it, use tested roll-forward.

### Answer 3

There are 101 logical consumers and only one confirmed migrated, so $m=1/101\approx0.00990099=0.99\%$, despite 99.9% new request share. Request weighting measures volume, not independent obligations, criticality, dormant cadence, or ability to handle target semantics. Require trusted inventory mapping and every required consumer migrated/retired/explicitly excepted; replacement contract/SDK/config; representative semantic/auth/limit/retry tests; target logical operations/business effects; no unexplained old successful or failed use after retry/cache/queue/offline/seasonal/DR horizon; telemetry health/sampling provenance; direct owner attestation for rare/hidden gateway paths; replacement SLO/capacity/security; state/rollback/recovery readiness; notice/support and terminal rehearsal. One unresolved critical consumer blocks contraction even if aggregate traffic rounds to 100%.

### Answer 4

Define event identity/version, key/partition/order/delivery/dedup/effect semantics and full writer-reader matrix including rollback and retained versions. Publish immutable schema and deterministic upcasters; deploy all relevant consumers/readers first so they accept old/new and preserve unknowns safely. Test generated readers against representative five-year replay, poison/malformed events, duplicates/reordering, and effects. Only then enable new producers by cohort/region. Avoid dual publish if it duplicates effects; if necessary, use stable event identity, idempotent consumers, explicit source of truth, reconciliation, and bounded overlap. Keep raw historical events/audit; upcast at read/projection. DR rehearsal restores registry/schemas, old data, queues, consumers, identity/dedup state, and ordering. Contraction waits for every consumer/region/replay/recovery path, retained-history migration or governed support change, no old emission, healthy telemetry, rollback update, and removal of dual topic/upcaster only when no history needs it.

### Answer 5

Zero traffic is hypothesis, not proof: validate telemetry, failed calls, identity, sampling, retention, seasonal/recovery cadence, and consumer outcomes. Inventory each artifact/owner/dependency. Migrate/rehearse the quarterly recovery tool and old SDK consumer first; update or retire rollback image so it reads current state/events. Close or renew the exception through authority only after exact risk evidence. Stop old creation/use, then wait applicable queue/cache/retry/quarterly/DR horizon. Remove consumer-facing old route only after terminal rehearsal and notices. Disable flag cohorts and gateway adapter after no entitled dependency; verify no downgrade/cache path. Remove database alias only after no old readers/writers/backups/restore require it and state reconciliation passes. Remove queue upcaster only after retained/replay/DR history is migrated or retention expires under policy. Finally delete flags/adapters/aliases/SDK/docs/tests/dashboards/credentials and preserve audit/raw history. Order follows dependency graph, not apparent inactivity.
