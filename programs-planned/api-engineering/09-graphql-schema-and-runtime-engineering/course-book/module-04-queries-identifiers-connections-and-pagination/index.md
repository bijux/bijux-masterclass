# Queries, Identifiers, Connections, and Pagination

**Module 04 of 10**

> **Governing question:** How can clients navigate lists and relationships without unstable pages, leaked internals, or unbounded work?

## Place in the program

Courses 1–8 established the contract, durable implementation, security, operations, performance, asynchronous events, typed RPC, and distributed ownership. Module 04 applies those guarantees to the graph interface; none are reset at the GraphQL boundary.

## Learning outcomes

- design meaningful roots

- encode and validate global identifiers

- implement stable connection pagination

- bind cursors to tenant and filters

- bound polymorphic search

## Capstone result

Implement global IDs and stable, bound connections.

## Root fields represent entry capabilities

A graph should have a small set of meaningful roots rather than a root field for every table. `project`, `analysisRun`, `artifact`, and `deliverySummary` enter through known authorities. `node` dispatches a global identifier to one source, but it does not grant access. `search` is explicit composition and therefore carries a higher cost and stricter cardinality limit.

Root design affects observability and authorization. A generic `entity(type,id)` field hides ownership and makes policy review harder. Strongly typed roots remain preferable even when a node interface is offered for client caching.

## Global identifiers are routing hints, not secrets

The course encodes type and local identity into an opaque string. Clients should not depend on its internal form, but the server may decode it to choose an authority. Obfuscation does not authorize access. Every decoded identifier still passes tenant and field policy.

Type confusion is rejected. An Artifact identifier cannot be supplied where a Project is required and silently coerced. Stable identifiers survive schema field renames; they should not embed mutable display names.

## Connections make pagination explicit

A connection contains edges, edge cursors, and `PageInfo`. The course profile requires `first` between one and one hundred, stable total ordering, an opaque cursor, and `hasNextPage`. The cursor binds tenant, normalized filters, current position, and a traversal high-water boundary.

This is keyset traversal, not an offset disguised with base64. New rows above the high-water value do not appear mid-traversal; a new traversal sees them. Deleted rows may shorten a page, which the client handles through `hasNextPage` rather than assuming a fixed count.

## Filters and sort order are part of cursor identity

A cursor created for `status: RUNNING` cannot be reused for `status: FAILED`. The codec signs a normalized filter hash and tenant identifier. Changing order fields also changes the cursor profile. The server rejects mismatches rather than producing plausible but incorrect pages.

Cursor signatures prevent client tampering; they do not replace authorization or source validation. Expiry may be added when retained snapshots or operational policy require it.

## Search and polymorphic results

Search crosses several types and may cross services. `SearchResult` is a union, forcing clients to select type-specific fields. The gateway must bound each source query, merge deterministically, disclose partial source failure, and avoid scoring incomparable results as if they were one authoritative ranking.

The capstone keeps search small and policy-heavy because broad graph search is a common route to uncontrolled fan-out. An organization may instead provide a dedicated search service with its own index authority.

## Root fields as deliberate entry points

A query root is not a dump of every entity table. Root fields should represent stable ways clients enter the capability graph. The capstone provides `project`, `analysisRun`, `artifact`, `node`, `analysisRuns`, `search`, `deliverySummary`, and `viewer`. Each has a distinct reason:

- singular owner-backed lookups for known identifiers;
- bounded collections for browsing;
- `node` for generic cache reconciliation and refetch;
- `search` for deliberate cross-type discovery;
- `viewer` for client-visible identity and permissions;
- delivery summary as an explicitly stale projection.

Avoid redundant roots that expose the same fact with subtly different authorization or consistency. Every root increases the compatibility surface and can become a separate admission path.

## Global identifiers

A global identifier lets the graph distinguish type and source-local identity. The course encoding carries a versioned type tag and local identifier and is opaque to clients. Decoding occurs only inside the gateway. The decoder rejects malformed, unknown, oversized, and type-mismatched values.

A global ID is not:

- an access token;
- proof that the object exists;
- permission to reveal the object's type;
- a stable database primary key exposed for eternity;
- a substitute for tenant binding.

After decoding, the resolver still performs tenant-aware authorization at the owner. A `NodeLookup` that returns `__typename` for a foreign object can become an existence oracle. The reference policy conceals unauthorized objects consistently.

The `NodeLookup @oneOf` input permits either `id` or `externalId`, not both. External identifiers can have different authority and normalization rules; they must not silently share the global-ID decoder.

## Connections and cursor identity

The course uses a connection profile because pagination is more than returning an array. A connection carries ordered edges and page information. The cursor identifies a continuation position under a specific query identity.

A correct cursor is bound to:

- tenant and authorization population;
- root field or field coordinate;
- normalized filters;
- sort order and tie-breaker;
- page-size policy where required;
- traversal high-water state if the consistency profile uses one;
- expiry and format version.

Changing `status`, tenant, or sort order while reusing a cursor must fail. Otherwise a cursor can cross data populations and leak or skip records. The cursor is opaque because clients should not construct positions or depend on storage layout.

The capstone's run connection orders by a stable tuple rather than a non-unique timestamp alone. A deterministic tie-breaker is mandatory. Offset pagination is easy to expose but becomes expensive and unstable as data changes; the course retains keyset semantics from Course 2.

## Pagination and GraphQL admission

GraphQL creates two page-size boundaries: the schema argument and the runtime policy. A default such as `first: 20` improves ergonomics, but admission must enforce a maximum even when the variable is supplied dynamically. Cost calculation uses the coerced variable value, not the source text.

Nested connections multiply cardinality. A query that requests ten projects, fifty runs per project, and ten artifacts per run has a potential result cardinality of five thousand artifact nodes even before other fields. Cost policy must account for nested multipliers and source fan-out. A simple depth limit would consider this query shallow and miss the risk.

Pagination does not remove authorization requirements. The source query must filter to authorized rows before it selects `first + 1` records and constructs page information. Fetching a broad page and deleting forbidden objects afterward creates sparse pages, timing leaks, and incorrect `hasNextPage` values.

## Search as composition, not a hidden database

`SearchPlatform` returns a union of projects, runs, and artifacts. It is intentionally a graph-owned composition field, but the gateway does not maintain a second authoritative business database. It calls bounded search capabilities or an explicitly governed search projection.

Search requires extra policy:

- supported types and fields;
- tenant-bound indexing;
- staleness and deletion behavior;
- bounded result count;
- stable ranking or cursor semantics;
- authorization-aware indexing and filtering;
- disclosure rules for `__typename`.

A search result cannot bypass source authorization merely because the projection contains a record. The graph may need to validate high-risk results with the owner or constrain the projection to facts safe for the search audience.

## Query design for clients

A good client operation is named, uses variables, asks only for values needed by one screen or workflow step, and has a stable error strategy. Fragments can improve consistency, but excessive global fragments cause over-fetching and make cost review opaque. The persisted-operation registry reviews the expanded operation, not just each fragment in isolation.

Clients should avoid one “universal query” containing every possible field behind directives. Such documents are hard to deprecate, cache, authorize, and budget. Prefer task-specific operations whose identity is meaningful in telemetry.

## Worked pagination scenario

A client requests the first twenty running analyses. The gateway:

1. coerces `first` and rejects values above policy;
2. decodes `after` and verifies tenant, field, filter, sort, and expiry;
3. asks Analysis Control for authorized rows after the stable key;
4. requests at most `first + 1` to determine continuation;
5. encodes the final returned key into a new opaque cursor;
6. records page size and source rows without logging identifiers;
7. returns edges and page information.

If a new run is inserted above the traversal high-water mark, the declared pagination profile determines whether it appears. The course's inherited high-water semantics exclude it until a new traversal, preventing duplicates and unstable movement across pages. The graph documentation must state that model rather than using vague “cursor pagination” language.

## Review checklist

For each root or connection, verify:

- there is a clear client entry task;
- the identifier is opaque, typed, bounded, and tenant-authorized;
- collection order is total and stable;
- cursor identity includes every result-shaping dimension;
- page size is bounded after variable coercion;
- authorization occurs before pagination;
- nested cardinality enters cost admission;
- search projections have explicit freshness and deletion behavior;
- active client operations use the field in a way the release gate can test.

## Worked capstone review

A `ListRuns` cursor signs tenant, normalized filter, position, and traversal high-water. Reusing it under another filter or tenant fails. Rows inserted above the high-water do not appear in the current traversal; a new query starts a new traversal.

## Python and TypeScript implications

Both tracks use base64url global IDs and HMAC-authenticated cursor envelopes. TypeScript requires safe integers; Python validates non-negative positions. Both bind tenant and filter hash.

## Evidence required before the next module

Complete the lab and checkpoint. The decisive artifact is the module report under `reports/module-04-*.json`; prose claims without its oracle do not pass.
