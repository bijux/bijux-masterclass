---
module_id: DSE-093
program: Data Structures Engineering
level: 2
module_number: 93
title: Succinct Trees and Graphs
status: complete
last_verified: 2026-08-30
---

# Succinct Trees and Graphs

## One-Page Review

### Governing question

How can tree topology and selected graph families be encoded near their information-theoretic baselines while retaining navigation, adjacency, and neighborhood operations under explicit models?

### Essential definitions

An *ordinal tree* is rooted and its children are ordered. The number of such trees on (n) nodes is the Catalan number (C_{n-1}), whose logarithm is $2n-O(\log n)$ bits. Balanced-parentheses (BP) encodes a preorder visit with `(` on entry and `)` on exit, using exactly (2n) topology bits. Rank/select, excess, matching, enclosing, and range-minimum/search supports add (o(n)) bits in static word-RAM results.

LOUDS lists nodes in breadth-first order and writes each node degree in unary, commonly (1^{d(v)}0), again totaling (2n-1) bits for a nonempty tree because degrees sum to (n-1). DFUDS is a depth-first unary-degree alternative. Each encoding favors different formulas/layouts and requires a declared bit convention.

General graphs do not have one universal two-bits-per-vertex representation. An undirected labeled simple graph with (n) vertices and (m) edges has baseline

$$
\log_2\binom{\binom n2}{m}
$$

bits for its edge set. Directed, labeled, multigraph, planar, web, geometric, and dynamic graph classes have different baselines and supported-operation trade-offs.

### Central model, mechanism, or theorem

In BP, define excess before position (i) as opens minus closes in prefix ([0,i)). An opening parenthesis represents a node; its matching close delimits exactly its subtree. Parent is the nearest enclosing open; first child is the next position when it opens; next sibling begins immediately after the node's close when that position opens. Succinct indexes implement matching/enclosing and excess searches without scanning.

Static ordinal trees can support a rich navigation interface in (2n+o(n)) bits with constant-time operations on a stated word RAM. Dynamic results use additional redundancy and polylogarithmic time. Graph succinctness requires choosing a graph class and operation set: degree/neighborhood may be easy in a compressed adjacency layout while constant-time arbitrary adjacency needs more indexing.

### Critical invariants

- Tree kind—binary, ordinal, labeled, forest—and node identity order are versioned.
- BP is balanced: prefix excess never becomes negative and final excess is zero.
- Each node maps to exactly one open; matching pairs are nested and cover exactly (2n) bits.
- Labels/payload arrays use the same preorder, breadth-first, or other node order as topology.
- Rank/select/excess supports share the topology's bit convention and immutable generation.
- Graph vertex namespace, direction, loop/parallel-edge policy, edge order, and label schemas are explicit.
- Graph encoding preserves exact edge multiplicity/attributes promised by the contract and bounds every decoded neighbor.
- Space claims name their information baseline and include auxiliary indexes, metadata, and construction peak separately.

### Common failures

Failures include counting labels as topology, mixing BP and LOUDS node orders, using inclusive rank in half-open formulas, accepting a balanced total with a negative prefix, confusing number of descendants with subtree parentheses length, serializing native pointers, claiming (2n) bits for arbitrary graphs, omitting vertex labels/direction/attributes from the baseline, sorting adjacency without permuting edge payloads, deduplicating parallel edges silently, applying planar bounds to nonplanar input, and mutating static supports in place.

### Compact example

A seven-node ordinal tree has preorder A/B/E/F/C/D/G and BP `((()())()(()))`. Matching pairs are A 0–13, B 1–6, E 2–3, F 4–5, C 7–8, D 9–12, G 10–11. The close-open span gives subtree sizes 7/3/1/1/1/2/1; stack-derived parents and children reproduce six edges. The bounded model verifies balance, matches, depths, preorder labels, subtree sizes, and a topology round trip.

### Connections

[DSE-091](091-bit-vectors-with-rank-and-select.md) supplies rank/select; [DSE-092](092-wavelet-trees.md) shows recursive coordinate navigation. The roadmap successor is [DSE-094, “Compressed Suffix Arrays”](../ROADMAP.md), whose suffix-tree relatives depend on succinct topology. Database tries, XML/JSON trees, compiler ASTs, RDF/web graphs, and compressed graph analytics all use these choices.

## Governing Question

How should a succinct tree or graph representation define its object class, lower bound, navigation API, labels, construction, serialization, updates, and verification so “succinct” is a reproducible claim rather than a synonym for compressed?

## Why This Matters

Pointer-rich trees often spend several machine words per node before labels. Graph adjacency objects add allocations, headers, and duplicated IDs. When topology is static and queried heavily, bit encodings reduce memory traffic as well as capacity. Rank/select and range-min/max supports recover navigation without reconstructing pointers.

But the topology alone is rarely the whole product. Node labels, edge attributes, vertex dictionaries, ordering permutations, indexes, checksums, and mutable overlays can dominate. Tree results do not transfer automatically to arbitrary graphs. Engineering begins by fixing the mathematical object and required operations.

## Prerequisites and Retrieval

Retrieve:

- rooted ordered trees, preorder/postorder/breadth-first order, degree, depth, ancestor, subtree, and lowest common ancestor;
- [bit-vector rank/select](091-bit-vectors-with-rank-and-select.md), prefix sums, excess, range minima, forward/backward search, and matching parentheses;
- Catalan numbers, binomial coefficients, information lower bounds, little-(o), and word-RAM assumptions;
- directed/undirected graphs, loops, parallel edges, adjacency/neighborhood/degree, planar and sparse graph classes;
- packed serialization, checked offsets, immutable generations, checksums, and differential/property testing.

The term “node number” is meaningless until its traversal order is declared. A payload array keyed by preorder cannot be joined directly with LOUDS breadth-first node IDs.

## Learning Objectives

After this chapter, you should be able to:

1. derive and validate BP, LOUDS, and null-marker topology encodings;
2. express parent/child/sibling/subtree/depth navigation through matching and excess primitives;
3. explain (2n+o(n)) static ordinal-tree results and their word-RAM qualifications;
4. choose an information baseline for labeled, directed, sparse, planar, or arbitrary graphs;
5. design topology/label/attribute ordering, construction, serialization, update, and mapping invariants;
6. reject cross-encoding formulas, corrupt topology, unsupported graph classes, and misleading space claims;
7. verify navigation/adjacency against pointer and edge-list oracles and report full footprint/performance.

## Core Exposition

### Information baselines

For rooted ordered trees with (n) nodes, Catalan growth yields about (2n) unavoidable topology bits. BP's (2n) bits are therefore near optimal even before auxiliary support. The label array is separate: labels from alphabet (Sigma) can require $n\log\sigma$ bits absent compression, and arbitrary payloads may dominate.

A binary-tree null-marker preorder emits one bit for each real node and one for each null child: (n+(n+1)=2n+1) bits. It preserves left/right distinction. Ordinal-tree BP preserves ordered variable-degree structure. Converting between them changes node semantics and must preserve labels under a declared traversal.

For an undirected labeled simple graph, there are $N=\binom n2$ possible edges and (inom Nm) edge sets of size (m). That is only the topology baseline for known vertex labels and exactly (m) edges. Directed graphs have up to (n(n-1)) loop-free arcs; loops and multiedges alter the universe; unlabeled graphs have isomorphism complications. Compression relative to observed regularity is not the same as worst-case succinctness.

### Balanced-parentheses encoding

During preorder DFS, emit open at node entry, recursively encode children left-to-right, then emit close. The result is balanced. Define $operatorname{excess}(i)=\operatorname{rank}_{(}(i)-\operatorname{rank}_{)}(i)$ before position (i). At a node's open position (p), excess equals its depth; after reading the open it is depth plus one.

The matching close is the first later position after which excess returns to its value at (p). The subtree interval is the matching parenthesis pair; because each node contributes a pair,

$$
\operatorname{subtree\_size}(p)=\frac{\operatorname{close}(p)-p+1}{2}.
$$

The first child exists when (p+1) is open. After child (u), a next sibling exists when (operatorname{close}(u)+1) is open before the parent's close. Parent is the nearest open whose match encloses (p). Succinct supports reduce these scans to rank/select, forward/backward excess search, range min/max, and lowest-excess queries.

Preorder number of an open at (p) is (operatorname{rank}_{(}(p)) under zero-based half-open rank. Postorder follows close rank. Depth, ancestor tests, degree, child-by-rank, subtree rank/select, level ancestor, and LCA can be reduced to the supported primitives, but exact formulas depend on conventions and the chosen support interface.

### LOUDS and DFUDS

LOUDS enumerates nodes breadth first and writes (d(v)) one-bits followed by zero for each node. Across the tree, one-bits total (n-1) and zeros (n). Runs of children correspond to unary degree fields; rank/select translate a node ordinal to its degree range and child ordinals. Some definitions prepend a sentinel or swap zeros/ones, changing formulas. Persist the exact variant.

LOUDS places nodes from the same level together and supports compact tries with contiguous label arrays. BP places subtrees contiguously and makes DFS/subtree operations natural. DFUDS writes degrees in depth-first order and supports another family of navigation reductions. No bitstring should be interpreted without encoding kind, sentinel, and node-number order.

Tree coverings and range min-max trees add small macro/micro summaries over BP. Microtree tables answer local operations; macro summaries jump across blocks. They realize lower-order redundancy and fast navigation but complicate finite layout, construction, and portability.

### Labels and attributes

Topology encodes no application label. Store node labels in the topology's node order, or store a permutation mapping. Edge labels in an ordinal tree can align with nonroot nodes if each node has one parent edge; general graphs need edge IDs and adjacency-occurrence ownership. Sorting neighbors for compression must reorder edge attributes identically.

Repeated labels may use wavelet trees, dictionaries, or compressed strings. Path labels in tries may use LOUDS plus edge-character arrays; path compression adds skip lengths and suffix storage. State whether navigation returns topology ordinal, stable external ID, or application record.

### Succinct graph design

An adjacency-array baseline stores offsets plus neighbor IDs. Gap coding, reference encoding, run/interval encoding, grammar compression, and k²-style recursive matrices exploit locality or similarity. These may be excellent compressed graph representations without matching the arbitrary-graph information bound or constant-time adjacency.

Operation sets conflict. Sorted compressed lists enumerate neighbors well but adjacency may decode/search a list. Bit matrices answer adjacency directly but cost (n^2) bits. Extra dictionaries or sampling accelerate membership. Farzan–Munro-style results analyze which sparse/dense regimes can reach information bounds with constant-time degree, adjacency, and output-sensitive neighborhood under model assumptions; do not attribute those guarantees to a generic gap-coded file.

Restricted classes permit stronger baselines. Planar graphs have (O(n)) edges and specialized encodings; trees are a subclass; bounded-degree, interval, geometric, and web graphs each expose structure. A validator must confirm class membership before relying on its encoding theorem.

### Construction, updates, and persistence

BP construction is streaming with a DFS stack; LOUDS uses a queue. Detect cycles/shared children when input promises a tree, validate exactly one root and parent per nonroot, and bind labels during traversal. For huge graphs, canonicalize vertex IDs and edge policy before compressing; external sorts must keep attributes and duplicate semantics.

Static succinct supports are generation-bound. Inserting a node shifts topology bits and ordinals; dynamic succinct trees use dynamic bit sequences and min/max summaries with polylogarithmic operations and higher constants. Immutable base plus mutable delta is often simpler, but queries and compaction must define identity, deletion, and ordering.

A durable envelope contains object/graph class, (n,m), root, direction/loop/multiedge rules, topology encoding and convention, node/edge order, label schemas/dictionaries, bit order, supports, offsets, counter widths, section checksums, source snapshot, and generation. Write private sections, validate, flush, then publish one manifest/root atomically.

Checked arithmetic prevents corrupt offsets and degree sums from escaping mapped sections. Validate BP prefix/final excess, LOUDS totals/degree sum, node/edge IDs, adjacency symmetry where promised, sortedness/duplicates, planar/class certificate where used, label-array cardinalities, and sampled oracle operations before publication.

### Verification and performance

Build a pointer-tree oracle and canonical edge-list oracle. For every tree node compare parent, children/order, depth, subtree, ancestors, preorder/postorder, degree, and LCA. Exhaust all small ordinal trees or generated Catalan shapes, plus chains, stars, complete/high-degree trees, empty forest policy, and maximum-depth inputs.

For graphs compare degree, adjacency, and full neighbor multiset under direction/loop/parallel-edge rules. Test isolated vertices, self-loops, duplicates, reciprocal mismatches, dense/sparse extremes, adversarial gaps, high degree, ID remaps, attribute joins, truncation, and corruption. Round-trip independent decoders.

Benchmark operations by depth/degree/list length, random and traversal-local queries, cold/warm mapping, cache/NUMA, construction peak, update overlay, and serialization. Report topology bits, auxiliary supports, labels, dictionaries, attributes, alignment, file/RSS bytes, build scratch, and latency distributions against pointer/CSR baselines.

The bounded model below parses fixed BP with a stack. Its dictionaries are not succinct and matching is precomputed; it demonstrates semantics, balance, traversal order, and subtree accounting rather than constant-time (2n+o(n)) support.

<!-- bijux-verify: {"id":"balanced-parentheses-tree","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"nodes=7\nbits=((()())()(()))\nopens=[0, 1, 2, 4, 7, 9, 10]\nmatches=[(0, 13), (1, 6), (2, 3), (4, 5), (7, 8), (9, 12), (10, 11)]\npreorder=['A', 'B', 'E', 'F', 'C', 'D', 'G']\nparents={'A': None, 'B': 'A', 'E': 'B', 'F': 'B', 'C': 'A', 'D': 'A', 'G': 'D'}\nchildren={'A': ['B', 'C', 'D'], 'B': ['E', 'F'], 'E': [], 'F': [], 'C': [], 'D': ['G'], 'G': []}\ndepths={'A': 0, 'B': 1, 'E': 2, 'F': 2, 'C': 1, 'D': 1, 'G': 2}\nsubtree_sizes={'A': 7, 'B': 3, 'E': 1, 'F': 1, 'C': 1, 'D': 2, 'G': 1}\nedges=6\nbalanced=True\nroundtrip=True\nvalid=True\nevidence=bounded_parentheses_tree_model\n","stderr":""}} -->
```python
BITS = "((()())()(()))"
LABELS = ["A", "B", "E", "F", "C", "D", "G"]

stack = []
open_positions = []
matching = {}
parent_open = {}
balanced = True

for position, symbol in enumerate(BITS):
    if symbol == "(":
        open_positions.append(position)
        parent_open[position] = stack[-1] if stack else None
        stack.append(position)
    elif stack:
        opening = stack.pop()
        matching[opening] = position
    else:
        balanced = False

balanced = balanced and not stack and len(matching) == len(LABELS)
label_at_open = {
    position: LABELS[index]
    for index, position in enumerate(open_positions)
}
parents = {
    label_at_open[position]: (
        label_at_open[parent_open[position]]
        if parent_open[position] is not None
        else None
    )
    for position in open_positions
}
children = {label: [] for label in LABELS}
for child, parent in parents.items():
    if parent is not None:
        children[parent].append(child)

depths = {}
for label in LABELS:
    depth = 0
    parent = parents[label]
    while parent is not None:
        depth += 1
        parent = parents[parent]
    depths[label] = depth

subtree_sizes = {
    label_at_open[position]: (matching[position] - position + 1) // 2
    for position in open_positions
}
matches = [
    (position, matching[position])
    for position in open_positions
]
roundtrip = "".join(
    "(" if position in matching else ")"
    for position in range(len(BITS))
) == BITS
valid = (
    balanced
    and len(open_positions) == 7
    and sum(len(values) for values in children.values()) == 6
    and subtree_sizes == {
        "A": 7,
        "B": 3,
        "E": 1,
        "F": 1,
        "C": 1,
        "D": 2,
        "G": 1,
    }
    and roundtrip
)

print(f"nodes={len(LABELS)}")
print(f"bits={BITS}")
print(f"opens={open_positions}")
print(f"matches={matches}")
print(f"preorder={LABELS}")
print(f"parents={parents}")
print(f"children={children}")
print(f"depths={depths}")
print(f"subtree_sizes={subtree_sizes}")
print(f"edges={sum(len(values) for values in children.values())}")
print(f"balanced={balanced}")
print(f"roundtrip={roundtrip}")
print(f"valid={valid}")
print("evidence=bounded_parentheses_tree_model")
```

## Definitions and Notation

- **Ordinal tree:** rooted tree with ordered children.
- **BP:** preorder open-on-entry/close-on-exit topology string.
- **LOUDS:** breadth-first unary degree sequence, here (1^{d(v)}0) without sentinel.
- **DFUDS:** depth-first unary degree sequence.
- (operatorname{excess}(i)): opens minus closes before bit position (i).
- **Match/enclose:** paired parenthesis and nearest strictly containing pair.
- **Topology ordinal:** node ID induced by preorder, postorder, breadth-first, or another declared order.
- (n,m): graph vertex and edge/arc counts under a declared graph model.
- **Adjacency query:** whether a specified edge exists; **neighborhood query:** enumeration of incident/outgoing neighbors.
- **Redundancy:** bits beyond a named information-theoretic topology baseline.
- **Generation:** atomic topology, ordering, labels/attributes, supports, and checksums.

## Mechanisms, Invariants, or Proof Structure

### BP navigation proof

DFS nesting makes a node's matching close occur after exactly all descendant pairs. Hence the pair span is twice subtree size. Opens whose matches strictly contain another open are its ancestors; the innermost is its parent. Prefix excess at an open is depth.

### Succinct-support argument

The raw BP payload is (2n) bits, within a lower-order term of the Catalan topology bound. Rank/select plus range min-max/micro-macro summaries can implement matching, enclosing, excess search, and derived navigation in (o(n)) auxiliary bits and constant time for static word-RAM formulations. This statement does not cover labels or every implementation.

### Graph-accounting invariant

Encoding and oracle agree on vertex namespace, direction, loops, parallel edges, and attributes. Degree sums equal (2m) for undirected loop-free graphs or (m) separately for directed out/in degrees. Every decoded adjacency occurrence is bounded and all reordering permutations apply identically to attributes.

## Alternatives and Trade-Offs

Pointers favor mutation and direct payload objects. BP favors depth/subtree operations; LOUDS favors breadth-first tries; DFUDS and tree coverings provide other navigation/engineering points; null markers preserve binary left/right structure. Dynamic succinct trees trade time and redundancy for edits.

CSR is a durable graph baseline. Gap/reference/run compression favors neighbor scans; bit matrices favor adjacency; WebGraph exploits similar consecutive lists; k²-trees exploit empty clustered matrix regions; specialized planar or sparse succinct encodings target class-specific lower bounds. Choose after fixing exact graph semantics and operations.

## Failure Modes and Misconceptions

- Final excess zero alone does not prove BP; no prefix may be negative.
- Matching parentheses by nearest close ignores nested descendants.
- BP preorder and LOUDS breadth-first ordinals differ.
- LOUDS sentinel/bit variants change every rank/select formula.
- Tree labels and edge payloads are not included in (2n) topology bits.
- Static supports become stale after insertion or bit mutation.
- An arbitrary graph is not a tree plus a few extra edges under the tree bound.
- Directed arcs, loops, and parallel edges change both baseline and degree laws.
- Sorting neighbors without attributes corrupts edge identity.
- Compression ratio on one web ordering is not an arbitrary-graph succinct theorem.
- Planar/class-specific encodings require validated membership.
- Successful mapping does not prove topology, offset, or support semantics.

## Worked Examples

### Example 1

**Finite lower bound.** Seven-node ordinal-tree shapes number (C_6=132), requiring at least $lceil\log_2 132\rceil=8$ bits for a fixed-length code; BP uses 14. **Conclusion:** (2n+o(n)) is asymptotic, not finite optimality for every (n).

### Example 2

**Subtree span.** B opens at 1 and closes at 6, so its subtree has ((6-1+1)/2=3) nodes: B/E/F. **Conclusion:** balanced nesting makes subtree size local.

### Example 3

**Depth.** Before G's open at 10, two opens remain unmatched, so depth is two. **Conclusion:** prefix excess represents ancestor count.

### Example 4

**LOUDS totals.** The fixture degrees are 3,2,0,1,0,0,0 in breadth-first node order; unary fields contain six ones and seven zeros, 13 bits. **Conclusion:** degree sum proves the (2n-1) raw length.

### Example 5

**Order mismatch.** Preorder labels A/B/E/F/C/D/G attached to LOUDS ordinals label nodes incorrectly because breadth-first is A/B/C/D/E/F/G. **Conclusion:** persist or transform node order.

### Example 6

**Graph baseline.** For eight labeled vertices and five undirected simple edges, there are (inom{28}{5}=98{,}280) edge sets, requiring 17 fixed-length bits. **Conclusion:** the baseline depends jointly on (n,m), not only vertices.

### Example 7

**Direction.** One stored pair `(u,v)` in an undirected graph contributes to both neighborhoods; in a directed graph it contributes once to out-degree and once to in-degree. **Conclusion:** one degree-sum validator cannot serve both silently.

### Example 8

**k² region.** A large all-zero adjacency quadrant becomes one zero branch instead of materialized cells. Randomly scattered edges remove that advantage. **Conclusion:** matrix clustering drives compression.

### Example 9

**Reference compression.** Consecutive web pages share many outgoing links, so one adjacency list can reference a predecessor plus edits. An adversarial vertex ordering destroys similarity. **Conclusion:** ordering is part of empirical evidence.

### Example 10

**Tree edit.** Inserting a first child after B's open shifts later BP positions and rank/excess summaries. An immutable new generation or dynamic support is required. **Conclusion:** topology bit insertion is not a local pointer edit.

## Cross-Program Connections

- **Databases:** succinct tries, XML/JSON navigation, dictionary indexes, and RDF relations separate topology from payloads.
- **Compilers:** immutable AST topology can use preorder labels and subtree intervals.
- **Information Retrieval:** suffix trees, document trees, and web graphs combine compressed navigation and labels.
- **Graph Engineering:** CSR, WebGraph, k²-trees, planar encodings, and dynamic overlays serve different operations/classes.
- **Systems:** checked mapped sections, bit conventions, traversal ordinals, crash publication, and cache locality govern safety.
- **Theory:** Catalan/binomial baselines and word-RAM/cell-probe results delimit truthful succinctness claims.

## References

1. Guy Jacobson, [Succinct Static Data Structures](https://csd.cs.cmu.edu/academics/doctoral/degrees-conferred/guy-jacobson), Carnegie Mellon University, 1988.
2. J. Ian Munro and Venkatesh Raman, [Succinct Representation of Balanced Parentheses and Static Trees](https://dblp.org/rec/journals/siamcomp/MunroR01.html), *SIAM Journal on Computing*, 2001.
3. Gonzalo Navarro and Kunihiko Sadakane, [Fully-Functional Static and Dynamic Succinct Trees](https://arxiv.org/abs/0905.0768), *ACM Transactions on Algorithms*, 2014.
4. Joshimar Cordova and Gonzalo Navarro, [Simple and Efficient Fully-Functional Succinct Trees](https://arxiv.org/abs/1601.06939), 2016.
5. Arash Farzan and J. Ian Munro, [Succinct Representations of Arbitrary Graphs](https://dblp.org/rec/conf/esa/FarzanM08.html), *ESA*, 2008.
6. Paolo Boldi and Sebastiano Vigna, [The WebGraph Framework I: Compression Techniques](https://vigna.di.unimi.it/ftp/papers/p595-boldi.pdf), *WWW*, 2004.
7. Nieves Brisaboa, Susana Ladra, and Gonzalo Navarro, [k²-tree Project and Publications](https://lbd.udc.es/research/k2tree/), accessed 2026-08-30.

## Exercises

### Exercise 1

For the fixture tree, derive BP, LOUDS under this chapter's convention, both node orders, matches, parents, depths, degrees, and subtree sizes.

### Exercise 2

Prove the BP subtree-span, parent-enclosure, depth-excess, and preorder-rank properties. State the support primitives needed for fast implementation.

### Exercise 3

For a labeled loop-free undirected graph with (n=100,m=200), state the information baseline and compare required semantics/validation with a directed multigraph.

### Exercise 4

Choose representations for an immutable XML tree, mutable trie, web crawl, clustered sparse binary relation, and dense small graph. Define workload evidence.

### Exercise 5

Design a portable topology/graph file envelope, construction pipeline, atomic publication, corruption validation, and differential test suite.

## Answers to the Exercises

### Answer 1

BP is `((()())()(()))` with preorder A/B/E/F/C/D/G and pairs shown in the model. Breadth-first order is A/B/C/D/E/F/G; degrees there are 3/2/0/1/0/0/0, so LOUDS is `1110 110 0 10 0 0 0` without spaces. Parents, depths, and subtrees are A:none/0/7; B:A/1/3; E:B/2/1; F:B/2/1; C:A/1/1; D:A/1/2; G:D/2/1. The two orders require a permutation for shared labels.

### Answer 2

DFS emits every descendant pair strictly between a node's open and matching close, so span divided by two is subtree size. Proper nesting makes ancestors exactly containing pairs and parent the innermost. Unmatched opens before a node equal ancestors, hence excess equals depth. Opens appear in preorder, so half-open open-rank gives zero-based preorder ordinal. Fast implementations need open/close rank/select, match/find-close, enclose, forward/backward excess search, and range-minimum/min-count/select primitives or equivalent micro/macro supports.

### Answer 3

There are $N=\binom{100}{2}=4{,}950$ possible edges and baseline $log_2\binom{4{,}950}{200}$ bits, rounded up for fixed-length storage. This assumes known labeled vertices, simple undirected topology, no loops, and exactly 200 edges. A directed multigraph needs ordered endpoints, loop policy, multiplicities, edge identities/order, and attribute rules; the simple-edge binomial universe and (2m) degree law no longer apply. Validators must compare exact neighbor multisets and in/out degrees.

### Answer 4

Use static BP plus label arrays for subtree-heavy immutable XML; a dynamic LOUDS/chunk tree or immutable trie segments plus delta for mutation; WebGraph-style reference/gap compression for crawl successor scans; k²-tree for clustered sparse matrix queries in both dimensions; and a bit matrix for a dense small graph needing constant adjacency. Benchmark full bytes/build peak, navigation/adjacency/neighborhood/range operations, ordering sensitivity, cache/mapping, updates, and exact round-trip semantics against pointer/CSR baselines.

### Answer 5

Bind schema, object class, counts, root, direction/loop/multiedge rules, topology encoding/variant, node/edge order and permutations, labels/attributes, bit order, supports, section bounds, widths, source snapshot, and checksums. Canonicalize and validate input before streaming BP/LOUDS or graph compression; keep attributes aligned; write private sections; verify balance, degree sums, edge semantics, sampled/exhaustive oracle operations, and checksums; flush then atomically publish one manifest. Fuzz truncation, offsets, negative BP prefixes, invalid matches, degree overflow, duplicate/asymmetric edges, label cardinalities, crash points, cross-platform readers, and round trips.
