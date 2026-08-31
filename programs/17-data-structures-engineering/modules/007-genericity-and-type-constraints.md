---
module_id: DSE-007
program: Data Structures Engineering
level: 1
module_number: 7
title: Genericity and Type Constraints
status: complete
last_verified: 2026-08-29
---

# Genericity and Type Constraints

## One-Page Review

### Governing question

How can one data-structure abstraction support many element, key, allocator, or policy types while requiring exactly the operations and semantic laws needed for correctness, safety, and useful performance?

### Essential definitions

- A **type parameter** is a placeholder for a type supplied when a generic abstraction is instantiated.
- A **constraint** states capabilities or relationships required of an admissible type or value.
- A **bound** relates a parameter to an interface, trait, protocol, class, lifetime, or type set.
- A **semantic law** is a behavioral requirement—such as transitive equality or stable hashing—not guaranteed merely by method presence.
- **parametricity** is uniform behavior across types when an implementation cannot inspect or assume type-specific operations beyond its interface.
- **variance** describes how subtyping of type arguments affects subtyping of constructed types.
- **monomorphization** specializes generic code for concrete type arguments; **erasure** or **dictionary dispatch** shares code through erased representations or runtime operation tables.
- **boxing** stores a value indirectly in a uniform heap/reference representation; **unboxing** stores its value representation directly where supported.
- A **policy parameter** supplies behavior such as comparison, hashing, allocation, growth, or reclamation.
- **heterogeneous lookup** queries a structure with a type different from the stored key while preserving a compatible equivalence/order relation.

### Central model, mechanism, or theorem

Define a generic ADT family (D[T]) over admissible types

$$
\mathcal T_C=\{T\mid T\text{ supplies operations }C_{op}\text{ and satisfies laws }C_{law}\}.
$$

For an ordered set, `compare` must do more than type-check. Its induced relation must satisfy the structure's declared ordering laws, and equivalent keys must remain equivalent while resident. For a hash map, equality and hashing must satisfy

$$
x\equiv y\implies hash(x)=hash(y),
$$

with stability and domain requirements stated. The type system may enforce operation availability; lawfulness generally needs proof, trusted contracts, tests, or restricted constructors.

### Critical invariants

- Constraints are derived from operations and representation invariants, not copied from implementation convenience.
- Read-only, write-only, and mutable interfaces expose variance only when their operations make substitution sound.
- Equality, hashing, comparison, cloning, destruction, serialization, and thread-safety requirements include semantic laws and failure behavior.
- Keys do not change in ways that invalidate their stored hash bucket or ordering position.
- Comparator/hash/policy objects have explicit identity, state, lifetime, determinism, reentrancy, and concurrency contracts.
- Generic algorithms do not assume object identity, byte layout, zero values, nullability, or cheap copying unless constrained.
- Type erasure, boxing, specialization, and monomorphization preserve abstract behavior while documenting layout/code-size/dispatch costs.
- Heterogeneous lookup uses a relation compatible with the one that built the structure.
- Serialization persists a versioned value schema, not compiler-specific generic instantiations or raw type metadata.
- Passing generic examples demonstrates selected instantiations, not universal lawfulness across all types.

### Common failures

Common failures are treating a method signature as proof of equality/order laws; constraining every element to be comparable when only one operation needs it; assuming mutable generic containers are covariant; hashing mutable keys; accepting NaN into an unqualified total order; using subtraction as a comparator and overflowing; making a stateful comparator differ between insertion and lookup; equating cloning with deep independence; assuming generics remove boxing; and exposing implementation type names as durable formats.

### Compact example

A sequence needs no ordering for append or indexed access. A `sort` operation may require a comparison only for that call. By contrast, a binary search tree needs one stable ordering policy for all insertions and lookups because representation validity depends on it. Giving the whole sequence type an ordering bound unnecessarily excludes useful elements; giving the tree no law contract permits silent corruption.

### Connections

[DSE-001](001-abstract-data-types-and-concrete-representations.md) supplies ADT families, [DSE-002](002-representation-invariants.md) supplies law-dependent validity, [DSE-003](003-operation-contracts.md) supplies callback and substitution rules, and [DSE-004](004-time-space-and-allocation-cost.md) supplies representation-cost accounting. DSE-008 applies constraints to iterators.

## Governing Question

What does a structure truly need to know about its elements, and which parts can be abstracted without sacrificing invariants, ownership safety, useful layout, or predictable behavior?

Generic syntax can make `Map<K,V>` compile, but the semantic contract lives below the angle brackets. Keys need an equality/hash or ordering relationship. Stored values need ownership and destruction behavior. Concurrent variants need send/share guarantees. Persistent variants need safe sharing. Serializers need schemas. Constraints are therefore part of data-structure correctness, not only compiler ergonomics.

## Why This Matters

Overconstraint reduces reuse and can force expensive representations. A stack does not need comparable elements. A graph search may need hashability for one visited-set strategy, not for the graph ADT. Requiring cloning can hide allocation and identity changes.

Underconstraint is worse: an invalid comparator can make an ordered tree unreachable, a mutable hash key can become unfindable, and unsafe sharing can create races. Production APIs need the narrowest sufficient capabilities plus explicit laws, failure behavior, and representation consequences.

## Prerequisites and Retrieval

You should understand types, interfaces, functions, equality, ordering, hashing, ownership/aliasing, and DSE-001 through DSE-006. Retrieve:

1. Syntactic availability of an operation does not prove its algebraic laws.
2. An invariant may depend on element behavior remaining stable over time.
3. Mutable producers and consumers have different safe subtype relationships.
4. Representation and dispatch strategy can change time, memory, and code size.
5. A callback is executable code with failure, state, reentrancy, and concurrency behavior.

## Learning Objectives

After completing this module, you should be able to:

- derive minimal generic constraints from ADT operations and invariants;
- distinguish syntactic bounds from semantic laws;
- specify lawful equality, hashing, total/strict-weak ordering, and compatibility;
- reason about covariance, contravariance, invariance, and read/write capabilities;
- compare monomorphization, erasure, boxing, dictionary dispatch, and type erasure;
- design policy parameters without making behavior unstable or unreviewable;
- specify heterogeneous lookup and key-view compatibility;
- handle nullability, ownership, cloning, destruction, and thread-safety constraints;
- test generic structures across representative and hostile types;
- review evolution/serialization without exposing compiler-specific representation.

## Core Exposition

**Start with the ADT, not language syntax.** A generic stack family (Stack[T]) stores finite sequences of values from (T). `push`, `pop`, and `top` need storage/lifetime operations but not equality, ordering, or hashing. A `contains(x)` extension needs an equivalence relation for that call. A `sorted()` extension needs ordering. Place requirements at the narrowest operation boundary when the representation invariant does not depend on them.

A hash set is different: bucket placement and duplicate detection depend on equality/hash throughout residence. An ordered tree depends on a stable ordering during every update/search. Those constraints belong to the structure's type/policy because changing them can invalidate its representation.

**Operation constraints versus laws.** An interface can require methods `eq`, `hash`, or `compare`. The compiler may verify signatures and lifetimes, but usually cannot establish reflexivity, symmetry, transitivity, determinism, or consistency. State laws explicitly.

For equality relation (\equiv), typical set/map laws are:

- reflexive: (x\equiv x);
- symmetric: (x\equiv y\Rightarrow y\equiv x);
- transitive: (x\equiv y\land y\equiv z\Rightarrow x\equiv z).

Some domains deliberately use partial/nonreflexive comparisons—for example IEEE NaN under ordinary equality. Then do not advertise a mathematical equivalence relation without normalization/wrapper policy.

Hash compatibility requires equal keys to hash equally. Unequal keys may collide. Hash stability while resident is essential: mutating fields used by equality/hash can strand an entry in a bucket not searched under its new hash. Defensive copying, immutable key types, identity hashing, or controlled reindexing are possible policies.

**Ordering laws.** An ordered structure needs a relation matching its algorithms. A total order compares every pair consistently and is antisymmetric/transitive under the chosen formulation. Many language libraries specify a strict weak ordering: irreflexive, transitive “less than,” with transitive equivalence induced by incomparability. Do not casually substitute one for the other.

A three-way comparator should return negative/zero/positive by relation, not compute `a-b` in a fixed-width type where subtraction can overflow. It must be deterministic for the structure's lifetime and agree with equality if the ADT claims one key per equality class. Locale-sensitive or time-varying collation requires pinned policy/version.

If a comparator considers two distinct objects equivalent, an ordered set must define which spelling/value is retained and how lookup/removal behaves. Ordered maps can legitimately use order-equivalence rather than language object equality, but clients must know.

**Policy objects.** Hashers, comparators, allocators, growth strategies, and reclamation policies can be type or value parameters. They improve reuse and testability but become part of representation identity. Two trees built with different comparators cannot be merged blindly.

Stateful policies need ownership, copying, equality, serialization, exception, reentrancy, and thread-safety rules. A random hash seed can be per process or per container; persistence must not assume bucket layout survives a seed change. A comparator callback that mutates the structure during comparison can violate invariants.

**Parametricity and representation independence.** When generic code can only store, return, and rearrange opaque `T` values, it cannot invent arbitrary values or inspect fields without capabilities. This uniformity supports reasoning. Reflection, runtime type tests, serialization, unsafe casts, pointer identity, and specialization weaken pure parametric reasoning and must be declared.

Representation independence says clients relying on the generic ADT contract should not distinguish an array versus linked implementation except through promised observations/resources. Type erasure or specialization may change layout and timing while preserving abstract behavior.

**Variance.** Suppose `Cat` is a subtype of `Animal`. A read-only sequence of cats can often be used where a read-only sequence of animals is expected: covariance. A consumer accepting any animal can often serve where a cat consumer is needed: contravariance. A mutable list both produces and consumes `T`, so treating `List[Cat]` as `List[Animal]` would allow insertion of a dog, violating the original list.

Therefore mutable generic containers are commonly invariant, while read-only views can be covariant. Use-site projections/wildcards or separate producer/consumer interfaces recover safe flexibility. Variance is a consequence of operations, not a naming preference.

Arrays in some languages are covariant with runtime store checks; this preserves type safety through dynamic failure but introduces exceptions and does not make mutable covariance substitutable in the stronger behavioral sense.

**Nullability and bottom values.** If `null`, `None`, or an uninitialized marker is admitted as an element, empty lookup/pop needs a tagged result or separate success flag. Using a default/sentinel value can collapse two abstract outcomes. Non-null bounds simplify representations but exclude valid domains; state them.

Some generic types have invalid bit patterns, alignment needs, destructors, pinning, or move restrictions. Low-level containers must obey construction/destruction and initialization rules. A byte-copy optimization needs a trait/constraint guaranteeing bitwise relocation, not mere genericity.

**Ownership, cloning, and destruction.** Storing a value can move ownership, borrow/reference it, retain/share it, or clone it. These choices affect lifetime, identity, allocation, failure, and aliasing. `Clone` or copying does not necessarily mean deep independence; clones can share internal state.

Destructors/finalizers can execute code, throw in some ecosystems, block, or reenter. Clearing a generic container invokes element destruction according to language rules. Failure and ordering must be considered when externally observable.

Persistent structures can share immutable nodes, but element objects may remain mutable unless constrained. A “persistent map” guarantees container versions, not deep immutability of arbitrary referenced values.

**Concurrency constraints.** A generic concurrent structure must specify whether elements/keys/policies can be transferred across threads and accessed concurrently. Languages express this through traits, marker interfaces, ownership, runtime checks, or documentation. A type marked sendable does not guarantee its equality callback is fast, nonblocking, or reentrancy-safe.

Memory reclamation may impose lifetimes, pinning, hazard, epoch, or destructor constraints. DSE-061 onward develops concurrent structures; here the rule is that generic element behavior participates in the concurrency proof.

**Implementation strategies.** Monomorphization generates/specializes machine code and often unboxes concrete values, enabling inlining/vectorization at possible code-size and compile-time cost. Erasure uses a shared representation/API, often boxing primitive/value types and inserting casts. Dictionary/witness-table dispatch passes implementations of required operations. JITs can specialize erased generics dynamically.

Do not infer performance solely from the language category. Optimizers can devirtualize, share monomorphized code, scalar-replace boxes, or fail to specialize. Measure code size, allocation, dispatch, layout, and hot-path behavior under the actual toolchain as DSE-004/006 require.

Type erasure can hide a concrete iterator/comparator behind an existential wrapper. It stabilizes APIs and reduces generic code exposure but can allocate, add indirection, constrain cloning, and erase capabilities. The erased wrapper must preserve lifetime and semantic laws.

**Specialization.** A generic structure can use optimized representations for small integers, trivially copyable values, or zero-sized types. Specialization must preserve the same abstract contract and error behavior unless the API says otherwise. Representation-specific iteration order or serialization must not leak accidentally.

Special cases can introduce coherence/overlap problems in languages with trait implementations: two applicable implementations need deterministic selection. Maintenance cost and testing matrix grow with specializations.

**Heterogeneous lookup.** A map storing owned strings may permit lookup by a borrowed string view, avoiding allocation. The borrowed query's hash and equality must be compatible with stored-key semantics. For ordered structures, comparison between query and key must induce the same ordering used to build the tree.

Compatibility includes normalization, case folding, locale, encoding, and version. A case-insensitive query against a case-sensitive map is not merely a cheaper key type; it asks a different equivalence question.

**Generic algorithms and iterators.** Constraints can describe iterator category/capabilities: single pass, multipass, bidirectional, random access, exact size, mutable reference, contiguous span. An algorithm should require the weakest capability it uses. Binary search needs random access for its standard index behavior or another cost analysis; a fold needs only iteration.

Associated types express element/reference/error types coupled to a collection. Higher-order callbacks add their own laws, effects, and failure contracts. DSE-008 develops traversal protocols.

**Dynamic typing and structural protocols.** Runtime/duck-typed code can be generic through operations rather than static parameters. Structural protocols describe required members without nominal inheritance. Runtime errors, tests, and documentation bear more of the constraint burden; semantic laws remain equally necessary.

Static types can also be unsoundly bypassed through casts/reflection/foreign code. Treat type checking as one evidence layer, not complete proof of data-structure validity.

**Testing generic lawfulness.** Test representative classes: small/large values, immutable/mutable keys, colliding hashes, equivalent-but-distinct keys, boundary numeric values, NaN/signed zero if admitted, stateful/throwing/reentrant callbacks, noncopyable/resource-owning values, zero-sized types, and concurrency markers.

Property tests exercise equality/hash/order laws over generated samples and compare operation traces with a reference model. They can find counterexamples, not prove all values/callbacks. Restrict construction to known-lawful wrappers or use formal verification for stronger evidence.

Compile-time tests can assert accepted/rejected instantiations and variance. Binary/code-size/allocation benchmarks compare implementation strategies. Serialization tests pin schema and forbid compiler-specific type names unless deliberately versioned.

**API evolution.** Adding a type bound breaks existing instantiations. Removing a bound can be source-compatible but expose new behavior/representations. Changing comparator defaults, hash/equality, nullability, variance, boxing, or specialization can break semantics, ABI, persistence, and performance.

Public formats should encode domain schema/version, not mangled generic type identities or in-memory layouts. Migrations validate every type argument, policy, and historical invariant.

The executable model below uses one key-function capability to insert values after existing equal-key values. It demonstrates selected numeric and string instantiations and stability; it cannot prove the key function defines a lawful total order for all inputs.

<!-- bijux-verify: {"id":"generic-stable-insertion","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"numeric=(1, 2, 2, 3)\nlength_order=('a', 'cc', 'bbb')\nstable_equal=('a', 'b', 'c')\nconstraint=key_returns_total_ordered_values\nevidence=finite_examples_not_lawfulness_proof\n","stderr":""}} -->
```python
def insert_ordered(values, value, key):
    result = list(values)
    target = key(value)
    index = 0
    while index < len(result) and key(result[index]) <= target:
        index += 1
    result.insert(index, value)
    return tuple(result)


numeric = insert_ordered((1, 2, 3), 2, lambda value: value)
length_order = insert_ordered(("a", "bbb"), "cc", len)
tagged = insert_ordered(((2, "a"), (2, "b")), (2, "c"), lambda value: value[0])
print(f"numeric={numeric}")
print(f"length_order={length_order}")
print(f"stable_equal={tuple(value[1] for value in tagged)}")
print("constraint=key_returns_total_ordered_values")
print("evidence=finite_examples_not_lawfulness_proof")
```

## Definitions and Notation

Let generic family (D:T\mapsto D[T]). Constraint environment (C(T)) combines syntactic capabilities, associated types/lifetimes, and semantic predicates. An operation may introduce an additional local constraint (C_{op}(T)) without constraining the entire family.

Equivalence (\equiv_T), hash (h_T), and strict order (<_T) are policy-indexed. Hash compatibility is (x\equiv_T y\Rightarrow h_T(x)=h_T(y)). Strict weak order additionally requires irreflexivity/transitivity and transitive incomparability equivalence under the applicable library definition.

For type constructor (F), covariance means (S<:T\Rightarrow F[S]<:F[T]); contravariance reverses the constructed relation; invariance provides neither. Actual language rules may use declaration-site, use-site, or inferred variance.

## Mechanisms, Invariants, or Proof Structure

**Constraint derivation.** List every operation performed on `T`, every representation clause depending on `T`, and every callback/lifetime/concurrency need. Remove constraints not required by the public family; attach operation-local constraints locally.

**Law preservation.** Assume lawful policy at construction, prove each operation uses that same compatible policy and prevents resident mutation that changes equivalence/hash/order position.

**Variance check.** Classify each occurrence of `T` as produced, consumed, or both. Demonstrate substitution with an attempted write/read; reject variance that permits a value outside the original element domain.

**Representation correspondence.** For monomorphized, boxed, erased, and specialized forms, define abstraction functions and prove equivalent results/errors/frames while measuring distinct resource costs.

**Heterogeneous lookup.** Prove cross-type relation/hash agrees with stored-key equivalence and ordering for all admitted query/key pairs; examples alone are calibration.

**Finite evidence boundary.** The snippet exercises three finite key functions and values. It does not verify totality, transitivity, exception behavior, mutable keys, typing, performance, or arbitrary policies.

## Alternatives and Trade-Offs

**Family-level versus operation-level constraints.** Family bounds simplify implementation and error messages but overconstrain unrelated operations. Local bounds maximize reuse at API complexity cost.

**Nominal versus structural constraints.** Nominal traits/interfaces centralize intent and law documentation. Structural protocols adapt existing types easily but can match accidental members; neither proves laws.

**Built-in order versus comparator policy.** Built-in bounds simplify use. Explicit policies support alternate orderings and unorderable types but add identity, storage, compatibility, failure, and serialization concerns.

**Monomorphization versus erasure/dictionaries.** Specialization can improve layout/inlining and increase code/compile size. Shared code reduces duplication but may box/dispatch. Actual optimizers blur the distinction.

**Mutable versus immutable generic views.** Mutability enables updates and forces invariant variance/ownership. Read-only interfaces support broader safe covariance and sharing.

**Homogeneous versus heterogeneous collections.** Homogeneous parameters enable specialized operations/layout. Existential/tagged unions support mixed values at dispatch, storage, and capability complexity.

**Static versus dynamic enforcement.** Static constraints reject classes before execution; dynamic checks adapt flexibly. Semantic laws, external mutation, and unsafe boundaries still require other evidence.

## Failure Modes and Misconceptions

1. **“Generic means any type.”** Every implementation has capability, layout, lifetime, or behavior requirements.
2. **“Implements Comparable proves an order.”** Signatures do not prove laws.
3. **“Hash collisions violate the contract.”** Equal values need equal hashes; unequal values may collide.
4. **“Mutable hash keys are fine if rarely changed.”** One relevant mutation can make entries unreachable.
5. **“All numeric values form an ordinary total order.”** NaN and domain-specific equivalence require policy.
6. **“Comparator subtraction is safe.”** Fixed-width overflow can reverse order.
7. **“List[Cat] is a List[Animal].”** Mutable insertion makes that covariance unsound.
8. **“Clone means deep copy.”** Clones may share internal objects/resources.
9. **“Generics eliminate boxing.”** Implementation strategy/toolchain decides.
10. **“Monomorphization is always faster.”** Code size, instruction cache, sharing, and optimization vary.
11. **“Heterogeneous lookup changes only input type.”** It must preserve equivalence/hash/order semantics.
12. **“Thread-safe container accepts any element safely.”** Element/policy behavior participates in concurrency.
13. **“Static typing proves runtime representation safety.”** Unsafe/foreign/reflection and semantic laws remain.
14. **“Tests across several types prove generic correctness.”** They sample instantiations and laws only.

## Worked Examples

### Example 1

**Question:** Does a stack require equality?

**Reasoning:** Push/pop/top preserve and return values without comparing them. `contains` can add an operation-local equivalence requirement.

**Conclusion:** Do not impose family-wide equality unnecessarily.

### Example 2

**Question:** Why can a mutable hash key disappear?

**Reasoning:** Mutation changes hash/equality while the entry remains in its old bucket; lookup probes according to the new hash.

**Conclusion:** Resident key semantics must remain stable or trigger controlled reindexing.

### Example 3

**Question:** Why is `return a-b` a bad integer comparator?

**Reasoning:** Fixed-width subtraction can overflow and yield a sign inconsistent with mathematical order.

**Conclusion:** Compare relationally or use a safe three-way primitive.

### Example 4

**Question:** Why is mutable `List[Cat]` not safely covariant?

**Reasoning:** An `Animal` client could insert a dog, violating the actual cat-list element invariant.

**Conclusion:** Producer/consumer operations determine variance.

### Example 5

**Question:** Can a read-only cat sequence be covariant?

**Reasoning:** It only produces cats, each usable as an animal, and offers no operation accepting arbitrary animals.

**Conclusion:** Separate read-only views can expose safe flexibility.

### Example 6

**Question:** What does an explicit comparator become part of?

**Reasoning:** Tree shape/validity, equivalence classes, lookup, merge compatibility, serialization assumptions, and concurrency/reentrancy.

**Conclusion:** Policies are representation identity, not disposable callbacks.

### Example 7

**Question:** Why can lookup by string view avoid allocation?

**Reasoning:** It compares/hashes borrowed characters against owned stored strings under the same equivalence without constructing an owned key.

**Conclusion:** Heterogeneous lookup needs cross-type law compatibility.

### Example 8

**Question:** Does a persistent generic map make values immutable?

**Reasoning:** Old map topology/value references persist, but referenced mutable objects can still change through aliases.

**Conclusion:** Container persistence and deep element immutability differ.

### Example 9

**Question:** What does the executable stable insertion prove?

**Reasoning:** For three selected key functions, it places the new item after existing keys less than or equal to its key and emits expected tuples.

**Conclusion:** It does not prove total-order laws or safety for arbitrary callbacks.

### Example 10

**Question:** A generic priority structure schedules medical actions. What exceeds type constraints?

**Reasoning:** Engineers verify comparator laws, units, overflow, stability, key mutation, failure, concurrency, serialization, specialization, timing, and implementation identity. Clinical and safety experts validate priority policy, ties, deadlines, overrides, and hazards; security, human-factors, quality, and regulatory reviewers validate their scopes. This chapter claims none.

**Conclusion:** Type-correct generic code cannot establish domain or deployment safety.

## Cross-Program Connections

- [Object-Oriented Programming](../../02-programming-languages-object-oriented-programming/ROADMAP.md) develops subtyping, variance, interfaces, and dynamic dispatch.
- [Functional Programming](../../03-programming-languages-functional-programming/ROADMAP.md) develops parametricity, type classes, higher-order constraints, and persistent values.
- [Systems Programming](../../05-programming-languages-systems-programming/ROADMAP.md) owns layout, ownership, lifetimes, monomorphization, and unsafe generic code.
- [Theory of Programming](../../07-programming-languages-theory-of-programming/ROADMAP.md) supplies type soundness, relational reasoning, and refinement.
- [Compilers & Language Implementation](../../08-compilers-and-language-implementation/ROADMAP.md) implements erasure, specialization, dictionaries, layout, and code generation.
- [Concurrent & Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) owns send/share, synchronization, and reclamation constraints.

## References

1. Rust Project, [*The Rust Reference: Generic parameters*](https://doc.rust-lang.org/reference/items/generics.html). Current type, const, and lifetime parameter rules.
2. Rust Project, [*The Rust Programming Language: Traits*](https://doc.rust-lang.org/book/ch10-02-traits.html). Trait bounds, associated behavior, blanket implementation, and conditional methods.
3. ISO C++ working draft, [Constraints and concepts](https://eel.is/c++draft/temp.constr). Current constraint normalization, satisfaction, subsumption, and concept rules.
4. ISO C++ working draft, [Sorting and related operations](https://eel.is/c++draft/alg.sorting). Current comparator, projection, ordering, and algorithm requirements.
5. Oracle, [Java Language Specification SE 25: Type arguments and parameterized types](https://docs.oracle.com/javase/specs/jls/se25/html/jls-4.html#jls-4.5). Generic type formation, bounds, erasure context, and subtyping foundations.
6. Oracle, [Java Tutorials: Generics, inheritance, and subtypes](https://docs.oracle.com/javase/tutorial/java/generics/subtyping.html). Invariance and generic subtype relationships.
7. Python Software Foundation, [`typing`: Generics](https://docs.python.org/3/library/typing.html#generics). Type variables, variance, protocols, bounds, constraints, and runtime limitations.
8. Go Project, [*The Go Programming Language Specification: Type parameter declarations*](https://go.dev/ref/spec#Type_parameter_declarations). Type parameters, constraints, type sets, inference, and instantiation.
9. Swift Project, [*The Swift Programming Language: Generics*](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/generics/). Generic functions/types, constraints, associated types, and where clauses.
10. Barbara Liskov and Jeannette Wing, [*A Behavioral Notion of Subtyping*](https://www.cs.cmu.edu/~wing/publications/LiskovWing94.pdf), ACM TOPLAS, 1994. Behavioral replacement and history/property constraints.

## Exercises

### Exercise 1

Derive minimal constraints for stack, sequence with `contains`, hash set, ordered map, and persistent vector. Separate family-level and operation-level needs.

### Exercise 2

State equality/hash and ordering laws for a case-insensitive string key. Address Unicode normalization/case folding, original spelling, version, and heterogeneous string-view lookup.

### Exercise 3

Use producer/consumer reasoning to determine variance for read-only sequence, write-only sink, mutable list, and immutable persistent collection whose elements may themselves be mutable.

### Exercise 4

Design a cross-language experiment comparing monomorphized/unboxed and erased/boxed generic sequences. Isolate representation, dispatch, allocation, and code-size effects and state limitations.

### Exercise 5

Prepare a verification plan for adding a comparator policy to a previously built-in ordered structure. Cover laws, migration, persistence, concurrency, hostile callbacks, specialization, compatibility, and human review.

## Answers to the Exercises

### Answer 1

Stack needs storage/lifetime/ownership capabilities only. A general sequence likewise; `contains` adds operation-local equivalence unless membership indexes are representation state. Hash set needs stable equivalence and compatible stable hash family-wide. Ordered map needs one stable lawful order/cross-key policy family-wide. A persistent vector needs safe value retention/sharing and version lifetime; it does not inherently need equality/order/hash or deep element immutability. Serialization, cloning, thread transfer, or sorting should add local constraints unless the representation/contract universally depends on them.

### Answer 2

Define a versioned canonical comparison key from declared Unicode normalization and full case-folding policy; equality is equality of canonical keys, hence must be reflexive/symmetric/transitive over admitted strings. Hash the same canonical key so equal strings hash equally. Preserve original spelling separately and define which spelling a set/map retains for equivalent insertions. Pin Unicode/policy version and migrate/reindex when it changes. A borrowed view lookup must produce/compare the identical canonical semantics without dangling storage or partial encoding; malformed sequences and allocation/folding failures have explicit outcomes. Locale-specific collation is a different policy and cannot silently substitute.

### Answer 3

A read-only sequence only produces `T` and can be covariant where the language supports it. A write-only sink consumes `T` and can be contravariant. A mutable list both consumes and produces and is invariant. An immutable persistent collection topology can expose a covariant read-only interface because updates return new collections; however, if it exposes mutation through element references or accepts callbacks consuming a narrower type, those operations affect variance. Covariance does not make referenced mutable elements deeply immutable or prevent alias-visible mutation.

### Answer 4

Implement semantically identical sequence kernels for a primitive/value type and reference type, using the language's specialized and erased paths where available. Pin source/toolchain/flags/runtime/GC/allocator/hardware. Validate outputs; inspect generated code/layout/assembly; measure element stride, object/box allocations, live/peak bytes, dispatch/inlining, cycles/instructions, throughput/tails, binary/code size, compile/startup cost, and cold/warm behavior across sizes. Avoid comparing different algorithms or vectorized library versus interpreter loop. Results characterize those toolchains and workloads; optimizers/JITs may specialize erasure or share monomorphized code, and finite measurements do not prove universal strategy superiority.

### Answer 5

Freeze old order/equality, iteration, duplicate, lookup, error, complexity, concurrency, and serialized semantics. Define comparator operation and exact laws, equivalence relationship, determinism, state/lifetime, copying, exceptions, reentrancy, thread safety, and heterogeneous compatibility. Decide whether policy identity participates in equality/merge and persist a stable policy/schema ID rather than function pointers/type names. Validate existing data under the new policy, rebuild indexes atomically, version formats, support rollback, and reject incompatible merges. Property-test order laws and model traces with boundary numeric, NaN if admitted, equivalent distinct, stateful/throwing/reentrant/slow comparators; fuzz corruption and inject failure. Test specializations and concurrent histories; measure timing/code/allocation. Independent type-system, data-structure, concurrency, security, persistence/API, operations and domain reviewers approve their scopes; high-stakes use needs relevant safety/quality/regulatory review, and no finite law test proves arbitrary callback correctness.
