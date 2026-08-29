---
module_id: DSE-016
program: Data Structures Engineering
level: 1
module_number: 16
title: Stacks
status: complete
last_verified: 2026-08-29
---

# Stacks

## One-Page Review

### Governing question

How can a last-in-first-out abstraction expose the smallest useful contract while making empty/full behavior, representation costs, retention, iteration, rollback, and concurrency explicit?

### Essential definitions

- A **stack** is a finite sequence whose designated accessible end is the **top**.
- **Push** appends one element at the top; **pop** removes and returns the top; **peek/top** observes it without removal.
- **LIFO** means that among elements not already removed, the most recently pushed element is the next popped element.
- **Underflow** is an attempted pop/peek on an empty stack. The API may signal it with an option, result, exception, sentinel, or precondition.
- **Overflow/full** is a push that cannot be accepted under a bounded capacity or resource policy. “Dynamically growing” is not the same as unbounded.
- A **bounded stack** has a declared maximum element/byte capacity and a defined full policy.
- A **checkpoint** records an abstract depth or version for later rollback; it is valid only under an ownership and mutation contract.
- A **container adaptor** restricts an underlying sequence to stack operations rather than defining one mandatory representation.
- A **call stack**, **operand stack**, **shadow stack**, and application Stack ADT are related LIFO mechanisms but have different elements, limits, and contracts.
- A **linearization point** is the instant a concurrent push or pop takes effect in the abstract history.

### Central model, mechanism, or theorem

Represent the abstract stack from bottom to top as

\[
S=\langle s_0,\ldots,s_{n-1}\rangle.
\]

Then `push(x)` maps `S` to `S·<x>`, `pop()` for `n>0` returns `s_(n-1)` and leaves `<s_0,...,s_(n-2)>`, and `peek()` returns `s_(n-1)` without changing `S`. For any successful pushes `x_1,...,x_k` with no intervening removal of them, subsequent successful pops return `x_k,...,x_1`. This follows immediately by induction on `k` from the append/remove-last transitions.

An array representation stores live elements in `[0,n)` with top at `n-1`; a singly linked representation stores top at head. Each can perform core link/index work in constant time given capacity/allocation assumptions. Dynamic-array push is amortized rather than worst-case constant when growth is possible; linked push may allocate; bounded array push can reject without allocation.

### Critical invariants

1. The representation encodes exactly the abstract bottom-to-top sequence.
2. Empty is exactly depth zero; no operation reads a nonexistent top.
3. Array form satisfies `0<=n<=capacity`, live `[0,n)`, and non-live `[n,capacity)`.
4. Linked form satisfies acyclic reachability of exactly `n` nodes from top/head.
5. Successful push publishes the new top only after element construction; failed push has its documented effect.
6. Successful pop removes exactly one live top and applies the stated ownership/destruction/return order.
7. Size, byte, capacity, checkpoint, iterator, and maximum-depth arithmetic is checked.
8. Concurrent operations and memory reclamation follow a specific algorithm; ordinary stack invariants alone do not imply thread safety.

### Common failures

- Confusing which end is top across push, pop, iteration, and serialization.
- Returning a magic sentinel that can also be a valid element.
- Calling growth-backed push worst-case `O(1)` or calling heap-backed capacity unlimited.
- Removing/destroying the top before safely producing the returned value.
- Retaining popped references in spare storage and unintentionally extending lifetime or secrets.
- Exposing an underlying mutable container that can violate the restricted interface.
- Treating a saved numeric depth as a valid rollback token after unrelated mutation or concurrency.
- Using recursive algorithms on adversarial depth without a runtime stack limit strategy.
- Assuming reverse acquisition is always a valid cleanup order when dependencies are not properly nested.
- Sharing a mutable stack without synchronization, or treating atomic top as sufficient reclamation.

### Compact example

A capacity-four stack pushes `alpha`, `beta`, records depth two, pushes `gamma` and `delta`, and rejects `epsilon`. After a pop/push variation, rollback to depth two removes later values. Popping `beta` and pushing `omega` leaves bottom-to-top `alpha,omega`. The trace verifies finite capacity, underflow/full results, live extent, rollback, and top; it does not prove arbitrary element lifetime or concurrency.

### Connections

[DSE-012](012-dynamic-arrays-and-geometric-growth.md) supplies growth and invalidation; [DSE-014](014-singly-linked-lists.md) supplies head-based ownership; [DSE-003](003-operation-contracts.md) supplies failure semantics; [DSE-004](004-time-space-and-allocation-cost.md) supplies amortized and bounded-resource analysis. The [program roadmap](../ROADMAP.md) next contrasts queues, deques, and ring buffers.

## Governing Question

What abstract law, representation invariant, failure policy, resource bound, and observer contract let a stack support dependable LIFO behavior—and when are recursion, cleanup, rollback, or concurrent use only superficially stack-shaped?

## Why This Matters

Stacks appear wherever work is suspended and resumed in reverse nesting order: expression evaluation, parsing, depth-first traversal, undo, backtracking, continuations, resource scopes, and virtual machines. The tiny API makes a stack an excellent abstraction boundary. Clients need not know whether elements occupy an array, linked chain, segmented buffer, persistent list, or specialized concurrent structure.

That minimalism can conceal operational differences. An array-backed push may allocate and relocate. A linked push may fail allocation every time. A bounded embedded stack must reject or fail deterministically when full. A call stack can exhaust even if an application stack could grow. An “undo stack” needs command validity, retained resources, and transaction semantics beyond LIFO order.

The governing principle is therefore to prove LIFO behavior at the ADT layer and then state representation, resource, failure, lifetime, and concurrency properties separately. A stack should restrict capability deliberately; exposing arbitrary middle mutation undermines the reasoning that makes it useful.

## Prerequisites and Retrieval

Before this module, retrieve:

- abstraction functions and representation invariants from [DSE-001](001-abstract-data-types-and-concrete-representations.md) and [DSE-002](002-representation-invariants.md);
- operation preconditions, failure guarantees, ownership, and observability from [DSE-003](003-operation-contracts.md);
- worst-case, amortized, allocation, byte, and tail-latency cost from [DSE-004](004-time-space-and-allocation-cost.md);
- generic construction/destruction and iterator contracts from [DSE-007](007-genericity-and-type-constraints.md) and [DSE-008](008-iterators-and-traversal-protocols.md);
- property/model tests and evidence discipline from [DSE-009](009-property-based-testing-of-data-structures.md) and [DSE-010](010-benchmarking-a-structure-without-misleading-results.md);
- dynamic-array and linked representations from [DSE-012](012-dynamic-arrays-and-geometric-growth.md), [DSE-014](014-singly-linked-lists.md), and [DSE-015](015-doubly-and-intrusive-linked-lists.md).

## Learning Objectives

After completing this module, you should be able to:

1. specify stack values and push, pop, peek, empty, and size transitions;
2. prove the LIFO theorem over an arbitrary successful push sequence;
3. distinguish underflow preconditions, options/results, exceptions, and sentinel failures;
4. implement array-backed, linked, bounded, and persistent stacks with exact invariants;
5. separate worst-case link/index work from allocation, growth, destruction, and retained-memory costs;
6. define iterator, exposure, checkpoint, rollback, clear, and serialization behavior;
7. distinguish an application stack from runtime call/operand/shadow stacks;
8. identify when reverse-order cleanup is valid and when a dependency graph is needed;
9. design state-machine, fault, boundary, memory, and performance evidence;
10. state the additional linearizability, memory-ordering, ABA, and reclamation work for concurrent stacks.

## Core Exposition

**Keep the ADT smaller than its representation.** A dynamic array supports indexing, insertion, erasure, reserve, and iteration, but a stack adaptor can expose only top-end operations. That restriction prevents clients from bypassing LIFO order and lets the implementation change. ISO C++ specifies `stack` as an adaptor over any compatible sequence supporting `back`, `push_back`, and `pop_back`; the default underlying choice is policy, not the abstract definition.

The abstract sequence is written bottom to top so append corresponds to push. Another document can write top first, but must remain consistent. Iteration order is not inherent to the minimal ADT. If iteration is offered, define whether it yields bottom-to-top or pop order, whether mutation is allowed, and what invalidates it.

**Specify empty behavior without stealing a value.** Pop and peek are partial mathematical operations because no top exists at depth zero. APIs make them total by returning an option/result, throwing, reporting a boolean plus output parameter, or defining a precondition whose violation is an error. A sentinel such as `-1` or null is ambiguous when it belongs to the element domain.

Rust `Vec::pop` returns `Option<T>`. Java deque interfaces offer paired forms: operations that throw and operations that return a special value, with null restrictions mattering to ambiguity. C++ `stack::top`/`pop` rely on underlying-container preconditions and `pop` does not return the element. These ecosystem differences must not be blended into a fictional universal API.

Returning by value can itself move/copy and fail in some language models. A safe owning implementation may first establish the return value, then shorten the stack, or provide a weaker documented guarantee. A reference from `peek` borrows the top and is invalidated when that element is popped or storage relocates. Holding it while mutating may be forbidden by a borrow system or dangerous through raw aliases.

**Array representation makes the live extent explicit.** State `(B,n,c)` has `0<=n<=c`; live elements occupy `[0,n)` and top is `B[n-1]` when nonempty. Push constructs at `B[n]`, then increments n. Pop obtains the element at `n-1`, decrements the committed live extent at the correct point, and destroys/clears the removed slot according to ownership and failure rules.

Fixed capacity makes full behavior predictable: reject, return false/full, throw, overwrite by a different abstraction, or terminate under a strict precondition. Overwriting the bottom is no longer an ordinary stack because it silently changes more than the top-end transition; if desired, name it a bounded dropping history and specify that policy.

A dynamic array can grow geometrically. Successful push has amortized constant element work, but a growth push can copy/move every element, allocate, invalidate observers, and create a latency/memory spike. Pre-reserving can remove some growth events but may retain memory or fail early. Hard real-time or memory-budget claims require a bounded allocation strategy and worst-case evidence, not amortized notation.

**Linked representation places top at head.** Push allocates/constructs `Node(x,old_head)` and publishes it as head. Pop saves head's value/successor, advances head, and retires the node. Core link work is constant; allocator and reclamation work remain. Each node adds link/padding/allocation overhead and traversal loses contiguity, although the stack rarely needs full traversal in its minimal API.

A linked stack has no fixed element capacity unless policy imposes one, but it is always bounded by representable size, allocator resources, process limits, and admission rules. “No capacity field” does not mean unbounded. A pool-backed linked stack can bound nodes and make exhaustion explicit while retaining stable nodes.

**Persistent stacks make sharing safe through immutability.** An immutable stack is empty or a node `(value,tail)`. Push returns a new node whose tail is the old stack; pop returns the top and old tail. Old and new versions share suffix nodes safely because none mutate. Reclamation and version retention decide actual memory use.

Persistent checkpoints can simply retain a version handle. Mutable checkpoints often store a depth, but rollback is only valid if all changes since the mark were pushes/pops in a compatible ownership scope and no external observer relies on removed elements. Generation/version tags can reject stale marks. Rollback must destroy or release discarded elements and define whether it can fail.

**LIFO follows from transitions, not storage.** Base case: after pushing `x1` onto S, it is the last element, so pop returns x1. Inductive step: assume pushes through `xk` would pop in reverse. Pushing `x(k+1)` appends it after every prior element, so the first pop returns it and restores the state after k pushes; the induction hypothesis gives the remaining reverse order. No array or link assumption enters.

Intervening operations require a more precise history statement. A stack is linearizable sequentially: every successful push adds one top, every successful pop removes the current top, and peek changes nothing. Search or iteration extensions do not change LIFO transitions but expand observability and synchronization obligations.

**Bulk operations need order definitions.** `push_all([a,b,c])` might behave like push a, then b, then c, leaving c on top; prepending a linked range naively can reverse it. A range API must specify source order, partial-failure behavior, self-aliasing, maximum checks, and returned count. One transactional design constructs all incoming state then publishes it, while another permits a successful prefix.

`pop_n(k)` can return values in pop order or bottom-to-top order. The latter may need reversal. It must define `k>size`, output allocation failure, element move failure, and whether removal is atomic. Naming the order in the return type/docs prevents a stack-shaped ambiguity.

**Clear and retention are observable resources.** Logically, clear changes any S to empty. Physically, an array may retain capacity while destroying/clearing live elements; a linked stack releases nodes; a persistent stack drops a version but shared nodes can remain. References in unused array slots must be cleared when the runtime would otherwise retain objects or secrets.

Secure erasure is stronger than logical removal. Copies can remain in allocator storage, old resized buffers, persistent versions, undo history, swap, or dumps. Use platform-appropriate non-elidable mechanisms and a system-wide retention policy when confidentiality requires it. A Stack ADT alone cannot promise forensic deletion.

**Iteration weakens encapsulation if careless.** A read-only snapshot or iterator can support diagnostics, serialization, and bulk inspection. If it exposes the underlying container, clients can reorder or remove interior elements and violate the intended API discipline. An array iterator can be invalidated by growth; a linked iterator to a surviving node may remain address-valid but still have membership/order changes.

Serialization must choose bottom-to-top or top-to-bottom order, record enough type/version information, validate untrusted lengths before allocation, and define partial I/O. Deserialization should build a valid stack without quadratic linked append or reversed order. Never assume an implementation's private container layout is a stable wire format.

**Stacks support algorithms through explicit pending work.** Depth-first search pushes discovered-but-unprocessed vertices; correctness also requires visited-state and a neighbor-order policy. Parsing stacks hold operators, states, delimiters, or semantic values, each with grammar-specific invariants. Expression evaluation must reject malformed arity rather than underflow.

Replacing recursion with an explicit stack moves depth consumption from a runtime call stack into an application-controlled structure. It can enable explicit capacity/error handling and store only necessary frame state, but it does not eliminate memory use or automatically preserve exception, return, and cleanup semantics. Proof compares simulated frames and transition order.

**A call stack is not merely this container.** Runtime frames can contain return addresses, locals, saved registers, exception/unwind data, security metadata, and implementation-specific state. JVM frames include local variables and an operand stack under class-file verification rules. Go's `defer` calls execute in reverse order when a function returns or panics, but language/runtime stack behavior has its own specification.

Do not use machine-specific “thread stacks are 1–8 MB” claims from legacy notes as universal facts. Reservation, commitment, guard pages, growth, segmented/copying strategies, ABI, runtime, and configuration vary. Measure and cite the exact environment when a stack-memory budget matters.

**Reverse cleanup works only for nested dependencies.** If resources are acquired A, then B, and B depends on A, pushing cleanup actions and executing B then A is correct. If resource dependencies are not the reverse of acquisition order, one flat stack can release something too early. A dependency graph and topological shutdown plan are then the right abstraction.

Rollback/undo has the same caveat. Commands must capture enough inverse state, remain valid against later external changes, handle irreversible effects, group transactions, and bound retained history. A stack orders undo attempts; it does not make every operation reversible or transactional.

**Concurrency requires a named algorithm.** A mutex-protected stack can give a straightforward linearizable contract if element callbacks and allocation interaction are controlled. A Treiber-style stack uses an atomic top compare-and-swap; successful top publication/removal supplies candidate linearization points. It also faces retry behavior, memory ordering, ABA, and safe node reclamation.

Garbage collection can simplify reclamation but does not by itself prove linearizability or progress. Tagged pointers, hazard pointers, epochs, or other schemes have their own wrap, lifecycle, and stalled-participant assumptions. A bounded concurrent stack additionally needs full behavior—reject, block, wait with timeout, or backpressure—and cancellation/shutdown semantics.

**Test the abstract history and resource boundaries.** A sequential model is a simple array. Generate push, pop, peek, clear, bulk, checkpoint, rollback, and failure sequences; after each, compare bottom-to-top values, size, top, and capacity/lifetime invariants. Include empty, singleton, exact full, just-over-full, maximum arithmetic, repeated equal/sentinel-like values, aliased inputs, failing construction, and stale checkpoints.

Measure default growth separately from reserved/bounded forms; report allocations, bytes retained, individual operation latency, distributions, element callbacks, clear/rollback work, and serialization. For algorithms, generate deep/adversarial nesting and invalid input. Concurrent validation needs controlled histories, linearizability checking or model exploration where practical, stress, race/memory tools, ABA/reuse cases, stalled reclamation participants, and overload behavior.

The following Python trace uses a fixed-capacity array and explicit full/empty behavior. `None` marks non-live slots and is prohibited as data only in this educational model.

<!-- bijux-verify: {"id":"bounded-stack-transition-trace","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"values=alpha,omega\ntop=omega\nsize=2\ncapacity=4\noverflow_rejected=True\nunderflow_rejected=True\ninvariant=True\nevidence=finite_bounded_stack_trace\n","stderr":""}} -->
```python
class BoundedStack:
    def __init__(self, capacity):
        if capacity < 0:
            raise ValueError("negative capacity")
        self.storage = [None] * capacity
        self.size = 0

    def push(self, value):
        if value is None:
            raise ValueError("None is the educational spare-slot marker")
        if self.size == len(self.storage):
            return False
        self.storage[self.size] = value
        self.size += 1
        return True

    def pop(self):
        if self.size == 0:
            raise LookupError("empty stack")
        self.size -= 1
        value = self.storage[self.size]
        self.storage[self.size] = None
        return value

    def peek(self):
        if self.size == 0:
            raise LookupError("empty stack")
        return self.storage[self.size - 1]

    def checkpoint(self):
        return self.size

    def rollback(self, depth):
        if not 0 <= depth <= self.size:
            raise ValueError("invalid checkpoint for this trace")
        while self.size > depth:
            self.pop()

    def values(self):
        return self.storage[:self.size]

    def invariant(self):
        return (
            0 <= self.size <= len(self.storage)
            and all(value is not None for value in self.storage[:self.size])
            and all(value is None for value in self.storage[self.size:])
        )


stack = BoundedStack(4)
assert stack.push("alpha") and stack.push("beta")
mark = stack.checkpoint()
assert stack.push("gamma") and stack.push("delta")
overflow_rejected = not stack.push("epsilon")
assert stack.pop() == "delta"
assert stack.push("zeta")
stack.rollback(mark)
assert stack.pop() == "beta"
assert stack.push("omega")

empty = BoundedStack(0)
try:
    empty.pop()
    underflow_rejected = False
except LookupError:
    underflow_rejected = True

print(f"values={','.join(stack.values())}")
print(f"top={stack.peek()}")
print(f"size={stack.size}")
print(f"capacity={len(stack.storage)}")
print(f"overflow_rejected={overflow_rejected}")
print(f"underflow_rejected={underflow_rejected}")
print(f"invariant={stack.invariant() and empty.invariant()}")
print("evidence=finite_bounded_stack_trace")
```

## Definitions and Notation

| Term or symbol | Meaning |
|---|---|
| `S` | Abstract bottom-to-top sequence. |
| `S·<x>` | Sequence S with x appended at top. |
| depth/size `n` | Number of live stack elements. |
| top | Unique accessible end; element `s_(n-1)` when nonempty. |
| underflow | Pop/peek request with `n=0`. |
| overflow/full | Push cannot be accepted under current capacity/resource contract. |
| adaptor | Restricted interface backed by another container. |
| bounded stack | Stack with explicit maximum capacity and full policy. |
| checkpoint | Token representing a rollback state under specified mutation/version rules. |
| call frame | Runtime activation record; not an ordinary Stack ADT element by default. |
| operand stack | Virtual-machine sequence of intermediate values with type/verification rules. |
| linearization point | Instant a concurrent operation takes effect in the abstract history. |

Unless stated, complexity counts core element/link operations. Allocation, copying/moving/destruction, byte traffic, retention, callbacks, synchronization, retries, and reclamation are separate.

## Mechanisms, Invariants, or Proof Structure

**ADT proof.** Push appends exactly x; pop removes exactly the last element; peek returns it unchanged. Induction over k consecutive successful pushes proves reverse pop order. Empty/full results are outside the successful-transition theorem and follow their explicit policy.

**Array proof.** Maintain `0<=n<=c`, live initialized prefix `[0,n)`, and spare non-live suffix. Successful push constructs at n before committing n+1. Successful pop safely obtains element n-1, commits n-1 under the return/failure contract, and clears/destroys exactly that slot.

**Linked proof.** Head/top reaches exactly n acyclic live nodes. Push publishes a constructed node pointing to old head; pop advances to successor and retires exactly old head after return/observer rules permit.

**Checkpoint proof.** A depth rollback is valid only if the token belongs to this version and every intervening mutation admits truncation to that prefix. Repeated pop restores the prefix and releases each discarded live element exactly once.

**Cost conclusion.** Fixed-array push/pop/peek use worst-case constant index work when capacity checks and element operations are bounded. Dynamic-array push is amortized with possible linear growth. Linked push/pop use constant links but may allocate/reclaim. Bulk, clear, rollback, search, iteration, and serialization scale with affected depth.

## Alternatives and Trade-Offs

- **Fixed array:** bounded memory and compact locality; explicit full policy and maximum capacity.
- **Dynamic array:** compact traversal and common-library support; growth latency, peak memory, and invalidation.
- **Linked nodes:** stable individual nodes and no bulk growth; per-node allocation/metadata and pointer chasing.
- **Pool-backed links:** bounded nodes and controlled allocation; pool exhaustion, handle, and reuse invariants.
- **Persistent immutable list:** constant push/pop with safe version sharing; retention and reclamation depend on version lifetime.
- **Throwing versus option/result empty API:** exceptions/preconditions can be concise; explicit sum/result types make absence part of ordinary control flow.
- **Reject versus block on full:** rejection bounds latency; blocking supplies backpressure but requires cancellation, shutdown, and deadlock analysis.
- **Opaque adaptor versus exposed container:** opacity preserves LIFO reasoning; exposure supports more operations but weakens the abstraction.
- **Runtime recursion versus explicit stack:** recursion follows language control flow; explicit frames expose depth, memory, cancellation, and traversal state.
- **Cleanup stack versus dependency graph:** reverse acquisition is simple for nesting; general dependencies require topological ordering.
- **Mutex versus lock-free stack:** mutex simplifies linearizability/reclamation; lock-free designs trade blocking for retry, ordering, ABA, and reclamation complexity.

## Failure Modes and Misconceptions

1. **“Stack means top is index zero.”** Either end can represent top; every operation and serialization must agree.
2. **“Pop and peek are total.”** Empty behavior needs an explicit contract.
3. **“Null is a universal empty result.”** Null may be a valid element or prohibited for separate reasons.
4. **“Dynamic means unbounded.”** Representable size, bytes, allocator, quotas, and policy impose limits.
5. **“Push is worst-case O(1).”** Dynamic growth or allocation can violate that statement.
6. **“C++ pop returns the value like other stacks.”** Ecosystem APIs differ; inspect the exact contract.
7. **“Decrement size first is always safe.”** Return/move/destruction failure and concurrent observation determine commit order.
8. **“Popped values disappear from memory.”** Spare storage and copies can retain them physically.
9. **“A depth integer is always a rollback token.”** Versions, unrelated pops, concurrency, and external effects can invalidate it.
10. **“Iteration order is obvious.”** Minimal stack semantics do not define an iterator.
11. **“An explicit stack makes any recursive algorithm safe.”** It still needs capacity, frame, cancellation, and malformed-input bounds.
12. **“LIFO cleanup handles every dependency.”** Only properly nested dependencies fit one reverse stack.
13. **“Undo means transactional rollback.”** Inverse validity, irreversible effects, grouping, and retention remain.
14. **“Atomic top makes a concurrent stack correct.”** Memory ordering, retries, ABA, and reclamation remain.
15. **“A throughput benchmark proves deadline behavior.”** Individual growth, contention, and reclamation tails need measurement/bounds.
16. **“One Stack ADT proof covers VM and call stacks.”** Runtime stacks have distinct frames, verification, security, and exhaustion rules.

## Worked Examples

### Example 1

Starting with `<A,B>`, push C yields `<A,B,C>` and pop returns C, restoring `<A,B>`. Peek then returns B without mutation. Conclusion: the top is the sequence's designated end and each transition changes only that end.

### Example 2

Pop on an empty stack cannot return a magic `-1` if integers including -1 are valid. `Option<int>`, `(success,value)`, or a specified exception preserves the full value domain. Conclusion: empty signaling is part of type/API design.

### Example 3

A capacity-three stack contains A,B,C. Pushing D returns full and leaves A,B,C unchanged. A dropping-history policy that removes A and accepts D would produce B,C,D but is a different abstraction. Conclusion: full behavior must not silently redefine stack semantics.

### Example 4

Nine pushes into a doubling array can trigger copies at capacity boundaries; pop remains end removal. LIFO correctness holds regardless, but a growth push may be linear in current depth. Conclusion: abstract and performance properties are independent layers.

### Example 5

An expression evaluator sees `+` but has only one operand. Its operand-stack pop would underflow, so the parser reports malformed arity rather than continuing with a sentinel. Conclusion: domain validation should translate stack failure into a meaningful error.

### Example 6

Depth-first traversal pushes neighbors C then B, causing B to be processed first. Reversing push order changes deterministic visitation even though both use LIFO. Conclusion: stack correctness does not choose an algorithm's neighbor-order policy.

### Example 7

A parser checkpoints depth 5, pushes three speculative states, and fails. If no unrelated mutation/effect occurred, rollback pops to 5. If another component popped below 5, the numeric mark is invalid. Conclusion: checkpoints need ownership/version scope.

### Example 8

Resources A then B are acquired, and B depends on A; cleanup stack B then A is valid. Resource C must outlive an asynchronously flushing B despite being acquired later, so flat reverse order is wrong. Conclusion: use a dependency plan when lifetimes are not nested.

### Example 9

Replacing recursive traversal of a million-deep adversarial tree with explicit frames permits a checked node/byte budget and an ordinary overflow result. It still consumes memory proportional to frontier depth. Conclusion: explicit stacks improve control, not asymptotic space automatically.

### Example 10

A lock-free stack passes millions of pushes/pops under garbage collection. That does not establish behavior under manual node reuse, ABA, stalled reclamation, memory-order variants, overload, or a safety deadline. Conclusion: concurrent evidence must cover algorithm and environment assumptions.

## Cross-Program Connections

- [Programming Languages and Semantics](../../01-programming-languages-and-semantics/ROADMAP.md) owns evaluation contexts, exceptions, continuations, recursion, and observable failure behavior.
- [Systems Programming](../../05-programming-languages-systems-programming/ROADMAP.md) owns call-frame/ABI details, stack exhaustion, guard pages, allocation, raw lifetime, and secure erasure.
- [Compilers and Language Implementation](../../08-compilers-and-language-implementation/ROADMAP.md) connects parser, operand, control, and virtual-machine stacks.
- [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) develops DFS, expression evaluation, monotonic stacks, backtracking, and explicit-frame transformations.
- [Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) owns linearizability, Treiber-style algorithms, ABA, memory ordering, and reclamation.
- [Software Engineering Patterns](../../11-software-engineering-patterns/ROADMAP.md) connects command histories, undo, scope guards, transactions, and dependency-aware shutdown.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) owns untrusted depth, exhaustion, stack corruption, secret retention, and denial-of-service models.

## References

1. ISO C++ working draft, [`stack`](https://eel.is/c%2B%2Bdraft/stack). Container-adaptor requirements, supported underlying operations, constructors, top, push, pop, size, swap, and range behavior.
2. ISO C++ working draft, [Container Adaptors: General](https://eel.is/c%2B%2Bdraft/container.adaptors.general). Adaptor ownership, underlying-container parameters, allocator behavior, and swap exception propagation.
3. Rust Project, [`std::vec`](https://doc.rust-lang.org/stable/std/vec/index.html). Current vector representation and documented indexing, amortized push, and pop complexity.
4. Rust Project, [`Vec<T>::pop`](https://doc.rust-lang.org/stable/std/vec/struct.Vec.html#method.pop). Current optional empty result, element removal, and top-at-end behavior.
5. Oracle, [Java SE 25 `Deque`](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/Deque.html). LIFO use, paired exception/special-value operations, capacity-restricted behavior, and endpoint semantics.
6. Oracle, [Java SE 25 `Stack`](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/Stack.html). Legacy class contract and official recommendation to prefer `Deque` for a more complete/consistent LIFO API.
7. Python Software Foundation, [Python Tutorial: Using Lists as Stacks](https://docs.python.org/3/tutorial/datastructures.html#using-lists-as-stacks). End-based append/pop stack usage and contrast with front operations.
8. Python Software Foundation, [`collections.deque`](https://docs.python.org/3/library/collections.html#collections.deque). Bounded `maxlen`, endpoint operations, thread-safe append/pop documentation, iteration, and rotation behavior.
9. Go Project, [Go Language Specification: Defer Statements](https://go.dev/ref/spec#Defer_statements). Reverse-order invocation and evaluation timing for deferred calls during return/panic.
10. Oracle, [Java Virtual Machine Specification SE 25: Run-Time Data Areas](https://docs.oracle.com/javase/specs/jvms/se25/html/jvms-2.html#jvms-2.5). JVM stacks, frames, operand stacks, limits, and error conditions as a distinct runtime contract.

## Exercises

### Exercise 1

Specify the Stack ADT and prove LIFO for an arbitrary finite sequence of successful pushes followed by their pops. Include empty/full behavior outside the theorem.

### Exercise 2

Design array-backed and linked implementations with exact construction, return, destruction, capacity, and failure transitions. Compare their cost models.

### Exercise 3

Design versioned checkpoint/rollback for a mutable stack. Diagnose stale tokens, nested marks, element cleanup, external effects, and concurrency.

### Exercise 4

Compare recursive and explicit-stack implementations of an adversarial tree traversal, including semantic equivalence, depth budgets, cancellation, and evidence.

### Exercise 5

Prepare a verification plan for replacing a mutex-protected bounded stack with a lock-free stack in a high-reliability service.

## Answers to the Exercises

### Answer 1

Values are finite bottom-to-top sequences. `push(x)` appends x; nonempty `pop` returns/removes last; nonempty `peek` returns last unchanged; empty/size follow sequence length. Base k=0 is vacuous. For k+1 pushes, the last push appends `x_(k+1)`, so first pop returns it and restores the state after k pushes; induction yields `x_k,...,x_1`. The theorem assumes all named operations succeed and no interfering mutation removes those elements. Underflow uses the selected option/result/exception/precondition. Full push rejects with no effect or follows another explicitly named policy; it is not a successful push in the theorem.

### Answer 2

Array state `(B,n,c)` has live `[0,n)`. Push checks full/growth and arithmetic, constructs at n, then publishes n+1; failure cleans partial construction and preserves the promised state. Pop first safely establishes the returned value under its type guarantee, changes live extent, and destroys/clears the old slot exactly once. Fixed push has constant index work and explicit full; dynamic push is amortized with linear growth events. Linked state has acyclic n-node head chain; push constructs `Node(x,head)` before publication, pop saves value/successor, advances head, then reclaims under observer rules. Link work is constant, but each push can allocate and nodes add metadata/layout cost.

### Answer 3

Use token `(stack_identity,generation,depth)` or a persistent version handle. A mark is accepted only for this stack/version lineage and `0<=depth<=current`; rollback removes elements above depth, releasing each exactly once and reporting any destructor/effect constraints. Increment/branch generation when an operation invalidates older depth assumptions; nested marks form a disciplined scope. Define whether rollback itself can fail and whether tokens are one-use. External I/O or mutations need compensating transactions rather than mere truncation. Concurrent access requires exclusive ownership/locking or a versioned algorithm; a naked integer depth is not safe.

### Answer 4

Define a frame containing exactly the recursive call's pending node, child/continuation state, and accumulators. Prove a simulation: each recursive call/return corresponds to explicit frame push/pop and produces the same visitation/output under the same child order and failure semantics. Set node-count and retained-byte limits, checked depth, cancellation checks, and malformed-cycle/visited policy. Test shallow equivalence exhaustively, generated shapes, skewed maximum-depth trees, cycles where input permits them, cancellation at every state, allocation failure, and output order. Measure call/runtime versus explicit memory and latency on target systems; neither representation removes O(depth) live state.

### Answer 5

Specify capacity, full/empty results, ordering, linearization, progress, cancellation, timeout, shutdown, and element lifetime first. Select the exact atomic algorithm and memory model; prove push/pop publication, retry, ABA defense, maximum-size accounting, and safe reclamation under stalled/crashed threads. Keep the locked stack as a model. Run controlled schedule/linearizability exploration, stress, race/memory/undefined-behavior tools, forced address reuse, tag wrap, allocation failure, full/empty contention, stalled reclamation, overload, and long-duration tests. Measure throughput plus latency tails, retries, CPU, and retained memory. Require named concurrency, runtime, reliability, security, safety, operations, and independent review; passing sequential tests or a throughput benchmark is insufficient.
