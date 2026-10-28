---
module_id: DSE-048
program: Data Structures Engineering
level: 1
module_number: 48
title: Suffix Trees
status: complete
last_verified: 2026-08-30
---

# Suffix Trees

## One-Page Review

### Governing question

How can every suffix of one text be represented as a compact radix tree whose edges reference the original text, while preserving linear-size structure, correct substring queries, safe construction, and generation-bound persistence?

### Essential definitions

- A **suffix trie** inserts every suffix symbol by symbol and can require quadratic nodes.
- A **suffix tree** is the path-compressed trie of all suffixes of a text, normally terminated by one unique sentinel.
- An **edge label** is represented by a half-open text interval `[start,end)` rather than copied characters.
- The **string depth** of a node is the total number of symbols on its root path.
- A **leaf label** records the starting position of the suffix spelled by its root path.
- An **explicit node** is materialized at a branch or suffix end; an **implicit position** lies inside an edge.
- A **suffix link** from an internal node spelling `aX` points to the node/position spelling `X` under the construction's convention.
- In Ukkonen-style construction, an **active point** records active node, edge, and matched length for the current extension.
- A **remainder** counts suffix extensions still requiring resolution in the current phase.
- An **open leaf end** is a shared mutable phase endpoint that extends many leaf edges without visiting them individually.

### Central model, mechanism, or theorem

Append a sentinel not occurring in the text and ordered under the declared alphabet. Every suffix then ends uniquely at a leaf, so no suffix is a prefix of another. Each internal nonroot node has at least two children. With `n` leaves, there are at most `n-1` internal nodes and fewer than `2n` total nodes; interval labels make total representation linear even though the spelled edge-label characters across suffixes are quadratic if copied.

Substring search consumes a pattern along edge labels. A mismatch means absent; finishing at a node or inside a matching edge means present. All descendant leaf labels are occurrence positions, including overlaps. Search compares at most `|P|` symbols plus transition-selection costs; reporting `k` occurrences adds `Theta(k)`.

Online linear-time construction is more subtle. Ukkonen processes text phases while suffix links, an active point, skip/count traversal, implicit endpoints, and shared leaf ends avoid restarting and extending every suffix. The linear bound assumes constant-time alphabet transitions (or accounts for their cost) and a precise model. A naïve compressed insertion remains a valuable finite oracle, not a scalable substitute.

### Critical invariants

1. Text encoding, coordinate unit, canonicalization, sentinel identity/order, and indexed generation are explicit and immutable.
2. Every edge interval is nonempty, within the same text generation, and siblings begin with distinct symbols.
3. Concatenated root-to-leaf labels equal exactly one complete sentinel-terminated suffix; leaf starts form a permutation of all indexed suffix starts.
4. Every nonroot internal node has at least two children; leaves have no children and valid suffix starts.
5. Parent/child ownership is acyclic and all owned nodes are reachable once unless immutable sharing is explicitly supported.
6. Node string depth equals parent depth plus edge length; cached leaf ranges/counts and suffix-array order agree.
7. Suffix links target the correct proper-suffix string under the implementation's root/implicit-node convention.
8. Active point is canonical: active length is within the selected edge and skip/count normalization has been applied.
9. Open leaf endpoints, phase position, remainder, and pending internal suffix links never expose invalid ranges or partial topology.
10. Queries, handles, serialized offsets, and auxiliary indexes bind to the same immutable text/tree generation.

### Common failures

- Copying edge-label substrings and claiming linear memory.
- Omitting the unique sentinel and then assuming every suffix ends at a leaf.
- Returning only when a pattern ends at a node, missing patterns that end inside edges.
- Reporting a leaf's lexicographic traversal rank instead of its suffix start.
- Losing overlapping matches.
- Splitting an edge without preserving its old child interval and parent relation.
- Updating a shared leaf end beyond the indexed text boundary or persisting it as an unresolved pointer.
- Creating a suffix link to a node whose path label is not the required suffix.
- Applying skip/count with active length larger than the edge and failing to normalize repeatedly.
- Treating Ukkonen's high-level theorem as validation of a particular implementation.

### Compact example

For `banana$`, the compact suffix tree has seven leaves and eleven nodes in one canonical representation. Root edges begin `$`, `a`, `b`, and `n`; the `b` edge label is `banana$`, while the visible root-edge strings are `$`, `a`, `banana$`, and `na`. Pattern `ana` ends at an internal node and returns positions 1 and 3. Pattern `nan` ends inside edge `na$` below root path `na` and returns position 2. The deepest internal string is `ana`, the longest repeated substring. Lexicographic leaf traversal yields suffix array `[6,5,3,1,0,4,2]`.

### Connections

[DSE-044](044-tries.md) and [DSE-045](045-compressed-and-radix-tries.md) establish sequence identity, edge splitting, and compact radix invariants. [DSE-047](047-suffix-arrays.md) supplies suffix order, LCP, BWT, and an array-based alternative. [DSE-005](005-contiguous-and-linked-layouts.md), [DSE-006](006-memory-locality-and-cache-behavior.md), and [DSE-008](008-iterators-and-traversal-protocols.md) supply ownership, locality, and traversal lifetime. The [program roadmap](../ROADMAP.md) continues with suffix automata and graph traversal.

## Governing Question

Which text and sentinel semantics, edge-interval representation, child container, construction algorithm, suffix-link convention, query/occurrence API, memory layout, and snapshot/persistence boundary justify a suffix tree over a suffix array or another string index?

## Why This Matters

Suffix trees make every substring a path prefix. Exact substring search reads the pattern once, then descendant leaves identify occurrences. Internal-node depths expose repetitions. Trees across multiple strings support longest-common-substring and document queries. The structure is algorithmically rich and historically central to linear-time string processing.

It is also easy to implement incorrectly and expensive in practice. A textbook picture hides child maps, nodes, parent/suffix links, intervals, object and allocator headers, alignment, leaf labels, cached ranges, and the original text that all intervals borrow. A suffix array often uses several flat integer arrays and wins in locality and memory even if both have linear asymptotic space.

Construction is the main difficulty. Inserting all suffixes into a compressed radix tree compares repeated prefixes and can be quadratic; expanding a suffix trie is quadratic space. Ukkonen's online algorithm achieves linear time through a web of invariants: implicit suffix tree phases, active points, suffix links, Rule 3 early termination, skip/count, and shared leaf endpoints. A one-off indexing system may safely use a verified library or suffix-array pipeline rather than own this complexity.

Text identity is inseparable from the tree. Edge intervals borrow one exact encoded text. Normalization, Unicode coordinate mapping, sentinel, document separators, and mutation must be finalized first. A search result is a position in that generation, not a stable position in an edited document.

## Prerequisites and Retrieval

Retrieve representation/operation invariants from [DSE-002](002-representation-invariants.md) and [DSE-003](003-operation-contracts.md), allocation and byte costs from [DSE-004](004-time-space-and-allocation-cost.md), locality from [DSE-006](006-memory-locality-and-cache-behavior.md), and property testing from [DSE-009](009-property-based-testing-of-data-structures.md). Retrieve trie identity and substring units from [DSE-044](044-tries.md), radix split/merge and label ownership from [DSE-045](045-compressed-and-radix-tries.md), and suffix/sentinel/LCP/BWT foundations from [DSE-047](047-suffix-arrays.md).

## Learning Objectives

After completing this module, you should be able to:

1. define suffix-tree text, sentinel, suffix, edge interval, explicit/implicit position, and leaf coordinates;
2. prove linear node count for a sentinel-terminated compact suffix trie;
3. implement and validate pattern traversal that may finish inside an edge;
4. derive occurrence, longest-repeat, suffix-array, and LCP relationships;
5. explain naïve compressed construction and why it is not linear;
6. state Ukkonen phases, extensions, active point, suffix links, Rule 3, skip/count, and open-leaf roles;
7. choose child/edge/node layouts and calculate concrete and peak memory;
8. specify immutable generation, concurrency, handle, and reclamation behavior;
9. validate a versioned persistent tree against authoritative text and suffixes; and
10. build reference, exhaustive, construction-state, fault, parser, and workload evidence.

## Core Exposition

**Define the indexed sequence first.** Let indexed text `T` have length `n` including a unique terminal symbol `$` that occurs only at `n-1`. This module indexes nonempty suffixes starting at `0..n-1`; the empty suffix at `n` is excluded. `$` is ordered below all ordinary symbols for lexicographic examples, although basic substring-tree topology needs uniqueness more than a particular order.

Use bytes, code points, tokens, or another fixed symbol sequence consistently. UTF-8 byte intervals return byte positions and can cut user-visible boundaries if patterns are not validated. If indexing normalized code points while returning original spans, persist a mapping. Never put pointers into a mutable string buffer beneath edges; edge intervals become wrong after insertion, deletion, reallocation, or normalization change.

For multiple documents, concatenate with separators that cannot occur in content and prevent matches from crossing boundaries. A single shared sentinel at the very end does not stop a substring from spanning document boundaries. Use distinct terminators or boundary-aware query/leaf metadata according to the generalized suffix-tree design. Document/tenant authorization is part of reporting leaves.

**Compact all unary nonterminal paths.** Begin conceptually with a trie of every suffix. A sentinel ensures each suffix ends before another can continue, so every suffix corresponds to a leaf. Compress each maximal path of nonroot nodes with one child and no terminal into one edge. Store edge label as `[start,end)` into `T`, not a copied string.

Each child under a node begins with a distinct symbol; otherwise their common first symbol should be represented before a branch. A node's string depth is parent depth plus interval length. The spelled path may combine intervals from different occurrences in `T`, but concatenated symbols define one substring.

There are exactly `n` leaves for the `n` suffixes. Let `i` be nonroot/root internal nodes as appropriate; every nonroot internal has at least two children, and root also has at least two for a nontrivial sentinel text. In any rooted tree, edges equal nodes minus one. Summing child counts yields at least `2i` edges, while edges equal `i+n-1`; therefore `i<=n-1`. Total nodes `i+n<=2n-1`. Degenerate empty/singleton conventions are handled separately.

This linear node count does not imply copied labels are linear. One edge can spell a long interval, and summing copied label lengths across suffixes can be quadratic. Interval pairs use constant words but bind node lifetime to text lifetime. Position/end widths and sentinel-extended length need checked arithmetic.

**Naïve insertion is the correctness oracle.** For each suffix start `s`, traverse from root comparing the remaining suffix with candidate edge labels. With no same-first-symbol child, add one edge `[s,n)` to a leaf labeled `s`. With a full label match, advance. On a partial match of length `j`, split the edge into common prefix, old remainder to old child, and new remainder to the new suffix leaf. With a unique sentinel, distinct suffixes do not end at an existing internal position.

This is ordinary radix insertion over `n` suffixes. It preserves the complete-suffix and unique-first-symbol invariants and is excellent for tiny reference construction. It can compare `Theta(n^2)` symbols across repetitive suffixes and may allocate/split extensively. Calling it “a suffix tree” describes output, not a linear construction bound.

Store leaf suffix start separately from the edge interval start. After splits, the leaf's incoming edge can refer to a later substring occurrence while its complete root path still represents suffix start `s`. Confusing these fields produces wrong occurrence positions.

Strong failure semantics prepare the split node, edge intervals, child container, new leaf, and metadata privately; publish through one parent child-slot replacement. Existing interval objects may be immutable values. If parent pointers exist, update them before/with publication under exclusive ownership. On failure, the old topology and text generation remain valid.

**Pattern search follows labels and can end implicitly.** Starting at root with pattern position `p=0`, select child by `P[p]`. Compare the edge interval symbol by symbol. Mismatch or text/edge exhaustion before the stored interval ends is absent, unless pattern itself has just ended. If the whole edge matches, advance to its child. If `p=|P|` at either a node or inside a matched edge, the pattern occurs.

All leaves below the reached child/implicit edge position are starts of suffixes beginning with `P`, hence occurrence positions. Overlaps are naturally included. Reporting them costs output size. Lexicographic DFS orders suffixes, not text positions; sort or maintain leaf-position structures if the API promises ascending text coordinates.

An empty pattern mathematically occurs at every boundary, while a tree with only nonempty suffix leaves represents starts `0..n-1`. Define whether to reject, return indexed starts, or include end boundary `n`. Paginate and authorize output. Do not traverse millions of leaves without limits.

Search symbol work is `O(|P|)` because each compared edge symbol consumes a pattern symbol, plus child lookup: fixed/small alphabet arrays can be constant, sorted vectors logarithmic in degree, hashes expected constant, and adaptive nodes platform-dependent. Reporting `k` leaves adds `Theta(k)`. Locating all leaves through repeated recursive traversal can overflow stack on malformed/deep trees; use bounded iteration.

**Tree topology exposes suffix order and LCP.** Traverse children in alphabet order and list leaf suffix starts: this is the suffix array. For `banana$`, DFS yields `[6,5,3,1,0,4,2]`. If child containers are hashed, explicitly sort their leading symbols or store an ordered representation; incidental iteration order is not suffix order.

The LCP of two suffixes is the string depth of their lowest common ancestor. Adjacent suffix-array LCP values arise from LCAs of adjacent leaves. Preprocess Euler tour plus RMQ, a succinct LCA structure, or derive SA/LCP arrays. Parent/depth correctness then matters. Trees can answer conceptual LCP paths, while arrays often answer faster and smaller in practice.

Every internal node's path string occurs in at least two descendant suffixes. The deepest internal string is a longest repeated substring; descendant leaf starts are occurrences, including overlaps. Ties require a policy. For a substring occurring at least `k` times, consider deepest nodes/subtree leaf counts or implicit loci and ensure the count/substring boundary definition.

Longest common substring across two documents uses a generalized tree and finds a deepest node with leaves from both sources. Separators must prevent crossing; cached source sets/counts can be large, compressed, or computed offline. Access control must stop cross-tenant inference.

**Suffix links encode repeated suffix work.** An internal node with path label `aX` has a suffix link to the node/implicit locus for `X`, often an explicit internal node in the suffix tree under the sentinel/construction invariant. Root is special. Links let construction move from one suffix extension context to the next without walking from root.

Validate suffix links semantically on tiny trees by reconstructing source/target path strings. In production, reconstructing every string is expensive; construction-state assertions, parent/depth intervals, hashes with collision-safe fallback, and differential rebuilds provide evidence. A pointer in range is not proof of correct suffix meaning.

Suffix links are construction accelerators and can remain for queries such as matching statistics, but cost one pointer/index per internal node. Omit them from final immutable format if unused, after construction no longer needs them. Persisting them requires same-generation IDs and validation.

**Ukkonen builds implicit suffix trees phase by phase.** At phase `i`, conceptually append `T[i]` to the current prefix and ensure all suffixes of `T[0..i]` are represented. Performing every extension from root is quadratic. Ukkonen maintains an active point `(active_node,active_edge,active_length)` and `remainder`, the unresolved suffix extensions.

An active point may lie at a node or inside an edge. Canonical form ensures active length is less than the current edge length after skip/count. When active length spans an edge, descend and subtract that edge length repeatedly instead of comparing its characters. This turns character-by-character walking across already known edge segments into constant work per skipped edge.

For the next extension, three outcomes are commonly described. If no outgoing edge begins with the new symbol, create a leaf. If the active point is inside an edge and the next edge symbol differs, split and add a leaf. If the next symbol already exists/matches, Rule 3 says the current extension is already represented; increase active length and end the phase early because remaining suffixes are implicitly present under the algorithm's invariant.

New internal nodes created across consecutive extensions receive suffix links. A pending previously created internal links to the current new internal, or to the active node/root as required. Root has special fallback: when active node is root and active length positive, decrement active length and advance the active-edge start according to the next suffix. Otherwise follow the active node's suffix link.

Leaves created in earlier phases should extend when a new symbol arrives. Rather than update every leaf edge end, store all current open leaf ends through a shared phase endpoint. Internal edges use fixed ends. At finalization, resolve/serialize endpoints as bounded integers. Never leave a pointer to a stack phase variable or allow end beyond text length.

The remainder loop decrements when one suffix extension is explicitly resolved; Rule 3 retains unresolved implicit extensions for the next phase according to the canonical algorithm. Off-by-one conventions vary: inclusive end versus half-open, active edge as text index versus symbol, remainder definition, and root link. Choose one source/implementation convention and derive tests from it; mixing pseudocode conventions is a primary defect source.

The linear-time analysis charges explicit node/leaf creations (linear total), suffix-link transitions, and skip/count edge descents amortized across phases. Rule 3 prevents repeated work. Child transition cost must be constant under bounded alphabet or adds map costs. This chapter explains obligations, not a full line-by-line formal proof or production implementation.

**Other construction routes can be safer.** A suffix tree can be built from SA and LCP in linear time by maintaining a stack of nodes with increasing string depths while scanning suffixes in lexicographic order. Each LCP value determines where the next leaf branches; pop deeper nodes, create an internal at a new LCP depth when needed, and attach leaves/previous subtree. Edge intervals are recovered from representative suffix positions and depth differences.

This route reuses a trusted suffix-array builder and avoids Ukkonen's online active-point complexity. It is not online and requires SA/LCP memory, but may be easier to validate. Conversely, a tree can emit SA/LCP. Cross-construction comparison is strong evidence.

Weiner and McCreight algorithms offer other linear-time construction perspectives. Choose based on online need, library maturity, alphabet, memory, and team expertise. A simpler `O(n log n)` or array-based index can be the durable production choice when inputs permit; theoretical optimality is not the sole criterion.

**Layout determines whether linear space is acceptable.** A pointer-rich node may carry child map object, parent, suffix link, edge start/end, suffix start, depth, flags, allocator header, and alignment. Hash maps reserve buckets/capacity. At `2n` nodes this can be many times the text and suffix array.

Use compact integer node IDs/indices, structure-of-arrays fields, inline small child vectors, sorted packed edges, adaptive fanout, or arenas. Integer offsets ease serialization and shrink pointers if within width. Arrays improve locality but mutation/growth can invalidate references; use indices/generations.

For immutable trees, flatten children into CSR-like edge arrays with per-node offsets, or store preorder ranges so each subtree's leaves form a contiguous SA interval. Then occurrence reporting can return `[leaf_lo,leaf_hi)` into a leaf-position/SA array without traversing nodes. Validate interval nesting, counts, and order.

Cache string depth if LCA/repeat queries need it; checked addition prevents overflow. Store edge end exclusive for uniform length. Separate leaf suffix start with a tag/type. Removing parent/suffix links after construction saves memory if queries do not need them. Measure final and peak construction memory.

**Immutability gives the cleanest concurrency model.** Build text/tree privately, validate, and release-publish one generation object. Readers pin it and traverse read-only intervals/children without locks. Reclaim after references/epochs/file leases drain. Lazy caches such as leaf ranges or LCA structures need their own synchronized publication and must bind to the generation.

Editing text invalidates every interval and suffix meaning. Do not mutate the borrowed buffer beneath a tree. Build a replacement, maintain immutable indexed segments, or use a different dynamic string index. Copy-on-write text alone is insufficient without tree rebuild.

Concurrent online construction is specialized: shared child creation, edge splits, leaf-end updates, suffix links, active state, and allocators all race. Parallel suffix-array construction followed by tree build may be easier. A coarse exclusive builder with concurrent reads only after final publication is a strong baseline.

Returned node/edge handles are unstable across rebuild/flatten/compaction. Return text positions, substrings copied/borrowed with generation lifetime, or opaque generation-tagged IDs. A leaf range cursor pins the generation and enforces output limits.

**Persistence serializes offsets, not pointers.** A format needs magic/schema, text or authenticated digest/reference, original/indexed length, alphabet/normalization/sentinel/separators, coordinate and integer widths, root, node/edge arrays, child offsets/order, leaf starts, optional parent/depth/suffix links/leaf ranges/LCA, build metadata, and checksums/provenance.

Validate checked region arithmetic and nonoverlap; root and node types; acyclic unique reachability; edge `[start,end)` nonempty and in text; unique sibling leading symbols; parent/child agreement; internal degree; leaf-start permutation; root-to-leaf suffix equality; depths; suffix links; child/leaf ranges; sentinel; and text digest. Bound work and diagnostics.

Full root-to-leaf comparison can be quadratic if done naïvely. High-assurance options rebuild/compare SA, use independent rolling/hash summaries with collision-safe samples/fallback, or reconstruct each suffix through SA/LCP evidence. State what was sampled versus proved. A checksum alone proves neither topology nor text association.

Crash-safe publication writes immutable text/tree/auxiliary files, validates, flushes, and atomically updates a durable generation manifest. Old generations stay until recovery/readers no longer need them. Never persist a runtime shared-leaf-end pointer or absolute address.

**Security includes parser, output, and corpus leakage.** Check every index before text/node access and every add/multiply for offsets, depths, sizes, and allocation. Reject cycles and excessive depth before recursive operations. Limit `n`, key/pattern length, nodes, edges, child degree, traversal steps, occurrence output, analytics, and error reports.

Repetitive text is adversarial for naïve construction and suffix comparisons; defend algorithm selection and time/temp memory. Malformed edge intervals can produce out-of-bounds reads. A sentinel or separator collision can permit cross-document matches. Unauthorized users must not enumerate leaves or infer repetitions across documents.

Tree traversal and memory access reveal pattern/text prefixes and are not constant-time. Multi-tenant indexes need namespace/source filters incorporated into reporting and cached counts. Persistent indexes require authenticated provenance where substitution matters.

Fuzz parsers and builders with sanitizers and allocation failure. Mutate every endpoint, node type, child offset, suffix link, depth, leaf label, sentinel, and generation binding. Crash-inject every durable step. Limit construction logs because dumping long edge labels/suffixes amplifies sensitive output.

**Evidence should use independent suffix representations.** For tiny text, materialize all suffixes and build a naïve compact tree. Enumerate root-to-leaf strings and require exact suffix multiset plus leaf starts. Compare search occurrences to brute-force substring scans and SA binary search. Compare lexicographic leaf order to a separately built SA and internal depths to LCP/repeated-substring results.

Exhaust tiny alphabets/texts including sentinel: empty-original/sentinel-only, one symbol, all equal, all distinct, periodic, alternating, long shared prefixes, and every short text. Patterns include empty, absent, full, suffix, prefix, ends inside edge, ends at node, longer than text, overlaps, sentinel, and document boundary.

For naïve split construction, force missing child, full-edge continuation, mismatch at every label position, and new suffix ending cases under sentinel conventions. For Ukkonen, trace after every phase: represented suffixes of current prefix, active canonicality, remainder, leaf ends, suffix links, Rule 3, root fallbacks, splits, and skip/count. Compare each phase against a naïve implicit tree for small texts.

Metamorphic properties include order-preserving alphabet remapping preserving topology/SA shape modulo symbols; leaf DFS equals SA; adjacent leaf LCA depths equal LCP; search equals brute force; longest repeat equals max LCP; append unique sentinel yields one leaf per suffix; serialize/reload preserves generation; and tree-from-SA/LCP equals direct tree logically.

Fault-inject text/child/node/edge allocation, split publication, suffix-link assignment, array flattening, SA/LCP conversion, file writes, validation, and manifest publication. Concurrency tests pin old readers across replacement, race lazy caches, enforce handle generations, and validate safe reclamation. No test result implies external review.

Benchmarks vary `n`, alphabet, repetition/entropy, common-prefix lengths, document count/separators, pattern length/hit/output, construction method/library, child layout, pointer/index widths, threads, and cache/NUMA/storage state. Measure final and peak bytes, nodes/edges/child capacity, build/validation time, symbol comparisons, search/output latency distributions, cache/TLB/branches/page faults, flatten/map/reload, generation retention, and publish/reclaim.

The executable below uses naïve owned-string edge labels to build the compact suffix tree for the finite text `banana$`. It validates suffix/leaf bijection, compression, reachability, sibling-leading symbols, occurrence search ending at nodes or inside edges, longest repeated internal path, and suffix-array order from leaves. It deliberately does not demonstrate interval ownership, Ukkonen's linear construction, Unicode, fixed-width safety, concurrency, persistence, or production performance.

<!-- bijux-verify: {"id":"suffix-tree-trace","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"text=banana$\nroot_edges=$,a,banana$,na\nnodes=11\nleaves=7\nana_positions=1,3\nnan_positions=2\nbanana_positions=0\nmissing_xyz=True\nlongest_repeat=ana\nsa_from_leaves=6,5,3,1,0,4,2\ninvariant=True\nevidence=finite_suffix_tree_trace\n","stderr":""}} -->
```python
class Node:
    def __init__(self, suffix_start=None):
        self.children = {}
        self.suffix_start = suffix_start


def common_prefix(a, b):
    length = 0
    while length < len(a) and length < len(b) and a[length] == b[length]:
        length += 1
    return length


class SuffixTree:
    def __init__(self, text):
        self.text = text
        self.root = Node()
        for start in range(len(text)):
            self._insert(text[start:], start)

    def _insert(self, suffix, suffix_start):
        node = self.root
        position = 0
        while position < len(suffix):
            first = suffix[position]
            edge = node.children.get(first)
            if edge is None:
                node.children[first] = (suffix[position:], Node(suffix_start))
                return
            label, child = edge
            matched = common_prefix(label, suffix[position:])
            if matched == len(label):
                position += matched
                node = child
                continue
            middle = Node()
            old_remainder = label[matched:]
            new_remainder = suffix[position + matched:]
            middle.children[old_remainder[0]] = (old_remainder, child)
            middle.children[new_remainder[0]] = (new_remainder, Node(suffix_start))
            node.children[first] = (label[:matched], middle)
            return

    def _leaf_starts(self, node):
        if node.suffix_start is not None:
            return [node.suffix_start]
        result = []
        for first in sorted(node.children):
            result.extend(self._leaf_starts(node.children[first][1]))
        return result

    def find(self, pattern):
        node = self.root
        position = 0
        while position < len(pattern):
            edge = node.children.get(pattern[position])
            if edge is None:
                return []
            label, child = edge
            compared = min(len(label), len(pattern) - position)
            if label[:compared] != pattern[position:position + compared]:
                return []
            position += compared
            if position == len(pattern):
                return sorted(self._leaf_starts(child))
            if compared < len(label):
                return []
            node = child
        return sorted(self._leaf_starts(node))

    def validate(self):
        seen = set()
        leaves = []
        paths = []
        deepest = ""

        def visit(node, path, is_root):
            nonlocal deepest
            if id(node) in seen:
                return False
            seen.add(id(node))
            if node.suffix_start is not None:
                leaves.append(node.suffix_start)
                paths.append(path)
                return len(node.children) == 0
            if not is_root and len(node.children) < 2:
                return False
            if not is_root and len(path) > len(deepest):
                deepest = path
            for first, edge in node.children.items():
                label, child = edge
                if label == "" or label[0] != first or not visit(child, path + label, False):
                    return False
            return True

        valid = visit(self.root, "", True)
        expected = [self.text[start:] for start in range(len(self.text))]
        return (
            valid
            and sorted(leaves) == list(range(len(self.text)))
            and sorted(paths) == sorted(expected),
            len(seen),
            len(leaves),
            deepest,
        )


text = "banana$"
tree = SuffixTree(text)
invariant, nodes, leaves, longest = tree.validate()
root_edges = sorted(label for label, _ in tree.root.children.values())
sa = tree._leaf_starts(tree.root)

print(f"text={text}")
print("root_edges=" + ",".join(root_edges))
print(f"nodes={nodes}")
print(f"leaves={leaves}")
print("ana_positions=" + ",".join(map(str, tree.find("ana"))))
print("nan_positions=" + ",".join(map(str, tree.find("nan"))))
print("banana_positions=" + ",".join(map(str, tree.find("banana"))))
print(f"missing_xyz={tree.find('xyz') == []}")
print(f"longest_repeat={longest}")
print("sa_from_leaves=" + ",".join(map(str, sa)))
print(f"invariant={invariant}")
print("evidence=finite_suffix_tree_trace")
```

## Definitions and Notation

Indexed text `T` has length `n` including sentinel; suffix `S_i=T[i..n)` for `0<=i<n`. Edge `e` carries label interval `[l_e,r_e)` or an equivalent immutable symbol slice. `depth(v)` is concatenated root-path length. A locus can be explicit node or implicit `(edge,offset)`. Leaf `leaf(i)` represents suffix start `i`. `occ(P)` is descendant leaf-start set after consuming pattern `P`.

For Ukkonen-style notation, phase `i` incorporates `T[i]`; active point is `(node,edge_index,length)` under one declared convention; remainder counts unresolved extensions; an open leaf end equals current phase endpoint. A suffix link's semantic source label `aX` maps to `X`, with root/single-symbol cases explicitly defined.

## Mechanisms, Invariants, or Proof Structure

Logical correctness contracts a complete suffix trie without changing any root-to-leaf string. Sentinel uniqueness proves one explicit leaf per suffix. Degree counting proves fewer than `2n` nodes; interval labels make each edge constant-size. Query correctness consumes exactly the pattern and returns precisely descendant suffix starts. Lexicographic child traversal and LCA string depths connect the tree to SA/LCP.

Construction correctness is separate. Naïve radix insertion proves finite topology but not linear time. Ukkonen requires phase suffix coverage, active-point canonicality, suffix-link meaning, skip/count, Rule 3, remainder, and leaf-end invariants. Storage, persistence, concurrency, parser, coordinate mapping, and security add independent obligations.

## Alternatives and Trade-Offs

| Representation/construction | Strength | Principal cost |
|---|---|---|
| suffix trie | simplest conceptual membership | quadratic nodes |
| naïve compact suffix insertion | small reference oracle | quadratic comparisons worst case |
| Ukkonen online tree | linear online construction model | active/suffix-link complexity |
| tree from SA+LCP | simpler batch derivation | requires array construction/storage |
| pointer-rich suffix tree | direct navigation/LCA | large objects and poor locality |
| flattened indexed tree | mapping/locality/compact IDs | immutable rebuild and format complexity |
| suffix array+LCP | compact sequential arrays | binary-search/RMQ rather than explicit paths |
| suffix automaton/FM-index | end-position states or compression | different operations/invariants |

Choose against online/batch need, query suite, text size/repetition, memory and peak build budget, library maturity, platform, persistence, and assurance—not only asymptotic labels.

## Failure Modes and Misconceptions

- Linear node count assumes compressed labels represented by intervals, not copied path strings.
- The sentinel establishes leaves but must be excluded consistently from user matches/analytics.
- Pattern loci may be implicit inside edges.
- Leaf edge interval start is not the leaf's suffix start.
- Lexicographic leaf order is not text-position order.
- Suffix links speed construction but require semantic target validation.
- Open leaf ends are construction state, not portable persistent pointers.
- Ukkonen pseudocode conventions are not interchangeable at off-by-one boundaries.
- A tree rebuilt over edited text invalidates every old interval/position handle.
- Finite naïve evidence cannot establish online linear time or production memory.

## Worked Examples

### Example 1

Without sentinel, suffix `a` is a prefix of suffix `ana`, so it may end at an internal point. Appending unique `$` creates `a$` and `ana$`, each ending at a distinct leaf.

### Example 2

`banana$` has seven suffixes/leaves. With each internal degree at least two, at most six internal nodes and thirteen total are possible; the finite canonical tree uses eleven nodes.

### Example 3

Pattern `nan` follows root edge `na`, then matches only `n` inside edge `na$`. Pattern consumption completes, so it is present at suffix start 2 even without an explicit `nan` node.

### Example 4

Two suffixes beginning `ana` branch after three symbols, so their LCA string depth is three. The path `ana` is an internal repeat with leaves 1 and 3.

### Example 5

Sorting root/child edges and DFS visiting leaves emits suffix lexicographic order. Hash-child iteration without sorting can emit a valid leaf set but not a suffix array.

### Example 6

A naïve insertion splits edge `anana$` after matching `ana` with suffix `ana$`; the old remainder `na$` keeps its old leaf, while new remainder `$` leads to the new leaf.

### Example 7

During an online phase, hundreds of leaf edges can share one mutable end equal to the phase index. Advancing it extends all leaves conceptually in constant work; internal split edges receive fixed endpoints.

### Example 8

Active length 12 over an edge of length 5 is not canonical. Skip/count descends, subtracts 5, then repeats until the active length lies within the current edge or at a node.

### Example 9

A physical file's edges can all be in text bounds while two siblings both begin `a`. That violates radix uniqueness and makes transition selection ambiguous; loader validation rejects it.

### Example 10

Searching a one-symbol pattern in a repetitive million-symbol text can reach nearly a million leaves. Path traversal is fast, but occurrence reporting is linear output and must be paginated/authorized.

## Cross-Program Connections

- **Algorithms:** tries, suffix arrays/LCP/RMQ, LCA, longest repeats/common substrings, and online amortization meet in one structure.
- **Database engineering:** immutable text/index generations, mapped node arrays, range metadata, rebuild publication, and provenance mirror secondary indexes.
- **Data engineering/search:** generalized document trees require separators, source labels, normalized-to-original coordinates, batching, and access filters.
- **Concurrent programming:** private construction, atomic generation publication, pinned readers, lazy-cache synchronization, and reclamation provide safe reads.
- **Security engineering:** hostile interval graphs, repetitive-input denial of service, cross-document leakage, output amplification, and parser bounds matter.
- **Computer architecture:** pointer/object overhead, compact IDs, child layouts, text cache misses, flattened arrays, and NUMA dominate real space/time.
- **Reliability:** phase-by-phase oracle comparison, semantic suffix links, crash injection, and tree/SA cross-validation provide layered evidence.

## References

1. [Esko Ukkonen, *On-line Construction of Suffix Trees*](https://www.cs.helsinki.fi/u/ukkonen/SuffixT1withFigs.pdf).
2. [Carnegie Mellon University, *Suffix Trees* lecture notes](https://www.cs.cmu.edu/~ckingsf/bioinfo-lectures/suffixtrees.pdf).
3. [LLVM, maintained `SuffixTree` implementation](https://llvm.org/doxygen/SuffixTree_8h_source.html).
4. [Rust `suffix_tree` crate documentation](https://docs.rs/suffix_tree/latest/suffix_tree/).
5. [Princeton Algorithms, *Suffix Arrays*](https://algs4.cs.princeton.edu/63suffix/).
6. [Carnegie Mellon University, *Suffix Arrays* lecture notes](https://www.cs.cmu.edu/~ckingsf/bioinfo-lectures/suffixarrays.pdf).
7. [Stanford CS166, *Tries and Suffix Trees* lecture notes](https://web.stanford.edu/class/archive/cs/cs166/cs166.1166/lectures/07/Small07.pdf).
8. [NIST Dictionary of Algorithms and Data Structures, *suffix tree*](https://xlinux.nist.gov/dads/HTML/suffixtree.html).

## Exercises

### Exercise 1

Construct a compact suffix tree for `aba$` using owned labels. List root edges, every leaf start/path, internal string depths, suffix-array order from DFS, and pattern results for `a`, `ba`, `ab`, and `aba$`.

### Exercise 2

Prove the `2n-1` node bound for a sentinel-terminated compact suffix tree and explain why storing copied edge strings can still consume quadratic symbols.

### Exercise 3

Specify and prove a pattern-search routine that handles completion at a node and inside an edge. Include empty pattern, overlapping matches, child lookup cost, occurrence ordering, and output limits.

### Exercise 4

Design a phase-by-phase validation harness for an Ukkonen implementation. State reference state, active point, suffix links, open ends, remainder, Rule 3, skip/count, allocation failure, and final cross-checks.

### Exercise 5

Design an immutable persistent suffix-tree generation for a multi-document normalized corpus. Include separators, original coordinate mapping, compact layout, validation, atomic publication, concurrency, authorization, and benchmark evidence.

## Answers to the Exercises

### Answer 1

Suffixes are `aba$` at 0, `ba$` at 1, `a$` at 2, `$` at 3. Root edges are `$` to leaf 3, `a` to an internal depth-one node, and `ba$` to leaf 1. The `a` node has `$` to leaf 2 and `ba$` to leaf 0. Root-to-leaf paths exactly match the four suffixes. Sorted child DFS yields SA `[3,2,0,1]`. Search `a` ends at the internal node and returns `[0,2]` in text order; `ba` ends inside root edge `ba$` and returns `[1]`; `ab` ends inside child edge `ba$` below `a` and returns `[0]`; `aba$` reaches leaf 0.

### Answer 2

There are `n` suffix leaves. Let `i` internal nodes including root for a nontrivial tree. Every internal has at least two children, so the number of edges is at least `2i`. A tree with `n+i` nodes has exactly `n+i-1` edges. Thus `2i<=n+i-1`, so `i<=n-1` and total nodes `n+i<=2n-1`. This counts edge records, not label symbols. If every edge copies its substring, long labels from many suffixes can collectively store `Theta(n^2)` symbols; `[start,end)` references keep each edge constant-size while the one authoritative text stores `n` symbols.

### Answer 3

At `(node,p)`, select by `P[p]`; absent child returns empty. Compare at most `min(edge_length,|P|-p)` symbols. Any mismatch returns empty. If pattern ends during or exactly after those comparisons, every leaf below the edge child is an occurrence because each descendant suffix shares the consumed path. If the edge ends first, advance to its child and continue. Therefore each pattern symbol is compared once along a single path, plus child lookup; reporting `k` leaves costs `Theta(k)`. Define empty pattern as rejected or a paginated set of all allowed positions/boundaries. Preserve overlaps. Return suffix-lexicographic leaf order or explicitly sort to text order. Apply authorization, limit/cursor, cancellation, and generation pinning.

### Answer 4

For every short prefix phase, build a naïve compact/implicit reference of all current-prefix suffixes under the exact sentinel/endpoint convention. Expand/enumerate the implementation and compare represented suffixes. Validate active node/edge/length bounds and canonical skip/count state; remainder against unresolved extensions; every open leaf end equals phase endpoint and fixed internal ends stay fixed; child uniqueness, parent/depth, and pending links; every completed suffix link maps path `aX` to `X`; Rule 3 only when the next symbol already follows the active locus; root fallback and remainder changes. Inject failure before every node/child/edge allocation and require documented unchanged/basic state. At final sentinel phase, validate one leaf per suffix, node bound, full suffix paths, search versus brute force, DFS SA versus independent SA, LCA depths versus LCP, and no unresolved runtime endpoint pointers.

### Answer 5

Normalize each document under one versioned policy and retain monotone maps from indexed coordinates to original byte spans. Insert unique/nonmatching boundary separators or store boundary-aware semantics; label every leaf with document and local/global start. Flatten nodes/edges into checked integer arrays, sorted child ranges, edge text offsets, leaf starts, subtree leaf ranges, optional depth/LCA, and omit construction links if unused. Store text/digest, documents, separators, encoding/version, widths, build metadata, checksums and authenticated provenance. Validate all regions, topology, edge bounds/leading uniqueness, degree, leaf suffix bijection without cross-boundary matches, depths/ranges, DFS SA/LCP, mappings, and digest. Build/flush/validate privately, atomically publish a manifest generation, pin readers, and reclaim old files after leases drain. Authorize/filter documents before reporting leaves or aggregates; bound patterns/output. Benchmark real/repetitive corpora, construction/final/peak bytes, validation, exact/output queries, mapping, cold/warm pages, concurrency, retained generations, and publication/recovery; do not claim universal superiority or external review.
