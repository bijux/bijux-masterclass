---
module_id: API-079
program: API & Service Engineering
level: 2
module_number: 79
title: Consistency and Read-After-Write Expectations
status: complete
last_verified: 2026-09-02
---

# Consistency and Read-After-Write Expectations

## One-Page Review

### Governing question

After an API acknowledges a write, which later reads must observe it, for whom, from which resources and regions, within what time, and how is that guarantee carried across replicas, caches, indexes, devices, and failover?

### Essential definitions

- **read-after-write** or **read-your-writes** means a qualifying later read observes at least the caller's acknowledged write.
- **monotonic reads** means a session never observes a version older than one it already observed.
- **session consistency** provides guarantees within a defined session, often using an opaque token/high-water mark.
- **linearizability** makes each single-object operation appear atomic in real-time order; **external consistency** additionally orders transactions consistently with observed commit order.
- **serializability** orders transactions as some serial execution but does not alone require real-time order.
- **eventual consistency** promises convergence after writes stop under its assumptions, without an inherent maximum delay.
- **bounded staleness** limits lag by time or versions under a defined scope.
- A **consistency token** carries the minimum version/position a later read must meet; it is not authentication.

### Central model, mechanism, or theorem

Let an acknowledged write produce version/commit position $v_w$, a session high-water mark be $h$, and a candidate read return version $v_r$. Read-your-writes and monotonic-read admission requires

$$
v_r\ge \max(v_w,h)
$$

under the resource's defined version order. If a selected replica/cache/index cannot meet the floor, the API waits within the original deadline, routes to an authoritative source, returns pending/stale-not-acceptable, or fails explicitly—it must not silently return an older value as success.

### Critical invariants

The contract defines what write acknowledgement proves: accepted, durably committed, replicated to which scope, and visible through which read surfaces. Every guarantee names resource/partition, subject/session, region, time/version bound, and behavior during failover. Read-your-writes is not “latest globally,” and database isolation is not inferred from an API label.

Tokens are opaque, integrity-protected or server-maintained, bounded in size, scoped to tenant/resource/epoch, and combined by maximum/causal rules—not trusted as authorization. Caches, search indexes, projections, list endpoints, and replicas either honor the floor or disclose that they cannot. Timeouts preserve uncertain write outcomes and stable operation identity.

### Common failures

Return `201` before durable responsibility; immediate GET hits a lagging replica; detail reads are strong but list/search lag silently; CDN caches pre-write content; session affinity breaks on autoscaling; token lives only in one browser tab; client chooses an arbitrary timestamp; versions compare across unrelated shards; failover resets counters; strong database read follows an asynchronously projected write; optimistic UI is mistaken for server truth; a retry uses a new idempotency key; monotonic reads regress across regions; “eventual” is marketed as “within seconds”; and dashboards measure average lag instead of violation tails.

### Compact example

A create returns resource version 42 and `Location: /orders/7`. An immediate GET is routed to a replica at version 40. With a required floor of 42, the gateway waits up to the read's remaining budget, then routes to the leader; it never returns version 40 as current. A collection index may still omit the order and must either accept the same token/consistency mode or state that its visibility contract is weaker. **Conclusion:** read-after-write applies per read surface, not automatically to every derived view.

### Connections

[Conditional Requests](006-conditional-requests.md) prevents lost updates but does not choose replica freshness. [API Caching and Invalidation](076-api-caching-and-invalidation.md) governs cached versions, and [Partial Results and Graceful Degradation](078-partial-results-and-graceful-degradation.md) governs explicit stale/pending results. The next module controls failure amplification.

## Governing Question

What observation did the API promise when it acknowledged a mutation, how does a caller prove its minimum required version to each later read surface, and what precise outcome occurs when topology or deadline cannot satisfy that promise?

## Why This Matters

Users reasonably expect a successful update to remain visible. A profile saved and immediately reverted by a replica read looks like data loss; an order created but absent from search invites duplicate creation; a permission revoked but served from cache is a security defect. These experiences occur even when every component works as configured.

Distributed databases expose different guarantees. DynamoDB documents eventually consistent and optional strongly consistent reads for particular surfaces, while some indexes remain eventual. Azure Cosmos DB defines strong, bounded staleness, session, consistent-prefix, and eventual levels, with session guarantees depending on a client session/token. Spanner documents strong reads and external consistency for its transaction model. An API may use any of these, but must translate their exact scope into a durable client contract rather than repeat a product adjective.

The write path and read path often differ. A command commits to a database, while GET reads a cache, collection queries use an index, analytics use a materialized view, and cross-region traffic uses a replica. Strong source storage does not make asynchronous projections strongly visible.

Consistency has latency, availability, throughput, and topology costs. Waiting for replication can exceed deadlines; leader routing can cross regions; failover can lose or reorder weakly replicated state. The design task is to choose the minimum guarantee each workflow needs, expose it explicitly, and fail truthfully when it cannot be met.

## Prerequisites and Retrieval

Retrieve [Conditional Requests](006-conditional-requests.md), [Long-Running Operations](018-long-running-operations.md), [Idempotency Keys](037-idempotency-keys.md), [Timeout and Deadline Budgets](071-timeout-and-deadline-budgets.md), [API Caching and Invalidation](076-api-caching-and-invalidation.md), [Fan-Out and Tail Latency](077-fan-out-and-tail-latency.md), and [Partial Results and Graceful Degradation](078-partial-results-and-graceful-degradation.md).

Retrieve every mutation acknowledgement point; transaction/commit/replication semantics; leader/replica routing; cache and invalidation; change-data-capture/outbox; search/list/materialized projections; version/ETag/commit positions; session/affinity/token propagation; client/device/auth lifecycle; multi-region and failover modes; read consistency options per SDK/API; idempotency/outcome lookup; deadline behavior; and metrics for replication/projection lag and consistency violations.

## Learning Objectives

After completing this module, you can:

1. distinguish read-your-writes, monotonic reads, bounded staleness, linearizability, serializability, and external consistency;
2. define write acknowledgement and visibility separately for resource, collection, search, cache, and projection surfaces;
3. design version/session tokens that carry a minimum observation without becoming authorization;
4. route, wait, escalate, or fail when a read surface is below the required version;
5. preserve guarantees across retries, devices, regions, reconnects, autoscaling, and failover;
6. combine cache/index lag with source consistency instead of assuming inheritance;
7. design snapshot-consistent pagination and multi-resource reads where required;
8. expose stale, pending, conflict, and unknown outcomes truthfully;
9. observe consistency latency, violation rate, token propagation, and escalation cost; and
10. verify concurrent, cross-surface, cross-region, partition, restore, and recovery histories.

## Core Exposition

### Name the guarantee precisely

“Strong consistency” is too broad without scope. Ask: latest with respect to which completed operations, on one object or a transaction, at one replica set or all regions, for one session or all clients, and through which API surfaces?

Read-your-writes guarantees a client/session does not miss its own acknowledged write on qualifying reads. It does not prevent another concurrent writer from producing a later version. Monotonic reads prevent regression below anything already observed. Writes-follow-reads and monotonic writes constrain causal/session ordering of later writes.

Linearizability concerns real-time ordering of operations on an object. Serializability concerns transaction equivalence to some serial order. Strict serializability/external consistency adds real-time transaction order. Snapshot reads can be internally consistent at an older timestamp without being current.

Eventual consistency has no intrinsic “two seconds” bound. If the product promises 99.99% within two seconds, that is a measured bounded-visibility SLO, not the definition of eventual consistency. During continuous writes, convergence language also needs care.

### Define what write success means

For each mutation response, document whether the command was merely accepted, durably logged, committed at the source of truth, replicated locally, replicated across regions, projected into read models, and visible from subsequent reads. These milestones differ.

`202 Accepted` transfers work to an asynchronous lifecycle only after durable responsibility is established. `200`/`201` for a synchronous write should represent the documented committed effect. Return resource identifier/`Location`, authoritative version/ETag, operation ID/idempotency key, and often the committed representation to avoid a needless immediate read.

A database commit followed by outbox publication means the resource may be visible before search/list projections. State that explicitly or wait for a visibility barrier if the workflow requires all surfaces. Do not hold an interactive request indefinitely for every analytics projection.

If the response is lost after commit, the client has an unknown observation, not a failed effect. It retries with the same idempotency identity or queries outcome; a new key can create a duplicate.

### Model every read surface

Create a visibility matrix: resource GET, collection/list, filtered query, search, count/aggregate, cache/CDN, graph relation, audit/event stream, export, and secondary region. For each, record source, version model, consistency, lag bound/SLO, token support, escalation, and error.

A resource GET can route to a leader while list uses an eventual global secondary index. A count can lag behind the items. A cache can serve a pre-write value after the database is current. A search document can update fields from different events.

The API contract must not imply that `GET /items/{id}` and `GET /items?owner=x` share visibility merely because both are GET. Offer separate consistency parameters/tokens or document the lag. Workflows that create then list need a defined solution.

Derived views should carry source version/checkpoint. Without comparability, the aggregator cannot tell whether a projection satisfies the caller's floor.

### Return authoritative write evidence

Use a monotonic version, ETag, commit timestamp, log position, or opaque consistency token created by the authority. Its comparison semantics can be server-only. A wall-clock timestamp supplied by a client is not a safe version: clocks skew and concurrent writes share resolution.

RFC 9110 notes an ETag in a `201 Created` response can validate later conditional requests. ETags also support `If-Match` lost-update prevention. Cache validation and write preconditions are related to version evidence but distinct from choosing a sufficiently current replica.

Return the committed representation when economical and authoritative. This gives immediate feedback without an extra read, but future reads still need a guarantee. If server transformations occur, return their resulting version rather than echoing client input.

Opaque tokens allow internal topology/version evolution. Document lifetime, propagation, maximum size, and failure behavior without exposing shard positions that become attack or coupling surfaces.

### Carry a session high-water mark

After write version $v_w$ or read version $v_r$, update session high-water $h=\max(h,v_w,v_r)$ within the version scope. Later reads present $h$; the server returns only a value at least $h$, waits/routes, or fails explicitly.

For multiple partitions, a token may be a vector/checkpoint map rather than one scalar. Bound its growth via server-side session state, signed compact summaries, epoch checkpoints, or workflow-scoped tokens. Never compare unrelated partition counters numerically.

Session scope can be one SDK instance, authenticated web session, workflow, user account, device, or explicit token chain. Cross-device read-your-writes requires shared server state or transferring a token; a browser-memory token cannot help a phone.

Merge tokens by a defined join/max operation. Do not let an untrusted caller forge an arbitrarily high token that forces leader waits/denial of service. Integrity-protect, validate scope/epoch, cap age/size, and rate-limit escalation.

### Enforce the floor on reads

At read time, resolve the minimum required version from explicit request, server session, and workflow. Select a source known to satisfy it. If a replica is behind, wait for catch-up only within the original deadline and a bounded waiter budget; otherwise route to leader/strong source if permitted.

If no eligible source can satisfy the floor, return a stable pending/consistency-unavailable response with safe retry guidance, or a degraded older result only when the caller explicitly permits and provenance is clear. Never silently discard the token and return stale success.

Read escalation itself consumes scarce leader/cross-region capacity. Protect with bulkheads, quotas, tenant fairness, load shedding, and observability. A malicious or buggy client must not force every read strong.

The response includes observed version/as-of and whether requested consistency was met. Do not reveal internal replicas/regions where sensitive.

### Distinguish session from global currentness

Session consistency can guarantee read-your-writes and monotonic reads for token-carrying operations while other clients see older values. It is often a good usability/performance compromise. It is not linearizability for all clients.

Azure Cosmos DB documentation, for example, scopes session guarantees and notes token sharing assumptions. Treat those as provider-specific mechanics. If requests use different SDK instances without sharing session state, the application guarantee can disappear.

A sticky session routes to a likely-current replica but is not a proof: failover, restart, rebalancing, cache, or separate projection can break it. Pair affinity with version evidence and fallback.

If global latest is required—authorization revocation, unique allocation, inventory commitment—use an authoritative strongly consistent/linearizable operation under the actual store contract, not session affinity.

### Compose caches with consistency floors

Store version and generation metadata with every cache entry. A read requiring floor $h$ can use the entry only if its version satisfies $h$ and domain freshness/security rules. Otherwise revalidate/load an eligible source.

Write-through/invalidation cannot alone guarantee immediate read-your-writes because delayed fills, other cache tiers, CDN variants, and lost events exist. Apply version-monotonic installation from API-076 and bypass/invalidate the writer's session safely.

Do not globally disable caching for all token reads if a current entry can satisfy the floor. Conversely, `Cache-Control: no-cache` validation does not necessarily mean a derived application projection caught up.

Cache keys include consistency mode/session-sensitive dimensions only when safe; otherwise use reuse predicates. Do not expose or fragment by raw token unnecessarily. A degraded stale response cannot advance session high-water beyond its actual version.

### Compose indexes and projections

Asynchronous indexes/materialized views consume changes at a checkpoint. To satisfy read-your-writes, accept a write checkpoint token and wait until the projection watermark reaches it, bounded by deadline; or route to a source query/overlay the writer's committed item.

Overlay techniques merge recent session writes/deletes with a lagging list/search result. They need complete predicates, ordering, pagination, authorization, and tombstone handling. A newly created item may belong in page one and shift boundaries; naive append creates duplicates or wrong order.

If exact overlay is too complex, expose projection consistency honestly: return pending visibility/status, offer resource GET, or provide an asynchronous “visible in search” milestone. Do not claim the write failed because indexing lags.

Track projection lag by version/time and oldest unprocessed event, including partitions. Average lag can hide one stuck shard holding a user's write.

### Design list and pagination consistency

Offset pagination over a changing/lagging collection can duplicate or skip items. Cursor pagination should carry stable ordering keys and, where needed, a snapshot/version fence. Every page in a snapshot session reads at the same logical time or clearly documents live semantics.

Read-your-writes for a collection can mean “my new item appears,” “my update appears in its correct sort position,” and “my delete is absent.” These are separate overlay/invalidation obligations. Total counts/facets may still lag.

Snapshot consistency across many resources requires a datastore snapshot/read-only transaction or versioned view. Reading each object strongly at different times is not one consistent snapshot.

Bound cursor/token lifetime and integrity-protect it. If the snapshot is unavailable/expired after failover, return a stable restart-required outcome rather than silently switch timelines.

### Preserve monotonic reads through topology change

Load balancing across replicas can return version 10, then version 8. Session high-water rejects the regression. During regional failover, the new region may not contain acknowledged weakly replicated writes; the API must choose between blocking/failing, returning explicit lost/pending status, or violating the guarantee.

Define replication durability separately from read consistency. A session token cannot make missing data exist. Multi-region weak replication may have nonzero RPO during regional loss; a successful local write might not survive failover under that contract.

Epochs prevent comparing versions across restore, reshard, or leader history. On epoch mismatch, use an authority/reconciliation protocol; never reset high-water silently. Backups can restore older state even when replica reads were monotonic before disaster.

Failback is also hazardous. Route only after the returning region reaches required checkpoint and caches/projections are warmed/validated. Ramp traffic while checking violation rate.

### Handle concurrent writers and causality

Read-your-writes says a later session read observes at least its write, but another concurrent write may legally supersede it. Return version and actor/update metadata so a user distinguishes overwrite from regression.

Use `If-Match`/version preconditions for lost-update prevention. A client reads version 5, edits, and writes only if current remains 5; otherwise it receives conflict and merges/retries as a new decision. Read-your-writes alone does not prevent lost updates.

Causal workflows pass a dependency token: write B that depends on read/write A should not become visible in a view that omits A. Achieving this across services requires outbox/event causation, version vectors, or an owned workflow—not merely timestamps in headers.

Multi-master conflict resolution (last-write-wins, CRDT, merge, application reconciliation) defines what “at least my write” means after conflicts. Do not promise it without modeling convergence and user-visible supersession.

### Treat optimistic UI as a separate layer

A client can display its submitted value immediately for responsiveness. Mark it pending and reconcile with the authoritative response/version. Optimistic state is not server read-your-writes and must not be reused for security or irreversible decisions.

If the server rejects/transforms the write, roll back or show conflict. Offline queues preserve command identity/order and display pending age; reconnect uses the same idempotency keys and consistency tokens.

A locally merged response should distinguish confirmed from pending fields. Analytics and caches must not count optimistic state as committed.

Testing includes refresh/new device/another session, where local illusion disappears. The server contract must remain correct.

### Coordinate deadlines and availability

Waiting for a replica or projection consumes the read deadline. Let remaining budget be $B$, estimated catch-up wait $W_c$, execution $W_e$, and response reserve $R$. Wait only if $W_c+W_e+R<B$ under a conservative estimate and waiter capacity exists.

Stronger reads can be slower/costlier or less available during partitions. Expose consistency choices only when the client can act on them and server policy can refuse unsafe escalation. Default by operation/workflow, not one global setting.

During overload, do not weaken a required consistency guarantee silently. Shed/fail, or return an explicitly permitted stale/degraded response. Strong-read retries can amplify leader pressure; use budgets/backoff/pushback.

Availability SLOs distinguish full-consistency success, permitted stale success, pending, and failure. A fast stale `200` does not satisfy a read-your-writes SLO.

### Observe consistency as a user outcome

Record write acknowledgement milestone/version/region/epoch; read required floor and observed version; source class; wait/escalation; cache/index checkpoint; lag time/versions; consistency mode; deadline; pending/failure reason; and token validation/merge errors.

Measure read-your-writes and monotonic violation rate directly with safe probes/history analysis, not only replication lag. Report distributions/tails of time-to-visible for resource, list, search, and cache surfaces. Segment by region, partition, client/SDK version, cache, projection, and failover.

Avoid raw sensitive IDs/tokens in logs. Hash bounded correlation keys and sample while retaining violations. Alert on any hard guarantee violation, stuck projection partition, escalation saturation, token rejection spikes, and failover epoch mismatch.

Track the cost: strong/leader read rate, waiters, cross-region calls, cache bypass, retries, and latency. A guarantee that routinely misses deadlines needs architectural change, not a larger timeout.

### Verify histories and boundaries

Construct histories: write acknowledged at $v$, then reads through every surface/session/device/region must meet their declared floor. Include concurrent writer supersession to distinguish legal newer data from illegal regression.

Inject replica/index/cache lag, lost/reordered invalidation/events, leader change, connection/session loss, autoscaling, token omission/forgery, clock skew, partition, regional failover/failback, backup restore, reshard/epoch, and continuous writes. Test deadlines around catch-up.

For pagination, mutate between pages and verify snapshot/live contract. For multi-resource reads, verify one snapshot where promised. For conditional writes, race two clients and confirm conflict rather than lost update.

Check invariants: no qualifying read version below floor; high-water never decreases within scope; tokens cannot raise authorization; mismatched scopes/epochs fail safely; caches/projections prove version before use; retries preserve effect ID; and failure/recovery never silently weakens the declared mode.

## Definitions and Notation

Let $v_w$ be acknowledged write version, $v_r$ observed read version, $h$ session high-water, $e$ version epoch, and $c_p$ projection/cache checkpoint. Let time-to-visible on surface $s$ be $L_s=t_{visible,s}-t_{ack}$, with an optional promised bound $T_s$.

Let remaining deadline budget be $B$, catch-up wait $W_c$, execution $W_e$, and response reserve $R$. Waiting is feasible only when $W_c+W_e+R<B$ and resource admission permits it. Let recovery point objective be RPO; it is a durability-loss bound, distinct from ordinary read staleness.

A **history** is ordered invocations/responses used to evaluate consistency. A **visibility barrier** is a version/checkpoint that a read surface must reach. An **epoch** identifies a version namespace/history. An **overlay** merges recent authoritative changes into a lagging projection.

## Mechanisms, Invariants, or Proof Structure

**Session-floor argument.** If high-water begins at a valid observed version, updates by maximum, and each qualifying read admits only $v_r\ge h$, observed versions cannot decrease. This assumes comparable versions in one scope/epoch and complete token propagation.

**Cross-surface counterexample.** Source commit $v=42$ and strong resource GET do not imply a search index at checkpoint 40 contains the write. Therefore source storage consistency cannot prove derived-view read-after-write; the projection must honor a barrier, overlay, or expose weaker visibility.

**Deadline feasibility.** If conservative catch-up plus execution and response reserve is at least remaining budget, waiting cannot satisfy the deadline under those estimates. Route to an eligible source, return a permitted stale/pending result, or fail; queueing anyway creates late work.

**Durability counterexample.** A token requiring version 50 cannot force a failover region whose durable state ends at 48 to return 50. Read consistency mechanisms do not repair missing replication; the API must expose recovery/reconciliation semantics.

Operational invariants are: acknowledgement semantics explicit; every surface scoped; floors enforced; high-water monotonic; tokens safe; projections/caches versioned; snapshots preserved; concurrent writes distinguished; deadlines bounded; failover honest; and violations directly observable.

## Alternatives and Trade-Offs

Leader/strong reads simplify currentness but add latency, cost, and a hot dependency. Replica reads improve locality/throughput but need tokens, waiting, or weaker contracts. Session consistency often gives good UX without global coordination but requires state propagation.

Returning the committed representation eliminates an immediate GET but can enlarge mutation responses and does not solve list/search visibility. Waiting for projection gives a simple client flow but couples write latency/availability to asynchronous infrastructure. Pending visibility decouples at lifecycle cost.

Sticky routing is cheap but fragile. Version tokens prove a floor but add protocol/state complexity. Server-side session state helps thin clients but adds storage/privacy/lifetime concerns; client tokens must be protected and propagated.

Overlaying recent writes makes lagging queries feel current but complicates filters, sorting, pagination, deletion, and authorization. Strong source queries may be simpler but expensive. Some eventual analytics/search surfaces should remain explicitly eventual.

Bounded staleness gives predictability at coordination/capacity cost. Eventual reads maximize availability/throughput but cannot support workflows that require immediate observation. Choose per invariant, not fashion.

## Failure Modes and Misconceptions

- “Successful write means every read sees it.” Acknowledgement and each read surface need explicit coupling.
- “Strong database means strong API.” Caches, indexes, projections, and regions can be weaker.
- “Read-your-writes means latest.” A concurrent writer can produce a newer legitimate value.
- “Serializable means real-time order.” Serializability alone can choose a non-real-time serial order.
- “Eventual means within a few seconds.” No bound exists unless separately promised and verified.
- “Sticky session is a guarantee.” Topology/failover/cache/projection can break affinity.
- “One scalar token fits all shards.” Independent version domains need scoped/vector semantics.
- “The client can send a timestamp.” Untrusted/skewed clocks are not authoritative versions.
- “Token grants access.” Authorization is reevaluated independently.
- “No-cache forces current projection.” HTTP validation cannot make an async view catch up.
- “Created resource appearing in GET means list is current.” Detail and index are different surfaces.
- “Strong read fixes lost updates.” Conditional writes/transactions are needed.
- “Optimistic UI is read-your-writes.” It is local pending state.
- “Failover can honor every token.” Missing weakly replicated data cannot be read.
- “Average replication lag proves SLO.” Stuck partitions and tail violations matter.
- “Retry the timed-out write with a new ID.” That can duplicate an already committed effect.

## Worked Examples

### Example 1

A create commits version 42 and returns it with `Location`. An immediate GET reaches replica version 40. Because the session floor is 42, the API waits briefly then routes to the leader and returns at least 42. Returning 40 would be an observable regression.

### Example 2

The resource GET sees a new order immediately, but `GET /orders?customer=7` reads an index at checkpoint 39 and omits it. The API accepts checkpoint 42 and waits/overlays, or documents the list as eventual. Strong resource storage alone did not satisfy collection visibility.

### Example 3

A session observes versions 10, 12, then is load-balanced to a replica at 11. High-water is 12, so version 11 is rejected. A later concurrent writer produces 13; returning 13 satisfies monotonic/read-your-writes even though it differs from the session's own value.

### Example 4

Two independent partitions both use local version 50. Comparing them numerically says nothing about causality. The consistency token stores scoped positions `{A:50,B:50}` or an opaque global checkpoint generated by an authority; it never treats them as one counter.

### Example 5

A projection is estimated 300 ms behind. The read has 250 ms remaining, needs 40 ms execution and 30 ms response reserve. Since $300+40+30>250$, waiting is infeasible. The API uses an eligible source/overlay or returns pending rather than queueing doomed work.

### Example 6

A client reads version 5, edits, and sends `If-Match: "5"`. Another writer committed version 6. The origin returns a precondition failure; it does not overwrite version 6. Read-your-writes would not have prevented this lost-update race by itself.

### Example 7

A profile cache holds version 20 while the session token requires 22. Although the entry is within TTL, it cannot satisfy the consistency floor. The cache revalidates/loads version 22 or higher and only then advances session state.

### Example 8

A local-region write at version 70 was acknowledged under asynchronous cross-region replication. The region fails while the survivor ends at 68. A token for 70 cannot manufacture the missing state. The API exposes recovery/pending/loss policy rather than returning 68 as if the guarantee held.

### Example 9

Page one is read at snapshot 100. Inserts occur before page two. The cursor carries snapshot 100, so page two continues the same ordered view without duplicates/skips. If snapshot 100 expired after failover, the API returns restart-required instead of silently switching to live version 110.

### Example 10

A web client shows an optimistic address update before server response. The server normalizes it and commits version 31. The UI replaces pending state with the authoritative representation/token. On rejection it rolls back; another device sees only confirmed server state.

## Cross-Program Connections

[Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies histories, linearizability, session guarantees, causality, replication, quorum, and partitions.

[Database Engineering](../../18-database-engineering/ROADMAP.md) provides transactions, isolation, MVCC, snapshots, indexes, replicas, commit positions, and conflict control.

[Data Engineering](../../19-data-engineering/ROADMAP.md) connects CDC, outbox, materialized views, projection checkpoints, lag, replay, and reconciliation.

[Network Engineering](../../24-network-engineering/ROADMAP.md) explains region/replica routing, affinity, partitions, failover, and latency trade-offs.

[Security Engineering](../../25-security-engineering/ROADMAP.md) governs revocation currentness, token integrity, authorization separation, tenant scope, and non-disclosure.

[Platform Engineering](../../29-platform-engineering/ROADMAP.md) owns consistency-token propagation, client libraries, routing, cache integration, failover policy, and violation telemetry.

## References

1. Amazon Web Services, [DynamoDB read consistency](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.ReadConsistency.html).
2. Google Cloud, [Spanner: TrueTime and external consistency](https://cloud.google.com/spanner/docs/true-time-external-consistency).
3. Google Cloud, [Spanner reads outside transactions](https://cloud.google.com/spanner/docs/reads).
4. Microsoft Azure, [Consistency level choices in Azure Cosmos DB](https://learn.microsoft.com/en-us/azure/cosmos-db/consistency-levels).
5. Microsoft Azure, [Manage consistency levels in Azure Cosmos DB](https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/how-to-manage-consistency).
6. IETF, [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html).

## Exercises

### Exercise 1

Define write acknowledgement and visibility contracts for create/update/delete across resource GET, collection list, search, cache, and analytics. Choose which surfaces support a consistency token and why.

### Exercise 2

Design a bounded session token for a system with 1,000 partitions, multiple devices, resharding epochs, and untrusted clients. Cover merge, lifetime, integrity, authorization, and denial-of-service.

### Exercise 3

A replica is 180 ms behind; remaining read deadline is 220 ms, execution is 35 ms, and response reserve is 25 ms. Analyze waiting. Then the estimate rises to 190 ms and leader routing costs 80 ms. Define the decision and outcome.

### Exercise 4

Design read-your-writes for create-then-search with asynchronous indexing, sorting, pagination, deletion, and authorization. Compare barrier waiting, overlay, source query, and pending visibility.

### Exercise 5

Create a history-based test plan for sessions, concurrent writers, caches, projections, region failover/failback, backup restore, token loss/forgery, snapshot pagination, and timeout-after-commit. State invariants and metrics.

## Answers to the Exercises

### Answer 1

Define synchronous success as source-of-truth commit with resource ID/version/outcome; `202` only for durable pending lifecycle. Resource GET accepts the version floor and routes/waits/escalates. Collection/search accept a projection checkpoint token only if their index can prove/overlay the change; otherwise document bounded/eventual visibility and return pending status. Cache entries carry source versions and cannot satisfy a higher floor. Analytics usually remains explicitly asynchronous with `asOf`/watermark rather than interactive session tokens. Delete includes tombstone/version so stale cache/index entries cannot resurrect. State replication/durability scope and failover behavior for each surface.

### Answer 2

A raw 1,000-entry vector is too large for every request. Use workflow/resource-scoped tokens, compact signed checkpoint summaries where the platform provides a comparable global position, or server-side session state keyed by opaque token with TTL/quotas. Merge only comparable partition positions by componentwise maximum; epoch changes require translation/reconciliation, not reset. Integrity-protect tenant/session/scope/epoch and cap size, age, number of active sessions, and escalation rate. Reauthorize every request independently. Cross-device behavior uses authenticated server session or explicit token transfer. Invalid/high/future tokens fail safely without forcing unbounded waits.

### Answer 3

First case needs $180+35+25=240$ ms, exceeding 220 ms, so waiting on that estimate is infeasible. A leader path at 80+35+25=140 ms fits if admission/capacity and region policy permit it. When lag becomes 190 ms, wait is even less feasible; route to leader. If leader admission is unavailable or its conservative tail cannot fit, return the documented consistency-unavailable/pending outcome or an explicitly permitted stale result; never drop the floor silently. Record required/observed version, decision, estimate, and deadline suppression.

### Answer 4

Emit a source commit/checkpoint token. Barrier waiting makes search simple but couples latency/availability to index catch-up. Overlay merges recent session creates/updates/deletes onto results, but must re-evaluate authorization/filter/sort, deduplicate, place items correctly, adjust pagination/tombstones, and qualify counts. Source query is authoritative but can be expensive or lack search semantics. Pending visibility exposes a status milestone and lets clients use resource GET until indexed. Choose barrier/overlay for bounded high-value workflows; otherwise make search lag explicit. Snapshot cursors carry index checkpoint, and deleted items remain tombstoned through replay windows.

### Answer 5

Generate histories of acknowledged writes and qualifying reads; assert observed version never falls below session high-water and no stale surface claims the floor. Race concurrent writers with `If-Match`, distinguishing legal newer versions from regression. Inject cache/index lag and lost/reordered events, SDK/session change, token omission/forgery, leader change, partition, region loss, failback, restore/epoch, and continuous writes. Page through a snapshot while mutating. Lose write responses after commit and retry same idempotency key. Metrics include write milestone/version, required/observed floor, surface checkpoint, time-to-visible distributions, wait/escalation, violations, token errors, strong-read cost, RPO/recovery state, and deadline outcomes.
