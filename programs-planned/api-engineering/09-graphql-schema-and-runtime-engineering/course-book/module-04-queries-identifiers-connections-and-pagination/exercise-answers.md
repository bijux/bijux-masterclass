# Worked Answers — Module 04: Queries, Identifiers, Connections, and Pagination

Use these solutions to audit your reasoning for **Queries, Identifiers, Connections, and Pagination**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. Why is a global ID not an authorization token?

It only identifies type and local identity. Possession does not prove tenant membership or field permission.

**Decisive evidence.** Decode a valid ID, then use it under a principal from another tenant. The source lookup must conceal the resource, proving identity decoding does not grant access.

The chapter’s decisive distinction is this: The course encodes type and local identity into an opaque string. Clients should not depend on its internal form, but the server may decode it to choose an authority. Obfuscation does not authorize access. Every decoded identifier still passes tenant and field policy.

## 2. What makes an ordering stable for cursor pagination?

It is total and deterministic, usually a business sort key plus a unique tie-breaker. The source applies the same order on every page.

**Decisive evidence.** Insert rows sharing the primary sort value and traverse multiple pages. The unique tiebreaker must prevent duplicates, skipped rows, and non-deterministic order.

In the cumulative capstone, the rule becomes concrete: The capstone's run connection orders by a stable tuple rather than a non-unique timestamp alone. A deterministic tie-breaker is mandatory. Offset pagination is easy to expose but becomes expensive and unstable as data changes; the course retains keyset semantics from Course 2.

## 3. Why bind a cursor to filters?

Reusing a position under different filters can skip or duplicate rows and reveal cross-query state. A filter hash makes misuse fail.

**Decisive evidence.** Reuse a cursor with a changed status or project filter. Signature validation may pass, but query binding must reject the continuation before source pagination.

A useful way to reason about the boundary is: A cursor created for status: RUNNING cannot be reused for status: FAILED. The codec signs a normalized filter hash and tenant identifier. Changing order fields also changes the cursor profile. The server rejects mismatches rather than producing plausible but incorrect pages.

## 4. Why include a high-water boundary?

It prevents newly inserted earlier rows from shifting the current traversal, giving a defined snapshot-like window.

**Decisive evidence.** Insert a newer row after page one. It must be absent from the existing traversal and present in a fresh traversal, demonstrating the declared high-water semantics.

The implementation consequence is: A ListRuns cursor signs tenant, normalized filter, position, and traversal high-water. Reusing it under another filter or tenant fails. Rows inserted above the high-water do not appear in the current traversal; a new query starts a new traversal.

## 5. Is base64 an opaque cursor security control?

No. Base64 is reversible. The course cursor is authenticated with HMAC and still requires authorization.

**Decisive evidence.** Tamper with one byte of a base64 cursor. A raw base64 offset may decode, while the HMAC-authenticated profile must reject modified state.

The important nuance is: Changing status, tenant, or sort order while reusing a cursor must fail. Otherwise a cursor can cross data populations and leak or skip records. The cursor is opaque because clients should not construct positions or depend on storage layout.

## 6. Why require `first` even with a default?

The schema and admission policy need an enforced maximum. Defaults help clients; they do not permit unbounded retrieval.

**Decisive evidence.** Coerce omitted, zero, negative, maximum, and over-maximum `first` values. Defaults may improve ergonomics, but every execution still needs an enforced cardinality bound.

Under concurrency or failure, the distinction becomes: GraphQL creates two page-size boundaries: the schema argument and the runtime policy. A default such as first: 20 improves ergonomics, but admission must enforce a maximum even when the variable is supplied dynamically. Cost calculation uses the coerced variable value, not the source text.

## 7. What does hasNextPage mean?

Under the declared traversal boundary, more eligible rows remain after the returned edge. It is not a promise about future inserts.

**Decisive evidence.** Fetch `first + 1` eligible rows and compare the returned page. `hasNextPage` is true only when another edge exists within the same authorized, filter-bound traversal.

The design remains honest only if: This is keyset traversal, not an offset disguised with base64. New rows above the high-water value do not appear mid-traversal; a new traversal sees them. Deleted rows may shorten a page, which the client handles through hasNextPage rather than assuming a fixed count.

## 8. Why can deletions shorten a page?

Rows may disappear between requests. The client follows pageInfo rather than assuming exactly `first` items.

**Decisive evidence.** Delete an eligible row between pages and continue. The course profile permits a shorter page without manufacturing replacements or claiming snapshot isolation.

The consumer-facing consequence is: A connection contains edges, edge cursors, and PageInfo. The course profile requires first between one and one hundred, stable total ordering, an opaque cursor, and hasNextPage. The cursor binds tenant, normalized filters, current position, and a traversal high-water boundary.

## 9. What makes search more expensive than direct lookup?

It may query several sources, merge rankings, and return polymorphic results. Its cost and fan-out require explicit bounds.

**Decisive evidence.** Compare direct ID lookup with search across projects, runs, and artifacts. Record source fan-out, ranking work, authorization filtering, and cursor population size.

The operational consequence is: The capstone keeps search small and policy-heavy because broad graph search is a common route to uncontrolled fan-out. An organization may instead provide a dedicated search service with its own index authority.

## 10. How should partial search failure appear?

Return available source results only if the policy permits, plus explicit source error and completeness metadata; never silently claim complete ranking.

**Decisive evidence.** Disable one search source while others remain available. The response must retain truthful results and a source-specific error, or reject the whole field according to declared nullability—never silently omit a source.

The strongest engineering interpretation is: Search crosses several types and may cross services. SearchResult is a union, forcing clients to select type-specific fields. The gateway must bound each source query, merge deterministically, disclose partial source failure, and avoid scoring incomparable results as if they were one authoritative ranking.

## 11. Why include __typename for union results?

It lets clients discriminate the actual object type and select the correct fragment safely.

**Decisive evidence.** Execute the search union through a client decoder. `__typename` must select the correct member shape and prevent guessing from overlapping fields.

The defect-oriented view is: A global identifier lets the graph distinguish type and source-local identity. The course encoding carries a versioned type tag and local identifier and is opaque to clients. Decoding occurs only inside the gateway. The decoder rejects malformed, unknown, oversized, and type-mismatched values.

## 12. When should node lookup be omitted?

When global identity is unstable, authorization cannot be applied uniformly, or the generic root would obscure ownership without useful client caching value.

**Decisive evidence.** Reject node lookup when opaque IDs cannot map to one authoritative owner, when existence concealment cannot be preserved, or when it would create unbounded service probing.

Across the Python and TypeScript tracks, the invariant is: Root design affects observability and authorization. A generic entity(type,id) field hides ownership and makes policy review harder. Strongly typed roots remain preferable even when a node interface is offered for client caching.
