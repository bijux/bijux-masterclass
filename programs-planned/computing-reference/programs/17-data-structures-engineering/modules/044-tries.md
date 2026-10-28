---
module_id: DSE-044
program: Data Structures Engineering
level: 1
module_number: 44
title: Tries
status: complete
last_verified: 2026-08-30
---

# Tries

## One-Page Review

### Governing question

How should an engineer represent a set or map of sequences so lookup, prefix navigation, ordering, Unicode semantics, memory layout, mutation, and production evidence agree?

### Essential definitions

- A **trie** is a rooted tree whose root-to-node path spells a sequence prefix and whose terminal markers identify stored keys.
- An **alphabet** is the domain of one logical key unit: bytes, Unicode code points, grapheme clusters, tokens, bits, or another symbol set.
- A **terminal marker/value** distinguishes a complete key from a prefix that exists only as a path.
- A **child representation** maps the next symbol to a child: fixed array, sorted vector, hash table, bitmap-plus-packed array, or adaptive node.
- A **radix/Patricia trie** compresses chains of single-child nonterminal nodes into labeled paths.
- A **longest-prefix match** returns the deepest stored key that prefixes a query.
- A **double-array trie** encodes transitions in indexed `base`/`check` arrays.
- A **finite-state transducer (FST)** can share equivalent suffix states in an immutable ordered key mapping and emit values/outputs.
- **normalization** maps textual variants to a chosen canonical representation; it is separate from case, locale, and grapheme policy.
- A **snapshot generation** binds iterators/node handles to one physical trie version.

### Central model, mechanism, or theorem

For a key of length `L` measured in the declared alphabet, exact lookup follows at most `L` transitions and checks terminal state, so its algorithmic cost is `Theta(L)` plus child-lookup costs. Prefix navigation reaches the prefix node similarly; enumerating `k` output symbols then costs proportional to traversed representation and output. These bounds are independent of the total number of keys only when transition lookup is bounded as assumed.

Each trie node represents a unique prefix in the uncompressed model. Insertion creates missing transitions and marks the final node terminal. Deletion clears the terminal/value and prunes upward only while a node is nonterminal and childless. A key may be a prefix of another, so childlessness is not the same as nonmembership. Path compression reduces nodes and pointers but makes matching, splitting, deletion, and handles more complex.

The alphabet and canonicalization define identity. UTF-8 bytes, Unicode code points, and user-perceived grapheme clusters produce different paths and lengths. Canonically equivalent text does not compare equal unless normalized. A production trie must apply one versioned canonicalization policy at every operation boundary or store exact bytes intentionally.

### Critical invariants

1. The key-unit alphabet, encoding, normalization, case/locale, empty-key, and invalid-input policies are explicit and identical for insert, lookup, prefix, delete, and persistence.
2. Every child transition has a unique symbol under its parent and points to exactly one owned/reachable node or valid immutable state.
3. A terminal marker/value exists exactly for stored canonical keys, including keys that are prefixes of longer keys.
4. The stored size counts terminal keys, not allocated nodes, prefixes, values, or insertion attempts.
5. Deletion prunes no node needed by another terminal key and leaves no unreachable owned nodes except allowed arena garbage.
6. Compressed edge labels are nonempty; outgoing labels from one node begin with distinct symbols; split/merge preserves spelled keys.
7. Ordering promises follow declared symbol collation, not incidental hash iteration or host locale.
8. Subtree counts, top-k caches, parent links, memory offsets, and other derived metadata agree with terminal membership.
9. Publication, iteration, serialization, and reclamation expose one coherent generation and reject malformed cycles/offsets/lengths.

### Common failures

- Treating every reached prefix node as a present key without checking terminal state.
- Clearing a terminal and deleting its subtree even though longer keys remain.
- Pruning a node that is still terminal for a shorter key.
- Mixing byte lengths, code-point lengths, and user-visible character counts.
- Normalizing only on insertion, so lookups cannot find stored canonical keys.
- Case-folding identifiers whose domain requires exact or locale-specific identity.
- Assuming hash-backed child traversal is lexicographic.
- Allocating a full Unicode-sized child array per node.
- Exposing node pointers or path slices that compaction/splitting invalidates.
- Claiming `O(L)` without stating transition structure, output cost, and canonicalization cost.

### Compact example

A code-point trie normalizes inputs with Unicode NFC plus locale-independent case folding. `Cat`, `car`, `cart`, `café`, and `dog` produce five keys. Inserting decomposed `cafe` plus combining acute updates the existing `café` value rather than adding a sixth key. Prefix `ca` has four keys. Removing `car` preserves `cart`; longest-prefix lookup for `cartwheel` remains `cart`. Independent traversal verifies size, unique paths, terminals, and reachability.

### Connections

[DSE-005](005-contiguous-and-linked-layouts.md), [DSE-006](006-memory-locality-and-cache-behavior.md), and [DSE-007](007-genericity-and-type-constraints.md) provide layout, locality, and symbol constraints. [DSE-031](031-binary-search-trees.md) supplies an ordered comparison-tree alternative; [DSE-022](022-separate-chaining.md) through [DSE-030](030-engineering-a-memory-efficient-hash-map.md) supply child-container trade-offs. The [program roadmap](../ROADMAP.md) continues with compressed radix trees, suffix structures, traversal, connectivity, and production storage.

## Governing Question

Which sequence identity, alphabet, canonicalization, transition layout, compression, query set, ordering, mutation model, snapshot semantics, and persistence format make a trie correct and worthwhile for the target workload?

## Why This Matters

Tries align representation with shared prefixes. Dictionaries, autocomplete, routing tables, token vocabularies, configuration paths, spell checking, lexical analysis, IP prefix routing, and search indexes all need operations that hashes and comparison trees do not provide as directly. Exact lookup follows the query itself; prefix enumeration begins at the prefix state; longest-prefix match remembers the deepest terminal along one traversal.

The simple picture—one node per character—hides most engineering decisions. What is a character? How are canonically equivalent Unicode strings treated? Are case and locale part of identity? Must results use byte order, Unicode scalar order, locale collation, insertion order, frequency, or a scoring model? Does every node allocate hundreds of child pointers? Can keys change while readers enumerate? Are returned handles stable? Is an immutable FST better than a mutable pointer tree?

Memory dominates many trie deployments. Uncompressed nodes can multiply allocator headers, pointers, hash capacity, and alignment across every prefix. Long common prefixes help sharing, but long unique suffixes create single-child chains. Radix compression, adaptive nodes, double arrays, succinct encodings, arenas, and FST minimization trade mutation simplicity for compactness and locality. Performance claims require actual bytes and workloads, not only `Theta(total key symbols)`.

Text identity is a correctness and security boundary. Visually similar sequences may have different code points; canonically equivalent sequences may have different encodings; case behavior can expand a character or depend on locale; invalid byte sequences need policy. A trie cannot repair an undefined key model. This module establishes that model first, then derives representation and evidence.

## Prerequisites and Retrieval

Retrieve ADT/representation separation from [DSE-001](001-abstract-data-types-and-concrete-representations.md), invariants and contracts from [DSE-002](002-representation-invariants.md) and [DSE-003](003-operation-contracts.md), byte and sequence costs from [DSE-004](004-time-space-and-allocation-cost.md), and locality from [DSE-005](005-contiguous-and-linked-layouts.md) and [DSE-006](006-memory-locality-and-cache-behavior.md). Retrieve generic symbol constraints from [DSE-007](007-genericity-and-type-constraints.md), iterator invalidation from [DSE-008](008-iterators-and-traversal-protocols.md), property testing from [DSE-009](009-property-based-testing-of-data-structures.md), and workload measurement from [DSE-010](010-benchmarking-a-structure-without-misleading-results.md).

## Learning Objectives

After completing this module, you should be able to:

1. define trie identity over bytes, code points, graphemes, tokens, or bits;
2. implement exact lookup, insert/update, deletion/pruning, prefix enumeration, and longest-prefix match;
3. prove terminal, transition, size, and reachability invariants;
4. derive costs in query units and include child lookup, canonicalization, and output;
5. select fixed, sorted, hashed, bitmap-packed, adaptive, or compressed transitions;
6. apply Unicode normalization/case policy consistently without confusing collation;
7. specify iterator/handle invalidation, concurrency, snapshot, and reclamation behavior;
8. design a versioned persistent format and validate hostile inputs;
9. compare mutable tries, radix trees, double arrays, and immutable FSTs; and
10. build reference, metamorphic, fault, Unicode, and workload evidence.

## Core Exposition

**Define the sequence domain before implementing nodes.** A trie accepts sequences over an alphabet `Sigma`. For binary routing, one symbol may be a bit. For ASCII commands, a byte can be appropriate. For arbitrary UTF-8 text, byte tries are valid and often compact, but prefix lengths and transition ordering are byte-based. Code-point tries decode first and represent Unicode scalar values. Grapheme-cluster tries align more closely with user-perceived characters but require a segmentation algorithm and version; clusters are variable sequences themselves.

Token tries operate on words, path components, protocol fields, or compiler symbols. Their child keys may be interned IDs rather than strings. The cost variable `L` must say which units it counts. A claim that lookup costs `O(L)` is incomplete when decoding, normalization, tokenization, or grapheme segmentation also processes the input and may allocate.

Choose whether the empty sequence is legal. If legal, the root can be terminal and store its value. This is useful for a default route or empty token but easy to omit from enumeration and size. If forbidden, reject it uniformly. Invalid encoding, overlong key, embedded null, forbidden separators, and resource-limit failures also need one operation contract.

For text, Unicode normalization forms such as NFC or NFKC answer canonical/compatibility equivalence; they do not answer case, locale collation, confusables, or grapheme boundaries. NFC commonly composes canonically equivalent sequences. NFKC can intentionally collapse compatibility distinctions and is unsuitable for domains where those distinctions matter. Case folding may expand text and is not a universal identifier policy. Apply the exact same versioned transformation on insert, lookup, prefix, delete, and persisted-key import.

Prefix semantics occur after or before normalization according to contract. Normalizing the complete query can alter code-point boundaries. A UI accepting incrementally typed text may need a raw-input layer before canonical lookup. Locale-aware autocomplete ordering is different from identity: store canonical keys, retain display forms separately, and sort results with a declared collation/version if required.

Security policy may go beyond equality. Confusable detection, script restrictions, bidirectional controls, and tenant namespaces belong at admission, not inside an unchecked transition loop. Preserve original display/audit text when needed, but do not let two subsystems canonicalize differently and then share a trie as if identities agreed.

**An uncompressed trie has one node per represented prefix.** The root represents the empty prefix. A transition labeled `a` from prefix `p` reaches prefix `p+a`. Each node has child transitions plus terminal/value state. Terminal cannot be inferred from leaf status: if keys `car` and `cart` exist, the `car` node is terminal and has a child.

Exact lookup canonicalizes the key, begins at root, and follows each symbol. A missing transition means absent. Reaching the last symbol means present only if the node is terminal. Returning “prefix exists” as exact membership is a classic false positive. Conversely, a terminal may hold an optional/nullable application value, so use a separate terminal bit when null is a legal stored value.

Insertion walks existing transitions and allocates missing nodes. At the final node, update or reject according to duplicate policy; size increases only on nonterminal-to-terminal transition. Strong failure semantics build missing suffix nodes privately or log created links so allocation/value-construction failure leaves no published partial path. Or permit harmless nonterminal prefixes under a documented basic guarantee, but account for memory and validation.

Deletion reaches the final node, returns false if absent/nonterminal, destroys or returns its value under ownership policy, clears terminal, and decrements size. Then walk toward the root, removing a child only when that child is nonterminal and has no children. Stop at the first needed node. Without parent pointers, retain a stack of `(parent,symbol,node)` during descent. Parent pointers speed ascent but cost a pointer per node and complicate moves/persistence.

Pruning proofs are local. A nonterminal childless node spells no stored key and is unnecessary. A terminal node represents a shorter stored key and must remain even if childless. A node with any child lies on a longer key and must remain even if nonterminal. Removing only unnecessary suffix nodes preserves exactly every other root-to-terminal path.

Prefix lookup follows the canonical prefix. If missing, return empty. Otherwise enumerate terminals in the subtree. Complexity is traversal plus output; returning a million matches is at least linear in output. APIs need limit, pagination/cursor, cancellation, scoring, and snapshot behavior. A depth-first iterator can maintain a stack instead of materializing results, but mutation may invalidate nodes and ordering.

Longest-prefix match traverses a query while remembering the most recent terminal. It returns the deepest stored key on the path, not the lexicographically closest key. IP routing uses bit prefixes; URL routers may use component/token prefixes and wildcards, which add transition precedence. The root terminal can serve as a default match.

**Child layout determines constants and sometimes asymptotics.** A fixed array indexed by symbol offers constant transition access but uses `|Sigma|` slots at every node. It is excellent for small fixed alphabets and wasteful for Unicode code points or sparse branching. Even 256 pointers per byte-trie node can overwhelm key bytes when most nodes have one child.

A sorted vector stores only existing `(symbol,child)` pairs, supports binary search `O(log degree)`, streams compactly, and enumerates lexicographically. Insert/delete shifts elements. A hash table gives expected constant lookup and update but has capacity/hash overhead, adversarial considerations, and unspecified order. Small linear vectors can beat both for low degrees due to locality.

Bitmap-plus-packed children uses a bitmap for a bounded alphabet and a dense child-pointer vector. Test a symbol bit; rank/popcount before it gives the packed index. This supports ordered enumeration and compact sparse nodes, with bitmap cost proportional to alphabet range. Multi-level bitmaps or encoded symbols extend the idea.

Adaptive radix trees select node formats by degree—for example tiny sorted arrays, medium indexed/bitmap layouts, and dense arrays—growing or shrinking at thresholds. They also compress paths. This improves space and cache use across skewed fanout, while node conversions need failure safety, publication, and handle invalidation. Thresholds are empirical design choices, not universal constants.

Actual memory includes node header, terminal/value/tag, child representation object, capacity slack, pointers/offsets, allocator metadata, alignment, labels, parent links, counters, and external/display keys. Calculate resident and peak build/update bytes. Arena allocation reduces per-node overhead and makes whole-generation destruction cheap, but individual deletion may only unlink nodes and leave space until rebuild.

**Radix compression collapses unary paths.** In a Patricia/radix trie, an edge can carry a nonempty sequence rather than one symbol. Outgoing labels from a node must begin with distinct symbols, so the next transition remains unambiguous. Lookup compares the query against an edge label until mismatch, label exhaustion, or query exhaustion.

Insertion may split an edge. If existing label is `romane` and inserted suffix is `romanus`, their common prefix `roman` becomes a new intermediate path; remaining labels `e` and `us` become children. If a key ends inside an edge, split there and mark the new node terminal. All values, subtree counts, and ownership must move consistently.

Deletion can merge a nonterminal single-child node with its child by concatenating labels, unless handle, parent, paging, or concurrency contracts forbid it. Label concatenation can allocate and fail; store slices into immutable key arenas, small inline prefixes plus external remainder, or perform copy-on-write. Compressed tries reduce nodes but increase comparisons and split/merge complexity.

Patricia bit tries choose the discriminating bit position rather than storing every bit node. They support longest-prefix/routing designs but require exact bit ordering, prefix-length validation, and address-family separation. “Radix tree,” “Patricia trie,” and “compressed trie” are used inconsistently across libraries; rely on stated invariants rather than names.

Double-array tries map transitions into `base` and `check` arrays. A parent chooses a base offset such that each outgoing symbol lands in a free slot; `check[next]` confirms the parent. They eliminate pointers and can be compact/cache-friendly, especially for mostly static dictionaries, but relocation and finding collision-free bases complicate mutation. Malformed persisted indices demand checked arithmetic and range validation.

Immutable finite-state structures can merge equivalent suffix states, sharing more than prefixes. A minimal acyclic automaton represents a static key set; an FST attaches outputs. Building from sorted keys can be streaming and compact. Immutability enables mapping and lock-free reads, but arbitrary updates require rebuilding, layers/deltas, or a mutable front structure. FST output algebra and serialization are separate correctness subjects.

**Ordering is a contract.** Fixed arrays or sorted children naturally enumerate in declared symbol order. Hash children do not. Unicode code-point order is not human locale collation. UTF-8 byte order has useful correspondence properties for scalar values but does not implement language-sensitive dictionary order. Frequency-ranked autocomplete is not lexicographic; it requires scores, subtree top-k caches, or collecting candidates then ranking.

Subtree terminal counts answer prefix counts and help pagination/rank. On a new insertion, increment the count along its path; on update, do not. On successful deletion, decrement. Compressed paths count at nodes or edges according to one convention. A failed or redundant operation must not drift counts. Recompute counts bottom-up in validation.

Top-k caches combine candidate scores from terminals/children. Score updates may touch all ancestors and ties need deterministic rules. Stale caches can return plausible wrong autocomplete. Version scores or rebuild caches; cap memory by selected nodes/degrees. Personalized ranking and access control should not leak candidates through a globally shared cache.

Wildcards, edit distance, fuzzy prefix, and regex queries explore multiple states. Their cost can grow with branching, pattern length, edit budget, and output. A trie prunes impossible prefixes but does not make exponential or combinatorial searches free. Bound state expansions and output, especially for untrusted patterns.

**Iteration and handles need generation semantics.** A DFS iterator stores nodes/child positions. In-place insertion can reallocate a child vector; deletion can free a node; radix split can replace it. Choose fail-fast modification counters, exclusive mutation, stable arena IDs, reference-counted immutable nodes, or snapshot iteration. Document whether values can mutate during traversal.

Returning a pointer to the caller's query buffer as an edge label is unsafe. Own or intern keys, copy labels, or tie borrowed memory to a longer-lived immutable arena. Returning internal mutable key slices lets callers violate ordering/transition invariants. Expose immutable views with explicit lifetime.

Immutable copy-on-write tries publish a new root after cloning the affected path; readers pin old roots. Shared subtrees require reference counting, tracing, epochs, or arenas per generation. Updates allocate `O(L)` nodes before compression/layout effects, which is attractive for snapshots but can amplify memory under slow readers.

A coarse reader-writer lock is the baseline mutable concurrency design. Reads include exact/prefix traversal; writes hold exclusive access through allocation and publication. Fine-grained node locks require a global order, validation after lock coupling, safe deletion, and careful compressed-edge splitting. Lock-free tries use tagged/immutable nodes and CAS protocols; safe reclamation is inseparable.

Linearization differs by operation. Insertion might take effect when the final terminal/value publishes after the path is reachable; deletion when terminal clears, followed by physical pruning. A reader must not observe terminal true with an uninitialized value. Subtree counts/top-k metadata can publish before, after, or transactionally; their consistency promise determines correctness.

**Persistence needs a logical and physical schema.** A portable logical format stores canonical keys and values plus normalization/collation/version policy, then rebuilds. It is simple and robust but may cost startup time. A physical snapshot stores node/edge arrays, offsets, labels, terminal bits, values, counts, and root index for memory mapping. It must specify magic, version, byte order, widths, encoding, normalization version, ordering flags, and checksums/authentication.

Validate all file-relative offsets and length arithmetic before slicing. Ensure indices lie in bounds; labels are nonempty where required; transition symbols/leading symbols are unique; graph is acyclic/root-reachable; every owned node is reachable exactly as the format requires; terminal/value shapes agree; size and subtree counts recompute; canonical keys obey policy; and traversal cannot exceed resource limits. A trie file is a graph-shaped parser target, not trusted because it is read-only.

Crash-safe updates commonly use a log plus rebuild, copy-on-write pages with atomic root publication, or immutable generation files referenced by a durable manifest. In-place multi-node radix splits are difficult to make crash-consistent. Absolute pointers cannot survive remapping; use offsets/IDs. Persisting normalized keys without the transformation version can change identity after Unicode/library upgrades.

**Security and reliability follow from identity plus bounds.** Limit key length in bytes and symbols, admitted keys, total nodes/label bytes, per-node degree, autocomplete output, wildcard state expansions, and diagnostics. A huge common prefix can force long work on every query even when key count is small. A flood of unique first symbols targets dense/adaptive roots and mapping memory.

Invalid UTF-8 can be rejected, replaced, or treated as bytes, but never inconsistently. Normalization expansion and case-fold expansion need checked buffer limits. Confusables and mixed scripts can create phishing identifiers even after NFC. NFKC may collapse security-relevant distinctions or, in a carefully designed identifier profile, intentionally reduce them. Domain policy and Unicode security review remain external to core trie correctness.

Hash-backed children inherit collision attacks. Compressed-label comparisons can leak timing proportional to common-prefix length when keys are secrets; tries generally reveal prefix structure through memory/access patterns. Do not use an ordinary trie as a constant-time secret lookup. Tenant and authorization filters must apply before autocomplete output and caches.

**Evidence needs an independent map and canonicalizer.** For manageable cases, use a reference ordered map from canonical full key to value. After every generated insert/update/delete, compare exact membership/value, size, prefix-filtered results, and longest-prefix answer. The reference should filter complete strings rather than emulate trie nodes.

Validate reachability and uniqueness by DFS. Reconstruct every root-to-terminal key and compare the reference map. Check distinct child symbols or first-symbol labels, nonempty compressed labels, no cycles/shared mutable child unless allowed, node ownership, subtree counts, sortedness flags, and no prunable nonterminal leaf after deletion. For arena designs, distinguish unreachable-but-owned garbage from a leak.

Exhaust tiny alphabets and keys: empty universe, empty key, one key, one-symbol keys, a key and its prefix, several keys sharing all but last symbol, no common prefix, duplicate update/reject, deletion leaf/prefix/internal/absent, and last child. Enumerate all small key subsets and operation permutations. For radix tries, force mismatch at first/middle/last label symbol and key ending inside a label.

Unicode vectors include composed/decomposed canonical equivalents, combining-mark sequences, case expansions, non-BMP scalars, emoji sequences, grapheme clusters, mixed scripts, invalid bytes, empty normalized output if policy allows, and versioned expected results from Unicode data. Test raw display preservation independently from canonical identity. Differential testing across libraries is useful only after matching policies.

Metamorphic properties include insert-then-find, update preserving size, delete-then-absence, delete of a prefix preserving descendants, deletion of a descendant preserving prefix, permutation-independent logical map, canonical-equivalent inputs resolving equally under the chosen policy, prefix results all beginning with the canonical prefix, and longest-prefix result being terminal and no shorter than any other stored prefix of the query.

Fault injection targets node/label/value/map allocation, normalization, child-layout conversion, compressed-edge split/merge, count/cache update, serialization, and publication. Concurrency evidence uses linearizable histories for point operations, specified snapshot/fail-fast behavior for enumeration, forced split/delete/read races, reclamation sanitizers, stalled readers, and generation retirement. Persistence evidence mutates every index/length/count and crash-injects every durable step.

Benchmarks vary key count, byte/symbol length, common-prefix distribution, alphabet/fanout, terminal density, hit/miss/prefix mix, result limit, update/delete ratio, normalization, values, and query popularity. Compare exact lookup, prefix seek, bounded enumeration, longest-prefix, construction, peak/resident bytes, update amplification, serialization/mapping, cold/warm cache, and concurrent scaling. Record node/child formats and actual distributions; a URL corpus, random bytes, and natural-language vocabulary stress different designs.

The executable below implements a mutable Unicode-code-point trie with a deliberately fixture-bounded canonicalizer: locale-independent case folding plus the one composed/decomposed acute-accent equivalence exercised by the trace. Production code must replace that illustrative function with the versioned Unicode policy described above. The trie demonstrates hash children, terminal/value separation, prefix counts by traversal, lexicographically sorted enumeration, longest-prefix match, deletion pruning, and an independent structural validator. It does not validate general Unicode normalization, any locale/security profile, compressed layout, concurrency, persistence, memory usage, or production performance.

<!-- bijux-verify: {"id":"trie-operations-trace","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"size=5\nlookup_CAT=5\nnormalized_update=10\nprefix_ca=4\nautocomplete_car=car:4,cart:7\nlongest_cartwheel=cart:7\ndelete_car=True\nlookup_car=None\nautocomplete_car_after=cart:7\nsize_after=4\nroot_children=c,d\ninvariant=True\nevidence=finite_trie_operations_trace\n","stderr":""}} -->
```python
def canonical(text):
    folded = text.casefold()
    return "caf\u00e9" if folded == "cafe\u0301" else folded


class Node:
    def __init__(self):
        self.children = {}
        self.terminal = False
        self.value = None


class Trie:
    def __init__(self):
        self.root = Node()
        self.size = 0

    def insert(self, key, value):
        node = self.root
        for symbol in canonical(key):
            node = node.children.setdefault(symbol, Node())
        created = not node.terminal
        if created:
            self.size += 1
        node.terminal = True
        node.value = value
        return created

    def get(self, key):
        node = self.root
        for symbol in canonical(key):
            node = node.children.get(symbol)
            if node is None:
                return None
        return node.value if node.terminal else None

    def items_with_prefix(self, prefix):
        text = canonical(prefix)
        node = self.root
        for symbol in text:
            node = node.children.get(symbol)
            if node is None:
                return []
        result = []

        def visit(current, suffix):
            if current.terminal:
                result.append((text + suffix, current.value))
            for symbol in sorted(current.children):
                visit(current.children[symbol], suffix + symbol)

        visit(node, "")
        return result

    def longest_prefix(self, query):
        node = self.root
        best = ("", node.value) if node.terminal else None
        consumed = ""
        for symbol in canonical(query):
            node = node.children.get(symbol)
            if node is None:
                break
            consumed += symbol
            if node.terminal:
                best = (consumed, node.value)
        return best

    def delete(self, key):
        node = self.root
        path = []
        for symbol in canonical(key):
            child = node.children.get(symbol)
            if child is None:
                return False
            path.append((node, symbol, child))
            node = child
        if not node.terminal:
            return False
        node.terminal = False
        node.value = None
        self.size -= 1
        for parent, symbol, child in reversed(path):
            if child.terminal or child.children:
                break
            del parent.children[symbol]
        return True

    def validate(self):
        seen = set()
        terminals = 0

        def visit(node):
            nonlocal terminals
            if id(node) in seen:
                return False
            seen.add(id(node))
            if node.terminal:
                terminals += 1
            elif node.value is not None:
                return False
            return all(len(symbol) == 1 and visit(child) for symbol, child in node.children.items())

        return visit(self.root) and terminals == self.size


trie = Trie()
for key, value in [("Cat", 5), ("car", 4), ("cart", 7), ("caf\u00e9", 9), ("dog", 3)]:
    trie.insert(key, value)
trie.insert("cafe\u0301", 10)
before = trie.items_with_prefix("car")
longest = trie.longest_prefix("cartwheel")
prefix_ca = len(trie.items_with_prefix("ca"))
deleted = trie.delete("car")
after = trie.items_with_prefix("car")

print(f"size=5")
print(f"lookup_CAT={trie.get('CAT')}")
print(f"normalized_update={trie.get('caf\u00e9')}")
print(f"prefix_ca={prefix_ca}")
print("autocomplete_car=" + ",".join(f"{key}:{value}" for key, value in before))
print(f"longest_cartwheel={longest[0]}:{longest[1]}")
print(f"delete_car={deleted}")
print(f"lookup_car={trie.get('car')}")
print("autocomplete_car_after=" + ",".join(f"{key}:{value}" for key, value in after))
print(f"size_after={trie.size}")
print("root_children=" + ",".join(sorted(trie.root.children)))
print(f"invariant={trie.validate()}")
print("evidence=finite_trie_operations_trace")
```

## Definitions and Notation

Let `Sigma` be the declared alphabet and `Sigma*` its finite sequences. A key `k` has length `|k|=L` in alphabet units. `p <=prefix k` means `p` is a prefix of `k`. A node in an uncompressed trie represents one sequence prefix; `terminal(v)` indicates that prefix is a stored key. `degree(v)` is transition count. `K` is stored key count, `N` allocated/reachable node count, and `T` total canonical key symbols before prefix sharing. A generation identifies one physical snapshot.

Canonicalization `C(raw)` is the versioned transformation applied at the API boundary. It may include decoding, a selected Unicode normalization, and a domain-approved case policy; collation and display form remain separate unless explicitly included. In a radix trie, edge label `lambda(e)` is a nonempty sequence and sibling labels have distinct first symbols. Output-sensitive complexity includes returned key/value bytes or symbols.

## Mechanisms, Invariants, or Proof Structure

Exact-lookup correctness follows by induction over consumed symbols: after `i` transitions, the node represents exactly canonical prefix `k[0:i]`; a missing unique transition proves no stored key spells `k`; after `L`, terminal is equivalent to membership. Insertion preserves unique transitions and adds exactly one terminal on first admission. Deletion's reverse pruning removes exactly nodes that are nonterminal, childless, and therefore represent no stored key path.

Representation proofs then branch: child containers must implement unique symbol maps and promised order; radix splitting must preserve concatenated root-to-terminal strings; derived counts/caches must update only on logical membership changes; snapshots must bind handles and lifetime. Complexity separates canonicalization, per-transition lookup, path-label comparisons, and output from the simple `L` transition count.

## Alternatives and Trade-Offs

| Representation | Best fit | Principal trade-off |
|---|---|---|
| fixed child array | small dense alphabet | constant transition, high per-node bytes |
| sorted child vector | low/medium degree, ordered traversal | compact reads, shifting updates |
| hashed children | mutable irregular fanout | expected lookup, capacity/order/security cost |
| bitmap plus packed children | bounded sparse alphabet | compact ordered rank/select transitions |
| adaptive radix tree | varied fanout and long keys | node conversions and compressed-path complexity |
| Patricia/radix trie | many unary paths | fewer nodes, label split/merge comparisons |
| double-array trie | compact mostly static dictionary | construction/relocation and rigid mutation |
| immutable FST | static ordered keys and mapping outputs | suffix sharing, rebuild/delta for updates |
| B-tree/hash map | order/page locality or exact lookup only | weaker native prefix navigation or repeated compares |

Choose with canonical key corpus, fanout and prefix distributions, exact/prefix/longest query mix, mutation and snapshot rate, ordering, values, memory target, platform, and persistence needs.

## Failure Modes and Misconceptions

- Trie cost depends on key representation and transition layout; `O(L)` is not “constant because keys are short.”
- Prefix existence, exact-key membership, and subtree output are different operations.
- NFC, case folding, grapheme segmentation, locale collation, and confusable security solve different problems.
- Canonicalization can expand text and must be bounded; normalization version belongs to persisted identity.
- Hash-backed children do not promise lexicographic traversal.
- Radix compression saves nodes but does not eliminate total label storage/comparison.
- Node count and terminal/key count are not interchangeable.
- Root-to-terminal paths can reveal prefixes; tries are not constant-time secret maps.
- Enumeration and fuzzy queries can be output/state-explosion bound even when prefix seek is cheap.
- Passing a finite functional trace does not establish production memory, Unicode security, concurrency, or persistence guarantees.

## Worked Examples

### Example 1

Keys `a` and `ab` share the `a` node. That node is terminal and has child `b`. Deleting `a` clears only its terminal; pruning it would also destroy `ab`. Deleting `ab` later can prune `b`, while `a` remains if reinserted.

### Example 2

A byte trie for UTF-8 `café` takes five byte transitions, while a code-point trie takes four. Decomposed `cafe` plus combining acute takes five code points until NFC maps it to the same four-code-point canonical key.

### Example 3

With alphabet `{A,C,G,T}`, four child pointers per node may be excellent. With all Unicode scalar values, a fixed array per node is infeasible; a small sorted vector or adaptive layout matches sparse degrees.

### Example 4

Keys `roman`, `romane`, and `romanus` can share compressed label `roman`; the node is terminal for `roman` and has labels `e` and `us`. Terminal state and outgoing labels coexist exactly as in the uncompressed prefix case.

### Example 5

Longest-prefix routing keys `/`, `/api`, and `/api/v1` queried with `/api/v1/users` returns `/api/v1`. Exact lookup for the full query is absent. Autocomplete under `/api` is yet another output operation.

### Example 6

A sorted child vector of degree six takes logarithmic comparisons and shifts on insertion. A six-entry hash table may reserve far more space and enumerate nondeterministically. Benchmark key distributions before choosing the theoretically expected lookup.

### Example 7

Updating an existing key's value does not change size or subtree terminal counts. Incrementing counts on every insert attempt causes prefix counts to drift while exact lookup still appears correct.

### Example 8

An iterator paused inside a child vector becomes invalid if insertion reallocates it. A generation-pinned immutable root preserves the old traversal, while the update publishes a new root and defers reclamation.

### Example 9

A mapped node claims edge-label offset near the maximum integer and length 32. `offset+length` can wrap into the file. Checked addition and file-region validation must precede slicing or decoding.

### Example 10

Autocomplete prefix `a` may match ten million keys. Prefix navigation can still be fast, but returning all results is not. A production API applies authorization, rank, limit/cursor, cancellation, and resource accounting.

## Cross-Program Connections

- **Programming languages:** lexers, token tries, symbol tables, and type-name completion require exact encoding and ownership contracts.
- **Database engineering:** prefix indexes, immutable segments, collation versions, page layouts, and FST dictionaries connect tries to storage engines.
- **Security engineering:** normalization, confusables, tenant separation, enumeration leakage, hostile formats, and bounded queries are identity controls.
- **Distributed systems:** route/config prefixes need deterministic canonicalization, versioned snapshots, and convergent update semantics.
- **Search and data engineering:** autocomplete and dictionary encoding combine tries/FSTs with ranking, compressed postings, and batch rebuilds.
- **Concurrent programming:** copy-on-write roots, publication, generation-pinned readers, and reclamation provide snapshot traversal.
- **Computer architecture:** node fanout, pointer width, cache lines, branch behavior, packed arrays, and memory mapping determine constants.

## References

1. [Princeton Algorithms, *Tries*](https://algs4.cs.princeton.edu/52trie/).
2. [Unicode Standard Annex #15, *Unicode Normalization Forms*](https://www.unicode.org/reports/tr15/).
3. [Unicode Standard Annex #29, *Unicode Text Segmentation*](https://www.unicode.org/reports/tr29/).
4. [Viktor Leis, Alfons Kemper, and Thomas Neumann, *The Adaptive Radix Tree: ARTful Indexing for Main-Memory Databases*](https://db.in.tum.de/~leis/papers/ART.pdf).
5. [Rust `fst` crate documentation](https://docs.rs/fst/latest/fst/).
6. [Apache Lucene maintained FST implementation](https://github.com/apache/lucene/tree/main/lucene/core/src/java/org/apache/lucene/util/fst).
7. [HashiCorp `go-immutable-radix` predecessor implementation (`libart`)](https://github.com/armon/libart).
8. [Stanford CS166, *Tries and Suffix Trees* lecture notes](https://web.stanford.edu/class/archive/cs/cs166/cs166.1166/lectures/07/Small07.pdf).

## Exercises

### Exercise 1

Insert `to`, `tea`, `ten`, `A`, and the empty key into an uncompressed code-point trie that permits empty keys and preserves exact case. Draw terminal nodes, compute size, then delete `tea` and state exactly which nodes can be pruned.

### Exercise 2

Specify a Unicode identity policy for usernames stored in a trie. Distinguish encoding, normalization, case, grapheme segmentation, display, collation, confusable/security review, versioning, invalid input, and length limits.

### Exercise 3

Design a radix insertion for an edge labeled `romane` when inserting `roman`, `romanus`, and `romane`. Explain every split, terminal transition, value movement, and failure guarantee.

### Exercise 4

Compare fixed arrays, sorted vectors, hash children, and adaptive radix nodes for a byte trie whose node-degree distribution is 80% degree one, 15% degree two to eight, and 5% degree above 100. State what measurements can overturn your initial choice.

### Exercise 5

Specify a validation and benchmark plan for a persistent concurrent autocomplete trie. Include reference semantics, Unicode vectors, malformed images, snapshot iteration, reclamation, ranking/count caches, output limits, workloads, byte accounting, and latency evidence.

## Answers to the Exercises

### Answer 1

The root is terminal for the empty key. It has exact-case children `t` and `A`; `A` is terminal. Under `t`, branch `o` is terminal for `to`, while `e` branches to terminal `a` for `tea` and terminal `n` for `ten`. Size is five. Deleting `tea` clears terminal at `a`; because that node is childless it can be removed. Node `e` still has child `n`, so it remains; `t`, `o`, `n`, `A`, and root terminals/paths remain. Exact-case policy keeps `A` distinct from `a`.

### Answer 2

Accept valid UTF-8, decode to Unicode scalars, apply a named normalization such as NFC, and choose explicitly whether usernames are case-sensitive or use a specified locale-independent identifier folding profile. Grapheme segmentation is needed for UI cursor/count behavior, not necessarily storage transitions. Retain original approved display text separately; define sorting through a named collation/version rather than trie code-point order. Apply confusable, mixed-script, bidirectional, reserved-name, tenant, and authorization rules at admission. Persist Unicode/profile/collation versions and plan revalidation/migration. Reject invalid encoding and canonical empty/disallowed forms; bound raw bytes, canonical scalars, normalization expansion, and display graphemes. Apply identical canonicalization to every operation.

### Answer 3

If `romane` already occupies one compressed edge from the current node, inserting `roman` finds common prefix `roman` and splits: create/publish an intermediate node reached by label `roman`, move old remaining label `e` and its terminal value below it, and mark the intermediate terminal with `roman`'s value. Inserting `romanus` reaches that node and adds label `us` to a new terminal; inserting `romane` reaches `e` and updates/rejects per duplicate policy. Prepare intermediate node, copied/sliced labels, children, and values privately; publish by one parent-child replacement only after all allocations/constructions succeed, leaving the old edge intact on failure.

### Answer 4

Start with compact inline sorted arrays for degree one through eight and a bitmap-packed/dense adaptive node for very high degree; a 256-pointer array at 80% degree-one nodes likely wastes memory, while hashes add headers/capacity and lose ordering. Adaptive conversion fits the bimodal tail. Measure actual node/header/alignment/allocator bytes, total/peak bytes during conversion, hit/miss transition latency, branch/cache/TLB behavior, iteration order and cost, update/delete shifting, degree thresholds, key-prefix distribution, concurrency publication, and workload-weighted end-to-end queries. A dense hot root, heavy mutation, different pointer width, SIMD bitmap rank, or allocator behavior can overturn the initial choice.

### Answer 5

Define canonical key/value, duplicate, ranking/tie, prefix, limit/cursor, and snapshot semantics. Compare every committed generation with an independent canonical ordered map for exact lookup, prefix filtering, ordering/ranking, counts, and longest prefix. Use Unicode conformance and domain-security vectors plus composed/decomposed, expansions, non-BMP, emoji, invalid and over-limit cases. Mutate every persisted index/offset/length/count/flag, detect cycles/unreachable nodes, verify checksums/provenance, and crash-inject publication. Force insert/delete/split/read races; validate fail-fast or generation-pinned iteration, cache coherence, linearization, stalled readers, and safe reclamation. Benchmark representative vocabularies and adversarial prefixes across construction, updates, exact/prefix/top-k, cold/warm mapping, concurrency, bytes and peak amplification. Report latency distributions and output/state limits, not only throughput; separate internal review from external Unicode/security/performance claims.
