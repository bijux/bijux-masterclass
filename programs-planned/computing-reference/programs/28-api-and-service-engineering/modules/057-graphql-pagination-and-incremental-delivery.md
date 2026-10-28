---
module_id: API-057
program: API & Service Engineering
level: 2
module_number: 57
title: GraphQL Pagination and Incremental Delivery
status: complete
last_verified: 2026-09-02
---

# GraphQL Pagination and Incremental Delivery

## One-Page Review

### Governing question

How should a GraphQL API expose large changing collections and progressively deliver slow selections while keeping order, cursor scope, page boundaries, patch identity, failure, cancellation, and protocol maturity explicit?

### Essential definitions

- A **connection** is a paginated collection object containing edges and page information.
- An **edge** represents one node's membership/relationship in a connection and carries its cursor plus relationship metadata.
- A **cursor** is an opaque continuation value identifying a position under one documented order and query scope.
- **keyset pagination** seeks after/before the last ordered key tuple instead of skipping a numeric offset.
- A **total order** compares every visible edge deterministically; a unique tie-breaker completes non-unique sort fields.
- **pageInfo** reports continuation facts such as `hasNextPage`, `hasPreviousPage`, `startCursor`, and `endCursor`.
- **overfetch-by-one** requests at most page size plus one edge to determine whether another edge exists.
- **incremental delivery** splits one query result into an initial payload and later patches for selected deferred fragments or streamed list items.
- `@defer` and `@stream` are current GraphQL Working Group proposals, not features of the September 2025 release specification.
- A **patch identity/path** lets the client associate a later payload with the pending selection and response position it completes.

### Central model, mechanism, or theorem

For ascending order tuple $(s,id)$ and decoded cursor $(s_c,id_c)$, the forward keyset predicate is

$$
(s>s_c)\lor(s=s_c\land id>id_c),
$$

followed by the same `ORDER BY s ASC, id ASC` and a limit of $p+1$. Return the first $p$ edges and set `hasNextPage` iff the extra edge exists. Backward traversal reverses the seek/computation internally but returns edges in the same public order.

A cursor is valid only under its bound scope:

$$
scope=(connection,tenant,filters,order,visibility,snapshot/version).
$$

Incremental delivery changes when response positions arrive, not the intended combined result. Absent interleaving mutations and failures, merging all patches should be semantically equivalent to non-incremental execution.

### Critical invariants

Every connection defines one deterministic total order and tie-breaker. Cursors are opaque, versioned, bounded, authenticated when tampering matters, and validated against connection/query/tenant/visibility/order scope. Clients never edit/decode them as contract. Page sizes have defaults and maxima; negative/conflicting arguments fail. Forward/backward results use the same edge order. Empty pages have null start/end cursors. `hasNextPage`/`hasPreviousPage` state precisely which direction/evidence they describe; total count is separate and never implied. Inserts/deletes between pages have documented snapshot/live semantics. Authorization filters precede page-boundary claims.

Incremental directives are exposed only when the server, transport path, and supported clients share one tested proposal/version. The initial payload and every subsequent payload are bounded, ordered/identifiable, redacted, cancellable, and merged exactly once. Patch errors retain their response association; non-null propagation and completion notices are handled. Proxies do not buffer or strip the chosen streaming representation. Client disconnect cancels remaining work cooperatively. Incremental delivery never masquerades as subscription/live updates or a work-reduction mechanism.

### Common failures

Unbounded list fields; offset pagination presented as stable; ordering by non-unique timestamp; cursor containing only a timestamp; cursor reusable across tenants/filters/orders; unsigned client-editable cursor that changes scope; encoding secrets; relying on base64 as integrity; fetching exactly $p$ then guessing `hasNextPage`; reversing edge order for backward pages; returning contradictory pageInfo; mandatory expensive total counts; applying authorization after pagination; snapshot promises without snapshot token/retention; duplicates/gaps ignored under concurrent writes; accepting `first` and `last` ambiguously; zero/negative/huge sizes; N+1 inside edges; adopting draft `@defer`/`@stream` as stable; confusing response stream with subscription; buffering all patches at proxy/client; applying a patch twice/out of order; using only labels as identity; ignoring cancellation; leaking errors after initial headers; and measuring first-byte improvement while total work, re-renders, memory, or tail latency worsens.

### Compact example

Orders sort by `(created_at,id)`. Page size 20 is executed with limit 21. The cursor binds tenant, filter digest, order version, and the last tuple. Twenty edges return; the extra row makes `hasNextPage=true`. A client next requests `after:endCursor`. If it also requests a slow audit fragment with a supported proposed `@defer`, the initial order data can arrive first and the fragment later; the client merges by protocol identity/path, not arrival guesswork. **Conclusion:** pagination stabilizes collection traversal; incremental delivery schedules one operation's response.

### Connections

[GraphQL Schema Design](055-graphql-schema-design.md) defines collection types, while [GraphQL Execution, Resolvers, and Batching](056-graphql-execution-resolvers-and-batching.md) executes edges efficiently. [Filtering, Sorting, and Pagination](017-filtering-sorting-and-pagination.md) supplies transport-independent ordering foundations. Authorization and cost control follow next.

## Governing Question

What collection identity and ordering does a cursor preserve, what anomalies are allowed as data changes, and—when experimental incremental delivery is enabled—how do server, transport, and client reconstruct one bounded operation without confusing it with a live event stream?

## Why This Matters

GraphQL makes nested collections easy to select, but an unbounded list is a denial-of-service and latency hazard. Pagination is therefore part of schema correctness, not a UI afterthought. Offset pagination is simple yet shifts under inserts/deletes and often becomes slower at high offsets. Cursor pagination can be stable and efficient only when the cursor represents a complete ordering position and is bound to the query's visibility scope.

Connections add useful structure. Edge objects can carry relationship facts; pageInfo carries continuation facts; nodes remain reusable domain objects. The convention does not automatically solve database ordering, concurrency, authorization, total counts, or cursor security. Those are server contracts.

Incremental delivery addresses a different axis. Pagination bounds how much collection data one request selects; `@defer`/`@stream` proposals can prioritize when selected response positions arrive. They can improve time to useful data but retain work and extend request lifetime. As of the September 2025 GraphQL specification, these directives and their incremental payload format are not part of the stable release; the Working Group proposals and HTTP RFC remain subject to change. Production use needs explicit capability/version negotiation and end-to-end compatibility.

## Prerequisites and Retrieval

Retrieve [Filtering, Sorting, and Pagination](017-filtering-sorting-and-pagination.md), [Compatibility Policy](021-api-contracts-and-behavioral-guarantees.md), [GraphQL Schema Design](055-graphql-schema-design.md), and [GraphQL Execution, Resolvers, and Batching](056-graphql-execution-resolvers-and-batching.md). Be able to define lexicographic ordering, unique tie-breakers, response paths, null propagation, request cancellation, and the difference between release specifications and active proposals.

## Learning Objectives

After completing this module, you can:

1. design connection, edge, and pageInfo types with precise forward/backward semantics;
2. derive correct keyset predicates for composite ascending/descending orders;
3. design opaque scoped cursors with versioning, integrity, bounds, and rotation;
4. reason about duplicates/gaps under live versus snapshot traversal;
5. compute page continuation with overfetch-by-one without claiming unsupported directions;
6. distinguish pagination, incremental delivery, and subscriptions;
7. evaluate `@defer`/`@stream` and HTTP multipart delivery at their current proposal maturity;
8. implement safe patch merge, error, cancellation, and proxy behavior; and
9. verify performance and semantics across datastore, GraphQL executor, transport, and client.

## Core Exposition

### Model a collection as a connection

A connection type normally exposes `edges` and non-null `pageInfo`. Each edge exposes a `node` and opaque cursor; it can also expose relationship metadata such as membership date, rank, or permission. Returning only `nodes` is convenient but removes per-edge cursor/metadata, so retain `edges` when clients paginate or relationships matter.

The Cursor Connections Specification reserves connection/edge patterns and `PageInfo`. Forward pagination uses non-negative `first` with `after`; backward uses non-negative `last` with `before`. Supporting both is useful only when the datastore and product require it. Reject unclear combinations such as `first` plus `last` under a documented policy rather than inventing surprising slicing.

Connection arguments may include typed filters and ordering. The same arguments define a distinct logical connection. A cursor from `status:OPEN, order:CREATED_ASC` must not silently continue `status:CLOSED` or another order.

### Define a stable total order

Pagination requires a deterministic total order across all visible edges. If `created_at` is not unique, append a stable unique tie-breaker such as immutable order ID. For descending primary sort and ascending ID, derive the lexicographic comparison exactly; do not apply one generic `>` to mixed directions.

Null sort values need explicit placement (`NULLS FIRST/LAST`) and cursor representation. Locale/collation, case folding, timezone, database version, and computed ranking can change comparison. Version the order contract or invalidate cursors when these semantics change.

Mutable sort keys cause movement between pages. An edited record can be duplicated, skipped, or move across the cursor. Choose immutable sort keys for traversal where possible. Otherwise document live-view anomalies or bind a snapshot/revision that can reproduce the view within a retention window.

### Build and validate scoped opaque cursors

A cursor is a server-issued continuation capability, not a public serialized database row. Its internal payload can include version, connection identity, direction/order version, last tuple, filter digest, tenant/visibility scope, and snapshot marker. Bound size before decoding. Authenticate it with a rotating key when tampering could alter scope or cost; encrypt only if payload confidentiality is needed. Base64 is encoding, not protection.

Validate version, signature, expiry/retention, tenant/principal policy as appropriate, filter/order digest, field/connection, and tuple types before querying. Return a stable invalid/expired-cursor error without exposing internals. Key rotation should accept a controlled previous-key window while issuing only the current version.

Avoid embedding raw personal data, SQL, secrets, or long filter expressions. A digest plus server-side/versioned contract is usually enough. Cursors may appear in logs, browser history, analytics, and support tickets; classify and redact them.

### Execute forward pages with overfetch-by-one

Given cursor tuple `(created,id)`, forward seek selects rows lexicographically after it under the exact same filter/visibility and order, limited to $p+1$. If more than $p$ rows arrive, drop the extra and set `hasNextPage=true`; otherwise false. `endCursor` comes from the last returned edge, not the probe row.

<!-- bijux-verify: {"id":"keyset-forward-page","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"page=[(10, 8), (11, 1), (11, 4)]\nhas_next=True\nend_cursor=(11, 4)\n","stderr":""}} -->
```python
def forward_page(rows, after, size):
    eligible = sorted(row for row in rows if row > after)
    probe = eligible[: size + 1]
    return probe[:size], len(probe) > size

rows = [(9, 7), (10, 5), (10, 8), (11, 1), (11, 4), (12, 2)]
page, has_next = forward_page(rows, after=(10, 5), size=3)
print("page=" + str(page))
print("has_next=" + str(has_next))
print("end_cursor=" + str(page[-1]))
```

Real code encodes rather than exposes tuples and applies tenant/filter/authorization inside the query. If authorization is filtered afterward, a short page can falsely claim end-of-list or leak hidden density.

`hasPreviousPage` during forward traversal may be cheap from presence of `after`, but the connection specification permits conservative behavior in some directions. State the exact contract; do not issue expensive reverse queries unless product value justifies them.

### Implement backward traversal without reversing public order

Backward pagination asks for edges before a cursor and returns at most `last`. A datastore commonly seeks in reverse order to get the nearest preceding rows efficiently, overfetches one, then reverses the selected rows back into the connection's public order. Clients should see the same edge ordering whether traversing forward or backward.

Mixed-direction composite sorts require mirrored predicates per component. Property-test against an in-memory total-order oracle across duplicates, boundaries, and null policy. Empty results have null `startCursor`/`endCursor`; one result has equal start/end.

### Choose live or snapshot traversal semantics

Under live keyset pagination, inserts after the cursor can appear later; inserts before it will not. Deletes can shrink later pages. An item whose sort key changes can be duplicated or missed. Keyset avoids offset shifting but does not create a snapshot.

Snapshot traversal binds a database snapshot, high-water mark, revision, or immutable dataset version into the cursor. It improves repeatability but consumes storage/state, expires, complicates distributed sources, and can hide newer records. Define retention and expiry behavior. A high-water mark prevents later inserts above a bound but may not freeze updates/deletes.

Total counts are often expensive and consistency-sensitive. Expose them only when semantically needed, with exact/estimated and snapshot meaning documented. `hasNextPage` from $p+1$ does not imply a total.

### Compare offset and cursor designs honestly

Offsets support direct page numbers and are easy for small stable datasets. They can skip/duplicate under mutation and require scanning/skipping at high offsets depending on datastore. Cursor/keyset traversal is efficient and locally stable but does not jump naturally to page 500 and makes shareable page numbers harder.

Search rankings may be nondeterministic or recomputed. Use provider search-after tokens or snapshot/version identifiers rather than pretending an offset is a durable cursor. The API can expose an opaque provider token only after binding it to tenant/filter/order and governing expiry.

### Separate pagination from incremental delivery

Pagination selects a bounded slice via another operation per continuation. Proposed `@stream` can deliver items from one selected list over several payloads; it does not justify selecting an unbounded list. Proposed `@defer` delays a fragment selection; it does not remove its computation. Subscriptions produce execution results for events over time and represent changing data, whereas incremental delivery reconstructs one operation result.

Use pagination for cardinality and navigation. Consider incremental delivery when one bounded operation contains independently useful fast and slow regions, and supported clients benefit from earlier rendering. Sometimes a separate lazy query is simpler, cacheable, retryable, and more interoperable.

### Treat `@defer` and `@stream` as proposals

The active Working Group proposal places `@defer` on fragment spreads/inline fragments and `@stream` on list fields, with conditional arguments, labels, and `initialCount` for streams. Proposed results use an initial payload and later notices/results such as `pending`, `incremental`, `completed`, and `hasNext`. Details and transport profiles can change until accepted into a release.

Do not advertise directives unless the chosen server implementation actually follows a named tested proposal version and every supported client can parse/merge it. Capability negotiation must prevent an incremental response being interpreted as ordinary JSON. Record exact library versions/proposal date/profile; avoid claiming generic “GraphQL compliance” covers it.

Labels aid correlation but may repeat under list paths and are not sufficient identity alone. Clients follow protocol IDs and response paths/subpaths. Apply each update exactly once, tolerate legal interleaving, and mark pending regions complete only on completion notice.

### Engineer the HTTP path end to end

Incremental delivery over HTTP is itself an RFC/proposal, commonly using a negotiated `multipart/mixed` response streamed without whole-body buffering. HTTP/1.1 chunked transfer is not an HTTP/2 header; HTTP/2 has native streaming framing. Do not hard-code obsolete media-type parameters from one implementation as universal.

Test client `Accept`, server response `Content-Type`, boundary parsing, chunk fragmentation, compression, proxy/CDN buffering, timeouts, idle limits, load balancers, service meshes, tracing middleware, and browser/runtime streaming behavior. A proxy that buffers until completion erases first-payload benefit while retaining complexity.

Headers/status may already be committed before later execution fails. Later errors must travel in the incremental protocol, not as a new HTTP status. Logs and monitors must understand completion versus truncated connection.

### Preserve patch consistency and null/error semantics

The initial payload can omit deferred fields or contain initial streamed items according to the adopted proposal. The client maintains a pending registry and applies data/items at the specified response location. Validate paths and types; reject malformed, duplicate-conflicting, unknown-ID, or post-completion patches.

Non-null failures can invalidate an incremental boundary or an ancestor already shown. The proposal's completion/error mechanisms must be implemented exactly so the client can retract/null affected data. UI code must represent pending, present-null, failed, and completed—not assume omitted means null.

Interleaving mutations can make late fields reflect different moments. Incremental delivery proposals do not promise snapshot consistency automatically. Use a transaction/snapshot/domain revision where the product requires it, or document ordinary consistency.

### Bound lifecycle, work, and client rendering

Limit page sizes, selected streamed cardinality, number of defers/streams, patch count/bytes, open duration, concurrent incremental operations, buffered unsent results, and per-client connections. API-058 owns general cost admission, but delivery has its own lifecycle limits.

Propagate one deadline and cancellation signal. On disconnect/cancel, stop pending resolvers and release snapshots/cursors/buffers; committed effects remain governed separately. Slow clients require backpressure or bounded buffering. Never retain entire result solely to produce small patches unless measured value justifies it.

Clients can re-render per patch and lose the latency win. Batch ready patches and UI updates without adding excessive delay. Measure time to first useful payload, time to each critical region, completion time, bytes, patch count, render work, abandoned work, errors, and resource occupancy.

### Verify collection and delivery semantics

For pagination, property-test random ordered datasets against an oracle: traverse all pages in both directions; assert order, no duplicate under immutable data, exact membership, start/end cursors, and page flags. Test equal sort keys, nulls, empty/one/exactly-$p$/$p+1$, min/max sizes, malformed/tampered/expired/wrong-scope cursors, authorization changes, inserts/deletes/mutable keys, and snapshot expiry.

For incremental delivery, compare fully merged output to ordinary execution under fixed data. Randomize chunk boundaries and legal patch readiness order. Test fragment/list nesting, aliases, null propagation across boundaries, per-patch/terminal errors, disconnect at every point, duplicate/truncated/malformed parts, slow readers, proxy buffering, compression, deadline, and version negotiation. Inspect logs/traces for cursor, variables, and error leakage.

## Definitions and Notation

Let an edge have total-order key $K(e)=(s(e),id(e))$. Cursor $c$ decodes under version/policy to $(scope_c,K_c)$. For page size $p$, eligible forward edges are $E^+=\{e:scope(e)=scope_c\land K(e)>K_c\}$ in ascending order. Probe $P=take(p+1,E^+)$, returned page $R=take(p,P)$, and `hasNextPage` is $|P|>p$.

Let incremental output be initial payload $I$ and updates $U_1,\ldots,U_k$ under an adopted proposal/profile. Merge $M(I,U_1,\ldots,U_k)$ must apply each identified update once at its valid response position. Under fixed data, successful completion, and compatible implementation/client, target equivalence is $M(...)=Execute(O)$.

## Mechanisms, Invariants, or Proof Structure

Lexicographic seek with a unique tie-breaker partitions the total order: every eligible edge is strictly after the cursor and no edge can occupy the same key. Reusing the exact predicate/order yields contiguous traversal under immutable data. Without uniqueness, two equal-sort edges cannot be consistently divided by a cursor containing only the shared value, so duplicates or omissions are unavoidable.

Overfetch-by-one proves existence of at least one further eligible edge without counting all remaining edges. If probe length exceeds $p$, its $(p+1)$th edge witnesses continuation; otherwise no further edge exists under that query snapshot/evaluation. It does not prove the opposite traversal direction or total count.

Cursor scope binding prevents substitution: if filters/order/tenant differ but the server accepts the old tuple, the continuation no longer denotes a position in the requested connection. Authenticating or server-indexing the scope prevents caller modification; server validation prevents accidental cross-use.

Incremental equivalence is conditional. Each response position from the ordinary result must appear exactly once in initial data or a valid patch, patch application must preserve its path/list position, and errors/null propagation must match. Interleaving mutations, cancellation, protocol mismatch, or duplicated/lost updates break the premises.

## Alternatives and Trade-Offs

Offset pagination is transparent and supports page jumps; keyset pagination improves continuation efficiency/stability but needs opaque cursors and total order. Snapshot cursors improve repeatability but add retention/state. Live cursors expose recent changes but permit documented anomalies.

Connections provide standardized edge/page metadata and client tooling. A simpler page object may suffice outside Relay ecosystems, but consistency across a graph is valuable. Exposing both `edges` and `nodes` adds convenience and schema surface; ensure they derive from identical order/results.

Overfetch-by-one is cheap relative to exact count. Exact totals serve genuine product needs but may be expensive/stale. Estimated totals need explicit labeling. Avoid silently computing totals because the client selected pageInfo.

`@defer`/`@stream` can improve time-to-useful-data in capable stacks. Separate follow-up queries have broader interoperability, independent retry/cache, and simpler failures. Server-side prefetch may solve latency without protocol changes. Choose from measured user experience and operational complexity.

Multipart streaming fits request/response infrastructure but faces buffering and experimental profiles. Other transports may stream naturally but add connection/state complexity. Transport choice cannot change GraphQL patch semantics.

## Failure Modes and Misconceptions

- **“Opaque means base64.”** Opacity is client contract; integrity/confidentiality need signing/encryption and validation.
- **“Cursor pagination creates a snapshot.”** It avoids offsets but live inserts/deletes/mutable sort keys still create anomalies.
- **“Timestamp is enough.”** Equal timestamps require a unique stable tie-breaker and matching predicate.
- **“Backward means reverse the edges.”** Fetch may reverse internally; public edge order stays consistent.
- **“`hasNextPage=false` means the dataset ends forever.”** It is scoped to filters, visibility, order, and evaluation/snapshot.
- **“Total count comes with connections.”** It is optional, potentially expensive, and semantically separate.
- **“`@stream` replaces pagination.”** It schedules delivery of selected list items; selection cardinality still needs bounds.
- **“Incremental delivery is stable GraphQL September 2025.”** It remains a Working Group proposal and needs exact profile/version compatibility.
- **“Incremental means live updates.”** It reconstructs one operation; subscriptions/events represent later changes.
- **“First payload means less work.”** Deferred work still runs unless cancelled; total bytes/CPU may increase.
- **“Labels uniquely locate patches.”** Protocol identity plus path/subpath governs association; list instances can repeat labels.
- **“HTTP streaming works if the app writes chunks.”** Every proxy, runtime, parser, timeout, compression, and client must preserve it.

## Worked Examples

### Example 1

**Situation:** 30 orders share the same second-level timestamp. **Reasoning:** timestamp-only cursor cannot locate a unique boundary. Order by `(created_at,id)` and encode both. **Conclusion:** total ordering requires a stable tie-breaker.

### Example 2

**Situation:** A cursor from tenant A/open orders is used for tenant B/closed orders. **Reasoning:** tuple position has no valid meaning and may leak scope. Validate signed connection, tenant, filter digest, and order version. **Conclusion:** cursors bind query scope.

### Example 3

**Situation:** Page size 20 yields 21 authorized rows. **Reasoning:** return first 20, cursor from row 20, and `hasNextPage=true`; never expose probe row. **Conclusion:** one extra row witnesses continuation.

### Example 4

**Situation:** Backward query fetches descending for efficiency. **Reasoning:** select nearest prior edges, overfetch, then reverse returned slice into public ascending order. **Conclusion:** traversal direction does not redefine connection order.

### Example 5

**Situation:** Authorization filtering occurs after database limit. **Reasoning:** hidden rows create short pages and false flags, leaking density. Push visibility into eligible-set query or overfetch under a formally bounded safe policy. **Conclusion:** visibility precedes pagination claims.

### Example 6

**Situation:** An item changes its sort score between pages. **Reasoning:** it may move across the boundary and repeat/disappear. Use snapshot/version or document live anomalies; do not claim exactly-once traversal. **Conclusion:** keyset is not snapshot isolation.

### Example 7

**Situation:** Client sends `@defer` to a server that does not expose it. **Reasoning:** validation should fail; server must not silently invent multipart behavior. Negotiate a supported proposal/profile. **Conclusion:** experimental capability is explicit.

### Example 8

**Situation:** Proxy buffers multipart until final boundary. **Reasoning:** user gets no early data while server holds a longer request. Add end-to-end flush tests or choose separate queries. **Conclusion:** deployment path determines delivery benefit.

### Example 9

**Situation:** A late patch's non-null field fails above its boundary. **Reasoning:** client must process protocol error/completion and invalidate affected ancestor data, not leave stale UI. **Conclusion:** incremental null propagation needs client state machinery.

### Example 10

**Situation:** `@stream` sends 200 one-item patches and UI renders each. **Reasoning:** network/render overhead exceeds first-paint gain. Bound selected items, batch ready updates, and measure rendering/completion. **Conclusion:** progressive delivery needs lifecycle economics.

## Cross-Program Connections

- **Database Engineering:** composite indexes, seek predicates, collation, MVCC snapshots, and counts implement cursor semantics.
- **Distributed Systems Engineering:** concurrent mutation, snapshot retention, cancellation, partial failure, and local clocks constrain traversal/delivery.
- **Security Engineering:** cursor scope/signing, tenant visibility, error redaction, and resource limits protect boundaries.
- **Network Engineering:** HTTP framing, multipart parsing, buffering, compression, flow control, and disconnects govern patches.
- **Client Engineering:** normalized caches, connection merging, pending states, patch idempotence, and rendering costs complete the protocol.
- **Formal Methods and Testing:** total orders, partition proofs, oracle traversal, and merge equivalence expose edge cases.

## References

1. GraphQL Foundation, “GraphQL Specification, September 2025,” list/response-path/execution/error behavior and stable release boundary, verified 2026-09-02. [GraphQL specification](https://spec.graphql.org/September2025/).
2. Relay, “GraphQL Cursor Connections Specification,” connection/edge/PageInfo requirements, forward/backward arguments, ordering, slicing, and page flags, verified 2026-09-02. [Connections specification](https://relay.dev/graphql/connections.htm).
3. GraphQL Foundation, “Pagination,” official connection and cursor-oriented guidance, verified 2026-09-02. [GraphQL documentation](https://graphql.org/learn/pagination/).
4. GraphQL Working Group, “Proposal: Incrementally deliver data with `@defer` and `@stream`,” active proposal semantics and payload model, verified 2026-09-02. [Working Group RFC](https://github.com/graphql/graphql-wg/blob/main/rfcs/DeferStream.md).
5. GraphQL over HTTP Working Group, “Incremental Delivery over HTTP,” proposed multipart/chunked delivery profile, verified 2026-09-02. [HTTP RFC](https://github.com/graphql/graphql-over-http/blob/main/rfcs/IncrementalDelivery.md).
6. IETF, RFC 9113, “HTTP/2,” June 2022, framing, flow control, and prohibition of HTTP/1.1 transfer-encoding connection semantics. [RFC Editor](https://www.rfc-editor.org/rfc/rfc9113.html).

## Exercises

### Exercise 1

Define connection, edge, cursor, keyset pagination, total order, overfetch-by-one, pageInfo, incremental delivery, and patch identity. Distinguish pagination, `@stream`, and subscription.

### Exercise 2

Derive forward and backward predicates for `priority DESC, created_at ASC, id ASC`. State the index/order needs and why the backward public order must remain unchanged.

### Exercise 3

Design a cursor envelope for tenant-scoped filtered orders with a 15-minute snapshot. Cover fields, integrity, confidentiality, size, validation, rotation, expiry, errors, and logging.

### Exercise 4

Diagnose a connection that orders only by timestamp, filters authorization after `LIMIT`, accepts any page size plus `first` and `last`, computes exact total always, and reverses backward edges. Provide repair/tests.

### Exercise 5

Design paginated and optionally incremental emergency incident delivery to web/mobile clients through proxies. Incidents change concurrently; locations are sensitive; responder details are slow. Specify connection/order/snapshot, cursors, pageInfo, `@defer` adoption boundary, patch/client lifecycle, cancellation, limits, evidence, and fallback.

## Answers to the Exercises

### Answer 1

A connection is a collection object with edges and pageInfo. An edge represents membership and carries node, cursor, and optional relationship facts. A cursor is an opaque continuation position scoped to one order/query. Keyset pagination seeks relative to the last composite key. A total order deterministically compares every edge. Overfetch-by-one requests $p+1$ to witness continuation. PageInfo reports directional continuation and boundary cursors. Incremental delivery splits one operation result into initial and later payloads. Patch identity/path associates each update with its pending response location.

Pagination selects another bounded slice in another operation. Proposed `@stream` progressively delivers items already selected by one bounded list operation. A subscription maps later source events to new execution results over time. Neither streaming nor subscription removes page-size/resource policy.

### Answer 2

For cursor $(p_c,t_c,id_c)$ and public order priority descending, then time/id ascending, “after” is `(priority < p_c) OR (priority = p_c AND created_at > t_c) OR (priority = p_c AND created_at = t_c AND id > id_c)`. Query with `ORDER BY priority DESC, created_at ASC, id ASC LIMIT p+1`.

For edges before the cursor, invert each lexicographic comparison: `(priority > p_c) OR (priority = p_c AND created_at < t_c) OR (priority = p_c AND created_at = t_c AND id < id_c)`. Efficient backward retrieval may use reversed physical order `priority ASC, created_at DESC, id DESC`, take `last+1`, then reverse returned slice into the public order. Use an index compatible with filters and composite order or datastore-specific search-after support. The unique immutable ID resolves ties. Public order must remain stable so clients can merge pages consistently and the Connections contract's forward/backward semantics agree.

### Answer 3

Use a compact versioned envelope containing key ID/version, connection coordinate/version, tenant/visibility-policy binding, normalized filter digest, exact order version, last composite tuple, snapshot/revision token plus issued/expiry times, and perhaps direction. Serialize canonically and authenticate with an AEAD/MAC under rotating server keys; use encryption if tuple/filter/snapshot metadata is sensitive. Keep sensitive location/customer values out and impose encoded/decoded byte/depth/type limits.

On receipt, decode within bounds; select allowed key/version; verify authentication before trusting fields; validate tenant/principal policy, connection, filter/order digest, tuple types/ranges, snapshot existence/retention, and expiry. Reject wrong-scope/tampered/expired cursors with stable safe codes and restart guidance, never decoder/SQL details. Accept previous signing keys only through a controlled rotation window and issue current version. Redact/hash cursors in logs/traces and prevent query-string analytics capture where possible.

### Answer 4

Add a stable unique tie-breaker to the timestamp and build the matching composite seek predicate/index. Move authorization/tenant visibility into the eligible database/dependency query before limit and page flags. Define one bounded default/max; reject negative/over-max and ambiguous `first`+`last` combinations. Use $p+1$ for directional continuation; compute exact total only behind an explicitly selected, authorized, budgeted field or omit it. Fetch backward efficiently in reverse internally, then return edges in the same public order.

Property-test traversal against an ordered oracle for equal timestamps, empty/one/$p$/$p+1$, both directions, start/end cursors, exact membership on immutable data, malformed/wrong-scope cursors, tenant overlap, policy changes, concurrent insert/delete/key mutation, and snapshot behavior. Measure query plans, rows/bytes, counts, latency, and leakage; ensure edge nodes batch without N+1.

### Answer 5

Expose `IncidentConnection` with edges carrying cursor and perhaps relationship-safe alert metadata, nodes carrying authorized incident data, and PageInfo. Order by immutable dispatch sequence or `(created_at,id)`; priority that changes should not be the only traversal key. Choose live traversal with explicit movement anomalies for a live dashboard, or a 15-minute snapshot/revision for audit/export. Cursor binds tenant, visibility policy, incident filters, order version, last tuple, and snapshot; authenticate/encrypt because location-related metadata is sensitive; bound/redact it. Page with capped `first`, use authorized seek plus one, and state only evidenced page flags. Exact total is optional.

Responder details may be selected in a separately retryable query by default. Enable proposed `@defer` only for an allowlisted web/mobile version after server/client/proxy interoperability tests; record exact WG/protocol profile and negotiate multipart capability. Initial payload contains usable incident/location data according to policy; pending IDs/paths track responder fragments; client applies each patch once, handles failure/null invalidation and completion, and keeps pending distinct from null. Do not treat it as live update—subscriptions/polling handle later incident changes.

Bound page size, defers, patches/bytes, open time, concurrent streams, buffers, and slow readers. Propagate deadline/cancellation and release snapshot/loaders on disconnect; committed assignment mutations remain separately recoverable. Test proxy buffering/chunk fragmentation/compression/timeouts, offline/old clients, malformed/duplicate/truncated patches, cross-tenant cursors, authorization changes, concurrent edits, snapshot expiry, responder partial failure, sensitive telemetry, time to useful/complete data, render count, total bytes/work, abandonment, and fallback to ordinary JSON plus follow-up query when negotiation fails.
