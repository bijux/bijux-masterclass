---
module_id: DSE-001
program: Data Structures Engineering
level: 1
module_number: 1
title: Abstract Data Types and Concrete Representations
status: complete
last_verified: 2026-08-29
---

# Abstract Data Types and Concrete Representations

## One-Page Review

### Governing question

How can a program promise the behavior of a data structure without making clients depend on the structure's storage layout?

### Essential definitions

- An **abstract data type** (ADT) is a set of abstract values together with operations and laws that define their observable behavior.
- A **concrete representation** is the implementation state used to encode abstract values in memory or storage.
- An **abstraction function** maps a valid concrete state to the abstract value it represents.
- A **representation invariant** identifies which concrete states are valid encodings.
- An **operation contract** states preconditions, results, state changes, and exceptional behavior at the abstract boundary.
- **Observational equivalence** means that no allowed client observation can distinguish two states or implementations.
- A **representation leak** exposes a concrete detail that clients can observe or mutate outside the ADT contract.

### Central model, mechanism, or theorem

Let abstract states be `A`, concrete states be `R`, valid states satisfy `RI(r)`, and the abstraction function be `AF : R_valid -> A`. A concrete operation `op_R` correctly implements abstract operation `op_A` when, for every valid input state satisfying the operation's precondition, `op_R` terminates as promised, preserves `RI`, and its observable result and successor state agree with `op_A` after applying `AF`.

### Critical invariants

- Every reachable concrete state is inside the domain of `AF`.
- Constructors establish the representation invariant.
- Mutating operations preserve it or leave the object unchanged when they fail.
- Public observations depend on the abstract value, not accidental layout.
- Aliases returned to clients cannot bypass the abstraction boundary.
- Two implementations advertised as the same ADT satisfy the same semantic contract, including errors.

### Common failures

Common errors are calling any class an ADT, specifying only method names, returning a mutable backing collection, confusing object identity with abstract equality, allowing invalid states between public calls, treating asymptotic cost as the ADT's meaning, and testing only one representation instead of the abstract laws.

### Compact example

A set ADT contains unique values and supports membership, insertion, and removal. One representation may be a sorted array; another may be a hash table. Their layouts, iteration costs, and update mechanisms differ. They implement the same ADT only if the contract's observations—including whether iteration order is promised—agree.

### Connections

[DSE-002](../ROADMAP.md) develops representation invariants, while [DSE-003](../ROADMAP.md) formalizes operation contracts. ADTs depend on language-level abstraction from [Programming Languages & Semantics](../../01-programming-languages-and-semantics/ROADMAP.md), algorithmic reasoning from [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md), and durable interface boundaries from [Software Engineering: Patterns](../../11-software-engineering-patterns/ROADMAP.md).

## Governing Question

Programs manipulate bits, addresses, array slots, nodes, pages, and machine words. Clients rarely want to reason at that level. They want a stack whose latest pushed item is the next popped item, a map associating keys with values, or a priority queue returning a minimum element. The governing engineering problem is to separate those two descriptions without losing correctness: state the client-visible mathematical behavior, choose an efficient encoding, and establish that the encoding implements the behavior.

Liskov and Zilles's 1974 paper, [*Programming with Abstract Data Types*](https://doi.org/10.1145/942572.807045), made this separation a programming-language concern: a programmer should be able to introduce data abstractions whose use does not reveal their representation. Guttag's [*Abstract Data Types and the Development of Data Structures*](https://doi.org/10.1145/359605.359618) showed how algebraic specifications can describe operations independently of a storage structure. The durable idea is not a particular class syntax. It is that clients program against meaning, and implementers discharge the obligation that concrete transitions preserve that meaning.

## Why This Matters

Representation independence permits change. A library can replace a list-backed set with a hash table, inline small values, compress pointers, add caching, or move data off heap without rewriting correct clients. This is more than maintainability. It is a control on the proof surface: client reasoning uses the abstract laws; representation reasoning is localized behind the boundary.

The separation also reveals when two structures are not interchangeable. A mathematical set does not define iteration order. If an API promises insertion-ordered iteration, order has become part of its abstract state. A hash set whose order changes after resizing may still implement the mathematical set ADT but not that richer API. Conversely, two implementations can have different time, allocation, and concurrency properties while matching functional observations. Correct substitution therefore depends on the whole published contract, not a shared noun.

Data-structure failures frequently cross the boundary. Returning a backing list allows a caller to create duplicates in a purported set. Hashing a mutable key can strand it in the wrong bucket. Serializing private node shape can turn an implementation detail into a long-lived wire contract. In safety-critical software, an apparently harmless representation change can alter overflow, ordering, or aliasing behavior. The ADT discipline forces these effects to be named and reviewed.

## Prerequisites and Retrieval

You should be able to read small Python programs, reason about sets, sequences, finite maps, and functions, and distinguish a mathematical value from its encoding. Recall that a function maps each input in its domain to exactly one output, an invariant is a predicate intended to remain true across allowed transitions, and a precondition is an obligation placed on a caller. Familiarity with asymptotic notation helps with engineering comparisons, but this chapter treats performance as a separate contract dimension rather than the definition of the ADT.

## Learning Objectives

After completing this module, you should be able to:

- define an ADT by its values, operations, laws, and error behavior;
- distinguish an ADT, an interface, a class, and a concrete data structure;
- write an abstraction function and representation invariant for a simple structure;
- state the commuting obligation between abstract and concrete operations;
- identify observable behavior and accidental representation detail;
- judge whether two concrete implementations are observationally equivalent;
- detect representation exposure through aliases, equality, iteration, and serialization;
- design conformance tests from abstract laws instead of implementation shape;
- explain which performance and resource properties belong in an engineering contract;
- scope human review when a representation participates in a high-stakes system.

## Core Exposition

An ADT begins with abstract values. For a stack over element set `E`, values are finite sequences over `E`; operations include creating an empty stack, pushing, inspecting the top, popping, and testing emptiness. Laws relate those operations: pushing `x` and then observing the top returns `x`; popping after pushing restores the previous abstract sequence. These statements do not mention an array, linked nodes, a capacity field, or a memory allocator.

An interface is a syntactic boundary: names, parameters, result types, visibility, and perhaps declared exceptions. It can support an ADT, but syntax alone is insufficient. Two methods named `remove(x)` can mean “remove one occurrence,” “remove all occurrences,” or “return a new collection without `x`.” Python's current `collections.abc` documentation explicitly notes that complex interfaces include semantics and method relationships that cannot be inferred merely from method presence. The semantic contract is what turns an interface into an implementation of a particular abstraction.

A class is one language mechanism for grouping state and operations. An ADT need not be a class: a module with opaque handles, a functional value with exported functions, a process protocol, or a database table behind a service can establish the same separation. A class also need not be an ADT implementation if clients freely inspect and mutate all fields. Encapsulation machinery helps enforce the boundary; it does not define its meaning.

A concrete representation chooses machine-manipulable state. Consider a bag, or multiset, whose abstract value is a finite function `B : E -> N` giving each element's multiplicity. One representation stores every occurrence in a list. Another stores one dictionary entry per distinct value with a positive count. For the list representation, the abstraction function counts equal occurrences. For the dictionary representation, it reads the stored counts. Different concrete states can map to the same abstract bag: `['red', 'blue', 'red']` and `{'red': 2, 'blue': 1}` do so.

The abstraction function is a reasoning device, not necessarily executable code. It says what each valid representation means. It need not be one-to-one: several array layouts may represent the same set because order is abstractly irrelevant. It must be defined for every valid reachable state. If a representation contains a cache, free-list, or tombstone, `AF` normally ignores those fields except where they affect the abstract value.

The representation invariant restricts the concrete domain. A count-map bag may require every key to have a strictly positive integer count and the total size field to equal the sum of counts. A circular buffer may require `0 <= size <= capacity`, indices within bounds, and a relationship among head, tail, and size. Invalid bit patterns can exist in the host language, but correct constructors and operations keep public execution within valid states.

Operation correctness connects the two levels. Suppose abstract `add(B, x)` produces a bag whose count of `x` is one larger and whose other counts are unchanged. A concrete list implementation may append `x`; a count-map implementation may increment a cell. For each valid concrete `r`, applying the concrete operation and then abstracting must yield the same value as abstracting first and applying the abstract operation. This is often called a commuting diagram because the two routes reach the same abstract result.

Queries have a similar obligation. If `count(x)` is promised to return `B(x)`, it cannot return the number of dictionary buckets or the first matching array index. Error behavior is observable too. If `remove(x)` on an absent element promises a `KeyError` and no state change, silently returning or partially mutating fails the contract even if successful removals work.

Abstraction boundaries constrain observations. Public method results, raised errors, equality, iteration order, textual forms promised as stable, serialization, callbacks, timing promises, memory limits, and concurrency semantics can all be observable. What is abstract depends on the declared contract. A stack that promises only `push`, `pop`, `top`, and `is_empty` may change its internal capacity invisibly. An API exposing `capacity()` has made some allocation state observable.

Equality deserves special care. Representation equality asks whether concrete fields match. Abstract equality asks whether two states denote the same abstract value. Two set arrays with different element orders can be abstractly equal. Python's data model requires objects that compare equal to have equal hashes, and warns against hashing mutable objects by mutable values. That language rule is a concrete manifestation of an abstract law needed by hash-based clients.

Representation exposure occurs when clients acquire authority over internal state. Returning the actual list behind a stack lets a client delete its bottom element without invoking an operation. Retaining a caller-owned mutable list without documenting ownership lets the caller mutate the object indirectly. Defenses include copying, immutable views, iterators with precise mutation rules, opaque handles, ownership types, and disciplined module boundaries. Each has cost; the central requirement is that the chosen defense matches the contract.

Observational equivalence supplies the replacement criterion. Two implementations are equivalent relative to an observer set when every legal sequence of operations produces matching allowed observations. “Relative” matters. If clients can measure exact allocation counts, two representations may be distinguishable even when values match. If the contract only gives upper complexity bounds, different exact timings need not violate it. A representation-independent client uses only allowed observations, so replacing one correct implementation with another preserves its conclusions.

Modern engineering adds resource contracts to the functional model. Big-O bounds, worst-case latency, maximum capacity, allocation behavior, persistence, thread safety, determinism, and side-channel constraints may be part of a usable abstraction. They should not be smuggled into the mathematical value definition, but neither should they be dismissed as mere details when clients rely on them. Later DSE modules develop those dimensions. Here the rule is: distinguish functional meaning from nonfunctional guarantees, then specify both where required.

## Definitions and Notation

Let `A` be the set of abstract values and `R` the set of possible concrete states. Let `RI : R -> {true, false}` be the representation invariant. Define `R_valid = {r in R | RI(r)}`. The abstraction function is `AF : R_valid -> A`.

For an abstract operation `f_A : A x X -> A x Y` and its concrete implementation `f_R : R_valid x X -> R x Y`, correctness requires, for every allowed `r` and input `x`:

1. `f_R(r, x)` satisfies its termination and error contract;
2. if it succeeds with `(r', y_R)`, then `RI(r')`;
3. if `f_A(AF(r), x) = (a', y_A)`, then `AF(r') = a'` and `y_R` agrees with `y_A`;
4. if it fails, the failure and resulting state match the abstract contract.

An **observer** is an allowed context that produces a public result from an ADT value. Concrete states `r1` and `r2` are observationally equivalent, written `r1 ~= r2`, when every allowed observer gives the same contract-level result. A **creator** produces a new value, a **query** observes without abstract mutation, and a **command** may change the abstract value. These categories describe semantics; a query may still update an invisible cache.

A **representation independence argument** shows that clients using only the abstraction cannot distinguish two implementations related by an appropriate simulation or abstraction relation. This chapter gives proof structures and small finite checks, not a machine-checked universal proof.

## Mechanisms, Invariants, or Proof Structure

The core proof obligation has four parts. First, define the abstract state and operations without concrete fields. Second, define `RI` and `AF`. Third, prove initialization: every constructor result satisfies `RI` and represents the promised abstract value. Fourth, prove preservation and correspondence for each public operation. Queries must return abstractly correct observations; commands must produce a valid representation of the abstract successor.

For the count-map bag, let concrete state be `(counts, size)`. Its invariant is: every stored count is a positive integer, `size` is a nonnegative integer, and `size = sum(counts.values())`. Its abstraction function maps absent keys to zero and present keys to their stored counts. `add(x)` either inserts count one or increments an existing count, then increments size. `remove(x)` rejects absent values without mutation; otherwise it decrements both count and size and deletes a zero count. These cases establish preservation.

The executable model below compares a repeated-list representation and a count-map representation under the same command trace. The equality of one trace is empirical evidence, not a proof for all traces. The assertions also check each representation's local invariant after every mutation.

<!-- bijux-verify: {"id":"bag-representation-equivalence","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"equivalent=True\nsnapshot=(('blue', 1), ('red', 1))\nsize=2 count(red)=1\nmissing=green\n","stderr":""}} -->
```python
class ListBag:
    def __init__(self):
        self.items = []

    def add(self, value):
        self.items.append(value)
        assert self.size() == len(self.items)

    def discard_one(self, value):
        if value not in self.items:
            raise KeyError(value)
        for index, item in enumerate(self.items):
            if item == value:
                del self.items[index]
                break

    def count(self, value):
        return self.items.count(value)

    def size(self):
        return len(self.items)

    def snapshot(self):
        return tuple(sorted((value, self.count(value)) for value in set(self.items)))


class CountBag:
    def __init__(self):
        self.counts = {}
        self.total = 0

    def _check(self):
        assert all(type(count) is int and count > 0 for count in self.counts.values())
        assert self.total == sum(self.counts.values())

    def add(self, value):
        self.counts[value] = self.counts.get(value, 0) + 1
        self.total += 1
        self._check()

    def discard_one(self, value):
        if value not in self.counts:
            raise KeyError(value)
        self.counts[value] -= 1
        self.total -= 1
        if self.counts[value] == 0:
            del self.counts[value]
        self._check()

    def count(self, value):
        return self.counts.get(value, 0)

    def size(self):
        return self.total

    def snapshot(self):
        return tuple(sorted(self.counts.items()))


bags = [ListBag(), CountBag()]
for action, value in [("add", "red"), ("add", "blue"),
                      ("add", "red"), ("discard", "red")]:
    for bag in bags:
        if action == "add":
            bag.add(value)
        else:
            bag.discard_one(value)

print(f"equivalent={bags[0].snapshot() == bags[1].snapshot()}")
print(f"snapshot={bags[0].snapshot()}")
print(f"size={bags[0].size()} count(red)={bags[0].count('red')}")
try:
    bags[1].discard_one("green")
except KeyError as error:
    print(f"missing={error.args[0]}")
```

The example intentionally uses comparable, hashable strings. The list representation can support unhashable values; the dictionary representation cannot without changing its key mechanism. Therefore “all Python values” is not a valid shared domain. Likewise, sorting the snapshot is a testing observer, not necessarily a bag operation. A real contract must state element requirements and exposed observations.

## Alternatives and Trade-Offs

**Algebraic versus model-based specification.** Algebraic laws state relationships among operations, such as `top(push(s, x)) = x`. Model-based specifications map values to familiar mathematics such as sequences or finite maps. Algebraic forms can hide representation completely; models can make state transitions easier to visualize. Both need defined preconditions and error behavior.

**Opaque modules versus classes.** Modules with hidden representation can enforce a strong boundary. Classes integrate dispatch and per-instance state but may expose fields, reflection, inheritance hooks, or subclass obligations. The choice is language- and ecosystem-dependent; neither syntax automatically guarantees abstraction.

**Mutable versus immutable values.** Mutable ADTs model commands as state transitions and require alias discipline. Immutable ADTs return new abstract values, simplifying some reasoning and enabling structural sharing, but allocation and retention behavior become important. Immutability prevents in-place mutation; it does not by itself prevent representation exposure through mutable components.

**Canonical versus noncanonical representations.** A canonical representation gives each abstract value one normal concrete form, simplifying equality and serialization. Maintaining normalization can cost time. Noncanonical forms may support faster updates but require abstract equality and careful testing. Sets stored in arbitrary array order are a simple example.

**Nominal versus structural conformance.** Nominal systems require an explicit declaration or inheritance relationship. Structural systems accept values that provide required operations. Structural matching improves flexibility, but method presence cannot establish semantic laws. Conformance tests and documentation remain necessary in either approach.

**Rich versus minimal interfaces.** A minimal operation set reduces commitments and proof obligations. Convenience operations can prevent inefficient client compositions and express atomic actions, but each new observer narrows future representation choices. Expose an operation when it has stable semantic value, not merely because one representation makes it easy.

## Failure Modes and Misconceptions

1. **“ADT” means “class.”** A class is syntax and dispatch; an ADT is a semantic specification plus a boundary.
2. **Matching method names implies substitutability.** Names and types do not establish laws, mutation behavior, ordering, or failures.
3. **Private naming prevents leaks.** Aliases, iterators, callbacks, serialization, debugging hooks, and reflection can still expose representation.
4. **The abstraction function must be executable.** It is a mathematical interpretation; executable checks may approximate it for testing.
5. **Every concrete state needs meaning.** `AF` needs to cover valid reachable states, not arbitrary corrupt bit patterns; `RI` defines that boundary.
6. **One passing trace proves equivalence.** Testing samples behavior. A universal claim requires reasoning over all allowed states and operation sequences.
7. **Iteration order is never part of a set.** It is absent from the mathematical set but becomes abstract behavior if the API promises it.
8. **Performance is only an implementation detail.** It is separate from functional meaning, yet promised bounds and resource limits are client-visible obligations.
9. **Copying always fixes exposure.** Shallow copying can retain aliases to mutable elements, and copying may violate required cost or identity semantics.
10. **Representation changes are internal by definition.** Persisted encodings, wire formats, equality, hashes, and exception details may have made the representation public.

## Worked Examples

### Example 1

**Question:** Define a stack as an ADT without choosing storage.

**Reasoning:** Abstract values are finite sequences. `empty()` returns the empty sequence. `push(s, x)` appends `x`; `top` returns the last element when nonempty; `pop` removes it; `is_empty` tests sequence length zero. Underflow behavior must also be named.

**Conclusion:** The stack's LIFO meaning is independent of arrays or nodes.

### Example 2

**Question:** Can `[a, b]` and `[b, a]` represent the same set?

**Reasoning:** Yes, if the invariant forbids duplicates and the abstraction function discards order. No, if ordered iteration is promised. Equality depends on abstract observations, not spelling alone.

**Conclusion:** Representation equivalence is relative to the declared contract.

### Example 3

**Question:** A set method returns its backing list “for efficiency.” What breaks?

**Reasoning:** A caller can append a duplicate or remove an element without the set's operations. The representation invariant and any cached size can become false. Returning an immutable snapshot or controlled iterator preserves less authority.

**Conclusion:** Exposing a mutable backing object destroys the abstraction boundary.

### Example 4

**Question:** Does an array-backed queue remain the same ADT after changing to a ring buffer?

**Reasoning:** It does if enqueue, dequeue, front, capacity/error behavior, order, and promised resource properties remain equivalent. Index wraparound and unused slots are concrete. A changed fixed-capacity rejection policy would be observable.

**Conclusion:** Mechanism may change freely only inside the complete contract.

### Example 5

**Question:** Why can a query legally mutate a cache?

**Reasoning:** Abstractly, a query preserves the value. Concretely, it may memoize a derived result while `AF` ignores cache state and `RI` requires any valid cache entry to agree with the value. Thread-safety or memory promises may still constrain this mutation.

**Conclusion:** Abstract immutability and concrete bitwise immutability are different claims.

### Example 6

**Question:** A bag removes an absent element silently in one implementation and raises in another. Are they equivalent?

**Reasoning:** Error behavior is observable. Unless the contract explicitly permits either result, a client can distinguish the implementations with one call.

**Conclusion:** Exceptional outcomes belong to ADT semantics.

### Example 7

**Question:** A dictionary stores zero-count bag entries. Is that automatically invalid?

**Reasoning:** Not automatically. One `RI` may forbid zeros for canonicality; another may allow them and let `AF` ignore them. The latter expands valid states but complicates equality, iteration, and space reclamation.

**Conclusion:** Representation invariants are design choices justified by proof and engineering needs.

### Example 8

**Question:** How should two bag implementations be tested together?

**Reasoning:** Generate legal command sequences, apply both, and compare contract-level observations after each step. Include duplicates, absent removal, empty state, repeated values, and alias probes. Do not compare private fields.

**Conclusion:** Differential testing should use an abstract oracle, not representation identity.

### Example 9

**Question:** A medication scheduler replaces an ordered dose queue with a hash-based collection. Is value membership enough evidence?

**Reasoning:** No. Dose order, duplicate handling, time comparison, overflow, persistence, and failure behavior may affect patient safety. The representation and migration require named clinical-domain, safety, and software reviewers plus system-level tests; this chapter supplies no such external review.

**Conclusion:** High-stakes representation substitution requires domain-specific human review beyond generic ADT equivalence.

### Example 10

**Question:** A serialized tree records left and right node pointers by position. Can balancing remain private?

**Reasoning:** Once consumers store, compare, or exchange that shape, rotations alter observable bytes. A logical key-value serialization would preserve more representation freedom. Versioning can explicitly support a format migration.

**Conclusion:** Persistence can accidentally promote concrete layout into a public contract.

## Cross-Program Connections

ADTs are where data structures meet programming-language semantics. Type abstraction, modules, ownership, and parametricity determine which representation facts clients can express. Reynolds's [*Types, Abstraction and Parametric Polymorphism*](https://doi.org/10.1016/0304-0208(83)90005-7) develops the deeper relation between type abstraction and representation-independent reasoning.

Algorithm engineering consumes ADT operations and supplies implementations. An algorithm proved against a priority-queue contract can be reused across binary, d-ary, or meldable heaps when their semantics and required costs match. Software patterns such as Iterator and Adapter operate at the interface boundary, but their correctness still depends on semantic laws. Database indexes are concrete representations of abstract relations and access promises; persistence makes format evolution and compatibility explicit concerns.

Security also depends on abstraction. Secret-bearing representations can leak through timing, error distinctions, dumps, or serialization even when functional results match. Distributed systems further complicate the observer set with retries, partial failure, and concurrency. “Same ADT” must therefore be scoped to a fault and observation model.

## References

- Barbara Liskov and Stephen Zilles, [*Programming with Abstract Data Types*](https://doi.org/10.1145/942572.807045), SIGPLAN Notices 9(4), 1974. Primary formulation of programmable data abstraction.
- John V. Guttag, [*Abstract Data Types and the Development of Data Structures*](https://doi.org/10.1145/359605.359618), Communications of the ACM 20(6), 1977. Primary account of algebraic specification and representation-independent development.
- C. A. R. Hoare, [*Proof of Correctness of Data Representations*](https://ora.ox.ac.uk/objects/uuid%3A496c86ab-dbfd-4901-b2dd-e94fc4f42e51), Acta Informatica 1(4), 1972. Primary source for relating abstract properties to concrete representations.
- David L. Parnas, [*On the Criteria To Be Used in Decomposing Systems into Modules*](https://doi.org/10.1145/361598.361623), Communications of the ACM 15(12), 1972. Primary source on information hiding as a decomposition criterion.
- John C. Reynolds, [*Types, Abstraction and Parametric Polymorphism*](https://doi.org/10.1016/0304-0208(83)90005-7), 1983. Primary source on abstraction and representation-independent reasoning through types.
- Harold Abelson and Gerald Jay Sussman with Julie Sussman, [*Structure and Interpretation of Computer Programs*, second edition](https://mitpress.mit.edu/9780262510875/structure-and-interpretation-of-computer-programs/), MIT Press, 1996, especially the treatment of data abstraction.
- Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein, [*Introduction to Algorithms*, fourth edition](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/), MIT Press, 2022. Durable foundations for data structures, interfaces, and correctness.
- Python Software Foundation, [*Python 3.14.7 Data Model*](https://docs.python.org/3/reference/datamodel.html), checked 2026-08-29. Official current rules for object value, identity, equality, and hashing.
- Python Software Foundation, [*collections.abc — Abstract Base Classes for Containers*, Python 3.14.7](https://docs.python.org/3/library/collections.abc.html), checked 2026-08-29. Official current interface and mixin semantics; it cautions that complex interfaces are more than method presence.

## Exercises

### Exercise 1

Define the abstract values and operations of a finite map. State what `lookup` does for a missing key.

### Exercise 2

A stack is represented by `(items, top_index)`, where live elements occupy positions `0` through `top_index`. Give an abstraction function and a representation invariant, including the empty state.

### Exercise 3

Diagnose this set implementation: its constructor stores the caller's list directly, `add` prevents duplicates, and `elements()` returns the stored list. Give two distinct invariant-breaking traces and a repair.

### Exercise 4

Compare a sorted-array set and a hash-table set. State the shared functional ADT, representation-specific assumptions, and at least three nonfunctional contract dimensions that determine whether one can replace the other.

### Exercise 5

An autonomous train controller stores pending braking commands in an ordered array. Engineers propose a heap to reduce insertion cost. Specify the evidence and named human-review roles required before claiming the new representation is a safe substitute. Do not assume that passing unit tests is sufficient.

## Answers to the Exercises

### Answer 1

Abstract values are finite partial functions `M : K -> V`. Operations can include `empty`, `bind(M, k, v)`, `lookup(M, k)`, `contains(M, k)`, and `remove(M, k)`. `bind` replaces any previous value at `k`; other mappings remain unchanged. The contract must choose missing-key behavior. One precise choice is for `lookup` to raise `MissingKey(k)` without changing `M`, while `contains` returns false. Returning a sentinel is valid only if the sentinel cannot be confused with a stored value or the result type distinguishes the cases.

### Answer 2

Let a concrete state be `(items, top_index)` with array capacity `len(items)`. Define `RI` by `-1 <= top_index < len(items)` when capacity is positive, with all live elements occupying exactly indices `0..top_index`; for a zero-capacity array, require `top_index = -1`. Define `AF(items, top_index)` as the sequence `items[0:top_index+1]`, so the empty representation maps to the empty sequence. If unused cells retain old values, `AF` ignores them. Push must establish space or follow a declared growth/overflow rule, write at `top_index + 1`, and increment the index. Pop must reject `-1` or return the indexed value and decrement while preserving bounds.

### Answer 3

First trace: create the set from `source = ['a']`, then execute `source.append('a')`; the backing list now contains a duplicate without `add`. Second trace: call `leak = elements()` and then `leak.append('b')` or append another `'a'`; again mutation bypasses the ADT. Copy the input at construction and return an immutable view, iterator with defined behavior, or defensive copy. If elements themselves are mutable, specify whether identity or value changes matter and whether deeper copying or immutability is required. Tests should retain both aliases and attempt mutation.

### Answer 4

The shared functional ADT is a finite set with membership, insertion, removal, size, and chosen absent-element behavior; iteration order is excluded unless deliberately promised. The sorted array requires a total ordering consistent with equality. The hash table requires stable hashing consistent with equality and a collision strategy. Replacement depends on at least lookup/update bounds, memory and allocation limits, iteration determinism, worst-case behavior under adversarial keys, concurrency guarantees, and serialization compatibility. If clients rely on sorted traversal, exact latency, or accepting unhashable-but-orderable elements, the structures do not satisfy the same full contract.

### Answer 5

First define observations: command priority and deadline ordering, tie-breaking, duplicate/coalescing rules, cancellation, capacity and overflow, persistence across restart, behavior on corrupt input, concurrency, and worst-case latency. Give `RI` and `AF` for both representations and prove or rigorously review initialization, preservation, and abstract correspondence for every operation. Add differential model tests, boundary tests for empty/full states and equal priorities, adversarial sequences, fault injection, timing measurements on target hardware, migration/rollback tests, and system-level braking scenarios. A named train-control domain engineer must validate operational semantics; a functional-safety engineer must assess hazards and required assurance; a data-structure/software reviewer must inspect the implementation argument; and an independent verification authority required by the applicable railway process must approve evidence. The exact regulatory roles depend on jurisdiction and system classification. No completion claim follows from this model answer, and no external human review has been performed here.
