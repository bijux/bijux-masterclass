---
module_id: API-014
program: API & Service Engineering
level: 1
module_number: 14
title: Collections and Individual Resources
status: complete
last_verified: 2026-09-01
---

# Collections and Individual Resources

## One-Page Review

### Governing question

How should an API model a collection, its individual member resources, and their relationship without conflating membership, identity, representation, and storage?

### Essential definitions

- A **collection resource** is an identified concept whose state includes a membership relation and often collection-level metadata or controls.
- A **member resource** has its own identity; it is not merely an array position or embedded copy.
- **membership** is the relation between a collection and a member at a stated time and visibility context.
- A **collection representation** communicates some view of collection state, often links or summaries rather than complete member state.
- A **projection** includes selected member attributes; an **embedded representation** includes a bounded representation of a related resource.
- A **relationship resource** identifies membership itself when role, validity, order, or lifecycle deserves independent interaction.
- A **snapshot** fixes membership or ordering under a declared model; an ordinary collection is usually time-varying.

### Central model, mechanism, or theorem

Let $C$ be a collection and $M_C(t,p)$ the set or ordered sequence of member identifiers visible at time $t$ to principal $p$. A collection response is representation $V(C,t,p)$ of that state, not the collection itself and not proof that every member remains accessible later. Member identity function $I(m)$ remains independent of position, page, or current membership.

### Critical invariants

Membership and member existence are distinct. Individual identity never depends on array position. Collection authorization is applied to membership and projected fields, while member authorization is evaluated independently. Embedded state declares freshness and authority. Collection-level validators describe the represented view, not automatically every member. Mutations state atomicity, ordering, duplication, and cascade rules.

### Common failures

Treating a collection as a raw table dump; using array index as member identity; returning unbounded full member objects; assuming removal deletes the member; exposing hidden members through counts; applying one collection permission to every member action; silently mixing stale summaries with current links; making list order accidental; and treating empty, hidden, and nonexistent collections as the same state.

### Compact example

`/teams/7/members` can identify the time-varying membership of team 7. Each entry links to a person and may summarize display name. Removing person 42 from the collection ends membership but does not delete `/people/42`. If role and validity need independent audit and conditional change, identify the membership relation itself.

### Connections

Resource Identification and URI Design establish meaning and references. The next modules define CRUD, partial update, filtering, sorting, pagination, long-running, and batch semantics. Web Linking supplies typed relationships; authorization and caching constrain safe representations.

## Governing Question

What does a collection resource mean, how does it relate to independently identified members, and which guarantees can a client infer from one collection representation?

## Why This Matters

Collections are among the most common API surfaces and among the easiest to underspecify. A JSON array can hide membership rules, visibility, ordering, freshness, continuation, partial results, and side effects. Database queries make it tempting to expose rows directly, but an API collection is a domain and authorization boundary, not a result-set accident.

RFC 9110 provides the generic resource and representation model but does not prescribe application collection semantics. RFC 8288 defines a link as a typed connection among a context, relation, and target; this supports member discovery without copying complete member state. Fielding's resource model permits collections as time-varying concepts. The application must still define membership, ordering, lifecycle, and authority.

This chapter focuses on the collection/member boundary. Detailed creation and deletion semantics belong to API-015, partial mutation to API-016, and filtering, ordering, and pagination mechanisms to API-017.

## Prerequisites and Retrieval

Retrieve resource identity, URI ownership, representations, links, HTTP methods, validators, caching, authorization, concurrency, and time-varying state. Recall that a response is evidence about selected state at a time; it does not freeze future membership unless the contract supplies a snapshot.

## Learning Objectives

By the end of this module, you should be able to:

1. distinguish a collection resource from its representation and storage query;
2. model membership separately from member existence and identity;
3. choose links, summaries, projections, or embedding deliberately;
4. define collection-level authorization without leaking hidden members;
5. model relationship resources when membership has independent state;
6. state ordering, duplication, snapshot, and mutation boundaries; and
7. diagnose stale embedding, inconsistent reads, cascade ambiguity, and oversized responses.

## Core Exposition

### A collection is an identified domain concept

A collection resource answers “which members belong under this collection's declared rule?” The rule may be all orders visible to a buyer, devices assigned to a site, revisions of a policy, or active memberships in a team. The collection can have metadata such as title, owner, count policy, update time, or links to supported operations.

The collection is not the response array. At time $t_1$ it might contain identifiers `{A,B}` and at $t_2$ `{B,C}` while remaining the same resource. A response may include only summaries or one bounded window. A database table can contain rows not visible in the collection, and one row can appear in several collections under different relationships.

Define the membership predicate in domain language. “Rows where `deleted_at IS NULL`” leaks storage. “Orders the principal may currently administer” states consumer meaning, though it still requires authorization, time, and consistency rules.

### Keep member identity independent

Each individual resource has a stable identifier independent of its position in a collection representation. Index `3` cannot identify a member because insertion, filtering, sorting, and visibility change positions. If entries have no independent identity or interaction, they may be values rather than member resources.

Membership does not imply ownership, containment, or deletion cascade. A book can belong to several reading lists. Removing it from one list changes a relation, not the book. Conversely, an order line may be lifecycle-bound to an order aggregate even though it is addressable within that boundary. State the relationship instead of inferring it from path nesting.

Member existence does not guarantee membership. A suspended account can still exist but leave the “active accounts” collection. Membership also does not guarantee current dereference access: permissions can change between list and member requests.

### Model membership as a relation

Let membership relation $E_C(t,p,m)$ mean member $m$ is visible in collection $C$ at time $t$ to principal $p$. Principal appears in the model because authorization can affect observable membership. If the business collection is principal-independent, separate its authoritative relation from the authorized view rather than pretending policy changes domain truth.

When the relation carries role, sequence, source, validity interval, approval, or state, it can deserve its own identity. A team membership is not merely a pointer from team to person if clients must suspend it, audit who approved it, or distinguish two historical membership periods.

Do not automatically expose relation internals inside the member resource. A person's team role belongs to a particular membership context; embedding it globally on the person produces contradictions when the person joins multiple teams.

### Choose representation depth deliberately

At one extreme, return only member links. This minimizes duplication and lets clients retrieve authoritative member representations, but increases round trips. At the other, embed full member representations. This reduces immediate requests but increases payload, authorization, staleness, and compatibility coupling.

A summary projection is often appropriate: stable member identifier, display label, relationship attributes, and the fields needed to choose the next interaction. Define whether these values are authoritative snapshots, cacheable summaries, or hints. A client must not use a stale embedded balance to authorize a payment when the individual account resource owns current balance.

Avoid universal `include=everything`. Bounded expansion needs allowed relationships, depth, item limits, authorization at every edge, cycle detection, cost limits, and predictable errors. Otherwise one request becomes an unbounded graph traversal.

### Use typed links for relationships

RFC 8288 models links with context, relation type, target, and optional target attributes. A collection representation can link each member and links such as `next`, `prev`, `canonical`, or application-defined relations where their semantics are registered or documented.

Link relation type describes why target relates to context; media type describes representation format. Do not invent relation names whose meaning depends on array position or undocumented client convention. Links can appear in representation content or the HTTP `Link` field, with different base-resolution rules that the chosen serialization must respect.

Links are controls or relationship statements, not proof of authorization or existence at click time. Clients handle target disappearance, permission change, and redirect according to the surrounding contract.

### Define visibility without side channels

Collection authorization includes whether the collection exists for a caller, which members are visible, which fields are projected, and whether aggregate metadata can reveal hidden members. Returning `total=100` with only two visible entries discloses 98 hidden memberships unless that disclosure is intentional.

Counts, facets, empty results, ordering gaps, identifiers, and timing can all leak protected data. Apply authorization before aggregation or define privacy-preserving aggregates. Do not fetch all rows, calculate totals, and remove forbidden entries only at serialization time if intermediate logs or metrics expose them.

An empty visible collection can mean no authoritative members or no visible members. Error and metadata policy decides whether callers can distinguish them. The same policy must hold across list, individual lookup, search, count, and event surfaces.

### State ordering and duplicate semantics

Sets have no intrinsic order; sequences do. If order matters, define the ordering keys, direction, tie-breaker, null handling, and mutation behavior. Database return order without an explicit contract is not stable. API-017 develops sorting and pagination; here the design decision is whether the collection's identity includes an order at all.

Decide whether one member can appear more than once. A playlist may intentionally contain the same track in several positions, meaning entries need their own identities. A set of account owners probably prohibits duplicate membership. Deduplicating silently can destroy relationship occurrences or mask corrupt data.

Ordered relationship entries often deserve identity distinct from the target member: playlist entry 81 can point to track 9 while carrying position and insertion metadata. Reordering entries changes the collection relation, not track identity.

### Bound consistency claims

A collection representation and individual representation can be observed at different times. List entry says `status=open`; by the subsequent GET, member is closed. This is normal under a live view unless the API promises a snapshot, validator relationship, or transaction boundary.

A collection validator describes the selected collection representation under its variation dimensions. It does not automatically validate each member's independently retrieved representation. Embedding full member state may require the collection validator to change when any embedded field changes, causing broad invalidation.

If clients need a reproducible export, identify a snapshot or report resource with creation time, membership basis, retention, and completeness evidence. Do not label a paginated live traversal a snapshot merely because every page request succeeded.

### Make collection mutation semantics explicit

Collection mutation can mean creating a new member, adding an existing member, removing membership, deleting a member, replacing the membership set, or changing relationship attributes. These are different domain operations and failure modes. The next modules choose methods and representations; this module fixes the conceptual distinction.

Define atomicity. Replacing memberships with `{A,B,C}` can be all-or-nothing, partially applied, or asynchronous. Define duplicate handling, missing members, authorization per member, invariant checks, and response after concurrent modification. Avoid treating a batch of unrelated member operations as one atomic collection write without implementation evidence.

Cascade behavior is policy, never an implication of nesting. Deleting a team might retain people, terminate membership resources, archive audit evidence, and schedule document ownership transfer. State each lifecycle consequence.

### Control scale and cost

Every collection needs a bounded representation policy. “Return all” fails eventually, even if current fixtures are small. Large embeddings increase serialization time, memory, transfer, client parsing, cache churn, and blast radius of one malformed member.

Size boundaries must not silently truncate while claiming completeness. Use explicit continuation, partial-result metadata, or a separate export operation as developed later. Enforce query complexity, expansion depth, per-page limits, deadlines, and cancellation across gateways and dependencies.

Observe route templates and bounded filter categories, not raw member identifiers in metric labels. Record result count, scanned/returned ratio, authorization filtering, continuation failures, and representation size without leaking protected membership.

## Definitions and Notation

Let $C$ be a collection, $P$ principals, $R$ member resources, and $T$ time. Membership view $M_C:T\times P\to\mathcal{P}(R)$ returns the visible member set. For ordered collections use sequence $S_C(t,p)$ whose entries may have identities distinct from target members. Representation function $V(C,t,p,o)$ also depends on options $o$ such as projection or bounded expansion.

A **membership predicate** decides inclusion under stated domain and visibility rules. A **member link** identifies a related resource. An **entry** is one occurrence in a collection representation or ordered relationship and may be a value, member summary, or relationship resource. **Completeness** states whether the representation covers the declared scope. **Cardinality** is member or occurrence count under the model, not necessarily a safe field to disclose.

## Mechanisms, Invariants, or Proof Structure

Review a collection in this order:

1. Define the collection resource and authoritative membership rule.
2. Separate member identity, existence, membership, ownership, and containment.
3. Decide whether membership carries independently identified relationship state.
4. Define links, summary fields, embedding depth, and field authority.
5. Apply collection, membership, member, field, and aggregate authorization.
6. State set versus sequence behavior, duplicates, ordering, and entry identity.
7. Bound snapshot, freshness, validator, and completeness claims.
8. Define add, remove, replace, delete, and cascade as separate conceptual effects.
9. Bound representation size, traversal cost, and telemetry cardinality.
10. Test concurrency, hidden members, stale embedding, partial failure, and lifecycle changes.

The **identity invariant** forbids position-based member identity. The **membership invariant** separates relation changes from member lifecycle. The **authority invariant** labels projected and embedded field ownership. The **visibility invariant** applies policy before disclosure and aggregation. The **boundedness invariant** prevents a collection contract from requiring an unbounded response.

## Alternatives and Trade-Offs

**Links versus embedding.** Links preserve member authority and small collection responses but cost round trips. Embedding improves locality but couples schemas, invalidation, authorization, and freshness. Bounded summaries plus links often provide a durable middle ground.

**Implicit versus identified membership.** An implicit relation is simple when membership has no attributes or lifecycle. A relationship resource supports role, validity, ordering, conditional change, and audit at the cost of more identifiers and operations.

**Live view versus snapshot.** Live collections reflect current state and are cheap to maintain but can shift during traversal. Snapshots support reproducibility but require creation, storage, expiration, access control, and correction policy.

**One global collection versus actor-specific collections.** A global collection with filtering can centralize semantics but creates disclosure and scale risk. Actor-scoped collections provide clearer authorization and bounded outcomes but may duplicate views. Choose based on meaning and trust boundaries.

## Failure Modes and Misconceptions

A collection is not a database table or array. A member link does not guarantee future access. Removing membership need not delete the member. Nested paths do not define cascade. Embedded state is not automatically authoritative or current. Collection ETags do not validate separately retrieved members. A `total` can leak hidden resources. Stable ordering requires an explicit total order, not storage coincidence. Empty, inaccessible, gone, and temporarily unavailable are distinct states even when policy hides distinctions.

## Worked Examples

### Example 1

A team representation lists person 42. Removing that entry ends one membership, while `/people/42` remains because the person belongs to other teams. **Conclusion:** membership lifecycle and member lifecycle are distinct.

### Example 2

A UI uses array index 3 as an edit target. Another member is inserted before the request arrives, so the edit reaches a different person. Stable member links fix the race. **Conclusion:** representation position is never member identity.

### Example 3

A collection embeds account balances captured at 10:00. A payment screen reads one at 10:05 after another transaction. The summary is labeled `observed_at` and clients retrieve authoritative current balance before payment. **Conclusion:** embedded fields need freshness and authority contracts.

### Example 4

A caller may see two of 100 incident records. Returning `total=100` exposes hidden incident volume. The API reports visible count only and documents its scope. **Conclusion:** aggregate metadata participates in authorization.

### Example 5

A playlist contains track 9 twice at different positions. Treating member target as a set deduplicates one occurrence. Modeling playlist entries with their own IDs preserves order and per-occurrence notes. **Conclusion:** ordered occurrence identity can differ from member identity.

### Example 6

A team membership stores role, approving administrator, and validity interval. Updating `person.team_role` fails when the person joins two teams. An identified membership relation scopes the state correctly. **Conclusion:** contextual relationship data belongs to the relation.

### Example 7

A collection response has validator `"c17"`; member 8 changes an unembedded private field. If the collection projection is unchanged, `"c17"` can remain valid. A separately fetched member needs its own validator. **Conclusion:** validators cover selected representations, not an assumed object graph.

### Example 8

A live collection is traversed while new orders arrive. Every request succeeds, yet the client sees a duplicate and misses one order under offset traversal. A reproducible audit instead requests an identified snapshot with declared membership time. **Conclusion:** successful pages do not prove snapshot completeness.

### Example 9

Deleting a project path is assumed to delete nested documents. Domain policy actually requires document retention and ownership transfer. The API separates project deletion, membership termination, and document reassignment. **Conclusion:** URI hierarchy does not supply cascade policy.

### Example 10

`include=members.manager.organization` expands a team into millions of nodes and cycles back through memberships. The API allows named bounded expansions, enforces depth and item budgets, and returns links beyond the bound. **Conclusion:** graph embedding requires explicit cost and cycle controls.

## Cross-Program Connections

[Resource Identification](012-resource-identification.md) establishes member and relationship identity; [URI Design](013-uri-design.md) supplies stable links. API-015 and API-016 define lifecycle and mutation methods, while API-017 defines filtering, sorting, and pagination. Security Engineering owns membership disclosure; databases own query and snapshot mechanisms but not public semantics; distributed systems owns cross-resource consistency limits.

## References

1. R. Fielding, M. Nottingham, and J. Reschke, *RFC 9110: HTTP Semantics*, Internet Standard 97, June 2022, Sections 3 and 9. Checked 2026-09-01. https://www.rfc-editor.org/rfc/rfc9110.html
2. M. Nottingham, *RFC 8288: Web Linking*, Standards Track, October 2017, Sections 2–3. Checked 2026-09-01. https://www.rfc-editor.org/rfc/rfc8288.html
3. R. T. Fielding, *Architectural Styles and the Design of Network-based Software Architectures*, doctoral dissertation, University of California, Irvine, 2000, Sections 5.2.1.1–5.2.1.2. Checked 2026-09-01. https://ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm

## Exercises

### Exercise 1

Distinguish collection resource, collection representation, member resource, membership relation, and embedded member summary for a university course roster.

### Exercise 2

Model a playlist that permits the same track several times, supports reorder, and stores a note on each occurrence. Identify which concepts need independent identity and why.

### Exercise 3

Diagnose an incident collection that returns 20 visible entries, `total=800`, and full embedded reporter profiles to a contractor who may see only assigned incidents.

### Exercise 4

Compare link-only, summary-plus-link, and full embedding for an order collection used by mobile clients. Evaluate round trips, payload, freshness, authorization, caching, schema coupling, and offline use.

### Exercise 5

A scientific archive must export a reproducible collection of datasets while ingestion and access revocation continue. Design collection/member identity, snapshot, authorization, completeness, retention, and correction semantics.

## Answers to the Exercises

### Answer 1

The course roster is the continuing collection resource. A response containing current visible students is one representation. Each student is an independently identified member resource. Enrollment is the membership relation and may itself need identity when it carries status, dates, grading mode, or audit history. An embedded name and program are summaries whose authority and observation time must be stated; they are not the complete student resource.

### Answer 2

Identify the playlist collection, every track resource, and every playlist-entry occurrence. Two entries can target the same track while having different stable entry IDs, positions, notes, and insertion history. Reordering changes entry order or position state without changing track identity. Removing one entry leaves the other occurrence and the track intact. Using track ID as the entry key would make duplicates impossible and notes ambiguous.

### Answer 3

`total=800` leaks the existence and volume of 780 hidden incidents. Full reporter profiles can disclose fields beyond the contractor's incident role, and fetching then filtering risks logs or timing leaks. Apply membership authorization before aggregation; report a clearly scoped visible count or omit it; project only authorized reporter summary fields; link to independently authorized profiles; bound embedding; and make unknown, forbidden, and empty behavior consistent with individual lookup and search.

### Answer 4

Link-only minimizes payload and duplication and keeps member reads authoritative, but performs poorly under high-latency mobile networks and offline use. Full embedding reduces round trips but increases payload, invalidation, privacy risk, and coupling to member schema. Summary-plus-link usually offers the needed order ID, state, amount, and next controls with bounded payload, while links support detail retrieval. Record `observed_at` or validators, apply field authorization, cache the collection by its actual variation dimensions, and offer an explicitly versioned offline snapshot if offline completeness is required.

### Answer 5

Keep stable dataset member identities independent of the export. Create an identified snapshot resource recording the membership rule, cutoff or transaction marker, requesting principal, authorization policy, ordered member identifiers, checksum/evidence, creation time, terminal status, and retention. Revocation policy must say whether later access removes download permission, redacts a corrected snapshot, or preserves regulated evidence for restricted auditors. Corrections create a new version or signed amendment rather than silently changing the claimed snapshot. Completeness is bounded to the stated ingestion cutoff and fault model, and export expiration does not reassign its identifier.
