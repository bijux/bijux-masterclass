---
module_id: DSE-002
program: Data Structures Engineering
level: 1
module_number: 2
title: Representation Invariants
status: complete
last_verified: 2026-08-29
---

# Representation Invariants

## One-Page Review

### Governing question

How do we state, establish, preserve, and audit the conditions that make a concrete data-structure state a valid representation of its abstract value?

### Essential definitions

- A **representation invariant**, written `RI(r)`, is a predicate that identifies valid concrete states.
- An **abstraction function**, `AF`, interprets every valid representation as an abstract value.
- An **inductive invariant** holds initially and is preserved by every allowed transition.
- A **local invariant** concerns one component; a **global invariant** relates components or the whole reachable graph.
- **Representation exposure** gives outside code authority to violate an invariant without passing through the owning operations.
- A **transient violation** is an intermediate invalid state permitted only inside an owned atomic boundary.
- A **validator** or `check_rep` recomputes selected invariant clauses at runtime.

### Central model, mechanism, or theorem

Let `R` be concrete states and `V = {r in R | RI(r)}`. For every creator `c`, prove `RI(c(...))`. For every operation `op` and valid input `r` satisfying its precondition, prove that every normally returned concrete successor `r'` satisfies `RI(r')` and that failures satisfy the promised state rule. Then prove abstract correspondence: `AF(r')` and the result agree with the abstract operation applied to `AF(r)`. Establishment plus preservation makes `RI` inductive over all reachable public states.

### Critical invariants

- `RI` is strong enough to make `AF` and every implementation operation well-defined.
- Every creator establishes all invariant clauses before publishing the object.
- Every mutator restores all clauses before control, an alias, or an observation escapes.
- Failure and cancellation paths preserve the old valid state or establish a documented valid successor.
- Cached and redundant fields agree with their authoritative source.
- Ownership prevents clients, callbacks, iterators, and concurrent actors from bypassing preservation.
- Checks are side-effect-free and independent enough to detect—not merely repeat—the implementation defect.

### Common failures

Typical failures are documenting only field types, writing an invariant that is too weak or impossible to maintain, checking only the changed field, forgetting empty and full states, exposing mutable aliases, publishing during construction, allowing callbacks during a transient violation, using disabled assertions as input validation, and treating passing checks as a proof of all reachable states.

### Compact example

A bounded min-priority collection stores pairs in a list and a cached size. Its invariant can require: capacity is a nonnegative integer; size equals list length; size does not exceed capacity; priorities are finite numbers; and each stored sequence number is unique. A minimum query is meaningful only after these facts hold. Construction establishes them; insertion validates inputs and capacity before mutation; removal updates the list and cache together; an independent checker recomputes every clause.

### Connections

[DSE-001](001-abstract-data-types-and-concrete-representations.md) separates abstract values from concrete state. [DSE-003](../ROADMAP.md) turns operation obligations into explicit contracts. [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) supplies loop invariants and correctness arguments, while [Software Engineering: Patterns](../../11-software-engineering-patterns/ROADMAP.md) studies ownership boundaries that keep invariants enforceable.

## Governing Question

Concrete data structures possess more possible machine states than they should ever expose. A list field can contain duplicates, a tree can contain a cycle, a cached count can disagree with reachable nodes, or a hash-table entry can occupy a bucket inconsistent with its hash. Type declarations rule out some nonsense, but they rarely express all relationships on which operations rely. A representation invariant names the admissible subset.

The governing question is therefore not merely “what should be true?” It is: which predicate is sufficient to interpret the state, who owns its preservation, across which boundaries must it hold, and what evidence justifies the claim? A useful answer connects specification, proof, implementation, testing, failure handling, concurrency, and maintenance. The invariant becomes a compact design theory for the representation.

C. A. R. Hoare's 1972 paper, [*Proof of Correctness of Data Representations*](https://ora.ox.ac.uk/objects/uuid%3A496c86ab-dbfd-4901-b2dd-e94fc4f42e51), formalized the relation between abstract properties and concrete representations. Liskov and Guttag's [*Abstraction and Specification in Program Development*](https://mitpress.mit.edu/9780262121125/abstraction-and-specification-in-program-development/) made representation invariants and abstraction functions central tools for modular development. Their durable lesson is that a representation is justified by obligations, not by familiarity.

## Why This Matters

An invariant turns an implicit dependency into a reviewable statement. A binary-search operation silently assumes sorted order. A linked-list traversal assumes termination and valid links. A heap removal assumes shape and order. Without explicit invariants, these assumptions are scattered across code, tests, and the memories of maintainers. A local edit can violate one and cause a failure far from the mutation.

Invariants also delimit fault containment. If only an owning module can mutate a representation, a violation points to a constructor, mutator, deserializer, or unsafe boundary in that module. If mutable aliases escape, any client becomes a suspect. This difference affects debugging cost, security review, concurrency design, and the feasibility of formal reasoning.

Production structures add redundant state for performance: cached lengths, parent pointers, summaries, fingerprints, free lists, or materialized indexes. Redundancy creates proof obligations because two encodings of the same fact can diverge. A useful invariant declares which component is authoritative and how derived components correspond. “The cache is correct” is too vague; “`cached_size` equals the number of reachable live nodes” is checkable.

Failure paths matter as much as successful paths. Allocation failure, invalid input, cancellation, exceptions from comparison callbacks, partial deserialization, and process recovery can interrupt a mutation. If an object becomes observable while invalid, subsequent operations may misbehave even when they are individually correct. Strong exception safety—failure leaves the abstract value unchanged—is one policy. A documented valid fallback state is another. Unspecified corruption is not.

Finally, invariants make optimization disciplined. One may replace an eager count with a cache, an array with a circular layout, or direct nodes with compressed indexes. The change is safe only if the new `RI` and `AF` support the same abstract contract. The invariant is not paperwork after implementation; it is the bridge that permits implementation change.

## Prerequisites and Retrieval

You should understand predicates, sets, finite sequences, functions, object references, and basic preconditions and postconditions. Recall from [DSE-001](001-abstract-data-types-and-concrete-representations.md) that `AF` maps a valid concrete state to an abstract value, and that multiple representations may encode the same value. Recall also that a proof by induction has a base case and a preservation step.

For this chapter, distinguish three uses of “invariant.” A loop invariant holds at a chosen point in every loop iteration. An object invariant holds at specified observable boundaries during an object's lifetime. A representation invariant characterizes valid encodings inside an abstraction. They share the establishment-and-preservation pattern but quantify over different states and boundaries.

## Learning Objectives

After completing this module, you should be able to:

- write a representation invariant as precise, separable clauses;
- distinguish type, structural, semantic, ownership, and derived-state clauses;
- choose an invariant strong enough to define `AF` and justify operations;
- prove establishment by creators and preservation by mutators;
- analyze normal, exceptional, cancellation, and callback paths;
- state where transient violations may exist and why they cannot escape;
- implement an independent, side-effect-free representation checker;
- design invariant-directed tests and corruption probes;
- explain the limits of runtime checking, static types, and testing;
- scope human review for invariants used in high-stakes structures.

## Core Exposition

Let `R` denote all concrete states expressible by the implementation language. A representation invariant is a predicate `RI : R -> {true, false}`. Its valid region is `V = {r in R | RI(r)}`. The abstraction function is usually partial over `R` but total over `V`: `AF : V -> A`, where `A` is the abstract state space. It need not assign meaning to a corrupt pointer graph or an array with impossible metadata.

Consider a queue stored as an array `data`, a head index `h`, and a cached size `n`. Field types alone allow negative `n`, `h` beyond the array, and `n` larger than capacity. A more useful invariant might require nonnegative capacity, `0 <= n <= len(data)`, a canonical empty head, and a rule identifying exactly which circular positions contain live values. The abstraction function then reads those `n` positions in logical order. Each clause exists because interpretation or an operation needs it.

An invariant can be too weak. “`n >= 0`” does not ensure indexing is safe or that `n` matches live elements. It can also be unnecessarily strong. Requiring unused array cells to contain `None` may force clearing values even if `AF` ignores unused cells and no security or retention requirement demands clearing. Stronger invariants can simplify reasoning but increase mutation cost and exclude useful representations. The right invariant is sufficient, maintainable, and connected to an obligation.

A practical invariant often has several kinds of clauses:

1. **Type and domain clauses:** capacities are integers, priorities are finite, keys satisfy equality/hash assumptions.
2. **Shape clauses:** a root is null exactly for an empty tree; reachable nodes form an acyclic tree; array indexes are in range.
3. **Ordering or semantic clauses:** search-tree keys respect bounds; heap parents precede children; counts are positive.
4. **Cross-field clauses:** cached size equals reachable nodes; head and tail agree in the singleton case.
5. **Ownership clauses:** no mutable internal node is reachable from untrusted clients; shared nodes obey an immutability or synchronization rule.
6. **Canonicality clauses:** zero counts are absent; unused slots have a prescribed form; equivalent states are normalized.

The list should be read conjunctively. Splitting it into named clauses makes failures diagnostic and proofs compositional. It also supports an invariant register mapping each operation to clauses it reads, may temporarily break, and must re-establish.

Creators establish the base case. A constructor, factory, parser, clone operation, and deserializer are all creators because each introduces a representation that clients can observe. Merely checking the ordinary constructor misses alternate entry points. A deserializer must distrust bytes and establish current invariants; it cannot assume that an old file or hostile input already obeys them.

Mutators provide the induction step. Assume `RI(r)` and the operation precondition. Follow every control-flow path. Show that a normal successor satisfies every clause, and analyze failure behavior. If an operation does not return normally, decide whether `r` is unchanged, whether a valid documented successor exists, or whether the object is deliberately quarantined. This proof is local: by induction, all states reachable through the abstraction's public operations remain valid.

Observers ordinarily do not alter the abstract value, but they can still threaten representation validity. Lazy caches, move-to-front heuristics, path compression, iterator bookkeeping, and reference-count changes mutate concrete state. An observer that returns a live internal list causes representation exposure. Thus operation categories describe abstract effects, not necessarily concrete writes.

Many algorithms temporarily violate `RI`. During a tree rotation, parent pointers may briefly disagree. During array insertion, a slot may be written before the cached size changes. This is acceptable only inside a boundary with exclusive ownership: no callback, iterator, signal handler, concurrent reader, exception escape, or reentrant method may observe the state. A useful design either keeps each small step valid, constructs a new valid candidate and swaps atomically, or uses rollback/finalization that covers every exit.

Assertions help but do not define the contract. Python's [simple-statement specification](https://docs.python.org/3/reference/simple_stmts.html#the-assert-statement) defines `assert` in terms of `__debug__` and notes that generated assertion code can be omitted under optimization. Therefore assertions are appropriate for detecting implementation defects during checked runs, not for validating untrusted input or enforcing public preconditions. Explicit exceptions remain necessary at trust boundaries.

The checker should be side-effect-free, deterministic for a fixed state, and sufficiently independent. If `push` increments `size` and `check_rep` merely tests that `size` was incremented, both can share the same mistake. Recomputing `len(items)` provides an independent oracle for the cross-field clause. For graphs, a checker can traverse with an identity set to detect cycles and recompute size. Expensive checks may run in tests, debug builds, sampling, or offline audits rather than on every production operation.

Static types and ownership systems can make some invalid states unrepresentable. A nonempty type can exclude the empty case; an enum can restrict tags; lifetimes or borrow rules can limit aliases. Yet many invariants quantify over values or graphs—sortedness, balance, uniqueness, acyclicity, checksum agreement—and remain beyond ordinary types. The engineering goal is not to choose one technique exclusively, but to push each clause into the strongest practical enforcement layer.

Immutability changes the preservation argument. Once a deeply immutable valid value exists, later mutation cannot corrupt it. But construction still must establish `RI`, and “frozen” may be shallow. Python's [`dataclasses` documentation](https://docs.python.org/3/library/dataclasses.html#frozen-instances), checked 2026-08-29, describes `frozen=True` as emulating immutability by adding assignment/deletion guards; it does not recursively freeze referenced objects. A frozen record containing a mutable list can still have its list changed.

Concurrency requires a time model. “`size` equals node count” might hold whenever a lock is released but not at each instruction. Lock-free structures can contain helping descriptors or marked nodes that would be invalid in a sequential representation. Their invariant must cover those protocol states, and correctness needs linearizability or another declared concurrent specification. Applying a sequential checker without quiescence can report a mixture of different moments.

Persistence extends the boundary across versions and failures. An on-disk invariant may include magic/version fields, length bounds, ordering, checksums, and reachability from a committed root. Crash consistency asks which states storage can expose after interruption. Write ordering, journaling, or copy-on-write roots become preservation mechanisms. Reopening is a creator: validate enough structure before trusting offsets or allocating from encoded lengths.

## Definitions and Notation

Let:

- `A` be the set of abstract values;
- `R` be the set of representable concrete states;
- `RI(r)` mean concrete state `r` is valid;
- `V = {r in R | RI(r)}` be the valid representation space;
- `AF : V -> A` be the abstraction function;
- `pre_op(a, x)` be the abstract precondition for operation input `x`;
- `op_A(a, x) = (a', y)` be the abstract transition and result;
- `op_R(r, x) = (r', y_R)` be its concrete implementation when it returns normally.

Correct correspondence requires `AF(r') = a'` and equivalent observable results `y_R ~= y` whenever `RI(r)`, `a = AF(r)`, and the precondition hold. If the contract promises termination, total correctness also requires termination. For an exceptional result, replace the normal relation with the contract's specified failure transition.

An **inductive** invariant satisfies a base condition and a step condition over the declared transitions. An **asserted** property can be true in sampled executions without being inductive. A **derived field** duplicates information computable from authoritative state. A **validity boundary** is a program point at which `RI` must hold. **Ownership** is authority to mutate representation state. **Reentrancy** occurs when control calls back into the same abstraction before an operation finishes.

## Mechanisms, Invariants, or Proof Structure

The central proof structure has five obligations.

**1. Sufficiency.** Show that `RI` makes `AF` total and implementation reads safe. If `AF` traverses next pointers until null, acyclicity and link validity are relevant. If a minimum operation calls numeric comparison, the priority domain must support that comparison.

**2. Establishment.** For every creator `c`, prove `RI(c(x))` when its precondition holds. Include empty, singleton, full-capacity, deserialized, copied, and migrated creation routes as applicable.

**3. Preservation.** For every operation, assume `RI(r)` and the operation precondition. Prove all public successors satisfy `RI`. A frame argument identifies untouched clauses; changed clauses receive direct reasoning.

**4. Correspondence.** Show the concrete result and successor implement the abstract transition through `AF`. Preserving an invariant is necessary but insufficient: a queue that discards the newest rather than oldest element may remain structurally valid while implementing the wrong ADT.

**5. Encapsulation.** Show no external mutation path can create a state outside `V`. Analyze constructor arguments, returned references, iterators, callbacks, subclasses, reflection/unsafe code, concurrency, serialization, and foreign-function boundaries.

The executable model uses a bounded stable priority collection. Its representation is a list of triples `(priority, sequence, value)`, a capacity, a cached size, and the next sequence number. The invariant requires exact built-in integer metadata, nonnegative bounds, `size = len(entries) <= capacity`, finite numeric priorities excluding booleans, unique nonnegative sequence numbers below `next_sequence`, and increasing allocation history. List order is not meaningful; the abstraction is the multiset of entries with stable minimum order determined by `(priority, sequence)`.

<!-- bijux-verify: {"id":"bounded-priority-invariant","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"removed=urgent,second\nremaining=((2.0, 0, 'routine'),)\nfull=priority collection is full\ninvalid=priority must be finite\n","stderr":""}} -->
```python
import math


class BoundedPriority:
    def __init__(self, capacity):
        if type(capacity) is not int or capacity < 0:
            raise ValueError("capacity must be a nonnegative integer")
        self._capacity = capacity
        self._entries = []
        self._size = 0
        self._next_sequence = 0
        self._check_rep()

    def _check_rep(self):
        assert type(self._capacity) is int and self._capacity >= 0
        assert type(self._size) is int
        assert self._size == len(self._entries)
        assert 0 <= self._size <= self._capacity
        assert type(self._next_sequence) is int and self._next_sequence >= 0
        sequences = []
        for priority, sequence, _value in self._entries:
            assert type(priority) in (int, float)
            assert math.isfinite(priority)
            assert type(sequence) is int
            assert 0 <= sequence < self._next_sequence
            sequences.append(sequence)
        assert len(sequences) == len(set(sequences))

    def add(self, priority, value):
        if type(priority) not in (int, float) or not math.isfinite(priority):
            raise ValueError("priority must be finite")
        if self._size == self._capacity:
            raise OverflowError("priority collection is full")
        candidate = (float(priority), self._next_sequence, value)
        self._entries.append(candidate)
        self._next_sequence += 1
        self._size += 1
        self._check_rep()

    def remove_min(self):
        if self._size == 0:
            raise IndexError("priority collection is empty")
        index = min(
            range(self._size),
            key=lambda position: self._entries[position][:2],
        )
        _priority, _sequence, value = self._entries.pop(index)
        self._size -= 1
        self._check_rep()
        return value

    def snapshot(self):
        self._check_rep()
        return tuple(sorted(self._entries))


queue = BoundedPriority(3)
queue.add(2, "routine")
queue.add(1, "urgent")
queue.add(1, "second")
print(f"removed={queue.remove_min()},{queue.remove_min()}")
print(f"remaining={queue.snapshot()}")
queue.add(3, "later")
queue.add(4, "last")
try:
    queue.add(5, "overflow")
except OverflowError as error:
    print(f"full={error}")
try:
    queue.add(float("nan"), "bad")
except ValueError as error:
    print(f"invalid={error}")
```

The program checks observed traces, not all possible traces. Its checker uses `assert`, so it is diagnostic rather than a public validation mechanism. It does not protect against reflective mutation of private-by-convention fields, malicious values whose callbacks mutate the object, memory corruption, concurrency, process failure, or exhaustion between operations. Those limitations define where additional ownership, synchronization, fault containment, static analysis, or formal proof is required.

For `add`, input validation and capacity rejection occur before mutation. Given the invariant, appending a fresh sequence preserves uniqueness and the bounds after size increments. For `remove_min`, nonemptiness ensures the range is nonempty; removing one entry and decrementing size preserves equality and capacity. Neither operation reuses a sequence, so every remaining sequence stays below `next_sequence`. Stable equal-priority behavior follows from selecting the minimum pair `(priority, sequence)`. This is a proof sketch; a line-by-line review must also consider every exception-capable expression and the language's numeric semantics.

## Alternatives and Trade-Offs

**Weak versus strong invariants.** A weak invariant admits more representations and can make updates cheaper, but shifts complexity into every operation. A strong invariant simplifies observers and proofs but may require eager normalization or maintenance. Lazy deletion, for example, can allow marked entries until compaction; then the invariant and `AF` must explicitly account for them.

**Always-valid versus transiently invalid updates.** Keeping `RI` after each primitive step reduces exception and reentrancy risk. Candidate construction followed by an atomic swap is often clearest but costs memory. In-place multi-step mutation can be fastest, yet demands exclusive ownership, rollback, or a protocol invariant covering intermediate states.

**Eager versus sampled checking.** Checking after every operation localizes faults but may be asymptotically expensive. Debug-only checking gives strong development feedback. Production sampling can detect rare corruption without paying every time, while offline full scans suit persistent structures. None substitutes for prevention when corruption has severe consequences.

**Executable versus declarative specifications.** A `check_rep` function is concrete and testable. Mathematical predicates can quantify over abstract reachability, histories, or concurrency behaviors that are impractical to recompute. Keeping both aligned avoids reducing the specification to whatever is cheap to test.

**Canonical versus permissive valid states.** Canonical representations simplify equality, serialization, and diagnostics. Permissive states may enable faster updates and structural sharing. If zero-count map entries are allowed, `AF` can ignore them, but memory use and iteration must be specified. Canonicality should serve an owned requirement.

**Redundant metadata versus recomputation.** Cached size gives constant-time observation but requires preservation. Recomputing from nodes removes a cross-field invariant but costs traversal. Hardware, workload, contention, and fault impact determine the trade-off.

**Internal repair versus fail-fast detection.** A checker can sometimes rebuild a cache or discard malformed indexes. Silent repair may hide defects or choose the wrong abstract value when sources disagree. Repair is appropriate only when authority and recovery semantics identify a trustworthy source; otherwise quarantine and diagnosis are safer.

## Failure Modes and Misconceptions

1. **“The types are the invariant.”** Types express domains, not usually ordering, uniqueness, reachability, balance, or cross-field agreement.
2. **“If `AF` can interpret it, it is valid.”** `RI` may also protect operational safety, resource bounds, ownership, canonicality, or promised complexity.
3. **“Observers need no preservation proof.”** Lazy caches, compression, iterators, and returned aliases can mutate concrete state.
4. **“An assertion enforces the API.”** Assertions may be disabled and signal implementation defects; explicit validation enforces caller obligations.
5. **“Check only the field just changed.”** A mutation can violate a distant relationship such as parent links, cached summaries, or global uniqueness.
6. **“A failed operation changes nothing automatically.”** Comparators, allocators, callbacks, cancellation, and partial I/O can fail after mutation begins.
7. **“Private naming guarantees ownership.”** Reflection, unsafe code, returned references, subclass hooks, and shared mutable inputs can bypass conventions.
8. **“The invariant must hold at every instruction.”** Owned transient violations can be valid designs, but the precise observation and failure boundary must be stated.
9. **“A passing checker proves correctness.”** It proves only that implemented predicates held for sampled states under the executed environment.
10. **“More clauses always mean safer code.”** Unnecessary clauses increase coupling and proof burden and can prevent useful representations without protecting a requirement.

## Worked Examples

### Example 1

**Question:** Write an invariant for an array-backed stack with fields `items`, `top`, and fixed `capacity`, where `top` is the next free index.

**Reasoning:** Require exact nonnegative integer capacity, `len(items) = capacity`, and `0 <= top <= capacity`. Live elements occupy `items[0:top]`; later slots are outside `AF`. Requiring them to be `None` is optional unless retention or canonical serialization matters.

**Conclusion:** Bounds and a live-region definition are essential; unused-cell clearing is a policy-dependent strengthening.

### Example 2

**Question:** Why is “a binary-search tree has comparable keys” insufficient?

**Reasoning:** It does not rule out cycles, shared nodes, invalid child references, or misplaced keys. A sufficient invariant requires an acyclic owned tree plus bounds: every key in a left subtree is below the node key and every key in a right subtree follows the chosen duplicate policy.

**Conclusion:** Value-domain clauses do not replace shape and global-order clauses.

### Example 3

**Question:** A linked list caches `size`. Insertion increments `size` before allocating the node, and allocation fails. What happened?

**Reasoning:** The old links remain but the cache changed, violating `size = reachable nodes`. Allocate and initialize an unlinked node first, then perform the nonfailing publication steps, or roll back the count on every failure path.

**Conclusion:** Order mutation steps so fallible work precedes invariant-breaking publication.

### Example 4

**Question:** Can a circular queue use `head = tail` for both empty and full states?

**Reasoning:** Not without another discriminator. A cached size, a reserved empty slot, or a generation/full flag can distinguish the states. The chosen invariant must explain the encoding; otherwise `AF` is ambiguous.

**Conclusion:** An invariant must make abstract interpretation unambiguous.

### Example 5

**Question:** A frozen record contains `tags: list[str]`. Is its “tags never change” invariant enforced?

**Reasoning:** Preventing assignment to `record.tags` does not prevent `record.tags.append(...)`. The referenced list remains mutable. Use an immutable tuple, defensive copying plus nonexposure, or an ownership regime that makes mutation impossible.

**Conclusion:** Shallow freezing is not deep immutability.

### Example 6

**Question:** A graph checker counts nodes with recursive traversal but has no visited set. Can it validate acyclicity?

**Reasoning:** On a cycle it may recurse forever rather than report corruption; on shared subgraphs it may double-count. Track object identity with visiting and visited states: an edge to visiting detects a cycle, while an edge to visited identifies sharing that the invariant may allow or forbid.

**Conclusion:** The checker itself must terminate and distinguish the graph shapes named by `RI`.

### Example 7

**Question:** A map accepts a mutable key whose hash changes after insertion. Which invariant fails?

**Reasoning:** Bucket placement must correspond to the key's current equality and hash behavior. Mutation can make lookup search a different bucket. Either require stable hash/equality for resident keys, own immutable key snapshots, or reindex on controlled change.

**Conclusion:** Representation invariants may constrain client-supplied element behavior, not only container fields.

### Example 8

**Question:** May a tree rotation temporarily leave a child with the wrong parent pointer?

**Reasoning:** Yes, if the mutation owns the entire tree, no observation or exception can escape during the interval, and all exit paths restore agreement. No, if a callback, concurrent reader, or reentrant observer can run then. Candidate rewiring or locking can strengthen the boundary.

**Conclusion:** Transient invalidity is justified by an explicit atomicity and ownership argument.

### Example 9

**Question:** A radiation-treatment scheduler maintains a priority structure of treatment events. Is an internal `check_rep` plus unit tests enough to approve a new representation?

**Reasoning:** No. The invariant must cover clinical ordering, ties, duplicates, cancellation, time units, overflow, persistence, recovery, and concurrency. Evidence needs requirements traceability, formal or independently reviewed preservation arguments, adversarial and fault-injection tests, target-system timing, migration validation, and named clinical-domain, safety, software, and independent verification reviewers under the applicable assurance process. This chapter performs no external human review.

**Conclusion:** High-stakes invariant claims require domain-specific human judgment and system evidence beyond generic data-structure checks.

### Example 10

**Question:** An on-disk free list is corrupt, but every allocated record is readable. May startup silently rebuild it?

**Reasoning:** Only if allocated-record reachability is the declared authority and a complete scan can distinguish live from free space. If both metadata sources can be stale after a crash, automatic repair may overwrite live data. A journal, committed root, or offline recovery policy must establish precedence.

**Conclusion:** Repair is sound only when the invariant identifies an authoritative source and a valid recovery transition.

## Cross-Program Connections

Representation invariants specialize program correctness to hidden state. [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) uses the same inductive pattern for loop and algorithm invariants, but its observation points differ. [Programming Languages & Semantics](../../01-programming-languages-and-semantics/ROADMAP.md) supplies type abstraction, ownership, and effect mechanisms that enforce boundaries.

[Software Engineering: Patterns](../../11-software-engineering-patterns/ROADMAP.md) studies modules, aggregates, factories, repositories, and concurrency patterns that assign invariant ownership. Patterns help only when the invariant is explicit; a factory that leaves another mutation path open does not establish control.

[Database Engineering](../../18-database-engineering/ROADMAP.md) extends invariants to pages, indexes, constraints, logs, and crash recovery. [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) replaces instantaneous global checks with protocol invariants over replicas and histories. [Security Engineering](../../25-security-engineering/ROADMAP.md) treats invariant bypass, malformed deserialization, integer overflow, and memory corruption as attack surfaces.

Testing connects executable checks with evidence. Property-based generation can produce operation sequences and check `RI` after every step. Model-based differential testing compares `AF(r)` with a simple reference model. Mutation testing can deliberately remove preservation steps and determine whether tests detect the resulting invalid state. These methods increase confidence but do not convert finite execution into a universal proof.

## References

- C. A. R. Hoare, [*Proof of Correctness of Data Representations*](https://ora.ox.ac.uk/objects/uuid%3A496c86ab-dbfd-4901-b2dd-e94fc4f42e51), *Acta Informatica* 1(4), 271–281, 1972. Primary foundation for proving abstract properties through concrete representations.
- Barbara Liskov and Stephen Zilles, [*Programming with Abstract Data Types*](https://doi.org/10.1145/942572.807045), SIGPLAN Notices 9(4), 1974. Primary account of language-supported data abstraction.
- Barbara Liskov and John V. Guttag, [*Abstraction and Specification in Program Development*](https://mitpress.mit.edu/9780262121125/abstraction-and-specification-in-program-development/), MIT Press, 1986. Systematic treatment of abstraction functions, invariants, specification, and modular development.
- John V. Guttag, [*Abstract Data Types and the Development of Data Structures*](https://doi.org/10.1145/359605.359618), *Communications of the ACM* 20(6), 1977. Primary treatment of algebraic specifications for data structures.
- Robert C. Martin et al., MIT 6.031, [*Abstraction Functions & Rep Invariants*](https://web.mit.edu/6.031/www/fa18/classes/11-abstraction-functions-rep-invariants/), Fall 2018. University teaching treatment connecting `AF`, `RI`, representation exposure, and `checkRep`.
- Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein, [*Introduction to Algorithms*, fourth edition](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/), MIT Press, 2022. Durable correctness and data-structure foundations.
- Python Software Foundation, [*The assert statement*, Python 3.14.7 Language Reference](https://docs.python.org/3/reference/simple_stmts.html#the-assert-statement), checked 2026-08-29. Official current semantics of `assert` and `__debug__`.
- Python Software Foundation, [*Frozen instances*, Python 3.14.7 `dataclasses` documentation](https://docs.python.org/3/library/dataclasses.html#frozen-instances), checked 2026-08-29. Official current characterization and limits of generated frozen-instance behavior.

## Exercises

### Exercise 1

A bounded buffer stores an array `slots`, an integer `count`, and capacity `k = len(slots)`. State a minimal representation invariant if live values always occupy the prefix `slots[0:count]`.

### Exercise 2

A singly linked set stores `head` and cached `size`. Duplicates are forbidden. Derive a `check_rep` traversal that terminates even on corrupt cyclic input, and state what it must compare.

### Exercise 3

Diagnose this mutator: a sorted collection appends a new value, calls a user-supplied comparison key while sorting in place, then updates its cached minimum. Identify invariant and failure-path hazards and propose a safer structure.

### Exercise 4

Compare two queue designs: one maintains a canonical contiguous live prefix after every operation; the other uses a circular array with head and size. Give invariants, preservation costs, and checking trade-offs for both.

### Exercise 5

An autonomous warehouse vehicle stores collision-avoidance waypoints in a mutable spatial tree. A team wants to add concurrent updates and background compaction. Specify the invariant layers, evidence, and named human-review roles required before claiming the design safe.

## Answers to the Exercises

### Answer 1

Require `type(count) is int` and `0 <= count <= k`, with `k` a nonnegative fixed capacity equal to `len(slots)`. Define the live region as exactly indexes `0` through `count - 1` and `AF` as the sequence `slots[0:count]`. If empty slots may retain old references, no value restriction after `count` is needed for functional interpretation; add clearing only for a confidentiality, retention, garbage-collection, or canonicality requirement. If `None` may be a valid live value, it cannot serve as an implicit occupancy marker.

### Answer 2

Traverse by object identity with a `seen` set. Before processing a non-null node, reject it if its identity is already in `seen`; otherwise add it, validate its payload domain, check that no equal payload has already appeared, increment a recomputed count, and advance. At null, require recomputed count to equal cached `size` and `size >= 0`. Comparing identities detects structural cycles even when node equality is overloaded; a separate value set or pairwise comparison enforces uniqueness according to the set's declared equality semantics. The checker must not call mutation-capable client code unless that risk is owned.

### Answer 3

Appending first breaks sortedness. The user key can raise, reenter the collection, mutate an element, or return inconsistent values while the representation is invalid. In-place sort itself may have partially rearranged the list when an exception escapes, and the cached minimum remains stale. Safer designs validate and compute keys before publication, build and sort a candidate list without exposing it, validate the candidate, derive its minimum, then swap the complete valid state under exclusive ownership. Alternatively insert at a precomputed position after all fallible callbacks finish. The public contract must constrain key stability and specify failure behavior.

### Answer 4

The contiguous design requires `0 <= size <= capacity` and declares `array[0:size]` live in queue order. Dequeue shifts remaining values, making preservation `O(n)` but interpretation and checking simple. The circular design requires `0 <= head < capacity` when capacity is positive, `0 <= size <= capacity`, a canonical rule for zero capacity, and live logical element `i` at `(head + i) mod capacity`. Enqueue and dequeue preserve it in `O(1)`, but wraparound, empty/full distinction, and checking are more complex. Both can recompute bounds cheaply; only the contiguous form can validate layout with one slice. Clearing unused cells is a separate retention policy in either design.

### Answer 5

Separate invariants into spatial semantics (every active waypoint appears once with correct coordinates and safety radius), tree shape and bounding summaries, ownership/lifetime of nodes, concurrency protocol states, background-compaction states, and persistence/recovery if state survives restart. Define quiescent and operation-time validity boundaries, linearization points or another concurrency specification, reclamation rules, and how readers treat nodes being moved. Evidence should include an abstraction relation to a simple waypoint set, establishment/preservation review for updates and compaction, race and linearizability testing, adversarial geometry, cancellation and crash injection, memory-reclamation analysis, target-hardware latency, end-to-end collision scenarios, and rollback/migration tests. Named reviewers should include a vehicle-control/domain engineer, a functional-safety or hazard-analysis engineer, a concurrency/data-structure specialist, the system test owner, and any independent assurance authority required by the operational regime. Passing generic unit tests or the local checker alone is insufficient; this model answer records no external human approval.
