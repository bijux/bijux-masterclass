---
module_id: DSE-020
program: Data Structures Engineering
level: 1
module_number: 20
title: Ropes and Piece Tables
status: complete
last_verified: 2026-08-29
---

# Ropes and Piece Tables

## One-Page Review

### Governing question

How can an editor represent a large, repeatedly modified text sequence without copying the whole document on each edit, while keeping indexing units, tree metrics, undo, snapshots, line boundaries, saving, and compaction correct?

### Essential definitions

- A **text-buffer ADT** represents a sequence and defines coordinates, slicing, insertion, deletion, replacement, versions, and serialization.
- A **rope** stores text in leaf chunks under a balanced tree whose internal summaries guide indexing and editing.
- `flatten(T)` is the logical text obtained by concatenating a tree's leaves left-to-right.
- A **weight/metric** is composable subtree metadata such as byte length, scalar count, UTF-16 count, or line-break summary.
- A **piece table** keeps immutable original storage `O`, append-only added storage `A`, and an ordered sequence of **pieces** `(source,start,length)`.
- A **piece tree** stores piece descriptors in a balanced, augmented tree.
- A **split** divides a logical sequence at a coordinate; **concatenation** joins sequences without changing order.
- **Structural sharing** lets versions reuse immutable subtrees or buffers.
- **coalescing** joins adjacent pieces that reference adjacent ranges of the same source.
- **compaction** rewrites live logical text into new backing storage to reduce fragmentation or retained history.

### Central model, mechanism, or theorem

For a rope node T,

$$
flatten(T)=
\begin{cases}
chunk(T), & T\text{ is a leaf},\\
flatten(T.left)\cdot flatten(T.right), & T\text{ is internal}.
\end{cases}
$$

If every node stores a composable metric `m(T)=m(left)⊕m(right)` and the tree height is O(log N), locating a coordinate descends one path in O(log N), apart from bounded leaf work. Insert and delete follow split/concatenate and restore balance/chunk bounds.

For pieces `P=<p0,...,p(k-1)>`, `flatten(P)` concatenates the referenced half-open source ranges. Insertion appends new text to A and inserts/splits descriptors; deletion removes/splits descriptors. O and previously written A bytes do not move. Descriptor organization—not the phrase “piece table”—determines lookup complexity.

### Critical invariants

1. Flattening yields exactly one logical document in order, with no unintended gaps or duplication.
2. Every range is nonempty, in bounds, and aligned to the declared coordinate/encoding rules.
3. Rope balance and leaf-size rules bound height and local editing work.
4. Every cached metric equals the composition of leaf content, including cross-chunk boundary state where required.
5. Piece sources are immutable/append-only; descriptors alone determine current visibility.
6. Insert/delete preserve all unaffected text and use one stated half-open range convention.
7. Versions, cursors, iterators, slices, and anchors have explicit validity and bias rules.
8. Compaction, saving, undo truncation, and external file changes follow lifecycle/durability contracts.

### Common failures

- Claiming O(log N) because storage is a tree while allowing an unbalanced chain or unbounded leaves.
- Calling an internal node's left-subtree weight the total node length, then using inconsistent navigation equations.
- Measuring an API offset in bytes on one path and Unicode scalar values or UTF-16 code units on another.
- Splitting UTF-8 inside a code point or a user edit inside a disallowed grapheme boundary.
- Counting CR and LF independently and double-counting a CRLF split across two chunks.
- Leaving zero-length pieces, out-of-bounds source ranges, or adjacent coalescible fragments.
- Assuming an append-only add buffer makes undo, crash recovery, or autosave automatic.
- Retaining every old root/buffer forever through snapshots, undo, plugins, or background tasks.
- Compacting while live versions or source-relative references still depend on old storage.
- Benchmarking only repeated typing at one cursor and generalizing to huge files, multicursor edits, reads, or save latency.

### Compact example

Original storage is $hello world\n$. Inserting `, durable` at coordinate five appends nine characters to A and splits the original descriptor. Deleting `world` removes one referenced range without altering O. Inserting `editor` appends six more characters to A. The document becomes $hello, durable editor\n$; O is unchanged, A has fifteen characters, and five coalesced pieces describe the result.

### Connections

[DSE-013](013-gap-buffers.md) supplies the local-cursor alternative; [DSE-012](012-dynamic-arrays-and-geometric-growth.md) supplies contiguous growth; [DSE-008](008-iterators-and-traversal-protocols.md) supplies traversal validity. This closes the sequence block; the [program roadmap](../ROADMAP.md) next begins hash-based structures with DSE-021.

## Governing Question

Which logical coordinate, backing-store policy, descriptor/tree invariants, metrics, edit transformations, and evidence make a rope or piece-table text engine dependable for large interactive documents?

## Why This Matters

Editing is hostile to a flat immutable string. Inserting near the front can copy almost the entire suffix; retaining many versions can multiply that cost. A gap buffer reduces local edits but may pay to move the gap after distant jumps. Large files, many cursors, background parsing, snapshots, undo histories, and language-server coordinates add pressures that one representation rarely solves accidentally.

Ropes and piece tables avoid moving most existing text, but through different ownership models. A rope makes chunk concatenation and splitting tree operations. A piece table leaves backing bytes in original or add storage and changes the sequence of references. Real editors often hybridize them with balanced piece trees, line summaries, immutable snapshots, and incremental downstream indexes.

The hard work is not drawing boxes. It is specifying what an offset counts, proving summaries after every split/rotation, preserving line and encoding semantics across chunk boundaries, managing old versions, and producing exact file bytes. A representation that makes insertion fast but corrupts CRLF, breaks graphemes, leaks undo history, or reports wrong UTF-16 positions is not production-grade.

## Prerequisites and Retrieval

Before this module, retrieve:

- abstraction functions, representation invariants, and operation contracts from [DSE-001](001-abstract-data-types-and-concrete-representations.md), [DSE-002](002-representation-invariants.md), and [DSE-003](003-operation-contracts.md);
- asymptotic, allocation, locality, and tree-layout cost models from [DSE-004](004-time-space-and-allocation-cost.md), [DSE-005](005-contiguous-and-linked-layouts.md), and [DSE-006](006-memory-locality-and-cache-behavior.md);
- generic element/encoding constraints and iterator rules from [DSE-007](007-genericity-and-type-constraints.md) and [DSE-008](008-iterators-and-traversal-protocols.md);
- model-based testing and measurement from [DSE-009](009-property-based-testing-of-data-structures.md) and [DSE-010](010-benchmarking-a-structure-without-misleading-results.md);
- arrays, growth, gap buffers, and ring/deque contrasts from [DSE-011](011-fixed-arrays.md), [DSE-012](012-dynamic-arrays-and-geometric-growth.md), [DSE-013](013-gap-buffers.md), [DSE-018](018-deques.md), and [DSE-019](019-ring-buffers.md).

## Learning Objectives

After completing this module, you should be able to:

1. specify a text-buffer ADT with exact indexing, range, edit, version, and serialization semantics;
2. derive rope lookup, split, concatenate, insert, and delete from flattening and subtree metrics;
3. state balance and leaf-occupancy assumptions behind logarithmic claims;
4. derive piece-table insertion and deletion as descriptor transformations over immutable/append-only sources;
5. compare list, balanced piece-tree, persistent rope, gap-buffer, and flat-string representations;
6. maintain byte, Unicode scalar, UTF-16, line, and boundary-sensitive summaries correctly;
7. design snapshots, undo, anchors, iterators, saving, and compaction lifecycles;
8. identify fragmentation, retention, overflow, malformed-text, and external-change failure modes;
9. test edits against a simple model across Unicode, newline, boundary, and version cases;
10. benchmark realistic read/edit/save workloads with memory and latency evidence.

## Core Exposition

**Define the text sequence before choosing a structure.** Let document D be a sequence of atomic units under a declared encoding policy. Operations commonly include `length`, `slice([a,b))`, `insert(p,S)`, `delete([a,b))`, `replace([a,b),S)`, traversal, line/column conversion, version creation, and serialization. Valid coordinates satisfy `0<=a<=b<=length(D)`.

“Character offset” is ambiguous. UTF-8 byte, Unicode scalar value, UTF-16 code unit, extended grapheme cluster, and display column are different units. Rust Ropey currently edits by Unicode scalar (`char`) indices while exposing byte, line, and UTF-16 conversions. Language Server Protocol clients often require UTF-16 or negotiated encodings. Screen columns depend on shaping, tabs, bidirectionality, and fonts and should not be smuggled into storage indexing.

An engine can choose bytes internally and offer checked conversions, but it must reject positions inside an encoded scalar and define malformed input. If user commands promise grapheme-safe movement/deletion, segmentation follows a declared Unicode version/profile such as extended grapheme clusters in UAX #29. Storage chunks may split grapheme clusters if boundary algorithms carry sufficient context; the public edit layer still enforces its promised boundaries.

**A rope is an augmented sequence tree.** Leaves hold chunks of text or references to immutable chunks. Internal nodes preserve left-to-right concatenation. A classic binary rope stores the length/weight of its left subtree to decide whether an index descends left or subtracts that weight and descends right. Other implementations store total metrics on every node or use wider B-tree-like nodes. State the convention.

The abstraction function is flattening. A leaf flattens to its chunk. An internal node flattens to left text followed by right text. Empty representation may be a distinguished empty tree rather than an empty leaf. Correctness of every structural transformation reduces to preserving this concatenation and metadata.

To locate zero-based coordinate i in a binary node whose left length is w: if i<w, descend left; otherwise descend right with i-w. A one-past-end coordinate is allowed for insertion/splitting but not element access. The path takes O(height); therefore O(log N) needs a balance invariant relating height to total text/chunks plus bounded work inside a leaf.

**Leaf policy is part of the bound.** One leaf per character creates huge node overhead. One unbounded leaf can make splitting/copying linear in the whole document. Practical ropes target a chunk range, split oversized leaves, and merge/redistribute undersized neighbors. The exact thresholds depend on allocator, string representation, cache, encoding, and workload.

A balanced tree can still contain poor chunks after adversarial edits unless rebalancing includes leaf normalization. Conversely, aggressively merging on every keystroke can copy too much text. Some engines tolerate temporary underfull leaves and repair locally or periodically. Complexity claims must state amortized versus worst-case behavior and any deferred normalization.

**Split and concatenate form the edit algebra.** `split(T,p)` returns L,R with `flatten(T)=flatten(L)·flatten(R)` and `length(L)=p`. It descends the search path, splits a leaf if p is internal to its chunk, and rebuilds/balances boundary paths. `concat(L,R)` returns text `flatten(L)·flatten(R)`, repairing height and leaf bounds.

Then insertion is `concat(L,concat(S,R))` after splitting at p. Deletion of `[a,b)` splits at a and at length b-a in the suffix, discards or unlinks the middle, and concatenates the outside parts. A persistent rope produces a new root and structurally shares untouched subtrees; a mutable rope updates owned paths. Both require exact lifetime and iterator rules.

The original Boehm–Atkinson–Plass paper presents ropes as heavyweight strings supporting efficient non-destructive operations. That historical foundation does not dictate one modern tree, chunk size, Unicode model, allocator, or thread-safety guarantee. Current libraries must be read by their own contracts.

**Metrics turn the tree into an index.** If leaf measure m maps text to a monoid `(M,⊕,e)`—an associative combine with identity—then internal summaries compose. Byte length, scalar count, and newline count often use integer addition. A lookup uses the relevant left summary and descends without flattening the document.

Not every metric is context-free scalar addition. CRLF is one line break even if CR ends one chunk and LF begins the next. A correct summary may carry boundary state such as starts-with-LF, ends-with-CR, internal break count, then combine while subtracting/merging the cross-boundary pair. Grapheme segmentation, word boundaries, and syntax state can need larger finite summaries or incremental rescanning windows.

Multiple coordinate systems mean multiple maintained metrics or conversions that scan within chunks. Every rotation, split, merge, replacement, and path-copy must recompute summaries from children in the right order. Cached absolute offsets on every leaf are expensive because one early edit shifts all successors; subtree-relative summaries localize updates.

**A piece table preserves source bytes.** Begin with immutable original buffer O and empty append-only add buffer A. A piece `(source,start,length)` references a valid half-open range. The document is the concatenation of piece ranges in descriptor order. Initial nonempty text is one O piece.

To insert S at logical p, append S to A, find the containing piece, split it at p if necessary, and insert a new A descriptor. Insertion at a piece boundary needs no split. To delete `[a,b)`, split descriptors at a and b, then remove every descriptor wholly inside. Neither edit changes previously stored source ranges.

Afterward, coalesce adjacent descriptors when they name the same source and contiguous source ranges. Remove zero-length pieces. Validate `start+length` with checked arithmetic and against the source size. These simple rules prevent descriptor explosion from trivial boundaries, but arbitrary alternating edits can still create many pieces.

A flat descriptor array makes lookup and middle insertion O(k) in piece count. Calling it a piece table does not promise logarithmic edits. Store pieces in a balanced tree augmented by subtree logical length and line metrics to obtain O(log k) navigation and local structural edits under balance assumptions. VS Code's documented piece-tree reimplementation combines multiple buffers, piece descriptors, red-black-tree organization, and line-start metadata.

**Ropes and piece tables are orthogonal ideas.** A rope answers how logical fragments are organized and summarized. A piece table answers where fragment bytes originate and why old bytes need not move. Rope leaves may own fresh chunks without original/add semantics. Pieces may live in a list without a tree. A piece tree uses a rope-like augmented balanced tree whose leaves/nodes reference piece-table buffers.

That distinction sharpens design reviews. “We use a rope” does not answer whether edits copy leaf bytes or preserve an append-only log. “We use a piece table” does not answer balance, line lookup, snapshot cost, or traversal locality.

**Undo and snapshots require version semantics.** Piece storage retains deleted bytes, so an undo record can restore earlier descriptors. A persistent rope can retain old roots that share subtrees. Neither automatically defines command grouping, redo branching, selection restoration, memory budgets, or external side effects.

Snapshots should state immutability, coordinate version, and lifetime. A background parser can read an immutable root while the editor publishes a new one, but referenced chunks remain live until readers release them. A plugin holding old snapshots can retain large deleted text. Bound undo/snapshot memory by policy and expose diagnostics rather than assuming structural sharing is free.

Cursor/selection anchors are not plain integers across versions. For an insertion at p, an anchor at p may remain before or move after inserted text according to left/right bias. Deletion can collapse anchors inside the removed interval. Multiple simultaneous edits require a normalized ordering and coordinate space—typically all ranges in one pre-edit version, applied in a safe order, or an explicit transformation.

**Line handling is a first-class metric.** Editors query line content far more often than an ADT sketch suggests. Maintain line-break summaries and provide line-to-offset/offset-to-line paths. Define whether the final empty segment after a trailing newline is a line, which terminators are recognized, and whether serialization preserves mixed endings.

VS Code's primary engineering account reports CRLF boundaries as a notable implementation difficulty, especially when edits split or create the pair. This is a correctness warning, not portable benchmark evidence. Test CR, LF, CRLF, CR|LF across pieces/leaves, mixed endings, empty text, trailing breaks, and enormous lines.

**Saving is not flattening alone.** A save traverses logical order and streams chunks/pieces to an output encoding. It must define malformed input, BOM, newline preservation/conversion, permissions, metadata, partial write, fsync/durability expectations, atomic replacement, and conflict with external file changes. Those filesystem policies belong above the sequence structure but must not be hidden by it.

Original/add storage is process memory unless explicitly persisted. Append-only A is not a write-ahead log merely because its bytes never change. Recovery needs records, checksums, commit markers, ordering, and restoration of descriptor/version state. Autosave can serialize a snapshot, but completion and error reporting still matter.

**Compaction trades locality for history.** Piece count, tiny rope leaves, add-buffer size, and retained dead text can grow. Compaction flattens a chosen live version into new backing chunks and rebuilds a balanced tree. It can improve traversal/locality and release unreachable bytes.

Compaction also can invalidate source-relative piece identities, old iterators, undo records, snapshots, parser caches, and diagnostics. Run only when dependencies are absent or migrate them through a defined version map. Trigger from observed fragmentation/memory/latency and a budget, not a magic edit count copied from another editor.

**Alternatives remain competitive.** A flat string is simple and often fastest for small or read-mostly text. A dynamic array works when copies are affordable. A gap buffer gives excellent local insertion and is used by GNU Emacs, whose documentation notes a possible delay when the gap first moves to a distant edit locus. Line arrays make line access direct but can create object/shift costs. Fixed-size block lists, B-trees, ropes, and piece trees occupy different points.

Choose using document-size distribution, edit locality, multicursor behavior, read/query patterns, snapshot/undo needs, interoperability coordinates, allocator/runtime, and save path. Hybrid systems can maintain a text store plus separate interval trees, syntax trees, search indexes, and layout caches; those derived structures need versioned invalidation.

**Correctness evidence starts with a flat oracle.** For manageable generated cases, a language string/byte vector implements the same coordinate policy. Generate insert, delete, replace, slice, line mapping, undo/redo, snapshot, compact, and serialization actions. After each, compare flattening, length metrics, line mappings, pieces/leaves, source bounds, balance, summaries, and old-version immutability.

Adversarial cases include empty documents, every edit boundary, whole-document replacement, repeated insertion at one point, alternating distant edits, many tiny pieces, oversized leaves, depth pressure, maximum arithmetic, allocation failure, Unicode multi-byte/scalar/grapheme sequences, malformed input policy, and CRLF across boundaries. Mutate balance/metric/coalescing code to prove tests reject plausible defects.

Benchmark open, first edit, sequential typing, random/multicursor edits, replace-all, line lookup, viewport scans, full traversal, snapshot/undo, save, and compaction. Report distributions for real corpus sizes, line lengths, encodings, edit traces, memory retained/live, allocations, piece/leaf counts, height, cache behavior, and tail latency. Compare simple alternatives. Historical or project-specific results motivate hypotheses but do not certify a new engine.

The following Python trace verifies sequential piece-table descriptor transformations. Python indices here count Unicode code points; the ASCII fixture makes them equal to bytes only for this finite case.

<!-- bijux-verify: {"id":"piece-table-edit-trace","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"text=hello, durable editor\\n\npieces=5\nadd_units=15\noriginal_unchanged=True\nline_count=2\ninvariant=True\nevidence=finite_piece_table_trace\n","stderr":""}} -->
```python
class PieceTable:
    def __init__(self, original):
        self.original = original
        self.added = ""
        self.pieces = [] if not original else [("original", 0, len(original))]

    def _source(self, name):
        return self.original if name == "original" else self.added

    def __len__(self):
        return sum(length for _, _, length in self.pieces)

    def _split_at(self, position):
        if not 0 <= position <= len(self):
            raise IndexError(position)
        logical = 0
        for index, (source, start, length) in enumerate(self.pieces):
            end = logical + length
            if position == logical:
                return index
            if position == end:
                return index + 1
            if logical < position < end:
                left = position - logical
                self.pieces[index:index + 1] = [
                    (source, start, left),
                    (source, start + left, length - left),
                ]
                return index + 1
            logical = end
        return len(self.pieces)

    def _coalesce(self):
        merged = []
        for piece in self.pieces:
            if (merged and merged[-1][0] == piece[0]
                    and merged[-1][1] + merged[-1][2] == piece[1]):
                source, start, length = merged[-1]
                merged[-1] = (source, start, length + piece[2])
            else:
                merged.append(piece)
        self.pieces = merged

    def insert(self, position, text):
        if not text:
            return
        boundary = self._split_at(position)
        start = len(self.added)
        self.added += text
        self.pieces.insert(boundary, ("added", start, len(text)))
        self._coalesce()

    def delete(self, start, end):
        if not 0 <= start <= end <= len(self):
            raise IndexError((start, end))
        left = self._split_at(start)
        right = self._split_at(end)
        del self.pieces[left:right]
        self._coalesce()

    def text(self):
        return "".join(self._source(source)[start:start + length]
                       for source, start, length in self.pieces)

    def invariant(self):
        for index, (source, start, length) in enumerate(self.pieces):
            if source not in ("original", "added") or length <= 0:
                return False
            if not 0 <= start <= start + length <= len(self._source(source)):
                return False
            if index and self.pieces[index - 1][0] == source:
                previous = self.pieces[index - 1]
                if previous[1] + previous[2] == start:
                    return False
        return len(self.text()) == len(self)


table = PieceTable("hello world\n")
original_snapshot = table.original
table.insert(5, ", durable")
table.delete(15, 20)
table.insert(15, "editor")
print("text=" + table.text().encode("unicode_escape").decode("ascii"))
print(f"pieces={len(table.pieces)}")
print(f"add_units={len(table.added)}")
print(f"original_unchanged={table.original == original_snapshot}")
print(f"line_count={table.text().count(chr(10)) + 1}")
print(f"invariant={table.invariant()}")
print("evidence=finite_piece_table_trace")
```

This trace does not establish balanced-tree complexity, Unicode boundary handling, persistence, filesystem durability, or editor-scale performance.

## Definitions and Notation

- `D`: logical document sequence under one declared atomic/indexing unit.
- `[a,b)`: half-open range containing coordinates a through b-1; empty when a=b.
- `flatten(X)`: logical concatenation represented by rope or piece sequence X.
- `N`: logical document length in a named metric; never an unqualified “characters.”
- `k`: number of rope chunks or piece descriptors, depending on context.
- `m(x)`: metric summary of x; `⊕` is its associative ordered composition and e its identity.
- **rope leaf**: bounded text chunk or immutable chunk reference.
- **rope internal node**: ordered child container with cached subtree summaries.
- `O`, `A`: original immutable storage and append-only added storage in a basic piece table.
- `piece=(source,start,length)`: checked reference to a nonempty half-open range in O or A.
- **version/root**: immutable identity of one logical document state.
- **anchor bias**: rule deciding which side of coincident inserted text an anchor follows.
- **fragmentation**: overhead/locality loss from many small descriptors/chunks or retained dead bytes.

## Mechanisms, Invariants, or Proof Structure

For ropes, prove flattening and metric correctness by structural induction. Leaves return their chunks and measured summaries. An internal node concatenates children in order and stores their composed summaries. Search consumes only left metrics and reaches the unique coordinate. Split and concat preserve flattening; rotations/rebalancing preserve child order and recompute metrics. Height/chunk bounds supply the complexity premise.

For piece tables, prove every descriptor range valid in its immutable/append-only source and flatten descriptors in order. Insertion appends one source range and partitions at most the containing logical piece; deletion partitions boundaries and omits exactly `[a,b)`. Unaffected ranges preserve identity/order. Coalescing preserves flattening because adjacent same-source ranges are contiguous.

For versions, prove published roots/buffers never mutate, references keep backing storage alive, and edit transforms use coordinates from the named input version. Compaction is a representation replacement with identical flattening/metrics and an explicit migration or invalidation of dependent identities.

Boundary-sensitive summaries add composition state. For CRLF, combining `x` and `y` must detect x ending CR and y starting LF so the pair is counted once. The same proof pattern applies to any incremental metric whose result depends on a bounded boundary context.

## Alternatives and Trade-Offs

| Representation | Strength | Cost or obligation |
|---|---|---|
| Flat immutable string | simplest snapshots and traversal | middle edits copy large suffixes |
| Dynamic array | compact, fast scan/index | shifts/copies and invalidation |
| Gap buffer | excellent repeated local edits | distant gap moves; snapshot sharing is separate |
| Rope with owned chunks | logarithmic structural edits when balanced | chunk normalization, metadata, traversal overhead |
| Piece list | simple append-only edit storage/undo basis | linear descriptor search/edit as k grows |
| Balanced piece tree | logarithmic descriptor navigation, line metrics | rotations, summaries, fragmentation, more state |
| Persistent rope | cheap immutable snapshots/version sharing | retained memory and reclamation policy |
| Line array | direct line lookup and simple APIs | per-line overhead, shifts, cross-line edits |

Small files may favor flat structures. Highly local typing may favor a gap. Large/multicursor/versioned workloads may favor a balanced rope or piece tree. Profile the complete editor pipeline rather than data-structure micro-operations alone.

## Failure Modes and Misconceptions

- **“Tree means logarithmic.”** Height and leaf work must be bounded by maintained invariants.
- **“Every rope weight has one definition.”** Some store left length, others totals/multiple metrics; navigation must match.
- **“Piece tables edit the add buffer.”** A basic design appends; logical deletion changes descriptors.
- **“Append-only means durable.”** Memory buffers lack recovery ordering, commits, and filesystem guarantees.
- **“Unicode character is one unit.”** Bytes, scalars, UTF-16 units, graphemes, glyphs, and columns differ.
- **“Newline count is additive.”** CRLF across a chunk boundary needs boundary-aware composition.
- **“O(log N) line access means line materialization is free.”** Returning content can copy/scan the line or chunks.
- **“Structural sharing saves all memory.”** Live old roots retain shared and deleted backing data.
- **“Undo follows automatically.”** Command grouping, redo branches, anchors, budget, and side effects remain policy.
- **“Compaction is invisible.”** Source identities, iterators, versions, caches, and undo can depend on old storage.
- **“One offset survives edits.”** Anchors require version and left/right bias or transformation.
- **“Saving the flattened text is safely persisted.”** encoding, partial writes, atomic replace, durability, and conflicts remain.
- **“One editor benchmark chooses the structure.”** runtimes, workloads, document distributions, and downstream calls differ.

## Worked Examples

### Example 1

A binary rope root has left metric eight. Lookup index five descends left unchanged; index eleven descends right as index three. Conclusion: left-subtree weight guides navigation without flattening.

### Example 2

Repeatedly concatenating each new one-byte leaf as the right child without rebalancing creates height N. Lookup becomes O(N), despite using rope nodes. Conclusion: logarithmic behavior depends on balance and chunk policy.

### Example 3

Split `abcdef` at coordinate two into `ab` and `cdef`; insert `XY` by concatenating `ab·XY·cdef`, yielding `abXYcdef`. Conclusion: split/concat preserve unaffected order and define insertion.

### Example 4

One rope leaf ends with CR and its next leaf begins LF. Summing one break per leaf reports two, while the document has one CRLF sequence. Conclusion: line metrics need cross-boundary state.

### Example 5

Original `abcd` has piece `(O,0,4)`. Insert `XY` at two: append XY to A and use `(O,0,2),(A,0,2),(O,2,2)`. Flattening yields `abXYcd`, O unchanged. Conclusion: descriptors express the edit.

### Example 6

Delete logical `[1,5)` from the prior `abXYcd`. Splitting boundaries retains `(O,0,1)` and `(O,3,1)`, yielding `ad`; deleted source bytes still exist. Conclusion: logical deletion changes reachability, not source storage.

### Example 7

An anchor at p is transformed through insertion S at p. Left-biased anchor stays p; right-biased becomes `p+length(S)`. Conclusion: a coordinate alone cannot specify cursor behavior across versions.

### Example 8

UTF-8 `é` occupies two bytes, one Unicode scalar, one UTF-16 code unit, and normally one grapheme cluster. An API receiving byte offset one points inside its encoding and must reject/translate. Conclusion: indexing unit is a safety contract.

### Example 9

A persistent edit changes one path in a balanced rope and a background task retains the previous root. New/old documents are stable, but deleting 500 MB from the new root may not free it while the snapshot lives. Conclusion: persistence trades copying for retention management.

### Example 10

A compactor rebuilds a piece tree whose flattening and line metrics match, then discards old buffers while an undo entry still references `(A,100,20)`. Undo becomes invalid. Conclusion: compaction must migrate or intentionally truncate dependent history before reclamation.

## Cross-Program Connections

- [Programming Languages and Semantics](../../01-programming-languages-and-semantics/ROADMAP.md) connects text units, persistent values, observable edits, and iterator behavior.
- [Functional Programming](../../03-programming-languages-functional-programming/ROADMAP.md) connects monoids, folds, persistent trees, zippers, and structural sharing.
- [Systems Programming](../../05-programming-languages-systems-programming/ROADMAP.md) owns encoding validity, allocation, file I/O, object lifetime, mapped storage, and checked arithmetic.
- [Compilers and Language Implementation](../../08-compilers-and-language-implementation/ROADMAP.md) connects source coordinates, incremental lexing/parsing, syntax trees, and diagnostic remapping.
- [Software Design and Domain Modeling](../../09-software-engineering-software-design-and-domain-modeling/ROADMAP.md) connects command grouping, versioned boundaries, and storage/service ownership.
- [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) connects balanced-tree operations, amortization, incremental summaries, and workload measurement.
- [Database Engineering](../../18-database-engineering/ROADMAP.md) connects append-only storage, snapshots, compaction, recovery, and durability distinctions.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) owns malformed encoding, arithmetic/range validation, resource exhaustion, path/save safety, and untrusted files.

## References

1. Hans-J. Boehm, Russ Atkinson, and Michael Plass, [Ropes: an Alternative to Strings](https://www.cs.tufts.edu/comp/150FP/archive/hans-boehm/ropes.pdf). Primary 1995 paper defining rope motivation, structure, non-destructive operations, balancing, and implementation experience.
2. Charles Crowley, [Data Structures for Text Sequences](https://www.cs.unm.edu/~crowley/papers/sds/sds.html). Primary comparative work covering arrays, gaps, lists, blocks, line pointers, piece tables, and experimental design.
3. Microsoft Visual Studio Code, [Text Buffer Reimplementation](https://code.visualstudio.com/blogs/2018/03/23/text-buffer-reimplementation). Primary engineering account of multiple backing buffers, piece descriptors, red-black tree metrics, line lookup, CRLF, memory, and workload profiling.
4. Microsoft Visual Studio Code, [`pieceTreeBase.ts`](https://github.com/microsoft/vscode/blob/main/src/vs/editor/common/model/pieceTreeTextBuffer/pieceTreeBase.ts). Current project source for piece-tree nodes, edits, traversal, line metadata, and invariants; private implementation details are version-specific.
5. Raph Levien, [Rope Science: Metrics](https://xi-editor.io/docs/rope_science_02.html). Primary Xi design note on composable metrics, monoid homomorphisms, tree summaries, and coordinate conversion.
6. Xi Editor, [The Xi Text Engine](https://xi-editor.io/docs/crdt-details.html). Primary code/design tour of immutable balanced ropes, bounded chunks, structural sharing, edits, and version-oriented text operations.
7. Ropey Project, [`Rope`](https://docs.rs/ropey/latest/ropey/struct.Rope.html). Current Rust rope API for UTF-8 text, byte/scalar/UTF-16/line metrics, chunks, edits, slices, and complexity claims.
8. Unicode Consortium, [Unicode Standard Annex #29: Text Segmentation](https://unicode.org/reports/tr29/). Current conformance clauses and algorithms for extended grapheme, word, and sentence boundaries.
9. GNU Emacs Project mirror, [Lisp Reference Manual buffer source](https://github.com/emacs-mirror/emacs/blob/master/doc/lispref/buffers.texi). Current mirrored manual source documenting gap insertion/deletion and the cost of moving the gap to a distant locus.
10. Unicode Consortium, [Unicode Standard Annex #14: Line Breaking Algorithm](https://unicode.org/reports/tr14/). Current Unicode line-break boundary model and conformance profiles, distinct from stored newline-sequence counting.

## Exercises

### Exercise 1

Specify a text-buffer ADT for UTF-8 storage that receives UTF-16 coordinates from a client. Define range, conversion, malformed input, grapheme-safe commands, version, and serialization behavior.

### Exercise 2

Prove rope lookup and insertion using flattening, left metrics, split, concat, balance, and leaf bounds. Identify exactly where O(log N) assumptions enter.

### Exercise 3

Starting from original $one two\n$, derive piece descriptors for inserting ` bright` after `one`, deleting `two`, undoing the delete, and coalescing. State what bytes and metadata each version retains.

### Exercise 4

Design ordered metric summaries for bytes, Unicode scalars, UTF-16 units, lines, and CRLF across leaf boundaries. Explain update and query evidence.

### Exercise 5

Prepare a production decision and verification plan comparing a gap buffer, persistent rope, and balanced piece tree for a large-file, multicursor editor with background parsing and bounded undo.

## Answers to the Exercises

### Answer 1

Store valid UTF-8 bytes and name byte offsets as the canonical internal coordinate. Maintain scalar/UTF-16 subtree summaries and convert a client `(line,utf16_column,version)` through line metrics plus checked scan within bounded chunks. Reject stale versions or transform through an explicit edit history; reject a UTF-16 position inside a surrogate pair and any result inside a UTF-8 scalar. User movement/deletion uses extended grapheme boundaries under a pinned UAX #29/Unicode version or declared tailoring, while programmatic scalar/byte APIs remain distinct. Ranges are half-open, checked, and tied to one version. Malformed file bytes are rejected, losslessly represented under a separate binary policy, or decoded with explicitly reported replacement—never silently mixed. Save streams logical bytes in order with declared encoding/BOM/newline/external-conflict and atomic-write/durability policy.

### Answer 2

Inductively, a leaf flattens to its chunk and stores its exact metric. An internal node flattens left then right and stores composed child metrics. Lookup i compares with left length w: i<w follows the unique left coordinate; otherwise right coordinate i-w selects the same character in concatenation. Split at p rebuilds boundary paths L,R with `flatten(T)=flatten(L)·flatten(R)` and `len(L)=p`. Insertion S yields `L·S·R`, exactly adding S while preserving outside order. Rebalancing rotations may regroup concatenation but must not reorder leaves and must recompute metrics. O(log N) enters only if height is O(log N) under a maintained balance rule and leaf lookup/split is bounded by maximum chunk size; concat/split must restore those rules with stated worst-case or amortized work.

### Answer 3

Start `[(O,0,8)]` for $one two\n$. Append ` bright` as `A[0:7]` and insert at three, giving `(O,0,3),(A,0,7),(O,3,5)` and text $one bright two\n$. Delete `two` at logical `[11,14)`: split the last O piece around its leading space and trailing newline, omit O[4:7], producing `(O,0,3),(A,0,7),(O,3,1),(O,7,1)` and $one bright \n$; the two O pieces are not source-contiguous. Undo can restore the prior descriptor root/list without changing O or A. It retains original eight units, added seven units, and descriptor/version metadata for both states. Coalesce only adjacent same-source ranges whose source end/start meet; undo's `(O,3,5)` is already one piece, while no cross-A/O merge is legal.

### Answer 4

Each leaf summary records byte, scalar, and UTF-16 counts; line internal count; begins-with-LF and ends-with-CR (and any additional terminator state required by policy). Composition adds byte/scalar/UTF-16 counts. For CRLF-as-one-newline, add child internal counts and reconcile the boundary: if left ends CR and right begins LF, combine the two boundary contributions into one according to the precise leaf-count convention. Store first/last boundary state even for empty children and test associativity on triples, because tree rotations change grouping. Updates recompute only edited leaf and ancestor summaries; queries descend by the requested left metric, then scan a bounded leaf with the pinned decoder/line rules. Evidence includes exhaustive small-string partitionings at every chunk boundary, Unicode conformance data for conversion/segmentation, CR/LF/CRLF/mixed cases, randomized edit comparison with a flat oracle, rotation mutations, and maximum arithmetic.

### Answer 5

Define distributions for file bytes/lines, long lines, encodings, cursor count/distance, edit size/locality, replace-all, read windows, snapshots, parse lifetime, saves, and undo budget. A gap buffer is the simplicity/local-typing baseline but may move large distances and does not itself supply immutable parser snapshots. A persistent rope gives balanced chunk edits and cheap roots but needs metric/chunk/reclamation rigor. A balanced piece tree preserves original/add bytes and supports local descriptor edits/undo, but needs tree summaries, fragmentation, compaction, and snapshot policy. Implement contract-equivalent prototypes or mature candidates; model-test edits, lines, coordinates, anchors, versions, save bytes, and compaction; fuzz malformed/Unicode/newline/large arithmetic; use sanitizer/race tools where relevant. Benchmark open, first/distant/multicursor edits, typing, replace-all, line/window/full reads, parse snapshots, undo, save, compaction, allocations, live/retained memory, height/piece/chunk counts, and p50/p95/p99 latency. Choose from measured end-to-end editor results and operational simplicity; do not claim external correctness or performance review without named records.
