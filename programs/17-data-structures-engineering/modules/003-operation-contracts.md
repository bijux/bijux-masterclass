---
module_id: DSE-003
program: Data Structures Engineering
level: 1
module_number: 3
title: Operation Contracts
status: complete
last_verified: 2026-08-29
---

# Operation Contracts

## One-Page Review

### Governing question

How can a data-structure operation state exactly what callers must provide, what successful and failed calls guarantee, what may change, and which resource or concurrency properties clients may rely on?

### Essential definitions

- A **precondition** is an obligation a caller must establish before an operation is invoked.
- A **postcondition** is an obligation the operation establishes on normal return.
- A **frame condition** states which abstract state may change and which state remains unchanged.
- An **exceptional postcondition** states the error and successor-state guarantee when an operation does not return normally.
- A **query** observes abstract state; a **command** may change it; one operation can return a result and change state.
- A **total operation** has specified behavior for every value in its declared input domain; a **partial operation** requires a precondition.
- A **history constraint** restricts relationships across observations over time, such as monotonic version numbers.
- **failure atomicity** means a rejected or failed operation has a stated all-or-nothing abstract effect.
- An **invalidation rule** states when references, views, handles, cursors, or iterators cease to be usable.
- A **complexity guarantee** is a scoped upper or amortized resource bound under stated size and operation assumptions.

### Central model, mechanism, or theorem

For abstract state (a\in A), input (x\in X), normal result (y\in Y), and successor $a'$, specify an operation as a relation

$$
Op\subseteq A\times X\times Outcome(Y)\times A.
$$

A normal Hoare-style obligation is

$$
\{RI\land Pre(a,x)\}\ op(x)\ \{RI'\land Post(a,x,y,a')\land Frame(a,a')\}.
$$

Every documented error outcome needs its own postcondition. If behavior outside `Pre` is unspecified, callers cannot rely on it; when practical, a total API can instead return an explicit result for empty, absent, full, or invalid cases.

### Critical invariants

- Contracts describe abstract values and observations rather than private fields.
- Every parameter domain, equality/order/hash requirement, ownership rule, and nullability condition is explicit.
- Normal results, errors, state changes, and no-change guarantees are separately stated.
- Frame conditions prevent an operation from changing unrelated abstract state.
- Returned aliases and views state mutability, lifetime, ownership, and invalidation.
- Complexity names worst-case or amortized form, size measure, operation model, and adversarial assumptions.
- Concurrent contracts name safety, progress, ordering, and consistency semantics rather than merely “thread-safe.”
- Subtypes and replacement implementations preserve client obligations and guarantees.
- Assertions check implementation invariants; they do not silently impose undocumented caller obligations.
- Tests and executable models are finite evidence, not universal proof of contract compliance.

### Common failures

Common failures are documenting only a method signature; using “undefined” where a checked result is feasible; omitting state after error; promising `O(1)` without worst-case/amortized scope; returning a mutable internal alias; leaving iterator invalidation implicit; confusing structural validity with correct abstract transition; strengthening preconditions in a subtype; weakening error or concurrency guarantees; and declaring correctness from happy-path examples.

### Compact example

For bounded stack `push(x)`, one partial contract is: precondition `size < capacity`; normal postcondition `contents' = contents ++ [x]`, result is unit, capacity unchanged, and no other stack changes. A total alternative returns `Full` when at capacity and guarantees `contents' = contents`. Allocation failure needs a separate exceptional guarantee. The representation may be an array or linked nodes; neither belongs in the abstract contract unless exposed.

### Connections

[DSE-001](001-abstract-data-types-and-concrete-representations.md) defines abstract behavior and representation independence. [DSE-002](002-representation-invariants.md) establishes valid concrete states. DSE-004 adds cost accounting, and later structure chapters instantiate these contracts. [TPROG-003](../../07-programming-languages-theory-of-programming/modules/003-induction-and-structural-induction.md) supplies proof structure.

## Governing Question

What may a caller conclude after `insert`, `remove`, `find`, `clear`, or `iterate` returns—or fails—and what must have been true before the call for that conclusion to be valid?

A type signature answers only part of the question. `remove(key) -> value` does not say whether an absent key throws, returns a sentinel, blocks, or creates a default; whether one or all duplicates are removed; whether other iterators remain valid; whether equality callbacks can reenter; or whether failure preserves state. Those choices define substitutability and must be reviewable.

## Why This Matters

Data structures sit beneath large amounts of code. A tiny semantic mismatch propagates: a map whose `put` returns the new rather than old value, a priority queue unstable on ties, a view that aliases mutable storage, or a failed insertion that changes size can corrupt higher-level reasoning while preserving representation invariants.

Contracts also preserve implementation freedom. If clients rely only on abstract effects and declared resource bounds, an array can become a tree or a compact hash table. If clients accidentally depend on traversal order, address stability, or exception timing, those observations have become de facto contract and block change.

Security and high-stakes uses make omissions dangerous. Hash flooding can invalidate latency assumptions; comparator callbacks can mutate a structure; stale handles can address new objects; allocation failure can leave partial state. A production contract names such boundaries and the human review required for domain use.

## Prerequisites and Retrieval

Retrieve these ideas from DSE-001 and DSE-002:

1. An ADT is defined by abstract values, operations, laws, and errors.
2. An abstraction function maps valid representations to abstract values.
3. A representation invariant can hold even when an operation implements the wrong abstract transition.
4. Constructors establish invariants and public operations preserve them.
5. Observable behavior includes errors, order, aliasing, serialization, concurrency, and promised resources.
6. A test trace covers finitely many states and inputs.

## Learning Objectives

After completing this module, you should be able to:

- specify operation input domains, preconditions, normal and exceptional postconditions;
- write frame conditions and distinguish abstract from concrete mutation;
- choose deliberately between partial, checked, and sentinel-returning APIs;
- specify equality, ordering, hashing, ownership, aliasing, and callback constraints;
- define iterator/view lifetime and invalidation rules;
- state worst-case, amortized, expected, and output-sensitive complexity precisely;
- describe sequential, concurrent, and persistent operation observations;
- evaluate behavioral subtyping and compatibility of contract changes;
- derive tests and proof obligations from a contract;
- audit failure paths and high-stakes uses without overstating evidence.

## Core Exposition

Start from abstract state. A sequence operation `append(x)` transforms mathematical sequence (s) into (s\mathbin{\|\!|}[x]). It may grow an array, allocate a node, copy a persistent path, or write a page. The public postcondition should state the sequence relation; representation details belong to the implementation proof.

Use old-state notation explicitly. Let (a_0) be state at invocation and (a_1) the state on return. A map update might say:

$$
lookup(a_1,k)=v
$$

and for all (j\ne k), (lookup(a_1,j)=lookup(a_0,j)). The second clause is a frame condition. Without it, an implementation that deletes every other entry still satisfies the first equation.

**Input domains and preconditions.** A declared element type rarely captures every obligation. Hash-map keys may require stable equality and hash values while resident. Ordered trees require a total or otherwise specified ordering over admitted keys. Numeric priorities may exclude NaN because it violates ordinary ordering assumptions. Ownership-sensitive structures can require that a node is currently unlinked.

Preconditions are caller obligations, not validation algorithms. A contract can require a valid comparator even if testing it exhaustively is impossible. Public APIs should avoid severe unchecked preconditions when a cheap checked result exists. Internal operations can use stronger preconditions when callers are controlled and proof/local checks establish them.

Distinguish invalid input from ordinary absence or capacity. An empty pop is part of common stack state, not necessarily programmer corruption. APIs can expose `try_pop -> Option<T>`, `pop -> T` with nonempty precondition, or `pop -> T` with a documented exception. Each is legitimate; consistency and client needs decide.

**Normal postconditions.** State result, abstract successor, preserved observations, and ownership transfer. For set insertion:

$$
S_1=S_0\cup\{x\},\qquad result=(x\notin S_0).
$$

This defines both idempotent state behavior and a Boolean meaning. “Returns success” is ambiguous: did the call finish, did membership change, or is the element present afterward?

For removal from a multiset, say whether one occurrence or all are removed. For priority queues, define minimum order, tie behavior, and whether equality of priorities implies stability. For queues, define FIFO over successful enqueues and whether rejected operations enter history.

**Frame conditions.** State what cannot change: other keys, element order outside the edited range, capacity, comparator, version, source collection, or sibling persistent versions. A query can change a cache without changing abstract state; the frame is abstract unless cache visibility or resource use is promised.

Frame scope includes external authority. `insert(x)` must not mutate `x` unless ownership transfer permits it. A sort operation may permute a supplied buffer because the buffer is its explicit target; a set lookup normally may not modify key objects through aliases.

**Errors and failure atomicity.** Enumerate ordinary negative results, caller errors, resource failures, callback failures, cancellation, corruption, and internal defects. For each observable outcome, state successor state. Useful levels include:

- **no-throw/guaranteed success:** operation completes under stated preconditions;
- **strong guarantee:** on failure, abstract state is unchanged;
- **basic guarantee:** invariant holds and resources are owned, but abstract state may change as documented;
- **no guarantee:** reserved for explicitly unsafe/internal boundaries, never inferred casually.

Names vary by ecosystem; state behavior rather than relying only on labels. If a comparator throws after swaps, a heap may remain valid but contain a different permutation. If allocation occurs before publication, insertion can often provide the strong guarantee. Callback and destructor behavior must be included.

Do not convert implementation defects into ordinary caller errors. A violated representation invariant indicates a bug, corruption, or trust-boundary failure. Assertions may terminate or diagnose; documented exceptions report anticipated contract outcomes.

**Aliasing, ownership, and lifetime.** Returned elements, slices, references, views, and iterators can expose internal state. Specify whether results are copies, immutable snapshots, live views, borrowed references, or owned transfers. State how long they remain valid and which operations invalidate them.

An array reallocation may invalidate all element references and iterators; an insertion into a node-based tree may preserve most handles; a compacting structure may move everything. Do not promise stability merely because the current implementation happens not to move values. Conversely, unnecessarily broad invalidation makes clients slow and fragile.

For input objects, say whether the structure retains an alias, copies, clones, or takes ownership. Mutable keys are dangerous when hash/equality or ordering changes after insertion. The contract can prohibit such mutation, snapshot the key, or reindex on controlled changes.

**Iteration contracts.** Define order, multiplicity, consistency, mutation behavior, and termination. A set may promise unspecified but deterministic-per-state order, insertion order, sorted order, or no stability. “Unspecified” does not mean random and should not be used to hide unsafe behavior.

Mutation during iteration can fail fast, invalidate the iterator, produce a weakly consistent traversal, snapshot at creation, or be forbidden. Concurrent iteration might omit or include racing updates according to a defined consistency model. State whether each element present throughout is seen and whether duplicates are possible.

**Complexity and resources.** A bound needs a size measure and cost model. `O(1)` may be worst-case, expected under a hash assumption, or amortized over a sequence. Amortized dynamic-array append permits occasional (O(n)) copies; it does not provide per-call latency.

State output sensitivity where relevant: reporting (k) range results may cost (O(\log n+k)). Name allocation, auxiliary space, recursion depth, I/O, cache behavior, and maximum capacity when clients rely on them. Complexity constants and machine effects are developed in DSE-004 through DSE-006.

Adversaries affect expected guarantees. Hash operations expected (O(1)) under independent distribution can degrade under chosen collisions. A contract for untrusted keys needs keyed hashing, collision bounds, tree fallback, or an honest weaker guarantee.

**Callbacks and reentrancy.** Comparators, hash functions, equality, allocators, destructors, visitors, and user predicates are executable dependencies. State purity, determinism, totality, exception, and reentrancy requirements. If equality mutates the map during lookup, reasoning can collapse.

Avoid holding internal locks while invoking arbitrary callbacks unless the contract handles deadlock and reentrancy. Snapshot inputs, defer callbacks, or use protocol states as appropriate. A type signature `Comparator<T>` cannot express all behavioral obligations.

**Concurrency contracts.** “Thread-safe” is incomplete. Name which operations may overlap, the consistency condition (for example linearizability or snapshot behavior), atomicity of compound operations, memory visibility, blocking, fairness, and progress class. `contains(k)` followed by `insert(k)` is not atomic unless a compound operation says so.

For linearizable operations, each completed call appears to take effect at one point between invocation and response, while real-time order is preserved. That does not guarantee lock freedom or deterministic scheduling. Progress and safety are separate.

**Persistent structures.** A functional update returns a new version and promises the old abstract value remains unchanged. Structural sharing is invisible unless identity, memory, or lifetime is exposed. Contracts state whether element objects themselves are immutable or merely container topology.

Version handles need lifetime and reclamation rules. Equality may be structural, identity-based, or abstract-value equality. Serialization compatibility and history access are separate promises.

**Behavioral subtyping and evolution.** A replacement cannot demand more of existing callers or promise less than the advertised abstraction. It may accept a wider input domain, provide stronger postconditions, or improve resource bounds without violating other observations. Error types, ordering, atomicity, invalidation, and complexity are compatibility surfaces.

Changing an absent lookup from `None` to exception, making iteration ordered, or weakening strong failure atomicity can break clients. Version contracts, provide adapters, and test old client traces. Deprecation text is not a compatibility proof.

**From contracts to evidence.** Derive example tests, boundary tests, algebraic properties, state-machine model tests, fault injection, aliasing tests, invalidation tests, resource measurements, concurrent histories, and proof obligations. Test rejected inputs before/after snapshots. Generate operation sequences against a small reference model.

The following bounded deque model makes normal, full, empty, and frame behavior observable. It uses immutable tuples so snapshots cannot mutate internal state. It is a finite executable calibration, not proof of all implementations.

<!-- bijux-verify: {"id":"bounded-deque-contract","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"after_push=('a', 'b')\nfull=unchanged=True\npop_left=a remaining=('b',)\nempty=unchanged=True\ntrace_contract_pass=True\n","stderr":""}} -->
```python
class BoundedDeque:
    def __init__(self, capacity):
        if type(capacity) is not int or capacity < 0:
            raise ValueError("capacity must be a nonnegative integer")
        self._capacity = capacity
        self._items = ()

    def snapshot(self):
        return self._items

    def try_push_right(self, value):
        old = self._items
        if len(old) == self._capacity:
            return False
        self._items = old + (value,)
        return True

    def try_pop_left(self):
        old = self._items
        if old == ():
            return None
        self._items = old[1:]
        return old[0]


deque = BoundedDeque(2)
assert deque.try_push_right("a")
assert deque.try_push_right("b")
print(f"after_push={deque.snapshot()}")
before_full = deque.snapshot()
print(f"full=unchanged={not deque.try_push_right('c') and deque.snapshot() == before_full}")
removed = deque.try_pop_left()
print(f"pop_left={removed} remaining={deque.snapshot()}")
assert deque.try_pop_left() == "b"
before_empty = deque.snapshot()
print(f"empty=unchanged={deque.try_pop_left() is None and deque.snapshot() == before_empty}")
print("trace_contract_pass=True")
```

## Definitions and Notation

Let an operation contract be (K=(Pre,N,E,F,R)): precondition, normal relation, exceptional relations, frame relation, and resource/concurrency guarantees. `old(e)` denotes expression (e) in invocation state; primed names denote response state.

For partial operation (op:A\times X\rightharpoonup A\times Y), `Pre` identifies its domain. A totalized form returns (Outcome(Y)=Ok(Y)\mid Error(Code)) and defines a successor for every admitted input.

A frame can be written as a modifies set or relational equality. For map update at key (k):

$$
\forall j\ne k.\ lookup(a',j)=lookup(a,j).
$$

Sequential history (h) is a sequence of invocations/responses. Concurrent specifications relate a history to allowed sequential histories or another consistency model. Resource bound (T(n,k,\alpha)) names input size (n), output size (k), and assumptions (\alpha).

## Mechanisms, Invariants, or Proof Structure

**Normal correctness.** Assume representation invariant and precondition. Prove termination if promised, successor invariant, abstraction correspondence, result relation, and frame.

**Failure correctness.** For each failure point, prove its documented error mapping and successor relation. Strong failure atomicity requires (AF(r')=AF(r)), not necessarily byte-identical representation.

**Totalization.** Replace an unchecked precondition such as nonempty with an explicit empty outcome. Show successful cases match the partial operation and rejected cases preserve the stated frame.

**Aliasing proof.** Enumerate references crossing the boundary and show ownership, immutability, copying, lifetime, or invalidation prevents unauthorized abstract mutation and use-after-invalidation.

**Resource proof.** Count primitive operations under a stated model; for amortized bounds define a potential or aggregate argument. Measurement calibrates constants and machine behavior but is not asymptotic proof.

**Replacement review.** Compare input domain, normal results, errors, state frame, aliases, order, resources, and concurrency. A shared name/signature is insufficient.

**Finite evidence boundary.** The snippet covers one capacity and trace. Tuple immutability helps its alias boundary, but it proves neither all capacities/traces nor exception, concurrency, memory, timing, or production behavior.

## Alternatives and Trade-Offs

**Partial versus checked operation.** Preconditions produce simple internal code and proof obligations for controlled callers. Checked outcomes compose safely at public boundaries but add branches and result handling.

**Exception versus option/result.** Exceptions separate uncommon failure from main flow; result types expose outcomes in signatures. Sentinels are compact but ambiguous if the element domain contains the sentinel.

**Strong versus basic failure guarantee.** Strong rollback simplifies clients and retry but may require copying or staged publication. Basic guarantees can be cheaper when partial progress is meaningful and documented.

**Live view versus snapshot.** Live views avoid copying and reflect updates but need lifetime/concurrency rules. Snapshots are stable and easy to reason about but consume time/memory and may become stale.

**Stable versus invalidating handles.** Stability enables long-lived references but constrains compaction/layout. Explicit invalidation enables dense structures and relocation. Generation-tagged handles can detect some stale use at added cost.

**Worst-case versus amortized/expected cost.** Amortized or expected bounds enable fast practical designs. Worst-case guarantees matter for latency, adversarial, and real-time uses. State the guarantee clients actually need.

**Minimal versus rich contract.** Minimal observations maximize implementation freedom. Rich ordering, atomicity, views, and performance can make the ADT useful. Every promise has maintenance and verification cost.

## Failure Modes and Misconceptions

1. **“The signature is the contract.”** It omits state relations, errors, aliasing, order, resources, and concurrency.
2. **“Preconditions are input checks.”** They are obligations; enforcement is a separate design choice.
3. **“Preserving the invariant proves correctness.”** A valid stack can remove the wrong end.
4. **“Failure means no change.”** Only an explicit exceptional postcondition provides that guarantee.
5. **“Queries never mutate.”** Invisible caches can change while abstract state remains fixed.
6. **“Returning a collection is harmless.”** A live mutable alias can bypass every operation contract.
7. **“O(1) has one meaning.”** Worst-case, expected, and amortized bounds differ materially.
8. **“Unspecified order can change mid-iteration arbitrarily.”** Allowed observations and mutation rules still constrain behavior.
9. **“Thread-safe makes a compound sequence atomic.”** Only a compound contract or transaction supplies atomicity.
10. **“A subtype can reject more cases for safety.”** Strengthening preconditions breaks substitutability.
11. **“Equivalent final values imply equivalent operations.”** Errors, histories, callbacks, resources, and intermediate visibility may differ.
12. **“Assertions document caller errors.”** Internal assertions usually diagnose violated implementation assumptions.
13. **“A reference implementation is the specification.”** It can contain omissions, defects, or accidental behavior.
14. **“Passing model tests proves universal compliance.”** Tested traces and finite inputs do not cover all executions.

## Worked Examples

### Example 1

**Question:** Specify `set.add(x)` returning Boolean.

**Reasoning:** Require `x` in element domain with stable equality/hash as applicable. Poststate is old set union `{x}`; result is true exactly when `x` was absent. Other memberships are unchanged.

**Conclusion:** State effect and Boolean meaning must agree.

### Example 2

**Question:** What frame is missing from “map.put(k,v) makes lookup(k)=v”?

**Reasoning:** Without `lookup(j)` unchanged for every `j != k`, the method may corrupt unrelated entries while satisfying the stated equation.

**Conclusion:** Local postconditions need noninterference clauses.

### Example 3

**Question:** How can `pop()` be total?

**Reasoning:** Return `Some(x)` with remaining stack on nonempty state and `None` with unchanged state on empty. If element values can be `None`, use a tagged option rather than sentinel.

**Conclusion:** Totalization converts a precondition into explicit outcomes.

### Example 4

**Question:** What does a strong insertion failure guarantee mean?

**Reasoning:** If allocation or copying fails, the abstract collection equals its invocation value and owned resources remain valid. Internal capacity may have changed invisibly if the abstraction permits it.

**Conclusion:** Strong guarantee concerns observable abstract state, not necessarily identical bytes.

### Example 5

**Question:** May a vector promise constant-time append?

**Reasoning:** Geometric growth typically gives amortized constant time, while a resizing append is linear. Reserving adequate capacity can yield a stronger scoped guarantee.

**Conclusion:** Name amortization and capacity assumptions.

### Example 6

**Question:** Why specify iterator invalidation?

**Reasoning:** After relocation, an iterator may point to freed or unrelated storage. Clients need to know which mutations preserve, invalidate, or update its meaning.

**Conclusion:** Lifetime is observable contract, not layout trivia.

### Example 7

**Question:** Can a lookup invoke user equality safely under a lock?

**Reasoning:** Equality may throw, reenter the map, block, or acquire another lock. The contract must constrain callbacks or the implementation must avoid unsafe lock/callback composition.

**Conclusion:** Behavioral dependencies extend beyond parameter types.

### Example 8

**Question:** Does `put_if_absent` equal `contains` then `put`?

**Reasoning:** Sequentially they may match; concurrently the two-call sequence races. An atomic compound operation has one linearization point and returns according to that instant.

**Conclusion:** Composition of thread-safe calls is not automatically atomic.

### Example 9

**Question:** Can a persistent tree update mutate shared element objects?

**Reasoning:** Topology persistence preserves old tree membership/path structure, not deep immutability of referenced elements unless promised.

**Conclusion:** Specify container and element ownership separately.

### Example 10

**Question:** A priority structure schedules radiation-treatment actions. What review exceeds its operation proof?

**Reasoning:** Data-structure reviewers verify ordering, ties, bounds, failure atomicity, overflow, concurrency, persistence, and tested implementation identity. Domain and clinical reviewers validate priorities, deadlines, cancellation, overrides, and fail-safe behavior. Safety, security, human-factors, quality, and regulatory reviewers validate the integrated workflow. This chapter claims none of those external approvals.

**Conclusion:** A correct ADT contract cannot validate the domain policy or deployed system.

## Cross-Program Connections

- [Theory of Programming](../../07-programming-languages-theory-of-programming/ROADMAP.md) supplies Hoare-style and refinement reasoning.
- [Software Design & Domain Modeling](../../09-software-engineering-software-design-and-domain-modeling/ROADMAP.md) connects operations to domain commands, queries, invariants, and errors.
- [Testing & Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) supplies model-based, property, fault, and concurrency testing.
- [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) establishes cost and correctness arguments for operations.
- [Concurrent & Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) owns memory models, linearizability, and progress in depth.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) reviews adversarial inputs, stale handles, resource exhaustion, and side channels.

## References

1. C. A. R. Hoare, [*An Axiomatic Basis for Computer Programming*](https://doi.org/10.1145/363235.363259), Communications of the ACM, 1969. Preconditions, postconditions, and compositional reasoning.
2. Barbara Liskov and Jeannette Wing, [*A Behavioral Notion of Subtyping*](https://www.cs.cmu.edu/~wing/publications/LiskovWing94.pdf), ACM TOPLAS, 1994. Behavioral replacement through constraints on methods and history.
3. Eiffel Software, [*Design by Contract, Assertions and Exceptions*](https://www.eiffel.org/doc/eiffel/ET-_Design_by_Contract_%28tm%29%2C_Assertions_and_Exceptions). Preconditions, postconditions, invariants, inheritance, and exception semantics.
4. OpenJML Project, [Documentation](https://www.openjml.org/documentation/). Executable and static checking of Java method specifications, frames, and exceptional behavior.
5. Dafny Project, [Online Tutorial Guide](https://dafny.org/dafny/OnlineTutorial/guide). Preconditions, postconditions, frames, invariants, termination, and verified data abstractions.
6. ISO C++ working draft, [Container requirements](https://eel.is/c++draft/container.requirements). Current operation semantics, complexity, and iterator requirements for standard containers.
7. Oracle, [Java SE 25 `Collection` API](https://docs.oracle.com/en/java/javase/25/docs/api/java.base/java/util/Collection.html). Current normative-style API semantics, optional operations, mutation, equality, and exceptions.
8. Rust Project, [Standard library `Vec` documentation](https://doc.rust-lang.org/std/vec/struct.Vec.html). Capacity, allocation, indexing, error, ownership, and complexity guarantees.
9. Python Software Foundation, [`collections.deque`](https://docs.python.org/3/library/collections.html#collections.deque). Bounded behavior, operation semantics, thread-safety statement, and complexity guidance.
10. SEI CERT C++, [ERR56-CPP: Guarantee exception safety](https://wiki.sei.cmu.edu/confluence/display/cplusplus/ERR56-CPP.+Guarantee+exception+safety). Failure-state and resource guarantees for exceptional operations.

## Exercises

### Exercise 1

Write complete normal and empty contracts for queue `try_dequeue`, including result, successor sequence, and frame. Explain why a null sentinel may be invalid.

### Exercise 2

Specify `map.compute_if_absent(k,f)` including key requirements, callback behavior, exceptions, reentrancy, state changes, and concurrency. Identify design choices that cannot remain implicit.

### Exercise 3

An array list documents append as `O(1)` and returns element references. Rewrite its resource and invalidation guarantees precisely for geometric growth.

### Exercise 4

Prove that the executable bounded deque trace satisfies the stated push/full/pop/empty contracts. State which universal claims remain unproved.

### Exercise 5

Prepare a verification plan for replacing a stable priority queue with a concurrent implementation in a high-stakes scheduler. Cover semantics, failures, resources, histories, migration, implementation evidence, and human review.

## Answers to the Exercises

### Answer 1

Let old queue be sequence (q). If nonempty (q=[x]\mathbin{\|\!|}r), return `Some(x)` and establish (q'=r); capacity/configuration and other objects are unchanged. If empty, return `None` and establish (q'=q=[]). The operation is total over valid queues. A null sentinel is ambiguous when null is an admitted element; a tagged option distinguishes empty from a stored null.

### Answer 2

Require valid resident-key equality/hash semantics. Specify whether `f` receives the key, may return null, may throw, block, or mutate the map, and whether it is invoked once. If key is present, return its value and do not invoke `f`. If absent and `f` returns value (v), associate (k\mapsto v) and leave other keys unchanged. If `f` fails or returns a prohibited value, state whether the map is unchanged. Define reentrancy and concurrent atomicity: a linearizable contract might allow several computations but publish at most one, or promise single execution under stronger coordination. These alternatives affect side effects and cannot be inferred from the name.

### Answer 3

Append is amortized (O(1)) over a sequence under geometric capacity growth, worst-case (O(n)) time when reallocation moves (n) elements, and may allocate proportional new capacity. If current size is below capacity and element construction is bounded, the no-reallocation path is constant under the stated machine model. Reallocation invalidates all references/iterators into the buffer; a nonreallocating append preserves references to existing elements but may invalidate the past-end iterator. Exact language/library rules override this generic contract.

### Answer 4

Starting empty with capacity two, each successful push appends one value, yielding `('a','b')`. The third push observes full state, returns false, and snapshot equality establishes the no-change clause for that call. Pop returns old first element `a` and successor suffix `('b',)`; the next returns `b` and empty. Empty pop returns `None` with equal before/after snapshots. Assertions and output reproduce this trace. They do not prove all values, capacities, operation sequences, exceptions, alias behavior in other implementations, concurrency, resource bounds, or the Python runtime.

### Answer 5

Freeze the sequential abstract contract: ordering, stable ties, duplicate identity, cancellation, capacity, errors, failure atomicity, persistence, deadlines, and overflow. Define concurrent history semantics, linearization points or allowed outcomes, progress/fairness, memory visibility, iterator/snapshot behavior, and shutdown. Model-test histories against the sequential specification; stress and systematically schedule races; inject allocation, callback, cancellation, crash, and recovery failures; test adversarial priorities and bounds; measure worst-case latency and capacity under production hardware. Verify migration/serialization and rollback, pin implementation/toolchain/configuration digests, and trace every contract change. Independent concurrency and data-structure reviewers assess proofs/code; domain, clinical/safety, security, operations, human-factors, quality, and regulatory owners validate scheduling policy and deployment. No release claim follows from unit tests or this chapter alone.
