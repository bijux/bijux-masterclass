---
module_id: DBE-096
program: Database Engineering
level: 2
module_number: 96
title: Graph Databases
status: complete
last_verified: 2026-09-05
---

# Graph Databases

## One-Page Review

### Governing question

When relationships are first-class data, how should a database represent, constrain, traverse, update, partition, authorize, and recover graphs without confusing convenient adjacency with bounded or correct query execution?

### Essential definitions

- A **graph** $G=(V,E)$ has vertices $V$ and edges $E$; direction, labels, properties, multiplicity, self-loops, and identity belong to the declared model.
- A **property graph** associates labels and key-value properties with vertices and edges.
- An **RDF graph** is a set of subject-predicate-object triples with standardized term semantics; it is not interchangeable with a property graph.
- **Adjacency** is the set of incident or outgoing/incoming edges for a vertex under a direction and edge-type filter.
- A **path** is a sequence of adjacent edges; a **simple path** repeats no vertex, while a **walk** may repeat vertices.
- **Degree** is incident-edge count under a chosen direction/type. A very high-degree vertex is a **supernode**.
- **Pattern matching** finds graph bindings satisfying node, edge, property, and path predicates.
- A **graph constraint** restricts identities, labels/types, properties, endpoints, cardinalities, or shapes.
- A **graph partition** assigns vertices/edges to ownership units; a **cut edge** crosses units.
- **Index-free adjacency** is an implementation claim that traversal can follow stored adjacency without a global lookup at each hop; it does not mean no indexes or constant-time arbitrary queries.

### Central model, mechanism, or theorem

Model the domain before choosing syntax. For a directed labeled property multigraph, an edge can be $(e,u,r,v,p)$: stable edge identity $e$, source $u$, relationship type $r$, destination $v$, and properties $p$. Multiple parallel edges and self-loops are either valid or prohibited by explicit constraints.

A traversal from start set $S$ expands only relationships permitted by direction, type, authorization, and version. A visited set prevents repeated expansion when semantics seek reachability or shortest unweighted distance. Without pruning, branching factor $b$ to depth $d$ can examine approximately $1+b+\cdots+b^d$, so locality alone does not make variable-length paths cheap.

### Critical invariants

- every vertex and edge has stable identity and exactly the permitted endpoint/type structure;
- uniqueness and endpoint/cardinality constraints are enforced within their declared scope;
- snapshot traversal never combines edges/vertices from incompatible committed versions unless the query contract permits it;
- path semantics state direction, relationship types, repetition, length bounds, and result uniqueness;
- indexes return a superset of valid candidates and are reconciled transactionally or by an explicit repair protocol;
- partition movement preserves adjacency, routing epochs, and updates across cut edges;
- authorization applies to start nodes, traversed edges, intermediate nodes, returned paths, and side-channel behavior;
- backup/restore preserves graph identities, properties, schema/constraints, adjacency, index rebuild rules, and replay position coherently.

### Common failures

- selecting a graph database because records contain foreign keys but queries do not traverse relationships;
- conflating RDF, property graph, and a product's query language;
- leaving edge identity and parallel-edge semantics implicit;
- running unbounded variable-length traversal over cycles or supernodes;
- treating “index-free adjacency” as proof of constant-time or distributed-local queries;
- partitioning by vertex hash while dominant paths cross communities;
- authorizing only returned vertices while traversal leaks forbidden relationships;
- storing derived similarity or recommendation edges without provenance and expiry;
- updating inverse/materialized edges without atomicity or reconciliation;
- benchmarking toy regular graphs rather than production degree, labels, skew, and mutations.

### Compact example

If every vertex has average effective branching 20, an unpruned depth-four walk can expose up to $1+20+400+8{,}000+160{,}000=168{,}421$ vertex visits before duplicates. A selective edge type reducing effective branching to 2 changes that idealized upper shape to 31. Depth limits, visited semantics, predicates, degree caps, budgets, and cancellation are correctness and availability controls, not cosmetic tuning.

### Connections

The previous module, [Time-Series Databases](095-time-series-databases.md), centers ordered temporal ranges; graph databases center relationship patterns and paths. The roadmap's next module, [Search Engines and Inverted Indexes](../ROADMAP.md), centers term-to-document retrieval. Prerequisites include [Recursive Queries](017-recursive-queries.md), [Full-Text and Inverted Indexes](038-full-text-and-inverted-indexes.md), [Serializable Snapshot Isolation](049-serializable-snapshot-isolation.md), and [Sharding and Data Placement](086-sharding-and-data-placement.md).

## Governing Question

A fraud investigator asks how accounts, devices, merchants, addresses, and transfers connect within three steps. An authorization service asks whether a subject reaches a permission through nested groups. A network operator asks for impacted dependencies. A recommendation service asks for ranked neighbors. These are relationship-shaped questions, but their semantics differ radically.

When does a graph model clarify identity and traversal, and how can an implementation bound path search, preserve transactional graph constraints, partition irregular topology, and recover without dangling or duplicated relationships? The answer must distinguish logical graph, query semantics, physical adjacency, analytical algorithm, and distributed protocol.

## Why This Matters

Graphs make relationships explicit rather than reconstructing every traversal through repeated joins or application round trips. Local adjacency can serve bounded neighborhood queries efficiently. Pattern languages can express variable relationships, alternation, and paths directly. This improves model clarity for domains where connections are central.

Graphs also amplify combinatorial and operational risks. One celebrity, root group, or shared device becomes a supernode. A short-looking variable path can enumerate exponentially many walks. A graph cut can turn each hop into network work. Concurrent updates can violate acyclicity or cardinality despite individually valid edges. Authorization can leak through counts, timing, or intermediate paths.

A graph database is not automatically the right home for all graph computation. Batch algorithms, vector search, relational recursive queries, search indexes, or specialized graph-processing systems may own different workloads. Choose from operations and guarantees.

## Prerequisites and Retrieval

Retrieve sets, relations, directed and undirected graphs, paths, cycles, trees, breadth-first and depth-first search, shortest path, connected components, indexes, joins, recursion, transactions, replication, sharding, and complexity. Be able to explain why output size lower-bounds runtime and why average degree hides skew.

Retrieve modeling distinctions: a person entity is not the same as a name; an edge type is not the same as an event; absence of an edge may mean false, unknown, expired, or unauthorized. Decide whether relationships are current facts, historical events, assertions with provenance, or derived scores.

For an engine, record version and graph model; query-language version; identity/constraint schema; path repetition and uniqueness; transaction/isolation; indexes; adjacency representation; partition/routing; replication; procedures/algorithms; memory/spill; timeouts; security; backup/restore; and limits. Current feature claims require official documentation.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish property-graph, RDF, and graph-processing models and choose one from semantics;
2. define vertex/edge identity, direction, multiplicity, labels, properties, and constraints;
3. state path repetition, direction, type, length, snapshot, and result semantics precisely;
4. estimate traversal expansion and diagnose supernodes, cycles, Cartesian patterns, and memory growth;
5. design transactional graph mutations and repairable derived/inverse relationships;
6. reason about graph partition cuts, distributed traversal, movement, and skew;
7. apply authorization and privacy policy to traversal and derived graph state;
8. benchmark and recover graphs with topology-shaped, semantic evidence.

## Core Exposition

**Choose a graph model deliberately.** A directed property graph commonly represents vertices and edges with labels and properties. Edge identity allows parallel relationships such as two purchases or multiple employment periods. Some products use edge tuples without independent identity or limit property types. State the exact model.

RDF represents triples whose subjects, predicates, and objects use IRIs, blank nodes, or literals under W3C semantics. Named graphs, entailment regimes, RDF-star-like extensions, and validation add further distinctions. SPARQL pattern matching is not merely alternate Cypher spelling. Convert only with documented loss and identity rules.

Graph-processing frameworks such as Pregel execute vertex-centric iterative computation over a graph. They can compute ranks or components at scale but need not provide low-latency transactional updates or interactive pattern matching. “Graph system” names a family, not one contract.

**Define vertex identity.** A vertex identifier must be stable across mutable properties, import, replication, and repartitioning. External natural keys can map to internal IDs under uniqueness constraints. If two data sources refer to the same person, entity resolution is a probabilistic/governed process, not a database merge-by-name.

Identity scope may be tenant-local or global. Namespace every external key and record provenance. Merging vertices redirects edges and can change reachability, authorization, and historical results; treat it as a reviewed migration with reversible evidence.

**Define edge identity and meaning.** An edge `OWES` might be a current balance relation, one obligation event, or a derived summary. Direction matters. Parallel edges may be meaningful events or prohibited duplicates. A self-loop may be valid in network topology and invalid in organizational management.

For edge identity, use a stable event/relationship ID or a uniqueness key such as `(source,type,destination,valid_from)` when domain semantics prove it. Do not assume `(source,type,destination)` is unique if multiple contracts or time intervals can coexist.

**Model time and provenance.** A property `since=2020` does not define whether an edge is valid now, asserted then, observed then, or loaded then. Use valid-time intervals, transaction versions, source/provenance, confidence, and correction lineage where needed. A current graph may be a projection from immutable relationship events.

Derived edges such as `SIMILAR_TO(score=.82)` need algorithm/model version, input frontier, generated time, expiry, and reproducibility. They should not silently become authoritative facts.

**Constrain graph shape.** Common constraints include unique IDs, required labels, property type/range, permitted edge endpoint labels, maximum cardinality, no self-loop, and acyclicity. Products may enforce only a subset declaratively. Application checks outside a transaction race.

Suppose each employee has at most one active manager. Two concurrent transactions can each observe none and add different `REPORTS_TO` edges. A unique ownership record or serializable predicate constraint is needed. A local uniqueness index on edge IDs does not preserve the cardinality invariant.

Acyclicity is global or scope-wide: adding edge $u\to v$ is safe only if no path $v\leadsto u$ exists in the relevant snapshot and no concurrent transaction creates one. Serializable validation, serialized ownership, hierarchy-specific encoding, or a compensating detection workflow may be required.

**Understand adjacency storage.** An engine may store outgoing/incoming adjacency lists beside vertex records, relationship records linked in both directions, or index entries keyed by endpoint/type. Following one stored link can avoid a global index lookup, but still costs cache, page, decode, predicate, MVCC, security, and perhaps network work.

Maintaining both outgoing and incoming adjacency duplicates references. Updates must atomically change both or have a repairable source authority. A half-edge after crash can omit traversal in one direction. Checksums and consistency scans need stable edge identity.

**Use indexes to find starts.** Adjacency helps after a start vertex is known. Property indexes, full-text indexes, vector indexes, or external mappings find candidate starts. A pattern beginning with every `Person` whose unindexed property matches may scan all persons before one hop.

Composite and partial index semantics still apply. Indexes must respect labels/types, null/missing, collation, snapshot, and authorization. An index-free-adjacency claim does not remove starting-point indexes.

**Specify pattern matching.** A pattern consists of variables, vertex/edge labels or types, property predicates, direction, and joins where variables repeat. Distinguish existence from enumeration. Asking “does any path exist?” can stop early; returning all paths can have enormous output even over a small graph.

Repeated variables enforce identity equality. Independent pattern parts can create a Cartesian product. Optional matching has null/missing semantics. Aggregation after expansion may allocate all bindings unless the planner can transform it safely.

**Define path repetition.** A walk may repeat edges and vertices; a trail repeats no edge; a simple path repeats no vertex. Query languages and procedures choose different defaults. On a cycle, an unbounded walk has infinitely many lengths. Always state minimum/maximum length, allowed relationship types/directions, repetition, path uniqueness, and whether results are endpoints or full paths.

For effective branching $b>1$ and depth $d$, the tree-like expansion sum is $(b^{d+1}-1)/(b-1)$. Real graphs merge paths, but path enumeration can still be exponential because distinct paths may share vertices. A visited set bounds reachability BFS by vertices/edges examined, but it changes all-path semantics.

**Choose the algorithm for the question.** BFS gives shortest unweighted hop distance when edges have equal cost and the queue/visited rules are correct. Dijkstra handles nonnegative weights. Negative weights require another algorithm; negative cycles can make minimum cost undefined. Bidirectional search can reduce work when source and target are known and reverse adjacency exists.

Ranking, community, centrality, and similarity algorithms carry assumptions about direction, weights, normalization, convergence, and graph snapshot. Do not treat a library procedure as a query-language guarantee. Record algorithm and version, parameters, input snapshot, nondeterminism, and validation.

**Bound supernodes.** Vertex degree distributions are often heavy-tailed. Expanding a global root, popular item, or shared IP can dominate memory and latency. Record degree by type/direction and percentiles/max, not mean only. Apply edge-type/time predicates before expansion when semantics permit, cap results, paginate by stable edge key, and isolate high-degree representations.

Degree caps can change correctness. A fraud query cannot silently sample neighbors and claim exhaustive absence. Return truncated/incomplete status, use offline processing, or redesign the question.

**Preserve snapshot semantics.** A multi-hop traversal may run while vertices and edges change. Without a transaction snapshot it can observe a path whose edges never coexisted, miss a newly linked component, or follow an edge to a deleted vertex. State isolation and whether long traversals pin history.

Serializable graph updates are expensive when predicates cover reachability or cardinality. MVCC snapshot alone prevents dirty reads but may allow write skew. Use exact constraints and transaction evidence from the chosen engine.

**Make mutation workflows idempotent.** A request to create vertex, edge, and derived inverse relation needs stable mutation ID. Under an atomic transaction, commit all authoritative pieces or none. Across external projections, publish a durable change and apply idempotently with source version, then reconcile.

Deleting a vertex must define incident-edge behavior: reject, cascade, tombstone, detach, or preserve historical edges. A cascade over a supernode is a large transaction and failure hazard. Mark-delete plus bounded asynchronous cleanup can be safer if reads honor the marker and the cleanup is resumable.

**Partition for traversals, not only balance.** Hashing vertices balances count but cuts community edges, turning hops into network messages. Community-aware partitioning reduces cuts but can skew sizes and changes as topology evolves. Replicating boundary vertices reduces remote reads at consistency/storage cost.

Define edge ownership: source partition, destination partition, separate edge partition, or replicas. Cross-partition updates need atomicity or repair. A distributed traversal must carry snapshot/version, deduplicate, budget messages, handle partial shard failure, and avoid retry storms.

Let $E_c$ be cut edges and $E$ total relevant edges; cut ratio $|E_c|/|E|$ is one locality measure, but weights by traversal frequency and direction are more useful. A low global cut can still place the hottest path across regions.

**Move graph ownership safely.** Repartitioning copies vertices and adjacency while mutations continue, catches up changes, switches a routing epoch, and fences old owners. Incoming indexes or replicated half-edges must move coherently. Validate edge counts by identity, endpoint existence, direction, properties, versions, and sampled reachability before cleanup.

**Treat query planning as join planning plus traversal.** Planners choose start candidates, pattern order, adjacency expansion, indexes, and operators such as hash join, expand-into, shortest path, or repeated expansion. Cardinality estimation is difficult because edges are correlated. Independence assumptions can misestimate triangles and community patterns drastically.

Inspect plans and actual row/binding counts at each operator. A predicate applied after expansion can create millions of intermediate bindings to return ten rows. Rewrite only when semantics—especially path and optional matching—are preserved.

**Distinguish transactional and analytical graphs.** Interactive operational graphs optimize small mutations and bounded neighborhoods. Global PageRank, components, or embeddings scan most edges and may belong in batch/distributed analytical snapshots. Running them on the primary can evict caches and block compaction or transactions.

Move analytical snapshots with explicit freshness and provenance. Applying a score back into the operational graph creates derived state requiring version, expiry, and reconciliation.

**Compare relational representation.** An edge table `(src,type,dst,properties)` with endpoint and composite indexes can serve many graphs. Recursive SQL expresses reachability; relational constraints and joins can be valuable. A native graph engine may provide direct adjacency, path syntax, and graph algorithms. Benchmark representative depth, selectivity, degree, mutation, transaction, and operations rather than counting joins.

**Compare RDF representation.** RDF and SPARQL support globally named predicates, interoperability, federated vocabularies, and graph patterns. Open-world and entailment choices differ from closed application constraints. SHACL describes validation of RDF graphs but validation scope and enforcement timing must still be engineered.

Mapping a property graph edge with properties into RDF may require reification or another extension; mapping RDF blank nodes and multi-valued predicates into a property graph can lose semantics. Document the mapping and round-trip tests.

**Secure traversal.** Authorize start vertices, edge types, intermediate nodes, properties, endpoints, path results, algorithms, and write operations. Filtering only final results can let a query infer forbidden relationships through existence, count, degree, timing, or error differences.

Row/label-based rules may be insufficient for relationship-based policy. Precompute permitted subgraphs only with freshness and revocation guarantees. Bound query complexity per tenant and protect supernodes from denial of service. Sanitize dynamic labels, property keys, and query fragments through typed APIs.

Graph data is re-identifiable: a few relationships can identify a person even after names are removed. Treat exports, embeddings, similarity scores, logs, and query traces as sensitive derived data. Deletion includes incident edges, replicas, indexes, analytical snapshots, and models under policy.

**Back up the complete graph.** Capture vertices, edges, stable IDs, labels/types, properties, version/tombstone state, schema/constraints, indexes or rebuild definitions, routing/topology metadata as needed, security, encryption keys, procedure versions, and replay coordinate under one boundary.

Restore into isolation. Verify unique identities, endpoint integrity, inverse adjacency, constraints, counts by type, property types, checksums, representative paths, shortest-path oracles, authorization, and replay continuity. Counts can match while edges point to wrong vertices.

**Benchmark topology-shaped workloads.** Use degree distributions, labels/types, communities, supernodes, cycles, path multiplicity, properties, temporal versions, and mutation locality matching production. Include point starts, one-hop, selective multi-hop, existence, all-path, shortest path, pattern joins, writes, deletes, constraints, and analytical jobs.

LDBC's Social Network Benchmark supplies governed workloads and data generation for graph systems, but no benchmark universally represents an authorization or fraud graph. Report dataset scale factor, engine/version/configuration, warm/cold cache, concurrency, result size, plans, network, memory/spill, compaction, and recovery.

Inject node and network loss, shard movement, stale routing, partial adjacency updates, corrupt edge/index records, disk full, timeout/cancellation, supernode requests, and restore. Compare finite queries against a simple reference graph. A successful run establishes observed behavior only.

The executable fixture below performs finite directed BFS with a visited set and sorted adjacency. It proves the declared shortest-hop result for one graph only. It is not a database, weighted solver, all-path enumerator, authorization engine, transaction test, or distributed benchmark.

<!-- bijux-verify: {"id":"finite-graph-bfs","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"reachable=true\nshortest_hops=3\npath=A,B,D,F\nvisited_vertices=6\ncycle_terminated=true\ndirection_respected=true\nevidence=finite_graph_bfs\n","stderr":""}} -->
```python
adjacency = {
    "A": ["B", "C"],
    "B": ["A", "D"],
    "C": ["D", "E"],
    "D": ["F"],
    "E": ["C"],
    "F": [],
}
queue = [("A", ["A"])]
visited = {"A"}
result = None
while queue:
    vertex, path = queue.pop(0)
    if vertex == "F":
        result = path
        break
    for neighbor in sorted(adjacency[vertex]):
        if neighbor not in visited:
            visited.add(neighbor)
            queue.append((neighbor, path + [neighbor]))

print(f"reachable={str(result is not None).lower()}")
print(f"shortest_hops={len(result) - 1}")
print(f"path={','.join(result)}")
print(f"visited_vertices={len(visited)}")
print(f"cycle_terminated={str(len(visited) <= len(adjacency)).lower()}")
print(f"direction_respected={str('A' not in adjacency['F']).lower()}")
print("evidence=finite_graph_bfs")
```

## Definitions and Notation

- $G=(V,E)$ is a graph with vertices $V$ and edges $E$; the declared model specifies direction, labels, properties, multiplicity, and self-loops.
- An edge $(e,u,r,v,p)$ has identity $e$, source $u$, relationship type $r$, destination $v$, and properties $p$.
- **Out-degree** $deg^+(v)$ and **in-degree** $deg^-(v)$ count directed edges under named filters.
- A **walk** may repeat vertices/edges; a **trail** repeats no edge; a **simple path** repeats no vertex.
- **Reachability** $u\leadsto v$ means at least one permitted directed path exists.
- $b$ is effective branching factor and $d$ maximum traversal depth in a tree-like expansion estimate.
- A **supernode** has unusually high degree or traversal workload relative to operating bounds.
- A **pattern binding** assigns graph entities/values to query variables while satisfying predicates.
- **Adjacency** is the incident relationship set under direction/type/version/security filters.
- **Index-free adjacency** is an implementation locality property, not absence of all indexes or a universal complexity guarantee.
- A **cut edge** connects graph ownership units; $E_c$ is the cut-edge set under a partitioning.
- A **routing epoch** identifies authoritative placement during graph movement.
- A **derived edge** is computed from source data and carries algorithm/input version and expiry.
- A **graph snapshot** is the version boundary under which vertices and edges are interpreted together.

## Mechanisms, Invariants, or Proof Structure

**BFS shortest-hop argument.** In an unweighted directed graph, FIFO BFS dequeues vertices in nondecreasing distance from the source. When each vertex is first discovered, its recorded predecessor path has minimum hops; any shorter path would have reached it from an earlier layer. A visited set terminates cycles and preserves reachability, but does not enumerate every distinct path.

**Expansion estimate.** A tree with root and constant branching $b$ has $b^i$ vertices at depth $i$; through depth $d$ the sum is $1+b+\cdots+b^d=(b^{d+1}-1)/(b-1)$ for $b\ne1$. Shared graph vertices can reduce unique visits, while all-path enumeration can retain combinatorial multiplicity. This is a risk model, not an exact database cost.

**Endpoint integrity.** Creating edge $e=(u,r,v)$ is safe only if $u$ and $v$ exist in the transaction snapshot or the model permits dangling endpoints, edge identity/uniqueness holds, endpoint label/type constraints hold, and publication updates every authoritative adjacency/index representation atomically or repairably.

**Acyclic insertion obligation.** Adding $u\to v$ preserves acyclicity if there is no path $v\leadsto u$ in a serialization order covering concurrent inserts. A snapshot check without conflict detection can race with another insert. The theorem's graph premise and the transaction mechanism are both necessary.

**Traversal authorization closure.** A result path is permitted only if the principal may access the start, every traversed edge and intermediate vertex, requested properties, and the result under the policy snapshot. Post-filtering only endpoints does not satisfy this closure and can leak through existence or cost.

**Partition-movement preservation.** Before routing epoch switch, old ownership remains authoritative while the new copy catches up by stable edge/vertex version. At switch, fencing prevents old-epoch writes. Verification compares entities and adjacency; only after readers drain can old copies be reclaimed. Dual authority without conflict protocol violates the invariant.

**Restore equivalence.** For selected snapshots and authorized queries, restored identity, properties, constraints, and path results must equal the backed-up state, followed by idempotent ordered replay. Type counts or file presence alone cannot establish graph equivalence.

## Alternatives and Trade-Offs

**Property graph versus RDF.** Property graphs often fit application entities, attributed relationships, and imperative/declarative traversals. RDF fits standardized linked-data terms, vocabularies, federation, and entailment choices. Translation costs and semantic loss must be tested.

**Graph versus relational.** Native adjacency and path syntax favor traversal-heavy workloads. Relations favor mature joins, constraints, aggregation, and tabular integration. Recursive SQL may be entirely adequate for bounded hierarchies. Benchmark both under the real topology.

**Operational graph versus batch processing.** A transactional engine serves fresh bounded neighborhoods and updates. Pregel-like or analytical systems serve global iterative algorithms on snapshots. Combining them reduces data movement but can create severe resource interference.

**Normalize versus materialize edges.** One authoritative direction avoids duplication; reverse traversal needs an index or scan. Materializing both directions speeds reads but needs atomic update or reconciliation. Derived shortcut edges trade query time for freshness and storage.

**Hash versus community partitioning.** Hashing balances vertex count simply but cuts relationships. Community partitioning improves locality but can skew and age poorly. Boundary replication reduces reads while increasing update consistency work.

**All paths versus reachability.** All paths can provide explanations but output explodes and cycles require semantics. Reachability or shortest path is cheaper and often sufficient. Top-k constrained paths need ranking and completeness definitions.

**Online versus offline constraints.** Online enforcement prevents invalid commits but may require global coordination. Offline detection scales for advisory or repairable rules but permits invalid intervals. Business consequence decides which is acceptable.

**Exact versus approximate graph analytics.** Exact algorithms support strict claims at potentially high cost. Sampling, sketches, embeddings, and approximate nearest neighbors reduce cost but need error, bias, version, and reproducibility evidence.

## Failure Modes and Misconceptions

- **“Relationships imply a graph database.”** Dominant operations and guarantees, not visual shape, decide storage.
- **“Property graphs and RDF are equivalent.”** Identity, properties, triples, entailment, validation, and queries differ.
- **“Edges need no identity.”** Parallel events, correction, idempotency, and audit often require it.
- **“Adjacency makes traversal O(1).”** Each hop may be local, but expansion and output remain large and can be remote.
- **“Depth three is always small.”** Effective branching and supernodes determine work.
- **“Visited sets are only optimization.”** They define reachability/simple exploration and terminate cycles; all-path semantics differ.
- **“Shortest path means BFS.”** Only for unweighted/equal-cost graphs under correct direction and snapshot.
- **“MVCC prevents graph invariant races.”** Snapshot isolation can permit cardinality and cycle write skew.
- **“Hash partitioning balances a graph.”** It may balance vertices while exploding cut-edge messages.
- **“Authorization can filter final results.”** Intermediate traversal and side channels can disclose forbidden structure.
- **“A derived edge is a fact.”** It is a versioned model output with expiry and provenance.
- **“Counts prove restore.”** Wrong endpoints can preserve counts and destroy reachability.
- **“An algorithm result is deterministic.”** Parallel scheduling, equal scores, floating arithmetic, and sampling can vary.
- **“Global analytics belongs on the primary.”** It can exhaust memory, network, and caches needed by transactions.
- **“Benchmark scale is only vertex count.”** Edges, degree skew, patterns, properties, mutations, and result size drive cost.

## Worked Examples

### Example 1

**Situation.** Two `TRANSFERRED_TO` events connect account A to B on different days. A schema identifies edges only by `(A,type,B)`.

The second collides with or overwrites the first, losing event history. Assign stable transfer IDs and event/valid time. If a separate current aggregate edge is useful, derive `TOTAL_TRANSFERRED` with source frontier and recomputation rules.

**Conclusion.** Parallel edge semantics determine whether a graph is a multigraph and how history survives.

### Example 2

**Situation.** An organization permits at most one active manager per employee. Two transactions concurrently see no manager and insert different edges.

Under snapshot isolation, both reads can be valid and both inserts touch different edge records, creating two managers. Enforce a unique active-manager ownership key, serializable predicate, or serialized employee aggregate. Detect-and-repair is acceptable only if a double-manager interval is allowed.

**Conclusion.** Edge uniqueness does not automatically enforce endpoint cardinality.

### Example 3

**Situation.** A query follows any relationship up to depth four with effective branching 20.

The tree-like visit shape is $1+20+400+8{,}000+160{,}000=168{,}421$. Cycles may reduce unique vertices with visited semantics, while all distinct paths may still explode. Restrict edge types, start selectivity, direction, depth, uniqueness, and budget.

**Conclusion.** A small hop count can still be an availability risk.

### Example 4

**Situation.** Graph A→B, A→C, B→D, C→D, D→F, with unit weights, asks shortest A-to-F hops.

BFS explores layers: distance 0 A; distance 1 B,C; distance 2 D and perhaps other neighbors; distance 3 F. Either A-B-D-F or A-C-D-F has three hops depending on stable neighbor order. A visited set prevents duplicate D expansion.

**Conclusion.** FIFO layering proves shortest hop count; deterministic tie ordering selects one equally short path.

### Example 5

**Situation.** A root group has ten million member edges. An authorization check asks whether user U belongs to root through nested groups.

Expanding outward from root is disastrous. Search backward from U through its usually small parent-group adjacency, or use bidirectional search/materialized closure with revocation guarantees. Degree-aware planning and edge direction matter more than nominal depth.

**Conclusion.** Supernode-aware traversal can change the direction and data structure of the query.

### Example 6

**Situation.** Vertices are hash-partitioned evenly, but 70% of traversed edges connect different partitions.

Vertex count is balanced while most hops incur network routing, serialization, retry, and partial failure. Measure traversal-weighted cut, not only $|E_c|/|E|$. Community-aware placement or boundary replication may help, with movement and consistency costs.

**Conclusion.** Balanced storage can coexist with path-locality failure.

### Example 7

**Situation.** Deleting a user cascades through five million incident edges in one transaction.

The transaction can exceed locks, WAL, timeout, replication, or recovery limits. Fence the user as logically deleted so reads and traversals exclude it, enumerate incident edges through resumable keyed batches, tombstone derived/index state, reconcile, and publish completion. Preserve audit and retention obligations.

**Conclusion.** Logical atomic visibility can be separated from bounded physical cleanup.

### Example 8

**Situation.** A fraud analyst may see accounts but not medical-device relationships. The query traverses hidden devices and returns only account endpoints.

Endpoint filtering still leaks that a connection exists, and timing/count may reveal hidden degree. Apply policy during expansion to edges and intermediate vertices under one policy snapshot; consider whether even reachability through hidden entities is allowed. Audit query intent and bound complexity.

**Conclusion.** Graph authorization is path-closed, not merely row filtering at output.

### Example 9

**Situation.** A similarity model writes edges but omits model version and input snapshot. A model update changes scores.

Old and new scores cannot be distinguished, selectively expired, or reproduced. Use derived edge identity containing pair plus model/output version, store input frontier and generated/expiry time, write a new generation, validate, atomically switch readers, and reclaim old generation later.

**Conclusion.** Computed edges are governed materializations, not timeless relationships.

### Example 10

**Situation.** Restore has 1 million vertices and 8 million edges, matching production counts, but shortest routes differ.

Counts permit edges with wrong endpoints, direction, types, or properties. Compare stable IDs and keyed digests, validate endpoint constraints and both adjacency directions, sample neighborhoods, run fixed reachability/shortest-path oracles, verify indexes/security, and replay from an exact coordinate.

**Conclusion.** Graph restore needs topology and semantic equivalence evidence.

## Cross-Program Connections

[Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) supplies graph representations, BFS/DFS, heaps, union-find, and complexity. Database engineering adds persistence, transactions, indexing, concurrency, recovery, and operations.

[Algorithms Engineering](../../16-algorithm-engineering/ROADMAP.md) connects shortest paths, flow, matching, ranking, approximation, and topology-shaped performance. Procedure names do not replace algorithm premises.

[Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies partitioning, replication, snapshots, membership, and partial-failure reasoning. Cut edges make these mechanisms visible at every hop.

[Security Engineering](../../25-security-engineering/ROADMAP.md) connects relationship-based authorization, inference, privacy, denial of service, audit, and deletion. Graph structure itself is sensitive data.

[Data Engineering](../../19-data-engineering/ROADMAP.md) connects event-derived graphs, replay, materialized relationships, provenance, reconciliation, and analytical snapshots. Derived edges need lifecycle ownership.

[API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) connects query cost budgets, pagination, cancellation, conditional mutations, authorization, and stable cursors. Exposing unrestricted graph language is an API and availability decision.

## References

- openCypher Project, [openCypher resources and specification](https://opencypher.org/resources/), current resources checked 2026-09-05. Property-graph query language grammar and semantic resources.
- Richard Cyganiak, David Wood, and Markus Lanthaler, editors, [RDF 1.1 Concepts and Abstract Syntax](https://www.w3.org/TR/rdf11-concepts/), W3C Recommendation, February 2014. RDF graph, triple, IRI, blank-node, literal, and dataset semantics.
- Steve Harris and Andy Seaborne, editors, [SPARQL 1.1 Query Language](https://www.w3.org/TR/sparql11-query/), W3C Recommendation, March 2013. Standard RDF graph-pattern and property-path query semantics.
- Holger Knublauch and Dimitris Kontokostas, editors, [Shapes Constraint Language (SHACL)](https://www.w3.org/TR/shacl/), W3C Recommendation, July 2017. Standard RDF graph validation shapes and result model.
- Apache TinkerPop, [Reference Documentation](https://tinkerpop.apache.org/docs/current/reference/), current documentation checked 2026-09-05. Property graph, traversal, path, strategy, and implementation-neutral API concepts.
- Neo4j, [Graph database concepts](https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/), current documentation checked 2026-09-05. Concrete property-graph node, relationship, label, property, traversal, and index concepts.
- Neo4j, [Constraints](https://neo4j.com/docs/cypher-manual/current/constraints/), current Cypher manual checked 2026-09-05. Concrete uniqueness, existence, type, and key constraint behavior.
- Neo4j, [Search-performance indexes](https://neo4j.com/docs/cypher-manual/current/indexes/search-performance-indexes/managing-indexes/), current Cypher manual checked 2026-09-05. Concrete range, text, point, token, and index-management behavior.
- Linked Data Benchmark Council, [Social Network Benchmark](https://ldbcouncil.org/benchmarks/snb/), current benchmark documentation checked 2026-09-05. Governed interactive, business-intelligence, and graph-analytics workloads and data generation.
- Grzegorz Malewicz et al., [Pregel: A System for Large-Scale Graph Processing](https://research.google/pubs/pregel-a-system-for-large-scale-graph-processing/), SIGMOD 2010. Primary source for vertex-centric bulk-synchronous graph computation.

## Exercises

### Exercise 1

Define property graph, RDF graph, vertex identity, edge identity, walk, simple path, supernode, cut edge, and index-free adjacency. Explain why none alone determines query performance.

### Exercise 2

For effective branching factor 6, compute the tree-like number of visits through depths 0 to 5. Then compare reachability with a visited set to all-path enumeration in a graph where many branches reconverge.

### Exercise 3

Two concurrent hierarchy updates add A→B and B→A after each transaction independently observes no reverse path. Diagnose the isolation anomaly and design three enforcement strategies with trade-offs.

### Exercise 4

Design storage and query paths for an authorization graph with users, groups, resources, delegated roles, expirations, revocation within one minute, supergroups, tenant isolation, and audit. Address identity, constraints, traversal, materialization, and failure.

### Exercise 5

A fraud graph must repartition while accepting writes, preserve historical relationship events, run global analytics nightly, protect sensitive relationship types, and prove restore equivalence. Design the operational protocol and its evidence.

## Answers to the Exercises

### Answer 1

A **property graph** stores labeled/property-bearing vertices and edges. An **RDF graph** is a set of standardized subject-predicate-object triples. **Vertex identity** names an entity occurrence; **edge identity** distinguishes a relationship/event, including parallel edges. A **walk** may repeat; a **simple path** repeats no vertex. A **supernode** has exceptional degree/work. A **cut edge** crosses ownership units. **Index-free adjacency** means an implementation can follow stored adjacency without a global lookup per hop. Performance still depends on start selectivity, branching, depth, path semantics, output, predicates, snapshot, cache/storage, partition cuts, authorization, concurrency, and plan.

### Answer 2

The count is $1+6+36+216+1{,}296+7{,}776=9{,}331$. In a reconvergent graph, reachability with a visited set expands each reachable vertex at most once under the selected edge set, so unique work approaches vertices plus examined edges. All-path enumeration preserves distinct predecessor sequences; many paths can share the same endpoints and internal vertices, so output and retained state can remain exponential. Using a visited set for an all-path question changes the answer. State whether the requirement is existence, shortest path, endpoints, top-k, trails, simple paths, or all walks.

### Answer 3

Each snapshot lacks the other's edge, so both pass local reachability tests and the committed graph has a cycle: predicate write skew. Strategy one uses serializable transactions whose read/write predicate detects the conflict; correctness is direct but reachability validation may be costly. Strategy two serializes hierarchy mutations through a scoped owner/lock or ordered coordinator; throughput is bounded by that scope but reasoning is simpler. Strategy three represents a strict tree/hierarchy with parent uniqueness and interval/path labels maintained under a specialized atomic protocol; it accelerates checks but makes reparenting complex. Offline cycle detection is a fourth option only if temporary cycles are acceptable and downstream behavior is safe.

### Answer 4

Use stable tenant-namespaced identities for users, groups, roles, resources, delegations, and mutation events. Constrain endpoint types, unique active delegation identity, expiry type, and self/cycle rules appropriate to group nesting. Traverse backward from user memberships and forward through bounded group/role edges under one policy snapshot, applying tenant, edge, intermediate-node, expiry, and resource authorization during expansion. Treat supergroups separately with indexed membership or sharded/materialized closure. A closure can meet one-minute revocation only with versioned updates, lag monitoring, fail-closed behavior after the freshness bound, replay, and reconciliation against authoritative edges. Mutations use idempotency, transactional authoritative edges, and an audit event carrying actor/reason. Timeouts, truncation, and partial shard failure cannot be interpreted as denial or permission silently; the API returns an explicit indeterminate/error according to policy.

### Answer 5

Store immutable relationship events as authority and project a current graph with stable vertex/edge IDs, source versions, valid time, and provenance. Repartition under a routing epoch: snapshot-copy vertices and both adjacency directions, stream later idempotent mutations, compare keyed edges/endpoints/properties and fixed path queries, then atomically switch/fence old owners and drain readers before reclamation. Nightly analytics consumes a versioned graph snapshot and writes derived edges/scores into a separate generation with model/input version and expiry. Authorization filters sensitive types during traversal and protects logs, exports, and analytical snapshots. Backup includes events, current projection, schema/constraints, indexes or rebuilds, routing epoch, security/keys, analytics generation, and replay coordinate. Restore verification checks IDs, endpoint integrity, adjacency symmetry, constraints, counts by type, digests, representative reachability/shortest paths, authorization, and idempotent replay. No global instant is claimed unless the snapshot protocol supplies one.
