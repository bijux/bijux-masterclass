---
module_id: DSE-013
program: Data Structures Engineering
level: 1
module_number: 13
title: Gap Buffers
status: complete
last_verified: 2026-08-29
---

# Gap Buffers

## One-Page Review

### Governing question

How can one movable region of spare storage make cursor-local insertion and deletion efficient while preserving sequence order, and which costs, invalidation rules, text semantics, and failure obligations keep the representation honest?

### Essential definitions

- A **gap buffer** stores a logical sequence in one array with an unused half-open interval, the **gap**, between a physical prefix and suffix.
- **Logical position** counts elements in the abstract sequence; **physical index** names a slot in the backing allocation. They differ after the gap.
- The state `(B, g0, g1)` has capacity `C=len(B)`, gap `[g0,g1)`, gap width `h=g1-g0`, and logical length `n=C-h`.
- The abstraction is `B[0:g0]` followed by `B[g1:C]`; gap slots are not logical elements and must never be observed as such.
- **Moving the gap** transfers elements across it until its left edge reaches an edit position. Its cost is proportional to the logical distance moved.
- **Gap growth** allocates or expands storage when an insertion exceeds current gap width. Its policy is separate from gap semantics.
- A **text unit** is the unit stored or indexed—bytes, encoding code units, Unicode scalar values, or grapheme clusters. These units are not interchangeable.
- A **marker** is a position that is adjusted under edits according to a specified affinity when insertion occurs exactly at that position.
- A **trace workload** records positions and sizes of actual or modeled edits; it is better evidence than a typing-only microbenchmark for a general editor.

### Central model, mechanism, or theorem

For each valid logical index `i`:

$$
\operatorname{phys}(i)=
\begin{cases}
i,&0\le i<g_0,\\
i+(g_1-g_0),&g_0\le i<n.
\end{cases}
$$

To edit at logical position `p`, move the gap from `g0` to `p`, preserving the order of transferred elements. Insertion consumes slots from the left of the gap; backspace expands the gap left; forward deletion expands it right. If an operation moves the gap distance `d`, inserts `k`, and triggers a transfer of `n` live elements during growth, its modeled work is `Theta(d+k+n)`; without growth it is `Theta(d+k)`. Thus repeated edits near one cursor can be cheap, but arbitrary jumps do not have worst-case constant cost.

### Critical invariants

1. `0 <= g0 <= g1 <= C`, `h=g1-g0`, and `n=C-h` are representable.
2. The non-gap slots, read prefix then suffix, encode exactly the abstract sequence in order.
3. Gap slots are outside the live-element set; initialization and destruction follow the element type's rules.
4. Moving the gap is overlap-safe and neither loses nor duplicates live elements.
5. An insertion has sufficient gap capacity before it publishes a larger abstract sequence.
6. Growth commits one valid representation or provides the documented failure guarantee with exact cleanup.
7. Indices, iterators, slices, pointers, markers, line indexes, and undo records obey distinct update or invalidation contracts.
8. Text operations state their storage and user-facing position units, encoding validity, segmentation version, and normalization policy.

### Common failures

- Calling all insertion and deletion `O(1)` while omitting gap movement and growth.
- Treating physical indices after the gap as logical positions.
- Copying in the wrong direction and corrupting overlapping source and destination ranges.
- Serializing the entire allocation and leaking gap contents or producing extra bytes.
- Assuming one byte, UTF code unit, Unicode scalar, and visible character are the same.
- Moving the gap while raw pointers, slices, or iterators still refer to physical slots.
- Updating text but not markers, line-break metadata, syntax state, selections, or undo information.
- Growing with unchecked capacity arithmetic or publishing metadata before transfer succeeds.
- Benchmarking only sequential typing and generalizing to random edits, large pastes, or many cursors.
- Sharing one unsynchronized mutable gap across threads or collaborative replicas.

### Compact example

Capacity eight initially encodes `abcd` before a four-slot gap. Moving the gap from logical position four to two transfers `c` and `d` two slots. Insert `X`, insert `Y`, backspace `Y`, delete forward `c`, move once to the end, then insert `!`. The result is `abXd!`, gap `[5,8)`, and three moved slots. The trace verifies the finite state transitions; it is not a universal performance result.

### Connections

[DSE-011](011-fixed-arrays.md) supplies backing-array layout and live-slot obligations; [DSE-012](012-dynamic-arrays-and-geometric-growth.md) supplies capacity growth and invalidation; [DSE-008](008-iterators-and-traversal-protocols.md) supplies traversal contracts; [DSE-009](009-property-based-testing-of-data-structures.md) and [DSE-010](010-benchmarking-a-structure-without-misleading-results.md) supply evidence methods. Later sequence modules compare chunked structures, ropes, and editor indexes.

## Governing Question

What representation, mapping, transition protocol, cost model, and surrounding metadata let a gap buffer serve an editable sequence—and under which locality, Unicode, latency, memory, concurrency, and durability requirements should it be replaced or embedded in a larger structure?

## Why This Matters

An array gives compact storage and fast traversal but ordinarily shifts a suffix for an insertion in the middle. A gap buffer turns unused capacity into a movable hole. Once that hole is at the edit point, consecutive typing, backspace, and forward deletion change only two boundaries and a few nearby slots. This is an unusually direct alignment between representation and interactive workload.

The appealing slogan—“edits at the cursor are constant time”—is only conditionally true. Moving from one distant edit point to another shifts intervening elements. Exhausting the gap invokes a capacity transition. Real editors also maintain cursor positions, selections, line indexes, syntax state, undo history, encoding validity, and often multiple views. The text sequence can be correct while those dependent structures are stale.

Gap buffers therefore teach a broader engineering lesson: optimize a measured locality pattern, not an abstract operation name. The core representation is small enough to prove, yet production fitness depends on contracts at its boundaries. Those boundaries include element lifetime, aliases, Unicode segmentation, failed allocation, file I/O, secure erasure, asynchronous readers, and collaborative edits.

## Prerequisites and Retrieval

Before this module, retrieve:

- abstract sequences, representation functions, and proof obligations from [DSE-001](001-abstract-data-types-and-concrete-representations.md) and [DSE-002](002-representation-invariants.md);
- failure guarantees and observable operation contracts from [DSE-003](003-operation-contracts.md);
- worst-case, amortized, allocation, byte-traffic, and latency models from [DSE-004](004-time-space-and-allocation-cost.md);
- fixed contiguous storage, initialized extents, checked indexing, and views from [DSE-011](011-fixed-arrays.md);
- geometric capacity growth, transfer failure, and alias invalidation from [DSE-012](012-dynamic-arrays-and-geometric-growth.md);
- iterator semantics, model-based tests, and representative benchmarks from [DSE-008](008-iterators-and-traversal-protocols.md), [DSE-009](009-property-based-testing-of-data-structures.md), and [DSE-010](010-benchmarking-a-structure-without-misleading-results.md).

## Learning Objectives

After completing this module, you should be able to:

1. define the abstraction function and logical-to-physical index mapping of a gap buffer;
2. prove order preservation for left and right gap movement;
3. implement insertion, backspace, forward deletion, and growth as valid state transitions;
4. derive costs from cursor distance, edit size, growth, element width, and dependent metadata;
5. specify ownership, initialization, destruction, failure, and invalidation for generic elements;
6. distinguish byte, code-unit, scalar-value, grapheme-cluster, line, and display-column positions;
7. design marker affinity, line-index, undo, serialization, and snapshot contracts around the buffer;
8. test the representation with reference models, adversarial boundaries, failures, and realistic traces;
9. compare a single gap with arrays, piece tables, ropes, chunked sequences, and multi-gap variants;
10. identify security, concurrency, hard-latency, and high-stakes claims that require evidence beyond this data structure.

## Core Exposition

**Start from the abstract sequence.** Let the logical value be `A=<a0,...,a(n-1)>`. A backing array `B` of capacity `C` is divided into live prefix `[0,g0)`, unused gap `[g0,g1)`, and live suffix `[g1,C)`. The abstraction function concatenates the two live ranges. The gap can have width zero; the prefix or suffix can be empty. No sentinel value is required in a low-level implementation because the boundaries determine liveness. The executable teaching model uses `None` only to make non-live slots inspectable.

Logical lookup must cross the discontinuity correctly. An index below `g0` maps to itself. An index at or beyond `g0` maps forward by the gap width. The valid logical range remains `[0,n)` and an insertion position may be in `[0,n]`. A physical index is an implementation detail: retaining it across gap movement can silently refer to a different element or a non-live slot.

**Move left without overwriting unread elements.** Suppose the gap begins at logical position `q=g0` and an edit is requested at `p<q`. The logical block `[p,q)` must move to the physical region immediately before `g1`, and the gap must end at `p`. One correct elementwise transition repeatedly decrements both boundaries, transfers `B[g0]` to `B[g1]`, and makes the old source slot non-live. This proceeds from the block's right edge toward its left edge. After `q-p` steps, sequence order is unchanged and the gap begins at `p`.

For trivially copyable bytes, a correctly specified overlap-safe bulk move can implement the same transformation. Generic objects may require move construction, assignment, destruction, and rollback rules. A raw byte copy is invalid for types whose representation is not freely relocatable. Direction remains important even when an API resembles `memmove`; its exact source, destination, length, lifetime, and failure semantics must be reviewed.

**Move right symmetrically.** For `p>g0`, transfer elements from the start of the suffix into the start of the gap, then increment both boundaries. This proceeds left to right, because each source is just after the gap and each destination is at its beginning. After `p-g0` transfers, the gap begins at `p`. Either direction performs exactly the logical distance in unit transfers in the simple model.

Moving a zero-width gap changes no storage: growth must first create slack if an insertion is requested. Moving to the current position is a no-op. Implementations must validate `0<=p<=n` before translating positions; subtracting unsigned positions before comparison is a common underflow route.

**Insertion consumes the gap.** With width at least `k`, inserting `X=<x0,...,x(k-1)>` at `p` first moves the gap to `p`, then constructs `X` in `[g0,g0+k)` and advances `g0`. The abstraction becomes old prefix + `X` + old suffix. If element construction can fail, publishing a partially increased boundary exposes incomplete data. A transactional implementation tracks the newly constructed prefix, cleans it on failure, and advances the committed boundary according to its advertised guarantee.

Input can alias the same buffer. For example, “insert this selected substring here” may move the gap or grow storage before reading every source element. The contract must either snapshot the input, constrain overlapping ranges, or define an overlap-safe order. Language borrow rules can prevent some aliases; FFI and raw pointers can reintroduce them.

**Deletion grows the gap.** Backspace at gap position `p>0` removes the element immediately before the gap: destroy or clear `B[g0-1]`, then decrement `g0`. Forward delete at `p<n` removes the first suffix element: destroy or clear `B[g1]`, then increment `g1`. Deleting a range is boundary movement plus destruction of precisely the removed live elements. Empty-boundary behavior—no-op, result flag, or error—is an API decision, not a representation fact.

For text, deleting one “character” is underspecified. If storage is UTF-8 bytes, removing one byte can make the buffer ill-formed. Removing one Unicode scalar value can split a user-perceived grapheme cluster. UAX #29 supplies default grapheme-boundary algorithms and permits tailoring. An editor can store bytes for compactness while a segmentation layer chooses valid user-facing cursor boundaries; it must say which Unicode version and tailoring it uses.

**Growth is a separate capacity transition.** When the requested insertion exceeds `h`, choose a new capacity `C'` with checked arithmetic and a desired new gap width. Allocate storage, place the logical prefix before the new gap and the suffix after it, construct incoming data according to the chosen protocol, then commit. The policies from DSE-012 apply: geometric growth offers an amortized aggregate bound for repeated expansion, but a particular growth can transfer every live element and temporarily retain both allocations.

A growth operation must preserve the requested logical gap position, not accidentally move it to the document end unless the API allows that policy. It also invalidates raw storage observers. If a transfer or allocation fails, cleanup and old-state preservation depend on element traits and the documented guarantee. Maximum capacity must incorporate element width, allocator limits, platform offsets, file/export limits, and application policy.

**State costs by their actual variables.** Let `d=|p-q|` be the gap movement distance, `k` the insertion length, `n` the current logical length, and `m` the number of dependent positions or metadata entries adjusted. Without growth, a direct edit costs `Theta(d+k)` element work plus metadata cost. With allocate-and-transfer growth it can add `Theta(n)`. If markers are scanned linearly, the total can add `Theta(m)` even when the text edit itself changes boundaries in constant time.

This yields excellent behavior for a run of typing at one cursor: after the first movement, each small insertion consumes nearby slack. It yields poor worst-case behavior for alternating edits at opposite ends of a large document. Calling insertion simply `O(1)` hides the workload parameter that motivated the design.

Byte count also matters. Moving one million fixed-size bytes differs from moving one million resource-owning objects or variable-width logical units. Cache and memory bandwidth often dominate large moves. Virtual memory may change physical commitment and latency. A sound benchmark reports positions, distance, sizes, allocations, bytes transferred, metadata work, and latency distribution on the target runtime.

**Traversal sees two spans.** Sequential iteration visits prefix then suffix. An iterator can store a logical index and translate each access, or traverse two contiguous spans. The latter minimizes per-element branching but needs a transition at the gap. Random access remains constant time under the mapping, with one comparison and addition in the simple model.

Physical movement can invalidate pointers and iterators even without allocation: elements crossing the gap occupy different slots. A logical index still names a position, but insertion or deletion before it changes which element occupies that position. Stable element identity needs IDs or handles. A snapshot needs copying, versioned immutable storage, copy-on-write, or a lifetime rule that prevents concurrent mutation; returning the two live spans is not an immutable snapshot by itself.

**Markers require explicit affinity.** Editors need cursor positions, selection endpoints, diagnostics, bookmarks, and annotations to remain meaningful. An integer offset does not update itself. A marker policy adjusts positions after an edit and defines what happens when text is inserted exactly at the marker: a left-affine marker remains before inserted text, while a right-affine marker moves after it. Deletion commonly collapses markers inside the removed interval to a boundary, but products can choose other semantics.

GNU Emacs documents markers whose positions relocate under insertion and deletion, including an insertion-type choice. A simple array of markers makes each edit linear in marker count. Trees, interval structures, lazy deltas, or anchoring schemes can reduce update costs but add invariants. Marker semantics belong to the editor model; the gap boundaries alone do not solve them.

**Line and derived indexes are part of the design.** A renderer, tokenizer, parser, and search engine often need line lookup and incremental invalidation. Scanning from the beginning for every line request wastes the text representation's gains. A line-start index can be updated for changed regions, but it needs rules for `LF`, `CRLF`, mixed line endings, and edits that split or form a multi-unit terminator. VS Code's account of its piece-tree design shows how line metadata and realistic read workloads can dominate the choice of text representation.

Syntax highlighting, parsing, wrapping, bidi layout, shaping, and display columns are derived views. An edit should generate a logical change interval and version so clients can invalidate or recompute safely. “The bytes are correct” does not prove the screen, diagnostics, or accessibility tree is current.

**Unicode makes position a layered contract.** UTF-8 indexes bytes; UTF-16-oriented APIs often index code units; Unicode algorithms operate on scalar values; users may expect cursor movement by extended grapheme cluster. Display cells are still different because width depends on shaping, fonts, combining behavior, emoji sequences, tabs, and terminal policy. Store offsets in one declared unit and convert through validated indexes rather than naming all of them “character positions.”

Normalization is also separate from segmentation. UAX #15 defines canonical and compatibility normalization forms. Canonically equivalent strings can have different code-point sequences before normalization. Editing near a combining sequence can affect boundaries and normalization windows. Blind compatibility normalization can discard distinctions. A buffer may preserve original code points, normalize on input, normalize at save, or maintain an invariant; each choice changes round-trip, search, indexing, and undo behavior.

**Serialization must skip the gap.** Writing `B[0:g0]` followed by `B[g1:C]` produces the logical sequence. Writing all `C` slots emits spare bytes and possibly deleted content. Scatter/gather I/O can write two live spans without first compacting, while APIs requiring one span can move the gap to the end or copy to an output buffer. That operation has a visible latency and invalidation profile even though it preserves the abstract sequence.

Gap contents are logically unused, not necessarily physically zero. After deletion or movement, old representations can remain in spare slots, allocator copies, swap, crash dumps, undo logs, or snapshots. If confidentiality requires erasure, use a platform-appropriate non-elidable mechanism and verify every retained copy. Clearing only the current gap cannot prove system-wide erasure.

**Undo and persistence need independent models.** A gap buffer stores current content; it does not inherently preserve edit history. Undo can record inverse edits, commands, snapshots, or persistent structure versions. Each scheme needs position transformation, grouping, memory limits, failure recovery, and secure-retention policy. Saving the buffer is not a transaction unless file replacement, flush, metadata, crash consistency, and error handling are designed at the storage layer.

**Concurrency challenges the single moving hotspot.** Unsynchronized readers can race with boundary updates, transfers, or reallocation and observe duplicates, omissions, invalid storage, or data races. A coarse lock can make operations correct but may block rendering or background analysis during long moves. Versioned snapshots, immutable ropes, actor ownership, copy-on-write, or read-copy-update-like schemes may provide different reader behavior, each with reclamation and freshness obligations.

Multiple simultaneous local cursors can cause repeated long movements if served sequentially by one gap. Multiple gaps, one gap per chunk, or a balanced tree of chunks distributes slack. Collaborative editors additionally need operation transformation, CRDT, or another convergence protocol; a local gap can be storage inside a replica, but it does not establish convergence, causality, or intention preservation.

**Verification follows the state machine.** A reference-model test applies generated insert/delete/move sequences to both a simple list/string and the gap buffer, comparing the abstract value after every operation. It checks bounds, `n=C-h`, gap non-liveness, and order. Generate zero-width gaps, empty buffers, both ends, movement across the entire sequence, growth at exact capacity, overlapping input, failure at every transfer, maximum arithmetic, Unicode boundary cases, marker affinity, and serialization.

Instrument moved elements, grown bytes, allocations, marker updates, line-index work, and individual latency. Replay local typing, search-and-replace, edits alternating far apart, large paste/delete, undo/redo, multi-cursor actions, file load/save, and background-reader workloads. Random tests find transitions; deterministic regressions preserve them. Sanitizers and race tools can expose classes of defects, but neither they nor one executable trace proves the representation for all programs.

The following standard-library Python model validates a finite transition trace. `None` is prohibited as data and represents the educational gap; production generic storage would use explicit lifetime management instead.

<!-- bijux-verify: {"id":"gap-buffer-transition-trace","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"text=abXd!\nlength=5\ncapacity=8\ngap=(5, 8)\ngap_width=3\nmoved_slots=3\ninvariant=True\nevidence=finite_gap_trace\n","stderr":""}} -->
```python
class GapBuffer:
    def __init__(self, values, capacity):
        if any(value is None for value in values) or capacity < len(values):
            raise ValueError("invalid initial state")
        self.buffer = list(values) + [None] * (capacity - len(values))
        self.g0 = len(values)
        self.g1 = capacity
        self.moved = 0

    def __len__(self):
        return len(self.buffer) - (self.g1 - self.g0)

    def invariant(self):
        return (
            0 <= self.g0 <= self.g1 <= len(self.buffer)
            and all(value is not None for value in self.buffer[:self.g0])
            and all(value is None for value in self.buffer[self.g0:self.g1])
            and all(value is not None for value in self.buffer[self.g1:])
        )

    def text(self):
        return "".join(self.buffer[:self.g0] + self.buffer[self.g1:])

    def move_gap(self, position):
        if not 0 <= position <= len(self):
            raise IndexError(position)
        while self.g0 > position:
            self.g0 -= 1
            self.g1 -= 1
            self.buffer[self.g1] = self.buffer[self.g0]
            self.buffer[self.g0] = None
            self.moved += 1
        while self.g0 < position:
            self.buffer[self.g0] = self.buffer[self.g1]
            self.buffer[self.g1] = None
            self.g0 += 1
            self.g1 += 1
            self.moved += 1

    def insert(self, value):
        if value is None or self.g0 == self.g1:
            raise ValueError("this finite trace requires one free slot")
        self.buffer[self.g0] = value
        self.g0 += 1

    def backspace(self):
        if self.g0 == 0:
            return False
        self.g0 -= 1
        self.buffer[self.g0] = None
        return True

    def delete_forward(self):
        if self.g1 == len(self.buffer):
            return False
        self.buffer[self.g1] = None
        self.g1 += 1
        return True


gap = GapBuffer("abcd", 8)
gap.move_gap(2)
gap.insert("X")
gap.insert("Y")
assert gap.backspace()
assert gap.delete_forward()
gap.move_gap(len(gap))
gap.insert("!")

print(f"text={gap.text()}")
print(f"length={len(gap)}")
print(f"capacity={len(gap.buffer)}")
print(f"gap=({gap.g0}, {gap.g1})")
print(f"gap_width={gap.g1 - gap.g0}")
print(f"moved_slots={gap.moved}")
print(f"invariant={gap.invariant()}")
print("evidence=finite_gap_trace")
```

## Definitions and Notation

| Term or symbol | Meaning |
|---|---|
| `A` | Abstract finite sequence. |
| `B` | Backing array or allocation. |
| `C` | Physical capacity, `len(B)`. |
| `[g0,g1)` | Half-open unused gap interval. |
| `h` | Gap width `g1-g0`. |
| `n` | Logical length `C-h`. |
| `p`, `q` | Requested and current logical gap positions. |
| `phys(i)` | Physical slot representing valid logical index `i`. |
| `d` | Gap movement distance `abs(p-q)`. |
| `k` | Number of inserted elements. |
| live slot | A slot currently containing a logical element whose lifetime is active. |
| spare slot | Storage in the gap, outside the abstract sequence. |
| marker affinity | Whether a marker at an insertion boundary remains before or moves after inserted content. |
| grapheme cluster | A default or tailored Unicode text-segmentation unit intended to approximate a user-perceived character. |
| finite trace | Reproduced behavior for specified inputs, not a proof for all states or implementations. |

Unless stated otherwise, complexity counts unit element transfers in a single-threaded RAM-style model. Byte traffic, allocation, element callbacks, marker/index maintenance, page faults, rendering, I/O, synchronization, and tail latency require separate models and evidence.

## Mechanisms, Invariants, or Proof Structure

**Representation invariant.** Require `0<=g0<=g1<=C`, checked `n=C-(g1-g0)`, live elements exactly outside the gap, and correct lifetime/alignment for every slot. The abstraction is prefix concatenated with suffix. For every `i` in `[0,n)`, the piecewise mapping reaches a live slot and preserves order.

**Left-movement proof.** Maintain a loop invariant: elements outside the not-yet-moved block plus the already-transferred suffix encode the original sequence, the gap width is constant, and both boundaries decrease together. Each iteration transfers the rightmost remaining element into the rightmost newly available destination. Source is live, destination is gap storage, and no unread source is overwritten. Termination measure is `g0-p`, which decreases to zero.

**Right-movement proof.** Symmetrically, each iteration transfers the leftmost suffix element into the leftmost gap slot and increments both boundaries. The source is outside the gap and destination is within it. The measure `p-g0` decreases. Reading prefix then suffix still yields the same sequence.

**Insertion proof.** After movement, `g0=p`. With `h>=k`, construct the insertion sequence in order at the gap's left edge. Commit the left boundary only for successfully established live elements according to the failure contract. The new abstraction is `A[:p] + X + A[p:]`, and new gap width is `h-k`.

**Deletion proof.** Backspace destroys `A[p-1]` and shifts only the left boundary, yielding `A[:p-1]+A[p:]`. Forward deletion destroys the first suffix element, yielding `A[:p]+A[p+1:]`. Range deletion repeats or performs an equivalent bulk lifetime transition. Empty-boundary cases leave a valid state.

**Growth proof obligation.** Checked arithmetic establishes `C'>=n+k` and a nonnegative new gap width. A transfer protocol constructs each old live element exactly once in its new logical order, then commits or cleans partial state. The new abstraction equals the old sequence plus the defined edit; ownership is neither leaked nor duplicated. The amortized capacity proof is inherited only if the actual growth rule satisfies its assumptions.

**Cost conclusion.** A movement performs `d` transfers; local insertion adds `k`; growth may add `n`; metadata adds its own update cost. A sequence of edits at positions `p_t` has movement work proportional to `sum |p_t-p_(t-1)|`, revealing locality directly. No distributional assumption turns that expression into a worst-case constant bound.

## Alternatives and Trade-Offs

- **Plain contiguous array:** simplest and densest; middle edits shift a suffix, while a gap concentrates spare capacity at one working position.
- **Single gap buffer:** excellent cursor locality and two-span traversal; distant alternating edits produce large moves and one mutable hotspot.
- **Multiple or chunk-local gaps:** distribute edit locality; add chunk selection, balancing, slack distribution, and cross-chunk movement invariants.
- **Piece table/tree:** retains original and append-only added buffers with pieces describing current text; supports edit history and dispersed edits differently, but piece metadata, lookup, and normalization can grow complex.
- **Rope or balanced chunk tree:** offers logarithmic navigation and edits for large/dispersed content, snapshots, and augmentation; costs nodes, indirection, balancing, chunk policy, and more complex iteration.
- **Linked lines:** makes some line edits local and positions stable; incurs per-node overhead, poor locality, and awkward operations crossing lines.
- **Immutable/persistent sequence:** favors snapshots, readers, undo, and concurrency; writes allocate structure and reclamation/retention become central.
- **Move gap on demand versus speculatively:** demand movement avoids wasted work; idle-time movement can hide expected latency but may waste bandwidth, race with input, or disturb power use.
- **Large versus small gap:** a large gap delays growth and typing pauses; it retains more memory and increases transfer/clear costs. A small gap does the reverse.
- **Raw bytes versus higher-level units:** bytes are compact and interoperable with encodings; user-facing boundaries require validation and segmentation indexes.
- **Logical-index iterators versus two-span iterators:** logical indexes are simple but translate repeatedly; spans traverse efficiently but expose invalidation and lifetime surfaces.
- **Coarse locking versus snapshots:** a lock simplifies mutation correctness but can block readers; snapshots reduce blocking at the cost of versions, copying/sharing, and reclamation.

## Failure Modes and Misconceptions

1. **“Insertion is constant time.”** Only an edit already at a sufficiently large gap has that bound in the narrow element model.
2. **“The gap contains blank characters.”** It is non-live storage; any residual bit pattern is outside the abstract sequence.
3. **“Logical and physical indexes differ by one offset everywhere.”** The offset applies only on or after the gap.
4. **“Any copy direction works.”** Overlap can overwrite unread elements; direction or an overlap-safe primitive is essential.
5. **“Moving bytes relocates any type.”** Generic object lifetime and relocation rules can forbid raw copying.
6. **“Gap movement preserves pointers.”** Moved elements change physical slots even without reallocation.
7. **“An integer cursor stays with its text.”** Edits before or at it require a marker update and affinity policy.
8. **“One code unit is one visible character.”** Encoding units, scalar values, grapheme clusters, and display cells differ.
9. **“Normalization and grapheme segmentation are the same.”** They solve related but distinct problems.
10. **“Saving the allocation saves the document.”** Correct serialization skips the gap and still needs encoding and failure handling.
11. **“Deletion erases sensitive text.”** Removed representations can remain in gap storage and other system copies.
12. **“The gap buffer supplies undo.”** History and current sequence representation are separate concerns.
13. **“A line index updates itself.”** Every dependent index needs an edit transformation and invalidation contract.
14. **“Typing benchmarks characterize editing.”** Random jumps, replacements, large pastes, reads, and multiple cursors can dominate.
15. **“A lock-free read of the two spans is safe.”** Boundary changes and transfers require a synchronization or snapshot protocol.
16. **“A local gap solves collaborative editing.”** Replica convergence and causality require a separate distributed algorithm.

## Worked Examples

### Example 1

An eight-slot buffer stores prefix `ab`, a three-slot gap, and suffix `cde`. Here `g0=2`, `g1=5`, `C=8`, `h=3`, and `n=5`. Logical index 1 maps to physical 1; logical index 2 maps to physical `2+3=5`, which contains `c`. Conclusion: mapping branches at the logical gap position, not at the physical gap end.

### Example 2

The state encodes `abcdef` with the gap at logical position six. Moving it to position two transfers `f`, `e`, `d`, then `c` toward the allocation's end. Both boundaries decrease four times and the logical concatenation remains `abcdef`. Conclusion: right-to-left transfer preserves order during left movement.

### Example 3

The gap is at position two before suffix `cdef`; move it to five. Transfer `c`, then `d`, then `e` from the suffix start into successive left gap slots. The gap arrives before `f`, after three transfers. Conclusion: right movement proceeds left-to-right and costs the logical distance.

### Example 4

A four-slot gap at position 10 receives the string `xyz`. Construction succeeds for `x` and `y` but fails for `z`. Under a strong guarantee, destroy the two new objects and keep the committed boundary at 10; under a documented partial-insert contract, another result might be allowed. Conclusion: boundary publication and failure guarantee must agree.

### Example 5

A zero-width gap in a 1,024-element buffer receives one element. Geometric growth chooses capacity 2,048 and a transfer places prefix and suffix around new slack. The abstract insertion is one element, but physical work can include all 1,024 old elements and peak coexistence of two allocations. Conclusion: local edit complexity does not remove growth latency or memory peaks.

### Example 6

A UTF-8 buffer contains a four-byte emoji. Backspacing one byte produces an invalid encoding; deleting one scalar can still split an emoji sequence joined by modifiers or zero-width joiners. A cursor layer uses UAX #29 extended grapheme boundaries and deletes the selected cluster's byte interval. Conclusion: the stored unit and edit unit require an explicit conversion contract.

### Example 7

A left-affine diagnostic marker and a right-affine caret both sit at logical position 20. Inserting three units there leaves the diagnostic at 20 and moves the caret to 23; every marker after 20 also shifts by three. Conclusion: equal numeric positions can intentionally transform differently at an insertion boundary.

### Example 8

A serializer writes all capacity slots from a buffer whose gap holds residual bytes from a deleted password. The output contains extra bytes and may disclose the deleted value. Writing only the prefix and suffix produces the logical document; a separate verified erasure policy is needed for confidentiality. Conclusion: abstraction-correct serialization and secure deletion are different obligations.

### Example 9

One workload performs 10,000 single-byte inserts at one cursor; after initial positioning, movement is near zero until growth. Another alternates positions zero and one million, moving roughly one million units per edit. Reporting only the first workload supports no general editor claim. Conclusion: total movement variation `sum |delta position|` belongs in benchmark evidence.

### Example 10

A clinical note editor preserves the exact abstract text through every tested edit. That does not establish correct grapheme navigation, marker attachment, crash-safe saving, audit history, access control, secure deletion, multi-user convergence, accessibility, or clinical safety. Conclusion: a verified sequence core is necessary but far from sufficient for high-stakes deployment.

## Cross-Program Connections

- [Programming Languages and Semantics](../../01-programming-languages-and-semantics/ROADMAP.md) owns object lifetime, exceptions, aliasing, ownership, and observable failure guarantees.
- [Systems Programming](../../05-programming-languages-systems-programming/ROADMAP.md) owns allocation, overlap-safe movement, encodings, files, unsafe views, and secure-erasure primitives.
- [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) supplies aggregate growth analysis, workload-sensitive bounds, augmentation, and benchmark design.
- [Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) supplies synchronization, snapshots, ownership transfer, and reader reclamation.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) owns replica convergence, causality, operational transformation, and CRDT semantics beyond local storage.
- [Software Engineering Patterns](../../11-software-engineering-patterns/ROADMAP.md) connects edit commands, undo, observers, derived views, and durable interface boundaries.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) owns untrusted sizes, memory exhaustion, data remanence, dumps, access control, and verified erasure.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md) connects editor services, developer experience, accessibility integration, telemetry, and operational delivery.

## References

1. GNU Project, [Emacs Lisp Reference Manual: The Buffer Gap](https://www.gnu.org/software/emacs/manual/html_node/elisp/Buffer-Gap.html). Official description of Emacs's invisible gap representation and its performance consequence.
2. GNU Project, [Emacs source: `buffer.c`](https://github.com/emacs-mirror/emacs/blob/master/src/buffer.c). Production buffer representation, invariants, and implementation context.
3. GNU Project, [Emacs source: `insdel.c`](https://github.com/emacs-mirror/emacs/blob/master/src/insdel.c). Production insertion, deletion, gap movement, markers, and modification machinery.
4. GNU Project, [Emacs Lisp Reference Manual: Markers](https://www.gnu.org/software/emacs/manual/html_node/elisp/Markers.html). Position relocation and insertion-type semantics under edits.
5. Craig A. Finseth, [The Craft of Text Editing, Chapter 6](https://web.mit.edu/~yandros/doc/craft-text-editing/Chapter-6.html). Buffer-gap mechanism, editor buffer alternatives, paging, and implementation trade-offs.
6. Unicode Consortium, [Unicode Standard Annex #29: Unicode Text Segmentation](https://www.unicode.org/reports/tr29/). Current default grapheme, word, and sentence boundary algorithms and tailoring rules.
7. Unicode Consortium, [Unicode Standard Annex #15: Unicode Normalization Forms](https://www.unicode.org/reports/tr15/). Current canonical and compatibility normalization definitions, stability, and implementation guidance.
8. Peng Lyu, Microsoft, [Text Buffer Reimplementation](https://code.visualstudio.com/blogs/2018/03/23/text-buffer-reimplementation). Official engineering account of VS Code's piece-table/tree, line-index, allocation, read, edit, and benchmark decisions.
9. Xi Editor project, [Rope Science: MapReduce for Text](https://xi-editor.io/docs/rope_science_01.html). Editor-oriented augmented rope computations and motivation for derived text metrics.
10. Xi Editor project, [The Xi Text Engine](https://xi-editor.io/docs/crdt-details.html). Rope-based text representation, logarithmic edits, deltas, and collaborative-engine context.

## Exercises

### Exercise 1

Specify the representation invariant, abstraction function, index mapping, and boundary behavior for a generic gap buffer, including the zero-width and empty states.

### Exercise 2

Trace moving a gap from logical position seven to two and then from two to six. State transfer direction, number of elements moved, and loop invariants.

### Exercise 3

Design transactional insertion and growth for a resource-owning element type whose copy may fail. Include aliasing input, cleanup, overflow, and invalidation.

### Exercise 4

Compare a single gap buffer, a piece tree, and a rope for a code editor with large files, random replacements, sequential reads, undo, multiple cursors, and background readers. Provide a measurement plan rather than one universal winner.

### Exercise 5

Design an evidence and review plan for a multilingual, security-sensitive medical-note editor whose current text storage uses a gap buffer.

## Answers to the Exercises

### Answer 1

State is `(B,g0,g1)` with capacity `C=len(B)`, checked `0<=g0<=g1<=C`, gap width `h=g1-g0`, and logical length `n=C-h`. Live elements occupy exactly `[0,g0)` and `[g1,C)` with correct lifetime; gap slots are non-live. The abstraction concatenates those ranges. For `0<=i<n`, map `i` to itself when `i<g0`, otherwise to `i+h`. Valid lookup indices are `[0,n)` and insertion positions `[0,n]`. Empty state may have `n=0` with the whole allocation as gap; zero-width gap has `g0=g1` and requires growth before insertion. Backspace at zero and forward delete at `n` follow an explicitly selected no-op/result/error contract.

### Answer 2

From seven to two, move five elements rightward into the far side of the gap while processing sources from right to left; decrement both boundaries after arranging each transfer. The invariant preserves gap width, original logical order outside the remaining block, valid lifetimes, and a decreasing measure `g0-2`. From two to six, move four elements leftward into the near side while processing sources left to right; increment both boundaries. Its decreasing measure is `6-g0`. Total movement is nine elements. In both transitions, prefix-plus-suffix abstraction remains unchanged.

### Answer 3

Validate the logical position and checked `required=n+k`, maximum elements, and byte size. If the source aliases the buffer and movement/growth can invalidate it, snapshot under the API's failure and allocation policy before mutation. When current gap is sufficient, move the gap using type-correct construction/assignment and track each lifetime; construct inserted elements into gap storage and publish committed boundaries only according to the advertised guarantee. For growth, allocate `C'>=required`, transfer prefix and suffix in logical order while tracking constructed ranges, construct input, then commit new storage and boundaries. On failure destroy only successfully constructed new objects, release new storage, and preserve the old representation for a strong guarantee; if element semantics prevent that guarantee, state the weaker one. Reallocation invalidates all physical observers, while non-growing movement invalidates observers to moved slots under the declared rules.

### Answer 4

The single gap is a strong candidate for concentrated typing and compact two-span traversal, but random distant or multi-cursor edits move large ranges and coarse locking blocks readers. A piece tree preserves original/append-only buffers and can integrate undo and line metadata, but accumulates pieces/nodes and needs balanced lookup and normalization policy. A rope distributes content through balanced chunks, supporting logarithmic edits, augmentation, and immutable snapshots, but adds node overhead, balancing, chunk boundary, and iteration complexity. Replay representative small/large files with typing, random replacements, multi-cursor actions, undo/redo, full and windowed reads, syntax updates, snapshots, and save. Report latency distributions, transferred/allocated bytes, node or piece counts, memory peaks, line lookup, background-reader blocking, and compaction work. Select from measured workload and required contracts, not asymptotic labels alone.

### Answer 5

Define storage encoding and valid-input policy; version the UAX #29 grapheme rules and any tailoring; state normalization and round-trip behavior; test combining marks, emoji sequences, bidirectional text, line endings, invalid encodings, input methods, and accessibility navigation with appropriate human review. Model-test every edit against a reference sequence, verify markers/selections/diagnostics/undo and serialization, inject allocation/I/O failure, check crash-safe persistence and audit events, and use memory/race/undefined-behavior tools where applicable. Threat-model untrusted lengths, malicious text, stale views, residual gap bytes, undo/snapshot retention, dumps, swap, access control, and erasure limits. Measure real traces, tail latency, memory peaks, save/recovery, multiple cursors, and readers on target systems. Obtain named independent security, privacy, clinical, safety, accessibility, human-factors, quality, regulatory, operations, and language-specific reviews. Finite state-machine tests establish neither medical correctness nor deployment certification.
