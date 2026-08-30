---
module_id: DSE-045
program: Data Structures Engineering
level: 1
module_number: 45
title: Compressed and Radix Tries
status: complete
last_verified: 2026-08-30
---

# Compressed and Radix Tries

## One-Page Review

### Governing question

How can unary trie paths be compressed into radix edges while preserving exact/prefix/longest-match semantics, bounded memory, safe structural mutation, ordered traversal, snapshots, and durable evidence?

### Essential definitions

- A **radix trie/tree** stores nonempty sequence labels on edges and branches where keys diverge.
- **path compression** replaces a chain of nonterminal single-child trie nodes by one edge labeled with the concatenated symbols.
- A **Patricia trie** is a compressed radix structure; bitwise variants store discriminating bit positions rather than explicit unary paths.
- The **longest common prefix (LCP)** of two sequences is their maximal equal initial segment.
- An **edge split** replaces one label by its common prefix and two remainders when insertion diverges inside the label.
- A **path merge** concatenates an incoming and sole outgoing label after deletion leaves a nonterminal unary node.
- A **crit-bit tree** branches at the first differing bit and keeps keys/items at leaves under a compact binary design.
- An **adaptive radix tree (ART)** combines path compression with node representations selected by fanout.
- A **prefix key** is a stored key that ends at an internal branching node; terminal/value state must exist independently from children.
- A **copy-on-write radix tree** creates a new root-to-change path and shares unchanged immutable subtrees.

### Central model, mechanism, or theorem

Each edge label is nonempty, and outgoing labels from one node have distinct first symbols. Concatenating labels from the root to a terminal spells exactly one stored key. Exact lookup selects by first symbol, then compares the whole label; mismatch means absence. Inserting a key that diverges `j` symbols into an edge splits it at the LCP: a new intermediate node owns the common label, the old child moves under the old remainder, and the new key moves under its remainder or terminates at the intermediate node.

Deletion clears terminal membership and removes empty suffixes. Whenever a nonroot node becomes nonterminal with exactly one child, its incoming label and sole child label may be concatenated. This restores the canonical compression invariant without changing any root-to-terminal string. With total query length `L`, lookup examines at most `L` key symbols, plus transition-selection overhead. Compression reduces nodes and pointer traversals but cannot asymptotically avoid reading distinguishing query symbols.

Compressed structure complicates memory ownership and publication. Labels may be owned strings, slices into immutable keys/arenas, or bounded inline prefixes with external tails. Split/merge can allocate and invalidate node/edge handles. Strong updates prepare replacement nodes/labels privately and publish one parent slot or a new root only after validation.

### Critical invariants

1. The alphabet, encoding, canonicalization, empty-key, bit order, and maximum-length policies match every operation and persisted generation.
2. Every stored edge label is nonempty; siblings have distinct first symbols under the declared alphabet equality.
3. Concatenated root-to-terminal labels are in one-to-one correspondence with stored canonical keys and values.
4. Every nonroot nonterminal node has at least two children in canonical fully compressed form; the sentinel root may be exceptional.
5. Split replaces label `q` by `q[0:j]` and remainders whose concatenations reproduce old and new keys exactly.
6. Merge occurs only for a nonterminal unary node and preserves terminal descendants and ordering.
7. Stored size counts terminals; subtree counts, minimum discriminating bits, adaptive node tags/capacities, and other metadata recompute correctly.
8. Edge/node/iterator handles identify their snapshot generation and follow documented invalidation after split, merge, conversion, or reclamation.
9. Persistent offsets, label ranges, node graph, and adaptive tags validate before traversal; concurrent publication exposes no partial split/merge.

### Common failures

- Comparing only the first symbol of a compressed label and accepting a query that mismatches later.
- Splitting at `j=0` after already selecting a sibling by the same first symbol, indicating broken transition uniqueness or alphabet equality.
- Forgetting the case where the inserted key ends inside the old edge label.
- Losing the old terminal/value when splitting an edge whose child represents a complete key.
- Merging through a terminal node and erasing a shorter prefix key.
- Storing labels as slices into temporary caller buffers.
- Assuming path compression guarantees fewer bytes when owned labels duplicate key material.
- Exposing node pointers as stable across ART node growth/shrink conversion.
- Mixing most-significant and least-significant bit numbering in Patricia routing.
- Using longest-prefix routing without validating prefix length/address family and canonical masked bits.

### Compact example

All five keys share root edge `r`. Its child branches through `oman` for `roman`, `romane`, and `romanus`, and through `ubic` for `rubicon` and `rubicundus`. The `roman` node is terminal and has edges `e` and `us`; the `rubic` node has edges `on` and `undus`. Deleting `romane` removes edge `e`; deleting prefix key `roman` leaves a nonterminal unary node, which merges `oman` and `us` into edge `omanus` below `r`. Three keys remain, longest prefix of `romanuscript` is still `romanus`, and all root-to-terminal strings are preserved.

### Connections

[DSE-044](044-tries.md) defines sequence identity, terminal membership, basic operations, Unicode policy, and evidence. [DSE-005](005-contiguous-and-linked-layouts.md) and [DSE-006](006-memory-locality-and-cache-behavior.md) supply layout/locality accounting; [DSE-012](012-dynamic-arrays-and-geometric-growth.md) and [DSE-022](022-separate-chaining.md) supply adaptive child containers. The [program roadmap](../ROADMAP.md) continues with suffix structures and graph algorithms.

## Governing Question

Which compression unit, label ownership, split/merge policy, transition/node layout, terminal encoding, stable-handle requirement, snapshot/update rate, routing convention, and persistence target justify a radix, Patricia, crit-bit, ART, or immutable radix design?

## Why This Matters

An uncompressed trie can allocate a node and pointer structure for every symbol of every distinct prefix. Many real key sets contain long stretches with no branching: paths, URLs, identifiers, IP prefixes, UUID-like strings, filesystem names, and database keys. Those unary nodes add indirections, allocator overhead, cache misses, and persistent metadata while contributing no choice. Path compression stores the whole stretch on one edge.

The optimization changes the algorithm. Lookup must compare labels, not single transitions. Insertion may stop inside an edge and rebuild a local topology. Deletion may reveal a compressible unary node. A label slice needs ownership. Ordering and prefix queries can end inside labels. Adaptive nodes change physical type as degree crosses thresholds. A pointer or iterator that was stable in a fixed node tree may become dangling after one split or conversion.

Several related structures use different contracts. String radix tries group symbols into labels. Patricia/crit-bit structures often branch on bits or store discriminating positions. ART uses compressed prefixes and multiple fanout node types for main-memory databases. Immutable radix trees path-copy for snapshots. Kernel XArrays are radix-like indexed structures with special entries and concurrency rules, not general text dictionaries. IP forwarding performs longest match over masked bit prefixes with address-family and canonical-prefix constraints.

The engineering question is therefore not “can unary nodes be removed?” It is whether compression, ownership, mutation, machine layout, identity, and lifecycle form a system whose logical keys remain provably exact.

## Prerequisites and Retrieval

Retrieve the full sequence/canonicalization contract, basic trie correctness, transition choices, Unicode distinctions, persistence, security, and tests from [DSE-044](044-tries.md). Retrieve representation and operation invariants from [DSE-002](002-representation-invariants.md) and [DSE-003](003-operation-contracts.md), concrete memory and allocation costs from [DSE-004](004-time-space-and-allocation-cost.md), cache behavior from [DSE-006](006-memory-locality-and-cache-behavior.md), iterator generations from [DSE-008](008-iterators-and-traversal-protocols.md), and validation/benchmark discipline from [DSE-009](009-property-based-testing-of-data-structures.md) and [DSE-010](010-benchmarking-a-structure-without-misleading-results.md).

## Learning Objectives

After completing this module, you should be able to:

1. state canonical radix edge, terminal, branching, and size invariants;
2. implement exact lookup and longest-prefix match across multi-symbol labels;
3. derive every LCP insertion case and preserve old/new terminal values;
4. delete keys and merge only safe nonterminal unary paths;
5. choose owned, interned, sliced, inline, or external label storage;
6. distinguish string radix, bitwise Patricia/crit-bit, ART, immutable radix, and indexed radix structures;
7. reason about adaptive node conversion, SIMD/cache behavior, and concrete bytes;
8. define snapshot, concurrency, handle invalidation, and reclamation semantics;
9. validate versioned persistent nodes, labels, offsets, bit prefixes, and metadata; and
10. build differential, exhaustive, metamorphic, fault, concurrency, and performance evidence.

## Core Exposition

**Compression preserves the logical uncompressed trie.** Begin with a trie in which every edge has one symbol. Any maximal path whose internal nodes are nonterminal and have one child can be replaced by one edge labeled with the concatenation. No key ends at a removed internal node, and no branch choice occurs there, so root-to-terminal strings remain unchanged. Conversely, expand every multi-symbol label into unary nodes to recover an equivalent uncompressed trie. This equivalence is the central correctness model.

The root is a sentinel and may have zero or one child without being merged away because an API needs a stable entry point and the empty key may terminate there. Every other nonterminal node should have at least two children in a canonical fully compressed trie. A terminal internal node can have one child: it represents a stored shorter key and cannot be removed. Some implementations deliberately leave temporary unary nodes to simplify updates; if so, “fully compressed” is not an invariant and compaction timing must be explicit.

Store children by first label symbol. Sibling first symbols are unique, because two edges beginning with the same symbol share a nonempty common prefix and should have an intermediate node. This gives deterministic transition selection before label comparison. A hash or adaptive child map may find the candidate; the algorithm then compares every label symbol against the corresponding query segment.

Exact lookup maintains query position `i`. Select the edge whose first symbol equals `key[i]`. Let its label have length `q`. If fewer than `q` query symbols remain or any comparison differs, the key is absent. Otherwise advance `i+=q` and reach the child. When `i=L`, return present only if the child is terminal. The query can end inside an edge: that prefix exists conceptually in the expanded trie but is not a stored key or materialized node.

Prefix enumeration needs a nuanced final comparison. A requested prefix may end exactly at a node or inside a matching edge. In both cases every terminal below that edge begins with the prefix. An iterator must remember the already-spelled edge label so it emits complete keys. If the prefix mismatches before ending, return empty. Longest-prefix match records terminal nodes reached at label boundaries; a key cannot terminate inside an edge under the invariant.

For query length `L`, total label symbols compared along one successful path are at most `L`; edges partition the consumed sequence. Transition lookup adds fixed, logarithmic, expected, or adaptive costs per branching node. Failed queries also compare at most the consumed prefix plus one mismatching symbol per chosen edge. Canonicalization and output remain additional. SIMD/vector label comparison can lower constants but must handle tails and avoid out-of-bounds reads.

**Insertion is an LCP case analysis.** Traverse until a missing first-symbol transition or a label comparison stops. With no candidate edge, create one edge labeled by the entire remaining nonempty key suffix and a terminal child. This is already compressed. If the existing label matches completely, advance; if the key also ends, update/reject at that child, otherwise continue.

Suppose existing edge label `q`, remaining key suffix `s`, and LCP length `j` satisfy `0<j<|q|`. Create an intermediate node reached by `q[:j]`. Move the old child beneath it under label `q[j:]`; this preserves every old descendant spelling. If `j=|s|`, the new key ends at the intermediate node, so mark it terminal with the new value. Otherwise add another child under `s[j:]` with a new terminal. The two remainder labels begin differently by maximality of the LCP.

If `j=|q|<|s|`, the old edge matched fully and traversal should continue at its child rather than split. If `j=0` despite selecting by the same first symbol, either the child index, alphabet equality, encoding, or stored label is corrupt. Make these branches explicit; a compact clever implementation often loses the key-ending-inside-edge case.

The old child itself may be terminal and may own counts, values, child storage, parent links, or persistent IDs. Splitting moves the edge relation, not the child's logical identity. The intermediate node's subtree count equals old subtree terminals plus one only when the inserted key is genuinely new. Duplicate update does not change counts. Parent pointers of the old child must change if stored.

Strong failure semantics prepare the intermediate/new leaf, copied or sliced labels, child structures, value, metadata, and capacity before replacing the parent's edge. A single publish installs the replacement. If labels reference immutable original key storage, ensure that storage outlives all descendants. If concatenated/substring objects allocate, account for failure and peak memory. In-place mutation of the old label before all allocations succeed can make rollback impossible.

**Deletion reverses structure without reversing insertion history.** Traverse full labels to a terminal node. If missing or nonterminal, return false. Clear/destroy the value and decrement size. If the node has no children, remove its incoming edge and node, then consider its parent. If it is nonterminal with one child, concatenate the incoming and outgoing labels, connect its parent directly to its child, and retire it.

Never merge through a terminal node: doing so erases a stored prefix key. A nonterminal node with two or more children is a necessary branching point. The root remains. Merging can cascade upward after deletion removes a branch. Recompute or update subtree counts and top-k aggregates. Parent links and generation-tagged handles require changes or invalidation.

Concatenation storage matters. Copying two strings is simple but can make deletion allocate and fail. A rope/two-slice label avoids immediate copy but accumulates fragments and complicates comparisons/persistence. Labels can reference ranges in immutable canonical key arenas, but merging labels originating from different keys may not be contiguous; choose one surviving full-key backing slice when the concatenated path is a prefix of it. Inline prefix plus external tail, as used in adaptive designs, bounds node size but needs careful length handling.

Lazy deletion may clear terminal and retain compressible structure until rebuild. Logical correctness can remain intact if lookup checks terminals, but memory and traversal degrade, and canonical node-degree validators must be relaxed. Tombstone values are different from nonterminal state if deletion history or snapshots need visibility. Declare compaction thresholds and evidence.

**Patricia and crit-bit variants encode divergence.** A binary Patricia trie avoids materializing every bit. Internal nodes identify a discriminating bit position, ordered strictly along paths; leaves hold full keys or references. Lookup follows the query bit at each internal node, then compares the candidate full key. Insertion finds the first differing bit and inserts a branch at the correct ordered position.

Bit numbering is part of the format: byte order, most/least significant bit, key length, and terminator/prefix semantics must be fixed. Without an end-of-key convention, one bit string that prefixes another is difficult to distinguish. Store lengths, an explicit terminator ordering, or leaves with full equality. Malformed discriminating positions that do not increase can create loops or incorrect routing.

Crit-bit trees emphasize two-way branches at the critical bit and a small control structure. They can support exact lookup and ordered traversal for byte strings. They are not identical to multiway string radix nodes, and performance depends on full-key storage, critical-position extraction, cache layout, and update protocol.

IP routing stores network prefixes rather than arbitrary terminated strings. IPv4 and IPv6 need separate or tagged domains; prefix lengths must be within 32/128; host bits beyond the prefix are conventionally masked for canonical identity. Longest-prefix match records the most specific route encountered. Default route length zero terminates at root. RFC routing behavior does not authorize ignoring next-hop policy, metrics, table/VRF identity, or update atomicity.

**ART makes fanout physical.** Adaptive Radix Trees use path compression and node types sized for different child counts. Small nodes store a few key bytes and child pointers compactly; larger nodes use indexed or direct arrays. Growth converts a node when full; deletion may shrink it. This avoids a full 256-pointer table for most sparse byte nodes while retaining fast dense lookup.

An implementation must validate type-specific degree/capacity, sorted key arrays where required, index sentinels, child ownership, and conversion thresholds. Converting a node can allocate and fail. Prepare the replacement, copy all children and metadata, validate, then atomically replace the parent link or copy-on-write path. Node-address handles invalidate even though logical prefixes remain.

ART often stores only a bounded prefix inline and recovers/compares longer prefix bytes from a descendant leaf. This saves node space but couples internal validation to leaf availability and key lifetime. A mismatch beyond the inline prefix must compare authoritative full key bytes. Deletion of the representative leaf may require choosing another. Persisted formats need the same reconstruction rule.

SIMD comparisons and small-node scans can reduce branches, while dense node indexes trade a byte lookup table for packed child pointers. Architecture, compiler, pointer width, allocator, key distribution, and cache state determine thresholds. The ART paper provides a design and measurements, not immutable constants for every platform.

**Immutable radix trees favor snapshots.** A functional update clones nodes/edges along the search path and shares unchanged subtrees. It publishes a new root after all allocations succeed, naturally giving the old root a consistent view. Long shared prefixes reduce copied branching state, though split/merge may create several nodes/labels. Slow readers retain old versions and can cause space amplification.

Reference counting, tracing, epochs, or arena generations reclaim shared nodes. Reference increments/decrements and recursive destruction can be costly; batch/epoch retirement may help. Values and labels must also be immutable or versioned. A root pointer alone is not a complete snapshot if referenced mutable value objects change underneath it.

HashiCorp's immutable radix implementation illustrates transactional roots and ordered walks, but its exact API and concurrency guarantees must be read rather than inferred. A mutable ART under a read-write lock, an RCU/copy-on-write radix tree, and a lock-free Patricia algorithm have different linearization and reclamation proofs despite similar diagrams.

Kernel XArray is an indexed radix-derived structure with special entries, marks, locking, and RCU-related APIs. It demonstrates how domain-specific semantics surround a radix layout. It should not be copied as a string map without its contracts, nor treated as proof that arbitrary radix mutations are automatically safe under RCU.

**Persistence must encode labels and topology defensively.** A logical snapshot of canonical key/value pairs is simplest and lets a loader rebuild canonical compression. A physical snapshot can accelerate mapping but must define root, node type/tag, degree, terminal/value, child table, label location/length, widths, byte order, alphabet/canonicalization version, count, and integrity/provenance.

Validate checked `offset+length` before label access, ensure nonempty labels, first-symbol uniqueness, in-range children, acyclic reachability, allowed sharing, canonical nonterminal degree, terminal count/size, subtree metadata, adaptive degree/capacity/tag, increasing Patricia bit positions, key reconstruction, and normalization. Bound nodes, depth, total label bytes, comparisons, diagnostics, and output.

Do not follow a malformed cycle recursively without limits. Use iterative graph validation with visit colors and checked work budget. Ensure every owned node is reachable or explicitly free; duplicated child ownership can double-free during teardown. Checksums detect accidental corruption, while authenticated provenance and authorization address malicious replacement.

Crash-safe in-place split requires durable ordering across new labels/nodes, old child relocation, metadata, and parent pointer. Immutable generation files plus an atomic durable root/manifest are simpler: write, validate, flush, publish, then reclaim old generations after readers drain. A log/replay approach may serialize logical insert/delete and rebuild.

**Security includes prefix leakage and amplification.** Compressed labels reveal common-prefix lengths through timing, traversal, and layout. Do not use a normal radix tree for constant-time secret comparisons. Autocomplete and route tables need authorization/table boundaries before traversal/output. A longest match from the wrong tenant or address family is a correctness and security failure.

Limit key bytes/symbols, label lengths, nodes, fanout, values, snapshot retention, update rate, enumeration, fuzzy states, and diagnostics. Adversarial keys can force repeated near-end label mismatches, high-degree root conversions, allocation churn around ART thresholds, or copy-on-write amplification. Hysteresis between grow/shrink thresholds prevents oscillation.

Canonicalization and Unicode security obligations from DSE-044 remain; compression must never operate on a different representation than lookup. In bit tries, reject noncanonical unused host bits or normalize them under a clear route policy. External label/key buffers must be owned or pinned, never trusted beyond request lifetime.

**Evidence compares reconstructed complete keys.** Use an independent canonical ordered map. Enumerate every root-to-terminal concatenation from the radix structure and compare key/value pairs. Exact, prefix, longest-prefix, insert/update/delete, ordering, size, and counts must match. Expand compressed edges conceptually or in a test helper and compare with a simple uncompressed trie built independently.

Exhaust tiny alphabets and key sets. Force missing first transition; full edge match; mismatch at first, middle, and last label position; new key ending inside old label; old label ending before new key; one key prefixing another; empty key; split of terminal/nonterminal child; deletion of leaf/prefix/branch; and cascading merge. Permute insertion/deletion order and compare logical keys, not physical shape unless canonical shape is promised.

Validate every structural invariant: nonempty labels, unique sibling first symbols, no cycles, reachability/ownership, terminal size, canonical nonroot nonterminal degree, counts, parent links, adaptive capacities/tags, Patricia bit ordering, root exception, and arena accounting. Metamorphic compression then expansion preserves the map; inserting the same pair is idempotent under update policy; deleting absent keys preserves bytes/logical digest when promised; split label concatenations recover original suffixes.

Fault-inject label/node/value allocation, child-container growth, ART conversion, split/merge, mapping, serialization, and root publication. Verify strong/basic guarantees exactly. Concurrency evidence forces readers at each split/merge publication boundary, competing updates to the same prefix, slow snapshot readers, reclamation, and handle-generation failures. Use linearizability histories for point operations and explicit snapshot semantics for walks.

Benchmarks vary key count/length, common-prefix length, mismatch position, alphabet, fanout distribution, terminal density, hit/miss/prefix/longest mix, update/delete ratio, values, and snapshot readers. Measure comparisons, nodes, label bytes, child capacity, allocator bytes, peak split/copy amplification, lookup/output latency distributions, construction, serialization/mapping, cache/TLB/branches, conversion churn, concurrency scaling, and retained generations. Compare uncompressed trie, radix, ART, crit-bit or B-tree/hash alternatives only with equivalent identity and query semantics.

The executable below implements an exact-string mutable radix trie with owned Python labels, terminal/value separation, LCP splitting, deletion pruning and cascading unary merge, longest-prefix match, lexicographic enumeration, and independent reconstruction validation. It demonstrates finite structural cases, not Unicode canonicalization, bitwise Patricia, ART layouts, allocation failure, stable handles, concurrency, persistence, security, or production performance.

<!-- bijux-verify: {"id":"compressed-radix-trie-trace","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"size=5\nroot_edges=r\nexact_roman=3\nprefix_rom=roman:3,romane:1,romanus:2\nlongest_romanuscript=romanus:2\ndelete_romane=True\ndelete_roman=True\nexact_roman_after=None\nroot_edges_after=r\nprefix_ru=rubicon:4,rubicundus:5\nsize_after=3\nnodes_after=6\ninvariant=True\nevidence=finite_compressed_radix_trie_trace\n","stderr":""}} -->
```python
class Node:
    def __init__(self, terminal=False, value=None):
        self.terminal = terminal
        self.value = value
        self.children = {}


def lcp(a, b):
    length = 0
    while length < len(a) and length < len(b) and a[length] == b[length]:
        length += 1
    return length


class RadixTrie:
    def __init__(self):
        self.root = Node()
        self.size = 0

    def insert(self, key, value):
        if key == "":
            node = self.root
        else:
            node = self.root
            position = 0
            while position < len(key):
                first = key[position]
                edge = node.children.get(first)
                if edge is None:
                    node.children[first] = (key[position:], Node(True, value))
                    self.size += 1
                    return True
                label, child = edge
                matched = lcp(label, key[position:])
                if matched == len(label):
                    position += matched
                    node = child
                    continue
                middle = Node()
                old_remainder = label[matched:]
                middle.children[old_remainder[0]] = (old_remainder, child)
                node.children[first] = (label[:matched], middle)
                position += matched
                if position == len(key):
                    middle.terminal = True
                    middle.value = value
                else:
                    new_remainder = key[position:]
                    middle.children[new_remainder[0]] = (new_remainder, Node(True, value))
                self.size += 1
                return True
        created = not node.terminal
        if created:
            self.size += 1
        node.terminal = True
        node.value = value
        return created

    def get(self, key):
        node = self.root
        position = 0
        while position < len(key):
            edge = node.children.get(key[position])
            if edge is None:
                return None
            label, node = edge
            if key[position:position + len(label)] != label:
                return None
            position += len(label)
        return node.value if node.terminal else None

    def items(self):
        result = []

        def visit(node, prefix):
            if node.terminal:
                result.append((prefix, node.value))
            for first in sorted(node.children):
                label, child = node.children[first]
                visit(child, prefix + label)

        visit(self.root, "")
        return result

    def longest_prefix(self, query):
        node = self.root
        position = 0
        best = ("", node.value) if node.terminal else None
        while position < len(query):
            edge = node.children.get(query[position])
            if edge is None:
                break
            label, child = edge
            if query[position:position + len(label)] != label:
                break
            position += len(label)
            node = child
            if node.terminal:
                best = (query[:position], node.value)
        return best

    def delete(self, key):
        node = self.root
        position = 0
        path = []
        while position < len(key):
            edge = node.children.get(key[position])
            if edge is None:
                return False
            label, child = edge
            if key[position:position + len(label)] != label:
                return False
            path.append((node, label, child))
            position += len(label)
            node = child
        if not node.terminal:
            return False
        node.terminal = False
        node.value = None
        self.size -= 1
        for parent, incoming, current in reversed(path):
            first = incoming[0]
            if current.terminal:
                break
            if len(current.children) == 0:
                del parent.children[first]
                continue
            if len(current.children) == 1:
                only_first = next(iter(current.children))
                outgoing, child = current.children[only_first]
                parent.children[first] = (incoming + outgoing, child)
                continue
            break
        return True

    def validate(self):
        seen = set()
        terminals = 0

        def visit(node, is_root):
            nonlocal terminals
            if id(node) in seen:
                return False
            seen.add(id(node))
            if node.terminal:
                terminals += 1
            elif node.value is not None:
                return False
            if not is_root and not node.terminal and len(node.children) < 2:
                return False
            for first, edge in node.children.items():
                label, child = edge
                if label == "" or label[0] != first or not visit(child, False):
                    return False
            return True

        valid = visit(self.root, True)
        return valid and terminals == self.size and len(self.items()) == self.size, len(seen)


trie = RadixTrie()
for key, value in [("romane", 1), ("romanus", 2), ("roman", 3), ("rubicon", 4), ("rubicundus", 5)]:
    trie.insert(key, value)
root_edges = sorted(label for label, _ in trie.root.children.values())
prefix_rom = [(key, value) for key, value in trie.items() if key[:3] == "rom"]
longest = trie.longest_prefix("romanuscript")
deleted_romane = trie.delete("romane")
deleted_roman = trie.delete("roman")
root_edges_after = sorted(label for label, _ in trie.root.children.values())
prefix_ru = [(key, value) for key, value in trie.items() if key[:2] == "ru"]
invariant, nodes = trie.validate()

print("size=5")
print("root_edges=" + ",".join(root_edges))
print(f"exact_roman=3")
print("prefix_rom=" + ",".join(f"{key}:{value}" for key, value in prefix_rom))
print(f"longest_romanuscript={longest[0]}:{longest[1]}")
print(f"delete_romane={deleted_romane}")
print(f"delete_roman={deleted_roman}")
print(f"exact_roman_after={trie.get('roman')}")
print("root_edges_after=" + ",".join(root_edges_after))
print("prefix_ru=" + ",".join(f"{key}:{value}" for key, value in prefix_ru))
print(f"size_after={trie.size}")
print(f"nodes_after={nodes}")
print(f"invariant={invariant}")
print("evidence=finite_compressed_radix_trie_trace")
```

## Definitions and Notation

For alphabet `Sigma`, an edge `e=(u,v)` has nonempty label `lambda(e) in Sigma+`. The spelled sequence of node `v` concatenates edge labels on its root path. `terminal(v)` identifies a stored key. `lcp(a,b)` is longest-common-prefix length. `L` is query symbols, `B` branching nodes visited, `K` keys, `N` physical nodes, and `T` total stored label symbols. A discriminating bit `d(v)` in Patricia form must follow the variant's strict path-order rule.

A canonical fully compressed form permits no nonroot nonterminal unary node. An **owned label** controls its bytes; a **borrowed/sliced label** depends on backing storage; an **inline prefix** stores a bounded beginning within the node. A logical key handle is distinct from a node/edge address and a generation-tagged physical descriptor.

## Mechanisms, Invariants, or Proof Structure

Compression correctness is an expand/contract equivalence: contracting only nonterminal unary chains cannot remove a key or branch, while expanding labels reconstructs a one-symbol trie with identical terminals. Lookup correctness composes unique first-symbol selection with full edge-label equality. LCP insertion proves the common edge plus two maximally differing remainders spell exactly old and new suffixes. Deletion merge is valid only because no key ends at the unary node.

Engineering proof layers add label lifetime, fallible replacement, metadata, adaptive node-type capacity, discriminating-bit order, snapshot generation, publication, reclamation, and persistent offset graph. These do not follow from logical string preservation and require independent validators/evidence.

## Alternatives and Trade-Offs

| Design | Natural strength | Primary obligation |
|---|---|---|
| compressed string radix | shared textual/path prefixes | label comparison and split/merge |
| binary Patricia | bounded discriminating-bit branches | bit order, prefix/end convention |
| crit-bit | compact exact byte-string dictionary | full-leaf equality and update protocol |
| ART | varied byte fanout in memory | node conversion and prefix reconstruction |
| immutable radix | snapshots and transactions | copy amplification and reclamation |
| double-array/static trie | compact indexed transitions | construction/relocation and rigid updates |
| FST/minimal automaton | static keys with suffix-state sharing | ordered build/output algebra/rebuild |
| uncompressed trie | simplest mutation and per-symbol nodes | node/pointer memory and indirection |

Selection follows key/alphabet distribution, mismatch positions, fanout, query mix, ordering, mutation/snapshot rate, handle needs, machine, serialization, and actual byte evidence.

## Failure Modes and Misconceptions

- Path compression removes nodes, not the requirement to compare distinguishing symbols.
- A query ending inside a label may be a conceptual prefix but is not an exact stored key.
- A terminal unary node cannot be merged without erasing a prefix key.
- LCP split metadata/value movement is as important as label slicing.
- Borrowed labels are safe only while immutable backing storage remains alive.
- ART's node names and thresholds are implementation choices, not universal performance guarantees.
- Patricia bit indices require strict representation/end-of-key conventions.
- Immutable roots do not make referenced mutable values into snapshots.
- Lazy deletion can preserve answers while violating canonical compression and memory targets.
- A finite split/merge trace proves neither Unicode, allocation failure, concurrency, persistence, nor workload performance.

## Worked Examples

### Example 1

Inserting `team` into edge `tear` finds LCP `tea`; intermediate edge `tea` receives children `m` and `r`. Since neither key ends at `tea`, the intermediate node is nonterminal with degree two and satisfies canonical compression.

### Example 2

Inserting `tea` into existing edge `tear` splits at `tea` and marks the intermediate node terminal, with child `r` retaining the old terminal/value. This is the key-ending-inside-old-label case.

### Example 3

Inserting `tearing` after `tear` matches the full old edge and continues at its terminal child, adding edge `ing`. No split of `tear` is needed; the node can be terminal and branching.

### Example 4

Deleting `tear` while `tearing` remains clears terminal. The now nonterminal unary node may merge incoming `tear` with outgoing `ing` to `tearing`. Deleting `tearing` while `tear` remains must not merge through the terminal `tear` node.

### Example 5

A failed query shares 1,000 of 1,001 label bytes. Compression removes pointer hops but still compares about 1,001 bytes. Prefix-skew and mismatch position belong in benchmarks and denial-of-service limits.

### Example 6

A Patricia node tests bit 17. If a child later tests bit 12 under a strictly increasing convention, the persisted structure is invalid even if pointers are in range; lookup can revisit semantic positions or route incorrectly.

### Example 7

An IPv4 prefix `192.0.2.7/24` canonicalizes to network bits for `192.0.2.0/24` under a masking policy. Treating host bits as separate route identity can create duplicate ambiguous prefixes.

### Example 8

An ART node grows from a small packed representation to a larger indexed one. All child pointers, count, compressed prefix, terminal/value, and parent publication must transfer; a raw pointer to the old node invalidates.

### Example 9

Copy-on-write insertion clones four nodes and shares two large subtrees. A reader pinned to the old root sees neither partial nodes nor the new key, but old storage cannot be reclaimed until that reader releases its generation.

### Example 10

A persisted label offset and length each fit 64 bits but their sum overflows. Checked addition, region containment, total-label budget, graph validation, and provenance verification precede any comparison or UTF-8 decoding.

## Cross-Program Connections

- **Database engineering:** ART, prefix-compressed indexes, immutable generations, and crash-safe root publication connect to main-memory and storage indexes.
- **Networking:** Patricia/radix longest-prefix tables require address-family, prefix-length, canonical masking, policy, and atomic update semantics.
- **Operating systems:** indexed radix structures such as XArray add marks, special entries, locking, RCU, and memory-lifecycle contracts.
- **Concurrent programming:** replacement publication, path copying, CAS/locks, generation readers, and reclamation determine safety.
- **Security engineering:** prefix timing/leakage, hostile labels/offsets, tenant route tables, resource amplification, and canonical identity matter.
- **Computer architecture:** adaptive fanout, SIMD label comparison, pointer width, cache lines, branches, and TLB behavior shape performance.
- **Testing/reliability:** expansion equivalence, exhaustive LCP cases, corrupted graphs, crash injection, and retained-generation tests generalize broadly.

## References

1. [Viktor Leis, Alfons Kemper, and Thomas Neumann, *The Adaptive Radix Tree: ARTful Indexing for Main-Memory Databases*](https://db.in.tum.de/~leis/papers/ART.pdf).
2. [D. J. Bernstein, *Crit-bit trees*](https://cr.yp.to/critbit.html).
3. [Armon Dadgar, `libart` maintained source](https://github.com/armon/libart).
4. [HashiCorp, `go-immutable-radix` maintained source](https://github.com/hashicorp/go-immutable-radix).
5. [Linux kernel documentation, *XArray*](https://docs.kernel.org/core-api/xarray.html).
6. [Rust `radix_trie` crate documentation](https://docs.rs/radix_trie/latest/radix_trie/).
7. [IETF RFC 4632, *Classless Inter-domain Routing (CIDR)*](https://datatracker.ietf.org/doc/html/rfc4632).
8. [Princeton Algorithms, *Tries*](https://algs4.cs.princeton.edu/52trie/).

## Exercises

### Exercise 1

Starting empty, insert `a`, `atom`, `at`, `atlas`, and `bar` into a canonical radix trie. Give one valid compressed topology with terminals, then delete `atom` and `at` in order and show safe pruning/merging.

### Exercise 2

Prove the complete LCP split case where `0<j<|old_label|` and the new key continues beyond `j`. State why the two remainder first symbols differ and why old keys/values remain reachable.

### Exercise 3

Design label ownership and strong failure semantics for a mutable radix map with large keys and values. Compare owned strings, arena slices, and inline-prefix/external-tail storage during split, merge, deletion, and compaction.

### Exercise 4

Specify an IPv4/IPv6 Patricia longest-prefix table API. Include key canonicalization, duplicate route policy, default route, next-hop/metric metadata, snapshot updates, handle identity, invalid input, and validation.

### Exercise 5

Design evidence comparing uncompressed trie, compressed radix, ART, and immutable radix for a read-heavy service. Include logical equivalence, exhaustive structural cases, failures/concurrency/persistence, workloads, byte accounting, and claims you cannot make from the results.

## Answers to the Exercises

### Answer 1

Root has edges `a` and `bar`; `bar` ends terminal. Edge `a` reaches a terminal node for `a`, whose sole edge `t` reaches terminal `at`. That node has edges `om` to terminal `atom` and `las` to terminal `atlas`. Terminal unary nodes remain because shorter keys exist. Delete `atom`: remove edge `om`; `at` remains terminal with child `las`. Delete `at`: clear its terminal; it is now nonterminal unary, so merge incoming `t` and outgoing `las` into `tlas` beneath terminal `a`. Keys `a`, `atlas`, and `bar` remain.

### Answer 2

Let old edge be `q` to subtree `T`, new remaining suffix `s`, and `j=lcp(q,s)` with `0<j<|q|` and `j<|s|`. Replace the parent edge by `q[:j]` to new node `M`. Add edge `q[j:]` from `M` to unchanged `T`, and edge `s[j:]` to a new terminal. For every old terminal, concatenation replaces `q` by `q[:j]+q[j:]=q`, preserving its full spelling/value. The new path concatenates to `s`. If remainder first symbols were equal, the common prefix would extend beyond `j`, contradicting maximal LCP. `M` is nonterminal degree two unless another explicit key ends there.

### Answer 3

Owned labels simplify lifetime but substring/merge copies and peak memory can be large. Prepare all new labels, nodes, child maps, and fallible value operations privately, then replace one parent edge; failure destroys private state. Arena slices make splitting cheap and pin backing keys until generation destruction, but concatenated merge may need a slice from a descendant full key or a new allocation; individual deletes do not reclaim space. Inline prefixes keep common bytes local and place overflow in immutable key storage, requiring authoritative full-key comparison and replacement-leaf rules. Handles carry generations. Compaction constructs a validated new arena/tree and atomically publishes it; slow readers retain old arenas. State whether merge may be lazy to avoid fallible deletion, and measure peak old+new+temporary bytes.

### Answer 4

Tag address family and store fixed network-order bits plus prefix length bounded to 32 or 128. Canonicalize by masking host bits; reject or normalize noncanonical input consistently. Key identity is `(family,table_or_VRF,network,prefix_length)`. Duplicate insertion replaces, rejects, or versions a route explicitly. Length zero is a per-family/table default at root. Terminal metadata contains stable route ID, next hop, metric, policy, and generation; internal node addresses are not handles. Build updates privately/copy-on-write and publish a table generation so lookup sees one snapshot; validate discriminating-bit order, bounds, canonical masks, unique prefixes, terminals/metadata/counts, reachability, and provenance. Reject malformed addresses, lengths, tables, unauthorized updates, and resource excess.

### Answer 5

Use one canonical ordered map and compare reconstructed complete key/value sets, exact/prefix/longest results, ordering, size, and update policy for every structure. Exhaust LCP insertion/end-inside, terminal unary, leaf/prefix/internal deletion, cascading merges, adaptive conversions, empty/maximum keys, and all tiny key subsets/permutations. Inject allocation/value/conversion/publication failure; corrupt serialized offsets/labels/tags/graphs; crash at durable steps; force split/delete/read races, snapshot retention, handle generation, and reclamation. Benchmark governed real and synthetic keys varying length, common prefix, mismatch position, fanout, query/update/output mix, values, snapshots, and concurrency. Measure resident/peak/allocator/label bytes, comparisons, cache/TLB/branches, latency distributions, construction, mapping, conversion churn, and retained versions. Results are platform/workload evidence only; they do not prove universal superiority, Unicode/security correctness, lock freedom, crash safety, or deployment fitness without the corresponding independent review.
