---
module_id: API-076
program: API & Service Engineering
level: 2
module_number: 76
title: API Caching and Invalidation
status: complete
last_verified: 2026-09-02
---

# API Caching and Invalidation

## One-Page Review

### Governing question

How can an API reuse responses and derived data without crossing authorization boundaries, serving unacceptable state, losing invalidations, or turning cache misses and recovery into dependency overload?

### Essential definitions

- A **cache key** identifies the request/representation context under which a stored value may be reused.
- **freshness lifetime** is how long a response may be reused without validation; **age** is time since generation or successful validation.
- A **validator** such as an entity tag lets a cache ask whether a representation still matches origin state.
- **revalidation** conditionally checks a stale response and can refresh metadata without transferring the full representation.
- **invalidation** marks or removes entries whose dependency state changed.
- **time to live (TTL)** is an eviction/freshness bound; it is not proof that data remains correct until expiry.
- **request coalescing** lets concurrent misses for the same key share one fill.
- A **cache stampede** is synchronized origin load from many misses or expirations.
- **negative caching** stores an absence or error under bounded, explicitly safe semantics.

### Central model, mechanism, or theorem

For a key $k$, let generation/version $v$ identify source state, $t_g$ be origin generation time, $t$ current time, and $F$ freshness lifetime. A stored response is fresh when

$$
A(t)=t-t_g < F.
$$

Freshness permits reuse; it does not prove the origin has not changed. Validation compares the stored validator to current selected representation. Invalidation must be ordered by version: an entry for version $v_f$ may be installed only if no observed invalidation/write version $v_i>v_f$ exists. This prevents a late fill from resurrecting older state.

### Critical invariants

The key includes every request property that changes representation, authorization, tenant, locale, encoding, schema, policy, or consistency. Shared caches store authenticated/private data only under explicit safe rules. `no-store`, `private`, `no-cache`, `must-revalidate`, `max-age`, `s-maxage`, `Vary`, validators, and stale extensions retain their defined scopes.

Every entry has provenance, generation/version, age, freshness, maximum allowed staleness, and invalidation ownership. Writes update the source of truth before publishing a durable/versioned invalidation or use a transactionally coupled alternative. Misses, revalidation, fallback, and cold recovery are concurrency- and load-bounded. A cache never fabricates success for an uncertain write.

### Common failures

Key only by URL; omit tenant or authorization scope; cache `404` during creation; confuse `no-cache` with “do not store”; treat TTL as consistency; generate unstable validators; return `304` for a different representation; delete then a late fill restores stale data; publish invalidation before commit; lose events and never reconcile; flush the fleet; expire hot keys simultaneously; every replica fills independently; hold a global fill lock; cache errors without class-specific TTL; cache mutable objects by reference; serve stale permissions or revocations; hide age/provenance; and let cache failure send peak traffic to an origin sized only for hit load.

### Compact example

One thousand callers request the same cold key while origin latency is 200 ms. Without coalescing, the origin receives 1,000 concurrent fills. A per-key single-flight admits one fill and lets bounded waiters share its result; other callers shed or use permitted stale data. With 50 service instances and only local coalescing, as many as 50 fills remain, so the origin still needs an aggregate miss budget. **Conclusion:** coalescing reduces duplicate work only within its coordination scope.

### Connections

[Content Negotiation](005-content-negotiation.md) and [Conditional Requests](006-conditional-requests.md) define representation selection and validators. [Circuit Breaking and Bulkheads](073-circuit-breaking-and-bulkheads.md), [API-Level Load Shedding](074-api-level-load-shedding.md), and [Backpressure Across Service Boundaries](075-backpressure-across-service-boundaries.md) bound cache/origin failure and recovery.

## Governing Question

For every cached API result, what exact request and security context selects it, how fresh may it be, how is equivalence validated, what source changes invalidate it, and how are fills and recovery kept inside origin capacity?

## Why This Matters

Caching can reduce latency, network transfer, origin cost, hot-key pressure, and failure coupling. HTTP caches can reuse fresh responses and validate stale ones with small conditional exchanges. Application caches can avoid repeated computation and database access. Stale data can sometimes preserve a useful degraded service when an origin is unavailable.

Caching also creates another distributed replica with weaker coordination. A key that omits identity can disclose one tenant's data to another. A delayed invalidation can authorize a revoked user. A cache-aside read racing a write can install old state after the write deletes the entry. A fleet-wide expiration can overload the origin more severely than steady uncached traffic.

RFC 9111 defines HTTP storage eligibility, key selection, freshness, age, validation, and invalidation. RFC 9110 defines selected representations, validators, and preconditions. RFC 5861 defines bounded `stale-while-revalidate` and `stale-if-error`; RFC 9211 defines `Cache-Status` for diagnostics. These standards govern HTTP caches, not arbitrary application coherence, so application caches need equally explicit semantics.

AWS's caching guidance emphasizes hit distribution, eventual-consistency tolerance, local-versus-external cache trade-offs, cold starts, dependency load proportional to fleet size, and request coalescing. The deciding question is not “can this value be cached?” but “can its permitted inconsistency, security scope, and failure load be proved?”

## Prerequisites and Retrieval

Retrieve [Content Negotiation](005-content-negotiation.md), [Conditional Requests](006-conditional-requests.md), [Rate Limits and Quotas](039-rate-limits-and-quotas.md), [Timeout and Deadline Budgets](071-timeout-and-deadline-budgets.md), [Circuit Breaking and Bulkheads](073-circuit-breaking-and-bulkheads.md), [API-Level Load Shedding](074-api-level-load-shedding.md), and [Backpressure Across Service Boundaries](075-backpressure-across-service-boundaries.md).

Retrieve every cache layer (browser, CDN, gateway, proxy, service local, distributed, ORM, database); actual cache keys and normalization; `Cache-Control`, `Vary`, `Age`, `Date`, `Expires`, ETag/Last-Modified behavior; authenticated/shared storage policy; source-of-truth versions and transactions; write/read paths; invalidation transport, retention, ordering, retry, and reconciliation; TTL/staleness rules; capacity/eviction; fill concurrency; origin miss capacity; deployment/autoscaling; and hit/miss/stale/invalidation telemetry.

## Learning Objectives

After completing this module, you can:

1. distinguish HTTP freshness, validation, eviction, invalidation, and application-cache coherence;
2. construct representation- and authorization-safe cache keys;
3. apply HTTP caching directives, age, validators, and conditional requests correctly;
4. choose cache-aside, read-through, write-through, write-behind, or versioned immutable strategies;
5. prevent read/write/fill/invalidation races from resurrecting older state;
6. set freshness and stale policies from semantic harm, not arbitrary performance targets;
7. prevent stampedes, hot-key overload, fleet cold starts, and cache-failure cascades;
8. make negative/error caching, fallback, and write outcomes truthful;
9. observe cache decisions, provenance, staleness, invalidation lag, and origin amplification; and
10. verify security, concurrency, topology, loss, eviction, restart, and recovery behavior.

## Core Exposition

### Separate five cache decisions

For each response answer separately: may it be stored, which future requests may reuse it, how long is it fresh, how is it validated after staleness, and what source changes invalidate it. Eviction is a storage-capacity decision and can occur before freshness expires; expiration makes an entry stale but does not necessarily delete it.

HTTP `no-store` prohibits storage by caches subject to the directive. `no-cache` allows storage but requires successful validation before reuse. `private` limits reuse by shared caches; `public` can explicitly allow shared reuse where other rules permit. `must-revalidate` prohibits stale reuse once stale. Treat directive names by normative semantics, not colloquial English.

Application caches must express equivalent decisions even without HTTP headers. A raw `put(key,value,ttl)` API hides security, version, staleness, and invalidation policy. Wrap it in a domain-owned cache contract.

### Design a complete key

An HTTP cache key includes at least request method and target URI, with representation selection affected by request fields named by `Vary`. Application keys may need tenant/account, authenticated subject or permission class, resource ID, query/filter/sort/page, locale, media type, encoding, API/schema version, feature/policy version, and consistency mode.

Normalize only semantic equivalents. Query parameter order may be irrelevant for one endpoint and meaningful for another; repeated parameters, case, Unicode, percent encoding, empty values, headers, and defaults require canonical rules. A collision is a correctness or confidentiality defect.

Do not put raw secrets or personal data into observable keys/metrics. Use a scoped opaque identifier or keyed digest, protect enumeration, and bound cardinality. A user-specific cache can destroy hit rate; that is preferable to unsafe sharing. Share only when authorization and representation are genuinely equivalent.

`Vary: *` prevents selecting a stored response for reuse; an incomplete `Vary` can serve the wrong language, encoding, origin, or authorization-derived representation. Test actual intermediaries because CDNs and gateways can normalize or ignore unconfigured dimensions.

### Decide storage eligibility and privacy

Do not cache credentials, tokens, one-time challenges, secrets, personalized responses, or rapidly changing authorization state in a shared cache unless a reviewed protocol explicitly makes reuse safe. RFC 9111 restricts shared storage of requests with `Authorization` absent a response directive that allows it.

`Set-Cookie` does not by itself define every caching outcome; configure responses explicitly and test the deployed cache. Avoid relying on an intermediary's undocumented heuristic. For sensitive endpoints prefer explicit `no-store` and defense-in-depth cache configuration.

Encryption at rest does not fix key isolation, stale authorization, or access-control bugs. Cache reads must occur under the same effective security policy as origin reads. If policy changes invalidate eligibility, include policy version or send invalidations.

Negative responses require care. A stable “resource does not exist” can be briefly cached, but tenant visibility, eventual creation, replication lag, and anti-enumeration semantics matter. Never reuse “not authorized” as “not found” across subjects.

### Model freshness, age, and staleness

Freshness is permission to reuse without contacting origin. It is a bounded inconsistency choice: the source can change immediately after generation. Choose lifetime from worst acceptable user/business/security harm, update frequency, invalidation reliability, and origin capacity.

RFC 9111 calculates current age using origin `Date`, apparent age, response delay, and resident time rather than trusting a local `now-generation` shortcut through intermediaries. Use compliant cache implementations for protocol age. Application caches should store monotonic receipt time plus authoritative generation/version where available and handle clock changes.

Separate freshness lifetime from domain validity. A price valid until market close, a credential expiring at a timestamp, and a cache TTL are different constraints; effective reuse ends at the earliest. Do not extend an expired authorization or business record because cache freshness remains.

Jitter expirations to avoid synchronized misses, but never beyond the semantic maximum. Probabilistic early refresh spreads origin work; it is not permission for unbounded stale service.

### Validate representations correctly

An ETag identifies a selected representation version. Strong validators support byte-level equivalence requirements; weak validators can support semantic cache validation but not every range/precondition use. Generate validators deterministically from representation/source version, not process-local hashes or timestamps that change on every serialization.

For stale cached GET, send `If-None-Match` with the stored ETag where available. A `304 Not Modified` refreshes applicable metadata and reuses the stored body; a changed representation returns a full response. `Last-Modified`/`If-Modified-Since` is less precise when timestamp resolution or multiple changes matter.

Representation dimensions must match. An ETag for gzip English v2 cannot validate an uncompressed Swedish body unless the validator intentionally and correctly represents their selected semantics. Preserve `Vary` and request context.

Conditional writes such as `If-Match` prevent lost updates but are not cache invalidation. The origin evaluates state-changing preconditions against authoritative current state; never accept a cache's stale version as authoritative.

### Choose a caching pattern

**Cache-aside** reads cache, loads origin on miss, and writes cache. It is simple but exposes fill/write races and duplicate misses. **Read-through** moves fill into cache infrastructure, which still needs correct key, loader, version, and failure semantics.

**Write-through** updates source/cache in a coordinated path and can improve read-after-write behavior, but dual-write atomicity and other writers remain. **Write-behind** acknowledges before origin commit, adding durability, ordering, conflict, and outcome obligations; use only as an explicit asynchronous write system, not a performance toggle.

**Refresh-ahead** updates before expiry based on demand forecasts; it can waste work and synchronize. **Immutable/versioned keys** avoid in-place invalidation: publish content under version/hash and update a short-lived pointer. This is powerful for assets/configuration but pointer consistency and garbage collection remain.

Local caches minimize latency and network dependence but multiply memory, invalidations, and origin fills by fleet size. A distributed cache centralizes reuse and control but adds a network dependency/hot keys. Multi-tier caches require inclusive/exclusive policy and invalidation at every tier.

### Prevent stale resurrection races

Consider cache-aside: reader R misses and reads source version 7. Writer W commits version 8 and deletes the cache. R then stores version 7, resurrecting stale state until TTL. Delete-after-write alone does not serialize a fill already in flight.

Use versioned values and a per-key high-water mark: store fill version only if it is not older than observed committed/invalidation version. Alternatives include transactional outbox with monotonic versions, compare-and-set, write-through under one serialization boundary, change-data-capture plus reconciliation, or immutable version keys.

Publish invalidation after source commit, otherwise consumers can evict before the new state is visible and refill old data. If publish can fail, use an outbox/change log coupled to commit. Consumers deduplicate and ignore older versions; ordering across partitions/regions must be specified.

Deletion events and tombstones need retention longer than maximum late fill/replay window, or an old update can recreate deleted state. Version comparisons must include epoch/namespace across restores and migrations.

### Design invalidation as a reliable data path

Map source changes to every affected key: direct object, lists, aggregates, authorization views, search, counts, and derived data. Dependency tagging reduces broad scans but tag membership/version is itself state. Prefer namespace/version invalidation to fleet-wide flushes.

Invalidation can be precise, prefix/tag-based, or coarse epoch bump. Precise events reduce churn but risk missing derived keys; coarse invalidation is safe only if origin can absorb refill. Document ownership for dependency graphs.

An invalidation bus needs durable publication, delivery semantics, ordering scope, retries, idempotent application, poison handling, replay, lag objectives, and bootstrap. “Best effort plus TTL” is acceptable only when TTL bounds all semantic harm.

Reconcile periodically from versions/change log so one lost event does not create permanent staleness. On reconnect, a client-side cache must assume missed invalidations unless the protocol proves a continuous sequence; flush or replay from a known offset.

### Prevent stampedes and hot keys

Coalesce concurrent fills per key (“single flight”). Bound waiters, propagate the caller deadline, and release them on success/error/cancellation. Do not hold a distributed global lock whose failure blocks all keys. A lease/lock must expire safely, and late owners must not overwrite newer versions.

Local coalescing creates at most one fill per instance, not per fleet. Combine it with origin bulkheads, miss/revalidation budgets, randomized expiry/early refresh, shared cache, or distributed per-key coordination where justified.

Hot keys can overload one cache shard or network path even at high hit ratio. Replicate read-only hot entries, use local near-cache with invalidation, shard saltable aggregates, or redesign access. Measure per-key concentration without exposing sensitive key material.

Cache penetration sends repeated misses for nonexistent/unauthorized keys. Use safe negative caching, membership filters with false-positive semantics, quotas, and input validation. Attackers can force high-cardinality keys, evict useful entries, and make the origin do work.

### Bound negative and error caching

Classify responses. Stable `404` for an immutable namespace may tolerate a TTL; “not yet replicated,” “not authorized,” throttled, transient `5xx`, timeout, and ambiguous result differ. Do not cache a temporary failure as absence.

Errors can become recovery blockers: cache a `503` for five minutes and the origin may recover immediately while callers still fail. Conversely, no error caching can stampede a failing origin. Use short class-specific TTL, stale-if-error where semantically safe, circuit/bulkhead limits, and explicit observability.

Never cache a write response as authoritative unless keyed by stable operation identity and backed by authoritative outcome storage. A timeout after commit requires idempotency/outcome lookup, not a negative cache entry.

For empty lists/counts, distinguish a valid empty representation from incomplete/failed computation. Cache provenance and completeness with the value.

### Use stale service deliberately

`stale-while-revalidate` can serve bounded stale content while one background validation refreshes it. `stale-if-error` can reuse stale content during an error within the stated window. RFC 9111 prohibits stale reuse where directives such as `must-revalidate` disallow it.

Define domain maximum staleness independently of protocol maximums, and choose the stricter. Stale product descriptions may be acceptable; stale access revocation, inventory reservation, medical direction, or financial balance may not be.

Expose `Age`, freshness/provenance, or a domain timestamp when users/clients need it. A stale response is a successful degraded result only if the contract says so; otherwise return an error or partial-status representation.

Revalidation work competes for origin capacity. Coalesce it and bound background refresh. When the origin is open-circuit or overloaded, do not let every request initiate a doomed validation.

### Treat cache loss as a capacity event

If steady hit ratio is 95% at 20,000 requests/s, origin sees about 1,000 misses/s. A total cache loss exposes up to 20,000/s—20 times steady miss load. An origin sized only for misses collapses before the cache warms.

Protect origin with concurrency/rate budgets, priority, load shedding, and gradual cache warmup. Serve bounded stale entries if valid, prewarm proven hot keys at a controlled rate, and ramp new instances. Do not flush all tiers or deploy an empty fleet simultaneously.

Autoscaling local caches increases cold miss streams. Retain warm capacity, use shared caches, seed snapshots with version checks, or delay full traffic until a bounded warm criterion. Cache restore must not reintroduce expired/revoked state.

Cache outage fallback is not automatically “bypass.” Decide whether to fail/degrade, bypass under a strict origin budget, or use stale local data. Test cache network latency too: a slow cache can be worse than a miss unless its deadline/circuit is bounded.

### Manage capacity and eviction

Set maximum entries/bytes, per-tenant/key-class partitions, object-size limits, and eviction policy. Account for metadata, allocator overhead, replication, serialization, and client-side copies. Reject giant values that evict the useful working set.

LRU/LFU-style policies are approximations and can be polluted by scans. Admission filters, segregated pools, cost-aware eviction, and tenant quotas can protect hot valuable entries. Eviction is expected and must not violate correctness.

Avoid mutable shared object references: one caller modifying a cached object corrupts future responses. Store immutable serialized values or defensive copies; include schema/version and validate on read.

Capacity pressure and invalidation storms can consume CPU/network. Bound invalidation fan-out and metadata while failing safe: false-positive invalidation loses hit rate; false-negative invalidation serves stale state.

### Observe cache truth and value

Measure requests, hits by fresh/stale/validated, misses by absent/expired/evicted/bypassed, fill/revalidation count and coalescing ratio, waiter count/time, origin calls, latency, bytes saved, eviction, entry age/version, invalidation publish/apply lag, dropped/replayed events, and reconciliation repairs.

Hit ratio alone is misleading. A high hit ratio can leak data or serve stale wrong values; a low hit ratio can still protect one expensive hot operation. Report weighted cost saved, correctness/freshness SLO, origin amplification, and user latency.

Use RFC 9211 `Cache-Status` where appropriate to expose standardized handling across HTTP cache layers, while applying security guidance and not leaking sensitive keys/topology. Correlate multiple cache hops and policy versions.

Audit key cardinality and distribution, but hash/redact sensitive dimensions. Sample cache-versus-origin comparisons carefully to detect stale/collision defects without doubling load or exposing data.

### Verify concurrency, loss, and recovery

Test key equivalence/non-equivalence across tenant, authorization, locale, encoding, query order, schema, feature, and policy. Test directive precedence, fresh/stale boundaries, age through intermediaries, ETag stability, weak/strong use, `304`, and invalid headers.

Build deterministic schedules for read miss versus write, fill versus invalidation, two writers, delete/tombstone, late event, duplicate/reordered event, reconnect gap, restore epoch, and multi-region conflict. Assert no lower version overwrites a higher observed version.

Load test cold start, synchronized expiry, hot key, high-cardinality penetration, cache slow/failure, origin slow/failure, invalidation storm, eviction churn, fleet scale-out, and recovery. Verify origin budgets and goodput rather than only cache throughput.

Inject cache corruption, serialization/schema mismatch, huge compressed values, clock changes, lost invalidation, bus lag, and failed fill owner. Check that waiters unblock, locks expire safely, errors are classed, stale limits hold, and the system returns to normal without global flush.

## Definitions and Notation

Let cache key be $k$, source/entry version $v$, generation time $t_g$, current time $t$, age $A(t)$, freshness lifetime $F$, and maximum permitted domain staleness $M$. Let hit ratio be $h$, request rate $\lambda$, and origin miss rate approximately $\lambda_o=(1-h)\lambda$ under stated independence/stability assumptions.

Let $C_f$ be concurrent fills for one key, $I$ service instances, and $B_o$ safe origin fill budget. Local single-flight gives $C_f\le I$ for one simultaneous key wave, not $C_f\le1$ fleet-wide. Let invalidation version/high-water mark be $v_i$ and fill version $v_f$; safe installation requires $v_f\ge v_i$ under the defined total/causal order.

A **hit** reuses stored content; a **miss** consults a loader/origin. **Eviction** removes for capacity/policy. **Expiration** ends freshness. **Validation** checks equivalence. **Invalidation** reacts to dependency change. **Coherence** is the system's guarantee relating cache state to source state.

## Mechanisms, Invariants, or Proof Structure

**Key-safety argument.** If two requests can select different authorized representations, they must not map to one reusable entry. Therefore every representation/security-varying dimension is in the key or reuse predicate. Finding one omitted dimension is a confidentiality/correctness counterexample.

**Version-monotonicity argument.** Maintain per-key observed high-water $v_i$. A fill at $v_f$ installs only when $v_f\ge v_i$ and atomically preserves the maximum. A delayed version-7 fill after version-8 invalidation cannot install. This requires comparable versions, durable/recoverable high-water state or safe reset, and coverage of every writer.

**Miss-amplification argument.** At rate $\lambda$ and hit ratio $h$, steady misses are $(1-h)\lambda$. At total cache loss they approach $\lambda$, an amplification of $1/(1-h)$ over steady misses. With $h=0.95$, amplification is 20. Independence and identical request mix are simplifying assumptions; hot keys and multi-tier caches can be worse or better.

**Coalescing-scope argument.** One in-process single-flight owner bounds concurrent fills per key to one per process. Across $I$ independent instances, the fleet can issue $I$ fills. Thus local coalescing alone does not prove origin-safe recovery.

Operational invariants are: safe keys and storage; freshness distinct from truth; validators bind selected representations; versions never regress; invalidation follows commit and can reconcile loss; fills are bounded; stale/error reuse is explicit; origin survives cache loss; write outcomes remain authoritative; and decisions are observable.

## Alternatives and Trade-Offs

Short TTL reduces stale duration but raises origin load and stampede frequency; long TTL improves hits but enlarges inconsistency. Reliable invalidation can support longer freshness yet adds a distributed data path that can fail.

Local caches are fast and failure-isolating but incoherent and fleet-multiplying. Distributed caches improve sharing and invalidation reach but add latency, hot shards, and correlated failure. Multi-tier designs combine benefits and multiply debugging/invalidation complexity.

Cache-aside is simple but racy. Write-through improves local coherence but needs dual-write correctness. Immutable version keys avoid mutation races but require pointer updates and garbage collection. Refresh-ahead smooths latency but performs speculative work.

Precise invalidation preserves hit rate but needs complete dependency tracking. Tag/prefix/epoch invalidation is simpler and safer against omissions but can cause refill storms. TTL-only bounds complexity but may not meet security or correctness staleness.

Strong consistency often makes caching expensive or inappropriate. Conditional validation can save bandwidth while contacting origin. Sometimes a read replica/materialized view with defined consistency is a better owned data product than a generic cache.

## Failure Modes and Misconceptions

- “TTL keeps data correct.” It only bounds reuse time under the chosen policy.
- “`no-cache` means no storage.” It requires validation before reuse; `no-store` controls storage.
- “URL is the key.” Method, representation, tenant, subject/policy, query, and version can vary.
- “Encryption makes shared caching safe.” Authorization selection and invalidation still apply.
- “ETag is a hash of the resource.” It identifies a selected representation under origin semantics.
- “A `304` has no effect.” It can refresh stored metadata governing reuse.
- “Delete on write solves invalidation.” A pre-write fill can install afterward.
- “Publish then commit is faster.” Consumers can refill old state before commit becomes visible.
- “The bus is reliable enough.” Lost/gapped invalidations require replay or reconciliation.
- “Local single-flight means one origin call.” It means one per coordinating process.
- “High hit ratio proves success.” Wrong/stale/private hits can be catastrophic.
- “Cache failure should bypass automatically.” Origin may only be sized for misses.
- “Negative caching is harmless.” Absence, authorization, lag, and transient error differ.
- “Serve stale on every error.” Directives and domain harm can prohibit it.
- “A global flush repairs coherence.” It can create a fleet-wide origin outage.
- “Eviction is failure.” It is normal capacity behavior, but must not affect correctness.
- “The cache is faster.” A slow network cache needs deadline and circuit protection.

## Worked Examples

### Example 1

`GET /profile` is keyed only by URL in a shared cache. Alice's authenticated response is reused for Bob. Adding a user header to `Vary` may still expose identifiers and depend on intermediary support; the safe design marks it private/no-store or keys an explicitly authorized private cache by opaque subject and policy version.

### Example 2

A response has freshness lifetime 60 seconds and current age 45 seconds, so it is fresh for cache purposes. The origin changed at second 10 after generation; freshness does not reveal that. The API accepts up to 60 seconds inconsistency or requires invalidation/shorter validation for the domain.

### Example 3

A cached response has ETag `"v17-json-en"`. Revalidation with matching `If-None-Match` returns `304`, so the cache reuses the body and updates applicable metadata. A gzip French representation uses a different selected-representation validator and key dimensions.

### Example 4

Reader R loads version 7 after a miss. Writer W commits version 8 and publishes invalidation 8. R finishes late. A naive cache stores 7; the versioned cache compares $7<8$ and rejects the fill. The high-water mark prevents stale resurrection.

### Example 5

One thousand callers miss one key. Per-key coalescing on each of 50 instances reduces 1,000 fills to at most 50, not one. A shared miss budget permits ten concurrent origin fills and bounded stale service handles the rest. Coordination scope is included in the capacity proof.

### Example 6

Traffic is 20,000 requests/s with 95% hits, so steady origin misses are $0.05\times20{,}000=1{,}000$/s. Total cache loss exposes 20,000/s, 20 times steady miss load. The origin budget sheds excess and the cache warms gradually by hot-key priority.

### Example 7

A `404` for a just-created eventually replicated object is cached for an hour. Users see absence long after replication. The corrected policy distinguishes immutable missing IDs from “not yet visible,” uses a short class-specific negative TTL, and invalidates on creation.

### Example 8

Ten thousand hot entries all use exactly 300-second TTL after a deploy. They expire together and overwhelm the database. The service uses bounded random early refresh, per-key coalescing, origin fill tokens, and maximum-semantic-TTL-respecting jitter.

### Example 9

An access revocation event is lost while a client cache is disconnected. On reconnect it continues serving the old permission because no new event arrives. The protocol detects a sequence gap and flushes/replays from a checkpoint; permissions also have a strict maximum validity independent of ordinary cache TTL.

### Example 10

A distributed cache starts taking 800 ms while origin normally takes 100 ms. A client waits one second for cache before falling back, exhausting its deadline and bulkhead. A short cache deadline/circuit permits controlled origin bypass within a miss budget; cache latency is monitored separately from hit/miss.

## Cross-Program Connections

[Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies replication, causal ordering, versioning, messaging, failure, and consistency models for invalidation.

[Data Engineering](../../19-data-engineering/ROADMAP.md) connects change-data capture, outbox logs, materialized views, watermarks, replay, and reconciliation.

[Security Engineering](../../25-security-engineering/ROADMAP.md) governs authorization-aware keys, private storage, revocation, side channels, poisoning, and sensitive telemetry.

[Platform Engineering](../../29-platform-engineering/ROADMAP.md) owns shared cache clients, safe defaults, fleet warmup, invalidation infrastructure, observability, and failure drills.

[Systems Engineering](../../26-systems-engineering/ROADMAP.md) frames caches as feedback/capacity systems with hot spots, correlated expiry, common-mode failure, and recovery load.

[Data Architecture Engineering](../../20-data-architecture-engineering/ROADMAP.md) provides source-of-truth transactions, isolation, versions, indexes, replicas, and change logs.

## References

1. IETF, [RFC 9111: HTTP Caching](https://www.rfc-editor.org/rfc/rfc9111.html).
2. IETF, [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html).
3. IETF, [RFC 5861: HTTP Cache-Control Extensions for Stale Content](https://www.rfc-editor.org/rfc/rfc5861.html).
4. IETF, [RFC 9211: The Cache-Status HTTP Response Header Field](https://www.rfc-editor.org/rfc/rfc9211.html).
5. Amazon Web Services, [Caching challenges and strategies](https://aws.amazon.com/builders-library/caching-challenges-and-strategies/).
6. Redis, [Client-side caching introduction](https://redis.io/docs/latest/develop/clients/client-side-caching/).

## Exercises

### Exercise 1

Design caching for a multilingual, compressed product API with public descriptions, tenant-specific prices, and authenticated inventory. Specify keys, directives, validators, freshness, stale policy, and invalidation.

### Exercise 2

Construct a deterministic cache-aside race between a read fill, update, delete invalidation, and late event. Design a version protocol that prevents regression across restart and explain its assumptions.

### Exercise 3

A service receives 50,000 requests/s at 98% hit ratio across 100 local-cache instances. Calculate steady miss rate, full-loss amplification, and worst same-key local-coalesced fills. Design origin protection and warmup.

### Exercise 4

Classify cache policy for `200` public data, personalized `200`, stable `404`, replication-lag `404`, `401/403`, `429`, `503`, timeout, and ambiguous write. State why status alone is insufficient.

### Exercise 5

Create a cache verification plan covering HTTP directives/validators, security key separation, invalidation loss/order, stampede, hot keys, eviction, cache latency/failure, fleet rollout, and recovery. Define pass invariants and metrics.

## Answers to the Exercises

### Answer 1

Key public descriptions by product, locale, selected media/schema version, and content encoding; use explicit public freshness, `Vary` for negotiated fields, and representation-specific ETags. Tenant prices require tenant/contract/currency/policy version and usually private application/shared-cache rules. Inventory requires short freshness or validation/invalidation consistent with reservation semantics and must not be shared across unauthorized contexts. Publish versioned invalidations after source commit for product, tenant price, and inventory dependencies; use maximum staleness per field. Stale descriptions may be allowed with age, while stale tenant price/inventory may require revalidation/error. Coalesce fills and protect origin.

### Answer 2

Schedule R miss/read version 7; W commit 8; W outbox invalidation 8; cache applies/delete-high-water 8; R attempts fill 7; delayed duplicate invalidation 7 arrives. Store values with monotonic source version and atomically install only when fill version is at least the durable observed high-water; invalidations set max(current, event version), so both late operations cannot regress. Persist/rebuild high-water from a durable ordered change log or use an epoch/version namespace after restart. Assumptions are comparable versions covering every writer, invalidation publication coupled after commit, and safe reconciliation for gaps.

### Answer 3

Steady misses are $(1-0.98)\times50{,}000=1{,}000$/s. Full loss can send 50,000/s, a 50-times amplification. For one simultaneous hot key, local single-flight permits up to 100 origin fills. Apply a fleet/origin token budget, per-key coalescing, randomized refresh/expiry, bounded stale service, cache/dependency bulkheads, and load shedding. Warm hot keys at a controlled rate, ramp traffic/instance cache windows, retain warm instances/shared tier, and monitor origin calls, goodput, queue, and invalidation freshness.

### Answer 4

Public `200` can use explicit shared freshness/validators; personalized `200` is private/no-store or securely subject-keyed. Stable immutable `404` may get a bounded negative TTL; replication-lag `404` needs short/no caching and creation invalidation. `401/403` depend on subject/policy and generally should not be shared; revocation risk dominates. `429` is scope/reset-specific and caching can deny other tenants. `503`/timeout are transient; short collapse/stale-if-error may protect origin only under policy. An ambiguous write is never negative-cached as failure: preserve operation identity and query authoritative outcome. Method, phase, identity, scope, source semantics, and retry/stale harm—not status alone—decide.

### Answer 5

Build a request-key matrix for tenant, subject/policy, locale, encoding, query, schema, and feature. Verify storage/directive precedence, age/fresh boundary, ETag stability and selected representation, `304`, `no-store`, `no-cache`, private/shared, and stale limits. Schedule fill/write/invalidation/delete races, duplicates, reorder, loss, gaps, restart, and reconciliation; assert versions never regress. Load test cold fleet, synchronized expiry, hot/high-cardinality keys, cache latency/outage, origin outage, eviction churn, and recovery. Pass invariants: no cross-security reuse, bounded staleness, no old-version install, truthful writes, bounded fills/origin load, waiter release, safe stale/error policy, and recovery without global flush. Metrics cover cache decisions, age/version, coalescing, origin amplification, invalidation lag/gaps, repairs, eviction, and goodput.
