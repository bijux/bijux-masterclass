---
module_id: SARCH-047
program: Software Engineering: Software Architecture
level: 1
module_number: 47
title: Caching Layers and Invalidation Boundaries
status: complete
last_verified: 2026-09-06
---

# Caching Layers and Invalidation Boundaries

## One-Page Review

### Governing question

Where may an architecture reuse a previously computed representation, and how should it bound identity, authority, freshness, invalidation, capacity, privacy, and failure across every cache layer?

### Essential definitions

- A **cache** stores a reusable result nearer to a consumer or cheaper execution path than its authority.
- A **cache key** identifies reuse scope; correctness requires every input that can change the permitted result, including tenant, principal, authorization, representation, locale, and version where relevant.
- A **hit** returns a cached representation; a **miss** consults another layer or authority; **hit ratio** alone says nothing about correctness or miss cost.
- **freshness lifetime** is the interval during which policy permits reuse without revalidation; **age** measures time since the relevant origin event under defined clocks.
- **invalidation** makes an entry ineligible because the underlying truth, authorization, policy, or representation changed.
- **revalidation** asks authority whether a stored representation remains usable, often by version or validator.
- **cache-aside**, **read-through**, **write-through**, **write-behind**, and **refresh-ahead** place read, write, and refresh responsibilities differently.
- A **stampede** occurs when many consumers regenerate the same missing or expired entry concurrently.
- A **negative cache** stores an absence or failure result; its safe lifetime can be much shorter than a positive value.
- **stale-while-revalidate** serves bounded stale data while one refresh proceeds; **stale-if-error** permits bounded stale use during failure.
- A **coherence domain** is the set of cached copies and changes subject to one consistency and invalidation policy.

### Central model, mechanism, or theorem

Model a cached representation as $C=(k,v,s,a,f,p)$: complete key $k$, value $v$, authoritative source/version $s$, stored or validated time $a$, freshness policy $f$, and authorization/purpose context $p$. A hit is permitted only if key equality, authority, policy, and freshness predicates all hold.

With hit ratio $h$, hit latency $L_h$, and miss latency $L_m$, simplified expected latency is

$$
E[L]=hL_h+(1-h)L_m.
$$

At request rate $\lambda$, simplified authority demand is $\lambda(1-h)$ only when misses cause one authority request and refresh, retries, fan-out, write traffic, and stampedes are absent. These are capacity models, not correctness proofs.

### Critical invariants

- name the authority, representation, purpose, and maximum acceptable staleness before introducing a cache;
- include every response-varying and authorization-varying input in the key or prohibit shared reuse;
- preserve source version, observation time, freshness, and completeness with the value;
- define invalidation ownership and every change that affects eligibility, not merely data-row updates;
- ensure stale use is safe for the named operation; never infer current authorization or safety from an old value;
- bound entry bytes, cardinality, tenant share, lifetime, refresh, retries, concurrency, and miss amplification;
- collapse or pace refreshes and keep origin admission independent of cache success;
- distinguish absence, transient failure, authorization denial, and redaction in negative caching;
- make warming, rebuild, eviction, regional loss, and rollback safe and observable;
- test multi-layer variation, update races, delayed invalidation, stampede, cache failure, poisoning, and privacy deletion;
- observe user outcomes, source load, hit and miss latency, age served, invalidation lag, evictions, and errors separately.

### Common failures

Common failures include adding a cache without a freshness contract; keying personalized data only by URL; caching authorization decisions past revocation; confusing expiry with invalidation delivery; deleting then writing under cache-aside and allowing a stale refill; refreshing every replica simultaneously; treating a 99% hit ratio as safe origin capacity; negative-caching transient failure; caching partial responses as complete; using mutable objects without version; placing a write-behind cache in front of an authority without loss semantics; and assuming one layer's purge reaches browser, CDN, gateway, application, and database caches.

### Compact example

Traffic is 20,000 reads/s, hit ratio is 0.96, cache-hit latency is 4 ms, and miss latency is 180 ms. Simplified origin read demand is $20{,}000(1-0.96)=800$/s. Expected latency is $0.96(4)+0.04(180)=11.04$ ms. If cache loss sends all 20,000/s to an origin safe at 2,000/s, the design is unsafe despite its normal average. Origin admission, staged warming, request coalescing, and degradation must cover the cold path.

### Connections

[SARCH-041](041-system-of-record-boundaries.md) identifies authority; [SARCH-043](043-synchronous-request-response-integration.md) supplies deadlines and fan-out; [SARCH-046](046-api-gateway-and-edge-architecture.md) supplies shared-edge variation. [SARCH-048](../ROADMAP.md) next examines deployment units. Database Engineering owns buffer and query-cache internals; Distributed Systems owns replication and consistency theory.

## Governing Question

Caching trades freshness and state-management complexity for latency, availability, cost, or origin protection. It appears in processors, operating systems, databases, applications, gateways, CDNs, browsers, clients, and domain projections. Each layer can reuse a different representation under different authority and trust.

The architectural task is to define what may be reused, for whom, for how long, after which changes, under which failures, and with what evidence. “Put it in Redis” or “add a CDN” names a mechanism, not a correctness policy.

## Why This Matters

A cache hit can remove milliseconds, database work, network transfer, and money. It can also return a deleted user's data, an old price, revoked access, a partial response, or a value from another tenant. Invalidation messages can be delayed. Expiration can synchronize traffic into a stampede. A cache outage can expose an origin that was sized only for misses.

Caches are derived state. Their authority comes from a source and a policy permitting reuse. The safest design treats rebuild and bypass as normal lifecycle paths, makes staleness visible where it matters, and never lets cache convenience redefine business truth silently.

## Prerequisites and Retrieval

Retrieve authority, representation, key, value, version, identity, principal, tenant, authorization, freshness, staleness, expiry, invalidation, revalidation, consistency, transaction, race, concurrency, queue, latency, throughput, capacity, eviction, privacy, observability, and recovery.

From SARCH-018 retrieve evidence; SARCH-024 supplies runtime interactions; SARCH-041 supplies source-of-record boundaries; SARCH-042 supplies storage placement; SARCH-043 supplies synchronous failure; SARCH-044 supplies invalidation messages; and SARCH-046 supplies edge and identity variation.

## Learning Objectives

After completing this module, you should be able to:

1. identify cache authority, representation, consumers, purpose, and staleness budget;
2. construct a complete cache key across identity, authorization, content negotiation, and version;
3. compare cache-aside, read-through, write-through, write-behind, and refresh-ahead;
4. reason about update and invalidation races with versions;
5. design bounded stale and failure behavior by consequence;
6. prevent stampedes, hot-key collapse, and cold-cache overload;
7. size normal and failure-path capacity using hit and miss demand;
8. evolve, warm, evict, rebuild, and retire caches safely;
9. protect multi-tenant privacy and resist poisoning;
10. test and observe freshness, correctness, load, and user outcomes across layers.

## Core Exposition

**Start from the reuse contract.** State the question answered by the representation, its authority, input identity, consumers, data classification, required completeness, maximum age, and consequences of error. Product catalog thumbnails tolerate different staleness from account permissions or medication interactions.

If no safe freshness bound exists, use revalidation or current authority. “Eventually consistent” does not specify how stale, which order, or what users may do with the result.

**Distinguish representation from entity.** A cached value may be an entity record, filtered view, aggregate, authorization-dependent document, rendered page, query result, or failure. Its identity includes every input that can change permitted bytes or meaning.

Two requests for `/account/7` are not equivalent if tenant, principal, role, field mask, locale, currency, API version, encoding, or experiment changes the response. Either include relevant dimensions in the key and validation policy or forbid shared caching.

**Name the authority and version.** Store source identity, source version or validator, observation time, schema/representation version, and completeness with the value. A timestamp generated by the cache is not necessarily source freshness.

Versions enable conditional revalidation and race rejection. A later-arriving update with source version 41 must not replace version 42 merely because its cache write happens later. If version comparison is unavailable, invalidation and refill races need other coordination or a deliberately weaker contract.

**Choose placement by purpose.** Browser and client caches reduce network use but are difficult to purge. CDN and edge caches absorb global reads but cross trust and geography. Gateway caches see API context. Application caches reuse domain representations. Database caches reuse pages or plans under engine mechanisms.

Each layer has separate keys, eviction, freshness, visibility, and operators. Draw them all. Purging the application cache does not remove an already fresh browser response.

**Understand cache-aside races.** In cache-aside, application reads cache, fetches authority on miss, then stores. Writes update authority and invalidate or update cache. A read can fetch old value before a write commits, then store it after invalidation, resurrecting stale data.

Mitigations include versioned values with compare rules, invalidation after commit plus delayed second invalidation, short bounded lifetime, serialization for critical keys, or read-through designs tied to change versions. Each has assumptions. Deleting a key is not a universal coherence protocol.

**Compare write paths.** Read-through delegates miss loading to cache infrastructure. Write-through commits cache and authority along an agreed path, but cross-system atomicity and partial failure remain. Write-behind acknowledges before authority persistence, improving write latency while making cache durability, ordering, loss, and reconciliation part of system-of-record semantics.

Use write-behind only when loss and conflict semantics are explicit and the cache layer is engineered as durable authority or journal. Do not place it casually before financial or safety state.

**Define freshness and revalidation.** Time-to-live is a policy after which reuse requires refresh or rejection. It does not guarantee updates propagate sooner, clocks agree, or the value was fresh when stored. Revalidation uses a source version or validator to avoid retransmitting unchanged content while consulting authority.

HTTP caching distinguishes freshness, validation, cache controls, and shared versus private caches [1]. These ideas generalize, but application caches must define their own domain semantics rather than copying header names mechanically.

**Use stale behavior by consequence.** Stale-while-revalidate can reduce latency and collapse refresh when bounded stale information remains useful. Stale-if-error can preserve availability when authority fails. Both need maximum age, eligible operations, source/version display where useful, and a prohibition list.

Never use stale data to grant revoked access, declare scarce inventory reserved, infer “no allergy,” or make another irreversible decision unless the domain explicitly establishes a safe rule. The same cached record may be safe for display and unsafe for action.

**Design invalidation around changes in eligibility.** Invalidation triggers include source data, authorization, tenant membership, policy, pricing, feature configuration, schema, representation code, key derivation, consent, legal hold, and deletion. Listing only database writes is incomplete.

Assign an owner and delivery model. Invalidation can be synchronous with write, transactional outbox event, version polling, short expiry, or epoch change. At-least-once invalidations must be idempotent; missed invalidation needs bounded recovery through version or expiry.

**Treat expiry and eviction separately.** Expiry is policy-based ineligibility. Eviction removes an entry for capacity. A valid entry can be evicted; an expired entry can still consume storage until reclaimed. Neither proves source change.

Eviction algorithms approximate value under workload. Size, frequency, recency, regeneration cost, tenant fairness, and priority matter. One tenant or hot scan must not evict every critical shared entry.

**Prevent stampedes.** When a hot entry expires, thousands of misses can hit authority simultaneously. Use per-key request coalescing or single flight, randomized expiry, refresh-ahead, bounded stale service, leases, and origin admission. Always bound waiters and refresh time.

A lock service can itself fail or become hot. Lease holders may pause and finish after expiry. Version checks prevent stale refresh from overwriting newer values. Serve a controlled error rather than letting cache failure collapse the origin.

**Plan the cold path.** If hit ratio is $h$, simple origin read demand is $\lambda(1-h)$. But total cache loss changes $h$ toward zero. The origin may also face refresh bursts, retries, writes, and other traffic. Either capacity supports the failure path or the architecture sheds, degrades, or warms traffic gradually.

Warm from authoritative bounded scans or observed safe keys. Do not replay sensitive keys into the wrong tenant or environment. Warming every entry may overload authority and fill the cache with cold data.

**Interpret hit ratio with latency distribution.** Expected latency can improve while tail misses remain slow. A 99% hit ratio still gives one million misses per second at 100 million requests/s. Segment by operation, tenant, key, age, and result type.

Measure hit and miss latency separately, including refresh queue and origin time. A high negative-cache hit rate may mean an attack or a broken publisher, not success.

**Cache absence carefully.** Negative caching prevents repeated work for genuine stable absence. Key it with the same identity and authorization dimensions as positive results. Use shorter lifetime when creation may occur soon.

Do not cache transient timeout as “not found,” authorization denial as global absence, or a partial search as empty. Otherwise an outage becomes durable false data. Preserve result class and authority evidence.

**Handle partial and composite results.** An aggregator may combine several sources. Cache the whole only if completeness, versions, authority, and variation are defined. Otherwise one failed optional branch can be stored as a complete empty field long after recovery.

Component caching allows separate freshness but complicates assembly and consistency. State whether a response can mix source versions and how clients learn partial or stale status.

**Protect multi-tenant and private data.** Separate key namespaces and authorization context. Limit administrative listing and debugging; keys themselves can reveal identities or queries. Encrypt where required, restrict operators, and avoid sensitive values in logs or metrics.

Deletion must reach cache layers, replicas, backups, and client-held copies according to authority and legal policy. Short TTL reduces exposure but is not proof of immediate deletion. A purge needs confirmation or residual-risk handling.

**Resist poisoning.** A cache can store attacker-controlled responses under keys later used by victims. Validate host, route, forwarding data, content negotiation, and origin authority. Do not let untrusted headers affect origin response without also affecting the key.

Separate environments and tenants. Authenticate invalidation and warming operations. Limit object size and serialization types; do not deserialize executable or unsafe objects from a shared cache.

**Evolve keys and values safely.** Schema, serialization, compression, semantics, and key derivation change. Include a stable namespace or version so old and new readers do not misinterpret bytes. Deploy readers that understand coexistence before writers publish new formats.

Version changes can double cardinality and origin load during rollout. Budget memory and misses, warm deliberately, and retire old namespaces after supported rollback ends. Never mass-delete without protecting the origin.

**Design regional behavior.** Regional caches reduce latency and isolate failures but serve different versions. Global invalidation has propagation delay and control-plane dependencies. Define per-operation staleness and whether regional failover may use a colder or older cache.

A global cache can reduce divergence but adds distance and shared blast radius. Hybrid designs use regional data with source versions and invalidation streams. Select from latency, consistency, privacy residency, availability, and cost.

**Keep cache out of authority unless intentionally promoted.** A cache is normally disposable derived state. Backups and recovery focus on authority; cache rebuild must be tested. If writes are acknowledged only in cache or unique facts exist there, it has become an authoritative store and needs corresponding durability, consistency, audit, and recovery.

Calling it a cache does not reduce those obligations. Document the actual role.

**Observe freshness and correctness.** Record hits, misses, bypasses, revalidations, refreshes, coalesced waiters, stale serves by age, invalidations sent/applied, version regressions rejected, evictions, memory, cardinality, origin load, and errors. Avoid unbounded high-cardinality labels.

Reconcile sampled cached values with authority using version and semantic checks. Synthetic probes cover tenant separation, invalidation, expiry, cold start, and stale policy. A latency dashboard alone cannot detect wrong data.

**Test races and failure.** Schedule read-before-write, write-before-fill, invalidation delay, duplicate and missing invalidation, clock skew, lease expiry, refresh crash, old-version arrival, cache partition, total loss, corrupted value, serializer mismatch, and origin overload.

Test privacy purge, revoked access, tenant key collision, cache poisoning, regional failover, configuration rollback, namespace migration, and browser/CDN/application interactions. Assert returned authority, version, age, and business consequence.

**Know when not to cache.** Avoid caching when work is cheap and low-volume, data is unique, freshness is immediate and consequence high, key variation is unbounded or unknowable, invalidation cannot be bounded, or caching increases operational risk more than it reduces cost.

Optimization follows measurement. First remove unnecessary calls, improve authoritative query shape, or use an intentional projection. A projection can have domain-owned update and freshness semantics; hiding it as an anonymous cache can obscure those responsibilities.

## Definitions and Notation

Let entry $e=(k,v,s,a,f,p)$ contain complete key $k$, representation $v$, source and version $s$, validated time $a$, freshness policy $f$, and principal/tenant/purpose policy $p$. Eligibility at time $t$ is a predicate $eligible(e,request,t)$, not merely key presence.

Let request rate be $\lambda$, hit ratio $h$, cache-hit latency $L_h$, and miss latency $L_m$. Simplified expected latency is $hL_h+(1-h)L_m$. Simplified miss demand is $\lambda(1-h)$ under one-origin-call-per-miss assumptions.

For token or data update version $q$, a cache write with version $q_1$ may replace $q_0$ only under the source's comparison relation. Wall-clock arrival order is not a substitute for authoritative version order.

Let freshness age be $age=t-t_{validated}$ only under a defined clock. Maximum usable age $F(operation,purpose)$ can differ for display, decision, and effect.

## Mechanisms, Invariants, or Proof Structure

**Authority invariant.** Every value names its authoritative source and representation semantics; a hit never promotes the cache silently to truth owner.

**Key invariant.** Equality includes every input that changes allowed bytes, meaning, authorization, tenant, or representation, or shared reuse is prohibited.

**Freshness invariant.** Every operation has a maximum usable age and failure rule; entry presence and TTL configuration do not alone prove eligibility.

**Version invariant.** Older authoritative versions cannot overwrite newer versions because of delayed fill, refresh, invalidation, or regional delivery.

**Race argument.** In cache-aside, a miss may read old authority before a concurrent commit and fill after post-commit deletion. Therefore delete-after-write alone cannot exclude stale resurrection without version, serialization, bounded expiry, or another mechanism.

**Capacity invariant.** Entry bytes, key cardinality, tenant share, waiters, refresh concurrency, miss rate, origin work, retries, and rebuild rate remain bounded.

**Failure invariant.** Cold, unavailable, partitioned, corrupt, and misconfigured caches have an origin admission and degradation path that cannot amplify without bound.

**Privacy invariant.** Cache identity, content, operations, telemetry, replicas, and retention preserve tenant isolation, purpose, authorization, and deletion obligations.

**Compatibility invariant.** Key and value versions coexist through deploy and rollback without mass invalidation overwhelming authority.

**Evidence invariant.** Hits, latency, freshness, invalidation, source versions, business outcomes, and user correctness are observed separately.

## Alternatives and Trade-Offs

| Choice | Advantages | Costs and risks | Prefer when |
|---|---|---|---|
| Cache-aside | simple application control | stale-fill races and duplicated logic | bounded reads tolerate explicit policy |
| Read-through | centralized loading | infrastructure gains source coupling | loading semantics are reusable |
| Write-through | cache updated on write path | cross-store partial failure and latency | coordinated semantics are explicit |
| Write-behind | low write latency and batching | loss, ordering, and authority shift | cache/journal is engineered for durability |
| Refresh-ahead | fewer user misses | refresh waste and origin load | hot keys are predictable |
| Revalidation | current authority with low transfer | authority latency and availability | versions are cheap and freshness matters |
| Stale-while-revalidate | low latency during refresh | bounded stale exposure | operation safely accepts known age |
| Stale-if-error | availability during source failure | extended stale decisions | failure consequence permits it |
| Regional cache | low latency and isolation | divergent copies and invalidation lag | regional staleness is bounded |
| Global cache | shared view and reuse | distance and blast radius | shared consistency outweighs locality |
| Domain projection | explicit derived product and lineage | pipeline and ownership cost | reuse has durable business semantics |
| No cache | simple current behavior | origin latency and cost | workload and consequence do not justify cache |

## Failure Modes and Misconceptions

1. **“A cache is only a performance detail.”** It changes freshness, failure, and privacy behavior.
2. **“TTL solves invalidation.”** It only bounds reuse after one timestamp under policy.
3. **“URL is the cache key.”** Identity, authorization, and representation may vary.
4. **“Delete after write prevents stale values.”** A concurrent old fill can arrive later.
5. **“High hit ratio means the origin is safe.”** cold loss and miss bursts can overwhelm it.
6. **“Expiry spreads naturally.”** identical TTLs can synchronize refresh.
7. **“Stale data is better than none.”** some actions must fail closed or revalidate.
8. **“Negative results can use the normal TTL.”** absence and failure have different dynamics.
9. **“A purge reaches every layer.”** clients and intermediaries have distinct state.
10. **“Write-behind is still just a cache.”** acknowledged unique writes make it authoritative.
11. **“Encryption prevents tenant leaks.”** incorrect keys return authorized plaintext to the wrong consumer.
12. **“Cache hit proves complete data.”** partial responses may have been stored.
13. **“A global cache guarantees coherence.”** failures and clients can retain other copies.
14. **“Versioning values is enough.”** key derivation and semantics also evolve.
15. **“Rebuild is harmless.”** it can overload authority and violate privacy scope.
16. **“Fast responses prove correctness.”** stale or poisoned hits can be fast.

## Worked Examples

### Example 1

**Situation.** A service receives 20,000 reads/s with hit ratio 0.96, 4 ms hit latency, and 180 ms miss latency.

**Reasoning.** Simplified miss demand is $20{,}000\times0.04=800$/s. Expected latency is $0.96\times4+0.04\times180=11.04$ ms. These averages omit tail, refresh, retry, and stampede. Total cache loss sends up to 20,000/s toward authority unless admission intervenes.

**Conclusion.** Normal hit economics and cold-path capacity are separate design questions.

### Example 2

**Situation.** An account response is cached by path but varies by tenant and field-level permission.

**Reasoning.** Path equality does not imply authorized representation equality. Include tenant, resource, principal authorization class or an unforgeable representation scope, field mask, API version, locale, and encoding as required. If permission changes faster than invalidation can be bounded, revalidate or disable shared caching.

**Conclusion.** Complete variation is a security invariant, not a cache-efficiency detail.

### Example 3

**Situation.** A cache-aside reader fetches version 7; a writer commits version 8 and deletes the key; then the reader stores version 7.

**Reasoning.** Delete-after-write allowed stale resurrection. Store source versions and reject writes older than the cache's observed epoch/version, or serialize fill with updates. Bounded TTL limits residual exposure but does not remove the race. Reads used for irreversible action query current authority.

**Conclusion.** Cache-aside coherence needs version or coordination beyond deletion order.

### Example 4

**Situation.** Ten thousand clients request one key as its one-hour TTL expires.

**Reasoning.** Deterministic simultaneous expiry creates a stampede. Randomize expiry, refresh ahead for measured hot keys, coalesce one bounded refresh per key, allow bounded stale display while refresh runs, and enforce origin admission. A failed refresher releases or expires its lease without allowing an older value to overwrite a newer version.

**Conclusion.** Stampede control combines scheduling, coalescing, versioning, and origin protection.

### Example 5

**Situation.** Product creation follows a cached `not found` result with a 24-hour negative TTL.

**Reasoning.** Users cannot see the new product for a day. Give stable absence a short domain-specific lifetime or invalidate on creation. Do not negative-cache timeout or authorization denial as absence. Key the negative entry by the same tenant, visibility, and representation dimensions as a positive entry.

**Conclusion.** Negative caching requires its own semantics and usually a different lifetime.

### Example 6

**Situation.** A dashboard combines five sources, one times out, and the incomplete response is cached as normal.

**Reasoning.** Subsequent users receive missing data even after recovery. The aggregate representation records component completeness, source versions, and freshness. Either do not cache incomplete results, give the missing component a narrow negative policy, or cache components separately and assemble with explicit partial status.

**Conclusion.** Composite caches must preserve partiality instead of laundering it into completeness.

### Example 7

**Situation.** A write-behind cache acknowledges bank transfers before durable ledger commit.

**Reasoning.** Cache loss can erase acknowledged transfers; reorder can violate balances; retry can duplicate. Either make the durable ledger commit the acceptance point or promote the cache/journal to a replicated authoritative log with stable operation identity, ordering, recovery, reconciliation, audit, and explicit residual failure semantics.

**Conclusion.** Write-behind is an authority decision when unique acknowledged state exists only in the cache.

### Example 8

**Situation.** A new value format changes the namespace and all instances warm every key simultaneously.

**Reasoning.** Cardinality temporarily doubles and origin load spikes. Deploy readers that understand old and new, warm only measured hot keys under a global budget, shift traffic gradually, observe misses and source saturation, retain rollback namespace, and retire old values after the rollback window.

**Conclusion.** Cache schema evolution is a capacity and deployment event, not just serialization work.

### Example 9

**Situation.** A user invokes privacy deletion, but copies remain in browser, CDN, gateway, and application caches.

**Reasoning.** Inventory each layer and its authority. Prevent future shared reuse, issue authenticated purges where supported, rotate or revoke object references, bound client freshness, delete application entries and replicas, and record residual backup policy. Do not claim immediate deletion when a layer cannot confirm it.

**Conclusion.** Privacy deletion follows the entire coherence domain and reports residual limits honestly.

### Example 10

**Situation.** A hospital cache contains a two-hour-old “no known allergy” result during source outage.

**Reasoning.** Absence is not current safety evidence. Medication administration fails closed or uses an explicitly governed signed local clinical summary whose allowed age, source, patient match, and emergency authority are satisfied. Display may show the stale record prominently, but the action path requires current or approved emergency evidence.

**Conclusion.** Freshness policy is operation-specific; safe display does not imply safe irreversible action.

## Cross-Program Connections

- **Distributed Systems Engineering:** owns replication, consistency, clocks, partitions, invalidation delivery, leases, and coherence theory.
- **Database Engineering:** owns buffer pools, query execution, indexes, materialized views, isolation, and durable storage internals.
- **Data Architecture Engineering:** owns authority, projections, lineage, freshness, privacy, and consumer-purpose contracts.
- **API and Service Engineering:** owns HTTP cache controls, validators, variation, client behavior, and cache-aware errors in depth.
- **Security Engineering:** owns authorization freshness, tenant isolation, poisoning threats, encryption, purge, and sensitive telemetry.
- **Software Delivery and Reliability Engineering:** owns capacity, cold starts, stampedes, observability, rollout, incidents, and recovery.
- **Platform Engineering:** owns shared cache services, quotas, namespaces, telemetry, resilience defaults, and safe self-service.
- **Operating Systems and Computer Architecture:** caches in memory and processors illustrate locality and coherence mechanisms under different contracts.

## References

1. R. Fielding, M. Nottingham, and J. Reschke, *RFC 9111: HTTP Caching*, IETF, June 2022. <https://www.rfc-editor.org/rfc/rfc9111>
2. M. Nottingham, *RFC 5861: HTTP Cache-Control Extensions for Stale Content*, IETF, May 2010. <https://www.rfc-editor.org/rfc/rfc5861>
3. Cary G. Gray and David R. Cheriton, “Leases: An Efficient Fault-Tolerant Mechanism for Distributed File Cache Consistency,” *SOSP*, 1989. <https://doi.org/10.1145/74850.74870>
4. Martin Kleppmann, *Designing Data-Intensive Applications*, O'Reilly Media, 2017.
5. Michael T. Nygard, *Release It! Design and Deploy Production-Ready Software*, 2nd ed., Pragmatic Bookshelf, 2018.
6. R. Fielding, M. Nottingham, and J. Reschke, *RFC 9110: HTTP Semantics*, IETF, June 2022. <https://www.rfc-editor.org/rfc/rfc9110>
7. NIST, *SP 800-207: Zero Trust Architecture*, August 2020. <https://csrc.nist.gov/pubs/sp/800/207/final>
8. Pat Helland, “Data on the Outside Versus Data on the Inside,” *CIDR*, 2005. <https://www.cidrdb.org/cidr2005/papers/P12.pdf>

## Exercises

### Exercise 1

Define cache, cache key, hit, miss, freshness lifetime, age, invalidation, revalidation, cache-aside, read-through, write-through, write-behind, refresh-ahead, stampede, negative cache, stale-while-revalidate, stale-if-error, and coherence domain.

### Exercise 2

A service receives 50,000 reads/s with hit ratio 0.985. Hits take 3 ms and misses 140 ms. Compute simplified miss rate and expected latency. The origin is safe at 4,000 reads/s: compute overload factor after total cache loss and explain why ordinary metrics do not prove safety.

### Exercise 3

Design a cache-aside product-price cache under concurrent writes. Cover complete key, source version, freshness, stale display versus purchase, fill/write race, invalidation delivery, stampede, negative entries, origin admission, and evidence.

### Exercise 4

Compare a browser cache, CDN, gateway cache, application cache, database materialized view, and domain projection for a personalized news page. Address authority, authorization, variation, freshness, invalidation, privacy, capacity, and failure.

### Exercise 5

Design caching for an intermittently connected wildfire-response application. Cover map tiles, road closures, weather, crew assignments, evacuation orders, authorization, source/version and age, stale/offline use, invalidation, capacity, poisoning, privacy, rebuild, and evidence. Identify decisions that cached absence must never authorize.

## Answers to the Exercises

### Answer 1

A **cache** stores reusable derived results. Its **key** defines reuse identity; a **hit** returns an eligible entry and a **miss** consults another path. **Freshness lifetime** permits reuse for an interval; **age** measures time under a defined clock. **Invalidation** removes eligibility after change; **revalidation** asks authority whether a version remains usable. **Cache-aside** puts lookup/fill in application code; **read-through** delegates loading; **write-through** updates cache on the write path; **write-behind** acknowledges before later authority persistence; **refresh-ahead** updates before expiry. A **stampede** is concurrent regeneration. A **negative cache** stores absence or failure. **Stale-while-revalidate** serves bounded stale data during refresh; **stale-if-error** does so during failure. A **coherence domain** is all copies and changes governed by one consistency/invalidation policy.

### Answer 2

Miss rate is $50{,}000(1-0.985)=750$/s. Expected latency is $0.985(3)+0.015(140)=5.055$ ms. Total cache loss offers 50,000/s to an origin safe at 4,000/s, an overload factor of 12.5. The average omits hit and miss tails, refresh and retry traffic, stampedes, request-cost variation, writes, tenant skew, and dependencies. The normal hit ratio says nothing about cold start or cache partition. Origin admission, coalescing, gradual warming, bounded stale policy, and load shedding must be tested under full and partial cache loss.

### Answer 3

Key by product, market, customer price class where authorized, currency, representation and contract version. Store price authority's version, amount, unit, observation time, and completeness. Display may permit a stated bounded age; purchase revalidates or calls current pricing authority. A fill may store only if its source version is not older than the cache epoch/version observed after a concurrent commit. Price authority commits then emits idempotent versioned invalidation through an outbox; expiry bounds a missed event. Coalesce refresh per key, jitter expiry, cap waiters, and protect origin with admission. Negative entries represent genuine invisible/absent products separately from timeouts or denial. Measure age served, invalidation lag, rejected stale writes, misses, origin load, and checkout outcomes.

### Answer 4

Browser caching saves client traffic but is hard to purge and must be private for personalization. A CDN suits public shared assets and only personalized responses with complete safe variation; otherwise it risks disclosure. A gateway cache shares API results but must preserve tenant, principal authorization, version, locale, and completeness. An application cache can reuse owned view fragments with source versions. A materialized view is database-managed derived state under database refresh/transaction semantics. A domain projection is a durable owned read product with lineage and explicit freshness, often clearer than an anonymous cache for news composition. Public articles, personal recommendations, subscription state, and moderation decisions need different policies. Every layer has separate capacity, invalidation, privacy deletion, failure, and telemetry.

### Answer 5

Public map tiles may use long versioned lifetimes; weather and road observations carry source, observation time, region, confidence, and short operation-specific bounds. Crew assignments and evacuation orders carry authoritative signed version and must not be inferred from absence. Offline mode displays age and completeness prominently and permits only actions under explicit delegated local authority; irreversible allocation or “road safe” decisions require current or approved emergency evidence. Keys include incident, jurisdiction, role, map/version, and data class without leaking sensitive identities. Versioned invalidations are authenticated and idempotent; expiry bounds loss. Devices cap storage and tenant/incident share, prioritize current safety data, and rebuild gradually. Validate provenance to resist poisoning, encrypt sensitive crew data, support revocation and device loss, and reconcile local observations after connection. Evidence records which source version informed each decision. Full credit requires that cached absence never authorize safety, availability, evacuation completion, or resource commitment.
