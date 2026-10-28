---
module_id: API-007
program: API & Service Engineering
level: 1
module_number: 7
title: Caching
status: complete
last_verified: 2026-09-01
---

# Caching

## One-Page Review

### Governing question

When may an HTTP cache reuse a stored response for a later request without contacting the origin, and what evidence bounds that reuse?

### Essential definitions

- A **cache** stores HTTP responses and controls their reuse for later requests.
- A **private cache** serves one user agent; a **shared cache** can reuse responses for multiple users.
- A response is **fresh** while its calculated age does not exceed its freshness lifetime; otherwise it is **stale**.
- **Validation** asks an origin or another authoritative cache whether a stored response remains reusable.
- A **cache key** starts with method and target URI and incorporates request fields named by `Vary`.
- **Invalidation** makes stored responses unsuitable after an unsafe request; it is not guaranteed global deletion.
- `no-cache` requires validation before reuse; `no-store` prohibits storage. Their names are historically easy to misread.

### Central model, mechanism, or theorem

For stored response $r$ at time $t$, reuse requires: the response is stored lawfully; the presented request matches its cache key and `Vary` dimensions; method and status permit reuse; authorization rules permit this recipient; and either $current\_age(r,t) < freshness\_lifetime(r)$ or a stale-use/validation rule authorizes reuse. Each premise is necessary; freshness alone is not permission.

### Critical invariants

Never share a response across authorization or tenant boundaries without a proved partition and explicit cache policy. Treat `Vary` as part of the key. Revalidate stale representations with their validators. Preserve metadata updated by `304`. Bound stale service explicitly. Invalidate affected target URIs after successful unsafe methods, while designing domain-specific purge/version mechanisms for related resources. Do not use cache hits as evidence of current authoritative state.

### Common failures

Treating `no-cache` as “do not store”; assuming every GET is cacheable; ignoring `Vary`; caching authenticated personalized responses publicly; resetting age at every proxy; using `max-age` as a promise that origin data stays true; purging one URL while related collections remain stale; collapsing requests across tenants; and serving stale error or permission data without an explicit policy.

### Compact example

A public catalog response carries `Cache-Control: public, max-age=60`, `ETag: "cat-9"`, and `Vary: Accept-Encoding`. A shared cache may reuse the matching encoded variant while fresh. After 60 seconds it sends `If-None-Match: "cat-9"`; a `304` refreshes stored metadata without transferring the catalog body. This reduces load while keeping the origin in the revalidation loop.

### Connections

Headers define `Cache-Control`, `Age`, `Date`, `Vary`, and validators. Content negotiation determines variant keys. Conditional requests drive revalidation. Method semantics govern invalidation and cacheability. Later API modules cover invalidation strategy, latency, gateways, and observability.

## Governing Question

What prior response is being reused, for which request and recipient, for how long, under whose authority, and with what recovery when the stored response is no longer fresh?

## Why This Matters

Caching can remove network round trips, absorb traffic spikes, reduce origin cost, and allow bounded service during failures. It also deliberately returns an earlier response. That trade is safe only when identity, variation, authorization, freshness, validation, and invalidation semantics are explicit.

RFC 9111 defines HTTP cache storage, matching, age, freshness, validation, and invalidation. RFC 9110 defines representation validators and method semantics. RFC 5861 defines the widely used `stale-while-revalidate` and `stale-if-error` extensions. These standards describe protocol permission; an application still owns business tolerance for old data and the security consequences of reuse.

## Prerequisites and Retrieval

Retrieve request methods, target URIs, selected representations, response fields, content negotiation, entity tags, conditional requests, authorization, clocks, and basic failure modes. Recall that a representation can be correct for one user and forbidden for another even when the URI and bytes appear similar.

## Learning Objectives

By the end of this module, you should be able to:

1. distinguish storage, freshness, reuse, validation, invalidation, and deletion;
2. derive a cache key including `Vary` dimensions;
3. calculate a simple freshness decision without resetting response age;
4. distinguish `no-cache`, `no-store`, `private`, `public`, `max-age`, and `s-maxage`;
5. design validator-based revalidation and interpret `304` correctly;
6. bound stale serving and request collapsing under failures; and
7. review personalized and multi-tenant caching for disclosure risk.

## Core Exposition

### Storage is not reuse

A cache first decides whether it may store a response. Later, for a new request, it decides whether a stored response matches and may be reused. A stored response can exist yet require validation before every reuse. Conversely, a response forbidden from storage cannot become reusable merely because it would still be fresh.

Cacheability depends on method, status, explicit directives, authorization context, and cache type. GET responses are the common case, but “GET” alone does not prove safe shared storage. Responses to authenticated requests have additional restrictions. A service should emit explicit policy for sensitive and high-value resources instead of relying on heuristic defaults.

### Cache keys and variants

The primary cache key includes the request method and target URI. `Vary` extends matching with named request fields used to select the response. If the origin selects on `Accept` and `Accept-Language` but names only `Accept`, a stored English representation can match a French request incorrectly. Correctness requires the selection function and cache key to agree.

High-cardinality variation reduces cache efficiency. `Vary: User-Agent` can fragment storage into many nearly unique entries. `Vary: Authorization` is not a complete multi-user security model. For personalized responses, `private` or `no-store` is often safer; a controlled edge cache instead needs an authenticated, non-forgeable partition key and a proof that no response crosses subjects or tenants.

### Freshness and age

Freshness lifetime can come from `s-maxage` for shared caches, `max-age`, `Expires`, or permitted heuristic calculation. Current age incorporates time already spent resident in upstream caches and transport, not just time since the local cache stored the response. The `Age` field communicates an estimate of seconds since generation or validation as required by the age calculation.

A simplified decision is fresh when $age < lifetime$. Production calculation must use RFC 9111's corrected initial age, resident time, response times, `Date`, and `Age` rules. Clock skew and integer bounds matter. A fresh response is reusable only when all other matching and policy conditions hold.

`max-age=60` does not assert that the represented fact remains true for 60 seconds. It permits reuse of this response under the stated cache policy for that lifetime. If stock quantity must never be older than five seconds, freshness policy is one enforcement mechanism, and the domain must still define authority, update latency, and failure behavior.

### Directive semantics

`no-store` tells caches not to store the response (or request, in its request form) under the specification's rules. It reduces persistence but is not a retroactive data-erasure protocol and does not control every non-HTTP log or browser mechanism.

`no-cache` permits storage but requires successful validation before reuse unless a field-name-qualified form applies. `private` restricts a response to private caches. `public` makes an otherwise restricted response eligible for shared caching but does not waive authorization correctness. `s-maxage` supplies a shared-cache freshness lifetime and takes precedence over `max-age` there. `must-revalidate` constrains reuse after staleness when disconnected.

Directive names are protocol tokens, not English summaries. Write tests for actual semantics and inspect the effective response after framework, gateway, and CDN transformations.

### Validation and `304`

When a stored response is stale, a cache can send a conditional request with `If-None-Match` or a date validator. A matching current representation yields `304 Not Modified`. The cache updates stored response metadata according to the rules and reuses the stored content. It must not treat `304` as a new body or return `304` to an unconditional downstream request merely because its upstream validation did.

Concurrent misses or validations for one key can be collapsed into one origin request, with other clients waiting for its result. This reduces stampedes but creates a shared fate and must preserve request variation and authorization partitions. A slow origin, canceled leader, or poisoned first response can otherwise affect many requests.

### Invalidation and related resources

Successful unsafe methods invalidate stored responses for the effective request URI and certain location targets under HTTP rules. This does not discover every representation whose domain content depends on the mutation. Updating `/products/7` may also change `/products`, `/search?q=...`, aggregates, and personalized recommendations.

Related-resource invalidation needs application design: explicit purge keys, surrogate tags, versioned namespaces, short bounded freshness, event-driven purge, or recomputation. Purge delivery is distributed work and can fail. State the maximum staleness during delayed purge and test it; “the CDN is invalidated” is not evidence until acknowledged and observed at each relevant layer.

### Controlled stale service

`stale-while-revalidate` permits serving a stale response for a bounded interval while revalidation proceeds. `stale-if-error` permits bounded stale service when an error occurs. These can improve availability and latency, but are dangerous for revoked permissions, rapidly changing prices, security policy, or commands. Use them only where an older representation is explicitly safer than failure, and expose age or warning evidence where consumers need it.

<!-- bijux-verify: {"id":"freshness-decision","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"age=42 lifetime=60 fresh=True\nage=61 lifetime=60 fresh=False\n","stderr":""}} -->
```python
def is_fresh(age_seconds, lifetime_seconds):
    return age_seconds < lifetime_seconds

for age in (42, 61):
    print(f"age={age} lifetime=60 fresh={is_fresh(age, 60)}")
```

This run verifies only the strict comparison in a simplified example. It does not implement RFC age calculation, storage permission, `Vary`, authorization, request directives, validation, or stale extensions.

## Definitions and Notation

Let $K(r)$ be the cache key derived for request $r$, including all applicable `Vary` dimensions. Let $stored(k)$ be candidate stored responses under key $k$. For response $x$ at time $t$, let $age(x,t)$ be its calculated current age and $life(x)$ its freshness lifetime. Freshness is $Fresh(x,t)\equiv age(x,t)<life(x)$.

A **cache hit** is a request satisfied using a stored response, potentially after validation. A **fresh hit** needs no validation. A **revalidated hit** reuses stored content after an authoritative `304` or equivalent validation result. A **miss** needs a new response. A **cache stampede** is concurrent origin work for the same cacheable result. **Request collapse** coalesces that work under a safe matching key.

## Mechanisms, Invariants, or Proof Structure

For every reuse decision:

1. Determine cache type and whether storage was permitted.
2. Match method, target, and every `Vary` dimension.
3. Re-evaluate authorization and partition assumptions.
4. Calculate current age and freshness lifetime.
5. Apply request and response directives.
6. If required, validate with the best available validator.
7. Update stored metadata correctly after validation.
8. Apply explicitly bounded stale behavior or fail closed.
9. Record cache status, age, key class, and validation outcome without exposing secrets.

The **key-completeness invariant** requires equal keys only for requests permitted to share a representation. The **age-monotonicity invariant** prevents a forwarding cache from resetting an older response to age zero. The **authorization-partition invariant** forbids cross-principal reuse without a proven shared representation. The **bounded-staleness invariant** requires every stale path to have a finite, documented limit.

## Alternatives and Trade-Offs

**Origin cache versus gateway/CDN cache.** Origin-adjacent caches have stronger application context and simpler trust boundaries; edge caches reduce global latency and origin load. Edge designs require precise keys, purge evidence, configuration control, and privacy review.

**Time-to-live versus explicit invalidation.** Short TTLs bound staleness without a purge dependency but increase origin work. Purge can make long-lived content update quickly but introduces distributed delivery and missed-key risks. Mature systems often combine versioned assets, explicit purge, and a finite TTL backstop.

**Cache-aside application data versus HTTP response caching.** Data caches store domain values and require application-defined consistency. HTTP caches store complete responses under HTTP semantics. They can coexist, but invalidating one layer does not automatically invalidate the other.

## Failure Modes and Misconceptions

Fresh means reusable under a protocol lifetime, not true now. `no-cache` does not mean no storage. `no-store` does not erase prior copies or logs. `Vary` does not provide access control. A `304` cannot supply a missing stored body. Purging one URI does not discover dependent queries. Request collapsing without complete keys can merge users. Cache-hit ratio alone rewards unsafe over-caching and says nothing about correctness.

## Worked Examples

### Example 1

A response has lifetime 60 seconds and calculated age 42 seconds. It is fresh under the strict comparison, so a matching authorized request may reuse it without validation. The conclusion still depends on storage, key, and directive premises—not age alone.

### Example 2

The same response reaches age 60. Because freshness uses $age<life$, equality is stale. The cache validates or follows an allowed stale policy. Treating equality as fresh silently lengthens the promised window.

### Example 3

`Cache-Control: no-cache, private` allows a browser cache to store a profile but requires validation before reuse and prevents shared-cache storage. Interpreting `no-cache` as `no-store` loses useful private revalidation; interpreting it as unrestricted reuse risks stale data.

### Example 4

A public response varies on `Accept-Encoding`. The cache stores gzip and identity variants under distinct secondary keys. Omitting `Vary` could send compressed bytes to a client that did not advertise support. Representation metadata alone does not repair the wrong cache match.

### Example 5

A stale catalog entry has `ETag: "c8"`. Revalidation returns `304` with updated freshness metadata. The cache retains the stored body, updates permitted fields, and serves a normal response to its client. It does not forward a bodyless `304` to an unconditional request.

### Example 6

A shared cache stores `/me` publicly because the URI is the same for everyone. User B receives User A's profile. The correct design marks it private/no-store or uses a controlled non-forgeable subject partition proven at every cache layer. `Vary: Authorization` alone is not the default repair.

### Example 7

One hundred requests miss the same public key. Safe request collapse sends one origin request and shares its response only after matching all variation dimensions. Collapsing by path alone could merge languages or tenants, turning load control into disclosure.

### Example 8

Updating `/products/7` invalidates that target, but cached `/products` still lists the old price. The application purges both by a product surrogate key and retains a five-minute TTL backstop. The conclusion is that HTTP invalidation cannot infer domain dependency graphs.

### Example 9

A news page permits `stale-if-error=300`; serving a five-minute-old article is preferable to an outage. An account-permission response forbids stale service because revocation must take effect promptly. Availability policy depends on the represented risk, not one global directive.

### Example 10

A proxy receives an upstream response with `Age: 50`, holds it for 20 seconds, then forwards it. It must not report age near zero; downstream reasoning must reflect accumulated residence. Resetting age makes a stale response appear fresh and violates age monotonicity.

## Cross-Program Connections

[Content Negotiation](005-content-negotiation.md) defines variant dimensions, [Conditional Requests](006-conditional-requests.md) defines revalidation, and [Headers and Metadata](004-headers-and-metadata.md) defines field trust. Distributed systems explains purge delay and partitioned evidence; security engineering owns cache disclosure threats; data engineering distinguishes response reuse from source-data caching.

## References

- Fielding, R., Nottingham, M., and Reschke, J. *HTTP Caching*, RFC 9111, IETF Standards Track, June 2022. Retrieved 2026-09-01. https://www.rfc-editor.org/rfc/rfc9111.html
- Fielding, R., Nottingham, M., and Reschke, J. *HTTP Semantics*, RFC 9110, IETF Standards Track, June 2022, Sections 8.8, 9, and 13. Retrieved 2026-09-01. https://www.rfc-editor.org/rfc/rfc9110.html
- Nottingham, M. *HTTP Cache-Control Extensions for Stale Content*, RFC 5861, Informational, May 2010. Retrieved 2026-09-01. https://www.rfc-editor.org/rfc/rfc5861.html

## Exercises

### Exercise 1

Distinguish storage, freshness, validation, and invalidation using one response lifecycle.

### Exercise 2

A stored response has a 120-second lifetime, an upstream `Age` of 30 seconds, and has resided locally for 50 seconds. Under a simplified additive model, compute current age and freshness.

### Exercise 3

Design safe caching for `/catalog` varying by `Accept-Language` and `Accept-Encoding`, including directives, validators, keys, and revalidation.

### Exercise 4

Compare a 30-second TTL with explicit purge plus a 30-minute TTL for a price representation. State failure behavior and maximum stale risk.

### Exercise 5

Review a multi-tenant API that uses `Cache-Control: public, max-age=300`, keys only by path, and collapses concurrent misses. Propose the evidence needed before any shared caching is permitted.

## Answers to the Exercises

### Answer 1

The origin returns a response that policy permits a cache to store. While its calculated age is below its freshness lifetime, matching requests can reuse it without contacting the origin. Once stale, it can be validated with an entity tag; `304` refreshes metadata and permits reuse of stored content. A successful unsafe request can invalidate matching stored responses, making them unsuitable even if their former lifetime had not expired. None of these steps implies physical deletion from every system.

### Answer 2

Under the stated simplified model, current age is $30+50=80$ seconds. Since $80<120$, it remains fresh for 40 seconds. A production cache must use RFC 9111's full age calculation, including request/response timing and `Date`; the arithmetic here isolates only accumulated upstream and resident age.

### Answer 3

Emit an explicit public freshness policy only if the catalog is truly identical across users. Select language and coding, emit accurate `Content-Language` and `Content-Encoding`, and send `Vary: Accept-Language, Accept-Encoding`. Generate a validator for each selected representation. Key matching includes both fields. When stale, revalidate with `If-None-Match`; update metadata on `304`. Bound or forbid stale-on-error according to catalog risk.

### Answer 4

A 30-second TTL needs no purge channel and bounds ordinary staleness near 30 seconds, but increases origin traffic and cannot instantly remove dangerous content. Purge plus 30 minutes improves hit ratio and normally updates quickly, but a lost purge can leave old price data for the TTL remainder. Use acknowledged purge evidence and retain the finite TTL as a backstop; choose the bound from the business consequence of an old price.

### Answer 5

Path-only keys and miss collapse can mix tenants, so shared caching is unsafe until the response is proven tenant-independent or the cache has a trusted, non-forgeable tenant partition. Evidence must cover authenticated edge identity, stripping of client-supplied partition fields, complete variation, authorization-specific bodies, errors and redirects, purge scope, log secrecy, and adversarial cross-tenant tests. Otherwise use `private` or `no-store` and collapse only within a private trusted boundary.
