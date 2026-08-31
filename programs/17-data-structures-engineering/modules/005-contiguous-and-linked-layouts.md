---
module_id: DSE-005
program: Data Structures Engineering
level: 1
module_number: 5
title: Contiguous and Linked Layouts
status: complete
last_verified: 2026-08-29
---

# Contiguous and Linked Layouts

## One-Page Review

### Governing question

How do contiguous and linked representations encode the same abstract sequence while changing address computation, update mechanics, ownership, invalidation, memory overhead, and failure behavior?

### Essential definitions

- A **contiguous layout** stores fixed-stride element slots in one adjacent logical memory region.
- A **linked layout** stores elements in nodes connected by references, pointers, handles, or indices.
- **stride** is the byte or storage-unit distance between successive element slots in a homogeneous contiguous layout.
- **random access** computes an element location from its index without traversing prior elements.
- A **link** identifies another node or a distinguished terminator; singly and doubly linked nodes store one or two directional links.
- A **sentinel** is a distinguished node or value used to simplify boundary cases without representing an ordinary element.
- An **intrusive structure** stores linkage fields inside elements; a non-intrusive structure owns wrapper nodes containing elements or references.
- **relocation** moves a representation while preserving its abstract value, potentially invalidating addresses, references, iterators, or views.
- A **view** exposes a range or projection backed by existing storage; a **copy** owns an independent representation.
- A **handle** is an indirect identity used to locate an element while controlling validation, movement, and lifetime.

### Central model, mechanism, or theorem

For fixed slot stride (s>0), contiguous element (i) has modeled address

$$
addr(i)=B+i\cdot s,\qquad 0\le i<n.
$$

A linked sequence begins at root (h) and follows a partial successor function

$$
next:N\rightharpoonup N.
$$

The abstract value is the ordered payload sequence encountered before the terminator. Correctness requires bounds/alignment and live-region invariants for the contiguous representation, and ownership, acyclicity or declared cyclic-sentinel structure, link consistency, and termination for the linked representation.

### Critical invariants

- Contiguous live elements occupy exactly the declared range and capacity arithmetic cannot overflow.
- Element stride, alignment, and layout match the language/ABI contract; padding is not silently treated as payload.
- Linked traversal from the root reaches exactly the owned logical nodes in abstract order.
- Acyclic lists terminate, while circular/sentinel lists state the permitted cycle and traversal stop rule.
- Doubly linked neighbors agree: when `x.next = y`, the applicable inverse link is `y.prev = x`.
- Ownership prevents dangling links, double insertion, double removal, and mutation through unauthorized aliases.
- Operations state whether addresses, references, iterators, slices, and handles remain valid after mutation.
- Inserting/removing at a known linked position is distinguished from finding that position.
- Memory comparisons include payload, slack, link fields, node headers, padding, allocation overhead, and transient copies.
- Measurements of locality are deferred to DSE-006 and never inferred solely from asymptotic notation.

### Common failures

Common failures are calling a language container contiguous without checking its element representation; assuming adjacent logical elements imply adjacent pointees; saying linked insertion is `O(1)` while ignoring search; retaining an array element pointer across reallocation; returning a writable slice without ownership rules; letting an intrusive node join two lists through one link field; losing the head/tail on boundary updates; traversing a corrupted cycle forever; serializing raw pointers; subtracting unrelated pointers; and comparing memory using payload bytes only.

### Compact example

For sequence `[10,20,30,40,50]`, array access at index three computes one slot address. A singly linked representation follows four nodes from the head. Inserting `25` at index two shifts three array elements, while a linked list with an already-known predecessor performs a constant number of link writes—but locating that predecessor from the head still traverses two nodes. The correct comparison names both access path and update.

### Connections

[DSE-001](001-abstract-data-types-and-concrete-representations.md) provides representation independence. [DSE-002](002-representation-invariants.md) owns validity proofs, [DSE-003](003-operation-contracts.md) owns invalidation and alias contracts, and [DSE-004](004-time-space-and-allocation-cost.md) owns resource accounting. DSE-006 adds cache behavior; DSE-011 through DSE-020 implement concrete sequence structures.

## Governing Question

When should a sequence be encoded as a region whose element location is computed arithmetically, and when should it be encoded as individually addressable nodes whose order is carried by links?

The choice is not “arrays are fast, lists insert fast.” Element width, ownership, search path, update position, relocation, allocator, concurrency, mutation patterns, view requirements, and machine hierarchy all matter. A useful comparison begins with the same abstract contract and derives concrete obligations for each representation.

## Why This Matters

Layout shapes every later data structure. Hash-table buckets can be contiguous control bytes or linked chains. Trees use linked nodes, array heaps, packed pages, or implicit indices. Graphs use node objects, edge arrays, compressed sparse regions, or hybrids. Persistent and concurrent structures add sharing and reclamation constraints.

Layout defects can violate memory safety and abstract behavior. An off-by-one array shift overwrites a neighbor; a stale pointer after growth becomes use-after-free; one missed doubly linked update corrupts future removal; an ownership cycle leaks; a forged index escapes a region. Production design needs representation invariants, checked arithmetic, and explicit authority—not only complexity tables.

## Prerequisites and Retrieval

You should know arrays, references/pointers, integer arithmetic, object identity, sequences, and DSE-001 through DSE-004. Retrieve:

1. Abstract sequence order is independent of physical address order.
2. Representation invariants define live elements, capacity, ownership, and link consistency.
3. Operation costs must include locating an update position.
4. Address/reference stability is observable only when the contract exposes it.
5. Logical element count does not determine exact memory bytes.
6. A view and its backing storage share lifetime and mutation consequences.

## Learning Objectives

After completing this module, you should be able to:

- define contiguous and linked sequence representations and abstraction functions;
- derive random-access and traversal costs from location mechanisms;
- reason about shifts, link rewrites, allocation, and position-search costs;
- specify live ranges, capacity, acyclicity, neighbor consistency, and sentinel invariants;
- compare singly, doubly, circular, intrusive, non-intrusive, and index-linked designs;
- calculate symbolic representation overhead without inventing platform constants;
- state relocation, iterator, view, handle, and element-reference invalidation;
- choose array-of-structures, structure-of-arrays, unrolled, or segmented hybrids deliberately;
- validate boundary updates and hostile/corrupt representations;
- separate structural reasoning from DSE-006's machine-locality evidence.

## Core Exposition

**Begin with one abstract sequence.** Let the abstract value be finite sequence $S=\langle e_0,\ldots,e_{n-1}\rangle$. Both representations must implement the same observations and updates: length, indexed lookup if promised, iteration, insertion, removal, and element mutation/ownership. Physical differences matter only through the published contract and resource behavior.

**Contiguous representation.** A low-level contiguous array owns a region starting at base (B), with capacity (c), element stride (s), and live size $n\le c$. Its abstraction function reads live slots $0$ through (n-1) in increasing index. Unused capacity is outside the abstract sequence.

When the language and ABI guarantee fixed stride, locating index (i) uses checked offset $i\cdot s$. The calculation must avoid integer overflow and remain within the same allocated object/region under the language's pointer rules. Bounds checks, provenance, alignment, and lifetime remain required; an arithmetic formula does not authorize arbitrary memory access.

“Contiguous elements” can still mean contiguous references rather than contiguous pointee objects. A Python list or Java `ArrayList`, for example, holds references in an array-like backing representation; referenced objects can live elsewhere. A packed array of 64-bit values has a different layout and ownership graph. State the element representation.

Capacity enables growth without every append reallocating. The invariant includes $0\le n\le c$, initialized live slots, and a valid backing region for capacity. Growth may allocate/copy and invalidate aliases as specified in DSE-003/004. Shrinking can release, retain, or compact storage; logical size alone does not decide.

**Insertion and removal in a region.** To insert at index (i), create room and shift live suffix (S[i:n]) one slot right, unless a gap or segmented layout changes the representation. The number of moved elements is (n-i). Remove shifts the suffix left by (n-i-1) and handles the now-unused final slot according to ownership/destruction rules.

Shifts can overlap. Low-level copying must use operations correct for overlap and element move/destruction semantics. If element construction can fail, operation ordering determines failure atomicity. Trivially movable bytes, reference slots, and objects with custom move/destruction are distinct cases.

Appending at the end avoids shifting but can grow. Removing from the end avoids shifts but may destroy/release an element. Clearing (n) owned objects can be $\Theta(n)$ even if resetting a size field is constant for trivially managed slots.

**Linked representation.** A singly linked node contains payload and successor. The root identifies the first node; null or sentinel ends traversal. The abstraction function follows links and collects payloads. Validity requires that every followed node is live, owned/shared according to policy, and part of the intended chain.

For an ordinary finite singly linked list, reachable nodes are acyclic and the final successor is null. A circular list deliberately points the final node to a sentinel/head; its invariant names that one cycle and iteration stops upon returning to the sentinel. “No cycles” would incorrectly reject it, while unconstrained cycles make traversal nonterminating.

A doubly linked node adds predecessor. Boundary variants store nullable head/tail links or use a sentinel whose `next`/`prev` point to itself when empty. Sentinels reduce special cases, but they need a non-payload identity and cannot leak as an element. Neighbor consistency must hold in both directions.

**Finding versus updating.** Indexed access in a singly linked list traverses from head, taking (i+1) node visits in a simple model. Inserting after an already-valid node can use a constant number of link writes. Inserting at index (i) from only the root still requires $\Theta(i)$ traversal.

Doubly linked lists support constant link rewrites around a known node and traversal from either end when tail/size are available. They do not make arbitrary index lookup constant. Complexity tables must state whether a cursor/iterator/node handle is an input and what validates it.

**Safe link update order.** For singly linked insertion after `p`, initialize `new.next = p.next` before publishing `p.next = new`. For removal after `p`, retain victim/successor references, redirect `p.next`, then destroy or detach victim under ownership rules. A callback/destructor can make even this sequence reentrant, so implementation language and contract matter.

For doubly linked insertion between `p` and `q`, establish `new.prev=p`, `new.next=q`, then connect neighbors under exclusive mutation or an explicit protocol. A failed/interleaved partial update can make forward and backward traversals disagree. Public operations either remain invariant-valid throughout observable execution or protect transient states.

**Ownership and lifetime.** A non-intrusive list owns wrapper nodes and stores values or references. Removing a node destroys/recycles the wrapper and returns/transfers payload according to contract. External code should not retain raw wrapper pointers unless stable handles and lifetime validation are promised.

An intrusive list stores link fields inside the element. It avoids wrapper allocation, permits known-node removal, and can improve control over layout. But one link field normally permits membership in only one list at a time. Multiple memberships need separate hooks. The list may not own the element; removal and element destruction must coordinate to avoid dangling links.

Garbage-collected references prevent some dangling-address bugs but do not automatically preserve list invariants. Detached nodes can remain reachable through external aliases; cycles can retain objects depending on runtime; mutation through a shared node can corrupt multiple owners. Ownership is a semantic contract, not merely a deallocation mechanism.

**Indices, handles, and compact links.** Links need not be machine pointers. An index into a node pool can be smaller, relocatable with the pool, serializable under a schema, and bounds-checkable. It may also suffer stale reuse: old index 7 can name a new node after deletion. Generation-tagged handles pair slot index with version and reject mismatches.

Relative offsets can make regions position-independent but require checked arithmetic and range limits. Compressed pointers trade address range and decode work for density. Every encoding defines a new representation invariant and trust boundary.

**Relocation and invalidation.** A contiguous buffer may move during growth/compaction. Raw element addresses, iterators, spans, and views into the old region then become invalid unless the runtime updates them or an indirection layer stabilizes identity. Index values can remain meaningful if element order is preserved, but insertion/removal changes indices.

Linked node addresses can remain stable across insertion if nodes are individually allocated and not moved. That is not intrinsic to “linked”: compacting GC, arena compaction, pool relocation, or serialized reload can move/rebind nodes. Publish only the stability the actual mechanism supports.

Handles add indirection so movement can update a table while stable identities persist. This costs lookups, table space, synchronization, and reclamation complexity. Pinning prevents movement but fragments or constrains memory management.

**Views, slices, and copies.** A contiguous slice can be represented by `(base, offset, length, stride)` without copying. Its validity depends on backing lifetime, mutation, and relocation. A writable view grants authority over shared storage; an immutable view can still observe mutations by the owner unless it is a snapshot.

A linked subrange view usually needs start/end handles and traversal; splitting/concatenating can be cheap with maintained endpoints but indexing remains traversal-based. Copying either representation produces a new container but may still shallow-share element objects. Deep copy requires a graph/identity policy and can be undefined for resources or cycles.

**Space accounting.** For fixed-width contiguous slots, symbolic steady storage is header (H_a), capacity $c\cdot s$, alignment/padding, and allocator overhead. Slack is ((c-n)s). Resize peak can include old and new regions as DSE-004 showed.

For a non-intrusive singly linked sequence, each node adds header, one link, payload/reference, padding, and allocation overhead; a doubly linked node adds another link. Allocator granularity can dominate small nodes. Intrusive hooks move link bytes into elements and may avoid wrapper allocation, but bytes still exist.

Linked structures can allocate nodes from a contiguous arena, combining stable index links with dense storage. Conversely, a segmented array can use several blocks and a directory, relaxing full contiguity. Layout is a spectrum rather than two mutually exclusive classes.

**Array of structures and structure of arrays.** For records `(x,y,active)`, an array of structures stores each complete record together; a structure of arrays stores separate arrays for each field. AoS favors whole-record access and direct element identity. SoA favors field-wise bulk operations, compression, and selective loading. It complicates insert/delete synchronization and references to one logical record.

Hybrid arrays-of-small-blocks, unrolled lists, chunked sequences, gap buffers, ropes, and piece tables tune movement, indirection, stable positions, and slack for workloads. DSE-013 and DSE-020 develop editor-oriented hybrids; external-memory blocks appear later.

**Locality boundary.** Contiguous layouts often enable fewer allocations and predictable address progression; linked nodes often introduce indirection and variable placement. These facts motivate cache analysis but do not by themselves prove performance. Hardware prefetching, node pools, element size, operation mix, compiler, and cache hierarchy decide observed behavior. DSE-006 owns that evidence.

**Concurrency boundary.** Contiguous growth changes a global buffer and commonly needs exclusive publication or versioning. Linked structures can update localized links but safe concurrent algorithms must handle atomicity, reachability, ABA, and memory reclamation. “Only two pointers change” is not a concurrency proof. DSE-061 through DSE-070 develop those protocols.

**Serialization and trust.** Raw addresses are process-specific capabilities, not durable references. Serialize abstract elements or validated indices/offsets under a versioned format. On load, validate sizes before allocation, arithmetic, bounds, cycles, duplicate ownership, and termination. Do not follow untrusted links before validating their range and budget.

**Testing representation seams.** Compare both implementations against one reference sequence using generated traces. Exercise empty/singleton, head/tail/middle, repeated insert/remove, capacity boundaries, alias/view invalidation, duplicate handles, stale generations, allocation failure, and corrupt links. Check forward/backward traversal, size, ownership, and absence of lost nodes.

The executable model below compares logical values and explicitly counted modeled steps. Python's own lists/objects are not used as evidence of physical contiguity or machine timing.

<!-- bijux-verify: {"id":"contiguous-linked-step-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"before_equal=True\nindex3=array:40 linked:40 steps=1,4\ninsert_index=2 array_shifts=3 linked_search_steps=2 link_writes=2\nafter=(10, 20, 25, 30, 40, 50)\nevidence=modeled_steps_not_machine_timing\n","stderr":""}} -->
```python
class Node:
    def __init__(self, value, next_node=None):
        self.value = value
        self.next = next_node


def linked_from(values):
    head = None
    for value in reversed(values):
        head = Node(value, head)
    return head


def linked_snapshot(head):
    values = []
    node = head
    while node is not None:
        values.append(node.value)
        node = node.next
    return tuple(values)


def linked_get(head, index):
    node = head
    visits = 1
    for _ in range(index):
        node = node.next
        visits += 1
    return node.value, visits


array = [10, 20, 30, 40, 50]
head = linked_from(array)
print(f"before_equal={tuple(array) == linked_snapshot(head)}")
linked_value, visits = linked_get(head, 3)
print(f"index3=array:{array[3]} linked:{linked_value} steps=1,{visits}")

insert_index = 2
array_shifts = len(array) - insert_index
array.insert(insert_index, 25)
predecessor = head
linked_search_steps = 1
for _ in range(insert_index - 1):
    predecessor = predecessor.next
    linked_search_steps += 1
predecessor.next = Node(25, predecessor.next)
print(
    f"insert_index={insert_index} array_shifts={array_shifts} "
    f"linked_search_steps={linked_search_steps} link_writes=2"
)
print(f"after={linked_snapshot(head)}")
print("evidence=modeled_steps_not_machine_timing")
```

## Definitions and Notation

Let abstract sequence be $S\in E^*$. A contiguous representation is (R_a=(B,n,c,s,slots)), with $0\le n\le c$, valid layout/alignment, and

$$
AF_a(R_a)=\langle slots[0],\ldots,slots[n-1]\rangle.
$$

A linked representation is (R_l=(N,h,next,value,owner)). For a null-terminated acyclic list, repeated `next` from (h) visits distinct owned live nodes $v_0,\ldots,v_{n-1}$ then null, and

$$
AF_l(R_l)=\langle value(v_0),\ldots,value(v_{n-1})\rangle.
$$

For a doubly linked list, `prev(next(x))=x` and `next(prev(x))=x` wherever both sides are applicable. For a sentinel list, replace null termination with a unique sentinel cycle and exclude sentinel payload from (AF_l).

A handle (H=(slot,generation)) resolves only when the slot is live and its stored generation equals `generation`. A view (V=(owner,revision,range,mutability)) is valid only under the owner's lifetime/invalidation contract.

## Mechanisms, Invariants, or Proof Structure

**Contiguous access.** Given valid index, fixed stride, checked multiplication/addition, and live backing region, address calculation selects the corresponding slot. The proof depends on language provenance/alignment rules, not arithmetic alone.

**Array insertion.** Preserve prefix, shift suffix without overwriting unread elements, construct the new slot, increment size, and maintain capacity. Prove exact abstract successor and failure rollback.

**Linked traversal.** Acyclic finite reachability supplies termination; each step follows the unique successor. Induction on position connects the (i)-th reached node to abstract element (S[i]).

**Link insertion.** With valid owned predecessor `p`, initialize new successor from old `p.next`, then publish `p.next=new`; show prefix, inserted value, and suffix correspondence. Doubly linked cases additionally restore inverse links.

**Ownership closure.** Every reachable wrapper is owned exactly once unless sharing is explicitly modeled; every owned logical node is reachable; removed nodes are detached before reuse/destruction.

**Handle validation.** Bounds and generation equality reject stale/reused slots. Generation width and wraparound policy remain explicit.

**Finite evidence boundary.** The snippet validates one six-element outcome and modeled operation counts. It does not establish physical layout, byte size, cache behavior, allocator effects, memory safety, concurrency, or all traces.

## Alternatives and Trade-Offs

**Contiguous versus linked.** Contiguous layout offers direct indexing, compact metadata, and bulk movement; insertion may shift or relocate. Linked layout supports local rewiring at known nodes and addressable node identity; traversal and per-node overhead increase.

**Singly versus doubly linked.** One link minimizes node space. Two links permit reverse traversal and known-node removal without predecessor search, at added bytes and invariant updates.

**Null boundaries versus sentinel.** Null head/tail makes termination explicit but creates boundary branches. A sentinel unifies cases but adds a distinguished node/cycle and leak/exclusion obligations.

**Intrusive versus wrapper nodes.** Intrusive hooks avoid wrapper allocations and support known-object removal. They couple element layout/lifetime to structure and require separate hooks for multiple memberships.

**Pointers versus indices/handles.** Pointers provide direct addressing within language rules. Indices compress/serialize and permit relocation; generation handles detect reuse but add lookup and version management.

**AoS versus SoA.** AoS groups complete records; SoA groups fields. Workload, vectorization, selective access, mutation synchronization, and identity decide.

**Pure versus hybrid layout.** Unrolled/segmented designs trade fewer allocations and bounded shifts against directories, block slack, and more complex invariants.

## Failure Modes and Misconceptions

1. **“Contiguous means values themselves are adjacent.”** The region may contain references to scattered objects.
2. **“Linked insertion is O(1).”** Only link rewrites at an already-known valid position are constant.
3. **“Arrays cannot provide stable handles.”** Indirection/generation tables can, with costs.
4. **“Linked nodes never move.”** Compaction, arenas, serialization, or GC can relocate/rebind them.
5. **“A sentinel removes invariants.”** It changes boundary invariants and traversal termination.
6. **“Doubly linked removal needs one assignment.”** Both neighbors, endpoints, ownership, and victim state matter.
7. **“Garbage collection prevents dangling structure.”** Logical stale aliases and invariant corruption remain possible.
8. **“A slice is a copy.”** Many slices/views share backing storage and invalidation.
9. **“Index links cannot dangle.”** Slot reuse makes stale indices name unrelated nodes unless validated.
10. **“Raw pointers can be serialized.”** Process addresses are not durable identities.
11. **“Same O(n) space means same memory.”** Metadata, slack, headers, padding, and allocation rounding differ.
12. **“Contiguity proves faster execution.”** Machine/workload measurements and cache analysis are still required.
13. **“Two pointer writes make an update thread-safe.”** Atomicity and reclamation need concurrency protocols.
14. **“A passing traversal proves ownership.”** Lost, multiply owned, unreachable, or externally mutable nodes may remain.

## Worked Examples

### Example 1

**Question:** What does array address arithmetic require beyond `base + i * stride`?

**Reasoning:** Validate index, multiplication/addition overflow, backing lifetime, object bounds/provenance, stride, alignment, and initialized live slot.

**Conclusion:** Arithmetic is one step in a memory-validity proof.

### Example 2

**Question:** Why does inserting at array index two of five shift three elements?

**Reasoning:** Old elements at indices 2, 3, and 4 must move to 3, 4, and 5 before writing the new element.

**Conclusion:** Shift cost is (n-i), excluding growth/destruction details.

### Example 3

**Question:** When is linked insertion constant-time?

**Reasoning:** The caller supplies a currently valid predecessor/node handle, and allocation/link writes have the stated cost. Searching by index/value is separate.

**Conclusion:** Include how the update location is obtained.

### Example 4

**Question:** What breaks if a doubly linked insertion updates only forward links?

**Reasoning:** Forward traversal may show the new node while backward traversal skips it; later known-node removal can corrupt neighbors.

**Conclusion:** Bidirectional agreement is one invariant, not two optional optimizations.

### Example 5

**Question:** Why can one intrusive hook not join two lists?

**Reasoning:** Each list needs independent predecessor/successor state. The second insertion overwrites links used by the first unless separate hooks exist.

**Conclusion:** Membership capacity is part of element layout and contract.

### Example 6

**Question:** What survives contiguous reallocation?

**Reasoning:** Abstract value/order and integer indices can survive if promised; raw addresses, iterators, slices, and references into the old buffer generally do not.

**Conclusion:** Logical and address identity differ.

### Example 7

**Question:** How does a generation handle reject stale reuse?

**Reasoning:** Removal advances the slot generation; an old `(slot,generation)` no longer matches even if the slot holds a new node.

**Conclusion:** Reuse detection needs a version and wraparound policy.

### Example 8

**Question:** When can SoA be better than AoS?

**Reasoning:** A scan reading only one numeric field avoids loading other record fields and supports dense field operations. Whole-record mutation/identity becomes more complex.

**Conclusion:** Field-access workload, not fashion, determines layout.

### Example 9

**Question:** Why is an arena-backed linked list still linked?

**Reasoning:** Abstract order is encoded by successor links/indices even if nodes occupy one dense allocation. Physical adjacency does not create index order semantics.

**Conclusion:** Allocation placement and logical linkage are independent dimensions.

### Example 10

**Question:** A linked structure represents commands in an aircraft-control subsystem. What review exceeds representation tests?

**Reasoning:** Engineers verify bounds, ownership, termination, update atomicity, stale handles, fixed capacity, allocation/reclamation, concurrency, corruption detection, timing, persistence, and exact implementation identity. Domain, real-time, safety, security, quality, human-factors, and regulatory reviewers validate command semantics and integrated hazards. This chapter claims no such approval.

**Conclusion:** A correct layout cannot establish system-level safety or domain correctness.

## Cross-Program Connections

- [Systems Programming](../../05-programming-languages-systems-programming/ROADMAP.md) supplies pointers, provenance, ownership, alignment, allocation, and unsafe boundaries.
- [Concurrent & Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) owns atomic publication and reclamation protocols.
- [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) analyzes traversal, shifts, and workload cost.
- [Operating Systems](../../22-operating-systems/ROADMAP.md) explains virtual memory and allocators underlying layouts.
- [Computer Architecture](../../23-computer-architecture/ROADMAP.md) supplies cache, prefetch, bandwidth, and alignment behavior.
- [Database Engineering](../../18-database-engineering/ROADMAP.md) develops page, record, slot, and index layouts for durable storage.

## References

1. Rust Project, [*The Rustonomicon: Alternative representations*](https://doc.rust-lang.org/nomicon/repr-rust.html). Field layout, alignment, padding, and representation guarantees.
2. Rust Project, [*The Rust Reference: Type layout*](https://doc.rust-lang.org/reference/type-layout.html). Current normative size, alignment, array, slice, pointer, and representation rules.
3. ISO C++ working draft, [Basic concepts: Types](https://eel.is/c++draft/basic.types). Object representation, layout, lifetime, and pointer-related requirements.
4. LLVM Project, [*LLVM Language Reference: Data Layout*](https://llvm.org/docs/LangRef.html#data-layout). Target layout, pointer, alignment, aggregate, and allocation-size specification.
5. Linux Kernel documentation, [Linked Lists in Linux](https://www.kernel.org/doc/html/latest/core-api/list.html). Intrusive circular doubly linked lists, traversal, mutation, and concurrency cautions.
6. Python Software Foundation, [Python/C API: List Objects](https://docs.python.org/3/c-api/list.html). List object operations, indices, references, and mutation boundaries.
7. Python Software Foundation, [Python/C API: MemoryView Objects](https://docs.python.org/3/c-api/memoryview.html). Views over buffer-protocol exporters and ownership behavior.
8. Pat Morin, [*Open Data Structures*, Python edition](https://opendatastructures.org/ods-python.pdf). Array- and linked-list representations, invariants, operations, and analysis.
9. Oracle, [Java SE 25 `LinkedList` API](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/LinkedList.html). Current doubly linked list operation and iterator contracts.
10. Oracle, [Java SE 25 `ArrayList` API](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/ArrayList.html). Current resizable-array operation, capacity, and iterator contracts.

## Exercises

### Exercise 1

Write representation invariants and abstraction functions for a size/capacity contiguous sequence and a null-terminated doubly linked sequence. Include empty and singleton cases.

### Exercise 2

Derive modeled operation counts for lookup and insertion at indices 0, (n/2), and (n) for an array and singly linked list, both with and without a supplied predecessor handle.

### Exercise 3

Design a generation-tagged pool representation for linked nodes. Specify allocation, removal, resolution, generation wraparound, and stale-handle errors.

### Exercise 4

Compare symbolic space for a contiguous array, non-intrusive doubly linked list, and intrusive list. Include payload/reference choice, slack, headers, links, padding, allocator overhead, and resize peak.

### Exercise 5

Prepare a verification plan for migrating a public linked representation to segmented contiguous storage without breaking abstract behavior or exposed handles. Cover compatibility, failures, concurrency, measurements, hostile states, rollout, and human review.

## Answers to the Exercises

### Answer 1

For array `(slots,n,c)`, require integers `0 <= n <= c`, valid backing storage for `c` correctly laid-out slots, initialized/owned live slots `[0,n)`, and an explicit unused-region policy. Its abstraction is live values in increasing index. For doubly linked `(head,tail,size)`, empty means both endpoints null and size zero; nonempty means head.prev and tail.next are null, following `next` visits exactly `size` distinct owned live nodes ending at tail/null, and every adjacent pair agrees through `prev`. Singleton has head=tail with both boundary links null. Its abstraction is payloads in forward traversal order.

### Answer 2

Array lookup is one modeled address access at any valid index. Singly linked lookup from head visits `i+1` nodes. Array insertion shifts `n-i` elements, plus construction and possible growth. Linked insertion from head visits the predecessor: index zero needs a head update; middle index `i>0` visits `i` nodes before constant link writes; append visits `n` without a tail, or uses constant linking with a valid tail/predecessor handle. With a supplied validated predecessor, linked rewiring is constant at all non-head positions; validation/allocation remain separate costs.

### Answer 3

Store pool slots with `{live,generation,payload,next}` and handles `(index,generation)`. Allocation selects a free slot, checks capacity, marks live, initializes payload/link, and returns its current generation. Resolution bounds-checks index, requires live and equal generation, then returns node authority. Removal detaches the node, clears owned state, marks free, and advances generation before reuse. Use a sufficiently wide nonwrapping generation or define exhaustion/quarantine; wrapping can make an ancient handle valid again. Invalid, removed, wrong-owner, or generation-mismatched handles return explicit errors without mutation.

### Answer 4

Let contiguous header be `Ha`, capacity `c`, slot stride `s`, and allocation overhead `Ra(c)`; steady bytes are `Ha+c*s+Ra(c)`, slack `(c-n)*s`, and copy-resize peak includes old and new regions. For non-intrusive doubly linked nodes, use list header `Hl` plus `n*(Hn+payload_or_reference+2p+padding+Rn)`. For intrusive layout, the element already owns two hook fields, so list-specific external wrapper/allocation may disappear, but total elements still contain `2p` plus padding and their primary allocation costs. If elements exist independently, allocate/count ownership accordingly. No comparison is numeric until ABI, runtime, allocator, element representation, and ownership scope are pinned.

### Answer 5

Freeze abstract value, order, equality, operations, errors, iterator/view semantics, handle lifetime, concurrency, complexity, serialization, and failure guarantees. Inventory clients relying on node identity or accidental address stability. Introduce stable generation handles or an adapter before movement; version serialized forms and validate mixed-version rollback. Prove segmented invariants, index arithmetic, capacity/overflow, update correspondence, failure atomicity, and handle resolution. Differentially model-test traces against the old implementation; inject allocation/corruption/cancellation, stress concurrent histories, fuzz sizes/segments/stale handles, and benchmark workloads for latency, peak memory, allocation, and locality under pinned environments. Roll out with telemetry, compatibility gates, rollback, and data migration verification. Independent data-structure, systems, concurrency, security, API, operations, domain, safety/quality reviewers approve their scopes; no local equivalence test alone proves production fitness.
