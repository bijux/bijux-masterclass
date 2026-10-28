# Worked answers — Queries, Identifiers, Connections, and Pagination

Compare the decision rule and evidence, not just wording.

## 1. Why is a global ID not an authorization token?

It only identifies type and local identity. Possession does not prove tenant membership or field permission.

**Decisive evidence.** Decode a valid ID, then use it under a principal from another tenant. The source lookup must conceal the resource, proving identity decoding does not grant access.

## 2. What makes an ordering stable for cursor pagination?

It is total and deterministic, usually a business sort key plus a unique tie-breaker. The source applies the same order on every page.

**Decisive evidence.** Insert rows sharing the primary sort value and traverse multiple pages. The unique tiebreaker must prevent duplicates, skipped rows, and non-deterministic order.

## 3. Why bind a cursor to filters?

Reusing a position under different filters can skip or duplicate rows and reveal cross-query state. A filter hash makes misuse fail.

**Decisive evidence.** Reuse a cursor with a changed status or project filter. Signature validation may pass, but query binding must reject the continuation before source pagination.

## 4. Why include a high-water boundary?

It prevents newly inserted earlier rows from shifting the current traversal, giving a defined snapshot-like window.

**Decisive evidence.** Insert a newer row after page one. It must be absent from the existing traversal and present in a fresh traversal, demonstrating the declared high-water semantics.

## 5. Is base64 an opaque cursor security control?

No. Base64 is reversible. The course cursor is authenticated with HMAC and still requires authorization.

**Decisive evidence.** Tamper with one byte of a base64 cursor. A raw base64 offset may decode, while the HMAC-authenticated profile must reject modified state.

## 6. Why require `first` even with a default?

The schema and admission policy need an enforced maximum. Defaults help clients; they do not permit unbounded retrieval.

**Decisive evidence.** Coerce omitted, zero, negative, maximum, and over-maximum `first` values. Defaults may improve ergonomics, but every execution still needs an enforced cardinality bound.

## 7. What does hasNextPage mean?

Under the declared traversal boundary, more eligible rows remain after the returned edge. It is not a promise about future inserts.

**Decisive evidence.** Fetch `first + 1` eligible rows and compare the returned page. `hasNextPage` is true only when another edge exists within the same authorized, filter-bound traversal.

## 8. Why can deletions shorten a page?

Rows may disappear between requests. The client follows pageInfo rather than assuming exactly `first` items.

**Decisive evidence.** Delete an eligible row between pages and continue. The course profile permits a shorter page without manufacturing replacements or claiming snapshot isolation.

## 9. What makes search more expensive than direct lookup?

It may query several sources, merge rankings, and return polymorphic results. Its cost and fan-out require explicit bounds.

**Decisive evidence.** Compare direct ID lookup with search across projects, runs, and artifacts. Record source fan-out, ranking work, authorization filtering, and cursor population size.

## 10. How should partial search failure appear?

Return available source results only if the policy permits, plus explicit source error and completeness metadata; never silently claim complete ranking.

**Decisive evidence.** Disable one search source while others remain available. The response must retain truthful results and a source-specific error, or reject the whole field according to declared nullability—never silently omit a source.

## 11. Why include __typename for union results?

It lets clients discriminate the actual object type and select the correct fragment safely.

**Decisive evidence.** Execute the search union through a client decoder. `__typename` must select the correct member shape and prevent guessing from overlapping fields.

## 12. When should node lookup be omitted?

When global identity is unstable, authorization cannot be applied uniformly, or the generic root would obscure ownership without useful client caching value.

**Decisive evidence.** Reject node lookup when opaque IDs cannot map to one authoritative owner, when existence concealment cannot be preserved, or when it would create unbounded service probing.
