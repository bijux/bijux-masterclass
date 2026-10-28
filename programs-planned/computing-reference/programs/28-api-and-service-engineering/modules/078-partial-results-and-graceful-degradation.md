---
module_id: API-078
program: API & Service Engineering
level: 2
module_number: 78
title: Partial Results and Graceful Degradation
status: complete
last_verified: 2026-09-02
---

# Partial Results and Graceful Degradation

## One-Page Review

### Governing question

When dependencies, time, or capacity cannot produce the ideal response, what reduced result remains truthful and useful, how is incompleteness represented, and when must the API fail instead?

### Essential definitions

- A **partial result** contains a defined subset of requested components/items plus explicit completeness and error metadata.
- **graceful degradation** preserves the operation's core value using a cheaper, older, reduced, or alternate representation under known conditions.
- A **hard dependency** is required for correctness; a **soft dependency** may be omitted or substituted under the contract.
- **completeness** states which expected components/items were evaluated, returned, omitted, failed, or remain pending.
- **quality** describes accuracy, freshness, coverage, fidelity, or confidence relative to the ideal result.
- **provenance** identifies the source, version, generation time, and fallback mode of returned data.
- A **fallback** is an alternate path; it is not automatically safe, simpler, or available.
- A **degradation budget** bounds how much quality, freshness, coverage, duration, and traffic may be degraded.

### Central model, mechanism, or theorem

Let requested components be $R$, required components $H\subseteq R$, valid returned components $V\subseteq R$, and explicitly classified omitted/failed/pending components $O$. A truthful partial response preserves

$$
H\subseteq V,\qquad V\cap O=\varnothing,\qquad V\cup O=R
$$

for a closed-world request, with each $o\in O$ carrying a stable state/reason that is safe to disclose. If any hard component is absent or a returned component violates its validity/authorization/quality floor, the operation is not a successful degraded result.

### Critical invariants

The API defines ideal, minimum useful, and invalid results before failure. Required fields/effects are never silently omitted; optionality in a schema does not imply operational dispensability. Every returned component remains authorized, valid, and attributable. Missing, null, empty, unavailable, unauthorized, not found, stale, approximate, and pending are not conflated.

Response-level status and item/component errors are stable and machine-readable. Clients can determine completeness without parsing prose. Writes preserve atomicity or expose authoritative per-item outcomes; a degraded path never fabricates a committed effect. Fallbacks have independent capacity, deadlines, security, freshness, observability, and failure controls. Recovery exits degradation gradually and does not oscillate.

### Common failures

Return `200` with fields silently missing; use HTTP `206` for application-level partial data; treat `null` as every failure; make authorization failure look like dependency outage; expose existence via per-item errors; cache degraded responses as ideal; serve stale security/pricing data; retry the entire batch and duplicate successes; fallback calls the same failed dependency; fallback cache overloads; feature flags require an unavailable control plane; partial write claims transaction success; clients ignore warnings; schema adds completeness only after an incident; degradation becomes permanent; and dashboards count any `2xx` as full success.

### Compact example

A product page requires identity, price, and purchasability; recommendations and reviews are optional. Recommendations time out. The API returns the three required components, marks `recommendations` as omitted with a stable temporary-unavailable reason, reports `complete=false`, and keeps reviews if valid. It does not use `206`, because no byte range was requested. **Conclusion:** degradation is successful only because the minimum useful contract remains satisfied and the omission is explicit.

### Connections

[Bulk and Batch Operations](019-bulk-and-batch-operations.md) defines per-item outcomes. [API Caching and Invalidation](076-api-caching-and-invalidation.md) governs stale provenance, and [Fan-Out and Tail Latency](077-fan-out-and-tail-latency.md) defines completion/cancellation. The next module addresses consistency and read-after-write expectations.

## Governing Question

For each API operation, which data and effects are indispensable, which reductions are contractually acceptable, how will clients distinguish every missing or downgraded component, and what capacity/correctness boundary forces an explicit failure?

## Why This Matters

A local dependency failure need not erase all user value. A search service may omit optional personalization, a dashboard may show older metrics with age, and a batch read may return successful items plus per-item failures. AWS reliability guidance recommends identifying core functions and transforming applicable hard dependencies into soft ones. Google SRE recommends cheaper degraded results before load shedding when they remain useful.

But “something is better than nothing” is not a correctness rule. A checkout without current price, a permission decision without policy, or a financial transfer without one atomic update can be worse than an error. Degradation requires business semantics, not merely catching exceptions.

Partial results also change the API contract. Clients need to know whether a field is absent because it was unrequested, unauthorized, nonexistent, unavailable, timed out, stale, or pending. If an old client treats missing data as zero or success, a new fallback can cause damage. Completeness and capability negotiation belong in the normal schema.

GraphQL demonstrates one explicit model: a response can contain partial data and field errors with paths, subject to null-propagation rules. That model is not automatically appropriate for REST, RPC, or writes, but it illustrates that error locality and data coexistence must be specified. HTTP `206 Partial Content` instead means a range response for a selected representation; it is not a generic application partial-success code.

## Prerequisites and Retrieval

Retrieve [Status Codes and Error Meaning](003-status-codes-and-error-meaning.md), [Bulk and Batch Operations](019-bulk-and-batch-operations.md), [Error Translation](035-error-translation.md), [API Caching and Invalidation](076-api-caching-and-invalidation.md), and [Fan-Out and Tail Latency](077-fan-out-and-tail-latency.md).

Retrieve the operation's core business invariant; requested/required/optional schema fields; per-item atomicity; dependency and fallback graph; deadline/criticality; freshness/accuracy/completeness limits; authorization and non-disclosure rules; client versions and unknown-field/null behavior; cache keys/directives; retry/idempotency/outcome contracts; degradation flags/configuration; fallback capacity; telemetry; and recovery/runbook tests.

## Learning Objectives

After completing this module, you can:

1. define ideal, minimum useful, partial, degraded, pending, and invalid outcomes;
2. classify hard/soft dependencies from business and security invariants;
3. design machine-readable completeness, per-component state, quality, and provenance;
4. choose correct HTTP/RPC/GraphQL/batch response semantics without misusing status codes;
5. preserve atomic writes and authoritative per-item effects under partial failure;
6. make stale, approximate, default, alternate, and asynchronous fallbacks explicit;
7. bound fallback capacity and prevent recursive/common-mode failure;
8. evolve contracts safely for clients that do not understand partial results;
9. measure full, degraded, partial, and failed user outcomes separately; and
10. verify dependency combinations, overload, security, cache, client, and recovery behavior.

## Core Exposition

### Define minimum useful truth

Begin with the user's decision or effect. List fields/effects required for that decision to be correct, those that improve value, and those that are cosmetic. A required database foreign key can be technically available while a current authorization decision is missing; infrastructure availability is not the classification criterion.

Define three levels: **ideal** contains all requested quality; **minimum useful** satisfies every hard invariant and declared quality floor; **invalid** could mislead, violate security, or create an uncertain effect. Partial/degraded responses must remain at or above minimum useful.

Optional in JSON/OpenAPI/GraphQL type syntax may mean backward-compatible absence, not “safe to drop during outage.” Conversely, a normally present feature can be operationally soft if clients understand its omission. Record both schema optionality and degradation criticality.

For each operation publish a degradation matrix: trigger, affected components, allowed substitute, maximum age/error, public state/reason, retry guidance, metrics, and exit criterion. Review it with product, security, data, and operations owners.

### Separate partial, degraded, pending, and failed

A partial result omits or fails some independently meaningful requested components/items. A degraded result may be complete in shape but lower quality—stale cache, lower resolution, approximate rank, reduced search corpus. A pending result transfers responsibility to an asynchronous lifecycle. A failed result does not meet minimum useful semantics.

These categories can combine: a response may contain partial fields and mark returned recommendations approximate. Model them explicitly rather than one boolean alone. `complete=false` needs component-level explanation; component states without an overall minimum-useful verdict force every client to reimplement policy.

An empty list is a valid evaluated result, not the same as “search unavailable.” `null` can be a legitimate domain value, unknown value, redacted value, or field error depending on schema. Prefer tagged state or errors alongside data so clients do not guess.

Pending writes use `202 Accepted` only when durable responsibility and a status resource/lifecycle exist. It is not a euphemism for “we might do it.”

### Classify dependencies by semantic role

A dependency is hard when its absence prevents authorization, validation, invariant preservation, authoritative outcome, or minimum usefulness. It is soft when the operation can omit/substitute its contribution under a reviewed contract.

The same dependency can be hard for one operation and soft for another. Inventory is hard for purchase authorization but may be soft for browsing if the UI says availability unknown. Audit logging may be hard in a regulated write and soft-but-buffered for a public read.

Soft does not mean unbounded failure. State maximum degradation duration and quality. A week-old configuration default can be unsafe even if a ten-minute cached value is acceptable. Reclassify dynamically only through explicit policy/version, not arbitrary exception handling.

Map common-mode dependencies. A fallback that calls the same database through another service is not independent. A feature-flag service required to enable the fallback can block the incident path.

### Design a closed completeness envelope

For a finite requested component set, return which components succeeded and which are omitted/failed/pending, with no unexplained gap. Include stable component/item identifier or field path, state, machine code/type, retryability, and safe details. Returned items carry source version/time and quality when relevant.

An overall field can state `complete`, `degraded`, mode/policy version, evaluated/requested counts, and response generation time. Do not require clients to compare arbitrary arrays to infer completeness unless the request itself defines that protocol.

For paginated/search results, “10 items returned” does not prove all partitions were searched. Report coverage such as shards evaluated/expected, result exactness, continuation behavior, and whether totals are exact/lower-bound/unknown. Avoid exposing internal topology or unauthorized existence.

Make ordering deterministic. Per-component errors reference stable paths/IDs, not response array positions that change when items are omitted. Duplicate requested IDs have defined correlation IDs.

### Choose response status and representation

Use HTTP status for the outcome of the HTTP operation/resource semantics. A successful domain representation that explicitly includes optional unavailable components may be `200 OK` under its contract. If the minimum useful representation cannot be produced, return the appropriate `4xx`/`5xx` with stable problem details.

Do not use `206 Partial Content` for missing fields, failed downstream calls, or partial batch success. RFC 9110 defines it for satisfying range requests with parts of a selected representation and `Content-Range` semantics.

RFC 9457 problem details are suitable when the response represents an error condition. If the response remains a domain resource representation with embedded component states, the domain schema is often more appropriate. Do not put machine instructions only in human `detail`; use stable typed extensions.

For multi-status/batch designs, use the existing documented media type/status contract and per-item outcomes. Generic intermediaries understand only standard status semantics; custom success-with-errors must be explicit to SDKs, caches, monitoring, and clients.

### Learn from GraphQL without copying blindly

The GraphQL specification permits partial data with field errors and identifies error paths. Non-null field failures propagate null to a nullable parent, possibly eliminating broader data. Clients are expected to inspect both `data` and `errors`.

The transferable lessons are field locality, stable path, explicit coexistence of data/error, and schema-defined nullability. The exact HTTP status, null propagation, and response shape are GraphQL protocol semantics, not universal REST rules.

Resolvers must not leak unauthorized existence or internal dependency names through errors. Repeated field errors require bounded payload/cardinality. A top-level success transport response still needs operational metrics for field failure and user completeness.

GraphQL clients/caches may normalize partial objects. Define whether errors prevent cache writes, tag incomplete records, or update only valid fields; otherwise a transient partial response can overwrite a complete cached entity with nulls.

### Preserve write and batch truth

For an atomic command, either the whole invariant commits or it does not. Do not degrade by skipping a required side effect and returning success. If an optional notification fails after commit, the authoritative response can report committed core outcome plus notification state only if that lifecycle is part of the contract.

For non-atomic batch operations, return one authoritative outcome per item: succeeded with result/version, rejected permanently, failed transiently, pending with operation ID, or not attempted because a batch-level condition stopped processing. Include stable input correlation and idempotency identity.

Retry only retryable failed/not-attempted items under the same effect keys. Retrying the whole batch can duplicate successful effects. If the client cannot safely act on partial writes, offer an atomic mode or reject rather than surprise it.

Unknown outcome after timeout is not failure. Mark unknown/pending and reconcile; never invite a new effect ID. Compensation is a new governed effect, not erasure of history.

### Use stale data with explicit provenance

Stale data is a degraded result only if its age/content remains within domain limits. Include generation/effective time, source/version, age or `asOf`, and mode. Apply the stricter of cache policy and business/security validity.

Do not serve stale authorization, revocation, inventory reservation, price commitment, medical instruction, or compliance data unless a specific contract permits it. A stale product description and a stale balance have different harm.

If fresh and stale components come from different snapshots, the combined response may violate cross-field invariants. Report per-component versions and use a consistency fence/snapshot when the user decision requires one.

Cache degraded responses separately by mode/quality and avoid overwriting ideal entries. A partial cached object must not erase previously known fields or be reused as complete.

### Design approximate and reduced-work modes

Examples include fewer search shards, smaller top-$K$, cached rather than live aggregates, lower image resolution, omitted recommendations, less expensive ranking, sampled analytics, and reduced history range. Define maximum error/coverage and visibly identify approximation where decisions depend on it.

Keep the degraded algorithm simpler than the primary path. A complex fallback rarely exercised may fail during the incident. Prefer static/local data, bounded computation, and minimal dependencies. Version and test defaults.

Do not let lower quality violate fairness or security. Sampling can underrepresent a tenant; reduced fraud checks can be unacceptable; approximate totals can mislead billing. Some operations have no safe reduced mode.

Degradation should reduce limiting-resource cost measurably. Omitting a small response field after already doing the expensive query does not protect capacity.

### Bound fallback capacity and recursion

Fallbacks are dependencies. A cache, alternate provider, read replica, secondary region, durable queue, or default store has finite capacity and its own latency/security/consistency. Give it bulkheads, deadlines, circuits, admission, and observability.

When the primary fails, all traffic can shift at once. Verify fallback at full diverted load plus recovery. Prevent recursive chains A→B→A or fallback calling the same failing shared database. Limit depth and record mode.

Fallback errors do not justify cascading to progressively less trustworthy data without a floor. If all acceptable modes fail, return an explicit failure. Fail closed for authorization and invariant-critical effects.

Feature flags/configuration for degradation need safe locally available defaults, authorization, audit, expiry, and rollback. Avoid requiring an unavailable control plane to enter the only safe mode.

### Make client capability explicit

Old clients may assume absent field means empty, ignore an errors array, or cache `200` as complete. Introduce partial semantics only through a version/media type, explicit request preference/capability, or backward-compatible shape whose old behavior is proven safe.

Clients can request `requireComplete`, minimum coverage, maximum staleness, or acceptable modes within server policy. A client cannot demand unsafe work during overload; if requirements cannot be met, fail explicitly. Defaults must be documented.

SDKs should expose completeness/mode as first-class results, not discard warnings. Generate types that force handling required per-item outcomes where language supports it. Unknown future component states fail conservatively.

Contract tests include legacy clients, proxies, caches, mobile/offline versions, and analytics pipelines. A warning header alone is often lost; keep semantic state in the representation.

### Coordinate deadlines, cancellation, and retries

The aggregator classifies components before launch and assigns deadlines by hard/soft role. When a soft branch cannot fit remaining time, omit it with a reason rather than start orphan work. A hard branch failure that makes minimum usefulness impossible can cancel other branches.

Optional branch retries/hedges must not consume capacity needed for hard components. All attempts share parent deadline and retry budget. Under overload, degrade before speculative attempts when policy allows.

Per-component retry guidance includes whether a later fetch endpoint exists. Avoid telling clients to retry the entire aggregate when only one optional field failed. If partial content is stable/cached, offer a component resource or conditional refresh.

Cancellation does not roll back effects. Preserve outcome identity and report committed core work even if optional response enrichment is cancelled.

### Protect security and privacy

Completeness metadata can reveal that a hidden component/resource exists. For unauthorized callers, apply the same non-disclosure policy as the ideal response. Do not distinguish “secret item failed” from “secret item absent” if that distinction is prohibited.

Fallback sources apply current authentication, authorization, tenant isolation, residency, encryption, and audit. A public cache/default cannot satisfy a private field simply because the primary is unavailable.

Error details avoid stack traces, dependency hostnames, shard counts, policy internals, or other attack guidance. RFC 9457 emphasizes interface-level problems rather than debugging internals. Stable opaque occurrence IDs support operators.

Attackers may intentionally fail optional branches, inflate requested fields/items, or trigger expensive fallback. Apply query complexity, item/fan-out, tenant, and degradation budgets before work.

### Prevent degraded mode from becoming normal

Define entry and exit signals with hysteresis: dependency circuit, load threshold, error/latency rate, operator override, and policy version. Record who/what activated it and an expiry for manual controls.

Recovery ramps expensive/optional components gradually while watching queues, tail latency, error, cache/fallback pressure, and user completeness. If every instance restores all enrichments at once, the recovered dependency can relapse.

Set maximum time or error-budget allowance for degraded operation. Sustained partial success is an incident even if core availability stays high. Product SLOs include full-quality and minimum-useful results separately.

Regularly exercise degradation on a small controlled cohort, as Google SRE guidance suggests for overload paths. Stale defaults, broken flags, and untested client rendering otherwise surface only during failure.

### Observe user value and data quality

Measure ideal, degraded-complete, partial-minimum-useful, pending, and failed outcomes; requested/returned/omitted/failed components; reason; mode/policy version; hard/soft dependency health; freshness/age; coverage; approximation quality; fallback load; retries; and recovery transitions.

Do not count every `2xx` as full availability. Maintain separate SLIs for minimum useful success, full-quality success, completeness, staleness/accuracy, and write outcome certainty. Weight by user/workflow importance where defined.

Trace component path and criticality without leaking sensitive data or exploding cardinality. Correlate omissions with dependency, zone, client version, tenant cohort, overload, cache, and configuration.

Alert on hard component omission, unknown/unclassified state, degraded mode beyond budget, fallback saturation, legacy-client harm, cache of partial as complete, and repeated recovery oscillation.

### Verify the degradation lattice

Enumerate dependency combinations, not only one-at-a-time failure. Test primary down plus cache stale, fallback slow, flag service down, telemetry down, authorization unavailable, and recovery. Use pairwise/risk-based expansion for large graphs and always include common-mode failures.

For each mode assert hard components, completeness closure, quality/freshness floor, safe errors, status semantics, cache behavior, retry/idempotency, and client rendering. Test null/empty/absent/unauthorized/not-found distinctions and error payload bounds.

Load test primary loss with all traffic on fallback, optional feature removal under overload, and gradual restore. Prove degradation reduces the actual limiting resource and does not shift collapse to cache/alternate region.

Test writes at every commit boundary, batch mixtures, timeout-after-commit, duplicate retry, compensation, and client crash. Check that no response claims more effect/completeness than authoritative evidence supports.

## Definitions and Notation

Let $R$ be requested components, $H\subseteq R$ hard components, $V$ valid returned components, and $O$ classified omitted/failed/pending components. Let coverage $c=|V|/|R|$ for $|R|>0$, noting that unweighted coverage does not express criticality or cost.

Let quality vector $q=(f,a,cov,e)$ represent freshness, accuracy, coverage, and error/confidence dimensions with policy floor $q_{\min}$ under a defined partial order. Let degradation duration be $T_d$ with maximum allowed $T_{\max}$. Let fallback capacity be $B_f$ and shifted offered load $L_f$.

A **closed-world** response knows the expected requested set; an open-ended search needs coverage/bounds rather than enumerating every absent item. A **mode** is a named versioned policy. A **quality floor** is the minimum safe/useful result, not an aspirational SLO.

## Mechanisms, Invariants, or Proof Structure

**Completeness-closure argument.** For finite $R$, if $V\cap O=\varnothing$ and $V\cup O=R$, every requested component has exactly one declared disposition. This does not prove returned correctness; authorization, validity, and quality invariants are additional.

**Minimum-useful argument.** If $H\subseteq V$ and every returned component meets its validity/quality floor, omission of only contractually soft components preserves the declared minimum result. If any hard component is absent, calling the result successful contradicts the contract.

**Fallback-capacity counterexample.** A primary handles load $L$ while fallback capacity is $0.4L$. On total primary loss, shifting all $L$ exceeds fallback by $0.6L$. Existence of a fallback does not prove graceful degradation; admission, reduced work, or provisioning must keep $L_f\le B_f$.

**Atomic-write argument.** If an operation invariant spans effects A and B, returning success after A commits and B is silently omitted produces a state excluded by the invariant. Partial success is valid only if the operation was explicitly non-atomic with authoritative per-effect/item outcomes or compensation/pending lifecycle.

Operational invariants are: minimum truth preserved; every omission classified; no unauthorized disclosure; quality/provenance explicit; status semantics accurate; writes authoritative; fallbacks bounded and independent enough; clients capable; degradation time-bounded; and full versus degraded outcomes observable.

## Alternatives and Trade-Offs

Fail-fast gives simple semantics and avoids misleading data but discards available value. Partial responses preserve value while increasing schema/client/testing complexity. Separate component endpoints simplify per-resource outcomes but add client round trips and coordination.

Stale cache is fast and failure-isolating but risks outdated state. Alternate providers/regions add independence but cost, consistency, residency, and common-mode concerns. Static defaults are simple but age; computed approximations can share the failed resource.

Embedded component errors make one aggregate self-describing. Out-of-band headers are easier to add but often lost by SDKs/caches. Top-level problem details are standard for failed HTTP operations but do not replace domain partial-result schemas.

Strict required fields protect correctness but lower availability. Softening a dependency improves continuity only when product/security semantics genuinely allow it. Version/capability negotiation protects legacy clients at rollout cost.

Automatic degradation reacts quickly but can oscillate or hide incidents. Operator controls offer judgment but add latency and control-plane dependence. Combine bounded automatic safe modes with audited overrides.

## Failure Modes and Misconceptions

- “Any data is better than an error.” Misleading or unauthorized data can be worse.
- “Optional schema field is a soft dependency.” Schema evolution and business criticality differ.
- “`206` means partial success.” In HTTP it is range response semantics.
- “`200` means every component succeeded.” Only the documented domain representation can say that.
- “Null explains failure.” It can also mean valid null, unknown, redacted, or absent.
- “Problem details describe each successful component.” They primarily represent error responses; domain schemas may fit mixed results.
- “Fallback equals availability.” It may share dependencies or lack shifted-load capacity.
- “Stale means safe.” Domain/security maximum age decides.
- “A default is harmless.” Defaults can be obsolete, insecure, or inconsistent.
- “Retry the batch.” Successful effects may duplicate; retry failed identities only.
- “Cancellation undoes optional work.” Remote effects may already commit.
- “GraphQL always returns usable partial data.” Nullability propagation can remove broader data, and clients must inspect errors.
- “Hide component errors for security.” Hide sensitive facts, but still give a non-leaking classified disposition.
- “Degraded `2xx` satisfies the SLO.” Full-quality and minimum-useful outcomes need separate objectives.
- “Recovery means turn everything on.” Gradual restore prevents relapse.
- “The fallback is simpler because it is secondary.” Simplicity must be designed and tested.

## Worked Examples

### Example 1

A page requests identity, price, purchasability, reviews, and recommendations. The first three are hard. Recommendations time out; the response returns the other four, classifies recommendations as temporarily unavailable, and sets `complete=false`, `mode=core`. Since $H\subseteq V$, it meets minimum usefulness.

### Example 2

A dashboard returns `balance: null` when the ledger times out. The client renders zero. The corrected schema omits the value and returns component state `unavailable`, while a legitimate zero remains numeric zero and a legitimate unknown uses its domain state. No client guesses from `null`.

### Example 3

A server returns HTTP `206` because two of ten upstream services failed. A proxy treats it as byte-range content and expects `Content-Range`. The API changes to its documented `200` degraded representation with component errors—or a `5xx` problem when hard data is absent.

### Example 4

A batch creates 100 items; 92 commit, 5 fail validation, 2 are transiently rejected, and 1 is not attempted after deadline. The response records all 100 correlation IDs and dispositions. The client retries only the two transient and one not-attempted entries using the same idempotency keys.

### Example 5

A search normally covers 50 shards; 45 respond. Returning 100 hits without coverage looks complete. The corrected result reports `45/50` shard coverage, whether total is a lower bound, omitted scope, and continuation/retry policy without exposing forbidden shard details.

### Example 6

A cached profile is 12 minutes old. Policy allows 15-minute stale display but requires live authorization. The service reauthorizes, marks `asOf`, and returns the profile. If authorization is unavailable, it fails closed; cached profile data does not grant access.

### Example 7

Primary recommendation capacity handles 10,000/s; fallback capacity handles 4,000/s. Total failover would overload fallback by 6,000/s. Admission limits fallback to eligible high-value traffic and omits recommendations for the rest, preserving core page goodput.

### Example 8

A purchase commits inventory and charge atomically, but email notification fails. Purchase success remains authoritative; notification is recorded pending in an outbox and reported only if the API exposes that lifecycle. The API does not roll back or label the purchase partial merely because an optional notification is delayed.

### Example 9

An old mobile client treats a missing `offers` array as “no offers” and makes a purchase decision. The new partial mode is offered only to clients declaring a media-type capability; legacy clients receive a clear failure when offers are unavailable until upgraded.

### Example 10

After a dependency recovers, 200 instances simultaneously re-enable expensive enrichment and overload it again. The platform ramps cohorts from 5% to 25% to 100% while monitoring queue, tail, error, and completeness; it rolls back on regression. Exit is a capacity event, not a flag flip.

## Cross-Program Connections

[Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies partial failure, consistency, atomicity, sagas, idempotency, and uncertainty models.

[Security Engineering](../../25-security-engineering/ROADMAP.md) governs fail-closed decisions, non-disclosure, fallback authorization, tenant isolation, and safe errors.

[Data Engineering](../../19-data-engineering/ROADMAP.md) connects completeness, provenance, freshness, coverage, quality dimensions, and reconciliation.

[Platform Engineering](../../29-platform-engineering/ROADMAP.md) owns degradation policy rollout, safe defaults, capability/config distribution, fallback capacity, telemetry, and recovery cohorts.

[Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md) contributes hard/soft dependency design, bounded contexts, interface evolution, and fallback simplicity.

[Systems Engineering](../../26-systems-engineering/ROADMAP.md) frames graceful degradation, resource trade-offs, feedback, common-mode failure, and recovery testing.

## References

1. GraphQL Foundation, [GraphQL Specification: Response](https://spec.graphql.org/October2021/#sec-Response).
2. Amazon Web Services, [Implement graceful degradation to transform applicable hard dependencies into soft dependencies](https://docs.aws.amazon.com/wellarchitected/latest/framework/rel_mitigate_interaction_failure_graceful_degradation.html).
3. Google, *Site Reliability Engineering*, [Addressing Cascading Failures](https://sre.google/sre-book/addressing-cascading-failures/).
4. Google, *Site Reliability Engineering*, [Production Services Best Practices](https://sre.google/sre-book/service-best-practices/).
5. IETF, [RFC 9457: Problem Details for HTTP APIs](https://www.rfc-editor.org/rfc/rfc9457.html).
6. IETF, [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html).

## Exercises

### Exercise 1

Design minimum-useful and degraded contracts for a travel itinerary API containing bookings, live disruption, weather, maps, recommendations, and loyalty data. Classify dependencies and quality floors.

### Exercise 2

Design a closed completeness envelope for a 200-item bulk read with authorization-sensitive existence, per-item versions, replica staleness, timeouts, duplicates, and pagination.

### Exercise 3

A primary feature handles 30,000 requests/s; fallback handles 9,000/s and costs twice as much. Design admission/degradation/recovery, calculate the minimum shed/omit volume under total primary loss, and state missing evidence.

### Exercise 4

Evolve an existing API whose clients assume every `200` is complete. Propose capability/versioning, schema, SDK, caching, telemetry, rollout, and rollback that safely introduces partial results.

### Exercise 5

Create a fault matrix and invariants for an atomic write with optional notification plus a non-atomic batch write. Include timeout-after-commit, retry, outbox, compensation, partial outcomes, fallback, and client crash.

## Answers to the Exercises

### Answer 1

Confirmed bookings and authorization/ownership are hard; current disruption may be hard when the itinerary claims travel readiness and otherwise can be explicitly unavailable with last-known timestamp. Weather, maps, recommendations, and loyalty enrichment are usually soft, but map/offline navigation or loyalty payment can change that operation. Define `ideal`, `core`, and perhaps `offline` modes; per-component state, source/asOf, accuracy/coverage, retry, and maximum age. Never infer “on time” from missing disruption data. Stale weather/map limits follow user harm; fallback capacity/security/residency are independent. If bookings cannot be verified, fail rather than return a misleading itinerary.

### Answer 2

Assign each request occurrence a correlation ID even for duplicate resource IDs. Return one disposition per occurrence or a deduplicated result plus explicit mapping. Authorized found items include value/version/asOf/consistency; authorized absent items use a stable non-leaking state; unauthorized and nonexistent follow the same public policy if enumeration is prohibited. Timeouts and stale-beyond-floor are transient states, not empty values. Include requested/evaluated/returned counts, page/continuation semantics, complete flag, mode/policy version, and per-item retryability. Do not reveal hidden IDs through counts/errors. A page is complete relative to its declared request scope, not the whole collection.

### Answer 3

At total primary loss, only 9,000 of 30,000 requests/s fit fallback, so at least 21,000/s must omit the feature, use another safe cheap mode, or be shed; sending all exceeds capacity by 21,000/s. Because fallback costs twice as much, financial and upstream resource budgets may require less than 9,000/s. Reserve it for authenticated high-value/within-entitlement traffic with fairness; omit from core responses otherwise. Ramp recovery in cohorts while monitoring fallback and primary. Missing evidence includes tail capacity under real mix, common dependencies, cold state, per-request cost, origin/fallback SLO, fairness, regional/residency constraints, and recovery behavior.

### Answer 4

Introduce a new media type/version or explicit `acceptPartial` capability; legacy clients continue receiving complete responses or clear failures. The new schema carries overall complete/mode/policy plus closed component dispositions, quality/provenance, and stable errors. SDKs expose a result type that requires completeness handling. Cache keys include capability/mode, partial entries cannot overwrite complete records, and staleness is bounded. Run contract tests for old clients/proxies, shadow responses, then opt-in cohorts. Metrics separate full/partial/fail and legacy harm. Roll back by disabling new-mode admission locally without depending on a remote control plane; never reinterpret an already cached old response.

### Answer 5

For atomic core effects, success only follows authoritative commit of the invariant. Timeout after commit uses the same idempotency key/outcome lookup; no duplicate effect. Optional notification is written to a transactional outbox with commit and may be pending/failed under its declared lifecycle; it never changes core purchase truth. For non-atomic batch, every item has stable identity and succeeded/rejected/transient/pending/not-attempted/unknown outcome; retries target only eligible items with same keys. Compensation is a new recorded effect and can fail. Test crash before/after commit/outbox publish/ack, client crash before response, duplicate delivery, notification fallback, partial batch mixes, and reconciliation. Invariants are no false success, no missing item disposition, stable identity, no silent atomicity weakening, and recoverable authoritative outcome.
