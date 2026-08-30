---
module_id: DSE-059
program: Data Structures Engineering
level: 2
module_number: 59
title: Full and Confluent Persistence
status: complete
last_verified: 2026-08-30
---

# Full and Confluent Persistence

## One-Page Review

### Governing question

What changes when clients may update any retained version and combine several versions, and how do version ancestry, merge semantics, sharing, complexity, lifetime, and evidence remain correct as history becomes a tree or DAG?

### Essential definitions

- **partial persistence** permits queries of all retained versions but updates only the newest version.
- **full persistence** permits a query or update from any retained version; one-parent updates form a rooted version tree.
- **confluent persistence** additionally permits an operation with two or more version operands; version history becomes a directed acyclic graph (DAG).
- A **version parent** is an input version from which an update derives a new version; it differs from a pointer inside the represented data structure.
- A version `a` is an **ancestor** of `b` when a directed version path leads from `a` to `b`.
- A **meld** is a structure-specific operation combining logical values, such as rope concatenation or set union; it is not a universal conflict resolver.
- **path multiplicity** counts root-to-version derivations; repeated operands can be normalized through distinct identity versions and still make it grow exponentially in a small version DAG.
- **effective depth** in the Fiat–Kaplan analysis is `1 + log2(number of root-to-version paths)`.
- **disjoint confluence** restricts meld operands so their represented node sets do not overlap.
- **functional persistence** restricts physical implementation to immutable nodes/new allocation; it does not by itself define a meaningful meld for every abstract data type.

### Central model, mechanism, or theorem

In partial persistence, field records can be chosen by greatest numeric version `<=q` because versions form a line. Full persistence breaks that rule: two records may lie on incomparable branches. A versioned read must choose the applicable modification on the ancestor path to query version `q`. Driscoll, Sarnak, Sleator, and Tarjan represent the version tree with a maintained preorder/order structure so descendant versions occupy an interval, then use fat-node or node-splitting machinery under stated pointer-machine assumptions.

Confluent persistence adds multi-parent derivations. Repeatedly concatenating a version with itself creates logical length `2^k` after `k` melds while allocating only a linear-size sharing DAG. Consequently, copying inputs is not merely a poor constant factor; materialization can be exponential in the compact derivation size. Fiat and Kaplan give general pointer-structure transformations whose costs depend on version-DAG path structure, including effective depth. Later work obtains logarithmic overhead under a disjoint-confluence restriction. These are exact model results, not guarantees for arbitrary merge APIs.

### Critical invariants

1. Version nodes are immutable after publication; every parent is already published, from the same structure/generation, and no version cycle exists.
2. Full-persistent field lookup applies only modifications ancestral to the query and selects the nearest applicable one according to the construction.
3. A one-parent update preserves every other branch and creates exactly one new logical state.
4. A meld's abstract semantics, operand order, duplicate-operand behavior, conflict policy, and failure behavior are explicit.
5. Structural sharing never creates a cycle in an abstractly acyclic value and does not permit mutation through aliases.
6. Version ancestry/path-count labels and physical-node pedigrees remain valid after insertion, serialization, compaction, and recovery.
7. Logical size, physical nodes, number of versions, number of version paths, and output materialization are measured separately.
8. Reclamation retains everything reachable from any live version, reader, iterator, export, replica, audit record, or recovery root.
9. Publication commits the new data root, all parent edges, provenance, indexes, and durability evidence atomically.
10. Validation checks both the version graph and the logical data value for every retained version against an independent model.

### Common failures

- Using numeric `<=` to resolve changes in a branching version tree.
- Confusing a data-structure node's parent with a version's parent.
- Calling two-way conflict resolution “confluent persistence” without defining an abstract meld.
- Treating version merge as union of physical node sets.
- Mutating shared input nodes after a meld.
- Assuming a purely functional representation automatically supplies efficient concatenation/union.
- Materializing a self-concatenated DAG and exhausting exponential time or memory.
- Counting version DAG nodes while ignoring exponentially many derivation paths or logical elements.
- Reclaiming a shared node because one input version was deleted.
- Importing parent edges without cycle, ownership, arity, size, and path-amplification limits.

### Compact example

Version 0 is rope `A`. Updating version 0 twice creates incomparable branches `AB` and `AC`. Melding them by ordered concatenation creates `ABAC`. Melding that value with itself four times creates a 64-character logical rope with only four additional concatenation nodes. Each repeated operand is represented by a distinct one-parent identity version before the meld, avoiding parallel version edges; the final version has 32 root paths. Random access descends by cached subtree lengths and never materializes the whole rope.

### Connections

[DSE-051](051-path-copying.md) introduces version roots; [DSE-052](052-structural-sharing.md) supplies alias and lifetime reasoning; [DSE-056](056-finger-trees.md) supplies a sequence representation with concatenation; [DSE-058](058-fat-nodes-and-partial-persistence.md) establishes the linear-history baseline. The [program roadmap](../ROADMAP.md) next makes the evidence/benchmark model explicit in DSE-060.

## Governing Question

When history can branch from any old version and later reconverge through structure-specific melds, which semantics and representations preserve every version without confusing ancestry, aliasing, compact sharing, logical size, operational cost, or durable provenance?

## Why This Matters

Branching is ordinary engineering reality. Editors fork documents. Solvers speculate. compilers preserve alternative intermediate representations. package managers compare dependency states. simulations explore counterfactuals. source-control-like systems retain divergent histories. A partially persistent structure forces updates through one newest state and cannot express these workflows directly.

Full persistence makes an old version a valid update base. A new version keeps exactly one parent, so history is a tree. Every branch remains queryable and updateable. Pure immutable trees often provide this naturally because an update returns a new root and leaves old nodes untouched. General transformation of an imperative pointer structure is harder because version selection is no longer a predecessor query on an integer timeline.

Confluence goes further: a new state derives from multiple prior versions. This is useful when the abstract type has a real composition operation—concatenate two ropes/deques, union two sets, meld heaps, link proof objects, or combine scene subgraphs. It is not synonymous with resolving concurrent edits. A map merge needs a policy for two values at one key; a text merge needs alignment and conflicts; a heap meld has different semantics. Persistence preserves operands and result; it does not choose the domain rule.

Confluence changes scale. A compact DAG can denote an exponentially large unfolded value. Starting with one symbol, repeatedly concatenate a rope with itself. The version count and allocated concatenation nodes grow linearly, while logical length doubles. Any API that eagerly flattens, hashes every element, serializes the unfolded value, or validates by expansion can be forced into exponential work.

The version graph itself becomes data. Parent order may affect noncommutative meld. Duplicate parents may be meaningful. Provenance, access control, retention, and audit traverse a DAG, not a list. Deleting one version cannot reclaim nodes shared through another path. Counting derivations can overflow fixed-width integers. Malicious imports can contain cycles or amplification bombs.

This module therefore treats semantics, version topology, data representation, complexity model, and system policy separately. A theorem about bounded-degree pointer machines does not settle a production merge contract; a correct immutable rope does not prove general confluent transformation bounds.

## Prerequisites and Retrieval

Retrieve trees/DAGs, reachability, topological order, lowest/common ancestors, ordered lists, hashing, immutable sharing, amortized analysis, transactions, and graph serialization. From [DSE-051](051-path-copying.md), retrieve path copying, version roots, and persistence levels. From [DSE-052](052-structural-sharing.md), retrieve logical versus physical equality and reachability-based lifetime.

From [DSE-056](056-finger-trees.md), retrieve measured sequences and concatenation interfaces. From [DSE-058](058-fat-nodes-and-partial-persistence.md), retrieve versioned fields, simulation, atomic publication, bounded in-degree, root directories, and the pointer-machine transformation boundary. You should be able to distinguish an abstract data graph from its version graph and prove an operation by refinement to an immutable mathematical value.

## Learning Objectives

After completing this module, you can:

1. distinguish partial, full, confluent, and functional persistence by interface and representation;
2. explain why numeric predecessor lookup fails on a version tree;
3. specify ancestry-aware field selection and the purpose of version-tree order maintenance;
4. define a structure-specific meld, including order, duplication, conflicts, and failure;
5. derive exponential logical growth under repeated self-composition without materializing it;
6. reason about effective depth, path multiplicity, and disjoint-confluence assumptions;
7. design version/DAG handles, provenance, atomic publication, retention, and recovery;
8. prevent alias mutation, cycles, amplification, and hostile serialized histories;
9. validate data semantics and version topology with independent models and metamorphic tests; and
10. benchmark physical growth, logical size, ancestry/index cost, sharing, query depth, merge tails, and reclamation.

## Core Exposition

**Separate two graphs.** The *data graph* consists of nodes/fields implementing one or more logical values. The *version graph* records derivation between published roots. A tree node may have a `parent` field while its containing version has a parent version; these relations are unrelated. Give their types different names and IDs.

Let version 0 contain initial root `R_0`. A full-persistent unary update `U(v,args)` returns new version `w` with version edge `v -> w` and root `R_w`. Because each new version has one parent, versions form a rooted tree even if their data roots share an arbitrary DAG. Query/update accepts any retained `v`.

A confluent operation `M(v_1,...,v_k,args)` returns `w` with an ordered parent tuple. With `k>=2`, the version graph is a DAG if every parent predates `w`. Parent order matters for concatenation and left-biased map merge. Reusing the same value twice may be meaningful. If the graph representation forbids parallel edges, create a distinct one-parent identity version for the second operand; silently deduplicating operands changes the result and path multiplicity.

**Full persistence invalidates linear stamps.** In a partial history `0<1<...`, a field read at version `q` chooses greatest stamp not exceeding `q`. Suppose version 0 branches to versions 1 and 2. A field changes to `A` on branch 1 and `B` on branch 2. Querying a descendant of 1 must ignore the `B` record even if version 2 received the larger numeric ID. Applicability is ancestry, not creation-time comparison.

A conceptually simple fat field stores modifications tagged by version. To read at `q`, filter to modifications whose version is an ancestor of `q` and choose the deepest applicable modification along that root-to-`q` path. This is correct but scanning all records and testing ancestry can be slow.

Driscoll, Sarnak, Sleator, and Tarjan maintain a total order corresponding to a preorder of the version tree. Descendants of a version occupy a contiguous interval beginning at it. New versions are inserted after their parent in a dynamically maintained version list/order. This supports determining which modifications govern a query without assuming version IDs are chronological predecessors. Their full-persistence constructions use fat nodes or node splitting with precise navigation and pointer-machine bounds.

The order label is internal metadata, not the public version identity. Relabeling/order-maintenance must not invalidate durable handles. A preorder rank assigned once cannot remain valid under arbitrary insertions without gaps/relabeling; use a proved order-maintenance structure or rebuild transactionally with stable IDs.

**Full persistence can be simple when the data type cooperates.** An immutable balanced tree update from any root copies a search path and returns a new root. The version tree is an external directory. No versioned-field ancestry search is required because physical nodes never change. The cost is representation-specific copying/allocation, and rebalancing proof must cover shared subtrees.

This simple approach is *functional* in implementation: existing nodes are not changed. General full-persistence transformations may mutate auxiliary representations while preserving observable versions. Interface strength and physical immutability are different axes. Also, immutability does not invent an efficient meld; concatenating two immutable arrays still copies unless a rope/tree representation supplies composition.

**Define confluence at the abstract type.** For ropes, `meld(a,b)=a followed by b`: ordered, noncommutative, duplicate-preserving. For sets, union is commutative/idempotent under set equality, though representation/provenance may differ. For maps, a key conflict requires reject, left/right bias, a combining function, multi-value storage, or domain reconciliation. For heaps, meld preserves the multiset and heap order; duplicate handling follows the heap contract.

State whether meld consumes no inputs (persistence says old versions remain observable), whether operands must belong to one universe/comparator/schema, whether identical operands are allowed, whether cycles/references are permitted, and what failure returns. If a callback resolves conflicts, its determinism, purity, termination, failure, security, and version compatibility are part of the operation.

Do not implement meld as union of physical node sets. Physical sharing is an implementation relation; logical concatenation may include the same shared subtree twice. Conversely, set union should not duplicate elements because two physical nodes exist. Refine physical roots to abstract values, define `M_abs`, and prove `abstract(R_w)=M_abs(abstract(R_v1),...)`.

**Compact confluence creates amplification.** Let rope `x_0` contain one symbol and define `x_(i+1)=concat(x_i,x_i)`. Its logical length satisfies `L_0=1` and `L_(i+1)=2L_i`, so `L_i=2^i`. An immutable rope DAG allocates one concatenation node per step and lets both child pointers reference the same root. Physical growth is `Theta(i)` while unfolded output is `Theta(2^i)`.

This sharing is correct because concatenation denotes occurrences, not unique physical nodes. Iteration legitimately visits the shared child twice. A visited-node set used as a generic cycle guard would incorrectly output it once; cycle detection must distinguish the active recursion stack from repeated acyclic occurrences. Random access can descend by stored subtree lengths in height time without expansion.

Cached length may exceed machine integers. Use checked/big integers or a documented cap/saturation policy. Saturation cannot support exact bounds/indexing beyond the cap without additional representation. Cached hashes can sometimes combine without unfolding, but cryptographic hash semantics for repeated concatenation require a composable scheme; naively hashing all bytes is output-size work.

**Version path multiplicity captures another amplification.** Fiat and Kaplan define effective depth `e(v)=1+log2 |R(v)|`, where `R(v)` is the set/count of root-to-`v` paths in the version DAG. A version tree has one root path per node, hence effective depth one even when ordinary depth is large. Melds make paths reconverge; repeated self-meld can double path count each step, making effective depth grow linearly in updates.

Ordinary depth is the longest parent chain. Effective depth can reflect far more derivations than depth alone. Counts may be enormous, so implementations can store logarithmic bounds or arbitrary-precision counts depending on the required decision. Do not use floating-point logs to authorize resource limits near a boundary without conservative error handling.

Fiat and Kaplan's general transformations show confluence is possible with costs depending on the version DAG, yielding an exponential improvement over naive materialization in the hard cases. Their fat-node pedigrees, path representations, and bounds are sophisticated. Cite/use the construction exactly; do not summarize it as “fat nodes plus two parents.”

Collette, Iacono, and Langerman later study a disjoint-confluence restriction: versions being merged do not share data nodes. Under their bounded-in-degree model, they obtain logarithmic overhead. Disjointness is a semantic/physical precondition that repeated self-concatenation violates maximally. Checking it may itself require ownership/provenance metadata.

**Sharing and alias safety are non-negotiable.** After meld, inputs and result may share nodes. Any in-place balancing, parent-pointer repair, memoization, lazy forcing, refcount update, or cache installation must be proven observationally safe and synchronized. Prefer immutable nodes or exclusive ownership before mutation. Copy-on-write uniqueness tests must include every retained version and reader, not only the two operands.

Parent pointers inside shared trees are especially problematic: one node can appear under multiple logical parents. Remove them, make them path/context data, version them, or define occurrence identities. A raw physical node handle cannot identify a unique logical position in an unfolded DAG. Use `(version,path)` or an abstract stable element ID with explicit multiplicity semantics.

Meld must not introduce a prohibited data cycle. Allocating a fresh concat node pointing to already published roots is acyclic because edges point to older nodes. Deserializing arbitrary node IDs or letting a callback install backedges requires cycle validation or a coinductive/cyclic abstract type with separate algorithms.

**Version identities and provenance.** A handle should include repository/structure identity, schema/comparator/universe fingerprint, generation, and stable version ID. Version IDs need not reveal topological order; parent validation ensures every new edge points to an existing compatible version and publication never creates a cycle.

Record operation kind, ordered parents, parameters or content digest, author/tenant, policy decision, timestamp as metadata, and resulting root digest where appropriate. This supports audit but can expose sensitive history. Sign/authenticate records if provenance is a security boundary; a hash alone does not establish who authorized a merge.

Content-addressed roots deduplicate equal physical content, but version identity may still differ because provenance, permissions, or operation history differs. Conversely, equal version IDs across replicas are unsafe without a namespace. Specify equality among handle identity, abstract value, content digest, and ancestry.

**Atomic multi-parent publication.** Validate all handles and access rights, pin operands, check schema/comparator and meld-specific preconditions, reserve resources, build the result in staging, validate data invariants, write nodes/indexes/provenance, make them durable as required, then atomically publish one version record containing the complete ordered parent tuple and result root. On failure, no parent or prior version changes.

Concurrent writers may safely create independent child versions if full persistence permits it, but publication must allocate unique IDs and maintain indexes. A confluent operation racing with retention must pin every operand. If policy forbids merging a revoked/expired version, authorization and pinning order must prevent time-of-check/time-of-use errors.

Crash recovery must never publish a version with one missing parent, root, or data chunk. A write-ahead/commit record names the complete dependency set and checksum. Recovery processes a topological prefix of valid commits, quarantines missing/cyclic/unauthorized records, and recomputes or verifies indexes.

**Retention becomes DAG reachability.** Deleting a version handle does not necessarily delete its root or ancestors: descendants and meld results may share them. Policies differ: retaining a result may require retaining parent provenance even if parent data roots can be compacted; audits may require full derivation; privacy erasure may require rewriting descendants or declaring impossibility/cryptographic erasure.

Compute liveness from named retained versions, readers, iterators, exports, replicas, backups, legal holds, and recovery transactions through both version dependencies and data roots. Reference counts must account for duplicate edges if they represent distinct ownership occurrences, although liveness itself is boolean reachability. Cyclic corruption defeats naïve refcount/traversal assumptions.

Compaction can rewrite a shared DAG into another representation while preserving abstract values and stable handles via indirection. Validate retained versions and parent/provenance mappings before switch. Flattening a compact exponential rope is not acceptable compaction; quotas must limit logical expansion and output requests.

**Security is graph security.** An attacker can submit enormous parent tuples, deep chains, exponentially many paths, huge logical lengths, cyclic data/version graphs, hash-collision workloads, incompatible comparators, expensive conflict callbacks, or recursive serializers. Enforce arity, versions, nodes, edges, depth, path/effective-depth estimates, logical size, physical bytes, traversal/output, callback time, recursion, and diagnostic limits.

Validate imports in quarantine: schema, stable-ID uniqueness, ownership/generation, parent existence/order, DAG acyclicity, topological sequence, operation arity, duplicate-parent policy, root existence, data cycles, lengths/aggregates, hashes/checksums/signatures, and abstract invariants. Do not allocate claimed logical size. Use iterative traversals or depth budgets.

Authorization may be monotone, intersection, union, or operation-specific across parents. A result must not leak data from an operand to a principal lacking access. Record who can name/read ancestors and whether provenance redacts sensitive parents. Error messages and timing can disclose version existence.

**Verification has two models.** First, model the version graph independently as immutable abstract values: unary update copies/transforms one value; meld computes the declared abstract operation. Compare every implementation version on generated histories. Second, validate the physical data/version graphs, sharing, cached measures, ancestry indexes, and lifetime.

Metamorphic tests: an update from `v` never changes `v` or siblings; meld leaves every operand unchanged; ordered meld reverses predictably; commutative/idempotent operations obey their algebra only when declared; serialization/reload preserves parents and abstract values; compaction preserves retained handles; failed publication adds no reachable version; resource rejection performs bounded work.

Small model checking can enumerate parent choices, repeated operands, incompatible handles, and injected failures. For full fat/node-splitting implementations, compare ancestry-aware field selection with a simple root-to-query scan. For confluence, test shared and disjoint operands separately and measure the stated precondition.

Benchmark version depth, branching factor, meld arity, path multiplicity/effective depth, operand overlap, logical/physical size ratio, data height, ancestry/index operations, allocations, cache misses, GC, pin duration, publication, serialization, recovery, and output size. A benchmark that flattens every result measures materialization rather than compact persistent operations.

## Definitions and Notation

- `G_V=(V,E_V)`: version graph with directed edges from parent versions to newly derived versions.
- `P(v)`: ordered parent tuple of version `v`; `|P(v)|=1` for an ordinary full-persistent update and at least two for a confluent meld.
- `a ⪯ v`: version `a` is an ancestor of `v`, including equality when reflexive ancestry is intended.
- `R_v`: physical data root associated with version `v`.
- `A(R_v)`: abstract value denoted by root `R_v`.
- `U_abs`: abstract unary update; correctness requires `A(R_w)=U_abs(A(R_v),args)`.
- `M_abs`: declared abstract meld; correctness requires `A(R_w)=M_abs(A(R_v1),...,A(R_vk),args)`.
- `paths(v)`: number of root-to-`v` directed paths in the version DAG; repeated operands are represented by distinct identity versions when parallel edges are excluded.
- `e(v)=1+log2(paths(v))`: effective depth used in the Fiat–Kaplan analysis.
- `d(v)`: ordinary longest root-to-`v` version-edge depth.
- `L(r)`: logical size/measure cached at data root `r`.
- `N_phys`: number of distinct allocated physical data nodes reachable from retained roots.
- `N_log(v)`: unfolded logical element/occurrence count of version `v`.
- **version tree**: a version graph in which each non-root version has exactly one parent.
- **version DAG**: an acyclic multi-parent derivation graph.
- **pedigree**: construction-specific metadata describing where a physical node/versioned value is applicable in a version DAG.
- **operand overlap**: physical data nodes reachable from more than one meld operand.

For a concat rope node `c=(left,right)`, `L(c)=L(left)+L(right)`. Random access at index `i` descends left when `i<L(left)` and otherwise descends right with `i-L(left)`. If both pointers are equal, they still denote two logical occurrence ranges.

## Mechanisms, Invariants, or Proof Structure

**Abstract version mechanism.** Publish version 0. A unary update validates one retained base and creates an immutable version record `(id,(base),operation,root)`. A confluent update validates an ordered tuple and creates `(id,parents,meld,root)`. Parents preexist, so publication order is a topological order and cycles cannot arise through the normal API.

**Full-persistence read invariant.** A versioned field at query `q` uses only records tagged by ancestors of `q`. Among applicable records, it chooses the one governing the nearest point on the unique root-to-`q` path. In a version tree that path is unique; incomparable branch records never compete. The selected DSST representation/order structure must implement this relation.

**Full update proof.** Assume `R_v` denotes abstract value `X`. Run the representation's persistent update, producing `R_w`, and prove refinement `A(R_w)=U_abs(X)`. Show every old root and its observable graph remains equivalent. Add one version edge `v->w`; because `w` is fresh, the version graph remains a tree.

**Meld proof.** Assume each operand root denotes `X_i`. Establish schema/universe compatibility and preconditions. Construct `R_w`, then prove `A(R_w)=M_abs(X_1,...,X_k)`. Prove operands remain unchanged, representation invariants hold, and resource/complexity claims include overlap and logical output semantics.

**Rope structural proof.** Leaves have positive finite text length. A concat node references already-built acyclic roots and stores their length sum, so induction proves data acyclicity and exact cached length. Character lookup decreases height each step and maps the index to exactly one leaf occurrence. Sharing, including `concat(r,r)`, does not affect this refinement.

**Exponential-growth derivation.** With `L_0=1` and `L_(i+1)=2L_i`, induction gives `L_i=2^i`: base `2^0=1`; if `L_i=2^i`, then `L_(i+1)=2*2^i=2^(i+1)`. The representation allocates one concat node per self-meld, so physical incremental space is linear, excluding metadata.

**Version-path recurrence.** For a root, `paths(root)=1`. For a derived version, `paths(v)=sum(paths(p) for p in P(v))`. A one-parent chain preserves one path. To double a value without parallel version edges, create identity child `u'` of `u`, then meld parents `(u,u')`; both have the same path count, so the sum doubles. Effective depth is derived from this combinatorial quantity, not data-tree height.

**Publication invariant.** A visible version record names a complete root, ordered parent tuple, operation/provenance, compatibility fingerprint, and valid indexes. Every referenced object is initialized/durable. Failure before the atomic commit leaves no visible version; recovery chooses only complete authenticated commits.

**Lifetime invariant.** A physical/version object is reclaimable only when unreachable from all named retained roots and dependency/provenance requirements and unpinned by readers/operations/replicas/recovery. Duplicate sharing cannot be inferred from one removed edge. Retention policy states whether ancestry metadata outlives operand data.

**Concurrency invariant.** Publication assigns unique stable IDs and atomic records. Readers pin version/data lifetime. Meld pins every operand through commit/failure. Mutable caches/indexes are synchronized. Callback behavior cannot reenter unpublished objects or mutate operands without an explicit effect protocol.

**Evidence hierarchy.** Source review checks theorem assumptions. Mathematical review checks ancestry selection, refinement, exponential recurrence, and path counting. Executable evidence covers a finite immutable rope/version DAG. Property/model tests compare abstract versions. Fault and concurrency tests cover publication/lifetime. Benchmarks characterize workload cost. None substitutes for the others.

## Alternatives and Trade-Offs

| Approach | Version topology | Strength | Principal cost/risk |
|---|---|---|---|
| Partial fat nodes | Line | old queries, latest update | numeric predecessor only; no branching |
| Full fat nodes | Tree | update/query any version | ancestry-aware record search |
| DSST node splitting | Tree | general bounded-degree transformation | sophisticated order/splitting proof |
| Immutable path copying | Tree naturally | simple branch isolation | changed-frontier allocation |
| Structure-specific meld | DAG | efficient domain composition | bespoke semantics/proof |
| Fiat–Kaplan transformation | DAG | general confluence model | effective-depth/pedigree complexity |
| Disjoint confluence | DAG with restriction | logarithmic-overhead result | operands must not share nodes |
| Copy then ephemeral merge | DAG logically | simplest semantics | can duplicate/explode logical inputs |
| Three-way application merge | DAG/provenance | conflict-aware user workflow | not a generic persistence transform |

Full immutable path copying is often the practical default for balanced search trees, tries, ropes, syntax trees, and other naturally recursive values. DSST-style transformation matters when converting an imperative bounded-degree structure and when its theoretical guarantees justify implementation complexity.

Structure-specific confluence can be dramatically better than a general transform. Finger trees/deques support concatenation through measured spines; unionable sets use order/hashing; heaps have native meld. Their guarantees depend on abstract operation and representation.

Naive copying is acceptable for small bounded values or rare administrative merges. It can also be a security boundary: materialize only below a strict size cap, validate, and detach aliases. It cannot handle compact exponential values without refusing them.

Application three-way merge uses a base plus two descendants and a conflict policy. It may create a multi-parent version, but its correctness is domain reconciliation, not merely persistent storage. CRDT joins require semilattice laws and distributed causality. Git-like objects/content addressing supply useful analogies but do not establish data-structure theorem bounds.

Choose based on whether old updates are needed, whether a real meld exists, operand overlap, degree, version topology, logical amplification, query/update/meld mix, output needs, durability, retention, security, and team proof capacity.

## Failure Modes and Misconceptions

- **“Larger version ID wins.”** IDs on incomparable branches do not determine applicability.
- **“A full history is a list.”** Full-persistent one-parent updates form a tree.
- **“Confluent means conflict-free.”** It means a declared multi-version operation; conflicts are domain semantics.
- **“Merge the node sets.”** Logical composition is not physical set union.
- **“Immutable means confluently efficient.”** Representation and operation must support compact meld.
- **“The DAG has ten nodes, so the value has size ten.”** Logical occurrence count can be exponential.
- **“Visited means cycle.”** A shared acyclic child can be visited through multiple occurrence paths; use active-stack cycle detection.
- **“Deduplicate repeated operands.”** `concat(v,v)` requires both logical occurrences; a simple-DAG model can represent the second through an identity version rather than discarding it.
- **“Depth captures all history complexity.”** Reconvergent path multiplicity motivates effective depth.
- **“General confluence is fat nodes with two stamps.”** Ancestry/pedigrees and transformation proofs are substantially more involved.
- **“Disjoint theorem applies after structural sharing.”** Shared nodes violate the precondition unless explicitly detached.
- **“One input deletion frees its nodes.”** Other inputs/results/readers can retain them.
- **“Refcount equals logical multiplicity.”** Physical liveness and unfolded occurrence count are distinct.
- **“Hashing is always compact.”** Ordinary byte hashing an exponential logical value is output-size work.
- **“Meld callbacks are harmless.”** Nondeterminism, failure, reentrancy, cost, and privilege can break publication.
- **“Any imported DAG is safe.”** Cycles, missing parents, amplification, incompatible schemas, and forged provenance require rejection.
- **“Benchmarking flatten proves persistent performance.”** It measures materialization, which may be intentionally exponential.

## Worked Examples

### Example 1

**Situation.** Version 0 has field `x=0`. Branch update version 1 sets `x=10`; branch update version 2 from version 0 sets `x=20`. Version 3 descends from version 1 but has numeric ID greater than 2. What is `x` at 3?

**Reasoning.** The root-to-3 version path contains 0,1,3, not 2. Modification 2 is incomparable and inapplicable despite its numeric ID. The nearest applicable field change is version 1.

**Conclusion.** `x=10`; full-persistent lookup uses ancestry, not greatest numeric stamp.

### Example 2

**Situation.** A team updates a historical immutable BST root and calls the result “partial persistence with snapshots.”

**Reasoning.** The update base is not restricted to latest. Each new root has one chosen parent; repeated historical updates branch. Queries and updates accept any retained version. Those are full-persistence interface semantics regardless of the word “snapshot.”

**Conclusion.** Classify persistence by permitted operations/version topology, not implementation vocabulary.

### Example 3

**Situation.** Define meld for maps where both operands contain key `k` with unequal values.

**Reasoning.** Physical sharing provides no answer. Choose and document reject, left/right bias, a total deterministic combiner, multi-value result, or a domain three-way reconciliation with base. The policy must specify order, errors, callback effects, and compatibility. Persistence only guarantees both inputs survive and the declared result becomes another version.

**Conclusion.** Confluence requires an abstract multi-input operation; it does not manufacture conflict semantics.

### Example 4

**Situation.** Starting from logical length one, self-concatenate 50 times.

**Reasoning.** Recurrence gives length `2^50=1,125,899,906,842,624`. A rope DAG needs roughly one new concat node per meld, but flattening needs over a quadrillion symbol occurrences. Checked lengths/output quotas must reject or stream only explicitly authorized bounded ranges.

**Conclusion.** Physical compactness does not make full materialization safe.

### Example 5

**Situation.** A serializer uses a global visited set while expanding rope `concat(r,r)`.

**Reasoning.** After visiting the left occurrence of `r`, the global set suppresses the right occurrence, producing half the logical output. For cycle rejection, track nodes active on the current recursion path; after returning from the left, `r` can be visited again on the right. For physical DAG serialization, a visited table is correct only because references preserve multiplicity explicitly.

**Conclusion.** Logical unfolding and physical graph serialization need different visitation semantics.

### Example 6

**Situation.** Build a finite full/confluent version DAG without parallel version edges and query it without flattening large values.

**Reasoning.** Immutable leaf/concat nodes cache exact length. Append from version 0 creates two branches. Ordered meld creates `ABAC`; before each of four self-compositions, a one-parent identity version supplies a distinct second parent. The final version is 11, has length 64 and 32 derivation paths. Indexed character access descends cached lengths; invariants recompute lengths and ensure both data/version edges point backward.

<!-- bijux-verify: {"id":"full-confluent-rope-dag","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"v0=A\nv1=AB\nv2=AC\nv3=ABAC\nv11_length=64\nv11_prefix=ABACABAC\nv11_last=C\nversion_paths=32\neffective_depth=6\nphysical_nodes=10\nold_versions_unchanged=True\nall_invariants=True\nevidence=finite_full_confluent_rope_dag\n","stderr":""}} -->
```python
from dataclasses import dataclass
from math import log2


@dataclass(frozen=True)
class Node:
    text: str | None
    left: int | None
    right: int | None
    length: int


class RopeVersions:
    def __init__(self, initial: str) -> None:
        self.nodes = [Node(initial, None, None, len(initial))]
        self.roots = [0]
        self.parents: list[tuple[int, ...]] = [()]

    def leaf(self, text: str) -> int:
        if not text:
            raise ValueError("empty leaves are excluded")
        self.nodes.append(Node(text, None, None, len(text)))
        return len(self.nodes) - 1

    def concat_roots(self, left: int, right: int) -> int:
        total = self.nodes[left].length + self.nodes[right].length
        self.nodes.append(Node(None, left, right, total))
        return len(self.nodes) - 1

    def append(self, version: int, text: str) -> int:
        root = self.concat_roots(self.roots[version], self.leaf(text))
        self.roots.append(root)
        self.parents.append((version,))
        return len(self.roots) - 1

    def clone(self, version: int) -> int:
        self.roots.append(self.roots[version])
        self.parents.append((version,))
        return len(self.roots) - 1

    def meld(self, left_version: int, right_version: int) -> int:
        root = self.concat_roots(
            self.roots[left_version], self.roots[right_version]
        )
        self.roots.append(root)
        self.parents.append((left_version, right_version))
        return len(self.roots) - 1

    def char_at(self, version: int, index: int) -> str:
        node_id = self.roots[version]
        if not 0 <= index < self.nodes[node_id].length:
            raise IndexError(index)
        while self.nodes[node_id].text is None:
            node = self.nodes[node_id]
            assert node.left is not None and node.right is not None
            left_length = self.nodes[node.left].length
            if index < left_length:
                node_id = node.left
            else:
                index -= left_length
                node_id = node.right
        return self.nodes[node_id].text[index]  # type: ignore[index]

    def materialize(self, version: int, limit: int) -> str:
        length = min(limit, self.nodes[self.roots[version]].length)
        return "".join(self.char_at(version, i) for i in range(length))

    def path_count(self, version: int) -> int:
        counts = [1]
        for current in range(1, version + 1):
            counts.append(sum(counts[parent] for parent in self.parents[current]))
        return counts[version]

    def invariants(self) -> bool:
        for node_id, node in enumerate(self.nodes):
            if node.text is not None:
                if node.left is not None or node.right is not None:
                    return False
                if node.length != len(node.text) or node.length == 0:
                    return False
            else:
                if node.left is None or node.right is None:
                    return False
                if not (node.left < node_id and node.right < node_id):
                    return False
                if node.length != (
                    self.nodes[node.left].length + self.nodes[node.right].length
                ):
                    return False
        return all(
            len(set(parents)) == len(parents)
            and all(parent < version for parent in parents)
            for version, parents in enumerate(self.parents)
        )


history = RopeVersions("A")
v1 = history.append(0, "B")
v2 = history.append(0, "C")
v3 = history.meld(v1, v2)
version = v3
for _ in range(4):
    duplicate = history.clone(version)
    version = history.meld(version, duplicate)
v11 = version

before = [history.materialize(v, 8) for v in range(4)]
paths = history.path_count(v11)
print(f"v0={history.materialize(0, 8)}")
print(f"v1={history.materialize(v1, 8)}")
print(f"v2={history.materialize(v2, 8)}")
print(f"v3={history.materialize(v3, 8)}")
print(f"v11_length={history.nodes[history.roots[v11]].length}")
print(f"v11_prefix={history.materialize(v11, 8)}")
print(f"v11_last={history.char_at(v11, 63)}")
print(f"version_paths={paths}")
print(f"effective_depth={int(1 + log2(paths))}")
print(f"physical_nodes={len(history.nodes)}")
print(f"old_versions_unchanged={before == ['A', 'AB', 'AC', 'ABAC']}")
print(f"all_invariants={history.invariants()}")
print("evidence=finite_full_confluent_rope_dag")
```

The program bounds materialization to eight characters and uses exact Python integers. It demonstrates immutable sharing/version parents only; it does not implement DSST/Fiat–Kaplan transformations, durability, reclamation, concurrency, hostile parsing, or production performance.

**Conclusion.** Branching and normalized self-confluence preserve old roots while compactly representing length 64 with ten physical data nodes in this finite trace.

### Example 7

**Situation.** A disjoint-confluence implementation is asked to meld two versions sharing a common immutable subtree.

**Reasoning.** Immutability makes the abstract meld potentially safe, but the transformation's disjointness precondition is physical node-set separation. Either reject, detach/copy one operand with accounted cost, use a representation-specific meld proved for sharing, or use a general overlapping-confluence method. A content hash indicating equality does not prove disjointness.

**Conclusion.** Semantic safety does not waive a theorem's representation precondition.

### Example 8

**Situation.** A repeated self-meld DAG has longest version depth 20 and `2^20` root-to-final paths.

**Reasoning.** Its effective depth is `1+log2(2^20)=21`. A one-parent chain of depth 20 has one root path, so effective depth one. The quantities describe different structure: ordinary depth is longest dependency latency; effective depth captures reconvergent derivation multiplicity.

**Conclusion.** Record and interpret both depth and path/effective-depth metrics.

### Example 9

**Situation.** Retention removes both explicit operand handles after their meld result is retained.

**Reasoning.** The result root may share all operand data nodes, so those nodes remain live. Policy may delete public handles while keeping parent IDs/provenance, or compact the result and retain a redacted derivation. Reclamation traces retained version roots and required provenance, not handle deletion events alone. Reader/export pins also delay reclamation.

**Conclusion.** DAG reachability and policy—not local reference disappearance—govern lifetime.

### Example 10

**Situation.** An untrusted import declares 1,000 nodes, a final logical length `2^500`, duplicate parents, and one backedge from an old node to the final node.

**Reasoning.** Parse under byte/node/edge limits into quarantine. Stable IDs/parents may be valid and duplicate operands permitted, but topological/cycle validation rejects the data backedge for an acyclic rope. Recompute cached lengths with big/checked integers and enforce logical-size/output/effective-depth policies without allocating `2^500`. Verify checksums/signatures and compatibility before atomic publication.

**Conclusion.** Compact graphs require validation and amplification limits based on both physical and logical structure.

## Cross-Program Connections

- **Database Engineering:** branching snapshots, temporal tables, MVCC ancestry, and mergeable indexes need transaction/isolation semantics beyond generic persistence.
- **Distributed Systems:** multi-parent commits, content-addressed DAGs, causal histories, consensus, and CRDT joins resemble version DAGs but add replicas/failures/algebraic laws.
- **Software Engineering Patterns:** copy-on-write, immutable aggregates, event sourcing, command histories, and three-way merge encode distinct version contracts.
- **Programming Languages:** purity, linear/unique ownership, effects, memoization, and observational equivalence determine whether shared nodes may be updated internally.
- **Security Engineering:** provenance authenticity, cross-tenant merge authorization, amplification bombs, and historical data erasure are first-class graph concerns.
- **Formal Methods:** refinement separates physical sharing from abstract occurrences; ancestry/order structures and meld algebra invite inductive/mechanized proofs.
- **Data Engineering:** lineage DAGs and multi-input transformations need ordered parents, schema compatibility, replay, retention, and bounded materialization.
- **Concurrent Programming:** atomic multi-root publication, pins/epochs, mutable caches, and callback reentrancy determine thread safety.

## References

1. James R. Driscoll, Neil Sarnak, Daniel D. Sleator, and Robert E. Tarjan, [“Making Data Structures Persistent”](https://www.cs.cmu.edu/~sleator/papers/making-data-structures-persistent.pdf), *Journal of Computer and System Sciences* 38(1), 1989, pp. 86–124. Primary full-persistence version-tree, fat-node, and node-splitting results.
2. Daniel D. Sleator, [Persistence bibliography page](https://www.cs.cmu.edu/~sleator/papers/Persistence.htm), Carnegie Mellon University. Author-hosted record and paper access.
3. Amos Fiat and Haim Kaplan, [“Making Data Structures Confluently Persistent”](https://www.cs.tau.ac.il/~haimk/papers/journal2.pdf), *Journal of Algorithms* 48(1), 2003, pp. 16–58. Author-hosted primary paper on general confluence transformations, effective depth, and the lower-bound framework.
4. Haim Kaplan, [publications record](https://www.cs.tau.ac.il/~haimk/pubs.html), Tel Aviv University. Author-maintained bibliographic record for the confluent-persistence paper.
5. Sébastien Collette, John Iacono, and Stefan Langerman, [“Confluent Persistence Revisited”](https://arxiv.org/abs/1104.3045), 2011; SODA 2012. Primary disjoint-confluence transformation result.
6. MIT 6.851, [Lecture 1: Persistence](https://courses.csail.mit.edu/6.851/spring12/lectures/L01.pdf), 2012. Graduate notes on full/confluent persistence, effective depth, and disjoint confluence.
7. MIT 6.851, [Lecture 1 scribe notes](https://courses.csail.mit.edu/6.851/spring12/scribe/lec1.pdf), 2012. Detailed graduate exposition of version trees, node splitting, and confluence.
8. MIT 6.851, [2021 Lecture 1](https://classes.csail.mit.edu/6.851/spring21/lectures/L01.html), current course record and theorem synopsis.

## Exercises

### Exercise 1

Draw the version graph for root 0; unary updates 1 and 2 from 0; unary update 3 from 1; meld 4 from ordered parents `(3,2)`; identity version 5 from 4; and meld 6 from ordered parents `(4,5)`. Classify the graph after each operation, list ancestors of 4, compute root-to-version path counts for all versions, and compute `e(6)`.

### Exercise 2

Prove that the immutable rope rule “allocate a fresh concat node pointing to two already-published acyclic roots and cache their length sum” preserves acyclicity and denotes ordered concatenation, even when both roots are identical. Explain why a global visited set is wrong for logical iteration.

### Exercise 3

A full-persistent fat-field implementation selects the greatest numeric version ID not exceeding the query ID. Construct a minimal counterexample, diagnose the violated invariant, and propose a correct but slow reference algorithm plus tests for an optimized ancestry index.

### Exercise 4

Design confluence for persistent maps shared across tenants. Specify comparator/schema compatibility, duplicate keys, ordered/unordered operands, provenance, authorization, resource limits, publication, retention, and evidence. Compare structure-specific immutable union, copy-and-merge, and a general confluence transformation.

### Exercise 5

Design a durable service for compact expression DAG versions supporting unary rewrites and multi-parent composition. It must survive crashes, concurrent writers/readers, hostile imports, and deletion requests. Specify abstract semantics, handles, graph/storage invariants, transactions, recovery, lifetime, security, verification, and metrics. State changes needed if composition callbacks are nondeterministic or effectful.

## Answers to the Exercises

### Answer 1

Edges are `0->1`, `0->2`, `1->3`, `3->4`, `2->4`, `4->5`, `4->6`, and `5->6`. Through version 3, each nonroot has one parent and the graph is a full-persistence version tree. Version 4 has two parents, so it becomes a confluent version DAG; versions 5 and 6 remain a DAG without parallel edges.

Ancestors of 4 (including itself) are `{0,1,2,3,4}`. Path recurrence gives `paths(0)=1`, `paths(1)=1`, `paths(2)=1`, `paths(3)=1`, `paths(4)=paths(3)+paths(2)=2`, `paths(5)=paths(4)=2`, and `paths(6)=paths(4)+paths(5)=4`. Therefore `e(6)=1+log2(4)=3`. Version 5 is an identity/clone in the abstract value model, but remains a distinct version vertex so self-composition needs no parallel version edge.

### Answer 2

Induct on allocation order. Published leaf/concat roots are acyclic. A new concat node has edges only to already-published older nodes; no older node points to the fresh node, so no directed path can return to it. Thus adding the node cannot create a cycle. Inductively, each child denotes a sequence; define the new abstract sequence as left sequence followed by right sequence. Cached length is their exact sum. Identical children are safe: the root has two edges/occurrences and denotes `X·X`, not `X`.

A global visited set suppresses the second occurrence of a shared node and therefore changes unfolding. Logical iteration can use an active recursion-stack set to detect cycles, removing a node after returning, or an iterative stack that schedules both child edges. Physical serialization may use global deduplication only if it emits both references so the decoder restores occurrence multiplicity.

### Answer 3

Let version 0 store `x=0`. Create version 1 from 0 with `x=1`; create version 2 from 0 with `x=2`; create version 3 from version 1 without changing `x`. Greatest numeric record `<=3` chooses version 2 and returns 2, but version 2 is not an ancestor of 3; correct value is 1.

The violated invariant is that only modifications on the unique root-to-query path apply. A slow oracle walks parents from query to root and returns the first modification of the requested field (or initial value). Tests create sibling/interleaved IDs, deep branches, changes on ancestors/siblings/descendants, no-change nodes, multiple fields, root changes, relabel/rebuild, serialization, and randomized version trees; compare every optimized lookup with the oracle after every insertion.

### Answer 4

Define maps only between operands with identical key comparator/canonicalization and compatible value schema/version. Choose deterministic duplicate-key semantics—such as reject unless equal, or invoke a named versioned pure combiner. Preserve operand order if left/right bias exists; otherwise document commutativity/idempotence and property-test them. Result records ordered parents, operation/policy version, tenant principals, authorizer, input/output digests, and root.

Authorize reading each operand and creating a result in the destination tenant; derive result labels conservatively so merge cannot launder restricted data. Pin operands, estimate logical/physical work, enforce parent count, key count, depth, overlap, memory, CPU/callback, and output quotas, build/validate in staging, durably write nodes/provenance, then atomically publish. Retention traces result/ancestor policy and reader/replica/legal pins; deletion may require rewriting/redaction or key destruction.

Structure-specific immutable union usually gives the clearest map semantics and can exploit ordered/hash structure/sharing. Copy-and-merge is simplest under strict bounded size but duplicates data. A general confluence transformation is justified only when its pointer-model assumptions and complex metadata beat the native design under measured workloads. Evidence includes reference-map comparison for all versions, algebraic tests only for declared laws, conflicting/incompatible/cross-tenant cases, shared/disjoint inputs, rejected-operation noninterference, fault/recovery, hostile callbacks/imports, reclamation, and latency/memory tails.

### Answer 5

Define each version as an immutable abstract expression plus an ordered derivation: unary rewrite has one parent and a specified total/partial rewrite; composition has named arity/order and exact tree/DAG semantics. Handles contain service/tenant, generation, stable version ID, schema/operator-set fingerprint, and authorization context. Physical expression nodes are immutable, acyclic, typed, and carry checked measures; version records name preexisting parents, root, operation/provenance, checksums/signature, and commit state. Parent and child node edges respect topological order.

Writers validate/pin operands, authorize, reserve quotas, evaluate deterministic construction in a bounded staging arena, validate types/acyclicity/measures, write immutable chunks, indexes, and a complete commit record, durably order writes, then atomically publish a unique version ID. Concurrent writers may branch; indexes use transactions/CAS while readers pin immutable roots/epochs. Recovery scans authenticated commits in topological order and accepts only those with complete parents/chunks/checksums, rebuilding indexes and quarantining partial/cyclic records.

Lifetime begins from retained handles, active readers, dependent versions/provenance, exports, replicas, backups, recovery work, and legal holds. Deletion applies policy to data and derivation separately; GC traces both version and data DAGs, and compaction proves retained abstract equality before switching generations. Hostile imports face schema/ID/type/parent/root/cycle/measure/hash/signature validation plus byte/node/edge/arity/depth/path/logical-size/output/CPU/memory/diagnostic quotas without expansion.

Verification includes a small immutable abstract interpreter for every version, randomized unary/multi-parent histories, repeat/overlap/incompatibility cases, algebraic properties where declared, model-checked publication failures, crash recovery at each write boundary, concurrent pin/GC stress, malformed imports/amplification, compaction/deletion equivalence, and metrics for physical/logical size, overlap, version depth/path estimates, query/rewrite/meld tails, allocations, GC, publication, recovery, and rejected work.

Nondeterministic/effectful callbacks require recording enough inputs, callback identity/version, outputs, external effects, and idempotency tokens to replay/recover—or they must run before staging and their returned value become immutable input. Sandbox and bound them; never reexecute blindly during recovery. If deterministic refinement and atomic effect coordination cannot be specified, the service must reject such callbacks because persistent replay/provenance claims would be false.
