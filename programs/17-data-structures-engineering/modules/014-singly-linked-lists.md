---
module_id: DSE-014
program: Data Structures Engineering
level: 1
module_number: 14
title: Singly Linked Lists
status: complete
last_verified: 2026-08-29
---

# Singly Linked Lists

## One-Page Review

### Governing question

How can a one-way chain represent a finite sequence safely, and which ownership, predecessor, failure, iterator, layout, and concurrency contracts determine whether its apparently simple pointer rewiring is correct and worthwhile?

### Essential definitions

- A **singly linked list** is a sequence represented by a head link and nodes containing one element plus one link to the next node.
- A **link** may be a raw pointer, managed reference, index, handle, smart pointer, or tagged option; its representation determines lifetime and aliasing obligations.
- The **head** identifies the first node or empty state. A **tail** field, if stored, identifies the last node and must remain synchronized.
- The **successor relation** follows `next`; the ordinary finite-list invariant requires one acyclic path from head to termination.
- A **predecessor** of node `x` is a node whose `next` refers to `x`. A singly linked node does not directly reveal its predecessor.
- A **sentinel** is a structural node that simplifies boundary rewiring but is not an element of the abstract sequence.
- **Ownership** answers who releases nodes; **reachability** answers which nodes can be followed; **identity** answers whether two links denote the same node. These are distinct.
- **Structural sharing** intentionally lets immutable versions share suffixes. It is incompatible with a mutable-list invariant that grants one exclusive owner to every reachable node unless extra coordination is added.
- **Iterator invalidation** states which observers remain usable after insertion, erasure, transfer, or destruction.
- **Pointer chasing** is serial traversal through dependent node addresses. Its realized cost depends on allocation, layout, caching, prefetching, runtime, and workload.

### Central model, mechanism, or theorem

Let `reach(head)` follow `next` until the termination link. For a mutable exclusive chain with stored size `n`, require:

1. traversal terminates after exactly `n` distinct live nodes;
2. those node values in traversal order equal the abstract sequence;
3. every reachable `next` is either termination or a valid link to the next owned node;
4. no owned node is reachable from another independently mutable list;
5. if a tail is stored, `n=0` iff `head=tail=null`, and otherwise tail is the last reachable node with `tail.next=null`.

Given a valid predecessor `p`, insertion after `p` allocates/constructs `x`, sets `x.next=p.next`, then sets `p.next=x`. Erasure after `p` saves `victim=p.next`, redirects `p.next=victim.next`, updates metadata, then destroys/releases `victim` only after no list link needs it. Reversing repeatedly changes `(prev,cur,next)` while preserving a partition of the original chain.

### Critical invariants

1. Head is termination exactly for the empty list; otherwise it identifies one live first node.
2. Successor traversal is acyclic and terminates after the declared size.
3. Each reachable node appears exactly once in the mutable exclusive sequence.
4. Values encountered from head equal the abstract sequence in order.
5. Every node and link obeys alignment, provenance, initialization, lifetime, and reclamation rules.
6. Stored head, tail, size, allocator, sentinel, and ownership metadata agree after every committed operation.
7. Failure cannot publish a link to an unconstructed node or lose ownership of an old subchain.
8. Iterators, references, handles, and concurrent readers follow an explicit validity/reclamation contract.

### Common failures

- Claiming constant-time insertion without already having the predecessor or an equivalent cursor.
- Losing the remaining chain by overwriting `current.next` before saving it during reversal.
- Creating a cycle by linking a list to one of its own reachable nodes.
- Freeing a node before unlinking it, or dereferencing it after reclamation.
- Forgetting the head, tail, size, or sentinel boundary case on erase or transfer.
- Sharing a mutable suffix between lists whose methods assume exclusive ownership.
- Treating a managed reference as proof that semantic aliasing and concurrency are safe.
- Assuming stable node addresses imply stable positions or valid erased-node iterators.
- Recursively traversing or destroying an adversarially long chain without a stack-depth contract.
- Repeating `append` by head traversal and accidentally building a quadratic workload.
- Assuming a linked list is faster because insertion rewires one link, or slower by a universal hardware ratio.
- Publishing a new link concurrently without memory ordering and safe reclamation.

### Compact example

Starting with `A -> B -> C`, prepend `Z`, remove the first `B`, and reverse. The final chain is `C -> A -> Z`. A temporary `tail.next=head` mutation lets Floyd's tortoise-and-hare algorithm observe a cycle; restoring termination makes the representation valid again. The finite trace checks values, size, tail termination, and acyclicity, but does not prove memory safety in raw-pointer implementations.

### Connections

[DSE-001](001-abstract-data-types-and-concrete-representations.md) and [DSE-002](002-representation-invariants.md) supply abstraction and invariants; [DSE-003](003-operation-contracts.md) supplies failure and ownership contracts; [DSE-005](005-contiguous-and-linked-layouts.md) and [DSE-006](006-memory-locality-and-cache-behavior.md) supply layout analysis; [DSE-008](008-iterators-and-traversal-protocols.md) supplies iterator semantics. The [program roadmap](../ROADMAP.md) continues with doubly and intrusive lists, then stack and queue specializations.

## Governing Question

What exact representation, ownership discipline, pointer-transition order, iterator contract, and evidence plan allow a singly linked list to preserve a finite sequence—and when do access patterns, memory layout, latency, concurrency, or persistence require a different structure?

## Why This Matters

A singly linked list is often taught as two boxes and an arrow. That picture communicates topology but omits almost every production obligation. What kind of link is the arrow? Who owns the node? Can two lists share a suffix? What happens if allocation fails? Does an iterator remain valid? Can a reader follow a node while another thread erases it? Does a stored tail still name the last node after a transfer?

The representation is valuable precisely because one-way linkage is minimal. Given the right position, insertion and erasure can change a constant number of links without shifting unrelated elements. Nodes can have stable addresses under many allocation models. Immutable chains can share suffixes efficiently. Hash buckets, free lists, adjacency structures, stacks, queues, and persistent histories can exploit these properties.

Minimal linkage also removes capabilities. Random access and predecessor discovery require traversal. Per-node allocation and metadata can dominate small values. Traversal is dependent pointer chasing rather than a contiguous scan. A correct design therefore begins with workload and contracts, not with the slogan that linked-list insertion is `O(1)`.

## Prerequisites and Retrieval

Before this module, retrieve:

- abstraction functions, concrete representations, reachability, and invariant preservation from [DSE-001](001-abstract-data-types-and-concrete-representations.md) and [DSE-002](002-representation-invariants.md);
- preconditions, failure guarantees, ownership, aliases, and observability from [DSE-003](003-operation-contracts.md);
- time, allocation, byte, locality, and tail-latency models from [DSE-004](004-time-space-and-allocation-cost.md), [DSE-005](005-contiguous-and-linked-layouts.md), and [DSE-006](006-memory-locality-and-cache-behavior.md);
- generic element construction, destruction, and constraints from [DSE-007](007-genericity-and-type-constraints.md);
- iterator invalidation, model-based testing, and representative measurement from [DSE-008](008-iterators-and-traversal-protocols.md), [DSE-009](009-property-based-testing-of-data-structures.md), and [DSE-010](010-benchmarking-a-structure-without-misleading-results.md);
- contiguous alternatives and their invalidation/growth behavior from [DSE-011](011-fixed-arrays.md) through [DSE-013](013-gap-buffers.md).

## Learning Objectives

After completing this module, you should be able to:

1. define singly linked mutable, sentinel-based, index-linked, and immutable shared representations;
2. state reachability, acyclicity, size, tail, ownership, and lifetime invariants precisely;
3. derive insertion and erasure transition order from those invariants;
4. prove in-place reversal using a loop invariant and termination measure;
5. distinguish node discovery cost from rewiring cost and end-to-end operation cost;
6. specify allocator failure, element failure, cleanup, and invalidation behavior;
7. diagnose lost subchains, cycles, stale tails, double release, leaks, and shared-mutation corruption;
8. compare null termination, sentinels, stored tails, cursors, pools, and persistent suffix sharing;
9. design model, fault, memory, concurrency, and performance evidence for a list implementation;
10. decide when arrays, deques, chunked sequences, intrusive lists, or concurrent queues better satisfy the system contract.

## Core Exposition

**Define the abstract value before the nodes.** The abstract value is a finite sequence `A=<a0,...,a(n-1)>`. The simplest representation stores `head`; every live node stores `(value,next)`, and a distinguished termination link ends traversal. Starting at head and repeatedly following next must visit exactly the nodes whose values form `A`, in order, then terminate.

This definition rules out cycles and accidental branching but does not yet define ownership. In a raw-pointer mutable list, the container might exclusively own every reachable node. In a garbage-collected runtime, reachability keeps nodes alive, yet application-level aliases can still mutate shared state. In a reference-counted persistent list, multiple heads intentionally share a suffix and nodes are immutable. These are different abstractions with different valid operations.

**Recursive topology needs finite representation.** Mathematically, a list is empty or an element paired with another list. A concrete node cannot contain another node of the same unbounded type inline, because its size would be recursively infinite. Indirection gives the link a fixed representation size. Rust's reference and book use `Box` to explain this boundary for recursive types. Other languages encode it with references or pointers; index-linked pools use an integer-like handle.

The termination representation can be null/nil/`None`, a tagged empty variant, a distinguished index, or a sentinel. Null termination is compact and familiar, but every boundary must handle absence. A head sentinel makes “predecessor of the first element” representable and supports uniform `insert_after` and `erase_after`. The sentinel is structural, so iteration, size, equality, and serialization must exclude it.

**Reachability is the core invariant.** Let `R(head)` be the ordered nodes visited until termination. A finite exclusive mutable list requires every node in `R` to be live and valid, no identity repeated, and no next edge from `R` to unowned invalid memory. Stored size equals `|R|`; stored tail, if present, equals the last node or the empty value. The abstraction maps each node to its element.

Checking the full invariant is linear because it traverses the chain and records identities or uses cycle detection plus a count. Production operations generally preserve it by local reasoning rather than scan after every mutation. Debug validation and property tests can afford broader checks. A size field makes `size()` constant time but adds a metadata update to every length-changing path. ISO C++ deliberately omits `size()` from `forward_list` to avoid requirements that conflict with its stated minimal-overhead design.

**Prepend is the minimal transition.** To prepend value `x`, first allocate and fully construct a node `q` whose `next` is the old head. Only after that succeeds, publish `head=q`; increment size and set tail if the list was empty. The new abstraction is `<x> + A`. If allocation or value construction fails before publication, destroy any partial state and leave the old list unchanged under a strong guarantee.

In a concurrent structure, “publish” is literal and requires synchronization: initializing fields then storing head with a suitable release operation can let an acquiring reader observe them, but this alone does not solve lost concurrent updates, deletion, ABA, or reclamation. Single-threaded transition order is not a lock-free algorithm.

**Insertion needs a position contract.** Given a valid predecessor node `p` in the list, insertion after `p` performs:

1. construct new node `q` with value `x`;
2. set `q.next=p.next`;
3. set `p.next=q`;
4. update tail if `p` was the old tail, then size.

The order matters: overwriting `p.next` before saving its old successor loses the suffix. With a sentinel, inserting before the first element is simply insertion after the sentinel. Without one, inserting at the front needs the head path.

The rewiring is constant in the unit-link model, but finding the predecessor by numeric index `i` takes `Theta(i)`. An iterator/cursor already positioned at `p` can make the complete mutation constant-time only if its validity and membership preconditions hold. A pointer to the node to erase is insufficient in an ordinary singly linked list because the operation must change its predecessor's link; value-swapping tricks change identity semantics and fail at the tail.

**Erasure disconnects before reclamation.** Given predecessor `p`, require `p.next` to be a live victim `v`. Save `s=v.next`, set `p.next=s`, update tail if `v` was last, decrement size, then destroy the value and release `v` under the language's lifetime rules. The abstract result removes that one position.

Precisely when destruction happens depends on exception and concurrency models, but no future list operation may follow the victim after it becomes unreachable. A raw implementation that releases `v` before reading its successor performs use-after-free. A managed runtime prevents that physical error while local `v` remains referenced, but callbacks, finalizers, weak references, and shared aliases can still make behavior observable.

Erasing the first element can use a sentinel predecessor or a separate head update. Erasing the only element must also clear the stored tail. Erasing after the tail is invalid or returns no element according to the API. Range erasure must retain the node before the range and the node after it while destroying every removed node exactly once.

**Append exposes the tail trade-off.** Without a stored tail, append traverses all `n` nodes and then links a new last node: `Theta(n)`. Repeating this to build `n` elements costs `0+1+...+(n-1)=Theta(n^2)` link traversals. Prepending each element is linear total but reverses input order unless the input is consumed in reverse or the result is reversed once.

A stored tail makes append rewiring constant time after successful construction, but adds an invariant. Empty insertion sets both head and tail. Removing the only node clears both. Concatenation, move, split, clear, reverse, and failure must update tail correctly. The tail does not make predecessor discovery or pop-back constant time; removing the last node still needs its predecessor.

**Reversal is a pointer-state proof.** Maintain three links: `prev`, `cur`, and `next`. Initially `prev` terminates and `cur=head`. On each iteration, save `next=cur.next`, set `cur.next=prev`, then advance `prev=cur` and `cur=next`. Saving first prevents loss of the unprocessed suffix.

A useful loop invariant partitions the original sequence into an unprocessed suffix starting at `cur` and a processed prefix reachable from `prev` in reverse order. Their nodes are disjoint, live, and together equal the original node set. Each iteration moves one node from unprocessed to processed; the count of unprocessed nodes decreases. At termination, `prev` is the new head. For a stored-tail list, the old head becomes the new tail and terminates.

**Cycle detection diagnoses, but does not repair, corruption.** Floyd's algorithm advances one link by one step and another by two. In a finite acyclic chain, the faster link reaches termination. In a cycle, the two eventually meet. This uses constant extra space and linear time. A meeting proves a reachable cycle but does not by itself identify ownership cause, safe break point, cycle entry, or which node may be reclaimed.

An invariant checker should not blindly count until null, because a corrupted cycle makes it loop forever. It can use a visited-identity set for direct diagnostics or Floyd followed by a bounded count. Concurrent mutation invalidates the proof assumptions; observing a cycle-like state without synchronization may be a data race rather than a stable structure.

**Aliases decide whether sharing is valid.** The legacy archive correctly emphasizes that two independently mutable lists sharing a tail can corrupt each other's values and sizes. If list 1 truncates inside the shared suffix, list 2 changes too. Exclusive ownership forbids that topology and can be checked or enforced with unique pointers/borrows.

Structural sharing is nevertheless valuable for immutable persistent lists. `cons(x,L)` allocates one new node pointing to immutable `L`; old and new versions share the suffix safely because no next link or value changes. Reclamation uses garbage collection, reference counting, arenas, or a persistent ownership scheme. Updating an interior position requires path copying from the head to that position, not mutating the shared suffix. The chapter preserves this distinction rather than calling all sharing corruption.

**Element and node ownership can differ.** A node can own its element inline, hold a borrowed reference, or carry an external handle. Removing a node may destroy an inline value, decrement a smart reference, or leave an external object alive. Intrusive lists—developed in DSE-015—embed linkage inside externally owned objects, so unlinking and object lifetime are distinct. Never infer element lifetime solely from node reachability without the type contract.

Recursive destruction is elegant but can overflow the call stack on a long adversarial chain in runtimes without guaranteed tail-call elimination. An iterative clear can detach one node at a time and release it, but smart-pointer destructors may recursively release successors unless the implementation deliberately takes ownership of each next link before dropping the current node. Stack depth is a resource bound, not merely style.

**Iterator stability is operation-specific.** Node-based storage often preserves links/references to nodes unaffected by insertion because nodes do not relocate. Erasure invalidates observers to erased nodes. Transfer/splice can preserve node identity while changing container membership; an iterator can still refer to the element but now belong logically to another container. Destruction invalidates all owned-node observers.

These guarantees are language/library contracts, not consequences of drawing separate boxes. Pool compaction, moving garbage collectors, compact handles, debug generations, ownership transfers, and custom allocators change observer behavior. A numeric position is not stable under earlier insertion/erasure, even when a node address is.

**Layout can dominate link-count complexity.** A node commonly consumes element bytes, one link, alignment padding, and allocator metadata. Separate allocations increase bookkeeping and fragmentation. Traversal depends on the next address discovered from the current node, limiting independent memory-level parallelism. Compared with a contiguous array, it may incur more cache and translation misses and transfer unused metadata.

But no universal slowdown factor follows. Arena allocation can place nodes close together; a list may be tiny or already cached; elements may be large; the workload may require stable handles or constant-time splice; an array mutation may shift expensive elements. The legacy archive's useful warning about pointer chasing is retained as a hypothesis, while its machine-specific nanosecond ranges and universal conclusions are not. Measure target hardware, runtime, allocator, element sizes, access pattern, and full operation.

Index-linked pools store next as an integer offset into arrays or slabs. They can improve compactness, serialization, bounds checking, and locality while preserving one-way topology. Handles can carry generations to reject stale reuse. The trade-off is pool capacity/relocation policy, handle translation, free-list correctness, and possibly fixed maximums.

**Sorting and splicing exploit links.** Merging sorted chains can redirect links while preserving stable element identity and avoid moving element payloads. Merge sort divides and recombines lists in `O(n log n)` comparisons with link rewiring and no random access. Concatenating with a stored tail can be constant link work if ownership and allocator compatibility permit.

The ISO C++ `forward_list` contract exposes `before_begin`, `insert_after`, `erase_after`, and `splice_after` because predecessor access is fundamental. Its exact complexity, exception, allocator, iterator, reference, and precondition wording should be used for that type; a handwritten list does not inherit those guarantees automatically.

**Concurrency changes every proof boundary.** A data race on `next`, head, size, or element state is not repaired by nodes being separate. A mutex around the list can provide a simple linearizable contract, but long traversals increase contention. Fine-grained locks require lock ordering and safe hand-over-hand traversal. Lock-free algorithms require atomic links, a linearization point, retry logic, memory ordering, and a reclamation scheme such as hazard pointers, epochs, or RCU appropriate to the environment.

The ABA problem occurs when a link changes from identity A to B and back to a reused A representation; a compare-and-swap can succeed although intervening state changed. Tagged generations can help but wrap and representation constraints require analysis. Garbage collection can simplify physical reclamation but not linearizability or semantic races. Linux's RCU documentation demonstrates read-mostly list techniques with explicit reader, updater, ordering, and grace-period obligations; copying its macros or vocabulary outside that environment supplies no proof.

**Test transitions, not just output.** A reference model can be a simple array/list. Generate prepend, insert-after, erase-after, remove-by-value, reverse, clear, split, concatenate, and transfer sequences; after each operation compare abstract values and check reachability, acyclicity, size, tail, and ownership. Use empty, singleton, first, last, repeated values, maximum length, self-operation, aliased inputs, and intentionally corrupted cycles.

For manual-memory implementations, inject allocation and element construction failure at every point. Count constructions, destructions, allocations, and releases; run memory and undefined-behavior tools; test stale handles and allocator mismatch. Concurrency tests need controlled schedules, stress, race detection, linearizability/model checking where feasible, and reclamation-specific evidence. Tests passing do not prove absence of all schedules or memory-model errors.

Performance evaluation compares end-to-end operations, not link assignments in isolation. Report build strategy, traversal, random access, search, append with/without tail, removal with/without predecessor, splice, sort, memory footprint, allocation count, cache/translation events where trustworthy, latency distribution, and allocator configuration. Compare against arrays, deques, chunked structures, and pools using equal semantics and workloads.

The following standard-library Python model checks a finite sequence of mutable link transitions. Python references avoid raw-memory reclamation hazards, so the evidence is deliberately limited to topology and metadata.

<!-- bijux-verify: {"id":"singly-linked-transition-trace","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"values=C,A,Z\nsize=3\nhead=C\ntail_next=None\ncycle_probe=True\ninvariant=True\nevidence=finite_link_transition_trace\n","stderr":""}} -->
```python
class Node:
    def __init__(self, value, next_node=None):
        self.value = value
        self.next = next_node


class SinglyLinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def append(self, value):
        node = Node(value)
        if self.head is None:
            self.head = node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = node
        self.size += 1

    def push_front(self, value):
        self.head = Node(value, self.head)
        self.size += 1

    def remove_first(self, value):
        sentinel = Node(None, self.head)
        predecessor = sentinel
        while predecessor.next is not None:
            if predecessor.next.value == value:
                predecessor.next = predecessor.next.next
                self.head = sentinel.next
                self.size -= 1
                return True
            predecessor = predecessor.next
        return False

    def reverse(self):
        previous = None
        current = self.head
        while current is not None:
            following = current.next
            current.next = previous
            previous = current
            current = following
        self.head = previous

    def has_cycle(self):
        slow = self.head
        fast = self.head
        while fast is not None and fast.next is not None:
            slow = slow.next
            fast = fast.next.next
            if slow is fast:
                return True
        return False

    def invariant(self):
        if self.has_cycle():
            return False
        count = 0
        current = self.head
        while current is not None:
            count += 1
            current = current.next
        return count == self.size

    def values(self):
        result = []
        current = self.head
        while current is not None:
            result.append(current.value)
            current = current.next
        return result


linked = SinglyLinkedList()
for item in ("A", "B", "C"):
    linked.append(item)
linked.push_front("Z")
assert linked.remove_first("B")
linked.reverse()

tail = linked.head
while tail.next is not None:
    tail = tail.next
tail.next = linked.head
cycle_probe = linked.has_cycle()
tail.next = None

print(f"values={','.join(linked.values())}")
print(f"size={linked.size}")
print(f"head={linked.head.value}")
print(f"tail_next={tail.next}")
print(f"cycle_probe={cycle_probe}")
print(f"invariant={linked.invariant()}")
print("evidence=finite_link_transition_trace")
```

## Definitions and Notation

| Term or symbol | Meaning |
|---|---|
| `A=<a0,...,a(n-1)>` | Abstract finite sequence. |
| node | Storage containing an element and one successor link. |
| `head` | Link to the first element node, or termination for empty. |
| `tail` | Optional stored link to the final node. |
| `next(x)` | Successor link stored in node `x`. |
| `R(head)` | Ordered nodes reachable by repeated successor traversal. |
| termination | Distinguished link/variant/index that ends traversal. |
| predecessor | Node whose successor is the node of interest. |
| sentinel | Non-element structural node used to unify boundary operations. |
| exclusive chain | Mutable representation in which independently owned lists do not share reachable nodes. |
| persistent list | Immutable versions that may safely share suffixes under a reclamation scheme. |
| cursor | Valid position object carrying a node/predecessor and an invalidation contract. |
| linearization point | Instant at which a concurrent operation takes effect in its abstract history. |
| ABA | Reuse pattern in which an atomic representation returns to an earlier bit pattern after intervening changes. |

Complexities assume unit link reads/writes unless stated. Allocation, deallocation, element callbacks, cache/translation behavior, synchronization, reclamation, and memory consumption are separate evidence dimensions.

## Mechanisms, Invariants, or Proof Structure

**Representation proof.** Establish that head reaches exactly `n` distinct live nodes and terminates; their values equal the abstract sequence; no outgoing reachable link is invalid; stored size/tail/sentinel metadata agrees; and ownership permits the topology. Acyclicity plus finite live ownership makes traversal terminate, but the size equality and abstraction order still need checking.

**Insertion proof.** Before publication, new node `q` owns a constructed element and refers to old successor `s=p.next`. Setting `p.next=q` replaces abstract edge `p->s` with `p->q->s`. Old prefix and suffix remain unchanged, q appears exactly once, and size increases. If any pre-publication step fails, q is cleaned and the old list remains; after publication, metadata must commit consistently.

**Erasure proof.** With `v=p.next` and `s=v.next`, setting `p.next=s` removes v from reachability without changing other order. Tail/size updates restore metadata. Reclamation occurs only after no permitted observer can use v. In concurrent designs, that last statement requires a memory-reclamation proof, not merely pointer rewiring.

**Reversal proof.** The processed chain at `prev` is the reverse of the original prefix; the unprocessed chain at `cur` is the original suffix; the two are disjoint and cover all original nodes. Saving following before rewiring preserves the suffix. Each iteration reduces unprocessed count by one. Termination yields the reverse and preserves node identity/set.

**Cost proof.** Access by index `i`, predecessor discovery, and search traverse up to `Theta(n)` nodes. Given a valid predecessor, one-node insert/erase rewires `O(1)` links, excluding allocation/destruction. Append is `Theta(n)` without tail and `O(1)` link work with tail. Building by repeated untailored append has arithmetic-series `Theta(n^2)` traversals. Full traversal and reversal are `Theta(n)`.

**Evidence boundary.** These proofs cover abstract topology under their premises. They do not prove raw-pointer provenance, allocator correctness, exception behavior, cache speed, stack bounds, thread safety, reclamation, persistence, security, or deployment fitness without corresponding mechanisms and evidence.

## Alternatives and Trade-Offs

- **Null termination:** minimal structural storage; boundary branches and absence checks remain in operations.
- **Head sentinel:** uniform predecessor operations and empty/front handling; one structural node must be excluded from abstraction and lifecycle counts.
- **Stored tail:** constant link work for append and concatenation; extra metadata invariant and no help for pop-back.
- **Stored size:** constant-time size query; extra update path and possible overflow/inconsistency. Omitting it keeps minimal representation.
- **Exclusive mutable nodes:** simple mutation and reclamation ownership; suffix sharing is forbidden.
- **Immutable structural sharing:** constant-time prepend and version tails; interior updates path-copy and retention/reclamation become important.
- **Raw pointers:** precise layout/control; provenance, lifetime, failure, and reclamation burdens are explicit.
- **Managed references/smart pointers:** automate parts of lifetime; cycles, alias semantics, callback effects, and concurrency still need contracts.
- **Index-linked pool:** compact handles, generations, serialization, and locality opportunities; pool allocation and handle translation replace general allocation.
- **Array/dynamic array:** compact traversal and random access; middle edits move elements and growth can invalidate addresses.
- **Deque/chunked sequence:** stronger endpoint or locality performance; more complex indexing and block policy.
- **Doubly linked list:** constant predecessor access from a node and bidirectional traversal; another link and more rewiring invariants.
- **Coarse lock:** straightforward synchronization; traversal and allocator latency extend critical sections.
- **Fine-grained/lock-free/RCU design:** more concurrency under specific workloads; far greater ordering, retry, reclamation, and proof complexity.

## Failure Modes and Misconceptions

1. **“Insertion anywhere is O(1).”** Finding the predecessor can be linear.
2. **“A node pointer is enough to erase it.”** Ordinary erasure needs the predecessor or a different identity contract.
3. **“Append is naturally constant time.”** Only a correct tail field or equivalent cursor supplies that.
4. **“Repeated append is linear construction.”** Without a tail it is quadratic traversal work.
5. **“Set predecessor.next first, then recover the suffix.”** The old link has already been lost.
6. **“Free victim, then read victim.next.”** That is use-after-reclamation in manual memory.
7. **“One lost node is only a small leak.”** Losing a head or link can lose an entire reachable suffix.
8. **“All sharing is corruption.”** Immutable persistent suffix sharing is intentional; mutable exclusive sharing is the incompatible case.
9. **“Garbage collection proves correctness.”** It prevents some leaks/use-after-free, not stale metadata, alias corruption, races, or wrong order.
10. **“Stable addresses mean stable positions.”** Earlier edits change sequence position; erased nodes are invalid.
11. **“A sentinel is a normal element with a magic value.”** It is structural and should not consume a value-domain sentinel.
12. **“Recursion is harmless because the list is finite.”** Adversarial finite length can exceed call-stack bounds.
13. **“Floyd validates a concurrently changing list.”** Its proof assumes a stable successor relation.
14. **“Big-O link counts predict elapsed time.”** Allocation and layout often dominate and must be measured.
15. **“Linked lists always lose to arrays.”** Workload, element movement, stable identity, splice, allocator, and layout can change the decision.
16. **“Atomic next makes deletion lock-free and safe.”** Linearization, ABA, memory ordering, and reclamation remain.

## Worked Examples

### Example 1

For `head -> A -> B -> null`, prepend `X` by constructing `X.next=head` and then setting head to X. The result traverses `X,A,B`, and no old link changes. Conclusion: construct-before-publish provides a simple strong prepend path when allocation/construction failure occurs first.

### Example 2

To insert `X` after A in `A -> B -> C`, first store `X.next=B`, then set `A.next=X`. Reversing those assignments sets `A.next=X` before B is saved, losing access to `B -> C`. Conclusion: transition order follows the need to retain the old suffix.

### Example 3

Erasing B with predecessor A saves C, redirects `A.next=C`, then retires B. Erasing the only node additionally clears head and tail; erasing after tail has no victim. Conclusion: the constant rewiring core does not remove boundary metadata or reclamation cases.

### Example 4

Building 10,000 nodes by append without tail traverses `0+1+...+9999=49,995,000` existing links. With a correct tail it performs constant append link work per node, excluding allocation. Conclusion: an omitted metadata field can change a construction workload from quadratic to linear.

### Example 5

During reversal of `A -> B -> C`, processing A yields `A -> null` and unprocessed `B -> C`; processing B yields `B -> A` and unprocessed C; processing C yields `C -> B -> A`. Conclusion: the processed and unprocessed partition explains both safety and termination.

### Example 6

Two mutable lists share suffix `S -> T`. Truncating `S.next` through the first list changes traversal of the second and can invalidate both stored sizes. In an immutable persistent design the same sharing is safe because neither link can be changed. Conclusion: topology alone does not classify sharing; the mutation/ownership contract does.

### Example 7

A head sentinel points to the first element. Insert-front becomes `insert_after(sentinel)` and erase-front becomes `erase_after(sentinel)`. The sentinel is never yielded, counted, compared, or serialized. Conclusion: a structural node can remove boundary branches without stealing a value-domain marker.

### Example 8

An arena stores nodes in a dense array and uses `(slot,generation)` handles for next. Reusing a freed slot increments its generation, so an old handle is rejected instead of naming a new node. Conclusion: one-way linkage need not imply general heap pointers, though pool and generation invariants replace them.

### Example 9

A benchmark compares an arena list with a separately allocated list and a dynamic array. It reports allocator calls, bytes per element, traversal latency distribution, cache events with stated tooling, and insert workloads with predecessor discovery included. Conclusion: layout claims require controlled end-to-end evidence, not a fixed nanosecond constant copied from another machine.

### Example 10

A lock-free medication queue passes a sequential linked-list test. That does not establish linearizability, memory ordering, reclamation, ABA resistance, deadline behavior, audit durability, or clinical safety. Conclusion: topology validation is only one layer of a high-stakes concurrent system claim.

## Cross-Program Connections

- [Programming Languages and Semantics](../../01-programming-languages-and-semantics/ROADMAP.md) owns references, identity, recursive types, effects, exceptions, and observable alias behavior.
- [Functional Programming](../../03-programming-languages-functional-programming/ROADMAP.md) develops immutable cons lists, recursion, folds, persistence, and structural sharing.
- [Systems Programming](../../05-programming-languages-systems-programming/ROADMAP.md) owns allocation, provenance, lifetime, destruction, arenas, handles, and unsafe link manipulation.
- [Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) owns atomics, linearizability, ABA, locking, hazard/epoch reclamation, and RCU reasoning.
- [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) develops cycle detection, merge sort, workload bounds, adversarial analysis, and evidence design.
- [Operating Systems](../../22-operating-systems/ROADMAP.md) connects kernel lists, allocators, caches, virtual memory, RCU, and free-list applications.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) owns corrupted links, stale handles, untrusted length, exhaustion, memory safety, and denial-of-service threat models.

## References

1. ISO C++ working draft, [`forward_list` Overview](https://eel.is/c%2B%2Bdraft/forward.list.overview). One-way container purpose, forward iteration, omitted size, predecessor rationale, and public surface.
2. ISO C++ working draft, [`forward_list` Modifiers](https://eel.is/c%2B%2Bdraft/forward.list.modifiers). Insert/erase effects, preconditions, exception guarantees, complexity, and iterator/reference invalidation.
3. ISO C++ working draft, [`forward_list` Operations](https://eel.is/c%2B%2Bdraft/forward.list.ops). Splice, remove, unique, merge, sort, reverse, allocator, identity, and complexity contracts.
4. Rust Project, [The Rust Reference: Recursive Types](https://doc.rust-lang.org/stable/reference/types.html#recursive-types). Finite-size restriction and pointer indirection for recursive nominal types.
5. Rust Project, [The Rust Programming Language: Using `Box<T>` to Point to Data on the Heap](https://doc.rust-lang.org/book/ch15-01-box.html). Recursive cons-list representation, indirection, ownership, and heap allocation.
6. Rust Project, [`Box<T>` library documentation and source](https://doc.rust-lang.org/src/alloc/boxed.rs.html). Current owned allocation semantics, recursive structure example, raw conversion, allocator, and safety contracts.
7. Linux Kernel project, [Linked Lists in Linux](https://docs.kernel.org/core-api/list.html). Production intrusive list and hlist interfaces, traversal, deletion, movement, splicing, concurrency caveats, and list integrity.
8. Linux Kernel project, [Using RCU to Protect Read-Mostly Linked Lists](https://docs.kernel.org/RCU/listRCU.html). Reader/updater coordination, deletion, ordering, grace periods, and read-mostly list patterns.
9. Clang project, [AddressSanitizer](https://clang.llvm.org/docs/AddressSanitizer.html). Official instrumentation for detecting use-after-free, bounds errors, and related memory defects within its documented limits.
10. Oracle, [Java SE 25 `ConcurrentLinkedQueue`](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/concurrent/ConcurrentLinkedQueue.html). Current production-library contract for a thread-safe linked queue, weakly consistent iteration, happens-before effects, size cost, and null policy.

## Exercises

### Exercise 1

Specify a mutable singly linked list with head, optional tail, and stored size. Include abstraction, acyclicity, ownership, empty/singleton, and observer invariants.

### Exercise 2

Prove insert-after, erase-after, and in-place reversal. State preconditions, transition order, failure points, loop invariant, and metadata updates.

### Exercise 3

Diagnose an implementation that builds by repeated untailored append, recursively clears, permits shared mutable suffixes, and erases a node before reading its successor. Give durable corrections and tests.

### Exercise 4

Design and compare a null-terminated exclusive list, a sentinel-and-tail list, an immutable persistent list, and an index-linked arena for an event-history service.

### Exercise 5

Prepare an evidence plan for replacing a mutex-protected linked work queue with a lock-free implementation in a safety-sensitive service.

## Answers to the Exercises

### Answer 1

State `(head,tail,n)` with nodes `(value,next)`. From head, traversal reaches exactly `n` distinct live nodes then termination; their values equal the abstract sequence; every next is termination or a valid owned successor; independently mutable lists share no reachable node. `n=0` iff both head and tail terminate. For `n>0`, head and tail are live, tail is the final reachable node, and `tail.next` terminates. Size arithmetic is representable. Element/node ownership and allocator match destruction. Iterators/references are valid only under the documented operation table; erased/destroyed nodes are invalid. A managed-reference version still retains exclusive-mutation semantics unless sharing is explicitly part of the abstraction.

### Answer 2

Insert-after requires a valid predecessor in this list. Fully construct `q`, set `q.next=p.next`, publish `p.next=q`, then update tail if p was last and increment size; construction failure before publication leaves the list. Erase-after requires live `v=p.next`; save `s=v.next`, set `p.next=s`, update tail and size, then retire/reclaim v after observer rules permit. For reversal, invariant: `prev` reaches the reverse of the processed original prefix, `cur` reaches the untouched suffix, sets are disjoint and cover all original nodes. Save following, redirect current, advance both; unprocessed count decreases. At termination set head=prev, old head becomes terminating tail, and size is unchanged.

### Answer 3

Repeated head-scanning append performs `Theta(n^2)` traversals; add a correctly maintained tail, construct by prepend plus one reverse, or use a builder cursor. Recursive clear can exhaust stack; detach and release iteratively, ensuring smart-pointer destruction does not recursively retain the chain. Shared mutable suffixes violate exclusive ownership; use unique ownership/copying or make nodes immutable with explicit persistent semantics and reclamation. Reading successor after release is use-after-free; save it and unlink before reclamation. Tests cover empty/singleton/end paths, large chains under constrained stack, construction/allocation failures, identity disjointness, cycle injection, stale tail/size, construction/destruction counts, sanitizers, and model equality after every generated operation.

### Answer 4

Null/exclusive minimizes structure and suits single-owner mutable histories but repeats front boundary logic and cannot safely share versions. Sentinel+tail makes uniform insert/erase-after and constant link append/concatenation, at the cost of metadata invariants and no constant pop-back. Immutable persistent lists give constant prepend, cheap snapshots, and safe suffix sharing; chronological traversal may need reverse/materialization and long-lived versions retain suffixes. An index arena can compact metadata, serialize handles, use generations, and improve locality; it adds pool sizing, reuse, translation, and reclamation policy. Select by append/prepend direction, chronological reads, version retention, random access, deletion, concurrency, persistence, memory budget, and measured layout—not “linked list” as one undifferentiated option.

### Answer 5

First specify queue semantics, linearization points, progress guarantee, cancellation, capacity/exhaustion, ordering, duplicate/loss behavior, shutdown, and latency. Choose an algorithm and exact memory model; prove publication, retry, ABA defense, and safe reclamation for all reader/updater schedules. Retain the mutex implementation as an executable reference model. Run deterministic schedule exploration where possible, state-machine/linearizability tests, stress, race and memory tools, allocator-failure tests, wrap/reuse tests, and prolonged reclamation/idle-thread cases. Benchmark equal workloads with contention levels, tail latency, CPU, allocation, memory retention, and overload on target systems. Require named concurrency, language/runtime, reliability, security, safety, domain, operations, and independent reviews. Sequential topology tests and throughput wins are insufficient to authorize a safety-sensitive replacement.
