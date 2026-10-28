---
module_id: DSE-015
program: Data Structures Engineering
level: 1
module_number: 15
title: Doubly and Intrusive Linked Lists
status: complete
last_verified: 2026-08-29
---

# Doubly and Intrusive Linked Lists

## One-Page Review

### Governing question

How do predecessor links and embedded hooks enable constant-link-time removal, movement, and bidirectional traversal, and what reciprocal-link, membership, ownership, lifetime, and concurrency obligations make those capabilities safe?

### Essential definitions

- A **doubly linked list** stores both `next` and `prev` navigation links for each node.
- A **reciprocal-link invariant** requires every adjacent pair to agree: if `x.next=y`, then `y.prev=x`, and symmetrically.
- A **circular sentinel** is a non-element node whose links reach the first and last nodes, or itself when empty. It eliminates null boundary links from internal rewiring.
- An **owning list** allocates/constructs and ultimately destroys/releases its element nodes.
- An **intrusive list** uses a hook embedded in or otherwise supplied by externally owned objects; unlinking does not normally destroy the object.
- A **hook** is linkage state—typically next/previous links plus optional diagnostic membership state—associated with one object.
- **Membership** states whether a particular hook is linked in a particular container. One hook cannot simultaneously occupy two list positions.
- **Splicing** transfers one node or a range by redirecting boundary links, often without moving element payloads.
- **Auto-unlink** lets hook/object destruction detach a linked node. It changes the container indirectly and complicates size and synchronization guarantees.
- **Stable identity** means nodes are not relocated by ordinary link operations; it does not preserve logical position or permit access after unlink/reclamation.

### Central model, mechanism, or theorem

For a circular sentinel `s`, empty means `s.next=s.prev=s`. Otherwise forward traversal from `s.next` returns the abstract sequence and backward traversal from `s.prev` returns its reverse. For every reachable node including `s`:

$$
x.next.prev=x \quad\text{and}\quad x.prev.next=x.
$$

To insert detached node `x` before linked position `p`, let `a=p.prev`, then set `x.prev=a`, `x.next=p`, `a.next=x`, and `p.prev=x` before committing membership metadata. To unlink linked `x`, let `a=x.prev`, `b=x.next`, set `a.next=b` and `b.prev=a`, then place `x` in the documented detached state. Given valid nodes and no failure during link writes, both operations use a constant number of links. Finding positions, allocating owning nodes, updating size, synchronization, and reclamation are separate costs.

### Critical invariants

1. Sentinel links are valid and reciprocal; empty state is sentinel self-linking.
2. Forward traversal visits exactly the declared element nodes once and returns to sentinel; backward traversal visits the same identities in reverse.
3. Every linked hook belongs to exactly its declared container and occupies one position.
4. Detached hooks have a defined state and are not followed by any container.
5. Owning-list node lifetime and intrusive-object lifetime follow different release contracts.
6. Stored size equals reachable element count, including after transfer and any indirect unlink path.
7. Each operation restores both directions, head/tail sentinel boundaries, membership, and size atomically at the abstraction level.
8. Iterators, callbacks, destructors, concurrent readers, and reclaimers obey explicit validity and synchronization rules.

### Common failures

- Updating only the forward chain and leaving stale `prev` links.
- Inserting a hook that is already linked, corrupting one or two containers.
- Destroying an intrusive object while its normal hook remains linked.
- Treating unlink as object destruction, or destruction as automatically unlinking, without that exact contract.
- Copying/moving an object's raw hook bits and duplicating membership.
- Splicing an overlapping range into itself without defined boundary handling.
- Forgetting size changes for cross-container transfer or auto-unlink.
- Calling pointer rewiring `O(1)` while hiding position/range validation, allocation, or size computation.
- Assuming stable addresses preserve order, ownership, or erased-node validity.
- Allowing callbacks/destructors to reenter a half-mutated container.
- Using unsynchronized links in readers while writers mutate or reclaim nodes.
- Choosing a linked list from asymptotic tables without measuring layout and workload.

### Compact example

Three externally owned tasks A, B, and C are linked into `todo`. Moving C before A rewires within that list; transferring B into `done` rewires two lists without copying task payloads. Forward `todo` order is `C,A`, reverse order is `A,C`, and `done` contains B. A membership check rejects inserting A again. This finite trace validates topology and owner tags, not raw-pointer lifetime or concurrent safety.

### Connections

[DSE-014](014-singly-linked-lists.md) supplies reachability, ownership, cycle, allocation, and iterator foundations. [DSE-002](002-representation-invariants.md), [DSE-003](003-operation-contracts.md), [DSE-005](005-contiguous-and-linked-layouts.md), and [DSE-006](006-memory-locality-and-cache-behavior.md) supply proof and layout tools. The [program roadmap](../ROADMAP.md) next specializes linear structures into stacks, queues, deques, and ring buffers.

## Governing Question

What representation and transition discipline let reciprocal links and intrusive hooks support bidirectional traversal, direct-node erasure, and splicing while preserving membership, ownership, lifetime, iterator, and concurrency contracts?

## Why This Matters

Adding one predecessor link changes what a list can do from a known node. Erasure no longer requires discovering the predecessor. Iteration can move in both directions. A range can be detached and inserted elsewhere by changing boundary links rather than moving each payload. Schedulers, caches, kernels, allocators, UI systems, and graph algorithms exploit these properties.

Intrusive linkage goes further: the application object itself carries the hook, so a container need not allocate a wrapper node or map from node back to object through another ownership layer. That can reduce allocations, preserve identity, and let one object participate in several indexes through distinct hooks. The price is coupling and lifetime discipline. The container may not own the object it can reach.

The main difficulty is not drawing four assignments. It is making every observer see a coherent bidirectional topology, rejecting duplicate membership, handling self-splice, defining object moves and destruction, maintaining size, and preventing readers from touching reclaimed objects. A durable chapter therefore treats ordinary owning and intrusive lists as related mechanisms with different contracts.

## Prerequisites and Retrieval

Before this module, retrieve:

- abstraction, representation predicates, and transition proof structure from [DSE-001](001-abstract-data-types-and-concrete-representations.md) and [DSE-002](002-representation-invariants.md);
- preconditions, strong/basic guarantees, ownership, aliases, callbacks, and invalidation from [DSE-003](003-operation-contracts.md);
- link-work versus allocation/layout/latency costs from [DSE-004](004-time-space-and-allocation-cost.md), [DSE-005](005-contiguous-and-linked-layouts.md), and [DSE-006](006-memory-locality-and-cache-behavior.md);
- generic lifetime, move, and type constraints from [DSE-007](007-genericity-and-type-constraints.md);
- iterator, model-testing, and benchmark evidence from [DSE-008](008-iterators-and-traversal-protocols.md) through [DSE-010](010-benchmarking-a-structure-without-misleading-results.md);
- singly linked reachability, predecessor cost, sentinels, sharing, cycle detection, and reclamation from [DSE-014](014-singly-linked-lists.md).

## Learning Objectives

After completing this module, you should be able to:

1. specify null-terminated and circular-sentinel doubly linked representations;
2. prove reciprocal-link, traversal, membership, size, and sentinel invariants;
3. derive insert, unlink, move, and range-splice boundary transitions;
4. distinguish owning nodes from intrusive hooks and external object lifetime;
5. design detached, normal-link, safe-link, and auto-unlink policies;
6. define copying, moving, destruction, membership, multi-hook, and reentrancy behavior;
7. analyze iterator/reference stability and logical membership after transfer;
8. test bidirectional topology, overlapping self-splice, failures, corrupted hooks, and object lifecycle;
9. evaluate memory/layout, stable-identity, allocation, splice, and traversal trade-offs against alternatives;
10. identify concurrency and high-stakes claims requiring algorithms and evidence beyond reciprocal links.

## Core Exposition

**Choose the boundary representation.** A null-terminated doubly linked list stores head and tail, and each element node stores previous and next links that can be null at the ends. A circular-sentinel representation stores one structural node `s`; first is `s.next`, last is `s.prev`, and every chain returns to `s`. Empty is `s.next=s.prev=s`.

The sentinel makes every insertion “between two linked nodes” and every erasure “join predecessor to successor.” It also supplies a stable past-the-end boundary in many implementations. It must never appear as an abstract element. Value operations cannot rely on a magic sentinel payload, because every payload value may be valid.

Some implementations embed only link fields in a sentinel-like base to avoid constructing an element value. Others use separate head/tail metadata. The public contract should not expose a layout assumption unless required. A self-linked detached hook and a self-linked empty sentinel can have similar bits but different roles and ownership.

**State the bidirectional invariant in both directions.** Forward reachability alone cannot detect a stale backward link. Require that for every linked node, following next then prev returns to the node, and following prev then next does likewise. Traversing forward from sentinel visits each element identity once, in abstract order, then sentinel. Backward traversal visits exactly the same identities once in reverse order.

With stored size `n`, both element traversal counts equal `n`. A stored container membership tag, owner pointer, or safe-link state must agree with topology. For an ordinary owning list, each reachable node is owned by the container. For an intrusive list, reachability establishes membership, not object ownership; the external owner must keep the object alive and at a stable address as required by the hook.

**Insertion is a four-edge local transformation.** To insert detached `x` before linked `p`, let `a=p.prev`. The old adjacency is `a <-> p`; the new adjacency is `a <-> x <-> p`. Assign `x.prev=a`, `x.next=p`, `a.next=x`, and `p.prev=x`. Then commit owner/membership and size metadata according to the operation's observation and failure model.

In single-threaded code with non-throwing link assignments, ordering primarily prevents temporary loss and supports debugging. Callbacks, exceptions, signals, concurrent observers, or reentrant destructors can observe intermediate state unless excluded or synchronized. A robust interface validates that `p` belongs to the destination and `x` is detached before changing links. In normal-link intrusive modes those checks may be unavailable, transferring the obligation to callers.

An owning container must construct the node and value before publishing it. If construction fails, old topology is unchanged. An intrusive insert ordinarily allocates nothing; the object's lifetime already began. It can still fail on precondition checks, size overflow, policy callbacks, or synchronization according to its API.

**Unlink joins neighbors before releasing anything.** For linked element `x`, save `a=x.prev` and `b=x.next`; replace `a <-> x <-> b` with `a <-> b` using `a.next=b` and `b.prev=a`. Decrement the correct container size and put x's hook into its documented detached state—often self-linked or null links—before permitting reuse.

An owning erase then destroys/releases the node, subject to iterator and callback rules. An intrusive erase only unlinks; the external owner decides when to destroy the object. Confusing these contracts causes either leaks (expecting erase to destroy) or dangling hooks (destroying while still linked).

If destructors can execute application code, first restore a coherent list and retain whatever local ownership is needed, then invoke destruction outside the vulnerable mutation state when feasible. Reentrancy policy should say whether callbacks may query or modify this container. “No callbacks during rewiring” is useful only if element destruction, comparison, allocation, and instrumentation actually obey it.

**Known-node erasure is constant link work.** A valid iterator or hook for x directly supplies both neighbors, so no predecessor scan is needed. But validation that x belongs to this container can be linear without a stored owner/tag or safe-link mechanism. Finding x by index or value remains linear. Deallocation and element destruction are separate. Complexity documentation must specify which inputs and checks are assumed.

Stable node addresses allow iterators/references to unaffected elements to remain valid across ordinary insertion in many list contracts. Erasing x invalidates x's observers. Transferring x between containers may preserve the node and reference while changing membership. ISO C++ `list` specifies exact behaviors and allocator preconditions; a custom or intrusive list must define its own.

**Range splice is boundary algebra.** Suppose an inclusive node range from `first` through `last` lies between `before` and `after`. Detach by connecting `before <-> after`. Insert before destination `p`, whose predecessor is `d`, by connecting `d <-> first`, `last <-> p`. Six boundary relationships describe the conceptual operation; internal range links remain unchanged.

Cross-container splice must update source and destination size. If range length is not known and size is stored, counting can make the operation linear even though rewiring is constant. Allocator/resource compatibility can determine whether an owning container may transfer nodes without reconstruction. Intrusive objects remain externally owned, but hook type and list policy must still match.

Self-splice requires special cases. If destination lies within the moved range, a naive detach-and-insert can corrupt topology; an API may define no effect, forbid the case, or handle it. Moving a node immediately before itself or its current successor should be a no-op under a reasonable contract. Range endpoints and whether the range is half-open or closed must be exact.

**Intrusive means linkage is part of the object contract.** A task object can embed `ready_hook`; a cache entry can embed `lru_hook`; a timer can embed `timer_hook`. Distinct hooks let one object occupy several containers simultaneously. Reusing one hook for two memberships is invalid because it contains only one predecessor/successor pair.

Base hooks couple through inheritance; member hooks make the role explicit in a field. Custom value traits can map between hook and object. C-style `container_of` techniques derive an enclosing object from member offset, which requires exact layout/provenance rules. Higher-level libraries can keep typed mapping. Do not reproduce a kernel macro in another language or ABI without proving its premises.

The intrusive container generally stores no owning reference beyond raw reachability. The object must not move in memory while linked unless links and every observer are repaired by a supported operation. Stack objects must outlive membership. Arena compaction, copying garbage collectors, object moves, vector relocation, and FFI ownership can violate address stability.

**Hook state is an explicit safety policy.** A normal-link hook may leave old link bits on removal and perform no duplicate-insert checks. It has minimal work but the strictest caller obligation. A safe-link hook initializes a recognized detached state, verifies it on insertion, and restores it on erasure; assertions catch some double-link or destroy-linked defects. Assertions are diagnostics, not recovery or proof in builds where disabled.

An auto-unlink hook detaches when the object/hook is destroyed. This can simplify cleanup but mutates a container without a direct container call. Stored constant-time size becomes difficult because the hook may not have or safely update container metadata; Boost.Intrusive documents compatibility restrictions. Auto-unlink is also a write for thread-safety and reentrancy analysis.

Copying a hook's raw links would create a second object whose links claim the original position. Safe designs initialize the copy as detached, prohibit copying linked objects, or define a higher-level copy that copies payload but not membership. Moving a linked object by relocating its address likewise breaks neighbors unless the library provides a node replacement/move protocol. Default-generated copy/move is rarely an adequate intrusive-object contract.

**Circularity is intentional, accidental cycles are not.** A circular sentinel list never reaches null; termination is return to its unique sentinel. The cycle is structural and validated by membership/count rules. A stray subcycle that excludes the sentinel or repeats an element is corruption. Generic Floyd detection alone cannot distinguish the intended outer cycle from valid termination; the checker must know the sentinel model.

An invariant checker can walk at most `n+1` steps, require the sentinel at exactly the boundary, check reciprocity on every edge, and repeat backward. It should compare node-identity sets and owner tags. A maximum-step guard prevents corrupted metadata from hanging diagnostics. Concurrent mutation still requires synchronization for a meaningful snapshot.

**Owning and intrusive APIs should look different where semantics differ.** An owning `erase` can return an iterator to the next element and destroy the erased value. An intrusive `unlink` can return the object still alive and detached. An owning `clear` destroys all nodes; an intrusive `clear` detaches hooks and must define whether objects are otherwise untouched. An intrusive container destructor must specify whether it unlinks all members, asserts empty, or merely abandons links—libraries differ.

Naming these operations precisely prevents dangerous generic code. A policy that passes a disposer callback during intrusive erase creates a hybrid ownership boundary and must specify callback failure/reentrancy. An object may own the container that links it, creating destruction-order cycles at the semantic level even if raw pointers do not participate in reference counting.

**Layout and workload decide value.** A doubly linked owning node adds two links, padding, and allocation metadata around each value. Traversal is pointer chasing and commonly transfers more bytes than a singly linked node. Backward traversal and direct-node removal may justify that cost. Intrusive hooks can eliminate wrapper allocation and preserve a direct object identity, but still consume two links per membership and couple object layout to container roles.

Arrays usually win for compact scanning and random access; deques/chunks can support endpoint edits with better locality. Lists are candidates when stable node identity, frequent known-position insertion/removal, or splice without payload movement matters. Large payloads can be held indirectly by any structure, weakening claims that only lists avoid movement. Benchmark full semantics, including finding positions, allocation, callbacks, size, synchronization, and memory footprint.

**Concurrency requires more than reciprocal atomics.** A reader traversing `next` can race with unlink, see an inconsistent forward/backward pair, or access a reclaimed object. Locking the container provides a coherent topology if all direct hook operations share the lock. Intrusive auto-unlink and object destruction must participate in the same synchronization.

Fine-grained or lock-free doubly linked lists are substantially harder because one abstract adjacency update touches multiple locations and helpers may observe partially completed operations. Designs use marking, descriptors, helping, versioning, or restricted operations plus a reclamation scheme. RCU can support specific read-mostly patterns, but reverse links, deletion, replacement, and grace periods have exact rules. A sequential four-assignment proof cannot be relabeled concurrent.

**Verification targets lifecycle and topology.** Model tests compare forward values to a simple sequence after insert, erase, move, rotate, reverse, clear, single/range splice, and cross-container transfer. After every operation, traverse both directions, check reciprocal edges, size, sentinel boundary, node identity set, and membership. Generate empty, singleton, first/last, adjacent moves, self-splice, destination inside range, whole-list transfer, duplicate insert, foreign position, and size overflow.

For owning lists inject allocation, element construction, comparison, and disposer failure; count lifetimes and allocator ownership. For intrusive lists test stack/arena/object destruction order, safe-link assertions where testable, copy/move policy, multiple distinct hooks, same-hook double insertion, auto-unlink, container destruction, and reentrancy. Memory/undefined-behavior/race tools address defect classes but do not replace contract proofs.

The following Python trace models an intrusive circular-sentinel list with explicit owner tags. Python manages object memory, so it demonstrates membership and link topology only.

<!-- bijux-verify: {"id":"intrusive-list-splice-trace","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"todo_forward=C,A\ntodo_reverse=A,C\ndone=B\nowners=todo,done,todo\nduplicate_rejected=True\ninvariant=True\nevidence=finite_intrusive_splice_trace\n","stderr":""}} -->
```python
class Task:
    def __init__(self, name):
        self.name = name
        self.prev = self
        self.next = self
        self.owner = None


class IntrusiveList:
    def __init__(self, name):
        self.name = name
        self.sentinel = Task("<sentinel>")
        self.sentinel.owner = self
        self.size = 0

    def insert_before(self, position, node):
        if position.owner is not self:
            raise ValueError("foreign position")
        if node.owner is not None:
            raise ValueError("node already linked")
        predecessor = position.prev
        node.prev = predecessor
        node.next = position
        predecessor.next = node
        position.prev = node
        node.owner = self
        self.size += 1

    def push_back(self, node):
        self.insert_before(self.sentinel, node)

    def detach(self, node):
        if node is self.sentinel or node.owner is not self:
            raise ValueError("node is not an element of this list")
        node.prev.next = node.next
        node.next.prev = node.prev
        self.size -= 1
        node.prev = node
        node.next = node
        node.owner = None

    def transfer_before(self, position, source, node):
        source.detach(node)
        self.insert_before(position, node)

    def forward(self):
        result = []
        current = self.sentinel.next
        while current is not self.sentinel:
            result.append(current.name)
            current = current.next
        return result

    def reverse(self):
        result = []
        current = self.sentinel.prev
        while current is not self.sentinel:
            result.append(current.name)
            current = current.prev
        return result

    def invariant(self):
        current = self.sentinel
        count = 0
        while True:
            if current.next.prev is not current or current.prev.next is not current:
                return False
            current = current.next
            if current is self.sentinel:
                break
            if current.owner is not self:
                return False
            count += 1
            if count > self.size:
                return False
        return count == self.size and self.reverse() == list(reversed(self.forward()))


todo = IntrusiveList("todo")
done = IntrusiveList("done")
a, b, c = Task("A"), Task("B"), Task("C")
for task in (a, b, c):
    todo.push_back(task)

todo.transfer_before(a, todo, c)
done.transfer_before(done.sentinel, todo, b)
try:
    todo.push_back(a)
    duplicate_rejected = False
except ValueError:
    duplicate_rejected = True

print(f"todo_forward={','.join(todo.forward())}")
print(f"todo_reverse={','.join(todo.reverse())}")
print(f"done={','.join(done.forward())}")
print(f"owners={a.owner.name},{b.owner.name},{c.owner.name}")
print(f"duplicate_rejected={duplicate_rejected}")
print(f"invariant={todo.invariant() and done.invariant()}")
print("evidence=finite_intrusive_splice_trace")
```

## Definitions and Notation

| Term | Meaning |
|---|---|
| owning list | Container owns node allocation, element lifetime, and release. |
| intrusive list | Container links hooks associated with externally owned objects. |
| hook | Link state for one container role. |
| `s` | Circular non-element sentinel. |
| reciprocal link | Adjacent relationship satisfying both next/prev directions. |
| linked state | Hook occupies exactly one position in a container. |
| detached state | Hook is in a documented nonmember state, often self-linked or null. |
| splice | Link-boundary transfer without ordinary payload movement. |
| base hook | Linkage supplied through inheritance. |
| member hook | Linkage supplied by an object field. |
| normal link | Minimal hook mode whose validity obligations are largely caller-owned. |
| safe link | Hook mode with recognized detached state and diagnostic checks. |
| auto-unlink | Hook mode in which destruction/unlink can mutate membership indirectly. |
| disposer | Callback/policy that releases an externally represented object after unlink. |

Complexity counts link operations only when explicitly labeled. Search, validation, range counting, allocation, destruction, callbacks, synchronization, reclamation, and cache behavior remain separate.

## Mechanisms, Invariants, or Proof Structure

**Topology proof.** Show sentinel self-links for empty or one closed reciprocal cycle through exactly `n` element hooks. For each visited node check `next.prev` and `prev.next`; forward and reverse identity sets agree; membership tags and size agree; sentinel is excluded from abstraction.

**Insert proof.** Replace adjacency `a<->p` with `a<->x<->p`. The four reciprocal equations hold after assignments, no old element changes relative order, x appears once, and size increases. Preconditions establish p is a member and x detached; owning construction completes before publication.

**Unlink proof.** Replace `a<->x<->b` with `a<->b`; restore x's detached state and remove its membership. Remaining abstract order is old sequence without x. Owning erase adds destruction after observer/reentrancy rules permit; intrusive unlink does not imply destruction.

**Splice proof.** Detach range boundaries, retain internal reciprocal edges, and insert those boundaries at destination. Prove source/destination identity sets and sizes, preserve range order, and handle same-container overlapping/no-op cases separately. Allocator/hook compatibility is a precondition.

**Cost conclusion.** Given valid positions and known range length when needed, node insert/unlink/transfer changes constant links. Search, index navigation, membership validation, and unknown-length size adjustment can be linear. Layout, allocation, and concurrency costs are not derived from link count.

## Alternatives and Trade-Offs

- **Null boundaries versus circular sentinel:** null is structurally smaller; sentinel unifies edge operations and supports closed reciprocal invariants.
- **Owning versus intrusive:** owning container centralizes lifetime/allocation; intrusive eliminates wrapper ownership and can support multiple roles but couples objects and callers.
- **Base versus member hooks:** base hooks can be concise but affect type hierarchy; member hooks name domain roles and allow several fields.
- **Normal versus safe link:** normal minimizes diagnostics; safe state catches some duplicate/destroy-linked misuse with overhead and assertion limits.
- **Explicit versus auto-unlink:** explicit unlink keeps mutations visible to container APIs; auto-unlink simplifies some lifecycle paths but complicates size, locks, and reentrancy.
- **One versus multiple hooks:** one hook minimizes object size; distinct hooks allow simultaneous memberships with independent invariants.
- **Stored size versus traversal size:** stored size gives constant queries but every direct/indirect transfer must update it.
- **List versus dynamic array:** list favors known-node removal, stable identity, and splice; array favors compact scan, indexing, and fewer allocations.
- **List versus deque/chunks:** list gives per-node linkage; blocked structures often improve locality while preserving endpoint or local edits.
- **Raw pointers versus handles/offsets:** raw pointers are direct; handles can support shared memory, generations, or relocation with translation cost.
- **Coarse lock versus advanced concurrency:** coarse locking simplifies reciprocal invariants; fine-grained/lock-free/RCU approaches require specialized algorithms and reclamation.

## Failure Modes and Misconceptions

1. **“Checking next links validates a doubly linked list.”** Backward links can still be stale or divergent.
2. **“The sentinel is an element with a special value.”** It is structural and outside the value domain.
3. **“Four assignments are atomic.”** Observers or callbacks can see intermediate state unless excluded or synchronized.
4. **“Known-node erase includes destruction.”** Only an owning erase normally does; intrusive unlink preserves the external object.
5. **“The intrusive container keeps objects alive.”** That is not implied by raw embedded hooks.
6. **“One hook can be in two lists.”** Each simultaneous membership needs distinct linkage.
7. **“Default copy/move is fine.”** Duplicated or relocated hook bits can corrupt membership.
8. **“Safe-link proves correctness.”** It catches some state misuse and may rely on assertions; it is not a complete proof.
9. **“Auto-unlink is a read-free convenience.”** It is an indirect container mutation with size and synchronization consequences.
10. **“Splice is always O(1).”** Range length, size update, validation, and allocator rules can add work.
11. **“Self-splice is just cross-splice.”** Destination overlap needs explicit handling.
12. **“Stable reference means same container and position.”** Transfer preserves identity while membership/order changes.
13. **“A circular list has a corruption cycle.”** Sentinel return is intentional; repeated element subcycles are not.
14. **“Intrusive always uses less memory.”** Object hooks, multiple memberships, padding, ownership infrastructure, and workload determine totals.
15. **“Atomic links make concurrent traversal safe.”** Coherence and reclamation still require an algorithm and memory-order proof.
16. **“Kernel or Boost patterns transfer unchanged.”** Their type, ABI, assertion, locking, and lifetime premises are environment-specific.

## Worked Examples

### Example 1

An empty sentinel has `s.next=s.prev=s`. Insert A before s: A's links both name s, while s's next and prev both name A. Forward and backward traversal each yield A once. Conclusion: the same four-edge rule covers empty and endpoint insertion.

### Example 2

For `A <-> B <-> C`, unlink B by setting `A.next=C` and `C.prev=A`, then self-link B and clear its owner tag. A stale `B.prev=A` with no detached policy could let accidental reuse corrupt the list. Conclusion: detached state is part of the hook contract.

### Example 3

Task T is in the ready list through `ready_hook` and the timeout list through `timer_hook`. The two link pairs are independent. Attempting to insert `ready_hook` into a second ready list is rejected. Conclusion: simultaneous roles require distinct hooks, not duplicated use of one hook.

### Example 4

Moving range B,C from `A,B,C,D` before Y in `X,Y,Z` joins A to D, X to B, C to Y, and updates sizes from 4/3 to 2/5. Internal B-C adjacency remains. Conclusion: range splice is boundary rewiring plus metadata, not payload movement.

### Example 5

Splicing B,C before C within the same list places the destination inside the range. A naive detach makes C's neighborhood change before insertion. The API must treat this as forbidden or no-op with validated endpoints. Conclusion: self-overlap is a semantic case, not a minor implementation detail.

### Example 6

Copying a linked object byte-for-byte produces a second hook pointing at the original neighbors, while those neighbors still point only to the original. Safe copy constructs the new object's hook detached and copies only payload. Conclusion: object value copying and membership copying must be separated.

### Example 7

Destroying an auto-unlink object removes it from its list but bypasses an ordinary container method. If size is stored and the hook cannot update it safely, size becomes stale. Conclusion: convenient indirect mutation constrains metadata and locking design.

### Example 8

An owning list and intrusive list each erase E. The owning list destroys E's node/value after unlink; the intrusive list returns E detached because another subsystem owns its lifetime. Conclusion: identical topology transitions can have opposite lifetime consequences.

### Example 9

A benchmark reports fast intrusive removal given handles but omits time to find those handles and the cost of maintaining them. A fair workload includes lookup/index maintenance, memory footprint, traversal, and lifecycle callbacks. Conclusion: constant link work is not automatically constant end-to-end service cost.

### Example 10

A kernel-style intrusive patient-work list passes forward/backward invariant tests. This does not establish lock discipline, grace periods, use-after-free resistance, deadline safety, prioritization fairness, auditability, or clinical correctness. Conclusion: container evidence cannot certify the enclosing high-stakes workflow.

## Cross-Program Connections

- [Programming Languages and Semantics](../../01-programming-languages-and-semantics/ROADMAP.md) owns object identity, layout, copying/moving, callbacks, effects, and alias contracts.
- [Systems Programming](../../05-programming-languages-systems-programming/ROADMAP.md) owns raw links, `container_of`-style recovery, alignment, provenance, allocators, arenas, destruction, and FFI.
- [Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) owns locks, atomics, linearization, memory ordering, ABA, RCU, and reclamation.
- [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) develops merge/sort/splice algorithms, cost models, adversarial cases, and benchmark design.
- [Operating Systems](../../22-operating-systems/ROADMAP.md) connects intrusive queues, scheduler/timer structures, kernel lists, RCU, and allocator metadata.
- [Software Design and Domain Modeling](../../09-software-engineering-software-design-and-domain-modeling/ROADMAP.md) connects object roles, lifecycle ownership, multiple memberships, and API boundaries.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) owns corrupted hooks, stale objects, reuse, memory safety, malicious ranges, and exhaustion threats.

## References

1. ISO C++ working draft, [`list` Overview](https://eel.is/c%2B%2Bdraft/list.overview). Bidirectional sequence semantics, iterator category, constant-time known-position insertion/erase, and lack of random access.
2. ISO C++ working draft, [`list` Modifiers](https://eel.is/c%2B%2Bdraft/list.modifiers). Insert/erase effects, exception guarantees, complexity, and iterator/reference invalidation.
3. ISO C++ working draft, [`list` Operations](https://eel.is/c%2B%2Bdraft/list.ops). Splice, remove, unique, merge, sort, reverse, allocator preconditions, identity, and complexity.
4. Linux Kernel project, [Linked Lists in Linux](https://docs.kernel.org/core-api/list.html). Production intrusive circular-list and hlist representation, container recovery, insertion, deletion, traversal, splice, and concurrency guidance.
5. Linux Kernel project, [Using RCU to Protect Read-Mostly Linked Lists](https://docs.kernel.org/RCU/listRCU.html). Reader/updater ordering, deletion, replacement, grace-period, and traversal obligations.
6. Boost Project, [How to Use Boost.Intrusive](https://www.boost.org/latest/doc/html/intrusive/usage.html). Base/member hooks, multiple tags, link modes, object lifetime, container configuration, and ownership distinctions.
7. Boost Project, [Safe Hooks](https://www.boost.org/latest/doc/html/intrusive/safe_hook.html). Detached-state initialization, duplicate-insert and destroy-linked assertions, and configuration.
8. Boost Project, [Boost.Intrusive Thread Safety Guarantees](https://www.boost.org/doc/libs/latest/doc/html/intrusive/thread_safety.html). Direct and indirect access, hook/object lifetime, multi-container membership, and synchronization boundaries.
9. Boost Project, [Presenting Boost.Intrusive Containers](https://www.boost.org/latest/doc/html/intrusive/presenting_containers.html). Owning versus intrusive differences, safe/auto-unlink hooks, pointer customization, size trade-offs, and supported containers.
10. Rust Project, [`LinkedList` Cursor](https://doc.rust-lang.org/std/collections/linked_list/struct.Cursor.html). Current nightly experimental bidirectional cursor and ghost non-element boundary model; version status is part of the citation.

## Exercises

### Exercise 1

Specify a circular-sentinel owning doubly linked list with stored size. Include forward/backward abstraction, reciprocity, empty/singleton, iterator, and lifetime invariants.

### Exercise 2

Prove insert-before, unlink, and cross-container range splice. Identify preconditions, link equations, membership, size, allocator, overlap, and failure obligations.

### Exercise 3

Design an intrusive task object that can simultaneously occupy ready, timeout, and diagnostics lists. Define hooks, copy/move, destruction, detached state, and synchronization.

### Exercise 4

Compare owning list, intrusive list, dynamic array of pointers, deque, and index-linked pool for an LRU-like service with stable handles and frequent known-node promotion.

### Exercise 5

Prepare verification and review evidence for an auto-unlink intrusive list used across threads in a high-reliability runtime.

## Answers to the Exercises

### Answer 1

State sentinel s, stored n, owning allocator, and element nodes. Empty iff `n=0` and `s.next=s.prev=s`. For every node reachable forward including s, `x.next.prev=x` and `x.prev.next=x`; forward traversal returns to s after exactly n element identities and yields the abstract sequence, while backward traversal reaches the same identities in reverse. The sentinel is never an element. For n>0, s.next and s.prev are first/last; singleton links both directions to s. Each element node is live, uniquely owned, allocator-compatible, and destroyed exactly once. Insert preserves unaffected observers under the declared contract; erase invalidates the erased node; transfer can change membership while preserving identity only where specified.

### Answer 2

Insert-before requires destination p linked here and x detached/compatible. With a=p.prev, establish `x.prev=a`, `x.next=p`, `a.next=x`, `p.prev=x`, membership, and size after owning construction succeeds. Unlink requires x linked and non-sentinel; with a=x.prev and b=x.next, establish `a.next=b`, `b.prev=a`, decrement size, clear membership, and restore detached state before optional owning destruction. Range splice detaches `before<->first...last<->after` by joining before/after, then joins destination predecessor to first and last to destination. Preserve internal range links/order; update both sizes using known/count length; require compatible allocator/hook policy; separately handle same-container destination inside/adjacent to range. No throwing callback may observe a half-mutated topology unless rollback is designed.

### Answer 3

Embed three distinct member hooks named by role. Each hook has a recognized detached state and an owner/container tag in diagnostic builds. Copy payload only and initialize every copied hook detached; either prohibit moving while any hook is linked or provide an explicit stable-address relocation protocol. Destruction requires all hooks detached, or an exact auto-unlink policy participating in all three containers' locks and size rules. External ownership outlives every membership. Ready, timeout, and diagnostics operations synchronize their own container and any object fields they share; cross-role atomic transitions acquire locks in a global order or use another proved protocol. Tests reject same-hook duplicate membership while allowing three different simultaneous memberships.

### Answer 4

An owning list centralizes node lifetime but adds wrapper allocation and pointer chasing. An intrusive list removes wrapper ownership and makes promotion from a known handle constant link work, but couples object layout/lifetime and needs one hook per role. An array of pointers gives compact pointer scanning and indexing; promotion shifts pointer ranges unless paired with another index. A deque improves endpoints but arbitrary known-position removal/promotion remains nonconstant. An index-linked pool offers stable generation handles and controllable locality without raw object hooks, but adds pool capacity/reuse/translation. Measure lookup, promotion, eviction, scans, allocations, bytes, cache behavior, handle maintenance, synchronization, and tail latency on representative sizes before choosing.

### Answer 5

Specify every direct and destructor-triggered mutation, stored-size policy, lock/atomic protocol, reentrancy, shutdown, object ownership, and reclamation. Prove reciprocal topology and linearization across insert/unlink/destruction, including lock order and the fact that auto-unlink is a write. Ensure no object can be destroyed while any reader can access its hook; use a documented grace-period/hazard/epoch/ownership mechanism. Model-test topology and lifecycle, force destructor timing, duplicate links, cross-container roles, concurrent reads/writes, cancellation, and shutdown; run race, memory, undefined-behavior, schedule, stress, and long-duration reclamation tests. Measure contention and tails under target load. Require named runtime, concurrency, security, reliability, safety, operations, and independent review. Safe-link assertions and finite stress do not prove all schedules or high-reliability fitness.
